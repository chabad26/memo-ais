# Installer et tester des règles Suricata

**Itération 7 — 7 octobre 2026 — Travail individuel — 1 h 15**

**Étape précédente dans le parcours :** [Comprendre les événements produits](comprendre-evenements-produits.md).
Le point d’observation est décrit dans la [première feuille](identifier-point-observation.md).

## 🎯 Objectif et prérequis

Lire, sélectionner, installer et tester **au maximum dix signatures** adaptées
au trafic observable. **Procédure et suivi de réalisation : voir le bilan daté ci-dessous.**
Suricata doit être installé directement sur l’hôte et disposer d’une configuration
de capture fonctionnelle ; le suivi ci-dessous distingue installation, démarrage
et visibilité effective.
Relever OS hôte, version (`suricata -V`), interface et configuration du service
(`systemctl cat suricata`). Adapter chemins et commandes à la distribution.

## Suivi de réalisation — 7 octobre 2026

| Étape | État et preuve disponible |
| --- | --- |
| Dépôt et sélection | Sorties fournies : commit `23bfba7e688fdf5fadd8e378f070dae843e14263`, quatre signatures extraites : 50500003, 50500004, 50500006 et 50100004 |
| Installation | Oubli initial signalé puis installation de Suricata ; version **8.0.3 RELEASE** observée dans les sorties |
| Chargement des règles | Premier YAML référençant uniquement le fichier standard absent `suricata.rules` : test en échec, code 1. Remplacement par le chemin absolu du fichier local ; test fourni : **4 chargées, 0 échouées, 0 ignorées, code 0** |
| Démarrage initial | Échec malgré règles valides : journal `af-packet: eth0: failed to find interface: No such device` ; service arrêté pour interrompre les tentatives automatiques |
| Choix d’interface | `ip route get` vers la VM indique `dev virbr0` ; relevé suivant : bridge UP et interface VM présente. Le trajet hôte → VM utilise ce bridge |
| Correction et reprise | Remplacement de `eth0` par **`virbr0`** dans `af-packet`, puis validation, remise à zéro de l’état d’échec et démarrage. Capture de 10 h 18 : **4 règles chargées, aucune échouée/ignorée, code 0 et service active (running)** depuis 10 h 18 min 27 s |
| Visibilité et alertes | Capture de 10 h 30 : échanges TCP sur 18080 et **quatre alertes EVE**, SID 50500003, 50500004, 50500006 et 50100004 ; validation limitée au serveur HTTP temporaire de la VM |

### Configuration retenue

```yaml
rule-files:
  - /etc/suricata/rules/ais-it8.rules
```

Dans le bloc **existant** `af-packet`, seule l’interface a été remplacée ;
conserver les autres paramètres :

```yaml
af-packet:
  - interface: virbr0
    # Autres paramètres existants conservés.
```

Commandes de validation et de reprise : le test et le service actif sont
désormais documentés par la capture de 10 h 18 :

```bash
sudo suricata -T -v -c /etc/suricata/suricata.yaml
echo "Code de retour : $?"
# Si code 0 et quatre règles chargées sans échec :
sudo systemctl reset-failed suricata
sudo systemctl start suricata
sudo systemctl status suricata --no-pager
```

**Sauvegarde :** le fichier `.avant-it8` a été recopié après modification du
YAML ; il ne garantit plus la configuration initiale. Pour une prochaine
modification, conserver une copie datée distincte de l’état actuel validé.

**Bilan :** capture réseau et quatre alertes corrélées aux essais sur 18080
sont documentées ci-dessous. La visibilité complète de tous les échanges et
la détection sur File Browser/8080 ne sont pas démontrées ; son filtrage reste distinct.

### Captures de réalisation

Les fichiers fournis sont conservés dans le dossier d’images `it-7` choisi
lors du dépôt ; ils illustrent ici l’activité Suricata classée en itération 8.
Les adresses visibles correspondent au laboratoire.

![Sélection des quatre signatures](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2009-58-12.png)

**09:58:12 :** Clonage du dépôt, commit et extraction des quatre SID ; la sélection est visible.

![Validation de configuration et démarrage Suricata](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2010-18-37.png)

**10:18:37 :** Suricata 8.0.3 : quatre règles chargées, zéro échec/ignorée, code 0 ; service actif après reprise à 10 h 18 min 27 s.

![Premiers essais HTTP sur le serveur temporaire](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2010-25-13.png)

**10:25:13 :** La VM reçoit les quatre GET sur 18080 et répond 404. L’erreur initiale de résolution du bind est suivie d’un démarrage avec l’IP réelle. Le tcpdump filtre encore 8080 : cette capture ne prouve pas la capture des tests sur 18080.

![Trafic TCP et quatre alertes Suricata corrélées](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2010-30-55.png)

**10:30:55 :** Les échanges entre hôte et VM sur 18080 sont visibles en haut ; les quatre SID apparaissent en bas dans EVE avec les mêmes adresses et le port destination 18080.

### Analyse des alertes observées

| SID | Horodatage EVE du 7 octobre 2026 (+02:00) | Motif et résultat |
| --- | --- | --- |
| 50500003 | 10:30:38.887961 | `%2e%2e` dans l’URI brute ; alerte observée |
| 50500004 | 10:30:38.892375 | `..%2f` dans l’URI brute ; alerte observée |
| 50500006 | 10:30:38.898569 | `%252e%252e` dans l’URI brute ; alerte observée |
| 50100004 | 10:30:38.904860 | Ouverture de balise script dans l’URI normalisée ; alerte observée |

Chaque événement montre une source hôte `192.168.122.1`, une destination VM
`192.168.122.229:18080` et un `flow_id` distinct. Le champ `action: allowed`
indique ici que le trafic n’a pas été bloqué ; il ne représente pas une
approbation de sécurité. Les réponses 404 n’empêchent pas la détection des
motifs dans les requêtes.

**Conclusion vérifiée pour cet essai :** les quatre signatures détectent les
marqueurs envoyés au serveur HTTP temporaire. Aucune exploitation réussie,
lecture de fichier sensible ou XSS exécutée n’est montrée. La détection sur
File Browser/8080, le trafic chiffré et tous les autres trajets restent hors
de la portée de ces preuves. L’arrêt final du serveur temporaire reste à confirmer.

## 1. Lire le dépôt et choisir — 20 min

Source : [daffainfo/suricata-rules](https://github.com/daffainfo/suricata-rules/tree/main),
consulté le 7 octobre 2026 via son API et ses fichiers bruts. Le dépôt contient
notamment des signatures HTTP génériques, des identifiants par défaut et des
signatures liées à des produits/CVE. Ne pas installer tout le dépôt ni exécuter
son script de génération pour cet exercice.

Quatre signatures sont proposées pour commencer ; le choix final appartient
à l’apprenant après lecture de **la ligne complète**. Le nombre de fichiers
n’est pas le nombre de signatures. Les signatures génériques signalent des
motifs ; elles ne démontrent pas que File Browser est vulnérable à ces attaques.

| Fichier et SID proposés | Comportement / conditions principales | Pertinence et limites |
| --- | --- | --- |
| `http/web-attacks/path-traversal.rules`, 50500003 | HTTP reconnu ; URI brute contenant deux points encodés `%2e%2e`, sans distinction de casse | Détecter une forme de sonde de traversée ; le contenu encodé doit rester visible sur le réseau |
| Même fichier, 50500004 | HTTP reconnu ; URI brute contenant `..%2f`, sans distinction de casse | Variante de séparateur encodé ; un motif n’indique pas une lecture de fichier réussie |
| Même fichier, 50500006 | HTTP reconnu ; URI brute contenant `%252e%252e`, sans distinction de casse | Double encodage ; vérifier que le client ne transforme pas la chaîne avant émission |
| `http/web-attacks/cross-site-scripting.rules`, 50100004 | HTTP reconnu ; URI normalisée contenant une ouverture de balise script, sans distinction de casse | Tester une signature de motif XSS ; aucun besoin d’exécuter du JavaScript ni d’affirmer une XSS réelle |

Toutes utilisent `alert http any any -> any any` : elles ne limitent pas à
elles seules la détection à la VM. Le filtre d’analyse doit identifier le
trafic de laboratoire ; documenter séparément toute adaptation de règle.
Les mots-clés HTTP anciens du dépôt et la version du moteur doivent être
vérifiés par le test de configuration, pas supposés compatibles.

```bash
git clone https://github.com/daffainfo/suricata-rules.git /tmp/ais-suricata-rules
git -C /tmp/ais-suricata-rules rev-parse HEAD
less /tmp/ais-suricata-rules/http/web-attacks/path-traversal.rules
less /tmp/ais-suricata-rules/http/web-attacks/cross-site-scripting.rules
```

Conserver commit, chemin, ligne complète, SID/rev, protocole, direction,
conditions (`content`, buffer HTTP, `nocase`, éventuel `flow`/PCRE), motif du
choix et limites. Écarter les règles pour des produits absents, sauf simulation
explicitement documentée. Ne pas recopier une alerte CVE comme preuve d’applicabilité.

Après lecture et acceptation des quatre signatures proposées, extraire uniquement
ces lignes ; si d’autres règles sont choisies, modifier explicitement la sélection :

```bash
python3 - <<'SELECT'
from pathlib import Path
root = Path('/tmp/ais-suricata-rules/http/web-attacks')
selection = {'path-traversal.rules': [50500003, 50500004, 50500006],
             'cross-site-scripting.rules': [50100004]}
lines = []
for name, sids in selection.items():
    for sid in sids:
        found = [line for line in (root / name).read_text().splitlines()
                 if line.lstrip().startswith('alert ') and f'sid:{sid};' in line]
        if len(found) != 1:
            raise SystemExit(f'SID {sid}: sélection ambiguë ou absente')
        lines.extend(found)
assert 1 <= len(lines) <= 10
Path('/tmp/ais-selection.rules').write_text('\n'.join(lines) + '\n')
print(f'{len(lines)} signatures sélectionnées')
SELECT
cat /tmp/ais-selection.rules
```

## 2. Installer et valider — 15 min

Sur l’hôte, sauvegarder configuration et fichier local existant avant modification.
Le chemin suivant est un exemple courant ; vérifier celui réellement utilisé
par le service. Éviter les collisions de SID avec des signatures déjà chargées.

```bash
sudo cp -a /etc/suricata/suricata.yaml /etc/suricata/suricata.yaml.avant-it8
sudo install -d -m 0755 /etc/suricata/rules
sudo install -m 0644 /tmp/ais-selection.rules /etc/suricata/rules/ais-it8.rules
sudoedit /etc/suricata/suricata.yaml
```

Ajouter à la liste **existante** `rule-files`, sans remplacer les autres entrées :

```yaml
rule-files:
  # Conserver ici les entrées déjà configurées.
  - /etc/suricata/rules/ais-it8.rules
```

Vérifier que la sortie EVE est active, que son type `alert` est activé et
que sa destination correspond à `/var/log/suricata/eve.json`. Vérifier
l’interface de capture réellement utilisée par le service et les variables
réseau ; ne pas présumer que `virbr0` ou la carte physique est la bonne interface.

```bash
sudo suricata -T -c /etc/suricata/suricata.yaml
```

Relever code de retour et bilan de chargement : **aucune signature sélectionnée
ne doit être rejetée**, même si le processus retourne zéro. Corriger chemins,
syntaxe ou SID en cas d’erreur. Conserver toute adaptation à côté de l’original.
Ne redémarrer qu’après acceptation de la configuration et des règles :

```bash
sudo systemctl restart suricata
sudo systemctl status suricata --no-pager
sudo journalctl -u suricata -n 40 --no-pager
```

Un service actif ne prouve pas encore la visibilité ni le déclenchement.
En cas d’échec, restaurer la configuration/fichier précédents et retester
avant reprise ; ne pas supprimer les preuves du diagnostic.

## 3. Vérifier le trajet puis générer les motifs — 20 min

Choisir l’IP réelle de la VM et une interface hôte portant son trafic.
`ip route get IP_VM`, `ip -br link` et la configuration réseau virtuel aident
à les identifier. Observer une requête normale avec `tcpdump` :

```bash
# Remplacer les deux valeurs avant exécution.
VM_IP='IP_VM_A_RENSEIGNER'
OBS_IF='INTERFACE_A_RENSEIGNER'
sudo tcpdump -ni "$OBS_IF" "host $VM_IP and tcp port 8080"
```

Dans un autre terminal hôte, envoyer un accès normal à la VM ; vérifier les
paquets et réponses sur **l’interface surveillée par Suricata**. Une requête
sur localhost, une interface différente ou un trafic chiffré ne valide pas
la visibilité des motifs HTTP attendus. Le port 8080 n’est pas une garantie
que le moteur reconnaît le protocole HTTP.

Pour un test sans action applicative sur File Browser, utiliser un **serveur
HTTP temporaire isolé dans la VM**, sur un port de laboratoire autorisé,
servant uniquement un répertoire vide. Le trafic VM/hôte emprunte le même
réseau observé ; ce test ne prouve pas la détection sur le flux File Browser 8080.
Sur la VM, avec Python 3 disponible, dans un terminal dédié :

```bash
TEST_DIR=$(mktemp -d /tmp/ais-ids-test.XXXXXX)
python3 -m http.server 18080 --bind IP_VM_A_RENSEIGNER --directory "$TEST_DIR"
```

Limiter cet accès au laboratoire ; ne pas ouvrir une publication Internet.
Sur l’hôte, contrôler les paquets du port 18080 sur la même interface puis
émettre seulement ces GET, sans authentification ni fichier sensible :

```bash
BASE="http://$VM_IP:18080"
curl --path-as-is --max-time 5 "$BASE/ids-test?probe=%2e%2e"
curl --path-as-is --max-time 5 "$BASE/ids-test?probe=..%2f"
curl --path-as-is --max-time 5 "$BASE/ids-test?probe=%252e%252e"
curl --path-as-is --max-time 5 "$BASE/ids-test?probe=%3Cscript"
```

Ces marqueurs sont inertes sur ce serveur de fichiers vide ; aucune charge
exécutable n’est nécessaire. Des réponses 404 sont compatibles avec une
alerte : la signature reconnaît la requête, pas la réussite d’une attaque.
Arrêter ensuite le serveur avec Ctrl+C et retirer l’éventuelle ouverture
temporaire. Ne pas affaiblir le filtrage de 8080 pour déclencher un test.

## 4. Retrouver et analyser EVE — 20 min

Noter heure et SID avant chaque essai. Lire les nouveaux événements pendant
les tests, plutôt que confondre anciennes alertes et nouvelles :

```bash
sudo tail -n 0 -F /var/log/suricata/eve.json | jq --unbuffered -c '
  select(.event_type == "alert") |
  select(.alert.signature_id == 50500003 or
         .alert.signature_id == 50500004 or
         .alert.signature_id == 50500006 or
         .alert.signature_id == 50100004) |
  {timestamp,flow_id,src_ip,src_port,dest_ip,dest_port,
   sid:.alert.signature_id,signature:.alert.signature,action:.alert.action}'
```

Comparer heures, IP, ports, SID/rev et `flow_id` au test. Une alerte indique
le motif observé ; elle ne prouve pas l’exploitation de File Browser et un
IDS passif ne remplace pas le pare-feu. Le [risque résiduel 8080](../it-5/finaliser-compte-rendu-durcissement-verification.md#complement-du-6-octobre-2026-acces-reseau-au-port-8080)
reste distinct de cette activité.

| Signature | Résultat à renseigner | Si pas d’alerte, expliquer les conditions manquantes |
| --- | --- | --- |
| 50500003 | Alerte observée sur 18080, capture de 10 h 30 | URI brute doit contenir le motif encodé ; contrôler émission et capture |
| 50500004 | Alerte observée sur 18080, capture de 10 h 30 | Séparateur encodé doit subsister dans la requête observée |
| 50500006 | Alerte observée sur 18080, capture de 10 h 30 | Double encodage exact requis |
| 50100004 | Alerte observée sur 18080, capture de 10 h 30 | URI normalisée doit contenir le motif ; HTTP doit être décodé |

En l’absence d’alerte : vérifier chargement, trajet, protocole, buffer,
encodage, chiffrement, pertes/compteurs, suppression/seuils éventuels et
sortie EVE. Ne pas conclure « règle inefficace » sans vérifier ces conditions.
Pour une autre règle choisie, expliquer produits, requêtes, état du flux et
buffers nécessaires ; conserver « non déclenchée » si l’essai ne peut pas
être réalisé sans risque. Une analyse hors ligne ne prouve pas la capture en direct.

## 📦 Livrables renseignés — Règles sélectionnées et tests

Les quatre signatures (rev 1) proviennent du commit
`23bfba7e688fdf5fadd8e378f070dae843e14263` du dépôt. Leurs conditions sont
analysées dans la table de sélection et vérifiées par les essais documentés.
Aucune signature supplémentaire n’est nécessaire pour atteindre le maximum :
**quatre règles choisies, quatre déclenchées**.

| Règle | Ce qu’elle cherche à détecter | Pertinente pour notre environnement ? | Test réalisé | Résultat |
| --- | --- | --- | --- | --- |
| SID 50500003 — points encodés | `%2e%2e` dans l’URI HTTP brute, sans distinction de casse | Oui pour observer une sonde HTTP générique ; ne démontre pas une vulnérabilité de File Browser | GET `/ids-test?probe=%2e%2e` vers VM:18080 depuis l’hôte, via virbr0 | Alerte EVE à 10:30:38.887961 +02:00 |
| SID 50500004 — séparateur encodé | `..%2f` dans l’URI HTTP brute, sans distinction de casse | Oui pour cette variante de motif de traversée ; comportement applicatif non évalué par la signature | GET `/ids-test?probe=..%2f` sur le même serveur temporaire | Alerte EVE à 10:30:38.892375 +02:00 |
| SID 50500006 — double encodage | `%252e%252e` dans l’URI HTTP brute, sans distinction de casse | Oui pour vérifier la détection du motif doublement encodé | GET `/ids-test?probe=%252e%252e` sur le même serveur temporaire | Alerte EVE à 10:30:38.898569 +02:00 |
| SID 50100004 — motif XSS | Ouverture de balise script dans l’URI normalisée, sans distinction de casse | Oui pour une détection HTTP générique ; aucune exécution JavaScript ni XSS prouvée | GET `/ids-test?probe=%3Cscript` sur le même serveur temporaire | Alerte EVE à 10:30:38.904860 +02:00 |

Suricata a accepté les quatre règles avant reprise du service : 4 chargées,
0 échouées, 0 ignorées et code 0. Les captures documentent les échanges sur
18080 et les quatre alertes. Les réponses HTTP 404 du serveur temporaire
n’empêchent pas la détection de la requête. Ces tests ne sont pas des attaques
réussies et ne prouvent pas le déclenchement sur File Browser/8080.

### Exemple d’alerte effectivement déclenchée

L’objet suivant est la **transcription de l’extrait affiché par le filtre jq**
sur la capture de 10:30:55. Il conserve les champs visibles de l’événement
EVE, avec les alias `sid`, `signature` et `action` utilisés par la commande.
Ce n’est pas une copie de l’objet EVE brut complet ni un exemple fictif :

```json
{
  "timestamp": "2026-10-07T10:30:38.887961+0200",
  "flow_id": 183670500373292,
  "src_ip": "192.168.122.1",
  "src_port": 52274,
  "dest_ip": "192.168.122.229",
  "dest_port": 18080,
  "sid": 50500003,
  "signature": "Possible Path Traversal attack, percent-encoded dot-dot sequence",
  "action": "allowed"
}
```

La source est l’hôte, la destination le serveur temporaire de la VM.
Le SID correspond à la chaîne `%2e%2e` envoyée ; l’action affichée ne montre
pas un blocage. La capture est conservée dans la section « Captures de
réalisation » de cette feuille.

Pour conserver **l’objet brut correspondant dans eve.json**, la commande
suivante a été utilisée ; son résultat est visible à 10:55:20. À retenir sur
l’hôte l’événement par SID et horodatage, sans dépendre des alias jq :

```bash
sudo jq -c '
  select(.event_type == "alert" and
         .alert.signature_id == 50500003 and
         .timestamp == "2026-10-07T10:30:38.887961+0200")
' /var/log/suricata/eve.json > "$HOME/ais-it8-alerte-50500003.json"
wc -l "$HOME/ais-it8-alerte-50500003.json"
jq . "$HOME/ais-it8-alerte-50500003.json"
```

**Export brut réalisé :** la capture de 10:55:20 montre une ligne et l’objet
complet attendu. Pour une nouvelle extraction, vérifier également le résultat.
Si le fichier est vide, rechercher le journal tourné/archivé contenant cet
horodatage ; ne pas présenter un export vide comme une preuve. Conserver
l’original dans l’espace privé de preuve et publier seulement les champs utiles
anonymisés. Aucune difficulté de déclenchement n’est constatée pour ces quatre
règles ; leurs limites de visibilité et de pertinence restent documentées.

## Captures complémentaires — Reprise des essais et export

Ces neuf captures du 7 octobre complètent les premières preuves. Les essais
sont présentés à leurs horaires réels ; un événement exporté à 10:55 peut
provenir du test antérieur de 10:30.

### 10:47:59 — Sélection des quatre signatures réutilisée

![Sélection des quatre signatures réutilisée](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2010-47-59.png)

Le dépôt existe déjà : le second clone échoue sans invalider la copie existante. Le même commit est affiché et les quatre signatures sont extraites à nouveau.

### 10:48:43 — Référence du fichier local dans le YAML

![Référence du fichier local dans le YAML](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2010-48-43.png)

Le bloc rule-files référence le chemin absolu ais-it8.rules ; default-rule-path reste /var/lib/suricata/rules. Le chemin absolu permet de charger le fichier local indépendamment de ce répertoire.

### 10:49:17 — Configuration acceptée et service actif après redémarrage

![Configuration acceptée et service actif après redémarrage](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2010-49-17.png)

Le test indique une configuration chargée avec succès ; le service est active (running) depuis 10:48:58. Cette image complète la validation détaillée des quatre règles de 10:18.

### 10:52:44 — Capture TCP sur virbr0 au port 18080

![Capture TCP sur virbr0 au port 18080](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2010-52-44.png)

Les échanges bidirectionnels hôte/VM sur 18080 sont visibles vers 10:52:37, avec établissement de connexions, données et fermeture.

### 10:52:54 — Quatre requêtes de test envoyées depuis l’hôte

![Quatre requêtes de test envoyées depuis l’hôte](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2010-52-54.png)

Les commandes curl portent les quatre motifs sélectionnés ; les réponses affichées sont des erreurs HTTP 404 du serveur temporaire.

### 10:53:00 — Journal du serveur temporaire dans la VM

![Journal du serveur temporaire dans la VM](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2010-53-00.png)

Le répertoire temporaire et le serveur lié à l’adresse de la VM sont visibles. Les quatre GET reçus à 10:52:37 correspondent aux motifs encodés ; chaque réponse est 404.

### 10:54:28 — Nouvelles alertes EVE lors des répétitions

![Nouvelles alertes EVE lors des répétitions](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2010-54-28.png)

La lecture affiche deux alertes SID 50500003 à 10:54:09 et 10:54:18, puis deux SID 50100004 à 10:54:19 et 10:54:20, sur 18080. Cette image montre ces deux signatures répétées ; elle ne remplace pas la preuve des quatre SID de 10:30.

### 10:54:36 — Répétition du motif de balise script

![Répétition du motif de balise script](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2010-54-36.png)

Deux appels avec le marqueur encodé sont visibles avec réponses 404 ; aucun JavaScript exécuté ni exploitation réussie ne sont démontrés.

### 10:55:20 — Export d’un événement EVE complet

![Export d’un événement EVE complet](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2010-55-20.png)

wc affiche une ligne dans ais-it8-alerte-50500003.json. jq montre l’objet correspondant au SID 50500003 du premier test à 10:30:38.887961, avec in_iface virbr0, URI, HTTP 404 et compteurs de flux.

**État actualisé :** l’export de l’objet brut est désormais documenté.
La fermeture finale du serveur temporaire et le retrait des éventuels accès
temporaires restent à confirmer ; aucune correction de filtrage 8080 n’est
déduite de ces captures.

## Sources et pièces à conserver

Conserver sélection (1 à 10 signatures), commit et analyse de chaque règle,
configuration acceptée et bilan de chargement, interface et visibilité,
commandes/horaires, événements EVE anonymisés, analyse et limites par signature.
Captures et journaux peuvent contenir des données privées : ne publier que
les extraits nécessaires et anonymisés. Les quatre alertes du bilan sont étayées par les captures ; les autres
vérifications doivent conserver leur statut propre.

- [Règles de traversée du dépôt](https://github.com/daffainfo/suricata-rules/blob/main/http/web-attacks/path-traversal.rules)
- [Règles XSS du dépôt](https://github.com/daffainfo/suricata-rules/blob/main/http/web-attacks/cross-site-scripting.rules)
- [Options officielles Suricata : test et capture](https://docs.suricata.io/en/latest/command-line-options.html) ; utiliser la documentation correspondant à la version installée.
- [Buffers HTTP officiels](https://docs.suricata.io/en/latest/rules/http-keywords.html)
- [Retour à l’itération 8](index.md)
- [Retour au module](../README.md)


- [Étape suivante — Observer l’activité autour de File Browser](observer-activite-file-browser.md)
