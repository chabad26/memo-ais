# Analyser une dégradation de stockage

## Objectif

Approfondir la situation sélectionnée dans la feuille [Rechercher les évolutions significatives](rechercher-evolutions-significatives.md) : le temps de réponse de l'opération d'écriture du scénario 17.

L'analyse doit déterminer si la hausse est une variation ponctuelle injectée ou le symptôme d'une dégradation reproductible. Elle doit comparer l'état nominal, l'état dégradé et le retour à la normale, puis relier la métrique au service et aux journaux.

!!! warning "Périmètre du test"
    Le scénario est volontairement simulé. Il ne mesure pas le remplissage réel du disque et ne doit pas être présenté comme une preuve de saturation. Ne pas remplir le disque de la VM.

## 1. Démarrer la plateforme dans la VM

Dans la VM qui contient `/home/oliv/Documents/entreprise/AIS/Modules/observabilite` :

```bash
cd /home/oliv/Documents/entreprise/AIS/Modules/observabilite

COMPOSE_FILES=(
  -f compose.yaml
  -f compose.override.yaml
  -f compose.inject18.yml
  -f compose.inject19.yml
  -f compose.simulateur.yml
)

docker compose "${COMPOSE_FILES[@]}" config --quiet
docker compose "${COMPOSE_FILES[@]}" up -d
```

Contrôler le démarrage :

```bash
docker compose "${COMPOSE_FILES[@]}" ps
docker compose "${COMPOSE_FILES[@]}" logs --tail=50 prometheus lab-simulator
curl --fail http://127.0.0.1:9090/-/ready
curl --fail http://127.0.0.1:18083/health
```

Les interfaces sont publiées en boucle locale : Prometheus `9090`, Grafana `3000`, Alertmanager `9093`, Kibana `5601` et simulateur `18083`. Depuis une autre machine, utiliser un tunnel SSH vers la VM plutôt que d'exposer ces ports.

## 2. Vérifier l'état nominal

Avant d'activer le scénario, noter l'heure :

```bash
date --iso-8601=seconds
```

Relever plusieurs fois la métrique nominale, à au moins 5 secondes d'intervalle :

```bash
curl --silent http://127.0.0.1:18083/metrics | grep 'lab_storage_operation_duration_seconds'
```

Dans Prometheus, utiliser :

```promql
lab_storage_operation_duration_seconds{scenario="17",operation="write"}
```

Contrôler également la disponibilité du simulateur et la fraîcheur de sa collecte :

```promql
up{job="lab_simulator"}
```

Noter dans le compte rendu l'heure, la valeur, l'unité, le nombre de points et le job utilisé. L'état nominal attendu est `0.03` seconde et `up=1`.

## 3. Activer le scénario 17

Dans un second terminal de la même VM :

```bash
cd /home/oliv/Documents/entreprise/AIS/Modules/observabilite
printf 'scenario 17 actif\n' > injects/simulateur/state/17-disque.active
date --iso-8601=seconds
```

Le simulateur est interrogé par Prometheus toutes les 5 secondes. Attendre plusieurs collectes, puis relever :

```promql
lab_storage_operation_duration_seconds{scenario="17",operation="write"}
```

La valeur simulée attendue est `3.2` secondes. Ce résultat montre une dégradation de l'opération observée ; il ne permet pas à lui seul d'attribuer la cause à un disque physique, au CPU, à la mémoire ou au réseau.

Consulter les journaux du simulateur :

```bash
docker compose "${COMPOSE_FILES[@]}" logs --since=5m lab-simulator
```

Conserver l'heure d'activation, les valeurs observées et les journaux sans modifier d'autre service.

## 4. Désactiver et vérifier le retour

Toujours dans la VM :

```bash
rm -f injects/simulateur/state/17-disque.active
date --iso-8601=seconds
```

Après plusieurs scrapes, vérifier le retour vers `0.03` seconde et `up=1`. La désactivation du fichier d'état est l'action de retour arrière du scénario.

| Phase | Heure | Valeur attendue | `up` | Preuve |
| --- | --- | ---: | ---: | --- |
| Avant activation |  | `0.03 s` | `1` | PromQL et capture |
| Pendant activation |  | `3.2 s` | `1` | PromQL, heure d'activation et logs |
| Après désactivation |  | `0.03 s` | `1` | PromQL et heure de retour |

## 5. Corréler et discuter la cause

Compléter ce tableau sans transformer une corrélation en causalité :

| Observation | Source | Ce que cela confirme | Ce que cela ne confirme pas |
| --- | --- | --- | --- |
| Durée d'écriture élevée | `lab_storage_operation_duration_seconds` | L'opération simulée est lente pendant le scénario. | Une saturation réelle du disque. |
| Simulateur toujours collecté | `up{job="lab_simulator"}` | Prometheus reçoit encore les métriques. | La santé de tous les services. |
| Événement du simulateur | logs Docker `lab-simulator` | Le scénario ou une requête a été traité. | La cause technique d'une infrastructure réelle. |
| CPU et mémoire de la VM | Node Exporter / Windows Exporter | Une ressource peut être comparée dans la même période. | Une cause si aucune évolution concordante n'est observée. |

Comparer la métrique avec CPU, mémoire, réseau, disponibilité et journaux sur une même plage. Une hausse du temps de réponse sans hausse des ressources peut correspondre au scénario lui-même ; une hausse reproductible hors scénario demanderait une investigation complémentaire.

## 6. Décider d'une action

| Résultat de l'essai | Décision |
| --- | --- |
| Hausse uniquement pendant l'activation, retour nominal après suppression | Classer comme variation injectée ; conserver le scénario comme test de supervision. |
| Hausse répétée hors activation | Rechercher la ressource ou dépendance commune, prolonger la collecte et créer une baseline. |
| Données absentes ou `up=0` | Traiter d'abord la perte de collecte ; aucune conclusion sur la performance du stockage. |
| Hausse accompagnée d'erreurs ou d'un service lent | Préparer une maintenance ciblée après confirmation par les journaux et le propriétaire du service. |

Une alerte de performance ne doit être proposée qu'après mesure d'un comportement nominal et choix d'une durée adaptée. Pour ce scénario, une valeur `3.2 s` est un résultat de test, pas un seuil de production.

## Livrable attendu

- une chronologie avant / pendant / après ;
- les valeurs PromQL et les heures de collecte ;
- les journaux utiles du simulateur ;
- la comparaison avec CPU, mémoire, réseau et service ;
- la conclusion sur variation ponctuelle ou dégradation à confirmer ;
- une action proposée et son retour arrière ;
- les limites de preuve, notamment l'absence de mesure du remplissage réel du disque.

[Préparer la maintenance préventive](preparer-maintenance-preventive.md) · [Retour au sommaire](index.md)
