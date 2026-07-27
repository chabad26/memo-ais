# Itération 4 — Exploitation, optimisation et documentation d'une infrastructure virtualisée

## Contexte

Le cluster de virtualisation d'AlpesNet est désormais opérationnel.

Les services critiques de l'entreprise bénéficient d'un stockage partagé, de la migration à chaud et de la haute disponibilité.

Avant la mise en production de cette nouvelle infrastructure, le responsable demande de réaliser les dernières opérations d'exploitation afin de garantir son bon fonctionnement, sa sécurité et sa maintenabilité.

La mission consiste à effectuer les contrôles techniques, à optimiser la plateforme et à produire la documentation destinée aux futurs administrateurs.

!!! question "Problématique"
    **Comment garantir qu'une infrastructure virtualisée est prête à être exploitée durablement en production ?**

## Objectifs de l'itération

- contrôler l'état du cluster, des VM, du stockage et des réseaux ;
- supprimer les points de configuration fragiles ou incohérents ;
- segmenter les communications selon le rôle des systèmes ;
- limiter chaque flux au strict nécessaire ;
- vérifier le fonctionnement et l'isolement obtenus ;
- conserver les commandes, résultats et captures utiles à une reprise d'exploitation ;
- définir des procédures de contrôle, de maintenance et de retour arrière.

## Environnement de départ réel

| Composant | Adresse actuelle | État |
| --- | --- | --- |
| `PVE1` | `10.42.0.131/24` | Nœud Proxmox existant |
| `PVE2` | `10.42.0.132/24` | Nœud Proxmox existant |
| `PVE3` | `10.42.0.133/24` | Nœud Proxmox existant |
| `NFS1` | `10.42.0.134/24` | Stockage partagé existant |
| `WEB1` | `10.42.0.125/24` | **Seule VM applicative encore présente** |

Les autres VM ont été supprimées afin de libérer des ressources. Les composants encore présents utilisent le réseau commun `10.42.0.0/24`.

!!! warning "Contrainte principale : manque de puissance"
    `LABO_CORE` ne dispose pas d'assez de ressources pour exécuter confortablement les trois nœuds Proxmox, `NFS1` et plusieurs VM applicatives. La réalisation pratique sera donc limitée à `WEB1` et aux composants du cluster. Les autres systèmes éventuellement cités représentent uniquement l'architecture cible d'AlpesNet.

!!! warning "Limite du laboratoire"
    `PVE1`, `PVE2` et `PVE3` sont hébergés sur le même serveur Hyper-V `LABO_CORE`. Les essais valident le fonctionnement logique de Proxmox, mais une panne de `LABO_CORE` affecterait tout le cluster.

## Feuille de travail

La première opération d'exploitation porte sur la segmentation et le filtrage des communications :

→ [Comment sécuriser les communications entre les machines virtuelles ?](comment-securiser-les-communications-entre-les-machines-virtuelles.md)
