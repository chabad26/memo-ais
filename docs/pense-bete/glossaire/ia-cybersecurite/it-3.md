# IA et Cybersécurité — Itération 3 : Détecter

## Repères du programme

| Terme | Repère |
| --- | --- |
| Classifieur supervisé | Apprend à partir d'observations accompagnées d'étiquettes ; ses prédictions restent à évaluer |
| Détecteur d'anomalies | Repère des observations atypiques sans apprendre les étiquettes d'attaque ; une anomalie doit être qualifiée |
| Caractéristique | Information utilisée en entrée du modèle, choisie et préparée à partir des journaux |
| Reproductibilité | Conserver données, dépendances, préparation et paramètres nécessaires à la répétition du travail |
| Notebook | Document mêlant explications, code et résultats ; fichier complété et exécution effective sont à distinguer |
| Alerte à qualifier | Signal destiné à l'analyste, sans action automatique de blocage prévue par le contexte |

## Livrables à suivre

Dossier **`ia01-j3`** : `carnet_J3.md`, les deux notebooks complétés et exécutés, `detection_ssh.py` commenté avec `requirements.txt`, et `alertes_a_qualifier.csv` produit par le script.

Le carnet réunira les réponses du kit et des notebooks, le tableau Bash / pandas et la fiche du modèle. Les données du kit sont fictives ; aucun journal réel n'est nécessaire pour cette activité.

## État du travail

Présentation du J3 et fiche d’ouverture intégrées. Le tableau des cinq scénarios fail2ban est renseigné ; les résultats des modèles sont explicitement non testés. Le nouveau scénario annonce l’arrêt du script de Sofia et la révocation de sa clé, sans intervention réelle attestée. Les cinq fichiers du kit sont reçus dans `livrables/ia-cybersecurite/it-3/ia01-j3/` : CSV de 1 704 observations et 11 colonnes, deux notebooks aux compteurs non renseignés, dépendances figées et squelette à compléter. Arbre de décision et Isolation Forest sont explicitement présents dans le squelette. Aucune installation, exécution de notebook, mesure de performance ou production d'alertes n'est attestée. Les séquences détaillées seront ajoutées à réception des consignes.

## Repères de la supervision

- Seuil fourni : cinq échecs par IP en dix minutes, sur les événements reconnus et collectés par la jail.
- Faible rythme, connexions réussies et journaux absents restent des limites pour cette règle.
- Un audit autorisé peut ressembler à une attaque ; vérifier source, périmètre et fenêtre approuvée.
- Un modèle local ne voit pas les événements absents des données et ne bloque rien automatiquement.

## Docs associées

- [Itération 3 — Détecter : votre premier modèle](../../../ia-cybersecurite/it-3/index.md)
- [Présentation du module](../../../ia-cybersecurite/README.md)
- [Exercice manuel du J1](../../../ia-cybersecurite/it-1/machine-learning-apprendre-exemples.md)

- [Le projet de la supervision](../../../ia-cybersecurite/it-3/le-projet-de-la-supervision.md)

## Séquence 3.2 — Chaîne et choix du modèle

Neuf étapes reliées au J1 et cinq besoins classés. R1 avait 2 FP/2 FN sur six cas ; R2 a été ajustée après lecture du test et demande une nouvelle évaluation indépendante. Précision = VP/(VP+FP), rappel = VP/(VP+FN). Une attaque nouvelle peut parfois être détectée par des caractéristiques communes ; rien ne le garantit. Graine et versions doivent être conservées ensemble pour la reproductibilité.

Le carnet `livrables/ia-cybersecurite/it-3/ia01-j3/carnet_J3.md` est commencé pour 3.1/3.2. Notebooks et script restent inchangés, modèles non entraînés.

- [Mettre en place un classifieur](../../../ia-cybersecurite/it-3/mettre-en-place-classifieur.md)

## Séquence 3.3 — Environnement local

Procédure rédigée, complétée par six captures de la VM : venv distinct du Python système, `python -m pip`, versions et dépendances à contrôler, Jupyter sur `127.0.0.1:8888` avec authentification. Sans navigateur VM : tunnel SSH lié à la boucle locale du poste. PEP 668 protège le Python géré par la distribution ; un venv n’est pas un bac à sable. `scikit-learn` est la distribution, `sklearn` le nom d’import. Les hachages contrôlent les distributions attendues, pas leur innocuité. Ne jamais publier le jeton Jupyter.

- [Installer son environnement](../../../ia-cybersecurite/it-3/installer-son-environnement.md)

### Preuves de la séquence 3.3

JupyterLab ouvert, venv actif avec pandas 3.0.6, refus du paquet sklearn et écoute 127.0.0.1:8888 observés. Le premier dry-run pandas était dans le venv. La capture 10-15-50 montre le second hors venv : `No module named pip`. Essai effectué, sans preuve d’un refus PEP 668 ; pip système absent. Première cellule et `pip check` non montrés ; aucun entraînement attesté.

## Séquence 3.4 — Python de survie

`NameError` : nom Echecs au lieu de echecs ; `KeyError` : clé accentuée inexistante ; `TypeError` : addition chaîne/entier, convertir avec `int`. pandas : `len(df)`, `value_counts()`, filtre par masque, `sort_values`, `nunique()`. Attention à l’en-tête CSV côté Bash et aux valeurs manquantes.

CSV brut vérifié séparément : 1 704 lignes, 138 IP, 1 587 normal / 117 attaque. Les cinq plus gros volumes viennent de 10.20.8.30 et sont étiquetés normal ; transfert nocturne récurrent compatible avec une sauvegarde, rôle non confirmé. Volume manquant le 19/09 à 1 h. Notebook source intact, exécution VM complète non attestée.

- [Python de survie](../../../ia-cybersecurite/it-3/python-de-survie.md)

### Captures pandas du 21 octobre

Cinq captures attestent chargement et cellules pandas : 1 704 × 11, maximum 298 échecs, 1 566 lignes internes/138 externes, 117 attaques, 138 IP via `unique()` et filtre nocturne avec succès de 127 lignes. `nunique()` renvoie directement le nombre, `unique()` la liste. Le top des volumes confirme 10.20.8.30, sans confirmer son rôle de sauvegarde. Les erreurs des bases et l’exécution complète restent non montrées.

Capture complémentaire 10-25-37 : `df["ip_source"].nunique()` retourne directement **138**. L’exercice b est désormais attesté avec le comptage demandé, en plus de la liste précédente.

## Séquence 3.5 — Préparation

Brut : 6,87 % d’attaques ; toujours normal donne 93,13 % de justesse mais zéro rappel. 90 volumes manquants sur deux périodes, dont neuf attaques. Choix proposé : retirer ces lignes du jeu complet sans les perdre du suivi ; restent 1 614 lignes et 108 attaques. Ne pas assimiler volume inconnu à zéro. Si imputation : ajustement sur entraînement seulement.

Sept caractéristiques : heure, externe, échecs, succès, comptes distincts, durée et volume. Exclure étiquette de X ; date/IP pour éviter mémorisation ici ; fail2ban pour comparaison indépendante. Scanner interne 10.20.1.250 compatible avec audits les 15/22 septembre à 21/22 h, rôle non prouvé par CSV seul. Parties A/B et nettoyage préparés, non exécutés dans la VM à ce stade.

- [Explorer et préparer les journaux](../../../ia-cybersecurite/it-3/explorer-preparer-journaux.md)

### Captures de préparation

Quatre captures montrent chargement brut, graphique après définition de `couleurs`, manques NetFlow et codage externe. Les sept caractéristiques sont définies, mais X reste à (1704, 7), 117 attaques ; le nettoyage contient encore `___`. Appliquer la stratégie retenue puis recréer X/y : attendu (1614, 7), 108 attaques et zéro volume manquant, non encore observé.

## Séquence 3.6 — Arbre exécuté : sept captures

Nettoyage confirmé ensuite : 1 614 lignes, 108 attaques ; entraînement 1 129 lignes (76 attaques), test 485 (32 attaques). Arbre profondeur 3 : 453 VN, 0 FP, 4 FN, 28 VP ; rappel 87,5 %, précision 100 % et justesse 99,18 % sur ce test. fail2ban historique : rappel 17/32 = 53,125 %, zéro FP. Onze attaques complémentaires montrées.

Six feuilles fondées sur comptes/durée/origine/heure ; ni échecs ni volume utilisés directement. Branche interne ≥4 comptes et heure ≥20 classée normal : raccourci dangereux, pas autorisation. Quatre FN externes sur un compte et durée 24–57 minutes. Profondeur demandée 10 / None : 1 FN, zéro FP, huit feuilles, à valider sur un autre jeu après comparaison. Les chiffres génériques 1 192/35 ne correspondent pas au test nettoyé observé. Notebook VM complété à rapatrier ; Isolation Forest non encore attesté.

- [Le classifieur supervisé](../../../ia-cybersecurite/it-3/le-classifieur-supervise.md)

## Séquence 3.7 — Isolation Forest, à exécuter dans l’ordre

`fit(X)` sans y ; `decision_function` bas = atypique, `predict==-1` = signalé, pas attaque certaine. Départ proposé contamination 0,03 ; masquer étiquette dans le top15 avant qualification. Le notebook ajuste et examine tout X : pas un test indépendant comparable directement au test de l’arbre.

Capacité 30/semaine : environ 60 sur deux semaines ; 3 % de 1 614 ≈49, valeur de budget non observée. FP/FN et drapeaux de Julien restent à relever. Pour Julien, afficher aussi anomalie : les agrégats SSH ne montrent pas le copier-coller dans un chatbot. Tableau comparatif renseigné avec résultats supervisés observés et hypothèses non supervisées signalées comme telles.

- [La détection d’anomalies](../../../ia-cybersecurite/it-3/la-detection-anomalies.md)

### Résultats Isolation Forest — Captures 11:03 à 11:06

À 0,03 : 49 alertes, 44 VP/5 FP/64 FN/1 501 VN ; précision 89,80 %, rappel 40,74 %. FP : scanner 3 lignes, sauvegarde 2. Top15 : quinze attaques de référence, qualifications antérieures à la révélation non montrées. À 0,05 : 81 alertes, 64 VP/17 FP/44 FN ; à 0,10 : 162 alertes, 104 VP/58 FP/4 FN. Seul 0,03 respecte 30 alertes/semaine en moyenne sur deux semaines, sans garantir un maximum hebdomadaire ni un risque acceptable.

Julien : False aux trois heures, scores 0,089614 / 0,123859 / 0,113330 ; aucune visibilité sur le contenu envoyé au chatbot. Détail des 64 FN encore à analyser. Ces résultats portent sur toutes les données d’ajustement, pas sur le test indépendant de l’arbre. Notebook exécuté à rapatrier et script final à produire.

## Séquence 3.8 — Script et CSV produits

`detection_ssh.py` complété et commenté avec assistance, squelette conservé. Tests de l’assistant dans un venv séparé : deux exécutions à42 identiques octet par octet, règles et métriques identiques aux captures ; essai à7 séparé. Fichiers et empreintes dans `livrables/ia-cybersecurite/it-3/ia01-j3/preuves/`.

Export union : 111 alertes, 45 puis66/semaine, budget30 dépassé. Descriptif sur tout X : 106 VP/5 FP/2 FN, pas une évaluation indépendante. IF seul20 puis29 ne représente pas la charge combinée. Graine7 : 108 alertes, 44 puis64 ; règles différentes malgré mêmes FP/FN arbre sur un test différent. Réentraînement/étiquettes requis par le démonstrateur : pas prêt au cron hebdomadaire sans chaîne de prédiction, validation, qualité des données et gouvernance. Fiche modèle consignée ; notebooks VM à récupérer et commentaires à relire personnellement.

- [Le script de détection](../../../ia-cybersecurite/it-3/le-script-de-detection.md)

### Captures du script dans la VM

11-20-40/11-20-55 : graine7 exécutée dans le venv Debian, résultats concordants avec l’essai séparé ; union108 (104 VP/4 FP/4 FN), 44 puis64 alertes/semaine. Budget dépassé et retour au prompt visibles. Pas de preuve de deux relances42 ou d’identité des fichiers entre VM et environnement de vérification.
