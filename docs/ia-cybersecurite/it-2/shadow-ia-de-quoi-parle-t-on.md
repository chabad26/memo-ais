# Shadow IA : de quoi parle-t-on ?

## La méthode d'analyse — À garder en tête du document

Cette grille constitue la **mission 2** et le fil conducteur du livrable de l'après-midi. Elle est placée ici avant le cours pour rester immédiatement accessible.

| Étape | La question à se poser | Séquence |
| --- | --- | --- |
| **1. Outil et fournisseur** | Quel est l'outil ? Qui l'exploite, et où les données sont-elles traitées ? Est-il approuvé ? | 2.2 et 2.3 |
| **2. Compte** | Avec quel compte est-il utilisé ? Qui l'administre ? Qui peut le désactiver ? | 2.3 |
| **3. Données** | Qu'est-ce qui a été envoyé, volontairement ou non ? De quelle classe PSSI ? | 2.4 |
| **4. Accès et connecteurs** | L'outil peut-il lire ou agir sur le SI ? Avec quels droits, et pour combien de temps ? | 2.5 |
| **5. Règle PSSI** | Quelle règle s'applique ? Est-elle respectée, enfreinte, ou muette ? | 2.6 |
| **6. Qualification** | Quelle gravité, quelle vraisemblance, quel niveau de risque ? | 2.7 |
| **7. Mesure** | Quelle mesure réduit le risque tout en répondant au besoin métier ? | 2.7 |

L'approbation d'un fournisseur ne prouve pas celle de tous ses produits et usages. Une règle ou une preuve absente doit être signalée comme **inconnue**, plutôt que supposée favorable ou défavorable. Les séquences indiquées sont celles du programme ; leurs activités ne sont pas préparées ici avant réception des consignes.

## Le concept

Le **shadow IT** désigne, dans le cadre de cet exercice, un outil ou un service utilisé hors du cadre de validation de la DSI, comme un espace de partage sur un compte personnel. Le **shadow IA** en est une forme particulière : des usages d'intelligence artificielle restent inconnus de l'organisation et ne sont pas évalués.

Trois caractéristiques appellent une attention particulière :

- **Des données sont fournies au modèle.** Un assistant doit traiter un contenu pour répondre. Avec un service distant externe, les éléments transmis quittent le périmètre concerné ; avec un traitement réellement local, ils ne sortent pas nécessairement du SI. Conservation, télémétrie et réutilisation éventuelle dépendent du produit, de sa configuration et du contrat. **Les données ne sortent donc pas « par nature » dans tous les cas.**
- **L'IA peut apparaître dans un outil déjà validé.** Une mise à jour peut activer une fonction nouvelle dont les données traitées et les accès n'ont pas encore été examinés. Une validation ancienne ne couvre pas automatiquement cette évolution.
- **L'IA peut agir grâce à ses outils.** Certains assistants et agents peuvent lire des messages, écrire dans un dépôt ou envoyer des courriels selon les connecteurs et permissions accordés. Il faut examiner les capacités effectives du service utilisé.

L'[ANSSI, guide ANSSI-PA-102 du 29 avril 2024](https://messervices.cyber.gouv.fr/documents-guides/Recommandations_de_s%C3%A9curit%C3%A9_pour_un_syst%C3%A8me_d_IA_g%C3%A9n%C3%A9rative.pdf), traite notamment des données sensibles transmises aux services tiers (**R34**) et des droits des outils connectés (**R35**). La [CNIL recommande de définir un cadre d'usage et de vérifier les garanties du service](https://www.cnil.fr/fr/les-questions-reponses-de-la-cnil-sur-lutilisation-dun-systeme-dia-generative).

Le point de départ de l'analyse est le **besoin métier** : gagner du temps, dépanner un incident, traduire un contrat. Il ne faut pas présumer une intention malveillante ni attribuer tous les usages à une cause unique. Une réponse utile doit traiter le besoin et l'organisation, en plus des pratiques individuelles ; une interdiction sans solution peut laisser persister le motif du contournement.

## Vocabulaire clé

| Terme | Ce que c'est concrètement |
| --- | --- |
| **Usage approuvé** | L'outil, le compte et le périmètre d'usage ont été validés par la DSI ; cette validation ne dispense pas de respecter ses conditions. |
| **Usage déclaré non validé** | La DSI connaît la demande, mais l'autorisation manque ou reste en attente. L'absence de réponse ne vaut pas validation. |
| **Shadow IA** | Un usage professionnel de l'IA que l'organisation ignore et n'a pas évalué, selon la distinction retenue pour ce cours. |
| **IA embarquée** | Une fonction IA intégrée à un logiciel existant, éventuellement ajoutée ou activée par une mise à jour ; ce n'est pas en soi un statut d'approbation. |
| **Zone grise** | Les règles ou le périmètre de validation disponibles ne permettent pas de trancher clairement ; il faut demander une clarification. |
| **Besoin métier** | Ce que la personne cherche à accomplir. La mesure proposée doit permettre une réponse adaptée à ce besoin. |

## Mission 1 — Classement renseigné des situations

Le classement suivant est **proposé à partir des seuls énoncés**. Pour les situations 1 et 3, je retiens l'hypothèse d'un usage non déclaré. Pour 2 et 8, je suppose que l'usage décrit correspond bien au périmètre acheté et validé. Les situations 4, 5 et 7 demandent une clarification : une information manquante ne prouve pas à elle seule un usage caché.

| N° | Situation chez Hexalp | Classement retenu | Pourquoi l'usage échappe-t-il à la DSI, ou que faut-il vérifier ? |
| --- | --- | --- | --- |
| **1** | Une comptable traduit un contrat fournisseur avec la traduction automatique de son navigateur. | **Shadow IA**, sous l'hypothèse d'un usage non déclaré | La traduction paraît être une fonction ordinaire du navigateur et peut ne pas être identifiée comme un usage d'IA. Vérifier le moteur de traduction, le traitement local ou distant, le compte et les données du contrat. Si cet usage a déjà été approuvé, il faut le reclasser. |
| **2** | La communication utilise un générateur d'images acheté par la DSI, avec un contrat. | **Approuvé**, pour le périmètre décrit | L'outil n'échappe pas à la DSI dans l'hypothèse retenue. Vérifier que le compte, la finalité et les données utilisées correspondent à l'accord : le seul achat ne validerait pas tous les usages possibles. |
| **3** | Un technicien photographie l'écran d'erreur d'un trieur et l'envoie à un assistant sur son téléphone personnel. | **Shadow IA**, sous l'hypothèse d'un usage non déclaré | L'outil et l'appareil personnels peuvent rester hors des canaux de recensement de la DSI. La photographie peut révéler d'autres informations que le message d'erreur ; son contenu précis et la destination restent à examiner. |
| **4** | Le logiciel de paie, validé en 2021, propose désormais un assistant IA activé par défaut après mise à jour. | **Zone grise — IA embarquée** | L'approbation de 2021 ne permet pas de conclure sur la nouvelle fonction. Vérifier son usage effectif, ses flux, ses données et le périmètre contractuel. Si elle est utilisée à l'insu de l'organisation sans évaluation, cet usage relève alors du shadow IA. L'activation seule ne prouve pas un transfert de données. |
| **5** | Un développeur exécute un modèle open source sur son poste pour relire son code, sans connexion à Internet. | **Zone grise** | L'absence de réseau réduit ici le risque de transmission distante, mais ne prouve ni approbation ni innocuité du modèle et de ses dépendances. Vérifier le cadre d'installation, la provenance et les ressources nécessaires. Si l'usage est inconnu de la DSI, il doit être reclassé en shadow IA ; s'il est validé, en usage approuvé. |
| **6** | Une manageuse a demandé un outil de transcription à la DSI ; sans réponse depuis trois semaines, elle l'utilise. | **Déclaré non validé** | La DSI connaît la demande : l'usage n'est donc pas totalement invisible, même si son démarrage peut ne pas avoir été signalé. La demande en attente ne vaut pas accord. Vérifier les données des réunions et le suivi de la demande. |
| **7** | Un administrateur utilise « Se connecter avec Microsoft » avec son compte Hexalp pour accéder à un service d'IA. | **Zone grise** | L'authentification professionnelle ne prouve pas la validation du service ou de son usage. Vérifier si la DSI connaît l'application, les consentements et les droits accordés. Une connexion ne prouve pas non plus, à elle seule, un accès à la messagerie. Un usage inconnu et non évalué serait du shadow IA. |
| **8** | Le standard téléphonique transcrit les messages vocaux par IA ; cette fonction figure au contrat signé par la DSI. | **Approuvé**, pour le périmètre contractuel décrit | La fonction est identifiée dans le contrat, dans l'hypothèse retenue. Vérifier néanmoins les conditions opérationnelles : accès, conservation et périmètre des données. La présence d'IA ne rend pas cet usage automatiquement « shadow ». |

**Bilan du classement proposé :** **2 approuvés** (2, 8), **1 déclaré non validé** (6), **2 shadow IA sous hypothèse** (1, 3), **3 zones grises** (4, 5, 7). Ce décompte est une réponse pédagogique sur huit situations, pas une mesure des usages réels d'Hexalp.

### 1. Quelles situations m'ont fait hésiter ?

Les situations **4, 5 et 7** sont les plus ambiguës : logiciel anciennement approuvé, modèle local et compte professionnel peuvent donner une impression de maîtrise sans établir la validation du nouvel usage.

Mon critère est : **l'organisation connaît-elle cet usage précis et l'a-t-elle évalué et autorisé dans ce périmètre ?** Je sépare ensuite ce statut du risque technique. Un usage peut être approuvé tout en conservant un risque résiduel ; un modèle local peut présenter des risques sans envoyer de données à un fournisseur. La situation 6 m'oblige aussi à distinguer « connu » de « autorisé ».

### 2. Situation 6 : qui est responsable ?

**Selon le vocabulaire du cours, c'est d'abord un usage déclaré non validé**, et non la preuve d'un usage entièrement caché. La manageuse a exprimé son besoin, mais décide de commencer sans validation. Elle doit signaler ce démarrage et suivre le cadre applicable ; son choix de poursuivre ne transforme pas le silence de la DSI en autorisation.

L'organisation a aussi un problème à traiter : demande sans réponse, absence éventuelle de délai ou de solution provisoire et besoin de transcription toujours présent. La DSI et le responsable métier doivent organiser une décision et une réponse adaptée. Il s'agit d'une **analyse de responsabilités opérationnelles**, pas d'une conclusion juridique sur la faute d'une personne.

Pour Hexalp, je proposerais un suivi visible de la demande, un interlocuteur responsable, un délai de réponse annoncé et une solution transitoire validée pour les réunions éligibles. Ces mesures restent proposées, non déployées.

### 3. Samsung, printemps 2023 : que s'est-il passé ?

**Faits rapportés à l'époque :** des ingénieurs de Samsung ont transmis du code source interne à ChatGPT en avril 2023, notamment dans un contexte d'aide au travail. L'incident est décrit dans un [article de The National du 2 mai 2023](https://www.thenationalnews.com/business/technology/2023/05/02/samsung-electronics-bans-employee-use-of-chatgpt/). Il s'agit de données confiées à un service externe ; cette information ne prouve pas qu'elles ont été publiées ou restituées à d'autres utilisateurs.

**Réaction de l'entreprise :** selon la [dépêche AFP publiée par The Business Times le 2 mai 2023](https://www.businesstimes.com.sg/companies-markets/samsung-bans-use-chatgpt-mobile-appliances-staff), Samsung confirme une restriction dans sa division mobile et électroménager. Le mémo cité décrit une interdiction temporaire sur les ordinateurs de l'entreprise, dans l'attente d'un environnement d'usage sécurisé, et demande de ne pas téléverser d'informations professionnelles depuis des ordinateurs personnels. Cela ne permet pas de décrire cette mesure comme une interdiction définitive et uniforme de toute IA chez Samsung.

**A-t-elle fait disparaître les usages ? Mon analyse :** les sources consultées ne mesurent pas une disparition totale des usages après la restriction. Je ne peux donc pas l'affirmer. Une interdiction peut réduire les usages sur le périmètre contrôlé ; elle ne supprime pas automatiquement le besoin d'aide au développement. Sans alternative, des usages personnels moins visibles restent possibles : c'est une hypothèse de risque organisationnel, pas un contournement Samsung établi par ces articles.

Pour Hexalp, j'en retiens qu'il faut **identifier les données et les besoins, décider des usages permis et fournir une solution adaptée**, puis vérifier les pratiques. Une règle publiée n'est pas la preuve de son adoption effective.

## Ma définition corrigée après la section 2.1

### Définition initiale conservée

> Le shadow IA, c'est l'utilisation d'outils ou de fonctions d'intelligence artificielle dans le cadre du travail sans que l'organisation en ait connaissance ou en ait validé les conditions d'usage.

### Définition retenue pour la suite du cours

> **Le shadow IA désigne un usage professionnel de l'intelligence artificielle inconnu de l'organisation et non évalué par elle, qu'il passe par un service dédié, une fonction embarquée ou un modèle local.**

**Ce que je corrige :** mon premier « ou » mélangeait deux statuts. Un usage peut être **connu mais non validé** : il doit alors être recensé comme tel, sans être présenté comme ignoré. La **zone grise** désigne pour sa part une règle ou un périmètre ambigu à clarifier. Cette distinction est celle de l'exercice ; les terminologies peuvent varier entre organisations.

## Mission 2 — Appliquer la méthode dans les séquences suivantes

La grille des **sept étapes placée en tête de cette page** est celle à recopier dans le document « Shadow IA chez Hexalp ». À chaque étape, séparer **fait observé, hypothèse, preuve manquante et action proposée**. Une règle PSSI ne sera déclarée enfreinte qu'après identification de son texte et du périmètre d'application.

Les huit situations ci-dessus sont classées ; la définition est corrigée. Les comparatifs de comptes, le caviardage, l'écran InboxPilot et les autres travaux annoncés seront traités à partir de leurs consignes et pièces, sans inventer les éléments manquants.

## Ressources

- [CNIL — Questions-réponses sur l'utilisation d'un système d'IA générative](https://www.cnil.fr/fr/les-questions-reponses-de-la-cnil-sur-lutilisation-dun-systeme-dia-generative)
- [ANSSI — Recommandations de sécurité pour un système d'IA générative](https://messervices.cyber.gouv.fr/documents-guides/Recommandations_de_s%C3%A9curit%C3%A9_pour_un_syst%C3%A8me_d_IA_g%C3%A9n%C3%A9rative.pdf), **ANSSI-PA-102, v1.0, 29 avril 2024**, notamment § 5.7.

Sources consultées le **20 octobre 2026**. Les articles sur Samsung relatent les événements de **2023**, sans établir les pratiques ou la politique actuelles de l'entreprise.

[Retour à l'itération](index.md)
