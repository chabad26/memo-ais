# Pense-bête Administration des réseaux

Cette section regroupe les rappels rapides du module **Administration des réseaux**.

Objectif : retrouver vite une commande, une notion ou un réflexe de diagnostic sans relire les pages de cours.

| Fiche | Contenu |
|---|---|
| [AlpesNet](admin-reseaux-alpesnet.md) | Plan d'adressage et topologie du cas pratique |
| [Commandes](admin-reseaux-commandes.md) | Commandes Linux, Cisco, GNS3 et diagnostic |
| [Installation](admin-reseaux-installation.md) | Préparation de l'environnement |
| [Modèles](admin-reseaux-modeles.md) | Modèles TCP/IP, OSI et encapsulation |
| [Niveaux](admin-reseaux-niveaux.md) | Couches L1, L2, L3 et rôles associés |
| [Protocoles](admin-reseaux-protocoles.md) | ARP, ICMP, DNS, TCP, UDP, HTTP |
| [Vocabulaire du routage](routage-vocabulaire.md) | OSPF, RIP, next-hop, métrique, route par défaut |
| [Switching, ARP, VLANs et STP](switching-arp-vlans.md) | Commutation, VLANs, trunk/access et anti-boucle |

## À retenir

- IP + masque = appartenance au réseau.
- Switch = couche 2, table MAC, VLANs.
- Routeur = couche 3, passage entre réseaux.
- ARP fait le lien IP -> MAC sur le LAN.
- `ping`, `traceroute`, `ip`, `tcpdump` et Wireshark sont les premiers réflexes de diagnostic.
