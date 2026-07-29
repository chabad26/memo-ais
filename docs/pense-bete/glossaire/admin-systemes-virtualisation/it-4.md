# Glossaire Virtualisation — Itération 4

## Sujet

Exploitation d'une infrastructure virtualisée : segmentation réseau, sécurité des communications, diagnostic, optimisation des performances, sauvegardes et transmission à une autre équipe.

## Termes à retenir

| Terme | Définition simple |
| --- | --- |
| **Segmentation réseau** | Découpage du réseau en zones séparées selon les rôles et les niveaux de confiance. |
| **VLAN** | Réseau logique isolé sur une même infrastructure physique. |
| **Bridge VLAN-aware** | Bridge capable de transporter et d'appliquer des tags VLAN. |
| **Tag VLAN** | Identifiant numérique associé à une trame réseau pour indiquer son VLAN. |
| **Trunk** | Lien transportant plusieurs VLAN entre équipements. |
| **DMZ** | Zone exposée contrôlée, souvent utilisée pour les services web. |
| **Réseau de management** | Réseau réservé à l'administration des hyperviseurs et consoles. |
| **Réseau de stockage** | Réseau réservé aux échanges entre hyperviseurs et stockage partagé. |
| **Réseau cluster** | Réseau utilisé pour les messages internes de quorum, HA ou Corosync. |
| **Matrice de flux** | Tableau listant source, destination, ports, protocole et décision de filtrage. |
| **Moindre privilège réseau** | Autoriser uniquement les communications nécessaires. |
| **Surengagement** | Attribution de plus de ressources virtuelles que la capacité réellement disponible. |
| **Contention CPU** | Attente des VM parce que les processeurs physiques sont trop sollicités. |
| **Pression mémoire** | Manque de RAM provoquant swap, lenteurs ou arrêt de processus. |
| **Latence stockage** | Temps de réponse du stockage pour lire ou écrire des données. |
| **IOPS** | Nombre d'opérations d'entrée/sortie par seconde. |
| **Métrique** | Mesure technique permettant de suivre l'état ou les performances. |
| **Journal d'exploitation** | Trace des actions, incidents et changements. |
| **Dossier de transmission** | Documentation permettant à une autre équipe de reprendre l'infrastructure. |
| **SPOF** | Point unique de défaillance. |

## Manipulations faites

| Action | Commandes ou contrôles |
| --- | --- |
| Identifier les bridges | `ip -br link show type bridge` |
| Lire la configuration réseau Proxmox | `cat /etc/network/interfaces` |
| Vérifier la carte d'une VM | `qm config 100 | grep '^net'` |
| Activer ou vérifier le VLAN d'une VM | `qm config 100` puis contrôle du tag réseau |
| Contrôler les VLAN du bridge | `bridge vlan show` |
| Lister les VM | `qm list` |
| Lister les conteneurs | `pct list` |
| Vérifier le cluster | `pvecm status`, `pvecm nodes` |
| Vérifier les stockages | `pvesm status`, `df -h`, `findmnt -t nfs,nfs4` |
| Vérifier la mémoire | `free -h`, `swapon --show` |
| Mesurer l'activité | `vmstat 2 30` |
| Vérifier les services en échec | `systemctl --failed` |
| Relever les logs | `journalctl --since "-24 hours"` |
| Documenter l'inventaire | noms, IP, versions, VM, vCPU, RAM, disques, réseaux |

## Zones réseau à connaître

| Zone | Usage | Exemple de flux |
| --- | --- | --- |
| `MGMT` | Administration Proxmox, Hyper-V, vCenter | HTTPS, SSH/RDP si justifié |
| `CLUSTER` | Quorum, HA, Corosync | Entre hyperviseurs uniquement |
| `STORAGE` | Accès NFS, iSCSI ou datastore | Hôtes vers stockage |
| `DMZ` | VM exposée, par exemple `WEB1` | HTTP/HTTPS |
| `SERVERS` | Services internes | AD, DNS, fichiers, supervision |
| `CLIENTS` | Postes utilisateurs | Accès applicatifs nécessaires |

## Repère AlpesNet

```text
LABO_CORE
  └─ Hyper-V
      ├─ PVE1 10.42.0.131
      ├─ PVE2 10.42.0.132
      ├─ PVE3 10.42.0.133
      ├─ NFS1 10.42.0.134
      └─ WEB1 10.42.0.125 environ, VM applicative de test
```

!!! warning "Limite du laboratoire"
    Les nœuds Proxmox et le stockage NFS sont imbriqués dans le même hôte Hyper-V `LABO_CORE`. Cela valide les mécanismes logiques, mais pas la résistance à une panne physique de l'hôte.

## À ne pas confondre

| Notions | Différence essentielle |
| --- | --- |
| VLAN et pare-feu | Le VLAN sépare les domaines de niveau 2 ; le pare-feu décide quels flux passent entre zones. |
| Monitoring et optimisation | Mesurer ne corrige pas ; l'optimisation doit être décidée à partir des métriques. |
| Stockage partagé et sauvegarde | Le stockage partagé aide la migration/HA ; il ne protège pas contre suppression ou corruption. |
| HA logique et HA physique | Un cluster imbriqué sur un seul hôte ne résiste pas à la panne de cet hôte. |
| Snapshot et sauvegarde | Le snapshot est temporaire ; la sauvegarde doit pouvoir être restaurée indépendamment. |
| Migration planifiée et reprise incident | La migration est contrôlée ; la HA intervient après panne ou perte d'hôte. |

## Preuves utiles pour SYS-01c

| Preuve | Utilité |
| --- | --- |
| Schéma architecture | Montrer hôtes, cluster, réseaux, stockages et VM |
| Inventaire VM | Justifier vCPU, RAM, disque, réseau et rôle |
| Matrice de flux | Prouver l'isolation et le moindre privilège |
| Capture performance | CPU, mémoire, stockage, réseau avant/après ajustement |
| Résultat sauvegarde/restauration | Prouver que la sauvegarde est réellement exploitable |
| Dossier de transmission | Permettre la reprise par une autre équipe |

## Docs associées

- [Vue d'ensemble de l'itération 4](../../../admin-systemes-virtualisation/it-4/index.md)
- [Sécuriser les communications entre les VM](../../../admin-systemes-virtualisation/it-4/comment-securiser-les-communications-entre-les-machines-virtuelles.md)
- [Identifier l'origine d'un dysfonctionnement](../../../admin-systemes-virtualisation/it-4/comment-identifier-origine-dysfonctionnement.md)
- [Optimiser les performances](../../../admin-systemes-virtualisation/it-4/comment-optimiser-performances-infrastructure-virtualisee.md)
- [Transmettre l'infrastructure à une autre équipe](../../../admin-systemes-virtualisation/it-4/comment-transmettre-infrastructure-autre-equipe.md)
