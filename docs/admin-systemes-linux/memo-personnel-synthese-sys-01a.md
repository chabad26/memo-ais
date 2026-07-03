# Mémo personnel de synthèse - SYS-01a

## Concept 1 - Script

Un script permet d'exécuter plusieurs opérations à la suite, avec ou sans interaction avec l'utilisateur du poste. On peut s'en servir par exemple :

- pour faire des sauvegardes
- faire les MaJ système et son nettoyage
- faire des opérations sur plusieurs processus et/ou utilisateurs via une boucle.

Le script permet d'automatiser des opérations et des tâches répétitives et même d'être schedulé via crontab.

## Concept 2 - Sauvegarde & backup

Les sauvegardes sont essentielles au sein d'une entreprise. Faites de manière régulière, cela permet de conserver les données après une défaillance ou une attaque.

Chaque sauvegarde doit être testée (via sha256sum & test de décompression) pour vérifier s'il n'y a pas eu de corruption durant la sauvegarde (risque augmenté à mesure que le poids de l'archive augmente).

En cas de problème, on peut donc "décompresser" les backups pour limiter la perte de données.

On peut les scheduler via des scripts et crontab.

## Concept 3 - Gestion des utilisateurs & groupes

Sur les distributions Linux, les processus et les utilisateurs ont chacun un compte. Cela permet de mieux gérer s'ils sont "interactifs" (si on peut se connecter au compte) ou non.
Chaque utilisateur interactif a un environnement dédié (/home/$user) propre à lui.

Chaque utilisateur peut être rattaché à un groupe lui donnant accès aux droits de celui-ci (sudo si on veut que l'utilisateur puisse avoir une élévation des privilèges par exemple). Grâce à cela, on peut donc gérer plus rapidement, grâce aux groupes, les autorisations des utilisateurs.

Des commandes permettent de voir rapidement chaque utilisateur et dans quel(s) groupe(s) il fait partie.

## Synthèse personnelle

Je dirais que ce module m'a fait comprendre les bonnes pratiques liées à l'environnement Linux.
