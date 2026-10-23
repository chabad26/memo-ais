# Compte rendu d’incident — Conversation IA et WMS Hexalp

**Olivier HIMBLOT — rédigé avec assistance le 23 octobre 2026**  
Situation étudiée : mardi 13 octobre 2026, après le message de Nadia de 09 h 05. Données fictives ; diffusion de travail limitée. Secrets et coordonnées individuelles caviardés.

## 1. Synthèse et qualification

**Oui, des données clients et personnelles ont été publiées** dans une conversation partagée : le décompte de Hugo porte sur 41 adresses e-mail, neuf clients, 17 adresses de livraison, 12 téléphones et six comptes de service (P3). Ces nombres ne s’additionnent pas pour obtenir un nombre de personnes uniques. Deux secrets sont exposés : mot de passe stats HAProxy et jeton de déploiement (P3/P6).

**Gravité 4, risque critique G4×V4=16 pour l’exposition C3**, conformément à la grille J2 ; exploitation hostile des secrets non établie. Trois volets : confidentialité (publication), intégrité (configuration non versionnée), disponibilité (retrait des backends retardé). L’accès VPN du 08/10 est à investiguer ; **aucun lien causal démontré avec l’exfiltration du 09/10**.

Le rapport s’appuie sur P1–P8, dont P5/P6/P8 reçues en captures. La trame et le tableau annoncés dans la consigne n’étaient pas visibles dans le copier-coller : structure de travail proposée. Les pièces décrivent des constats et collectes, **pas un confinement terminé**.

## 2. Chronologie sourcée

| Moment du scénario | Fait et source |
| --- | --- |
| 24/09, 02:38 et 03:10 | Stats : compte admin, HTTP200 depuis le poste de Julien, attribution de Hugo (P5) |
| 24/09, 02:41–03:24 | Conversation personnelle gratuite ; configuration/logs puis script de déploiement transmis (P3) |
| 24/09, 03:29 puis 03:31 | Lien public créé ; message de forum qui le diffuse (P2/P3) |
| Depuis le 02/10 | Indexation du **forum** rapportée par le CERT, pas preuve d’indexation directe du lien ChatGPT (P1) |
| 08/10, 23:47–23:58 | Depuis 10.20.250.200 :401 initial, puis 200 avec admin et neuf autres 200 ; attribution VPN attendue (P5) |
| 09/10, 03:00 | Exfiltration du scénario J4 ; source 10.20.250.151 dans les données J4. Correspondances VPN officielles demandées (P5/J4) |
| 12/10, 17:48 | CERT signale l’exposition, sans information d’exploitation (P1) |
| 13/10, 08:02 ; 08:15 ; 09:05 | Capture forum ; export avec Julien/Nadia ; incident et main courante annoncés ouverts (P2/P3/message Nadia) |

Heures reprises des pièces, fuseaux et horloges à confirmer. La fiche U2 du J2 avait déjà identifié le secret stats et proposé sa rotation ; aucune preuve que cette mesure ait été exécutée avant l’alerte.

## 3. Ce qui a été transmis

Canal : copier-coller dans le compte personnel gratuit de Julien, puis instantané complet des neuf messages rendu accessible par lien et annoncé sur le forum (P2/P3). Option d’amélioration du modèle activée selon P3 ; cela autorise un usage possible, sans démontrer un entraînement effectif. Le proxy corrobore 3,6 Mo envoyés le 24/09, pas le contenu de chaque octet.

| Élément publié (P3, sauf mention) | Classe PSSI / secret ? | Portée et impact |
| --- | --- | --- |
| Mot de passe stats **[CAVIARDÉ]** | C3, secret | Lecture de la supervision HAProxy ; page sans stats admin selon Hugo. Pas un accès shell ou un droit de modifier la configuration (P5) |
| Jeton déploiement **[CAVIARDÉ]**, svc-deploy | C3, secret | read_registry/write_registry, sans expiration, registre interne/VPN ; script et CI l’utilisent. Risque d’altération d’images, pas preuve de droits sur tous les dépôts GitLab (P6) |
| Configuration de sécurité, IP, ports, backends | Configuration : C3 ; cartographie isolée : C2 ; adresses/noms non secrets d’authentification | Reconnaissance de l’architecture, services et routage |
| Chemin du certificat TLS | C2 proposé, non secret | Révèle un emplacement ; ni certificat complet ni clé privée transmis dans l’extrait |
| Empreinte ED25519 de clé publique | C2 contextuel, non secret | Empreinte publique, pas clé privée ; trace d’authentification, pas de capacité de connexion à elle seule |
| Noms des comptes deploy/svc-deploy et six comptes de service | C2, identifiants non secrets | Facilite ciblage et reconnaissance ; aucun mot de passe de ces six comptes démontré |
| Script deploy_wms.sh hors jeton | C2, code interne | Hôtes, registre et chaîne de déploiement ; le secret qu’il contient relève séparément de C3 |
| Clients, commandes et erreurs applicatives | C2, non secrets d’authentification | Données commerciales et métiers ; lien entre client, livraison et incident |
| Contacts, e-mails, téléphones, livraisons | C2 ; données personnelles au moins pour les contacts | Publication et risques de ciblage ; décompte de Hugo à dédupliquer, adresses de livraison à qualifier |
| Profil/signature de Julien | C2 proposé, coordonnées personnelles caviardées | Identification du salarié et rapprochement avec Hexalp |

PSSI : écarts 5.2 (compte personnel),5.5 (secrets en clair), exigences 2.3/7.1 à confronter aux validations et contrats. P4 indique aucun contrat Hexalp pour ce compte. Ne pas assimiler toutes les informations confidentielles à des secrets ni affirmer une fuite de clé privée absente.

## 4. Constats techniques et actions

P5 : les accès récurrents du proxy Zabbix et les 401 du scan concordent avec le journal DSI. Un 401 initial VPN est compatible avec l’authentification Basic, pas à lui seul une attaque. Les 200 de 10.20.250.200, plage hors équipe infra, justifient l’enquête, **pas l’attribution à un attaquant**. L’utilisateur nommé admin ne confère pas le mode stats admin.

P6 : seules des sources attendues (Ansible, deux applications) sont recensées pour le jeton ; dernière utilisation 12/10 à 06 h. Pas d’abus observé dans ce résumé, mais pas de garantie d’intégrité des hôtes/images. P7 : check inter 30s fall 10 présents, fichier modifié hors commit et changement absent du journal selon Sofia. Compatible avec la commande IA, sans preuve de l’exécutant exact. Ordre de grandeur du retrait : cinq minutes contre six secondes annoncées par Sofia, selon cadence/état des sondes ; ce n’est pas une durée mesurée.

**Déjà documenté :** signalement CERT, capture forum, export accompagné, examen des logs/jeton/configuration, demande de correspondances VPN et ouverture de main courante. **Non attesté :** retrait public, rotation des deux secrets, correction de configuration, notifications ou réponse VPN.

| Priorité | À faire ; responsable proposé | Justification / preuve de résultat attendue |
| --- | --- | --- |
| Immédiat, en parallèle | Nadia pilote ; Hugo préserve sources et logs, Julien aide pour le compte | Originaux restreints, heures/auteurs/empreintes, références ; ne pas retarder le confinement pour une collecte parfaite |
| Immédiat | Administrateurs révoquent/remplacent stats et jeton ; CI/Ansible coordonnés | Invalider aussi le jeton oublié en 5.1 ; mettre à jour CI/scripts, coffre-fort, moindre droit/expiration ; contrôler continuité sans tester le secret divulgué |
| Immédiat | Julien retire le lien ; RSSI/éditeur traitent le forum et les caches | Preuves minimales d’abord ; vérifier le lien et les pages séparément, sans promettre effacement de toutes les copies |
| Sans délai | Hugo enquête sur VPN, stats, registre/CI/images et activité des comptes | Attribution des deux IP à l’heure précise, sessions et traces de transfert/déploiement ; conserver l’hypothèse de deux incidents indépendants |
| Contrôlé, après capture | Sofia/admins rétablissent des checks validés avec propriétaire WMS | Comparaison au référentiel actuel, test/rechargement maîtrisé, validation métier, commit et retour arrière ; ne pas écraser une évolution légitime ni l’ancien secret |
| Après préservation | Julien/fournisseur : suppression et demandes nécessaires, RSSI/DPO coordonnent | Distinguer lien, conversation, mémoires/fichiers et copies tierces ; réponses/preuves de traitement conservées |

## 5. Information, délais et décisions

Procédure v 1.4(P8) : **DPO immédiatement** si données personnelles possibles, ici confirmées ; **commercial et juridique** car clients touchés ; **direction générale** via Nadia pour gravité 4. Nadia et la direction décident d’autorités/plainte. Aucune de ces informations n’est prouvée comme déjà faite par les pièces.

P8 prévoit **notification Bricomax sous 48 h** : vérifier immédiatement avec juridique le contrat, son déclencheur et les autres contrats, puis préparer une information initiale sans attendre la réponse VPN. Le délai contractuel ne remplace pas le délai RGPD.

Le DPO pilote la qualification prévue par P8 ; juridiquement le responsable de traitement reste responsable des notifications. Documenter la violation ; notification CNIL sauf absence probable de risque pour les personnes, sous 72 h si possible après connaissance ; communication aux personnes en cas de risque élevé. Confirmer rôles client/Hexalp (responsable ou sous-traitant), point de départ et décision motivée : **ni l’ouverture à 9 h ni l’enquête incomplète ne remettent le délai à zéro**. Une notification initiale peut être complétée. Sources : CNIL, RGPD art.33/34, vérifiés 23/10/2026.

## 6. Conclusion et RETEX

**Lien avec l’exfiltration : non établi.** Proximité temporelle, même SI et accès via VPN ; IP différentes, lecture seule des stats et absence d’attribution VPN interdisent d’en déduire une chaîne causale. Recouper sessions, identités, machines, accès registre et chronologie du transfert ; une même identité ne suffirait pas seule à démontrer le lien.

Incident non clos. Avant clôture : secrets invalidés, exposition réduite et vérifiée, impacts investigués, configuration/chaîne d’images validées, obligations traitées et risques résiduels acceptés. **RETEX sous 15 jours selon P8**, déclencheur à préciser avec Nadia ; proposer une échéance au plus tard le 28/10 si retenue à compter du 13/10. Prévoir circuit d’astreinte approuvé, revue des commandes/changements, coffre-fort et prévention des secrets publiés, sans sanctionner la coopération.

Références : P1–P8 du kit/captures ; inventaire J2 U2, PSSI2.6, grille 2.7, journal DSI4.2 et résultats J4. Sources officielles et vérification détaillée de P4 : fiche 5.3 du mémo. Compte rendu provisoire sur les pièces disponibles : chaque mesure reste proposée jusqu’à preuve dans la main courante. Aucun secret n’est reproduit.
