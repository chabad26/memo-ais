#!/usr/bin/env bash
# TP privé dans quatre netns ; aucun nft/sysctl/routage modifié sur l’hôte.
set -euo pipefail
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
BASE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
STATE=/run/ais45-itot
NAMES=(ais45-it ais45-fw ais45-gw ais45-ot)
ACTION=${1:-help}

require_root() { [[ $EUID -eq 0 ]] || { echo 'Lancer avec sudo dans votre terminal.' >&2; exit 1; }; }
require_lab() {
    [[ -f "$STATE/base" ]] && [[ $(cat "$STATE/base") == "$BASE" ]] || { echo 'Laboratoire absent ou créé depuis un autre dossier.' >&2; exit 1; }
}
record() {
    local phase=$1
    mkdir -p "$RUN/$phase"
    for ns in "${NAMES[@]}"; do
        ip -n "$ns" -br addr > "$RUN/$phase/$ns-adresses.txt"
        ip -n "$ns" route > "$RUN/$phase/$ns-routes.txt"
        ip netns exec "$ns" ss -lnt > "$RUN/$phase/$ns-ecoutes.txt"
    done
    ip netns exec ais45-fw nft -a list ruleset > "$RUN/$phase/regles-it-ot.nft"
    ip netns exec ais45-fw nft -j list ruleset > "$RUN/$phase/regles-it-ot.json"
}
setup() {
    [[ ! -e "$STATE" ]] || { echo 'TP déjà préparé : utiliser inspect/apply/verify, ou teardown explicitement.' >&2; exit 1; }
    for ns in "${NAMES[@]}"; do
        if ip netns list | awk '{print $1}' | grep -Fxq "$ns"; then echo "Espace déjà présent : $ns ; abandon." >&2; exit 1; fi
    done
    [[ -f "$BASE/poc/lab/server.py" ]] || { echo 'Copie poc/ manquante.' >&2; exit 1; }
    for binary in ip nft python3 runuser ss sysctl; do command -v "$binary" >/dev/null; done
    local owner=${SUDO_USER:-root}
    RUN="$BASE/evidence/run-$(date -u +%Y%m%dT%H%M%SZ)"
    mkdir -p "$STATE" "$RUN"
    printf '%s\n' "$BASE" > "$STATE/base"
    printf '%s\n' "$RUN" > "$STATE/run"
    printf '%s\n' "$owner" > "$STATE/owner"
    cp -- "$BASE/filtrage-it-ot.nft" "$RUN/filtrage-source.nft"
    date -u --iso-8601=seconds > "$RUN/preparation-date-utc.txt"
    # La sauvegarde hôte est en lecture seule et ne sera jamais rechargée par le script.
    nft -a list ruleset > "$RUN/hote-avant.nft"
    ip -br addr > "$RUN/hote-adresses-avant.txt"
    ip route > "$RUN/hote-routes-avant.txt"
    for ns in "${NAMES[@]}"; do
        ip netns add "$ns"
        ip -n "$ns" link set lo up
        ip netns exec "$ns" sysctl -qw net.ipv4.ip_forward=0
        ip netns exec "$ns" sysctl -qw net.ipv6.conf.all.disable_ipv6=1 net.ipv6.conf.default.disable_ipv6=1
    done
    # Les paires veth sont créées dans les espaces, pas sur enp1s0.
    ip -n ais45-it link add it0 type veth peer name fw-it netns ais45-fw
    ip -n ais45-gw link add dmz0 type veth peer name fw-dmz netns ais45-fw
    ip -n ais45-ot link add ot0 type veth peer name fw-ot netns ais45-fw
    ip -n ais45-it addr add 10.77.10.2/24 dev it0
    ip -n ais45-gw addr add 10.77.20.2/24 dev dmz0
    ip -n ais45-ot addr add 10.77.30.2/24 dev ot0
    ip -n ais45-fw addr add 10.77.10.1/24 dev fw-it
    ip -n ais45-fw addr add 10.77.20.1/24 dev fw-dmz
    ip -n ais45-fw addr add 10.77.30.1/24 dev fw-ot
    for spec in 'ais45-it it0' 'ais45-gw dmz0' 'ais45-ot ot0' 'ais45-fw fw-it' 'ais45-fw fw-dmz' 'ais45-fw fw-ot'; do
        read -r ns iface <<< "$spec"; ip -n "$ns" link set "$iface" up
    done
    ip -n ais45-it route add default via 10.77.10.1
    ip -n ais45-gw route add default via 10.77.20.1
    ip -n ais45-ot route add default via 10.77.30.1
    ip netns exec ais45-fw sysctl -qw net.ipv4.ip_forward=1
    (
        cd "$BASE/poc"
        nohup ip netns exec ais45-ot runuser -u "$owner" -- env PYTHONDONTWRITEBYTECODE=1 python3 -u -m lab.server --host 10.77.30.2 --port 15020 < /dev/null > "$RUN/server.log" 2>&1 &
        echo "$!" > "$STATE/server-launch.pid"
        nohup ip netns exec ais45-gw runuser -u "$owner" -- env PYTHONDONTWRITEBYTECODE=1 python3 -u -m lab.gateway --listen-host 10.77.20.2 --listen-port 15021 --upstream-host 10.77.30.2 --upstream-port 15020 < /dev/null > "$RUN/gateway.log" 2>&1 &
        echo "$!" > "$STATE/gateway-launch.pid"
        nohup ip netns exec ais45-gw runuser -u "$owner" -- env PYTHONDONTWRITEBYTECODE=1 python3 -u -m lab.dashboard --host 10.77.20.2 --port 18080 --plc-host 10.77.20.2 --plc-port 15021 < /dev/null > "$RUN/dashboard.log" 2>&1 &
        echo "$!" > "$STATE/dashboard-launch.pid"
    )
    local ready=0
    for _ in {1..40}; do
        if ip netns exec ais45-ot python3 -c 'import socket; socket.create_connection(("10.77.30.2",15020),.2).close()' 2>/dev/null && ip netns exec ais45-gw python3 -c 'import socket; socket.create_connection(("10.77.20.2",15021),.2).close()' 2>/dev/null && ip netns exec ais45-gw python3 -c 'import socket; socket.create_connection(("10.77.20.2",18080),.2).close()' 2>/dev/null; then ready=1; break; fi
        sleep .1
    done
    [[ $ready == 1 ]] || { echo "Démarrage incomplet ; examiner $RUN puis teardown si nécessaire." >&2; exit 1; }
    record avant
    python3 "$BASE/verify.py" --phase before --poc "$BASE/poc" --output "$RUN/baseline.json"
    echo "Préparation isolée terminée. Preuves : $RUN"
}
apply() {
    require_lab; RUN=$(cat "$STATE/run")
    local batch="$RUN/chargement.nft"
    if ip netns exec ais45-fw nft list table inet ais45 >/dev/null 2>&1; then
        printf 'delete table inet ais45\n' > "$batch"
    else : > "$batch"; fi
    cat "$BASE/filtrage-it-ot.nft" >> "$batch"
    ip netns exec ais45-fw nft -c -f "$batch"
    ip netns exec ais45-fw nft -f "$batch"
    record apres-application
    echo 'Filtrage appliqué uniquement dans ais45-fw.'
}
verify() {
    require_lab; RUN=$(cat "$STATE/run")
    # Sans la table active, ne pas présenter un simple défaut de service comme un refus.
    ip netns exec ais45-fw nft list table inet ais45 >/dev/null
    local verification_status=0
    python3 "$BASE/verify.py" --phase after --poc "$BASE/poc" --output "$RUN/verification.json" || verification_status=$?
    record apres-tests
    nft -a list ruleset > "$RUN/hote-apres.nft"
    ip -br addr > "$RUN/hote-adresses-apres.txt"
    ip route > "$RUN/hote-routes-apres.txt"
    if cmp -s "$RUN/hote-avant.nft" "$RUN/hote-apres.nft"; then
        echo 'Ruleset hôte inchangé entre les relevés.' | tee "$RUN/comparaison-hote.txt"
    else
        echo 'Ruleset hôte différent : examiner les relevés (aucune commande de modification hôte dans ce script).' | tee "$RUN/comparaison-hote.txt"
    fi
    cp -- "$RUN/apres-tests/regles-it-ot.nft" "$RUN/regles-it-ot.nft"
    echo "Export réel et résultats : $RUN"
    return "$verification_status"
}
inspect() { require_lab; RUN=$(cat "$STATE/run"); record inspection; echo "$RUN"; }
reset_filter() {
    require_lab
    if ip netns exec ais45-fw nft list table inet ais45 >/dev/null 2>&1; then ip netns exec ais45-fw nft delete table inet ais45; fi
    echo 'Table ais45 retirée uniquement du pare-feu isolé ; la référence initiale était vide. Accès directs redevenus possibles dans le TP privé.'
}
teardown() {
    require_lab
    for ns in "${NAMES[@]}"; do
        if ip netns list | awk '{print $1}' | grep -Fxq "$ns"; then
            mapfile -t pids < <(ip netns pids "$ns")
            if ((${#pids[@]})); then kill -- "${pids[@]}" 2>/dev/null || true; fi
        fi
    done
    sleep .2
    for ns in "${NAMES[@]}"; do
        if ip netns list | awk '{print $1}' | grep -Fxq "$ns"; then
            mapfile -t pids < <(ip netns pids "$ns")
            if ((${#pids[@]})); then kill -KILL -- "${pids[@]}" 2>/dev/null || true; fi
            ip netns del "$ns"
        fi
    done
    rm -r -- "$STATE"
    echo 'Espaces ais45 supprimés, modèle arrêté. Dossier evidence conservé.'
}
case "$ACTION" in
 all) require_root; setup; apply; verify ;;
 setup) require_root; setup ;;
 apply) require_root; apply ;;
 verify) require_root; verify ;;
 inspect) require_root; inspect ;;
 reset-filter) require_root; reset_filter ;;
 teardown) require_root; teardown ;;
 *) echo 'Usage : sudo bash lab-it-ot.sh {all|setup|apply|verify|inspect|reset-filter|teardown}'; exit 0 ;;
esac
