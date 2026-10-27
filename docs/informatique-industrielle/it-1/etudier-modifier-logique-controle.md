# 1.5 — Atelier 5 | Étudier et modifier la logique de contrôle

## Objectif et modalité

**Comprendre la logique de régulation d’un automate et observer les conséquences de la modification de ses paramètres.** TP en binôme, sur le modèle Python fourni, sans connaissance préalable en développement Python.

Le contrôleur reste un **programme Python simulé**, pas un automate matériel ou un runtime OpenPLC. Cette fiche comprend les réponses, une procédure sur copie de travail et une comparaison calculée localement. Sept captures utilisateur documentent désormais le code initial, la modification et des états du modèle modifié. Les durées de cycle mesurées, la restauration et la mise en commun restent à compléter.

## 1 — Comprendre la logique de régulation

```text
SI capteur défaillant :
    arrêter le compresseur
SINON SI température >= consigne + 0,5 :
    démarrer le compresseur
SINON SI température <= consigne - 0,5 :
    arrêter le compresseur
SINON :
    conserver l’état précédent
```

### Réponses aux quatre questions

1. **Pourquoi conserver l’état précédent ?** Entre les deux seuils, aucune nouvelle décision de marche ou d’arrêt n’est nécessaire. La mémoire de l’état crée l’hystérésis : à 4 °C, le compresseur peut être en marche pendant le refroidissement ou arrêté pendant le réchauffement.
2. **Avec une consigne unique ?** Une petite oscillation ou du bruit de mesure autour de ce seuil pourrait provoquer des commutations fréquentes. La fréquence réelle dépendrait de la mesure, de la dynamique et d’éventuelles temporisations de protection.
3. **Pourquoi une hystérésis ?** Pour éviter ces basculements autour d’un seuil unique, en acceptant une bande de variation de température. Elle ne remplace pas les protections mécaniques ou les temps minimaux de marche et d’arrêt, qui ne sont pas implémentés ici.
4. **Consigne ou logique ?** La consigne est une valeur utilisée par la règle : passer de 4 à 6 °C déplace les deux seuils. Modifier la logique change la façon de décider : élargir les écarts à ±1 °C change la bande de régulation à consigne constante. Dans ce laboratoire, ces écarts sont codés en dur : les modifier nécessite de changer le fichier et de relancer le serveur.

## 2 — Identifier la logique dans le programme

Dans `lab/model.py`, méthode `Plant.advance()` :

```python
if self.sensor_fault:
    self.compressor = False
elif self.automatic:
    if self.temp >= self.setpoint + 0.5:
        self.compressor = True
    elif self.temp <= self.setpoint - 0.5:
        self.compressor = False
```

| Élément à identifier | Code et rôle |
| --- | --- |
| Consigne | `self.setpoint`, initialement **4.0 °C**. |
| Température | `self.temp`, initialement **5.0 °C** dans le modèle. |
| Seuil haut | `self.setpoint + 0.5`, donc **4,5 °C** à consigne 4 °C. |
| Seuil bas | `self.setpoint - 0.5`, donc **3,5 °C** à consigne 4 °C. |
| État du compresseur | `self.compressor` : `True` en marche, `False` à l’arrêt. |
| Défaut capteur | `self.sensor_fault` : priorité à l’arrêt, règle propre au scénario. |
| Mode automatique | `self.automatic` : la régulation par seuils ne s’exécute que s’il est actif. |
| Conservation de l’état | Aucun `else` ne réaffecte le compresseur entre les seuils : sa valeur précédente reste en mémoire. |

Le pseudo-code suppose le mode automatique actif. Le programme réel comporte cette condition supplémentaire ; si `automatic=False` et sans défaut, les seuils ne modifient plus l’état du compresseur.

## 3 — Modifier l’hystérésis dans une copie

### Préparer et sauvegarder

Arrêter le serveur de l’atelier précédent par **Ctrl + C** dans son terminal avant de lancer une nouvelle instance sur le même port. La supervision peut rester ouverte ; elle sera temporairement sans contrôleur pendant la transition.

Depuis la racine du mémo, créer une copie dans un répertoire temporaire distinct :

```bash
atelier5Dir=$(mktemp -d /tmp/ot-atelier5.XXXXXX)
cp -a livrables/informatique-industrielle/it-1/ot-refrigeration-poc/. "$atelier5Dir/"
cd "$atelier5Dir"
cp -p lab/model.py lab/model.py.initial
```

Noter le chemin affiché par `pwd` et ouvrir les terminaux de cet essai dans ce même dossier. Le laboratoire de référence reste intact.

Ouvrir le fichier avec l’éditeur disponible, par exemple :

```bash
nano lab/model.py
```

Changer **uniquement les deux écarts** :

```python
if self.sensor_fault:
    self.compressor = False
elif self.automatic:
    if self.temp >= self.setpoint + 1.0:
        self.compressor = True
    elif self.temp <= self.setpoint - 1.0:
        self.compressor = False
```

Ne pas modifier la consigne, les coefficients thermiques, le calcul d’alarme ni la branche de défaut.

### Vérifier, relancer et observer

```bash
diff -u lab/model.py.initial lab/model.py
python3 -m py_compile lab/model.py
python3 -m lab.server
```

La sortie de `diff` doit montrer les deux remplacements de `0.5` par `1.0`. Son code de retour 1 signifie ici qu’une différence a été trouvée. `py_compile` vérifie la syntaxe, pas la validité de la régulation.

Dans un autre terminal placé dans la copie, vérifier :

```bash
python3 -m lab.client status
```

Au redémarrage, une nouvelle instance repart des **valeurs initiales du code**, sans conserver automatiquement les derniers paramètres : température 5 °C, consigne 4 °C, porte fermée, défaut inactif, automatique actif. La température initiale correspond exactement au nouveau seuil haut ; le compresseur démarre au premier pas.

Ouvrir ou conserver la supervision sur `http://127.0.0.1:18080`. Si elle n’est plus lancée, exécuter `python3 -m lab.dashboard` dans un troisième terminal. Comparer plusieurs cycles avec le fonctionnement initial, en gardant la porte fermée et sans défaut.

| Paramètre | Initial | Modifié |
| --- | --- | --- |
| Consigne | 4 °C | 4 °C |
| Écart de chaque côté | ±0,5 °C | ±1 °C |
| Seuil de démarrage | 4,5 °C | 5 °C |
| Seuil d’arrêt | 3,5 °C | 3 °C |
| Largeur totale de la bande | 1 °C | 2 °C |

Relever les instants des démarrages et arrêts, les températures extrêmes, les états de porte et de défaut. Comparer des cycles après le transitoire de démarrage ; les arrondis d’affichage et le rafraîchissement peuvent masquer l’instant exact d’une bascule.

### Restaurer le modèle initial

Arrêter le serveur modifié avec **Ctrl + C**, puis dans la copie :

```bash
cp -p lab/model.py.initial lab/model.py
cmp lab/model.py.initial lab/model.py
python3 -m lab.server
```

`cmp` ne doit rien afficher et doit réussir : le fichier est restauré à l’identique. Vérifier ensuite `status` et le retour aux seuils initiaux. Arrêter le serveur de test puis la supervision à la fin de la session. Le retour au code initial implique ici un nouveau démarrage de simulation, pas une continuité de l’état thermique.

## 4 — Analyser les conséquences

1. **Différence entre les cycles :** dans le modèle et à conditions identiques, l’hystérésis plus large laisse davantage de temps au réchauffement et au refroidissement avant chaque bascule. Les cycles sont plus longs, les commutations moins fréquentes, et la température parcourt une bande plus large.
2. **Une meilleure régulation ?** Pas nécessairement. Une fréquence de commutation réduite peut être recherchée, mais l’écart à la consigne augmente. Une bande de 3 à 5 °C peut être incompatible avec des besoins plus stricts. La qualité se juge selon les exigences du procédé, pas seulement le nombre de démarrages.
3. **Effets possibles sur l’équipement :** changement du nombre de démarrages, des durées de marche/arrêt, de la sollicitation mécanique et électrique et des variations thermiques. L’effet sur la consommation et la durée de vie doit être mesuré sur l’équipement ; ce modèle ne permet pas de le conclure. Une modification erronée des comparaisons ou des priorités pourrait empêcher le refroidissement ou dégrader la réaction aux défauts.
4. **Pourquoi tester avant déploiement réel ?** Pour vérifier les températures admissibles, les transitions, les modes de fonctionnement, les alarmes et défauts, les contraintes du compresseur et le retour arrière. Faire valider le changement par l’exploitation et les personnes compétentes avant une fenêtre autorisée. Une copie syntaxiquement valide et quelques cycles normaux ne couvrent pas toutes ces conditions.

## 📦 Livrable — Comparaison renseignée et limites

### Calcul comparatif local du 26 octobre 2026

Les deux versions ont été exécutées **en mémoire**, à partir du même fichier source ; seuls les deux écarts ont été remplacés pour la variante. Aucun fichier du laboratoire fourni n’a été modifié. Chaque version utilise une nouvelle instance `Plant()` et **6 000 pas de 0,1 s**, soit **600 secondes simulées**, sans attente réelle ni serveur réseau.

Conditions communes : température initiale **5 °C**, ambiance **22 °C**, consigne **4 °C**, porte fermée, défaut inactif, automatique actif. Un cycle complet est mesuré entre deux démarrages successifs après le premier arrêt.

| Résultat calculé | Initial ±0,5 °C | Modifié ±1 °C |
| --- | --- | --- |
| Premier démarrage | 0,1 s | 0,1 s |
| Premier arrêt | 54,6 s | 73,2 s |
| Démarrage suivant | 134,2 s | 232,3 s |
| Arrêt suivant | 170,8 s | 305,4 s |
| Démarrage suivant | 250,4 s | 464,5 s |
| Durée d’un cycle après le transitoire | **116,2 s** : 134,2 → 250,4 | **232,2 s** : 232,3 → 464,5 |
| Temps de marche sur ce cycle | 36,6 s | 73,1 s |
| Temps d’arrêt sur ce cycle | 79,6 s | 159,1 s |
| Bande attendue après le transitoire | Environ 3,5–4,5 °C | Environ 3–5 °C |

De très faibles dépassements des seuils sont possibles avec le pas discret : la décision précède l’évolution thermique de chaque pas. La valeur initiale de 5 °C dépasse aussi la bande du modèle initial : elle ne doit pas être incluse comme un maximum représentatif du cycle stabilisé.

> À consigne constante de 4 °C, le passage de ±0,5 à ±1 °C double la largeur de la bande d’hystérésis. Le calcul sur le modèle fourni montre un cycle d’environ 232 s contre 116 s après le transitoire : le compresseur commute moins souvent, mais la température varie davantage. Ce résultat ne suffit pas à affirmer une amélioration de la conservation des produits, de la consommation ou de la durée de vie de l’équipement. Le choix doit être validé selon les contraintes du procédé et les prescriptions de l’équipement.

### Captures utilisateur — modification et fonctionnement observé

Les heures proviennent des noms des fichiers, sans constituer un horodatage interne des mesures. Les captures du code et du terminal documentent la modification ; les états affichés ci-dessous lui sont associés dans la séquence fournie, sans afficher eux-mêmes la version chargée.

#### 11:31:11 — Repérage du contrôle initial

![Repérage du contrôle initial](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2011-31-11.png)

La méthode `advance()` montre les seuils **`self.setpoint + 0.5`** et **`self.setpoint - 0.5`**, la priorité du défaut capteur et le contrôle conditionné au mode automatique. Elle correspond à la logique initiale décrite dans la fiche.

#### 11:38:43 — Hystérésis modifiée à ±1 °C

![Hystérésis modifiée à ±1 °C](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2011-38-43.png)

Le code affiché utilise **`self.setpoint + 1`** et **`self.setpoint - 1`**. La priorité du défaut et le mode automatique sont conservés dans l’extrait. La capture établit la modification affichée ; le diff suivant précise son étendue.

#### 11:38:53 — Diff, vérification de syntaxe et serveur relancé

![Diff, vérification de syntaxe et serveur relancé](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2011-38-53.png)

Le terminal est dans un dossier temporaire de travail `/tmp/ot-atelier5.…`. Le diff entre `lab/model.py.initial` et `lab/model.py` montre uniquement les deux changements de seuil **0.5 → 1**. La séquence affiche `python3 -m py_compile lab/model.py`, sans erreur visible, puis `python3 -m lab.server` et **`Listening on 127.0.0.1:15020 (Modbus TCP)`**. Elle atteste la copie initiale disponible, la différence ciblée et le lancement du serveur modifié ; la vérification syntaxique ne valide pas à elle seule tous ses comportements.

#### 11:39:13 — Température de 3 °C, compresseur arrêté

![Température de 3 °C, compresseur arrêté](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2011-39-13.png)

La supervision affiche **3 °C**, consigne **4 °C**, compresseur **OFF**, porte fermée et aucune alarme. Cet état est cohérent avec le nouveau seuil bas de **3 °C**, sans montrer l’instant précis du passage à l’arrêt.

#### 11:40:21 — Remontée à 3,9 °C, compresseur arrêté

![Remontée à 3,9 °C, compresseur arrêté](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2011-40-21.png)

La supervision affiche **3,9 °C**, consigne **4 °C**, compresseur **OFF**, porte fermée et aucune alarme. L’état est compatible avec une phase de réchauffement conservant l’arrêt dans la nouvelle bande.

#### 11:42:37 — À 4,7 °C, le compresseur reste arrêté

![À 4,7 °C, le compresseur reste arrêté](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2011-42-37.png)

La supervision affiche **4,7 °C**, consigne **4 °C**, compresseur **OFF**, porte fermée et aucune alarme. C’est le point de comparaison le plus parlant : **4,7 °C dépasse l’ancien seuil de 4,5 °C, mais reste sous le nouveau seuil de 5 °C**. Dans la séquence après élargissement de l’hystérésis, cet arrêt est cohérent avec la nouvelle logique et ne suffit pas à diagnostiquer un défaut capteur. Le tableau de bord seul ne montre toutefois ni le défaut ni le mode automatique.

#### 11:43:02 — Compresseur en marche à 4,9 °C

![Compresseur en marche à 4,9 °C](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2011-43-02.png)

La supervision affiche **4,9 °C**, consigne **4 °C**, compresseur **ON**, porte fermée et aucune alarme. Cet état est compatible avec un démarrage après atteinte de 5 °C, suivi d’un refroidissement. Le franchissement de 5 °C et l’instant de démarrage ne sont pas capturés : la valeur 4,9 °C ne doit pas être présentée comme le seuil de démarrage.

**Comparaison attestée :** les observations du modèle modifié sont compatibles avec une plage plus large, dont un état à 3 °C à l’arrêt et un maintien de l’arrêt à 4,7 °C. Les captures de l’[atelier 1.3](prendre-en-main-modele-frigorifique.md) documentaient les états du modèle initial ; les conditions ne constituent pas un enregistrement comparatif continu. Les durées de 116,2 et 232,2 s ci-dessus restent des résultats du calcul local, pas des mesures déduites de ces captures.

### État des preuves utilisateur

| Trace attendue | État |
| --- | --- |
| Copie initiale et différence limitée aux deux seuils | Attestées par le diff du 11:38:53. |
| États du modèle modifié dans le navigateur | Quatre captures intégrées : 3 °C OFF, 3,9 °C OFF, 4,7 °C OFF, 4,9 °C ON. Cycles complets et mesures CLI avant/après à compléter. |
| Restauration du fichier initial et vérification du fonctionnement | À documenter. |
| Comparaison et corrections en binôme | À compléter. |

**Convention de nommage :** `[Nom]-[Prénom]-[Site]-Iteration1-Atelier5`. Site et format de remise à confirmer ; cette fiche conserve le nom thématique du mémo.

[Retour à l’itération](index.md) · [Atelier précédent — Dysfonctionnements](observer-dysfonctionnements-consequences.md)
