# Glossaire Supervision — Itération 1 : instrumenter et mesurer

## Sujet

Préparer l’observation du laboratoire sur laptop, géré avec virt-manager : VM Debian et Windows Server ; VM dédiée `supervision` désormais confirmée par le relevé du 14 septembre 2026.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Observabilité | Exploiter les données pour comprendre l’état et le comportement de l’infrastructure. |
| Métrique | Mesure numérique horodatée : CPU, mémoire, espace libre ou délai. |
| Journal | Événement horodaté donnant du contexte système ou applicatif. |
| Sonde | Contrôle direct dont le résultat peut alimenter une métrique. |
| Exporter | Composant exposant des métriques collectables par Prometheus. |
| Prometheus | Collecte, conservation et interrogation des métriques. |
| Grafana | Visualisation des métriques et tableaux de bord dans ce module. |
| ELK | Elasticsearch, Logstash et Kibana pour les journaux. |
| Fraîcheur | Âge de la dernière donnée : indispensable pour repérer une collecte interrompue. |
| Hôte / invité | Le laptop héberge les VM ; les ressources physiques sont partagées. |

## Gestes et commandes à retenir

Ces rappels ne constituent pas une preuve d’exécution.

| Besoin | Commande ou action |
| --- | --- |
| Inventorier | Lister machines, services et applications réellement disponibles. |
| Classer | Distinguer observation d’état, mesure de performance et recherche de cause. |
| Collecte minimale | Disponibilité, CPU, mémoire, espace disque, état des services, journaux et heure du dernier contrôle. |
| Linux : mémoire et disque | `free -h`, `df -h`, `df -i` dans Debian. |
| Linux : état et événements | `systemctl --failed`, `journalctl --since "-1 hour"` ; certains journaux nécessitent des droits supplémentaires. |
| Windows | Gestionnaire des tâches, Moniteur de performances, Services et Observateur d’événements. |
| Copier la clé publique SSH | `ssh-copy-id -i ~/.ssh/id_ed25519.pub UTILISATEUR@IP_VM` depuis le laptop ; adapter les deux valeurs. |
| Vérifier SSH | `ssh UTILISATEUR@IP_VM` ; une syntaxe corrigée ne prouve pas une connexion réussie. |

## Déploiement du socle — nouveaux repères

| Notion ou contrôle | À retenir |
| --- | --- |
| Emplacement proposé | VM `supervision`, Debian 13.7, `192.168.122.80` (adresse actuelle ; `.81` dans le relevé initial) ; Docker 29.8.0 et Compose v5.5.1 répondent. Les cinq composants restent à déployer. |
| Compose | Décrit les cinq services et leurs réseaux, configurations et volumes. |
| Accès aux interfaces | Publication sur la boucle locale de la VM et tunnel SSH depuis le laptop. |
| État des conteneurs | `sudo docker compose ps` ; « Up » ne prouve pas la circulation des données. |
| Diagnostic | `sudo docker compose logs --tail=100` ; masquer les secrets avant partage. |
| Prometheus prêt | `curl --fail http://127.0.0.1:9090/-/ready` dans la VM si le port est publié localement. |
| Auto-collecte | `up{job="prometheus"}` doit valoir `1` après collecte. |
| Source Grafana | `http://prometheus:9090` si les services partagent le réseau Docker et ces noms. |
| ELK complet | Retrouver dans Kibana un événement de test passé par Logstash puis Elasticsearch. |
| Persistance | Volumes configurés, panneau et événement conservés après redémarrage contrôlé. |
| Exploitation | Relever versions, ports, paramètres, certificats, tests et difficultés résolues. |

La procédure complète s'appuie sur les documentations officielles citées dans la fiche associée. Les exemples ne constituent pas des preuves d'installation.

### Fichiers de départ Prometheus et Grafana

- [Compose du socle métriques](../../../assets/configs/supervision-optimisation-performances/it-1/compose.yaml)
- [Configuration d’auto-collecte Prometheus](../../../assets/configs/supervision-optimisation-performances/it-1/prometheus/prometheus.yml)

Dans la VM, placer les fichiers dans `~/observabilite/compose.yaml` et `~/observabilite/prometheus/prometheus.yml`. Depuis ce répertoire : `sudo docker compose config --quiet`, puis `sudo docker compose up -d prometheus` et, à l’étape suivante, `sudo docker compose up -d grafana`. La procédure complète précise téléchargement, validation et tunnel SSH.

La VM est désormais à **8 Gio**, confirmé par l’utilisateur. Prometheus et Grafana gardent chacun un plafond de 512 Mio. Les plafonds proposés pour Elasticsearch, Kibana et Logstash sont respectivement 2 Gio, 1,5 Gio et 1,5 Gio ; total : 6 Gio.

### Elasticsearch et Kibana

- Ajouter [compose.override.yaml](../../../assets/configs/supervision-optimisation-performances/it-1/compose.override.yaml) à côté du `compose.yaml` existant.
- Vérifier `sudo docker compose config --services`, puis lancer `sudo docker compose up -d elasticsearch kibana` après téléchargement des images.
- Inscrire Kibana avec le jeton généré par Elasticsearch ; utiliser le tunnel SSH sur le port 5601.
- Distinguer accès humain `elastic` et identité technique de Kibana. Conserver certificats et configuration dans les volumes.
- Tester `GET /_cluster/health` dans Kibana, puis surveiller la mémoire. Elasticsearch est plafonné à 2 Gio et Kibana à 1,5 Gio ; le message de test Logstash est retrouvé dans Kibana.

### État des vérifications transmises

Connexion à Kibana et dashboard confirmés. Le contrôle Elasticsearch renvoie `green`, un nœud, 52 shards actifs et aucun shard non attribué. La capture de recherche du 14 septembre confirme également un document `TEST_LAB_OBSERVABILITE` après le test Logstash. Ce relevé valide le test initial ; les sections suivantes documentent désormais l’intégration des endpoints et de leurs journaux.

### Premier test Logstash

Un pipeline décrit l'entrée des événements et leur destination. Le test fabrique un seul message `TEST_LAB_OBSERVABILITE`, puis le stocke dans l'index `observabilite-test`. Son résultat est désormais illustré par la capture de recherche dans la feuille de déploiement.

- Créer l'index et une clé API dédiée dans Kibana Dev Tools selon la feuille.
- Conserver la clé au format `id:api_key` dans le `.env` local, exclu de Git.
- Créer [test.conf](../../../assets/configs/supervision-optimisation-performances/it-1/logstash/pipeline/test.conf) et ajouter le service Logstash du Compose complémentaire.
- Vérifier la configuration puis exécuter `sudo docker compose up -d logstash`.
- Retrouver le message dans Elasticsearch puis Discover. Les logs seuls ne prouvent pas son indexation.
- Le profil de test et `restart: "no"` évitent une boucle ; `Exited (0)` après envoi est normal pour ce générateur ponctuel. La capture `docker inspect` confirme Logstash 9.5.3, état `exited`, code `0`. Pour montrer le conteneur arrêté : `sudo docker compose ps -a logstash`.

### Appliquer une modification mémoire du Compose

Après modification des fichiers sur la VM : `sudo docker compose config --quiet`, puis `sudo docker compose up -d elasticsearch kibana`. Un simple `restart` ne recharge pas le Compose. Le test Logstash utilise désormais un plafond de 1,5 Gio et un tas Java de 512 Mio. Les nouvelles limites ne sont pas encore attestées comme appliquées aux conteneurs.

## Points de vigilance

Un ping réussi ne valide pas une application ; un service actif peut mal fonctionner. Surveiller aussi le laptop et la fraîcheur des données. Les fréquences du cours sont proposées, la collecte centralisée n’est pas attestée par ces feuilles.

## Docs associées

- [Classer les informations de supervision selon leur utilisation](../../../supervision-optimisation-performances/it-1/classer-informations-supervision.md)
- [Comprendre l'observabilité — mots clés et architecture](../../../supervision-optimisation-performances/it-1/comprendre-observabilite.md)
- [Identifier les éléments à observer](../../../supervision-optimisation-performances/it-1/identifier-elements-observer.md)
- [Itération 1 — Instrumenter et mesurer l'infrastructure](../../../supervision-optimisation-performances/it-1/index.md)
- [Instrumenter et mesurer l'infrastructure](../../../supervision-optimisation-performances/it-1/instrumenter-mesurer-infrastructure.md)

- [Déployer et valider la plateforme d’observabilité](../../../supervision-optimisation-performances/it-1/deployer-plateforme-observabilite.md)

Les [captures de déploiement](../../../supervision-optimisation-performances/it-1/deployer-plateforme-observabilite.md) documentent les interfaces, le contrôle HTTPS et le message de test. L’accueil Grafana ne prouve pas encore sa connexion à Prometheus.

Le premier relevé affichait 7,762 Gio pour Kibana. L’utilisateur a identifié une saisie `1536g` au lieu de `1536m`, puis corrigé et recréé le conteneur. La nouvelle capture confirme **1,239 Gio utilisés sur 1,5 Gio**. Relire les unités et vérifier les limites réellement appliquées avec `docker stats --no-stream`. Les captures des services actifs et des consommations figurent dans la section exploitation de la feuille.

## Intégration des endpoints — commandes à retenir

Les captures du 14 septembre 2026 attestent les deux cibles `UP` et les résultats des requêtes d’identité, d’OS, de RAM et de disque dans Prometheus. Windows Server est en **Core** : installation et contrôles en PowerShell administrateur.

| Besoin | Repère |
| --- | --- |
| Linux | `sudo apt install prometheus-node-exporter` ; service `prometheus-node-exporter`, port 9100. |
| Windows Core | MSI `windows_exporter` via PowerShell, service `windows_exporter`, port 9182. |
| Accès | Limiter les exporters à la supervision ; vérifier les IP actuelles, notamment celle de Debian recréée. |
| Déclaration | Jobs `linux` et `windows` dans `prometheus/prometheus.yml`, IP réelles, chemin `/metrics`, intervalle 30 s. |
| Validation | `promtool check config`, puis recréation du seul conteneur Prometheus avec son volume conservé. |
| Disponibilité | `up{job=~"linux|windows"}` : succès de collecte, pas santé complète de la machine. |
| RAM | `node_memory_MemAvailable_bytes` et `windows_memory_available_bytes`. |
| Diagnostic | État local, écoute, pare-feu, page Targets et erreurs des collecteurs. |

- [Procédure complète Linux et Windows Server Core](../../../supervision-optimisation-performances/it-1/integrer-endpoints-linux-windows.md)
- [Exemple Prometheus à adapter](../../../assets/configs/supervision-optimisation-performances/it-1/prometheus/endpoints-example.yml)

### Lire les premières mesures

- Diviser les valeurs en octets par `1024^3` pour les afficher en Gio.
- Identité : `node_uname_info` / `windows_os_hostname` ; OS : `node_os_info` / `windows_os_info`.
- Disques : `node_filesystem_avail_bytes` / `windows_logical_disk_free_bytes` ; lire les labels de montage ou de volume. Ne pas confondre le tmpfs de Debian avec un disque.
- `scrape_samples_scraped{job=~"linux|windows"}` : échantillons par collecte, pas nombre de types de métriques. Les captures montrent 1 279 pour Debian et 1 949 pour Windows.
- Une valeur ponctuelle ne valide pas la fréquence dans le temps ; Grafana et les erreurs des collecteurs restent à vérifier.

## Sondes — commandes et distinctions à retenir

[Feuille Créer et configurer les sondes](../../../supervision-optimisation-performances/it-1/creer-configurer-sondes.md). Les captures attestent les deux sondes à `probe_success=1`, HTTP 200 et leur collecte dans Prometheus. Les captures suivantes attestent les pannes provoquées et `probe_success=0` sur les deux sondes ; les captures de 15:09 attestent ensuite leur retour à `1` après restauration.

- Blackbox Exporter : modules dans `blackbox/blackbox.yml`, port interne 9115 ; Prometheus appelle `/probe` avec `module` et `target`.
- HTTP : contrôler le code **et** le contenu attendu. Le laboratoire propose Nginx et IIS sur TCP 8080, accessible depuis supervision.
- `up=1` : résultat collecté. `probe_success=1` : contrôle réussi. Un site en panne peut avoir `up=1` et `probe_success=0`.
- `probe_http_status_code` et `probe_duration_seconds` : réponse et durée du contrôle. Ajouter `debug=true` à l’appel `/probe` pour examiner un échec.
- Fréquence proposée : 30 s ; timeout Prometheus : 10 s ; timeout du module : 5 s.
- Windows Core : `Stop-Website -Name 'AlpesNet-Sonde'`, puis `Start-Website -Name 'AlpesNet-Sonde'`, depuis Windows PowerShell administrateur avec `Import-Module WebAdministration`.
- Garder Prometheus, Blackbox et les exporters actifs pendant la panne du service. Documenter **1 → 0 → 1**, les horaires et la restauration ; tester un endpoint à la fois.

### Timeout HTTP Windows — adresse source à vérifier

Supervision utilise **192.168.122.80**. La règle IIS initiale autorisait `.81` : le test local fonctionnait, mais le test distant expirait. Les captures montrent ensuite HTTP 200 depuis supervision.

- Vérifier la source avec `ip route get 192.168.122.25` sur supervision.
- Corriger la portée de la règle Windows existante avec `Get-NetFirewallRule -Name 'AlpesNet-Sonde-HTTP' | Get-NetFirewallAddressFilter | Set-NetFirewallAddressFilter -RemoteAddress 192.168.122.80`.
- Recontrôler également les restrictions des exporters et de la sonde Linux ; ne pas désactiver globalement le pare-feu.
- [Incident et captures](../../../supervision-optimisation-performances/it-1/creer-configurer-sondes.md#incident-rencontre-supervision-en-80-regle-restee-en-81).

### Pannes de sondes observées

- Debian : `health.txt` renommé, HTTP 404 local, puis `probe_success{job="sonde_linux_http"}=0` dans Prometheus.
- Windows : site `AlpesNet-Sonde` à `Stopped`, puis `probe_success{job="sonde_windows_http"}=0`.
- Les cibles restent UP : la collecte fonctionne et transporte un résultat d’échec. Lire `probe_success` pour connaître l’état du contrôle.
- Les captures successives prouvent **1 → 0 → 1** pour les deux sondes, avec de nouveaux résultats à `1` après les pannes. Le graphe peut compléter le dossier ; fréquence réelle et délai exact de détection restent à mesurer.

## Ajouter une source de logs — commandes à retenir

[Feuille complète](../../../supervision-optimisation-performances/it-1/ajouter-source-logs.md). Les captures attestent la collecte Linux et Windows, la recherche des tests dans Dev Tools et les événements dans Discover. Les captures de 16:25 et 16:26 valident les filtres KQL Linux et Windows, avec un document retrouvé pour chaque marqueur ; le test Windows porte le code 1001.

- Debian : journald → Filebeat ; Windows Core : Application/System → Winlogbeat.
- Trajet : Beats → `192.168.122.80:5044` en TLS mutuel → `logstash-logs` permanent → Elasticsearch en HTTPS → Kibana.
- Le service `logstash` historique reste le test ponctuel ; `logstash-logs` utilise le pipeline `endpoints.conf` et une nouvelle clé `LOGSTASH_LOGS_API_KEY` au format `id:api_key`.
- Index : `observabilite-linux` / `observabilite-windows`. La clé expire à 7 jours, les certificats client/serveur à 90 jours ; prévoir renouvellement et rétention.
- Contrôles : `filebeat test config`, `filebeat test output`, équivalents `winlogbeat.exe`, puis recherche de l’événement dans ELK. Une sortie connectée ne prouve pas l’indexation.
- Test Linux : `logger -t alpesnet-lab 'MARQUEUR_UNIQUE'`, puis `journalctl -t alpesnet-lab`.
- Test Windows : source Application `AlpesNet-Lab`, `Write-EventLog`, code 1001, marqueur unique ; vérifier avec `Get-WinEvent`.
- Kibana : période, `message`, `host.name`, `agent.type`, `fields.lab_source`, puis `winlog.channel` / `event.code` pour Windows. Comparer aux événements locaux.
- Ne pas effacer les registres de lecture ni exposer les clés et certificats privés dans Git ou les captures.

### Corrections rencontrées pendant la collecte des logs

- Filebeat : l’erreur « more than one namespace configured accessing output » se corrige en conservant uniquement `output.logstash`, sans le bloc Elasticsearch d’origine.
- Winlogbeat : tests administrateur réussis mais service en échec → examiner les droits de LocalSystem sur les certificats. Correction confirmée : `icacls 'C:\Program Files\Winlogbeat\certs' /grant '*S-1-5-18:RX' /T`, puis démarrage du service.
- Kibana : **Gestion de la Suite → Kibana → Vues de données** ; créer `Journaux AlpesNet` au lieu de modifier une vue gérée.
- Discover : `message:` doit être suivi d’une valeur. Utiliser le marqueur complet et une période couvrant l’événement ; une erreur KQL n’est pas un échec d’ingestion.
- Les tests documentés sont `ALPESNET_LOG_LINUX_20260914T140642Z` et `ALPESNET_LOG_WINDOWS_20260914T141352Z`.
