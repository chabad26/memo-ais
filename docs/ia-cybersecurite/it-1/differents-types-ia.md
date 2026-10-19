# Les différents types d'IA

## Le concept

« IA » est un mot-valise. Derrière lui se cachent des familles de techniques emboîtées comme des poupées russes. Pour les grands modèles de langage actuels étudiés dans ce module :

**LLM ⊂ Deep Learning ⊂ Machine Learning ⊂ Intelligence artificielle.**

Un LLM relève donc aussi du DL, du ML et de l'IA. L'inverse n'est pas vrai : un modèle de ML n'est pas nécessairement un réseau profond, et une IA peut reposer sur des connaissances et des règles explicites.

Il faut distinguer **la technique employée**, **la tâche réalisée** et **le système complet**. Un même produit peut associer un modèle appris, des règles, des seuils et des outils capables d'agir.

## Vocabulaire clé

| Terme | Ce que c'est concrètement | Repère pour ce module |
| --- | --- | --- |
| **Intelligence artificielle** | Domaine regroupant des méthodes pour réaliser des tâches associées à des capacités comme raisonner, percevoir ou traiter le langage ; certaines reposent sur des règles explicites. | Un système expert relève de l'IA ; une simple automatisation à seuil n'est pas automatiquement une IA. |
| **Machine Learning — ML** | Apprentissage automatique : les paramètres ou la structure d'un modèle sont ajustés à partir de données, plutôt que de définir chaque décision à la main. | Un filtre peut apprendre à distinguer spam et courrier légitime à partir d'exemples. |
| **Deep Learning — DL** | Sous-ensemble du ML utilisant des réseaux de neurones comportant plusieurs couches cachées. | Peut servir à reconnaître un visage comme à générer du texte. |
| **LLM** | Grand modèle de langage : modèle neuronal profond entraîné sur de grands corpus, notamment de texte et de code. | Le moteur génératif d'un assistant conversationnel ; l'application ajoute une interface et éventuellement des outils. |
| **Modèle discriminatif** | Modèle apprenant à distinguer des classes ou à prédire une cible à partir des données d'entrée. | Exemple : classer une connexion selon une catégorie apprise. Tout détecteur d'anomalies n'est cependant pas un classifieur supervisé. |
| **Modèle génératif** | Modèle apprenant une distribution des données et permettant de produire de nouveaux exemples ; certains modèles génératifs servent aussi à classer. | Un LLM génère du texte ou du code ; un modèle génératif peut aussi produire des images. |

Les définitions sont reformulées à partir du [glossaire de la CNIL](https://www.cnil.fr/fr/intelligence-artificielle/glossaire-ia), de sa définition de [l'apprentissage profond](https://cnil.fr/fr/definition/apprentissage-profond-deep-learning) et de celles des modèles [discriminatifs](https://www.cnil.fr/fr/definition/modele-discriminatif) et [génératifs](https://www.cnil.fr/fr/definition/modele-generatif).

!!! tip "Le repère pour le J3"
    Le programme annonce un modèle de détection d'anomalies : il devra attribuer un score ou une décision aux événements, plutôt que produire du texte ou des images. Selon l'algorithme choisi, cet apprentissage pourra se faire sans étiquettes « normal / attaque ». La documentation Scikit-learn distingue notamment [détection de valeurs aberrantes et détection de nouveautés](https://scikit-learn.org/stable/modules/outlier_detection.html). L'algorithme du TP reste à préciser avec sa consigne.

## Mission — Classement renseigné

Le tableau donne **un choix argumenté pour chaque ligne**. Pour les produits non identifiés, il s'agit d'une hypothèse pédagogique, à confronter à la documentation de l'outil réellement utilisé. La colonne « Apprend des données ? » concerne **la construction du modèle**, pas nécessairement un réentraînement pendant chaque utilisation.

| Système | Famille retenue : règles / ML / DL / LLM | Apprend des données ? | Classe ou génère ? | Argument et limite du choix |
| --- | --- | --- | --- | --- |
| **Une règle Fail2ban qui bannit une IP après 5 échecs SSH** | **Règles** ; automatisation déterministe | **Non** pour la règle décrite. | **Décide et agit** : bannit selon un seuil ; ne génère pas de contenu. | Le compteur est comparé à un seuil configuré, dans une fenêtre temporelle. Ce comportement ne suffit pas à qualifier Fail2ban d'IA. |
| **Une signature Suricata qui reconnaît un exploit connu** | **Règles** ; détection par signature | **Non** pour la signature décrite. | **Détecte** une correspondance et peut déclencher une alerte. | Les conditions de la signature sont explicites. Charger une nouvelle signature est une mise à jour de règles, pas un apprentissage du moteur sur nos logs. |
| **Le filtre antispam de votre messagerie** | **ML**, avec règles possibles ; hypothèse d'un filtre appris | **Oui**, sur des exemples de courriels pour sa partie ML. | **Classe** : spam / courrier légitime, éventuellement avec un score. | Un filtre bayésien est un exemple de ML sans DL. La messagerie réelle peut combiner réputation, listes, règles et modèles plus complexes ; son implémentation reste à vérifier. |
| **Un EDR qui repère un comportement inhabituel sur un poste** | **ML + règles** ; hypothèse d'une détection comportementale apprise | **Oui** si le profil ou le score est appris ; **non** pour une règle comportementale fixe. | **Détecte ou évalue** un comportement, puis peut déclencher une action. | « Inhabituel » ne prouve pas à lui seul l'emploi du ML. Un EDR est une solution complète : il faut identifier le moteur à l'origine de l'alerte. |
| **Le déverrouillage d'un téléphone par reconnaissance faciale** | **DL** pour un dispositif neuronal, tel que Face ID | **Oui**, lors de l'entraînement des réseaux ; l'enrôlement du visage est une étape distincte. | **Vérifie une identité** : correspondance / non-correspondance, puis autorisation ou refus. | Apple documente des réseaux neuronaux pour Face ID. Ce choix ne décrit pas tous les téléphones et ne signifie pas que le réseau est réentraîné à chaque déverrouillage. |
| **L'assistant conversationnel que vous utilisez le plus** | **LLM**, donc aussi DL et ML ; exemple documenté ici : Codex | **Oui**, lors de l'entraînement du modèle. Une réponse ne prouve pas une mise à jour de ses poids. | **Génère** du texte ou du code ; peut aussi répondre à une demande de classement. | Le classement porte sur le moteur de langage. Les usages de Codex sont visibles dans l'inventaire ; le fait qu'il soit l'assistant le plus utilisé du mois reste à confirmer. |
| **L'autocomplétion de code dans votre IDE** | **LLM** si assistant de code génératif ; **règles / analyse statique** si complétion classique | **Oui** pour le modèle génératif ; **non** pour la simple liste de symboles et les snippets fixes. | **Génère** une suite de code dans le premier cas ; **propose** des symboles connus dans le second. | Je retiens LLM sous l'hypothèse d'une complétion générative. Le nom de l'extension et son mode sont nécessaires pour trancher sur l'IDE réel. Aucun usage personnel de cette fonction n'est établi ici. |
| **Un système de détection de fraude à la carte bancaire** | **ML + règles** ; hypothèse d'un score de risque appris | **Oui** pour le modèle de score ; **non** pour les règles fixes. | **Évalue ou classe** une transaction ; peut conduire à une vérification ou un refus. | Je retiens ML pour le score et règles pour les contraintes explicites. Le nom du service ne permet pas de conclure à du DL ; les transactions et le moteur réels ne sont pas fournis. |
| **Une alerte Zabbix « disque plein à 90 % »** | **Règles** ; seuil de supervision | **Non** pour ce déclencheur. | **Évalue une condition** et déclenche une alerte ; ne génère pas de contenu au sens de l'IA générative. | Une expression compare l'occupation du disque à un seuil. Ce déclencheur précis n'apprend pas un profil normal, même si d'autres fonctions de supervision peuvent être plus élaborées. |

Les cas déterministes s'appuient sur les documentations de [Fail2ban — paramètres des jails](https://github.com/fail2ban/fail2ban/blob/master/man/fail2ban-client.1), [Suricata — format des signatures](https://docs.suricata.io/en/latest/rules/intro.html) et [Zabbix — expressions des déclencheurs](https://www.zabbix.com/documentation/current/en/manual/config/triggers/expression). Le cas biométrique prend pour exemple [Face ID — sécurité de la reconnaissance faciale](https://support.apple.com/en-ie/guide/security/sece151358d1/web). Les lignes EDR et fraude sont des choix pédagogiques conditionnels, sans audit d'un produit particulier.

## Les lignes discutables — Mon raisonnement

**Une règle n'est pas automatiquement une IA.** Une alerte à 90 % et un bannissement après cinq échecs illustrent une décision automatisée. Un système expert peut aussi fonctionner avec des règles, mais il organise une base de connaissances et un raisonnement : le seul mot « règles » ne suffit pas à identifier une IA.

**« Classe ou génère ? » décrit ici la sortie attendue.** Il ne permet pas toujours de déduire la famille mathématique du modèle : Naive Bayes est un modèle génératif que l'on peut utiliser pour classer des spams, et un LLM génératif peut fournir une étiquette en réponse à une consigne. La documentation [Scikit-learn sur Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html) décrit son apprentissage des probabilités et son usage antispam.

**Un produit peut combiner plusieurs familles.** Une règle fixe peut encadrer la décision d'un modèle appris. De même, un assistant peut générer une commande puis appeler un outil pour l'exécuter. L'exécution de cette commande est une action du système ; elle ne constitue pas, en elle-même, un apprentissage du modèle.

## Reprise de mes usages de l'activité 1.1

L'[inventaire initial](le-message-de-nadia.md) documente deux usages du même outil. Leur famille est renseignée ci-dessous, sans ajouter d'autres usages personnels supposés.

| Usage observé | Famille de l'outil ou du moteur | Apprend des données ? | Ce que je lui fais produire ou faire |
| --- | --- | --- | --- |
| **Codex — assistant conversationnel pour la rédaction** | **LLM → DL → ML → IA** | Le modèle a été entraîné en amont. L'échange observé ne démontre pas un réentraînement. | Générer et reformuler des supports pédagogiques, des tableaux et du Mermaid. |
| **Codex — agent intervenant dans le dépôt du mémo** | **LLM associé à des outils**, avec des permissions d'accès au dépôt et aux commandes | Le moteur repose sur un modèle appris ; lire un fichier ou lancer une commande ne prouve pas une modification de ses poids. | Lire et modifier des fichiers, mettre à jour la navigation et exécuter des vérifications à l'aide des outils disponibles. |

Le type de compte et les autres outils utilisés ce mois-ci restent à confirmer dans l'inventaire. La famille « LLM » ne renseigne pas à elle seule les conditions de conservation ou de réutilisation des données envoyées : ces points demandent une vérification du service et du compte utilisés.

## Résultat de la fiche

Le vocabulaire, les neuf systèmes et les deux usages déjà documentés sont renseignés. Les hypothèses sont explicites pour les systèmes non identifiés. Aucun EDR, filtre de messagerie, service bancaire ou modèle de TP n'a été audité ou testé dans cette activité documentaire.

## Ressources

- [CNIL — glossaire de l'intelligence artificielle](https://www.cnil.fr/fr/intelligence-artificielle/glossaire-ia)
- [Elements of AI — cours gratuit en français, chapitres 1 et 4](https://www.elementsofai.fr/) : ressource fournie dans la consigne ; contenu non consultable lors de cette vérification.

**Sources consultées le 19 octobre 2026.**

[Retour à l'itération](index.md)
