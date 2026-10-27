# 1.4 — Atelier 4 | Observer des dysfonctionnements et leurs conséquences

## Objectif et modalité

**Comprendre les relations entre défauts techniques, comportement du contrôleur et conséquences sur le processus physique.** Expérimentation en binôme et analyse des résultats.

La procédure s’applique au laboratoire Python/Modbus de l’[atelier 1.3](prendre-en-main-modele-frigorifique.md). Les réponses ci-dessous reposent sur le code fourni, un calcul local du modèle et **deux captures utilisateur de l’atelier 1.4**. Elles attestent l’injection puis la suppression du défaut, ainsi que les états associés du compresseur. La mise en commun et les relevés chronométrés restent à compléter.

## 1 — Simuler une défaillance du capteur

### Préparation et injection

Laisser le serveur et la supervision en fonctionnement, puis utiliser le terminal client depuis :

```text
livrables/informatique-industrielle/it-1/ot-refrigeration-poc/
```

Vérifier et restaurer les conditions de départ :

```bash
python3 -m lab.client setpoint 4
python3 -m lab.client door 0
python3 -m lab.client sensor-fault 0
python3 -m lab.client status
```

Attendre une phase de marche du compresseur si l’on souhaite observer son passage de marche à arrêt, puis injecter :

```bash
python3 -m lab.client sensor-fault 1
python3 -m lab.client status
```

Répéter `status` après quelques secondes et observer en parallèle `http://127.0.0.1:18080`.

### Ce qu’il faut observer

| Élément | Comportement déterminé par le code | Relevé utilisateur |
| --- | --- | --- |
| Indication du défaut | Le client affiche `sensor_fault=1`. L’injection écrit la coil Modbus d’adresse **1**. | Injection acceptée visible ; lecture `status` du défaut non capturée. |
| Compresseur | Au prochain pas de simulation, le défaut force `compressor=False`, avant toute régulation automatique. Un compresseur déjà arrêté reste arrêté. | OFF à 5 °C après injection ; ON à 5,2 °C après suppression. |
| Température | Le refroidissement cesse ; avec une enceinte autour de 4 °C et une ambiance à 22 °C, la température remonte progressivement. | 5 puis 5,2 °C sur les deux captures ; trajectoire et temps de réponse non mesurés. |
| Supervision | La page conserve température, consigne, compresseur, porte et alarme haute ; **elle n’affiche pas le défaut capteur**. | Deux captures conjointes supervision/commandes intégrées ci-dessous ; lecture `status` non visible. |
| Alarme haute température | Calcul distinct du défaut : déclenchement seulement après température > 8 °C pendant au moins 10 secondes de simulation. | `Alarm: none` sur les deux captures ; cela ne signifie pas absence de défaut capteur. |

Dans `lab/model.py`, la branche `if self.sensor_fault` arrête le compresseur. Le modèle continue pourtant à calculer et publier sa température : il ne simule pas ici une mesure figée, absente ou aberrante. Le client peut lire le défaut dans l’input register **3** ; `lab.dashboard` lit ce registre parmi les quatre input registers, mais **ne l’inclut ni dans son API JSON ni dans son affichage HTML**.

Une valeur de température encore affichée n’est donc pas une preuve de validité d’un capteur réel. De même, le nom `alarm` désigne ici l’alarme haute température, pas une synthèse de tous les défauts.

### Réponses aux quatre questions

#### 1. Pourquoi le contrôleur ne peut-il plus appliquer normalement sa régulation ?

Une régulation fondée sur une mesure défaillante ne peut plus se fier normalement à cette mesure. Dans ce laboratoire, le booléen de défaut déclenche une règle explicite : arrêter le compresseur et ne pas appliquer la branche d’hystérésis tant que le défaut est actif. Ce n’est pas une disparition réelle de la température calculée : c’est une décision programmée pour le scénario.

#### 2. Quelles conséquences l’arrêt du compresseur peut-il avoir ?

Dans les conditions du modèle, l’enceinte se réchauffe vers l’ambiance. Une température durablement supérieure à 8 °C déclenche l’alarme temporisée. À court terme, l’absence d’alarme haute reste possible malgré le défaut.

Pour une installation réelle, les conséquences possibles seraient une température hors plage, une dégradation des produits, une perte économique ou une interruption d’activité. Elles dépendent des produits, des durées d’exposition, de l’inertie thermique et des dispositifs de secours. Les seuils du laboratoire ne permettent pas de décider de la conformité de produits alimentaires.

#### 3. Quelles autres réactions pourrait-on envisager selon la conception réelle ?

- Basculer sur une mesure redondante validée et signaler le défaut.
- Détecter une incohérence entre plusieurs mesures et passer dans un mode dégradé conçu à cet effet.
- Appliquer une commande de secours limitée dans le temps, si elle a été étudiée et validée pour le procédé.
- Mettre l’installation dans un état de sécurité défini par son analyse de risques, avec intervention de l’exploitation.
- Prévoir une alerte dédiée, un contrôle local indépendant ou un dispositif de froid de secours.

Ce sont des **options à étudier**, pas des protections présentes dans le laboratoire. Continuer à refroidir, maintenir une dernière commande ou arrêter peuvent chacun présenter des risques selon la conception. L’arrêt du compresseur choisi ici n’est pas une règle universelle de sûreté frigorifique.

#### 4. Quelles informations faut-il avant de décider d’une intervention ?

| Information à obtenir | Utilité pour la décision |
| --- | --- |
| Température mesurée indépendamment, qualité et ancienneté des données | Évaluer l’état physique sans dépendre uniquement du capteur signalé défaillant. |
| Type de défaut : capteur, alimentation, câblage, communication ou entrée du contrôleur | Localiser la défaillance et éviter un remplacement ou un redémarrage injustifié. |
| Produits stockés, limites applicables, durée d’exposition et inertie | Estimer l’urgence et les mesures de préservation à faire valider. |
| Mode de repli prévu, protections, redondances et état des actionneurs | Comprendre les conséquences de l’intervention. |
| Documentation constructeur, schémas, versions et modifications récentes | Préparer un diagnostic adapté à l’installation. |
| Responsable d’exploitation, mainteneur compétent et procédure d’intervention | Déterminer qui autorise, réalise et surveille l’action. |
| Sauvegarde des paramètres, solution de secours et retour arrière | Réduire les conséquences d’une action qui échouerait. |

### Supprimer le défaut et vérifier la reprise

```bash
python3 -m lab.client sensor-fault 0
python3 -m lab.client status
```

Vérifier `sensor_fault=0`, consigne à 4 °C et porte fermée. La régulation reprend au pas suivant si `auto=1`. Le compresseur ne redémarre pas nécessairement immédiatement : sa décision dépend de la température et de l’hystérésis. À partir de 4,5 °C, il redémarre ; dans la bande intermédiaire, il peut rester arrêté.

### Captures utilisateur — défaut puis reprise de la régulation

**Le point visuel à retenir : la température dépasse non seulement la consigne de 4 °C, mais aussi le seuil normal de démarrage de 4,5 °C, tandis que le compresseur reste arrêté lorsque le défaut est injecté.** Après suppression du défaut, le compresseur est à nouveau en marche.

#### 11:25:05 — Défaut injecté : 5 °C, compresseur arrêté

![Défaut injecté : 5 °C, compresseur arrêté](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2011-25-05.png)

La commande `python3 -m lab.client sensor-fault 1` reçoit **`write accepted`**. La supervision affiche **5 °C**, consigne **4 °C**, compresseur **OFF**, porte **CLOSED** et **`Alarm: none`**. À 5 °C, le seuil de démarrage normal est dépassé : l’arrêt est cohérent avec la priorité donnée au défaut dans le code. La page ne signale pourtant pas explicitement le défaut capteur. La capture atteste cet état au moment de la prise de vue, pas sa durée ni une courbe complète de hausse sous défaut.

#### 11:25:31 — Défaut supprimé : 5,2 °C, compresseur en marche

![Défaut supprimé : 5,2 °C, compresseur en marche](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2011-25-31.png)

La commande `python3 -m lab.client sensor-fault 0` reçoit **`write accepted`**. La supervision affiche **5,2 °C**, consigne **4 °C**, compresseur **ON**, porte **CLOSED** et **`Alarm: none`**. La reprise est cohérente avec la régulation normale au-dessus de 4,5 °C. Une température encore élevée au moment de la reprise ne signifie pas que le refroidissement a échoué : l’effet thermique est progressif.

Les températures affichées passent de **5 à 5,2 °C** entre les deux images. La seconde est prise après suppression du défaut : ces seuls instantanés ne permettent pas d’attribuer toute la hausse à une période précise ni de chronométrer le redémarrage. Les heures proviennent des noms des fichiers. Aucun relevé `status` ne montre directement `sensor_fault` ou `auto` ; les commandes acceptées, les états affichés et le code constituent ici les éléments d’analyse.

### Calcul local réalisé le 26 octobre 2026

Vérification par import direct de `Plant`, sans réseau ni navigateur : départ à **4 °C**, compresseur en marche, porte fermée, consigne 4 °C, mode automatique ; injection avec `write_coil(1, 1)` puis appels à `advance(0.1)`.

| Étape | Résultat observé dans le calcul |
| --- | --- |
| Après écriture du défaut, avant le prochain pas | Défaut actif ; compresseur encore en marche. |
| Après un pas de 0,1 s simulée | Compresseur arrêté ; température arrondie à 4,00 °C. |
| Après 60 s simulées de défaut | Température **4,74 °C**, compresseur arrêté, défaut actif, aucune alarme haute. |
| Suppression du défaut puis un pas supplémentaire | Défaut inactif, compresseur en marche, température arrondie à 4,74 °C. |

Ces durées sont calculées, sans attente réelle. Elles attestent le comportement du modèle dans ces conditions initiales, pas les observations du binôme. La suite de 12 tests déjà exécutée à l’atelier 1.3 comprend aussi un test de réaction au défaut ; elle reste une preuve distincte.

## 2 — Analyser les cinq scénarios

### Situation A — Le navigateur n’affiche plus les températures, mais le contrôleur fonctionne

**Composants concernés :** navigateur, interface HTTP, service de supervision ou liaison de lecture Modbus. La panne d’affichage ne localise pas à elle seule le défaut.

**Contrôle et processus :** le scénario indique que le contrôleur fonctionne. Dans ce laboratoire, si `lab.server` reste actif, il peut poursuivre la régulation sans `lab.dashboard`. L’opérateur perd toutefois la visibilité de cette interface et peut ne plus voir une alarme.

**Diagnostic :** comparer `python3 -m lab.client status` avec le navigateur ; vérifier l’accès HTTP local, les messages du terminal de supervision et les écoutes. Une page qui s’ouvre peut malgré tout afficher `PLC unavailable` si les requêtes échouent. Distinguer l’échec du navigateur, du service HTTP et de sa connexion au serveur Modbus.

**Avant intervention :** conserver un moyen de surveillance valide ; privilégier un diagnostic ciblé avant tout redémarrage. La documentation établit la séparation des processus du laboratoire ; l’existence d’une IHM de secours, de notifications et d’une autonomie comparable en production doit être confirmée avec l’exploitation.

### Situation B — La température augmente alors que la supervision reste accessible

**Composants concernés :** procédé, porte, capteur, contrôleur, commande ou compresseur ; l’accessibilité de la supervision ne désigne pas la cause.

**Contrôle et processus :** une hausse peut être normale si le compresseur est arrêté dans la bande d’hystérésis. Elle peut aussi accompagner une porte ouverte, un défaut capteur qui arrête le compresseur, une consigne modifiée ou une autre anomalie. Dans un système réel, une commande de marche ne prouve pas que le compresseur produit effectivement du froid ; le laboratoire utilise un booléen et ne simule pas toutes les pannes mécaniques.

**Diagnostic :** relever la tendance et sa durée, consigne, compresseur, porte, mode automatique, défaut et alarme. Comparer CLI et supervision, puis utiliser si possible une mesure indépendante sur l’installation réelle. Le défaut capteur n’étant pas affiché par le tableau de bord fourni, la lecture CLI est nécessaire à cette vérification dans le TP.

**Avant intervention :** qualifier l’état physique et l’urgence avec l’exploitation ; ne pas modifier la consigne pour masquer le symptôme. Les tolérances des produits, les secours et les actions de préservation doivent être confirmés par les responsables.

### Situation C — Un administrateur souhaite redémarrer le serveur de supervision

**Composants concernés :** machine hôte, service de supervision et tous les services partageant cet hôte.

**Contrôle et processus :** arrêter seulement `lab.dashboard` prive de l’affichage mais laisse `lab.server` poursuivre ses calculs. **Redémarrer la machine Linux qui héberge les deux interrompt également le contrôleur simulé et le modèle physique.** Dans le laboratoire, la simulation ne progresse pas pendant cet arrêt et un nouveau serveur crée une nouvelle instance avec les valeurs par défaut ; cela ne reproduit pas l’évolution d’une enceinte réelle pendant une panne informatique.

**Diagnostic :** préciser si « serveur » désigne le service ou la machine ; inventorier les dépendances et vérifier où s’exécutent commande, alarmes et historisation éventuelle.

**Avant intervention :** faire valider une fenêtre, prévoir la surveillance durant l’indisponibilité et les contrôles de reprise. Les cohébergements du laboratoire sont établis par le code ; ceux de l’installation réelle et son comportement en perte de serveur doivent être confirmés avec ses responsables. Ne pas redémarrer l’hôte sur la seule hypothèse que « ce n’est que l’affichage ».

### Situation D — Une nouvelle version du contrôle nécessite un redémarrage

**Composants concernés :** logiciel de contrôle, environnement d’exécution et équipements pilotés.

**Contrôle et processus :** le redémarrage interrompt la commande exécutée par le composant concerné. Une nouvelle version peut changer les échanges, les paramètres, les temporisations ou les règles. Pour le serveur Python, un relancement recrée le modèle par défaut ; une installation réelle peut avoir des sorties de repli et des variables rémanentes différentes.

**Diagnostic :** identifier les versions, le motif du changement, la compatibilité, les corrections et les effets attendus. La seule disponibilité d’une nouvelle version ne prouve ni son urgence ni sa validation pour ce procédé.

**Avant intervention :** préparer sauvegarde du programme et des paramètres, essais hors production, validation du mainteneur/constructeur selon le cas, fenêtre autorisée, retour arrière et contrôle de reprise. L’état des sorties pendant l’arrêt, l’acceptabilité de l’interruption et les conditions de remise en service doivent être confirmés avec automaticiens et exploitation. Aucun essai de mise à jour n’est réalisé dans cet atelier.

### Situation E — Un prestataire souhaite modifier la consigne à distance

**Composants concernés :** poste et compte du prestataire, accès distant, chemin de maintenance et contrôleur.

**Contrôle et processus :** une modification acceptée change les seuils de régulation ; la température évolue ensuite selon le procédé. Le laboratoire accepte directement des consignes de 0 à 50 °C. La limite conseillée de 8 °C dans le registre holding 1 n’est pas une borne imposée par le logiciel. Cette possibilité technique ne vaut pas autorisation métier.

**Diagnostic :** connaître l’identité, le mandat, la raison du changement, la valeur actuelle et demandée, les plages autorisées et les dépendances. Le serveur fourni écoute par défaut en local, sans authentification Modbus : un accès externe du prestataire n’est pas configuré ni démontré par ce TP.

**Avant intervention :** faire approuver la valeur et l’horaire par l’exploitation, limiter l’accès au besoin, tracer avant/après, vérifier la prise en compte et surveiller l’évolution. Pour l’installation réelle, faire confirmer le chemin autorisé d’accès distant, les droits, l’authentification et les moyens de reprise ; ne pas exposer directement le serveur pédagogique pour créer cet accès.

## 3 — Mise en commun : synthèse proposée

| Action courante en IT | Particularité OT à prendre en compte |
| --- | --- |
| Redémarrer un serveur pour rétablir un service | Il peut héberger la commande ou les alarmes ; vérifier le périmètre et les dépendances. |
| Installer une mise à jour disponible | Qualifier la compatibilité avec le procédé, tester et préparer l’interruption comme la reprise. |
| Modifier un paramètre à distance | La donnée écrite peut changer une commande et provoquer une conséquence physique progressive. |
| Conclure « tout va bien » parce que l’interface répond | Une page accessible ne prouve ni la validité des mesures ni le fonctionnement physique attendu. |
| Réinitialiser un défaut ou forcer une commande | L’action peut masquer une cause ou contourner une protection ; décision à faire valider selon le procédé. |

**Proposition pour l’oral :** « Je sépare la visibilité, la validité de la mesure, la décision de commande et l’effet physique. Avant une action, je vérifie les dépendances et l’état réel du procédé avec l’exploitation. Le défaut capteur de notre laboratoire arrête le compresseur sans afficher ce défaut dans la supervision : une interface accessible et une température affichée ne suffisent donc pas pour décider. »

La comparaison effective avec les autres binômes et les corrections du formateur restent à consigner.

## Traces à conserver

- État avant injection : consigne, porte, température, défaut et compresseur.
- Commande d’injection et lecture `sensor_fault=1`, puis observations espacées et horodatées.
- Capture conjointe CLI/supervision pour montrer ce que chaque interface expose.
- Commande de suppression et vérification de la reprise, avec température et mode automatique.
- Analyse A–E annotée après mise en commun, en séparant documentation, observation et information à confirmer.

[Retour à l’itération](index.md) · [Atelier précédent — Prendre en main le modèle](prendre-en-main-modele-frigorifique.md)
