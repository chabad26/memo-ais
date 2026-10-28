# Livrables J3 — Analyse IT/OT Montval

- `J3-analyse-exigences-architecture-IT-OT.md` : source du dossier unique C3, consolidée à partir des fiches 3.1 à 3.6.
- `generer_dossier_j3.py` : génération du PDF formateur depuis cette source, sans exécuter de test ou d’intervention.
- `generer_schema_purdue_montval.py` et `generer_architecture_montval.py` : schémas SVG et draw.io.

PDF : `docs/assets/files/informatique-industrielle/it-2/J3-analyse-exigences-architecture-IT-OT-Olivier-HIMBLOT.pdf` (12 pages, deux schémas A3 et dix pages A4 paysage). Fiche d’activité distincte : `docs/informatique-industrielle/it-2/finaliser-dossier-analyse-it-ot.md`.

Depuis la racine du dépôt, avec Python et dépendances `reportlab`, `svglib`, `markdown`, `beautifulsoup4`, et polices Lato installées :

```bash
python3 livrables/informatique-industrielle/it-2/generer_schema_purdue_montval.py
python3 livrables/informatique-industrielle/it-2/generer_architecture_montval.py
python3 livrables/informatique-industrielle/it-2/generer_dossier_j3.py
```

Les données et décisions restent documentaires/proposées. Mettre à jour la source du dossier si les fiches évoluent, puis régénérer et vérifier le PDF. Les marqueurs `page:A4L`, `page:A3P`, `page:A3L` contrôlent les changements de format.
