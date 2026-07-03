#!/usr/bin/env bash
set -euo pipefail

# Auteur : Olivier
# Date : 2026-07-03
# Module : 02-utilisateurs
# Objet : comptes, groupes, sudo restreint et controles UID 0/NOPASSWD.
# Usage : lance par main.sh
# Dependances : useradd, groupadd, visudo

run_module() {
  local module="02-utilisateurs"
  local group account login primary shell comment sudoers_file

  for group in "${GROUPES[@]}"; do
    if getent group "$group" >/dev/null; then
      log_msg "$module" OK "groupe deja present : $group"
    else
      run_cmd "$module" "groupadd '$group'"
    fi
  done

  for account in "${COMPTES[@]}"; do
    IFS=: read -r login primary shell comment <<< "$account"
    getent group "$primary" >/dev/null || run_cmd "$module" "groupadd '$primary'"
    if id "$login" >/dev/null 2>&1; then
      log_msg "$module" OK "compte deja present : $login"
      run_cmd "$module" "usermod -g '$primary' -s '$shell' -c '$comment' '$login'"
    else
      run_cmd "$module" "useradd -m -g '$primary' -s '$shell' -c '$comment' '$login'"
    fi
  done

  sudoers_file="/etc/sudoers.d/alpesnet-${SUDO_GROUP}"
  write_file "$module" "$sudoers_file" "%${SUDO_GROUP} ALL=(root) ${SUDO_ALLOWED_COMMANDS}"
  run_cmd "$module" "chmod 0440 '$sudoers_file'"
  run_cmd "$module" "visudo -cf '$sudoers_file'"

  if awk -F: '($3 == 0 && $1 != "root") {print $1}' /etc/passwd | grep -q .; then
    log_msg "$module" ERROR "un compte non-root possede UID 0"
    return 1
  fi
  if grep -R "NOPASSWD: *ALL" /etc/sudoers /etc/sudoers.d 2>/dev/null | grep -v '^#' | grep -q .; then
    log_msg "$module" ERROR "regle NOPASSWD: ALL detectee"
    return 1
  fi
  log_msg "$module" OK "controles comptes et sudo valides"
}
