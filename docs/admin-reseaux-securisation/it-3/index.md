# VPN site-à-site et architecture sécurisée

## Itération 3

Cette itération introduit les VPN dans l'infrastructure sécurisée. Après la segmentation VLAN, le filtrage inter-VLAN et la journalisation pfSense, l'objectif est maintenant de créer une liaison chiffrée entre deux sites.

Le scénario retenu est un VPN site-à-site : un site principal représente le réseau local déjà protégé par pfSense, tandis qu'un second site distant est simulé derrière une machine Linux ou un routeur dédié jouant le rôle d'extrémité VPN.

## Objectifs de l'itération

À la fin de cette itération, il faut être capable de :

- expliquer le rôle d'un VPN dans une architecture réseau ;
- distinguer IPsec, OpenVPN et WireGuard ;
- préparer une architecture site-à-site avec un site principal et un site distant ;
- vérifier le routage, les VLANs, les règles pfSense et la connectivité avant la mise en place du tunnel ;
- documenter l'architecture de départ avant configuration.

## Environnement de travail

Chaque groupe dispose de :

- 6 machines Linux ;
- 1 routeur physique ;
- 3 machines Kali Linux ;
- 1 pfSense ;
- VLAN 10, VLAN 20 et VLAN 30.

Une machine Linux ou l'équipement `R2` visible sur le plan GNS3 servira de routeur VPN pour représenter un second site distant.

## Ateliers de l'itération

| Atelier | Sujet | Objectif |
| --- | --- | --- |
| Atelier 1 | Introduction aux VPN et architecture du TP | Comprendre les technologies VPN et préparer l'architecture site-à-site |
| Atelier 2 | Mise en place d'un VPN OpenVPN site-à-site | Configurer le tunnel, le routage et les règles firewall associées |
| Atelier 3 | Analyse du trafic OpenVPN avec Wireshark et les logs | Comparer le trafic avant/après VPN et diagnostiquer OpenVPN avec les captures et journaux |

## Points de vigilance

- Ne pas commencer la configuration VPN avant d'avoir validé la connectivité de base.
- Bien distinguer les flux locaux, les flux inter-VLAN et les flux qui devront traverser le tunnel.
- Documenter les adresses IP et les passerelles réelles observées dans le lab.
- Garder les captures ou sorties de commandes comme preuves techniques.
- Toujours préciser l'interface Wireshark utilisée, car une capture sur `tun0` et une capture sur l'interface physique ne montrent pas la même couche du trafic.
