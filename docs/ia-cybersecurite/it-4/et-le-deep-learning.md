# Et le Deep Learning ?

**Séquence 4.7 — 45 min — Présentiel**

## Le concept

Hugo fournit un autoencodeur pré-entraîné qui tente de recopier une connexion en passant par un goulot de trois neurones. Une reconstruction inhabituelle produit une erreur élevée : elle devient un signal à examiner, pas une preuve d’attaque.

```text
7 caractéristiques → 8 neurones → 3 neurones → 8 neurones → 7 valeurs reconstruites
```

L’objectif est de vérifier le fichier, utiliser le réseau **en inférence seule**, expliquer un score et comparer les détecteurs. Le notebook 04 a été complété et exécuté avec assistance **localement, hors VM**, sur les données fictives. L’autoencodeur et son normaliseur n’ont pas été réentraînés ; l’Isolation Forest de comparaison est ajustée sur septembre comme demandé par le kit.

## Mission 1 — Vérifier avant de charger

### Résultat du contrôle

La référence est désormais fournie par le **PDF du cours, section 4.7**, et non seulement calculée à partir du fichier :

```text
01464c560c949742a4b832c1b615194971ce56e29c93f39fd98bda3169e38b00
```

Commande à reproduire dans le dossier de travail :

```bash
sha256sum autoencodeur_hexalp.joblib
```

**Concordance vérifiée avant chargement et après inférence.** Le modèle du kit n’a pas été modifié. En cas de différence, arrêter sans charger et prévenir le responsable du modèle. Le notebook contrôle l’empreinte avant `joblib.load` ; ne pas exécuter la cellule de chargement isolément en contournant ce contrôle.

![Contrôle SHA-256 du modèle dans la VM Debian](../../assets/img/ia-cybersecurite/it-4/Capture%20d’écran%20du%202026-10-22%2010-14-57.png)

*Capture de l’apprenant du 22/10 à 10:14:57 : depuis `(.venv) oliv@debian:~/ia01-j4`, la commande `sha256sum autoencodeur_hexalp.joblib` retourne exactement l’empreinte de la section 4.7 du PDF. Le contrôle du fichier dans la VM est donc documenté ; cette capture ne montre pas son chargement ni l’inférence du notebook.*


![Vérification de l’empreinte dans le notebook](../../assets/img/ia-cybersecurite/it-4/Capture%20d’écran%20du%202026-10-22%2010-17-41.png)

*Capture de l’apprenant, 10:17:41 : la valeur calculée correspond à la référence attendue et le contrôle affiche « Empreinte conforme ». Cette vue complète la commande dans le terminal ; elle ne certifie pas l’innocuité du modèle.*

### 1. Pourquoi un autre canal ?

Si l’adversaire peut remplacer le fichier et l’empreinte publiée à côté, il peut les rendre cohérents. La référence doit venir d’un canal dont l’origine est vérifiée, par exemple un message authentifié du producteur ou un manifeste signé. Ici le PDF joue le rôle de référence du TP ; nous n’avons pas reçu un vrai message authentifié de Hugo. La concordance ne certifie donc pas toute la chaîne de provenance.

### 2. Risque de `joblib` et alternative

Un fichier `joblib`/`pickle` peut exécuter du code arbitraire lors du chargement : ce n’est pas un simple tableau de nombres. La documentation propose **`skops.io`**, avec inspection des types avant autorisation, ou **ONNX** pour une inférence compatible sans reconstruire l’objet Python. Ne pas considérer une conversion comme une protection rétroactive si elle exige de charger d’abord un fichier douteux. [Documentation officielle Scikit-learn, consultée le 22/10/2026](https://scikit-learn.org/stable/model_persistence.html).

### 3. Lien avec slopsquatting et `sklearn`

Un paquet et un modèle téléchargés sont des composants de la chaîne logicielle : leur nom ou extension ne garantit ni le producteur ni l’innocuité. Un paquet suggéré mais inexistant peut conduire vers un nom malveillant ; un modèle inconnu peut cacher un chargement dangereux. Vérifier source, provenance, intégrité et environnement avant usage. Pour la bibliothèque, le paquet attendu reste `scikit-learn`, même si l’import s’appelle `sklearn`.

## Mission 2 — Utiliser le réseau

### Les compléments du notebook

| Emplacement | Valeur renseignée | Sens |
| --- | --- | --- |
| Empreinte attendue | SHA-256 de la section 4.7 du PDF | Comparer à une référence avant chargement |
| Nombre de paramètres | `nb_parametres` | Additionner les tailles des poids et biais |
| Seuil d’anomalie | `SEUIL` | Utiliser le seuil livré, sans le choisir sur octobre |
| Première sauvegarde | `index[0]` | Examiner la première observation de cette IP |

Le modèle contient un seuil de **2,7615**. Sa description annonce un entraînement le 30/09/2026 par Hugo sur **1 587 connexions normales** de septembre, et un seuil au 95e centile des erreurs de septembre. Cette description embarquée est une **déclaration du producteur dans le scénario**, pas un audit de son entraînement.

### R1 — Paramètres et explicabilité

Le réseau compte **186 paramètres** :

| Liaison | Poids | Biais | Total |
| --- | ---: | ---: | ---: |
| 7 → 8 | 56 | 8 | 64 |
| 8 → 3 | 24 | 3 | 27 |
| 3 → 8 | 24 | 8 | 32 |
| 8 → 7 | 56 | 7 | 63 |
| **Total** | **160** | **26** | **186** |

Le commentaire source « 24 poids entre l’entrée et la première couche » a été corrigé : il y en a **56**. Notre arbre V2 comporte **cinq nœuds de séparation et six feuilles** ; un chemin suit au plus trois questions. Le réseau utilise de nombreux calculs combinés et des activations : regarder un poids isolé ne donne pas une règle du type « volume supérieur à… donc attaque ». Ses 186 paramètres n’incluent pas les statistiques du normaliseur ni le seuil d’alerte externe au réseau.


![Architecture, 186 paramètres et première matrice de poids](../../assets/img/ia-cybersecurite/it-4/Capture%20d’écran%20du%202026-10-22%2010-17-53.png)

*Capture de l’apprenant, 10:17:53 : les couches [7, 8, 3, 8, 7] et les 186 paramètres sont affichés. La matrice d’entrée a sept lignes et huit colonnes, soit **56 poids** : le commentaire « 24 poids » visible dans cette version du notebook est une coquille du kit, sans effet sur le calcul.*

### R2 — Où fait-il mieux ou moins bien ?

**Périmètre du notebook : 2 119 lignes, 215 attaques**, conversion Ko/Mo puis imputation des quatorze vrais manques par la médiane d’octobre. L’Isolation Forest de comparaison utilise la médiane de septembre et une contamination de **0,05** ; ce n’est pas notre V2 à 0,03. Les groupes ci-dessous peuvent se chevaucher : ne pas les additionner.

| Groupe | Observations | Signalées par IF 0,05 | Signalées par autoencodeur |
| --- | ---: | ---: | ---: |
| Sauvegarde nocturne, normale | 28 | 19 | **4** |
| Proxy Zabbix, normal | 278 | 0 | 0 |
| Exfiltrations VPN, attaques | 9 | 9 | **9** |
| Brute force selon le filtre du notebook, attaques | 50 | 40 | **50** |
| Toutes les attaques | 215 | 61 | **70** |
| Toutes les normales | 1 904 | 22 | **6** |

| Détecteur sur les 2 119 lignes | VN | FP | FN | VP | Précision | Rappel | Alertes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| IF pédagogique 0,05 | 1 882 | 22 | 154 | 61 | 73,49 % | 28,37 % | 83 |
| Autoencodeur | 1 898 | 6 | **145** | 70 | **92,11 %** | **32,56 %** | 76 |

Le réseau fait mieux sur les totaux et groupes présentés : neuf attaques supplémentaires détectées au total et seize FP en moins. **Il manque toutefois trois attaques repérées par cette Isolation Forest**, et en repère douze qu’elle manque : l’amélioration globale n’est pas une domination sur chaque observation. Son rappel de 32,56 % reste faible. Une seule comparaison ne justifie pas « le Deep Learning est meilleur ».

L’autoencodeur apprend à reconstruire le normal validé ; la forêt apprend les régularités de septembre incluant des attaques. Les objectifs et corpus diffèrent. Le normaliseur du réseau est réutilisé par `transform`, sans `fit` sur octobre. L’imputation par médiane d’octobre suit ici le kit ; pour une chaîne de production, définir une préparation stable et sa gestion des manques, sans mélanger cette expérience à notre stratégie V2.

**À périmètre V2 comparable**, en retirant les quatorze vrais volumes absents, le même autoencodeur produit **6 FP, 141 FN, 70 VP, 1 888 VN** sur 2 105 lignes : précision 92,11 %, rappel **33,18 %**, 76 alertes. Il ne remplace pas notre union V2 (37 FP, 9 FN, 202 VP). Ce calcul supplémentaire utilise toujours le réseau de Hugo, sans réentraînement.


![Inférence sur octobre, matrice de confusion et comparaison par groupe](../../assets/img/ia-cybersecurite/it-4/Capture%20d’écran%20du%202026-10-22%2010-18-45.png)

*Capture de l’apprenant, 10:18:45 : la table croisée affiche **70 VP, 145 FN, 6 FP et 1 898 VN**. Le tableau confirme neuf VPN détectés sur neuf et quatre fausses alertes sur la sauvegarde, contre dix-neuf pour IF. Le code visible utilise la médiane et IF0,05 : ces sorties concernent les **2 119 lignes du périmètre pédagogique**, distinct du périmètre V2.*

### R3 — Qu’est-ce qui dérange le réseau ?

Pour l’observation du **09/10 à 3 h**, le volume est **8 690,075 Mo**. L’erreur quadratique de reconstruction de la composante volume vaut **928,97**, contre 0,08 à 0,60 pour chacune des autres composantes affichées. Il domine donc l’erreur moyenne, d’environ **132,97**, très au-dessus du seuil 2,7615.

**Ces erreurs portent sur les données normalisées : 928,97 n’est pas un nombre de Mo.** Elles montrent ce que le réseau recopie mal, pas l’intention de la personne. Pour la première sauvegarde examinée (28/09 à 1 h, 1 666,53 Mo), l’erreur volume vaut seulement 0,15 et l’erreur moyenne environ 0,033 : cette observation n’est pas signalée. Cela n’exclut pas les quatre autres fausses alertes de sauvegarde du bilan.

Phrase pour Nadia : « Le réseau a signalé un transfert dont le volume s’écarte fortement de ce qu’il sait reconstruire ; il faut vérifier le compte, la destination et la justification du transfert avant de décider d’une mesure. » **Cette explication seule ne suffit pas à couper un accès VPN.** Appliquer la procédure d’incident avec les éléments de contexte et la décision d’un analyste.


![Erreurs de reconstruction de l’exfiltration et de la première sauvegarde](../../assets/img/ia-cybersecurite/it-4/Capture%20d’écran%20du%202026-10-22%2010-19-17.png)

*Capture de l’apprenant, 10:19:17 : le volume du transfert est de 8 690,075 Mo, avec une erreur quadratique de reconstruction **928,97 sur la composante normalisée**. La sauvegarde examinée vaut 1 666,53 Mo et son erreur volume est de 0,15. La comparaison aide à interpréter le score ; elle ne révèle pas à elle seule une intention malveillante.*

### R4 — Trois altérations possibles et limites de SHA-256

Le fichier pourrait être remplacé sur le poste d’entraînement compromis, modifié sur un partage accessible en écriture, ou substitué dans l’archive/copie de distribution. La référence elle-même peut aussi être falsifiée si son canal n’est pas protégé.

SHA-256 vérifie que les octets reçus correspondent à la référence attendue ; il ne démontre pas la qualité du modèle, son innocuité, l’absence d’empoisonnement avant publication, ni l’identité réelle de son auteur. Une empreinte ne prouve la provenance qu’avec une référence et une chaîne de confiance fiables.

### R5 — Ce que cela apprend sur les grands modèles

Une multitude de paramètres ne se résume pas à des règles lisibles. Il faut connaître le producteur, la version et les données annoncées, vérifier les artefacts, puis mesurer les erreurs et limites sur son propre besoin. Une explication plausible ne garantit pas une bonne décision.

Un LLM et cet autoencodeur utilisent des réseaux de neurones, mais **ce ne sont pas la même architecture ni le même objectif** : le LLM génère des tokens ; ici un petit réseau reconstruit sept mesures. Le principe de vérifier les sources et d’évaluer les sorties se transpose, pas les résultats de performance du TP.

## Tableau comparatif rempli — Référence V2 et réseau de Hugo

Les chiffres ci-dessous portent sur **les 2 105 mêmes observations conservées** ; le tableau précédent reste la comparaison pédagogique du notebook.

| Critère | Arbre V2 | Isolation Forest V2 0,03 | Autoencodeur pré-entraîné |
| --- | --- | --- | --- |
| Besoin d’étiquettes ? | Oui, pour apprendre normal/attaque | Non pour ajuster ; oui pour mesurer ses erreurs | Pas d’étiquette en prédiction ; normal validé sélectionné à l’entraînement grâce aux annotations |
| Nombre de paramètres ou règles | 5 séparations, 6 feuilles ; profondeur maximale 3 | 100 arbres d’isolation par défaut, pas 100 règles simples | 186 poids/biais ; seuil fourni 2,7615 et normaliseur associés |
| Exfiltrations VPN repérées ? | **0/9** | **5/9** | **9/9** |
| Fausses alertes sur sauvegarde | **0** | **10** | **4** |
| Peut-on expliquer une alerte à Nadia ? | Chemin de seuils exact | Score d’isolement et contexte ; moins direct | Erreurs par caractéristique ; explication partielle, pas preuve causale d’attaque |
| Qui entraîne et quelles données confier ? | Équipe modèle/supervision, avec les exemples étiquetés et préparation validés | Équipe modèle/supervision avec corpus représentatif, sans réponses requises pour ajuster | Hugo selon le kit, sur le normal validé ; conserver normaliseur, ordre des entrées, seuil, provenance et versions |

Les nombres de paramètres, d’arbres et de règles ne sont pas des unités comparables de qualité ou de complexité. Les responsables du tableau décrivent le scénario ou des rôles proposés, pas une délégation réellement mise en place chez Hexalp.

## Livrables et preuves

Dans le kit J4 : **`04_autoencodeur.ipynb`** complété/exécuté (18 cellules, dont 9 de code), original **`04_autoencodeur.source.ipynb`** conservé, **`preuves/autoencodeur_47.json`** et **`preuves/execution_autoencodeur_47.txt`**. Le générateur **`completer_notebook_47.py`** est conservé au niveau de l’itération dans les livrables.

L’inférence a été exécutée localement avec Python 3.14.4, pandas 3.0.6 et Scikit-learn 1.9.1. Le calcul SHA-256 dans la VM est attesté par la capture de l’apprenant ; quatre captures supplémentaires documentent maintenant le contrôle dans le notebook, l’architecture, l’inférence et les erreurs de reconstruction chez l’apprenant. Elles ne montrent pas l’adresse du serveur ni ses versions : l’environnement exact de ces vues n’est pas vérifiable sur les seules images. Les empreintes avant/après correspondent à la référence du PDF. Le script V2 et son fichier d’alertes restent inchangés ; le PDF intermédiaire attend l’actualisation finale.

**Sources :** kit apprenant PDF, section 4.7 ; notebook 04 fourni ; résultats locaux conservés ; [documentation officielle sur la persistance des modèles](https://scikit-learn.org/stable/model_persistence.html), consultée le 22/10/2026.

- [Attaquer son modèle — 4.6](attaquer-son-modele.md)
- [Rapport d’évaluation — 4.4](le-rapport-evaluation.md)
