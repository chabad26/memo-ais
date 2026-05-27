# Fondations TCP/IP et capture

## 1.1 — Modèle TCP/IP et protocoles fondamentaux

### Objectif

Comprendre comment les données voyagent sur un réseau : quel protocole intervient, à quelle couche, avec quelle responsabilité. Le modèle TCP/IP repose sur une idée simple : séparer les rôles en couches indépendantes pour permettre à des réseaux et systèmes différents de communiquer.

Historiquement, TCP/IP apparaît dans les années 1970 pour répondre à un problème d'interopérabilité : chaque constructeur utilisait ses propres protocoles. DARPA finance alors une architecture ouverte, portée notamment par Vint Cerf et Bob Kahn, capable de relier des réseaux hétérogènes.

### Le modèle TCP/IP en 4 couches

| Couche | Rôle | Protocoles et technologies |
| --- | --- | --- |
| Application | Services utilisés par les applications | HTTP, HTTPS, DNS, DHCP, SSH, FTP, SMTP, SNMP |
| Transport | Communication entre processus, fiabilité ou rapidité | TCP, UDP |
| Internet | Adressage logique et routage entre réseaux | IP, ICMP, ARP |
| Accès réseau | Transmission locale sur le support physique | Ethernet, Wi-Fi 802.11, PPP, VLAN 802.1Q |

Chaque couche rend un service à la couche supérieure et utilise la couche inférieure. Par exemple, HTTP n'a pas besoin de savoir si la machine utilise Ethernet ou Wi-Fi.

### Protocoles à connaître

#### IP — Internet Protocol

IP est le protocole central d'Internet. Il sert à acheminer des paquets d'une source vers une destination, parfois à travers plusieurs routeurs.

Caractéristiques importantes :

- protocole sans connexion ;
- pas de garantie de livraison ;
- pas de garantie d'ordre ;
- chaque paquet est traité indépendamment ;
- le champ TTL est décrémenté à chaque routeur.

Quand le TTL atteint 0, le paquet est détruit et un message ICMP **TTL Exceeded** est renvoyé. C'est ce mécanisme qui permet à `traceroute` de découvrir le chemin suivi.

#### TCP — Transmission Control Protocol

TCP ajoute la fiabilité au-dessus d'IP. Il garantit que les données arrivent complètes, dans le bon ordre et sans duplication.

Avant d'échanger des données, TCP établit une connexion avec le **3-way handshake** :

```text
Client                       Serveur
  | ---- SYN --------------> |
  | <--- SYN-ACK ----------- |
  | ---- ACK --------------> |
  | ==== Données ========== |
```

TCP utilise des numéros de séquence, des accusés de réception, des retransmissions et une fenêtre glissante. On l'utilise quand l'intégrité des données est prioritaire : web, SSH, transfert de fichiers, email.

| Service | Transport | Pourquoi |
| --- | --- | --- |
| HTTP/HTTPS | TCP | Une page ne doit pas arriver corrompue |
| SSH | TCP | Une commande doit arriver complète |
| FTP | TCP | Un fichier tronqué est inutilisable |
| SMTP | TCP | Un email partiel est illisible |

#### UDP — User Datagram Protocol

UDP est plus simple et plus léger que TCP. Il envoie des datagrammes sans connexion, sans garantie de livraison et sans ordre garanti.

On l'utilise quand la latence compte plus que la fiabilité parfaite :

| Service | Transport | Pourquoi |
| --- | --- | --- |
| DNS | UDP | Une requête tient souvent dans un seul paquet |
| DHCP | UDP | Fonctionne avant même que le client ait une IP |
| Streaming | UDP | Mieux vaut perdre un paquet que bloquer la vidéo |
| VoIP | UDP | Mieux vaut un court silence qu'un gel de l'appel |

#### Ports TCP et UDP

Les ports permettent à un système d'exploitation d'envoyer les paquets à la bonne application. Un port est un nombre de 0 à 65535.

| Plage | Nom | Usage |
| --- | --- | --- |
| 0-1023 | Ports bien connus | Services standards |
| 1024-49151 | Ports enregistrés | Applications connues |
| 49152-65535 | Ports éphémères | Ports temporaires côté client |

Ports standards à retenir :

| Port | Service | Transport |
| --- | --- | --- |
| 22 | SSH | TCP |
| 25 | SMTP | TCP |
| 53 | DNS | UDP et TCP |
| 67/68 | DHCP | UDP |
| 80 | HTTP | TCP |
| 443 | HTTPS | TCP |
| 161/162 | SNMP | UDP |

Commande utile :

```bash
ss -tulnp
```

#### ARP — Address Resolution Protocol

ARP associe une adresse IP à une adresse MAC sur un réseau local. Une machine connaît généralement l'adresse IP de destination, mais Ethernet a besoin d'une adresse MAC pour livrer une trame.

Principe :

1. Le PC veut joindre une IP locale.
2. Il cherche l'adresse MAC correspondante dans son cache ARP.
3. Si elle est absente, il envoie une requête ARP en broadcast.
4. La machine concernée répond avec son adresse MAC.
5. Le PC mémorise l'association temporairement.

Commandes utiles :

```bash
ip neigh show
arp -a
ping -c 1 192.168.10.1 && ip neigh show
```

Point sécurité : ARP ne vérifie pas l'identité des machines. Cela rend possible l'ARP spoofing. Sur des switches managés, une contre-mesure courante est **Dynamic ARP Inspection**.

#### ICMP — Internet Control Message Protocol

ICMP sert à signaler des erreurs et à diagnostiquer la connectivité IP. Il ne transporte pas de données applicatives.

| Type ICMP | Signification | Outil |
| --- | --- | --- |
| 8 / 0 | Echo Request / Echo Reply | `ping` |
| 3 | Destination Unreachable | Diagnostic automatique |
| 11 | TTL Exceeded | `traceroute` |

Commandes utiles :

```bash
ping -c 4 8.8.8.8
traceroute 8.8.8.8
mtr --report 8.8.8.8
```

#### DNS — Domain Name System

DNS traduit les noms de domaine en adresses IP. Sans DNS, il faudrait mémoriser les adresses IP des services.

Résumé d'une résolution récursive :

1. Le navigateur demande l'adresse IP d'un nom.
2. Le système vérifie son cache local.
3. La requête part vers le résolveur DNS configuré.
4. Le résolveur interroge les serveurs racine.
5. Il interroge ensuite le serveur TLD concerné, par exemple `.com`.
6. Il interroge le serveur autoritaire du domaine.
7. Il renvoie l'adresse IP au client.

DNS utilise souvent UDP, car une requête simple tient dans un paquet. TCP peut être utilisé pour les réponses volumineuses ou certains échanges spécifiques.

Commandes utiles :

```bash
nslookup google.com
dig @8.8.8.8 google.com A
dig google.com MX
```

### Encapsulation

Quand une application envoie des données, chaque couche ajoute son propre en-tête. C'est le principe d'encapsulation.

```text
Application : Données HTTP
Transport   : [TCP][Données HTTP]
Internet    : [IP][TCP][Données HTTP]
Accès réseau: [Ethernet][IP][TCP][Données HTTP][FCS]
```

À chaque routeur, l'en-tête Ethernet est remplacé pour le prochain lien. L'en-tête IP, lui, continue jusqu'à la destination, même si certains champs comme le TTL évoluent.

### Ressources

- RFC 791 : IPv4 — <https://tools.ietf.org/html/rfc791>
- RFC 793 : TCP — <https://tools.ietf.org/html/rfc793>
- RFC 9293 : TCP mis à jour — <https://www.rfc-editor.org/rfc/rfc9293>
- RFC 768 : UDP — <https://tools.ietf.org/html/rfc768>
- RFC 826 : ARP — <https://tools.ietf.org/html/rfc826>
- RFC 792 : ICMP — <https://tools.ietf.org/html/rfc792>
- RFC 1034 et 1035 : DNS — <https://tools.ietf.org/html/rfc1034>
- IANA ports : <https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml>
- Cloudflare Learning : <https://www.cloudflare.com/learning/>
- Pages manuelles : `man ip`, `man ss`, `man ping`, `man dig`
