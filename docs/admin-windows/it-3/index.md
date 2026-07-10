# Itération 3 - Serveur de fichiers et données utilisateurs

## Objectif de l'itération

Cette itération sert à séparer les données utilisateurs du contrôleur de domaine.

L'objectif est de mettre en place un serveur de fichiers dédié, nommé `SRV-FIC01`, qui portera les futurs partages de l'entreprise.

## Principes importants

Un contrôleur de domaine ne doit pas devenir un serveur multifonction.

Dans une infrastructure propre :

- `SRV-AD01` porte Active Directory et DNS ;
- `SRV-FIC01` porte les données utilisateurs ;
- les données sont placées sur un volume séparé du système ;
- un volume ou support distinct est prévu pour les sauvegardes ;
- les partages seront ensuite protégés par des groupes Active Directory.

!!! warning "Point de vigilance"
    Ne pas héberger les partages métiers sur `SRV-AD01`. Le contrôleur de domaine doit rester dédié à l'identité, au DNS et aux services AD.

## Activités prévues

1. Créer `SRV-FIC01` comme serveur de fichiers dédié.
2. Ajouter un disque de données pour `D:`.
3. Prévoir un disque de sauvegarde pour `E:`.
4. Joindre le serveur au domaine `corp.local`.
5. Installer le rôle serveur de fichiers.
6. Créer l'arborescence de données.
7. Préparer les partages et permissions dans les activités suivantes.
