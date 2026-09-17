# Identifier la cause probable

## Objectif et travail demandé

Établir le diagnostic du cas **`ServiceHTTPIndisponible` sur Windows Core / IIS** à partir des informations recueillies. La conclusion distingue les faits observés, les suppositions, les vérifications et la cause probable. Elle indique aussi le niveau de confiance et l’action que les preuves autorisent.

Cette feuille clôt l’analyse commencée avec l’[alerte](partir-alerte-rechercher-situation.md), poursuivie par la [vérification des hypothèses](formuler-verifier-hypotheses.md) et la [chronologie corrélée](correler-metriques-sondes-journaux.md).

!!! note "Portée du diagnostic"
    Il s’agit d’un exercice contrôlé. La cause technique du défaut HTTP est fortement étayée : la commande `Stop-Website`, l’état `Stopped`, l’événement HttpService et le retour après reprise convergent. Les preuves ne donnent pas l’heure exacte de la commande ni l’identité de la personne qui l’a exécutée. Elles ne démontrent pas non plus une panne complète de Windows.

## 1. Qualifier les informations recueillies

| Catégorie | Informations du cas IIS |
| --- | --- |
| **Observé** | Sonde IIS à 0 ; sonde Nginx à 1 ; endpoint Windows collecté ; règle `pending` puis `firing` ; site `Stopped` ; événement HttpService ; notifications reçues |
| **Supposé au début de l’analyse** | Site arrêté, chemin réseau vers le port 8080 perturbé ou contrôle HTTP incorrect |
| **Vérifié** | `Stop-Website` et état `Stopped` visibles ; événement HttpService à 14:18:46.509 ; reprise avec site `Started`, HTTP 200 et sonde à 1 |
| **Cause probable retenue** | Arrêt volontaire du site IIS `AlpesNet-Sonde`, qui a retiré ses URL HTTP et rendu la page de contrôle indisponible |
| **Non établi** | Auteur de l’action, heure exacte de `Stop-Website` et `Start-Website`, motif opérationnel hors cadre de l’exercice |

Une information observée n’est pas automatiquement une cause. `probe_success=0` est un symptôme ; `Stop-Website` et l’état `Stopped` décrivent ici le mécanisme qui l’a produit.

## 2. Diagnostic complété

| Élément | Conclusion |
| --- | --- |
| Incident observé | Indisponibilité temporaire de la page de contrôle HTTP du site IIS de test ; alerte `ServiceHTTPIndisponible` déclenchée |
| Élément concerné | Windows Core, site `AlpesNet-Sonde`, service logique `iis-lab`, URL `http://192.168.122.25:8080/health.txt` |
| Symptôme principal | `probe_success=0` pendant plus d’une minute alors que la collecte de la sonde reste valide ; réponse distante indisponible |
| Données utilisées | Prometheus Alerts, métriques et dashboard Grafana, sonde Blackbox, Alertmanager, PowerShell, événement Kibana `Microsoft-Windows-HttpService`, journal `alert-receiver` |
| Hypothèse principale | Le site IIS a été arrêté volontairement, sans arrêt général de Windows ni perte générale de supervision |
| Vérifications réalisées | `Stop-Website` et `Stopped` visibles ; endpoint Windows toujours collecté ; Nginx disponible ; événement HttpService avant le `pending` ; après reprise : `Started`, HTTP 200, sonde à 1, règle inactive, alerte retirée et `resolved` reçu |
| Cause probable | Arrêt du site `AlpesNet-Sonde`, entraînant le retrait des URL du groupe HTTP et l’échec de la sonde sur le port 8080 |
| Niveau de confiance | **Élevé sur la cause technique** ; limité sur l’auteur et les heures exactes des commandes |
| Action recommandée | Si l’arrêt n’est pas prévu, remettre uniquement le site concerné en état `Started`, vérifier HTTP local et distant, contrôler la sonde et observer la stabilité ; rechercher ensuite pourquoi l’arrêt a été demandé |

## 3. Chaîne de preuves

| Preuve | Ce qu’elle établit | Ce qu’elle n’établit pas seule |
| --- | --- | --- |
| PowerShell : `Stop-Website`, puis `Stopped` | Le site a été arrêté dans le cadre du test | Heure exacte et auteur de la commande |
| Kibana : HttpService, code 115, 14:18:46.509 | Les URL d’un groupe HTTP ont été supprimées avant le `pending` | Que cet événement provient nécessairement de la seule commande visible |
| Grafana : IIS à 0, Nginx à 1, collecte Windows à 1 | Le défaut est ciblé sur IIS ; la supervision générale reste disponible | Cause exacte de l’échec HTTP |
| Prometheus : `pending`, puis `firing` | La condition configurée a persisté plus d’une minute | Cause technique de la panne |
| `alert-receiver` : `firing`, puis `resolved`, HTTP 200 | Les notifications ont été livrées et la résolution transmise | Disponibilité fonctionnelle du site pour un utilisateur |
| PowerShell `Started` et HTTP 200, puis sonde à 1 | Le service local et le contrôle distant sont rétablis | Stabilité à long terme |

La fiabilité vient de la convergence de sources différentes : commande et état local, événement système centralisé, contrôle fonctionnel distant, métriques, moteur d’alerte et notification.

## 4. Examiner les hypothèses alternatives

| Hypothèse alternative | Résultat du contrôle | Conclusion |
| --- | --- | --- |
| Panne complète de Windows Core | Collecte de l’endpoint Windows à 1 pendant le défaut | Écartée pour la période observée |
| Perte générale de la supervision | Sonde Nginx à 1 et résultats Blackbox toujours collectés | Écartée |
| Perturbation réseau propre au port 8080 | Aucun blocage réseau ni correction réseau documentés ; la reprise suit celle du site IIS | Non démontrée, moins probable que l’arrêt du site |
| URL, module ou contenu de sonde incorrect | La même sonde revient à 1 après reprise du site, sans changement de configuration attesté | Affaiblie ; non nécessaire pour expliquer l’incident |
| Saturation des ressources Windows | Pas de hausse manifeste dans les panneaux visibles | Non démontrée ; les captures ne soutiennent pas cette cause |

Une hypothèse affaiblie n’est pas déclarée impossible en dehors de la période observée. Le diagnostic retient l’explication qui correspond aux faits, prévoit le symptôme observé et disparaît après l’action corrective.

## 5. Action recommandée et contrôles après intervention

Dans le contexte du lab, l’action corrective porte uniquement sur le site de test :

```powershell
Import-Module WebAdministration
Start-Website -Name 'AlpesNet-Sonde'
Get-Website -Name 'AlpesNet-Sonde'
Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:8080/health.txt' |
  Select-Object StatusCode, Content
```

Cette commande de démarrage est une procédure à retenir ; la capture disponible montre le résultat `Started`, pas la saisie de `Start-Website`.

Après l’intervention, vérifier successivement :

1. site IIS `Started` et réponse locale HTTP 200 avec le contenu attendu ;
2. `probe_success{job="sonde_windows_http"}=1` depuis la supervision ;
3. collecte toujours présente et règle `ServiceHTTPIndisponible` inactive ;
4. notification `resolved` reçue par le canal configuré ;
5. stabilité sur plusieurs évaluations et absence de nouvel échec.

Si l’arrêt n’était pas prévu, rechercher ensuite son origine : changement d’administration, tâche planifiée, déploiement, action applicative ou événement système. Ne pas attribuer l’action à une personne sans journal d’audit correspondant.

## 6. Formulation du diagnostic pour le rapport

> Le 16 septembre 2026, la sonde HTTP du site `AlpesNet-Sonde` sur Windows Core est passée à 0 alors que l’endpoint Windows et les autres contrôles restaient disponibles. Prometheus a déclenché `ServiceHTTPIndisponible` après une minute de persistance, puis Alertmanager a transmis la notification `firing` au webhook. PowerShell montre que le site avait été arrêté avec `Stop-Website`, et Kibana conserve un événement HttpService relatif au retrait des URL HTTP avant le déclenchement. Après remise du site en état `Started`, la réponse HTTP 200 et la sonde à 1 ont été rétablies ; le webhook a reçu `resolved`. La cause probable est donc l’arrêt volontaire du site IIS. Le niveau de confiance est élevé sur cette cause technique, mais l’auteur et l’heure exacte des commandes ne sont pas établis.

## Question de fin d’étape

### Quelles preuves permettent d’affirmer que le diagnostic est suffisamment fiable pour engager une action ?

L’action proposée est proportionnée et réversible : redémarrer uniquement le site de test concerné. Elle est justifiée par plusieurs preuves convergentes :

- le site est explicitement observé `Stopped` après `Stop-Website` ;
- Windows Core reste collecté, ce qui écarte un arrêt général de la VM ;
- la sonde IIS seule échoue tandis que Nginx continue de répondre ;
- l’événement HttpService précède le `pending` et décrit le retrait des URL HTTP ;
- la remise en état du site est suivie de HTTP 200, de la sonde à 1 et de la résolution de l’alerte ;
- le webhook reçoit `firing` puis `resolved` dans cet ordre.

Ces éléments établissent le périmètre, le mécanisme probable et l’effet de l’action corrective. Ils sont suffisants pour agir sur le site IIS du lab. Ils ne sont pas suffisants pour désigner l’auteur de l’arrêt ou modifier d’autres composants.

## Point de contrôle

- [x] Les observations sont séparées des suppositions.
- [x] L’hypothèse principale a été confrontée à plusieurs sources.
- [x] Les hypothèses alternatives ont été examinées.
- [x] La cause probable et le niveau de confiance sont explicités.
- [x] L’action recommandée correspond au périmètre démontré.
- [x] Les limites du diagnostic sont conservées dans le rapport.

[Chronologie corrélée](correler-metriques-sondes-journaux.md) · [Hypothèses](formuler-verifier-hypotheses.md) · [Sommaire de l’itération](index.md)

[Suite — Vérifier le retour à la normale](verifier-retour-normale.md)
