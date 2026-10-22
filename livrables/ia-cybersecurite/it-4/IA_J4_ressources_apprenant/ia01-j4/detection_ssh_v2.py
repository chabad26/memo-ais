"""Hexalp J4 : apprendre sur septembre, évaluer octobre, sans action sur le SI.

Olivier HIMBLOT — 22 octobre 2026 — rédaction avec assistance, à relire.
Évolution du script J3 ; ses paramètres et l'ordre des caractéristiques sont conservés.
Usage : python detection_ssh_v2.py
Octobre peut ne pas contenir d'étiquettes : on exporte alors sans calculer les erreurs.
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text

DOSSIER = Path(__file__).resolve().parent
GRAINE = 42
PROFONDEUR_ARBRE = 3
CONTAMINATION = 0.03
CARACTERISTIQUES = [
    "heure", "externe", "echecs_auth", "succes_auth", "comptes_distincts",
    "duree_session_min", "octets_sortants_mo",
]
COLONNES = {
    "date", "heure", "ip_source", "origine", "echecs_auth", "succes_auth",
    "comptes_distincts", "duree_session_min", "octets_sortants_mo", "fail2ban_ban",
}


def preparer(chemin, nouvelle_sonde, seuil_manques):
    """Contrôler le contrat de données avant toute prédiction et tracer les exclusions."""
    df = pd.read_csv(chemin)
    requises = COLONNES | ({"octets_sortants_ko"} if nouvelle_sonde else {"etiquette"})
    autorisees = requises | {"etiquette"}
    if not requises.issubset(df.columns) or set(df.columns) - autorisees:
        raise ValueError(f"{chemin.name} : schéma absent/inconnu, conversion à revoir")
    if df.empty:
        raise ValueError("Fichier vide")
    obligatoires = list(COLONNES - {"octets_sortants_mo"})
    if df[obligatoires].isna().any().any():
        raise ValueError("Champ obligatoire manquant hors mesure NetFlow")
    if not df["origine"].isin(["interne", "externe"]).all():
        raise ValueError("Origine inconnue")
    if "etiquette" in df and not df["etiquette"].isin(["normal", "attaque"]).all():
        raise ValueError("Étiquette absente ou inconnue")
    mesures = [x for x in CARACTERISTIQUES if x != "externe"]
    if nouvelle_sonde:
        mesures += ["octets_sortants_ko"]
    df[mesures] = df[mesures].apply(pd.to_numeric, errors="raise")
    if np.isinf(df[mesures].to_numpy(dtype=float)).any() or (df[mesures] < 0).any().any():
        raise ValueError("Mesure négative/infinie")
    if not df["heure"].between(0, 23).all() or (df["heure"] % 1 != 0).any():
        raise ValueError("Heure incohérente")
    pd.to_datetime(df["date"], format="%Y-%m-%d", errors="raise")

    # V2 : reconnaître le nouveau format avant de traiter les vrais manques.
    # La convention 1024 Ko pour 1 Mo vient du kit et doit être validée hors TP.
    if nouvelle_sonde:
        if df[["octets_sortants_mo", "octets_sortants_ko"]].notna().all(axis=1).any():
            raise ValueError("Deux mesures présentes : cohérence des unités à contrôler")
        df["octets_sortants_mo"] = df["octets_sortants_mo"].fillna(
            df["octets_sortants_ko"] / 1024
        )
    manques = df["octets_sortants_mo"].isna()
    print(f"{chemin.name} : {len(df)} brutes ; {int(manques.sum())} sans volume après conversion")
    if manques.mean() > seuil_manques:
        raise ValueError("Couverture insuffisante : arrêt avant prédiction")
    # Même choix qu'au J3 : pas d'imputation artificielle, mais une exclusion tracée.
    exclus = df.loc[manques].copy()
    df = df.loc[~manques].copy()
    df["externe"] = (df["origine"] == "externe").astype(int)
    return df, exclus


def mesurer(nom, y, prediction):
    tn, fp, fn, tp = confusion_matrix(y, prediction, labels=[0, 1]).ravel()
    print(f"\n{nom} : VN={tn} FP={fp} FN={fn} VP={tp}")
    print(classification_report(y, prediction, labels=[0, 1],
                                target_names=["normal", "attaque"], digits=4, zero_division=0))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--septembre", type=Path, default=DOSSIER / "hexalp_ssh_sept2026.csv")
    p.add_argument("--octobre", type=Path, default=DOSSIER / "hexalp_ssh_oct2026.csv")
    p.add_argument("--sortie", type=Path, default=DOSSIER / "alertes_octobre.csv")
    p.add_argument("--taux-manquants-max", type=float, default=0.10,
                   help="Seuil pédagogique d'arrêt, à valider avant exploitation (défaut 10 %%)")
    args = p.parse_args()
    if not 0 <= args.taux_manquants_max <= 1:
        p.error("Le seuil de manques doit être entre 0 et 1")
    if args.sortie.resolve() in {args.septembre.resolve(), args.octobre.resolve()}:
        p.error("La sortie ne doit pas écraser une entrée")
    print(f"Graine={GRAINE}, profondeur={PROFONDEUR_ARBRE}, contamination={CONTAMINATION}")
    septembre, exclus_s = preparer(args.septembre, False, args.taux_manquants_max)
    octobre, exclus_o = preparer(args.octobre, True, args.taux_manquants_max)
    if septembre["date"].max() >= octobre["date"].min():
        raise ValueError("Les périodes d'entraînement et d'évaluation se chevauchent")

    # V2 : seule la période passée entre dans fit. Les étiquettes d'octobre
    # n'interviennent jamais dans l'ajustement ou le réglage des modèles.
    X_s = septembre[CARACTERISTIQUES]
    y_s = (septembre["etiquette"] == "attaque").astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X_s, y_s, test_size=0.3, stratify=y_s, random_state=GRAINE,
    )
    arbre = DecisionTreeClassifier(max_depth=PROFONDEUR_ARBRE, random_state=GRAINE)
    arbre.fit(X_train, y_train)
    iforest = IsolationForest(contamination=CONTAMINATION, random_state=GRAINE)
    iforest.fit(X_s)
    print(export_text(arbre, feature_names=CARACTERISTIQUES))
    mesurer("Arbre, contrôle septembre", y_test, arbre.predict(X_test))

    # Prédire sur la période suivante, sans lui fournir ses réponses de référence.
    X_o = octobre[CARACTERISTIQUES]
    octobre["avis_arbre"] = arbre.predict(X_o)
    octobre["score_anomalie"] = iforest.decision_function(X_o)
    octobre["anomalie"] = iforest.predict(X_o) == -1
    octobre["alerte"] = (octobre["avis_arbre"] == 1) | octobre["anomalie"]
    octobre["modeles_declencheurs"] = np.select(
        [(octobre["avis_arbre"] == 1) & octobre["anomalie"], octobre["avis_arbre"] == 1],
        ["arbre+isolation_forest", "arbre"], default="isolation_forest",
    )
    if "etiquette" in octobre:
        y_o = (octobre["etiquette"] == "attaque").astype(int)
        for nom, colonne in [("Arbre octobre", "avis_arbre"), ("Isolation Forest octobre", "anomalie"),
                              ("Union octobre", "alerte"), ("fail2ban historique", "fail2ban_ban")]:
            mesurer(nom, y_o, octobre[colonne].astype(int))
    else:
        print("Octobre sans étiquettes : pas d'évaluation, les avis restent à qualifier")

    # Export sans les étiquettes : la file d'exploitation n'a pas besoin de la réponse.
    # Le modèle déclencheur est explicite ; un score faible classe en tête sans prouver une attaque.
    colonnes = ["date", "heure", "ip_source", "origine", "echecs_auth", "succes_auth",
                "comptes_distincts", "duree_session_min", "octets_sortants_mo", "avis_arbre",
                "anomalie", "score_anomalie", "modeles_declencheurs"]
    alertes = octobre.loc[octobre["alerte"]].sort_values(
        ["score_anomalie", "date", "heure", "ip_source"], kind="stable",
    )
    alertes[colonnes].to_csv(args.sortie, index=False)
    semaines = pd.to_datetime(octobre["date"]).dt.to_period("W-SUN").astype(str)
    print("\nAlertes par semaine :")
    compte = octobre.groupby(semaines)["alerte"].sum()
    print(compte.to_string())
    print(f"{len(alertes)} alertes écrites dans {args.sortie.name}")
    if (compte > 30).any():
        print("BUDGET DÉPASSÉ : 30 alertes/semaine ; arbitrage requis")
    print(f"Hors couverture : {len(exclus_s)} lignes septembre, {len(exclus_o)} octobre")
    print("Aucun blocage, aucune connexion externe : l'analyste décide")


if __name__ == "__main__":
    main()
