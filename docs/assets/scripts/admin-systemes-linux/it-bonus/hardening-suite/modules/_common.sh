#!/usr/bin/env bash
set -euo pipefail

# Auteur : Olivier
# Date : 2026-07-03
# Module : commun
# Objet : fonctions partagees de la suite de hardening AlpesNet.
# Usage : source modules/_common.sh
# Dependances : Bash, coreutils, systemd

log_msg() {
  local module="$1"
  local level="$2"
  local message="$3"
  printf '[%s] [%s] [%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$module" "$level" "$message" | tee -a "$LOGFILE"
}

run_cmd() {
  local module="$1"
  local command="$2"
  log_msg "$module" INFO "$command"
  if [ "${DRY_RUN:-0}" -eq 1 ]; then
    log_msg "$module" OK "dry-run : commande simulee"
    return 0
  fi
  bash -o pipefail -c "$command" >> "$LOGFILE" 2>&1
}

backup_file() {
  local module="$1"
  local file="$2"
  if [ -f "$file" ]; then
    local backup="${file}.bak.$(date +%Y%m%d%H%M%S)"
    run_cmd "$module" "cp '$file' '$backup'"
    log_msg "$module" OK "sauvegarde creee : $backup"
  fi
}

write_file() {
  local module="$1"
  local target="$2"
  local content="$3"
  backup_file "$module" "$target"
  if [ "${DRY_RUN:-0}" -eq 1 ]; then
    log_msg "$module" INFO "dry-run : ecriture simulee de $target"
    return 0
  fi
  printf '%s\n' "$content" > "$target"
}

contains_word() {
  local wanted="$1"
  shift
  local item
  for item in "$@"; do
    [ "$item" = "$wanted" ] && return 0
  done
  return 1
}

service_exists() {
  systemctl list-unit-files "$1.service" >/dev/null 2>&1
}

append_check() {
  local status="$1"
  local section="$2"
  local detail="$3"
  printf '%s\t%s\t%s\n' "$status" "$section" "$detail" >> "$AUDIT_CHECKS_FILE"
}
