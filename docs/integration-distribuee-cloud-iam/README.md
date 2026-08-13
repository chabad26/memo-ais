# Intégration distribuée : Cloud & IAM

!!! info "Nouveau module"
    Ce module prolonge l'infrastructure **DIST-01a on-premise** vers le cloud. Le sujet n'est pas de découvrir un outil isolé, mais de reprendre le même projet sur un nouveau terrain : deux fournisseurs cloud, une automatisation complète, une gestion stricte des identités et des secrets.

## Objectif global

Ce module fait passer l'infrastructure construite en on-premise vers une infrastructure cloud déployée sur deux fournisseurs :

- **OVH**, fournisseur européen ;
- **AWS**, fournisseur non européen.

L'objectif est de savoir justifier une architecture cloud, automatiser son déploiement de bout en bout avec **OpenTofu** et **Ansible**, puis sécuriser l'ensemble avec une gestion rigoureuse des identités, des accès et des secrets.

En fin de module, tu dois être capable d'expliquer non seulement ce qui a été déployé, mais aussi pourquoi ce choix est cohérent : modèle cloud utilisé, responsabilités du fournisseur et du client, dépendances migrées, niveau de souveraineté, sécurité appliquée et capacité de reprise après incident.

## Fil conducteur

Le fil conducteur reste la migration de l'infrastructure **DIST-01a**.

La démarche est volontairement répétée sur deux fournisseurs pour éviter de dépendre d'une seule plateforme. Ce qui compte n'est pas uniquement la syntaxe AWS, OVH, OpenTofu ou Ansible, mais la méthode :

1. comprendre l'existant ;
2. comparer les options cloud ;
3. créer manuellement un premier socle ;
4. automatiser le provisionnement ;
5. configurer les services ;
6. sécuriser les identités et les secrets ;
7. tester, restaurer, mesurer et documenter.

Cette répétition permet de distinguer ce qui est propre à un fournisseur de ce qui relève d'une vraie compétence d'architecte et d'intégrateur cloud.

## Ce que le module fait travailler

| Axe | Ce qu'il faut comprendre |
| --- | --- |
| Modèles cloud | Différencier IaaS, PaaS, SaaS et relier chaque modèle au partage des responsabilités. |
| Migration | Analyser l'infrastructure existante, ses dépendances et les services à déplacer ou adapter. |
| Fournisseurs | Comparer OVH et AWS selon les critères techniques, économiques, juridiques et de souveraineté. |
| Infrastructure as Code | Provisionner une infrastructure reproductible avec OpenTofu, versionnée dans Git. |
| Configuration as Code | Installer et configurer les services avec Ansible après le provisionnement. |
| IAM | Gérer utilisateurs, groupes, rôles, MFA et identités de service selon le moindre privilège. |
| Secrets | Protéger les secrets avec SOPS et git-crypt, sans les exposer dans le dépôt. |
| Sécurité cloud | Chiffrer les données au repos, sécuriser les flux et contrôler les accès réseau. |
| Exploitation | Restaurer un service après incident et mesurer objectivement un RTO et un RPO. |

## Notions clés

### Responsabilité partagée

Dans le cloud, le fournisseur ne sécurise pas tout. Il prend en charge une partie de l'infrastructure, mais le client reste responsable de ses configurations, de ses identités, de ses données, de ses secrets et de ses choix d'exposition réseau.

Comprendre cette frontière est essentiel pour éviter les fausses impressions de sécurité.

### Souveraineté numérique

Le choix entre OVH et AWS ne se limite pas à une comparaison technique. Il pose aussi des questions de localisation des données, de cadre juridique, de dépendance fournisseur et de conformité attendue par le métier.

Le module doit permettre de justifier ces arbitrages devant un jury.

### Automatisation reproductible

L'automatisation ne sert pas seulement à aller plus vite. Elle sert surtout à rendre l'infrastructure lisible, rejouable, contrôlable et auditable.

OpenTofu décrit les ressources cloud à créer. Ansible configure les systèmes et services une fois les ressources disponibles. Git garde la trace des choix et des évolutions.

### IAM et moindre privilège

L'IAM cloud devient un point central de sécurité. Chaque utilisateur, rôle ou identité de service doit avoir uniquement les droits nécessaires à sa mission.

Le module fait travailler la séparation des rôles, l'activation du MFA, la gestion des comptes de service et la réduction des permissions excessives.

### Secrets et chiffrement

Les secrets ne doivent pas être stockés en clair dans le dépôt. Les outils comme SOPS et git-crypt permettent de versionner des fichiers sensibles tout en gardant leur contenu chiffré.

La sécurité attendue couvre aussi le chiffrement des données au repos et la protection des échanges réseau.

## Progression du module

| Étape | Orientation |
| --- | --- |
| [1. Préparer la migration](it-1/preparer-migration.md) | Analyser l'existant DIST-01a, préparer les comptes cloud et installer les outils. |
| [1. Comprendre les modèles cloud](it-1/comprendre-modeles-cloud-responsabilite.md) | Distinguer IaaS, PaaS, SaaS et le modèle de responsabilité partagée. |
| [1. Classer les services](it-1/classer-services-responsabilites.md) | Situer des services dans IaaS, PaaS ou SaaS et identifier la responsabilité OS. |
| [1. Analyser les dépendances](it-1/analyser-dependances-infrastructure.md) | Cartographier les dépendances DIST-01a avant de décider l'ordre de migration. |
| [1. Estimer les coûts de migration](it-1/estimer-comparer-couts-migration.md) | Comparer le coût mensuel OVHcloud et AWS avec hypothèses datées. |
| [1. Comprendre les enjeux juridiques](it-1/comprendre-enjeux-juridiques-cloud.md) | Relier Cloud Act, RGPD et souveraineté au choix du fournisseur cloud. |
| [1. Rédiger une note de cadrage](it-1/rediger-note-cadrage-migration.md) | Produire une note courte pour faire valider le principe de migration par la direction. |
| [1. Lire et interpréter un SLA cloud](it-1/lire-interpreter-sla-cloud.md) | Comprendre disponibilité, exclusions, responsabilités client et compensations. |
| [1. Produire les livrables DIST01b](it-1/produire-livrables-dist01b-plan-migration.md) | Consolider plan de migration, matrice pondérée et note de cadrage. |
| [2. Déployer et automatiser OVH](it-2/deployer-automatiser-ovh.md) | Créer le socle cloud du premier fournisseur, puis l'automatiser avec OpenTofu et Ansible. |
| [2. Construire un réseau isolé OVH à la main](it-2/construire-reseau-isole-ovh.md) | Créer manuellement réseau privé, sous-réseau, VM Ubuntu et security group minimal avant automatisation. |
| [2. Comprendre l'IaC et le cycle OpenTofu](it-2/comprendre-iac-cycle-opentofu.md) | Comprendre providers, fichiers `.tf`, état et commandes `init`, `plan`, `apply`, `destroy`. |
| 3. Migrer et sécuriser l'IAM | Configurer les accès, les rôles, le MFA, les identités de service et les secrets. |
| 4. Reproduire sur le second fournisseur | Porter l'infrastructure, comparer les écarts et adapter la méthode. |
| 5. Exploiter et clôturer | Superviser, gérer un incident, mesurer RTO/RPO et documenter les choix. |

## Livrables attendus

Les livrables du module doivent permettre de prouver la démarche, pas seulement le résultat final :

- une analyse de l'infrastructure DIST-01a à migrer ;
- une matrice de décision comparant OVH et AWS ;
- un plan de migration argumenté ;
- un dépôt Git contenant le code OpenTofu et Ansible ;
- une documentation IAM : utilisateurs, groupes, rôles, MFA et identités de service ;
- une stratégie de gestion des secrets avec SOPS et git-crypt ;
- des preuves de chiffrement au repos et en transit ;
- des captures ou sorties de validation des déploiements ;
- un scénario d'incident et de restauration ;
- des mesures RTO/RPO et les écarts constatés.

## En fin de module

Tu dois être capable de migrer, automatiser et sécuriser une infrastructure sur deux fournisseurs cloud différents, puis de défendre chaque choix devant un jury.

La compétence visée n'est pas seulement de "faire marcher" une plateforme cloud. Elle consiste à construire une trajectoire de migration claire, automatisée, sécurisée, documentée et justifiable.
