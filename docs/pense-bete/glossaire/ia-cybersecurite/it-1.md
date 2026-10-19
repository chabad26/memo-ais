# IA et Cybersécurité — Itération 1

## Termes à retenir

| Terme | Sens dans l'activité |
| --- | --- |
| RSSI | Responsable de la sécurité des systèmes d'information ; rôle de Nadia chez Hexalp |
| COMEX | Comité exécutif ; demande ici le développement des usages de l'IA |
| Usage de l'IA | Utilisation d'un outil ou d'une fonctionnalité d'IA, y compris intégrée à un IDE, un navigateur ou une messagerie |
| Type de compte | Personnel, professionnel ou aucun ; à relever pour chaque outil utilisé |
| Journaux ou logs | Événements enregistrés par les systèmes et applications ; contenus à identifier dans l'inventaire |
| IA à base de règles | Connaissances et règles explicites ; illustration historique : systèmes experts |
| Apprentissage automatique | Ajustement d'un modèle à partir de données ; illustration : Perceptron ou filtre antispam appris |
| Hiver de l'IA | Période de recul des soutiens et des attentes ; bornes variables selon les pays et les secteurs |
| Approche hybride | Combinaison à expliciter : profils statistiques et règles chez Denning, réseaux appris et recherche dans AlphaGo |
| Agent fondé sur un modèle de langage | Modèle associé à des outils pour interagir avec un environnement ; ReAct est un jalon de 2022 |
| Deep Learning — DL | Sous-ensemble du ML utilisant des réseaux de neurones avec plusieurs couches cachées |
| LLM | Grand modèle de langage ; les modèles actuels étudiés ici relèvent du DL, donc du ML et de l'IA |
| Modèle discriminatif | Apprend à distinguer des classes ou à prédire une cible à partir des entrées |
| Modèle génératif | Apprend une distribution et peut produire de nouveaux exemples ; peut aussi être utilisé pour classer |
| Inférence | Utilisation d'un modèle entraîné pour produire un résultat ; distincte de son entraînement |
| Observation / caractéristique / étiquette | Une ligne de données / une information utilisée pour prédire / la réponse de référence fournie pour l'apprentissage supervisé |
| Faux positif / faux négatif | Une activité normale signalée comme attaque / une attaque manquée par la règle |
| Jeu de test | Données gardées à l'écart pour évaluer une règle figée ; les utiliser pour l'améliorer impose ensuite une nouvelle évaluation indépendante |
| Renforcement | Apprentissage d'une politique d'action à partir d'interactions et de récompenses ou pénalités |
| Paramètre / hyperparamètre | Valeur apprise par le modèle / réglage encadrant l'apprentissage ; un seuil d'alerte peut être choisi séparément |
| Poids / biais | Paramètres du neurone : pondération des entrées / décalage ajouté à leur somme |
| Activation | Transformation de la somme pondérée ; sa non-linéarité permet aux couches de construire des frontières complexes |
| Couche cachée | Couche intermédiaire entre les entrées et la sortie ; elle apprend une représentation utilisée par les couches suivantes |
| Loss | Fonction de perte mesurant une erreur selon l'objectif choisi ; ce n'est pas directement un pourcentage d'erreurs |
| Surapprentissage / sous-apprentissage | Adaptation à des particularités qui généralisent mal / apprentissage insuffisant des relations utiles |
| Token / tokenizer | Unité représentée par un identifiant / mécanisme de découpage ; le nombre dépend du texte exact et de l'encodage |
| Fenêtre de contexte | Budget de tokens pris en compte pour une requête, avec les contraintes propres au modèle et au service |
| Température | Réglage de l'échantillonnage : valeur basse pour concentrer la distribution, élevée pour l'aplatir ; ne garantit pas la vérité |
| Hallucination | Contenu généré sans fondement factuel suffisant, notamment s'il est présenté comme une information vérifiée |
| SFT / RLHF | Affinage sur des démonstrations / optimisation à partir de préférences humaines, selon la recette du modèle |
| RAG | Recherche de contenus fournis ensuite dans le contexte ; distincte d'un réentraînement des poids sur les documents |
| Injection indirecte | Consigne malveillante placée dans un contenu externe pour détourner le traitement ou les actions de l'assistant |
| Permissions excessives | Capacités d'un connecteur ou agent dépassant ce que demande la tâche ; elles amplifient l'impact d'une erreur ou d'une injection |
| Slopsquatting | Publication d'un paquet malveillant sous un nom susceptible d'être inventé et recommandé par un modèle |
| Prompt système et secret | Une consigne de confidentialité n'est pas un coffre ni un contrôle d'accès externe au modèle |

## Gestes à retenir

1. Recenser les outils et fonctionnalités utilisés ce mois-ci, au travail comme ailleurs.
2. Préciser le type de compte et les catégories de contenus envoyés.
3. Inclure autocomplétion, extensions, traduction et assistants intégrés.
4. Signaler les informations à vérifier et conserver l'inventaire initial pour la fin de journée.
5. Décrire les contenus sans publier de données sensibles dans le mémo.
6. Pour la frise historique, vérifier chaque date sur deux sources et préciser le jalon retenu.
7. Justifier le classement des approches et signaler les cas hybrides ou les événements de contexte.
8. Distinguer famille technique, tâche réalisée et produit complet ; une alerte ou un score ne prouve pas l'emploi du ML.
9. Pour classer un outil, vérifier son moteur ; pour les usages observés, distinguer entraînement, génération et actions via outils.
10. Figer une règle avant le test ; compter FP et FN séparément et préciser le coût des actions déclenchées.
11. Une anomalie demande une qualification humaine ; un zéro erreur sur un petit jeu ne prouve pas la généralisation.
12. Dans Playground, commencer avec x₁ et x₂ seuls ; les entrées au carré peuvent rendre un cercle séparable sans couche cachée.
13. Comparer les pertes d'entraînement et d'évaluation sur la durée ; bruit et faible quantité de données ne garantissent pas à eux seuls un surapprentissage visible.
14. Noter architecture, activation, graine, part d'entraînement, bruit et époques pour comparer les essais ; le temps dépend du navigateur et de la machine.
15. Pour compter les tokens, conserver texte exact, encodage et périmètre : texte seul ou conversation complète.
16. Ne pas confondre probabilité d'un token, vérité d'une réponse et autorisation d'une action.
17. Préserver l'origine des documents et faire contrôler les appels d'outils par l'application ; un prompt système seul ne garantit pas la résistance aux injections.
18. Distinguer utiliser, entraîner et exploiter ; le conditionnement par un prompt n'implique pas une mise à jour des poids.
19. Pour un risque, relier mécanisme, scénario, impact, indices, mesures technique et organisationnelle, puis référence précise.
20. Pour les connecteurs, vérifier les droits effectifs et les destinataires ; conserver des traces utiles sans recopier de secrets dans les journaux publics.
21. Réserver les essais de contournement au laboratoire et au périmètre autorisé ; documenter les refus autant que les réussites réelles.

## Manipulations faites

Une première version de l'inventaire décrit les usages de Codex observés pendant la création du module. Le type de compte et les autres usages du mois restent à confirmer. Aucun entraînement sur les journaux d'Hexalp ni analyse technique de l'incident du scénario ne sont documentés à ce stade.

La fiche historique comprend une frise Mermaid verticale renseignée, deux références par jalon et des réponses documentaires aux trois questions. Ce travail ne constitue pas un entraînement de modèle ni un test de détection.

La fiche sur les types d'IA contient le classement argumenté des neuf systèmes et des deux usages de Codex observés. Les produits non identifiés sont traités comme des hypothèses pédagogiques.

L'exercice manuel de ML est résolu et ses calculs vérifiés sur les 18 observations fournies : le seuil « échecs > 20 » donne 0 erreur d'entraînement, puis 2 FP et 2 FN sur le test. Le graphique et les règles exploratoires ne constituent pas un entraînement Scikit-learn ni une mesure sur un SI réel.

Six essais Playground ont été exécutés par l'assistant sur des données synthétiques, avec captures et relevé des réglages : cercle, spirale, puis bruit et faible part d'entraînement. Avec quatre neurones cachés sur le cercle, la perte de test affichée atteint 0.013 après 500 époques, contre 0.521 sans couche cachée. Ces résultats ne sont pas des mesures sur les logs d'Hexalp ni des manipulations attribuées à l'apprenant.

La fiche LLM comprend cinq comptages locaux avec tiktoken 0.14.0 et deux encodages, ainsi qu'une comparaison des températures recalculée sur les logits GPT-2 pré-calculés publiés par Transformer Explainer. Aucune nouvelle inférence sur le prompt de mot de passe Hexalp ni lecture ou transmission d'une configuration n'est attestée.

Trois fiches risques sont renseignées pour les secrets, les injections indirectes et les permissions excessives, avec références ANSSI et OWASP 2025. Le retour sur les usages de Codex est une analyse de risques possibles. Deux captures de l'apprenant documentent des défis **Agent Breaker de niveau 1**, chacun validé à **100/100** : **Trippy Planner**, injection indirecte et lien de phishing repris dans la réponse ; **Thingularity**, demande directe d'inventaire des outils internes, dont les détails sont partiellement masqués. Aucun clic, opération commerciale, vol de données, mot de passe Gandalf obtenu ni contrôle déployé chez Hexalp n'est attesté. La connaissance du nom d'un outil ne doit pas conférer le droit de l'exécuter.

## Docs associées

- [Module](../../../ia-cybersecurite/README.md)
- [Itération 1 — Sous le capot de l'IA](../../../ia-cybersecurite/it-1/index.md)
- [Le message de Nadia et inventaire des usages](../../../ia-cybersecurite/it-1/le-message-de-nadia.md)
- [70 ans d'intelligence artificielle](../../../ia-cybersecurite/it-1/70-ans-intelligence-artificielle.md)
- [Les différents types d'IA](../../../ia-cybersecurite/it-1/differents-types-ia.md)
- [Le Machine Learning : apprendre à partir d'exemples](../../../ia-cybersecurite/it-1/machine-learning-apprendre-exemples.md)
- [Le Deep Learning](../../../ia-cybersecurite/it-1/deep-learning.md)
- [Comment fonctionne un LLM](../../../ia-cybersecurite/it-1/comment-fonctionne-llm.md)
- [Les risques derrière les LLM](../../../ia-cybersecurite/it-1/risques-derriere-llm.md)
