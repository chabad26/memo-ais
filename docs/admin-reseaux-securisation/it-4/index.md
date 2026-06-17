# Analyse réseau avec Zeek

## Itération 4

Cette itération introduit Zeek comme outil d'analyse réseau et de supervision de sécurité. Après les VLANs, pfSense et OpenVPN, l'objectif est maintenant d'observer l'infrastructure avec un outil capable de produire automatiquement des journaux exploitables.

Zeek ne remplace ni Wireshark ni le pare-feu. Il complète l'architecture :

- pfSense filtre et journalise les décisions de sécurité ;
- Wireshark permet l'analyse paquet par paquet ;
- Zeek observe le trafic et transforme les communications réseau en logs structurés.

## Objectifs de l'itération

À la fin de cette itération, il faut être capable de :

- expliquer le rôle de Zeek dans une architecture réseau sécurisée ;
- distinguer l'usage de Zeek et de Wireshark ;
- placer une machine Zeek à un endroit pertinent du réseau ;
- vérifier que Zeek observe bien du trafic ;
- générer et lire les premiers logs Zeek ;
- documenter l'architecture d'analyse réseau retenue ;
- relier les observations Zeek aux VLANs, à pfSense et au VPN OpenVPN si actif.

## Environnement de travail

Chaque groupe dispose de :

- 4 machines Linux ;
- 1 routeur physique ;
- pfSense ;
- 1 machine Kali Linux ;
- VLAN 10 et VLAN 20 ;
- 1 machine utilisée pour Zeek.

La machine Zeek doit être placée de manière à observer le trafic du groupe. Son emplacement peut évoluer pendant l'itération selon les besoins d'observation.

## Ateliers de l'itération

| Atelier | Sujet | Objectif |
| --- | --- | --- |
| Atelier 1 | Découverte de Zeek et architecture d'analyse réseau | Installer, placer et valider une machine Zeek dans le lab |
| Atelier 2 | Installation de Zeek et génération de logs réseau | Générer du trafic depuis Kali Linux et lire les premiers logs Zeek |
| Atelier 3 | Détection de scans et simulation de déni de service avec Zeek | Observer des scans Nmap, un SYN flood limité et comparer Zeek, Wireshark et pfSense |

## Points de vigilance

- Zeek observe le trafic, mais ne le bloque pas.
- Zeek ne voit que le trafic qui arrive sur son interface.
- Le choix de l'emplacement de la machine Zeek est donc central.
- Une capture sur un mauvais segment peut donner l'impression que Zeek ne fonctionne pas.
- Les logs Zeek doivent toujours être interprétés avec le contexte réseau : VLAN, routage, pfSense, NAT et VPN.

## Ressource principale

- Zeek Documentation : <https://docs.zeek.org/>
