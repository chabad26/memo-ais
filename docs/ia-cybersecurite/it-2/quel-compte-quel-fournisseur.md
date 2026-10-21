# Quel compte, quel fournisseur ?

## Le problème à résoudre

Un même modèle peut être utilisé sous plusieurs contrats. Pour savoir ce que deviennent les données, il faut examiner **l'offre, le contrat, les réglages et les fonctions utilisées**, puis identifier qui contrôle le compte. Le nom du modèle et le prix de l'abonnement ne suffisent pas.

Cette fiche approfondit les étapes **1. Outil et fournisseur** et **2. Compte** de la [méthode d'analyse](shadow-ia-de-quoi-parle-t-on.md).

## Mission — Comparer les comptes

**Fournisseur retenu : OpenAI. Consultation des sources officielles : 20 octobre 2026.** Ce choix s'appuie sur les deux usages de Codex documentés dans [l'inventaire du J1](../it-1/le-message-de-nadia.md). Il ne démontre ni que ce fournisseur est le plus utilisé sur le mois, ni quelle offre ou quels réglages sont effectivement utilisés : ces informations restent **à vérifier**.

Le tableau compare les offres ChatGPT, l'API OpenAI et un déploiement local possible de gpt-oss. **Le local est un mode de déploiement, pas un type de compte cloud.** Il ne consiste pas à télécharger les modèles propriétaires du service ChatGPT.

| Type de compte | Données utilisées pour l'entraînement ? | Durée de conservation | Qui administre le compte ? | Que devient l'historique au départ du salarié ? | Contrat avec l'entreprise ? |
| --- | --- | --- | --- | --- | --- |
| **Gratuit personnel — ChatGPT Free** | Utilisation possible selon les réglages ; désactiver « Improve the model for everyone » exclut les nouvelles conversations de l'entraînement. [S1] | Conversations ordinaires jusqu'à suppression ; suppression des systèmes normalement sous 30 jours, avec exceptions. [S2] | Titulaire individuel ; la DSI n'en a pas automatiquement la maîtrise. | Le départ d'Hexalp ne déclenche pas, à lui seul, une suppression ou un transfert : accès et historique restent liés au compte personnel. | Pas de contrat d'entreprise établi par la seule utilisation personnelle ; relation individuelle à distinguer d'un achat au nom d'Hexalp. |
| **Payant personnel — ChatGPT Plus / Pro** | Payer ne garantit pas l'exclusion de l'entraînement : contrôler les réglages comme pour le personnel gratuit. [S1] | Même principe pour les conversations ordinaires : jusqu'à suppression, puis normalement sous 30 jours, avec exceptions. [S2] | Titulaire individuel ; remboursement et adresse professionnelle ne prouvent pas une administration DSI. | Même problème de continuité : aucune récupération automatique par Hexalp du seul fait d'avoir payé les frais. | L'abonnement personnel ne prouve pas un contrat passé au nom d'Hexalp. |
| **Offre entreprise — ChatGPT Business / Enterprise** | Pas d'entraînement sur les données métier par défaut. [S3] | **Enterprise :** politique de conservation de l'espace configurable. **Business :** le retrait d'un membre conserve ses conversations, fichiers et canvas sans limite de durée annoncée ; suppression du contenu à traiter séparément. [S4] | Propriétaires et administrateurs de l'espace, désignés par l'organisation. | Retrait = révocation de l'accès. Conservation selon l'offre et la politique ; ce n'est pas une suppression automatique, ni un transfert général des conversations à un successeur. [S4] | Oui si Hexalp est le client contractant de l'espace ; vérifier les conditions et engagements applicables. [S3] |
| **API OpenAI** | Non par défaut ; partage volontaire possible. [S5] | Journaux de contrôle des abus : jusqu'à 30 jours par défaut, avec exceptions ; données applicatives selon la fonction, parfois jusqu'à suppression. [S5] | Propriétaires de l'organisation et responsables des projets ; maîtrise Hexalp seulement si organisation, facturation et habilitations sont gérées par elle. | Pas d'historique ChatGPT automatique : données de l'application et objets API à gérer. Révoquer les accès individuels et traiter les clés ; le départ ne supprime pas toutes les données. | Possible sous contrat professionnel ; une clé issue d'un compte personnel ne démontre pas un contrat maîtrisé par Hexalp. |
| **Modèle exécuté en local — par exemple gpt-oss** | Les prompts ne sont pas automatiquement envoyés au fournisseur pour entraîner ses modèles si toute la chaîne fonctionne réellement en local. Une éventuelle réutilisation interne dépend du déploiement. | Définie par Hexalp : interface, journaux, caches et sauvegardes ; aucune durée universelle de « zéro conservation ». | Administrateurs du poste ou du serveur et de l'application ; sur un poste personnel, la DSI peut ne rien maîtriser. | Dépend du stockage et de la procédure de départ : récupérer les données métier autorisées, fermer les accès et appliquer la politique de conservation. | Licence du modèle et conditions des logiciels à vérifier ; le téléchargement ne crée pas à lui seul un contrat SaaS d'entreprise. [S6] |

### Sources du tableau et précisions

- **[S1]** [OpenAI — Data Controls FAQ](https://help.openai.com/en/articles/7730893-data-controls-faq) : désactivation de l'entraînement et application aux nouvelles tâches Codex des offres personnelles. Codex possède aussi un réglage distinct concernant l'entraînement sur les environnements complets : vérifier les deux périmètres.
- **[S2]** [OpenAI — Chat and file retention in ChatGPT](https://help.openai.com/en/articles/8983778-chat-and-file-retention-in-chatgpt) : archivage ≠ suppression ; exceptions de sécurité, obligations légales ou données déjà désidentifiées et dissociées du compte. Une copie de fichier conservée dans Library doit être supprimée séparément du chat.
- **[S3]** [OpenAI — Enterprise privacy](https://openai.com/enterprise-privacy/) : engagements pour les offres professionnelles et contrôles de l'organisation.
- **[S4]** [OpenAI — Data retention when a member is removed](https://help.openai.com/en/articles/8266418-data-retention-when-a-member-is-removed-from-a-workspace) : distinction entre retrait d'accès et suppression du contenu. [Confidentialité dans Business](https://help.openai.com/en/articles/8798634-managing-data-sharing-and-privacy-in-chatgpt-business) : administrer un espace ne rend pas automatiquement tous les chats lisibles par les autres membres.
- **[S5]** [OpenAI — Data controls in the API](https://developers.openai.com/api/docs/guides/your-data) : conservation des journaux et des états applicatifs à examiner séparément. Des fonctions persistantes gardent leurs données jusqu'à suppression ; Zero Data Retention exige une éligibilité et une approbation, avec limites par fonction.
- **[S6]** [OpenAI — Exécuter gpt-oss localement avec Ollama](https://developers.openai.com/cookbook/articles/gpt-oss/run-locally-ollama) : exemple de déploiement local ; ne démontre pas qu'un tel modèle est installé chez Hexalp.

!!! note "Entraînement, historique et conservation sont trois questions différentes"
    Désactiver l'entraînement ne supprime pas l'historique. Un chat temporaire non enregistré peut encore être conservé jusqu'à 30 jours pour la sécurité. Les fichiers, journaux et services connectés peuvent suivre d'autres règles. Sources : [contrôles de données](https://help.openai.com/en/articles/7730893-data-controls-faq) et [conservation](https://help.openai.com/en/articles/8983778-chat-and-file-retention-in-chatgpt).

## Réponses aux questions

### 1. Pourquoi « payant » ne veut-il pas dire « professionnel » ?

Le prix achète des fonctionnalités ou une capacité d'usage. Il ne prouve ni un contrat au nom d'Hexalp, ni une administration centralisée, ni une politique de conservation adaptée. **Une offre personnelle payante reste à évaluer comme telle**, notamment pour l'entraînement, les accès et le départ du salarié. Les engagements professionnels sont à vérifier dans l'offre et le contrat retenus. [Sources : S1 et S3 ci-dessus.]

### 2. Que change le remboursement d'un abonnement personnel ?

Une note de frais prouve un remboursement ; elle ne prouve ni le transfert du compte à Hexalp, ni l'attribution de droits d'administration à la DSI. **Le contrôle opérationnel du compte personnel et de son historique reste chez son titulaire**, sauf mécanisme contractuel ou migration effectivement établi. La propriété des documents métier est une autre question : on ne peut pas la déduire de la facture seule.

Au départ, Hexalp risque de perdre l'accès à des éléments utiles tandis que des données de l'entreprise restent dans le compte. La mesure proposée est un espace professionnel administré par Hexalp, avec conservation des livrables utiles dans son référentiel documentaire et procédure de départ. On ne récupère pas le mot de passe personnel du salarié pour organiser cette continuité. Pour un espace professionnel, appliquer les règles de retrait et de conservation documentées en [S4].

### 3. Une clé API personnelle devient-elle acceptable parce que les données ne servent pas à l'entraînement ?

**Non, cette garantie ne suffit pas.** Il reste à identifier l'organisation facturée, les personnes capables de révoquer la clé, les droits accordés, les données conservées et le lieu de stockage du secret. Une clé personnelle peut laisser Hexalp dépendante d'un salarié et exposer des données via une application mal configurée.

**Mesure proposée pour Hexalp :** organisation et projet gérés par l'entreprise, facturation identifiée, identité technique adaptée, droits limités, clé stockée dans un gestionnaire de secrets, suivi de consommation et procédure de rotation/révocation. Ne pas conserver la clé dans un dépôt Git, un prompt ou des journaux. Vérifier séparément la rétention des fonctions utilisées : l'absence d'entraînement n'est pas une promesse de zéro stockage. [Documentation API, S5.]

### 4. Avec un modèle local, quels risques disparaissent et lesquels restent ?

Si l'inférence, l'interface et le stockage sont entièrement internes, sans télémétrie de contenu ni service externe, **l'envoi des prompts au fournisseur pour cette inférence est évité**. Cela réduit l'exposition liée au traitement distant ; il faut vérifier les flux, les extensions et les connecteurs pour confirmer cette condition.

Restent les erreurs et hallucinations, la prompt injection, les permissions excessives d'un agent, les vulnérabilités du moteur et des dépendances, la provenance des fichiers du modèle, les accès au poste, les journaux et sauvegardes, ainsi que le coût en ressources. Hexalp doit donc gérer les habilitations, les mises à jour, la provenance des composants, les flux réseau et la conservation. **Local ne signifie pas automatiquement approuvé ni sécurisé.** Le déploiement local est documenté en [S6] ; ces mesures sont des propositions pour le scénario, pas des contrôles constatés chez Hexalp.

## Deux points de vigilance

!!! note "Politiques changeantes : préciser le choix proposé à l'utilisateur"
    L'annonce Anthropic du **28 août 2025** décrit un choix d'utilisation des données pour l'entraînement sur les offres grand public Free, Pro et Max, modifiable dans les réglages. Elle annonce une conservation étendue à cinq ans si l'utilisateur accepte cette utilisation. Elle ne permet pas d'affirmer que toutes les conversations de tous les comptes sont automatiquement utilisées. Dater la source et vérifier le réglage réel évite ce raccourci. [Annonce officielle Anthropic](https://www.anthropic.com/news/updates-to-our-consumer-terms), consultée le 20 octobre 2026.

!!! warning "L'authentification Microsoft n'est pas une validation DSI"
    « Se connecter avec Microsoft » indique un mécanisme d'authentification. Ce bouton ne prouve ni l'approbation de l'outil, ni l'existence d'un contrat adapté, ni à lui seul un accès aux mails. Examiner séparément l'application, son consentement et ses permissions : ce sera l'objet de la séquence sur les connecteurs.

## Retour sur les usages documentés

| Usage du J1 | Fournisseur | Offre / espace réellement utilisé | Point à vérifier avant transposition chez Hexalp |
| --- | --- | --- | --- |
| Codex pour rédiger et expliquer les fiches | OpenAI | À vérifier ; personnel ou professionnel non établi | Offre, contrat, réglages d'entraînement et conservation des contenus |
| Codex agent pour lire/modifier le dépôt et lancer les vérifications | OpenAI | À vérifier ; administration et réglages non établis | Points précédents, réglage propre aux environnements Codex, périmètre des fichiers accessibles et permissions d'exécution |

Aucun paramètre réel du compte n'a été inspecté ou modifié pour cette fiche. La comparaison est documentaire ; elle ne vaut pas validation DSI de ces usages.

## Ressources complémentaires

- [Google — Guide sur la confidentialité des applications Gemini](https://support.google.com/gemini/answer/13594961?hl=fr) : autre fournisseur à étudier avec la même méthode, sans lui transposer le tableau OpenAI.
- [Retour à la méthode en sept étapes](shadow-ia-de-quoi-parle-t-on.md)
- [Retour à l'itération 2](index.md)
