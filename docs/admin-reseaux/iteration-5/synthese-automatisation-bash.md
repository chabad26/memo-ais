# Synthèse · Automatisation Bash pour l'administration réseau

## Contexte — Pourquoi automatiser ?

Un administrateur réseau répète régulièrement les mêmes tâches :

- vérifier que 50 équipements sont accessibles avec `ping` ;
- sauvegarder la configuration de 10 routeurs avant une mise à jour ;
- générer un rapport de l'état du réseau chaque matin.

Chaque tâche manuelle est une opportunité d'erreur humaine : oublier un équipement, copier la mauvaise IP, lancer une commande dans le mauvais ordre.

Un script apporte trois avantages :

| Avantage | Explication |
|---|---|
| Fiable | Les mêmes commandes sont exécutées dans le même ordre à chaque lancement |
| Reproductible | Un collègue peut l'exécuter sans refaire toute la procédure à la main |
| Traçable | Le script peut être versionné avec Git, commenté et audité |

## Variables et substitution

Une variable permet de stocker une valeur réutilisable.

```bash
IP="192.168.10.1"
TIMEOUT=3

echo "Test de connectivité vers $IP"
```

Bonnes pratiques :

- mettre les variables entre guillemets : `"$IP"` ;
- utiliser des noms explicites : `TIMEOUT`, `HOSTS_FILE`, `LOG_FILE` ;
- éviter les valeurs codées partout dans le script.

## Structures de contrôle

### Condition

```bash
if ping -c 1 -W "$TIMEOUT" "$IP" &>/dev/null; then
    echo "UP"
else
    echo "DOWN"
fi
```

Lecture :

- si le `ping` réussit, le code de retour vaut `0` et le bloc `then` s'exécute ;
- sinon, le bloc `else` s'exécute ;
- `&>/dev/null` masque la sortie standard et les erreurs pour ne garder que le résultat.

### Boucle sur un fichier

```bash
while IFS= read -r ligne; do
    echo "Traitement : $ligne"
done < fichier.txt
```

Cette structure est utile pour lire une liste d'équipements, une IP par ligne.

### Boucle `for`

```bash
for ip in 192.168.10.1 192.168.10.2 192.168.10.3; do
    ping -c 1 "$ip" && echo "OK" || echo "KO"
done
```

Cette forme est pratique pour une petite liste connue à l'avance.

## Fonctions

Une fonction regroupe une action réutilisable.

```bash
check_host() {
    local ip="$1"

    if ping -c 1 -W 2 "$ip" &>/dev/null; then
        echo "[OK]   $ip"
        return 0
    else
        echo "[DOWN] $ip"
        return 1
    fi
}

check_host "192.168.10.1"
```

Points importants :

- `local ip="$1"` récupère le premier argument donné à la fonction ;
- `return 0` signifie succès ;
- `return 1` signifie erreur ou échec.

## Codes de retour

Toute commande renvoie un code de retour :

- `0` = succès ;
- autre valeur = erreur ou résultat négatif.

```bash
ping -c 1 192.168.10.1
echo "Code retour : $?"
```

Exemple :

- ping OK → code retour `0` ;
- timeout ou hôte injoignable → code retour différent de `0`.

Directive utile :

```bash
set -e
```

`set -e` arrête le script à la première erreur non gérée. Dans un script professionnel, on utilise souvent une version plus stricte :

```bash
set -euo pipefail
```

| Option | Rôle |
|---|---|
| `-e` | arrêter le script en cas d'erreur non gérée |
| `-u` | refuser les variables non définies |
| `pipefail` | faire échouer un pipeline si une commande du pipeline échoue |

## Structure d'un script Bash professionnel

```bash
#!/bin/bash
# ============================================================
# Auteur     : [Prénom NOM]
# Date       : [YYYY-MM-DD]
# Version    : 1.0
# Objet      : Vérification de connectivité des équipements AlpesNet
# Usage      : ./check_connectivity.sh [fichier_hosts]
# Dépendances: ping (standard Ubuntu)
# ============================================================

set -euo pipefail

# --- Variables de configuration ---
HOSTS_FILE="${1:-hosts.txt}"
LOG_DIR="/var/log/alpesnet"
LOG_FILE="${LOG_DIR}/check_$(date +%Y%m%d_%H%M).log"
TIMEOUT=3
OK_COUNT=0
DOWN_COUNT=0

# --- Vérification des prérequis ---
if [ ! -f "$HOSTS_FILE" ]; then
    echo "ERREUR : Fichier $HOSTS_FILE introuvable." >&2
    echo "Usage : $0 [fichier_hosts]" >&2
    exit 1
fi

mkdir -p "$LOG_DIR"

# --- Fonctions ---
check_host() {
    local ip="$1"
    local timestamp

    timestamp=$(date +%H:%M:%S)

    if ping -c 1 -W "$TIMEOUT" "$ip" &>/dev/null; then
        echo "$timestamp [OK]   $ip"
        ((OK_COUNT++)) || true
    else
        echo "$timestamp [DOWN] $ip"
        ((DOWN_COUNT++)) || true
    fi
}

# --- Exécution ---
echo "=== Vérification réseau AlpesNet — $(date) ===" | tee "$LOG_FILE"

while IFS= read -r line; do
    [[ -z "$line" || "$line" == \#* ]] && continue
    check_host "$line" | tee -a "$LOG_FILE"
done < "$HOSTS_FILE"

# --- Résumé ---
TOTAL=$((OK_COUNT + DOWN_COUNT))

echo "===========================================" | tee -a "$LOG_FILE"
echo "Résultat : $OK_COUNT/$TOTAL UP · $DOWN_COUNT DOWN" | tee -a "$LOG_FILE"
echo "Log : $LOG_FILE"
```

## Exemple de fichier `hosts.txt`

```text
# Routeurs AlpesNet
192.168.10.1
192.168.20.1
192.168.30.1

# Serveurs
192.168.10.5
192.168.10.10
```

Les lignes vides et les commentaires commençant par `#` sont ignorés.

## Points de vigilance

| Point | Pourquoi c'est important |
|---|---|
| Guillemets autour des variables | Évite les erreurs avec les espaces ou valeurs vides |
| `stderr` avec `>&2` | Sépare les erreurs de la sortie normale |
| Fichier de log | Permet de prouver le résultat et de garder une trace |
| Une fonction par action | Rend le script plus lisible et réutilisable |
| Une modification à la fois | Facilite le diagnostic si le script échoue |

## Ressources Bash

- `man bash` — référence complète
- [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)
- [ShellCheck](https://www.shellcheck.net/) — validateur de scripts
- [Explainshell](https://explainshell.com/) — explication de commandes shell
- [Netmiko](https://github.com/ktbyers/netmiko) — automatisation SSH vers équipements réseau en Python
