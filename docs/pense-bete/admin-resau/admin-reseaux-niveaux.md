# Schémas réseau L1 / L2 / L3

Un schéma réseau professionnel peut représenter plusieurs niveaux. Il faut savoir les distinguer pour ne pas mélanger câbles, VLAN et routage dans une seule vue confuse.

## Distinction des niveaux

| Niveau | Ce qu'on représente | Questions auxquelles il répond |
| --- | --- | --- |
| L1 physique | Câbles, ports, baies, équipements, liens physiques | Qui est branché où ? Sur quel port ? |
| L2 liaison | Switchs, VLAN, trunks, accès, adresses MAC | Quels équipements sont dans le même domaine de broadcast ? |
| L3 réseau | Sous-réseaux IP, passerelles, routeurs, interfaces routées | Qui route entre les réseaux ? Quelle passerelle utiliser ? |

## L1 — Physique

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

## L2 — Liaison

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

## L3 — Réseau

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

## Réflexe de lecture

Quand tu regardes un schéma, demande-toi :

1. **L1** : le câble existe-t-il et relie-t-il les bons ports ?
2. **L2** : les VLAN et trunks permettent-ils au trafic d'arriver au bon domaine ?
3. **L3** : les IP, passerelles et routes permettent-elles de joindre le bon réseau ?

!!! tip "Phrase à garder"
    L1 connecte physiquement, L2 sépare ou regroupe avec les VLAN, L3 permet de passer d'un réseau IP à un autre.
