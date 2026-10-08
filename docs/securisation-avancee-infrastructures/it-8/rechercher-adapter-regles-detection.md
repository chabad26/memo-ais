# Rechercher et adapter des règles de détection

**Itération 8 — 8 octobre 2026 — Travail individuel — 1 h 15**

## 🎯 Objectif et statut

Rechercher des signatures directes ou des comportements associés aux
[constats de l’exercice précédent](vulnerabilites-besoins-detection.md), puis
choisir des règles dont les conditions sont visibles depuis `virbr0` sur l’hôte.

**Recherche réalisée ; configuration acceptée et alerte 1008001 observée dans
la capture fournie le 8 octobre.** Les règles 1008002 et 1008003 restent à
valider par une alerte correspondante. Les alertes du J7 ne valident pas
automatiquement ces nouvelles règles. Suricata 8.0.3 observe la VM `192.168.122.229` ; le service
File Browser est sur 8080. Adapter l’adresse si elle change.

## 1. Résultats de recherche et choix — 20 min

Source : [dépôt daffainfo](https://github.com/daffainfo/suricata-rules/tree/main),
copie consultée le 8 octobre, commit **23bfba7e688fdf5fadd8e378f070dae843e14263**. Une recherche textuelle de
`CVE-2022-23806`, `CVE-2020-26160`, `filebrowser`, `containerd` et `BuildKit`
dans les fichiers HTTP n’a pas trouvé de correspondance. **Cela ne prouve pas
qu’aucune règle n’existe ailleurs**, ni qu’une technique n’est pas couverte sous
un autre nom. Les signatures génériques de traversée et XSS sont présentes.

| Vulnérabilité / problème | Règle recherchée ou retenue | Ce que la règle détecte réellement | Test possible ? | Résultat / limite |
| --- | --- | --- | --- | --- |
| C01/C02 runtime / BuildKit | Aucune directe identifiée dans la recherche limitée | Les opérations sur socket Unix et les constructions locales ne sont pas visibles sur virbr0 | Pas de test d’exploitation prévu | Journaux runtime/build et audit hôte nécessaires ; flux sortant seul ne prouve pas la CVE |
| C03/C04 SSH | Piste : fréquence de connexions et métadonnées SSH, pas de signature CVE choisie | Ouvertures réseau, pas échecs de mot de passe ni commandes chiffrées | Contrôle normal possible ultérieurement | Authentification à corréler avec journald/auth.log ; pas d’alerte SSH nouvelle installée ici |
| C06 CUPS localhost | Aucune retenue | Pas de trafic direct du loopback VM sur virbr0 | Pas de réactivation du service | Défaut historique, service arrêté ; pas correctement détectable directement ici |
| C10/C12 application et image | Adaptation du SID 50500003 → local 1008001 | Motif encodé dans une URI envoyée à la VM:8080 ; ce n’est pas une preuve de faille File Browser | Oui, marqueur inerte en paramètre d’un GET | Configuration acceptée ; alerte 1008001 sur 8080 visible dans la capture ; HTTP en clair requis |
| C13 accès applicatif / répétition | Local 1008002, original | Cinq GET / de la même source en 10 secondes, pas cinq échecs d’authentification | Oui, cinq accès normaux | Seuil pédagogique, faux positif volontaire ; ne détecte pas un compte compromis à lui seul |
| Refus applicatifs liés aux accès | Local 1008003, original | Réponse HTTP 401 du service sur 8080, sans identification de l’utilisateur | Si un endpoint connu retourne 401 sans secret ; sinon conserver non déclenchée | /api/renew 401 a été vu au J7 ; ce n’est pas un mauvais mot de passe prouvé |
| CVE-2022-23806 initiale | Aucune retenue | Chemin d’appel et encodage attaquable non démontrés | Aucun exploit prévu | Symbole présent dans ancien Go insuffisant ; pas de signature correcte justifiable avec les données actuelles |

C13 et 8080 complètent les audits initiaux. Les défauts corrigés ne sont pas
réactivés pour cet exercice ; les exclusions CVE antérieures sont conservées.
Les quatre règles génériques J7 restent une preuve de détection de motifs
sur le serveur temporaire, pas une garantie de détection des CVE du conteneur.

## 2. Trois règles proposées et justification — 15 min

Règles **locales**, avec SID distincts des originaux. Vérifier leur absence
dans le jeu chargé avant installation. Le premier reprend la condition du
SID 50500003, en limitant direction, destination et port et en utilisant le
buffer HTTP moderne ; les deux autres sont des créations pédagogiques.

```suricata
alert http any any -> 192.168.122.229 8080 (msg:"AIS LAB motif encode vers File Browser"; flow:established,to_server; http.uri.raw; content:"%2e%2e"; nocase; classtype:web-application-attack; sid:1008001; rev:1;)
alert http any any -> 192.168.122.229 8080 (msg:"AIS LAB cinq GET racine en dix secondes"; flow:established,to_server; http.method; content:"GET"; bsize:3; http.uri; content:"/"; bsize:1; threshold:type threshold, track by_src, count 5, seconds 10; classtype:misc-activity; sid:1008002; rev:1;)
alert http 192.168.122.229 8080 -> any any (msg:"AIS LAB reponse HTTP 401 File Browser"; flow:established,to_client; http.stat_code; content:"401"; bsize:3; classtype:misc-activity; sid:1008003; rev:1;)
```

- **1008001 :** URI brute, motif insensible à la casse, HTTP reconnu et flux établi vers 8080. Un motif dans le corps ou uniquement dans une réponse ne correspond pas. HTTPS masque cette condition.
- **1008002 :** GET exact sur URI normalisée `/`, cinquième correspondance de la source dans la fenêtre. Une query, une autre méthode ou des ressources statiques ne satisfont pas ces conditions. Ce seuil doit être réglé après observation des usages ; une source partagée peut agréger plusieurs utilisateurs.
- **1008003 :** sens réponse, statut exact 401 ; ne distingue ni renouvellement de session, ni mauvais secret, ni attaque. L’alerte utilise l’IP serveur comme source : retrouver le client par le flux/destination.

Si les règles J7 larges sont conservées, 1008001 peut produire une alerte en
plus du SID 50500003. Documenter ce doublon avant de décider d’un retrait ou
réglage ; ne pas supprimer les originaux sans trace.

## 3. Installation et validation sur l’hôte — 15 min

Sauvegarder l’état actuel dans un nom daté unique et conserver le fichier
local précédent s’il existe. Créer `/etc/suricata/rules/ais-it8-adaptations.rules`
avec les trois lignes, puis ajouter son chemin au bloc `rule-files` existant.
Le fichier J7 peut encore s’appeler `ais-it8.rules` sur l’hôte : le renommage
des dossiers du mémo ne renomme pas une configuration déjà déployée.

```bash
sudoedit /etc/suricata/rules/ais-it8-adaptations.rules
sudoedit /etc/suricata/suricata.yaml
```

Entrée à **ajouter**, en conservant les fichiers déjà chargés :

```yaml
  - /etc/suricata/rules/ais-it8-adaptations.rules
```

```bash
sudo suricata -T -v -c /etc/suricata/suricata.yaml
echo "Code de retour : $?"
```

Vérifier code 0, absence de règles rejetées et présence des trois SID sans
collision. Si exactement quatre signatures J7 sont conservées, sept signatures
sont attendues ; ajuster ce nombre au jeu réellement chargé. **La capture
fournie montre deux fichiers traités, sept règles chargées, aucune règle
rejetée ou ignorée et un code de retour 0.** Cette validation a été exécutée
par le participant ; le contenu complet des fichiers n’est pas visible.
Corriger et retester avant tout redémarrage si la configuration change.

Après acceptation seulement :

```bash
sudo systemctl restart suricata
sudo systemctl status suricata --no-pager
```

## 4. Tests contrôlés et EVE — 20 min

Ouvrir sur l’hôte le suivi avant les essais :

```bash
sudo tail -n 0 -F /var/log/suricata/eve.json | jq --unbuffered -c '
  select(.event_type == "alert") |
  select(.alert.signature_id == 1008001 or
         .alert.signature_id == 1008002 or
         .alert.signature_id == 1008003) |
  {timestamp,flow_id,src_ip,src_port,dest_ip,dest_port,http,alert}'
```

Depuis l’hôte, avec capture sur virbr0 si nécessaire :

```bash
FB_BASE='http://192.168.122.229:8080'
# Motif inerte dans un paramètre, sans chemin vers fichier sensible.
curl --path-as-is --max-time 5 -o /dev/null "$FB_BASE/?ais_probe=%2e%2e"
# Série normale à faible volume, sans query.
for essai in 1 2 3 4 5; do
  curl --max-time 5 -o /dev/null -sS "$FB_BASE/"
  sleep 1
done
```

Attendre une alerte de motif puis une de fréquence si les conditions sont
remplies. Un test négatif consiste en GET `/` isolé, hors fenêtre contenant
les cinq précédents ; il ne doit pas satisfaire ces deux règles. Noter les
horaires : ne pas déclarer l’absence d’alerte à partir d’un suivi lancé trop tard.

Pour 1008003, utiliser uniquement un accès non authentifié à un endpoint
**déjà confirmé** retournant 401, ou observer un renouvellement 401 normal.
Ne pas envoyer de mauvais mots de passe en boucle ni publier de corps de login.
Si le serveur retourne 200/403/404, la condition 401 n’est pas remplie ; conserver
« non déclenchée » et préciser ce qu’il faudrait observer. Un serveur temporaire
retournant 401 validerait la syntaxe après adaptation de port, pas la règle
ciblée sur File Browser/8080.

| SID | Preuve attendue | État actuel |
| --- | --- | --- |
| 1008001 | Test accepté, URI brute visible, alerte sur 8080, contrôle négatif | Alarme 1008001 visible sur 8080 ; contrôle négatif non documenté |
| 1008002 | Cinq GET dans dix secondes, alerte et test sous seuil | Boucle de cinq GET visible ; aucune alerte 1008002 affichée dans cette capture, validation à compléter |
| 1008003 | Réponse effective 401, alerte corrélée ; absence sur autre statut | Aucune réponse 401 ni alerte 1008003 visible dans cette capture ; test à compléter |

## 5. Capture et résultat observé — 8 octobre 2026

![Validation de la configuration Suricata, service actif et alerte locale 1008001 vers File Browser](../../assets/img/securisation-avancee-infrastructures/it-8/Capture%20d’écran%20du%202026-10-08%2011-53-27.png)

*Capture fournie par le participant : sept signatures acceptées dans deux
fichiers, code de retour 0, puis service actif depuis 11:52:19. À droite,
le suivi de `eve.json` affiche une alerte de la règle locale 1008001.*

| Champ de l’événement visible | Valeur |
| --- | --- |
| Date et heure | `2026-10-08T11:53:20.484380+0200` |
| Identifiant du flux | `105860300332322` |
| Source | Hôte `192.168.122.1:55214` |
| Destination | VM `192.168.122.229:8080` |
| Requête | `GET /?ais_probe=%2e%2e`, HTTP/1.1, client curl/8.18.0 |
| Réponse HTTP | `200` |
| Signature | `1008001`, révision 1, « AIS LAB motif encode vers File Browser » |
| Action | `allowed` |

Cette alerte confirme la détection du marqueur encodé envoyé au service sur
8080. Le statut HTTP 200 ne prouve aucune exploitation : le test utilise un
paramètre inerte. L’action `allowed` ne constitue pas un blocage du trafic.

La boucle de cinq GET apparaît à gauche, mais aucune alerte 1008002 n’est
visible à droite. Cela ne suffit pas à conclure à une absence dans tout le
journal : rechercher ce SID dans le fichier complet, puis contrôler les URI,
les horaires et la règle effectivement chargée si nécessaire. La règle
1008003 nécessite une réponse 401 ; cette capture n’en montre aucune.

La capture illustre l’événement, mais ne remplace pas l’export de la ligne
JSON originale à conserver avec les preuves du test.

## 📦 Livrable et sources

Conserver recherche/commit, lien à chaque constat, original/adaptation/SID,
conditions, décision de pertinence, configuration testée, horaires, objet EVE
anonymisé et limite de chaque test. Une absence de signature pertinente est
une conclusion valable si chemin local, chiffrement ou applicabilité inconnue
empêchent la détection. Ne pas inventer des alertes ni confondre indicateur et
preuve d’exploitation. Aucun blocage ou correctif 8080 n’est acquis par l’IDS.

- [Règles de traversée du dépôt](https://github.com/daffainfo/suricata-rules/blob/main/http/web-attacks/path-traversal.rules)
- [Seuils Suricata 8.0.3](https://docs.suricata.io/en/suricata-8.0.3/rules/thresholding.html)
- [Buffers HTTP Suricata 8.0.3](https://docs.suricata.io/en/suricata-8.0.3/rules/http-keywords.html)
- [Besoins de détection](vulnerabilites-besoins-detection.md)
- [Preuves J7](../it-7/installer-tester-regles-suricata.md)
- [Retour à l’itération 8](index.md)
- [Retour au module](../README.md)
