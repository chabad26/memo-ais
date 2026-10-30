# 5.1 — Atelier 1 | Prendre connaissance de l’incident

## 🎯 Objectif et modalités

Comprendre la situation initiale, identifier les informations disponibles et définir les premières vérifications nécessaires.

- **Modalité :** présentation du scénario et analyse en binôme avec le formateur.
- **Durée :** à compléter, non précisée dans la consigne.
- **Supports :** manuel MAN-OT-01, architecture Montval et dossier d’incident fourni.

!!! info "Statut de l’analyse au 30 octobre 2026"
    Il s’agit d’un **incident fictif du 8 octobre 2026**. Les documents et premiers exports ont été examinés et inventoriés ; la capture réseau est conservée mais n’est pas encore décodée dans cette fiche. Les vérifications sur équipements, entretiens et reproductions PoC ci-dessous sont **à réaliser**, pas des résultats acquis. Aucune intervention n’est effectuée sur la VM ou une installation réelle pour cette prise de connaissance.

## 1 — Situation initiale et portée des informations

Montval signale une hausse de température sur **ZF-02, réserve produits laitiers**, commandée par **REG-02**. Une modification de consigne a été relevée ; le magasin ne connaît pas de demande applicable. FrigoMaint dispose d’un accès distant de maintenance. REG-02 est ancien, sans support ni correctif disponible et doit rester en exploitation faute de remplacement financé.

La mission situe la demande de contribution de l’équipe IT à **10:04**. Le journal de SUP-01 mentionne un passage de **4 à 12 °C à 09:14**, une alarme à **09:52** et un acquittement à **10:04**. Ce sont des informations enregistrées dans des **sources du scénario**, à confronter aux autres traces ; elles ne désignent pas à elles seules une personne ni une intention.

| Élément initial | Statut et interprétation prudente |
| --- | --- |
| Hausse de température signalée | Information de scénario, avec export de mesures disponible ; vérifier mesure de l’enceinte, état réel et situation des lots. |
| Consigne inhabituelle | Journal SUP-01 : 4 → 12 °C ; confirmer adresse, valeur et réponse serveur dans le PCAP, puis confronter aux mesures. |
| Magasin et FrigoMaint ne déclarent pas de changement à 12 °C | Déclarations à documenter ; absence de demande connue ≠ preuve qu’aucun document n’existe. |
| Accès distant disponible | Chemin possible à examiner ; disponibilité d’accès ≠ utilisation malveillante prouvée. |
| REG-02 non maintenu | Contrainte documentée ; ne prouve ni exploitation d’une vulnérabilité ni cause de l’incident. Aucune CVE ou version constructeur n’est fournie. |
| Autorisation de remise à 4 °C à 10:18 et action déclarée à 10:21 | Ticket INC-881 ; SUP-01 rapporte aussi le retour à 4 °C. Vérifier l’exécution et les contrôles de remise en service, sans la refaire comme si elle était encore en attente. |

Le PoC J4 est un laboratoire séparé. Le dossier indique que l’architecture réellement en place peut différer des propositions J3/J4 : **ne pas affirmer qu’un bastion, GW-02 ou les 32 règles existaient sur le site lors de l’incident**. La VM `192.168.122.105` et les adresses `10.77.*` ne sont pas les équipements du scénario.

## 2 — Inventaire des sources reçues

[Télécharger les sept fichiers du dossier](../../assets/files/informatique-industrielle/it-4/Montval-J5-Incident_dossier.zip) · [Inventaire, tailles et SHA-256](../../assets/files/informatique-industrielle/it-4/Montval-J5-inventaire-sources.json) · [Mission](../../assets/files/informatique-industrielle/it-4/01_mission.md) · [Sources et horloges](../../assets/files/informatique-industrielle/it-4/02_sources_et_horloges.md).

| Fichier | Apport pour l’investigation | Limite à conserver |
| --- | --- | --- |
| `01_mission.md` | Périmètre ZF-02/REG-02, demande à 10:04, objectifs et contraintes. | Scénario pédagogique, pas compte rendu d’une intervention réelle. |
| `02_sources_et_horloges.md` | Adresses, registre, horloges et fiabilité. | Documente la normalisation ; ne garantit pas l’exhaustivité des traces. |
| `temperatures_ZF02_2026-10-08.csv` | Mesure par minute, consigne, commande compresseur, alarme et qualité. | Export 08:30–11:30 ; température enregistrée de l’enceinte, pas température produit. Un état de commande ne prouve pas le mouvement physique du compresseur. |
| `evenements_SUP01.csv` | Changements de consigne, alarme, acquittement et suivi. | Horloge locale CEST ; origine technique déclarée, pas authentification humaine. |
| `maintenance_FrigoMaint.csv` | Tickets, autorisations, actions et déclarations des intervenants. | Informations saisies potentiellement incomplètes ; distinguer autorisation et réalisation. |
| `acces_distants_VPN.csv` | Ouvertures et fermetures de session vers MAINT-01, comptes et sources réseau. | Horloge en avance de 2 min 10 s ; le compte partagé `maint-shared` ne désigne pas une personne unique. |
| `modbus_REG02_capture.pcap` | Échantillon synthétique TCP/Modbus sur le segment de REG-02. | Trace partielle ; analyse des requêtes/réponses à réaliser. Aucun paquet absent ne prouve seul l’absence d’une action. |

Les originaux sont conservés dans `livrables/informatique-industrielle/it-4/Incident_dossier/`. L’archive contient leurs octets sans modification. Les empreintes établissent une référence de la copie reçue le 30 octobre ; elles ne certifient pas l’authenticité antérieure des événements. Travailler sur des copies et garder fichier, ligne ou numéro de trame pour chaque constat.

### Horloges et adresses à ne pas confondre

- **SUP-01, mesures et tickets :** heures locales du scénario avec `+02:00` lorsqu’indiqué.
- **VPN :** soustraire **00:02:10** à l’horodatage brut avant corrélation avec SUP-01 ; conserver les deux valeurs et le motif de correction.
- **PCAP :** temps en UTC ; choisir explicitement l’affichage Wireshark. Pour le 8 octobre, les horodatages locaux fournis sont en UTC+02:00.
- **Adresses du scénario :** REG-02 `10.30.10.22:502`, MAINT-01 `10.30.20.15`, SUP-01 `10.30.20.10`, consultation `10.30.20.30`.
- **Registre documenté :** Holding Register PDU **0**, consigne en dixièmes de °C ; `40` = 4 °C, `120` = 12 °C. FC03 lit, FC06 écrit.

Exemple de normalisation : l’ouverture VPN horodatée **09:14:10+02:00** correspond à **09:12:00+02:00** sur la référence SUP-01. Une proximité temporelle peut étayer un chemin technique ; elle n’identifie pas son opérateur humain. Conserver les IP sources exactement telles que fournies, sans en déduire une localisation, une réputation ou un propriétaire.

## 3 — Enjeux d’exploitation et fonctions à préserver

| Enjeu / question | Réponse fondée sur le manuel | Vérifications et limites |
| --- | --- | --- |
| Fonctions de REG-02 | Acquisition locale et commande du groupe de ZF-02 selon mesure, consigne et hystérésis ; paramètres conservés localement. EXP-01 à EXP-03. | Vérifier sonde, alimentation, état de porte et groupe ; ne pas confondre panne de supervision et arrêt de régulation. |
| Consigne élevée | Peut retarder le démarrage du compresseur ou modifier ses cycles et laisser augmenter la température avant le nouveau seuil. EXP-02/03. | La relation temporelle avec la hausse doit être étayée ; une porte ouverte, un défaut capteur ou du groupe peuvent aussi contribuer. |
| Alarmes attendues | EXP-07 : température **strictement supérieure à 8 °C pendant 10 minutes**. EXP-08 : affichage OPS-01 et signal local selon capacités du REG. | Vérifier historique, continuité des mesures, horaire de déclenchement, signalement et acquittement. Le PoC utilise **10 secondes**, pas 10 minutes. |
| Acquittement | EXP-09 : confirme la prise en compte, sans corriger température, consigne ou commande. | L’acquittement à 10:04 ne démontre pas un rétablissement du froid. |
| Continuité de régulation | EXP-01 : la boucle locale doit rester active si ses composants sont opérationnels, même sans SUP-01 ou OPS-01. | Éviter coupure générale ou redémarrage du REG sans coordination ; vérifier comportement réel avant isolement. |
| Qualité et sécurité des produits | EXP-12 : décision de l’exploitation selon les procédures du magasin. | Obtenir lots, durées d’exposition, mesures indépendantes et procédures ; ne pas conclure à la conformité depuis un CSV d’enceinte. |
| Supervision et traçabilité | EXP-04 à EXP-06 : fraîcheur et dates, mesures par minute, changements et alarmes, conservation prévue 90 jours. | Conserver exports originaux, décalages d’horloge et périodes manquantes ; vérifier disponibilité des données au-delà de cet échantillon. |
| Retour au service | EXP-10/11 et MAI-08 : contrôler état réel, températures, commandes, alarmes, supervision et paramètres. | Un écran disponible, un retour à 4 °C de consigne ou une alarme terminée ne suffisent pas à qualifier les denrées. |

**Sécurité IT :** examiner les accès, le poste MAINT-01, les chemins réseau et les écritures sans justification. **Continuité OT :** préserver le contrôle local et la capacité de diagnostic. **Produits :** décision spécifique de l’exploitation. **Traçabilité :** garder les heures, autorisations, actions et contrôles. Ces quatre besoins doivent être traités ensemble.

### Acteurs et contraintes d’intervention

| Intervenant | Vérification ou décision attendue |
| --- | --- |
| Responsable d’exploitation | Confirme les dérogations, autorise les actions touchant au froid et traite les produits ; coordonne l’urgence. |
| Personnel magasin / OPS-01 | Précise premier constat, signalement, acquittement, relève locale et mouvements de marchandises. |
| FrigoMaint | Confirme tickets, techniciens, outils, sessions et paramètres ; assure diagnostic et vérification industrielle. |
| Équipe IT / responsable des accès distants | Préserve traces et configurations, vérifie sessions, poste et filtrage ; propose un confinement ciblé. |
| Responsable SUP-01 | Fournit événements, mesures, fraîcheur, règles d’alarme et cohérence d’horodatage. |

MAI-01/02 imposent autorisation et traçabilité ; MAI-03 rend l’accès distant utile aux interventions, pas à la régulation permanente ; MAI-05/06 imposent préparation, coordination et fenêtres adaptées. ORG-01/02 organisent le partage des décisions. Le créneau usuel du mardi ne suffit pas à autoriser une coupure et n’interdit pas une urgence coordonnée. L’obsolescence empêche de retenir un simple correctif logiciel comme solution immédiate dans ce scénario.

## 4 — Préparer l’investigation avant toute conclusion d’attaque

| Vérification proposée | Informations à recueillir / interlocuteur | Ce qu’elle permettrait de déterminer |
| --- | --- | --- |
| Confirmer état réel et urgence | Exploitation et FrigoMaint : mesure indépendante, groupe, porte, défauts, lots et autres zones. | Besoin de protection des produits et contraintes de disponibilité avant action IT. |
| Vérifier consigne et trace d’écriture | PCAP : requête FC06, PDU 0, valeur, réponse/exception, source, transaction ; lecture ultérieure et SUP. | Différencier écriture demandée, acceptée, valeur relue et effet progressif. |
| Rechercher une autorisation | Tickets, dérogations, appels, astreinte, exploitation et FrigoMaint. | Autorisation documentée, périmètre exact et éventuelle action non justifiée ; sans assimiler absence de pièce reçue à absence certaine. |
| Rapprocher VPN et MAINT-01 | Journaux corrigés, sessions sur poste, comptes/outils/processus, identité des utilisateurs et éventuel partage de compte. | Chemin d’accès et origine technique ; une session seule ne prouve pas l’auteur d’une écriture. |
| Contrôler chemins réels et protections | IT : réseau, règles actives, NAT, VPN, accès locaux/alternatifs, exposition Modbus au moment des faits. | Différence entre architecture proposée et déployée ; possibilité de contournement, sans l’inventer. |
| Confronter aux autres causes | Mesures, défauts capteur, porte, commande et fonctionnement mécanique, FrigoMaint. | Départager modification de consigne et causes contributives physiques ou techniques. |
| Préserver et compléter les traces | SUP, VPN, MAINT, REG si journal disponible ; dates, rétention, configurations et versions. | Lacunes, fiabilité, horloges et possibilité d’attribution ; pas d’attribution par la seule IP. |
| Vérifier les actions de retour au service déjà déclarées | INC-881, accord de 10:18, action de 10:21, suivi et validation sur place. | Ce qui a été exécuté, par qui selon quelle source, et ce qui reste à contrôler ; éviter une action corrective doublonnée. |

### Questions à poser

**À l’exploitation :** quand et comment l’anomalie a-t-elle été remarquée ? Qui a reçu et acquitté l’alarme ? Une dérogation était-elle autorisée ? Quels lots et relevés locaux sont concernés ? Quels contrôles ont suivi le retour déclaré à 4 °C ? Quelles actions sont possibles sans arrêter le froid ?

**À FrigoMaint :** FM-426 autorisait-il seulement la lecture, ou également la réécriture à 4 °C mentionnée à 08:46 ? Qui utilisait MAINT-01 et le compte partagé lors des sessions ? Existe-t-il un ticket pour la session ultérieure ? Quelle commande, quel outil et quelle validation ont accompagné le retour à 4 °C ? Quels journaux et sauvegardes peuvent être fournis ?

**À l’IT et au responsable de supervision :** quelle topologie était réellement active le 8 octobre ? Qui administrait le VPN et les droits ? Les heures et les exports sont-ils complets ? Existe-t-il une trace de session applicative sur MAINT-01 ou un autre chemin d’écriture ? Quelles mesures conservatoires préserveraient lecture et contrôle local ?

## 5 — Hypothèses et mesures conservatoires à discuter

| Hypothèse, non conclusion | Éléments nécessaires pour l’étayer ou la réfuter |
| --- | --- |
| Erreur de maintenance ou d’outil | Commandes, comptes, tickets, entretiens et traces du poste, rapprochés du trafic. |
| Usage non autorisé d’un accès légitime | Droits, sessions, autorisations, identité des utilisateurs et actions réellement enregistrées. |
| Compromission de MAINT-01 ou d’un compte | Éléments techniques du poste et de l’authentification ; accès disponible ou compte partagé seuls insuffisants. |
| Autre origine ou cause contributive | Exhaustivité des captures, autres chemins, mesures indépendantes et diagnostic frigorifique. |

**À proposer conjointement, pas exécuté ici :** préserver immédiatement les sources reçues, organiser la surveillance locale et l’évaluation des lots, puis examiner la suspension ciblée des seuls accès/écritures non nécessaires. Avant de changer une règle, vérifier le chemin de consultation, l’accès de maintenance indispensable à l’urgence et le retour arrière. Ne pas couper l’alimentation de REG-02, vider les règles ou réinitialiser la VM pour « commencer proprement ».

Le jumeau numérique permettra des reproductions séparées, à documenter avec état initial, manipulation, attentes et observations. Une reproduction plausible ne prouvera pas à elle seule le déroulement exact de l’incident du scénario.

## Production attendue et état final de cet atelier

- Inventaire des sept fichiers et de leurs limites, originaux conservés et empreintes de la copie reçue.
- Enjeux OT/IT/produits/traçabilité associés aux exigences du manuel.
- Liste des vérifications et questions aux intervenants, avec faits, déclarations et hypothèses séparés.
- Horloges et adresses distinguées de celles du PoC ; PCAP à analyser, aucune attribution humaine ni exploitation de vulnérabilité affirmée.
- Aucune modification du laboratoire ni de la production ; poursuite de l’investigation sur copies et en coordination avec le formateur.

[Retour à l’itération 4](index.md) · [Manuel MAN-OT-01](../it-2/MAN-OT-01_Manuel_exploitation_installation_frigorifique.md) · [Dossier J4](../it-3/documenter-protections-limites.md).
