# Revue de l'itération

## Éléments vérifiés

- OpenLDAP est la source des utilisateurs et des groupes.
- Samba utilise le backend `ldapsam` pour l'authentification SMB.
- Les partages `Commun`, `Developpement`, `Bureau-etudes` et
  `Administration` sont déclarés dans `samba-ad/config/smb.conf`.
- Les données OpenLDAP et Samba sont conservées dans des volumes Docker.
- Les procédures sont regroupées dans `operations.md`.
- Le plan de validation est décrit dans `validation.md`.

## Points restant à valider

- exécuter V-01 à V-06 avec des comptes de test dédiés ;
- réaliser un refus d'accès sur chaque partage sensible ;
- vérifier la désactivation LDAP selon le profil LAM utilisé ;
- réaliser une sauvegarde puis une restauration réelle des volumes ;
- documenter la supervision et les alertes ;
- tester une restauration sur une autre machine.

## Choix d'architecture

Les projets Compose restent séparés :

- `openldap/` pour l'annuaire ;
- `ldap-account-manager/` pour l'interface ;
- `samba-ad/` pour le serveur de fichiers ;
- `wordpress-compose/` pour l'application Web.

Cette séparation permet de redémarrer un service indépendamment. Aucun Compose
global n'est ajouté à ce stade : les projets utilisent des fichiers `.env`
distincts, le réseau externe `openldap_default` et des cycles de reprise
différents. Un fichier fédérateur nécessiterait un test dédié de l'ordre de
démarrage, des secrets et des dépendances.

## Décision

L'itération est documentée mais reste partiellement validée tant que les tests
V-01 à V-06 n'ont pas été exécutés et consignés.
