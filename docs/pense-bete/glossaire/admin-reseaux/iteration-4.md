# Glossaire Réseaux - Itération 4

## Sujet

Services réseau : DHCP, NAT/PAT, DNS et finalisation de l'infrastructure AlpesNet.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| DHCP | Service qui attribue automatiquement IP, masque, passerelle et DNS. |
| Bail DHCP | Durée pendant laquelle une adresse est attribuée à un client. |
| DORA | Séquence DHCP Discover, Offer, Request, Ack. |
| NAT | Traduction d'adresses réseau. |
| PAT | Variante NAT qui partage une adresse via les ports. |
| DNS | Service qui traduit un nom en adresse IP. |
| Zone DNS | Espace de noms géré par un serveur DNS. |
| Enregistrement A | Association nom DNS vers adresse IPv4. |

## Manipulations faites

| Manipulation | Commandes ou actions |
| --- | --- |
| Configurer DHCP | Pools, exclusions, passerelle, DNS. |
| Vérifier DHCP | `show ip dhcp binding`, capture DORA. |
| Configurer NAT/PAT | Interfaces inside/outside, ACL, overload. |
| Vérifier NAT | `show ip nat translations`, tests ping/curl. |
| Configurer DNS | Zone, enregistrements, tests `dig`/`nslookup`. |

## Docs associées

- [Vue d'ensemble](../../../admin-reseaux/iteration-4/index.md)
- [Synthèse DHCP](../../../admin-reseaux/iteration-4/synthese-dhcp.md)
- [TP DHCP et VLANs](../../../admin-reseaux/iteration-4/dhcp-vlans-gns3.md)
- [NAT et PAT](../../../admin-reseaux/iteration-4/nat-pat.md)
- [TP NAT/PAT GNS3](../../../admin-reseaux/iteration-4/tp-nat-pat-gns3.md)
- [DNS interne](../../../admin-reseaux/iteration-4/dns.md)
- [Finalisation AlpesNet](../../../admin-reseaux/iteration-4/finalisation-infrastructure-alpesnet.md)

