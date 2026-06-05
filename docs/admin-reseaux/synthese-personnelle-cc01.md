# Mémo personnel final — Administration des réseaux

## Objectif

Cette page sert de synthèse finale du module **Administration des réseaux**. Elle regroupe ce que j'ai compris, ce qui reste à consolider, les gestes que je veux garder et la manière dont je pourrai les réutiliser en situation professionnelle.

## Synthèse personnelle

Ce module m'a fait passer d'une vision assez théorique du réseau à une lecture plus concrète : une machine ne communique pas seulement parce qu'elle a une adresse IP, mais parce que plusieurs couches fonctionnent ensemble. Le câble ou l'interface doit être actif, le VLAN doit être correct, l'adresse IP doit appartenir au bon réseau, la passerelle doit router, puis les services comme DHCP, DNS ou NAT doivent répondre.

Le premier geste que je maîtrise mieux est le raisonnement **TCP/IP et adressage IPv4**. Je sais lire une IP, un masque, une passerelle et vérifier si deux machines sont dans le même réseau. Le subnetting demande encore de l'attention, mais je sais poser la méthode : réseau, plage utilisable, broadcast, capacité et passerelle.

Le deuxième geste est la lecture d'une infrastructure en couches **L1/L2/L3**. Sur AlpesNet, les VLANs, les ports access/trunk, les tables MAC, ARP et les routes ont pris du sens ensemble. Je comprends mieux qu'un VLAN isole un domaine de broadcast, qu'un trunk transporte plusieurs VLANs et que le routage devient nécessaire dès qu'on veut faire communiquer deux réseaux différents.

Le troisième geste est le **diagnostic méthodique**. Avant, j'aurais pu chercher directement une commande de correction. Maintenant, je pars du symptôme, je formule une hypothèse, je lance une commande, puis je conclus. `ping`, `show ip route`, `show ip ospf neighbor`, `show ip dhcp binding`, `show ip nat translations` et Wireshark deviennent des preuves pour expliquer ce qui se passe.

## Ce qui est clair

- TCP/IP sert à séparer les rôles : accès réseau, Internet, transport, application.
- Une adresse IP seule ne suffit pas : masque, passerelle et route sont indispensables.
- Un switch travaille surtout en L2 avec les MAC, les VLANs et les trunks.
- OSPF apprend automatiquement des routes si les voisins et les annonces sont corrects.
- DHCP attribue les paramètres réseau ; une APIPA signale une absence de réponse DHCP.
- NAT/PAT permet à des clients privés de sortir vers un réseau public.
- Une fiche de dépannage doit prouver la cause et la résolution, pas seulement dire que "ça remarche".

## Ce qui reste à travailler

Je dois encore gagner en rapidité sur le subnetting, surtout avec les masques moins évidents. OSPF est compris dans l'usage de base, mais les notions de coût, LSDB, LSA, convergence et authentification restent à approfondir. NAT/PAT mérite aussi plus de pratique, notamment avec les sous-interfaces, les ACL NAT et la différence entre un test depuis le routeur et un test depuis un client interne.

L'automatisation Bash est un bon début : lire un fichier, boucler, journaliser, gérer les erreurs et valider avec ShellCheck. Il faudra continuer avec des sauvegardes SSH plus robustes et, à terme, avec Python/Netmiko.

## Situation professionnelle concrète

Je réutiliserai ces apprentissages lors d'un incident réseau en entreprise. Si un site ne joint plus un service, je commencerai par délimiter le périmètre : une machine, un VLAN, un site ou tout le réseau. Ensuite, je déroulerai la méthode OSI : lien, VLAN, IP, passerelle, route, service, puis capture Wireshark si nécessaire.

Par exemple, si des postes obtiennent une APIPA, je chercherai DHCP après avoir vérifié L1/L2/L3. Si un site ne joint plus un autre site, je regarderai le routage et OSPF. Si le routeur ping un serveur public mais pas les clients internes, je contrôlerai NAT/PAT. Le réflexe à garder est simple : observer, tester, corriger une seule chose, puis prouver que le symptôme initial est résolu.

## Boîte à outils personnelle

| Thème | Notions à garder | Fiche associée |
| --- | --- | --- |
| Modèles réseau | TCP/IP, OSI, encapsulation, rôle des couches | [Modèles TCP/IP et OSI](../pense-bete/admin-resau/admin-reseaux-modeles.md) |
| AlpesNet | VLANs, plan d'adressage, passerelles, topologie L1/L2/L3 | [AlpesNet](../pense-bete/admin-resau/admin-reseaux-alpesnet.md) |
| Commandes | `ping`, `show ip route`, `show vlan brief`, OSPF, Bash | [Commandes et diagnostic](../pense-bete/admin-resau/admin-reseaux-commandes.md) |
| Switching | MAC, ARP, VLAN access/trunk, STP | [Switching, ARP, VLANs et STP](../pense-bete/admin-resau/switching-arp-vlans.md) |
| Routage | Route statique, next-hop, OSPF, convergence | [Vocabulaire du routage](../pense-bete/admin-resau/routage-vocabulaire.md) |
| Protocoles | DHCP, DNS, ICMP, TCP/UDP, OSPF | [Protocoles réseau](../pense-bete/admin-resau/admin-reseaux-protocoles.md) |
| Diagnostic | Méthode OSI, Wireshark, filtres, automatisation Bash | [Diagnostic, Wireshark et automatisation](../pense-bete/admin-resau/diagnostic-wireshark-automatisation.md) |
| Lecture par couches | Distinguer L1 physique, L2 VLAN/MAC, L3 IP/routage | [Niveaux L1/L2/L3](../pense-bete/admin-resau/admin-reseaux-niveaux.md) |

## Formule à garder

**Un bon diagnostic réseau ne commence pas par une correction : il commence par une hypothèse vérifiable et se termine par une preuve.**
