# Glossaire Réseaux - Itération 2

## Sujet

Commutation, table MAC, ARP, VLANs, trunks et STP.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Switch | Equipement couche 2 qui transmet les trames selon les adresses MAC. |
| Adresse MAC | Identifiant matériel d'une interface réseau Ethernet. |
| Table MAC | Table qui associe adresse MAC et port de switch. |
| ARP | Protocole qui associe une adresse IP à une adresse MAC sur un LAN. |
| VLAN | Réseau logique isolé au niveau couche 2. |
| Port access | Port appartenant à un seul VLAN pour une machine finale. |
| Port trunk | Port transportant plusieurs VLANs avec étiquetage 802.1Q. |
| STP | Protocole anti-boucle au niveau couche 2. |

## Manipulations faites

| Manipulation | Commandes ou actions |
| --- | --- |
| Observer ARP | `arp -a`, Wireshark, ping initial. |
| Lire la table MAC | Commandes switch `show mac address-table`. |
| Configurer VLAN | Création VLAN, affectation port access. |
| Configurer trunk | Autoriser VLANs, vérifier transport 802.1Q. |
| Observer STP | Etat des ports, racine, blocage de boucle. |

## Docs associées

- [Vue d'ensemble](../../../admin-reseaux/iteration-2/index.md)
- [Commutation et VLANs](../../../admin-reseaux/iteration-2/synthese_switching_arp_stp.md)
- [GNS3 tables MAC et ARP](../../../admin-reseaux/iteration-2/gns3_mac_arp.md)
- [Synthèse VLANs](../../../admin-reseaux/iteration-2/synthese_vlans.md)
- [STP avancé](../../../admin-reseaux/iteration-2/stp_avance.md)

