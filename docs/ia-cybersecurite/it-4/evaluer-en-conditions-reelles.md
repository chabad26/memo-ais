# Évaluer en conditions réelles

**Séquence 4.3 — 1 h — Autonomie**

## Le concept

Au J3, le test provenait de la même période que l'entraînement. Ici, **septembre sert à apprendre et octobre sert à évaluer** : les étiquettes d'octobre ne doivent jamais participer à l'ajustement. Ce protocole temporel rapproche l'expérience du fonctionnement d'un détecteur appliqué à des données futures.

Cette fiche reprend **uniquement la section 4.3 du PDF** `Kit_apprenant_IA-01_Iteration_4.pdf`, consulté le **22 octobre 2026**. Le rapport demandé en **4.4** n'est pas préparé ici. Les résultats retenus sont ceux du dernier protocole corrigé et reproduit, pas les essais précédents à 263 ou 259 alertes.

## Mission 1 — Le script V2

### Fichiers et attribution

Dans **`livrables/ia-cybersecurite/it-4/IA_J4_ressources_apprenant/ia01-j4/`** :

- **`detection_ssh_v2.py`** : évolution commentée du script J3, rédigée avec assistance ; commentaires à relire, comprendre et reformuler personnellement si nécessaire.
- **`requirements.txt`** : dépendances du kit conservées.
- **`alertes_octobre.csv`** : **239 observations signalées**, réellement exportées par la V2 ; pas d'étiquette de référence dans la file analyste.
- **`preuves/execution_v2.txt`** : sortie du test de l'assistant.
- **`preuves/verification_v2.json`** : versions, résultats des contrôles et empreintes des sources/script/sortie.

Le script J3 et les CSV sources restent intacts. Aucune action sur le SI, aucun bannissement, aucun chargement du modèle `.joblib` et aucun cron n'ont été ajoutés.

### Exigences du PDF et réalisation

| Exigence | Réalisation dans la V2 |
| --- | --- |
| Apprendre seulement sur septembre | Arbre ajusté sur les mêmes 70 % stratifiés de septembre qu'au J3 ; Isolation Forest sur tout septembre préparé, sans étiquettes |
| Préparer octobre avec la nouvelle sonde | Compléter Mo par Ko/1024 selon la convention du kit, puis retirer seulement les volumes réellement absents |
| Garder caractéristiques, hyperparamètres et graine du J3 | Même ordre des sept variables, profondeur **3**, contamination **0,03**, graine **42** |
| Mesurer arbre, Isolation Forest et union sur octobre | Évaluation après prédiction, uniquement si les références d'octobre sont présentes ; fail2ban comparé sur les mêmes lignes |
| Exporter les plus atypiques et identifier les modèles | Tri croissant du score d'anomalie, départage date/heure/IP ; colonnes `avis_arbre`, `anomalie` et **`modeles_declencheurs`** |
| Arrêter sur préparation incompatible | Contrat de colonnes, types, origine, heures, valeurs négatives/infinies, double mesure Mo/Ko et couverture ; périodes successives contrôlées |
| Commenter les blocs modifiés | Commentaires sur conversion, entraînement temporel, exclusions, prédiction et export, explicitement proposés avec assistance |

Le seuil d'arrêt sur les manques est **10 % par défaut**, configurable par `--taux-manquants-max`. C'est une **valeur pédagogique provisoire à arbitrer avec Nadia**, pas une tolérance approuvée pour l'exploitation. Le contrôle ne prétend pas détecter toutes les dérives ou erreurs de sens : une constante numérique plausible peut encore passer. Les exclusions sont affichées et ne doivent pas disparaître du suivi de collecte.

### Lancer dans la VM

Copier le script V2 dans `~/ia01-j4`, puis :

```bash
source ~/ia01-j3/.venv/bin/activate
cd ~/ia01-j4
python detection_ssh_v2.py
```

Les chemins par défaut sont relatifs au script. Une option permet de conserver des essais séparés :

```bash
python detection_ssh_v2.py --sortie alertes_octobre_essai.csv
```

**Exécution dans la VM documentée le 22 octobre 2026.** Les captures montrent le lancement depuis `~/ia01-j4`, environnement activé, sous le nom `detection_sshv2.py`. Le fichier fourni dans le dépôt s'appelle `detection_ssh_v2.py` : adapter la commande au nom effectivement copié. Les résultats affichés concordent avec le notebook et les tests locaux de l'assistant.

### Captures de l'exécution

![Lancement du script V2 dans la VM et résultats de l'arbre](../../assets/img/ia-cybersecurite/it-4/Capture%20d’écran%20du%202026-10-22%2009-37-35.png)

*Première capture : paramètres 42 / 3 / 0,03, volumes manquants (90 en septembre, 14 en octobre), règles de l'arbre et évaluation temporelle : 26 faux positifs et 17 faux négatifs en octobre.*

![Résultats des détecteurs et export des alertes dans la VM](../../assets/img/ia-cybersecurite/it-4/Capture%20d’écran%20du%202026-10-22%2009-37-46.png)

*Seconde capture : union des détecteurs, 37 faux positifs, 9 faux négatifs et 202 attaques détectées ; export annoncé de 239 alertes, réparties en 104 puis 135 par semaine. Le dépassement du budget de 30 alertes hebdomadaires et les lignes hors couverture sont explicitement affichés.*

Ces captures attestent les sorties du script dans la VM. Elles ne démontrent ni deux relances identiques dans cette VM, ni l'identité des fichiers par empreinte avec ceux du dépôt ; les contrôles de reproductibilité ci-dessous restent attribués à l'environnement distinct de l'assistant.

### Préparation et protocole figés

| Étape | Effectifs et décision |
| --- | --- |
| Septembre brut | **1 704 observations, 117 attaques**, du 14 au 27 septembre |
| Septembre préparé | **1 614, dont 108 attaques** ; 90 volumes manquants exclus, dont 9 attaques |
| Apprentissage de l'arbre | **1 129 lignes** ; contrôle sur **485** lignes de septembre ; mêmes règles que le J3 à graine 42 |
| Octobre brut | **2 119 observations, 215 attaques**, du 28 septembre au 11 octobre |
| Octobre préparé et évalué | **2 105, dont 211 attaques** ; 14 vrais manques exclus après conversion, dont 4 attaques |
| Prédiction | Aucun `fit` ni réglage des modèles sur octobre ; étiquettes utilisées seulement après prédiction pour compter les erreurs |

Les **14 observations exclues d'octobre**, dont quatre attaques, sont hors couverture des métriques : elles ne deviennent ni normales ni détectées. La stratégie de suppression est conservée du J3 ; ce n'est pas l'imputation par médiane du corrigé générique.

## Résultats validés pour cet essai

| Détection sur les mêmes 2 105 lignes d'octobre | VN | FP | FN | VP | Précision attaque | Rappel attaque |
| --- | --- | --- | --- | --- | --- | --- |
| **Arbre** | 1 868 | **26** | **17** | **194** | **88,18 %** | **91,94 %** |
| **Isolation Forest** | 1 883 | **11** | **175** | **36** | **76,60 %** | **17,06 %** |
| **Union — alerte finale** | 1 857 | **37** | **9** | **202** | **84,52 %** | **95,73 %** |
| **fail2ban historique** | 1 894 | **0** | **150** | **61** | **100 %** | **28,91 %** |

L'union ajoute **8 attaques repérées** par rapport à l'arbre, mais aussi **11 faux positifs**. Les étiquettes sont les références fictives de Hugo : les métriques ne prouvent pas une performance sur le SI réel ou en novembre.

![Matrice finale octobre : 1857 VN, 37 FP, 9 FN, 202 VP](../../assets/img/ia-cybersecurite/it-4/Capture%20d’écran%20du%202026-10-22%2009-23-59.png)

**Capture fournie par l'apprenant, 09:23:59 :** matrice cohérente avec les résultats transmis et reproduits par la V2. Les lignes sont les références, les colonnes les prédictions. Les essais à mauvais volumes ou à ordre de caractéristiques différent ne sont pas mélangés à cette version.

## Mission 2 — Lire les erreurs

### Faux positifs : 37 observations sur trois sources

| Adresse/groupe | Nombre | Qui est-ce ? | Pourquoi le modèle s'inquiète | Faut-il l'ignorer ? |
| --- | --- | --- | --- | --- |
| **10.20.1.7** | **26** | Nouveau proxy Zabbix, journal DSI du 30/09 à 10 h | **Arbre seul** : quatre comptes distincts, origine interne, heure ≤19 ; profil appris comme attaque. Les lignes font aussi apparaître essais et succès | **Non globalement**. Vérifier le fonctionnement attendu et l'écart entre deux comptes annoncés au journal et quatre dans les agrégats ; contextualiser ou revoir l'apprentissage après validation |
| **10.20.8.30** | **10** | Profil de sauvegarde nocturne légitime du kit | **Isolation Forest seul** : gros volumes atypiques par rapport à septembre | Ne pas supprimer toutes les alertes de cette IP. Vérifier tâche, destination, fenêtre et évolution des volumes ; surveiller les écarts à ce contexte |
| **10.20.1.250** | **1** | Scanner autorisé ; scan prévu le 06/10 à 21 h | **Isolation Forest seul** ; ligne du 06/10 à22 h, 91 échecs et39 comptes | Rapprocher du scan autorisé et de sa durée réelle, sans présumer que toute activité à22 h est couverte par le seul horaire de début du journal |

Le proxy Zabbix est un cas de **nouvel usage légitime insuffisamment représenté**. Le scanner et la sauvegarde sont de vraies anomalies possibles mais de fausses alertes d'attaque selon les références. Une liste blanche générale masquerait une éventuelle compromission de ces machines.

### Faux négatifs : neuf attaques non signalées

| Profil observé | Nombre | Pourquoi le modèle ne le voit pas | Ce qui pourrait le révéler |
| --- | --- | --- | --- |
| **Accès VPN internes, un compte et un succès, transferts de 6 629 à7 617 Mo** : .112, .149, .184, .133 | **4** | Arbre : au plus3 comptes et durée entre0,5 et64 min → normal. Scores Isolation Forest positifs, très proches du seuil pour certaines lignes | Contexte VPN, destination et autorisation, historique du compte, volumes par rôle et séquences. Évaluer un contrôle complémentaire sans ajuster un seuil pour simplement effacer les erreurs d'octobre |
| **Activité interne sur trois comptes**, sources 10.20.3.50/.118/.57 | **3** | Même branche de durée ordinaire ; essais de faible volume, avec zéro ou un succès. Isolation Forest ne les juge pas assez atypiques | Corrélation sur plusieurs heures/hôtes, comptes concernés, posture du poste et liens entre échecs/succès ; type exact d'attaque à investiguer |
| **Connexions externes réussies sur un compte**, 198.51.100.67 et .131 | **2** | Durées26/48 min ordinaires ; volumes70,78 et653,23 Mo ; scores positifs dont un proche de zéro | Identité, nouvelle source, horaire habituel, destination des données et contexte métier ; pas de preuve de légitimité tirée du seul succès |

Ces neuf lignes sont étiquetées attaque ; le scénario complet de chacune n'est pas fourni. Leur somme ne comprend pas les quatre attaques retirées faute de mesure. L'identité « interne » et la réussite d'authentification ne suffisent pas à établir une activité sûre.

## Réponses aux quatre questions

### 1. Qu'est-ce qui a baissé depuis la fiche J3 ?

| Mesure | J3 à42 | Octobre, modèle figé | Lecture |
| --- | --- | --- | --- |
| **Arbre — précision** | 100 % sur test septembre | **88,18 %** | Baisse liée aux26 alertes normales du nouveau proxy |
| **Arbre — rappel** | 87,5 % sur32 attaques test | **91,94 %** sur211 attaques | Ne baisse pas dans cet essai ; effectifs et types de cas différents, pas preuve d'amélioration universelle |
| **IF — précision** | 89,80 % sur septembre d'ajustement | **76,60 %** | Plus de bruit relatif ; sauvegardes/scanner toujours à contextualiser |
| **IF — rappel** | 40,74 % sur septembre d'ajustement | **17,06 %** | Baisse descriptive ; ne pas oublier que la mesure J3 n'était pas sur de nouvelles données |
| **Union — précision / rappel** | 95,50 % /98,15 % sur jeu connu | **84,52 % /95,73 %** | Baisse descriptive ; la référence J3 inclut des données d'entraînement de l'arbre et ne donne pas une comparaison indépendante à périmètre égal |

Ne pas écrire que « tout a baissé » : le rappel de l'arbre est plus haut sur ce jeu. L'infrastructure et la population d'attaques changent ; la qualité doit être jugée avec **les erreurs, la couverture et la charge**, pas un seul pourcentage.

### 2. Combien seront lues avec une capacité de30 ?

| Semaine | Alertes produites | Capacité | Excédent si aucun renfort ni regroupement |
| --- | --- | --- | --- |
| **28/09–04/10, semaine40** | **104** | 30 | **74** |
| **05/10–11/10, semaine41** | **135** | 30 | **105** |
| **Total** | **239** | **60** | **179** |

Sans règle de priorité et retour réel de l'astreinte, on ne sait pas **quelles** lignes seront lues. La V2 trie les scores les plus bas en premier, mais un score d'anomalie n'est pas une gravité métier. Aucun plafond de30 n'a été ajouté et aucune des179 alertes excédentaires n'est considérée normale. Elles seraient non traitées dans cette fenêtre ou en attente, pas nécessairement « jamais lues » sans information sur les moyens et la gestion du retard.

Définir avec Nadia priorités, regroupement, escalade SOC et suivi du stock. Ne pas augmenter/réduire les hyperparamètres jusqu'à « réussir octobre » ; conserver cet essai et discuter les choix dans le rapport futur.

### 3. fail2ban apporte-t-il moins que le modèle ?

Son rappel vaut **61/211 =28,91 %**, avec zéro FP dans ces données. L’union détecte202 attaques, soit **141 de plus en compte brut**. Le rapprochement des lignes montre **60 détections communes**, **142 attaques trouvées par l’union sans fail2ban**, et **une attaque trouvée par fail2ban mais manquée par les modèles** : `10.20.3.118`, le05/10 à10 h. Le meilleur total ne signifie donc pas que le modèle remplace toutes les détections de la règle. Les contrôles ne sont pourtant pas interchangeables : bannissement par règle sur une fenêtre courte d'un côté, analyse horaire et qualification humaine de l'autre. Le modèle apporte une couverture complémentaire, au prix de37 faux positifs et d'une file surchargée.

### 4. L'exfiltration du9 octobre est-elle détectée ?

**Oui après conversion**, sur la ligne **index1813**, le **09/10 à3 h**, source **10.20.250.151** (plage VPN des autres salariés selon le journal). La nouvelle sonde donne **8 898 637 Ko**, soit **8 690,075195 Mo** avec la convention1024 du kit : ordre de grandeur du récit « 8,5 Go ».

| Avis et trace | Résultat V2 vérifié |
| --- | --- |
| Arbre | **0 — normal** : un compte, durée50 min, branche de durée ordinaire ; volume non utilisé dans cette branche |
| Isolation Forest | **Anomalie True**, score **−0,010177** environ |
| Modèle déclencheur exporté | **`isolation_forest`** |
| fail2ban du CSV | **0**, un échec seulement |

L'adaptation est la **récupération des Ko convertis en Mo**, au lieu de supprimer/remplacer à tort la mesure absente de l'ancienne colonne. Le modèle reçoit enfin le volume réel et Isolation Forest le signale. Cela ne signifie pas que tous les transferts VPN volumineux sont détectés : quatre autres lignes de ce profil restent parmi les FN.

## Vérifications du script et limites de preuve

La V2 a été exécutée par l'assistant dans un **venv séparé de la VM**, Python3.14.4, pandas3.0.6, Scikit-learn1.9.1, NumPy2.5.4. Les mêmes comptes que les dernières sorties de l'apprenant sont retrouvés. Contrôles réalisés :

1. **Deux exécutions : CSV identiques octet par octet.**
2. **Retrait des étiquettes d'octobre : mêmes prédictions et même export**, sans calcul des métriques ; les étiquettes de septembre restent nécessaires à l'entraînement de l'arbre.
3. **Schéma octobre inconnu : arrêt sans export.**
4. **Seuil de manques fixé à zéro pour l'essai : arrêt sans export**, puisque la mesure comporte de vrais trous.

Les fichiers de preuve sont conservés dans le sous-dossier `preuves/`. Aucun hyperparamètre n'a été ajusté pour améliorer les résultats d'octobre. Le notebook ayant déjà permis d'observer octobre, l'analyse reste exploratoire et ne garantit pas une performance sur novembre. La V2 **réentraîne à chaque lancement sur septembre** : elle reproduit le protocole demandé mais ne gère pas encore un artefact de modèle validé, persistant et gouverné.

Les agrégats SSH ne révèlent pas le contenu envoyé à un chatbot. Les pannes de mesure, les attaques proches du normal, les rôles machines et la dérive restent à traiter. L'exécution de la V2 dans la VM est désormais illustrée par deux captures ; la récupération des notebooks complets reste à documenter.

## Carnet et sources

Les missions, les tableaux et les réponses sont ajoutés à **`carnet_J4.md`**. **`rapport_evaluation.md` n'est pas rédigé ici** : il relève de la4.4.

Source pédagogique : PDF local `Kit_apprenant_IA-01_Iteration_4.pdf`, section4.3, lu le22 octobre2026. Résultats : sorties de l'apprenant, capture de matrice et reproduction indépendante de la V2 sur les CSV fictifs. Les scénarios non prouvés restent des hypothèses.

- [Relancer et réparer — 4.2](relancer-et-reparer.md)
- [J3 — Script et fiche du modèle](../it-3/le-script-de-detection.md)
- [Retour à l'itération 4](index.md)
