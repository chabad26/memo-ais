# Le classifieur supervisé

**1 h — Présentiel**

## Le concept et les effectifs réellement observés

Un arbre de décision apprend des questions successives sur les caractéristiques ; à chaque nœud, il cherche une séparation locale des classes, puis poursuit dans les branches. Cette recherche n'est pas une garantie de trouver le meilleur arbre global. `max_depth` limite la profondeur. Le test est tenu à l'écart de l'entraînement pour examiner la généralisation. [Scikit-learn — arbres de décision](https://scikit-learn.org/stable/modules/tree.html).

Les captures de l'apprenant montrent le **nettoyage appliqué**, la séparation, l'entraînement et l'évaluation de la partie C. Elles remplacent les valeurs génériques de la consigne : **1 129 observations d'entraînement**, et non 1 192 ; **32 attaques dans le test**, et non 35.

| Ensemble | Normal | Attaque | Total |
| --- | --- | --- | --- |
| CSV brut, avant nettoyage | 1 587 | 117 | 1 704 |
| Après suppression des volumes manquants | 1 506 | 108 | 1 614 |
| Entraînement | 1 053 | 76 | **1 129** |
| Test | 453 | 32 | **485** |

Le partage utilise `test_size=0.3`, `stratify=y` et `random_state=GRAINE` (42 dans le kit). La stratification préserve approximativement les proportions : avec des effectifs entiers, elles ne peuvent pas toujours être exactement identiques. Les 90 observations supprimées ne participent pas à ces scores ; elles ne deviennent pas normales pour autant.

## Code des cellules à compléter

Le nettoyage est effectué **avant de recréer X/y**, puis de séparer les données :

```python
df = df.dropna(subset=["octets_sortants_mo"]).copy()
X = df[CARACTERISTIQUES]
y = (df["etiquette"] == "attaque").astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=GRAINE
)

arbre = DecisionTreeClassifier(max_depth=3, random_state=GRAINE)
arbre.fit(X_train, y_train)
predictions = arbre.predict(X_test)

print("Accuracy :", round(accuracy_score(y_test, predictions), 3))
```

`fit` est la méthode d'entraînement, pas `___`. `test_size` attend ici une proportion, pas une instruction de nettoyage. Pour la comparaison indépendante :

```python
decision_f2b = df.loc[X_test.index, "fail2ban_ban"]
print(classification_report(
    y_test, decision_f2b,
    target_names=["normal", "attaque"],
    zero_division=0,
))
```

`df.loc` utilise **les mêmes index de test** et la colonne de décision historique ; `X.train` n'est pas une sélection valable de cette colonne.

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

## Captures et preuve de travail

### Nettoyage, séparation et entraînement

![Nettoyage puis séparation 1129 et 485 lignes, arbre profondeur 3 accuracy 0.992](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-48-58.png)

**10:48:58 :** suppression des volumes manquants, reconstruction de X/y, séparation et appel `fit` visibles. L'accuracy affichée est **0,992** ; les deux tailles totalisent 1 614 lignes.

### Arbre appris

![Arbre de décision de profondeur 3 à six feuilles](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-49-10.png)

**10:49:10 :** six feuilles et règles retranscrites en C1. Le nœud racine affiche 1 129 exemples, dont 76 attaques ; la sortie texte des règles n'est pas montrée.

### Matrice et rapport

![Matrice de confusion 453 VN 0 FP 4 FN 28 VP](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-49-21.png)

**10:49:21 :** supports et erreurs confirment 32 attaques test et le rappel de 87,5 %. Le rapport arrondit à 0,88.

### Les quatre attaques manquées

![Tableau des quatre faux négatifs et aucun faux positif](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-49-42.png)

**10:49:42 :** les quatre index de C3 sont visibles ; le tableau des faux positifs n'a pas de ligne.

### Profondeurs comparées

![Résultats des profondeurs 1 3 10 et None](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-49-52.png)

**10:49:52 :** scores, FP/FN et feuilles de C4. Pas de nouveau test indépendant ni d'adoption du modèle profond démontrés.

### fail2ban sur le même test

![Rapport fail2ban avec rappel attaque 0.53 et support 32](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-52-14.png)

**10:52:14 :** sélection corrigée `df.loc[X_test.index, "fail2ban_ban"]` et rapport des décisions historiques.

### Détections complémentaires

![Onze observations attaque signalées par arbre sans bannissement historique](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2010-52-26.png)

**10:52:26 :** onze lignes satisfont le filtre attaque réelle, prédiction attaque et absence de bannissement historique. La colonne de prédiction est coupée à droite mais la condition du filtre est visible. Aucun blocage du SI n'a été effectué.

## État du livrable et limites

Les réponses C1–C6, l'explication à Nadia et la comparaison des scénarios sont consignées dans **`livrables/ia-cybersecurite/it-3/ia01-j3/carnet_J3.md`**. Les captures attestent le travail exécuté dans Jupyter ; **le notebook du dépôt n'est pas automatiquement synchronisé avec celui de la VM** et n'a pas été modifié pour créer cette fiche. Sa version complétée et enregistrée reste à récupérer pour le livrable final.

Les chiffres sont ceux du test aléatoire du kit, déjà consulté pour comparer des réglages. Ils ne démontrent ni une performance indépendante après sélection, ni une détection en production, ni l'absence de dérive. Des lignes proches d'une même IP peuvent figurer de part et d'autre du partage aléatoire ; une évaluation temporelle et des scénarios nouveaux renforceraient l'analyse. Les observations exclues faute de volume restent hors couverture de ces résultats.

## Ressources

- [Scikit-learn — Decision Trees](https://scikit-learn.org/stable/modules/tree.html)
- [Inria — Cours Scikit-learn, Decision tree models](https://inria.github.io/scikit-learn-mooc/)

Sources consultées le **21 octobre 2026**. Résultats issus des sept captures de l'apprenant ; interprétations séparées des faits. Aucun entraînement supplémentaire effectué par l'assistant pour rédiger cette fiche.

[Retour à l'itération 3](index.md)
