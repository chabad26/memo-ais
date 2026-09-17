# Runbook réservé — Déployer les injects 11 à 20

> **Injecteur uniquement.** Ce document révèle les mécanismes de panne et les retours arrière. Ne pas l’ouvrir devant le diagnostiqueur.

> **Cadre validé par le formateur le 17 septembre 2026 :** les incidents peuvent être simulés. Une simulation doit néanmoins produire des données cohérentes et être identifiée comme telle dans le dossier de préparation réservé à l’injecteur.

Les procédures entièrement détaillées sont séparées pour faciliter l’exécution :

- [simulateur commun des injects 11 à 17 et 20](deployer-simulateur-step-by-step.md) ;
- cette feuille conserve les injects conteneur 18 et dépendance 19, ainsi que les principes généraux.

## Principe retenu

Les injects sont construits dans un mini-lab séparé des services de supervision. Chaque scénario doit produire quatre traces cohérentes : un signal Prometheus, une observation dans Grafana, un résultat de sonde lorsque c’est pertinent et un événement dans les journaux.

Trois niveaux de réalisme sont distingués :

- **réel et isolé** : le composant de test subit réellement la panne ;
- **émulé** : un service de laboratoire reproduit le comportement d’un service métier ;
- **simulé** : une métrique ou une temporisation est créée pour l’exercice, sans prétendre reproduire le matériel.

L’autorisation du formateur permet de retenir en priorité le troisième niveau pour DNS, DHCP, sauvegarde, authentification, disque, activité de sécurité et instabilité réseau. Cela réduit les risques sans changer le travail demandé au diagnostiqueur : il devra toujours corréler le signal, les métriques, les sondes et les journaux.

## Étape 0 — Conserver l’état actuel

Sur `supervision` :

```bash
cd ~/observabilite
date -Is
sudo docker compose config --quiet
sudo docker compose ps

INJECT_BACKUP="$HOME/inject-backups/$(date +%Y%m%d-%H%M%S)"
install -d -m 700 "$INJECT_BACKUP"
cp -a compose.yaml compose.override.yaml prometheus blackbox alertmanager "$INJECT_BACKUP/"
printf 'Sauvegarde : %s\n' "$INJECT_BACKUP"
```

Vérifier que la copie contient les fichiers attendus. Cette sauvegarde ne remplace pas les volumes Docker ; elle protège seulement les configurations qui seront modifiées.

Créer l’arborescence réservée :

```bash
cd ~/observabilite
install -d -m 700 injects/{11-dns,12-reseau,13-dhcp,14-tls,15-backup,16-auth,17-disque,18-conteneur,19-dependance,20-securite}
install -d -m 700 injects/preuves
```

## Étape 1 — Fixer les règles communes

Avant chaque scénario :

1. ne lancer qu’un seul inject à la fois ;
2. relever `date -Is` et l’état nominal ;
3. conserver une cible témoin non perturbée ;
4. écrire la commande de retour arrière avant l’injection ;
5. définir une durée maximale ;
6. vérifier la règle Prometheus avec `promtool` ;
7. attendre l’état `firing` avant la passation ;
8. après le diagnostic, confirmer `resolved` et la stabilité.

Utiliser des labels communs sur toutes les nouvelles métriques :

```text
lab="alpesnet"
scenario="11" à "20"
service="nom-du-service"
endpoint="inject-lab"
```

Les règles d’exercice peuvent utiliser `for: 1m` pour rester démontrables. Ce délai est un choix de laboratoire et doit être réévalué avant une utilisation réelle.

## Étape 2 — Ajouter les fichiers sans remplacer l’existant

Créer des fragments distincts :

```bash
cd ~/observabilite
nano compose.injects.yaml
nano prometheus/injects-jobs.yml
nano prometheus/rules/injects.yml
nano blackbox/blackbox.yml
```

Ne pas remplacer les jobs, modules ou règles existants. Fusionner les nouveaux blocs dans les clés déjà présentes de `prometheus/prometheus.yml` et `blackbox/blackbox.yml`.

Après chaque modification :

```bash
sudo docker compose -f compose.yaml -f compose.override.yaml -f compose.injects.yaml config --quiet
sudo docker compose run --rm --no-deps --entrypoint promtool prometheus \
  check config /etc/prometheus/prometheus.yml
sudo docker compose run --rm --no-deps --entrypoint promtool prometheus \
  check rules /etc/prometheus/rules/injects.yml
```

## Inject 19 — Service dépendant indisponible

Commencer par celui-ci, car son application servira ensuite aux injects 16 et 20.

Le paquet prêt à copier se trouve dans `livrables/supervision-optimisation-performances/inject-lab/19-dependance/` du dépôt documentaire.

### 19.1 Comprendre les trois fichiers Prometheus/Blackbox

| Élément | Fichier sur `supervision` | Rôle |
| --- | --- | --- |
| Règle d’alerte | `~/observabilite/prometheus/rules/injects.yml` | Dit à Prometheus quand passer de `inactive` à `pending`, puis `firing` |
| Job de collecte | `~/observabilite/prometheus/prometheus.yml` | Dit où lire `/metrics` et quelles sondes exécuter |
| Module de sonde | `~/observabilite/blackbox/blackbox.yml` | Dit à Blackbox comment tester une URL HTTP |

La règle ne va pas dans Alertmanager. **Prometheus déclenche l’alerte** ; Alertmanager la reçoit ensuite et la transmet au webhook déjà configuré.

### 19.2 Copier le paquet vers la VM de supervision

Depuis le **laptop**, à la racine du dépôt `memo-ais` :

```bash
scp -r \
  livrables/supervision-optimisation-performances/inject-lab/19-dependance \
  oliv@192.168.122.80:~/inject19-transfert
```

Puis, sur **`oliv@supervision`** :

```bash
cd ~/observabilite
install -d -m 700 injects/19-dependance
cp -p ~/inject19-transfert/app.py injects/19-dependance/
cp -p ~/inject19-transfert/dependency.py injects/19-dependance/
cp -p ~/inject19-transfert/compose.inject19.yml ./
cp -p ~/inject19-transfert/injects-rule.yml prometheus/rules/injects.yml
```

Les scripts doivent maintenant se trouver ici :

```text
~/observabilite/injects/19-dependance/app.py
~/observabilite/injects/19-dependance/dependency.py
```

### 19.3 Ajouter le module Blackbox

Sauvegarder le fichier actuel :

```bash
cd ~/observabilite
cp -p blackbox/blackbox.yml \
  "blackbox/blackbox.yml.avant-inject19-$(date +%Y%m%d-%H%M%S)"
nano blackbox/blackbox.yml
```

Dans ce fichier, il existe déjà une seule clé `modules:`. Ajouter le bloc suivant **sous cette clé**, au même niveau que `http_linux` et `http_windows`. Ne pas ajouter une seconde ligne `modules:`.

```yaml
  http_inject19:
    prober: http
    timeout: 4s
    http:
      method: GET
      preferred_ip_protocol: ip4
      follow_redirects: false
      valid_status_codes: [200]
```

Les deux espaces avant `http_inject19` sont nécessaires.

Si Blackbox affiche `field http_inject19 not found in type config.plain`, le bloc a été placé à la racine. Afficher les lignes avec leur indentation :

```bash
sed -n '1,40l' blackbox/blackbox.yml
```

La ligne doit commencer par deux espaces, tandis que `modules:` commence tout à gauche.

### 19.4 Ajouter les jobs dans Prometheus

Sauvegarder puis ouvrir la configuration :

```bash
cd ~/observabilite
cp -p prometheus/prometheus.yml \
  "prometheus/prometheus.yml.avant-inject19-$(date +%Y%m%d-%H%M%S)"
nano prometheus/prometheus.yml
```

Repérer la clé existante :

```yaml
scrape_configs:
```

Sous sa liste de jobs, ajouter le contenu de `prometheus-job.yml` fourni dans le paquet. Ne pas recopier son commentaire et ne pas créer une seconde clé `scrape_configs:`. Les nouveaux jobs sont :

- `lab_app_inject19` : collecte les deux métriques métier sur `lab-app:8080/metrics` ;
- `sonde_inject19_app` : vérifie que l’application principale reste disponible ;
- `sonde_inject19_dependency` : vérifie directement le backend ;
- `sonde_inject19_feature` : appelle `/feature`, ce qui teste réellement la dépendance et actualise la métrique métier.

Le troisième contrôle est indispensable : sans appel régulier à `/feature`, la dernière valeur de `lab_dependency_request_success` pourrait rester à `1` après l’arrêt du backend.

### 19.5 Comprendre où mettre l’alerte

Le fichier créé à l’étape 19.2 est :

```text
~/observabilite/prometheus/rules/injects.yml
```

Il est séparé de `alertes.yml`. Prometheus charge déjà tous les fichiers du dossier grâce à cette configuration :

```yaml
rule_files:
  - /etc/prometheus/rules/*.yml
```

La règle fournie est :

```yaml
groups:
  - name: alpesnet-injects
    interval: 15s
    rules:
      - alert: ServiceDependantIndisponible
        expr: |
          (lab_dependency_request_success{scenario="19"} == 0)
          and on(instance) (up{job="lab_app_inject19"} == 1)
        for: 1m
        labels:
          severity: warning
          team: infrastructure
          scenario: "19"
        annotations:
          summary: "Fonction dépendante indisponible"
          description: "L'application principale répond, mais son appel à lab-dependency échoue depuis 1 minute."
          action: "Comparer les sondes de l'application, de la fonctionnalité et de la dépendance, puis examiner les journaux applicatifs."
```

La deuxième partie de l’expression exige que `lab-app` soit toujours collectée. Elle évite de confondre une dépendance en panne avec une perte totale de l’application ou de sa collecte.

### 19.6 Valider les fichiers avant de démarrer

Toutes les commandes suivantes se lancent sur **`supervision`**, depuis `~/observabilite` :

```bash
cd ~/observabilite
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject19.yml \
  config --quiet
```

Valider ensuite Prometheus et la nouvelle règle. Le fragment Compose doit être fourni à `docker compose run` pour que les nouveaux services soient connus, même s’ils ne sont pas encore démarrés :

```bash
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject19.yml \
  run --rm --no-deps --entrypoint promtool prometheus \
  check config /etc/prometheus/prometheus.yml

sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject19.yml \
  run --rm --no-deps --entrypoint promtool prometheus \
  check rules /etc/prometheus/rules/injects.yml
```

Attendu : `SUCCESS` pour la configuration et **1 rule found** pour `injects.yml`.

### 19.7 Démarrer l’application et recharger les collecteurs

```bash
cd ~/observabilite
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject19.yml \
  pull lab-app lab-dependency

sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject19.yml \
  up -d lab-app lab-dependency
```

Blackbox doit être recréé pour relire son fichier, puis Prometheus pour relire les jobs et la règle :

```bash
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject19.yml \
  up -d --force-recreate --no-deps blackbox prometheus
```

Vérifier l’état :

```bash
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject19.yml \
  ps lab-app lab-dependency blackbox prometheus

sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject19.yml \
  logs --tail=50 lab-app lab-dependency blackbox prometheus
```

### 19.8 Valider l’état nominal

Les ports 18080 et 18081 sont publiés uniquement sur la boucle locale de `supervision` :

```bash
curl --fail http://127.0.0.1:18080/health
curl --fail http://127.0.0.1:18080/feature
curl --fail http://127.0.0.1:18081/health
curl --fail http://127.0.0.1:18080/metrics
```

Attendu :

```text
LAB_APP_OK
FEATURE_OK
DEPENDENCY_OK
lab_dependency_request_success{scenario="19",service="lab-dependency"} 1
```

Dans Prometheus, exécuter successivement :

```promql
up{job="lab_app_inject19"}
```

```promql
probe_success{job=~"sonde_inject19_.*"}
```

```promql
lab_dependency_request_success{scenario="19"}
```

Tous les résultats doivent valoir `1`. Dans **Status > Targets**, les quatre nouveaux jobs doivent être `UP`. Dans **Alerts**, `ServiceDependantIndisponible` doit être `Inactive`.

### 19.9 Provoquer l’inject

Arrêter uniquement le backend :

```bash
cd ~/observabilite
date -Is
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject19.yml \
  stop lab-dependency
```

Contrôler immédiatement :

```bash
curl --fail http://127.0.0.1:18080/health
curl -i http://127.0.0.1:18080/feature
```

Résultat attendu : `/health` retourne toujours HTTP 200, tandis que `/feature` retourne HTTP 503. Après les prochains scrapes :

- `sonde_inject19_app` reste à `1` ;
- `sonde_inject19_dependency` passe à `0` ;
- `sonde_inject19_feature` passe à `0` ;
- `lab_dependency_request_success` passe à `0` ;
- la règle devient `Pending`, puis `Firing` après une minute continue.

Observer le journal JSON :

```bash
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject19.yml \
  logs --since=5m lab-app
```

Le message `dependency_call_failed` doit apparaître. C’est à ce moment que le diagnostiqueur peut recevoir `T1`.

### 19.10 Restaurer le service

Le diagnostiqueur devrait proposer ou exécuter le redémarrage ciblé de la dépendance :

```bash
cd ~/observabilite
date -Is
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject19.yml \
  start lab-dependency
```

Vérifier ensuite :

```bash
curl --fail http://127.0.0.1:18081/health
curl --fail http://127.0.0.1:18080/feature
```

Attendre plusieurs cycles de 15 secondes et confirmer : sondes à `1`, métrique métier à `1`, règle `Inactive`, disparition du groupe dans Alertmanager et notification `resolved` dans `alert-receiver`.

### 19.11 Arrêter entièrement le mini-lab après l’exercice

```bash
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject19.yml \
  stop lab-app lab-dependency
```

Ne pas utiliser `down`, car cette commande appliquée à l’ensemble du projet Compose pourrait aussi arrêter les composants d’observabilité.

## Inject 18 — Redémarrages d’un conteneur

Cet inject utilise un conteneur jetable sur la VM `supervision`. Le fichier `active` ordonne au processus de quitter avec le code `1` après 20 secondes. La politique `restart: unless-stopped` le relance, ce qui crée une vraie boucle de redémarrage limitée à ce service de test.

Le paquet se trouve dans `livrables/supervision-optimisation-performances/inject-lab/18-conteneur/`.

### 18.1 Revenir à l’état neutre

Tu as peut-être déjà créé le déclencheur. Sur **`supervision`**, commence par le supprimer :

```bash
cd ~/observabilite
rm -f injects/18-conteneur/active
```

Cette commande ne supprime aucun conteneur. Elle garantit seulement que le premier démarrage sera nominal.

### 18.2 Copier le paquet depuis le laptop

Depuis le **laptop**, à la racine de `memo-ais` :

```bash
scp -r \
  livrables/supervision-optimisation-performances/inject-lab/18-conteneur \
  oliv@192.168.122.80:~/inject18-transfert
```

Sur **`supervision`** :

```bash
cd ~/observabilite
install -d -m 700 injects/18-conteneur
cp -p ~/inject18-transfert/crashloop.py injects/18-conteneur/
cp -p ~/inject18-transfert/compose.inject18.yml ./
cp -p ~/inject18-transfert/inject18-rule.yml prometheus/rules/
rm -f injects/18-conteneur/active
chmod 755 injects/18-conteneur
chmod 644 injects/18-conteneur/crashloop.py
```

Le service n’existe pour Docker Compose qu’après la présence de `compose.inject18.yml` et l’utilisation explicite de ce fichier avec `-f`.

Le conteneur utilise l’utilisateur non privilégié `65534`. Le dossier monté sur `/state` doit donc être traversable et ses fichiers lisibles. Un dossier en mode `700` provoquerait `Permission denied` et empêcherait la détection du fichier `active`.

### 18.3 Ajouter le job Prometheus

Sauvegarder et ouvrir le fichier :

```bash
cd ~/observabilite
cp -p prometheus/prometheus.yml \
  "prometheus/prometheus.yml.avant-inject18-$(date +%Y%m%d-%H%M%S)"
nano prometheus/prometheus.yml
```

Sous la liste `scrape_configs:` existante, ajouter :

```yaml
  - job_name: lab_crashloop_inject18
    scrape_interval: 5s
    scrape_timeout: 3s
    static_configs:
      - targets: ['lab-crashloop:8082']
        labels:
          endpoint: inject-lab
          scenario: "18"
```

Ne pas créer une deuxième clé `scrape_configs:`.

### 18.4 Vérifier que Compose connaît le service

```bash
cd ~/observabilite
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  config --quiet

sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  config --services | grep -x lab-crashloop
```

La dernière commande doit afficher :

```text
lab-crashloop
```

Si elle n’affiche rien, vérifier le nom et l’emplacement de `compose.inject18.yml`. Le simple dossier `injects/18-conteneur/` ne crée pas un service Compose.

### 18.5 Valider Prometheus et la règle

```bash
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  run --rm --no-deps --entrypoint promtool prometheus \
  check config /etc/prometheus/prometheus.yml

sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  run --rm --no-deps --entrypoint promtool prometheus \
  check rules /etc/prometheus/rules/inject18-rule.yml
```

Attendu : configuration valide et **1 rule found**.

### 18.6 Démarrer en état nominal

```bash
cd ~/observabilite
rm -f injects/18-conteneur/active

sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  pull lab-crashloop

sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  up -d lab-crashloop

sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  up -d --force-recreate --no-deps prometheus
```

Vérifier :

```bash
curl --fail http://127.0.0.1:18082/health
curl --fail http://127.0.0.1:18082/metrics
```

Attendu : `CRASHLOOP_APP_OK` et `lab_container_restart_simulation_active=0`.

Dans Prometheus :

```promql
up{job="lab_crashloop_inject18"}
```

```promql
lab_container_start_time_seconds{scenario="18"}
```

La collecte doit valoir `1` et l’alerte `RedemarragesConteneurRepetes` doit être `Inactive`.

Relever le compteur Docker initial :

```bash
CID=$(sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  ps -q lab-crashloop)
sudo docker inspect --format '{{.RestartCount}}' "$CID"
```

### 18.7 Déclencher la boucle de redémarrage

```bash
cd ~/observabilite
date -Is
touch injects/18-conteneur/active
chmod 644 injects/18-conteneur/active

sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  restart lab-crashloop
```

Suivre les événements pendant environ une minute :

```bash
sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  logs -f lab-crashloop
```

Utiliser `Ctrl+C` pour quitter uniquement l’affichage des journaux. Les messages attendus sont :

```text
restart_simulation_armed
simulated_application_crash
lab_crashloop_started
```

Le cycle dure environ 20 secondes. Après au moins deux redémarrages, vérifier le compteur :

```bash
CID=$(sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  ps -q lab-crashloop)
sudo docker inspect --format '{{.RestartCount}}' "$CID"
```

Dans Prometheus, la requête suivante doit devenir supérieure ou égale à `2` :

```promql
changes(lab_container_start_time_seconds{scenario="18"}[90s])
```

L’alerte passe ensuite par `Pending`, puis `Firing` après 10 secondes de persistance.

### 18.8 Arrêter l’injection

Supprimer le déclencheur. Le conteneur actuellement lancé peut encore effectuer le crash déjà programmé ; le démarrage suivant restera stable.

```bash
cd ~/observabilite
date -Is
rm -f injects/18-conteneur/active

sudo docker compose \
  -f compose.yaml \
  -f compose.override.yaml \
  -f compose.inject18.yml \
  restart lab-crashloop
```

Vérifier le retour nominal :

```bash
curl --fail http://127.0.0.1:18082/health
sleep 30
curl --fail http://127.0.0.1:18082/health
```

La valeur `changes(...)` diminuera lorsque les redémarrages sortiront de la fenêtre de 90 secondes. Confirmer ensuite l’alerte `Inactive`, la notification `resolved`, l’absence de nouveaux messages `simulated_application_crash` et la stabilité du compteur Docker.

### 18.9 Arrêter le service après l’exercice

```bash
rm -f ~/observabilite/injects/18-conteneur/active
sudo docker compose \
  -f ~/observabilite/compose.yaml \
  -f ~/observabilite/compose.override.yaml \
  -f ~/observabilite/compose.inject18.yml \
  stop lab-crashloop
```

## Inject 14 — Certificat proche de l’expiration

### Déploiement

1. Créer une CA exclusivement réservée au lab.
2. Générer un certificat nominal, puis un certificat d’injection valable quelques jours.
3. Déployer un endpoint HTTPS de test.
4. Ajouter un module Blackbox HTTPS qui collecte la date de fin du certificat.
5. Ajouter une alerte sur :

```promql
(probe_ssl_earliest_cert_expiry{job="sonde_tls_inject"} - time()) / 86400 < 7
```

6. Vérifier que la sonde collecte bien `probe_ssl_earliest_cert_expiry` avant de poursuivre.

### Injection

Remplacer uniquement le certificat du service HTTPS de test par le certificat court, puis redémarrer ce service. Le service reste disponible : l’incident est préventif.

### Retour arrière

Restaurer le certificat nominal et vérifier que le nombre de jours restants repasse au-dessus du seuil. Ne jamais utiliser les certificats Elasticsearch, Beats ou Logstash pour cet inject.

## Inject 15 — Sauvegarde incomplète

### Déploiement

1. Créer quelques fichiers fictifs dans `injects/15-backup/source/`.
2. Écrire un script qui produit une archive, un manifeste, un journal et un fichier de métriques Prometheus.
3. Exposer au minimum :

```text
lab_backup_last_run_success{scenario="15"} 1
lab_backup_last_success_timestamp_seconds{scenario="15"} 0
lab_backup_expected_bytes{scenario="15"} 0
lab_backup_actual_bytes{scenario="15"} 0
```

4. Faire collecter ce fichier par le Textfile Collector de `node_exporter`, ou déployer un petit exporteur dédié.
5. Alerter lorsque le dernier job vaut `0` ou lorsque la taille réelle est inférieure à la taille attendue.

### Injection

Le script doit accepter un mode `--fail-before-finalize`. Ce mode copie seulement une partie des fichiers, écrit une erreur et conserve le dernier jeu valide.

### Retour arrière

Relancer le job sans option d’échec, vérifier le manifeste, la taille, le statut `1` et l’absence de nouvelle erreur. Ne jamais provoquer l’exercice avec une sauvegarde réelle.

## Inject 17 — Latence disque

### Variante A — Attente applicative, recommandée pour un exercice sûr

Un `sleep` ou un `wait` simule la lenteur d’une opération de stockage vue par l’application. Il ne produit pas une vraie saturation disque.

1. Faire lire ou écrire un fichier de test par `lab-app`.
2. Ajouter une valeur `delay_ms` dans un fichier réservé.
3. Dans le chemin d’E/S, attendre après l’ouverture du fichier et mesurer toute l’opération.
4. Exposer un histogramme ou une jauge :

```text
lab_storage_operation_duration_seconds{scenario="17",operation="write"}
```

5. Alerter si cette durée dépasse, par exemple, 2 secondes pendant 1 minute.
6. Dans `T1`, parler de **latence des opérations de stockage de l’application**, pas de défaillance physique du disque.

Pseudo-code :

```python
start = time.monotonic()
with open(TEST_FILE, "ab") as stream:
    stream.write(payload)
    stream.flush()
time.sleep(delay_ms / 1000)
duration = time.monotonic() - start
```

L’attente doit être incluse dans la durée mesurée. La supprimer ramène immédiatement le service au nominal.

### Variante B — Latence réelle du périphérique

1. Ajouter un disque virtuel uniquement destiné au test.
2. Le monter dans un chemin dédié et relever son nom de périphérique.
3. Installer `fio` sur la VM qui porte ce disque.
4. Exécuter une charge bornée en temps, taille et débit.
5. Observer les métriques `node_disk_*` du seul périphérique de test.

Ne jamais exécuter `fio` sur `/`, sur les volumes Elastic/Prometheus ou sans limite. Préparer une minuterie d’arrêt et conserver la console virt-manager.

### Choix pour le livrable

Utiliser la variante A si le but principal est la démarche de diagnostic. Utiliser la variante B seulement si la compétence exige de démontrer une vraie dégradation des métriques du disque. Ne pas mélanger les preuves des deux variantes.

## Inject 11 — DNS indisponible

### Déploiement

1. Déployer un serveur DNS de test, par exemple CoreDNS, sur un réseau Docker dédié.
2. Créer uniquement une zone fictive, par exemple `lab.invalid`.
3. Ajouter un module DNS dans Blackbox et une cible interrogeant un nom connu de cette zone.
4. Collecter le succès et la durée de la résolution.
5. Alerter si la résolution échoue plusieurs fois tandis que le serveur ou son port reste joignable.

### Injection

Basculer le serveur de test vers une configuration qui accepte la requête mais retarde ou échoue sur la réponse de la zone. Ne pas modifier `/etc/resolv.conf` des VM.

### Retour arrière

Restaurer la configuration nominale du serveur DNS de test, recharger uniquement ce service et vérifier plusieurs résolutions successives.

## Inject 13 — DHCP saturé

Ce scénario doit rester sur un réseau virtuel isolé.

1. Créer dans libvirt un réseau sans DHCP existant et sans route vers le réseau d’administration.
2. Ajouter une petite VM ou un conteneur privilégié dédié au serveur DHCP de test.
3. Définir un pool volontairement petit.
4. Ajouter des clients jetables capables de demander puis libérer leurs baux.
5. Exporter le nombre total, utilisé et disponible de baux.
6. Centraliser les journaux DHCP.
7. Alerter sur les baux disponibles proches de zéro et sur les refus de requête.

Ne jamais lancer un second DHCP sur le bridge libvirt qui porte les VM actuelles. Si l’isolement ne peut pas être garanti, remplacer ce scénario par une **simulation de gestion de pool** clairement nommée et ne pas émettre de trames DHCP.

Le retour arrière libère les baux de test, restaure le pool nominal et vérifie qu’un nouveau client obtient une adresse.

## Inject 16 — Échecs d’authentification

Réutiliser `lab-app` et ajouter une dépendance d’authentification `lab-auth`.

1. Créer uniquement des comptes fictifs.
2. Exposer le nombre d’authentifications réussies et échouées.
3. Journaliser l’échec de communication avec `lab-auth` séparément d’un mauvais mot de passe.
4. Garder CPU et mémoire visibles comme indicateurs témoins.
5. Alerter sur un taux d’échec élevé pendant 1 minute.

L’injection recommandée consiste à arrêter `lab-auth` ou à lui faire répondre en erreur. Elle correspond mieux au `T3` du classeur qu’une rafale de mauvais mots de passe.

Le retour arrière redémarre `lab-auth`, effectue une authentification fictive valide et confirme l’arrêt des nouvelles erreurs.

## Inject 20 — Activité inhabituelle

Réutiliser la route de connexion de `lab-app`.

1. Créer un compte fictif sans droit d’administration.
2. Générer un petit nombre d’échecs depuis une seule origine du lab.
3. Utiliser un seuil bas adapté à l’exercice, par exemple cinq échecs en deux minutes.
4. Envoyer les événements structurés dans la chaîne de journaux.
5. Exposer un compteur Prometheus ou créer la détection dans l’outil de logs selon ce qui est réellement disponible.
6. Vérifier qu’aucun service fonctionnel n’est interrompu.

Ne pas viser SSH, les comptes réels, Active Directory ou les interfaces de supervision. Le retour au nominal correspond à l’arrêt des tentatives et à l’absence de nouveaux événements pendant une fenêtre définie ; il ne nécessite pas de supprimer les preuves.

## Inject 12 — Instabilité réseau

Réaliser ce scénario en dernier.

1. Cibler uniquement une interface ou un conteneur de test.
2. Garder la console virt-manager ouverte.
3. Préparer la commande de suppression avant l’ajout de la règle.
4. Programmer une restauration automatique indépendante de la session SSH.
5. Appliquer une perte et une latence modérées avec `tc netem`.
6. Observer la sonde, la durée et les erreurs applicatives.

Exemple à adapter à l’interface de test, jamais à copier sans vérifier son nom :

```bash
sudo tc qdisc add dev INTERFACE_TEST root netem delay 300ms 100ms loss 10%
```

Retour arrière :

```bash
sudo tc qdisc del dev INTERFACE_TEST root
```

`netem` simule pertes et latence. Il ne garantit pas l’augmentation des compteurs d’erreurs physiques. Adapter `T1` à ce qui est effectivement mesuré.

## Étape finale — Valider chaque scénario avant la passation

Pour chaque inject :

```bash
cd ~/observabilite
sudo docker compose config --quiet
curl --fail http://127.0.0.1:9090/-/ready
curl --fail http://127.0.0.1:9093/-/ready
sudo docker compose logs --since=15m prometheus alertmanager alert-receiver
```

Puis conserver :

1. l’état nominal ;
2. la commande d’injection et son heure dans le dossier injecteur ;
3. le passage métrique ou sonde du nominal vers l’anomalie ;
4. les journaux utiles ;
5. `pending`, `firing` et la notification reçue ;
6. la commande corrective ou le retour arrière ;
7. la remontée au nominal ;
8. `resolved` et une période de stabilité.

Un scénario qui ne fournit pas ces éléments reste « en construction » et ne doit pas être remis au diagnostiqueur.
