# 3.7 — Atelier 7 | Finaliser le dossier d’analyse IT/OT

## 🎯 Objectif et modalités

Documenter les exigences opérationnelles, leurs conséquences informatiques et les choix d’architecture proposés.

**Modalité :** travail en binôme et bilan avec le formateur.

## 1 — Constituer le dossier

Produire un document unique intitulé **`J3-analyse-exigences-architecture-IT-OT`**, réunissant :

1. **Matrice OT → IT :** exigences d’exploitation, besoins informatiques et informations à confirmer.
2. **Architecture Purdue :** positionnement des composants et identification des frontières IT/OT.
3. **Architecture proposée et matrice de flux :** zones, communications nécessaires et conditions d’accès.
4. **Décisions d’intervention :** synthèse des réponses aux situations SIT-01 à SIT-04.

Distinguer les **exigences documentées**, les **hypothèses techniques** et les **propositions d’architecture**.

### Dossier préparé pour le formateur

[📄 Télécharger le dossier J3 — PDF, 12 pages](../../assets/files/informatique-industrielle/it-2/J3-analyse-exigences-architecture-IT-OT-Olivier-HIMBLOT.pdf)

Le PDF constitue le document unique : matrices, schémas, décisions et limites y sont intégrés. La source éditable est conservée dans `livrables/informatique-industrielle/it-2/J3-analyse-exigences-architecture-IT-OT.md` avec son générateur PDF.

| Partie | Contenu intégré | Pages PDF | Travaux sources |
| --- | --- | --- | --- |
| Présentation C3 | Critères, portée des informations et statut du dossier. | 1 | Consignes 3.7 et manuel. |
| Matrice OT → IT | Exigences, besoins, solutions envisageables et confirmations nécessaires. | 2–3 | [3.1](analyser-exigences-exploitation-ot.md), [3.2](traduire-exigences-ot-besoins-informatiques.md). |
| Architecture Purdue | Schéma et justification des placements, avec fonctions et actifs distingués. | 4 | [3.3](organiser-installation-modele-purdue.md). |
| Architecture et communications | Zones, cible DMZ/bastion, matrices contrôle/maintenance/services et dépendances. | 5–10 | [3.4](mettre-en-commun-exigences-consequences-it.md), [3.5](concevoir-architecture-it-ot-montval.md). |
| Décisions d’intervention | Quatre décisions courtes, conditions, inconnues et comparaisons. | 11 | [3.6](decider-intervention-contraintes-ot.md). |
| Cohérence et préparation J4 | Contrôles documentaires, informations ouvertes, recette proposée et sources. | 12 | Synthèse des travaux J3. |

Les schémas sont intégrés sur deux pages A3, pour garder les annotations lisibles ; les autres pages sont en A4 paysage. Les sources modifiables restent accessibles :

- [Schéma Purdue — draw.io](../../assets/files/informatique-industrielle/it-2/Montval-Purdue-cible.drawio) · [SVG](../../assets/files/informatique-industrielle/it-2/Montval-Purdue-cible.svg).
- [Architecture cible IT/OT — draw.io](../../assets/files/informatique-industrielle/it-2/Montval-architecture-IT-OT-J4.drawio) · [SVG](../../assets/files/informatique-industrielle/it-2/Montval-architecture-IT-OT-J4.svg).

!!! info "Statut du livrable"
    Dossier documentaire et proposition de conception préparés sur **MAN-OT-01 v1.0 du 14 octobre 2022**, scénario fictif Montval. DMZ, bastion et services OT proposés ne sont pas déclarés déployés. Les arbitrages du binôme/formateur, les adresses et capacités manquantes restent à confirmer ; aucune configuration J4, disponibilité mesurée ou décision de validation n’est attestée par la création du PDF.

## 2 — Vérifier la cohérence

| Vérification demandée | État du dossier / point d’attention |
| --- | --- |
| Choix techniques justifiés par le manuel. | Références EXP/MAI/ORG conservées ; solutions techniques explicitement proposées. |
| Contrôle local distinct de la supervision. | REG-01 à REG-03 exécutent les boucles ; SUP-01 porte supervision et historique ; OPS-01 présente les informations. |
| Communications nécessaires explicitées. | Flux C00–C03, A01–A05 et S01–S04 ; consultation, acquittement et modification distingués. |
| Informations manquantes non remplacées par des suppositions implicites. | Protocoles non documentés, topologie/IP, sauvegardes, capacités et objectifs de reprise signalés à confirmer. |
| Contraintes d’exploitation prises en compte dans les interventions. | Conditions, surveillance, coordination et reports des SIT-01 à SIT-04 indiqués ; 45 minutes REG-02 hors validation et impossibilité éventuelle de reconstituer l’historique explicites. |

Points à conserver lors de la relecture : **alarme Montval après 10 minutes**, distincte des 10 secondes du PoC ; **SUP-01 unique**, même s’il porte des fonctions N2/N3 ; **DMZ et bastion proposés**, non constatés ; autorisation d’intervention et vérification des zones, sans assimilation du retour du réseau à une reprise complète.

**Validation en séance à renseigner :** participants, date du bilan, points discutés, hypothèses acceptées, corrections demandées et appréciation du formateur. Aucun accord n’est prérempli.

## 3 — Préparer J4

La journée suivante porte sur la **mise en œuvre technique des protections réseau**. Réutiliser la matrice de flux pour configurer une séparation IT/OT, limiter les accès et vérifier que les communications nécessaires restent possibles.

Avant traduction en règles : confirmer topologie, adresses, interfaces, protocoles/ports, outils et droits réellement supportés. Préparer sauvegarde et retour arrière si réalisable, puis les essais autorisés du laboratoire. La présence d’un bastion ne dispense pas de vérifier les flux directs et la séparation lecture/écriture.

Conserver le dossier, les schémas et la matrice comme référence de conception ; ajouter en J4 les configurations et résultats réellement obtenus. Les critères de recette préparés en 3.5 restent des essais proposés tant qu’ils n’ont pas été exécutés et documentés.

## 📦 Livrable et compétence C3

**Livrable de validation : dossier d’analyse des exigences et de l’architecture IT/OT.**

**C3 — Analyser les exigences d’exploitation et les interactions IT/OT.**

Critères de validation de l’atelier :

- Identifie les dépendances techniques.
- Traduit les contraintes d’exploitation en besoins IT.
- Cartographie les composants et leurs interactions.
- Justifie les communications nécessaires et les conditions d’intervention.

**Pour le formateur :** critères « identifie les dépendances techniques ; traduit les exigences d’exploitation en besoins IT ; cartographie et justifie les communications ». **Preuve de travail : J3 — Dossier d’analyse des exigences et de l’architecture IT/OT.**

**Convention de nommage :** `[Nom]-[Prénom]-[Site]-Iteration2-Atelier7`. Nom et prénom disponibles : HIMBLOT Olivier ; site de remise à confirmer. Le PDF utilise le titre du dossier et le nom de l’auteur, sans inventer ce champ.

## Ressources

- [MAN-OT-01 — Manuel Montval](MAN-OT-01_Manuel_exploitation_installation_frigorifique.md), sections 2 à 8.
- [Sommaire J3 et fiches 3.1 à 3.6](index.md).

[Retour à l’itération 2](index.md) · [Pense-bête](../../pense-bete/glossaire/informatique-industrielle/it-2.md)
