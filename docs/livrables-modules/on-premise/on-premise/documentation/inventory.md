# Inventaire initial


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/inventory.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.


| Élément | Type | Port publié | Données persistantes | Répertoire |
| --- | --- | ---: | --- | --- |
| Image figlet | Image Docker | Aucun | Non | dockerfile-demo/ |
| Site Nginx | Conteneur Web | 8080:80 | Non | nginx-demo/ |
| WordPress | Application Web | 8085:80 | Oui, via MariaDB | wordpress-compose/ |
| MariaDB | Base de données | Aucun port publié | Oui, volume db_data | wordpress-compose/ |
| Dépôt Git | Dépôt local | Aucun | Historique des fichiers | ~/on-premise/.git/ |
| OpenLDAP | Annuaire LDAP | 389:3890 | Oui, volumes LDAP | openldap/ |
| LDAP Account Manager | Interface Web d'administration | 8081:80 | Configuration rejouable | ldap-account-manager/ |
| Samba LDAP | Serveur de fichiers SMB autonome | 139, 445 | Oui, volumes samba_config, samba_state et samba_share | samba-ad/ |
| Stack OpenLDAP + LAM | Compose fédérateur de l'annuaire et de son interface | 389, 8081 | Oui, volumes LDAP | infrastructure-compose/ |
| Elasticsearch | Stockage et indexation des journaux | 127.0.0.1:9200 | Oui, volume `monitoring_elasticsearch_data` | monitoring-compose/ |
| Kibana | Visualisation des journaux | 127.0.0.1:5601 | Configuration reproductible | monitoring-compose/ |
| Filebeat | Collecte des journaux Docker et BorgBackup | Aucun | Oui, registre de lecture | monitoring-compose/ |

## Ressources Compose

- Réseau : wordpress-compose_default
- Service base de données : db
- Service Web : wordpress
- Volume : wordpress-compose_db_data
- Accès local : http://localhost:8085

## Fichiers importants

- wordpress-compose/compose.yaml : description des services ;
- wordpress-compose/.env.example : modèle des variables ;
- wordpress-compose/.gitignore : exclusion de .env ;
- wordpress-compose/README.md : procédure de reprise ;
- documentation/ : documents de suivi du module.
- `documentation/technical-files-guide.md` : rôle des Compose, Dockerfiles,
  configurations externes, volumes, réseaux et scripts du module.

## Ressources LDAP

| Élément | Valeur |
| --- | --- |
| Base DN | `dc=embedded,dc=local` |
| Compte administrateur | `cn=admin,dc=embedded,dc=local` |
| Réseau Docker partagé | `openldap_default` |
| Service LDAP | `openldap` |
| Service Web d'administration | `lam` |
| Port Web LAM | `8081` |
| Port LDAP publié | `389` |
| Volumes OpenLDAP | `ldap_data`, `ldap_config`, `ldap_backups` |
| Unités créées | `ou=People`, `ou=Groups`, `ou=Services`, `ou=Computers` |

## Comptes et groupes vérifiés

Six utilisateurs de laboratoire et six groupes ont été vérifiés dans LAM. Le
détail est conservé dans `documentation/users.md`.

## Partages Samba

| Partage | Répertoire conteneur | Groupes autorisés |
|---|---|---|
| `Commun` | `/srv/samba/commun` | groupes de service autorisés |
| `Developpement` | `/srv/samba/developpement` | `grp-developpement` |
| `Bureau-etudes` | `/srv/samba/bureau-etudes` | `grp-bureau-etudes` |
| `Administration` | `/srv/samba/administration` | `grp-administration` |

Le partage technique `partage` est conservé pour les tests historiques.
Le volume `samba_share` contient les données des espaces de partage.
`samba_config` conserve les configurations copiées au démarrage et
`samba_state` conserve l'état interne de Samba.

## Messagerie

| Élément | Type | Port publié | Données persistantes | Répertoire |
|---|---|---:|---|---|
| Postfix | Serveur SMTP et submission | 25, 587 | Oui, file Postfix | `messaging-compose/` |
| Dovecot | Serveur IMAP et LMTP | 143, 993 | Oui, boîtes Maildir | `messaging-compose/` |
| Roundcube | Webmail | 8082 | Oui, configuration | `messaging-compose/` |
| MariaDB Roundcube | Base de données | Aucun port publié | Oui | `messaging-compose/` |

Le schéma et les dépendances sont détaillés dans
`documentation/mail-architecture.md`.

## Documentation de sauvegarde

- `documentation/backup-requirements.md` : exigences issues du PCA/PRA ;
- `documentation/backup-strategy.md` : fréquence, rétention, chiffrement et
  tests de restauration.
- `documentation/backup-implementation.md` : dépôt, script, volumes et
  première sauvegarde ;
- `documentation/restore-procedure.md` : restauration de configuration,
  document Samba, Maildir et volume OpenLDAP ;
- `documentation/backup-automation.md` : cron, journaux et contrôle quotidien ;
- `documentation/backup-strategy-validation.md` : scénario de corruption LDAP
  confronté aux objectifs PCA/PRA ;
- `documentation/incident-majeur-ldap.md` : compte rendu de gestion de crise,
  décisions, rôles et plan d'actions pour l'exercice de compromission LDAP ;
- `documentation/rapport-restauration-pra.md` : rapport d'execution de la
  restauration PRA avec services restaures, RTO observe et RPO estime ;
- `documentation/gestion-certificats-roundcube.md` : operations de revocation,
  CRL, remplacement et validation client du certificat Roundcube compromis ;
- `documentation/retour-experience-pca-pra.md` : compte rendu REX simule,
  difficultes, nouveaux besoins et ameliorations PCA/PRA ;
- `backup/backup.sh`, `run-backup-cron.sh` et `check-backup.sh` : scripts
  opérationnels de l'itération.

## Documentation de supervision

- `documentation/monitoring-requirements.md` : journaux, événements,
  indicateurs et priorités de supervision de l'itération 7 optionnelle ;
- `documentation/logging-architecture.md` : architecture Filebeat,
  Elasticsearch et Kibana, flux de collecte et politique de conservation ;
- `documentation/logging-platform.md` : déploiement, paramètres et tests de
  persistance d'Elasticsearch et Kibana ;
- `documentation/logging-collection.md` : configuration Filebeat, sources et
  résultats de collecte ;
- `documentation/monitoring-dashboards.md` : tableaux de bord Kibana, filtres
  KQL, objectifs d'exploitation et procédure de réimport ;
- `monitoring-compose/` : projet Docker Compose de la plateforme de
  journalisation.
