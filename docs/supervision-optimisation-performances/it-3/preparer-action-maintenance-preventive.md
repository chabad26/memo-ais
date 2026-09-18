# Préparer une action de maintenance préventive

## Objectif

Reprendre le goulet d'étranglement ou la tendance analysée précédemment et préparer une intervention avant qu'une dégradation ne devienne un incident. La décision doit relier :

**Tendance observée → Goulet d'étranglement → Risque futur → Action préventive → Indicateur de suivi**

Le scénario 17 sert ici de cas pédagogique : il montre une hausse de la durée d'écriture, mais ne prouve pas que le disque réel est saturé. Une action de production doit donc être déclenchée par des mesures réelles et répétées.

## 1. Situation reprise

| Élément observé | Période étudiée | Évolution constatée | Situation | Risque potentiel |
| --- | --- | --- | --- | --- |
| Durée de l'opération d'écriture du scénario 17 | Avant, pendant et après l'activation de `17-disque.active`, avec plusieurs scrapes Prometheus à 5 s | Passage attendu de `0,03 s` à `3,2 s`, puis retour vers `0,03 s` après désactivation ; la reproductibilité hors scénario reste à vérifier. | Dégradation simulée et réversible ; tendance réelle non démontrée. | Si une latence réelle se répétait, elle pourrait provoquer des files d'attente, des erreurs d'écriture, une hausse de latence applicative puis une indisponibilité. |
| Capacité du stockage réel | À relever sur plusieurs jours, avec heures et fuseau | Aucune consommation réelle démontrée par le scénario 17 ; compléter avec espace libre, inodes et vitesse de croissance. | Surveillance particulière : données nécessaires à la décision encore incomplètes. | Saturation progressive, journaux impossibles à écrire et perte de fonctionnement de services dépendants. |

## 2. Décider avant le seuil critique

Une maintenance préventive n'attend pas nécessairement le dépassement d'un seuil critique. Elle peut être déclenchée par une tendance suffisamment établie, une marge qui diminue, une récidive ou une échéance estimée avant saturation.

Pour le stockage réel, retenir temporairement les niveaux de vigilance suivants, à ajuster selon les besoins du service :

| Niveau | Condition indicative | Décision |
| --- | --- | --- |
| Normal | espace libre stable, absence d'erreur et durée d'écriture dans la baseline | Continuer la collecte et la revue prévue. |
| Vigilance | occupation supérieure à 75 %, croissance confirmée ou durée d'écriture au-dessus de la baseline sur plusieurs mesures | Identifier les producteurs, vérifier la rétention et préparer l'action. |
| Préparation obligatoire | occupation supérieure à 85 %, marge qui diminue rapidement ou latence répétée avec impact | Planifier la maintenance, vérifier sauvegardes et retour arrière. |
| Critique | écritures en erreur, service impacté ou capacité proche de l'épuisement | Traiter l'incident et appliquer la procédure d'escalade ; la prévention n'a pas été engagée assez tôt. |

Ces pourcentages sont des repères de travail, pas une preuve de seuil adapté à tous les volumes. Compléter avec les octets libres, les inodes, la vitesse de croissance et le délai nécessaire à l'intervention.

## 3. Plan de maintenance préventive

| Élément à définir | Décision proposée |
| --- | --- |
| Indicateur à surveiller | `node_filesystem_avail_bytes` pour `/`, `windows_logical_disk_free_bytes` pour `C:`, taux de croissance de l'espace utilisé, inodes Linux et `lab_storage_operation_duration_seconds` pour le test de performance. |
| Seuil ou niveau de vigilance | Déclencher une revue à 75 % d'occupation ou dès qu'une durée dépasse durablement la baseline ; préparer l'action à 85 %, après confirmation sur plusieurs points. |
| Fréquence d'analyse | Collecte toutes les 30 s pour l'état courant ; revue quotidienne pour une croissance rapide et revue hebdomadaire pour la capacité, à adapter au rythme des journaux. |
| Responsable | Administrateur système pour le volume et la rotation ; équipe supervision pour les métriques et alertes ; propriétaire applicatif si l'opération lente concerne une application. |
| Action à réaliser | Mesurer la croissance, identifier les fichiers ou journaux responsables, vérifier la rotation et la rétention, puis supprimer/déplacer selon la procédure ou étendre le volume après validation. Ne rien supprimer au hasard. |
| Retour arrière | Restaurer la configuration de rotation ou de rétention précédente ; restaurer les données depuis la sauvegarde si une opération de déplacement l'exige ; annuler l'extension uniquement selon la procédure du stockage. |
| Vérification d'efficacité | Espace libre revenu dans la marge, croissance ralentie, écritures fonctionnelles, durée dans la baseline, service et sondes nominaux, absence de nouvelles erreurs et stabilité observée. |

## 4. Préparer l'intervention

Avant la fenêtre de maintenance :

- confirmer la tendance sur une période adaptée et vérifier qu'elle n'est pas due à un trou de collecte ;
- identifier le volume, le propriétaire des données et le service impactable ;
- vérifier les sauvegardes et la possibilité de restauration ;
- mesurer l'espace libre, les inodes, la croissance et la durée des opérations ;
- définir la limite d'arrêt et le retour arrière ;
- informer les responsables et obtenir la validation du changement ;
- conserver les configurations avant modification.

Pendant l'intervention :

- agir sur le périmètre minimal ;
- conserver les journaux et l'heure de chaque action ;
- vérifier que les écritures, le service et la collecte restent opérationnels ;
- arrêter l'opération si le risque ou l'impact dépasse le prévu.

Après l'intervention :

- refaire exactement les mêmes mesures qu'avant ;
- vérifier `up`, `probe_success` et `probe_duration_seconds` lorsque le service possède une sonde ;
- vérifier les journaux et l'absence de nouvelles erreurs ;
- observer plusieurs collectes puis confirmer la stabilité ;
- noter le résultat réel, les écarts et la prochaine date de revue.

## 5. Vérifier l'efficacité

| Indicateur | Avant action | Après action | Critère de réussite |
| --- | --- | --- | --- |
| Espace libre du volume |  |  | marge suffisante et croissance maîtrisée |
| Inodes Linux |  |  | aucune saturation d'inodes |
| Durée d'écriture |  |  | retour dans la baseline hors scénario |
| Erreurs d'écriture |  |  | aucune nouvelle erreur pertinente |
| Service rendu |  |  | fonctionnalité et statut HTTP attendus |
| Sondes |  |  | `probe_success=1`, `up=1`, durée stable |
| Journaux |  |  | collecte fraîche et absence d'erreurs liées |
| Stabilité |  |  | état maintenu pendant la période définie |

Une baisse immédiate de l'indicateur ne suffit pas si la croissance reprend ou si le service reste dégradé. Comparer des périodes équivalentes et documenter les limites de la mesure.

## 6. Répondre aux questions

### Une maintenance préventive doit-elle attendre le dépassement d'un seuil critique ?

Non. Elle doit intervenir lorsque le risque est suffisamment établi et qu'une action peut encore être planifiée sans urgence. Le seuil critique sert à l'escalade ou à l'incident, pas à définir le seul moment possible d'action.

### Comment déterminer qu'une tendance justifie une intervention ?

Vérifier plusieurs points, une direction ou répétition, une capacité qui diminue, un impact possible et une action proportionnée. Plus l'échéance estimée est courte et l'action longue à préparer, plus la priorité augmente.

### Quelle différence entre action corrective et action préventive ?

Une action corrective rétablit un service déjà dégradé ou interrompu. Une action préventive traite une tendance ou un risque avant l'incident, par exemple corriger la rotation des journaux avant la saturation du volume.

### Comment prioriser plusieurs actions préventives ?

Classer les actions selon l'impact potentiel, la probabilité, le délai avant conséquence, la facilité de retour arrière et les dépendances. Prioriser une perte de visibilité ou une saturation proche avant une optimisation de confort.

### Quelles données vérifient l'efficacité ?

Les mêmes indicateurs qu'avant l'action : espace libre, vitesse de croissance, inodes, durée d'opération, erreurs, service, sonde, collecte et stabilité. Une preuve efficace compare avant/après et indique la période observée.

## 7. Transition vers un dispositif durable

Pour transformer cette analyse en exploitation durable :

- conserver une baseline par ressource et par service ;
- afficher la tendance, la capacité restante et la fraîcheur dans les dashboards ;
- créer des alertes graduées avec une durée et une procédure associée ;
- relier chaque alerte à un responsable, une action et un retour arrière ;
- maintenir un registre des actions préventives et des prochaines revues ;
- rejouer régulièrement les contrôles et mettre à jour le dossier après chaque incident ;
- distinguer dans les rapports les résultats réalisés, proposés, non testés et non démontrés.

## Livrable L4 — enrichissement

Ajouter au rapport de diagnostic et d'analyse de performance :

```text
Tendance observée :
Goulet d'étranglement :
Risque futur :
Action préventive :
Indicateur de suivi :
Période et preuves :
Hypothèses écartées :
Niveau de confiance :
Limites :
```

Le rapport doit joindre les requêtes, périodes, captures ou exports, corrélations, hypothèses, décisions, responsables, seuils, contrôles avant/après et prochaine date de revue. Le scénario 17 peut illustrer la méthode, mais ne doit pas être présenté comme une saturation réelle du disque.

## Auto-évaluation

- [ ] Identifier une tendance à partir de données d'observabilité.
- [ ] Distinguer une variation ponctuelle d'une dégradation progressive.
- [ ] Analyser plusieurs indicateurs en les mettant en relation.
- [ ] Identifier un goulet d'étranglement.
- [ ] Formuler une hypothèse sur l'évolution future.
- [ ] Identifier le risque lié à cette évolution.
- [ ] Proposer une action de maintenance préventive.
- [ ] Justifier la priorité de cette action.
- [ ] Définir les indicateurs de suivi de son efficacité.
- [ ] Argumenter l'analyse avec des données observées.

Ne demander la validation que lorsque chaque case peut être expliquée et illustrée par une preuve ou une limite clairement formulée.

## Validation par le formateur

Être capable de présenter la tendance ou la dégradation, les données utilisées, le goulet ou facteur limitant, les hypothèses examinées, le risque futur, l'action préventive, sa priorité et les indicateurs de vérification.

[Analyser un goulet d'étranglement](analyser-goulet-etranglement.md) · [Préparer la maintenance préventive](preparer-maintenance-preventive.md) · [Retour au sommaire](index.md)
