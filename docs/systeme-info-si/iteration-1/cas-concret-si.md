# Cas concret SI

## Cyberattaque du CHU de Rouen, novembre 2019

Le CHU de Rouen a subi le 15 novembre 2019 une cyberattaque de type rançongiciel, publiquement associée à Clop / CryptoMix Clop.

L'incident a rendu indisponible une partie importante du système d'information : applications métiers, postes de travail, serveurs et usages critiques comme les admissions, prescriptions, analyses, radiologie, urgences et comptes rendus.

Ce cas montre qu'une cyberattaque n'est pas seulement un problème informatique : elle touche directement les activités métier d'un hôpital.

## Ressources utilisées

- [Le Monde - Cyberattaque du CHU de Rouen](https://www.lemonde.fr/pixels/article/2019/11/18/frappe-par-une-cyberattaque-massive-le-chu-de-rouen-force-de-tourner-sans-ordinateurs_6019650_4408996.html)
- [LeMagIT - CHU de Rouen : autopsie d'une cyberattaque](https://www.lemagit.fr/etude/CHU-de-Rouen-autopsie-dune-cyberattaque)
- [L'Usine Digitale - Origine criminelle de la cyberattaque](https://www.usine-digitale.fr/article/la-cyberattaque-du-chu-de-rouen-serait-bien-d-origine-criminelle.N908519)
- [CERT-FR / ANSSI - Rançongiciel Clop](https://www.cert.ssi.gouv.fr/uploads/CERTFR-2019-CTI-009.pdf)
- [ANSSI - Cartographie du système d'information](https://messervices.cyber.gouv.fr/documents-guides/20181213_anssi_guide_cartographie_v1b.pdf)
- [ANSSI - Architectures de systèmes d'information sensibles](https://messervices.cyber.gouv.fr/documents-guides/anssi-guide-recommandations_architectures_systemes_information_sensibles_ou_diffusion_restreinte-v1.2.pdf)

## 1. Partir des activités réelles

Avant de parler serveurs, applications ou réseau, il faut regarder ce que fait réellement l'hôpital.

Activités principales :

- admission et identification des patients ;
- accueil et orientation aux urgences ;
- soins médicaux et suivi patient ;
- prescriptions de médicaments et d'examens ;
- laboratoire et résultats d'analyses ;
- imagerie médicale : radio, scanner, IRM ;
- pharmacie hospitalière ;
- bloc opératoire et stérilisation ;
- dossier patient et comptes rendus ;
- communication entre services ;
- facturation, RH, logistique et maintenance biomédicale.

Même en crise, certaines missions doivent continuer : urgences, soins, prescriptions vitales, examens indispensables et coordination entre services.

## 2. Regrouper en couches fonctionnelles

| Couche fonctionnelle | Exemples d'activités |
| --- | --- |
| Administration patient | admissions, identité patient, rendez-vous |
| Urgences | accueil, orientation, priorisation |
| Soins | observations, suivi patient, traitements |
| Prescriptions / pharmacie | médicaments, examens, délivrance |
| Laboratoire | prélèvements, analyses, résultats |
| Imagerie | radios, scanners, IRM, comptes rendus |
| Dossier patient | historique, allergies, comptes rendus |
| Support | DSI, RH, logistique, maintenance biomédicale |

Cette vue permet de relier les impacts techniques aux impacts métier.

## 3. Identifier les dépendances au SI

| Couche | Applications / données nécessaires | Impact si indisponible |
| --- | --- | --- |
| Administration patient | logiciel d'admission, identité patient, dossier administratif | entrées ralenties, risque d'erreur d'identité |
| Urgences | dossier patient, orientation, prescriptions, résultats | prise en charge plus lente, coordination difficile |
| Soins | dossier patient, observations, traitements, allergies | suivi perturbé, risque d'erreur ou de retard |
| Laboratoire | demandes d'analyses, prélèvements, résultats | décisions médicales ralenties |
| Imagerie | demandes d'examens, images, comptes rendus | diagnostics retardés ou difficiles |
| Pharmacie | prescriptions, stocks, posologies, allergies | distribution des médicaments perturbée |
| Dossier patient | historique, comptes rendus, examens, traitements | perte temporaire de l'historique numérique |
| DSI / support | annuaire, supervision, sauvegardes, comptes | reprise plus difficile, visibilité réduite |

## 4. Décomposer le SI en 4 axes

| Axe | Briques probables ou confirmées | Rôle |
| --- | --- | --- |
| Réseau | réseau interne, accès Internet, flux internes, ToIP isolée, cloisonnement | relier les sites, postes, serveurs et services |
| Applicatif | admissions, DPI, prescriptions, laboratoire, imagerie, pharmacie, messagerie | soutenir les activités métier |
| Données | identité patient, données médicales, résultats, images, comptes rendus, sauvegardes | permettre le suivi et la continuité des soins |
| Utilisateurs | médecins, infirmiers, accueil, DSI, direction, prestataires | utiliser, administrer et prioriser le SI |

Hypothèses réalistes :

- présence probable d'un SI patient centralisé ;
- annuaire central de type Active Directory ;
- séparation entre certaines applications et bases de données ;
- cloisonnement réseau partiel ;
- procédures papier de secours ;
- connexions avec des partenaires externes.

Ces hypothèses sont cohérentes avec le fonctionnement d'un hôpital et avec les informations publiées sur le cas du CHU de Rouen.

## 5. Retour au cas du CHU de Rouen

| Point | Fait à retenir |
| --- | --- |
| Date | 15 novembre 2019, en début de soirée |
| Type d'attaque | rançongiciel / cryptovirus |
| Rançongiciel associé | Clop / CryptoMix Clop selon les sources publiques |
| Établissement | CHU de Rouen, réparti sur cinq sites |
| Impact technique | postes et serveurs touchés, fichiers chiffrés, applications métiers indisponibles |
| Mesure de crise | arrêt rapide des ordinateurs pour limiter la propagation |
| Mode de fonctionnement | mode dégradé, papier, téléphone, récupération physique de certains résultats |
| Données | aucune fuite de données médicales ou personnelles constatée à la date du communiqué du CHU |
| Suites | plainte contre X pour accès frauduleux et tentative d'extorsion |

## 6. Couches impactées

| Couche | Impact observé |
| --- | --- |
| Administration patient | admissions perturbées |
| Urgences | gestion plus difficile, coordination ralentie |
| Soins | observations et transmissions papier |
| Prescriptions | prescriptions perturbées ou à refaire |
| Laboratoire | résultats récupérés physiquement, service ralenti |
| Imagerie | radiologie ralentie |
| Dossier patient | accès numérique perturbé |
| Communication interne | retour au téléphone, messagerie perturbée |

## 7. Priorités de reprise

Dans une crise hospitalière, la reprise doit suivre l'importance métier.

| Priorité | À rétablir | Pourquoi |
| --- | --- | --- |
| 1 | urgences et admission minimale | identifier les patients et gérer les arrivées |
| 2 | dossier patient et soins | retrouver les informations médicales essentielles |
| 3 | prescriptions et pharmacie | éviter les erreurs de traitement |
| 4 | laboratoire et imagerie | permettre les diagnostics urgents |
| 5 | communication interne | coordonner les services |
| 6 | administration, facturation, RH | reprendre le fonctionnement global |

## Ce qui est certain / ce qui reste flou

| Certain | Flou ou non confirmé publiquement |
| --- | --- |
| Une cyberattaque a touché le CHU de Rouen le 15 novembre 2019. | Le point d'entrée exact dans le SI. |
| Des fichiers ont été chiffrés sur des ordinateurs et serveurs. | L'étendue exacte du chiffrement machine par machine. |
| Le CHU a fonctionné en mode dégradé. | La durée exacte du retour complet à la normale. |
| Les applications métiers ont été fortement perturbées. | Le niveau précis d'impact service par service. |
| Clop / CryptoMix Clop est cité publiquement. | L'identité exacte des auteurs individuels. |
| Une plainte contre X a été déposée. | Le montant de la rançon et les échanges éventuels avec les attaquants. |

## Formulation courte

Le CHU de Rouen a subi le 15 novembre 2019 une cyberattaque de type rançongiciel, publiquement associée à Clop / CryptoMix Clop. L'incident a rendu indisponible une partie importante du système d'information : applications métiers, postes de travail, serveurs, admissions, prescriptions, analyses, radiologie, urgences et comptes rendus. L'établissement a basculé en mode dégradé, avec arrêt des ordinateurs, usage du papier, téléphone et ralentissement de plusieurs services. Les sources confirment une tentative d'extorsion et une plainte contre X, mais ne permettent pas d'affirmer avec certitude le point d'entrée exact, l'étendue complète du chiffrement ou l'identité des auteurs.

## À retenir

Une cyberattaque sur un hôpital touche directement les missions métier.

Pour analyser le SI, il faut partir des activités réelles, identifier les couches fonctionnelles, repérer les dépendances numériques et prioriser la reprise selon l'impact sur les patients.
