# Glossaire Réseaux sécurisés - Itération 4

## Sujet

Zeek, analyse réseau, logs, scans, attaques et corrélation forensique.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Zeek | Moteur d'analyse réseau produisant des logs structurés. |
| `conn.log` | Journal Zeek des connexions observées. |
| Forensique | Analyse de traces pour reconstruire un événement. |
| Corrélation | Croisement de plusieurs sources pour confirmer une chronologie. |
| Scan | Recherche de ports ou services exposés. |
| Etat TCP | Indication du déroulement d'une connexion (`S0`, `S1`, etc.). |
| Wireshark | Vue paquet détaillée, complémentaire des logs Zeek. |
| Log pfSense | Trace de décision firewall pass/block. |

## Manipulations faites

| Manipulation | Commandes ou actions |
| --- | --- |
| Installer Zeek | Interface surveillée, premiers logs. |
| Générer du trafic | Ping, curl, scans contrôlés, tests VLAN Hopping. |
| Lire les logs | `conn.log`, timestamps, IP sources/destinations, ports. |
| Corréler les sources | Zeek + Wireshark + pfSense + OpenVPN. |
| Produire une chronologie | Détection, observation, interprétation, conclusion. |

## Docs associées

- [Vue d'ensemble](../../../admin-reseaux-securisation/it-4/index.md)
- [Découverte de Zeek et architecture d'analyse réseau](../../../admin-reseaux-securisation/it-4/atelier1.md)
- [Installation et premiers logs Zeek](../../../admin-reseaux-securisation/it-4/atelier2.md)
- [Analyse des logs Zeek et détection d'attaques](../../../admin-reseaux-securisation/it-4/atelier3.md)
- [Corrélation et analyse forensique réseau](../../../admin-reseaux-securisation/it-4/atelier4.md)

