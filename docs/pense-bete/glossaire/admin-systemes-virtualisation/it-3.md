# Glossaire Virtualisation — Itération 3

## Sujet

Disponibilité des services virtualisés, cluster Proxmox VE imbriqué dans Hyper-V et stockage partagé NFS.

## Disponibilité et cluster

| Terme | Définition simple |
|---|---|
| **Disponibilité** | Capacité d'un service à rester accessible lorsqu'il est nécessaire. |
| **Haute disponibilité (HA)** | Ensemble de mécanismes réduisant l'interruption d'un service après une panne. |
| **Point unique de défaillance (SPOF)** | Composant unique dont la panne suffit à interrompre le service. |
| **Cluster** | Groupe de serveurs travaillant ensemble pour héberger et reprendre des services. |
| **Nœud** | Serveur physique membre d'un cluster. |
| **Basculement ou failover** | Redémarrage ou transfert automatique d'un service vers un nœud disponible après une panne. |
| **Retour arrière ou failback** | Retour contrôlé d'une charge vers son emplacement habituel après réparation. |
| **Heartbeat** | Messages réguliers échangés entre les nœuds pour vérifier qu'ils sont encore opérationnels. |
| **Quorum** | Mécanisme permettant au cluster de déterminer quelle partie peut continuer à fonctionner. |
| **Témoin ou witness** | Ressource supplémentaire participant au calcul du quorum sans héberger les VM. |
| **Split-brain** | Situation dangereuse où deux parties isolées d'un cluster se croient simultanément actives. |
| **Redondance** | Duplication d'un composant ou d'un chemin afin de résister à sa panne. |
| **Tolérance de panne** | Capacité à continuer de fonctionner malgré la défaillance d'un composant. |
| **Continuité de service** | Organisation permettant de maintenir les activités essentielles pendant un incident. |
| **Maintenance planifiée** | Intervention préparée pendant laquelle les charges peuvent être déplacées proprement. |
| **Panne imprévue** | Arrêt non planifié nécessitant une détection et une reprise automatiques. |
| **N+1** | Dimensionnement conservant la capacité d'un nœud supplémentaire pour supporter une panne. |
| **RTO** | Durée maximale acceptable pour rétablir un service après un incident. |
| **RPO** | Quantité maximale de données que l'entreprise accepte de perdre, exprimée en temps. |

## Proxmox et virtualisation

| Terme | Définition simple |
|---|---|
| **VMware ESXi** | Hyperviseur de type 1 installé directement sur un serveur physique. |
| **vSphere** | Ensemble des technologies VMware utilisées pour administrer une infrastructure virtualisée. |
| **vCenter Server** | Outil central qui administre plusieurs hôtes ESXi, clusters et machines virtuelles. |
| **Cluster vSphere** | Regroupement d'hôtes ESXi administrés ensemble dans vCenter. |
| **Proxmox VE** | Plateforme de virtualisation basée sur Linux utilisée ici pour créer un cluster pédagogique de trois nœuds. |
| **Virtualisation imbriquée** | Exécution d'un hyperviseur dans une machine virtuelle hébergée par un autre hyperviseur. |
| **Corosync** | Service utilisé par les nœuds Proxmox pour échanger leur état et gérer l'appartenance au cluster. |
| **pvecm** | Commande Proxmox utilisée pour créer, rejoindre et contrôler un cluster. |
| **pmxcfs** | Système de fichiers distribué Proxmox qui présente la configuration du cluster dans `/etc/pve`. |
| **pve-cluster** | Service qui démarre et maintient le système de fichiers de configuration Proxmox. |
| **alpesnetcluster** | Nom du cluster pédagogique regroupant `PVE1`, `PVE2` et `PVE3`. |
| **MAC spoofing Hyper-V** | Option autorisant une VM hyperviseur à transmettre les adresses MAC de ses propres VM imbriquées. |
| **vSphere HA** | Fonction qui redémarre les VM sur un autre hôte ESXi après une panne. |
| **vMotion** | Déplacement à chaud d'une VM en fonctionnement entre deux hôtes ESXi. |
| **Storage vMotion** | Déplacement à chaud des fichiers d'une VM vers un autre datastore. |
| **DRS** | Fonction qui recommande ou automatise le placement des VM selon la charge des hôtes. |
| **VMkernel** | Couche système d'ESXi et nom des interfaces utilisées pour la gestion, vMotion ou le stockage. |
| **Interface VMkernel** | Interface IP technique d'un hôte ESXi dédiée à un type de trafic. |
| **VMDK** | Format de disque virtuel principalement utilisé par VMware. |
| **Datastore** | Espace logique dans lequel ESXi stocke les fichiers des machines virtuelles. |
| **VMFS** | Système de fichiers VMware conçu pour les datastores sur stockage bloc partagé. |
| **Port group** | Ensemble de ports virtuels partageant une configuration réseau, par exemple un VLAN. |
| **vSwitch** | Commutateur logiciel reliant les VM et les interfaces VMkernel au réseau physique. |

## Stockage partagé

| Terme | Définition simple |
|---|---|
| **Stockage local** | Disques directement installés dans un hôte et normalement accessibles uniquement par lui. |
| **Stockage partagé** | Espace de stockage accessible par plusieurs hyperviseurs. |
| **Stockage bloc** | Stockage présenté au serveur comme un disque composé de blocs, par exemple avec iSCSI ou Fibre Channel. |
| **Stockage fichier** | Stockage présenté sous forme de partage de fichiers, par exemple avec NFS ou SMB. |
| **Baie de stockage** | Équipement regroupant des disques, contrôleurs et interfaces afin de fournir du stockage aux serveurs. |
| **SAN** | Réseau spécialisé donnant accès à du stockage en mode bloc. |
| **NAS** | Serveur ou équipement fournissant des fichiers partagés sur le réseau. |
| **LUN** | Volume logique présenté par une baie à un ou plusieurs serveurs. |
| **Capacité brute** | Somme de la capacité physique de tous les disques avant protection et réserves. |
| **Capacité utile** | Espace réellement disponible après RAID, réplication et réserves système. |
| **RAID** | Organisation de plusieurs disques visant la performance et/ou la tolérance aux pannes. |
| **Contrôleur de stockage** | Composant qui pilote les disques, le cache, les volumes et leurs accès. |
| **Chemin de stockage** | Liaison réseau ou matérielle reliant un hôte à la baie. |
| **Latence** | Temps nécessaire pour effectuer une opération de lecture ou d'écriture. |
| **Débit** | Quantité de données transférée par seconde. |
| **IOPS** | Nombre d'opérations de lecture ou d'écriture traitées par seconde. |
| **Réplication** | Copie des données vers un autre équipement ou site afin d'améliorer leur disponibilité. |

## Protocoles et accès au stockage

| Terme | Définition simple |
|---|---|
| **iSCSI** | Protocole transportant des commandes de stockage SCSI sur un réseau IP/Ethernet. |
| **Initiateur iSCSI** | Client installé sur l'hyperviseur qui se connecte à la cible de stockage. |
| **Cible iSCSI** | Ressource de la baie qui présente un ou plusieurs LUN aux initiateurs autorisés. |
| **Portail iSCSI** | Adresse IP et port permettant de découvrir et joindre une cible iSCSI. |
| **IQN** | Identifiant unique d'un initiateur ou d'une cible iSCSI. |
| **CHAP** | Méthode d'authentification par secret utilisée lors d'une connexion iSCSI. |
| **MPIO** | Gestion de plusieurs chemins entre un serveur et le même stockage pour la redondance ou la performance. |
| **Fibre Channel (FC)** | Technologie de réseau de stockage bloc utilisant des équipements spécialisés. |
| **HBA** | Carte matérielle reliant un serveur à un réseau de stockage, notamment Fibre Channel. |
| **FCoE** | Transport de Fibre Channel sur un réseau Ethernet compatible. |
| **NFS** | Protocole utilisé dans le laboratoire pour présenter le même stockage aux trois nœuds Proxmox. |
| **SMB 3** | Protocole Microsoft de partage de fichiers pouvant héberger des VM Hyper-V. |
| **Storage Spaces Direct (S2D)** | Technologie Microsoft regroupant et répliquant les disques locaux de plusieurs nœuds. |

## Termes propres au cluster Hyper-V

Ces termes apparaissent dans la documentation précédente et servent à comprendre l'équivalence avec VMware.

| Terme | Définition simple |
|---|---|
| **Failover Clustering** | Fonction Windows Server permettant de créer un cluster de basculement. |
| **CSV** | *Cluster Shared Volume*, volume partagé accessible simultanément par les nœuds Hyper-V. |
| **Live Migration** | Équivalent Hyper-V de vMotion : déplacement à chaud d'une VM. |
| **VHDX** | Format de disque virtuel utilisé par Hyper-V. |

## Réseaux de l'infrastructure

| Terme | Définition simple |
|---|---|
| **Réseau de gestion** | Réseau utilisé pour administrer les hyperviseurs, vCenter et les équipements. |
| **Réseau de stockage** | Réseau réservé aux échanges entre les hyperviseurs et la baie. |
| **Réseau vMotion** | Réseau utilisé pour transférer l'état et la mémoire des VM lors d'une migration. |
| **Réseau des VM** | Réseau transportant les communications des services hébergés dans les VM. |
| **VLAN** | Séparation logique de plusieurs réseaux sur une même infrastructure physique. |
| **Route statique** | Chemin ajouté manuellement pour atteindre un réseau distant. |
| **Passerelle** | Routeur utilisé pour joindre les réseaux situés hors du sous-réseau local. |

## À ne pas confondre

| Notions | Différence essentielle |
|---|---|
| HA et tolérance de panne sans interruption | HA redémarre généralement la VM après une panne ; une courte interruption reste possible. |
| vMotion et vSphere HA | vMotion déplace une VM pendant une maintenance ; HA la redémarre après une panne. |
| Datastore et LUN | Le LUN est le volume présenté par la baie ; le datastore est l'espace exploité par ESXi dessus. |
| SAN et NAS | Le SAN fournit généralement des blocs ; le NAS fournit des fichiers. |
| RAID et sauvegarde | Le RAID maintient le stockage après certaines pannes de disque ; la sauvegarde permet de restaurer des données perdues ou supprimées. |
| Stockage partagé et sauvegarde | Le stockage partagé facilite migration et HA ; il ne protège pas contre la corruption ou la suppression. |
| Checkpoint et réplication | Le checkpoint conserve un état local temporaire ; la réplication copie les données vers une autre destination. |
| Migration et basculement | La migration est planifiée ; le basculement répond à une panne ou une indisponibilité. |

## Repère AlpesNet

```text
LABO_CORE — Hyper-V — 10.42.0.2
    │
    ├─ PVE1 — 10.42.0.131
    ├─ PVE2 — 10.42.0.132
    ├─ PVE3 — 10.42.0.133
    └─ NFS1 — Debian/NFS — 10.42.0.134
```

## Documents associés

- [Vue d'ensemble de l'itération 3](../../../admin-systemes-virtualisation/it-3/index.md)
- [Installer trois Proxmox dans Hyper-V](../../../admin-systemes-virtualisation/it-3/installer-trois-proxmox-dans-hyper-v.md)
- [Partager le stockage entre plusieurs hyperviseurs](../../../admin-systemes-virtualisation/it-3/comment-partager-le-stockage-entre-plusieurs-hyperviseurs.md)
- [Créer et valider le cluster Proxmox](../../../admin-systemes-virtualisation/it-3/comment-creer-un-cluster-proxmox.md)
- [Assurer automatiquement la continuité de service](../../../admin-systemes-virtualisation/it-3/comment-assurer-la-haute-disponibilite.md)
