# Mettre en place un classifieur

**45 min — Présentiel**

## Le concept — Une chaîne, pas une action unique

Une erreur de préparation, de choix des caractéristiques ou d'évaluation se répercute dans les alertes. Choisir un algorithme ne compense pas des données mal représentées. Cette fiche renseigne les missions conceptuelles de **3.2** ; elle ne lance pas les modèles du kit.

## Vocabulaire clé

| Terme | Ce que c'est concrètement |
| --- | --- |
| **Classifieur** | Modèle supervisé attribuant une catégorie à une observation, par exemple « normal » ou « attaque » selon les références apprises |
| **Arbre de décision** | Suite de questions sur les caractéristiques ; la machine apprend les variables et seuils de séparation, dans les limites fixées par les hyperparamètres |
| **Détection d'anomalies** | Repérage de comportements atypiques sans apprendre directement une étiquette « attaque » ; atypique ne veut pas dire malveillant |
| **Isolation Forest** | Détecteur qui isole aléatoirement les observations ; celles isolées en peu de séparations sont considérées comme plus atypiques |
| **Hyperparamètre** | Réglage choisi avant l'entraînement, par exemple `max_depth` ou `contamination` ; ce dernier règle le seuil lié à la proportion attendue d'anomalies, pas une proportion d'attaques prouvée |
| **Paramètre appris** | Élément déterminé à partir des exemples, par exemple les seuils de séparation de l'arbre |
| **Graine — `random_state`** | Contrôle les tirages aléatoires concernés ; aide à reproduire un calcul avec mêmes données, ordre, code, réglages et environnement. Une graine seule ne garantit pas la reproductibilité de tout le projet |
| **Matrice de confusion** | Croise étiquettes de référence et prédictions ; vérifier l'ordre des classes et des axes avant d'interpréter VP, VN, FP et FN |
| **Précision — precision** | `VP / (VP + FP)` : parmi les alertes, proportion d'attaques selon les étiquettes de référence |
| **Rappel — recall** | `VP / (VP + FN)` : parmi les attaques de référence, proportion détectée |
| **Justesse — accuracy** | `(VP + VN) / total` : proportion de prédictions correctes ; à distinguer de la précision des alertes, notamment si les classes sont déséquilibrées |

Si le dénominateur d'une métrique est nul, préciser la convention de calcul ; ne pas annoncer automatiquement un score parfait. Sources : [Google — métriques de classification](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall?hl=fr) et [Inria — cours Scikit-learn](https://inria.github.io/scikit-learn-mooc/), consultés le **21 octobre 2026**.

## Mission 1 — Ma chaîne du J1

Le tableau reprend la résolution documentée des [18 observations SSH du J1](../it-1/machine-learning-apprendre-exemples.md). « J'ai » décrit ce travail pédagogique, pas une collecte réelle chez Hexalp ni un test à l'aveugle attesté.

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

Vérifier calendrier, source, responsable et autorisation. Inversement, une attaque peut imiter le comportement habituel et ne produire aucune anomalie détectable. Voir les [scénarios de la supervision](le-projet-de-la-supervision.md).

### 3. Qui fournit les étiquettes et que se passe-t-il en cas d'erreur ?

Les analystes SOC, équipes de réponse à incident ou responsables métier qualifient les événements à partir de preuves. Pour Zabbix, les décisions de l'astreinte peuvent servir de point de départ, avec une définition commune de « utile ». Dans le CSV du kit, les étiquettes sont **fictives et fournies** : nous ne les avons pas établies à partir d'incidents réels.

Une erreur d'étiquetage peut apprendre au modèle à ignorer des attaques ou à alerter sur des usages normaux. Elle fausse aussi l'évaluation si le jeu de test contient ces erreurs. Prévoir revue des cas ambigus, traçabilité, possibilité de rectification et vérification indépendante d'un échantillon. Ne pas transformer automatiquement toutes les prédictions du modèle en nouvelles étiquettes de référence.

## Repères d'évaluation

| Référence réelle / prédiction | Prédit attaque | Prédit normal |
| --- | --- | --- |
| **Étiquette attaque** | Vrai positif — VP | Faux négatif — FN |
| **Étiquette normal** | Faux positif — FP | Vrai négatif — VN |

Une sortie numérique « attaque » est **une classe prédite**, pas une confirmation d'incident. La décision opérationnelle reste à l'analyste. Le projet J3 produit des alertes à qualifier et ne déclenche aucun blocage.

## Travail consigné et état de preuve

Les réponses de cette séquence sont également consignées dans **`livrables/ia-cybersecurite/it-3/ia01-j3/carnet_J3.md`**. Le carnet est commencé pour les seules missions reçues : tableau Bash / pandas, questions des notebooks et fiche du modèle seront complétés aux étapes correspondantes.

**Aucun notebook ni script du kit n'a été exécuté ou modifié pour cette fiche ; aucun modèle J3 n'est entraîné.** Les résultats cités concernent uniquement l'exercice des 18 lignes du J1.

## Ressources

- [Scikit-learn — Choisir un estimateur](https://scikit-learn.org/stable/machine_learning_map.html)
- [Google — Justesse, précision et rappel](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall?hl=fr)
- [Inria — Cours Scikit-learn](https://inria.github.io/scikit-learn-mooc/)

Sources consultées le **21 octobre 2026**.

[Retour à l'itération 3](index.md)
