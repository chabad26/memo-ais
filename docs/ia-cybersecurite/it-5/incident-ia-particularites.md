# Ce qu’un incident IA a de particulier

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

Comme expliqué au [J2, section 2.4](../it-2/quelles-donnees-sont-envoyees.md), **supprimer le chat ne démontre pas un retrait rétroactif d’un entraînement déjà réalisé**. Nous n’avons aucune preuve d’entraînement sur la conversation de Julien. Les règles vérifiées aujourd’hui ne prouvent pas les réglages ni les conditions exactes de son compte au 24 septembre : les conserver et les vérifier dans le dossier.

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

- [L’alerte — 5.1](l-alerte.md)
- [Sommaire du J5](index.md)

**Références consultées le 23/10/2026 :** NIST SP800-61r3 ; CNIL, notification de violation ; documentation officielle OpenAI liée ci-dessus. Les éléments du scénario sont distincts de ces règles générales.
