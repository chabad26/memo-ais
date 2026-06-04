#!/usr/bin/env bash
# ============================================================
# Auteur     : Olivier
# Date       : 2026-06-04
# Version    : 1.0
# Objet      : Verification de connectivite des hotes AlpesNet
# Usage      : ./check_connectivity.sh [hosts.txt]
# Dependances: ping, date, mkdir
# ============================================================

set -uo pipefail
shopt -s extglob

HOSTS_FILE="${1:-hosts.txt}"
REPORT_DIR="reports"
REPORT_FILE="${REPORT_DIR}/connectivity_$(date +%Y%m%d_%H%M%S).log"
TIMEOUT=2
UP_COUNT=0
DOWN_COUNT=0
TOTAL_COUNT=0

usage() {
    printf 'Usage: %s [hosts.txt]\n' "$0" >&2
}

clean_line() {
    local line="$1"

    line="${line%%#*}"
    line="${line##+([[:space:]])}"
    line="${line%%+([[:space:]])}"

    printf '%s\n' "$line"
}

check_host() {
    local ip="$1"
    local timestamp

    timestamp="$(date '+%Y-%m-%d %H:%M:%S')"

    if ping -c 1 -W "$TIMEOUT" "$ip" >/dev/null 2>&1; then
        printf '%s [OK]   %s\n' "$timestamp" "$ip"
        return 0
    fi

    printf '%s [DOWN] %s\n' "$timestamp" "$ip"
    return 1
}

if [[ ! -f "$HOSTS_FILE" ]]; then
    printf 'ERREUR: fichier introuvable: %s\n' "$HOSTS_FILE" >&2
    usage
    exit 1
fi

mkdir -p "$REPORT_DIR"

{
    printf '=== Rapport de connectivite AlpesNet ===\n'
    printf 'Date: %s\n' "$(date '+%Y-%m-%d %H:%M:%S')"
    printf 'Source: %s\n' "$HOSTS_FILE"
    printf '\n'
} | tee "$REPORT_FILE"

while IFS= read -r raw_line || [[ -n "$raw_line" ]]; do
    ip="$(clean_line "$raw_line")"

    [[ -z "$ip" ]] && continue

    TOTAL_COUNT=$((TOTAL_COUNT + 1))

    if result="$(check_host "$ip")"; then
        UP_COUNT=$((UP_COUNT + 1))
    else
        DOWN_COUNT=$((DOWN_COUNT + 1))
    fi

    printf '%s\n' "$result" | tee -a "$REPORT_FILE"
done < "$HOSTS_FILE"

{
    printf '\n'
    printf '=== Resume ===\n'
    printf '%d UP / %d DOWN sur %d total\n' "$UP_COUNT" "$DOWN_COUNT" "$TOTAL_COUNT"
    printf 'Rapport: %s\n' "$REPORT_FILE"
} | tee -a "$REPORT_FILE"
