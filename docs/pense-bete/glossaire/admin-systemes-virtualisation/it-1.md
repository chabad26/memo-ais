# Glossaire Virtualisation — Itération 1

## Sujet

Fondamentaux de la virtualisation, fonctionnement d'une machine virtuelle, partage des ressources et haute disponibilité.

## Infrastructure et composants

| Terme | Définition courte |
|---|---|
| Virtualisation | Création de ressources informatiques logiques à partir de ressources physiques. |
| Hôte | Serveur physique qui fournit ses ressources aux machines virtuelles. |
| Hyperviseur | Couche logicielle qui crée, exécute, isole et administre les VM. |
| Hyperviseur de type 1 | Hyperviseur exécuté directement sur le matériel, adapté à la production. |
| Hyperviseur de type 2 | Application de virtualisation exécutée sur un système d'exploitation hôte. |
| Machine virtuelle (VM) | Ordinateur logiciel isolé possédant des ressources virtuelles et son propre OS. |
| Système d'exploitation hôte | OS installé sur la machine physique, partagé par les conteneurs ou accueillant un hyperviseur de type 2. |
| Système d'exploitation invité | OS installé et exécuté à l'intérieur d'une machine virtuelle. |
| VMM | *Virtual Machine Manager*, composant chargé de gérer les machines virtuelles. |
| Cluster | Ensemble d'hôtes associés pour améliorer la disponibilité et répartir les charges. |
| Nœud de cluster | Serveur ou équipement membre d'un cluster. |
| Espace de stockage virtualisé (datastore) | Espace logique regroupant le stockage utilisé par les machines virtuelles. |
| Conteneur | Environnement isolé qui partage le noyau du système hôte. |
| Conteneurisation | Empaquetage et exécution d'une application isolée avec ses dépendances. |
| Moteur de conteneurs | Logiciel qui crée et exécute des conteneurs à partir d'images. |
| Image de conteneur | Modèle immuable contenant une application, ses dépendances et ses métadonnées. |
| Orchestrateur | Plateforme automatisant le déploiement, la disponibilité et la mise à l'échelle des conteneurs. |
| VDI | Infrastructure fournissant des postes de travail virtuels aux utilisateurs. |

## Ressources virtuelles

| Terme | Définition courte |
|---|---|
| Abstraction matérielle | Présentation à la VM de ressources logiques masquant le matériel réel. |
| Allocation | Quantité de CPU, RAM, stockage ou réseau attribuée à une VM. |
| vCPU | Processeur logique présenté à une machine virtuelle. |
| vRAM | Quantité de mémoire vive attribuée à une machine virtuelle. |
| Disque virtuel | Fichier ou volume présenté à la VM comme un disque physique. |
| VHDX | Format de disque virtuel principalement utilisé par Microsoft Hyper-V. |
| VMDK | Format de disque virtuel principalement utilisé par VMware. |
| vNIC | Carte réseau virtuelle d'une machine virtuelle. |
| Carte réseau virtuelle | Interface réseau logique attribuée à une VM ou à un conteneur. |
| Réseau virtuel | Réseau logique reliant des charges sans dépendre directement du câblage physique. |
| vSwitch | Commutateur logiciel reliant les VM entre elles et au réseau physique. |
| Ordonnanceur | Mécanisme qui distribue le temps processeur entre les vCPU. |
| Passthrough | Attribution presque directe d'un périphérique physique à une VM. |

## Performances et optimisation

| Terme | Définition courte |
|---|---|
| Overhead | Ressources consommées par la couche de virtualisation elle-même. |
| Contention | Concurrence entre plusieurs VM pour une ressource devenue insuffisante. |
| Surallocation | Attribution logique de plus de ressources que le matériel n'en possède réellement. |
| Surengagement des ressources (overcommitment) | Attribution d'un total de ressources virtuelles supérieur à la capacité physique, en supposant qu'elles ne seront pas toutes utilisées simultanément. |
| Mutualisation des ressources | Partage contrôlé des mêmes ressources physiques entre plusieurs charges. |
| Concentration | Regroupement d'équipements dans un espace physique réduit. |
| Consolidation | Regroupement de plusieurs charges sur moins de serveurs pour mieux utiliser leurs ressources. |
| Rationalisation | Suppression des équipements ou ressources inutiles ou redondants. |
| Hyperconvergence | Regroupement du calcul, du stockage, du réseau et de la virtualisation dans une même architecture. |
| Dimensionnement | Attribution de ressources en fonction de la charge actuelle et de son évolution prévue. |
| Évolutivité | Capacité d'une infrastructure à accueillir de nouvelles charges ou ressources. |
| IOPS | Nombre d'opérations de lecture ou d'écriture qu'un stockage peut traiter par seconde. |

## Disponibilité et exploitation

| Terme | Définition courte |
|---|---|
| Haute disponibilité (HA) | Mécanismes limitant l'interruption d'un service en cas de panne. |
| Failover | Basculement ou redémarrage d'une charge sur un autre nœud après une panne. |
| Load balancing | Répartition de la charge entre plusieurs nœuds. |
| Migration à froid | Déplacement d'une VM arrêtée vers un autre hôte ou stockage. |
| Migration à chaud | Déplacement d'une VM en fonctionnement avec peu ou pas d'interruption. |
| Point de restauration (snapshot) | Capture temporaire de l'état d'une VM ; il ne remplace pas une sauvegarde. |
| Sauvegarde | Copie indépendante permettant de restaurer une VM ou ses données. |
| Isolation | Séparation empêchant une VM d'accéder directement aux ressources des autres. |
| N+1 | Dimensionnement conservant la capacité d'un nœud supplémentaire pour supporter une panne. |
| Point unique de défaillance (SPOF) | Composant dont la panne suffit à interrompre tout ou partie du service. |
| Redondance | Duplication de composants afin de maintenir le service lors d'une panne. |
| Réseau d'administration | Réseau réservé à la gestion des hyperviseurs et de l'infrastructure. |
| Stockage partagé | Stockage accessible par plusieurs hôtes et permettant la migration ou la reprise des VM. |
| Supervision | Collecte de métriques et d'alertes sur l'état et les performances de l'infrastructure. |

## Technologies citées

| Technologie | Catégorie |
|---|---|
| Microsoft Hyper-V | Hyperviseur de type 1. |
| VMware ESXi | Hyperviseur de type 1. |
| Proxmox VE | Plateforme de virtualisation utilisant notamment KVM. |
| KVM | Technologie de virtualisation intégrée au noyau Linux. |
| Xen | Hyperviseur de type 1. |
| VirtualBox | Hyperviseur de type 2. |
| VMware Workstation | Hyperviseur de type 2. |
| Parallels Desktop | Hyperviseur de type 2 pour macOS. |
| SAN | Réseau spécialisé donnant accès à du stockage en mode bloc. |
| NAS | Équipement fournissant du stockage partagé par le réseau. |

## Documents associés

- [Vue d'ensemble de l'itération](../../../admin-systemes-virtualisation/it-1/index.md)
- [Qu'est-ce que la virtualisation ?](../../../admin-systemes-virtualisation/it-1/quest-ce-que-la-virtualisation.md)
- [Comment fonctionne une machine virtuelle ?](../../../admin-systemes-virtualisation/it-1/comment-fonctionne-une-machine-virtuelle.md)
- [Pourquoi virtualiser une infrastructure ?](../../../admin-systemes-virtualisation/it-1/pourquoi-virtualiser-une-infrastructure.md)
- [Machine virtuelle ou conteneur : lequel choisir ?](../../../admin-systemes-virtualisation/it-1/machine-virtuelle-ou-conteneur-lequel-choisir.md)
