# La politique d’utilisation de l’IA


> **Nadia [13:30]** Le compte rendu est parti à la direction, merci 🙏 Les secrets sont changés, le lien et le message du forum sont supprimés.
>
> Vendredi au comité, je ne veux pas seulement l’incident. Je veux la règle qui évite le suivant. Quatre pages maximum, que les 300 salariés puissent appliquer lundi. Et je vous rappelle mon seul interdit : pas de « il faut tout interdire » 🙃

## Ce qui change dans le scénario

Ce nouveau message rapporte trois actions achevées : envoi du compte rendu à la direction, changement des secrets et suppression du lien et du message de forum. Il complète les constats disponibles au moment de [5.3](le-dossier-incident.md), sans réécrire rétroactivement les pièces P1–P8. **Aucune de ces actions n’est une exécution de l’assistant.** Les traces de rotation, le périmètre des copies résiduelles, les impacts et les obligations de notification restent à vérifier. Suppression des publications ne signifie pas absence de copies ni clôture de l’incident.

## Objectif et livrables rédigés

Transformer les constats J1–J4, l’incident et la [fiche 5.4](ce-qui-arrive.md) en règles qui indiquent **un responsable, une action, un contrôle et une alternative métier**.

- [Politique IA Hexalp — PDF de quatre pages, annexes comprises](../../assets/files/ia-cybersecurite/it-5/Politique-IA-Hexalp-proposition.pdf).
- [Politique IA Hexalp — source Markdown téléchargeable au format texte](../../assets/files/ia-cybersecurite/it-5/politique_ia_hexalp.md.txt).
- Source de remise : **`livrables/ia-cybersecurite/it-5/ia01-j5/politique_ia_hexalp.md`**.

**V0.1 proposée, rédigée avec assistance le 23 octobre 2026.** Le texte n’est ni une adoption par la direction ni une validation de groupe ; le PDF est une mise en page vérifiée du même Markdown. La présente fiche pédagogique et le carnet ne font pas partie des quatre pages de politique.

## Mission et organisation

Répartir les rubriques et s’accorder sur les outils pendant **15 minutes**, rédiger pendant **1 h 15**, puis consacrer **30 minutes** à la relecture croisée. Chaque règle commence par un verbe d’action et nomme son responsable. Pour chaque interdiction, couvrir le besoin métier. Justifier ensuite les règles qui auraient évité ou réduit l’incident de Julien.

## Les quinze rubriques sont couvertes

| N° | Décision écrite dans la politique | Vérification et solution en cas de blocage |
| --- | --- | --- |
| **1 — Objet/périmètre** | Tous les intervenants et usages, y compris IA embarquée, local et détection | Inventaire par DSI ; pas d’exemption pour le gratuit ou le poste personnel |
| **2 — Outils** | Trois listes A/B/C et critères de changement de statut | Catalogue avec preuve d’accord ; rédaction, traduction, recrutement et dépannage internes en attendant |
| **3 — Comptes** | Compte professionnel administré, achats DSI, clés dans un gestionnaire approuvé | Vérifier offre et identité ; le SSO n’est pas une autorisation de service |
| **4 — Données** | C0/C1/C2 uniquement dans le périmètre validé ; exclusion C3 des entrées IA | Classement et validation DPO si données personnelles ; valeur fictive ou traitement interne |
| **5 — Code/configuration/logs** | Minimisation, caviardage, contexte maîtrisé et filtrage testé | Pas de garantie attribuée à un proxy non déployé ; diagnostic interne si doute |
| **6 — Assistants de code** | Licence, provenance et dépendances vérifiées | Test isolé, paquet connu ou développement classique |
| **7 — Agents/connecteurs** | Accord DSI/RSSI, identité dédiée et droits bornés, validation d’action, révocation | Règle issue de 5.4 ; contrôle technique et traitement manuel de secours |
| **8 — Relecture** | Seconde personne habilitée avant production, tests et journal DSI | Référent d’astreinte ; procédure interne si relecteur indisponible |
| **9 — Modèles Hexalp** | Recette avant pilote, contrôle des lots, intégrité et revue hebdomadaire | Pas de déploiement automatique du J4 ; maintien des règles et gestion visible du surplus |
| **10 — Traces** | Décisions 12 mois après fin d’autorisation, événements 6 mois, changements 12 mois | Durées proposées à valider DPO ; purge et collecte à tester, pas de prompts complets par défaut |
| **11 — Demande** | Accusé sous 1 jour ouvré, décision sous 10 jours ouvrés, alternative et escalade | Silence sans autorisation ; même plafond pour demandes ordinaires et dérogations |
| **12 — Incident** | Signalement immédiat RSSI/astreinte ; soutien à la bonne foi | Préservation/confinement, DPO et chaîne P8 ; téléphone si portail indisponible |
| **13 — Responsabilités** | Salarié, manager, DSI, RSSI, DPO et direction nommés | Vérifier catalogue, annuaire et moyens avant entrée en vigueur |
| **14 — Révision** | Trimestrielle et immédiate sur événement significatif | Suspendre le seul périmètre affecté et maintenir une alternative |
| **15 — PSSI** | Rattachements aux articles exacts et extension proposée de 9.2 | Ne pas annoncer une modification de la PSSI déjà approuvée |

## Les choix à défendre en groupe

**Ouvrir un usage utile sans inventer un contrat existant.** La liste A propose un espace ChatGPT professionnel administré, limité aux textes publics/fictifs et sans connecteur, ainsi que l’évaluation locale J3/J4 sur données fictives. Le catalogue doit identifier l’offre, le compte et les réglages avant ouverture. Aucune licence d’entreprise déjà acquise n’est affirmée ; avant disponibilité, les solutions internes couvrent les besoins. C1/C2 ne sont pas autorisés par ces entrées initiales ; une validation ciblée permet de les ajouter.

**Préciser l’interdiction des secrets.** Les mots de passe et jetons ne sont jamais fournis au modèle, au contexte ou aux journaux. L’authentification technique d’une API avec un secret géré est distinguée de son insertion dans le prompt. Le modèle local ne crée pas d’exception à cette règle de données.

**Conserver la décision J4.** Le modèle reste en évaluation ; le pilote de quatre semaines exige une décision et des moyens réels. Trente qualifications hebdomadaires ne justifient pas d’effacer le surplus, et la règle existante de fail2ban demeure indépendante du modèle.

**Assumer les choix internes.** Accusé sous un jour, plafond de dix jours, durées de six/douze mois et revue trimestrielle sont des propositions d’organisation. Ils ne sont pas attribués à une norme ANSSI, CNIL ou OWASP. Les coordonnées opérationnelles doivent venir de l’annuaire vérifié ; aucun faux téléphone ou service d’astreinte déjà actif n’est inventé.

## Retour sur l’incident de Julien

| Point de l’incident | Règles numérotées | Effet attendu et limite |
| --- | --- | --- |
| Compte personnel pour diagnostiquer le WMS | **2, 3, 11** | Accès professionnel contrôlé ou diagnostic interne, avec circuit de réponse au besoin |
| Secret stats et jeton dans les contenus | **4, 5** | Retirer les secrets avant envoi ; filtrage complémentaire à tester, sans garantie absolue |
| Données clients et journaux trop larges | **4, 5, 13** | Minimiser et respecter le périmètre DPO ; anonymisation non présumée sur le seul retrait des noms |
| Configuration modifiée sans trace suffisante | **8, 10** | Seconde lecture, test, journal et retour arrière ; causalité exacte du changement non inventée |
| Lien et forum publics | **2, 5, 12** | Partage interne restreint et signalement/retrait rapide ; les copies tierces restent possibles |
| Besoin urgent pendant l’astreinte | **8, 11, 13** | Référent et solution interne ; pas de validation fictive quand le relecteur manque |

Ces règles auraient pu prévenir l’exposition ou en limiter la gravité ; elles ne démontrent pas rétrospectivement qu’une attaque a exploité les secrets.

## Relecture croisée préparée

**Test « verbe + responsable » :** chaque prescription est introduite par une action et un rôle ; les entrées A/B/C décrivent les statuts gérés par la DSI, les intitulés de rubrique ne sont pas eux-mêmes des règles. Les cinq rappels d’ouverture s’adressent explicitement aux salariés/prestataires.

**Test « interdiction + besoin » :** compte personnel → compte administré/support interne ; C3 → valeur fictive/coffre-fort ; extension trop large → lecture/résumé interne puis outil limité ; paquet douteux → catalogue ou développement classique ; agent trop privilégié → traitement manuel ; décision autonome RH → examen humain ; absence de relecteur → référent et procédure interne.

**Test « vérifiable lundi » :** faire approuver la politique ; désigner les responsables ; vérifier catalogue et espace professionnel disponible ; tester restrictions, traces et révocation ; confirmer support/astreinte et annuaire ; diffuser aux équipes. Ces vérifications sont des prérequis à exécuter, pas des résultats déclarés acquis. La relecture de groupe reste à confirmer.

## Usage de l’assistance IA pour cette production

| Point à contrôler avant assistance | État de cette rédaction |
| --- | --- |
| Outil | Codex dans l’espace de travail, pour rédaction et modification du dépôt ; son autorisation chez Hexalp n’est pas établie |
| Compte/offre/contrat | Type de compte et garanties non vérifiés ici ; ne pas déclarer la conformité à la future politique |
| Données utilisées | Consignes, éléments fictifs du scénario et synthèses caviardées ; aucun secret réel ni pièce brute ajouté à la politique |
| Contribution et défense | Brouillon rédigé avec assistance ; groupe chargé de relire, corriger, justifier et décider de l’adopter |

La politique est une production pédagogique assistée, pas un travail collectif autonome attesté. En situation réelle, vérifier d’abord outil/compte et autorisation ; à défaut, poursuivre la rédaction en interne sans envoyer les documents de l’entreprise.

## Références consultées le 23 octobre 2026

- [ANSSI — Recommandations de sécurité pour un système d’IA générative](https://messervices.cyber.gouv.fr/documents-guides/Recommandations_de_s%C3%A9curit%C3%A9_pour_un_syst%C3%A8me_d_IA_g%C3%A9n%C3%A9rative.pdf), **ANSSI-PA-102, v1.0 du 29 avril 2024** : sécurité et cycle de vie ; recommandations à adapter, pas certification de la politique.
- [CNIL — Questions-réponses sur l’utilisation d’un système d’IA générative](https://www.cnil.fr/fr/les-questions-reponses-de-la-cnil-sur-lutilisation-dun-systeme-dia-generative), **18 juillet 2024** : aide à l’encadrement des usages et des traitements de données personnelles.
- [OWASP — Top 10 for Agentic Applications for 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), **9 décembre 2025** : risques agentiques ; édition distincte du Top 10 LLM.
- [PSSI et angles morts J2](../it-2/ce-que-dit-la-pssi.md), [inventaire](../it-2/le-dossier-hexalp.md), [conditions J4](../it-4/exploiter-sans-se-fier-aveuglement.md), [pièces de l’incident](le-dossier-incident.md) et [fiche 5.4](ce-qui-arrive.md).

## État de remise

Politique Markdown rédigée, quinze rubriques et deux annexes intégrées, PDF de **quatre pages** contrôlé en texte et en rendu. Proposition de listes, mesures et durées ; aucun achat, consentement, déploiement, approbation de groupe, adoption par la direction ou envoi au comité n’est attesté. Le message de Nadia annonce l’envoi du **compte rendu**, pas celui de cette politique.

[Retour au J5](index.md) · [Pense-bête](../../pense-bete/glossaire/ia-cybersecurite/it-5.md)
