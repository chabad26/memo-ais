# Définir les règles du cycle de vie d’un service

**Itération 6 — Travail individuel — 6 octobre 2026**

## 🎯 Objectif

Encadrer un service de son déploiement à son retrait avec des exigences
vérifiables, des destinataires et des responsables explicites.

**Statut : première version proposée, à valider.** Les délais et fréquences
ci-dessous sont des choix locaux à approuver avec les moyens nécessaires.
Cette fiche ne prouve ni leur adoption ni leur application au laboratoire.
Elle prolonge le [périmètre](definir-perimetre-fragment-pssi.md) et les
[rôles et responsabilités](definir-roles-responsabilites.md).

## 1. Partir des problèmes du cas

Le scénario décrit un service documentaire livré en 2021, encore exposé à
Internet en 2026, avec une application ancienne et une maintenance mal
attribuée. Cette exposition appartient au scénario ; elle n’est pas établie
pour la VM du laboratoire. Les travaux d’audit soulèvent également le suivi
des versions, des alertes et de la persistance des données. Une correction
technique ne garantit pas la maintenance future ni la décision de retrait.

La [PSSI publique de l’Université de Poitiers](https://imedias.univ-poitiers.fr/images/medias/fichier/pssi-v1_1404811176958-pdf),
consultée le 6 octobre 2026, inspire la structure : contexte et périmètre
(§ 1), organisation et responsabilités (§ 2.1), protection des données
(§ 2.2), puis exigences techniques. Les règles suivantes sont une rédaction
locale originale ; les délais ne sont pas attribués à Poitiers. La consultation
de cette version publique ne garantit pas qu’elle soit la dernière version.
Voir l’[analyse J5](../it-5/analyser-pssi-existante-poitiers.md).

## 2. Règles proposées

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

## 3. Grille de contrôle

Les méthodes, fréquences, rôles de revue et modalités de dérogation sont
précisés dans la section [Contrôles et exceptions](definir-controles-exceptions.md)
du fragment de PSSI.

Pour chaque service, conserver : règle CV, pièce attendue, référence/date de
preuve, résultat, écart, responsable et échéance.

| Résultat | Critère |
| --- | --- |
| Conforme | Preuves actuelles couvrant toutes les exigences applicables |
| Non conforme | Écart observé ; action et éventuelle exception référencées |
| Non vérifiable | Preuve absente ou contrôle non réalisé |
| Non applicable | Motif documenté et validé pour le périmètre |

Une exception reste un écart temporairement autorisé ; elle n’efface pas
l’exigence. Aucune règle n’est déclarée appliquée par la rédaction de cette fiche.

## 📦 Livrable attendu

Onze règles couvrant le cycle complet, avec attentes, destinataires,
responsables et contrôles. Avant adoption, valider nominations, délégations,
délais, fréquences, moyens et circuit de restriction urgente. Pour les services
existants, approuver un calendrier de mise en conformité en donnant priorité
aux expositions et aux couches sans mainteneur.

- [Rôles et responsabilités](definir-roles-responsabilites.md)
- [Propositions J5](../it-5/proposer-regles-adaptees-cas-fil-rouge.md)
- [Retour à l’itération 6](index.md)
- [Retour au module](../README.md)
