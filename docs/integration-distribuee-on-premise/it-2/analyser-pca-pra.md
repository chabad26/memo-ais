# Découvrir le PCA et le PRA de l'entreprise

## Objectif

Analyser les extraits du Plan de Continuité d'Activité (PCA) et du Plan de Reprise d'Activité (PRA) fournis par l'entreprise.

Les documents datent de 2021. Ils décrivent une infrastructure qui a évolué depuis leur rédaction. Cette activité consiste à identifier les informations valides, les écarts et les mises à jour à prévoir.

!!! warning "Documents de référence"
    Les extraits du PCA et du PRA ne doivent pas être modifiés pendant cette activité. Cette fiche constitue uniquement le document de synthèse préparatoire.

## Spécifications

- Travail en binôme.
- Les extraits du PCA et du PRA sont fournis.
- Les documents ont été rédigés il y a environ cinq ans.
- Les mises à jour seront réalisées progressivement pendant le projet.
- Les hypothèses non confirmées doivent être signalées comme des points à valider.

## 1. Services décrits dans les documents

Les deux documents couvrent les services suivants :

| Service | PCA | PRA | Rôle |
| --- | --- | --- | --- |
| Authentification | Oui | Oui | Connexion des utilisateurs et gestion des identités. |
| Partage de fichiers | Oui | Oui | Accès aux documents de travail. |
| Messagerie | Oui | Oui | Échanges internes et externes. |
| Sauvegardes | Oui | Oui | Protection et restauration des données. |
| Supervision | Oui | Oui | Détection des incidents et suivi de l'infrastructure. |
| ERP | Hors périmètre | Procédure spécifique | Application métier non détaillée. |
| Serveurs Git | Hors périmètre | Procédure spécifique | Gestion du code et des versions. |
| Compilation Linux | Hors périmètre | Procédure spécifique | Production des logiciels embarqués. |
| Plateforme de tests | Hors périmètre | Procédure spécifique | Validation des logiciels. |
| Réseau, VPN et Wi-Fi | Hors périmètre | Non détaillé | Services nécessaires aux accès et aux communications. |
| Téléphonie IP | Hors périmètre | Non détaillé | Service fourni ou maintenu par un prestataire. |

## 2. Informations qui restent exploitables

Certaines informations des documents restent utiles comme base de travail :

- l'authentification est une dépendance prioritaire ;
- le partage de fichiers est nécessaire aux équipes ;
- les sauvegardes doivent être vérifiées régulièrement ;
- la supervision facilite la détection des incidents ;
- le PRA doit prévoir une identification de l'incident, une priorisation, une restauration et une validation ;
- le Responsable Informatique coordonne la décision de déclenchement ;
- le PCA et le PRA doivent être révisés après une évolution importante ou un incident ;
- les documents associés doivent comprendre un inventaire, les sauvegardes et les contrats utiles.

Ces principes peuvent être conservés, mais les informations techniques doivent être vérifiées avant réutilisation.

## 3. Écarts identifiés dans le PCA et le PRA

| Domaine | Information ancienne | Écart ou risque | Mise à jour à prévoir | Priorité |
| --- | --- | --- | --- | --- |
| Version et date | PCA 2.3 de juin 2021, PRA 1.8.1 de juillet 2021 | Documents anciens et historique incomplet. | Mettre à jour les versions, dates, auteurs et validation. | P1 |
| Infrastructure | Serveurs et machines virtuelles décrits de manière générale. | L'inventaire actuel, les dépendances et les supports ne sont pas détaillés. | Refaire l'inventaire des hôtes, VM, conteneurs, volumes et réseaux. | P1 |
| Authentification | Contrôleur de domaine Windows repris comme seule référence. | Le périmètre actuel peut inclure plusieurs services d'identité et des dépendances DNS. | Documenter le domaine, le DNS, les OU, les groupes, les comptes et les contrôleurs réellement présents. | P1 |
| Partage de fichiers | Serveur de fichiers Windows avec quatre espaces métiers. | Les noms des serveurs, partages, groupes et droits ne sont pas précisés. | Ajouter la matrice groupes/ressources, les chemins, les droits NTFS/SMB et la procédure de restauration. | P1 |
| Sauvegardes | Sauvegarde nocturne et copie hebdomadaire sur disque externe. | RPO, RTO, rétention, chiffrement, emplacement et test de restauration absents. | Décrire la stratégie, les supports, la fréquence, la rétention et les tests de restauration. | P1 |
| Virtualisation | Restauration de machines virtuelles prévue. | Une machine physique Ubuntu ne peut pas être restaurée par snapshot d'hyperviseur. | Distinguer VM, machine physique, image disque, sauvegarde externe et snapshot LVM/Btrfs si applicable. | P1 |
| Docker | Aucun conteneur ni volume n'est décrit. | WordPress, MariaDB, Nginx et les volumes actuels ne figurent pas dans les plans. | Ajouter les services Docker, leurs images, ports, réseaux, volumes et procédures de reprise. | P1 |
| Git | Serveurs Git seulement mentionnés hors périmètre. | La documentation et les scripts du projet utilisent maintenant un dépôt Git local. | Définir ce qui est versionné, les commits attendus, les sauvegardes du dépôt et les accès. | P2 |
| WordPress/MariaDB | Aucun service Web ou base MariaDB dans le périmètre. | Le projet contient un service Web et une base persistante. | Décrire le volume MariaDB, la sauvegarde de la base et la reconstruction avec Compose. | P1 |
| Nginx | Aucun serveur Web de test décrit. | Le conteneur Nginx et son Dockerfile ne sont pas inventoriés. | Ajouter l'image, le port publié, le fichier de configuration et le test HTTP. | P2 |
| Réseau | VPN, Wi-Fi et réseau industriel renvoyés à d'autres documents. | Les dépendances réseau entre services ne sont pas représentées. | Ajouter DNS, réseau Compose, ports, flux autorisés et dépendances critiques. | P1 |
| Supervision | Alertes transmises par courrier électronique. | Le mécanisme, les destinataires et le fonctionnement en cas de panne de la messagerie ne sont pas décrits. | Identifier l'outil, les sondes, les alertes alternatives et les vérifications manuelles. | P2 |
| Messagerie | SMTP et IMAP doivent être vérifiés après restauration. | Serveur, fournisseur, DNS, relais et données à restaurer non précisés. | Confirmer le service réellement utilisé et sa procédure de reprise. | P2 |
| Contacts | Téléphones et contrats renvoient à des documents externes. | Les coordonnées de crise ne sont pas immédiatement disponibles dans le plan. | Vérifier les contacts, les astreintes et les contrats. | P2 |
| Tests | Révision annuelle prévue. | Aucun résultat d'exercice, scénario testé ou date de dernier test n'est fourni. | Ajouter un calendrier d'exercices et les comptes rendus de validation. | P2 |

## 4. Services ou procédures devenus incomplets

### 4.1 Reprise du contrôleur de domaine

La procédure indique seulement de restaurer une machine virtuelle puis de vérifier Active Directory.

Informations manquantes :

- nom et adresse du contrôleur ;
- rôle DNS associé ;
- emplacement et méthode de sauvegarde ;
- mot de passe DSRM ;
- ordre de reprise en présence de plusieurs contrôleurs ;
- vérification des enregistrements DNS et des rôles AD ;
- procédure de restauration autorisée.

### 4.2 Reprise du serveur de fichiers

La procédure ne précise pas les permissions à restaurer.

Informations manquantes :

- nom du serveur ;
- chemins des données ;
- noms des partages ;
- groupes autorisés ;
- droits NTFS et SMB ;
- dernière sauvegarde valide ;
- test de restauration d'un fichier ;
- validation par un responsable métier.

### 4.3 Reprise des sauvegardes

Le PRA prévoit de restaurer le serveur de sauvegarde, mais ne précise pas comment accéder aux copies si ce serveur est indisponible.

Point à clarifier :

- les sauvegardes externes doivent pouvoir être utilisées indépendamment du serveur de sauvegarde principal.

### 4.4 Reprise de WordPress et MariaDB

La procédure actuelle ne décrit pas le déploiement Compose.

À prévoir :

1. restaurer le fichier Compose et le fichier d'exemple des variables ;
2. récupérer les vraies variables dans un emplacement protégé ;
3. restaurer le volume ou l'export MariaDB ;
4. relancer les services ;
5. vérifier la résolution DNS de MariaDB par WordPress ;
6. vérifier l'accès Web et les données applicatives.

### 4.5 Reprise d'un service Nginx

Le Dockerfile, la page Web et le port publié doivent être conservés dans le dépôt ou dans une sauvegarde de projet.

Le PRA doit distinguer :

- reconstruction de l'image à partir du Dockerfile ;
- recréation du conteneur ;
- restauration des données éventuelles ;
- vérification HTTP.

## 5. Nouveaux services à intégrer pendant le projet

Les services suivants devront être ajoutés aux documents s'ils restent présents dans l'architecture finale :

- Docker Engine et Docker Compose ;
- conteneur Nginx ;
- WordPress ;
- MariaDB ;
- volumes Docker ;
- réseaux Docker et résolution DNS entre services ;
- dépôt Git local de documentation et de scripts ;
- serveur de fichiers sécurisé ;
- Active Directory et DNS ;
- services de sauvegarde ;
- supervision ;
- éventuellement messagerie, VPN, Wi-Fi et autres services réseau.

Pour chaque service, il faudra documenter :

- son rôle ;
- ses dépendances ;
- son emplacement ;
- ses données persistantes ;
- son mode de sauvegarde ;
- son ordre de reprise ;
- son test de fonctionnement ;
- son propriétaire ou responsable de validation.

## 6. Priorité des mises à jour

### Priorité P1 - Avant toute validation de reprise

1. Mettre à jour l'inventaire réel de l'infrastructure.
2. Confirmer les services réellement présents et leur emplacement.
3. Décrire les dépendances DNS, réseau, identité et stockage.
4. Définir les RTO et RPO avec les responsables métier.
5. Documenter les sauvegardes, la rétention et les tests de restauration.
6. Décrire la reprise d'Active Directory, du DNS et du serveur de fichiers.
7. Ajouter Docker, WordPress, MariaDB, Nginx et les volumes si ces services sont conservés.
8. Distinguer les procédures applicables aux VM et à la machine physique Ubuntu.

### Priorité P2 - Pour rendre le plan exploitable

1. Mettre à jour les contacts et les responsabilités.
2. Décrire la supervision et les alertes de secours.
3. Décrire la messagerie réellement utilisée.
4. Documenter le dépôt Git, sa sauvegarde et sa restauration.
5. Ajouter les tests de fonctionnement et les preuves attendues.
6. Organiser un exercice de reprise et conserver son compte rendu.

### Priorité P3 - Amélioration continue

1. Ajouter les schémas d'architecture et les flux.
2. Ajouter les procédures détaillées par service.
3. Ajouter les modèles de compte rendu d'incident.
4. Automatiser les contrôles d'inventaire et de sauvegarde.
5. Réviser les documents après chaque évolution significative.

## 7. Questions nécessitant des informations complémentaires

Les points suivants doivent être confirmés avant la mise à jour définitive :

- Quels sont les noms et adresses actuels des serveurs ?
- Le domaine Active Directory possède-t-il un ou plusieurs contrôleurs ?
- Quelle est la méthode officielle de sauvegarde d'Active Directory ?
- Quels sont les RTO et RPO validés pour chaque service ?
- Où sont stockées les copies de sauvegarde hors ligne ou hors site ?
- Les sauvegardes sont-elles chiffrées et régulièrement restaurées en test ?
- Quel serveur de fichiers et quels partages sont réellement utilisés ?
- Quels groupes donnent accès aux dossiers métiers ?
- La messagerie est-elle interne ou fournie par un prestataire ?
- Quelle solution de supervision est utilisée et qui reçoit les alertes ?
- Le dépôt Git local doit-il être sauvegardé sur un serveur distant ?
- Le volume MariaDB est-il sauvegardé par export SQL, copie de volume ou les deux ?
- Quelle personne valide la remise en service de chaque application ?
- Quels services sont prioritaires pour les équipes de développement embarqué, d'intégration et de validation ?
- Quels contacts doivent être disponibles en cas d'indisponibilité du réseau ou de la messagerie ?

## Ressources

- [Plan de Continuité d'Activité - ANSSI](https://cyber.gouv.fr/)
- [Tutoriel Docker Compose du projet](../it-1/deployer-wordpress-compose.md)

## Notions acquises

- PCA
- PRA
- RTO
- RPO
- Analyse d'écarts
- Priorisation des mises à jour
- Dépendances d'infrastructure
- Documentation de reprise d'activité

## Récapitulatif final — PCA/PRA et réalité observée

Ce tableau compare les extraits historiques de 2021 avec l'état réellement travaillé dans le module. Il ne constitue pas encore un PCA ou un PRA final : les éléments non vérifiés doivent rester à confirmer.

| Domaine | Ce que décrivent les anciens PCA/PRA | Réalité observée dans le module | Statut |
| --- | --- | --- | --- |
| Support Ubuntu | Non détaillé. | Ubuntu 24.04 est utilisé sur une machine physique. Il n'y a pas de snapshot d'hyperviseur disponible. | Vérifié |
| Docker | Absent des documents. | Docker Engine et Docker Compose sont installés et utilisés pour les travaux. | Vérifié |
| Nginx | Aucun serveur Web de test décrit. | Une image Nginx sert une page HTML via un conteneur et un port publié. | Vérifié en laboratoire |
| WordPress | Absent du PCA et du PRA. | WordPress est déployé avec Docker Compose sur le port 8085. | Vérifié en laboratoire |
| MariaDB | Aucune base de données détaillée. | MariaDB est utilisé comme service WordPress avec le volume nommé db_data. | Vérifié en laboratoire |
| Persistance | Sauvegardes de serveurs décrites de manière générale. | La persistance du volume est vérifiée après docker compose down. La sauvegarde réelle du volume reste à définir. | Partiel |
| Réseau des services | Réseau et dépendances peu détaillés. | Le réseau Compose et la résolution DNS du service db sont vérifiés. | Vérifié en laboratoire |
| Git | Serveurs Git mentionnés hors périmètre. | Un dépôt Git local conserve documentation, Dockerfiles, Compose et scripts. | Vérifié en laboratoire |
| Authentification | Contrôleur de domaine Windows présenté comme service prioritaire. | Aucun contrôleur de domaine ni annuaire LDAP n'est encore validé dans l'itération 1. | À construire et confirmer |
| Partage de fichiers | Serveur Windows avec espaces métiers. | Aucun serveur de fichiers n'est encore déployé dans cette partie du module. | À construire et confirmer |
| Messagerie | Service SMTP/IMAP à restaurer. | Aucun service de messagerie n'est encore déployé ou testé. | À confirmer |
| Sauvegardes | Sauvegardes nocturnes et copie externe hebdomadaire. | La stratégie réelle, les supports, la rétention et les restaurations ne sont pas encore établis. | À définir |
| Supervision | Supervision centralisée avec alertes par courrier électronique. | Aucun outil de supervision ni mécanisme d'alerte n'est encore validé. | À construire et confirmer |
| Virtualisation | Reprise de machines virtuelles prévue. | L'hôte de travail actuel est physique ; une procédure d'image ou de sauvegarde doit remplacer le snapshot VM. | Partiel |
| PCA/PRA | Documents versionnés en 2021 et révisés annuellement. | Une analyse d'écarts est réalisée, mais les plans originaux n'ont pas encore été mis à jour. | En cours |

### Conclusion opérationnelle

La réalité actuelle est un environnement de laboratoire en construction, centré sur Ubuntu, Docker, Nginx, WordPress, MariaDB, les volumes Docker et Git. Les anciens PCA/PRA décrivent surtout une infrastructure serveur Windows avec authentification, fichiers, messagerie, sauvegardes et supervision.

Les plans ne peuvent donc pas être appliqués tels quels à l'environnement actuel. Ils doivent être mis à jour progressivement pour intégrer les services réellement construits, leurs dépendances, leurs données persistantes et leurs méthodes de restauration.

Les points les plus urgents à ajouter sont :

1. l'inventaire réel des hôtes, conteneurs, volumes, réseaux et services ;
2. la sauvegarde et la restauration de MariaDB et des volumes Docker ;
3. la procédure de reconstruction WordPress/Nginx avec Compose ;
4. la procédure de retour adaptée à la machine Ubuntu physique ;
5. l'intégration future de l'annuaire, du serveur de fichiers, de la messagerie et de la supervision ;
6. les RTO/RPO validés et les preuves de tests de reprise.
