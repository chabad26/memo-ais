# Préparation de l'environnement et installation de Greenbone

## Objectif

Préparer la cible du cas fil rouge et commencer le déploiement de l'outil
d'audit. À la fin de cette activité, File Browser doit être accessible depuis
l'hôte et l'initialisation de Greenbone doit être engagée.

**Statut : cible accessible et Greenbone en cours d'initialisation.** Les sorties
et les sept captures fournies par l'apprenant le **30 septembre 2026** montrent
File Browser 2.15.0 actif dans la VM, son montage et un accès HTTP réussi depuis
l'hôte. Greenbone est démarré sur l'hôte ; son interface est accessible sur le
port local 8443 après correction d'un conflit. Une session ouverte et une
synchronisation des feeds en cours sont visibles. La disponibilité du scanner
reste à vérifier. Les scans viendront ensuite et leur seule cible sera votre propre VM.

Les heures indiquées dans les légendes reprennent les noms des fichiers fournis.

## Contexte et emplacement des actions

En 2021, un service a installé File Browser 2.15.0 dans un conteneur sur un
serveur Ubuntu 20.04 pour échanger des documents avec des partenaires externes.
Le service reste exposé sur Internet en 2026. La maintenance applicative devait
relever du service demandeur, mais les responsabilités et le suivi sont peu
documentés. Vous commencez l'évaluation de cette infrastructure.

| Machine | Configuration et rôle | Actions de cette fiche |
| --- | --- | --- |
| **Hôte** | Machine d'audit | Accéder à la VM et installer Greenbone Community Edition par conteneurs |
| **VM cible** | Ubuntu Server **20.04**, **2 vCPU**, **4 Go de RAM** | Installer Docker et exécuter **File Browser 2.15.0** |

**Ne réalisez aucun scan sur les machines des autres apprenants.** Le serveur
exposé sur Internet est le scénario étudié ; la VM historique reste dans le
réseau du laboratoire, avec accès depuis votre hôte.

## Étape 1 — Préparer la cible

### 1. Vérifier la VM et relever son adresse

**Sur la console de la VM Ubuntu 20.04**, ou dans une session SSH vers elle :

```bash
hostname
cat /etc/os-release
nproc
free -h
ip -br address
ip route
```

Vérifier Ubuntu **20.04**, deux processeurs virtuels et une mémoire proche de
4 Go. Dans virt-manager, confirmer l'allocation dans les paramètres de la VM.
Relever l'adresse de son interface reliée au réseau virtuel ; ne pas utiliser
l'adresse du pont `docker0`, qui apparaîtra après installation de Docker.

#### Résultats observés — contrôle initial

Source : sorties de terminal transmises par l'apprenant.

| Contrôle | Résultat observé |
| --- | --- |
| Système | Ubuntu **20.04.6 LTS**, Focal Fossa |
| Processeurs disponibles, `nproc` | **2** |
| Mémoire visible, `free -h` | **3,8 GiB**, cohérent avec les 4 Go demandés |
| Interface réseau | `enp1s0`, état `UP` |
| Adresse IPv4 de la cible | **`192.168.122.229/24`** |
| Passerelle par défaut | `192.168.122.1` via `enp1s0`, route fournie par DHCP |

Ces sorties établissent la version du système, les ressources visibles et la
configuration réseau locale. Les captures suivantes complètent ce relevé avec
le téléchargement de l'image et l'accès HTTP depuis l'hôte. Relever de nouveau
l'adresse après un changement de bail DHCP.

Le réseau doit permettre l'accès depuis l'hôte et les téléchargements nécessaires
depuis la VM. Le réseau NAT de virt-manager peut convenir : aucune redirection
de port sur la box Internet n'est nécessaire pour l'accès de l'hôte à sa VM.

### 2. Installer Docker dans la VM

**Sur la VM uniquement**, rechercher d'abord une installation existante :

```bash
command -v docker
dpkg -l docker.io docker-ce containerd containerd.io 2>/dev/null
```

Si un moteur fonctionne déjà, conserver cette installation et passer aux
contrôles. Sur une VM neuve, la voie proposée pour Ubuntu 20.04 est le paquet
`docker.io` des dépôts Ubuntu :

```bash
sudo apt update
apt-cache policy docker.io
sudo apt install docker.io curl ca-certificates docker-buildx
sudo systemctl enable --now docker
```

Avant l'installation, vérifier qu'APT propose un candidat pour `docker.io`.
Si aucun candidat n'est disponible, vérifier les dépôts Focal et leur composant
`universe`, puis demander l'aide du formateur au besoin. Ne pas remplacer le
nom de version Ubuntu par celui d'une autre distribution dans les dépôts.

Le [paquet Ubuntu pour Focal](https://launchpad.net/ubuntu/focal/+package/docker.io)
permet de conserver le système imposé. La
[procédure actuelle Docker Engine](https://docs.docker.com/engine/install/ubuntu/)
ne liste plus Ubuntu 20.04 parmi les versions prises en charge ; elle convient
aux hôtes compatibles, mais ne doit pas être appliquée aveuglément à cette cible
historique. Ne pas mélanger `docker.io` et `docker-ce` sur une même installation.

Contrôler ensuite le moteur de la VM :

```bash
sudo systemctl is-active docker
sudo docker version
sudo docker info
```

Résultats attendus : service `active`, informations du client **et du serveur**
Docker, sans erreur d'accès au démon. Les commandes suivantes utilisent `sudo`
pour éviter de devoir modifier les groupes de l'utilisateur.

### 3. Créer les répertoires de documents

**Sur la VM** :

```bash
sudo mkdir -p /srv/filebrowser/public \
  /srv/filebrowser/partenaires/partenaire-alpha \
  /srv/filebrowser/partenaires/partenaire-beta \
  /srv/filebrowser/interne

sudo find /srv/filebrowser -maxdepth 2 -type d | sort
```

Arborescence attendue :

```text
/srv/filebrowser/
├── public/
├── partenaires/
│   ├── partenaire-alpha/
│   └── partenaire-beta/
└── interne/
```

Les fichiers seront ajoutés dans une activité ultérieure. Ne pas créer de
documents de test ni changer récursivement les permissions à ce stade.

### 4. Récupérer et lancer File Browser 2.15.0

**Sur la VM** :

```bash
sudo docker pull filebrowser/filebrowser:v2.15.0
sudo docker image inspect filebrowser/filebrowser:v2.15.0 \
  --format '{{json .RepoDigests}}'
sudo docker ps -a --filter name=^/filebrowser$
```

Conserver le tag et le digest dans les preuves. Si un conteneur `filebrowser`
existe déjà, l'inspecter avant de poursuivre ; ne pas le supprimer pour relancer
la commande. Sinon, exécuter la commande du sujet, avec `sudo` :

```bash
sudo docker run -d \
  --name filebrowser \
  -p 8080:80 \
  -v /srv/filebrowser:/srv \
  filebrowser/filebrowser:v2.15.0
```

| Paramètre | Effet |
| --- | --- |
| `-d` | Exécution en arrière-plan |
| `--name filebrowser` | Nom utilisé pour les contrôles et journaux |
| `-p 8080:80` | Port 8080 de la **VM** vers le port 80 du conteneur |
| `-v /srv/filebrowser:/srv` | Répertoire de la VM présenté comme racine des documents dans le conteneur |
| `v2.15.0` | Version historique imposée, conservée pour l'état initial |

La publication `8080:80` écoute par défaut sur les adresses de la VM. Conserver
la portée du réseau de laboratoire ; une règle UFW seule ne garantit pas le
filtrage des ports publiés par Docker. Voir les
[interactions Docker et pare-feu](https://docs.docker.com/engine/install/ubuntu/#firewall-limitations).

#### Preuve — image récupérée et conteneur créé

![Terminal de la VM : téléchargement de File Browser v2.15.0, digest et création du conteneur](<../../assets/img/securisation-avancee-infrastructures/it-1/Capture d’écran du 2026-09-30 09-39-54.png>)

*Capture de 09:39:54 — Le téléchargement aboutit, l'inspection retrouve le digest
et `docker run -d` retourne un identifiant de conteneur.*

Digest observé pour `filebrowser/filebrowser:v2.15.0` :

```text
sha256:1595cf9b36528113a18178996d9ff9ee8bc7814699bb5f8e1d8ad8ec48aa89ac
```

### 5. Vérifier le conteneur et le montage

**Sur la VM** :

```bash
sudo docker ps -a --filter name=^/filebrowser$
sudo docker logs --tail 50 filebrowser
sudo docker exec filebrowser /filebrowser version
sudo docker inspect filebrowser \
  --format '{{range .Mounts}}{{println .Source "->" .Destination}}{{end}}'
sudo docker exec filebrowser ls -la /srv
curl -sS --connect-timeout 5 -o /dev/null \
  -w 'HTTP %{http_code}\n' http://127.0.0.1:8080/
```

Résultats attendus : conteneur en cours d'exécution, version 2.15.0, montage
`/srv/filebrowser -> /srv`, dossiers `public`, `partenaires` et `interne`,
réponse HTTP permettant d'accéder à l'application, normalement `200` sur `/`.
Lire les journaux en cas d'écart. Ne pas publier de secret éventuellement affiché.

#### Preuve — version, montage et réponse locale

![Contrôles dans la VM : File Browser healthy, version 2.15.0, montage vers srv et HTTP 200](<../../assets/img/securisation-avancee-infrastructures/it-1/Capture d’écran du 2026-09-30 09-43-24.png>)

*Capture de 09:43:24 — Le conteneur est `Up (healthy)`, le binaire annonce
`File Browser v2.15.0/73ccbe91`, le montage est `/srv/filebrowser -> /srv`
et `http://127.0.0.1:8080/` répond **HTTP 200** dans la VM.*

Les dossiers `interne`, `partenaires` et `public` sont visibles dans `/srv`.
Cette liste ne montre pas le contenu de `partenaires` : la présence de
`partenaire-alpha` et `partenaire-beta` ainsi que l'absence de fichiers dans
l'ensemble de l'arborescence restent à documenter.

!!! note "Persistance de la version historique"
    La [configuration du tag v2.15.0](https://github.com/filebrowser/filebrowser/blob/v2.15.0/.docker.json)
    place la base dans `/database.db` et les documents dans `/srv`.
    Avec la commande du sujet, seuls les documents sont montés depuis la VM :
    supprimer le conteneur peut perdre sa base, ses utilisateurs et ses réglages.
    Un arrêt/démarrage du même conteneur conserve sa couche inscriptible.
    Ne pas transposer les chemins `/database` et `/config` des versions récentes
    sans vérifier la version. Ne pas ajouter de durcissement avant de relever
    l'état initial demandé.

### 6. Tester depuis la machine d'audit

**Sur l'hôte**, utiliser l'adresse observée, à actualiser si le bail DHCP change :

```bash
CIBLE_IP="192.168.122.229"
ping -c 3 "$CIBLE_IP"
curl -sS --connect-timeout 5 -o /dev/null \
  -w 'HTTP %{http_code}\n' "http://${CIBLE_IP}:8080/"
```

Dans le **navigateur de l'hôte**, ouvrir `http://192.168.122.229:8080`
si cette adresse est toujours attribuée à la cible.
Conserver une capture de la page accessible, avec la cible et le port visibles,
sans identifiant ni mot de passe. La page de connexion suffit à cette première
vérification d'accessibilité ; les usages et droits seront étudiés ensuite.

`localhost:8080` depuis l'hôte désignerait l'hôte, pas la VM. Un ping refusé
n'empêche pas nécessairement HTTP : le contrôle du port et la page web sont
nécessaires pour conclure.

#### Preuves — accès depuis l'hôte et page de connexion

![Terminal de l'hôte : ping vers 192.168.122.229 sans perte et HTTP 200 sur le port 8080](<../../assets/img/securisation-avancee-infrastructures/it-1/Capture d’écran du 2026-09-30 09-43-50.png>)

*Capture de 09:43:50 — Depuis `ubuntu-oliv`, les trois requêtes ICMP reçoivent
une réponse et l'URL `http://192.168.122.229:8080/` renvoie **HTTP 200**.
L'accès hôte → VM sur le port applicatif est confirmé.*

![Page de connexion File Browser avec champs utilisateur et mot de passe vides](<../../assets/img/securisation-avancee-infrastructures/it-1/Capture d’écran du 2026-09-30 09-39-42.png>)

*Capture de 09:39:42 — La page de connexion File Browser est affichée, sans
secret saisi. L'adresse du navigateur n'est pas visible ; le rattachement à
l'IP et au port de la cible repose sur le contrôle HTTP ci-dessus.
Aucune authentification File Browser n'est démontrée par cette page.*

## Étape 2 — Commencer l'installation de Greenbone

### 1. Vérifier la machine d'audit

**Toutes les commandes de cette étape s'exécutent sur l'hôte.**

```bash
hostname
cat /etc/os-release
docker --version
docker compose version
docker info
free -h
df -h "$HOME" /var/lib/docker
```

#### Résultats observés — hôte d'audit

Source : sorties de terminal transmises par l'apprenant depuis son hôte.

| Contrôle | Résultat observé |
| --- | --- |
| Système hôte | Ubuntu **26.04.1 LTS**, Resolute Raccoon |
| Docker client et serveur | **29.1.3** ; `docker info` accède au serveur sans erreur |
| Plugin Compose | **v5.5.1**, reconnu par `docker compose version` et `docker info` |
| Processeurs logiques vus par Docker | **20** |
| Mémoire | Environ **30 GiB** au total, **19 GiB disponibles** au moment du contrôle |
| Stockage | **80 Go disponibles**, occupation de **83 %** |
| Conteneurs dans le contexte Docker `default` | **0** au moment du contrôle |

Les deux lignes de `df` désignent le même système de fichiers pour le dossier
personnel et `/var/lib/docker` : les 80 Go disponibles ne s'additionnent pas.
Ce relevé décrit l'état avant le déploiement Greenbone. Le démarrage et la
correction du conflit de port sont documentés plus bas.

Si Docker et Compose sont déjà opérationnels, les conserver. Sinon, suivre la
[documentation Docker adaptée à l'hôte](https://docs.docker.com/engine/install/),
avec le plugin Compose. Sur Ubuntu, installer aussi `curl` et `ca-certificates`
s'ils manquent. En cas de refus d'accès au démon, utiliser `sudo docker` de façon
cohérente pour cette étape ; ne pas changer les permissions du socket Docker.

!!! tip "Erreur `unknown shorthand flag: 'p' in -p`"
    L'option `-p ais-greenbone` nomme le projet Compose et est valide. Cette
    erreur peut apparaître lorsque Docker ne reconnaît pas le sous-programme
    `compose`. Vérifier d'abord `hostname` : le terminal doit être celui de
    l'hôte, pas celui de la VM Ubuntu 20.04. Tester ensuite `docker compose version`
    dans ce même terminal. Si ce contrôle échoue aussi sur l'hôte, identifier
    l'installation avec `type -a docker` et `docker --version`, puis suivre
    l'[installation officielle du plugin Compose](https://docs.docker.com/compose/install/linux/)
    adaptée au système et au dépôt utilisés. Ne reprendre les commandes Greenbone
    qu'une fois la version Compose affichée correctement.

Le guide Greenbone indique un minimum de **2 cœurs, 4 Go de RAM et 20 Go de
stockage**, avec **4 cœurs, 8 Go et 60 Go recommandés**. Ces ressources concernent
Greenbone, en plus de la VM cible et des besoins de l'hôte.
[Source : prérequis Greenbone](https://greenbone.github.io/docs/latest/22.4/container/index.html#hardware-requirements).

### 2. Récupérer la définition officielle des conteneurs

**Sur l'hôte, pour un premier déploiement**, dans un dossier distinct des autres
laboratoires et du dépôt du mémo :

```bash
GB_DIR="$HOME/lab-securisation-avancee/greenbone"
mkdir -p "$GB_DIR"
cd "$GB_DIR"

if [ -e compose.yaml ]; then
  printf 'compose.yaml existe déjà : le conserver et le vérifier.\n'
else
  curl -fL https://greenbone.github.io/docs/latest/_static/compose.yaml \
    -o compose.yaml
fi

docker compose -p ais-greenbone config --quiet
docker compose -p ais-greenbone config --services
sha256sum compose.yaml
```

Le fichier doit être téléchargé sans erreur et sa validation doit réussir.
Conserver date, empreinte et liste des services. Le nom de projet `ais-greenbone`
isole les ressources de ce TP ; le garder dans les commandes suivantes.
Procédure de référence :
[Greenbone Community Containers](https://greenbone.github.io/docs/latest/22.4/container/index.html).

#### Trace de préparation — validation effectuée dans la VM

![Terminal de la VM : fichier Compose existant, validation, liste des services et empreinte](<../../assets/img/securisation-avancee-infrastructures/it-1/Capture d’écran du 2026-09-30 09-49-40.png>)

*Capture de 09:49:40 — `config --quiet` revient sans erreur visible,
`config --services` affiche les services et `sha256sum` fournit une empreinte.*

L'invite `oliv-Standard-PC-Q35-ICH9-2009` correspond ici à la **VM cible**.
Cette capture conserve une étape de préparation sur cette machine ; elle ne
prouve pas un déploiement Greenbone sur l'hôte. L'empreinte concerne le fichier
présent dans ce terminal, avant la correction du port. Le déploiement sur
`ubuntu-oliv` est attesté par la capture des conteneurs plus bas.

### 3. Télécharger puis démarrer

**Sur l'hôte, dans le même dossier** :

```bash
docker compose -p ais-greenbone pull
docker compose -p ais-greenbone up -d
docker compose -p ais-greenbone ps -a
docker compose -p ais-greenbone logs --tail 100
```

Pour suivre l'initialisation :

```bash
docker compose -p ais-greenbone logs -f --tail 50 gvmd ospd-openvas
```

`Ctrl+C` quitte le suivi des journaux sans arrêter les conteneurs. Après
réouverture d'un terminal, revenir dans
`$HOME/lab-securisation-avancee/greenbone` avant de reprendre les commandes.
Ne pas utiliser `--remove-orphans` ni supprimer les volumes pour résoudre une
initialisation lente.

### 4. Distinguer démarrage et disponibilité pour l'audit

| État | Vérification | Conclusion possible |
| --- | --- | --- |
| Images récupérées | `pull` terminé sans erreur | Téléchargement terminé |
| Services démarrés | `ps -a` et journaux sans erreur bloquante | Déploiement lancé |
| Données en cours de chargement | Activité d'import dans les journaux | Initialisation à laisser progresser |
| Feeds et objets disponibles | État des feeds, scanner et profils de scan dans l'interface | Préparation d'un audit possible |

Le chargement initial peut durer de plusieurs minutes à plusieurs heures. Le
téléchargement des images et l'import des données sont deux opérations distinctes.
Des données incomplètes faussent les scans : conserver l'état « initialisation en
cours » tant que leur disponibilité n'est pas vérifiée.
[Source : chargement des feeds](https://greenbone.github.io/docs/latest/22.4/container/workflows.html#loading-the-feed-changes).

L'initialisation peut continuer pendant les exercices suivants, conformément
au sujet. Cette activité ne demande pas encore un rapport de scan.

### 5. Ouvrir l'interface lorsqu'elle est disponible

Le fichier officiel consulté le **30 septembre 2026** publie l'interface via
`nginx` sur `127.0.0.1:443`. Ce port étant déjà occupé dans le laboratoire,
la publication locale a été déplacée sur **8443**, comme détaillé ci-dessous.
Dans le navigateur **de l'hôte**, ouvrir **`https://127.0.0.1:8443`** et vérifier
le certificat local auto-signé présenté. Cette adresse correspond à la
configuration corrigée du laboratoire ; vérifier les ports avant une nouvelle installation.
[Source : fichier Compose officiel](https://greenbone.github.io/docs/latest/_static/compose.yaml).

Utiliser les indications du guide officiel pour la première connexion et
remplacer le mot de passe initial du compte Greenbone depuis l'interface dès
que possible. Le conserver dans le gestionnaire de mots de passe, pas dans les
captures ou le mémo. Ce compte appartient à l'outil d'audit sur l'hôte.

#### Preuve — session ouverte et feeds en cours de synchronisation

![Tableau de bord OPENVAS avec session admin ouverte et message de synchronisation des feeds](<../../assets/img/securisation-avancee-infrastructures/it-1/Capture d’écran du 2026-09-30 10-04-59.png>)

*Capture de 10:04:59 — Le tableau de bord affiche une session `admin`,
la version d'interface **28.5.0** et le message « Feed is currently syncing. ».
L'interface indique que les scans sont indisponibles pendant cette phase.*

Cette capture confirme l'accès à une session authentifiée. Les compteurs de
tâches et de tests affichent zéro à cet instant ; aucun rapport de scan n'est
présenté. Le changement du mot de passe initial et la fin de l'import des feeds
ne sont pas démontrés par cet écran.

### Incident rencontré — port 443 déjà occupé

Le démarrage a échoué pour `ais-greenbone-nginx-1` avec :

```text
failed to bind host port 127.0.0.1:443/tcp: address already in use
```

Le contrôle a retrouvé une écoute sur le port 443, Nginx à l'état `Created`
et les autres composants principaux démarrés. Le port local 8443 était disponible.

**Correction appliquée par l'assistant dans le laboratoire :** sauvegarde de
`~/lab-securisation-avancee/greenbone/compose.yaml` dans un fichier
`compose.yaml.before-port-8443-*.bak`, puis remplacement de la seule publication
`127.0.0.1:443:443` par `127.0.0.1:8443:443` dans le service `nginx` :

```yaml
ports:
  - 127.0.0.1:8443:443
  - 127.0.0.1:9392:9392
```

Le port du conteneur reste 443 et l'écoute reste limitée à la boucle locale.
Cette notation suit le format de [publication des ports Docker Compose](https://docs.docker.com/reference/compose-file/services/#ports).
Le service qui occupait le port 443 a été conservé.

Après validation du fichier, seul Nginx a été recréé, ses dépendances étant
déjà démarrées :

```bash
cd "$HOME/lab-securisation-avancee/greenbone" &&
docker compose -p ais-greenbone config --quiet &&
docker compose -p ais-greenbone up -d --no-deps nginx
```

| Vérification effectuée | Résultat observé |
| --- | --- |
| Validation Compose | Réussie |
| Conteneur Nginx | `Up` |
| Publication HTTPS | `127.0.0.1:8443 -> 443/tcp` |
| Requête locale sur `https://127.0.0.1:8443/` | **HTTP 200**, page HTML titrée `OPENVAS` |

Le contrôle HTTP a toléré le certificat auto-signé uniquement pour cette URL
locale. Il confirme l'accès à la page, pas la confiance TLS, l'authentification,
la fin du chargement des feeds ou la capacité à réaliser un scan.

![Conteneurs du projet ais-greenbone sur l'hôte ubuntu-oliv avec Nginx publié sur 8443](<../../assets/img/securisation-avancee-infrastructures/it-1/Capture d’écran du 2026-09-30 10-06-09.png>)

*Capture de 10:06:09 — `docker compose -p ais-greenbone ps -a` est exécuté
sur **`ubuntu-oliv`**. Nginx est `Up`, avec `127.0.0.1:8443 -> 443/tcp` ;
`gvmd`, `pg-gvm` et plusieurs services de données sont `healthy`.
`gsad`, `ospd-openvas`, `openvas` et `openvasd` sont également démarrés.*

Les conteneurs affichés `Exited (0)` ont terminé avec un code de sortie nul.
Ce relevé complète la preuve du démarrage, sans établir à lui seul que les feeds
sont entièrement importés ni que le scanner est prêt.

Utiliser directement l'adresse HTTPS avec **8443** ; l'ancien point d'entrée
9392 ne constitue pas la vérification de cette nouvelle publication.
Le retour au port 443 demanderait de libérer ce port, de rétablir la ligne
sauvegardée puis de recréer Nginx ; il n'a pas été réalisé.

## En cas de difficulté

| Symptôme | Contrôle ciblé | Suite à donner |
| --- | --- | --- |
| Docker inaccessible sur la VM | `sudo systemctl status docker --no-pager` et `sudo journalctl -u docker -n 50 --no-pager` | Identifier l'erreur du moteur avant File Browser |
| Nom `filebrowser` déjà utilisé | `sudo docker ps -a --filter name=^/filebrowser$` | Inspecter ; si c'est le bon conteneur arrêté, utiliser `sudo docker start filebrowser` |
| Port 8080 occupé | `sudo ss -ltnp` et `sudo docker ps` sur la VM | Identifier le service ; ne pas arrêter une application inconnue |
| HTTP local fonctionne, accès hôte impossible | IP de la VM, réseau virtuel, routes, publication Docker et filtrage | Corriger le chemin hôte → VM sans élargir la cible aux autres machines |
| `pull` échoue | Nom d'image, DNS, accès au registre et espace disque | Conserver l'erreur exacte et reprendre après correction |
| `unknown shorthand flag: 'p' in -p` | `hostname`, `docker compose version`, `type -a docker` | Revenir sur l'hôte si la commande a été lancée dans la VM ; sinon vérifier le plugin Compose |
| Greenbone ne démarre pas | `docker compose -p ais-greenbone ps -a` puis `logs --tail 100` | Identifier le service en échec et consulter sa documentation |
| Port 443 ou 9392 occupé sur l'hôte | `sudo ss -ltnp` et `docker ps` | Préserver les services existants ; dans ce laboratoire, le conflit sur 443 a été corrigé avec `127.0.0.1:8443:443` |
| Interface vide ou profils absents | Journaux `gvmd`/`ospd-openvas` et état des feeds | Distinguer un import en cours d'une erreur persistante |

Dans cet ordre : **identifier l'étape en échec, lire les erreurs et journaux,
vérifier la documentation, puis demander l'aide du formateur si nécessaire**.
Consulter aussi le [dépannage officiel Greenbone](https://greenbone.github.io/docs/latest/22.4/container/troubleshooting.html).
Joindre la commande, la machine concernée et l'erreur nettoyée des secrets.

## État final attendu et preuves à conserver

| Contrôle | Preuve attendue | Résultat réel |
| --- | --- | --- |
| VM Ubuntu 20.04, 2 vCPU, 4 Go | OS et ressources visibles | **Observé** : Ubuntu 20.04.6, `nproc` = 2, mémoire visible 3,8 GiB |
| Configuration réseau locale | Interface, adresse et route | **Observé** : `enp1s0` UP, `192.168.122.229/24`, passerelle `192.168.122.1` ; accès depuis l'hôte confirmé |
| Docker sur la cible | Fonctionnement du moteur et versions client/serveur | **Observé** : téléchargement, création, inspection et exécution réussis ; le [relevé d'observation](observer-cible.md) confirme ensuite Docker **26.1.3** côté client et serveur de la VM |
| Arborescence demandée | Liste des répertoires sans fichiers ajoutés | **Partiellement observé** : `interne`, `partenaires`, `public` visibles ; sous-dossiers des partenaires et absence de fichiers à vérifier |
| File Browser 2.15.0 | Tag, digest, version et état du conteneur | **Observé** : tag et digest conservés, binaire `v2.15.0/73ccbe91`, conteneur `Up (healthy)` |
| Montage des documents | `/srv/filebrowser` → `/srv` | **Observé** par `docker inspect` |
| Accès depuis l'hôte | Réponse HTTP et page sur l'IP de la VM, port 8080 | **Observé** : ping 3/3 et HTTP 200 sur `192.168.122.229:8080` ; page de connexion fournie sans barre d'adresse |
| Docker et Compose sur l'hôte | Versions et accès au moteur | **Observé** : Docker client/serveur 29.1.3, Compose v5.5.1, `docker info` réussi |
| Ressources de l'hôte | CPU, mémoire et espace disponible | **Observé** : 20 processeurs logiques, 19 GiB de RAM disponibles et 80 Go de disque libre au moment du contrôle |
| Greenbone sur l'hôte | Compose validé, conteneurs démarrés et interface accessible | **Observé** : Compose valide, services démarrés sur `ubuntu-oliv`, HTTP 200 sur `https://127.0.0.1:8443/` après correction du conflit sur 443 ; session ouverte dans l'interface |
| Initialisation Greenbone | État des feeds dans l'interface et journaux | **En cours sur la capture** : synchronisation signalée, scans indisponibles ; disponibilité finale à contrôler |

Conserver ces pièces dans le [dossier de preuves](../dossier-preuves.md).
Une interface accessible ne constitue pas encore un audit de la cible.

## Ressources

- [Documentation officielle Greenbone Community Containers](https://greenbone.github.io/docs/latest/22.4/container/index.html).
- [Documentation File Browser fournie dans le sujet](https://github.com/filebrowser/filebrowser/blob/master/docs/installation.md) : documentation actuelle, à distinguer du tag historique.
- [Dockerfile File Browser v2.15.0](https://github.com/filebrowser/filebrowser/blob/v2.15.0/Dockerfile) et [configuration de cette version](https://github.com/filebrowser/filebrowser/blob/v2.15.0/.docker.json).
- [Tutoriel complémentaire fourni par le formateur](https://www.fosslinux.com/7320/how-to-install-and-configure-openvas-9-on-ubuntu.htm) : utiliser la procédure officielle par conteneurs pour les commandes de ce TP.

- [Retour à l'itération 1](index.md)
- [Activité suivante — Vulnérabilité ou autre problème ?](vulnerabilite-ou-autre-probleme.md)
- [Pense-bête de l'itération](../../pense-bete/glossaire/securisation-avancee-infrastructures/it-1.md)
- [Retour au module](../README.md)
