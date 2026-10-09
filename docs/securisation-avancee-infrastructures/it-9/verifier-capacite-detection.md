# Vérifier votre capacité de détection

**Itération 9 — 9 octobre 2026 — Travail individuel**

## 🎯 Objectif

Démontrer qu’une activité de sécurité peut être détectée, retrouvée et
expliquée avec le dispositif mis en place : scan Nmap de la VM, connexions
vers des ports fermés et requêtes HTTP vers des chemins inhabituels.

**Statut : trois comportements observés et trois signatures locales
positivement testées.** Dix règles ont été acceptées et le service relancé
à 11:46:12. Les captures de 12:07 montrent les alertes 1009001, 1009002 et
1009003 corrélées aux nouveaux essais. Le contrôle négatif GET `/` est
documenté par curl, tcpdump, l’objet HTTP EVE et la recherche vide des
nouveaux SID. Qualité du seuil en exploitation et corrélation applicative
complémentaire restent à étudier.

**Détecter un comportement ne permet pas à lui seul de déterminer son intention.**

## Résultats fournis — 9 octobre 2026, 11:34–11:36 CEST

Les cinq captures ci-dessous proviennent des essais exécutés par Olivier.
Elles documentent des résultats client, une capture réseau, des sockets
locaux et un extrait EVE ; elles ne prouvent pas de nouvelle alerte Wazuh.

### A — Scan Nmap et observation réseau

![Scan SYN de la VM et paquets observés sur virbr0](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2011-35-22.png)

Fenêtre affichée : **11:34:53–11:34:55 +02:00**. Nmap **7.98** réalise
`-sS -Pn -n -p 1-100,8080 --reason` sur `192.168.122.229`.
Les **101 ports TCP testés** donnent **99 fermés (reset)** et deux ouverts :
**22** et **8080**, avec réponse SYN-ACK. Les libellés `ssh`/`http-proxy`
sont ceux de Nmap ; sans `-sV`, ils ne prouvent pas la version ou l’identité
exacte du service. La durée de scan affichée est 0,13 s.

À gauche, `tcpdump` sur `virbr0` montre des SYN depuis
`192.168.122.1:38486` vers plusieurs ports de la VM, des RST-ACK pour des
ports refusés et un SYN-ACK sur 22. Les heures concordent avec Nmap.
**Scan visible sur le réseau**, sans nouvelle alerte de ce scan affichée.
Les alertes visibles en haut à droite sont celles des exercices précédents :
leurs horodatages 11:24 ne valident pas le scan de 11:34.

### B — Ports fermés et état local

![Ports 65001 à 65003 fermés et tentatives nc refusées](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2011-36-08.png)

Le contrôle Nmap `-sT` indique **65001, 65002 et 65003 closed**, motif
`conn-refused`. À **11:35:47 +02:00**, les trois commandes `nc` affichent
**Connection refused**. Il s’agit de refus, pas d’expirations.

![Sockets TCP en écoute sur la VM File Browser](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2011-36-19.png)

`ss -lntp` montre notamment `sshd` sur 22 et `docker-proxy` sur 8080,
ainsi que des sockets de loopback. Aucun écouteur 65001–65003 n’est affiché.
Cela complète les refus distants ; le relevé seul ne décrit pas toutes les
règles de filtrage. Les traces Docker 401 visibles au-dessus sont antérieures
et ne documentent pas les connexions à ces ports.

### C — Chemins HTTP et événements EVE

![Trois chemins inhabituels testés avec curl](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2011-36-34.png)

À **11:36:23 +02:00**, les trois GET vers `/ais-lab-inhabituel-a`,
`/ais-lab-inhabituel-b` et `/ais-lab-inhabituel-c` retournent **HTTP 200**.
Aucun 404 n’est déduit de leur caractère inhabituel.

![Requêtes HTTP et flux fermés retrouvés dans EVE](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2011-36-59.png)

Deux objets HTTP complets sont lisibles :

| Heure CEST | Requête / trajet | Référence et résultat |
| --- | --- | --- |
| 11:36:23.760153 | GET `/ais-lab-inhabituel-b`, hôte:53354 → VM:8080 | `flow_id:2136318824747664`, HTTP 200, `text/html`, longueur 5762, `alert:null` |
| 11:36:23.760672 | GET `/ais-lab-inhabituel-c`, hôte:53364 → VM:8080 | `flow_id:2161883566350554`, HTTP 200, `text/html`, longueur 5762, `alert:null` |

Le haut de l’image contient la fin d’un objet précédent ; son URI n’est pas
visible. **Le chemin a est prouvé par curl, sans objet EVE complet lisible
ici.** La longueur et le statut ne prouvent pas l’existence d’un fichier à
ces chemins : la réponse peut correspondre à une page applicative de repli,
à confirmer en examinant la réponse.

Deux objets `flow` complets concernent aussi les ports fermés :

| Port destination | Début du flux (CEST) | flow_id | État observé |
| --- | --- | --- | --- |
| 65002 | 11:35:47.465621 | `873928049703254` | Un paquet par sens, SYN vers serveur, RST/ACK vers client, `tcp.state:closed`, `flow.alerted:false` |
| 65001 | 11:35:47.477410 | `910647135855106` | Un paquet par sens, SYN vers serveur, RST/ACK vers client, `tcp.state:closed`, `flow.alerted:false` |

Ces flux sont affichés vers **11:36:47–11:36:48**, après expiration : pour
les rapprocher des commandes, lire `flow.start` à **11:35:47**, pas seulement
le `timestamp` d’émission EVE. Les valeurs `tcp_flags` sont un bilan agrégé,
pas une liste de paquets. Le flux du port 65003 n’est pas visible ici.

Un autre flux vers 22 apparaît avec un début vers 11:35:30 et un trafic plus
important. Il **n’est pas attribué au scan** de 11:34:55 : sa présence dans
la même vue ne suffit pas à établir cette relation.

### Tableau de résultats au dernier état fourni

| Activité | Source | Événement observé | Alerte ? | Règle | Interprétation |
| --- | --- | --- | --- | --- | --- |
| Scan Nmap | Nmap et tcpdump sur virbr0 | SYN vers plusieurs ports, RST/SYN-ACK ; 99 fermés et 22/8080 ouverts sur le périmètre testé | Aucune nouvelle alerte montrée ; recherche complète à faire | 1009001 proposée, non validée | Découverte de ports contrôlée ; intention connue par le contexte du test, pas par les seuls paquets |
| Connexions vers ports fermés | Nmap, nc, ss et EVE | Trois refus client ; pas d’écouteur affiché ; flux fermés EVE pour 65001/65002 | `flow.alerted:false` pour les deux flux montrés ; pas de conclusion exhaustive sur 65003 | 1009002 proposée, non validée | Refus et resets cohérents ; filtrage détaillé non fourni ; absence de session applicative réussie pour ces tentatives |
| Chemins HTTP inhabituels | curl et EVE | Trois 200 client ; URI b/c retrouvées dans HTTP | Pas de bloc alerte dans les deux objets HTTP ; objets `alert` distincts à rechercher | 1009003 proposée, non validée | Motifs inhabituels par scénario ; pas de preuve d’exploitation ou de ressource réelle |

**Limites et suite :** compléter les recherches d’alertes sur les fenêtres,
conserver les objets originaux, puis installer uniquement les règles pertinentes
si aucune règle adaptée n’alerte. Retester positifs/négatifs et joindre la
validation de configuration. Aucune corrélation Docker/Wazuh des chemins C
n’est fournie ; les événements de l’activité précédente ne peuvent pas la
remplacer. Aucun taux de faux positifs, couverture complète des ports ou
blocage n’est établi.

### Compléments — nouvelles captures de 11:41 à 11:43

![Nouvel essai de scan et échanges TCP](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2011-41-33.png)

**11:41:33 :** Nmap retrouve 99 ports fermés et 22/8080 ouverts ; à droite,
SYN et RST sont visibles vers plusieurs ports autour de 11:41:26. Des erreurs
Bash apparaissent ensuite (`commande introuvable`, syntaxe près de `(`),
compatibles avec des lignes de résultat exécutées comme commandes. Elles
ne démontrent pas une panne du capteur ou de la VM ; leur origine précise
n’est pas établie par l’image seule.

![Scan correctement exécuté à 11:41:48](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2011-41-51.png)

**11:41:48 +02:00 :** nouvelle exécution lisible de
`sudo nmap -sS -Pn -n -p 1-100,8080 --reason 192.168.122.229`.
Résultat : 99 fermés, 22/8080 ouverts, durée 0,11 s. `tcpdump` montre les
SYN depuis **hôte:39301** et les réponses de la VM. Des échanges VM →
Wazuh:1514 sont aussi visibles à 11:41:49 ; ils prouvent du trafic vers le
manager, pas la collecte du scan ou une alerte Wazuh liée à celui-ci.

![Relevé des sockets de la VM](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2011-42-08.png)

**11:42:08 :** le relevé confirme les écouteurs 22/8080 et les sockets de
loopback déjà documentés ; aucun écouteur 65001–65003 n’est affiché.

![Nouveau contrôle des trois ports et refus nc](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2011-42-33.png)

**11:42:16 +02:00 :** Nmap connect indique les trois ports fermés,
`conn-refused`, puis `nc` produit trois `Connection refused`. Le relevé
`ss` de la VM et les résultats client concordent.

![Flux EVE du scan et des trois ports fermés](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2011-43-48.png)

**Corrélation du scan avec Suricata désormais documentée :** plusieurs objets
`flow` partent de **192.168.122.1:39301**, commencent à **11:41:48.221…**
et ciblent des ports du scan (notamment 66, 98, 34, 1, 2, 45, 37, 42, 59,
10, 55 et 78). Ils montrent un paquet par sens, SYN puis RST/ACK,
`tcp.state:closed` et **`flow.alerted:false`**. Ils sont émis vers
11:42:53, après expiration. Heure de début et port source permettent de
les rapprocher du scan Nmap/tcpdump de 11:41:48.

**Les trois ports fermés sont maintenant visibles dans EVE :**

| Port | Débuts de flux visibles à 11:42:16 CEST | Information disponible |
| --- | --- | --- |
| 65001 | .937315 et .943952 | Deux flux fermés ; un paquet par sens, SYN/RST-ACK, `alerted:false` |
| 65002 | .945419 et .937322 | Deux flux fermés ; mêmes indicateurs |
| 65003 | .937297 et .947047 | Deux flux fermés ; mêmes indicateurs |

Les deux flux par port sont cohérents avec le contrôle Nmap `-sT` puis le
contrôle `nc`, exécutés dans la même seconde. La capture seule ne permet pas
d’attribuer chaque flux à un outil avec certitude ; il faut une fenêtre
séparée ou les ports sources relevés au moment de chaque commande pour
lever cette ambiguïté. Les événements sont publiés à 11:43:17–11:43:20 :
ce délai de sortie EVE ne doit pas être confondu avec l’heure de tentative.

Un flux 22 plus volumineux, débutant à 11:41:55, apparaît aussi : il n’est
pas attribué au scan. La proximité dans la vue ne suffit pas à une corrélation.

### Bilan actualisé et étape restante

- **Scan Nmap :** résultat client, paquets et flux EVE concordent pour le nouveau scan. Les flux fermés affichés n’ont pas d’alerte associée (`alerted:false`) ; cela ne décrit pas tous les flux du scan ni une recherche exhaustive des alertes.
- **Ports fermés :** refus des trois ports et flux EVE 65001/65002/65003 documentés ; absence d’alerte associée aux six flux affichés.
- **Chemins HTTP :** résultats de 11:36 conservés ; aucun nouvel essai HTTP visible dans ce complément.
- **Règles :** aucune capture de création du fichier, de chargement des signatures 1009001–1009003 ou de leur déclenchement. Elles restent proposées, non validées.

La visibilité est donc documentée pour les trois comportements. Pour achever
la vérification de capacité d’alerte, suivre la section d’adaptation ci-dessous,
valider la configuration puis refaire les scénarios concernés et les contrôles
négatifs. Ne pas répéter les recherches de visibilité déjà établies.

### Configuration acceptée et redémarrage — capture jointe à 11:46

La capture fournie directement dans la conversation montre l’ouverture de
`/etc/suricata/rules/ais-it9-capacite.rules` et du YAML avec `sudoedit`, puis
le test Suricata et le redémarrage du service. Cette image n’est pas encore
présente dans le dossier des captures du dépôt ; les résultats sont retranscrits
ici sans inventer de lien vers un fichier absent.

| Contrôle | Résultat visible |
| --- | --- |
| Version | Suricata 8.0.3 RELEASE |
| Configuration | `/etc/suricata/suricata.yaml` |
| Chargement | **3 fichiers, 10 règles chargées, 0 échouée, 0 ignorée** |
| Test | Configuration acceptée, **code de retour 0** |
| Redémarrage | **active (running)** depuis **2026-10-09 11:46:12 CEST** |

**Résultat : configuration syntaxiquement acceptée et service relancé.**
Le contenu du fichier de règles et les SID ne sont pas affichés : les dix
signatures chargées ne prouvent pas à elles seules les conditions exactes de
1009001–1009003. Leur déclenchement reste à vérifier avec les essais ci-dessous.
Le tableau de résultats précédent décrit l’état **avant adaptation** ; ses absences d’alerte
ne sont pas un résultat des nouvelles règles.

### Essais après redémarrage — commandes prêtes à utiliser

Sur l’hôte, commencer dans un terminal dédié par le suivi des nouveaux SID :

```bash
sudo tail -n 0 -F /var/log/suricata/eve.json | jq --unbuffered -c '
  select(.event_type == "alert")
  | select(.alert.signature_id == 1009001
        or .alert.signature_id == 1009002
        or .alert.signature_id == 1009003)
  | {timestamp,flow_id,src_ip,src_port,dest_ip,dest_port,http,alert}'
```

Dans un autre terminal **de l’hôte**, lancer les positifs séparés :

```bash
date --iso-8601=seconds
sudo nmap -sS -Pn -n -p 1-100,8080 --reason 192.168.122.229
sleep 15
date --iso-8601=seconds
for port in 65001 65002 65003; do
  nc -vz -w 2 192.168.122.229 "$port"
done
sleep 15
date --iso-8601=seconds
for chemin in /ais-lab-inhabituel-a /ais-lab-inhabituel-b /ais-lab-inhabituel-c; do
  curl --max-time 10 -sS -o /dev/null -w 'HTTP %{http_code}\n' \
    "http://192.168.122.229:8080$chemin"
done
date --iso-8601=seconds
```

Attendre 1009001 pour le volume SYN, 1009002 pour les RST des trois ports
et 1009003 pour les chemins choisis **si les règles installées correspondent
aux propositions**. Le suivi ne prouve pas une absence exhaustive : en cas
vide, rechercher la fenêtre complète dans le fichier et vérifier les SID
réellement chargés avant toute modification supplémentaire.

Pour les contrôles négatifs, après au moins 15 secondes, réaliser une seule
connexion normale vers 8080 puis GET `/`. Rechercher l’absence des **nouveaux
SID** sur cette fenêtre ; ne pas exiger l’absence de toutes les anciennes
règles. Conserver commandes, horaires et objets EVE de ces essais.

### Tests positifs après adaptation — captures de 12:07

![Alertes des trois signatures locales pendant les nouveaux essais](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2012-07-48.png)

![Commandes et résultats client des trois scénarios](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2012-07-56.png)

Les commandes sont exécutées depuis l’hôte, avec quinze secondes entre les
scénarios. Nmap retrouve **99 ports fermés, 22 et 8080 ouverts**, durée
0,09 s. Les trois `nc` donnent **Connection refused**, puis les trois GET
retournent **200**. La capture d’alertes donne les mêmes scénarios avec leurs
nouveaux SID, révision 1, catégorie `Misc activity`, sévérité 3 et
**`action:allowed`**.

| Activité | Source | Événement observé | Alerte ? | Règle | Interprétation |
| --- | --- | --- | --- | --- | --- |
| Scan Nmap | Nmap et Suricata EVE | Série de SYN depuis hôte:60668 vers VM, alertes autour de **12:07:05.274–.274348 CEST** | **Oui**, plusieurs objets visibles | **1009001 — AIS LAB volume SYN vers VM** | Volume SYN détecté pendant le scan contrôlé ; le SID ne prouve pas à lui seul Nmap, des ports distincts ou une intention hostile |
| Connexions vers ports fermés | nc et Suricata EVE | Trois refus et réponses VM:65001/65003/65002 → hôte | **Oui**, trois objets visibles à **12:07:20** | **1009002 — AIS LAB RST depuis ports de test VM** | RST corrélés aux tentatives sur les ports déjà contrôlés fermés ; le motif reste compatible avec un rejet réseau dans un autre contexte |
| Chemins HTTP inhabituels | curl et Suricata EVE | GET des trois chemins choisis, réponse 200, contenu text/html | **Oui**, un objet par chemin à **12:07:35** | **1009003 — AIS LAB chemin HTTP inhabituel de test** | Préfixe de laboratoire détecté ; pas de preuve d’exploitation ni de détection générale des chemins inhabituels |

### Références précises pour les refus et les chemins

| Heure EVE CEST | Source → destination | Ressource / flow_id |
| --- | --- | --- |
| 12:07:20.323566 | VM:65001 → hôte:41628 | RST ; `263317513634689` |
| 12:07:20.326387 | VM:65003 → hôte:57070 | RST ; `275552850949435` |
| 12:07:20.325062 | VM:65002 → hôte:34714 | RST ; `269893905817929` |
| 12:07:35.335489 | Hôte:50774 → VM:8080 | `/ais-lab-inhabituel-a` ; `1999140498569494` |
| 12:07:35.342608 | Hôte:50780 → VM:8080 | `/ais-lab-inhabituel-b` ; `2030135812092854` |
| 12:07:35.348978 | Hôte:50794 → VM:8080 | `/ais-lab-inhabituel-c` ; `205830145529477` |

Les trois objets HTTP montrent curl/8.18.0, méthode GET, statut 200 et
longueur 3854. Cette longueur ne prouve pas l’identité ou le contenu de la
ressource ; le corps n’est pas affiché. Les RST et alertes de volume SYN
n’ont pas de bloc HTTP (`http:null`), ce qui est cohérent avec ces scénarios TCP.

**Résultat : capacité d’alerte démontrée pour les trois scénarios positifs
retenus.** Les preuves initiales de visibilité sans alerte sont conservées
comme état avant adaptation ; elles ne décrivent plus les résultats des
nouveaux essais. Le contenu complet des règles n’est pas affiché, mais SID,
révision, signature et déclenchement sont maintenant observés.

**Limites restantes :** aucune capture de contrôle négatif après adaptation,
pas de mesure des faux positifs ou d’un scan lent, pas d’alerte Wazuh liée à
ces trois essais, pas d’objet JSON brut exporté ici. La multiplication des
alertes 1009001 montre aussi un bruit potentiel à régler selon les usages ;
un test positif seul ne valide pas la qualité du seuil en exploitation.

Pour compléter sans refaire les positifs, attendre quinze secondes après
la dernière activité et lancer depuis l’hôte un seul GET normal :

```bash
date --iso-8601=seconds
curl --max-time 10 -sS -o /dev/null -w 'HTTP %{http_code}\n' \
  'http://192.168.122.229:8080/'
date --iso-8601=seconds
```

Rechercher les nouveaux SID sur cette fenêtre dans EVE, en gardant le suivi
actif. Ce contrôle est attendu sans 1009001 (volume sous seuil), sans
1009002 (port 8080 hors sélection) et sans 1009003 (préfixe absent), si les
règles correspondent aux propositions. Il ne prouve pas l’absence de tous
les faux positifs ; d’autres anciennes règles peuvent rester actives.

### Contrôle normal — sortie fournie à 12:12:35

Le GET `/` depuis l’hôte retourne **HTTP 200**. L’extrait `tcpdump` fourni
montre à **12:12:35.442530–.443704** une connexion
`192.168.122.1:42646` → `192.168.122.229:8080` : SYN, SYN-ACK, ACK,
GET `/`, réponse **HTTP/1.1 200 OK**, puis FIN/ACK dans les deux sens.
Aucun RST n’est visible pour cet échange. Le trafic normal est donc
observé au point de capture ; cette sortie ne recherche pas les alertes EVE.

**Contrôle négatif : activité normale exécutée, verdict d’absence des SID
1009001–1009003 encore Non vérifiable.** Rechercher le résultat dans EVE
sur cette fenêtre, sans refaire la requête :

```bash
sudo jq -c '
  select(.timestamp >= "2026-10-09T12:12:30"
     and .timestamp < "2026-10-09T12:12:41")
  | select(.event_type == "alert")
  | select(.alert.signature_id == 1009001
        or .alert.signature_id == 1009002
        or .alert.signature_id == 1009003)
  | {timestamp,flow_id,src_ip,src_port,dest_ip,dest_port,http,alert}
' /var/log/suricata/eve.json
echo "Code de lecture : $?"
```

Avec les horodatages EVE CEST déjà observés, un résultat vide et code 0
établit l’absence de ces alertes **dans ce fichier et cette fenêtre**.
Vérifier que la fenêtre n’a pas été déplacée dans un fichier tourné et que
la capture EVE du GET existe avant de conclure. Une absence d’alerte sans
événement HTTP correspondant ne valide pas la chaîne de capture.

L’extrait contient aussi des échanges VM → manager Wazuh:1514 à 12:12:41
et 12:13:01, et un GET sortant VM → `91.189.91.96:80` à 12:12:46,
avec réponse **204** et RST ultérieurs. Ce sont des flux distincts du GET
File Browser : ne pas leur attribuer sa réponse ou son intention. Le trafic
1514 ne prouve pas la réception d’un message applicatif précis dans Wazuh ;
le but du GET externe n’est pas établi par cet extrait.

### Preuves du contrôle négatif — quatre captures ajoutées

![GET normal visible dans tcpdump](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2012-12-42.png)

![Réponse curl HTTP 200](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2012-12-46.png)

![Recherche des nouveaux SID vide avec code de lecture 0](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2012-14-04.png)

La recherche dans `/var/log/suricata/eve.json` sur **12:12:30 inclus à
12:12:41 exclu**, pour les SID **1009001, 1009002 et 1009003**, ne retourne
aucun objet et affiche **Code de lecture : 0**. Cela confirme l’absence de
ces trois alertes dans la fenêtre du fichier lu. Le GET `/` et sa réponse
200 sont prouvés par curl et tcpdump ; **l’objet HTTP EVE de ce GET n’est
pas montré**. La vérification complète de la journalisation EVE du contrôle
normal reste donc à terminer, sans refaire l’activité.

Sur l’hôte, retrouver l’objet HTTP à partir du trajet capturé :

```bash
sudo jq -c '
  select(.timestamp >= "2026-10-09T12:12:30"
     and .timestamp < "2026-10-09T12:12:41")
  | select(.event_type == "http")
  | select(.src_ip == "192.168.122.1" and .src_port == 42646
       and .dest_ip == "192.168.122.229" and .dest_port == 8080)
  | {timestamp,flow_id,src_ip,src_port,dest_ip,dest_port,http}
' /var/log/suricata/eve.json
```

![Trafic Wazuh et sortie HTTP distincts du contrôle File Browser](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2012-14-15.png)

La quatrième capture conserve les autres flux déjà décrits : échanges avec
Wazuh:1514 et GET externe avec réponse 204. Ils ne sont pas utilisés pour
valider la journalisation du GET File Browser.

**Bilan du contrôle négatif :** réponse normale et absence des nouveaux SID
sur la fenêtre documentées ; objet HTTP EVE correspondant à fournir. Ce
contrôle ponctuel ne mesure pas le taux de faux positifs en exploitation.

### Contrôle négatif complété — deux captures à 12:34

![Objet HTTP EVE du GET normal de 12:12:35](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2012-34-46.png)

La recherche ciblée retrouve l’objet HTTP attendu :

| Champ EVE | Valeur visible |
| --- | --- |
| timestamp | `2026-10-09T12:12:35.443529+0200` |
| flow_id | `1056229479386453` |
| Origine | `192.168.122.1:42646` |
| Destination | `192.168.122.229:8080` |
| Requête | GET `/`, HTTP/1.1, curl/8.18.0 |
| Réponse | 200, `text/html`, longueur affichée 5762 |

**Contrôle négatif validé pour ce scénario et cette fenêtre :** activité
normale exécutée, trafic observé sur `virbr0`, événement HTTP journalisé par
Suricata, et aucune alerte **1009001–1009003** retrouvée dans le fichier EVE
sur **12:12:30–12:12:41**, avec code de lecture 0. L’objet EVE correspond
au port source et à l’heure de la capture TCP ; les étapes précédemment
marquées à compléter sont désormais documentées. Cela ne prouve pas
l’absence de toutes les alertes ni de faux positifs sur d’autres usages.

![Nouvel échange HTTP inhabituel et trafic vers Wazuh à 12:34](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2012-34-37.png)

L’autre capture montre **à 12:34:22** un GET
`/ais-lab-inhabituel-c`, hôte:33024 → VM:8080, réponse 200 puis fermeture
FIN/ACK. Elle complète la visibilité de ce chemin ; aucune nouvelle alerte
1009003 de cette fenêtre n’est affichée dans cette image. Les échanges vers
Wazuh:1514 à 12:34:31 restent distincts et ne prouvent pas la réception du
message de cette requête. Cette activité ne remplace pas le GET normal de
12:12:35 pour le contrôle négatif.

### Conclusion sur la capacité vérifiée

Les trois comportements sont observés et les signatures 1009001, 1009002
et 1009003 ont déclenché pendant les tests positifs de 12:07. Le GET normal
isolé a été observé et journalisé sans ces trois alertes dans la fenêtre
recherchée. **La capacité de détection est démontrée pour ces scénarios
précis**, en mode IDS sans blocage. Intention hostile, couverture générale,
qualité du seuil sur une longue période et détection Wazuh de ces scénarios
ne sont pas établies par ces preuves.

La procédure suivante reste la référence pour ces compléments ; ne pas
refaire les phases déjà prouvées sans besoin de nouveau test.

## 1. Préparer les observations

Reprendre la [vue exploitable des événements](construire-vue-exploitable-evenements.md).
Suricata est sur l’hôte, interface `virbr0` ; File Browser est sur la VM
`192.168.122.229:8080` aux dernières preuves. Wazuh reçoit ses logs Docker
via l’agent VM **001 — vm-filebrowser**. L’ingestion EVE dans Wazuh et une
alerte Wazuh spécifique à File Browser ne sont pas démontrées.

Effectuer les essais **depuis l’hôte vers sa propre VM**, après confirmation
de l’adresse. Ne pas scanner les autres apprenants. Séparer les trois fenêtres,
noter date/fuseau, commande et résultat ; attendre au moins 15 secondes entre
les scénarios pour distinguer les seuils des règles proposées.

Sur l’hôte, dans un second terminal, avant les essais :

```bash
# Observation de tous les ports TCP de la VM, pas uniquement 8080.
sudo tcpdump -ni virbr0 'host 192.168.122.229 and tcp'
```

Une capture de paquets peut prouver des SYN/RST qu’EVE ne détaille pas.
EVE `flow` peut être écrit à la clôture ou après expiration : attendre avant
une recherche. `tcpdump` et Suricata observent le réseau au même endroit ;
leur concordance n’ajoute pas à elle seule une preuve applicative.

## 2. Générer les trois comportements

### A — Scan Nmap limité de la VM

Depuis l’hôte :

```bash
date --iso-8601=seconds
# Scan SYN TCP limité, sans détection de version ni scripts NSE.
sudo nmap -sS -Pn -n -p 1-100,8080 --reason 192.168.122.229
date --iso-8601=seconds
```

Conserver les ports et états réellement retournés : `open`, `closed` ou
`filtered`. Ce scan n’est pas un inventaire exhaustif. Comparer ports sondés,
SYN envoyés et réponses avec le trafic observé. Un SYN suivi de RST est
compatible avec un port fermé ; une absence de réponse ne suffit pas à
conclure « fermé ». Le scan SYN ne réalise pas une session applicative normale.

**Intérêt :** une série de sondes peut signaler une découverte de services.
**Qualification :** source, cible, ports distincts, durée, réponses et contexte.
**Compléments :** autorisation du test, inventaire des services et éventuels
journaux de pare-feu. Les traces réseau seules n’identifient pas avec certitude
le logiciel Nmap ou l’intention de la personne.

### B — Connexions vers des ports fermés

Sur la **VM**, relever les sockets en écoute :

```bash
sudo ss -lntp
```

Choisir trois ports TCP sans service attendu et vérifier leur état depuis
l’hôte ; **65001–65003 sont des exemples à confirmer**, pas des ports fermés
prouvés à l’avance. L’absence dans `ss` doit être rapprochée des publications
Docker et du filtrage : elle ne suffit pas à déterminer l’état distant.

```bash
# Sur l’hôte : confirmer les états avant le scénario distinct.
nmap -sT -Pn -n -p 65001-65003 --reason 192.168.122.229
# Après séparation de la fenêtre, si ces ports sont bien closed :
date --iso-8601=seconds
for port in 65001 65002 65003; do
  nc -vz -w 2 192.168.122.229 "$port"
done
date --iso-8601=seconds
```

Relever succès, refus ou expiration. Ne pas transformer une expiration en
refus. Si les ports sont ouverts ou filtrés, en choisir d’autres ou conserver
le résultat avec sa limite. Adapter également la règle B aux ports retenus.

**Intérêt :** recherche d’un service absent, erreur de configuration ou
activité de découverte. **Compléments :** service attendu, origine du client,
pare-feu et historique des changements. Les logs File Browser n’ont pas de
raison de contenir une connexion rejetée sur un autre port.

### C — Chemins HTTP inhabituels

Depuis l’hôte, envoyer quelques GET inertes, sans jeton ni contenu sensible :

```bash
FB_BASE='http://192.168.122.229:8080'
date --iso-8601=seconds
for chemin in /ais-lab-inhabituel-a /ais-lab-inhabituel-b /ais-lab-inhabituel-c; do
  printf '%s : ' "$chemin"
  curl --max-time 10 -sS -o /dev/null -w 'HTTP %{http_code}\n' "$FB_BASE$chemin"
done
date --iso-8601=seconds
```

Ces chemins sont inhabituels **par choix de scénario** ; ils ne prouvent pas
une reconnaissance hostile. File Browser peut retourner 200 via sa page
applicative pour un chemin inexistant. Le statut seul ne prouve donc ni
l’existence d’un fichier ni sa lecture. Retrouver URI, méthode, statut et
contexte. Une réponse 404/401 n’est pas présumée.

**Intérêt :** des requêtes hors usages connus peuvent justifier une analyse.
**Compléments :** routes applicatives, référence des usages normaux, compte,
réponse effective et logs applicatifs. HTTPS masquerait les URI au capteur
sans déchiffrement ; l’IP seule ne fournit pas l’identité utilisateur.

## 3. Retrouver événements et alertes avant adaptation

Sur l’hôte, rechercher dans les deux directions et sur **tous les ports** :

```bash
sudo tail -n 10000 /var/log/suricata/eve.json | jq -c '
  select(.src_ip == "192.168.122.229" or .dest_ip == "192.168.122.229")
  | select(.event_type == "alert" or .event_type == "flow"
      or .event_type == "http")
  | {timestamp,event_type,flow_id,src_ip,src_port,dest_ip,dest_port,
     proto,app_proto,http,alert,flow,tcp}'
```

Sélectionner les fenêtres A/B/C puis rapprocher de `tcpdump` et du résultat
client. Les 10 000 dernières lignes ne sont pas exhaustives : étendre la
recherche au fichier complet ou aux journaux tournés si nécessaire.
Conserver les objets originaux pertinents, pas seulement cette projection.
Une absence d’alerte n’est prouvée que pour un jeu de règles et une fenêtre
recherchée explicitement ; un filtre centré sur 8080 manquerait A/B.

Sur la VM, rechercher les lignes applicatives de C avec
`sudo docker logs --since '<début ISO de C>' filebrowser` (remplacer le début).
Si elles existent, chercher les mêmes messages dans les archives du manager
avec agent 001, fenêtre, `location` et `data.log`. Ne pas chercher uniquement
`/api/renew` : ce filtre des activités précédentes ne couvre pas les chemins C.

Pour A/B, examiner les logs système/pare-feu **s’ils sont configurés et
produisent une trace**. Agent actif et archives présentes ne garantissent pas
une journalisation des paquets. Écrire « non disponible » si aucune source
hôte correspondante n’est disponible, sans installer une collecte pour faire
semblant de l’avoir déjà vérifiée.

## 4. Si visible sans alerte : rechercher ou adapter une règle

Les sept règles précédentes visent des motifs HTTP, des GET `/` répétés
et le statut 401. Elles ne constituent pas une détection dédiée des trois
comportements nouveaux. Examiner d’abord toute alerte existante et sa
condition réelle ; conserver SID, révision, source et décision.

Les trois signatures suivantes sont des **propositions locales pédagogiques
non testées**, à utiliser seulement après observation sans alerte adaptée.
Vérifier l’absence de collision des SID et adapter IP/ports. Elles utilisent
la syntaxe documentée pour Suricata 8.0.3, mais le test local reste obligatoire.

```suricata
alert tcp any any -> 192.168.122.229 any (msg:"AIS LAB volume SYN vers VM"; tcp.flags:S,CE; flow:stateless; threshold:type threshold, track by_src, count 10, seconds 10; classtype:misc-activity; sid:1009001; rev:1;)
alert tcp 192.168.122.229 [65001:65003] -> any any (msg:"AIS LAB RST depuis ports de test VM"; tcp.flags:R+; flow:stateless; classtype:misc-activity; sid:1009002; rev:1;)
alert http any any -> 192.168.122.229 8080 (msg:"AIS LAB chemin HTTP inhabituel de test"; flow:established,to_server; http.uri; content:"/ais-lab-inhabituel-"; startswith; classtype:misc-activity; sid:1009003; rev:1;)
```

| SID proposé | Ce qu’il reconnaît | Ce qu’il ne prouve pas / réglage nécessaire |
| --- | --- | --- |
| 1009001 | Dix correspondances SYN par source en dix secondes vers la VM | Ne compte pas dix ports distincts ; retransmissions ou connexions normales rapides peuvent déclencher. Ni Nmap identifié ni scan lent couvert |
| 1009002 | RST émis par la VM depuis les trois ports choisis | Ni port fermé certain ni cause du refus établie : pare-feu REJECT ou autre reset possible. Corréler SYN initial, résultat client et état local ; peut aussi déclencher pendant un scan |
| 1009003 | Préfixe URI normalisée choisi pour le laboratoire | Règle de scénario, pas détecteur général de tout chemin inhabituel ; statut et intention non déterminés par le motif |

### Installer sans écraser le jeu validé

1. Sauvegarder le YAML et les fichiers de règles dans une copie datée distincte.
2. Créer `/etc/suricata/rules/ais-it9-capacite.rules` avec les règles retenues.
3. Ajouter ce chemin dans le bloc `rule-files` existant, sans retirer J8.
4. Tester la configuration **avant** redémarrage :

```bash
sudo suricata -T -v -c /etc/suricata/suricata.yaml
echo "Code du test : $?"
# Seulement après code 0 et aucune règle rejetée :
sudo systemctl restart suricata
sudo systemctl status suricata --no-pager
```

Si les sept précédentes et les trois nouvelles sont conservées, dix signatures
sont attendues ; adapter au jeu retenu. Ne pas annoncer dix chargées sans
sortie correspondante. En cas d’échec, corriger ou restaurer la copie avant
reprise, puis retester.

### Vérifier déclenchement et contrôle négatif

Refaire uniquement les scénarios concernés dans de nouvelles fenêtres :

- A : scan borné pour le positif ; une connexion isolée après expiration de la fenêtre pour le négatif de 1009001. Documenter les correspondances réellement observées et les ports distincts séparément.
- B : vérifier un refus sur les ports choisis et la réponse RST ; comparer avec l’accès normal à 8080, hors ports ciblés. Pas de RST visible signifie que la condition proposée n’est pas validée.
- C : les trois chemins choisis pour le positif ; GET `/` pour le négatif de 1009003. D’autres règles, par exemple 1008002, peuvent néanmoins alerter sur la répétition.

Retrouver SID, heure, source/destination et `flow_id`. Ajuster un seuil à partir
des observations, sans présenter une règle qui compte des paquets comme une
règle comptant des ports ou des personnes. Aucun essai local n’est réalisé
par le mémo.

## 5. Documenter et expliquer

| Activité | Source | Événement observé | Alerte ? | Règle | Interprétation |
| --- | --- | --- | --- | --- | --- |
| Scan Nmap | À relever | Non vérifiable | À rechercher avant/après adaptation | Existante ou 1009001 proposée | À justifier avec ports, réponses, fréquence et contexte ; pas d’intention déduite |
| Connexions vers des ports fermés | À relever | Non vérifiable | À rechercher avant/après adaptation | Existante ou 1009002 proposée | À justifier avec refus/RST et état des ports ; une expiration n’est pas un refus |
| Chemins HTTP inhabituels | À relever | Non vérifiable | À rechercher avant/après adaptation | Existante ou 1009003 proposée | À justifier avec URI/statut et usages ; un 200 n’établit pas l’existence d’un fichier |

Pour chaque ligne, compléter : intérêt pour la surveillance, informations de
qualification, compléments nécessaires et limites. Distinguer **observé sans
alerte**, **observé avec alerte**, **non retrouvé** et **non vérifiable**.

Lorsque plusieurs sources voient la même activité, rapprocher heure/fuseau,
IP/ports, URI/statut et message ; conserver leurs références. Wazuh peut
copier un message Docker : ce n’est pas une deuxième activité indépendante.
Le `flow_id` Suricata n’est pas un identifiant commun avec Wazuh.

## 📦 Preuves et conclusion attendues

- Commandes, fenêtres des trois scénarios et résultats réellement obtenus.
- Traces réseau/applicatives et objets EVE/Wazuh utiles, sans secrets.
- Tableau complété ; état avant/après règle, SID/version et contrôle de configuration.
- Tests positifs/négatifs, faux positifs possibles et angles morts explicités.

Conclure sur **les comportements effectivement observables et détectables**,
la source qui apporte chaque information et ce qui reste inconnu. Un scan,
un port refusé ou un chemin inhabituel ne constitue pas automatiquement une
attaque. Aucun blocage n’est acquis par une règle IDS `alert`.

## Références techniques

- [Nmap — techniques de scan et interprétation des réponses](https://nmap.org/book/man-port-scanning-techniques.html).
- [Suricata 8.0.3 — drapeaux TCP](https://docs.suricata.io/en/suricata-8.0.3/rules/header-keywords.html#tcp-flags).
- [Suricata 8.0.3 — seuils de déclenchement](https://docs.suricata.io/en/suricata-8.0.3/rules/thresholding.html).
- [Suricata 8.0.3 — buffers HTTP](https://docs.suricata.io/en/suricata-8.0.3/rules/http-keywords.html).

- [Vue exploitable des événements](construire-vue-exploitable-evenements.md)
- [Reprise du dispositif](reprendre-dispositif-detection.md)
- [Retour à l’itération 9](index.md)
- [Retour au module](../README.md)
