#!/usr/bin/env bash
set -euo pipefail

# Auteur : Olivier
# Date : 2026-07-03
# Module : 05-services
# Objet : comparaison des services actifs avec la liste autorisee et fermeture des ecarts.
# Usage : lance par main.sh
# Dependances : systemctl, ss

run_module() {
  local module="05-services"
  local service base answer
  run_cmd "$module" "ss -tulnp > /tmp/alpesnet-ports-avant.txt"
  run_cmd "$module" "systemctl list-units --type=service --state=running --no-legend > /tmp/alpesnet-services-avant.txt"

  while read -r service _; do
    [ -z "${service:-}" ] && continue
    base="${service%.service}"
    case "$base" in
      dbus|systemd-*|user@*|getty@*|serial-getty@*)
        log_msg "$module" OK "service systeme protege : $base"
        continue
        ;;
    esac
    if contains_word "$base" "${SERVICES_AUTORISES[@]}" || contains_word "$base" "${SERVICES_SYSTEME_PROTEGES[@]}"; then
      log_msg "$module" OK "service conserve : $base"
      continue
    fi
    log_msg "$module" WARN "service non autorise detecte : $base"
    if [ "${MODE_INTERACTIF:-0}" -eq 1 ]; then
      read -r -p "Desactiver $base ? [oui/non] : " answer
      [ "$answer" = "oui" ] || continue
    fi
    run_cmd "$module" "systemctl disable --now '$base' || true"
  done < /tmp/alpesnet-services-avant.txt

  run_cmd "$module" "ss -tulnp > /tmp/alpesnet-ports-apres.txt"
  log_msg "$module" OK "ports avant/apres journalises dans /tmp/alpesnet-ports-*.txt"
}
