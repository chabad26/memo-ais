# Identifier les éléments à observer

## Objectif

Identifier les informations nécessaires à l'exploitation quotidienne avant de configurer leur collecte : disponibilité, ressources, état des services et événements.

## Infrastructure de travail

Le laboratoire sera réalisé sur le **laptop**, avec **virt-manager** pour gérer les VM :

- **VM Debian** : serveur Linux prévu.
- **VM Windows Server** : serveur Windows prévu.
- **VM de supervision** : possibilité envisagée, à confirmer.

Les services réseau et applicatifs à observer seront choisis parmi ceux réellement installés ou repris des modules précédents. Leur présence n'est pas encore attestée dans cette feuille.

!!! note "Deux niveaux à distinguer"
    Une VM Debian est à la fois une machine virtuelle, vue depuis l'hôte, et un serveur Linux, vu depuis son système invité. Il n'est donc pas nécessaire de créer une VM supplémentaire pour remplir la ligne « VM ». L'état « en cours d'exécution » dans virt-manager ne prouve pas à lui seul que le système ou ses services répondent.

## Travail demandé

À partir de l'infrastructure, observer plusieurs types d'éléments :

- un serveur Linux ;
- un serveur Windows ;
- une machine virtuelle ;
- un service réseau ;
- un service applicatif.

Pour chaque élément, rechercher les informations qu'un administrateur souhaiterait connaître lors de l'exploitation quotidienne. Compléter progressivement le tableau avec les sources réellement disponibles et les fréquences retenues.

## Tableau d'observation à compléter

Cette première proposition sert de guide. **Les fréquences sont indicatives et ne correspondent pas à une collecte déjà configurée.** Les noms des services, les sources exactes et les fréquences seront précisés pendant les manipulations.

| Élément | Information recherchée | Où la trouver ? | Fréquence de collecte envisagée |
| --- | --- | --- | --- |
| Serveur Linux — VM Debian | Disponibilité, utilisation CPU et mémoire, swap, espace disque et inodes libres, erreurs système. | Dans Debian : outils système, état des services et journal système ; puis dans la plateforme après intégration. | Métriques toutes les 30 à 60 s ; journaux collectés au fil des événements. |
| Serveur Windows — VM Windows Server | Disponibilité, utilisation CPU et mémoire, espace libre des volumes, état des services et erreurs système. | Gestionnaire des tâches, Moniteur de performances, console Services et Observateur d'événements ; puis collecte centralisée. | Métriques toutes les 30 à 60 s ; journaux collectés au fil des événements. |
| VM — Debian ou Windows Server, vue depuis l'hôte | État démarré/arrêté, vCPU et RAM attribués, activité disponible côté hyperviseur ; ressources restantes sur le laptop. | Détails de la VM dans virt-manager et outils de surveillance du laptop. Les mesures disponibles dépendent de la configuration. | État et mesures toutes les 30 à 60 s ; inventaire des allocations à chaque modification. |
| Service réseau — à préciser | Réponse au contrôle, temps de réponse, état du service et erreurs. | État du service sur le serveur, journaux associés et sonde depuis le réseau ; par exemple une résolution DNS si ce service est présent. | Contrôle toutes les 30 à 60 s ; journaux au fil des événements. |
| Application — à préciser | Réponse à une opération attendue, temps de réponse, erreurs et accès. | Test fonctionnel depuis un client, journaux applicatifs et métriques si l'application en expose. | Test simple toutes les 60 s ; journaux au fil des événements. |

Une fréquence courte donne une vision plus récente, mais augmente le volume de données et la charge de collecte. Les valeurs seront adaptées aux besoins et aux ressources du laptop. Une consultation manuelle constitue une observation ponctuelle, pas une collecte automatique.

## Questions et repères de réponse

### Comment savoir si une machine est disponible ?

Croiser son état dans virt-manager avec un contrôle depuis une autre machine : réponse réseau et connexion à un service attendu. Un ping réussi indique une réponse ICMP, mais ne valide pas le fonctionnement des applications. Un ping sans réponse ne suffit pas non plus à déclarer la machine arrêtée : le trafic peut être filtré.

### Comment savoir si elle manque de ressources ?

Observer l'utilisation du CPU, la mémoire disponible, le recours au swap ou à la pagination et les délais d'accès au disque. Rechercher une pression durable et la rapprocher des ralentissements constatés. Vérifier également le laptop : plusieurs VM peuvent se disputer les mêmes ressources physiques.

### Comment détecter une saturation du stockage ?

Surveiller l'espace libre en volume et en pourcentage, ainsi que sa vitesse de diminution. Sur Debian, contrôler aussi les inodes disponibles : leur épuisement peut empêcher la création de fichiers même s'il reste de l'espace. Distinguer un disque presque plein d'un disque dont les entrées/sorties sont saturées, ce qui se manifeste par des délais élevés. Vérifier les volumes invités et le stockage du laptop qui héberge les disques virtuels.

### Comment savoir si un service est arrêté ?

Consulter son état dans le gestionnaire de services du système, puis tester la fonction attendue depuis un client. Un processus actif ou un port ouvert ne garantit pas que le service fonctionne correctement. Les journaux peuvent expliquer un arrêt ou un échec de démarrage.

### Comment retrouver les événements survenus sur une machine ?

Consulter le journal système et les journaux applicatifs sous Debian, ou l'Observateur d'événements et les journaux applicatifs sous Windows Server. Après centralisation, filtrer par machine, service et période. Des horloges synchronisées permettent de rapprocher les événements entre les machines.

### Quelle différence faites-vous entre une métrique et un journal ?

Une **métrique** est une mesure numérique suivie dans le temps, par exemple le pourcentage de CPU utilisé ou l'espace disque libre. Elle permet de repérer une tendance ou un dépassement de seuil.

Un **journal** décrit un événement horodaté, par exemple un échec de connexion ou l'arrêt d'un service. Il apporte du contexte pour comprendre ce qui s'est passé. Les deux se complètent : une hausse d'erreurs peut être visible dans une métrique et expliquée par les événements correspondants.

### Quelles informations doivent être disponibles immédiatement pour l'exploitation ?

- Les machines et services indisponibles ou dégradés, avec leur identité et l'heure du dernier contrôle.
- Les ressources sous pression : CPU, mémoire et stockage, côté VM et côté laptop.
- Les résultats des contrôles fonctionnels et les temps de réponse.
- Les erreurs récentes et un accès aux journaux concernés.
- L'état de la collecte et la fraîcheur des données : une absence de données doit être visible pour éviter de la confondre avec un fonctionnement normal.

## Trace à conserver dans le dossier de déploiement

Compléter le tableau au fil des observations, puis noter la date, l'élément contrôlé, la méthode utilisée et le résultat réellement obtenu. Ajouter les captures utiles, sans secrets ni identifiants inutiles.

Le résultat attendu est un inventaire des informations à collecter et de leurs sources, qui servira à préparer l'intégration dans la plateforme. Les repères ci-dessus restent à confronter au laboratoire et à reformuler à partir des observations.

[Retour au sommaire de l'itération](index.md)
