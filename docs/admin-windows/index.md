# Administration Windows

## Présentation du module

Ce module regroupe les travaux pratiques liés à l'administration d'une infrastructure Windows.

L'objectif est de construire progressivement une plateforme de laboratoire permettant de travailler sur :

- Windows Server,
- Hyper-V,
- Windows Admin Center,
- Active Directory Domain Services,
- DNS,
- les comptes et groupes,
- les stratégies de groupe,
- les serveurs de fichiers SMB,
- les volumes NTFS dédiés aux données,
- l'automatisation PowerShell,
- le durcissement et l'audit,
- l'administration distante,
- la documentation technique.

## Logique du module

Le module commence par la préparation d'une machine physique ou hôte nommée **LABO**.

Cette machine sert de base pour :

- installer Windows Server,
- activer Hyper-V,
- créer les machines virtuelles,
- administrer l'infrastructure,
- héberger le futur contrôleur de domaine.

La première VM importante est **SRV-AD01**. Elle servira ensuite à créer le domaine Active Directory.

Windows Admin Center sert d'interface principale pour administrer LABO depuis un navigateur, gérer Hyper-V et ouvrir la console des machines virtuelles.

## Compétences visées

À la fin du module, l'objectif est de savoir :

- préparer un hôte Windows Server,
- configurer le réseau, le nom de machine et l'accès distant,
- installer et utiliser Hyper-V,
- créer une VM serveur proprement documentée,
- installer Windows Server Core,
- préparer un contrôleur de domaine,
- administrer à distance avec RSAT ou Windows Admin Center,
- séparer les rôles AD et fichiers sur des serveurs distincts,
- automatiser des tâches d'administration avec PowerShell.

!!! tip "Bon réflexe"
    Une infrastructure Windows propre commence par une documentation claire : noms, adresses IP, rôles, disques, emplacements et captures de preuves.
