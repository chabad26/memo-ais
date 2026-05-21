# Pense-bête Système d'info & archi SI

## Ce que je retiens de la cartographie SI

Cartographier un SI, ce n'est pas dessiner tous les serveurs un par un.

C'est comprendre :

- quelles activités métier dépendent du numérique ;
- quelles applications, données, réseaux et utilisateurs sont impliqués ;
- quels flux sont indispensables ;
- quels points peuvent bloquer toute l'organisation ;
- quelles hypothèses sont crédibles, et lesquelles doivent être vérifiées.

La cartographie sert à expliquer le SI à quelqu'un d'autre, mais aussi à voir où un incident peut se propager.

## La démarche en 4 axes

| Axe | Question à poser | Exemples dans un hôpital |
| --- | --- | --- |
| Réseau | Quelles zones communiquent entre elles ? | Internet, VPN, postes, serveurs, biomédical, ToIP |
| Applicatif | Quelles applications soutiennent l'activité ? | DPI, prescriptions, admissions, laboratoire, imagerie |
| Données | Où sont les données critiques et comment circulent-elles ? | dossier patient, résultats, images, comptes rendus, sauvegardes |
| Utilisateurs | Qui accède à quoi, comment et pourquoi ? | médecins, infirmiers, DSI, prestataires, administratif |

À retenir :

- le réseau montre les chemins ;
- l'applicatif montre les services ;
- les données montrent la valeur à protéger ;
- les utilisateurs montrent les usages, droits et risques humains.

## Hypothèses argumentées

Une hypothèse est acceptable si elle est annoncée et justifiée.

| Hypothèse | Pourquoi elle est crédible | À vérifier |
| --- | --- | --- |
| Le SI utilise un annuaire central | beaucoup d'utilisateurs et de postes à gérer | AD unique ou plusieurs annuaires |
| Des accès prestataires existent | maintenance applicative et biomédicale fréquente | VPN, comptes, périmètre exact |
| Le DPI dépend de serveurs et bases centrales | les soins nécessitent un dossier partagé | architecture réelle du DPI |
| Les sauvegardes sont séparées ou devraient l'être | indispensable après ransomware | isolation, tests, fréquence |
| Le biomédical devrait être cloisonné | équipements sensibles, parfois anciens | segmentation réelle |

Phrase utile :

**Je ne dis pas que c'est certain ; je dis que c'est plausible, justifié, et à vérifier.**

## Les 5 typologies d'architecture

| Modèle | Principe | Avantage | Limite |
| --- | --- | --- | --- |
| Centralisée | traitements et données concentrés sur un système principal | simple à piloter, données cohérentes | point unique de panne possible |
| Décentralisée | plusieurs services ou sites ont leurs propres systèmes | autonomie locale | doublons, cohérence difficile |
| Distribuée | plusieurs composants coopèrent via le réseau | meilleure répartition et disponibilité | flux et supervision plus complexes |
| Cloud | applications ou données hébergées chez un fournisseur | élasticité, maintenance déléguée | dépendance réseau/fournisseur, conformité |
| Hybride | mélange d'interne, cloud, centralisé et distribué | réaliste et flexible | intégration et sécurité plus difficiles |

Dans un hôpital, le modèle est souvent **hybride** :

- certaines données sensibles restent internes ;
- certaines sauvegardes ou services peuvent être externalisés ;
- des applications spécialisées existent par métier ;
- l'identité et les droits sont souvent centralisés.

## Ce qui m'a surpris dans le cas CHU de Rouen

- Un ransomware ne touche pas seulement des fichiers : il désorganise les soins, les admissions, les prescriptions et les résultats.
- Le mode dégradé papier/téléphone reste indispensable, même dans un hôpital très informatisé.
- Les sauvegardes sont aussi importantes que les applications : sans restauration, la crise dure.
- La téléphonie isolée peut devenir un vrai moyen de continuité.
- Un poste ou un accès prestataire peut devenir critique si les droits ou le cloisonnement sont insuffisants.
- Le plus dangereux n'est pas toujours le point d'entrée, mais la capacité de rebond vers l'AD, les serveurs et les données.

## Données qu'un ransomware vise en priorité

| Priorité | Données ou systèmes | Pourquoi |
| --- | --- | --- |
| 1 | dossier patient, prescriptions, résultats | bloque directement les soins |
| 2 | comptes, AD/IAM, droits administrateurs | permet la propagation |
| 3 | sauvegardes | empêche une restauration rapide |
| 4 | données administratives et RH | augmente l'impact métier |
| 5 | journaux et configurations | gêne l'analyse et la reprise |

## Utilisateurs et facteurs humains

Un utilisateur n'est pas seulement un risque : c'est un acteur du SI avec des contraintes.

| Profil | Besoin | Risque possible |
| --- | --- | --- |
| Médecins | accéder vite au dossier et prescrire | session ouverte, urgence, mobilité |
| Infirmiers | suivre les soins sur postes partagés | partage de session ou de carte |
| Administratif | gérer admissions, rendez-vous, messages | phishing, pièce jointe, erreur de saisie |
| DSI / IT | administrer, dépanner, restaurer | compte admin utilisé trop largement |
| Prestataires | maintenir à distance | accès VPN trop large ou permanent |

Question clé :

**Dans quelles conditions quelqu'un est-il poussé à contourner la sécurité ?**

Réponses fréquentes :

- urgence ;
- outil trop lent ;
- manque de postes ;
- authentification trop lourde ;
- droits insuffisants ;
- procédure de support trop longue.

## Vocabulaire enrichi cette semaine

| Terme | Définition simple | Pourquoi c'est important |
| --- | --- | --- |
| SI | système d'information : personnes, outils, données, procédures, infrastructures | dépasse la technique pure |
| DPI | dossier patient informatisé | coeur des données de soins |
| SPOF | Single Point of Failure : point unique de panne | un seul composant peut bloquer beaucoup de services |
| Middleware | couche logicielle qui connecte applications, données et utilisateurs | explique les dépendances entre systèmes |
| API | interface permettant à deux applications d'échanger | rend les flux applicatifs visibles |
| Flux | circulation d'une donnée ou demande entre deux éléments | base des diagrammes |
| Segmentation | découpage réseau en zones ou VLAN | limite les chemins possibles |
| Cloisonnement | séparation fonctionnelle ou technique des zones | limite la propagation |
| AD / Active Directory | annuaire central de comptes, groupes et droits | point critique pour l'authentification |
| IAM | gestion des identités et des accès | répond à qui a droit à quoi |
| VPN | accès distant sécurisé au SI | utile mais sensible pour prestataires |
| MFA | authentification multifacteur | réduit l'impact d'un mot de passe volé |
| PACS | stockage et consultation des images médicales | critique pour l'imagerie |
| RIS | système de radiologie : demandes, planning, comptes rendus | souvent lié au PACS et au DPI |
| SIEM | centralisation et corrélation des journaux de sécurité | aide à détecter les incidents |
| ToIP | téléphonie sur IP | peut aider en crise si isolée |
| PRA | plan de reprise d'activité | redémarrer après incident |
| PCA | plan de continuité d'activité | continuer malgré l'incident |
| Mode dégradé | fonctionnement réduit sans SI complet | papier, téléphone, procédures manuelles |

## Réflexes pour lire un diagramme SI

Se poser toujours les mêmes questions :

- Où sont les données sensibles ?
- Qui y accède ?
- Par quels systèmes d'autorisation ?
- Quels flux sont indispensables ?
- Quels accès distants existent ?
- Quels composants sont des SPOF ?
- Quelles zones sont cloisonnées ?
- Où sont les sauvegardes ?
- Que peut-on couper en crise ?
- Quelles hypothèses doivent être vérifiées ?

## Checklist d'un diagramme finalisé

| Point | À vérifier |
| --- | --- |
| Titre | le sujet est clair |
| Légende | les couleurs et flèches sont expliquées |
| Lisibilité | le texte reste lisible |
| Simplicité | peu d'éléments par schéma |
| Direction | les flux ont un sens |
| Hypothèses | elles sont indiquées |
| Défense | je peux expliquer pourquoi c'est crédible |

## À retenir de l'itération

Une bonne cartographie SI ne cherche pas à tout savoir immédiatement.

Elle sert à construire une représentation défendable :

- basée sur les usages réels ;
- organisée selon les 4 axes ;
- enrichie par les typologies d'architecture ;
- claire sur ses hypothèses ;
- utile pour repérer les points critiques ;
- compréhensible par un tiers.

il faut savoir faire aussi l'analyse des enjeux et des risques. Les 5 enjeux principaux sont **disponibilité**, **sécurité**, **évolutivité**, **intégration** et **conformité**. Pour la disponibilité, il faut savoir raisonner avec le **RTO** (temps maximal acceptable avant reprise) et le **RPO** (perte de données maximale acceptable). Ensuite, les risques doivent être classés par nature : **techniques**, **organisationnels** ou **humains**, puis priorisés par impact. Les normes et règlements comme **RGPD**, **NIS2**, **DORA** et **ISO 27001** aident à relier les risques aux obligations, à la gouvernance et au travail concret d'administration système.

Synthèse à garder :

- un enjeu explique ce qu'on veut protéger ;
- un risque décrit ce qui peut mal se passer ;
- une norme donne un cadre ou des exigences ;
- un exemple réel permet de vérifier que l'analyse reste concrète.
