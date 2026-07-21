# Glossaire Administration Windows — Itération 4

## Sujet

Automatisation PowerShell, inventaire Active Directory, pare-feu et journaux Windows.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| PowerShell | Shell et langage d'automatisation orienté objets de Microsoft. |
| CSV | Format tabulaire utilisé comme source ou résultat d'un script. |
| `Import-Csv` | Importe chaque ligne d'un fichier CSV comme un objet PowerShell. |
| `-WhatIf` | Simule une action compatible sans appliquer la modification. |
| Transcript | Journal textuel d'une session PowerShell. |
| Windows Defender Firewall | Pare-feu hôte gérant les flux entrants et sortants par profil. |
| Event Viewer | Console d'analyse des journaux Système, Application et Sécurité. |
| Événements 4624/4625 | Connexion réussie / échec de connexion dans le journal Sécurité. |

## Manipulations faites

| Manipulation | Commandes ou actions |
| --- | --- |
| Automatiser les comptes | Importer un CSV, valider les données et créer les utilisateurs AD. |
| Inventorier AD | Exporter utilisateurs, groupes, ordinateurs et paramètres utiles. |
| Contrôler le pare-feu | Auditer et documenter les règles appliquées aux serveurs. |
| Exploiter les journaux | Filtrer et exporter les événements utiles au diagnostic et à l'audit. |

## Docs associées

- [Vue d'ensemble](../../../admin-windows/it-4/index.md)
- [Créer des utilisateurs depuis un CSV](../../../admin-windows/it-4/activite9-creation-utilisateurs-csv-powershell.md)
- [Inventaire Active Directory](../../../admin-windows/it-4/activite10-inventaire-active-directory-powershell.md)
- [Firewall et journaux Windows](../../../admin-windows/it-4/activite11-firewall-journaux-windows.md)

