# Sauvegarde BorgBackup


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/backup/README.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


La chaîne entre cron, les trois scripts et Borg est détaillée dans
[`../documentation/technical-files-guide.md`](../documentation/technical-files-guide.md).

## Préparation

```bash
cd ~/on-premise/backup
cp .env.example .env
chmod 600 .env
nano .env
chmod 700 backup.sh
```

La phrase secrète protège la clé `repokey`. Elle doit être conservée hors de
Git et séparément du dépôt Borg.

## Première sauvegarde

```bash
./backup.sh
```

Sans fichier `.env`, le script demande la phrase secrète de manière
interactive. Le dépôt par défaut est :

```text
/home/oliv/borg-infrastructure-backup
```

## Contenu sauvegardé

- exports LDIF OpenLDAP ;
- volumes OpenLDAP ;
- volumes Samba de la configuration, des partages et de l'état ;
- boîtes Dovecot ;
- export MariaDB Roundcube ;
- configuration Roundcube ;
- volume MariaDB WordPress s'il existe ;
- configurations, scripts et documentation de `~/on-premise`.

La file Postfix, les images, les conteneurs, les réseaux, `.git`, `borg-demo`,
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]

## Rétention et vérification

Le script conserve 7 archives quotidiennes, 4 hebdomadaires et 6 mensuelles.
Il exécute ensuite `borg compact`, `borg check`, `borg list` et `borg info`.

Les journaux locaux sont créés dans `backup/logs/` et ne sont pas versionnés.

## Automatisation

Les fichiers suivants préparent une exécution quotidienne :

- `run-backup-cron.sh` lance la sauvegarde avec un verrou anti-chevauchement ;
- `check-backup.sh` contrôle l'état, l'âge, le journal et la dernière archive ;
- `crontab.example` contient les tâches de 02 h 00 et de 08 h 15.

Avant d'installer la crontab, tester manuellement :

```bash
./run-backup-cron.sh
./check-backup.sh
```

La procédure complète se trouve dans `documentation/backup-automation.md`.

## Exporter la clé

Après l'initialisation, exporter la clé vers un emplacement sécurisé distinct
du dépôt :

```bash
borg key export /home/oliv/borg-infrastructure-backup \
  /chemin/securise/borg-infrastructure-key
```

Ne pas stocker la clé exportée ni la phrase secrète dans Git.
