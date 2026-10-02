# Mettre en œuvre et vérifier les remédiations

**Itération 4 — Travail individuel — Feuille préparée le 2 octobre 2026**

## 🎯 Objectif

Rechercher, mettre en œuvre et vérifier les remédiations prioritaires identifiées
lors de l’audit, en suivant la [préparation précédente](preparer-remediations.md).
Démontrer séparément la correction du défaut et le maintien du service.

**Bilan au 2 octobre 2026 : les lots retenus R01 à R09 ont été appliqués,
avec les limites de validation détaillées ci-dessous.** Ubuntu, SSH, Docker,
auditd, arrêt persistant de CUPS et deux lots sysctl disposent de preuves ;
File Browser fonctionne et reprend après redémarrage. Les CVE résiduelles et
la maintenance applicative ne sont pas toutes clôturées. Les interventions
ont été réalisées par Olivier sur le laboratoire ; l’assistant documente les
résultats reçus et n’a pas exécuté ces commandes sur la VM.

Les sections de collecte et les comptes rendus intermédiaires ci-dessous
conservent leur état historique. Le bilan suivant et le tableau de suivi
présentent l’avancement actuel ; une mention ancienne « à réaliser » ne décrit
pas nécessairement l’état final.

## Bilan actualisé — Captures et documents ajoutés le 2 octobre 2026

**R04, premier lot : appliqué et validé sur le service principal 8080.**
Olivier rattache les captures ci-dessous aux essais après réactivation du
conteneur durci. Elles complètent les contrôles de sécurité et de reprise
précédents. Les captures de navigateur sont recadrées sans barre d’adresse :
l’attribution à 8080 repose sur son retour et la capture Docker sur ce port.
Les heures indiquées sont celles des noms de fichiers, pas un horodatage
visible de chaque opération.

| Preuve | Observation | Validation |
| --- | --- | --- |
| SSH, 11:53:20 | Connexion avec clés désactivées et méthode password imposée : Permission denied (publickey) | Authentification password refusée |
| SSH, 11:53:45 et 11:53:58 | Root interdit, password/interactif désactivés, clés permises, UMAC-64 absents | Configuration effective du premier lot R02 |
| SSH, 12:05:14 | Nouvelle connexion depuis l’hyperviseur ; sudo -v retourne 0 | Accès administrateur conservé |
| Docker, 12:42:19 | Processus filebrowser UID/GID 1000, CapEff/CapBnd nuls, NoNewPrivs 1, Seccomp 2 ; unless-stopped | Protections appliquées au processus applicatif et reprise configurée |
| Docker, 12:47:07 | no-new-privileges:true, CapDrop ALL ; healthy sur 8080 | Durcissement actif après réactivation |
| Navigateur, 12:48:42 | test2 présent, 38 octets ; téléchargement Terminé | Consultation et téléchargement réussis |
| Navigateur, 12:48:52 | AIS.pdf ajouté, 166,39 Kio, modification récente | Upload documenté dans le parcours déclaré sur 8080 |
| Navigateur, 12:49:01 | AIS.pdf absent ; dossiers et fichiers test/test2 conservés | Suppression corroborée par la séquence et le retour d’Olivier |

L’accès à l’interface authentifiée et les opérations autorisées confirment le
fonctionnement. La séquence ne montre pas la saisie du secret ni la fenêtre de
confirmation de suppression ; aucun de ces écrans n’est inventé.
La racine du conteneur reste modifiable ; aucune protection read-only ni
correction des dépendances vulnérables n’est attribuée à ce lot.

### Captures de validation SSH

![SSH : authentification par mot de passe refusée](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2011-53-20.png)

![SSH : configuration effective après durcissement](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2011-53-45.png)

![SSH : complément de capture de la configuration effective](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2011-53-58.png)

![SSH : connexion par clé depuis hyperviseur et sudo réussi](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2012-05-14.png)

### Captures Docker et essais sur le service principal

![Docker : processus File Browser non root, capacités retirées et NoNewPrivs actif](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2012-42-19.png)

![Docker : conteneur durci réactivé et healthy sur 8080](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2012-47-07.png)

![Essai sur 8080 : téléchargement de test2 terminé](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2012-48-42.png)

![Essai sur 8080 : AIS.pdf ajouté par upload](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2012-48-52.png)

![Essai sur 8080 : AIS.pdf absent après suppression](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2012-49-01.png)

### Documents de preuve ajoutés

| Document | Contenu vérifié / limite |
| --- | --- |
| [Lynis — journal après migration et premier lot SSH](../../assets/files/securisation-avancee-infrastructures/it-4/lynis.log) | Lynis 3.1.6, audit 11:56:54–11:57:47 ; 259 tests, indice 65 ; précède le durcissement Docker |
| [Greenbone — premier rapport](../../assets/files/securisation-avancee-infrastructures/it-4/report-70b9bf20-5779-44b1-b5d3-4c6cf73416da.xml) | Trois Low exportés avec QoD minimum 70, dont MAC faibles ; fenêtre 11:47–11:53 |
| [Greenbone — rapport avec Log et QoD minimum 0](../../assets/files/securisation-avancee-infrastructures/it-4/report-033adb79-59bf-4076-bfdb-3d372e86794a.xml) | Scan 12:11–12:17 : 204 résultats de sécurité et 44 Log ; Auth-SSH-Success pour gvm-audit ; précède le lot Docker |
| [Trivy — export texte 2.15.0](../../assets/files/securisation-avancee-infrastructures/it-4/trivy-filebrowser-v2.15.0.txt) | Deux cibles, 40 + 103 HIGH et 8 + 5 CRITICAL : 156 associations ; identité exacte et bases à rattacher aux preuves historiques |
| [Trivy — export texte 2.63.23](../../assets/files/securisation-avancee-infrastructures/it-4/trivy-filebrowser-v2.63.23.txt) | bin/filebrowser : 10 HIGH, 0 CRITICAL ; applicabilité et maintenance future à traiter |

Les exports JSON Trivy mentionnés dans l’historique ne sont pas présents dans
ce dossier it-4 : les textes ajoutés ne les remplacent pas pour l’identité et
la conservation du scan complet. Le rapport Greenbone conserve son adresse
127.0.0.1 malgré l’authentification réussie et la concordance OS/noyau ; cette
limite reste documentée. Ces documents bruts constituent des preuves de
laboratoire contenant des informations internes.

**Clôture du périmètre réalisé :** R05, R06 et les deux lots R07 sont validés
selon leurs preuves. Les restrictions SSH complémentaires et la racine Docker
read-only ne font pas partie des lots réalisés. La qualification complète des
alertes et le remplacement d’une application sans maintenance sont des suites
à planifier ; aucune absence globale de vulnérabilité n’est revendiquée.


### Inventaire complet des journaux et rapports

Les pièces ci-dessous sont conservées dans leur format source. Les analyses et
les limites de preuve figurent dans les sections correspondantes.

- [lynis-apres-remediations-20261002-132326.log](../../assets/files/securisation-avancee-infrastructures/it-4/lynis-apres-remediations-20261002-132326.log)
- [lynis.log](../../assets/files/securisation-avancee-infrastructures/it-4/lynis.log)
- [report-033adb79-59bf-4076-bfdb-3d372e86794a.xml](../../assets/files/securisation-avancee-infrastructures/it-4/report-033adb79-59bf-4076-bfdb-3d372e86794a.xml)
- [report-70b9bf20-5779-44b1-b5d3-4c6cf73416da.xml](../../assets/files/securisation-avancee-infrastructures/it-4/report-70b9bf20-5779-44b1-b5d3-4c6cf73416da.xml)
- [report-934f13f0-28fc-4f03-95e7-337d8f08a5db.xml](../../assets/files/securisation-avancee-infrastructures/it-4/report-934f13f0-28fc-4f03-95e7-337d8f08a5db.xml)
- [trivy-filebrowser-v2.15.0.txt](../../assets/files/securisation-avancee-infrastructures/it-4/trivy-filebrowser-v2.15.0.txt)
- [trivy-filebrowser-v2.63.23.txt](../../assets/files/securisation-avancee-infrastructures/it-4/trivy-filebrowser-v2.63.23.txt)

## Bilan de clôture — périmètre et risques résiduels

À la demande d’Olivier, terminer la séquence sans ajouter de nouveau lot de
configuration. La clôture concerne les interventions et leurs vérifications,
pas une certification de sécurité globale de la VM.

| Élément | Bilan / suite |
| --- | --- |
| Ubuntu et service | Migration et fonctionnement validés ; inventaire final conservé |
| SSH et Docker | Protections du périmètre retenu actives, accès par clé et opérations applicatives validés |
| Auditd, CUPS, sysctl | Persistance et fonctionnement contrôlés ; rotation manuelle auditd réussie |
| Greenbone | Quelques résultats contradictoires qualifiés ; sudo core24 corrigé par rétroportage Ubuntu. Les autres résultats et l’adresse exportée 127.0.0.1 restent à qualifier |
| Trivy | Dix HIGH résiduels dans l’export de la nouvelle image ; applicabilité non entièrement établie et JSON complet absent des pièces de cette feuille |
| Maintenance File Browser | Fin de maintenance annoncée par l’application : remplacement recommandé dans une suite distincte. Aucune acceptation formelle du risque n’est attribuée à Olivier |
| Mesures complémentaires | Transferts SSH, autres sysctl, racine Docker read-only, collecte distante et intégrité des fichiers : hors des lots réalisés, sans extension automatique du chantier |

**Dernières pièces utiles à la remise :** conserver les captures et exports
existants ; produire un dernier relevé de santé et un scan Greenbone après
les derniers lots si un bilan complet avant/après est attendu. Le rapport
Greenbone actuel précède le durcissement Docker, CUPS, auditd et sysctl : il
ne peut pas en constituer le rescan final. La comparaison doit conserver la
cible, le profil, les filtres et la date ; ne pas réduire la conclusion à un
compteur de vulnérabilités. Conserver les sauvegardes jusqu’à la clôture.

## Relevé final de santé — 2 octobre 2026, 13:36:51 +02:00

Sortie fournie par Olivier depuis la VM. Ce relevé clôture les contrôles de
santé des lots réalisés ; il ne constitue pas un nouveau scan de vulnérabilités.

| Contrôle | Résultat observé |
| --- | --- |
| systemctl --failed | Aucune unité en échec : 0 loaded units listed |
| sshd -t | Aucune erreur affichée ; code de sortie non relevé séparément |
| Audit noyau | enabled 1, daemon PID 627, lost 0, backlog 0, backlog_limit 8192 ; failure 1 est le mode de traitement des erreurs, pas un compteur d’échecs |
| CUPS service/socket/path | Trois unités masked et inactive |
| Port 631 | Aucune écoute affichée par ss |
| File Browser principal | Conteneur f9810c6225f6, healthy, actif depuis 16 minutes, port publié 8080 |
| Protections Docker | SecurityOpt no-new-privileges:true ; CapDrop ALL ; Restart unless-stopped |

**Clôture technique du périmètre réalisé :** état final conforme aux lots
retenus, sans nouvelle modification de configuration. Les tests applicatifs
et les contrôles de persistance précédents complètent ce relevé. Le dernier
rapport Greenbone disponible précède les derniers lots : le rescan final de 13:38–13:44 est conservé dans la section suivante, avec
ses résultats et limites de comparaison. Les risques Trivy et
la fin de maintenance File Browser restent consignés dans le bilan.


### Capture du relevé final

**Capture 13:37:07 — Contrôle final : audit sans perte, CUPS masqué sans écoute et File Browser healthy avec protections actives.**

![Contrôle final : audit sans perte, CUPS masqué sans écoute et File Browser healthy avec protections actives](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2013-37-07.png)

## Rescan Greenbone final — 13:38:59–13:44:33 +02:00

[Rapport XML final conservé](../../assets/files/securisation-avancee-infrastructures/it-4/report-934f13f0-28fc-4f03-95e7-337d8f08a5db.xml).
Scan du 2 octobre 2026, statut **Done**, après le relevé final de santé.
Même identifiant de tâche et même identifiant de cible que le rapport de
12:11–12:17 ; cible nommée `AIS-Ubuntu20-avec-auth`. Le nom historique ne
constitue pas une détection Ubuntu 20. Les détails hôte indiquent Ubuntu
26.04 LTS et **Auth-SSH-Success : port 22, utilisateur gvm-audit**.

| Résultats exportés | Rapport 12:11–12:17 | Rapport final 13:38–13:44 |
| --- | --- | --- |
| Critical | 10 | 10 |
| High | 73 | 73 |
| Medium | 113 | 113 |
| Low | 8 | 8 |
| Log | 44 | 44 |
| Total sécurité / total exporté | 204 / 248 | 204 / 248 |

Filtres conservés : `levels=chmlg`, `min_qod=0`, `apply_overrides=0`,
`rows=1000`. Le multiensemble des noms, sévérités et ports des résultats est
identique entre ces deux exports ; cela ne signifie pas que toutes les preuves
détaillées ou les versions des tests sont identiques. La majorité des résultats
de sécurité conserve une faible QoD : 191 à 30, six à 1, cinq à 50 et deux à 80.

**Limites :** tous les résultats portent encore l’adresse `127.0.0.1`.
L’authentification et la détection Ubuntu corroborent le contexte de la VM,
mais la cause de cette adresse reste inexpliquée. Les mêmes identifiants de
tâche/cible et filtres soutiennent la comparaison ; l’identité complète du
profil et des bases de tests n’est pas démontrée ici. Les descriptions détaillées
des résultats ne sont pas présentes dans cet export : conserver les inventaires
locaux et les qualifications précédentes comme pièces complémentaires.

**Conclusion finale :** rescan réalisé et pièce jointe reçue. Aucun recul du
compteur Greenbone n’est observé entre ces deux scans. Ce compteur ne prouve
ni l’échec des lots SSH/Docker/auditd/CUPS/sysctl, vérifiés séparément, ni
204 vulnérabilités applicables. Les résultats déjà qualifiés pour libcurl,
OpenSSH et sudo core24 restent à distinguer des alertes non qualifiées.
Le chantier de configuration est clôturé dans le périmètre retenu ; les
risques Trivy, la maintenance File Browser et la qualification exhaustive
des autres alertes demeurent des suites documentées, sans nouveau lot imposé.

## R01 — Migration Ubuntu et validations du 2 octobre 2026

### Parcours réalisé et agrandissement du disque

Le parcours **20.04.6 → 22.04.5 → 24.04.5 → 26.04.1 LTS** est documenté
par les sorties initiales et les captures des trois versions obtenues.
Les heures ci-dessous proviennent des lignes `date -Is` visibles, en **+02:00** ;
elles ne représentent pas les heures de début ou de fin exactes des migrations.

| Relevé | Système et noyau observés | Espace sur `/` | Validation observée |
| --- | --- | --- | --- |
| 10:47:17 | Ubuntu 22.04.5 LTS ; `6.8.0-138-generic` | 24 Go ; 3,9 Go disponibles ; 83 % utilisés | Aucune unité en échec ; paquets à jour ; Docker actif |
| 11:14:59 | Ubuntu 24.04.5 LTS ; `6.8.0-146-generic` | 39 Go ; 19 Go disponibles ; 51 % utilisés | Aucune unité en échec ; paquets à jour ; Docker actif ; File Browser initialement arrêté puis démarré, `health: starting` |
| 11:33:46 | Ubuntu 26.04.1 LTS ; `7.0.0-38-generic` | 39 Go ; 18 Go disponibles ; 52 % utilisés | Aucune unité en échec ; paquets à jour ; Docker actif et activé ; File Browser `Up 49 seconds (healthy)` après redémarrage |

**Contrainte rencontrée :** espace limité après la première migration. Le disque
virtuel qcow2 faisait 25 Gio. Les sorties transmises montrent une table MBR,
`vda1` EFI, `vda2` étendue et `vda5` logique ext4 portant `/`. Après agrandissement,
la table reçue montre `vda2` et `vda5` terminant à **42,9 Go (40 Gio)** ;
les captures suivantes confirment la capacité accrue du système de fichiers.

La procédure proposée utilisait `qemu-img resize … 40G` sur l’hyperviseur,
`resizepart 2 100%` puis `resizepart 5 100%`, un redémarrage et
`resize2fs /dev/vda5` dans la VM. Parted affichait initialement l’aide française
(`redimpart`) ; la relance avec `LC_ALL=C` a été proposée pour utiliser les
commandes anglaises. Les états obtenus sont prouvés ; les sorties de chaque
commande de modification ne sont pas toutes conservées. La sauvegarde de VM
et sa restauration ont été demandées dans la procédure, mais leur réalisation
n’est pas prouvée par ces captures. Aucun retour arrière exécuté n’est rapporté.

### Preuves visuelles des étapes Ubuntu

![Ubuntu 22.04.5 : contrôles système et Docker après migration](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2010-47-55.png)

![Ubuntu 24.04.5 : disque agrandi et contrôles après migration](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2011-15-31.png)

![Ubuntu 24.04 : File Browser démarré, healthcheck encore en cours](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2011-16-09.png)

![Ubuntu 26.04.1 : contrôles système, Docker actif et File Browser healthy](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2011-34-32.png)


### Preuves visuelles complémentaires

**Capture 10:46:55 — Étape Ubuntu 22.04.5 : accès SSH et Docker actif.**

![Étape Ubuntu 22.04.5 : accès SSH et Docker actif](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2010-46-55.png)

### Validation applicative et limites de clôture

La capture de 10:15:23 montre déjà une session `admin` et **File Browser 2.63.23**
avant les migrations Ubuntu. Après la dernière étape, celle de 11:35:15 montre
la même version et la capacité accrue du stockage. Celle de 11:36:11 montre
les dossiers `interne`, `partenaires`, `public`, le fichier `test` de 30 octets
et `test2` de 38 octets ; le navigateur indique le téléchargement de `test2`
**terminé**. Olivier confirme ensuite **« tout ok »** pour les tests proposés :
connexion, consultation, téléchargement et dépôt d’un fichier de test.
Le dépôt et l’authentification avec le nouveau secret sont des résultats
attribués à son retour ; les captures montrent une session ouverte et le
fichier présent, sans exposer de mot de passe.

![File Browser 2.63.23 avant migration Ubuntu](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2010-15-23.png)

![File Browser 2.63.23 accessible après migration, stockage agrandi](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2011-35-15.png)

![Fichiers de test présents et téléchargement de test2 terminé](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2011-36-11.png)

**Bilan R01 : migration appliquée et fonctionnement validé.** La sortie finale
Docker indique le moteur `29.1.3-0ubuntu1.4` et containerd `2.1.3`, selon les
lignes de journal visibles. Cela ne clôture pas automatiquement C01/C02/C03 :
relever les versions exactes des paquets, la configuration SSH et produire des
rescans Greenbone/Lynis comparables pour qualifier les constats de sécurité.
Le retour à l’invite sans sortie d’audit de paquets et l’absence d’unités en
échec ne prouvent pas l’absence de vulnérabilités.

Des avertissements Docker `error locating sandbox id … not found` restent
visibles au démarrage. Leur cause n’est pas établie ; ils ne suffisent pas à
qualifier une panne alors que le conteneur est healthy et les tests réussis.
Les identifiants internes ne sont pas retranscrits dans le texte.

**R08 : reprise après redémarrage corroborée par l’état final du conteneur.**
La valeur exacte `unless-stopped` est confirmée par la collecte de 11:45 ; la capture
ne prouve pas une persistance après une nouvelle recréation. **R03 : version
2.63.23 visible et fonctionnement confirmé ; risques résiduels du scan conservés.**
R09 dispose maintenant d’une capture du refus des identifiants, présentée
dans sa section ci-dessous ; les captures de session attestent l’accès applicatif.

## Complément final — Collecte du 2 octobre 2026 à 11:45:00 +02:00

**Source : sorties exécutées par Olivier et transmises dans la conversation.**
Les adresses, empreintes de clé SSH et identifiants de démarrage ne sont pas
reproduits. Cette collecte précise les versions finales : les versions de
journaux tronqués ou lues dans les captures ne remplacent pas `dpkg-query`.

| Contrôle | Résultat observé | Validation / suite |
| --- | --- | --- |
| OS / paquets | Ubuntu 26.04.1 ; noyau `7.0.0-38-generic` ; aucun message de `dpkg --audit` ; aucune unité en échec | Fonctionnement système corroboré ; rescans de sécurité encore nécessaires |
| Versions exactes installées | OpenSSH `1:10.2p1-2ubuntu3.6`, Docker `29.1.3-0ubuntu4.1`, containerd `2.2.2-0ubuntu1.1` | Référence finale des paquets pour R01 ; ne clôture pas seule les CVE |
| Services | SSH, Docker et containerd actifs ; Docker/containerd activés ; SSH déclenché par `ssh.socket`, unité service désactivée | Ne pas qualifier SSH de panne à partir du seul état disabled ; vérifier l’activation du socket si nécessaire |
| Connexion SSH | Journal : authentification par clé ED25519 acceptée pour Olivier après redémarrage | Accès par clé observé ; conserver une session et une console avant R02 |
| Syntaxe et paramètres SSH | `sshd -t` sans erreur ; `passwordauthentication yes`, `permitrootlogin prohibit-password`, transferts permis, deux MAC UMAC-64 encore présents | R02 non appliquée ; examiner Include/Match avant durcissement |
| Image | Digest `sha256:a469ea076d4a1b4b1d86a41d130f2f536cd9da996a2b1fb39c0d7635f9d89b9a` ; ImageID `sha256:b3983274c0375dda1722f8e2b65c30d1b9001435e441f0a34855c2e5f8da462e` ; utilisateur déclaré `user` | Concordance avec l’image 2.63.23 scannée |
| Montages | Trois bind mounts distincts sous le répertoire persistant : `/config`, `/database`, `/srv`, tous RW | Persistance configurée prouvée ; test de recréation encore distinct |
| Reprise | `RestartPolicy.Name=unless-stopped`, compteur 0 | Politique R08 maintenant corroborée par inspection et reprise finale observée |
| Isolation | `Privileged=false`, `ReadonlyRootfs=false`, `SecurityOpt=null`, `CapAdd=null`, `CapDrop=null` | Conteneur non privilégié ; racine modifiable ; pas de restrictions personnalisées dans ces champs |
| PID 1 | `tini`, UID/GID 1000 ; CapEff/CapPrm nuls ; CapBnd `00000000a80425fb` ; NoNewPrivs 0 ; Seccomp 2 | Amélioration d’identité du PID 1 par rapport à l’ancien conteneur root ; vérifier séparément le processus File Browser enfant |

**R04 partiellement améliorée par R03 :** le PID 1 est non root et sans
capacités effectives. Ce PID est désormais `tini`, contrairement à l’ancien
PID 1 `filebrowser` : vérifier l’UID, les capacités et NoNewPrivs du processus
applicatif pour comparer les mêmes objets. Les protections no-new-privileges,
réduction des capacités et racine en lecture seule restent à tester selon les
besoins d’écriture. Aucun changement additionnel n’est appliqué par cette collecte.

### Complément — Include SSH et processus applicatif

Sorties transmises par Olivier le 2 octobre 2026, sans horodatage propre :
`sshd_config` inclut `/etc/ssh/sshd_config.d/*.conf` à la ligne 24 ; aucun
fichier n’est retourné par la collecte du répertoire. Aucun bloc Match actif
n’est retourné par la recherche du fichier principal. `ssh.socket` est activé.
La configuration calculée avec `sshd -T -C` pour la connexion d’Olivier
confirme les mots de passe acceptés, root permis par clé, transferts permis
et les MAC UMAC-64 présents. R02 reste à appliquer.

`docker top` montre `tini -- /init.sh` et
`filebrowser --config=/config/settings.json`, tous deux sous l’utilisateur
hôte `oliv` (UID 1000 dans la collecte précédente). L’exécution non root du
processus applicatif est ainsi corroborée ; ses capacités et NoNewPrivs restent
à relever séparément. Aucun durcissement supplémentaire n’est démontré.

## R02 — Premier lot SSH appliqué et nouveau relevé Lynis

**Source : captures transmises par Olivier le 2 octobre 2026.** La configuration
calculée pour sa connexion affiche `permitrootlogin no`,
`pubkeyauthentication yes`, `passwordauthentication no` et
`kbdinteractiveauthentication no`. Les MAC `umac-64-etm@openssh.com` et
`umac-64@openssh.com` sont absents de la liste finale.

Le test SSH avec clés désactivées et méthode password imposée retourne
`Permission denied (publickey)` : le refus du parcours par mot de passe est
observé. Ce test a été lancé depuis la VM vers son adresse réseau, selon
l’invite visible ; une nouvelle connexion par clé depuis l’hyperviseur après
rechargement, suivie de `sudo -v`, reste à confirmer explicitement. Le journal
antérieur prouve une connexion par clé avant ce lot, pas après celui-ci.

Le fichier `lynis.log` fourni a été examiné : **Lynis 3.1.6**, audit du
**2 octobre 2026 de 11:56:54 à 11:57:47**, Ubuntu 26.04.1, fin réussie,
**259 tests exécutés** et indice de durcissement **65**. Ce score ne mesure pas
un pourcentage de sécurité et ne suffit pas à conclure à une amélioration sans
une référence initiale comparable. Le relevé confirme `PermitRootLogin NO`.

Les suggestions SSH restantes portent notamment sur les transferts TCP/agent,
X11, LogLevel, MaxAuthTries et MaxSessions ; leur traitement dépend des usages.
Ne pas changer le port pour obtenir un score. Les suggestions auditd
(ACCT-9628), CUPS (PRNT-2307) et sysctl (KRNL-6000) restent à contextualiser.
La base EOL de ce Lynis ne reconnaît pas Ubuntu 26.04.1 : c’est une limite de
l’outil, pas une preuve de fin de support de l’OS.

**Statut R02 : premier lot appliqué, paramètres et refus du mot de passe
vérifiés ; nouvelle connexion par clé après changement à confirmer.** Le
journal brut contient des informations internes : les seules observations
utiles sont synthétisées ici, sans recopier son contenu intégral.

### R02 — Accès administrateur après durcissement confirmé

La nouvelle capture transmise par Olivier montre une connexion depuis
l’hyperviseur avec réutilisation de connexion désactivée et méthodes password /
keyboard-interactive désactivées. La bannière Ubuntu 26.04.1 apparaît ;
`sudo -v` suivi de `echo $?` retourne **0**. La connexion par clé et l’accès
sudo après durcissement sont donc confirmés. Le premier lot R02 est validé
sur ses paramètres et son fonctionnement ; les autres restrictions restent
à sélectionner selon les usages.

### Rapport Greenbone reçu — Périmètre à vérifier

Le XML a été retrouvé dans le dossier **it-4**, et non it-1 indiqué dans le
message. Sa fenêtre est **2 octobre 2026, 11:47:38–11:53:14 +02:00**
(09:47:38–09:53:14 UTC dans l’export). Le filtre est `levels=chml`,
`min_qod=70`, `apply_overrides=0`. Les trois résultats exportés ont un QoD de 80 :

| Résultat exporté | Sévérité | Hôte indiqué |
| --- | --- | --- |
| TCP Timestamps Information Disclosure | Low, 2.6 | `127.0.0.1` |
| Weak MAC Algorithm(s) Supported (SSH) | Low, 2.6 | `127.0.0.1`, port 22 |
| ICMP Timestamp Reply Information Disclosure | Low, 2.1 | `127.0.0.1` |

**Limite majeure :** loopback désigne la machine dans le contexte du scanner.
Confirmer où OpenVAS s’exécute et la cible de la tâche avant d’attribuer ces
résultats à la VM auditée. Aucun résultat HIGH/MEDIUM/CRITICAL n’est exporté
avec ce filtre ; cela ne prouve pas l’absence de vulnérabilités sur la VM.
La chronologie exacte du rechargement SSH par rapport au scan n’est pas
fournie : le résultat MAC peut précéder l’application du lot ou concerner une
autre machine. Refaire un scan de la cible vérifiée après durcissement pour
clôturer C05. Les deux informations de timestamps restent à contextualiser,
sans appliquer automatiquement les commandes proposées par le scanner.

### Cible Greenbone — Configuration confirmée par capture

Olivier précise que le scanner tourne sur son poste et utilise une clé SSH
dédiée au compte d’audit, distincte de sa clé personnelle. La capture de la
cible **AIS-Ubuntu20-avec-auth** indique `192.168.122.229`, un seul hôte,
la liste **All IANA assigned TCP** et l’identifiant **AIS-SSH-gvm-audit**
sur le port 22. Cette configuration est correcte pour viser la VM ; elle ne
prouve pas à elle seule une authentification réussie pendant le scan.

Le XML est bien associé à une cible portant le même nom, mais les trois
résultats exportés indiquent `127.0.0.1`. L’écart entre configuration actuelle
et résultats reste inexpliqué : ne pas conclure automatiquement à un scan du
poste ni à un tunnel SSH. Comparer l’hôte dans le rapport affiché par Greenbone,
le rapport complet et le succès des contrôles authentifiés. Un nouveau scan
après correction avec export complet doit permettre de vérifier cette attribution.

### Nouveau scan Greenbone — 2 octobre 2026, 12:11:59–12:17:23 +02:00

L’export `report-033adb79-59bf-4076-bfdb-3d372e86794a.xml`, retrouvé dans
**it-4**, indique `Done` et la même tâche/cible **AIS-Ubuntu20-avec-auth**.
Le filtre reste `levels=chml`, `min_qod=70`, `apply_overrides=0` : les résultats
Log ne sont pas inclus. Les deux résultats exportés, QoD 80, sont **TCP
Timestamps Information Disclosure (Low 2.6)** et **ICMP Timestamp Reply
Information Disclosure (Low 2.1)**. Ils indiquent encore `127.0.0.1`.

**Évolution observée :** le résultat **Weak MAC Algorithm(s) Supported (SSH)**
présent dans l’export précédent n’apparaît plus dans celui-ci, avec les mêmes
filtres. Cela concorde avec le retrait UMAC-64 capturé ; l’attribution réseau
reste cependant à établir avant de clôturer définitivement C05 sur cette base.
Aucun résultat HIGH/MEDIUM/CRITICAL n’est exporté dans ce périmètre filtré.

**Validation restante :** exporter les résultats Log et ceux de QoD inférieur
pour rechercher les preuves de connexion SSH du scanner, puis expliquer
l’adresse loopback dans l’export malgré la cible configurée sur l’adresse de
la VM. Ne pas présenter les deux timestamps comme des vulnérabilités corrigées
ni appliquer leurs mitigations sans analyse d’impact.

### Réexport du même rapport — QoD minimum abaissé à 0

Le fichier du rapport `033adb79` a été remplacé par un export plus large du
**même scan**, sans nouvelle fenêtre de scan. Le filtre est désormais
`levels=chml min_qod=0` : les résultats Log restent exclus.

| Niveau | Nombre de résultats exportés |
| --- | --- |
| Critical | 10 |
| High | 73 |
| Medium | 113 |
| Low | 8 |
| Total | **204**, avec 204 identifiants de résultats distincts |

Répartition de confiance : **191 résultats QoD 30**, **6 QoD 1**, **5 QoD 50**
et **2 QoD 80**. Les deux résultats QoD 80 sont les timestamps déjà documentés.
Ces compteurs ne sont ni 204 CVE uniques ni 204 vulnérabilités applicables.
Les mêmes noms de tests reviennent sur plusieurs résultats ; 56 noms distincts
sont présents. Tous les hôtes exportés restent `127.0.0.1`.

Des contradictions apparentes nécessitent une qualification : un résultat
**OpenSSH < 10.1** cite une détection **10.2p1** ; une alerte libcurl d’octobre
2023 cite **8.18.0**. Plusieurs résultats sudo concernent un chemin **snap**,
notamment `/snap/core24/2124/usr/bin/sudo`, à distinguer du paquet de l’hôte.
Examiner les plages affectées dans les avis officiels, les correctifs de la
distribution et les chemins réellement utilisés avant de retenir ou exclure
chaque association. La faible confiance ne suffit pas à écarter un résultat.

Les détections de fichiers par tests nommés **Linux/Unix SSH Login** sont
compatibles avec des contrôles locaux authentifiés, mais cet export ne fournit
pas le résultat Log de succès d’authentification demandé. Exporter également
les Log et vérifier l’attribution à la VM avant de clôturer les constats.
La comparaison précédente « deux Low » décrivait le filtre QoD ≥ 70, pas
l’ensemble des résultats enregistrés par le scanner.

### Export avec Log — Authentification du scanner confirmée

Le réexport examiné inclut maintenant `levels=chmlg min_qod=0` : **248 résultats**,
soit les 204 résultats de sécurité précédents et **44 Log**. Il s’agit toujours
du même scan du 2 octobre, 12:11:59–12:17:23 +02:00.

**Preuve explicite :** résultat **SSH Login Successful For Authenticated Checks**
et détail d’hôte **Auth-SSH-Success : Protocol SSH, Port 22, User gvm-audit**.
L’authentification du compte d’audit a donc réussi après le durcissement.
L’identification locale relève **Ubuntu 26.04 LTS**, noyau **7.0.0-38-generic**,
OpenSSH **10.2p1** dans `/usr/sbin/sshd`, et des binaires **9.6p1** dans
`/snap/core24/2124/`. Ces éléments concordent avec la VM et expliquent la
nécessité de distinguer paquets hôte et composants snap dans les alertes.

L’adresse exportée reste `127.0.0.1`. Sa cause n’est pas établie, mais elle
ne justifie plus d’affirmer que les contrôles authentifiés n’ont pas réussi.
La concordance OS/noyau et la cible configurée soutiennent l’attribution à la
VM ; garder l’écart d’adresse comme limite de traçabilité à expliquer. Les clés
publiques, empreintes et autres données internes de l’export ne sont pas recopiées.

**Bilan :** authentification du scanner confirmée ; premier lot SSH fonctionnel,
y compris pour gvm-audit ; absence du constat MAC faibles dans l’export après
correction. Les 202 résultats de sécurité sous QoD 70 restent à qualifier,
notamment par composant, chemin, version affectée et correctif de distribution.
Aucun nouveau changement ni suppression de snap n’est justifié par le seul compteur.

## R04 — Test du premier lot Docker réussi sur copie

**Retour d’Olivier du 2 octobre 2026 :** le conteneur
`filebrowser-hardening-test`, publié sur 8081, est **Up 3 minutes (healthy)**.
Les logs confirment `/config/settings.json`, `/database/filebrowser.db` et
l’écoute sur le port 80. L’heure `10:36:50` du journal n’a pas de fuseau explicite
et n’est pas assimilée à l’heure locale du poste.

| Contrôle | Résultat reçu |
| --- | --- |
| Utilisateur déclaré | `user` |
| Options de sécurité | `["no-new-privileges:true"]` |
| Capacités retirées | `["ALL"]` |
| PID 1 tini | UID/GID 1000 ; CapEff et CapBnd nuls ; NoNewPrivs 1 ; Seccomp 2 |
| Tests fonctionnels | Téléchargement, upload et suppression réussis selon Olivier |

**Statut : premier lot R04 testé avec succès sur copie ; bascule du service
principal sur 8080 encore à effectuer.** Le test porte sur le PID 1 ; relever
également les mêmes champs pour le processus File Browser enfant après bascule.
La racine en lecture seule n’est pas appliquée dans ce lot.

Le journal rappelle l’archivage du projet et l’absence de futures corrections.
Le durcissement du conteneur limite ses privilèges, mais ne corrige pas les
vulnérabilités compilées dans l’image et ne rétablit pas la maintenance R03.

### R04 — Bascule, reprise puis retour arrière effectivement exécuté

La capture fournie montre le nouveau conteneur principal healthy sur 8080,
`unless-stopped`, `no-new-privileges:true` et `CapDrop=["ALL"]`. Le contrôle du
processus **filebrowser** confirme UID/GID 1000, CapEff/CapBnd nuls,
NoNewPrivs 1 et Seccomp 2. Le relevé après redémarrage indique **Up 18 seconds
(healthy)** : la reprise du conteneur durci est observée. Les opérations sur
fichiers avaient été confirmées sur la copie ; leur confirmation explicite
sur le principal après bascule reste à recueillir.

**Dernière action reçue :** Olivier a ensuite exécuté les commandes de retour
arrière : arrêt du conteneur durci, renommage en `filebrowser-hardening-failed`,
renommage de `filebrowser-before-hardening` en `filebrowser`, puis démarrage.
Les commandes stop/start retournent `filebrowser`, sans erreur affichée.
L’état final attendu est donc l’ancien conteneur remis en service ; vérifier
son inspection avant de déclarer les protections actives. Le nom « failed »
provient de la procédure de secours et **ne prouve pas une panne** : aucune
panne du conteneur durci n’est rapportée.

**R04 : protections et reprise vérifiées, puis retour arrière exécuté ;
réactivation du conteneur durci à réaliser.** Les mêmes montages étaient
utilisés par les deux conteneurs de même image ; aucune restauration de la
copie de sauvegarde n’est rapportée. Ne pas démarrer les deux simultanément
sur la même base. La racine reste modifiable dans ce premier lot.

### R04 — Conteneur durci réactivé : état final reçu

Le dernier relevé transmis par Olivier confirme, pour le conteneur principal
`filebrowser`, **SecurityOpt=["no-new-privileges:true"]**, **CapDrop=["ALL"]**
et **Up 2 minutes (healthy)**, publié sur **8080 → 80**. Le conteneur correspond
à celui dont les privilèges applicatifs et la reprise après redémarrage avaient
été vérifiés avant le retour arrière. Le premier lot R04 est donc de nouveau
actif ; le retour arrière reste conservé dans l’historique.

**Validation restante :** confirmer connexion, téléchargement, upload et
suppression fictive sur le service principal **8080** après cette réactivation.
Ces opérations étaient réussies sur la copie 8081 ; elles ne sont pas encore
explicitement confirmées pour ce dernier état. La racine en lecture seule
et les risques résiduels de l’image restent hors du lot appliqué.

## R06 / R05 — Désactivation CUPS et installation auditd

**État initial reçu : 2 octobre 2026, 12:53:42 +02:00.** CUPS/cups-daemon
`2.4.16-1ubuntu1.3` ; trois unités activées et actives ; écoute 631 uniquement
sur loopback ; aucune imprimante ni destination par défaut ; cupsd.conf
mode 644 root:root. auditd et audispd-plugins absents ; environ 19 Go libres.

Olivier a exécuté `systemctl disable --now` pour cups.service, cups.socket et
cups.path. La validation finale affiche trois **disabled**, trois **inactive**
et aucune écoute 631. L’avertissement transitoire sur les unités déclenchantes
pendant l’arrêt n’invalide pas cette validation finale. Les paquets ne sont
pas supprimés ; aucune correction de CVE ni modification de droits CUPS n’est
attribuée à l’arrêt. Le parcours File Browser après ce lot et la persistance
après redémarrage restent à confirmer.

**R05 : auditd installé, version 1:4.1.2-1ubuntu0.1**, actif et activé depuis
12:55:09 ; audit-rules.service activé par le paquet. `auditctl -s` : enabled 1,
failure 1, lost 0, backlog 0, backlog_limit 8192. `auditctl -l` affiche
**No rules** : installation validée, mais audit ciblé non encore configuré.
Le message No plugins found décrit l’absence de plugins de dispatch ; il ne
prouve pas une absence de journalisation locale. Règles, événement de test,
rotation/rétention et validation après redémarrage restent à compléter.


### Preuves visuelles complémentaires

**Capture 12:54:43 — État initial : CUPS actif sur loopback et auditd absent.**

![État initial : CUPS actif sur loopback et auditd absent](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2012-54-43.png)

**Capture 12:54:57 — Premier arrêt CUPS : disabled, inactive et aucune écoute 631 ; persistance encore à vérifier.**

![Premier arrêt CUPS : disabled, inactive et aucune écoute 631 ; persistance encore à vérifier](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2012-54-57.png)

### R05 — Sept règles chargées et événement retrouvé

Sorties reçues d’Olivier le 2 octobre 2026 : sauvegarde de `/etc/audit`
commandée, fichier `50-ais.rules` édité et mode 640 appliqué ; chargement par
`augenrules --load`. Le message initial No rules pendant le chargement est
suivi d’un `auditctl -l` contenant **sept règles b64** : écritures/attributs
sur passwd, group, shadow, gshadow, sudoers, sudoers.d et ssh. Les clés sont
`ais_identity`, `ais_sudo` et `ais_ssh`. État final : enabled 1, lost 0, backlog 0.

Le test à **12:57:07** retrouve la création puis la suppression du fichier
`.ais-audit-test…` dans `/etc/ssh`, avec clé **ais_ssh**, appels **openat** et
**unlinkat**, `success=yes`, identité de connexion Olivier et identité effective
root via sudo. L’événement CONFIG_CHANGE à 12:56:44 prouve aussi l’ajout de la
règle. Les paramètres et contenus SSH n’ont pas été modifiés par le test.
Seule la règle SSH a un test fonctionnel reçu ; aucune modification des
comptes ou des règles sudo n’est exécutée pour fabriquer des preuves.

**Rotation configurée observée :** `/var/log/audit/audit.log`, limite **8 Mio**,
**num_logs 5**, action **ROTATE** ; dossier de 48 Kio au relevé. Il s’agit d’une
rétention bornée par taille, pas de cinq jours. Alerte SYSLOG sous 75 Mio libres,
SUSPEND sous 50 Mio, disque plein ou erreur disque. Ces seuils tardifs et la
suspension sont documentés ; prévoir une supervision de l’espace et des pertes.
La configuration existante est conservée pour ce laboratoire, sans prétendre
qu’une rotation réelle a déjà été observée ni qu’elle constitue une politique
de conservation d’entreprise. Test de rotation et persistance des règles après
redémarrage restent à vérifier ; les règles b32 sont hors du périmètre actuel.


### Preuves visuelles complémentaires

**Capture 12:56:36 — Sept règles audit b64 proposées dans le fichier de configuration.**

![Sept règles audit b64 proposées dans le fichier de configuration](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2012-56-36.png)

**Capture 12:57:02 — Chargement et liste effective des sept règles ; lost 0 et backlog final 0.**

![Chargement et liste effective des sept règles ; lost 0 et backlog final 0](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2012-57-02.png)

**Capture 12:57:19 — Création et suppression du fichier de test : événements ais_ssh retrouvés.**

![Création et suppression du fichier de test : événements ais_ssh retrouvés](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2012-57-19.png)

**Capture 12:57:36 — Configuration de rétention et rotation auditd.**

![Configuration de rétention et rotation auditd](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2012-57-36.png)

**Capture 12:58:52 — Première rotation manuelle réussie : audit.log.1 présent, auditd actif et lost 0.**

![Première rotation manuelle réussie : audit.log.1 présent, auditd actif et lost 0](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2012-58-52.png)

### Validation après redémarrage — 13:02:17 +02:00

Le relevé d’Olivier du 2 octobre confirme **auditd actif**, les **sept règles
b64 conservées**, enabled 1, lost 0 et backlog 0. L’événement CONFIG_CHANGE de
12:59:07 montre le chargement au démarrage ; à **13:02:49**, création puis
suppression d’un nouveau fichier de test sont retrouvées avec clé ais_ssh et
success=yes. **R05 : persistance et événement après reboot validés** ; la sortie
du test de rotation n’a pas été fournie et reste à joindre.

Docker a repris : **filebrowser Up 3 minutes (healthy)** sur 8080,
no-new-privileges:true et CapDrop ALL toujours présents. Le parcours navigateur
après ce dernier reboot n’est pas explicitement confirmé dans ce retour.

**R06 : validation après reboot en échec.** Les trois unités CUPS sont disabled,
mais cups.service et cups.socket sont **active**, cups.path inactive ; écoute
631 sur loopback IPv4/IPv6 de nouveau présente. Disabled ne bloque pas une
activation à la demande ou par dépendance. La source exacte de cette activation
n’est pas établie. Pour le choix retenu d’une VM sans impression, proposer
le masquage des trois unités avec arrêt immédiat, conserver les paquets et
vérifier l’absence d’écoute avant puis après reboot. Le retour arrière est
unmask puis restauration des états initiaux enabled/active si le besoin revient.
Aucun masquage n’est encore prouvé dans ce relevé.


### Preuves visuelles complémentaires

**Capture 13:02:41 — Après reboot : règles audit persistantes, Docker durci healthy, mais CUPS réactivé malgré disabled.**

![Après reboot : règles audit persistantes, Docker durci healthy, mais CUPS réactivé malgré disabled](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2013-02-41.png)

**Capture 13:02:57 — Événements ais_ssh de création et suppression retrouvés après reboot.**

![Événements ais_ssh de création et suppression retrouvés après reboot](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2013-02-57.png)

### R06 — Masquage validé après redémarrage, 13:05:40 +02:00

Le relevé final d’Olivier du 2 octobre affiche **masked** pour cups.service,
cups.socket et cups.path, **inactive** pour les trois, et aucune écoute sur
631. Il est transmis après la procédure de masquage et de redémarrage.
**R06 : arrêt persistant validé dans ce contrôle après reboot.** Les paquets
CUPS restent installés ; aucune correction de CVE ni purge n’est revendiquée.

File Browser est **Up 5 seconds (healthy)** sur 8080, avec le même conteneur
durci que dans les vérifications précédentes. Sa reprise est observée ; ce
relevé ne contient pas un nouveau parcours navigateur. Le retour arrière de
R06 est unmask des trois unités puis restauration de leur activation initiale,
uniquement si le besoin d’impression revient.


### Preuves visuelles complémentaires

**Capture 13:05:22 — Masquage des trois unités CUPS et absence d’écoute 631.**

![Masquage des trois unités CUPS et absence d’écoute 631](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2013-05-22.png)

**Capture 13:05:58 — Après reboot : CUPS masked et inactive, port 631 sans écoute, File Browser healthy.**

![Après reboot : CUPS masked et inactive, port 631 sans écoute, File Browser healthy](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2013-05-58.png)

### R05 — Rotation manuelle vérifiée, relevé vers 13:07

Olivier a exécuté `auditctl --signal rotate`. Le listing montre **audit.log
1,4 Kio**, **audit.log.1 621 Kio** et **audit.log.2 45 Kio** ; le dossier totalise
684 Kio. Les deux premiers fichiers portent l’heure 13:07, le second journal
archivé 12:58. Un journal archivé et un nouveau journal actif sont donc observés.
`auditctl -s` confirme enabled 1, **lost 0** et **backlog 0**.

**R05 validée pour le périmètre retenu :** sept règles b64 persistantes,
événement SSH retrouvé avant/après reboot, rotation manuelle opérationnelle
et absence de perte au relevé. Le déclenchement automatique au seuil de 8 Mio
n’a pas été provoqué ; sa configuration ROTATE/num_logs 5 est documentée.
Aucune conservation en jours ni test exhaustif des règles identité/sudo n’est
revendiqué. Les seuils d’espace et la suspension de journalisation restent
à surveiller selon le besoin du laboratoire.


### Preuves visuelles complémentaires

**Capture 13:07:51 — Nouvelle rotation auditd réussie, archives présentes, lost 0 et backlog 0.**

![Nouvelle rotation auditd réussie, archives présentes, lost 0 et backlog 0](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2013-07-51.png)

## R07 — Qualification initiale sysctl, 13:09:46 +02:00

Olivier fournit les valeurs effectives, les interfaces/routes et les fragments
sysctl du fournisseur. La VM a une interface réseau de laboratoire et un
bridge docker0 ; route IPv4 par défaut vers l’hyperviseur et route du sous-réseau
Docker. Les routes IPv6 reçues sont uniquement link-local.

| Paramètre / état reçu | Décision proposée et justification |
| --- | --- |
| fs.protected_fifos 1 | Tester 2 : étendre la protection aux répertoires sticky inscriptibles par le groupe ; vérifier les usages applicatifs |
| kernel.kptr_restrict 1 | Tester 2 : masquer davantage les adresses noyau ; impact possible sur les diagnostics privilégiés |
| ip_forward / all.forwarding 1 | Conserver pour le réseau Docker ; ne pas imposer le profil d’un hôte sans routage |
| all.rp_filter 2 | Conserver le mode souple ; fragment fournisseur en 2, compatibilité des routes Docker à préserver |
| unprivileged_bpf_disabled 2 | Conserver : BPF non privilégié déjà désactivé ; valeur réversible administrativement |
| modules_disabled 0 | Conserver dans ce laboratoire : ne pas bloquer irréversiblement les chargements de modules jusqu’au reboot |
| suid_dumpable 2 et core_pattern pipe Apport | Garder pour ce premier lot ; examiner la collecte/les permissions avant de supprimer le diagnostic |
| sysrq 176 | Garder pour ce premier lot ; masque de fonctions de secours, ne pas assimiler toute valeur non nulle à toutes les fonctions activées |
| bpf_jit_harden 0 | Lot distinct à qualifier selon usages/impact |
| Redirects IPv4/IPv6 et log_martians | Lot réseau à préparer avec valeurs par interface et tests ; aucune mutation réseau dans ce premier lot |

Les fragments examinés dans `/usr/lib/sysctl.d` sont des valeurs du fournisseur,
à conserver. Un fragment local dédié sera proposé pour les seules valeurs
retenues. **Premier lot préparé, aucune application prouvée à ce stade.**
L’écart entre core_pattern effectif (Apport) et le fragment fournisseur (core)
montre qu’une autre source peut modifier les valeurs ; un grep ne suffit pas
à attribuer toutes les valeurs à un unique fichier ni à prouver leur persistance.


### Preuves visuelles complémentaires

**Capture 13:10:21 — Interfaces, routes et paramètres persistants avant durcissement sysctl.**

![Interfaces, routes et paramètres persistants avant durcissement sysctl](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2013-10-21.png)

### R07 — Premier lot appliqué, contrôle après reboot à 13:12:36 +02:00

Le relevé d’Olivier du 2 octobre, transmis après la procédure de modification
et redémarrage, confirme **fs.protected_fifos=2** et **kernel.kptr_restrict=2**.
Le conteneur principal File Browser est **Up 8 seconds (healthy)** sur 8080.
L’audit noyau est enabled 1, **lost 0**, **backlog 0**.

**Premier lot R07 : valeurs effectives et persistance après redémarrage
validées.** La nouvelle session permet le relevé administrateur ; les opérations
File Browser après ce dernier reboot et les tests ciblés d’effet de sécurité
ne sont pas fournis dans ce retour. Ne pas les déduire du seul healthcheck.
Les autres paramètres sysctl restent ceux de la qualification initiale ;
aucun changement réseau, BPF, Apport, SysRq ou modules n’est revendiqué.


### Preuves visuelles complémentaires

**Capture 13:12:03 — Configuration du premier lot : protected_fifos et kptr_restrict à 2.**

![Configuration du premier lot : protected_fifos et kptr_restrict à 2](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2013-12-03.png)

**Capture 13:12:53 — Après reboot : deux valeurs à 2, File Browser healthy et audit sans perte.**

![Après reboot : deux valeurs à 2, File Browser healthy et audit sans perte](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2013-12-53.png)

### R07 — Confirmation fonctionnelle après le dernier reboot

Olivier confirme **« c’est bon »** en réponse à la demande de vérifier connexion,
téléchargement et upload dans File Browser après le reboot du premier lot R07.
Ces tests sont donc **réussis selon son retour**, en complément du relevé
13:12:36 montrant les deux valeurs à 2, le conteneur healthy et lost 0.
Aucune nouvelle capture de ces opérations n’est attribuée à cette confirmation.
**Premier lot R07 : application, persistance et fonctionnement validés** ;
tests ciblés d’effet de sécurité et qualification des autres paramètres restent
distincts de cette validation fonctionnelle.

### R07 — Lot réseau appliqué : valeurs effectives reçues

État initial du 2 octobre 2026 à **13:17:46 +02:00** : redirections IPv4 en
réception à 1 sur default/enp1s0/docker0, all à 0 ; émission IPv4 à 1 et réception
IPv6 à 1 sur les quatre entrées. File Browser utilise le réseau bridge IPv4.

Après la procédure du fragment local `99-ais-network.conf`, Olivier fournit
un relevé sans horodatage propre : **accept_redirects IPv4/IPv6 et send_redirects
IPv4 à 0** sur **all, default, enp1s0 et docker0**. **ip_forward=1** et
**all.rp_filter=2** sont conservés. File Browser est **Up 14 seconds (healthy)**
sur 8080. Les paramètres de forwarding et le filtrage souple n’ont pas été
sacrifiés pour satisfaire le profil Lynis.

**Lot réseau : application et valeurs effectives vérifiées.** Le relevé est
reçu après la demande de reboot, mais ne comporte ni heure de démarrage ni
confirmation explicite de ce reboot ; le seul Up 14 seconds peut aussi suivre
un redémarrage du conteneur. Confirmer séparément le reboot et les tests de
nouvelle connexion SSH, téléchargement, upload et suppression sur 8080 avant
de clôturer la persistance et le fonctionnement du lot. Aucun test de paquet
ICMP Redirect injecté n’est rapporté.


### Preuves visuelles complémentaires

**Capture 13:17:58 — État réseau avant le deuxième lot et réseau bridge Docker IPv4.**

![État réseau avant le deuxième lot et réseau bridge Docker IPv4](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2013-17-58.png)

**Capture 13:19:42 — Configuration des redirections IPv4 et IPv6 à 0.**

![Configuration des redirections IPv4 et IPv6 à 0](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2013-19-42.png)

**Capture 13:20:41 — Valeurs effectives après redémarrage déclaré : redirections à 0, forwarding 1, rp_filter 2 et File Browser healthy.**

![Valeurs effectives après redémarrage déclaré : redirections à 0, forwarding 1, rp_filter 2 et File Browser healthy](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2013-20-41.png)

### R07 — Lot réseau : reboot et fonctionnement confirmés

Olivier confirme **« c’est bon »** en réponse à la demande de confirmer que
le relevé des redirections à 0 est effectué après reboot de la VM et que la
nouvelle connexion SSH, le téléchargement, l’upload et la suppression sur
8080 fonctionnent. **Persistance et tests fonctionnels du lot réseau validés
selon ce retour utilisateur**, en complément des valeurs effectives fournies.
L’heure exacte du reboot et de chaque test n’est pas fournie ; aucune capture
supplémentaire ni injection ICMP de test n’est supposée.

**R07 : deux lots appliqués et validés sur leur configuration/persistance et
fonctionnement.** Les autres paramètres sont conservés ou à qualifier selon
le tableau initial ; cette validation ne signifie pas que toutes les
suggestions sysctl de Lynis ont été appliquées ni tous leurs effets testés.

## Rescan Lynis après remédiations — 13:23:26–13:24:23

Le journal fourni par Olivier depuis `/home/oliv/lynis.log` est conservé sous
un [nom distinct après remédiations](../../assets/files/securisation-avancee-infrastructures/it-4/lynis-apres-remediations-20261002-132326.log),
sans écraser le relevé précédent. **Lynis 3.1.6**, même version que le scan de
11:56 ; **259 tests exécutés**, fin réussie. Les paramètres détaillés de lancement
et le profil exact restent à conserver pour une comparaison complète.

| Contrôle | Relevé 11:56 | Relevé 13:23 | Conclusion |
| --- | --- | --- | --- |
| Indice de durcissement | 65 | **67** | +2 points, indicateur du profil ; pas un pourcentage de sécurité |
| Écarts sysctl KRNL-6000 | 15 | **9** | Six écarts du profil ne sont plus signalés |
| FIFO / adresses noyau | Valeurs 1 | **2**, conformes au profil | Corrobore le premier lot R07 |
| Redirections | Plusieurs écarts | all.send_redirects IPv4 et accept_redirects contrôlés conformes | Corrobore le lot réseau R07 |
| Auditd ACCT-9628 / ACCT-9630 | Absent | **En fonctionnement, règles trouvées** | Corrobore R05 ; preuves d’événement et rotation documentées séparément |
| CUPS | Processus actif, suggestion PRNT-2307 | **cupsd non trouvé** ; tests de configuration/droits ignorés | Corrobore l’arrêt R06 ; disparition de la suggestion ne prouve pas des droits corrigés |

**Neuf écarts sysctl restants :** suid_dumpable, modules_disabled, sysrq,
unprivileged_bpf_disabled, bpf_jit_harden, all.forwarding, all.rp_filter,
all.log_martians et default.log_martians. Les décisions de maintien pour Docker,
BPF non privilégié et diagnostics sont consignées dans R07 ; bpf_jit_harden
et log_martians restent à qualifier. Ne pas appliquer aveuglément les neuf
valeurs du profil. Les six écarts disparus ne sont pas six CVE corrigées.

**Suggestions SSH encore présentes :** transferts TCP/agent, X11, LogLevel,
MaxAuthTries, MaxSessions, ClientAliveCountMax, TCPKeepAlive et port. Les lots
réalisés ne visaient pas toutes ces options. Les usages et les gains doivent
être justifiés avant tout lot additionnel.

Le scan suggère aussi intégrité des fichiers, collecte externe des logs,
politique des comptes, permissions et divers outils. Ce sont des mesures
complémentaires à sélectionner dans le contexte du laboratoire, pas des preuves
que les remédiations réalisées ont échoué. Le rescan ne remplace pas Trivy ni
la qualification des alertes Greenbone ; il ne prouve pas la sécurité globale
ou la correction de toutes les CVE des paquets.

## Qualification ciblée des résultats Greenbone

Analyse documentaire du rapport `033adb79`, sans modification de la VM.
Les conclusions ci-dessous portent uniquement sur le composant et la version
mentionnés dans chaque résultat ; elles ne couvrent pas les autres copies,
notamment dans les snaps. La contradiction doit être conservée dans le dossier
et rapprochée d’un inventaire local avant clôture définitive.

| Résultat | Détection dans le rapport | Référence éditeur | Qualification |
| --- | --- | --- | --- |
| CVE-2023-38545 | libcurl 8.18.0, `/usr/lib/x86_64-linux-gnu/libcurl.so.4.8.0`, QoD 30 | [curl : versions affectées 7.69.0 à 8.3.0, corrigé dès 8.4.0](https://curl.se/docs/CVE-2023-38545.html) | Version détectée hors plage affectée : résultat contradictoire, exclusion proposée pour cette copie sous réserve de confirmation locale |
| CVE-2025-26466 | OpenSSH 10.2p1, port 22, QoD 30 | [OpenSSH 9.9p2 : correction du déni de service SSH2_MSG_PING](https://www.openssh.org/txt/release-9.9p2) | Version détectée postérieure au correctif : exclusion proposée pour ce service, cohérente avec le paquet openssh-server déjà relevé |
| CVE-2024-39894 | OpenSSH 10.2p1, port 22, QoD 30 | [OpenSSH 9.8 : correction du client ObscureKeystrokeTiming](https://www.openssh.org/txt/release-9.8) | Version hors plage 9.5–9.7 ; le défaut concerne le client. La bannière du serveur ne constitue pas un inventaire de tous les clients SSH |
| CVE-2025-32462 | sudo 1.9.15p5 dans `/snap/core24/2124/usr/bin/sudo` | [Suivi Ubuntu de la CVE](https://ubuntu.com/security/CVE-2025-32462) | À qualifier : relever la version complète du paquet dans le snap et ses éventuels correctifs rétroportés. La version du sudo de l’hôte ne permet pas de clôturer ce résultat |

**Prochaine preuve attendue :** inventaire des paquets hôte, liste des révisions
snap et version du paquet sudo embarqué dans core24. Aucun retrait de snap ni
mise à jour forcée n’a été exécuté à ce stade. Ces quelques résultats ne
permettent pas de classer globalement les 204 résultats de sécurité comme faux
positifs ou comme vulnérabilités confirmées.

### Inventaire local confirmé — 13:32:17 +02:00

Olivier a exécuté le contrôle sur `oliv-Standard-PC-Q35-ICH9-2009`.
Le précédent relevé de 13:31:38 provenait du poste `ubuntu-oliv` et ne constitue
pas une preuve des paquets installés dans la VM.

| Paquet de la VM | Version complète |
| --- | --- |
| libcurl4t64:amd64 | 8.18.0-1ubuntu2.7 |
| openssh-client et openssh-server | 1:10.2p1-2ubuntu3.6 |
| sudo de l’hôte VM | 1.9.17p2-1ubuntu3.1 |

Cet inventaire corrobore les exclusions proposées pour CVE-2023-38545 sur la
copie libcurl système et CVE-2025-26466 / CVE-2024-39894 sur les composants
OpenSSH système inventoriés. Il ne couvre pas les copies embarquées dans les
snaps et ne démontre pas l’absence de toute autre vulnérabilité.

Le snap **core24 20260824, révision 2124**, est actif ; `current` pointe vers
`/snap/core24/2124`, chemin correspondant au résultat Greenbone sudo. Les deux
recherches de base dpkg n’ont affiché aucune version de sudo : son niveau de
correctif reste **non vérifié**. Les révisions core20 1828, snap-store 638 et
snapd 18357 sont désactivées ; leur présence seule ne prouve pas leur exécution.
Aucune suppression de révision n’a été effectuée.

### Sudo de core24 — correctif rétroporté identifié

La sortie transmise après les contrôles de 13:33 confirme, à la ligne 246 de
`/snap/core24/2124/usr/share/snappy/dpkg.list`, le paquet **sudo
1.9.15p5-3ubuntu5.24.04.2**, amd64. Le fichier est un tableau `dpkg -l` :
les recherches précédentes visant un champ `Package:` ou un nom en début de
ligne ne correspondaient pas à son format. Le binaire a le bit SUID ; cette
permission seule ne démontre pas une vulnérabilité.

[Ubuntu USN-7604-1](https://ubuntu.com/security/notices/USN-7604-1) indique que
**CVE-2025-32462 et CVE-2025-32463** sont corrigées pour Noble dans
`1.9.15p5-3ubuntu5.24.04.1`. La révision `.2` inventoriée dans core24 est
postérieure à cette révision corrigée. **CVE-2025-32462 : résultat Greenbone
classé faux positif de version pour cette copie**, sur la base de l’inventaire
complet et du correctif Ubuntu rétroporté. La comparaison de la seule version
amont `1.9.15p5` n’intègre pas ce correctif. Aucune exploitation n’a été tentée,
aucune modification du snap ni du bit SUID n’a été réalisée. Cette conclusion
ne couvre pas les autres révisions ou copies de sudo présentes dans le rapport.

## État initial reçu — 2 octobre 2026 à 09:43:29 +02:00

**Source : sorties de commandes exécutées par Olivier sur la VM et transmises
dans la conversation.** Cette collecte constitue une preuve de l’état initial,
pas une validation après remédiation. Les identifiants de machine/démarrage et
les identifiants internes Docker ne sont pas reproduits.

| Contrôle exécuté | Résultat observé | Conclusion et limite |
| --- | --- | --- |
| `date -Is`, `hostnamectl`, `/etc/os-release`, `uname -r` | Ubuntu **20.04.6 LTS**, VM KVM x86-64, noyau **5.15.0-139-generic** | La VM est toujours sur Ubuntu 20.04 ; la cible 26.04 n’est pas appliquée |
| `dpkg-query -W openssh-server docker.io containerd` | OpenSSH **1:8.2p1-4ubuntu0.13**, Docker **26.1.3-0ubuntu1~20.04.1**, containerd **1.7.24-0ubuntu1~20.04.2** | Versions initiales confirmées ; aucune correction logicielle n’est démontrée par cette collecte |
| `systemctl status ssh docker containerd` | Trois services **active (running)**, unités activées ; démarrage vers 09:06:48–49 | Fonctionnement des processus observé ; plusieurs lignes de journal sont tronquées et ne permettent pas un diagnostic complet |
| `ss -lntup` — SSH / application | TCP **22** et **8080** sur toutes les interfaces IPv4/IPv6 ; 8080 porté par docker-proxy | Écoute locale confirmée ; aucune joignabilité Internet ni validation HTTP/applicative démontrée |
| `ss -lntup` — CUPS / containerd | CUPS **631** sur loopback IPv4/IPv6 ; containerd sur **127.0.0.1:41485** | Exposition locale limitée à loopback pour ces écoutes ; ne pas assimiler le port containerd ponctuel à une configuration permanente |
| `ss -lntup` — DNS / découverte | Résolveur local **127.0.0.53:53** ; Avahi UDP **5353** sur IPv4/IPv6, autres ports UDP observés | Présence des services observée ; aucune panne DNS ni défaut Avahi qualifié sur cette seule base |
| `docker ps -a` | Un conteneur nommé **filebrowser**, image **filebrowser/filebrowser:v2.15.0**, **Up 34 minutes (healthy)** ; publication **8080 → 80/tcp** IPv4/IPv6 | Conteneur en exécution et healthcheck réussi au relevé ; image ancienne toujours utilisée. Le statut healthy ne remplace pas les tests d’authentification, de droits et de fichiers |

**Avancement :** l’étape 1 « vérifier l’état initial » dispose maintenant de
résultats pour l’OS, les versions, les services, les écoutes et l’état du
conteneur. R01 et R03 restent **à réaliser**. Le complément ci-dessous fournit la configuration
SSH de base, l’identité exacte de l’image et les montages. Les contextes Match
et les privilèges effectifs restent à compléter pour les lots concernés. Aucun changement de mot de passe
n’est prouvé par ces commandes : R09 reste à réaliser/valider selon le plan.

### Complément reçu — Configuration SSH et inspection Docker

**Source : commandes exécutées par Olivier, communiquées le 2 octobre 2026.**
Cette sortie complémentaire ne contient pas d’horodatage propre ; elle est
rattachée au retour utilisateur, sans lui attribuer automatiquement l’heure
09:43:29 du relevé précédent. Aucun changement n’est démontré.

| Contrôle | Résultat observé | Qualification |
| --- | --- | --- |
| `sudo sshd -t` | Retour à l’invite sans message d’erreur | Aucune erreur de validation signalée ; code de retour non fourni. Cela ne prouve pas une nouvelle connexion ni un durcissement |
| `sudo sshd -T` — accès | `passwordauthentication yes`, `pubkeyauthentication yes`, `permitrootlogin without-password`, `maxauthtries 6` | C04 précisé : mot de passe accepté ; root peut être autorisé par clé, pas par mot de passe avec cette valeur. Aucune clé root effectivement autorisée n’est démontrée |
| `sudo sshd -T` — transferts | `allowtcpforwarding yes`, `allowagentforwarding yes`, `x11forwarding yes`, `allowstreamlocalforwarding yes`, `disableforwarding no` | Fonctions permises dans la configuration affichée ; usages à inventorier avant restrictions R02 |
| `sudo sshd -T` — protections et traces | `gssapiauthentication no`, `permitemptypasswords no`, `strictmodes yes`, `loglevel INFO` | Protections partielles présentes ; aucun niveau de sécurité global n’en est déduit |
| `sudo sshd -T` — MAC | `umac-64-etm@openssh.com` et `umac-64@openssh.com` présents dans la liste | C05 corroboré : les deux MAC signalés au J3 restent configurés ; aucune négociation réelle n’est mesurée |
| Image du conteneur | `filebrowser/filebrowser:v2.15.0`, ImageID `sha256:a68f43720ea6ff331fa4b92becced20af14b72f4c3a22ca1f764076a8e42e1a5` | Identité concordante avec l’image étudiée au J3 ; R03 non appliquée au relevé |
| Montage | Bind `/srv/filebrowser` vers `/srv`, `RW=true`, propagation `rprivate` | Montage documentaire en lecture-écriture confirmé ; droits applicatifs et fichiers réellement accessibles non établis par ce seul contrôle |
| Utilisateur / options Docker | `.Config.User` vide ; `.HostConfig.SecurityOpt` vaut `null` | Aucun utilisateur explicite ni option de sécurité personnalisée dans ces champs. Ne prouve pas l’absence de protections par défaut ; l’UID réel et NoNewPrivs restent à relever |

La sortie `sshd -T` ne fournit pas de contexte `-C` : les éventuels blocs
`Match` doivent être examinés pour les comptes et connexions concernés.
Elle décrit la configuration calculée depuis les fichiers au moment du test,
pas à elle seule les paramètres chargés par un processus qui n’aurait pas
été rechargé après une modification.

**Avancement :** R02 dispose maintenant d’une référence de configuration ;
R03/R04 disposent de l’image exacte et du montage. Les validations après
correction restent **Non vérifiable**. Le résultat `.Config.User` vide ne
remplace pas le contrôle d’UID déjà consigné au J3 : il faut le relever à
nouveau si l’on veut attester l’état actuel.

**Contrôles complémentaires proposés sur la VM, non exécutés ici :**

```bash
sudo docker exec filebrowser cat /proc/1/status
sudo docker inspect --format '{{.HostConfig.Privileged}} {{.HostConfig.ReadonlyRootfs}} {{json .HostConfig.CapAdd}} {{json .HostConfig.CapDrop}}' filebrowser
sudo docker inspect --format '{{json .HostConfig.RestartPolicy}}' filebrowser
sudo grep -nE '^[[:space:]]*(Include|Match)([[:space:]]|$)' /etc/ssh/sshd_config
```

Dans `/proc/1/status`, relever notamment `Uid`, `Gid`, `CapEff`, `NoNewPrivs`
et `Seccomp`. Examiner aussi les fichiers réellement inclus, puis choisir
le contexte `sshd -T -C` correspondant aux connexions à préserver. Ces
contrôles restent des observations ; aucune restriction ne doit être déclarée
appliquée à partir des sorties initiales.

### Complément reçu — Privilèges effectifs et politique de redémarrage

**Source : sorties exécutées par Olivier et communiquées le 2 octobre 2026,
sans horodatage propre dans ce complément.** Les relevés décrivent l’état
avant durcissement R04 ; aucune modification de privilèges n’est démontrée.

| Contrôle exécuté | Valeur observée | Interprétation limitée |
| --- | --- | --- |
| `/proc/1/status` — identité | PID 1 `filebrowser`, `Uid: 0 0 0 0`, `Gid: 0 0 0 0` | Processus exécuté avec UID/GID 0 dans le conteneur ; ne prouve pas un accès root à la VM |
| `/proc/1/status` — capacités | `CapPrm`, `CapEff`, `CapBnd` : `00000000a80425fb` ; `CapInh`/`CapAmb` nuls | Capacités effectives présentes ; absence de capacités héritables/ambiantes ne signifie pas absence de privilèges |
| `/proc/1/status` — élévation | `NoNewPrivs: 0` | Protection no-new-privileges non activée pour le processus relevé |
| `/proc/1/status` — filtrage | `Seccomp: 2`, `Seccomp_filters: 1` | Filtrage seccomp actif ; règles exactes et couverture non évaluées |
| Inspection Docker — isolation | `Privileged=false`, `ReadonlyRootfs=false` | Mode privilégié désactivé ; racine du conteneur non déclarée en lecture seule |
| Inspection Docker — capacités personnalisées | `CapAdd=null`, `CapDrop=null` | Aucun ajout ni retrait explicite dans ces champs ; les capacités effectives restent celles relevées ci-dessus |
| Inspection Docker — reprise | `RestartPolicy={"Name":"no","MaximumRetryCount":0}` | Pas de redémarrage automatique prévu par cette politique Docker ; besoin de reprise R08 à définir, sans qualifier une panne |

**C10 est corroboré dans l’état actuel :** UID/GID 0, capacités effectives,
NoNewPrivs désactivé et racine modifiable, avec le montage documentaire RW
confirmé dans le relevé précédent. Le mode non privilégié et seccomp sont des
protections présentes. Aucun accès non autorisé, évasion de conteneur ou
compromission n’est démontré.

**R04 reste à préparer/tester avant application.** Identifier les écritures
nécessaires de l’application et de sa base, tester un UID non privilégié et
les droits adaptés sur données fictives, puis réduire les capacités et activer
no-new-privileges si compatibles. La racine en lecture seule nécessite des
chemins d’écriture explicitement prévus. Ne pas modifier globalement les
propriétaires des documents ni retirer toutes les capacités sans tests.

Après modification, répéter les mêmes contrôles et vérifier démarrage,
connexion, téléchargement/téléversement autorisés et persistance des données.
**R08 reste conditionnelle :** choisir une politique de reprise uniquement
après définition du comportement attendu ; le statut healthy et la politique
no ne prouvent pas ensemble une reprise automatique après redémarrage.

### Compléter la collecte avant changement

Sur la VM, commandes proposées, **non encore exécutées dans les résultats reçus** :

```bash
sudo systemctl status ssh docker containerd --no-pager -l
sudo sshd -t
sudo sshd -T
sudo docker inspect --format '{{.Config.Image}} {{.Image}}' filebrowser
sudo docker inspect --format '{{json .Mounts}}' filebrowser
sudo docker inspect --format '{{.Config.User}} {{json .HostConfig.SecurityOpt}}' filebrowser
sudo docker inspect --format '{{json .HostConfig.RestartPolicy}}' filebrowser
```

Conserver les résultats pertinents sans données internes ni secrets. La
politique de redémarrage actuelle n’est pas déduite du statut « Up » : elle
doit être relevée. Confirmer séparément une nouvelle connexion SSH et un
parcours File Browser dans le navigateur pour établir la référence fonctionnelle.
La procédure R09 peut ensuite être mise en œuvre en conservant les preuves
avant/après prévues.

## R09 — Mot de passe administrateur changé : retour du 2 octobre 2026

**Source : test et modification déclarés par Olivier.** L’utilisateur confirme
avoir changé le mot de passe administrateur File Browser et que l’ancien mot
de passe ne fonctionne plus, **y compris en navigation privée**. La méthode
exacte de changement et son heure ne sont pas fournies. Une capture ajoutée
le même jour montre le refus de connexion ; son nom indique 11:38:14, sans
horodatage visible dans l’interface. Aucun nouveau mot de passe n’est reproduit
dans le mémo.

| Élément | Résultat documenté |
| --- | --- |
| Constat traité | **C13 — Identifiants par défaut actifs** : connexion `admin` / `admin` initialement réussie selon le test utilisateur |
| Modification réalisée | **R09 appliquée selon le retour utilisateur** : mot de passe administrateur remplacé |
| Commandes / configuration utilisées | Méthode exacte à renseigner ; aucune commande ni utilisation de l’interface n’est supposée |
| Vérification réalisée | Tentative avec l’ancien mot de passe, notamment en navigation privée |
| Résultat obtenu | Capture : compte `admin`, mot de passe masqué et message **Wrong credentials** ; Olivier attribue ce refus à l’essai de l’ancien mot de passe |
| Test fonctionnel | Connexion avec le nouveau secret et opérations sur fichiers confirmées par Olivier ; session et téléchargement de `test2` visibles dans les captures précédentes |
| Problème rencontré, le cas échéant | Aucun problème signalé dans ce retour ; ne constitue pas un bilan exhaustif |
| Démarche de diagnostic | Non nécessaire pour un échec non signalé ; aucune investigation supplémentaire fournie |
| Solution / décision finale | Conserver le nouveau secret de façon privée ; changement et tests fonctionnels validés selon le retour utilisateur, avec capture du refus |
| Limites restantes | Secret essayé non lisible dans la capture ; navigation privée attestée par le retour utilisateur ; méthode/heure du changement et révocation des sessions déjà ouvertes non documentées |
| Statut | **Appliquée ; refus capturé et attribué aux anciens identifiants par Olivier ; fonctionnement confirmé** |

### Capture — Refus des anciens identifiants

![File Browser : compte admin et message Wrong credentials, mot de passe masqué](../../assets/img/securisation-avancee-infrastructures/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-02%2011-38-14.png)

La capture montre un refus de connexion pour `admin`. Le champ masqué ne
permet pas d’identifier le secret essayé : le lien avec l’ancien mot de passe
et le test en navigation privée repose sur le retour d’Olivier. Cette preuve,
complétée par l’accès fonctionnel confirmé, documente R09 sans publier de secret.
Elle ne prouve pas la révocation des jetons ou sessions déjà ouverts. C13
conserve sa preuve initiale et son historique.

## 1. Choisir un premier lot et conserver sa référence

| Ordre | Remédiation | Constat / objectif | Recherche et prérequis |
| --- | --- | --- | --- |
| 1 | **R09 — Mot de passe File Browser** | C13 : connexion `admin` / `admin` réussie selon le test utilisateur | Identifier le compte, la méthode de changement dans cette version et l’accès de secours ; conserver la preuve initiale |
| 2 | **R01 — Migration de l’hôte** | C07 et écarts logiciels C01/C02/C03 ; C06 si conservé | Cible Ubuntu 26.04 ; choisir nouvelle VM ou étapes 20.04 → 22.04 → 24.04 → 26.04, vérifier la disponibilité réelle et tester la restauration |
| 3 | **R02 — SSH** | C03/C04/C05 : paquet, accès et MAC | Vérifier clés, clients, usages des transferts, configuration effective et console de secours |
| 4 | **R03 — Mise à niveau File Browser** | C12 : image et dépendances anciennes | Sélectionner la release et le digest ; vérifier migration de base et sauvegarde cohérente ; traiter la fin de maintenance du projet |
| 5 | **R04 — Privilèges**, puis R05/R06 si retenus | C10 : droits ; C08 : audit ciblé ; C06 : CUPS | Valider droits nécessaires, volumes et dépendances avant chaque changement |

La dernière release File Browser relevée dans la préparation est 2.63.23.
Le [projet original est archivé](https://github.com/filebrowser/filebrowser) :
une dernière version publiée ne garantit pas une maintenance future. Documenter
le risque résiduel et le choix de maintien temporaire ou de remplacement.
La migration de l’hôte ne met pas à jour les bibliothèques embarquées dans
l’image ; une image neuve ne garantit pas le changement d’un mot de passe
conservé dans la base existante.

Ne pas appliquer toutes les recommandations pour améliorer un score. Retenir
les risques importants, les changements compatibles et les résultats vérifiables.
R07 (sysctl) reste une investigation et R08 (reprise) dépend du besoin validé.

## 2. Rechercher avant de modifier

Pour chaque action, relever la version exacte, la documentation correspondante,
les fichiers ou paramètres concernés, la syntaxe, les dépendances et la méthode
de retour. Lire les aides locales en complément des références suivantes :

| Composant | Documentation utile | Recherche à effectuer |
| --- | --- | --- |
| Ubuntu | [Mise à niveau officielle](https://ubuntu.com/server/docs/how-to/software/upgrade-your-release/) | Parcours supporté, dépôts, espace, paquets bloqués, sauvegarde et redémarrages |
| File Browser | [Dépôt et documentation du projet](https://github.com/filebrowser/filebrowser), notes de la release choisie | Changement de mot de passe, base/configuration réellement utilisées, compatibilité et sessions |
| Docker | [Inspection ciblée d’un conteneur](https://docs.docker.com/reference/cli/docker/container/inspect/) | ImageID/digest, montages, utilisateur, ports et paramètres du conteneur réellement déployé |
| OpenSSH | [Manuel sshd](https://man.openbsd.org/sshd.8) ; `man sshd` et `man sshd_config` de la VM | Validation syntaxique, configuration effective, Include/Match et options de la version locale |
| Services et journaux | `man systemctl`, `man journalctl` | Unité réelle, état, rechargement/restart et recherche sur la fenêtre du changement |

**À renseigner pour chaque recherche :** lien ou manuel, version concernée,
commande retenue, fichier/paramètre exact et raison du choix. Ne pas exécuter
une commande de mutation avant d’en comprendre l’effet et le retour arrière.
Les commandes de modification restent à rechercher par l’apprenant.

## 3. Appliquer les sept étapes à chaque modification

### 1 — Vérifier l’état initial

Relever date, machine, version, configuration et reproduction limitée du défaut.
Conserver les configurations initiales et sauvegardes en privé selon le lot.
Pour une base applicative, choisir une sauvegarde cohérente et tester sa
restauration ; une simple copie pendant des écritures peut être insuffisante.

**Sur la VM cible, commandes de lecture proposées, non exécutées :**

```bash
date -Is
hostnamectl
cat /etc/os-release
uname -r
dpkg-query -W openssh-server docker.io containerd
sudo systemctl status ssh docker containerd --no-pager
sudo ss -lntup
sudo docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
```

Adapter les paquets et unités à l’installation réelle : Docker peut provenir
d’autres paquets que `docker.io`. Un nom absent ne prouve pas que le logiciel
n’est pas installé. Relever les erreurs plutôt que les masquer.

Pour R09, conserver le résultat de l’essai unique des identifiants par défaut.
Pour R02, relever la configuration effective SSH. Pour R03/R04, identifier
l’image et les montages avant toute suppression/recréation de conteneur.

### 2 — Rechercher la modification

À partir de l’état initial, choisir la méthode et vérifier qu’elle s’applique
à la version présente. Écrire les commandes retenues et leur effet attendu.
Si un paramètre dépend du contexte (Match SSH, UID, volume, réseau), préciser
ce contexte. Ne pas choisir un UID ni un chemin de base par supposition.

### 3 — Appliquer la modification

Appliquer une action ou un lot cohérent dans la fenêtre choisie. Noter heure,
commande exacte et objets modifiés. Garder l’accès de secours pour SSH.
Pour une migration, maîtriser les écritures et conserver l’état cohérent
nécessaire au retour arrière. Ne pas publier de secret dans une commande,
une capture, un historique ou le mémo.

### 4 — Vérifier la configuration obtenue

Relire la valeur effective, pas seulement le fichier édité. Vérifier versions,
source des paquets, digest, paramètres chargés et erreurs de validation.

**Exemples ciblés sur la VM, à adapter et non exécutés :**

```bash
sudo sshd -t
sudo sshd -T
sudo docker inspect --format '{{.Config.Image}} {{.Image}}' NOM_CONTENEUR
sudo docker inspect --format '{{json .Mounts}}' NOM_CONTENEUR
sudo docker inspect --format '{{.Config.User}} {{json .HostConfig.SecurityOpt}}' NOM_CONTENEUR
```

Remplacer `NOM_CONTENEUR` par le nom réellement relevé. Pour les blocs Match,
compléter `sshd -T` avec le contexte de connexion approprié. Une valeur Docker
`User` vide demande de contrôler l’UID réel du processus ; elle ne suffit pas
à valider le durcissement. Ne pas diffuser un export d’inspection complet
susceptible de contenir des secrets d’environnement.

### 5 — Vérifier l’effet de sécurité

Rejouer le test du défaut dans les mêmes conditions pertinentes et comparer :

| Action | Test de sécurité attendu |
| --- | --- |
| R09 | Dans une nouvelle session privée, `admin` / `admin` refusé ; vérifier le comportement des sessions déjà ouvertes |
| R01 | Versions corrigées et sources vérifiées ; nouveaux constats Greenbone comparés aux anciens, pas seulement un compteur total |
| R02 | Valeurs effectives conformes et restrictions réellement testées ; contrôle des MAC proposés/négociés |
| R03 | Trivy sur l’image exacte ; comparer résultats et changements de bases/options ; qualifier les risques résiduels |
| R04 | UID/capacités/NoNewPrivs conformes ; accès ou écriture hors droits refusés |
| R05/R06 | Événement d’audit ciblé retrouvé / disparition de l’écoute et des unités CUPS prévues |

Pour Trivy, conserver le JSON complet sous un nom distinct et utiliser un export
HIGH/CRITICAL séparé. Ne pas écraser la preuve initiale. Une baisse de compteur
ne suffit pas si les bases ou le périmètre ont changé. Le projet File Browser
signale des limites sur la révocation des JWT : ne pas déduire leur invalidation
d’un simple changement de mot de passe ou d’une déconnexion.

### 6 — Vérifier que le service reste fonctionnel

Tester une **nouvelle connexion SSH** et le parcours File Browser : connexion
avec les bons identifiants, navigation, téléchargement/téléversement fictifs,
séparation des comptes, lecture seule et déconnexion. Choisir les opérations
qui répondent au rôle du compte testé.

**Depuis la machine d’audit**, après confirmation de l’IP actuelle :

```bash
CIBLE_IP="192.168.122.229"
nc -vz -w 3 "$CIBLE_IP" 22
nc -vz -w 3 "$CIBLE_IP" 8080
curl --max-time 10 -I "http://$CIBLE_IP:8080/"
```

Ces commandes sont des exemples non exécutés. Adapter protocole/port si le
déploiement change. Un port accessible ou une réponse HTTP ne valide pas les
autorisations ni le parcours complet ; le test navigateur reste nécessaire.
Vérifier après redémarrage les changements dont la persistance est attendue.

### 7 — Documenter le résultat

Renseigner la fiche ci-dessous et le
[journal des changements](../dossier-preuves.md#journal-des-changements).
Relier les preuves avant/après au constat et distinguer les statuts :
**préparée**, **appliquée à vérifier**, **validée**, **échouée / retour effectué**.
Ne clôturer qu’après preuve de sécurité et test fonctionnel réussis.

## 4. Fiche de résultat — À dupliquer pour chaque remédiation

| Élément | Description / résultat réel |
| --- | --- |
| Identifiant et date | R… / C… — date et machine à renseigner |
| Constat traité | Référence du J3, risque et preuve initiale |
| Modification réalisée | **Non vérifiable** — renseigner uniquement ce qui a été appliqué |
| Commandes / configuration utilisées | **À renseigner** — commandes exactes, fichiers, paramètres et source technique ; sans secret |
| Vérification réalisée | **Non vérifiable** — contrôle effectif et test de sécurité avant/après |
| Résultat obtenu | **Non vérifiable** — sortie, interprétation, risque résiduel et référence de capture |
| Test fonctionnel | **Non vérifiable** — parcours, compte/rôle, résultat et preuve |
| Problème rencontré, le cas échéant | **À renseigner** — « aucun » seulement après mise en œuvre et vérifications |
| Démarche de diagnostic | **À renseigner** — observations, commandes, hypothèses vérifiées |
| Solution / décision finale | **À renseigner** — correction validée, autre méthode justifiée, report ou retour arrière |
| État initial et retour arrière | Sauvegarde/configuration conservée, méthode, résultat si réellement exécuté |
| Statut de clôture | **Préparée — non appliquée dans cette feuille** |

### Suivi des actions retenues

| Action | Mise en œuvre | Sécurité après changement | Fonctionnement après changement | Décision |
| --- | --- | --- | --- | --- |
| R09 — Mot de passe | Changé selon le retour utilisateur | Refus Wrong credentials capturé ; ancien mot de passe et navigation privée selon Olivier | Accès et opérations confirmés par Olivier ; session visible dans les captures | Appliquée et tests utilisateur validés ; révocation des anciennes sessions non vérifiée |
| R01 — Ubuntu / moteurs | Migration 20.04 → 22.04 → 24.04 → 26.04.1 ; disque porté à 40 Gio | Versions changées ; clôture des CVE et rescans hôte à compléter | Captures : aucune unité en échec, Docker actif, File Browser healthy ; tests applicatifs confirmés par Olivier | Appliquée ; fonctionnement validé ; validation de sécurité à compléter |
| R02 — SSH | Root interdit, mots de passe/interactif désactivés, deux MAC UMAC-64 retirés | Paramètres effectifs capturés ; refus password observé ; Lynis confirme root interdit | Nouvelle connexion par clé depuis hyperviseur et sudo (code 0) confirmés | Premier lot validé ; transferts et autres réglages à contextualiser |
| R03 — File Browser | Bascule 2.63.23 déclarée et version visible dans les captures | Trivy examiné : 10 HIGH, 0 CRITICAL ; applicabilité et maintenance future à traiter | Healthy après migration ; parcours confirmé et téléchargement capturé | Appliquée ; fonctionnement validé ; risques résiduels ouverts |
| R08 — Reprise | Politique unless-stopped confirmée par inspection ; Docker activé | Montages persistants config/base/documents confirmés | File Browser en fonctionnement après le redémarrage final | Reprise corroborée ; test après recréation distinct à compléter |
| R04 — Privilèges | Lot cap-drop ALL / no-new-privileges appliqué, retour arrière puis réactivation confirmée | Processus filebrowser UID 1000, capacités nulles, NoNewPrivs 1 observés sur le conteneur durci | Healthy et reprise prouvés ; téléchargement, upload et suppression sur 8080 documentés | Premier lot appliqué et validé ; racine read-only hors lot |
| R05 — Audit ciblé | auditd actif ; sept règles b64 chargées ; rotation 8 Mio, num_logs 5 | lost 0 ; création/suppression sous ais_ssh retrouvées | Événement réussi avant/après reboot ; sept règles persistantes ; rotation manuelle réussie, lost 0 | R05 validée sur le périmètre b64 retenu ; rotation automatique au seuil non testée |
| R06 — CUPS | Trois unités masquées, arrêtées et contrôlées après reboot | Aucune écoute 631 à 13:05:40 ; paquets conservés | File Browser healthy après reboot ; nouveau parcours navigateur à confirmer | R06 appliquée ; arrêt persistant validé |
| R07 — sysctl | Deux paramètres hôte à 2 ; redirections IPv4/IPv6 désactivées, forwarding 1 et rp_filter 2 conservés | Lot hôte persistant ; valeurs du lot réseau vérifiées ; tests ciblés de sécurité à compléter | File Browser healthy ; audit enabled, lost 0 ; connexion/téléchargement/upload confirmés après reboot | Lots hôte et réseau validés ; reboot et tests SSH/fichiers confirmés par Olivier |

## 5. En cas de problème : diagnostiquer avant de poursuivre

Arrêter le lot, noter le symptôme et l’heure. Déterminer si le défaut concerne
la syntaxe, le service, le processus, le port, le réseau, les droits ou
l’application. Ne pas cumuler des changements sans pouvoir attribuer leurs effets.

**Sur la VM, exemples de recherche non exécutés :**

```bash
sudo systemctl status NOM_UNITE --no-pager
sudo journalctl -u NOM_UNITE --since '15 minutes ago' --no-pager
sudo ss -lntup
sudo docker logs --since 15m NOM_CONTENEUR
sudo docker inspect --format '{{json .State}}' NOM_CONTENEUR
```

Adapter les noms et la fenêtre au changement réel ; conserver les messages
pertinents et les masquer si nécessaire avant diffusion. Pour une migration
Ubuntu, examiner aussi les journaux de mise à niveau réellement produits.

| Symptôme possible — pas un incident observé | Informations à examiner | Décision à justifier |
| --- | --- | --- |
| SSH refuse la nouvelle connexion | Console, validation syntaxique, valeurs Match, état/unité et journaux, clé et permissions | Corriger la cause ou restaurer les seuls fichiers du lot via l’accès de secours |
| File Browser ne démarre plus | État/logs, image exacte, base/configuration, UID, montages et chemins d’écriture | Corriger une incompatibilité prouvée ou restaurer image et données cohérentes |
| HTTP répond mais une opération échoue | Droits du compte, portée applicative, permissions du montage et logs de l’opération | Corriger le droit précis ; ne pas accorder tous les droits globalement |
| Ancien jeton reste utilisable | Test en session distincte, configuration et documentation de la version | Documenter la limite ; choisir une mesure adaptée ou revoir la solution |
| Upgrade interrompu | Erreur, espace, réseau, dépôts, dépendances et journaux | Corriger la cause selon la documentation ou restaurer l’état validé |

Pour chaque incident, documenter **problème, symptômes, commandes/informations,
cause si établie, solution essayée et résultat**. Une hypothèse reste une
hypothèse tant qu’elle n’a pas été vérifiée. Si une autre méthode est préférable,
modifier le plan en expliquant le risque, les contraintes et les preuves qui
justifient ce choix. Préciser si le retour arrière a réellement été exécuté.

## État final attendu et preuves

Chaque action clôturée comporte une configuration effective conforme, un test
de sécurité attribuable au changement, un test fonctionnel réussi et les
preuves datées. Les actions non retenues, échouées ou différées gardent leur
justification et leurs risques résiduels. Aucun nombre de corrections ni
résultat de scan n’est inventé pour compléter les tableaux.

## 📚 Notions acquises

Mise en œuvre d’un plan de remédiation, recherche documentaire, vérification de
configuration effective, validation de sécurité, test fonctionnel, diagnostic,
retour arrière et traçabilité des décisions.

- [Activité précédente — Préparer les remédiations](preparer-remediations.md)
- [Rapport et plan du J3](../it-3/finaliser-rapport-plan-remediation.md)
- [Dossier de preuves](../dossier-preuves.md)
- [Retour à l’itération 4](index.md)
- [Retour au module](../README.md)

## Historique des interventions — Image, persistance et reprise avant Ubuntu

Olivier retient l’ordre **R03 → persistance applicative → R08 → R01**.
La mise à jour File Browser et la préparation de sa reprise précèdent Ubuntu.
Le changement du mot de passe R09 est déclaré réalisé, pas la migration.

### Localiser les données avant remplacement

**Sur la VM Ubuntu**, commandes de lecture à exécuter ; résultats non encore
fournis. Ne pas recréer le conteneur avant la sauvegarde cohérente de la base
et de la configuration : le seul montage connu conserve les documents.

```bash
sudo docker inspect --format '{{json .Config.Entrypoint}} {{json .Config.Cmd}}' filebrowser
sudo docker exec filebrowser sh -c 'tr "\000" " " < /proc/1/cmdline; printf "\n"'
sudo docker exec filebrowser sh -c 'ls -la / /database /config 2>/dev/null'
sudo docker diff filebrowser
sudo systemctl is-enabled docker
```

Les chemins `/database` et `/config` sont des pistes à vérifier, pas des chemins
attestés sur cette image. Relever ensuite les chemins de base/configuration
réellement chargés, sauvegarder ces éléments sans publier leur contenu et
préparer les montages correspondants. Garder l’ancien conteneur/image et une
copie cohérente de la base jusqu’à validation de la migration.

**Cible de reprise retenue : `unless-stopped`.** La configuration doit être
reprise dans la méthode de déploiement utilisée ; son application reste à
réaliser. Tester la reprise après redémarrage de Docker/VM depuis un conteneur
en fonctionnement. Après un arrêt manuel, cette politique conserve l’arrêt :
un démarrage explicite est nécessaire. Vérifier séparément la persistance
après recréation et le fonctionnement applicatif après redémarrage.

### Résultats reçus — Localisation de la base File Browser

Sorties exécutées par Olivier et communiquées le 2 octobre 2026, sans
horodatage propre dans ce complément :

| Contrôle | Observation | Conséquence pour R03/persistance |
| --- | --- | --- |
| Entrypoint / Cmd et `/proc/1/cmdline` | Entrypoint `/filebrowser`, Cmd null, processus `/filebrowser` sans argument | Les paramètres peuvent provenir du fichier de configuration ou des valeurs par défaut ; contenu utile à vérifier |
| Liste de la racine | `/database.db` présent, 65 536 octets, mode 600, propriétaire root ; `/.filebrowser.json` présent, 117 octets | Sauvegarder la base et la configuration avant remplacement ; les chemins `/database` et `/config` ne sont pas établis par ce relevé |
| `docker diff filebrowser` | `A /database.db`, changement `/root`, ajout d’historique shell | La base a été ajoutée dans la couche modifiable ; elle n’est pas protégée par le seul montage documentaire `/srv` |

**Décision :** arrêter temporairement File Browser pour copier une base
cohérente, conserver `/.filebrowser.json` et sauvegarder les documents. Ne pas
supprimer le conteneur initial. Préparer ensuite un montage persistant de la
base avec le chemin explicitement choisi pour la nouvelle image ; vérifier
les options de cette image avant la bascule. Aucun arrêt, copie, changement
d’image ou montage persistant de base n’est encore démontré.

L’historique shell, la base et la configuration bruts restent privés ; leur
contenu ne doit pas être publié dans le dépôt. La présence de `/database.db`
ne prouve pas à elle seule le paramètre de base chargé : vérifier dans la
configuration copiée les champs utiles (`database`, `root`, `address`, `port`)
sans afficher de secret.

### R03 — Sauvegarde préalable réalisée le 2 octobre 2026

**Source : sorties exécutées par Olivier.** Dossier de sauvegarde daté
`20261002-100420`, hors dépôt. Le conteneur a été arrêté avant la copie, puis
redémarré après sauvegarde. Les commandes stop/start retournent `filebrowser` ;
aucun parcours applicatif après cette remise en service n’a encore été fourni.

| Élément | Résultat reçu | Limite |
| --- | --- | --- |
| Base | `/database.db` copiée, fichier de 64 Kio | Restauration et compatibilité avec la nouvelle version à tester |
| Configuration | `/.filebrowser.json` copiée, 117 octets | Sauvegarde privée, paramètres utiles extraits seulement |
| Documents | Archive de `/srv/filebrowser`, **274 octets** | Contenu à inventorier : taille faible ne prouve ni absence de données ni perte ; contrôler les fichiers attendus |
| Protection | Dossier créé avec mode 700 ; trois fichiers root:root et mode 600 | État constaté dans les sorties reçues |
| Intégrité | SHA-256 calculés pour les trois fichiers | Empreintes relevées dans les preuves privées ; ne démontrent pas à elles seules une restauration réussie |
| Paramètres source | `database=/database.db`, `root=/srv`, `address` vide, `port=80` | Chemins source confirmés par la configuration copiée |

**Avancement R03 : sauvegarde préalable réalisée ; mise à jour et montage
persistant de la base non encore appliqués.** Conserver l’ancien conteneur et
la sauvegarde initiale. Tester la migration avec une copie distincte de la
base et des documents afin de ne pas altérer les données de retour arrière.
La configuration devra pointer vers le chemin de base persistant choisi pour
la nouvelle image. Le changement de mot de passe doit être conservé lors de
la migration, puis retesté. R08 reste à appliquer et à vérifier.

### R03 — Archive inventoriée et nouvelle image téléchargée

Retour utilisateur du 2 octobre 2026 : l’archive se liste sans erreur et contient
les dossiers public, interne, partenaires (alpha/beta) et un fichier `test`.
L’inventaire limité de la source trouve `test`, 30 octets ; aucune liste
exhaustive des fichiers profonds ni restauration complète n’est encore prouvée.
La faible taille de l’archive est compatible avec ces éléments.

L’image **filebrowser/filebrowser:v2.63.23** a été téléchargée :

- ImageID : `sha256:b3983274c0375dda1722f8e2b65c30d1b9001435e441f0a34855c2e5f8da462e` ;
- RepoDigest : `filebrowser/filebrowser@sha256:a469ea076d4a1b4b1d86a41d130f2f536cd9da996a2b1fb39c0d7635f9d89b9a` ;
- Entrypoint : `tini -- /init.sh`, Cmd null, utilisateur déclaré `user` ;
- volumes déclarés : `/config`, `/database`, `/srv`.

Ces volumes déclarés ne prouvent pas des montages hôte persistants correctement
choisis. Préparer une copie de test avec droits adaptés au nouvel utilisateur.
**Téléchargement effectué ; migration, restauration testée, bascule et reprise
automatique non encore réalisées.** L’ancien conteneur et les sauvegardes restent
la référence de retour arrière.

### R03 — Test de migration réussi selon le retour utilisateur

Olivier indique **« tout bien passé »** après la procédure de test sur copie
avec l’image 2.63.23. Ce retour confirme le succès déclaré du démarrage et des
contrôles proposés : connexion avec le nouveau mot de passe, refus des
identifiants par défaut en navigation privée, dossiers/fichier test présents,
téléchargement et téléversement fictifs. Les logs détaillés, captures et
chemin exact de la copie de test restent à joindre. Aucun résultat n’a été
observé directement par l’assistant.

**R09 : effet de sécurité et accès fonctionnel confirmés selon le retour
utilisateur ; preuves visuelles à joindre. R03 : test de migration sur copie
réussi selon ce retour ; bascule définitive et rescan Trivy encore à réaliser.**
La base et les documents source restent à recopier à l’arrêt pour la bascule,
si l’ancien service a reçu des écritures depuis la sauvegarde. Ne pas prendre
la copie contenant des fichiers de test pour la dernière version des données.

La bascule prévue conserve l’ancien conteneur arrêté, utilise des répertoires
hôte persistants distincts pour base/configuration/documents et configure
`unless-stopped`. La reprise après redémarrage et la persistance après
recréation restent à démontrer. Un retour à l’ancien conteneur ne reprend pas
automatiquement les écritures faites après la bascule : les maîtriser et
prévoir leur récupération avant tout retour.

### R03 / R08 — Bascule et reprise : succès déclaré

**Retour d’Olivier du 2 octobre 2026 : « tout bien passé »**, après la
procédure de bascule définitive et les vérifications proposées. Le résultat
est attribué à l’utilisateur ; les sorties détaillées et captures ne sont
pas encore jointes.

| Élément | Résultat déclaré / limite de preuve |
| --- | --- |
| Constat traité | C12 (image ancienne), persistance de la base/configuration, C11 (besoin de reprise, sans panne spontanée) |
| Modification réalisée | Bascule vers File Browser 2.63.23, avec montages persistants documents/base/configuration et politique `unless-stopped`, selon le retour utilisateur |
| Commandes / configuration utilisées | Procédure proposée : copies de l’état actuel à l’arrêt, nouveau répertoire `/srv/filebrowser-persistent.XXXXXX`, ancien conteneur renommé `filebrowser-legacy`, image épinglée par digest, Docker activé au démarrage. Chemin exact et sorties à joindre |
| Vérification réalisée | Contrôles de conteneur, montages, politique de reprise et activation Docker proposés, puis parcours applicatif et redémarrage VM ; ensemble déclaré réussi |
| Résultat obtenu | Service mis à niveau et reprise automatique déclarés réussis ; disparition des vulnérabilités non encore démontrée par un nouveau scan |
| Test fonctionnel | Connexion avec le nouveau secret, refus des identifiants par défaut, opérations fictives et conservation des comptes/fichier après redémarrage déclarés réussis |
| Problème rencontré | Aucun problème signalé dans ce retour |
| Démarche de diagnostic | Aucune nouvelle investigation rapportée |
| Solution / décision finale | Conserver ancien conteneur et sauvegardes ; relever le chemin persistant exact et effectuer Trivy sur l’image déployée |
| Retour arrière | Prévu dans la procédure ; aucun retour arrière exécuté n’est déclaré |

**Statut : R03 appliquée et fonctionnement déclaré validé ; validation de
réduction des vulnérabilités encore à faire. R08 appliquée et reprise déclarée
validée.** Le succès après redémarrage est distinct d’un test de persistance
après une nouvelle recréation : ce dernier n’a pas été explicitement rapporté.
Les montages rendent les données indépendantes de la couche modifiable,
mais leur preuve technique reste à joindre.

La dernière release du projet archivé ne rétablit pas une maintenance future.
Conserver ce risque résiduel et qualifier les résultats du nouveau scan avant
de clôturer C12. À ce stade historique, Ubuntu restait à migrer ; les captures R01 en début
de feuille documentent maintenant la migration de l’hôte.

### R03 — Nouveau scan Trivy examiné le 2 octobre 2026

Les fichiers `trivy-filebrowser-v2.63.23.txt` et `.json` du dossier privé ont
été lus. Le JSON identifie l’image déployée par
`sha256:b3983274c0375dda1722f8e2b65c30d1b9001435e441f0a34855c2e5f8da462e`.

| Niveau | Avant : relevé historique HIGH/CRITICAL de la 2.15.0 | Après : export 2.63.23 examiné |
| --- | --- | --- |
| HIGH | 143 | 10 |
| CRITICAL | 13 | 0 |
| Total des associations affichées | 156 | 10 |

**Baisse de compteur observée : 146 associations, soit environ 93,6 %.**
Il s’agit d’une comparaison au relevé historique documenté, pas d’un nombre
de CVE exploitables définitivement corrigées. Les commandes/options et dates
des bases du nouveau scan restent à conserver pour apprécier la comparabilité.
Le nouveau JSON contient une cible `bin/filebrowser` de type `gobinary` ;
aucun objet OS n’y est renseigné. Cette absence n’est pas une preuve
d’absence de vulnérabilité système.

**Limite de conservation :** au contrôle actuel, le JSON nommé
`trivy-filebrowser-v2.15.0.json` contient lui aussi l’ImageID de la 2.63.23
et 10 HIGH. Son nom ne permet donc plus de l’utiliser comme export initial
de la 2.15.0. Une substitution ou un écrasement est possible, sans que sa
cause soit établie. Retrouver une copie initiale ou rescanner l’ancienne image
encore conservée avec les mêmes bases/options sous un nouveau nom distinct.
Ne pas attribuer au fichier actuel les anciennes empreintes.

### Risques résiduels détectés — Applicabilité à qualifier

| Composant / version détectée | Résultats dans le rapport | Correction indiquée par le rapport |
| --- | --- | --- |
| `golang.org/x/crypto` v0.54.0 | CVE-2026-56854 | 0.55.0 |
| `golang.org/x/image` v0.44.0 | CVE-2026-46603 | 0.45.0 |
| Go stdlib v1.26.5 | CVE-2026-33818, CVE-2026-39821, CVE-2026-46600, CVE-2026-56853, CVE-2026-56858, CVE-2026-56859, CVE-2026-56860, CVE-2026-56862 | Versions corrigées indiquées par ligne, notamment 1.26.6 ; références à vérifier avant choix |

Les dix résultats sont classés HIGH par Trivy. Le statut `fixed` signifie
qu’une version corrigée est indiquée dans les données du scanner, **pas que
le composant installé est déjà corrigé**. L’applicabilité des dix scénarios
à File Browser reste à analyser ; aucune exploitation n’est démontrée.
Une mise à jour Ubuntu ne remplace pas ces dépendances compilées dans le
binaire de l’image. Le projet File Browser étant archivé, documenter la
stratégie de traitement et la maintenance future.

**R03 : réduction importante du compteur HIGH/CRITICAL documentée et image
mise à niveau ; risque résiduel ouvert.** La migration ne clôture pas tous
les risques de C12 et ne dispense pas des preuves fonctionnelles/captures.

### Complément historique reçu — SSH contextualisé et processus du nouveau conteneur

Retour utilisateur communiqué le 2 octobre 2026, sans date d’exécution propre
ni version OS/paquet dans ces sorties. Il ne fournit pas les résultats APT
de préparation ni la preuve de migration Ubuntu.

- La configuration principale inclut `/etc/ssh/sshd_config.d/*.conf` (ligne 24).
  Aucun contenu de fragment n’apparaît dans la recherche fournie ; aucun Match
  actif dans les fichiers inclus n’est établi par cette seule sortie.
- `ssh.socket` est **enabled** : activation au démarrage configurée, sans
  preuve d’état actif du socket. Examiner socket et service pour la configuration
  d’écoute et les rechargements lors du durcissement.
- `sshd -T -C` utilise le contexte du compte oliv et les variables de la session
  SSH courante. Dans cette sortie, mot de passe, transferts TCP/agent, X11 et
  les deux MAC umac-64 restent autorisés ; root est `prohibit-password`,
  MaxAuthTries vaut 6 et LogLevel INFO. Les restrictions R02 restent à réaliser.
- `docker top` montre `tini -- /init.sh` et `filebrowser
  --config=/config/settings.json`, affichés avec l’utilisateur hôte **oliv**.
  C’est compatible avec un UID non nul résolu par le système hôte ; contrôler
  l’UID numérique et le processus applicatif pour conclure sur le durcissement
  actuel. Ne pas attribuer ces processus au compte administrateur de l’application.

L’état initial ancien avec File Browser PID 1 UID 0 demeure une preuve
historique. Après changement d’image, PID 1 est tini ; l’évaluation actuelle
de R04 doit donc inclure le processus File Browser, pas seulement `/proc/1/status`.
Les options SSH diffèrent du relevé initial : relever OS et version OpenSSH
avant de choisir une prochaine étape de migration, sans déduire Ubuntu 26.04
des seuls algorithmes présents.
