# Partir d’une alerte pour rechercher ce qui s’est produit

## Objectif et travail demandé

À partir d’une alerte réellement déclenchée, réunir les informations utiles pour comprendre la situation : élément concerné, nature du signal, date et heure, métriques, sondes, journaux et évolution des dashboards. Compléter le tableau d’observation, puis formuler **au moins deux hypothèses vérifiables**.

Cette feuille prolonge la [procédure de réponse](construire-procedure-reponse.md). Le cas retenu est **`ServiceHTTPIndisponible` sur Windows Core / IIS**, déclenché pendant le test du 16 septembre 2026. Les [captures du test et du retour au nominal](configurer-tester-alertes.md#captures-test-iis-realise-le-16-septembre-2026) servent de preuves ; il n’est pas nécessaire de provoquer une nouvelle panne pour commencer l’analyse.

!!! note "Ce qui est déjà connu"
    Dans cet exercice contrôlé, PowerShell montre `Stop-Website` puis le site `Stopped`. Kibana fournit aussi un événement `Microsoft-Windows-HttpService` à 14:18:46 relatif à la suppression des URL d’un groupe HTTP. Le webhook confirme ensuite `firing` et `resolved`. Ces preuves renforcent la chronologie sans attribuer à elles seules l’action à un utilisateur.

## 1. Lire l’alerte avant d’élargir la recherche

| Élément | Information observée |
| --- | --- |
| Nom | `ServiceHTTPIndisponible` |
| Élément concerné | `endpoint=windows-core`, `service=iis-lab` |
| Cible | `http://192.168.122.25:8080/health.txt` |
| Source | `job=sonde_windows_http` |
| Criticité et responsable | `severity=critical`, `team=infrastructure` |
| Condition | `probe_success=0` avec collecte de sonde `up=1`, pendant 1 min |
| État | Pending observé à 14:19:34 ; Firing observé à 14:20:29 |
| Transmission | Présence dans Alertmanager à 14:20:36, récepteur `journal-local` |
| Première orientation | Vérifier réponse HTTP, site IIS et journaux de la cible |

L’alerte indique **un échec du contrôle HTTP**, pas automatiquement un arrêt de Windows, un problème réseau ou la cause exacte du défaut. Une valeur `0` est ici le résultat de la sonde, pas un code HTTP.

Les heures précédentes sont celles des captures, en heure locale du lab. La vue Alertmanager affiche aussi `2026-09-16T12:20:15.701Z`, soit 14:20:15.701 à Paris ce jour-là. Conserver cet horodatage comme une donnée de l’alerte, sans le transformer en heure exacte d’arrêt du site ou de livraison au webhook.

## 2. Fixer le périmètre et la chronologie

Dans Grafana et Kibana, choisir une **plage absolue le 16 septembre 2026 de 14:15 à 14:25, heure de Paris**, soit **12:15 à 12:25 UTC**. Vérifier le fuseau réellement utilisé par chaque interface. Élargir avant 14:15 si un changement antérieur semble pertinent.

| Heure de capture locale | Observation | Interprétation permise |
| --- | --- | --- |
| 14:19:34 | Règle HTTP Pending | La condition d’échec est détectée ; attente de persistance en cours |
| 14:19:43 | Sonde IIS à 0 ; collecte endpoint Windows à 1 ; sonde Nginx à 1 | Défaut HTTP Windows, sans perte générale de collecte visible |
| 14:20:29 | Règle HTTP Firing | La condition a persisté assez longtemps pour déclencher |
| 14:20:36 | Alerte présente dans Alertmanager | Transmission Prometheus → Alertmanager constatée |
| 14:20:46 | Terminal conservant HTTP 200 puis `Stop-Website` et site Stopped | Arrêt volontaire visible ; heure des commandes non affichée |
| 14:22:04 | Site Started et réponse locale HTTP 200 | Service local rétabli ; contenu tronqué dans le terminal |
| 14:22:19 à 14:22:42 | Règles Inactive, sonde IIS à 1, Alertmanager vide | Retour au nominal corroboré par plusieurs sources |

Ne pas calculer une durée exacte de panne à partir de ces seules captures. Elles encadrent des observations ; elles ne donnent pas toutes les transitions ni les instants d’exécution des commandes.

## 3. Tableau d’observation complété

| Observation initiale | Information recherchée | Source à consulter | Résultat |
| --- | --- | --- | --- |
| Alerte HTTP critique | Quelle cible et quel service ? | Labels Prometheus / Alertmanager | **Observé :** Windows Core, IIS, URL de health.txt sur le port 8080 |
| État Firing | Quelle condition et quelle durée ? | Règle développée dans Prometheus | **Observé :** sonde à 0 avec collecte de sonde à 1, `for: 1m` |
| Sonde HTTP en échec | Panne du service ou perte de supervision ? | `probe_success`, `up` du job de sonde, collecte endpoint | **Observé :** expression d’alerte avec collecte valide ; dashboard endpoint à 1 ; pas de preuve d’arrêt de Windows |
| Échec sur Windows | Le problème touche-t-il aussi Debian ? | Dashboard Grafana, sonde Nginx | **Observé :** Nginx à 1 tandis qu’IIS est à 0 |
| Durée de sonde proche de 5 s | Timeout, réseau, application ou contrôle de contenu ? | Courbe de durée, détail Blackbox et réponse HTTP | **Observé :** plateau proche de 5 s ; **à rechercher :** détail de l’échec, ce plateau seul ne tranche pas |
| Suspicion de saturation | CPU, mémoire et disque se dégradent-ils simultanément ? | Panneaux ressources Windows sur la même période | **Observé :** pas de hausse manifeste sur les courbes visibles ; **à vérifier :** valeurs détaillées et résolution temporelle |
| Site potentiellement arrêté | Quel état IIS et quelle action récente ? | PowerShell et historique de manipulation du test | **Observé :** `Stop-Website` suivi de `Stopped` ; arrêt volontaire étayé |
| Besoin d’expliquer le changement | Un événement système ou applicatif précède-t-il l’échec ? | Kibana Discover, journaux Windows disponibles | **Observé :** HttpService, code 115, suppression des URL d’un groupe HTTP à 14:18:46.509 |
| Alerte disparue | Le service répond-il réellement à nouveau ? | PowerShell, Grafana, Prometheus, Alertmanager | **Observé :** Started, HTTP 200, sonde à 1, règle inactive, alerte retirée |
| Récepteur `journal-local` affiché | Les notifications ont-elles été reçues ? | Journaux Docker d’`alert-receiver` | **Observé :** `firing` à 12:20:25 UTC puis `resolved` à 12:21:25 UTC ; deux POST HTTP 200 |

Chaque résultat doit être marqué **observé**, **à rechercher**, **non disponible** ou **hypothèse**. Une source ne contenant pas l’information attendue est aussi un résultat à consigner, avec ses limites.

## 4. Rechercher les données complémentaires

### A. Prometheus et Grafana : comparer les mêmes cibles et la même période

Commencer par la règle et ses labels, puis par les sondes : elles permettent de distinguer défaut du service et perte de visibilité. Dans **Grafana → Explore → Prometheus → Code**, examiner séparément les requêtes suivantes sur la plage du test :

```promql
probe_success{job="sonde_windows_http"}
```

```promql
up{job="sonde_windows_http"}
```

```promql
probe_duration_seconds{job="sonde_windows_http"}
```

```promql
up{job="windows"}
```

Comparer avec `probe_success{job="sonde_linux_http"}` si ce job est bien celui chargé dans la configuration du lab. La collecte de l’exporter Windows et la collecte du résultat Blackbox sont deux chemins différents : ne pas utiliser l’un comme preuve de l’autre.

Déplacer le curseur sur les courbes pour relever les valeurs avant, pendant et après l’alerte. Consulter aussi CPU, mémoire et disque Windows dans le dashboard existant, sans confondre avec le stress CPU Debian du test précédent. Une coïncidence temporelle entre deux courbes ne prouve pas une causalité.

Les sélecteurs PromQL filtrent les séries par leurs labels. Vérifier les labels réellement retournés et la présence des données ; une série absente n’est pas une mesure à zéro. [Bases des requêtes Prometheus](https://prometheus.io/docs/prometheus/latest/querying/basics/)

!!! warning "Historique disponible"
    Le lab utilise une rétention Prometheus limitée. Si la période n’est plus conservée, le noter et s’appuyer sur les captures sauvegardées. Une requête vide aujourd’hui ne contredit pas une capture datée. Un contrôle actuel ne reconstitue pas l’état passé.

### B. Kibana : chercher les événements Windows sans présumer leur contenu

Dans **Discover**, choisir la vue **Journaux AlpesNet** et la même période absolue. Commencer par :

```kql
fields.lab_source: "windows"
```

Afficher `@timestamp`, `host.name`, `event.provider`, `event.code`, `winlog.channel` et `message` lorsque ces champs existent. Relever le nom d’hôte dans un document, puis filtrer sa valeur réelle si plusieurs machines Windows sont présentes. Trier chronologiquement pour lire les événements avant et après l’alerte.

Pour examiner les changements de services collectés, essayer ensuite :

```kql
fields.lab_source: "windows" and event.provider: "Service Control Manager"
```

Ce filtre est une piste, pas une promesse de résultat. L’arrêt d’un **site IIS** ne signifie pas l’arrêt d’un **service Windows** ; ne pas exiger arbitrairement un événement 7036. Revenir au filtre large si nécessaire, puis rechercher les fournisseurs et messages effectivement présents. Les filtres KQL sélectionnent des documents, sans établir de lien causal. [Documentation KQL](https://www.elastic.co/docs/explore-analyze/query-filter/languages/kql)

Si aucun document utile n’apparaît, contrôler période, fuseau, hôte, canaux collectés et continuité d’ingestion. Distinguer « aucun événement trouvé dans les données disponibles » de « aucun événement ne s’est produit ». Les journaux d’accès IIS ne sont pas implicitement disponibles dans Kibana parce que Winlogbeat fonctionne ; vérifier leur collecte avant de les citer.

Conserver un extrait pertinent avec horodatage, hôte, fournisseur, code et message. Si `event.ingested` existe, le comparer à `@timestamp` pour repérer un retard ; sinon ne pas inventer une heure d’ingestion.

### C. Vérifications locales et transmission des notifications

Sur **Windows Core, PowerShell administrateur**, ces contrôles lisent l’état actuel sans arrêter le site :

```powershell
Import-Module WebAdministration
Get-Website -Name 'AlpesNet-Sonde'
Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:8080/health.txt' |
  Select-Object StatusCode, Content
```

Comparer la réponse locale au résultat de la sonde distante. Le détail Blackbox se recherche avec la [procédure de diagnostic des sondes](../it-1/creer-configurer-sondes.md), en conservant module, URL, résultat et moment du contrôle. Une réponse locale correcte avec une sonde distante en échec oriente vers le chemin réseau ou la configuration du contrôle ; elle ne prouve pas automatiquement un défaut de pare-feu.

Sur **supervision**, pour examiner les notifications conservées de la période :

```bash
cd ~/observabilite
sudo docker compose logs --no-color \
  --since='2026-09-16T12:15:00Z' \
  --until='2026-09-16T12:25:00Z' alert-receiver
```

Rechercher `ServiceHTTPIndisponible`, `windows-core`, les états et les heures `received_at`. La capture conservée montre `firing`, puis `resolved`, avec HTTP 200 pour les deux POST. Les horaires `received_at` sont en UTC.

## 5. Formuler et départager les hypothèses

Une hypothèse doit expliquer les observations et proposer un contrôle capable de la renforcer ou de l’affaiblir. En choisir au moins deux avant de conclure ; ne pas présenter toutes les pistes comme des causes confirmées.

| Hypothèse | Indices compatibles | Vérification discriminante | Bilan pour ce test |
| --- | --- | --- | --- |
| **H1 — Le site IIS a été arrêté volontairement** | Sonde HTTP à 0, exporter Windows joignable, autres services supervisés disponibles | Examiner état du site et action d’administration, puis réponse après reprise | **Étayer par les preuves :** la capture contient `Stop-Website` puis Stopped ; après reprise, Started, HTTP 200 et sonde à 1. C’est l’explication retenue pour l’exercice contrôlé |
| **H2 — Le chemin réseau vers le port 8080 est perturbé** | Sonde distante en échec, durée proche de 5 s, exporter joignable sur un autre port | Pendant l’incident, comparer HTTP local et sonde distante ; examiner écoute, filtrage et erreur Blackbox | **Non démontrée :** l’exporter accessible n’exclut pas un défaut propre à 8080 ; la preuve d’arrêt du site rend cette hypothèse moins nécessaire, sans exclure un défaut concomitant |
| **H3 — Le contrôle HTTP est mal configuré ou le contenu a changé** | VM collectée mais sonde HTTP à 0 | Vérifier URL, module, statut et marqueur attendus ; comparer avec une réponse complète et les changements récents | **Non démontrée :** le retour de la sonde à 1 après reprise est compatible avec le rétablissement du site ; aucune erreur de module n’est prouvée |

**Conclusion proportionnée :** le test documente une indisponibilité HTTP provoquée par l’arrêt du site, détectée puis rétablie. L’événement HttpService renforce la chronologie et le webhook prouve les notifications. Le test ne démontre ni une panne complète de Windows ni une saturation CPU Windows ; l’auteur et l’heure exacte des commandes ne sont pas fournis par les journaux.

## Questions de fin d’étape

| Question | Réponse attendue |
| --- | --- |
| Que vous apprend directement l’alerte ? | La condition détectée, la cible, le service, la criticité, l’état et les informations configurées. |
| Quelles informations manquent ? | Cause, auteur éventuel du changement, impact utilisateur complet, chronologie précise et détails techniques non inclus dans les annotations. |
| Quelle source consulter en premier ? | La règle et ses labels pour cadrer la recherche, puis les métriques et sondes qui la déclenchent ; ensuite les journaux et contrôles adaptés à la piste. |
| Pourquoi compléter l’alerte ? | Pour distinguer les causes possibles, mesurer l’étendue et choisir une action appropriée. |
| L’alerte suffit-elle à identifier la cause ? | Non : une même condition HTTP peut résulter d’un site arrêté, d’un chemin réseau défaillant ou d’un contrôle incorrect. |
| Comment choisir les données pertinentes ? | Même cible, même période et fuseau, données suffisamment fraîches et détaillées, source fiable, capacité à départager une hypothèse. |

## Trace d’analyse à conserver

Conserver le tableau d’observation, la plage horaire et le fuseau, les références des captures, les requêtes exécutées et leurs résultats réels, au moins deux hypothèses avec leur contrôle discriminant, puis la conclusion et ses limites. Relier l’action éventuelle à la [procédure de réponse HTTP](construire-procedure-reponse.md#b-servicehttpindisponible).

- [ ] Je retrouve l’élément concerné et la condition qui a déclenché.
- [ ] Je distingue heure de capture, détection et réception.
- [x] Je compare sondes, métriques et journaux sur une période commune.
- [ ] Je signale les données absentes ou non collectées.
- [ ] Je propose au moins deux hypothèses et un contrôle pour chacune.
- [ ] Ma conclusion distingue faits, déductions et incertitudes.

[Procédures de réponse — L3](construire-procedure-reponse.md) · [Sommaire de l’itération](index.md) · [Pense-bête](../../pense-bete/glossaire/supervision-optimisation-performances/it-2.md)

[Suite — Formuler et vérifier des hypothèses](formuler-verifier-hypotheses.md)
