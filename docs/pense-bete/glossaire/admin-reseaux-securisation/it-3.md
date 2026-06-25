# Glossaire Réseaux sécurisés - Itération 3

## Sujet

VPN site-à-site, OpenVPN, routage et analyse du tunnel.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| VPN | Tunnel chiffré reliant un client ou un site à un réseau distant. |
| OpenVPN | Solution VPN utilisant TLS et un tunnel réseau virtuel. |
| Tunnel | Interface logique transportant du trafic encapsulé. |
| Chiffrement | Protection de la confidentialité des échanges. |
| Certificat | Identité cryptographique utilisée dans l'authentification TLS. |
| Route poussée | Route envoyée au client VPN par le serveur. |
| Réseau de transit | Réseau traversé par le tunnel, sans voir le contenu interne. |
| `tun0` | Interface virtuelle souvent créée par OpenVPN. |

## Manipulations faites

| Manipulation | Commandes ou actions |
| --- | --- |
| Préparer l'architecture VPN | Identifier serveur, client, transit et VLANs à joindre. |
| Configurer OpenVPN | Fichiers serveur/client, certificats, routes. |
| Tester la connexion | Logs OpenVPN, ping vers réseaux internes. |
| Observer avant/après | Wireshark sur transit puis sur interface tunnel. |
| Diagnostiquer | Lire erreurs de configuration et valider correction. |

## Docs associées

- [Vue d'ensemble](../../../admin-reseaux-securisation/it-3/index.md)
- [Introduction aux VPN et architecture du TP](../../../admin-reseaux-securisation/it-3/atelier1.md)
- [Mise en place d'un VPN OpenVPN site-à-site](../../../admin-reseaux-securisation/it-3/atelier2.md)
- [Analyse Wireshark et logs OpenVPN](../../../admin-reseaux-securisation/it-3/atelier3.md)

