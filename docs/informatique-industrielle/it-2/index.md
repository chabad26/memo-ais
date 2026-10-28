# Itération 2 — J3 : Spécificités de l’OT

## Objectifs de la journée

Comprendre les contraintes d’exploitation d’une installation industrielle et leurs conséquences sur l’administration des infrastructures informatiques.

À partir du manuel d’exploitation de l’installation frigorifique fictive **Montval**, identifier les fonctions à préserver, les dépendances techniques, les besoins de communication et les contraintes de maintenance. Utiliser le modèle Purdue pour organiser les composants industriels et informatiques, puis proposer une architecture IT/OT adaptée.

**Matinée en autonomie**, avec les ressources fournies et l’entraide du groupe. **Après-midi avec le formateur**, pour confronter les analyses, concevoir une architecture et étudier des situations d’exploitation.

En fin de journée, pouvoir traduire des exigences d’exploitation OT en besoins techniques pour l’infrastructure IT et justifier les communications nécessaires entre les systèmes.

## Fiches disponibles

- [3.1 — Analyser les exigences d’exploitation d’une installation OT](analyser-exigences-exploitation-ot.md) : installation Montval, matrice sourcée des exigences et distinction contrôle local / supervision.
- [3.2 — Traduire les exigences OT en besoins informatiques](traduire-exigences-ot-besoins-informatiques.md) : matrice OT → IT, précautions avant/après six opérations et cinq informations à obtenir.
- [3.3 — Organiser l’installation avec le modèle Purdue](organiser-installation-modele-purdue.md) : schéma SVG/draw.io, DMZ et bastion proposés, matrice des flux et cinq réponses.
- [3.4 — Mettre en commun les exigences et leurs conséquences IT](mettre-en-commun-exigences-consequences-it.md) : support de débrief, comparaison des options et architectures ; décisions collectives à renseigner.
- [3.5 — Concevoir l’architecture IT/OT de Montval](concevoir-architecture-it-ot-montval.md) : cible DMZ/bastion, services OT proposés, matrice des droits et flux, cinq dépendances et préparation J4.
- [3.6 — Décider d’une intervention selon les contraintes OT](decider-intervention-contraintes-ot.md) : analyse SIT-01 à SIT-04, conditions d’intervention/report, contrôles et quatre décisions proposées.
- [3.7 — Finaliser le dossier d’analyse IT/OT](finaliser-dossier-analyse-it-ot.md) : fiche de clôture et PDF C3 de 12 pages, dossier unique consolidé pour le formateur.
- [Pense-bête de l’itération 2](../../pense-bete/glossaire/informatique-industrielle/it-2.md).

## Sources et état du travail

Les objectifs et consignes 3.1 à 3.7 sont intégrés. Le [manuel MAN-OT-01, version 1.0 du 14 octobre 2022](MAN-OT-01_Manuel_exploitation_installation_frigorifique.md) est fourni ; l’analyse des sections 1 à 6 renseigne les exigences EXP-01 à EXP-12, MAI-01 à MAI-08 et ORG-01–02. La matrice et les six réponses de 3.1 sont complétées ; 3.2 traduit les exigences en besoins techniques et options à confirmer, sans sélection de produit ni coût. Le schéma 3.3 ajoute une cible DMZ/bastion explicitement proposée et distingue fonctions et actifs. La fiche 3.4 prépare la confrontation des analyses, avec une trace de séance à compléter. Le dossier 3.5 prépare l’architecture et les flux de J4, sans configuration appliquée. La fiche 3.6 analyse les quatre situations de la section 7 et prépare des décisions techniques conditionnelles. La fiche 3.7 donne accès au dossier C3 consolidé en PDF (12 pages) et distingue sa constitution de la validation collective. Il s’agit d’une analyse documentaire du scénario, sans preuve de conformité de l’installation ni restitution collective attestée.

Le modèle Python des J1–J2 reste une ressource pédagogique distincte : ses ports, seuils et comportements ne sont pas automatiquement ceux de Montval.

[Retour au module](../README.md)
