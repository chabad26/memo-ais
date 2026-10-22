# Remise J4 — Olivier HIMBLOT

Compétence : évaluer les performances et limites d’un modèle de détection d’anomalies.
Données Hexalp fictives ; travaux rédigés/exécutés avec assistance, 22 octobre 2026.

## Lire

- Evaluation-modele-SSH-Hexalp-Olivier-HIMBLOT.pdf : dossier de 13 pages ; rapport d’évaluation limité à trois pages (pages2–4), annexes de preuve séparées.
- ia01-j4/rapport_evaluation.md : rapport source complet ; carnet_J4.md : réponses4.1–4.8.
- conditions_exploitation_48.md : chaîne, conditions et cinq questions à l’éditeur.

## Exécuter

Depuis ia01-j4, dans l’environnement isolé du J3 avec les dépendances fournies :

```bash
python detection_ssh_v2.py --sortie alertes_octobre_rejeu.csv
```

Ne pas écraser l’export de référence ; les CSV septembre et octobre sont inclus pour reproduire. Le script n’agit pas sur le SI et ne se connecte à aucun fournisseur.

## Preuves

- detection_ssh_v2.py, requirements.txt, alertes_octobre.csv (239 alertes).
- Notebooks03 et04 complétés et exécutés localement hors VM ; sources originales conservées dans sources_notebooks/.
- preuves/ : sorties et vérifications locales, comparaisons et simulations ; captures/ : captures fournies par l’apprenant.
- 04 utilise le modèle fourni en inférence seule. Référence du PDF du cours4.7 : 01464c560c949742a4b832c1b615194971ce56e29c93f39fd98bda3169e38b00. Vérifier avant tout chargement ; une concordance ne prouve pas l’innocuité ni la qualité.
- MANIFESTE_SHA256.txt permet de vérifier le contenu de la remise ; ce manifeste local n’est pas une signature du producteur du modèle.

## Portée

V2 figée : graine42, profondeur3, contamination0,03 ; corpus septembre seulement. Le kit pédagogique des notebooks utilise médiane/0,05 : les résultats sont distingués. Les autoencodeur/script/données sont inchangés par les simulations. Les captures attestent les sorties visibles, pas l’identité de tous les fichiers de la VM ou deux relances V2 identiques dans celle-ci. Les tests locaux de répétabilité sont conservés séparément.

Avis final : pas de mise en service générale ; pilote supervisé proposé pendant quatre semaines, sous conditions. Responsabilités, cibles, enrichissements et intégrations restent proposés, non approuvés ni déployés. Aucun envoi au formateur n’a été réalisé.
