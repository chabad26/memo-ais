# Itération 1 — Découvrir une installation industrielle automatisée

## Journée 1 — Objectifs

Découvrir le fonctionnement d’une installation industrielle automatisée et comprendre les différences entre un système **OT — Operational Technology** et une infrastructure IT classique.

À partir de la documentation d’une **installation frigorifique fictive** et d’un **modèle logiciel prévu par les consignes**, identifier les composants, observer le fonctionnement et étudier les conséquences de différentes situations sur le processus physique.

À l’issue de la journée, pouvoir expliquer le fonctionnement général de l’installation et identifier les informations nécessaires pour construire son **jumeau numérique**.

## Journée 1 — Fiches

- [1.1 — Atelier 1 | Découvrir l’OT et les systèmes industriels](decouvrir-ot-systemes-industriels.md) : comparaison IT/OT, composants et analyse des cinq événements.
- [1.2 — Atelier 2 | Étudier une installation frigorifique](etudier-installation-frigorifique.md) : schéma fonctionnel annoté, hystérésis, alarme et six réponses renseignées.
- [1.3 — Atelier 3 | Prendre en main le modèle frigorifique](prendre-en-main-modele-frigorifique.md) : lancement Linux, lectures Modbus, consigne, porte, dix captures commentées et vérifications locales.
- [1.4 — Atelier 4 | Observer des dysfonctionnements et leurs conséquences](observer-dysfonctionnements-consequences.md) : défaut capteur, limites de supervision et analyse des situations A–E.
- [1.5 — Atelier 5 | Étudier et modifier la logique de contrôle](etudier-modifier-logique-controle.md) : repérage du code, modification sur copie, comparaison ±0,5 / ±1 °C et restauration.
- [1.6 — Atelier 6 | Préparer la construction du jumeau numérique](preparer-jumeau-numerique.md) : fonctions dans le code, schéma numérique, registres et synthèse pour le J2.
- [1.7 — Atelier 7 optionnel | Découvrir OpenPLC](decouvrir-openplc.md) : Editor/Runtime, parcours d’installation, lecture du ST et limites d’intégration.
- [1.8 — Atelier 8 optionnel | Découvrir FUXA et la supervision industrielle](decouvrir-fuxa.md) : installation locale, tunnel SSH, écran de démonstration et bilan HMI/SCADA.
- [Pense-bête de l’itération](../../pense-bete/glossaire/informatique-industrielle/it-1.md).

## Journée 2 — Communications et validation du jumeau numérique

**La journée 2 appartient toujours à l’itération 1.** La numérotation 2.1 désigne le premier atelier du J2, pas une nouvelle itération.

Comprendre les communications entre composants pour assembler et valider un jumeau numérique simplifié. À partir du modèle frigorifique du J1, analyser les échanges Modbus TCP, identifier les variables de contrôle et de supervision, puis vérifier les comportements attendus de l’installation fictive à l’aide de tests documentés.

**Matinée en autonomie**, avec ressources et entraide du groupe ; **après-midi avec le formateur**, pour mise en commun, validation de l’environnement et essais. En fin de journée, pouvoir expliquer les échanges et démontrer le fonctionnement par des tests documentés.

### Fiches de la journée 2

- [2.1 — Découvrir les communications Modbus TCP](decouvrir-communications-modbus-tcp.md) : 1 h en autonomie, données, fonctions et propriétés de sécurité ; réponses renseignées.
- [2.2 — Analyser les échanges Modbus dans Wireshark](analyser-echanges-modbus-wireshark.md) : capture sur lo, parcours tcpdump/SSH, décodage, MBAP et dix captures commentées ; FC06 confirmé, FC03/FC04 et PCAP brut à compléter.
- [2.3 — Cartographier les variables et tester les opérations Modbus](cartographier-variables-tester-modbus.md) : 1 h 15 en autonomie, table complétée, huit captures FC01/FC03/FC04/FC05 et test Python ; exception 02 attestée dans la session utilisateur.
- [2.4 — Mettre en commun les observations sur Modbus](mettre-en-commun-observations-modbus.md) : support de débrief, chaîne consigne/commande/température et limites du modèle ; collectif à confirmer.
- [2.5 — Assembler les composants du jumeau numérique](assembler-composants-jumeau-numerique.md) : deux chemins, 15 captures et PCAP analysé ; lecture relayée, écriture directe acceptée et refus via passerelle attestés.
- [2.6 — Valider les comportements du jumeau numérique](valider-comportements-jumeau-numerique.md) : six scénarios et six captures de validation commentées ; consigne, porte, défaut et passerelle observés, limites et validation collective explicitées.
- [2.7 — Finaliser le dossier de validation](J2-validation-jumeau-numerique.md) : dossier C2 consolidé et PDF formateur de 7 pages, architecture, variables, preuves, résultats et limites.
- [Pense-bête commun de l’itération 1](../../pense-bete/glossaire/informatique-industrielle/it-1.md).

Les ateliers suivants seront ajoutés à réception des consignes. L’analyse documentaire 2.1 ne constitue pas encore une capture de trames ou une validation du modèle assemblé.

## Livrable formateur — J1

**Version V3 — présentation verticale par niveaux Purdue, selon l’exemple du formateur :** [dossier PDF, 3 pages](../../assets/files/informatique-industrielle/it-1/Schema-architecture-OT-J1-Olivier-HIMBLOT-V3.pdf) · [schéma A3 portrait](../../assets/files/informatique-industrielle/it-1/Schema-architecture-OT-J1-Olivier-HIMBLOT-Purdue.pdf) · [source draw.io](../../assets/files/informatique-industrielle/it-1/Schema-architecture-OT-J1-Olivier-HIMBLOT-Purdue.drawio).

Les fonctions du laboratoire sont placées aux niveaux 0–2 ; les niveaux supérieurs et la DMZ restent des repères non documentés. Il ne s’agit pas d’une segmentation mise en œuvre. Repérage fonctionnel : [Cisco — Industrial Security 3.1, chapitre 2](https://www.cisco.com/c/dam/en/us/td/docs/Technology/Industrial-Security-3-1-DG.pdf).


**Version V2 — présentation de type Visio :** [dossier PDF, 3 pages](../../assets/files/informatique-industrielle/it-1/Schema-architecture-OT-J1-Olivier-HIMBLOT-V2.pdf) · [schéma A3 seul](../../assets/files/informatique-industrielle/it-1/Schema-architecture-OT-J1-Olivier-HIMBLOT-Visio.pdf) · [source modifiable draw.io](../../assets/files/informatique-industrielle/it-1/Schema-architecture-OT-J1-Olivier-HIMBLOT-Visio.drawio).

Pictogrammes d’équipements, zones fonctionnelles et connecteurs orthogonaux ; le laboratoire initial reste la référence représentée.


[📄 Schéma d’architecture OT annoté — Olivier HIMBLOT (PDF, 3 pages)](../../assets/files/informatique-industrielle/it-1/Schema-architecture-OT-J1-Olivier-HIMBLOT.pdf)

Composants, fonctions et interactions du laboratoire frigorifique ; distinction contrôle local / supervision et deux captures commentées du défaut capteur.

### Architecture cible proposée par l’apprenant

[Schéma isométrique du 27 octobre : enceinte frigorifique, bastion et chemins de maintenance/supervision](preparer-jumeau-numerique.md#complement-du-27-octobre-architecture-cible-securisee-proposee). Capture intégrée comme proposition d’architecture, distincte du laboratoire observé et des configurations effectivement déployées.

## État des éléments disponibles

Les consignes des ateliers 1.1 à 1.8 sont intégrées. Le laboratoire est disponible dans `livrables/informatique-industrielle/it-1/ot-refrigeration-poc/` : README, table des registres, modèle Python, serveur/client Modbus, supervision et tests ont été examinés. Les 12 tests fournis ont réussi localement ; des calculs directs du modèle vérifient les bascules, la consigne et l’effet de la porte. Dix captures de la session utilisateur attestent désormais la supervision, les lectures CLI, les écoutes locales, les modifications de consigne, la porte, les 12 tests et les paramètres restaurés. Les délais précis, les seuils de bascule et la mise en commun restent à documenter.

L’atelier 1.4 est renseigné à partir du code ; un calcul direct du modèle vérifie l’arrêt sur défaut et la reprise. Deux captures utilisateur attestent l’injection du défaut avec compresseur arrêté à 5 °C, puis sa suppression avec reprise à 5,2 °C. Les échanges en binôme restent à documenter.

L’atelier 1.5 propose une modification sur copie et un livrable comparatif fondé sur deux calculs de 600 secondes simulées ; aucune modification du laboratoire fourni n’a été conservée. Sept captures utilisateur attestent le code initial, les deux changements de seuil, le lancement et des états du modèle modifié, notamment 4,7 °C avec compresseur arrêté. Les cycles chronométrés et la restauration restent à attester.

L’atelier 1.6 consolide les composants numériques, les échanges et les limites du modèle ; la version restaurée, les critères de validation et la restitution collective restent à confirmer. L’analyse détaillée des trames est réservée au J2.

L’atelier optionnel 1.7 est renseigné sur les fichiers et la documentation officielle : comparaison ST/Python et distinction Editor/Runtime v4. Neuf captures attestent désormais l’environnement Debian, l’ouverture de l’Editor 4.3.2, le projet ST et des états affichés dans le débogueur. Aucun déploiement sur Runtime distinct ni liaison au modèle Python n’est attesté.

Trois captures de l’atelier optionnel 1.8 attestent FUXA 1.3.5-2968 en fonctionnement, la publication locale du port 1881, HTTP 200, l’éditeur et une vue statique avec les quatre indicateurs. Aucune connexion au modèle n’est demandée ni attestée.

Le programme général mentionne IndustriAlp, une usine chimique. L’itération 1 utilise une installation frigorifique fictive ; son rattachement à IndustriAlp n’est pas précisé et n’est pas supposé.

Les activités suivantes seront ajoutées à réception des consignes.

[Retour au module](../README.md)
