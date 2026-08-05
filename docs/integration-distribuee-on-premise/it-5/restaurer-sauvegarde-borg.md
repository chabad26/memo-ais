# Restaurer une sauvegarde BorgBackup

## Objectif

Restaurer un fichier, un document partagé, une boîte aux lettres ou un volume
Docker à partir des archives Borg, puis vérifier les données restaurées.

## 1. Sélectionner l'archive

```bash
cd ~/on-premise/backup
set -a
source .env
set +a

borg check "$BORG_REPO"
borg list "$BORG_REPO"
```

Archive disponible pour l'exercice :

```text
embedded-infra-ubuntu-oliv-2026-08-05T12-14-01
```

```bash
ARCHIVE_NAME=embedded-infra-ubuntu-oliv-2026-08-05T12-14-01
borg list "$BORG_REPO::$ARCHIVE_NAME"
```

## 2. Restaurer un fichier de configuration

Toujours restaurer dans un répertoire temporaire pour ne pas écraser la
production :

```bash
RESTORE_DIR=$(mktemp -d /tmp/borg-restore-config.XXXXXX)
cd "$RESTORE_DIR"

borg extract "$BORG_REPO::$ARCHIVE_NAME" \
  home/oliv/on-premise/messaging-compose/docker-compose.yml
```

Comparer le fichier restauré avec l'original :

```bash
sha256sum \
  /home/oliv/on-premise/messaging-compose/docker-compose.yml \
  "$RESTORE_DIR/home/oliv/on-premise/messaging-compose/docker-compose.yml"

cmp \
  /home/oliv/on-premise/messaging-compose/docker-compose.yml \
  "$RESTORE_DIR/home/oliv/on-premise/messaging-compose/docker-compose.yml"
echo "Code retour cmp : $?"
```

Résultat obtenu le 5 août 2026 : les empreintes SHA-256 sont identiques et
`cmp` retourne `0`. Le fichier restauré est conforme.

## 3. Restaurer un document Samba

```bash
SHARE_TAR_PATH=$(borg list --format '{path}{NL}' \
  "$BORG_REPO::$ARCHIVE_NAME" |
  grep 'samba-ad_samba_share.tar.gz$' |
  head -n 1)

RESTORE_DIR=$(mktemp -d /tmp/borg-restore-samba.XXXXXX)
cd "$RESTORE_DIR"
borg extract "$BORG_REPO::$ARCHIVE_NAME" "$SHARE_TAR_PATH"

mkdir restored-share
tar -xzf "$RESTORE_DIR/$SHARE_TAR_PATH" -C restored-share
find restored-share -type f -ls
```

Comparer le fichier demandé avec `sha256sum` et `cmp`, puis vérifier ses droits
avec `stat`.

## 4. Restaurer une boîte Dovecot

```bash
MAIL_TAR_PATH=$(borg list --format '{path}{NL}' \
  "$BORG_REPO::$ARCHIVE_NAME" |
  grep 'messaging-compose_dovecot_mail.tar.gz$' |
  head -n 1)

RESTORE_DIR=$(mktemp -d /tmp/borg-restore-mail.XXXXXX)
cd "$RESTORE_DIR"
borg extract "$BORG_REPO::$ARCHIVE_NAME" "$MAIL_TAR_PATH"

mkdir restored-mail
tar -xzf "$RESTORE_DIR/$MAIL_TAR_PATH" -C restored-mail
find restored-mail -type f -ls
```

Après une restauration réelle, vérifier les propriétaires, exécuter
`doveadm force-resync` et tester la boîte par IMAP.

## 5. Restaurer un volume Docker de test

```bash
VOLUME_TAR_PATH=$(borg list --format '{path}{NL}' \
  "$BORG_REPO::$ARCHIVE_NAME" |
  grep 'openldap_ldap_data.tar.gz$' |
  head -n 1)

RESTORE_DIR=$(mktemp -d /tmp/borg-restore-volume.XXXXXX)
cd "$RESTORE_DIR"
borg extract "$BORG_REPO::$ARCHIVE_NAME" "$VOLUME_TAR_PATH"

docker volume create restore-openldap-test
docker run --rm \
  --volume restore-openldap-test:/restore \
  --volume "$RESTORE_DIR:/backup:ro" \
  alpine:3.20 \
  tar -xzf "/backup/$VOLUME_TAR_PATH" -C /restore
```

Le volume de test est isolé. Ne jamais extraire directement dans un volume de
production avant validation.

## 6. Résultats

| Élément restauré | Archive utilisée | Résultat |
|---|---|---|
| `messaging-compose/docker-compose.yml` | `embedded-infra-ubuntu-oliv-2026-08-05T12-14-01` | Conforme, SHA-256 identiques et `cmp=0` |
| Document partagé | À définir par le formateur | À tester |
| Boîte aux lettres | À définir par le formateur | À tester |
| Volume Docker | À définir par le formateur | À tester |

## Recommandations

- sélectionner une archive antérieure à la perte ;
- vérifier le dépôt avant extraction ;
- restaurer dans un emplacement isolé ;
- contrôler empreintes, propriétaires et permissions ;
- réaliser un test fonctionnel du service ;
- conserver les commandes et résultats dans le journal technique ;
- effectuer une nouvelle sauvegarde avant tout remplacement en production.

