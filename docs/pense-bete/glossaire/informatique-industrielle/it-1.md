# Informatique industrielle — Itération 1

## Termes à retenir

| Terme | Rappel |
| --- | --- |
| IT | Systèmes de traitement et d’échange d’informations. |
| OT | Systèmes qui surveillent ou commandent un procédé physique. |
| Capteur | Mesure une grandeur physique. |
| Actionneur | Agit sur le procédé. |
| PLC / automate programmable industriel | Exécute la logique de commande. |
| HMI / IHM | Interface opérateur : états, alarmes et commandes autorisées. |
| SCADA | Supervision et acquisition de données d’une ou plusieurs installations. |
| Poste d’ingénierie | Programmation et configuration des équipements de contrôle. |
| Poste de maintenance | Diagnostic et interventions autorisées. |
| Consigne | Valeur ou objectif demandé à la régulation. |
| Hystérésis | Deux seuils et mémoire de l’état précédent : ici marche ≥ 4,5 °C, arrêt ≤ 3,5 °C pour une consigne à 4 °C. |
| Alarme temporisée | Ici T > 8 °C pendant au moins 10 secondes ; calcul et réinitialisation à vérifier dans le modèle. |
| Mode de repli | Comportement prévu lors d’une défaillance ; à vérifier dans la documentation. |
| Jumeau numérique | Représentation numérique du système étudié ; périmètre, données, actualisation et fidélité à préciser. |

## Gestes à retenir

- Rechercher où s’exécute la régulation et de quoi elle dépend.
- Distinguer perte de visibilité, perte de commande et conséquence physique.
- Séparer conséquence certaine, possibilité et condition d’architecture.
- Une supervision perdue n’implique pas nécessairement un processus arrêté.
- Une mesure incorrecte peut fausser la commande ; vérifier les contrôles et protections.
- Avant toute modification : coordination exploitation, essais, sauvegarde et retour arrière adapté.

## Manipulations faites

Vérification locale du laboratoire : **12 tests fournis réussis**, couvrant notamment TCP/Modbus et HTTP. Calculs directs du modèle : hystérésis, effet de consigne et effet de porte vérifiés. Dix captures utilisateur complètent ces résultats : CLI et navigateur, écoutes locales, consigne à 6 puis 4 °C, porte ouverte puis fermée, 12 tests réussis et paramètres finaux restaurés. Les délais thermiques et les instants exacts de bascule ne sont pas mesurés par ces images.

## Commandes du laboratoire

Depuis `livrables/informatique-industrielle/it-1/ot-refrigeration-poc/`, utiliser Python ≥ 3.10, sans paquet externe.

```bash
python3 -m lab.server                 # terminal 1 : 127.0.0.1:15020
python3 -m lab.dashboard              # terminal 2 : http://127.0.0.1:18080
python3 -m lab.client status          # terminal 3
python3 -m lab.client setpoint 6
python3 -m lab.client setpoint 4       # restauration
python3 -m lab.client door 1
python3 -m lab.client door 0           # fermeture
```

À retenir : consigne de 6 °C → seuils 5,5 / 6,5 °C ; changer la consigne ne change pas instantanément la température. La porte ouverte double l’apport thermique dans le modèle. La supervision est en lecture seule ; le contrôle et l’alarme restent dans le serveur Python. Arrêter les deux services par Ctrl + C après restauration.

## Docs associées

- [Sommaire et objectifs de la journée](../../../informatique-industrielle/it-1/index.md).
- [Atelier 1.1 — Découvrir l’OT et les systèmes industriels](../../../informatique-industrielle/it-1/decouvrir-ot-systemes-industriels.md) : composants, tableau des cinq événements et ressources ANSSI/NIST.

- [Atelier 1.2 — Étudier une installation frigorifique](../../../informatique-industrielle/it-1/etudier-installation-frigorifique.md) : schéma, seuils et réponses aux six questions.

- [Atelier 1.3 — Prendre en main le modèle frigorifique](../../../informatique-industrielle/it-1/prendre-en-main-modele-frigorifique.md) : procédure, réponses et résultats locaux.

## Atelier 1.4 — Défaut et diagnostic

```bash
python3 -m lab.client sensor-fault 1
python3 -m lab.client status
python3 -m lab.client sensor-fault 0
python3 -m lab.client status
```

- Défaut injecté → compresseur arrêté au prochain pas, selon une règle pédagogique.
- `sensor_fault=1` est visible en CLI, **pas dans le tableau de bord fourni**. La température simulée reste affichée.
- L’alarme haute température est distincte du défaut capteur.
- Redémarrer la seule supervision diffère de redémarrer l’hôte qui exécute aussi le contrôle.
- Calcul direct vérifié : départ 4 °C, défaut pendant 60 s simulées → 4,74 °C ; reprise de la marche après retrait du défaut. Deux captures utilisateur attestent le compresseur OFF à 5 °C après injection, puis ON à 5,2 °C après suppression, avec consigne 4 °C. Le seuil normal de marche de 4,5 °C est dépassé sur les deux images.
- Avant intervention : état physique, validité des mesures, dépendances, autorisation d’exploitation et reprise.

[Atelier 1.4 — Observer des dysfonctionnements et leurs conséquences](../../../informatique-industrielle/it-1/observer-dysfonctionnements-consequences.md) : réponses aux quatre questions et analyse A–E.

## Atelier 1.5 — Modifier l’hystérésis

- À consigne 4 °C : **±0,5 °C → marche 4,5 / arrêt 3,5 °C** ; **±1 °C → marche 5 / arrêt 3 °C**.
- Entre les seuils, absence de réaffectation : l’état précédent est conservé.
- Consigne : valeur utilisée par la règle ; logique : manière de décider. Ici les écarts sont codés en dur.
- Travailler sur une copie, sauvegarder `lab/model.py`, modifier uniquement les deux écarts et redémarrer le serveur.
- Le redémarrage recrée l’état initial, il ne conserve pas l’état thermique.
- Calcul local sur 600 s simulées : cycle après transitoire **116,2 s contre 232,2 s**. Moins de commutations, mais bande thermique élargie ; aucune économie d’énergie démontrée.
- Restaurer la copie initiale et contrôler avec `cmp` avant de relancer. Sept captures attestent la modification et le lancement, avec notamment 4,7 °C / OFF puis 4,9 °C / ON, cohérents avec la nouvelle hystérésis. Le franchissement de 5 °C, les durées de cycle et la restauration ne sont pas capturés.

[Atelier 1.5 — Étudier et modifier la logique de contrôle](../../../informatique-industrielle/it-1/etudier-modifier-logique-controle.md) : procédure, réponses et comparaison renseignée.

## Atelier 1.6 — Modèle, simulation et communications

- **Modèle :** représentation par états et règles. **Simulation :** calcul de son évolution dans le temps. Le laboratoire est un prototype sur spécification fictive, sans synchronisation avec une installation réelle.
- Processus, capteur simulé, contrôle et commande sont dans `Plant` ; leurs échanges sont internes au programme Python.
- Navigateur → HTTP 18080 → supervision → Modbus TCP 15020 → serveur de contrôle. La maintenance accède directement au serveur Modbus.
- Adresses PDU à partir de zéro ; toujours préciser la table : holding 0 = consigne, input 0 = température, input 1 = compresseur, coil 0 = porte, input 2 = alarme.
- Lecture : FC03 holding, FC04 input, FC01 coils, FC02 discrete inputs. Écriture : FC06 consigne, FC05 porte/défaut.
- 40 en registre de température/consigne → 4 °C. Limites de représentation des températures négatives à conserver dans l’analyse.
- Validation : version, conditions initiales, données horodatées, critères d’acceptation et preuve des résultats. Les tests logiciels ne valident pas une installation réelle.
- Avant J2 : confirmer la restauration des seuils ±0,5 °C ; l’analyse des trames est à venir.

[Atelier 1.6 — Préparer la construction du jumeau numérique](../../../informatique-industrielle/it-1/preparer-jumeau-numerique.md) : schéma, table des variables et synthèse de clôture de la journée.

## Atelier 1.7 — OpenPLC, optionnel

- **Editor :** élaboration du projet. **Runtime :** exécution et échanges avec les interfaces configurées.
- Le Runtime v4 expose une API HTTPS sur 8443, pas une interface web de gestion ; utiliser l’Editor compatible. Voir les sources datées dans la fiche.
- `optional/thermostat.st` reprend l’hystérésis ±0,5 °C et la priorité au défaut, mais pas le mode automatique ni la temporisation d’alarme du Python.
- Un fichier ST avec variables initialisées ne reçoit pas automatiquement une mesure ni ne pilote le compresseur simulé.
- Connexion future : physique séparée, mesure vers PLC, commande vers modèle, mapping et cycle validés, une seule autorité de commande.
- Neuf captures attestent l’Editor ouvert, le projet ST et le débogueur : 5 °C → marche, 3,2 °C → arrêt, 9 °C → marche et alarme. À 4,2 °C, arrêt affiché sans preuve de continuité entre essais. Déploiement Runtime, défaut ST et boucle avec Python non attestés ; activité facultative.

[Atelier 1.7 — Découvrir OpenPLC](../../../informatique-industrielle/it-1/decouvrir-openplc.md) : sources officielles, installation proposée et comparaison renseignée.

## Atelier 1.8 — FUXA, optionnel

- Interface web de supervision, édition et consultation ; contrairement à l’Editor Electron, aucun transfert X11 requis.
- Procédure proposée : conteneur, port publié **127.0.0.1:1881** dans la VM ; conserver digest/version et volumes persistants.
- Depuis le poste : `ssh -N -L 127.0.0.1:1881:127.0.0.1:1881 oliv@192.168.122.106`, puis `http://127.0.0.1:1881`.
- Vue demandée : température, consigne, état compresseur, état alarme ; valeurs statiques autorisées et signalées comme telles.
- Un voyant ne prouve pas une règle d’alarme testée ; un écran ne prouve pas une connexion au procédé.
- Dans le conteneur, `127.0.0.1` n’est pas la VM. La future connexion Modbus nécessite son propre chemin et mapping.
- Trois captures attestent FUXA 1.3.5-2968, le conteneur actif, le mapping local 1881, HTTP 200, l’éditeur et la vue statique réalisée (4,2 °C / consigne 4 °C / arrêt gris / aucune alarme). Aucune connexion industrielle ni règle d’alarme testée ; persistance après réouverture non attestée.

[Atelier 1.8 — Découvrir FUXA](../../../informatique-industrielle/it-1/decouvrir-fuxa.md) : commandes, écran proposé et cinq réponses.

## Journée 2 — Atelier 2.1 : Modbus TCP

**Même itération 1**, journée 2. Analyse documentaire en autonomie, sans nouvelle capture réseau attestée.

| Code | Opération |
| --- | --- |
| FC01 | Lire les coils (bits). |
| FC02 | Lire les discrete inputs (bits). |
| FC03 | Lire les holding registers (16 bits). |
| FC04 | Lire les input registers (16 bits). |
| FC05 | Écrire une coil. |
| FC06 | Écrire un holding register. |

- Toujours associer table, adresse, type et unité ; les droits dépendent du serveur.
- Modbus TCP conventionnel : port 502 ; laboratoire : **15020**. Modbus Security/TLS : port 802, non implémenté dans ce laboratoire.
- Le conventionnel ne fournit ni chiffrement ni authentification native ; un client joignable n’est pas pour autant autorisé au sens métier.
- `status` utilise FC03, FC04 et FC01 ; `setpoint 6` écrit **60** par FC06 à l’adresse holding 0.
- Le navigateur parle HTTP au dashboard ; le dashboard est client Modbus.

[2.1 — Découvrir les communications Modbus TCP](../../../informatique-industrielle/it-1/decouvrir-communications-modbus-tcp.md) : tableaux, exemples du code et sources officielles datées.

## Complément — Architecture cible isométrique

[Capture du 27 octobre et analyse](../../../informatique-industrielle/it-1/preparer-jumeau-numerique.md#complement-du-27-octobre-architecture-cible-securisee-proposee) : zone bleue = **enceinte frigorifique** ; maintenance proposée via bastion ; supervision avec un chemin distinct. Les protections et le retour d’état du compresseur sont des intentions de conception, pas des fonctions déployées et prouvées dans le laboratoire Python.

## Journée 2 — Atelier 2.2 : Wireshark / tcpdump

- Dans la VM : `sudo tcpdump -i lo -nn -s 0 -w modbus-j2.pcap 'tcp port 15020'` ; arrêter avec Ctrl + C après les opérations.
- Copier le PCAP vers le poste par `scp`, puis l’ouvrir dans Wireshark ; le bouclage de la VM n’est pas celui du poste.
- Filtre d’affichage : `tcp.port == 15020`. Décoder le port en **Modbus/TCP** via Analyze → Decode As si nécessaire.
- FC03/FC04/FC06 : `modbus.func_code == 3`, `4` ou `6` ; ces filtres incluent requêtes et réponses.
- Consigne 6 °C : **FC06, holding 0, valeur 60 / 0x003C**. Réponse normale = écho adresse/valeur ; ACK TCP seul insuffisant.
- MBAP : transaction 2 octets, protocole 2, longueur 2, unité 1. Longueur = unité + PDU.
- Ce client fixe Transaction ID et unité à 1 ; apparier aussi par flux TCP. Chaque requête ouvre une connexion locale avec un port client éphémère.
- Aucune identité humaine dans la requête Modbus conventionnelle. Dix captures reçues : FC06 **34 → 36**, port client **60894**, valeur **60**, réponse **284 µs** ; **74 → 76**, port client **60928**, valeur **40**, réponse **486 µs**. Détails FC03/FC04 et PCAP brut restent à fournir.

[2.2 — Analyser les échanges Modbus dans Wireshark](../../../informatique-industrielle/it-1/analyser-echanges-modbus-wireshark.md) : procédure, exemple hexadécimal déduit du code et réponses.

- Dépannage Wireshark observé : décodage partiel et Query/Response inversés ; vérifier le port serveur Modbus/TCP **15020**, pas un port client éphémère. Le marquage initial « malformed » ne suffit pas à conclure à un défaut de trame.

## Journée 2 — Atelier 2.3 : variables et erreurs

- Table complète dans la fiche : consigne holding 0 ; température input 0 ; compresseur input 1 / discrete 0 ; porte coil 0 ; alarme input 2 / discrete 1 ; défaut coil 1 / input 3 ; mode auto holding 2.
- `door 1` : **FC05, coil 0, 0xFF00** ; `door 0` : **0x0000**. Consigne : FC06 et entier en dixièmes de °C.
- `Client("127.0.0.1", 15020).request(3, 100, 1)` : réponse attendue **exception 02 — Illegal Data Address**, PDU **83 02**.
- Une exception applicative est une réponse de refus ; un timeout n’identifie pas à lui seul sa cause. Lire le message exact et les paquets avant intervention.
- Test local temporaire : porte lue 0 → 1 → 0 et exception 02 reçue. Huit captures utilisateur ajoutées : FC03 14/16 et 54/56, requête FC04 pour 4 registres, FC05 4/6 et 44/46, fermeture coil 0 à 0x0000. Détails d’ouverture, réponses de lecture à compléter ; test Python utilisateur à l’adresse 100 attesté avec exception 02. Numérotation propre à cette session.
- Fin de TP : consigne 4 °C, porte fermée, `status` conservé.

[2.3 — Cartographier les variables et tester les opérations Modbus](../../../informatique-industrielle/it-1/cartographier-variables-tester-modbus.md) : table, commandes corrigées et réponses.

## Journée 2 — Atelier 2.4 : synthèse collective

- Chaîne : commande client → registre / consigne → décision du contrôleur → commande compresseur → évolution thermique.
- Dans ce modèle, registre holding 0 et consigne sont la même donnée interne exposée par Modbus : pas de copie vers un PLC matériel séparé.
- Écriture lors du traitement ; commande au pas suivant ; température progressive ; affichage selon son rafraîchissement.
- Les réponses FC06 à 284 / 486 µs ne mesurent pas un délai thermique. Les captures J1 et J2 ne sont pas une unique trace synchronisée.
- Exception 02 : serveur joint mais adresse/quantité refusée ; diagnostic différent d’un timeout.
- Limites : physique simplifiée, entrées/sorties simulées, temps non garanti, protections matérielles absentes du modèle.
- Support préparé ; comparaison entre binômes, corrections du formateur et démonstration collective non encore attestées.

[2.4 — Mettre en commun les observations sur Modbus](../../../informatique-industrielle/it-1/mettre-en-commun-observations-modbus.md) : tableaux de restitution et chaîne causale.

## Journée 2 — Atelier 2.5 : assemblage et passerelle

- `lab.server` : **15020** ; `lab.dashboard` : HTTP **18080**, client Modbus direct vers 15020 ; `lab.gateway` : **15021** vers 15020.
- `python3 -m lab.client status --port 15021` : lectures FC03/FC04/FC01 relayées vers la même instance `Plant`.
- `python3 -m lab.client setpoint 6 --port 15021` : refus **exception 01 — Illegal Function**, réponse attendue **86 01**.
- La passerelle autorise uniquement FC01–FC04 ; le port direct 15020 reste accessible en écriture. Filtrage sur un chemin ≠ segmentation réseau.
- Supervision par défaut hors passerelle ; elle lit Modbus, pas les variables Python internes.
- Test local réussi : lecture par les deux chemins, écriture directe visible via proxy, écriture via proxy refusée, valeur inchangée puis restauration directe. Supervision non testée dans cette session ciblée.
- 15 captures utilisateur et assemblage-j2.pcap analysés : 2554/2564 lecture via 15021 ; 2734/2736 écriture directe 60 ; 8204/8206 restauration directe 40 ; 11574/11576 refus 86 01 via 15021. Bastion, OpenPLC et FUXA ne sont pas raccordés par cette procédure.

[2.5 — Assembler les composants du jumeau numérique](../../../informatique-industrielle/it-1/assembler-composants-jumeau-numerique.md) : schéma, commandes et quatre réponses.

Filtre ciblé du PCAP d’assemblage, avec **virgules** :

```text
frame.number in {2554,2564,2734,2736,8204,8206,11574,11576}
```

## Journée 2 — Atelier 2.6 : validation

- Six scénarios : normal, consigne, porte, défaut, lecture relayée, écriture refusée.
- Définir version, état initial et résultat attendu avant chaque essai ; relever observations et écarts, puis conserver les preuves.
- Redémarrer réinitialise l’état du modèle, **pas le code de l’hystérésis**. Remettre les paramètres ne restaure pas à lui seul la température initiale.
- La température est progressive ; porte ouverte = apport accru, pas nécessairement réchauffement si le froid reste suffisant.
- Preuves 2.5 établies : lecture via proxy et refus d’écriture. Les scénarios thermiques disposent de captures partielles et de calculs locaux, pas d’une campagne utilisateur exhaustive.
- Limites : compresseur simplifié, absence de matériel, thermique non calibrée, pas de synchronisation réelle, protections partielles.
- Fin : consigne 4 °C, porte fermée, défaut inactif, auto actif ; noter la version, la température et tout redémarrage. Validation collective non encore attestée.

[2.6 — Valider les comportements du jumeau numérique](../../../informatique-industrielle/it-1/valider-comportements-jumeau-numerique.md) : matrice V1–V6 et état des preuves.

### Résultats utilisateur 2.6 — série du 27 octobre

Six captures intégrées : essais à **consigne 6 °C**, porte ouverte puis fermée, défaut actif avec compresseur arrêté, puis défaut à 0 / compresseur actif ; lectures directe/passerelle concordantes. Fin : consigne ramenée à **4 °C**, tentative à 6 °C via proxy refusée (exception 01), relecture à 4 °C, porte fermée, défaut inactif, auto actif.

Les relevés montrent des pentes thermiques différentes mais à températures initiales différentes. Cycle complet V1, version des seuils, bascule précisément provoquée par le défaut et appréciation du formateur restent non attestés. Paramètres restaurés ≠ température déjà stabilisée.

## Journée 2 — Atelier 2.7 : dossier C2

[Dossier unique J2](../../../informatique-industrielle/it-1/J2-validation-jumeau-numerique.md) et [PDF formateur, 7 pages](../../../assets/files/informatique-industrielle/it-1/J2-validation-jumeau-numerique-Olivier-HIMBLOT.pdf). Architecture réelle, table Modbus, captures et PCAP, six scénarios avec portée des observations, limites. Version des seuils, cycles complets et appréciation du formateur à confirmer. Conserver les fichiers pour J3 ; ne pas confondre passerelle de lecture et segmentation effective.
