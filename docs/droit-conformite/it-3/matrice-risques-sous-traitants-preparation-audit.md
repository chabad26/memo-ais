# Travail en autonomie — Matrice des risques et préparation de l’audit

**Module : Droit et conformité — Itération 3 — Jour 3 — Travail en autonomie.**

## Objectif de la journée et statut

Documenter un dossier de conformité exploitable, le défendre avec une posture argumentée dans une **simulation d’audit ANSSI**, et construire un plan de remédiation pilotable : priorités, indicateurs, revues et surveillance dans le temps.

!!! note "Version documentaire V0 du 16 octobre 2026"
    Le formateur n’est pas présent pendant la production ; l’exemple de matrice et la correction seront présentés au débrief. Les réponses ci-dessous sont proposées à partir du [dossier fictif ÉnergieAlp](../annexes/dossier-entreprise-energiealp.md). Aucun entretien d’audit, retour du formateur, accès technique, contrat signé ni remédiation exécutée n’est attesté. La présente auto-évaluation est documentaire : elle ne remplace pas une vérification opérationnelle.

**Référentiel principal conservé :** [ReCyF v2.5 du 17 mars 2026, document de travail](https://messervices.cyber.gouv.fr/documents-ressources/20260317_NIS_V2_ReCyF_v2.5.pdf). Les objectifs et moyens acceptables de conformité (MAC) structurent l’exercice ; NIS2 reste la correspondance juridique. Les MAC propres aux EE sont étudiés sous l’**hypothèse documentaire EE** des jours précédents, sans désignation officielle.

## 1. Déroulement fourni

| Étape | Activité | Résultat attendu |
| --- | --- | --- |
| 1 | Relire les livrables des jours 1 et 2 et identifier les fragilités | Auto-évaluation justifiée, pièces manquantes et corrections prioritaires |
| 2 | Construire la première matrice des risques fournisseurs et les procédures associées | Risques pour GridSoft, CloudPeak et RéseauTech, liés à leur rôle et à leurs accès |
| 3 | Préparer les réponses pour l’auditeur de l’après-midi | Réponses argumentées, sources, limites et actions |
| 4 | Structurer la gestion des tiers en quatre chapitres | Qualification, contrat/sécurité/audit, revue des accès, fin de contrat |

Aucune durée détaillée n’est donnée pour cette séance. La durée et les consignes de la simulation de l’après-midi ne sont pas présumées.

## 2. Auto-évaluation des livrables des jours 1 et 2

Les références de pièces ci-dessous constituent un **index documentaire pour l’entretien**. Elles ne sont pas des preuves de déploiement. Pour chacune, conserver version, auteur, date de production, sources et limites ; auteur/date du dossier pédagogique initial non fournis.

| Pièce | Production disponible | Fragilité identifiée | Travail à faire / portée de la preuve |
| --- | --- | --- | --- |
| **D-01 — [Cartographie des cadres](../it-1/comprendre-conformite-reglementaire.md)** | Textes, champs, obligations, exclusions et sources | Conditions nationales et rôles exacts à vérifier ; absence d’information parfois déterminante | Vérifier versions et champ applicable avant conclusion juridique ; tableau documentaire disponible |
| **D-02 — [Statut juridique](../it-1/de-exigence-a-preuve.md)** | EE proposée : distribution électrique, environ 650 salariés, annexe I | Effectif de référence, groupe et périmètre juridique non confirmés ; simulateur non exécuté ; OIV inconnu | Obtenir pièces de calcul et vérification juridique ; ne pas présenter EE comme désignation ni OIV comme acquis |
| **D-03 — [Registre des actifs](../it-2/registre-actifs-critiques.md)** | Cinq services EA-01 à EA-05, C/I/D/T justifiés | Cotations non validées ; EA-04 I4 prudent, D3 provisoires, propriétaire EA-02 à désigner ; registre existant non fourni | Recenser aussi activités/services et SI supports ; rapprochement et exclusions selon 1.1 à 1.3-EI/EE et 5.A.1-EI/EE |
| **D-04 — [Matrice ReCyF / NIS2](../it-2/debrief-matrice-cloud-act-politique-securite.md#32-referentiel-principal-de-lexercice-recyf)** | Vingt objectifs et sélection explicite de MAC, contrôles et plan ; articles NIS2 en correspondance | Sélection de MAC, sans audit unitaire exhaustif sur chaque SI ; preuves techniques attendues non recueillies | Décliner par SI selon 2.C.1-EI/EE ; suivre action/responsable/échéance selon 2.C.2-EI/EE ; aucune conformité globale démontrée |
| **D-05 — [Analyse Cloud Act](../it-2/debrief-matrice-cloud-act-politique-securite.md#4-analyse-cloud-act-cloudpeak-americas)** | RC-01 à RC-05, comparaison et orientation conditionnelle | Juridiction réelle, régions, accès, clés, coûts et compatibilité inconnus ; aucune demande US ni transfert effectif prouvé | Obtenir réponses CloudPeak, analyse juridique, devis et pilote ; contractualiser et décider selon 3.B.1-EI/EE et 16.2/16.3-EE |
| **D-06 — [Politique simplifiée](../it-2/debrief-matrice-cloud-act-politique-securite.md#6-politique-de-securite-simplifiee-proposition-v0)** | Onze rubriques avec responsabilités, contrôles et références ReCyF | V0 non adoptée ; revue croisée et diffusion non documentées | Présenter pour approbation selon 2.B.3-EI/EE ; conserver décision et preuve d’application |
| **D-07 — [Procédures tiers initiales](../it-2/debrief-matrice-cloud-act-politique-securite.md#7-procedures-de-gestion-des-tiers-a-joindre-a-la-politique)** | PR-ST-01 à PR-ST-04 rédigées | Aucun dossier fournisseur complet, revue exécutée ni retrait testé | Les décliner et les rendre contrôlables dans la présente V0 ; distinguer rédaction, approbation et application |

**Fragilités à traiter en premier :** accès VPN à la supervision sans MFA ; absence déclarée de contrat et d’analyse cloud ; accès prestataires sans revue documentée ; complétude des actifs et des preuves. Une belle présentation ne compense pas l’absence de pièces opérationnelles.

## 3. Périmètre des trois prestataires

| ID | Rôle et accès connus | Actifs / responsable interne | Informations manquantes |
| --- | --- | --- | --- |
| **ST-01 — GridSoft Solutions** | Éditeur/intégrateur SCADA, France ; accès accordés à la demande sans stratégie ni revue périodique documentée | EA-01 ; Responsable Production, coordination DSI/RSSI proposée | Personnes, privilèges, canal d’accès, contrats, versions/support, journaux, engagements d’incident et de sortie ; aucun VPN GridSoft présumé |
| **ST-02 — CloudPeak Americas** | Cloud public pour partie du CRM et analytics ; filiale européenne d’un groupe américain ; aucun contrat ni analyse de risque formalisée dans le scénario | EA-03 et EA-04 ; DSI, appui RSSI/juridique proposé | Entité contractante, régions, sous-prestataires, administration, clés, continuité, réversibilité et contacts |
| **ST-03 — RéseauTech Maintenance** | Maintenance terrain/postes sources/compteurs ; VPN vers supervision sans MFA ; accès à la demande sans revue documentée | EA-02, EA-05, EA-01 ; Production pour terrain/supervision et DSI pour VPN | Intervenants, droits précis, durée, terminaux, accès physiques, contrats et traces des actions sur cible |

**Périmètre ReCyF :** 3.A.1-EI/EE concerne les relations de droit **ou de fait** : l’absence de contrat CloudPeak ne justifie donc pas son exclusion de la cartographie. Ajouter les contacts selon 3.A.2-EI/EE et les interconnexions confirmées. Le rôle de sous-traitant au sens du RGPD reste à qualifier selon les traitements ; il n’est pas automatiquement identique à celui de fournisseur informatique.

## 4. Méthode de la matrice des risques

Cette **première matrice est qualitative**. Elle relie prestation → accès/dépendance → événement redouté → conséquence → état connu → traitement → preuve et pilote. Elle n’est pas une analyse EBIOS RM achevée.

- **Impact proposé I :** 1 limité et local ; 2 perturbation métier contenue ; 3 perturbation importante ou atteinte significative aux données ; 4 atteinte majeure au service électrique, au SI clientèle ou à un ensemble sensible de dossiers. La note est un jugement documentaire à confirmer avec les métiers, sans incident avéré présumé.
- **Vraisemblance : non évaluée (NE)** tant que l’exposition, les droits et l’efficacité des mesures ne sont pas vérifiés. Aucun produit impact × probabilité n’est calculé sur des valeurs inventées.
- **P1 :** traitement ou investigation prioritaire d’un écart établi sur un accès sensible, d’un hébergement de données clients non encadré, ou d’une dépendance pouvant compromettre la continuité. **P2 :** investigation complémentaire et assurance à organiser après ces urgences. La priorité est motivée par scénario, exposition connue et gravité potentielle, pas par le seul impact.
- **Risque résiduel : non évalué** avant mise en œuvre et contrôle. Un contrat signé ou une revue de droits ne permet pas à lui seul de déclarer le risque faible. Direction et responsables métier, avec RSSI selon gouvernance à formaliser, examinent la décision de risque ; seul le RSSI valide une dérogation de sécurité selon le dossier.

La criticité C/I/D/T d’un actif est un besoin de protection ; elle ne donne ni la vraisemblance d’un scénario fournisseur ni sa priorité automatique. Les périodicités et échéances proposées ci-dessous sont locales, distinctes des minima explicitement cités du ReCyF.

### 4.1. Première matrice renseignée

Les identifiants **RC-01 à RC-05** sont conservés depuis l’analyse Cloud Act ; **RG** et **RT** complètent les scénarios GridSoft et RéseauTech. **V = NE** et **résiduel = NE** pour toutes les lignes.

| Risque / prestataire / actif | Scénario et conséquence redoutée | Fait déclencheur et limites | I / priorité justifiée | Traitement et preuve de réduction à rechercher |
| --- | --- | --- | --- | --- |
| **RG-01 / ST-01 / EA-01** | Accès tiers excessif ou devenu inutile : modification non autorisée de paramètres/commandes, exploitation perturbée | Accès à la demande sans revue documentée ; droits et canal inconnus, aucun accès administrateur généralisé affirmé | **I4 proposé ; P1** : supervision critique et défaut de revue établi | Justifier mission, limiter/expirer droits et attribuer actions ; PR-ST-03, habilitations et tests de retrait |
| **RG-02 / ST-01 / EA-01** | Mise à jour défectueuse, vulnérabilité ou support insuffisant : indisponibilité ou exposition du SCADA | Rôle éditeur/intégrateur connu ; aucune version obsolète ni mise à jour défaillante constatée | **I4 proposé ; P2** : vérifier support et maintenance, sans panne établie | PR-ST-01/02, clauses support/vulnérabilités, essais et retour arrière ; versions et rapports de maintenance |
| **RC-01 / ST-02 / EA-03, EA-04** | Demande légale à une entité sous juridiction US contrôlant les données : divulgation possible | Groupe américain et analyse absente ; ni demande ni capacité réelle d’accès au clair démontrées | **I4 proposé ; P1** : hébergement de données clients sans analyse ; probabilité non déduite de la nationalité | Examiner juridiction, contrôle et garanties ; PR-ST-01/02, analyse juridique et décision d’hébergement |
| **RC-02 / ST-02 / EA-03** | Accès fournisseur légal ou compromis à dossiers clients/IBAN : atteinte à la confidentialité | Données connues, contrat absent ; droits administratifs et chiffrement inconnus | **I4 proposé ; P1** : données sensibles pour le métier et accès à clarifier | Moindre privilège, contrôle du clair/clés, traces ; PR-ST-02/03, matrice de responsabilités et tests |
| **RC-03 / ST-02 / EA-04** | Réidentification ou usage indu des consommations agrégées/individuelles | Présence de données individuelles ; aucune anonymisation démontrée, aucun usage abusif constaté | **I3 proposé ; P2** : minimisation et finalités à qualifier | Réduire granularité et accès ; pseudonymisation ou anonymisation démontrée ; revue des jeux et finalités |
| **RC-04 / ST-02 / EA-03, EA-04** | Dépendance et sortie impossible ou trop lente : données indisponibles, service interrompu | Hébergement partiel CRM et analytics ; réversibilité/engagements non décrits, pas d’échec de restauration établi | **I4 proposé ; P1** : continuité CRM exigée avant toute migration | PR-ST-02/04, export/restauration pilote, DMIA/PRD et recette, coût et durée mesurés |
| **RC-05 / ST-02 / EA-03, EA-04** | Transfert ou accès hors EEE sans garanties appropriées si les flux sont confirmés | Régions/support inconnus ; aucun transfert US avéré | **I4 proposé ; P1 investigation** avec RC-01, sans présumer une infraction | Cartographier flux/support/sous-prestataires, vérifier mécanismes juridiques ; engagements et décision documentés |
| **RT-01 / ST-03 / EA-05, EA-01** | Compromission d’un mot de passe puis accès indu à la supervision | VPN sans MFA et absence de revue documentée déclarés ; aucune compromission observée | **I4 proposé ; P1** : voie distante et faiblesse d’authentification établies | MFA conforme au critère retenu 8.3-EE, accès nominatifs et bornés ; PR-ST-03, tests avec/sans facteur et expiration |
| **RT-02 / ST-03 / EA-02 et terrain** | Intervention physique ou configuration erronée : relevés altérés, équipement indisponible ou impact d’exploitation selon équipement | Maintenance terrain connue ; autorisations physiques et contrôle des interventions non documentés | **I4 pour postes sources, I3 pour relève proposés ; P2** : scénario à différencier, sans incident établi | Qualification intervenant, ordre de travail, autorisation/accompagnement, recette ; PR-ST-01/03, compte rendu d’intervention |

Un contrôle est une vérification, une mesure est le dispositif mis en place, et la preuve est le résultat conservé. Si une pièce montre une réduction d’exposition, mettre à jour le scénario et justifier la nouvelle appréciation ; ne pas copier une baisse de note prévue comme si elle était observée.

### 4.2. Relier la matrice au ReCyF

| Scénarios / objets | MAC retenus | Utilisation dans l’exercice |
| --- | --- | --- |
| Tous ST et leurs interconnexions | **3.A.1-EI/EE, 3.A.2-EI/EE** | Cartographie de l’écosystème et contact identifié, y compris CloudPeak sans contrat |
| Contrats et assurance fournisseur | **3.B.1-EI/EE, 3.B.2-EI/EE** | Garanties contractuelles, vérification périodique ; audit proportionné comme moyen de vérification |
| RG-01, RT-01 et accès CloudPeak | **4.4-EI/EE, 8.3-EE, 8.4-EE, 10.A.5-EI/EE, 10.A.6-EI/EE, 10.C.2-EI/EE, 10.C.4-EI/EE** | Cycle des accès, MFA distant EE avec facteur de connaissance, retrait, moindre privilège et revues au moins annuelles des comptes/droits |
| RG-02, RT-02 et changements | **5.A.1-EI/EE, 5.B.3-EI/EE, 5.B.4-EI/EE, 6.3-EE, 6.4-EI/EE** | Ressources/versions, avis et correction selon exposition ; accès physiques au besoin et externes accompagnés ou autorisés |
| RC-04, incidents et crise fournisseur | **12.3-EI/EE, 13.2-EI/EE, 13.4-EE, 13.6-EE, 14.4-EI/EE** | Qualification, test de restauration au moins annuel, DMIA/PRD et plans EE, annuaire des parties prenantes |
| Analyse, suivi et audit | **2.C.1-EI/EE, 2.C.2-EI/EE, 16.2-EE, 16.3-EE, 16.4-EE, 17.2-EE, 17.4-EE, 17.5-EE** | Analyse par SI, plan/pilote/échéance, décision sur résiduel, réexamen des risques, rapport et correction des constats |

Référence : [ReCyF, p. 10–14, 15, 18, 20–21, 24, 26–28 et 30–33](https://messervices.cyber.gouv.fr/documents-ressources/20260317_NIS_V2_ReCyF_v2.5.pdf). Les MAC sélectionnés sont des repères de contrôle, pas une déclaration de conformité ni un audit exhaustif de tous les moyens du référentiel.

## 5. Procédure fournisseurs — quatre chapitres

Cette version **précise PR-ST-01 à PR-ST-04 du jour 2**, sans prétendre à une approbation ni à une application. Les points de contact à obtenir restent des rôles, sans identité ou numéro fictif.

### PR-ST-01 — Qualification avant contractualisation

**Déclencheurs :** nouveau fournisseur, renouvellement, changement d’hébergement, mission ou accès. **Pilote :** DSI ou Production selon prestation ; RSSI pour analyse, appui juridique à désigner.

1. Enregistrer ST, service, actifs EA, données, interconnexions et responsable interne ; obtenir au moins un contact technique et un contact incident utilisable.
2. Définir criticité de la prestation et des accès : lecture/écriture/administration, distant/physique, permanents/temporaires ; vérifier sous-prestataires et lieux d’intervention.
3. Examiner juridiction, contrôle de l’entreprise et des données, localisation et accès support ; vérifier le périmètre exact d’une éventuelle qualification SecNumCloud. Ni siège français ni nationalité américaine ne suffisent à conclure seuls.
4. Recueillir garanties proportionnées et pièces : support/correctifs pour GridSoft ; entité/régions/clés/continuité pour CloudPeak ; intervenants/terminaux/accès pour RéseauTech.
5. Compléter les scénarios de risque et proposer accord, accord conditionnel ou refus selon les compétences de décision à formaliser. Tout manque conserve un responsable et une échéance ; une dérogation de sécurité RSSI ne remplace pas une obligation légale.

**Sortie vérifiable :** fiche qualifiée avec pièces, réserves, risques et décision attribuée/datée. **Contrôle :** vérifier chaque champ et le lien ST → EA → risque ; l’absence de pièce ne devient pas une garantie.

### PR-ST-02 — Clauses de sécurité et d’audit

**Déclencheurs :** engagement, régularisation CloudPeak ou évolution de prestation. **Pilote :** responsable interne avec appui juridique/RSSI proposé.

- Définir périmètre, responsabilités partagées, données et accès autorisés ; sous-prestataires et conditions de changement ; règles de maintenance et vulnérabilités selon la prestation.
- Prévoir signalement d’incident au contact interne, éléments utiles, coopération et préservation des preuves. Fixer un délai contractuel compatible avec le circuit de notification de l’entité ; **aucun délai contractuel n’est présenté comme déjà convenu**.
- Définir continuité, sauvegardes, restauration, réversibilité, formats/coûts de sortie, restitution et effacement sous réserve des obligations de conservation.
- Prévoir le droit de contrôle/audit : périmètre, pièces, préavis et cas urgents, auditeur autorisé, confidentialité, règles d’intervention, rapport et suivi des corrections. Adapter les tests aux contraintes de production ; aucun scan ou test d’intrusion sans mandat ni périmètre approuvé.
- Définir engagements de sécurité mesurables et vérification périodique. Selon les faits, traiter séparément les clauses RGPD et mécanismes de transfert nécessaires.

**Sortie vérifiable :** contrat signé et annexes reliés à ST/EA/risques. **Contrôle :** revue clause par clause des obligations retenues et du plan d’assurance ; l’audit fournisseur ne se réduit pas à collecter un certificat hors périmètre.

### PR-ST-03 — Octroi, revue et audit de l’accès

**Déclencheurs :** demande de mission, changement de droit, revue périodique ou incident. **Pilote :** DSI pour accès logiques, responsable du système pour approbation ; Production pour supervision/terrain.

1. Demande nominative précisant mission, actif, besoin de droits, début/fin, terminal et fenêtre ; approbation par responsable habilité avant configuration.
2. Configurer moindre privilège, durée, MFA distant approprié à l’hypothèse EE et compte d’administration dédié si administration ; pour 8.3-EE, vérifier au moins un facteur de connaissance. En cas d’impossibilité technique, justifier et traiter le risque selon le référentiel et les règles de dérogation.
3. Tester accès autorisé et refus hors périmètre/sans facteur/après expiration ; rapprocher les connexions des actions sur cible. Les journaux VPN seuls ne prouvent pas toutes les opérations sur le SCADA.
4. Revue locale proposée **trimestrielle**, et après changement de mission, départ ou incident ; les MAC 10.A.6-EI/EE et 10.C.4-EI/EE prévoient au moins une revue annuelle. Comparer comptes/droits aux missions, supprimer ou corriger les anomalies et conserver la décision.
5. Vérifier la prestation selon 3.B.2-EI/EE : examen documentaire, entretiens et contrôles techniques mandatés selon risque ; rapport avec constats, limites, action, responsable et échéance ; recontrôle avant clôture.

**Sortie vérifiable :** approbations, export anonymisé, résultat des tests, revue et rapport. Pas de secret, clé, donnée client ou identité réelle dans le mémo public.

### PR-ST-04 — Fin de contrat, mission ou accès

**Déclencheurs :** fin/rupture, départ d’intervenant, mission terminée ou suspension nécessaire. **Pilote :** responsable interne, DSI/Production selon système ; RSSI si incident.

1. Préparer le transfert de service et les données/configurations à restituer ; tester reprise et réversibilité avant fermeture d’une dépendance essentielle.
2. Révoquer comptes, sessions, clés d’API, certificats et accès distants/physiques concernés ; vérifier les secrets partagés s’ils existent et leur renouvellement adapté. Ne pas affirmer leur présence sans inventaire.
3. Tester le refus de l’ancien accès et contrôler les dépendances pour éviter d’interrompre une autre prestation encore autorisée.
4. Faire restituer données/supports/matériels ; demander preuve d’effacement appropriée et couvrant copies/sous-prestataires, selon contrat et obligations de conservation. Distinguer déclaration d’effacement et vérification effectivement possible.
5. Clore seulement après recette, retraits testés, décision de conservation et mise à jour des registres/risques. En cas d’incident, préserver les preuves et activer le circuit approprié avant destruction.

**Sortie vérifiable :** procès-verbal de sortie, résultats d’accès refusé, restitution/effacement et risques restant ouverts avec décision. La désactivation d’un compte seule ne démontre pas la sortie complète du prestataire.

## 6. Plan de remédiation et pilotage proposé

**J = approbation future de ce plan.** Les fenêtres, tests, critères de réussite et retour arrière s’appliquent avant modification de supervision ou SI clientèle ; nuit/hors pics sauf urgence de sécurité avérée. Aucune action n’est marquée « faite » sur le seul fondement de sa rédaction.

| Action / risque | Priorité / pilote proposé | Échéance locale | Preuve et condition de clôture |
| --- | --- | --- | --- |
| **AS-01 — RT-01, RG-01, RC-02** | P1 ; DSI/Production, coordination RSSI | Inventaire des accès J+7, première revue J+15 | Liste réconciliée, approbations, retraits/expirations testés ; canal GridSoft clarifié |
| **AS-02 — RT-01** | P1 ; DSI avec Production/RSSI | Étude MFA et secours J+7 ; déploiement après essais en fenêtre validée | Facteur de connaissance et second facteur vérifiés, refus/continuité testés, exceptions bornées et motivées |
| **AS-03 — RC-01, RC-02, RC-05** | P1 ; DSI/RSSI, juridique proposé | Collecte et contractualisation lancées J+7 ; orientation J+30 | Réponses CloudPeak, analyse, engagements signés et décision documentée ; résiduel réévalué sur pièces |
| **AS-04 — RC-04** | P1 ; DSI et métiers | Objectifs et plan de test J+30 ; recette avant sortie/bascule | DMIA/PRD validés ; export/restauration et retour arrière mesurés, sans promesse de zéro interruption non prouvée |
| **AS-05 — RG-02, RT-02, RC-03** | P2 ; Production/DSI et métiers | Dossiers techniques et données J+30 | Support/versions et maintenance qualifiés, accès physiques vérifiés, données analytics nécessaires justifiées |
| **AS-06 — tous ST** | P2 ; RSSI, responsables internes et direction | Plan de vérification/audit et revue J+30 | Fiches, contacts, clauses, revue des risques, mandat et contrôles planifiés ; preuves d’application à collecter |

### Indicateurs à renseigner, sans valeurs inventées

| Indicateur / calcul | Source / responsable / fréquence proposée | Cible locale et alerte |
| --- | --- | --- |
| **K-01 — Couverture fournisseurs** : dossiers qualifiés avec contact, EA et risques / fournisseurs recensés | Registre ST ; DSI/Production ; mensuel | Cible 100 % du périmètre réconcilié ; trois prestataires décrits, complétude inconnue |
| **K-02 — Accès revus** : comptes/droits tiers revus dans la période / comptes/droits tiers recensés | Revue et exports ; DSI ; mensuel, revue trimestrielle | Cible 100 % ; dénominateur inconnu = **non calculable**, pas 100 % |
| **K-03 — Couverture MFA distante** : accès distants concernés vérifiés avec MFA conforme au critère retenu / accès concernés recensés | Paramètres et essais ; DSI ; après changement et mensuel | Cible 100 % ou impossibilités dûment traitées à part ; distinguer protégés et exceptions. Valeur actuelle non mesurée |
| **K-04 — Actions P1 en retard** : nombre P1 dépassant échéance approuvée ; taux = ce nombre / P1 ayant une échéance approuvée | Plan AS ; RSSI ; hebdomadaire | Cible 0 en retard ; pas de date approuvée = décision attendue, pas action réputée à l’heure |
| **K-05 — Garanties fournisseurs vérifiées** : prestations avec engagements sécurité/audit et revue documentée / prestations concernées | Contrats, rapports ; responsable interne ; trimestriel | Cible 100 % ; contrat CloudPeak absent selon scénario, taux global non établi |
| **K-06 — Reprise vérifiée** : scénarios prioritaires testés et acceptés / scénarios prioritaires planifiés | Recettes ; DSI/métiers ; chaque test et revue trimestrielle | Cible 100 % du programme ; absence de test = non démontré. Restauration au moins annuelle selon 13.2-EI/EE |

**Valeur initiale de tous ces indicateurs : non mesurée ou non calculable selon les pièces disponibles.** Les cibles sont proposées et ne constituent ni un résultat ni une prescription chiffrée générale du ReCyF.

**Modalités de surveillance proposées :** point hebdomadaire RSSI/DSI/Production sur P1 et obstacles ; revue mensuelle des actions et indicateurs ; revue trimestrielle des prestataires, droits et écarts ; réexamen immédiat après incident, changement d’accès, sous-prestataire ou hébergement. Revoir l’analyse des risques au moins tous les trois ans et selon événements en hypothèse EE (16.4-EE) ; les rythmes locaux plus fréquents ne remplacent pas cette analyse. Garder comptes rendus, décisions, exceptions et preuves de recontrôle. Après changement significatif, mettre à jour D-03, D-04, D-05 et D-06 si concernés.

**États du plan :** proposé → approuvé/planifié → en cours → réalisé à vérifier → clos après contrôle. Ajouter « bloqué » avec cause, pilote et prochaine décision. **Décision de risque** et **avancement de l’action** restent séparés : une action clôturée n’est pas une acceptation de tous les risques.

## 7. Réponses préparées pour l’auditeur

Structure de réponse : **conclusion limitée → pièce et périmètre → limite de preuve → action et pilote**. Les phrases suivantes sont des formulations préparées, pas des échanges déjà tenus.

| Question possible | Réponse argumentée proposée | Pièce à montrer / limite |
| --- | --- | --- |
| « Quel référentiel avez-vous utilisé ? » | « Le ReCyF v2.5 est notre base pédagogique. Nous citons objectifs et MAC ; NIS2 est la correspondance juridique. Nous conservons le statut de document de travail. » | D-04, source versionnée ; ne pas prétendre que son emploi prouve le droit national ou la conformité |
| « Pourquoi vous dites-vous EE ? » | « C’est une qualification documentaire proposée : distribution électrique et environ 650 salariés. Nous devons confirmer le périmètre de calcul et les modalités applicables. Aucun résultat de simulateur ni statut OIV n’est prouvé. » | D-02 ; réserves visibles |
| « Votre registre est-il complet ? » | « Il décrit cinq services du scénario. Il ne prouve pas un recensement complet de toutes les activités/SI. Nous demandons le rapprochement de l’inventaire et des dépendances. » | D-03, 1.1/1.3-EI/EE ; AS-06 et AS-05 selon périmètre, renvoi à la revue des actifs du jour 2 |
| « Comment avez-vous priorisé ? » | « Nous avons relié rôle, accès, événement et conséquence. Le VPN sans MFA et les lacunes cloud sont des faits ; impact proposé et priorité sont motivés. La vraisemblance et le résiduel restent non évalués. » | Matrice §4 ; pas de score inventé |
| « GridSoft utilise quel accès ? » | « Le dossier ne le précise pas. Nous connaissons des accès à la demande, pas le canal ni tous les privilèges. AS-01 doit les clarifier et les faire revoir. » | ST-01, RG-01 ; ne pas inventer VPN ou droits globaux |
| « Le VPN est-il sécurisé maintenant ? » | « Le scénario le décrit sans MFA. Nous avons proposé essais et déploiement ; aucune preuve de changement n’est recueillie. Le critère retenu 8.3-EE inclut un facteur de connaissance. » | RT-01, AS-02 ; export et essais encore attendus |
| « CloudPeak transfère-t-il aux États-Unis ? » | « Aucun transfert ni demande d’accès n’est documenté. Nous analysons juridiction, contrôle réel, flux et accès ; les scénarios RC-01 et RC-05 sont distincts. » | D-05, demandes de pièces AS-03 |
| « Comment contrôlez-vous vos fournisseurs ? » | « Nous avons rédigé qualification, clauses d’audit, revue d’accès et sortie. Leur application reste à démontrer par contrats, revues et tests. » | PR-ST-01 à 04 ; 3.A/3.B, AS-06 |
| « Qui accepte les risques résiduels ? » | « Nous proposons une décision attribuée à la direction et aux responsables métiers avec RSSI selon la gouvernance à formaliser. Le dossier habilite le RSSI seul pour une dérogation de sécurité ; ce n’est pas un pouvoir général de déroger à la loi. » | 16.3-EE, D-06 ; aucune acceptation signée |
| « Que prouvent les PDF et la politique ? » | « Ils prouvent la production documentaire et les propositions de contrôle. Ils ne prouvent pas l’adoption de la politique ni le fonctionnement des configurations. » | D-04 à D-07, versions et limites ; ne pas montrer une cible comme export réel |
| « Et si un fournisseur provoque une interruption ? » | « Nous préparons contacts, qualification/escalade, continuité, reprise et sortie testée. Les objectifs et essais ne sont pas encore validés sur preuves. » | RC-04, AS-04, 13.4/13.6-EE ; pas de restauration réussie revendiquée |
| « Comment suivez-vous dans le temps ? » | « Nous proposons des indicateurs avec dénominateur, source et pilote, des revues et des déclencheurs. Les valeurs ne sont pas mesurées ; une clôture nécessitera un recontrôle. » | Plan AS, K-01 à K-06 et comptes rendus futurs |

Une demande non couverte reçoit une réponse explicite : « information non disponible sur ce périmètre ; voici la pièce attendue, le responsable proposé et l’échéance à approuver ». Ne pas répondre « conforme » pour éviter une question ou transformer une recommandation en action déjà réalisée.

## 8. Dossier à conserver pour le débrief

- Index D-01 à D-07, versions sources et réserves ; présente matrice fournisseurs V0, plan AS et grille d’indicateurs.
- Historique des risques : scénario, actif, prestataire, fait/hypothèse, impact proposé, décision, mesure, preuve, auteur/date et prochaine revue.
- Après le débrief seulement : exemple du formateur référencé, retours reçus attribués, corrections et motifs ; conserver V0 puis V1 sans inventer de validation.
- Pour une présentation publique : copies anonymisées, sans comptes réels, adresses internes, secrets, données clients ou détails de sécurité sensibles.

**Livrable disponible :** première matrice qualitative des risques pour les trois prestataires, quatre procédures proposées et réponses préparées. **Reste à démontrer :** qualification fournisseur sur pièces, probabilité/résiduel, contrats, revues, tests, arbitrages, indicateurs mesurés et tenue effective de l’audit simulé.

## Ressources

- [Dossier entreprise ÉnergieAlp](../annexes/dossier-entreprise-energiealp.md), sections 2 à 5.
- [ReCyF v2.5 du 17/03/2026 — source officielle](https://messervices.cyber.gouv.fr/documents-ressources/20260317_NIS_V2_ReCyF_v2.5.pdf) ; [présentation et mesures — ANSSI](https://messervices.cyber.gouv.fr/nis2), consultées le 16 octobre 2026.
- [Directive NIS2](https://eur-lex.europa.eu/eli/dir/2022/2555/oj), notamment art. 21 §2 d et §3 pour la chaîne d’approvisionnement ; correspondance et qualification détaillées dans D-02/D-04.
- [Synthèse du jour 2 : matrice, cloud et politique](../it-2/debrief-matrice-cloud-act-politique-securite.md).

[Retour à l’itération](index.md) · [Module](../README.md) · [Pense-bête](../../pense-bete/glossaire/droit-conformite/it-3.md)
