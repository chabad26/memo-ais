# Analyser une PSSI existante

**Itération 5 — Travail individuel — 5 octobre 2026**

## 🎯 Objectif

Comprendre comment une PSSI définit des règles et des responsabilités, puis
analyser leur pertinence pour le cas File Browser. Cette lecture prolonge
[Identifier ce que la technique ne règle pas](identifier-ce-que-technique-ne-regle-pas.md).

## 1. Identifier le document réellement consulté

**Source :** [Université de Poitiers — Politique de sécurité des systèmes d’information](https://imedias.univ-poitiers.fr/images/medias/fichier/pssi-v1_1404811176958-pdf).
PDF de **14 pages**, consulté le 5 octobre 2026, fichier référencé `pssi-v1`.
Les références de page ci-dessous désignent les **pages du PDF, couverture
comprise**. La date d’approbation et le statut de politique actuellement en
vigueur ne sont pas établis par cette lecture ; le nom du fichier ne suffit
pas à les déterminer.

Les éléments décrivant Poitiers sont des synthèses du document cité ; les
adaptations et contrôles proposés pour File Browser sont une analyse du cas,
pas des règles déjà adoptées par l’université ou par le laboratoire.

## 2. Parcourir la structure

| Élément recherché | Repère dans le document | Lecture synthétique |
| --- | --- | --- |
| Objectifs | §1.3, p.3 | Confidentialité, disponibilité, intégrité |
| Périmètre et systèmes | §1.2, p.2 | Ensemble des SI, applications, réseaux et interconnexions |
| Personnes concernées | §1.5–2.1.4, p.3–5 ; annexe p.11–14 | Gouvernance, administrateurs, utilisateurs et partenaires selon leur rôle |
| Responsabilités | §1.5, p.3–4 ; §2.1, p.4–5 | Président/AQSSI, RSSI, i-médias, composantes et correspondants SSI |
| Catégories de règles | §2.1–2.4, p.4–10 | Organisation, données, sécurisation, mesure et incidents |
| Document complémentaire | Annexe, p.11–14 | Charte d’utilisation des moyens informatiques |

### Lire la formulation d’une règle

Le texte associe prescriptions, responsabilités, conditions et exceptions.
Par exemple, §2.3.7, p.7–8, formalise le filtrage ; §2.3.4, p.7, encadre les
accès. Le §2.3.8, p.8, traite du maintien de sécurité et le §2.4, p.8–10,
du contrôle. [Source : PSSI de Poitiers](https://imedias.univ-poitiers.fr/images/medias/fichier/pssi-v1_1404811176958-pdf)

Pour analyser une règle, rechercher son destinataire, son action, son objet,
ses conditions et la trace permettant un contrôle. Une règle formulée comme
un principe doit être déclinée en procédure, avec responsable, échéance et
critères de vérification. Ne pas ajouter à la source un délai chiffré qu’elle
ne fournit pas.

## 3. Analyser des règles pertinentes pour File Browser

**Applicable directement ?** apprécie le passage complet dans le contexte du
cas fil rouge, pas une conformité déjà démontrée du serveur. « Partiellement »
signifie que le principe est utile mais que les rôles, moyens ou procédures
doivent être adaptés.

| Sujet de la règle / repère | Objectif | Personnes ou systèmes concernés | Problème du cas fil rouge concerné | Applicable directement ? | Adaptation éventuellement nécessaire |
| --- | --- | --- | --- | --- | --- |
| Administration des serveurs — §2.3.1, p.6 | Attribuer l’administration | Administrateurs institutionnels et des composantes | Serveur livré, application posée par un autre service, frontière de maintenance floue | Partiellement | Remplacer les fonctions universitaires par les équipes réelles ; distinguer OS, Docker, image et application ; désigner propriétaire et suppléant |
| Contrôle d’accès — §2.3.4, p.7 | Encadrer droits et authentification | Utilisateurs, propriétaire du service, SI | Identifiants par défaut et partenaires externes à suivre | Partiellement | Définir comptes partenaires, durée, révocation et validation métier ; ne pas imposer l’annuaire universitaire au laboratoire |
| Sécurité des applications — §2.3.5, p.7 | Intégrer la sécurité au projet | Projets et décideurs SSI | Publication de File Browser sans suivi clair | Partiellement | Préparer une fiche de sécurité avant publication : données, accès, support, sauvegarde, mainteneur et décision d’exposition |
| Réseau — §2.3.7, p.7–8 | Maîtriser les flux | Réseau et serveurs | Exposition Internet du scénario maintenue dans le temps | Partiellement | Adapter les flux aux partenaires ; documenter publication, administration, filtrage, revue et test externe autorisé |
| Maintien de sécurité — §2.3.8, p.8 | Organiser le suivi technique | RSSI et moyens techniques | Versions anciennes et alertes sans traitement clair | Partiellement | Attribuer veille, qualification et correction à des équipes nommées ; prévoir échéances selon risque et remplacement d’une application sans maintenance |
| Sauvegarde — §2.2.1, p.5 | Préserver les données | Données et services | Migration de base et retour arrière | Partiellement | Définir périmètre config/base/documents, responsables et besoins de reprise ; tester une restauration de File Browser |
| Journalisation — §2.4.3–2.4.4, p.8–9 | Exploiter les traces | Services et acteurs SSI | Auditd installé mais suivi opérationnel à organiser | Partiellement | Choisir destinataires, événements utiles, protection, rétention justifiée et réaction aux pertes ou à la saturation |

Références des lignes : [PSSI de Poitiers, §2.2 à §2.4](https://imedias.univ-poitiers.fr/images/medias/fichier/pssi-v1_1404811176958-pdf).
Les objectifs sont reformulés ; aucune longue reproduction des règles n’est
nécessaire pour expliquer leur rapport avec le cas.

## 4. Transformer l’analyse en contrôles concrets

Ces contrôles sont **proposés pour le cas File Browser**. Ils complètent les
tests techniques J4/J5 mais n’ont pas été réalisés comme audit organisationnel.

| Règle analysée | Contrôle proposé | Preuve attendue |
| --- | --- | --- |
| Administration | Envoyer une alerte OS et une alerte application au circuit défini | Fiche de responsabilités ; deux prises en charge attribuées ; suppléant identifié |
| Accès | Comparer comptes actifs, partenaires et habilitations approuvées | Revue datée, décision métier et retrait d’un accès arrivé à échéance |
| Application | Examiner les conditions de mise en service et de maintenance | Fiche de sécurité approuvée ; support et responsable de remplacement identifiés |
| Réseau | Rapprocher les flux réellement ouverts de ceux autorisés | Inventaire de publication, justification métier et résultat de test externe |
| Maintien de sécurité | Suivre une alerte depuis réception jusqu’à décision | Composant/version/chemin, qualification, ticket, responsable, délai et preuve de clôture ou exception |
| Sauvegarde | Restaurer base et documents sur une copie de test | Compte-rendu de restauration et contrôle des données ; sauvegarde source préservée |
| Journalisation | Produire un événement et vérifier son traitement | Trace, réception, destinataire, action et contrôle de l’espace disponible |

Une politique peut attribuer une responsabilité sans préciser toutes les
commandes. La procédure d’exploitation doit ensuite expliquer comment faire,
quand contrôler et où conserver les preuves. Une procédure écrite seule ne
prouve pas que son application est effective.

## 5. Adaptations et limites de transposition

Les termes DCSSI, CIL et les anciennes couleurs Vigipirate présents dans le
PDF signalent des références historiques. [Document consulté](https://imedias.univ-poitiers.fr/images/medias/fichier/pssi-v1_1404811176958-pdf)
Cette feuille ne fournit pas une analyse juridique de leur actualité. Avant
réemploi dans une politique en 2026, vérifier les autorités, textes applicables
et terminologies actuelles auprès des responsables compétents.

Pour File Browser, ne pas assimiler partenaire de partage documentaire et
prestataire d’infogérance : le premier accède à des documents, le second peut
administrer le SI. De même, une règle visant les postes utilisateurs ne devient
pas automatiquement la procédure de mise à jour d’un serveur.

La PSSI peut inspirer l’organisation du suivi, mais elle ne fournit pas ici un
plan complet de remplacement de File Browser ni les délais propres à notre
cas. Le cycle de vie, les budgets, les responsabilités applicatives et les
échéances doivent être explicités dans la proposition locale. L’exposition
Internet est celle du scénario pédagogique ; elle n’est pas démontrée pour
la VM du laboratoire.

## 📦 Résultat attendu

Une analyse sourcée de la structure et de plusieurs règles, avec leurs liens
au cas fil rouge, leur applicabilité et les adaptations nécessaires. Les
principes retenus doivent ensuite alimenter des propositions contrôlables,
sans prétendre recopier ou appliquer intégralement une PSSI d’un autre organisme.

**Bilan :** la PSSI donne un cadre de décision et de responsabilité ; le
compte-rendu technique apporte des preuves d’exécution. Pour éviter le retour
à une application ancienne sans suivi, il faut relier les deux par une
maintenance attribuée, une exposition justifiée et des contrôles périodiques.

- [Problèmes organisationnels du cas](identifier-ce-que-technique-ne-regle-pas.md)
- [Compte-rendu de durcissement et de vérification](finaliser-compte-rendu-durcissement-verification.md)
- [Retour à l’itération 5](index.md)
- [Retour au module](../README.md)
