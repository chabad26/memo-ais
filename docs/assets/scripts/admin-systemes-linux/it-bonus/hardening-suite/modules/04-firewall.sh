#!/usr/bin/env bash
set -euo pipefail

# Auteur : Olivier
# Date : 2026-07-03
# Module : 04-firewall
# Objet : pare-feu UFW et protection brute force SSH avec Fail2ban.
# Usage : lance par main.sh
# Dependances : ufw, fail2ban

run_module() {
  local module="04-firewall"
  local rule port_proto source port proto jail

  run_cmd "$module" "ufw --force default deny incoming"
  run_cmd "$module" "ufw --force default allow outgoing"
  for rule in "${UFW_RULES[@]}"; do
    port_proto="${rule%%:*}"
    source="${rule#*:}"
    port="${port_proto%%/*}"
    proto="${port_proto#*/}"
    if [ "$source" = "any" ]; then
      run_cmd "$module" "ufw allow '$port/$proto'"
    else
      run_cmd "$module" "ufw allow from '$source' to any port '$port' proto '$proto'"
    fi
  done
  run_cmd "$module" "ufw --force enable"

  mkdir -p /etc/fail2ban/jail.d
  jail="[sshd]
enabled = true
port = ssh
filter = sshd
logpath = %(sshd_log)s
bantime = ${FAIL2BAN_BANTIME}
findtime = ${FAIL2BAN_FINDTIME}
maxretry = ${FAIL2BAN_MAXRETRY}"
  write_file "$module" "/etc/fail2ban/jail.d/alpesnet-sshd.local" "$jail"
  run_cmd "$module" "fail2ban-client -t"
  run_cmd "$module" "systemctl enable --now fail2ban"
  run_cmd "$module" "systemctl restart fail2ban"
  run_cmd "$module" "ufw status verbose"
  run_cmd "$module" "fail2ban-client status sshd"
}
