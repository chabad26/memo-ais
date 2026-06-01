# Pense-bête Switching, ARP, VLANs et STP

---

## Switching

| Cas | Action du switch |
|---|---|
| MAC source vue | Ajout/maj dans la table MAC |
| MAC destination connue | Unicast vers le bon port |
| MAC destination inconnue | Flooding sauf port d'entrée |
| Broadcast | Flooding |

```bash
show mac address-table          # lire la table
clear mac address-table dynamic # vider et forcer le réapprentissage
```

---

## ARP

- Résout **IP -> MAC** sur un réseau local.
- Request = broadcast `ff:ff:ff:ff:ff:ff`.
- Reply = unicast vers le demandeur.

```bash
ip neigh show   # cache ARP Linux : REACHABLE / STALE / FAILED
```

---

## VLANs

- 1 VLAN = 1 domaine de broadcast isolé.
- Inter-VLAN = routeur ou switch L3.
- Access = 1 VLAN, trames non taguées, port utilisateur.
- Trunk = plusieurs VLANs, trames taguées 802.1Q, lien switch/switch ou switch/routeur.
- VID valide : **1 à 4094**.

```bash
switchport mode access
switchport access vlan 10

switchport mode trunk
switchport trunk allowed vlan 10,20
show interfaces trunk
```

---

## STP

- Évite les boucles de commutation en bloquant un lien redondant.
- Root Bridge = BID le plus bas.
- BID = priorité + VLAN + MAC.
- Priorité par défaut Cisco : `32768`, valeurs par multiples de `4096`.

| Rôle | État | À retenir |
|---|---|---|
| Root | `FWD` | Meilleur chemin vers le root |
| Designated | `FWD` | Port actif sur le segment |
| Alternate | `BLK` | Port bloqué |

- STP classique : ~30-50 s.
- Rapid STP : souvent < 5 s si activé sur les switches concernés.

```bash
show spanning-tree vlan 1
spanning-tree vlan 1 priority 4096
spanning-tree mode rapid-pvst
```

---

## Réflexes de diagnostic

| Symptôme | Vérifier |
|---|---|
| Un poste ne joint pas un autre poste local | IP, masque, cache ARP, table MAC |
| Trafic visible partout | Table MAC vide, broadcast, hub, mauvaise config |
| VLAN isolé malgré câblage correct | Mode access/trunk, VLAN autorisés, VLAN actif |
| Boucle ou réseau instable | `show spanning-tree vlan X`, root bridge, port bloqué |
