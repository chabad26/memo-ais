terraform {
  required_version = ">= 1.8.0"

  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 3.0"
    }
  }
}

provider "openstack" {
  region = var.region
}

resource "openstack_compute_keypair_v2" "admin" {
  name       = var.ssh_key_name
  public_key = file(pathexpand(var.ssh_public_key_path))
  region     = var.region
}

resource "openstack_compute_instance_v2" "prototype" {
  name            = var.instance_name
  image_name      = var.image_name
  flavor_name     = var.flavor_name
  key_pair        = openstack_compute_keypair_v2.admin.name
  security_groups = ["default"]
  region          = var.region

  network {
    name = var.public_network_name
  }

  dynamic "network" {
    for_each = var.private_network_name == null ? [] : [var.private_network_name]

    content {
      name = network.value
    }
  }
}

resource "openstack_compute_instance_v2" "small" {
  count           = length(var.small_instance_names)
  name            = var.small_instance_names[count.index]
  image_name      = var.image_name
  flavor_name     = var.small_flavor_name
  key_pair        = openstack_compute_keypair_v2.admin.name
  security_groups = ["default"]
  region          = var.region

  network {
    name = var.public_network_name
  }

  dynamic "network" {
    for_each = var.private_network_name == null ? [] : [var.private_network_name]

    content {
      name = network.value
    }
  }
}
