# Itération 4 — J5 : Analyser un incident de cybersécurité OT

## 🎯 Objectifs de la journée

Analyser un incident de cybersécurité affectant une installation industrielle et déterminer les mesures permettant de rétablir et de sécuriser son fonctionnement.

À partir de l’installation frigorifique Montval, exploiter des traces techniques, reconstituer les événements, identifier les conséquences sur le processus industriel et proposer une réponse tenant compte des contraintes d’exploitation.

Utiliser le jumeau numérique pour reproduire certains comportements et vérifier les corrections **sans intervenir sur une installation réelle**. À l’issue de la journée, distinguer faits et hypothèses, conduire l’investigation, choisir des mesures de remédiation et démontrer le maintien des fonctions nécessaires.

## Fiches disponibles

- [5.1 — Prendre connaissance de l’incident](prendre-connaissance-incident.md) : enjeux, inventaire des sept sources, horloges, premières vérifications et questions.
- [5.2 — Analyser les traces et reconstituer les événements](analyser-traces-reconstituer-evenements.md) : 18 trames, huit captures commentées, chronologie, VPN corrigé et diagnostic provisoire ; limites FC03 et affichage Wireshark explicites.
- [5.3 — Déterminer les premières actions de réponse](determiner-premieres-actions-reponse.md) : huit actions évaluées, proposition de confinement coordonnée, continuité OT et responsabilités ; aucune action exécutée.
- [5.4 — Reproduire l’incident sur le jumeau numérique](reproduire-incident-jumeau-numerique.md) : 24 captures et PCAP de 2 630 trames : tests IT/proxy au premier essai, montée à 12,1 °C, alarme et correction au second ; séquences distinctes.
- [5.5 — Choisir et valider les mesures correctives](choisir-valider-mesures-correctives.md) : C01 appliquée, cinq captures, NFLOG trois paquets, export des deux tables et tests utiles confirmés ; continuité complète et retour arrière non attestés.
- [5.6 — Vérifier le retour à un fonctionnement maîtrisé](verifier-retour-fonctionnement-maitrise.md) : liste de contrôle, réserves labo/Montval, transmission exploitation et retour d’expérience ; aucune clôture opérationnelle supposée.
- [5.7 — Finaliser le compte-rendu d’investigation et de remédiation](finaliser-compte-rendu-investigation-remediation.md) : compte-rendu C5 unique, PDF formatrice, restitution et archive Markdown/PDF/annexes ; faits, propositions et limites distingués.
- [Pense-bête de l’itération 4](../../pense-bete/glossaire/informatique-industrielle/it-4.md).

## Ressources et état du travail

[Dossier d’incident fourni — archive](../../assets/files/informatique-industrielle/it-4/Montval-J5-Incident_dossier.zip) · [Inventaire avec empreintes SHA-256](../../assets/files/informatique-industrielle/it-4/Montval-J5-inventaire-sources.json).

Sources originales conservées dans `livrables/informatique-industrielle/it-4/Incident_dossier/`. Les événements du scénario datent du **8 octobre 2026** ; la prise en connaissance documentaire dans le mémo date du **30 octobre 2026**. Les traces sont fictives, le PCAP est synthétique et partiel ; aucune attribution humaine ni attaque confirmée n’est déduite du seul accès distant disponible. L’analyse des sources et les essais à venir restent distincts des tests J4 déjà réalisés.

[Manuel MAN-OT-01](../it-2/MAN-OT-01_Manuel_exploitation_installation_frigorifique.md) · [Dossier J4](../it-3/documenter-protections-limites.md) · [Retour au module](../README.md).
