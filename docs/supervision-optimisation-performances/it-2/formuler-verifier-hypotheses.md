# Formuler et vérifier des hypothèses

## Objectif et travail demandé

Transformer les pistes issues de l’[analyse initiale de l’alerte](partir-alerte-rechercher-situation.md) en hypothèses vérifiables. Pour chacune, rechercher des données capables de la confirmer ou de l’écarter en croisant, lorsque cela est pertinent, les métriques, les sondes, les journaux, les dashboards et les informations temporelles.

Le cas étudié reste l’alerte **`ServiceHTTPIndisponible` sur Windows Core / IIS**, observée le 16 septembre 2026. Trois hypothèses sont examinées : arrêt du site IIS, perturbation réseau vers le port 8080 et erreur de configuration ou de contenu de la sonde HTTP.

!!! note "Périmètre des preuves"
    Les captures attestent l’arrêt volontaire du site, l’échec de la sonde, le déclenchement, les notifications `firing` et `resolved`, puis le retour au nominal. Kibana fournit un événement HttpService cohérent avec le retrait des URL HTTP. Les heures exactes des commandes et l’attribution de l’action restent inconnues.

## 1. Passer d’une idée à une hypothèse testable

Une hypothèse utile relie un fait observé à une cause possible et prévoit un contrôle susceptible de la contredire. Elle doit pouvoir être reformulée ainsi :

> Si cette hypothèse est vraie, alors telle donnée devrait être présente ; si telle autre donnée apparaît, l’hypothèse doit être écartée ou révisée.

| Niveau | Sens dans le diagnostic |
| --- | --- |
| Fait observé | Information directement visible dans une source conservée |
| Indice compatible | Information cohérente avec l’hypothèse, mais également explicable autrement |
| Donnée discriminante | Information qui permet de départager plusieurs hypothèses |
| Contradiction | Information incompatible avec l’hypothèse telle qu’elle est formulée |
| Donnée manquante | Information non collectée, expirée ou pas encore recherchée |
| Conclusion | Hypothèse confirmée, écartée, affaiblie ou encore indéterminée |

Une hypothèse n’est pas confirmée par le nombre de captures, mais par la qualité et l’indépendance des données. Une commande d’administration, le résultat d’une sonde distante et le retour fonctionnel HTTP décrivent des aspects différents du même cas.

## 2. Chronologie commune aux vérifications

Utiliser la plage absolue **16 septembre 2026, 14:15–14:25 heure de Paris**, soit **12:15–12:25 UTC**. Vérifier le fuseau affiché par chaque outil.

| Heure de capture locale | Donnée |
| --- | --- |
| 14:19:34 | `ServiceHTTPIndisponible` passe en `pending` |
| 14:19:43 | Sonde IIS à 0, sonde Nginx à 1 et collecte des endpoints à 1 |
| 14:20:29 | Alerte HTTP en `firing` dans Prometheus |
| 14:20:36 | Alerte visible dans Alertmanager |
| 14:20:46 | PowerShell montre `Stop-Website` puis le site `Stopped` |
| 14:22:04 | Site `Started` et réponse HTTP locale 200 |
| 14:22:19–14:22:42 | Règles inactives, sonde IIS à 1 et Alertmanager vide |

Ces heures sont celles des captures. Elles ordonnent les observations, mais ne donnent ni l’instant exact des commandes ni une durée exacte de panne.

## 3. Tableau de vérification complété

| Hypothèse | Donnée recherchée | Source | Observation | Hypothèse confirmée ? |
| --- | --- | --- | --- | --- |
| **H1 — Le site IIS a été arrêté volontairement** | Action d’arrêt et état du site | PowerShell Windows Core | `Stop-Website -Name 'AlpesNet-Sonde'`, puis état `Stopped` visibles | **Oui, pour le test contrôlé** |
| H1 | Le système Windows reste observable pendant l’échec HTTP | Dashboard Grafana | Collecte de l’endpoint Windows à 1 tandis que la sonde IIS vaut 0 | **Compatible** : l’hôte reste supervisé, le défaut est plus ciblé |
| H1 | Le retour du site fait disparaître le symptôme | PowerShell, Grafana, Prometheus, Alertmanager | Site `Started`, HTTP 200, sonde à 1, règles inactives et Alertmanager vide | **Oui, convergence de plusieurs sources** |
| H1 | Événement journalisé autour de l’arrêt ou de la reprise | Kibana Discover / journaux Windows disponibles | **Observé :** HttpService code 115 à 14:18:46.509, suppression des URL d’un groupe HTTP | **Compatible et temporellement cohérent**, sans attribution de l’action |
| **H2 — Le chemin réseau vers le port 8080 est perturbé** | Réponse locale correcte pendant que la sonde distante échoue | Test local Windows et sonde Blackbox au même instant | Aucune paire de mesures simultanées de ce type n’est conservée | **Indéterminée sur ce seul contrôle** |
| H2 | Disponibilité du reste de l’hôte et d’une autre sonde | Grafana | Exporter Windows et sonde Nginx disponibles | **Indice faible** : cela n’exclut pas un défaut propre au port 8080 |
| H2 | Reprise après une correction réseau | Pare-feu, écoute, détail Blackbox et journal des changements | Aucune correction réseau n’est montrée ; la reprise suit le rétablissement IIS | **Non démontrée et rendue moins probable** |
| **H3 — L’URL, le module ou le contenu attendu par la sonde est incorrect** | Configuration Blackbox et cible chargée | Fichiers Prometheus/Blackbox et page Targets | La même cible redevient à 1 après la reprise du site, sans correction de sonde attestée | **Affaiblie** |
| H3 | HTTP local 200 et contenu complet pendant un échec persistant de sonde | PowerShell et détail Blackbox simultanés | Aucun écart simultané conservé ; les contenus visibles sont tronqués | **Indéterminée sur le contenu exact** |
| H3 | Modification de configuration au moment du retour | Historique des fichiers et journaux de déploiement | Aucune modification de sonde documentée entre l’échec et la reprise | **Non démontrée** |

### Conclusion du tableau

**H1 est confirmée dans le cadre de l’exercice contrôlé.** La commande d’arrêt et l’état `Stopped` fournissent la cause connue ; l’échec de la sonde et l’alerte constituent les symptômes observés. Le retour du site à `Started`, la réponse HTTP 200 et la sonde revenue à 1 renforcent cette conclusion.

H2 et H3 ne sont pas prouvées. Elles ne peuvent pas être déclarées impossibles dans l’absolu, car certaines données discriminantes n’ont pas été capturées pendant l’incident. Elles sont toutefois inutiles pour expliquer ce test une fois l’arrêt volontaire établi, sauf si un second défaut concomitant est suspecté.

## 4. Vérifier méthodiquement chaque hypothèse

### H1 — Site IIS arrêté

Les données les plus fortes sont l’état local du site et la commande d’administration. Les sondes et dashboards servent ensuite à mesurer l’effet et le périmètre.

Sur Windows Core, pendant un prochain exercice contrôlé :

```powershell
Get-Date -Format o
Get-Website -Name 'AlpesNet-Sonde'
Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:8080/health.txt' |
  Select-Object StatusCode, Content
```

Conserver le résultat avant l’arrêt, pendant l’arrêt et après la reprise. `Get-Date` aide à rapprocher les contrôles locaux des métriques, sans supposer que les horloges sont parfaitement synchronisées.

| Confirme H1 | Écarte ou oblige à reformuler H1 |
| --- | --- |
| Site `Stopped` pendant l’échec distant ; reprise après `Start-Website` | Site `Started`, réponse locale 200 complète et sonde distante toujours en échec pendant la même période |

### H2 — Perturbation du chemin réseau vers le port 8080

Cette hypothèse exige de comparer **au même moment** le service local et l’accès depuis la supervision. Une réponse locale réussie ne suffit pas si elle est prise après le rétablissement.

Sur supervision, utiliser la procédure Blackbox existante pour obtenir le détail de la sonde, puis vérifier la connectivité vers la cible. Conserver l’heure, le module et le résultat. Ne pas modifier le pare-feu uniquement pour « essayer » sans avoir identifié un blocage.

| Confirme H2 | Écarte ou affaiblit H2 |
| --- | --- |
| HTTP local fonctionnel, écoute présente, mais accès distant au port 8080 impossible avec une erreur réseau cohérente | Site local `Stopped`, puis sonde distante rétablie dès que le site repasse `Started`, sans correction réseau |

La collecte de `windows_exporter` sur un autre port prouve seulement qu’un autre chemin fonctionne. Elle ne valide pas le port 8080.

### H3 — Configuration ou contenu de sonde incorrect

Comparer la cible réellement chargée, le module Blackbox et la réponse complète du service. Vérifier les fichiers et la page Targets avant toute modification.

```promql
probe_success{job="sonde_windows_http"}
```

```promql
probe_http_status_code{job="sonde_windows_http"}
```

La présence de `probe_http_status_code` dépend du résultat et des métriques exposées par Blackbox. Une série absente ne doit pas être interprétée comme un code zéro.

| Confirme H3 | Écarte ou affaiblit H3 |
| --- | --- |
| HTTP local répond, mais le statut, l’URL ou le marqueur ne respecte pas le module ; la correction du contrôle rétablit la sonde | Même configuration avant et après, et sonde à 1 dès que le site IIS est relancé |

## 5. Croiser métriques, sondes, journaux et dashboards

| Source | Ce qu’elle apporte | Limite dans ce cas |
| --- | --- | --- |
| Métriques Prometheus | Valeurs de la sonde, collecte et évolution temporelle | Décrivent un état mesuré, pas l’auteur ni la cause directe |
| Sonde Blackbox | Résultat fonctionnel depuis le chemin de supervision | Un échec peut venir du service, du réseau ou du contrôle |
| PowerShell Windows | État local d’IIS, réponse locale et action d’administration | Une capture tardive ne reconstitue pas seule toute la chronologie |
| Grafana | Vue corrélée avant, pendant et après | La résolution et la plage choisies peuvent masquer un événement bref |
| Prometheus Alerts / Alertmanager | Condition, labels, états et transmission de l’alerte | Ne prouvent pas la cause ni la livraison au webhook |
| Kibana / journaux Windows | Événement HttpService avant l’alerte ; recherche SCM visible hors fenêtre | Renforce la chronologie, mais n’indique pas l’auteur ni l’heure exacte de la commande |

Dans Kibana Discover, utiliser la même plage temporelle que les métriques et commencer par :

```kql
fields.lab_source: "windows"
```

Examiner les fournisseurs réellement présents avant de resserrer le filtre. Un arrêt de site IIS n’implique pas automatiquement un événement `Service Control Manager`, car le service IIS complet peut continuer à fonctionner. Noter « aucun événement pertinent trouvé dans les journaux collectés » si c’est le résultat ; ne pas conclure qu’aucun événement ne s’est produit.

## 6. Symptôme, cause et corrélation

| Élément | Application au test IIS |
| --- | --- |
| Symptôme | `probe_success=0`, alerte HTTP, durée de sonde élevée |
| Cause établie du test | Arrêt volontaire du site `AlpesNet-Sonde` |
| Conséquence | Page de contrôle inaccessible depuis la sonde pendant la période |
| Contexte concomitant | Test CPU Debian visible dans la même plage, sans lien causal démontré avec IIS |

Deux événements proches dans le temps peuvent avoir une cause commune, être indépendants ou résulter l’un de l’autre. La corrélation temporelle sert à orienter les vérifications ; elle ne suffit pas à démontrer la causalité. Ici, la commande `Stop-Website` et le rétablissement après reprise apportent une preuve plus forte que la simple proximité des courbes.

## Questions de fin d’étape

| Question | Réponse attendue |
| --- | --- |
| Quelle donnée confirme l’hypothèse ? | Une donnée prédite par l’hypothèse et suffisamment discriminante : ici, `Stop-Website`, l’état `Stopped` et la reprise après redémarrage. |
| Quelle donnée permet de l’écarter ? | Une contradiction observée au même moment : par exemple site local fonctionnel et erreur réseau distante persistante contre l’hypothèse d’un site arrêté. |
| Plusieurs sources donnent-elles la même information ? | Elles convergent sur l’indisponibilité et la reprise, mais chacune observe un niveau différent : action locale, service, sonde, règle et routage. |
| Les informations sont-elles cohérentes ? | Oui : événement HttpService, échec, alerte, notification, résolution et reprise s’ordonnent de façon cohérente. Les heures exactes des commandes restent inconnues. |
| La corrélation temporelle prouve-t-elle la causalité ? | Non. Elle sélectionne des pistes ; il faut une donnée discriminante ou une reproduction contrôlée. |
| Quelle différence entre symptôme et cause ? | Le symptôme est l’effet observable ; la cause est le mécanisme ou l’action qui produit cet effet. |

## Trace à conserver dans le rapport de diagnostic

Le rapport doit pouvoir être relu par un autre administrateur sans accès à la mémoire de l’exercice.

| Rubrique | Contenu à conserver |
| --- | --- |
| Alerte initiale | Nom, cible, service, criticité, condition et annotations |
| Périmètre temporel | Début et fin de recherche, fuseau et limites des horodatages |
| Observations | Valeurs, états, captures et résultats des commandes, avec leur source |
| Hypothèses | Formulation, donnée attendue, donnée contraire et priorité |
| Vérification | Requêtes et commandes exécutées, résultat réel, donnée manquante |
| Conclusion | Hypothèse confirmée, écartée ou indéterminée, avec niveau de confiance |
| Suite | Action corrective, vérification du retour au nominal et surveillance |

### Tableau vierge réutilisable

| Hypothèse | Donnée recherchée | Source | Observation | Hypothèse confirmée ? |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |

- [ ] Chaque hypothèse prévoit une donnée capable de la contredire.
- [ ] Les sources sont comparées sur la même cible et la même période.
- [ ] Les observations sont séparées des interprétations.
- [ ] Les données manquantes sont signalées.
- [ ] La conclusion distingue symptôme, cause et contexte.
- [ ] Le rapport conserve les commandes, résultats, heures et fuseaux utiles.

[Analyse initiale de l’alerte](partir-alerte-rechercher-situation.md) · [Procédure de réponse](construire-procedure-reponse.md) · [Sommaire de l’itération](index.md)

[Suite — Corréler les métriques, les sondes et les journaux](correler-metriques-sondes-journaux.md)
