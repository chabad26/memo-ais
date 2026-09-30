# Vulnérabilité ou autre problème ?

**Durée prévue : 30 minutes.**

## Objectif

Distinguer différents types de constats de sécurité avant d'interpréter les
résultats d'un scanner.

**Statut : réponses de l'apprenant relues et précisées avec l'assistant.**
Les quatre classements proposés sont corrects. Les situations ci-dessous sont
des cas pédagogiques fournis par le formateur, pas des constats d'audit de la VM.

## Consigne

Pour chaque situation, déterminer la catégorie principale, justifier le choix
et relever les informations nécessaires avant de décider d'une action :

- vulnérabilité logicielle ;
- défaut de configuration ;
- version ancienne sans vulnérabilité démontrée ;
- service inutilement exposé.

## Situation A — Connexion SSH directe de root

> Un serveur SSH autorise la connexion directe du compte `root` par mot de passe.

**Classement : défaut de configuration.**

Le choix de l'apprenant est correct. Cette configuration permet une connexion
directe à un compte très privilégié avec un mot de passe et limite la traçabilité
individuelle lorsque le compte est partagé. Le constat porte sur un réglage
d'accès, sans démontrer un défaut du logiciel SSH.

**Précision apportée :** l'énoncé indique une connexion **par mot de passe**,
pas une connexion sans mot de passe. La formulation « root ne doit jamais être
accessible via SSH » est trop absolue. On privilégie généralement des comptes
nominatifs et une élévation des privilèges via `sudo` ; un éventuel besoin de
connexion directe doit être justifié et encadré.

**Informations à recueillir avant d'agir :**

- exposition de SSH : Internet, réseau interne ou réseau d'administration ;
- méthodes d'authentification et restrictions d'accès réellement appliquées ;
- comptes nominatifs disponibles et droits `sudo` ;
- besoin particulier d'un accès direct, notamment pour une automatisation ;
- autre accès administrateur testé avant de modifier la connexion de `root`.

## Situation B — Bibliothèque concernée par une CVE

> Une application utilise une bibliothèque pour laquelle une CVE indique que
> la version installée est vulnérable dans certaines conditions.

**Classement : vulnérabilité logicielle, dont l'applicabilité reste à confirmer.**

Le choix de l'apprenant est correct : la CVE décrit un défaut du logiciel.
Sa proposition de vérifier si l'environnement permet l'exploitation est
pertinente. La présence d'une version concernée ne prouve pas à elle seule que
les conditions d'exploitation sont réunies dans cette application.

**Informations à recueillir avant d'agir :**

- version exacte, provenance du paquet et éventuels correctifs déjà intégrés ;
- versions affectées et conditions décrites dans l'avis de sécurité ;
- présence et utilisation de la fonctionnalité vulnérable ;
- exposition de cette fonctionnalité et droits nécessaires à l'exploitation ;
- impact possible, correctif disponible et compatibilité avec l'application.

L'absence d'une condition d'exploitation peut réduire le risque dans le contexte
observé ; elle ne signifie pas que le défaut logiciel a été corrigé.

## Situation C — Logiciel publié il y a quatre ans

> Un serveur utilise une version d'un logiciel publiée il y a quatre ans.
> Vous ne disposez d'aucune information montrant qu'elle contient une
> vulnérabilité connue.

**Classement : version ancienne sans vulnérabilité démontrée.**

Le choix de l'apprenant est correct. L'âge d'une version ne suffit pas à
démontrer une vulnérabilité. Il ne prouve pas non plus son innocuité.
La priorité d'une mise à jour ou d'une migration doit reposer sur des éléments
complémentaires, plutôt que sur la seule date de publication.

**Informations à recueillir avant d'agir :**

- statut du support et maintien des mises à jour de sécurité ;
- version exacte, correctifs intégrés et avis de sécurité applicables ;
- exposition du service, criticité et données traitées ;
- compatibilité des dépendances et contraintes d'une mise à jour ;
- possibilité de tester le changement et de revenir en arrière.

Une migration peut être justifiée pour retrouver un logiciel maintenu, même
sans vulnérabilité connue démontrée à cet instant.

## Situation D — Administration accessible depuis Internet

> Un service d'administration est accessible depuis Internet alors que les
> administrateurs l'utilisent uniquement depuis le réseau interne.

**Classement : service inutilement exposé.**

Le choix de l'apprenant est correct : l'accès depuis Internet dépasse le besoin
décrit et augmente la surface d'attaque, même si le logiciel est à jour.
Rechercher pourquoi le service est exposé est une bonne démarche.

**Précision apportée :** le télétravail est un besoin à vérifier, pas un besoin
établi dans l'énoncé. Même lorsqu'un accès distant est nécessaire, il ne justifie
pas automatiquement une exposition directe du service ; un accès via VPN peut
répondre au besoin.

**Informations à recueillir avant d'agir :**

- utilisateurs concernés et besoin réel d'accès distant ;
- raison et responsable de la publication sur Internet ;
- interfaces d'écoute, règles de pare-feu et éventuelles redirections de ports ;
- accès distant sécurisé déjà disponible et restrictions existantes ;
- dépendances ou automatisations qui pourraient être affectées par la fermeture.

Si aucun besoin externe n'est confirmé, restreindre l'accès au réseau autorisé,
puis vérifier que l'administration fonctionne toujours depuis ce réseau.

## Synthèse des réponses

| Situation | Catégorie principale | Point décisif avant une action |
| --- | --- | --- |
| A | Défaut de configuration | Vérifier les accès nécessaires et conserver un autre accès administrateur |
| B | Vulnérabilité logicielle | Confirmer la version affectée et les conditions d'exploitation |
| C | Version ancienne sans vulnérabilité démontrée | Vérifier le support, les correctifs et les avis de sécurité |
| D | Service inutilement exposé | Confirmer le besoin et limiter l'accès au périmètre utile |

Ces catégories servent à qualifier le **problème principal**. Elles peuvent
se recouper : une exposition inutile peut découler d'un défaut de configuration,
et un logiciel vulnérable peut aussi être inutilement exposé.

## Résultat attendu et trace du travail

La réponse à conserver comprend les quatre classements, leurs justifications
et les informations manquantes avant décision. Cette fiche reprend les choix
de l'apprenant et distingue les précisions ajoutées lors de la relecture.
Aucun scan ni test d'exploitation n'est demandé pour cet exercice.

- [Activité précédente — Préparer la cible et installer Greenbone](preparer-cible-installer-greenbone.md)
- [Activité suivante — Lire et analyser trois entrées CVE](lire-analyser-entrees-cve.md)
- [Retour à l'itération 1 — Auditer et prioriser](index.md)
- [Pense-bête de l'itération](../../pense-bete/glossaire/securisation-avancee-infrastructures/it-1.md)
- [Retour au module](../README.md)
