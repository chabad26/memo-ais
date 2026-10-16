# Simulation d’audit ANSSI, plan de remédiation et fermeture du module

**Droit et conformité — Itération 3 — Présentiel.**

## Objectif et statut de la feuille

Défendre le dossier fictif ÉnergieAlp à partir de pièces identifiables, tracer la simulation dans un rapport et organiser le traitement des écarts jusqu’au recontrôle. Cette séance prolonge la [préparation de l’audit](matrice-risques-sous-traitants-preparation-audit.md).

!!! note "Support préparatoire — simulation non attestée"
    Cette feuille fournit une trame à remplir et des exemples pédagogiques. Aucun participant, entretien tenu, retour du formateur, résultat de test ou accord de direction n’est inventé. La clôture pédagogique du module ne clôt pas les écarts opérationnels. Aucun contrôle officiel de l’ANSSI ni certification n’est revendiqué.

## PDF pour le formateur

[Télécharger le compte rendu d’audit ÉnergieAlp et son plan de remédiation — Olivier HIMBLOT (PDF, 7 pages)](../../assets/files/droit-conformite/it-3/CR-audit-EnergieAlp-plan-remediation-Olivier-HIMBLOT.pdf).

Compétence : **Participer à la mesure et à l’analyse du niveau de sécurité de l’infrastructure**. Le rapport présente une simulation documentaire réduite, les constats restant ouverts et le plan AS priorisé. Entretiens, mise en œuvre et validation du formateur restent à documenter. Le plan distingue le court terme (moins de 6 mois), le moyen terme (de 6 mois à 1 an inclus) et le long terme (plus d’un an), à partir de son approbation.

## 1. Déroulement fourni

| Étape | Activité | Trace attendue |
| --- | --- | --- |
| 1 | Présentation rapide de la démarche d’audit et de l’entretien | Périmètre, critères et méthode de collecte compris |
| 2 | **Simulation collective : 30 min**, 1 à 2 questions précises par apprenant, demandes de preuves, pression mesurée et débrief en temps réel | Journal des questions, réponses, pièces et retours |
| 3 | **Rédaction du rapport : 20 min** | Trame renseignée sur les échanges effectivement réalisés |
| 4 | Finalisation des livrables avec le formateur | Versions corrigées et retours attribués |
| 5 | Qualification des écarts résiduels, priorités, coût, délai, indicateurs et revues | Plan pilotable et décisions restant à prendre |
| 6 | Assemblage du dossier de conformité unique | Index versionné et pièces accessibles |
| 7 | **REX Speedboat animé par le formateur ou la formatrice** | Acquis, difficultés et améliorations retenues |

Seules les étapes 2 et 3 ont une durée imposée dans la consigne. Les autres durées sont à organiser avec le formateur.

## 2. Démarche d’audit et posture d’entretien

Un audit confronte des critères définis à des éléments vérifiables sur un périmètre convenu. Le [référentiel PASSI v2.2 de l’ANSSI](https://cyber.gouv.fr/sites/default/files/document/PASSI_Referentiel-exigences_v2.2.pdf) sert ici de repère méthodologique pour relier preuves et constats ; il concerne les prestations d’audit et ne devient pas le référentiel de conformité d’ÉnergieAlp.

Le **ReCyF v2.5, document de travail retenu dans les feuilles précédentes**, reste la base pédagogique des critères. Reporter pour chaque contrôle son identifiant, sa version et son applicabilité ; conserver les réserves sur le statut EE proposé et le droit applicable. Les références détaillées figurent dans la [matrice du jour 2](../it-2/debrief-matrice-cloud-act-politique-securite.md). Cette simulation ne couvre pas exhaustivement tous les MAC.

### Priorités proposées pour l’exercice ÉnergieAlp

| Priorité d’examen | Question précise | Pièce à demander et limite |
| --- | --- | --- |
| Périmètre et gouvernance | Qui porte le risque et quel SI est couvert ? | Registre EA, matrice d’applicabilité, politique ; approbation à distinguer de la rédaction |
| Accès distants à la supervision | Comment démontrez-vous la protection du VPN ? | Configuration datée, inventaire et essais ; le scénario décrit l’absence de MFA, aucun correctif n’est prouvé |
| Accès des tiers | Qui dispose encore de quels droits et pour quelle durée ? | Exports, demandes, validation et revue ; procédure seule insuffisante |
| Cloud et garanties contractuelles | Quelle analyse soutient votre décision d’hébergement ? | Analyse CloudPeak et contrat ; absence de contrat dans le scénario, aucun transfert américain démontré |
| Continuité et pilotage | Quelle preuve permet de clore une action de reprise ? | Compte rendu de test, résultats attendus/obtenus et validation métier ; plan seul insuffisant |

Cet ordre est une proposition fondée sur les risques du scénario, pas un ordre universel imposé par l’ANSSI.

L’entretien suit : **question → réponse → pièce → vérification du périmètre et de la date → constat limité → contradiction éventuelle → action**. Une déclaration est attribuée à son auteur ; elle ne devient pas automatiquement une preuve technique. En cas de désaccord, conserver les deux positions, la référence discutée et la pièce complémentaire demandée.

**Réponse préparée :** « Le dossier décrit un VPN sans MFA. Notre plan AS-02 propose une correction, mais nous n’avons pas de preuve de déploiement. La DSI doit fournir configuration et essais en fenêtre validée ; la clôture attendra leur recontrôle. »

La posture attendue associe preuve disponible, écart reconnu et trajectoire de correction. Si une information manque, indiquer précisément la pièce à obtenir, le pilote proposé et l’échéance à approuver. Ne pas répondre par une conformité globale ou par un abandon de l’argumentation.

### Organisation des 30 minutes

Proposition locale : 3 min de cadrage, 24 min de questions et débrief immédiat, 3 min de synthèse. Pour N apprenants, répartir les 24 minutes entre eux ; garantir une première question chacun avant une seconde selon l’effectif. Le formateur adapte le rythme et garde une pression mesurée, centrée sur les faits et les preuves.

Désigner auditeur/formateur, personnes interviewées et secrétaire de séance. Consigner au fil de l’eau la question exacte, la réponse attribuée, la pièce montrée, sa portée et le retour du formateur. Aucun test technique intrusif n’est nécessaire à cette simulation documentaire.

## 3. Trame de rapport à renseigner en 20 minutes

Répartition indicative : 3 min pour le cadre, 7 min pour les échanges et constats, 7 min pour les actions, 3 min pour les limites et la relecture.

### A. Identification et synthèse

| Champ | À renseigner après ou pendant la séance |
| --- | --- |
| Rapport | SIM-EA-[date]-[version] ; auteur ; historique des révisions |
| Séance | Date, heures, lieu ; commanditaire pédagogique ; destinataires et diffusion |
| Participants | Auditeur, secrétaire, personnes interviewées et fonctions ; présence réelle à confirmer |
| Objet | Simulation documentaire ÉnergieAlp ; objectifs et périmètre SI/prestataires |
| Critères | Référentiel, version, date, exigences précises et justification d’applicabilité |
| Méthode | Entretiens, examen documentaire, échantillon retenu et motif ; exclusions motivées |
| Limites | Pièces absentes, déclarations non corroborées, temps et contrôles non effectués |
| Synthèse | Points étayés, écarts prioritaires, incertitudes et décisions demandées |
| Relecture | Commentaires des interviewés, désaccords, retour formateur ; date et statut de validation |

**Conclusion préparatoire utilisable :** « Les productions disponibles structurent la démarche. Leur application opérationnelle reste à établir. Les conclusions de la simulation seront limitées aux critères et pièces effectivement examinés. » Adapter ce texte aux échanges réellement tenus.

### B. Journal des entretiens et des preuves

| ID / horaire | Personne et fonction | Question exacte / critère | Réponse attribuée | Pièce, version, origine, date, périmètre | Vérification et retour formateur |
| --- | --- | --- | --- | --- | --- |
| Q-01 / à remplir | À remplir | À remplir | À remplir | PR-01 ou « non fournie » | À remplir |

Pour chaque PR : préciser producteur, date de collecte, collecteur, méthode, emplacement, restrictions d’accès et limite de portée. Une pièce attendue porte le statut **attendue** ; une pièce consultée peut rester **non concluante**. Conserver les originaux et une copie anonymisée pour présentation publique, sans secrets ni données personnelles réelles.

### C. Registre des constats

| ID | Critère et applicabilité | Fait / source / preuve | Qualification et limite | Impact / priorité motivée | Action liée / avis de l’interviewé |
| --- | --- | --- | --- | --- | --- |
| EC-01 | À remplir | À remplir | À remplir | À remplir | AS-xx / à recueillir |

Vocabulaire local de l’exercice : **écart étayé** si critère applicable et fait probant ; **non vérifiable** si preuve insuffisante ; **point satisfaisant sur l’échantillon** si contrôle concluant ; **hors périmètre** avec motif ; **piste d’amélioration** si aucune violation de critère n’est établie. Une pièce absente peut révéler un écart documentaire si le critère exige précisément cette pièce ; elle ne prouve pas à elle seule la défaillance technique.

**Exemple préparatoire EC-01 :** VPN sans MFA selon le dossier pédagogique ; critère 8.3-EE retenu sous hypothèse EE dans la matrice ; enjeu d’accès à la supervision ; action AS-02. C’est un constat sur le scénario, pas une observation de configuration ni un résultat de l’entretien. Référencer Q/PR seulement après collecte effective.

## 4. Plan de remédiation et écarts restant ouverts

Reprendre les identifiants **AS-01 à AS-06** du [plan existant](matrice-risques-sous-traitants-preparation-audit.md#6-plan-de-remediation-et-pilotage-propose), afin de conserver une seule chaîne de suivi. Ajouter les nouveaux constats au même registre plutôt que créer des actions concurrentes.

La priorité dépend de l’impact métier, de l’exposition, des éléments disponibles et des dépendances. Coût et délai guident le séquencement, sans rendre acceptable un risque critique à eux seuls. Une mesure compensatoire doit avoir un périmètre, une durée et un contrôle d’efficacité.

| Action existante / écart à rattacher | Priorité proposée et raison | Pilote proposé / coût à chiffrer | Délai cible à approuver | Contrôle de clôture attendu |
| --- | --- | --- | --- | --- |
| AS-02 — VPN sans MFA | P1 : accès distant à la supervision | DSI + Production ; licences, intégration, temps de recette et formation | Reprendre la cible AS-02 ; convertir en date après accord et fenêtre validée | Configuration, essais MFA et refus, maintien du service, validation métier |
| AS-01 — Accès tiers sans revue | P1 : droits et durée insuffisamment maîtrisés | DSI/Production ; charge inventaire et revue | Reprendre AS-01 ; dépend de l’inventaire et des propriétaires | Revue attribuée, corrections et test de retrait d’accès |
| AS-03 — Lacunes CloudPeak | P1 : garanties et décision non étayées | DSI/RSSI, juridique/achats ; étude, contrat, éventuelle migration à chiffrer | Reprendre AS-03 ; jalons analyse puis décision | Analyse et décision tracées, garanties vérifiées ; migration testée si retenue |
| AS-04 à AS-06 — Reprise, actifs et tiers | Conserver les priorités motivées du plan initial ; revoir selon nouveaux faits | Pilotes du plan ; charge et devis à recueillir | Reprendre les jalons existants | Recettes, registre rapproché, contrôles fournisseurs et décisions |

Ce tableau complète le plan initial sans valider ses délais. **Aucun budget ni engagement n’est approuvé.** Pour chaque ligne ajouter : EC lié, coût estimé en euros et jours-personnes avec source/date, dépendances, date approuvée, responsable nommé, mesure transitoire, statut, preuve et recontrôleur. Si l’estimation manque, écrire « à chiffrer » et fixer le jalon d’estimation, sans inventer un montant.

### Risque résiduel et décision

Distinguer **écart encore ouvert**, **risque résiduel projeté après mesures prévues** et **risque résiduel évalué après mesures vérifiées**. Dans l’état documentaire actuel, aucun niveau résiduel mesuré n’est établi.

| Écart / risque | Mesures réellement vérifiées / preuves | Résiduel et incertitudes | Décision / autorité / date | Expiration et recontrôle |
| --- | --- | --- | --- | --- |
| À remplir | Aucune preuve ou PR identifiées | Non évalué si données insuffisantes | Traitement, évitement, transfert ou acceptation motivée à décider | À remplir |

Une acceptation de risque ne supprime pas une obligation applicable. Dans le scénario, seul le RSSI valide une dérogation de sécurité ; cela ne permet pas de déroger à la loi. Faire tracer les arbitrages et responsabilités selon la gouvernance retenue.

**États :** proposé → approuvé/planifié → en cours → réalisé à vérifier → clos après recontrôle. Un blocage conserve cause, pilote et date de décision. La clôture exige un résultat comparé au critère attendu, un vérificateur, une date et une preuve ; un simple « fait » ne suffit pas.

## 5. Indicateurs et surveillance de la conformité

Conserver K-01 à K-06 et leurs définitions dans la feuille précédente. Les cibles suivantes sont des propositions locales ; aucune valeur n’est mesurée.

| Suivi | Calcul / source | Pilote / rythme proposé | Cible et réaction |
| --- | --- | --- | --- |
| K-03 — MFA | Accès concernés protégés et testés / accès concernés recensés ; inventaire, paramètres et essais | DSI ; mensuel et après changement | 100 % proposé ; écarts et exceptions examinés séparément |
| K-04 — Retards P1 | Nombre de P1 après échéance approuvée ; registre AS daté | RSSI ; hebdomadaire | 0 ; escalade et arbitrage sur chaque retard |
| K-06 — Reprise | Scénarios prioritaires testés et acceptés / scénarios prioritaires planifiés ; recettes | DSI/métiers ; à chaque test, synthèse trimestrielle | 100 % du programme ; planifier les essais manquants |
| Clôtures étayées | Actions déclarées closes avec preuve et recontrôle / actions déclarées closes ; registre et PR | RSSI ; mensuel | 100 % ; rouvrir une clôture sans preuve suffisante |

Dénominateur inconnu : **non calculable**. Dénominateur nul : **sans objet sur la période**, à justifier. Ni l’un ni l’autre ne vaut 100 %. Afficher date, périmètre, effectifs et source avec chaque valeur.

**Programme de revue proposé, à approuver :** point hebdomadaire sur P1 ; revue mensuelle du plan et des indicateurs ; revue trimestrielle des accès et fournisseurs ; audit interne annuel du périmètre retenu, avec échantillon et évaluateur distinct du réalisateur autant que possible ; revue de direction annuelle des résultats, ressources, exceptions et risques. Ces fréquences locales complètent les exigences particulières recensées dans la matrice et ne sont pas présentées comme des fréquences ANSSI universelles.

Après incident, changement significatif, nouvelle prestation ou évolution d’un texte : réexaminer immédiatement l’applicabilité, les risques et les preuves concernées. Conserver calendrier, comptes rendus, arbitrages, actions et date de prochaine revue.

## 6. Assembler le dossier de conformité unique

Créer un dossier maître avec sommaire, responsable, version, date, diffusion et historique. Un export PDF peut faciliter la lecture ; conserver aussi les sources et les pièces référencées. Le présent mémo fournit l’index ; les preuves opérationnelles et le rapport rempli restent à joindre.

| Partie | Contenu et renvoi | État actuel |
| --- | --- | --- |
| 00 — Index | Périmètre, versions, auteurs, accès aux pièces, limites et liste des manquants | À figer pour la remise |
| 01 — Applicabilité | D-01/D-02 : [cadres](../it-1/comprendre-conformite-reglementaire.md) et [qualification](../it-1/de-exigence-a-preuve.md) | Raisonnement documentaire ; qualification à confirmer |
| 02 — Actifs | D-03 : [registre EA](../it-2/registre-actifs-critiques.md) | V0 à rapprocher de l’inventaire réel |
| 03 — Exigences et politique | D-04/D-06 : [matrice et politique](../it-2/debrief-matrice-cloud-act-politique-securite.md) | Proposition ; adoption et application non attestées |
| 04 — Cloud et tiers | D-05/D-07 et [risques/procédures tiers](matrice-risques-sous-traitants-preparation-audit.md) | Analyses préparées ; contrats et contrôles manquants |
| 05 — Simulation | Rapport §3, journal Q, constats EC, retours attribués | Trames disponibles ; séance non attestée |
| 06 — Traitement et suivi | Plan AS, coûts/dates approuvés, décisions résiduelles, indicateurs K et calendrier | Propositions ; mesures et décisions à recueillir |
| 07 — Preuves | Registre PR, pièces collectées, résultats de recontrôle, versions anonymisées | À constituer ; distinguer attendues et recueillies |
| 08 — REX | Speedboat, améliorations, responsables et suites | À renseigner en séance |

Avant remise : ouvrir chaque lien et pièce, vérifier la correspondance exigence → constat → action → preuve, retirer doublons et anciennes versions ambiguës, conserver les réserves. Faire relire avec le formateur et attribuer ses retours sans présumer son approbation. Les noms des personnes interviewées restent dans la version à diffusion maîtrisée ; pseudonymiser la version publique.

## 7. Fermeture du module — REX Speedboat

Le formateur ou la formatrice anime un tour de parole puis une sélection collective des améliorations. Les propositions ci-dessous servent de questions, pas de retours déjà recueillis.

| Élément | Question à poser | Trace à renseigner |
| --- | --- | --- |
| Île / destination | Quel résultat voulions-nous atteindre ? | Objectif et critères de réussite |
| Vent / moteurs | Qu’est-ce qui a aidé à comprendre et à produire ? | Acquis, outils et pratiques utiles |
| Ancres | Qu’est-ce qui a ralenti ou posé difficulté ? | Obstacle et exemple concret |
| Rochers | Quels risques persistent pour la suite ? | Risque, conséquence et vigilance |
| Cap / actions | Que ferions-nous différemment ? | Amélioration, pilote, délai et résultat attendu |

Chaque apprenant formule un acquis et une difficulté. Le groupe retient quelques actions réalisables et les reporte dans un tableau **amélioration → responsable → échéance → preuve de résultat**. Distinguer retour individuel, accord collectif et décision du formateur.

## 8. État final attendu

- Rapport renseigné sur les entretiens réels, avec participants, critères, questions, pièces, constats et limites.
- Livrables relus, versions figées et retours du formateur attribués.
- Plan unique priorisé avec coût estimé ou jalon de chiffrage, pilotes, dates approuvées et critères de clôture.
- Écarts restant ouverts et décisions résiduelles explicites ; indicateurs et prochaines revues définis.
- Dossier indexé présentable et REX tracé, sans affirmation de conformité globale.

**État à la création de la feuille :** support et trames disponibles ; tenue de la simulation, rapport rempli, relectures, décisions, preuves et REX restent à documenter.

[Retour à l’itération](index.md) · [Module](../README.md) · [Pense-bête](../../pense-bete/glossaire/droit-conformite/it-3.md)
