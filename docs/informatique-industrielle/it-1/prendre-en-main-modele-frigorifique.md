# 1.3 — Atelier 3 | Prendre en main le modèle de l’installation frigorifique

## Objectif et environnement

**Faire fonctionner un modèle logiciel d’installation industrielle et observer les interactions entre le processus, le contrôle et la supervision.** TP guidé sur machine Linux, avec le modèle de référence Python/Modbus fourni.

Le laboratoire est présent et déjà décompressé dans :

```text
livrables/informatique-industrielle/it-1/ot-refrigeration-poc/
├── README.md
├── lab/
├── docs/
├── tests/
└── optional/
```

Le contrôleur est **simulé en Python**. Aucun programme OpenPLC n’est exécuté dans cet atelier. Le modèle représente une installation fictive : il n’est pas synchronisé avec un réfrigérateur réel.

## 1 — Préparer l’environnement

Depuis la racine du dépôt du mémo :

```bash
cd livrables/informatique-industrielle/it-1/ot-refrigeration-poc
python3 --version
ls
```

Utiliser **Python 3.10 ou supérieur**. Le cœur du laboratoire utilise la bibliothèque standard : aucun paquet `pip` n’est requis. Ouvrir les trois terminaux suivants **dans ce même répertoire**, celui qui contient `lab/`, `docs/` et `tests/`, afin que `python3 -m lab.…` trouve les modules.

Lire en priorité :

```bash
less README.md
less docs/REGISTER_MAP.md
less lab/model.py
```

| Fichier | Ce qu’il permet d’identifier |
| --- | --- |
| `README.md` | Lancement, composants, périmètre et limites du laboratoire. |
| `docs/REGISTER_MAP.md` | Adresses Modbus, unités, valeurs et droits de lecture/écriture. |
| `lab/model.py` | État initial, évolution thermique, hystérésis et calcul de l’alarme. |
| `lab/server.py` et `lab/modbus.py` | Exposition Modbus TCP et boucle de simulation. |
| `lab/dashboard.py` | Supervision HTTP en lecture seule, qui interroge le serveur Modbus. |
| `lab/client.py` | Consultation et modification des paramètres depuis le terminal. |

Le README propose aussi une passerelle et des exercices supplémentaires. **Ils ne sont pas nécessaires à l’atelier 1.3** : seules les manipulations ci-dessous sont reprises ici.

## 2 — Démarrer l’installation simulée

### Terminal 1 — Processus, contrôle et serveur Modbus

```bash
python3 -m lab.server
```

Adresse par défaut : **`127.0.0.1:15020`**, sur l’interface de bouclage uniquement. Ce processus héberge le modèle thermique, le contrôleur et le serveur Modbus ; ce ne sont pas trois machines distinctes.

### Terminal 2 — Supervision

```bash
python3 -m lab.dashboard
```

Ouvrir sur **la même machine Linux** :

```text
http://127.0.0.1:18080
```

Si le laboratoire fonctionne dans une VM, `127.0.0.1` désigne cette VM : ouvrir le navigateur dans la VM pour suivre ces commandes telles quelles.

La page montre température, consigne, compresseur, porte et alarme. Elle est en **lecture seule** et son JavaScript actualise les données chaque seconde. Le service HTTP lit les valeurs par Modbus, sans accéder directement à l’objet Python du processus.

### Terminal 3 — Poste de maintenance simulé

```bash
python3 -m lab.client status
```

Répéter après quelques secondes. Le client interroge directement le serveur Modbus sur le port `15020`.

Pour vérifier les écoutes locales :

```bash
ss -ltn '( sport = :15020 or sport = :18080 )'
```

Les adresses attendues sont `127.0.0.1:15020` et `127.0.0.1:18080`. Conserver les valeurs par défaut : le serveur pédagogique permet volontairement des écritures directes sans authentification.

### Correspondance des composants

| Fonction industrielle | Élément du laboratoire |
| --- | --- |
| Enceinte et échanges thermiques | Calcul dans `Plant.advance()` de `lab/model.py`. |
| Capteur | Température simulée publiée dans les registres. |
| Contrôleur | Logique Python de la même méthode `advance()`. |
| Actionneur | État booléen `compressor` et terme de refroidissement. |
| Supervision | `lab.dashboard` et navigateur. |
| Maintenance | `lab.client`, avec commandes de lecture et d’écriture. |

## 3 — Observer le fonctionnement normal

### État initial confirmé dans le code

| Variable | Valeur au moment de la création du modèle |
| --- | --- |
| Température | **5 °C** |
| Température ambiante | **22 °C** |
| Consigne | **4 °C** |
| Compresseur | Arrêté avant le premier pas de calcul. |
| Porte | Fermée. |
| Mode automatique | Actif. |
| Défaut capteur / alarme | Inactifs. |

La boucle appelle normalement le modèle toutes les **0,1 seconde** avec un pas `dt = 0.1`. Au premier pas, la température initiale de 5 °C dépasse le seuil de démarrage de 4,5 °C : le compresseur démarre. Une première consultation réseau peut donc déjà afficher le compresseur en marche et une température inférieure à la valeur initiale.

La température diminue jusqu’au seuil bas de **3,5 °C**, où le compresseur s’arrête. L’ambiance réchauffe ensuite l’enceinte jusqu’au seuil haut de **4,5 °C**, où il redémarre. Entre les seuils, son état précédent est conservé.

### Relevés attestés par les captures de la session

Les heures ci-dessous proviennent des **noms des fichiers de capture**, pas d’un horodatage interne des mesures. Une capture CLI/navigateur peut réunir des lectures successives.

| Capture du 26 octobre 2026 | Température CLI | Température navigateur | Consigne | Compresseur | Porte | Alarme |
| --- | --- | --- | --- | --- | --- | --- |
| 11:13:12 | Non visible | 3,8 °C | 4 °C | Marche | Fermée | Aucune |
| 11:16:09 | 4,1 °C | Non visible | 4 °C | Arrêt | Fermée | Aucune |
| 11:16:35 | 4,1 → 4,3 → 4,3 → 4,4 °C | Non visible | 4 °C | Arrêt sur les quatre lectures | Fermée | Aucune |
| 11:17:47 | 3,8 °C sur les deux lectures | 3,8 °C | 6 °C | Arrêt | Fermée | Aucune |
| 11:18:00 | 4,0 °C | 4,1 °C | 4 °C | Arrêt | Fermée | Aucune |
| 11:18:13 | 4,3 °C | 4,3 °C | 4 °C | Arrêt | Ouverte | Aucune |
| 11:18:27 | 4,4 °C | 4,4 °C | 4 °C | Marche | Fermée | Aucune |
| 11:19:19 | 3,6 °C | 3,6 °C | 4 °C | Arrêt | Fermée | Aucune |

La température initiale à la création du modèle (5 °C) n’est pas capturée. Les états marche et arrêt sont attestés, mais **les instants exacts des bascules à 3,5 et 4,5 °C ne sont pas visibles**. À 4,4 °C avec le compresseur en marche, l’état observé est compatible avec un refroidissement après franchissement du seuil haut ; le franchissement lui-même n’est pas photographié.

La température Modbus est arrondie au **dixième de degré**, tandis que le modèle conserve une valeur plus précise. Une valeur affichée de 3,5 ou 4,5 °C ne suffit donc pas à prouver que le seuil exact est franchi. CLI et navigateur interrogent le même serveur, mais à des instants différents : de petits écarts sont possibles pendant l’évolution.

## 4 — Modifier la consigne

Dans le troisième terminal :

```bash
python3 -m lab.client status
python3 -m lab.client setpoint 6
python3 -m lab.client status
```

Observer le navigateur, puis renouveler les consultations pendant l’évolution.

| Question | Réponse fondée sur le modèle |
| --- | --- |
| **1. La température change-t-elle immédiatement ?** | L’écriture modifie la consigne, sans remplacer la température par 6 °C. La température évolue ensuite progressivement avec les pas de simulation. |
| **2. La commande du compresseur change-t-elle ?** | Elle est réévaluée au prochain pas de contrôle, selon la température et l’état précédent. Avec la nouvelle consigne, arrêt à **5,5 °C ou moins**, marche à **6,5 °C ou plus**. En fonctionnement normal autour de 4 °C, un compresseur en marche s’arrêtera ; s’il était déjà arrêté, il restera arrêté. |
| **3. Combien de temps faut-il pour observer un effet physique ?** | Le modèle calcule une évolution dès le pas suivant, normalement 0,1 s. Un changement visible au dixième de degré prend davantage de temps et dépend de la situation. Le navigateur se rafraîchit chaque seconde. Chronométrer le résultat du TP ; il n’existe pas un délai universel de passage à 6 °C. |
| **4. Paramètre de contrôle ou évolution physique ?** | La consigne est une donnée de commande écrite par le client. La température est un état du procédé : elle dépend des échanges thermiques, de la porte, du compresseur et du temps écoulé. |

Restaurer ensuite la valeur initiale :

```bash
python3 -m lab.client setpoint 4
python3 -m lab.client status
```

Le retour à une consigne de 4 °C ne remet pas instantanément l’enceinte à 4 °C.

## 5 — Simuler l’ouverture de la porte

```bash
python3 -m lab.client door 1
python3 -m lab.client status
```

Observer la pente de température et l’état du compresseur, puis fermer :

```bash
python3 -m lab.client door 0
python3 -m lab.client status
```

Dans `lab/model.py`, le modèle applique :

```text
apport thermique = 0,0007 × (ambiante − température) × facteur porte
facteur porte = 2 si ouverte, 1 si fermée
refroidissement = 0,040 si compresseur en marche, 0 sinon
température suivante = température + (apport thermique − refroidissement) × dt
```

**L’ouverture double l’apport thermique dans ce modèle**, sans doubler nécessairement la variation nette de température. Lorsque le compresseur tourne, l’enceinte peut encore refroidir, mais plus lentement. Comparer si possible à température et état du compresseur identiques.

L’ouverture est une **perturbation physique simulée** : elle modifie les échanges thermiques, puis la mesure utilisée par le contrôleur. Celui-ci applique toujours la même règle, sans modification de sa consigne ni de son programme. Dans le laboratoire, la commande informatique `door 1` sert à injecter cet événement physique ; elle ne représente pas un changement du réglage du thermostat.

## Captures de la session utilisateur — preuves et interprétation

Les dix originaux sont conservés dans `docs/assets/img/informatique-industrielle/it-1/`. Les relevés ci-dessus proviennent de leur lecture ; ils sont distincts des calculs directs du modèle et des tests locaux de rédaction présentés plus bas.

### 11:13:12 — Supervision en fonctionnement

![Supervision en fonctionnement](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2011-13-12.png)

La page affiche **3,8 °C**, consigne **4 °C**, compresseur **ON**, porte **CLOSED**, sans alarme. Le compresseur peut rester en marche dans la bande d’hystérésis. Cette capture ne montre ni la commande de lancement ni le premier état du modèle.

### 11:16:09 — Première lecture CLI capturée

![Première lecture CLI capturée](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2011-16-09.png)

La commande `python3 -m lab.client status` renvoie **4,1 °C**, `setpoint=4.0`, `compressor=0`, `alarm=0`, `door=0`, `sensor_fault=0`, `auto=1`. Le client accède au serveur et lit son état.

### 11:16:35 — Lectures successives en fonctionnement normal

![Lectures successives en fonctionnement normal](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2011-16-35.png)

Les quatre consultations montrent **4,1 ; 4,3 ; 4,3 ; 4,4 °C**, avec compresseur arrêté, consigne à 4 °C, porte fermée et aucune alarme. Elles attestent une remontée de température entre les lectures extrêmes, sans donner leurs intervalles exacts.

### 11:16:59 — Vérification des interfaces d’écoute

![Vérification des interfaces d’écoute](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2011-16-59.png)

La sortie de `ss -ltn` affiche **`127.0.0.1:18080`** et **`127.0.0.1:15020`** en `LISTEN`. Les deux écoutes sélectionnées sont sur le bouclage local. Le `0.0.0.0:*` de la colonne distante ne signifie pas une écoute locale sur toutes les interfaces.

### 11:17:47 — Consigne portée à 6 °C

![Consigne portée à 6 °C](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2011-17-47.png)

La commande `setpoint 6` est visible avec une réponse **`write accepted`** ; les deux lectures CLI affichent une consigne de **6 °C**, comme le navigateur. La température reste affichée à **3,8 °C** et le compresseur est arrêté. La capture confirme que température et consigne sont distinctes ; elle ne montre pas un passage du compresseur de marche à arrêt ni le temps nécessaire pour atteindre la nouvelle zone de régulation.

### 11:18:00 — Restauration de la consigne à 4 °C

![Restauration de la consigne à 4 °C](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2011-18-00.png)

La commande `setpoint 4` est acceptée. Le client lit **4,0 °C**, le navigateur **4,1 °C**, tous deux avec une consigne de **4 °C**, compresseur arrêté, porte fermée et aucune alarme. Ce dixième d’écart est compatible avec des lectures décalées pendant le réchauffement ; ce n’est pas une preuve de désynchronisation anormale.

### 11:18:13 — Ouverture de la porte virtuelle

![Ouverture de la porte virtuelle](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2011-18-13.png)

La commande `door 1` est acceptée. Le client affiche `door=1` et le navigateur **OPEN**. Les deux montrent **4,3 °C**, consigne **4 °C**, compresseur arrêté et aucune alarme. L’injection de l’ouverture est attestée ; cette seule capture ne mesure pas le doublement de l’apport thermique.

### 11:18:27 — Fermeture de la porte virtuelle

![Fermeture de la porte virtuelle](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2011-18-27.png)

La commande `door 0` est acceptée ; le client affiche `door=0` et le navigateur **CLOSED**. Les deux montrent **4,4 °C**, compresseur en marche et aucune alarme. La température, plus élevée que sur la capture précédente, n’indique pas à elle seule une anomalie : la trajectoire entre les deux captures n’est pas enregistrée.

### 11:18:54 — Tests exécutés dans la session utilisateur

![Tests exécutés dans la session utilisateur](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2011-18-54.png)

La commande `python3 -m unittest discover -s tests -v` affiche les **12 tests `ok`**, puis **`Ran 12 tests in 1.747s`** et **`OK`**. C’est une preuve d’exécution utilisateur de la suite fournie, distincte de son exécution locale pendant la préparation de la fiche. Elle ne constitue pas une certification du modèle pour un usage industriel.

### 11:19:19 — État final restauré

![État final restauré](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-26%2011-19-19.png)

Les commandes `setpoint 4` et `door 0` sont visibles avec deux réponses **`write accepted`**. CLI et navigateur indiquent **3,6 °C**, consigne **4 °C**, compresseur arrêté, porte fermée et aucune alarme. Le client indique aussi `sensor_fault=0` et `auto=1`. La remise des paramètres est attestée ; l’arrêt des services par Ctrl + C n’est pas montré.

### Bilan de preuve

**Établi par les captures :** supervision et client opérationnels, écoutes locales des deux services, lectures successives de température, écriture de consigne à 6 °C puis restauration à 4 °C, ouverture/fermeture virtuelle de porte, cohérence des états CLI/navigateur aux instants capturés, 12 tests réussis et paramètres finaux restaurés.

**Encore à documenter si demandé :** délai chronométré après modification de consigne, courbes comparables porte ouverte/fermée, instants exacts de bascule, déclenchement temporisé de l’alarme et arrêt des services. Aucune alarme haute n’est active sur les captures ; cela ne prouve pas son impossibilité de déclenchement.

## Vérifications locales réalisées le 26 octobre 2026

### Tests fournis

Commande exécutée depuis la racine du laboratoire :

```bash
python3 -m unittest discover -s tests -v
```

**Résultat : 12 tests réussis.** Ils couvrent le modèle, les échanges TCP/Modbus, le client, la supervision HTTP et la passerelle. Le test d’intégration lance des sous-processus sur des ports locaux disponibles, vérifie une écriture de consigne et sa lecture par l’API HTTP, puis arrête ses services. Il inclut une consigne de démonstration à 50 °C ; ce n’est pas une manipulation demandée dans cet atelier.

### Calculs directs du modèle

Vérification distincte du TP en navigateur : import de `Plant` et appels à `advance(0.1)`, sans attente du temps réel. Les durées ci-dessous sont du **temps simulé calculé**, pas des chronométrages utilisateur.

| Essai local | Résultat observé |
| --- | --- |
| État initial par défaut | Température 5 °C, consigne 4 °C, compresseur arrêté, porte fermée. |
| Évolution normale sur 300 s simulées | Marche à 0,1 s ; premier arrêt à 54,6 s ; redémarrage à 134,2 s ; nouvel arrêt à 170,8 s. Températures arrondies aux bascules : 3,5 / 4,5 °C. |
| Départ à 5 °C, compresseur en marche ; écriture de consigne à 6 °C | Immédiatement après l’écriture : température inchangée à 5 °C, compresseur encore en marche. Au pas suivant : compresseur arrêté. Après 30 s simulées : **5,35 °C**. |
| Départ à 4 °C, compresseur arrêté, porte fermée pendant 10 s simulées | **4,13 °C**, arrondi au centième. |
| Même départ, porte ouverte pendant 10 s simulées | **4,25 °C**, arrondi au centième. |

Ces contrôles confirment le comportement du modèle fourni. Ils complètent les captures de la session Linux sans prouver une évolution identique d’un équipement réel. Le README parle de temps de démonstration accéléré ; le serveur inspecté transmet un pas fixe de 0,1 s à chaque attente nominale de 0,1 s, sans multiplicateur explicite. Un ralentissement de la machine peut créer un écart entre temps calculé et temps mural.

## Informations désormais établies pour le schéma OT

- La régulation et le calcul d’alarme sont dans `lab/model.py`, hébergés par le serveur Python.
- L’alarme utilise la température après évolution ; son compteur revient à zéro lorsque la température n’est plus strictement supérieure à 8 °C. L’alarme n’est pas mémorisée indépendamment de cette condition et aucun acquittement n’est implémenté dans ce modèle.
- La supervision consulte par Modbus ; son arrêt seul n’arrête pas la boucle du serveur, si ce dernier reste actif.
- La maintenance écrit directement par Modbus : registre holding **0** pour la consigne en dixièmes de degré (6 °C → valeur **60**), coil **0** pour l’ouverture de porte.
- L’état initial du compresseur est arrêté, avant sa première évaluation.

Ces faits précisent les hypothèses du [schéma de l’atelier 1.2](etudier-installation-frigorifique.md). Aucun automate matériel, OpenPLC, protocole chiffré ou équipement réel n’est attesté par ce laboratoire.

## Éléments à conserver et fin du TP

Les relevés CLI et navigateur fournis avant/après changement de consigne et ouverture de porte sont intégrés ci-dessus. Compléter si nécessaire avec des relevés horodatés pour mesurer les délais et les pentes de température. Distinguer systématiquement **consigne écrite**, **commande du compresseur** et **température observée**.

Avant de terminer :

```bash
python3 -m lab.client setpoint 4
python3 -m lab.client door 0
python3 -m lab.client status
```

Arrêter la supervision puis le serveur avec **Ctrl + C** dans leurs terminaux respectifs. La vérification locale de la suite de tests s’est arrêtée automatiquement ; aucun service permanent n’a été installé pour rédiger cette fiche.

[Retour à l’itération](index.md) · [Atelier précédent — Installation frigorifique](etudier-installation-frigorifique.md)
