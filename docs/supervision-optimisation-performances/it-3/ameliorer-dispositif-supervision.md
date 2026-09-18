# Améliorer le dispositif de supervision

## Objectif

Transformer les difficultés observées pendant les incidents en améliorations mesurables. Une amélioration doit préciser le problème, le changement proposé, le risque traité, la priorité et la preuve attendue.

## Bilan par composant

| Composant | Question de revue | Amélioration possible | Preuve attendue |
| --- | --- | --- | --- |
| Collecte L1 | Les données sont-elles présentes, fraîches et conservées assez longtemps ? | Mesurer le délai de scrape, documenter la rétention et alerter sur la perte de collecte. | Série récente, erreur de Target absente, durée documentée. |
| Dashboard L2 | Un opérateur voit-il état, évolution, capacité et impact ? | Ajouter période, unité, légende, cible témoin et panneau de fraîcheur. | Question d'exploitation répondue sans interprétation cachée. |
| Alertes L3 | Le signal est-il actionnable et non bruyant ? | Revoir seuil, `for`, criticité, annotations, maintenance et condition de résolution. | Test bref non déclenché, test soutenu déclenché puis `resolved`. |
| Diagnostic L4 | Les sources permettent-elles de distinguer symptôme et cause ? | Harmoniser fuseaux, labels et requêtes ; conserver une chronologie reproductible. | Rapport avec faits, hypothèses, vérifications et limites. |
| Exploitation | Un autre administrateur peut-il agir sans connaissance implicite ? | Lier chaque alerte à une procédure, un responsable et une action de retour arrière. | Fiche jouée par une autre personne et résultat consigné. |

## Tableau de priorisation

| Problème observé | Impact | Effort | Priorité | Décision et responsable |
| --- | --- | --- | --- | --- |
|  | faible / moyen / fort | faible / moyen / fort | P1 / P2 / P3 |  |

Prioriser les pertes de visibilité, les alertes qui n'aboutissent à aucune action et les indicateurs incapables de montrer une dégradation avant incident. Ne pas augmenter le nombre de panneaux ou d'alertes sans usage opérationnel identifié.

## Contrôles à prévoir

- Vérifier qu'une cible `up=1` n'est pas interprétée comme un service fonctionnel : confronter avec `probe_success` lorsque la sonde existe.
- Afficher l'âge de la dernière donnée ou une alerte de fraîcheur ; une interface accessible ne prouve pas une collecte actuelle.
- Distinguer une absence de série d'une valeur nulle dans les panneaux et les procédures.
- Utiliser des seuils reliés à l'impact, à la durée et à la capacité restante, pas à un pourcentage isolé.
- Tester les notifications `firing` et `resolved`, y compris après une maintenance planifiée.
- Conserver une cible témoin et des marqueurs de test non secrets pour rejouer les contrôles.

## Critères d'acceptation d'une amélioration

Une amélioration est retenue seulement si elle est compréhensible par un autre opérateur, vérifiable sur les données réelles, réversible et documentée. Après modification, comparer avant/après sur la même période ou rejouer un scénario contrôlé. Indiquer ce qui reste non testé.

[Formaliser le dossier d'exploitation](formaliser-dossier-exploitation.md) · [Retour au sommaire](index.md)
