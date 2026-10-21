# Itération 3 — Détecter : votre premier modèle

**IA & cybersécurité — J3**

## Modalités

- **Travail individuel**, guidé le matin et en début d'après-midi, puis en autonomie en fin de journée.
- **Durée : 1 jour.**

## Contexte et objectifs

Au J1, vous avez cherché à la main une règle qui sépare les connexions normales des attaques. Aujourd'hui, vous confiez ce travail à une machine.

Vous installez vous-mêmes un environnement Python, vous apprenez juste assez de Python pour le piloter, puis vous entraînez deux modèles avec **Scikit-learn** sur les journaux SSH d'Hexalp : **un classifieur qui apprend à partir d'exemples étiquetés**, et **un détecteur d'anomalies qui s'en passe**.

À la fin de la journée, vous aurez un **script reproductible qui produit des alertes pour un analyste**, et vous saurez dire ce que ces alertes valent. Une prédiction ou une anomalie ne constitue pas à elle seule une attaque confirmée ; le script aide l'analyste sans agir à sa place.

## Compétences

- Expliquer la chaîne d'entraînement d'un modèle, de l'observation à la prédiction.
- Installer un environnement Python isolé et reproductible, sans exposer de service.
- Lire, exécuter et modifier un notebook Python.
- Préparer des journaux d'infrastructure : nettoyage, transformation et choix des caractéristiques.
- Entraîner et évaluer un classifieur et un détecteur d'anomalies avec Scikit-learn.
- Produire un script reproductible et commenté qui aide un analyste sans agir à sa place.

## 📦 Livrables — Dossier `ia01-j3`

| Livrable attendu | Contenu demandé | État actuel |
| --- | --- | --- |
| **`carnet_J3.md`** | Réponses aux missions du kit et aux questions ✍️ des notebooks, tableau Bash / pandas et fiche du modèle | Commencé : réponses 3.1/3.2, chaîne du J1 et réponses théoriques 3.3 ; sorties VM à relever ; tableau Bash/pandas et réponses 3.4 préparés ; sorties VM, questions de détection et fiche du modèle à compléter |
| **`00_python_survie.ipynb`** | Notebook d'initiation complété et exécuté | Reçu dans le kit ; emplacements à compléter, compteurs d’exécution non renseignés |
| **`01_detection_ssh.ipynb`** | Notebook de détection complété et exécuté | Reçu dans le kit ; emplacements à compléter, compteurs d’exécution non renseignés |
| **`detection_ssh.py`** | Script fonctionnel, reproductible et commenté, accompagné de `requirements.txt` | Produit et vérifié par l’assistant sur le kit ; exécution VM à graine 7 attestée par deux captures ; relecture et relances VM à 42 à documenter |
| **`alertes_a_qualifier.csv`** | Fichier d'alertes produit par le script, destiné à la qualification par un analyste | Produit : 111 alertes union à graine 42, 45 puis 66 par semaine ; dépassement du budget explicite |

## Fichiers fournis — Kit reçu

| Fichier | Ce qu'il contient | Disponibilité dans le mémo |
| --- | --- | --- |
| **`requirements.txt`** | Bibliothèques Python à installer, avec leurs versions | Reçu dans `livrables/ia-cybersecurite/it-3/ia01-j3/` ; distinct du fichier de dépendances du site |
| **`hexalp_ssh_sept2026.csv`** | Deux semaines de journaux SSH du bastion d'Hexalp, résumés et étiquetés ; données fictives | Reçu dans le dossier du kit |
| **`00_python_survie.ipynb`** | Notebook d'initiation Python, séquence 3.4 | Reçu dans le dossier du kit |
| **`01_detection_ssh.ipynb`** | Notebook de détection à compléter, séquences 3.5 à 3.7 | Reçu dans le dossier du kit |
| **`detection_ssh_squelette.py`** | Squelette du script final à compléter et commenter, séquence 3.8 | Reçu dans le dossier du kit |

### Repérage des fichiers — 21 octobre 2026

Les cinq fichiers sont conservés dans **`livrables/ia-cybersecurite/it-3/ia01-j3/`**. Ils ont été lus pour identifier leur contenu, sans installation de leurs dépendances ni exécution de leur code.

- **CSV : 1 704 lignes de données**, avec les colonnes `date`, `heure`, `ip_source`, `origine`, `echecs_auth`, `succes_auth`, `comptes_distincts`, `duree_session_min`, `octets_sortants_mo`, `fail2ban_ban`, `etiquette`. Le notebook annonce la période du 14 au 27 septembre 2026 ; le nettoyage sera traité dans les séquences prévues.
- **Notebook Python :** 35 cellules, dont 23 de code ; **notebook détection :** 46 cellules, dont 27 de code. Tous les compteurs d'exécution sont non renseignés ; cela décrit les fichiers reçus, pas leur éventuelle utilisation ailleurs.
- **Algorithmes explicitement présents dans le squelette :** `DecisionTreeClassifier` et `IsolationForest`. Les paramètres et les instructions marqués `___` / `TODO` sont à compléter ; aucun modèle n'est encore entraîné dans notre travail.
- **Dépendances déclarées :** `jupyterlab==4.6.4`, `pandas==3.0.6`, `scikit-learn==1.9.1`, `matplotlib==3.11.2`. L'en-tête indique Python 3.11 ou plus récent. Ce relevé ne valide pas encore la disponibilité ni la compatibilité de ces versions : l'installation sera vérifiée à l'étape correspondante.

Les numéros de séquences reprennent le programme transmis ; leurs fiches ne sont pas préparées avant réception des consignes. Les sources reçues restent intactes. Aucun score ni résultat d'entraînement n'est annoncé.

## État attendu en fin de journée

Le dossier `ia01-j3` devra réunir les réponses, les deux notebooks exécutés, le script et ses dépendances, ainsi que le CSV réellement généré. Les résultats devront permettre de discuter les erreurs et les limites des deux approches. **Un fichier de sortie ne prouve pas, à lui seul, la qualité de la détection.**

Les fiches 3.1–3.3 sont intégrées. Les captures de la VM attestent JupyterLab ouvert, un venv actif, pandas 3.0.6, le refus de sklearn et une écoute locale sur 127.0.0.1:8888. La première cellule et les autres vérifications restent à documenter ; la partie C est ensuite attestée par sept captures : nettoyage, entraînement d’un arbre profondeur 3 et test (0 FP, 4 FN, 28 VP). Isolation Forest est ensuite attesté par quatre captures : 49 alertes dont 44 VP/5 FP à 0,03 ; le script est ensuite complété et vérifié : CSV union de 111 alertes et tests à graines 42/7, distincts des exécutions VM.

## Fiches de l’itération

- [Le projet de la supervision](le-projet-de-la-supervision.md) : message de Nadia, cinq scénarios comparés à fail2ban et besoins de données pour les modèles — 15 min.

- [Mettre en place un classifieur](mettre-en-place-classifieur.md) : chaîne du J1, choix classification/anomalies et réponses renseignées — 45 min.

- [Installer son environnement](installer-son-environnement.md) : procédure VM, venv, Jupyter local, tunnel SSH et réponses administrateur — 45 min ; six captures commentées et vérifications restantes.

- [Python de survie](python-de-survie.md) : trois erreurs expliquées, tableau Bash/pandas rempli, six captures des exercices et analyse des transferts nocturnes — 1 h.

- [Explorer et préparer les journaux](explorer-preparer-journaux.md) : réponses A1–A4/B1–B2, quatre captures, manques NetFlow et sept caractéristiques ; nettoyage restant à vérifier — 45 min.

- [Le classifieur supervisé](le-classifieur-supervise.md) : C1–C6 renseignés, sept captures, règles, erreurs et comparaison fail2ban — 1 h.

- [La détection d’anomalies](la-detection-anomalies.md) : partie D, D1–D5, tableau comparatif et quatre captures des résultats — 1 h.

- [Le script de détection](le-script-de-detection.md) : script complété, tests de reproductibilité, export union de 111 alertes à 42, deux captures VM à 7 et fiche modèle — 1 h.

## Repères et liens

- [J1 — Le Machine Learning : apprendre à partir d'exemples](../it-1/machine-learning-apprendre-exemples.md)
- [J2 — Le dossier Hexalp](../it-2/le-dossier-hexalp.md)
- [Pense-bête de l'itération 3](../../pense-bete/glossaire/ia-cybersecurite/it-3.md)
- [Retour au module](../README.md)
