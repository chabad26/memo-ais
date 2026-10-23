# Carnet de bord J5 — Incident et politique IA d’Hexalp

**Olivier HIMBLOT — 23 octobre 2026**  
Initialisation du carnet avec assistance. Mise en situation fictive ; aucune activité J5 exécutée à ce stade.

## Contexte reçu

Le matin, un compte rendu individuel doit analyser l’incident lié à la conversation de Julien du 24 septembre : données sorties, compte, preuves, mesures et personnes à informer. L’après-midi, une politique IA est attendue en groupe, puis relue et corrigée si nécessaire. Le carnet accueillera les réponses, la fiche « Ce qui arrive », la relecture de la politique et le retour sur les usages du J1.

Aucune installation ni nouveau jeu de fichiers n’est demandé. Les consignes détaillées des missions restent attendues ; le compte rendu et la politique ne sont pas préremplis.

## Références de travail

- [Usages du J1](../../../../docs/ia-cybersecurite/it-1/le-message-de-nadia.md) et [frise de l’IA](../../../../docs/ia-cybersecurite/it-1/70-ans-intelligence-artificielle.md) — 5.4/5.7.
- [Dossier Hexalp, inventaire et note à Nadia](../../../../docs/ia-cybersecurite/it-2/le-dossier-hexalp.md) — 5.3/5.5.
- [PSSI](../../../../docs/ia-cybersecurite/it-2/ce-que-dit-la-pssi.md) et [qualification du risque](../../../../docs/ia-cybersecurite/it-2/qualifier-risque-choisir-mesure.md) — 5.3/5.5.
- [Journal des changements de la DSI](../../../../docs/ia-cybersecurite/it-4/relancer-et-reparer.md) — 5.3.
- [Rapport J4](../../../../docs/ia-cybersecurite/it-4/le-rapport-evaluation.md) et [conditions proposées d’exploitation](../../../../docs/ia-cybersecurite/it-4/exploiter-sans-se-fier-aveuglement.md) — 5.5.

## État initial

Présentation et références réunies. Aucun compte rendu d’incident, échange collectif, politique validée ou action sur le SI n’est attesté pour le J5. Les faits, propositions, actions réalisées et limites de preuve seront distingués au fil des exercices. Les secrets des pièces seront cités caviardés.


# Séquence 5.1 — L’alerte

**Séquence 5.1 — Présentiel**

## Mardi 13 octobre — Le message de Nadia

Nadia devait présenter le rapport d’évaluation vendredi au comité. Un message reçu la veille a changé son programme.

> **Nadia [08:41]** Mauvaise nouvelle de la soirée 😬  
> Le CERT régional m’a écrit hier à 17 h 48 : une page publique contient une configuration d’Hexalp, avec un mot de passe.  
> C’est la conversation de Julien du 24 septembre, celle que vous aviez relevée dans votre inventaire du J2. Elle avait été partagée par un lien public.  
> Julien est avec nous et il coopère. Ce n’est pas un procès, c’est un incident 🙏  
> J’ouvre l’incident à 9 h. À midi, je veux un compte rendu : ce qui est sorti, ce qu’on a fait, ce qui reste à faire.

**Chronologie du scénario :** conversation le 24 septembre 2026 ; signalement du CERT rapporté pour le lundi 12 octobre à 17 h 48 ; message de Nadia le mardi 13 octobre à 08 h 41 ; ouverture annoncée à 9 h et compte rendu demandé à midi. **Date réelle de rédaction de cette feuille : 23 octobre 2026.** Aucun dossier détaillé de l’incident n’est encore fourni pour cette activité.

## Mission — Cinq premières actions, avant d’ouvrir le dossier

Proposition initiale rédigée avec assistance à partir de l’alerte et des éléments déjà connus du J2, **avant les nouvelles pièces du dossier J5**. Ce sont des actions à lancer, pas un relevé d’actions exécutées. Leur ordre sera comparé au compte rendu en fin de matinée.

| Ordre | Action à lancer | Pourquoi elle passe avant la suivante |
| --- | --- | --- |
| **1** | **Confirmer la prise en charge avec Nadia et mobiliser Julien et les administrateurs concernés.** Horodater le signalement dans le suivi d’incident, désigner le pilote et demander au CERT son message original et la référence de la page par le canal de contact existant. | Un pilote et une cible identifiée permettent d’agir vite sans se disperser ; ne pas attendre 9 h pour alerter et préparer le confinement. |
| **2** | **Préserver un minimum de preuves sans retarder la protection.** Conserver message CERT, URL, horodatage et copie contrôlée de la page/conversation dans un espace restreint ; préserver les journaux utiles. Julien coopère à la collecte de son compte, sans communiquer son mot de passe. | Le retrait public peut faire disparaître une source utile ; une collecte courte précède ce retrait. Ne pas attendre une expertise complète pour lancer les deux mesures suivantes. |
| **3** | **Neutraliser le secret exposé.** Avec les administrateurs, identifier sa portée, renouveler le mot de passe de l’interface stats, traiter une éventuelle réutilisation et restreindre l’accès à cette interface ; vérifier le résultat sans interrompre inutilement le WMS. | Retirer la page n’invalide pas les copies déjà réalisées : l’ancien secret doit cesser d’ouvrir un accès. Préserver les traces disponibles et tracer le changement. |
| **4** | **Couper la diffusion publique.** Avec Julien, désactiver le lien partagé ; demander au fournisseur le retrait si nécessaire, puis vérifier que l’ancienne URL n’ouvre plus le contenu sans authentification. Rechercher les autres partages et copies accessibles. | Cela réduit les nouvelles consultations ; après le confinement du secret, retirer la source limite la poursuite de la diffusion sans supposer que toutes les copies disparaissent. |
| **5** | **Délimiter l’impact et préparer le point de situation.** Identifier les données réellement publiées, rechercher les accès et modifications sur l’interface/HAProxy/WMS et les comptes concernés, examiner les changements du 24 septembre ; informer les responsables utiles via Nadia, et associer le DPO si des données personnelles sont en jeu. | Une fois les premières mesures lancées, l’enquête guide les décisions suivantes et le compte rendu ; elle évite d’annoncer une compromission ou un retour à la normale sans preuve. |

Cet ordre est une **priorité logique**, pas une obligation de travailler en série : dès que l’URL et le service sont identifiés, préservation courte, rotation et retrait peuvent être répartis entre plusieurs intervenants. Une exposition active peut justifier de confiner immédiatement, en documentant ce qui n’a pas pu être préservé.

Dans le livrable, les secrets seront **caviardés** ; les originaux nécessaires restent dans un espace de preuve à accès limité. Aucune commande de la conversation ne doit être exécutée comme une procédure de réparation validée.

## Relecture du J2 — La fiche de Julien

Référence relue : **fiche U2, source pièce 7**, dans [Le dossier Hexalp — 2.8](../../../../docs/ia-cybersecurite/it-2/le-dossier-hexalp.md).

| Question | Réponse issue de notre inventaire J2 |
| --- | --- |
| **Quel niveau de risque ?** | **G4 × V4 = 16 — Critique**, pour l’exposition décrite du secret C3. Cette cotation ne signifiait pas qu’un attaquant avait utilisé le secret. |
| **Quelle mesure avions-nous proposée ?** | Renouveler le secret stats, vérifier sa portée et les accès, récupérer les preuves sous accès restreint ; contrôler HAProxy/WMS et les modifications réellement appliquées, avec tests et retour arrière. Fournir un circuit de dépannage et un outil approuvé avec extraits minimisés, y compris en astreinte. |
| **Quel besoin métier ?** | Rétablir le WMS en incident nocturne ; la réponse doit préserver la capacité de dépannage, pas seulement interdire l’assistant. |
| **Que savions-nous ?** | Copier-coller d’une configuration et de logs dans un assistant public sur compte personnel gratuit ; secret stats transmis en clair ; réseau interne décrit ; 2 400 lignes annoncées, non disponibles intégralement. |
| **Que le J2 ne montrait-il pas ?** | La création d’un **lien public** et l’accessibilité de la conversation sur une page ; leurs dates, durée, lecteurs, indexation et éventuelles copies. Les nouvelles pièces seront nécessaires pour établir ces éléments précisément. |
| **Quels autres points restaient inconnus ?** | Contenu complet des logs, données personnelles ou autres secrets éventuels ; rotation déjà effectuée ou non ; accès illégitime, réutilisation du secret et effets réels de la commande proposée sur la production. |

Le chemin d’un certificat figurant dans la configuration ne démontrait **ni la sortie de sa clé privée ni celle de son contenu**. Le « ça remarche » de Julien ne prouvait pas l’exécution exacte de la commande ou une réparation durable. Le nouveau message de Nadia ne comble pas ces inconnues.

## Ce que l’alerte change — et ne prouve pas encore

Le scénario apporte **un signalement de publication accessible par lien public**, au-delà de l’envoi au fournisseur déjà relevé au J2. La source disponible ici reste le message de Nadia rapportant celui du CERT : la page, le message original et leurs traces ne sont pas encore collectés dans cette activité.

La date du 24 septembre est celle de la conversation, **pas nécessairement celle de création du lien**. Rien ici ne permet de dater une première consultation, d’identifier tous les lecteurs, de conclure à une indexation, à une exploitation du mot de passe ou à un entraînement du fournisseur sur cette conversation. Le retrait du lien ne démontrerait pas à lui seul l’effacement de toutes les copies.

La cotation critique était donc déjà justifiée par le secret C3 ; ce nouveau vecteur public élargit l’exposition à examiner, sans transformer automatiquement le risque en compromission démontrée.

## Julien, source de preuve et partenaire de résolution

La coopération rapide permet de retrouver conversation, partage, contexte de dépannage et changements réalisés. Expliquer ce qui est collecté et pourquoi, limiter l’accès aux éléments personnels et conserver une chronologie factuelle. Le compte rendu décrit faits et actions ; il ne cherche pas un responsable à sanctionner. La posture annoncée par Nadia doit permettre les signalements précoces et éviter que l’organisation perde des preuves par peur de l’aveu.

## Carnet et suite

Les cinq actions initiales et la relecture U2 sont inscrites dans **`livrables/ia-cybersecurite/it-5/ia01-j5/carnet_J5.md`**. La comparaison avec les actions réellement documentées du dossier reste **à faire en fin de matinée**. Aucun retrait, renouvellement de secret, accès au compte de Julien ou contact CERT n’est effectué par l’assistant.

- [Présentation du J5](../../../../docs/ia-cybersecurite/it-5/index.md)
- [Pense-bête de l’itération](../../../../docs/pense-bete/glossaire/ia-cybersecurite/it-5.md)


# Séquence 5.2 — Ce qu’un incident IA a de particulier

**Séquence 5.2 — Présentiel**

## Le concept

Un incident impliquant un service d’IA se traite avec le cycle habituel : détecter, qualifier, contenir, éradiquer, restaurer et tirer les leçons. Il oblige toutefois à examiner plusieurs endroits : le SI, le compte de l’utilisateur, le fournisseur et les éventuelles copies publiques.

| Particularité | Conséquence pour l’intervention |
| --- | --- |
| **Les données ne se rappellent pas comme un accès réseau** | Retirer un partage ou demander une suppression ne garantit pas l’effacement des copies ni un retrait rétroactif d’un entraînement éventuel. Ne pas présumer qu’un entraînement a eu lieu. |
| **Des preuves sont hors du SI** | Conversation, partages et réglages sont dans le compte et chez le prestataire. Le proxy du dossier montre des volumes et destinations, pas le contenu de la conversation. |
| **Les fonctions du service étendent l’exposition** | Examiner partage par lien, mémoire, historique synchronisé et connecteurs effectivement présents ; ne pas affirmer qu’ils ont tous été utilisés. |
| **Le conseil peut avoir changé la production** | Vérifier les commandes réellement exécutées, les fichiers et les contrôles de santé ; une réponse générée ne prouve ni exécution ni changement non tracé. |

Le cycle n’est pas une suite rigide : confinement et collecte peuvent se chevaucher. Le NIST inscrit la réponse aux incidents dans la gestion continue du risque, avec détection, réponse et rétablissement. [NIST SP 800-61 Rev. 3, publié en avril 2025](https://csrc.nist.gov/pubs/sp/800/61/r3/final).

## Vocabulaire clé

| Terme | Sens concret |
| --- | --- |
| **Événement / incident** | Fait observé / événement portant atteinte ou susceptible de porter atteinte à la sécurité du SI |
| **Main courante** | Journal horodaté : auteur, constat, action, résultat, référence de preuve ; séparer ce qui est signalé de ce qui est vérifié |
| **Conservation des preuves** | Préserver avant modification si possible : source, heure et fuseau si connu, méthode, original protégé, empreinte et accès tracés ; une empreinte seule ne prouve pas la provenance |
| **Confinement** | Réduire la poursuite de l’exposition ou d’un accès : retrait public, révocation, restriction d’accès, isolement proportionné |
| **Révocation / rotation** | Invalider un secret / le remplacer et mettre à jour ses usages autorisés, puis s’assurer que l’ancien ne reste pas accepté par la configuration |
| **Violation de données personnelles** | Atteinte à la confidentialité, à l’intégrité ou à la disponibilité de données personnelles ; ce n’est pas seulement un vol ni nécessairement une cyberattaque |
| **RETEX** | Identifier causes et améliorations après l’incident, sans recherche automatique d’un coupable |

La qualification des données personnelles et les obligations associées sont à examiner avec le DPO et le responsable de traitement. [CNIL — Notifier une violation](https://www.cnil.fr/fr/services-en-ligne/notifier-une-violation-de-donnees-personnelles).

## Mission 1 — Une fuite pas comme les autres

La configuration est la même dans les deux cas ; on compare les circuits de perte de maîtrise. Un portable perdu n’est pas automatiquement lu, et une conversation envoyée à un service public n’est pas automatiquement visible par tout Internet : **le partage public est un fait supplémentaire** dans le scénario de Julien.

| Question | Portable perdu dans le train, disque non chiffré | Configuration collée dans un assistant public |
| --- | --- | --- |
| **Qui détient maintenant la donnée ?** | L’entreprise peut conserver l’original ; le détenteur inconnu du portable dispose d’un support lisible, avec d’éventuelles copies faites depuis sa perte | L’entreprise conserve l’original ; le fournisseur traite une copie dans le compte utilisé. Les destinataires d’un partage et auteurs de copies peuvent en détenir d’autres |
| **Peut-on la récupérer ou la détruire ?** | Récupération matérielle possible, sans preuve d’absence de copie. Effacement à distance seulement si dispositif déjà opérationnel et machine joignable ; pas une garantie sur les copies | Demandes et fonctions de suppression/retrait possibles, selon le compte et le service. La DSI ne maîtrise ni toutes les copies ni l’effacement interne du fournisseur ; pas de garantie de retrait rétroactif d’un entraînement déjà réalisé |
| **Combien de personnes ont pu y accéder ?** | Inconnu : personne, une personne ou plusieurs, puis d’éventuels destinataires de copies ; disque non chiffré augmente la possibilité d’accès sans prouver sa lecture | Inconnu : traitements/personnes autorisés selon le service et ses règles ; avec le lien public de Julien, toute personne qui l’obtient peut accéder au contenu partagé. Ni nombre de lecteurs ni indexation déduits du seul partage |
| **Où trouver les preuves de ce qui est sorti ?** | Inventaire des fichiers et synchronisations, sauvegardes, EDR/MDM et journaux disponibles ; support s’il est retrouvé. L’inventaire prouve un contenu possible, pas toutes les lectures | Export et capture de conversation, fichiers transmis, partages/réglages, signalement CERT et page du forum, journaux et demandes au fournisseur. Le proxy corrobore un trafic sans restituer le texte envoyé |
| **Qui peut agir sur la copie, et comment ?** | La personne qui retrouve le support ; l’entreprise via MDM si possible, et les acteurs autorisés de la récupération. L’entreprise peut surtout neutraliser les secrets côté SI | Julien pour son compte personnel ; fournisseur pour ses systèmes ; administrateur du forum pour sa page. Hexalp demande/coordonne ces actions et invalide les secrets de son SI, mais n’administre pas le compte personnel |
| **Le SI a-t-il pu être modifié ?** | Oui si le portable contient un accès, une session ou un secret permettant une action ; la perte seule ne prouve aucune modification | Oui par réutilisation d’un secret exposé ou exécution humaine d’une commande générée. Ni l’envoi du texte ni la réponse du modèle ne prouvent que l’assistant a lui-même accès au SI |

**Point commun :** retirer la source ne rend pas un secret déjà copié inoffensif. La rotation, la recherche de traces et la vérification de l’intégrité restent nécessaires, avec conservation des preuves.

## Mission 2 — L’ordre compte

Ordre proposé : **B → C → A → E → F → G → D → H**. C’est un ordre d’engagement, pas huit tâches à finir l’une après l’autre. Réponse théorique à l’exercice : aucune action n’est exécutée ici.

| Rang | Lettre et action | Justification et précautions |
| --- | --- | --- |
| **1** | **B — Capturer et horodater la page du forum et exporter la conversation complète** | Préserver les éléments avant retrait ; originaux restreints, copies de travail caviardées, liens et heures tracés. Une capture minimale peut précéder le confinement ; ne pas attendre un export long pour protéger le SI |
| **2** | **C — Changer le mot de passe de la page de statistiques HAProxy** | Invalider rapidement le secret exposé et vérifier sa portée/réutilisation. Préserver la configuration nécessaire et tracer l’opération ; contrôler les dépendances. Ne pas attendre de démontrer son exploitation |
| **3** | **A — Supprimer le lien de partage de la conversation** | Réduire les nouvelles consultations avec Julien et vérifier le retrait. Traiter séparément la page du forum auprès de son administrateur si elle reproduit le contenu : supprimer le lien ne supprime pas une copie autonome |
| **4** | **E — Prévenir le DPO** | L’associer tôt pour examiner les données personnelles possibles des logs, l’impact et les obligations. À engager en parallèle dès cette possibilité identifiée, sans attendre la fin des opérations techniques |
| **5** | **F — Chercher dans les journaux si le mot de passe a été utilisé** | Préserver les logs dès B, puis analyser en parallèle de C/A/E : connexions réussies/échouées, comptes, sources, accès à l’interface et changements. L’absence de trace ne prouve pas l’absence d’accès |
| **6** | **G — Remettre HAProxy dans l’état validé** | Après préservation de l’état observé et identification des modifications, appliquer une configuration adaptée à l’infrastructure actuelle, validée et testée, avec retour arrière. Ne pas restaurer aveuglément un ancien fichier ni réintroduire l’ancien secret |
| **7** | **D — Demander à Julien de supprimer la conversation** | Seulement après collecte utile, décision de conservation et coordination avec RSSI/DPO ; contrôler séparément mémoire/fichiers/partages concernés. La suppression réduit la source accessible, sans démontrer l’effacement partout |
| **8** | **H — Rédiger le RETEX** | Consolider causes, décisions, délais, efficacité et corrections avec responsables/échéances. Les faits et actions sont consignés dans la main courante dès le début, pas reconstruits seulement au RETEX |

### 1. Si A précède B, que perd-on ?

On peut perdre l’accès à l’état publié, son contenu, les éléments de contexte et la possibilité de montrer ce qui était visible avant retrait. Le message CERT ou une copie du forum peuvent subsister, mais ne remplacent pas nécessairement l’état exact du partage. La disparition d’un lien complique aussi le rapprochement entre sa publication et la conversation.

Il ne faut toutefois pas prolonger une exposition pour obtenir une preuve parfaite : si le risque est immédiat, confiner, préserver ce qui est accessible et tracer les limites de collecte. **La conservation préalable est un objectif ; elle ne justifie pas de laisser fonctionner un accès dangereux.**

### 2. Conversation supprimée : effacée chez le fournisseur ?

**Pas nécessairement immédiatement, ni partout.** Pour ChatGPT, fournisseur fortement corroboré au J2, la documentation consultée le **23 octobre 2026** indique un retrait immédiat de l’affichage et une suppression des systèmes programmée sous **30 jours**, avec exceptions, notamment obligations de sécurité/juridiques ou données déjà désidentifiées et dissociées. Archiver n’est pas supprimer ; les fichiers conservés séparément dans Library se gèrent à part. [OpenAI — Suppression et archivage des chats](https://help.openai.com/en/articles/8809935-deleting-and-archiving-chats-in-chatgpt).

Supprimer un lien arrête son accès futur, sans effacer les copies déjà conservées par un destinataire. Une page de forum ou une copie indépendante nécessite son propre traitement. [OpenAI — Partages et copies](https://help.openai.com/en/articles/7925741-sharing-conversations-and-scheduled-tasks-in-chatgpt).

Une mémoire distincte peut subsister après suppression du chat : gérer aussi les informations mémorisées et leurs sources concernées. [OpenAI — Mémoire](https://help.openai.com/en/articles/8590148-memory-in-chatgpt).

Comme expliqué au [J2, section 2.4](../../../../docs/ia-cybersecurite/it-2/quelles-donnees-sont-envoyees.md), **supprimer le chat ne démontre pas un retrait rétroactif d’un entraînement déjà réalisé**. Nous n’avons aucune preuve d’entraînement sur la conversation de Julien. Les règles vérifiées aujourd’hui ne prouvent pas les réglages ni les conditions exactes de son compte au 24 septembre : les conserver et les vérifier dans le dossier.

### 3. Rechercher F avant de changer C, ou en même temps ?

**En parallèle dès que possible.** On préserve les journaux et l’état utile, puis on neutralise le secret pendant que le SOC analyse les traces. Attendre toute l’enquête avant rotation laisse une possibilité d’accès persistante. Modifier sans tracer ou préserver l’état peut au contraire compliquer l’attribution, altérer des éléments ou casser une dépendance.

Des journaux d’authentification peuvent montrer un compte et un résultat, **pas forcément quel mot de passe précis a été présenté**. Chercher les traces d’accès compatibles avec la période et les ressources exposées ; documenter les limites de l’authentification/journalisation. Ne jamais utiliser le secret divulgué pour « tester s’il fonctionne » : cela crée des événements qui brouillent l’enquête. Vérifier la configuration et la bonne application du renouvellement par les moyens d’administration autorisés.

### 4. Ce qu’Hexalp peut faire seule ou non

| Action | Maîtrise d’Hexalp / dépendances |
| --- | --- |
| **B — Preuves** | Peut préserver ses propres systèmes, signalement et page accessible dans le cadre autorisé ; export du compte personnel avec la coopération de Julien, et informations internes du fournisseur sur demande |
| **C — Secret** | Maîtrise de ses secrets/services et changements autorisés, sans besoin du compte personnel |
| **A — Lien public** | Julien agit depuis son compte ; Hexalp sollicite le fournisseur si nécessaire. Pour le forum, agir dépend du titulaire du contenu et/ou de l’administrateur, pas seulement de Julien |
| **D — Conversation** | Julien pour son compte personnel ; le fournisseur pour l’effacement de ses systèmes selon ses règles. Ne pas demander les identifiants personnels de Julien ni s’attribuer un droit d’administration inexistant |
| **E / F / G / H** | Mobilisation du DPO, journaux SI, configuration et RETEX sous maîtrise organisationnelle ; les traces et copies détenues par des tiers restent à demander |

Le compte personnel retire à la DSI une partie de la visibilité et de la capacité d’action. Une réponse coordonnée dépend davantage de la coopération de l’utilisateur et du fournisseur. La correction organisationnelle doit fournir un circuit approuvé qui couvre aussi le dépannage nocturne.

## DPO et notification : ne pas confondre information interne et obligation externe

Informer le DPO est une mesure interne de qualification ; **toute fuite de configuration ne déclenche pas automatiquement une notification CNIL**. Examiner si des données personnelles sont touchées, les conséquences et le risque pour les personnes. Lorsqu’une notification est requise, elle ne doit pas attendre un rapport complet : la CNIL prévoit une notification initiale dans le délai de 72 heures applicable et des compléments si nécessaire. Documenter la connaissance de la violation, les décisions et toute raison de retard ; l’ouverture administrative à 9 h ne remet pas un délai à zéro. La décision relève du responsable de traitement, avec l’appui du DPO. [CNIL — Nature, documentation et notification d’une violation](https://www.cnil.fr/fr/services-en-ligne/notifier-une-violation-de-donnees-personnelles).

Le dossier disponible ne permet pas encore de fixer le point de départ réglementaire ni de conclure aux obligations précises d’Hexalp. Aucun signalement externe n’est effectué dans cet exercice.

## État et suite

Comparaison remplie, ordre et quatre réponses inscrits dans **`carnet_J5.md`**, le 23 octobre 2026 avec assistance. La mention d’une page de forum vient de la mission B ; sa relation exacte avec le partage signalé en 5.1 reste à établir sur les pièces. Aucun compte rendu final, restauration, rotation ou suppression effective n’est revendiqué à ce stade.

- [L’alerte — 5.1](../../../../docs/ia-cybersecurite/it-5/l-alerte.md)
- [Sommaire du J5](../../../../docs/ia-cybersecurite/it-5/index.md)

**Références consultées le 23/10/2026 :** NIST SP800-61r3 ; CNIL, notification de violation ; documentation officielle OpenAI liée ci-dessus. Les éléments du scénario sont distincts de ces règles générales.


# Séquence5.3 — Le dossier d’incident

**Séquence 5.3 — 2 h 15 — Autonomie**

> **Nadia [09:05]** L’incident est ouvert, la main courante aussi. Voici tout ce que Julien, Hugo et Sofia ont retrouvé depuis ce matin. Est-ce qu’il y a des données clients dedans ? Et est-ce que ça a un rapport avec l’exfiltration du 9 octobre ? Je veux des faits. Et quand on ne sait pas, je veux qu’on l’écrive.

## Livrable et limites des pièces reçues

Le compte rendu est rédigé dans **`livrables/ia-cybersecurite/it-5/ia01-j5/compte_rendu_incident.md`**. Analyse avec assistance des huit pièces ; P5/P6/P8 complétées par les captures fournies. Le copier-coller n’incluait pas la trame du rapport ni le tableau « Ce qui a été transmis » : la structure et le tableau ci-dessous sont proposés, à ajuster si ces éléments sont transmis. Les données et organisations sont fictives.

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


Compte rendu source : **`compte_rendu_incident.md`**, rédigé sur les pièces disponibles ; mesures correctives proposées, non réalisées par l’assistant.


**Contrôle de remise5.3 :** compte rendu caviardé rédigé ; pagination A4 de contrôle vérifiée sur quatre pages. Trame originale et tableau de consigne non visibles dans le texte reçu, structure proposée à confirmer. La réponse VPN et les preuves d’exécution des mesures ne sont pas inventées. Aucun document transmis à un tiers.


# Séquence 5.4 — Ce qui arrive

**23 octobre 2026 — synthèse préparée avec assistance ; choix de groupe à confirmer.**

Sujet proposé : **2 — Des attaquants outillés par des agents**. La [fiche complète](../../../../docs/ia-cybersecurite/it-5/ce-qui-arrive.md) contient les trois lignes factuelles, les deux sources datées (Anthropic et MITRE C0062), leurs intérêts et limites, les conséquences pour l’infrastructure, la règle proposée et la trame de restitution. MITRE reprend ici les informations d’Anthropic : deux publications ne prouvent pas une validation indépendante du chiffre d’automatisation.

**Règle proposée :** tout agent accédant au SI est déclaré et approuvé, dispose d’une identité dédiée et de droits limités, exige une validation humaine avant écriture en production, produit des traces sans secrets et peut être révoqué. Responsables proposés : infrastructure et RSSI ; test avant activation en environnement de test.

**Carte 2025–2026 ajoutée à la frise J1 :** campagne septembre 2025, révélation novembre 2025, fiche MITRE 2026 ; apprentissage associé aux outils, sans réapprentissage démontré pendant l’attaque. Importance : encadrer les actions et les permissions, au-delà du texte du prompt.

**Réserve documentaire :** page officielle OWASP LLM consultée affichant 2025, Excessive Agency en LLM06 ; rang 3 en 2026 non corroboré. Les cinq sujets sont conservés comme pistes ; pas de tests Glasswing exécutés ou de bilan indépendant inventé. Répartition entre groupes, présentation de deux minutes, politique approuvée et déploiement non attestés.


# Séquence 5.5 — La politique d’utilisation de l’IA

**Nouvelle information du scénario — Nadia13h30 :** compte rendu envoyé à la direction, secrets changés, lien et message du forum supprimés. Déclaration attribuée à Nadia, sans exécution de l’assistant ni preuve d’effacement de copies. Les conclusions antérieures correspondaient aux pièces alors disponibles ; impacts et notifications restent à suivre.

**Production :** `politique_ia_hexalp.md`, V0.1 rédigée avec assistance, quinze rubriques et annexes ; PDF de quatre pages dans le mémo. [Feuille5.5 et téléchargements](../../../../docs/ia-cybersecurite/it-5/la-politique-utilisation-ia.md). Listes A/B/C proposées, usage ChatGPT professionnel limité C0/fictif sous prérequis d’ouverture et laboratoire local fictif ; pas d’autorisation SaaS ou C2 déjà acquise. Chaque interdiction dispose d’une solution métier interne.

**Trois vérifications de relecture :** prescriptions introduites par un verbe et un rôle ; alternatives métier indiquées ; incident Julien rapproché des§2/3/4/5/8/10/11/12/13. Règle du sujet5.4 inscrite au§7 : identité d’agent dédiée, droits minimaux, validation des actions et révocation. Les durées de conservation et délais sont des choix proposés, pas des normes attribuées aux sources.

**Préparation du lundi :** approbation direction, responsables, catalogue/compte/réglages, supports et annuaire, tests techniques et diffusion à vérifier. Signalement de bonne foi protégé ; le silence après demande ne vaut pas accord. Compte/offre de l’assistance non vérifiés, donc aucune conformité de cette rédaction à une politique Hexalp déjà en vigueur n’est affirmée.

**État :** rédaction et contrôle de pagination réalisés ; partage des rubriques entre membres, relecture croisée collective, approbation direction et déploiement non attestés. Aucun envoi de la politique à un tiers.


# Séquence 5.6 — Convaincre le comité et retour sur mes usages

**Consigne reçue :** Nadia16h15 ; présentation de trois minutes sans diaporama, cinq règles, règle préférée justifiée par une situation étudiée, retour sur le24/09, puis usages personnels et bilan. Numérotation5.6 confirmée par l’apprenant. Préparation avec assistance ; oral non attesté.

## Préparation orale

**0:00–0:50 — Les cinq règles.**

« Notre politique permet d’utiliser l’IA avec un cadre clair. Première règle : choisir un outil et un compte professionnels approuvés pour l’usage. Deuxième : retirer les secrets et limiter les données avant toute demande. Troisième : faire relire et tester le code, les commandes et les configurations avant la production. Quatrième : faire approuver les extensions, connecteurs et agents, avec des droits limités. Cinquième : signaler immédiatement un envoi ou un accès suspect, sans sanction pour le seul fait d’avoir signalé de bonne foi. »

**0:50–1:45 — La règle à défendre.**

« Nous proposons de défendre le paragraphe 11 : une demande d’outil reçoit un accusé sous un jour ouvré et une décision sous dix jours ouvrés, avec une alternative métier. Le silence ne vaut pas autorisation. En urgence, manager et RSSI arbitrent une solution interne. Cela répond au problème du J2 : une personne avait attendu trois semaines et commencé à utiliser un outil sans validation. Une interdiction seule n’aurait pas couvert son besoin. Cette règle oblige aussi l’organisation à répondre et à fournir une solution. »

« La situation du J2 a guidé notre relecture : attendre trois semaines sans réponse ne couvre pas le besoin métier. Le paragraphe 11 fixe donc un responsable, un délai et une solution transitoire. »

**1:45–2:40 — Ce qui aurait changé le 24 septembre.**

« Julien aurait eu un chemin de dépannage interne et un référent d’astreinte, au lieu d’utiliser son compte personnel. Les paragraphes 4 et 5 imposent de retirer les deux secrets et de minimiser les journaux et données clients. Le paragraphe 8 exige une seconde relecture et des tests avant d’appliquer une commande en production ; le paragraphe 10 garde la trace du changement. Les paragraphes 2 et 5 excluent le partage public de la conversation métier. Si une exposition survient malgré tout, le paragraphe 12 organise immédiatement l’alerte, le confinement et les personnes à informer. »

**2:40–3:00 — La décision demandée.**

« Nous demandons d’approuver le cadre et ses moyens : catalogue, compte professionnel, support, relecteurs et contrôles vérifiés. L’ouverture de l’espace IA reste conditionnée à ces vérifications ; les outils internes permettent de travailler en attendant. Nous ne prétendons pas que le texte suffit à déployer les contrôles. »

### Correction de la consigne

**Coquille confirmée par l’apprenant : le module ne comporte pas de crash-test.** La présentation s’appuie sur la relecture de la politique et sur les situations étudiées au J2 et dans l’incident de Julien. Aucun résultat de crash-test ni correction associée n’est attendu au carnet.

## Retour sur mes usages du J1

Source : [inventaire personnel du 19 octobre](../it-1/le-message-de-nadia.md). Deux usages de **Codex**, un seul outil, sont documentés ; aucun autre outil personnel n’est ajouté par supposition. L’évaluation ci-dessous applique la politique proposée comme grille de lecture, sans prétendre qu’elle régit déjà la formation.

| Usage observé | Ce que la politique en dirait | Pourquoi et conditions | Changement proposé dès lundi |
| --- | --- | --- | --- |
| **Codex pour rédiger et structurer le mémo** | **À valider** | Codex n’a pas d’entrée autorisée dédiée dans la liste A ; type de compte, offre et garanties non vérifiés. §2/3/4/11 : faire valider outil, compte et classes de données avant emploi professionnel | Vérifier compte et périmètre autorisé ; préparer des contenus fictifs ou publics minimaux ; ne pas envoyer de pièces internes en attendant l’accord |
| **Codex comme agent dans le dépôt** | **À valider** | Même outil, avec lecture/édition/exécution supplémentaires. §5/7/8/10 : vérifier fichiers accessibles, permissions, commandes, traces et validation des actions à impact. Un accès au dépôt ne prouve pas un accès à une production | Limiter l’espace accessible ; retirer secrets et fichiers sans rapport ; relire les différences et commandes ; vérifier la séparation entre documentation locale et production |

**Interdit dans les deux usages :** fournir des secrets ou traiter des informations Hexalp avec un compte personnel (§3/4), même si l’outil est ensuite approuvé. Le compte n’étant pas identifié, on ne transforme pas cette condition en constat d’écart réel. Un usage non validé ne devient pas autorisé parce que son résultat semble utile.

### Mes pratiques dès lundi — engagements proposés à confirmer

- Vérifier le type de compte et l’autorisation pour le contexte professionnel avant tout envoi.
- Décrire le problème avec un exemple fictif minimal ; garder configurations, journaux bruts et coordonnées internes dans les outils internes.
- Définir le périmètre de fichiers accessible à l’agent ; contrôler ses changements avant de les conserver.
- Faire relire par une seconde personne habilitée toute proposition destinée à la production, avec tests et retour arrière ; pour une modification documentaire locale, conserver une relecture adaptée et les vérifications du dépôt.
- Signaler immédiatement une exposition suspectée, sans recopier le secret ni attendre une preuve d’exploitation.

Ces points sont des engagements de pratique proposés, pas la preuve qu’ils ont déjà été mis en place. L’inventaire personnel reste limité aux usages observés.

## État avant remise

Politique V0.1 de quatre pages disponible ; présentation et retour d’usages préparés. Aucun crash-test n’est prévu dans le module, selon la correction de l’apprenant ; aucune rubrique de résultats associée ne manque. La validation collective reste à confirmer.

## Ce que je sais faire aujourd’hui — bilan proposé à personnaliser

> Aujourd’hui, je sais mieux distinguer un modèle fondé sur l’apprentissage d’une règle automatisée et expliquer ce qu’ajoutent les outils d’un agent. Je sais analyser un usage d’IA en regardant le fournisseur, le compte, les données, les permissions et les preuves disponibles. Les exercices m’ont appris à regarder les faux positifs, les faux négatifs et la charge de qualification plutôt qu’un pourcentage global. Pour un incident, je peux distinguer exposition, exploitation démontrée et mesure seulement proposée, puis transformer le risque en une règle avec un responsable, un contrôle et une solution métier. Il me reste à vérifier mon propre compte et les garanties des outils, à pratiquer la validation des permissions et la révocation, et à vérifier l’application de la politique sur des situations concrètes. Je dois aussi pouvoir expliquer ces choix sans reprendre aveuglément le texte de l’assistant.

Ce bilan est proposé à partir des travaux documentés ; il ne mesure pas les compétences initiales ni une maîtrise autonome. L’apprenant le corrige selon ce qu’il peut personnellement expliquer et reproduire.

