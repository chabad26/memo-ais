# Synthèse — Switching, ARP & STP

---

## 1. Hub vs Switch

| Critère | Hub | Switch |
|---|---|---|
| **Fonctionnement** | Retransmet sur **tous** les ports | Retransmet uniquement vers le port de **destination** |
| **Collisions** | Fréquentes (domaine de collision partagé) | Éliminées (domaine par port) |
| **Bande passante** | Partagée entre toutes les machines | Dédiée par port |
| **Sécurité** | Toute machine peut écouter tout le trafic | Trafic isolé par destination |
| **Intelligence** | Aucune | Apprentissage des adresses MAC |

---

## 2. Table MAC (CAM Table)

Le switch maintient une table qui associe chaque **adresse MAC** à un **port physique**.

### Apprentissage dynamique

1. Une trame arrive sur le port 3, avec MAC source `AA:BB:CC:DD:EE:01`
2. Le switch enregistre : *"cette MAC est accessible sur le port 3"*
3. L'entrée a un **TTL ~300 s** — elle expire si la machine ne se manifeste plus

### Décision de commutation

| Situation | Action du switch |
|---|---|
| MAC de destination **connue** | Envoi uniquement sur le port associé (**unicast / forwarding**) |
| MAC de destination **inconnue** | Envoi sur tous les ports sauf celui d'arrivée (**flooding**) |
| MAC de destination **broadcast** `FF:FF:FF:FF:FF:FF` | **Toujours floodé** sur tous les ports |

### Commandes Cisco IOS utiles

```bash
# Afficher la table MAC
SW1# show mac address-table

# Afficher les compteurs
SW1# show mac address-table count

# Vider la table (force le réapprentissage)
SW1# clear mac address-table dynamic
```

---

## 3. ARP (Address Resolution Protocol)

> **Rôle :** résoudre une adresse IP en adresse MAC avant la première communication locale.  
> **Couche :** Couche 2 (Accès réseau — modèle TCP/IP)

### Ce que voit le switch

| Trame ARP | Ce que fait le switch |
|---|---|
| **ARP Request** (broadcast `FF:FF:FF:FF:FF:FF`) | Flood sur tous les ports |
| **ARP Reply** (unicast vers le demandeur) | Apprend la MAC source, met à jour sa table |

### États du cache ARP (Linux)

| État | Signification |
|---|---|
| `REACHABLE` | Entrée récemment utilisée et vérifiée |
| `STALE` | En cache, mais non vérifiée récemment |
| `FAILED` | Tentative de résolution échouée |

### Commandes Ubuntu utiles

```bash
# Voir le cache ARP
arp -a
ip neigh show

# Forcer une résolution ARP
ping -c 1 192.168.10.1
ip neigh show    # l'entrée passe à REACHABLE
```

---

## 4. STP — Spanning Tree Protocol (IEEE 802.1D)

### Problème : les boucles de commutation

Avec plusieurs switches interconnectés (redondance), il peut exister plusieurs chemins → **boucle de commutation** → tempête de broadcast → réseau saturé en quelques secondes.

### Solution STP en 3 étapes

1. **Élection du Root Bridge** — le switch avec la priorité la plus basse (défaut : `32768` sur Cisco IOS) devient la racine
2. **Calcul du chemin de coût minimal** — chaque switch choisit le chemin le moins coûteux vers le root bridge
3. **Blocage des ports redondants** — les ports créant des boucles sont mis en état `Blocking`

> **BID (Bridge ID)** = Priorité (16 bits) + VLAN (12 bits) + Adresse MAC (48 bits)

### États des ports STP

| État | Description | Durée |
|---|---|---|
| **Blocking** | N'envoie pas de données, écoute les BPDUs | Jusqu'à panne détectée |
| **Listening** | Prépare la transition, n'apprend pas les MACs | 15 s |
| **Learning** | Apprend les MACs, n'envoie pas encore de données | 15 s |
| **Forwarding** | Fonctionnement normal — envoie et reçoit | Indéfini |
| **Disabled** | Désactivé administrativement | — |

### Rôles des ports STP

| Rôle | Description |
|---|---|
| **Root Port** (`Root`) | Port le plus proche du Root Bridge |
| **Designated Port** (`Desg`) | Port actif en forwarding sur un segment |
| **Alternate Port** (`Altn`) | Port bloqué — redondant |

### Commande Cisco IOS utile

```bash
SW1# show spanning-tree vlan 1
```

---

## Résumé visuel du flux d'une trame

```
Machine A envoie une trame à Machine B
        │
        ▼
Switch reçoit la trame sur le port d'entrée
        │
        ├─ Apprend la MAC source → mise à jour table MAC
        │
        └─ Cherche la MAC destination dans la table
              │
              ├─ Connue   → forwarding (unicast vers le bon port)
              └─ Inconnue → flooding (tous les ports sauf source)
                  └─ Broadcast → flooding systématique
```

---

*Sources : RFC 826 (ARP) · IEEE 802.1D (STP) · Cisco IOS documentation*
