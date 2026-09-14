# Comprendre l'observabilité — mots clés et architecture

## Objectif

Comprendre les informations utilisées pour observer une infrastructure et le rôle de **Prometheus**, **Grafana** et **ELK** dans l'architecture retenue pour ce module.

## Observabilité

L'**observabilité** permet d'exploiter les données produites par une infrastructure afin de comprendre son état et son comportement. Elle aide à repérer un dysfonctionnement, à situer son apparition et à rechercher son origine.

Dans ce module, trois sources complémentaires sont exploitées : **les métriques, les journaux et les résultats des sondes**.

!!! note "Vocabulaire"
    Une sonde est un mécanisme de contrôle ; son résultat peut devenir une métrique, par exemple un succès/échec ou un temps de réponse. Dans une présentation générale de l'observabilité, les trois familles souvent citées sont les métriques, les journaux et les traces. Les traces suivent le parcours d'une requête entre composants ; elles ne sont pas au centre de cette première itération.

## Métriques

Les **métriques** sont des données numériques mesurées dans le temps. Elles permettent de suivre une évolution, de comparer des périodes et de repérer une pression sur les ressources.

| Domaine | Exemples de métriques |
| --- | --- |
| CPU | Pourcentage d'utilisation, température si un capteur est accessible. |
| Mémoire | RAM utilisée et disponible, pourcentage d'utilisation, activité du swap ou de la pagination. |
| Stockage | Espace utilisé et disponible, pourcentage d'occupation, débit et latence des entrées/sorties (I/O). |
| Trafic réseau | Débits entrant et sortant, erreurs, pertes de paquets et latence selon les mesures disponibles. |
| Disponibilité | Résultat d'un ping, succès d'une connexion à un service, durée du contrôle. |
| Performances | Temps de réponse, temps de traitement d'un service, nombre d'opérations par seconde. |

Une mesure doit être accompagnée de son **horodatage**, de sa **source** et d'une **unité** ou d'une signification explicite. Une valeur isolée est moins informative que son évolution dans le temps.

Dans le laboratoire virt-manager, les VM n'exposent pas nécessairement les capteurs physiques du laptop. Les températures du CPU ou de la mémoire ne seront donc collectées que si le matériel et les outils les rendent accessibles, généralement côté hôte. De même, le débit réseau observé ne donne pas directement la bande passante encore disponible.

## Journaux

Les **journaux** décrivent les événements produits par les systèmes et les applications :

- démarrage et arrêt de services ;
- erreurs ;
- authentifications réussies ou échouées ;
- événements système ;
- événements applicatifs.

Ils apportent le contexte nécessaire au diagnostic : **quand**, **sur quelle machine**, **dans quel service** et **avec quel message** un événement s'est produit.

Par exemple, une métrique peut montrer une pression mémoire tandis qu'un journal système peut signaler l'arrêt d'un processus faute de mémoire. Il faut rapprocher les heures et les sources avant de conclure à un lien entre ces observations.

## Sondes

Les **sondes** sont des mécanismes permettant de vérifier directement un état, une disponibilité ou un fonctionnement attendu.

| Contrôle | Ce que la sonde vérifie | Limite à garder en tête |
| --- | --- | --- |
| Ping | Réponse ICMP d'une machine depuis le point de contrôle. | Une absence de réponse peut venir d'un filtrage ; une réponse ne valide pas une application. |
| Port réseau | Possibilité d'établir une connexion sur le port attendu. | Un port accessible ne garantit pas une réponse fonctionnelle correcte. |
| Réponse HTTP | Code de réponse, délai et éventuellement contenu attendu. | Le contrôle doit viser une page ou une fonction pertinente. |
| Service réseau | Résultat d'une opération, par exemple une résolution DNS. | Le résultat dépend aussi du réseau et des dépendances du service. |
| État d'un équipement | Réponse à un contrôle d'état adapté à l'équipement. | Le périmètre du contrôle doit être précisé. |
| Application | Réussite d'une opération représentative de son utilisation. | Une fonction testée ne couvre pas tous les usages de l'application. |

Les résultats peuvent être numériques : **1 pour un succès, 0 pour un échec**, ou une **durée en secondes**, selon la sonde et le format retenus. Ils peuvent ainsi alimenter des métriques et des tableaux de bord.

## Architecture retenue pour ce module

| Outil | Rôle dans le module | Données exploitées |
| --- | --- | --- |
| **Prometheus** | Collecter, conserver et interroger les métriques. | Mesures système et résultats de sondes exposés sous une forme compatible. |
| **Grafana** | Visualiser les métriques et construire les tableaux de bord (*dashboards*). | Données interrogées auprès de Prometheus dans l'architecture prévue. |
| **ELK** | Centraliser, rechercher et exploiter les journaux. | Événements système et applicatifs collectés sur les machines. |

**ELK** désigne **Elasticsearch**, **Logstash** et **Kibana** :

- **Elasticsearch** stocke, indexe et permet de rechercher les événements.
- **Logstash** reçoit et traite les événements avant leur envoi vers Elasticsearch.
- **Kibana** permet de rechercher les journaux et de construire des visualisations à partir des données d'Elasticsearch.

Des composants de collecte seront nécessaires sur les machines ou à proximité des services. Un **exporter** expose des métriques que Prometheus peut récupérer ; un collecteur de journaux transmet les événements vers la chaîne de centralisation. Le choix et la configuration de ces composants seront documentés lors du déploiement.

Cette séparation permet de construire une **observabilité unifiée à partir de données de natures différentes**. Pour rapprocher les informations, il faudra conserver des noms de machines et de services cohérents, synchroniser les horloges et consulter la même période dans les différents outils. Installer les outils ne suffit pas à établir automatiquement ces correspondances.

### Application au laboratoire

Les sources prévues sont la **VM Debian** et la **VM Windows Server**, hébergées sur le laptop et gérées avec **virt-manager**. Leurs métriques et journaux alimenteront la plateforme ; des sondes vérifieront les services effectivement retenus dans l'inventaire.

Une VM dédiée à la supervision reste envisagée. Cette feuille présente l'architecture logique du module, sans attester de son déploiement ni fixer encore l'emplacement de ses composants.

## À retenir

- Les **métriques** quantifient un état ou une performance et permettent d'en suivre l'évolution.
- Les **journaux** décrivent les événements et apportent du contexte pour rechercher une cause.
- Les **sondes** testent directement une disponibilité ou un fonctionnement ; leurs résultats peuvent être collectés sous forme de métriques.

[Retour au sommaire de l'itération](index.md)
