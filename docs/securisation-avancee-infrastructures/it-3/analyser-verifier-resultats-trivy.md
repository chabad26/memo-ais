# Analyser et vérifier les résultats Trivy

**Date de l’analyse : 1er octobre 2026**

**Statut : analyse documentaire et vérifications locales réalisées**

## Objectif

Sélectionner des résultats significatifs du rapport Trivy et vérifier si leurs
conditions d’exploitation correspondent réellement au service File Browser
2.15.0 étudié.

## Sources et périmètre

L’analyse repose sur :

- le rapport Trivy JSON produit à partir de l’ImageID
  `sha256:a68f43720ea6ff331fa4b92becced20af14b72f4c3a22ca1f764076a8e42e1a5` ;
- l’inventaire Trivy des paquets Alpine et du binaire Go ;
- le code source correspondant exactement au tag
  [`v2.15.0`](https://github.com/filebrowser/filebrowser/tree/v2.15.0) ;
- les entrées CVE, les enregistrements JSON `cvelistV5` et les avis des projets ;
- l’examen du binaire `/filebrowser` extrait de l’image ;
- un contrôle réseau du service sur `192.168.122.229:8080`.

Le rapport contient 294 associations composant–vulnérabilité. Cinq résultats ont
été retenus parce qu’ils concernent l’authentification, le serveur HTTP, la
cryptographie ou le traitement de données compressées. Cette sélection mélange
des niveaux `HIGH` et `CRITICAL` et tient compte de la fonction du composant.

## Synthèse

| CVE | Composant détecté | Sévérité / CVSS | Applicabilité au cas observé | Conclusion |
| --- | --- | --- | --- | --- |
| CVE-2020-26160 | `jwt-go` `v3.2.0` | Trivy `HIGH`, CVSS 3.1 : 7.5 | **Non pertinente** | La fonction vulnérable de contrôle d’audience n’est pas utilisée par File Browser 2.15.0 |
| CVE-2021-44716 | Go `net/http` dans `stdlib v1.16.2` | `HIGH`, CVSS 3.1 : 7.5 | **Non pertinente dans la configuration observée** | La vulnérabilité nécessite HTTP/2 ; le service répond en HTTP/1.1 et refuse le test HTTP/2 direct |
| CVE-2022-23806 | Go `crypto/elliptic` dans `stdlib v1.16.2` | Trivy `CRITICAL`, CVSS 3.1 : 9.1 | **À vérifier** | La version et le symbole sont présents, mais aucun chemin depuis une entrée attaquable n’est démontré |
| CVE-2021-3711 | OpenSSL `1.1.1k-r0` | Trivy `CRITICAL`, CVSS 3.1 : 9.8 | **Non pertinente pour le processus File Browser observé** | Le binaire est statique et la condition exige un déchiffrement SM2 avec une API OpenSSL précise |
| CVE-2022-37434 | zlib `1.2.11-r3` | Trivy `CRITICAL`, CVSS 3.1 : 9.8 | **Non pertinente pour le processus File Browser observé** | Le binaire statique ne charge pas la zlib Alpine et le code serveur ne décompresse pas avec `inflateGetHeader` |

La présence et la version affectée sont confirmées dans les cinq cas. Cela ne
suffit pas à confirmer l’exploitation : quatre résultats ne remplissent pas les
conditions décrites par leur avis, et le cinquième nécessite une analyse de
chemin d’appel supplémentaire.

## Résultat 1 — CVE-2020-26160

| Élément | Analyse |
| --- | --- |
| CVE | [CVE-2020-26160](https://www.cve.org/CVERecord?id=CVE-2020-26160) — [enregistrement JSON](https://github.com/CVEProject/cvelistV5/blob/main/cves/2020/26xxx/CVE-2020-26160.json) |
| Composant | `github.com/dgrijalva/jwt-go` |
| Version présente | `v3.2.0+incompatible`, détectée par Trivy et déclarée dans le [`go.mod`](https://github.com/filebrowser/filebrowser/blob/v2.15.0/go.mod) du tag `v2.15.0` |
| Sévérité / CVSS | Trivy : `HIGH` ; GitHub Advisory : CVSS 3.1 **7.5 HIGH**, `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Conditions pertinentes | Le contournement nécessite un jeton dont la revendication `aud` est un tableau et un appel à `MapClaims.VerifyAudience` avec `req=false`, sans contrôle d’audience propre au service |
| Vérification effectuée | Le fichier [`http/auth.go`](https://github.com/filebrowser/filebrowser/blob/v2.15.0/http/auth.go) utilise `jwt.StandardClaims`, crée ses propres jetons HS256 et ne renseigne pas `Audience`. La recherche dans le tag ne trouve ni `MapClaims`, ni `VerifyAudience` |
| Applicabilité | **Non pertinente dans File Browser 2.15.0 observé** |
| Correction disponible | Pour l’ancien chemin de module, la base Go indique « aucune correction connue ». L’avis recommande de migrer vers `github.com/golang-jwt/jwt` à partir de `v3.2.1`, ce qui impose une modification puis une reconstruction de l’application |
| Risque dans le contexte du serveur | Faible pour cette CVE précise, même si la dépendance d’authentification abandonnée reste un signal fort d’obsolescence |
| Justification | File Browser utilise bien des JWT, mais pas la fonction ni la revendication nécessaires à ce contournement particulier |

Références consultées : [base de vulnérabilités Go](https://pkg.go.dev/vuln/GO-2020-0017),
[GitHub Advisory](https://github.com/advisories/GHSA-w73w-5m7g-f7qc) et code
source du tag `v2.15.0`.

## Résultat 2 — CVE-2021-44716

| Élément | Analyse |
| --- | --- |
| CVE | [CVE-2021-44716](https://www.cve.org/CVERecord?id=CVE-2021-44716) — [enregistrement JSON](https://github.com/CVEProject/cvelistV5/blob/main/cves/2021/44xxx/CVE-2021-44716.json) |
| Composant | Bibliothèque standard Go, paquet `net/http` |
| Version présente | `stdlib v1.16.2`, détectée dans le binaire par Trivy |
| Sévérité / CVSS | Trivy : `HIGH` ; NVD : CVSS 3.1 **7.5 HIGH**, `AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Conditions pertinentes | Un attaquant doit envoyer des requêtes **HTTP/2** afin de provoquer une croissance mémoire non bornée dans le cache de canonicalisation des en-têtes |
| Vérification effectuée | Le code [`cmd/root.go`](https://github.com/filebrowser/filebrowser/blob/v2.15.0/cmd/root.go) utilise `http.Serve` et ne configure ni `h2c`, ni un serveur HTTP/2 explicite. `curl` obtient `HTTP/1.1 200` sur le port 8080. Le test `--http2-prior-knowledge` échoue avant toute réponse HTTP avec le code curl `16` |
| Applicabilité | **Non pertinente dans la configuration observée** |
| Correction disponible | Reconstruire avec Go `1.16.12` au minimum, ou une branche Go maintenue plus récente |
| Risque dans le contexte du serveur | Faible pour le service actuel en HTTP/1.1 ; à réévaluer si HTTP/2 est activé par File Browser ou par un chemin réseau qui lui transmet réellement des flux HTTP/2 |
| Justification | La version Go est affectée et le service est exposé, mais le protocole indispensable à l’exploitation n’est pas accepté sur le point d’entrée testé |

Référence principale : [avis Go GO-2022-0288](https://pkg.go.dev/vuln/GO-2022-0288).

## Résultat 3 — CVE-2022-23806

| Élément | Analyse |
| --- | --- |
| CVE | [CVE-2022-23806](https://www.cve.org/CVERecord?id=CVE-2022-23806) — [enregistrement JSON](https://github.com/CVEProject/cvelistV5/blob/main/cves/2022/23xxx/CVE-2022-23806.json) |
| Composant | Bibliothèque standard Go, paquet `crypto/elliptic` |
| Version présente | `stdlib v1.16.2`, alors que l’avis affecte les versions antérieures à `1.16.14` |
| Sévérité / CVSS | Trivy : `CRITICAL` ; NVD : CVSS 3.1 **9.1 CRITICAL**, `AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Conditions pertinentes | Une valeur `big.Int` négative ou débordant le champ doit parvenir à `CurveParams.IsOnCurve`. La fonction peut alors accepter une valeur invalide, puis provoquer une opération de courbe incorrecte ou un panic. L’avis précise que `Unmarshal` ne produit pas de telles valeurs |
| Vérification effectuée | Trivy identifie la bibliothèque standard Go 1.16.2. L’examen des chaînes du binaire statique retrouve `crypto/elliptic.(*CurveParams).IsOnCurve`. Aucune entrée applicative conduisant une valeur contrôlée par un partenaire vers ce symbole n’a été démontrée |
| Applicabilité | **À vérifier** |
| Correction disponible | Go `1.16.14` ou `1.17.7` selon la branche ; en pratique, reconstruire File Browser avec une version Go maintenue |
| Risque dans le contexte du serveur | Potentiellement important si une fonctionnalité cryptographique transforme une entrée distante en coordonnées de courbe non validées ; non démontré avec les éléments actuels |
| Justification | La version et le symbole vulnérables sont présents, mais une analyse de symboles ne prouve pas qu’un appel attaquable existe. `govulncheck -mode=binary` n’a pas pu être exécuté car la commande `go` n’est pas installée sur la machine d’audit |

Référence principale : [avis Go GO-2021-0319](https://pkg.go.dev/vuln/GO-2021-0319).

## Résultat 4 — CVE-2021-3711

| Élément | Analyse |
| --- | --- |
| CVE | [CVE-2021-3711](https://www.cve.org/CVERecord?id=CVE-2021-3711) — [enregistrement JSON](https://github.com/CVEProject/cvelistV5/blob/main/cves/2021/3xxx/CVE-2021-3711.json) |
| Composant | `libcrypto1.1` et `libssl1.1` |
| Version présente | `1.1.1k-r0`, détectée dans les paquets Alpine de l’image |
| Sévérité / CVSS | Trivy : `CRITICAL` ; NVD : CVSS 3.1 **9.8 CRITICAL**, `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Conditions pertinentes | L’application doit appeler deux fois `EVP_PKEY_decrypt` pour déchiffrer un contenu chiffré **SM2** contrôlé par l’attaquant. Le calcul de taille incorrect peut alors provoquer un dépassement de tampon |
| Vérification effectuée | L’examen ELF montre que `/filebrowser` est un binaire Go **statiquement lié** et ne déclare aucune dépendance dynamique vers `libssl` ou `libcrypto`. Le conteneur sert actuellement File Browser en HTTP sur le port 80 et aucune fonction de déchiffrement SM2 n’a été trouvée dans le code du tag |
| Applicabilité | **Non pertinente pour le processus exposé observé** |
| Correction disponible | OpenSSL `1.1.1l` ; Trivy indique les paquets Alpine `1.1.1l-r0` |
| Risque dans le contexte du serveur | Faible pour File Browser. Le paquet vulnérable reste néanmoins présent dans l’image et devrait disparaître avec le remplacement de cette image hors support |
| Justification | La seule présence du paquet ne fournit pas le chemin d’exécution très spécifique requis par l’avis OpenSSL |

Référence principale : [avis de sécurité OpenSSL du 24 août 2021](https://mta.openssl.org/pipermail/openssl-announce/2021-August/000207.html).

## Résultat 5 — CVE-2022-37434

| Élément | Analyse |
| --- | --- |
| CVE | [CVE-2022-37434](https://www.cve.org/CVERecord?id=CVE-2022-37434) — [enregistrement JSON](https://github.com/CVEProject/cvelistV5/blob/main/cves/2022/37xxx/CVE-2022-37434.json) |
| Composant | `zlib` |
| Version présente | Paquet Alpine `1.2.11-r3`, affecté par l’avis visant les versions jusqu’à `1.2.12` |
| Sévérité / CVSS | Trivy : `CRITICAL` ; NVD : CVSS 3.1 **9.8 CRITICAL**, `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Conditions pertinentes | L’application doit appeler `inflateGetHeader` et traiter un en-tête gzip contenant un champ supplémentaire de grande taille |
| Vérification effectuée | `/filebrowser` est statiquement lié et ne charge pas la `libz.so.1.2.11` présente dans l’image. Le code [`http/raw.go`](https://github.com/filebrowser/filebrowser/blob/v2.15.0/http/raw.go) utilise `mholt/archiver` pour **créer** des archives lors d’un téléchargement de répertoire ; aucun appel à la zlib C ou à `inflateGetHeader` n’est présent dans le code serveur |
| Applicabilité | **Non pertinente pour le processus exposé observé** |
| Correction disponible | Trivy indique le paquet Alpine `1.2.12-r2`. Le projet zlib indique que la version amont `1.2.13` corrige CVE-2022-37434 |
| Risque dans le contexte du serveur | Faible pour le processus File Browser. À réévaluer si un autre programme du conteneur utilisant la zlib C devient exécutable depuis le service ou une tâche d’administration |
| Justification | La version affectée est présente dans l’image, mais le processus exposé ne lie pas cette bibliothèque et la fonction vulnérable n’est pas appelée par le code serveur étudié |

Référence principale : [notes de version zlib 1.2.13](https://github.com/madler/zlib/releases/tag/v1.2.13).

## Conclusion de l’analyse

Le scanner a correctement signalé des composants dont les versions sont
associées à des vulnérabilités connues. L’examen du protocole, du code et du
binaire ne confirme toutefois aucune des cinq vulnérabilités comme exploitable
dans la configuration actuelle : quatre sont classées non pertinentes et une
reste à vérifier.

Cette conclusion ne rend pas l’image acceptable. Alpine 3.13.4 est hors support,
File Browser 2.15.0 et sa chaîne Go sont anciens, et le rapport contient de
nombreux autres résultats. La mesure structurelle à étudier est le remplacement
de l’image par une version maintenue, suivi d’un nouveau scan et de tests de
non-régression. La présente activité qualifie les constats ; elle ne constitue
pas encore le plan de remédiation définitif.

## Limites

- L’analyse statique du binaire confirme des symboles et l’absence de liaisons
  dynamiques ; elle ne reconstitue pas à elle seule tous les chemins d’appel.
- Le test HTTP décrit l’exposition directe sur le port 8080 au moment du
  contrôle ; un futur mandataire inverse pourrait modifier le protocole visible.
- L’absence d’un appel dans le code du tag ne couvre pas une modification locale
  de l’image, mais l’ImageID analysé correspond à l’image historique exportée.
- Les scores CVSS mesurent une sévérité générique et non le risque propre à ce
  serveur.

- [Activité précédente — Analyser l’image avec Trivy](analyser-image-trivy.md)
- [Activité suivante — Consolider les trois sources d’audit](consolider-trois-sources-audit.md)
- [Retour à l’itération 3](index.md)
- [Dossier de preuves](../dossier-preuves.md)
