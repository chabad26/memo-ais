# Protocoles essentiels

## Protocoles courants

| Protocole | Rôle | À retenir |
| --- | --- | --- |
| IP | Transporte les paquets entre réseaux | Pas de garantie de livraison |
| TCP | Transport fiable | Connexion, ordre, ACK, retransmission |
| UDP | Transport rapide et léger | Pas de connexion ni garantie |
| ARP | Associe IP et MAC sur le LAN | Fonctionne en broadcast |
| ICMP | Diagnostic et erreurs IP | `ping`, `traceroute` |
| DNS | Traduit nom de domaine en IP | `dig`, `nslookup` |
| DHCP | Distribue une configuration IP | Client sans IP au départ |
| OSPF | Routage dynamique interne | Hello, voisins, LSDB |
| mDNS | Résolution locale sans serveur DNS | Multicast `224.0.0.251` / `ff02::fb` |

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
| 5353 | mDNS | UDP |
| 161/162 | SNMP | UDP |

Lister les ports ouverts :

```bash
ss -tulnp
```

## Encapsulation

```text
Application : données
Transport   : [TCP/UDP][données]
Internet    : [IP][TCP/UDP][données]
Accès réseau: [Ethernet][IP][TCP/UDP][données][FCS]
```

À chaque routeur, l'en-tête Ethernet change. L'adresse IP source et destination reste la référence logique de bout en bout, même si le TTL diminue.

## DHCP DORA

| Étape | Message | Sens |
| --- | --- | --- |
| 1 | Discover | Client -> broadcast |
| 2 | Offer | Serveur -> client |
| 3 | Request | Client -> serveur |
| 4 | Ack | Serveur -> client |

Options DHCP utiles :

| Option | Rôle |
| --- | --- |
| 53 | Type de message DHCP |
| 1 | Masque |
| 3 | Passerelle |
| 6 | DNS |
| 51 | Durée du bail |

Filtre Wireshark : `bootp`.

## OSPF

À observer :

- Hello vers `224.0.0.5` ;
- router-id ;
- hello/dead timers ;
- voisins en état `Full` ;
- LSUpdate lors d'une reconvergence.

Commandes Cisco :

```text
show ip ospf neighbor
show ip ospf interface brief
show ip route ospf
show ip ospf database
```

Filtre Wireshark : `ospf`.

## mDNS

mDNS apparaît souvent dans les captures physiques, même sans action volontaire.

Repères :

- IPv4 multicast : `224.0.0.251` ;
- IPv6 multicast : `ff02::fb` ;
- port UDP : `5353`.

Filtre Wireshark : `mdns` ou `udp.port == 5353`.
