# Observer la cible

**Durée prévue : 30 minutes.**

## Objectif

Établir un premier état de la VM avant de consulter les résultats de Greenbone :
adresse IP, système, ports accessibles, services, versions, conteneurs et rôles
attendus. Réutiliser les commandes Linux et réseau déjà travaillées.

**Statut : observation locale et accès distants TCP 22/8080 documentés.**
Le relevé de l'apprenant du **30 septembre 2026**, repéré à **11:51:09 +02:00**,
confirme le système, le réseau, les écoutes, les services et Docker dans la VM.
La session sur l'hôte, repérée à **11:53:01 +02:00**, confirme l'accès TCP aux
ports 22 et 8080 ainsi qu'une réponse HTTP 200. La version OpenSSH et le besoin
des services supplémentaires restent à préciser.

## Périmètre et méthode

| Point d'observation | Machine | Ce qu'on cherche |
| --- | --- | --- |
| Dans la cible | VM Ubuntu 20.04, précédemment `192.168.122.229` | Configuration locale, processus, services et conteneurs |
| Depuis l'extérieur de la VM | Hôte d'audit `ubuntu-oliv` | Accessibilité effective de la cible depuis le réseau du laboratoire |

L'exposition depuis l'hôte ne prouve pas une exposition depuis Internet.
Ne tester que **sa propre VM**, après avoir confirmé son adresse actuelle.
Conserver l'état initial : les commandes ci-dessous observent et interrogent
les services, sans mise à jour ni changement de configuration.

## 1. Identifier la VM et son système

**Dans le terminal de la VM**, par sa console ou une session SSH déjà disponible :

```bash
date -Is
hostname
cat /etc/os-release
uname -r
ip -br address
ip route
```

Noter l'heure avec son décalage de fuseau, le nom de machine, la version Ubuntu,
la version du noyau, l'interface active, son adresse et la passerelle.
La version du noyau donnée par `uname -r` ne remplace pas celle de la distribution.

Le relevé précédent indiquait `192.168.122.229/24` sur `enp1s0`. Vérifier le bail
DHCP avant de réutiliser cette IP ; ne pas prendre l'adresse de `docker0` pour
l'adresse de la VM à joindre depuis l'hôte.

## 2. Relever les écoutes et les services locaux

**Sur la VM** :

```bash
sudo ss -lntup
systemctl list-units --type=service --state=running --no-pager
```

Dans `ss`, `-l` sélectionne les sockets en écoute, `-n` garde les adresses et
ports numériques, `-t` et `-u` couvrent TCP et UDP, et `-p` affiche les processus
quand les permissions le permettent. Pour chaque ligne pertinente, noter
**protocole, adresse locale, port et processus**.

| Adresse locale observée | Interprétation |
| --- | --- |
| `127.0.0.1` ou `::1` | Écoute sur la boucle locale de la machine |
| `0.0.0.0` | Écoute sur toutes les adresses IPv4 locales |
| `[::]` | Écoute IPv6 ; vérifier séparément la prise en charge d'IPv4 |
| Adresse précise de la VM | Écoute liée à cette adresse |

Un service `running` n'écoute pas nécessairement sur le réseau. Une écoute
locale ne démontre pas non plus qu'un autre système peut l'atteindre : il faut
ensuite vérifier le chemin depuis l'hôte.

Pour préciser le rôle d'une unité identifiée, utiliser `systemctl status` avec
son nom. Par exemple, **si SSH apparaît dans le relevé**, examiner :

```bash
systemctl status ssh --no-pager
dpkg-query -W openssh-server
```

L'absence d'unité ou de paquet est un résultat à noter, pas une raison de
l'installer. Le port 22 seul ne suffit pas à identifier SSH : recouper avec le
processus et le paquet. Relever la version complète du paquet, suffixe Ubuntu compris.

## 3. Observer Docker et File Browser

**Sur la VM**, pour ne pas mélanger ses conteneurs avec ceux de Greenbone sur l'hôte :

```bash
sudo docker version
sudo docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
sudo docker port filebrowser
sudo docker exec filebrowser /filebrowser version
sudo docker inspect filebrowser \
  --format '{{range .Mounts}}{{println .Source "->" .Destination}}{{end}}'
```

Noter les versions du client et du serveur Docker, tous les conteneurs en cours
d'exécution, leurs images, leurs états et leurs ports publiés. Si `filebrowser`
n'apparaît pas, utiliser `sudo docker ps -a` pour rechercher un conteneur arrêté
et consigner son état avant de décider d'une action.

Dans la préparation, **`8080:80`** signifie : **port TCP 8080 de la VM vers
port TCP 80 du conteneur**. Cela ne démontre pas que le port 80 de la VM est
accessible. Docker peut assurer la publication par des règles réseau ; croiser
`ss`, `docker port` et le test distant plutôt que conclure à partir de `ss` seul.
[Source : publication des ports Docker](https://docs.docker.com/engine/network/port-publishing/).

Le tag d'image est une première indication de version. La commande exécutant
`/filebrowser version` vérifie le binaire présent. Pour tout service dont la
version reste inconnue, écrire **« version non identifiée »**, sans la déduire
du numéro de port.

## 4. Vérifier l'accès depuis la machine d'audit

**Sur l'hôte `ubuntu-oliv`**, après confirmation de l'IP actuelle de la VM :

```bash
date -Is
hostname
CIBLE_IP="192.168.122.229"
ip route get "$CIBLE_IP"
ping -c 3 "$CIBLE_IP"
curl -sS --connect-timeout 5 --max-time 10 -o /dev/null \
  -w 'HTTP %{http_code}\n' "http://${CIBLE_IP}:8080/"
```

Ouvrir aussi `http://192.168.122.229:8080` dans le navigateur de l'hôte si l'IP
est inchangée. Une capture avec l'adresse visible complète le test HTTP.

Pour les ports TCP relevés sur la VM, réutiliser **`nc`**, déjà employé dans les
[ateliers réseau](../../admin-reseaux-securisation/it-1/atelier3.md) :

```bash
command -v nc
nc -vz -w 3 "$CIBLE_IP" 8080
```

**Si une écoute SSH sur 22 a été observée**, compléter par :

```bash
nc -vz -w 3 "$CIBLE_IP" 22
```

Répéter ce contrôle sur les autres ports TCP effectivement relevés, en remplaçant
le numéro. Si `nc` n'est pas disponible, conserver les contrôles réalisables
avec les commandes présentes et noter la couverture manquante ; aucun nouvel
outil n'est nécessaire pour chaque information.

| Résultat | Conclusion à noter |
| --- | --- |
| Ping réussi | La cible répond à ICMP depuis l'hôte ; cela ne prouve pas l'accès applicatif |
| Ping sans réponse | Résultat à investiguer ; tester aussi le service car ICMP peut être filtré |
| Connexion TCP réussie avec `nc` | Port accessible depuis ce point d'observation, sans preuve du bon fonctionnement applicatif |
| `Connection refused` | Connexion refusée ; absence d'écoute ou rejet à distinguer avec le relevé local |
| Délai dépassé | Pas de réponse dans le délai ; ne suffit pas à conclure que le port est fermé |
| HTTP 200 | Une réponse HTTP réussie est reçue ; ne prouve ni authentification ni sécurité du service |

Ce contrôle est ciblé sur les ports inventoriés : ce n'est pas un relevé exhaustif
des 65 535 ports TCP. Les sockets UDP vus avec `ss` restent des observations
locales tant qu'aucun échange avec leur protocole n'a été vérifié depuis l'hôte.

## 5. Associer chaque service à un rôle attendu

| Service ou composant | Rôle attendu dans ce laboratoire | Justification à relever |
| --- | --- | --- |
| File Browser | Échange de documents avec les partenaires dans le cas fil rouge | Binaire, conteneur, montage des documents et accès HTTP sur 8080 |
| SSH, si présent | Administration distante de la VM | Processus, unité, version et besoin d'administration ; sa présence ne justifie pas toute exposition |
| Docker | Exécution du conteneur applicatif | Moteur et conteneurs observés ; ne pas supposer une API Docker exposée sur TCP |
| Autre service observé | À déterminer | Identifier son responsable, son usage et pourquoi il écoute sur cette interface |

Les ports locaux **8443 et 9392 de Greenbone appartiennent à l'hôte d'audit**,
pas à l'inventaire des services de la VM cible. Un service dont le rôle n'est
pas identifié reste **à investiguer**, avant toute conclusion sur son utilité.

## Résultats observés — relevé du 30 septembre 2026

Sources : terminal copié par l'apprenant et fichier joint `Texte collé.txt`
contenant `ss` et `systemctl`. Le repère horaire est celui de `date -Is` au début
de la session ; il n'est pas une heure d'exécution individuelle pour chaque commande.
L'invite identifie la **VM**, même si le répertoire courant s'appelle `greenbone`.

### Identité, réseau et versions

| Information | Commande ou preuve | Résultat observé |
| --- | --- | --- |
| Machine | `hostname` | `oliv-Standard-PC-Q35-ICH9-2009` |
| Système | `cat /etc/os-release` | Ubuntu **20.04.6 LTS**, Focal Fossa |
| Noyau | `uname -r` | **`5.15.0-139-generic`** |
| Interface principale | `ip -br address` | `enp1s0` UP, **`192.168.122.229/24`**, IPv6 locale au lien `fe80::108c:dd85:55bb:70ba/64` |
| Route par défaut | `ip route` | Via **`192.168.122.1`** sur `enp1s0`, fournie par DHCP |
| Réseau Docker | `ip -br address`, `ip route` | `docker0` UP, **`172.17.0.1/16`**, route `172.17.0.0/16` ; interface `veth51bc43a@if4` active |
| Docker client et serveur | `sudo docker version` | **26.1.3**, API **1.45**, build `26.1.3-0ubuntu1~20.04.1`, `linux/amd64` |
| Composants du moteur | `sudo docker version` | containerd **1.7.24**, runc **1.1.12-0ubuntu2~20.04.1**, docker-init **0.19.0** |
| Conteneurs en fonctionnement | `sudo docker ps --format ...` | Une ligne : **`filebrowser`**, image `filebrowser/filebrowser:v2.15.0`, **`Up 2 hours (healthy)`** |
| Version applicative | `sudo docker exec filebrowser /filebrowser version` | **`File Browser v2.15.0/73ccbe91`** |
| Publication | `sudo docker port filebrowser` | `80/tcp → 0.0.0.0:8080` et `80/tcp → [::]:8080` |
| Montage | `sudo docker inspect filebrowser --format ...` | **`/srv/filebrowser → /srv`** |

Les versions ci-dessus appartiennent à la VM : Docker **29.1.3** relevé plus tôt
appartient à l'hôte d'audit. `docker ps` inventorie les conteneurs en fonctionnement
dans le contexte interrogé, sans établir l'absence de conteneurs arrêtés.

### Écoutes locales et rôles

Le relevé `sudo ss -lntup` montre les éléments suivants. Les adresses génériques
indiquent une liaison à toutes les adresses de la famille concernée ; elles ne
prouvent pas le franchissement des filtres réseau depuis l'hôte ou Internet.

| Protocole et port | Adresse locale | Processus | Rôle / qualification |
| --- | --- | --- | --- |
| TCP **22** | `0.0.0.0`, `[::]` | `sshd` | Administration SSH ; `ssh.service` actif, accès TCP IPv4 depuis l'hôte confirmé ci-dessous ; version à relever |
| TCP **8080** | `0.0.0.0`, `[::]` | `docker-proxy` | Publication de File Browser, confirmée par `docker port` |
| TCP et UDP **53** | `127.0.0.53%lo` | `systemd-resolve` | Résolution DNS locale, recoupée avec `systemd-resolved.service` |
| TCP **631** | `127.0.0.1`, `[::1]` | `cupsd` | Service d'impression CUPS en boucle locale ; besoin à justifier pour ce serveur |
| TCP **37517** | `127.0.0.1` | `containerd` | Socket local du moteur d'exécution ; fonction exacte de cette écoute à préciser |
| UDP **5353** | `0.0.0.0`, `[::]` | `avahi-daemon` | Découverte mDNS/DNS-SD ; utilité pour le cas fil rouge à justifier |
| UDP **36609** / **35745** | `0.0.0.0` / `[::]` | `avahi-daemon` | Autres sockets Avahi observés ; ne pas supposer ces numéros fixes lors d'un prochain relevé |

### Services en fonctionnement et points à investiguer

`systemctl list-units --type=service --state=running --no-pager` retourne
**34 unités**. Parmi elles : `ssh`, `docker`, `containerd`, `systemd-resolved`,
`avahi-daemon`, `cups`, `cups-browsed`, `gdm`, `NetworkManager`, `rsyslog`,
`systemd-journald`, `systemd-timesyncd` et `unattended-upgrades`.

La présence de **`gdm.service` (GNOME Display Manager)** et de services comme
`colord` et `spice-vdagentd` montre des composants liés à un environnement de
bureau et à son intégration dans la VM. Cela ne permet pas d'identifier avec
certitude l'image Ubuntu utilisée à l'installation. Le besoin de ces composants,
de l'impression et de la découverte réseau est à vérifier au regard de la
consigne **Ubuntu Server** et du rôle d'échange de documents.

Ces observations ne démontrent pas une vulnérabilité logicielle et ne justifient
pas une suppression immédiate. De même, une unité `unattended-upgrades` active
ne prouve pas que tous les correctifs sont installés.

### Accessibilité distante — session de 11:53:01 +02:00

Source : sorties transmises par l'apprenant depuis **`ubuntu-oliv`**.
`date -Is` indique `2026-09-30T11:53:01+02:00` au début du bloc ; les commandes
suivantes ne sont pas horodatées individuellement.

| Commande sur l'hôte | Résultat observé | Conclusion |
| --- | --- | --- |
| `hostname` | `ubuntu-oliv` | Point d'observation : hôte d'audit |
| `ip route get "$CIBLE_IP"` | `192.168.122.229 dev virbr0 src 192.168.122.1` | Chemin vers la VM via `virbr0`, adresse source `192.168.122.1` |
| `ping -c 3 "$CIBLE_IP"` | 3 paquets transmis, 3 reçus, **0 % de perte** ; RTT moyen **0,268 ms** | Réponse ICMP de la cible |
| `curl` vers `http://192.168.122.229:8080/` | **HTTP 200** | Accès HTTP confirmé à nouveau depuis l'hôte |
| `command -v nc` | `/usr/bin/nc` | Commande disponible sur l'hôte |
| `nc -vz -w 3 "$CIBLE_IP" 8080` | `Connection to 192.168.122.229 8080 port [tcp/http-alt] succeeded!` | Connexion TCP au port **8080** réussie |
| `nc -vz -w 3 "$CIBLE_IP" 22` | `Connection to 192.168.122.229 22 port [tcp/ssh] succeeded!` | Connexion TCP au port **22** réussie |

Le service sur 22 est identifié comme SSH en recoupant ce test avec `sshd` et
`ssh.service` sur la VM. Les libellés `ssh` et `http-alt` affichés par `nc` ne
constituent pas à eux seuls une identification du logiciel ou de sa version.
Le test TCP n'établit pas une authentification SSH réussie.

**Bilan :** depuis `192.168.122.1`, la cible `192.168.122.229` répond sur les
ports TCP **22 et 8080**, et File Browser fournit une réponse HTTP réussie.
Ce relevé ne prouve pas une exposition Internet, une accessibilité IPv6 ou UDP,
ni l'absence d'autres ports accessibles.

### Contrôles restants

**Sur la VM**, relever encore la version du serveur SSH :

```bash
dpkg-query -W openssh-server
```

Les rôles des services supplémentaires, les autres versions utiles et
l'accessibilité UDP restent à documenter. Aucun réglage d'authentification SSH
(notamment la connexion directe de `root`) n'est établi par ces sorties.

Pour les contrôles complémentaires, ajouter une ligne par service, y compris si le test échoue :

| Date / heure | Machine d'exécution | Commande | Résultat pertinent | Service, version et rôle | Conclusion / limite |
| --- | --- | --- | --- | --- | --- |
| 2026-09-30T11:58:07+02:00 | VM | `dpkg-query -W openssh-server` | Sortie `openssh-server 1:8.2p1-4ubuntu0.13` | Identifié | Accessible |

## Résultat attendu et preuves à conserver

Un état initial daté qui relie **IP → port/protocole → service → version → rôle**,
avec les commandes réellement utilisées et les limites du relevé. Conserver les
sorties et captures pertinentes, sans secrets ; ne pas remplir un résultat
attendu comme s'il avait été observé.

Cet inventaire permettra ensuite de comparer ce que Greenbone détecte avec ce
qui fonctionne réellement sur la cible, sans qualifier une vulnérabilité sur
le seul âge d'une version ou le seul numéro d'un port.

- [Activité précédente — Comprendre CVSS](comprendre-cvss.md)
- [Retour à l'itération 1](index.md)
- [Pense-bête de l'itération](../../pense-bete/glossaire/securisation-avancee-infrastructures/it-1.md)
- [Retour au module](../README.md)
