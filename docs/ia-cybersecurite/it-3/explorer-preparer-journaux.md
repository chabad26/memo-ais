# Explorer et préparer les journaux

**45 min — Présentiel**

## L'extraction de Sofia

> **Sofia [13:32]** Je vous ai déposé l'extraction : deux semaines de logs du bastion, du 14 au 27 septembre.  
> Une ligne = une IP pendant une heure, comme dans votre exercice du J1.  
> Hugo, l'analyste du SOC, a étiqueté chaque ligne normal ou attaque.  
> Il y a eu deux pannes de la sonde NetFlow, désolée pour les trous 🙈

Le modèle n'apprend que ce que les données représentent. Cette fiche répond aux questions **A1 à A4 et B1/B2** du notebook `01_detection_ssh.ipynb`. Les calculs du corrigé sont vérifiés sur le CSV fictif du kit, en lecture seule avec la bibliothèque standard Python ; **ils n'attestent pas l'exécution du notebook dans la VM**.

Le TP prépare des caractéristiques numériques sans valeurs manquantes. C'est le contrat retenu pour cette chaîne : l'affirmation générale « Scikit-learn n'accepte jamais de cases vides » serait trop large, certains estimateurs gérant les `NaN`. Il faut connaître les contraintes des estimateurs réellement utilisés. [Scikit-learn — valeurs manquantes](https://scikit-learn.org/stable/modules/impute.html).

## Mission 1 — Explorer : partie A

### Chargement et graphique à compléter

```python
df = pd.read_csv("hexalp_ssh_sept2026.csv")
print(df.shape)
df.head()
```

Pour le nuage de points du notebook, définir aussi `couleurs` dans le noyau avant de l’utiliser (sinon `NameError`) :

```python
couleurs = df["etiquette"].map({"normal": "tab:blue", "attaque": "tab:red"})
plt.figure(figsize=(8, 5))
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

!!! note "Mise à jour après la partie C"
    Les captures de cette page conservent l’état avant nettoyage. Les [captures du classifieur supervisé](le-classifieur-supervise.md) montrent ensuite la suppression appliquée et un partage de **1 129 + 485 = 1 614 lignes**. Le nettoyage n’est donc plus seulement prévu ; les remarques ci-dessous décrivent l’état des captures initiales.

## Captures des exercices — 21 octobre 2026

### Chargement du fichier brut

![Chargement du CSV avec 1704 lignes et 11 colonnes](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-35-30.png)

**10 h 35 min 30 s :** `pd.read_csv`, `df.shape` et l’aperçu montrent **1 704 lignes et 11 colonnes**. Le fichier brut est chargé ; cette étape ne démontre pas son nettoyage.

### Graphique exécuté après définition des couleurs

![Nuage de points des échecs et comptes distincts coloré par étiquette](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-35-37.png)

**10 h 35 min 37 s :** la définition de `couleurs` et le nuage de points sont visibles. Cela confirme la résolution de l’erreur `NameError` rencontrée précédemment. On voit le groupe dense près de l’origine, des points rouges proches de ce groupe et quelques points bleus dans la zone d’échecs élevés. Le graphique illustre les limites des deux caractéristiques ; il ne prouve pas l’entraînement d’un modèle.

### Pannes NetFlow et codage de l’origine

![Localisation des volumes manquants et origine codée en binaire](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-38-54.png)

**10 h 38 min 54 s :** les comptes par date/heure sont affichés pour les périodes du **19 septembre, 0–11 h**, et du **22 septembre, 10–15 h**. Leur somme vaut **90 observations**, cohérente avec le calcul sur le fichier. Le codage montre **interne → 0, externe → 1**.

**Point restant :** la cellule du choix de nettoyage contient encore `___` et aucune sortie « Cases vides restantes » n’est visible. La capture ne démontre donc aucune suppression ni imputation. L’affichage du code `df.isna().sum()` sans sa sortie ne suffit pas non plus à confirmer à lui seul le décompte de chaque colonne.

### Caractéristiques définies, mais jeu encore brut

![Sept caractéristiques et dimensions de X avant nettoyage](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-39-09.png)

**10 h 39 min 09 s :** les sept caractéristiques proposées sont bien renseignées ; la sortie est **`(1704, 7) 117 attaques`**. Elle est cohérente avec le jeu **avant suppression des volumes manquants**. Elle ne correspond pas encore à la préparation choisie dans ce corrigé.

Pour poursuivre avec cette stratégie, remplacer `___` dans la cellule B1 par :

```python
df = df.dropna(subset=["octets_sortants_mo"]).copy()
```

Puis exécuter cette cellule, vérifier le nombre de valeurs manquantes, et **réexécuter les cellules de codage et de création de `X`/`y`** : ces objets ne se mettent pas à jour automatiquement quand `df` change. Résultat attendu sur une reprise depuis le fichier fourni : **0 volume manquant**, **`(1614, 7) 108 attaques`**. Conserver les observations exclues séparément si ce suivi est retenu. Ne pas entraîner sur la seule foi de la présence des sept colonnes.

## Carnet et état du travail

A1–A4, B1/B2 et la liste des sept caractéristiques sont consignés dans **`livrables/ia-cybersecurite/it-3/ia01-j3/carnet_J3.md`**. Le CSV et le notebook source ne sont pas modifiés ; aucun modèle n'a été entraîné pour cette fiche. Quatre captures attestent le chargement, le graphique, la localisation des manques, le codage de l’origine et la définition des sept caractéristiques. Le nettoyage reste à appliquer et vérifier ; A1/A2, A4 et l’enregistrement complet du notebook ne sont pas tous montrés. Aucun entraînement n’est attesté.

**Preuves attendues :** répartition des classes, graphique avec deux zones commentées, lignes du scanner, décompte/localisation des manques, résultat du nettoyage, codage d'origine et dimensions de `X`/`y`. Si un résultat diffère, noter la version du fichier, les cellules exécutées et le traitement appliqué, sans forcer la sortie attendue.

Sources Scikit-learn consultées le **21 octobre 2026** ; valeurs chiffrées vérifiées sur le CSV fictif fourni. Les rôles de scanner et de sauvegarde restent des interprétations à confirmer par un contexte métier absent du CSV.

[Retour à l'itération 3](index.md)
