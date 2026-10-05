# Proposer des règles adaptées au cas fil rouge

**Itération 5 — Travail individuel — 5 octobre 2026**

## 🎯 Objectif

Transformer les problèmes observés pendant l’audit en premières propositions
de règles de sécurité adaptées au service File Browser. Chaque règle précise
ce qui est attendu, à qui elle s’applique et comment vérifier son application.

**Statut : propositions à valider.** Ce document ne constitue pas une PSSI
complète, une politique déjà adoptée ou une preuve d’application des règles.
Les responsabilités et les échéances devront être approuvées par l’organisation.

## 1. Partir du cas et des travaux précédents

Le cas pédagogique décrit un serveur livré en 2021, une application déployée
par le service demandeur et une exposition Internet toujours présente en 2026,
avec une version ancienne et des responsabilités de maintenance mal définies.
L’exposition Internet n’a pas été démontrée pour la VM du laboratoire.

Les propositions reprennent :

- les [problèmes organisationnels](identifier-ce-que-technique-ne-regle-pas.md) : responsabilité, maintenance, exposition et cycle de vie ;
- l’[analyse de la PSSI de Poitiers](analyser-pssi-existante-poitiers.md) : principes sourcés et adaptations nécessaires ;
- le [compte-rendu de durcissement et de vérification](finaliser-compte-rendu-durcissement-verification.md) : mesures réalisées et risques résiduels.

La PSSI de référence inspire la répartition des responsabilités et les
contrôles. Les règles ci-dessous sont des **propositions locales originales** :
elles ne sont pas attribuées à l’Université de Poitiers.

## 2. Définir les rôles avant de rédiger les règles

| Rôle proposé | Responsabilité dans le cas |
| --- | --- |
| Propriétaire du service | Porte le besoin métier, les partenaires, les habilitations, la continuité et la décision de maintien ou de retrait |
| Mainteneur applicatif | Suit File Browser, l’image, les dépendances et la base ; prépare changements et tests |
| Équipe infrastructure | Maintient les couches confiées : VM, OS, Docker, réseau et stockage |
| Référent sécurité | Coordonne qualification des risques, exigences, contrôles et escalades |
| Autorité de décision | Arbitre les risques, les moyens et les exceptions selon sa délégation |

Ces fonctions doivent être associées à des personnes ou équipes nommées,
avec suppléants. Une même personne peut remplir plusieurs rôles dans un petit
service, à condition que les responsabilités et validations restent explicites.
Un administrateur ne doit pas accepter seul un risque au nom du métier sans
mandat.

## 3. Premières propositions de règles

### P01 — Attribuer la maintenance du service

| Élément | Proposition |
| --- | --- |
| Problème observé | Le serveur et l’application sont gérés par des acteurs différents sans frontière de maintenance claire |
| Objectif | Éviter qu’une couche du service reste sans suivi |
| Règle proposée | Avant toute mise en service ou poursuite d’exploitation de File Browser, le propriétaire doit faire valider une fiche désignant un responsable et un suppléant pour OS, runtime, image/application, données et exposition. Tout changement d’équipe doit inclure la transmission des accès, procédures et alertes |
| Rôle responsable | Propriétaire du service pour la fiche ; infrastructure et mainteneur applicatif pour leurs périmètres |
| Contrôle permettant de vérifier son application | Fiche approuvée et contacts vérifiés ; suivre une alerte OS puis applicative jusqu’à leur prise en charge ; relever tout périmètre sans responsable |

### P02 — Qualifier et suivre les vulnérabilités

| Élément | Proposition |
| --- | --- |
| Problème observé | Alertes nombreuses, parfois contradictoires, sans traitement durablement attribué |
| Objectif | Transformer une alerte en décision traçable et adaptée au risque |
| Règle proposée | Le référent sécurité doit organiser la réception des avis et résultats de scans. Toute alerte retenue doit être reliée à un composant/version/chemin, qualifiée selon exposition et impact, puis affectée à un responsable avec priorité et échéance. Toute exclusion doit être justifiée et réexaminée si le composant ou le contexte change |
| Rôle responsable | Référent sécurité pour le suivi ; mainteneur ou infrastructure pour l’analyse technique et la correction |
| Contrôle permettant de vérifier son application | Échantillon d’alertes : preuve d’applicabilité ou d’exclusion, responsable, échéance, décision et preuve de clôture ; revue des tickets sans prise en charge ou en retard |

Une faible QoD ne suffit pas à exclure une alerte. Une version amont ancienne
ne suffit pas à confirmer une vulnérabilité si un correctif a été rétroporté.

### P03 — Organiser les mises à jour et les migrations

| Élément | Proposition |
| --- | --- |
| Problème observé | OS et application anciens ; mises à jour susceptibles d’interrompre le partage documentaire |
| Objectif | Maintenir le service sans reporter indéfiniment les corrections |
| Règle proposée | Les mainteneurs doivent conserver l’inventaire des versions et échéances de support, préparer les correctifs selon la priorité définie, et planifier les migrations avant fin de support. Chaque changement doit prévoir sauvegarde cohérente, test adapté, retour arrière, fenêtre et validation fonctionnelle. Tout report doit donner lieu à une exception explicite |
| Rôle responsable | Infrastructure pour ses couches ; mainteneur applicatif pour image/application ; propriétaire pour fenêtre et validation métier |
| Contrôle permettant de vérifier son application | Inventaire comparé aux versions réelles ; tickets avec versions/digest avant-après, essais, sauvegarde et résultat ; liste des fins de support sans plan et des reports non approuvés |

### P04 — Autoriser et revoir l’exposition externe

| Élément | Proposition |
| --- | --- |
| Problème observé | Dans le scénario, le partage reste exposé à Internet plusieurs années après sa création |
| Objectif | Maintenir uniquement une exposition justifiée et maîtrisée |
| Règle proposée | Toute publication externe de File Browser doit être autorisée sur la base du besoin partenaire et d’une analyse des données et flux. La fiche doit préciser services/ports, accès d’administration, protections, responsable et échéance de revue. Les flux sans justification doivent être retirés après analyse d’impact |
| Rôle responsable | Propriétaire justifie le besoin ; référent sécurité examine le risque ; infrastructure applique les flux autorisés |
| Contrôle permettant de vérifier son application | Comparer exposition effective et flux approuvés ; test externe autorisé ; revue du besoin, de l’échéance et des accès d’administration |

L’ouverture du partage documentaire ne vaut pas autorisation d’exposer tous
les services du serveur. Les modalités précises sont à choisir selon les
partenaires et la sensibilité, sans imposer ici un moyen unique.

### P05 — Contrôler périodiquement et après changement

| Élément | Proposition |
| --- | --- |
| Problème observé | Les mesures appliquées peuvent disparaître lors d’un reboot, d’une recréation ou d’une nouvelle image |
| Objectif | Vérifier que les protections et le fonctionnement restent effectifs |
| Règle proposée | Les exploitants doivent réaliser les contrôles définis à la mise en service, après tout changement affectant les protections, puis selon un calendrier validé en fonction du risque. Le contrôle doit associer état effectif, effet attendu et fonctionnement, conserver les preuves et ouvrir une action pour chaque écart |
| Rôle responsable | Infrastructure et mainteneur réalisent ; référent sécurité définit les points de sécurité ; propriétaire valide les parcours métier |
| Contrôle permettant de vérifier son application | Calendrier et rapports datés ; vérifier cible, profils, filtres et digest ; échantillon de tests SSH, privilèges Docker, audit, écoute réseau et opérations applicatives ; suivi des écarts |

Un scan complet n’est pas obligatoire à chaque changement. Choisir le contrôle
pertinent ; une image identique peut néanmoins recevoir de nouvelles alertes
si la base du scanner évolue. Justifier les contrôles non relancés.

### P06 — Encadrer les exceptions et risques résiduels

| Élément | Proposition |
| --- | --- |
| Problème observé | Des alertes et des actions différées pourraient devenir des risques acceptés implicitement |
| Objectif | Éviter les dérogations permanentes et sans décideur |
| Règle proposée | Toute dérogation doit préciser règle concernée, périmètre, motif, risque, mesures compensatoires, responsable de suivi, autorité approbatrice et date d’expiration. À l’échéance, corriger, renouveler avec justification ou retirer le service. Une exception échue ou aggravée doit être escaladée |
| Rôle responsable | Propriétaire demande ; référent sécurité analyse ; autorité habilitée décide ; mainteneur suit l’exécution |
| Contrôle permettant de vérifier son application | Registre des exceptions, approbations et échéances ; contrôle des compensations et des actions de sortie ; repérage des exceptions expirées |

Les dix HIGH Trivy et la fin de maintenance de File Browser ne sont pas
formellement acceptés par la simple rédaction du compte-rendu de laboratoire.

### P07 — Prévoir remplacement et retrait

| Élément | Proposition |
| --- | --- |
| Problème observé | Un service utile en 2021 peut rester en ligne sans support ou sans besoin confirmé en 2026 |
| Objectif | Prévenir la persistance d’un service abandonné et protéger ses données |
| Règle proposée | Le propriétaire doit revoir l’utilité et la maintenance du service aux échéances prévues. La fin de maintenance, l’absence de mainteneur ou la disparition du besoin doit déclencher une décision de remplacement, de retrait ou d’exception. Le retrait doit traiter données, accès, publication, inventaire et conservation justifiée des sauvegardes |
| Rôle responsable | Propriétaire décide du besoin ; mainteneur et infrastructure préparent la transition ; autorité alloue les moyens et arbitre |
| Contrôle permettant de vérifier son application | Décision datée, plan avec responsable et échéance ; pour un retrait, test d’inaccessibilité, révocation des accès et inventaire mis à jour ; pour un remplacement, tests de migration et restitution des données |

### P08 — Gérer les accès au partage documentaire

| Élément | Proposition |
| --- | --- |
| Problème observé | Identifiants par défaut constatés et accès partenaires susceptibles de survivre au besoin |
| Objectif | Limiter l’accès aux personnes autorisées pendant la durée nécessaire |
| Règle proposée | Le propriétaire doit valider les habilitations et leur durée. Le mainteneur doit supprimer les secrets initiaux avant ouverture, privilégier des accès attribuables, appliquer les droits utiles et retirer les accès en fin de besoin. Les comptes partagés et les limites de révocation des sessions doivent être identifiés et justifiés |
| Rôle responsable | Propriétaire valide ; mainteneur applique et contrôle ; partenaires respectent les conditions d’accès |
| Contrôle permettant de vérifier son application | Revue comptes/partages/échéances ; refus de l’ancien identifiant et d’un accès expiré ; test des droits et des sessions selon la fonction ; secrets absents des captures et documents |

## 4. Rendre les règles applicables avant adoption

| Décision à prendre | Pourquoi elle reste nécessaire |
| --- | --- |
| Nommer les responsables et suppléants | Les rôles proposés ne sont pas encore des affectations réelles |
| Définir criticité et sensibilité des données | Elles déterminent contrôles, protections et priorité |
| Fixer délais, fréquence des revues et escalade | Aucun délai chiffré n’est présenté comme une exigence déjà en vigueur |
| Identifier l’autorité habilitée aux exceptions | Une acceptation de risque nécessite un mandat clair |
| Choisir l’emplacement des inventaires et preuves | Une règle doit pouvoir être contrôlée sans dépendre d’une personne ou d’un historique de terminal |
| Vérifier moyens, interruption et remplacement | La maintenance et la sortie nécessitent temps, compétences et ressources |

Avant validation, lire chaque règle avec les équipes concernées : le
destinataire et l’action sont-ils identifiables ? Le contrôle peut-il révéler
un écart ? Une responsabilité ou une échéance reste-t-elle sans porteur ?
Les délais seront proposés selon le risque, puis approuvés, plutôt qu’inventés
comme des obligations universelles.

## 📦 Résultat attendu

Huit premières propositions adaptées au cas, avec problème, objectif, règle,
responsable et contrôle. Elles constituent une base de discussion pour une
politique et des procédures locales ; **elles ne prouvent pas leur adoption
ou leur application** et ne cherchent pas à couvrir toute une PSSI.

Les priorités organisationnelles sont de nommer la maintenance, traiter la
fin de maintenance applicative et attribuer le suivi des alertes ouvertes.
Les contrôles techniques J4/J5 fournissent des exemples de preuves utiles,
mais la pérennité dépend de ces décisions et de leur suivi.

- [Problèmes organisationnels](identifier-ce-que-technique-ne-regle-pas.md)
- [Analyse de la PSSI de référence](analyser-pssi-existante-poitiers.md)
- [Compte-rendu de durcissement et de vérification](finaliser-compte-rendu-durcissement-verification.md)
- [Retour à l’itération 5](index.md)
- [Retour au module](../README.md)
