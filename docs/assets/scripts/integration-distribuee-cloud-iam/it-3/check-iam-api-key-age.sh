#!/usr/bin/env bash
set -euo pipefail

max_age_days="${MAX_AGE_DAYS:-90}"
input_file="${1:-iam-credentials-metadata.json}"
now="$(date +%s)"
status=0

if ! command -v jq >/dev/null 2>&1; then
  printf 'Erreur : jq est requis.\n' >&2
  exit 2
fi

if [[ ! -f "$input_file" ]]; then
  printf 'Erreur : fichier absent : %s\n' "$input_file" >&2
  exit 2
fi

printf 'Contrôle des clés API âgées de plus de %s jours\n' "$max_age_days"

while IFS=$'\t' read -r identity key_id created_at; do
  created_epoch="$(date -d "$created_at" +%s 2>/dev/null || true)"
  if [[ -z "$created_epoch" ]]; then
    printf 'Date invalide pour %s (%s)\n' "$identity" "$created_at" >&2
    status=2
    continue
  fi

  age_days="$(( (now - created_epoch) / 86400 ))"
  if (( age_days > max_age_days )); then
    printf 'ALERTE identity=%s key=%s age_days=%s created_at=%s\n' \
      "$identity" "$key_id" "$age_days" "$created_at"
    status=1
  else
    printf 'OK    identity=%s key=%s age_days=%s\n' \
      "$identity" "$key_id" "$age_days"
  fi
done < <(jq -r '.[] | [.identity, .key_id, .created_at] | @tsv' "$input_file")

exit "$status"
