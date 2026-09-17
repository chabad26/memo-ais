# Guide du testeur — Diagnostiquer l’incident injecté

## Objectif

Prendre en charge un incident inconnu à partir du signal initial, rechercher sa cause probable, proposer une action adaptée et démontrer le retour à la normale.

Cette feuille fournit des pistes et des commandes de **consultation**. Elle ne donne ni la cause de l’incident, ni le mécanisme d’injection, ni les résultats attendus par l’injecteur.

!!! warning "Avant toute action"
    Conserver le signal et les premières observations avant de modifier l’environnement. Ne pas arrêter toute la plateforme, supprimer des fichiers, utiliser `docker compose down` ou lancer plusieurs corrections simultanément.

## 1. Ouvrir le dossier de diagnostic

Sur la VM `supervision` :

```bash
date --iso-8601=seconds
cd ~/observabilite
INCIDENT_ID="incident-$(date +%Y%m%d-%H%M%S)"
install -d -m 700 "diagnostics/$INCIDENT_ID"/{captures,exports,journaux}
printf '%s\n' "$INCIDENT_ID"
```

Utiliser cette chronologie dans `chronologie.md` :

| Heure et fuseau | Source | Fait observé | Hypothèse | Vérification | Résultat | Décision |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

Noter l’heure avant chaque recherche ou action. Distinguer ce qui est observé, supposé et vérifié.

## 2. Relever le signal initial

Dans Prometheus **Alerts** ou Alertmanager, relever :

| Information | Valeur |
| --- | --- |
| Nom de l’alerte | |
| État | `pending`, `firing` ou autre |
| Heure et fuseau | |
| Scénario ou service | |
| Criticité | |
| Résumé | |
| Valeur ou seuil | |
| Action suggérée | |

L’alerte indique un symptôme. Elle ne prouve pas encore la cause.

## 3. Vérifier que la supervision fonctionne

Depuis `~/observabilite` :

```bash
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  -f compose.inject19.yml \
  -f compose.simulateur.yml \
  ps
```

```bash
curl --fail http://127.0.0.1:9090/-/ready
curl --fail http://127.0.0.1:9093/-/ready
```

Dans Prometheus, vérifier les collectes :

```promql
up
```

```promql
up == 0
```

Une série absente ne vaut pas zéro. Vérifier **Status > Targets**, l’heure du dernier scrape et le message d’erreur éventuel.

## 4. Examiner toutes les alertes actives

Depuis le terminal :

```bash
curl --silent 'http://127.0.0.1:9090/api/v1/alerts' |
  python3 -m json.tool
```

Dans Prometheus, utiliser également **Alerts** pour consulter l’expression, les labels et la durée d’activation.

Rechercher si plusieurs alertes décrivent le même incident ou si l’une d’elles concerne seulement une perte de collecte.

## 5. Explorer les métriques utiles

Commencer par les métriques générales :

```promql
up{job=~"linux|windows|lab_.*"}
```

```promql
probe_success{job=~"sonde_.*"}
```

Puis choisir les requêtes liées au signal reçu.

### Service DNS

```promql
lab_dns_query_success
```

```promql
lab_dns_query_duration_seconds
```

### Réseau

```promql
lab_network_receive_errors_rate
```

```promql
lab_network_latency_seconds
```

### DHCP

```promql
lab_dhcp_available_leases
```

```promql
lab_dhcp_request_success
```

### Certificat TLS

```promql
(lab_tls_certificate_expiry_timestamp_seconds - time()) / 86400
```

Le résultat représente le nombre de jours avant l’expiration annoncée.

### Sauvegarde

```promql
lab_backup_last_run_success
```

```promql
lab_backup_actual_bytes / lab_backup_expected_bytes * 100
```

### Authentification

```promql
lab_auth_backend_up
```

```promql
lab_auth_failures_per_minute
```

### Stockage

```promql
lab_storage_operation_duration_seconds
```

Comparer avec CPU et mémoire de la cible afin de vérifier si la lenteur est générale ou limitée à l’opération observée.

### Activité de sécurité

```promql
lab_security_auth_failures_2m
```

### Redémarrages du conteneur

```promql
lab_container_start_time_seconds
```

```promql
changes(lab_container_start_time_seconds[90s])
```

Retrouver le conteneur et son compteur Docker :

```bash
CID=$(sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  ps -q lab-crashloop)

sudo docker inspect --format '{{.RestartCount}}' "$CID"
```

### Application et service dépendant

```promql
lab_dependency_request_success
```

```promql
lab_dependency_request_duration_seconds
```

```promql
probe_success{job=~"sonde_inject19_.*"}
```

Comparer la disponibilité de l’application principale, de sa fonctionnalité et de sa dépendance.

## 6. Tester les services sans les modifier

### Simulateur

```bash
curl --fail http://127.0.0.1:18083/health
curl --fail http://127.0.0.1:18083/metrics
```

### Conteneur applicatif de test

```bash
curl --fail http://127.0.0.1:18082/health
curl --fail http://127.0.0.1:18082/metrics
```

### Application et dépendance

```bash
curl --fail http://127.0.0.1:18080/health
curl -i http://127.0.0.1:18080/feature
curl -i http://127.0.0.1:18081/health
```

Interprétation possible :

| Application | Fonctionnalité | Dépendance | Conclusion limitée |
| --- | --- | --- | --- |
| 200 | 200 | 200 | Chemin fonctionnel disponible au moment du test |
| 200 | 503 | échec | Application principale disponible, dépendance ou chemin vers elle en défaut |
| échec | — | 200 | Défaut de l’application principale ou de son chemin d’accès |
| échec | — | échec | Panne plus large ou plusieurs composants indisponibles |

## 7. Consulter les journaux Docker

### Simulateur

```bash
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  -f compose.inject19.yml \
  -f compose.simulateur.yml \
  logs --since=15m lab-simulator
```

### Conteneur qui redémarre

```bash
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  logs --since=15m lab-crashloop
```

### Application et dépendance

```bash
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject19.yml \
  logs --since=15m lab-app lab-dependency
```

### Parcours de l’alerte

```bash
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  -f compose.inject19.yml \
  -f compose.simulateur.yml \
  logs --since=15m prometheus alertmanager alert-receiver
```

Chercher l’ordre suivant : événement technique, métrique anormale, état `pending`, état `firing`, notification. Un événement proche dans le temps constitue une piste ; il ne prouve pas automatiquement la causalité.

## 8. Consulter Kibana

Dans **Kibana > Discover**, sélectionner `Journaux AlpesNet`, choisir la même plage absolue que dans Grafana et rechercher les événements Linux ou Windows :

```kql
fields.lab_source: "linux" or fields.lab_source: "windows"
```

Filtrer ensuite sur l’hôte ou le fournisseur pertinent. Les journaux Docker du mini-lab sont consultables avec `docker compose logs` ; leur absence dans Kibana ne signifie pas qu’aucun événement n’existe.

## 9. Formuler les hypothèses

Écrire au moins trois hypothèses avant de corriger :

| Hypothèse | Donnée qui la confirmerait | Donnée qui la contredirait | Vérification | Résultat |
| --- | --- | --- | --- | --- |
| H1 | | | | |
| H2 | | | | |
| H3 | | | | |

Quelques familles d’hypothèses :

- service local indisponible ;
- dépendance distante indisponible ;
- ressource épuisée ou lente ;
- configuration arrivée à une limite ;
- événement inhabituel ou erreur applicative ;
- supervision ou collecte elle-même en défaut.

## 10. Proposer l’action corrective

Avant l’action, annoncer :

1. la cause probable ;
2. les preuves qui la soutiennent ;
3. l’action minimale proposée ;
4. le risque et le retour arrière ;
5. les vérifications prévues après l’action.

Dans un scénario simulé, l’injecteur peut appliquer le rétablissement caché après validation de la proposition. Ne pas chercher ni modifier les fichiers réservés de l’injecteur.

Pour une dépendance réellement arrêtée, une action ciblée peut être proposée puis exécutée :

```bash
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject19.yml \
  start lab-dependency
```

Une action n’est pas justifiée uniquement parce qu’elle est disponible. Elle doit correspondre aux preuves recueillies.

## 11. Vérifier le retour à la normale

Après l’action ou le rétablissement par l’injecteur :

1. refaire exactement les requêtes anormales ;
2. refaire le test fonctionnel ;
3. vérifier la stabilité de la collecte ;
4. rechercher l’événement de retour dans les journaux ;
5. vérifier l’alerte `Inactive` ;
6. vérifier la notification `resolved` ;
7. observer une durée supérieure au délai `for` de la règle.

```bash
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  -f compose.inject19.yml \
  -f compose.simulateur.yml \
  logs --since=10m alert-receiver
```

La disparition de l’alerte ne suffit pas si la série a disparu ou si le service ne répond toujours pas.

## 12. Compte rendu attendu

Le rapport final doit indiquer :

- le signal de départ et son heure ;
- le service et l’impact observés ;
- les métriques, sondes et journaux consultés ;
- les hypothèses confirmées ou écartées ;
- la chronologie ;
- la cause probable et le niveau de confiance ;
- l’action réalisée ou proposée ;
- les preuves du retour nominal ;
- les limites et informations manquantes.

[Prendre en charge l’incident](prendre-en-charge-incident.md) · [Préparer la mise en situation](preparer-mise-en-situation.md) · [Retour au sommaire](index.md)
