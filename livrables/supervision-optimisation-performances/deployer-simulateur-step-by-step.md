# Runbook réservé — Simulateur des injects 11 à 17 et 20

> **Injecteur uniquement.** Le formateur a autorisé la simulation. Ce guide révèle les déclencheurs et ne doit pas être montré au diagnostiqueur.

## 1. Ce que déploie le simulateur

Un seul conteneur `lab-simulator` expose des métriques Prometheus et produit des journaux JSON. Chaque incident est contrôlé par un fichier distinct dans `~/observabilite/injects/simulateur/state/`.

| Inject | Fichier déclencheur | Alerte |
| ---: | --- | --- |
| 11 | `11-dns.active` | `DNSRequetesEnEchec` |
| 12 | `12-reseau.active` | `ErreursInterfaceReseau` |
| 13 | `13-dhcp.active` | `PoolDHCPPresqueEpuise` |
| 14 | `14-tls.active` | `CertificatTLSProcheExpiration` |
| 15 | `15-backup.active` | `SauvegardeIncomplete` |
| 16 | `16-auth.active` | `EchecsAuthentificationMassifs` |
| 17 | `17-disque.active` | `LatenceOperationsStockage` |
| 20 | `20-securite.active` | `ActiviteAuthentificationInhabituelle` |

Créer un fichier active l’incident. Le supprimer rétablit les valeurs nominales. Aucun redémarrage du simulateur n’est nécessaire.

## 2. Copier le paquet sur `supervision`

Depuis le **laptop**, à la racine de `memo-ais` :

```bash
scp -r \
  livrables/supervision-optimisation-performances/inject-lab/simulateur \
  oliv@192.168.122.80:~/simulateur-transfert
```

Sur **`supervision`** :

```bash
cd ~/observabilite
install -d -m 755 injects/simulateur/state
cp -p ~/simulateur-transfert/simulator.py injects/simulateur/
cp -p ~/simulateur-transfert/compose.simulateur.yml ./
cp -p ~/simulateur-transfert/simulateur-rules.yml prometheus/rules/
chmod 755 injects/simulateur injects/simulateur/state
chmod 644 injects/simulateur/simulator.py
```

S’assurer qu’aucun scénario n’est actif au premier démarrage :

```bash
find injects/simulateur/state -maxdepth 1 -type f -name '*.active' -delete
```

Cette commande est limitée au dossier du simulateur et aux fichiers terminant par `.active`.

## 3. Ajouter le job Prometheus

Sauvegarder la configuration :

```bash
cd ~/observabilite
cp -p prometheus/prometheus.yml \
  "prometheus/prometheus.yml.avant-simulateur-$(date +%Y%m%d-%H%M%S)"
nano prometheus/prometheus.yml
```

Sous la liste `scrape_configs:` existante, ajouter exactement :

```yaml
  - job_name: lab_simulator
    scrape_interval: 5s
    scrape_timeout: 3s
    static_configs:
      - targets: ['lab-simulator:8083']
        labels:
          endpoint: inject-lab
```

Ne pas créer une deuxième clé `scrape_configs:`. Les deux espaces avant `- job_name` placent le job dans la liste existante.

## 4. Vérifier les fichiers avant le démarrage

Les conteneurs des injects 18 et 19 utilisent le même nom de projet Compose `observabilite`. Charger uniquement `compose.simulateur.yml` peut donc produire un avertissement `Found orphan containers`. Ce message ne signifie pas que Prometheus est invalide. Ne pas employer `--remove-orphans` : cette option supprimerait les mini-services 18 et 19. Pour les commandes globales de validation, charger les trois fragments comme ci-dessous.

Vérifier que Compose connaît le service :

```bash
cd ~/observabilite
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  -f compose.inject19.yml \
  -f compose.simulateur.yml \
  config --quiet

sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  -f compose.inject19.yml \
  -f compose.simulateur.yml \
  config --services | grep -x lab-simulator
```

Attendu :

```text
lab-simulator
```

Valider Prometheus et les huit règles :

```bash
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  -f compose.inject19.yml \
  -f compose.simulateur.yml \
  run --rm --no-deps --entrypoint promtool prometheus \
  check config /etc/prometheus/prometheus.yml

sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  -f compose.inject19.yml \
  -f compose.simulateur.yml \
  run --rm --no-deps --entrypoint promtool prometheus \
  check rules /etc/prometheus/rules/simulateur-rules.yml
```

Attendu : configuration valide et **8 rules found**.

## 5. Démarrer le simulateur

```bash
cd ~/observabilite
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.simulateur.yml \
  pull lab-simulator

sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.simulateur.yml \
  up -d lab-simulator

sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.simulateur.yml \
  up -d --force-recreate --no-deps prometheus
```

Contrôler le service :

```bash
curl --fail http://127.0.0.1:18083/health
curl --fail http://127.0.0.1:18083/metrics
```

Attendu : `LAB_SIMULATOR_OK`, puis toutes les métriques. Dans Prometheus :

```promql
up{job="lab_simulator"}
```

La valeur doit être `1`. Les huit nouvelles règles doivent être `Inactive`.

## 6. Inject 11 — DNS en échec

### État nominal

Dans Prometheus :

```promql
lab_dns_query_success{scenario="11"}
```

```promql
lab_dns_query_duration_seconds{scenario="11"}
```

Attendu : succès `1`, durée proche de `0.02` seconde.

### Déclenchement

```bash
cd ~/observabilite
date -Is
touch injects/simulateur/state/11-dns.active
chmod 644 injects/simulateur/state/11-dns.active
```

Après un scrape de cinq secondes : succès `0`, durée `3`. Après 20 secondes continues, l’alerte `DNSRequetesEnEchec` passe en `Firing`.

```bash
sudo docker compose \
  -f compose.yaml -f compose.override.yaml -f compose.simulateur.yml \
  logs --since=2m lab-simulator | grep dns_query_timeout
```

### Retour nominal

```bash
rm -f ~/observabilite/injects/simulateur/state/11-dns.active
```

Attendre au moins 30 secondes, puis confirmer succès `1`, durée nominale, alerte inactive et notification `resolved`.

## 7. Inject 12 — Instabilité réseau simulée

### État nominal

```promql
lab_network_receive_errors_rate{scenario="12"}
```

```promql
lab_network_latency_seconds{scenario="12"}
```

Attendu : erreurs `0`, latence proche de `0.01` seconde.

### Déclenchement

```bash
cd ~/observabilite
date -Is
touch injects/simulateur/state/12-reseau.active
chmod 644 injects/simulateur/state/12-reseau.active
```

Attendu : taux d’erreurs `12`, latence `1.2`, puis alerte `ErreursInterfaceReseau` en moins d’une minute.

```bash
sudo docker compose \
  -f compose.yaml -f compose.override.yaml -f compose.simulateur.yml \
  logs --since=2m lab-simulator | grep network_errors_detected
```

Cette injection ne modifie aucune interface réelle. Les preuves doivent la désigner comme simulation.

### Retour nominal

```bash
rm -f ~/observabilite/injects/simulateur/state/12-reseau.active
```

## 8. Inject 13 — Pool DHCP épuisé

### État nominal

```promql
lab_dhcp_available_leases{scenario="13"}
```

```promql
lab_dhcp_request_success{scenario="13"}
```

Attendu : 20 baux disponibles et succès `1`.

### Déclenchement

```bash
cd ~/observabilite
date -Is
touch injects/simulateur/state/13-dhcp.active
chmod 644 injects/simulateur/state/13-dhcp.active
```

Attendu : baux disponibles `0`, requêtes en succès `0`, alerte `PoolDHCPPresqueEpuise`.

```bash
sudo docker compose \
  -f compose.yaml -f compose.override.yaml -f compose.simulateur.yml \
  logs --since=2m lab-simulator | grep dhcp_pool_exhausted
```

### Retour nominal

```bash
rm -f ~/observabilite/injects/simulateur/state/13-dhcp.active
```

Confirmer le retour à 20 baux et le succès à `1`. Aucun paquet DHCP réel n’est émis.

## 9. Inject 14 — Certificat proche de l’expiration

### État nominal

Afficher le nombre de jours restants :

```promql
(lab_tls_certificate_expiry_timestamp_seconds{scenario="14"} - time()) / 86400
```

Attendu : environ 90 jours.

### Déclenchement

```bash
cd ~/observabilite
date -Is
touch injects/simulateur/state/14-tls.active
chmod 644 injects/simulateur/state/14-tls.active
```

Attendu : environ 3 jours restants, service simulateur toujours `up=1`, alerte `CertificatTLSProcheExpiration` après 10 secondes.

```bash
sudo docker compose \
  -f compose.yaml -f compose.override.yaml -f compose.simulateur.yml \
  logs --since=2m lab-simulator | grep certificate_expiry_warning
```

### Retour nominal

```bash
rm -f ~/observabilite/injects/simulateur/state/14-tls.active
```

Le nombre de jours revient près de 90. Il s’agit d’une date synthétique ; aucun certificat réel n’est remplacé.

## 10. Inject 15 — Sauvegarde incomplète

### État nominal

```promql
lab_backup_last_run_success{scenario="15"}
```

```promql
lab_backup_actual_bytes{scenario="15"} / lab_backup_expected_bytes{scenario="15"} * 100
```

Attendu : succès `1` et complétude `100 %`.

### Déclenchement

```bash
cd ~/observabilite
date -Is
touch injects/simulateur/state/15-backup.active
chmod 644 injects/simulateur/state/15-backup.active
```

Attendu : succès `0`, taille réelle 30 Mio pour 100 Mio attendus, complétude `30 %`, alerte `SauvegardeIncomplete`.

```bash
sudo docker compose \
  -f compose.yaml -f compose.override.yaml -f compose.simulateur.yml \
  logs --since=2m lab-simulator | grep backup_job_incomplete
```

### Retour nominal

```bash
rm -f ~/observabilite/injects/simulateur/state/15-backup.active
```

Confirmer le retour à `1` et `100 %`. Aucune sauvegarde réelle n’est modifiée.

## 11. Inject 16 — Échecs d’authentification

### État nominal

```promql
lab_auth_backend_up{scenario="16"}
```

```promql
lab_auth_failures_per_minute{scenario="16"}
```

Attendu : backend `1`, échecs `0`.

### Déclenchement

```bash
cd ~/observabilite
date -Is
touch injects/simulateur/state/16-auth.active
chmod 644 injects/simulateur/state/16-auth.active
```

Attendu : backend `0`, 24 échecs par minute, alerte critique `EchecsAuthentificationMassifs`.

```bash
sudo docker compose \
  -f compose.yaml -f compose.override.yaml -f compose.simulateur.yml \
  logs --since=2m lab-simulator | grep authentication_backend_unreachable
```

### Retour nominal

```bash
rm -f ~/observabilite/injects/simulateur/state/16-auth.active
```

Confirmer backend `1`, échecs `0` et `resolved`. Aucun compte réel n’est utilisé.

## 12. Inject 17 — Latence des opérations de stockage

### État nominal

Dans Prometheus :

```promql
lab_storage_operation_duration_seconds{scenario="17"}
```

Attendu : environ `0.03` seconde.

Mesurer aussi l’endpoint depuis `supervision` :

```bash
time curl --fail http://127.0.0.1:18083/storage/write
```

La réponse doit arriver presque immédiatement.

### Déclenchement

```bash
cd ~/observabilite
date -Is
touch injects/simulateur/state/17-disque.active
chmod 644 injects/simulateur/state/17-disque.active
```

Mesurer de nouveau :

```bash
time curl --fail http://127.0.0.1:18083/storage/write
```

La réponse attend environ trois secondes. La métrique vaut `3.2` et l’alerte `LatenceOperationsStockage` se déclenche après 20 secondes.

```bash
sudo docker compose \
  -f compose.yaml -f compose.override.yaml -f compose.simulateur.yml \
  logs --since=2m lab-simulator | grep -E 'storage_operation_slow|storage_write_completed'
```

Cette méthode utilise bien une attente applicative. Elle ne démontre pas une latence physique du disque ; le signal et le rapport doivent parler de latence simulée des opérations de stockage.

### Retour nominal

```bash
rm -f ~/observabilite/injects/simulateur/state/17-disque.active
```

Refaire `time curl` et confirmer une réponse rapide, une métrique proche de `0.03` et l’alerte résolue.

## 13. Inject 20 — Activité inhabituelle

### État nominal

```promql
lab_security_auth_failures_2m{scenario="20"}
```

Attendu : `0`.

### Déclenchement

```bash
cd ~/observabilite
date -Is
touch injects/simulateur/state/20-securite.active
chmod 644 injects/simulateur/state/20-securite.active
```

Attendu : 12 événements sur deux minutes et alerte `ActiviteAuthentificationInhabituelle`. Le service reste disponible.

```bash
sudo docker compose \
  -f compose.yaml -f compose.override.yaml -f compose.simulateur.yml \
  logs --since=2m lab-simulator | grep security_auth_failure_burst
```

### Retour nominal

```bash
rm -f ~/observabilite/injects/simulateur/state/20-securite.active
```

La valeur revient à `0`. Conserver l’événement de l’incident : le retour à la normale ne consiste pas à effacer les preuves.

## 14. Contrôles communs pendant un inject

Voir toutes les métriques simulées :

```promql
{job="lab_simulator"}
```

Voir uniquement les alertes actives du simulateur via l’API :

```bash
curl --silent 'http://127.0.0.1:9090/api/v1/alerts' | python3 -m json.tool
```

Suivre le webhook :

```bash
cd ~/observabilite
sudo docker compose logs -f --since=5m alert-receiver
```

Quitter avec `Ctrl+C` ne coupe pas le conteneur.

## 15. Réinitialisation générale

À utiliser entre deux passages ou à la fin de l’exercice :

```bash
cd ~/observabilite
find injects/simulateur/state -maxdepth 1 -type f -name '*.active' -delete
curl --fail http://127.0.0.1:18083/metrics >/dev/null
```

Attendre au moins 30 secondes, puis vérifier dans Prometheus que les huit alertes sont `Inactive`. Cette remise à zéro ne touche ni aux injects 18 et 19, ni aux composants de supervision.

Pour arrêter le simulateur :

```bash
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.simulateur.yml \
  stop lab-simulator
```
