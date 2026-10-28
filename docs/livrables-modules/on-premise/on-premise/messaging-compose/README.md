# Préparation de l'infrastructure de messagerie


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/messaging-compose/README.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


Le rôle détaillé du Compose, de `postfix-init.sh` et des fichiers Dovecot est
décrit dans
[`../documentation/technical-files-guide.md`](../documentation/technical-files-guide.md).

Ce dossier contient les fichiers de configuration et le déploiement de
laboratoire de l'infrastructure de messagerie.

## Arborescence

```text
messaging-compose/
├── docker-compose.yml
├── .env
├── .env.example
├── .gitignore
├── README.md
├── postfix/
├── postfix-init.sh
├── dovecot/
└── roundcube/
```

## Préparer les paramètres

```bash
cd ~/on-premise/messaging-compose
cp .env.example .env
```

[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
avant tout déploiement.

## Contrôles autorisés pendant cette activité

La configuration peut être inspectée sans démarrer de conteneur :

```bash
docker compose --env-file .env.example config
docker compose --env-file .env.example config --quiet
```

Ne pas exécuter `docker compose up` pendant cette activité.

## Volumes prévus

- `postfix_spool` : files et état Postfix ;
- `dovecot_mail` : boîtes et index Dovecot ;
- `roundcube_db` : base de données Roundcube ;
- `roundcube_config` : configuration Roundcube.

Les volumes devront être sauvegardés avant toute opération destructive.

La configuration Postfix est générée par l'image à partir des variables
d'environnement. Le répertoire `postfix/` est conservé pour les adaptations
documentées ; les fichiers générés par le conteneur ne doivent pas être
versionnés.

`postfix-init.sh` génère au démarrage la table LDAP des destinataires. Le
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
jamais être ajoutés à Git.

`dovecot/dovecot.conf` envoie les journaux vers `/dev/stdout` et `/dev/stderr`
pour qu'ils soient capturés par le pilote Docker puis par Filebeat. Le détail
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
