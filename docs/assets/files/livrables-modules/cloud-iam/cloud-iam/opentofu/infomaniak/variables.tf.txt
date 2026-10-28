variable "cloud_name" {
  description = "Nom du cloud dans ~/.config/openstack/clouds.yaml."
  type        = string
  default     = "PCP-XXXXXXX"
}

variable "region" {
  description = "Region Infomaniak cible, par exemple dc3-a ou dc4-a."
  type        = string
  default     = "dc4-a"
}

variable "instance_name" {
  description = "Nom de la VM principale."
  type        = string
  default     = "dist01b-infomaniak"
}

variable "flavor_name" {
  description = "Flavor Infomaniak de la VM principale."
  type        = string
  default     = "a2-ram4-disk50-perf1"
}

variable "small_instance_names" {
  description = "Noms des deux VM de services secondaires."
  type        = list(string)
  default     = ["files-infomaniak", "mail-infomaniak"]
}

variable "small_flavor_name" {
  description = "Flavor Infomaniak des VM secondaires."
  type        = string
  default     = "a1-ram2-disk50-perf1"
}

variable "image_name" {
  description = "Image disponible dans la region Infomaniak cible."
  type        = string
  default     = "Ubuntu 24.04 LTS Noble Numbat"
}

variable "ssh_key_name" {
  description = "Nom de la cle publique OpenStack."
  type        = string
  default     = "laptop"
}

variable "ssh_public_key_path" {
  description = "Chemin local vers la cle SSH publique."
  type        = string
  default     = "~/.ssh/id_ed25519.pub"
}

variable "ssh_user" {
  description = "Utilisateur SSH de l'image Ubuntu."
  type        = string
  default     = "ubuntu"
}

variable "public_network_name" {
  description = "Reseau public Infomaniak, souvent ext-net1."
  type        = string
  default     = "ext-net1"
}

variable "private_network_name" {
  description = "Reseau prive prealablement cree dans la region, ou null."
  type        = string
  default     = null
  nullable    = true
}
