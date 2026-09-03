#!/usr/bin/env bash
set -euo pipefail

execute=false
infra_dir=""
inventory=""
service_url=""
limit_group="infomaniak"
destroy_after=false
cloud_iam_dir="${CLOUD_IAM_DIR:-$HOME/cloud-iam}"

usage() {
  cat <<'EOF'
Usage:
  test-restauration-cloud.sh --infra-dir DIR --inventory FILE --service-url URL [options]

Options:
  --execute          Execute les commandes. Par defaut, dry-run seulement.
  --destroy-after    Lance tofu destroy apres validation. A utiliser seulement en lab isole.
  --limit GROUP      Groupe Ansible a tester, par defaut infomaniak.
  --cloud-iam-dir DIR
                     Racine du depot cloud-iam, par defaut $HOME/cloud-iam.
  -h, --help         Affiche cette aide.

Variables attendues:
  OS_CLOUD           Profil OpenStack a utiliser.
  OS_PASSWORD        Mot de passe OpenStack, si requis par clouds.yaml.

Le script ne gere aucun secret et n'ecrit aucune cle dans le depot.
EOF
}

die() {
  printf 'Erreur: %s\n' "$1" >&2
  exit 1
}

run_cmd() {
  printf '+ %s\n' "$*"
  if [[ "$execute" == true ]]; then
    "$@"
  fi
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "commande introuvable: $1"
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --execute)
        execute=true
        shift
        ;;
      --destroy-after)
        destroy_after=true
        shift
        ;;
      --infra-dir)
        infra_dir="${2:-}"
        shift 2
        ;;
      --inventory)
        inventory="${2:-}"
        shift 2
        ;;
      --service-url)
        service_url="${2:-}"
        shift 2
        ;;
      --limit)
        limit_group="${2:-}"
        shift 2
        ;;
      --cloud-iam-dir)
        cloud_iam_dir="${2:-}"
        shift 2
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        die "argument inconnu: $1"
        ;;
    esac
  done
}

validate_inputs() {
  [[ -n "$infra_dir" ]] || die "--infra-dir est obligatoire"
  [[ -n "$inventory" ]] || die "--inventory est obligatoire"
  [[ -n "$service_url" ]] || die "--service-url est obligatoire"
  [[ -d "$infra_dir" ]] || die "dossier introuvable: $infra_dir"
  [[ -f "$inventory" ]] || die "inventaire introuvable: $inventory"
  [[ -d "$cloud_iam_dir" ]] || die "dossier cloud-iam introuvable: $cloud_iam_dir"
  [[ -n "${OS_CLOUD:-}" ]] || die "OS_CLOUD doit etre exporte"

  require_cmd tofu
  require_cmd ansible
  require_cmd ansible-playbook
  require_cmd curl
}

main() {
  parse_args "$@"
  validate_inputs

  printf '# Test de restauration cloud\n'
  printf 'Mode execute: %s\n' "$execute"
  printf 'T0: %s\n' "$(date -Is)"

  pushd "$infra_dir" >/dev/null
  run_cmd tofu init
  run_cmd tofu fmt
  run_cmd tofu validate
  run_cmd tofu plan
  run_cmd tofu apply -auto-approve
  run_cmd tofu output
  popd >/dev/null

  run_cmd ansible -i "$inventory" "$limit_group" -m ping
  run_cmd ansible-playbook -i "$inventory" "$cloud_iam_dir/ansible/playbooks/base-system.yml"
  run_cmd ansible-playbook -i "$inventory" "$cloud_iam_dir/ansible/playbooks/deploy-on-premise.yml"
  run_cmd curl -fsS -I "$service_url"

  printf 'T1: %s\n' "$(date -Is)"
  printf 'Calculer ensuite RTO = T1 - T0 et RPO = T0 - horodatage de la sauvegarde restauree.\n'

  if [[ "$destroy_after" == true ]]; then
    pushd "$infra_dir" >/dev/null
    run_cmd tofu destroy -auto-approve
    popd >/dev/null
  fi
}

main "$@"
