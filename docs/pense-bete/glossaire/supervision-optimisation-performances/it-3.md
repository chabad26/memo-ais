# Pense-bête — Itération 3 : optimiser et formaliser l'exploitation

## Périmètre

Cette itération exploite les observations des incidents pour améliorer la supervision, anticiper les dégradations et préparer la maintenance préventive.

- [Mise en situation](../../../supervision-optimisation-performances/it-3/optimiser-formaliser-exploitation.md)
- [Analyser les tendances et la capacité](../../../supervision-optimisation-performances/it-3/analyser-tendances-capacite.md)
- [Améliorer le dispositif de supervision](../../../supervision-optimisation-performances/it-3/ameliorer-dispositif-supervision.md)
- [Préparer la maintenance préventive](../../../supervision-optimisation-performances/it-3/preparer-maintenance-preventive.md)
- [Formaliser le dossier d'exploitation](../../../supervision-optimisation-performances/it-3/formaliser-dossier-exploitation.md)
- [Pense-bête de l'itération 2](it-2.md)

## Termes à retenir

| Terme | Sens pour l'exploitation |
| --- | --- |
| Tendance | Évolution régulière ou significative d'un indicateur dans le temps. |
| Baseline | Comportement de référence servant à comparer une situation observée. |
| Capacité | Ressource encore disponible pour absorber une charge ou une croissance. |
| Goulet d'étranglement | Élément qui limite la performance globale d'un service ou d'une chaîne. |
| Marge | Écart disponible avant une limite de capacité ou une condition d'action. |
| Fraîcheur | Âge de la dernière donnée exploitable ; une donnée absente n'est pas une valeur nulle. |
| Rétention | Durée pendant laquelle les métriques ou journaux restent consultables. |
| Maintenance préventive | Intervention préparée avant l'incident, à partir d'un risque ou d'une dégradation. |
| Échéance estimée | Date ou délai calculé à partir d'une évolution et d'hypothèses explicites. |
| Retour arrière | Action préparée pour annuler une modification si le résultat ou le risque n'est pas acceptable. |
| Capacité restante | Quantité disponible avant une limite ; elle doit être exprimée avec une unité et une période. |

## Méthode de décision

Toujours relier : **Observation → Risque → Échéance ou condition → Action → Vérification**.

- Une capture ponctuelle décrit un état, pas une tendance.
- Vérifier la période, le nombre de points, la fréquence et les trous de collecte.
- Comparer la cible à une référence ou à une cible témoin.
- Relier les métriques aux sondes, journaux et effets sur le service.
- Ne pas désigner le goulet à partir du seul pourcentage le plus élevé.
- Si la vitesse de croissance est inconnue ou irrégulière, écrire « échéance non estimable » et améliorer d'abord la collecte.
- Distinguer observation, interprétation, hypothèse, décision et preuve.

## Requêtes de départ

Adapter les labels et les unités aux séries réellement présentes :

```promql
node_filesystem_avail_bytes{mountpoint="/",fstype!="tmpfs"}
```

```promql
windows_logical_disk_free_bytes{volume="C:"}
```

```promql
probe_duration_seconds{job=~"sonde_.*"}
```

```promql
up{job=~"linux|windows|sonde_.*"}
```

Pour les compteurs, utiliser un taux ou une augmentation sur une fenêtre cohérente. Conserver la requête, la période, la cible et le fuseau dans le dossier.

## Revue de supervision

- La collecte est-elle fraîche, régulière et conservée assez longtemps ?
- Le dashboard répond-il à une question d'exploitation avec une unité et une période lisibles ?
- L'alerte distingue-t-elle perte de collecte, échec fonctionnel et dégradation de performance ?
- Le seuil tient-il compte de la durée, de l'impact et de la capacité restante ?
- La procédure indique-t-elle une première action, une escalade et un critère de retour ?
- Les notifications `firing` et `resolved` ont-elles été testées ?

## Registre de maintenance

Pour chaque action, noter l'observation, la source, le risque, l'échéance ou condition, le responsable, la fenêtre, le retour arrière, les contrôles avant/après et la prochaine revue. Ne pas tester une saturation en remplissant le disque réel du laboratoire ; utiliser des séries synthétiques pour la logique.

## Preuves et limites

Un résultat doit être classé : réalisé, proposé, testé partiellement, non testé ou non démontré. Masquer les secrets et ne conserver que les événements utiles. Après une action, vérifier service fonctionnel, données fraîches, sondes, journaux, alertes et stabilité sur une période adaptée.
