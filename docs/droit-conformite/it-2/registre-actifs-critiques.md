# Travail en autonomie — Registre des actifs critiques

## Objectif et cadre de la séance

Produire un registre des actifs critiques d'**ÉnergieAlp**, justifier les cotations et proposer de premières remédiations. Le formateur est absent pendant la production : aucun choix n'est validé au fil de l'eau. Le débrief collectif de l'après-midi servira à corriger le travail et à comparer le registre à l'exemple du formateur.

**Statut : proposition pédagogique V0 du 15 octobre 2026, à discuter au débrief.** Les faits proviennent du [dossier entreprise](../annexes/dossier-entreprise-energiealp.md), sections 2 à 5. Les notes et les actions ci-dessous sont proposées, sans audit technique ni validation métier. Le SCADA est traité comme un actif ; son fonctionnement technique n'est pas approfondi.

## 1. Méthode et lien avec NIS2

La [directive (UE) 2022/2555, article 21](https://eur-lex.europa.eu/eli/dir/2022/2555/oj?locale=fr) traite notamment de l'analyse des risques, de la continuité, des fournisseurs, de la gestion des actifs et des accès. **Elle n'impose pas un modèle unique de tableau ni cette échelle de cotation.** Le présent registre constitue un support de travail pour ces exigences ; il ne démontre ni le statut juridique d'ÉnergieAlp ni sa conformité au droit national applicable.

Chaque entrée contient un identifiant stable, son rôle, les données, le responsable, les dépendances connues, une cotation **C/I/D/T** et une justification. L'inventaire est ici au niveau des services : les instances, équipements, versions et emplacements précis restent à recenser.

### Échelle de travail

L'exemple fourni mentionnait « Eloquant » : le périmètre est ici **ÉnergieAlp**. Les critères d'intégrité mélangent fréquence de revue et besoin de protection ; ils sont reformulés en impacts pour permettre une cotation cohérente. Les tolérances de disponibilité ci-dessous explicitent les intervalles manquants de l'exemple. Ces adaptations sont à faire valider au débrief.

| Note | Confidentialité (C) | Intégrité (I) : impact d'une altération | Disponibilité (D) : interruption maximale tolérable proposée | Traçabilité (T) : besoin de preuve |
| --- | --- | --- | --- | --- |
| 1 — Faible | Public | Impact négligeable | Plus de 7 jours | Pas de besoin particulier identifié |
| 2 — Moyen | Interne, ensemble des collaborateurs | Impact limité, correction différable | Plus de 24 h et jusqu'à 7 jours | Actions des utilisateurs |
| 3 — Élevé | Limité aux services habilités | Impact métier important | Jusqu'à 24 h, interruption non nulle | Actions des administrateurs, en complément des utilisateurs |
| 4 — Critique | Personnes explicitement autorisées | Impact majeur sur le service ou les décisions | Aucune interruption acceptable selon le besoin métier | Ensemble des actions utilisateurs et administrateurs |

**Criticité globale = maximum de C, I, D et T**, sans moyenne : un besoin critique ne doit pas être masqué. Conserver les quatre notes pour savoir pourquoi un actif est critique. Ce choix prudent produit plusieurs notes globales de 4 ; l'ordre des remédiations repose ensuite sur l'exposition et les conséquences métier. D4 exprime un besoin, sans prouver une disponibilité réelle de 100 %. Les durées précises et objectifs de reprise restent à confirmer avec les métiers.

## 2. Registre proposé

Toutes les notes sont **provisoires**. Les responsables explicitement indiqués dans le dossier sont repris ; les autres attributions sont signalées comme proposées.

| ID / actif | Service et données | Responsable / dépendances connues | C | I | D | T | Globale |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EA-01 — SCADA / supervision réseau | Télésurveillance, télécommande ; états, mesures, commandes | Responsable Production ; GridSoft éditeur/intégrateur ; accès distant via EA-05 | 3 | 4 | 4 | 4 | **4 — Critique** |
| EA-02 — Compteurs communicants | Relève ; consommations, identifiants, adresses | Responsable métier à désigner ; Production proposée ; maintenance RéseauTech | 3 | 3 | 3 | 3 | **3 — Élevé** |
| EA-03 — CRM / facturation | Contrats, relation client, factures ; identité, adresse, IBAN, historique | DSI ; hébergement partiel CloudPeak Americas | 4 | 4 | 4 | 4 | **4 — Critique** |
| EA-04 — Plateforme data analytics | Analyse et prévision de charge ; consommations agrégées et individuelles | DSI ; hébergement CloudPeak Americas | 3 | 4 | 3 | 3 | **4 — Critique** |
| EA-05 — VPN technicien | Accès distant à la supervision ; identifiants et journaux de connexion | DSI ; techniciens itinérants et RéseauTech ; accès à EA-01 | 4 | 4 | 3 | 4 | **4 — Critique** |

### Justification traçable des cotations

| ID | Raisonnement C / I / D / T | Source et limites à lever |
| --- | --- | --- |
| EA-01 | **C3** : informations techniques réservées aux équipes habilitées. **I4** : une commande ou un état altéré peut affecter l'exploitation électrique. **D4** : supervision continue exigée. **T4** : retracer commandes, consultations et interventions pour attribuer les actions. | Dossier §2 et §5. C/I/T sont une analyse proposée ; conséquences précises et possibilités de fonctionnement dégradé à confirmer avec Production. |
| EA-02 | **C3** : consommations et adresses permettent un rattachement aux clients. **I3** : altérations susceptibles de fausser les relevés exploités par le SI. **D3** : tolérance de 24 h proposée pour la relève, sans assimiler une panne de relève à une coupure électrique. **T3** : attribuer consultations et changements administratifs. | Dossier §2 et §3. Délai de relève et flux vers CRM/analytics à confirmer ; aucune interruption tolérable n'est donnée pour cet actif. |
| EA-03 | **C4** : IBAN et dossiers clients nécessitent des habilitations nominatives. **I4** : altération massive de contrats ou de facturation susceptible d'affecter le service à grande échelle. **D4** : continuité du SI clientèle explicitement exigée. **T4** : attribuer modifications, accès et opérations de facturation. | Dossier §2, §3 et §5. Granularité des droits, impact financier et couverture réelle des journaux non documentés. |
| EA-04 | **C3** : consommations individuelles à réserver aux équipes habilitées ; agrégation ne prouve pas anonymisation. **I4** : prévisions altérées susceptibles de dégrader les décisions de charge. **D3** : reprise sous 24 h proposée en l'absence de tolérance métier donnée. **T3** : attribuer traitements, accès et modifications administratives. | Dossier §2 et §3. I4 est une hypothèse prudente : dépendance des décisions d'exploitation aux prévisions à vérifier ; pas de commande directe du SCADA établie. |
| EA-05 | **C4** : secrets d'accès à réserver individuellement. **I4** : configuration ou habilitations altérées susceptibles d'ouvrir un accès indu à la supervision. **D3** : une panne bloque l'accès distant ; continuité locale et délai de 24 h à confirmer. **T4** : attribuer connexions et actions privilégiées dans les systèmes cibles. | Dossier §2 à §5. Absence de MFA établie ; absence de journaux non établie. Les journaux VPN seuls ne prouvent pas les actions sur le SCADA. |

## 3. Complétude : ce qui reste à rechercher

Le dossier affirme que le registre existant est incomplet, mais **ne le fournit pas** : impossible de désigner un actif comme absent de ce registre ou d'affirmer qu'aucune cotation n'existe déjà.

| Périmètre à rapprocher de l'inventaire existant | Information ou preuve à demander |
| --- | --- |
| Postes sources et disjoncteurs, mentionnés au §2 | Liste des équipements et sites, identifiants, responsable, rattachement au SCADA ; sous-registre terrain à qualifier |
| Compteurs, CRM, analytics, VPN et SCADA | Réconciliation des cinq entrées avec l'inventaire, instances, versions, cycle de vie, sites et hébergements |
| Comptes prestataires GridSoft et RéseauTech | Comptes nominatifs, droits, actifs accessibles, dates d'expiration, approbations et revues |
| Hébergement CloudPeak | Répartition exacte CRM/cloud, régions, accès administratifs, sous-traitants, responsabilités et engagements |
| Sauvegardes, identité, réseau, postes techniciens et collecte des journaux | Vérifier leur existence et leurs dépendances ; créer des entrées si confirmés. Leur absence du dossier ne prouve pas leur absence réelle. |

Les prestataires sont ici des dépendances ; leurs contrats et accès devront être reliés aux identifiants des actifs. Le registre interne complet doit rester accessible aux personnes habilitées ; les copies destinées à une présentation publique doivent être anonymisées.

## 4. Premiers écarts et remédiations

Les renvois à NIS2 servent de **repères d'analyse**. Une lacune documentaire ne suffit pas à conclure à une violation juridique. Priorités et délais sont proposés à compter de la validation du plan, sans remédiation exécutée.

| ID / actifs | Constat et statut | Repère NIS2, art. 21 §2 | Action proposée / responsable / cible | Preuve attendue |
| --- | --- | --- | --- | --- |
| E01 / tous | Registre incomplet : **fait du dossier** ; actifs manquants non identifiés | i — gestion des actifs | **P1, sous 30 jours** : rapprocher inventaires, terrain et cloud ; DSI avec Production, coordination RSSI proposée | Registre versionné, rapprochement et exclusions justifiées, responsables désignés |
| E02 / tous | Qualification formelle existante : **non documentée**, à vérifier | a, i — risques et actifs | **P1, sous 30 jours** : récupérer les cotations existantes puis faire arbitrer C/I/D/T et les tolérances par les responsables métiers | Notes justifiées, auteur, date, validation et prochaine revue |
| E03 / EA-05, EA-01 | VPN sans MFA : **fait du dossier**, accès à la supervision | j — authentification selon les besoins | **P1, étude sous 7 jours** : DSI, avec Production et RSSI, préparer MFA, tester compatibilité et retour arrière ; déployer en fenêtre validée | Tests d'accès autorisé/refusé, MFA, continuité et retrait des exceptions temporaires |
| E04 / EA-01, EA-05 | Accès GridSoft et RéseauTech à la demande sans stratégie ni revue périodique documentée : **fait du dossier** | d, i — fournisseurs et accès | **P1, sous 15 jours** : DSI et Production, coordination RSSI proposée ; recenser, approuver, limiter dans le temps et revoir les accès | Liste compte–droit–actif–approbateur, expirations et compte rendu de revue |
| E05 / EA-03, EA-04 | Analyse de risque cloud non formalisée et absence de contrat : **faits du dossier** | a, d — risques et chaîne d'approvisionnement | **P1, lancement sous 7 jours** : DSI, RSSI et fonction juridique à mobiliser ; analyser accès, localisation et dépendances, formaliser responsabilités et garanties | Analyse datée, décision, contrat et engagements ; aucun transfert aux États-Unis présumé |
| E06 / EA-01, EA-03 à EA-05 | Reprise, sauvegardes et couverture des traces : **non documentées**, absence non démontrée | b, c, f — incidents, continuité et évaluation | **P2, sous 30 jours** : DSI et Production collectent les procédures et résultats existants, puis planifient les tests manquants | Restauration testée, délais mesurés et traces attribuables ; écarts résiduels enregistrés |

**Contraintes à respecter :** interventions sur la supervision et le SI clientèle en fenêtres validées, la nuit et hors pics, sauf urgence de sécurité avérée. Seul le RSSI peut valider une dérogation. Le prestataire apporte les éléments attendus ; le responsable interne conserve la responsabilité du suivi.

## 5. Livrable à conserver et débrief

Conserver cette V0, la référence du dossier, les décisions de cotation, les questions ouvertes et le plan d'écarts. Pour chaque ligne, compléter ensuite : emplacement précis, version, état du cycle de vie, auteur, date de revue, validation métier et référence de preuve. Prévoir une revue après changement significatif et une périodicité à décider avec le RSSI.

Au débrief : comparer l'échelle adaptée à celle du formateur, discuter I4 d'EA-04 et les D3 proposés, identifier les actifs réellement manquants à partir de l'inventaire existant, puis produire une V1 avec l'historique des arbitrages. **Aucune validation du formateur, exécution de remédiation ni conformité n'est attestée à ce stade.**

[Sommaire de l'itération](index.md) · [Module](../README.md) · [Pense-bête](../../pense-bete/glossaire/droit-conformite/it-2.md)
