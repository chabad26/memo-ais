# Livrable formateur — Matrice d’applicabilité NIS2

- [PDF — Olivier HIMBLOT](Matrice-applicabilite-NIS2-Olivier-HIMBLOT.pdf) : 14 pages A4 paysage, version documentaire du 15 octobre 2026.
- [Source textuelle](Matrice-applicabilite-NIS2-Olivier-HIMBLOT.md).
- [Générateur ReportLab](generer_matrice_nis2.py).

Le PDF examine les articles 1 à 46 de la directive, détaille les contrôles proposés, reprend les cinq actifs et les trois prestataires du scénario, puis formalise quatre procédures de gestion des tiers. Les faits du dossier sont distingués des configurations cibles, des tests attendus et des preuves non recueillies. Aucun déploiement ni audit réel n’est attesté.

Pour régénérer : installer ReportLab dans un environnement Python isolé, puis exécuter `python generer_matrice_nis2.py`. Les polices DejaVu Sans sont attendues dans `/usr/share/fonts/truetype/dejavu/`.

Validation effectuée : métadonnées et pagination par `pdfinfo`, extraction du texte par `pdftotext`, contrôle visuel des tableaux techniques et du plan de preuve par `pdftoppm`, puis `git diff --check`.
