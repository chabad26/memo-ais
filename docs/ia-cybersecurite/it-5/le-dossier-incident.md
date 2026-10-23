# Le dossier d’incident

!!! note "Suite du scénario reçue en 5.5 — Nadia, 13 h 30"
    Nadia annonce le compte rendu envoyé à la direction, les secrets changés et le lien/message de forum supprimés. Les analyses ci-dessous conservent leur état sur P1–P8 avant ce message ; les copies résiduelles et impacts ne sont pas réputés résolus. Voir [la suite et la politique proposée](la-politique-utilisation-ia.md).

**Séquence 5.3 — 2 h 15 — Autonomie**

> **Nadia [09:05]** L’incident est ouvert, la main courante aussi. Voici tout ce que Julien, Hugo et Sofia ont retrouvé depuis ce matin. Est-ce qu’il y a des données clients dedans ? Et est-ce que ça a un rapport avec l’exfiltration du 9 octobre ? Je veux des faits. Et quand on ne sait pas, je veux qu’on l’écrive.

## Livrable et limites des pièces reçues

Le compte rendu est rédigé dans **`livrables/ia-cybersecurite/it-5/ia01-j5/compte_rendu_incident.md`**. Analyse avec assistance des huit pièces ; P5/P6/P8 complétées par les captures fournies. Le copier-coller n’incluait pas la trame du rapport ni le tableau « Ce qui a été transmis » : la structure et le tableau ci-dessous sont proposés, à ajuster si ces éléments sont transmis. Les données et organisations sont fictives. Une mise en page de contrôle A4 du compte rendu tient sur **quatre pages** ; les tableaux d’analyse de cette fiche ne font pas partie de ce décompte.

Les originaux transmis ne sont pas recopiés dans le dépôt : ils contiennent des secrets et des coordonnées. Le rapport caviarde ces valeurs et cite les pièces. **Une pièce de constat n’est pas une preuve de mesure corrective exécutée.**

## Bordereau des huit pièces

| Pièce | Ce qu’elle établit dans le scénario | Limite principale |
| --- | --- | --- |
| **P1 — CERT** | Signalement12/10 à17h48 ; forum publié24/09, indexation rapportée depuis02/10 | Aucune exploitation connue du CERT ; indexation du forum, pas nécessairement du lien de conversation |
| **P2 — Forum** | Capture13/10 à08h02 ; message03h31 le24/09, lien et signature Hexalp,214 vues | Vues de la page, pas214 personnes uniques ni214 consultations de la conversation |
| **P3 — Export** | Export accompagné08h15 ; neuf messages, secret stats, jeton, logs clients, lien03h29 et réglage d’amélioration activé | Export présenté par extraits ; comptages de Hugo, pas un audit autonome de chaque ligne ni preuve d’entraînement effectif |
| **P4 — Notes fournisseur** | Résumé de Sofia à vérifier | Notes et non documentation ; conditions actuelles ne prouvent pas rétroactivement celles de septembre |
| **P5 — Stats** | Accès attendus et accès VPN à enquêter ; page en lecture seule, attente des correspondances VPN | Pas d’identité attribuée à10.20.250.200, ni valeur du secret prouvée par un code200 ; pas d’accès shell démontré |
| **P6 — Jeton** | read_registry/write_registry ; sans expiration, service de déploiement, usage script/CI, registre interne/VPN | Pas de droit global sur GitLab prouvé ; sources attendues recensées ne prouvent pas l’absence d’usage hostile depuis un hôte compromis |
| **P7 — Configuration** | Paramètres30s/10 ; fichier modifié, pas de commit ou journal trouvé pour ce changement | Auteur et moment exacts à établir ; similarité avec la commande IA, pas trace d’exécution exacte |
| **P8 — Procédure** | Signalement RSSI, main courante, DPO, clients/juridique, DG, autorités, RETEX | Application effective non attestée ; contrat Bricomax mentionné, texte complet et déclencheur48h à vérifier |

## Pièces 5, 6 et 8 — Lecture détaillée caviardée

### P5 — Interpréter les accès, sans inventer un attaquant

| Date | Source | Réponse | Lecture |
| --- | --- | --- | --- |
| 24/09 02h38 et03h10 | 10.20.2.14, admin | 200 | Attribué à Julien par Hugo ; premier accès avant conversation, second après début : pas tout accès postérieur à une fuite est hostile |
| 30/09 10h05–12/10 | 10.20.1.7, admin | Environ3600 accès | Proxy Zabbix mis en service au journal DSI ; rotation du secret à coordonner pour ne pas casser la collecte |
| 06/10 21h14 | 10.20.1.250 | 401×12 | Scanner mensuel connu ; événement non assimilé automatiquement à une intrusion |
| 08/10 23h47 | 10.20.250.200 | 401 puis200 avec admin | Challenge Basic puis succès : accès VPN hors infra à attribuer, pas preuve en soi d’un brute force |
| 08/10 23h48–23h58 | Même IP/admin | 200×9 | Consultations répétées ; sauvegarder les traces et rapprocher des sessions VPN, sans conclure au vol d’identifiants sur le seul codeHTTP |

La page est déclarée **en lecture seule**, sans directive `stats admin`. Le mot `admin` du compte ne suffit pas à déduire un privilège de modification HAProxy. La documentation distingue l’authentification et l’activation du niveau d’administration. [HAProxy, manuel officiel](https://docs.haproxy.org/3.2/configuration.html).

### P6 — Le jeton à traiter en plus du mot de passe

| Propriété | Analyse utile au traitement |
| --- | --- |
| Secret | **[JETON CAVIARDÉ]** associé à svc-deploy |
| Vie | Créé14/03/2025 ; aucune expiration |
| Portée | read_registry/write_registry sur le registre interne ; pas un mot de passe SSH ni une clé privée |
| Dépendances | Script de déploiement et CI WMS ; Ansible et les deux hôtes applicatifs, dernière utilisation12/10 à06h |
| Risque | Un détenteur disposant de la connectivité et des droits effectifs pourrait lire ou publier des images ; compromission de la chaîne possible, non prouvée |
| Mesure | Révoquer et remplacer dans toutes les dépendances, coffre-fort, expiration et droits minimaux ; préserver/inspecter journaux registre, CI et images/digests déployés |

La remarque de l’assistant qui recommandait de protéger le jeton n’a pas retiré sa valeur de l’historique partagé. Faire une réponse pertinente sur un secret ne remédie pas à son exposition.

### P8 — Information et gouvernance

| Destinataire / action | Règle du scénario | État des preuves |
| --- | --- | --- |
| RSSI et main courante | Signalement sans délai ; heures et auteurs de chaque fait/action | Nadia informée ; ouverture annoncée, contenu complet de la main courante non fourni |
| DPO | Immédiatement si données personnelles possibles | Nécessaire ici ; information et décision non attestées |
| Commercial/juridique | Si données client ; Bricomax48h, autres contrats à vérifier | À engager ; pas de notification réputée envoyée |
| Direction générale | Information RSSI pour gravité3/4 | Gravité4 ; information à tracer |
| Autorités/plainte | Décision RSSI avec DG | Décision à documenter, pas d’automatisme |
| RETEX | Sous15jours, recherche de causes | À planifier ; point de départ à préciser, proposition de borne28/10 si compté depuis13/10 |

P8 confie la décision interne de notification au DPO ; **le RGPD maintient la responsabilité juridique du responsable de traitement**. Il faut aussi vérifier si Hexalp agit pour certains clients comme sous-traitant. Le délai72h concerne la connaissance de la violation et non l’ouverture administrative du ticket ; les compléments peuvent suivre une notification initiale. [CNIL, RGPD articles33/34](https://www.cnil.fr/fr/reglement-europeen-protection-donnees/chapitre4), consulté23/10/2026.

## Vérifier les cinq notes du fournisseur — P4

Vérification le **23 octobre 2026**, pas certification des conditions historiques du24/09. La conservation des réglages/conditions de l’époque reste nécessaire.

| Point P4 | Vérification officielle et nuance |
| --- | --- |
| **1 — Amélioration des modèles** | Confirmé pour les offres individuelles : usage possible et refus pour les nouvelles conversations. Réglage activé dans P3, mais pas de preuve qu’une conversation donnée ait été entraînée. [OpenAI, usage des données](https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance) |
| **2 — Suppression sous30jours** | À nuancer : programmée sous30jours, sauf obligations de sécurité/juridiques ou données déjà désidentifiées/dissociées ; disparition du compte immédiate, pas effacement partout attesté. [OpenAI, suppression des chats](https://help.openai.com/en/articles/8809935-deleting-and-archiving-chats-in-chatgpt) |
| **3 — Suppression du lien** | Contrôle accessible au titulaire ; suppression de la conversation originale retire aussi son lien. Une copie conservée par un destinataire peut subsister. [OpenAI, partage](https://help.openai.com/en/articles/7925741-sharing-conversations-and-scheduled-tasks-in-chatgpt) |
| **4 — Seul titulaire, aucun contrat Hexalp** | L’export personnel et les contrôles de compte nécessitent une identité vérifiée ; Hexalp n’est pas administrateur de ce compte. « Seul peut demander l’effacement » est trop absolu : droits des personnes et demandes au prestataire suivent leurs propres voies. Absence de contrat Hexalp rapportée par P4, pas prouvée par une page de documentation. [OpenAI, export et Privacy Portal](https://help.openai.com/en/articles/7260999-exporting-your-chatgpt-history-and-data) |
| **5 — Forum/caches** | Un lien retiré ne retire pas les copies d’un tiers ; traiter la page de forum et les moteurs séparément. Ne pas garantir l’effacement de copies téléchargées. [OpenAI, limites du retrait d’un partage](https://help.openai.com/en/articles/7925741-sharing-conversations-and-scheduled-tasks-in-chatgpt) |

**Été2025 :** un article Malwarebytes du1er août2025 rapporte le retrait par OpenAI d’une expérimentation permettant de rendre des conversations partagées découvrables par les moteurs via une option volontaire. Il relaie l’annonce du responsable sécurité ; la publication primaire liée n’a pas été accessible lors de la vérification. Ce précédent documente un risque de partage, **pas la cause de l’indexation du forum Hexalp en2026**. [Ressource historique du kit, Malwarebytes](https://www.malwarebytes.com/blog/news/2025/08/openai-kills-short-lived-experiment-where-chatgpt-chats-could-be-found-on-google).

## Réponses à inscrire au carnet

### 1. Réponse à Nadia sur l’exfiltration, en trois lignes

Le lien n’est pas établi : publication et consultation VPN précèdent l’exfiltration, sur le même SI, mais les IP diffèrent.  
L’interface stats est en lecture seule ; le jeton peut agir sur le registre, sans abus démontré dans les sources recensées.  
Il faut les correspondances VPN, les sessions, les traces hôte/registre et la chronologie du transfert ; même une identité commune ne prouverait pas seule la causalité.

### 2. Ce qui n’est pas un secret

Le chemin TLS n’est pas la clé privée ; l’empreinte publique SSH n’est pas une clé privée ; les noms de compte ne sont pas leurs mots de passe ; IP, ports, noms et code hors jeton ne sont pas des secrets d’authentification. Les données clients/personnelles sont confidentielles sans être pour autant des moyens d’accès. Cela évite de surévaluer certaines capacités tout en **ne minimisant pas la fuite C2**. Séparer rotation des deux vrais secrets, protection des personnes et enquête sur l’architecture/code.

### 3. Retour sur les cinq actions initiales de5.1

| Action initiale | Ce que le dossier oblige à préciser ou compléter |
| --- | --- |
| Piloter avec Nadia/Julien | Ajouter explicitement DG, commercial/juridique et DPO, avec obligations P8 ; contact CERT déjà reçu, ne pas le présenter comme à initier |
| Préserver des preuves | Des captures/export existent ; obtenir les originaux, leur intégrité et la main courante complète, sans attribuer des heures inventées à nos propres actions |
| Neutraliser le secret stats | **Oubli principal : le jeton de déploiement**, non visible au J2U2. Traiter CI/Ansible/registre et leurs dépendances ; ne pas casser le proxy qui réutilise le compte stats |
| Retirer le public | Deux objets : lien et forum, plus copies/caches ; captures et indexation désormais étayées ;214 vues ne sont pas214 lecteurs du lien |
| Délimiter/informer | Données personnelles confirmées ; déclencher immédiatement la chaîne P8, vérifier Bricomax48h, et recouper deux IP VPN sans conclure. Formaliser remise en état, preuve de résultat et RETEX15jours |

Les cinq actions initiales étaient cohérentes mais trop générales sur le second secret, les dépendances techniques et les délais clients/RETEX. Le dossier ne prouve pas encore qu’elles ont été appliquées : garder la différence entre recommandation et main courante effective.

## Compte rendu rédigé

Le texte ci-dessous est la copie de lecture du livrable ; les notes et tableaux d’analyse détaillés ci-dessus restent hors de sa limite de quatre pages.

---

## Compte rendu d’incident — Conversation IA et WMS Hexalp

**Olivier HIMBLOT — rédigé avec assistance le 23 octobre 2026**  
Situation étudiée : mardi 13 octobre 2026, après le message de Nadia de 09 h 05. Données fictives ; diffusion de travail limitée. Secrets et coordonnées individuelles caviardés.

### 1. Synthèse et qualification

**Oui, des données clients et personnelles ont été publiées** dans une conversation partagée : le décompte de Hugo porte sur 41 adresses e-mail, neuf clients, 17 adresses de livraison, 12 téléphones et six comptes de service (P3). Ces nombres ne s’additionnent pas pour obtenir un nombre de personnes uniques. Deux secrets sont exposés : mot de passe stats HAProxy et jeton de déploiement (P3/P6).

**Gravité 4, risque critique G4×V4=16 pour l’exposition C3**, conformément à la grille J2 ; exploitation hostile des secrets non établie. Trois volets : confidentialité (publication), intégrité (configuration non versionnée), disponibilité (retrait des backends retardé). L’accès VPN du 08/10 est à investiguer ; **aucun lien causal démontré avec l’exfiltration du 09/10**.

Le rapport s’appuie sur P1–P8, dont P5/P6/P8 reçues en captures. La trame et le tableau annoncés dans la consigne n’étaient pas visibles dans le copier-coller : structure de travail proposée. Les pièces décrivent des constats et collectes, **pas un confinement terminé**.

### 2. Chronologie sourcée

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

### 3. Ce qui a été transmis

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

### 4. Constats techniques et actions

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

### 5. Information, délais et décisions

Procédure v 1.4(P8) : **DPO immédiatement** si données personnelles possibles, ici confirmées ; **commercial et juridique** car clients touchés ; **direction générale** via Nadia pour gravité 4. Nadia et la direction décident d’autorités/plainte. Aucune de ces informations n’est prouvée comme déjà faite par les pièces.

P8 prévoit **notification Bricomax sous 48 h** : vérifier immédiatement avec juridique le contrat, son déclencheur et les autres contrats, puis préparer une information initiale sans attendre la réponse VPN. Le délai contractuel ne remplace pas le délai RGPD.

Le DPO pilote la qualification prévue par P8 ; juridiquement le responsable de traitement reste responsable des notifications. Documenter la violation ; notification CNIL sauf absence probable de risque pour les personnes, sous 72 h si possible après connaissance ; communication aux personnes en cas de risque élevé. Confirmer rôles client/Hexalp (responsable ou sous-traitant), point de départ et décision motivée : **ni l’ouverture à 9 h ni l’enquête incomplète ne remettent le délai à zéro**. Une notification initiale peut être complétée. Sources : CNIL, RGPD art.33/34, vérifiés 23/10/2026.

### 6. Conclusion et RETEX

**Lien avec l’exfiltration : non établi.** Proximité temporelle, même SI et accès via VPN ; IP différentes, lecture seule des stats et absence d’attribution VPN interdisent d’en déduire une chaîne causale. Recouper sessions, identités, machines, accès registre et chronologie du transfert ; une même identité ne suffirait pas seule à démontrer le lien.

Incident non clos. Avant clôture : secrets invalidés, exposition réduite et vérifiée, impacts investigués, configuration/chaîne d’images validées, obligations traitées et risques résiduels acceptés. **RETEX sous 15 jours selon P8**, déclencheur à préciser avec Nadia ; proposer une échéance au plus tard le 28/10 si retenue à compter du 13/10. Prévoir circuit d’astreinte approuvé, revue des commandes/changements, coffre-fort et prévention des secrets publiés, sans sanctionner la coopération.

Références : P1–P8 du kit/captures ; inventaire J2 U2, PSSI2.6, grille 2.7, journal DSI4.2 et résultats J4. Sources officielles et vérification détaillée de P4 : fiche 5.3 du mémo. Compte rendu provisoire sur les pièces disponibles : chaque mesure reste proposée jusqu’à preuve dans la main courante. Aucun secret n’est reproduit.
