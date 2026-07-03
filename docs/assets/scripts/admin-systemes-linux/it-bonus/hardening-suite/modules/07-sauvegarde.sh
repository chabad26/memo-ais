#!/usr/bin/env bash
set -euo pipefail

# Auteur : Olivier
# Date : 2026-07-03
# Module : 07-sauvegarde
# Objet : sauvegarde rsync de /etc et des repertoires configures, cron et checksum.
# Usage : lance par main.sh
# Dependances : rsync, sha256sum, cron

run_module() {
  local module="07-sauvegarde"
  local date_tag dest backup_script cron_file dir checksum_file
  date_tag="$(date +%Y%m%d_%H%M%S)"
  dest="${BACKUP_DEST}-${date_tag}"
  checksum_file="${dest}/checksums.sha256"
  backup_script="/usr/local/sbin/alpesnet-backup.sh"
  cron_file="/etc/cron.d/alpesnet-backup"

  run_cmd "$module" "mkdir -p '$dest'"
  for dir in "${BACKUP_DIRS[@]}"; do
    if [ -e "$dir" ]; then
      run_cmd "$module" "mkdir -p '$dest$dir'"
      run_cmd "$module" "rsync -a --delete '$dir/' '$dest$dir/'"
    else
      log_msg "$module" WARN "source absente : $dir"
    fi
  done
  run_cmd "$module" "find '$dest' -type f ! -name 'checksums.sha256' -print0 | sort -z | xargs -0 sha256sum > '$checksum_file'"
  run_cmd "$module" "cd / && sha256sum -c '$checksum_file'"

  write_file "$module" "$backup_script" "#!/usr/bin/env bash
set -euo pipefail
DEST=\"${BACKUP_DEST}-\$(date +%Y%m%d_%H%M%S)\"
mkdir -p \"\$DEST\"
for DIR in ${BACKUP_DIRS[*]}; do
  [ -e \"\$DIR\" ] || continue
  mkdir -p \"\$DEST\$DIR\"
  rsync -a --delete \"\$DIR/\" \"\$DEST\$DIR/\"
done
find \"\$DEST\" -type f ! -name 'checksums.sha256' -print0 | sort -z | xargs -0 sha256sum > \"\$DEST/checksums.sha256\"
find \"$(dirname "$BACKUP_DEST")\" -maxdepth 1 -type d -name '$(basename "$BACKUP_DEST")-*' -mtime +${BACKUP_RETENTION_DAYS} -exec rm -rf {} +"
  run_cmd "$module" "chmod 0750 '$backup_script'"
  write_file "$module" "$cron_file" "SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
${BACKUP_CRON} root ${backup_script} >> /var/log/alpesnet/backup.log 2>&1"
  run_cmd "$module" "chmod 0644 '$cron_file'"
  run_cmd "$module" "systemctl reload cron || systemctl reload crond || true"
}
