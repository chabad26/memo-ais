# Livrable formateur — Matrice d’applicabilité NIS2

- [PDF — Olivier HIMBLOT](Matrice-applicabilite-NIS2-Olivier-HIMBLOT.pdf) : 30 pages A4 paysage, version 3 documentaire — base ReCyF du 15 octobre 2026.
- [Source textuelle](Matrice-applicabilite-NIS2-Olivier-HIMBLOT.md).
- [Générateur ReportLab](generer_matrice_nis2.py).

Le PDF repose sur les vingt objectifs du ReCyF v2.5 du 17/03/2026, document de travail, avec une sélection de MAC identifiés, leur contrôle et les preuves attendues. Il examine les articles 1 à 46 de la directive en annexe juridique, détaille les contrôles proposés, reprend les cinq actifs et les trois prestataires du scénario, puis formalise quatre procédures de gestion des tiers. La V2 ajoute l’analyse Cloud Act, cinq scénarios de risque, une comparaison des offres, une orientation conditionnelle de maintien/migration, la politique en onze rubriques et une grille de revue croisée. Les faits du dossier sont distingués des configurations cibles, des tests attendus et des preuves non recueillies. Aucun déploiement ni audit réel n’est attesté.

Pour régénérer : installer ReportLab dans un environnement Python isolé, puis exécuter `python generer_matrice_nis2.py`. Les polices DejaVu Sans sont attendues dans `/usr/share/fonts/truetype/dejavu/`.

Validation effectuée : métadonnées et pagination par `pdfinfo`, extraction du texte par `pdftotext`, contrôle visuel des tableaux techniques et du plan de preuve par `pdftoppm`, puis `git diff --check`.

## Synthèse de comparaison hyperscalers / cloud souverain

- [PDF distinct — Olivier HIMBLOT](Synthese-comparaison-hyperscalers-cloud-souverain-Olivier-HIMBLOT.pdf) : 9 pages A4 paysage, V2 documentaire — base ReCyF du 15 octobre 2026.
- [Source textuelle](Synthese-comparaison-hyperscalers-cloud-souverain-Olivier-HIMBLOT.md).
- [Générateur ReportLab](generer_synthese_cloud.py).

Compétence : **Contribuer à la conception d’une infrastructure sécurisée**. Comparaison qualitative des familles d’offres, cinq risques Cloud Act, options et cible proposées, plan de migration, recette et retour arrière. Les fournisseurs, prix et résultats de tests non fournis ne sont pas inventés. Aucune migration effective n’est attestée.

Régénération : `python generer_synthese_cloud.py` dans un environnement équipé de ReportLab et des polices DejaVu Sans. Vérification : `pdfinfo`, `pdftotext`, contrôle visuel `pdftoppm`, puis `git diff --check`.

## Correction du référentiel de l’exercice

La précision du formateur reçue le 15 octobre 2026 fait du **ReCyF le référentiel principal**. La matrice est en V3 et la synthèse cloud en V2 ; NIS2 demeure la correspondance juridique, SecNumCloud une qualification d’offre distincte.

- Source officielle : [ReCyF v2.5 du 17/03/2026](https://messervices.cyber.gouv.fr/documents-ressources/20260317_NIS_V2_ReCyF_v2.5.pdf), document de travail.
- [Données partagées des analyses ReCyF](recyf_energiealp.py) : vingt objectifs, sélection explicite de MAC, pages sources, écarts et contrôles proposés. Les identifiants ont été rapprochés du texte officiel ; l’analyse n’est pas présentée comme un audit unitaire exhaustif de tous les MAC.
- Le générateur de la matrice reprend les rubriques de politique de la feuille MkDocs ; conserver l’arborescence du dépôt pour régénérer. Les deux générateurs importent le module partagé ci-dessus.

Les MAC spécifiques EE sont conservés sous hypothèse de qualification EE. Les fréquences choisies localement restent distinguées des minima du référentiel. La divergence de rédaction entre l’objectif 20 (24 heures) et le MAC 20.1-EE (24h ouvrés) est signalée ; aucune interprétation officielle n’est revendiquée.
