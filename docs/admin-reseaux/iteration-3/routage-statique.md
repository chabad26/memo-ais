# Routage statique

!!! note "Vocabulaire"
    Les sigles et termes comme `OSPF`, `RIP`, `next-hop`, `métrique` ou `distance administrative` sont résumés dans le [glossaire réseaux - itération 3](../../pense-bete/glossaire/admin-reseaux/iteration-3.md).

## Pourquoi router ?

Un switch travaille surtout en **couche 2** : il transporte des trames Ethernet à l'intérieur d'un même réseau local.

Pour faire communiquer deux réseaux IP différents, par exemple `192.168.10.0/24` et `192.168.20.0/24`, il faut un équipement de **couche 3** : un routeur ou un switch L3.

Le routeur lit l'**adresse IP de destination** de chaque paquet, consulte sa table de routage, puis choisit l'interface ou le next-hop vers lequel envoyer le paquet.

---

## Table de routage

La table de routage est la liste des réseaux connus par le routeur et du chemin à utiliser pour les atteindre.

```bash
R1# show ip route
```

Exemple de lignes importantes :

```text
C     192.168.10.0/24 is directly connected, GigabitEthernet0/0
L     192.168.10.1/32 is directly connected, GigabitEthernet0/0
S     192.168.20.0/24 [1/0] via 10.0.1.2
O     192.168.30.0/24 [110/2] via 10.0.1.2
S*    0.0.0.0/0 [1/0] via 203.0.113.2
```

| Code | Signification | Distance admin. |
| --- | --- | --- |
| `C` | Réseau directement connecté | 0 |
| `L` | Adresse IP locale de l'interface (`/32`) | 0 |
| `S` | Route statique configurée à la main | 1 |
| `O` | Route apprise par OSPF | 110 |
| `R` | Route apprise par RIP | 120 |
| `S*` | Route statique par défaut | 1 |

Dans `[1/0]` :

- `1` = distance administrative, donc la priorité de la source de la route ;
- `0` = métrique, donc le coût du chemin.

Plus la distance administrative est basse, plus la route est préférée.

---

## Longest Prefix Match

Si plusieurs routes correspondent à la destination, le routeur choisit la route la plus précise, c'est-à-dire celle avec le **préfixe le plus long**.

Destination : `192.168.10.25`

```text
0.0.0.0/0          -> correspond, mais très général
192.168.0.0/16     -> correspond, plus précis
192.168.10.0/24    -> correspond, choisi car plus spécifique
```

---

## Configurer une route statique

Syntaxe générale :

```bash
R1(config)# ip route <réseau_destination> <masque> <next-hop>
```

Exemple :

```bash
R1(config)# ip route 192.168.20.0 255.255.255.0 10.0.1.2
```

Route par défaut, utilisée quand aucune route plus spécifique n'existe :

```bash
R1(config)# ip route 0.0.0.0 0.0.0.0 203.0.113.2
```

Vérification :

```bash
R1# show ip route static
R1# ping 192.168.20.10
```

---

## Limites du routage statique

- Chaque route doit être ajoutée manuellement sur chaque routeur.
- Si un lien tombe, la route peut rester dans la table et le trafic est perdu.
- Il n'y a pas de convergence automatique.
- Plus le réseau grossit, plus la configuration devient lourde à maintenir.

Le routage statique est donc adapté aux petites topologies ou aux routes simples. Pour des réseaux plus grands ou redondants, on utilise plutôt du routage dynamique comme OSPF.

---

## Exercice GNS3 : routage statique entre deux sites

Objectif : faire communiquer deux LANs différents avec deux routeurs reliés par un lien WAN simulé.

Topologie utilisée :

- Site 1 : LAN `192.168.10.0/24`, passerelle `192.168.10.1` sur R1.
- Site 2 : LAN `192.168.20.0/24`, passerelle `192.168.20.1` sur R2.
- Lien WAN R1-R2 : réseau `10.0.1.0/30`.
- R1 côté WAN : `10.0.1.1/30`.
- R2 côté WAN : `10.0.1.2/30`.

### 1. Configuration des interfaces

Sur R1, les interfaces LAN et WAN sont configurées avec une adresse IP, une description et `no shutdown`.

```bash
R1(config)# interface GigabitEthernet0/0
R1(config-if)# ip address 192.168.10.1 255.255.255.0
R1(config-if)# description "LAN-Site1"
R1(config-if)# no shutdown

R1(config)# interface GigabitEthernet0/1
R1(config-if)# ip address 10.0.1.1 255.255.255.252
R1(config-if)# description "WAN-vers-R2"
R1(config-if)# no shutdown
```

Sur R2, on applique la même logique :

- `192.168.20.1/24` côté LAN ;
- `10.0.1.2/30` côté WAN.

La commande `show ip interface brief` permet de vérifier que les interfaces sont bien en état `up/up`.

### 2. Ajout des routes statiques

Chaque routeur connaît automatiquement ses réseaux directement connectés. En revanche, il ne connaît pas le LAN distant : il faut donc ajouter une route statique.

```bash
R1(config)# ip route 192.168.20.0 255.255.255.0 10.0.1.2
R2(config)# ip route 192.168.10.0 255.255.255.0 10.0.1.1
```

Lecture :

- R1 envoie les paquets vers `192.168.20.0/24` au next-hop `10.0.1.2`.
- R2 envoie les paquets vers `192.168.10.0/24` au next-hop `10.0.1.1`.

### 3. Test de connectivité

Depuis le PC du site 1, le ping vers un PC du site 2 valide le routage entre les deux LANs.

![Ping du PC-A vers le site 2](../../assets/img/admin-reseau/it-3/ping%20PC.png)

Si le ping répond, cela confirme que :

- les interfaces sont actives ;
- les passerelles des PC sont correctes ;
- les routes statiques existent dans les deux sens.

### 4. Lecture de la table de routage

Sur R1, la commande `show ip route` permet de documenter les routes connues.

![Table de routage de R1](../../assets/img/admin-reseau/it-3/show%20ip%20route%20R1.png)

Exemple d'annotation des lignes importantes :

| Code | Réseau | Via | Signification |
| --- | --- | --- | --- |
| `C` | `10.0.1.0/30` | `GigabitEthernet0/1` | Réseau WAN directement connecté à R1. |
| `L` | `10.0.1.1/32` | `GigabitEthernet0/1` | Adresse IP locale de l'interface WAN de R1. |
| `C` | `192.168.10.0/24` | `GigabitEthernet0/0` | LAN du site 1 directement connecté à R1. |
| `L` | `192.168.10.1/32` | `GigabitEthernet0/0` | Adresse IP locale de l'interface LAN de R1. |
| `S` | `192.168.20.0/24` | `10.0.1.2` | Route statique vers le LAN du site 2, via R2. |

À retenir : la ligne `S` est celle qui a été ajoutée manuellement avec `ip route`.

### 5. Observation d'une panne

On coupe ensuite le lien WAN côté R1 :

```bash
R1(config)# interface GigabitEthernet0/1
R1(config-if)# shutdown
R1# show ip route
```

![Shutdown de l'interface WAN et nouvelle table de routage](../../assets/img/admin-reseau/it-3/shutdown%20interface%200%201.png)

Constat :

- le réseau WAN directement connecté peut disparaître si l'interface est coupée ;
- la route statique `S` vers `192.168.20.0/24` peut rester présente ;
- le routeur ne recalcule pas automatiquement un autre chemin.

C'est la limite principale du routage statique : il ne fait pas de convergence automatique. Si le lien tombe, l'administrateur doit corriger la configuration ou remettre le lien en service.

---

## Exercice GNS3 : routage statique entre trois sites

Objectif : chaque routeur doit pouvoir atteindre les deux autres réseaux LAN.

Topologie logique :

- Site 1 : `192.168.10.0/24`, PC `192.168.10.10`, routeur R1.
- Site 2 : `192.168.20.0/24`, PC `192.168.20.10`, routeur R2.
- Site 3 : `192.168.30.0/24`, PC `192.168.30.10`, routeur R3.
- Lien R1-R2 : `10.0.1.0/30`, avec R1 `10.0.1.1` et R2 `10.0.1.2`.
- Lien R2-R3 : `10.0.2.0/30`, avec R2 `10.0.2.1` et R3 `10.0.2.2`.

Dans cette topologie, R2 sert de routeur intermédiaire entre le site 1 et le site 3.

### 1. Routes statiques nécessaires

Chaque routeur connaît déjà ses réseaux directement connectés. Il faut donc ajouter uniquement les routes vers les LANs distants.

Sur R1 :

```bash
R1(config)# ip route 192.168.20.0 255.255.255.0 10.0.1.2
R1(config)# ip route 192.168.30.0 255.255.255.0 10.0.1.2
```

R1 envoie vers R2 tout ce qui concerne le site 2 et le site 3.

Sur R2 :

```bash
R2(config)# ip route 192.168.10.0 255.255.255.0 10.0.1.1
R2(config)# ip route 192.168.30.0 255.255.255.0 10.0.2.2
```

R2 connaît les deux côtés du réseau : il envoie vers R1 pour joindre le site 1, et vers R3 pour joindre le site 3.

Sur R3 :

```bash
R3(config)# ip route 192.168.10.0 255.255.255.0 10.0.2.1
R3(config)# ip route 192.168.20.0 255.255.255.0 10.0.2.1
```

R3 envoie vers R2 tout ce qui concerne le site 1 et le site 2.

Résumé :

| Routeur | Route vers site 1 | Route vers site 2 | Route vers site 3 |
| --- | --- | --- | --- |
| R1 | Déjà connecté | `ip route 192.168.20.0 255.255.255.0 10.0.1.2` | `ip route 192.168.30.0 255.255.255.0 10.0.1.2` |
| R2 | `ip route 192.168.10.0 255.255.255.0 10.0.1.1` | Déjà connecté | `ip route 192.168.30.0 255.255.255.0 10.0.2.2` |
| R3 | `ip route 192.168.10.0 255.255.255.0 10.0.2.1` | `ip route 192.168.20.0 255.255.255.0 10.0.2.1` | Déjà connecté |

### 2. Tests de ping

Il faut tester toutes les combinaisons utiles entre les sites :

- site 1 vers site 2 ;
- site 1 vers site 3 ;
- site 2 vers site 1 ;
- site 2 vers site 3 ;
- site 3 vers site 1 ;
- site 3 vers site 2.

Depuis le site 1, le ping vers le site 3 fonctionne :

![Ping du site 1 vers le site 3](../../assets/img/admin-reseau/it-3/ping%20site1-%3Esite3.png)

Depuis le site 2, les pings vers les sites 1 et 3 fonctionnent :

![Ping du site 2 vers les autres sites](../../assets/img/admin-reseau/it-3/ping%20site2%20vers%20les%20autres.png)

Depuis le site 3, le ping vers le site 1 fonctionne :

![Ping du site 3 vers le site 1](../../assets/img/admin-reseau/it-3/ping%20site3-%3Esite%201.png)

Les réponses ICMP prouvent que les routes existent dans les deux sens. Pour qu'un ping fonctionne, il faut l'aller et le retour : une route seulement dans un sens ne suffit pas.

### 3. Comptage des routes

Avec 3 sites, chaque routeur doit connaître les 2 LANs distants.

Calcul :

```text
3 routeurs x 2 routes distantes = 6 routes statiques au total
```

Formule générale :

```text
N sites x (N - 1) routes = nombre total de routes statiques
```

Donc :

| Nombre de sites | Routes par routeur | Total de routes statiques |
| --- | --- | --- |
| 2 sites | 1 | 2 |
| 3 sites | 2 | 6 |
| 4 sites | 3 | 12 |

Si un 4e site s'ajoute :

- chaque routeur existant doit ajouter 1 route vers le nouveau LAN ;
- le nouveau routeur doit ajouter 3 routes vers les anciens LANs ;
- on passe de 6 à 12 routes, donc 6 routes de plus au total.

C'est l'argument numérique qui motive le routage dynamique : plus le nombre de sites augmente, plus le routage statique devient lourd. Avec OSPF, les routeurs échangent automatiquement leurs réseaux et recalculent les chemins en cas de changement.
