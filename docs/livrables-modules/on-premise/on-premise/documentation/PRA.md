# Plan de Reprise d'Activité - état du projet


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/PRA.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Priorité de reprise

1. Docker et stockage des volumes ;
2. OpenLDAP ;
3. Samba et espaces de partage ;
4. Dovecot, Postfix, Roundcube et MariaDB ;
5. certificats de service et volumes TLS nécessaires aux échanges chiffrés ;
6. WordPress et MariaDB ;
7. LDAP Account Manager ;
8. Elasticsearch, Kibana et Filebeat ;
9. vérification des utilisateurs, groupes, services et tableaux de bord.

## Reprise OpenLDAP

1. Restaurer `openldap/compose.yaml` et les paramètres protégés du fichier `.env`.
2. Vérifier les volumes `ldap_data`, `ldap_config` et `ldap_backups`.
3. Démarrer le service avec `docker compose up -d`.
4. Vérifier `docker compose ps` et les journaux.
5. Tester `ldapwhoami` avec `cn=admin,dc=embedded,dc=local`.
6. Exécuter une recherche LDAP sur `dc=embedded,dc=local`.
7. Vérifier la présence des unités, des six groupes et des six utilisateurs.
8. Si TLS est requis, restaurer ou régénérer le certificat OpenLDAP, préparer
   le volume `openldap_tls`, puis valider LDAPS sur `ldap.embedded.local:636`.

Le stack `infrastructure-compose/` peut être utilisé à la place des deux
Compose unitaires pour reprendre OpenLDAP et LAM ensemble. Dans ce cas,
restaurer son `.env` local et exécuter `docker compose up -d` depuis ce dossier.

## Reprise WordPress et MariaDB

1. Restaurer `wordpress-compose/compose.yaml` et le fichier `.env` protégé.
2. Vérifier le volume `wordpress-compose_db_data`.
3. Démarrer avec `docker compose up -d`.
4. Vérifier l'accès Web sur le port défini par `WORDPRESS_PORT`.
5. Contrôler les journaux de `db` et `wordpress`.
6. Vérifier que la configuration et les contenus WordPress sont présents.

## Reprise LAM

1. Vérifier qu'OpenLDAP est opérationnel.
2. Vérifier que le réseau Docker `openldap_default` existe.
3. Restaurer `ldap-account-manager/compose.yaml` et les paramètres protégés.
4. Démarrer LAM et vérifier l'accès sur `http://localhost:8081`.
5. Tester la connexion à `ldap://openldap:3890`.
6. Si LAM est indisponible, utiliser `ldapsearch` et `ldapmodify`.

## Données et limites

Les Compose et les `.env.example` permettent de reconstruire les services,
mais ne remplacent pas les sauvegardes des volumes. Les volumes MariaDB et
LDAP ainsi que les fichiers `.env` protégés doivent être disponibles pour une
reprise complète. L'extraction dans des volumes isolés a été réalisée ; le
démarrage d'un service restauré reste à effectuer dans un exercice dédié.

## Reprise Samba

1. Restaurer `samba-ad/compose.yaml`, `samba-ad/config/smb.conf` et les
   paramètres protégés de `samba-ad/.env`.
2. Vérifier que le réseau `openldap_default` et OpenLDAP sont opérationnels.
3. Restaurer les volumes `samba_config`, `samba_share` et, si nécessaire,
   `samba_state`.
4. Démarrer Samba avec `docker compose up -d --build`.
5. Vérifier `docker compose ps`, `testparm -s` et les journaux.
6. Tester l'authentification et chaque partage avec `validation.md`.

Un fichier du volume Samba a été restauré avec des empreintes identiques et
`cmp=0`. La reprise complète du service et le test de refus d'accès doivent
encore être réalisés dans un exercice dédié.

## Reprise de la messagerie

[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
2. Restaurer `dovecot_mail`, la base Roundcube et sa configuration.
3. Restaurer ou régénérer les certificats Postfix, Dovecot et Roundcube.
4. Recréer les volumes TLS avec `messaging-compose/prepare-tls-volumes.sh`.
5. Reconstruire Postfix et Dovecot à partir des configurations versionnées.
6. Démarrer les services avec `docker compose up -d`.
7. Vérifier l'authentification LDAP, IMAPS, SMTP STARTTLS et l'accès HTTPS
   Roundcube.
8. Envoyer puis recevoir un message de test avec une pièce jointe.

La file Postfix n'est pas restaurée par défaut afin d'éviter la remise en
circulation de messages déjà délivrés. Toute exception doit être analysée et
documentée.

## Reprise des certificats TLS

1. Restaurer `pki/certs/Campus-CA-root.crt` depuis Git.
2. Vérifier l'empreinte publique documentée dans `pki/README.md`.
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
   clés privées réellement nécessaires, ou réémettre des certificats propres.
4. Mettre à jour `documentation/certificate-register.md` avec les nouvelles
   dates, SAN et numéros de série.
5. Préparer les volumes TLS OpenLDAP et messagerie.
6. Valider la chaîne depuis `client-validation/` avec
   `docker compose run --rm tls-client`.

Les certificats de laboratoire délivrés le 7 août 2026 avaient une durée
courte. Lors d'un exercice exécuté après leur expiration, la réémission est une
étape normale du PRA, pas une anomalie.

## Reprise de la supervision

1. Restaurer `monitoring-compose/compose.yaml`, `filebeat.yml`, `.env` protégé
   et le volume `monitoring_elasticsearch_data` si les index doivent être
   conservés.
2. Démarrer Elasticsearch, Kibana et Filebeat depuis `monitoring-compose/`.
3. Vérifier `_cluster/health`, l'accès Kibana et l'index
   `logs-infrastructure*`.
4. Réimporter les tableaux de bord depuis
   `monitoring-compose/kibana/dashboards.ndjson` si nécessaire.
5. Vérifier les cinq tableaux de bord : messagerie, LDAP, BorgBackup,
   redémarrages et certificats.

La supervision aide à diagnostiquer la reprise, mais ne doit pas bloquer le
retour des services métier prioritaires.

## Référence de sauvegarde

Les données, fréquences et rétentions sont définies dans
`backup-strategy.md`. Le test PRA doit mesurer le temps réel de restauration
et mettre à jour ce document si les objectifs ne sont pas atteints.

L'analyse `backup-strategy-validation.md` estime la reprise d'OpenLDAP à
1 h 20. Cette estimation respecte l'objectif de 2 heures, mais la conformité
définitive nécessite le démarrage et le chronométrage d'un service restauré.
