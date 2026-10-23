# L’alerte

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

Référence relue : **fiche U2, source pièce 7**, dans [Le dossier Hexalp — 2.8](../it-2/le-dossier-hexalp.md).

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

- [Présentation du J5](index.md)
- [Pense-bête de l’itération](../../pense-bete/glossaire/ia-cybersecurite/it-5.md)
