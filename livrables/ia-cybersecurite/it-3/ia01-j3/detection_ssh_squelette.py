"""
detection_ssh.py — Détection de connexions SSH suspectes chez Hexalp
IA-01 · Jour 3

Auteur  : ___
Date    : ___
Usage   : python detection_ssh.py
Entrée  : hexalp_ssh_sept2026.csv (une ligne = l'activité d'une IP pendant une heure)
Sortie  : alertes_a_qualifier.csv

Ce script NE BLOQUE RIEN. Il produit une liste d'alertes classées par score,
destinée à un analyste qui décide de la suite.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.ensemble import IsolationForest
from sklearn.metrics import confusion_matrix, classification_report

# ---------------------------------------------------------------------------
# 0. Paramètres
# ---------------------------------------------------------------------------
FICHIER_ENTREE = "hexalp_ssh_sept2026.csv"
FICHIER_ALERTES = "alertes_a_qualifier.csv"
GRAINE = 42
# TODO commentaire : expliquez ce bloc et pourquoi on le fait ainsi.

CARACTERISTIQUES = [___]
# TODO commentaire : expliquez ce bloc et pourquoi on le fait ainsi.

PROFONDEUR_ARBRE = ___
CONTAMINATION = ___
# TODO commentaire : expliquez ce bloc et pourquoi on le fait ainsi.

# ---------------------------------------------------------------------------
# 1. Chargement
# ---------------------------------------------------------------------------
df = pd.read_csv(FICHIER_ENTREE)
print(f"{len(df)} observations chargées depuis {FICHIER_ENTREE}")

# ---------------------------------------------------------------------------
# 2. Nettoyage et préparation
# ---------------------------------------------------------------------------
# TODO commentaire : expliquez ce bloc et pourquoi on le fait ainsi.
___

# TODO commentaire : expliquez ce bloc et pourquoi on le fait ainsi.
df["externe"] = (df["origine"] == "externe").astype(int)

X = df[CARACTERISTIQUES]
y = (df["etiquette"] == "attaque").astype(int)

# ---------------------------------------------------------------------------
# 3. Classifieur supervisé : arbre de décision
# ---------------------------------------------------------------------------
# TODO commentaire : expliquez ce bloc et pourquoi on le fait ainsi.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=GRAINE
)

arbre = DecisionTreeClassifier(max_depth=PROFONDEUR_ARBRE, random_state=GRAINE)
___
# TODO commentaire : expliquez ce bloc et pourquoi on le fait ainsi.

predictions = ___
tn, fp, fn, tp = confusion_matrix(y_test, predictions).ravel()

print("\n=== Arbre de décision (jeu de test) ===")
print(export_text(arbre, feature_names=CARACTERISTIQUES))
print(classification_report(y_test, predictions, target_names=["normal", "attaque"]))
print(f"Faux positifs : {fp} | Faux négatifs : {fn}")
# TODO commentaire : expliquez ce bloc et pourquoi on le fait ainsi.

# ---------------------------------------------------------------------------
# 4. Détection d'anomalies : Isolation Forest
# ---------------------------------------------------------------------------
# TODO commentaire : expliquez ce bloc et pourquoi on le fait ainsi.
iforest = IsolationForest(contamination=CONTAMINATION, random_state=GRAINE)
___

df["score_anomalie"] = iforest.decision_function(X)
df["anomalie"] = iforest.predict(X) == -1
df["avis_arbre"] = arbre.predict(X)

print("\n=== Isolation Forest (toutes les observations) ===")
print(pd.crosstab(df["anomalie"], df["etiquette"]))

# ---------------------------------------------------------------------------
# 5. Liste d'alertes pour l'analyste
# ---------------------------------------------------------------------------
# TODO commentaire : expliquez ce bloc et pourquoi on le fait ainsi.
alertes = df[___].sort_values("score_anomalie")

colonnes = ["date", "heure", "ip_source", "origine", "echecs_auth", "succes_auth",
            "comptes_distincts", "octets_sortants_mo", "score_anomalie", "anomalie", "avis_arbre"]
alertes[colonnes].to_csv(FICHIER_ALERTES, index=False)
print(f"\n{len(alertes)} alertes écrites dans {FICHIER_ALERTES}")
