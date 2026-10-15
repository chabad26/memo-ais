# Débrief, matrice d’applicabilité, Cloud Act et politique de sécurité

**Module : Droit et conformité — Itération 2 — 3 h 30 — Présentiel.**

## Objectif et statut du travail

Passer du [registre des actifs critiques](registre-actifs-critiques.md) à une matrice NIS2 renseignée, argumenter le maintien ou la migration de l’hébergement CloudPeak et rédiger une politique de sécurité simplifiée en onze rubriques.

!!! note "Proposition documentaire du 15 octobre 2026"
    Les réponses ci-dessous s’appuient sur le [dossier fictif ÉnergieAlp](../annexes/dossier-entreprise-energiealp.md). Le débrief, les échanges entre binômes et la validation du formateur **ne sont pas documentés comme réalisés**. Les configurations, procédures et échéances sont proposées ; aucun déploiement, contrat signé, test technique ou adoption de la politique n’est attesté. Les cotations du registre V0 sont conservées jusqu’à un arbitrage explicite.

## 1. Déroulement de la séance

| Étape | Travail demandé | Production attendue |
| --- | --- | --- |
| 1 | Débrief collectif du registre : comparer les cotations, corriger la méthode, capitaliser les bonnes pratiques | Historique des décisions et registre révisé après arbitrage |
| 2 | Reprendre la chaîne source → exigence → applicabilité → contrôle/dispositif → preuve → état → écart → action | Matrice complète sur le périmètre étudié, liée aux actifs et à un plan d’action |
| 3 | Mobiliser les acquis du module Cloud pour analyser CloudPeak et le Cloud Act | Analyse des conditions juridiques et des risques concrets, avec questions ouvertes |
| 4 | Comparer offres américaines et offres présentant des garanties de souveraineté | Décision de maintien ou migration argumentée, conditionnelle et réversible |
| 5 | En groupe, rédiger une politique suivant les onze rubriques ; échange avec un autre binôme puis débrief | Politique proposée, fiche de relecture et corrections tracées |

La durée globale est de **3 h 30** ; aucune durée par étape n’est fournie. Les productions proposées ici constituent une base de discussion, sans compte rendu inventé du groupe.

## 2. Préparer le débrief du registre

| Point de méthode | Position actuelle de la V0 | Question à soumettre au groupe / correction possible | État de la décision |
| --- | --- | --- | --- |
| Échelle | C/I/D/T de 1 à 4 ; intégrité reformulée en impact et intervalles D explicités | Confirmer l’adaptation de l’exemple du kit et utiliser les mêmes critères pour tous les actifs | À arbitrer |
| Agrégation | Maximum des quatre notes, sans moyenne | Conserver les notes détaillées ; justifier le maximum retenu et distinguer criticité de priorité | Méthode proposée |
| EA-04 analytics | I4 prudent car les prévisions peuvent influer sur les décisions de charge | Demander aux métiers quelle décision dépend réellement de la plateforme et avec quel impact | Aucune commande directe du SCADA établie |
| Disponibilité | D4 pour supervision et CRM ; D3 provisoires pour compteurs, analytics et VPN | Valider délais tolérables, modes dégradés et objectifs de reprise ; ne pas confondre besoin et disponibilité mesurée | D3 et objectifs de reprise non validés |
| Complétude | Cinq services recensés, mais registre existant non fourni | Rapprocher inventaires, terrain et cloud ; identifier les instances et actifs de support confirmés | Actifs absents du registre existant non identifiables |
| Responsables | DSI et Production repris du dossier ; propriétaire des compteurs proposé | Désigner explicitement un propriétaire métier pour EA-02 | Désignation attendue |

**Bonnes pratiques à vérifier pendant la revue :** justification par dimension, référence au dossier, hypothèses visibles, propriétaire nommé, dépendances tracées et historique des modifications. Ce sont des critères de relecture, pas des observations déjà recueillies dans le groupe.

Après le débrief, conserver **actif → ancienne note → nouvelle note → motif → auteur → date → validateur**. Une note modifiée sans justification affaiblit la traçabilité.

## 3. Matrice d’applicabilité NIS2 renseignée

### 3.1. Périmètre, sources et règles de lecture

- **Source européenne :** [directive (UE) 2022/2555](https://eur-lex.europa.eu/eli/dir/2022/2555/oj), articles et annexes précisés ci-dessous. Les modalités nationales doivent être vérifiées séparément avant une conclusion juridique opérationnelle.
- **Qualification proposée :** gestionnaire de distribution d’électricité, annexe I ; environ 650 salariés ; **entité essentielle (EE)** selon le raisonnement de l’[activité 1.2](../it-1/de-exigence-a-preuve.md), sous réserve du périmètre juridique et des règles de calcul. Aucun résultat du simulateur n’est disponible ; OIV non déterminé.
- **Périmètre technique :** EA-01 SCADA, EA-02 compteurs, EA-03 CRM, EA-04 analytics, EA-05 VPN ; les dépendances à confirmer sont recensées dans le registre.
- **Référentiel d’aide :** [ReCyF — ANSSI](https://cyber.gouv.fr/reglementation/cybersecurite-systemes-dinformation/directives-nis-nis2-et-dispositif-saiv/directive-nis-2/), présenté comme document de travail lors de la consultation du 15 octobre 2026. Ne pas transformer ses recommandations en obligations nationales supposées déjà opposables.
- **État des preuves :** P-DOS-01 = dossier pédagogique, §1 à §6 ; auteur et date de production non précisés, lecture du 15 octobre 2026. Il étaye les faits du scénario, sans prouver un état opérationnel réel.

La sélection article par article ci-après reprend l’examen documentaire préparé pour le livrable formateur. Les codes sont : **A**, retenu dans l’hypothèse EE ; **C**, conditionnel à vérifier ; **H**, cadre institutionnel ou juridique sans réglage technique directement déductible ; **X**, hors activité décrite. Ils ne sont pas des notes de conformité.

### 3.2. Examen article par article

#### Articles 1 à 16

Référence : directive (UE) 2022/2555. Les motifs ci-dessous expliquent la sélection du périmètre. Pour H, l’absence de réglage technique ne signifie pas que l’article est sans effet juridique. État de mise en œuvre : non évalué, sauf écarts explicitement déclarés par le dossier ÉnergieAlp.

| Art. | Objet résumé | Code | Lien au périmètre / décision motivée |
| --- | --- | --- | --- |
| 1 | Objet | H | Cadre de la directive ; aucun réglage technique isolé à en déduire. |
| 2 | Champ | A | Électricité et taille : qualification ci-dessus ; confirmer le périmètre. |
| 3 | EE / EI | A | EE proposée ; supervision art. 32 et informations d’identification art. 3 §4 à préparer selon modalités nationales. Pas de décision officielle. |
| 4 | Textes sectoriels UE | C | Rechercher équivalence sectorielle au sens du texte ; aucune exclusion établie dans le dossier. |
| 5 | Harmonisation minimale | H | Cadre pour les États ; vérifier exigences françaises additionnelles. |
| 6 | Définitions | H | Fixer vocabulaire incident, risque, entité et systèmes dans les procédures. |
| 7 | Stratégie nationale | H | Responsabilité étatique ; pas de stratégie nationale à produire par ÉnergieAlp. |
| 8 | Autorités / points de contact | H | Identifier les interlocuteurs officiels dans la procédure d’incident M-05 ; ÉnergieAlp ne les désigne pas. |
| 9 | Gestion nationale des crises | H | Articuler l’escalade interne avec les autorités ; dispositif national hors maîtrise interne. |
| 10 | CSIRT nationaux | H | Référencer le CSIRT compétent, sans assimiler l’équipe interne à un CSIRT national. |
| 11 | Capacités / missions CSIRT | H | Obligations des CSIRT ; prévoir coopération et éléments d’incident côté entité. |
| 12 | Divulgation coordonnée | C | Prévoir réception et transmission des vulnérabilités ; mécanisme national hors entité. |
| 13 | Coopération nationale | H | Organisation des autorités ; tenir des contacts internes cohérents. |
| 14 | Groupe de coopération | H | Structure européenne ; pas de configuration ÉnergieAlp directement exigée. |
| 15 | Réseau des CSIRT | H | Coopération européenne ; contribution via le CSIRT compétent si nécessaire. |
| 16 | EU-CyCLONe | H | Coordination des crises majeures ; conserver chaîne d’escalade interne. |

#### Articles 17 à 31

Référence : directive (UE) 2022/2555. Les motifs ci-dessous expliquent la sélection du périmètre. Pour H, l’absence de réglage technique ne signifie pas que l’article est sans effet juridique. État de mise en œuvre : non évalué, sauf écarts explicitement déclarés par le dossier ÉnergieAlp.

| Art. | Objet résumé | Code | Lien au périmètre / décision motivée |
| --- | --- | --- | --- |
| 17 | Coopération internationale | H | Cadre institutionnel ; pas d’obligation technique autonome identifiée. |
| 18 | Rapport européen | H | Rapport sur l’état de la cybersécurité ; exploiter comme contexte de risque. |
| 19 | Évaluation par les pairs | H | Mécanisme institutionnel ; ne pas le confondre avec audit interne. |
| 20 | Gouvernance | A | M-06 : politique approuvée, suivi et formation de la direction. |
| 21 | Gestion des risques | A | M-01 à M-04 et M-07 à M-14 ; décomposition §2 a à j, proportionnalité et fournisseurs. |
| 22 | Chaînes critiques | H | Évaluations coordonnées au niveau UE ; intégrer leurs résultats disponibles dans M-02. |
| 23 | Notifications | A | M-05 : qualification, horodatage, destinataires et délais de notification. |
| 24 | Certification | C | Rechercher une exigence imposée au périmètre concerné ; aucun certificat exigé démontré ici. |
| 25 | Normalisation | H | Utiliser les normes pertinentes comme moyens ; aucune obligation générale ISO 27001 déduite. |
| 26 | Juridiction / territorialité | A | France pour l’entité décrite ; confirmer établissement et autorités. Cloud : analyser séparément le fournisseur. |
| 27 | Registre de certaines entités | X | Activités numériques listées non décrites pour ÉnergieAlp ; utiliser un cloud ne fait pas d’elle un fournisseur cloud. |
| 28 | Données d’enregistrement DNS | X | Aucun service de registre de domaine ou d’enregistrement visé décrit. |
| 29 | Partage d’informations | C | Participation éventuelle à encadrer ; pas d’adhésion ni d’accord existant prouvé. |
| 30 | Notification volontaire | C | Circuit distinct des notifications obligatoires ; préciser les cas dans la procédure d’incident M-05. |
| 31 | Supervision générale | A | Préparer dossier de preuve et coopération ; encadre surtout les pouvoirs des autorités. |

#### Articles 32 à 46

Référence : directive (UE) 2022/2555. Les motifs ci-dessous expliquent la sélection du périmètre. Pour H, l’absence de réglage technique ne signifie pas que l’article est sans effet juridique. État de mise en œuvre : non évalué, sauf écarts explicitement déclarés par le dossier ÉnergieAlp.

| Art. | Objet résumé | Code | Lien au périmètre / décision motivée |
| --- | --- | --- | --- |
| 32 | Supervision EE | A | M-15 : produire preuves et suivre demandes d’audit dans l’hypothèse EE. |
| 33 | Supervision EI | X | Non retenu avec hypothèse EE ; réexaminer si qualification modifiée. |
| 34 | Amendes administratives | A | Prendre en compte gouvernance et risque juridique ; pas d’amende effective déduite du dossier. |
| 35 | Articulation RGPD | C | Articuler incident cyber et violation personnelle ; ne pas confondre notifications NIS2/RGPD. |
| 36 | Sanctions nationales | H | Règles à établir par les États ; vérifier droit national avant chiffrage opérationnel. |
| 37 | Assistance mutuelle | H | Coopération entre autorités ; centraliser réponses et demandes côté entité. |
| 38 | Délégation | H | Pouvoirs de la Commission ; aucune configuration directement applicable. |
| 39 | Comité | H | Procédure institutionnelle ; aucune action technique interne autonome. |
| 40 | Réexamen | H | Suivre évolution du texte dans la veille juridique. |
| 41 | Transposition | H | Vérifier les textes nationaux et leurs dates ; la directive seule ne décrit pas toutes les modalités françaises. |
| 42 | Modification UE 910/2014 | H | Articulation des textes ; pas de service de confiance décrit pour ÉnergieAlp. |
| 43 | Modification UE 2018/1972 | H | Articulation communications électroniques ; aucune activité de fournisseur décrite. |
| 44 | Abrogation NIS1 | H | Distinguer ancien statut OSE et qualification EE/EI ; ne pas les confondre. |
| 45 | Entrée en vigueur | H | Repère temporel européen ; ne vaut pas preuve de mise en œuvre nationale. |
| 46 | Destinataires | H | Directive adressée aux États membres ; exigences opérationnelles à lire avec transposition. |

### 3.3. Exigences, applicabilité et état

Les identifiants **M-01 à M-05** prolongent la matrice du jour 1. **M-06 à M-16** complètent l’analyse. Sauf mention contraire, les exigences sont retenues dans l’hypothèse EE. Les articles sont décomposés en contrôles adaptés au scénario ; les configurations choisies sont des moyens proposés, sans prétendre être des commandes imposées par la directive.

| ID / source | Exigence et applicabilité au périmètre | Dispositif / contrôle à relier | Preuve attendue | État, écart et limite de conclusion |
| --- | --- | --- | --- | --- |
| **M-01 — art. 21 §2 j** | Authentification adaptée au risque ; accès VPN EA-05 à la supervision EA-01 | MFA, comptes nominatifs, essai des accès et secours contrôlé | P-01 : paramètres réellement chargés et essais avec/sans second facteur | **Écart déclaré** : VPN sans MFA ; aucun export ni test disponible |
| **M-02 — art. 21 §2 a, d et §3** | Évaluer risques et garanties fournisseur ; CRM/analytics chez CloudPeak | Analyse Cloud Act, responsabilités, clauses et contrôle des accès ; procédure PR-ST-01/02 ci-dessous | P-02 : analyse approuvée, contrat, cartographie données/accès | **Écart déclaré** : pas d’analyse formalisée ni de contrat ; pas de transfert US démontré |
| **M-03 — art. 21 §2 i** | Gérer les actifs ; EA-01 à EA-05 et dépendances confirmées | Inventaire réconcilié et criticité justifiée | P-03 : registre versionné avec propriétaires, sites, versions et validation | **Écart déclaré** : registre existant incomplet ; V0 produite, non réconciliée ni validée |
| **M-04 — art. 21 §2 i** | Maîtriser les accès internes/tiers ; GridSoft, RéseauTech et systèmes concernés | Habilitations nominatives, moindre privilège, expiration, revue et retrait ; PR-ST-03/04 | P-04 : matrice de droits, approbations, exports et revue datée | **Écart déclaré** pour les tiers : accès à la demande sans stratégie ni revue documentée ; comptes internes non évalués |
| **M-05 — art. 23** | Qualifier et notifier les incidents significatifs du périmètre EE | Procédure, horodatage de prise de connaissance, escalade et destinataires officiels | P-05 : procédure et exercice daté ; accusé uniquement si notification réellement effectuée | **Non évalué** : procédure non décrite ; absence non démontrée |
| **M-06 — art. 20 §1–2** | Approbation et supervision des mesures par la direction ; formation | Politique proposée, rôles, budget, suivi et formation des dirigeants | P-06 : décision d’approbation, compte rendu de suivi et formation | **Non évalué** : aucune adoption ni formation prouvée |
| **M-07 — art. 21 §1, §2 a** | Analyser les risques proportionnellement, y compris environnement physique | Scénarios liés aux actifs : atteinte aux données, arrêt de service, énergie, locaux, télécoms | P-07 : analyse de risque, mesures et arbitrages | Cloud sans analyse selon le dossier ; couverture générale **non évaluée** |
| **M-08 — art. 21 §2 c** | Continuité, sauvegarde, reprise et gestion de crise ; EA-01/03 prioritaires | Objectifs métier, copies protégées, restauration isolée, modes dégradés et cellule de crise | P-08 : plan et résultats de restauration/reprise mesurés | **Non évalué** : aucune architecture de secours ni sauvegarde décrite |
| **M-09 — art. 21 §2 e** | Sécurité des acquisitions et de la maintenance, traitement/divulgation des vulnérabilités | Versions/support, réception des avis, qualification, test de correction et retour arrière | P-09 : inventaire, avis, dossier de changement et test | **Non évalué** : aucune version ni politique de correctifs fournie |
| **M-10 — art. 21 §2 f et §4** | Évaluer l’efficacité et corriger sans retard indu les écarts constatés | Plan de contrôles et suivi des actions avec recontrôle avant clôture | P-10 : rapports, décisions et preuves de correction | **Non évalué** : un plan rédigé ne démontre pas l’efficacité |
| **M-11 — art. 21 §2 g ; art. 20 §2** | Hygiène et formation adaptées aux rôles | Accueil, sensibilisation, formation administration/tiers et direction | P-11 : supports, participation et évaluation | **Non évalué** : pas de formation documentée |
| **M-12 — art. 21 §2 h** | Politique d’usage de la cryptographie et du chiffrement | Choix selon risques, flux/données sensibles, certificats et maîtrise des clés | P-12 : politique, configuration et essais de récupération | **Non évalué** : chiffrement réel et contrôle des clés inconnus |
| **M-13 — art. 21 §1 et approche tous risques du §2** | Protéger les systèmes et leur environnement physique ; locaux et équipements terrain | Zones, accès physiques habilités, visiteurs, protection énergie/environnement selon analyse | P-13 : règles, contrôles d’accès et essai d’un scénario validé | **Non évalué** : aucun contrôle physique décrit ; ne pas conclure à leur absence |
| **M-14 — art. 21 §2 b** | Détecter, traiter et documenter les incidents ; tous EA | Collecte de traces utiles, horodatage, alertes, triage et escalade | P-14 : événement brut, alerte, ticket et chronologie | Journaux VPN mentionnés, mais couverture et exploitation **non évaluées** |
| **M-15 — art. 31–32** | Coopérer à la supervision dans l’hypothèse EE ; art. 33 écarté sous cette hypothèse | Dossier de preuve, accès contrôlé, suivi des demandes et mesures correctrices | P-15 : index, habilitations et bordereaux de remise si demande réelle | **Non évalué** : aucun audit d’autorité attesté |
| **M-16 — art. 2–3, 26** | Confirmer champ/qualification, rattachement et informations d’identification selon règles nationales | Dossier juridique : activité, effectif, groupe, établissement, contacts et mise à jour | P-16 : qualification approuvée, sources nationales et transmission si requise | EE proposée ; périmètre de calcul et modalités nationales à confirmer |

**Article 23 :** pour un incident significatif, distinguer alerte précoce sous 24 h, notification sous 72 h à compter de la prise de connaissance, rapport intermédiaire sur demande et rapport final généralement au plus tard un mois après la notification. Si l’incident est encore en cours, appliquer les dispositions de rapport d’avancement puis de rapport final du texte. Identifier les impacts, la gravité, les destinataires et les personnes à informer selon les conditions de l’article ; une simple alerte technique ne déclenche pas automatiquement toutes les notifications. Articuler séparément avec les articles 33–34 du RGPD si des données personnelles sont concernées. [Source : directive NIS2, art. 23](https://eur-lex.europa.eu/eli/dir/2022/2555/oj).

### 3.4. Traduction en configurations et tests attendus

| Contrôles liés | Configuration ou procédure cible proposée | Vérification et condition de réussite |
| --- | --- | --- |
| M-01 / M-04 | MFA VPN, comptes nominatifs, droits limités à mission et date d’expiration ; séparer usages d’administration et usages courants | Connexion autorisée avec facteur valide ; refus sans facteur, hors droit ou après expiration ; secours contrôlé testé. Ne pas supprimer l’ancien accès avant validation de la solution de remplacement |
| M-02 / M-12 | Cartographie des flux cloud, accès administratifs limités, choix de chiffrement et séparation des responsabilités sur les clés | Vérifier accès réellement possibles, protocole/certificat négocié et possibilité du fournisseur d’obtenir le clair ; tester récupération des clés sur copie isolée |
| M-03 | Identifiants EA stables, instance/version/site, propriétaire, données, dépendances et cycle de vie | Comparer inventaire, terrain et cloud ; expliquer chaque exclusion et faire valider les cotations par les métiers |
| M-05 / M-14 | Source, compte, action, résultat et heure fiables dans les traces utiles ; circuit d’alerte et annuaire d’incident accessibles | Injecter un événement de test autorisé, retrouver sa trace et son ticket ; exercice sur table de notification horodaté, sans envoi externe non autorisé |
| M-08 | Sauvegardes et droits séparés selon analyse, objectifs de reprise métier, procédure et solution de continuité adaptées à chaque service | Restaurer un échantillon isolé, vérifier données et fonctionnement, mesurer temps et perte ; comparer aux objectifs approuvés |
| M-09 | Circuit d’avis vulnérabilités, versions/support et changement documentés | Tester correction et retour arrière avant déploiement ; contrôler version effectivement chargée et fonctionnement du service |
| M-06 / M-10 / M-11 | Politique approuvée, calendrier de contrôle/formation, ticket par écart et validation avant clôture | Vérifier décisions, participation, évaluation et preuves de recontrôle ; une procédure seule ne permet pas de déclarer « conforme » |
| M-07 / M-13 | Inventaire des zones sensibles, habilitations physiques, gestion des visiteurs et dispositions de continuité énergie adaptées | Contrôler un échantillon de droits et un scénario validé sans mettre l’exploitation en danger ; documenter périmètre et limites |
| M-15 / M-16 | Répertoire de preuves avec droits de lecture, origine et version ; veille juridique et dossier d’identification | Retrouver une preuve à partir d’une ligne de matrice ; vérifier destinataire/habilitation avant remise et mettre à jour la qualification lors d’un changement |

Aucun produit, port, algorithme ou réglage chiffré n’est présenté comme observé : les versions et architectures ne sont pas fournies. Les détails techniques devront être précisés par la DSI et Production après analyse et essais.

### 3.5. Plan d’action associé

**J = date future d’approbation du plan.** Les échéances sont proposées ; elles ne sont pas des délais légaux. Pour toute intervention sur supervision ou SI clientèle : fenêtre validée, nuit/hors pics sauf urgence de sécurité avérée, critères de réussite et retour arrière. Seul le RSSI valide une dérogation de sécurité.

| Action / lignes | Priorité motivée | Responsable proposé | Échéance proposée | Clôture vérifiable |
| --- | --- | --- | --- | --- |
| A-01 / M-01, M-04 | P1 : accès distant à la supervision et absence MFA déclarée | DSI avec Production et RSSI | Étude J+7 ; déploiement après essais en fenêtre validée | Paramétrage et tests positifs/négatifs ; exceptions bornées et tracées |
| A-02 / M-02, M-12 | P1 : données clients hébergées sans contrat ni analyse documentée | DSI, RSSI, appui juridique à désigner | Lancement J+7 ; décision d’orientation J+30 | Analyse, contrat et décision motivée ; risques non résolus conservés dans le plan |
| A-03 / M-04 | P1 : accès prestataires sans revue documentée | DSI et Production selon actif | Première revue J+15 ; fréquence trimestrielle proposée | Droits justifiés, retraits/expirations testés et revue signée |
| A-04 / M-03, M-07, M-13 | P1 : inventaire incomplet, dépendances physiques/support à vérifier | DSI et Production ; propriétaire EA-02 à désigner | J+30 | Registre réconcilié, responsables et cotations validés ; analyse physique documentée |
| A-05 / M-05, M-08, M-14 | P2 : vérifier des capacités essentielles à la continuité, non décrites | RSSI, DSI et Production | Collecte existant J+30 ; tests ensuite planifiés | Procédures, restauration mesurée, événement retrouvé et exercice d’incident |
| A-06 / M-06, M-09 à M-11, M-15, M-16 | P2 : gouvernance, preuve d’efficacité et cadre juridique à compléter | Direction, RSSI, DSI et Production | Revue documentaire J+30 | Politique approuvée si décision, contrôles/formation et responsabilités planifiés, sources nationales vérifiées |

Pour P-01 à P-16, conserver : producteur/collecteur, date/heure/fuseau, origine et version, actifs et comptes testés, méthode, résultat attendu/constaté, limites, emplacement contrôlé, relecteur et décision. **Ces preuves opérationnelles sont attendues, pas recueillies.** Le registre V0 et cette matrice sont des productions documentaires disponibles.

## 4. Analyse Cloud Act : CloudPeak Americas

### 4.1. Partir des acquis Cloud et des faits

Réutiliser les notions déjà travaillées dans le [module Cloud/IAM](../../integration-distribuee-cloud-iam/README.md) et la [comparaison d’un second fournisseur](../../integration-distribuee-cloud-iam/it-4/reproduire-exploiter-second-fournisseur.md) : responsabilités partagées, région, IAM, coût et réversibilité. Le laboratoire antérieur ne prouve aucune configuration de CloudPeak.

**Faits :** CloudPeak est une filiale européenne d’un groupe américain et héberge une partie du CRM ainsi que l’analytics. Aucun contrat ni analyse de risque formalisée n’est fourni. Le CRM traite notamment des IBAN ; l’analytics traite aussi des consommations individuelles. Localisation précise, accès d’administration, sous-prestataires et maîtrise des clés ne sont pas documentés.

**Précision juridique :** la formulation « société de droit américain » de la consigne est un point de départ simplifié. L’analyse doit examiner la juridiction américaine sur l’entité visée et la possession, garde ou maîtrise des données. Un stockage hors des États-Unis ne suffit pas à exclure une demande ; l’appartenance au groupe ne prouve ni qu’une demande a été émise ni que la maison mère peut obtenir toutes les données. [DOJ — présentation du Cloud Act](https://www.justice.gov/opa/press-release/file/1153446/dl).

### 4.2. Questions et risques concrets

| ID / actif | Scénario de risque à analyser | Information à obtenir | Mesure / preuve attendue |
| --- | --- | --- | --- |
| RC-01 / EA-03, EA-04 | Demande légale adressée à une entité relevant de la juridiction américaine et pouvant produire les données | Entité contractante, structure du groupe, pouvoirs juridiques/techniques et procédure de demandes légales | Analyse juridique individualisée ; engagements d’information/contestation lorsque permis ; aucune garantie absolue déduite du contrat |
| RC-02 / EA-03 | Divulgation de dossiers clients ou IBAN par un accès fournisseur, légal ou compromis | Administrateurs, lieux d’accès, habilitations, traces et sous-prestataires | Réduction des droits, traçabilité, chiffrement approprié et minimisation ; tests d’accès et matrice de responsabilités |
| RC-03 / EA-04 | Réidentification ou usage indu de consommations prétendument agrégées | Granularité, possibilité de rattachement, finalités et jeux de données réellement nécessaires | Minimiser, pseudonymiser ou anonymiser si démontré ; vérifier les limites. Agrégation ne signifie pas anonymisation |
| RC-04 / EA-03, EA-04 | Dépendance fournisseur et sortie impossible dans le délai métier | Formats/API, volumes, coûts de sortie, licences, services propriétaires, droits d’export | Export et restauration sur environnement cible ; estimation de durée et coût ; clause et test de réversibilité |
| RC-05 / EA-03, EA-04 | Transfert hors EEE ou accès depuis un pays tiers sans garanties adaptées | Régions données/sauvegardes/support, destinataires, finalités et mécanisme juridique éventuel | Cartographie des flux et analyse RGPD selon réalité des transferts ; ne pas assimiler risque Cloud Act et transfert effectivement constaté |

Les probabilités et risques résiduels ne sont pas chiffrés faute d’informations suffisantes. RC-01 à RC-05 constituent une **première identification**, destinée à alimenter la future matrice des risques fournisseurs, sans la présenter comme validée.

Le chiffrement au repos géré par le fournisseur ne garantit pas qu’il ne puisse accéder au clair. Examiner qui utilise les clés et où les données sont déchiffrées ; une clé dite « client » ne suffit pas si le service peut l’invoquer. Des clés hors contrôle fournisseur peuvent réduire certains accès, avec des contraintes fonctionnelles et de reprise à tester. [CNIL — pratiques de chiffrement dans le cloud public](https://www.cnil.fr/fr/les-pratiques-de-chiffrement-dans-linformatique-en-nuage-cloud-public).

## 5. Comparer les offres et argumenter une décision

### 5.1. Grille de comparaison à appliquer aux offres précises

| Critère | Offre d’un hyperscaler américain : question à instruire | Offre revendiquant une souveraineté : question à instruire | Pièce de décision |
| --- | --- | --- | --- |
| SecNumCloud | L’offre précise possède-t-elle une qualification et pour quel périmètre ? Ne pas extrapoler depuis une autre offre ou une annonce | Vérifier offre, version, périmètre et validité ; une démarche « en cours » n’est pas une qualification acquise | Décision ANSSI et périmètre exact, vérifiés au choix du fournisseur |
| Siège et contrôle juridique | Entité contractante, groupe, juridictions et contrôle possible des données | Siège, actionnariat, contrôle, dépendances et sous-prestataires ; le siège français seul ne suffit pas | Analyse juridique documentée |
| Localisation et accès | Région de production, sauvegardes, support et administration | Mêmes vérifications, y compris support et services annexes | Carte des données et accès, engagements vérifiables |
| Sécurité et clés | Capacités IAM, traces, chiffrement, maîtrise du clair et responsabilités | Mêmes critères techniques ; vérifier mise en œuvre dans l’offre et dans le service client | Exports/tests sur périmètre pilote, sans présumer le résultat |
| Maturité et compatibilité | Compatibilité CRM/analytics, services propriétaires, support et compétences disponibles | Couverture fonctionnelle, dépendances, capacité et support effectifs | Pilote avec tests métier et techniques |
| Réversibilité | Exports complets, formats, documentation et frais de sortie | Même exigence ; changer de fournisseur ne supprime pas l’enfermement | Export/restauration réussis et délai mesuré |
| Coût global | Hébergement, licences, trafic, sortie, compétences et maintien des protections | Même périmètre, ajout migration, double exploitation et formation | Devis comparables ; aucun prix fictif |
| Continuité | Engagements de service, reprise, défaillance et secours | Mêmes exigences, validées sur offre et architecture réelles | Objectifs métier, contrat et test de reprise |

La [qualification SecNumCloud](https://cyber.gouv.fr/enjeux-technologiques/cloud/) porte sur une offre définie et apporte des garanties sur celle-ci ; elle ne certifie pas automatiquement le CRM ou la configuration du client. Une appellation « souveraine » doit être étayée. Aucun des faits du dossier ne démontre une obligation générale de migrer tous les actifs d’ÉnergieAlp vers SecNumCloud.

### 5.2. Recommandation proposée pour ÉnergieAlp

**Proposition : instruire une migration ciblée de la partie sensible du CRM, tout en préparant un maintien transitoire encadré pour préserver le service ; décider séparément pour l’analytics après examen des données individuelles et des garanties réelles.** Ce choix est une orientation prudente fondée sur la sensibilité et les lacunes contractuelles, sans affirmer que CloudPeak est illégal par nature ou qu’un autre fournisseur éliminerait tout risque.

| Étape | Travail / condition de passage | Responsable et preuve |
| --- | --- | --- |
| 1 — Contenir et clarifier | Recenser données et droits, demander éléments juridiques/techniques, lancer contractualisation ; éviter de nouveaux usages non évalués | DSI et RSSI, appui juridique proposé ; P-02 et décision tracée |
| 2 — Évaluer le maintien | Maintien durable seulement si garanties juridiques/techniques suffisantes, contrat et risque résiduel examinés par les instances compétentes ; sinon déclencher scénario de sortie | Direction pour orientation/ressources ; RSSI pour dérogation de sécurité uniquement. Une tolérance interne ne légalise pas un traitement illicite |
| 3 — Piloter une cible | Comparer au moins deux offres sur le même périmètre ; privilégier l’examen d’une offre qualifiée pour les données sensibles ; tester compatibilité, contrôle des clés, reprise et coût | DSI avec métiers et RSSI ; grille comparative, devis et tests. Aucun fournisseur sélectionné ici |
| 4 — Décider par jeu de données | CRM : protéger données clients/IBAN ; analytics : déterminer si les données individuelles restent nécessaires et si les garanties permettent le maintien | Décision motivée par périmètre, conditions, risque résiduel, coût et date de réexamen |
| 5 — Migrer si décidé | Sauvegarde et restauration préalables, synchronisation et intégrité vérifiées, bascule en fenêtre validée, critères de succès et retour arrière | DSI, validation métier ; CRM disponible selon contrainte du dossier. Maintien de l’ancienne instance seulement dans un périmètre approuvé |
| 6 — Clore la sortie | Valider métier, retirer accès/sessions, récupérer données et configurations, traiter conservation/effacement selon obligations | Procès-verbal de recette, accès retirés, restitution et preuve d’effacement si applicable |

Si des faits établissent une non-conformité juridique nécessitant une action immédiate, faire arbitrer sans attendre le calendrier indicatif. Le maintien transitoire proposé n’est ni approuvé ni exécuté ; il ne dispense pas de traiter l’absence de contrat.

## 6. Politique de sécurité simplifiée — proposition V0

**État : rédigée pour revue, non adoptée.** Les règles ci-dessous indiquent le résultat, le périmètre, le responsable et le contrôle. Les fréquences sont proposées pour l’exercice, à confirmer selon risques et organisation. Elles reprennent les lignes M de la présente matrice et les actifs EA du registre.

### 1 — Objet et périmètre

- Protéger l’exploitation électrique, les services clients et les données sur EA-01 à EA-05 et leurs dépendances confirmées ; intégrer cloud et accès des prestataires. **Direction** approuve le périmètre proposé par DSI/Production avec RSSI. **Contrôle :** rapprochement annuel et après changement majeur entre politique, registre et matrice. **Liens : M-03, M-06, M-16 ; A-04/A-06.**

### 2 — Organisation de la sécurité

- **Direction :** approuver politique, moyens et arbitrages ; suivre les écarts et se former. **RSSI :** coordonner risques, incidents et contrôles ; valider seul les dérogations de sécurité, avec motif, périmètre, mesures compensatoires et date de fin. **DSI :** porter CRM, VPN et analytics ; **Responsable Production :** porter supervision ; propriétaire des compteurs à désigner. **Utilisateurs :** respecter habilitations et signaler les événements suspects. **Contrôle :** responsabilités nominatives, décisions et revue du suivi proposée trimestrielle. **Liens : M-06/M-10 ; A-06.**

### 3 — Gestion des actifs

- **DSI/Production** tiennent le registre avec identifiant, propriétaire, données, dépendances, criticité justifiée, version/support et emplacement ; ajout ou retrait déclenche une mise à jour. Toute cotation est validée par le métier concerné. **Contrôle :** rapprochement proposé trimestriel et après changement ; conserver historique et exclusions. **Liens : EA-01 à EA-05 ; M-03/M-09 ; registre incomplet, A-04.**

### 4 — Contrôle des accès

- **DSI**, après accord du responsable du système, attribue des accès nominatifs limités au besoin ; applique MFA aux accès VPN sensibles après essais, sépare administration/usages et retire les droits en fin de mission. Les accès tiers ont une date de fin et une revue proposée trimestrielle. **Contrôle :** approbations, tests autorisé/refusé, expiration et retrait ; exceptions bornées validées par RSSI. **Liens : M-01/M-04 ; VPN sans MFA et revues absentes, A-01/A-03.**

### 5 — Sécurité physique des sites et équipements

- **Production** pour supervision/terrain et **DSI** pour locaux SI, rôles proposés à confirmer, réservent l’accès physique aux personnes habilitées ; définissent accueil des visiteurs, protection des équipements et mesures face aux pertes d’énergie et risques environnementaux. **Contrôle :** liste des zones et droits, revue proposée trimestrielle et contrôle d’un scénario autorisé. **Liens : M-07/M-13 ; contrôles non documentés, A-04.**

### 6 — Gestion des incidents

- **Utilisateurs et prestataires** signalent rapidement les événements au contact interne désigné ; **DSI/Production** préservent les traces, qualifient avec **RSSI** et appliquent l’escalade. Le RSSI organise les notifications requises avec la direction et les rôles formalisés, selon critères et délais de l’article 23 et modalités nationales vérifiées. **Contrôle :** procédure, annuaire, chronologie et exercice proposé semestriel ; distinguer incidents significatifs, autres événements et violation de données personnelles. **Liens : M-05/M-14 ; procédure non décrite, A-05.**

### 7 — Continuité et reprise d’activité

- **DSI/Production avec les métiers** définissent les objectifs de reprise et perte admissible par actif, organisent sauvegardes, restauration et modes dégradés ; planifient les changements selon les fenêtres du dossier. Toute modification prévoit tests et retour arrière. **Contrôle :** restauration isolée proposée semestrielle et après changement majeur, mesures comparées aux objectifs approuvés, exercice de crise. **Liens : EA-01/EA-03 prioritaires ; M-08 ; reprise non documentée, A-05.**

### 8 — Gestion des sous-traitants

- **Responsable interne du service**, avec RSSI et appui juridique proposé, évalue le fournisseur avant engagement ou changement ; formalise accès, sécurité, incidents, sous-prestataires, continuité et sortie dans les engagements appropriés. Relier GridSoft, CloudPeak et RéseauTech aux actifs et aux risques RC-01 à RC-05, puis à la future matrice des risques fournisseurs. **Contrôle :** dossier fournisseur proposé annuel, revue des accès trimestrielle et après changement ; PR-ST-01 à PR-ST-04 ci-dessous. **Liens : M-02/M-04/M-09 ; contrat et analyse cloud absents, A-02/A-03.**

### 9 — Sensibilisation et formation du personnel

- **RSSI**, avec RH proposée et responsables opérationnels, organise accueil sécurité avant accès, rappel annuel et formation adaptée aux administrateurs, utilisateurs, direction et tiers selon leur mission. Inclure signalement d’incident, accès distant et protection des données. **Contrôle :** programme, participation et évaluation ; formation complémentaire selon difficultés observées. **Liens : M-11 ; formation non documentée, A-06.**

### 10 — Conformité et audit

- **RSSI avec appui juridique proposé** tient la matrice d’applicabilité et les sources à jour ; **DSI/Production** fournissent les preuves des contrôles, corrigent les écarts et testent l’efficacité avant clôture. Réduire exposition et vulnérabilités selon le risque, maîtriser chiffrement et clés ; coopérer aux demandes habilitées des autorités. **Contrôle :** revue proposée trimestrielle du plan et annuelle de la matrice, contrôle après incident/changement majeur ; aucune conformité déclarée sans preuve. **Liens : M-09/M-10/M-12/M-15/M-16 ; A-06.**

### 11 — Revue et mise à jour de la politique

- **RSSI** propose une révision annuelle et après incident significatif, changement fournisseur/architecture ou évolution juridique ; **direction** approuve, les responsables diffusent et organisent l’application. **Contrôle :** version, auteur, date, motifs, approbation et diffusion ; dérogations revues à leur échéance. La V0 reste conservée pour retracer les choix. **Liens : M-06/M-10/M-16 ; A-06.**

## 7. Procédures de gestion des tiers à joindre à la politique

| Procédure | Déclencheur / responsable proposé | Étapes et preuve de respect |
| --- | --- | --- |
| **PR-ST-01 — Évaluer** | Nouveau fournisseur, renouvellement ou changement ; DSI/Production avec RSSI | Décrire service, actifs, données, juridictions, sous-prestataires, accès et dépendances ; évaluer vulnérabilités et pratiques ; ouvrir risques RC ; conserver décision, réserves et responsable |
| **PR-ST-02 — Contractualiser** | Avant service ou régularisation ; responsable interne avec juridique proposé | Définir responsabilités, sécurité, notification d’incident, continuité, contrôle et réversibilité ; clauses RGPD selon rôle/flux ; conserver contrat signé et correspondance actifs/risques. CloudPeak à régulariser selon A-02 |
| **PR-ST-03 — Autoriser et revoir les accès** | Chaque mission puis revue proposée trimestrielle ; DSI et propriétaire de l’actif | Demande nominative avec besoin, droits, début/fin et fenêtre ; approbation ; configuration MFA/expiration ; test ; revue et retrait des droits inutiles. Conserver approbations, exports anonymisés et résultats |
| **PR-ST-04 — Gérer incident et sortie** | Incident, fin de mission/contrat ; responsable interne, RSSI, DSI/Production | Activer circuit incident et préserver traces ; à la sortie tester restitution/reprise, désactiver comptes/sessions, traiter les secrets partagés s’ils existent et effacement selon obligations ; conserver tests de refus, recette de sortie et attestations pertinentes |

GridSoft : EA-01, responsable Production ; canal d’accès exact à confirmer. CloudPeak : EA-03/EA-04, DSI ; analyse et contrat absents. RéseauTech : maintenance terrain/compteurs et VPN vers supervision, coordination Production/DSI. Aucun rôle de sous-traitant RGPD n’est déduit automatiquement d’une relation fournisseur : le qualifier selon le traitement.

## 8. Revue croisée et débrief formateur

**Grille à utiliser lors de l’échange ; aucune relecture par un autre binôme n’est attestée.** Les points de vigilance viennent de l’analyse documentaire, sans attribuer de propos au groupe.

| Contrôle de relecture | Point précis à vérifier | Preuve / décision à consigner après échange |
| --- | --- | --- |
| Criticité | Notes EA-04 I4 et D3 provisoires ; justification par dimension, propriétaire EA-02 | Auteur, actif, ancienne/nouvelle note, motif et validateur |
| Applicabilité | Hypothèse EE, exclusions article par article, source européenne versus droit national | Article, fait, réserve levée ou vérification à poursuivre |
| Traçabilité | Chaque rubrique de politique renvoie à un actif, une ligne M, un écart ou une action | Rubrique, référence manquante éventuelle et correction |
| Contrôle des règles | Résultat attendu, responsable, périmètre et preuve vérifiable | Test proposé, critère de réussite et responsable de collecte |
| Cloud Act | Juridiction et contrôle réel, distinction risque/transfert, clés et usage du clair | Question au fournisseur, pièce attendue et effet sur la décision |
| Faisabilité | Fenêtres, continuité, coût, compatibilité et retour arrière | Condition de mise en œuvre, arbitrage et délai |
| Adoption | La politique est-elle approuvée, diffusée et appliquée ? | À ce stade : **non documenté** ; ne pas confondre rédaction et adoption |

Conserver la production initiale, les commentaires attribués à leurs auteurs lorsqu’ils seront reçus, la version corrigée et le résultat du débrief seulement après réalisation. Pour le mémo public, utiliser des copies anonymisées sans données clients, secrets ni configurations sensibles.

## 9. Livrables et ressources

| Livrable | Disponible dans cette fiche | Reste à compléter sur preuves |
| --- | --- | --- |
| Registre et débrief | V0 liée, questions de méthode identifiées | Retours du groupe et validation des cotations |
| Matrice NIS2 | 46 articles examinés, M-01 à M-16, contrôles et actions associés | Sources nationales, exports/tests, décisions et états de conformité |
| Analyse Cloud Act | RC-01 à RC-05, comparaison et orientation conditionnelle | Réponses CloudPeak, offres/devis, analyse juridique et décision direction |
| Politique simplifiée | Onze rubriques et quatre procédures tiers proposées | Revue croisée, approbation, diffusion et application |

Sources consultées le **15 octobre 2026** :

- [Dossier ÉnergieAlp](../annexes/dossier-entreprise-energiealp.md) ; [registre V0](registre-actifs-critiques.md) ; [matrice du jour 1](../it-1/de-exigence-a-preuve.md).
- [Directive NIS2 — EUR-Lex](https://eur-lex.europa.eu/eli/dir/2022/2555/oj).
- [NIS2 et ReCyF — ANSSI](https://cyber.gouv.fr/reglementation/cybersecurite-systemes-dinformation/directives-nis-nis2-et-dispositif-saiv/directive-nis-2/).
- [Cloud et SecNumCloud — ANSSI](https://cyber.gouv.fr/enjeux-technologiques/cloud/) ; [FAQ qualification](https://cyber.gouv.fr/enjeux-technologiques/cloud/faq-qualification-secnumcloud/).
- [Cloud Act — DOJ, livre blanc](https://www.justice.gov/opa/press-release/file/1153446/dl).
- [Chiffrement cloud — CNIL](https://www.cnil.fr/fr/les-pratiques-de-chiffrement-dans-linformatique-en-nuage-cloud-public) ; [RGPD](https://www.cnil.fr/fr/reglement-europeen-protection-donnees).

[Retour à l’itération](index.md) · [Module](../README.md) · [Pense-bête](../../pense-bete/glossaire/droit-conformite/it-2.md)
