# Synthèse — VLANs (IEEE 802.1Q)

---

## 1. Pourquoi utiliser des VLANs ?

Sans VLANs, tous les équipements d'un switch partagent le même **domaine de broadcast** :

- Un ARP Request touche **toutes** les machines
- Une machine compromise peut intercepter le trafic de n'importe qui sur le segment

> **Exemple concret :** sur un switch 48 ports sans VLANs, un poste du service marketing peut voir les requêtes ARP, certaines requêtes DNS et des flux non chiffrés provenant d'autres services.

### Ce que les VLANs apportent

| Problème sans VLAN | Solution avec VLAN |
| --- | --- |
| Un seul domaine de broadcast pour tous | Chaque VLAN = domaine de broadcast **isolé** |
| Toute machine peut sniffer le réseau | Isolation logique du trafic |
| Segmentation impossible sans matériel séparé | Segmentation **logique** sur un seul switch physique |
| Communication libre entre tous les hôtes | Inter-VLAN uniquement via **routeur** ou **switch L3** |

---

## 2. Port Access — connexion d'un équipement terminal

Un port **access** appartient à **un seul VLAN**. Les trames circulent **sans tag 802.1Q** — l'équipement terminal (PC, imprimante…) n'a pas besoin de connaître le VLAN.

```text
PC-Admin ──── port Gi0/1 (access, VLAN 10) ──── SW1
```

### Configuration Cisco IOS

```bash
SW1(config)# interface GigabitEthernet0/1
SW1(config-if)# switchport mode access
SW1(config-if)# switchport access vlan 10
SW1(config-if)# description "PC-Admin-01"
SW1(config-if)# exit
```

### Résumé port Access

| Caractéristique | Valeur |
| --- | --- |
| Nombre de VLANs transportés | **1** |
| Tag 802.1Q sur les trames | **Non** |
| Équipements connectés typiques | PC, imprimante, téléphone IP |
| L'équipement doit connaître son VLAN | **Non** |

---

## 3. Port Trunk — transport de plusieurs VLANs

Un port **trunk** transporte **plusieurs VLANs simultanément** en ajoutant un tag 802.1Q aux trames. On l'utilise entre switches, ou entre un switch et un routeur.

```text
SW1 ──── port Gi0/0 (trunk, VLANs 10+20) ──── R1 (ou SW2)
```

### Le tag 802.1Q

Quand une trame traverse un port trunk, **4 octets** sont insérés dans le header Ethernet :

```text
Trame originale : [DST MAC][SRC MAC][Type (0x0800)][Données][FCS]

Trame taguée :   [DST MAC][SRC MAC][0x8100][TCI][Type (0x0800)][Données][FCS]
                                      ↑      ↑
                                    TPID    TCI = PCP (3 bits) + DEI (1 bit) + VID (12 bits)
                                  (802.1Q)                                       ↑
                                                                          VLAN ID (1–4094)
```

| Champ | Taille | Rôle |
| --- | --- | --- |
| **TPID** `0x8100` | 16 bits | Identifie la trame comme taguée 802.1Q |
| **PCP** | 3 bits | Priorité (QoS) |
| **DEI** | 1 bit | Drop Eligible Indicator |
| **VID** | 12 bits | VLAN ID — de **1 à 4094** |

### Configuration Cisco IOS d'un trunk

```bash
SW1(config)# interface GigabitEthernet0/0
SW1(config-if)# switchport trunk encapsulation dot1q
SW1(config-if)# switchport mode trunk
SW1(config-if)# switchport trunk allowed vlan 10,20
SW1(config-if)# description "Trunk vers R1"
SW1(config-if)# exit
```

### Vérification

```bash
SW1# show interfaces trunk

Port        Mode         Encapsulation  Status        Native vlan
Gi0/0       on           802.1q         trunking      1

Port        Vlans allowed on trunk
Gi0/0       10,20

Port        Vlans allowed and active in management domain
Gi0/0       10,20
```

### Résumé port Trunk

| Caractéristique | Valeur |
| --- | --- |
| Nombre de VLANs transportés | **Plusieurs** |
| Tag 802.1Q sur les trames | **Oui** |
| Équipements connectés typiques | Switch, routeur, serveur multi-VLAN |
| L'équipement doit gérer les tags | **Oui** |

---

## 4. Comparatif Access vs Trunk

| Critère | Port Access | Port Trunk |
| --- | --- | --- |
| VLANs transportés | 1 seul | Plusieurs |
| Trames taguées | Non | Oui (802.1Q) |
| Usage typique | PC, imprimante | Switch↔Switch, Switch↔Routeur |
| Connaissance VLAN côté équipement | Inutile | Nécessaire |
| Commande IOS | `switchport mode access` | `switchport mode trunk` |

---

## 5. Schéma d'ensemble

```text
                        ┌─────────────────────────────┐
                        │            SW1              │
  PC-Admin (VLAN 10) ───┤ Gi0/1 [access VLAN 10]      │
  PC-RH    (VLAN 20) ───┤ Gi0/2 [access VLAN 20]      │
  PC-DSI   (VLAN 10) ───┤ Gi0/3 [access VLAN 10]      │
                        │ Gi0/0 [trunk VLANs 10+20] ──┼──── R1 (routeur inter-VLAN)
                        └─────────────────────────────┘

  VLAN 10 (Admin/DSI)  ←── domaine de broadcast isolé
  VLAN 20 (RH)         ←── domaine de broadcast isolé
  Communication inter-VLAN uniquement via R1
```

---

***Sources : IEEE 802.1Q · Cisco VLAN Configuration Guide · ANSSI — sécurisation des réseaux locaux***
