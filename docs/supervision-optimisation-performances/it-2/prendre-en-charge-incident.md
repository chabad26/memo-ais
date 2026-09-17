# Prendre en charge l’incident

## Objectif de la mise en situation

Prendre en charge, de manière autonome et traçable, un incident déclenché dans l’environnement de supervision. La nature du problème, l’élément à l’origine de l’incident, sa cause et les données utiles ne sont pas connus à l’avance.

Le diagnostic doit partir uniquement du signal reçu et des informations réellement disponibles dans Prometheus, Grafana, Blackbox Exporter, Alertmanager, Kibana et les systèmes observés. Cette feuille décrit la démarche à suivre ; elle ne révèle pas l’inject et ne constitue pas la preuve qu’un incident a déjà été traité.

!!! warning "Règle d’intervention"
    Observer et conserver les traces avant de modifier l’environnement. Ne pas redémarrer toute la plateforme, arrêter une VM ou changer plusieurs paramètres « pour essayer ». Toute action doit être ciblée, justifiée, horodatée et réversible lorsque c’est possible.

## 1. Ouvrir le suivi de l’incident

Noter immédiatement l’heure et créer un dossier distinct sur la VM `supervision` :

```bash
date --iso-8601=seconds
cd ~/observabilite
INCIDENT_ID="incident-$(date +%Y%m%d-%H%M%S)"
install -d -m 700 "diagnostics/$INCIDENT_ID"/{captures,exports,journaux}
printf '%s\n' "$INCIDENT_ID"
```

Dans `chronologie.md`, consigner chaque observation et chaque action dans le même fuseau horaire :

| Heure et fuseau | Source | Observation factuelle | Hypothèse | Vérification ou action | Résultat | Décision suivante |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

Ne jamais remplacer un fait par une interprétation. Par exemple, `probe_success=0` prouve l’échec d’une sonde ; cette valeur ne prouve pas encore que la cible est arrêtée.

## 2. Qualifier le signal initial

Relever le signal sans acquitter, masquer ou corriger immédiatement l’incident.

| Information | Valeur à relever |
| --- | --- |
| Source du signal | Prometheus, Alertmanager, Grafana, utilisateur, journal ou autre source |
| Nom et état | Nom de l’alerte ou description exacte du signal ; `pending`, `firing` ou autre état |
| Première heure visible | Horodatage et fuseau affichés par la source |
| Élément désigné | Instance, endpoint, service, job, URL ou hôte |
| Criticité | Label et impact observable, sans les confondre |
| Condition | Expression, seuil et durée de persistance |
| Résumé disponible | Message, annotations et valeurs présentes |

Dans Prometheus, examiner **Alerts**, puis la règle concernée. Dans Alertmanager, relever les labels sans conclure que la notification explique la cause. Si le signal vient d’un utilisateur, retranscrire ses mots et l’heure du constat.

Formuler ensuite une première question opérationnelle :

> Quel service rendu est affecté, depuis quand, pour quelles cibles et avec quel impact actuellement observable ?

## 3. Vérifier que les sources de diagnostic fonctionnent

Avant d’interpréter une absence de données, contrôler la plateforme depuis `supervision` :

```bash
cd ~/observabilite
sudo docker compose ps
curl --fail http://127.0.0.1:9090/-/ready
curl --fail http://127.0.0.1:9093/-/ready
```

Vérifier dans Prometheus **Status > Targets** la collecte des jobs attendus. Une série absente ne vaut pas zéro : elle peut signaler une collecte interrompue, une requête incorrecte ou une donnée trop ancienne.

Si les interfaces doivent être consultées depuis le laptop, garder ce tunnel ouvert :

```bash
ssh -N -o ExitOnForwardFailure=yes \
  -L 9090:127.0.0.1:9090 \
  -L 3000:127.0.0.1:3000 \
  -L 5601:127.0.0.1:5601 \
  -L 9093:127.0.0.1:9093 \
  oliv@192.168.122.80
```

Le tunnel donne accès aux interfaces. Il ne transporte pas les journaux Filebeat vers `192.168.122.80:5044`.

Si un outil de supervision est lui-même en défaut, consigner cette limite. Ne pas attribuer automatiquement ce défaut à l’incident injecté.

## 4. Délimiter l’incident avec les métriques

Choisir dans Grafana une plage couvrant une période stable avant le signal, le déclenchement et l’état actuel. Utiliser une plage absolue pour le rapport. Comparer la cible suspecte avec une cible témoin et examiner notamment :

```promql
up{job=~"linux|windows"}
```

```promql
probe_success{job=~"sonde_.*"}
```

```promql
probe_duration_seconds{job=~"sonde_.*"}
```

Adapter ensuite les requêtes à l’alerte : charge CPU, mémoire disponible, espace disque, disponibilité de l’exporter ou état fonctionnel HTTP. Relever la valeur, les labels, l’heure du dernier point, la tendance et la comparaison avant/pendant l’incident.

Répondre à quatre questions :

1. le défaut concerne-t-il un service, un hôte ou plusieurs cibles ;
2. la collecte fonctionne-t-elle encore ;
3. le symptôme est-il brutal, progressif, intermittent ou permanent ;
4. un autre indicateur évolue-t-il au même moment sans qu’un lien causal soit encore établi ?

## 5. Examiner les sondes concernées

Pour une alerte fonctionnelle, distinguer la collecte de la sonde et le résultat de la sonde :

| Observation | Interprétation limitée |
| --- | --- |
| `up=1` et `probe_success=0` | Blackbox est collecté, mais le contrôle de la cible échoue |
| `up=0` | Prometheus ne collecte pas correctement la cible du job |
| Série absente | Donnée indisponible ou requête à revoir ; aucune conclusion sur le service |
| Sonde témoin à `1` | Le témoin fonctionne ; cela ne valide pas tous les chemins réseau |

Consulter le détail disponible : statut HTTP, durée, phase lente, erreur TLS, résolution DNS ou refus de connexion. Comparer si possible un test local sur la cible et le test distant depuis la supervision au même instant.

## 6. Rechercher les événements dans les journaux

Dans **Kibana > Discover**, sélectionner la vue `Journaux AlpesNet`, reprendre exactement la plage temporelle des métriques et trier du plus ancien au plus récent.

Commencer large, puis resserrer selon les champs réellement présents :

```kql
fields.lab_source: "linux" or fields.lab_source: "windows"
```

```kql
host.name: "NOM_HOTE"
```

Afficher si disponibles `@timestamp`, `host.name`, `event.provider`, `event.code`, `winlog.channel`, `log.file.path` et `message`. Rechercher successivement :

- les changements d’état du service concerné ;
- les erreurs applicatives, réseau, disque, mémoire ou authentification proches du signal ;
- les actions d’administration ou redémarrages visibles ;
- les événements précédant le symptôme, puis ceux du rétablissement.

L’absence de résultat signifie seulement : « aucun événement pertinent trouvé dans les journaux collectés, pour ce filtre et cette période ». Conserver le filtre, la période, le fuseau et le nombre de résultats.

Pour contrôler le parcours de l’alerte sur `supervision` :

```bash
cd ~/observabilite
sudo docker compose logs --no-color --since=30m \
  prometheus alertmanager alert-receiver
```

Limiter ensuite l’export à la fenêtre utile et ne jamais inclure de clé, mot de passe, jeton ou identifiant inutile dans le rapport.

## 7. Reconstituer une chronologie commune

Reporter uniquement les transitions soutenues par une source :

| Ordre | Heure | Source | Fait observé | Niveau de certitude |
| ---: | --- | --- | --- | --- |
| 1 |  | Métrique, sonde ou journal | Dernier état nominal visible | Observé / estimé |
| 2 |  | Journal ou métrique | Premier changement pertinent | Observé / compatible |
| 3 |  | Prometheus | Condition détectée puis éventuel état `pending` | Observé |
| 4 |  | Prometheus / Alertmanager | Passage en `firing` et transmission | Observé |
| 5 |  | Système cible | Action corrective | Réalisée / proposée |
| 6 |  | Sources croisées | Retour des valeurs au nominal | Observé |
| 7 |  | Alertmanager | État `resolved` ou disparition de l’alerte | Observé |

Convertir explicitement UTC et heure locale si nécessaire. Ne pas déduire l’heure exacte d’une panne à partir de l’heure d’une capture prise plus tard.

## 8. Formuler et vérifier plusieurs hypothèses

Écrire au moins trois hypothèses avant de corriger. Elles doivent être testables et couvrir des niveaux différents, par exemple service local, ressource système, chemin réseau, configuration de sonde ou défaut de collecte.

| Hypothèse | Résultat attendu si elle est vraie | Donnée discriminante | Vérification non destructive | Résultat | Décision |
| --- | --- | --- | --- | --- | --- |
| H1 |  |  |  |  | Confirmée / affaiblie / écartée |
| H2 |  |  |  |  | Confirmée / affaiblie / écartée |
| H3 |  |  |  |  | Confirmée / affaiblie / écartée |

Pour chaque hypothèse, chercher aussi une donnée susceptible de la contredire. Plusieurs courbes simultanées prouvent une corrélation temporelle ; elles ne prouvent pas à elles seules une causalité.

Retenir comme cause probable l’explication qui correspond au périmètre, précède le symptôme, résiste aux contradictions et explique le retour au nominal. Indiquer un niveau de confiance et les informations manquantes.

## 9. Décider et réaliser l’action corrective

Avant l’action, noter :

- la cause probable et les preuves qui la soutiennent ;
- l’impact attendu si aucune action n’est réalisée ;
- l’action choisie, son risque et son périmètre ;
- la solution de retour arrière ;
- l’heure de début et la personne qui intervient.

Privilégier l’action minimale qui traite la cause probable. Si l’action dépasse les droits accordés, risque d’aggraver l’incident ou exige une indisponibilité supplémentaire, ne pas l’improviser : proposer l’action, préserver les traces et appliquer l’escalade prévue.

Une amélioration temporaire après un redémarrage ne démontre pas que la cause a été supprimée. Consigner alors le redémarrage comme mesure de rétablissement et poursuivre l’analyse de cause.

## 10. Vérifier le retour à la normale

Répéter les mêmes contrôles qu’au début, sans se limiter à la disparition de l’alerte :

| Contrôle | Critère de validation |
| --- | --- |
| Service rendu | Test fonctionnel réussi depuis le point de vue attendu |
| Métriques | Valeurs revenues dans la plage nominale et points récents |
| Sonde | `probe_success=1` si applicable, avec collecte active |
| Journaux | Absence de nouvelle erreur pertinente ; événement de reprise conservé s’il existe |
| Alerte | Règle inactive et notification `resolved` observée si le parcours la prévoit |
| Stabilité | État maintenu pendant une durée cohérente avec le `for` de la règle et le rythme de collecte |
| Effets de bord | Autres services et cibles témoins toujours opérationnels |

Si un contrôle échoue, l’incident reste ouvert. Reprendre les hypothèses avec les nouvelles données plutôt que de déclarer le rétablissement.

## 11. Constituer les traces du rapport

Conserver dans le dossier de l’incident :

- le signal initial, ses labels et son horodatage ;
- la plage temporelle et les requêtes PromQL utilisées ;
- les états des cibles et des sondes avant, pendant et après ;
- les filtres Kibana et seulement les événements utiles ;
- la chronologie consolidée ;
- les hypothèses, y compris celles qui ont été écartées ;
- la cause probable, son niveau de confiance et les limites du diagnostic ;
- l’action réalisée ou proposée, son résultat et son éventuel retour arrière ;
- les preuves fonctionnelles du retour à la normale et de sa stabilité.

Les captures montrent ce qui était visible ; les exports textuels, commandes et requêtes rendent le diagnostic reproductible. Masquer les secrets et réduire les données au strict périmètre de l’incident.

## Compte rendu final

Le rapport doit permettre à une autre personne de répondre sans ambiguïté aux questions suivantes :

1. quel signal a déclenché la prise en charge ;
2. quel élément et quel service rendu étaient concernés ;
3. quelles sources ont été consultées et sur quelle période ;
4. quelle chronologie est soutenue par les preuves ;
5. quelles hypothèses ont été vérifiées ;
6. quelle cause probable a été retenue et avec quel niveau de confiance ;
7. quelle action a été réalisée ou proposée ;
8. comment le retour à la normale et sa stabilité ont été démontrés ;
9. quelles informations manquent encore et quelles suites sont nécessaires.

## État attendu

L’incident est pris en charge à partir d’un signal conservé. Le périmètre et la chronologie reposent sur des métriques, des sondes et des journaux corrélés. Plusieurs hypothèses ont été confrontées aux données. La cause probable, l’action et les limites sont explicites. Le retour à la normale est démontré par un test fonctionnel et une période de stabilité, puis les traces utiles sont prêtes pour le rapport.

[Préparer la mise en situation](preparer-mise-en-situation.md) · [Procédure de réponse](construire-procedure-reponse.md) · [Retour au sommaire](index.md)
