# 2.3 — Atelier 3 | Cartographier les variables et tester les opérations Modbus

**Itération 1 · Journée 2 · 1 h 15 · Travail en autonomie.**

## Objectif et organisation

**Associer les données Modbus aux éléments physiques de l’installation et vérifier les effets des opérations de lecture et d’écriture.** TP individuel ou en binôme, sans présence du formateur ; utiliser documentation et entraide du groupe.

La table et les réponses sont renseignées à partir du laboratoire. Un test local distinct est décrit plus bas. **Huit captures utilisateur** attestent désormais les lectures FC03/FC04 et les échanges FC05, avec fermeture de la coil 0 détaillée. La sortie Python atteste aussi l’exception 02 pour l’adresse invalide ; le détail d’ouverture à 0xFF00 reste à fournir ; les preuves FC06 de l’[atelier 2.2](analyser-echanges-modbus-wireshark.md) restent disponibles.

## 1 — Construire la table des variables

Références : `docs/REGISTER_MAP.md`, `Plant.read()`, `write_register()` et `write_coil()` dans `lab/model.py`. Les adresses sont les **adresses PDU à partir de zéro**, pas des libellés 40001/30001. Identifier une donnée par **table + adresse**.

| Variable | Type Modbus | Adresse PDU | Fonction de lecture | Fonction d’écriture | Unité ou valeur |
| --- | --- | --- | --- | --- | --- |
| **Consigne de température** | Holding register | **0** | **FC03** | **FC06** | Dixièmes de °C ; 40 = 4 °C. Valeurs acceptées 0 à 500, soit 0 à 50 °C. |
| **Température mesurée simulée** | Input register | **0** | **FC04** | **Non accessible en écriture** | Dixièmes de °C, arrondis pour la lecture. |
| **État du compresseur** | Input register ; aussi discrete input | **1** ; aussi **0** dans la seconde table | **FC04** ; aussi **FC02** | **Non accessible directement en écriture** | 1 = marche, 0 = arrêt ; commande simulée, pas retour mécanique indépendant. |
| **État de la porte** | Coil | **0** | **FC01** | **FC05** | 1 = ouverte, 0 = fermée. FC05 transporte 0xFF00 pour vrai et 0x0000 pour faux. |
| **Alarme de température** | Input register ; aussi discrete input | **2** ; aussi **1** dans la seconde table | **FC04** ; aussi **FC02** | **Non accessible directement en écriture** | 1 = active, 0 = inactive ; T > 8 °C pendant au moins 10 s calculées. |
| **Défaut du capteur** | Coil d’injection ; état aussi dans input register | **1** ; aussi **3** dans la seconde table | **FC01** ; aussi **FC04** | **FC05 sur coil 1 uniquement** | 1 = défaut injecté, 0 = pas de défaut injecté. L’input register 3 reste en lecture seule. |
| **Mode automatique** | Holding register | **2** | **FC03** | **FC06** | 1 = régulation automatique active ; 0 = suspendue. Ne garantit pas l’arrêt du compresseur. |

### Points d’interprétation

- La **limite conseillée** est un holding register supplémentaire d’adresse **1**, lu par FC03 : **80 → 8 °C**. Il est en lecture seule et n’impose pas cette borne aux écritures de consigne.
- Une même information peut être présentée dans deux tables : le compresseur est lisible par FC04 ou FC02. Cela ne décrit pas deux compresseurs différents.
- Une variable non modifiable directement peut varier par effet du contrôle : une consigne ou un défaut écrits peuvent modifier la commande du compresseur.
- La température publiée est celle du modèle, même quand le défaut capteur est injecté. L’interface web fournie ne signale pas ce défaut.
- La transmission des températures négatives n’est pas correctement couverte par l’encodage non signé fourni ; les essais documentés restent au-dessus de 0 °C.

## 2 — Tester les commandes de porte

Depuis le dossier du laboratoire, serveur actif sur `127.0.0.1:15020`, vérifier l’état :

```bash
python3 -m lab.client status
```

Si nécessaire, restaurer la consigne :

```bash
python3 -m lab.client setpoint 4
python3 -m lab.client status
```

Pour isoler l’effet de la porte, vérifier aussi `sensor_fault=0` et `auto=1` ; ne pas interpréter une réaction thermique sans connaître ces conditions et la version d’hystérésis utilisée.

### Ouverture puis fermeture

Démarrer une capture sur `lo` comme dans l’atelier 2.2, puis exécuter séparément :

```bash
python3 -m lab.client door 1
python3 -m lab.client status
```

Puis :

```bash
python3 -m lab.client door 0
python3 -m lab.client status
```

Résultats attendus : `write accepted`, puis `door=1` après ouverture et `door=0` après fermeture. Les valeurs thermiques ne sont pas fixes et doivent être relevées avec leur contexte. L’ouverture augmente l’apport thermique du modèle ; elle ne modifie pas sa consigne.

### Quelle différence avec la consigne ?

| Opération | Code / objet | Contenu écrit |
| --- | --- | --- |
| Porte ouverte | **FC05**, coil **0** | **0xFF00**, codage de vrai. Ce n’est pas la valeur brute 0x0001. |
| Porte fermée | **FC05**, coil **0** | **0x0000**, codage de faux. |
| Consigne 6 °C | **FC06**, holding register **0** | **60 / 0x003C**, valeur numérique en dixièmes de °C. |

`lab/client.py` réalise ces conversions avant d’appeler `Client.request()`. Dans les deux cas, la réponse normale d’écriture reprend la fonction, l’adresse et la valeur ; elle ne contient pas une mesure indépendante du résultat physique.

Dans Wireshark, après décodage du port serveur 15020 :

```text
tcp.port == 15020 && modbus.func_code == 5
```

Pour une lecture après l’écriture :

```text
tcp.port == 15020 && modbus.func_code == 1
```

Repérer requête et réponse par sens, ports et flux TCP. Pour FC01, la réponse regroupe les états sous forme de bits : utiliser le détail du décodeur, pas une lecture arbitraire de l’octet comme température.

## 3 — Tester une adresse invalide

Sans modifier les fichiers, depuis le dossier du laboratoire :

```bash
python3 - <<'PYCODE'
from lab.modbus import Client

client = Client("127.0.0.1", 15020)

try:
    print(client.request(3, 100, 1))
except Exception as exc:
    print(type(exc).__name__, exc)
PYCODE
```

Cette commande demande **FC03**, adresse holding **100**, quantité **1**. Le serveur fourni ne possède que les adresses holding **0, 1 et 2**.

Avec ce serveur actif, la sortie attendue est :

```text
ProtocolError Modbus exception code 2
```

### Interpréter l’exception

Le code **02 — Illegal Data Address** indique que l’adresse ou la combinaison adresse/quantité n’est pas permise pour le serveur. Une réponse d’exception reprend le code de fonction avec son bit de poids fort positionné : **0x03 + 0x80 = 0x83**, suivi du code **0x02**. [Spécification Modbus V1.1b3, §7, p. 47–48](https://www.modbus.org/file/secure/modbusprotocolspecification.pdf).

Pour ce laboratoire, la PDU de réponse attendue est donc :

```text
83 02
│  └─ Exception : Illegal Data Address
└──── Réponse d’exception à FC03
```

Le MBAP attendu garde transaction **1**, protocole **0**, unité **1** et une longueur de **3** (unité + deux octets de PDU). Ces valeurs sont déduites du code, sans être encore attestées dans une capture utilisateur de cet essai.

### Réponses aux quatre questions

1. **Le serveur répond-il ? Oui**, si l’on obtient cette exception : une réponse applicative Modbus a été reçue et interprétée par le client.
2. **La requête est-elle acceptée ? Non**, l’opération de lecture de l’adresse 100 est refusée. Le serveur a traité la demande pour la rejeter ; il n’a pas renvoyé la valeur d’un registre valide.
3. **Erreur de protocole ou absence de réponse ?** L’exception est une réponse structurée, avec un code expliquant le refus. Un timeout signifie qu’aucune réponse complète n’a été reçue avant la limite ; une connexion refusée indique un autre échec, au niveau de l’établissement TCP. Un message local `ProtocolError` peut aussi signaler une réponse mal formée : lire son contenu exact et, si possible, la capture.
4. **Pourquoi les distinguer ?** Pour orienter le diagnostic. Une exception 02 fait vérifier table, adresse et quantité ; une absence de réponse fait examiner notamment service, chemin réseau, filtrage et délais. Redémarrer sans avoir distingué ces cas peut interrompre inutilement un procédé et ne corrige pas une mauvaise adresse.

| Observation | Conclusion limitée | Première vérification |
| --- | --- | --- |
| Réponse Modbus d’exception 02 | Le serveur joint refuse cette adresse/quantité. | Mapping, base 0/1 et quantité. |
| Timeout | Pas de réponse complète dans le délai. | Capture, chemin, charge, service et temporisation ; ne pas conclure automatiquement « serveur arrêté ». |
| Connexion refusée | Connexion TCP non établie, rejet reçu. | Adresse, port, service en écoute et règles de rejet éventuelles. |
| Erreur de décodage Wireshark | L’affichage peut être mal configuré. | Association au port serveur ; le problème déjà observé en 2.2 ne prouvait pas une trame invalide. |

## Vérification locale réalisée le 27 octobre 2026

Un serveur temporaire a été démarré sur **un port libre de 127.0.0.1**, avec le code fourni et une nouvelle instance `Plant`. Le client a utilisé ce port, puis le serveur a été arrêté. Ce test est distinct de la session utilisateur sur 15020 et ne produit pas de capture Wireshark de l’apprenant.

| Test local | Résultat observé |
| --- | --- |
| Lecture FC01, coil 0 | `[0]` initialement. |
| Écriture FC05, coil 0, 0xFF00 puis relecture | Réponse validée `True`, lecture `[1]`. |
| Écriture FC05, coil 0, 0x0000 puis relecture | Réponse validée `True`, lecture `[0]`. |
| FC03, adresse 100, quantité 1 | **`ProtocolError Modbus exception code 2`**. |
| Appel direct du gestionnaire sur PDU `03 00 64 00 01` | PDU d’exception **`83 02`**. |

Ce contrôle confirme les opérations et le refus applicatif dans le laboratoire. Il ne démontre pas un dispositif d’autorisation ni un filtrage réseau.

## Captures utilisateur du 27 octobre — lectures et porte

Les heures des titres proviennent des noms des images. **Ces numéros de trames appartiennent à la capture de cette session** : ne pas les assimiler aux mêmes numéros dans la capture précédente de l’atelier 2.2. Aucun PCAP brut correspondant n’a été fourni ici.

### 09:46:11 — Lectures FC03 : deux paires requête/réponse

![Lectures FC03 : deux paires requête/réponse](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2009-46-11.png)

Le filtre **`tcp.port == 15020 && modbus.func_code == 3`** montre **14 Query / 16 Response**, puis **54 Query / 56 Response**, pour **Read Holding Registers**, transaction **1**, unité **1**. Les adresses source et destination sont **127.0.0.1**. Cette liste atteste les lectures et leurs réponses ; les valeurs renvoyées ne sont pas développées.

### 09:46:27 — Requête FC03 : adresse 0, quantité 3

![Requête FC03 : adresse 0, quantité 3](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2009-46-27.png)

Le détail montre **Read Holding Registers (3)**, **Reference Number 0**, **Word Count 3** et aucune exception sur le message affiché. Le MBAP contient transaction **1**, protocole **0**, longueur **6**, unité **1**. Selon le mapping, la demande vise **consigne, limite conseillée et mode automatique**. La capture ne donne pas le numéro du paquet sélectionné ni les valeurs d’une réponse.

### 09:46:46 — Octets de la lecture FC04

![Octets de la lecture FC04](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2009-46-46.png)

La zone hexadécimale montre le contenu applicatif **`00 01 00 00 00 06 01 04 00 00 00 04`** : MBAP **1 / 0 / 6 / 1**, fonction **04**, adresse **0000**, quantité **0004**. La sélection sur **`00 04`** correspond à la quantité de quatre registres, pas à une température de 4 °C. La capture suivante rend ces champs lisibles dans le décodeur.

### 09:46:51 — Requête FC04 : adresse 0, quantité 4

![Requête FC04 : adresse 0, quantité 4](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2009-46-51.png)

Wireshark affiche **Read Input Registers (4)**, **Reference Number 0**, **Word Count 4**, MBAP **1 / 0 / 6 / 1**. La demande vise température, commande du compresseur, alarme et défaut capteur selon la table du laboratoire. Les valeurs de réponse et le numéro de la trame ne sont pas visibles ; on ne peut donc pas leur attribuer des valeurs observées.

### 09:47:50 — Écritures de porte : deux paires FC05

![Écritures de porte : deux paires FC05](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2009-47-50.png)

Le filtre correct **`tcp.port == 15020 && modbus.func_code == 5`** affiche **4 Query / 6 Response**, puis **44 Query / 46 Response**, en **Write Single Coil**, transaction **1**, unité **1**. La liste atteste deux échanges FC05 ; elle ne montre pas, à elle seule, la valeur de chaque écriture. **FC05 concerne la porte ; FC06 concernait la consigne.**

### 09:48:16 — Fermeture : coil 0, valeur 0x0000

![Fermeture : coil 0, valeur 0x0000](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2009-48-16.png)

Le détail affiche **Write Single Coil (5)**, **Reference Number 0**, **Data 0000** ; les octets de PDU sont **`05 00 00 00 00`**. Ils confirment l’écriture de la coil 0 à faux, soit la **fermeture de la porte virtuelle** selon le mapping. Le MBAP reste **1 / 0 / 6 / 1**. Le numéro de la trame n’est pas affiché et son association à la paire 44/46 ne peut pas être affirmée à partir de cette seule image. L’écho détaillé de réponse n’est pas développé ici.

### 09:49:43 — Relecture FC01 : porte ouverte, défaut inactif

![Réponse FC01 avec bit 0 à 1 et bit 1 à 0](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2009-49-43.png)

La réponse **Read Coils (1)** est liée à **Request Frame 34**, avec un délai de **286 µs**. Elle contient **Byte Count 1**, **Bit 0 = 1** et **Bit 1 = 0**. Selon le mapping, la porte virtuelle est **ouverte** et le défaut capteur injecté **inactif**. Le MBAP indique transaction **1**, protocole **0**, longueur **4**, unité **1** ; le contenu applicatif se termine par **`01 01 01`** (fonction, nombre d’octets, octet de bits).

Cette capture prouve une lecture d’état, distincte de l’acceptation d’une écriture. Le numéro de la réponse n’est pas visible ; le délai concerne l’échange réseau, pas l’ouverture physique d’une porte réelle. La requête 34 de cette session ne doit pas être confondue avec la requête FC06 numéro 34 de l’atelier 2.2.

### 09:50:14 — Test Python d’une adresse inexistante

![Lecture Python FC03 à l’adresse 100 et exception Modbus code 2](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2009-50-14.png)

Dans la VM Debian, le script crée **`Client("127.0.0.1", 15020)`**, puis exécute **`client.request(3, 100, 1)`** : lecture FC03 d’un holding register à l’adresse PDU 100. La sortie est **`ProtocolError Modbus exception code 2`**.

Cette exécution utilisateur confirme que **le serveur répond par une exception 02 — Illegal Data Address**, et que la lecture demandée est refusée. Il ne s’agit pas d’un timeout ou d’une connexion refusée. Le script intercepte l’exception pour afficher son type et son message ; aucun fichier du laboratoire n’est modifié.

La PDU **`83 02`** est attendue d’après le code et le test local, mais cette capture de terminal ne montre pas les octets réseau ni les numéros de trames de l’échange. Une capture Wireshark correspondante constituerait une preuve complémentaire.

### Bilan des observations

| Observation attestée | Limite de preuve |
| --- | --- |
| Deux paires FC03 14/16 et 54/56 ; demande à partir de 0 pour 3 registres | Valeurs retournées et ports clients à relever dans les détails. |
| Demande FC04 à partir de 0 pour 4 registres | Réponse et valeurs non développées dans les images reçues. |
| Réponse FC01 liée à la requête 34 : porte ouverte, défaut inactif | Numéro de réponse et détail de requête non visibles ; fermeture relue à compléter. |
| Test utilisateur FC03 adresse 100, quantité 1 : exception 02 | Sortie Python attestée ; octets et numéros de trames non capturés dans cette image. |
| Deux paires FC05 4/6 et 44/46 | Valeurs de chaque paire non visibles dans la liste. |
| Écriture FC05, coil 0 à 0x0000 | Fermeture documentée ; numéro exact et écho de réponse à développer. |
| Transaction 1, protocole 0, longueur 6, unité 1 sur les demandes détaillées | Ces identifiants n’établissent pas une identité humaine. |

**À compléter :** détail d’ouverture **coil 0 / 0xFF00**, relecture de la porte fermée (l’état ouvert est désormais attesté par FC01), trames de l’exception 02 si demandées (sortie Python désormais attestée) et restauration finale attestée par `status`. La valeur d’écriture 0xFF00 reste vérifiée dans le code et le test local, sans détail utilisateur développé ; l’erreur 02 est désormais attestée dans le terminal utilisateur.

## 4 — Préparer la mise en commun et restaurer

| Élément à conserver | État |
| --- | --- |
| Table complète des sept variables | Renseignée sur documentation et code. |
| Capture d’une lecture | FC03 et FC04 documentés par les six images ; valeurs des réponses à compléter. |
| Capture d’une écriture | Deux paires FC05 attestées ; coil 0 à 0x0000 détaillée. Ouverture 0xFF00 à développer. FC06 reste documenté en 2.2. |
| Erreur d’adresse invalide | Test local et sortie Python utilisateur réussis : `ProtocolError Modbus exception code 2`. Requête/réponse Wireshark non encore documentées. |
| Numéros de trames, ports clients et identifiants | À relever pour les nouveaux essais, sans réutiliser ceux d’une ancienne capture. |

Avant de terminer l’autonomie :

```bash
python3 -m lab.client setpoint 4
python3 -m lab.client door 0
python3 -m lab.client status
```

Vérifier **`setpoint=4.0` et `door=0`**. Conserver la sortie, ainsi que le contexte du défaut, du mode automatique et de la version du programme. Ces preuves rejoindront le dossier de validation du jumeau numérique en fin de journée ; ce dossier n’est pas déclaré validé par la seule rédaction de la fiche.

## Ressources

- `docs/REGISTER_MAP.md`, `lab/client.py`, `lab/modbus.py` et `lab/model.py` dans le laboratoire fourni.
- [Modbus Organization — Specifications](https://www.modbus.org/modbus-specifications).
- [Spécification applicative V1.1b3 — §6.5, §6.6 et §7](https://www.modbus.org/file/secure/modbusprotocolspecification.pdf), consultée le **27 octobre 2026**.

[Retour à l’itération 1](index.md) · [Atelier précédent — Analyse Wireshark](analyser-echanges-modbus-wireshark.md)
