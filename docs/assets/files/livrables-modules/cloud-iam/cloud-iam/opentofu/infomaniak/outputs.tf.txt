output "instance_id" {
  description = "Identifiant OpenStack de la VM principale."
  value       = openstack_compute_instance_v2.prototype.id
}

output "instance_name" {
  description = "Nom de la VM principale."
  value       = openstack_compute_instance_v2.prototype.name
}

output "instance_ipv4" {
  description = "Adresse IPv4 d'acces de la VM principale."
  value       = openstack_compute_instance_v2.prototype.access_ip_v4
}

output "instance_networks" {
  description = "Reseaux rattaches a la VM principale."
  value       = openstack_compute_instance_v2.prototype.network
}

output "ssh_connection_hint" {
  description = "Commande SSH indicative."
  value       = "ssh ${var.ssh_user}@${openstack_compute_instance_v2.prototype.access_ip_v4}"
}

output "small_instance_ids" {
  description = "Identifiants des VM secondaires."
  value       = openstack_compute_instance_v2.small[*].id
}

output "small_instance_names" {
  description = "Noms des VM secondaires."
  value       = openstack_compute_instance_v2.small[*].name
}

output "small_instance_ipv4s" {
  description = "Adresses IPv4 d'acces des VM secondaires."
  value       = openstack_compute_instance_v2.small[*].access_ip_v4
}
