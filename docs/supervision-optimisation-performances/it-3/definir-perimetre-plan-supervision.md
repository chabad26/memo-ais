# Définir le périmètre du plan de supervision

## Objectif de la séquence

À partir des éléments produits lors des itérations précédentes et des analyses de l'itération 3, construire un plan de supervision et d'exploitation cohérent, exploitable et adapté aux besoins de l'infrastructure.

Cette activité mobilise la compétence **CA-09 — Élaborer un plan de supervision et d'exploitation**.

Le plan doit permettre à un administrateur de savoir :

- quoi superviser ;
- quelles données collecter ;
- quels indicateurs suivre ;
- quelles situations doivent générer une alerte ;
- quelles actions entreprendre ;
- quelles opérations de maintenance prévoir ;
- comment faire évoluer le dispositif.

## Problématique

Comment transformer les éléments de supervision, les alertes, les procédures et les analyses de performance en un plan d'exploitation cohérent et durable ?

## 1. Principes de périmètre

Ne pas superviser tous les éléments de la même manière. Le niveau dépend de la criticité du service, de l'impact d'une indisponibilité, de la capacité à agir et de la qualité des données disponibles.

| Niveau | Usage | Exemple d'action |
| --- | --- | --- |
| Critique | Service indispensable ou perte d'exploitation immédiate | Alerte immédiate, procédure de réponse, escalade et vérification du rétablissement. |
| Renforcé | Risque important ou dégradation annonciatrice d'un incident | KPI fréquent, tendance, seuil d'avertissement et maintenance préventive. |
| Standard | Ressource utile dont la dégradation doit être connue | Dashboard, revue périodique et alerte si la condition persiste. |
| Référence | Élément utile au diagnostic ou à la comparaison | Collecte conservée, consultation à la demande, pas nécessairement d'alerte. |

## 2. Tableau du périmètre recommandé

Le tableau reprend l'environnement actuellement configuré : VM de supervision, endpoints Linux/Windows, sondes HTTP, journaux, alertes et simulateurs d'incidents. Les niveaux et seuils sont des choix de plan à confirmer avec le responsable Infrastructure.

| Asset / Service | Fonction | Données à collecter | KPI à suivre | Risque associé | Niveau de surveillance |
| --- | --- | --- | --- | --- | --- |
| VM `supervision` | Héberger Prometheus, Grafana, Alertmanager, Blackbox et la collecte | CPU, mémoire, espace disque, état Docker, disponibilité des ports, journaux des conteneurs | disponibilité de la plateforme, fraîcheur des scrapes, consommation CPU/mémoire, espace libre | perte de visibilité sur toute l'infrastructure et absence de notifications | Critique / renforcé |
| Prometheus | Collecter les métriques et évaluer les règles | `/api/v1/targets`, règles, erreurs de scrape, âge des séries, stockage TSDB | `up`, Targets en erreur, fraîcheur, règles `pending`/`firing`/`resolved` | diagnostic incomplet, alertes absentes ou fausses conclusions | Critique |
| Alertmanager et `alert-receiver` | Router et conserver les notifications | état de disponibilité, notifications reçues, erreurs de routage, logs du récepteur | délai de notification, notifications `firing` et `resolved`, alertes non routées | incident non transmis ou clôture non confirmée | Critique |
| Endpoint Debian | Fournir les métriques système et le service Nginx de test | CPU, mémoire disponible, filesystem, inodes, état service, journaux | `up`, CPU, mémoire, espace libre, `probe_success`, durée HTTP | ralentissement, saturation ou indisponibilité du service Linux | Renforcé |
| Windows Server Core | Fournir les métriques système et le service IIS de test | CPU, mémoire, volume `C:`, état IIS, événements Windows | `up`, CPU, mémoire, espace libre, disponibilité IIS, durée et statut HTTP | indisponibilité applicative et perte de visibilité Windows | Renforcé |
| Sondes HTTP Linux/Windows | Vérifier le fonctionnement depuis la supervision | `probe_success`, statut HTTP, contenu attendu, durée, erreur Blackbox | succès de sonde, latence, taux d'échec, fraîcheur | `up=1` pourrait masquer un service HTTP réellement indisponible | Critique pour les services exposés |
| Journaux Linux et Windows | Fournir le contexte des incidents et changements d'état | journald, événements Windows, horodatage, hôte, fournisseur, niveau, message | erreurs par période, événements de service, fraîcheur et continuité d'ingestion | cause introuvable, diagnostic retardé ou incomplet | Renforcé |
| `logstash-logs`, Elasticsearch, Kibana | Centraliser, rechercher et visualiser les journaux | état des pipelines, indexation, santé Elasticsearch, volume et rétention | délai d'ingestion, documents reçus, erreurs pipeline, état cluster | perte ou retard des journaux nécessaires au diagnostic | Critique / renforcé |
| Stockage des endpoints et de la supervision | Conserver données, journaux et volumes Docker | octets libres, inodes, croissance, rétention, erreurs d'écriture | occupation, vitesse de croissance, durée d'écriture, marge restante | saturation, perte de collecte et échec des services | Renforcé |
| Réseau de supervision | Relier collecteurs, endpoints, journaux et sondes | disponibilité, latence, erreurs, ports, flux TLS Beats | erreurs réseau, latence, succès des connexions, continuité des flux | données absentes ou services considérés à tort comme indisponibles | Renforcé |
| Simulateur et injects | Tester les alertes et procédures sans production | métriques scénarisées, état des fichiers `.active`, logs et horaires | cohérence avant/pendant/après, retour au nominal, délai de détection | test non reproductible ou preuve confondue avec une observation réelle | Standard / référence |

## 3. Questions de périmètre

### Quels éléments sont indispensables ?

La VM de supervision, Prometheus, Alertmanager, les collecteurs des endpoints et les sondes sont indispensables à la visibilité et à la détection. Les endpoints Linux et Windows portent les services observés. Elasticsearch, Logstash et Kibana sont indispensables au diagnostic par les journaux, même si une indisponibilité temporaire de Kibana ne signifie pas nécessairement que les services métiers sont arrêtés.

### Quels éléments peuvent avoir un impact important ?

Une perte de l'endpoint, l'arrêt d'un service HTTP, une perte de Prometheus ou d'Alertmanager, une saturation du stockage et une rupture d'ingestion Logstash peuvent empêcher l'exploitation ou retarder la détection. L'impact doit être distingué : service réellement indisponible, visibilité perdue ou diagnostic rendu incomplet.

### Quels éléments nécessitent uniquement une surveillance ?

Le simulateur et les injects sont des outils de test : ils nécessitent une vérification avant et après un exercice, mais ne doivent pas produire d'alerte de production permanente. Certains indicateurs de référence, comme la version ou le nombre de séries, peuvent être suivis lors des revues sans alerte immédiate.

### Quels éléments nécessitent une alerte ?

La perte de collecte, l'échec d'une sonde fonctionnelle, l'absence de notification, une saturation de stockage, une charge durablement élevée et une erreur persistante d'ingestion justifient une alerte si la condition, la durée et le responsable sont définis.

### Quelles données sont réellement utiles ?

Les données utiles sont celles qui permettent de qualifier un état, une tendance, un impact ou une cause : valeurs horodatées, labels de cible, fraîcheur, durée, statut de sonde, événements de service, erreurs de collecte et journaux corrélables. Une donnée sans unité, période ou cible est difficilement exploitable.

### Existe-t-il des éléments insuffisamment supervisés ?

Oui, à confirmer par les mesures runtime : la mémoire et l'activité réseau réelle des endpoints ne sont pas couvertes par les scénarios du simulateur ; la capacité et la croissance des volumes doivent être suivies sur plusieurs jours ; le délai complet entre alerte, notification et réception doit être mesuré ; la continuité des journaux doit être surveillée au-delà d'un simple test d'indexation.

### Que renforcer après les incidents ?

Renforcer la fraîcheur de collecte, les notifications `firing`/`resolved`, le suivi de Logstash, les sondes fonctionnelles distinctes de `up`, la capacité des volumes et la traçabilité des heures. Les incidents de perte de journaux et le cycle IIS ont montré que l'état d'un conteneur ou d'une interface ne suffit pas à prouver le fonctionnement complet.

## 4. Consolidation L1, L2 et L3

| Production existante | Dispositif déjà présent | Écart ou amélioration recommandée |
| --- | --- | --- |
| L1 — données et collecte | Exporters Linux/Windows, sondes HTTP, journaux et Prometheus configurés | Ajouter un KPI explicite de fraîcheur et de continuité des données ; `up=1` seul ne valide ni le service ni l'ingestion complète. |
| L2 — dashboards | Dashboards Grafana et Kibana présentant métriques et événements | Ajouter une vue de capacité, une baseline, l'âge du dernier point et un statut clair « données absentes » ; distinguer consultation historique et collecte actuelle. |
| L3 — alertes et procédures | Cinq alertes, criticités, procédures, tests CPU/IIS et retour nominal documenté | Compléter les preuves des règles restantes, mesurer les délais de notification et rattacher chaque seuil à une action et une maintenance. |
| L4 — diagnostic | Corrélation métriques, sondes, journaux et hypothèses | Ajouter le périmètre, les propriétaires, les limites de collecte et le registre des améliorations dans le plan durable. |

Les deux écarts prioritaires à retenir sont donc :

1. **Capacité et tendances insuffisamment couvertes** : les dashboards et alertes montrent surtout l'état courant ; il faut ajouter croissance, marge, échéance estimée et fraîcheur.
2. **Chaîne de notification et d'ingestion à prouver de bout en bout** : une règle `firing`, un message envoyé et un message reçu sont trois preuves différentes ; même distinction pour un journal produit, ingéré et retrouvé dans Kibana.

## 5. Niveau de surveillance et exploitation quotidienne

| Fréquence | Contrôles recommandés |
| --- | --- |
| À chaque prise de service | état des conteneurs, Prometheus/Alertmanager prêts, Targets, sondes, fraîcheur des métriques et journaux récents. |
| Toutes les 30 secondes | scrapes des endpoints et sondes selon la configuration actuelle. |
| Toutes les 5 secondes pendant un test | métriques du simulateur et de l'inject ; conserver l'heure de début et de fin. |
| Quotidienne | alertes actives, erreurs de collecte, croissance du stockage, erreurs de journaux, notifications reçues et services critiques. |
| Hebdomadaire | tendances CPU/mémoire/stockage, capacité, qualité des dashboards, rétention et procédures non rejouées. |
| Après incident ou changement | comparaison avant/après, retour nominal, stabilité, mise à jour du dossier et décision de maintenance. |

## 6. Question de transition

Une fois le périmètre défini, l'exploitation durable doit organiser chaque KPI avec une unité, une baseline, une période, un seuil, une durée, une criticité, un responsable et une procédure. Le plan final doit relier :

```text
Asset / service
    -> données collectées
    -> KPI et baseline
    -> seuil et durée
    -> alerte et destinataire
    -> procédure et escalade
    -> maintenance préventive
    -> preuve de retour et revue
```

La prochaine étape consiste à transformer ce périmètre en catalogue opérationnel des KPI, seuils, alertes et procédures, puis à intégrer les décisions dans le dossier d'exploitation.

## Livrable attendu

Un périmètre hiérarchisé, un tableau des assets et services, les données réellement utiles, les niveaux de surveillance, au moins deux écarts entre L1/L2/L3 et le dispositif recommandé, ainsi que les priorités d'amélioration.

[Formaliser le dossier d'exploitation](formaliser-dossier-exploitation.md) · [Retour au sommaire](index.md)
