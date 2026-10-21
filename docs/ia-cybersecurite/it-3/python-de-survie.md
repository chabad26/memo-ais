# Python de survie

**1 h — Présentiel**

## Le problème à résoudre

Il ne s'agit pas de devenir développeur : il faut savoir **lire un notebook, exécuter ses cellules, modifier un réglage et comprendre une erreur**. pandas propose des opérations familières à qui utilise `head`, `cut`, `awk` ou `sort`, mais sur des tableaux structurés.

**Support :** `livrables/ia-cybersecurite/it-3/ia01-j3/00_python_survie.ipynb`, avec le CSV du même dossier. Les réponses ci-dessous correspondent aux cellules du fichier reçu. Le notebook source reste intact : le corrigé et le carnet ne sont pas une preuve qu'il a été complété et exécuté dans la VM.

## Vocabulaire clé

| Terme | Ce que c'est concrètement |
| --- | --- |
| **Cellule** | Bloc de code ou de texte ; `Maj + Entrée` exécute le code ou affiche le texte mis en forme et passe à la suite |
| **Noyau — kernel** | Processus qui exécute le code et conserve les variables ; son état suit l'ordre réel d'exécution, pas seulement l'ordre visuel des cellules |
| **Variable** | Nom associé à une valeur : `echecs = 87` |
| **Liste** | Collection ordonnée : `[22, 80, 443]` ; premier index : `0` |
| **Dictionnaire** | Association de clés à des valeurs : `{"ip": "10.20.1.5"}` |
| **Fonction / méthode** | Appel avec parenthèses : `len(ports)` ; méthode appelée sur un objet : `ip.startswith("10.")` |
| **Import** | Chargement d'un module et association à un nom, par exemple `import pandas as pd` |
| **DataFrame** | Tableau pandas, souvent nommé `df` ; ici les lignes sont des observations et les colonnes incluent caractéristiques, identifiants et étiquette |

**Attention à l'état du noyau :** une cellule exécutée avant celle qui définit ses variables peut échouer. Un redémarrage efface cet état. Une fois les exercices corrigés, relancer dans l'ordre permet de vérifier que les résultats ne dépendent pas de variables oubliées en mémoire. Les trois cellules d'erreurs doivent d'abord être observées individuellement : une exécution globale s'arrêtera normalement à la première erreur non corrigée.

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

## Captures des exercices — 21 octobre 2026

Les six captures suivantes proviennent du travail de l’apprenant dans Jupyter. Aucun jeton n’y est visible. Elles montrent les opérations pandas présentées, sans démontrer à elles seules l’exécution complète ou la sauvegarde de tout le notebook.

### Chargement du CSV et structure du tableau

![Chargement du CSV et structure du tableau](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-19-32.png)

**Capture 10:19:32 :** `pd.read_csv`, `df.head()`, `df.shape` et `df.columns` ont une sortie visible : **1 704 lignes et 11 colonnes**. La colonne `echecs_auth` est affichée avec le type `int64`. Cela atteste ces opérations, pas l’absence de doublons ou de valeurs manquantes.

### Maximum, origines et filtre sur les échecs

![Maximum, origines et filtre sur les échecs](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-20-00.png)

**Capture 10:20:00 :** Maximum d’échecs : **298** ; origines : **1 566 internes et 138 externes**, soit 1 704 observations. Ce sont des effectifs de lignes, pas des nombres d’IP. Le filtre `echecs_auth > 50` contient aussi des lignes étiquetées normal pour `10.20.1.250` : un gros nombre d’échecs ne prouve pas une attaque. Des volumes `NaN` sont visibles, à traiter lors de la préparation.

### Tri décroissant des échecs SSH

![Tri décroissant des échecs SSH](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-20-18.png)

**Capture 10:20:18 :** Le tri sur `echecs_auth` et `head(10)` est exécuté ; la première ligne affiche **298 échecs**. Ce résultat porte sur les échecs, à distinguer du tri des volumes sortants de la dernière capture.

### Exercices a à d : effectifs et filtre nocturne

![Exercices a à d : effectifs et filtre nocturne](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-23-43.png)

**Capture 10:23:43 :** Les sorties montrent **1 704 observations**, **1 587 normal / 117 attaque**, et **127 lignes** satisfaisant heure ≤ 5 et succès > 0. Pour b), `unique()` affiche les valeurs distinctes et indique `Length: 138` ; c’est cohérent avec 138 IP, mais `nunique()` répond directement par un nombre. Une ligne étiquetée attaque est visible parmi les connexions nocturnes réussies : succès ne veut pas dire légitime.

### Exercice e : les cinq plus gros volumes sortants

![Exercice e : les cinq plus gros volumes sortants](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-23-52.png)

**Capture 10:23:52 :** Le tri sur `octets_sortants_mo` donne les cinq lignes du tableau de référence : toutes concernent **10.20.8.30** et portent l’étiquette **normal**. Le maximum est **2 548,99 Mo** le 22 septembre à 1 h ; une ligne du classement est à 2 h. La capture confirme les données, pas l’hypothèse métier de sauvegarde.

### Exercice b complété — Compter directement les IP distinctes

![Cellule nunique affichant 138 IP distinctes](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-25-37.png)

**Capture de 10 h 25 min 37 s :** `print(df["ip_source"].nunique())` retourne **138**. L'exercice b est désormais illustré avec le comptage direct demandé, en complément de la capture précédente qui affichait la liste avec `unique()`. Ce nombre porte sur les IP distinctes du DataFrame chargé, pas sur des utilisateurs ou des machines physiques identifiés.

## Carnet et preuves à conserver

Les deux tableaux, les corrections a–e et l'analyse de la machine sont reportés dans **`livrables/ia-cybersecurite/it-3/ia01-j3/carnet_J3.md`**. Dans la VM, exécuter les cellules, observer les erreurs avant de les corriger, enregistrer le notebook et consigner les résultats réels. Une capture doit montrer la cellule et sa sortie, sans jeton Jupyter.

**État : corrigé préparé ; six captures attestent le chargement et les exercices pandas visibles. Les trois erreurs des bases ne sont pas montrées par ces captures, et l’exécution complète ainsi que la sauvegarde du notebook dans la VM restent à documenter. Le notebook source du dépôt reste non modifié ; aucun modèle entraîné.** Les journaux de ce kit sont fictifs ; des données équivalentes d'entreprise seraient à traiter comme C2 selon la PSSI Hexalp. Ne transmettre que du contenu autorisé et minimisé, et pouvoir expliquer chaque ligne rendue.

## Ressources

- [Python — Tutoriel officiel](https://docs.python.org/fr/3/tutorial/index.html)
- [pandas — 10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)

Sources consultées le **21 octobre 2026**.

[Retour à l'itération 3](index.md)
