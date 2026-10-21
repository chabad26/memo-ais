# Carnet J3 — Détecter : votre premier modèle

**Olivier HIMBLOT — 21 octobre 2026**

Données fictives du kit Hexalp. Carnet commencé pour les séquences reçues ; aucun entraînement ou résultat J3 n’est revendiqué.

## Séquence 3.1 — Le projet de la supervision

Réponses détaillées : `docs/ia-cybersecurite/it-3/le-projet-de-la-supervision.md` dans le dépôt.

| Scénario | Réponse fail2ban pour le seuil fourni |
| --- | --- |
| 1 — 200 essais rapides | Oui si même IP, journaux visibles et IP non exemptée |
| 2 — Un essai toutes les dix minutes | Non pour le rythme total décrit |
| 3 — Connexion valide puis 1 Go sortant | Non avec la règle d’échecs |
| 4 — Dix comptes sur serveurs de production | Dépend des journaux collectés, de la cadence et de la répartition par hôte |
| 5 — Scanner autorisé | Oui sous les mêmes conditions de seuil ; contexte d’audit à qualifier |

Un modèle peut aider surtout pour les essais lents, les usages inhabituels et la corrélation, si les données existent. Un audit mensuel autorisé est une anomalie légitime possible. Résultats des deux modèles : non testés.

## Séquence 3.2 — Mettre en place un classifieur

## Mission 1 — Ma chaîne du J1

Le tableau reprend la résolution documentée des 18 observations SSH du J1. « J'ai » décrit ce travail pédagogique, pas une collecte réelle chez Hexalp ni un test à l'aveugle attesté.

| N° | Étape | Question à se poser | Séquence | Au J1, j'ai… |
| --- | --- | --- | --- | --- |
| **1** | **Observations** | Que représente une ligne ? Combien y en a-t-il ? | 3.5 | Lu 18 observations fictives, chacune résumant une IP pendant une heure : 12 exemples initiaux et 6 nouveaux cas |
| **2** | **Caractéristiques** | Quelles colonnes le modèle peut-il regarder ? | 3.5 | Choisi d'abord les échecs SSH ; comparé l'heure et étudié les comptes distincts. Le numéro identifie la ligne et l'étiquette sert à vérifier : ni l'un ni l'autre ne doit fournir directement la réponse au modèle |
| **3** | **Nettoyage et transformation** | Que faire des cases vides et du texte ? | 3.5 | Utilisé un tableau déjà lisible et sans manque apparent ; défini « nuit » par heure ≥ 22 ou heure < 6. Je n'ai pas audité systématiquement types, doublons, valeurs manquantes ou incohérences |
| **4** | **Séparation** | Quelles données pour apprendre, lesquelles pour vérifier ? | 3.6 | Cherché R1 sur les lignes 1–12, puis appliqué cette règle figée sur 13–18. Ensuite, j'ai modifié la règle après avoir vu les erreurs : ces six lignes ne sont plus un test indépendant pour R2 |
| **5** | **Type de modèle** | Ai-je des étiquettes ? Classification ou anomalies ? | 3.2 | Fait une classification binaire avec les étiquettes normal/attaque ; puis observé les points sans utiliser ces étiquettes pour discuter les anomalies |
| **6** | **Algorithme** | Quel outil et quels réglages ? | 3.6 et 3.7 | Comparé manuellement des règles à seuil ; aucun estimateur Scikit-learn n'a été entraîné dans cet exercice. Retenu R1 : échecs > 20, puis exploré R2 : échecs > 3 ET comptes > 3 |
| **7** | **Entraînement** | Comment les paramètres sont-ils trouvés ? | 3.6 et 3.7 | Cherché un seuil séparant les douze exemples ; tout seuil de 12 inclus à 30 exclu convenait. Le choix de 20 était simple, pas un optimum démontré |
| **8** | **Prédiction et score** | Que répond le modèle sur un cas nouveau ? | 3.6 et 3.7 | Appliqué R1 aux six nouvelles lignes : attaque pour 13, 15 et 18 ; normal pour 14, 16 et 17. Aucun score probabiliste n'était produit |
| **9** | **Évaluation** | Combien de FP/FN ? Est-ce acceptable ? | 3.6 et 3.7 | Compté pour R1, sur le test : 1 VP, 1 VN, 2 FP et 2 FN, soit précision = rappel = 1/3. Discuté le coût métier ; constaté que zéro erreur à l'entraînement ne garantit pas la qualité sur de nouveaux cas |

### Quelles étapes ai-je sautées ou simplifiées ?

- **Contrôles des données :** tableau préparé, sans démarche complète de validation et de nettoyage.
- **Validation séparée :** après les essais sur les erreurs, R2 a besoin d'un nouveau test tenu à l'écart. Son zéro erreur sur les 18 lignes est exploratoire.
- **Contexte et représentativité :** 18 observations ne couvrent pas tous les comportements ni les évolutions temporelles d'un bastion.
- **Traçabilité de l'expérience :** règle et résultat sont écrits, mais pas de chaîne Python, d'environnement de dépendances ou d'entraînement automatisé dans ce travail du J1.

Je n'avais donc pas sauté la séparation ou l'évaluation entièrement : je les avais pratiquées à petite échelle, puis fragilisées en réutilisant le test pour améliorer la règle. Le nettoyage était surtout fourni implicitement par l'exercice.

## Mission 2 — Classification ou anomalies ?

| N° | Besoin | Approche retenue | Pourquoi ? |
| --- | --- | --- | --- |
| **1** | Repérer les brute force SSH avec deux ans d'incidents qualifiés par le SOC | **Classification** | Des exemples et étiquettes existent ; vérifier leur qualité, les changements du SI et conserver une évaluation sur des données non utilisées pour apprendre |
| **2** | Surveiller un serveur installé la semaine dernière, sans historique d'attaque | **Détection d'anomalies, avec prudence au démarrage** | Pas d'exemples d'attaques étiquetés ; apprendre une référence d'activité représentative et utiliser entre-temps les règles existantes. Une semaine peut être insuffisante pour les cycles légitimes |
| **3** | Trier des mails avec 5 000 exemples phishing/légitime | **Classification** | Les catégories cibles sont connues et accompagnées d'exemples ; contrôler biais de signalement, doublons et séparation des campagnes entre apprentissage et test |
| **4** | Repérer une exfiltration par compte de service jamais rencontrée chez Hexalp | **Détection d'anomalies en complément des autres contrôles** | Comparer l'activité au comportement habituel du compte : volumes, horaires et destinations ; il faut disposer de cette télémétrie et l'exfiltration peut rester discrète |
| **5** | Distinguer les alertes Zabbix utiles du bruit avec six mois de décisions de l'astreinte | **Classification** | Les décisions passées peuvent fournir les étiquettes utile/bruit ; harmoniser les critères et ne pas assimiler une alerte ignorée à une alerte sans intérêt |

Le choix dépend du besoin et des données, pas d'une supériorité générale d'une approche. La [carte des estimateurs Scikit-learn](https://scikit-learn.org/stable/machine_learning_map.html) aide à orienter le choix ; elle ne remplace pas l'évaluation dans le contexte d'Hexalp.

### 1. Un classifieur peut-il reconnaître une attaque absente de ses exemples ?

**Il ne peut pas apprendre directement une catégorie jamais représentée**, mais il peut parfois signaler un type d'attaque nouveau s'il partage des caractéristiques avec les attaques apprises. Par exemple, une attaque inconnue qui produit beaucoup d'échecs peut franchir la frontière apprise.

L'affirmation « il ne peut jamais reconnaître une attaque absente » serait donc trop forte. Le vrai problème est **l'absence de garantie sur les comportements nouveaux** : un compte volé qui se connecte sans échec peut ressembler à un cas normal. La généralisation dépend de la représentation, des exemples et de l'algorithme ; l'absence de détection ne prouve pas la légitimité.

### 2. Une anomalie est-elle forcément une attaque ?

**Non.** Le scanner de vulnérabilités d'Hexalp peut générer un pic mensuel d'échecs SSH : événement rare, mais légitime si l'audit est autorisé et respecte son périmètre. Une maintenance nocturne ou un transfert exceptionnel autorisé peut également être atypique.

Vérifier calendrier, source, responsable et autorisation. Inversement, une attaque peut imiter le comportement habituel et ne produire aucune anomalie détectable. Voir les scénarios de la supervision.

### 3. Qui fournit les étiquettes et que se passe-t-il en cas d'erreur ?

Les analystes SOC, équipes de réponse à incident ou responsables métier qualifient les événements à partir de preuves. Pour Zabbix, les décisions de l'astreinte peuvent servir de point de départ, avec une définition commune de « utile ». Dans le CSV du kit, les étiquettes sont **fictives et fournies** : nous ne les avons pas établies à partir d'incidents réels.

Une erreur d'étiquetage peut apprendre au modèle à ignorer des attaques ou à alerter sur des usages normaux. Elle fausse aussi l'évaluation si le jeu de test contient ces erreurs. Prévoir revue des cas ambigus, traçabilité, possibilité de rectification et vérification indépendante d'un échantillon. Ne pas transformer automatiquement toutes les prédictions du modèle en nouvelles étiquettes de référence.

## Repères d'évaluation

| Référence réelle / prédiction | Prédit attaque | Prédit normal |
| --- | --- | --- |
| **Étiquette attaque** | Vrai positif — VP | Faux négatif — FN |
| **Étiquette normal** | Faux positif — FP | Vrai négatif — VN |

Une sortie numérique « attaque » est **une classe prédite**, pas une confirmation d'incident. La décision opérationnelle reste à l'analyste. Le projet J3 produit des alertes à qualifier et ne déclenche aucun blocage.


## Séquence 3.3 — Installer son environnement

**État : procédure et réponses théoriques préparées ; six captures du 21 octobre 2026 apportent des preuves partielles d’installation et de contrôle.** Fiche détaillée : `docs/ia-cybersecurite/it-3/installer-son-environnement.md` dans le dépôt.

| Question | Réponse documentaire |
| --- | --- |
| venv et PEP 668 | Isoler les dépendances évite les conflits avec APT ; Python système peut refuser pip avec `externally-managed-environment`. Observer avec `--dry-run` sans modifier le système. Un venv n’isole ni fichiers ni réseau. |
| Versions et hachages | Les quatre dépendances directes sont figées ; transitives, Python, OS, pip et disponibilité restent à contrôler. `--require-hashes` vérifie les distributions par hachage dans un fichier complet et correctement figé ; le fichier actuel ne contient pas ces hachages. |
| sklearn | Installation du paquet déprécié attendue en erreur ; installer `scikit-learn`, importer `sklearn`. Nom réservé pour éviter un détournement malveillant de l’alias connu. Vérifier tout paquet recommandé par un LLM. |
| Écoute et jeton | Attendre `127.0.0.1:8888`, à vérifier avec `ss` dans la VM ; jeton = authentification, pas chiffrement. Avec poste hôte : tunnel SSH, authentification Jupyter conservée. |
| Exposition et Qubitstrike | Serveur joignable sans authentification : exécution de code avec les droits Jupyter. Campagne 2023 contre instances exposées : exécution de charges et vol d’identifiants cloud. Aucun test d’exposition à faire. |
| Sofia / J3 | Calcul et CSV fictif locaux, aucune clé API IA nécessaire ; restent le jeton Jupyter, l’accès SSH, les dépendances et les risques d’exécution de code ou de fuite locale. |

### Preuves VM à compléter avec les sorties réelles

| Vérification | Résultat réel |
| --- | --- |
| VM, distribution et version Python | Terminal Debian visible ; chemin du venv sous Python 3.13. Version complète Python à relever |
| Création/activation du venv, chemin pip | Activation visible dans 10-10-26 ; venv `~/ia01-j3/.venv` et pandas sous `.venv/lib/python3.13/site-packages`. Création non montrée |
| Installation des dépendances, `pip check`, version pip | pandas 3.0.6 déjà installé selon pip ; installation complète, `pip check` et version pip non montrés |
| Première cellule de code : Python/pandas/scikit-learn/matplotlib/sys.prefix | Non exécutée |
| Observation hors venv avec `--dry-run` | Capture 10-15-50 : `/usr/bin/python3: No module named pip`. Essai réalisé, pip système absent ; aucun refus PEP 668 observé |
| Essai `python -m pip install sklearn` dans le venv | Refus observé dans 10-10-38 : paquet déprécié, utiliser scikit-learn |
| Écoute `ss` et accès local ou tunnel SSH | 10-11-03 : jupyter-lab écoute sur 127.0.0.1:8888 ; interface ouverte à 09-59-56. Tunnel ou navigateur VM non déterminable |
| Arrêt de Jupyter et du tunnel | Non montré ; Jupyter est actif lors du contrôle ss |

Sources et commandes dans la fiche de la séquence ; aucune version installée n’est inventée à partir du fichier requirements.

## Séquence 3.4 — Python de survie

Corrigé préparé à partir du notebook source et vérifications séparées avec Python local. Six captures fournies ensuite attestent les cellules pandas visibles dans Jupyter ; elles sont détaillées en fin de séquence.

## Mission 1 — Les bases : sections 1 à 5

### Compléter les premiers exercices

Le seuil du J1 était **20**. Pour les trois caractéristiques, on utilise les noms correspondants du CSV J3 :

```python
seuil = 20
alerte = echecs > seuil

colonnes_j1 = ["echecs_auth", "heure", "comptes_distincts"]
print(colonnes_j1[1])  # deuxième élément : heure

print(evenement["comptes"])  # clé du dictionnaire de l'exercice : 42
```

La clé `comptes` du petit dictionnaire n'est pas le nom `comptes_distincts` de la colonne du CSV. Les chaînes doivent correspondre aux clés réellement présentes. `=` affecte une valeur ; `==` compare deux valeurs. Un test de préfixe `ip.startswith("10.")` n'est pas une détection générale de toutes les adresses privées.

### Tableau des trois erreurs — Corrigé

| Erreur | Dernière ligne du message | Cause | Correction |
| --- | --- | --- | --- |
| **n°1** : `print(Echecs)` | `NameError: name 'Echecs' is not defined` | Python distingue majuscules et minuscules ; la variable créée est `echecs` | `print(echecs)` → `87` |
| **n°2** : `print(evenement["échecs"])` | `KeyError: 'échecs'` | La clé réelle est `echecs`, sans accent | `print(evenement["echecs"])` → `87` |
| **n°3** : `print(nombre_lu + 1)` avec `nombre_lu = "87"` | `TypeError: can only concatenate str (not "int") to str` | On tente d'additionner une chaîne et un entier | `print(int(nombre_lu) + 1)` → `88` |

Ces trois erreurs ont été **reproduites isolément avec Python 3.14.4 dans l'environnement de vérification de l'assistant**, en fournissant les variables préalables. Ce ne sont pas des sorties de la VM. La formulation, les suggestions et le contexte du traceback peuvent varier selon la version ; le type et la cause restent à comparer avec vos sorties.

**Lecture du traceback :** commencer par la dernière ligne, puis remonter jusqu'à la cellule et à l'instruction concernées. Ajouter `str(1)` à la troisième expression produirait `871` : cela ne corrige pas l'intention d'une addition numérique. Sur des entrées non garanties, `int()` peut lui-même lever `ValueError` : il faut alors traiter la valeur invalide.

## Mission 2 — De Bash à pandas : sections 6 et 7

Préalable dans le notebook :

```python
import pandas as pd

df = pd.read_csv("hexalp_ssh_sept2026.csv")
```

Le chemin est relatif au dossier de travail du noyau. En cas de `FileNotFoundError`, vérifier où le noyau travaille et si le fichier y est présent, plutôt que modifier son nom au hasard.

### Tableau Bash / pandas renseigné

| Ce que vous voulez faire | En Bash — repère de la consigne | En pandas |
| --- | --- | --- |
| Voir les premières lignes | `head -5 fichier.csv` | `df.head()` |
| Compter les observations | `wc -l fichier.csv` | `len(df)` ou `df.shape[0]` |
| Extraire une colonne | `cut -d, -f5 fichier.csv` | `df["echecs_auth"]` |
| Compter chaque valeur de la colonne origine | `cut -d, -f4 fichier.csv` puis `sort` puis `uniq -c` | `df["origine"].value_counts()` |
| Filtrer les lignes avec plus de 50 échecs | `awk -F, '$5 > 50' fichier.csv` | `df[df["echecs_auth"] > 50]` |
| Trier les volumes sortants et garder les dix plus grands | `sort -t, -k9 -nr` puis `head` | `df.sort_values("octets_sortants_mo", ascending=False).head(10)` |
| Compter les IP distinctes | `cut -d, -f3 fichier.csv` puis `sort -u` puis `wc -l` | `df["ip_source"].nunique()` |

**Ce sont des correspondances d'intention, pas des sorties strictement identiques :**

- `head -5` inclut l'en-tête du CSV, alors que `df.head()` affiche cinq observations en plus des noms de colonnes.
- Sur ce fichier, `wc -l` compte aussi l'en-tête ; `len(df)` compte les observations. Les commandes Bash sur une colonne doivent exclure l'en-tête pour ne pas le compter comme une valeur ou une IP.
- `value_counts()` et `nunique()` ignorent normalement les valeurs manquantes ; utiliser `dropna=False` pour les compter explicitement.
- `cut`, `awk` et `sort` ne constituent pas un parseur CSV général : séparateurs entre guillemets, champs multilignes et en-tête demandent des précautions.
- Les tris numériques nécessitent des valeurs numériques. Ne pas remplacer les volumes manquants par zéro sans justifier le choix ; le nettoyage sera traité ensuite.

### Corrigé des cellules a à e

```python
# a) Nombre d'observations, hors en-tête
print(len(df))

# b) Nombre d'IP distinctes non manquantes
print(df["ip_source"].nunique())

# c) Effectifs de chaque étiquette
print(df["etiquette"].value_counts())
# Pour compter seulement les attaques :
print((df["etiquette"] == "attaque").sum())

# d) De 0 h à 5 h inclus, avec au moins une connexion réussie
# Le CSV fourni utilise des heures entières de la journée.
df[(df["heure"] <= 5) & (df["succes_auth"] > 0)]

# e) Les cinq observations au volume sortant le plus élevé
# Il ne s'agit pas d'un cumul des volumes par IP.
df.sort_values("octets_sortants_mo", ascending=False).head(5)
```

Pour rendre le filtre d) explicite même avec des valeurs incohérentes, on peut employer `df["heure"].between(0, 5)`. Les parenthèses entourant chaque condition et l'opérateur `&` sont nécessaires pour combiner les masques pandas ; `and` ne remplace pas `&` ici.

### Valeurs de référence vérifiées sur le fichier fourni

Les comptes et le tri ci-dessous ont été recalculés **en lecture seule avec la bibliothèque standard Python (`csv`, `collections`)**, sans exécuter le notebook ni utiliser pandas. Ils servent à vérifier vos résultats pandas dans la VM, pas à attester son exécution.

| Vérification | Valeur du CSV reçu, avant nettoyage |
| --- | --- |
| Observations | **1 704** |
| Colonnes | **11** |
| IP distinctes | **138** |
| Étiquette `normal` | **1 587** |
| Étiquette `attaque` | **117** |

| Date | Heure | IP source | Volume sortant (Mo) | Étiquette fournie |
| --- | --- | --- | --- | --- |
| 22/09/2026 | 1 h | `10.20.8.30` | **2 548,99** | normal |
| 27/09/2026 | 1 h | `10.20.8.30` | **2 503,46** | normal |
| 25/09/2026 | 2 h | `10.20.8.30` | **2 491,15** | normal |
| 16/09/2026 | 1 h | `10.20.8.30` | **2 353,11** | normal |
| 18/09/2026 | 1 h | `10.20.8.30` | **2 161,69** | normal |

Les 1 704 lignes sont des **enregistrements bruts**, pas une affirmation que toutes les observations sont distinctes, complètes ou prêtes pour l'entraînement.

## Que fait `10.20.8.30` à 1 h du matin ?

**Elle réalise un transfert nocturne récurrent de gros volumes, compatible avec une tâche planifiée telle qu'une sauvegarde ou une synchronisation.** C'est l'hypothèse de lecture à retenir, sans la confondre avec un rôle machine démontré.

Le CSV contient une ligne à **1 h pour chacun des 14 jours**, du 14 au 27 septembre. Ces lignes sont toutes étiquetées **normal**, sans échec SSH, avec **un ou deux succès**, **un compte distinct** et **40 à 56 minutes** de session. Les volumes renseignés vont de **886,39 à 2 548,99 Mo** ; celui du **19 septembre manque** et ne doit pas être interprété comme un transfert nul. Une des cinq plus grosses observations a lieu à **2 h**, pas à 1 h.

Les plus gros volumes ne correspondent donc pas ici à des attaques **selon les étiquettes du kit**. Pour confirmer une sauvegarde, il faudrait l'inventaire de l'hôte, la tâche planifiée, sa destination et l'autorisation métier. **Un volume élevé seul ne prouve pas une exfiltration, et une étiquette normal ne garantit pas la légitimité d'une nouvelle connexion future.** Ce cas peut devenir un faux positif d'un détecteur d'anomalies : conserver cette référence pour l'après-midi.


### Preuves des exercices pandas — Captures du 21 octobre 2026

| Capture | Résultat observé |
| --- | --- |
| 10-19-32 | Chargement, aperçu et structure : 1 704 lignes, 11 colonnes ; sélection echecs_auth de type int64 |
| 10-20-00 | Maximum 298 échecs ; 1 566 lignes internes / 138 externes ; filtre > 50 avec cas normal et NaN visibles |
| 10-20-18 | Tri décroissant des échecs et dix premières lignes affichés |
| 10-23-43 | 1 704 lignes ; unique() affiche 138 IP distinctes (nunique() donne directement le nombre) ; 1 587 normal / 117 attaque ; filtre nocturne avec succès : 127 lignes |
| 10-25-37 | Exercice b : `print(df["ip_source"].nunique())` retourne directement 138 ; comptage demandé confirmé |
| 10-23-52 | Cinq plus gros volumes : 10.20.8.30, tous étiquetés normal ; maximum 2 548,99 Mo le 22/09 à 1 h |

Ces captures attestent les cellules visibles. Les trois erreurs de la section 5, la première cellule de versions et l’exécution complète/sauvegarde du notebook ne sont pas montrées. Hypothèse de sauvegarde nocturne toujours à confirmer par le contexte métier. Captures intégrées à la fiche Python de survie dans le mémo.

## Séquence 3.5 — Explorer et préparer les journaux

Corrigé et calculs indépendants sur CSV, complétés par quatre captures attestant certaines cellules A/B. Nettoyage encore non appliqué sur les captures ; aucun entraînement attesté.

## Mission 1 — Explorer : partie A

### Chargement et graphique à compléter

```python
df = pd.read_csv("hexalp_ssh_sept2026.csv")
print(df.shape)
df.head()
```

Pour le nuage de points du notebook :

```python
plt.scatter(
    df["echecs_auth"],
    df["comptes_distincts"],
    c=couleurs,
    alpha=0.6,
    s=15,
)
```

Les étiquettes servent ici à colorer et comprendre les exemples ; elles ne doivent pas être fournies comme caractéristique d'entrée. Le fichier brut contient **1 704 lignes et 11 colonnes**, et non exactement 1 700. Une ligne regroupe une activité horaire : elle ne décrit pas à elle seule l'ordre précis des connexions dans cette heure.

### A1 — Quelle proportion d'attaques ?

| Étiquette | Effectif brut | Proportion |
| --- | --- | --- |
| **normal** | 1 587 | **93,13 %** |
| **attaque** | 117 | **6,87 %** |
| **Total** | 1 704 | 100 % |

Les classes sont déséquilibrées : les observations normales dominent. Il s'agit des proportions du fichier fourni, pas d'un taux réel d'attaque généralisable à tout le SI.

### A2 — Toujours répondre normal : quelle justesse ?

Ce modèle aurait **1 587 / 1 704 ≈ 93,13 % de bonnes réponses**, mais **zéro attaque détectée** : rappel égal à **0 %**, 117 faux négatifs, aucun vrai positif et aucun faux positif. La précision des alertes serait indéfinie faute d'alertes ; un outil peut appliquer une convention d'affichage à préciser.

Il ne répond donc pas au besoin de Nadia. Cette référence montre pourquoi une bonne *accuracy* seule ne suffit pas : mesurer aussi faux positifs, faux négatifs, précision et rappel sur un jeu indépendant.

### A3 — Où les points bleus et rouges se mélangent-ils ?

Les zones ci-dessous sont définies explicitement et comptées sur le CSV brut pour étayer la lecture du futur graphique. « Mélange » signifie ici proximité dans une zone, pas nécessairement coordonnées exactement identiques.

| Zone des deux caractéristiques | Normal | Attaque | Ce qui risque d'échapper à un simple seuil |
| --- | --- | --- | --- |
| **0 à 5 échecs et 1 à 3 comptes** | 1 564 | 22 | Connexions avec identifiants valides ou activité discrète : peu d'échecs peut ressembler à une activité normale |
| **Plus de 5 à 25 échecs et au plus 10 comptes** | 19 | 16 | Essais de faible volume, parfois compatibles avec du password spraying, mêlés à des erreurs légitimes ; le type précis reste à confirmer |
| **Au moins 50 échecs et au moins 10 comptes** | 4 | 56 | Force brute et essais d'un scanner autorisé peuvent se ressembler |

Deux caractéristiques ne suffisent pas à interpréter l'intention. Horaires, origine, succès, durée et volume peuvent apporter du contexte, sans garantie de séparation parfaite. Une IP connue ou une étiquette du kit n'est pas une preuve de légitimité future.

### A4 — Qui est `10.20.1.250` ?

Les quatre observations normales les plus chargées en échecs correspondent à cette IP interne :

| Date | Heure | Échecs | Comptes distincts | Volume sortant (Mo) | Étiquette |
| --- | --- | --- | --- | --- | --- |
| 15/09/2026 | 21 h | 162 | 37 | 0,10 | normal |
| 15/09/2026 | 22 h | 138 | 42 | 0,10 | normal |
| 22/09/2026 | 21 h | 81 | 46 | 0,10 | normal |
| 22/09/2026 | 22 h | 83 | 25 | 0,10 | normal |

**Interprétation attendue : un scanner interne effectuant un audit planifié**, compatible avec l'exemple d'audit autorisé étudié en 3.1. La répétition sur deux mardis, aux mêmes heures, et l'étiquette normal soutiennent cette lecture. **Le CSV ne fournit toutefois ni inventaire de la machine ni ticket d'autorisation** : son rôle et le motif exact retenu par Hugo restent à confirmer. Ne pas qualifier cet audit de mensuel d'après ces données : deux occurrences sont espacées d'une semaine.

Pour un vrai incident, vérifier propriétaire, calendrier d'audit, périmètre et preuve de qualification. `fail2ban_ban = 0` ne prouve pas, à lui seul, une exemption configurée ou un accord métier.

## Mission 2 — Préparer : partie B

### B1 — Les cases vides : une décision à justifier

**90 valeurs manquent dans `octets_sortants_mo`** ; les dix autres colonnes ne contiennent pas de champ vide dans le fichier reçu. Les manques sont concentrés sur :

| Période visible dans le CSV | Lignes concernées |
| --- | --- |
| **19 septembre : heures 0 à 11 incluses** | 20 |
| **22 septembre : heures 10 à 15 incluses** | 70 |
| **Total** | **90**, dont **81 normal et 9 attaque** |

Les heures indiquent les tranches agrégées affectées, pas les instants exacts de début/fin de panne. Ces absences représentent environ **5,28 %** du fichier. Le contexte de Sofia les attribue à la sonde ; le vide ne signifie pas absence de trafic.

| Option proposée | Ce qu'elle conserve | Ce qu'elle perd ou suppose |
| --- | --- | --- |
| **Supprimer les lignes** | Valeurs réellement mesurées, sans volume inventé | Retire aussi les autres informations valides des lignes concernées et neuf attaques étiquetées ; peut biaiser la couverture temporelle et l'évaluation |
| **Remplacer par zéro** | Toutes les observations | Assimile « mesure indisponible » à « aucun volume sortant », pouvant masquer une exfiltration ; hypothèse injustifiée ici |
| **Remplacer par la médiane** | Toutes les observations avec une valeur centrale moins influencée par les extrêmes | Fabrique un volume ordinaire pour une observation potentiellement extrême ; efface une information importante et peut masquer l'exfiltration. La médiane doit être apprise sur le seul entraînement, jamais sur tout le jeu avant le test |

**Choix pour ce TP : supprimer les lignes incomplètes**, afin de ne pas inventer un volume et de conserver la suite simple prévue par le kit. Ce choix ne résout pas la panne : les 90 observations doivent être conservées à part et signalées comme **non couvertes par cette chaîne complète**, pas présumées normales. Il faudra comparer ultérieurement la couverture et la qualité avec une autre stratégie.

La ligne à placer dans la cellule « votre choix » est :

```python
df = df.dropna(subset=["octets_sortants_mo"]).copy()
```

Le sous-ensemble cible le champ réellement manquant plutôt que supprimer silencieusement une ligne pour n'importe quel futur champ vide. Avant cette ligne, garder si besoin les observations exclues dans une variable distincte :

```python
observations_sans_volume = df[df["octets_sortants_mo"].isna()].copy()
```

**Résultats attendus d'après les comptages indépendants :** 1 614 lignes conservées, dont **1 506 normal et 108 attaque** ; zéro valeur manquante restante pour le volume. Ce sont des références à vérifier lors de l'exécution, pas une sortie de notebook reçue.

En exploitation, une panne de mesure demande une alerte de qualité des données ou une chaîne de détection dégradée sur les autres variables, explicitement évaluée. Une suppression silencieuse des observations serait dangereuse. Une imputation éventuelle doit être apprise après la séparation, puis appliquée au test sans recalcul sur ce test. [Scikit-learn — éviter les fuites lors de la préparation](https://scikit-learn.org/stable/common_pitfalls.html).

### Transformer origine en externe

```python
df["externe"] = (df["origine"] == "externe").astype(int)
```

Le CSV reçu n'utilise que `interne` et `externe`. Contrôler ces valeurs avant la transformation : toute valeur inconnue serait sinon convertie silencieusement en zéro et confondue avec interne. Le codage numérique n'établit pas qu'externe signifie malveillant, ni qu'interne signifie sûr.

### B2 — Tableau des caractéristiques renseigné

| Colonne | Donnée au modèle ? | Pourquoi ? |
| --- | --- | --- |
| **date** | **Non dans ce premier modèle** | Risque d'apprendre le calendrier particulier du petit jeu et ses incidents. Conserver pour analyse, séparation temporelle et traçabilité ; des caractéristiques calendaires justifiées resteraient possibles dans un autre modèle |
| **heure** | **Oui** | Contexte temporel, disponible après la tranche observée ; une activité nocturne peut aussi être légitime. Le codage 0–23 est simple, sans prétendre représenter parfaitement le cycle |
| **ip_source** | **Non** | Identifiant à forte cardinalité : risque de mémorisation et faible généralisation aux nouvelles IP. À conserver pour l'analyste ; une IP n'est pas intrinsèquement une étiquette ni une fuite automatique |
| **origine → externe** | **Oui, sous forme binaire `externe`** | Contexte réseau disponible ; ne pas inclure aussi le texte brut `origine`. Ce n'est pas une preuve de malveillance |
| **echecs_auth, succes_auth, comptes_distincts** | **Oui** | Résument volume d'essais, réussites et dispersion des comptes ; disponibles à la fin de l'heure |
| **duree_session_min, octets_sortants_mo** | **Oui, après traitement des valeurs manquantes** | Peuvent aider à repérer une activité de session ou un transfert inhabituel ; les transferts de sauvegarde restent un piège possible |
| **fail2ban_ban** | **Non pour la comparaison indépendante retenue** | Résultat d'un dispositif de sécurité qu'on souhaite comparer au modèle. L'inclure peut faire apprendre sa décision et créer une dépendance circulaire ; sa disponibilité temporelle doit aussi être vérifiée. Ce n'est pas automatiquement une fuite dans tout projet : le choix dépend du but et du moment de prédiction |
| **etiquette** | **Jamais dans X** | C'est la réponse de référence pour le classifieur et l'évaluation. Dans `y` pour le supervisé ; exclue de l'entraînement d'Isolation Forest et utilisée seulement pour interpréter ses résultats |

### Liste à reporter dans le notebook

```python
CARACTERISTIQUES = [
    "heure",
    "externe",
    "echecs_auth",
    "succes_auth",
    "comptes_distincts",
    "duree_session_min",
    "octets_sortants_mo",
]

X = df[CARACTERISTIQUES]
y = (df["etiquette"] == "attaque").astype(int)

print(X.shape, y.sum(), "attaques")
```

Avec le choix de suppression décrit plus haut, référence attendue : **`(1614, 7) 108 attaques`**. Ne pas l'inscrire comme sortie réelle avant d'avoir exécuté les cellules dans la VM.

## Fuite de données et moment de la prédiction

Une **fuite d'information en apprentissage — data leakage** survient quand la préparation, l'apprentissage ou la sélection utilisent des informations indisponibles au moment réel de la prédiction ou réservées au test. Donner `etiquette` dans `X` fournirait directement la réponse ; calculer une médiane sur tout le jeu ferait participer le test à la préparation. Ce sens est distinct d'une fuite de confidentialité vers un fournisseur externe.

Ici, on classe une **tranche horaire terminée** : volume, durée et succès de cette heure peuvent être disponibles. On ne peut pas prétendre utiliser ces valeurs finales pour détecter dès la première tentative de l'heure. En production, vérifier délais de collecte et mode de calcul des agrégats ; concevoir un autre protocole si une détection en cours d'heure est nécessaire.

La date et l'IP exclues ne sont pas interdites universellement. Leur exclusion limite ici la mémorisation et clarifie l'expérience. Il faut aussi réserver des exemples indépendants pour évaluer la généralisation ; une bonne préparation seule ne démontre aucune performance.


### Preuves A/B — Captures du 21 octobre 2026

| Capture | Observation et limite |
| --- | --- |
| 10-35-30 | CSV chargé, dimensions (1704, 11) et aperçu visibles |
| 10-35-37 | Définition de couleurs et graphique exécutés ; NameError corrigée |
| 10-38-54 | Répartition des manques sur les deux périodes, codage interne 0/externe 1 ; cellule de nettoyage encore ___, sans sortie |
| 10-39-09 | Sept caractéristiques définies ; X=(1704, 7), 117 attaques : jeu brut encore présent |

**À faire avant l’entraînement avec le choix retenu :** appliquer dropna sur octets_sortants_mo, vérifier zéro manque et recréer X/y ; références attendues (1614, 7), 108 attaques. Un changement de df ne recalcule pas X/y automatiquement. Ces résultats nettoyés ne sont pas encore attestés par capture.

## Séquence 3.6 — Le classifieur supervisé

Sept captures de l’apprenant attestent nettoyage puis entraînement : 1 614 lignes complètes, 1 129 entraînement / 485 test, arbre profondeur 3, graine prévue 42. Capture de la matrice : 453 VN, 0 FP, 4 FN, 28 VP. Le fichier notebook exécuté reste à rapatrier depuis la VM ; aucune nouvelle exécution par l’assistant.

## C1 — Traduire les règles de l'arbre

L'arbre affiché a une **profondeur maximale de 3 et six feuilles**. Ses règles sont retranscrites depuis le graphique de la capture, pas depuis une sortie `export_text` montrée : cette cellule ne porte pas de résultat visible.

| Conditions successives | Classe prédite |
| --- | --- |
| **Au plus 3 comptes** et durée cumulée **≤ 0,5 minute** | attaque |
| **Au plus 3 comptes** et durée cumulée **> 0,5 et ≤ 64 minutes** | normal |
| **Au plus 3 comptes** et durée cumulée **> 64 minutes** | attaque |
| **Au moins 4 comptes** et origine **externe** | attaque |
| **Au moins 4 comptes**, origine **interne**, heure **≤ 19** | attaque |
| **Au moins 4 comptes**, origine **interne**, heure **≥ 20** | normal |

Les comptes sont entiers : le seuil graphique **3,5** sépare 3 de 4 comptes. L'heure est entière : **19,5** sépare 19 h de 20 h. Les durées du CSV sont cumulées sur la tranche : **64 minutes ne désignent pas nécessairement une seule session**, plusieurs sessions peuvent se chevaucher.

On retrouve l'intérêt du **nombre de comptes** exploré au J1, mais pas la règle initiale « échecs > 20 ». Malgré les sept variables proposées, cet arbre utilise seulement **comptes distincts, durée, origine et heure**. Il ne teste directement **ni échecs SSH ni volume sortant**.

**Branche fragile :** au moins quatre comptes, origine interne et horaire ≥ 20 h est classé normal. Cette règle peut refléter les exemples d'audit vus à ces horaires, sans connaître leur autorisation. La feuille repose sur **trois exemples d'entraînement** : ce n'est pas une règle métier sûre pour toutes les connexions internes nocturnes.

## C2 — Erreurs, justesse et indicateurs utiles

| Étiquette réelle / prédiction | Prédit normal | Prédit attaque |
| --- | --- | --- |
| **normal** | **453 VN** | **0 FP** |
| **attaque** | **4 FN** | **28 VP** |

| Indicateur sur les 485 observations test | Arbre profondeur 3 | Toujours normal, sur le même test |
| --- | --- | --- |
| Justesse — accuracy | **481 / 485 = 99,18 %**, affiché `0.992` | **453 / 485 = 93,40 %** |
| Rappel des attaques | **28 / 32 = 87,5 %** | **0 %** |
| Précision des alertes attaque | **28 / 28 = 100 %** sur ce test | Non définie, aucune alerte |
| Faux positifs / faux négatifs | **0 / 4** | **0 / 32** |

La référence A2 sur le **CSV brut** était 93,13 % ; la comparaison à périmètre identique vaut ici 93,40 %. Nadia doit examiner **rappel et faux négatifs**, mais aussi précision, faux positifs, volume d'alertes et impact métier. Le zéro faux positif sur 453 normales ne garantit pas zéro faux positif futur.

Avec **32 attaques**, une seule erreur représente **1/32 = 3,125 points de rappel**, et non exactement la variation calculée sur 35 attaques dans la consigne générique. Les scores arrondis ne doivent pas masquer ces petits effectifs.

## C3 — Examiner chaque erreur

La capture ne montre **aucun faux positif** et les quatre faux négatifs suivants. Les interprétations d'attaque restent des hypothèses : le CSV donne une étiquette, pas un compte rendu d'incident.

| Index du CSV | Date / heure | Source | Échecs / succès | Comptes | Durée min / volume Mo | Explication proposée |
| --- | --- | --- | --- | --- | --- | --- |
| **140** | 15/09, 0 h | `203.0.113.157` | 0 / 1 | 1 | 57 / 905,12 | Connexion réussie compatible avec un compte compromis et un transfert non autorisé ; l'arbre voit un compte et une durée ordinaire |
| **1468** | 25/09, 0 h | `203.0.113.203` | 0 / 1 | 1 | 42 / 49,25 | Connexion valide peu volumineuse, potentiellement usurpée ; le volume réduit ne prouve pas une activité légitime |
| **1671** | 27/09, 3 h | `203.0.113.173` | 2 / 2 | 1 | 24 / 398,80 | Quelques échecs puis des succès possibles dans l'heure ; leur ordre n'est pas fourni. Profil compatible avec une intrusion discrète |
| **1150** | 23/09, 2 h | `198.51.100.10` | 0 / 2 | 1 | 54 / 1 053,16 | Transfert nocturne potentiellement malveillant après succès ; l'arbre n'utilise pas le volume sortant |

Ces quatre lignes suivent la même branche : **un compte et durée entre 0,5 et 64 minutes → normal**. L'origine externe et l'horaire nocturne ne sont pas examinés dans cette branche. L'arbre ne déduit donc pas la légitimité d'un accès ; il applique un raccourci appris sur le jeu.

## C4 — Quelle profondeur retenir ?

| `max_depth` demandé | Score entraînement | Score test | FP | FN | Feuilles |
| --- | --- | --- | --- | --- | --- |
| **1** | 0,985 | 0,986 | 1 | 6 | 2 |
| **3** | 0,996 | 0,992 | 0 | 4 | 6 |
| **10** | 1,000 | 0,998 | 0 | 1 | 8 |
| **None** | 1,000 | 0,998 | 0 | 1 | 8 |

**Pour expliquer l'expérience à Nadia, je conserve l'arbre de profondeur 3 comme référence lisible**, dont toutes les branches sont analysées ici. **Pour améliorer la détection, le candidat demandé à profondeur 10 mérite une validation**, puisqu'il manque une seule attaque sur ce test contre quatre ; il n'a que huit feuilles. Le paramètre 10 est une limite, pas la profondeur réellement atteinte, non affichée dans cette capture.

Je ne retiens donc pas 3 comme optimum démontré ni 10 comme meilleur en production. La comparaison a utilisé les mêmes données de test pour choisir un réglage : ce jeu joue désormais aussi un rôle de validation. Avant une conclusion finale, réserver un autre test, idéalement temporel, puis contrôler rappel, faux positifs, stabilité et lisibilité. Un score d'entraînement parfait est un signal à examiner, pas une preuve automatique de surapprentissage ; l'écart et la généralisation doivent être vérifiés.

La boucle de l'expérience utilise la variable `modele`. Elle ne remplace pas automatiquement **`arbre`**, qui reste ici celui de profondeur 3 pour les erreurs et comparaisons suivantes.

## C5 — Que gagne l'arbre par rapport à fail2ban ?

La comparaison porte sur **les mêmes 485 lignes de test**, avec les mêmes étiquettes. Les décisions fail2ban sont celles du **CSV fictif**, pas un test de bannissement exécuté sur le bastion.

| Indicateur | fail2ban historique | Arbre profondeur 3 |
| --- | --- | --- |
| Attaques détectées | **17 / 32** | **28 / 32** |
| Rappel attaque | **53,125 %**, affiché 0,53 | **87,5 %**, affiché 0,88 |
| Faux négatifs | **15** | **4** |
| Faux positifs | **0** | **0** |
| Précision attaque | 100 % sur ce test | 100 % sur ce test |

Le rapport fail2ban arrondi et les supports permettent de reconstituer **17 VP, 15 FN et 453 VN** ; sa justesse vaut 470/485 ≈ 96,91 %. La liste complémentaire montre **11 attaques** repérées par l'arbre sans bannissement historique : essais de faible volume sur plusieurs comptes, activité interne répartie, mais aussi une ligne avec **222 échecs** et `fail2ban_ban=0`.

**Ne pas expliquer ce dernier cas par certitude :** l'agrégat horaire ne donne ni cadence dans dix minutes, ni configuration, ni exemption, ni état réel de la jail. La colonne peut refléter une limite ou une convention de génération du kit ; investiguer avant d'affirmer un contournement précis.

Le gain est **11 détections dans ce test**, soit **34,375 points de rappel**. L'arbre ne remplace pas automatiquement fail2ban : il produit ici un avis après agrégation, alors que fail2ban peut agir sur des échecs en cours de fenêtre. Périmètre, moment et action sont différents.

## C6 — Pourquoi ne pas fournir `fail2ban_ban` au modèle ?

Le modèle pourrait se reposer sur la décision d'un contrôle existant plutôt que repérer des comportements complémentaires. Cela brouillerait la comparaison indépendante avec fail2ban. Si ses seuils, exemptions ou sa disponibilité changent, cette caractéristique peut changer de sens et dégrader la généralisation.

Ce n'est pas une fuite automatique dans tous les projets : une décision connue au moment de prédire peut être une donnée utilisable pour un autre objectif. Ici, l'exclusion évite dépendance circulaire et raccourci d'apprentissage ; un signal calculé après le moment visé de détection serait en plus une fuite temporelle. L'étiquette reste exclue de `X` dans tous les cas.

## Pour Nadia — Trois phrases sans jargon

> L'outil compare le nombre de comptes utilisés, la durée des connexions, leur origine et l'heure à des habitudes apprises sur nos exemples. Sur 32 attaques du test, il en a signalé 28 et en a manqué 4, sans alerter à tort sur les 453 observations normales. Il aide à choisir ce qu'il faut examiner, mais certaines connexions réussies ou internes peuvent lui échapper et il ne bloque rien.

## Retour aux cinq scénarios de 3.1

Ces réponses sont une **lecture des règles apprises**, pas cinq tests d'attaque exécutés. Les scénarios incomplets ne permettent pas une prédiction unique.

| Scénario | Ce que ferait l'arbre de profondeur 3 | Limites |
| --- | --- | --- |
| **1 — 200 mots de passe sur root** | Avec un seul compte et aucune session réussie, durée nulle → **attaque** | Ce n'est pas le seuil de 200 échecs qui le fait réagir ; une durée entre 1 et 64 minutes sur un compte changerait la branche finale |
| **2 — Un essai lent sur six comptes** | **Attaque** si au moins quatre comptes se trouvent dans la même observation et source externe ; avec au plus trois comptes et aucune session, durée nulle → attaque également | L'agrégation horaire et le placement des six essais doivent être vérifiés ; les caractéristiques exactes du cas ne sont pas toutes données |
| **3 — Succès à 23 h et 1 Go sortant** | Pour un compte, **normal si durée > 0,5 et ≤ 64 minutes**, attaque au-delà de 64 minutes ou à durée ≤ 0,5 | L'arbre n'utilise pas le volume. Sans durée, pas de verdict unique ; les quatre FN illustrent cette fragilité |
| **4 — Poste interne, dix comptes de service** | Si dix comptes sont présents dans une observation visible : **attaque jusqu'à 19 h, normal dès 20 h** | Aucun modèle n'observe des connexions directes à la production absentes des logs du bastion ; répartition entre hôtes et heures inconnue |
| **5 — Scanner légitime, 150 échecs** | Pour un scanner interne visant au moins quatre comptes, **normal dès 20 h**, attaque plus tôt | Horaire et nombre de comptes nécessaires ; les audits du kit à 21/22 h peuvent passer, sans garantie sur les autres audits |

### Que révèle la branche des connexions internes ?

Un poste interne déjà compromis reste une source d'attaque possible. L'arbre lui accorde une confiance injustifiée dans certaines conditions horaires, apprises sur quelques exemples légitimes ; une activité malveillante qui ressemble à ces exemples peut donc être manquée. Il faut tester des scénarios internes variés, enrichir la qualification et revoir le modèle, **sans transformer « interne » ou une plage horaire en exemption générale**.


## Séquence 3.7 — La détection d’anomalies

Quatre captures du 21 octobre attestent Isolation Forest : 49 alertes, 44 VP, 5 FP, 64 FN à contamination 0,03 sur les 1 614 observations d’ajustement. Top15 sans étiquette puis révélation visibles ; qualifications à l’aveugle non documentées.

## Mission 1 — Le travail de l'analyste

### Étape 1 — Compléter la première cellule

Pour un premier essai cohérent avec la capacité évoquée en D4, on propose **0,03**. C'est un réglage initial à justifier, pas un résultat de détection.

```python
iforest = IsolationForest(contamination=0.03, random_state=GRAINE)
iforest.fit(X)  # aucune étiquette fournie

df["score_anomalie"] = iforest.decision_function(X)
df["anomalie"] = iforest.predict(X) == -1

print(df["anomalie"].sum(), "observations signalées sur", len(df))
```

Remplacer le premier `___` par **`0.03`**, celui de `fit` par **`X`**. Conserver la valeur effectivement choisie dans le carnet. Le classement des scores n'est pas un jugement de malveillance ; une observation signalée peut être légitime.

### D1 — Qualifier les quinze premières lignes, sans voir l'étiquette

La cellule du kit propose un tableau qui inclut `etiquette`. Pour respecter la mission à l'aveugle, utiliser **deux affichages successifs** :

```python
colonnes = [
    "date", "heure", "ip_source", "origine", "echecs_auth", "succes_auth",
    "comptes_distincts", "octets_sortants_mo", "score_anomalie", "etiquette",
]

top15 = df.sort_values("score_anomalie").head(15).copy()
colonnes_lecture = [c for c in colonnes if c != "etiquette"]
display(top15[colonnes_lecture])
```

**Avant d'exécuter la cellule suivante**, noter pour chacune des quinze lignes son index, les indices observés, la qualification — attaque probable, comportement légitime ou à investiguer — et la preuve métier manquante. Ne pas deviner l'ordre des lignes à partir de leur IP.

| Profil à rechercher | Qualification provisoire possible | Vérification nécessaire |
| --- | --- | --- |
| Nombreux essais et comptes, aucune session réussie | Attaque probable | Source, autorisation d'audit et traces détaillées |
| Transfert nocturne récurrent d'une machine de sauvegarde | Comportement légitime si l'autorisation est confirmée, sinon à investiguer | Tâche, destination, volume attendu et propriétaire |
| Volume ou durée inhabituels après succès | À investiguer, éventuellement attaque probable avec d'autres indices | Compte, destination et activité métier |
| Activité d'administration pendant un incident | À investiguer sans conclure sur le seul score | Ticket, administrateur et actions réellement effectuées |

Ensuite seulement :

```python
display(top15[["etiquette"]])
```

**Classement observé dans les captures :** indices **763, 836, 1624, 729, 1458, 1303, 995, 1536, 1296, 1464, 1301, 838, 1633, 1694, 986**. La comparaison ultérieure affiche **attaque pour les quinze**. Les captures montrent l'affichage sans étiquette puis leur révélation, mais pas des qualifications manuscrites ou enregistrées entre les deux : **un classement analyste à l'aveugle n'est donc pas attesté**.

Lecture proposée **après consultation des étiquettes**, sans lui attribuer un caractère aveugle :

| Index | Indices visibles | Qualification argumentée proposée après coup |
| --- | --- | --- |
| **763** | Externe, 2 échecs/2 succès, 1 compte, 1 472,70 Mo | À investiguer : transfert élevé après connexions réussies ; autorisation et destination à vérifier |
| **836** | Externe, 1 échec/2 succès, 1 compte, 1 239,32 Mo | À investiguer : même limite, le volume seul ne prouve pas l'exfiltration |
| **1624** | Externe, 289 échecs, 63 comptes, aucun succès | Attaque probable de recherche d'accès ; vérifier l'absence d'audit autorisé |
| **729** | Externe, 270 échecs, 58 comptes, aucun succès | Attaque probable, essais massifs sur plusieurs comptes |
| **1458** | Externe, 262 échecs, 59 comptes, aucun succès | Attaque probable, mêmes indices de recherche d'accès |
| **1303** | Externe, 170 échecs, 79 comptes, aucun succès | Attaque probable, forte dispersion des comptes |
| **995** | Externe, 220 échecs, 78 comptes, aucun succès | Attaque probable, essais massifs |
| **1536** | Externe, 222 échecs, 73 comptes, aucun succès | Attaque probable ; ne pas déduire l'état réel de fail2ban de ce seul profil |
| **1296** | Externe, 235 échecs, 72 comptes, aucun succès | Attaque probable, essais massifs |
| **1464** | Externe, 1 échec/2 succès, 1 compte, 702,07 Mo | À investiguer : transfert inhabituel à rapprocher du contexte |
| **1301** | Externe, 298 échecs, 18 comptes, aucun succès | Attaque probable, force brute possible |
| **838** | Externe, 2 échecs/2 succès, 1 compte, 1 073,84 Mo | À investiguer : accès valide possible et transfert important |
| **1633** | Externe, 248 échecs, 23 comptes, aucun succès | Attaque probable, essais massifs |
| **1694** | Externe, 261 échecs, 49 comptes, aucun succès | Attaque probable, essais massifs |
| **986** | Externe, 142 échecs, 73 comptes, aucun succès | Attaque probable, forte dispersion des comptes |

Le score le plus bas du classement est **−0,063548**, pour l'index 763 ; c'est un score relatif, pas une probabilité. Le top 15 contient uniquement des attaques de référence, mais cela ne décrit pas toute la file de **49** alertes.

### Étape 2 — Évaluer les alertes et les erreurs

```python
pd.crosstab(df["anomalie"], df["etiquette"], margins=True)
```

Lire les cellules : **True/attaque = VP**, **True/normal = FP**, **False/attaque = FN**, **False/normal = VN**. L'évaluation utilise les étiquettes ; l'ajustement du détecteur ne les utilise pas.

```python
# Faux positifs par source
print(df[df["anomalie"] & (df["etiquette"] == "normal")]
      ["ip_source"].value_counts())

# Attaques manquées : ce code ajoute une vue utile pour D3
display(df[(~df["anomalie"]) & (df["etiquette"] == "attaque")][colonnes])
```

### Résultats observés au réglage initial 0,03

| Étiquette réelle / signalement | Non signalé | Signalé |
| --- | --- | --- |
| **normal** | **1 501 VN** | **5 FP** |
| **attaque** | **64 FN** | **44 VP** |

Le total est **1 614**, dont **49 signalées**. Calculés à partir des effectifs observés : **précision = 44/49 ≈ 89,80 %**, **rappel = 44/108 ≈ 40,74 %**, justesse = 1 545/1 614 ≈ **95,72 %**. Le bon classement du top 15 ne doit pas masquer les **64 attaques non signalées**.

Ces métriques concernent le jeu ayant servi à ajuster Isolation Forest ; elles ne constituent pas une performance sur un jeu indépendant.

### D2 — Qui sont les faux positifs ? Sont-ils vraiment atypiques ?

**Cinq faux positifs observés : trois lignes de `10.20.1.250` et deux de `10.20.8.30`.** Ils correspondent aux profils de scanner et de sauvegarde discutés précédemment. Le détail individuel de ces cinq lignes n'est pas affiché dans cette capture ; ne pas en inventer les dates ou les scores.

Un comportement rare mais légitime peut être une **vraie anomalie statistique** et une **fausse alerte d'attaque**. Pour le qualifier, il manque au détecteur le rôle de la machine, les autorisations et fenêtres d'audit ou de sauvegarde, les destinations et l'historique métier. Ajouter ce contexte après détection ou évaluer des profils par rôle, sans supposer qu'une IP connue est toujours sûre.

### D3 — Quelles attaques passent sous le radar ?

**64 attaques non signalées sont comptées à contamination 0,03. Leur liste détaillée n’est pas affichée dans les captures : il reste à exécuter la vue des FN ci-dessus pour les expliquer individuellement**, sans les déduire du seul nom Isolation Forest. Les attaques qui ressemblent aux usages fréquents peuvent être difficiles à isoler : accès valides discrets, essais lents et transferts proches des pratiques ordinaires. Le nuage échecs/comptes de la partie A montre le recouvrement de certains profils, mais Isolation Forest dispose ici de sept variables : le graphique seul ne prédit pas son résultat.

Relier chaque erreur aux caractéristiques et au contexte. Les 90 lignes retirées pour absence de volume sont **hors de l'évaluation**, pas des faux négatifs calculés de ce modèle : elles demandent un suivi distinct de couverture.

### Étape 3 — Comparer les contaminations

Exécuter la boucle du notebook **après D1–D3** :

```python
for c in [0.03, 0.05, 0.10]:
    m = IsolationForest(contamination=c, random_state=GRAINE).fit(X)
    signale = m.predict(X) == -1
    vrais = (signale & (y == 1)).sum()
    faux = (signale & (y == 0)).sum()
    rates = (~signale & (y == 1)).sum()
    print(
        f"contamination={c:.2f} | alertes={signale.sum():4d}"
        f" | vraies attaques={vrais:3d} | faux positifs={faux:3d}"
        f" | attaques ratées={rates:3d}"
    )
```

La boucle crée `m` et ne remplace pas automatiquement `iforest` ni les colonnes de `df`. Pour adopter un nouveau réglage, réajuster explicitement le modèle de référence et recalculer scores et drapeaux ; conserver la version et le réglage de chaque résultat.

### D4 — Trente alertes par semaine : quel choix ?

Le jeu couvre **deux semaines**. Trente alertes par semaine représentent donc environ **60 sur la période**, à comparer à des observations signalées, pas automatiquement à 60 incidents distincts.

| Contamination | Ordre de grandeur sur 1 614 lignes | Moyenne hebdomadaire sur deux semaines |
| --- | --- | --- |
| **0,03** | Environ **48–49** | Environ **24–25** |
| **0,05** | Environ **81** | Environ **40–41** |
| **0,10** | Environ **161–162** | Environ **81** |

Ce sont des calculs de budget, **pas les sorties observées** ; seuils, égalités de scores et arrondis peuvent modifier les nombres exacts. Les futurs flux peuvent aussi avoir une autre proportion signalée.

### Mesures observées dans la boucle

| Contamination | Alertes / 2 semaines | VP | FP | FN | Précision | Rappel | Moyenne alertes / semaine |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **0,03** | **49** | **44** | **5** | **64** | 89,80 % | 40,74 % | 24,5 |
| **0,05** | **81** | **64** | **17** | **44** | 79,01 % | 59,26 % | 40,5 |
| **0,10** | **162** | **104** | **58** | **4** | 64,20 % | 96,30 % | 81 |

**Parmi ces trois valeurs, 0,03 est la seule compatible avec une moyenne de 30 alertes hebdomadaires**, mais elle manque **64 attaques sur 108** dans ce jeu. Ce compromis n'est pas automatiquement acceptable : Nadia doit l'arbitrer avec les autres contrôles et la charge réelle. Les dates des alertes ne sont pas toutes montrées : une moyenne de 24,5 ne garantit pas qu'aucune semaine ni journée ne dépasse la capacité. À 0,10, le meilleur rappel coûte 58 fausses alertes et 81 alertes/semaine en moyenne.

Les types exacts des 64 attaques manquées restent à établir depuis leur détail ; ne pas présenter les profils plausibles de D3 comme une analyse déjà effectuée des 64 lignes.

Un seuil plus restrictif ne garantit pas un risque acceptable. Suivre aussi la concentration des alertes par jour, leur durée de traitement, la déduplication et la détection complémentaire de l'arbre/fail2ban. Le budget de 30 concerne l'ensemble du dispositif si les outils sont combinés, pas une enveloppe indépendante pour chacun. Aucun réglage n'est accepté définitivement sans décision explicite.

### D5 — Julien pendant l'incident WMS du 24 septembre

Pour répondre **« sont-elles signalées ? »**, afficher le drapeau, absent de la liste `colonnes` initiale :

```python
masque_julien = (
    (df["ip_source"] == "10.20.2.14")
    & (df["date"] == "2026-09-24")
    & df["heure"].between(2, 4)
)
display(df.loc[masque_julien, colonnes + ["anomalie"]])
```

La lecture indépendante du CSV confirme les trois observations suivantes ; les scores et drapeaux sont désormais observés dans la capture :

| Heure | Échecs / succès | Comptes | Durée cumulée min | Volume Mo | Étiquette du kit | Signalée par Isolation Forest ? |
| --- | --- | --- | --- | --- | --- | --- |
| **2 h** | 1 / 4 | 2 | 60 | 22,07 | normal | **Non : False**, score 0,089614 |
| **3 h** | 2 / 7 | 2 | 33 | 17,49 | normal | **Non : False**, score 0,123859 |
| **4 h** | 2 / 3 | 2 | 55 | 19,80 | normal | **Non : False**, score 0,113330 |

La consigne rattache cette machine à **Julien pendant l'incident WMS**. **Aucune de ces trois observations n’est signalée au réglage initial 0,03.** Ces mesures ne montrent **ni le contenu collé dans le chatbot, ni le secret de configuration divulgué au J2** : ce sont des agrégats SSH, pas le contenu de la navigation web. Une activité SSH normale n'exclut donc pas un usage IA non autorisé. Si elles sont signalées, cela peut simplement refléter le dépannage nocturne ; si elles ne le sont pas, cela ne signifie pas que l'usage du chatbot était sûr.

## Mission 2 — Comparer les deux approches

Le tableau distingue le résultat supervisé **déjà attesté** des hypothèses Isolation Forest **à vérifier**.

| Critère | Arbre de décision | Isolation Forest |
| --- | --- | --- |
| **Besoin d'étiquettes ?** | Oui pour apprendre ; test comparé aux références de Hugo | Non pour ajuster ; étiquettes utilisées ensuite pour mesurer les erreurs par rapport aux attaques |
| **Signaler un type d'attaque jamais vu ?** | Parfois, si caractéristiques communes aux attaques apprises ; aucune garantie | Possible si le comportement est atypique dans les caractéristiques disponibles ; une attaque discrète peut passer |
| **Expliquer l'alerte à Nadia ?** | Chemin de questions lisible : comptes, durée, origine, heure dans l'arbre observé | Expliquer score, profil et écarts au contexte ; pas de règle courte équivalente à un seul arbre, et le score seul n'explique pas une intention |
| **Faux positifs typiques chez Hexalp** | **Aucun sur les 453 normales du test** ; audits hors horaires appris ou tâches à durée atypique sont des risques à tester | **5 FP observés : 3 lignes scanner, 2 sauvegarde**, atypiques mais étiquetées normal |
| **Faux négatifs typiques chez Hexalp** | **Quatre attaques manquées** : un compte et durée de 24–57 minutes ; fragilité de la branche interne à partir de 20 h | **64 FN sur 108 attaques à 0,03** ; types détaillés à examiner, profils proches des usages fréquents possibles |
| **Maintenance dans le temps** | Étiquettes revues, exemples nouveaux, validation indépendante/temporelle, suivi des erreurs et réentraînement versionné | Référence représentative, suivi de dérive et des pannes de mesure, revue analyste, seuil adapté à la charge et réajustement versionné |

### Choisir ou combiner ?

**Proposer une combinaison évaluée**, en maintenant les rôles distincts : fail2ban traite sa règle opérationnelle existante ; l'arbre fournit un avis supervisé ; Isolation Forest fait remonter des profils atypiques. Les modèles du TP restent sans action de blocage.

Pour la file analyste, regrouper les observations par contexte et distinguer **accord des deux modèles** et **désaccord**. Une sélection par **OU** peut augmenter la couverture mais aussi le bruit ; exiger **ET** peut réduire le bruit au prix d'attaques manquées par un des deux. Ne pas supprimer systématiquement les alertes « anomalie seule ». Mesurer l'union, les doublons, les erreurs et la charge sur **un même jeu indépendant**, plutôt que juxtaposer le test de l'arbre et l'analyse de tout `X`.

La revue humaine doit conserver les raisons, la priorité et les preuves utiles. Aucune hausse chiffrée de détection de la combinaison ne peut être annoncée avant ces essais.

## Sauvegardes et listes blanches — Repère pour le J4

Le contexte pédagogique décrit la sauvegarde comme une activité légitime potentiellement atypique. Son signalement est désormais confirmé pour deux lignes à 0,03. Une liste blanche permanente sur son IP pourrait masquer une compromission de cette machine ; préférer un contexte précis — tâche, horaire, destination, volume et autorisation — avec contrôle des écarts et revue. Cette piste est conservée pour le J4, sans préparer ses activités.


### Preuves conservées dans le mémo

Captures 11-03-41 : fit et top15 ; 11-04-12 : matrice/FP/contaminations ; 11-05-12 : quinze étiquettes attaque ; 11-06-22 : Julien False aux trois heures. Détail des FN et notebook exécuté à rapatrier. Aucun blocage effectué.

## Séquence 3.8 — Le script de détection

Script detection_ssh.py complété avec assistance, commentaires à relire personnellement. Choix : sept caractéristiques, dropna volumes manquants, arbre profondeur3, contamination0,03, graine42. Export union des deux modèles, aucun blocage. Sources du kit préservées.

Vérifications exécutées par l’assistant sur données fictives, dans un venv temporaire Python3.14.4 avec les dépendances directes du kit. Ces essais ne sont pas présentés comme une exécution dans la VM de l’apprenant. Logs, versions et empreintes sont dans preuves/verification_script.md.

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


### Preuve d'exécution dans la VM — 21 octobre 2026

Deux captures 11-20-40 et 11-20-55 montrent l'exécution `python detection_ssh.py --graine 7 --sortie alertes_graine7.csv` dans le venv Debian. Résultats visibles : arbre test 0 FP/4 FN/28 VP ; fail2ban 0 FP/14 FN/18 VP ; IF 4 FP/63 FN/45 VP ; union 4 FP/4 FN/104 VP, 44 puis 64 alertes/semaine et avertissement de dépassement. Retour au prompt visible.

Ces sorties correspondent à l'essai graine7 de l'assistant, mais aucune égalité de fichiers entre environnements n'est démontrée. Les captures n'incluent pas deux relances à42 ni le contenu/empreinte du CSV VM. Le CSV final du dépôt reste celui de42 ; l'essai7 utilise un fichier distinct. Captures intégrées dans la fiche du script.

## Éléments restant à remettre ou confirmer

- Récupérer les deux notebooks complétés et enregistrés depuis la VM ; leurs originaux du dépôt ne sont pas automatiquement synchronisés.
- Relire et reformuler les commentaires pour pouvoir expliquer chaque bloc ; ne pas présenter l’assistance comme un travail rédigé seul.
- Exécution VM à graine7 attestée ; compléter les versions et, si la reproductibilité VM est revendiquée, conserver deux exécutions à42 et comparer leurs fichiers.
- La file union dépasse la capacité : arbitrage de Nadia et validation sur de nouvelles données avant exploitation ; aucun cron ni acceptation de risque réalisés.
