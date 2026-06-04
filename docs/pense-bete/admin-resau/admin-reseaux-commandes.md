# Commandes et diagnostic

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
| `ss -tulnp` | Voir les ports en écoute |
| `nc -zv 192.168.10.5 443` | Tester l'ouverture d'un port TCP |
| `curl -v http://192.168.10.5` | Tester un service HTTP |
| `openssl s_client -connect 192.168.10.5:443` | Tester TLS/HTTPS |

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
| `eth.dst == ff:ff:ff:ff:ff:ff` | Broadcast Ethernet |
| `ip.dst == 224.0.0.251` | mDNS IPv4 |
| `udp.port == 5353` | mDNS |

À observer avec `ospf` :

- paquets `Hello` vers `224.0.0.5` ;
- échanges réguliers entre voisins ;
- changement de trafic lors d'une panne ou d'une reconvergence.

## Lire des fichiers pcapng

| Commande | Usage |
| --- | --- |
| `capinfos capture.pcapng` | Métadonnées : durée, nombre de paquets, interface |
| `tcpdump -nn -r capture.pcapng -c 50` | Lire les 50 premiers paquets |
| `tcpdump -nn -r capture.pcapng arp` | Lire uniquement ARP |
| `tcpdump -nn -r capture.pcapng icmp` | Lire uniquement ICMP |
| `tcpdump -nn -r capture.pcapng port 67 or port 68` | Lire DHCP |
| `tcpdump -nn -r capture.pcapng udp port 5353` | Lire mDNS |

À retenir :

- `-r` lit un fichier de capture ;
- `-nn` garde les IP et ports numériques ;
- `-c` limite le nombre de paquets affichés.

## Commandes Cisco OSPF

| Commande | Usage |
| --- | --- |
| `router ospf 1` | Entrer dans la configuration OSPF. |
| `router-id 1.1.1.1` | Définir l'identifiant OSPF du routeur. |
| `network 192.168.10.0 0.0.0.255 area 0` | Annoncer un LAN `/24` dans l'area 0. |
| `network 10.0.1.0 0.0.0.3 area 0` | Annoncer un lien WAN `/30` dans l'area 0. |
| `show ip ospf neighbor` | Voir les voisins OSPF. Attendu : `Full`. |
| `show ip route ospf` | Voir les routes apprises par OSPF. |
| `show ip ospf interface brief` | Voir les interfaces actives dans OSPF. |
| `show ip ospf database` | Voir la base LSDB. |
| `show ip protocols` | Vérifier les protocoles de routage actifs. |

Authentification MD5 sur un lien OSPF :

```bash
R1(config)# interface GigabitEthernet0/1
R1(config-if)# ip ospf message-digest-key 1 md5 MonMotDePasse
R1(config-if)# ip ospf authentication message-digest
```

À faire des deux côtés du lien avec la même clé, sinon l'adjacence tombe.

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

## Diagnostic réseau — réflexe

1. Vérifier l'interface : `ip link show`.
2. Vérifier l'adresse IP : `ip addr show`.
3. Vérifier la passerelle : `ip route show`.
4. Tester une IP locale.
5. Tester une IP externe.
6. Tester un nom DNS.
7. Observer les paquets avec Wireshark si le doute reste.

## Diagnostic OSI rapide

| Couche | Test rapide |
| --- | --- |
| L1 | `ip link show` : interface UP ? |
| L2 | `ip neigh show` ou filtre Wireshark `arp` |
| L3 | `ip addr`, `ip route`, `ping` |
| L4 | `ss -tulnp`, `nc -zv ip port` |
| L7 | `curl -v`, `dig`, logs applicatifs |

Méthode : formuler une hypothèse avant chaque test, puis s'arrêter à la première couche qui échoue.

## Bash — automatisation rapide

Tester plusieurs hôtes :

```bash
for ip in 192.168.10.1 192.168.10.2 192.168.10.3; do
    ping -c 1 "$ip" && echo "$ip OK" || echo "$ip KO"
done
```

Lire un fichier `hosts.txt` :

```bash
while IFS= read -r line; do
    [[ -z "$line" || "$line" == \#* ]] && continue
    ping -c 1 "$line" && echo "$line OK" || echo "$line KO"
done < hosts.txt
```

Options pro :

- `set -euo pipefail` : mode strict ;
- `"$variable"` : toujours protéger les variables ;
- `tee -a fichier.log` : afficher et journaliser.

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
