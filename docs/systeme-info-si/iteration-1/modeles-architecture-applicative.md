# Modèles d'architecture applicative

## Objectif

Identifier différents modèles d'architecture applicative dans un système d'information hospitalier, puis relier des applications réelles à ces modèles.

Dans un hôpital, toutes les applications ne fonctionnent pas forcément de la même manière. Certaines sont très centralisées, d'autres sont locales à un service, d'autres encore reposent sur plusieurs composants ou sur des services externes.

## Ressources utilisées

- [GeeksforGeeks - Centralized vs Decentralized vs Distributed Systems](https://www.geeksforgeeks.org/system-design/comparison-centralized-decentralized-and-distributed-systems/)
- [Vidéo YouTube fournie en ressource](https://www.youtube.com/watch?v=fEBl_bKG_js&t=2s)
- [Le Monde - Cyberattaque du CHU de Rouen](https://www.lemonde.fr/pixels/article/2019/11/18/frappe-par-une-cyberattaque-massive-le-chu-de-rouen-force-de-tourner-sans-ordinateurs_6019650_4408996.html)
- [LeMagIT - CHU de Rouen : autopsie d'une cyberattaque](https://www.lemagit.fr/etude/CHU-de-Rouen-autopsie-dune-cyberattaque)
- [CERT-FR / ANSSI - Rançongiciel Clop](https://www.cert.ssi.gouv.fr/uploads/CERTFR-2019-CTI-009.pdf)

## 1. Découvrir les modèles

| Modèle | Description courte | Idée principale |
| --- | --- | --- |
| Centralisée | Les traitements et les données sont concentrés sur un système principal. | Simple à gérer, mais dépend fortement d'un point central. |
| Décentralisée | Plusieurs systèmes locaux fonctionnent de manière relativement indépendante. | Plus autonome localement, mais plus difficile à coordonner. |
| Distribuée | Plusieurs composants coopèrent et échangent continuellement. | Plus disponible et scalable, mais plus complexe. |
| Cloud | Les applications ou données sont hébergées chez un fournisseur externe. | Externalise l'infrastructure, mais ajoute une dépendance fournisseur. |
| Hybride | Mélange de plusieurs modèles. | Très fréquent : une partie locale, une partie cloud ou distribuée. |

## 2. Comparer les modèles

| Modèle | Avantages | Risques / limites |
| --- | --- | --- |
| Centralisée | administration plus simple, données cohérentes, sécurité plus facile à piloter au même endroit | point unique de panne, forte dépendance au serveur central, montée en charge limitée |
| Décentralisée | autonomie des services, impact localisé en cas de panne, meilleure continuité locale | doublons de données, intégration difficile, règles de sécurité parfois hétérogènes |
| Distribuée | meilleure disponibilité, répartition de charge, redondance possible | supervision plus complexe, synchronisation des données, dépendance aux flux réseau |
| Cloud | élasticité, services accessibles à distance, maintenance déléguée | dépendance Internet/fournisseur, conformité, localisation des données, contrôle réduit |
| Hybride | compromis réaliste, conservation du sensible en interne, usage du cloud pour certains services | intégration complexe, gestion des identités, sécurité des flux entre environnements |

## 3. Exemples hospitaliers

### Architecture centralisée

Exemples :

- le dossier patient principal est hébergé sur un serveur ou une base principale du CHU ;
- toutes les unités médicales utilisent la même base de données centrale ;
- les droits utilisateurs sont gérés dans un annuaire central.

Questions :

- Avantage : les données patient sont plus cohérentes.
- Risque : si le composant central tombe, beaucoup de services peuvent être bloqués.

### Architecture décentralisée

Exemples :

- chaque service hospitalier possède son propre outil local ;
- le laboratoire conserve une base indépendante ;
- la radiologie peut continuer partiellement même si l'administration est indisponible.

Questions :

- Avantage : un service peut parfois continuer à fonctionner seul.
- Risque : les données peuvent être difficiles à synchroniser avec le reste du SI.

### Architecture distribuée

Exemples :

- plusieurs serveurs applicatifs partagent les traitements ;
- une application de rendez-vous utilise plusieurs composants ;
- des données sont répliquées entre plusieurs systèmes.

Questions :

- Avantage : une panne isolée ne bloque pas forcément tout le service.
- Risque : il faut gérer la cohérence, les flux et la supervision.

### Architecture cloud

Exemples :

- messagerie hébergée chez un fournisseur externe ;
- sauvegardes externalisées ;
- application de télémédecine accessible depuis Internet ;
- visioconférence médicale.

Questions :

- Avantage : accès plus souple, maintenance déléguée, capacité évolutive.
- Risque : dépendance au réseau, au fournisseur et aux règles de protection des données.

### Architecture hybride

Exemples :

- dossier patient gardé au CHU, messagerie externalisée ;
- serveurs locaux pour les applications critiques, cloud pour les sauvegardes ;
- outils internes et externes utilisés en même temps.

Questions :

- Avantage : modèle flexible et fréquent dans les organisations réelles.
- Risque : sécurité et intégration plus difficiles à maîtriser.

## 4. Classer des applications hospitalières

| Application / service | Modèle probable | Justification |
| --- | --- | --- |
| Dossier patient informatisé | centralisée ou hybride | souvent partagé par plusieurs services, avec données critiques centralisées |
| Admissions | centralisée | besoin d'une identité patient cohérente dans tout l'hôpital |
| Prescriptions | centralisée ou distribuée | doit communiquer avec soins, pharmacie, laboratoire et dossier patient |
| Laboratoire | décentralisée ou distribuée | peut avoir son propre logiciel, mais doit échanger les résultats avec le dossier patient |
| Imagerie médicale | décentralisée ou distribuée | système spécialisé, avec échanges vers le dossier patient et les médecins |
| Messagerie | cloud ou hybride | souvent externalisée ou connectée à Internet |
| Sauvegardes | hybride | copies locales possibles avec duplication externe ou hors site |
| RH / paie | centralisée ou cloud | données administratives, parfois hébergées dans des outils spécialisés |
| Visioconférence / télémédecine | cloud | usage fréquent de services externes accessibles par Internet |
| Active Directory / annuaire | centralisée | gestion commune des comptes et droits |

## 5. Lecture critique

| Question | Réponse synthétique |
| --- | --- |
| Quel modèle semble le plus simple ? | Le centralisé, car il y a moins de composants à coordonner. |
| Quel modèle semble le plus résilient ? | Le distribué ou l'hybride, si la redondance et le cloisonnement sont bien pensés. |
| Quel modèle pose le plus de complexité ? | Le distribué et l'hybride, car il faut gérer les flux, identités, droits et dépendances. |
| Quel modèle pose le plus de risques de point de panne ? | Le centralisé, si un composant unique porte trop de fonctions critiques. |
| Quel modèle est fréquent aujourd'hui ? | L'hybride, car les organisations mélangent souvent applications internes, cloud et services spécialisés. |

## 6. Lien avec le cas CHU de Rouen

Dans le cas du CHU de Rouen, les sources publiques indiquent plusieurs éléments utiles :

- des applications métiers ont été rendues indisponibles ;
- des postes et serveurs Windows ont été touchés ;
- Active Directory est mentionné dans le retour d'expérience LeMagIT ;
- des bases Oracle sur Linux auraient été épargnées ;
- la ToIP était isolée du réseau informatique principal ;
- les sauvegardes ont été protégées pendant la crise ;
- le CHU a fonctionné en mode dégradé avec papier et téléphone.

On peut donc formuler des hypothèses prudentes :

| Hypothèse | Modèle associé | Justification |
| --- | --- | --- |
| Le SI patient reposait probablement sur des composants centraux. | centralisée / hybride | admissions, prescriptions et dossier patient doivent partager des données communes |
| Certains services spécialisés avaient leurs propres briques. | décentralisée / distribuée | laboratoire, imagerie et pharmacie ont souvent des logiciels métiers dédiés |
| Le SI mélangeait plusieurs technologies. | hybride | présence probable de Windows, Linux, Oracle, annuaire, sauvegardes et téléphonie séparée |
| Le cloisonnement a limité certains impacts. | hybride / segmentée | la ToIP et certaines bases n'ont pas été affectées de la même manière |

## 7. Livrable attendu

Le livrable peut prendre la forme d'un tableau de classification.

| Application | Modèle | Avantage | Risque |
| --- | --- | --- | --- |
| Dossier patient | centralisée / hybride | cohérence des données patient | blocage large si composant central indisponible |
| Laboratoire | décentralisée / distribuée | autonomie métier | intégration des résultats nécessaire |
| Imagerie | décentralisée / distribuée | outil spécialisé adapté au service | dépendance aux flux vers le dossier patient |
| Messagerie | cloud / hybride | accès souple, maintenance déléguée | dépendance fournisseur et Internet |
| Sauvegardes | hybride | meilleure résilience | risque si les sauvegardes restent accessibles au rançongiciel |

## À retenir

Un SI hospitalier est rarement 100 % centralisé, décentralisé, distribué ou cloud.

Il est souvent **hybride**, avec :

- des données critiques centralisées,
- des applications métier spécialisées,
- des flux entre services,
- des accès externes,
- des sauvegardes,
- des contraintes fortes de disponibilité et de sécurité.

Le bon raisonnement consiste à identifier le modèle dominant de chaque application, puis à analyser les dépendances, les points de panne et les impacts en cas d'incident.
