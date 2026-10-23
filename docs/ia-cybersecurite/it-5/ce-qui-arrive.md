# Ce qui arrive

**Séquence 5.4 — 1 h — Présentiel**

## Le problème à résoudre

La frise du J1 s’arrêtait à l’arrivée des agents. Une politique écrite aujourd’hui doit aussi tenir face aux évolutions de demain. Avant de rédiger celle d’Hexalp, examiner cinq évolutions récentes et leurs conséquences pour un administrateur d’infrastructure.

**Objectif :** transformer une information vérifiée en une règle applicable, avec un responsable, un contrôle et une preuve attendue.

## Mission et organisation

Chaque groupe choisit **un sujet différent de celui des autres groupes**, lit la source de départ, en recherche au moins une autre et remplit les trois rubriques de la fiche. Présentation : **deux minutes par groupe**. Ajouter ensuite une carte « 2025–2026 » à la [frise du J1](../it-1/70-ans-intelligence-artificielle.md).

Répartition indicative : 5 min de choix, 20 min de lecture croisée, 15 min de rédaction, 15 min de restitutions et 5 min pour la frise ; adapter le temps de restitution au nombre de groupes.

| N° | Sujet proposé | Point de départ et vigilance |
| --- | --- | --- |
| **1** | Des failles trouvées plus vite qu’on ne les corrige | [Project Glasswing — Anthropic](https://www.anthropic.com/glasswing), annoncé le **7 avril 2026** ; [bilan Help Net Security du 26 mai 2026](https://www.helpnetsecurity.com/2026/05/26/anthropic-project-glasswing-update/). Distinguer découvertes annoncées, vulnérabilités validées et correctifs déployés. |
| **2** | Des attaquants outillés par des agents | [MITRE ATT&CK C0062](https://attack.mitre.org/campaigns/C0062/) ; campagne de **septembre 2025**, [publication Anthropic du 13 novembre 2025](https://www.anthropic.com/news/disrupting-AI-espionage). Sujet retenu ci-dessous comme proposition de travail. |
| **3** | Un accès fournisseur qui peut changer brutalement | [Déclaration Anthropic du 12 juin 2026](https://www.anthropic.com/news/fable-mythos-access) et [rétablissement annoncé le 30 juin, mise à jour le 1er juillet](https://www.anthropic.com/news/redeploying-fable-5). Examiner les modèles et périmètres concernés ; ne pas assimiler cet épisode à l’arrêt de tous les services du fournisseur. |
| **4** | Les agents, nouvelle surface d’attaque | [OWASP Top 10 agentique 2026, publié le 9 décembre 2025](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/). Le comparer au [Top 10 LLM officiel](https://genai.owasp.org/llm-top-10/), avec la réserve ci-dessous. |
| **5** | Des conversations partagées deviennent publiques | [The Register, 1er août 2025](https://www.theregister.com/2025/08/01/openai_removes_chatgpt_selfdoxing_option/). Rechercher une deuxième source sur le mécanisme de partage/indexation et ses limites ; distinguer conversation privée, lien partagé et page indexée. |

**Consultation des liens ci-dessus : 23 octobre 2026.** Les dates indiquent les publications ou mises à jour, sauf mention explicite de la date de l’événement. Les sujets non retenus sont des pistes de recherche, pas quatre fiches d’enquête achevées.

!!! warning "Une affirmation du sujet 4 reste non corroborée"
    Au **23 octobre 2026**, la page officielle consultée présente le **Top 10 LLM 2025** : les permissions/autonomies excessives sont **LLM06:2025 — Excessive Agency**, tandis que **LLM03:2025** concerne la chaîne d’approvisionnement. L’affirmation de la consigne « Top 10 LLM 2026, permissions excessives en 3e position » n’est donc pas confirmée par cette page. Le **Top 10 agentique 2026** est bien un autre référentiel. Conserver son titre, son édition et sa date, sans mélanger les classements.

## Fiche renseignée — Sujet 2 : des attaquants outillés par des agents

**Choix proposé pour le carnet ; répartition entre groupes à confirmer.** Cette synthèse documentaire n’atteste pas une présentation collective déjà réalisée.

### Ce qui s’est passé — trois lignes

En **septembre 2025**, une campagne a utilisé Claude Code et des outils MCP pour automatiser des opérations offensives contre environ trente organisations, selon Anthropic.  
L’éditeur l’a rendue publique le **13 novembre 2025** ; la fiche **MITRE ATT&CK C0062**, créée le **20 avril 2026** et modifiée le **31 juillet 2026**, en organise les techniques.  
Les opérateurs humains conservaient des décisions : l’estimation d’Anthropic de **80–90 %** d’actions réalisées par l’IA ne signifie ni autonomie totale ni taux de réussite des attaques.

Sources : [Anthropic — annonce et rapport](https://www.anthropic.com/news/disrupting-AI-espionage) ; [MITRE — C0062](https://attack.mitre.org/campaigns/C0062/). **Consultées le 23 octobre 2026.**

### Qui parle, avec quel intérêt et quelles limites ?

| Source | Apport | Intérêt et limite |
| --- | --- | --- |
| **Anthropic**, publication du 13/11/2025, correction du 14/11/2025 | Observations de l’éditeur sur l’abus de son service | Source directement impliquée, avec un intérêt commercial et réputationnel à valoriser ses capacités de détection et de défense. Les traces publiques ne permettent pas de recalculer ici le pourcentage annoncé. |
| **MITRE ATT&CK**, fiche créée le 20/04/2026, dernière modification affichée le 31/07/2026 | Classement des comportements et identifiants techniques | Organisme distinct, mais références de cette fiche issues d’Anthropic : ce n’est pas une seconde enquête indépendante établissant le degré d’autonomie. |

**Lecture critique :** deux publications ne sont pas automatiquement deux preuves indépendantes. L’annonce d’Anthropic a corrigé sa description du débit le 14 novembre : il ne faut pas reprendre « des milliers de requêtes par seconde ». L’attribution de la campagne reste celle des sources ; aucune attribution propre n’est réalisée ici. [Correction et limites rapportées par Anthropic](https://www.anthropic.com/news/disrupting-AI-espionage).

### Ce que cela change pour un administrateur d’infrastructure

Les correspondances suivantes partent des comportements recensés par [MITRE C0062](https://attack.mitre.org/campaigns/C0062/). La colonne « adaptation » contient **nos propositions pour Hexalp**, pas des mesures déjà appliquées ni des exigences attribuées à MITRE.

| Comportement documenté | Adaptation proposée pour Hexalp | Preuve attendue après mise en œuvre |
| --- | --- | --- |
| Scan actif — **T1595.001/.002** | Inventorier les services exposés ; prioriser les correctifs selon exposition, exploitabilité et impact WMS ; prévoir restriction d’accès si le correctif doit attendre | Inventaire daté, ticket de correction, vérification de version et test d’accès |
| Recherche de comptes — **T1087** ; création de compte local — **T1136.001** | Comptes d’agent dédiés, droits minimaux, accès d’administration séparés ; alerter sur les créations et élévations inattendues | Matrice de droits, événements IAM/hôtes et revue des comptes |
| Collecte automatisée — **T1119** ; données locales — **T1005** | Limiter les données accessibles à chaque outil ; séparer production et laboratoire ; surveiller les lectures et exports inhabituels | Test de refus sur une ressource hors périmètre et trace de l’accès autorisé |
| Serveurs accessibles via MCP — **T1584.004** | Inventorier les connecteurs, destinations et identités ; restreindre les sorties réseau et prévoir leur révocation | Registre des connecteurs, règles réseau et essai de coupure |
| Exfiltration via service web — **T1567** | Corréler identité, session, hôte et transferts ; formaliser l’escalade vers l’astreinte sans attendre d’identifier une IA | Journaux horodatés, alerte testée et fiche réflexe de confinement |

Une rafale de requêtes ne suffit pas à identifier un agent d’IA. La détection porte d’abord sur les **actions, droits et flux**, quel que soit l’outil de l’attaquant. Les seuils d’alerte et délais de correction devront être décidés selon le contexte d’Hexalp, sans inventer des valeurs prétendument déjà validées.

### Une règle pour la politique d’Hexalp

> **Tout agent ou connecteur IA accédant au SI doit être déclaré, approuvé par le responsable infrastructure et la RSSI, et utiliser une identité dédiée dont les ressources et actions autorisées sont documentées. Toute écriture en production exige une validation humaine explicite avant exécution. Les appels d’outils et leurs résultats sont journalisés sans secrets, et l’accès doit pouvoir être révoqué.**

| Élément de contrôle proposé | Application attendue |
| --- | --- |
| **Responsables** | Responsable infrastructure pour les droits et l’exploitation ; RSSI pour l’approbation et les dérogations |
| **Avant activation** | Vérifier un accès autorisé, le refus d’une action hors périmètre, la validation d’une écriture et la révocation en environnement de test |
| **Traçabilité** | Conserver l’identité de l’agent, l’outil, l’heure, la cible, le résultat et l’approbateur ; masquer les secrets et limiter les données journalisées |
| **En cas de doute** | Suspendre le connecteur, préserver les traces minimales et appliquer le circuit d’incident existant |

**Statut :** proposition à discuter pour la politique de l’après-midi. Aucun compte d’agent, contrôle, test ou dispositif d’astreinte n’a été créé par cette activité.

## Restitution en deux minutes — trame proposée

- **0:00–0:30 :** dater la campagne et sa publication ; nommer les deux sources.
- **0:30–1:00 :** expliquer leur dépendance et la limite du chiffre de 80–90 %.
- **1:00–1:30 :** illustrer les conséquences par les comptes dédiés, les connecteurs et les journaux.
- **1:30–2:00 :** défendre la règle proposée et son test de révocation.

## Carte « 2025–2026 » pour la frise du J1

**Titre :** des agents capables d’enchaîner des actions deviennent aussi des outils d’attaque.

**Dates :** campagne en septembre 2025, révélation le 13 novembre 2025, fiche MITRE en 2026.

**Règles ou apprentissage ?** Un modèle issu de l’**apprentissage** est associé à des outils et à une orchestration. Cela ne prouve pas qu’il réapprend pendant l’attaque. Les règles de permissions et de validation doivent être imposées par les systèmes qui exécutent les actions.

**Pourquoi c’est important ?** Un assistant peut agir sur plusieurs ressources ; sa sécurité dépend aussi des comptes, connecteurs et contrôles d’exécution. La carte est ajoutée à la frise du J1 avec un renvoi à cette fiche.

## Méthode à conserver pour les autres sujets

Noter titre, auteur, URL, date de publication/mise à jour et date de consultation. Distinguer date de l’événement et date de sa révélation. Chercher une autre provenance de preuve, pas seulement une reprise du communiqué.

Pour **Glasswing**, rechercher le rapport d’un évaluateur indépendant : périmètre, versions, conditions, échantillon, validation des failles, reproductibilité et résultats négatifs. Un média relayant un bilan d’éditeur ne constitue pas à lui seul un test indépendant. Cette recherche détaillée reste à faire si le groupe choisit le sujet 1.

## État de la production

Fiche du sujet 2 renseignée, sources datées, règle et restitution proposées, carte ajoutée à la frise et synthèse inscrite au carnet. **Répartition des sujets, présentation en groupe, approbation de la politique et mise en œuvre restent non attestées.** Aucun résultat de test indépendant sur Glasswing n’est inventé.

[Retour au sommaire du J5](index.md) · [Pense-bête du J5](../../pense-bete/glossaire/ia-cybersecurite/it-5.md)
