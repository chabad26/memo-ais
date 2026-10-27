# 1.7 — Atelier 7 | Activité optionnelle — Découvrir OpenPLC

## Objectif et modalité

**Découvrir un environnement de programmation d’automates industriels et comparer sa logique avec le contrôleur Python utilisé pendant la journée.** Exploration individuelle ou en binôme.

L’analyse documentaire est complétée par **neuf captures utilisateur** : environnement Debian, démarrage de l’Editor, saisie du ST et valeurs dans son débogueur. L’Editor est ouvert ; le déploiement sur un Runtime distinct et la connexion au modèle frigorifique ne sont pas attestés. Cette connexion n’est pas demandée pendant l’activité.

## 1 — Étudier la documentation

Depuis la racine du laboratoire `livrables/informatique-industrielle/it-1/ot-refrigeration-poc/` :

```bash
less optional/OPENPLC_FUXA.md
less optional/thermostat.st
```

L’annexe décrit des pistes facultatives, explicitement distinctes du cœur Python testé. Elle demande notamment de vérifier versions, correspondance des variables et boucle bidirectionnelle avant de présenter l’intégration comme opérationnelle. FUXA n’est pas requis pour cette découverte d’OpenPLC.

!!! info "Point de version vérifié le 26 octobre 2026"
    L’annexe locale parle d’une interface de gestion sur HTTPS 8443. Le [README officiel du Runtime v4](https://github.com/Autonomy-Logic/openplc-runtime#readme) précise qu’il s’agit d’une **API**, sans interface web comme en v3. L’Editor desktop se connecte au Runtime ; ouvrir cette adresse dans un navigateur n’est pas le test d’interface attendu en v4. Le fichier d’origine du laboratoire est conservé.

## 2 — Préparer l’installation et vérifier l’accès

### Distinguer les composants

| Élément | Utilité pour l’activité |
| --- | --- |
| **Editor** | Environnement dans lequel créer ou examiner le programme, préparer sa cible et accéder aux outils de compilation/déploiement disponibles. |
| **Runtime** | Environnement qui exécute le programme PLC et réalise les échanges avec les entrées/sorties configurées. |
| **Modèle Python** | Simulation frigorifique déjà utilisée ; elle n’est pas automatiquement reliée à OpenPLC. |

La documentation du [Runtime v4](https://github.com/Autonomy-Logic/openplc-runtime#readme) l’associe à l’Editor v4, avec une API HTTPS sur 8443 et un moteur d’exécution C/C++. Elle propose des méthodes conteneurisées et natives. Pour la voie native, elle indique notamment GCC, CMake ≥ 3.28 et Python ≥ 3.10. Choisir une paire compatible et consigner les versions exactes avant installation.

### Relever l’environnement cible

Sur la machine Linux utilisée pour ce TP :

```bash
cat /etc/os-release
uname -m
python3 --version
git --version
node --version
make --version
g++ --version
```

Si node manque :

```bash

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.8/install.sh | bash
\. "$HOME/.nvm/nvm.sh"
nvm install 22
node -v # Should print "v22.23.4".
npm -v # Should print "10.9.9".
```

Si g+ ou make manque :

```bash

sudo apt install build-essential python3
make --version
g++ --version
```

Ces sorties sont à recueillir sur **la machine de l’apprenant** ; aucune distribution ou architecture n’est supposée ici. Vérifier ensuite dans la documentation de la version retenue les dépendances, l’affichage graphique et, pour une installation conteneurisée, le moteur de conteneurs disponible.

### Parcours de découverte de l’Editor

Consulter les [versions publiées de l’Editor](https://github.com/Autonomy-Logic/openplc-editor/releases) et choisir un paquet compatible avec le système, l’architecture et le Runtime retenu, s’il est disponible. Noter son numéro et suivre ses instructions d’installation.

À défaut, le [README de l’Editor](https://github.com/Autonomy-Logic/openplc-editor#readme), consulté le 26 octobre 2026, documente un lancement **de développement**, avec Git, accès réseau et Node.js **≥22 et <24** :

```bash
git clone https://github.com/Autonomy-Logic/openplc-editor.git
cd openplc-editor
git rev-parse HEAD
npm install
npm run dev
```

Cette séquence suit la branche obtenue au clonage : le commit affiché sert à identifier l’essai, pas à affirmer sa stabilité. Pour un essai reproductible, sélectionner une révision compatible documentée avant l’installation des dépendances. Ce parcours développeur n’est pas présenté comme une installation validée sur votre machine.

**Contrôle attendu :** l’application Editor s’ouvre et permet de créer ou examiner un projet. Une fenêtre ouverte ne prouve pas encore que le programme ST compile ou s’exécute.

### Vérifier et installer les dépendances graphiques — Debian 13

Après l’installation des dépendances npm, depuis le dossier `openplc-editor`, vérifier les bibliothèques requises par le binaire Electron :

```bash
ldd node_modules/electron/dist/electron | grep 'not found'
```

Chaque ligne `not found` indique une bibliothèque introuvable. **Aucune sortie signifie qu’aucune bibliothèque manquante n’est détectée par ce contrôle** ; cela ne garantit pas encore le lancement complet de l’Editor. Si le fichier `electron` lui-même est absent, reprendre le diagnostic de `npm install` avant ce contrôle.

Sur la VM Debian 13, les journaux ont montré des bibliothèques NSS, GTK, ATK, CUPS, audio et d’affichage manquantes. Installer les paquets correspondants :

```bash
sudo apt update
sudo apt install libnss3 libatk1.0-0t64 libatk-bridge2.0-0t64 \
  libcups2t64 libgtk-3-0t64 libpango-1.0-0 libcairo2 \
  libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
  libgbm1 libxkbcommon0 libasound2t64 libatspi2.0-0t64
```

APT résout les dépendances de ces paquets ; certains peuvent donc déjà être installés par un autre paquet de la liste. Les noms ci-dessus sont destinés à **Debian 13**, notamment les variantes `t64`.

Relancer ensuite le même contrôle :

```bash
ldd node_modules/electron/dist/electron | grep 'not found'
```

Si une ligne reste présente, conserver son nom exact pour identifier le paquet correspondant. Ne pas copier arbitrairement un fichier `.so` depuis une autre distribution.

Références Debian : [NSS](https://packages.debian.org/trixie/amd64/libnss3/filelist), [GTK](https://packages.debian.org/trixie/libgtk-3-0t64), [ATK bridge](https://packages.debian.org/trixie/libatk-bridge2.0-0t64), [CUPS](https://packages.debian.org/trixie/libcups2t64), [ALSA](https://packages.debian.org/trixie/libasound2t64).

**Vérifications distinctes avant de relancer :** ces paquets corrigent les bibliothèques manquantes. Ils ne corrigent ni l’absence d’affichage graphique (`echo "$DISPLAY"` vide dans la session SSH observée), ni la limite mémoire atteinte par Webpack sur la VM de 2 Go. Le serveur web de développement sur 1313 ne remplace pas à lui seul la fenêtre Electron.

### Si le Runtime est également installé

Suivre la méthode de la version retenue dans les [instructions officielles du Runtime](https://github.com/Autonomy-Logic/openplc-runtime#quick-start). Conserver les versions, la méthode, les messages et les paramètres d’écoute. Pour un laboratoire local, prévoir un accès de gestion limité au périmètre de test.

En v4, vérifier la connexion depuis l’Editor avec l’adresse et les identifiants configurés. Distinguer **service démarré**, **connexion authentifiée**, **programme compilé** et **programme en exécution**. Le port d’API ne démontre ni l’activation de Modbus ni le mapping des variables du thermostat.

### Journal d’installation à compléter

| Point | Résultat réel / preuve à noter |
| --- | --- |
| Distribution, version et architecture | Capture : Debian GNU/Linux 13, `DEBIAN_VERSION_FULL=13.7`, x86_64 ; Python 3.13.5, Git 2.47.3. |
| Editor : version ou commit, méthode et interface ouverte | Journal de lancement : `open-plc-editor@4.3.2`, `npm run dev` ; fenêtre graphique attestée. Commit exact à conserver. |
| Runtime, s’il est installé : version, méthode et connexion | À documenter ; facultatif selon le parcours choisi. |
| Difficulté rencontrée, message exact, cause et solution vérifiée | Échanges de dépannage : Node 24 incompatible, compilation native, bibliothèques absentes et limite mémoire. Ouverture finale attestée ; toutes les corrections et ressources finales ne sont pas capturées. |
| Projet créé, validation syntaxique, compilation ou exécution | Projet `RefrigerationThermostat`, programme ST `main` et valeurs de débogage visibles. Pas de journal de compilation/déploiement sur Runtime distinct fourni. |

## 3 — Examiner le programme fourni

Extrait de `optional/thermostat.st` :

```iecst
PROGRAM RefrigerationThermostat
VAR
    Temperature : REAL := 5.0;
    Setpoint : REAL := 4.0;
    SensorFault : BOOL := FALSE;
    Compressor : BOOL := FALSE;
    HighTemperature : BOOL := FALSE;
END_VAR
IF SensorFault THEN
    Compressor := FALSE;
ELSIF Temperature >= Setpoint + 0.5 THEN
    Compressor := TRUE;
ELSIF Temperature <= Setpoint - 0.5 THEN
    Compressor := FALSE;
END_IF;
HighTemperature := Temperature > 8.0;
END_PROGRAM
```

### Variables et décisions

| Élément | Structured Text | Correspondance Python |
| --- | --- | --- |
| Température | `Temperature : REAL := 5.0` | `self.temp`, température simulée. |
| Consigne | `Setpoint : REAL := 4.0` | `self.setpoint`. |
| Défaut capteur | `SensorFault : BOOL := FALSE` | `self.sensor_fault`. |
| Commande compresseur | `Compressor : BOOL := FALSE` | `self.compressor`. |
| Démarrage | `Temperature >= Setpoint + 0.5` | Même seuil dans le modèle initial. |
| Arrêt | `Temperature <= Setpoint - 0.5` | Même seuil dans le modèle initial. |
| Entre les seuils | Aucune réaffectation | Conservation de l’état précédent. |
| Défaut actif | `Compressor := FALSE` avant les seuils | Même priorité pédagogique à l’arrêt. |

`REAL` représente ici une grandeur numérique réelle ; `BOOL` un état vrai/faux. `:=` affecte une valeur, tandis que `IF / ELSIF / END_IF` expriment les branches de décision. L’extrait est en **Structured Text (ST)**, pas en Python ni en Ladder.

### Différences à ne pas masquer

- **Mode automatique :** le Python conditionne l’hystérésis à `self.automatic`. Le ST fourni n’a pas cette variable ni cette condition.
- **Alarme :** `HighTemperature := Temperature > 8.0` active immédiatement ce booléen au-dessus de 8 °C. Le Python exige **10 secondes** au-dessus du seuil. Une temporisation adaptée au cycle serait nécessaire pour reproduire ce comportement.
- **Physique :** le ST ne calcule pas le réchauffement, le refroidissement ou la porte. Sans alimentation externe de `Temperature`, sa valeur initiale ne devient pas une mesure dynamique du modèle.
- **Entrées/sorties :** les variables fournies n’ont pas de mapping matériel ou Modbus explicite. Leur nom seul ne crée pas une liaison vers Python ou la supervision.
- **Version des seuils :** le ST correspond à **±0,5 °C**, pas à la variante ±1 °C de l’atelier 1.5. La restauration du Python doit encore être confirmée pour comparer les mêmes règles.

**Bilan :** l’hystérésis et la priorité au défaut sont comparables, mais le fichier ST n’est pas un remplacement fonctionnel complet du laboratoire.

### Explorer dans l’Editor, si l’installation le permet

Créer un projet pour la cible et la version retenues. Reprendre ou adapter les déclarations et le corps du programme selon le format accepté, puis utiliser la validation proposée par l’éditeur. Si nécessaire, configurer une tâche cyclique et une instance du programme selon le projet cible.

Ne pas déduire de la présence du fichier `.st` qu’il constitue un projet directement déployable. Conserver les adaptations et erreurs éventuelles. Une validation syntaxique ne prouve pas la correspondance des entrées/sorties ni une boucle de régulation fermée.

## 4 — Faire le bilan : réponses

### 1. Programme PLC et application Python : quelles différences ?

Le programme PLC exprime la commande dans un langage et un projet destinés à une cible d’automatisation, avec tâches, cycle et entrées/sorties à configurer. Une application Python peut organiser librement ses appels, ses données et ses communications ; dans notre laboratoire, elle regroupe aussi physique, contrôleur et serveur.

Les deux peuvent conserver un état et exprimer une hystérésis. Le langage seul ne garantit ni temps réel, ni sûreté, ni adéquation au procédé : il faut examiner l’environnement d’exécution, le cycle, les interfaces et les validations.

### 2. Quel est le rôle du Runtime ?

Exécuter le programme préparé pour la cible, gérer son cycle et relier ses variables aux interfaces configurées. Il est distinct de l’Editor, utilisé pour élaborer et piloter le déploiement. Sa présence n’injecte pas automatiquement la température du modèle Python dans `Temperature`.

### 3. Comment communiquer avec équipements et supervision ?

Par des entrées/sorties physiques ou des interfaces réseau prises en charge et configurées, par exemple Modbus TCP dans la piste du laboratoire. Il faut définir pour chaque variable le sens, le type, l’unité, l’adresse et le rythme d’échange, puis contrôler les droits et les réactions aux erreurs. La compatibilité de protocole ne suffit pas à rendre deux tables de registres équivalentes.

### 4. Quelles étapes pour connecter OpenPLC au modèle frigorifique ?

| Étape à concevoir | Résultat à vérifier |
| --- | --- |
| Séparer la physique du contrôleur Python | Une seule autorité commande le compresseur ; éviter que Python et OpenPLC se contredisent. Le mode `auto=0` ne suffit pas à créer une entrée distante de commande absente du modèle actuel. |
| Alimenter les entrées OpenPLC | Température, consigne et défaut reçus avec types, unités et correspondances validés. |
| Récupérer la sortie de commande | `Compressor` appliqué au modèle thermique par une interface à concevoir ; l’état compresseur du serveur Python actuel est en lecture seule par Modbus. |
| Compléter la logique | Décider des fonctions nécessaires : mode automatique, alarme temporisée, état initial et réactions aux communications perdues. |
| Configurer les échanges | Rôles client/serveur, plugin disponible, interfaces, adresses, ports et période de mise à jour explicités. |
| Relier la supervision à la bonne source | Éviter qu’elle continue à lire un ancien contrôle Python sans rapport avec le programme OpenPLC. |
| Tester la boucle fermée | Mesure → décision OpenPLC → commande → évolution physique → nouvelle mesure, puis essais de défaut et perte de liaison. |

Cette connexion reste **à concevoir et à tester** ; elle n’est pas réalisée pendant l’activité et aucune intégration OpenPLC/FUXA n’est présentée comme acquise.

## Captures utilisateur — environnement, Editor et essais ST

Les heures proviennent des noms des images. Les captures de débogage montrent des valeurs configurées et affichées, pas une évolution thermique produite par le modèle Python. Le tableau des variables montre des changements de **valeur initiale** : on ne déduit donc pas que l’état est resté continu entre les essais.

### 13:34:38 — Environnement de la VM

![Environnement de la VM](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2013-34-38.png)

Les commandes affichent **Debian GNU/Linux 13 (trixie)**, `DEBIAN_VERSION_FULL=13.7`, **x86_64**, **Python 3.13.5** et **Git 2.47.3**. La configuration annoncée pendant la préparation est 2 vCPU, 2 Go de RAM et 20 Go de disque ; ces ressources ne sont pas mesurées sur cette capture.

### 13:36:29 — Version Node initialement incompatible

![Version Node initialement incompatible](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2013-36-29.png)

La capture montre **Node v24.22.1** et **npm 11.19.1**, avant correction. Le journal transmis ensuite dans la conversation atteste **Node v22.23.4** et **npm 10.9.9**. Il ne faut pas utiliser cette image comme preuve d’une installation réussie avec Node 24.

### 14:06:25 — Fenêtre OpenPLC Editor ouverte

![Fenêtre OpenPLC Editor ouverte](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2014-06-25.png)

La fenêtre native de l’Editor affiche l’accueil, **New Project**, **Open** et les projets locaux. Son ouverture est attestée ; aucun Runtime connecté ni projet déployé n’est visible.

### 14:07:01 — Lancement de l’Editor depuis les sources

![Lancement de l’Editor depuis les sources](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2014-07-01.png)

Le terminal montre `npm run dev`, **open-plc-editor@4.3.2**, le serveur de développement sur **1313** et le lancement d’Electron. Plusieurs avertissements restent présents (GTK canberra, extension de développement, Browserslist, configuration Tailwind et messages Electron). La fenêtre précédente atteste l’ouverture malgré ces messages ; cette image ne prouve pas leur correction ni une absence d’erreur ultérieure.

### 14:20:55 — Projet et saisie du programme ST

![Projet et saisie du programme ST](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2014-20-55.png)

Le projet **RefrigerationThermostat** contient le programme **main** en Structured Text, avec hystérésis ±0,5 °C et comparaison d’alarme `Temperature > 8.0`. Le tableau de variables est encore vide, des noms sont soulignés et l’onglet porte un astérisque : c’est une étape de saisie, pas une preuve de validation.

### 14:23:44 — Débogueur : température 5 °C

![Débogueur : température 5 °C](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2014-23-44.png)

Les variables visibles du tableau sont locales : `Temperature`, **REAL**, initialisée à **5.0**, et `Setpoint`, **REAL**, initialisée à **4.0**. Les valeurs en ligne indiquent **SensorFault=FALSE**, **Compressor=TRUE**, **HighTemperature=FALSE**. Cet état est cohérent avec le dépassement du seuil haut de 4,5 °C. Les déclarations des trois booléens ne sont pas toutes visibles dans la portion du tableau affichée.

### 14:26:33 — Débogueur : température 4,2 °C

![Débogueur : température 4,2 °C](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2014-26-33.png)

La valeur initiale affichée de `Temperature` est **4.2** ; les valeurs en ligne montrent **Compressor=FALSE**, défaut inactif et alarme inactive. À 4,2 °C, on est dans la bande d’hystérésis : un état arrêté est possible. Cette capture ne démontre pas un passage continu depuis le précédent état à 5 °C ; si la simulation a été réinitialisée, le compresseur peut repartir de sa valeur initiale `FALSE`.

### 14:31:29 — Débogueur : température 3,2 °C

![Débogueur : température 3,2 °C](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2014-31-29.png)

La température configurée et affichée vaut **3.2 °C**, la consigne **4 °C**, le défaut est inactif, **Compressor=FALSE** et l’alarme inactive. L’état est cohérent avec la condition d’arrêt **T ≤ 3,5 °C** ; l’instant de transition depuis un état en marche n’est pas enregistré.

### 14:32:13 — Débogueur : température 9 °C et alarme

![Débogueur : température 9 °C et alarme](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2014-32-13.png)

La température configurée et affichée vaut **9 °C**, la consigne **4 °C**, le défaut est inactif, **Compressor=TRUE** et **HighTemperature=TRUE**. Les deux états correspondent aux comparaisons du ST. L’alarme de cet exemple est une comparaison immédiate à 8 °C ; la temporisation Python de 10 secondes n’est pas présente.

### Bilan des preuves

| Établi par les éléments fournis | Limite / complément attendu |
| --- | --- |
| Editor graphique ouvert et projet ST créé | L’installation détaillée et le commit final restent à consigner. |
| Débogueur avec valeurs à 5, 4,2, 3,2 et 9 °C | États cohérents avec la logique ; pas de courbe thermique ni de cycle physique fermé. |
| Compresseur actif au-dessus du seuil haut, arrêté sous le seuil bas | Pas de séquence continue capturée prouvant les deux états possibles à une même température dans la bande. |
| Alarme affichée active à 9 °C | Aucune temporisation de 10 s dans ce ST. |
| Défaut affiché inactif pendant ces essais | Essai ST avec `SensorFault=TRUE` non capturé ; les preuves de défaut Python de l’atelier 1.4 restent distinctes. |
| Programme repris dans l’Editor | Aucun déploiement sur un Runtime distinct, mapping Modbus ni liaison au modèle Python attesté. |

L’apprenant confirme devoir **arrêter le programme pour modifier le tableau des valeurs initiales**. Cette méthode ne permet pas de réaliser la séquence continue proposée précédemment : chaque relancement peut réinitialiser le compresseur. Les essais séparés et la lecture du code suffisent à cette découverte optionnelle ; la conservation d’état entre deux températures n’est pas revendiquée comme testée. Aucun essai supplémentaire n’est requis pour terminer cette activité.

## Éléments à conserver

- Versions et environnement réellement utilisés, méthode d’installation et difficultés résolues.
- Capture de l’Editor et, si utilisé, preuve de connexion au Runtime.
- Extrait ST annoté et comparaison des seuils, du défaut et de l’alarme.
- Adaptations apportées et résultat exact : examen, validation, compilation ou exécution.

## Ressources et état des vérifications

- `optional/OPENPLC_FUXA.md` et `optional/thermostat.st` : lus dans le laboratoire fourni.
- [OpenPLC — site du projet](https://www.openplcproject.com/) : lien fourni ; consultation automatique en échec lors de cette vérification.
- [OpenPLC Runtime — dépôt officiel et README](https://github.com/Autonomy-Logic/openplc-runtime) : consulté le 26 octobre 2026.
- [OpenPLC Editor — dépôt officiel et README](https://github.com/Autonomy-Logic/openplc-editor) : consulté le 26 octobre 2026.

**État :** étude documentaire, ouverture de l’Editor, projet ST et états du débogueur documentés par neuf captures. Test continu d’hystérésis, défaut ST et déploiement sur Runtime distinct non attestés ; intégration au modèle Python non réalisée.

[Retour à l’itération](index.md) · [Atelier précédent — Préparer le jumeau numérique](preparer-jumeau-numerique.md)
