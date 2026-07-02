#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_NAME="$(basename "$0")"
FLAGS_DIR="${FLAGS_DIR:-/flags}"
STATE_DIR="$FLAGS_DIR/.ctf-alpesnet"
LOG_DIR="${LOG_DIR:-/var/log/ctf-alpesnet}"
RUN_ID="$(date +%Y%m%d_%H%M%S)"
LOG_FILE="$LOG_DIR/$RUN_ID-$SCRIPT_NAME.log"
PRENOM="${PRENOM:-prenom}"
MACHINE_IP="${MACHINE_IP:-}"
REPORT_DATE="${REPORT_DATE:-2026-07-03}"
AUTHORIZED_USERS="${AUTHORIZED_USERS:-root oliv olivier ${SUDO_USER:-} ${USER:-}}"
SSH_PUBLIC_KEY="${SSH_PUBLIC_KEY:-}"
F1_METHOD="${F1_METHOD:-}"
APPLY=0
DRY_RUN=0
AUTO_ALL=0
INTERACTIVE=0
TASKS=()

declare -A STEP_TO_TASK=(
  [1]=F1
  [2]=F2
  [3]=F3
  [4]=F4
  [5]=F5
  [6]=F6
  [7]=F7
  [8]=F8
)

usage() {
  cat <<USAGE
Usage: sudo ./$SCRIPT_NAME [options]

Options:
  --menu                Lance un menu interactif étape par étape
  --all                 Exécute F1 à F8 dans l'ordre
  --task F1|F2|...      Exécute un flag précis
  --step 1..8           Exécute l'étape associée
  --prenom PRENOM       Génère /flags/rapport_PRENOM.txt et .md
  --ip X.X.X.X          Renseigne l'IP de la VM dans le rapport
  --f1-method TEXTE     Force la methode F1 documentee dans /flags/F1.txt
  --authorized-users L  Liste de comptes legitimes a exclure de F2
  --ssh-public-key KEY  Cle publique SSH a installer pour l'utilisateur cible
  --apply               Applique les corrections F2/F4/F5/F6/F7 après confirmation
  --dry-run             Affiche les actions sans les exécuter
  -h, --help            Affiche cette aide

Exemples:
  sudo ./ctf-alpesnet.sh --menu --prenom Olivier --ip 192.168.56.20
  sudo ./ctf-alpesnet.sh --all --prenom Alice --ip 192.168.56.20
  sudo ./ctf-alpesnet.sh --task F1 --f1-method "mot de passe cache retrouve dans la VM puis su root"
  sudo ./ctf-alpesnet.sh --task F3 --prenom Alice
  sudo ./ctf-alpesnet.sh --task F2 --authorized-users "root oliv admin-alpesnet"
  sudo ./ctf-alpesnet.sh --task F5 --ssh-public-key "\$(cat ~/.ssh/id_ed25519.pub)" --apply
  sudo ./ctf-alpesnet.sh --task F5 --apply --prenom Alice
USAGE
}

log() {
  mkdir -p "$LOG_DIR"
  printf '%s %s\n' "$(date '+%F %T')" "$*" >> "$LOG_FILE"
}

ensure_directories() {
  if [ "$DRY_RUN" -eq 0 ]; then
    mkdir -p "$FLAGS_DIR" "$STATE_DIR" "$LOG_DIR"
    touch "$STATE_DIR/timeline.tsv" "$STATE_DIR/actions.tsv"
  fi
}

need_root_for_flags() {
  if [ "$(id -u)" -ne 0 ] && [ ! -w "$FLAGS_DIR" ]; then
    echo "Ce script doit etre lance avec sudo pour ecrire dans $FLAGS_DIR." >&2
    exit 1
  fi
}

append_timeline() {
  local event="$1"
  local source="$2"
  local stamp
  stamp="$(date '+%F %T')"
  printf '%s\t%s\t%s\n' "$stamp" "$event" "$source" >> "$STATE_DIR/timeline.tsv"
  log "TIMELINE $event | $source"
}

append_action() {
  local flag="$1"
  local action="$2"
  local verification="$3"
  printf '%s\t%s\t%s\n' "$flag" "$action" "$verification" >> "$STATE_DIR/actions.tsv"
  log "ACTION $flag | $action | $verification"
}

live_section() {
  printf '\n=== %s ===\n' "$1"
}

live_info() {
  printf '[INFO] %s\n' "$1"
}

live_ok() {
  printf '[OK] %s\n' "$1"
}

live_warn() {
  printf '[A VERIFIER] %s\n' "$1"
}

live_ko() {
  printf '[KO] %s\n' "$1"
}

save_state() {
  local key="$1"
  local value="$2"
  printf '%s\n' "$value" > "$STATE_DIR/$key"
}

read_state() {
  local key="$1"
  local default="${2:-A completer}"
  if [ -s "$STATE_DIR/$key" ]; then
    head -n 1 "$STATE_DIR/$key"
  else
    printf '%s\n' "$default"
  fi
}

ask_value() {
  local prompt="$1"
  local default="${2:-}"
  local answer
  if [ "$INTERACTIVE" -eq 1 ]; then
    read -r -p "$prompt${default:+ [$default]} : " answer
    printf '%s\n' "${answer:-$default}"
  else
    printf '%s\n' "$default"
  fi
}

confirm() {
  local prompt="$1"
  local answer
  if [ "$APPLY" -ne 1 ]; then
    return 1
  fi
  if [ "$INTERACTIVE" -eq 1 ]; then
    read -r -p "$prompt [oui/non] : " answer
    [ "$answer" = "oui" ]
  else
    return 0
  fi
}

confirm_destructive() {
  local prompt="$1"
  local answer
  if [ "$APPLY" -ne 1 ]; then
    return 1
  fi
  if [ "$INTERACTIVE" -ne 1 ]; then
    return 0
  fi
  read -r -p "$prompt [taper SUPPRIMER pour confirmer] : " answer
  [ "$answer" = "SUPPRIMER" ]
}

run_cmd() {
  local cmd="$1"
  local out="${2:-}"
  echo "+ $cmd"
  log "$cmd"
  if [ "$DRY_RUN" -eq 1 ]; then
    [ -n "$out" ] && printf '[DRY-RUN] %s\n' "$cmd" >> "$out"
    return 0
  fi
  if [ -n "$out" ]; then
    bash -c "$cmd" >> "$out" 2>&1
  else
    bash -c "$cmd"
  fi
}

write_header() {
  local out="$1"
  local title="$2"
  {
    echo "# $title"
    echo
    echo "Date : $(date '+%F %T')"
    echo "Machine : $(hostname)"
    echo "IP : ${MACHINE_IP:-$(hostname -I 2>/dev/null | awk '{print $1}')}"
    echo
  } > "$out"
}

build_f1_password_clues() {
  local clues="$STATE_DIR/f1_password_clues.log"
  local roots=()
  local skip_home="${SUDO_USER:-${USER:-oliv}}"
  local marker_regex='investigateur|backdoor-sys|Inv3st1g4t3ur!|root.{0,40}(pass|passwd|password|mdp|su|login|secret|credential|creds)|((pass|passwd|password|mdp|su|login|secret|credential|creds).{0,40}root)'
  : > "$clues"

  for wanted in /home/investigateur /home/backdoor-sys; do
    [ -d "$wanted" ] && roots+=("$wanted")
  done
  if [ -d /home ]; then
    while IFS= read -r home_dir; do
      case "$home_dir" in
        "/home/$skip_home"|/home/oliv|/home/olivier)
          continue ;;
      esac
      roots+=("$home_dir")
    done < <(find /home -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort)
  fi
  {
    echo "Racines inspectees pour F1 :"
    printf '%s\n' "${roots[@]}"
    echo
    echo "Racines volontairement exclues : /root et fichiers .ctf_answer* (reponses formateur), /home/oliv /home/olivier /home/$skip_home"
    echo
    echo "Marqueurs scenario recherches dans les homes suspects : investigateur, backdoor-sys, Inv3st1g4t3ur!, root avec contexte pass/su/login"
    echo
    echo "Fichiers caches inspectes dans les homes suspects :"
    for base in "${roots[@]}"; do
      [ -d "$base" ] || continue
      find "$base" -xdev -maxdepth 3 \
        ! -name '.ctf_answer' \
        ! -name '.ctf_answers' \
        -type f -name '.*' -printf '%m %u:%g %p\n' 2>/dev/null | head -60 || true
    done
    echo
    echo "Fichiers dont le nom evoque les users du scenario :"
    for base in "${roots[@]}"; do
      [ -d "$base" ] || continue
      find "$base" -xdev -maxdepth 5 \
        ! -path '*/.git/*' \
        ! -path '*/node_modules/*' \
        ! -path '*/vendor/*' \
        ! -path '*/site/*' \
        ! -name '.ctf_answer' \
        ! -name '.ctf_answers' \
        -type f \( \
        -iname '*investigateur*' -o \
        -iname '*backdoor*' -o \
        -iname '*root*' \
      \) -printf '%m %u:%g %p\n' 2>/dev/null | head -30 || true
    done
    echo
    echo "Fichiers contenant les marqueurs exacts du scenario :"
    for base in "${roots[@]}"; do
      [ -d "$base" ] || continue
      find "$base" -xdev -maxdepth 5 \
        ! -path '*/.git/*' \
        ! -path '*/node_modules/*' \
        ! -path '*/vendor/*' \
        ! -path '*/site/*' \
        ! -name '.ctf_answer' \
        ! -name '.ctf_answers' \
        -type f -readable -size -512k -print0 2>/dev/null \
        | xargs -0 grep -IlE "$marker_regex" 2>/dev/null \
        | sort -u \
        | head -50 || true
    done
    echo
    echo "Occurrences utiles avec fichier source et ligne :"
    for base in "${roots[@]}"; do
      [ -d "$base" ] || continue
      find "$base" -xdev -maxdepth 5 \
        ! -path '*/.git/*' \
        ! -path '*/node_modules/*' \
        ! -path '*/vendor/*' \
        ! -path '*/site/*' \
        ! -name '.ctf_answer' \
        ! -name '.ctf_answers' \
        -type f -readable -size -512k -print0 2>/dev/null \
        | xargs -0 grep -IEni "$marker_regex" 2>/dev/null \
        | head -80 || true
    done
  } >> "$clues"

  sed -i '/^[[:space:]]*$/d' "$clues" 2>/dev/null || true
  printf '%s\n' "$clues"
}

has_f1_password_clues() {
  local clues="$1"
  [ -s "$clues" ] && grep -Eq '^/home/[^:]+:[0-9]+:' "$clues"
}

write_f1_ssh_check() {
  local target_ip="${MACHINE_IP:-$(hostname -I 2>/dev/null | awk '{print $1}')}"

  echo "Verification SSH root annoncee par le scenario :"
  echo
  echo "Configuration SSH utile :"
  if command -v sshd >/dev/null 2>&1; then
    sshd -T 2>/dev/null | grep -Ei '^(permitrootlogin|passwordauthentication|pubkeyauthentication|permitemptypasswords)[[:space:]]' || true
  else
    echo "sshd absent ou commande introuvable."
  fi
  echo
  echo "Service SSH :"
  systemctl is-active ssh 2>/dev/null || systemctl is-active sshd 2>/dev/null || echo "service ssh/sshd non actif ou systemctl indisponible"
  echo
  echo "Port 22 en ecoute :"
  ss -tlnp 2>/dev/null | awk 'NR==1 || /:22[[:space:]]/' || true
  echo
  echo "Commande de preuve a lancer depuis la machine hote si root SSH est encore autorise :"
  echo "ssh root@${target_ip:-IP_VM}"
  echo "Ne pas utiliser /root/.ctf_answers ou .ctf_answer : ce sont les reponses formateur."
}

task_f1() {
  local out="$FLAGS_DIR/F1.txt"
  local default_method="sudo su sans mot de passe : droits sudo trop permissifs sur le compte initial"
  local hidden_method="mot de passe cache retrouve dans la VM puis utilisation de su/root ou ssh root@IP"
  local password_clues
  password_clues="$(build_f1_password_clues)"
  write_header "$out" "F1 - Acces root"
  {
    echo "Objectif : obtenir l'acces root sur la VM compromise."
    echo
    echo "Commandes de preuve :"
    echo '```'
    id
    whoami
    echo
    echo "sudo -n true :"
    sudo -n true >/dev/null 2>&1 && echo "OK - sudo utilisable sans mot de passe" || echo "KO - sudo demande un mot de passe ou est interdit"
    echo
    echo "sudo -l :"
    sudo -l 2>&1 || true
    echo '```'
    echo
    write_f1_ssh_check
    echo
    echo "Recherche d'un mot de passe cache dans la VM :"
    echo '```'
    if has_f1_password_clues "$password_clues"; then
      sed -n '1,120p' "$password_clues"
    else
      echo "Aucun indice de mot de passe cache trouve automatiquement dans les racines ciblees."
    fi
    echo '```'
    echo
    echo "Commandes rejouables pour la demo :"
    echo '```bash'
    echo "sudo find /home -mindepth 1 -maxdepth 1 -type d ! -name oliv ! -name olivier -print"
    echo "sudo find /home/investigateur /home/backdoor-sys -xdev -maxdepth 3 -type f -name '.*' ! -name '.ctf_answer' ! -name '.ctf_answers' -printf '%m %u:%g %p\\n' 2>/dev/null"
    echo "sudo grep -RInEi --exclude='.ctf_answer' --exclude='.ctf_answers' 'investigateur|backdoor-sys|Inv3st1g4t3ur!|root.{0,40}(pass|passwd|password|mdp|su|login|secret|credential|creds)|((pass|passwd|password|mdp|su|login|secret|credential|creds).{0,40}root)' /home/investigateur /home/backdoor-sys 2>/dev/null | head -80"
    echo "sshd -T | grep -Ei '^(permitrootlogin|passwordauthentication)'"
    echo "systemctl is-active ssh || systemctl is-active sshd"
    echo "ss -tlnp | grep ':22'"
    echo "ssh root@${MACHINE_IP:-IP_VM}"
    echo '```'
    echo
  } >> "$out" 2>&1

  local method="A completer : decrire l'escalade de privileges utilisee"
  if [ -n "$F1_METHOD" ]; then
    method="$F1_METHOD"
    live_ok "F1 : methode forcee par option --f1-method : $method"
  elif has_f1_password_clues "$password_clues"; then
    method="$hidden_method"
    live_ok "F1 : indices de mot de passe cache detectes, methode retenue : $method"
  elif [ "$(id -u)" -eq 0 ]; then
    method="$default_method"
    live_ok "F1 : acces root confirme, methode retenue automatiquement : $method"
  elif sudo -n true >/dev/null 2>&1; then
    method="$default_method"
    live_ok "F1 : sudo sans mot de passe confirme, methode retenue automatiquement : $method"
  else
    {
      echo "Acces root non obtenu pendant cette execution."
      echo "Indice utile : verifier sudo -l, services mal configures, SUID inattendus."
      sudo -l 2>&1 || true
    } >> "$out"
    live_warn "F1 : acces root non confirme automatiquement, voir $out."
  fi

  {
    echo "Resultat a soumettre :"
    echo "$method"
  } >> "$out"
  save_state "f1_method" "$method"
  append_timeline "Acces root obtenu et methode documentee" "id ; whoami ; sudo -l ; recherche mot de passe cache"
  append_action "F1" "Acces root : $method" "id ; whoami ; sudo -l ; find/grep indices mot de passe cache"
  echo "F1 ecrit dans $out"
}

is_known_system_user() {
  case "$1" in
    root|daemon|bin|sys|sync|games|man|lp|mail|news|uucp|proxy|www-data|backup|list|irc|gnats|nobody|_apt|messagebus|sshd|systemd-*|polkitd|uuidd|tcpdump|tss|mysql|postgres|redis|Debian-exim)
      return 0 ;;
    *)
      return 1 ;;
  esac
}

is_authorized_user() {
  local candidate="$1"
  [[ " $AUTHORIZED_USERS " == *" $candidate "* ]]
}

build_f2_candidates() {
  local candidates="$STATE_DIR/f2_candidates.tsv"
  : > "$candidates"

  while IFS=: read -r user _ uid gid gecos home shell; do
    local score=0
    local reasons=()
    local strong="non"
    local groups=""

    is_known_system_user "$user" && continue
    is_authorized_user "$user" && continue

    if [ "$uid" -eq 0 ]; then
      score=$((score + 100))
      strong="oui"
      reasons+=("UID 0 hors root")
    fi

    if [ "$uid" -ge 1000 ] && [ "$uid" -lt 60000 ]; then
      score=$((score + 15))
      reasons+=("UID utilisateur")
    fi

    if [[ "$shell" =~ /(bash|sh|zsh)$ ]]; then
      score=$((score + 10))
      reasons+=("shell interactif")
    fi

    if [[ "$home" == /home/* ]]; then
      score=$((score + 5))
      reasons+=("home dans /home")
    fi

    groups="$(id -nG "$user" 2>/dev/null || true)"
    if [[ " $groups " =~ [[:space:]](sudo|admin|wheel)[[:space:]] ]]; then
      score=$((score + 40))
      reasons+=("groupe admin/sudo")
    fi

    if grep -RqsE "(^|[^A-Za-z0-9_-])$user([^A-Za-z0-9_-]|$)" /etc/sudoers /etc/sudoers.d 2>/dev/null; then
      score=$((score + 50))
      strong="oui"
      reasons+=("reference sudoers")
    fi

    if [ "$score" -gt 0 ]; then
      local reason_text
      reason_text="$(IFS=', '; echo "${reasons[*]}")"
      printf '%03d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$score" "$user" "$uid" "$gid" "$home" "$shell" "$strong" "$reason_text" >> "$candidates"
    fi
  done < /etc/passwd

  sort -r "$candidates" -o "$candidates"
}

print_active_sudoers_d() {
  local found=0
  local file

  while IFS= read -r -d '' file; do
    found=1
    grep -Hve '^[[:space:]]*#' -e '^[[:space:]]*$' "$file" 2>/dev/null || true
  done < <(find /etc/sudoers.d -maxdepth 1 -type f ! -name '*~' ! -name '*.*' ! -name 'README' -print0 2>/dev/null)

  if [ "$found" -eq 0 ]; then
    echo "Aucun fichier sudoers additionnel actif hors README."
  fi
}

choose_f2_suspect() {
  local candidates="$1"
  local default="$2"
  local answer suspect

  if [ "$INTERACTIVE" -ne 1 ]; then
    printf '%s\n' "$default"
    return
  fi

  echo >&2
  echo "Candidats suspects F2 :" >&2
  if [ -s "$candidates" ]; then
    awk -F '\t' '{
      printf "%2d. %-18s score=%s uid=%s shell=%s indice_fort=%s raisons=%s\n", NR, $2, $1, $3, $6, $7, $8
    }' "$candidates" >&2
    echo >&2
    echo "Choisir un numero, appuyer sur Entree pour garder le defaut, ou taper un autre login." >&2
  else
    echo "Aucun candidat calcule automatiquement." >&2
    echo "Taper le login du compte non autorise si le formateur l'a donne ou si vous l'avez identifie manuellement." >&2
  fi

  read -r -p "Compte non autorise identifie pour F2 [$default] : " answer
  answer="${answer:-$default}"

  if [[ "$answer" =~ ^[0-9]+$ ]] && [ -s "$candidates" ]; then
    suspect="$(awk -F '\t' -v n="$answer" 'NR==n{print $2}' "$candidates")"
    if [ -n "$suspect" ]; then
      printf '%s\n' "$suspect"
      return
    fi
    printf '[A VERIFIER] Numero F2 invalide, valeur par defaut conservee : %s\n' "$default" >&2
    printf '%s\n' "$default"
    return
  fi

  printf '%s\n' "$answer"
}

print_account_creation_clues() {
  local user="$1"
  local home

  echo "Compte analyse : $user"
  echo
  echo "Entree passwd :"
  getent passwd "$user" || true
  echo

  home="$(getent passwd "$user" | awk -F: '{print $6}')"
  echo "Dates du dossier personnel :"
  if [ -n "$home" ] && [ -e "$home" ]; then
    stat -c 'Birth: %w' "$home" 2>/dev/null || true
    stat -c 'Change: %z' "$home" 2>/dev/null || true
    stat -c 'Modify: %y' "$home" 2>/dev/null || true
    stat -c 'Access: %x' "$home" 2>/dev/null || true
    stat -c 'Path: %n' "$home" 2>/dev/null || true
  else
    echo "Home introuvable pour $user."
  fi
  echo

  echo "Informations chage :"
  chage -l "$user" 2>/dev/null || echo "chage indisponible ou compte inaccessible."
  echo

  echo "Traces de creation dans les logs locaux :"
  local found=0
  local logpath
  for logpath in /var/log/auth.log /var/log/auth.log.1 /var/log/syslog /var/log/syslog.1; do
    if [ -r "$logpath" ] && grep -EH "useradd|adduser|new user|new group|$user" "$logpath" 2>/dev/null | grep -E "$user|useradd|adduser" | head -n 20; then
      found=1
    fi
  done
  if [ "$found" -eq 0 ]; then
    echo "Aucune trace useradd/adduser exploitable trouvee dans les logs non compresses."
  fi
  echo

  echo "Connexions connues :"
  lastlog -u "$user" 2>/dev/null || true
  last "$user" 2>/dev/null | head -n 10 || true
}

task_f2() {
  local out="$FLAGS_DIR/F2.txt"
  build_f2_candidates
  local candidates="$STATE_DIR/f2_candidates.tsv"
  local auto_suspect="A completer"
  if [ -s "$candidates" ]; then
    auto_suspect="$(awk -F '\t' '$7=="oui"{print $2; exit}' "$candidates")"
    auto_suspect="${auto_suspect:-$(awk -F '\t' 'NR==1{print $2}' "$candidates")}"
    auto_suspect="${auto_suspect:-A completer}"
  fi

  write_header "$out" "F2 - Compte non autorise"
  {
    echo "Objectif : identifier le compte cree par l'attaquant."
    echo
    echo "Audit immediat :"
    echo '```'
    id
    echo
    echo "Comptes UID 0 autres que root :"
    awk -F: '($3==0)&&($1!="root"){print $1":"$3":"$6":"$7}' /etc/passwd || true
    echo
    echo "Comptes avec shell interactif :"
    awk -F: '($7 ~ /(bash|sh|zsh)$/){print $1":"$3":"$6":"$7}' /etc/passwd || true
    echo
    echo "Groupes par utilisateur :"
    while IFS=: read -r user _ uid _ _ _ _; do
      [ "$uid" -ge 1000 ] || [ "$uid" -eq 0 ] || continue
      printf '%s: %s\n' "$user" "$(id -nG "$user" 2>/dev/null || echo groupes_inaccessibles)"
    done < /etc/passwd
    echo
    echo "Sudoers additionnels :"
    print_active_sudoers_d
    echo
    echo "Dernieres connexions :"
    lastlog 2>/dev/null | head -n 30 || true
    echo '```'
    echo
    echo "Explication des commandes F2 :"
    echo
    echo "- \`awk -F: '(\$3==0)'\` lit \`/etc/passwd\` avec \`:\` comme separateur. Le champ 3 est l'UID. Un UID \`0\` donne les privileges root ; tout compte UID 0 autre que \`root\` est donc critique."
    echo "- \`getent passwd\` confirme l'existence d'un compte et affiche son UID, son home et son shell."
    echo "- La boucle \`id -nG\` affiche les groupes par utilisateur, ce qui permet de reperer un compte ajoute a \`sudo\`, \`admin\` ou \`wheel\`."
    echo "- La lecture de \`/etc/sudoers.d\` montre les regles sudo additionnelles actives, sans le README ni les commentaires."
    echo "- \`lastlog\` aide a reperer une connexion recente ou anormale."
    echo
    echo "Candidats suspects calcules par le script :"
    echo "Utilisateurs consideres autorises et exclus du score : $AUTHORIZED_USERS"
    echo
    if [ -s "$candidates" ]; then
      echo "| Score | User | UID | GID | Home | Shell | Indice fort | Raisons |"
      echo "| ---: | --- | ---: | ---: | --- | --- | --- | --- |"
      awk -F '\t' '{printf "| %d | `%s` | %s | %s | `%s` | `%s` | %s | %s |\n", $1, $2, $3, $4, $5, $6, $7, $8}' "$candidates"
    else
      echo "Aucun candidat fort detecte automatiquement. Comparer manuellement avec le contexte donne par le formateur."
    fi
    echo
    echo "Resultat observe F2 :"
    echo
    if [ "$auto_suspect" = "A completer" ]; then
      echo "Aucun compte suspect fort n'a ete retenu automatiquement. Le resultat doit etre confirme manuellement avec les sorties ci-dessus."
    else
      echo "Le compte le plus probable est \`$auto_suspect\` car il ressort dans les indices calcules ci-dessus."
    fi
    echo
  } >> "$out"

  local suspect
  suspect="$(choose_f2_suspect "$candidates" "$auto_suspect")"
  if [ "$suspect" = "A completer" ] || [[ "$suspect" =~ ^A\ completer ]]; then
    live_warn "F2 : aucun compte suspect retenu automatiquement, choix manuel necessaire."
  else
    live_ok "F2 : compte retenu pour le rapport : $suspect"
  fi
  save_state "f2_account" "$suspect"
  {
    echo "Compte suspect retenu : $suspect"
    echo "Commande de verification : getent passwd $suspect"
  } >> "$out"

  if [ "$suspect" != "A completer" ]; then
    {
      echo
      echo "Estimation de la date de creation du compte suspect :"
      echo
      echo '```'
      print_account_creation_clues "$suspect"
      echo '```'
      echo
      echo "Explication : Linux ne stocke pas toujours une date de creation de compte fiable. On l'estime en croisant la date de naissance/modification du home, les informations chage, les traces useradd/adduser dans les logs et les premieres connexions."
    } >> "$out"
  fi

  if [ "$suspect" != "A completer" ] && confirm_destructive "Supprimer le compte $suspect avec userdel -r ?" ; then
    run_cmd "userdel -r '$suspect'" "$out" || true
    run_cmd "getent passwd '$suspect' || echo 'Compte absent apres correction.'" "$out"
    append_action "F2" "userdel -r $suspect" "getent passwd $suspect doit ne rien retourner"
  else
    append_action "F2" "Compte non autorise identifie : $suspect" "getent passwd $suspect"
  fi

  append_timeline "Audit des comptes et sudoers" "awk UID0 ; getent passwd ; sudoers.d actifs hors README ; lastlog"
  echo "F2 ecrit dans $out"
}

task_f3() {
  local out="$FLAGS_DIR/F3.txt"
  local raw_events="$STATE_DIR/f3_ssh_events.log"
  local ip_counts="$STATE_DIR/f3_ip_counts.tsv"
  : > "$raw_events"
  : > "$ip_counts"

  for logpath in /var/log/auth.log /var/log/auth.log.1 /var/log/secure /var/log/secure.1; do
    if [ -r "$logpath" ]; then
      grep -EH "Invalid user|Failed password|authentication failure|Connection closed by invalid user|Disconnected from invalid user|PAM.*authentication failure" "$logpath" >> "$raw_events" 2>/dev/null || true
    fi
  done
  journalctl -u ssh -u sshd --no-pager 2>/dev/null \
    | grep -E "Invalid user|Failed password|authentication failure|Connection closed by invalid user|Disconnected from invalid user|PAM.*authentication failure" >> "$raw_events" || true

  awk '
    {
      for (i = 1; i <= NF; i++) {
        token = $i
        gsub(/[^0-9.]/, "", token)
        if (token ~ /^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/) {
          split(token, octets, ".")
          valid = 1
          for (j = 1; j <= 4; j++) {
            if (octets[j] < 0 || octets[j] > 255) valid = 0
          }
          if (valid == 1) print token
        }
      }
    }
  ' "$raw_events" | sort | uniq -c | sort -nr | awk '{print $1 "\t" $2}' > "$ip_counts"

  local ip="A completer"
  if [ -s "$ip_counts" ]; then
    ip="$(awk -F '\t' 'NR==1{print $2}' "$ip_counts")"
  fi

  write_header "$out" "F3 - IP source des tentatives d'intrusion"
  {
    echo "Objectif : trouver l'IP source des tentatives d'intrusion."
    echo
    echo "Logs examines : /var/log/auth.log, /var/log/auth.log.1, /var/log/secure, /var/log/secure.1, journalctl -u ssh/sshd"
    echo
    echo "Compteur IP extrait automatiquement :"
    echo
    if [ -s "$ip_counts" ]; then
      echo "| Occurrences | IP |"
      echo "| ---: | --- |"
      { awk -F '\t' '{printf "| %s | `%s` |\n", $1, $2}' "$ip_counts" | head -20; } || true
    else
      echo "Aucune IP trouvee dans les evenements SSH suspects disponibles."
    fi
    echo
    echo "IP source retenue automatiquement : $ip"
    echo
    echo "Extraits de logs justificatifs pour $ip :"
    echo '```'
    if [ "$ip" != "A completer" ]; then
      grep -F "$ip" "$raw_events" | head -20 || true
    else
      head -20 "$raw_events" || true
    fi
    echo '```'
    echo
    echo "Fichiers de travail :"
    echo "- Evenements SSH : $raw_events"
    echo "- Compteur IP : $ip_counts"
  } >> "$out"

  save_state "f3_ip" "$ip"
  {
    echo
    echo "Resultat a soumettre :"
    echo "IP source retenue : $ip"
    echo "Commande de preuve : grep/awk sur les logs SSH, voir compteur ci-dessus."
  } >> "$out"
  append_timeline "Analyse des logs d'authentification et extraction IP" "/var/log/auth.log ; journalctl -u ssh"
  append_action "F3" "IP source identifiee : $ip" "compter les occurrences par IP dans les logs SSH"
  echo "F3 ecrit dans $out"
}

is_expected_permission_path() {
  case "$1" in
    /tmp|/var/tmp|/dev/shm|/run/lock|/var/lock)
      return 0 ;;
    /var/crash|/var/metrics)
      return 0 ;;
    /usr/bin/sudo|/usr/bin/su|/usr/bin/passwd|/usr/bin/chsh|/usr/bin/chfn|/usr/bin/gpasswd|/usr/bin/newgrp|/usr/bin/mount|/usr/bin/umount|/usr/bin/pkexec|/usr/lib/openssh/ssh-keysign|/usr/lib/dbus-1.0/dbus-daemon-launch-helper)
      return 0 ;;
    *)
      return 1 ;;
  esac
}

build_f4_candidates() {
  local candidates="$STATE_DIR/f4_candidates.tsv"
  : > "$candidates"

  while IFS=$'\t' read -r mode owner group type path; do
    [ -n "$path" ] || continue
    is_expected_permission_path "$path" && continue

    local score=0
    local risk=""
    local fix="750"
    local last3="${mode: -3}"
    local special="${mode:0:1}"

    [ "$type" = "l" ] && continue
    if [ "$type" = "d" ] && [ "$last3" = "777" ] && [[ "$special" =~ [13] ]]; then
      continue
    fi

    if [ "$last3" = "777" ]; then
      score=$((score + 100))
      risk="permissions 0777"
      if [ "$type" = "f" ]; then
        fix="640"
      else
        fix="750"
      fi
    fi

    if [ "$type" = "f" ] && [ "${#mode}" -eq 4 ] && [[ "$special" =~ [24567] ]]; then
      score=$((score + 80))
      risk="${risk:+$risk + }SUID/SGID"
      fix="u-s,g-s"
    fi

    case "$path" in
      /home/*|/opt/*|/srv/*|/var/www/*|/usr/local/*)
        score=$((score + 30)) ;;
      /tmp/*|/var/tmp/*|/dev/shm/*)
        score=$((score + 20)) ;;
      /usr/bin/*|/usr/sbin/*|/bin/*|/sbin/*)
        score=$((score - 20)) ;;
    esac

    if [ "$owner" = "root" ]; then
      score=$((score + 10))
    fi

    if [ "$score" -gt 0 ] && [ -n "$risk" ]; then
      printf '%03d\t%s\t%s\t%s:%s\t%s\t%s\t%s\n' "$score" "$path" "$mode" "$owner" "$group" "$type" "$risk" "$fix" >> "$candidates"
    fi
  done < <(find / -xdev \( -perm 0777 -o -perm /4000 -o -perm /2000 \) -printf '%m\t%u\t%g\t%y\t%p\n' 2>/dev/null || true)

  sort -r "$candidates" -o "$candidates"
}

task_f4() {
  local out="$FLAGS_DIR/F4.txt"
  build_f4_candidates
  local candidates="$STATE_DIR/f4_candidates.tsv"
  local path="A completer"
  local mode="750"
  local risk="A completer"
  if [ -s "$candidates" ]; then
    path="$(awk -F '\t' '$1 >= 100{print $2; exit}' "$candidates")"
    mode="$(awk -F '\t' '$1 >= 100{print $7; exit}' "$candidates")"
    risk="$(awk -F '\t' '$1 >= 100{print $6; exit}' "$candidates")"
    path="${path:-A completer}"
    mode="${mode:-750}"
    risk="${risk:-A completer}"
  fi

  write_header "$out" "F4 - Permissions dangereuses"
  {
    echo "Objectif : identifier un fichier ou repertoire avec permissions dangereuses."
    echo
    echo "Candidats dangereux calcules automatiquement :"
    echo
    if [ -s "$candidates" ]; then
      echo "| Score | Chemin | Mode | Proprio | Type | Risque | Correction proposee |"
      echo "| ---: | --- | ---: | --- | --- | --- | --- |"
      { awk -F '\t' '{printf "| %d | `%s` | `%s` | `%s` | `%s` | %s | `chmod %s` |\n", $1, $2, $3, $4, $5, $6, $7}' "$candidates" | head -30; } || true
    else
      echo "Aucun candidat dangereux detecte automatiquement sur la partition racine."
    fi
    echo
    echo "Element retenu automatiquement : $path"
    echo "Risque retenu : $risk"
    echo "Correction proposee : chmod $mode $path"
    echo
    echo "Preuve stat :"
    echo '```'
    if [ "$path" != "A completer" ]; then
      stat -c '%a %A %U:%G %n' "$path" 2>/dev/null || true
    fi
    echo '```'
  } >> "$out"

  save_state "f4_path" "$path"
  save_state "f4_mode" "$mode"
  {
    echo
    echo "Resultat a soumettre :"
    echo "Element dangereux retenu : $path"
    echo "Risque : $risk"
    echo "Correction prevue : chmod $mode $path"
  } >> "$out"

  if [ "$path" != "A completer" ] && confirm "Appliquer chmod $mode sur $path ?" ; then
    run_cmd "chmod '$mode' '$path'" "$out" || true
    run_cmd "stat -c '%a %U:%G %n' '$path'" "$out" || true
    append_action "F4" "chmod $mode $path" "stat -c '%a %U:%G %n' $path"
  else
    append_action "F4" "Permission dangereuse documentee : $path" "find / -xdev -perm 0777 ; find / -xdev -perm /4000"
  fi

  append_timeline "Recherche des permissions dangereuses" "find / -perm 0777 ; find / -perm /4000"
  echo "F4 ecrit dans $out"
}

set_sshd_option() {
  local key="$1"
  local value="$2"
  local file="/etc/ssh/sshd_config"
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "[DRY-RUN] set $key $value in $file"
    log "DRY-RUN set $key $value in $file"
    return 0
  fi
  if grep -Eq "^[#[:space:]]*$key[[:space:]]+" "$file"; then
    sed -i "s|^[#[:space:]]*$key[[:space:]].*|$key $value|" "$file"
  else
    printf '\n%s %s\n' "$key" "$value" >> "$file"
  fi
}

write_fail2ban_jail() {
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "[DRY-RUN] write /etc/fail2ban/jail.d/ctf-sshd.local"
    return 0
  fi

  mkdir -p /etc/fail2ban/jail.d
  if [ -s /var/log/auth.log ]; then
    cat > /etc/fail2ban/jail.d/ctf-sshd.local <<'EOF'
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
EOF
  else
    cat > /etc/fail2ban/jail.d/ctf-sshd.local <<'EOF'
[sshd]
enabled = true
port = ssh
filter = sshd
backend = systemd
maxretry = 3
bantime = 3600
findtime = 600
EOF
  fi
}

report_fail2ban_status() {
  if ! command -v fail2ban-client >/dev/null 2>&1; then
    echo "fail2ban-client absent."
    return 0
  fi

  if fail2ban-client ping >/dev/null 2>&1; then
    fail2ban-client status 2>&1 || true
    fail2ban-client status sshd 2>&1 || true
  else
    echo "fail2ban-client ne trouve pas le socket : le service n'est probablement pas demarre."
    echo "Diagnostic systemd :"
    systemctl status fail2ban --no-pager 2>&1 | head -n 40 || true
    echo
    echo "Derniers logs fail2ban :"
    journalctl -u fail2ban --no-pager -n 40 2>&1 || true
  fi
}

target_ssh_user() {
  if id oliv >/dev/null 2>&1; then
    printf '%s\n' "oliv"
  else
    printf '%s\n' "oliv"
  fi
}

check_ssh_key_status() {
  local user="$1"
  local home
  home="$(getent passwd "$user" | awk -F: '{print $6}')"
  if [ -z "$home" ]; then
    echo "Utilisateur $user introuvable."
    return 1
  fi

  echo "Utilisateur SSH cible : $user"
  echo "Fichier authorized_keys : $home/.ssh/authorized_keys"
  if [ -s "$home/.ssh/authorized_keys" ]; then
    echo "authorized_keys existe deja."
    if [ -n "$SSH_PUBLIC_KEY" ] && grep -qxF "$SSH_PUBLIC_KEY" "$home/.ssh/authorized_keys"; then
      echo "La cle publique fournie est deja installee."
    elif [ -n "$SSH_PUBLIC_KEY" ]; then
      echo "authorized_keys existe, mais la cle fournie n'est pas encore presente."
    fi
  else
    echo "Aucune cle publique detectee dans authorized_keys."
  fi
}

install_ssh_public_key() {
  local user="$1"
  local key="$2"
  local home
  home="$(getent passwd "$user" | awk -F: '{print $6}')"
  if [ -z "$home" ]; then
    echo "Utilisateur $user introuvable."
    return 1
  fi
  if [ -z "$key" ]; then
    echo "Aucune cle publique fournie."
    return 1
  fi
  if ! printf '%s\n' "$key" | grep -Eq '^(ssh-ed25519|ssh-rsa|ecdsa-sha2-nistp[0-9]+) '; then
    echo "Format de cle publique non reconnu."
    return 1
  fi

  mkdir -p "$home/.ssh"
  touch "$home/.ssh/authorized_keys"
  if grep -qxF "$key" "$home/.ssh/authorized_keys"; then
    echo "Cle publique deja presente pour $user."
  else
    printf '%s\n' "$key" >> "$home/.ssh/authorized_keys"
    echo "Cle publique ajoutee pour $user."
  fi
  chown -R "$user:$user" "$home/.ssh" 2>/dev/null || chown -R "$user" "$home/.ssh" 2>/dev/null || true
  chmod 700 "$home/.ssh"
  chmod 600 "$home/.ssh/authorized_keys"
}

write_f5_proposals() {
  cat <<'EOF'
Corrections proposees pour F5 :
- SSH : verifier qu'une cle publique est presente dans ~/.ssh/authorized_keys.
- SSH : sauvegarder /etc/ssh/sshd_config puis limiter les connexions a AllowUsers oliv.
- SSH : conserver PasswordAuthentication yes pour ne pas casser scp/SSH pendant le CTF.
- SSH : conserver PubkeyAuthentication yes et refuser PermitEmptyPasswords.
- SSH : ne pas changer le mot de passe root et ne pas s'appuyer sur ce compte pour la connexion distante.
- SSH : valider avec sshd -t puis recharger ssh/sshd.
- UFW : deny incoming, allow outgoing, allow OpenSSH/22, HTTP/80, HTTPS/443, enable.
- Fail2ban : creer/mettre a jour la jail sshd, tester avec fail2ban-client -t, redemarrer le service.
- Services : arreter/desactiver les services inutiles detectes parmi avahi-daemon, cups, rpcbind, nfs-server, smbd.
EOF
}

write_f5_snapshot() {
  local label="$1"
  {
    echo "===== F5 $label ====="
    echo "Date : $(date '+%F %T')"
    echo "Machine : $(hostname)"
    echo
    echo "## SSH"
    grep -E '^(AllowUsers|PermitRootLogin|PasswordAuthentication|ChallengeResponseAuthentication|KbdInteractiveAuthentication|PubkeyAuthentication|PermitEmptyPasswords)' /etc/ssh/sshd_config 2>/dev/null || echo "Parametres SSH non trouves ou fichier inaccessible."
    echo
    echo "## Cle publique SSH"
    check_ssh_key_status "$(target_ssh_user)" || true
    echo
    echo "## UFW"
    if command -v ufw >/dev/null 2>&1; then
      ufw status verbose 2>&1 || true
    else
      echo "ufw absent"
    fi
    echo
    echo "## Fail2ban"
    report_fail2ban_status
    echo
    echo "## Ports en ecoute"
    ss -tulpn 2>/dev/null || true
    echo
    echo "## Services cibles"
    for svc in avahi-daemon cups rpcbind nfs-server smbd; do
      if systemctl list-unit-files "$svc.service" >/dev/null 2>&1; then
        printf '%s enabled=' "$svc"
        systemctl is-enabled "$svc" 2>&1 || true
        printf '%s active=' "$svc"
        systemctl is-active "$svc" 2>&1 || true
      else
        echo "$svc absent"
      fi
    done
  }
}

confirm_f5_apply() {
  if [ "$APPLY" -eq 1 ]; then
    return 0
  fi
  if [ "$INTERACTIVE" -eq 1 ]; then
    local answer
    read -r -p "Appliquer ces corrections F5 maintenant ? [oui/non] : " answer
    [ "$answer" = "oui" ]
    return
  fi
  return 1
}

task_f5() {
  local out="$FLAGS_DIR/F5.txt"
  local before="$FLAGS_DIR/F5_avant.txt"
  local after="$FLAGS_DIR/F5_apres.txt"
  write_header "$out" "F5 - Durcissement SSH, ufw, fail2ban et services"
  write_f5_snapshot "AVANT CORRECTION" > "$before"
  {
    echo "Objectif : appliquer SSH + ufw + fail2ban + services et preparer la demo live."
    echo
    echo "Rapport avant correction : $before"
    echo "Rapport apres correction : $after"
    echo
    echo "Etat initial synthetique :"
    echo '```'
    sed -n '1,120p' "$before"
    echo '```'
    echo
    write_f5_proposals
    echo
  } >> "$out"

  if [ "$(id -u)" -ne 0 ]; then
    echo "F5 doit etre applique en root." >> "$out"
    write_f5_snapshot "APRES AUDIT NON-ROOT" > "$after"
    append_action "F5" "Durcissement non applique : execution non-root" "relancer avec sudo"
    return
  fi

  if [ "$INTERACTIVE" -eq 1 ]; then
    echo
    write_f5_proposals
    echo
  fi

  if confirm_f5_apply ; then
    echo "Application des corrections F5." >> "$out"
    local ssh_user
    ssh_user="$(target_ssh_user)"
    if [ -z "$SSH_PUBLIC_KEY" ] && [ "$INTERACTIVE" -eq 1 ]; then
      read -r -p "Coller la cle publique SSH a installer pour $ssh_user (laisser vide pour passer) : " SSH_PUBLIC_KEY
    fi
    install_ssh_public_key "$ssh_user" "$SSH_PUBLIC_KEY" >> "$out" 2>&1 || true
    run_cmd "cp -n /etc/ssh/sshd_config /etc/ssh/sshd_config.ctf-alpesnet.bak" "$out" || true
    set_sshd_option AllowUsers "$ssh_user"
    set_sshd_option PasswordAuthentication yes
    set_sshd_option PubkeyAuthentication yes
    set_sshd_option PermitEmptyPasswords no
    run_cmd "sshd -t" "$out"
    run_cmd "systemctl reload ssh || systemctl reload sshd" "$out" || true

    if ! command -v ufw >/dev/null 2>&1 && command -v apt-get >/dev/null 2>&1; then
      run_cmd "apt-get update" "$out" || true
      run_cmd "apt-get install -y ufw" "$out" || true
    fi
    if command -v ufw >/dev/null 2>&1; then
      run_cmd "ufw default deny incoming" "$out"
      run_cmd "ufw default allow outgoing" "$out"
      run_cmd "ufw allow OpenSSH" "$out"
      run_cmd "ufw allow http" "$out" || true
      run_cmd "ufw allow https" "$out" || true
      run_cmd "ufw --force enable" "$out"
    fi

    if ! command -v fail2ban-client >/dev/null 2>&1 && command -v apt-get >/dev/null 2>&1; then
      run_cmd "apt-get install -y fail2ban" "$out" || true
    fi
    write_fail2ban_jail >> "$out"
    run_cmd "fail2ban-client -t" "$out" || true
    run_cmd "systemctl restart fail2ban" "$out" || true
    run_cmd "systemctl enable fail2ban" "$out" || true

    for svc in avahi-daemon cups rpcbind nfs-server smbd; do
      if systemctl list-unit-files "$svc.service" >/dev/null 2>&1; then
        run_cmd "systemctl stop '$svc' || true" "$out" || true
        run_cmd "systemctl disable '$svc' || true" "$out" || true
      fi
    done
  else
    echo "Mode audit : corrections non appliquees. Lancer en menu pour repondre oui, ou relancer avec --apply." >> "$out"
  fi

  write_f5_snapshot "APRES CORRECTION OU AUDIT" > "$after"

  {
    echo
    echo "Etat final / demo live :"
    echo '```'
    sed -n '1,180p' "$after"
    echo '```'
    echo
    echo "Preuve de travail F5 a montrer :"
    echo
    echo '```bash'
    echo "ssh root@${MACHINE_IP:-IP_VM}"
    echo "sudo ufw status verbose"
    echo "sudo fail2ban-client status sshd"
    echo '```'
    echo
    echo "Explication des mesures F5 :"
    echo
    echo "- \`ssh root@IP\` doit etre refuse : SSH est limite a \`AllowUsers oliv\`, donc root n'est pas un compte autorise en connexion distante. Le mot de passe root n'est pas modifie."
    echo "- \`ufw status verbose\` prouve que le pare-feu local est actif, avec les entrees limitees aux ports classiques utiles : SSH/22, HTTP/80 et HTTPS/443."
    echo "- \`fail2ban-client status sshd\` prouve que la jail SSH surveille les tentatives d'authentification et peut bannir les sources abusives."
  } >> "$out"

  append_timeline "Durcissement SSH, pare-feu, fail2ban et services" "sshd_config ; ufw status verbose ; fail2ban-client status"
  append_action "F5" "SSH limite a oliv, mot de passe root non modifie, ufw/fail2ban actifs" "ssh root@IP refuse ; ufw status verbose ; fail2ban-client status sshd"
  echo "F5 ecrit dans $out"
}

write_f6_snapshot() {
  local label="$1"
  local target_url="http://${MACHINE_IP:-127.0.0.1}"
  {
    echo "===== F6 $label ====="
    echo "Date : $(date '+%F %T')"
    echo "Machine : $(hostname)"
    echo "URL testee : $target_url"
    echo
    echo "## nginx -t"
    if command -v nginx >/dev/null 2>&1; then
      nginx -t 2>&1 || true
    else
      echo "nginx absent"
    fi
    echo
    echo "## systemctl status nginx"
    systemctl status nginx --no-pager 2>&1 | head -n 50 || true
    echo
    echo "## journalctl nginx"
    journalctl -u nginx --no-pager -n 50 2>&1 || true
    echo
    echo "## Ports HTTP/HTTPS en ecoute"
    ss -tulpn 2>/dev/null | awk 'NR==1 || /:80[[:space:]]|:443[[:space:]]/' || true
    echo
    echo "## Test HTTP"
    if command -v curl >/dev/null 2>&1; then
      curl -sS -I -H 'Cache-Control: no-cache' --max-time 5 "$target_url" 2>&1 || true
    else
      echo "curl absent"
    fi
  }
}

detect_f6_status() {
  local nginx_test="$STATE_DIR/f6_nginx_test.log"
  local http_code="000"
  : > "$nginx_test"

  if ! command -v nginx >/dev/null 2>&1; then
    printf '%s\t%s\t%s\n' "nginx_absent" "nginx est absent" "Installer nginx si autorise, puis configurer le site avant de tester HTTP 200."
    return
  fi

  if ! nginx -t > "$nginx_test" 2>&1; then
    local err
    err="$(tr '\n' ' ' < "$nginx_test" | sed 's/[[:space:]][[:space:]]*/ /g')"
    if grep -q 'unknown directive "invalid_ctf_directive"' "$nginx_test"; then
      local file line
      file="$(sed -nE 's#.* in (/[^:]+):([0-9]+).*#\1#p' "$nginx_test" | head -1)"
      line="$(sed -nE 's#.* in (/[^:]+):([0-9]+).*#\2#p' "$nginx_test" | head -1)"
      printf '%s\t%s\t%s\n' "config_invalid_ctf_directive" "$err" "Commenter la ligne $line dans $file puis relancer nginx -t et systemctl restart nginx."
      return
    fi
    printf '%s\t%s\t%s\n' "config_invalide" "$err" "Corriger le fichier indique par nginx -t, relancer nginx -t, puis redemarrer nginx."
    return
  fi

  if ! systemctl is-active nginx >/dev/null 2>&1; then
    printf '%s\t%s\t%s\n' "service_inactif" "nginx -t est OK mais le service nginx n'est pas actif" "systemctl restart nginx"
    return
  fi

  if command -v curl >/dev/null 2>&1; then
    http_code="$(curl -sS -H 'Cache-Control: no-cache' -o /dev/null -w '%{http_code}' --max-time 5 "http://${MACHINE_IP:-127.0.0.1}" 2>/dev/null || true)"
    http_code="${http_code:-000}"
  fi

  if [ "$http_code" = "200" ]; then
    printf '%s\t%s\t%s\n' "ok" "nginx actif et HTTP 200 obtenu" "Aucune correction necessaire."
  else
    printf '%s\t%s\t%s\n' "http_non_200" "nginx actif mais curl retourne HTTP $http_code" "Verifier server_name, root/index, site enabled, pare-feu et vhost par defaut."
  fi
}

confirm_f6_apply() {
  if [ "$APPLY" -eq 1 ]; then
    return 0
  fi
  if [ "$INTERACTIVE" -eq 1 ]; then
    local answer
    read -r -p "Appliquer la correction F6 proposee maintenant ? [oui/non] : " answer
    [ "$answer" = "oui" ]
    return
  fi
  return 1
}

write_f6_possible_corrections() {
  local status="$1"
  local reason="$2"
  local proposal="$3"
  local target_url="http://${MACHINE_IP:-127.0.0.1}"
  local nginx_test="$STATE_DIR/f6_nginx_test.log"
  local file=""
  local line=""

  if [ -s "$nginx_test" ]; then
    file="$(sed -nE 's#.* in (/[^:]+):([0-9]+).*#\1#p' "$nginx_test" | head -1)"
    line="$(sed -nE 's#.* in (/[^:]+):([0-9]+).*#\2#p' "$nginx_test" | head -1)"
  fi

  echo "Erreurs detectees F6 :"
  echo "- Statut : $status"
  echo "- Detail : $reason"
  echo
  echo "Corrections possibles :"
  case "$status" in
    config_invalid_ctf_directive)
      echo "- Sauvegarder le fichier Nginx concerne."
      echo "- Commenter la directive CTF invalide."
      echo "- Retester la configuration puis redemarrer Nginx."
      echo
      echo "Commandes proposees :"
      echo "sudo cp -n ${file:-/etc/nginx/nginx.conf} ${file:-/etc/nginx/nginx.conf}.ctf-f6.bak"
      if [ -n "$line" ]; then
        echo "sudo sed -i '${line}s/^/# CTF F6 correction: /' ${file:-/etc/nginx/nginx.conf}"
      else
        echo "sudo sed -i '/invalid_ctf_directive/s/^/# CTF F6 correction: /' /etc/nginx/nginx.conf"
      fi
      echo "sudo nginx -t"
      echo "sudo systemctl restart nginx"
      echo "curl -I -H 'Cache-Control: no-cache' $target_url"
      ;;
    config_invalide)
      echo "- Lire l'erreur exacte de nginx -t."
      echo "- Corriger le fichier et la ligne indiques par Nginx."
      echo "- Ne pas redemarrer tant que nginx -t echoue."
      echo
      echo "Commandes proposees :"
      echo "sudo nginx -t"
      if [ -n "$file" ]; then
        echo "sudo cp -n $file $file.ctf-f6.bak"
        echo "sudo nano +${line:-1} $file"
      else
        echo "sudo nano /etc/nginx/nginx.conf"
      fi
      echo "sudo nginx -t"
      echo "sudo systemctl restart nginx"
      ;;
    service_inactif)
      echo "- La configuration est valide, mais le service est arrete."
      echo "- Redemarrer Nginx puis verifier HTTP."
      echo
      echo "Commandes proposees :"
      echo "sudo nginx -t"
      echo "sudo systemctl restart nginx"
      echo "sudo systemctl status nginx --no-pager"
      echo "curl -I -H 'Cache-Control: no-cache' $target_url"
      ;;
    http_non_200)
      echo "- Nginx tourne, mais le code HTTP n'est pas 200."
      echo "- Verifier le vhost actif, le root/index, le pare-feu et le site par defaut."
      echo
      echo "Commandes proposees :"
      echo "sudo nginx -T | sed -n '1,220p'"
      echo "ls -l /etc/nginx/sites-enabled /var/www /var/www/html 2>/dev/null"
      echo "sudo ufw status verbose"
      echo "curl -I -H 'Cache-Control: no-cache' $target_url"
      ;;
    nginx_absent)
      echo "- Installer Nginx si le scenario CTF l'autorise."
      echo "- Activer le service et retester HTTP 200."
      echo
      echo "Commandes proposees :"
      echo "sudo apt-get update"
      echo "sudo apt-get install -y nginx"
      echo "sudo systemctl enable --now nginx"
      echo "curl -I -H 'Cache-Control: no-cache' $target_url"
      ;;
    ok)
      echo "- Aucune correction necessaire."
      echo "- Conserver la preuve curl HTTP 200."
      ;;
    *)
      echo "- $proposal"
      ;;
  esac
}

fix_f6_invalid_ctf_directive() {
  local out="$1"
  local nginx_test="$STATE_DIR/f6_nginx_test.log"
  local file line current

  file="$(sed -nE 's#.* in (/[^:]+):([0-9]+).*#\1#p' "$nginx_test" | head -1)"
  line="$(sed -nE 's#.* in (/[^:]+):([0-9]+).*#\2#p' "$nginx_test" | head -1)"

  if [ -z "$file" ] || [ -z "$line" ]; then
    echo "Impossible d'extraire le fichier/ligne depuis nginx -t." >> "$out"
    return 1
  fi
  if [ ! -f "$file" ]; then
    echo "Fichier Nginx introuvable : $file" >> "$out"
    return 1
  fi

  current="$(sed -n "${line}p" "$file")"
  {
    echo "Fichier cible : $file"
    echo "Ligne cible : $line"
    echo "Contenu avant : $current"
  } >> "$out"

  if ! printf '%s\n' "$current" | grep -q 'invalid_ctf_directive'; then
    echo "Securite : la ligne cible ne contient pas invalid_ctf_directive, correction annulee." >> "$out"
    return 1
  fi

  run_cmd "cp -n '$file' '$file.ctf-f6.bak'" "$out" || true
  run_cmd "sed -i '${line}s/^/# CTF F6 correction: /' '$file'" "$out"
  run_cmd "nginx -t" "$out"
  run_cmd "systemctl restart nginx" "$out"
}

task_f6() {
  local out="$FLAGS_DIR/F6.txt"
  local before="$FLAGS_DIR/F6_avant.txt"
  local after="$FLAGS_DIR/F6_apres.txt"
  local status_file="$STATE_DIR/f6_status.tsv"
  local status reason proposal correction code

  write_f6_snapshot "AVANT CORRECTION" > "$before"
  detect_f6_status > "$status_file"
  IFS=$'\t' read -r status reason proposal < "$status_file"
  correction="$proposal"

  write_header "$out" "F6 - Remise en service Nginx"
  {
    echo "Objectif : corriger Nginx et obtenir un HTTP 200."
    echo
    echo "Rapport avant correction : $before"
    echo "Rapport apres correction : $after"
    echo
    echo "Erreur / etat detecte : $reason"
    echo "Correction proposee : $proposal"
    echo
    write_f6_possible_corrections "$status" "$reason" "$proposal"
    echo
    echo "Diagnostic avant correction :"
    echo '```'
    sed -n '1,180p' "$before"
    echo '```'
    echo
  } >> "$out"

  if [ "$INTERACTIVE" -eq 1 ]; then
    echo
    write_f6_possible_corrections "$status" "$reason" "$proposal"
    echo
  fi

  if [ "$status" = "ok" ]; then
    echo "Aucune correction F6 necessaire : HTTP 200 deja obtenu." >> "$out"
  elif [ "$status" = "nginx_absent" ]; then
    echo "Correction automatique non appliquee : nginx est absent." >> "$out"
  elif [ "$(id -u)" -ne 0 ]; then
    echo "F6 doit etre applique en root pour redemarrer nginx." >> "$out"
  elif [ "$status" = "service_inactif" ] && confirm_f6_apply ; then
    echo "Application de la correction F6 : $proposal" >> "$out"
    run_cmd "nginx -t" "$out"
    run_cmd "systemctl restart nginx" "$out"
  elif [ "$status" = "config_invalid_ctf_directive" ] && confirm_f6_apply ; then
    echo "Application de la correction F6 : $proposal" >> "$out"
    fix_f6_invalid_ctf_directive "$out" || true
  elif [ "$status" = "config_invalid_ctf_directive" ]; then
    echo "Correction automatique disponible mais non appliquee : relancer avec --apply ou repondre oui en mode menu." >> "$out"
  elif [ "$status" = "config_invalide" ]; then
    echo "Correction automatique non appliquee : nginx -t indique une configuration invalide a corriger dans le fichier signale." >> "$out"
  elif [ "$status" = "http_non_200" ]; then
    echo "Correction automatique non appliquee : le service tourne mais HTTP n'est pas 200, verifier le vhost/site avant modification." >> "$out"
  else
    echo "Mode audit : lancer en menu pour appliquer la correction proposee, ou relancer avec --apply." >> "$out"
  fi

  write_f6_snapshot "APRES CORRECTION OU AUDIT" > "$after"
  code="000"
  if command -v curl >/dev/null 2>&1; then
    code="$(curl -sS -H 'Cache-Control: no-cache' -o /dev/null -w '%{http_code}' --max-time 5 "http://${MACHINE_IP:-127.0.0.1}" 2>/dev/null || true)"
    code="${code:-000}"
  fi
  save_state "f6_correction" "$correction"
  save_state "f6_http_code" "$code"
  {
    echo "Correction documentee : $correction"
    echo "Code HTTP obtenu : $code"
    echo "Commande : curl -H 'Cache-Control: no-cache' -I http://${MACHINE_IP:-127.0.0.1}"
    echo
    echo "Diagnostic apres correction/audit :"
    echo '```'
    sed -n '1,180p' "$after"
    echo '```'
  } >> "$out"

  append_timeline "Verification et remise en service Nginx" "nginx -t ; systemctl restart nginx ; curl HTTP $code"
  append_action "F6" "Correction Nginx : $correction" "curl http://${MACHINE_IP:-127.0.0.1} retourne HTTP $code"
  echo "F6 ecrit dans $out"
}

write_f7_proposals() {
  local archive="$1"
  local checksum="$2"
  cat <<EOF
Sauvegarde proposee pour F7 :
- Creer le dossier /backup si besoin.
- Archiver /etc et /var/www dans : $archive
- Generer le checksum : $checksum
- Verifier l'integrite avec sha256sum -c.

Commandes proposees :
sudo mkdir -p /backup
sudo tar -C / -czf '$archive' etc var/www
sudo sha256sum '$archive' > '$checksum'
sudo sha256sum -c '$checksum'
EOF
}

confirm_f7_create() {
  if [ "$APPLY" -eq 1 ]; then
    return 0
  fi
  if [ "$INTERACTIVE" -eq 1 ]; then
    local answer
    read -r -p "Creer la sauvegarde F7 maintenant ? [oui/non] : " answer
    [ "$answer" = "oui" ]
    return
  fi
  return 1
}

task_f7() {
  local out="$FLAGS_DIR/F7.txt"
  write_header "$out" "F7 - Sauvegarde /etc et /var/www"
  if [ "$(id -u)" -ne 0 ]; then
    echo "F7 necessite root pour sauvegarder /etc et /var/www." >> "$out"
    append_action "F7" "Sauvegarde non creee : execution non-root" "relancer avec sudo"
    return
  fi

  local backup_dir="/backup"
  local archive="$backup_dir/ctf-alpesnet-$RUN_ID.tar.gz"
  local checksum="$archive.sha256"
  {
    echo "Objectif : sauvegarder /etc et /var/www puis generer un checksum sha256."
    echo "Archive cible : $archive"
    echo "Checksum cible : $checksum"
    echo
    write_f7_proposals "$archive" "$checksum"
    echo
  } >> "$out"

  if [ "$INTERACTIVE" -eq 1 ]; then
    echo
    write_f7_proposals "$archive" "$checksum"
    echo
  fi

  if confirm_f7_create ; then
    echo "Creation de la sauvegarde F7." >> "$out"
    [ "$DRY_RUN" -eq 1 ] || mkdir -p "$backup_dir"
    run_cmd "tar -C / -czf '$archive' etc var/www" "$out"
    run_cmd "sha256sum '$archive' > '$checksum'" "$out"
    run_cmd "sha256sum -c '$checksum'" "$out"
  else
    echo "Mode audit : sauvegarde non creee. Repondre oui en mode menu ou relancer avec --apply." >> "$out"
  fi

  {
    echo
    echo "Preuve attendue :"
    echo "Archive : $archive"
    echo "Checksum : $checksum"
    [ -s "$checksum" ] && cat "$checksum"
  } >> "$out"

  save_state "f7_archive" "$archive"
  save_state "f7_checksum" "$checksum"
  append_timeline "Sauvegarde de /etc et /var/www avec checksum" "tar -C / ; sha256sum -c"
  append_action "F7" "Sauvegarde creee : $archive" "sha256sum -c $checksum"
  echo "F7 ecrit dans $out"
}

print_f8_timeline() {
  if [ ! -s "$STATE_DIR/timeline.tsv" ]; then
    echo "   [Heure estimee]  [Evenement identifie]  [Source : fichier/commande]"
    return
  fi

  awk -F '\t' '
    /Acces root/ { f1=$0 }
    /Audit des comptes/ { f2=$0 }
    /Analyse des logs/ { f3=$0 }
    /Recherche des permissions/ { f4=$0 }
    /Durcissement SSH/ { f5=$0 }
    /Verification et remise en service Nginx/ { f6=$0 }
    /Sauvegarde de \/etc et \/var\/www/ { f7=$0 }
    function print_row(row) {
      if (row != "") {
        split(row, item, FS)
        printf "   %s  %s  [Source : %s]\n", item[1], item[2], item[3]
      }
    }
    END {
      print_row(f1)
      print_row(f2)
      print_row(f3)
      print_row(f4)
      print_row(f5)
      print_row(f6)
      print_row(f7)
    }
  ' "$STATE_DIR/timeline.tsv"
}

print_f8_latest_actions() {
  if [ ! -s "$STATE_DIR/actions.tsv" ]; then
    return
  fi

  awk -F '\t' '
    { latest[$1]=$0 }
    function print_action(flag) {
      if (latest[flag] != "") {
        split(latest[flag], item, FS)
        printf "   %s -- %s | Verification : %s\n", item[1], item[2], item[3]
      }
    }
    END {
      print_action("F1")
      print_action("F2")
      print_action("F3")
      print_action("F4")
      print_action("F5")
      print_action("F6")
      print_action("F7")
    }
  ' "$STATE_DIR/actions.tsv"
}

print_f8_file_block() {
  local title="$1"
  local file="$2"

  echo "### $title"
  echo
  if [ -s "$file" ]; then
    echo '~~~text'
    cat "$file"
    echo '~~~'
  else
    echo "Fichier non disponible : $file"
  fi
  echo
}

print_f8_step_by_step() {
  echo "## 6. DETAIL STEP BY STEP DES FLAGS"
  echo
  echo "Cette section centralise les preuves dans le rapport final, comme demande par le formateur."
  echo

  print_f8_file_block "F1 - Acces root" "$FLAGS_DIR/F1.txt"
  print_f8_file_block "F2 - Compte non autorise : audit, explication et resultat" "$FLAGS_DIR/F2.txt"
  print_f8_file_block "F3 - IP source de l'intrusion" "$FLAGS_DIR/F3.txt"
  print_f8_file_block "F4 - Permissions dangereuses et SUID" "$FLAGS_DIR/F4.txt"
  print_f8_file_block "F5 - Durcissement : synthese et explication des mesures" "$FLAGS_DIR/F5.txt"
  print_f8_file_block "F5 - Etat avant correction" "$FLAGS_DIR/F5_avant.txt"
  print_f8_file_block "F5 - Etat apres correction ou audit" "$FLAGS_DIR/F5_apres.txt"
  print_f8_file_block "F6 - Remise en service Nginx" "$FLAGS_DIR/F6.txt"
  print_f8_file_block "F7 - Sauvegarde et checksum" "$FLAGS_DIR/F7.txt"
}

task_f8() {
  local out="$FLAGS_DIR/rapport_${PRENOM}.txt"
  local out_md="$FLAGS_DIR/rapport_${PRENOM}.md"
  local ip="${MACHINE_IP:-$(hostname -I 2>/dev/null | awk '{print $1}')}"
  {
    echo "# ============================================================"
    echo "# Auteur : $PRENOM -- Date : $REPORT_DATE"
    echo "# Machine : VM CTF AlpesNet -- IP : ${ip:-A completer} -- Module : SYS-01a CTF"
    echo "# ============================================================"
    echo
    echo "1. TIMELINE DE L'INCIDENT"
    print_f8_timeline
    echo
    echo "2. ANALYSE DES CAUSES"
    echo "   Cause principale    : compte ou service expose ayant permis une compromission de la VM."
    echo "   Vecteur d'intrusion : $(read_state f3_ip "IP source a confirmer") via SSH ou service expose, a confirmer avec les logs."
    echo "   Compte suspect      : $(read_state f2_account "compte a confirmer")"
    echo "   Permission faible   : $(read_state f4_path "chemin a confirmer")"
    echo
    echo "3. ACTIONS CORRECTIVES"
    echo "   F1 -- Acces root       : $(read_state f1_method "methode a completer")"
    echo "   F2 -- Compte supprime  : userdel $(read_state f2_account "[compte]") + verification getent passwd"
    echo "   F4 -- Permissions      : chmod $(read_state f4_mode "X") $(read_state f4_path "[fichier]") + verification stat"
    echo "   F5 -- SSH              : AllowUsers oliv, PasswordAuthentication yes, PubkeyAuthentication yes, PermitEmptyPasswords no"
    echo "   F5 -- ufw              : OpenSSH, HTTP et HTTPS autorises ; verification par ufw status verbose"
    echo "   F5 -- fail2ban         : jail sshd active, maxretry=3, bantime=3600"
    echo "   F6 -- Nginx            : $(read_state f6_correction "erreur et correction a completer")"
    echo "   F7 -- Sauvegarde       : $(read_state f7_archive "/backup/ctf-alpesnet.tar.gz") + sha256sum -c $(read_state f7_checksum "checksum a completer")"
    echo
    if [ -s "$STATE_DIR/actions.tsv" ]; then
      echo "   Dernieres actions retenues :"
      print_f8_latest_actions
      echo
    fi
    echo "4. ETAT FINAL"
    echo "   ssh oliv@${ip:-IP}           : autorise"
    echo "   ssh root@${ip:-IP}           : refuse"
    echo "   ssh autre_compte@${ip:-IP}   : refuse"
    echo "   ufw status              : regles actives a verifier avec ufw status verbose"
    echo "   fail2ban-client status  : jail sshd active a verifier"
    echo "   curl http://${ip:-IP}        : HTTP $(read_state f6_http_code "code a confirmer")"
    echo
    echo "5. RECOMMANDATIONS"
    echo "   - Limiter SSH aux comptes autorises avec AllowUsers ; basculer vers cle seule apres verification que les cles sont deployees."
    echo "   - Auditer regulierement les comptes UID 0, sudoers et shells interactifs."
    echo "   - Surveiller les logs SSH et conserver une rotation exploitable."
    echo "   - Corriger les permissions 0777/SUID injustifiees et documenter toute exception."
    echo "   - Maintenir ufw et fail2ban actifs, avec tests apres chaque changement."
    echo "   - Tester les sauvegardes et verifier les checksums, pas seulement creer les archives."
    echo
    print_f8_step_by_step
  } > "$out"
  cp "$out" "$out_md"

  echo "F8 ecrit dans $out"
  echo "Version Markdown ecrite dans $out_md"
}

describe_task() {
  local task="$1"
  live_section "$task - prerequis, actions et validation"
  case "$task" in
    F1)
      live_info "Prerequis : etre connecte sur la VM CTF et pouvoir tester id/whoami/sudo -l."
      live_info "Action : chercher investigateur/backdoor-sys/Inv3st1g4t3ur!, controler su/root et verifier aussi SSH root."
      live_info "Validation : presence de F1.txt, methode d'escalade renseignee, et preuve des commandes rejouables."
      ;;
    F2)
      live_info "Prerequis : acces lecture a /etc/passwd, /etc/sudoers.d et lastlog."
      live_info "Action : chercher les comptes UID 0, shells interactifs, sudoers et connexions recentes."
      live_info "Validation : compte suspect retenu dans $FLAGS_DIR/F2.txt, sans confondre avec les comptes legitimes."
      ;;
    F3)
      live_info "Prerequis : logs SSH disponibles dans /var/log/auth.log, /var/log/secure ou journalctl."
      live_info "Action : extraire les IP depuis les evenements SSH suspects et compter les occurrences."
      live_info "Validation : IP retenue dans $FLAGS_DIR/F3.txt avec extraits de logs."
      ;;
    F4)
      live_info "Prerequis : acces find/stat sur la partition racine."
      live_info "Action : rechercher 777, SUID/SGID, filtrer les chemins attendus et proposer une correction."
      live_info "Validation : chemin dangereux documente dans $FLAGS_DIR/F4.txt avec preuve stat."
      ;;
    F5)
      live_info "Prerequis : execution root pour appliquer SSH, ufw, fail2ban et services."
      live_info "Action : generer un avant/apres, afficher les corrections, demander confirmation ou utiliser --apply."
      live_info "Validation : $FLAGS_DIR/F5_avant.txt, $FLAGS_DIR/F5_apres.txt, sshd_config, ufw et fail2ban."
      ;;
    F6)
      live_info "Prerequis : nginx et curl disponibles, IP cible renseignee avec --ip si besoin."
      live_info "Action : afficher nginx -t, status/logs, corrections possibles, puis corriger si confirme."
      live_info "Validation : $FLAGS_DIR/F6_avant.txt, $FLAGS_DIR/F6_apres.txt et HTTP 200 si le service est retabli."
      ;;
    F7)
      live_info "Prerequis : execution root et espace disponible dans /backup."
      live_info "Action : proposer la sauvegarde /etc + /var/www, demander confirmation ou utiliser --apply."
      live_info "Validation : archive creee, checksum sha256 genere et sha256sum -c OK."
      ;;
    F8)
      live_info "Prerequis : etapes F1 a F7 executees ou au moins documentees dans $STATE_DIR."
      live_info "Action : generer le rapport final en .txt et .md."
      live_info "Validation : rapport present avec timeline, causes, actions, etat final et recommandations."
      ;;
    *)
      live_warn "Etape inconnue : $task"
      ;;
  esac
}

file_ok() {
  local path="$1"
  if [ -s "$path" ]; then
    live_ok "$path existe et n'est pas vide."
    return 0
  fi
  live_warn "$path absent ou vide."
  return 1
}

state_value_ok() {
  local key="$1"
  local label="$2"
  local value
  value="$(read_state "$key" "A completer")"
  if [ -n "$value" ] && [ "$value" != "A completer" ] && ! [[ "$value" =~ ^A\ completer ]]; then
    live_ok "$label : $value"
    return 0
  fi
  live_warn "$label a completer ou non detecte automatiquement."
  return 1
}

validate_task_live() {
  local task="$1"
  local ok=0
  live_section "$task - validation en direct"
  case "$task" in
    F1)
      file_ok "$FLAGS_DIR/F1.txt" || ok=1
      state_value_ok "f1_method" "Methode F1" || ok=1
      ;;
    F2)
      file_ok "$FLAGS_DIR/F2.txt" || ok=1
      state_value_ok "f2_account" "Compte suspect F2" || ok=1
      if [ -s "$STATE_DIR/f2_candidates.tsv" ]; then
        live_ok "Candidats F2 conserves dans $STATE_DIR/f2_candidates.tsv."
      else
        live_warn "Aucun candidat F2 fort conserve, controle manuel a prevoir."
      fi
      ;;
    F3)
      file_ok "$FLAGS_DIR/F3.txt" || ok=1
      state_value_ok "f3_ip" "IP source F3" || ok=1
      if [ -s "$STATE_DIR/f3_ip_counts.tsv" ]; then
        live_ok "Compteur IP disponible dans $STATE_DIR/f3_ip_counts.tsv."
      else
        live_warn "Compteur IP vide, verifier la presence des logs SSH."
      fi
      ;;
    F4)
      file_ok "$FLAGS_DIR/F4.txt" || ok=1
      state_value_ok "f4_path" "Chemin dangereux F4" || ok=1
      if [ -s "$STATE_DIR/f4_candidates.tsv" ]; then
        live_ok "Candidats F4 conserves dans $STATE_DIR/f4_candidates.tsv."
      else
        live_warn "Aucun candidat F4 conserve, controle manuel a prevoir."
      fi
      ;;
    F5)
      file_ok "$FLAGS_DIR/F5.txt" || ok=1
      file_ok "$FLAGS_DIR/F5_avant.txt" || ok=1
      file_ok "$FLAGS_DIR/F5_apres.txt" || ok=1
      if [ -r /etc/ssh/sshd_config ] && grep -Eq '^[[:space:]]*AllowUsers[[:space:]].*(^|[[:space:]])oliv([[:space:]]|$)' /etc/ssh/sshd_config; then
        live_ok "SSH : AllowUsers oliv present."
      else
        live_warn "SSH : AllowUsers oliv non confirme dans /etc/ssh/sshd_config."
      fi
      if command -v ufw >/dev/null 2>&1 && ufw status 2>/dev/null | grep -qi active; then
        live_ok "ufw actif."
      else
        live_warn "ufw non actif ou non disponible."
      fi
      if command -v fail2ban-client >/dev/null 2>&1 && fail2ban-client ping >/dev/null 2>&1; then
        live_ok "fail2ban repond au ping client."
      else
        live_warn "fail2ban ne repond pas encore, voir $FLAGS_DIR/F5_apres.txt."
      fi
      ;;
    F6)
      file_ok "$FLAGS_DIR/F6.txt" || ok=1
      file_ok "$FLAGS_DIR/F6_avant.txt" || ok=1
      file_ok "$FLAGS_DIR/F6_apres.txt" || ok=1
      local code
      code="$(read_state "f6_http_code" "000")"
      if [ "$code" = "200" ]; then
        live_ok "Nginx : HTTP 200 obtenu."
      else
        live_warn "Nginx : HTTP $code, correction ou controle manuel encore necessaire."
        ok=1
      fi
      ;;
    F7)
      file_ok "$FLAGS_DIR/F7.txt" || ok=1
      local archive checksum
      archive="$(read_state "f7_archive" "")"
      checksum="$(read_state "f7_checksum" "")"
      if [ -s "$archive" ]; then
        live_ok "Archive presente : $archive"
      else
        live_warn "Archive absente : repondre oui en menu ou relancer avec --apply."
        ok=1
      fi
      if [ -s "$checksum" ] && sha256sum -c "$checksum" >/dev/null 2>&1; then
        live_ok "Checksum valide : sha256sum -c $checksum"
      else
        live_warn "Checksum non valide ou non cree : $checksum"
        ok=1
      fi
      ;;
    F8)
      file_ok "$FLAGS_DIR/rapport_${PRENOM}.txt" || ok=1
      file_ok "$FLAGS_DIR/rapport_${PRENOM}.md" || ok=1
      if grep -q "1. TIMELINE DE L'INCIDENT" "$FLAGS_DIR/rapport_${PRENOM}.md" 2>/dev/null \
        && grep -q "5. RECOMMANDATIONS" "$FLAGS_DIR/rapport_${PRENOM}.md" 2>/dev/null \
        && grep -q "DETAIL STEP BY STEP" "$FLAGS_DIR/rapport_${PRENOM}.md" 2>/dev/null \
        && grep -q "F2 - Compte non autorise" "$FLAGS_DIR/rapport_${PRENOM}.md" 2>/dev/null \
        && grep -q "F5 - Durcissement" "$FLAGS_DIR/rapport_${PRENOM}.md" 2>/dev/null; then
        live_ok "Rapport F8 structure avec timeline, recommandations et detail step by step F2/F5."
      else
        live_warn "Rapport F8 a verifier : structure attendue incomplete."
        ok=1
      fi
      ;;
    *)
      live_ko "Etape inconnue : $task"
      ok=1
      ;;
  esac

  if [ "$ok" -eq 0 ]; then
    live_ok "$task valide pour la demo."
  else
    live_warn "$task genere des preuves, mais une verification reste a faire."
  fi
}

run_selected() {
  for task in "${TASKS[@]}"; do
    describe_task "$task"
    case "$task" in
      F1) task_f1 ;;
      F2) task_f2 ;;
      F3) task_f3 ;;
      F4) task_f4 ;;
      F5) task_f5 ;;
      F6) task_f6 ;;
      F7) task_f7 ;;
      F8) task_f8 ;;
      *) echo "Tache inconnue : $task" >&2 ;;
    esac
    validate_task_live "$task"
  done
}

menu() {
  INTERACTIVE=1
  while true; do
    cat <<MENU

CTF AlpesNet - menu step by step
1. F1 - Acces root
2. F2 - Compte non autorise
3. F3 - IP source intrusion
4. F4 - Permissions dangereuses
5. F5 - Durcissement SSH/ufw/fail2ban/services
6. F6 - Nginx HTTP 200
7. F7 - Sauvegarde + sha256sum
8. F8 - Rapport d'incident final
9. Tout executer dans l'ordre
0. Quitter
MENU
    local choice
    read -r -p "Choix : " choice
    case "$choice" in
      1|2|3|4|5|6|7|8) TASKS=("${STEP_TO_TASK[$choice]}"); run_selected ;;
      9) TASKS=(F1 F2 F3 F4 F5 F6 F7 F8); run_selected ;;
      0) break ;;
      *) echo "Choix invalide." ;;
    esac
  done
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --menu) INTERACTIVE=1 ;;
    --all) AUTO_ALL=1 ;;
    --task)
      shift
      TASKS+=("${1^^}") ;;
    --step)
      shift
      TASKS+=("${STEP_TO_TASK[$1]}") ;;
    --prenom)
      shift
      PRENOM="$1" ;;
    --ip)
      shift
      MACHINE_IP="$1" ;;
    --f1-method)
      shift
      F1_METHOD="$1" ;;
    --authorized-users)
      shift
      AUTHORIZED_USERS="$1" ;;
    --ssh-public-key)
      shift
      SSH_PUBLIC_KEY="$1" ;;
    --apply) APPLY=1 ;;
    --dry-run) DRY_RUN=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Option inconnue : $1" >&2; usage; exit 2 ;;
  esac
  shift
done

need_root_for_flags
ensure_directories

if [ "$INTERACTIVE" -eq 1 ] && [ "${#TASKS[@]}" -eq 0 ] && [ "$AUTO_ALL" -eq 0 ]; then
  menu
  echo "Termine. Les livrables sont dans $FLAGS_DIR."
  exit 0
fi

if [ "$AUTO_ALL" -eq 1 ]; then
  TASKS=(F1 F2 F3 F4 F5 F6 F7 F8)
fi

if [ "${#TASKS[@]}" -eq 0 ]; then
  echo "Aucune tache selectionnee." >&2
  usage
  exit 2
fi

run_selected
echo "Termine. Les livrables sont dans $FLAGS_DIR."
