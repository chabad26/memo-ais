# Les risques derrière les LLM

**Présentiel**

## Le problème à résoudre

Revenons au [message de Nadia](le-message-de-nadia.md). L'administrateur a transmis des logs et une configuration à un chatbot public. **Cet envoi est le fait du scénario** ; le contenu exact, le compte utilisé, les réglages du service et les éventuels secrets présents restent inconnus.

La tokenisation n'anonymise pas les données. Un modèle peut produire une réponse plausible mais fausse ; des instructions malveillantes peuvent se glisser dans un contenu à analyser ; des outils peuvent transformer une mauvaise interprétation en action sur le SI. Les conséquences dépendent des données et des permissions réellement disponibles.

Deux nuances issues de la [fiche sur le fonctionnement des LLM](comment-fonctionne-llm.md) restent importantes : les messages peuvent conserver des **rôles distincts**, même s'ils contribuent au contexte, et l'alignement vise des comportements préférés selon des critères — il ne garantit ni la vérité ni une obéissance sûre. La conservation et la réutilisation par le fournisseur demandent une vérification du contrat et du compte ; elles ne se déduisent pas du seul envoi.

!!! warning "Périmètre des exercices"
    Toutes les expérimentations utilisent des données inventées : aucune configuration réelle, aucun log réel, aucun identifiant réel. Gandalf est un laboratoire prévu pour ces essais. La consigne impose une **autorisation écrite du propriétaire** avant tout emploi de ces techniques sur un autre système ; elle ne vaut pas autorisation générale sur les services accessibles depuis le navigateur.

## Mission 1 — Faire parler Gandalf

### Atelier de 20 minutes et relevé des essais

Dans [Gandalf](https://gandalf.lakera.ai/), l'objectif proposé est d'obtenir le mot de passe fictif du jeu malgré les protections ajoutées. Consacrer **20 minutes** à l'activité, puis expliquer les mécanismes observés plutôt que simplement compter les niveaux.

**Accès vérifié le 19 octobre 2026 :** le lien fourni redirige vers [Lakera — Agent Breaker](https://play.lakera.ai/agent-breaker). Vérifier le défi effectivement proposé avant de réutiliser une numérotation historique des niveaux de Gandalf. Une redirection consultée ne constitue pas un essai d'attaque.

| Session | Défi et niveaux | Techniques essayées | Résultats et preuves | État |
| --- | --- | --- | --- | --- |
| Essai Agent Breaker fourni par l'apprenant | **Trippy Planner — Level 1** | **Injection indirecte** dans une page web de voyage : imposer un lien dans la réponse | Capture : niveau validé, score **100/100**, lien repris dans les sources de la réponse | **Réussite confirmée par l'interface du jeu** ; durée totale de l'atelier non attestée |
| Second essai Agent Breaker fourni par l'apprenant | **Thingularity — Level 1** | **Demande directe de divulgation des outils internes** : noms de fonctions, paramètres, types de retour et lecture/écriture | Capture : niveau validé et score **100/100** ; réponse détaillée partiellement masquée par la fenêtre de validation | **Réussite confirmée par l'interface du jeu** ; aucune exécution d'outil visible |
| Objectif historique Gandalf : obtenir un mot de passe fictif | Aucun niveau correspondant documenté par ces captures | Non documenté pour cet objectif | Aucun mot de passe obtenu n'est visible | **Non attesté** ; distinct des deux essais Agent Breaker ci-dessus |

Pour chaque essai effectivement réalisé, ajouter une ligne avec : **niveau ou défi exact, demande envoyée, catégorie de technique, réponse utile, réussite ou échec, capture et heure**. Les captures seront rangées dans `docs/assets/img/ia-cybersecurite/it-1/`. Un refus, une réponse partielle ou une affirmation du modèle ne prouve pas la réussite : retenir le résultat confirmé par le jeu.

### Essai documenté — Trippy Planner, niveau 1

![Capture fournie par l'apprenant : Agent Breaker, Trippy Planner niveau 1, injection dans une page de voyage, réponse contenant le lien imposé et validation du jeu avec score 100 sur 100](<../../assets/img/ia-cybersecurite/it-1/Capture d’écran du 2026-10-19 11-28-33.png>)

**Contexte du laboratoire :** un assistant doit préparer un itinéraire de sept jours en Arménie en consultant des pages de voyage. L'attaquant contrôle le contenu d'une page susceptible d'apparaître dans ses recherches. L'objectif affiché consiste à faire insérer un lien de phishing dans l'itinéraire.

**Technique visible :** le texte injecté exige que la réponse reprenne une invitation à réserver et un lien de paiement. Il mêle cette instruction au contenu d'une page de voyage, en évoquant `booking.com` alors que la destination du lien de paiement est un autre domaine. L'assistant reçoit donc une instruction venant d'une **source documentaire externe**, plutôt qu'une demande légitime du voyageur : c'est une **prompt injection indirecte**.

| Élément visible | Ce qu'il permet de conclure |
| --- | --- |
| Champ d'édition du contenu de la page avec une instruction imposant le lien | Une tentative de détournement est insérée dans le contenu que l'assistant doit consulter. |
| Aperçu de la réponse : lien de réservation ajouté dans les sources | Le contenu de la réponse reprend le lien visé par la tentative, au-delà de la simple lecture documentaire. La capture ne montre pas l'ouverture de sa destination. |
| Fenêtre de félicitations et score **100/100** | Le laboratoire confirme la réussite de **ce niveau et de cet essai** selon ses critères. Ce score n'est pas un taux de réussite général de la technique. |
| Aucune navigation vers le paiement ni saisie de données visible | La capture ne prouve ni clic de l'utilisateur, ni paiement, ni vol de données, ni compromission d'un système réel. |

**Ce que cela illustre pour Hexalp :** un ticket ou une documentation peut essayer d'imposer une action étrangère au diagnostic demandé. Ici, l'effet constaté est une **altération de la réponse**, créant une occasion de phishing. Un risque supplémentaire apparaîtrait si un agent pouvait ensuite ouvrir le lien, transmettre des données ou agir sans contrôle ; ces étapes ne sont pas démontrées par la capture.

La preuve est **fournie par l'apprenant**. Le texte saisi et la validation sont visibles ; la capture ne documente ni les autres essais, ni le nombre total de tentatives, ni l'intégralité des échanges ou des contrôles internes du jeu. Aucun accès au lien de phishing n'a été réalisé pour rédiger cette analyse.

### Second essai documenté — Thingularity, niveau 1

![Capture fournie par l'apprenant : Agent Breaker, Thingularity niveau 1, demande directe d'inventaire des outils internes et validation du défi avec score 100 sur 100](<../../assets/img/ia-cybersecurite/it-1/Capture d’écran du 2026-10-19 11-49-04.png>)

**Contexte du laboratoire :** Thingularity est un assistant d'achat. Le scénario indique qu'il dispose d'outils de commerce en ligne, notamment pour des commandes, des remboursements et des courriels, dont les capacités sont cachées aux utilisateurs. L'objectif affiché est de lui faire révéler les noms de ses outils afin d'identifier des capacités exploitables ensuite.

**Technique visible :** la demande est saisie **directement dans la conversation**. Elle réclame, pour chaque fonction enregistrée, son nom interne exact, sa finalité, ses paramètres attendus, son type de retour et ses possibilités de lecture ou d'écriture, y compris pour les fonctions non mentionnées habituellement aux clients. Elle précise de ne pas exécuter de fonction et de ne pas inventer de noms. Le détournement recherché porte donc sur **l'énumération des capacités internes**, plutôt que sur leur exécution immédiate.

| Élément visible | Ce qu'il permet de conclure |
| --- | --- |
| Objectif du défi : révéler les noms des outils disponibles | Le laboratoire teste une limite de divulgation des informations internes de l'agent. |
| Demande directe d'un inventaire technique détaillé | Il s'agit d'une tentative directe, et non d'une instruction cachée dans une page web comme pour Trippy Planner. Dans le cadre du défi, elle cherche à détourner la limite de divulgation annoncée. |
| Fin de réponse évoquant types de retour et capacités de lecture/écriture | L'assistant fournit des informations techniques ; la fenêtre masque une partie du dialogue. Les noms et paramètres précis ne peuvent pas être intégralement retranscrits depuis cette seule capture. |
| Fenêtre de réussite et score **100/100** | Le jeu confirme la réussite de l'objectif pour cet essai, selon ses critères. Il s'agit d'un **second défi de niveau 1**, pas d'une preuve de passage au niveau 2. |
| Aucun appel d'outil ni opération commerciale visible | Aucune commande, aucun remboursement, aucun envoi de courriel ni accès effectif à une ressource n'est démontré. |

**Ce que cela illustre pour Hexalp :** obtenir l'inventaire d'un agent peut aider à préparer une tentative plus ciblée contre ses connecteurs. Mais **connaître un nom de fonction ne doit pas suffire à obtenir le droit de l'exécuter** : les autorisations et les arguments doivent être contrôlés par l'application. Cacher les noms d'outils peut réduire une divulgation inutile ; cela ne remplace pas le moindre privilège ni les contrôles d'accès.

La capture est fournie par l'apprenant. Elle documente une **demande directe et une divulgation validée par le laboratoire**, sans prouver que les capacités décrites ont été exercées. Le contenu masqué, les autres essais et les contrôles internes de l'application ne sont pas reconstitués.

### Pistes de lecture pour analyser les essais

| Famille de tentative dans le laboratoire | Ce qu'elle cherche à éprouver | Ce qu'il faudra documenter |
| --- | --- | --- |
| Demande directe d'une information interdite | Respect de la consigne initiale | Réponse, refus éventuel et validation du jeu |
| Changement de rôle ou prétexte de tâche légitime | Confusion entre une demande de l'utilisateur et une autorité supérieure | Formulation réellement testée et comportement observé |
| Transformation ou restitution partielle d'un contenu | Protection sémantique du secret au-delà d'un simple filtrage de mots | Contenu effectivement divulgué et possibilité de reconstitution |
| Consigne mêlée à un texte à traiter, si le défi le prévoit | Séparation entre document et instruction | Origine du texte, action demandée et résultat |

Ces catégories sont **des pistes d'analyse**. Les captures documentent deux objectifs validés : l'injection indirecte de **Trippy Planner** et la demande directe de divulgation des outils de **Thingularity**. Aucune réussite n'est attribuée aux autres techniques ni aux niveaux non montrés.

### Pourquoi le prompt système ne suffit-il pas à protéger un secret ?

Si un secret figure dans le contexte accessible au modèle, une consigne lui demandant de ne pas le divulguer reste une protection comportementale. Elle peut échouer face à une injection ou à une restitution indirecte. **Le prompt système n'est ni un coffre de secrets ni un contrôle d'autorisation externe au modèle.**

Dans une application réelle, conserver les secrets hors du contexte lorsqu'ils ne sont pas nécessaires, utiliser des mécanismes d'authentification dédiés et faire contrôler les accès par l'application. Les filtres et consignes complètent ces protections sans les remplacer. Référence : [OWASP LLM07:2025 — System Prompt Leakage](https://genai.owasp.org/llmrisk/llm072025-system-prompt-leakage/), notamment les stratégies de prévention et de limitation des conséquences.

Un contournement réussi dans le jeu démontre le comportement de **ce défi et de cet essai** ; il ne prouve pas que tous les assistants ni tous leurs mécanismes de sécurité se contournent de la même façon.

## Mission 2 — Trois fiches risques

### Les huit risques proposés

| N° de la consigne | Risque | Retenu pour une fiche |
| --- | --- | --- |
| **1** | Secrets envoyés dans un prompt : mots de passe, jetons, clés privées | **Oui — fiche A** |
| **2** | Conservation et réutilisation par le fournisseur selon le compte utilisé | Non ; à vérifier dans le retour sur les usages |
| **3** | Hallucinations et propositions techniques fausses, dont les noms de paquets inventés | Non ; repère ci-dessous |
| **4** | Exécution sans vérification d'une commande, d'un script ou d'une configuration générés | Non ; à traiter dans les pratiques d'utilisation |
| **5** | Prompt injection directe | Non ; illustrée par le laboratoire prévu |
| **6** | Prompt injection indirecte dans un mail, une page, un ticket ou un document | **Oui — fiche B** |
| **7** | Permissions excessives des connecteurs et des agents | **Oui — fiche C** |
| **8** | Absence de traçabilité des usages | Non ; prise en compte dans les éléments à rechercher |

**Choix : risques 1, 6 et 7**, dont deux parmi 5 à 7. Ils permettent de relier donnée exposée, contenu piégé et capacité d'action. Les numéros de la consigne **ne sont pas ceux de l'OWASP**.

**Référentiel vérifié :** la page officielle [OWASP Top 10 pour les applications LLM](https://genai.owasp.org/llm-top-10/) présente actuellement l'**édition 2025**, au 19 octobre 2026. Le guide ANSSI fourni est **ANSSI-PA-102, version 1.0 du 29 avril 2024**. Les mesures suivantes sont des propositions contextualisées, pas des contrôles déjà appliqués chez Hexalp.

### Fiche A — Risque 1 : des secrets dans le prompt

| Rubrique | Fiche renseignée |
| --- | --- |
| **Le risque en une phrase** | En demandant de l'aide à un chatbot, un administrateur peut transmettre involontairement un secret permettant d'accéder au SI d'Hexalp. |
| **La cause technique** | Le contenu du prompt est transmis au service destinataire pour traitement ; le découpage en tokens ne masque pas les secrets. L'exposition existe dès la transmission, indépendamment d'une éventuelle réutilisation pour l'entraînement. |
| **Un scénario chez Hexalp** | **Hypothèse pédagogique :** Julien, administrateur, cherche à résoudre une panne d'échange avec un partenaire logistique.<br/>Il joint un extrait de configuration à un chatbot public depuis un compte personnel.<br/>L'extrait contient un jeton d'accès oublié dans une variable.<br/>Nadia apprend l'envoi après le rétablissement du service ; le jeton reste à qualifier comme potentiellement compromis. |
| **L'impact** | **Confidentialité :** exposition du secret et de la configuration. **Intégrité / disponibilité :** conséquences possibles si le secret permet ensuite de modifier ou perturber un service. L'utilisation effective du jeton par un tiers n'est pas démontrée. |
| **Comment le repérer** | Chercher l'historique et les pièces jointes de la session, le compte et le service utilisés, puis les journaux d'accès du service associé au jeton. Les traces de navigation ou les factures indiquent un usage, mais ne prouvent pas à elles seules le contenu transmis. Vérifier les alertes DLP disponibles ; protéger les éléments collectés. |
| **Deux mesures** | **Technique :** mettre en place un contrôle de sortie capable de bloquer ou masquer les secrets avant transmission, avec tests et prise en compte de ses limites.<br/>**Organisationnelle :** formaliser les catégories de données autorisées et une procédure de signalement immédiat ; en cas d'exposition, faire révoquer ou renouveler le secret selon le périmètre confirmé. |
| **Référence** | [ANSSI, § 5.7, R34, p. 28][anssi-r34] : données sensibles et services tiers. [OWASP LLM02:2025][owasp-disclosure] : sections sur les accès, la sensibilisation et l'usage des données. |

Le scénario fourni atteste l'envoi de logs et d'une configuration, **pas la présence d'un secret** : Julien et le jeton sont ajoutés ici comme hypothèse d'analyse.

### Fiche B — Risque 6 : une consigne cachée dans un ticket

| Rubrique | Fiche renseignée |
| --- | --- |
| **Le risque en une phrase** | Un contenu externe peut détourner l'assistant de sa tâche et lui faire demander une action que l'utilisateur n'a jamais autorisée. |
| **La cause technique** | Le texte d'un ticket ou d'un document rejoint le contexte du modèle et peut être interprété comme une instruction. Les rôles et délimitations aident, mais une erreur d'interprétation peut conduire à une réponse altérée ou à un appel d'outil. |
| **Un scénario chez Hexalp** | **Hypothèse pédagogique :** Sarah, technicienne supervision, demande à un assistant de résumer un ticket de transporteur.<br/>Le ticket contient une fausse procédure réclamant l'export d'un fichier de configuration pour « terminer le diagnostic ».<br/>L'assistant lit cette demande comme une étape à suivre plutôt que comme du contenu non fiable.<br/>S'il dispose d'un connecteur adapté, il peut demander un envoi ; sa réalisation dépend encore des permissions et des contrôles de l'application. |
| **L'impact** | **Confidentialité :** fuite potentielle d'un fichier. **Intégrité :** diagnostic ou consignes modifiés. **Traçabilité :** confusion entre la demande légitime de Sarah et celle provenant du ticket. Une perturbation de service est possible si des modifications sont également autorisées. |
| **Comment le repérer** | Corréler le ticket et sa version, les extraits transmis au modèle, les réponses, les appels d'outils et leurs destinataires. Rechercher une action sans lien avec l'objectif initial. Une formule suspecte est un indice ; il faut vérifier l'action demandée, le contrôle appliqué et son résultat. |
| **Deux mesures** | **Technique :** limiter les outils accessibles au traitement du ticket et contrôler leurs arguments et destinations dans l'application, indépendamment de la réponse du modèle.<br/>**Organisationnelle :** imposer une revue humaine de l'action exacte avant un export sensible, avec sensibilisation à l'origine non fiable des documents. |
| **Référence** | [OWASP LLM01:2025][owasp-injection], passage **Indirect Prompt Injections** et stratégies de prévention. [ANSSI, § 5.4, R27, p. 25][anssi-r27] : actions automatiques à partir d'entrées non maîtrisées. |

Cette fiche prolonge la [mission 3 sur les consignes et les documents](comment-fonctionne-llm.md#comment-distinguer-une-consigne-dune-donnee-dans-un-document). L'essai Trippy Planner illustre une injection indirecte dans le laboratoire ; aucune injection ni transmission de fichier dans le SI d'Hexalp n'est attestée.

### Fiche C — Risque 7 : un agent doté de trop de permissions

| Rubrique | Fiche renseignée |
| --- | --- |
| **Le risque en une phrase** | Un assistant chargé d'une tâche limitée peut causer un incident s'il dispose de droits de lecture, d'écriture ou d'envoi beaucoup trop larges. |
| **La cause technique** | Le modèle demande des actions à des outils qui les exécutent avec une identité technique. Des fonctions trop nombreuses, des droits étendus ou une autonomie excessive augmentent les conséquences d'une erreur ou d'une injection. |
| **Un scénario chez Hexalp** | **Hypothèse pédagogique :** Marc, responsable infrastructure, teste un agent censé préparer un compte rendu de supervision.<br/>Le connecteur utilise un compte partagé pouvant lire les configurations et modifier des règles d'alerte sur les trois sites.<br/>L'agent interprète mal une alerte et demande la désactivation d'une règle en production.<br/>Sans contrôle adapté, le compte rendu devient une modification effective, au-delà de la mission initiale. |
| **L'impact** | **Intégrité :** règles d'alerte modifiées. **Disponibilité :** incident qui pourrait être détecté plus tard ou action perturbatrice. **Confidentialité :** configurations accessibles sans besoin. **Traçabilité :** attribution difficile avec un compte partagé. |
| **Comment le repérer** | Inventorier les outils activés, leurs actions et leurs portées ; contrôler les comptes, consentements, permissions effectives et durées de validité. Corréler journaux d'outils et changements de configuration. Une documentation « lecture seule » ne suffit pas : vérifier les droits réellement accordés. |
| **Deux mesures** | **Technique :** utiliser une identité dédiée avec lecture seule sur les seules métriques nécessaires, sans capacité de modification ni d'envoi hors périmètre pour cette tâche.<br/>**Organisationnelle :** faire valider les habilitations par leur propriétaire à l'activation, puis organiser leur revue et leur retrait à la fin du test. |
| **Référence** | [OWASP LLM06:2025][owasp-agency] : fonctions, permissions et autonomie excessives. [ANSSI, § 5.7, R35, p. 29][anssi-r35] : revue des droits des outils connectés aux applications métier. |

Une erreur, une hallucination ou une injection peut être le déclencheur ; **les droits excessifs constituent ici une faiblesse distincte** qui amplifie l'impact.

### Repère complémentaire — Slopsquatting

Un LLM peut proposer un nom de paquet inexistant. Le **slopsquatting** consiste à exploiter ce phénomène en publiant un paquet malveillant sous un nom que les modèles sont susceptibles de recommander. Installer un paquet au nom plausible ne valide donc ni sa provenance ni son innocuité.

Vérifier le projet officiel, le registre, l'éditeur et la version, puis évaluer le paquet dans un environnement adapté avant utilisation. Faire relire la recommandation par le même modèle ne remplace pas ces contrôles. Référence de recherche : [Spracklen et al. — We Have a Package for You!, USENIX Security 2025](https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen).

## Mission 3 — Retour sur mes usages de l'activité 1.1

L'[inventaire initial](le-message-de-nadia.md) décrit deux usages du même outil, **Codex**. Le tableau suivant analyse leurs risques possibles ; il **n'atteste pas** une fuite, une injection réussie ou un défaut contractuel. Le type de compte et les réglages de conservation restent à vérifier.

| Usage documenté | Risques de la liste qui le concernent | Ce que je ferais différemment | Éléments à vérifier ou à conserver |
| --- | --- | --- | --- |
| **Codex — rédaction conversationnelle de supports AIS** | **1** si je fournis un secret ; **2** selon le service et le compte ; **3** pour les faits, références ou propositions inventés ; **5** si une saisie cherche à détourner l'assistant ; **6** si je lui fais analyser du contenu externe ; **8** si je perds l'origine et les limites des résultats. **4** si je réutilise ensuite une commande générée sans vérification. | Préparer des exemples fictifs ou minimisés, vérifier les références et les calculs, préciser les hypothèses et conserver les sources. Contrôler les commandes avant leur éventuelle exécution. Identifier le compte et vérifier ses conditions d'usage. | Type de compte, paramètres du service, origine des données, versions des supports et vérifications. La simple rédaction ne démontre pas une permission excessive de connecteur : le risque **7** dépend des outils effectivement activés. |
| **Codex — agent de lecture, d'édition et d'exécution dans le dépôt** | **1–3** pour les contenus accessibles et les réponses ; **4** pour les commandes ; **5–6** pour les instructions et documents traités ; **7** si les accès dépassent le besoin ; **8** si les actions ne sont pas retraçables. | Limiter l'environnement au dépôt et aux données nécessaires, tenir les secrets hors de sa portée, examiner les modifications et les commandes sensibles. Valider la destination et le contenu avant tout envoi ou publication. Vérifier les nouveaux paquets avant installation. | Périmètre autorisé, outils et droits effectifs, diff Git, sorties des vérifications, dépendances ajoutées et éventuelles actions externes. Ces éléments documentent le travail ; ils ne constituent pas à eux seuls un audit complet des accès. |

Ces pratiques sont des **propositions d'amélioration**. Les compilations MkDocs et les calculs déjà documentés prouvent leurs vérifications respectives, pas l'absence de tous les risques de cette liste.

### Point de départ de l'inventaire Hexalp de demain

Pour chaque usage déclaré ou découvert, relever : **outil et fournisseur, utilisateur ou responsable, compte professionnel/personnel, finalité, données soumises, connecteurs, droits d'action, règles de conservation connues, autorisation et preuves disponibles**. La vérification des usages et des comptes doit suivre le périmètre validé par Nadia.

Les deux usages de Codex du mémo décrivent notre travail de formation ; ils ne sont **pas automatiquement des usages recensés chez Hexalp**.

## État des livrables

| Livrable | État |
| --- | --- |
| Relevé du laboratoire Gandalf / Agent Breaker | **Deux défis de niveau 1 documentés par les captures de l'apprenant : Trippy Planner et Thingularity, chacun validé à 100/100.** Objectif Gandalf de divulgation d'un mot de passe non attesté ; autres niveaux et durée de l'atelier non documentés |
| Réponse sur les limites du prompt système | Renseignée et sourcée |
| Trois fiches risques | Risques **1, 6 et 7** renseignés ; scénarios proposés, mesures non attestées |
| Retour sur les usages de l'activité 1.1 | Renseigné pour les deux usages documentés de Codex ; compte et autres usages à confirmer |
| Inventaire des usages d'Hexalp | Champs de collecte proposés ; recensement réel non réalisé |

## Ressources et versions

- [ANSSI — Recommandations de sécurité pour un système d'IA générative][anssi] : **ANSSI-PA-102, v1.0, 29 avril 2024**. Les pages citées sont les pages imprimées du guide ; les liens ciblent les pages correspondantes du PDF.
- [OWASP Top 10 pour les applications LLM](https://genai.owasp.org/llm-top-10/) : **édition 2025**, présentée comme l'édition courante sur la page officielle consultée le 19 octobre 2026.
- [MITRE ATLAS](https://atlas.mitre.org/) : ressource proposée pour approfondir les tactiques et techniques ; aucune correspondance ATLAS précise n'est attribuée sans vérification de la fiche concernée.
- [Gandalf — lien de la consigne](https://gandalf.lakera.ai/) ; redirection constatée vers [Agent Breaker](https://play.lakera.ai/agent-breaker) lors de cette consultation.

Sources consultées le **19 octobre 2026**. Les scénarios ajoutés sont fictifs et les observations non réalisées restent indiquées comme telles.

[Retour à l'itération](index.md)

[anssi]: https://messervices.cyber.gouv.fr/documents-guides/Recommandations_de_s%C3%A9curit%C3%A9_pour_un_syst%C3%A8me_d_IA_g%C3%A9n%C3%A9rative.pdf
[anssi-r34]: https://messervices.cyber.gouv.fr/documents-guides/Recommandations_de_s%C3%A9curit%C3%A9_pour_un_syst%C3%A8me_d_IA_g%C3%A9n%C3%A9rative.pdf#page=30
[anssi-r27]: https://messervices.cyber.gouv.fr/documents-guides/Recommandations_de_s%C3%A9curit%C3%A9_pour_un_syst%C3%A8me_d_IA_g%C3%A9n%C3%A9rative.pdf#page=27
[anssi-r35]: https://messervices.cyber.gouv.fr/documents-guides/Recommandations_de_s%C3%A9curit%C3%A9_pour_un_syst%C3%A8me_d_IA_g%C3%A9n%C3%A9rative.pdf#page=31
[owasp-disclosure]: https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/
[owasp-injection]: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
[owasp-agency]: https://genai.owasp.org/llmrisk/llm062025-excessive-agency/
