# Reprendre les constats du J1

**Durée prévue : 45 min.**

## Objectif

Reprendre l'inventaire initial, les rapports Greenbone et les cinq constats du
J1 afin de préparer les vérifications locales nécessaires. Cette activité
complète la vue du scanner sans modifier la configuration de la VM cible.

**Statut : contrôles locaux partiellement réalisés le 1er octobre 2026.** Les
versions, les services, les écoutes, OpenSSH, le compte `gvm-audit` et CUPS ont
été relevés. L'état Ubuntu Pro, l'usage de BuildKit, les permissions des sockets
Docker/containerd et les usages avancés de containerd restent à vérifier.

## Point de départ

Les éléments établis pendant le J1 sont conservés dans le
[premier audit Greenbone](../it-1/premier-audit-greenbone.md) :

| Constat | État établi au J1 | Informations encore nécessaires |
| --- | --- | --- |
| G01 — USN-8472-1, containerd | Mise à jour manquante confirmée par le scan SSH authentifié | Révision exacte du paquet, état du service, interfaces locales et fonctions de containerd réellement utilisées |
| G02 — USN-8230-1, Docker/BuildKit | Version Docker antérieure à la révision corrigée Focal | Activation et usage de BuildKit, accès au socket Docker, comptes privilégiés et provenance des contextes de construction |
| G03 — USN-8804-1, OpenSSH | Mise à jour manquante et TCP 22 accessible | Configuration effective : GSSAPI, transferts, tunnels, méthodes d'authentification, comptes et restrictions conditionnelles |
| G04 — USN-7897-1, CUPS | Paquet vulnérable détecté localement | Version exacte, service actif ou déclenché par socket, adresse d'écoute, configuration web et besoin métier |
| G05 — MAC SSH faible | Acceptation distante d'au moins un MAC faible confirmée dans A et B | Liste exacte des MAC proposés par le serveur, origine du paramètre et compatibilité des clients autorisés |

Les rapports détaillés sont au format **Anonymous XML**. Ils prouvent la
réussite SSH de `gvm-audit`, mais ne conservent pas toutes les valeurs locales,
notamment le nom exact du MAC faible.

## Résultats locaux observés — 1er octobre 2026

Le relevé a été effectué à **09:38:08 +02:00** sur
`oliv-Standard-PC-Q35-ICH9-2009`, Ubuntu **20.04.6 LTS**, noyau
`5.15.0-139-generic`. Aucun changement de configuration n'est visible dans les
commandes fournies.

### Versions et état des services

| Composant | Version installée et candidate | État observé | Lecture |
| --- | --- | --- | --- |
| containerd | `1.7.24-0ubuntu1~20.04.2` | Service actif et activé ; socket Unix `/run/containerd/containerd.sock` et écoute locale dynamique sur `127.0.0.1` | La révision corrigée `+esm2` citée par l'USN-8472-1 n'est pas installée. L'exposition réseau externe de containerd n'est pas observée. |
| Docker | `26.1.3-0ubuntu1~20.04.1` | Service actif et activé ; socket Unix `/run/docker.sock` | La révision corrigée `+esm2` citée par l'USN-8230-1 n'est pas installée. Les droits du socket et l'usage de BuildKit restent à relever. |
| OpenSSH | `1:8.2p1-4ubuntu0.13` | Service actif et activé ; écoute sur `0.0.0.0:22` et `[::]:22` | La révision corrigée `+esm3` citée par l'USN-8804-1 n'est pas installée et le service est exposé sur toutes les interfaces de la VM. |
| CUPS | `2.3.1-9ubuntu1.9` | Service et socket actifs et activés | La révision corrigée `+esm3` citée par l'USN-7897-1 n'est pas installée, mais le port 631 est limité à la boucle locale. |

Pour les quatre composants, la version candidate du cache APT est identique à
la version installée. Ce constat ne prouve pas que les correctifs ESM sont
inaccessibles : l'état Ubuntu Pro et la date de mise à jour des listes de paquets
n'ont pas été fournis.

### OpenSSH et compte d'audit

`sshd -t` ne renvoie aucune erreur. La configuration effective contient :

- `PasswordAuthentication yes` et `PubkeyAuthentication yes` ;
- `PermitRootLogin without-password` : connexion directe de `root` interdite
  par mot de passe, mais encore possible par clé si une clé autorisée existe ;
- `AllowTcpForwarding yes`, `DisableForwarding no` et `PermitTunnel no` ;
- `GSSAPIAuthentication no`, `MaxAuthTries 6` et `AuthenticationMethods any` ;
- les MAC 64 bits `umac-64-etm@openssh.com` et `umac-64@openssh.com`, qui
  expliquent le constat G05 de Greenbone.

Le fichier principal inclut `/etc/ssh/sshd_config.d/*.conf`, mais la recherche
fournie ne montre aucune redéfinition explicite des paramètres étudiés. Les
valeurs observées proviennent donc de la configuration effective et de ses
valeurs par défaut, sous réserve d'une vérification complète des fichiers inclus.

Le compte `gvm-audit` possède l'UID/GID 1001, le shell `/bin/bash`, aucun groupe
supplémentaire et aucun droit `sudo`. Son répertoire `.ssh` est en mode `700` et
`authorized_keys` en `600`. Une clé RSA de 3072 bits destinée à l'audit est
présente ; son empreinte n'est pas publiée dans cette documentation.

### CUPS

CUPS est actif, activé et déclenchable par `cups.socket` et `cups.path`. Il
écoute uniquement sur `127.0.0.1:631`, `[::1]:631` et le socket Unix
`/run/cups/cups.sock`. La découverte est désactivée avec `Browsing Off`.
L'interface web est activée, les opérations sensibles exigent `@SYSTEM` ou
`@OWNER`, et aucune imprimante n'est configurée.

Le paquet vulnérable est donc réellement actif, mais aucune exposition directe
du port 631 hors de la VM n'est démontrée. L'absence d'imprimante renforce la
question du besoin métier ; elle ne suffit pas à autoriser la suppression du
service sans validation du responsable.

## Règle de travail : observer sans corriger

Pendant cette activité, ne pas utiliser `apt upgrade`, `apt install`,
`apt remove`, `systemctl restart`, `systemctl stop`, `systemctl disable`,
`docker rm`, `docker run`, ni modifier un fichier de configuration. Ne pas lancer
non plus `apt update`, qui actualiserait les listes locales de paquets.

Les commandes avec `sudo` ci-dessous servent uniquement à lire des informations.
Ne pas afficher ni copier une clé privée, un mot de passe ou le contenu brut
d'`authorized_keys`. Les empreintes de clés suffisent pour l'inventaire.

## Étape 1 — Relever un état local commun

Exécuter les commandes suivantes **dans la VM Ubuntu 20.04 cible** :

```bash
date -Is
hostname
cat /etc/os-release
uname -r

dpkg-query -W \
  -f='${binary:Package}\t${Version}\t${db:Status-Abbrev}\n' \
  docker.io containerd openssh-server cups cups-daemon

apt-cache policy docker.io containerd openssh-server cups cups-daemon
```

Le premier bloc rattache la preuve à la bonne VM et à l'heure locale. Le second
donne la version **complète** des paquets, suffixes Ubuntu et ESM compris.
`apt-cache policy` lit le cache existant : sa version candidate n'est pertinente
que si les listes locales sont à jour, ce qui doit être daté séparément.

Vérifier ensuite l'état des services sans les recharger :

```bash
systemctl is-active docker containerd ssh cups cups.socket
systemctl is-enabled docker containerd ssh cups cups.socket
systemctl show docker containerd ssh cups cups.socket \
  -p Id -p ActiveState -p SubState -p UnitFileState \
  -p FragmentPath -p DropInPaths --no-pager
sudo ss -lntup
sudo ss -lxnp
```

Une unité inactive peut être déclenchée par un socket. Il faut donc lire ensemble
l'état de `cups.service`, de `cups.socket` et l'écoute sur le port 631.

Si l'outil Ubuntu Pro est présent, relever seulement son état :

```bash
if command -v pro >/dev/null 2>&1; then
  sudo pro status
else
  echo "Commande pro absente"
fi
```

Ce contrôle permet d'établir si les correctifs Focal annoncés via ESM sont
accessibles à la VM ; il n'active aucun abonnement.

## Étape 2 — Examiner containerd et Docker/BuildKit

Toujours **dans la VM cible**, relever les versions, les unités, les sockets et
les droits d'accès :

```bash
sudo docker version
sudo docker info
sudo containerd --version
sudo systemctl cat docker containerd
sudo stat -c '%U:%G %a %n' /var/run/docker.sock /run/containerd/containerd.sock
getent group docker
ps -eo user,pid,ppid,args | grep -E '[d]ockerd|[c]ontainerd'
```

Rechercher ensuite la disponibilité et l'usage visible de BuildKit :

```bash
sudo docker buildx version 2>&1
sudo docker buildx ls 2>&1
sudo docker system info --format 'Driver={{.Driver}} SecurityOptions={{json .SecurityOptions}}'
sudo grep -RInE 'buildkit|features|hosts|tls' \
  /etc/docker/daemon.json /etc/docker/daemon.d 2>/dev/null
```

L'absence de `buildx` ne démontre pas à elle seule l'absence de BuildKit. Noter
aussi, auprès du responsable, si cette VM construit des images, importe des
checkpoints ou exécute uniquement l'image historique déjà récupérée.

Pour rattacher le contrôle au conteneur du cas fil rouge sans afficher tout son
environnement :

```bash
sudo docker ps --filter name='^/filebrowser$' \
  --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
sudo docker inspect filebrowser \
  --format 'Image={{.Image}} User={{.Config.User}} Privileged={{.HostConfig.Privileged}} ReadonlyRootfs={{.HostConfig.ReadonlyRootfs}}'
sudo docker inspect filebrowser \
  --format '{{range .Mounts}}{{println .Source "->" .Destination}}{{end}}'
```

Greenbone a inventorié les paquets de l'hôte. Il n'a pas démontré les composants
présents dans l'image File Browser ni les pratiques de construction d'images.

## Étape 3 — Examiner OpenSSH et le compte d'audit

Vérifier d'abord la syntaxe, puis afficher la configuration effective du serveur :

```bash
sudo sshd -t
sudo sshd -T | grep -E \
  '^(macs|permitrootlogin|passwordauthentication|pubkeyauthentication|gssapiauthentication|disableforwarding|allowtcpforwarding|permittunnel|maxauthtries|authenticationmethods) '

sudo grep -RInE \
  '^[[:space:]]*(Include|Match|MACs|PermitRootLogin|PasswordAuthentication|PubkeyAuthentication|GSSAPIAuthentication|DisableForwarding|AllowTcpForwarding|PermitTunnel|MaxAuthTries|AuthenticationMethods)[[:space:]]' \
  /etc/ssh/sshd_config /etc/ssh/sshd_config.d 2>/dev/null
```

`sshd -T` indique les valeurs effectives générales. Les blocs `Match` peuvent
appliquer des valeurs différentes selon le compte, l'adresse ou l'hôte ; leur
présence doit être relevée avant de conclure.

Contrôler le compte utilisé par Greenbone sans afficher les clés :

```bash
getent passwd gvm-audit
id gvm-audit
sudo -l -U gvm-audit
sudo stat -c '%U:%G %a %n' \
  /home/gvm-audit /home/gvm-audit/.ssh \
  /home/gvm-audit/.ssh/authorized_keys
sudo -u gvm-audit ssh-keygen -lf \
  /home/gvm-audit/.ssh/authorized_keys
```

Noter le shell, les groupes, les éventuels droits `sudo`, les permissions et
le nombre d'empreintes. Ne pas copier le contenu d'`authorized_keys` dans la
documentation.

## Étape 4 — Examiner CUPS

Déterminer si CUPS est seulement installé, réellement actif, déclenchable et
accessible au-delà de la boucle locale :

```bash
systemctl status cups cups.socket --no-pager
systemctl is-active cups cups.socket
systemctl is-enabled cups cups.socket
sudo ss -lntup | grep -E '(:631[[:space:]]|:631$)'

sudo grep -RInE \
  '^[[:space:]]*(Listen|Port|Browsing|BrowseLocalProtocols|WebInterface|DefaultAuthType|Allow|Deny|Require)[[:space:]]' \
  /etc/cups/cupsd.conf /etc/cups/cups-files.conf 2>/dev/null

lpstat -r -v -p 2>&1
```

Une écoute sur `127.0.0.1:631` n'est pas une exposition Internet. Elle reste à
évaluer avec l'utilité du service, les comptes autorisés, l'interface web et les
imprimantes configurées. Demander au responsable du service si l'impression a
un rôle attendu sur ce serveur d'échange de documents.

## Étape 5 — Compléter les cinq constats

Reporter uniquement les résultats effectivement observés :

| Constat | Version / état local | Configuration ou condition vérifiée | Protection déjà présente | Ce que Greenbone ne pouvait pas établir | Statut après contrôle |
| --- | --- | --- | --- | --- | --- |
| G01 — containerd | `1.7.24-0ubuntu1~20.04.2`, actif et activé | Sockets locaux observés ; usages de checkpoint/import non établis | Pas d'écoute sur une interface externe observée ; droits des sockets à relever | Fonctions réellement utilisées et scénario exploitable | **Confirmé** pour le correctif manquant ; exploitabilité **à vérifier** |
| G02 — Docker/BuildKit | `26.1.3-0ubuntu1~20.04.1`, actif et activé | Socket Unix présent ; disponibilité et usage de BuildKit non fournis | Pas d'écoute TCP Docker observée ; groupes et permissions à relever | Processus métier de construction et confiance accordée aux entrées | **Confirmé** pour le correctif manquant ; BuildKit **à vérifier** |
| G03 — OpenSSH | `1:8.2p1-4ubuntu0.13`, actif sur IPv4 et IPv6 | Mot de passe et clés autorisés ; GSSAPI désactivé ; transfert TCP autorisé ; tunnel désactivé | `gvm-audit` sans sudo ni groupe privilégié ; `.ssh` en 700 et clés en 600 | Besoin d'exposition, filtrage amont et usages légitimes du transfert | **Confirmé** ; plusieurs conditions et priorités restent **à vérifier** |
| G04 — CUPS | `2.3.1-9ubuntu1.9`, service/socket actifs et activés | Boucle locale, interface web active, découverte désactivée, aucune imprimante | Écoute limitée à `127.0.0.1`, `[::1]` et socket Unix ; opérations sensibles restreintes | Utilité métier et accès possible depuis des processus locaux | **Confirmé** pour le paquet ; priorité réduite par l'absence d'exposition réseau directe |
| G05 — MAC SSH | OpenSSH 8.2p1 ; MAC effectifs relevés | `umac-64-etm@openssh.com` et `umac-64@openssh.com` sont proposés | Algorithmes modernes également disponibles ; compatibilité des clients inconnue | Le rapport anonymisé ne donnait pas les noms exacts | **Confirmé** |

Le statut d'un avis de sécurité peut rester **Confirmé** tandis que certaines
conditions d'exploitation restent **À vérifier**. Ne classer un constat
**Non pertinent** que si une preuve démontre que sa condition ne peut pas se
présenter dans l'environnement étudié.

## Informations hors de portée directe du scanner

Même avec une authentification SSH réussie, Greenbone ne fournit pas à lui seul :

- le besoin métier et le propriétaire de Docker, CUPS ou SSH ;
- l'usage réel de BuildKit, des transferts SSH ou des fonctions de checkpoint ;
- la confiance accordée aux fichiers, dépôts, images et partenaires externes ;
- toutes les configurations conditionnelles et les procédures d'exploitation ;
- la compatibilité d'une correction avec File Browser et les usages des partenaires ;
- l'état interne complet de l'image de conteneur si elle n'est pas analysée comme artefact ;
- la présence d'un retour arrière testé, d'une sauvegarde exploitable ou d'une
  surveillance capable de détecter les scénarios étudiés.

Ces informations nécessitent une observation locale, l'analyse de l'artefact et
des échanges avec les responsables. L'absence d'information ne devient pas une
preuve d'absence.

## État final attendu

Les contrôles fournis remplissent une partie de l'objectif. Pour clôturer
l'activité, chaque constat doit posséder :

- une version locale complète et datée ;
- au moins une condition de configuration ou d'exploitation contrôlée ;
- les protections existantes identifiées ;
- une limite explicite de Greenbone ;
- un statut justifié et les questions restant ouvertes.

Aucune correction n'est appliquée. Les sorties utiles sont conservées sans
secret afin de préparer le choix des mesures de durcissement et le journal des
changements de l'itération 2.

## Preuves à conserver

- date, nom de la VM, OS, noyau et versions complètes des cinq paquets ;
- états `systemd`, écoutes réseau et sockets locaux pertinents ;
- extraits filtrés des configurations Docker, SSH et CUPS ;
- identité, groupes et permissions du compte `gvm-audit`, sans contenu de clé ;
- tableau des cinq constats complété et questions adressées aux responsables.

- [Activité précédente — Premier audit Greenbone](../it-1/premier-audit-greenbone.md)
- [Retour à l'itération 2](index.md)
- [Pense-bête de l'itération](../../pense-bete/glossaire/securisation-avancee-infrastructures/it-2.md)
- [Dossier de preuves](../dossier-preuves.md)
