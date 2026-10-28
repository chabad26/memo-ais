# Mise en œuvre de la sauvegarde BorgBackup


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/backup-implementation.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Configuration retenue

| Élément | Configuration |
|---|---|
| Dépôt Borg | `/home/oliv/borg-infrastructure-backup` |
| Chiffrement | `repokey` |
| Compression | `lz4` |
| Rétention | 7 quotidiennes, 4 hebdomadaires, 6 mensuelles |
| Script | `backup/backup.sh` |
| VALEUR RETIRÉE | VALEUR RETIRÉE |
| Journaux | `backup/logs/`, exclus de Git |

## Données sauvegardées

Le script crée des exports LDIF pour OpenLDAP et un export cohérent de la base
MariaDB Roundcube. Il sauvegarde également les volumes LDAP, Samba, Dovecot,
Roundcube et WordPress, ainsi que les configurations et la documentation du
dépôt `~/on-premise`.

Pour Samba, les trois volumes sauvegardés sont `samba_config`, `samba_state`
et `samba_share`. Ils permettent de retrouver respectivement les fichiers de
configuration persistants, l'état interne du service et les documents
partagés.

OpenLDAP, Samba et Dovecot sont brièvement mis en pause pendant la copie de
leurs volumes. Un mécanisme de sortie garantit leur reprise si le script est
interrompu.

## Exclusions

- file Postfix ;
- images, conteneurs et réseaux Docker ;
- dépôt `.git` et démonstration `borg-demo` ;
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
- journaux locaux du script.

## Commandes

```bash
cd ~/on-premise/backup
cp .env.example .env
chmod 600 .env
nano .env
chmod 700 backup.sh
./backup.sh
```

Contrôles après exécution :

```bash
borg list /home/oliv/borg-infrastructure-backup
borg info /home/oliv/borg-infrastructure-backup
borg check /home/oliv/borg-infrastructure-backup
```

## État de validation

La première sauvegarde a été exécutée le 5 août 2026 :

| Élément | Résultat |
|---|---|
| Archive | `embedded-infra-ubuntu-oliv-2026-08-05T12-14-01` |
| Fichiers | 82 |
| Taille originale | 5,57 MB |
| Taille compressée | 3,06 MB |
| Taille dédupliquée | 3,06 MB |
| Chiffrement | `repokey` |
| Rétention | Archive conservée par la règle quotidienne n°1 |
| Contrôle Borg | Conforme, code retour `0` |
| Journal | `backup/logs/backup-2026-08-05T12-13-57.log` |

Le contenu de l'archive a été contrôlé. Les exports LDAP, l'export MariaDB
Roundcube, le volume Samba et le volume Dovecot sont présents. Le fichier
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
`.env.example` est conservé.

Les exports LDAP et MariaDB ainsi que la lecture du volume Samba ont été
testés. OpenLDAP signale actuellement des avertissements de checksum sur deux
fichiers `slapd.d`, conséquence de la réinitialisation hors ligne du mot de
passe administrateur. Les exports aboutissent, mais cette configuration devra
être régénérée proprement avant une mise en production.

## Protection de la clé

La clé Borg doit être exportée vers un emplacement sécurisé distinct du dépôt :

```bash
borg key export /home/oliv/borg-infrastructure-backup \
  /chemin/securise/borg-infrastructure-key
```

La clé exportée et la phrase secrète sont toutes les deux nécessaires à la
reprise et ne doivent pas être ajoutées à Git.
