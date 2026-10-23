# Itération 5 — Incident et politique IA

## Le fil du J5

Matin : compte rendu individuel de l’incident lié à la conversation de Julien du 24 septembre. Après-midi : évolutions de l’IA, politique en groupe, relecture et corrections éventuelles. Aucune installation ou nouveau fichier fourni ; réutiliser les productions J1/J2/J4.

## Livrables et état

Dossier : **`livrables/ia-cybersecurite/it-5/ia01-j5/`**.

| Livrable | État au 23 octobre 2026 |
| --- | --- |
| `compte_rendu_incident.md` | Rédigé en5.3, sources et limites tracées |
| `politique_ia_hexalp.md` | V0.1 rédigée avec assistance, PDF de quatre pages ; approbation à confirmer |
| `carnet_J5.md` | Contexte, références et réponses5.1–5.3 renseignés |

## Références à garder sous la main

- [Usages du J1](../../../ia-cybersecurite/it-1/le-message-de-nadia.md) et [frise](../../../ia-cybersecurite/it-1/70-ans-intelligence-artificielle.md).
- [Dossier Hexalp et note RSSI](../../../ia-cybersecurite/it-2/le-dossier-hexalp.md).
- [PSSI](../../../ia-cybersecurite/it-2/ce-que-dit-la-pssi.md) et [qualification du risque](../../../ia-cybersecurite/it-2/qualifier-risque-choisir-mesure.md).
- [Journal DSI](../../../ia-cybersecurite/it-4/relancer-et-reparer.md).
- [Rapport J4](../../../ia-cybersecurite/it-4/le-rapport-evaluation.md) et [conditions d’exploitation proposées](../../../ia-cybersecurite/it-4/exploiter-sans-se-fier-aveuglement.md).

## Repères de preuve

Données sorties ≠ exploitation ou entraînement démontrés. Compte personnel/professionnel, service, données et traces à identifier. Préserver les éléments et caviarder les secrets. Mesure proposée ≠ mesure appliquée ; politique rédigée ≠ approuvée. Les conditions J4 restent des propositions. Documenter les contributions au travail collectif lorsqu’il aura eu lieu.

- [Présentation complète de l’itération 5](../../../ia-cybersecurite/it-5/index.md)


## 5.1 — L’alerte

Scénario : conversation24/09 ; CERT lundi12/10 à17h48 selon Nadia ; message mardi13/10 à8h41, ouverture annoncée9h, compte rendu à midi. Rédaction réelle23/10. Cinq actions proposées : pilotage avec Nadia/Julien ; preuves minimales ; neutraliser le secret ; couper le lien public ; délimiter impact et informer via RSSI. Confinement et preuve peuvent être parallèles ; pas d’attente d’une expertise complète pour agir. Aucune action exécutée ici.

J2 U2 : **G4×V4=16 critique pour exposition C3**, pas exploitation prouvée. Mesures déjà proposées : renouvellement du secret stats, vérification accès/changements HAProxy/WMS, preuves protégées, circuit de dépannage approuvé. Lien public non visible au J2 ; date de conversation ≠ date de partage, lecteurs et copies inconnus. Nouvelle alerte rapportée ≠ dossier déjà collecté. Comparaison avec traitement documenté à faire en fin de matinée.

- [L’alerte — cinq actions et relecture J2](../../../ia-cybersecurite/it-5/l-alerte.md)


## 5.2 — Particularités d’un incident IA

Tableau portable/assistant rempli. Ordre proposé **B→C→A→E→F→G→D→H**, avec collecte minimale, rotation/retrait et enquête en parallèle ; DPO informé tôt, pas après toute l’enquête. Forum et lien de conversation sont deux objets à traiter si copie indépendante. Préserver avant suppression sans retarder le confinement ; restaurer une configuration validée compatible avec les changements actuels, sans ancien secret.

Suppression ChatGPT : retrait de l’affichage immédiat, suppression systèmes programmée sous30jours avec exceptions ; partages/copies tierces, mémoire et fichiers séparés à examiner. Aucun entraînement démontré, pas de garantie de retrait rétroactif. Sources officielles vérifiées23/10/2026 dans la fiche. Journaux : accès/authentification, pas forcément valeur du secret ; ne jamais le tester. Notification CNIL conditionnelle au risque sur données personnelles, pas automatique ; ouverture d’incident≠départ du délai. Aucune action réelle exécutée.

- [Ce qu’un incident IA a de particulier](../../../ia-cybersecurite/it-5/incident-ia-particularites.md)


## 5.3 — Dossier d’incident

P1–P8 reçues, dont P5/P6/P8 en captures ; trame originale/tableau non visibles dans le texte, structure proposée. Données clients confirmées P3 :41e-mails,9clients,17livraisons,12téléphones,6comptes de service ; pas nombre de personnes uniques. Deux vrais secrets : stats et jeton de déploiement. CheminTLS≠clé privée, empreinteSSH≠secret, identifiant≠mot de passe.

Stats lecture seule ;200 depuis10.20.250.200 à23h47 le08/10 à attribuer, pas preuve d’attaquant. J4exfil10.20.250.151 à3h le09/10 : lien causal non établi, réponseVPN attendue. Jeton read/write_registry sans expiration, CI/Ansible dépendants, sources connues recensées mais intégrité à vérifier. Changement inter30s/fall10 non committé/journalisé, compatible commandeIA sans auteur démontré.

P8 : DPO immédiat, commercial/juridique, Bricomax48h seloncontrat, DG pourgravité4, autoritésRSSI/DG, RETEX15jours. Horloge des notifications à qualifier, pas remiseàzéro à9h. Collectes constatées≠rotation/retrait/remise enétat exécutés ; aucun confinement confirmé.

- [Le dossier d’incident — compte rendu et réponses](../../../ia-cybersecurite/it-5/le-dossier-incident.md)


## 5.4 — Ce qui arrive

Sujet proposé : **2 — campagne assistée par agents, MITRE C0062**. Événement septembre 2025, publication Anthropic 13/11/2025, fiche MITRE créée 20/04/2026 et modifiée 31/07/2026 ; consultation 23/10/2026. Deux publications, mais même origine de preuve : pas deux enquêtes indépendantes. Pourcentage d’automatisation annoncé ≠ taux de réussite ni autonomie totale.

Règle proposée : agent déclaré/approuvé, identité dédiée, droits bornés, validation humaine avant écriture en production, traces sans secrets et révocation testable. Proposition non appliquée. Carte 2025–2026 ajoutée au J1 : apprentissage + outils, sans réapprentissage démontré pendant l’attaque. Restitution collective non attestée.

Vigilance OWASP : Top 10 agentique 2026 publié le 09/12/2025 ; page LLM consultée affichant l’édition 2025, Excessive Agency en LLM06 et non 3e. Affirmation « LLM 2026, 3e » non corroborée. Sujet Glasswing non retenu : tests indépendants à rechercher si choisi.

- [Ce qui arrive — fiche et sources datées](../../../ia-cybersecurite/it-5/ce-qui-arrive.md)


## 5.5 — Politique d’utilisation de l’IA

Message Nadia13h30 : compte rendu envoyé à la direction, secrets changés, lien et forum supprimés selon le scénario ; copies résiduelles/impacts et preuves à vérifier. Politique V0.1 rédigée avec assistance, quinze rubriques et annexes, quatre pages PDF ; adoption et relecture collective non attestées.

Cinq réflexes : outil/compte approuvés ; aucun C3 en entrée IA ; seconde relecture avant production ; connecteurs approuvés et bornés ; signalement immédiat protégé pour la bonne foi. Listes A/B/C, alternatives métier, compte professionnel distinct du SSO. Espace ChatGPT C0/fictif proposé, ouverture conditionnée à validation DSI/RSSI ; aucun contrat déjà acquis affirmé. J4 hors exploitation avant recette ; pilote éventuel quatre semaines, revue hebdomadaire et surplus visible.

Demande : accusé1jour ouvré, décision10jours ouvrés, alternative et escalade, silence≠accord. Traces minimales sans secrets : événements6mois, décisions durée d’autorisation+12mois, changements12mois ; choix proposés à valider DPO. Révision trimestrielle et sur événement. Règle5.4 intégrée au§7 ; Julien couvert par§2–5/8/10–13.

- [Politique, relecture et livrables](../../../ia-cybersecurite/it-5/la-politique-utilisation-ia.md)


## 5.6 — Comité et retour sur mes usages

Trois minutes sans diaporama : cinq règles ; règle préférée justifiée par une situation étudiée ; effet attendu sur le24/09. Trame préparée :§11, réponse sous dix jours et alternative métier, illustrée par le cas du J2. **Coquille confirmée : aucun crash-test dans le module ; aucun résultat ni correction associé n’est attendu.** La présentation et la validation collectives restent à confirmer.

Inventaire personnel J1 : deux usages de **Codex** (rédaction et agent du dépôt), tous deux **à valider** selon la politique proposée. Compte/offre et autorisation inconnus ; ne pas inventer des usages supplémentaires ou attribuer ceux d’Hexalp à l’apprenant. Dès lundi : vérifier compte/outils, minimiser les données, limiter les fichiers accessibles, relire les modifications, faire valider les actions en production et signaler sans délai. Bilan personnel proposé en fin de carnet, à personnaliser ; oral et maîtrise autonome non attestés.

- [Présentation, usages et bilan](../../../ia-cybersecurite/it-5/convaincre-comite-retour-usages.md)
