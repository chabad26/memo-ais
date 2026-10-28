# Procédure de restauration BorgBackup


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/restore-procedure.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.


## Principe de sécurité

Une restauration est d'abord réalisée dans un répertoire ou un volume de test.
La production n'est remplacée qu'après contrôle de l'intégrité, des droits et
du fonctionnement du service.

## Préparation

```bash
cd ~/on-premise/backup
set -euo pipefail
set -a
source .env
set +a

borg check "$BORG_REPO"
borg list "$BORG_REPO"

ARCHIVE_NAME=$(borg list --format '{archive}{NL}' "$BORG_REPO" | tail -n 1)
test -n "$ARCHIVE_NAME" || {
  echo "Aucune archive Borg disponible"
  exit 1
}
echo "Archive utilisée : $ARCHIVE_NAME"
```

## Restaurer un fichier de configuration

```bash
RESTORE_DIR=$(mktemp -d /tmp/borg-restore-config.XXXXXX)
cd "$RESTORE_DIR"

borg extract "$BORG_REPO::$ARCHIVE_NAME" \
  home/oliv/on-premise/messaging-compose/docker-compose.yml

sha256sum \
  /home/oliv/on-premise/messaging-compose/docker-compose.yml \
  "$RESTORE_DIR/home/oliv/on-premise/messaging-compose/docker-compose.yml"

cmp \
  /home/oliv/on-premise/messaging-compose/docker-compose.yml \
  "$RESTORE_DIR/home/oliv/on-premise/messaging-compose/docker-compose.yml"
echo "Code retour cmp : $?"
```

Résultat du 5 août 2026 : empreintes identiques et code retour `cmp` égal à
`0`. Le fichier restauré est conforme à l'original.

Revalidation du 6 août 2026 depuis l'archive encore présente
`embedded-infra-ubuntu-oliv-2026-08-05T12-55-10` : empreinte
`8c8f7879ab221181e2857c1f8a28db966c1398f278cf620534fa7a0a1a521c70`
identique pour les deux fichiers et `cmp=0`.

## Restaurer un document partagé Samba

Identifier puis extraire l'archive du volume :

```bash
SHARE_TAR_PATH=$(borg list --format '{path}{NL}' \
  "$BORG_REPO::$ARCHIVE_NAME" |
  grep 'samba-ad_samba_share.tar.gz$' |
  head -n 1 || true)

test -n "$SHARE_TAR_PATH" || {
  echo "Archive du volume Samba introuvable"
  exit 1
}

RESTORE_DIR=$(mktemp -d /tmp/borg-restore-samba.XXXXXX)
cd "$RESTORE_DIR"
borg extract "$BORG_REPO::$ARCHIVE_NAME" "$SHARE_TAR_PATH"

mkdir restored-share
tar -xzf "$RESTORE_DIR/$SHARE_TAR_PATH" -C restored-share
find restored-share -type f -ls
```

Comparer le document du volume actif avec celui qui vient d'être restauré :

```bash
ORIGINAL_FILE=$(mktemp)
docker run --rm \
  --volume samba-ad_samba_share:/share:ro \
  alpine:3.20 \
  cat /share/preuve-ldap/document-restauration.txt \
  > "$ORIGINAL_FILE"

RESTORED_FILE="$RESTORE_DIR/restored-share/preuve-ldap/document-restauration.txt"
sha256sum "$ORIGINAL_FILE" "$RESTORED_FILE"
cmp "$ORIGINAL_FILE" "$RESTORED_FILE"
echo "Code retour cmp : $?"
```

Résultat : empreintes identiques et code retour `cmp` égal à `0`.

Revalidation du 6 août 2026 depuis l'archive
`embedded-infra-ubuntu-oliv-2026-08-05T12-55-10` : empreinte
`cc177c42e595cb4fffe879fbc133d6e952d15fc56528af6c6c072dbec362b68f`
identique pour le document actif et restauré, avec `cmp=0`.

## Restaurer une boîte Dovecot

```bash
MAIL_TAR_PATH=$(borg list --format '{path}{NL}' \
  "$BORG_REPO::$ARCHIVE_NAME" |
  grep 'messaging-compose_dovecot_mail.tar.gz$' |
  head -n 1 || true)

test -n "$MAIL_TAR_PATH" || {
  echo "Archive du volume Dovecot introuvable"
  exit 1
}

RESTORE_DIR=$(mktemp -d /tmp/borg-restore-mail.XXXXXX)
cd "$RESTORE_DIR"
borg extract "$BORG_REPO::$ARCHIVE_NAME" "$MAIL_TAR_PATH"

mkdir restored-mail
tar -xzf "$RESTORE_DIR/$MAIL_TAR_PATH" -C restored-mail
find restored-mail -type f -ls
```

Avant toute réinjection, contrôler les messages, les propriétaires et le compte
concerné. Après restauration dans Dovecot, reconstruire les index avec
`doveadm force-resync` et valider la lecture en IMAP.

## Restaurer un volume Docker isolé

Exemple avec la sauvegarde du volume LDAP :

```bash
VOLUME_TAR_PATH=$(borg list --format '{path}{NL}' \
  "$BORG_REPO::$ARCHIVE_NAME" |
  grep 'openldap_ldap_data.tar.gz$' |
  head -n 1 || true)

test -n "$VOLUME_TAR_PATH" || {
  echo "Archive du volume OpenLDAP introuvable"
  exit 1
}

RESTORE_DIR=$(mktemp -d /tmp/borg-restore-volume.XXXXXX)
cd "$RESTORE_DIR"
borg extract "$BORG_REPO::$ARCHIVE_NAME" "$VOLUME_TAR_PATH"

docker volume create restore-openldap-test
docker run --rm \
  --volume restore-openldap-test:/restore \
  --volume "$RESTORE_DIR:/backup:ro" \
  alpine:3.20 \
  tar -xzf "/backup/$VOLUME_TAR_PATH" -C /restore

docker run --rm \
  --volume restore-openldap-test:/restore:ro \
  alpine:3.20 \
  find /restore -maxdepth 2 -type f -ls
```

Le volume `restore-openldap-test` est distinct du volume de production. Il ne
doit remplacer celui-ci qu'après validation dans un conteneur isolé.

## Incidents rencontrés

| Symptôme | Cause | Correction |
|---|---|---|
| Emplacement Borg terminé par `::` | Variable d'archive vide ou `.env` non chargé | Charger `.env`, sélectionner une archive existante et afficher son nom. |
| Archive `12-42-02` absente | Archive supprimée par la rétention après une nouvelle sauvegarde | Utiliser `borg list` puis sélectionner la dernière archive disponible. |
| Chemin d'extraction vide | Le filtre `grep` n'avait trouvé aucun fichier | Contrôler chaque variable avec `test -n` et arrêter le script en cas d'échec. |
| Sauvegarde Samba sans fichier | Le volume ne contenait qu'un répertoire vide | Ajouter un document témoin, refaire la sauvegarde et comparer les deux fichiers. |

## Résultats

| Élément restauré | Archive utilisée | Résultat |
|---|---|---|
| `messaging-compose/docker-compose.yml` | `embedded-infra-ubuntu-oliv-2026-08-05T12-55-10` | Revalidé le 6 août, SHA-256 identiques et `cmp=0` |
| `preuve-ldap/document-restauration.txt` | `embedded-infra-ubuntu-oliv-2026-08-05T12-55-10` | Revalidé le 6 août, SHA-256 identiques et `cmp=0` |
| Volume Dovecot | `embedded-infra-ubuntu-oliv-2026-08-05T12-44-31` | Extraction Maildir réussie ; test IMAP restant avant réinjection |
| Volume OpenLDAP | `embedded-infra-ubuntu-oliv-2026-08-05T12-44-31` | Extraction réussie dans un volume isolé ; démarrage LDAP restant à valider |

## Traçabilité

Pour chaque opération, conserver l'archive choisie, le chemin restauré, les
commandes, les empreintes, les permissions, le résultat fonctionnel et le nom
de l'administrateur. Ne jamais extraire directement par-dessus les données de
production sans copie de sécurité et validation préalable.
