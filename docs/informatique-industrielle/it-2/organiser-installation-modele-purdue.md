# 3.3 — Atelier 3 | Organiser l’installation avec le modèle Purdue

## 🎯 Objectif et modalités

Utiliser le modèle Purdue pour représenter les niveaux d’une infrastructure industrielle et identifier les communications entre IT et OT.

- **Modalité :** recherche documentaire et réalisation d’un schéma en autonomie, individuellement ou en binôme.
- **Durée :** à compléter ; non précisée dans la consigne.
- **Supports :** manuel Montval MAN-OT-01 et ressources d’architecture industrielle.

Le formateur n’est pas présent sur cette séance. S’appuyer sur les ressources et l’entraide du groupe ; conserver le schéma pour le débrief de l’après-midi.

!!! info "Deux statuts sur le même schéma"
    Les composants Montval et leurs fonctions proviennent du manuel. **La DMZ industrielle, le bastion, le point d’accès distant et les contrôles de filtrage sont proposés**, à la demande de l’apprenant, pour représenter une cible d’entreprise. Leur présence dans le dessin ne démontre pas leur déploiement. Les protocoles non documentés restent à confirmer.

## 1 — Comprendre les niveaux Purdue

Purdue organise les fonctions industrielles et celles de l’entreprise. Le repérage suivant est cohérent avec le [guide d’architecture industrielle Cisco, chapitre 2](https://www.cisco.com/c/dam/en/us/td/docs/Technology/Industrial-Security-3-1-DG.pdf). La DMZ, fréquemment notée **3.5**, est une zone intermédiaire ajoutée dans les architectures de sécurité ; les niveaux restent des repères fonctionnels.

| Niveau | Rôle | Application à Montval et justification |
| --- | --- | --- |
| **0 — Processus physique** | Procédé, mesures et action physique. | Enceintes ZF-01 à ZF-03, sondes, contacts de porte et groupes frigorifiques. Les capteurs/actionneurs sont regroupés ici avec le terrain. |
| **1 — Contrôle** | Exécution de la logique locale et commande. | REG-01 à REG-03 : hystérésis, consignes conservées localement et commande des compresseurs. |
| **2 — Supervision et conduite** | Présentation des états, conduite et alarmes. | OPS-01 et fonction de supervision de SUP-01. La supervision consulte les régulateurs, sans exécuter la boucle de régulation. |
| **3 — Opérations industrielles du site** | Fonctions de suivi et services d’exploitation à l’échelle du site. | Historisation des trois zones assurée par SUP-01. Il s’agit d’une fonction logique portée par le **même serveur**, pas d’un second historian identifié. |
| **3.5 — DMZ industrielle proposée** | Médiation des échanges entre entreprise/extérieur et OT. | Point d’entrée distant et bastion proposés, avec filtrage aux frontières. Aucun de ces actifs n’est identifié comme présent par le manuel. |
| **4 — Informatique de l’entreprise** | Systèmes métier et informatique générale du site. | EXP-IT ; un poste d’administration IT peut y être situé dans la cible, mais son identité et son implantation restent inconnues. |
| **5 / extérieur** | Réseau d’entreprise étendu et connexions extérieures, selon la représentation retenue. | FrigoMaint et MAINT-01 sont représentés **hors du périmètre OT du magasin**. Le niveau 5 sert de repère graphique ; le prestataire n’est pas un service interne de Montval. |

Un même actif peut porter plusieurs fonctions. Le placement dépend donc de son rôle et du déploiement réel ; il ne suffit pas d’écrire « serveur » pour choisir un niveau. Purdue n’impose pas un VLAN par niveau ni une relation unique entre niveau fonctionnel et zone de sécurité. Les zones et flux devront être justifiés selon les dépendances, les risques et les capacités des équipements.

## 2 — Schéma fonctionnel et cible d’entreprise

![Montval : niveaux Purdue, trois zones frigorifiques, supervision et cible DMZ/bastion](../../assets/files/informatique-industrielle/it-2/Montval-Purdue-cible.svg)

[Ouvrir le schéma SVG](../../assets/files/informatique-industrielle/it-2/Montval-Purdue-cible.svg) · [Modifier dans draw.io](../../assets/files/informatique-industrielle/it-2/Montval-Purdue-cible.drawio)

**Lecture :** les traits pleins représentent les besoins fonctionnels documentés, avec protocoles inconnus signalés ; les pointillés représentent des chemins proposés. Les flèches réseau désignent la demande du client vers le service, les réponses sont implicites. Les liaisons terrain F0 regroupent mesures remontantes et commandes descendantes ; leur technique n’est pas documentée.

**SUP-01 reste un serveur unique au niveau 2**, avec une fonction d’historisation rattachée logiquement au niveau 3. Il n’y a pas de serveur ajouté pour remplir chaque niveau. Le diagramme ne constitue pas un câblage ni une configuration de filtrage prête à appliquer.

### Chemins proposés via DMZ et bastion

1. **FrigoMaint / MAINT-01 → point d’entrée distant sécurisé → bastion en DMZ.** Identité vérifiée, ouverture liée à une intervention autorisée, session tracée ; mécanismes exacts à choisir.
2. **Bastion → cibles OT explicitement autorisées.** Accès de diagnostic et, si nécessaire, modifications de consigne selon l’autorisation ; accès aux trois REG seulement si le périmètre de l’intervention le justifie. Le dessin illustre le départ vers REG-03, mais les trois régulateurs sont des cibles possibles de règles séparées.
3. **Administration IT → bastion → SUP-01.** Chemin proposé pour administrer le serveur, avec droits et protocole à confirmer. L’accès au bastion ne doit pas conférer à lui seul un droit d’écriture sur tous les équipements.
4. **SUP-01 → régulateurs** pour la collecte courante et **OPS-01 → SUP-01** pour la consultation restent des échanges OT internes ; ils ne sont pas contraints de passer par le bastion de maintenance.

La DMZ est une zone d’intermédiation, le bastion un service d’accès et les pare-feux des contrôles de flux : ces trois fonctions se complètent. Le bastion n’exécute pas la régulation et ne s’insère pas entre sonde et régulateur. Si un équipement n’accepte pas de session interactive, une station ou un outil de maintenance compatible peut être nécessaire derrière le bastion ; cette compatibilité reste à établir. Un tunnel sécurisé protège un segment d’accès, sans rendre automatiquement authentifié ou chiffré le Modbus du dernier segment.

## 3 — Matrice des communications

Le seul protocole industriel explicitement nommé pour Montval est **Modbus TCP** (§2.3). Les adresses, ports configurés et registres détaillés restent à obtenir : ne pas importer les ports 15020/15021 du PoC.

| Flux | Origine → destination / niveaux | Fonction et fréquence | Protocole et statut | Frontière IT/OT et justification |
| --- | --- | --- | --- | --- |
| **F0** | Sondes/contacts ↔ REG ; REG → groupe, N0 ↔ N1. | Mesure et contrôle local continus selon le cycle propre au régulateur. | Interactions documentées (§2.1), liaison électrique/bus et cycle à confirmer. | Terrain OT ; indépendant de SUP-01 et EXP-IT sous les conditions d’EXP-01. |
| **F1** | SUP-01 → REG-01/02/03, N2 ↔ N1. | Collecte périodique températures, consignes, états et alarmes ; rafraîchissement écran nominal souhaité 5 s. | **Modbus TCP documenté** ; table, droits et paramètres réseau à confirmer. | Interne OT dans la cible. EXP-04 et §2.3 ; trafic client et réponses autorisés. |
| **F2** | OPS-01 → SUP-01, N2. | Consultation courante et présentation des alarmes ; acquittement selon les fonctions autorisées. | Interface documentée, protocole **à confirmer** : HTTP/HTTPS non établis par le manuel. | Interne OT si OPS-01 est dédié à la conduite ; s’il est sur le réseau IT, ce flux traverse une frontière et doit être repensé/contrôlé. EXP-04, 08–09. |
| **F3** | Collecte → historique sur SUP-01 ; fonctions N2/N3. | Au moins une température/minute ; événements et acquittements conservés 90 jours. | Fonction documentée ; stockage interne ou composant distinct **à confirmer**. Aucun flux réseau supplémentaire supposé. | Pas de franchissement IT/OT établi pour ce stockage. EXP-05. |
| **F4** | MAINT-01 externe → accès distant/bastion DMZ → supervision ou cible de diagnostic autorisée. | Consultation distante pendant les interventions, y compris urgence autorisée. | Besoin documenté MAI-03–04 ; chemins sécurisés **proposés**, protocoles à confirmer. | Extérieur → DMZ → OT ; aucun accès externe direct aux régulateurs dans la cible. |
| **F5** | Outil autorisé de FrigoMaint, via bastion → REG concernés. | Lecture de diagnostic et modification autorisée de consignes seulement pendant l’intervention. | Variables industrielles exposées en Modbus TCP ; méthode réelle d’écriture et fonctions supportées à confirmer auprès de FrigoMaint. Transport de session et outillage non spécifiés. | Maintenance extérieure → DMZ → OT ; MAI-01–03 et EXP-02. Traçabilité humaine complémentaire nécessaire. |
| **F6** | Poste administrateur, origine IT proposée → bastion → SUP-01. | Administration de la supervision pendant les opérations autorisées. | Besoin d’administration déduit des rôles (§6) ; chemin proposé. Protocole d’administration et système d’exploitation inconnus : ni SSH ni RDP affirmés. | IT → DMZ → OT ; MAI-05–08, ORG-01. |

**Horodatage, sauvegarde et restauration :** EXP-06 et MAI-05 entraînent aussi des besoins de services. Leurs serveurs, protocoles et chemins ne sont pas identifiés ; ils devront faire l’objet de flux supplémentaires justifiés lorsqu’ils seront connus. Ni connexion directe à Internet pour les régulateurs, ni sortie générale de l’OT ne se déduisent du besoin de synchronisation ou de mise à jour.

## 4 — Préparer la discussion : cinq réponses

### 1. Quels échanges doivent être possibles en permanence ?

Les interactions de mesure et de commande **F0** doivent rester disponibles pour le contrôle local. Les lectures périodiques **F1** et la consultation **F2** assurent le service nominal de supervision ; l’historisation **F3** doit tenir sa cadence et sa rétention (**EXP-04–06**). « Disponible en permanence » ne signifie pas connexion TCP permanente ni écriture générale autorisée. Les besoins d’alarme locale doivent rester assurés même sans SUP-01 (**EXP-08**).

### 2. Quels échanges ne sont nécessaires que pendant les interventions ?

Les accès distants **F4**, les écritures de maintenance **F5** et les sessions d’administration **F6** sont liés à des opérations autorisées et tracées (**MAI-01–05**). Un dispositif doit permettre l’urgence avec l’exploitation et l’astreinte (**MAI-04**), sans rendre nécessaire une session permanente du prestataire. Les mécanismes d’ouverture/fermeture restent à concevoir ; un besoin de consultation ne justifie pas des droits d’écriture.

### 3. Quels composants doivent continuer à fonctionner si le réseau IT est indisponible ?

Les **REG-01 à REG-03**, sondes, commandes de groupes et avertissements locaux doivent préserver le service local prévu, si alimentation et équipements restent opérationnels (**EXP-01**, **EXP-08**, §4). L’accès distant ne doit pas être une dépendance de la régulation (**MAI-03**). SUP-01 et OPS-01 pourront continuer leur service interne si leur réseau OT, leur alimentation et leurs dépendances restent disponibles : c’est un objectif de la cible, à vérifier sur la topologie réelle. Aucune panne réseau ne permet de conclure que les températures sont correctes sans contrôle des zones (**EXP-11**).

### 4. Où une zone intermédiaire pourrait-elle être utile ?

Entre l’informatique générale/les accès externes et l’environnement de supervision/contrôle. La **DMZ industrielle proposée** héberge ici le point d’accès distant et le bastion pour médiatiser les sessions de FrigoMaint et l’administration IT. Le filtrage aux deux frontières limite les origines, cibles et services. Elle ne déplace pas les boucles locales hors de l’OT et n’impose pas de faire transiter la collecte courante par le bastion. Un éventuel relais de données ou de mises à jour pourra être étudié si son besoin est établi.

### 5. Que manque-t-il pour déployer cette architecture ?

Il faut le plan d’adressage et la topologie réels, les dépendances d’alimentation et de services, les notices et registres Modbus, les capacités de filtrage et d’authentification, la configuration SUP/OPS/MAINT, les protocoles de consultation et d’administration, les mécanismes d’accès distant et leur compatibilité. Ajouter responsabilités, astreinte, sauvegardes, restauration, disponibilité requise des accès et conditions de recette (§8). Ces éléments permettent de choisir équipements, zones de sécurité, règles et contrôles ; leur absence du manuel n’établit pas leur absence dans l’installation.

## Production et limites

Schéma annoté, source draw.io et matrice F0–F6 disponibles pour le débrief. Analyse documentaire et proposition d’architecture réalisées ; aucune segmentation, règle de pare-feu, session bastion ni mesure de disponibilité n’est déployée ou testée dans cet atelier. L’accord collectif reste à recueillir.

## Ressources

- [MAN-OT-01, v1.0 du 14 octobre 2022](MAN-OT-01_Manuel_exploitation_installation_frigorifique.md), §2–6 et §8.
- [Cisco — Industrial Security 3.1 Design Guide, chapitre 2](https://www.cisco.com/c/dam/en/us/td/docs/Technology/Industrial-Security-3-1-DG.pdf) : niveaux et zone intermédiaire dans l’architecture de référence.
- [Cisco — Industrial Automation, section Industrial DMZ](https://www.cisco.com/c/en/us/td/docs/solutions/Verticals/Industrial_Automation/IA_Horizontal/DG/Industrial-AutomationDG/Industrial-AutomationDG.html) : médiation entre zones entreprise et industrielle ; la DMZ est un ajout à la représentation Purdue.
- [ANSSI — Cybersécurité des systèmes industriels : méthode de classification](https://messervices.cyber.gouv.fr/guides/la-cybersecurite-des-systemes-industriels) : ressource de cybersécurité fournie, distincte du manuel Montval.
- [3.1 — Exigences d’exploitation](analyser-exigences-exploitation-ot.md) · [3.2 — Besoins IT](traduire-exigences-ot-besoins-informatiques.md).

[Retour à l’itération 2](index.md) · [Pense-bête](../../pense-bete/glossaire/informatique-industrielle/it-2.md)
