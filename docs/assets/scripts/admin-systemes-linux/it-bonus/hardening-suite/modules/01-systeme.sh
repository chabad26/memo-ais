#!/usr/bin/env bash
set -euo pipefail

# Auteur : Olivier
# Date : 2026-07-03
# Module : 01-systeme
# Objet : mise a jour du systeme et installation des outils de base.
# Usage : lance par main.sh
# Dependances : apt, dpkg

run_module() {
  local module="01-systeme"
  local before_count="0"
  before_count="$(apt list --upgradable 2>/dev/null | sed '1d' | wc -l || true)"
  run_cmd "$module" "apt-get update"
  run_cmd "$module" "DEBIAN_FRONTEND=noninteractive apt-get upgrade -y"
  if [ "${#OUTILS_BASE[@]}" -gt 0 ]; then
    run_cmd "$module" "DEBIAN_FRONTEND=noninteractive apt-get install -y ${OUTILS_BASE[*]}"
  fi
  log_msg "$module" OK "paquets disponibles avant mise a jour : $before_count"
}
