# Simulation croisée — Vérifier le dispositif d’observabilité

## Contexte et situation professionnelle

**Comment vérifier que notre dispositif de supervision permet réellement d’observer une infrastructure et de détecter les événements qui l’affectent ?**

Au sein de l’équipe Infrastructure d’AlpesNet, chaque binôme dispose d’un endpoint Linux, d’un endpoint Windows, de services, de sources de journaux et des outils d’observabilité déjà déployés.

Le responsable souhaite qu’un administrateur puisse comprendre ce qui se passe **sans connaître à l’avance les événements prévus**. Chaque binôme prépare donc son environnement et trois événements, puis confie leur observation à un autre binôme. Les équipes confrontent ensuite actions, observations et preuves pour améliorer la supervision.

!!! note "État du laboratoire et limites des preuves"
    Les feuilles précédentes documentent les métriques Linux/Windows, les sondes avec panne et rétablissement, ainsi que les journaux retrouvés dans ELK. Le 15 septembre 2026, l’utilisateur confirme que les IP sont restées correctes à la reprise. La simulation croisée n’est pas encore attestée. Un dashboard manuel à neuf panneaux est maintenant illustré dans la feuille dédiée, avec des réglages à finaliser avant la simulation. Les cases ci-dessous correspondent à une nouvelle vérification avant l’exercice.

## 1. Préparer l’environnement et les rôles

| Machine du laboratoire | Adresse | Rôle |
| --- | --- | --- |
| `supervision` | `192.168.122.80` | Prometheus, Grafana, Blackbox, Elasticsearch, Kibana et Logstash |
| `debian13` | `192.168.122.158` | Endpoint Debian, Nginx, Node Exporter et Filebeat |
| `win2k25` | `192.168.122.25` | Windows Server Core, IIS, windows_exporter et Winlogbeat |

Les [réservations DHCP](identifier-elements-observer.md#adresses-stabilisees-par-reservation-dhcp) associent ces adresses aux MAC des VM. Dans un autre laboratoire, remplacer cet inventaire par les données réelles.

- **Binôme organisateur** : prépare la fiche confidentielle, provoque les événements, note leurs horaires exacts et restaure les services.
- **Binôme observateur** : surveille les interfaces, note les anomalies, propose des explications et conserve les preuves, sans consulter la fiche confidentielle.
- Après le débriefing, **inverser les rôles** pour une seconde séquence.

Communiquer aux observateurs le périmètre, les noms des hôtes et services, les accès, la fenêtre globale de l’exercice et les contacts. Garder confidentiels le choix précis des événements, leur ordre, leurs heures et les marqueurs recherchés. Ne pas montrer la console où les actions sont lancées.

Les adresses `192.168.122.x` sont celles du réseau privé du laptop : un autre laptop ne peut pas les utiliser directement sans accès réseau prévu. Pour ce laboratoire, les observateurs peuvent utiliser les interfaces ouvertes sur le laptop hôte, tandis que les organisateurs gardent leurs consoles séparées. Vérifier les accès avant de commencer et ne pas publier les interfaces sur Internet.

Si aucun autre binôme n’est disponible, réaliser un entraînement avec une autre personne qui choisit et déclenche les actions. Un exercice effectué seul en connaissant les actions reste un autotest ; ne pas le présenter comme une observation à l’aveugle.

## 2. Vérifier l’état nominal avant la simulation

| Domaine | Contrôle | Preuve à conserver | Validé |
| --- | --- | --- | --- |
| Endpoints | Linux et Windows présents ; métriques récentes collectées | `up=1`, mesure par hôte et dernier scrape | ☐ |
| Sondes | Sonde Linux et sonde Windows fonctionnelles | Deux `probe_success=1`, HTTP 200 et contenu attendu | ☐ |
| Logs | Sources Linux et Windows reçues dans ELK | Un événement récent identifié pour chaque source | ☐ |
| Mesure | KPI disponibles et dashboard accessible aux observateurs | Dashboard enregistré avec noms, unités et période lisibles | ☐ |
| Temps | Horloges cohérentes et actualisation configurée | Fuseau retenu et heures comparables entre outils | ☐ |
| Rétablissement | Méthode de retour nominal disponible pour chaque action | Commande de restauration et accès console prêts | ☐ |

Une ancienne capture ne valide pas l’état de départ du jour. Corriger tout défaut avant de lancer la simulation ; ne pas confondre une panne préexistante avec un événement provoqué.

### Contrôler les endpoints et les sondes

Dans **Prometheus → Query**, exécuter séparément :

```promql
up{job=~"linux|windows|sonde_.*|blackbox"}
```

```promql
probe_success{job=~"sonde_.*"}
```

```promql
scrape_samples_scraped{job=~"linux|windows"}
```

Vérifier la présence de toutes les séries attendues, des collectes réussies et des échantillons reçus. Dans Targets, observer le dernier scrape sur plusieurs cycles. Une série absente n’est pas un succès. **`up` décrit la collecte ; `probe_success` décrit le contrôle du service.**

### Contrôler les journaux

Dans **Kibana Discover**, sélectionner `Journaux AlpesNet`, choisir une période récente et consulter successivement :

```kql
fields.lab_source: "linux"
```

```kql
fields.lab_source: "windows"
```

Vérifier `@timestamp`, `host.name`, `agent.type` et `message`. Si nécessaire, générer un événement de préparation distinct de ceux de l’exercice, suivant la [feuille des logs](ajouter-source-logs.md). Identifier cet événement comme un contrôle préalable et démarrer la simulation après sa réception.

## 3. Vérifier le dashboard de préparation

Réaliser la feuille dédiée [Construire un premier dashboard Grafana](construire-dashboard-grafana.md) avant cette simulation. Elle regroupe l’import, la construction des panneaux, le choix des KPI, les unités et les contrôles sur les deux endpoints.

Avant l’exercice, vérifier que le dashboard enregistré est accessible au binôme observateur, que les données sont récentes et que les unités sont comprises. Le scénario confidentiel reste séparé du dashboard. Les notifications automatiques ne sont pas encore configurées dans ce parcours.

## 4. Préparer trois événements confidentiels

Chaque binôme choisit **exactement trois événements**, couvrant les trois familles ci-dessous. Les possibilités sont publiques ; le choix réel et le calendrier restent dans une fiche privée.

| Événement | Possibilités à adapter | Donnée attendue | Retour nominal à prévoir |
| --- | --- | --- | --- |
| 1 — Disponibilité | Arrêt du site IIS dédié, indisponibilité de la ressource HTTP Nginx, arrêt d’un service réseau de test | `probe_success=0`, état du service ou réponse incorrecte | Redémarrage du site ou restauration de la ressource ; retour à 1 |
| 2 — Performance | Charge CPU limitée, consommation mémoire bornée ou création d’un fichier de test de taille limitée | Évolution de la métrique retenue par rapport au niveau initial | Fin automatique ou arrêt de la charge ; libération de la ressource |
| 3 — Journalisation | Événement Application Windows ou message journald de test | Événement centralisé avec source, heure et message | Fin de l’action ; conserver le journal comme preuve |

Répartir si possible les actions entre Linux et Windows. Conserver Prometheus, les exporters, Blackbox et les collecteurs de logs actifs pour observer les effets.

Définir à l’avance une durée maximale, un moyen d’arrêt et une procédure de restauration. Ne pas remplir le disque, épuiser toute la RAM ou multiplier les échecs d’authentification au risque de verrouiller un compte. La préproduction du laptop héberge aussi les outils nécessaires à l’exercice.

### Exemple de charge CPU bornée, à choisir uniquement dans la fiche privée

Sur **l’endpoint Debian**, si Python 3 est installé, cet exemple utilise un seul processus pendant environ deux minutes ; `timeout` impose une limite supplémentaire. Il est fourni comme possibilité, pas comme événement déjà choisi ni exécuté :

```bash
timeout 130s nice -n 10 python3 - <<'PYCPU'
import time
end = time.monotonic() + 120
while time.monotonic() < end:
    sum(i * i for i in range(10000))
PYCPU
```

`Ctrl+C` permet d’interrompre ce processus dans sa console. La hausse attendue dépend du nombre de vCPU et de la charge du laptop : un processus ne saturera pas nécessairement le pourcentage moyen de la VM. Observer le retour au niveau initial après la fin, en tenant compte du lissage de la courbe.

Pour les autres actions, reprendre les commandes de [panne et restauration des sondes](creer-configurer-sondes.md#7-provoquer-une-indisponibilite-et-verifier-le-retablissement) et de [génération de journaux](ajouter-source-logs.md), sans révéler aux observateurs le marqueur choisi.

### Fiche de simulation — à préparer secrètement

Copier ce tableau **dans un document privé, hors de `docs/`, des assets et du dépôt partagé**. Une section repliée ou une page absente du menu MkDocs ne rend pas son contenu confidentiel. Ne publier la fiche remplie qu’après le débriefing si cela est demandé.

Binôme organisateur : … · Binôme observateur : … · Fenêtre de simulation : … · Fuseau : …

| Événement | Action réalisée | Donnée attendue | Source |
| --- | --- | --- | --- |
| 1 — Disponibilité | À renseigner confidentiellement | À renseigner | Sonde |
| 2 — Performance | À renseigner confidentiellement | À renseigner | Métrique |
| 3 — Journalisation | À renseigner confidentiellement | À renseigner | Log |

Pour chaque ligne, préciser en privé : hôte, commande exacte, heure prévue puis heure réelle, durée maximale, arrêt d’urgence, restauration et preuve locale. Les horaires réels serviront à comparer la chronologie de l’observateur.

## 5. Faire observer sans dévoiler les actions

1. Faire valider l’état nominal et les accès par les deux binômes.
2. Démarrer l’observation et noter l’heure commune de début.
3. L’organisateur déclenche ses événements dans l’ordre privé, sans les annoncer. Pour cette première séance, restaurer l’état nominal entre les événements qui modifient le service ou les ressources.
4. L’observateur suit les courbes, les sondes et les logs, note les changements et conserve ses hypothèses **avant** de recevoir les explications.
5. Clore l’observation, vérifier le rétablissement et seulement ensuite ouvrir la fiche confidentielle.

Pour les sondes collectées toutes les 30 secondes, maintenir l’indisponibilité au moins deux cycles pour le premier exercice. Une panne située entièrement entre deux collectes peut ne pas être visible. Pour les performances, attendre suffisamment de mesures pour distinguer la variation du bruit habituel.

## 6. Grille d’observation et débriefing

Cette grille appartient aux observateurs : elle ne contient pas le scénario préparé.

| Heure de première observation | Hôte/service suspecté | Changement observé | Source et preuve | Hypothèse | Confiance / vérification restante |
| --- | --- | --- | --- | --- | --- |
| … | … | … | … | … | … |
| … | … | … | … | … | … |
| … | … | … | … | … | … |

Après révélation du scénario, comparer :

| Événement | Heure réelle de l’action | Heure de détection par l’observateur | Détecté ? | Interprétation correcte ? | Amélioration nécessaire |
| --- | --- | --- | --- | --- | --- |
| Disponibilité | … | … | ☐ | ☐ | … |
| Performance | … | … | ☐ | ☐ | … |
| Journalisation | … | … | ☐ | ☐ | … |

Calculer le **délai d’observation** comme l’heure de première détection humaine moins l’heure réelle de l’action. Ne pas le confondre avec la durée de la sonde, le timestamp du journal ou un délai d’alerte automatique. Si les heures ne sont pas disponibles, noter « non mesuré ».

Une cause exacte n’est pas toujours déductible d’un seul signal : distinguer « service HTTP indisponible » de « site IIS arrêté ». Consigner aussi les faux positifs, les événements manqués et les données qui auraient permis de lever le doute.

| Difficulté | Amélioration possible | Nouvelle vérification |
| --- | --- | --- |
| Panne masquée par Targets UP | Afficher `probe_success` séparément de `up` | Rejouer le contrôle et observer 1 → 0 → 1 |
| Hausse CPU illisible | Vérifier unité, moyenne par hôte et fenêtre de calcul | Comparer repos, charge et retour au repos |
| Journal difficile à retrouver | Ajouter hôte, canal, code et message dans Discover | Retrouver un nouvel événement sans connaître son marqueur |
| Données anciennes ou absentes | Vérifier collecte, période et actualisation | Observer de nouvelles mesures et de nouveaux événements |

Modifier une chose à la fois, noter la configuration avant/après et rejouer seulement le contrôle concerné. Un signal présent dans la plateforme mais non remarqué par l’observateur révèle un besoin de présentation ou de procédure.

## 7. Traces et point de contrôle

Conserver le relevé nominal, les captures horodatées, la grille de l’observateur, la fiche confidentielle révélée après exercice, les configurations modifiées et la preuve du retour nominal. Identifier clairement les événements simulés et les résultats réellement observés.

- [ ] Endpoints, sondes et logs sont fonctionnels au début de la séance.
- [ ] Le dashboard et les KPI utiles sont accessibles et compréhensibles.
- [ ] Trois événements ont été préparés confidentiellement : disponibilité, performance, journalisation.
- [ ] Un autre binôme les a observés sans connaître le scénario.
- [ ] Les actions et les observations ont été comparées avec leurs preuves.
- [ ] Les écarts ont donné lieu à des améliorations et à une vérification ciblée si nécessaire.
- [ ] L’environnement est revenu à son état nominal.

[Retour au sommaire de l’itération](index.md)
