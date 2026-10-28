variable "region" {
  description = "Region OVHcloud cible."
  type        = string
  default     = "GRA9"
}

variable "instance_name" {
  description = "Nom de l'instance prototype."
  type        = string
  default     = "d2-4-2026_08_31-09-17"
}

variable "flavor_name" {
  description = "Modele d'instance OVHcloud."
  type        = string
  default     = "d2-4"
}

variable "small_instance_names" {
  description = "Noms des deux VM de services secondaires."
  type        = list(string)
  default = [
    "d2-2-2026_08_31-01",
    "d2-2-2026_08_31-02",
  ]
}

variable "small_flavor_name" {
  description = "Modele des VM de services secondaires."
  type        = string
  default     = "d2-2"
}

variable "image_name" {
  description = "Image systeme disponible dans la region cible."
  type        = string
  default     = "Ubuntu 26.04 - UEFI"
}

variable "ssh_key_name" {
  description = "Nom de la cle SSH publique importee dans OVHcloud."
  type        = string
  default     = "laptop"
}

variable "ssh_public_key_path" {
  description = "Chemin local vers la cle SSH publique."
  type        = string
  default     = "~/.ssh/id_ed25519.pub"
}

variable "ssh_user" {
  description = "Utilisateur SSH par defaut de l'image."
  type        = string
  default     = "ubuntu"
}

variable "public_network_name" {
  description = "Nom du reseau public OVHcloud."
  type        = string
  default     = "Ext-Net"
}

variable "private_network_name" {
  description = "Nom du reseau prive OVHcloud a rattacher, ou null si non utilise."
  type        = string
  default     = "pn-GRA9-31082026"
  nullable    = true
}

variable "private_cidr" {
  description = "CIDR prive autorise pour les flux internes."
  type        = string
  default     = "10.42.10.0/24"
}

variable "admin_ssh_cidr" {
  type = string
}
