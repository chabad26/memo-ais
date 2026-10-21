# Le script de détection

**1 h — Autonomie : 30 min de script, 15 min de tests, 15 min de fiche modèle.**

## Le besoin de Nadia

> **Nadia [16:00]** Sofia me dit que vos résultats sont prometteurs 👏  
> Elle voudrait le relancer chaque lundi sur la semaine écoulée.  
> Un notebook, c'est bien pour explorer. Pour l'exploitation, je veux un script lisible et commenté.  
> Que n'importe qui dans l'équipe puisse relire, relancer et obtenir les mêmes résultats.

**Objectif :** transformer les étapes du notebook en un script reproductible qui **enrichit une file à qualifier et n'agit jamais sur le SI**. Le démonstrateur du J3 reste un outil d'entraînement et d'évaluation, pas une chaîne de production hebdomadaire prête à déployer.

## Mission 1 — Script complété et fichiers disponibles

Dans **`livrables/ia-cybersecurite/it-3/ia01-j3/`** :

| Fichier | État et rôle |
| --- | --- |
| **`detection_ssh_squelette.py`** | Original conservé intact |
| **`detection_ssh.py`** | Copie complétée, structurée et commentée ; vérifie les entrées, entraîne les deux modèles et exporte les alertes |
| **`requirements.txt`** | Versions directes du kit conservées sans modification |
| **`alertes_a_qualifier.csv`** | **111 lignes d'alertes** réellement produites à graine 42, plus l'en-tête |
| **`preuves/verification_script.md`** | Environnement, protocole, résultats et empreintes de vérification |
| **`preuves/execution_graine42.txt`**, **`execution_graine7.txt`** | Sorties console des essais dans l'environnement de vérification de l'assistant |
| **`preuves/alertes_graine7.csv`** | Export séparé pour la comparaison ; le fichier final reste celui de graine 42 |
| **`preuves/dependances_verification.txt`** | Relevé des versions installées, y compris transitives ; ne remplace pas un verrouillage avec hachages |

**Attribution :** les commentaires ont été proposés avec l'assistance de l'IA. Ils ne sont pas présentés comme rédigés seul par l'apprenant : les relire, les reformuler si nécessaire et pouvoir expliquer chaque bloc avant remise.

### Paramètres retenus

- **Sept caractéristiques :** heure, externe, échecs, succès, comptes distincts, durée cumulée et volume sortant.
- **Préparation :** suppression explicite des volumes manquants, comptés comme hors couverture ; `origine` vérifiée puis codée en `externe`.
- **Arbre :** `max_depth=3` ; test stratifié de 30 % ; **graine 42**.
- **Isolation Forest :** `contamination=0.03`, même graine ; ajustement sur tout `X`, sans étiquette.
- **Export : union** des lignes signalées par Isolation Forest **OU** prédites attaque par l'arbre ; tri croissant par score d'anomalie, puis départage stable par date/heure/IP.

L'export conserve les signaux complémentaires ; il **ne signifie pas que la combinaison a été validée sur un test indépendant**. La colonne `avis_arbre` sur tout `X` contient aussi des avis sur les données d'entraînement. Les étiquettes de référence ne sont pas exportées dans la file analyste et le score d'anomalie n'est pas une probabilité d'attaque.

Le script valide les colonnes, les valeurs d'origine et d'étiquette, les mesures numériques et l'heure. Une entrée inattendue provoque une erreur explicite plutôt qu'une conversion silencieuse. Il refuse d'utiliser le même chemin pour l'entrée et la sortie. Il ne contient aucun appel de bannissement, pare-feu, désactivation de compte ou envoi externe : sa seule écriture métier est le CSV de sortie demandé.

### Lancer dans la VM

Après avoir copié le script complété dans **`~/ia01-j3`** :

```bash
cd ~/ia01-j3
source .venv/bin/activate
python detection_ssh.py
```

Le programme retrouve par défaut le CSV près de son propre fichier, même depuis un autre dossier de lancement. La sortie existante au chemin choisi est remplacée lors d'une nouvelle exécution ; choisir un autre nom pour conserver un essai :

```bash
python detection_ssh.py --graine 7 --sortie alertes_graine7.csv
```

Une entrée différente peut être indiquée avec `--entree`, mais elle doit encore respecter le schéma et contenir les étiquettes nécessaires à cette version. Cela ne rend pas le programme apte aux nouvelles données non qualifiées.

## Mission 2 — Tests réellement effectués

**Périmètre :** exécutions par l'assistant dans un venv temporaire local, **distinct de la VM de l'apprenant**, avec Python **3.14.4**, pandas **3.0.6**, Scikit-learn **1.9.1**, matplotlib **3.11.2**, JupyterLab **4.6.4**, NumPy **2.5.4** et SciPy **1.18.1**. Les quatre versions directes du kit ont été installées ; `pip check` ne signale pas d'incompatibilité. Aucun serveur Jupyter n'a été lancé pour ces essais.

### 1. Retrouve-t-on les résultats du notebook ?

**Oui à graine 42**, pour les effectifs et règles observés dans les captures :

| Évaluation | VN | FP | FN | VP | Précision attaque | Rappel attaque |
| --- | --- | --- | --- | --- | --- | --- |
| **Arbre — test de 485 lignes** | 453 | **0** | **4** | **28** | 100 % | 87,5 % |
| **fail2ban — mêmes lignes test** | 453 | 0 | 15 | 17 | 100 % | 53,125 % |
| **Isolation Forest — tout X d'ajustement** | 1 501 | **5** | **64** | **44** | 89,80 % | 40,74 % |
| **Union — descriptive sur tout X** | 1 501 | **5** | **2** | **106** | 95,50 % | 98,15 % |

Les deux premières lignes portent sur le test indépendant de l'ajustement de l'arbre ; les deux dernières non. L'union est une **description du jeu connu**, pas la performance attendue sur une nouvelle semaine. L'amélioration apparente du rappel n'autorise pas une comparaison sans tenir compte de ce biais.

En cas d'écart dans la VM : vérifier **le CSV, son ordre, le nettoyage, les sept caractéristiques et leur ordre, la graine, les paramètres et les versions**. Ne pas ajuster artificiellement le résultat pour retrouver une capture. Le notebook peut aussi conserver un ancien `X` après modification de `df` ; le script repart du fichier à chaque exécution.

### 2. Deux exécutions, puis une autre graine

Les **deux exécutions à graine 42** ont produit des sorties console et des CSV **identiques octet par octet**. Empreinte SHA-256 du CSV :

```text
3bb985d4cfb64d31c204404d4300f7c8cb8eb47b2c0979ed5c28d4a438a24b40
```

| Résultat | Graine 42 | Graine 7 |
| --- | --- | --- |
| Arbre, test : FP / FN / VP | **0 / 4 / 28** | **0 / 4 / 28** |
| Règles de l'arbre | Comptes, durée, origine, heure | Comptes, succès, volume, origine, échecs : règles différentes |
| Isolation Forest sur tout X : FP / FN / VP | **5 / 64 / 44** | **4 / 63 / 45** |
| Alertes union | **111** | **108** |
| Union par semaine | **45 puis 66** | **44 puis 64** |

Les mêmes scores de test de l'arbre ne signifient pas les mêmes cas ni les mêmes règles : le partage aléatoire change. Le hasard intervient aussi dans l'ajustement des modèles. Dans les fichiers exportés, **107 observations sont communes**, **4 propres à 42**, **1 propre à 7**. L'essai 7 est conservé séparément ; la graine finale reste **42**, sans sélectionner le meilleur hasard après consultation des résultats.

### 3. Combien d'alertes pour l'astreinte ?

Le CSV final contient **111 alertes** sur les deux semaines du kit :

| Période lundi–dimanche | Alertes Isolation Forest seules | **Alertes union réellement exportées** | Budget union |
| --- | --- | --- | --- |
| **14–20 septembre** | 20 | **45** | Dépassement de **15** |
| **21–27 septembre** | 29 | **66** | Dépassement de **36** |

**55,5 alertes hebdomadaires en moyenne** pour l'union, et non 24,5 : le calcul à 0,03 sur Isolation Forest ne décrit pas à lui seul l'export combiné. Le programme affiche le dépassement ; il n'élimine pas silencieusement des observations pour prétendre respecter le budget.

**Décision proposée à Nadia : pas de mise en service de cette file telle quelle.** Évaluer regroupement des alertes récurrentes, priorités, répartition SOC/astreinte et un seuil combiné sur des données indépendantes. Baisser la contamination ne réduit pas les alertes provenant de l'arbre seul : cela peut être insuffisant.

Une file limitée aux anomalies respecterait **20 puis 29** sur ces deux semaines, mais laisserait **64 attaques de référence non signalées** ; conserver cette option comme arbitrage explicite, pas comme solution sûre. Un plafond de 30 masquerait aussi des alertes : garder la trace des éléments non traités, prévoir leur suivi et mesurer les attaques perdues avant toute acceptation. Aucun risque résiduel n'est accepté à la place de Nadia.

### 4. Prêt pour chaque lundi ?

**Non.** Le script réentraîne les modèles et évalue sur un CSV **déjà étiqueté**, alors qu'une nouvelle semaine ne fournit pas immédiatement les réponses de Hugo. Il manquerait notamment :

| Besoin d'exploitation | Pourquoi ? |
| --- | --- |
| **Séparer entraînement validé et prédiction sur nouveaux logs** | Un modèle figé et sa préparation doivent pouvoir prédire sans `etiquette` ; réentraîner chaque semaine sans contrôle ferait changer le comportement et peut normaliser une activité malveillante |
| **Versionner le modèle et son contexte** | Sauvegarder paramètres, dépendances, empreinte des données et modèle depuis une source de confiance ; permettre contrôle et retour arrière |
| **Validation temporelle indépendante et supervision des erreurs** | Les semaines, machines et usages changent ; suivre faux positifs, attaques manquées, dérive et retour des analystes |
| **Gestion des manques et qualité de collecte** | Les lignes sans NetFlow ne doivent pas disparaître silencieusement de la surveillance ; prévoir signal de panne ou détection dégradée évaluée |
| **Entrées, archivage, erreurs et planification maîtrisés** | Définir période hebdomadaire, schéma, doublons, fichiers datés, permissions, logs sans secrets, codes de retour, reprise et surveillance de la tâche |
| **Gouvernance de la file analyste** | Déduplication, priorités, responsabilité, capacité, suivi des alertes non traitées et décision humaine ; ni ban ni désactivation automatiques |

Ces évolutions sont **à concevoir et valider**, pas déjà déployées. Aucun cron ni accès réseau n'a été créé.

## Mission 3 — Fiche du modèle

**Hexalp — Prototype J3, 21 octobre 2026.** Version pédagogique, non autorisée pour l'exploitation automatique.

| Rubrique | Fiche synthétique |
| --- | --- |
| **Données** | CSV fictif du bastion, 14–27/09/2026 ; 1 704 lignes, 117 attaques (**6,87 %**). Après nettoyage : 1 614 lignes, 108 attaques (**6,69 %**), étiquettes Hugo selon le scénario |
| **Préparation** | Retrait de 90 volumes absents, dont 9 attaques : ne pas les assimiler à zéro ; suivi hors couverture. Origine interne/externe validée puis codée 0/1 |
| **Caractéristiques** | Heure, externe, échecs, succès, comptes, durée, volume. Exclues : étiquette (réponse), fail2ban (comparaison indépendante), IP et date (éviter mémorisation du contexte) ; identifiants gardés pour l'analyste |
| **Modèles / réglages** | DecisionTreeClassifier profondeur 3, partage stratifié test 30 % ; IsolationForest contamination 0,03 ; graine 42. Dépendances du kit. Export union des avis |
| **Résultats** | Arbre test : **0 FP/4 FN**, précision **100 %**, rappel **87,5 %**. IF sur ajustement : **5 FP/64 FN**, précision **89,80 %**, rappel **40,74 %**. Union descriptive : **5 FP/2 FN**, **111 alertes**, **45 puis 66/semaine** ; hors budget 30 |
| **Limites** | 90 lignes exclues ; SSH ne montre pas le contenu envoyé au chatbot ; branche interne/horaire fragile ; sauvegardes/scanner atypiques ; test réutilisé pour réglages ; IF et union mesurés sur ajustement ; données et pratiques évolutives |
| **Conditions** | SOC/astreinte qualifie, Nadia arbitre charge et risques. Aucun blocage. Réévaluer avant nouvelles semaines et après changement de collecte, règles, usages ou hausse d'erreurs ; traçabilité et nouvelle validation avant adoption |

Cette fiche courte est également consignée dans le carnet. La pagination « une page » dépendra de l'export final ; aucune pagination PDF n'est revendiquée ici.

## Captures — Exécution dans la VM à graine 7

### Lancement et résultats des modèles

![Exécution dans le venv Debian à graine 7 et rapports des modèles](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2011-20-40.png)

**Capture de 11 h 20 min 40 s :** commande `python detection_ssh.py --graine 7 --sortie alertes_graine7.csv` exécutée depuis le venv de la VM Debian. Sont visibles : **1 704 lignes brutes**, **90 exclues dont 9 attaques**, **1 614 conservées dont 108 attaques**, partage **1 129 / 485** et règles de l'arbre à graine 7.

Les comptes affichés concordent avec l'essai séparé de l'assistant : arbre **453 VN, 0 FP, 4 FN, 28 VP** ; fail2ban historique **453 VN, 0 FP, 14 FN, 18 VP** ; Isolation Forest **1 502 VN, 4 FP, 63 FN, 45 VP**. Cette concordance porte sur les sorties visibles, pas sur une comparaison d'empreintes des fichiers des deux environnements.

### File combinée et fin du programme

![Résultat union à graine 7 et dépassement du budget hebdomadaire](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2011-20-55.png)

**Capture de 11 h 20 min 55 s :** union descriptive **1 502 VN, 4 FP, 4 FN et 104 VP**, soit **108 observations signalées** par addition VP+FP. Le décompte hebdomadaire montre **44 puis 64**, avec le message **BUDGET DÉPASSÉ** et le rappel de revue humaine sans blocage. Le retour au prompt atteste que le programme a rendu la main sans erreur visible dans cette fin de sortie.

La ligne annonçant l'écriture du CSV n'est pas visible dans ces deux cadrages ; son chemin est demandé dans la commande et les comptes finaux sont observés, mais le contenu exact et l'empreinte du fichier VM ne sont pas contrôlés par ces captures. Elles ne montrent pas non plus deux relances à graine 42 : la preuve d'identité octet par octet à 42 reste celle des essais de l'assistant. Le CSV final du dépôt reste à **graine 42**, l'essai VM à **7** utilise un autre nom.

## État des preuves

**Réalisé par l'assistant sur données fictives :** script commenté, installation isolée des dépendances du kit, deux exécutions identiques à 42, une à 7, vérification du CSV, comptage hebdomadaire et export final. **Fourni par l'apprenant précédemment :** captures des notebooks. **Fourni ensuite par l’apprenant :** deux captures d’exécution du script dans sa VM à graine 7, concordantes sur les résultats visibles. **Encore nécessaire :** relecture personnelle des commentaires, récupération des notebooks complétés/enregistrés et, pour attester la reproductibilité dans la VM, conservation de deux sorties à graine 42 et comparaison des CSV.

Les chemins d'environnement temporaire de vérification ne sont pas requis dans la VM : recréer son propre venv. Les sources CSV, squelette et notebooks fournis sont conservées. Le script doit être relu et compris avant remise.

## Ressources

- [Notebook et kit reçus — présentation J3](index.md)
- [Aide-mémoire Python/pandas](python-de-survie.md), [classifieur](le-classifieur-supervise.md), [anomalies](la-detection-anomalies.md)
- [Scikit-learn — guide utilisateur](https://scikit-learn.org/stable/user_guide.html), consulté le **21 octobre 2026**.

[Retour à l'itération 3](index.md)
