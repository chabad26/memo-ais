# 1.8 — Atelier 8 | Activité optionnelle — Découvrir FUXA et la supervision industrielle

## Objectif et modalité

**Découvrir une interface HMI/SCADA et créer une visualisation simple du fonctionnement d’une installation.** Exploration individuelle ou en binôme.

L’écran peut utiliser des **valeurs de démonstration ou des éléments statiques** : aucune connexion au modèle frigorifique n’est nécessaire. La procédure s’applique à la VM Debian 13 sans interface graphique. **Trois captures utilisateur attestent désormais le conteneur en fonctionnement, l’éditeur accessible et une vue statique réalisée.** Aucune connexion au modèle frigorifique n’est attestée.

## 1 — Étudier la documentation

Lire `optional/OPENPLC_FUXA.md` dans le laboratoire fourni. Cette annexe présente une piste facultative, distincte du cœur Python testé.

FUXA fournit un environnement web de supervision et un éditeur de visualisations. Le projet annonce notamment Modbus RTU/TCP, OPC UA, MQTT, Siemens S7, BACnet IP et Ethernet/IP. Les possibilités incluent indicateurs, états, historiques et configuration d’alarmes. Les méthodes proposées comprennent conteneur, sources, paquet npm et distributions préconstruites. Le parcours ci-dessous retient le conteneur afin de séparer ses dépendances de celles de l’Editor OpenPLC. [Source : dépôt officiel FUXA, consulté le 26 octobre 2026](https://github.com/frangoteam/FUXA).

La documentation distingue une vue d’édition et une vue de consultation. Les rubriques **Devices and Tags**, **Bind Controls**, **Setup Alarms** et **Save/Load Project** permettent d’approfondir l’exploration. [Documentation officielle](https://frangoteam.github.io/FUXA/).

## 2 — Installer et démarrer dans la VM

### Vérifier les prérequis

Dans la session SSH de la VM :

```bash
cat /etc/os-release
uname -m
free -h
df -h /
command -v docker
```

Il faut un moteur de conteneurs fonctionnel, un accès au registre pour télécharger l’image, de l’espace disque et des ressources disponibles. Arrêter le processus de développement OpenPLC avec **Ctrl + C** dans son terminal si cet essai est terminé, afin de libérer ses ressources.

Si Docker n’est pas installé, Debian 13 fournit le paquet [docker.io](https://packages.debian.org/trixie/docker.io). Pour une VM ne disposant pas déjà d’une autre installation Docker :

```bash
sudo apt update
sudo apt install docker.io docker-cli
sudo systemctl enable --now docker
sudo docker version
```

Ne pas mélanger cette méthode avec une installation Docker déjà configurée depuis un autre dépôt. Les commandes suivantes utilisent `sudo` sans demander d’ajout au groupe Docker.

### Télécharger et lancer FUXA

La commande est adaptée de l’exemple officiel : publication du port **uniquement sur le bouclage de la VM**, avec stockage persistant.

```bash
sudo docker pull frangoteam/fuxa:latest
sudo docker image inspect frangoteam/fuxa:latest --format '{{json .RepoDigests}}'
sudo docker run -d --name fuxa-lab \
  -p 127.0.0.1:1881:1881 \
  -v fuxa_appdata:/usr/src/app/FUXA/server/_appdata \
  -v fuxa_db:/usr/src/app/FUXA/server/_db \
  -v fuxa_logs:/usr/src/app/FUXA/server/_logs \
  -v fuxa_images:/usr/src/app/FUXA/server/_images \
  frangoteam/fuxa:latest
```

`latest` est mobile : conserver le digest affiché et la version visible de FUXA pour identifier précisément l’essai. Les chemins des volumes et le port 1881 proviennent du [README officiel](https://github.com/frangoteam/FUXA#installing-and-running). Ne pas ajouter de redirection de port sur le routeur ou d’exposition publique.

Vérifier dans la VM :

```bash
sudo docker ps --filter name=fuxa-lab
sudo docker logs --tail 50 fuxa-lab
sudo docker port fuxa-lab
curl -I http://127.0.0.1:1881/
```

Si `curl` manque, l’installer avec `sudo apt install curl`. Le mapping attendu est **`1881/tcp -> 127.0.0.1:1881`**. Une réponse HTTP confirme le service web ; elle ne démontre pas encore qu’un écran fonctionne ou que des données industrielles sont reçues.

Si le conteneur existe déjà, le reprendre avec `sudo docker start fuxa-lab` au lieu de répéter `docker run` avec le même nom.

### Accéder depuis le poste graphique

Depuis **ton poste**, ouvrir le tunnel et conserver cette session :

```bash
ssh -N -L 127.0.0.1:1881:127.0.0.1:1881 oliv@192.168.122.106
```

Puis ouvrir dans le navigateur du poste :

```text
http://127.0.0.1:1881
```

Ici, **1881 = FUXA**, **18080 = supervision Python** et **1313 = serveur de développement OpenPLC**. Le transfert X11 n’est pas nécessaire pour consulter FUXA : son interface est web.

### Fin de session

Enregistrer le projet depuis l’application, puis arrêter si nécessaire :

```bash
sudo docker stop fuxa-lab
```

Les volumes persistent. Fermer le tunnel avec Ctrl + C dans son terminal sur le poste. Pour reprendre ultérieurement : démarrer le conteneur et réouvrir le tunnel. Aucun conteneur n’a été lancé automatiquement lors de la rédaction de cette fiche.

## 3 — Explorer et créer une vue simple

### Fonctions à repérer

| Fonction | À rechercher dans l’interface / documentation |
| --- | --- |
| Équipements et connexions | Configuration des sources de données et de leurs paramètres. |
| Variables, ou tags | Nom, type, adresse éventuelle, unité, valeur et qualité disponible. |
| Écrans de supervision | Création d’une vue et placement des objets graphiques. |
| Indicateurs et états | Valeurs numériques, textes, couleurs et liens vers les tags. |
| Alarmes | Conditions, affichage et opérations disponibles selon la configuration. |

Les intitulés exacts peuvent varier avec la version. Pour ce premier écran, utiliser les objets disponibles sans configurer de connexion industrielle.

### Proposition d’écran statique de démonstration

Créer une vue nommée **Chambre froide — Démonstration**. Ajouter le bandeau **« Valeurs de démonstration — aucune connexion au procédé »**, puis les quatre éléments demandés :

| Objet | Contenu proposé | Interprétation |
| --- | --- | --- |
| Indicateur de température | **4,2 °C** | Exemple statique, pas une mesure reçue. |
| Indication de consigne | **4,0 °C** | Exemple statique, sans écriture vers un contrôleur. |
| Voyant compresseur | **ARRÊT**, teinte neutre ou sombre | État illustratif ; ajouter du texte pour ne pas dépendre seulement de la couleur. |
| Voyant d’alarme | **AUCUNE ALARME**, teinte neutre | État illustratif ; ne prouve pas une condition d’alarme configurée et testée. |

Avec l’hystérésis initiale, un compresseur arrêté à 4,2 °C est possible selon l’état précédent. La valeur proposée sert seulement à construire une vue cohérente.

Enregistrer et ouvrir la vue de consultation pour vérifier lisibilité, unités, titres et états. Conserver une capture de l’édition et une de la visualisation. Si les objets sont ensuite liés à des tags de démonstration, préciser la source et les valeurs utilisées.

**Un voyant d’alarme dessiné n’est pas un mécanisme d’alarme testé.** Si une règle est explorée, consigner séparément sa condition, son déclenchement et sa disparition. L’activité autorise l’écran statique ; il n’est pas nécessaire de connecter le laboratoire pour la terminer.

## 4 — Faire le bilan : réponses

### 1. HMI et SCADA : quelle différence ?

Une **HMI/IHM** est l’interface par laquelle l’opérateur consulte et, selon ses droits, agit sur un équipement ou un procédé. Un **SCADA** organise une supervision et une acquisition de données plus larges : plusieurs équipements ou installations, alarmes et éventuellement historiques. Les fonctions peuvent se recouvrir : une IHM peut faire partie d’un SCADA. Le nom du logiciel ne suffit pas à décrire son périmètre réellement configuré.

### 2. Quel est le rôle des variables ?

Les variables relient une information nommée à son utilisation dans la vue : température, consigne, commande, défaut ou alarme. Leurs types, unités et éventuelles conversions permettent d’interpréter les données. Une valeur statique ou de démonstration doit rester identifiable ; une valeur affichée sans information sur sa source ne prouve pas qu’elle représente l’état actuel du procédé.

### 3. Quels protocoles permettraient de communiquer avec un automate ?

Selon les capacités des deux extrémités et les pilotes configurés : **Modbus TCP/RTU, OPC UA ou Siemens S7**, par exemple. Le fait qu’un protocole soit pris en charge par FUXA ne prouve pas que l’automate ciblé le propose. Pour le laboratoire Python fourni, le chemin envisagé est **Modbus TCP**, avec son sous-ensemble de fonctions implémenté.

### 4. Quelles informations pour connecter FUXA au modèle fourni ?

| Information | Valeur connue / point à confirmer |
| --- | --- |
| Serveur cible | Modèle Python, par défaut `127.0.0.1:15020` dans son propre environnement. |
| Point de vue réseau | Dans un conteneur, `127.0.0.1` désigne le conteneur, pas la VM. La publication HTTP de FUXA ne crée pas une liaison au serveur Modbus local de la VM. Un chemin adapté et limité au laboratoire devra être conçu. |
| Identifiant d’unité | 1 dans les exemples fournis. |
| Consigne | Holding register 0, lecture FC03 ; valeur entière ×0,1 pour obtenir les °C. Écriture FC06 uniquement si elle est explicitement autorisée. |
| Température | Input register 0, lecture FC04 ; valeur entière ×0,1. |
| Compresseur | Input register 1, lecture FC04 ; 0/1, commande simulée. |
| Alarme | Input register 2, lecture FC04 ; 0/1. |
| Porte, si utilisée | Coil 0, lecture FC01. |
| Adressage du pilote | Vérifier s’il attend une base 0 ou 1, sans addition automatique supposée. Commencer par une valeur connue. |
| Rythme et erreurs | Période de lecture, timeout, valeurs périmées et comportement de la vue à la perte de connexion à définir. |
| Autorité et sécurité | Identifier la source : Python ou futur OpenPLC ; commencer en lecture seule. Le prototype n’a pas d’authentification Modbus. |

Ces éléments préparent une connexion ultérieure. **Aucune lecture FUXA du modèle n’est attestée par cette fiche.**

### 5. Quels risques sur un réseau non maîtrisé ?

- Consultation non autorisée des informations de procédé et de son architecture.
- Modification d’écrans, de connexions, de variables ou de règles si les droits le permettent.
- Écriture de commandes ou de consignes, avec effet physique possible si la supervision dispose de ce chemin.
- Indisponibilité, affichage trompeur ou exploitation d’une vulnérabilité du service.
- Utilisation du serveur comme point de passage vers d’autres équipements accessibles.

Le périmètre du laboratoire doit rester limité ; contrôler les comptes et droits disponibles, les flux, la version et la traçabilité avant toute connexion réelle. Le tunnel SSH protège le chemin d’accès utilisé ici mais ne remplace pas une politique de droits applicative.

## Captures utilisateur — installation et visualisation réalisées

Les heures ci-dessous proviennent des noms des fichiers. Le journal de FUXA utilise des horodatages UTC suffixés `Z` : par exemple 13:41 UTC correspond à 14:41 en heure de Paris le 26 octobre 2026.

### 14:41:56 — Conteneur démarré, publication locale et réponse HTTP

![Conteneur démarré, publication locale et réponse HTTP](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2014-41-56.png)

La sortie de `docker ps` montre **fuxa-lab**, image **frangoteam/fuxa:latest**, état **Up** et publication **127.0.0.1:1881 → 1881/tcp**. Les logs annoncent **FUXA V.1.3.5-2968**, puis `FUXA started!`. `docker port` confirme le mapping de bouclage et `curl -I http://127.0.0.1:1881/` reçoit **HTTP/1.1 200 OK**. En bas de la capture, le terminal du poste montre la commande du tunnel SSH vers la VM. Ces éléments attestent le service actif et le chemin d’accès préparé ; le digest de l’image et les montages de volumes ne sont pas affichés.

### 14:45:33 — Éditeur accessible et vue MainView

![Éditeur accessible et vue MainView](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2014-45-33.png)

L’interface FUXA présente une vue **MainView** vide, la palette graphique, les contrôles et les outils d’enregistrement/visualisation. L’accès à l’éditeur est attesté. Aucun équipement, tag industriel ou flux Modbus n’est visible sur cette image.

### 14:50:32 — Écran statique terminé

![Écran statique terminé](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2014-50-32.png)

L’écran **Chambre froide démonstration** contient les quatre éléments demandés : température **4,2 °C**, consigne **4,0 °C**, compresseur **ARRÊT** avec voyant **gris**, alarme **AUCUNE** avec voyant bleu. La mention **« Valeurs statiques — aucune connexion au procédé »** est présente. Le gris rend l’état arrêté moins ambigu que le voyant vert de la première version partagée dans la conversation. Cette capture atteste la visualisation demandée ; elle ne prouve ni réception de mesures, ni commande d’actionneur, ni règle d’alarme fonctionnelle.

**Bilan :** le service FUXA fonctionne, l’interface est accessible et l’écran statique de découverte est réalisé. La connexion à un équipement n’était pas nécessaire à cet atelier. La sauvegarde/export puis la réouverture du projet ne sont pas démontrées par ces seules captures ; les conserver si une preuve de persistance est demandée.

## Éléments à conserver et statut

| Élément | État initial de la fiche |
| --- | --- |
| Méthode choisie | Conteneur dans la VM, accès web par tunnel SSH. |
| Image, digest, version et ressources finales | Image `frangoteam/fuxa:latest`, logs FUXA 1.3.5-2968 attestés. Digest, volumes et ressources finales à relever. |
| Conteneur démarré et publication locale vérifiée | Attestés : `Up`, mapping 127.0.0.1:1881 et HTTP 200. |
| Interface accessible et vue à quatre indicateurs | Attestées : éditeur MainView puis vue finale à quatre indicateurs. |
| Source des valeurs | Valeurs statiques explicitement signalées ; aucune réception de donnée industrielle attestée. |
| Connexion au modèle ou à OpenPLC | Non réalisée, non nécessaire à l’activité. |

Ressources : [projet FUXA](https://github.com/frangoteam/FUXA), [documentation officielle](https://frangoteam.github.io/FUXA/) et `optional/OPENPLC_FUXA.md`. Sources consultées le 26 octobre 2026.

[Retour à l’itération](index.md) · [Atelier précédent — OpenPLC](decouvrir-openplc.md)
