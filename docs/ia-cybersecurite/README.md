# IA et Cybersécurité

## Itération 1 — Sous le capot de l'IA

- [Sommaire de l'itération](it-1/index.md)
- [Le message de Nadia](it-1/le-message-de-nadia.md) : arrivée chez Hexalp et inventaire des usages de l'IA.
- [70 ans d'intelligence artificielle](it-1/70-ans-intelligence-artificielle.md) : frise Mermaid verticale renseignée, sources et analyse des cycles de l'IA — 30 min en présentiel.
- [Les différents types d'IA](it-1/differents-types-ia.md) : vocabulaire et tableaux de classement renseignés — 45 min en présentiel.
- [Le Machine Learning : apprendre à partir d'exemples](it-1/machine-learning-apprendre-exemples.md) : règles, test, faux positifs et négatifs, graphique et familles d'apprentissage ; missions renseignées.
- [Le Deep Learning](it-1/deep-learning.md) : neurones, couches, Playground, surapprentissage et LLM.
- [Comment fonctionne un LLM](it-1/comment-fonctionne-llm.md) : quatre missions renseignées, tokenisation, température, agents et sécurité — 1 h 30.
- [Les risques derrière les LLM](it-1/risques-derriere-llm.md) : secrets, injections, permissions et retour sur les usages ; essais Trippy Planner et Thingularity niveau 1 documentés, fiches renseignées.
- [Pense-bête de l'itération](../pense-bete/glossaire/ia-cybersecurite/it-1.md)

## Itération 2 — Shadow IA

**Travail individuel en autonomie — 1 jour.** Méthode d'analyse le matin, puis application au dossier de Nadia l'après-midi.

- [Sommaire, objectifs et livrables prévus](it-2/index.md)
- [Le recensement de Nadia](it-2/le-recensement-de-nadia.md) : retour sur les usages du J1 et définition initiale proposée.
- [Shadow IA : de quoi parle-t-on ?](it-2/shadow-ia-de-quoi-parle-t-on.md) : classement renseigné, définition corrigée, cas Samsung et méthode en sept étapes.
- [Quel compte, quel fournisseur ?](it-2/quel-compte-quel-fournisseur.md) : tableau OpenAI rempli, sources datées et réponses sur les comptes, l’API et le local.
- [Quelles données sont envoyées ?](it-2/quelles-donnees-sont-envoyees.md) : données sensibles du WMS classées, extrait caviardé et tableaux renseignés.
- [Les connecteurs : quand l’IA a les clés](it-2/connecteurs-quand-ia-a-les-cles.md) : permissions InboxPilot renseignées, révocation et analyse EchoLeak.
- [Ce que dit la PSSI](it-2/ce-que-dit-la-pssi.md) : tableau des dix situations, angles morts et analyse du délai de réponse.
- [Qualifier le risque et choisir une mesure](it-2/qualifier-risque-choisir-mesure.md) : trois risques qualifiés, mesures proposées et continuité du travail.
- [Le dossier Hexalp](it-2/le-dossier-hexalp.md) : livrable en quatre parties, dix fiches croisées sur les dix pièces et limites de preuve.
- [Pense-bête de l'itération](../pense-bete/glossaire/ia-cybersecurite/it-2.md)

## Itération 3 — Détecter : votre premier modèle

**Travail individuel, guidé puis en autonomie — 1 jour.** Environnement Python, préparation de journaux SSH fictifs, classification et détection d'anomalies avec Scikit-learn, puis script d'alertes pour l'analyste.

- [Contexte, objectifs, kit reçu et livrables](it-3/index.md)
- [Le projet de la supervision](it-3/le-projet-de-la-supervision.md) : cinq scénarios renseignés, limites de fail2ban et conditions du projet — 15 min.
- [Mettre en place un classifieur](it-3/mettre-en-place-classifieur.md) : chaîne du J1 et tableau classification/anomalies renseignés ; carnet J3 commencé — 45 min.
- [Installer son environnement](it-3/installer-son-environnement.md) : installation guidée et réponses théoriques ; six captures VM commentées et preuves restantes — 45 min.
- [Python de survie](it-3/python-de-survie.md) : tableaux et exercices corrigés, analyse de la machine nocturne — 1 h.
- [Explorer et préparer les journaux](it-3/explorer-preparer-journaux.md) : exploration renseignée, choix de nettoyage et caractéristiques — 45 min.
- [Le classifieur supervisé](it-3/le-classifieur-supervise.md) : entraînement attesté en captures, règles, C1–C6 et limites de l’arbre — 1 h.
- [La détection d’anomalies](it-3/la-detection-anomalies.md) : cellules dans l’ordre, quatre captures et analyse des résultats observés — 1 h.
- [Le script de détection](it-3/le-script-de-detection.md) : script et CSV produits, deux graines testées et fiche du modèle renseignée — 1 h.
- [Pense-bête de l'itération](../pense-bete/glossaire/ia-cybersecurite/it-3.md)

Les cinq fichiers du kit sont disponibles dans `livrables/ia-cybersecurite/it-3/ia01-j3/`. Les consignes détaillées suivantes sont attendues ; l’entraînement supervisé est désormais documenté par les captures de la partie C ; les autres résultats sont suivis dans le sommaire.

## 🎯 Objectifs

### Objectif global

Dans ce module, vous apprenez à sécuriser l'utilisation quotidienne des outils d'intelligence artificielle et à comprendre le fonctionnement d'un modèle de détection d'anomalies.

À partir d'un cas d'entreprise, vous identifiez les usages déclarés et non déclarés de l'IA, les données exposées et les contournements de la politique de sécurité. Vous étudiez notamment les risques liés aux comptes personnels, aux services publics, aux assistants de code, aux connecteurs et aux agents capables d'agir sur le système d'information.

Vous entraînez ensuite un premier modèle avec Scikit-learn à partir de journaux d'infrastructure. Vous apprenez à préparer les données, choisir des caractéristiques pertinentes, évaluer les résultats et reconnaître les limites du modèle. Vous comparez cette détection avec les mécanismes de supervision et les règles de sécurité déjà mis en œuvre dans les modules précédents.

Enfin, vous traitez un incident provoqué par un usage non autorisé de l'IA et vous produisez une politique d'utilisation sécurisée de l'intelligence artificielle, articulée avec la PSSI existante.

### Vous apprendrez à

- **Identifier** les usages de l'intelligence artificielle présents dans une organisation, y compris les usages non déclarés ;
- **Analyser** les risques liés aux données, aux comptes, aux fournisseurs, aux connecteurs et aux agents ;
- **Distinguer** l'utilisation d'un modèle, son entraînement et son exploitation ;
- **Préparer** des journaux d'infrastructure pour entraîner un modèle simple ;
- **Entraîner** un modèle de détection d'anomalies avec Scikit-learn ;
- **Mesurer** les performances du modèle et interpréter ses erreurs ;
- **Identifier** les biais, les faux positifs, les faux négatifs et les possibilités de contournement ;
- **Analyser** un incident lié à un usage non autorisé de l'IA ;
- **Définir** des règles d'utilisation sécurisée de l'intelligence artificielle.

## 🎓 En fin de module

Vous serez capables d'identifier les risques associés aux usages quotidiens de l'IA, d'analyser une situation de shadow AI, d'entraîner et d'évaluer un premier modèle de détection d'anomalies, de traiter un incident lié à une utilisation non autorisée et de formaliser une politique d'utilisation sécurisée de l'IA.

## 🔄 Démarche pédagogique

- **Analyser les usages existants** — Vous partez de vos pratiques quotidiennes pour identifier les outils utilisés, les données manipulées et les risques associés.
- **Identifier le shadow AI** — Vous recherchez les usages non déclarés et analysez leurs écarts avec les règles de sécurité de l'organisation.
- **Entraîner un premier modèle** — Vous préparez des journaux d'infrastructure et entraînez un modèle simple de détection d'anomalies avec Scikit-learn.
- **Évaluer le modèle** — Vous mesurez ses résultats, analysez ses erreurs et étudiez ses limites face à des données imparfaites ou manipulées.
- **Encadrer les usages** — Vous traitez un incident lié à l'IA et formalisez une politique d'utilisation sécurisée articulée avec la PSSI.

## Compétences développées

- **Analyser les usages de l'intelligence artificielle et leurs risques pour le système d'information** — Recenser les outils et les comptes utilisés, identifier les données manipulées, repérer les usages non déclarés et qualifier les écarts avec la PSSI.
- **Entraîner un modèle simple à partir de journaux d'infrastructure** — Préparer les données, sélectionner des caractéristiques pertinentes, choisir un algorithme Scikit-learn et entraîner un modèle reproductible.
- **Évaluer les performances et les limites d'un modèle de détection d'anomalies** — Interpréter les résultats, mesurer les faux positifs et les faux négatifs, étudier l'influence des paramètres et déterminer les conditions d'utilisation du modèle.
- **Analyser et traiter un incident lié à un usage non autorisé de l'intelligence artificielle** — Identifier les données et les ressources potentiellement exposées, collecter les éléments utiles, appliquer les premières mesures et proposer des actions correctives.
- **Définir des règles d'utilisation sécurisée de l'intelligence artificielle** — Déterminer les outils, comptes, données et usages autorisés, préciser les règles de validation humaine, de traçabilité et de signalement, puis articuler ces règles avec la PSSI.
