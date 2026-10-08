# Comprendre les événements produits

**Itération 7 — 7 octobre 2026 — Travail individuel**

## 🎯 Objectif et état de départ

Identifier les informations produites par Suricata, retrouver un événement
et distinguer activité observée et activité signalée comme suspecte.

**Étape précédente dans le parcours :** [Identifier le point d’observation](identifier-point-observation.md).
Les tests de règles ont déjà été réalisés avant cette remise en ordre du parcours ;
leurs preuves sont conservées dans la [feuille des règles](installer-tester-regles-suricata.md).
Quatre alertes sur le serveur temporaire/18080 sont déjà documentées. Cette
nouvelle activité porte aussi sur le trafic normal, les sorties de la VM et
les accès File Browser/8080. **Les captures de 10 h 38 à 10 h 41 documentent les résultats ci-dessous.**
Suricata et les lectures EVE sont sur **l’hôte**, le trafic sortant est généré
**dans la VM** ; ne pas inverser les machines.

## Résultats observés — 7 octobre 2026

### Localisation EVE — 10:38:40

![Fichier EVE présent et configuration du service](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2010-38-40.png)

Le fichier `/var/log/suricata/eve.json` existe sur l’hôte, taille affichée
1,4 Mo. Le service lance Suricata avec `--af-packet` et la configuration
`/etc/suricata/suricata.yaml`. La commande `--dump-config` est saisie, mais
son contenu n’est pas visible : les types activés ne sont pas prouvés par
cette image seule. Les événements suivants prouvent plusieurs sorties effectives.

### DNS et TLS — capture de 10:40:25

La capture fournie montre `dig example.org A` exécuté dans la VM avec
réponse `NOERROR`. Le résolveur local affiché est `127.0.0.53`, tandis qu’EVE
observe l’échange réseau entre la VM et `192.168.122.1:53` sur `virbr0`.
La requête et la réponse partagent le même `flow_id`.

L’accès externe réellement utilisé est `https://www.google.com/`, plutôt
que la destination illustrative de la procédure. Curl retourne HTTP/2 200 ;
EVE produit un événement TLS avec SNI `www.google.com` et version TLS 1.3.
La réponse affichée par curl est vue par le client, pas déchiffrée par Suricata.

### HTTP vers File Browser — capture de 10:40:53

Après sortie de la session VM, l’hôte exécute un HEAD vers
`http://192.168.122.229:8080/`. Curl retourne HTTP/1.1 404 et EVE enregistre
un événement `http` : source `192.168.122.1:59208`, destination
`192.168.122.229:8080`, méthode HEAD, URL `/`, statut 404.
Cela établit la visibilité du flux HTTP vers le port File Browser publié ;
ce n’est ni une validation du parcours authentifié ni une preuve d’exploitation.

**Présentation des deux captures :** les images de 10:40:25 et 10:40:53
contiennent des valeurs `Set-Cookie`. Leurs résultats sont repris ci-dessus,
mais les images brutes ne sont pas intégrées à la page. Des copies avec ces
valeurs masquées pourront remplacer ces descriptions. Les originaux déposés
restent à retirer des assets publics ou à anonymiser avant publication du site.

### Recherche des objets EVE — 10:41:18

![Recherche des événements DNS TLS HTTP et flux dans EVE](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2010-41-18.png)

La recherche historique montre les objets complets, notamment `in_iface:
virbr0`, des événements DNS, TLS, HTTP et `flow`. Un flux HTTP de contrôle de
connectivité et un flux NTP apparaissent aussi : il ne faut pas les attribuer
aux commandes manuelles sans preuve. Certains bilans de flux indiquent
`alerted:false`. La capture de la lecture en direct montre `alert:null` pour
les événements normaux sélectionnés ; cette absence ne prouve pas l’innocuité
de tout le trafic.

| Événement choisi | Heure (+02:00) et transport | Informations disponibles et interprétation |
| --- | --- | --- |
| DNS example.org | 10:40:08.438453, UDP ; VM:42289 → hôte:53 | Requête A, réponse à 10:40:08.454504, NOERROR ; activité DNS observée |
| TLS Google | 10:40:08.513018, TCP ; VM:49188 → 142.251.157.119:443 | SNI, TLS 1.3, métadonnées ; contenu HTTP chiffré non observé dans EVE |
| HTTP File Browser | 10:40:49.990033, TCP ; hôte:59208 → VM:8080 | HEAD `/`, HTTP/1.1, statut 404 ; événement normal, sans alerte affichée |
| Bilan DNS | 10:40:47.169714, UDP ; VM:55584 → hôte:53 | Compteurs, début/fin, expiration et `alerted:false` ; bilan d’un échange antérieur |

**Bilan :** fichier localisé, activités normales retrouvées et distinguées des
quatre alertes pédagogiques précédentes. L’accès 8080 est visible depuis
l’hôte ; son filtrage, la connexion authentifiée, la visibilité de tous les
trajets et l’ingestion Wazuh ne sont pas démontrés par ces captures.

## 1. Localiser et vérifier EVE sur l’hôte

Le chemin courant est `/var/log/suricata/eve.json`, déjà utilisé pour les
alertes précédentes. Vérifier le chemin effectif dans son installation :

```bash
sudo ls -lh /var/log/suricata/eve.json
systemctl cat suricata
sudo suricata --dump-config -c /etc/suricata/suricata.yaml | less
```

Dans la configuration effective, examiner `default-log-dir`, le bloc
`outputs` / `eve-log` (`enabled`, `filetype`, `filename`, `types`) et une
éventuelle option de lancement `-l`. Une sortie vers un socket, des fichiers
par thread ou une autre destination change la façon de retrouver EVE.
Ne pas rechercher ce fichier dans la VM puisque le capteur fonctionne sur l’hôte.

EVE est généralement un flux **JSON avec un objet par ligne**, pas un tableau
JSON unique. Afficher les cinq derniers objets complets :

```bash
sudo tail -n 5 /var/log/suricata/eve.json | jq .
```

Vérifier que les types utiles (`dns`, `http`, `tls`, `flow`, `alert`) sont
activés dans le bloc EVE existant ; ne pas le remplacer par une configuration
minimale qui ferait disparaître les autres sorties. Si une modification est
nécessaire, conserver une sauvegarde distincte, tester avec `suricata -T -v -c`
puis redémarrer seulement après succès et vérifier le service.
La présence du fichier seule ne prouve pas qu’il reçoit de nouveaux événements.

## 2. Suivre les activités sans filtrer uniquement les alertes

Sur l’hôte, ouvrir la lecture **avant** les essais :

```bash
sudo tail -n 0 -F /var/log/suricata/eve.json | jq --unbuffered -c '
  select(.src_ip == "192.168.122.229" or .dest_ip == "192.168.122.229") |
  {timestamp,event_type,flow_id,src_ip,src_port,dest_ip,dest_port,
   proto,app_proto,dns,http,tls,flow,alert}'
```

Ce filtre vise la VM observée sur `virbr0`. Les événements `stats` sans IP
n’apparaîtront pas ; consulter le fichier sans filtre pour examiner ces compteurs.
`tail -n 0` ne montre pas les événements antérieurs. Les journaux de flux peuvent
être produits après fermeture/expiration : ne pas attendre un événement pour
chaque paquet ni conclure immédiatement à une absence d’observation.

## 3. Générer du trafic normal

Noter machine émettrice, heure avec fuseau, commande, destination et résultat.
Éviter les identifiants, jetons et documents privés dans les exemples.

### Depuis la VM — DNS et connexion externe

```bash
date --iso-8601=seconds
# Si dig est disponible : requête via le résolveur configuré.
dig example.org A
curl --max-time 10 -I https://example.org/
```

Ne pas imposer un DNS public si le réseau exige son propre résolveur.
Si `dig` manque, utiliser l’outil DNS déjà disponible ; `getent ahosts example.org`
peut utiliser un cache ou `/etc/hosts` et ne garantit pas une émission DNS.
Une résolution locale via `127.0.0.53` n’est pas visible sur le bridge : seule
l’éventuelle requête réseau du résolveur l’est. Avec cache, DNS chiffré ou proxy,
les événements disponibles peuvent différer.

Le HTTPS peut produire des métadonnées TLS ou un flux, selon les types activés
et le décodage ; le contenu HTTP chiffré n’est pas lisible depuis ce point.
Conserver les échecs éventuels comme résultats et vérifier DNS, routage et
filtrage sans ouvrir de flux supplémentaire pour obtenir artificiellement une preuve.

### Depuis l’hôte — accès File Browser, extérieur à la VM

```bash
date --iso-8601=seconds
curl --max-time 10 -I http://192.168.122.229:8080/
```

L’hôte est extérieur **à la VM**, mais cet essai ne démontre pas une exposition
à Internet. Un accès par navigateur à la page de connexion, sans opération
sur les documents, peut compléter le test. Noter redirection/code de réponse.
Le port 18080 et ses quatre alertes précédentes appartiennent au serveur de
test ; ne pas les attribuer à File Browser.

Si besoin, vérifier en parallèle le trajet sur l’hôte :

```bash
sudo tcpdump -ni virbr0 'host 192.168.122.229 and (port 53 or port 443 or port 8080)'
```

Cette capture cible uniquement ces ports ; elle ne couvre pas tout le trafic.
Elle prouve des paquets visibles, pas leur enregistrement dans EVE.

## 4. Sélectionner et retrouver plusieurs événements

Rechercher les activités déjà écrites, sans exclure les événements normaux :

```bash
sudo jq -c '
  select(.src_ip == "192.168.122.229" or .dest_ip == "192.168.122.229") |
  select(.event_type == "dns" or .event_type == "http" or
         .event_type == "tls" or .event_type == "flow" or
         .event_type == "alert")
' /var/log/suricata/eve.json | tail -n 20
```

Choisir plusieurs objets correspondant aux heures des essais : par exemple
DNS, TLS/flux sortant, HTTP vers File Browser et une alerte du test précédent.
Conserver l’objet complet dans l’espace de preuve protégé avant d’en extraire
les champs utiles. Si un type manque, documenter la cause et garder
**Non vérifiable** au lieu de créer un exemple présenté comme observé.

Pour retrouver les événements d’un flux choisi, remplacer la valeur par le
`flow_id` réellement lu ; `--arg` évite de saisir un grand identifiant comme
nombre dans le filtre :

```bash
sudo jq --arg fid 'FLOW_ID_A_RENSEIGNER' '
  select(.flow_id != null and (.flow_id | tostring) == $fid)
' /var/log/suricata/eve.json
```

Compléter la corrélation avec date, capteur, IP et ports ; le `flow_id` n’est
pas un identifiant universel entre toutes les sources/outils. Certains objets
n’ont pas de ports, de protocole applicatif ou de bloc `alert` : champ absent
ne signifie pas automatiquement une erreur.

| Champ | Ce qu’il permet de lire |
| --- | --- |
| `timestamp` | Date/heure et décalage de fuseau ; rapprocher l’heure des essais |
| `src_ip`, `dest_ip` | Adresses du trafic observé ; tenir compte du point de capture et du NAT éventuel |
| `src_port`, `dest_port` | Ports lorsqu’applicables ; préciser la direction de l’objet observé |
| `proto`, `app_proto` | Transport réseau et protocole applicatif reconnu, lorsqu’ils sont présents |
| `event_type` | Nature du journal : activité DNS/HTTP/TLS, flux, alerte, statistiques, etc. |
| `flow_id` | Lien entre objets EVE d’un même flux lorsqu’il est présent |
| `dns` | Requête/réponse, nom/type et réponses selon l’objet et la configuration |
| `http` | Méthode, hôte, URL ou statut selon les informations décodées/loguées |
| `tls` | Métadonnées de session disponibles ; ne donne pas automatiquement le contenu HTTP |
| `flow` | Bilan du flux, compteurs et état lorsqu’ils sont journalisés |
| `alert` | SID/rev, signature, catégorie, sévérité et action disponibles ; à analyser dans le contexte |

### Grille d’analyse à compléter

| Activité | Date/heure, IP/ports, transport | Type et informations applicatives | Alerte associée / preuve / limite |
| --- | --- | --- | --- |
| DNS depuis VM | 10:40:08 +02:00 ; UDP VM → hôte:53 | Requête A example.org et réponse NOERROR | Événements normaux documentés |
| Connexion externe depuis VM | 10:40:08 +02:00 ; TCP VM → serveur:443 | TLS 1.3, SNI www.google.com | TLS observé ; contenu HTTP non visible dans EVE |
| Accès File Browser depuis hôte | 10:40:49 +02:00 ; TCP hôte → VM:8080 | HEAD /, statut 404 | HTTP observé ; parcours authentifié non testé |
| Marqueurs du serveur temporaire | 7 octobre, autour de 10:30:38 +02:00 ; hôte vers VM:18080 | `alert`, quatre SID de la feuille précédente | Alertes documentées ; aucune exploitation démontrée |

## 5. Observer et détecter : deux conclusions différentes

**Observer une activité** consiste à enregistrer une communication ou ses
métadonnées : un nom DNS demandé, une session TLS ou une requête HTTP.
Un événement normal n’a pas besoin d’une signature suspecte pour être journalisé.

**Détecter une activité considérée comme suspecte** consiste ici à produire
une alerte lorsque les conditions d’une règle correspondent au trafic visible.
Les quatre marqueurs pédagogiques ont déclenché des alertes alors que leur
émission était volontaire et inerte. Une alerte demande qualification ; elle
ne prouve ni une intrusion ni la réussite d’une attaque.

Un événement `http` ou `dns` n’est donc pas une alerte par nature. L’absence
d’alerte ne garantit pas l’innocuité : visibilité, règles, chiffrement, pertes
et types journalisés conditionnent les résultats. Le champ `action` ne remplace
pas la vérification d’un blocage effectif ; un IDS passif ne devient pas un pare-feu.

## 📦 Livrable et suite

Localisation/configuration EVE, commandes et horaires des activités, plusieurs
objets anonymisés et grille renseignée, avec différences entre événements
normaux et alertes. Les nouveaux essais sont documentés dans le bilan ; conserver les limites
de portée et anonymiser les captures avec cookies avant publication.

EVE pourra être exploité par Wazuh lors de la suite du module. Son existence
ne prouve pas une ingestion Wazuh : accès au fichier, collecte, décodage et
réception devront être vérifiés séparément. Ne pas activer pour cet exercice
la journalisation des corps ou en-têtes d’authentification sans besoin.

- [Sortie EVE — documentation Suricata 8.0.3](https://docs.suricata.io/en/suricata-8.0.3/output/eve/eve-json-output.html)
- [Format EVE — documentation Suricata 8.0.3](https://docs.suricata.io/en/suricata-8.0.3/output/eve/eve-json-format.html)
- [Point d’observation](identifier-point-observation.md)
- [Tests de règles et preuves existantes](installer-tester-regles-suricata.md)
- [Retour à l’itération 8](index.md)
- [Retour au module](../README.md)

- [Étape suivante — Installer et tester des règles Suricata](installer-tester-regles-suricata.md)
