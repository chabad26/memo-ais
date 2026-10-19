# Le message de Nadia

## Inventaire de mes usages de l'IA — Première version

En tête de votre document, listez les outils d'IA que vous avez utilisés **ce mois-ci**, au travail comme ailleurs. Pour chacun, notez le compte utilisé et ce que vous lui avez envoyé.

**Mois observé :** octobre 2026. **Date de l'inventaire :** 19 octobre 2026.

Cette première version est renseignée à partir de l'échange consacré à ce module. Elle reste à compléter pour couvrir l'ensemble du mois, au travail comme ailleurs. Les deux lignes ci-dessous décrivent deux usages du même outil.

| Outil ou fonctionnalité d'IA utilisé | Contexte : travail ou ailleurs | Compte utilisé : personnel, professionnel, aucun | Éléments envoyés : texte, code, logs, configuration, fichiers |
| --- | --- | --- | --- |
| Codex — assistant conversationnel pour la rédaction | Formation AIS : structuration du mémo et des supports pédagogiques | À vérifier : personnel ou professionnel | Texte : programme du module « IA et Cybersécurité », objectifs, compétences, scénario Hexalp et consignes de l'itération 1 |
| Codex — agent intervenant dans le dépôt du mémo | Formation AIS : création de pages Markdown, mise à jour de la navigation et vérification du site MkDocs | Même compte ; type à vérifier | Fichiers du dépôt rendus accessibles et consultés : pages Markdown, index et configuration `mkdocs.yml` ; sorties des commandes de vérification |

Ajoutez une ligne par outil ou fonctionnalité. Si une information est inconnue, indiquez **« à vérifier »**. Vous reviendrez sur cet inventaire en fin de journée.

**Famille des outils recensés :** Codex en mode conversationnel repose sur un **LLM**, donc aussi sur le **Deep Learning** et le **Machine Learning**. L'usage comme agent associe ce moteur à des outils de lecture, d'édition et d'exécution. Le [tableau de reprise des usages](differents-types-ia.md#reprise-de-mes-usages-de-lactivite-11) précise la famille et la finalité des deux lignes.

[Retour sur les risques de ces deux usages et les pratiques à améliorer](risques-derriere-llm.md#mission-3-retour-sur-mes-usages-de-lactivite-11) : analyse des risques possibles, sans présumer une fuite ni un usage réel chez Hexalp.

!!! tip "Pensez large"
    L'autocomplétion de votre IDE, une extension de navigateur, la traduction automatique ou l'assistant intégré à votre messagerie sont aussi de l'IA.

!!! note "Documenter les usages"
    Décrivez les contenus envoyés sans publier de logs bruts, de configurations internes, de données personnelles, de mots de passe ou de tokens. Les autres outils éventuellement utilisés (chatbot, autocomplétion, traduction, extension ou assistant de messagerie) et leurs comptes restent à confirmer. Le partage de logs et de configuration par un administrateur d'Hexalp appartient au scénario pédagogique ; il n'est pas attribué à vos usages personnels.

## Contexte — Hexalp

Vous venez d'intégrer l'équipe infrastructure d'**Hexalp**, une entreprise de logistique de **300 salariés répartis sur trois sites**. Le SI est stable, la supervision tourne, les sauvegardes aussi.

Il est **8 h 52**. Vous n'avez pas encore fini votre café quand un message de **Nadia, la RSSI**, s'affiche :

> **Nadia [08:52] Bonjour l'équipe !**
>
> Le COMEX veut « de l'IA partout » d'ici la fin de l'année 🙃
>
> La supervision veut tester un modèle qui détecte les anomalies dans nos logs
>
> Et j'ai appris hier qu'un admin a collé des logs et une conf dans un chatbot public pour débugger un incident…
>
> Avant de décider quoi que ce soit, j'ai besoin que vous compreniez ce qu'il y a sous le capot
>
> Pas besoin d'être data scientist. Mais je veux que vous sachiez m'expliquer comment ça marche, et pourquoi c'est risqué
>
> Point demain matin ☕

Vous relisez le message. Vous utilisez l'IA tous les jours. Mais si Nadia vous demandait ce qui se passe réellement quand vous appuyez sur Entrée, vous seriez bien en peine de lui répondre.

## Mission

Complétez l'inventaire placé en tête de cette page avec les outils utilisés ce mois-ci, au travail comme ailleurs, le type de compte et les catégories de contenus envoyés. Conservez cette première version pour y revenir en fin de journée.

**Résultat attendu :** un inventaire initial renseigné à partir de vos usages réels. Les usages non vérifiés restent signalés comme tels.

[Retour à l'itération](index.md)
