# Pense-bête — Itération 2 : alerter et diagnostiquer les incidents

## Périmètre et avancement

Réutiliser la plateforme et les dashboards de l’itération 1. Les cinq règles sont chargées. Le test CPU est documenté jusqu’au retour nominal. Le cycle IIS est attesté avec événement Kibana, `firing` et `resolved` reçus par le webhook, puis retour au nominal. Les autres règles et variations temporaires restent à tester.

- [Mise en situation](../../../supervision-optimisation-performances/it-2/alerter-diagnostiquer-incidents.md)
- [Situations à alerter, tableau et requêtes](../../../supervision-optimisation-performances/it-2/identifier-situations-alerte.md)
- [Pense-bête de l’itération 1](it-1.md)

## Termes à retenir

| Terme | Sens pour l’exploitation |
| --- | --- |
| Information | Fait à conserver ou consulter |
| Anomalie | Écart à un comportement attendu |
| Incident | Interruption ou dégradation du service |
| Alerte | Signal issu d’une condition à traiter ; ce n’est pas une preuve automatique d’incident |
| Criticité | Niveau déterminé par l’impact et l’urgence |
| Durée de persistance | Temps pendant lequel la condition doit rester présente avant déclenchement |
| Notification | Message adressé à un destinataire par un canal ; réception à vérifier |
| Fatigue d’alerte | Désensibilisation provoquée par trop de sollicitations inutiles |
| Procédure de réponse | Premiers contrôles, responsable, actions et retour au nominal |

## Décider et préparer

- Observer valeur, durée, comportement habituel, impact et possibilité d’action. Une valeur élevée n’est pas forcément anormale.
- `up=0` signifie échec de collecte, pas forcément VM arrêtée. Une cible absente de la configuration demande un contrôle du périmètre.
- `probe_success=0` avec `up=1` pour le job de sonde signifie échec du contrôle récupéré correctement.
- Quatre situations proposées : collecte endpoint en échec, service HTTP indisponible, stockage presque plein et CPU durablement élevé. Seuils et durées de la fiche restent à justifier et à tester.
- Dans Grafana **Explore → Prometheus → Code**, les requêtes d’examen n’installent aucune alerte. Dans Kibana, les recherches vont dans la barre **KQL** de Discover.
- Une période historique permet de préparer le diagnostic ; vérifier les données du jour avant la mise en service des alertes.
- Prévoir un responsable, une première action, une condition de résolution et le traitement des maintenances/données absentes.
- Une alerte déclenchée, une notification envoyée et une notification reçue sont trois faits distincts à prouver.

## Dossier à tenir

Tableau de décisions, quatre situations retenues, sources et requêtes, conditions/durées, criticité, destinataires à définir, procédure et preuves datées. Les configurations et les captures du test CPU sont dans la feuille « Configurer et tester les alertes » ; compléter les preuves encore manquantes.

## Cas de reprise des journaux — 16 septembre

- Filebeat : `connection refused` vers `192.168.122.80:5044` lors du test de sortie.
- Distinguer `logstash` (ancien test ponctuel, Exited 0) de `logstash-logs` (collecte permanente). Un conteneur Up ne garantit pas un pipeline opérationnel.
- Après `sudo docker compose up -d logstash-logs`, l’utilisateur retrouve les journaux. La capture de 11:48 montre 90 documents sur 15 min et des entrées Linux à 11:47 ; des catégories Windows sont également présentes.
- Reprise visible, cause racine non confirmée. Vérifier de nouveaux marqueurs des deux sources et la continuité ; ne pas confondre date de l’événement et heure d’ingestion.
- [Preuve et chronologie du diagnostic](../../../supervision-optimisation-performances/it-2/identifier-situations-alerte.md#cas-observe-le-16-septembre-refus-de-connexion-puis-reprise-des-journaux).

## Définir les seuils et la criticité

- [Feuille dédiée : tableaux, conditions PromQL et justification](../../../supervision-optimisation-performances/it-2/definir-seuils-criticite.md).
- Propositions à confirmer : collecte en échec 2 min (`warning`), HTTP en échec avec collecte valide 1 min (`critical` pendant l’exploitation), stockage > 85 % pendant 10 min (`warning`).
- `for` exige une condition persistante aux évaluations ; il ne correspond ni à la période du dashboard ni au délai complet de notification.
- Dans une règle Prometheus, une série retournée à 0 par `up == 0` active bien la condition. Ne pas ajouter `bool` aux filtres d’échec proposés.
- Criticité = impact et urgence ; le label seul ne configure pas le destinataire. Relier chaque alerte à une première action.
- Stockage : vérifier aussi les octets libres et la vitesse de croissance. Une marge de 15 % n’offre pas un délai identique sur tous les volumes.
- Retour au nominal : données présentes et condition levée. Une absence de données n’est pas une guérison.
- Arrêt nocturne et reprise : prévoir une fenêtre bornée, vérifier les composants prêts et les données récentes ; ne pas masquer les problèmes avec des temporisations de plusieurs heures.
- Conserver observations, choix, versions des seuils et preuves de tests. Les règles ne sont pas encore déployées par cette feuille.

## CPU — quatrième alerte candidate

- `CPUEleve` : moyenne CPU > 80 % pendant 2 min, calcul `rate` sur 2 min, criticité `warning` à adapter à l’impact.
- [Requêtes et procédure complète](../../../supervision-optimisation-performances/it-2/definir-seuils-criticite.md#d-cpu-durablement-eleve-test-simple-sur-debian).
- Sur l’endpoint Debian uniquement : installer `stress-ng`, puis `stress-ng --cpu "$(nproc)" --cpu-load 100 --timeout 5m --metrics-brief`. Arrêt automatique après 5 min ou Ctrl+C.
- Solliciter les vCPU de la VM pour franchir le seuil moyen ; un seul worker peut être insuffisant. Garder le laptop et la supervision disponibles.
- Fenêtre de calcul et durée de persistance s’additionnent partiellement dans le délai observé : relever les heures et laisser le calcul redescendre après l’arrêt.
- Une métrique en hausse ne prouve pas une notification reçue. Le test CPU est désormais documenté dans la feuille suivante ; la réception dans le webhook reste à attester.

## Configurer et tester les alertes

[Feuille complète, fichiers et commandes](../../../supervision-optimisation-performances/it-2/configurer-tester-alertes.md).

### Manipulations faites — preuve disponible

- Capture du 16 septembre : la condition CPU > 80 % retourne Debian à environ 92,87 %. Elle ne prouve pas la durée `for`, l’état `firing` ni une notification.
- Captures suivantes du 16 septembre : validations réussies, trois conteneurs Up, sondes Ready/OK et cinq règles Inactive avant test.
- CPU Debian : Pending à 14:07:32, charge Grafana proche de 100 %, alerte visible dans Alertmanager à 14:09:37 ; règles Inactive à 14:13:55 et Alertmanager vide à 14:14:01.
- Ces heures sont celles des captures. La vue Grafana de 14:19:43 montre le CPU Debian revenu près de zéro avec la collecte endpoint à 1. Pour IIS, `firing` et `resolved` sont reçus par le webhook ; les notifications CPU et les autres essais restent à documenter.
- Test IIS : terminal montrant HTTP 200 puis site Stopped ; Pending à 14:19:34, sonde IIS à 0 dans Grafana à 14:19:43, Firing à 14:20:29 et présence dans Alertmanager à 14:20:36. La série suivante montre le retour : Started et HTTP 200 à 14:22:04, règles Inactive à 14:22:19, sonde IIS à 1 à 14:22:22 et Alertmanager vide à 14:22:42.

### Gestes et commandes à retenir

- Règles dans `prometheus/rules/alertes.yml`, déclarées par `rule_files` ; `alerting` pointe vers `alertmanager:9093`.
- Quatre règles principales + `CollecteSondeEnEchec` pour la perte de visibilité Blackbox.
- Fusionner le fragment dans `compose.override.yaml`, conserver les services et volumes existants.
- Valider `docker compose config --quiet`, `promtool check rules`, `promtool check config`, `amtool check-config` avant démarrage ; commandes complètes dans la feuille.
- États : inactive → pending → firing ; la valeur doit persister pendant `for`.
- Canal local : Alertmanager → webhook `alert-receiver` → `sudo docker compose logs -f --since=5m alert-receiver`.
- `send_resolved: true` : rechercher les deux notifications `firing` et `resolved` ; délai de notification distinct de `for`.
- CPU : stress borné à 5 min sur Debian. IIS : `Stop-Website -Name 'AlpesNet-Sonde'`, puis toujours `Start-Website -Name 'AlpesNet-Sonde'`.
- Une sonde collectée reste `up=1` même si `probe_success=0`. Une disparition de données ne prouve pas le rétablissement.
- Garder heures, labels, criticité, action, courbe/sonde, notifications et preuve de retour nominal. Tests non réalisés ≠ validations acquises.


## Construire la procédure de réponse — L3

[Feuille dédiée : revue des alertes, cinq procédures et validation CA-06](../../../supervision-optimisation-performances/it-2/construire-procedure-reponse.md).

### Manipulations faites

- Procédures rédigées pour les cinq règles : collecte endpoint, HTTP, stockage, CPU et collecte de sonde. Leur rédaction ne prouve pas leur exécution.
- Preuves CPU et cycle IIS avec rétablissement disponibles ; notification locale `firing`/`resolved` attestée pour IIS. Aucune variation temporaire maîtrisée n’est encore documentée.

### Gestes et commandes à retenir

- Lire anomalie, cible, heure/durée, criticité, impact, responsable et première action avant d’intervenir.
- Vérifier seuil, durée, labels et annotations ; comparer un dépassement bref à une condition soutenue. Pour le CPU, raisonner sur la moyenne calculée et pas seulement sur la durée de stress.
- Procédure = vérifications → première action → correction possible → escalade → critère de retour → contrôle après intervention.
- Escalader si impact important, délai convenu menacé, périmètre ou droits dépassés ; fournir chronologie, preuves et actions tentées.
- Clôturer avec données fraîches, service utilisable, stabilité et notification resolved ; une alerte disparue ne suffit pas.
- Stockage : `df -h /`, `df -i /` sur Debian ; `Get-Volume -DriveLetter C` sur Windows. Tester le seuil sur séries synthétiques, sans remplir le disque du lab.
- Conserver la distinction entre test de logique isolé et preuve de la chaîne complète Prometheus → Alertmanager → récepteur.
- L3 rassemble configuration, justification des seuils, criticités, procédures et preuves pour la démonstration individuelle.


## Partir d’une alerte pour rechercher la situation

[Feuille d’investigation : cas IIS, tableau et hypothèses](../../../supervision-optimisation-performances/it-2/partir-alerte-rechercher-situation.md).

### Manipulations faites

- Analyse documentaire des captures du test IIS du 16 septembre : défaut HTTP, règle Pending puis Firing, réception Alertmanager et retour au nominal.
- PowerShell montre Stop-Website puis Stopped ; Kibana montre un événement HttpService à 14:18:46 ; le récepteur journalise `firing` puis `resolved`.

### Gestes et commandes à retenir

- Partir des labels et de l’expression, puis comparer les sources sur la même cible et période.
- Période du cas IIS : 16 septembre 2026, 14:15–14:25 Paris = 12:15–12:25 UTC. Ne pas confondre capture, début de panne et réception.
- Grafana Explore : `probe_success{job="sonde_windows_http"}`, `up{job="sonde_windows_http"}`, `probe_duration_seconds{job="sonde_windows_http"}` ; distinguer `up{job="windows"}` pour l’exporter.
- Kibana Discover : `fields.lab_source: "windows"`, puis filtrer l’hôte réel et les fournisseurs présents. Un arrêt de site IIS n’est pas nécessairement un arrêt de service Windows.
- Formuler au moins deux hypothèses : site arrêté, chemin réseau vers 8080 perturbé, configuration/contenu du contrôle incorrect. Définir un contrôle discriminant pour chacune.
- Absence de série, journal manquant ou historique expiré : consigner la limite, sans inventer le résultat. Un contrôle actuel ne prouve pas l’état passé.
- Conserver observation → information recherchée → source → résultat, puis conclusion avec faits et incertitudes.

## Formuler et vérifier des hypothèses

[Feuille dédiée : vérification des hypothèses du cas IIS](../../../supervision-optimisation-performances/it-2/formuler-verifier-hypotheses.md).

### Manipulations faites

- Les preuves conservées confirment l’arrêt volontaire d’`AlpesNet-Sonde` pour l’exercice : `Stop-Website`, état `Stopped`, échec de sonde, puis `Started`, HTTP 200 et sonde à 1.
- Les pistes réseau et configuration de sonde ne sont pas démontrées. L’événement HttpService renforce l’hypothèse de l’arrêt du site sans attribuer l’action à un utilisateur.

### Gestes et commandes à retenir

- Formuler une hypothèse avec une donnée attendue et une donnée capable de la contredire.
- Comparer les sources sur la même cible, la même période et le même fuseau.
- Classer le résultat : confirmé, écarté, affaibli ou indéterminé ; signaler les données manquantes.
- Symptôme du cas : sonde à 0 et alerte HTTP. Cause établie du test : arrêt volontaire du site IIS.
- Une corrélation temporelle oriente l’analyse, mais ne prouve pas un lien causal.
- L’accès à `windows_exporter` sur un autre port n’exclut pas un défaut propre au port 8080.
- Un retour de sonde après reprise, sans changement de configuration, affaiblit l’hypothèse d’une sonde mal configurée.
- Dans le rapport, conserver alerte, plage temporelle, observations, hypothèses, vérifications, conclusion et action corrective.

## Corréler métriques, sondes et journaux

[Feuille dédiée : chronologie corrélée du cas IIS](../../../supervision-optimisation-performances/it-2/correler-metriques-sondes-journaux.md).

### Manipulations faites

- Chronologie reconstituée à partir des captures Prometheus, Grafana, Alertmanager et PowerShell : arrêt, échec HTTP, Pending, Firing, reprise et retour nominal.
- Kibana conserve un événement HttpService antérieur au `pending` ; le webhook conserve `firing` à 12:20:25 UTC et `resolved` à 12:21:25 UTC, avec HTTP 200.

### Gestes et commandes à retenir

- Utiliser une plage absolue et vérifier les fuseaux avant de rapprocher les sources.
- Une heure de capture date l’image, pas nécessairement la commande visible.
- Détection : sonde Blackbox à 0 puis règle Prometheus. Compréhension : comparaison IIS/Nginx et collecte Windows. Cause du test : `Stop-Website` et site `Stopped`.
- Séquence retenue : IIS répond → arrêt → sonde à 0 → Pending → Firing → Alertmanager → reprise → HTTP 200 → sonde à 1 → Inactive.
- Kibana : commencer par `fields.lab_source: "windows"`, examiner les fournisseurs réellement présents et noter aussi une absence de résultat pertinent.
- Récepteur : chercher les états `firing` et `resolved` dans la fenêtre UTC du test.
- Ne calculer une durée précise que si les instants des événements comparés sont effectivement disponibles.

## Identifier la cause probable

[Feuille dédiée : diagnostic final du cas IIS](../../../supervision-optimisation-performances/it-2/identifier-cause-probable.md).

### Manipulations faites

- Diagnostic établi à partir de PowerShell, Prometheus, Grafana, Blackbox, Alertmanager, Kibana et du webhook.
- Cause probable retenue avec confiance élevée : arrêt volontaire du site `AlpesNet-Sonde`. Auteur et heure exacte des commandes non établis.

### Gestes et commandes à retenir

- Séparer dans le rapport : observé, supposé, vérifié, cause probable et non établi.
- Symptôme : sonde HTTP à 0. Cause technique : site IIS arrêté. Ne pas confondre les deux.
- Vérifier les hypothèses alternatives : VM arrêtée, supervision perdue, réseau 8080, sonde incorrecte, saturation.
- Niveau de confiance élevé grâce à la convergence de l’état local, l’événement HttpService, la sonde, les métriques et le retour après correction.
- Action proportionnée : rétablir uniquement le site concerné, puis vérifier HTTP local, sonde distante, règle inactive, `resolved` et stabilité.
- Une preuve technique de l’arrêt ne permet pas d’attribuer l’action à une personne sans journal d’audit.

## Vérifier le retour à la normale

[Feuille dédiée : contrôles avant/après et clôture IIS](../../../supervision-optimisation-performances/it-2/verifier-retour-normale.md).

### Manipulations faites

- Retour IIS confirmé sur la période observée : site Started, HTTP 200, sonde à 1, collectes présentes, règle Inactive, Alertmanager vide et webhook `resolved`.
- L’absence prolongée de tout nouvel événement Windows significatif n’est pas démontrée par une vue exhaustive.

### Gestes et commandes à retenir

- Une alerte disparue ne suffit pas : vérifier service, métriques, sonde, collecte, journal de résolution et stabilité.
- Comparer avant, pendant et après sur le même périmètre et avec des heures/fuseaux explicites.
- Vérifier `probe_success`, `up` de la sonde, `up` de l’endpoint et `probe_duration_seconds`.
- Une série absente n’est pas un retour nominal ; contrôler présence et fraîcheur des données.
- Rechercher après la reprise : erreurs, nouvelles suppressions d’URL, latence élevée et récidives Pending/Firing.
- Clôturer seulement avec un fonctionnement attendu rétabli et une durée d’observation adaptée à la criticité.
- Conserver la trace pour justifier l’action, transmettre le diagnostic et accélérer le traitement d’une récidive.

## Préparer la mise en situation — Diagnostic autonome

[Feuille dédiée : contrôle des prérequis et préparation des traces](../../../supervision-optimisation-performances/it-2/preparer-mise-en-situation.md).

### Manipulations faites

- Les activités précédentes ont validé les composants et le scénario IIS au 16 septembre 2026.
- La disponibilité au début de la future mise en situation reste à contrôler en direct ; la préparation décrite ici ne constitue pas encore une nouvelle preuve d’exécution.

### Gestes et commandes à retenir

- Vérifier Compose, Prometheus, Alertmanager, les cibles, les sondes et la fraîcheur des journaux avant le retrait du formateur.
- Une interface accessible ne suffit pas : contrôler la présence et l’horodatage des données utiles au diagnostic.
- Préparer un dossier par incident et noter chaque observation, hypothèse, recherche, action et résultat avec son heure et son fuseau.
- Séparer les faits observés, les hypothèses et les éléments effectivement vérifiés.
- Ne commencer la mise en situation que lorsque les outils de diagnostic nécessaires au scénario sont opérationnels.
- Conserver des traces ciblées et reproductibles sans secret ni identifiant inutile.
- Garder le classeur et ses informations `T2/T3` du côté injecteur ; le diagnostiqueur reçoit uniquement la situation professionnelle et `T1` au départ.
- Avant la passation, vérifier que l’inject choisi possède réellement une métrique, une sonde, une alerte et des journaux exploitables dans le lab.
- L’injecteur note l’action exacte, l’heure, la limite de sécurité et le retour arrière sans transmettre ces éléments au diagnostiqueur.

## Guide du testeur — Diagnostic autonome

[Feuille dédiée : commandes et pistes remises au diagnostiqueur](../../../supervision-optimisation-performances/it-2/guide-testeur-diagnostic.md).

### Manipulations faites

- Une feuille de diagnostic sans mécanisme d’injection ni réponses `T2/T3` a été préparée pour le testeur.
- La réalisation d’un nouveau diagnostic avec cette feuille reste à démontrer lors de la mise en situation.

### Gestes et commandes à retenir

- Partir de l’alerte, vérifier `up`, puis choisir les métriques liées au signal.
- Comparer service principal, fonctionnalité et dépendance avant de conclure.
- Consulter les journaux Docker des mini-services et les notifications `firing`/`resolved` du webhook.
- Écrire plusieurs hypothèses et rechercher une donnée contradictoire avant toute correction.
- Dans un scénario simulé, proposer l’action technique ; l’injecteur applique le rétablissement caché.
- Refaire les mêmes contrôles après intervention et observer une période stable supérieure au délai `for`.
