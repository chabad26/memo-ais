# Comprendre les modèles cloud et la responsabilité partagée

## Objectif

Cette feuille pose les bases avant de comparer OVH et AWS et de préparer une migration cloud.

Avant de choisir une architecture, il faut savoir ce que l'on administre réellement, ce que le fournisseur prend en charge et ce qui reste sous la responsabilité du client.

## Ce que tu vas faire, et pourquoi

Tu vas distinguer trois grands modèles de service cloud :

- **IaaS**, Infrastructure as a Service ;
- **PaaS**, Platform as a Service ;
- **SaaS**, Software as a Service.

Tu vas aussi comprendre le **modèle de responsabilité partagée**. Dans le cloud, la sécurité n'est jamais totalement déléguée au fournisseur. Plus le service est managé, plus le fournisseur prend de responsabilités, mais le client conserve toujours une part critique : identités, données, configuration, secrets et usages.

## IaaS - Infrastructure as a Service

Avec l'IaaS, le fournisseur fournit l'infrastructure de base :

- datacenters ;
- matériel physique ;
- réseau physique ;
- hyperviseur ;
- capacité de calcul, stockage et réseau.

Le client gère principalement :

- les machines virtuelles ;
- le système d'exploitation ;
- les mises à jour ;
- les services installés ;
- le pare-feu applicatif ;
- les comptes et accès ;
- les données.

Exemples typiques :

- une instance de calcul AWS EC2 ;
- une instance Public Cloud OVH ;
- un volume bloc attaché à une VM ;
- un réseau privé virtuel cloud.

Ce modèle ressemble le plus à l'administration d'une infrastructure on-premise, mais sans gérer le matériel physique.

## PaaS - Platform as a Service

Avec le PaaS, le fournisseur gère davantage de couches techniques. Il prend en charge l'infrastructure, le système d'exploitation, le runtime ou certains composants de plateforme.

Le client se concentre davantage sur :

- le code applicatif ;
- les paramètres de déploiement ;
- les données ;
- les accès ;
- la configuration de sécurité exposée par le service.

Exemples typiques :

- une base de données managée ;
- une plateforme d'exécution applicative ;
- un service Kubernetes managé selon le périmètre exact proposé ;
- un service de file de messages managé.

Le PaaS réduit l'administration système directe, mais il impose de bien comprendre les options de configuration et les limites du service.

## SaaS - Software as a Service

Avec le SaaS, le fournisseur fournit une application complète prête à l'emploi.

Le client ne gère plus les serveurs, l'OS, le runtime ou l'application elle-même. Il gère surtout :

- les utilisateurs ;
- les rôles ;
- les paramètres de sécurité ;
- les données déposées dans l'application ;
- la conformité des usages.

Exemples typiques :

- une messagerie cloud prête à l'emploi ;
- un outil collaboratif ;
- un CRM ;
- une solution de gestion documentaire.

Le SaaS est le modèle le plus managé. Il réduit fortement la charge d'administration technique, mais ne supprime pas la responsabilité du client sur les accès, les données et les configurations.

## Comparaison rapide

| Modèle | Ce que fournit le cloud | Ce que le client garde principalement |
| --- | --- | --- |
| IaaS | Infrastructure, matériel, virtualisation | OS, services, mises à jour, IAM, données, sécurité système |
| PaaS | Infrastructure, OS, runtime ou plateforme | Code, configuration, IAM, données, sécurité applicative |
| SaaS | Application complète | Utilisateurs, rôles, données, paramètres de sécurité |

## Responsabilité partagée

Le modèle de responsabilité partagée sépare deux grandes zones :

- la sécurité **du cloud** ;
- la sécurité **dans le cloud**.

Le fournisseur est responsable de la sécurité **du cloud** :

- datacenters ;
- alimentation électrique ;
- contrôle physique ;
- matériel ;
- hyperviseur ;
- réseau physique ;
- disponibilité des services managés selon le contrat.

Le client est responsable de la sécurité **dans le cloud** :

- configuration IAM ;
- utilisateurs, groupes, rôles et MFA ;
- chiffrement des données ;
- gestion des clés et secrets ;
- mises à jour des systèmes quand il les administre ;
- règles réseau et pare-feu ;
- sauvegardes selon le service utilisé ;
- configuration applicative ;
- contrôle des données stockées.

!!! warning "Point clé"
    Le cloud ne rend pas automatiquement une infrastructure sécurisée. Une VM exposée avec un mauvais pare-feu, un compte sans MFA ou un secret commité dans Git restent des erreurs côté client.

## Effet du niveau de service

Plus le service est managé, plus la part du fournisseur augmente.

| Niveau | Part fournisseur | Part client |
| --- | --- | --- |
| IaaS | Matériel, virtualisation, datacenter | Forte responsabilité sur OS, services et sécurité |
| PaaS | Infrastructure, OS, runtime | Responsabilité centrée sur code, données, accès et configuration |
| SaaS | Application complète | Responsabilité centrée sur usages, comptes, droits et données |

Cela ne signifie pas que le SaaS supprime le risque. Il déplace le risque vers la gestion des comptes, des droits, des données et de la conformité.

## Application à la migration DIST-01a

Pour migrer l'infrastructure DIST-01a, il faut se poser les bonnes questions pour chaque composant :

| Composant | Question de migration |
| --- | --- |
| OpenLDAP | Faut-il garder une VM IaaS ou utiliser un service d'identité managé ? |
| Samba et partages | Faut-il déplacer les volumes, utiliser un stockage objet ou un service de fichiers managé ? |
| Messagerie | Faut-il maintenir une pile complète ou utiliser un SaaS/PaaS de messagerie ? |
| PKI | Faut-il conserver une autorité interne ou utiliser un service de certificats managé ? |
| Sauvegardes | Qui garantit la rétention, la restauration et le chiffrement ? |
| Supervision | Faut-il porter ELK, utiliser un service managé ou combiner les deux ? |

Le choix n'est donc pas seulement technique. Il dépend aussi :

- du niveau de maîtrise attendu ;
- du budget ;
- du temps d'administration disponible ;
- des exigences de souveraineté ;
- de la sécurité attendue ;
- des preuves à fournir au jury.

## Vérifications à conserver

Cette feuille est surtout conceptuelle. Les preuves attendues sont donc des éléments d'analyse :

- un tableau comparatif IaaS, PaaS, SaaS ;
- une synthèse du modèle de responsabilité partagée ;
- une première liste des composants DIST-01a à classer ;
- les questions ouvertes pour OVH et AWS.

## État final attendu

À la fin de cette feuille, tu dois pouvoir expliquer :

- ce qui différencie IaaS, PaaS et SaaS ;
- ce que le fournisseur cloud prend en charge ;
- ce que le client doit encore sécuriser ;
- pourquoi un service managé réduit certaines tâches sans supprimer la responsabilité ;
- comment ces notions orientent la migration de DIST-01a.

## Ressources

- [AWS - Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/)
- [OVHcloud - Learn](https://www.ovhcloud.com/fr/learn/)
