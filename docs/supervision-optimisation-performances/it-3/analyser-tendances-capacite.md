# Analyser les tendances et la capacité

## Objectif

Passer d'une valeur observée à une évolution interprétable. L'analyse doit répondre à deux questions : « que se passe-t-il dans le temps ? » et « quand cette évolution risque-t-elle de devenir problématique ? »

## Méthode

1. Définir l'indicateur, la cible, l'unité et la question d'exploitation.
2. Choisir une période cohérente avec le phénomène : heures pour une charge, jours ou semaines pour un disque.
3. Vérifier la fraîcheur, la fréquence et les trous de collecte.
4. Comparer la cible à son historique et, si possible, à une cible témoin.
5. Qualifier la forme : stable, hausse, baisse, saisonnière, cyclique, brutale ou intermittente.
6. Relier l'indicateur à l'état du service, aux sondes et aux journaux.
7. Estimer une capacité restante et une condition d'action.

## Tableau d'analyse

| Ressource ou service | Indicateur | Période et fréquence | Observation | Risque | Capacité ou échéance | Donnée à compléter |
| --- | --- | --- | --- | --- | --- | --- |
| Debian | espace disponible `/` | à relever | N/A | saturation ou échec d'écriture | calculer selon la croissance | points historiques |
| Windows | espace libre `C:` | à relever | N/A | journaux ou service bloqués | calculer selon la croissance | octets libres et événements |
| Endpoint | CPU et mémoire disponibles | à relever | N/A | ralentissement ou pression mémoire | comparer aux charges prévues | processus et latence |
| Service HTTP | durée et succès de sonde | à relever | N/A | dégradation avant indisponibilité | définir une limite de performance | journaux applicatifs |
| Collecte | `up`, âge du dernier point | à relever | N/A | perte de visibilité | agir avant absence durable | erreur Target et fréquence |

## Estimer une échéance

Pour une ressource qui diminue, calculer une vitesse moyenne sur une période comparable :

```text
vitesse de consommation = (valeur initiale - valeur finale) / durée
temps restant = capacité disponible / vitesse de consommation
```

Préciser l'unité et les hypothèses. Une croissance irrégulière, une rétention modifiée ou une période trop courte rendent l'estimation fragile. Donner une fourchette ou « non estimable » si les données ne permettent pas un calcul défendable.

## PromQL de départ

Les requêtes sont à adapter aux labels réellement présents dans la plateforme :

```promql
node_filesystem_avail_bytes{mountpoint="/",fstype!="tmpfs"}
```

```promql
windows_logical_disk_free_bytes{volume="C:"}
```

```promql
100 * (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)
```

```promql
probe_duration_seconds{job=~"sonde_.*"}
```

```promql
up{job=~"linux|windows|sonde_.*"}
```

Pour un compteur, préférer un taux ou une augmentation sur une fenêtre adaptée. Pour une valeur instantanée, ne pas parler de tendance sans plusieurs points. Conserver la requête exacte et le moment de consultation.

## Rechercher un goulet d'étranglement

Ne pas conclure à partir du seul indicateur le plus élevé. Examiner la chaîne : ressource → composant → service → expérience utilisateur. Par exemple, un CPU élevé peut accompagner une latence sans en être la cause ; une mémoire disponible faible peut provoquer du swap ; un disque presque plein peut perturber les journaux et le service.

| Question | Vérification discriminante |
| --- | --- |
| La dégradation touche-t-elle une seule cible ? | Comparer une cible témoin et les labels. |
| La collecte fonctionne-t-elle ? | `up`, fraîcheur des points et erreur Target. |
| Le service est-il réellement lent ou indisponible ? | `probe_success`, durée, statut HTTP et test fonctionnel. |
| Une ressource évolue-t-elle avant le symptôme ? | Superposer les séries sur la même plage et le même fuseau. |
| Le journal confirme-t-il l'hypothèse ? | Chercher l'événement proche du changement, sans confondre corrélation et causalité. |

## Conclusion attendue

Chaque analyse doit se terminer par une décision : poursuivre l'observation, créer ou ajuster une alerte, planifier une maintenance, augmenter la capacité, ou déclarer l'estimation non concluante. Une valeur élevée sans évolution ni impact ne suffit pas à déclencher une intervention.

[Préparer la maintenance préventive](preparer-maintenance-preventive.md) · [Retour au sommaire](index.md)
