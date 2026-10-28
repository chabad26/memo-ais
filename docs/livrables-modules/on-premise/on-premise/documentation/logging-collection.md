# Collecte centralisée avec Filebeat


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/logging-collection.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Architecture mise en œuvre

```text
Logs JSON Docker ----\
                      -> Filebeat -> logs-infrastructure -> Elasticsearch
Journaux BorgBackup -/                                      -> Kibana
```

Filebeat utilise la même version `9.3.1` qu'Elasticsearch et Kibana. Il est
déployé dans `monitoring-compose` et attend que le contrôle de santé
Elasticsearch soit réussi.

## Sources configurées

| Input | Chemin dans Filebeat | Contenu |
|---|---|---|
| `docker-containers` | `/var/lib/docker/containers/*/*.log` | Docker, Postfix, Dovecot, OpenLDAP, Samba et les autres conteneurs |
| `borgbackup-files` | `/var/log/borgbackup/*.log` | sauvegardes Borg et `last-run.status` |

Le parseur `container` retire l'enveloppe JSON du pilote Docker et conserve le
message, le flux et l'horodatage. `add_docker_metadata` ajoute notamment
`container.name`, `container.image.name` et les labels. Les journaux Filebeat
sont exclus pour ne pas être collectés par Filebeat lui-même.

Dovecot a été configuré avec `log_path = /dev/stderr` et
`info_log_path = /dev/stdout`. Ses événements deviennent ainsi des journaux
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]

## Fichiers et volumes

- `monitoring-compose/filebeat.yml` : inputs, processeurs et sortie ;
- `monitoring-compose/compose.yaml` : conteneur et montages ;
- `monitoring_filebeat_data` : registre des fichiers et positions lus ;
- `monitoring_elasticsearch_data` : événements indexés.

## Vérifications techniques

```bash
cd ~/on-premise/monitoring-compose
docker compose config
docker compose up -d
docker compose ps

docker compose exec filebeat filebeat test config -e
docker compose exec filebeat filebeat test output -e
docker compose logs --tail=100 filebeat

curl 'http://127.0.0.1:9200/_cat/indices/logs-infrastructure*?v'
```

Compter les événements par source :

```bash
curl -s http://127.0.0.1:9200/logs-infrastructure*/_search \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 0,
    "aggs": {
      "conteneurs": {
        "terms": {"field": "container.name", "size": 20}
      },
      "sources": {
        "terms": {"field": "log_source", "size": 10}
      }
    }
  }'
```

## Consultation dans Kibana

1. Ouvrir <http://127.0.0.1:5601>.
2. Ouvrir **Stack Management**, puis **Data Views**.
3. Créer la vue `logs-infrastructure*`.
4. Choisir `@timestamp` comme champ temporel.
5. Ouvrir **Discover** et sélectionner cette vue.
6. Filtrer avec `container.name: mail-postfix`,
   `container.name: mail-dovecot`, `container.name: openldap`,
   `container.name: samba-ldap` ou `service.name: borgbackup`.

La vue **Journaux infrastructure**, associée au motif
`logs-infrastructure*` et au champ temporel `@timestamp`, a également été
créée par l'API Kibana :

```bash
curl -X POST http://127.0.0.1:5601/api/data_views/data_view \
  -H 'kbn-xsrf: true' \
  -H 'Content-Type: application/json' \
  -d '{
    "data_view": {
      "title": "logs-infrastructure*",
      "name": "Journaux infrastructure",
      "timeFieldName": "@timestamp"
    }
  }'
```

## Sécurité

Filebeat s'exécute comme `root` pour lire `/var/lib/docker/containers`. Le
socket Docker est nécessaire à l'enrichissement des événements mais donne un
accès puissant à l'hôte. Le montage est acceptable pour le TP avec l'image
officielle contrôlée ; il doit être réévalué et protégé en production.

TLS et un compte Filebeat limité devront remplacer la connexion HTTP anonyme
avant toute exposition réseau.

## Résultats du 6 août 2026 à 16 h 19

| Service | Filtre Kibana | Journaux reçus |
|---|---|---|
| Docker | `log_source: docker` | Oui, 4 720 événements |
| Postfix | `container.name: mail-postfix` | Oui, 608 événements |
| Dovecot | `container.name: mail-dovecot` | Oui, 9 événements |
| OpenLDAP | `container.name: openldap` | Oui, 1 043 événements |
| Samba | message `liaison LDAP administrateur refusée` | Oui, 6 événements |
| BorgBackup | `service.name: borgbackup` | Oui, 210 événements |

Les nombres constituent un instantané et augmentent avec l'activité. Samba
était arrêté avant le démarrage de Filebeat : ses lignes sont indexées depuis
le fichier JSON historique, mais le processeur Docker ne lui a pas associé de
nom de conteneur actif. La recherche utilise donc ici le message d'erreur
Samba. Lors d'un prochain démarrage réussi, les nouveaux événements recevront
automatiquement `container.name: samba-ldap`.

## Anomalies corrigées

| Symptôme | Cause | Correction |
|---|---|---|
| erreur initiale `no matching index template` | le motif `logs-infrastructure-*` ne couvrait pas le data stream de base | motif élargi à `logs-infrastructure*` et template rechargé |
| aucun événement Dovecot | Dovecot n'écrivait pas dans les sorties du conteneur | `log_path` vers `stderr` et `info_log_path` vers `stdout` |
| lecture différée des très petits fichiers | `filestream` attend par défaut une empreinte de 1 024 octets | plusieurs événements de test non sensibles ont été générés |
| avertissement TLS | Elasticsearch fonctionne encore en HTTP local | attendu pour le TP ; TLS sera ajouté avant exposition réseau |
