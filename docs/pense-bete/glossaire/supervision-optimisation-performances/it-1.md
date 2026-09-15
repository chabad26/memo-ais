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

## Réservations DHCP du laboratoire — appliquées

Le 14 septembre 2026, les adresses ont été réservées dans le réseau libvirt `default`, en configuration active **et persistante** : supervision `.80`, Debian `.158`, Windows `.25`. Aucun redémarrage du réseau ou des VM n’a été effectué ; le réseau est en démarrage automatique.

- Vérifier les réservations sur le laptop : `virsh -c qemu:///system net-dumpxml default --inactive`.
- Vérifier les baux : `virsh -c qemu:///system net-dhcp-leases default`.
- Les invités restent en DHCP. Conserver les MAC ; recontrôler l’association si une VM est recréée.
- Le 15 septembre 2026, l’utilisateur confirme les IP correctes à la reprise ; la persistance XML avait été vérifiée la veille. Aucun nouveau relevé de bail n’est joint.
- [Associations MAC/IP et sauvegarde](../../../supervision-optimisation-performances/it-1/identifier-elements-observer.md#adresses-stabilisees-par-reservation-dhcp).

## Simulation croisée — préparation et observation

[Feuille de simulation croisée](../../../supervision-optimisation-performances/it-1/simulation-croisee-observabilite.md). Exercice proposé, non encore réalisé.

- Vérifier l’état nominal du jour : métriques récentes, deux sondes à 1, événements récents des deux sources, dashboard lisible.
- Préparer trois événements : disponibilité, performance, journalisation. Conserver choix et horaires dans une fiche privée, hors du site et du dépôt partagé.
- Le binôme observateur connaît le périmètre, pas les actions ; noter observations et hypothèses avant de révéler le scénario.
- `up` mesure la collecte ; `probe_success` mesure le résultat du contrôle. Pour le CPU, utiliser le taux d’évolution du compteur et une unité en pourcentage.
- Prévoir durée maximale et restauration ; maintenir les collecteurs actifs. Revenir au nominal entre les essais de cette première simulation.
- Délai d’observation = première détection humaine moins heure réelle de l’action ; noter « non mesuré » si les horaires manquent.
- Après comparaison, améliorer la configuration ou la présentation et rejouer le contrôle concerné. Ne pas présenter un autotest comme un exercice à l’aveugle.

## Construire un dashboard Grafana

- [JSON prêt à importer](../../../assets/configs/supervision-optimisation-performances/it-1/grafana/alpesnet-observation-croisee.json) : 12 panneaux, actualisation 30 s, période 1 h.
- Grafana via tunnel SSH, port 3000 ; source Prometheus : `http://prometheus:9090` depuis le conteneur Grafana.
- **Dashboards → New → Import**, charger le fichier, sélectionner la source Prometheus. Import/rendu à confirmer dans l’interface.
- CPU en pourcentage moyen sur 2 minutes ; mémoire non disponible et stockage occupé en pourcentage de 0 à 100. Durée des sondes en secondes. Les sondes affichent « Sans données » quand leur collecte échoue.
- Les journaux restent dans Discover via le tunnel 5601 ; le dashboard ne contient aucun scénario confidentiel.

- [Feuille dédiée au dashboard](../../../supervision-optimisation-performances/it-1/construire-dashboard-grafana.md) : import et construction manuelle, choix des KPI, unités, périodes, actualisation et tests. La simulation croisée reste une activité séparée.

### Dashboard manuel — capture du 15 septembre

Neuf panneaux sont présents ; la construction se fait à la main, le JSON reste facultatif. Avant validation : remplacer les métriques mémoire brutes, retirer les anciennes séries du disque Windows, vérifier les valeurs CPU négatives et afficher les états séparément sans somme/empilement. Finaliser unités, légendes, actualisation 30 s et enregistrement. Ne pas ajouter de panneaux uniquement pour augmenter leur nombre.


## Construire un dashboard Kibana

- [Feuille de construction manuelle](../../../supervision-optimisation-performances/it-1/construire-dashboard-kibana.md) : cinq panneaux illustrés sur 24 h ; classement étendu à Linux, collecte actuelle à valider.
- Accès via tunnel : `http://127.0.0.1:5601` ; supervision `192.168.122.80`.
- Vue **Journaux AlpesNet**, index `observabilite-linux,observabilite-windows`, date `@timestamp`.
- Cinq panneaux : total, évolution temporelle, sources, types d’événements et tableau Discover trié du plus récent au plus ancien.
- Compter les documents avec **Count of records** ; ne pas sommer `event.code` et ne pas confondre événements et incidents.
- `fields.lab_source` distingue Linux/Windows ; `host.name` identifie la machine. Les niveaux ne sont pas encore harmonisés : classement par types avec filtres KQL et catégorie « Autres ».
- Enregistrer la session Discover sans filtre de marqueur, puis l’ajouter depuis la bibliothèque du dashboard.
- Dernière heure, actualisation 30 s ; mêmes filtres et période pour tous les panneaux. Une actualisation ne prouve pas la fraîcheur de la collecte.
- Les anciens tests datent du 14 septembre 2026, vers 16:06 et 16:13 heure de Paris : adapter la période ou produire de nouveaux marqueurs.

### Kibana — libellés français et preuves sur 24 h

- **Indicateur** = Metric ; **Compte → Enregistrements** = Count of records ; **Camembert** pour la répartition ; **Valeurs les plus élevées** = Top values.
- Pour les types, utiliser **Vertical à barres**, axe horizontal **Filtres**, axe vertical **Compte → Enregistrements**.
- Cinq captures du 15 septembre montrent les événements du 14 : 268 documents = 229 Linux + 39 Windows, et chaque marqueur historique est retrouvé une fois.
- Le classement actuel sélectionne 40 documents : tests et événements Windows. L’utilisateur confirme que « Autres » cible Windows ; renommer cette catégorie « Autres événements Windows ».
- Ajouter « Autres événements Linux » avec `fields.lab_source: "linux" and not log.syslog.appname: "alpesnet-lab"`. Sur les mêmes données, attendre 228 événements supplémentaires, soit 268 au total. Ajout visible sur la capture de 10:25 : quatre barres, total 268, infobulle « Autres événements Windows » à 19. Relever les quatre valeurs exactes au survol pour confirmer leur somme.
- Une fenêtre de 24 h prouve la consultation de l’historique, pas la collecte actuelle : générer de nouveaux tests pour valider cette dernière.

- Après correction, certains libellés des catégories sont masqués : élargir le panneau ou raccourcir les étiquettes pour garder les quatre catégories lisibles.

## Améliorer les dashboards — Livrable L2

- [Feuille L2 et validation individuelle CA-05](../../../supervision-optimisation-performances/it-1/ameliorer-dashboards.md).
- Un panneau doit répondre à une question d’exploitation : identifier sa source, son calcul, son unité, son périmètre et ses limites.
- Corriger les données et calculs avant les titres et couleurs ; retirer les doublons, expliciter les endpoints, distinguer absence de données et succès.
- Grafana : reprendre les ajustements des neuf panneaux ; leur validation finale reste à confirmer.
- Kibana : quatre catégories présentes ; rendre tous les libellés lisibles, relever les décomptes et distinguer consultation sur 24 h et collecte actuelle.
- Comparer avant/après sur la même période et avec les mêmes filtres ; vérifier les deux endpoints et l’accès aux données source.
- L2 : deux dashboards enregistrés et accessibles, dossier de configuration, preuves datées et amélioration justifiée. Présentation individuelle avec au moins deux choix de visualisation expliqués.
- Compléter l’auto-évaluation avant de demander la validation ; la préparation du dossier ne vaut pas validation du formateur.

- [Corrections Grafana à saisir](../../../supervision-optimisation-performances/it-1/ameliorer-dashboards.md#mode-demploi-ou-coller-les-requetes) : neuf requêtes PromQL, titres, légendes, unités et réglages par panneau. Coller dans **Queries → Code**, remplacer les anciennes requêtes du panneau.
- [Corrections Kibana à saisir](../../../supervision-optimisation-performances/it-1/ameliorer-dashboards.md#mode-demploi-champs-a-modifier-dans-kibana) : champs en français, quatre filtres KQL, titres et recherches de contrôle. Distinguer **Formule** (`count()`), filtres de catégories et barre KQL globale.

### L2 — captures après changements

- Grafana, capture de 11:11 : deux états distincts pour la collecte et deux pour les sondes ; mémoire affichée autour de 16–18. Calculs à confirmer, unités et légendes à finaliser ; le disque Windows contient encore les tailles de volumes.
- Kibana, capture de 11:19 : quatre catégories lisibles, tableau à cinq colonnes trié par date décroissante, 268 documents sur 24 h. Titres et hauteur du compteur à finaliser.
- Les écrans restent en édition ; la fraîcheur de la collecte, l’enregistrement final et la réouverture ne sont pas prouvés par ces captures.
- [Captures et bilan des améliorations](../../../supervision-optimisation-performances/it-1/ameliorer-dashboards.md#captures-des-ameliorations-15-septembre-2026).

### Grafana — emplacement exact du nom de légende

- **Sous le graphique : Queries → requête A → Options → Legend → Auto → Custom**, puis saisir par exemple `Windows Core — {{volume}}` et cliquer sur **Run queries**.
- Le menu **Legend** à droite (Visibility, List/Table, Bottom/Right, Values) règle la présentation ; il ne contient pas ce champ Custom.
- [Repères détaillés dans L2](../../../supervision-optimisation-performances/it-1/ameliorer-dashboards.md#trouver-le-champ-de-legende-sous-le-graphique).

### L2 — dernières captures de 11:36 et 11:43

- Grafana : titres explicites, états nommés, disque C: seul autour de 30, légendes des services et unités temporelles visibles. Finaliser les unités % et bornes 0–100 des ressources, ainsi que les textes des états si retenus.
- Kibana : titres des répartitions, couleurs Linux/Windows distinctes et compteur 268 entièrement visible. Ajouter le titre de l’histogramme, redonner de la largeur au tableau et retirer l’arrière-plan du compteur s’il n’aide pas la lecture.
- Les deux captures restent en édition et ne valident ni l’enregistrement final ni la fraîcheur de collecte. Les anciennes remarques décrivent chaque étape datée.

### L2 — bilan visuel à 11:48

- Grafana : six graphiques de ressources avec bornes 0–100 et titres en %, états distincts et nommés, durées avec unités.
- Kibana : titre « Évolution du nombre d’événements » ajouté, tableau élargi et compteur 268 visible sur 24 h.
- Les anciens points sur les échelles, ce titre et la largeur du tableau sont levés par les nouvelles captures. Enregistrement/réouverture et validation de collecte restent à vérifier séparément.
- [Dernières preuves de présentation L2](../../../supervision-optimisation-performances/it-1/ameliorer-dashboards.md#bilan-visuel-a-1148-echelles-et-titres-harmonises).
