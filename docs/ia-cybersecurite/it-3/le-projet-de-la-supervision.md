# Le projet de la supervision

**15 min — Présentiel**

## Le message de Nadia

Votre inventaire d'hier a fait son effet. **Dans la suite du scénario**, le script de Sofia qui envoyait les alertes Zabbix à une API publique a été coupé et sa clé révoquée. Le besoin qui l'avait fait naître reste présent.

> **Nadia [10:05]** Le script de Sofia, c'est fini 🔒  
> Mais elle avait raison sur un point : l'astreinte est noyée sous les alertes et fail2ban ne voit pas tout.  
> La supervision veut tester un modèle de détection sur les logs SSH du bastion.  
> Mes conditions : **tout tourne chez nous, aucune donnée ne sort, et le modèle ne bloque rien tout seul**.  
> Et je veux comprendre ce qu'il fait avant de l'écouter. Vous vous en chargez ? 🙂

L'arrêt et la révocation sont des faits annoncés par ce nouveau contexte fictif, pas des opérations exécutées par l'assistant ni des preuves collectées sur un serveur réel. Ils prolongent les actions proposées au J2 sans réécrire leur statut à cette date.

**Objectif :** identifier ce que la protection actuelle détecte déjà et ce qu'une analyse complémentaire pourrait apporter, avant de construire un modèle.

## Mission — Ce que fail2ban voit déjà

Sur le bastion, la règle fournie bannit une adresse IP après **5 échecs d'authentification en 10 minutes**. Les réponses supposent une jail SSH active, un filtre qui reconnaît les échecs concernés, une IP non exemptée et une action de bannissement fonctionnelle. « Détecté » désigne ici le franchissement de ce seuil, pas la reconnaissance certaine d'une intention malveillante.

| N° | Scénario | fail2ban le voit-il ? | Pourquoi ? |
| --- | --- | --- | --- |
| **1** | Un robot teste 200 mots de passe sur `root` en une heure | **Oui si les échecs viennent de la même IP et atteignent le bastion surveillé** | Le seuil de cinq échecs en dix minutes est atteint bien avant 200 tentatives. Le bannissement devrait ensuite empêcher une partie des essais ; les 200 représentent la tentative décrite, pas nécessairement 200 authentifications effectivement traitées après blocage. Une attaque répartie entre de nombreuses IP demanderait une autre analyse |
| **2** | Un mot de passe courant testé sur six comptes, un essai toutes les dix minutes | **Non avec cette règle** | En supposant un essai total toutes les dix minutes, la même IP reste sous cinq échecs dans la fenêtre. Changer de compte ne remet pas le compteur IP à zéro ; c'est ici le faible rythme qui permet l'évitement. Six essais rapprochés depuis la même IP seraient au contraire détectables |
| **3** | Connexion réussie du premier coup avec identifiants volés, à 23 h, puis sortie de 1 Go | **Non avec la règle d'échecs SSH** | Aucun échec à compter. L'horaire, l'identité usurpée et le volume sortant ne sont pas évalués par ce seuil. La réussite peut figurer dans les logs sans déclencher ce bannissement |
| **4** | Un poste interne compromis teste dix comptes de service sur les serveurs de production | **Pas nécessairement ; hors visibilité du bastion si accès direct** | Le caractère interne de l'IP ne suffit pas à l'exempter. Si cinq échecs d'une même IP sont visibles en dix minutes sur un hôte protégé, sa jail peut réagir. Mais les logs du bastion ne voient pas automatiquement les authentifications directes aux serveurs de production ; des essais répartis entre hôtes ne sont pas automatiquement additionnés |
| **5** | Le scanner Hexalp réalise son audit mensuel : 150 échecs en une heure | **Oui sous les mêmes conditions que le scénario 1, sauf exemption configurée** | Le nombre d'échecs d'une même IP dépasse le seuil si ces événements sont surveillés. La règle ne sait pas qu'un audit est autorisé : un bannissement serait un faux positif du point de vue de l'intention malveillante, même si elle applique correctement son seuil |

Référence technique : [configuration officielle fail2ban, paramètres `findtime`, `maxretry`, `ignoreip` et jails](https://github.com/fail2ban/fail2ban/blob/master/config/jail.conf), consultée le **21 octobre 2026**. Les valeurs **5 / 10 minutes** viennent de la consigne Hexalp ; elles ne sont pas présentées comme une configuration relevée sur un serveur.

## 1. Où un modèle pourrait-il faire mieux ?

| Scénario | Apport possible et informations nécessaires | Limite à vérifier |
| --- | --- | --- |
| **1 — Force brute rapide** | Compter les échecs, les comptes distincts et leur évolution ; éventuellement corréler plusieurs IP et hôtes | La règle traite déjà bien le cas simple ; un modèle doit démontrer un bénéfice plutôt que le supposer |
| **2 — Essais lents sur plusieurs comptes** | Agréger sur une durée plus longue, observer le nombre de comptes distincts et la répétition des essais par source | Une agrégation trop courte ou des caractéristiques limitées au volume d'échecs peuvent manquer ce comportement. Une règle de corrélation pourrait aussi le détecter |
| **3 — Connexion valide et exfiltration** | Heure inhabituelle pour ce compte, source nouvelle, première utilisation, durée de session, destination et volume sortant ; croisement logs SSH et télémétrie réseau | Si le CSV ne contient que des échecs SSH, il ne permet pas de détecter la sortie de 1 Go. Un horaire tardif n'est pas à lui seul une attaque |
| **4 — Mouvement depuis un poste compromis** | Source interne inhabituelle, nombre de serveurs et comptes ciblés, échecs/succès et chronologie, avec journaux des serveurs de production | Un modèle entraîné uniquement sur le bastion ne voit pas les événements absents de ses données. Il faut une collecte adaptée avant tout algorithme |
| **5 — Audit autorisé** | Reconnaissance d'un comportement habituel du scanner, rapproché de l'inventaire, de la fenêtre d'audit et de l'autorisation | Un modèle d'anomalies peut signaler l'audit mensuel comme rare ; un classifieur peut aussi se tromper. La connaissance métier est nécessaire |

Le bénéfice est surtout plausible pour **2, 3 et 4**, avec des données suffisantes, et pour **5** si le contexte aide à réduire les alertes inutiles. Il n'est pas encore mesuré. Après réception du kit, le CSV fournit notamment l’heure, les comptes distincts, les succès, la durée des sessions et les octets sortants. Il ne fournit pas de compte utilisateur individuel ni d’hôte destination : les corrélations par compte et entre serveurs décrites ici demanderaient d’autres données. La sélection et l’évaluation effectives des caractéristiques restent à réaliser.

**Une règle peut aussi utiliser plusieurs caractéristiques et plusieurs fenêtres.** Le modèle apprend certaines relations à partir des données ; il ne gagne ni visibilité ni compréhension métier par sa seule présence. Les deux approches peuvent se compléter.

## 2. Le scanner réalise-t-il une attaque ?

**Dans le scénario 5, c'est un audit autorisé**, pas une attaque malveillante. Techniquement, ses essais peuvent pourtant ressembler à ceux d'un attaquant. Le nombre d'échecs seul ne permet pas de les distinguer.

Pour qualifier l'alerte, l'analyste doit rapprocher **source réellement utilisée, identité du scanner, fenêtre de changement, périmètre et autorisation d'audit**. Une règle peut intégrer une exception contrôlée ; un modèle supervisé peut apprendre à partir d'exemples d'audits bien étiquetés. Aucun de ces mécanismes ne prouve que tout trafic d'une IP connue est légitime : un scanner peut être compromis ou sortir du périmètre prévu.

Préférer une exception **limitée, documentée, surveillée et révisable** à une confiance permanente. Conserver les traces même si l'alerte est dépriorisée. Un détecteur d'anomalies signale un écart au comportement appris ; il ne connaît pas automatiquement l'autorisation donnée par Hexalp.

## Tableau à conserver pour le bilan de fin de journée

| Scénario | Résultat attendu de la règle dans les hypothèses ci-dessus | Classifieur J3 — résultat observé | Détecteur d'anomalies J3 — résultat observé |
| --- | --- | --- | --- |
| **1** | Oui, sous conditions de source et de collecte | **Non testé** | **Non testé** |
| **2** | Non pour le rythme décrit | **Non testé** | **Non testé** |
| **3** | Non pour cette règle | **Non testé** | **Non testé** |
| **4** | Dépend de la collecte et du rythme par hôte | **Non testé** | **Non testé** |
| **5** | Oui, sauf exemption ; audit légitime | **Non testé** | **Non testé** |

Les cellules « Non testé » reflètent l'état réel du travail, et non des réponses laissées à deviner. Au bilan, ne conclure que pour des scénarios représentés par les données et caractéristiques utilisées. Sinon noter **non évaluable avec ce jeu**, puis préciser ce qui manque.

## Conditions du projet à retenir

- Traitement local dans le périmètre Hexalp, sans envoi des journaux vers un service externe.
- Prédictions et alertes destinées à un analyste ; aucun bannissement automatique par le modèle.
- Explication de la préparation, des caractéristiques et des erreurs avant tout usage opérationnel.
- Aucun entraînement, test de détection ou changement de configuration fail2ban n'a été exécuté pour cette fiche.

[Retour à l'itération 3](index.md)
