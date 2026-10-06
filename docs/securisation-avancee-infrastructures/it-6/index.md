# Itération 6 — Élaborer le fragment de PSSI

## Travail J6 — Définir puis rédiger le fragment

Reprendre la [préparation J5](../it-5/preparer-fragment-pssi.md) et commencer
par [Définir le périmètre du fragment de PSSI](definir-perimetre-fragment-pssi.md) :
systèmes administrés hors de l’équipe principale, acteurs, responsabilités,
cycle de vie et exclusions. **Périmètre proposé le 6 octobre 2026 ; adoption
à valider.** La première version est désormais consolidée dans le document V1 ci-dessous.

Poursuivre avec [Définir les rôles et responsabilités](definir-roles-responsabilites.md) :
demande, autorisation, administration par couche, vulnérabilités, décisions,
revues, transfert et retrait ; rôles proposés et nominations à valider.

Poursuivre avec [Définir les règles du cycle de vie d’un service](definir-regles-cycle-vie-service.md) :
onze règles vérifiables, du déploiement au retrait, avec délais proposés à valider.

Compléter le fragment avec [Définir les contrôles et les exceptions](definir-controles-exceptions.md) :
matrice liée à CV01–CV11, résultats, traitement des écarts et circuit des dérogations.

[Tester le fragment de PSSI](tester-fragment-pssi.md) : appliquer les règles
aux situations A–E, identifier les informations manquantes et compléter CV07/CV11.
Test documentaire réalisé ; application réelle et adoption non démontrées.

## Document de référence conservé

[Fragment de PSSI — V1](fragment-pssi-v1.md), consolidé le 6 octobre 2026 :
objectif/périmètre, responsabilités, autorisation, CV01–CV11, contrôles,
exceptions et révision après REX. **V1 rédigée et conservée ; adoption à valider.**
Utiliser cette version pendant les journées suivantes ; créer une V2 distincte
après le retour d’expérience de l’incident.

## Préparation antérieure — Incident et REX

La préparation ci-dessous est conservée comme activité distincte du travail
PSSI J6 ; aucun incident n’est présenté comme réalisé.

## Objectif

Utiliser les dispositifs construits pendant le module pour qualifier un incident
affectant le serveur étudié, reconstruire les faits et contribuer à sa résolution.

**Statut : exercice à réaliser.** Le scénario d'incident sera fourni ou validé
par le formateur. Aucun événement, indicateur de compromission ou résultat de
confinement n'est inventé dans cette préparation.

## Préparer la prise en charge

Disposer de l'état initial, du registre des constats, des corrections réalisées,
des sources Suricata/Wazuh et des contacts métier, système, applicatif et sécurité.
Identifier qui peut décider du confinement et du retour au service.

Ouvrir la [chronologie d'incident](../dossier-preuves.md#chronologie-dincident).
Nommer un rédacteur de la chronologie et attribuer les actions techniques.

## Conduire le traitement

| Phase | Travail attendu | Éléments à conserver |
| --- | --- | --- |
| Détection | Identifier le signal initial et vérifier sa source | Alerte, heure, machine, règle et contexte |
| Qualification | Évaluer réalité, périmètre, impact et urgence | Faits confirmés, inconnues et hypothèses |
| Préservation | Conserver les traces disponibles et documenter la collecte | Copies protégées, sources, auteurs, heures et empreintes |
| Chronologie | Rapprocher les événements réseau, hôte et application | Séquence sourcée et écarts d'horloge éventuels |
| Confinement | Limiter la propagation ou l'accès selon l'impact et l'autorité désignée | Décision, périmètre, heure et vérification de l'effet |
| Remédiation | Traiter la cause, les accès compromis et les mécanismes indésirables identifiés | Changements, preuves et limites de vérification |
| Reprise | Rétablir un service jugé acceptable et renforcer l'observation | Tests fonctionnels, contrôles de sécurité et décision de reprise |
| REX | Identifier les améliorations techniques et organisationnelles | Actions, responsables, échéances et contrôles |

Ces phases peuvent se chevaucher. Un confinement urgent peut précéder certaines
collectes ; noter le motif et les éléments devenus indisponibles. Éviter une
réinstallation ou une suppression de traces avant d'avoir évalué les besoins
de conservation et les effets de l'action.

## Distinguer fait, hypothèse et décision

| Nature | Formulation attendue |
| --- | --- |
| Fait | Ce qu'une source datée montre, avec sa référence |
| Hypothèse | Une explication possible, accompagnée du contrôle permettant de la vérifier |
| Décision | Une action retenue par une personne identifiée, avec motif et résultat |
| Limite | Une source absente, une période manquante ou une conclusion non démontrée |

Une alerte réseau ne prouve pas qu'une exploitation a réussi. Un code de réponse
HTTP ne prouve pas à lui seul une compromission. Rapprocher les sources utiles
et indiquer le degré de confiance sans combler les périodes manquantes.

## Vérifier les effets des actions

- Après confinement : le flux ou l'accès visé est-il réellement interrompu ?
- Après remédiation : la cause identifiée est-elle traitée et contrôlée ?
- Après reprise : les parcours métier, les données utiles et la collecte sont-ils fonctionnels ?
- Sur la période d'observation : les indicateurs recherchés réapparaissent-ils ?

L'absence de nouvelle alerte doit être accompagnée d'une vérification de la
collecte et d'une fenêtre d'observation documentée. Elle ne prouve pas à elle
seule que toute compromission a disparu.

## Construire le retour d'expérience

| Axe | Question à traiter |
| --- | --- |
| Prévention | Quel constat d'audit ou quelle faiblesse a joué un rôle démontré ? |
| Détection | Quel signal a été utile ? Quel angle mort subsiste ? |
| Réponse | Qu'est-ce qui a facilité ou retardé la qualification et le confinement ? |
| Responsabilités | Qui devait maintenir, surveiller, décider et communiquer ? |
| Amélioration | Quelle action, quel responsable, quelle échéance et quelle preuve de clôture ? |

Mesurer les délais uniquement si les horodatages nécessaires sont disponibles
et comparables. Sinon, indiquer « non mesurable avec les traces disponibles ».

## État final attendu et preuves L6

Un compte rendu précise la qualification, le périmètre, la chronologie, les
actions, leurs effets et les limites. Le REX relie les apprentissages au plan
de correction et prépare la traduction en règles de sécurité.

Identifier clairement le caractère simulé de l'exercice. Les données de scénario
réservées à l'injecteur ne sont pas ajoutées au guide public de l'analyste.

- [Pense-bête de l'itération](../../pense-bete/glossaire/securisation-avancee-infrastructures/it-6.md)
- [Étape suivante — Évolution d'un fragment de PSSI](../it-7/index.md)
- [Retour au module](../README.md)
