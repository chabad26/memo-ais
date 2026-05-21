# Propositions d'amélioration

## Objectif

Proposer des améliorations réalistes pour réduire les risques du SI administratif d'une mairie.

Les propositions tiennent compte :

- du coût ;
- du contexte d'une collectivité ;
- des usages réels des agents ;
- de la simplicité de mise en place ;
- de l'impact sur la sécurité et la continuité de service.

## Amélioration 1 : mieux gérer les comptes et les droits

| Élément | Description |
| --- | --- |
| Problème identifié | Les agents n'ont pas tous les mêmes besoins, mais les droits peuvent être trop larges ou mal suivis dans le temps. Un ancien agent, un prestataire ou un compte partagé peut devenir un point d'entrée. |
| Solution proposée | Mettre en place une revue régulière des comptes et des droits : création, modification, suppression, comptes prestataires, comptes administrateurs. Ajouter si possible une authentification multi-facteurs pour les accès sensibles. |
| Justification | La gestion des accès est un levier important car elle limite ce qu'un compte compromis peut faire. C'est aussi une amélioration réaliste, car elle repose d'abord sur une procédure et un suivi. |
| Impact attendu | Moins de comptes inutiles, accès mieux limités, réduction du risque de compromission, meilleure traçabilité. |
| Alternatives écartées | Remplacer tous les outils par une solution unique d'identité serait plus propre techniquement, mais trop coûteux et trop lourd pour une première amélioration. |

## Amélioration 2 : formaliser une procédure de sauvegarde et de restauration

| Élément | Description |
| --- | --- |
| Problème identifié | Les sauvegardes peuvent exister sans être testées. En cas de panne, erreur humaine ou ransomware, la mairie peut découvrir trop tard que la restauration est impossible ou incomplète. |
| Solution proposée | Définir une procédure simple : quoi sauvegarder, à quelle fréquence, où stocker les sauvegardes, qui vérifie, qui restaure, et à quelle fréquence faire un test de restauration. Prévoir au moins une copie isolée ou difficilement modifiable. |
| Justification | La sauvegarde est critique pour la continuité de service. Une procédure claire évite de dépendre uniquement d'une personne ou d'un prestataire. |
| Impact attendu | Meilleure capacité de reprise, réduction du risque de perte de données, confiance dans les sauvegardes, temps d'interruption plus court. |
| Alternatives écartées | Acheter immédiatement une solution de reprise complète peut être trop cher. Une procédure testée et documentée est une première étape plus réaliste. |

## Amélioration 3 : former les agents aux risques concrets

| Élément | Description |
| --- | --- |
| Problème identifié | Les risques humains sont importants : phishing, pièces jointes piégées, mots de passe partagés, documents envoyés au mauvais destinataire, sessions non verrouillées. |
| Solution proposée | Organiser une formation courte et ciblée pour les agents, avec des exemples liés à la mairie : faux mail de facture, demande urgente d'un élu, pièce jointe suspecte, données personnelles d'un habitant. Ajouter un rappel simple des bons réflexes. |
| Justification | Une mairie dépend beaucoup des usages quotidiens des agents. Une formation concrète est souvent plus efficace qu'une règle technique mal comprise. |
| Impact attendu | Moins d'erreurs, meilleure détection des mails suspects, meilleure protection des données, culture sécurité plus solide. |
| Alternatives écartées | Bloquer fortement la messagerie ou interdire de nombreux usages pourrait gêner le travail quotidien. La formation permet de réduire le risque sans bloquer l'activité. |

## Amélioration 4 : segmenter progressivement le réseau

| Élément | Description |
| --- | --- |
| Problème identifié | Si tous les postes, imprimantes, serveurs et accès Wi-Fi sont sur le même réseau, un incident peut se propager plus facilement. |
| Solution proposée | Séparer progressivement les zones : postes administratifs, Wi-Fi invité, équipements d'impression, administration technique, sauvegardes. Commencer par isoler le Wi-Fi invité et les équipements les plus exposés. |
| Justification | La segmentation limite la propagation d'une attaque ou d'une panne. Elle peut être mise en place par étapes, sans tout reconstruire. |
| Impact attendu | Réduction du risque de propagation, meilleure maîtrise des flux, protection renforcée des données sensibles. |
| Alternatives écartées | Refaire toute l'architecture réseau immédiatement serait coûteux et risqué. Une segmentation progressive est plus adaptée au contexte. |

## Amélioration 5 : simplifier et documenter les outils critiques

| Élément | Description |
| --- | --- |
| Problème identifié | Les outils peuvent être nombreux, avec des usages mal documentés. En cas d'absence d'un agent ou de départ d'un prestataire, certaines opérations deviennent difficiles. |
| Solution proposée | Créer une fiche courte pour chaque outil critique : rôle, utilisateurs, données traitées, prestataire, accès, sauvegarde, procédure en cas d'incident. |
| Justification | La documentation réduit la dépendance à une seule personne et facilite le support. C'est une amélioration organisationnelle peu coûteuse. |
| Impact attendu | Meilleure continuité, support plus rapide, vision plus claire des dépendances, préparation facilitée aux incidents. |
| Alternatives écartées | Mettre en place un outil ITSM complet serait utile mais trop lourd pour démarrer. Des fiches simples suffisent pour une première version. |

## Priorités proposées

| Priorité | Amélioration | Pourquoi |
| --- | --- | --- |
| 1 | Sauvegardes et tests de restauration | indispensable pour reprendre l'activité après incident |
| 2 | Comptes, droits et MFA sur accès sensibles | réduit les effets d'un compte compromis |
| 3 | Formation ciblée des agents | agit sur les erreurs quotidiennes et le phishing |
| 4 | Documentation des outils critiques | diminue la dépendance aux personnes |
| 5 | Segmentation progressive du réseau | amélioration utile mais plus technique à planifier |

