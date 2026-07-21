# Termes essentiels de la virtualisation

## Livrable — Itération 1

Cette fiche regroupe les termes les plus importants à connaître pour expliquer le fonctionnement d'une infrastructure virtualisée.

| Terme | Définition essentielle |
|---|---|
| **Virtualisation** | Technique permettant de créer plusieurs ressources informatiques logiques à partir d'un même matériel physique. |
| **Hyperviseur** | Couche logicielle qui crée, exécute, isole et administre les machines virtuelles. |
| **Hyperviseur de type 1** | Hyperviseur installé directement sur le matériel, comme VMware ESXi, Proxmox VE ou Hyper-V. Il est principalement utilisé en production. |
| **Hyperviseur de type 2** | Logiciel de virtualisation installé sur un OS hôte, comme VirtualBox ou VMware Workstation. Il est adapté aux tests et à la formation. |
| **Hôte** | Serveur physique qui fournit son processeur, sa mémoire, son stockage et son réseau aux VM. |
| **Machine virtuelle (VM)** | Ordinateur logiciel isolé possédant du matériel virtuel et son propre système d'exploitation. |
| **Système d'exploitation hôte** | OS installé sur la machine physique et accueillant un hyperviseur de type 2 ou un moteur de conteneurs. |
| **Système d'exploitation invité** | OS installé et exécuté à l'intérieur d'une machine virtuelle. |
| **vCPU** | Processeur logique attribué à une VM à partir de la capacité des CPU physiques. |
| **vRAM** | Quantité de mémoire vive physique attribuée à une VM. |
| **Disque virtuel** | Fichier ou volume présenté à une VM comme un disque physique, par exemple au format VHDX ou VMDK. |
| **Carte réseau virtuelle** | Interface réseau logique permettant à une VM de communiquer avec les autres machines et réseaux. |
| **Réseau virtuel** | Réseau logique reliant des VM ou des conteneurs sans dépendre directement du câblage physique. |
| **Espace de stockage virtualisé (Datastore)** | Espace logique contenant les fichiers et disques virtuels des VM. |
| **Cluster** | Groupe de plusieurs hôtes associés pour répartir les charges et améliorer la disponibilité. |
| **Nœud de cluster** | Serveur physique ou équipement faisant partie d'un cluster. |
| **Haute disponibilité (HA)** | Ensemble de mécanismes limitant l'interruption d'un service lorsqu'un composant tombe en panne. |
| **Migration à chaud** | Déplacement d'une VM en fonctionnement vers un autre hôte avec peu ou pas d'interruption. |
| **Point de restauration (Snapshot)** | Capture temporaire de l'état d'une VM permettant un retour arrière rapide. Ce n'est pas une sauvegarde. |
| **Sauvegarde** | Copie indépendante et durable permettant de restaurer une VM ou ses données après une perte. |
| **Conteneur** | Processus isolé regroupant une application et ses dépendances tout en partageant le noyau de l'hôte. |
| **Conteneurisation** | Technique consistant à empaqueter et exécuter une application dans un conteneur isolé. |
| **Moteur de conteneurs** | Logiciel chargé de créer et d'exécuter les conteneurs, comme Docker ou Podman. |
| **Image de conteneur** | Modèle immuable contenant une application, ses dépendances et les instructions nécessaires à son exécution. |
| **Orchestrateur** | Plateforme automatisant le déploiement, le redémarrage et la mise à l'échelle des conteneurs, comme Kubernetes. |
| **Mutualisation des ressources** | Partage contrôlé des mêmes ressources physiques entre plusieurs VM ou conteneurs. |
| **Abstraction matérielle** | Présentation de composants virtuels qui masquent à la VM les détails du matériel réel. |
| **Isolation** | Séparation empêchant une charge d'accéder directement aux ressources ou aux données des autres charges. |
| **Consolidation** | Regroupement de plusieurs services sur moins de serveurs afin de mieux utiliser leurs ressources. |
| **Concentration** | Regroupement d'un grand nombre d'équipements dans un espace physique réduit. |
| **Rationalisation** | Suppression des équipements ou ressources devenus inutiles, redondants ou sous-utilisés. |
| **Hyperconvergence** | Architecture regroupant calcul, stockage, réseau et virtualisation dans une solution administrée comme un ensemble. |
| **Surengagement des ressources (Overcommitment)** | Attribution d'un total de ressources virtuelles supérieur à la capacité physique, en supposant qu'elles ne seront pas toutes utilisées simultanément. |

!!! warning "À retenir"
    Un **snapshot** dépend de l'infrastructure de la VM et sert surtout au retour arrière. Une **sauvegarde** est une copie indépendante conçue pour restaurer durablement les données.

## Repère rapide

```text
Matériel physique
       ↓
Hyperviseur
       ↓
Machines virtuelles
       ↓
OS invités et applications
```

Dans une infrastructure conteneurisée :

```text
Matériel physique
       ↓
OS hôte et noyau partagé
       ↓
Moteur de conteneurs
       ↓
Conteneurs et applications
```
