# Découverte de l'entreprise fictive

## Objectif de la feuille

Cette feuille sert à comprendre le contexte métier du module avant de déployer les services techniques.

L'objectif n'est pas encore de concevoir toute l'architecture, mais d'identifier les utilisateurs, les postes, les services internes et les premières dépendances qui guideront la suite de l'itération.

## Déroulement

Le formateur présente une entreprise fictive qui conçoit, intègre et maintient des systèmes électroniques et logiciels.

Cette entreprise comprend notamment :

- une équipe de conception matérielle ;
- une équipe de développement embarqué ;
- une équipe d'intégration et de validation ;
- des fonctions administratives et commerciales ;
- des postes de travail Linux et Windows ;
- une infrastructure utilisée pour les compilations Yocto ;
- une ferme de tests existante ;
- des services internes qui seront progressivement déployés pendant le module.

Durant les prochains jours, plusieurs services nécessaires au fonctionnement de cette entreprise seront mis en place et intégrés progressivement.

## Ce qu'il faut identifier à ce stade

### Grandes catégories d'utilisateurs

Repérez les profils qui utiliseront l'infrastructure :

- conception matérielle ;
- développement embarqué ;
- intégration et validation ;
- administration système ;
- fonctions administratives et commerciales.

Pour chaque catégorie, notez les besoins probables : accès aux fichiers, outils de compilation, messagerie, authentification, supervision ou administration.

### Principaux types de postes

Identifiez les machines présentes ou probables dans l'entreprise :

| Type de poste | Usage probable |
| --- | --- |
| Poste Linux | Développement, compilation, administration et outils techniques |
| Poste Windows | Bureautique, fonctions commerciales, outils métier ou validation |
| Serveur de compilation | Construction d'images ou de composants Yocto |
| Machines de test | Exécution de scénarios de validation |
| Serveurs internes | Hébergement des services progressivement déployés |

### Services qui devront communiquer

À ce stade, il faut surtout repérer les communications probables :

- postes utilisateurs vers annuaire ;
- postes utilisateurs vers partages de fichiers ;
- services internes vers DNS ;
- services internes vers certificats ;
- utilisateurs vers messagerie ;
- serveur de compilation vers dépôts ou partages ;
- ferme de tests vers services de validation ;
- supervision vers machines et services surveillés.

### Dépendances techniques probables

Certains services dépendront d'autres briques pour fonctionner correctement.

| Dépendance | Pourquoi elle compte |
| --- | --- |
| Réseau | Les postes et serveurs doivent pouvoir communiquer. |
| DNS | Les services doivent être joignables par nom. |
| Annuaire | Les comptes et groupes doivent être centralisés. |
| Certificats | Les échanges internes doivent pouvoir être sécurisés. |
| Stockage | Les données, partages et sauvegardes doivent être conservés. |
| Sauvegarde | Les services critiques doivent pouvoir être restaurés. |
| Supervision | Les incidents doivent être détectés et suivis. |
