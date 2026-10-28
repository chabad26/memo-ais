terraform {
  required_providers {
    ovh = {
      source  = "ovh/ovh"
      version = "~> 2.0"
    }
  }
}

provider "ovh" {
  endpoint = "ovh-eu"
}

resource "ovh_cloud_project_storage" "tofu_state" {
  service_name = var.service_name
  region_name  = "GRA"
  name         = var.bucket_name

  versioning = {
    status = "enabled"
  }

  encryption = {
    sse_algorithm = "AES256"
  }
}
