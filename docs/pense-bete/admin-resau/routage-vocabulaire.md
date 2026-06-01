# Vocabulaire du routage

Cette fiche sert à décoder les mots et sigles utilisés dans les pages sur le routage.

## Bases

| Terme | Définition simple |
| --- | --- |
| Routage | Action d'envoyer un paquet IP vers le bon réseau de destination. |
| Routeur | Équipement de couche 3 qui relie plusieurs réseaux IP. |
| Switch L3 | Switch capable de faire aussi du routage entre réseaux ou VLANs. |
| Interface | Port réseau d'un routeur ou d'un switch. Chaque interface peut avoir une IP. |
| Next-hop | Prochain routeur à qui envoyer le paquet pour atteindre un réseau distant. |
| Gateway | Passerelle utilisée par une machine pour sortir de son réseau local. |
| Table de routage | Liste des routes connues par un routeur. |

## Types de routes

| Code Cisco | Nom | À retenir |
| --- | --- | --- |
| `C` | Connected | Réseau directement connecté à une interface du routeur. |
| `L` | Local | Adresse IP exacte d'une interface du routeur, souvent en `/32`. |
| `S` | Static | Route ajoutée manuellement avec `ip route`. |
| `S*` | Static default | Route par défaut, utilisée si aucune route plus précise n'existe. |
| `O` | OSPF | Route apprise automatiquement avec le protocole OSPF. |
| `R` | RIP | Route apprise automatiquement avec le protocole RIP. |

Dans une table de routage, le code au début de la ligne indique l'origine de la route :

- `C` : le réseau est directement branché sur le routeur.
- `L` : l'adresse IP appartient à une interface du routeur.
- `S` : la route a été ajoutée à la main.
- `S*` : c'est une route statique par défaut.
- `O` ou `R` : la route vient d'un protocole de routage dynamique.

## Protocoles de routage

| Terme | Définition simple |
| --- | --- |
| Routage statique | Routes écrites à la main par l'administrateur. Simple, mais peu pratique sur un grand réseau. |
| Routage dynamique | Routes apprises automatiquement entre routeurs grâce à un protocole. |
| OSPF | Protocole de routage dynamique utilisé dans les réseaux d'entreprise. Il choisit les chemins selon un coût. |
| RIP | Ancien protocole de routage dynamique. Il choisit selon le nombre de routeurs traversés. Limité à 15 sauts. |
| Convergence | Moment où tous les routeurs ont mis à jour leurs routes après un changement réseau. |

## OSPF

| Terme | Définition simple |
| --- | --- |
| Link-state | Type de protocole où chaque routeur partage l'état de ses liens pour reconstruire la topologie. |
| LSA | Annonce OSPF qui décrit un lien ou une information de topologie. |
| LSDB | Base de données OSPF contenant la carte logique de la zone. |
| Dijkstra | Algorithme utilisé par OSPF pour calculer le plus court chemin. |
| Router ID | Identifiant unique d'un routeur OSPF, par exemple `1.1.1.1`. |
| Adjacence | Relation OSPF complète entre deux routeurs voisins. |
| Full | État attendu quand deux voisins OSPF ont synchronisé leurs informations. |
| Hello | Paquet OSPF envoyé régulièrement pour découvrir et surveiller les voisins. |
| Dead interval | Temps sans Hello après lequel un voisin OSPF est considéré perdu. |
| Area | Zone OSPF. En petit lab, on utilise souvent seulement l'area `0`. |
| Backbone area | Zone OSPF principale : `area 0`. |
| Coût OSPF | Valeur utilisée par OSPF pour choisir le meilleur chemin. Plus le coût est bas, plus le chemin est préféré. |
| Wildcard mask | Masque inversé utilisé dans les commandes `network`. Exemple : `/24` devient `0.0.0.255`. |

États d'adjacence à reconnaître :

| État | À retenir |
| --- | --- |
| `Down` | Aucun Hello reçu. |
| `Init` | Hello reçu, mais reconnaissance pas encore complète. |
| `2-Way` | Les deux routeurs se voient. |
| `ExStart` / `Exchange` | Début de synchronisation des informations OSPF. |
| `Loading` | Demande des informations manquantes. |
| `Full` | Adjacence complète, routage OSPF opérationnel. |

Repères rapides :

- OSPF utilise l'adresse multicast `224.0.0.5`.
- Les Hello sont souvent envoyés toutes les `10` secondes.
- Le dead interval est souvent de `40` secondes.
- Les routes OSPF apparaissent avec le code `O`.
- La distance administrative OSPF est `110`.
- L'authentification MD5 limite le risque d'injection de fausses routes par un routeur non autorisé.

## Priorité et choix des routes

| Terme | Définition simple |
| --- | --- |
| Distance administrative | Priorité de la source d'une route. Plus la valeur est basse, plus la route est préférée. |
| Métrique | Coût d'un chemin à l'intérieur d'un même protocole de routage. |
| Longest Prefix Match | Règle qui choisit la route la plus précise quand plusieurs routes correspondent. |
| Route par défaut | Route `0.0.0.0/0`, utilisée quand le routeur ne connaît pas de route plus précise. |

## Exemples rapides

| Exemple | Lecture |
| --- | --- |
| `S 192.168.20.0/24 [1/0] via 10.0.1.2` | Route statique vers `192.168.20.0/24`, next-hop `10.0.1.2`. |
| `[1/0]` | Distance administrative `1`, métrique `0`. |
| `S* 0.0.0.0/0 via 203.0.113.2` | Route par défaut vers `203.0.113.2`. |
| `O 192.168.30.0/24 [110/2]` | Route apprise par OSPF, distance administrative `110`, coût `2`. |

## Commandes OSPF rapides

| Commande | Usage |
| --- | --- |
| `router ospf 1` | Active le processus OSPF numéro `1`. |
| `router-id 1.1.1.1` | Définit l'identifiant unique du routeur. |
| `network 192.168.10.0 0.0.0.255 area 0` | Active OSPF sur un réseau `/24`. |
| `network 10.0.1.0 0.0.0.3 area 0` | Active OSPF sur un lien `/30`. |
| `show ip ospf neighbor` | Affiche les voisins OSPF et leur état. |
| `show ip route ospf` | Affiche seulement les routes apprises par OSPF. |
| `show ip ospf interface brief` | Vérifie quelles interfaces participent à OSPF. |
| `show ip ospf database` | Affiche la LSDB. |

## À retenir

- `C` et `L` apparaissent automatiquement quand une interface est configurée.
- `S` est ajouté manuellement.
- `O` et `R` viennent de protocoles de routage dynamique.
- Le routeur choisit d'abord la route la plus précise, puis tient compte de la distance administrative et de la métrique.
