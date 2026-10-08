# Observer l’activité autour de File Browser

**Itération 7 — 7 octobre 2026 — Travail individuel**

## 🎯 Objectif et point de départ

Observer plusieurs activités contrôlées sur **File Browser**, retrouver leurs
traces et distinguer connaissances de l’expérimentateur et conclusions possibles
à partir des seuls événements Suricata.

Suricata écoute sur l’hôte, sur `virbr0`. La VM est `192.168.122.229` et le
port documenté de File Browser est **8080**. L’hôte est extérieur à la VM ;
les essais depuis l’hôte ne démontrent pas une exposition Internet.
Les quatre signatures installées reconnaissent des motifs de traversée/XSS.
Leurs déclenchements antérieurs sur **18080** concernent le serveur temporaire,
pas File Browser. Ne pas reprendre ces alertes comme résultats de cette activité.

**Statut : essais HTTP documentés par les captures ci-dessous ; activité SSH/22 à compléter.** Un HEAD `/` vers 8080 avec
HTTP 404 a déjà été observé à 10:40:49 dans la
[feuille des événements](comprendre-evenements-produits.md). Cette preuve peut
servir de point de comparaison, sans inventer de nouveaux résultats.

## Bilan des captures — 7 octobre 2026

Huit captures documentent les activités HTTP. Elles sont conservées dans le
dossier de dépôt `it-7` et illustrent cette feuille de l’itération 8.
Aucune de ces images ne documente l’essai A4 sur SSH/22.

| Activité réalisée | Événement retrouvé ? | Alerte ? | Informations disponibles | Informations manquantes |
| --- | --- | --- | --- | --- |
| A1 — Navigateur et GET / | Oui : http et fileinfo, autour de 10:58:52 et 10:59:21 | alert:null dans les objets projetés ; flux curl montré avec alerted:false | Hôte/VM, 8080, virbr0, méthode, URL, user-agent, statut 200 | Identité métier, intention, validation complète du parcours |
| A2 — Cinq GET successifs | Oui : transactions et bilans de flux de 10:59:51–55 | Bilans affichés avec alerted:false | Rythme, ports sources distincts, GET /, HTTP 200 | Motif de répétition et activité hors intervalle capturé |
| A3 — Ressources de la page | Oui : JavaScript, CSS, police, favicon et logo | alert:null dans les objets sélectionnés | Chemins, types de contenu, statut 200 et referer | Quels chargements sont des actions humaines ; droits métier |
| A4 — Autre service/22 | Non vérifiable : capture manquante | Non vérifiable | Aucun résultat nouveau fourni | Commande, trajet et objet SSH/flux correspondant |
| A5 — Chemin supposé absent | Oui : http et fileinfo à 11:00:56 | alert:null dans l’objet projeté | URI exacte, GET, HTTP 200, HTML longueur 5762 | Cause du retour 200 ; l’échec HTTP attendu n’est pas obtenu |
| Refus applicatif observé | Oui : POST /api/renew à 10:58:53, HTTP 401 | alert:null dans les objets sélectionnés | Endpoint, méthode et refus HTTP | Cause précise du refus ; ne pas l’assimiler à un échec de mot de passe |

**Interprétation :** les accès normaux et répétés sont observables sur 8080.
Les données montrées ne signalent pas d’alerte pour ces transactions ; elles
ne constituent pas une recherche exhaustive de toute activité suspecte.
Les quatre signatures actuelles ne comportent pas de règle dédiée aux répétitions
ou aux refus de renouvellement. L’activité répétée reste intéressante pour la
sécurité, mais son intention est inconnue sans contexte.

**Écart au scénario :** la ressource supposée absente retourne 200. Conserver
ce résultat réel. Le refus 401 sur /api/renew fournit un exemple d’échec HTTP
observé, sans en inventer la cause. L’essai SSH/22 reste à réaliser/documenter.

### 10:59:07 — Page de connexion File Browser

![Page de connexion File Browser](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2010-59-07.png)

Le navigateur affiche la page login sur 8080. Le nom admin visible ne prouve pas une connexion réussie ; aucun secret n’est affiché.

### 10:59:31 — Chargement de page et ressources dans EVE

![Chargement de page et ressources dans EVE](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2010-59-31.png)

GET / et ressources JavaScript, CSS, police et images sont visibles avec statut 200 sur virbr0. POST /api/renew retourne 401 : ce refus concerne un renouvellement et ne prouve pas un mauvais mot de passe. Les objets sélectionnés affichent alert:null.

### 10:59:42 — GET simple observé

![GET simple observé](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2010-59-42.png)

Un événement fileinfo à 10:59:21.172808 décrit la réponse HTTP à GET /, curl/8.18.0, statut 200 et longueur 5762. La direction est serveur vers client ; fileinfo n’est pas une alerte.

### 11:00:05 — Accès successifs visibles dans EVE

![Accès successifs visibles dans EVE](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2011-00-05.png)

Les dernières requêtes de la série autour de 10:59:53–55 apparaissent comme http/fileinfo, avec GET / et statut 200. Une transaction peut produire plusieurs objets.

### 11:00:15 — Cinq accès successifs côté client

![Cinq accès successifs côté client](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2011-00-15.png)

La boucle émet cinq accès entre 10:59:51 et 10:59:55, chacun avec HTTP 200. Les bilans de flux de la dernière capture complètent les traces réseau.

### 11:01:03 — Ressource supposée absente dans EVE

![Ressource supposée absente dans EVE](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2011-01-03.png)

L’objet fileinfo à 11:00:56.425363 montre GET /ais-observation-ressource-absente-20261007 avec statut 200 et réponse HTML de longueur 5762 : pas un 404.

### 11:01:07 — Résultat client de la ressource supposée absente

![Résultat client de la ressource supposée absente](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2011-01-07.png)

Curl confirme HTTP 200 à 11:00:56. Le chemin choisi ne produit donc pas l’échec attendu ; cela peut correspondre à un repli applicatif, à confirmer par le contenu/configuration.

### 11:01:33 — Objets historiques HTTP et bilans de flux

![Objets historiques HTTP et bilans de flux](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2011-01-33.png)

POST /api/login et GET /api/usage/ retournent 200 à 11:00:22. EVE seul ne désigne pas l’identité métier ni les droits obtenus. Les bilans des GET successifs montrent alerted:false ; les événements sont sur virbr0 et 8080.

## 1. Préparer le suivi sur l’hôte

Vérifier service actif, interface et destination avant les essais. Noter heure,
commande ou geste navigateur, URL, résultat client et identifiant d’activité
A1–A5. Utiliser uniquement le laboratoire et quelques requêtes ; ne pas faire
de scan large, de tentative de mot de passe ni de modification de documents.

Ouvrir le suivi EVE **avant** l’activité :

```bash
sudo tail -n 0 -F /var/log/suricata/eve.json | jq --unbuffered -c '
  select(.src_ip == "192.168.122.229" or .dest_ip == "192.168.122.229") |
  {timestamp,event_type,flow_id,in_iface,src_ip,src_port,dest_ip,dest_port,
   proto,app_proto,http,ssh,flow,alert}'
```

Ce filtre conserve événements normaux et alertes, ainsi que les deux sens.
`tail -n 0` ne montre pas le passé. Les objets `flow` peuvent apparaître
après fermeture/expiration ; une ligne EVE n’équivaut pas à un paquet.

## 2. Générer des activités contrôlées depuis l’hôte

### A1 — Accès normal

Avec le navigateur, ouvrir la page de connexion sans saisir de secret pour
la capture. Noter l’URL réellement chargée, redirections et ressources demandées.
Un contrôle en ligne de commande peut compléter cette observation :

```bash
FB_BASE='http://192.168.122.229:8080'
date --iso-8601=seconds
curl --max-time 5 -o /dev/null -sS -w 'HTTP %{http_code}\n' "$FB_BASE/"
```

Un GET `/` peut avoir un résultat différent du HEAD `/` déjà testé.
Conserver le code obtenu, sans supposer un 200. Le navigateur peut charger
plusieurs ressources pour un seul geste.

### A2 — Quelques accès successifs

```bash
for essai in 1 2 3 4 5; do
  date --iso-8601=seconds
  curl --max-time 5 -o /dev/null -sS -w 'HTTP %{http_code}\n' "$FB_BASE/"
  sleep 1
done
```

Cette série limitée n’est pas un test de charge. Rechercher cinq transactions
HTTP si journalisées ; le nombre de flux peut différer avec réutilisation de
connexion, et le nombre de paquets n’est pas le nombre de requêtes.

### A3 — Ressources différentes

Identifier deux ressources **réelles** de la page via le navigateur, puis
ouvrir chacune sans télécharger de document privé. Noter chemins et méthodes.
Ne pas inventer des chemins d’API ni envoyer de DELETE/POST pour obtenir une trace.
Distinguer requête réseau et ressource servie depuis le cache du navigateur.

### A4 — Autre service de la VM

SSH/22 est documenté dans le dossier ; si son accès est autorisé, ouvrir une
session avec les moyens habituels puis la fermer. Sinon, limiter l’essai
à la connectivité TCP d’un port déjà connu et autorisé :

```bash
date --iso-8601=seconds
nc -vz -w 3 192.168.122.229 22
```

Un test TCP ne garantit pas un événement applicatif `ssh` : il peut ne produire
qu’un flux. Les commandes d’une session SSH sont chiffrées et ne sont pas
lisibles par ce capteur réseau. Ne pas réactiver le serveur temporaire/18080
uniquement pour remplacer l’observation de File Browser.

### A5 — Requête qui échoue

Demander une ressource inexistante à nom unique :

```bash
date --iso-8601=seconds
curl --max-time 5 -o /dev/null -sS -w 'HTTP %{http_code}\n'   "$FB_BASE/ais-observation-ressource-absente-20261007"
```

Noter le statut réel ; une application peut retourner sa page d’accueil ou
rediriger au lieu de produire un 404. Une erreur HTTP n’est pas une preuve
d’attaque. Ne pas confondre code HTTP, refus de connexion et expiration réseau.

## 3. Retrouver les événements et les éventuelles alertes

Lire l’historique si les événements ont précédé le lancement du suivi :

```bash
sudo jq -c '
  select(.src_ip == "192.168.122.229" or .dest_ip == "192.168.122.229") |
  select(.event_type == "http" or .event_type == "ssh" or
         .event_type == "flow" or .event_type == "alert")
' /var/log/suricata/eve.json | tail -n 40
```

Corréler heure/fuseau, IP, port, méthode, URL et `flow_id`. Examiner les alertes
du même intervalle et flux ; ne pas associer automatiquement une alerte sur
18080 à une requête sur 8080. Vérifier SID, signature et contexte.

Les cinq activités ne contiennent normalement pas les motifs des quatre
signatures sélectionnées. **Hypothèse : aucune alerte de ces signatures**,
à confirmer dans EVE. Une ressource ou une réponse peut néanmoins contenir
un motif : si une alerte apparaît, lire les conditions et les données visibles
avant d’en déduire une attaque. Aucun déclenchement n’est requis pour chaque activité.

## 4. Grille pour compléter ou reproduire les essais

| Activité réalisée | Événement retrouvé ? | Alerte ? | Informations disponibles | Informations manquantes |
| --- | --- | --- | --- | --- |
| Référence antérieure : HEAD `/` sur 8080, 10:40:49 | Oui : HTTP, preuve dans la feuille EVE | Aucune alerte affichée dans l’objet sélectionné ; pas une recherche exhaustive | Hôte:59208 → VM:8080, HEAD, URL `/`, HTTP/1.1, statut 404, heure/flow_id | Intention, identité métier, état global du service ; pas de preuve d’un parcours authentifié |
| A1 : accès normal actuel | À vérifier | À vérifier | Relever IP/ports, méthode, URL, statut, heure et flow_id | Noter les champs absents et limites de décodage |
| A2 : cinq accès successifs | À vérifier | À vérifier | Nombre et rythme des transactions effectivement journalisées | Identité de l’utilisateur, intention, éventuels accès non journalisés |
| A3 : deux ressources réelles | À vérifier | À vérifier | Chemins/méthodes/statuts visibles | Cache navigateur, contenu non journalisé, droits applicatifs |
| A4 : SSH ou connectivité TCP/22 | À vérifier | À vérifier | IP/ports, flux ; SSH si réellement décodé et journalisé | Commandes et contenu chiffré ; utilisateur non établi par le flux seul |
| A5 : ressource absente | À vérifier | À vérifier | URI et réponse réelles si HTTP journalisé | Cause applicative exacte de l’échec et intention |

Si aucun événement n’apparaît, vérifier trajet, types EVE activés, chiffrement,
délai de sortie, pertes et journal tourné. Écrire **Non vérifiable** tant que
la preuve manque ; absence de trace ne signifie pas absence de trafic.

## 5. Ce que je sais / ce que le capteur permet de déduire

| Connaissance de l’expérimentateur | Conclusion possible à partir d’EVE seul |
| --- | --- |
| J’ai volontairement lancé cinq requêtes | Plusieurs requêtes visibles à un rythme donné ; leur intention n’est pas connue |
| Je suis l’utilisateur autorisé sur l’hôte | Une adresse source observée ; elle ne prouve pas une identité métier |
| J’ai choisi une ressource inexistante | Une URI et un statut ; la cause précise nécessite logs/contexte applicatifs |
| J’ai ouvert/fermé une session SSH | Connexion ou négociation SSH observable ; opérations internes chiffrées non lisibles |
| J’ai chargé une page dans le navigateur | Ensemble de transactions, pas forcément une action humaine par requête |

### Trois constats à retenir

- **Activité correctement observable déjà prouvée :** le HEAD vers File Browser/8080 du premier essai, avec méthode, URL et statut 404. Compléter avec les nouvelles activités une fois leurs événements retrouvés.
- **Information non déterminable avec ces seules données :** l’intention de l’émetteur et son identité métier. Pour SSH/HTTPS, le contenu chiffré n’est pas accessible comme du HTTP en clair.
- **Activité intéressante pour la sécurité sans règle dédiée actuellement :** répétition rapide d’accès ou série de ressources inexistantes. Les quatre signatures installées recherchent des motifs de traversée/XSS, pas un seuil de fréquence ni une série d’échecs. Le résultat réel doit être vérifié : un rythme inhabituel peut justifier une investigation mais ne prouve pas une attaque.

Une future détection de fréquence demanderait fenêtre, seuil, regroupement
par source/service, usages légitimes et tests de faux positifs. Ne pas l’ajouter
implicitement au jeu actuel ni déclarer ces accès bloqués par Suricata.

## 📦 Livrable

Tableau renseigné pour A1, A2, A3 et le résultat réel A5 ; A4 reste à compléter.
Conserver commandes/gestes et horaires, objets EVE anonymisés,
alertes éventuelles ou absence constatée sur un intervalle défini, et comparaison
entre connaissances du testeur et déductions du capteur. Conserver les références
aux preuves sans publier secrets, cookies, jetons ou documents privés.

- [Règles installées et limites de leurs tests](installer-tester-regles-suricata.md)
- [Événements EVE et preuve HTTP antérieure](comprendre-evenements-produits.md)
- [Point d’observation](identifier-point-observation.md)
- [Retour à l’itération 8](index.md)
- [Retour au module](../README.md)

- [Étape suivante — Faire le bilan du dispositif](bilan-dispositif-detection.md)
