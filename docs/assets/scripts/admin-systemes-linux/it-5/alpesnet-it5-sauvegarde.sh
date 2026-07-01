#!/usr/bin/env bash
set -u
set -o pipefail

# AlpesNet - Iteration 5
# Menu pas-a-pas pour sauvegarde, restauration, Nginx, securite et validations.

SCRIPT_NAME="$(basename "$0")"
RUN_ID="$(date +%Y%m%d_%H%M%S)"
LOG_DIR="${LOG_DIR:-/var/log/alpesnet-it5}"
REPORT="${REPORT:-$LOG_DIR/rapport-it5-$RUN_ID.md}"
RAW_LOG="${RAW_LOG:-$LOG_DIR/execution-it5-$RUN_ID.log}"
TIMELINE_LOG="${TIMELINE_LOG:-$LOG_DIR/timeline-it5-$RUN_ID.md}"

DATE_TAG="${DATE_TAG:-$(date +%Y%m%d)}"
SOURCE_DIR="${SOURCE_DIR:-/srv/alpesnet}"
BACKUP_DIR="${BACKUP_DIR:-/backup}"
RSYNC_DEST="${RSYNC_DEST:-$BACKUP_DIR/alpesnet-$DATE_TAG}"
CONFIG_ARCHIVE="${CONFIG_ARCHIVE:-$BACKUP_DIR/configs-$DATE_TAG.tar.gz}"
CHECKSUM_FILE="${CHECKSUM_FILE:-$BACKUP_DIR/checksums.txt}"
RESTORE_DIR="${RESTORE_DIR:-/tmp/restauration-test}"
RESTORE_WWW_DIR="${RESTORE_WWW_DIR:-/tmp/restauration-www-test}"
NGINX_USER="${NGINX_USER:-www-nginx}"
INTRANET_HOST="${INTRANET_HOST:-intranet.alpesnet.local}"
INTRANET_ROOT="${INTRANET_ROOT:-/var/www/intranet.alpesnet.local/html}"
PUBLIC_REPORT="${PUBLIC_REPORT:-$INTRANET_ROOT/rapport-it5.md}"
PRENOM="${PRENOM:-Oliv}"
CAMPUS_SUBNET="${CAMPUS_SUBNET:-192.168.56.0/24}"
WWW_BACKUP_DIR="${WWW_BACKUP_DIR:-$BACKUP_DIR/www}"
WWW_RESTORE_DIR="${WWW_RESTORE_DIR:-$RESTORE_WWW_DIR}"
DRY_RUN=0
AUTO_ALL=0
VALIDATION_CHOICE=""
STEP=0
COMPLETED=0
CURRENT_ACTION="initialisation"

usage() {
  cat <<USAGE
Usage:
  sudo ./$SCRIPT_NAME [options]

Options:
  --dry-run          Affiche et journalise les commandes sans les appliquer.
  --all              Execute toutes les etapes dans l'ordre, sans menu.
  --validation N     Lance directement une validation precise (1 a 8).
  -h, --help         Affiche cette aide.

Variables utiles:
  SOURCE_DIR       Source a sauvegarder. Defaut: $SOURCE_DIR
  BACKUP_DIR       Dossier de sauvegarde. Defaut: $BACKUP_DIR
  RESTORE_DIR      Dossier de restauration test. Defaut: $RESTORE_DIR
  RESTORE_WWW_DIR  Dossier de restauration /var/www test. Defaut: $RESTORE_WWW_DIR
  PRENOM           Prenom affiche dans index.html. Defaut: $PRENOM
  INTRANET_HOST    server_name Nginx. Defaut: $INTRANET_HOST
  CAMPUS_SUBNET    Sous-reseau autorise en SSH. Defaut: $CAMPUS_SUBNET
  DATE_TAG         Etiquette de sauvegarde. Defaut: $DATE_TAG
  LOG_DIR          Dossier des rapports. Defaut: $LOG_DIR

Exemples:
  sudo PRENOM=Oliv ./$SCRIPT_NAME
  sudo ./$SCRIPT_NAME --all
  ./$SCRIPT_NAME --dry-run --all
  sudo ./$SCRIPT_NAME --validation 4
USAGE
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=1 ;;
    --all) AUTO_ALL=1 ;;
    --validation)
      shift
      VALIDATION_CHOICE="${1:-}"
      ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Option inconnue: $1" >&2; usage; exit 2 ;;
  esac
  shift
done

if [ "$(id -u)" -ne 0 ] && [ "$DRY_RUN" -ne 1 ]; then
  echo "Lance ce script avec sudo/root, ou utilise --dry-run pour tester." >&2
  exit 1
fi

mkdir -p "$LOG_DIR"
: > "$RAW_LOG"
: > "$TIMELINE_LOG"

cat > "$REPORT" <<EOF_REPORT
# Rapport automatique - Iteration 5 AlpesNet

| Champ | Valeur |
| --- | --- |
| Date | $(date '+%Y-%m-%d %H:%M:%S') |
| Machine | $(hostname) |
| Source | $SOURCE_DIR |
| Destination rsync | $RSYNC_DEST |
| Archive configs | $CONFIG_ARCHIVE |
| Restauration test | $RESTORE_DIR |
| Hote intranet | $INTRANET_HOST |
| Utilisateur Nginx | $NGINX_USER |
| Sous-reseau SSH | $CAMPUS_SUBNET |
| Mode dry-run | $DRY_RUN |

Ce rapport liste les commandes executees par le menu, leurs resultats, les validations et l'etat final verifiable.

EOF_REPORT

finish_report_on_exit() {
  local status=$?

  if [ "$COMPLETED" -eq 1 ]; then
    return "$status"
  fi

  {
    echo
    echo "# Execution terminee ou interrompue"
    echo
    echo "| Champ | Valeur |"
    echo "| --- | --- |"
    echo "| Code retour | \`$status\` |"
    echo "| Derniere action | $CURRENT_ACTION |"
  } >> "$REPORT"
}

trap finish_report_on_exit EXIT

clean_report_output() {
  tr -d '\r' < "$1" | LC_ALL=C sed -E $'s/\x1B\\[[0-?]*[ -/]*[@-~]//g'
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
      clean_report_output "$output_file" | sed -n '1,160p'
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
  local explanation="${3:-Commande ajoutee au rapport.}"
  local allow_fail="${4:-no}"
  local report_command="${5:-$command}"
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
  append_report "$title" "$report_command" "$status" "$explanation" "$output_file"
  printf '| %02d | %s | `%s` |\n' "$STEP" "$title" "$status" >> "$TIMELINE_LOG"

  if [ "$status" -ne 0 ] && [ "$allow_fail" != "yes" ]; then
    printf '     Statut: ERREUR (code %s)\n' "$status"
    printf '     Rapport: %s\n' "$REPORT"
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

pause_menu() {
  if [ "$AUTO_ALL" -eq 0 ] && [ -z "$VALIDATION_CHOICE" ]; then
    printf '\nAppuie sur Entree pour revenir au menu...'
    read -r _
  fi
}

step_prepare() {
  section "Preparation"
  run_cmd \
    "Preparer le dossier de sauvegarde" \
    "mkdir -p '$BACKUP_DIR' && chmod 750 '$BACKUP_DIR' && ls -ld '$BACKUP_DIR'" \
    "Cree le dossier de sauvegarde avec des droits restrictifs."

  run_cmd \
    "Verifier ou creer la source AlpesNet" \
    "mkdir -p '$SOURCE_DIR/logs' '$SOURCE_DIR/projects' '$SOURCE_DIR/secrets' '$SOURCE_DIR/web'; [ -f '$SOURCE_DIR/preuve.txt' ] || printf '%s\n' 'preuve sauvegarde AlpesNet' > '$SOURCE_DIR/preuve.txt'; [ -f '$SOURCE_DIR/logs/system.log' ] || printf '%s\n' 'log test AlpesNet' > '$SOURCE_DIR/logs/system.log'; [ -f '$SOURCE_DIR/projects/projet-alpha.txt' ] || touch '$SOURCE_DIR/projects/projet-alpha.txt'; [ -f '$SOURCE_DIR/projects/projet-beta.txt' ] || touch '$SOURCE_DIR/projects/projet-beta.txt'; [ -f '$SOURCE_DIR/secrets/db.conf' ] || printf '%s\n' 'db=alpesnet' > '$SOURCE_DIR/secrets/db.conf'; find '$SOURCE_DIR' -maxdepth 2 -type f -ls" \
    "Prepare une source de test si le dossier est vide, puis liste les fichiers a sauvegarder."
}

step_rsync_backup() {
  section "Etape 1 - Sauvegarde rsync"
  run_cmd \
    "Executer la sauvegarde rsync" \
    "rsync -avz --delete '$SOURCE_DIR/' '$RSYNC_DEST/'" \
    "Synchronise la source vers un dossier date. L'option --delete garde la destination conforme a la source."

  run_cmd \
    "Verifier le contenu sauvegarde" \
    "find '$RSYNC_DEST' -maxdepth 2 -type f -ls" \
    "Prouve que les fichiers attendus existent dans la sauvegarde rsync."

  run_cmd \
    "Verifier que rsync n'a plus rien a synchroniser" \
    "tmp=\$(mktemp); rsync -avz --dry-run --checksum '$SOURCE_DIR/' '$RSYNC_DEST/' | tee \"\$tmp\"; if awk 'BEGIN {bad=0} /^sending incremental file list$/ {next} /^sent / {next} /^total size is / {next} /^$/ {next} /^\\.\/$/ {next} /\/$/ {next} {print; bad=1} END {exit bad}' \"\$tmp\"; then rm -f \"\$tmp\"; echo 'OK: aucun fichier a synchroniser'; else echo 'ERREUR: rsync liste encore des fichiers a synchroniser'; rm -f \"\$tmp\"; exit 1; fi" \
    "Relance rsync en simulation avec comparaison par checksum. Le controle ignore les dossiers et echoue seulement si un fichier est liste."
}

step_tar_restore() {
  section "Etape 2 - Archive tar et restauration"
  run_cmd \
    "Creer l'archive des configurations" \
    "tar -C / -czf '$CONFIG_ARCHIVE' etc/ssh etc/rsyslog.d && ls -lh '$CONFIG_ARCHIVE'" \
    "Archive les configurations critiques SSH et rsyslog dans un fichier compresse. L'option -C / evite les chemins absolus." \
    "no" \
    "sudo sh -c \"tar -C / -czf '$CONFIG_ARCHIVE' etc/ssh etc/rsyslog.d && ls -lh '$CONFIG_ARCHIVE'\""

  run_cmd \
    "Lister le contenu de l'archive" \
    "tar -tzf '$CONFIG_ARCHIVE' | grep -E 'etc/ssh|etc/rsyslog.d'" \
    "Controle le contenu de l'archive sans extraire les fichiers."

  run_cmd \
    "Tester la restauration dans un repertoire temporaire" \
    "rm -rf '$RESTORE_DIR'; mkdir -p '$RESTORE_DIR'; tar -xzf '$CONFIG_ARCHIVE' -C '$RESTORE_DIR'; find '$RESTORE_DIR' -maxdepth 3 -type f | sed -n '1,40p'" \
    "Extrait l'archive dans un dossier de test et montre les fichiers restaures."
}

step_checksum() {
  section "Etape 3 - Integrite SHA-256"
  run_cmd \
    "Generer et verifier le checksum" \
    "sha256sum '$CONFIG_ARCHIVE' > '$CHECKSUM_FILE'; cat '$CHECKSUM_FILE'; cd / && sha256sum -c '$CHECKSUM_FILE'" \
    "Genere une empreinte SHA-256, affiche le fichier de controle et verifie l'integrite de l'archive."
}

write_intranet_page() {
  cat <<'HTML'
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Intranet AlpesNet</title>
  <style>
    :root { color-scheme: dark; --bg:#09111f; --panel:#101b2e; --text:#eef6ff; --muted:#9fb2c8; --line:rgba(255,255,255,.14); --accent:#28d4b7; --accent2:#5aa9ff; }
    * { box-sizing: border-box; }
    body { margin:0; min-height:100vh; font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; background:#09111f; color:var(--text); }
    main { width:min(1120px, calc(100% - 32px)); margin:0 auto; padding:42px 0; }
    header { display:flex; justify-content:space-between; gap:24px; align-items:flex-start; padding-bottom:30px; border-bottom:1px solid var(--line); }
    .brand { color:var(--muted); font-weight:700; text-transform:uppercase; font-size:.82rem; }
    h1 { max-width:760px; margin:28px 0 16px; font-size:clamp(2.4rem, 6vw, 5.4rem); line-height:.95; letter-spacing:0; }
    .lead { max-width:720px; margin:0; color:var(--muted); font-size:1.08rem; line-height:1.7; }
    .status, section { border:1px solid var(--line); border-radius:8px; background:var(--panel); }
    .status { min-width:220px; padding:16px; }
    .status strong { display:block; color:var(--accent); margin-bottom:8px; }
    .grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:16px; margin-top:28px; }
    section { padding:20px; }
    h2 { margin:0 0 14px; font-size:1rem; color:var(--accent2); letter-spacing:0; }
    ul { margin:0; padding-left:18px; color:var(--muted); line-height:1.7; }
    a { color:var(--accent); font-weight:800; }
    pre { margin-top:28px; padding:18px; overflow:auto; border:1px solid var(--line); border-radius:8px; background:#050a12; color:#d7fbe8; line-height:1.55; }
    @media (max-width:820px) { header { display:block; } .status { margin-top:22px; } .grid { grid-template-columns:1fr; } }
  </style>
</head>
<body>
  <main>
    <header>
      <div>
        <div class="brand">Olidev style - AlpesNet intranet</div>
        <h1>Intranet AlpesNet</h1>
        <p class="lead">Serveur web interne deploye avec Nginx, utilisateur dedie, firewall minimal, logs separes, sauvegarde verifiee et restauration testee.</p>
        <p><a href="/rapport-it5.md">Voir le rapport</a></p>
      </div>
      <aside class="status">
        <strong>HTTP 200 attendu</strong>
        <span>intranet.alpesnet.local</span>
      </aside>
    </header>
    <div class="grid">
      <section><h2>Securite</h2><ul><li>Worker Nginx sous www-nginx</li><li>SSH restreint</li><li>Fail2ban actif</li></ul></section>
      <section><h2>Exploitation</h2><ul><li>Vhost dedie</li><li>Logs separes</li><li>Checksums SHA-256</li></ul></section>
      <section><h2>Restauration</h2><ul><li>Sauvegarde /backup/www</li><li>Test dans /tmp/restauration-www-test</li><li>Rapport publie</li></ul></section>
    </div>
    <pre>curl -v http://intranet.alpesnet.local
ps -eo user,args | grep "[n]ginx"
sudo ufw status verbose
sha256sum -c /backup/checksums.txt</pre>
  </main>
</body>
</html>
HTML
}

step_nginx_deploy() {
  section "Etape 4 - Deploiement Nginx"
  run_cmd \
    "Installer Nginx et les outils de securite" \
    "apt-get update && apt-get install -y nginx ufw fail2ban logrotate curl" \
    "Installe le serveur web et les outils requis pour firewall, bannissement SSH, rotation de logs et tests HTTP."

  run_cmd \
    "Creer l'utilisateur dedie Nginx" \
    "id '$NGINX_USER' >/dev/null 2>&1 || useradd --system --no-create-home --shell /usr/sbin/nologin '$NGINX_USER'; getent passwd '$NGINX_USER'" \
    "Cree un compte systeme dedie sans shell interactif et sans home."

  run_cmd \
    "Configurer la directive user de Nginx" \
    "cp -a /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak.$RUN_ID; if grep -q '^user ' /etc/nginx/nginx.conf; then sed -i 's/^user .*/user $NGINX_USER;/' /etc/nginx/nginx.conf; else sed -i '1i user $NGINX_USER;' /etc/nginx/nginx.conf; fi; grep '^user ' /etc/nginx/nginx.conf" \
    "Force Nginx a lancer ses workers avec l'utilisateur dedie."

  if [ "$DRY_RUN" -eq 1 ]; then
    run_cmd \
      "Creer la racine web et la page intranet" \
      "mkdir -p '$INTRANET_ROOT'; printf '%s\n' '[DRY-RUN] installation de la page index.html'; cp '$REPORT' '$PUBLIC_REPORT'; chown -R '$NGINX_USER':'$NGINX_USER' '/var/www/intranet.alpesnet.local'; chmod -R 750 '/var/www/intranet.alpesnet.local'" \
      "Dry-run : montre l'action sans ecrire la page."
  else
    mkdir -p "$INTRANET_ROOT"
    write_intranet_page > "$INTRANET_ROOT/index.html"
    cp "$REPORT" "$PUBLIC_REPORT"
    chown -R "$NGINX_USER":"$NGINX_USER" "/var/www/intranet.alpesnet.local"
    chmod -R 750 "/var/www/intranet.alpesnet.local"
    run_cmd \
      "Verifier la racine web et la page intranet" \
      "find '/var/www/intranet.alpesnet.local' -maxdepth 3 -ls" \
      "Cree une page intranet professionnelle avec rapport publie, puis verifie les droits."
  fi

  run_cmd \
    "Configurer le vhost intranet" \
    "printf '%s\n' 'server {' '    listen 80;' '    server_name $INTRANET_HOST;' '' '    root $INTRANET_ROOT;' '    index index.html;' '    etag off;' '    if_modified_since off;' '    expires off;' '    add_header Cache-Control \"no-store, no-cache, must-revalidate, max-age=0\" always;' '    add_header Pragma \"no-cache\" always;' '' '    access_log /var/log/nginx/intranet_access.log;' '    error_log /var/log/nginx/intranet_error.log warn;' '' '    location = /rapport-it5.md {' '        default_type text/plain;' '        try_files \$uri =404;' '    }' '' '    location / {' '        try_files \$uri \$uri/ =404;' '    }' '}' > /etc/nginx/sites-available/intranet; ln -sfn /etc/nginx/sites-available/intranet /etc/nginx/sites-enabled/intranet; rm -f /etc/nginx/sites-enabled/default; nginx -t" \
    "Declare le vhost, la racine web et les logs separes, puis valide la syntaxe Nginx."

  run_cmd \
    "Ajouter la resolution locale du nom intranet" \
    "grep -qE '[[:space:]]$INTRANET_HOST( |$)' /etc/hosts || printf '%s\n' '127.0.0.1 $INTRANET_HOST' >> /etc/hosts; grep '$INTRANET_HOST' /etc/hosts" \
    "Permet de tester curl directement depuis la VM sans DNS externe."

  run_cmd \
    "Demarrer et verifier Nginx" \
    "systemctl enable --now nginx; systemctl reload nginx; systemctl --no-pager --full status nginx | sed -n '1,14p'" \
    "Demarre Nginx, applique la configuration et garde une preuve de service actif."
}

step_security() {
  section "Etape 5 - Securisation serveur web"
  run_cmd \
    "Configurer UFW pour SSH restreint et HTTP ouvert" \
    "ufw default deny incoming; ufw default allow outgoing; ufw allow from '$CAMPUS_SUBNET' to any port 22 proto tcp; ufw allow 80/tcp; ufw --force enable; ufw status numbered" \
    "Applique le filtrage demande : SSH limite au sous-reseau campus et HTTP ouvert."

  run_cmd \
    "Verifier Fail2ban SSH" \
    "mkdir -p /etc/fail2ban/jail.d; printf '%s\n' '[sshd]' 'enabled = true' > /etc/fail2ban/jail.d/alpesnet-sshd.local; fail2ban-client -t && systemctl enable --now fail2ban && systemctl restart fail2ban && sleep 1 && fail2ban-client status sshd" \
    "Active et verifie la jail SSH Fail2ban."

  run_cmd \
    "Verifier les droits de /var/www" \
    "ls -la /var/www/; find /var/www/intranet.alpesnet.local -maxdepth 2 -ls" \
    "Montre que la racine intranet appartient au groupe de l'utilisateur Nginx dedie."
}

step_web_backup_restore() {
  section "Etape 6 - Sauvegarde web et restauration testee"
  run_cmd \
    "Configurer logrotate pour les logs intranet" \
    "printf '%s\n' '/var/log/nginx/intranet_access.log /var/log/nginx/intranet_error.log {' '    daily' '    rotate 7' '    compress' '    missingok' '    notifempty' '    create 0640 $NGINX_USER adm' '    sharedscripts' '    postrotate' '        [ -s /run/nginx.pid ] && kill -USR1 \$(cat /run/nginx.pid)' '    endscript' '}' > /etc/logrotate.d/nginx-intranet; logrotate -d /etc/logrotate.d/nginx-intranet" \
    "Configure une rotation quotidienne sur 7 jours avec compression pour les logs separes."

  run_cmd \
    "Sauvegarder /var/www dans /backup/www" \
    "mkdir -p '$WWW_BACKUP_DIR'; rsync -avz --delete /var/www/ '$WWW_BACKUP_DIR/'; find '$WWW_BACKUP_DIR' -maxdepth 4 -type f -ls" \
    "Sauvegarde le contenu web, dont la page intranet, dans /backup/www."

  run_cmd \
    "Generer et verifier le checksum de la sauvegarde web" \
    "find '$WWW_BACKUP_DIR' -type f -print0 | sort -z | xargs -0 sha256sum > '$BACKUP_DIR/www-checksums.txt'; cat '$BACKUP_DIR/www-checksums.txt'; cd / && sha256sum -c '$BACKUP_DIR/www-checksums.txt'" \
    "Produit et verifie les empreintes SHA-256 des fichiers sauvegardes dans /backup/www."

  run_cmd \
    "Tester la restauration de /var/www" \
    "rm -rf '$WWW_RESTORE_DIR'; mkdir -p '$WWW_RESTORE_DIR'; rsync -avz '$WWW_BACKUP_DIR/' '$WWW_RESTORE_DIR/'; find '$WWW_RESTORE_DIR' -maxdepth 4 -type f | sed -n '1,40p'" \
    "Restaure la sauvegarde web dans un repertoire de test et montre les fichiers restaures."
}

step_audit_compromised() {
  section "Etape 7 - Audit systeme compromis"
  run_cmd \
    "Identifier les comptes UID 0" \
    "awk -F: '(\$3==0) {print}' /etc/passwd" \
    "Liste les comptes avec UID 0. En situation normale, seul root doit apparaitre."

  run_cmd \
    "Identifier les permissions dangereuses 777" \
    "find / -xdev -type d -perm -0002 -ls 2>/dev/null | sed -n '1,80p'" \
    "Recherche les repertoires modifiables par tous sur le systeme local."

  run_cmd \
    "Identifier les fichiers SUID" \
    "find / -xdev -perm /4000 -type f -ls 2>/dev/null | sed -n '1,80p'" \
    "Recherche les binaires SUID a controler sur une VM CTF ou un systeme compromis."
}

step_full_hardening_validation() {
  section "Etape 8 - Verification durcissement Linux complet"
  run_cmd \
    "Verifier le refus SSH root" \
    "sshd -T 2>/dev/null | grep -E '^permitrootlogin|^passwordauthentication' || grep -E 'PermitRootLogin|PasswordAuthentication' /etc/ssh/sshd_config" \
    "Montre les parametres SSH utiles pour prouver le durcissement."

  run_cmd \
    "Verifier UFW et Fail2ban" \
    "ufw status verbose; fail2ban-client status sshd" \
    "Montre que le pare-feu et la jail SSH sont actifs."

  run_cmd \
    "Lister les services actifs a surveiller" \
    "systemctl --type=service --state=running --no-pager | sed -n '1,80p'" \
    "Aide a justifier les services conserves et ceux a desactiver si inutiles."
}

write_final_summary() {
  {
    echo "# Lecture rapide pour jury"
    echo
    echo "## Timeline d'execution"
    echo
    echo "| Etape | Action | Code retour |"
    echo "| --- | --- | --- |"
    cat "$TIMELINE_LOG"
    echo
    echo "## Causes et risques traites"
    echo
    echo "| Cause ou risque initial | Effet possible | Reponse appliquee |"
    echo "| --- | --- | --- |"
    echo "| Sauvegarde non testee | Impossible de prouver une reprise apres incident | Sauvegarde rsync, archive tar, restauration dans /tmp et checksum |"
    echo "| Integrite non controlee | Archive modifiee ou corrompue non detectee | Empreintes SHA-256 et verification avec sha256sum -c |"
    echo "| Serveur web trop generique | Confusion avec le site par defaut ou logs melanges | Vhost intranet dedie, site default desactive, logs separes |"
    echo "| Processus web trop privilegie | Impact plus fort en cas de compromission | Worker Nginx execute sous $NGINX_USER |"
    echo "| Exposition SSH trop large | Surface d'attaque plus grande | UFW avec SSH restreint au sous-reseau $CAMPUS_SUBNET |"
    echo "| Tentatives SSH repetees | Risque de force brute | Fail2ban actif sur la jail sshd |"
    echo
    echo "## Etat final verifiable"
    echo
    echo "| Controle | Commande | Etat attendu |"
    echo "| --- | --- | --- |"
    echo "| Sauvegarde rsync | \`rsync -avz --dry-run --checksum '$SOURCE_DIR/' '$RSYNC_DEST/'\` | aucune synchronisation necessaire |"
    echo "| Archive | \`tar -tzf '$CONFIG_ARCHIVE'\` | contenu listable |"
    echo "| Checksum | \`sha256sum -c '$CHECKSUM_FILE'\` | \`OK\` |"
    echo "| Intranet HTTP | \`curl -v http://$INTRANET_HOST\` | \`HTTP/1.1 200 OK\` |"
    echo "| Worker dedie | \`ps aux | grep nginx\` | \`$NGINX_USER\` visible |"
    echo "| Pare-feu | \`ufw status verbose\` | SSH restreint, HTTP 80 ouvert |"
    echo "| Fail2ban | \`fail2ban-client status sshd\` | jail sshd active |"
    echo
    echo "## Procedure de restauration /var/www"
    echo
    echo "Si /var/www est perdu :"
    echo
    echo "1. Verifier la sauvegarde avec \`sha256sum -c '$BACKUP_DIR/www-checksums.txt'\`."
    echo "2. Restaurer dans un repertoire de test avec \`rsync -avz '$WWW_BACKUP_DIR/' '$WWW_RESTORE_DIR/'\`."
    echo "3. Controler les fichiers restaures avec \`find '$WWW_RESTORE_DIR' -maxdepth 4 -type f\`."
    echo "4. Restaurer en production seulement apres verification."
    echo
    echo "# Synthese finale"
    echo
    echo "- Rapport Markdown : \`$REPORT\`"
    echo "- Log brut : \`$RAW_LOG\`"
    echo "- Sauvegarde rsync : \`$RSYNC_DEST\`"
    echo "- Archive configs : \`$CONFIG_ARCHIVE\`"
    echo "- Checksum : \`$CHECKSUM_FILE\`"
    echo "- Restauration testee : \`$RESTORE_DIR\`"
    echo "- Vhost Nginx : \`$INTRANET_HOST\`"
    echo "- Racine intranet : \`$INTRANET_ROOT\`"
    echo "- Sauvegarde web : \`$WWW_BACKUP_DIR\`"
    echo "- Restauration web testee : \`$WWW_RESTORE_DIR\`"
  } >> "$REPORT"

  if [ "$DRY_RUN" -ne 1 ] && [ -d "$INTRANET_ROOT" ]; then
    cp "$REPORT" "$PUBLIC_REPORT"
    chown root:"$NGINX_USER" "$PUBLIC_REPORT"
    chmod 640 "$PUBLIC_REPORT"
  fi
}

validation_header() {
  local title="$1"
  local criteria="$2"
  local proof="$3"

  section "Validation - $title"
  {
    echo "**Criteres** : $criteria"
    echo
    echo "**Preuve de travail** : $proof"
    echo
  } >> "$REPORT"
  printf '\n--- Validation : %s ---\n' "$title"
  printf 'Criteres: %s\n' "$criteria"
  printf 'Preuve: %s\n' "$proof"
}

validation_rsync_checksum() {
  validation_header \
    "Sauvegarder avec rsync et verifier avec --checksum" \
    "La sauvegarde est creee et --dry-run --checksum ne retourne aucun fichier a synchroniser." \
    "Je lance d'abord la sauvegarde rsync, puis rsync -avz --dry-run --checksum et je montre qu'aucun fichier n'est liste."
  run_cmd \
    "Validation creer la sauvegarde rsync" \
    "rsync -avz --delete '$SOURCE_DIR/' '$RSYNC_DEST/'" \
    "Cree ou met a jour la sauvegarde avant le controle. Sans cette etape, le dry-run simule logiquement la creation de toute la destination."

  run_cmd \
    "Validation rsync dry-run checksum sans ecart" \
    "tmp=\$(mktemp); rsync -avz --dry-run --checksum '$SOURCE_DIR/' '$RSYNC_DEST/' | tee \"\$tmp\"; if awk 'BEGIN {bad=0} /^sending incremental file list$/ {next} /^sent / {next} /^total size is / {next} /^$/ {next} /^\\.\/$/ {next} /\/$/ {next} {print; bad=1} END {exit bad}' \"\$tmp\"; then rm -f \"\$tmp\"; echo 'OK: aucun fichier a synchroniser'; else echo 'ERREUR: rsync liste encore des fichiers a synchroniser'; rm -f \"\$tmp\"; exit 1; fi" \
    "Compare source et destination sans modification. Le controle ignore les dossiers et echoue si rsync liste un fichier a transferer ; la preuve attendue finit par OK: aucun fichier a synchroniser."
}

validation_tar_restore() {
  validation_header \
    "Creer une archive tar et tester la restauration" \
    "L'archive est creee, listable et le contenu est restaurable dans un repertoire de test." \
    "Je cree l'archive, je liste le contenu avec tar -tzf, puis j'extrais dans /tmp/restauration-test/ et je montre les fichiers restaures."
  run_cmd \
    "Validation creer l'archive tar" \
    "mkdir -p '$BACKUP_DIR'; tar -C / -czf '$CONFIG_ARCHIVE' etc/ssh etc/rsyslog.d; ls -lh '$CONFIG_ARCHIVE'" \
    "Cree l'archive tar.gz des configurations SSH et rsyslog, puis affiche le fichier cree."

  run_cmd \
    "Validation lister le contenu avec tar -tzf" \
    "tar -tzf '$CONFIG_ARCHIVE' | sed -n '1,80p'" \
    "Liste le contenu de l'archive sans extraire les fichiers."

  run_cmd \
    "Validation extraire et afficher les fichiers restaures" \
    "rm -rf '$RESTORE_DIR'; mkdir -p '$RESTORE_DIR'; tar -xzf '$CONFIG_ARCHIVE' -C '$RESTORE_DIR'; find '$RESTORE_DIR' -maxdepth 3 -type f | sed -n '1,80p'" \
    "Extrait l'archive dans /tmp/restauration-test et montre les fichiers restaures."
}

validation_sha256() {
  validation_header \
    "Verifier l'integrite d'une sauvegarde avec sha256sum" \
    "Le checksum est produit et sha256sum -c retourne OK." \
    "Je montre cat /backup/checksums.txt puis sha256sum -c /backup/checksums.txt affichant OK."
  run_cmd \
    "Validation checksum SHA-256" \
    "cat '$CHECKSUM_FILE'; cd / && sha256sum -c '$CHECKSUM_FILE'" \
    "Affiche le fichier de checksum puis controle l'integrite."
}

validation_nginx_deploy() {
  validation_header \
    "Deployer Nginx avec vhost, utilisateur dedie et logs separes" \
    "Nginx actif, worker sous www-nginx, vhost intranet.alpesnet.local repondant HTTP 200, logs access et error separes." \
    "Je montre curl -v, ps aux | grep nginx et ls -la /var/log/nginx/."
  run_cmd \
    "Validation Nginx vhost worker logs" \
    "curl -v 'http://$INTRANET_HOST'; ps aux | grep '[n]ginx'; ls -la /var/log/nginx/ | grep -E 'intranet_access|intranet_error'" \
    "Controle la reponse HTTP, l'utilisateur worker et les logs separes."
}

validation_web_security() {
  validation_header \
    "Securiser le serveur web selon le principe du moindre privilege" \
    "ufw autorise uniquement 22 restreint et 80, fail2ban actif, /var/www/intranet appartient a www-nginx." \
    "Je montre sudo ufw status verbose, sudo fail2ban-client status sshd et ls -la /var/www/."
  run_cmd \
    "Validation moindre privilege serveur web" \
    "ufw status verbose; fail2ban-client status sshd; ls -la /var/www/; find /var/www/intranet.alpesnet.local -maxdepth 2 -ls" \
    "Montre le pare-feu, Fail2ban et les droits de la racine web."
}

validation_report_restore() {
  validation_header \
    "Produire un rapport de deploiement avec procedure de restauration testee" \
    "Le rapport documente chaque choix securite et la procedure de restauration depuis la sauvegarde a ete testee." \
    "Je montre le rapport et j'explique : Si /var/www est perdu, voici les etapes pour le restaurer depuis /backup/www."
  write_final_summary
  run_cmd \
    "Validation rapport et restauration /var/www" \
    "sed -n '1,220p' '$REPORT'; rm -rf '$WWW_RESTORE_DIR'; mkdir -p '$WWW_RESTORE_DIR'; rsync -avz '$WWW_BACKUP_DIR/' '$WWW_RESTORE_DIR/'; find '$WWW_RESTORE_DIR' -maxdepth 4 -type f | sed -n '1,40p'" \
    "Affiche le rapport puis reteste la restauration de /var/www depuis /backup/www."
}

validation_compromised_accounts() {
  validation_header \
    "Identifier comptes non autorises et permissions dangereuses" \
    "Le compte intrus et les permissions dangereuses 777 ou SUID sont identifies avec les commandes correctes." \
    "J'explique awk -F: '(\$3==0)' pour les UID 0 et find / -perm /4000 pour les SUID. Je montre le resultat sur la VM CTF."
  run_cmd \
    "Validation audit comptes et permissions dangereuses" \
    "printf '%s\n' 'UID 0:'; awk -F: '(\$3==0) {print}' /etc/passwd; printf '%s\n' 'SUID:'; find / -xdev -perm /4000 -type f -ls 2>/dev/null | sed -n '1,80p'; printf '%s\n' 'Permissions 777:'; find / -xdev -perm -0002 -ls 2>/dev/null | sed -n '1,80p'" \
    "Montre les UID 0, les fichiers SUID et les permissions modifiables par tous."
}

validation_full_hardening() {
  validation_header \
    "Appliquer le durcissement complet d'un systeme Linux" \
    "SSH durci, ufw actif, fail2ban actif, services inutiles desactives, verifiable par commandes." \
    "Je montre ssh root@[IP] refuse, sudo ufw status verbose, sudo fail2ban-client status sshd et j'explique chaque mesure."
  run_cmd \
    "Validation durcissement Linux complet" \
    "sshd -T 2>/dev/null | grep -E '^permitrootlogin|^passwordauthentication' || true; ufw status verbose; fail2ban-client status sshd; systemctl --type=service --state=running --no-pager | sed -n '1,80p'" \
    "Montre les controles SSH, pare-feu, Fail2ban et les services actifs."
}

show_validation_report_block() {
  local start_line="$1"

  printf '\n=== Bloc ajoute au rapport Markdown ===\n'
  tail -n +"$start_line" "$REPORT"
  printf '=== Fin du bloc Markdown ===\n'
}

run_validation_choice() {
  local report_start_line

  report_start_line=$(( $(wc -l < "$REPORT") + 1 ))

  case "$1" in
    1) validation_rsync_checksum ;;
    2) validation_tar_restore ;;
    3) validation_sha256 ;;
    4) validation_nginx_deploy ;;
    5) validation_web_security ;;
    6) validation_report_restore ;;
    7) validation_compromised_accounts ;;
    8) validation_full_hardening ;;
    *) echo "Choix validation invalide: $1" >&2; return 1 ;;
  esac

  show_validation_report_block "$report_start_line"
}

validation_menu() {
  local choice

  while true; do
    cat <<MENU

=== Sous-menu Validation ===
1) Sauvegarder avec rsync et verifier avec --checksum
2) Creer une archive tar et tester la restauration
3) Verifier l'integrite avec sha256sum
4) Deployer Nginx avec vhost, utilisateur dedie et logs separes
5) Securiser le serveur web selon le moindre privilege
6) Produire le rapport avec procedure de restauration testee
7) Identifier comptes non autorises et permissions dangereuses
8) Appliquer le durcissement complet d'un systeme Linux
0) Retour
MENU
    printf 'Choix validation: '
    read -r choice
    case "$choice" in
      0) return 0 ;;
      [1-8]) run_validation_choice "$choice"; pause_menu ;;
      *) echo "Choix invalide." ;;
    esac
  done
}

run_all_steps() {
  AUTO_ALL=1
  step_prepare
  step_rsync_backup
  step_tar_restore
  step_checksum
  step_nginx_deploy
  step_security
  step_web_backup_restore
  step_audit_compromised
  step_full_hardening_validation
  write_final_summary
}

main_menu() {
  local choice

  while true; do
    cat <<MENU

=== Menu AlpesNet IT5 ===
1) Preparation des dossiers et donnees de test
2) Sauvegarde rsync
3) Archive tar et restauration test
4) Checksum SHA-256
5) Deploiement Nginx intranet
6) Securisation web (UFW, Fail2ban, droits)
7) Sauvegarde /var/www et restauration test
8) Audit systeme compromis
9) Verification durcissement Linux complet
10) Sous-menu Validation
11) Tout executer dans l'ordre
12) Finaliser le rapport
0) Quitter
MENU
    printf 'Choix: '
    read -r choice
    case "$choice" in
      1) step_prepare; pause_menu ;;
      2) step_rsync_backup; pause_menu ;;
      3) step_tar_restore; pause_menu ;;
      4) step_checksum; pause_menu ;;
      5) step_nginx_deploy; pause_menu ;;
      6) step_security; pause_menu ;;
      7) step_web_backup_restore; pause_menu ;;
      8) step_audit_compromised; pause_menu ;;
      9) step_full_hardening_validation; pause_menu ;;
      10) validation_menu ;;
      11) run_all_steps; pause_menu ;;
      12) write_final_summary; echo "Rapport finalise: $REPORT"; pause_menu ;;
      0) return 0 ;;
      *) echo "Choix invalide." ;;
    esac
  done
}

if [ -n "$VALIDATION_CHOICE" ]; then
  run_validation_choice "$VALIDATION_CHOICE"
elif [ "$AUTO_ALL" -eq 1 ]; then
  run_all_steps
else
  main_menu
fi

COMPLETED=1

echo
echo "Termine."
echo "Rapport: $REPORT"
echo "Log brut: $RAW_LOG"
