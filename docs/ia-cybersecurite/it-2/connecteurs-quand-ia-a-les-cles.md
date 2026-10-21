# Les connecteurs : quand l'IA a les clés

## Le concept

Un **connecteur** permet à un assistant d'interroger un service : messagerie, agenda, documents ou dépôt de code. Avec OAuth, un consentement peut autoriser une application à obtenir des jetons ; selon les droits et le flux utilisés, l'accès peut continuer sans nouvelle interaction de l'utilisateur.

L'assistant **peut accéder au périmètre autorisé**, sans nécessairement tout lire à chaque demande. Un mail ou un document récupéré peut contenir une injection indirecte. Par ailleurs, une connexion du fournisseur vers Microsoft 365 peut se faire **de serveur à serveur** : le proxy des postes d'Hexalp ne voit alors pas ce flux. Il faut aussi examiner les journaux d'identité, de consentement et d'activité du service.

Cette fiche approfondit l'étape **4. Accès et connecteurs** de la [méthode](shadow-ia-de-quoi-parle-t-on.md).

## Vocabulaire clé

| Terme | Ce que c'est concrètement |
| --- | --- |
| **Connecteur** | Intégration permettant à l'assistant d'accéder à un service ; sa durée dépend du mécanisme et des autorisations |
| **Consentement OAuth** | Accord sur les permissions demandées par une application ; ne vaut pas validation métier ou sécurité |
| **Portée — scope** | Permission précise ; en accès délégué, l'application agit dans le contexte d'un utilisateur |
| **Jeton d'accès** | Justificatif présenté à l'API, avec une durée de validité limitée |
| **Jeton d'actualisation** | Permet d'obtenir de nouveaux jetons d'accès ; `offline_access` permet de demander cet accès prolongé dans les flux concernés |
| **MCP** | Model Context Protocol : protocole ouvert pour intégrer outils et sources de contexte ; il ne garantit pas la sûreté du serveur ou de ses permissions |
| **Agent** | Assistant qui choisit et enchaîne des actions avec ses outils dans une boucle |

Références : [Microsoft — Jetons d'actualisation](https://learn.microsoft.com/en-us/entra/identity-platform/refresh-tokens) et [présentation officielle de MCP](https://modelcontextprotocol.io/). **Sources consultées le 20 octobre 2026.**

## Mission 1 — L'écran de consentement d'InboxPilot

**Scénario fictif :** une commerciale envisage InboxPilot, éditeur non vérifié, pour « résumer vos mails et préparer vos réponses ». L'écran fourni demande `User.Read`, `Mail.ReadWrite`, `Mail.Send`, `Files.Read.All`, `Calendars.ReadWrite` et `offline_access`.

L'analyse suppose des **permissions Microsoft Graph déléguées**, cohérentes avec un consentement utilisateur. Des permissions applicatives sans utilisateur auraient un autre périmètre et nécessiteraient une analyse distincte. « Éditeur non vérifié » ne prouve pas une application malveillante, mais justifie une vérification de son identité et de ses engagements avant approbation.

### Tableau renseigné

| Permission | Nécessaire pour résumer des mails ? | Ce qu'elle permet si l'assistant reçoit un mail piégé |
| --- | --- | --- |
| **User.Read** | Pas pour lire le contenu des mails ; peut être justifiée pour identifier l'utilisateur connecté | Lire son profil de base et personnaliser une usurpation ; ne donne pas accès à toute la messagerie ni à tout l'annuaire |
| **Mail.ReadWrite** | **Excessive pour un résumé** : `Mail.Read` suffit normalement à lire le corps des messages | Lire, créer, modifier ou supprimer des messages dans la boîte autorisée ; préparer un brouillon malveillant. **N'autorise pas l'envoi à elle seule** |
| **Mail.Send** | **Non** ; préparer un texte de réponse n'exige pas de l'envoyer | Envoyer un message en tant qu'utilisateur, par exemple transmettre des données à l'extérieur ou usurper une demande métier |
| **Files.Read.All** | **Non pour résumer les mails** | Lire les fichiers auxquels l'utilisateur a accès, y compris des documents partagés accessibles ; ne confère pas accès à tous les fichiers du tenant |
| **Calendars.ReadWrite** | **Non** | Lire ou modifier des événements, créer ou supprimer des rendez-vous et exposer des informations d'agenda |
| **offline_access** | **Non pour un usage ponctuel** ; éventuellement justifiée pour un traitement de fond validé | Prolonger la capacité d'accès via renouvellement des jetons ; **n'ajoute pas de droit de lecture ou d'écriture** aux autres permissions |

Ces capacités ne sont pas des actions automatiquement déclenchées par la présence d'un mail piégé : elles deviennent exploitables si l'application interprète son contenu comme une instruction et dispose des outils correspondants. Référence des six permissions : [Microsoft Graph — Permissions reference](https://learn.microsoft.com/en-us/graph/permissions-reference).

### 1. Quelles permissions garder et quelles actions faire valider ?

Pour le besoin minimal, proposer **`Mail.Read`**, avec `User.Read` seulement si l'identification de session est nécessaire. `Mail.ReadBasic` ne suffit pas à résumer le corps des messages. Retirer les accès aux fichiers et calendriers ainsi que l'envoi. Refuser `offline_access` si une lecture ponctuelle suffit ; pour une synthèse planifiée, examiner ce besoin séparément et prévoir une révocation maîtrisée.

**Préparer des réponses peut signifier produire du texte dans l'interface**, sans droit d'écriture dans la boîte. Si le métier exige des brouillons Outlook, `Mail.ReadWrite` peut être justifiée, mais son étendue reste supérieure au seul droit « créer un brouillon ». Chercher un intermédiaire qui limite les opérations réellement exposées à l'agent.

Si l'envoi ou les modifications sont ensuite approuvés, exiger une validation humaine **avant l'appel effectif** pour chaque envoi, suppression ou modification à impact : afficher destinataires, contenu, pièces jointes et différences. Cette validation doit être imposée par l'application ou un contrôle extérieur au modèle, pas seulement demandée dans son prompt. Une confirmation ne corrige pas des permissions inutiles : les retirer d'abord.

**Décision proposée : annuler le consentement actuel**, puis demander une version aux droits réduits et une évaluation DSI du fournisseur, du contrat, de la conservation et des flux. Il ne s'agit pas d'une interdiction générale des assistants de messagerie.

### 2. Pourquoi « tous les fichiers accessibles » dépasse-t-il les fichiers de la commerciale ?

Ses droits peuvent inclure des bibliothèques SharePoint, des documents d'équipe et des fichiers partagés par des collègues. `Files.Read.All` délégué s'appuie sur ce périmètre existant : des partages trop larges augmentent l'exposition. **Ce n'est ni uniquement son OneDrive personnel, ni un accès automatique à tout le SI.** Vérifier les droits effectifs et réduire les partages excessifs avant connexion. [Microsoft Graph — Files.Read.All](https://learn.microsoft.com/en-us/graph/permissions-reference#filesreadall).

### 3. Changement de mot de passe et départ d'Hexalp

**Un changement de mot de passe par l'utilisateur ne garantit pas la coupure.** Microsoft distingue plusieurs types de jetons ; certains, notamment ceux de clients confidentiels, peuvent rester valides après ce changement. `offline_access` ne signifie toutefois pas un accès irrévocable : jetons et consentements peuvent être révoqués. [Microsoft — tableau de révocation des jetons](https://learn.microsoft.com/en-us/entra/identity-platform/refresh-tokens).

Au départ de la commerciale, appliquer une procédure : bloquer le compte, révoquer sessions et jetons, retirer les consentements et affectations concernés, puis vérifier les traces d'accès. Un jeton d'accès déjà délivré peut encore fonctionner jusqu'à expiration ou prise en compte d'une révocation selon le service et ses mécanismes. Si une application possède aussi des permissions applicatives indépendantes de l'utilisatrice, les traiter séparément. Les copies déjà envoyées au fournisseur ne disparaissent pas avec la fermeture du compte : leur suppression dépend aussi du contrat et de sa politique.

### 4. Où administrer les consentements ?

| Environnement | Voir les applications et permissions | Encadrer le consentement |
| --- | --- | --- |
| **Microsoft Entra ID** | Centre d'administration → **Entra ID → Applications d'entreprise → Toutes les applications → application → Autorisations** ; examiner consentement administrateur et utilisateur, puis journaux d'audit et de connexion | **Applications d'entreprise → Consentement et autorisations → Paramètres de consentement utilisateur** : désactiver le consentement autonome ou le limiter selon la politique ; prévoir une demande d'approbation administrateur |
| **Google Workspace** | Console d'administration → **Sécurité → Contrôle des accès et des données → Commandes des API → Gérer l'accès des applications tierces** ; examiner applications et accès demandés/accordés | Restreindre les services et configurer les applications autorisées ou bloquées ; examiner aussi le traitement des applications non configurées et les règles par population |

Les intitulés peuvent varier avec la langue et l'évolution des consoles. Prévoir les rôles administratifs adaptés. Sources : [Microsoft — examiner et révoquer les permissions](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/manage-application-permissions), [configurer le consentement utilisateur](https://learn.microsoft.com/fr-fr/entra/identity/enterprise-apps/configure-user-consent) et [Google — contrôler les applications accédant aux données Workspace](https://knowledge.workspace.google.com/admin/apps/control-which-apps-access-google-workspace-data).

Aucun accès à un tenant ni aucune modification de consentement n'ont été réalisés pour cette fiche.

## Mission 2 — Le cas EchoLeak

### Résumé — cinq lignes

1. **EchoLeak, CVE-2025-32711**, visait Microsoft 365 Copilot ; l'attaquant déposait des instructions piégées dans un mail externe.
2. Quand ce mail était récupéré pour répondre à une demande ordinaire, Copilot pouvait traiter ses instructions comme des consignes.
3. Des informations sensibles du contexte accessible à l'utilisateur pouvaient alors être intégrées à une URL dans la réponse.
4. Le chargement automatique d'une image, avec un relais Microsoft autorisé, pouvait transmettre ces données au serveur de l'attaquant, sans clic sur un lien malveillant.
5. Le cas a été divulgué en juin 2025 après correction côté service ; c'est une démonstration de vulnérabilité, pas une preuve ici d'exploitation chez Hexalp.

Source technique consultée : [étude de recherche EchoLeak, sections « Overview » et « Analysis »](https://arxiv.org/html/2509.10540v1). Elle analyse la chaîne publiée par Aim Labs ; elle ne constitue pas notre propre expérimentation. La [publication originale Aim Labs](https://www.aim.security/lp/aim-labs-echoleak-blogpost) a renvoyé une erreur d'accès lors de la consultation. La [fiche NVD demandée](https://nvd.nist.gov/vuln/detail/CVE-2025-32711) et l'[avis Microsoft MSRC](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-32711) restent les références d'identification ; leur détail n'a pas pu être extrait par l'outil de consultation.

### 1. Quel risque du J1 retrouve-t-on ?

Le **risque 6 : prompt injection indirecte**, car l'instruction vient d'un contenu externe récupéré par l'assistant. La conséquence est une divulgation d'informations ; l'étendue des outils et droits peut aggraver l'impact, comme dans le **risque 7**. Voir les [fiches risques du J1](../it-1/risques-derriere-llm.md).

### 2. Pourquoi les connexions aggravent-elles le risque ?

Elles mettent en relation une entrée non fiable — le mail externe — avec un contexte métier confidentiel et une possibilité de sortie. Des accès étendus et des partages excessifs augmentent le volume potentiellement exposé. **Copilot n'obtient pas pour autant tous les fichiers du tenant sans contrôle de droits**, et une lecture autorisée ne doit pas être confondue avec une autorisation de transmettre à un tiers.

Le moindre privilège limite l'impact, mais ne suffit pas : même un accès en lecture seule peut permettre une exfiltration par une sortie réseau ou une réponse. Il faut également contrôler les sources, les destinations et le traitement des contenus externes.

### 3. L'utilisateur a-t-il commis une faute ?

Le mécanisme décrit ne requiert pas de cliquer sur un lien malveillant ni de donner volontairement des secrets : une utilisation normale qui récupère le mail piégé pouvait suffire. **Le seul fait d'utiliser l'assistant ne permet donc pas d'attribuer une faute à l'utilisateur.** Cela ne signifie pas non plus que toute réception d'un mail déclenchait automatiquement une fuite : le contenu devait entrer dans le traitement vulnérable.

L'analyse doit répartir les actions correctives entre conception et correction du service, configuration des accès, contrôle des partages et surveillance de l'organisation. La responsabilité juridique d'un incident précis demanderait des faits et contrats supplémentaires ; elle n'est pas tranchée par ce scénario.

## À retenir — Excessive Agency

L'[OWASP LLM06:2025](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) distingue **trop de fonctions, trop de permissions et trop d'autonomie**. Chez Hexalp, la réponse proposée est donc : moins d'outils exposés, des droits adaptés au besoin et une validation humaine pour les actions à impact. Ni un prompt de prudence ni le bouton « Se connecter avec Microsoft » ne remplacent ces contrôles.

!!! warning "Pas de test avec un compte réel"
    InboxPilot est fictif. Ne pas tester un connecteur avec un compte d'entreprise ou d'école. Cette fiche est une analyse documentaire de l'écran fourni ; aucun consentement, envoi, appel API ou test d'exploitation n'a été effectué.

[Retour à l'itération 2](index.md)
