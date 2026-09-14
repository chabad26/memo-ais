# Instrumenter et mesurer l'infrastructure

## Contexte

Vous intégrez l'équipe Infrastructure d'**AlpesNet**.

L'entreprise dispose désormais d'une infrastructure virtualisée comprenant plusieurs serveurs Linux et Windows, des machines virtuelles, des services réseau et des applications.

L'infrastructure fonctionne, mais l'équipe d'exploitation rencontre une difficulté : lorsqu'un utilisateur signale un problème, les administrateurs doivent se connecter successivement aux différents serveurs pour comprendre ce qui se passe.

Le responsable infrastructure vous confie donc une nouvelle mission : **mettre en place une capacité d'observation centralisée permettant de savoir rapidement ce qui fonctionne, ce qui fonctionne mal et où rechercher l'origine d'un problème**.

## Objectifs

- Déployer une plateforme d'observabilité.
- Intégrer les systèmes existants.
- Collecter leurs métriques.
- Centraliser leurs journaux.
- Vérifier la disponibilité des services.
- Construire une première vision synthétique de l'infrastructure.

## Périmètre d'intervention

Vous intervenez sur **l'infrastructure de préproduction**, afin de préparer la future mise en production.

Appuyez-vous autant que possible sur l'infrastructure et les services déjà produits lors des modules précédents. L'inventaire de départ devra préciser les machines et les services réellement disponibles, ceux qui sont retenus pour cette mission et ceux qui restent à préparer.

!!! note "Statut de cette feuille"
    Cette feuille présente le cadrage et les résultats attendus de la mission. Elle ne constitue pas une preuve de déploiement ou de collecte déjà réalisés.

### Adaptation au laboratoire local

Le laboratoire de préproduction sera hébergé directement sur le **laptop**, avec **virt-manager** pour gérer les machines virtuelles. Le périmètre prévu comprend une **VM Debian** et une **VM Windows Server**. Une troisième VM dédiée à la supervision est envisagée, mais ce choix reste à confirmer.

Ces éléments décrivent l'organisation prévue du laboratoire ; l'installation des VM et les services disponibles seront renseignés au fil des travaux. Le laptop constitue aussi un point d'observation : ses ressources sont partagées entre les VM.

## Problématique

**Comment observer une infrastructure hétérogène depuis un point central sans devoir contrôler manuellement chaque machine et chaque service ?**

## Travaux à mener

Afin de pouvoir superviser l'infrastructure, il est nécessaire de :

1. **Déployer des outils d'observabilité**, dans le cadre du socle Prometheus, Grafana et ELK prévu par le module.
2. **Intégrer des endpoints à la supervision et au monitoring** : les machines et systèmes Linux et Windows retenus dans le périmètre.
3. **Configurer leurs métriques**, en sélectionnant les indicateurs utiles pour observer leur état et leurs performances.

La mission comprend également la centralisation des journaux, les contrôles de disponibilité et la construction d'une première vue synthétique. Ces travaux doivent permettre à l'exploitation de repérer un problème et d'orienter ses recherches vers les machines ou services concernés.

## Dossier de déploiement et de configuration

**Tout au long de cette mission, consignez vos choix, méthodes et procédures dans un dossier de déploiement et de configuration.**

Le dossier sera enrichi au fil des manipulations, avec les éléments suivants :

| Rubrique | Éléments à consigner |
| --- | --- |
| Périmètre et inventaire | Machines Linux et Windows, services, applications et éléments repris des modules précédents. |
| Choix d'architecture | Outils retenus, emplacement des composants, flux nécessaires et justification des choix. |
| Déploiement | Prérequis, versions effectivement utilisées, étapes d'installation et configurations utiles. |
| Intégration des systèmes | Méthode d'intégration de chaque endpoint et vérification de sa visibilité depuis la plateforme. |
| Métriques | Indicateurs collectés, source, fréquence de collecte configurée et intérêt pour l'exploitation. |
| Journaux | Sources intégrées, méthode de collecte et recherches permettant de retrouver les événements. |
| Sondes | Services contrôlés, type de vérification et résultat attendu. |
| Vue synthétique | Tableaux de bord créés, indicateurs affichés et mode de lecture. |
| Validation | Tests effectués, résultats observés, preuves datées, écarts et corrections. |

Pour chaque manipulation, conserver une trace simple : **objectif → méthode → configuration → vérification → résultat observé**. Distinguer les actions réalisées, les actions prévues et les éventuels tests simulés. Les extraits de configuration et les captures doivent être expurgés des secrets et des identifiants inutiles.

## Résultat attendu en fin d'itération

Depuis la plateforme centralisée, l'équipe d'exploitation doit pouvoir :

- identifier les systèmes intégrés et vérifier la remontée de leurs métriques ;
- consulter les journaux des sources configurées ;
- connaître le résultat des contrôles de disponibilité des services ;
- lire une première synthèse de l'état de l'infrastructure ;
- retrouver les choix et les procédures dans le dossier de déploiement.

Les preuves à conserver pourront inclure la liste des systèmes intégrés, une consultation de métriques, une recherche de journaux, les résultats des sondes et une capture de la vue synthétique. Chaque preuve devra correspondre à une vérification effectivement réalisée.

[Retour au sommaire de l'itération](index.md)
