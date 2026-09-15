# Itération 1 — Instrumenter et mesurer l'infrastructure

Cette première itération porte sur la mise en place d'une observation centralisée de l'infrastructure de préproduction d'AlpesNet : intégration des systèmes, collecte des métriques, centralisation des journaux et contrôle de la disponibilité des services.

## Fiches de l'itération

- [Cadrage de la mission — Instrumenter et mesurer l'infrastructure](instrumenter-mesurer-infrastructure.md) : contexte, objectifs, périmètre et dossier de déploiement à constituer.
- [Identifier les éléments à observer](identifier-elements-observer.md) : laboratoire virt-manager, tableau d'observation et questions d'exploitation.
- [Classer les informations de supervision selon leur utilisation](classer-informations-supervision.md) : état, performances, recherche des causes et collecte minimale Linux/Windows.
- [Comprendre l'observabilité — mots clés et architecture](comprendre-observabilite.md) : métriques, journaux, sondes et rôles de Prometheus, Grafana et ELK.

- [Déployer et valider la plateforme d'observabilité](deployer-plateforme-observabilite.md) : installation, tests fonctionnels et dossier d'exploitation.

- [Intégrer les endpoints Linux et Windows Server Core](integrer-endpoints-linux-windows.md) : exporters, PowerShell, cibles Prometheus et validation.

- [Créer et configurer les sondes](creer-configurer-sondes.md) : contrôles HTTP Linux/Windows Core, indisponibilité et rétablissement.

- [Ajouter une source de logs](ajouter-source-logs.md) : journald, événements Windows, collecte TLS et recherche dans ELK.

- [Construire un premier dashboard Grafana](construire-dashboard-grafana.md) : KPI, visualisations, import, unités et validation sur Linux/Windows.
- [Construire un dashboard Kibana](construire-dashboard-kibana.md) : cinq panneaux, événements Linux/Windows, recherches et validation.
- [Améliorer les dashboards — Livrable L2](ameliorer-dashboards.md) : audit, améliorations, preuves et validation individuelle CA-05.

- [Simulation croisée — Vérifier le dispositif d’observabilité](simulation-croisee-observabilite.md) : état nominal, KPI, événements confidentiels et observation par un autre binôme.

[Retour au module](../README.md)

## Pense-bête

- [Termes et gestes à retenir](../../pense-bete/glossaire/supervision-optimisation-performances/it-1.md)
