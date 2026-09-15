# Supervision et optimisation des performances

Ce module vise à mettre en place une plateforme d'observabilité pour suivre une infrastructure, détecter les incidents et analyser les performances. Il associe la collecte de métriques, la centralisation des journaux et les sondes de contrôle pour construire une supervision utile à l'exploitation.

## Objectifs

**À l'issue de ce module, l'apprenant est capable de :**

- Déployer une plateforme d'observabilité reposant sur Prometheus, Grafana et ELK
- Intégrer des endpoints Linux et Windows dans une plateforme de supervision
- Créer et configurer des sondes permettant de vérifier la disponibilité, l'état et le fonctionnement des services
- Ajouter et exploiter des sources de journaux dans une plateforme d'observabilité
- Construire des tableaux de bord adaptés aux besoins de l'exploitation et du pilotage
- Configurer des alertes pertinentes et définir les procédures de réponse associées
- Diagnostiquer un incident en corrélant métriques, journaux et données issues des sondes
- Analyser les performances et identifier les besoins de maintenance préventive ou d'optimisation
- Élaborer un plan de supervision et d'exploitation réutilisable dans un contexte professionnel

## Itérations disponibles

### Itération 1 — Instrumenter et mesurer l'infrastructure

- [Sommaire de l'itération](it-1/index.md)
- [Cadrage de la mission — Instrumenter et mesurer l'infrastructure](it-1/instrumenter-mesurer-infrastructure.md)
- [Identifier les éléments à observer](it-1/identifier-elements-observer.md)
- [Classer les informations de supervision selon leur utilisation](it-1/classer-informations-supervision.md)
- [Comprendre l'observabilité — mots clés et architecture](it-1/comprendre-observabilite.md)
- [Déployer et valider la plateforme d'observabilité](it-1/deployer-plateforme-observabilite.md)
- [Intégrer les endpoints Linux et Windows Server Core](it-1/integrer-endpoints-linux-windows.md)

- [Créer et configurer les sondes](it-1/creer-configurer-sondes.md)

- [Ajouter une source de logs](it-1/ajouter-source-logs.md)

- [Construire un premier dashboard Grafana](it-1/construire-dashboard-grafana.md)
- [Construire un dashboard Kibana](it-1/construire-dashboard-kibana.md)
- [Améliorer les dashboards — Livrable L2](it-1/ameliorer-dashboards.md)
- [Simulation croisée — Vérifier le dispositif d’observabilité](it-1/simulation-croisee-observabilite.md)

## Sommaire prévisionnel

Cette progression est proposée à partir des objectifs du module. Les fiches et les itérations seront ajoutées au fil des activités ; les thèmes ci-dessous ne représentent pas des travaux déjà réalisés.

| Partie | Thème | Travail prévu |
| --- | --- | --- |
| 1 | Plateforme d'observabilité | Préparer et déployer le socle Prometheus, Grafana et ELK. |
| 2 | Supervision Linux et Windows | Intégrer les machines supervisées et vérifier la remontée des métriques. |
| 3 | Sondes de contrôle | Vérifier la disponibilité, l'état et le fonctionnement des services. |
| 4 | Centralisation des journaux | Ajouter des sources, organiser les événements et exploiter les recherches. |
| 5 | Tableaux de bord | Présenter les indicateurs utiles aux équipes d'exploitation et au pilotage. |
| 6 | Alertes et procédures de réponse | Définir les conditions de déclenchement, les destinataires et les actions associées. |
| 7 | Diagnostic d'incident | Croiser les métriques, les journaux et les résultats des sondes pour rechercher la cause. |
| 8 | Performances et maintenance préventive | Identifier les points de saturation, proposer des améliorations et mesurer leurs effets. |
| 9 | Plan de supervision et d'exploitation | Regrouper le périmètre, les indicateurs, les alertes et les procédures dans un document réutilisable. |

## Fil conducteur

Partir des services à surveiller et des besoins de l'exploitation, puis construire progressivement la collecte, les contrôles, les tableaux de bord et les alertes. Les données recueillies serviront ensuite à diagnostiquer les incidents et à justifier les optimisations.

Chaque activité permettra de conserver les configurations utiles, les vérifications effectuées et les résultats observés. Les procédures prévues et les exemples seront distingués des manipulations effectivement réalisées.

## Livrables envisagés

- Une documentation de la plateforme et des machines Linux et Windows intégrées.
- Un inventaire des sondes, des métriques et des sources de journaux.
- Des tableaux de bord documentés selon leur public et leur usage.
- Un catalogue d'alertes accompagné des procédures de réponse.
- Une analyse d'incident et un bilan de performances appuyés sur des observations.
- Un plan de supervision et d'exploitation réutilisable en contexte professionnel.

## Pense-bête du module

- [Itération 1](../pense-bete/glossaire/supervision-optimisation-performances/it-1.md)
