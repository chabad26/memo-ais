# Intégration distribuée on-premise

!!! info "Nouveau module"
    Ce module marque le passage d'une administration de machines isolées à l'intégration d'une infrastructure d'entreprise complète, cohérente et exploitable.

## Objectif global

Ce module a pour objectif de construire progressivement une infrastructure **on-premise moderne**, composée de services interdépendants et proches d'un contexte professionnel réel.

Pendant dix jours, le travail ne consiste pas seulement à installer des outils séparés, mais à comprendre comment ils s'assemblent pour former un système d'information exploitable : services conteneurisés, annuaire central, partage de fichiers, messagerie, autorité de certification interne, sauvegardes et supervision.

L'objectif n'est pas de devenir expert Docker, LDAP ou messagerie en quelques jours. L'enjeu principal est d'acquérir une **vision globale d'architecture** : savoir identifier le rôle de chaque service, comprendre ses dépendances, vérifier son bon fonctionnement et documenter son intégration dans l'infrastructure.

## Fil conducteur

Tout au long du module, les travaux s'appuient sur une entreprise fictive de conception et d'intégration de systèmes électroniques.

Cette entreprise dispose de plusieurs équipes :

- une équipe de développement embarqué ;
- une équipe de validation ;
- une équipe d'administration ;
- des services internes nécessitant authentification, partage, messagerie et continuité d'activité.

Les choix techniques sont guidés par des exigences métier : disponibilité des services, continuité d'activité, sécurité des accès, reprise après incident et capacité à expliquer l'état de l'infrastructure à une autre personne.

## Ce que le module fait travailler

| Axe | Ce qu'il faut comprendre |
| --- | --- |
| Services conteneurisés | Déployer des services isolés, reproductibles et plus faciles à maintenir. |
| Annuaire central | Gérer les identités, les comptes et les accès depuis une source commune. |
| Partage de fichiers | Mettre à disposition des espaces de travail adaptés aux équipes. |
| Messagerie | Intégrer un service de communication interne dépendant du DNS, des certificats et des comptes. |
| PKI interne | Créer une autorité de certification pour sécuriser les échanges internes. |
| Sauvegarde | Définir ce qui doit être sauvegardé, à quelle fréquence et comment le restaurer. |
| Supervision | Observer l'état des services, détecter les pannes et garder des traces exploitables. |
| PCA/PRA | Relier les choix techniques aux objectifs de continuité et de reprise. |

## Notions clés

### Infrastructure intégrée

Une infrastructure d'entreprise n'est pas une addition de serveurs indépendants. Les services dépendent les uns des autres : l'annuaire fournit les identités, le DNS permet de joindre les services, les certificats sécurisent les accès, la sauvegarde protège les données et la supervision permet de savoir si l'ensemble fonctionne.

Le module sert donc à apprendre à raisonner en **système complet**.

### Exigences métier

Les décisions techniques doivent répondre à des besoins concrets : qui doit accéder à quoi, quels services sont critiques, combien de données l'entreprise peut perdre, combien de temps un service peut rester indisponible et quelles preuves permettent de montrer que l'infrastructure fonctionne.

### PCA, PRA, RPO et RTO

Le module introduit les notions de continuité et de reprise d'activité :

- **PCA** : plan de continuité d'activité, pour maintenir les services essentiels malgré un incident ;
- **PRA** : plan de reprise d'activité, pour restaurer progressivement l'infrastructure après un sinistre ;
- **RPO** : quantité maximale de données que l'on accepte de perdre ;
- **RTO** : durée maximale acceptable avant le retour d'un service.

Ces notions ne restent pas théoriques : elles guident la stratégie de sauvegarde, la priorisation des services et les tests de restauration.

## Progression du module

| Temps | Orientation |
| --- | --- |
| [Itération 1 - Docker](it-1/index.md) | Préparer la machine Ubuntu 24.04 LTS qui servira de base au module. |
| Jours 1 à 3 | Poser les fondations : architecture cible, conteneurs, réseau, DNS et premiers services. |
| Jours 4 à 6 | Intégrer les services d'entreprise : annuaire, partages, messagerie et certificats internes. |
| Jours 7 à 8 | Consolider l'exploitation : sauvegardes, supervision, preuves de fonctionnement et documentation. |
| Jours 9 à 10 | Gérer un sinistre simulé et appliquer un plan de reprise existant. |

## Résultat attendu

En fin de module, l'infrastructure doit être suffisamment claire pour être comprise, testée et reprise par une autre personne.

Les livrables attendus doivent montrer :

- les services déployés et leur rôle ;
- les dépendances entre les services ;
- les comptes, accès et certificats utilisés ;
- la stratégie de sauvegarde ;
- les contrôles de supervision ;
- les objectifs RPO/RTO associés aux services critiques ;
- la procédure suivie lors du sinistre simulé ;
- l'état final vérifiable après reprise.

## En fin de module

Tu devrais être capable d'expliquer comment une infrastructure on-premise moderne est construite, pourquoi ses services sont interdépendants, comment vérifier son bon fonctionnement et comment réagir lorsqu'un incident oblige à restaurer les services critiques.

Ce module sert surtout à développer une posture d'intégrateur : ne pas seulement installer un service, mais le relier proprement au reste de l'infrastructure, le documenter et prévoir sa reprise en cas de problème.
