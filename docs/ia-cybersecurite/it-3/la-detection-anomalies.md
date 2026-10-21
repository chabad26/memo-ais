# La détection d'anomalies

**1 h — Présentiel**

## Le concept

L'arbre a appris à partir des étiquettes de Hugo. Il peut parfois signaler une attaque nouvelle si elle ressemble aux exemples connus, mais ne garantit pas la reconnaissance d'un comportement inédit.

**Isolation Forest apprend ici sans étiquette** : des séparations aléatoires isolent les observations, et les chemins d'isolation courts indiquent des profils atypiques. Dans Scikit-learn, **`decision_function` faible signifie plus atypique**, et `predict` renvoie **−1 pour une anomalie, +1 pour une observation non signalée**. Ce n'est pas une probabilité d'attaque. [Scikit-learn — Isolation Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html).

`contamination` règle le seuil en fonction d'une proportion attendue d'observations atypiques dans les données d'ajustement. Ce n'est ni un taux d'attaque mesuré ni une garantie de quota futur. Le modèle peut être construit avec un nombre d'arbres configurable : il ne faut pas supposer un nombre exact sans relever ses paramètres.

**Ordre retenu :** préparer les données, entraîner sans `y`, qualifier les quinze premières lignes sans étiquette, puis seulement comparer aux références de Hugo. Cette fiche fournit le code et les réponses conceptuelles ; **quatre captures attestent désormais l’exécution décrite ci-dessous**.

## Avant de commencer la partie D

Conserver l'état nettoyé et les sept caractéristiques de la partie C : **1 614 observations, 108 étiquettes attaque**, sans volume manquant. `X` doit correspondre aux mêmes lignes et index que `df` ; `y` reste réservé à l'évaluation. Si le noyau a redémarré, refaire les étapes précédentes dans l'ordre.

```python
assert len(df) == len(X) == len(y)
assert X.index.equals(df.index)
assert y.index.equals(df.index)
assert not X.isna().any().any()
```

Dans le notebook fourni, Isolation Forest est ajusté **et examiné sur tout `X`**. Il s'agit d'une exploration d'anomalies dans le jeu courant, **pas d'un test indépendant sur de nouvelles données**. Ses futurs chiffres ne seront donc pas directement comparables au rappel de l'arbre mesuré sur 485 lignes tenues à l'écart de son entraînement.

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

## Captures de la partie D — 21 octobre 2026

### Ajustement et top 15 sans étiquette

![Isolation Forest contamination 0.03 et top15 sans étiquette](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2011-03-41.png)

**11:03:41 :** `fit(X)` sans étiquette et **49 signalées sur 1 614**. Le top 15 est présenté sans étiquette ; aucune qualification écrite avant révélation n'est visible.

### Évaluation, faux positifs et contaminations

![Table croisée faux positifs et trois contaminations comparées](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2011-04-12.png)

**11:04:12 :** matrice initiale, cinq FP répartis entre scanner et sauvegarde, et résultats 0,03/0,05/0,10. La boucle utilise `m` : elle ne remplace pas le `iforest` initial ni ses colonnes dans `df`.

### Révélation des étiquettes du top 15

![Les quinze étiquettes du classement sont attaque](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2011-05-12.png)

**11:05:12 :** les quinze index du classement portent tous l'étiquette attaque. Le tri efficace en tête de file ne signifie pas que toutes les attaques sont trouvées.

### Les trois observations de Julien

![Trois lignes de Julien avec scores positifs et anomalie False](../../assets/img/ia-cybersecurite/it-3/Capture%20d’écran%20du%202026-10-21%2011-06-22.png)

**11:06:22 :** drapeaux **False** pour 2, 3 et 4 h le 24 septembre, scores positifs affichés. Cette absence d'alerte sur les agrégats SSH ne couvre pas l'envoi de données au chatbot.

## État du carnet et limites de preuve

Les résultats ci-dessus et le tableau comparatif sont consignés dans **`livrables/ia-cybersecurite/it-3/ia01-j3/carnet_J3.md`**. Quatre captures attestent désormais la partie D ; aucune exécution supplémentaire n'a été réalisée par l'assistant. Restent à conserver les qualifications individuelles réellement faites avant révélation si elles existent, à examiner le détail des 64 FN et à rapatrier le notebook complété/enregistré depuis la VM.

L'arbre a été testé sur 485 observations tenues à l'écart de son ajustement ; Isolation Forest est ici évalué sur les **1 614 utilisées pour l'ajustement**. Ne pas comparer directement leurs rappels comme un concours à périmètre identique. La file combinée, son efficacité et sa charge ne sont pas mesurées. Les 90 observations sans volume restent exclues des métriques.

## Ressources

- [Scikit-learn — Détection d'anomalies, Isolation Forest](https://scikit-learn.org/stable/modules/outlier_detection.html)
- [Scikit-learn — Référence IsolationForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)
- [Résultats du classifieur supervisé](le-classifieur-supervise.md)

Sources consultées le **21 octobre 2026**. Les trois lignes de Julien sont vérifiées en lecture seule sur le CSV fictif ; les résultats Isolation Forest proviennent des captures de l’apprenant, sans nouvelle exécution par l’assistant.

[Retour à l'itération 3](index.md)
