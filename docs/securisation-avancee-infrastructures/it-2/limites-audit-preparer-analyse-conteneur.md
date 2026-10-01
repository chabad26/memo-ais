# Identifier les limites de l’audit et préparer l’analyse du conteneur

**Durée indicative : 1 h**

## Objectif

Déterminer ce que Greenbone, Lynis et les vérifications manuelles permettent
réellement de conclure sur File Browser 2.15.0. Préparer l’identification de
l’image exacte et les informations nécessaires à son analyse au J3.

**Statut au 1er octobre 2026 : analyse des limites et relevé des métadonnées
de l’image réalisés ; contenu et dépendances à analyser au J3.** Les sorties transmises à **11:36:10 +02:00** sont intégrées ci-dessous ;
les commandes restent disponibles pour reproduire le relevé.
Aucune configuration ni politique de redémarrage ne doit être modifiée.

## 1. Répondre aux six questions à partir des preuves

| Question | Réponse étayée | Limite ou complément nécessaire |
| --- | --- | --- |
| Que sait-on avec certitude de la version ? | Le J1 documente une version du binaire **2.15.0**, la référence Docker `filebrowser/filebrowser:v2.15.0` et un HTTP 200 sur le port 8080. Le relevé Docker J2 confirme cette référence pour le conteneur `filebrowser` | Un tag seul ne prouve pas le contenu ni l’identité immuable de l’image. Son ImageID et son RepoDigest sont désormais relevés et reliés au conteneur dans la section 4 |
| Greenbone a-t-il trouvé des vulnérabilités propres à File Browser ? | Dans les résultats exportés analysés au J1, le port 8080 est ouvert mais File Browser n’est pas identifié ; les cinq constats retenus concernent containerd, Docker/BuildKit, OpenSSH, CUPS et les MAC SSH | Aucun constat spécifique à File Browser n’est établi par ces preuves. Cela ne démontre pas que l’application est sans vulnérabilité |
| Lynis analyse-t-il le contenu de cette image ? | L’audit Lynis réalisé porte sur la VM : comptes, SSH, services, noyau et environnement Docker. `CONT-8106` demande de comparer l’inventaire Docker | Aucune analyse des fichiers, paquets ou dépendances de l’image n’est prouvée par cet audit. Une détection de Docker n’équivaut pas à une analyse de l’image |
| Quels composants internes sont connus ? | La version applicative observée est connue ; les métadonnées actuellement fournies montrent un montage dans `/srv` et la configuration du conteneur | Le contrôle interne à 11:49 identifie Alpine 3.13.4 ; paquets, bibliothèques et dépendances embarquées restent non inventoriés. Le Dockerfile de base exact reste à établir |
| Absence de constat signifie-t-elle absence de vulnérabilité connue ? | **Non.** Un résultat dépend de la couverture, des signatures, des droits, des composants identifiés et de la date de l’analyse | Les requêtes PHP/PHPUnit ayant reçu 404 ne prouvent ni la présence ni l’absence exhaustive de ces composants, ni une exploitation réussie |
| Que faut-il pour analyser l’image elle-même ? | ID exact référencé par le conteneur, digests disponibles, plateforme, inventaire du système de fichiers et des dépendances, provenance et Dockerfile correspondant, SBOM si disponible | Prévoir au J3 un scanner d’image et ses bases datées, puis valider l’applicabilité des résultats. Un inventaire de paquets seul peut manquer les dépendances compilées ou embarquées |

Preuves : [premier audit Greenbone](../it-1/premier-audit-greenbone.md),
[analyse Lynis](analyser-prioriser-resultats-lynis.md) et
[vérifications manuelles](verifier-configuration-systeme.md).

## 2. État connu du conteneur

| Élément | État documenté | Portée |
| --- | --- | --- |
| Nom et référence | `filebrowser` ; `filebrowser/filebrowser:v2.15.0` | Confirmés par `docker ps -a` |
| État | Arrêté, code 1 ; `OOMKilled=false` | Arrêt volontaire de la VM déclaré par l’utilisateur, corroboré par l’arrêt propre de Docker/containerd le 30 septembre à 14:42:59 +02:00 ; aucune panne spontanée démontrée |
| Dernière exécution | Début le 30 septembre à 09:39:25 +02:00 ; fin à 14:42:59 +02:00 | Ces dates sont des dates d’exécution, pas de construction de l’image |
| Redémarrage | `RestartPolicy=no`, `RestartCount=0` | Besoin de reprise automatique à définir ultérieurement |
| Configuration | `User=` vide, `Privileged=false`, `ReadonlyRootfs=false` | Ne prouve pas l’identité effective du processus ; un entrypoint peut changer d’utilisateur |
| Montage | `/srv/filebrowser -> /srv`, `RW=true` | Les données de l’hôte montées dans le conteneur ne constituent pas le contenu de l’image |
| Droits des données | Répertoires `root:root 755`, aucun fichier affiché jusqu’à profondeur 3 ; ACL de base sur quatre chemins | Aucun test de confidentialité applicative ni de lecture de document prouvé |
| Ports | J1 : HTTP sur le port hôte 8080 ; log de fermeture du listener interne sur `[::]:80` | Ports déclarés dans l’image et règles de publication à relever. La colonne PORTS vide d’un conteneur arrêté n’établit pas l’absence de configuration |

## 3. Relever les métadonnées dans la VM cible

**Lieu : VM Ubuntu qui héberge File Browser**, et non l’hôte qui héberge
Greenbone. Ces contrôles fonctionnent sur un conteneur arrêté. Ne pas utiliser
`docker pull`, `run`, `start`, `exec`, `commit` ou une reconstruction pendant
cette activité : conserver l’objet analysé et l’état du laboratoire.

Relire les sorties avant publication. Les commandes, labels ou historiques
peuvent contenir des informations internes. Ne pas publier un `inspect` brut
avec l’ensemble des variables d’environnement.

### A. Identifier le conteneur et l’image qu’il référence

```bash
date -Is
hostname
sudo docker ps -a --no-trunc \
  --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'

sudo docker inspect --type container filebrowser --format \
  'ContainerID={{.Id}} Reference={{.Config.Image}} ImageID={{.Image}} ContainerCreated={{.Created}} Status={{.State.Status}}'
```

**Résultat à conserver :** référence textuelle, ID du conteneur, ID complet de
l’image et date de création du conteneur. Cette dernière ne correspond pas à
la création de l’image.

Utiliser l’ID référencé par le conteneur pour les lectures suivantes : si le
tag a été déplacé depuis la création, lire le tag seul pourrait analyser une
autre image.

```bash
FB_IMAGE_ID=$(sudo docker inspect --type container filebrowser --format '{{.Image}}')
sudo docker image inspect "$FB_IMAGE_ID" --format \
  'ImageID={{.Id}} RepoTags={{json .RepoTags}} RepoDigests={{json .RepoDigests}} ImageCreated={{.Created}} OS={{.Os}} Architecture={{.Architecture}} SizeBytes={{.Size}}'
```

**Attendu :** des métadonnées, pas une liste de vulnérabilités. Si l’image locale
est introuvable, conserver le diagnostic sans la télécharger à nouveau.
`RepoDigests` peut être vide : l’ID local reste à conserver, sans inventer de
digest de registre. ID d’image et digest de manifeste désignent des objets
différents ; les libeller séparément.

### B. Examiner la configuration de l’image et celle du conteneur

```bash
sudo docker image inspect "$FB_IMAGE_ID" --format \
  'User={{json .Config.User}} WorkingDir={{json .Config.WorkingDir}} Entrypoint={{json .Config.Entrypoint}} Cmd={{json .Config.Cmd}} ExposedPorts={{json .Config.ExposedPorts}} Volumes={{json .Config.Volumes}}'

sudo docker inspect --type container filebrowser --format \
  'User={{json .Config.User}} WorkingDir={{json .Config.WorkingDir}} Entrypoint={{json .Config.Entrypoint}} Cmd={{json .Config.Cmd}} Privileged={{.HostConfig.Privileged}} ReadonlyRootfs={{.HostConfig.ReadonlyRootfs}} RestartPolicy={{.HostConfig.RestartPolicy.Name}} NetworkMode={{.HostConfig.NetworkMode}}'
```

Comparer les valeurs : des paramètres du conteneur peuvent remplacer ceux de
l’image. Un `User` vide ne permet pas d’identifier l’UID final du processus.
Les chemins de `Volumes` sont des déclarations de l’image, pas la liste des
montages effectivement appliqués.

### C. Examiner les montages et les ports

```bash
sudo docker inspect --type container filebrowser --format \
  '{{range .Mounts}}{{println .Type .Source "->" .Destination "RW=" .RW}}{{end}}'

sudo docker inspect --type container filebrowser --format \
  'DeclaredPorts={{json .Config.ExposedPorts}} PortBindings={{json .HostConfig.PortBindings}} RuntimePorts={{json .NetworkSettings.Ports}}'
```

Distinguer **port déclaré**, **publication configurée sur l’hôte** et **service
réellement accessible**. Ces métadonnées ne prouvent pas un listener actif ;
le conteneur est arrêté. Les adresses de publication éventuelles sont à
anonymiser dans une copie publique.

### D. Relever les informations de construction disponibles

```bash
sudo docker image history --no-trunc "$FB_IMAGE_ID" \
  --format 'table {{.ID}}\t{{.CreatedAt}}\t{{.Size}}'

sudo docker image inspect "$FB_IMAGE_ID" --format \
  'Source={{index .Config.Labels "org.opencontainers.image.source"}} Revision={{index .Config.Labels "org.opencontainers.image.revision"}} VersionLabel={{index .Config.Labels "org.opencontainers.image.version"}} CreatedLabel={{index .Config.Labels "org.opencontainers.image.created"}}'
```

Ces labels peuvent être absents ; leur contenu est déclaratif et non une preuve
de provenance authentifiée. L’historique fournit des indices de création,
pas un inventaire complet des composants ni le Dockerfile original garanti.
Les dates disponibles ne donnent pas nécessairement la date de téléchargement.

Pour approfondir **localement seulement**, l’historique des instructions peut
être consulté avec `sudo docker image history --no-trunc "$FB_IMAGE_ID"`.
Ne pas publier la colonne des instructions sans relecture : elle peut révéler
arguments, chemins ou secrets de construction.

Références des commandes : [Docker inspect](https://docs.docker.com/reference/cli/docker/inspect/),
[image inspect](https://docs.docker.com/reference/cli/docker/image/inspect/) et
[image history](https://docs.docker.com/reference/cli/docker/image/history/).

## 4. Métadonnées relevées pour le J3

Le relevé commence le **1er octobre 2026 à 11:36:10 +02:00**, sur la VM cible.
L’ID renvoyé par le conteneur concorde avec celui de `docker image inspect`.

| Information | Valeur observée | Portée de la preuve |
| --- | --- | --- |
| Nom/tag | `filebrowser/filebrowser:v2.15.0` | Référence du conteneur et RepoTags concordants |
| ImageID | `sha256:a68f43720ea6ff331fa4b92becced20af14b72f4c3a22ca1f764076a8e42e1a5` | Identité locale exacte à utiliser pour le scan J3 |
| RepoDigest | `filebrowser/filebrowser@sha256:1595cf9b36528113a18178996d9ff9ee8bc7814699bb5f8e1d8ad8ec48aa89ac` | Digest de registre disponible, distinct de l’ImageID |
| Création du conteneur | `2026-09-30T07:39:24.875990635Z`, soit 09:39:24 +02:00 | Métadonnée du conteneur, pas de l’image |
| Création de l’image | `2021-04-06T12:09:44.177946785Z`, soit 14:09:44 +02:00 | Date déclarée dans les métadonnées ; ne donne pas la date de téléchargement |
| Plateforme et taille | `linux/amd64`, `42892931` octets | Distribution de base non identifiée par ces champs |
| Configuration image et conteneur | User et WorkingDir vides, Entrypoint `["/filebrowser"]`, Cmd null | Valeurs concordantes ; PID 1 et shell exec observés UID/GID 0 à 11:49 dans l’activité optionnelle |
| Restrictions d’exécution | `Privileged=false`, `ReadonlyRootfs=false`, `RestartPolicy=no`, réseau `bridge` | Configuration observée ; aucun changement effectué |
| Montage | Type `bind`, `/srv/filebrowser -> /srv`, RW true ; image déclarant `/srv` comme volume | Montage réel distingué de la déclaration de volume |
| Ports | Image/conteneur déclarent `80/tcp` ; PortBindings : HostIp vide, HostPort `8080` ; RuntimePorts `{}` | Publication configurée 8080 vers 80/tcp ; aucune accessibilité active prouvée pour ce conteneur arrêté |
| Historique | Entrées datées du 31 mars et du 6 avril 2021 ; plusieurs ID `<missing>` | Informations de construction disponibles ; ces valeurs ne prouvent pas une corruption ni un inventaire de composants |
| Label source | `https://github.com/filebrowser/filebrowser` | Valeur déclarative ; dépôt non inspecté dans cet exercice |
| Label révision | `73ccbe912fc1848957d8b2f6bbe5243804769d85` | Révision déclarée, correspondance avec le contenu non authentifiée |
| Labels version/création | `2.15.0` ; `2021-04-06T12:01:23Z` | Label de création distinct du Created de l’image ; ne pas confondre les deux dates |
| Distribution, paquets, bibliothèques | Alpine Linux **3.13.4** identifié par os-release à 11:49 ; paquets et bibliothèques non inventoriés | Provenance de la base et composants à analyser au J3 |
| Dépendances du binaire | **À analyser au J3** | SBOM, métadonnées de compilation ou scanner adapté |
| Vulnérabilités applicables | **À analyser au J3** | Résultats datés et rapprochement avec les avis éditeur |

L’ancienneté de la date de création justifie d’examiner les composants et leur
maintenance ; elle ne démontre pas à elle seule une vulnérabilité précise.
Aucune distribution ni dépendance ne peut être déduite des seules tailles
des entrées d’historique.

### Démarrage de contrôle et arrêt volontaire

Le relevé `Exited (1) 4 seconds ago` correspond à un **arrêt volontaire** :
l’utilisateur indique avoir démarré le conteneur pour vérifier qu’il démarrait
sans erreur, puis l’avoir arrêté afin de poursuivre l’activité.

**Résultat déclaré par l’utilisateur : démarrage sans erreur constatée.**
Ce témoignage explique le nouvel état arrêté ; aucune panne spontanée n’est
retenue. Il ne constitue pas un test documenté d’accès HTTP, de connexion à
l’application, de permissions des documents ou de reprise automatique après
redémarrage de la VM. Les sorties du démarrage ne sont pas fournies ; le code
1 seul ne remet pas en cause l’explication de l’arrêt volontaire.

C11 est donc expliqué pour les deux observations : arrêt volontaire de la VM
le 30 septembre, puis démarrage de contrôle et arrêt volontaire du conteneur
le 1er octobre. Aucune investigation supplémentaire de la cause de cet arrêt
n’est nécessaire. Le besoin de reprise automatique reste à définir au stade
approprié ; aucune politique n’est modifiée dans cette activité.

## 5. Ajouter les limites à l’analyse d’audit unique

Ce complément prolonge les constats **C10** (isolation des données) et **C11**
(reprise après arrêt volontaire), ainsi que C01/C02 pour le moteur de
conteneurs. Il ne transforme pas les vulnérabilités de la VM en vulnérabilités
de l’image.

| Limite | Conséquence sur la conclusion | Travail restant |
| --- | --- | --- |
| Vue distante GB sans identification applicative dans les exports | Aucun bilan de sécurité de File Browser démontré | Identifier l’application et rapprocher les avis applicables de la version exacte |
| Scan authentifié avec compte non administrateur sur l’hôte | Les contrôles de paquets Ubuntu portent sur l’hôte et les droits du compte | Analyser séparément l’image référencée par le conteneur |
| Audit LY de la VM et inventaire Docker | Pas d’inventaire interne de l’image prouvé | Collecter image, plateforme et contenu, puis scanner au J3 |
| Tag, ImageID et RepoDigest désormais relevés | Objet du scan identifié, contenu encore inconnu | Analyser cet ImageID et conserver la plateforme linux/amd64 |
| Image, couche modifiable et montages différents | Un scan d’image ne suffit pas à évaluer documents montés, comptes applicatifs et configuration d’exécution | Tester séparément les permissions et usages, avec données fictives |
| Bases et couverture des scanners limitées | Zéro résultat ne garantit pas zéro vulnérabilité connue ou inconnue | Conserver versions des outils, date des bases, exclusions, erreurs et composants non identifiés |

## État final attendu et livrables

Les métadonnées sont désormais renseignées. Conserver les sorties datées et
relues, compléter le contenu et les dépendances au J3, puis rattacher
l’ensemble à l’[analyse consolidée](consolider-resultats-greenbone-lynis.md).
Les valeurs non obtenues restent « À relever » ou « Non vérifiable ».

Pour le J3, disposer de l’image exacte à analyser, de ses métadonnées, des
questions ouvertes sur les composants et d’un périmètre distinct pour l’image,
le conteneur et les données montées. Aucun téléchargement, scan d’image,
redémarrage, changement de configuration ou correction n’est présenté comme
réalisé dans cette feuille.

- [Activité précédente — Consolider les résultats Greenbone et Lynis](consolider-resultats-greenbone-lynis.md)
- [Complément — Observer le conteneur sans y exécuter Lynis](etendre-audit-conteneur.md)
- [Retour à l’itération 2](index.md)
- [Dossier de preuves](../dossier-preuves.md)
- [Pense-bête de l’itération](../../pense-bete/glossaire/securisation-avancee-infrastructures/it-2.md)
