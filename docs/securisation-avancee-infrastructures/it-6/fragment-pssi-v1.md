# Fragment de PSSI — V1

**Encadrement des systèmes et applications administrés hors de l’équipe informatique principale**

| Identification | Valeur |
| --- | --- |
| Version | **V1 — version de référence conservée** |
| Date | 6 octobre 2026 |
| Rédaction | Travail individuel d’Olivier HIMBLOT, dans le cadre de la formation AIS |
| Statut | Première version consolidée ; adoption organisationnelle à valider |
| Base de consolidation | Fiches J6 et test documentaire des situations A–E |
| Prochaine évolution | V2 après analyse du retour d’expérience de l’incident |

Cette V1 constitue le document autonome de référence pour les journées
suivantes. Les fiches de préparation restent des supports de travail.
Les formulations prescriptives ci-dessous définissent les exigences proposées ;
elles ne prouvent ni leur adoption ni leur application à une infrastructure.
Les personnes, mandats, moyens et délais doivent être validés avant adoption.

## 1. Objectif, périmètre et interfaces

Assurer qu’un service garde un propriétaire, une maintenance attribuée,
un suivi des risques et une décision de fin de vie, même lorsque son
administration est assurée en tout ou partie par un service métier, une autre
équipe ou un prestataire.

Le fragment couvre les services nouveaux et existants, internes ou exposés
à des partenaires. Une seule couche administrée hors équipe principale
suffit à entrer dans le périmètre. Il couvre demande, autorisation, exploitation,
changements, transfert, exceptions et retrait.

Les ressources concernées sont : VM/hébergement, OS, runtime, application,
image et dépendances, configuration, données, sauvegardes, comptes et accès,
flux/publication, inventaire, alertes, journaux et preuves. Les responsabilités
sur chaque couche doivent être explicitement acceptées.

La fourniture d’une VM ou une aide ponctuelle ne transfère pas implicitement
la maintenance applicative à l’équipe principale. L’externalisation ne supprime
pas le propriétaire interne, le contrôle sécurité ni l’autorité de décision.
Une modification de répartition nécessite une passation formalisée.

Ce fragment ne remplace pas la PSSI complète, les procédures techniques,
la gestion de crise ni les politiques RH, juridiques et achats. Leurs
interfaces et règles communes doivent être identifiées avant adoption.
Une application entièrement administrée par l’équipe principale est hors du
périmètre pour sa gestion interne ; ses interfaces avec un service délégué
restent couvertes. Aucune autorisation de déployer ou publier n’est implicite.

Le cas File Browser motive ces exigences : application ancienne, exposition
durable et maintenance mal attribuée dans le scénario. L’exposition Internet
du scénario ne constitue pas une preuve pour la VM du laboratoire.

## 2. Rôles et maintien des responsabilités


| Rôle | Responsabilités proposées | Limite du rôle |
| --- | --- | --- |
| Demandeur habilité | Formaliser le besoin, les utilisateurs, les données et la durée envisagée ; obtenir le soutien du responsable métier | Une demande ne vaut pas autorisation de déployer ou de publier |
| Propriétaire du service | Porter le besoin métier et le suivi du service ; valider habilitations et fonctionnement ; organiser les moyens ; proposer maintien, remplacement ou retrait | N’administre pas automatiquement les couches techniques ; ne peut accepter un risque au-delà de sa délégation |
| Autorité d’autorisation | Approuver déploiement, changements d’exposition, exceptions et arbitrages selon un mandat explicite | Son approbation ne transfère pas l’exécution à l’équipe informatique |
| Responsable technique du système | Coordonner les couches et leurs mainteneurs ; tenir l’inventaire, les contacts et le suivi de maintenance ; signaler les lacunes | Ne doit pas être présumé exécuter les tâches de toutes les équipes |
| Équipe informatique principale | Maintenir les couches et interfaces convenues ; maîtriser raccordement, flux et publication ; contribuer à l’évaluation | La fourniture d’une VM ne signifie pas la maintenance de l’application |
| Administrateur système délégué | Administrer les couches système qui lui sont confiées, appliquer correctifs et procédures, sauvegarder selon répartition et remonter les difficultés | Aucune responsabilité sur une couche non attribuée ni publication sans autorisation |
| Mainteneur applicatif | Administrer application/image/dépendances/base, qualifier les alertes pertinentes, préparer mises à jour et tests | Un accès administrateur ne lui donne pas seul le pouvoir d’accepter un risque métier |
| Référent sécurité | Coordonner veille et qualification, recommander les mesures, suivre écarts et escalades, contrôler le dispositif | Ne remplace ni les mainteneurs ni l’autorité de décision |
| Suppléant désigné | Assurer la continuité d’un rôle avec accès et compétences adaptés | Sa désignation doit être vérifiée ; un nom sans moyens ne suffit pas |

Un prestataire éventuel occupe les rôles techniques prévus par son contrat ;
un propriétaire interne et un interlocuteur de suivi restent désignés.
Les partenaires utilisateurs n’assurent pas la maintenance du seul fait qu’ils
accèdent aux documents.

Une même personne peut cumuler plusieurs fonctions. La fiche de service doit
alors préciser dans quel rôle elle demande, exécute ou approuve. Les décisions
sensibles suivent le circuit de validation défini, même en cas de cumul.

## 3. Règles applicables au cycle de vie


### CV01 — Autoriser la mise en service

- **Attendu :** avant ouverture aux utilisateurs, constituer une fiche précisant besoin, données et sensibilité, utilisateurs, durée prévue, architecture, flux, maintenance par couche, support, sauvegarde/restauration et risques résiduels. Obtenir une décision datée de l’autorité après avis sécurité et tests fonctionnels. Lever les réserves bloquantes ou obtenir une exception CV09 avant ouverture. Fournir une VM ne vaut pas autorisation de publier l’application.
- **S’applique à :** demandeurs et exploitants de services nouveaux ou remplacés dans le périmètre.
- **Responsable :** propriétaire pour le dossier ; autorité d’autorisation pour la décision ; exploitants pour respecter ses conditions.
- **Vérification :** comparer date d’ouverture, approbation, réserves et résultats des tests. Une autorisation absente constitue un écart.

### CV02 — Identifier les responsables

- **Attendu :** avant ouverture, nommer propriétaire, responsable technique, référent sécurité, autorité et suppléants. Attribuer explicitement OS, runtime, application/image/dépendances, réseau, données et sauvegardes à des mainteneurs ayant accepté leurs tâches et disposant des moyens nécessaires. Aucun périmètre ne doit rester sans porteur.
- **S’applique à :** services nouveaux et existants, équipes internes et prestataires concernés.
- **Responsable :** propriétaire pour les désignations ; responsable technique pour la répartition par couche.
- **Vérification :** fiche acceptée, contacts et délégations ; faire attribuer une alerte OS puis une alerte applicative sans ambiguïté.

### CV03 — Inventorier le système et ses composants

- **Attendu :** avant ouverture, inventorier identifiant du service, hôte/VM, OS, runtime, image avec version et digest, application, dépendances identifiables, stockage persistant, configuration, sauvegardes, flux, mainteneurs et fins de support connues. Chaque information inconnue reçoit une action de recherche et une échéance. Actualiser l’inventaire à chaque changement avant clôture du ticket.
- **S’applique à :** toutes les couches du service, y compris celles confiées à un prestataire.
- **Responsable :** responsable technique ; chaque mainteneur renseigne sa couche.
- **Vérification :** rapprocher inventaire et versions réelles, inspection des conteneurs/montages et configurations réseau. Pour File Browser, vérifier où résident base et fichiers et leur conservation après recréation.

### CV04 — Encadrer l’exposition réseau

- **Attendu :** avant toute ouverture ou modification, faire approuver une matrice source/destination/protocole/port/usage/protection/durée. Refuser par défaut les flux non autorisés. Le partage externe utilise un canal chiffré et des habilitations validées ; supprimer les secrets initiaux avant ouverture. L’administration passe par un accès restreint approuvé, par exemple VPN ou bastion ; aucune interface administrative ne doit être librement accessible depuis Internet. Toute dérogation suit CV09.
- **S’applique à :** publications internes/externes, flux applicatifs et accès administratifs.
- **Responsable :** propriétaire justifie ; autorité approuve après avis sécurité ; équipe réseau et mainteneurs appliquent.
- **Vérification :** comparer matrice et règles effectives ; tests autorisés depuis zones admises et interdites, contrôle du chiffrement et des accès.

### CV05 — Organiser la maintenance

- **Attendu :** avant ouverture, documenter démarrage/arrêt, diagnostic, supervision, sauvegarde, restauration et escalade. Examiner chaque semaine les échecs de sauvegarde, alertes opérationnelles et échéances ; les urgences suivent immédiatement le circuit d’incident défini. Tester une restauration isolée avant ouverture, puis chaque trimestre et après changement du mécanisme de sauvegarde ; vérifier données et fonctionnement restaurés.
- **S’applique à :** exploitants du système, de l’application, des données et des sauvegardes.
- **Responsable :** responsable technique organise ; mainteneurs exécutent ; propriétaire valide le fonctionnement métier.
- **Vérification :** procédures accessibles aux suppléants, relevés de suivi, rapports de restauration et tickets d’échec. Une sauvegarde réussie seule ne prouve pas la restaurabilité.

### CV06 — Appliquer les mises à jour

- **Attendu :** examiner chaque mois les correctifs disponibles sur toutes les couches. Chaque mise à jour retenue possède un ticket avec versions avant/après, impact, tests, sauvegarde cohérente, retour arrière, fenêtre et résultat fonctionnel. Les délais CV07 priment sur ce calendrier. Tout report au-delà du délai exige CV09 avant échéance. Préparer les migrations avant les fins de support connues.
- **S’applique à :** OS, runtime, image, application et dépendances gérées.
- **Responsable :** mainteneur de chaque couche ; responsable technique coordonne ; propriétaire valide fenêtre et fonctionnement.
- **Vérification :** versions effectives, tickets et calendrier ; conserver résultats des contrôles de correction et de reprise, pas seulement les commandes lancées.

### CV07 — Suivre les vulnérabilités

- **Attendu :** désigner les destinataires des avis éditeur/CERT et organiser une veille hebdomadaire. Enregistrer les alertes concernant les composants inventoriés avec applicabilité, exposition, impact, protections, priorité, responsable et échéance. Qualifier sous un jour ouvré une alerte d’exploitation active crédible sur un composant exposé ; décider d’une correction ou restriction sous 24 heures après confirmation. Qualifier les autres alertes sous cinq jours ouvrés ; traiter les risques élevés sous 15 jours calendaires et les autres sous 60 jours après qualification, ou appliquer CV09. Sans correctif, décider d’une protection, d’un remplacement ou d’un retrait.
- **S’applique à :** avis de sécurité et résultats de scans concernant le service.
- **Responsable :** référent sécurité coordonne et priorise avec les mainteneurs ; mainteneurs traitent ; autorité arbitre les risques.
- **Vérification :** registre daté, sources, justification d’applicabilité ou d’exclusion, décisions et recontrôles. Ni CVSS seul ni compteur Trivy ne suffisent ; revoir les exclusions si le contexte change.

**Circuit de notification et de décision :** le référent sécurité et les mainteneurs
nommés reçoivent les avis pertinents. Le premier informé ouvre un ticket et
notifie le référent sécurité, le responsable technique, le mainteneur concerné
et le propriétaire au plus tard sous un jour ouvré ; une urgence crédible est
signalée immédiatement par le canal d’escalade convenu. Le responsable technique
coordonne la correction avec le mainteneur dans le mandat de changement établi ;
le propriétaire valide les impacts métier. L’autorité décide des exceptions,
restrictions/suspensions et arbitrages dépassant ce mandat. L’équipe principale
est informée si ses couches ou interfaces sont affectées. Le référent sécurité
vérifie les preuves avant clôture ; une compensation temporaire laisse la
vulnérabilité ouverte et liée à CV09.

### CV08 — Contrôler périodiquement

- **Attendu :** chaque trimestre, vérifier inventaire, support, flux, habilitations, privilèges, restauration, collecte d’alertes, exceptions et utilité du service. Après un changement affectant une protection, refaire le contrôle pertinent avant clôture. Chaque écart reçoit un responsable et une échéance selon son risque ; examiner mensuellement les actions échues.
- **S’applique à :** tout service en exploitation, même si sa version reste inchangée.
- **Responsable :** responsable technique organise ; mainteneurs contrôlent ; référent sécurité examine résultats et écarts ; propriétaire confirme le besoin.
- **Vérification :** calendrier et rapports datés avec cible, méthode, résultat et pièces. Justifier les contrôles omis ; une absence d’alerte ne prouve pas la sécurité globale.

### CV09 — Gérer les exceptions

- **Attendu :** avant dérogation, enregistrer règle, périmètre, motif, risque, compensations vérifiables, propriétaire du risque, responsable de suivi et plan de sortie. Obtenir l’approbation de l’autorité après avis sécurité pour au maximum 90 jours. Vérifier mensuellement les compensations. Tout renouvellement exige une nouvelle décision avant échéance ; sinon appliquer la règle ou restreindre/suspendre le périmètre dérogatoire selon la procédure approuvée. Réexaminer immédiatement une aggravation du risque.
- **S’applique à :** reports de correctifs, défauts de support et autres écarts à CV01–CV11.
- **Responsable :** propriétaire demande ; référent sécurité analyse ; autorité approuve ; mainteneur applique ; responsable de suivi surveille l’échéance.
- **Vérification :** registre, approbation, dates, tests des compensations et sortie. Un compte-rendu de laboratoire ne constitue pas une acceptation du risque.

### CV10 — Transmettre les responsabilités

- **Attendu :** avant un départ ou changement prévu, désigner un entrant ayant accepté les tâches ; transmettre inventaire, procédures, alertes, tickets, exceptions, support et accès nécessaires. Tester sa prise en charge, actualiser les destinataires d’alertes et retirer les droits devenus inutiles à la date du changement. En cas d’absence imprévue, activer le suppléant dès notification. Sans couverture, l’autorité décide avant poursuite de l’exploitation d’une prise en charge temporaire ou restriction/suspension. Ne pas transmettre de clé privée personnelle.
- **S’applique à :** propriétaires, responsables techniques, mainteneurs et prestataires changeant de fonction.
- **Responsable :** propriétaire organise ; responsable technique conduit la passation ; équipes habilitées adaptent les accès ; autorité traite l’absence de couverture.
- **Vérification :** passation acceptée, accès testé, alertes reçues par l’entrant et révocation des droits du sortant.

### CV11 — Décider la fin de vie et retirer le service

- **Attendu :** disparition du besoin, fin de support annoncée ou absence de mainteneur déclenche un dossier de décision sous dix jours ouvrés. Le propriétaire propose remplacement, retrait ou exception ; l’autorité fixe échéance et moyens, avant fin de support lorsqu’elle est connue. Avant retrait, identifier les dépendances, informer les utilisateurs, restituer les données utiles et faire approuver conservation ou effacement. À la date prévue, supprimer publication et flux, révoquer comptes/secrets/certificats dédiés, arrêter puis retirer les ressources et clôturer l’inventaire. Les sauvegardes conservées restent protégées avec motif, responsable et date de suppression. Vérifier l’impact avant de supprimer une ressource partagée.
- **S’applique à :** application, VM/conteneurs, données, accès, DNS/publication, supervision et sauvegardes du service retiré.
- **Responsable :** propriétaire prépare décision et sort des données ; autorité approuve ; responsable technique coordonne l’exécution.
- **Vérification :** décision, checklist, restitution contrôlée, tests d’inaccessibilité depuis les zones auparavant desservies, accès révoqués et inventaire clôturé. Arrêter seulement le conteneur ne prouve pas un retrait complet.

**Service exposé dont l’usage ou le propriétaire est inconnu :** dès le constat,
l’équipe qui le découvre informe le référent sécurité et l’autorité. Celle-ci
désigne sous un jour ouvré un pilote provisoire disposant des moyens de
coordination. Le pilote examine l’exposition et recherche propriétaire,
utilisateurs, dépendances, données et support, avec un dossier sous dix jours
ouvrés. L’absence de preuve d’usage ne prouve pas l’abandon. L’autorité décide
et consigne dans ce même délai le maintien justifié, une restriction, un
remplacement ou un retrait ; toute dérogation suit CV09. Si un risque urgent
est identifié, appliquer le circuit de restriction immédiate prévu sans
attendre l’enquête. Ne pas effacer les données avant décision sur leur sort.

## 4. Programme de contrôles


Le responsable technique tient le calendrier et rassemble les preuves des
mainteneurs. Le propriétaire confirme le besoin métier et les responsables.
Le référent sécurité examine les résultats, suit les écarts et alerte
l’autorité d’autorisation. Lorsque cela est possible, la personne qui valide
le contrôle est distincte de celle qui a réalisé le changement ; sinon,
documenter le cumul et faire relire les résultats par un autre rôle compétent.

Chaque contrôle porte sur un service identifié et couvre toutes ses couches
applicables. Les tests réseau et restaurations sont réalisés avec autorisation,
dans un périmètre défini et sans altérer les données de production.

| Contrôle / règles | Méthode et critère de respect | Fréquence ou déclencheur proposé | Réalisation → revue | Preuves à conserver |
| --- | --- | --- | --- | --- |
| Autorisation — CV01 | Comparer ouverture effective, décision signée et conditions ; aucune réserve bloquante sans traitement ou exception valide | Avant ouverture ou remplacement ; revue trimestrielle des décisions applicables | Responsable technique → autorité | Fiche du service, décision, tests et réserves levées |
| Responsables — CV02, CV10 | Confirmer propriétaire, suppléants et mainteneurs par couche ; tester contact, réception d’une alerte et capacité de reprise. Chaque couche possède un porteur ayant accepté la tâche | Chaque trimestre ; avant changement prévu, dès notification d’une absence imprévue | Propriétaire et responsable technique → référent sécurité | Désignations, confirmations, passation et tests d’accès/alerte |
| Utilité — CV08, CV11 | Faire confirmer usage, partenaires, données et durée par le propriétaire ; rapprocher cette confirmation d’indices d’activité disponibles. Une absence de connexion seule ne justifie pas un retrait si l’usage est saisonnier | Chaque trimestre ; disparition du besoin signalée | Propriétaire → autorité pour décision de maintien/retrait | Confirmation datée, indicateurs contextualisés, décision et prochaine revue |
| Inventaire et support — CV03, CV06 | Comparer inventaire aux versions réelles, digest, montages, dépendances et fins de support ; toute inconnue possède responsable et échéance | Chaque trimestre ; à chaque changement avant clôture | Mainteneurs, coordination technique → référent sécurité | Inventaire daté, sorties utiles, références de support et tickets |
| Maintenance — CV05 | Examiner alertes et échecs ; restaurer dans un environnement isolé et vérifier données et parcours métier | Suivi hebdomadaire ; restauration avant ouverture, trimestrielle et après modification du mécanisme | Mainteneurs → responsable technique et propriétaire pour le fonctionnel | Rapports de sauvegarde/restauration, résultats et tickets d’échec |
| Mises à jour — CV06 | Rapprocher correctifs disponibles, versions installées et tickets ; vérifier tests, retour arrière et reports approuvés. Aucune échéance dépassée sans exception valide | Chaque mois ; après mise à jour avant clôture | Mainteneurs → responsable technique | Veille de versions, ticket avant/après, tests et éventuelle exception |
| Vulnérabilités — CV07 | Vérifier réception des avis, applicabilité, priorité contextualisée, affectation et respect des délais CV07 ; vérifier la correction ou la compensation, et motiver chaque exclusion | Veille hebdomadaire ; traitement selon CV07 ; revue mensuelle des retards | Mainteneurs → référent sécurité | Registre, sources, qualification, horodatages, décisions et recontrôles |
| Exposition — CV04, CV08 | Faire confirmer le besoin d’exposition ; comparer flux approuvés, pare-feu, publication et écoute réelle ; tester accès autorisés/refusés et chiffrement depuis les zones pertinentes | Avant ouverture/modification ; chaque trimestre | Équipe réseau et mainteneurs → référent sécurité ; propriétaire confirme le besoin | Matrice approuvée, configuration, tests datés et justification métier |
| Exceptions — CV09 | Vérifier approbation, délégation, échéance, justification toujours actuelle, compensations effectives et progression du plan de sortie | Chaque mois ; avant échéance ; immédiatement si risque aggravé | Responsable de suivi → référent sécurité ; autorité renouvelle ou retire | Registre, tests des compensations, avis, décisions et plan de sortie |
| Retrait — CV11 | Vérifier restitution/conservation des données, fermeture des flux/publications, révocation des accès et retrait des ressources dédiées ; contrôler les dépendances partagées | À la date du retrait ; aux échéances de suppression des sauvegardes conservées | Responsable technique et mainteneurs → propriétaire et autorité | Checklist, tests d’inaccessibilité, révocations, inventaire clôturé et sort des sauvegardes |

Pour File Browser, comparer séparément hôte, runtime, image/application,
données et exposition. Un digest inchangé ne dispense pas de revoir les
nouvelles vulnérabilités connues. Un scan ne démontre pas à lui seul que le
besoin métier, la responsabilité ou l’autorisation restent valides.

En cas de service exposé sans usage confirmé ou propriétaire identifié,
appliquer le circuit ajouté à **CV11** : alerte dès constat, pilote provisoire
sous un jour ouvré et dossier/décision sous dix jours ouvrés. Pour les alertes
de vulnérabilité, appliquer le circuit de notification et de clôture de **CV07**.
Ces déclencheurs priment sur la revue périodique.

## 5. Résultats, preuves et écarts


Chaque fiche de contrôle contient : identifiant, service/périmètre, règle CV,
date et contrôleur, méthode, résultat attendu et observé, référence des preuves,
conclusion, relecteur, action, responsable et échéance.

| Conclusion | Traitement |
| --- | --- |
| Conforme | Preuves actuelles couvrant les exigences ; noter la prochaine revue |
| Non conforme | Ouvrir une action ; corriger ou demander une exception avant dépassement de l’échéance |
| Non vérifiable | Signaler la preuve manquante ; affecter sa collecte ou le contrôle avec échéance, sans conclure à la conformité |
| Non applicable | Documenter et faire valider le motif pour le périmètre ; réexaminer si celui-ci change |

Une exception approuvée est référencée comme **écart temporairement autorisé** ;
elle ne transforme pas le résultat en conformité à la règle d’origine.
Les actions échues sont examinées mensuellement par le référent sécurité.
Un danger urgent ou une compensation défaillante suit immédiatement le circuit
d’incident et de décision, sans attendre la revue mensuelle.

Conserver les pièces dans un espace à accès maîtrisé, avec auteur, date,
périmètre et référence du ticket. La fiche publique ne contient ni secrets
ni diagnostics internes complets. La durée de conservation des preuves doit
être fixée avant adoption selon les besoins de suivi de l’organisation.

## 6. Gestion des exceptions


1. **Demander :** le propriétaire identifie la règle précise et l’exigence impossible à respecter, le périmètre, la cause et les solutions examinées. Il propose une durée, un responsable de suivi et un plan de retour à la règle.
2. **Analyser :** les mainteneurs et le référent sécurité décrivent le scénario de risque, l’exposition, les données et impacts, les protections existantes et le risque résiduel après compensation. Un simple score de scanner ne suffit pas.
3. **Décider :** une personne nommée disposant de la délégation appropriée approuve ou refuse par écrit. Le demandeur ou l’administrateur ne s’autorise pas une dérogation sans mandat. L’avis du référent sécurité ne remplace pas cette décision.
4. **Activer :** vérifier les compensations requises avant la prise d’effet, enregistrer les dates, notifier les exploitants et programmer les contrôles. Une demande en attente n’autorise pas à dépasser une règle ; maintenir les restrictions nécessaires jusqu’à décision.
5. **Suivre :** vérifier mensuellement justification et compensations, suivre les étapes du plan de sortie ; réexaminer immédiatement tout changement d’exposition, de vulnérabilité ou de responsabilité affectant le risque.
6. **Réexaminer et clôturer :** avant échéance, apporter la preuve de correction ou demander une nouvelle décision justifiée. Aucun renouvellement tacite. À expiration sans renouvellement, appliquer la règle ou la restriction/suspension prévue par la procédure approuvée ; conserver la preuve de clôture.

La durée maximale proposée par **CV09 est de 90 jours**, avec une date de
réexamen antérieure ou égale à l’expiration. Ce plafond n’impose pas d’accepter
90 jours si le risque demande une durée moindre. Une exception ne peut couvrir
que le périmètre et les exigences expressément autorisés par le décideur.

## 7. Fiche d’exception obligatoire


| Champ obligatoire | Contenu attendu |
| --- | --- |
| Identifiant et service | Référence EX, service, composants/versions et périmètre exact |
| Règle concernée | Identifiant CV et exigence précise non respectée |
| Demandeur / propriétaire du risque | Personne nommée et contact |
| Justification | Cause, contrainte, solutions examinées et motif du choix temporaire |
| Risque accepté | Scénario, exposition, données/impacts et risque résiduel après compensation |
| Mesures compensatoires | Mesures, exécutants, preuves d’efficacité et fréquence des tests ; si aucune, justification explicite |
| Avis sécurité | Analyse datée, réserves et recommandation |
| Autorisation | Nom du décideur, délégation, décision datée et conditions ; refus possible |
| Durée | Date de prise d’effet, expiration et date de réexamen, dans la limite CV09 |
| Suivi | Responsable, contrôles prévus, alertes et critères de réexamen anticipé |
| Sortie | Correction/remplacement/retrait prévu, étapes, responsables et échéances |
| État et clôture | Demandée, refusée, approuvée, échue ou clôturée ; références des preuves et dernière décision |

## 8. Adoption et entrée dans le périmètre

Avant adoption, l’autorité valide les rôles nominatifs, suppléants et délégations,
les moyens techniques/humains, les calendriers, les délais CV07/CV09/CV11,
le canal d’alerte urgent et la procédure habilitant les restrictions/suspensions.
Cette procédure désigne qui peut exécuter une mesure conservatoire immédiate,
pour quel périmètre, avec notification et traçabilité. Sans ces désignations,
la préparation documentaire ne constitue pas une capacité opérationnelle vérifiée.

Chaque fiche de service renseigne besoin, données, partenaires, propriétaire,
responsable technique, mainteneurs par couche, suppléants, référent sécurité,
autorité, flux, support, sauvegarde/reprise, preuves et prochaines revues.
L’autorité examine la capacité de maintenance avant autorisation CV01.

Pour les services existants, le recensement déclenche une fiche, une analyse
des écarts et un calendrier de mise en conformité approuvé, avec responsables
et échéances. Prioriser les expositions et couches sans mainteneur. Ce calendrier
ne vaut pas exception : chaque dérogation suit CV09. Les situations urgentes
et services sans propriétaire suivent immédiatement CV07/CV11.

## 9. Conservation de V1 et révision après incident

| Version | État | Évolution |
| --- | --- | --- |
| V1 — 6 octobre 2026 | Première version consolidée conservée | Notification et clôture CV07 ; prise en charge provisoire et enquête CV11, issues du test A–E |
| V2 | À produire après REX | Aucun contenu ni résultat d’incident anticipé |

Le [test documentaire A–E](tester-fragment-pssi.md) a permis de préciser
CV07 et CV11. Il vérifie la possibilité de déterminer actions, rôles et preuves ;
il ne vérifie pas l’exécution réelle ni n’accepte un risque.
Les règles retenues comportent toutes une attente, des destinataires,
un responsable et une vérification. Les formulations générales sans critère
ne sont pas retenues comme règles autonomes.

Lors du REX, relever pour chaque difficulté la règle concernée, les faits et
preuves, les responsabilités, les délais observables et la modification
proposée. Conserver **cette page V1** ; créer une page V2 distincte avec tableau
des changements, justification et décision de validation. Aucun incident
n’est présenté comme déjà réalisé par cette consigne de révision.

## 10. Sources et travaux de préparation

La [PSSI publique de l’Université de Poitiers](https://imedias.univ-poitiers.fr/images/medias/fichier/pssi-v1_1404811176958-pdf),
consultée pendant la préparation J6, a servi de référence de structure et de
répartition des responsabilités. Les règles et délais de cette V1 sont des
propositions locales originales ; ils ne sont pas attribués à Poitiers.
La consultation ne garantit pas que ce document public soit sa dernière version.

- [Définir le périmètre](definir-perimetre-fragment-pssi.md)
- [Définir les responsabilités](definir-roles-responsabilites.md)
- [Rédiger les règles du cycle de vie](definir-regles-cycle-vie-service.md)
- [Définir contrôles et exceptions](definir-controles-exceptions.md)
- [Tester le fragment](tester-fragment-pssi.md)
- [Retour à l’itération 6](index.md)
- [Retour au module](../README.md)
