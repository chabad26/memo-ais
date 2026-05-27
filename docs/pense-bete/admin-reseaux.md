# Pense-bête Administration des réseaux

## À installer avant les TP

### GNS3

GNS3 sert à construire des topologies réseau et à faire tourner des images Cisco pour s'entraîner dans un environnement proche du réel.

```bash
sudo add-apt-repository ppa:gns3/ppa
sudo apt update
sudo apt install gns3-gui gns3-server
sudo usermod -aG ubridge,libvirt,kvm,wireshark $USER
```

Après installation, se déconnecter puis se reconnecter.

```bash
gns3 --version
groups $USER
```

À retenir :

- `ubridge`, `libvirt`, `kvm` et `wireshark` doivent apparaître dans les groupes.
- Au premier lancement, choisir **Run the topologies on my local computer**.
- Si l'état est **Connected**, GNS3 est prêt.

### Wireshark

Wireshark sert à capturer et lire le trafic réseau.

```bash
sudo apt install wireshark tshark
sudo usermod -aG wireshark $USER
```

```bash
wireshark
wireshark capture.pcapng
tshark -i eth0 -w capture.pcapng
```

### Outils réseau utiles

```bash
sudo apt install net-tools ipcalc nmap traceroute mtr dnsutils bind9-utils
```

```bash
sudo apt install screen minicom
screen /dev/ttyUSB0 9600
```

Quitter `screen` : `Ctrl+A`, puis `K`.

## Modèle TCP/IP

| Couche | Rôle | Exemples |
| --- | --- | --- |
| Application | Services utilisés par les applications | HTTP, HTTPS, DNS, DHCP, SSH |
| Transport | Communication entre applications | TCP, UDP |
| Internet | Adressage logique et routage | IP, ICMP, ARP |
| Accès réseau | Transmission locale | Ethernet, Wi-Fi, VLAN |

Phrase utile : chaque couche rend un service à la couche du dessus et s'appuie sur celle du dessous.

## Adressage IPv4

Une adresse IPv4 contient 32 bits, écrits sous forme de 4 octets décimaux.

```text
192.168.10.25/24
```

Dans cet exemple, `/24` signifie : 24 bits pour le réseau et 8 bits pour les hôtes.

### Table CIDR rapide

| Préfixe | Masque | Hôtes utilisables |
| --- | --- | --- |
| `/24` | `255.255.255.0` | 254 |
| `/25` | `255.255.255.128` | 126 |
| `/26` | `255.255.255.192` | 62 |
| `/27` | `255.255.255.224` | 30 |
| `/28` | `255.255.255.240` | 14 |
| `/29` | `255.255.255.248` | 6 |
| `/30` | `255.255.255.252` | 2 |

Formule :

```text
Hôtes utilisables = 2^(32 - préfixe) - 2
```

### Adresses spéciales

Pour `192.168.10.0/24` :

| Adresse | Rôle |
| --- | --- |
| `192.168.10.0` | Adresse réseau |
| `192.168.10.1` | Passerelle fréquente |
| `192.168.10.254` | Dernière adresse hôte |
| `192.168.10.255` | Broadcast |

Ne pas assigner l'adresse réseau ni l'adresse de broadcast à une machine.

### Plages privées

| Plage | Préfixe |
| --- | --- |
| `10.0.0.0` | `/8` |
| `172.16.0.0` à `172.31.255.255` | `/12` |
| `192.168.0.0` | `/16` |

### Méthode subnetting

Pour 50 hôtes :

```text
50 + 2 = 52 adresses nécessaires
Puissance de 2 supérieure : 64
64 = 2^6, donc 6 bits hôtes
32 - 6 = /26
```

Résultat : `192.168.10.0/26`, masque `255.255.255.192`, hôtes `.1` à `.62`, broadcast `.63`.

```bash
ipcalc 192.168.10.0/26
```

## Protocoles essentiels

| Protocole | Rôle | À retenir |
| --- | --- | --- |
| IP | Transporte les paquets entre réseaux | Pas de garantie de livraison |
| TCP | Transport fiable | Connexion, ordre, ACK, retransmission |
| UDP | Transport rapide et léger | Pas de connexion ni garantie |
| ARP | Associe IP et MAC sur le LAN | Fonctionne en broadcast |
| ICMP | Diagnostic et erreurs IP | `ping`, `traceroute` |
| DNS | Traduit nom de domaine en IP | `dig`, `nslookup` |
| DHCP | Distribue une configuration IP | Client sans IP au départ |

## TCP ou UDP ?

| Besoin | Choix courant | Exemples |
| --- | --- | --- |
| Fiabilité | TCP | HTTP(S), SSH, SMTP, FTP |
| Faible latence | UDP | DNS, DHCP, VoIP, streaming |

TCP garantit l'ordre et la livraison. UDP privilégie la simplicité et la rapidité.

## Ports à connaître

| Port | Service | Transport |
| --- | --- | --- |
| 22 | SSH | TCP |
| 25 | SMTP | TCP |
| 53 | DNS | UDP/TCP |
| 67/68 | DHCP | UDP |
| 80 | HTTP | TCP |
| 443 | HTTPS | TCP |
| 161/162 | SNMP | UDP |

```bash
ss -tulnp
```

## Commandes réseau rapides

| Commande | Usage |
| --- | --- |
| `ip addr show` | Voir les interfaces et IP |
| `ip link show` | Voir l'état des interfaces |
| `ip route show` | Voir la table de routage |
| `ip neigh show` | Voir le cache ARP |
| `ping -c 4 8.8.8.8` | Tester la connectivité IP |
| `traceroute 8.8.8.8` | Voir le chemin réseau |
| `mtr --report 8.8.8.8` | Diagnostic de route continu |
| `dig google.com A` | Tester le DNS |
| `ipcalc 192.168.10.0/26` | Vérifier un sous-réseau |

!!! tip "Diagnostic rapide"
    Si `ping 8.8.8.8` fonctionne mais pas `ping google.com`, la connectivité IP est probablement OK et le problème vient plutôt du DNS.

## Filtres Wireshark utiles

| Filtre | Affiche |
| --- | --- |
| `icmp` | Pings |
| `tcp` | Trafic TCP |
| `udp` | Trafic UDP |
| `dns` | Requêtes DNS |
| `arp` | Résolution IP/MAC |
| `bootp` | DHCP |
| `ospf` | Routage OSPF |
| `ip.addr == 192.168.10.1` | Trafic lié à une IP |

## Exercices Wireshark : réponses types

### ARP

À chercher avec le filtre `arp` :

- ARP Request : destination Ethernet `ff:ff:ff:ff:ff:ff`, donc broadcast.
- IP recherchée dans l'exemple : `192.168.1.1`.
- ARP Reply : `192.168.1.1` répond avec la MAC `1c:57:3e:6c:2b:df`.
- Demandeur : `192.168.1.195`, MAC `ce:5a:3a:58:08:5b`.

### ICMP

À chercher avec le filtre `icmp` :

- Echo Request : type `8`.
- Echo Reply : type `0`.
- Exemple local : `192.168.1.195 -> 192.168.1.1`, TTL `64`.
- Réponse locale : `192.168.1.1 -> 192.168.1.195`, TTL `64`.
- Vers Internet, les réponses de `8.8.8.8` reviennent avec un TTL différent, par exemple `114`, car elles ont traversé des routeurs.

### TCP handshake

À chercher avec le filtre `tcp.flags.syn == 1` :

```text
SYN      client -> serveur
SYN-ACK  serveur -> client
ACK      client -> serveur
```

Exemple observé :

- client : `192.168.1.195:50377`
- serveur : `34.223.124.45:80`
- SYN client : `Seq=0`
- SYN-ACK serveur : `Seq=0`, `Ack=1`

À retenir : le SYN consomme un numéro de séquence, donc `ACK = ISN client + 1`.

### DNS

À chercher avec le filtre `dns` :

- transport observé : UDP ;
- port DNS : `53` ;
- nom demandé : `claude.ai` ;
- type : `AAAA` ;
- réponse : `2607:6bc0::10`.

## Encapsulation

```text
Application : données
Transport   : [TCP/UDP][données]
Internet    : [IP][TCP/UDP][données]
Accès réseau: [Ethernet][IP][TCP/UDP][données][FCS]
```

À chaque routeur, l'en-tête Ethernet change. L'adresse IP source et destination reste la référence logique de bout en bout, même si le TTL diminue.

## Schémas réseau L1 / L2 / L3

Un schéma réseau professionnel peut représenter plusieurs niveaux. Il faut savoir les distinguer pour ne pas mélanger câbles, VLAN et routage dans une seule vue confuse.

| Niveau | Ce qu'on représente | Questions auxquelles il répond |
| --- | --- | --- |
| L1 physique | Câbles, ports, baies, équipements, liens physiques | Qui est branché où ? Sur quel port ? |
| L2 liaison | Switchs, VLAN, trunks, accès, adresses MAC | Quels équipements sont dans le même domaine de broadcast ? |
| L3 réseau | Sous-réseaux IP, passerelles, routeurs, interfaces routées | Qui route entre les réseaux ? Quelle passerelle utiliser ? |

### L1 — Physique

À noter sur un schéma L1 :

- nom des équipements ;
- type d'équipement : routeur, switch, serveur, poste ;
- ports utilisés : `Gi0/0`, `Gi0/1`, `Fa0/1`, etc. ;
- type de lien : cuivre, fibre, console, uplink ;
- emplacement si utile : baie, salle, bureau.

Exemple d'information L1 :

```text
PC-ADM-01 eth0 -> SW-ACC-01 Gi0/3
SW-ACC-01 Gi0/24 -> R1 Gi0/0
```

### L2 — Liaison

À noter sur un schéma L2 :

- VLAN ;
- ports access ;
- ports trunk ;
- domaine de broadcast ;
- nom des switchs ;
- éventuellement STP si le réseau est redondant.

Exemple :

```text
VLAN 10 Administration
VLAN 20 Production
VLAN 30 Serveurs
VLAN 40 DMZ
Trunk SW-ACC-01 Gi0/24 <-> R1 Gi0/0
```

À retenir : deux machines dans le même VLAN sont dans le même réseau L2. Deux VLAN différents doivent passer par du routage L3 pour communiquer.

### L3 — Réseau

À noter sur un schéma L3 :

- sous-réseaux IPv4 ;
- passerelles ;
- interfaces de routeur ;
- routes statiques ou dynamiques ;
- services réseau importants : DHCP, DNS, NAT.

Exemple pour AlpesNet :

| Segment | Réseau | Passerelle |
| --- | --- | --- |
| Production | `192.168.10.0/26` | `192.168.10.1` |
| Administration | `192.168.10.64/27` | `192.168.10.65` |
| Serveurs | `192.168.10.96/28` | `192.168.10.97` |
| DMZ | `192.168.10.112/29` | `192.168.10.113` |

### Réflexe de lecture

Quand tu regardes un schéma, demande-toi :

1. L1 : le câble existe-t-il et relie-t-il les bons ports ?
2. L2 : les VLAN et trunks permettent-ils au trafic d'arriver au bon domaine ?
3. L3 : les IP, passerelles et routes permettent-elles de joindre le bon réseau ?

!!! tip "Phrase à garder"
    L1 connecte physiquement, L2 sépare ou regroupe avec les VLAN, L3 permet de passer d'un réseau IP à un autre.

## En-tête des configurations

```text
! ============================================================
! Auteur     : [Prénom NOM]
! Date       : [YYYY-MM-DD]
! Équipement : [Nom - type]
! Module     : RES-01a
! Objet      : [Description en une ligne]
! Version    : 1.0
! ============================================================
```

## Réflexe de diagnostic

1. Vérifier l'interface : `ip link show`.
2. Vérifier l'adresse IP : `ip addr show`.
3. Vérifier la passerelle : `ip route show`.
4. Tester une IP locale.
5. Tester une IP externe.
6. Tester un nom DNS.
7. Observer les paquets avec Wireshark si le doute reste.
