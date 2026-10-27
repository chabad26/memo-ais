# 1.1 — Atelier 1 | Découvrir l’OT et les systèmes industriels

## Objectif et modalité

**Comprendre les composants d’une installation industrielle et les contraintes particulières des systèmes OT.** Présentation et échanges avec le formateur, suivis d’un travail en binôme.

Cette fiche propose des réponses pour préparer la mise en commun. Les exemples frigorifiques sont illustratifs : ils ne décrivent pas encore le modèle fourni en formation.

## 1 — IT et OT : quelles différences ?

L’**IT — Information Technology** traite, stocke et échange des informations. L’**OT — Operational Technology** surveille ou commande des équipements qui interagissent avec le monde physique : production industrielle, distribution d’énergie, traitement de l’eau, gestion technique des bâtiments, froid et chauffage.

L’ANSSI souligne les risques possibles pour les personnes, les biens et l’environnement, ainsi que les limites d’une transposition des solutions de sécurité de l’informatique de gestion aux systèmes industriels. [Source : ANSSI, méthode de classification](https://messervices.cyber.gouv.fr/guides/la-cybersecurite-des-systemes-industriels).

| Dimension | Infrastructure IT classique | Installation OT |
| --- | --- | --- |
| Finalité | Fournir des services et traiter des données. | Surveiller et commander un procédé physique. |
| Disponibilité | Interruption à évaluer selon le métier ; certains services sont vitaux. | Interruption à évaluer selon l’état du procédé et ses conséquences physiques. |
| Temps de réponse | Dépend du service et de ses engagements. | Certaines boucles doivent respecter des échéances déterminées ; tout le réseau OT n’est pas nécessairement temps réel. |
| Sûreté de fonctionnement | Fiabilité et continuité des services. | Fonctionnement attendu, gestion des défaillances et mise en sécurité du procédé. |
| Maintenance | Tests, sauvegarde et fenêtre de changement. | Coordination avec l’exploitation, compatibilité constructeur, essais et fenêtre compatible avec le procédé. |
| Durée de vie | Renouvellement variable selon l’actif. | Équipements parfois conservés pendant des décennies, avec contraintes de support. |
| Conséquence d’une panne | Perte de service, de données ou d’activité ; effets physiques possibles selon les dépendances. | Perte de contrôle ou de visibilité, dégradation de production, dommages matériels, risques humains ou environnementaux selon l’installation. |

La sécurité des personnes et du procédé guide les arbitrages. Il faut déterminer les besoins de disponibilité, d’intégrité et de confidentialité de chaque fonction : une mesure disponible mais fausse peut être aussi problématique qu’une mesure absente. Le NIST traite précisément des exigences propres à l’OT en matière de performance, de fiabilité et de sécurité physique. [Source : NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final).

## 2 — Identifier les composants

| Composant | Rôle | Exemple frigorifique illustratif |
| --- | --- | --- |
| **Capteur** | Mesurer une grandeur physique : température, pression, position ou niveau. | Sonde de température d’une chambre froide. |
| **Actionneur** | Agir sur le processus : moteur, pompe, vanne ou compresseur. | Compresseur ou vanne commandée. |
| **PLC — Programmable Logic Controller**, automate programmable industriel | Exécuter la logique de commande à partir des entrées, de son programme et de ses paramètres. | Comparer une mesure à une consigne et commander la production de froid. |
| **HMI — Human-Machine Interface**, ou IHM | Présenter l’état de l’installation et permettre les commandes autorisées à l’opérateur. | Afficher température, consigne, alarmes et état du compresseur. |
| **SCADA — Supervisory Control and Data Acquisition** | Superviser et collecter les informations d’une ou plusieurs installations. | Centraliser les états de plusieurs chambres froides. |
| **Poste d’ingénierie** | Programmer et configurer les équipements de contrôle. | Modifier le programme de l’automate avec l’outil adapté. |
| **Poste de maintenance** | Consulter les diagnostics et réaliser les interventions autorisées. | Examiner un défaut et l’historique des interventions. |

Une IHM peut faire partie d’une solution SCADA. Les fonctions d’ingénierie et de maintenance peuvent partager un poste ; leur séparation réelle reste à vérifier.

### Lire la chaîne de fonctionnement

Dans un exemple simplifié, le capteur transmet la température au PLC ; le PLC exécute sa logique et commande un actionneur ; le procédé évolue, puis une nouvelle mesure est effectuée. L’IHM et le SCADA donnent de la visibilité et peuvent transmettre des commandes autorisées. **L’emplacement réel de la régulation est déterminant** pour analyser une panne.

Les protections, interverrouillages et fonctions de sécurité doivent être identifiés séparément : leur présence et leur indépendance ne sont pas démontrées par ce seul exemple.

## 3 — Réflexion en binôme : réponses proposées

Dans le tableau, **certain** désigne l’effet directement impliqué par l’événement, **possible** un effet qui peut survenir, et **dépend de l’architecture** les conditions à vérifier. Il ne s’agit pas de résultats de tests.

| Événement | Conséquence certaine au périmètre indiqué | Conséquences possibles | Dépend de l’architecture / informations à vérifier |
| --- | --- | --- | --- |
| **1. Perte de connexion entre la supervision et l’automate** | Le canal perdu ne permet plus ses échanges habituels. Les données affichées peuvent devenir périmées. | Perte de visibilité, d’alarmes distantes ou de commandes ; arrêt ou mode dégradé si une surveillance de liaison le prévoit. | Régulation locale dans le PLC ? Chemin redondant ? Comportement à la perte de communication ? Horodatage et indicateur de qualité des mesures ? |
| **2. Arrêt du service informatique hébergeant la supervision** | La fonction portée par le service arrêté n’est plus assurée par cette instance. | Indisponibilité de l’interface, rupture de collecte ou d’historisation ; perte de commandes centrales ; maintien du procédé en autonomie. | Supervision redondée ? IHM locale ? Dépendance de la commande au serveur ? Autonomie et mode de repli du PLC ? |
| **3. Redémarrage d’un automate pendant la production** | L’exécution normale de son programme est interrompue pendant le redémarrage. | Sorties maintenues ou changées, arrêt d’équipements, perte de variables non rémanentes, reprise incorrecte d’une séquence, transitoire de pression ou de température. | Valeurs de repli des sorties ? Variables rémanentes ? Automate redondant ? Conditions de reprise et protections indépendantes ? Un redémarrage ne signifie pas automatiquement que toutes les sorties passent à zéro. |
| **4. Capteur envoyant une valeur incorrecte** | Une mesure erronée est fournie ; son acceptation par la commande n’est pas acquise. | Mauvaise commande si la valeur est utilisée : refroidissement insuffisant ou excessif, alarme injustifiée, défaut non détecté, dégradation des produits. | Contrôle de plausibilité ? Redondance des mesures ? Diagnostic de rupture ? Seuils indépendants ? Quelle logique utilise cette mesure ? |
| **5. Mise à jour du logiciel de contrôle sans essais préalables** | La modification n’a pas été validée par des essais préalables ; cela ne prouve pas qu’elle échouera. | Incompatibilité, indisponibilité, modification des temporisations ou des échanges, régression fonctionnelle et commande inadaptée. | Logiciel concerné : PLC, IHM ou SCADA ? Validation constructeur ? Compatibilité des versions ? Sauvegarde, retour arrière, fenêtre de maintenance et essais de réception ? |

### Une perte de supervision implique-t-elle nécessairement un arrêt du processus ?

**Non.** Si le PLC assure localement la régulation avec ses capteurs et ses actionneurs, le processus peut continuer sans SCADA. L’opérateur peut toutefois perdre la visibilité, les alarmes distantes ou la possibilité de modifier certaines consignes.

Un arrêt ou un mode dégradé peut être prévu si une commande centrale, une autorisation périodique ou un mécanisme de surveillance de liaison est nécessaire. Il faut lire la logique et la documentation pour trancher. La poursuite du fonctionnement ne garantit pas, à elle seule, que les conditions de sécurité restent satisfaites.

### Proposition de réponse pour la mise en commun

> Je distingue la perte d’information, la perte de commande et l’effet sur le procédé. Pour chacun des cinq événements, je recherche où la régulation s’exécute, les dépendances, les protections et les modes de repli. Sans ces éléments, je peux décrire des conséquences possibles, mais je ne peux pas affirmer que le processus s’arrête ou reste sûr.

La mise en commun et les éventuelles corrections du binôme restent à documenter.

## Préparer la découverte du jumeau numérique

Pour expliquer le fonctionnement de l’installation et préparer sa représentation logicielle, relever les informations suivantes dans les documents et le modèle attendus.

| Information à rechercher | Utilité pour le futur modèle |
| --- | --- |
| Fonction du système, périmètre et conditions d’utilisation | Définir ce que le modèle représente. |
| Composants, connexions et emplacement de la commande | Relier procédé, capteurs, automate, actionneurs et supervision. |
| Grandeurs, unités, plages de mesure et sens d’action | Interpréter correctement les valeurs et commandes. |
| Consignes, seuils, hystérésis, temporisations et modes | Reproduire la logique de fonctionnement documentée. |
| Évolution physique : inertie thermique, charge, échanges et conditions extérieures | Décrire comment le procédé évolue avec le temps ; valeurs à obtenir, sans les inventer. |
| Alarmes, protections, interverrouillages et repli | Représenter les limites et les réactions aux anomalies. |
| Conditions initiales, pas de temps, entrées/sorties du logiciel | Comprendre l’exécution du modèle fourni. |
| Données de référence et critères de comparaison | Vérifier la fidélité du modèle et préciser ses limites. |

Aucune valeur, aucun protocole ni aucune protection propre à l’installation n’est établi à ce stade. Le terme « jumeau numérique » est celui de la consigne ; le lien éventuel du modèle avec des données actualisées du système reste à préciser.

## Résultat attendu et éléments à conserver

- Une explication de la chaîne **mesure → commande → action → évolution physique** et du rôle de la supervision.
- Le tableau des cinq situations, corrigé après les échanges, avec les hypothèses conservées explicitement.
- La liste des composants et paramètres réellement trouvés, avec les références aux documents.
- Lors des futurs essais : état initial, action, résultat attendu, résultat observé, horodatage et limites de l’observation.

Aucune manipulation n’est exécutée dans cette fiche. Les redémarrages, défauts de capteurs et mises à jour ne constituent pas des actions à réaliser sur une installation réelle dans le cadre de cet atelier de découverte.

## Ressources

- [ANSSI — La cybersécurité des systèmes industriels : méthode de classification](https://messervices.cyber.gouv.fr/guides/la-cybersecurite-des-systemes-industriels) — ressource fournie, page consultée le 26 octobre 2026.
- [NIST — SP 800-82 Rev. 3, Guide to Operational Technology Security](https://csrc.nist.gov/pubs/sp/800/82/r3/final) — complément sur les architectures et contraintes OT, page consultée le 26 octobre 2026.
- [What is OT (Operational Technology)?](https://www.youtube.com/watch?v=wjTYgASdCk4) — vidéo fournie dans la consigne ; non visionnée ici.
- [Complete Guide to the Manufacturing Automation Architecture Stack (Field, PLC, HMI, SCADA, MES, ERP)](https://www.youtube.com/watch?v=gpxvy2M-GvA) — vidéo fournie dans la consigne ; non visionnée ici.

[Retour à l’itération](index.md)
