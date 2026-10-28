terraform {
  required_providers {
    ovh = {
      source  = "ovh/ovh"
      version = "~> 2.0"
    }
  }
}

provider "ovh" {
  endpoint = var.ovh_endpoint
}

resource "ovh_me_identity_group" "operators" {
  name = "operateurs"
  role = "UNPRIVILEGED"
}

resource "ovh_iam_policy" "tofu" {
  name        = "tofu-project-limited"
  description = "Droits OpenTofu limites au projet de laboratoire"
  identities  = [var.tofu_service_identity]
  resources   = [var.project_urn]

  # Remplacer par les actions verifiees dans la documentation et l'API OVH.
  allow = var.tofu_allowed_actions
}
