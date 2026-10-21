# IA et Cybersécurité — Itération 2 : Shadow IA

## Termes à retenir

| Terme | Repère pour l'ouverture de l'itération |
| --- | --- |
| Shadow IA | Définition corrigée en 2.2 : usage professionnel d'IA inconnu de l'organisation et non évalué, y compris fonction embarquée ou modèle local |
| Déclaré non validé | L'organisation connaît la demande mais n'a pas autorisé l'usage ; le silence ne vaut pas validation |
| Zone grise | Règle ou périmètre de validation ambigu, à clarifier ; ne prouve pas à lui seul un usage caché |
| IA embarquée | Fonction IA intégrée à un logiciel ; une validation ancienne ne couvre pas nécessairement une nouvelle fonction |
| Besoin métier | Finalité réelle à préserver dans la mesure proposée, pour éviter de laisser le problème sans réponse |
| Déclaration | Information de la DSI sur un usage, sa finalité, son compte, ses données et ses accès ; ne vaut pas nécessairement approbation |
| Validation | Accord sur un périmètre d'usage et ses conditions ; doit être distingué d'une simple connaissance de l'outil |
| Statut inconnu | Information ou preuve manquante ; ne signifie pas à lui seul qu'un usage a été refusé ou interdit |
| Entraînement / conservation | Exclure les données de l’entraînement ne supprime ni l’historique ni les journaux |
| Compte personnel payant | Le paiement ou le remboursement ne démontre pas une administration ni un contrat Hexalp |
| Départ du salarié | Révocation de l’accès, conservation et transfert des données sont des opérations distinctes |
| Minimisation | Ne transmettre que les informations nécessaires à la question ; supprimer un champ inutile plutôt que seulement le masquer |
| Alias stable | Conserve les relations entre événements sans transmettre les identifiants réels ; ne garantit pas une anonymisation |
| Secret / empreinte | Un mot de passe ou jeton donne potentiellement accès ; une empreinte de clé publique ne permet pas de s’authentifier |
| OAuth / consentement | Accord sur des permissions ; ne vaut pas validation sécurité de l’application |
| offline_access | Permet un accès prolongé via renouvellement des jetons ; n’ajoute pas de droit sur les données |
| Excessive Agency | Trop de fonctions, trop de permissions, trop d’autonomie |
| MCP | Protocole d’intégration des outils et du contexte ; aucune garantie automatique de sûreté |
| Conformité / preuve | Une règle applicable et une preuve manquante ne suffisent pas à déclarer un écart établi |
| Dérogation — 9.2 | Demande au RSSI, réponse sous 10 jours ouvrés ; le silence ne vaut pas accord |
| Extension de navigateur | Logiciel ajouté au poste : catalogue ou validation selon l’interprétation retenue de 4.1 |
| Cotation pédagogique | Gravité × vraisemblance : 1–3 faible, 4–6 modéré, 8–9 élevé, 12–16 critique ; décrire l’événement coté et les hypothèses |
| Risque résiduel | À réévaluer après vérification des mesures, pas à déclarer réduit sur la seule base d’un plan |
| Traitement du risque | Remplacer, réduire, encadrer, accepter par décision habilitée ou interdire en couvrant le besoin métier |
| Usage / outil | Plusieurs pratiques peuvent reposer sur le même outil : ici, deux usages de Codex |

## Gestes à retenir

1. Reprendre les usages documentés du J1 sans ajouter d'outil personnel supposé.
2. Distinguer déclaration, validation et preuve disponible.
3. Rendre explicite toute hypothèse de transposition des pratiques de formation chez Hexalp.
4. Décrire le besoin métier et les conditions d'usage au lieu de conclure à une interdiction générale.
5. Attendre les pièces annoncées avant de qualifier les usages des équipes ou les permissions d'InboxPilot.
6. Suivre les sept étapes : outil/fournisseur → compte → données → accès/connecteurs → règle PSSI → qualification → mesure.
7. Ne pas déduire une autorisation d'un compte professionnel, d'une installation locale ou d'un achat sans vérifier le périmètre.
8. Distinguer l'interdiction annoncée de la réduction des usages effectivement mesurée.

## Travail documenté

Le programme de l'itération et ses livrables sont annoncés. La fiche d'ouverture reprend les deux usages de Codex : **deux usages non déclarés dans une hypothèse explicite**, aucune validation DSI documentée et statut réel inconnu. La définition initiale est conservée puis corrigée en 2.2.

La fiche 2.2 classe huit situations sous hypothèses explicites : 2 approuvées, 1 déclarée non validée, 2 shadow IA et 3 zones grises. Le cas Samsung de 2023 est sourcé, sans conclure à la disparition des usages. La grille en sept étapes est disponible en tête de la fiche.

La fiche 2.3 compare les comptes OpenAI à partir de sources officielles consultées le 20 octobre 2026. Les quatre réponses sont renseignées ; l’offre et les réglages du compte réellement utilisé restent à vérifier.

La PSSI fournie et l’écran fictif InboxPilot ont été analysés. Le dossier 2.8 est complété par les tableaux proxy, dépenses, consentements, parc et sondage, transcrits depuis les captures. Aucun tenant réel n’a été inspecté.

## Docs associées

- [Itération 2 — Shadow IA](../../../ia-cybersecurite/it-2/index.md)
- [Le recensement de Nadia](../../../ia-cybersecurite/it-2/le-recensement-de-nadia.md)
- [Shadow IA : de quoi parle-t-on ?](../../../ia-cybersecurite/it-2/shadow-ia-de-quoi-parle-t-on.md)
- [Inventaire des usages du J1](../../../ia-cybersecurite/it-1/le-message-de-nadia.md)

- [Quel compte, quel fournisseur ?](../../../ia-cybersecurite/it-2/quel-compte-quel-fournisseur.md)

La fiche 2.4 classe 21 éléments/groupes du kit fictif, fournit un extrait minimisé et analyse cinq canaux de contexte implicite. La suppression d’un chat ne prouve pas son retrait d’un entraînement passé.

- [Quelles données sont envoyées ?](../../../ia-cybersecurite/it-2/quelles-donnees-sont-envoyees.md)

La fiche 2.5 analyse les six permissions d’InboxPilot et le cas EchoLeak, sans expérimentation. Changer le mot de passe ne garantit pas la révocation de tous les accès OAuth.

- [Les connecteurs : quand l’IA a les clés](../../../ia-cybersecurite/it-2/connecteurs-quand-ia-a-les-cles.md)

La fiche 2.6 rapproche dix situations des neuf articles fournis de la PSSI v3.2. Les écarts établis sont séparés des conditions à vérifier ; le dépassement de 9.2 dépend du destinataire, de la nature et de la date de la demande.

- [Ce que dit la PSSI](../../../ia-cybersecurite/it-2/ce-que-dit-la-pssi.md)

La fiche 2.7 propose trois cotations initiales : Thomas 16 critique pour l’exposition supposée, InboxPilot 12 critique et modèle local 4 modéré sous hypothèses explicites. Les mesures restent proposées et les risques résiduels non vérifiés.

- [Qualifier le risque et choisir une mesure](../../../ia-cybersecurite/it-2/qualifier-risque-choisir-mesure.md)

La fiche 2.8 croise les dix pièces en dix fiches : Sofia/API, Julien/WMS, TalentSort, HelpFlow, ChatGPT commercial, MeetNote, AI Summarizer, Copilot, Ollama et DeepL. HelpFlow et l’usage effectif d’Ollama restent à vérifier. Cinq actions et deux messages sont proposés ; achats et consentements commerciaux sont cités sans présumer les données envoyées. SNCF/Acrobat sont exclus faute d’usage IA démontré. Le sondage anonyme de juin ne permet pas d’attribution individuelle ni de mesure de septembre.

- [Le dossier Hexalp](../../../ia-cybersecurite/it-2/le-dossier-hexalp.md)
