# Reprendre le dispositif de détection

**Itération 9 — 9 octobre 2026 — Travail individuel**

## 🎯 Objectif

Vérifier l’état des différentes sources de détection avant leur utilisation.
Reprendre l’environnement de J8, générer quelques activités connues et
retrouver les informations attendues. Un processus actif ne suffit pas :
la chaîne **activité → source → collecte → information retrouvée** doit être contrôlée.

**Statut : reprise partiellement vérifiée par les sorties fournies le 9 octobre.
Suricata : trois règles locales déclenchées. File Browser : réponses HTTP
200/401 observées. Agent Wazuh reconnecté ; deux nouveaux messages
applicatifs reçus et décodés dans les archives du manager. Contrôles négatifs,
usage authentifié et alerte applicative Wazuh spécifique restent à compléter.**

## Résultats de reprise — sorties fournies le 9 octobre 2026

Les résultats ci-dessous proviennent des commandes exécutées par Olivier et
transmises en texte ; aucun contrôle distant supplémentaire n’a été réalisé.

| Contrôle | Résultat observé | Portée de la preuve |
| --- | --- | --- |
| VM et trajet | `enp1s0` UP, `192.168.122.229/24` ; route hôte vers VM par `virbr0`, source `192.168.122.1` | Adresse et trajet confirmés |
| Suricata | 8.0.3, actif depuis 08:55:30 CEST ; service utilisant `/etc/suricata/suricata.yaml` avec AF_PACKET | Un redémarrage automatique figure dans le journal ; sa cause n’est pas établie |
| Règles | Deux fichiers, sept signatures chargées, zéro échec/ignorée, code 0 | Configuration acceptée ; trois déclenchements ci-dessous |
| Journal EVE | Fichier présent, 65 Mo à 10:21 ; nouveaux objets d’alerte fournis | Activités réseau effectivement retrouvées |
| File Browser | GET `/` : HTTP 200 ; POST `/api/renew` sans authentification : HTTP 401 | Service HTTP répondant ; authentification et opération sur fichier T1 non vérifiées |
| Docker sur la VM | Refus initial sans sudo, puis commandes réussies avec sudo : File Browser `running`, `healthy`, port 8080 → 80, driver `json-file` | Conteneur actif ; chemin courant concordant avec celui annoncé par logcollector |
| Agent Wazuh | Cinq processus annoncés running ; fichier Docker surveillé par logcollector | Processus et source déclarée, pas preuve de réception du nouvel événement |
| Connexion Wazuh | Erreur à 10:17:46, puis Connected à `192.168.122.37:1514/TCP` à 10:17:56 ; agent online ensuite | Reconnexion documentée après une erreur transitoire ; cause initiale non établie |
| Stack Wazuh | Manager, dashboard et indexer Up 15 minutes | Conteneurs démarrés ; disponibilité du dashboard et santé de l’indexer non contrôlées par cette seule sortie |
| SCA | Politique Ubuntu 22.04 ignorée : `Check Ubuntu version.` | Cette politique ne fournit pas de résultat de conformité pour la VM actuelle |
| Test logcollector | Nouveau test fourni avec `Code du test : 0` | Configuration acceptée ; réception confirmée par les deux objets du manager ci-dessous |

### Trois alertes locales désormais observées

Horaires EVE du **9 octobre 2026, UTC+02:00** :

| SID | Heure / flux | Activité et interprétation |
| --- | --- | --- |
| 1008001 | 10:21:34.419233 ; `1797495602826803` | GET `/?ais_probe=%2e%2e`, hôte:55142 → VM:8080, réponse 200. Motif encodé détecté ; pas de preuve d’exploitation |
| 1008002 | 10:21:38.466507 ; `593686364267183` | GET `/`, hôte:37612 → VM:8080, réponse 200, après la boucle de cinq GET. Déclenchement du seuil pédagogique ; pas de preuve d’attaque |
| 1008003 | 10:32:45.084757 ; `1486062693647918` | POST `/api/renew`, réponse 401 ; événement orienté VM:8080 → hôte:59460. Détection du statut de réponse ; pas de preuve de force brute |

Les trois objets affichent `action:allowed` : **détection sans blocage**.
Les nouvelles preuves J9 complètent les déclenchements 1008002/1008003 qui
n’étaient pas validés en J8 ; elles ne modifient pas rétroactivement le bilan J8.
Le GET isolé sans marqueur a retourné 200 ; aucune recherche exhaustive sur
sa fenêtre n’est fournie pour prouver le contrôle négatif de 1008001.

### Essai supplémentaire depuis la VM — 10:34:37 CEST

Une nouvelle série a été exécutée **sur la VM File Browser elle-même**
(prompt `oliv@oliv-Standard-PC-Q35-ICH9-2009`), vers sa propre adresse
`192.168.122.229:8080`. Début et fin affichés :
`2026-10-09T10:34:37+02:00` (précision à la seconde).

| Requête | Résultat fourni |
| --- | --- |
| GET `/?ais_probe=%2e%2e` | HTTP 200 |
| GET `/` | HTTP 200 |
| POST `/api/renew` sans cookie ni jeton | HTTP 401 |

Cela confirme les réponses HTTP depuis la VM. Une connexion à sa propre
adresse est normalement routée localement et ne traverse pas le bridge de
l’hôte : **ne pas utiliser cette série pour valider la capture Suricata sur
virbr0**, ni la confondre avec les trois alertes précédentes générées depuis
l’hôte. Aucune nouvelle alerte EVE correspondant à cette série n’est fournie.

Le POST 401 peut en revanche servir à vérifier les journaux Docker et leur
réception Wazuh, indépendamment de ce trajet réseau. Rechercher ce nouveau
message vers **10:34:37 CEST / 08:34:37 UTC** en distinguant heure applicative,
heure Docker et heure de réception. Les lignes Docker et leur réception côté manager sont désormais fournies
ci-dessous.

### Vérification Docker et collecteur — complément fourni

Les commandes reprises avec `sudo` réussissent : conteneur `f9810c6225f6`,
image affichée `filebrowser/filebrowser` (version précise non déduite de ce
nom), état **running / healthy**, publication **8080 → 80**. Le driver est
`json-file` et le chemin retourné par l’inspection correspond exactement au
fichier annoncé comme surveillé par logcollector lors de son démarrage.

Deux traces applicatives sont retrouvées dans `docker logs` :

```text
2026/10/09 08:32:45 /api/renew: 401 192.168.122.1 <nil>
2026/10/09 08:34:37 /api/renew: 401 192.168.122.229 <nil>
```

La première correspond à l’essai depuis l’hôte (10:32:45 CEST), également
visible dans l’alerte Suricata 1008003. La seconde correspond à l’essai local
VM (10:34:37 CEST). Le décalage de deux heures est cohérent avec UTC dans
ces traces applicatives, sans fuseau explicite dans leur format.

Le nouveau `wazuh-logcollector -t` retourne **0**. La source produit donc
bien les messages et sa configuration de collecte est acceptée. Ces sorties locales sont complétées par la preuve de réception suivante.

### Réception Wazuh de bout en bout — preuve J9 fournie

La recherche dans `archives.json` du conteneur manager retrouve les **deux
nouveaux messages**. Chaque objet sélectionné porte l’agent **001**, nom
`vm-filebrowser`, IP `192.168.122.229`, le décodeur `json`, `stream:stdout`
et la même `location` Docker que l’inspection locale et le collecteur.

| Essai | Message applicatif (`data.log`) | Horodatage Docker (`data.time`, UTC) | Réception manager (`timestamp`, UTC) |
| --- | --- | --- | --- |
| Depuis l’hôte | `2026/10/09 08:32:45 /api/renew: 401 192.168.122.1 <nil>` | `2026-10-09T08:32:45.065601672Z` | `2026-10-09T08:32:46.751+0000` |
| Depuis la VM | `2026/10/09 08:34:37 /api/renew: 401 192.168.122.229 <nil>` | `2026-10-09T08:34:37.550156346Z` | `2026-10-09T08:34:38.763+0000` |

**Conclusion : collecte File Browser → fichier Docker JSON → agent VM →
manager Wazuh vérifiée en J9 pour ces deux activités.** La première est
également corrélée à l’alerte réseau Suricata 1008003 à 10:32:45 CEST.
Ce rapprochement des preuves ne signifie pas que Suricata est ingéré dans Wazuh.

Les sorties sont des objets projetés par `jq`, pas les objets bruts complets.
Elles prouvent la réception et le décodage JSON ; aucune règle Wazuh dédiée,
alerte correspondante ou indexation dashboard de ces deux messages n’est
montrée. Le 401 reste un refus de renouvellement de session, sans attaque établie.

### Tableau des sources au dernier état fourni

| Source | Fonctionnelle ? | Informations disponibles | Limites connues |
| --- | --- | --- | --- |
| Suricata | **Oui pour les trois scénarios testés** | Alertes 1008001/1008002/1008003, heures, flux, IP/ports, URI, méthodes et statuts | Contrôles négatifs à compléter ; visibilité de virbr0 et HTTP en clair ; aucun blocage |
| Wazuh | **Oui pour la collecte et le décodage des deux essais 401** | Deux messages reçus dans les archives, agent 001, location Docker concordante, décodeur JSON, heures et messages | Alerte applicative spécifique et indexation non démontrées ; dashboard/indexer à contrôler ; politique SCA ignorée ; agent dans le conteneur absent |
| Logs Docker File Browser | **Oui pour les deux essais 401** | Messages à 08:32:45 et 08:34:37, IP hôte/VM, driver JSON et chemin courant concordant ; test collecteur code 0 | Réception Wazuh confirmée ; continuité après rotation/recréation non testée |

### Commandes de contrôle utilisées et vérification restante

Sur la **VM File Browser**, les commandes suivantes ont désormais été
exécutées avec succès ; elles sont conservées comme référence :

```bash
sudo docker ps --filter name=filebrowser
sudo docker inspect --format '{{.State.Status}} {{.HostConfig.LogConfig.Type}} {{.LogPath}}' filebrowser
sudo docker logs --since '2026-10-09T10:30:00+02:00' filebrowser 2>&1 | rg '/api/renew'
sudo /var/ossec/bin/wazuh-logcollector -t
echo "Code du test : $?"
```

Sur la **VM Wazuh**, cette recherche a retrouvé les deux messages J9 ;
commande conservée comme référence :

```bash
sudo docker exec single-node-wazuh.manager-1 \
  tail -n 5000 /var/ossec/logs/archives/archives.json | jq -c '
  select(.agent.id == "001")
  | select(.timestamp | startswith("2026-10-09"))
  | select((.data.log // "") | contains("/api/renew"))
  | {timestamp,agent,location,decoder,data}'
```

Comparer l’heure et le message avec la trace Docker de 10:32 environ (08:32
UTC si ces horodatages sont en UTC). Si la sélection est vide, élargir la
recherche et vérifier l’état des archives ; les 5 000 dernières lignes ne
constituent pas une recherche exhaustive. Compléter l’accès dashboard et
l’état de l’agent sans republier d’identifiants ou de jetons.

---

La procédure ci-dessous reste disponible comme référence ; les résultats
ci-dessus font foi pour les étapes déjà effectuées.

## 1. Point de départ documenté en J8

| Élément | Dernière preuve disponible | Ce qui reste à vérifier aujourd’hui |
| --- | --- | --- |
| File Browser | Service joint sur VM `192.168.122.229:8080` ; Ubuntu 26.04.1 LTS relevé | Adresse actuelle, accès et activité applicative normale |
| Suricata | Version 8.0.3 sur l’hôte, capture sur `virbr0`, service actif | Configuration réellement utilisée, capture et nouveaux objets EVE |
| Règles retenues | Sept règles acceptées ; SID 1008001 déclenché sur 8080 | Jeu conservé, nouveau déclenchement et contrôle négatif ; 1008002/1008003 toujours à valider |
| Wazuh | VM `192.168.122.37`, dashboard accessible, indexer green documenté | Composants, accès et événements récents retrouvés |
| Agent Wazuh | Agent **001 — vm-filebrowser** sur la VM ; trois messages File Browser reçus dans les archives du manager | Connexion, source Docker actuelle et réception d’un nouveau message |
| Agent dans le conteneur | Installation dans le conteneur BusyBox-musl non réalisée | Conserver cette limite ; utiliser l’agent sur la VM déjà disponible |

Les adresses sont celles du laboratoire aux dernières preuves : les confirmer
avant les essais. La réception de logs File Browser dans Wazuh ne prouve pas
l’ingestion de `eve.json` ni une alerte applicative spécifique.

## 2. Reprendre les services et leurs sources

### Sur la VM File Browser

```bash
ip -br address
docker ps --filter name=filebrowser
# Adapter le nom si nécessaire ; ces champs évitent un inspect complet.
docker inspect --format '{{.State.Status}} {{.HostConfig.LogConfig.Type}} {{.LogPath}}' filebrowser
sudo /var/ossec/bin/wazuh-control status
sudo tail -n 40 /var/ossec/logs/ossec.log
sudo /var/ossec/bin/wazuh-logcollector -t
```

Vérifier que l’agent surveille le **fichier Docker actuel** dans son bloc
`localfile` (`log_format=json`). Après recréation du conteneur, son chemin
peut avoir changé. Le test du collecteur vérifie la configuration, pas la
réception côté manager. Ne pas installer un nouvel agent dans le conteneur
pour remplacer ce contrôle.

### Sur l’hôte Suricata

```bash
ip -br link
# Utiliser l’adresse VM confirmée.
ip route get 192.168.122.229
sudo systemctl status suricata --no-pager
sudo systemctl cat suricata
sudo suricata -T -v -c /etc/suricata/suricata.yaml
echo "Code du test : $?"
sudo ls -lh /var/log/suricata/eve.json
```

Comparer interface, fichier de configuration et fichiers de règles réellement
utilisés par le service à ceux du test. Attendre code 0 et aucune règle rejetée ;
le nombre attendu dépend du jeu effectivement conservé, **sept au dernier
état J8**. Ne pas remplacer la configuration validée ou relancer les services
sans avoir relevé une erreur à corriger.

### Sur la VM Wazuh

```bash
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

Identifier le conteneur manager, puis contrôler ses services avec
`docker exec <nom-manager> /var/ossec/bin/wazuh-control status`.
Ouvrir le dashboard depuis le navigateur de l’hôte, vérifier l’agent 001 et
sa dernière connexion. Une page de connexion ou un conteneur « Up » ne suffit
pas : rechercher ensuite un événement récent provenant de la source testée.

## 3. Générer quelques activités connues

Avant chaque essai, noter début/fin avec fuseau, machine émettrice, destination,
action et résultat attendu. Ne publier ni mot de passe ni jeton de session.

| Essai | Activité contrôlée | Informations attendues | Verdict à renseigner |
| --- | --- | --- | --- |
| T1 — usage normal | Ouvrir File Browser, se connecter normalement et consulter un fichier de test sans donnée sensible | Application utilisable ; GET et contexte HTTP dans EVE pour le trafic HTTP visible. Ne pas présumer que tous les accès réussis sont journalisés par l’application | Non vérifiable |
| T2 — signature positive | Envoyer le marqueur inerte de J8 à File Browser | Nouvelle alerte SID 1008001 sur 8080, URI et horodatage corrélés | Non vérifiable |
| T3 — comparaison normale | Envoyer GET `/` sans marqueur | Événement HTTP ; vérifier l’absence de SID 1008001 dans la fenêtre, sans supposer l’absence de toute autre alerte | Non vérifiable |
| T4 — collecte Wazuh | Refaire un accès non authentifié à `/api/renew` si cet endpoint retourne toujours 401 | Réponse réelle, ligne Docker correspondante, puis même message dans les archives du manager avec agent 001 | Vérifié : deux messages reçus et décodés, voir bilan J9 |

Depuis l’hôte, après confirmation de la cible :

```bash
date --iso-8601=seconds
curl --max-time 10 -sS -o /dev/null -w 'HTTP %{http_code}\n' \
  'http://192.168.122.229:8080/?ais_probe=%2e%2e'
curl --max-time 10 -sS -o /dev/null -w 'HTTP %{http_code}\n' \
  'http://192.168.122.229:8080/'
# Méthode déjà observée en J8 ; sans cookie, jeton ni corps de connexion.
curl --max-time 10 -sS -X POST -o /dev/null -w 'HTTP %{http_code}\n' \
  'http://192.168.122.229:8080/api/renew'
date --iso-8601=seconds
```

Conserver le statut réel. Si T4 ne retourne pas 401 ou n’apparaît pas dans
les logs Docker, noter l’écart et utiliser une autre activité inerte réellement
journalisée. Un 401 de renouvellement ne prouve pas un essai de mot de passe.
T2 valide un motif, pas une exploitation ; `action:allowed` ne signifie pas blocage.

## 4. Retrouver et analyser les informations

### Suricata : événements et alertes

Sur l’hôte, lire les derniers événements sélectionnés :

```bash
sudo tail -n 3000 /var/log/suricata/eve.json | jq -c '
  select(.dest_ip == "192.168.122.229" and .dest_port == 8080)
  | select(.event_type == "http" or .event_type == "alert")
  | {timestamp,event_type,flow_id,src_ip,src_port,dest_ip,dest_port,http,alert}'
```

Corréler chaque essai par heure, URI et `flow_id`. Relever SID, signature et
`action` pour T2. L’extrait des 3 000 dernières lignes est une vue pratique :
un résultat vide n’établit pas une absence dans tout le journal. Étendre la
recherche à la fenêtre complète et aux fichiers tournés si nécessaire ; garder
les objets originaux correspondants comme pièces de preuve.

### Wazuh : source locale, transmission et réception

Sur la VM File Browser, lire `docker logs --since 10m filebrowser` et retrouver
le message T4. Côté manager, lire les derniers objets du fichier
`/var/ossec/logs/archives/archives.json` **dans le conteneur manager** et filtrer
sur `agent.id == "001"`, la fenêtre et `data.log` contenant `/api/renew`.

Comparer horodatage applicatif, `data.time` Docker et `timestamp` de réception ;
J8 affichait UTC côté manager et UTC+02 côté laboratoire. Conserver agent,
source (`location`), décodeur et message sans secret.

L’archivage JSON était activé au dernier état J8 après correction de la
configuration effective. Vérifier son état actuel avant de chercher ; s’il est
désactivé, les anciens événements ou l’absence d’archives ne valident pas T4.
Documenter le choix de collecte et de rétention avec le groupe avant changement.

Chercher aussi dans les alertes/dashboard si une règle pertinente existe.
**Message reçu dans les archives ≠ alerte produite ≠ événement indexé dans
le dashboard.** Sans règle applicative validée, conclure uniquement sur la
réception. Une catégorie MITRE seule ne prouve pas une activité malveillante.

## 5. Tableau de reprise à compléter

| Source | Fonctionnelle ? | Informations disponibles | Limites connues |
| --- | --- | --- | --- |
| Suricata | Non vérifiable en J9 ; renseigner après T1–T3 | À relever : HTTP, alerte 1008001, heures, URI, IP/ports et flux | Capture limitée aux trajets visibles sur virbr0 ; contenu chiffré inaccessible ; 1008002/1008003 non validées à la fin de J8 |
| Wazuh | Non vérifiable en J9 ; renseigner après réception T4 | À relever : agent 001, source Docker, décodeur JSON, message et heures | Agent dans le conteneur absent ; alerte File Browser spécifique et ingestion Suricata non démontrées ; archives dépendantes de la configuration |
| Autre source utile : logs Docker File Browser | Non vérifiable en J9 ; renseigner après T4 | À relever : message applicatif exact, statut, heure et fichier source | Tous les accès réussis ne sont pas nécessairement journalisés ; rotation/recréation à contrôler |

Utiliser **Oui**, **Partielle**, **Non** ou **Non vérifiable**, avec la référence
du test et de sa preuve. « Oui » s’applique à la fonction testée, sans promettre
une couverture exhaustive. Un service actif sans information retrouvée conserve
un verdict partiel ou non vérifiable selon les éléments disponibles.

## 6. Diagnostic et fin de reprise

Si une information manque, suivre la chaîne : activité réellement exécutée,
trace à la source, fichier surveillé, collecteur, connexion, réception,
décodage/règle puis recherche dans la bonne vue. Noter message exact, hypothèse,
correction éventuelle et résultat du nouvel essai. Ne pas transformer une
capture absente en preuve d’un échec de transmission.

Si l’agent n’est plus fonctionnel, **ne pas consacrer toute la séance à son
installation**. Poursuivre avec Suricata et les journaux disponibles ; conserver
l’absence de collecte Wazuh comme limite. L’intégration dans le conteneur ne
doit pas être déclarée réussie par le seul fonctionnement de l’agent sur la VM.

## 📦 Preuves à conserver

- Tableau de reprise complété avec date, périmètre et verdict justifié.
- État des services, interface et validation des règles retenues.
- Activités T1–T4 : heures, résultat HTTP et informations retrouvées.
- Objets EVE et extrait Wazuh correspondants, source et identité de l’agent.
- Écarts, limites restantes et corrections réellement testées.

**État attendu :** savoir quelles sources sont utilisables pour la suite de
la séance, quelles informations elles apportent et quelles activités restent
sans visibilité. Une limite documentée vaut mieux qu’un fonctionnement supposé.

- [Règles et preuves Suricata J8](../it-8/rechercher-adapter-regles-detection.md)
- [Collecte File Browser dans Wazuh J8](../it-8/etudier-agent-wazuh-file-browser.md)
- [Plateforme Wazuh](../it-8/installer-wazuh-single-node.md)
- [Retour à l’itération 9](index.md)
- [Retour au module](../README.md)
