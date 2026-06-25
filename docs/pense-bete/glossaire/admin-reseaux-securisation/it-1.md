# Glossaire Réseaux sécurisés - Itération 1

## Sujet

Segmentation sécurisée, VLANs, filtrage `nftables` et introduction au VLAN Hopping.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Segmentation | Découpage du réseau en zones pour limiter les impacts. |
| VLAN sécurisé | VLAN configuré avec ports access, trunk contrôlé et VLAN natif maîtrisé. |
| ACL | Règle d'autorisation ou de blocage de flux réseau. |
| Politique restrictive | Tout bloquer par défaut, autoriser seulement le nécessaire. |
| `nftables` | Pare-feu Linux moderne remplaçant progressivement iptables. |
| Chain | Chaîne de règles dans une table nftables. |
| Hook | Point d'accroche réseau où s'applique une chaîne. |
| VLAN Hopping | Technique visant à sortir d'un VLAN via mauvaise configuration couche 2. |
| Double tagging | Variante utilisant deux tags 802.1Q dans une trame. |

## Manipulations faites

| Manipulation | Commandes ou actions |
| --- | --- |
| Définir l'architecture sécurisée | Identifier VLANs, rôles, flux autorisés et flux bloqués. |
| Configurer les VLANs | Ports access, trunks, VLANs autorisés. |
| Filtrer avec nftables | Table, chain forward, policy drop, règles accept/drop. |
| Tester le filtrage | `ping`, `ssh`, `nc`, serveur HTTP temporaire. |
| Observer VLAN Hopping | Wireshark, Scapy/Yersinia en laboratoire contrôlé. |

## Docs associées

- [Vue d'ensemble](../../../admin-reseaux-securisation/it-1/index.md)
- [Introduction du module et architecture sécurisée](../../../admin-reseaux-securisation/it-1/atelier1.md)
- [VLANs sécurisés et préparation du filtrage](../../../admin-reseaux-securisation/it-1/atelier2.md)
- [Filtrage réseau avec nftables](../../../admin-reseaux-securisation/it-1/atelier3.md)
- [Introduction au VLAN Hopping et tests d'attaque](../../../admin-reseaux-securisation/it-1/atelier4.md)

