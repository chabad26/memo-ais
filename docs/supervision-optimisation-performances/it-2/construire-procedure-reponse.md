# Construire la procédure de réponse

## Objectif et travail demandé

Reprendre les cinq alertes de l’[activité 1.3 — Configurer et tester les alertes](configurer-tester-alertes.md) pour permettre à un autre administrateur d’identifier l’anomalie, de vérifier son impact et d’engager une action adaptée. Cette feuille complète le **livrable L3 — Alertes et procédures de réponse**, associé à **CA-06 dans le travail demandé**.

!!! note "État des preuves — 16 septembre 2026"
    Les captures du 16 septembre attestent le cycle CPU jusqu’au retour nominal et le cycle IIS complet : arrêt, `pending`, `firing`, notification locale, reprise, `resolved` et contrôles nominaux. Les procédures ci-dessous sont rédigées pour les cinq règles ; les déclenchements des règles de collecte et de stockage, ainsi que les variations temporaires, restent à tester.

## 1. Principes d’une alerte exploitable

Une alerte doit permettre d’agir. Elle signale une condition détectée ; elle ne fournit pas nécessairement sa cause. La procédure transforme cette information en contrôles, décisions et actions vérifiables.

| Question | Information à retrouver dans le lab |
| --- | --- |
| Qu’est-ce qui est en anomalie ? | `alertname`, résumé `summary`, mesure ou résultat du contrôle |
| Où ? | `endpoint`, `instance`, `job`, puis `service` ou volume selon la règle |
| Depuis quand ? | Heure de première observation, état `pending`/`firing`, `startsAt` et heure de réception ; préciser le fuseau |
| Avec quelle criticité ? | `severity`, impact réel sur le service et urgence |
| Pourquoi intervenir ? | Risque ou gêne : perte de visibilité, service indisponible, saturation, ralentissement |
| Que vérifier ? | `description`, métriques récentes, sondes, journaux et maintenance éventuelle |
| Quelle action entreprendre ? | Annotation `action`, procédure correspondante, responsable et escalade |

`startsAt` et l’heure de réception ne prouvent pas l’heure exacte du début de la panne. Conserver la chronologie observée, sans inventer un temps de détection.

### Seuil et criticité

Le **seuil** définit une condition significative dans le contexte d’exploitation. Il se justifie par le comportement habituel, la capacité disponible, la durée et les conséquences attendues. Un pourcentage élevé ne suffit pas à conclure à un incident.

| Niveau | Signification | Application au lab |
| --- | --- | --- |
| Information | Événement intéressant, sans action immédiate | Changement attendu à conserver dans le journal ; aucune des cinq règles n’utilise ce niveau |
| Avertissement (`warning`) | Situation inhabituelle à vérifier et surveiller | Collecte, CPU, stockage ; intervenir si la situation persiste ou menace le service |
| Critique (`critical`) | Situation nécessitant une intervention rapide | Échec HTTP pendant une période où le service doit être disponible |

Ces niveaux s’adaptent à l’organisation. Une perte de collecte généralisée ou un disque sur le point de saturer peut imposer une escalade urgente même si la règle porte `warning`. Documenter cette décision ; le label ne change pas automatiquement. Dans le lab, les deux criticités utilisent le récepteur `journal-local`.

### Fausses alertes et variations temporaires

Une règle trop sensible sollicite inutilement l’administrateur ; une règle trop permissive détecte trop tard. Ajuster d’abord la compréhension de l’impact, puis le seuil et la durée. Une maintenance connue se documente ; elle ne justifie pas de masquer durablement une dégradation.

Dans Prometheus, `for` impose que la condition reste présente aux évaluations avant de passer de `pending` à `firing`. La fenêtre de calcul CPU `[2m]` est distincte de cette attente. Les annotations peuvent porter le texte d’aide et un lien de procédure. [Documentation des règles Prometheus](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/)

Un silence Alertmanager suspend les notifications correspondantes ; il ne répare pas le service et ne supprime pas la condition évaluée. [Principes Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/)

## 2. Revoir les cinq alertes

Les conditions ci-dessous reprennent le [fichier de règles du lab](../../assets/configs/supervision-optimisation-performances/it-2/prometheus/alertes.yml). Les justifications sont des choix d’exploitation à confirmer par les essais et les besoins du service.

| Alerte | Seuil et durée configurés | Criticité et justification | Informations à contrôler |
| --- | --- | --- | --- |
| `CollecteEndpointEnEchec` | `up=0` pour Linux/Windows, 2 min | `warning` : perte de visibilité persistante, sans preuve automatique d’arrêt de la VM | Endpoint, cible, job, durée, erreur dans Targets |
| `ServiceHTTPIndisponible` | `probe_success=0` et collecte de sonde `up=1`, 1 min | `critical` : service attendu indisponible ; délai court pour limiter l’impact | Endpoint, service, URL, statut/contenu attendu, collecte valide |
| `StockagePresquePlein` | Occupation > 85 % sur `/` ou `C:`, 10 min | `warning` : conserver une marge d’action ; confronter les 15 % restants aux octets libres et à la croissance | Endpoint, volume, occupation, espace libre et tendance |
| `CPUEleve` | CPU moyen > 80 %, calcul sur 2 min, persistance 2 min | `warning` : charge soutenue à examiner, pas preuve d’une panne applicative | Endpoint, CPU moyen, durée, processus et latence des services |
| `CollecteSondeEnEchec` | `up=0` pour les jobs de sonde, 2 min | `warning` : disponibilité HTTP devenue inconnue ; ne pas annoncer à tort une panne du site | Endpoint, URL, job, erreur de collecte et état de Blackbox |

### Tableau d’amélioration

Les observations non démontrées sont explicitement indiquées comme risques à vérifier. Les améliorations proposées ici sont documentaires ; elles ne modifient pas automatiquement les règles déployées.

| Alerte | Problème constaté ou risque à vérifier | Amélioration | Résultat attendu |
| --- | --- | --- | --- |
| `CPUEleve` | Pendant le test, la montée CPU a précédé l’apparition dans Alertmanager | Expliquer fenêtre de calcul, `for` et états ; relever les heures ; identifier le processus | L’opérateur distingue l’attente normale d’une rupture de transmission |
| `CollecteEndpointEnEchec` | Risque de confondre exporter inaccessible et VM arrêtée ; panne non testée | Commencer par Targets, accès VM et service exporter | Correction du composant fautif sans redémarrage global injustifié |
| `ServiceHTTPIndisponible` | Risque de confondre panne HTTP et collecte perdue ; cycle IIS et notifications attestés | Vérifier ensemble `probe_success`, `up`, réponse locale et sonde distante | Incident qualifié sur le bon service et bon périmètre |
| `StockagePresquePlein` | Le pourcentage seul n’indique pas le temps restant ; déclenchement non testé | Ajouter au diagnostic octets libres, inodes Linux et vitesse de croissance | Action proportionnée, avant saturation, sans suppression arbitraire |
| `CollecteSondeEnEchec` | Risque de déclarer le site rétabli lorsque la sonde ne fournit plus de données | Vérifier Blackbox puis le résultat HTTP après reprise de collecte | Retour de visibilité confirmé avant de conclure sur le service |

### Vérifier le comportement temporaire et le retour au nominal

Pour chaque essai, conserver la configuration utilisée, les heures, les séries observées, les états et les notifications. Tester une règle à la fois sur le périmètre du lab, puis rétablir le composant même si l’alerte ne se déclenche pas.

| Alerte | Variation temporaire à vérifier | Déclenchement soutenu et retour attendu |
| --- | --- | --- |
| `CPUEleve` | Impulsion CPU bornée ; vérifier que **l’expression calculée**, et pas seulement le stress, reste vraie moins de 2 min | Réutiliser le test de 5 min ; attendre la baisse de la moyenne, confirmer CPU habituel et `up=1` |
| `ServiceHTTPIndisponible` | Arrêt puis reprise du seul site de test IIS ; condition observée moins de 1 min | Réutiliser le test IIS de la feuille précédente ; réponse 200 avec contenu attendu, `probe_success=1` et `up=1` |
| `CollecteEndpointEnEchec` | Arrêt bref du seul exporter du lab, après identification de son service ; condition observée moins de 2 min | Maintenir l’échec au-delà de `for`, puis relancer l’exporter ; cible attendue toujours déclarée, `up=1` et métriques fraîches |
| `CollecteSondeEnEchec` | Arrêt bref de Blackbox dans le lab ; condition observée moins de 2 min | Rétablir Blackbox après déclenchement ; `up=1` pour les sondes puis contrôle de leurs résultats HTTP |
| `StockagePresquePlein` | Séries synthétiques franchissant 85 % moins de 10 min, dans un test de règles isolé | Séries au-dessus du seuil plus de 10 min puis sous le seuil ; ne pas remplir le disque réel |

**Attendu pour une variation trop courte :** aucun `firing`, avec éventuellement un passage par `pending` puis retour à `inactive`. Une impulsion entre deux collectes peut ne pas être observée. Pour le stockage, un test synthétique valide la logique ; il ne prouve pas la chaîne de notification en exploitation. Un [test unitaire Prometheus](https://prometheus.io/docs/prometheus/latest/configuration/unit_testing_rules/) peut servir à préparer ces séries ; il reste à produire et exécuter.

Après un déclenchement soutenu, vérifier les notifications `firing` puis `resolved`, les données toujours présentes et le service réellement utilisable. Pour ce lab, retenir **au moins trois évaluations consécutives nominales**, puis prolonger l’observation si l’incident était intermittent. Cette durée est un choix de validation, pas un engagement de service.

| Alerte | Variation temporaire | Déclenchement | Retour et notifications |
| --- | --- | --- | --- |
| CPU Debian | À tester | Pending et présence dans Alertmanager attestés | Inactive, disparition et CPU revenu près de zéro attestés ; notifications à compléter |
| HTTP / IIS | À tester | Arrêt du site, Pending, Firing, Alertmanager et notification `firing` attestés | Site Started, HTTP 200, sonde à 1, Inactive, disparition et notification `resolved` attestés |
| Collecte endpoint | À tester | À tester | À tester |
| Stockage | Test synthétique à préparer | Non testé | Non testé |
| Collecte sonde | À tester | À tester | À tester |

## 3. Procédures de réponse

Le responsable initial est l’administrateur du lab (`team=infrastructure`). Les destinations d’escalade ci-dessous sont des **rôles à attribuer** ; inscrire les noms, moyens de contact et délais convenus avant une exploitation réelle. Pour l’exercice, le formateur est le recours lorsqu’une intervention dépasse le périmètre maîtrisé.

À réception : relever l’heure et l’identité de l’alerte, vérifier la maintenance prévue, évaluer l’impact, préserver les éléments utiles, puis appliquer la procédure concernée. Ne pas attendre la fin du diagnostic pour signaler un impact critique.

### A. CollecteEndpointEnEchec

| Élément | Contenu |
| --- | --- |
| Nom de l’alerte | `CollecteEndpointEnEchec` |
| Situation détectée | Prometheus ne collecte plus l’exporter Linux ou Windows depuis 2 min |
| Criticité | `warning` ; urgence accrue si plusieurs cibles ou un service essentiel deviennent invisibles |
| Vérification à effectuer | Lire l’erreur dans Targets ; contrôler présence de la cible, accès SSH/console ou Windows, état de la VM, exporter, écoute réseau et filtrage |
| Première action | Identifier si l’échec concerne une cible ou toutes ; comparer l’accès à la VM et à son exporter |
| Action corrective possible | Relancer uniquement l’exporter s’il est arrêté et que la cause est comprise ; corriger adresse, service ou règle réseau erronée en conservant la configuration précédente |
| Escalade nécessaire | Administrateur système/réseau si accès perdu, panne commune, changement hors périmètre ou première correction inefficace |
| Critère de retour à la normale | Cible attendue toujours présente, `up=1`, métriques récentes et règle inactive |
| Vérification après intervention | Observer plusieurs collectes, contrôler le service hébergé, vérifier `resolved` après un `firing` reçu et consigner la cause |

### B. ServiceHTTPIndisponible

| Élément | Contenu |
| --- | --- |
| Nom de l’alerte | `ServiceHTTPIndisponible` |
| Situation détectée | Échec HTTP persistant 1 min, avec collecte de sonde valide |
| Criticité | `critical` si le site doit être disponible ; confronter au planning de maintenance |
| Vérification à effectuer | Contrôler `probe_success=0`, `up=1`, URL et contenu attendus ; tester depuis l’endpoint puis depuis la supervision ; examiner Nginx/IIS et les journaux disponibles |
| Première action | Déterminer si le site est arrêté, répond incorrectement ou est inaccessible depuis le réseau |
| Action corrective possible | Pour le test IIS, rétablir `AlpesNet-Sonde` avec `Start-Website -Name 'AlpesNet-Sonde'` ; sinon corriger le composant identifié ou revenir sur le changement fautif selon la procédure du service |
| Escalade nécessaire | Responsable applicatif et système/réseau dès impact important, dépendance défaillante ou impossibilité de rétablir dans le délai convenu |
| Critère de retour à la normale | Réponse HTTP 200 et contenu attendu, sonde `probe_success=1`, collecte `up=1`, règle inactive |
| Vérification après intervention | Confirmer depuis le chemin de supervision et par un accès fonctionnel ; surveiller latence et erreurs, vérifier `resolved` |

Les commandes du [test IIS](configurer-tester-alertes.md#6-test-2-indisponibilite-du-site-iis-sur-windows-core) se lancent sur Windows Core. Redémarrer l’ensemble d’IIS n’est pas la première action pour un seul site arrêté.

### C. StockagePresquePlein

| Élément | Contenu |
| --- | --- |
| Nom de l’alerte | `StockagePresquePlein` |
| Situation détectée | Plus de 85 % du volume `/` ou `C:` occupés depuis 10 min |
| Criticité | `warning` ; escalader rapidement si marge faible, croissance rapide ou écritures en échec |
| Vérification à effectuer | Confirmer volume, octets libres et tendance ; Linux : `df -h /` et `df -i /` ; Windows : `Get-Volume -DriveLetter C` ; identifier le producteur des données |
| Première action | Estimer le temps disponible et localiser la croissance, sans supprimer de fichiers au hasard |
| Action corrective possible | Corriger une rotation défaillante, appliquer la rétention prévue, déplacer des données identifiées ou étendre le volume selon les capacités ; vérifier les sauvegardes avant toute suppression utile au diagnostic ou au service |
| Escalade nécessaire | Responsable système/stockage et propriétaire des données si saturation imminente, extension nécessaire ou données impossibles à retirer sans décision métier |
| Critère de retour à la normale | Occupation au plus à 85 %, marge libre suffisante pour la croissance attendue, écritures fonctionnelles et règle inactive |
| Vérification après intervention | Contrôler que l’espace ne se remplit pas à nouveau, vérifier la collecte et les applications, puis `resolved` ; documenter la capacité gagnée |

### D. CPUEleve

| Élément | Contenu |
| --- | --- |
| Nom de l’alerte | `CPUEleve` |
| Situation détectée | Moyenne CPU > 80 % sur 2 min, maintenue pendant 2 min |
| Criticité | `warning` ; escalade si ralentissement important, erreurs ou indisponibilité |
| Vérification à effectuer | Lire la courbe récente, identifier le processus avec `top` sur Debian ou le moniteur de ressources adapté sur Windows ; comparer au travail prévu, aux sondes et aux journaux |
| Première action | Identifier le consommateur et son propriétaire ; distinguer test, tâche attendue et anomalie |
| Action corrective possible | Pour le test, laisser finir stress-ng ou l’arrêter par Ctrl+C dans son terminal ; sinon ajuster la tâche identifiée, sa planification ou la capacité après analyse |
| Escalade nécessaire | Responsable applicatif/système si processus critique, récidive, cause inconnue ou impact persistant ; ne pas tuer arbitrairement un processus métier |
| Critère de retour à la normale | CPU au niveau habituel et au plus à 80 %, métriques présentes, `up=1`, services utilisables et règle inactive |
| Vérification après intervention | Observer la courbe après la fenêtre de calcul, confirmer sondes et latence, vérifier `resolved`, noter le processus et l’action |

### E. CollecteSondeEnEchec

| Élément | Contenu |
| --- | --- |
| Nom de l’alerte | `CollecteSondeEnEchec` |
| Situation détectée | Prometheus ne récupère plus le résultat d’un job de sonde depuis 2 min |
| Criticité | `warning` : état du service inconnu ; escalade si perte générale de supervision |
| Vérification à effectuer | Lire Targets, contrôler Blackbox, réseau Docker, module et URL de sonde ; comparer les autres jobs |
| Première action | Sur supervision, examiner `sudo docker compose ps blackbox` puis `sudo docker compose logs --tail=50 blackbox` depuis `~/observabilite` |
| Action corrective possible | Rétablir Blackbox s’il était arrêté, ou corriger le module/adressage fautif ; refaire les contrôles de la feuille des sondes |
| Escalade nécessaire | Responsable supervision/réseau si plusieurs sondes perdues, erreur persistante ou configuration non maîtrisée |
| Critère de retour à la normale | Résultats de sonde à nouveau collectés, `up=1`, règle inactive ; vérifier séparément `probe_success` |
| Vérification après intervention | Si `probe_success=0`, appliquer la procédure HTTP ; sinon confirmer la stabilité, vérifier `resolved` et documenter la perte de visibilité |

Consulter la [configuration et le diagnostic des sondes](../it-1/creer-configurer-sondes.md) pour les commandes propres aux modules du lab.

## 4. Escalade et clôture

Escalader lorsque l’impact devient important, que le périmètre s’étend, que les compétences ou droits nécessaires manquent, que l’action présente un risque non maîtrisé ou que le délai convenu approche sans rétablissement. Fournir : alerte et cible, début observé avec fuseau, impact, métriques/journaux utiles, actions déjà tentées et résultat, hypothèses restantes et besoin précis. Ne pas transmettre de secrets dans le dossier.

La clôture demande davantage que la disparition de l’alerte : **données présentes, condition levée, service utilisable et stabilité observée**. Vérifier aussi la résolution reçue par le canal prévu. Si la cause reste inconnue après rétablissement, l’écrire et prévoir l’analyse de récidive.

## 5. Livrable L3 — Alertes et procédures de réponse

| Pièce du dossier | Contenu et emplacement |
| --- | --- |
| Configuration | [Règles, routage, récepteur et Compose](configurer-tester-alertes.md) ; conserver la version réellement déployée |
| Justification | [Seuils et criticité](definir-seuils-criticite.md), contexte d’exploitation et ajustements décidés |
| Procédures | Les cinq tableaux ci-dessus, responsables et contacts à compléter |
| Tests | Variation temporaire, déclenchement soutenu, informations affichées, retour réel au nominal et notifications pour chaque règle ; indiquer les tests synthétiques |
| Preuves | Captures datées, courbes/sondes, journaux du récepteur, heures et fuseaux, résultats attendus comparés aux résultats observés |
| Améliorations | Tableau problème/amélioration, justification des changements, validation des fichiers et nouveau test après modification |

Pour la démonstration individuelle au formateur, expliquer une règle et son seuil, retrouver la cible, dérouler sa procédure, montrer le déclenchement et le rétablissement, puis exposer les limites des preuves. Ce dossier soutient la validation de **CA-06** ; sa rédaction seule ne valide pas la compétence.

## Questions de fin d’étape

| Question | Réponse attendue |
| --- | --- |
| Une alerte seule permet-elle de savoir quoi faire ? | Pas toujours : elle décrit une condition ; une procédure précise les contrôles et décisions adaptés au contexte. |
| Quelles informations doivent l’accompagner ? | Anomalie, cible, heure/durée, criticité, impact, mesure, responsable, premiers contrôles et procédure. |
| Quelle différence entre alerte et procédure ? | L’alerte attire l’attention ; la procédure guide la vérification, la correction, l’escalade et la validation. |
| Quand escalader ? | Impact important, délai dépassé ou menacé, cause hors périmètre, droits/compétences manquants ou action risquée. |
| Comment prouver la résolution ? | Confirmer données fraîches et service fonctionnel, disparition de la condition, stabilité et notification de résolution. |

## Auto-évaluation individuelle

- [ ] Identifier une situation nécessitant une alerte.
- [ ] Justifier un seuil selon le contexte d’exploitation.
- [ ] Définir une criticité selon l’impact et l’urgence.
- [ ] Configurer une alerte et vérifier les fichiers chargés.
- [ ] Provoquer son déclenchement dans un test maîtrisé.
- [ ] Identifier l’élément concerné.
- [ ] Vérifier le retour réel à la normale.
- [ ] Expliquer les informations fournies par l’alerte.
- [ ] Construire une procédure de réponse utilisable par un autre administrateur.

Si un critère reste non acquis, reprendre l’activité correspondante avant de demander la validation. Ne cocher que ce qui peut être expliqué et démontré individuellement.

[Configurer et tester les alertes](configurer-tester-alertes.md) · [Sommaire de l’itération](index.md) · [Pense-bête](../../pense-bete/glossaire/supervision-optimisation-performances/it-2.md)

[Suite — Partir d’une alerte pour rechercher ce qui s’est produit](partir-alerte-rechercher-situation.md)
