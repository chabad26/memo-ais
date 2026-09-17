# Itération 2 — Alerter et diagnostiquer les incidents

Cette itération transforme les données de supervision en alertes exploitables, puis les utilise pour rechercher les causes d’un incident. Elle réutilise obligatoirement la plateforme, les endpoints, les sondes, les journaux et les dashboards construits lors de l’itération 1.

## Fiches de l’itération

- [Mise en situation — Alerter et diagnostiquer les incidents](alerter-diagnostiquer-incidents.md) : contexte AlpesNet, problématique, périmètre et dossier.
- [Identifier les situations nécessitant une alerte](identifier-situations-alerte.md) : examiner les données, justifier l’intervention et sélectionner au moins trois situations.
- [Définir les seuils et la criticité](definir-seuils-criticite.md) : conditions, durées, impacts, actions et prise en compte des redémarrages du lab.

- [Configurer et tester les alertes](configurer-tester-alertes.md) : fichiers prêts à saisir, Alertmanager, notifications locales et essais CPU/IIS.

- [Construire la procédure de réponse — Livrable L3](construire-procedure-reponse.md) : revue des cinq alertes, variations temporaires, procédures, escalade et validation individuelle CA-06.

- [Partir d’une alerte pour rechercher ce qui s’est produit](partir-alerte-rechercher-situation.md) : cas IIS, chronologie, métriques, sondes, journaux et hypothèses.

- [Formuler et vérifier des hypothèses](formuler-verifier-hypotheses.md) : confronter les trois pistes IIS aux données et distinguer symptôme, cause et corrélation.

- [Corréler les métriques, les sondes et les journaux](correler-metriques-sondes-journaux.md) : reconstituer la chronologie IIS avant, pendant et après l’alerte.

- [Identifier la cause probable](identifier-cause-probable.md) : établir le diagnostic IIS, son niveau de confiance et l’action proportionnée.

- [Vérifier le retour à la normale](verifier-retour-normale.md) : comparer avant/après et confirmer le rétablissement fonctionnel du site IIS.

- [Préparer la mise en situation — Diagnostic autonome](preparer-mise-en-situation.md) : contrôler les prérequis en direct et préparer les traces avant le retrait du formateur.

- [Prendre en charge l’incident](prendre-en-charge-incident.md) : conduire le diagnostic inconnu de bout en bout, corréler les sources, agir et conserver les preuves du retour à la normale.

- [Guide du testeur — Diagnostiquer l’incident injecté](guide-testeur-diagnostic.md) : commandes de consultation, requêtes PromQL, journaux et démarche de résolution sans révéler les injects.

Le test CPU est documenté jusqu’au retour au nominal. Le cycle IIS est attesté de l’arrêt au rétablissement, avec `firing` et `resolved` reçus par le webhook. Kibana fournit un événement HttpService cohérent avec le retrait des URL HTTP. Les règles de collecte et de stockage et les variations temporaires restent à tester.

## Réutilisation et pense-bête

- [Itération 1 — Instrumenter et mesurer](../it-1/index.md)
- [Dashboards et livrable L2](../it-1/ameliorer-dashboards.md)
- [Pense-bête de l’itération 2](../../pense-bete/glossaire/supervision-optimisation-performances/it-2.md)

[Retour au module](../README.md)
