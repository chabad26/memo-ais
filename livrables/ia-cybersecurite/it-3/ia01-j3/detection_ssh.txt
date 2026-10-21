"""Évaluer deux modèles SSH sur le kit fictif Hexalp et exporter des alertes.

IA-01 / J3 — Olivier HIMBLOT, avec assistance à la rédaction, 21 octobre 2026.
Usage : python detection_ssh.py [--graine 42] [--entree fichier.csv] [--sortie alertes.csv]
Ce démonstrateur réentraîne les modèles et exige des étiquettes : il n'est pas
un service de détection hebdomadaire prêt à la production. Aucune action sur le SI.
Les commentaires sont une proposition à relire et expliquer par l'apprenant.
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text

# Les chemins par défaut partent du script, pas du terminal de lancement.
DOSSIER = Path(__file__).resolve().parent
FICHIER_ENTREE = DOSSIER / "hexalp_ssh_sept2026.csv"
FICHIER_ALERTES = DOSSIER / "alertes_a_qualifier.csv"
GRAINE = 42

# On décrit le comportement, sans donner la réponse ni copier le contrôle fail2ban.
# Date et IP restent dans le résultat pour que l'analyste retrouve les événements.
CARACTERISTIQUES = [
    "heure", "externe", "echecs_auth", "succes_auth", "comptes_distincts",
    "duree_session_min", "octets_sortants_mo",
]
PROFONDEUR_ARBRE = 3
CONTAMINATION = 0.03
# Garder les mêmes réglages que les captures facilite la comparaison.
# L'export retient l'union : une attaque vue par un seul modèle reste examinable.
# Ce choix peut dépasser le budget d'astreinte ; il est mesuré, pas caché.


def bilan(nom, reference, prediction):
    """Afficher des comptes explicites, en conservant l'ordre normal / attaque."""
    tn, fp, fn, tp = confusion_matrix(reference, prediction, labels=[0, 1]).ravel()
    print(f"\n=== {nom} ===")
    print(classification_report(
        reference, prediction, labels=[0, 1],
        target_names=["normal", "attaque"], zero_division=0,
    ))
    print(f"VN={tn} FP={fp} FN={fn} VP={tp}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entree", type=Path, default=FICHIER_ENTREE)
    parser.add_argument("--sortie", type=Path, default=FICHIER_ALERTES)
    parser.add_argument("--graine", type=int, default=GRAINE)
    args = parser.parse_args()
    if args.entree.resolve() == args.sortie.resolve():
        parser.error("La sortie doit être distincte du CSV d'entrée.")

    # Refuser un schéma inattendu évite de produire silencieusement de faux avis.
    df = pd.read_csv(args.entree)
    attendues = {
        "date", "heure", "ip_source", "origine", "echecs_auth", "succes_auth",
        "comptes_distincts", "duree_session_min", "octets_sortants_mo",
        "fail2ban_ban", "etiquette",
    }
    if not attendues.issubset(df.columns):
        raise ValueError(f"Colonnes manquantes : {sorted(attendues - set(df.columns))}")
    if df.empty:
        raise ValueError("Le fichier ne contient aucune observation.")
    if df[list(attendues - {"octets_sortants_mo"})].isna().any().any():
        raise ValueError("Champ obligatoire manquant hors volume NetFlow.")
    if not df["origine"].isin(["interne", "externe"]).all():
        raise ValueError("Origine inconnue : ne pas la convertir en interne.")
    if not df["etiquette"].isin(["normal", "attaque"]).all():
        raise ValueError("Étiquette inconnue : jeu évalué obligatoirement qualifié.")

    # Valider les mesures avant toute suppression : une chaîne illisible n'est pas zéro.
    mesures = [c for c in CARACTERISTIQUES if c != "externe"]
    df[mesures] = df[mesures].apply(pd.to_numeric, errors="raise")
    valeurs = df[mesures].to_numpy(dtype=float)
    if np.isinf(valeurs).any() or (df[mesures] < 0).any().any():
        raise ValueError("Mesure négative ou infinie.")
    if not df["heure"].between(0, 23).all() or (df["heure"] % 1 != 0).any():
        raise ValueError("L'heure doit être un entier de 0 à 23.")
    dates_brutes = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="raise")
    print(f"Graine={args.graine}, profondeur={PROFONDEUR_ARBRE}, contamination={CONTAMINATION}")
    print(f"{len(df)} observations brutes, du {dates_brutes.min().date()} au {dates_brutes.max().date()}")

    # Une sonde en panne n'a pas mesuré zéro octet. On reproduit le choix du TP :
    # ces lignes sont exclues du modèle complet et explicitement comptées hors couverture.
    absentes = df["octets_sortants_mo"].isna()
    print(f"Hors couverture : {absentes.sum()} volumes manquants, "
          f"dont {(df.loc[absentes, 'etiquette'] == 'attaque').sum()} attaques de référence")
    df = df.loc[~absentes].copy()
    df["externe"] = (df["origine"] == "externe").astype(int)
    X = df[CARACTERISTIQUES]
    y = (df["etiquette"] == "attaque").astype(int)
    if y.nunique() != 2 or y.value_counts().min() < 2:
        raise ValueError("Deux classes avec assez d'exemples sont nécessaires au partage stratifié.")

    # Réserver le même test que le notebook : ni l'IP, ni l'étiquette, ni fail2ban
    # n'entrent dans X. Le partage aléatoire reste une limite pour des séries temporelles.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=args.graine,
    )
    print(f"Après nettoyage : {len(df)} lignes, {int(y.sum())} attaques")
    print(f"Entraînement : {X_train.shape} ; test : {X_test.shape}")
    arbre = DecisionTreeClassifier(max_depth=PROFONDEUR_ARBRE, random_state=args.graine)
    arbre.fit(X_train, y_train)
    predictions = arbre.predict(X_test)
    print(export_text(arbre, feature_names=CARACTERISTIQUES))
    bilan("Arbre, test indépendant de son ajustement", y_test, predictions)
    bilan("fail2ban historique, mêmes lignes test", y_test, df.loc[X_test.index, "fail2ban_ban"])

    # Comme dans la partie D, l'Isolation Forest voit toutes les observations sans y.
    # Comparer ensuite à y aide l'analyse, mais ce n'est PAS un test sur données nouvelles.
    iforest = IsolationForest(contamination=CONTAMINATION, random_state=args.graine)
    iforest.fit(X)
    df["score_anomalie"] = iforest.decision_function(X)
    df["anomalie"] = iforest.predict(X) == -1
    df["avis_arbre"] = arbre.predict(X)
    bilan("Isolation Forest, toutes les données d'ajustement", y, df["anomalie"].astype(int))
    print("Attention : avis_arbre sur tout X inclut ses lignes d'entraînement.")

    # L'union préserve les signaux complémentaires. Le tri stable et ses départages
    # rendent l'export déterministe à données et environnement identiques.
    masque = df["anomalie"] | (df["avis_arbre"] == 1)
    alertes = df.loc[masque].sort_values(
        ["score_anomalie", "date", "heure", "ip_source"], kind="stable",
    )
    colonnes = [
        "date", "heure", "ip_source", "origine", "echecs_auth", "succes_auth",
        "comptes_distincts", "octets_sortants_mo", "score_anomalie", "anomalie", "avis_arbre",
    ]
    alertes[colonnes].to_csv(args.sortie, index=False)
    print(f"\n{len(alertes)} alertes écrites dans {args.sortie.name}")
    bilan("Union descriptive sur toutes les lignes, pas test indépendant", y, masque.astype(int))

    # Compter par semaine réelle rend visibles les pics masqués par une moyenne.
    # Les semaines sans alerte restent affichées si des observations existent.
    semaines = pd.to_datetime(df["date"]).dt.to_period("W-SUN")
    hebdo = pd.DataFrame({"semaine": semaines.astype(str), "alerte": masque})
    print("Alertes union par semaine (lundi-dimanche) :")
    print(hebdo.groupby("semaine")["alerte"].sum().to_string())
    if (hebdo.groupby("semaine")["alerte"].sum() > 30).any():
        print("BUDGET DÉPASSÉ : 30 alertes/semaine. Revue humaine et arbitrage requis.")
    print("Aucune action de blocage ; revue SOC/astreinte obligatoire.")


if __name__ == "__main__":
    main()
