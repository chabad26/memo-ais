# Plateforme d’observabilité AlpesNet

Ce dossier contient la version publiable et reproductible de la plateforme déployée dans `~/observabilite` sur la VM `supervision`.

## Composants

- Prometheus et Grafana ;
- Elasticsearch, Logstash et Kibana ;
- Blackbox Exporter ;
- Alertmanager et le webhook pédagogique `alert-receiver` ;
- collecte Node Exporter et Windows Exporter ;
- sondes HTTP Linux et Windows ;
- règles d’infrastructure ;
- inject 18, inject 19 et simulateur des injects 11 à 17 et 20.

## Éléments volontairement absents

Le dépôt ne contient jamais :

- `.env` et les clés API Logstash ;
- les clés privées de la CA et des clients Beats ;
- les certificats propres au lab ;
- les données des volumes Docker ;
- les diagnostics, captures privées et sauvegardes de configuration ;
- les fichiers `.active` utilisés pour déclencher un scénario.

Le fichier `.env.example` documente seulement les noms des variables attendues. Les certificats doivent être régénérés avec `generer-certificats.sh` ou récupérés depuis l’instance locale appropriée sans les ajouter à Git.

## Adapter le réseau

Les adresses présentes correspondent au lab documenté :

| Élément | Adresse |
| --- | --- |
| VM de supervision | `192.168.122.80` |
| Endpoint Debian | `192.168.122.158` |
| Endpoint Windows Server Core | `192.168.122.25` |

Modifier `compose.override.yaml` et `prometheus/prometheus.yml` si le plan d’adressage change.

## Préparer les secrets localement

```bash
cp .env.example .env
chmod 600 .env
nano .env
```

Ne jamais afficher, capturer ou commiter le contenu final de `.env`.

## Générer les certificats Beats

```bash
chmod 700 generer-certificats.sh
./generer-certificats.sh 192.168.122.80
```

Le script refuse d’écraser un dossier `tls-beats` existant. Les clés générées restent ignorées par Git.

Le fichier `certs/http_ca.crt`, également ignoré, doit provenir de l’instance Elasticsearch utilisée par le déploiement.

## Valider les configurations

```bash
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  -f compose.inject19.yml \
  -f compose.simulateur.yml \
  config --quiet
```

```bash
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  -f compose.inject19.yml \
  -f compose.simulateur.yml \
  run --rm --no-deps --entrypoint promtool prometheus \
  check config /etc/prometheus/prometheus.yml
```

```bash
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  -f compose.inject19.yml \
  -f compose.simulateur.yml \
  run --rm --no-deps --entrypoint sh prometheus \
  -c 'for rules in /etc/prometheus/rules/*.yml; do promtool check rules "$rules" || exit 1; done'
```

## Démarrer la plateforme

```bash
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  -f compose.inject19.yml \
  -f compose.simulateur.yml \
  up -d
```

Vérifier ensuite :

```bash
curl --fail http://127.0.0.1:9090/-/ready
curl --fail http://127.0.0.1:9093/-/ready
curl --fail http://127.0.0.1:18082/health
curl --fail http://127.0.0.1:18080/health
curl --fail http://127.0.0.1:18083/health
```

## Documentation associée

Les procédures détaillées, les limites de preuve et les feuilles destinées à l’injecteur ou au diagnostiqueur se trouvent dans le module MkDocs `docs/supervision-optimisation-performances/` et dans le dossier parent `livrables/supervision-optimisation-performances/`.
