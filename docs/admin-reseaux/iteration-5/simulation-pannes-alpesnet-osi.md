# Simulation de pannes AlpesNet avec la méthode OSI

## Contexte

Le projet GNS3 AlpesNet utilisé pour l'exercice est corrompu. Les pannes ci-dessous sont donc **simulées** à partir de l'architecture déjà documentée :

- 4 sites reliés par OSPF ;
- DHCP actif sur les sites ;
- NAT/PAT configuré sur `R1` ;
- serveur public joignable en `203.0.113.2`.

L'objectif n'est pas de prouver une capture réelle, mais de montrer une démarche de diagnostic propre : partir du symptôme, tester couche par couche, identifier une cause probable, appliquer un correctif minimal, puis vérifier que le symptôme initial disparaît.

## Mode opératoire

Pour chaque panne :

1. Lire précisément le symptôme.
2. Délimiter le périmètre : qui est impacté, qui fonctionne encore.
3. Appliquer la démarche OSI de L1 vers L7.
4. Documenter les tests dans la fiche de dépannage.
5. Appliquer un seul correctif.
6. Refaire le test initial pour confirmer la résolution.

## Rappel de topologie logique

```text
Site 1 --- R1 --- R2 --- R3 --- R4 --- Site 4
          NAT      |      |
         /PAT    Site 2  Site 3
           |
 réseau public 203.0.113.0/30
```

Hypothèses d'adressage utilisées pour la simulation :

| Élément | Réseau / IP |
| --- | --- |
| Site 1 | `192.168.10.0/24` |
| Site 2 | `192.168.20.0/24` |
| Site 3 | `192.168.30.0/24` |
| Site 4 | `192.168.40.0/24` |
| Lien R1-R2 | `10.0.1.0/30` |
| Lien R2-R3 | `10.0.2.0/30` |
| Lien R3-R4 | `10.0.3.0/30` |
| Serveur public | `203.0.113.2` |

---

## Panne A - Site 2 ne joint pas le site 3

### Symptôme

Un PC du site 2 ne peut pas joindre un PC du site 3. Les sites 1 et 4 sont accessibles.

### Fiche de dépannage

```text
=== FICHE DE DÉPANNAGE ===
Auteur     : Olivier
Date/Heure : 2026-06-04
Topologie  : AlpesNet - simulation OSI
Panne      : A

SYMPTÔME
Depuis PC-Site2, le ping vers PC-Site3 échoue.
Les pings vers Site1 et Site4 fonctionnent.

PÉRIMÈTRE
Affecte : le trafic Site2 -> Site3.
Fonctionne encore : Site2 -> Site1, Site2 -> Site4.
Première lecture : le poste et la passerelle du site 2 ne sont pas totalement isolés.
Le problème vise probablement une route précise vers le réseau 192.168.30.0/24.
```

| Couche | Hypothèse avant le test | Commande simulée | Résultat simulé | Conclusion |
| --- | --- | --- | --- | --- |
| L1 | Le PC ou le lien local du site 2 est coupé. | `show ip interface brief` sur R2 | Interfaces LAN et WAN en `up/up` | L1 OK |
| L2 | Le PC du site 2 ne résout pas sa passerelle. | `arp -a` / `show arp` | MAC de la passerelle présente | L2 OK |
| L3 | La route vers le site 3 manque ou pointe au mauvais endroit. | `R2# show ip route 192.168.30.0` | Route absente ou route statique incorrecte | Cause en L3 |
| L3 | OSPF n'apprend plus le réseau du site 3. | `R2# show ip ospf neighbor` | Voisin R3 `Full`, mais route `192.168.30.0/24` absente | Annonce OSPF du LAN site 3 incorrecte |
| L4-L7 | Non prioritaire. | Non testé | ICMP échoue déjà en L3 | Inutile d'aller plus haut |

### Cause identifiée

La panne est simulée comme une **annonce OSPF manquante sur R3** : le réseau LAN du site 3 n'est plus déclaré dans le processus OSPF.

Exemple de configuration fautive :

```cisco
R3# show running-config | section router ospf
router ospf 1
 router-id 3.3.3.3
 network 10.0.2.0 0.0.0.3 area 0
 network 10.0.3.0 0.0.0.3 area 0
```

Il manque :

```cisco
network 192.168.30.0 0.0.0.255 area 0
```

### Correctif appliqué

```cisco
R3(config)# router ospf 1
R3(config-router)# network 192.168.30.0 0.0.0.255 area 0
```

### Vérification

```text
R2# show ip route 192.168.30.0
O 192.168.30.0/24 [110/2] via 10.0.2.2

PC-Site2> ping 192.168.30.10
84 bytes from 192.168.30.10 icmp_seq=1 ttl=62 time=...
```

Conclusion : la route vers le site 3 est réapprise par OSPF et le ping initial fonctionne.

---

## Panne B - Les PC du site 1 reçoivent une APIPA

### Symptôme

Les PC du site 1 obtiennent une adresse `169.254.x.x` au lieu d'une IP en `192.168.10.x`.

Rappel : une adresse APIPA signifie que le client n'a reçu aucune réponse DHCP dans le délai attendu.

### Fiche de dépannage

```text
=== FICHE DE DÉPANNAGE ===
Auteur     : Olivier
Date/Heure : 2026-06-04
Topologie  : AlpesNet - simulation OSI
Panne      : B

SYMPTÔME
Les PC du site 1 n'obtiennent pas d'adresse DHCP.
Ils s'auto-attribuent une adresse 169.254.x.x.

PÉRIMÈTRE
Affecte : les clients DHCP du site 1.
Fonctionne encore : le routeur R1 peut être joignable si une IP statique correcte est posée.
Première lecture : le problème concerne DHCP, donc L7 applicatif, mais il faut d'abord vérifier L1 à L3.
```

| Couche | Hypothèse avant le test | Commande simulée | Résultat simulé | Conclusion |
| --- | --- | --- | --- | --- |
| L1 | Le lien PC-switch ou switch-routeur est coupé. | `show interfaces status` / `show ip interface brief` | Ports en `connected`, interfaces `up/up` | L1 OK |
| L2 | Le VLAN du port client est mauvais ou le trunk ne transporte pas le VLAN site 1. | `show vlan brief` et `show interfaces trunk` | VLAN site 1 présent et autorisé | L2 OK |
| L3 | La passerelle du réseau site 1 est absente. | `R1# show ip interface brief` | Interface LAN site 1 en `192.168.10.1` et `up/up` | L3 OK |
| L7 | Le service DHCP ne propose pas d'adresse pour `192.168.10.0/24`. | `show running-config | section ip dhcp pool` | Pool absent ou mauvais réseau configuré | Cause DHCP |
| L7 | Le serveur reçoit les Discover mais ne répond pas. | `show ip dhcp server statistics` | `DHCPDISCOVER` augmente, `DHCPOFFER` reste à `0` | Pool DHCP incorrect |

### Cause identifiée

La panne est simulée comme un **pool DHCP manquant ou mal configuré sur R1** pour le site 1.

Exemple de configuration fautive :

```cisco
R1# show running-config | section ip dhcp pool
ip dhcp pool SITE2
 network 192.168.20.0 255.255.255.0
 default-router 192.168.20.1
 dns-server 203.0.113.2
```

Il n'y a aucun pool correspondant au réseau `192.168.10.0/24`.

### Correctif appliqué

```cisco
R1(config)# ip dhcp excluded-address 192.168.10.1 192.168.10.20
R1(config)# ip dhcp pool SITE1
R1(dhcp-config)# network 192.168.10.0 255.255.255.0
R1(dhcp-config)# default-router 192.168.10.1
R1(dhcp-config)# dns-server 203.0.113.2
```

### Vérification

Sur un PC du site 1 :

```text
PC-Site1> ip dhcp
DORA IP 192.168.10.21/24 GW 192.168.10.1

PC-Site1> show ip
IP 192.168.10.21/24
Gateway 192.168.10.1
```

Sur R1 :

```cisco
R1# show ip dhcp binding
192.168.10.21    client-id/hardware-address    Automatic

R1# show ip dhcp server statistics
DHCPOFFER et DHCPACK augmentent
```

Conclusion : les clients ne reçoivent plus d'APIPA et obtiennent une adresse valide en `192.168.10.x`.

---

## Panne C - Les PC internes ne joignent plus le serveur public

### Symptôme

Les PC internes ne peuvent plus accéder au serveur public `203.0.113.2`. Depuis `R1` lui-même, le ping vers `203.0.113.2` fonctionne.

### Fiche de dépannage

```text
=== FICHE DE DÉPANNAGE ===
Auteur     : Olivier
Date/Heure : 2026-06-04
Topologie  : AlpesNet - simulation OSI
Panne      : C

SYMPTÔME
Depuis les PC internes, le ping vers 203.0.113.2 échoue.
Depuis R1, le ping vers 203.0.113.2 fonctionne.

PÉRIMÈTRE
Affecte : les clients internes uniquement.
Fonctionne encore : connectivité R1 -> serveur public.
Première lecture : le chemin externe existe. Le problème se situe entre les réseaux privés et la sortie publique, donc probablement NAT/PAT.
```

| Couche | Hypothèse avant le test | Commande simulée | Résultat simulé | Conclusion |
| --- | --- | --- | --- | --- |
| L1 | Une interface de sortie est coupée. | `R1# show ip interface brief` | Interface vers Internet `up/up` | L1 OK |
| L2 | Le lien R1-réseau public ne résout pas l'adresse du next-hop. | `R1# show arp` | ARP présent pour le next-hop public | L2 OK |
| L3 | R1 n'a pas de route vers `203.0.113.2`. | `R1# ping 203.0.113.2` | Ping OK depuis R1 | L3 externe OK |
| L3 | Le PC interne n'a pas de passerelle correcte. | `show ip` sur PC interne | Gateway correcte vers R1 | L3 interne OK |
| L3/NAT | Les paquets privés sortent sans translation. | `R1# show ip nat translations` après ping client | Aucune nouvelle translation | Cause NAT |
| L3/NAT | L'ACL NAT ne couvre pas les réseaux internes. | `show running-config | include ip nat|access-list` | ACL NAT absente ou trop restrictive | Cause confirmée |

### Cause identifiée

La panne est simulée comme une **ACL NAT incorrecte sur R1**. `R1` peut joindre le serveur public avec sa propre IP, mais les PC internes en `192.168.x.x` ne sont pas translatés.

Exemple de configuration fautive :

```cisco
access-list 1 permit 192.168.10.0 0.0.0.255
ip nat inside source list 1 interface GigabitEthernet0/2 overload
```

Dans cet exemple, seuls les clients du site 1 sont couverts. Si la panne touche tous les PC internes, l'ACL peut aussi être vide, supprimée, ou associée à la mauvaise interface.

### Correctif appliqué

Correctif large pour couvrir les quatre sites privés AlpesNet :

```cisco
R1(config)# no access-list 1
R1(config)# access-list 1 permit 192.168.0.0 0.0.255.255
R1(config)# interface GigabitEthernet0/0
R1(config-if)# ip nat inside
R1(config)# interface GigabitEthernet0/1
R1(config-if)# ip nat inside
R1(config)# interface GigabitEthernet0/2
R1(config-if)# ip nat outside
R1(config)# ip nat inside source list 1 interface GigabitEthernet0/2 overload
```

Si la topologie utilise des sous-interfaces, le marquage `ip nat inside` doit être posé sur les sous-interfaces internes concernées, par exemple `Gi0/1.10`, `Gi0/1.20`, `Gi0/1.30` et `Gi0/1.40`.

### Vérification

Depuis un PC interne :

```text
PC-Site1> ping 203.0.113.2
84 bytes from 203.0.113.2 icmp_seq=1 ttl=...
```

Sur R1 :

```cisco
R1# show ip nat translations
Pro  Inside global      Inside local       Outside local      Outside global
icmp 10.0.0.1:1         192.168.10.21:1    203.0.113.2:1      203.0.113.2:1

R1# show ip nat statistics
Hits augmentent pendant les pings
```

Conclusion : le serveur public était joignable depuis R1, mais les clients internes n'étaient pas traduits. Après correction NAT/PAT, les PC internes accèdent de nouveau à `203.0.113.2`.

---

## Synthèse des causes simulées

| Panne | Couche OSI principale | Cause simulée | Correctif |
| --- | --- | --- | --- |
| A | L3 - Réseau | Réseau du site 3 non annoncé dans OSPF | Ajouter `network 192.168.30.0 0.0.0.255 area 0` sur R3 |
| B | L7 - Service DHCP, après validation L1-L3 | Pool DHCP du site 1 absent ou incorrect | Recréer le pool DHCP `SITE1` sur R1 |
| C | L3/NAT | ACL NAT ou marquage inside/outside incorrect sur R1 | Corriger ACL NAT, interfaces `ip nat inside/outside`, et PAT overload |

## Conclusion

Même sans maquette GNS3 exploitable, les trois pannes peuvent être documentées de manière crédible si la logique reste claire :

- Panne A : le symptôme vise un réseau distant précis, donc on cherche une erreur de routage.
- Panne B : l'APIPA prouve que DHCP ne répond pas, mais on vérifie d'abord le lien, le VLAN et la passerelle.
- Panne C : R1 atteint le serveur public mais pas les clients, donc la cible principale est NAT/PAT.

Le point important est de ne pas annoncer directement la cause. On montre d'abord les tests qui éliminent les couches basses, puis on justifie la couche où le correctif est appliqué.
