#!/usr/bin/env bash
set -u
set -o pipefail

# AlpesNet - Iteration 5 evolving automation script
# Current scope: backup, integrity check, tested restoration and secure Nginx
# intranet deployment for Autonomie 3.

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
STEP=0
COMPLETED=0
CURRENT_ACTION="initialisation"

usage() {
  cat <<USAGE
Usage:
  sudo ./$SCRIPT_NAME [options]

Options:
  --dry-run      Show and log commands without applying changes.
  -h, --help     Show this help.

Useful environment variables:
  SOURCE_DIR       Source data directory. Default: $SOURCE_DIR
  BACKUP_DIR       Backup directory. Default: $BACKUP_DIR
  RESTORE_DIR      Test restoration directory. Default: $RESTORE_DIR
  RESTORE_WWW_DIR  Test /var/www restoration directory. Default: $RESTORE_WWW_DIR
  PRENOM           First name displayed on index.html. Default: $PRENOM
  INTRANET_HOST    Nginx server_name. Default: $INTRANET_HOST
  CAMPUS_SUBNET    Subnet allowed to SSH. Default: $CAMPUS_SUBNET
  DATE_TAG         Backup date tag. Default: $DATE_TAG
  LOG_DIR          Report directory. Default: $LOG_DIR

Example:
  sudo PRENOM=Oliv CAMPUS_SUBNET=192.168.56.0/24 ./$SCRIPT_NAME
USAGE
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=1 ;;
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

Ce rapport liste les commandes executees par le script, leur resultat, leur explication, la timeline, les causes/risques traites, les actions correctives et l'etat final verifiable.

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
  } >> "$REPORT"
}

trap finish_report_on_exit EXIT

clean_report_output() {
  tr -d '\r' < "$1" | sed -E $'s/\x1B\\[[0-?]*[ -/]*[@-~]//g'
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
  local explanation="${3:-Commande de demonstration ajoutee au rapport.}"
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

section "Preparation"

run_cmd \
  "bois un café" \
  "curl -fsSL git.io/coffee || printf '%s\n' '    ( (' '     ) )' '  ........' '  |      |]' '  \      /' '   ------'" \
  "Tu l'as bien mérité" \
  "no" \
  "curl -fsSL git.io/coffee"

run_cmd \
  "Preparer le dossier de sauvegarde" \
  "mkdir -p '$BACKUP_DIR' && chmod 750 '$BACKUP_DIR' && ls -ld '$BACKUP_DIR'" \
  "Cree le dossier de sauvegarde avec des droits restrictifs."

run_cmd \
  "Verifier ou creer la source AlpesNet" \
  "mkdir -p '$SOURCE_DIR/logs' '$SOURCE_DIR/projects' '$SOURCE_DIR/secrets' '$SOURCE_DIR/web'; [ -f '$SOURCE_DIR/preuve.txt' ] || printf '%s\\n' 'preuve sauvegarde AlpesNet' > '$SOURCE_DIR/preuve.txt'; [ -f '$SOURCE_DIR/logs/system.log' ] || printf '%s\\n' 'log test AlpesNet' > '$SOURCE_DIR/logs/system.log'; [ -f '$SOURCE_DIR/projects/projet-alpha.txt' ] || touch '$SOURCE_DIR/projects/projet-alpha.txt'; [ -f '$SOURCE_DIR/projects/projet-beta.txt' ] || touch '$SOURCE_DIR/projects/projet-beta.txt'; [ -f '$SOURCE_DIR/secrets/db.conf' ] || printf '%s\\n' 'db=alpesnet' > '$SOURCE_DIR/secrets/db.conf'; find '$SOURCE_DIR' -maxdepth 2 -type f -ls" \
  "Prepare une source de test si le dossier /srv/alpesnet est vide, puis liste les fichiers a sauvegarder."

section "Exercice 1 - Sauvegarde rsync"

run_cmd \
  "Executer la sauvegarde rsync" \
  "rsync -avz --delete '$SOURCE_DIR/' '$RSYNC_DEST/'" \
  "Synchronise la source vers un dossier date. L'option --delete garde la destination conforme a la source."

run_cmd \
  "Verifier le contenu sauvegarde" \
  "find '$RSYNC_DEST' -maxdepth 2 -type f -ls" \
  "Prouve que les fichiers attendus existent dans la sauvegarde rsync."

run_cmd \
  "Verifier rsync en dry-run checksum" \
  "rsync -avz --dry-run --checksum '$SOURCE_DIR/' '$RSYNC_DEST/'" \
  "Compare le contenu source/destination sans modifier les fichiers. Une absence d'ecart significatif valide la synchronisation."

section "Exercice 1 - Archive tar et restauration"

run_cmd \
  "Creer l'archive des configurations" \
  "tar -czf '$CONFIG_ARCHIVE' /etc/ssh /etc/rsyslog.d && ls -lh '$CONFIG_ARCHIVE'" \
  "Archive les configurations critiques SSH et rsyslog dans un fichier compresse."

run_cmd \
  "Lister le contenu de l'archive" \
  "tar -tzf '$CONFIG_ARCHIVE' | grep -E 'etc/ssh|etc/rsyslog.d'" \
  "Controle le contenu de l'archive sans extraire les fichiers."

run_cmd \
  "Tester la restauration dans un repertoire temporaire" \
  "rm -rf '$RESTORE_DIR'; mkdir -p '$RESTORE_DIR'; tar -xzf '$CONFIG_ARCHIVE' -C '$RESTORE_DIR'; ls '$RESTORE_DIR/etc/ssh'; ls '$RESTORE_DIR/etc/rsyslog.d'; sed -n '1,20p' '$RESTORE_DIR/etc/ssh/sshd_config'" \
  "Extrait l'archive dans un dossier de test et verifie que les fichiers restaures sont lisibles."

run_cmd \
  "Generer et verifier le checksum" \
  "sha256sum '$CONFIG_ARCHIVE' > '$CHECKSUM_FILE'; cd / && sha256sum -c '$CHECKSUM_FILE'" \
  "Genere une empreinte SHA-256 et verifie l'integrite de l'archive."

section "Procedure de restauration"

run_cmd \
  "Generer la procedure de restauration SSH" \
  "printf '%s\\n' 'Procedure de restauration /etc/ssh' '1. Identifier la derniere archive valide dans /backup.' '2. Verifier son integrite avec sha256sum -c /backup/checksums.txt.' '3. Extraire l archive dans /tmp/restauration-test.' '4. Comparer les fichiers restaures avec les fichiers actuels.' '5. Copier uniquement les fichiers necessaires vers /etc/ssh.' '6. Verifier la syntaxe avec sudo sshd -t.' '7. Recharger SSH avec sudo systemctl reload sshd.' '8. Tester une nouvelle connexion avant de fermer la session active.' > '$BACKUP_DIR/procedure-restauration-ssh-$DATE_TAG.txt'; cat '$BACKUP_DIR/procedure-restauration-ssh-$DATE_TAG.txt'" \
  "Produit une procedure courte a conserver dans le carnet de bord."

section "Autonomie 3 - Deploiement Nginx securise"

run_cmd \
  "Installer Nginx et les outils de securite" \
  "apt-get update && apt-get install -y nginx ufw fail2ban logrotate curl" \
  "Installe le serveur web et les outils requis pour firewall, bannissement SSH, rotation de logs et tests HTTP."

run_cmd \
  "Creer l'utilisateur dedie Nginx" \
  "id '$NGINX_USER' >/dev/null 2>&1 || useradd --system --no-create-home --shell /usr/sbin/nologin '$NGINX_USER'; getent passwd '$NGINX_USER'" \
  "Cree un compte systeme dedie sans shell interactif et sans home. Le worker Nginx tournera sous ce compte."

run_cmd \
  "Configurer la directive user de Nginx" \
  "cp -a /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak.$RUN_ID; if grep -q '^user ' /etc/nginx/nginx.conf; then sed -i 's/^user .*/user $NGINX_USER;/' /etc/nginx/nginx.conf; else sed -i '1i user $NGINX_USER;' /etc/nginx/nginx.conf; fi; grep '^user ' /etc/nginx/nginx.conf" \
  "Force Nginx a lancer ses workers avec l'utilisateur dedie www-nginx au lieu de www-data."

run_cmd \
  "Creer la racine web et la page intranet" \
  "mkdir -p '$INTRANET_ROOT'; cat > '$INTRANET_ROOT/index.html' <<HTML
<!doctype html>
<html lang=\"fr\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Intranet AlpesNet - $PRENOM</title>
  <style>
    :root {
      color-scheme: dark;
      --bg: #09111f;
      --panel: #101b2e;
      --panel-2: #142238;
      --text: #eef6ff;
      --muted: #9fb2c8;
      --line: rgba(255,255,255,.12);
      --accent: #28d4b7;
      --accent-2: #5aa9ff;
      --warn: #ffd166;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif;
      background:
        radial-gradient(circle at 15% 15%, rgba(40,212,183,.18), transparent 30%),
        radial-gradient(circle at 85% 8%, rgba(90,169,255,.18), transparent 28%),
        linear-gradient(135deg, #07101d 0%, var(--bg) 48%, #0f1a2d 100%);
      color: var(--text);
    }
    main {
      width: min(1120px, calc(100% - 32px));
      margin: 0 auto;
      padding: 42px 0;
    }
    header {
      display: flex;
      justify-content: space-between;
      gap: 24px;
      align-items: flex-start;
      padding-bottom: 30px;
      border-bottom: 1px solid var(--line);
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 14px;
      color: var(--muted);
      font-weight: 700;
      letter-spacing: .08em;
      text-transform: uppercase;
      font-size: .82rem;
    }
    .mark {
      width: 42px;
      height: 42px;
      display: grid;
      place-items: center;
      border: 1px solid rgba(40,212,183,.5);
      border-radius: 12px;
      background: rgba(40,212,183,.1);
      color: var(--accent);
      font-weight: 900;
      letter-spacing: 0;
    }
    h1 {
      max-width: 760px;
      margin: 28px 0 16px;
      font-size: clamp(2.4rem, 6vw, 5.4rem);
      line-height: .95;
      letter-spacing: 0;
    }
    .lead {
      max-width: 720px;
      margin: 0;
      color: var(--muted);
      font-size: clamp(1rem, 2vw, 1.18rem);
      line-height: 1.7;
    }
    .actions {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 22px;
    }
    .button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 44px;
      padding: 0 16px;
      border: 1px solid rgba(40,212,183,.62);
      border-radius: 8px;
      background: rgba(40,212,183,.14);
      color: var(--text);
      font-weight: 800;
      text-decoration: none;
    }
    .button:hover,
    .button:focus-visible {
      background: rgba(40,212,183,.24);
      outline: none;
    }
    .status {
      min-width: 220px;
      padding: 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(16,27,46,.78);
    }
    .status strong {
      display: block;
      margin-bottom: 8px;
      color: var(--accent);
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
      margin-top: 28px;
    }
    section {
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(16,27,46,.82);
      padding: 20px;
    }
    section h2 {
      margin: 0 0 14px;
      font-size: 1rem;
      color: var(--accent-2);
      letter-spacing: 0;
    }
    dl, ul { margin: 0; }
    dl { display: grid; gap: 12px; }
    dt { color: var(--muted); font-size: .84rem; }
    dd { margin: 3px 0 0; font-weight: 700; }
    ul {
      padding-left: 18px;
      color: var(--muted);
      line-height: 1.7;
    }
    .wide { grid-column: span 2; }
    .terminal {
      margin-top: 28px;
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
      background: #050a12;
    }
    .terminal-bar {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 12px 14px;
      background: var(--panel-2);
      color: var(--muted);
      font-size: .82rem;
    }
    .dot { width: 10px; height: 10px; border-radius: 50%; background: var(--accent); }
    pre {
      margin: 0;
      padding: 18px;
      overflow: auto;
      color: #d7fbe8;
      font-size: .92rem;
      line-height: 1.55;
    }
    footer {
      margin-top: 24px;
      color: var(--muted);
      font-size: .9rem;
    }
    @media (max-width: 820px) {
      header { display: block; }
      .status { margin-top: 22px; }
      .grid { grid-template-columns: 1fr; }
      .wide { grid-column: auto; }
    }
  </style>
</head>
<body>
  <main>
    <header>
      <div>
        <div class=\"brand\"><span class=\"mark\">OD</span><span>Olidev style - AlpesNet intranet</span></div>
        <h1>Intranet AlpesNet</h1>
        <p class=\"lead\">Serveur web interne deploye avec Nginx, utilisateur dedie, firewall minimal, logs separes, sauvegarde verifiee et restauration testee.</p>
        <div class=\"actions\">
          <a class=\"button\" href=\"/rapport-it5.md\">Voir le rapport</a>
        </div>
      </div>
      <aside class=\"status\">
        <strong>HTTP 200 attendu</strong>
        <span>Cache navigateur desactive</span>
        <span>$INTRANET_HOST</span>
      </aside>
    </header>

    <div class=\"grid\">
      <section>
        <h2>Identite</h2>
        <dl>
          <div><dt>Prenom</dt><dd>$PRENOM</dd></div>
          <div><dt>Date</dt><dd>$(date +%Y-%m-%d)</dd></div>
          <div><dt>Serveur</dt><dd>$(hostname)</dd></div>
        </dl>
      </section>

      <section>
        <h2>Securite</h2>
        <ul>
          <li>Worker Nginx sous $NGINX_USER</li>
          <li>SSH restreint au campus</li>
          <li>Fail2ban actif sur sshd</li>
          <li>Port 80 ouvert pour l'intranet</li>
        </ul>
      </section>

      <section>
        <h2>Exploitation</h2>
        <ul>
          <li>Vhost dedie</li>
          <li>Logs separes</li>
          <li>Rotation 7 jours compressee</li>
          <li>Checksum SHA-256</li>
        </ul>
      </section>

      <section class=\"wide\">
        <h2>Livrables RNCP</h2>
        <ul>
          <li>Configuration Nginx annotee dans /etc/nginx/sites-available/intranet</li>
          <li>Sauvegarde de /var/www dans /backup/www</li>
          <li>Restauration testee dans /tmp/restauration-www-test</li>
          <li>Rapport automatique publie sur /rapport-it5.md</li>
        </ul>
      </section>

      <section>
        <h2>Validation</h2>
        <dl>
          <div><dt>Commande</dt><dd>curl -v http://$INTRANET_HOST</dd></div>
          <div><dt>Resultat</dt><dd>Page servie par Nginx</dd></div>
        </dl>
      </section>
    </div>

    <div class=\"terminal\">
      <div class=\"terminal-bar\"><span class=\"dot\"></span><span>controle-alpesnet.sh</span></div>
      <pre>nginx -t
ps -eo user,args | grep \"[n]ginx\"
sudo ufw status verbose
sha256sum -c /backup/www-checksums.txt</pre>
    </div>

    <footer>AlpesNet - deploiement automatise par $PRENOM - $(date +%Y-%m-%d)</footer>
  </main>
</body>
</html>
HTML
cp '$REPORT' '$PUBLIC_REPORT'; chown -R root:'$NGINX_USER' '/var/www/intranet.alpesnet.local'; chmod -R 750 '/var/www/intranet.alpesnet.local'; find '/var/www/intranet.alpesnet.local' -maxdepth 3 -ls" \
  "Cree une page intranet plus professionnelle, inspiree d'une page portfolio/dev sobre, avec prenom, date, nom du serveur, statut, securite, livrables, bouton de consultation du rapport et commandes de verification."

run_cmd \
  "Configurer le vhost intranet" \
  "printf '%s\\n' 'server {' '    listen 80;' '    server_name $INTRANET_HOST;' '' '    root $INTRANET_ROOT;' '    index index.html;' '    etag off;' '    if_modified_since off;' '    expires off;' '    add_header Cache-Control \"no-store, no-cache, must-revalidate, max-age=0\" always;' '    add_header Pragma \"no-cache\" always;' '' '    access_log /var/log/nginx/intranet_access.log;' '    error_log /var/log/nginx/intranet_error.log warn;' '' '    location = /rapport-it5.md {' '        default_type text/plain;' '        try_files \$uri =404;' '    }' '' '    location / {' '        try_files \$uri \$uri/ =404;' '    }' '}' > /etc/nginx/sites-available/intranet; ln -sfn /etc/nginx/sites-available/intranet /etc/nginx/sites-enabled/intranet; rm -f /etc/nginx/sites-enabled/default; nginx -t" \
  "Declare le vhost intranet.alpesnet.local, la racine web, les logs separes, l'affichage texte du rapport Markdown, desactive le cache navigateur pour eviter les 304 et desactive le site par defaut."

run_cmd \
  "Ajouter la resolution locale du nom intranet" \
  "grep -qE '[[:space:]]$INTRANET_HOST( |$)' /etc/hosts || printf '%s\\n' '127.0.0.1 $INTRANET_HOST' >> /etc/hosts; grep '$INTRANET_HOST' /etc/hosts" \
  "Permet de tester curl http://intranet.alpesnet.local directement depuis la VM sans DNS externe."

run_cmd \
  "Demarrer et verifier Nginx" \
  "systemctl enable --now nginx; systemctl reload nginx; systemctl --no-pager --full status nginx | sed -n '1,14p'" \
  "Demarre Nginx, applique la configuration et garde une preuve de service actif."

section "Autonomie 3 - Firewall et Fail2ban"

run_cmd \
  "Configurer UFW pour SSH restreint et HTTP ouvert" \
  "ufw default deny incoming; ufw default allow outgoing; ufw allow from '$CAMPUS_SUBNET' to any port 22 proto tcp; ufw allow 80/tcp; ufw --force enable; ufw status numbered" \
  "Applique le filtrage demande : SSH limite au sous-reseau campus et HTTP ouvert pour l'intranet."

run_cmd \
  "Verifier Fail2ban SSH" \
  "mkdir -p /etc/fail2ban/jail.d; printf '%s\\n' '[sshd]' 'enabled = true' > /etc/fail2ban/jail.d/alpesnet-sshd.local; fail2ban-client -t && systemctl enable --now fail2ban && systemctl restart fail2ban && sleep 1 && fail2ban-client status sshd" \
  "Active et verifie la jail SSH Fail2ban pour proteger le serveur contre les tentatives de force brute."

section "Autonomie 3 - Rotation et sauvegarde web"

run_cmd \
  "Configurer logrotate pour les logs intranet" \
  "printf '%s\\n' '/var/log/nginx/intranet_access.log /var/log/nginx/intranet_error.log {' '    daily' '    rotate 7' '    compress' '    missingok' '    notifempty' '    create 0640 $NGINX_USER adm' '    sharedscripts' '    postrotate' '        [ -s /run/nginx.pid ] && kill -USR1 \$(cat /run/nginx.pid)' '    endscript' '}' > /etc/logrotate.d/nginx-intranet; logrotate -d /etc/logrotate.d/nginx-intranet" \
  "Configure une rotation quotidienne sur 7 jours avec compression pour les logs separes du vhost."

run_cmd \
  "Sauvegarder /var/www dans /backup/www" \
  "mkdir -p '$WWW_BACKUP_DIR'; rsync -avz --delete /var/www/ '$WWW_BACKUP_DIR/'; find '$WWW_BACKUP_DIR' -maxdepth 4 -type f -ls" \
  "Sauvegarde le contenu web, dont la page intranet, dans /backup/www."

run_cmd \
  "Generer et verifier le checksum de la sauvegarde web" \
  "find '$WWW_BACKUP_DIR' -type f -print0 | sort -z | xargs -0 sha256sum > '$BACKUP_DIR/www-checksums.txt'; cd / && sha256sum -c '$BACKUP_DIR/www-checksums.txt'" \
  "Produit et verifie les empreintes SHA-256 des fichiers sauvegardes dans /backup/www."

run_cmd \
  "Tester la restauration de /var/www" \
  "rm -rf '$WWW_RESTORE_DIR'; mkdir -p '$WWW_RESTORE_DIR'; rsync -avz '$WWW_BACKUP_DIR/' '$WWW_RESTORE_DIR/'; test -f '$WWW_RESTORE_DIR/intranet.alpesnet.local/html/index.html'; sed -n '1,20p' '$WWW_RESTORE_DIR/intranet.alpesnet.local/html/index.html'" \
  "Restaure la sauvegarde web dans un repertoire de test et verifie que index.html est lisible."

section "Autonomie 3 - Criteres de reussite"

run_cmd \
  "Verifier HTTP 200" \
  "code=\$(curl -s -H 'Cache-Control: no-cache' -o /tmp/intranet-curl-body.txt -w '%{http_code}' 'http://$INTRANET_HOST'); printf '%s\\n' \"\$code\"; test \"\$code\" = '200'" \
  "Verifie que le vhost intranet repond exactement en HTTP 200 avec une demande sans cache. Si le code est different, le script echoue."

run_cmd \
  "Verifier le worker Nginx sous www-nginx" \
  "ps -eo user:32,args | awk '\$1 == \"'$NGINX_USER'\" && /nginx: worker process/ {found=1; print} END {exit !found}'" \
  "Prouve que les workers Nginx tournent sous l'utilisateur dedie et pas sous root."

run_cmd \
  "Verifier les regles UFW finales" \
  "ufw status verbose" \
  "Conserve la preuve des ports exposes : SSH restreint au sous-reseau et HTTP 80 ouvert."

run_cmd \
  "Verifier les checksums finaux" \
  "cd / && sha256sum -c '$CHECKSUM_FILE' && sha256sum -c '$BACKUP_DIR/www-checksums.txt'" \
  "Valide les checksums des configurations et de la sauvegarde web."

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
  echo "## Actions correctives et commandes de verification"
  echo
  echo "| Action corrective | Commande appliquee | Verification associee |"
  echo "| --- | --- | --- |"
  echo "| Creer la sauvegarde des donnees | \`rsync -avz --delete '$SOURCE_DIR/' '$RSYNC_DEST/'\` | \`find '$RSYNC_DEST' -maxdepth 2 -type f -ls\` et \`rsync --dry-run --checksum\` |"
  echo "| Archiver les configurations | \`tar -czf '$CONFIG_ARCHIVE' /etc/ssh /etc/rsyslog.d\` | \`tar -tzf '$CONFIG_ARCHIVE'\` |"
  echo "| Tester la restauration configs | \`tar -xzf '$CONFIG_ARCHIVE' -C '$RESTORE_DIR'\` | \`ls '$RESTORE_DIR/etc/ssh'\` et lecture de \`sshd_config\` |"
  echo "| Verifier l'integrite configs | \`sha256sum '$CONFIG_ARCHIVE' > '$CHECKSUM_FILE'\` | \`sha256sum -c '$CHECKSUM_FILE'\` |"
  echo "| Durcir l'execution Nginx | directive \`user $NGINX_USER;\` dans \`/etc/nginx/nginx.conf\` | \`ps -eo user,args | grep '[n]ginx'\` |"
  echo "| Publier l'intranet | vhost \`/etc/nginx/sites-available/intranet\` | \`nginx -t\` puis \`curl http://$INTRANET_HOST\` |"
  echo "| Filtrer le reseau | UFW SSH restreint + HTTP ouvert | \`ufw status verbose\` |"
  echo "| Activer l'anti force brute | jail Fail2ban \`sshd\` | \`fail2ban-client status sshd\` |"
  echo "| Sauvegarder /var/www | \`rsync -avz --delete /var/www/ '$WWW_BACKUP_DIR/'\` | \`sha256sum -c '$BACKUP_DIR/www-checksums.txt'\` et restauration testee |"
  echo
  echo "## Etat final verifiable"
  echo
  echo "| Controle | Commande | Etat attendu |"
  echo "| --- | --- | --- |"
  echo "| Intranet HTTP | \`curl -s -H 'Cache-Control: no-cache' -o /tmp/intranet-curl-body.txt -w '%{http_code}' http://$INTRANET_HOST\` | \`200\` |"
  echo "| Worker dedie | \`ps -eo user,args | grep '[n]ginx: worker'\` | \`$NGINX_USER\` |"
  echo "| Pare-feu | \`ufw status verbose\` | SSH restreint au campus, HTTP 80 ouvert |"
  echo "| Sauvegardes | \`sha256sum -c '$CHECKSUM_FILE'\` et \`sha256sum -c '$BACKUP_DIR/www-checksums.txt'\` | \`OK\` |"
  echo "| Restauration | \`test -f '$WWW_RESTORE_DIR/intranet.alpesnet.local/html/index.html'\` | fichier restauré lisible |"
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
  echo
  echo "Conclusion : la sauvegarde est creee, verifiee, restauree dans un repertoire de test, puis le serveur Nginx intranet est deployee et controle selon les criteres Autonomie 3."
} >> "$REPORT"

if [ -d "$INTRANET_ROOT" ]; then
  cp "$REPORT" "$PUBLIC_REPORT"
  chown root:"$NGINX_USER" "$PUBLIC_REPORT"
  chmod 640 "$PUBLIC_REPORT"
fi

COMPLETED=1

echo "Done."
echo "Report: $REPORT"
echo "Raw log: $RAW_LOG"
