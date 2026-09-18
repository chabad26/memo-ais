# Préparer la maintenance préventive

## Principe

Une maintenance préventive intervient avant l'incident, à partir d'une dégradation ou d'un risque documenté. Elle ne consiste pas à appliquer automatiquement une correction dès qu'un indicateur dépasse une valeur.

La recommandation doit relier : **Observation → Risque → Échéance ou condition → Action → Vérification**.

## Registre des actions

| Observation | Risque | Échéance ou condition | Action préparée | Responsable | Retour arrière | Vérification |
| --- | --- | --- | --- | --- | --- | --- |
| Espace libre en baisse régulière | saturation et échec d'écriture | avant la marge minimale ou à la date estimée | vérifier rétention, rotation, extension ou déplacement | système / propriétaire des données | restaurer configuration précédente | espace, écritures, journaux, tendance |
| Durée HTTP en hausse | dégradation visible avant panne | plusieurs points au-dessus de la baseline | rechercher dépendance, charge et logs applicatifs | applicatif / système | annuler changement identifié | statut, durée, `probe_success`, stabilité |
| CPU élevé à horaires récurrents | ralentissement ou contention | avant la prochaine fenêtre récurrente | déplacer, limiter ou replanifier la tâche | propriétaire de la tâche | rétablir planification | CPU, service, absence d'erreur |
| Mémoire disponible en baisse | swap, OOM ou instabilité | seuil de marge atteint sur période confirmée | identifier consommateur, corriger fuite ou dimensionner | système / applicatif | arrêter le changement ou restaurer | mémoire, processus, journaux |
| Perte intermittente de collecte | diagnostic impossible au prochain incident | récidive ou trous dépassant la durée acceptée | vérifier réseau, exporter, Blackbox et rétention | supervision / réseau | remettre configuration précédente | `up`, fraîcheur et absence de trous |

## Fiche d'une action

Avant intervention, renseigner :

- l'observation, sa source, sa période et son niveau de confiance ;
- le risque évité et le service concerné ;
- la condition de déclenchement et l'échéance estimée ;
- l'action minimale, son périmètre et sa fenêtre ;
- les prérequis, sauvegardes, responsable et validation ;
- le retour arrière et le critère d'arrêt ;
- les contrôles avant, pendant et après ;
- le résultat réel et la prochaine date de revue.

## Exemple de raisonnement capacité disque

Une baisse de l'espace disponible n'est pas encore une saturation. Relever plusieurs points, calculer une vitesse sur une période représentative, vérifier la rétention et rechercher les pics. Si l'estimation est fiable, planifier la correction avant la marge minimale. Si la croissance est irrégulière ou les données insuffisantes, produire d'abord une amélioration de collecte ou une revue plus fréquente.

Ne jamais remplir volontairement le disque du laboratoire pour provoquer une alerte. Utiliser un test isolé ou des séries synthétiques pour valider la logique, puis contrôler séparément le comportement réel de la chaîne de supervision.

## Validation et retour d'expérience

Après l'action, vérifier le service fonctionnel, les métriques fraîches, les sondes, les journaux, l'absence d'effet de bord et la stabilité sur une période adaptée. Comparer avant/après avec les mêmes unités. Si l'objectif n'est pas atteint, conserver le résultat et requalifier l'hypothèse plutôt que déclarer la maintenance réussie.

[Formaliser le dossier d'exploitation](formaliser-dossier-exploitation.md) · [Retour au sommaire](index.md)
