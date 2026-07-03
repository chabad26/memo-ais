#!/usr/bin/env bash
set -euo pipefail

# Auteur : Olivier
# Date : 2026-07-03
# Module : 03-ssh
# Objet : durcissement SSH avec validation sshd -t avant rechargement.
# Usage : lance par main.sh
# Dependances : openssh-server, systemctl

run_module() {
  local module="03-ssh"
  local target="/etc/ssh/sshd_config.d/99-alpesnet-hardening.conf"
  local content
  content="# AlpesNet hardening
PermitRootLogin ${SSH_PERMIT_ROOT}
PasswordAuthentication ${SSH_PASSWORD_AUTH}
AllowUsers ${SSH_ALLOW_USERS}
MaxAuthTries ${SSH_MAX_AUTH_TRIES}
LoginGraceTime ${SSH_LOGIN_GRACE_TIME}"

  mkdir -p /etc/ssh/sshd_config.d
  write_file "$module" "$target" "$content"
  run_cmd "$module" "sshd -t"
  if systemctl list-unit-files ssh.service >/dev/null 2>&1; then
    run_cmd "$module" "systemctl reload ssh"
  else
    run_cmd "$module" "systemctl reload sshd"
  fi
  log_msg "$module" OK "configuration SSH validee avant rechargement"
}
