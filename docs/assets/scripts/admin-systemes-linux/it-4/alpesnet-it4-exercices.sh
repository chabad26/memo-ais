#!/usr/bin/env bash
set -u
set -o pipefail

# AlpesNet - Iteration 4 automation script
# Goal: run the NFS, Samba and Linux hardening exercises, then produce
# a final Markdown log with commands, results and explanations.

SCRIPT_NAME="$(basename "$0")"
RUN_ID="$(date +%Y%m%d_%H%M%S)"
LOG_DIR="${LOG_DIR:-/var/log/alpesnet-it4}"
REPORT="${REPORT:-$LOG_DIR/rapport-it4-$RUN_ID.md}"
RAW_LOG="${RAW_LOG:-$LOG_DIR/execution-it4-$RUN_ID.log}"

CAMPUS_SUBNET="${CAMPUS_SUBNET:-192.168.56.0/24}"
SERVER_IP="${SERVER_IP:-$(hostname -I 2>/dev/null | awk '{print $1}')}"
NFS_EXPORT_DIR="${NFS_EXPORT_DIR:-/exports/projets-alpesnet}"
NFS_CLIENT_MOUNT="${NFS_CLIENT_MOUNT:-/mnt/alpesnet-projets}"
SAMBA_DIR="${SAMBA_DIR:-/samba/equipe}"
SAMBA_SHARE="${SAMBA_SHARE:-equipe-alpesnet}"
DEVOPS_GROUP="${DEVOPS_GROUP:-devops}"
ALICE_USER="${ALICE_USER:-alice.martin}"
BOB_USER="${BOB_USER:-bob.dupont}"
SAMBA_PASSWORD="${SAMBA_PASSWORD:-AlpesNet-2026!}"
SSH_ALLOW_USERS="${SSH_ALLOW_USERS:-${SUDO_USER:-${USER}}}"
DISABLE_UNUSED_SERVICE="${DISABLE_UNUSED_SERVICE:-avahi-daemon}"
CONFIRM_SSH_KEYS="${CONFIRM_SSH_KEYS:-no}"
CONFIRM_UFW="${CONFIRM_UFW:-no}"
DRY_RUN=0
CLIENT_TESTS=0
STEP=0
COMPLETED=0
CURRENT_ACTION="initialisation"

usage() {
  cat <<USAGE
Usage:
  sudo ./$SCRIPT_NAME [options]

Options:
  --dry-run          Log commands without applying changes.
  --client-tests     Also run local client tests for NFS and Samba.
  -h, --help         Show this help.

Important environment variables:
  CAMPUS_SUBNET      Authorized subnet. Default: $CAMPUS_SUBNET
  SSH_ALLOW_USERS    SSH users allowed by AllowUsers. Default: $SSH_ALLOW_USERS
  CONFIRM_SSH_KEYS   Must be "yes" to apply PasswordAuthentication no.
  CONFIRM_UFW        Must be "yes" to enable UFW automatically.
  SAMBA_PASSWORD     Password used for Samba test users.

Recommended safe launch:
  sudo CONFIRM_SSH_KEYS=yes CONFIRM_UFW=yes SSH_ALLOW_USERS="adm-oliv oliv" CAMPUS_SUBNET="192.168.56.0/24" ./$SCRIPT_NAME --client-tests
USAGE
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=1 ;;
    --client-tests) CLIENT_TESTS=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 2 ;;
  esac
  shift
done

if [ "$(id -u)" -ne 0 ] && [ "$DRY_RUN" -ne 1 ]; then
  echo "Run this script with sudo/root." >&2
  exit 1
fi

mkdir -p "$LOG_DIR"
: > "$RAW_LOG"

cat > "$REPORT" <<EOF_REPORT
# Rapport automatique - Iteration 4 AlpesNet

| Champ | Valeur |
| --- | --- |
| Date | $(date '+%Y-%m-%d %H:%M:%S') |
| Machine | $(hostname) |
| IP detectee | ${SERVER_IP:-non detectee} |
| Sous-reseau autorise | $CAMPUS_SUBNET |
| Utilisateurs SSH autorises | $SSH_ALLOW_USERS |
| Mode dry-run | $DRY_RUN |

Ce rapport liste les commandes executees par le script, leur resultat et l'explication associee.

EOF_REPORT

finish_report_on_exit() {
  local status=$?

  if [ "$COMPLETED" -eq 1 ]; then
    return "$status"
  fi

  {
    echo
    echo "# Execution interrompue"
    echo
    echo "| Champ | Valeur |"
    echo "| --- | --- |"
    echo "| Code retour | \`$status\` |"
    echo "| Derniere action | $CURRENT_ACTION |"
    echo
    echo "Le rapport est incomplet : le script s'est arrete avant la synthese finale."
    echo "Relancer le script apres correction du point indique dans la sortie terminale ou le log brut."
  } >> "$REPORT"
}

trap finish_report_on_exit EXIT

abort_run() {
  local status="$1"
  local message="$2"

  CURRENT_ACTION="$message"

  {
    echo
    echo "# Arret de securite"
    echo
    echo "$message"
  } >> "$REPORT"

  echo "$message" >&2
  exit "$status"
}

append_report() {
  local title="$1"
  local command="$2"
  local status="$3"
  local explanation="$4"
  local output_file="$5"

  {
    echo "## $title"
    echo
    echo "**Commande**"
    echo
    echo '```bash'
    echo "$command"
    echo '```'
    echo
    echo "**Resultat** : code retour \`$status\`"
    echo
    echo '```text'
    if [ -s "$output_file" ]; then
      sed -n '1,160p' "$output_file"
      if [ "$(wc -l < "$output_file")" -gt 160 ]; then
        echo "... sortie tronquee dans le rapport, voir $RAW_LOG"
      fi
    else
      echo "(aucune sortie)"
    fi
    echo '```'
    echo
    echo "**Explication**"
    echo
    echo "$explanation"
    echo
  } >> "$REPORT"
}

run_cmd() {
  local title="$1"
  local command="$2"
  local explanation="$3"
  local allow_fail="${4:-no}"
  local output_file
  local status

  STEP=$((STEP + 1))
  CURRENT_ACTION="$title"
  output_file="$(mktemp)"

  printf '\n[%02d] %s\n' "$STEP" "$title"
  printf '     Commande: %s\n' "$command"
  printf '     Execution...\n'

  echo "### $title" >> "$RAW_LOG"
  echo "$command" >> "$RAW_LOG"

  if [ "$DRY_RUN" -eq 1 ]; then
    echo "[DRY-RUN] $command" > "$output_file"
    status=0
  else
    bash -o pipefail -c "$command" > "$output_file" 2>&1
    status=$?
  fi

  cat "$output_file" >> "$RAW_LOG"
  echo >> "$RAW_LOG"
  append_report "$title" "$command" "$status" "$explanation" "$output_file"

  if [ "$status" -ne 0 ] && [ "$allow_fail" != "yes" ]; then
    printf '     Statut: ERREUR (code %s)\n' "$status"
    printf '     Rapport: %s\n' "$REPORT"
    echo "ERROR at step: $title" >&2
    echo "See report: $REPORT" >&2
    rm -f "$output_file"
    exit "$status"
  fi

  if [ "$status" -ne 0 ]; then
    printf '     Statut: ECHEC ATTENDU (code %s)\n' "$status"
  else
    printf '     Statut: OK\n'
  fi
  printf '     Rapport mis a jour: %s\n' "$REPORT"

  rm -f "$output_file"
}

section() {
  printf '\n=== %s ===\n' "$1"
  {
    echo
    echo "# $1"
    echo
  } >> "$REPORT"
}

has_authorized_key() {
  local user="$1"
  local home_dir
  home_dir="$(getent passwd "$user" | cut -d: -f6)"
  [ -n "$home_dir" ] && [ -s "$home_dir/.ssh/authorized_keys" ]
}

ensure_ssh_safety() {
  local user

  if [ "$DRY_RUN" -eq 1 ]; then
    return 0
  fi

  if [ "$CONFIRM_SSH_KEYS" != "yes" ]; then
    abort_run 10 "Security stop. CONFIRM_SSH_KEYS=yes is required before applying PasswordAuthentication no. Reason: without a valid SSH key for an allowed user, the script could lock you out."
  fi

  for user in $SSH_ALLOW_USERS; do
    if ! getent passwd "$user" >/dev/null; then
      abort_run 11 "Allowed SSH user does not exist: $user"
    fi
  done

  for user in $SSH_ALLOW_USERS; do
    if has_authorized_key "$user"; then
      return 0
    fi
  done

  abort_run 12 "No authorized_keys found for SSH_ALLOW_USERS=[$SSH_ALLOW_USERS]. Stop."
}

ensure_ufw_safety() {
  if [ "$DRY_RUN" -eq 1 ]; then
    return 0
  fi

  if [ "$CONFIRM_UFW" != "yes" ]; then
    abort_run 13 "Security stop. CONFIRM_UFW=yes is required before enabling UFW. Reason: verify CAMPUS_SUBNET first, otherwise SSH can be blocked. Current CAMPUS_SUBNET=$CAMPUS_SUBNET"
  fi
}

section "Preparation et etat initial"

run_cmd \
  "Installer les paquets necessaires" \
  "apt-get update && apt-get install -y nfs-kernel-server nfs-common samba smbclient fail2ban ufw" \
  "Installe les services utilises pendant l'iteration 4 : NFS, Samba, client SMB, Fail2ban et UFW."

run_cmd \
  "Capturer les ports AVANT" \
  "ss -tulnp | grep LISTEN | tee /tmp/ports-avant.txt" \
  "Conserve l'etat initial des ports en ecoute pour comparer la surface exposee avant et apres durcissement." \
  "yes"

run_cmd \
  "Capturer les services AVANT" \
  "systemctl list-units --type=service --state=active | tee /tmp/services-avant.txt" \
  "Conserve la liste des services actifs avant modification."

run_cmd \
  "Preparer le groupe devops" \
  "getent group '$DEVOPS_GROUP' >/dev/null || groupadd '$DEVOPS_GROUP'; getent group '$DEVOPS_GROUP'" \
  "Cree le groupe projet si necessaire. Il servira aux droits NFS et Samba."

run_cmd \
  "Preparer les utilisateurs de test" \
  "id '$ALICE_USER' >/dev/null 2>&1 || useradd -m -s /bin/bash '$ALICE_USER'; id '$BOB_USER' >/dev/null 2>&1 || useradd -m -s /bin/bash '$BOB_USER'; usermod -aG '$DEVOPS_GROUP' '$ALICE_USER'; gpasswd -d '$BOB_USER' '$DEVOPS_GROUP' >/dev/null 2>&1 || true; id '$ALICE_USER'; id '$BOB_USER'" \
  "Cree ou verifie les comptes de test. Alice est membre de devops, Bob reste hors du groupe pour valider les refus."

section "Exercice 1 - NFS AlpesNet"

run_cmd \
  "Creer le repertoire NFS" \
  "mkdir -p '$NFS_EXPORT_DIR' && chown '$ALICE_USER:$DEVOPS_GROUP' '$NFS_EXPORT_DIR' && chmod 770 '$NFS_EXPORT_DIR' && ls -ld '$NFS_EXPORT_DIR'" \
  "Prepare le dossier exporte avec les droits attendus : alice.martin et le groupe devops ont acces, les autres sont exclus."

run_cmd \
  "Configurer /etc/exports" \
  "cp -a /etc/exports /etc/exports.bak.$RUN_ID; grep -v '^$NFS_EXPORT_DIR[[:space:]]' /etc/exports > /tmp/exports.$RUN_ID; printf '%s  %s(rw,sync,no_subtree_check,root_squash)\\n' '$NFS_EXPORT_DIR' '$CAMPUS_SUBNET' >> /tmp/exports.$RUN_ID; install -m 0644 /tmp/exports.$RUN_ID /etc/exports; grep '$NFS_EXPORT_DIR' /etc/exports" \
  "Ajoute l'export NFS limite au sous-reseau autorise, avec root_squash pour eviter que root client devienne root serveur."

run_cmd \
  "Appliquer et verifier les exports NFS" \
  "exportfs -arv && systemctl enable --now nfs-kernel-server && exportfs -v" \
  "Recharge les exports, demarre NFS et affiche la configuration effective."

section "Exercice 2 - Samba AlpesNet"

run_cmd \
  "Creer le repertoire Samba" \
  "mkdir -p '$SAMBA_DIR' && chown 'root:$DEVOPS_GROUP' '$SAMBA_DIR' && chmod 1770 '$SAMBA_DIR' && ls -ld '$SAMBA_DIR'" \
  "Prepare le partage Samba avec sticky bit : seuls les proprietaires de fichiers peuvent supprimer leurs propres fichiers."

run_cmd \
  "Configurer le partage Samba" \
  "cp -a /etc/samba/smb.conf /etc/samba/smb.conf.bak.$RUN_ID; awk 'BEGIN{skip=0} /^\\[$SAMBA_SHARE\\]/{skip=1; next} /^\\[/{skip=0} !skip{print}' /etc/samba/smb.conf > /tmp/smb.conf.$RUN_ID; printf '%s\\n' '[$SAMBA_SHARE]' '   comment = Partage equipe AlpesNet' '   path = $SAMBA_DIR' '   browseable = yes' '   writable = yes' '   valid users = @$DEVOPS_GROUP' '   create mask = 0664' '   directory mask = 0775' >> /tmp/smb.conf.$RUN_ID; install -m 0644 /tmp/smb.conf.$RUN_ID /etc/samba/smb.conf; grep -A8 '^\\[$SAMBA_SHARE\\]' /etc/samba/smb.conf" \
  "Ajoute un partage Samba limite aux membres du groupe devops."

run_cmd \
  "Creer les utilisateurs Samba" \
  "printf '%s\\n%s\\n' '$SAMBA_PASSWORD' '$SAMBA_PASSWORD' | smbpasswd -s -a '$ALICE_USER'; printf '%s\\n%s\\n' '$SAMBA_PASSWORD' '$SAMBA_PASSWORD' | smbpasswd -s -a '$BOB_USER'; pdbedit -L | grep -E '$ALICE_USER|$BOB_USER'" \
  "Ajoute Alice et Bob dans la base Samba. Bob existe pour prouver que valid users=@devops le bloque quand meme."

run_cmd \
  "Valider et demarrer Samba" \
  "testparm -s && systemctl enable --now smbd nmbd && systemctl --no-pager --full status smbd | sed -n '1,12p'" \
  "Verifie la syntaxe Samba, demarre les services et conserve une preuve de leur etat."

section "Exercice 3 - Durcissement SSH, UFW, Fail2ban et services"

ensure_ssh_safety
run_cmd \
  "Sauvegarder et durcir SSH" \
  "cp -a /etc/ssh/sshd_config /etc/ssh/sshd_config.bak.$RUN_ID; mkdir -p /etc/ssh/sshd_config.d; printf '%s\\n' 'PermitRootLogin no' 'PasswordAuthentication no' 'PubkeyAuthentication yes' 'AllowUsers $SSH_ALLOW_USERS' 'MaxAuthTries 3' 'LoginGraceTime 20' 'ClientAliveInterval 300' 'ClientAliveCountMax 2' 'X11Forwarding no' 'AllowTcpForwarding no' > /etc/ssh/sshd_config.d/99-alpesnet-hardening.conf; sshd -t && systemctl reload sshd; sed -n '1,80p' /etc/ssh/sshd_config.d/99-alpesnet-hardening.conf" \
  "Applique le durcissement SSH dans un fichier de configuration separe, verifie la syntaxe puis recharge SSH sans couper la session active."

ensure_ufw_safety
run_cmd \
  "Configurer UFW" \
  "ufw default deny incoming; ufw default allow outgoing; ufw allow from '$CAMPUS_SUBNET' to any port 22 proto tcp; ufw allow from '$CAMPUS_SUBNET' to any port nfs; ufw allow from '$CAMPUS_SUBNET' to any port 445 proto tcp; ufw allow from '$CAMPUS_SUBNET' to any port 139 proto tcp; ufw --force enable; ufw logging on; ufw status verbose" \
  "Active une politique entrante restrictive et autorise uniquement SSH, NFS et Samba depuis le sous-reseau du lab."

run_cmd \
  "Configurer Fail2ban pour SSH" \
  "if [ -f /etc/fail2ban/jail.local ]; then cp -a /etc/fail2ban/jail.local /etc/fail2ban/jail.local.bak.$RUN_ID; mv /etc/fail2ban/jail.local /etc/fail2ban/jail.local.disabled.$RUN_ID; fi; mkdir -p /etc/fail2ban/jail.d; printf '%s\\n' '[DEFAULT]' 'bantime = 3600' 'findtime = 600' 'maxretry = 3' '' '[sshd]' 'enabled = true' > /etc/fail2ban/jail.d/alpesnet-sshd.local; fail2ban-client -t && systemctl restart fail2ban && sleep 1 && systemctl is-active fail2ban && fail2ban-client status sshd || { systemctl --no-pager --full status fail2ban; journalctl -u fail2ban -n 80 --no-pager; exit 1; }" \
  "Sauvegarde et neutralise un ancien jail.local potentiellement casse, cree une configuration locale propre pour sshd, teste la configuration puis redemarre Fail2ban."

run_cmd \
  "Analyser les services actifs non essentiels" \
  "systemctl list-units --type=service --state=active | grep -Ev 'ssh|rsyslog|cron|fail2ban|ufw|nfs|smb|systemd' | tee /tmp/services-a-analyser.txt || true" \
  "Liste les services actifs qui ne font pas partie du socle attendu. Cette etape aide a justifier ou desactiver ce qui est inutile."

run_cmd \
  "Desactiver un service inutile si present" \
  "if systemctl list-unit-files '$DISABLE_UNUSED_SERVICE.service' >/dev/null 2>&1; then systemctl disable --now '$DISABLE_UNUSED_SERVICE' || true; else echo '$DISABLE_UNUSED_SERVICE absent'; fi" \
  "Desactive le service defini dans DISABLE_UNUSED_SERVICE lorsqu'il existe. Par defaut : avahi-daemon."

section "Validations locales et preuves"

run_cmd \
  "Test NFS avec Alice cote serveur" \
  "su - '$ALICE_USER' -c 'touch $NFS_EXPORT_DIR/test-alice-script.txt && ls -l $NFS_EXPORT_DIR/test-alice-script.txt'" \
  "Valide qu'Alice, proprietaire du dossier et membre de devops, peut creer un fichier dans l'export NFS."

run_cmd \
  "Test NFS avec Bob cote serveur attendu en refus" \
  "su - '$BOB_USER' -c 'touch $NFS_EXPORT_DIR/test-bob-script.txt'" \
  "Bob n'est pas membre de devops. Le refus confirme les permissions 770 du repertoire NFS." \
  "yes"

run_cmd \
  "Test Samba Alice en local" \
  "printf 'preuve samba script\\n' > /tmp/test-samba-alice-script.txt; smbclient '//127.0.0.1/$SAMBA_SHARE' -U '$ALICE_USER%$SAMBA_PASSWORD' -c 'put /tmp/test-samba-alice-script.txt test-samba-alice-script.txt; ls'" \
  "Valide qu'Alice peut se connecter au partage Samba et deposer un fichier."

run_cmd \
  "Test Samba Bob attendu en refus" \
  "smbclient '//127.0.0.1/$SAMBA_SHARE' -U '$BOB_USER%$SAMBA_PASSWORD' -c 'ls'" \
  "Bob a un compte Samba mais n'est pas dans devops. Le refus prouve que valid users=@devops fonctionne." \
  "yes"

if [ "$CLIENT_TESTS" -eq 1 ]; then
  section "Tests client locaux optionnels"

  run_cmd \
    "Monter le partage NFS en client local" \
    "mkdir -p '$NFS_CLIENT_MOUNT'; mountpoint -q '$NFS_CLIENT_MOUNT' && umount '$NFS_CLIENT_MOUNT' || true; mount '127.0.0.1:$NFS_EXPORT_DIR' '$NFS_CLIENT_MOUNT'; df -h | grep -E '$NFS_CLIENT_MOUNT|nfs'" \
    "Monte l'export NFS depuis le serveur lui-meme pour obtenir une preuve de montage. En TP, ce test est normalement fait depuis le laptop."

  run_cmd \
    "Tester root_squash depuis le montage NFS" \
    "touch '$NFS_CLIENT_MOUNT/test-root-squash-script.txt'; ls -l '$NFS_EXPORT_DIR/test-root-squash-script.txt' '$NFS_CLIENT_MOUNT/test-root-squash-script.txt'" \
    "Teste l'effet root_squash. Selon le contexte local, le fichier doit apparaitre avec l'identite nobody/nogroup ou etre refuse si les droits ne le permettent pas." \
    "yes"

  run_cmd \
    "Demonter le partage NFS local" \
    "umount '$NFS_CLIENT_MOUNT'" \
    "Nettoie le montage client local apres les tests."
fi

run_cmd \
  "Capturer les ports APRES" \
  "ss -tulnp | grep LISTEN | tee /tmp/ports-apres.txt" \
  "Conserve l'etat des ports apres configuration et durcissement." \
  "yes"

run_cmd \
  "Comparer ports avant/apres" \
  "diff -u /tmp/ports-avant.txt /tmp/ports-apres.txt || true" \
  "Produit la comparaison attendue pour le rapport de durcissement."

run_cmd \
  "Verifier les services en echec" \
  "systemctl list-units --state=failed" \
  "Verifie qu'aucun service critique n'est casse apres execution."

run_cmd \
  "Verifier les journaux Samba et Fail2ban" \
  "grep -R '$ALICE_USER\\|$BOB_USER' /var/log/samba/ 2>/dev/null | tail -20 || true; fail2ban-client status sshd" \
  "Ajoute au rapport les traces utiles : connexions Samba et etat de la jail Fail2ban."

{
  echo "# Synthese finale"
  echo
  echo "- Rapport Markdown : \`$REPORT\`"
  echo "- Log brut : \`$RAW_LOG\`"
  echo "- Exports NFS : \`exportfs -v\`"
  echo "- Partage Samba : \`testparm -s\` et \`smbclient //127.0.0.1/$SAMBA_SHARE -U $ALICE_USER\`"
  echo "- Durcissement SSH : \`sshd -t\` et test depuis un nouveau terminal"
  echo "- UFW : \`ufw status verbose\`"
  echo "- Fail2ban : \`fail2ban-client status sshd\`"
  echo
  echo "Important : le bannissement Fail2ban reel se teste depuis un autre terminal/client avec plusieurs tentatives SSH echouees."
} >> "$REPORT"

COMPLETED=1

echo "Done."
echo "Report: $REPORT"
echo "Raw log: $RAW_LOG"
