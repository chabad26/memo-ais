# Glossaire Intégration distribuée on-premise — Itération 7

## Sujet

Supervision de l'infrastructure avec Elasticsearch, Kibana et Filebeat.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Journal | Enregistrement horodaté d'un événement produit par un service. |
| Centralisation | Envoi de journaux de plusieurs sources vers une même plateforme. |
| Filebeat | Agent qui lit les journaux et les envoie à Elasticsearch. |
| Elasticsearch | Moteur qui indexe, stocke et recherche les événements. |
| Kibana | Interface qui permet de rechercher et visualiser les événements indexés. |
| Index | Ensemble d'événements stockés dans Elasticsearch. |
| KQL | Langage de requête utilisé dans Kibana pour filtrer les journaux. |
| Tableau de bord | Ensemble de visualisations de suivi. |
| Alerte | Notification déclenchée lorsqu'un événement dépasse un seuil. |
| Faux positif | Alerte sans action réellement nécessaire. |

## Manipulations faites

| Manipulation | Commande ou action |
| --- | --- |
| Démarrer la plateforme | `docker compose up -d` dans `~/on-premise/monitoring-compose` |
| Vérifier Elasticsearch | `curl http://127.0.0.1:9200/_cluster/health?pretty` |
| Vérifier Kibana | `curl -I http://127.0.0.1:5601` |
| Vérifier Filebeat | `docker compose exec filebeat filebeat test output -e` |
| Filtrer un service | KQL : `container.name: "mail-postfix"` |
| Rechercher un échec LDAP | KQL : `message: "err=49"` |
| Examiner une chronologie | Trier les événements par `@timestamp`, puis corréler les sources. |

## Points de vigilance

- La supervision doit être surveillée : une collecte Filebeat interrompue masque les incidents.
- Un conteneur actif peut redémarrer en boucle ; contrôler aussi ses journaux et redémarrages.
- Les alertes doivent avoir un seuil, un destinataire et une action connue.
- Les secrets et mots de passe ne doivent pas être indexés dans les journaux.
- Elasticsearch et Kibana sont limités à `127.0.0.1` dans le laboratoire ; TLS reste à activer avant exposition réseau.

## Docs associées

- [Vue d'ensemble de l'itération 7](../../../integration-distribuee-on-premise/it-7/index.md)
- [Déployer Elasticsearch et Kibana](../../../integration-distribuee-on-premise/it-7/deployer-elasticsearch-kibana.md)
- [Configurer la collecte Filebeat](../../../integration-distribuee-on-premise/it-7/configurer-collecte-filebeat.md)
- [Analyser un incident avec les journaux centralisés](../../../integration-distribuee-on-premise/it-7/analyser-incident-journaux-centralises.md)
- [Définir le plan d'alertes](../../../integration-distribuee-on-premise/it-7/definir-plan-alertes-exploitation.md)
