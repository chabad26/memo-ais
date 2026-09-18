# Analyser un goulet d'étranglement

## Objectif

À partir de la dégradation sélectionnée dans l'activité précédente, rechercher ce qui limite réellement les performances de l'élément concerné. Une valeur élevée n'identifie pas automatiquement un goulet d'étranglement : il faut comparer plusieurs sources et reconstruire la chronologie.

Dans cette feuille, le cas de départ est la hausse du temps de réponse de l'opération d'écriture du scénario 17. Le scénario est simulé ; le diagnostic doit donc distinguer ce que les données démontrent de ce qu'elles ne permettent pas d'attribuer.

!!! note "Définition"
    Un goulet d'étranglement est un élément qui limite la performance globale d'un service ou d'une chaîne. Il peut être situé dans la ressource mesurée, une dépendance, le réseau, le service ou le dispositif de collecte.

## Travail demandé

À partir de la tendance ou de la dégradation sélectionnée :

1. reprendre la période avant, pendant et après la dégradation ;
2. comparer la ressource concernée aux autres ressources du même système ;
3. examiner les performances du service et les sondes associées ;
4. rechercher les événements pertinents dans les journaux ;
5. reconstruire la chronologie des évolutions ;
6. formuler plusieurs hypothèses et rechercher une donnée qui pourrait les contredire ;
7. identifier un goulet seulement si les données convergent suffisamment.

Ne pas conclure à partir du seul indicateur dont la valeur est la plus élevée. Vérifier également la fraîcheur de chaque donnée et distinguer une absence de mesure d'une valeur normale.

## 1. Préparer la comparaison

Reprendre la chronologie de la feuille [Analyser une dégradation de stockage](analyser-degradation-stockage.md). Les trois phases attendues sont :

| Phase | Événement à documenter | Heure | Source |
| --- | --- | --- | --- |
| Avant | état nominal de l'opération et des services |  | Prometheus / logs |
| Pendant | activation du scénario 17 et hausse de la durée |  | fichier d'état / métrique |
| Après | désactivation et retour de la durée |  | métrique / logs |

La collecte du simulateur est configurée toutes les 5 secondes. Les endpoints Linux, Windows et les sondes HTTP sont configurés toutes les 30 secondes. Tenir compte de cette différence avant de comparer les heures.

## 2. Indicateurs à consulter

| Domaine | Indicateur ou source | Question à poser |
| --- | --- | --- |
| Ressource concernée | `lab_storage_operation_duration_seconds{scenario="17"}` | La durée augmente-t-elle uniquement pendant le scénario ? |
| CPU | métriques Node Exporter ou Windows Exporter | Le processeur évolue-t-il avant ou pendant la latence ? |
| Mémoire | mémoire disponible, swap ou pression mémoire | Une pression mémoire peut-elle expliquer la lenteur ? |
| Stockage réel | espace libre, inodes, métriques disque disponibles | Le scénario mesure-t-il une capacité pleine ou seulement une latence simulée ? |
| Service | statut HTTP, fonctionnalité, durée de réponse | L'utilisateur ou le service voit-il une dégradation ? |
| Sonde | `probe_success`, `probe_duration_seconds`, `up` | Le contrôle fonctionnel confirme-t-il la dégradation ? |
| Réseau | erreurs, latence et disponibilité si disponibles | Le chemin réseau peut-il expliquer la durée ? |
| Journaux | logs Docker du simulateur et événements centralisés | Quel événement précède la hausse et confirme le scénario ? |
| Collecte | `up{job="lab_simulator"}` et âge du dernier point | La mesure est-elle fraîche et fiable ? |

Requêtes de départ :

```promql
lab_storage_operation_duration_seconds{scenario="17",operation="write"}
```

```promql
up{job="lab_simulator"}
```

```promql
probe_success{job=~"sonde_.*"}
```

```promql
probe_duration_seconds{job=~"sonde_.*"}
```

```promql
up{job=~"linux|windows"}
```

Adapter les requêtes aux labels réellement présents et conserver leur version exacte dans le dossier de preuve.

## Tableau à compléter

| Élément analysé | Indicateur observé | Évolution constatée | Autre donnée à corréler | Observation | Identification d'un goulet d'étranglement ? |
| --- | --- | --- | --- | --- | --- |
| Opération d'écriture simulée | `lab_storage_operation_duration_seconds` | `0,03 s` avant et après ; `3,2 s` pendant l'activation du scénario 17 | heure d'activation, logs du simulateur, `up` du job | La dégradation est synchronisée avec le scénario et réversible. | ☑ Oui ☐ Non |
| CPU du système observé | CPU Node Exporter ou Windows Exporter | À relever sur la même période | durée d'écriture et latence du service | Une hausse concordante pourrait soutenir l'hypothèse CPU ; son absence l'affaiblit. | ☐ Oui ☑ Non |
| Mémoire du système observé | mémoire disponible / swap | À relever sur la même période | durée d'écriture et événements OOM | Aucune cause mémoire ne doit être retenue sans pression mesurée. | ☐ Oui ☑ Non |
| Stockage réel | espace libre, inodes, métriques disque disponibles | À relever ; le scénario 17 ne remplit pas le disque | `df -h`, `df -i`, journaux et durée d'écriture | La capacité réelle n'est pas démontrée par la métrique simulée. | ☐ Oui ☑ Non |
| Service et sonde associée | `probe_success`, `probe_duration_seconds`, statut HTTP | À relever avant, pendant et après | durée d'écriture et journaux applicatifs | Une sonde stable indique que la lenteur simulée ne rend pas nécessairement le service indisponible. | ☐ Oui ☑ Non |
| Réseau | erreurs et latence réseau disponibles | À relever ; scénario 12 séparé | durée d'écriture et `up` | Une dégradation réseau doit être écartée ou confirmée sur la même période, pas supposée. | ☐ Oui ☐ Non |
| Journaux | logs Docker `lab-simulator` et journaux centralisés | événement lié au scénario 17, si présent | heure de la métrique et état du fichier | Le journal confirme le contexte du test, pas une panne de disque physique. | ☐ Oui ☐ Non |

Les cases cochées dans le tableau constituent un point de départ à confirmer par les mesures réellement prises. Pour un service différent du simulateur, remplacer les lignes par les indicateurs de la cible concernée.

## 3. Formuler les hypothèses

| Hypothèse | Donnée attendue si elle est vraie | Donnée qui pourrait la contredire | Résultat |
| --- | --- | --- | --- |
| H1 — l'opération ou sa dépendance de stockage est le goulet | durée d'écriture élevée pendant le scénario, sans nécessité d'une panne de collecte | retour immédiat à la valeur nominale et absence de reproduction hors scénario |  |
| H2 — le CPU limite l'opération | CPU élevé avant ou pendant la hausse, avec autres signes de contention | CPU stable et aucune charge concordante |  |
| H3 — la mémoire limite l'opération | mémoire disponible en baisse, swap ou événement OOM | mémoire stable, absence de swap et pas d'événement mémoire |  |
| H4 — le réseau limite l'opération | erreurs, latence réseau ou autres services dégradés au même instant | réseau stable et dégradation limitée à l'opération |  |
| H5 — le service ou la sonde est le goulet | durée de sonde élevée, erreurs HTTP ou `probe_success=0` | sonde stable, service fonctionnel et seule la métrique simulée change |  |
| H6 — la collecte donne une fausse impression | `up=0`, points absents ou horodatages incohérents | points réguliers, `up=1` et logs concordants |  |

Une hypothèse est écartée seulement lorsqu'une donnée discriminante la contredit. L'absence d'une donnée ne suffit pas : elle doit être notée comme limite d'analyse.

## 4. Construire la chronologie

| Ordre | Heure et fuseau | Source | Fait observé | Interprétation prudente |
| ---: | --- | --- | --- | --- |
| 1 |  | Prometheus / simulateur | valeur nominale et collecte active | état de référence |
| 2 |  | fichier d'état / terminal | activation du scénario 17 | début du test, pas cause réelle de production |
| 3 |  | Prometheus | durée d'écriture élevée | dégradation de l'opération mesurée |
| 4 |  | logs | événement associé, s'il existe | confirmation du contexte ou limite si absent |
| 5 |  | Prometheus / sonde | service et collecte pendant l'essai | impact fonctionnel à qualifier |
| 6 |  | terminal / fichier d'état | désactivation du scénario | début du retour arrière |
| 7 |  | Prometheus | durée nominale et `up=1` | retour observé, à maintenir sur plusieurs points |

Ne pas utiliser l'heure d'une capture comme heure exacte de l'action. Conserver le fuseau et la précision réellement disponible.

## 5. Formuler le diagnostic

Répondre aux questions suivantes dans le compte rendu :

### Quel élément présente la principale limitation de performance ?

Nommer l'élément et l'indicateur, sans extrapoler au disque physique si seule l'opération simulée est mesurée.

### Quels éléments permettent de l'affirmer ?

Citer au minimum la série temporelle, la comparaison avant/pendant/après, la fraîcheur de la collecte et une source secondaire : service, sonde ou journal.

### Quels autres éléments ont été analysés et pourquoi ?

Expliquer l'analyse du CPU, de la mémoire, du stockage réel, du réseau, du service et de la collecte. Une hypothèse écartée reste une partie du diagnostic.

### Quelle relation existe entre la dégradation et le goulet identifié ?

Décrire la chronologie et la portée : le goulet doit précéder ou accompagner la dégradation, expliquer son impact et disparaître ou être corrigé avec le retour nominal.

### Quelles hypothèses ont été écartées ?

Lister les hypothèses contredites par une observation. Écrire « non déterminée » lorsque la donnée discriminante n'a pas été collectée.

## Diagnostic de référence du scénario 17

Avec les seules données du code du simulateur, le diagnostic défendable est : **la métrique d'opération d'écriture est le point de dégradation observé et le scénario 17 est la cause du changement de valeur pendant le test**. Le niveau de confiance est élevé pour le contexte simulé, car la valeur passe de `0,03 s` à `3,2 s` puis revient au nominal après suppression du fichier d'état.

Ce résultat ne permet pas d'affirmer qu'un disque réel est le goulet d'une infrastructure. Pour cette conclusion, il faudrait corréler la durée avec l'espace libre, les inodes, les métriques disque, le CPU, la mémoire, le réseau, le service et les journaux sur la même période.

## Conséquences et actions préventives

Si une limitation réelle se poursuit, elle peut provoquer une hausse de latence, des files d'attente, des erreurs d'écriture, une dégradation du service puis une indisponibilité. Avant l'incident :

- mesurer une baseline hors scénario et suivre la durée dans le temps ;
- vérifier l'espace libre, les inodes et la croissance des journaux ;
- ajouter une alerte sur une durée persistante, après avoir justifié le seuil ;
- relier l'alerte à une procédure de diagnostic et à un responsable ;
- contrôler les sondes et le service, pas seulement la métrique de stockage ;
- planifier la rotation, l'extension ou le déplacement des données si la capacité diminue ;
- rejouer le test après chaque changement et conserver les preuves avant/après.

## Trace à conserver

Le dossier doit contenir la période et le fuseau, les requêtes, les filtres de journaux, les captures ou exports, la chronologie, les corrélations, les hypothèses, les éléments écartés, le goulet retenu, le niveau de confiance, les limites et l'action proposée.

[Analyser les tendances et la capacité](analyser-tendances-capacite.md) · [Préparer la maintenance préventive](preparer-maintenance-preventive.md) · [Retour au sommaire](index.md)
