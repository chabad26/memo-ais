# Vérifier le retour à la normale

## Objectif et travail demandé

Après l’action corrective sur le site IIS, vérifier que le service est réellement revenu à l’état nominal. La disparition de l’alerte doit être confrontée aux métriques, à la sonde, aux journaux et au fonctionnement attendu, puis comparée à l’état antérieur à l’incident.

Le cas étudié reste **`ServiceHTTPIndisponible` sur Windows Core / IIS**. La [cause probable](identifier-cause-probable.md) est l’arrêt volontaire du site `AlpesNet-Sonde`. Les preuves du [test et de sa reprise](configurer-tester-alertes.md#captures-retour-au-nominal-du-site-iis) datent du 16 septembre 2026.

!!! note "Limite de la validation"
    Les captures prouvent un retour fonctionnel sur plusieurs contrôles successifs entre 14:21:25 et 14:22:42. Elles ne constituent pas une surveillance prolongée. La stabilité doit continuer à être observée si le service est destiné à rester disponible.

## 1. État nominal attendu

| Élément | État nominal retenu |
| --- | --- |
| Site IIS | `AlpesNet-Sonde` en état `Started` |
| Contrôle local | HTTP 200 et contenu attendu sur `http://127.0.0.1:8080/health.txt` |
| Sonde distante | `probe_success{job="sonde_windows_http"}=1` |
| Collecte | Endpoint Windows et résultat de sonde toujours collectés |
| Alerte | `ServiceHTTPIndisponible` inactive et absente des alertes actives d’Alertmanager |
| Notification | `resolved` reçu par `alert-receiver` |
| Journaux | Aucun nouvel événement significatif indiquant une nouvelle perte du service pendant la période observée |

L’état nominal ne signifie pas que toutes les métriques doivent être identiques à une valeur historique exacte. Elles doivent être cohérentes avec le fonctionnement attendu et rester présentes.

## 2. Vérification avant et après traitement

| Élément vérifié | Avant traitement | Après traitement | Retour à la normale confirmé |
| --- | --- | --- | --- |
| Alerte | `ServiceHTTPIndisponible` en `pending` à 14:19:34, puis `firing` à 14:20:29 ; alerte visible dans Alertmanager | Webhook `resolved` à 14:21:25 UTC+2 ; cinq règles `Inactive` à 14:22:19 ; Alertmanager vide à 14:22:42 | **Oui** |
| Métrique | Collecte Windows à 1 ; durée de la sonde IIS proche de 5 s pendant l’échec ; pas de saturation Windows manifeste | Collecte Windows toujours à 1 ; durée de la sonde redescendue après le plateau ; autres panneaux stables | **Oui pour les métriques visibles**, avec surveillance prolongée à poursuivre |
| Sonde | IIS à 0 tandis que Nginx reste à 1 | IIS à 1 et Nginx à 1 à 14:22:22 ; réponse locale HTTP 200 | **Oui**, contrôle local et distant concordants |
| Journal | Kibana : HttpService code 115 à 14:18:46, suppression des URL d’un groupe HTTP ; webhook `firing` à 14:20:25 | Webhook `resolved` à 14:21:25, POST HTTP 200 ; aucun nouvel événement Windows significatif n’est démontré par une vue exhaustive | **Oui pour la chaîne d’alerte** ; absence durable d’événement Windows à surveiller |

### Conclusion

Le retour à l’état nominal est **confirmé pour le service IIS et sa supervision** : le site est `Started`, la réponse locale retourne HTTP 200, la sonde distante vaut 1, la collecte reste présente, la règle est inactive, Alertmanager ne présente plus le groupe et le webhook a reçu `resolved`.

Cette conclusion porte sur la période observée. Elle ne prouve pas une stabilité de plusieurs heures et ne permet pas d’affirmer qu’aucun autre événement Windows n’a eu lieu après la dernière capture.

## 3. Contrôles à effectuer après l’action corrective

### A. Vérifier le service local

Sur Windows Core, en PowerShell administrateur :

```powershell
Import-Module WebAdministration
Get-Website -Name 'AlpesNet-Sonde'
Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:8080/health.txt' |
  Select-Object StatusCode, Content
```

Attendre `Started`, HTTP 200 et le contenu prévu. La capture disponible montre ces résultats, même si le contenu apparaît tronqué dans le terminal.

### B. Vérifier les métriques et la sonde

Dans Grafana Explore ou Prometheus :

```promql
probe_success{job="sonde_windows_http"}
```

```promql
up{job="sonde_windows_http"}
```

```promql
up{job="windows"}
```

```promql
probe_duration_seconds{job="sonde_windows_http"}
```

Vérifier au minimum que `probe_success=1`, que les deux collectes restent à 1 et que la durée de sonde ne reste pas au niveau dégradé observé pendant l’incident. Une série absente ne vaut pas zéro et ne confirme pas une résolution.

### C. Vérifier l’alerte et la notification

Dans Prometheus, confirmer que `ServiceHTTPIndisponible` est `Inactive`. Dans Alertmanager, vérifier que le groupe actif a disparu. Sur supervision :

```bash
cd ~/observabilite
sudo docker compose logs --no-color \
  --since='2026-09-16T12:15:00Z' \
  --until='2026-09-16T12:25:00Z' alert-receiver
```

Le résultat conservé contient `resolved` à `2026-09-16T12:21:25.734460+00:00`, avec un POST `/alerts` traité en HTTP 200.

### D. Rechercher de nouveaux événements

Dans Kibana Discover, utiliser une période qui commence avant l’incident et se prolonge après la reprise :

```kql
fields.lab_source: "windows"
```

Comparer les événements avant et après 14:21:25. Examiner notamment `@timestamp`, `event.provider`, `event.code`, `message` et l’hôte. L’objectif est de repérer une nouvelle suppression d’URL, un redémarrage, une erreur IIS ou une répétition du symptôme.

La capture `Service_Control_Manager` montre des événements visibles à 14:39, mais leurs messages ne sont pas développés et ils se situent hors de la fenêtre initiale 14:15–14:25. Ils ne doivent pas être qualifiés comme rechute ou événement significatif sans lecture de leur contenu.

## 4. Comparaison avec l’état antérieur à l’incident

| Contrôle | Avant l’incident | Pendant | Après |
| --- | --- | --- | --- |
| Site IIS | HTTP 200 observé | `Stopped` | `Started`, HTTP 200 |
| Sonde IIS | État nominal attendu à 1 | 0 | 1 |
| Sonde Nginx | 1 | 1 | 1 |
| Collecte Windows | 1 | 1 | 1 |
| Alerte HTTP | Inactive | Pending puis Firing | Inactive |
| Alertmanager | Aucun groupe | Groupe HTTP actif | Aucun groupe |
| Webhook | Aucun événement attendu | `firing` reçu | `resolved` reçu |

Cette comparaison montre que le service a retrouvé le même comportement fonctionnel qu’avant l’incident, tandis que les composants de collecte sont restés disponibles pendant toute la séquence.

## 5. Détecter une dégradation persistante

Une alerte peut disparaître alors qu’une dégradation subsiste. Cela peut arriver si la valeur passe juste sous le seuil, si les données disparaissent, si le service répond avec une forte latence ou si le test vérifie seulement une page trop simple.

Après la résolution, contrôler donc :

- la présence continue des séries et leur fraîcheur ;
- la durée de la sonde et pas seulement son résultat binaire ;
- les codes HTTP et le contenu fonctionnel attendu ;
- les ressources Windows et les erreurs applicatives ;
- les événements répétés dans les journaux ;
- l’absence de nouveaux passages `pending` ou `firing` pendant une période adaptée au service.

Dans ce lab, observer au moins plusieurs évaluations successives. Pour une exploitation réelle, définir une durée de stabilité selon la criticité et les engagements de service.

## 6. Apport théorique — Diagnostic à partir de l’observabilité

Le diagnostic commence par un signal : alerte, métrique anormale, sonde en échec ou événement dans un journal. Ce signal décrit un symptôme possible, pas nécessairement sa cause.

```text
Signal → Observation → Hypothèse → Vérification → Corrélation
→ Cause probable → Action → Vérification du retour nominal
```

Les sources répondent à des questions complémentaires :

| Source | Question principale | Application au cas IIS |
| --- | --- | --- |
| Métriques | Qu’est-ce qui évolue ou se dégrade ? | Résultat et durée de sonde, continuité de collecte, ressources Windows |
| Sondes | Quel service répond correctement ? | IIS échoue tandis que Nginx répond, puis IIS revient à 1 |
| Journaux | Quels événements se sont produits ? | Retrait des URL HTTP, réception de `firing` puis `resolved` |

La corrélation rapproche les événements, les variations, les changements d’état et leurs heures. Elle permet de construire une hypothèse. La vérification doit ensuite rechercher une donnée discriminante et un retour cohérent après l’action corrective.

La fin de l’incident exige cinq contrôles : alerte résolue, métriques attendues, sondes nominales, absence de nouvel événement significatif dans la période observée et fonctionnement réellement rétabli.

## Questions de fin d’étape

| Question | Réponse pour le cas IIS |
| --- | --- |
| La disparition de l’alerte suffit-elle ? | Non. Elle peut provenir d’un retour sous le seuil ou d’une perte de données. Il faut confirmer le service, les métriques, la sonde et la collecte. |
| Quelles données prouvent la résolution ? | Site `Started`, HTTP 200, `probe_success=1`, collectes à 1, règle inactive, Alertmanager vide et notification `resolved`. |
| Comment détecter une dégradation persistante ? | Observer durée de sonde, ressources, erreurs, fraîcheur des séries et éventuelles récidives sur plusieurs évaluations. |
| Pourquoi conserver la trace du diagnostic ? | Pour justifier l’action, expliquer les limites, accélérer une récidive, améliorer l’alerte et transmettre la connaissance à un autre administrateur. |

## Trace à conserver

- état avant, pendant et après avec heures et fuseaux ;
- action corrective proposée ou réalisée ;
- requêtes, commandes et résultats ;
- preuve `resolved` et contrôles fonctionnels ;
- événements significatifs ou absence documentée dans la période ;
- durée d’observation après reprise ;
- limites et risque de récidive.

## Point de contrôle

- [x] État de l’alerte vérifié après traitement.
- [x] Métriques et continuité de collecte vérifiées.
- [x] Sonde locale et distante vérifiées.
- [x] Notification `resolved` recherchée et conservée.
- [x] Situation comparée à l’état antérieur.
- [x] Retour nominal confirmé pour le service IIS sur la période observée.
- [ ] Absence prolongée de nouvel événement significatif à confirmer par une surveillance plus longue.

[Cause probable](identifier-cause-probable.md) · [Chronologie corrélée](correler-metriques-sondes-journaux.md) · [Sommaire de l’itération](index.md)
