# Définir le périmètre du fragment de PSSI

**Itération 6 — Travail individuel — 6 octobre 2026**

## 🎯 Objectif

Définir précisément les situations, systèmes et acteurs couverts par un
fragment de PSSI encadrant les services dont l’administration est assurée,
en tout ou partie, hors de l’équipe informatique principale.

**Statut : périmètre proposé pour la première version J6, à valider.** Cette
feuille ne constitue ni une PSSI complète ni une délégation déjà approuvée.
Elle reprend la [préparation J5](../it-5/preparer-fragment-pssi.md) et ses
[propositions P01–P08](../it-5/proposer-regles-adaptees-cas-fil-rouge.md).

## 1. Situation couverte et formulation du périmètre

> Le fragment s’applique lorsqu’un service souhaite déployer ou exploiter un
> système ou une application dont tout ou partie de l’administration sera
> assuré par le service demandeur, une autre équipe ou un prestataire, plutôt
> que directement par l’équipe informatique principale. Il couvre la demande,
> l’autorisation, la répartition de maintenance, l’exploitation, les changements
> et le retrait, ainsi que leurs interfaces avec le SI de l’organisation.

L’administration hors équipe principale peut concerner **une seule couche** :
le cas File Browser entre donc dans le périmètre même si l’équipe informatique
fournit et maintient la VM ou l’OS tandis que le demandeur gère l’application.
Un service interne non publié sur Internet est également concerné. Une
responsabilité distribuée ne signifie pas une absence de contrôle central.

Un service existant rejoint ce périmètre lors de son recensement : les règles
ne doivent pas viser uniquement les nouveaux déploiements. L’acceptation d’un
service existant nécessite l’identification de ses responsables et des écarts,
puis une décision et un plan de traitement.

**Titre de travail :** « Encadrement des systèmes et applications administrés
hors de l’équipe informatique principale ».

## 2. Application au cas File Browser

Dans le scénario pédagogique, un service demande en 2021 un serveur pour
partager des documents avec des partenaires. L’infrastructure fournit Ubuntu
20.04, puis le demandeur déploie File Browser. En 2026, le service reste exposé
à Internet avec une application ancienne et une maintenance mal attribuée.

Le fragment doit empêcher qu’une livraison de serveur soit interprétée comme
la prise en charge automatique de l’application, ou que le déploiement par le
métier soit interprété comme une liberté sans suivi. Les remédiations J4/J5
servent d’exemples de contrôle ; l’exposition Internet appartient au scénario
et n’a pas été démontrée pour la VM du laboratoire.

## 3. Systèmes et ressources concernés

| Élément dans le périmètre | Pourquoi le couvrir | Limite de prise en charge |
| --- | --- | --- |
| VM, serveur ou hébergement fourni au service | Support du système délégué ; ressources et maintenance à attribuer | Le fragment attribue les responsabilités, sans décrire toute l’exploitation de l’hyperviseur |
| OS et moteurs Docker/containerd | Versions, support et correctifs distincts de l’application | Identifier qui maintient chaque couche ; ne pas présumer que le demandeur administre l’OS |
| Application, image et dépendances | Source du risque de version ancienne et de fin de maintenance | Inclure base et migrations applicatives ; identifier le mainteneur et le remplacement |
| Configuration, données et sauvegardes | Documents partenaires et cohérence base/configuration lors des changements | Sensibilité, accès, besoins de reprise et conservation à définir avec le propriétaire |
| Comptes, partages et accès administratifs | Autoriser les partenaires et maîtriser les privilèges | Les partenaires utilisateurs ne deviennent pas des administrateurs ou des infogérants |
| Flux réseau et publication | Interface entre service délégué, SI et extérieur | Couvrir la décision d’exposition et les flux utiles ; pas toute la politique réseau de l’organisation |
| Inventaire, alertes, journaux et preuves | Assurer suivi et contrôlabilité dans le temps | Définir suivi et interfaces avec les dispositifs communs, sans imposer un outil unique |
| Service externalisé répondant à la situation | Une administration par un prestataire ne supprime pas la responsabilité interne | Adapter les engagements contractuels et interfaces ; ne pas attribuer automatiquement les mêmes tâches que pour une VM locale |

## 4. Acteurs concernés

| Acteur / rôle | Attente à définir dans le fragment |
| --- | --- |
| Service demandeur / propriétaire métier | Justifier le besoin, les données et partenaires ; valider les habilitations et le fonctionnement ; décider du maintien ou du retrait |
| Équipe informatique principale | Définir les ressources et interfaces qu’elle fournit, les couches qu’elle maintient et les conditions de raccordement/publication |
| Administrateur délégué / mainteneur applicatif | Accepter un périmètre explicite ; assurer maintenance, correctifs, changements et remontée des difficultés |
| Prestataire éventuel | Respecter son périmètre et ses engagements, protéger les accès et transmettre les informations nécessaires à la continuité |
| Référent sécurité | Contribuer à l’analyse du risque, au suivi des alertes, aux exigences et à l’escalade |
| Autorité habilitée | Approuver selon sa délégation les mises en service, exceptions et arbitrages de risque/moyens |
| Utilisateurs et partenaires | Respecter les conditions d’accès et signaler les anomalies ; droits limités au besoin |
| Suppléants | Assurer la continuité des tâches et décisions attribuées en cas d’absence ou de départ |

Les rôles sont proposés ; les noms, mandats et capacités réelles restent à
renseigner. Dans une petite structure, une personne peut cumuler des rôles,
mais la responsabilité de décision et l’exécution doivent rester identifiables.

## 5. Responsabilités à formaliser avant exploitation

| Sujet | Décision ou attribution indispensable | Trace / contrôle envisagé |
| --- | --- | --- |
| Propriété du service | Qui porte le besoin et le risque métier ? | Fiche de service approuvée, responsable et suppléant |
| Maintenance par couche | Qui suit OS, runtime, application, dépendances et données ? | Matrice explicite, contacts et capacité de prise en charge |
| Vulnérabilités et mises à jour | Qui reçoit, qualifie, corrige, valide et escalade ? | Circuit des alertes, tickets, échéances et tests avant/après |
| Exposition et accès | Qui autorise publication, flux et habilitations ? | Décision, inventaire des accès et revue du besoin |
| Sauvegarde et reprise | Qui sauvegarde et teste la restauration, pour quels besoins ? | Périmètre, procédure et preuve de restauration |
| Contrôles et écarts | Qui vérifie, suit les pertes et prend en charge les écarts ? | Calendrier, résultats, actions attribuées et clôture |
| Exceptions | Qui peut accepter un risque, pour quelle durée ? | Autorité identifiée, motivation, compensations et expiration |
| Remplacement et retrait | Qui décide, finance et exécute la sortie ? | Plan, données traitées, accès/publication retirés et inventaire actualisé |

Une demande d’aide ponctuelle à l’équipe principale ne transfère pas
implicitement la maintenance. Toute modification de la répartition doit être
formalisée et accompagnée d’un transfert des accès, procédures et alertes.

## 6. Étapes du cycle de vie couvertes

| Étape | Ce que le fragment devra encadrer | Lien avec les sujets J5 |
| --- | --- | --- |
| Demande / conception | Besoin, données, partenaires, durée, architecture et capacité de maintenance | S01, S03 |
| Évaluation / autorisation | Analyse du risque, support, responsabilités, exposition et conditions d’acceptation | S01–S03, S04 |
| Déploiement / réception | Configuration, secrets initiaux, sauvegarde, tests et validation avant ouverture | S02–S04 |
| Exploitation | Inventaire, veille, correctifs, journaux, habilitations et revues périodiques | S01–S04 |
| Changement / transfert | Mise à niveau, nouvelle image, changement de responsable ou de prestataire, tests et retour arrière | S01, S02, S04 |
| Écart / alerte / difficulté | Qualification, escalade, mesures compensatoires et exception ; interface avec la gestion d’incident | S02, S04 |
| Fin de support / fin de besoin | Décision de remplacement, de retrait ou d’exception limitée | S04, S05 |
| Retrait / clôture | Données et sauvegardes, comptes, clés, flux, publication, contrats et inventaire | S03, S05 |

Les fréquences et délais seront motivés et proposés dans la rédaction, puis
validés. Aucun calendrier chiffré n’est présenté ici comme déjà adopté.

## 7. Hors périmètre et interfaces à conserver

| Hors du fragment | Interface nécessaire |
| --- | --- |
| PSSI complète de l’organisation | Respecter les règles communes approuvées ; éviter les contradictions |
| Administration détaillée des services entièrement gérés par l’équipe principale | Couvrir leur interface avec le service délégué, sans réécrire leurs procédures |
| Catalogue exhaustif de commandes SSH, Docker, auditd ou de solutions de sécurité | Renvoyer aux procédures techniques et aux preuves ; conserver des exigences vérifiables |
| Organisation complète de crise, investigation et réponse aux incidents | Définir interlocuteurs et remontée vers le dispositif existant |
| Politique globale RH, juridique, physique et achats | Solliciter les acteurs compétents si un sujet conditionne l’autorisation ou le retrait |
| Tous les usages informatiques personnels ou autonomes | Ne les inclure que s’ils correspondent à un système/service exploité relevant de la situation définie |

« Hors périmètre » ne signifie pas sans obligation : les interfaces et les
règles communes applicables doivent être identifiées avant adoption. Ce
fragment ne crée pas une autorisation implicite de déployer n’importe quel
outil ou de contourner l’équipe principale.

## 8. Vérifier les frontières sur des situations concrètes

| Situation | Dans le périmètre ? | Justification |
| --- | --- | --- |
| Infrastructure maintient Ubuntu, service métier maintient File Browser | Oui | Administration partagée entre couches : cas fil rouge |
| Application interne administrée par une autre équipe | Oui | L’exposition Internet n’est pas le critère d’entrée |
| Prestataire administre l’application avec un propriétaire interne | Oui | Administration extérieure et responsabilités/interfaces à définir |
| Application et toutes ses couches administrées directement par l’équipe principale | Non pour sa gestion interne | Seules ses interfaces avec un service délégué relèvent du fragment |
| Partenaire télécharge uniquement des documents | Acteur utilisateur concerné | Droits et durée d’accès, sans responsabilité de maintenance implicite |

## 📦 Livrable préparatoire

Un périmètre proposé, avec situation d’entrée, ressources, acteurs,
responsabilités, cycle de vie, exclusions et interfaces. Il servira à rédiger
les règles du fragment J6 sans produire une PSSI complète.

**À valider avant adoption :** responsabilités nominatives, autorité
d’approbation, moyens, délais, articulation avec les règles existantes et
conditions d’acceptation des services déjà exploités.

- [Préparation J5 du fragment](../it-5/preparer-fragment-pssi.md)
- [Règles proposées P01–P08](../it-5/proposer-regles-adaptees-cas-fil-rouge.md)
- [Retour à l’itération 6](index.md)
- [Retour au module](../README.md)
