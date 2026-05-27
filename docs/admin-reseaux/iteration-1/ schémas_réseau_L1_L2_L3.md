# Schémas réseau L1 / L2 / L3

## 1 · Les trois niveaux de représentation

| Niveau | Représente |
| --- | --- |
| L1 — Physique | Équipements nommés, liaisons physiques, numéros d'interface, types de câble |
| L2 — Liaison | VLAN, type de port access/trunk, domaine de broadcast, root bridge STP |
| L3 — Réseau | Adresses IP, masques CIDR, passerelles, délimitation des sous-réseaux |

### L1 — Physique

Le niveau L1 répond à la question : **qui est branché où ?**

À faire apparaître :

- noms des équipements ;
- ports physiques utilisés ;
- liaisons entre équipements ;
- type de câble si nécessaire ;
- emplacement physique si utile : baie, salle, bureau.

Exemple :

```text
PC-ADM-01 eth0 -> SW-ACC-01 Gi0/3
SW-ACC-01 Gi0/24 -> R1 Gi0/0
```

### L2 — Liaison

Le niveau L2 répond à la question : **qui partage le même domaine de broadcast ?**

À faire apparaître :

- VLAN ;
- ports access ;
- ports trunk ;
- domaines de broadcast ;
- root bridge STP si le protocole STP est étudié ou utilisé.

Exemple :

```text
VLAN 10 Administration
VLAN 20 Production
VLAN 30 Serveurs
VLAN 40 DMZ
Port Gi0/3 : access VLAN 10
Port Gi0/24 : trunk VLAN 10,20,30,40
```

### L3 — Réseau

Le niveau L3 répond à la question : **comment les sous-réseaux communiquent-ils entre eux ?**

À faire apparaître :

- adresses IP des interfaces actives ;
- masques CIDR ;
- passerelles ;
- sous-réseaux ;
- routeur ou équipement qui assure le routage ;
- routes si elles sont nécessaires à la compréhension.

Exemple :

```text
Administration : 192.168.10.64/27  GW 192.168.10.65
Production     : 192.168.10.0/26   GW 192.168.10.1
Serveurs       : 192.168.10.96/28  GW 192.168.10.97
DMZ            : 192.168.10.112/29 GW 192.168.10.113
```

## 2 · Ce qui doit toujours être présent

Un schéma réseau rendu comme livrable doit toujours contenir :

- le nom de chaque équipement ;
- les adresses IP de toutes les interfaces actives ;
- les masques CIDR ;
- la passerelle par défaut de chaque segment ;
- les VLAN si le schéma contient du L2 ;
- les numéros d'interface si le schéma contient du L1 ;
- une légende si des couleurs, icônes ou types de traits sont utilisés.

Tableau de contrôle :

| Élément | Obligatoire ? | Pourquoi |
| --- | --- | --- |
| Nom des équipements | Oui | Identifier précisément chaque élément |
| Interfaces | Oui en L1/L3 | Savoir où brancher et quoi configurer |
| VLAN | Oui en L2 | Comprendre les domaines de broadcast |
| IP et CIDR | Oui en L3 | Configurer et diagnostiquer le routage |
| Passerelle | Oui | Savoir comment sortir du segment |
| Légende | Recommandée | Rendre le schéma lisible par quelqu'un d'autre |

## 3 · Le seuil professionnel

!!! warning "Livrable professionnel"
    Un schéma sans adressage complet ou sans nommage n'est pas un livrable professionnel.

Un schéma professionnel doit permettre à une autre personne de comprendre l'infrastructure sans explication orale.

Avant de rendre un schéma, vérifier :

1. Chaque équipement a un nom.
2. Chaque lien important a ses interfaces indiquées.
3. Chaque réseau IP est écrit avec son CIDR.
4. Chaque segment possède une passerelle.
5. Les VLAN sont visibles si le schéma représente la couche L2.
6. Le schéma distingue clairement L1, L2 et L3, ou précise qu'il s'agit d'une vue mixte.

## Ressources

- draw.io : <https://app.diagrams.net>
- LibreOffice Draw : `libreoffice --draw`
- Icônes Cisco : <https://www.cisco.com/c/en/us/about/brand-center/network-topology-icons.html>

## Compétences

- Produire un schéma réseau annoté L1/L2/L3 — CA-03.
