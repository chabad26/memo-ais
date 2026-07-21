# Glossaire Administration Windows — Itération 3

## Sujet

Serveur de fichiers, modèle AGDLP, partages SMB et sauvegarde.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| SMB | Protocole Windows de partage de fichiers sur le réseau. |
| NTFS | Système de fichiers Windows portant les autorisations détaillées. |
| AGDLP | Comptes → groupes globaux → groupes locaux de domaine → permissions. |
| Groupe local de domaine | Groupe auquel on attribue les permissions sur une ressource du domaine. |
| Shadow Copies | Instantanés permettant d'accéder aux versions précédentes de fichiers. |
| Windows Server Backup | Fonctionnalité de sauvegarde et restauration de Windows Server. |
| Lecteur réseau | Partage SMB présenté à l'utilisateur sous forme de lettre de lecteur. |

## Manipulations faites

| Manipulation | Commandes ou actions |
| --- | --- |
| Déployer `SRV-FIC01` | Joindre le domaine, ajouter les volumes `D:` et `E:` et installer le rôle fichiers. |
| Organiser les accès | Créer l'arborescence, les groupes AGDLP et les permissions NTFS/partage. |
| Distribuer les partages | Mapper les lecteurs réseau avec une GPO. |
| Protéger les données | Tester les versions précédentes, la sauvegarde et la restauration. |

## Docs associées

- [Vue d'ensemble](../../../admin-windows/it-3/index.md)
- [Créer SRV-FIC01](../../../admin-windows/it-3/activite7-creation-srv-fic01-serveur-fichiers.md)
- [AGDLP, partages et lecteurs réseau](../../../admin-windows/it-3/activite7bis-agdlp-partages-lecteurs-reseau.md)
- [Sauvegarde et restauration](../../../admin-windows/it-3/activite8-sauvegarde-restauration-srv-fic01.md)

