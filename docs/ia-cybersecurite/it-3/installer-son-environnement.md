# Installer son environnement

**45 min — Présentiel**

## Le problème à résoudre

Nadia demande un traitement chez Hexalp, sans envoi des journaux à un service externe et sans blocage automatique. L'environnement Python doit être **isolé des dépendances du système, documenté et accessible uniquement localement**. JupyterLab exécute du code par cellules dans des notebooks `.ipynb` et affiche leurs résultats.

**Support retenu : une VM Linux de TP**, à créer ou à réutiliser. Cette fiche associe la procédure, les réponses théoriques et les captures fournies le 21 octobre 2026. Celles-ci attestent un environnement partiellement vérifié ; les contrôles non montrés restent à compléter. Les commandes sont à exécuter une par une, après lecture des sorties.

## Mission 1 — Installer

### 1. Préparer et copier le kit

Dans la VM, utiliser un compte non privilégié et un dossier personnel. Les cinq fichiers sources du kit sont dans le dépôt, sous **`livrables/ia-cybersecurite/it-3/ia01-j3/`**. Le carnet commencé peut être copié avec eux. Copier les fichiers par le moyen disponible sur l'hyperviseur ou par SSH ; **ne pas copier un environnement `.venv` d'une autre machine**.

```bash
mkdir -p ~/ia01-j3
cd ~/ia01-j3
ls -la
python3 --version
```

Vérifier la présence de `requirements.txt`, `hexalp_ssh_sept2026.csv`, `00_python_survie.ipynb`, `01_detection_ssh.ipynb` et `detection_ssh_squelette.py`. Le kit annonce Python **3.11 ou plus récent** ; cela ne garantit pas que toutes les versions figées acceptent chaque version de Python : l'installation devra le confirmer.

### 2. Créer l'environnement et installer les dépendances

```bash
python3 -m venv .venv
```

**Uniquement si l'échec indique un module venv/ensurepip absent**, sur une VM Debian/Ubuntu :

```bash
sudo apt install python3-venv
python3 -m venv .venv
```

Un autre message d'erreur demande une autre correction : ne pas attribuer systématiquement l'échec à ce paquet. Si les index APT sont absents ou obsolètes, les actualiser avant l'installation. Pour un Python installé séparément, le paquet venv doit correspondre à cet interpréteur.

```bash
source .venv/bin/activate
python -m pip --version
python -m pip install -r requirements.txt
python -m pip install --upgrade pip
python -m pip check
```

`python -m pip` cible le pip de l'interpréteur actif. L'ordre reprend le kit ; si l'installation échoue à cause d'un pip ancien, mettre pip à jour **dans le venv** puis relancer l'installation et noter cette adaptation. Ne pas supprimer les versions demandées pour masquer un échec : conserver le message et vérifier la version de Python, l'index, la disponibilité des paquets et la compatibilité.

Le téléchargement des dépendances nécessite normalement une connexion au dépôt de paquets. **Cela ne doit pas envoyer les journaux SSH.** Si l'environnement doit être totalement hors ligne, préparer les distributions et toutes leurs dépendances sur un poste autorisé, puis installer depuis un dépôt local contrôlé. Un venv ne bloque pas les communications réseau.

### 3. Lancer JupyterLab sur la boucle locale

```bash
jupyter lab --no-browser --ip=127.0.0.1 --port=8888 --ServerApp.port_retries=0
```

L'option supplémentaire `port_retries=0` évite de passer silencieusement à 8889 si 8888 est déjà occupé. Garder le terminal ouvert. L'URL affichée ressemble à `http://127.0.0.1:8888/lab?token=[CAVIARDÉ]` ; le jeton réel reste privé et ne doit figurer ni dans le carnet partagé, ni dans une capture publiée, ni dans Git. Vérifier qu'une ancienne configuration ne désactive pas l'authentification.

**VM avec interface graphique :** ouvrir l'URL affichée dans le navigateur **de la VM**. `127.0.0.1` désigne la machine où s'exécute le navigateur, pas automatiquement la VM depuis le poste hôte.

### Retrouver le jeton sur la page de connexion

Si Jupyter affiche **« Password or token »**, ouvrir un **second terminal dans la VM**, avec le même utilisateur que celui qui a lancé Jupyter :

```bash
source ~/ia01-j3/.venv/bin/activate
jupyter server list
```

La commande affiche les serveurs en cours et leurs URL, par exemple :

```text
http://127.0.0.1:8888/?token=[JETON_PRIVÉ] :: /chemin/ia01-j3
```

Copier **uniquement la valeur après `token=`**, sans les informations qui suivent l'URL, dans le champ **« Password or token »**, puis cliquer sur **Log in**. Le jeton figure aussi dans le terminal de lancement de Jupyter. Il n'est pas nécessaire de remplir la section de création d'un mot de passe pour se connecter avec ce jeton.

**Ne pas partager la sortie brute de `jupyter server list`** : elle contient le secret d'accès. Dans le carnet ou une capture, remplacer sa valeur par `[CAVIARDÉ]`. Avec un tunnel SSH, utiliser l'adresse et le port locaux du poste tout en conservant le jeton du serveur de la VM.

### 4. VM sans interface graphique — Tunnel SSH

Prérequis : accès SSH fonctionnel à la VM, avec vérification de son identité. Depuis un terminal **du poste hôte**, remplacer les valeurs d'exemple :

```bash
ssh -N -o ExitOnForwardFailure=yes -L 127.0.0.1:8888:127.0.0.1:8888 utilisateur@ADRESSE_VM
```

Puis ouvrir sur le poste hôte `http://127.0.0.1:8888/lab` et saisir le jeton de la VM. Conserver le tunnel ouvert. Si le port local 8888 est occupé, utiliser `127.0.0.1:8889:127.0.0.1:8888` et ouvrir le port **8889** côté poste ; Jupyter reste sur **8888 dans la VM**.

Le réseau doit permettre SSH vers la VM : avec un NAT sans accès direct depuis l'hôte, utiliser le mécanisme d'accès privé de l'hyperviseur ou une redirection SSH liée à la boucle locale du poste. **Ne pas ouvrir le port Jupyter de la VM ni le rediriger directement vers le réseau.** Le tunnel chiffre le transport ; il ne remplace pas l'authentification Jupyter.

### 5. Vérifier le notebook et conserver la preuve

Ouvrir `00_python_survie.ipynb` et exécuter **la première cellule de code**, pas toutes les cellules : certaines erreurs des exercices suivants sont intentionnelles. Elle affiche Python, pandas, scikit-learn, matplotlib et `sys.prefix`.

| Point à relever | Résultat attendu — à distinguer du résultat réel |
| --- | --- |
| Python | Version effectivement installée et compatible avec les paquets |
| pandas / scikit-learn / matplotlib | Versions installées, à comparer au fichier du kit |
| `sys.prefix` | Chemin de l'environnement `~/ia01-j3/.venv`, avec le chemin personnel développé |
| Cohérence des dépendances | Sortie de `python -m pip check` sans incompatibilité signalée |
| Écoute réseau | Jupyter en écoute sur `127.0.0.1:8888`, pas sur toutes les interfaces |

Copier les **sorties réellement obtenues** dans `carnet_J3.md`, en caviardant les secrets. Aucun numéro de version installé n'est rempli par anticipation.

Dans un nouveau terminal, réactiver `source ~/ia01-j3/.venv/bin/activate`. Pour sortir : `deactivate`. Pour arrêter Jupyter, utiliser `Ctrl+C` dans son terminal et confirmer si demandé ; fermer également le tunnel SSH. Sortir du venv ne stoppe pas un serveur déjà lancé.

## Mission 2 — Les questions de l'administrateur

### 1. Pourquoi un venv ? Que prévoit PEP 668 ?

Un venv sépare les bibliothèques du projet de celles gérées par le système, sans `sudo pip install`. Cela limite les conflits de versions et les modifications des fichiers gérés par APT. **Ce n'est pas un bac à sable de sécurité** : le code garde les droits de l'utilisateur, l'accès à ses fichiers et au réseau. [Python — venv](https://docs.python.org/fr/3/library/venv.html).

La **PEP 668** permet de marquer un Python système comme géré extérieurement. Sur les distributions concernées, pip refuse normalement d'y installer un paquet et affiche une erreur de type `externally-managed-environment`, orientant vers un venv. Ce message n'est pas universel : il dépend du Python et de sa distribution. [PEP 668](https://peps.python.org/pep-0668/).

Pour examiner le comportement sans installer réellement pandas dans Python système, utiliser un **second terminal hors venv** :

```bash
python3 -m pip install --dry-run pandas
```

Relever le résultat. Si le Python n'est pas marqué ou si pip manque, la réponse sera différente ; ne pas inventer l'erreur PEP 668. Le kit propose `pip install pandas` hors venv : son exécution peut réellement installer si le système ne la bloque pas. La variante `--dry-run` permet ici l'observation sans modification du Python système. Ne pas contourner le refus par `--break-system-packages` ou `sudo pip`.

### 2. Pourquoi figer les versions ? Quelles limites et quels hachages ?

Le fichier du kit fixe les **quatre dépendances directes**, ce qui réduit les variations. Il ne fige pas toutes les dépendances transitives, Python, l'OS, les binaires ou la version de pip, et ne garantit ni disponibilité future, ni absence de vulnérabilité, ni absence de code malveillant. La mise à jour non figée de pip doit aussi être documentée. « Versions figées = résultats identiques partout » serait trop fort.

L'option **`--require-hashes`** de pip exige les hachages attendus des distributions et un ensemble de dépendances correctement figé. Elle contrôle les octets téléchargés par rapport à des valeurs approuvées ; elle ne prouve pas que le logiciel est sûr. Le fichier actuel n'a pas ces hachages : ajouter simplement cette option fera échouer l'installation. Il faut préparer un fichier complet, y compris les dépendances transitives et les variantes de distributions autorisées, depuis une source de confiance. [pip — Secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/).

### 3. Pourquoi `pip install sklearn` échoue-t-il ?

Dans le venv de TP, le kit propose :

```bash
python -m pip install sklearn
```

**Résultat attendu, non encore observé dans la VM :** le paquet relais `sklearn` est déprécié et son installation récente échoue volontairement en demandant d'utiliser **`scikit-learn`**. La bibliothèque réelle s'installe sous ce nom et s'importe avec `import sklearn`. Ne pas activer le contournement de dépréciation pour ce TP.

Les mainteneurs conservent le nom pour empêcher qu'un acteur malveillant profite de la confusion entre nom d'import et nom de distribution. Le lien avec le **slopsquatting** est la confiance accordée à un nom de paquet proposé ou supposé : vérifier son existence et ses mainteneurs avant installation, même si un assistant le recommande. Le cas `sklearn` est une réservation défensive d'un alias connu, pas la preuve d'un paquet halluciné. [Page officielle du paquet sur PyPI](https://pypi.org/project/sklearn/).

### 4. Sur quelle adresse écoute Jupyter ? Que protège le jeton ?

Dans un second terminal **de la VM**, conserver la commande du kit :

```bash
ss -tlnp | grep 8888
```

Ou filtrer précisément le port avec `ss` :

```bash
ss -ltnp 'sport = :8888'
```

**Attendu :** une écoute `127.0.0.1:8888`. La visibilité du nom de processus dépend des droits. Relever la sortie réelle : une URL affichée ne remplace pas cette vérification. Le jeton authentifie l'accès au serveur qui permet l'exécution de code avec les droits de son utilisateur. Il ne chiffre pas HTTP, ne remplace pas la limitation réseau et ne protège pas contre le code malveillant déjà exécuté dans un notebook. [Jupyter — sécurité du serveur](https://jupyter-server.readthedocs.io/en/latest/operators/security.html).

### 5. Pourquoi ne pas exposer Jupyter sans authentification ? Qubitstrike

Une écoute sur toutes les interfaces permet une accessibilité au-delà de la boucle locale si le réseau et le pare-feu l'autorisent. Sans jeton **ni autre authentification**, un tiers joignant Jupyter pourrait exécuter du code, lire/modifier les fichiers accessibles et utiliser les ressources de la VM. L'accès initial donne les droits du processus Jupyter, pas automatiquement ceux de root.

**Qubitstrike, documentée en octobre 2023**, a visé des instances Jupyter exposées et mal configurées. Cado rapporte l'utilisation de leur terminal pour exécuter des charges malveillantes et rechercher des identifiants cloud ; la campagne illustre le risque d'accès au système via un outil de travail. Référence primaire : [Cado Security — bilan H2 2023](https://www.cadosecurity.com/blog/key-findings-cado-security-labs-h2-2023-cloud-threat-findings-report). La [ressource BleepingComputer du kit](https://www.bleepingcomputer.com/news/security/qubitstrike-attacks-rootkit-jupyter-linux-servers-to-steal-credentials/) fournit le récit de la campagne, notamment minage et dissimulation.

**Aucun test d'exposition n'est nécessaire :** garder boucle locale, authentification, compte non privilégié et tunnel SSH si besoin. Ne jamais lancer pour ce TP Jupyter sur toutes les interfaces ou sans authentification.

### 6. Comparaison avec le script de Sofia

| Point | Script de Sofia — J2, P6 | Environnement Jupyter prévu pour J3 |
| --- | --- | --- |
| **Exécution** | Script sur serveur de supervision ; appel d'un modèle distant | Python et calcul des modèles dans la VM |
| **Données** | Alertes internes envoyées à l'API externe, résumé vers Teams | CSV fictif conservé et traité localement ; vérifier le code et les extensions pour ne pas créer d'envoi |
| **Secrets** | Clé API sur compte personnel et mot de passe SQL écrits dans le script | Aucune clé de fournisseur IA nécessaire ; jeton Jupyter local et accès SSH à protéger |
| **Maîtrise** | Projet personnel, intégration récurrente et gestion des accès mal documentée | Venv et dépendances documentés, lancement explicite, écoute locale, travail sous compte de TP |
| **Action sur le SI** | Le script publiait un résumé, sans exécution des suggestions démontrée | Les cellules exécutent du code avec les droits de l'utilisateur ; le script de détection final ne doit déclencher aucun blocage |

Les sorties d'alertes vers l'API personnelle et la dépendance à sa clé sont évitées **si la chaîne reste réellement locale**. Apparaissent ou persistent : dépendances compromises, notebooks exécutant des commandes, serveur Jupyter mal exposé, jeton divulgué, accès aux fichiers de la VM et erreurs d'analyse. Le venv n'arrête pas ces risques ; il sert à l'isolation des dépendances.

## Captures du travail réalisé — 21 octobre 2026

### Connexion puis ouverture de JupyterLab

![Page de connexion Jupyter demandant un mot de passe ou un jeton](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2009-57-15.png)

**Capture de 09 h 57 :** l'écran indique que l'authentification par jeton est activée. L'URL affichée dans l'aide est un exemple tronqué, pas une preuve du jeton réel. Cet écran seul n'établit pas la portée réseau du service.

![JupyterLab ouvert avec les fichiers du kit et le noyau Python proposé](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2009-59-56.png)

**Capture de 09 h 59 :** le lanceur JupyterLab est ouvert ; les deux notebooks, le squelette, le CSV et `requirements.txt` figurent dans le navigateur de fichiers. Cela montre l'accès à l'interface et la présence du kit, **pas l'exécution de la première cellule** ni l'entraînement des modèles. Le moyen d'accès — navigateur de la VM ou tunnel — n'est pas visible.

### Activation du venv et observation de pandas

![Terminal Debian avec activation du venv et pandas déjà installé](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-10-26.png)

**Capture de 10 h 10 min 26 s :** terminal sur Debian, activation de `~/ia01-j3/.venv`, puis `python3 -m pip install --dry-run pandas`. pip indique **pandas 3.0.6** déjà présent sous `.venv/lib/python3.13/site-packages`. Ce chemin situe l'environnement dans une arborescence Python 3.13 ; la sortie exacte de `python3 --version` n'est pas montrée.

**Le test a lieu dans le venv**, comme l'indique le prompt. Il ne démontre donc pas un refus PEP 668 du Python système. Un second essai hors venv est désormais fourni ci-dessous ; il échoue parce que pip est absent du Python système, avant toute vérification PEP 668.

### Essai pandas hors environnement : pip absent

![Commande pandas hors venv et erreur No module named pip](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-15-50.png)

**Capture de 10 h 15 min 50 s :** le prompt n'affiche plus `(.venv)` et la commande `python3 -m pip install --dry-run pandas` répond :

```text
/usr/bin/python3: No module named pip
```

**Résultat observé : pip n'est pas disponible pour cet interpréteur système.** L'essai hors environnement a donc bien été effectué et aucun paquet n'a été installé par cette commande. En revanche, pip n'ayant pas démarré, **aucun refus `externally-managed-environment` n'est démontré**. Cette sortie ne permet pas non plus de conclure que le système n'applique pas PEP 668.

Pour poursuivre le TP, garder le pip du venv : il n'est pas nécessaire d'installer pip globalement pour travailler dans cet environnement. La question « que répond votre système ? » a sa réponse réelle ; le mécanisme PEP 668 reste expliqué à partir de sa documentation.

### Refus du paquet déprécié sklearn

![Échec de l'installation sklearn et recommandation d'utiliser scikit-learn](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-10-38.png)

**Capture de 10 h 10 min 38 s :** `python -m pip install sklearn` échoue lors de la préparation du paquet `sklearn-0.0.post12`, avec le message explicite demandant `scikit-learn`. Le résultat attendu de la question 3 est donc **observé dans le venv**. Cet échec ne démontre pas une panne de scikit-learn, ni sa version installée. Ne pas activer le contournement proposé dans le message de dépréciation.

### Port d'écoute du serveur

![Sortie ss montrant Jupyter en écoute sur 127.0.0.1 port 8888](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-11-03.png)

**Capture de 10 h 11 :** les deux commandes `ss` montrent le processus `jupyter-lab` en écoute sur **`127.0.0.1:8888`**. Le champ distant `0.0.0.0:*` n'est pas l'adresse locale d'écoute : il ne signifie pas que Jupyter écoute sur toutes les interfaces. Ce contrôle confirme la boucle locale **à cet instant**, sans prouver l'absence de redirection de port ou la configuration complète du réseau.

## État de preuve et carnet

Les réponses documentaires sont consignées dans **`livrables/ia-cybersecurite/it-3/ia01-j3/carnet_J3.md`**. Les six captures attestent l’accès à JupyterLab, un venv actif avec pandas 3.0.6, le refus de `sklearn`, l’écoute locale et l’essai hors venv échouant faute de pip système. PEP 668 n’est pas observée dans cet essai. Restent à relever : première cellule du notebook, versions exactes des autres bibliothèques, `pip check` et arrêt du service. Ces observations proviennent des captures de l’apprenant ; aucune commande n’a été exécutée à sa place sur la VM.

Sources consultées le **21 octobre 2026**. Les versions du kit ne sont pas changées ; aucun script ni notebook source n'a été exécuté pour rédiger la fiche.

[Retour à l'itération 3](index.md)
