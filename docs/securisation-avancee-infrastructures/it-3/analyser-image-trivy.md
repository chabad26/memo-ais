# Analyser l’image avec Trivy

**Durée indicative : 1 h**

## Objectif

Utiliser Trivy sur la machine d’audit pour identifier les composants, leurs
versions et les vulnérabilités connues présentes dans l’image File Browser du
cas fil rouge.

**Statut : scan et inventaire réalisés ; vulnérabilités à qualifier.** Trivy est
installé sur la machine d’audit, l’image exacte a été exportée puis transférée
avec une empreinte identique. Le scan a produit un rapport JSON avec un code
retour nul. Les catégories et composants sont inventoriés ; les vulnérabilités
du rapport restent à extraire et à qualifier.

## Périmètre

| Machine | Rôle dans cette activité |
| --- | --- |
| VM Ubuntu 20.04 cible | Héberge l’image réellement utilisée ; produit une archive avec `docker image save` |
| Machine d’audit Ubuntu 26.04 | Installe Trivy, reçoit l’archive et réalise l’analyse |
| Conteneur File Browser | Aucun Trivy installé ou exécuté à l’intérieur |

L’objet à analyser est l’ImageID déjà rattaché au conteneur :

```text
sha256:a68f43720ea6ff331fa4b92becced20af14b72f4c3a22ca1f764076a8e42e1a5
```

Le tag `filebrowser/filebrowser:v2.15.0` et le RepoDigest sont conservés comme
références, mais le scan ne doit pas dépendre d’un nouveau téléchargement du
tag. Un tag peut désigner un autre objet après sa publication initiale.

## Étape 1 — Installer Trivy sur la machine d’audit

Suivre le dépôt DEB indiqué par la documentation officielle :

```bash
sudo apt-get install wget gnupg
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key \
  | gpg --dearmor \
  | sudo tee /usr/share/keyrings/trivy.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb generic main" \
  | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy
```

Ces commandes modifient les sources APT de la machine d’audit. Conserver la date,
la source ajoutée et la version effectivement installée :

```bash
date -Is
hostname
trivy --version
dpkg-query -W -f='${binary:Package}\t${Version}\t${db:Status-Abbrev}\n' trivy
```

Ne pas recopier dans la feuille un numéro de version attendu : seule la sortie
obtenue le jour du scan constitue la preuve.

### Résultat observé le 1er octobre 2026

| Élément vérifié | Résultat |
| --- | --- |
| Horodatage | `2026-10-01T13:15:32+02:00` |
| Machine | `ubuntu-oliv` |
| Version annoncée par Trivy | `0.74.0` |
| Paquet DEB | `trivy` version `0.74.0`, état `ii` |

**Conclusion :** Trivy 0.74.0 est installé et exécutable sur la machine d’audit.
Cette vérification atteste l’outil disponible ; elle ne constitue pas encore une
preuve d’analyse de l’image ni de mise à jour réussie de sa base de
vulnérabilités.

## Étape 2 — Exporter l’image exacte depuis la VM cible

Dans la **VM Ubuntu 20.04 cible** :

```bash
date -Is
hostname
FB_IMAGE_ID=$(sudo docker inspect --type container filebrowser \
  --format '{{.Image}}')
echo "$FB_IMAGE_ID"

sudo docker image inspect "$FB_IMAGE_ID" --format \
  'ImageID={{.Id}} RepoTags={{json .RepoTags}} RepoDigests={{json .RepoDigests}} OS={{.Os}} Architecture={{.Architecture}}'

TRIVY_EXPORT_DIR="$HOME/preuves-trivy"
install -d -m 700 "$TRIVY_EXPORT_DIR"
sudo docker image save "$FB_IMAGE_ID" \
  -o "$TRIVY_EXPORT_DIR/filebrowser-v2.15.0-image.tar"
sudo chown "$USER:$(id -gn)" \
  "$TRIVY_EXPORT_DIR/filebrowser-v2.15.0-image.tar"
chmod 600 "$TRIVY_EXPORT_DIR/filebrowser-v2.15.0-image.tar"
sha256sum "$TRIVY_EXPORT_DIR/filebrowser-v2.15.0-image.tar"
```

Comparer l’ImageID affiché à la valeur connue. Si l’objet référencé a changé,
arrêter et expliquer l’écart avant le scan. `docker image save` exporte l’image ;
il n’installe rien dans le conteneur et ne nécessite pas de le démarrer.

### Résultat observé le 1er octobre 2026

| Élément vérifié | Résultat |
| --- | --- |
| Horodatage | `2026-10-01T13:16:33+02:00` |
| VM cible | `oliv-Standard-PC-Q35-ICH9-2009` |
| ImageID du conteneur | `sha256:a68f43720ea6ff331fa4b92becced20af14b72f4c3a22ca1f764076a8e42e1a5` |
| Tag | `filebrowser/filebrowser:v2.15.0` |
| RepoDigest | `filebrowser/filebrowser@sha256:1595cf9b36528113a18178996d9ff9ee8bc7814699bb5f8e1d8ad8ec48aa89ac` |
| Plateforme | `linux/amd64` |
| Archive créée | `/home/oliv/preuves-trivy/filebrowser-v2.15.0-image.tar` |
| SHA-256 de l’archive | `172f240628118923c202ec30648f2d8e4fe1fccec3b94d613a010c424dc6a20c` |

**Conclusion :** l’ImageID observé est identique à celui déjà associé au
conteneur File Browser. L’archive a été produite à partir de cet identifiant
précis et son empreinte fournit la valeur de référence à comparer après le
transfert vers la machine d’audit.

## Étape 3 — Transférer l’archive vers la machine d’audit

Depuis la **machine d’audit**, adapter l’adresse uniquement si celle de la VM a
changé :

```bash
TRIVY_WORK_DIR="$HOME/Documents/entreprise/AIS/Modules/preuves-trivy-filebrowser"
install -d -m 700 "$TRIVY_WORK_DIR"

scp oliv@192.168.122.229:/home/oliv/preuves-trivy/filebrowser-v2.15.0-image.tar \
  "$TRIVY_WORK_DIR/"
chmod 600 "$TRIVY_WORK_DIR/filebrowser-v2.15.0-image.tar"
sha256sum "$TRIVY_WORK_DIR/filebrowser-v2.15.0-image.tar"
```

L’empreinte calculée sur la machine d’audit doit être identique à celle obtenue
sur la VM. Cette égalité contrôle le transfert ; elle ne prouve pas à elle seule
la provenance éditoriale de l’image.

### Résultat observé le 1er octobre 2026

Le transfert SCP de l’archive de 41 Mo a abouti. L’empreinte obtenue sur la
machine d’audit est :

```text
172f240628118923c202ec30648f2d8e4fe1fccec3b94d613a010c424dc6a20c
```

Elle est identique à l’empreinte calculée sur la VM cible : l’intégrité du
fichier pendant ce transfert est confirmée.

SSH a également affiché un avertissement indiquant que la connexion n’utilisait
pas d’algorithme d’échange de clés post-quantique. Cet avertissement n’a pas
empêché le transfert et ne remet pas en cause l’égalité des empreintes. Il
signale une propriété cryptographique de la session SSH à examiner séparément,
notamment par la vérification des versions et algorithmes pris en charge par le
client et le serveur.

## Étape 4 — Produire un rapport complet

Le premier scan conserve toutes les sévérités et la liste des paquets. Il ne
filtre pas les résultats `LOW`, `MEDIUM` ou `UNKNOWN` :

```bash
TRIVY_WORK_DIR="$HOME/Documents/entreprise/AIS/Modules/preuves-trivy-filebrowser"
IMAGE_ARCHIVE="$TRIVY_WORK_DIR/filebrowser-v2.15.0-image.tar"
REPORT_JSON="$TRIVY_WORK_DIR/trivy-filebrowser-v2.15.0.json"

date -Is
trivy image \
  --input "$IMAGE_ARCHIVE" \
  --scanners vuln \
  --list-all-pkgs \
  --format json \
  --output "$REPORT_JSON"
TRIVY_EXIT=$?
echo "Code retour Trivy=$TRIVY_EXIT"
sha256sum "$REPORT_JSON"
```

Conserver le code de retour, les messages de téléchargement ou de mise à jour de
la base, les avertissements sur la fin de support d’Alpine et les éventuelles
erreurs. Un rapport créé avec une analyse partielle doit rester marqué comme tel.

Générer ensuite une vue lisible depuis le rapport JSON, sans relancer le scan :

```bash
trivy convert \
  --format table \
  --output "$TRIVY_WORK_DIR/trivy-filebrowser-v2.15.0.txt" \
  "$REPORT_JSON"
sha256sum "$TRIVY_WORK_DIR/trivy-filebrowser-v2.15.0.txt"
```

Le format JSON conserve davantage de métadonnées et permet de produire d’autres
vues. Le tableau facilite la lecture mais ne remplace pas le rapport source.

### Résultat observé le 1er octobre 2026

Le scan a commencé à `2026-10-01T13:18:22+02:00`. Trivy a téléchargé sa base de
vulnérabilités, activé l’analyse des vulnérabilités puis terminé avec le code
retour `0`.

| Observation Trivy | Résultat |
| --- | --- |
| Système détecté | Alpine Linux `3.13.4` |
| Paquets du système examinés | 20 |
| Fichiers propres à un langage | 1 |
| Analyse de langage annoncée | binaire Go (`gobinary`) |
| État de support de l’OS | Fin de support signalée par Trivy |
| Code retour | `0` |
| Rapport JSON | `/home/oliv/preuves-trivy-filebrowser/trivy-filebrowser-v2.15.0.json` |
| SHA-256 du rapport JSON | `61352a7122908c0c782901f0b0184658a20e1e2a3c7aaa6b307d786f83c1fb70` |
| Rapport texte | `/home/oliv/preuves-trivy-filebrowser/trivy-filebrowser-v2.15.0.txt` |
| SHA-256 du rapport texte | `f1e8a85bf615d8fe07111735a302fb1314beeb951823195f066011054599e872` |

Trivy avertit qu’il utilise, pour certaines vulnérabilités, les sévérités
attribuées par d’autres fournisseurs. La sévérité doit donc être accompagnée de
sa source lors de la qualification. Il avertit aussi qu’Alpine 3.13.4 n’est plus
pris en charge par la distribution et que la détection peut être insuffisante,
car cette version ne reçoit plus de mises à jour de sécurité.

La conversion en texte a produit un fichier, mais avec l’avertissement
`No enabled scanners found. Summary table will not be displayed.` Cette sortie
ne doit pas être utilisée seule pour conclure sur le contenu du scan. Le rapport
JSON, produit directement par `trivy image` et associé à un code retour nul,
reste la source à exploiter pour les composants et vulnérabilités.

Après le scan, le dossier de preuves a été déplacé vers :

```text
/home/oliv/Documents/entreprise/AIS/Modules/preuves-trivy-filebrowser
```

Les empreintes du rapport JSON et de l’archive sont restées respectivement
`61352a…fb70` et `172f24…20c` après le déplacement. Le champ `ArtifactName` du
rapport conserve légitimement l’ancien chemin, puisqu’il décrit le chemin au
moment du scan.

## Étape 5 — Vérifier l’objet réellement analysé

Si `jq` est déjà installé sur la machine d’audit :

```bash
jq '{ArtifactName, ArtifactType, Metadata: {ImageID: .Metadata.ImageID, RepoTags: .Metadata.RepoTags, RepoDigests: .Metadata.RepoDigests, OS: .Metadata.OS}}' \
  "$REPORT_JSON"
```

Comparer l’ImageID et les digests du rapport aux valeurs relevées avant
l’export. Si Trivy ne renseigne pas un champ, le laisser « non fourni » au lieu
de le déduire du nom de l’archive.

### Métadonnées observées dans le rapport

| Champ | Valeur |
| --- | --- |
| `ArtifactName` | `/home/oliv/preuves-trivy-filebrowser/filebrowser-v2.15.0-image.tar` |
| `ArtifactType` | `container_image` |
| `Metadata.ImageID` | `sha256:a68f43720ea6ff331fa4b92becced20af14b72f4c3a22ca1f764076a8e42e1a5` |
| `Metadata.RepoTags` | Non fourni (`null`) |
| `Metadata.RepoDigests` | Non fourni (`null`) |
| Système | Alpine Linux `3.13.4` |
| Fin de support | `EOSL: true` |

L’ImageID du rapport correspond à celui relevé sur la VM avant l’export. Trivy
n’a pas conservé le tag et le RepoDigest dans les métadonnées de cette analyse
d’archive ; ces valeurs restent donc rattachées à la preuve `docker inspect`,
pas déduites du rapport Trivy.

## Étape 6 — Identifier les catégories de composants

Trivy peut produire plusieurs cibles dans `Results`, par exemple des paquets du
système d’exploitation et des dépendances propres à un langage. Relever ce qui
est réellement présent :

```bash
jq -r '.Results[] | [.Target, .Class, .Type] | @tsv' \
  "$REPORT_JSON"

jq -r '
  [.Results[]
   | . as $result
   | ($result.Packages // [])[]
   | [$result.Target, $result.Class, $result.Type, .Name, .Version]]
  | .[] | @tsv' "$REPORT_JSON"
```

| Cible Trivy | Classe | Type | Nombre de composants | Conclusion |
| --- | --- | --- | ---: | --- |
| Archive de l’image `(alpine 3.13.4)` | `os-pkgs` | `alpine` | 20 | Paquets du système de base de l’image |
| `filebrowser` | `lang-pkgs` | `gobinary` | 53 | Module principal, bibliothèque standard Go et dépendances incorporées au binaire |

Deux catégories sont donc effectivement couvertes par ce scan. Le nombre
`53` correspond aux lignes de composants Go produites par l’extraction, tandis
que les 20 paquets Alpine correspondent à la cible `os-pkgs` annoncée par Trivy.

### Paquets Alpine observés

| Paquet | Version | Paquet | Version |
| --- | --- | --- | --- |
| `alpine-baselayout` | `3.2.0-r8` | `alpine-keys` | `2.2-r0` |
| `apk-tools` | `2.12.4-r0` | `brotli-libs` | `1.0.9-r3` |
| `busybox` | `1.32.1-r5` | `ca-certificates` | `20191127-r5` |
| `ca-certificates-bundle` | `20191127-r5` | `curl` | `7.74.0-r1` |
| `libc-utils` | `0.7.2-r3` | `libcrypto1.1` | `1.1.1k-r0` |
| `libcurl` | `7.74.0-r1` | `libssl1.1` | `1.1.1k-r0` |
| `libtls-standalone` | `2.9.1-r1` | `mailcap` | `2.1.49-r0` |
| `musl` | `1.2.2-r0` | `musl-utils` | `1.2.2-r0` |
| `nghttp2-libs` | `1.42.0-r1` | `scanelf` | `1.2.8-r0` |
| `ssl_client` | `1.32.1-r5` | `zlib` | `1.2.11-r3` |

Dans la sortie copiée, le nom et la version de `libcrypto1.1` et de
`nghttp2-libs` apparaissent concaténés. Ils sont présentés séparément ci-dessus
selon les champs demandés par la commande `jq` ; le JSON reste la référence à
consulter en cas de doute.

### Exemples de composants Go observés

| Composant | Version relevée |
| --- | --- |
| `github.com/filebrowser/filebrowser/v2` | Non fournie dans cette extraction |
| `stdlib` | `v1.16.2` |
| `github.com/caddyserver/caddy` | `v1.0.3` |
| `github.com/dgrijalva/jwt-go` | `v3.2.0+incompatible` |
| `github.com/gorilla/mux` | `v1.7.3` |
| `github.com/gorilla/websocket` | `v1.4.1` |
| `github.com/mholt/archiver` | `v3.1.1+incompatible` |
| `go.etcd.io/bbolt` | `v1.3.3` |
| `golang.org/x/crypto` | `v0.0.0-20200510223506-06a226fb4e37` |
| `golang.org/x/net` | `v0.0.0-20200528225125-3c3fba18258b` |
| `gopkg.in/square/go-jose.v2` | `v2.2.2` |
| `gopkg.in/yaml.v2` | `v2.3.0` |

Ces lignes prouvent que Trivy ne s’est pas limité aux paquets Alpine : il a
aussi lu les informations de construction du binaire Go. La liste complète des
53 composants reste conservée dans le rapport JSON et dans la sortie de la
commande. Leur présence ne prouve pas encore qu’une CVE est applicable ni que
toutes les fonctions correspondantes sont atteignables depuis l’application.

Une catégorie absente du rapport peut signifier qu’aucun fichier reconnu n’a été
trouvé. Elle ne démontre pas que l’image ne contient aucun composant de cette
catégorie.

## Étape 7 — Examiner toutes les vulnérabilités

Compter les résultats sans supprimer les vulnérabilités sans correctif :

```bash
jq -r '
  [.Results[] | (.Vulnerabilities // [])[] | .Severity]
  | group_by(.)
  | map({severity: .[0], count: length})' "$REPORT_JSON"

jq -r '
  .Results[]
  | . as $result
  | ($result.Vulnerabilities // [])[]
  | [$result.Target, .PkgName, .InstalledVersion,
     .VulnerabilityID, .Severity, (.FixedVersion // ""),
     (.Status // ""), (.PrimaryURL // "")]
  | @tsv' "$REPORT_JSON"
```

Documenter les colonnes suivantes pour les résultats étudiés :

| Élément | Valeur attendue |
| --- | --- |
| Cible et catégorie | Paquet OS, bibliothèque ou autre cible Trivy |
| Composant | Nom réellement détecté |
| Version installée | Version complète relevée par Trivy |
| Vulnérabilité | Identifiant CVE ou avis associé |
| Sévérité | Valeur et source de sévérité lorsqu’elle est disponible |
| Version corrigée | Valeur Trivy, vide si aucun correctif n’est indiqué |
| Référence | Avis Alpine, CVE.org, éditeur ou source indiquée |
| Applicabilité | Fonction présente, configuration, exposition et conditions d’exploitation |
| Statut | Confirmé / À vérifier / Non pertinent |

### Résultat de l’extraction

Le fichier texte produit par la commande contient 294 associations entre un
composant et une vulnérabilité. Elles correspondent à 244 identifiants distincts :
une même CVE peut apparaître pour plusieurs paquets, notamment `curl` et
`libcurl`, sans constituer deux CVE différentes.

| Sévérité Trivy | Nombre d’associations |
| --- | ---: |
| `CRITICAL` | 13 |
| `HIGH` | 143 |
| `MEDIUM` | 121 |
| `LOW` | 14 |
| `UNKNOWN` | 3 |
| **Total** | **294** |

| Cible | Critique | Élevée | Moyenne | Faible | Inconnue | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Paquets Alpine | 8 | 40 | 26 | 8 | 0 | 82 |
| Binaire File Browser et composants Go | 5 | 103 | 95 | 6 | 3 | 212 |

Trivy indique l’état `fixed` et une version corrigée pour 283 associations. Pour
11 associations, l’état est `affected` et le champ `FixedVersion` est vide. Une
version corrigée renseignée prouve qu’une correction est connue dans la source
de Trivy ; elle ne prouve pas qu’une mise à jour isolée du paquet est une méthode
de remédiation durable dans cette image Alpine hors support.

La sortie complète est conservée dans le dossier privé :

```text
/home/oliv/Documents/entreprise/AIS/Modules/lab-securisation-avancee/greenbone/rapport_vulnerabilites.txt
```

Son empreinte SHA-256 après déplacement est
`d0a47acec71775adda7d36cce95eb94a56fbd48e0f0d1f33442f05aaadb323c8`.

### Fichiers filtrés `HIGH` et `CRITICAL`

À la demande de la formatrice, trois fichiers supplémentaires ont été générés
depuis le rapport JSON. Ils conservent la cible, le composant, la version
installée, l’identifiant, la sévérité, la version corrigée, le statut et la
référence Trivy.

| Fichier | Filtre | Résultats | SHA-256 |
| --- | --- | ---: | --- |
| `rapport_vulnerabilites_critical.txt` | `CRITICAL` | 13 | `0553ed973b5e760d1f93416d69f3d93dc95ec5705b3cbd033e093fa9b9e931f4` |
| `rapport_vulnerabilites_high.txt` | `HIGH` | 143 | `4871b77db6d105135f8830897577c7ee6f4596007f97cc6909abf134e8f77bf1` |
| `rapport_vulnerabilites_high_critical.txt` | `HIGH` ou `CRITICAL` | 156 | `2a0dbaeafe3593fc76390d9c881d02de0bf499ae370c8f6298d0b6133c896578` |

Ils sont conservés dans :

```text
/home/oliv/Documents/entreprise/AIS/Modules/lab-securisation-avancee/greenbone
```

Un contrôle automatique a confirmé que le premier fichier ne contient que la
sévérité `CRITICAL`, le deuxième uniquement `HIGH`, et le troisième uniquement
ces deux sévérités. Ces exports facilitent la revue, mais le rapport complet
reste nécessaire pour ne pas écarter un résultat moins sévère mais plus
applicable au serveur.

## Étape 8 — Sélectionner les résultats à qualifier

Ne pas classer uniquement par sévérité. Commencer par examiner l’ensemble des
résultats, puis retenir des cas significatifs selon :

- la présence et la version réellement détectées ;
- l’utilisation du composant par File Browser ;
- la possibilité pour un partenaire ou un attaquant de contrôler l’entrée ;
- les privilèges du processus et l’accès au montage `/srv` ;
- l’existence d’un correctif et la possibilité de reconstruire ou remplacer
  l’image ;
- les protections Docker et réseau déjà présentes ;
- les conséquences sur la confidentialité, l’intégrité et la disponibilité des
  documents.

| Rang | Composant / version | CVE | Sévérité Trivy | Correctif indiqué | Applicabilité | Priorité motivée |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `github.com/dgrijalva/jwt-go` `v3.2.0+incompatible` | CVE-2020-26160 | `HIGH` | Non indiqué ; état `affected` | **À vérifier** : déterminer si File Browser utilise cette bibliothèque pour valider les jetons d’authentification et si la condition de la CVE est atteignable | Composant lié à l’authentification dans un service Internet ; l’absence de correctif indiqué impose d’examiner le remplacement de la dépendance ou de l’image |
| 2 | Bibliothèque standard Go `v1.16.2` | CVE-2022-23806 | `CRITICAL` | Go `1.16.14` ou `1.17.7` | **À vérifier** : identifier la fonction concernée et confirmer son usage dans le binaire | Le composant est intégré au binaire exposé ; une correction suppose normalement une reconstruction avec une version Go corrigée |
| 3 | `libcrypto1.1` et `libssl1.1` `1.1.1k-r0` | CVE-2021-3711 | `CRITICAL` | `1.1.1l-r0` | **À vérifier** : confirmer l’usage de ces bibliothèques par un chemin traitant des données contrôlables | Bibliothèques cryptographiques anciennes présentes dans une image hors support ; la même CVE apparaît sur deux paquets liés |
| 4 | `curl` et `libcurl` `7.74.0-r1` | CVE-2021-22945 | `CRITICAL` | `7.79.0-r0` | **À vérifier** : déterminer si le binaire ou ses scripts appellent ces composants avec une entrée contrôlable | Résultat critique présent sur deux paquets, mais leur simple présence ne démontre pas leur utilisation par le service web |
| 5 | `zlib` `1.2.11-r3` | CVE-2022-37434 | `CRITICAL` | `1.2.12-r2` | **À vérifier** : rechercher les traitements de données compressées et la bibliothèque réellement chargée | Le service échange des fichiers, ce qui rend le traitement d’archives plausible sans le prouver ; le correctif est identifié par Trivy |

Ce classement est provisoire. Le résultat `jwt-go` est placé en premier malgré
une sévérité inférieure aux quatre autres, car une bibliothèque de validation de
jetons peut concerner directement le contrôle d’accès de File Browser. Cette
hypothèse doit être confirmée dans la documentation de la CVE, le code ou la
configuration de l’application. Les quatre résultats critiques restent à
vérifier pour éviter de prioriser des composants présents mais non utilisés.

Un résultat `CRITICAL` non atteignable peut être moins urgent qu’un résultat
`MEDIUM` directement exploitable depuis le service exposé. L’absence de
`FixedVersion` signifie seulement que Trivy n’indique pas de correction dans sa
source au moment du scan ; elle ne signifie ni « faux positif » ni « impossible
à traiter ».

## Limites à conserver

- Trivy rapproche des composants reconnus d’une base datée ; il ne détecte pas
  toutes les vulnérabilités inconnues ou tous les binaires compilés manuellement.
- Alpine 3.13.4 est ancien : un avertissement de fin de support peut limiter la
  qualité des données de correction disponibles.
- Le scan de l’image ne couvre pas automatiquement la couche modifiable du
  conteneur ni les documents montés depuis `/srv/filebrowser`.
- Une CVE trouvée dans une bibliothèque ne prouve pas que le chemin vulnérable
  est utilisé par File Browser.
- Un rapport sans vulnérabilité ne prouve pas que l’image est sûre.

## Preuves attendues

- version de Trivy et paquet installé ;
- ImageID, RepoDigest, plateforme et empreinte de l’archive ;
- commande exacte et code de retour ;
- date ou messages de mise à jour de la base ;
- rapports JSON et texte avec empreintes SHA-256 ;
- catégories de composants détectées ;
- vulnérabilités retenues avec version installée, correctif et applicabilité ;
- erreurs, avertissements et limites de couverture.

Les rapports complets peuvent contenir des chemins et métadonnées internes. Les
conserver dans le dossier privé et ne publier que les extraits nécessaires.

## Ressources

- [Installation officielle de Trivy](https://www.trivy.dev/docs/latest/getting-started/installation/)
- [Analyse d’une image de conteneur](https://trivy.dev/docs/latest/guide/target/container_image/)
- [Formats de rapport Trivy](https://trivy.dev/docs/latest/configuration/reporting/)
- [Dépôt Trivy](https://github.com/aquasecurity/trivy)

- [Activité précédente — Identifier ce qui manque dans l’audit](identifier-manques-audit.md)
- [Activité suivante — Analyser et vérifier les résultats Trivy](analyser-verifier-resultats-trivy.md)
- [Retour à l’itération 3](index.md)
- [Dossier de preuves](../dossier-preuves.md)
