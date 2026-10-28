# Plateforme de journalisation


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/monitoring-compose/README.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.


Le rôle du Compose, du healthcheck, du volume et du réseau est détaillé dans
[`../documentation/technical-files-guide.md`](../documentation/technical-files-guide.md).

Pile de travaux pratiques composée d'un nœud Elasticsearch, de Kibana et de
Filebeat.

## Rôle des fichiers

| Fichier | Rôle |
|---|---|
| `compose.yaml` | démarre les trois services, les volumes et le réseau |
| `filebeat.yml` | définit les fichiers lus, les métadonnées et l'index cible |
| `kibana/dashboards.ndjson` | export reproductible des tableaux de bord Kibana |
| `.env` | fixe localement la version et les ports |
| `.env.example` | documente les variables attendues |

Filebeat lit les fichiers JSON produits par le pilote Docker `json-file` et
les journaux `../backup/logs`. Son volume `monitoring_filebeat_data` conserve
le registre de lecture : après un redémarrage, il reprend au dernier octet lu au
lieu de réindexer tous les fichiers.

## Prérequis

```bash
sysctl vm.max_map_count
free -h
docker compose config
```

La valeur recommandée pour `vm.max_map_count` est `1048576`.

## Démarrage

```bash
docker compose up -d
docker compose ps
curl http://127.0.0.1:9200/_cluster/health?pretty
curl -I http://127.0.0.1:5601
curl 'http://127.0.0.1:9200/_cat/indices/logs-infrastructure*?v'
```

Kibana est accessible sur <http://127.0.0.1:5601>.

## Persistance et redémarrage

```bash
docker volume inspect monitoring_elasticsearch_data
docker compose down
docker compose up -d
docker compose ps
```

Ne pas ajouter l'option `-v` à `docker compose down` : elle supprimerait le
volume Elasticsearch.

## Journaux

```bash
docker compose logs --tail=100 elasticsearch
docker compose logs --tail=100 kibana
docker compose logs --tail=100 filebeat
docker compose exec filebeat filebeat test config -e
docker compose exec filebeat filebeat test output -e
```

Dans Kibana, créer la vue de données `logs-infrastructure*` avec
`@timestamp` comme champ temporel. Les services Docker se filtrent avec
`container.name` et BorgBackup avec `service.name: borgbackup`.

Les cinq tableaux de bord de supervision sont décrits dans
[`../documentation/monitoring-dashboards.md`](../documentation/monitoring-dashboards.md).
Pour les restaurer :

```bash
curl -X POST 'http://127.0.0.1:5601/api/saved_objects/_import?overwrite=true' \
  -H 'kbn-xsrf: true' \
  --form file=@kibana/dashboards.ndjson
```

## Sécurité

Les ports sont liés à `127.0.0.1`. La sécurité Elastic est temporairement
désactivée pour valider le fonctionnement local. TLS et l'authentification
devront être activés avec les certificats de `step-ca` avant toute exposition
sur le réseau.

Le socket `/var/run/docker.sock` est monté pour que `add_docker_metadata`
retrouve le nom, l'image et les labels de chaque conteneur. Même monté en
lecture seule, ce socket donne un accès très puissant à l'API Docker. Filebeat
doit donc rester une image officielle, avec une configuration contrôlée. Une
collecte distante ou un agent installé sur l'hôte est préférable en production.
