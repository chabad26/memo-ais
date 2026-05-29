# Synthèse — Schéma réseau AlpesNet

**Date** : 28/05/2026  
**Objectif** : Concevoir une topologie réseau multi-VLAN avec routeur central séparant 4 domaines isolés.

## Topologie réseau

```text
Internet → R1 (Routeur IOSv) 
         ↙           ↘
      SW1              SW2
    (Switch)         (Switch)
    ↙      ↘         ↙      ↘
PC-Admin PC-Prod  PC-Serv1 PC-DMZ1
```

## Concept clé : VLAN (Virtual LAN)

Un **VLAN** segmente logiquement un switch en domaines isolés. Les machines d'un VLAN ne communiquent qu'à travers le routeur.

**4 VLANs** :

- **VLAN 10** (Admin) : PC-Admin, subnet `/27`
- **VLAN 20** (Prod) : PC-Prod, subnet `/26`
- **VLAN 30** (Serveurs) : PC-Serv1, subnet `/28`
- **VLAN 40** (DMZ) : PC-DMZ1, subnet `/29`

## Types de ports (L2)

| Mode | Rôle | Exemple |
| --- | --- | --- |
| **access** | Relie un hôte à un VLAN unique | `Gi0/1 access VLAN 10` |
| **trunk** | Relie deux équipements réseau, **transporte tous les VLANs** | `Gi0/24 trunk (10,20,30,40)` |

⚠️ Important : un port **access** = 1 VLAN, un port **trunk** = tous les VLANs passent.

## Configuration appliquée

**SW1** :

- `Gi0/1` : access VLAN 10 → PC-Admin
- `Gi0/2` : access VLAN 20 → PC-Prod
- `Gi0/24` : **trunk** → R1 (transporte VLAN 10,20,30,40)

**SW2** :

- `Gi0/1` : access VLAN 30 → PC-Serv1
- `Gi0/2` : access VLAN 40 → PC-DMZ1
- `Gi0/24` : **trunk** → R1 (transporte VLAN 10,20,30,40)

**R1** (routeur, L3) :

- `Gi0/0` : `192.168.10.65/27` → Gateway VLAN 10
- `Gi0/1` : `192.168.10.1/26` → Gateway VLAN 20

## Adressage IP (L3)

| Équipement | VLAN | IP | Masque | Sous-réseau |
| --- | --- | --- | --- | --- |
| PC-Admin | 10 | `192.168.10.66` | `/27` | `192.168.10.64/27` |
| PC-Prod | 20 | `192.168.10.2` | `/26` | `192.168.10.0/26` |
| PC-Serv1 | 30 | `192.168.10.98` | `/28` | `192.168.10.96/28` |
| PC-DMZ1 | 40 | `192.168.10.114` | `/29` | `192.168.10.112/29` |

**Passerelle par VLAN** = interface du routeur de ce VLAN (ex: pour VLAN 10 → `.65`).

## Diagramme DrawIO

Fichier complet : `/docs/admin-reseaux/iteration-1/drawio/AlpesNet-L1L2L3.drawio`

Couvre 3 niveaux :

- **L1** (Physique) : équipements et liaisons avec numéros de port
- **L2** (Liaison) : configuration des VLANs et types de ports
- **L3** (Réseau) : adressage IP et passerelles
