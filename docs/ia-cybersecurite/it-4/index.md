# Itération 4 — Critiquer : ce que vaut votre modèle

**IA & cybersécurité — J4**

## Modalités

- **Travail individuel**, en autonomie le matin, guidé l'après-midi.
- **Durée : 1 jour.**

## Contexte et objectifs

Hier, le modèle a appris sur deux semaines de journaux et obtenu des résultats sur des données de la même période. Aujourd'hui, il affronte **les deux semaines suivantes**, dans le scénario d'une infrastructure qui évolue et d'attaquants qui changent de méthode.

Le matin, vous le réparez, vous l'évaluez dans les conditions de l'exploitation et vous rédigez son rapport d'évaluation. L'après-midi, vous changez de camp pour l'attaquer dans le cadre du TP, vous utilisez un réseau de neurones pré-entraîné et vous fixez les conditions auxquelles Hexalp pourrait l'exploiter **sans s'y fier aveuglément**.

Le [travail du J3](../it-3/le-script-de-detection.md) a déjà montré plusieurs limites : test réutilisé pour comparer les réglages, détection d'anomalies examinée sur ses données d'ajustement, observations exclues pendant une panne NetFlow et charge de la file combinée supérieure à la capacité. Ces résultats constituent le point de départ ; ils ne préjugent pas des performances sur octobre.

## Compétences

- Évaluer un modèle sur des données qu'il n'a jamais vues, dans les conditions de l'exploitation.
- Adapter la préparation des données à un changement de l'infrastructure.
- Interpréter les faux positifs et faux négatifs et estimer leur coût pour l'astreinte.
- Identifier les attaques contre un modèle : extraction, contournement et empoisonnement.
- Utiliser un modèle de Deep Learning pré-entraîné en vérifiant son intégrité.
- Définir les conditions d'exploitation et de réévaluation d'un modèle de détection.

## 📦 Livrables — Dossier `ia01-j4`

| Livrable attendu | Contenu demandé | État actuel |
| --- | --- | --- |
| **`rapport_evaluation.md`** | Rapport rédigé le matin et complété l'après-midi | Rapport complet4.1–4.8 ; PDF final13pages (rapport3pages + annexes), remise groupée ZIP préparée |
| **`detection_ssh_v2.py`** et **`requirements.txt`** | Script fonctionnel et commenté, dépendances associées | V2 commentée produite et testée ; dépendances du kit conservées, exécution VM illustrée par deux captures |
| **`alertes_octobre.csv`** | Alertes réellement produites par le script | Généré par la V2 : 239 alertes, 104 puis135 par semaine |
| **`carnet_J4.md`** | Réponses aux missions du kit et aux questions ✍️ des notebooks | Commencé : séquences 4.1–4.8 renseignées ; hypothèses, journal DSI, comparaison et préparation, avec limites de preuve |
| **Notebooks 03 et 04** | Fichiers complétés et exécutés | 03 et 04 complétés/exécutés localement hors VM ; sources conservées |

## Fichiers fournis — Kit reçu

**Emplacement dans le dépôt :** `livrables/ia-cybersecurite/it-4/IA_J4_ressources_apprenant/ia01-j4/`.

| Fichier | Contenu annoncé et vérification de présence |
| --- | --- |
| **`hexalp_ssh_oct2026.csv`** | Deux semaines suivantes, **28 septembre–11 octobre 2026**, étiquetées par Hugo selon le scénario ; **2 119 lignes de données** dans le fichier reçu ; données fictives |
| **`hexalp_ssh_sept2026.csv`** | Jeu du J3 réservé à l'entraînement ; **1 704 lignes**, 14–27 septembre ; copie identique octet par octet au fichier source du J3 |
| **`02_boite_a_outils.ipynb`** | Outils pour comparer, préparer et évaluer — séquences 4.2/4.3 ; 32 cellules, dont 21 de code, compteurs vides |
| **`03_attaquer_le_modele.ipynb`** | Notebook d'attaque à compléter — séquence 4.6 ; source conservée (29 cellules, dont 15 de code) ; version complétée/exécutée localement : 31 cellules, dont 16 de code |
| **`04_autoencodeur.ipynb`** | Notebook du réseau de neurones à compléter — séquence 4.7 ; source conservée (16 cellules, dont 8 de code) ; version complétée/exécutée localement : 18 cellules, dont 9 de code |
| **`autoencodeur_hexalp.joblib`** | Modèle annoncé comme pré-entraîné par Hugo ; empreinte comparée à la référence du PDF4.7 ; chargé pour inférence locale, sans entraînement ni modification |
| **`requirements.txt`** | Même liste de dépendances et versions que J3 ; commentaire d'en-tête mis à jour pour J3/J4 |

Le relevé ci-dessus est une inspection de fichiers, pas une exécution des notebooks ou une évaluation des modèles. Les numéros de séquences reprennent le contexte transmis ; leurs activités ne sont pas préparées avant réception des consignes.

### Environnement conservé du J3

Les versions demandées restent **JupyterLab 4.6.4**, **pandas 3.0.6**, **Scikit-learn 1.9.1** et **matplotlib 3.11.2**. Le kit n'ajoute donc pas de bibliothèque à installer. Conserver le venv existant de la VM ; la V2 a été exécutée dans la VM ; le modèle pré-entraîné a été utilisé en inférence locale de vérification, hors VM.

## Préparer le dossier de travail dans la VM

Créer **`~/ia01-j4`**, y copier les sept fichiers du kit et **votre `detection_ssh.py` du J3**. Garder les originaux ; la V2 sera distincte. Les copies et le lancement ci-dessous sont à effectuer dans la VM, pas attestés par l'inspection du dépôt.

```bash
mkdir -p ~/ia01-j4
```

Après la copie des fichiers :

```bash
source ~/ia01-j3/.venv/bin/activate
cd ~/ia01-j4
jupyter lab --no-browser --ip=127.0.0.1 --port=8888 --ServerApp.port_retries=0
```

L'option `port_retries=0` conserve explicitement le port demandé. Si Jupyter du J3 utilise encore 8888, l'arrêter proprement avant ce lancement ou employer un autre port local en adaptant le tunnel. Ne pas désactiver le jeton ni ouvrir toutes les interfaces. Pour une VM sans navigateur, reprendre le [tunnel SSH et la récupération du jeton](../it-3/installer-son-environnement.md).

## Repères de méthode pour cette journée

- **Séparer septembre et octobre :** septembre sert à entraîner ; octobre évalue le futur. Une préparation qui apprend une statistique doit elle aussi respecter cette séparation.
- **Séparer résultat et hypothèse :** l'évolution annoncée de l'infrastructure et des attaques appartient au contexte ; les effets sur les données et erreurs seront établis pendant les missions.
- **Vérifier avant de charger le modèle :** sa présence et une empreinte calculée localement ne démontrent pas seules une provenance fiable ou une conformité à une référence indépendante. Aucun chargement du `.joblib` n'est réalisé ici.
- **Conserver la décision humaine :** modèles et expériences du kit servent à analyser et qualifier, sans déclencher de blocage du SI.

Ces repères ne remplacent pas les consignes détaillées des séquences à venir.

## État du travail

**Présentation de l'itération intégrée et sept fichiers repérés le 21 octobre 2026.** Aucun notebook J4 n'a été exécuté, aucun modèle pré-entraîné chargé, aucune attaque du modèle réalisée lors de cette inspection initiale et aucun résultat sur octobre calculé pour cette présentation. Cette phrase décrit la seule inspection initiale du kit. Depuis, l’apprenant a transmis des résultats du notebook02 : exploration et évaluations rapportées, avec conversion corrigée ; la V2 retrouve désormais les règles du J3 et son exécution dans la VM est illustrée par deux captures. Le carnet4.1 est commencé ; V2 et CSV désormais produits/testés en 4.3 ; rapport4.4 enrichi des simulations4.6 ; notebook03 exécuté localement. Notebook04 également exécuté localement en4.7 après contrôle du SHA-256. Conditions finales proposées en4.8 ; PDF final et archive de remise groupée préparés, sans envoi au formateur.

## Fiches de l’itération

- [99 %](99-pour-cent.md) : scénario d’ouverture, trois hypothèses et premières vérifications ; chronologie réelle explicitée.
- [Relancer et réparer](relancer-et-reparer.md) : journal DSI, comparaison renseignée et préparation adaptée — 1 h 15 en autonomie.
- [Évaluer en conditions réelles](evaluer-en-conditions-reelles.md) : script V2, 239 alertes, tableaux des erreurs et exfiltration retrouvée — 1 h en autonomie.

- [Le rapport d’évaluation](le-rapport-evaluation.md) : synthèse pour Nadia, coût des erreurs et avis provisoire de mise en service — 1 h en autonomie.

- [Le mur des matrices](le-mur-des-matrices.md) : coût des faux positifs, classement et comparaison locale A/B/C, distincte du tableau du cours — 30 min.

- [Attaquer son modèle](attaquer-son-modele.md) : notebook 03 exécuté localement, réponses A1–D4, comparaison kit/V2 et tableau des six attaques — 1 h 30.

- [Et le Deep Learning ?](et-le-deep-learning.md) : SHA-256 vérifié, autoencodeur utilisé en inférence, réponses R1–R5 et tableau des trois modèles — 45 min.

- [Exploiter sans se fier aveuglément](exploiter-sans-se-fier-aveuglement.md) : chaîne, conditions, recommandation finale et cinq questions à l’éditeur — 45 min.

## Liens

- [Pense-bête de l'itération 4](../../pense-bete/glossaire/ia-cybersecurite/it-4.md)
- [Itération 3 — Détecter : votre premier modèle](../it-3/index.md)
- [Retour au module](../README.md)
