# Introduction aux normes SI

## Objectif

Comprendre les normes et règlements qui influencent un système d'information.

Le but n'est pas de faire une analyse juridique détaillée. Il faut comprendre :

- ce que la norme ou le règlement demande globalement ;
- qui est concerné ;
- quels acteurs apparaissent ;
- quels impacts cela a sur l'organisation ;
- ce que cela change pour un administrateur système.

## Ressources officielles

- [CNIL - Les grands principes du RGPD](https://www.cnil.fr/fr/comprendre-le-rgpd/les-six-grands-principes-du-rgpd)
- [CNIL - Responsable de traitement et sous-traitant](https://www.cnil.fr/fr/rgpd-comment-bien-identifier-son-role)
- [ANSSI - Directives NIS / NIS 2](https://cyber.gouv.fr/reglementation/cybersecurite-systemes-dinformation/directives-nis-nis2-et-dispositif-saiv/)
- [EUR-Lex - Règlement DORA](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32022R2554)
- [ISO - ISO/IEC 27001](https://www.iso.org/fr/standard/27001)

## Vue d'ensemble

| Texte | Nature | Idée principale | Public concerné |
| --- | --- | --- | --- |
| RGPD | règlement européen | protéger les données personnelles | tout organisme traitant des données personnelles |
| NIS2 | directive européenne | renforcer la cybersécurité des entités importantes ou essentielles | secteurs critiques et importants |
| DORA | règlement européen | renforcer la résilience numérique du secteur financier | banques, assurances, finance, prestataires TIC critiques |
| ISO 27001 | norme volontaire | organiser un système de management de la sécurité de l'information | toute organisation voulant structurer sa sécurité |

## Fiche RGPD

| Question | Réponse courte |
| --- | --- |
| Exigences principales | finalité, minimisation, sécurité, droits des personnes, conservation limitée, documentation |
| Acteurs concernés | responsable de traitement, sous-traitant, personnes concernées, DPO si nécessaire |
| Nouveaux acteurs | DPO, responsable de traitement, sous-traitants encadrés par contrat |
| Impacts organisationnels | registre des traitements, gestion des droits, sécurité des données, analyse d'impact si risque élevé |
| Obligatoire ? | oui, pour les organismes qui traitent des données personnelles dans le champ du RGPD |
| Impact admin système | gérer les accès, tracer, sécuriser, limiter les données, appliquer les durées de conservation, aider en cas de fuite |

### Exemple concret

Un hôpital traite des données de santé. Il doit limiter les accès au DPI, tracer les consultations, protéger les données et pouvoir répondre aux demandes des personnes selon le cadre applicable.

## Fiche NIS2

| Question | Réponse courte |
| --- | --- |
| Exigences principales | gestion des risques cyber, mesures de sécurité, notification d'incidents, gouvernance, contrôle |
| Acteurs concernés | entités essentielles et importantes dans des secteurs critiques ou importants |
| Nouveaux acteurs | autorité nationale, référents cybersécurité, direction impliquée, CSIRT/CERT |
| Impacts organisationnels | pilotage cyber, procédures d'incident, cartographie, sécurité fournisseurs, continuité |
| Obligatoire ? | oui pour les entités entrant dans le périmètre après transposition nationale |
| Impact admin système | durcir les systèmes, documenter, superviser, remonter les incidents, appliquer les règles de sécurité |

### Exemple concret

Une organisation critique doit être capable d'identifier ses actifs, protéger ses accès, détecter les incidents et notifier les événements importants.

## Fiche DORA

| Question | Réponse courte |
| --- | --- |
| Exigences principales | gestion du risque TIC, tests de résilience, gestion des incidents, gestion des prestataires TIC |
| Acteurs concernés | entités financières : banques, assurances, services d'investissement, etc. |
| Nouveaux acteurs | responsables de résilience numérique, autorités de supervision, prestataires TIC critiques |
| Impacts organisationnels | contrats fournisseurs, tests, plans de continuité, reporting incident, gouvernance des risques TIC |
| Obligatoire ? | oui pour les entités financières concernées par le règlement |
| Impact admin système | documenter les actifs TIC, tester la reprise, suivre les prestataires, préparer les preuves et rapports |

### Exemple concret

Une banque qui dépend d'un fournisseur cloud doit gérer ce risque fournisseur, prévoir des tests, suivre les incidents et prouver sa capacité de reprise.

## Fiche ISO 27001

| Question | Réponse courte |
| --- | --- |
| Exigences principales | mettre en place un SMSI, analyser les risques, choisir des mesures, améliorer en continu |
| Acteurs concernés | toute organisation qui veut structurer ou certifier sa sécurité |
| Nouveaux acteurs | responsable SMSI, auditeurs, pilotes de risques, propriétaires d'actifs |
| Impacts organisationnels | politiques sécurité, gestion des risques, preuves, audits, amélioration continue |
| Obligatoire ? | non en général, sauf exigence contractuelle ou sectorielle |
| Impact admin système | appliquer les contrôles, produire des preuves, gérer les accès, sauvegardes, logs, incidents |

### Exemple concret

Une entreprise veut rassurer ses clients : elle structure ses processus sécurité, documente ses risques et prépare une certification ISO 27001.

## Comparaison rapide

| Critère | RGPD | NIS2 | DORA | ISO 27001 |
| --- | --- | --- | --- | --- |
| Sujet central | données personnelles | cybersécurité des entités critiques | résilience numérique financière | management de la sécurité |
| Type | règlement | directive | règlement | norme |
| Obligation | oui si traitement de données personnelles | oui si entité dans le périmètre | oui si entité financière concernée | volontaire sauf exigence |
| Logique | protéger les personnes | protéger les services essentiels | protéger la continuité financière | structurer la sécurité |
| Effet sur l'admin | sécurité, accès, traces, conservation | durcissement, supervision, incident | reprise, tests, fournisseurs TIC | preuves, contrôles, amélioration |

## Déroulement de l'activité

### a) Répartition des normes

Chaque groupe choisit une norme ou un règlement :

- RGPD ;
- NIS2 ;
- DORA ;
- ISO 27001.

### b) Analyse

Pour la norme ou le règlement choisi, compléter la fiche suivante.

| Question | Notes du groupe |
| --- | --- |
| Norme / règlement étudié | |
| Exigences principales | |
| Acteurs concernés | |
| Nouveaux acteurs ou rôles qui apparaissent | |
| Impacts sur l'organisation | |
| Conditions d'application : obligatoire ? pour qui ? | |
| Impact sur le travail d'un administrateur système | |
| Exemple concret lié au module | |

### c) Préparation restitution

Préparer une restitution courte de 5 minutes.

Structure possible :

1. présenter la norme ou le règlement ;
2. expliquer qui est concerné ;
3. donner 2 ou 3 exigences principales ;
4. montrer un exemple concret d'impact sur le SI ;
5. expliquer ce que cela change pour un administrateur système.

## Conseils

- Rester au niveau global.
- Éviter le détail juridique.
- Privilégier des exemples concrets.
- Relier aux activités vues dans le module : cartographie SI, risques, accès, sauvegardes, conformité.

## Livrables

- présentation orale courte ;
- notes de groupe.

## Notions acquises

- normes SI : RGPD, NIS2, DORA, ISO 27001 ;
- gouvernance ;
- impact organisationnel ;
- lien entre exigences réglementaires et travail technique.

## Compétence travaillée

Identifier et prioriser les risques d'un SI.

## À retenir

Les normes et règlements ne sont pas seulement des textes.

Ils changent le SI parce qu'ils imposent ou encouragent :

- de documenter ;
- de tracer ;
- de sécuriser les accès ;
- de gérer les incidents ;
- de tester la continuité ;
- de mieux encadrer les prestataires ;
- de prouver que les mesures sont réellement appliquées.
