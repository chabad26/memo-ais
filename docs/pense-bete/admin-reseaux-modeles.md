# Modèles et Adressage

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
