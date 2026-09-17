# Préparer la mise en situation — Diagnostic autonome

## Objectif de la séquence

Mettre en œuvre de manière autonome une démarche de détection, de diagnostic et de traitement d’un incident à partir des données d’observabilité, puis formaliser le diagnostic réalisé.

> **Situation professionnelle :** un incident vient de se produire sur l’infrastructure. Il faut le prendre en charge, identifier sa cause probable, appliquer ou proposer une action adaptée et vérifier le retour à la normale.

Cette feuille prépare les outils et les traces nécessaires. Elle ne décrit pas encore l’incident qui sera déclenché. Une fois la préparation validée, le formateur se retire complètement de la mise en situation : l’apprenant conduit seul le diagnostic et consigne ses décisions.

## 1. Distinguer preuve antérieure et disponibilité actuelle

Les activités précédentes attestent qu’au **16 septembre 2026**, Prometheus, Grafana, les sondes Blackbox, les journaux centralisés, Alertmanager et le récepteur local ont été utilisés. Le scénario IIS a également produit une alerte `firing`, une notification `resolved` et un retour fonctionnel du site.

Ces preuves ne garantissent pas que la plateforme est encore prête au début de l’exercice. Chaque contrôle ci-dessous doit donc être refait en direct. Une donnée ancienne, une cible absente ou une interface simplement accessible ne suffit pas.

## 2. Vérifier les prérequis

Depuis la VM de supervision :

```bash
cd ~/observabilite
sudo docker compose config --quiet
sudo docker compose ps
curl --fail http://127.0.0.1:9090/-/ready
curl --fail http://127.0.0.1:9093/-/ready
```

La configuration Compose doit être valide. Prometheus et Alertmanager doivent répondre qu’ils sont prêts. Dans la sortie Compose, vérifier également les services utilisés par le diagnostic : Grafana, Blackbox Exporter, Elasticsearch, Kibana, `logstash-logs` et `alert-receiver`.

Si un service attendu n’est pas actif, examiner d’abord ses journaux sans redémarrer toute la plateforme :

```bash
sudo docker compose logs --tail=80 NOM_DU_SERVICE
```

### Grille de préparation

| Élément requis | Vérification à effectuer | Critère « prêt » | Résultat à relever |
| --- | --- | --- | --- |
| Plateforme d’observabilité | État des services Compose et absence d’erreur bloquante | Tous les services nécessaires au scénario sont actifs | Services, état, date et heure |
| Alertes configurées | Prometheus **Alerts** et Alertmanager | Les cinq règles sont chargées ; Alertmanager est joignable | Nombre de règles et état initial |
| Dashboards | Ouvrir Grafana depuis le laptop | Les panneaux affichent des données récentes, sans erreur de source | Dashboard, plage temporelle et heure du dernier point |
| Endpoints | Requête Prometheus `up{job=~"linux|windows"}` | Une série récente vaut `1` pour chaque endpoint attendu | Job, instance, valeur et horodatage |
| Sondes | Requêtes `up{job=~"sonde_.*|blackbox"}` et `probe_success{job=~"sonde_.*"}` | Collecte et contrôle fonctionnel valent `1` | Cible, résultat et durée de sonde |
| Journaux | Kibana **Discover**, vue `Journaux AlpesNet` | Des événements récents Linux et Windows sont recherchables | Source et dernier horodatage visible |
| Procédures de réponse | Ouvrir les procédures des alertes | L’alerte testée possède seuil, criticité, vérifications, action et escalade | Nom de la procédure retenue |
| Suivi temporel | Modifier la plage de temps dans Grafana et Kibana | L’évolution avant, pendant et après peut être affichée | Fuseau horaire et plage retenue |

Une série absente ne vaut pas `0` : elle peut signaler une collecte interrompue ou une mauvaise requête. Il faut vérifier la fraîcheur des points avant de conclure.

## 3. Vérifier les interfaces depuis le laptop

Si les tunnels ne sont pas déjà ouverts, lancer depuis le laptop et conserver le terminal actif :

```bash
ssh -N -o ExitOnForwardFailure=yes \
  -L 3000:127.0.0.1:3000 \
  -L 5601:127.0.0.1:5601 \
  -L 9090:127.0.0.1:9090 \
  -L 9093:127.0.0.1:9093 \
  oliv@192.168.122.80
```

Ouvrir ensuite :

- Prometheus : `http://127.0.0.1:9090` ;
- Grafana : `http://127.0.0.1:3000` ;
- Kibana : `http://127.0.0.1:5601` ;
- Alertmanager : `http://127.0.0.1:9093`.

Dans Prometheus, contrôler **Status > Targets**, **Alerts** et les requêtes de la grille. Dans Kibana, filtrer successivement les événements Linux et Windows, puis vérifier que le dernier document correspond à l’état actuel du lab. Ne pas enregistrer de secret, de jeton ou d’identifiant inutile dans les captures.

## 4. Préparer l’espace de travail

Créer un dossier distinct pour conserver les éléments du futur diagnostic :

```bash
cd ~/observabilite
INCIDENT_ID="incident-$(date +%Y%m%d-%H%M%S)"
install -d -m 700 "diagnostics/$INCIDENT_ID"/{captures,exports,journaux}
printf '%s\n' "$INCIDENT_ID"
```

Créer dans ce dossier un fichier `chronologie.md` et y utiliser le tableau suivant :

| Heure et fuseau | Source | Observation factuelle | Hypothèse | Recherche ou action | Résultat | Décision suivante |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

Noter l’heure **avant** chaque recherche ou action. Employer le même fuseau dans tout le rapport, ou indiquer explicitement les conversions UTC/heure de Paris. Séparer ce qui est observé, supposé et vérifié.

### Traces à conserver

- l’alerte initiale avec son nom, sa cible, sa criticité et son horodatage ;
- les requêtes PromQL et leur plage temporelle ;
- les états des sondes et des endpoints ;
- les filtres Kibana et les événements utiles ;
- les extraits de journaux applicatifs ou système nécessaires ;
- les hypothèses acceptées ou écartées et les preuves associées ;
- les actions réalisées, avec leur heure et leur résultat ;
- les contrôles de retour à la normale et une période de stabilité.

Les captures illustrent une observation ; les exports textuels et les requêtes rendent l’analyse reproductible. Limiter chaque trace au périmètre utile et masquer toute donnée sensible.

## 5. Décider si la mise en situation peut commencer

| Point de contrôle | Oui | Non | Observation |
| --- | :---: | :---: | --- |
| Les interfaces Prometheus, Grafana, Kibana et Alertmanager sont accessibles | V | ☐ | |
| Les cibles Linux et Windows remontent des métriques récentes | V | ☐ | |
| Les sondes produisent un résultat récent et exploitable | ☐ | ☐ | |
| Les journaux Linux et Windows sont recherchables | V | ☐ | |
| Les règles d’alerte et le récepteur de notifications sont disponibles | V | ☐ | |
| La procédure associée à l’alerte du scénario est accessible | V | ☐ | |
| Le dossier de diagnostic et la chronologie sont prêts | V | ☐ | |
| Le fuseau horaire de référence est noté | V | ☐ | |

La mise en situation commence lorsque tous les points nécessaires au scénario sont validés. En cas d’échec, consigner le blocage et rétablir le prérequis concerné avant le retrait du formateur : un défaut de l’outil de diagnostic ne doit pas être confondu avec l’incident étudié.

Pendant l’exercice, ne pas supprimer de données et ne pas arrêter l’ensemble de la plateforme. Toute action corrective doit rester ciblée, traçable et proportionnée. Si elle dépasse les droits accordés ou présente un risque pour l’environnement, appliquer l’escalade prévue dans la [procédure de réponse](construire-procedure-reponse.md).

## État attendu

La plateforme fournit des métriques, des résultats de sondes, des journaux, des dashboards et des alertes actuels. Les procédures sont accessibles et un espace horodaté permet de conserver toute la démarche. L’apprenant peut alors partir du signal reçu, formuler des hypothèses, les vérifier, agir et démontrer le retour à la normale sans assistance du formateur.

## Suite de la démarche

- [Prendre en charge l’incident](prendre-en-charge-incident.md)
- [Partir d’une alerte pour rechercher ce qui s’est produit](partir-alerte-rechercher-situation.md)
- [Formuler et vérifier des hypothèses](formuler-verifier-hypotheses.md)
- [Corréler les métriques, les sondes et les journaux](correler-metriques-sondes-journaux.md)
- [Identifier la cause probable](identifier-cause-probable.md)
- [Vérifier le retour à la normale](verifier-retour-normale.md)
- [Retour au sommaire de l’itération](index.md)
