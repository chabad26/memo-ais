# Cartographie et architecture SI

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
