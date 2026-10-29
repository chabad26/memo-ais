# 4.2 — Atelier 2 | Définir les accès et les règles de pare-feu

## 🎯 Objectif et modalités

Traduire les besoins de communication de Montval en une politique de filtrage réseau.

**Modalité :** atelier de conception en binôme avec le formateur. **Durée :** à compléter, non précisée.

!!! info "Statut de la politique"
    Politique **proposée**, issue du manuel MAN-OT-01 et de l’architecture 4.1. Les alias sont fonctionnels, pas des IP inventées. Le **TCP 502** est fourni par la consigne 4.2 pour SUP → REG ; les autres ports proposés sont des hypothèses identifiées. Aucune règle n’est chargée, aucun accès ni refus n’est testé dans cette fiche. Les conditions non confirmées empêchent l’activation de la règle correspondante.

!!! note "Complément du 4.3 — REG-02 obsolète"
    La nouvelle contrainte retire REG-02 des accès directs R10 et R22. Q00–Q02 passent avant l’acceptation des sessions établies ; Q10–Q13 imposent le chemin par GW-02 proposé. La liste CSV est mise à jour (32 règles). [Voir les limites et hypothèses H8–H10 du 4.3](proteger-regulateur-industriel-obsolete.md). Les permissions REG-01/03 ne justifient aucun contournement vers REG-02.

## 1 — Définir les zones de sécurité

| Zone / alias | Contenu proposé | Frontière et justification |
| --- | --- | --- |
| **IT** | STOCK-01, ORDER-01, IT-ADMIN, BACKUP-01. | L’informatique de gestion ne commande pas les REG. Distinguer aussi les rôles métier, administration et sauvegarde ; un réseau IT unique ne suffit pas à filtrer les échanges locaux. |
| **OT-SUP** | SUP-01, OPS-01. | Collecte, conduite, alarmes et historique ; préserver la fraîcheur des données et la reprise sans écrasement des consignes (**EXP-04–06, EXP-10**). |
| **OT-CTRL** | REG-01 à REG-03, liaisons locales, groupes et avertissements. | Préserver les boucles locales (**EXP-01–03, EXP-08**). Le pare-feu ne doit pas être introduit dans une liaison terrain non identifiée. |
| **OT-SERV** | Services OT proposés en J3, dont référence de temps si compatible. | Service utile à l’exploitation distinct de la commande. Identifier clients et dépendances avant de créer un flux ; pas de dépendance de régulation au réseau IT ajoutée. |
| **DMZ** | RELAIS-DONNÉES, DÉPÔT-OT, point d’entrée distant et BASTION proposés. | Médiation de la publication, des copies et de la maintenance. Fonctions et droits distincts ; pas de confiance générale entre toutes les machines DMZ. Filtrage interne/hôte ou sous-zones si nécessaire. |
| **Maintenance** | MAINT-01 et session FrigoMaint, puis outil autorisé du bastion. | Rôle et chemin dédiés, droits bornés à l’intervention (**MAI-01–04**). Cette zone logique ne crée pas un accès direct au contrôle. |
| **Externe commercial** | SUPPLIER-01, destinations exactes à définir. | Commandes/confirmations avec ORDER, sans droit OT. Ne pas confondre fournisseur commercial et mainteneur frigorifique. |

Les frontières principales sont **IT/DMZ**, **DMZ/OT**, **OT-SUP/OT-CTRL** et **IT/extérieur**. Choisir les points réels de contrôle après inventaire : une règle sur un routeur ne voit pas nécessairement un trafic entre hôtes du même réseau. Une séparation logique, une ACL ou un filtrage hôte/bridge pourra être nécessaire selon le déploiement ; le choix reste à justifier.

## 2 — Poser les hypothèses de services

| Code | Hypothèse ou donnée | Conséquence avant déploiement |
| --- | --- | --- |
| **D1** | **Modbus TCP / 502 fourni par la consigne 4.2** pour SUP → REG. | Vérifier les ports et interfaces réellement configurés ; aucune transposition des 15020/15021 du PoC. |
| **H1** | Interfaces métier et publication du relais proposées en **HTTPS sur TCP 443**. | Confirmer API, mode client/serveur, authentification, droits, certificats et destinations ; 443 n’est pas une preuve du support HTTPS. |
| **H2** | Interface OPS → SUP proposée en **HTTPS sur TCP 443**. | Ni HTTP ni HTTPS n’étaient documentés par le manuel ; vérifier la supervision avant activation. |
| **H3** | Administration : symboles **P_ADMIN_IT** et **P_ADMIN_SUP**, protocoles/ports inconnus. | Inactifs tant que l’OS, l’outil et les services réels ne sont pas connus. Ne pas remplacer par tous les ports ni supposer SSH/RDP. |
| **H4** | BACKUP tire les données IT ; **P_BACKUP_IT** et protocole à confirmer. | Confirmer support, cohérence, initiateur et compte. Si mode poussé retenu, modifier la matrice plutôt qu’autoriser les deux sens. |
| **H5** | Export SUP → DÉPÔT-OT et lecture BACKUP → DÉPÔT-OT proposés en **HTTPS / TCP 443**. | Valider cette interface et séparer publication, lecture et restauration. Le dépôt n’est pas le relais de STOCK. |
| **H6** | Point d’entrée distant proposé sur **TCP 443**, puis **P_SESSION** vers bastion à confirmer. | Le port ne définit pas à lui seul un VPN ni une authentification. Confirmer le produit/protocole choisi et les sessions ; pas de flux réseau supplémentaire si fonctions réunies dans le même service. |
| **H7** | Service de temps OT proposé en **NTP / UDP 123** pour clients compatibles. | Vérifier support, précision et origine des horodatages. Aucun flux REG → temps ni sortie Internet générale ajouté sans besoin établi. |

Toutes les valeurs H sont des **choix de conception à confirmer**, et non des services constatés. Pour chaque alias, relever les IP et interfaces réelles, y compris IPv6 si présent. Un nom de portail n’est pas automatiquement une règle de pare-feu valide : résoudre/maintenir ses destinations selon les capacités de la solution et le contrat fournisseur.

## 3 — Matrice des flux et autorisations

Les conditions et droits de la [matrice 4.1](integrer-services-informatiques-magasin.md#2-analyser-les-besoins-et-les-initiateurs) restent applicables. Ici, chaque ligne prépare sa traduction réseau.

| Source | Destination | Protocole / port | Fonction et droits | Autorisation proposée | Justification |
| --- | --- | --- | --- | --- | --- |
| SUP-01 | REG-01 et REG-03 ; REG-02 via GW-02-LECT depuis 4.3 | TCP / 502, D1 ; H8 sur passerelle. | Collecte en **consultation**. | Autoriser le transport, **lecture seule à garantir séparément**. | Supervision, EXP-04, EXP-08. |
| SUP-01 | RELAIS-DONNÉES DMZ | TCP / 443, H1. | Publication métier ; écriture des données sur le relais, pas commande REG. | Sous réserve H1, rôle de publication limité. | Exposer les informations de conservation sans ouvrir le contrôle. |
| STOCK-01 | RELAIS-DONNÉES DMZ | TCP / 443, H1. | **Lecture** des données de conservation. | Sous réserve H1, lecture seulement ; refuser STOCK → REG. | Suivi des lots ; fraîcheur/horodatage à conserver. |
| ORDER-01 | STOCK-01 | TCP / 443, H1. | Consultation des stocks. | Sous réserve H1, rôle de lecture nécessaire. | Réapprovisionnement. |
| ORDER-01 | SUPPLIER-01 | TCP / 443, H1. | **Transactions commerciales** : commandes/confirmations. | Sous réserve H1 ; destinations du portail uniquement. | Gestion commerciale, sans droit OT. |
| OPS-01 | SUP-01 | TCP / 443, H2. | Lecture et acquittement selon rôle ; aucun changement de consigne courant. | Sous réserve H2 ; droits applicatifs distincts. | EXP-04, EXP-09. |
| MAINT-01 | REG-01/03 via entrée/bastion ; **REG-02 via GW-02-MAINT** | Entrée TCP 443 H6 ; P_SESSION ; dernier segment Modbus TCP 502 si utilisé. | Diagnostic, puis **modification autorisée** selon outil et tâche. | Pas de direct ; sessions temporaires, cibles/actes autorisés et tracés. | MAI-01–04, EXP-02. |
| IT-ADMIN | REG-01 à REG-03 | Tous ports. | Administration demandée mais besoin non établi pour ce rôle. | **Refuser en direct** ; ne pas assimiler administration IT et maintenance frigorifique. | Pas de besoin justifié par le manuel ; voie FrigoMaint si intervention requise. |
| IT-ADMIN | BASTION puis SUP-01 | P_SESSION, P_ADMIN_SUP, H3/H6. | Administration autorisée de SUP. | Inactif tant que protocoles inconnus ; activation limitée à l’intervention. | MAI-05–08, ORG-01. |
| IT-ADMIN | STOCK, ORDER, BACKUP | P_ADMIN_IT, H3. | Administration IT, modification possible. | Cibles/rôles nommés et opérations autorisées ; pas extension à l’OT. | Exploitation des services informatiques. |
| BACKUP-01 | Sources STOCK/ORDER | P_BACKUP_IT, H4. | Lecture de sauvegarde ; écritures dans son propre dépôt. | Mode et ports à confirmer ; droits spécifiques, pas administration générale. | Continuité des services. |
| SUP-01 puis BACKUP-01 | DÉPÔT-OT, en deux sessions distinctes | TCP / 443, H5. | SUP publie une copie ; BACKUP la lit. | Droits de publication et collecte distincts ; aucun accès BACKUP → REG. | Sauvegarde OT sans commande métier directe. |
| SUP-01, OPS-01 compatibles | S-TEMPS | UDP / 123, H7. | Synchronisation technique de l’heure. | Clients et référence limités ; support à valider. | EXP-06. |
| Autres origines / flux | Frontières IT/OT concernées | Tous protocoles / ports non autorisés. | Aucun besoin établi. | **Refuser par défaut** ; traces utiles et limitées en débit. | Réduire les chemins inutiles ou non justifiés. |

**Historisation :** C03 reste une fonction de SUP-01 ; ne pas inventer une ouverture réseau de base de données pour remplir une matrice. **Restauration et mises à jour :** chemins exceptionnels à préciser et autoriser séparément après préparation ; les lignes de sauvegarde ne donnent pas automatiquement un droit de restauration. Les services d’identité, de noms ou de journaux réellement nécessaires seront ajoutés une fois leurs besoins documentés, sans règle générale de commodité.

## 4 — Liste ordonnée des règles de pare-feu

[Télécharger la liste des règles — CSV](../../assets/files/informatique-industrielle/it-3/Montval-4.2-regles-filtrage-proposees.csv)

Les zones et hôtes remplacent les adresses tant que le plan réel est inconnu. **Ce tableau est une politique de conception, pas un fichier nftables exécutable.** Chaque autorisation vaut pour les seules sources/destinations nommées et reste soumise à ses prérequis. Les autorisations d’ouverture portent sur les nouvelles connexions ; R05 traite ensuite leur poursuite et leur retour.

### Règles préalables et suivi des connexions

| Règle | Source → destination | Protocole / port | Action | Justification / activation |
| --- | --- | --- | --- | --- |
| **R00** | Toutes zones traversantes → Toutes zones traversantes | Tous ; ct state invalid | **REFUSER** | Paquets invalides ; filtrage cohérent. Permanent ; politique proposée. |
| **R01** | IT dont IT-ADMIN, STOCK, ORDER, BACKUP ; extérieur dont MAINT direct → REG-01 à REG-03 / contrôle OT | Tous protocoles / ports | **REFUSER** | Pas de commande directe depuis IT ou extérieur. Tous états ; avant acceptation established. |
| **R02** | DMZ : RELAIS-DONNÉES, DÉPÔT-OT et autres sources sauf BASTION autorisé → REG-01 à REG-03 | Tous protocoles / ports | **REFUSER** | Empêcher le pivot par relais métier ou dépôt. Tous états ; BASTION soumis à R04 et R22. |
| **R03** | Extérieur : fournisseurs et mainteneur → SUP-01 et OPS-01 | Tous protocoles / ports | **REFUSER** | Pas de publication directe de la supervision. Tous états ; accès de maintenance via DMZ seulement. |
| **R04** | Origines des flux temporaires A/M : IT-ADMIN, MAINT-01, accès distant, BASTION → Cibles de leurs règles temporaires | Tous protocoles / ports pour les tuples expirés ou révoqués | **REFUSER** | Une ancienne session ne doit pas prolonger une autorisation retirée. Contrôle de validité avant R05 ; par périmètre/source/cible, pas une coupure générale. |
| **Q00** | Toute source sauf interface aval autorisée de GW-02 → REG-02 | Tous protocoles / ports | **REFUSER** | REG-02 accessible uniquement par la passerelle contrôlée. Tous états ; avant established ; supprime le direct SUP et BASTION vers REG-02. |
| **Q01** | Sources des accès temporaires à GW-02 → GW-02-MAINT et administration GW-02 | P_MAINT_02 / P_ADMIN_GW02 ; flux expirés ou révoqués | **REFUSER** | Ne pas laisser persister une session de maintenance retirée. Vérifier autorisation avant established ; fermer sessions et droits de façon ciblée. |
| **Q02** | Origines non autorisées pour chaque point d’entrée GW-02 → GW-02-LECT, GW-02-MAINT et administration | Tous protocoles / ports | **REFUSER** | Éviter le passage de SUP du rôle lecture vers le rôle écriture. GW-LECT : SUP-01 seul ; MAINT/admin : outil BASTION autorisé seulement, aux ports définis ; tous états. |
| **R05** | Extrémités d’un flux répertorié autorisé → Extrémité correspondante / réponse | Même connexion ; ct state established | **AUTORISER** | Poursuite et retour des seules sessions encore permises. Chemins/tuples encore autorisés ; refus R01–R04 et Q00–Q02 prioritaires ; Q01 pour révocation REG-02. |
| **R06** | Équipements participant aux échanges permis → Extrémités concernées | ICMP/ICMPv6 nécessaires, ct state related ; types à préciser | **AUTORISER SOUS CONDITION** | Erreurs réseau et fonctionnement des communications permises. Périmètre qualifié ; pas de helper ouvrant implicitement des services applicatifs. |

### Collecte et protection particulière de REG-02

| Règle | Source → destination | Protocole / port | Action | Justification / activation |
| --- | --- | --- | --- | --- |
| **R10** | OT-SUP : SUP-01 → OT-CTRL : REG-01 et REG-03 seulement | TCP / 502 (consigne 4.2) | **AUTORISER** | Collecte courante de températures, états et alarmes. REG-02 exclu : Q10/Q11 via GW-02 le remplacent ; lecture seule à garantir séparément pour REG-01/03. |
| **Q10** | OT-SUP : SUP-01 → OT-PROTECTION : GW-02-LECT | TCP / 502 (H8 : écoute de passerelle proposée) | **AUTORISER SOUS CONDITION** | Consultation des données REG-02 par un endpoint sans écriture. Pas d’accès direct ; fonctions et plages de lecture utiles qualifiées ; aucune écriture via ce rôle. |
| **Q11** | Interface aval GW-02 → REG-02 | TCP / 502 (consigne 4.2, configuration à vérifier) | **AUTORISER SOUS CONDITION** | Transport des opérations validées par GW-02. Seule source réseau admise ; la règle IP ne distingue pas lectures/écritures ; politique applicative indispensable. |
| **Q12** | Station ou outil autorisé via BASTION → GW-02-MAINT | P_MAINT_02 / protocole à confirmer (H9) | **AUTORISER SOUS CONDITION** | Diagnostic ou écritures spécifiquement accordées par intervention. Inactive sans protocole/outillage qualifiés ; cibles/fonctions/registres/valeurs et durée bornés ; traces puis révocation. |
| **Q13** | Station d’administration autorisée via BASTION → Administration de GW-02 | P_ADMIN_GW02 / protocole à confirmer (H10) | **AUTORISER SOUS CONDITION** | Administrer le dispositif de protection sans ouvrir son rôle industriel. Inactive sans protocole qualifié ; identité et changement autorisés ; sauvegarde de sa politique. |
| **Q90** | Sources ou services non couverts par Q10/Q12/Q13 → GW-02 | Tous protocoles / ports restants | **REFUSER** | Refus par défaut des autres services de passerelle. Après les seules autorisations valides ; journalisation limitée et compteur. |

### Services, maintenance générale et refus final

| Règle | Source → destination | Protocole / port | Action | Justification / activation |
| --- | --- | --- | --- | --- |
| **R11** | OT-SUP : SUP-01 → DMZ : RELAIS-DONNÉES | TCP / 443 (H1) | **AUTORISER SOUS CONDITION** | Publication de données de conservation B01. H1 validée ; compte de publication limité ; pas de commandes REG. |
| **R12** | IT : STOCK-01 → DMZ : RELAIS-DONNÉES | TCP / 443 (H1) | **AUTORISER SOUS CONDITION** | Lecture des seules données métier B02. H1 validée ; rôle lecture ; pas d’accès aux sauvegardes ni au bastion. |
| **R13** | IT : ORDER-01 → IT : STOCK-01 | TCP / 443 (H1) | **AUTORISER SOUS CONDITION** | Consultation des stocks B03. H1 validée ; si même réseau, filtrage hôte ou séparation rendant le flux contrôlable. |
| **R14** | IT : ORDER-01 → Externe commercial : SUPPLIER-01 | TCP / 443 (H1) | **AUTORISER SOUS CONDITION** | Commandes et confirmations B04. H1 validée ; destinations du portail délimitées ; réponses R05, pas nouvelle session entrante générale. |
| **R15** | OT-SUP : OPS-01 → OT-SUP : SUP-01 | TCP / 443 (H2) | **AUTORISER SOUS CONDITION** | Vue opérateur et acquittements autorisés. H2 validée ; droits applicatifs distincts des écritures de consigne. |
| **R16** | IT : IT-ADMIN → IT : STOCK-01, ORDER-01, BACKUP-01 selon rôle | P_ADMIN_IT / protocole à confirmer (H3) | **AUTORISER SOUS CONDITION** | Administration IT. Inactive tant que protocole inconnu ; activation sur changement autorisé ; pas extension aux REG. |
| **R17** | IT : BACKUP-01 → IT : sources STOCK-01, ORDER-01 prévues | P_BACKUP_IT / protocole à confirmer (H4) | **AUTORISER SOUS CONDITION** | Collecte des sauvegardes IT S00. Mode tiré à valider ; compte de sauvegarde limité ; fenêtre et charge maîtrisées. |
| **R18** | OT-SUP : SUP-01 → DMZ : DÉPÔT-OT | TCP / 443 (H5) | **AUTORISER SOUS CONDITION** | Publication de copies OT S01. H5 validée ; mode poussé ; compte dédié ; pas d’alias commun avec relais métier. |
| **R19** | IT : BACKUP-01 → DMZ : DÉPÔT-OT | TCP / 443 (H5) | **AUTORISER SOUS CONDITION** | Récupération des copies OT S02. H5 validée ; lecture du dépôt ; ne donne aucun accès BACKUP vers les REG. |
| **R20** | Externe maintenance : MAINT-01 via point d’accès défini → DMZ : service d’entrée distant | TCP / 443 (H6) | **AUTORISER SOUS CONDITION** | Entrée FrigoMaint M01. H6 et provenance validées ; identité, intervention autorisée, expiration et traces. |
| **R21** | Session distante relayée ; IT-ADMIN autorisé → DMZ : service BASTION | P_SESSION / protocole à confirmer (H6) | **AUTORISER SOUS CONDITION** | Ouverture de session vers les cibles accordées. Pas d’autorisation tant que protocole indéfini ; si entrée et bastion même service, pas de flux réseau inventé. |
| **R22** | DMZ : station ou outil de maintenance du BASTION → OT-CTRL : REG-01 et REG-03 concernés seulement | TCP / 502 pour diagnostic Modbus ; autres ports non ouverts | **AUTORISER SOUS CONDITION** | Diagnostic et opérations Modbus autorisées M02. REG-02 exclu : Q12 puis Q11 ; intervention autorisée pour REG-01/03, contrôles applicatifs requis. |
| **R23** | DMZ : station d’administration du BASTION → OT-SUP : SUP-01 | P_ADMIN_SUP / protocole à confirmer (H3) | **AUTORISER SOUS CONDITION** | Administration de la supervision A02. Inactive tant que protocole inconnu ; changement autorisé ; aucune modification implicite des consignes. |
| **R24** | OT : SUP-01, OPS-01 si compatibles → OT-SERV : S-TEMPS proposé | UDP / 123 (H7) | **AUTORISER SOUS CONDITION** | Cohérence temporelle EXP-06. H7 validée ; clients nommés et référence unique prévue ; pas de service entrant depuis Internet. |
| **R90** | Hôtes et zones non couverts par une autorisation valide → Autres zones / services non autorisés | Tous protocoles / ports restants | **REFUSER** | Refus explicite et observation des écarts. Journalisation limitée en débit ; compteur ; le refus continue même si les logs sont limités. |
| **R99** | Toutes origines sur les frontières couvertes → Toutes destinations non acceptées | Tous protocoles / ports restants | **REFUSER PAR DÉFAUT** | Aucune ouverture implicite. Policy drop des chaînes de filtrage concernées ; couverture IPv4/IPv6 et autres chemins vérifiée. |

### Ordre, sessions existantes et révocation

La [documentation nftables sur conntrack](https://wiki.nftables.org/wiki-nftables/index.php/Matching_connection_tracking_stateful_metainformation) explique les états `new`, `established`, `related` et `invalid`, ainsi que les tuples d’origine et de réponse. Le suivi de connexion ne prouve ni identité humaine ni autorisation métier.

- Évaluer les refus explicites et la validité des accès temporaires **avant** une acceptation des connexions établies. Une règle globale `ct state established,related accept` en tête pourrait préserver une session devenue interdite.
- **R05** doit rester bornée aux services/chemins permis, en tenant compte du sens origine/réponse. Une ancienne connexion présente dans conntrack ne doit pas être automatiquement autorisée lors du durcissement initial.
- À la fin d’une maintenance, fermer les nouvelles ouvertures **et** empêcher la poursuite des sessions devenues non autorisées : contrôle de validité par chemin, fermeture au bastion, retrait des droits et, si nécessaire, traitement ciblé des entrées conntrack correspondantes. La méthode exacte dépend du déploiement et doit être testée.
- Ne pas vider tout conntrack pour fermer une intervention : cela peut couper les communications de supervision. Cibler la session/cible concernée et vérifier que la collecte normale continue.
- Pour `related`, limiter aux besoins effectivement identifiés, par exemple des erreurs réseau nécessaires. Ne pas activer de helpers ou de services associés arbitraires sous prétexte de cette catégorie.

Les règles R90/R99 prévoient un refus final ; la limitation des journaux ne doit pas limiter le refus lui-même. Compteurs et journaux limités servent à observer les écarts sans perturber les ressources du laboratoire.

## 5 — Traduction nftables : emplacement et limites

La [documentation officielle des chaînes](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains) distingue les hooks `input` (trafic destiné à l’hôte), `output` (émis par l’hôte) et `forward` (trafic traversant). Elle précise la politique de chaîne et l’effet des autres chaînes attachées au même hook.

| Déploiement | Conséquence pour la politique |
| --- | --- |
| Pare-feu routant entre réseaux distincts | Le filtrage interzones relève principalement de `forward` ; définir aussi la protection du pare-feu lui-même et son administration autorisée. |
| Services sur une seule machine | `input`/`output` et les interfaces réellement traversées peuvent être concernés ; un `forward` ne contrôle pas automatiquement les échanges locaux. |
| Hôtes dans un même segment / bridge | Vérifier le passage effectif par le contrôle choisi ; un routeur absent du chemin ne peut pas appliquer sa règle à ce trafic. |
| Laboratoire Python sur 127.0.0.1 | Le serveur et la passerelle utilisent la boucle locale, pas une séparation physique IT/OT. Traduire le scénario selon les consignes de laboratoire, sans prétendre qu’une chaîne `forward` isole des processus locaux. |
| IPv4 et IPv6 | Couvrir les familles et chemins réellement présents. La famille `inet` peut traiter les deux, mais des règles d’adresses et services adaptées restent nécessaires ; ne pas laisser un chemin alternatif non contrôlé. |

Aucune règle système ni commande de chargement n’est exécutée ici. Avant mise en œuvre partielle : relever interfaces/IP/routage, règles déjà présentes, accès d’administration utile, conditions de retour arrière et scénario d’essai convenu. Éviter qu’une autre chaîne, un bridge, un chemin NAT ou une ouverture existante contredise la politique prévue.

### Autoriser TCP 502 ne signifie pas « lecture seule »

Un filtrage réseau sur TCP 502 permet le transport Modbus ; il ne distingue pas à lui seul les fonctions de lecture et d’écriture ni l’intervenant humain. Les droits de **consultation** de R10 doivent être assurés par des capacités réelles : équipement, outil, relais applicatif ou pare-feu disposant d’un contrôle adapté, à confirmer.

Dans le PoC, `lab/gateway.py` n’autorise que les fonctions **01–04** et rejette les autres, mais le serveur direct reste accessible tant qu’aucun contrôle de chemin ne l’empêche. Ce relais pédagogique n’est pas une segmentation réseau ni un équipement de sécurité industriel qualifié. Si SUP et un outil d’écriture partagent une même origine réseau, leur adresse seule peut ne pas permettre de les distinguer : définir un point de contrôle compatible plutôt que prétendre que R10 les sépare.

## 6 — Vérifier les règles et les modes dégradés

Pour chaque ligne R : confirmer besoin et initiateur, vérifier qu’aucune source/destination superflue n’est couverte, distinguer permanent/périodique/temporaire, examiner le chemin vers les REG, puis documenter l’effet d’indisponibilité du service. Les essais ci-dessous sont **proposés**, pas réalisés.

| Règles / cas | Résultat attendu à vérifier | Limite / précaution d’exploitation |
| --- | --- | --- |
| R10 / Q10–Q11 : lectures SUP → REG ou GW selon cible | Mesures et alarmes restent consultables ; un dispositif distinct bloque les écritures non autorisées. | Pas de modification perturbatrice pour tester en réel. Vérifier péremption et avertissements locaux ; TCP autorisé seul ne démontre pas le blocage applicatif. |
| R11–R12 : publication/lecture STOCK | STOCK lit les données publiées, horodatage et qualité compris, sans atteindre les REG ni lire le dépôt de sauvegarde. | Arrêt du relais = données métier absentes/périmées, pas arrêt local ; vérifier que SUP ne se bloque pas en publiant. |
| R13–R14 : stock/commandes | ORDER consulte les stocks et échange avec le portail ; nouvelle connexion fournisseur non demandée refusée. | Panne de portail : retard commercial, pas droit de contourner vers l’OT ; reprise sans doublons à confirmer. |
| R15 : conduite | OPS affiche les valeurs courantes et permet le seul acquittement autorisé. | Panne SUP : contrôle local attendu, mais visibilité/historique dégradés ; recette de reprise sans changement de consigne. |
| R16–R19 : administration/sauvegarde | Seuls rôles/sources et dépôts prévus sont accessibles ; sauvegarde cohérente et récupération vérifiées séparément. | Planifier charge et opérations ; une sauvegarde qui réussit n’atteste pas à elle seule une restauration réussie. |
| R20–R23, R04–R05 : intervention | Accès sur autorisation, cibles utiles seulement ; après révocation, **nouvelle connexion et session existante** refusées/fermées selon le mécanisme ; collecte normale préservée. | Rôle lecture puis écriture explicitement accordé ; prévoir urgence/astreinte sans accès général permanent. |
| R24 : temps | Seuls clients et référence prévus sont accessibles. | Perte de référence : cohérence des événements à surveiller, pas nouvelle dépendance du contrôle local. |
| R01–R03, R90–R99 : chemins interdits | IT-ADMIN, STOCK, ORDER, BACKUP, fournisseur et MAINT direct n’atteignent pas les commandes REG ; autres flux non justifiés refusés. | Vérifier chemins IPv4/IPv6, latéraux et sessions préexistantes ; ne pas perturber les liaisons terrain. |

**Preuves à conserver lors de la mise en œuvre :** matrice avec hypothèses levées ou maintenues, règles réellement chargées et points de contrôle, compteurs/traces utiles, captures des flux permis/refusés, contrôle de fermeture de session de maintenance, observations opérateur et écarts. Le succès d’une construction MkDocs ne valide pas la politique réseau ni sa mise en œuvre.

## Production et préparation du laboratoire

Matrice et liste de règles renseignées, refus par défaut et traitement des sessions précisés. À confronter en binôme avec le formateur et à adapter à la topologie du laboratoire avant application partielle l’après-midi. Les adresses et paramètres non confirmés ne doivent pas être remplacés par une ouverture générale.

## Ressources

- [MAN-OT-01](../it-2/MAN-OT-01_Manuel_exploitation_installation_frigorifique.md), notamment EXP-01, EXP-04–06, EXP-10, MAI-01–08 et ORG-01–02.
- [Architecture J3](../it-2/concevoir-architecture-it-ot-montval.md) et [intégration 4.1](integrer-services-informatiques-magasin.md).
- [nftables — documentation officielle](https://wiki.nftables.org/), [chaînes et hooks](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains), [états et métadonnées conntrack](https://wiki.nftables.org/wiki-nftables/index.php/Matching_connection_tracking_stateful_metainformation), [référence rapide des familles/règles](https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes) — consultées le 29 octobre 2026.

[Retour à l’itération 3](index.md) · [Pense-bête](../../pense-bete/glossaire/informatique-industrielle/it-3.md)
