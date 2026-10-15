# Comprendre la conformité réglementaire

**Module : Droit et conformité — Itération 1 — 3 h 30 — Présentiel.**

## Objectif et résultat attendu

Identifier les sources d'exigences de cybersécurité, expliquer leur champ d'application et préparer une qualification argumentée d'ÉnergieAlp. À la fin de la séance, disposer d'un tableau des textes étudiés, de leurs obligations et sanctions, avec les raisons de leur applicabilité potentielle ou de leur exclusion.

!!! note "Statut de la fiche"
    Proposition de réponse documentaire du 15 octobre 2026, à discuter au débrief. Les faits proviennent du dossier fictif ; aucune recherche en groupe, utilisation du simulateur ou remédiation n'est attestée ici.

## 1. Déroulement fourni

| Étape | Contenu | Durée indiquée |
| --- | --- | --- |
| 1 | Ouverture : présentation du module, du kit apprenant et des livrables attendus sur trois jours | Non précisée |
| 2 | Mise en situation : intégrer l'équipe Conformité d'ÉnergieAlp ; qualifier son statut, auditer les écarts et préparer une simulation d'audit ANSSI. Lire le dossier entreprise dès maintenant | Non précisée |
| 3 | Positionner la conformité dans la GRC ; distinguer réglementation, norme, exigence contractuelle et politique interne | Non précisée |
| 4 | Panorama : RGPD, NIS2, LPM, Cloud Act, CRA, AI Act, DORA et cadres sectoriels tels que HDS. Approfondir surtout NIS2 et Cloud Act | Non précisée |
| 5 | Activité en groupe : rechercher les principales réglementations cyber, leurs caractéristiques et leur applicabilité potentielle à ÉnergieAlp | **20 min** |
| 6 | Mise en commun : quelques groupes partagent leur tableau et discutent leurs justifications | **10 min** |
| 7 | Présentation approfondie de NIS2 | Non précisée |

Les durées restantes sont à répartir par le formateur dans les 3 h 30 ; elles ne sont pas précisées dans la consigne.

## 2. La conformité dans la GRC

La **gouvernance** fixe les responsabilités et arbitre les décisions. La gestion des **risques** identifie les événements redoutés et les mesures adaptées. La **conformité** identifie les exigences applicables et rassemble les éléments permettant de démontrer leur respect.

La direction doit pouvoir justifier ses choix devant les autorités compétentes, ses clients, ses partenaires ou ses auditeurs, selon le texte ou l'engagement concerné. Pour ÉnergieAlp, le RSSI coordonne la sécurité ; le DSI et le Responsable Production portent les responsabilités opérationnelles définies dans le dossier. La responsabilité des organes de direction ne disparaît pas avec la délégation technique.

| Source | Logique d'applicabilité | Exemple | Preuve à rechercher |
| --- | --- | --- | --- |
| **Réglementation** | Champ défini par un texte : activité, territoire, taille, données, rôle | RGPD pour les traitements de données personnelles | Analyse d'applicabilité, registre, procédures et contrôles |
| **Norme** | Démarche volontaire, pouvant devenir une exigence contractuelle ou être citée par un texte | ISO/IEC 27001 | Périmètre du SMSI, audit ; certificat uniquement s'il existe |
| **Contrat** | Engagement accepté par les parties | Clauses de sécurité et de sous-traitance cloud | Contrat signé, annexes, contrôles de respect |
| **Politique interne** | Règles adoptées par l'organisation pour un périmètre donné | PSSI, procédure de revue des accès | Version approuvée, diffusion, application et dérogations |

Une certification ISO 27001 ne démontre pas à elle seule le respect de toutes les lois applicables. Une procédure rédigée doit être distinguée d'une procédure approuvée et effectivement mise en œuvre.

## 3. Panorama pour orienter les recherches

Ce tableau aide à commencer l'activité ; il ne remplace pas le livrable argumenté. Pour chaque texte, relever les articles et vérifier la version ainsi que les dates d'application.

| Texte | Champ d'application et obligations à étudier | Sanctions à rechercher | Piste pour ÉnergieAlp |
| --- | --- | --- | --- |
| **RGPD** | Traitements de données personnelles : licéité, droits, sécurité, sous-traitance, violations et transferts internationaux | Selon le manquement, plafonds de 10 M€ ou 2 % et de 20 M€ ou 4 % du CA annuel mondial, le montant le plus élevé étant retenu | CRM, compteurs et données individuelles ; analyser aussi les identifiants et journaux. Une agrégation ne prouve pas l'anonymisation |
| **NIS2** | Entités des secteurs visés : gouvernance, gestion des risques, chaîne d'approvisionnement et notification des incidents significatifs | Étudier l'article 34 : plafonds maximaux nationaux au moins égaux à 10 M€ ou 2 % pour les entités essentielles, 7 M€ ou 1,4 % pour les importantes, selon le montant le plus élevé ; distinguer ces dispositions du droit français applicable | Secteur électricité, taille et activité à confronter aux articles 2 et 3 et à l'annexe I ; qualification à argumenter en 1.2 |
| **LPM / régime OIV** | Dispositif français lié à la désignation OIV ; règles de sécurité des SI d'importance vitale, incidents et contrôles | Consulter le Code de la défense et les dispositions applicables au manquement étudié | La distribution d'électricité invite à vérifier une désignation ; le dossier n'en apporte aucune preuve |
| **Cloud Act** | Cadre américain d'accès légal aux données détenues par des fournisseurs relevant de sa juridiction ; analyser les demandes et le contrôle des données | Étudier les conséquences d'une injonction pour le fournisseur ; éviter de l'assimiler à une amende RGPD pour ÉnergieAlp | Groupe américain de CloudPeak : risque à analyser, sans en déduire un accès effectif ou un transfert déjà réalisé |
| **CRA** | Produits comportant des éléments numériques : obligations des fabricants, importateurs et distributeurs ; sécurité et gestion des vulnérabilités | Consulter le règlement (UE) 2024/2847, notamment l'article 64, selon le rôle et le manquement | Identifier les produits et les rôles. Être utilisateur d'un SCADA ne suffit pas à établir toutes les obligations d'un fabricant |
| **AI Act** | Obligations selon le rôle, l'usage et la catégorie de risque du système d'IA | Consulter les dispositions de sanctions et leur calendrier, selon l'infraction et l'acteur | Une plateforme analytics ne prouve pas l'usage d'une IA ; obtenir une description des systèmes avant de qualifier |
| **DORA** | Résilience numérique du secteur financier ; risque TIC, incidents, tests et prestataires | Vérifier les mesures et sanctions prévues par les autorités nationales, selon les dispositions applicables | Aucune activité financière visée n'est documentée ; un IBAN dans le CRM ne suffit pas à rendre DORA applicable |
| **HDS** | Certification pour certains hébergements de données de santé à caractère personnel, selon les conditions du Code de la santé publique | Rechercher les dispositions applicables à l'hébergement sans certification requise | Aucun hébergement de santé visé n'est décrit ; ne pas généraliser HDS à toutes les données personnelles |

Sources : [RGPD — CNIL](https://www.cnil.fr/fr/reglement-europeen-protection-donnees), [directive NIS2](https://eur-lex.europa.eu/eli/dir/2022/2555/oj), [dispositif SAIV — ANSSI](https://cyber.gouv.fr/reglementation/cybersecurite-systemes-dinformation/directives-nis-nis2-et-dispositif-saiv/dispositif-saiv/), [Cloud Act — DOJ](https://www.justice.gov/criminal/cloud-act-resources), [CRA — ANSSI](https://cyber.gouv.fr/reglementation/cybersecurite-des-produits/cyber-resilience-act/), [AI Act — Commission européenne](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai), [DORA — règlement](https://eur-lex.europa.eu/eli/reg/2022/2554/oj), [HDS — ANS](https://esante.gouv.fr/produits-services/hds).

## 4. Activité en groupe — 20 minutes

Les tableaux suivants proposent une réponse à partir du [dossier ÉnergieAlp](../annexes/dossier-entreprise-energiealp.md). Les sanctions sont des repères du texte concerné, conditionnés au manquement, au rôle et au calendrier applicables ; aucune sanction effectivement encourue par ÉnergieAlp n’est établie par cet exercice.

| Texte | Champ d'application | Principales obligations | Sanctions prévues par le texte |
| --- | --- | --- | --- |
| RGPD | Traitements de données personnelles ; CRM, relève individuelle et comptes d’accès d’ÉnergieAlp | Base légale, information et droits ; minimisation ; registre, sécurité, contrat de sous-traitance ; violations et transferts selon les conditions des art. 5, 6, 12–22, 28, 30, 32–34, 44–49 | Art. 83 : jusqu’à 10 M€ ou 2 %, ou 20 M€ ou 4 % du CA annuel mondial selon le manquement, montant le plus élevé ; mesures correctrices art. 58 |
| NIS2 | Secteurs des annexes I/II et critères de l’art. 2 ; distributeur d’électricité de 650 salariés : hypothèse EE justifiée dans la fiche 1.2 | Gouvernance et formation (20), risques/continuité/fournisseurs/accès (21), notification des incidents significatifs (23) | Art. 34 : maxima nationaux au moins égaux à 10 M€ ou 2 % pour EE, 7 M€ ou 1,4 % pour EI, montant le plus élevé ; modalités françaises à vérifier |
| LPM / OIV | Opérateurs désignés OIV et SI d’importance vitale concernés | Règles de sécurité, déclaration des incidents et contrôles : Code de la défense, L.1332-6-1 à L.1332-6-4 | L.1332-7 : notamment 150 000 € pour les dirigeants en cas de manquements visés ; vérifier l’infraction et les conditions précises |
| Cloud Act | Fournisseur relevant de la juridiction américaine et données sous sa possession ou son contrôle, même stockées hors des États-Unis | Réponse du fournisseur à une procédure légale valide ; examiner juridiction, contrôle, contestation et conflits de lois | Pas de barème d’amende directement applicable à ÉnergieAlp au seul motif d’un hébergement cloud ; conséquences d’un refus d’injonction à apprécier dans la procédure du fournisseur |
| CRA — UE 2024/2847 | Produits comportant des éléments numériques et opérateurs économiques selon leur rôle | Sécurité des produits, vulnérabilités, documentation et conformité ; art. 14 applicable depuis le 11 septembre 2026, application générale le 11 décembre 2027 selon l’art. 71 | Art. 64 : jusqu’à 15 M€ ou 2,5 % pour exigences essentielles et obligations visées ; 10 M€ ou 2 % pour d’autres obligations ; 5 M€ ou 1 % pour certaines informations incorrectes, selon conditions |
| AI Act — UE 2024/1689 | Systèmes d’IA ; obligations selon fournisseur/déployeur, usage et risque | Pratiques interdites, maîtrise de l’IA, exigences des systèmes à haut risque et transparence selon rôle ; calendrier art. 113 à vérifier pour chaque obligation | Art. 99 : notamment jusqu’à 35 M€ ou 7 % pour pratiques interdites ; 15 M€ ou 3 % pour les obligations visées ; régime adapté aux PME et autres cas |
| DORA — UE 2022/2554 | Entités financières énumérées à l’art. 2 et cadre spécifique des prestataires TIC | Gestion du risque TIC, incidents, tests, contrats et suivi des prestataires | Art. 50–51 : sanctions et mesures administratives selon le dispositif national ; pas de plafond unique à transposer au distributeur d’électricité |
| HDS | Certains hébergements pour le compte de tiers de données de santé personnelles, conditions de L.1111-8 CSP | Certification de l’hébergeur pour le périmètre concerné et respect des exigences applicables | L.1115-1 CSP : 3 ans d’emprisonnement et 45 000 € pour l’infraction visée ; personnes morales selon L.1115-2 |

### Justification d’applicabilité au scénario

Sources consultées le **15 octobre 2026**. Les conclusions portent sur les faits fournis ; les questions non résolues sont conservées.

| Texte étudié | Fait du dossier mobilisé | Conclusion provisoire | Information manquante / vérification | Source et articles |
| --- | --- | --- | --- | --- |
| RGPD | Identité, adresses, IBAN et consommations individuelles ; cloud partiel du CRM | **Applicable** aux traitements personnels ; transferts internationaux à déterminer | Registre, finalités et bases légales, durées, rôles et clauses du fournisseur ; régions et accès hors EEE | [RGPD, art. 2–3, 5–6, 28, 30, 32 et 44–49](https://www.cnil.fr/fr/reglement-europeen-protection-donnees) ; [sanctions art. 83](https://www.cnil.fr/fr/reglement-europeen-protection-donnees/chapitre8) |
| NIS2 | Distribution d’électricité, environ 650 salariés, 30 M€ de CA | **Dans le champ de la directive sur les faits fournis ; EE proposée**, sous réserve du périmètre de calcul ; droit national à vérifier séparément | Périmètre juridique et données de groupe, effectif de référence, règles françaises applicables | [Directive, art. 2–3, 20–23, 34 et annexe I énergie](https://eur-lex.europa.eu/eli/dir/2022/2555/oj) |
| LPM / OIV | Activité électrique critique ; aucune désignation fournie | **À déterminer** ; EE ne signifie pas OIV | Justificatif de désignation et périmètre SIIV auprès des personnes habilitées, sans publication d’éléments sensibles | [Code de la défense, L.1332-1 et suivants](https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006166900/) |
| Cloud Act | CloudPeak, filiale européenne d’un groupe américain ; analyse et contrat absents | **Exposition juridique potentielle à analyser via le fournisseur** ; pas d’accès effectif ni de transfert avéré | Entité contractante, juridiction, contrôle technique/juridique des données et clés, procédures de demandes légales | [DOJ, livre blanc Cloud Act, juridiction et contrôle des données](https://www.justice.gov/archives/opa/press-release/file/1153446/dl) |
| CRA | SCADA et compteurs utilisés ; GridSoft éditeur/intégrateur | **Obligations directes d’opérateur économique non établies** pour ÉnergieAlp ; sujet à intégrer aux achats | Fabrication, importation, distribution ou modification substantielle éventuelles ; produits et versions concernés | [UE 2024/2847, art. 2–3, 13–23, 64 et 71](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) |
| AI Act | Analytics et prévision de charge ; usage d’IA non documenté | **À déterminer**, analytics ne suffit pas à prouver une IA | Présence d’un système d’IA, finalité, rôle et éventuelle fonction de sécurité dans l’électricité | [UE 2024/1689, art. 2–6, 26, 99, 113 et annexe III](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) |
| DORA | Distributeur d’électricité ; IBAN utilisés pour la clientèle | **Non applicable au périmètre d’activité décrit** comme entité financière ; aucune prestation TIC financière documentée | Revoir si une activité financière visée ou une prestation TIC pertinente apparaît | [UE 2022/2554, art. 2, 50–51](https://eur-lex.europa.eu/eli/reg/2022/2554/oj) |
| HDS | Aucune prestation d’hébergement de données de santé décrite | **Non applicable au périmètre décrit** ; données personnelles ne signifie pas données de santé | Revoir en cas de projet d’hébergement entrant dans L.1111-8 ; ne pas déduire une obligation HDS du seul traitement RH | [CSP, L.1115-1 à L.1115-2 et renvoi à L.1111-8](https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072665/LEGISCTA000006170997/) |

**Méthode :** identifier le texte, lire son champ, le confronter aux faits, relever les obligations et sanctions pertinentes, puis justifier la conclusion. Une absence d'information appelle une vérification ; elle ne prouve pas une exemption.

## 5. Mise en commun — 10 minutes

Présenter les textes retenus, un texte écarté avec justification et un point restant incertain. Comparer les sources et les articles utilisés. Corriger le tableau après discussion, en conservant les raisons des exclusions.

## 6. Introduction approfondie à NIS2

### Qualification : questions à traiter en activité 1.2

1. L'activité relève-t-elle d'un secteur et d'un type d'entité visés ? Vérifier l'**annexe I, secteur énergie, électricité**, notamment les gestionnaires de réseaux de distribution.
2. Quels critères de taille et quelles règles de calcul s'appliquent ? Utiliser les **650 salariés** et les **30 M€ de CA 2025**, sans conclure uniquement à partir du chiffre d'affaires. Identifier les informations de groupe et de périmètre nécessaires.
3. Comment les articles **2 et 3** distinguent-ils champ d'application, entité essentielle et entité importante ? Quelles exceptions faut-il examiner ?
4. Quel est le cadre français applicable au moment de l'exercice ? Séparer la directive européenne, sa transposition et les recommandations de préparation.
5. Que donne le simulateur ANSSI avec ces données ? Conserver les entrées, la date, le résultat et ses limites : une préqualification ne vaut pas décision officielle.

**Aucun résultat de simulateur n’a été obtenu dans cette fiche.** La qualification documentaire EE est argumentée dans la [fiche 1.2](de-exigence-a-preuve.md) ; sa confirmation reste distincte du simulateur.

### Obligations européennes à repérer

- **Article 20 :** approbation et supervision des mesures par les organes de direction, formation et responsabilités.
- **Article 21 :** mesures proportionnées de gestion des risques : analyse de risque, incidents, continuité, fournisseurs, vulnérabilités, contrôle de l'efficacité, hygiène, formation, cryptographie, actifs et accès. Le texte inclut le MFA ou l'authentification continue lorsque cela est approprié.
- **Article 23 :** pour les incidents significatifs, alerte précoce au plus tard sous 24 h, notification sous 72 h et rapport final généralement sous un mois après la notification ; étudier les conditions et cas particuliers du texte.
- **Articles 32 à 34 :** supervision, mesures d'exécution et sanctions ; distinguer les régimes des entités essentielles et importantes.

Référence : [directive (UE) 2022/2555 — texte officiel](https://eur-lex.europa.eu/eli/dir/2022/2555/oj). Ces repères portent sur la directive et ne fixent pas à eux seuls les modalités françaises applicables.

### ReCyF et cadre français

La [page ANSSI NIS2](https://cyber.gouv.fr/reglementation/cybersecurite-systemes-dinformation/directives-nis-nis2-et-dispositif-saiv/directive-nis-2/), consultée le **13 octobre 2026**, présente ReCyF comme un **document de travail**, non obligatoire par défaut. Vérifier son statut et sa version au moment de l'utilisation. La page de présentation ne suffit pas à établir l'ensemble du droit français en vigueur : consulter les textes publiés pour conclure juridiquement.

### Relier les faits aux preuves attendues

| Fait du scénario | Axe à examiner | Preuve à demander ou à construire |
| --- | --- | --- |
| Matrice NIS2 absente | Applicabilité et gouvernance | Qualification argumentée, matrice avec articles, périmètre, responsables et justificatifs |
| VPN sans MFA | Gestion des accès et risques | Analyse du risque, solution proposée, essais d'accès et continuité avant déploiement |
| Cloud sans analyse ni contrat | Fournisseurs et données personnelles | Analyse juridique et technique, contrat de sous-traitance si pertinent, garanties et contrôle des accès |
| Inventaire critique incomplet | Connaissance des actifs | Inventaire validé avec propriétaires, dépendances et criticité |
| Accès prestataires sans revue | Cycle de vie des habilitations | Comptes nominatifs, règles d'octroi et de retrait, revue datée et décisions |

Les mesures sont à proposer. Respecter les fenêtres validées et la disponibilité continue. Le Responsable Production porte la supervision ; le DSI porte CRM, VPN et analytics ; seul le RSSI valide une dérogation de sécurité selon le dossier.

## 7. Cloud Act : préparer l'analyse suivante

Rechercher l'entité contractante, la juridiction, les lieux d'hébergement, les accès d'administration, les sous-traitants, le contrôle des données et la gestion des clés. Un hébergement en Europe ne suffit pas à résoudre toute question d'accès extraterritorial ; l'appartenance à un groupe américain ne prouve pas qu'une demande d'accès a eu lieu. Étudier parallèlement le RGPD, notamment les articles 28, 32 et 44 à 49 selon les traitements et les flux identifiés.

Sources : [ressources officielles Cloud Act — DOJ](https://www.justice.gov/criminal/cloud-act-resources) et [RGPD — CNIL](https://www.cnil.fr/fr/reglement-europeen-protection-donnees).

## 8. Ressources du kit

- [Dossier entreprise ÉnergieAlp](../annexes/dossier-entreprise-energiealp.md)
- [RGPD — CNIL](https://www.cnil.fr/fr/reglement-europeen-protection-donnees)
- [NIS2 et ReCyF — ANSSI](https://cyber.gouv.fr/reglementation/cybersecurite-systemes-dinformation/directives-nis-nis2-et-dispositif-saiv/directive-nis-2/)
- [LPM 2024-2030 — Ministère des Armées](https://www.defense.gouv.fr/ministere/politique-defense/loi-programmation-militaire-2024-2030)
- [Cloud Act — DOJ](https://www.justice.gov/criminal/cloud-act-resources)
- [CRA — ANSSI](https://cyber.gouv.fr/reglementation/cybersecurite-des-produits/cyber-resilience-act/)
- [AI Act — règlement (UE) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng/)
- [DORA — guide AFG fourni dans le kit](https://www.afg.asso.fr/app/uploads/2023/12/AFG-GuidePro-DORA_2026-ok-w-pap.pdf) ; compléter par le texte officiel cité plus haut.
- [HDS — Agence du numérique en santé](https://esante.gouv.fr/produits-services/hds)
- [Simulateur NIS2 — lien fourni](https://messervices.cyber.gouv.fr/simulateur-nis2) ; [MonEspaceNIS2 — orientation actuelle depuis l'ANSSI](https://monespacenis2.cyber.gouv.fr/)

## Éléments à conserver

Tableau complété, articles cités, dates de consultation, justifications d'applicabilité et d'exclusion, questions ouvertes. Pour l'activité 1.2, ajouter le résultat daté du simulateur seulement après utilisation effective. Une simulation d'audit constitue un exercice pédagogique, sans valeur de contrôle officiel ANSSI.

[Séance suivante — De l’exigence à la preuve](de-exigence-a-preuve.md)

[Retour à l'itération](index.md) · [Pense-bête](../../pense-bete/glossaire/droit-conformite/it-1.md)
