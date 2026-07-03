#!/usr/bin/env bash
set -euo pipefail

# Auteur : Olivier
# Date : 2026-07-03
# Module : main
# Objet : orchestrateur AlpesNet Hardening Suite.
# Usage : sudo ./main.sh --menu | --all | --modules 01,02,03 | --audit-only [--dry-run]
# Dependances : Bash, systemd, outils GNU standard

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config/alpesnet.conf"
MODULE_DIR="$SCRIPT_DIR/modules"
REPORT_DIR="$SCRIPT_DIR/rapports"
RUN_ID="$(date +%Y%m%d_%H%M%S)"
LOG_DIR="/var/log/alpesnet"
LOGFILE="$LOG_DIR/hardening-${RUN_ID}.log"
RUN_TIMES_FILE="$REPORT_DIR/run-times-${RUN_ID}.tsv"
LOCKFILE="/var/lock/alpesnet-hardening.lock"
DRY_RUN=0
MENU_MODE=0
SSHUSER_OVERRIDE=""
REQUESTED_MODULES=()
TOTAL_START="$(date +%s)"
TOTAL_DURATION=0

declare -A MODULE_FILES=(
  ["01-systeme"]="01-systeme.sh"
  ["02-utilisateurs"]="02-utilisateurs.sh"
  ["03-ssh"]="03-ssh.sh"
  ["04-firewall"]="04-firewall.sh"
  ["05-services"]="05-services.sh"
  ["06-logs"]="06-logs.sh"
  ["07-sauvegarde"]="07-sauvegarde.sh"
  ["08-audit"]="08-audit.sh"
)

MODULE_ORDER=(
  "01-systeme"
  "02-utilisateurs"
  "03-ssh"
  "04-firewall"
  "05-services"
  "06-logs"
  "07-sauvegarde"
  "08-audit"
)

declare -A MODULE_TITLES=(
  ["01-systeme"]="Mise a jour systeme et outils de base"
  ["02-utilisateurs"]="Comptes, groupes et sudo restreint"
  ["03-ssh"]="Durcissement SSH"
  ["04-firewall"]="Pare-feu UFW et Fail2ban"
  ["05-services"]="Services inutiles et ports ouverts"
  ["06-logs"]="Rsyslog et logrotate SSH"
  ["07-sauvegarde"]="Rsync, cron et checksum"
  ["08-audit"]="Rapport d'audit PASS/FAIL/WARN"
)

declare -A DEPENDANCES=(
  ["01-systeme"]=""
  ["02-utilisateurs"]="01-systeme"
  ["03-ssh"]="01-systeme 02-utilisateurs"
  ["04-firewall"]="03-ssh"
  ["05-services"]="01-systeme"
  ["06-logs"]="01-systeme"
  ["07-sauvegarde"]="02-utilisateurs"
  ["08-audit"]=""
)

declare -A STATUT=()
declare -A DUREES=()

usage() {
  cat <<USAGE
Usage:
  sudo ./main.sh --menu
  sudo ./main.sh --all [--dry-run] [--sshuser oliv]
  sudo ./main.sh --modules 01,02,03 [--dry-run] [--sshuser oliv]
  sudo ./main.sh --audit-only

Options:
  --menu            Affiche un menu interactif avec la liste des modules.
  --all             Execute tous les modules dans l'ordre.
  --modules LISTE   Execute une liste: 01,02,03 ou 03-ssh,04-firewall.
  --audit-only      Execute uniquement le module 08-audit.
  --sshuser USER     Force AllowUsers SSH pour eviter de couper son acces.
  --dry-run         Simule les commandes sans modifier le systeme.
  -h, --help        Affiche cette aide.
USAGE
}

print_module_list() {
  local module deps
  echo
  echo "Modules disponibles"
  echo "-------------------"
  for module in "${MODULE_ORDER[@]}"; do
    deps="${DEPENDANCES[$module]}"
    printf '  %s  %-48s' "${module%%-*}" "${MODULE_TITLES[$module]}"
    if [ -n "$deps" ]; then
      printf ' dependances: %s' "$deps"
    else
      printf ' dependances: aucune'
    fi
    echo
  done
}

menu_select_modules() {
  local answer token normalized clean ssh_answer
  while true; do
    print_module_list
    cat <<MENU

Choix possibles :
  all            lancer tous les modules
  audit          lancer seulement le module 08
  dry-run        activer/desactiver le mode simulation
  1 2 3          lancer des modules par numeros
  01,02,03       lancer des modules par liste
  q              quitter

Mode dry-run actuel : $DRY_RUN
MENU
    read -r -p "Ton choix : " answer
    case "$answer" in
      q|Q|quit|exit)
        echo "Annule."
        exit 0
        ;;
      all|ALL)
        REQUESTED_MODULES=("${MODULE_ORDER[@]}")
        return 0
        ;;
      audit|AUDIT|8|08)
        REQUESTED_MODULES=("08-audit")
        return 0
        ;;
      dry-run|dryrun)
        if [ "$DRY_RUN" -eq 1 ]; then
          DRY_RUN=0
        else
          DRY_RUN=1
        fi
        continue
        ;;
      "")
        echo "Choix vide."
        continue
        ;;
    esac

    REQUESTED_MODULES=()
    clean="${answer//,/ }"
    for token in $clean; do
      normalized="$(normalize_module "$token")" || {
        echo "Module inconnu: $token"
        REQUESTED_MODULES=()
        break
      }
      REQUESTED_MODULES+=("$normalized")
    done
    if [ "${#REQUESTED_MODULES[@]}" -gt 0 ]; then
      break
    fi
  done

  if requested_contains "03-ssh" && [ -z "$SSHUSER_OVERRIDE" ]; then
    echo
    echo "Securite SSH : utilisateur autorise actuel : ${SSH_ALLOW_USERS:-non defini}"
    read -r -p "Utilisateur SSH a garder autorise [${SUDO_USER:-${USER:-oliv}}] : " ssh_answer
    SSHUSER_OVERRIDE="${ssh_answer:-${SUDO_USER:-${USER:-oliv}}}"
  fi
}

log_main() {
  local level="$1"
  local message="$2"
  printf '[%s] [main] [%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$level" "$message" | tee -a "$LOGFILE"
}

normalize_module() {
  local raw="$1"
  local module
  for module in "${MODULE_ORDER[@]}"; do
    if [ "$raw" = "$module" ] || [ "$raw" = "${module%%-*}" ]; then
      printf '%s\n' "$module"
      return 0
    fi
  done
  return 1
}

parse_args() {
  local item normalized
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --all)
        REQUESTED_MODULES=("${MODULE_ORDER[@]}")
        ;;
      --menu)
        MENU_MODE=1
        ;;
      --modules)
        shift
        [ "${1:-}" ] || { echo "--modules attend une liste" >&2; exit 2; }
        IFS=, read -r -a REQUESTED_MODULES <<< "$1"
        for item in "${!REQUESTED_MODULES[@]}"; do
          normalized="$(normalize_module "${REQUESTED_MODULES[$item]}")" || {
            echo "Module inconnu: ${REQUESTED_MODULES[$item]}" >&2
            exit 2
          }
          REQUESTED_MODULES[$item]="$normalized"
        done
        ;;
      --audit-only)
        REQUESTED_MODULES=("08-audit")
        ;;
      --sshuser)
        shift
        [ "${1:-}" ] || { echo "--sshuser attend un nom d'utilisateur" >&2; exit 2; }
        SSHUSER_OVERRIDE="$1"
        ;;
      --dry-run)
        DRY_RUN=1
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        echo "Option inconnue: $1" >&2
        usage
        exit 2
        ;;
    esac
    shift
  done
  if [ "$MENU_MODE" -eq 1 ]; then
    return 0
  fi
  if [ "${#REQUESTED_MODULES[@]}" -eq 0 ]; then
    usage
    exit 2
  fi
}

check_root_and_debian() {
  if [ "$(id -u)" -ne 0 ] && [ "$DRY_RUN" -ne 1 ]; then
    echo "Lancer avec sudo/root, ou utiliser --dry-run." >&2
    exit 1
  fi
  if [ -r /etc/os-release ]; then
    # shellcheck disable=SC1091
    . /etc/os-release
    if [ "${ID:-}" != "debian" ]; then
      echo "Distribution non supportee: ${PRETTY_NAME:-inconnue}. Cible: Debian 12." >&2
      exit 1
    fi
  fi
}

setup_runtime() {
  mkdir -p "$REPORT_DIR"
  if [ "$DRY_RUN" -eq 1 ] && [ "$(id -u)" -ne 0 ]; then
    LOG_DIR="/tmp/alpesnet"
    LOGFILE="$LOG_DIR/hardening-${RUN_ID}.log"
    LOCKFILE="/tmp/alpesnet-hardening.lock"
  fi
  mkdir -p "$LOG_DIR"
  : > "$RUN_TIMES_FILE"
  : > "$LOGFILE"
}

acquire_lock() {
  local old_pid
  if [ -f "$LOCKFILE" ]; then
    old_pid="$(cat "$LOCKFILE" 2>/dev/null || true)"
    if [ -n "$old_pid" ] && kill -0 "$old_pid" 2>/dev/null; then
      echo "ERREUR : une execution est deja en cours (PID $old_pid)" >&2
      exit 1
    fi
    echo "AVERTISSEMENT : verrou orphelin detecte (PID ${old_pid:-inconnu} inactif), nettoyage"
    rm -f "$LOCKFILE"
  fi
  echo "$$" > "$LOCKFILE"
  trap cleanup EXIT
}

cleanup() {
  rm -f "$LOCKFILE"
}

load_config() {
  if [ ! -r "$CONFIG_FILE" ]; then
    echo "Configuration absente: $CONFIG_FILE" >&2
    exit 1
  fi
  # shellcheck disable=SC1090
  . "$CONFIG_FILE"
  if [ -n "$SSHUSER_OVERRIDE" ]; then
    SSH_ALLOW_USERS="$SSHUSER_OVERRIDE"
  fi
}

validate_ssh_user_override() {
  if [ -z "$SSHUSER_OVERRIDE" ]; then
    return 0
  fi
  if ! [[ "$SSHUSER_OVERRIDE" =~ ^[a-z_][a-z0-9_-]*[$]?$ ]]; then
    echo "Nom d'utilisateur SSH invalide: $SSHUSER_OVERRIDE" >&2
    exit 2
  fi
}

requested_contains() {
  local wanted="$1"
  local module
  for module in "${REQUESTED_MODULES[@]}"; do
    [ "$module" = "$wanted" ] && return 0
  done
  return 1
}

dependencies_ok() {
  local module="$1"
  local dep
  for dep in ${DEPENDANCES[$module]}; do
    if [ "${STATUT[$dep]:-NON_EXECUTE}" != "OK" ]; then
      STATUT[$module]="SKIPPED"
      DUREES[$module]=0
      printf '%s\t%s\t%s\n' "$module" "SKIPPED" "0" >> "$RUN_TIMES_FILE"
      log_main WARN "$module saute : dependance '$dep' non satisfaite (statut: ${STATUT[$dep]:-non execute})"
      return 1
    fi
  done
  return 0
}

run_one_module() {
  local module="$1"
  local start end duration status file
  file="$MODULE_DIR/${MODULE_FILES[$module]}"
  if [ ! -r "$file" ]; then
    STATUT[$module]="FAIL"
    DUREES[$module]=0
    log_main ERROR "$module introuvable : $file"
    return 1
  fi
  dependencies_ok "$module" || return 0

  log_main INFO "demarrage $module"
  start="$(date +%s)"
  TOTAL_DURATION=$(($(date +%s) - TOTAL_START))
  set +e
  DRY_RUN="$DRY_RUN" SSHUSER_OVERRIDE="$SSHUSER_OVERRIDE" LOGFILE="$LOGFILE" REPORT_DIR="$REPORT_DIR" RUN_TIMES_FILE="$RUN_TIMES_FILE" TOTAL_DURATION="$TOTAL_DURATION" \
    bash -c "set -euo pipefail; source '$CONFIG_FILE'; if [ -n \"\${SSHUSER_OVERRIDE:-}\" ]; then SSH_ALLOW_USERS=\"\$SSHUSER_OVERRIDE\"; fi; source '$MODULE_DIR/_common.sh'; source '$file'; run_module"
  status=$?
  set -e
  end="$(date +%s)"
  duration=$((end - start))

  if [ "$status" -eq 0 ]; then
    STATUT[$module]="OK"
    log_main OK "$module termine en ${duration}s (statut: OK)"
  else
    STATUT[$module]="FAIL"
    log_main ERROR "$module termine en ${duration}s (statut: FAIL, code: $status)"
  fi
  DUREES[$module]="$duration"
  printf '%s\t%s\t%s\n' "$module" "${STATUT[$module]}" "$duration" >> "$RUN_TIMES_FILE"
  return 0
}

print_summary() {
  local module
  TOTAL_DURATION=$(($(date +%s) - TOTAL_START))
  log_main INFO "recapitulatif final - duree totale ${TOTAL_DURATION}s"
  {
    echo
    echo "Recapitulatif final"
    echo "Module | Statut | Duree"
    echo "--- | --- | ---"
    for module in "${MODULE_ORDER[@]}"; do
      if [ -n "${STATUT[$module]:-}" ]; then
        echo "$module | ${STATUT[$module]} | ${DUREES[$module]:-0}s"
      fi
    done
    echo
    echo "Tri du plus long au plus court"
    sort -t '	' -k3,3nr "$RUN_TIMES_FILE" | while IFS='	' read -r m s d; do
      echo "$m | $s | ${d}s"
    done
  } | tee -a "$LOGFILE"
}

main() {
  parse_args "$@"
  validate_ssh_user_override
  load_config
  if [ "$MENU_MODE" -eq 1 ]; then
    menu_select_modules
    validate_ssh_user_override
    load_config
  fi
  check_root_and_debian
  setup_runtime
  acquire_lock

  log_main INFO "run $RUN_ID"
  log_main INFO "log principal : $LOGFILE"
  log_main INFO "modules demandes : ${REQUESTED_MODULES[*]}"
  if [ -n "$SSHUSER_OVERRIDE" ]; then
    log_main INFO "override SSH_ALLOW_USERS : $SSH_ALLOW_USERS"
  fi

  local module
  for module in "${MODULE_ORDER[@]}"; do
    requested_contains "$module" || continue
    run_one_module "$module"
  done
  print_summary
}

main "$@"
