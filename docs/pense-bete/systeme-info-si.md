# Pense-bête Système d'info & archi SI

## Système d'information

Un **système d'information** regroupe les personnes, les outils, les données, les procédures et les infrastructures qui permettent à une organisation de fonctionner.

Dans un hôpital, le SI soutient :

- les admissions,
- les soins,
- les prescriptions,
- le dossier patient,
- le laboratoire,
- l'imagerie,
- la pharmacie,
- les urgences,
- la facturation,
- la RH,
- la maintenance biomédicale.

## Architecture SI

L'**architecture SI** décrit comment les composants sont organisés :

- utilisateurs,
- applications,
- données,
- réseau,
- serveurs,
- sécurité,
- flux,
- dépendances.

Une bonne architecture facilite :

- l'administration,
- la supervision,
- l'évolution,
- la sécurité,
- la reprise après incident.

## Méthode de cartographie

Pour analyser un SI, on peut avancer dans cet ordre :

1. Partir des activités réelles de l'organisation.
2. Regrouper les activités en couches fonctionnelles.
3. Identifier les dépendances au SI.
4. Décomposer en 4 axes : réseau, applicatif, données, utilisateurs.
5. Dessiner une première vue globale.
6. Produire un diagramme réseau.
7. Repérer les zones critiques et les zones floues.

## Couches fonctionnelles d'un hôpital

| Couche | Exemples |
| --- | --- |
| Administration patient | admissions, identité patient, rendez-vous |
| Urgences | accueil, orientation, priorisation |
| Soins | observations, suivi patient, traitements |
| Prescriptions | médicaments, examens, actes |
| Laboratoire | analyses, prélèvements, résultats |
| Imagerie | radio, scanner, IRM, comptes rendus |
| Pharmacie | stocks, délivrance, validation |
| Dossier patient | historique, allergies, comptes rendus |
| Support technique | DSI, supervision, maintenance, sauvegardes |

## Les 4 axes d'analyse

| Axe | Ce qu'on cherche |
| --- | --- |
| Réseau | zones, flux, Internet, VPN, segmentation, cloisonnement |
| Applicatif | applications métiers, DPI, prescriptions, laboratoire, imagerie |
| Données | identité patient, résultats, images, comptes rendus, sauvegardes |
| Utilisateurs | soignants, accueil, DSI, direction, prestataires |

## Diagrammes à produire

| Diagramme | Utilité |
| --- | --- |
| Vue globale du SI | Comprendre les grandes zones et les interactions principales. |
| Diagramme réseau | Voir les zones réseau, les flux, les points d'entrée et les chemins d'attaque. |
| Schéma de crise | Montrer ce qui tombe, ce qui continue et ce qui doit être repris en priorité. |

## Questions importantes

Pour lire un SI côté défense ou côté attaquant :

- Par où un attaquant peut-il entrer ?
- Quels accès distants existent ?
- Où sont les applications critiques ?
- Où sont les données sensibles ?
- Comment les utilisateurs s'authentifient ?
- Quels flux sont indispensables ?
- Quelles zones sont cloisonnées ?
- Quelles sauvegardes sont protégées ?
- Que peut-on couper en cas de crise ?

## Cas CHU de Rouen

Le CHU de Rouen a subi le 15 novembre 2019 une cyberattaque de type rançongiciel.

Points importants à retenir :

- attaque associée publiquement à Clop / CryptoMix Clop,
- chiffrement de fichiers sur des ordinateurs et serveurs,
- applications métiers fortement perturbées,
- admissions, prescriptions, analyses, imagerie, urgences et comptes rendus touchés,
- arrêt rapide des ordinateurs pour éviter la propagation,
- fonctionnement en mode dégradé,
- retour au papier et au téléphone,
- plainte contre X pour accès frauduleux et tentative d'extorsion.

## Priorités de reprise en hôpital

| Priorité | À rétablir |
| --- | --- |
| 1 | Urgences et admission minimale |
| 2 | Dossier patient et soins |
| 3 | Prescriptions et pharmacie |
| 4 | Laboratoire et imagerie |
| 5 | Communication interne |
| 6 | Administration, facturation, RH |

## Points d'entrée possibles

| Point d'entrée | Exemple |
| --- | --- |
| Messagerie | phishing, pièce jointe, lien malveillant |
| Accès distant | VPN, prestataire, télémaintenance |
| Service exposé | portail web, messagerie, application publiée |
| Poste utilisateur | infection initiale puis déplacement interne |

## Déplacement d'un attaquant

Un scénario possible :

1. Compromission d'un poste utilisateur.
2. Récupération d'identifiants.
3. Rebond vers l'annuaire ou l'administration.
4. Propagation vers les serveurs applicatifs.
5. Chiffrement des fichiers sur postes et serveurs.
6. Tentative d'atteinte des sauvegardes.

## Segmentation et cloisonnement

À retenir :

- séparer les postes utilisateurs et les serveurs,
- isoler les sauvegardes,
- protéger les comptes administrateurs,
- cloisonner les équipements biomédicaux,
- garder la téléphonie aussi indépendante que possible,
- limiter les flux entre zones,
- journaliser les accès importants.

## À retenir

Une cartographie SI ne cherche pas la perfection au début.

Elle sert d'abord à comprendre :

- les activités métier,
- les dépendances numériques,
- les zones critiques,
- les flux,
- les priorités de reprise.
