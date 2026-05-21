# Enjeux d'un SI à partir du réel

## Objectif

Identifier les enjeux d'un système d'information et les relier à des situations concrètes.

Un enjeu de SI n'est pas seulement une notion théorique. Il se voit quand une activité est bloquée, quand une donnée fuit, quand un outil ne suit plus la charge, quand deux systèmes ne communiquent pas, ou quand une règle légale impose une contrainte.

## Les 5 enjeux à connaître

| Enjeu | Définition simple | Question à se poser |
| --- | --- | --- |
| Disponibilité | Le SI doit être accessible quand les utilisateurs en ont besoin. | Que se passe-t-il si le service tombe ? |
| Sécurité | Le SI doit protéger les données, les accès et les systèmes. | Qui peut accéder à quoi, et comment éviter l'abus ? |
| Évolutivité | Le SI doit pouvoir absorber plus d'utilisateurs, de données ou de fonctionnalités. | Le système peut-il grandir sans casser ? |
| Intégration | Le SI doit permettre aux applications de communiquer entre elles. | Les outils échangent-ils correctement les informations ? |
| Conformité | Le SI doit respecter les règles légales, métiers et contractuelles. | Sommes-nous en règle avec le RGPD, les normes ou les obligations internes ? |

## Fiche structurée

| Enjeu | Définition | Exemple réel | Impact |
| --- | --- | --- | --- |
| Disponibilité | Capacité d'un service à rester accessible et utilisable. | Cyberattaque du CHU de Rouen : applications métiers perturbées, retour au papier et au téléphone. | Soins ralentis, admissions et prescriptions dégradées, perte de temps, stress opérationnel. |
| Sécurité | Protection contre les accès non autorisés, attaques, fuites et altérations. | Phishing ou ransomware visant des postes utilisateurs puis des serveurs. | Données chiffrées, comptes compromis, arrêt de services, risque de fuite. |
| Évolutivité | Capacité à supporter une croissance de charge ou de périmètre. | Site de rendez-vous ou plateforme en ligne saturée lors d'un pic massif de connexions. | Temps de réponse élevé, erreurs, utilisateurs bloqués, image dégradée. |
| Intégration | Capacité à connecter des systèmes différents pour partager des données. | Système legacy difficile à connecter au DPI, au laboratoire ou à l'imagerie. | Ressaisies manuelles, erreurs, délais, données incohérentes. |
| Conformité | Respect des lois, normes et règles applicables. | RGPD : données personnelles et données de santé à protéger, limiter et tracer. | Sanctions, perte de confiance, obligation de correction, risque juridique. |

## Disponibilité : RTO et RPO

La disponibilité se mesure aussi avec deux notions importantes.

| Terme | Signification | Question simple | Exemple |
| --- | --- | --- | --- |
| RTO | Recovery Time Objective : durée maximale acceptable avant de rétablir un service. | Combien de temps peut-on rester sans ce service ? | Le DPI doit revenir vite car il soutient les soins. |
| RPO | Recovery Point Objective : quantité maximale de données que l'on accepte de perdre. | Jusqu'à quel moment doit-on pouvoir restaurer les données ? | Perdre 24 h de prescriptions serait beaucoup plus grave que perdre 5 min. |

### Estimation simple dans un hôpital

| Service | RTO acceptable | RPO acceptable | Justification |
| --- | --- | --- | --- |
| Urgences / admission minimale | très court : minutes à 1 h | très faible | impact immédiat sur la prise en charge |
| DPI / dossier patient | court : 1 à 4 h | très faible | nécessaire aux soins, traitements et antécédents |
| Prescriptions / pharmacie | court : 1 à 4 h | très faible | risque direct sur les traitements |
| Laboratoire / imagerie | moyen : quelques heures | faible | diagnostic ralenti si indisponible |
| Messagerie | moyen : quelques heures à 1 jour | modéré | contournement possible par téléphone |
| RH / facturation | plus long : 1 à plusieurs jours | modéré | impact important mais moins immédiat sur les soins |

Ces valeurs sont des hypothèses pédagogiques. Dans un vrai SI, elles doivent être validées avec les métiers.

## Exemples des enjeux

| Enjeu | Exemple personnel possible | Exemple projet connu | Exemple actualité / réel |
| --- | --- | --- | --- |
| Disponibilité | ENT, application bancaire ou site administratif indisponible. | Serveur de jeu ou e-commerce en panne. | Hôpital en mode dégradé après ransomware. |
| Sécurité | Compte mail piraté, mot de passe réutilisé. | Fuite de base utilisateurs. | Ransomware, phishing, fuite de données personnelles. |
| Évolutivité | Site qui rame quand trop de personnes se connectent. | Billetterie ou plateforme de réservation saturée. | Pic de charge lors d'une inscription massive ou d'un événement. |
| Intégration | Export CSV manuel entre deux outils. | Ancien logiciel métier difficile à connecter. | SI hospitalier reliant DPI, labo, imagerie, pharmacie. |
| Conformité | Formulaire demandant trop de données. | Application qui doit gérer consentement et suppression. | RGPD, données de santé, conservation limitée. |

## Questions pour défendre l'analyse

- Pourquoi cet enjeu est-il important pour l'organisation ?
- Quel service ou quelle activité est touché ?
- Quel est l'impact si l'enjeu est mal géré ?
- Peut-on estimer un RTO ou un RPO ?
- Quelles données ou quels utilisateurs sont concernés ?
- Quelle hypothèse faut-il vérifier ?

## À retenir

Les enjeux d'un SI sont liés entre eux.

Par exemple, une sauvegarde concerne :

- la **disponibilité**, car elle permet de restaurer ;
- la **sécurité**, car elle doit être protégée d'un ransomware ;
- la **conformité**, car elle contient parfois des données personnelles ;
- l'**intégration**, car elle dépend des applications et bases à sauvegarder ;
- l'**évolutivité**, car le volume de données augmente avec le temps.
