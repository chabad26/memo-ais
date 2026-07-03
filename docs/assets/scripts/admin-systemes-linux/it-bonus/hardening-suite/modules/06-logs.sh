#!/usr/bin/env bash
set -euo pipefail

# Auteur : Olivier
# Date : 2026-07-03
# Module : 06-logs
# Objet : rsyslog dedie SSH AlpesNet et rotation des logs.
# Usage : lance par main.sh
# Dependances : rsyslog, logrotate, logger

run_module() {
  local module="06-logs"
  local rsyslog_conf="/etc/rsyslog.d/30-alpesnet-ssh.conf"
  local logrotate_conf="/etc/logrotate.d/alpesnet-ssh"
  mkdir -p "$(dirname "$LOG_SSH_FILE")"

  write_file "$module" "$rsyslog_conf" "auth,authpriv.* ${LOG_SSH_FILE}"
  write_file "$module" "$logrotate_conf" "${LOG_SSH_FILE} {
    daily
    rotate ${LOGROTATE_RETENTION}
    compress
    missingok
    notifempty
    create 0640 root adm
}"
  run_cmd "$module" "rsyslogd -N1"
  run_cmd "$module" "systemctl restart rsyslog"
  run_cmd "$module" "logger -p authpriv.info 'ALPESNET_TEST_SSH_LOG'"
  run_cmd "$module" "logrotate -d '$logrotate_conf'"
}
