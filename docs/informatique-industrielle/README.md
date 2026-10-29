# Informatique industrielle

**Cybersécurité — Administrateur d’Infrastructures Sécurisées — 2026 · Grenoble**

Dernier module spécialisé du parcours, sur **cinq jours**, consacré à la cybersécurité des environnements **OT — Operational Technology**.

## Itération 1 — Découvrir une installation industrielle automatisée

- [Objectifs de la journée et sommaire](it-1/index.md).
- [1.1 — Découvrir l’OT et les systèmes industriels](it-1/decouvrir-ot-systemes-industriels.md) : composants, différences IT/OT et réponses proposées aux cinq situations.
- [1.2 — Étudier une installation frigorifique](it-1/etudier-installation-frigorifique.md) : scénario de grande surface, schéma fonctionnel et régulation à hystérésis.
- [1.3 — Prendre en main le modèle frigorifique](it-1/prendre-en-main-modele-frigorifique.md) : Python/Modbus, supervision, consigne et porte ; 12 tests locaux réussis.
- [1.4 — Observer des dysfonctionnements et leurs conséquences](it-1/observer-dysfonctionnements-consequences.md) : défaut capteur, deux captures de l’arrêt/reprise, diagnostic et analyse A–E.
- [1.5 — Étudier et modifier la logique de contrôle](it-1/etudier-modifier-logique-controle.md) : hystérésis, copie de travail, sept captures commentées, comparaison calculée et procédure de restauration.
- [1.6 — Préparer la construction du jumeau numérique](it-1/preparer-jumeau-numerique.md) : schéma numérique, fonctions, registres et limites de validation. Complément : schéma isométrique de la cible sécurisée proposée par l’apprenant.
- [1.7 — Découvrir OpenPLC — optionnel](it-1/decouvrir-openplc.md) : Editor ouvert, neuf captures, projet Structured Text et débogueur ; intégration au modèle à concevoir.
- [1.8 — Découvrir FUXA — optionnel](it-1/decouvrir-fuxa.md) : conteneur et accès web local attestés, écran statique réalisé ; trois captures commentées.
- [Pense-bête de l’itération](../pense-bete/glossaire/informatique-industrielle/it-1.md).

La journée porte sur une installation frigorifique fictive de grande surface. Le scénario fonctionnel et le laboratoire Python/Modbus sont intégrés ; code et registres examinés, tests locaux réussis. Dix captures du TP sont intégrées et commentées dans la fiche 1.3.

### Journée 2 — Dans la même itération 1

- [Objectifs, organisation et fiches du J2](it-1/index.md#journee-2-communications-et-validation-du-jumeau-numerique).
- [2.1 — Découvrir les communications Modbus TCP](it-1/decouvrir-communications-modbus-tcp.md) : 1 h en autonomie, quatre tables, six fonctions et sécurité du protocole.

- [2.2 — Analyser les échanges Modbus dans Wireshark](it-1/analyser-echanges-modbus-wireshark.md) : capture, décodage du port 15020, MBAP ; dix captures et écritures 34/36 et 74/76 confirmées.

- [2.3 — Cartographier les variables et tester les opérations Modbus](it-1/cartographier-variables-tester-modbus.md) : sept variables, huit captures : lectures, porte en FC05 et exception 02 obtenue par le script Python.

- [2.4 — Mettre en commun les observations sur Modbus](it-1/mettre-en-commun-observations-modbus.md) : synthèse des preuves, temporalités et comparaison au réel.

- [2.5 — Assembler les composants du jumeau numérique](it-1/assembler-composants-jumeau-numerique.md) : serveur, supervision HTTP et passerelle ; 15 captures et analyse du PCAP confirment les deux chemins.

- [2.6 — Valider les comportements du jumeau numérique](it-1/valider-comportements-jumeau-numerique.md) : six scénarios, six captures commentées, critères et limites de transposition au réel.
- [2.7 — Finaliser le dossier de validation du jumeau numérique](it-1/J2-validation-jumeau-numerique.md) : dossier C2 unique et PDF formateur de 7 pages.

## Itération 2 — J3 : Spécificités de l’OT

- [Objectifs de la journée et sommaire](it-2/index.md).
- [3.1 — Analyser les exigences d’exploitation d’une installation OT](it-2/analyser-exigences-exploitation-ot.md) : Montval, manuel intégré, matrice sourcée EXP/MAI/ORG et six réponses ; limites documentaires identifiées.
- [3.2 — Traduire les exigences OT en besoins informatiques](it-2/traduire-exigences-ot-besoins-informatiques.md) : matrice OT → IT, six interventions et cinq demandes documentaires.
- [3.3 — Organiser Montval avec le modèle Purdue](it-2/organiser-installation-modele-purdue.md) : schéma modifiable, flux, DMZ et bastion proposés ; distinction entre cible et état documenté.
- [3.4 — Mettre en commun les exigences et leurs conséquences IT](it-2/mettre-en-commun-exigences-consequences-it.md) : synthèse documentaire pour le débrief, solutions à confronter et trace des arbitrages à compléter.
- [3.5 — Concevoir l’architecture IT/OT de Montval](it-2/concevoir-architecture-it-ot-montval.md) : schéma SVG/draw.io, zones, flux lecture/modification et dépendances ; référence proposée pour J4.
- [3.6 — Décider d’une intervention selon les contraintes OT](it-2/decider-intervention-contraintes-ot.md) : quatre situations Montval, vérifications, coordination, reports et décisions courtes proposées.
- [3.7 — Finaliser le dossier d’analyse IT/OT](it-2/finaliser-dossier-analyse-it-ot.md) : fiche Markdown et dossier PDF C3 consolidé de 12 pages pour le formateur.
- [Pense-bête de l’itération 2](../pense-bete/glossaire/informatique-industrielle/it-2.md).

## Itération 3 — J4 : Protections réseau

- [Objectifs de J4 et sommaire](it-3/index.md).
- [4.1 — Intégrer les services informatiques du magasin](it-3/integrer-services-informatiques-magasin.md) : STOCK, ORDER, fournisseurs, IT-ADMIN et BACKUP ; données, initiateurs et architecture étendue proposée.
- [4.2 — Définir les accès et les règles de pare-feu](it-3/definir-acces-regles-pare-feu.md) : matrice et liste ordonnée CSV, hypothèses explicites, maintenance temporaire et refus par défaut.
- [4.3 — Protéger un régulateur industriel obsolète](it-3/proteger-regulateur-industriel-obsolete.md) : REG-02 en fin de support, protection compensatoire via GW proposée, limites et politique consolidée.
- [4.4 — Préparer les essais de segmentation](it-3/preparer-essais-segmentation.md) : briefing, composants Python/Modbus, topologie à confirmer et plan d’essais CSV.
- [4.5 — Mettre en œuvre le filtrage IT/OT](it-3/mettre-en-oeuvre-filtrage-it-ot.md) : TP appliqué sur Debian 192.168.122.105 ; 8 contrôles conformes, douze captures, scripts et exports nft réels ; refus par défaut confirmé et PCAP de 39 trames.
- [4.6 — Tester les protections et le fonctionnement](it-3/tester-protections-fonctionnement.md) : sept captures, tests conformes, régulation locale observée pendant coupure et reprise des lectures/API attestée.
- [4.7 — Documenter les protections et leurs limites](it-3/documenter-protections-limites.md) : dossier C4 unique et PDF formateur ; architecture et 32 règles proposées, configuration appliquée, preuves et limites.
- [Pense-bête de l’itération 3](../pense-bete/glossaire/informatique-industrielle/it-3.md).

## Livrable formateur

**Version V3 — présentation verticale par niveaux Purdue, selon l’exemple du formateur :** [dossier PDF, 3 pages](../assets/files/informatique-industrielle/it-1/Schema-architecture-OT-J1-Olivier-HIMBLOT-V3.pdf) · [schéma A3 portrait](../assets/files/informatique-industrielle/it-1/Schema-architecture-OT-J1-Olivier-HIMBLOT-Purdue.pdf) · [source draw.io](../assets/files/informatique-industrielle/it-1/Schema-architecture-OT-J1-Olivier-HIMBLOT-Purdue.drawio).

Les fonctions du laboratoire sont placées aux niveaux 0–2 ; les niveaux supérieurs et la DMZ restent des repères non documentés. Il ne s’agit pas d’une segmentation mise en œuvre. Repérage fonctionnel : [Cisco — Industrial Security 3.1, chapitre 2](https://www.cisco.com/c/dam/en/us/td/docs/Technology/Industrial-Security-3-1-DG.pdf).


**Version V2 — présentation de type Visio :** [dossier PDF, 3 pages](../assets/files/informatique-industrielle/it-1/Schema-architecture-OT-J1-Olivier-HIMBLOT-V2.pdf) · [schéma A3 seul](../assets/files/informatique-industrielle/it-1/Schema-architecture-OT-J1-Olivier-HIMBLOT-Visio.pdf) · [source modifiable draw.io](../assets/files/informatique-industrielle/it-1/Schema-architecture-OT-J1-Olivier-HIMBLOT-Visio.drawio).

Pictogrammes d’équipements, zones fonctionnelles et connecteurs orthogonaux ; le laboratoire initial reste la référence représentée.


[📄 J1 — Schéma d’architecture OT annoté — Olivier HIMBLOT (PDF)](../assets/files/informatique-industrielle/it-1/Schema-architecture-OT-J1-Olivier-HIMBLOT.pdf)

## 🎯 Objectifs

### Objectif global

Découvrir les architectures industrielles, comprendre leurs contraintes et acquérir la culture OT nécessaire pour intervenir avec précaution, dialoguer avec les automaticiens et les ingénieurs procédés, puis proposer des mesures de sécurité adaptées.

Le module aborde les architectures SCADA, les automates PLC, les unités RTU et les protocoles Modbus, OPC UA et DNP3. Il met en perspective les différences avec l’IT : contraintes temporelles, continuité du procédé, équipements conservés pendant des décennies et conséquences physiques possibles d’une défaillance. La sécurité des personnes et du procédé guide les décisions ; les exigences de disponibilité, d’intégrité et de confidentialité s’apprécient selon l’installation.

Le cas fil rouge est **IndustriAlp, une usine chimique**, pour laquelle vous intervenez comme consultant en cybersécurité industrielle. La progression conduit à une **note de recommandations actionnable pour la direction**, articulant coûts, impacts opérationnels et risques humains. Cette note constitue la pièce phare du module pour le dossier projet RNCP.

### Vous apprendrez à

- **Comprendre une architecture OT** : SCADA, PLC, RTU, capteurs, actionneurs, IHM, historian et modèle Purdue.
- **Comparer les contraintes IT et OT** : temps réel, disponibilité, cycles de vie longs, maintenance et conséquences physiques.
- **Analyser les vulnérabilités spécifiques** : communications non protégées, automates accessibles sans authentification, comptes par défaut, équipements non mis à jour et accès distants non maîtrisés.
- **Concevoir et configurer une segmentation IT/OT** : DMZ industrielle, filtrage des flux, protection des communications selon les capacités des équipements et accès distants contrôlés.
- **Préparer la détection et la réponse aux incidents OT** : observation du trafic industriel, qualification des alertes et coordination avec les équipes du procédé.
- **Mobiliser les principes de la série IEC 62443** pour la segmentation, les accès et la maintenance adaptée aux contraintes industrielles.
- **Analyser des incidents industriels réels**, notamment Colonial Pipeline et Triton/TRISIS, en articulant facteurs techniques, organisationnels et humains.
- **Formuler des recommandations pour une direction** : priorités, coûts estimés, impacts sur la production, risques humains et conditions de mise en œuvre.

## 🎓 En fin de module

Vous serez capables de lire une architecture industrielle, d’identifier les actifs critiques, d’analyser les vulnérabilités d’un environnement OT simulé, de concevoir une segmentation sécurisée et de construire un playbook adapté aux contraintes du procédé.

Vous pourrez défendre des recommandations compréhensibles par une direction non technique et expliquer leurs implications opérationnelles, humaines et financières dans votre dossier de certification.

## 🔄 Démarche pédagogique

**Comprendre → analyser → sécuriser → détecter → recommander.** Les cinq phases ci-dessous reprennent le programme fourni ; les activités et itérations seront ajoutées à réception de leurs consignes.

### 1. Comprendre l’architecture OT

Identifier les rôles du SCADA (*Supervisory Control and Data Acquisition*), des PLC (*Programmable Logic Controller*), des RTU (*Remote Terminal Unit*), des capteurs et actionneurs, des IHM (*Interfaces Homme-Machine*) et de l’historian, chargé de l’historisation des données du procédé.

Étudier les usages et les options de protection de Modbus, OPC UA et DNP3, puis situer les équipements dans le modèle Purdue. Relier chaque choix d’architecture aux contraintes du procédé et aux différences IT/OT.

### 2. Analyser les vulnérabilités OT

À partir de l’environnement simulé IndustriAlp, cartographier les actifs critiques : automates, supervision, postes opérateurs et liaisons vers l’ERP.

Rechercher les situations prévues par le programme : Modbus en clair, automates accessibles sans authentification, comptes constructeur par défaut, absence de mises à jour et accès distants d’intégrateurs non maîtrisés. Le rapport attendu documente **au moins cinq vulnérabilités critiques**, leur exploitabilité et les recommandations associées. La qualification devra être justifiée par les observations et les conséquences sur le procédé ; cette liste de recherche ne constitue pas un constat d’audit.

### 3. Sécuriser un réseau OT

Concevoir une segmentation IT/OT avec une DMZ industrielle, en s’appuyant sur le modèle Purdue et les principes de la série IEC 62443. Définir les flux autorisés et les règles du pare-feu adapté à l’environnement industriel.

Étudier la protection des communications selon les capacités des équipements : prise en charge de Modbus sécurisé par TLS, ou tunnel sécurisé lorsque cette solution est adaptée et validée. Prévoir des accès distants d’intégrateurs contrôlés, via un serveur de rebond (*jump server*) et une traçabilité des sessions.

Produire le schéma cible et conserver les configurations commentées ainsi que les preuves des tests réalisés.

### 4. Détecter et répondre aux incidents OT

Découvrir les approches de détection dédiées à l’OT ; Nozomi Networks, Claroty et Dragos sont cités dans le programme. Étudier l’observation passive du trafic et les alertes sur les écarts de comportement. Leur évocation ne suppose ni leur installation ni leur utilisation dans le laboratoire.

Construire un playbook pour une **modification non autorisée de commandes PLC**. Prévoir la coordination entre exploitation, automaticiens et sécurité, la collecte des preuves et les décisions de confinement. Toute action affectant le procédé doit tenir compte de sa mise en sécurité ; l’arrêt ou l’isolement d’un équipement ne se décide pas sur un réflexe IT.

Tester le playbook dans le scénario prévu, puis consigner les écarts et améliorations dans un compte rendu.

### 5. Recommander à la direction

L’atelier de clôture prévoit l’étude de Triton/TRISIS, en complément du cas Colonial Pipeline. En extraire des enseignements applicables à IndustriAlp, en distinguant les faits sourcés des hypothèses du scénario.

Rédiger une note lisible par un dirigeant non technique : trajectoire de remédiation priorisée et chiffrée, impacts sur la production, pertes financières envisagées, risques pour le personnel et les riverains, dépendances et conditions de réalisation.

Le programme prévoit également l’examen de la série IEC 62443 et des obligations LPM/OIV. L’applicabilité réglementaire à IndustriAlp reste à établir à partir des informations du cas et des textes en vigueur ; elle ne découle pas de la seule activité chimique.

## Compétences développées

| Compétence | Résultat attendu |
| --- | --- |
| Lire une architecture OT | Identifier les composants, leurs rôles, les flux et les actifs critiques. |
| Comprendre les protocoles industriels | Expliquer les usages, les limites et les possibilités de durcissement selon l’équipement. |
| Analyser les vulnérabilités | Relier chaque observation à son exploitabilité, aux conséquences industrielles et à une recommandation. |
| Concevoir une segmentation IT/OT | Justifier les zones, la DMZ, les flux autorisés et les accès distants. |
| Construire une réponse à incident OT | Articuler sécurité physique, coordination métier, confinement et collecte des preuves. |
| Analyser un incident réel | Extraire des enseignements techniques, organisationnels et humains à partir de sources vérifiées. |
| Conseiller une direction | Présenter des décisions priorisées, leurs coûts estimés, leurs impacts et leurs risques résiduels. |

## 📋 Modalités et livrables

| Livrable prévu | Contenu attendu |
| --- | --- |
| **Fiche de synthèse + schéma d’architecture OT** | Installation IndustriAlp : SCADA, PLC, RTU, IHM, historian et protocoles ; annotations sur les différences IT/OT et les enjeux de sécurité. |
| **Rapport de vulnérabilités + recommandations** | Au moins cinq vulnérabilités critiques documentées sur le réseau simulé, avec criticité justifiée, exploitabilité et recommandations. |
| **Schéma réseau sécurisé + configurations** | Segmentation, DMZ industrielle, protection des communications, configurations du pare-feu sauvegardées et commentées, justifications par référence à IEC 62443 et preuves de configuration. |
| **Playbook de réponse OT + compte rendu d’incident** | Réponse adaptée aux contraintes industrielles, test sur le scénario de commandes PLC non autorisées, écarts et améliorations. |
| **Note de recommandations IndustriAlp [P]** | Note pour la direction : trajectoire chiffrée et priorisée, impacts opérationnels, risques humains, exigences applicables et décisions proposées. Cinquième livrable **[P]** formel du parcours selon le programme fourni. |

### Statut des travaux et preuves

Cette page présente le **programme pédagogique fourni**. Les livrables sont attendus : aucune configuration, vulnérabilité observée, exécution de test ou conformité acquise n’est attestée ici.

Les futures fiches distingueront le scénario simulé, les hypothèses, les actions proposées, les actions exécutées et les preuves recueillies. Les coûts et pertes financières devront être accompagnés de leurs hypothèses ; les références techniques, historiques et réglementaires seront vérifiées lors des activités concernées.
