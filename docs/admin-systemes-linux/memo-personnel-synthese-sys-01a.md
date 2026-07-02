# Mémo personnel de synthèse - SYS-01a

## Concept 1 - Identités et comptes

Pour moi, un compte Linux n'est pas juste un nom : c'est une identité avec un UID, des groupes, un home, un shell et des droits. Il faut distinguer les comptes humains, qui servent à tracer une personne, et les comptes de service, qui servent à faire tourner un programme.

Pour la sécurité, c'est essentiel : si les comptes sont mélangés ou partagés, on ne sait plus qui a fait quoi. Des identités séparées permettent d'appliquer le moindre privilège et de garder une vraie traçabilité.

## Concept 2 - Permissions et accès

Les permissions Linux définissent qui peut lire, modifier ou exécuter un fichier. `chmod`, `chown`, `umask` et les ACL permettent d'adapter les droits selon le besoin réel.

Pour la sécurité, c'est une base : un fichier sensible mal protégé peut être lu, modifié ou supprimé par la mauvaise personne. Bien gérer les droits limite les fuites, les erreurs et les escalades de privilèges.

## Concept 3 - Traces, vérifications et preuves

Administrer un serveur, ce n'est pas seulement faire des commandes. Il faut aussi vérifier et prouver l'état du système : logs, rapports, tests SSH, services actifs, sauvegardes, restaurations et état avant/après.

Pour la sécurité, les preuves sont indispensables. Sans logs ni vérifications, on ne peut pas comprendre un incident ni démontrer qu'une correction fonctionne.

## Synthèse personnelle

Ce module me montre qu'un serveur Linux sécurisé repose d'abord sur des bases simples : savoir qui accède au système, à quoi il a accès, et comment le prouver.
