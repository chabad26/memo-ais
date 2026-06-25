# Glossaire Réseaux - Itération 5

## Sujet

Analyse de trafic, diagnostic OSI, simulation de pannes, Wireshark et automatisation Bash.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Diagnostic OSI | Méthode consistant à tester couche par couche. |
| Symptôme | Ce qui est observé comme dysfonctionnement. |
| Cause probable | Hypothèse la plus cohérente après tests. |
| Preuve | Capture, commande ou log qui confirme une observation. |
| Capture pcapng | Fichier de capture Wireshark. |
| Automatisation | Transformation d'une vérification répétitive en script. |
| Sauvegarde de configuration | Copie horodatée d'une configuration équipement. |

## Manipulations faites

| Manipulation | Commandes ou actions |
| --- | --- |
| Diagnostiquer par couches | L1 câble/interface, L2 ARP/VLAN, L3 IP/route, L4 ports. |
| Capturer avec Wireshark | Filtrer ICMP, DNS, DHCP, OSPF. |
| Simuler des pannes | Interface down, mauvaise passerelle, route absente. |
| Ecrire un script | Test de connectivité, boucle sur fichier d'hôtes. |
| Sauvegarder des configs | SSH, fichiers `.cfg`, horodatage. |

## Docs associées

- [Vue d'ensemble](../../../admin-reseaux/iteration-5/index.md)
- [Méthode de diagnostic OSI](../../../admin-reseaux/iteration-5/methode-diagnostic-osi.md)
- [Simulation pannes AlpesNet OSI](../../../admin-reseaux/iteration-5/simulation-pannes-alpesnet-osi.md)
- [Critères fiche dépannage AlpesNet](../../../admin-reseaux/iteration-5/criteres-fiche-depannage-alpesnet.md)
- [TP Wireshark GNS3 et réseau physique](../../../admin-reseaux/iteration-5/tp-wireshark-gns3-reseau-physique.md)
- [Synthèse automatisation Bash](../../../admin-reseaux/iteration-5/synthese-automatisation-bash.md)
- [Automatisation connectivité et sauvegarde](../../../admin-reseaux/iteration-5/automatisation-connectivite-sauvegarde.md)

