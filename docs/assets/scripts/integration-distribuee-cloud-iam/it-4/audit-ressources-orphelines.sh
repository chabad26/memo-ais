#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  audit-ressources-orphelines.sh openstack <OS_CLOUD>

Ce script est en lecture seule. Il liste des ressources probablement
orphelines, mais ne supprime rien.
EOF
}

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    printf 'Commande introuvable: %s\n' "$1" >&2
    exit 127
  fi
}

show_openstack_clouds() {
  printf '\n## Profils OpenStack disponibles\n' >&2
  if ! openstack cloud list >&2; then
    printf 'Impossible de lire les profils OpenStack. Verifier ~/.config/openstack/clouds.yaml.\n' >&2
  fi
}

check_openstack_cloud() {
  local cloud_name="$1"

  if openstack --os-cloud "$cloud_name" configuration show >/dev/null 2>&1; then
    return 0
  fi

  printf 'Profil OpenStack introuvable ou illisible: %s\n' "$cloud_name" >&2
  show_openstack_clouds
  printf '\nConseil: utiliser le nom exact de la colonne "Name".\n' >&2
  printf 'Chez Infomaniak, il ressemble souvent a PCP-XXXXXXX-dc3-a ou PCP-XXXXXXX-dc4-a.\n' >&2
  printf 'Ne pas utiliser le nom court du projet ni le nom utilisateur PCU-XXXXXXX.\n' >&2
  exit 2
}

audit_openstack() {
  local cloud_name="$1"
  need_cmd openstack
  check_openstack_cloud "$cloud_name"

  printf '# Audit OpenStack - profil %s\n' "$cloud_name"
  date -Is
  printf '\n## Instances\n'
  openstack --os-cloud "$cloud_name" server list || true

  printf '\n## Volumes probablement orphelins: status available\n'
  openstack --os-cloud "$cloud_name" volume list --status available || true

  printf '\n## IP publiques: verifier la colonne Port\n'
  openstack --os-cloud "$cloud_name" floating ip list || true

  printf '\n## Snapshots de volume: verifier age et utilite\n'
  openstack --os-cloud "$cloud_name" volume snapshot list || true

  printf '\n## Rappel\n'
  printf 'Verifier chaque ressource avant suppression: inventaire Ansible, etat OpenTofu, sauvegardes, dependances applicatives.\n'
}

main() {
  if [[ "${1:-}" == "-h" || "${1:-}" == "--help" || "${1:-}" == "help" ]]; then
    usage
    exit 0
  fi

  if [[ $# -ne 2 ]]; then
    usage >&2
    exit 2
  fi

  case "$1" in
    openstack)
      audit_openstack "$2"
      ;;
    *)
      usage >&2
      exit 2
      ;;
  esac
}

main "$@"
