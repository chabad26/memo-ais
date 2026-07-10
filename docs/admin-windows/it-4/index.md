# Itération 4 - PowerShell, durcissement, firewall et journaux

## Objectif de l'itération

Cette itération sert à automatiser les tâches d'administration Windows et à renforcer la sécurité de l'infrastructure.

L'objectif est de travailler sur :

- l'automatisation PowerShell ;
- la création de comptes Active Directory depuis un CSV ;
- les scripts contrôlés avec journalisation ;
- le durcissement de base ;
- les règles de pare-feu ;
- l'exploitation des journaux Windows.

## Principes importants

Un script d'administration doit être prévisible, testable et documenté.

Avant une exécution large :

- tester sur un petit jeu de données ;
- prévoir un mode simulation ;
- ne jamais stocker de secret en clair ;
- produire un rapport d'exécution ;
- gérer les erreurs.

!!! tip "Bon réflexe"
    En PowerShell, commencer par un mode `-WhatIf` ou un petit CSV de test évite les mauvaises surprises dans Active Directory.

## Activités prévues

1. Créer des utilisateurs Active Directory depuis un fichier CSV.
2. Produire un inventaire Active Directory exploitable.
3. Ajouter progressivement des contrôles, rapports et journaux.
4. Durcir les règles de pare-feu Windows.
5. Exploiter les journaux pour auditer les actions.

## Activités

- [Activité 9 - Créer des utilisateurs depuis un CSV](activite9-creation-utilisateurs-csv-powershell.md)
- [Activité 10 - Inventaire Active Directory](activite10-inventaire-active-directory-powershell.md)
- [Activité 11 - Durcissement firewall et journaux Windows](activite11-firewall-journaux-windows.md)
