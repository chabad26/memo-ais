# Glossaire Réseaux - Itération 3

## Sujet

Routage statique et routage dynamique OSPF.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Route | Chemin connu pour atteindre un réseau. |
| Next-hop | Prochain routeur à joindre pour atteindre une destination. |
| Route statique | Route configurée manuellement. |
| Route par défaut | Route utilisée quand aucune route plus précise ne correspond. |
| Routage dynamique | Echange automatique d'informations de routage entre routeurs. |
| OSPF | Protocole de routage dynamique à état de liens. |
| Voisin OSPF | Routeur avec lequel une relation OSPF est établie. |
| Métrique | Coût utilisé pour choisir le meilleur chemin. |

## Manipulations faites

| Manipulation | Commandes ou actions |
| --- | --- |
| Ajouter une route statique | `ip route`, commandes routeur Cisco. |
| Vérifier la table | `ip route`, `show ip route`. |
| Configurer OSPF | Réseaux annoncés, voisins, interfaces. |
| Vérifier OSPF | `show ip ospf neighbor`, `show ip route ospf`. |
| Tester la panne | Couper une interface et observer la convergence. |

## Docs associées

- [Vue d'ensemble](../../../admin-reseaux/iteration-3/index.md)
- [Routage statique](../../../admin-reseaux/iteration-3/routage-statique.md)
- [Routage dynamique OSPF](../../../admin-reseaux/iteration-3/routage-dynamique-OSPF.md)

