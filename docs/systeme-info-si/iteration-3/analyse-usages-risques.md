# Analyse des usages et des risques

## 1. Utilisateurs

Le SI est utilisé par plusieurs profils :

- agents d'accueil et d'état civil ;
- agents des services urbanisme, finances, RH et scolaire ;
- élus et direction ;
- administrateur informatique ou prestataire ;
- citoyens via le site web ou les démarches en ligne ;
- partenaires publics via des portails administratifs.

Les accès doivent être adaptés aux missions de chaque profil. Les agents d'accueil n'ont pas les mêmes besoins que le service RH ou le service finances.

Les principales contraintes sont :

- continuité de l'accueil du public ;
- protection des données personnelles ;
- simplicité d'utilisation pour des agents aux niveaux informatiques différents ;
- accès ponctuels de prestataires pour la maintenance.

Les comportements à risque possibles sont :

- partage de mots de passe entre agents ;
- ouverture de pièces jointes frauduleuses ;
- stockage de documents sensibles au mauvais endroit ;
- utilisation d'une messagerie personnelle ;
- absence de verrouillage de session sur un poste d'accueil.

## 2. Risques

| Type de risque | Exemple | Impact possible |
| --- | --- | --- |
| Technique | panne du serveur de fichiers ou de l'accès internet | interruption des services administratifs |
| Organisationnel | droits d'accès mal définis | consultation de données non nécessaires |
| Humain | phishing ou erreur de manipulation | vol d'identifiants, perte ou fuite de données |
| Dette technique | postes anciens, logiciels non maintenus | vulnérabilités, lenteurs, incompatibilités |
| Point d'entrée non contrôlé | accès distant prestataire mal sécurisé | compromission du SI |
| SPOF | une seule sauvegarde, un seul lien internet, un seul compte admin | blocage ou perte durable en cas d'incident |

Les données les plus sensibles sont les données personnelles des habitants, les dossiers des agents, les documents administratifs et les archives.

## 3. Dépendances

Le SI dépend fortement :

- du réseau interne ;
- de l'accès internet ;
- des applications métier ;
- de la messagerie ;
- des comptes utilisateurs ;
- des sauvegardes ;
- des prestataires qui maintiennent certains outils.

Les points critiques sont :

- le poste d'accueil, car il est exposé au public et utilisé fréquemment ;
- les comptes administrateurs, car ils donnent des droits élevés ;
- les applications état civil, finances et RH, car elles traitent des données sensibles ;
- les sauvegardes, car elles conditionnent la reprise après incident ;
- l'accès internet, car il permet la messagerie, les portails externes et certains outils cloud.

## Conclusion

Le SI d'une mairie est une architecture hybride avec des usages variés et des données sensibles. Les risques principaux viennent des accès utilisateurs, de la dépendance aux prestataires, des sauvegardes et des points d'entrée externes.

Les priorités sont de sécuriser les comptes, limiter les droits, vérifier les sauvegardes, encadrer les accès distants et sensibiliser les utilisateurs aux risques courants.

