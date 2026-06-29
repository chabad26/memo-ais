# Mémo personnel de synthèse - SYS-01a

## Concept 1 - Un compte n'est pas seulement un nom d'utilisateur

Pour moi, un compte Linux représente une identité technique : il a un UID, appartient à un ou plusieurs groupes, possède un répertoire personnel et peut recevoir des droits précis. Un compte humain sert à tracer les actions d'une personne, alors qu'un compte de service sert uniquement à faire tourner un programme.

Lien avec la sécurité : si tout le monde utilise le même compte, on ne sait plus qui a fait quoi. En séparant les comptes humains, les groupes et les comptes de service, on limite les droits et on garde une meilleure traçabilité.

## Concept 2 - Les permissions protègent les fichiers avant même les outils de sécurité

Les droits Linux (`r`, `w`, `x`) indiquent qui peut lire, modifier ou exécuter un fichier. `chmod` règle les permissions, `chown` définit le propriétaire, et `umask` fixe les droits par défaut lors de la création de nouveaux fichiers. Les ACL permettent d'ajouter des exceptions plus fines quand les permissions classiques ne suffisent pas.

Lien avec la sécurité : un fichier sensible mal protégé peut être lu ou modifié par un utilisateur qui ne devrait pas y avoir accès. Bien régler les permissions évite les fuites d'information et réduit les risques d'erreur ou de sabotage.

## Concept 3 - Administrer un serveur, c'est aussi prouver ce qui a été fait

Les logs, les commandes de vérification et les rapports ne sont pas seulement de la documentation. Ils servent à montrer l'état du système avant/après une action : comptes créés, droits appliqués, services actifs, erreurs, connexions, sauvegardes et restaurations testées.

Lien avec la sécurité : sans traces, on ne peut pas enquêter correctement après un incident. Les journaux système, les rapports d'audit et les preuves de test permettent de détecter un problème, comprendre ce qui s'est passé et démontrer que les mesures de sécurité fonctionnent.

## Synthèse personnelle

Ce module me montre qu'un serveur Linux sécurisé repose d'abord sur des bases simples : des identités séparées, des permissions maîtrisées et des preuves vérifiables. Avant d'ajouter des outils avancés, il faut savoir qui a accès à quoi, pourquoi, et comment le démontrer.
