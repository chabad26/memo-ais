# Vérification du script J3 — 21 octobre 2026

Exécutions effectuées par l’assistant, sur le kit fictif, dans un venv temporaire distinct de la VM apprenant.

- Python : 3.14.4 ; système : Linux / x86_64.
- pandas 3.0.6 ; scikit-learn 1.9.1 ; matplotlib 3.11.2 ; JupyterLab 4.6.4.
- NumPy 2.5.4 ; SciPy 1.18.1. Dépendances complètes : dependances_verification.txt.
- pip check : No broken requirements found.

## Protocole et résultats

1. Installation du requirements du kit dans un venv temporaire, sans modification du fichier.
2. Exécution du script à graine 42 ; export copié en référence temporaire.
3. Deuxième exécution à graine 42 : console et CSV identiques octet par octet.
4. Exécution à graine 7 avec un autre chemin de sortie ; CSV final à 42 préservé.
5. Lecture de l’export et comptages des observations par période ; pas de blocage, planification ou serveur lancé.

- Graine 42 : arbre test VN453 FP0 FN4 VP28 ; IF VN1501 FP5 FN64 VP44.
- Union descriptive sur tout X : VN1501 FP5 FN2 VP106 ; 111 alertes, 45 puis 66 par semaine.
- Graine 7 : arbre test VN453 FP0 FN4 VP28 (règles et partage différents) ; IF VN1502 FP4 FN63 VP45.
- Union graine 7 : 108 alertes, 44 puis 64 ; 107 observations communes avec graine42, 4 propres à42 et 1 propre à7.
- IF seules graine42 : 20 puis 29 alertes/semaine.
- Limites : IF ajusté sur les données évaluées ; union inclut les données d’entraînement de l’arbre ; pas un test de généralisation.

## Empreintes SHA-256

- `detection_ssh.py` : `90b8f9f9ded91056983e61c82b7594191ffbb0dd01a6cafbe00a9568f53a20a2`
- `hexalp_ssh_sept2026.csv` : `8f9565ee5b5b9e1d034cd6171d9e68ac3a7307af0f64b3ccda096e0badb1c126`
- `requirements.txt` : `1aeb643d57b014b2fb693179d02ad0dc5fada6306958d62379d99e9a10739d34`
- `alertes_a_qualifier.csv` : `3bb985d4cfb64d31c204404d4300f7c8cb8eb47b2c0979ed5c28d4a438a24b40`
