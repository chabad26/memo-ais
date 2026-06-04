#!/usr/bin/env bash
# ============================================================
# Auteur     : Olivier
# Date       : 2026-06-04
# Version    : 1.0
# Objet      : Sauvegarde SSH des configurations AlpesNet
# Usage      : ./backup_configs.sh [equipements.txt]
# Dependances: ssh, date, mkdir
# ============================================================

set -uo pipefail
shopt -s extglob

EQUIPMENT_FILE="${1:-equipements.txt}"
BACKUP_DIR="backups"
SSH_USER="${SSH_USER:-admin}"
SSH_TIMEOUT=8
OK_COUNT=0
ERROR_COUNT=0

usage() {
    printf 'Usage: SSH_USER=admin %s [equipements.txt]\n' "$0" >&2
}

clean_line() {
    local line="$1"

    line="${line%%#*}"
    line="${line##+([[:space:]])}"
    line="${line%%+([[:space:]])}"

    printf '%s\n' "$line"
}

write_header() {
    local equipment_name="$1"
    local equipment_ip="$2"

    cat <<EOF
! ============================================================
! ALPESNET - SAUVEGARDE CONFIGURATION EQUIPEMENT
! Equipement : ${equipment_name}
! Adresse IP : ${equipment_ip}
! Date       : $(date '+%Y-%m-%d %H:%M:%S')
! Auteur     : Olivier
! Commande   : show running-config
! ============================================================

EOF
}

backup_equipment() {
    local equipment_ip="$1"
    local equipment_name="$2"
    local backup_date
    local backup_file
    local temp_file

    backup_date="$(date +%Y%m%d)"
    backup_file="${BACKUP_DIR}/backup_${equipment_name}_${backup_date}.cfg"
    temp_file="${backup_file}.tmp"

    write_header "$equipment_name" "$equipment_ip" > "$temp_file"

    if ssh \
        -o BatchMode=yes \
        -o ConnectTimeout="$SSH_TIMEOUT" \
        -o StrictHostKeyChecking=accept-new \
        "${SSH_USER}@${equipment_ip}" \
        "terminal length 0; show running-config" >> "$temp_file"; then
        mv "$temp_file" "$backup_file"
        printf '[OK]   %s (%s) -> %s\n' "$equipment_name" "$equipment_ip" "$backup_file"
        return 0
    fi

    rm -f "$temp_file"
    printf '[ERROR] %s (%s)\n' "$equipment_name" "$equipment_ip" >&2
    return 1
}

if [[ ! -f "$EQUIPMENT_FILE" ]]; then
    printf 'ERREUR: fichier introuvable: %s\n' "$EQUIPMENT_FILE" >&2
    usage
    exit 1
fi

mkdir -p "$BACKUP_DIR"

while IFS= read -r raw_line || [[ -n "$raw_line" ]]; do
    line="$(clean_line "$raw_line")"

    [[ -z "$line" ]] && continue

    read -r equipment_ip equipment_name extra <<< "$line"

    if [[ -z "${equipment_ip:-}" || -z "${equipment_name:-}" || -n "${extra:-}" ]]; then
        printf '[ERROR] ligne invalide: %s\n' "$raw_line" >&2
        ERROR_COUNT=$((ERROR_COUNT + 1))
        continue
    fi

    if backup_equipment "$equipment_ip" "$equipment_name"; then
        OK_COUNT=$((OK_COUNT + 1))
    else
        ERROR_COUNT=$((ERROR_COUNT + 1))
    fi
done < "$EQUIPMENT_FILE"

printf 'Resume: %d sauvegardes OK / %d erreurs\n' "$OK_COUNT" "$ERROR_COUNT"
