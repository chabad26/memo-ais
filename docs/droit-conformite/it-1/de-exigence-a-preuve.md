# De l'exigence à la preuve : méthode, statut juridique et modèle de matrice

!!! info "Cadrage corrigé — exercice fondé sur le ReCyF"
    Le ReCyF v2.5 du 17 mars 2026 est le référentiel principal demandé pour l’exercice. Les articles NIS2 ci-dessous restent les correspondances juridiques. Voir la [matrice ReCyF et ses mesures précises](../it-2/debrief-matrice-cloud-act-politique-securite.md#32-referentiel-principal-de-lexercice-recyf). Les cotations C/I/D/T sont une méthode pédagogique locale, pas une échelle imposée par le ReCyF. Le recensement doit couvrir toutes les activités, services et SI (1.1-EI/EE), avec revue au moins annuelle (1.3-EI/EE), cartographie (5.A.1-EI/EE) et analyse des risques en hypothèse EE (16.2-EE).


**Module : Droit et conformité — Itération 1, activité 1.2 — 3 h 30 — Présentiel.**

## Objectif

Transformer une obligation en contrôle vérifiable, argumenter le statut juridique d'ÉnergieAlp et renseigner une première matrice qui servira dès le jour 2.

À lire avant la séance : [dossier entreprise ÉnergieAlp](../annexes/dossier-entreprise-energiealp.md) et [Comprendre la conformité réglementaire](comprendre-conformite-reglementaire.md).

!!! note "Statut des éléments"
    Les exemples sont préparatoires. Les écarts issus du dossier sont des faits du scénario fictif, sans vérification opérationnelle. La qualification proposée ci-dessous est un raisonnement documentaire ; aucun résultat de simulateur ni audit réel n'est présenté comme obtenu.

## 1. Déroulement fourni

| Étape | Travail |
| --- | --- |
| 1 | Méthode générale : source → exigence → applicabilité → contrôle/dispositif → preuve → état → écart → action. Examiner les preuves exploitables et leur traçabilité : qui, quand, comment |
| 2 | Introduire la matrice d'applicabilité, fil rouge du module : qualifier et justifier chaque exigence, au lieu de recopier tous les articles |
| 3 | **Activité en groupe :** utiliser le simulateur NIS2 pour qualifier ÉnergieAlp, argumenter le statut et en déduire les principales obligations. Repérer aussi la question OIV/LPM, sans l'approfondir |
| 4 | Construire un premier modèle de matrice NIS2, avec les colonnes de la méthode et quelques exemples. Le formateur présente un exemple au débrief ; compléter le gabarit à partir du jour 2 |

La durée totale est de **3 h 30** ; la consigne ne fixe pas de durée par étape.

## 2. De l'exigence à la preuve

| Maillon | Question à résoudre | Exemple pédagogique : accès VPN |
| --- | --- | --- |
| **Source** | Quel texte, article, version et statut juridique ? | Directive NIS2, article 21, paragraphe 2, point j ; modalités françaises à vérifier |
| **Exigence** | Quel résultat est attendu ? | Examiner la nécessité d'une authentification multifacteur adaptée au risque |
| **Applicabilité** | Pourquoi cette exigence concerne-t-elle ce périmètre ? | Accès distant aux systèmes de supervision par les techniciens et un prestataire |
| **Contrôle / dispositif** | Comment obtenir et vérifier ce résultat ? | Prévoir configuration MFA, règles d'accès et essais de connexion |
| **Preuve** | Quel élément démontre le fonctionnement du contrôle ? | Configuration exportée et résultats datés d'essais, à recueillir |
| **État** | Que peut-on conclure à partir des éléments disponibles ? | Écart déclaré dans le scénario ; efficacité du futur dispositif non vérifiable |
| **Écart** | Que manque-t-il par rapport au résultat attendu ? | Le dossier indique un VPN sans MFA |
| **Action** | Qui corrige, pour quand et avec quelle validation ? | DSI ; déploiement planifié en fenêtre validée, essais et retour arrière ; étude sous 7 jours après validation du plan |

Le contrôle est une vérification, par exemple tester un refus d'accès. Le dispositif est le moyen mis en place, par exemple le MFA. La preuve est le résultat conservé : une intention de déploiement ne démontre pas que le dispositif fonctionne.

### Une preuve exploitable

Une preuve doit permettre de retrouver le contrôle réalisé, d'en comprendre le périmètre et d'évaluer la conclusion. La traçabilité fait partie de sa valeur.

| Élément | Ce qu'il peut étayer | Limite à expliciter |
| --- | --- | --- |
| Capture d'écran | État affiché d'un paramètre ou résultat visible | Une capture isolée ne prouve ni la configuration de tous les systèmes ni le comportement réel |
| Fichier de configuration | Paramètres du composant et version observée | Vérifier qu'il s'agit du fichier effectivement chargé ; distinguer export réel et modèle |
| Journal d'événements | Événement daté, source et résultat | Définir la période, les filtres et la fiabilité de l'horodatage ; l'absence d'événement n'est pas une preuve générale d'absence d'incident |
| Rapport de test | Étapes, résultat attendu et résultat constaté | Documenter le contexte et les cas testés ; un test réussi reste limité à son périmètre |
| Document approuvé | Décision, responsabilités ou procédure adoptée | Ajouter une preuve d'application pour conclure sur le fonctionnement opérationnel |

**Exemple :** une capture « MFA activé » étaye un paramétrage. Des essais montrant une connexion autorisée avec le second facteur et refusée sans lui étayent le comportement sur les comptes testés. Aucun de ces éléments n'a été recueilli pour ÉnergieAlp dans cette fiche.

### Fiche de traçabilité à utiliser

La fiche suivante référence la **preuve documentaire du scénario**, pas une preuve de fonctionnement du VPN.

| Champ | Valeur renseignée |
| --- | --- |
| Identifiant de preuve | P-DOS-01 ; source des constats M-01 à M-04 |
| Producteur / collecteur | Producteur : dossier pédagogique fourni ; auteur non identifié. Reprise documentaire dans le mémo ; aucun collecteur technique mandaté |
| Date et heure | Relecture : 15 octobre 2026 ; heure non consignée. Date de production et période des faits non précisées dans le dossier |
| Origine et périmètre | Annexe ÉnergieAlp, §2 à §5 ; cinq systèmes et prestataires ; versions techniques non fournies |
| Méthode | Lecture du dossier et rapprochement des constats avec les exigences ; aucun export ni test exécuté |
| Résultat et limites | Le scénario déclare VPN sans MFA, inventaire incomplet, cloud sans analyse ni contrat, accès prestataires sans revue documentée ; aucune configuration réelle inspectée |
| Conservation | [Annexe du mémo](../annexes/dossier-entreprise-energiealp.md), copie pédagogique versionnée ; originaux et droits du dossier source non documentés |
| Relecture / validation | À soumettre au débrief ; aucune validation métier ni du formateur documentée |

Conserver les originaux dans un espace contrôlé ; une empreinte aide à détecter une modification mais ne garantit pas la véracité de l'élément. Pour le mémo public, utiliser des copies anonymisées sans identifiants personnels, secrets, clés ou données clients.

## 3. Applicabilité et état : deux décisions différentes

La matrice qualifie les exigences pertinentes et justifie également celles qui sont écartées. Décomposer les articles en exigences contrôlables ; garder une trace des articles examinés et des exclusions.

| Applicabilité | Justification attendue |
| --- | --- |
| **Applicable** | Le champ et les conditions concernent le périmètre étudié |
| **Non applicable** | Une condition juridique ou factuelle exclut ce périmètre ; citer laquelle |
| **Partiellement applicable** | Une partie seulement de l'exigence ou du périmètre est concernée ; identifier précisément la partie et décomposer si possible |
| **À déterminer** | Information nécessaire manquante ; préciser la vérification à réaliser |

« Partiellement applicable » ne signifie pas « partiellement respectée ». Un VPN dépourvu de MFA ne rend pas l'exigence inapplicable. Le manque de preuve ne constitue pas non plus une exemption.

Dans une colonne distincte, indiquer l'**état de conformité** : conforme sur le périmètre vérifié, partiellement conforme, non conforme, non vérifiable ou non évalué. Pour les exemples ci-dessous, utiliser **écart déclaré dans le scénario** ou **non évalué**, sans attester une inspection réelle.

## 4. Activité en groupe — Qualification juridique

### Vocabulaire à corriger dans la consigne

Le kit emploie « entité essentielle (OSE) ». **OSE** désigne un opérateur de services essentiels dans le cadre de **NIS1**. Sous **NIS2**, les catégories sont **entité essentielle (EE)** et **entité importante (EI)**. Un ancien statut OSE peut intervenir dans la qualification, mais les termes ne sont pas synonymes. Source : [ANSSI — qualification NIS2](https://messervices.cyber.gouv.fr/conseils-cyber/directive-nis2-mon-organisation-est-elle-concernee).

### Procédure avec le simulateur

1. Ouvrir le [simulateur ANSSI fourni dans le kit](https://messervices.cyber.gouv.fr/simulateur-nis2), ou passer par [l'espace NIS2](https://messervices.cyber.gouv.fr/nis2).
2. Renseigner les faits : gestionnaire de réseau de distribution d'électricité en France, **650 salariés**, **30 M€ de CA 2025**.
3. Ne pas inventer un total de bilan, des données de groupe ou une désignation OSE/OIV. Si l'outil les demande sans permettre de poursuivre, documenter la limite et poursuivre le raisonnement juridique séparément.
4. Conserver les réponses, la date, le résultat exact et les limites de l'outil.
5. Confronter la préqualification aux textes et rédiger la justification. En cas de divergence, examiner les entrées et le périmètre avant de conclure.

| Élément du compte rendu | État renseigné au 15 octobre 2026 |
| --- | --- |
| Date, outil et adresse | Simulateur ANSSI prévu : https://messervices.cyber.gouv.fr/simulateur-nis2 ; **non exécuté**, aucune date d’utilisation à déclarer |
| Réponses saisies et hypothèses | Aucune réponse saisie. Entrées préparées : France, distribution d’électricité, environ 650 salariés, 30 M€ de CA 2025 ; bilan, groupe et désignations non fournis |
| Résultat exact du simulateur | **Non obtenu** ; ne pas présenter la conclusion documentaire comme une sortie de l’outil |
| Articles utilisés et raisonnement | NIS2, annexe I énergie/électricité : activité visée ; art. 2 : champ ; art. 3 §1 a : entité de l’annexe I dépassant les plafonds des moyennes entreprises, effectif annoncé de 650 salariés |
| Conclusion et réserves | **EE proposée par analyse documentaire**, sous réserve du calcul de l’effectif et du périmètre juridique ; vérifier séparément le droit français. OIV non déterminé |

### Raisonnement documentaire proposé, à discuter

| Critère | Fait fourni | Argument |
| --- | --- | --- |
| Activité | Distribution d'électricité | Type d'entité visé par l'annexe I, secteur énergie / électricité |
| Taille | Environ 650 salariés | Effectif dépassant le seuil des moyennes entreprises ; vérifier le calcul sur le périmètre juridique pertinent |
| Chiffre d'affaires | 30 M€ en 2025 | Ce montant ne suffit pas à exclure l'entité : le critère d'effectif doit aussi être examiné |
| Qualification | Activité de l'annexe I et taille indiquée | **Conclusion pédagogique proposée : entité essentielle**, au regard de l'article 3, paragraphe 1, point a, sous réserve de confirmation du périmètre et des règles de calcul |

Cette conclusion est une analyse des faits fournis, **pas un résultat de simulateur ni une désignation officielle**. Sources : [directive (UE) 2022/2555, articles 2 et 3 et annexe I](https://eur-lex.europa.eu/eli/dir/2022/2555/oj) et [orientation ANSSI sur les critères](https://messervices.cyber.gouv.fr/conseils-cyber/directive-nis2-mon-organisation-est-elle-concernee). Vérifier séparément le droit français applicable à la date de l'exercice.

### Obligations à déduire

Repérer la gouvernance et la formation des dirigeants (**article 20**), la gestion proportionnée des risques (**article 21**), la notification des incidents significatifs (**article 23**) et la supervision des entités essentielles (**article 32**). Les exemples de matrice ci-dessous déclinent certains axes ; compléter l'analyse lors des séances suivantes. Référence : [texte officiel NIS2](https://eur-lex.europa.eu/eli/dir/2022/2555/oj).

### Repérer la question OIV / LPM

La criticité de l'électricité conduit à poser la question ; elle ne prouve pas un statut OIV. Celui-ci dépend d'une désignation par l'État. Le dossier n'en fournit aucune : retenir **statut OIV non déterminé**, et préciser le justificatif à rechercher. Une qualification EE ne suffit pas à conclure OIV. Source : [ANSSI — dispositif SAIV](https://cyber.gouv.fr/reglementation/cybersecurite-systemes-dinformation/directives-nis-nis2-et-dispositif-saiv/dispositif-saiv/).

## 5. Construire le gabarit de matrice

### En-tête du document

Renseigner l'organisation, le périmètre des systèmes et traitements, la qualification retenue avec ses réserves, les textes et versions, la date de revue, le rédacteur et le validateur à désigner. Garder séparés le texte européen, les textes français et le référentiel utilisé. ReCyF est présenté comme document de travail non obligatoire par défaut sur la [page ANSSI consultée le 13 octobre 2026](https://cyber.gouv.fr/reglementation/cybersecurite-systemes-dinformation/directives-nis-nis2-et-dispositif-saiv/directive-nis-2/).

### Première matrice renseignée

| ID | Source / article / version | Exigence | Périmètre | Applicabilité et justification | Contrôle / dispositif | Preuve : ID, origine, producteur, date, méthode, emplacement | État et limites | Écart | Action | Responsable | Échéance / validation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M-01 | NIS2 2022/2555, art. 21 §2 j | Authentification adaptée aux accès distants | VPN techniciens et RéseauTech vers supervision | Applicable dans l’hypothèse EE ; accès sensible, besoin de MFA à documenter | Analyse du risque, MFA et essais autorisé/refusé | P-DOS-01, annexe §4 ; auteur/date source non fournis ; lecture du 15/10/2026 ; annexe versionnée. Exports/tests à recueillir | Écart déclaré ; efficacité non vérifiable | VPN sans MFA | Étudier compatibilité, tester et déployer avec retour arrière | DSI ; Production pour impact supervision | Étude sous 7 jours après validation du plan ; déploiement en fenêtre validée ; dérogation par RSSI seul |
| M-02 | NIS2, art. 21 §2 a et d | Évaluer et maîtriser le risque fournisseur | CloudPeak : CRM partiel et analytics | Applicable dans l’hypothèse EE ; services externalisés | Analyse de risque et revue des engagements | P-DOS-01 §3–4, mêmes métadonnées ; analyse approuvée et contrat à recueillir | Écart déclaré ; aucune revue fournisseur inspectée | Analyse non formalisée, contrat absent | Identifier entité/régions/accès, traiter risques et formaliser engagements | DSI et RSSI ; appui juridique proposé | Lancement sous 7 jours après validation ; décision de traitement à faire approuver selon gouvernance à formaliser |
| M-03 | NIS2, art. 21 §2 i | Recenser et qualifier les actifs | SCADA, compteurs, CRM, analytics, VPN et dépendances | Applicable dans l’hypothèse EE ; actifs nécessaires aux services | Rapprocher inventaires, propriétaires, dépendances et criticité | P-DOS-01 §2–5 ; V0 itération 2 disponible, validation absente ; inventaire existant à demander | Écart déclaré ; complétude non vérifiable | Registre incomplet ; actifs manquants inconnus | Réconcilier la V0 avec l’existant et faire valider les notes | DSI et Responsable Production ; coordination RSSI proposée | Sous 30 jours après validation du plan ; validation par responsables métiers |
| M-04 | NIS2, art. 21 §2 i | Maîtriser le cycle des habilitations | Accès GridSoft et RéseauTech | Applicable dans l’hypothèse EE ; comptes de tiers | Octroi approuvé, durée limitée, retrait et revue périodique | P-DOS-01 §4 ; export des comptes, approbations et revue datée à recueillir | Écart déclaré ; droits effectifs non inspectés | Accès à la demande, sans stratégie ni revue périodique documentée | Recenser et faire approuver les droits ; proposer revue trimestrielle et à chaque changement de mission | DSI et Production selon système ; coordination RSSI proposée | Première revue sous 15 jours après validation ; périodicité proposée à approuver |
| M-05 | NIS2, art. 23 | Qualifier et notifier les incidents significatifs selon les délais du texte | Périmètre NIS2 retenu | Applicable dans l’hypothèse EE ; modalités nationales à vérifier | Procédure et exercice de qualification/notification | P-DOS-01 ne décrit pas la procédure ; demander version approuvée, rôles, contacts et exercice horodaté | Non évalué ; aucune preuve recueillie | Existence et efficacité non documentées ; absence non établie | Vérifier l’existant, formaliser les rôles et simuler les délais sans notification externe réelle | RSSI, direction et DSI ; répartition proposée à formaliser | Vérification sous 30 jours après validation ; procédure à faire approuver par direction |

Les échéances et rôles ajoutés sont des propositions à faire valider, sans engagement ni action exécutée. P-DOS-01 étaye les faits du scénario ; les preuves opérationnelles attendues restent à recueillir. La [V0 du registre](../it-2/registre-actifs-critiques.md) apporte un premier travail documentaire pour M-03.

Une ligne = une exigence contrôlable sur un périmètre explicite. Une même preuve peut servir plusieurs lignes si elle étaye chacune d'elles. Les justificatifs longs peuvent être référencés par identifiant plutôt que recopiés.

### Vue synthétique des contrôles à préparer

Les colonnes « dispositif », « preuve » et « action » sont des propositions. Les articles renvoient à la [directive NIS2](https://eur-lex.europa.eu/eli/dir/2022/2555/oj), dont l'applicabilité est ici l'hypothèse pédagogique EE argumentée plus haut.

| ID / source | Exigence / périmètre | Applicabilité justifiée | Contrôle / dispositif proposé | Preuve attendue, non recueillie | État / écart du scénario | Action / responsable / échéance |
| --- | --- | --- | --- | --- | --- | --- |
| M-01 — art. 21 § 2 j | Authentification adaptée / VPN | Applicable selon le risque : accès distant à la supervision ; pertinence du MFA à documenter | MFA et essais d'accès | Export, tests autorisés/refusés, collecteur et date | Écart déclaré : sans MFA ; aucun test réel | Analyser puis déployer / DSI / étude sous 7 jours après validation, puis fenêtre validée |
| M-02 — art. 21 § 2 a et d | Risques et fournisseurs / CloudPeak | Applicable : CRM et analytics externalisés | Analyse des risques et revue fournisseur | Analyse approuvée, contrats, contrôle des accès, auteur et version | Écart déclaré : analyse et contrat absents | Formaliser / DSI, RSSI pour le risque, appui juridique à désigner / lancement sous 7 jours après validation |
| M-03 — art. 21 § 2 i | Actifs / systèmes critiques | Applicable : inventaire nécessaire au périmètre étudié | Inventaire et contrôle des dépendances | Registre daté, propriétaires et validation | Écart déclaré : registre incomplet | Compléter / DSI et Responsable Production selon les actifs / sous 30 jours après validation |
| M-04 — art. 21 § 2 i | Accès / GridSoft et RéseauTech | Applicable : accès externes à maîtriser | Règles d'octroi, retrait et revue périodique | Export des habilitations et revue signée, période et méthode | Écart déclaré : pas de revue documentée | Organiser les revues / responsables des systèmes concernés / première revue sous 15 jours après validation, puis fréquence trimestrielle proposée |
| M-05 — art. 23 | Incidents significatifs / périmètre qualifié | Applicable sous réserve de qualification ; critères à vérifier | Procédure de qualification et notification | Procédure et exercice daté ; simulation explicitement identifiée | Non évalué : le dossier ne décrit pas cette procédure | Vérifier l'existant puis compléter / RSSI, rôles à formaliser / vérification sous 30 jours après validation |

Le contrat cloud doit aussi être examiné au titre du RGPD ; ne pas attribuer toutes ses clauses à NIS2. Dans la matrice finale, ajouter les métadonnées de preuve et les validations du gabarit complet.

Les actions doivent respecter la disponibilité continue et les fenêtres validées. Prévoir essais, critères de réussite et retour arrière avant un changement. Selon le dossier, seul le RSSI valide une dérogation de sécurité ; le DSI porte CRM, VPN et analytics, le Responsable Production la supervision. Une dérogation interne ne supprime pas une obligation légale.

## 6. Livrables de la journée

| Livrable demandé | Contenu minimal attendu | État à ce stade |
| --- | --- | --- |
| **Première cartographie des cadres applicables** | Textes, périmètres, justification, exclusions et questions ouvertes ; reprendre le tableau de la première séance | Tableaux documentaires renseignés dans la première fiche ; exclusions et réserves explicitées, à discuter au débrief |
| **Statut juridique argumenté** | Critères NIS2, faits, articles, résultat daté du simulateur après utilisation, conclusion EE/EI et obligations ; point OIV distinct | Raisonnement proposé ; simulateur non exécuté |
| **Modèle de matrice d'applicabilité** | Gabarit reprenant la chaîne, responsables, preuves et quelques lignes justifiées | Première matrice M-01 à M-05 renseignée ; preuves opérationnelles et validations à recueillir |

Au débrief, comparer le gabarit à l'exemple du formateur. Vérifier que chaque ligne relie une source à une exigence, justifie son applicabilité et distingue preuve attendue, preuve recueillie et conclusion. Conserver les décisions et les points à reprendre au jour 2.

[Retour à l'itération](index.md) · [Pense-bête](../../pense-bete/glossaire/droit-conformite/it-1.md)
