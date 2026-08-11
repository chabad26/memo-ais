# Automatisation - Connectivité et sauvegarde AlpesNet

## Objectif

Cette feuille applique la même logique que les fiches de dépannage : on part d'un besoin clair, on écrit un script réexécutable, on garde une trace, puis on valide le résultat.

Deux sujets sont traités :

- **Sujet A** : vérifier automatiquement la connectivité d'une liste d'IPs ;
- **Sujet B** : sauvegarder automatiquement les configurations des équipements réseau.

Les fichiers de l'atelier sont regroupés dans `tools/admin-reseaux/iteration-5/` :

```text
tools/admin-reseaux/iteration-5/check_connectivity.sh
tools/admin-reseaux/iteration-5/hosts.txt
tools/admin-reseaux/iteration-5/backup_configs.sh
tools/admin-reseaux/iteration-5/equipements.txt
tools/admin-reseaux/iteration-5/backup_configs_netmiko.py
```

---

## Sujet A - Vérification de connectivité

### Besoin

Le script doit :

1. lire une liste d'IPs depuis `hosts.txt` ;
2. ignorer les lignes vides et les commentaires `#` ;
3. envoyer un ping sur chaque IP avec 1 paquet et un timeout de 2 secondes ;
4. afficher `[OK]` ou `[DOWN]` avec horodatage ;
5. sauvegarder le rapport dans un fichier daté ;
6. afficher un résumé `X UP / Y DOWN sur Z total`.

### Fichier d'entrée `hosts.txt`

```text
# Hotes AlpesNet - exemple
# Une IP par ligne. Les lignes vides et commentaires sont ignores.
192.168.10.1
192.168.20.1
192.168.30.1
192.168.40.1
203.0.113.2
```

### Script `check_connectivity.sh`

```bash
#!/usr/bin/env bash
# ============================================================
# Auteur     : Olivier
# Date       : 2026-06-04
# Version    : 1.0
# Objet      : Verification de connectivite des hotes AlpesNet
# Usage      : ./check_connectivity.sh [hosts.txt]
# Dependances: ping, date, mkdir
# ============================================================

set -uo pipefail
shopt -s extglob

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
HOSTS_FILE="${1:-${SCRIPT_DIR}/hosts.txt}"
REPORT_DIR="${REPO_ROOT}/reports"
REPORT_FILE="${REPORT_DIR}/connectivity_$(date +%Y%m%d_%H%M%S).log"
TIMEOUT=2
UP_COUNT=0
DOWN_COUNT=0
TOTAL_COUNT=0

usage() {
    printf 'Usage: %s [hosts.txt]\n' "$0" >&2
    printf 'Par defaut: %s\n' "${SCRIPT_DIR}/hosts.txt" >&2
}

clean_line() {
    local line="$1"

    line="${line%%#*}"
    line="${line##+([[:space:]])}"
    line="${line%%+([[:space:]])}"

    printf '%s\n' "$line"
}

check_host() {
    local ip="$1"
    local timestamp

    timestamp="$(date '+%Y-%m-%d %H:%M:%S')"

    if ping -c 1 -W "$TIMEOUT" "$ip" >/dev/null 2>&1; then
        printf '%s [OK]   %s\n' "$timestamp" "$ip"
        return 0
    fi

    printf '%s [DOWN] %s\n' "$timestamp" "$ip"
    return 1
}

if [[ ! -f "$HOSTS_FILE" ]]; then
    printf 'ERREUR: fichier introuvable: %s\n' "$HOSTS_FILE" >&2
    usage
    exit 1
fi

mkdir -p "$REPORT_DIR"

{
    printf '=== Rapport de connectivite AlpesNet ===\n'
    printf 'Date: %s\n' "$(date '+%Y-%m-%d %H:%M:%S')"
    printf 'Source: %s\n' "$HOSTS_FILE"
    printf '\n'
} | tee "$REPORT_FILE"

while IFS= read -r raw_line || [[ -n "$raw_line" ]]; do
    ip="$(clean_line "$raw_line")"

    [[ -z "$ip" ]] && continue

    TOTAL_COUNT=$((TOTAL_COUNT + 1))

    if result="$(check_host "$ip")"; then
        UP_COUNT=$((UP_COUNT + 1))
    else
        DOWN_COUNT=$((DOWN_COUNT + 1))
    fi

    printf '%s\n' "$result" | tee -a "$REPORT_FILE"
done < "$HOSTS_FILE"

{
    printf '\n'
    printf '=== Resume ===\n'
    printf '%d UP / %d DOWN sur %d total\n' "$UP_COUNT" "$DOWN_COUNT" "$TOTAL_COUNT"
    printf 'Rapport: %s\n' "$REPORT_FILE"
} | tee -a "$REPORT_FILE"
```

### Exécution

```bash
chmod +x tools/admin-reseaux/iteration-5/check_connectivity.sh
tools/admin-reseaux/iteration-5/check_connectivity.sh
```

Exemple de sortie attendue :

```text
2026-06-04 15:40:12 [OK]   192.168.10.1
2026-06-04 15:40:14 [DOWN] 192.168.20.1

=== Resume ===
1 UP / 1 DOWN sur 2 total
Rapport: reports/connectivity_20260604_154012.log
```

### Validation ShellCheck

Commande obligatoire :

```bash
shellcheck tools/admin-reseaux/iteration-5/check_connectivity.sh
```

Résultat attendu :

```text
aucune erreur
```

---

## Sujet B - Sauvegarde de configurations

### Besoin B

Le script doit :

1. lire une liste `equipements.txt` au format `IP NOM` ;
2. se connecter en SSH à chaque équipement ;
3. exécuter `show running-config` ;
4. sauvegarder le résultat dans `backup_NOM_YYYYMMDD.cfg` ;
5. ajouter automatiquement l'en-tête standard ;
6. afficher un résumé `X sauvegardes OK / Y erreurs`.

### Fichier d'entrée `equipements.txt`

```text
# Equipements AlpesNet - exemple
# Format: IP NOM
192.168.10.1 R1
192.168.20.1 R2
192.168.30.1 R3
192.168.40.1 R4
```

### Script Bash `backup_configs.sh`

Le script utilise la variable d'environnement `SSH_USER`. Si elle n'est pas définie, il utilise `admin`.

```bash
SSH_USER=admin tools/admin-reseaux/iteration-5/backup_configs.sh
```

Pour chaque équipement, le fichier généré suit ce modèle :

```text
reports/backups/backup_R1_20260604.cfg
```

En-tête ajouté automatiquement :

```text
! ============================================================
! ALPESNET - SAUVEGARDE CONFIGURATION EQUIPEMENT
! Equipement : R1
! Adresse IP : 192.168.10.1
! Date       : 2026-06-04 15:45:00
! Auteur     : Olivier
! Commande   : show running-config
! ============================================================
```

### Point de vigilance

Sur un vrai équipement Cisco, l'utilisateur SSH doit avoir le droit d'exécuter :

```cisco
terminal length 0
show running-config
```

`terminal length 0` évite que la configuration soit coupée par la pagination `--More--`.

---

## Profil avancé - Python avec Netmiko

### Installation

```bash
pip install netmiko --break-system-packages
```

### Exécution B

```bash
NET_USER=admin NET_PASSWORD='motdepasse' python3 tools/admin-reseaux/iteration-5/backup_configs_netmiko.py
```

### Principe

Netmiko gère la connexion SSH aux équipements réseau et simplifie l'envoi de commandes Cisco.

Le script Python reprend le même fichier `tools/admin-reseaux/iteration-5/equipements.txt`, génère le même type de fichier `backup_NOM_YYYYMMDD.cfg`, puis ajoute le même en-tête standard.

Documentation : [github.com/ktbyers/netmiko](https://github.com/ktbyers/netmiko)

---

## Résumé

| Sujet | Fichier principal | Entrée | Sortie |
| --- | --- | --- | --- |
| A - Connectivité | `tools/admin-reseaux/iteration-5/check_connectivity.sh` | `tools/admin-reseaux/iteration-5/hosts.txt` | `reports/connectivity_YYYYMMDD_HHMMSS.log` |
| B - Sauvegarde Bash | `tools/admin-reseaux/iteration-5/backup_configs.sh` | `tools/admin-reseaux/iteration-5/equipements.txt` | `reports/backups/backup_NOM_YYYYMMDD.cfg` |
| B avancé - Netmiko | `tools/admin-reseaux/iteration-5/backup_configs_netmiko.py` | `tools/admin-reseaux/iteration-5/equipements.txt` | `reports/backups/backup_NOM_YYYYMMDD.cfg` |

La validation minimale obligatoire pour le Sujet A est :

```bash
shellcheck tools/admin-reseaux/iteration-5/check_connectivity.sh
```
