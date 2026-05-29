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
