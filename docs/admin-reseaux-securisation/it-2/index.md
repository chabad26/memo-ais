# Pare-feu pfSense, journalisation et validation du cloisonnement réseau

## Itération 2

Cette itération introduit pfSense comme pare-feu central de l'infrastructure. L'objectif est de remplacer le simple routage inter-VLAN par un équipement dédié au filtrage, à la journalisation et, par la suite, à la mise en place de règles de sécurité plus strictes.

Le travail reprend les VLANs et l'adressage de l'itération 1. pfSense est placé entre les VLANs internes et le routeur physique afin de contrôler les flux réseau avant de les autoriser vers une autre zone.

L'itération sera segmentée en plusieurs ateliers :

- Déploiement de pfSense
