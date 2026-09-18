# Rechercher les évolutions significatives

## Objectif

À partir des données disponibles dans la plateforme d'observabilité, rechercher des évolutions qui dépassent la simple photographie d'un état. L'objectif est de distinguer une variation ordinaire d'un signal qui peut révéler une dégradation future.

Une observation doit toujours préciser la cible, la période, l'unité, la fréquence attendue et la source utilisée. Une capture isolée ne suffit pas à prouver une tendance.

## Travail demandé

Rechercher des évolutions significatives concernant :

- le CPU ;
- la mémoire ;
- le stockage ;
- la disponibilité ou le temps de réponse des services ;
- l'activité réseau lorsque les données sont disponibles ;
- les événements ou erreurs présents dans les journaux.

Utiliser les dashboards, Prometheus, les sondes et Kibana. Comparer si possible une cible observée avec une cible témoin et conserver les requêtes ou filtres employés.

## Vérifier les données avant d'interpréter

Avant de remplir le tableau :

1. noter la période exacte et le fuseau horaire ;
2. vérifier que les points sont suffisamment nombreux et régulièrement espacés ;
3. contrôler la fraîcheur et les éventuels trous de collecte ;
4. confirmer l'unité et les labels de la série ;
5. rapprocher métriques, sondes et journaux sur une période commune ;
6. distinguer une valeur nulle d'une donnée absente.

Requêtes de départ à adapter aux labels réellement présents :

```promql
up{job=~"linux|windows|sonde_.*"}
```

```promql
probe_success{job=~"sonde_.*"}
```

```promql
probe_duration_seconds{job=~"sonde_.*"}
```

```promql
node_filesystem_avail_bytes{mountpoint="/",fstype!="tmpfs"}
```

```promql
windows_logical_disk_free_bytes{volume="C:"}
```

```promql
100 * (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)
```

Si les métriques réseau détaillées ne sont pas disponibles, l'indiquer explicitement et exploiter les erreurs, la latence ou les journaux réseau disponibles. Ne pas inventer une évolution à partir d'une donnée absente.

## Relevé à partir du lab disponible

Le Compose du lab confirme une collecte Prometheus toutes les 30 secondes pour Linux, Windows et les sondes HTTP, et toutes les 5 secondes pour le simulateur et l'inject 18. Prometheus conserve au maximum 3 jours ou 1 Go. Les valeurs ci-dessous doivent donc être lues comme un relevé de travail : elles s'appuient sur le code du simulateur et les preuves déjà conservées, mais ne remplacent pas une capture prise pendant une nouvelle exécution.

| Élément observé | Période étudiée | Évolution constatée | Situation | Risque potentiel |
| --- | --- | --- | --- | --- |
| CPU | 16 septembre 2026, test Debian documenté dans l'itération 2 | CPU proche de 100 % pendant le stress, puis retour près de zéro après l'arrêt ; aucune dérive longue n'est documentée. | Variation ponctuelle ; surveillance particulière si le phénomène revient hors test. | Ralentissement, contention ou indisponibilité si la charge devient récurrente. |
| Mémoire | Période disponible dans Prometheus : au plus 3 jours, relevé à refaire avec plusieurs points | Le simulateur n'expose pas de métrique mémoire ; aucune tendance mémoire ne peut être démontrée à partir des fichiers fournis. | Surveillance particulière : donnée manquante pour conclure. | Une baisse progressive pourrait conduire au swap, à un OOM ou à une instabilité avant qu'une alerte existe. |
| Stockage | Scénario simulé 17, pendant l'activation du fichier `17-disque.active` | `lab_storage_operation_duration_seconds` passe de `0,03 s` à `3,2 s` pour une écriture ; retour à `0,03 s` après désactivation. | Variation ponctuelle injectée, pas dégradation progressive démontrée. | Latence applicative et erreurs d'écriture si la lenteur devient persistante ; capacité disque réelle non mesurée par ce scénario. |
| Disponibilité ou temps de réponse d'un service | 16 septembre 2026, cycle IIS documenté ; scénarios simulateur 11, 17 et 19 disponibles | IIS : `probe_success` est passé de `1` à `0`, puis à `1`, avec HTTP 200 au retour. Le simulateur prévoit DNS à `3 s`, écriture à `3,2 s` et dépendance 19 indisponible, mais ces activations doivent être horodatées. | Variation ponctuelle attestée pour IIS ; autres cas à tester. | Une répétition ou une hausse de durée avant l'échec annoncerait une dégradation progressive du service. |
| Activité réseau, si disponible | Scénario simulé 12, pendant l'activation du fichier `12-reseau.active` | `lab_network_receive_errors_rate` passe de `0` à `12 erreurs/s` et `lab_network_latency_seconds` de `0,01 s` à `1,2 s`, puis revient au nominal. Aucune tendance réseau réelle longue n'est fournie. | Variation ponctuelle injectée. | Retransmissions, ralentissements et indisponibilité d'une dépendance ; vérifier l'interface et le chemin réseau avant d'accuser l'application. |
| Événements ou erreurs des journaux | 14–16 septembre 2026, marqueurs Linux/Windows et reprise Logstash documentés | Les marqueurs `ALPESNET_LOG_LINUX_20260914T140642Z` et `ALPESNET_LOG_WINDOWS_20260914T141352Z` ont été retrouvés. Le 16 septembre, une perte de connexion vers `192.168.122.80:5044` a été suivie d'une reprise après démarrage de `logstash-logs`. | Événement ponctuel et incident de collecte ; continuité longue non démontrée. | Perte de visibilité, diagnostic incomplet ou retard de détection si la collecte des journaux s'interrompt à nouveau. |

### Limites de ce relevé

- Les valeurs du simulateur sont des états activés/désactivés, pas des séries de croissance naturelle. Elles servent à vérifier la détection et le retour au nominal.
- Les fichiers Compose ne prouvent pas qu'un scénario a été activé. Pour chaque scénario, conserver l'heure d'activation, plusieurs scrapes, l'alerte éventuelle et l'heure du retour.
- La mémoire et l'activité réseau des endpoints réels nécessitent une nouvelle consultation de Prometheus ; le simulateur ne suffit pas pour ces deux tendances.
- Une vraie dégradation progressive du stockage demande plusieurs mesures d'espace libre ou de croissance, pas seulement le scénario de latence d'écriture.

## Tableau à compléter

| Élément observé | Période étudiée | Évolution constatée | Situation | Risque potentiel |
| --- | --- | --- | --- | --- |
| CPU |  |  | Stable / ponctuelle / tendance / dégradation progressive / surveillance particulière |  |
| Mémoire |  |  | Stable / ponctuelle / tendance / dégradation progressive / surveillance particulière |  |
| Stockage |  |  | Stable / ponctuelle / tendance / dégradation progressive / surveillance particulière |  |
| Disponibilité ou temps de réponse d'un service |  |  | Stable / ponctuelle / tendance / dégradation progressive / surveillance particulière |  |
| Activité réseau, si disponible |  |  | Stable / ponctuelle / tendance / dégradation progressive / surveillance particulière |  |
| Événements ou erreurs des journaux |  |  | Stable / ponctuelle / tendance / dégradation progressive / surveillance particulière |  |

Pour chaque ligne, joindre ou référencer la preuve utile : panneau, requête PromQL, filtre KQL, capture datée ou export. Si aucune évolution significative n'est démontrée, écrire « aucune tendance démontrée sur la période étudiée » plutôt que de forcer une conclusion.

## Classer la situation

| Situation | Indice principal | Conclusion prudente |
| --- | --- | --- |
| Stable | Variations limitées autour d'un niveau habituel | Continuer la surveillance selon la fréquence prévue. |
| Variation ponctuelle | Écart bref sans répétition ni dérive | Rechercher le contexte et vérifier le retour au niveau habituel. |
| Tendance | Évolution répétée dans une même direction sur plusieurs points | Mesurer la vitesse et rechercher la capacité restante. |
| Dégradation progressive | Tendance accompagnée d'un impact croissant sur le service | Préparer une action avant le seuil critique. |
| Surveillance particulière | Donnée inhabituelle, incertaine, intermittente ou incomplète | Améliorer la collecte ou rapprocher les sources avant de conclure. |

## Questions à traiter

### Une valeur actuellement normale peut-elle révéler une future dégradation ?

Oui. Une valeur peut rester sous son seuil tout en augmentant régulièrement. La marge disponible, la vitesse d'évolution et la capacité restante permettent d'anticiper le moment où la situation deviendra problématique.

### Comment distinguer une variation ponctuelle d'une tendance ?

Comparer plusieurs points sur une période adaptée, rechercher la répétition et vérifier le contexte. Une variation ponctuelle revient vers le niveau habituel ; une tendance conserve une direction ou se répète selon un cycle identifiable.

### Quelle période faut-il observer ?

Elle dépend du phénomène : minutes ou heures pour une latence et une charge, jours pour une consommation de stockage, et plusieurs cycles pour une activité périodique. La période doit être assez longue pour éviter de confondre incident bref et comportement habituel.

### Quels indicateurs doivent être analysés ensemble ?

CPU, mémoire, stockage, disponibilité, durée de sonde, erreurs et journaux doivent être rapprochés lorsque le service est dégradé. Il faut aussi comparer `up` avec `probe_success` : la collecte d'une sonde peut fonctionner alors que le service contrôlé échoue.

### Une augmentation régulière constitue-t-elle nécessairement un problème ?

Non. Elle peut correspondre à une croissance prévue, une sauvegarde, une activité métier ou une période normale. Elle devient un risque lorsque la capacité restante, l'impact, la vitesse ou l'échéance ne sont plus compatibles avec l'exploitation.

### À partir de quel moment une tendance doit-elle entraîner une action ?

Lorsqu'elle est suffisamment établie, reliée à un risque et proche d'une condition d'intervention définie. L'action peut d'abord consister à améliorer la collecte, augmenter la fréquence d'observation, créer une alerte ou planifier une maintenance ; elle ne doit pas attendre l'incident.

## Sélection pour l'activité suivante

Choisir une tendance ou une dégradation qui mérite une analyse plus approfondie. Justifier le choix avec le tableau suivant :

| Élément retenu | Pourquoi est-il significatif ? | Sources à corréler | Question à vérifier ensuite | Action provisoire |
| --- | --- | --- | --- | --- |
| Temps de réponse de l'opération d'écriture du scénario 17 | La durée simulée passe de `0,03 s` à `3,2 s`, soit environ 100 fois plus, ce qui peut annoncer une dégradation applicative avant une indisponibilité. | `lab_storage_operation_duration_seconds`, CPU/mémoire de l'endpoint, journaux du simulateur et sonde du service. | La hausse est-elle limitée à une activation du scénario ou se reproduit-elle sur plusieurs périodes ? Quelle ressource ou dépendance explique la latence ? | Rejouer le scénario avec des horaires consignés, vérifier la durée avant/pendant/après et préparer une alerte seulement après avoir établi une baseline. |

La sélection doit privilégier une évolution documentée, mesurable et reliée à un risque. Elle servira de base à [l'analyse des tendances et de la capacité](analyser-tendances-capacite.md), où seront étudiées la vitesse d'évolution, la capacité restante, le goulet éventuel et l'échéance d'action.

## Livrable attendu

Un tableau renseigné et sourcé, les réponses aux questions, puis une évolution sélectionnée pour la suite. Les observations non concluantes, les données manquantes et les limites de la plateforme doivent être conservées dans le compte rendu.

[Retour au sommaire de l'itération](index.md) · [Pense-bête](../../pense-bete/glossaire/supervision-optimisation-performances/it-3.md)
