# Critères de réussite - Fiche de dépannage AlpesNet

## Objectif

Cette feuille complète la simulation des pannes AlpesNet. Elle explique ce qui est attendu dans une fiche de dépannage et précise **d'où vient l'erreur** pour chaque panne simulée.

Le but est de montrer une démarche professionnelle : on ne saute pas directement à la solution. On formule une hypothèse, on lance une commande, on analyse le résultat, puis seulement ensuite on identifie la cause.

## Critères de réussite de la fiche

| Critère | Ce qui est attendu | Application AlpesNet |
| --- | --- | --- |
| 1. Démarche couche par couche | La fiche suit les couches OSI sans arriver directement à la solution. | On commence par L1/L2, puis on remonte vers L3, DHCP ou NAT selon le symptôme. |
| 2. Hypothèse avant chaque commande | Chaque commande doit être précédée d'une hypothèse claire. | Exemple : "J'émets l'hypothèse que la route vers le site 3 est absente", puis `show ip route 192.168.30.0`. |
| 3. Cause précise | La cause doit nommer le paramètre fautif exact. | Pas seulement "problème OSPF", mais "le réseau `192.168.30.0/24` n'est pas annoncé par R3". |
| 4. Correctif exact | Les commandes de correction doivent être écrites. | Exemple : `R3(config-router)# network 192.168.30.0 0.0.0.255 area 0`. |
| 5. Vérification du symptôme | Le test final doit reprendre le symptôme initial. | On vérifie par le ping initial, l'obtention DHCP, ou le ping client vers `203.0.113.2`. |

## Règle importante

Une bonne fiche ne dit pas simplement :

```text
Cause : interface en shutdown.
Correctif : no shutdown.
```

Elle doit expliquer **quelle interface**, **sur quel équipement**, **pourquoi cette interface provoque ce symptôme**, et **quel test prouve que le service initial refonctionne**.

Dans notre simulation AlpesNet, les causes sont volontairement plus précises qu'une simple interface coupée.

---

## Panne A - D'où vient l'erreur ?

### Symptôme rappelé

Un PC du site 2 ne peut pas joindre un PC du site 3. Les sites 1 et 4 sont accessibles.

### Raisonnement

Le poste du site 2 n'est pas totalement isolé, car il peut encore atteindre les sites 1 et 4. Le problème ne touche donc pas toute sa connectivité.

Le lien entre `R2` et `R3` n'est pas considéré comme coupé si l'adjacence OSPF reste en état `Full`. Dans ce cas, le problème n'est ni le câble, ni l'interface, ni le voisinage OSPF.

### Origine précise de l'erreur

L'erreur vient de la configuration OSPF de `R3` : le réseau LAN du site 3, `192.168.30.0/24`, n'est plus annoncé dans le processus OSPF.

Conséquence : `R2` peut toujours atteindre d'autres sites, mais il ne reçoit plus de route valide vers le site 3.

### Commande qui révèle l'erreur

```cisco
R3# show running-config | section router ospf
```

Configuration fautive simulée :

```cisco
router ospf 1
 router-id 3.3.3.3
 network 10.0.2.0 0.0.0.3 area 0
 network 10.0.3.0 0.0.0.3 area 0
```

Il manque :

```cisco
network 192.168.30.0 0.0.0.255 area 0
```

### Correctif exact

```cisco
R3(config)# router ospf 1
R3(config-router)# network 192.168.30.0 0.0.0.255 area 0
```

### Vérification qui prouve la résolution

```text
PC-Site2> ping 192.168.30.10
84 bytes from 192.168.30.10 icmp_seq=1 ttl=62 time=...
```

La preuve n'est pas seulement que OSPF affiche une route. La vraie preuve est que le PC du site 2 peut de nouveau joindre le PC du site 3.

---

## Panne B - D'où vient l'erreur ?

### Symptôme rappelé

Les PC du site 1 obtiennent une adresse `169.254.x.x` au lieu d'une IP en `192.168.10.x`.

### Raisonnement

Une adresse `169.254.x.x` est une adresse APIPA. Elle apparaît quand le client ne reçoit pas de réponse DHCP.

Avant d'accuser DHCP, il faut tout de même éliminer les couches basses :

- L1 : le port client et le lien vers le routeur sont actifs ;
- L2 : le VLAN du site 1 est correct ;
- L3 : la passerelle `192.168.10.1` existe sur `R1`.

Une fois ces points validés, le problème se situe bien sur le service DHCP.

### Origine précise de l'erreur

L'erreur vient du pool DHCP de `R1` pour le site 1. Le routeur reçoit les requêtes `DHCPDISCOVER`, mais il ne peut pas répondre avec une adresse `192.168.10.x`, car le pool `SITE1` est absent ou configuré avec un mauvais réseau.

### Commande qui révèle l'erreur

```cisco
R1# show running-config | section ip dhcp pool
```

Configuration fautive simulée :

```cisco
ip dhcp pool SITE2
 network 192.168.20.0 255.255.255.0
 default-router 192.168.20.1
 dns-server 203.0.113.2
```

Il manque un pool correspondant à `192.168.10.0/24`.

### Correctif exact

```cisco
R1(config)# ip dhcp excluded-address 192.168.10.1 192.168.10.20
R1(config)# ip dhcp pool SITE1
R1(dhcp-config)# network 192.168.10.0 255.255.255.0
R1(dhcp-config)# default-router 192.168.10.1
R1(dhcp-config)# dns-server 203.0.113.2
```

### Vérification qui prouve la résolution

```text
PC-Site1> ip dhcp
DORA IP 192.168.10.21/24 GW 192.168.10.1

PC-Site1> show ip
IP 192.168.10.21/24
Gateway 192.168.10.1
```

La preuve est que le client ne reçoit plus une APIPA et obtient bien une adresse en `192.168.10.x`.

---

## Panne C - D'où vient l'erreur ?

### Symptôme rappelé

Les PC internes ne peuvent plus accéder au serveur public `203.0.113.2`. Depuis `R1`, le ping vers `203.0.113.2` fonctionne.

### Raisonnement

Le fait que `R1` puisse ping `203.0.113.2` est très important. Cela élimine :

- une panne du serveur public ;
- une absence de route de sortie sur `R1` ;
- une coupure physique entre `R1` et le réseau public.

La différence entre `R1` et un PC interne, c'est NAT/PAT. `R1` peut sortir directement, alors qu'un client interne en `192.168.x.x` doit être translaté.

### Origine précise de l'erreur

L'erreur vient de la configuration NAT/PAT de `R1`. Les paquets des PC internes ne correspondent pas à l'ACL NAT, ou les interfaces ne sont pas correctement marquées `ip nat inside` et `ip nat outside`.

Si `show ip nat translations` ne crée aucune entrée pendant un ping depuis un PC interne, cela prouve que NAT ne prend pas le trafic client en charge.

### Commande qui révèle l'erreur

```cisco
R1# show running-config | include ip nat|access-list
R1# show ip nat translations
```

Configuration fautive simulée :

```cisco
access-list 1 permit 192.168.10.0 0.0.0.255
ip nat inside source list 1 interface GigabitEthernet0/2 overload
```

Cette ACL ne couvre pas tous les réseaux internes AlpesNet. Elle peut laisser de côté les sites `192.168.20.0/24`, `192.168.30.0/24` et `192.168.40.0/24`.

### Correctif exact

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

Si AlpesNet utilise des sous-interfaces, le `ip nat inside` doit être placé sur les sous-interfaces internes concernées.

### Vérification qui prouve la résolution

Depuis un PC interne :

```text
PC-Site1> ping 203.0.113.2
84 bytes from 203.0.113.2 icmp_seq=1 ttl=...
```

Sur `R1` :

```cisco
R1# show ip nat translations
Pro  Inside global      Inside local       Outside local      Outside global
icmp 10.0.0.1:1         192.168.10.21:1    203.0.113.2:1      203.0.113.2:1
```

La preuve complète est double : le PC interne ping le serveur public et `R1` affiche une translation NAT créée pendant ce test.

---

## Synthèse

| Panne | D'où vient l'erreur ? | Cause précise |
| --- | --- | --- |
| A | OSPF sur `R3` | Le LAN `192.168.30.0/24` du site 3 n'est pas annoncé. |
| B | DHCP sur `R1` | Le pool `SITE1` manque ou ne correspond pas à `192.168.10.0/24`. |
| C | NAT/PAT sur `R1` | L'ACL NAT ou le marquage `inside/outside` ne couvre pas les clients internes. |

À retenir : la cause doit expliquer le lien entre la mauvaise configuration et le symptôme observé. C'est cette phrase qui transforme une simple correction en vraie fiche de dépannage.
