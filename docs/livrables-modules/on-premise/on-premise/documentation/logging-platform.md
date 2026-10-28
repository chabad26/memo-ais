# Déploiement Elasticsearch et Kibana


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/logging-platform.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.


## Configuration retenue

| Paramètre | Valeur |
|---|---|
| Projet | `~/on-premise/monitoring-compose` |
| Version Elastic | `9.3.1` pour Elasticsearch et Kibana |
| Mode Elasticsearch | nœud unique |
| Mémoire Java | 1 Gio minimum et maximum |
| API Elasticsearch | `http://127.0.0.1:9200` |
| Interface Kibana | `http://127.0.0.1:5601` |
| Volume | `monitoring_elasticsearch_data` |
| Réseau | `monitoring` |

La sécurité Elastic est désactivée uniquement pour ce déploiement fonctionnel
local. Les ports ne sont pas publiés sur le réseau. Avant toute exposition
externe, Elasticsearch et Kibana devront recevoir des certificats dédiés
Campus CA, une authentification et des comptes applicatifs limités.

## Vérifications

```bash
cd ~/on-premise/monitoring-compose
docker compose config
docker compose up -d
docker compose ps

curl http://127.0.0.1:9200/_cluster/health?pretty
curl -I http://127.0.0.1:5601
docker volume inspect monitoring_elasticsearch_data
```

## Test de redémarrage et de persistance

```bash
curl -X PUT http://127.0.0.1:9200/validation-persistance
docker compose down
docker compose up -d

curl http://127.0.0.1:9200/_cat/indices/validation-persistance?v
docker compose ps
```

Le test est réussi lorsque l'index `validation-persistance` est toujours
présent et que les deux services sont de nouveau démarrés. Il ne faut pas
utiliser `docker compose down -v`, car cette option supprime le volume.

## Résultats obtenus le 6 août 2026

| Vérification | Résultat | Preuve attendue |
|---|---|---|
| Elasticsearch opérationnel | Conforme | conteneur `healthy`, API accessible |
| Kibana accessible | Conforme | API Kibana accessible après démarrage |
| Volume persistant configuré | Conforme | volume `monitoring_elasticsearch_data` présent |
| Redémarrage réussi | Conforme | deux services actifs après `down` puis `up -d` |
| Index conservé | Conforme | index `validation-persistance` encore présent |

Après la création de l'index, le cluster est `yellow` : le shard primaire est
actif, mais sa réplique ne peut pas être attribuée sur un déploiement à un seul
nœud. Ce résultat est attendu pour le TP. Aucun message d'erreur de démarrage
n'a été relevé. L'avertissement Kibana concernant l'assistant IA indique
seulement qu'une licence supérieure serait nécessaire pour cette fonction.

## Captures à conserver

1. `docker compose ps` avec Elasticsearch et Kibana actifs ;
2. réponse de l'API `_cluster/health` ;
3. page d'accueil de Kibana dans le navigateur.
