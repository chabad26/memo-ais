# Synthèse — NAT / PAT

## 1. Pourquoi utiliser du NAT ?

Les adresses privées, par exemple `192.168.x.x`, `10.x.x.x` ou `172.16.x.x`, sont prévues pour les réseaux internes. Elles ne sont pas routables directement sur Internet.

Si un poste interne envoie un paquet vers Internet avec une adresse source privée comme `192.168.10.10`, le retour ne peut pas fonctionner correctement : les routeurs Internet ne savent pas renvoyer une réponse vers cette adresse privée.

Le **NAT** (*Network Address Translation*) répond à deux problèmes :

- permettre aux machines d'un réseau privé d'accéder à Internet ;
- économiser les adresses IPv4 publiques.

Grâce au NAT/PAT, toute une entreprise peut sortir sur Internet avec une seule adresse IPv4 publique.

---

## 2. Les types de NAT

| Type | Principe | Cas d'usage |
| --- | --- | --- |
| NAT statique | 1 adresse privée correspond toujours à 1 adresse publique fixe | Exposer un serveur interne depuis Internet |
| NAT dynamique | Des adresses privées utilisent un pool d'adresses publiques disponibles | Peu courant, car il faut plusieurs IP publiques |
| PAT / NAT overload | Plusieurs machines privées partagent une seule adresse publique grâce aux ports | Box Internet, routeur d'entreprise |

### NAT statique

Le **NAT statique** crée une correspondance permanente :

```text
192.168.10.10  <->  203.0.113.10
```

L'équipement interne peut être joignable depuis Internet si les règles de pare-feu l'autorisent.

### NAT dynamique

Le **NAT dynamique** utilise un pool d'adresses publiques. Une translation est créée à la demande, puis supprimée après expiration.

Exemple :

```text
Réseau interne       Pool public
192.168.10.0/24  ->  203.0.113.10 à 203.0.113.20
```

Ce mode est moins fréquent, car il nécessite plusieurs adresses publiques.

### PAT

Le **PAT** (*Port Address Translation*) est aussi appelé **NAT overload**.

Il permet à plusieurs machines internes de partager une seule adresse publique. Le routeur distingue les connexions grâce aux numéros de ports.

C'est le fonctionnement courant :

- des box ADSL/fibre ;
- des routeurs d'entreprise ;
- des accès Internet mutualisés.

---

## 3. Comment fonctionne le PAT ?

Exemple : un poste interne interroge un serveur DNS public.

### Avant NAT

```text
Paquet sortant :

src IP   = 192.168.10.10
src port = 54321
dst IP   = 8.8.8.8
dst port = 53
```

L'adresse source `192.168.10.10` est privée. Elle ne peut pas être utilisée telle quelle sur Internet.

### Table NAT créée par le routeur

```text
Inside Local          Inside Global        Outside
192.168.10.10:54321   203.0.113.1:32001   8.8.8.8:53
```

Vocabulaire Cisco :

| Terme | Signification |
| --- | --- |
| `Inside local` | Adresse réelle du client dans le réseau privé |
| `Inside global` | Adresse publique utilisée après translation |
| `Outside global` | Adresse de destination sur Internet |

### Après NAT

```text
Paquet envoyé sur Internet :

src IP   = 203.0.113.1
src port = 32001
dst IP   = 8.8.8.8
dst port = 53
```

Le routeur a remplacé l'adresse privée par son adresse publique et a réécrit le port source.

### Réponse reçue

```text
Réponse :

dst IP   = 203.0.113.1
dst port = 32001
```

Le routeur consulte sa table NAT, retrouve la correspondance, puis réécrit la destination :

```text
203.0.113.1:32001 -> 192.168.10.10:54321
```

La réponse est ensuite livrée au bon poste interne.

---

## 4. Configuration PAT sur Cisco IOS

Objectif : permettre aux réseaux internes de sortir vers Internet avec l'adresse publique de l'interface externe.

### Étape 1 : marquer les interfaces NAT

Les interfaces côté LAN sont en `inside`. L'interface côté Internet est en `outside`.

Exemple simple :

```bash
R1(config)# interface GigabitEthernet0/0
R1(config-if)# ip nat inside
R1(config-if)# description LAN-interne-inside-NAT
R1(config-if)# exit

R1(config)# interface GigabitEthernet0/2
R1(config-if)# ip nat outside
R1(config-if)# description Vers-Internet-outside-NAT
R1(config-if)# exit
```

Dans le lab avec plusieurs VLANs, les sous-interfaces internes peuvent aussi être déclarées en `inside` :

```bash
R1(config)# interface GigabitEthernet0/0
R1(config-if)# ip nat inside
R1(config-if)# exit

R1(config)# interface GigabitEthernet0/1.20
R1(config-subif)# ip nat inside
R1(config-subif)# exit

R1(config)# interface GigabitEthernet0/1.30
R1(config-subif)# ip nat inside
R1(config-subif)# exit

R1(config)# interface GigabitEthernet0/1.40
R1(config-subif)# ip nat inside
R1(config-subif)# exit

R1(config)# interface GigabitEthernet0/2
R1(config-if)# ip nat outside
R1(config-if)# exit
```

### Étape 2 : définir les adresses privées à translater

On utilise une ACL pour dire quelles adresses internes ont le droit d'être translatées.

Pour tout le lab `192.168.10.0/24` :

```bash
R1(config)# access-list 1 permit 192.168.10.0 0.0.0.255
```

Si d'autres réseaux internes existent :

```bash
R1(config)# access-list 1 permit 192.168.20.0 0.0.0.255
```

### Étape 3 : activer le PAT

```bash
R1(config)# ip nat inside source list 1 interface GigabitEthernet0/2 overload
```

Lecture :

- `inside source` : on traduit les adresses sources venant du réseau interne ;
- `list 1` : seules les adresses autorisées par l'ACL 1 sont concernées ;
- `interface GigabitEthernet0/2` : l'adresse de sortie est celle de l'interface Internet ;
- `overload` : plusieurs clients partagent la même adresse publique grâce aux ports.

### Étape 4 : ajouter une route par défaut

Le routeur doit savoir où envoyer le trafic Internet.

```bash
R1(config)# ip route 0.0.0.0 0.0.0.0 203.0.113.2
```

Ici, `203.0.113.2` représente le next-hop côté FAI ou routeur Internet simulé.

---

## 5. Vérifier NAT/PAT

### Voir les translations actives

```bash
R1# show ip nat translations
```

Exemple :

```text
Pro  Inside local        Inside global       Outside global
icmp 192.168.10.10:1     203.0.113.1:1024    8.8.8.8:1
udp  192.168.10.11:54321 203.0.113.1:32001   8.8.8.8:53
```

Chaque ligne correspond à une connexion active ou récente.

### Voir les statistiques NAT

```bash
R1# show ip nat statistics
```

Exemple :

```text
Total active translations: 5
Peak translations: 12
Hits: 234
Misses: 3
```

Lecture :

- `active translations` : nombre de translations actuellement en table ;
- `peak translations` : maximum atteint ;
- `hits` : paquets ayant utilisé une translation existante ;
- `misses` : paquets nécessitant une nouvelle translation.

### Effacer les translations

Utile pendant un debug ou après modification de la configuration NAT :

```bash
R1# clear ip nat translation *
```

---

## 6. Exemple de test

Depuis un PC interne :

```bash
PC> ping 8.8.8.8
```

Puis sur R1 :

```bash
R1# show ip nat translations
R1# show ip nat statistics
```

Si le ping fonctionne et que des translations apparaissent, le PAT est opérationnel.

Si aucune translation n'apparaît :

- vérifier que l'interface LAN est bien en `ip nat inside` ;
- vérifier que l'interface Internet est bien en `ip nat outside` ;
- vérifier que l'ACL autorise le réseau source ;
- vérifier la route par défaut ;
- vérifier que le next-hop Internet répond.

---

## 7. Résumé express

| Élément | À retenir |
| --- | --- |
| Adresses privées | Non routables directement sur Internet |
| NAT | Traduit une adresse privée en adresse publique |
| NAT statique | 1 privée vers 1 publique fixe |
| NAT dynamique | Pool privé vers pool public |
| PAT | Plusieurs clients vers 1 seule IP publique |
| `inside` | Côté réseau interne |
| `outside` | Côté Internet |
| ACL NAT | Définit les sources à translater |
| `overload` | Active le partage par ports |
| Vérification | `show ip nat translations`, `show ip nat statistics` |

---

## Sources

- [RFC 3022 — Traditional IP Network Address Translator](https://datatracker.ietf.org/doc/html/rfc3022)
- [RFC 2993 — Architectural Implications of NAT](https://datatracker.ietf.org/doc/html/rfc2993)
- [Cisco — Configuring Network Address Translation](https://www.cisco.com/c/en/us/support/docs/ip/network-address-translation-nat/13772-12.html)
- [RFC 1918 — Address Allocation for Private Internets](https://datatracker.ietf.org/doc/html/rfc1918)
