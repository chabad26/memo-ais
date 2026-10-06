# Définir les rôles et responsabilités

**Itération 6 — Travail individuel — 6 octobre 2026**

## 🎯 Objectif

Définir les responsabilités lorsqu’un système est exploité hors de
l’administration directe de l’équipe informatique principale. Couvrir la
prise de décision, l’administration, le maintien en sécurité et la fin de vie.

**Statut : organisation proposée pour le fragment de PSSI, à valider.**
Les fonctions ci-dessous ne sont pas des nominations réelles. Elles prolongent
le [périmètre J6](definir-perimetre-fragment-pssi.md) et les
[règles proposées J5](../it-5/proposer-regles-adaptees-cas-fil-rouge.md).

## 1. Rôles retenus

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

## 2. Répartir les responsabilités pendant le cycle de vie

Dans ce tableau, le **pilote** organise la prise en charge et le suivi ; le
**décideur** approuve dans sa délégation ; les **intervenants** exécutent ou
apportent leur expertise. Les destinataires sont informés selon leur périmètre.

| Question / activité | Pilote | Décideur | Intervenants et personnes informées | Trace attendue |
| --- | --- | --- | --- | --- |
| Qui peut demander un nouveau service ? | Demandeur habilité, soutenu par le propriétaire métier | Responsable métier valide la demande avant instruction | Informatique et sécurité consultées sur faisabilité/risque | Demande décrivant besoin, données, partenaires et durée |
| Qui autorise le déploiement ? | Propriétaire prépare le dossier | Autorité d’autorisation désignée | Responsable technique, informatique et sécurité rendent leurs avis | Approbation avec conditions, responsables et périmètre |
| Qui est responsable du système ? | Responsable technique nommé ; propriétaire reste porteur du service | Autorité valide les désignations et moyens | Mainteneurs de chaque couche et suppléants | Fiche de service et matrice de maintenance approuvées |
| Qui administre système et application ? | Responsable technique coordonne | Responsable de chaque équipe attribue ses tâches dans le cadre approuvé | Informatique ou administrateur délégué pour système ; mainteneur pour application | Répartition des couches, droits et procédures |
| Qui assure les mises à jour ? | Mainteneur de la couche concernée | Validation du changement par le rôle habilité ; propriétaire valide fenêtre et parcours métier | Infrastructure, administrateur délégué, mainteneur applicatif et sécurité selon l’impact | Ticket, versions/digest, tests, sauvegarde et retour arrière |
| Qui suit les vulnérabilités ? | Référent sécurité organise le circuit ; responsable technique suit la couverture | Autorité habilitée arbitre les priorités contestées | Chaque mainteneur surveille et qualifie ses composants | Alertes reliées à inventaire, responsable, échéance et décision |
| Qui décide l’exposition réseau/Internet ? | Propriétaire justifie le besoin et responsable technique décrit les flux | Autorité d’autorisation après avis sécurité et informatique | Équipe réseau applique ; mainteneurs et propriétaire informés | Décision de publication et flux autorisés, revue prévue |
| Qui est informé d’une vulnérabilité importante ? | Découvreur la remonte au circuit sécurité ; référent sécurité coordonne | Autorité concernée informée si arbitrage/urgence | Propriétaire, responsable technique, mainteneurs impactés et équipe principale si ses interfaces sont concernées | Notification datée, destinataires et accusé de prise en charge |
| Qui décide les mesures à prendre ? | Responsable technique prépare les options avec sécurité | Autorité habilitée arbitre interruption, retrait ou exception ; mainteneur applique les corrections déjà autorisées par procédure | Propriétaire précise l’impact métier ; équipes exécutent | Décision, motif, mesures, responsable et échéance |
| Qui vérifie périodiquement le maintien ? | Responsable technique tient le calendrier et les preuves | Propriétaire valide la continuité du besoin ; sécurité examine les écarts | Mainteneurs contrôlent les couches ; référent sécurité contrôle le suivi | Revue versions/support, accès, tests et actions en retard |
| Qui traite un départ ou changement de fonction ? | Responsable hiérarchique signale ; propriétaire organise le remplacement | Autorité ou responsable habilité approuve la nouvelle attribution | Sortant, entrant, informatique et sécurité selon les accès | Transfert accepté, accès actualisés, inventaire/alertes réaffectés |
| Qui décide fin de vie et retrait ? | Propriétaire propose et responsable technique prépare | Autorité habilitée approuve selon impact et règles de conservation | Mainteneurs et informatique retirent données/accès/flux ; partenaires informés selon besoin | Plan, décision, contrôles de retrait et clôture d’inventaire |

**Délais et fréquence :** à proposer selon criticité/exposition puis à valider.
Aucun délai chiffré n’est présenté comme une règle existante. Une urgence ne
doit pas rester sans contact ; les mesures immédiates autorisées et leur
notification doivent être définies à l’avance dans le circuit d’incident.

## 3. Application au serveur File Browser

| Couche / décision | Attribution proposée | Contrôle de la responsabilité |
| --- | --- | --- |
| Besoin documentaire et partenaires | Propriétaire dans le service demandeur | Besoin et habilitations validés, utilité revue |
| VM et OS fournis par l’infrastructure | Équipe principale si cette maintenance est explicitement acceptée ; sinon administrateur délégué identifié | Inventaire, versions/support et tickets OS |
| Docker/containerd | Équipe choisie dans la fiche, sans attribution implicite | Qui reçoit l’alerte runtime et applique le correctif ? |
| Image File Browser, dépendances et base | Mainteneur applicatif nommé par le service ou équipe ayant accepté le transfert | Version/digest, tests de migration et suivi des vulnérabilités |
| Données/configuration/sauvegardes | Répartition entre mainteneur et infrastructure, coordonnée par responsable technique | Sauvegarde cohérente et restauration testée |
| Flux, exposition et accès administratifs | Autorité approuve ; équipe réseau et mainteneurs appliquent | Publication justifiée et contrôle des flux/accessibilités |
| Fin de maintenance applicative | Propriétaire porte le remplacement ; mainteneur et sécurité analysent ; autorité arbitre moyens/risque | Plan daté, responsable et échéance ; exception explicite si nécessaire |

La distinction entre **propriétaire du service**, **responsable technique du
système** et **administrateur de chaque couche** évite de laisser la
maintenance dans l’intervalle entre deux équipes. La proposition ne suppose
pas que le service demandeur possède déjà les compétences nécessaires :
l’autorisation doit examiner sa capacité ou organiser une prise en charge.

## 4. Transfert lors d’un départ ou changement de fonction

1. Le responsable hiérarchique signale le changement au propriétaire du service.
2. Le propriétaire identifie les tâches concernées, nomme un entrant ou un suppléant et fait valider la nouvelle répartition.
3. Le responsable technique organise la transmission de l’inventaire, procédures, incidents ouverts, alertes, exceptions et échéances de support.
4. Les accès sont transférés par les dispositifs autorisés : comptes individuels, droits revus, secrets partagés renouvelés si nécessaire ; aucune clé privée personnelle n’est copiée pour simuler une continuité.
5. L’entrant confirme sa prise en charge et réalise un contrôle adapté de l’accès et de la maintenance ; les contacts et destinataires d’alertes sont actualisés.
6. Les droits du sortant sont retirés selon sa nouvelle fonction et la fiche de service est mise à jour.

**Si aucun remplaçant n’est disponible :** ne pas continuer implicitement comme
si la maintenance était assurée. Le propriétaire alerte l’autorité et la
sécurité ; une décision doit organiser une prise en charge temporaire, une
restriction, une interruption ou un retrait selon le risque. Toute exception
reste motivée, attribuée et limitée dans le temps.

Un départ inattendu suit le même principe de reprise par le suppléant et de
récupération via les moyens de l’organisation, sans dépendre d’un compte ou
d’un secret personnel inaccessible.

## 5. Fiche de désignation à compléter avant adoption

| Champ | Valeur à renseigner / vérifier |
| --- | --- |
| Service et périmètre | Nom, usage, données, partenaires et couches concernées |
| Propriétaire et suppléant | Personne/équipe, contact et validation |
| Responsable technique et suppléant | Personne/équipe, coordination et capacité de prise en charge |
| Mainteneurs par couche | OS, runtime, application, réseau, données et sauvegardes |
| Référent sécurité | Circuit d’alerte et modalités d’escalade |
| Autorité d’autorisation | Identité, délégation et limites d’arbitrage |
| Calendrier et preuves | Échéances de support, revues, tickets et emplacement des pièces |
| Continuité et retrait | Transfert, accès de secours autorisés, critères et décideur de fin de vie |

**Test de cohérence proposé :** faire cheminer une demande de publication,
une alerte OS, une alerte File Browser et un départ de mainteneur. Pour chacun,
identifier un pilote, un décideur habilité, un exécutant et une preuve. Toute
case sans porteur ou tout circuit contradictoire doit être résolu avant
validation du fragment.

## 📦 Livrable

Une répartition explicite des rôles sur tout le cycle de vie et des modalités
de transmission, utilisables pour la première version du fragment. **Nominations,
mandats et organisation réelle à valider ; aucun circuit n’est présenté comme
déjà testé ou adopté.**

- [Périmètre du fragment](definir-perimetre-fragment-pssi.md)
- [Préparation J5](../it-5/preparer-fragment-pssi.md)
- [Retour à l’itération 6](index.md)
- [Retour au module](../README.md)
