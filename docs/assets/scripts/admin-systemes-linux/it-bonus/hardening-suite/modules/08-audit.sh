#!/usr/bin/env bash
set -euo pipefail

# Auteur : Olivier
# Date : 2026-07-03
# Module : 08-audit
# Objet : rapport final PASS/FAIL/WARN exploitable sans commande supplementaire.
# Usage : lance par main.sh
# Dependances : awk, ss, systemctl, ufw, fail2ban-client

audit_block() {
  local title="$1"
  local command="$2"
  {
    echo
    echo "## $title"
    echo
    echo '```text'
    bash -o pipefail -c "$command" 2>&1 || true
    echo '```'
  } >> "$AUDIT_REPORT"
}

run_module() {
  local module="08-audit"
  local now os total pass fail warn score
  now="$(date +%Y%m%d_%H%M%S)"
  AUDIT_REPORT="${REPORT_DIR}/audit-$(hostname)-${now}.txt"
  AUDIT_CHECKS_FILE="${REPORT_DIR}/audit-checks-${now}.tsv"
  : > "$AUDIT_CHECKS_FILE"

  os="$(. /etc/os-release 2>/dev/null && printf '%s %s' "${PRETTY_NAME:-inconnu}" "${VERSION_ID:-}")"
  {
    echo "# Rapport d'audit AlpesNet Hardening"
    echo
    echo "Hostname: $(hostname)"
    echo "IP: $(hostname -I 2>/dev/null | awk '{print $1}')"
    echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "OS: ${os:-inconnu}"
    echo "Duree totale hardening: ${TOTAL_DURATION:-0}s"
  } > "$AUDIT_REPORT"

  append_check PASS "En-tete" "hostname, IP, date et OS renseignes"
  if awk -F: '($3 == 0 && $1 != "root") {print $1}' /etc/passwd | grep -q .; then
    append_check FAIL "Comptes" "compte non-root avec UID 0 detecte"
  else
    append_check PASS "Comptes" "aucun compte non-root UID 0"
  fi
  if grep -R "NOPASSWD: *ALL" /etc/sudoers /etc/sudoers.d 2>/dev/null | grep -v '^#' | grep -q .; then
    append_check FAIL "Comptes" "NOPASSWD: ALL detecte"
  else
    append_check PASS "Comptes" "aucun NOPASSWD: ALL detecte"
  fi
  sshd -T 2>/dev/null | grep -Eq 'permitrootlogin no' && append_check PASS "SSH" "PermitRootLogin no actif" || append_check FAIL "SSH" "PermitRootLogin no absent"
  sshd -T 2>/dev/null | grep -Eq 'passwordauthentication no' && append_check PASS "SSH" "PasswordAuthentication no actif" || append_check WARN "SSH" "PasswordAuthentication no absent ou non verifiable"
  ufw status 2>/dev/null | grep -qi active && append_check PASS "Pare-feu" "ufw actif" || append_check FAIL "Pare-feu" "ufw inactif"
  systemctl is-active fail2ban >/dev/null 2>&1 && append_check PASS "Pare-feu" "fail2ban actif" || append_check FAIL "Pare-feu" "fail2ban inactif"
  rsyslogd -N1 >/dev/null 2>&1 && append_check PASS "Logs" "syntaxe rsyslog valide" || append_check FAIL "Logs" "syntaxe rsyslog invalide"
  logrotate -d /etc/logrotate.d/alpesnet-ssh >/dev/null 2>&1 && append_check PASS "Logs" "logrotate SSH valide" || append_check WARN "Logs" "logrotate SSH non verifiable"
  compgen -G "${BACKUP_DEST}-*/checksums.sha256" >/dev/null && append_check PASS "Sauvegarde" "checksum de sauvegarde present" || append_check WARN "Sauvegarde" "checksum de sauvegarde absent"
  [ -f /etc/cron.d/alpesnet-backup ] && append_check PASS "Sauvegarde" "cron de sauvegarde present" || append_check WARN "Sauvegarde" "cron de sauvegarde absent"

  audit_block "Comptes avec shell actif" "awk -F: '(\$7 !~ /(nologin|false)$/) {print \$1\":\"\$3\":\"\$7}' /etc/passwd"
  audit_block "UID 0" "awk -F: '(\$3==0) {print \$1\":\"\$3}' /etc/passwd"
  audit_block "Membres sudo" "getent group sudo"
  audit_block "SSH actif" "sshd -T | grep -E 'permitroot|password|allowusers|maxauth'"
  audit_block "Pare-feu UFW" "ufw status verbose"
  audit_block "Fail2ban" "fail2ban-client status; fail2ban-client status sshd"
  audit_block "Ports ouverts" "ss -tulnp"
  audit_block "Services actifs" "systemctl list-units --type=service --state=running --no-pager"
  audit_block "Rsyslog" "rsyslogd -N1"
  audit_block "Logrotate" "logrotate -d /etc/logrotate.d/alpesnet-ssh"
  audit_block "Sauvegardes" "ls -lh ${BACKUP_DEST}-* 2>/dev/null; cat /etc/cron.d/alpesnet-backup 2>/dev/null"

  {
    echo
    echo "## Execution"
    echo
    echo "| Module | Statut | Duree |"
    echo "| --- | --- | --- |"
    if [ -f "$RUN_TIMES_FILE" ]; then
      sort -t '	' -k3,3nr "$RUN_TIMES_FILE" | while IFS='	' read -r m s d; do
        echo "| $m | $s | ${d}s |"
      done
    fi
    echo
    echo "## Score"
    echo
    echo "| Statut | Section | Detail |"
    echo "| --- | --- | --- |"
    while IFS='	' read -r status section detail; do
      echo "| $status | $section | $detail |"
    done < "$AUDIT_CHECKS_FILE"
  } >> "$AUDIT_REPORT"

  total="$(wc -l < "$AUDIT_CHECKS_FILE")"
  pass="$(awk -F '\t' '$1=="PASS"{c++} END{print c+0}' "$AUDIT_CHECKS_FILE")"
  fail="$(awk -F '\t' '$1=="FAIL"{c++} END{print c+0}' "$AUDIT_CHECKS_FILE")"
  warn="$(awk -F '\t' '$1=="WARN"{c++} END{print c+0}' "$AUDIT_CHECKS_FILE")"
  score="PASS=${pass}/${total} WARN=${warn} FAIL=${fail}"
  printf '\nScore global: %s\n' "$score" >> "$AUDIT_REPORT"
  log_msg "$module" OK "rapport genere : $AUDIT_REPORT ($score)"
}
