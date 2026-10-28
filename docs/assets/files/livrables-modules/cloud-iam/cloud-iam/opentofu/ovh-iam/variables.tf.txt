variable "ovh_endpoint" {
  type    = string
  default = "ovh-eu"
}

variable "project_urn" {
  type      = string
  sensitive = false
}

variable "tofu_service_identity" {
  type      = string
  sensitive = false
}

variable "tofu_allowed_actions" {
  description = "Actions OVHcloud strictement necessaires a OpenTofu"
  type        = list(string)
}
