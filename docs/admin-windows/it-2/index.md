# Itération 2 - Organisation Active Directory

## Objectif de l'itération

Cette itération sert à organiser l'annuaire Active Directory après la création du domaine.

L'objectif est de construire une arborescence claire avec :

- des unités d'organisation ;
- des utilisateurs ;
- des groupes globaux ;
- des descriptions ;
- des affectations propres par groupe.
- des stratégies de groupe de base ;
- un premier déploiement logiciel par GPO.
- une première stratégie BitLocker avec récupération dans Active Directory.
- Windows LAPS pour gérer les mots de passe administrateur locaux.

## Principes importants

Dans Active Directory, il faut éviter de tout placer dans les conteneurs par défaut.

Une bonne organisation facilite :

- la gestion des comptes ;
- l'application future des GPO ;
- la délégation d'administration ;
- l'audit ;
- la lisibilité de l'annuaire.

!!! tip "Bon réflexe"
    On donne les droits aux groupes, pas directement aux utilisateurs. Les utilisateurs héritent des accès par leur appartenance aux groupes.

## Activités prévues

1. Créer l'arborescence de base AD.
2. Créer les premiers utilisateurs.
3. Créer les groupes globaux.
4. Affecter les utilisateurs aux groupes.
5. Joindre un poste Windows 11 au domaine.
6. Créer les premières GPO : mot de passe, restriction panneau de configuration et déploiement 7-Zip.
7. Configurer BitLocker avec sauvegarde des clés de récupération dans AD DS.
8. Déployer Windows LAPS pour gérer un mot de passe administrateur local unique par poste.
9. Préparer une structure avancée de type Tier 0 / Tier 1 / Tier 2 si demandé.
