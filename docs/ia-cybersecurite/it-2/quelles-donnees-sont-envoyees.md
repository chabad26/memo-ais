# Quelles données sont envoyées ?

## Le problème à résoudre

« Ce n'est qu'un log. » Pourtant, journaux et configurations peuvent révéler des clients, des personnes, la structure du réseau et des moyens d'accès. Cette fiche répond à l'étape **3. Données** de la [méthode d'analyse](shadow-ia-de-quoi-parle-t-on.md).

**Objectif :** identifier et classer les informations du copier-coller de Thomas, puis produire un extrait minimal utile au diagnostic du WMS, le logiciel de gestion d'entrepôt.

!!! warning "Kit fictif uniquement"
    Toutes les valeurs fournies dans cet exercice sont fictives. L'analyse ci-dessous n'atteste ni envoi réel, ni compromission. Les secrets du kit ne sont pas recopiés : leur nom de variable suffit à les identifier. Ne pas reproduire cet exercice avec de vrais secrets dans un service public.

## Référence — PSSI Hexalp, article 2.1 fourni dans l'exercice

| Classe | Définition | Exemples |
| --- | --- | --- |
| **C0 — Public** | Information destinée à être diffusée | Site web, offres d'emploi |
| **C1 — Interne** | Diffusion libre au sein d'Hexalp | Organigramme, procédures courantes |
| **C2 — Confidentiel** | Diffusion restreinte ; une fuite causerait un préjudice | Données clients, données personnelles, schémas réseau, code source |
| **C3 — Secret** | Accès nominatif ; une fuite compromettrait la sécurité ou l'activité | Mots de passe, clés et jetons, configurations de sécurité |

Les classements suivants appliquent cet extrait au scénario. La PSSI complète n'est pas fournie : les cas limites sont des propositions motivées. Le fichier `.env` contenant des secrets est **C3 dans son ensemble**, même si certains champs pris isolément sont C2.

## Mission 1 — La chasse aux données

### Inventaire renseigné

**Convention de comptage : 21 éléments distincts ou groupes fonctionnels**, chaque ligne comptant pour un élément. Les répétitions dans plusieurs lignes ne sont pas recomptées. Ce nombre dépend du découpage annoncé ; ce n'est pas un nombre de personnes ni de secrets.

| N° | Élément | Catégorie | Classe PSSI proposée | Ce qu'un attaquant pourrait en faire |
| --- | --- | --- | --- | --- |
| 1 | Date précise et horaires nocturnes des trois événements | Autre : activité et chronologie | C2 dans ce contexte opérationnel | Corréler l'incident avec une tâche planifiée ou une fenêtre de moindre disponibilité |
| 2 | Nom du serveur applicatif `wms-app-01` | Topologie interne | C2 | Identifier le rôle et la nomenclature des machines |
| 3 | Logiciels, processus et identifiants : nginx, app, sshd, PID | Autre : informations techniques internes | C2 dans cet extrait | Préparer une reconnaissance ; aucun numéro de version exploitable n'est toutefois fourni |
| 4 | IP du client HTTP `10.20.4.37` | Topologie interne | C2 | Repérer un poste ou service appelant ; l'IP seule ne prouve pas une identité personnelle |
| 5 | Nom interne du service `wms.hexalp.local` | Topologie interne | C2 | Construire une cartographie DNS et du service métier |
| 6 | Méthode et chemin `POST /api/v2/orders` | Autre : interface applicative | C2 | Identifier un point d'entrée de création ou traitement de commandes |
| 7 | Identifiant client `CARREFIX`, répété dans la requête et le log | Donnée client | C2 | Relier un client à Hexalp et préparer un prétexte commercial crédible |
| 8 | Destination HTTP de l'upstream `10.20.8.12:8080` | Topologie interne | C2 | Identifier une liaison applicative, un port et un protocole ; aucun accès direct depuis Internet n'est démontré |
| 9 | Numéro de commande `88412` | Donnée client | C2 | Cibler une transaction et crédibiliser une demande frauduleuse |
| 10 | Adresse de contact nominative du client | Donnée personnelle et client | C2 | Faire du phishing ciblé et associer une personne à une commande |
| 11 | Adresse de livraison | Donnée client ; personnelle si rattachable à une personne physique | C2 | Identifier un lieu et enrichir un scénario de fraude ; l'adresse seule ne prouve pas qu'il s'agit d'un domicile |
| 12 | `OrderService`, timeout de base et erreur nginx | Autre : fonctionnement et incident | C2 dans le contexte original | Identifier une dépendance défaillante ou une période d'indisponibilité |
| 13 | Compte SSH `deploy` | Autre : identité technique | C2 | Cibler un compte de déploiement ; ce nom seul ne donne pas de droit d'accès |
| 14 | IP source SSH `10.20.1.5` et port source `52211` | Topologie interne | C2 | Repérer une source d'administration ; le port éphémère n'est pas un port d'écoute serveur |
| 15 | Authentification réussie par clé ED25519 et empreinte tronquée | Autre : métadonnées d'authentification | C2 ; configuration de sécurité complète à traiter C3 | Corréler une clé ou un accès avec d'autres traces ; **une empreinte n'est pas une clé privée et ne permet pas de se connecter** |
| 16 | `DB_HOST=10.20.8.20` | Topologie interne | C2 | Localiser le serveur de base de données |
| 17 | `DB_USER=wms_app` | Autre : compte applicatif | C2 | Identifier le compte à cibler ; combiné à son mot de passe, il devient un moyen d'accès |
| 18 | Valeur de `DB_PASSWORD` — volontairement non reproduite | Secret | **C3** | Tenter un accès à la base si les conditions réseau et les droits le permettent |
| 19 | `REDIS_URL` : hôte `10.20.8.21`, protocole et port `6379` | Topologie interne | C2 | Localiser le cache et ses dépendances ; l'extrait ne prouve pas l'absence d'authentification ou de chiffrement ailleurs |
| 20 | Valeur de `TRANSPORTEUR_API_KEY` — volontairement non reproduite | Secret | **C3** | Appeler les services du transporteur selon les droits et la validité du jeton |
| 21 | `SMTP_RELAY=mail-relay.hexalp.local` | Topologie interne | C2 | Identifier un relais de messagerie et enrichir la cartographie interne |

### 1. Quel élément est le plus grave ?

Les deux secrets, **mot de passe de base et jeton transporteur**, sont prioritaires : ils peuvent autoriser un accès, contrairement à un simple nom de machine. On ne peut pas départager leur impact sans connaître leurs droits, leur validité et leur exposition réseau. Le jeton pourrait être utilisable à distance si l'API est accessible ; le mot de passe pourrait donner accès aux commandes et données clients si la base est joignable.

**Si ces valeurs étaient réelles et envoyées à un outil non autorisé :** signaler l'exposition, révoquer ou renouveler les secrets concernés et examiner les traces d'usage. Supprimer le chat seul ne révoque aucun accès. Il s'agit ici de mesures proposées, pas d'actions exécutées.

### 2. De quoi l'assistant a-t-il besoin ?

Pour une première analyse, il lui suffit de savoir qu'un proxy nginx attend son service applicatif, qu'un timeout de base apparaît deux secondes plus tard et que l'incident survient vers 03 h 14. **La chronologie suggère une dépendance à examiner ; elle ne démontre pas la cause.** Les identités du client et du contact, les coordonnées de livraison et les secrets n'aident pas à expliquer le timeout.

Pour aller plus loin, Thomas devra collecter dans le SI des métriques et traces pertinentes : récurrence, durée des requêtes, charge et verrous de la base, saturation des connexions, latence réseau, sauvegardes et tâches planifiées. Il pourra ensuite transmettre un résumé autorisé et minimisé. Aucun de ces facteurs n'est établi par les trois lignes du kit.

## Mission 2 — Caviarder

### Version minimale proposée

Les événements sont remis en lignes séparées. Les noms sont remplacés par des alias stables, la date est retirée, et seuls l'horaire utile et les écarts temporels sont conservés. Le bloc `.env` et l'événement SSH, sans lien établi avec le timeout, sont retirés entièrement.

```text
Contexte : un service de gestion d'entrepôt rencontre un incident nocturne.
Architecture minimale : PROXY_A -> APP_A -> DB_A.

Vers 03:14, t+0 s — PROXY_A / nginx :
upstream timed out (110) while reading response header from upstream
request: "POST /api/orders HTTP/1.1", upstream: "http://APP_A:PORT_APP"

t+2 s — APP_A :
ERROR OrderService — DB timeout lors du traitement d'une commande.

Question : quelles hypothèses vérifier et quelles métriques collecter
pour comprendre ce timeout nocturne, sans conclure à partir de ces seules traces ?
```

La relation `APP_A -> DB_A` résume la dépendance indiquée par le timeout et la configuration ; elle ne prouve pas une architecture complète. Le chemin est volontairement généralisé. Cet extrait sert à discuter, **pas à être exécuté comme une configuration**.

### 1. L'assistant peut-il encore répondre ?

Oui, pour proposer des pistes et une méthode de diagnostic : latence de la base, contention, pool de connexions, traitement long ou tâches nocturnes. Il ne peut pas désigner une cause certaine avec ces seules informations. Le caviardage conserve le signal technique nécessaire à cette première question.

### 2. Pourquoi ne pas remplacer toutes les adresses par `X.X.X.X` ?

Cela efface les relations : impossible de distinguer le client, le proxy, l'application et la base, ou de voir qu'une même adresse revient. Utiliser des alias **distincts et stables** comme `CLIENT_A`, `APP_A`, `DB_A`, en conservant seulement les relations utiles. Si une syntaxe IP est indispensable à un test, employer des adresses de documentation et une correspondance cohérente, sans reproduire les sous-réseaux réels.

La table de correspondance doit rester dans le SI et ne pas être jointe au prompt. Cette substitution peut rester une **pseudonymisation**, surtout si le contexte permet une réidentification ; elle ne garantit pas l'anonymat et ne rend pas automatiquement le contenu C0.

### 3. Le caviardage manuel suffit-il pour 300 salariés ?

Non : oubli, capture partielle et format inhabituel rendent les erreurs probables. Il faut combiner une procédure simple, des exemples de prompts minimisés, la formation, une offre approuvée et des contrôles techniques : détection de secrets et de données personnelles avant envoi, exclusion des fichiers sensibles, filtrage des flux et revue pour les cas à fort enjeu. Les détecteurs ont aussi des faux négatifs et ne doivent pas devenir un prétexte pour tout transmettre.

Ces propositions rejoignent les mesures de nettoyage des données, de moindre privilège et de sensibilisation de l'[OWASP LLM02:2025](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/). L'objectif est de réduire le contenu envoyé avant sa sortie, avec une solution adaptée au besoin de dépannage.

## Mission 3 — Ce que vous n'avez pas tapé

Les possibilités ci-dessous dépendent des fonctions, permissions et réglages effectivement activés. Elles ne prouvent pas que ces outils sont installés ou utilisés chez Hexalp.

| Canal | Ce qui peut partir sans que vous le tapiez | Exemple hypothétique chez Hexalp |
| --- | --- | --- |
| **Assistant de code dans l'IDE** | Fichier ouvert, sélection, fichiers voisins ou contexte du dépôt, erreurs du terminal, selon l'outil et ses autorisations | En demandant de corriger `OrderService`, Thomas transmet aussi des extraits de configuration présents dans le contexte collecté |
| **Extension de navigateur « IA »** | Texte d'une page, champs de formulaire, documents affichés ou URL selon les permissions et le déclenchement | Une fonction de résumé lit une fiche client ouverte dans le WMS, avec contact et numéro de commande |
| **Photo ou capture d'écran** | Texte lisible par reconnaissance visuelle, onglets, notifications, noms de comptes ; éventuellement métadonnées si le service les reçoit | Le technicien photographie une erreur du trieur avec un jeton affiché dans la fenêtre voisine |
| **Fichier glissé dans la conversation** | Contenu complet accessible, feuilles masquées, commentaires, suivi des modifications, propriétés et pièces embarquées selon le format et le traitement | Un export Excel de commandes contient une feuille masquée avec les coordonnées des destinataires |
| **Fonction « mémoire » de l'assistant** | Informations conservées depuis des échanges précédents puis réutilisées comme contexte ; ce n'est pas une lecture autonome de tout le SI | Un nom de client ou une information de projet réapparaît dans une réponse ultérieure sans être retapé ; une recherche web ou un connecteur peut aussi transmettre du contexte selon ses règles |

**Point commun :** contrôler le contexte réellement accessible, les destinations et les fonctions activées. Une autorisation d'accès n'implique pas que toutes les données accessibles doivent être envoyées. Voir aussi les [recommandations ANSSI–BSI sur les assistants de programmation](https://cyber.gouv.fr/nous-connaitre/publications/publications-internationales/ai-coding-assistants/).

## Que devient une conversation supprimée ?

**Fournisseur étudié : OpenAI, comme en [2.3](quel-compte-quel-fournisseur.md). Sources officielles consultées le 20 octobre 2026.**

La suppression retire immédiatement le chat de l'affichage du compte ; sa suppression définitive des systèmes est normalement programmée sous **30 jours**, avec exceptions notamment de sécurité, d'obligation légale ou de contenu déjà désidentifié et dissocié du compte. Archiver n'est pas supprimer. Une copie de fichier dans Library doit être supprimée séparément. [OpenAI — Conservation des chats et fichiers](https://help.openai.com/en/articles/8983778-chat-and-file-retention-in-chatgpt).

**Oui, une conversation a pu être utilisée avant sa suppression**, si l'offre, les réglages et les conditions applicables autorisaient cet usage. Sur les offres personnelles, le contenu peut servir à améliorer les modèles ; le refus concerne les nouvelles conversations. Un retour volontaire sur une réponse peut également autoriser l'utilisation de la conversation associée, même après désactivation de l'entraînement. Les offres Business, Enterprise et l'API excluent cet usage par défaut, sous réserve des mécanismes de partage ou accords applicables. [OpenAI — Utilisation des données pour améliorer les modèles](https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance).

La suppression du chat **n'est pas une preuve de retrait rétroactif d'un entraînement déjà réalisé**. Nous n'avons aucune preuve qu'une conversation précise de Thomas ou du compte de formation a été utilisée pour entraîner un modèle. Les mémoires enregistrées se gèrent également séparément : supprimer une conversation ne doit pas être supposé effacer toutes les informations conservées par ailleurs.

## Livrable obtenu

Inventaire classé, version minimale caviardée, réponses aux cinq questions des missions 1 et 2, tableau des cinq canaux et analyse documentaire de la suppression. Les valeurs originales restent fictives ; aucun envoi de ces logs à un autre assistant, aucune révocation et aucun contrôle du compte réel ne sont attestés.

[Retour à l'itération 2](index.md)
