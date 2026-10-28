# Journal technique


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/journal.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Documentation transversale

- ajout d'un guide expliquant le cycle de lecture d'un projet Compose ;
- distinction entre fichier déclaratif, configuration externe, script et
  données persistantes ;
- description des projets WordPress, LDAP/LAM, Samba, messagerie, BorgBackup
  et supervision ;
- ajout d'un README explicatif dans les projets qui n'en possédaient pas.

## Itération 1

### Préparation

- Création du répertoire principal ~/on-premise.
- Création du dépôt Git local avec git init.
- Création des répertoires de démonstration et de documentation.

### Dockerfile et Figlet

- Construction de l'image figlet-demo:1.0 à partir d'Ubuntu 24.04.
- Exécution de l'image avec docker run.
- Modification du texte puis reconstruction de figlet-demo:2.0.
- Comparaison des images avec docker image ls et docker history.

### Nginx

- Création de la page index.html.
- Création du Dockerfile basé sur nginx:latest.
- Publication du port 8080 vers le port 80 du conteneur.
- Vérification avec curl et un navigateur.
- Arrêt, redémarrage, consultation des logs puis suppression du conteneur.

### WordPress et MariaDB

- Création du projet wordpress-compose.
- Déploiement de MariaDB et WordPress avec Docker Compose.
- Vérification de la résolution DNS du service db.
- Modification du port publié de 8080 vers 8085.
- Suppression et recréation des conteneurs avec conservation du volume db_data.
- Vérification de la persistance de la configuration WordPress.

### Git

- Premier commit : état initial de la documentation et des scripts.
- Second commit : modification du journal technique.
- Vérification de l'historique avec git log.
- Dépôt Git initialisé pour conserver la documentation et les scripts du module.
## Points de vigilance

- Ne jamais ajouter wordpress-compose/.env à Git.
- Ne pas utiliser docker compose down -v avant d'avoir vérifié la persistance.
- Ne pas confondre le port publié sur l'hôte avec le port interne du conteneur.
- Vérifier git status avant chaque commit.

## Itération 2 - OpenLDAP et LDAP Account Manager

- Déploiement d'OpenLDAP avec l'image `osixia/openldap:2.6.10-alpha`.
- Utilisation de la base DN `dc=embedded,dc=local`.
- Conservation des données avec les volumes `ldap_data`, `ldap_config` et
  `ldap_backups`.
- Déploiement de LDAP Account Manager sur le réseau Docker `openldap_default`.
- Vérification de l'interface LAM sur le port `8081`.
- Création et vérification de six groupes et six utilisateurs de laboratoire.
- Recherche LDAP terminée par `result: 0 Success`.

Les fichiers Compose sont maintenant conservés dans `openldap/` et
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]

## Itération 5 - Sauvegarde et restauration

### Mise en œuvre BorgBackup

- création du dépôt chiffré `/home/oliv/borg-infrastructure-backup` en mode
  `repokey` ;
- création du script `backup/backup.sh` pour exporter OpenLDAP et MariaDB,
  sauvegarder les volumes et archiver la documentation ;
- application de la rétention 7 quotidiennes, 4 hebdomadaires et 6 mensuelles ;
- création des archives du 5 août 2026, dont
  `embedded-infra-ubuntu-oliv-2026-08-05T12-55-10` ;
- contrôle d'intégrité Borg terminé avec le code retour `0`.

### Restaurations vérifiées

- restauration de `messaging-compose/docker-compose.yml` avec empreintes
  SHA-256 identiques et `cmp=0` ;
- restauration du document Samba `document-restauration.txt` avec empreintes
  identiques et `cmp=0` ;
- extraction des Maildir Dovecot ;
- extraction des données OpenLDAP dans un volume Docker isolé.

### Automatisation

- ajout de `run-backup-cron.sh`, d'un verrou `flock` et du fichier
  `last-run.status` ;
- ajout de `check-backup.sh` pour contrôler l'état, l'âge, le journal et la
  dernière archive ;
- installation d'une sauvegarde cron à 02 h 00 et d'un contrôle à 08 h 15 ;
- lancement manuel validé avec `SUCCESS`, code `0` et contrôle `CONFORME`.

Le 6 août, la machine a démarré à 08 h 48 et les tâches antérieures n'ont pas
été rejouées par cron. Une exécution planifiée sans intervention reste donc à
observer sur un hôte actif.

### Validation PCA/PRA

Le scénario de corruption LDAP estime la reprise à 1 h 20, sous les objectifs
de 2 heures du PRA et de 4 heures du PCA. La conformité reste partielle tant
que le démarrage complet d'un LDAP restauré, la copie hors hôte et la mesure du
délai réel ne sont pas réalisés.

### Points de vigilance

- corriger les avertissements de checksum OpenLDAP avant la production ;
- conserver la clé Borg séparément du dépôt et de la phrase secrète ;
- ne pas versionner `backup/.env` ni les dépôts Borg ;
- ne jamais restaurer directement par-dessus un volume de production sans
  validation isolée.

## Itération 7 - Supervision et diagnostic (optionnelle)

- analyse des journaux OpenLDAP, Samba, Postfix, Dovecot, Roundcube, MariaDB,
  BorgBackup, Docker et LAM ;
- prise en compte des futurs journaux step-ca de l'itération 6 ;
- définition des événements importants, des informations de diagnostic et des
  données sensibles à exclure ;
- proposition de seuils initiaux pour la disponibilité, les redémarrages,
  l'espace disque, les sauvegardes et les certificats ;
- conception d'une centralisation Filebeat, Elasticsearch et Kibana avec
  réseau dédié, volume persistant et conservation différenciée ;
- déploiement du projet `monitoring-compose` avec Elasticsearch et Kibana
  épinglés en version `9.3.1` ;
- limitation des ports à l'interface locale et ajout d'un test de santé
  Elasticsearch ;
- validation de l'API Elasticsearch et de l'interface Kibana ;
- validation de la persistance de l'index `validation-persistance` après
  suppression et recréation des conteneurs sans suppression du volume ;
- état `yellow` attendu après le test, car la réplique de l'index ne peut pas
  être placée sur le nœud unique du TP.
- ajout de Filebeat `9.3.1` à la pile de supervision ;
- collecte des fichiers JSON Docker et des journaux BorgBackup avec deux
  inputs `filestream` séparés ;
- enrichissement des événements avec le nom et l'image des conteneurs ;
- persistance du registre Filebeat dans `monitoring_filebeat_data`.
- création dans Kibana de la vue `logs-infrastructure*` ;
- vérification de la réception de Docker, Postfix, Dovecot, OpenLDAP, Samba et
  BorgBackup ;
- redirection des journaux Dovecot vers `stdout` et `stderr` pour leur collecte.
- création de cinq tableaux de bord Kibana pour la messagerie, LDAP,
  BorgBackup, les redémarrages et les certificats ;
- enregistrement d'une période de sept jours et vérification visuelle des
  événements réellement indexés ;
- export des objets Kibana dans `monitoring-compose/kibana/dashboards.ndjson` ;
- tableau certificats marqué comme préparation jusqu'au déploiement de
  `step-ca` ;
- redémarrages déduits des messages applicatifs, sans prétendre disposer d'un
  compteur Docker exact.
