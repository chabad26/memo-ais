# Pense-bête — Switching, ARP, VLANs & STP

---

## Switching & Table MAC

- **Hub** → flood tout sur tous les ports · **Switch** → forward uniquement vers la destination
- Le switch **apprend** la MAC source de chaque trame reçue → CAM Table (TTL ~300s)
- **MAC inconnue** → flooding · **MAC connue** → unicast · **Broadcast** → toujours floodé

```bash
show mac address-table          # lire la table
clear mac address-table dynamic # vider (force réapprentissage)
```

---

## ARP

- Résout **IP → MAC** avant toute communication locale (couche 2)
- **ARP Request** = broadcast `ff:ff:ff:ff:ff:ff` → floodé par le switch
- **ARP Reply** = unicast vers le demandeur → le switch apprend la MAC au passage

```bash
ip neigh show   # cache ARP Linux  |  REACHABLE / STALE / FAILED
```

---

## VLANs (802.1Q)

- 1 VLAN = 1 domaine de broadcast isolé · inter-VLAN uniquement via routeur ou switch L3
- **Port Access** → 1 VLAN, trames **non taguées**, pour PC/imprimante
- **Port Trunk** → plusieurs VLANs, trames **taguées** (4 octets insérés : TPID `0x8100` + VID 12 bits), pour liens switch↔switch ou switch↔routeur
- VID : valeurs **1 à 4094**

```bash
switchport mode access / switchport access vlan 10
switchport mode trunk  / switchport trunk allowed vlan 10,20
show interfaces trunk
```

---

## STP (802.1D / Rapid 802.1w)

- Évite les **boucles de commutation** en bloquant les ports redondants
- **Root Bridge** = switch avec la priorité la plus basse (défaut `32768`) · ex-æquo → MAC la plus basse gagne
- **BID** = Priorité + VLAN + MAC · priorité toujours **multiple de 4096**

| Rôle port | État | Description |
|---|---|---|
| Designated | `FWD` | Port actif sur le segment |
| Root | `FWD` | Meilleur chemin vers le root bridge |
| Alternate | `BLK` | Port bloqué — casse la boucle |

- **STP classique** : reconvergence ~30-50s (Listening 15s + Learning 15s)
- **Rapid STP** : reconvergence < 5s (négociation active entre switches)

```bash
show spanning-tree vlan 1
spanning-tree vlan 1 priority 4096   # forcer l'élection d'un root bridge
spanning-tree mode rapid-pvst        # activer Rapid STP (sur TOUS les switches)
```
