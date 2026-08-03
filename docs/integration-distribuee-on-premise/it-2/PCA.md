# Plan de Continuité d'Activité (PCA)

**Société :** Embedded Solutions  
**Version :** 2.3  
**Date :** Juin 2021  
**Classification :** Interne  
**Responsable du document :** Responsable Informatique

---

## 1. Objet

Le présent Plan de Continuité d'Activité (PCA) décrit les dispositions permettant d'assurer le maintien des activités essentielles de la société Embedded Solutions lors d'un incident affectant le système d'information.

Il couvre les principaux services d'infrastructure utilisés par les collaborateurs de l'entreprise.

## 2. Périmètre

Les services suivants sont couverts par le présent document :

- Authentification des utilisateurs
- Partage de fichiers
- Messagerie électronique
- Sauvegardes
- Supervision de l'infrastructure

Les services suivants disposent de procédures spécifiques et ne sont pas détaillés dans ce document :

- ERP
- Serveurs Git
- Ferme de compilation Linux
- Plateforme de tests automatiques
- Réseau industriel
- VPN
- Wi-Fi
- Téléphonie IP

## 3. Objectifs de continuité

| Service | Priorité | Temps maximal d'interruption |
| ---------- | ---------- | ----------------------------- |
| Authentification | Haute | 4 heures |
| Partage de fichiers | Haute | 8 heures |
| Messagerie | Moyenne | 24 heures |
| Sauvegardes | Haute | 24 heures |
| Supervision | Faible | 48 heures |

## 4. Authentification des utilisateurs

### Description

Les collaborateurs s'authentifient sur le domaine Windows de l'entreprise.

Le contrôleur de domaine fournit :

- l'authentification des utilisateurs ;
- la gestion des comptes ;
- la gestion des groupes de sécurité.

### Mesures de continuité

En cas d'indisponibilité du serveur :

- les utilisateurs déjà connectés peuvent continuer à travailler localement ;
- les nouvelles connexions peuvent être limitées ;
- les administrateurs doivent rétablir le serveur dans les meilleurs délais.

Le contrôleur de domaine est sauvegardé quotidiennement.

## 5. Partage de fichiers

### Description

Les documents sont stockés sur un serveur de fichiers Windows accessible depuis les postes de travail.

Les principaux espaces de partage sont :

- Bureau d'études
- Développement
- Validation
- Administration

### Mesures de continuité

En cas d'interruption :

- utiliser les copies locales lorsque cela est possible ;
- suspendre les modifications des documents partagés ;
- informer les utilisateurs ;
- rétablir le serveur de fichiers en priorité.

## 6. Messagerie électronique

### Description

La messagerie électronique est utilisée pour les échanges avec les clients, fournisseurs et collaborateurs.

### Mesures de continuité

En cas d'indisponibilité :

- privilégier les communications téléphoniques ;
- utiliser les outils collaboratifs disponibles ;
- informer les utilisateurs de la durée estimée de l'interruption.

## 7. Sauvegardes

### Description

Les serveurs sont sauvegardés chaque nuit sur un serveur de sauvegarde dédié.

Une copie hebdomadaire est réalisée sur un disque externe conservé dans un local sécurisé.

### Vérifications quotidiennes

Chaque matin, l'administrateur vérifie :

- le succès des sauvegardes nocturnes ;
- l'espace disque disponible ;
- les journaux d'erreur.

## 8. Supervision

### Description

Les principaux serveurs sont supervisés par une solution de supervision centralisée.

Les alertes sont transmises par courrier électronique à l'équipe informatique.

### Mesures de continuité

En cas d'indisponibilité de la supervision :

- surveiller quotidiennement les serveurs ;
- contrôler manuellement les journaux système ;
- vérifier les sauvegardes.

## 9. Services hors périmètre

Les services suivants sont exploités par l'entreprise mais disposent de procédures spécifiques :

| Service | Commentaire |
| ---------- | ------------- |
| ERP | Documentation dédiée |
| Serveurs Git | Administrés par l'équipe développement |
| Ferme de compilation Linux | Documentation spécifique de l'équipe embarquée |
| Plateforme de tests automatiques | Procédures internes du bureau d'études |
| VPN | Documentation réseau |
| Wi-Fi | Documentation réseau |
| Téléphonie IP | Prestataire externe |

## 10. Responsabilités

Le Responsable Informatique est chargé :

- du maintien à jour du présent document ;
- de l'organisation des tests de continuité ;
- de la coordination des opérations en cas d'incident.

Les administrateurs système appliquent les procédures décrites dans ce document et signalent toute évolution de l'infrastructure nécessitant une mise à jour du PCA.

## 11. Révision du document

Le présent document est révisé :

- après toute évolution majeure de l'infrastructure ;
- après un incident significatif ;
- au minimum une fois par an.

## 12. Historique des versions

| Version | Date | Auteur | Description |
| ---------- | ------ | --------- | ------------- |
| 1.0 | Avril 2018 | Service informatique | Création du document |
| 2.0 | Mars 2020 | Service informatique | Ajout de la supervision |
| 2.3 | Juin 2021 | Responsable informatique | Mise à jour de l'inventaire des services |

## Mise à jour du projet — 3 août 2026

### Annuaire OpenLDAP

L'annuaire OpenLDAP est ajouté au périmètre technique du projet. Il fournit une base centralisée pour la gestion future des utilisateurs, groupes et comptes techniques.

| Élément | État actuel |
| --- | --- |
| Image | osixia/openldap:2.6.10-alpha |
| Base DN | dc=embedded,dc=local |
| DN administrateur | cn=admin,dc=embedded,dc=local |
| Accès LDAP | Port hôte 389 vers port conteneur 3890 |
| Persistance | Volumes ldap_data, ldap_config et ldap_backups |
| Déploiement | Docker Compose dans ~/on-premise/openldap |
| Vérification | Conteneur actif et authentification administrateur testée |

### Mesures de continuité

- conserver compose.yaml, .env.example et .gitignore dans le dépôt Git ;
- conserver le fichier .env dans un emplacement protégé, sans l'ajouter au dépôt ;
- maintenir les volumes LDAP sur un stockage sauvegardé ;
- documenter le mot de passe administrateur dans l'emplacement sécurisé prévu ;
- vérifier régulièrement l'état du conteneur, les journaux et une recherche LDAP ;
- prévoir une solution de fonctionnement dégradé si l'annuaire est indisponible.

L'annuaire devient une dépendance pour les futurs services utilisant l'authentification centralisée. Les comptes, groupes, sauvegardes et tests de restauration restent à documenter au fur et à mesure du projet.

La structure initiale de l'annuaire comprend désormais les unités `ou=People,dc=embedded,dc=local` pour les utilisateurs et `ou=Groups,dc=embedded,dc=local` pour les groupes. Ces unités devront être incluses dans les contrôles de disponibilité et les sauvegardes LDAP.

**Version de suivi :** 2.4 — août 2026 — ajout du service OpenLDAP et de ses mesures de continuité.

## Mise à jour du projet — LDAP Account Manager

LDAP Account Manager (LAM) est ajouté comme interface d'administration de l'annuaire. Il ne remplace pas OpenLDAP et n'est pas une dépendance à la disponibilité de l'annuaire : OpenLDAP reste le service prioritaire.

Paramètres observés :

- image ghcr.io/ldapaccountmanager/lam:9.6 ;
- port Web publié : 8081 ;
- serveur LDAP utilisé : ldap://openldap:3890 ;
- réseau Docker : openldap_default ;
- base DN : dc=embedded,dc=local ;
- DN d'administration : cn=admin,dc=embedded,dc=local.

Mesures de continuité :

- conserver le Compose et le fichier .env.example ;
- protéger le mot de passe LAM et le mot de passe LDAP ;
- conserver une procédure d'administration en ligne de commande ;
- maintenir l'accès à OpenLDAP même si l'interface LAM est indisponible ;
- ne pas exposer LAM directement sur Internet ;
- prévoir HTTPS et un contrôle d'accès dans un environnement réel.

LAM est classé comme outil d'administration à priorité secondaire. Sa reconstruction est nécessaire pour le confort d'administration, mais son indisponibilité ne doit pas empêcher l'accès direct à l'annuaire par les outils LDAP.

## Validation de la structure LDAP — 3 août 2026

La structure LDAP prévue pour l'entreprise a été créée avec LAM puis vérifiée
avec une recherche LDAP.

- 6 groupes sont présents dans `ou=Groups` : `grp-administration`,
  `grp-bureau-etudes`, `grp-developpement`, `grp-direction`,
  `grp-informatique` et `grp-integration` ;
- 6 utilisateurs de laboratoire sont présents dans `ou=People` : `amartin`,
  `bdupont`, `cdurand`, `dbernard`, `erobert` et `oadmin` ;
- les UID et GID sont visibles dans LAM ;
- la recherche LDAP se termine par `result: 0 Success`.

Cette validation confirme que l'annuaire peut fournir une base centralisée pour
les futures authentifications et autorisations. Les captures sont conservées
dans la feuille de l'activité LDAP. La sauvegarde et la restauration des
volumes LDAP restent à tester séparément.
