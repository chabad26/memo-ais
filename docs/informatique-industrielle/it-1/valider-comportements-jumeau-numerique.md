# 2.6 — Atelier 6 | Valider les comportements du jumeau numérique

**Itération 1 · Journée 2 · TP en binôme et analyse avec le formateur.**

## Objectif et portée

**Vérifier que le modèle numérique reproduit les comportements spécifiés de l’installation frigorifique.**

Le protocole ci-dessous définit les résultats attendus **avant les essais** et consolide les observations déjà documentées en J1/J2. **Six captures utilisateur** documentent désormais une série d’essais à consigne 6 °C et une restauration finale à 4 °C. L’empreinte/version du modèle et les cycles complets ne sont pas visibles ; cette série ne constitue pas une campagne exhaustive sur une version identifiée. La comparaison et l’approbation avec le formateur restent à confirmer ; aucune validation d’une installation physique réelle n’est revendiquée.

## Préparer une campagne comparable

### Identifier la version et les conditions

Depuis le répertoire du laboratoire, relever la version effective du fichier :

```bash
sha256sum lab/model.py
rg -n 'self.temp >=|self.temp <=' lab/model.py
```

Si `rg` n’est pas installé, ouvrir `lab/model.py` avec `less`. Le modèle initial utilise **±0,5 °C**. La variante **±1 °C** de l’atelier 1.5 doit être identifiée ou restaurée à partir de la sauvegarde connue, serveur arrêté. Un redémarrage seul **ne restaure pas le code** : il recharge le fichier présent.

Noter également : date/heure, copie utilisée, ports, mode automatique, défaut, porte, consigne et état du compresseur. L’empreinte du fichier permet d’éviter de comparer deux versions comme si elles étaient identiques.

### Remise à l’état initial

Pour retrouver les conditions initiales calculées par le code, arrêter **le serveur identifié** avec Ctrl + C, puis le relancer dans son terminal :

```bash
python3 -m lab.server
```

Une nouvelle instance démarre à **5 °C**, ambiance **22 °C**, consigne **4 °C**, porte fermée, défaut inactif, mode automatique actif, compresseur arrêté avant le premier pas. Il démarre ensuite selon la règle au premier calcul. La supervision peut afficher une indisponibilité pendant l’arrêt ; la passerelle ne recrée pas le processus à la place du serveur.

Si un redémarrage n’est pas souhaité, on peut remettre les paramètres avec les commandes suivantes, mais **cela ne remet ni la température ni tout l’historique interne à l’état initial** :

```bash
python3 -m lab.client setpoint 4 --port 15020
python3 -m lab.client door 0 --port 15020
python3 -m lab.client sensor-fault 0 --port 15020
python3 -m lab.client auto 1 --port 15020
python3 -m lab.client status --port 15020
```

Les trois services et l’accès web sont décrits dans l’[atelier 2.5](assembler-composants-jumeau-numerique.md). Utiliser le port **15020** pour préparer les états : la passerelle **15021** bloque les écritures.

## 1 — Définir les six scénarios de validation

Les critères ci-dessous valent pour le modèle initial, en automatique et sans défaut sauf mention contraire. Les températures affichées sont arrondies et les observations espacées peuvent manquer une bascule exacte.

| ID / scénario | État initial et manipulation | Résultat attendu avant essai | Critère à vérifier |
| --- | --- | --- | --- |
| **V1 — Fonctionnement normal** | Consigne 4 °C, porte fermée, défaut inactif ; observer plusieurs cycles après le démarrage. | Marche à T ≥ 4,5 °C, arrêt à T ≤ 3,5 °C ; conservation de l’état dans la bande. | Trajectoire et alternances cohérentes avec les seuils ; ne pas juger le maximum initial de 5 °C comme un écart du cycle stabilisé. |
| **V2 — Consigne 4 → 6 °C** | Situation connue à consigne 4 °C ; écrire `setpoint 6` en direct. | Consigne relue à 6 °C ; nouveaux seuils 5,5 / 6,5 °C, commande réévaluée, température progressive. | Écriture et relecture attestées ; commande et tendance cohérentes avec l’état initial. Aucun saut instantané imposé à 6 °C. |
| **V3 — Porte ouverte** | Comparer des conditions aussi proches que possible : température, ambiance, consigne et compresseur ; ouvrir puis fermer la porte. | Apport thermique doublé dans le modèle. Si le compresseur tourne, la température peut encore baisser mais plus lentement. | Porte relue à 1 puis 0 ; série de mesures comparables montrant l’effet thermique. Ne pas exiger systématiquement une hausse immédiate. |
| **V4 — Défaut capteur** | Consigne 4 °C, porte fermée ; observer si possible une phase compresseur en marche ; injecter le défaut. | Compresseur forcé à l’arrêt au prochain calcul ; réchauffement progressif dans les conditions nominales. | Défaut relu à 1 et compresseur arrêté même au-dessus du seuil haut ; retrait du défaut et reprise conforme à température/mode. |
| **V5 — Lecture via passerelle** | Serveur et passerelle actifs ; consulter les deux accès. | FC01–FC04 autorisées par le proxy, réponses du même modèle. | Consigne et états cohérents entre les chemins ; petits écarts thermiques possibles entre lectures successives. |
| **V6 — Écriture refusée** | Consigne confirmée à 4 °C ; tenter `setpoint 6 --port 15021`. | Refus applicatif exception 01, sans modification de la consigne par cette tentative. | Réponse d’exception / message client et relecture toujours à 4 °C ; pas de confusion avec un timeout. |

## 2 — Réaliser et documenter les essais

### V1 — Régulation normale

```bash
python3 -m lab.client status --port 15020
```

Répéter les lectures sur plusieurs minutes et comparer avec le navigateur. Conserver les instants des états marche/arrêt. La méthode doit permettre de voir les deux phases ; une seule température proche de la consigne ne valide pas un cycle.

Pour produire un relevé local horodaté depuis le dossier du laboratoire, exemple de suivi de cinq minutes :

```bash
for i in $(seq 1 60); do
  date -Iseconds
  python3 -m lab.client status --port 15020
  sleep 5
done | tee validation-v1.log
```

Ce relevé est une procédure proposée, pas un fichier déjà produit. Son pas d’observation ne permet pas de chronométrer une transition à 0,1 s ; il sert à observer une tendance et des états. Choisir un nom distinct si un relevé précédent doit être conservé.

### V2 — Nouvelle consigne

```bash
python3 -m lab.client setpoint 6 --port 15020
python3 -m lab.client status --port 15020
python3 -m lab.client status --port 15021
```

Conserver la vue web, les réponses et les observations suivantes. Une commande déjà arrêtée peut rester arrêtée sans que le test échoue. Restaurer après l’observation :

```bash
python3 -m lab.client setpoint 4 --port 15020
```

### V3 — Perturbation par la porte

```bash
python3 -m lab.client door 1 --port 15020
python3 -m lab.client status --port 15020
```

Relever plusieurs températures, le temps et le compresseur, puis :

```bash
python3 -m lab.client door 0 --port 15020
python3 -m lab.client status --port 15020
```

Pour comparer une vitesse d’évolution, ne pas opposer une phase porte fermée/compresseur en marche à une phase porte ouverte/compresseur arrêté comme si seule la porte changeait. Deux essais depuis des conditions initiales identiques permettent une comparaison plus propre.

### V4 — Défaut puis reprise

```bash
python3 -m lab.client sensor-fault 1 --port 15020
python3 -m lab.client status --port 15020
```

Le dashboard n’affiche pas le défaut : conserver une lecture CLI. La température simulée reste visible et l’alarme haute peut être inactive malgré le défaut. Après observation :

```bash
python3 -m lab.client sensor-fault 0 --port 15020
python3 -m lab.client status --port 15020
```

Le redémarrage éventuel dépend de la température. La règle d’arrêt sur défaut est propre au scénario, pas une garantie universelle de sûreté frigorifique.

### V5 — Lecture relayée

```bash
python3 -m lab.client status --port 15020
python3 -m lab.client status --port 15021
```

Comparer les états et la consigne ; noter le temps écoulé entre lectures. Le navigateur, par défaut, lit le port direct et ne prouve donc pas à lui seul le passage par la passerelle.

### V6 — Écriture rejetée et valeur conservée

```bash
python3 -m lab.client setpoint 4 --port 15020
python3 -m lab.client status --port 15021
python3 -m lab.client setpoint 6 --port 15021
python3 -m lab.client status --port 15021
python3 -m lab.client status --port 15020
```

Attendu : **`Modbus operation failed: Modbus exception code 1`**, puis consigne toujours **4 °C**. La PDU d’exception à FC06 est **86 01**. Le refus ne bloque pas les écritures sur l’accès direct 15020 ; ne pas en déduire une segmentation.

### Fiche de résultat à utiliser pour chaque essai

| Champ | Contenu à renseigner |
| --- | --- |
| ID, date, opérateurs et version | Identifier le scénario, le fichier modèle et l’environnement. |
| État initial | Température, consigne, compresseur, porte, défaut, mode et alarme. |
| Manipulation et résultat attendu | Consigner avant l’exécution. |
| Résultat observé et instants | CLI, supervision, trames et mesures utiles. |
| Écart / explication | Différencier délai, arrondi, erreur de configuration et véritable comportement inattendu. |
| Conclusion et preuve | Conforme dans les conditions testées, partiel ou non concluant ; noms des fichiers/captures. |
| État final | Paramètres restaurés, processus conservé ou redémarré, anomalie résiduelle. |

## État des preuves — antériorité et campagne 2.6

Les preuves antérieures sont réutilisables en précisant **leur session et leur périmètre**. Elles ne sont pas transformées en une campagne complète, synchronisée et validée collectivement.

| Scénario | Éléments déjà disponibles | Conclusion limitée / complément |
| --- | --- | --- |
| **V1** | Captures J1 de températures et états ; calcul direct du modèle initial sur plusieurs cycles, fiche 1.3. | Pas de cycle complet normal à 4 °C dans les six nouvelles captures ; chronométrage et version effective à compléter. |
| **V2** | PCAP d’assemblage **2734/2736** : FC06 à 60 acceptée ; CLI des deux chemins et supervision à consigne 6 °C, puis restauration **8204/8206**. | En 2.6 : écriture 6 °C acceptée, lectures sur les deux ports à 4,1 °C ; températures horodatées à 4,2 °C ensuite. Courbe complète du cycle et instant de bascule non capturés. |
| **V3** | Porte ouverte/fermée attestée en J1 ; FC01 porte à 1 et FC05 fermeture à 0 en 2.3 ; calcul comparatif local porte fermée/ouverte en 1.3. | En 2.6 : porte ouverte, consigne 6 °C, compresseur arrêté, hausse 4,8 → 5,4 °C entre 11:13:18 et 11:13:43 ; après fermeture, hausse 6,0 → 6,3 °C entre 11:14:14 et 11:14:39. Conditions thermiques différentes : comparaison indicative, pas preuve quantitative du facteur deux. |
| **V4** | Captures 1.4 : **5 °C, compresseur OFF** après défaut, puis **5,2 °C, ON** après retrait ; calcul local complémentaire. | En 2.6 : défaut relu à 1, compresseur arrêté et hausse 5,8 → 6,1 °C ; capture suivante avec défaut à 0 et compresseur en marche. Consigne 6 °C, pas 4 °C ; état juste avant défaut et bascule marche → arrêt non montrés. |
| **V5** | PCAP **2554/2564** via 15021 : réponse FC03 **[40, 80, 1]** ; CLI de comparaison des deux accès. | Complément 2.6 : lectures directes et via 15021 identiques à 6,3 °C / consigne 6 °C, puis à 5,8 °C / consigne 4 °C en fin d’essai. |
| **V6** | PCAP **11574/11576** : FC06 via 15021 refusée, **86 01** ; CLI avec consigne relue à 4 °C sur les deux accès. | Complément 2.6 : tentative via 15021 à 6 °C refusée par exception 01 après restauration ; deux lectures toujours à 4 °C. Aucune segmentation démontrée. |

Les détails et captures sont dans les fiches [1.3](prendre-en-main-modele-frigorifique.md), [1.4](observer-dysfonctionnements-consequences.md), [2.3](cartographier-variables-tester-modbus.md) et [2.5](assembler-composants-jumeau-numerique.md). Les tests logiciels déjà réussis sont un appui distinct ; les six captures ci-dessous sont des observations utilisateur, sans nouveau test local exécuté lors de leur intégration.

## Captures utilisateur — six étapes de la série d’essais

Les titres utilisent les heures des fichiers. Les relevés du terminal affichent leurs propres instants au format ISO, avec **+01:00**. La version de l’hystérésis n’est pas visible sur ces captures : les seuils ±0,5 °C restent la référence attendue, pas une configuration vérifiée par ces images.

**Adaptation au protocole :** les essais de porte et de défaut se déroulent ici à **6 °C de consigne**, puis la consigne est ramenée à 4 °C pour le refus via passerelle et l’état final. Cela doit rester explicite dans les conclusions, au lieu de présenter toute la série comme réalisée à 4 °C.

### 11:12:54 — V2 — Consigne 6 °C acceptée, température progressive

![V2 — Consigne 6 °C acceptée, température progressive](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2011-12-54.png)

La commande **`setpoint 6 --port 15020`** est acceptée. Les lectures directe et via **15021** affichent **temp=4.1**, **setpoint=6.0**, **compressor=0**, **door=0**, **sensor_fault=0**, **auto=1**. Le relevé montre ensuite **4,2 °C à 11:12:33 et 11:12:38**. L’écriture n’a pas remplacé la température par la consigne. La température préalable avec consigne 4 °C n’est pas visible ici ; les deux états thermiques à 4,2 °C peuvent s’expliquer par l’arrondi d’affichage.

### 11:13:54 — V3 — Porte ouverte et réchauffement

![V3 — Porte ouverte et réchauffement](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2011-13-54.png)

La commande **`door 1 --port 15020`** est acceptée. La lecture initiale visible donne **4,7 °C**, consigne **6 °C**, porte **1**, compresseur arrêté, défaut inactif et mode auto actif. Dans le relevé, **4,8 °C à 11:13:18** devient **5,4 °C à 11:13:43**, avec les mêmes états : hausse affichée **0,6 °C en 25 s**. La porte ouverte et l’augmentation thermique sont observées ; cette pente dépend de ces conditions.

### 11:14:46 — V3 — Porte fermée et poursuite de l’évolution

![V3 — Porte fermée et poursuite de l’évolution](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2011-14-46.png)

La commande **`door 0 --port 15020`** est acceptée ; la lecture montre alors **5,9 °C**, consigne **6 °C**, porte **0**, compresseur arrêté, défaut inactif et mode auto actif. Le relevé passe de **6,0 °C à 11:14:14** à **6,3 °C à 11:14:39**, soit **0,3 °C en 25 s** sur les valeurs arrondies. La pente affichée est plus faible que dans l’extrait porte ouverte, mais les températures de départ diffèrent : on ne valide pas quantitativement le coefficient thermique à partir de cette seule comparaison.

### 11:16:37 — V4 — Défaut injecté, état arrêté et réchauffement

![V4 — Défaut injecté, état arrêté et réchauffement](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2011-16-37.png)

La commande **`sensor-fault 1 --port 15020`** est acceptée ; la lecture affiche **5,7 °C**, consigne **6 °C**, compresseur **0**, défaut **1**, porte fermée et mode auto actif. Le relevé montre **5,8 °C à 11:16:04**, puis **6,1 °C à 11:16:29**, compresseur toujours arrêté. La capture atteste défaut actif et arrêt, mais pas le passage depuis un compresseur en marche. Avec les seuils initiaux, ces températures restent sous le démarrage à 6,5 °C : cette image seule ne démontre pas l’inhibition au-dessus du seuil haut, déjà illustrée dans l’essai J1 à consigne 4 °C.

### 11:17:17 — V5 — Lectures concordantes après retrait du défaut

![V5 — Lectures concordantes après retrait du défaut](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2011-17-17.png)

Les commandes `status --port 15020` puis `status --port 15021` donnent toutes deux **6,3 °C**, **consigne 6 °C**, **compresseur 1**, **porte 0**, **défaut 0**, **auto 1**. L’état sans défaut et la marche sont observés, mais la commande de suppression et le moment de reprise ne sont pas visibles. Un compresseur actif à 6,3 °C est compatible avec le refroidissement après franchissement du seuil haut ; il ne faut pas attribuer 6,3 °C comme un nouveau seuil de démarrage.

### 11:17:47 — V6 — Refus d’écriture et restauration finale

![V6 — Refus d’écriture et restauration finale](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2011-17-47.png)

L’écriture directe **`setpoint 4 --port 15020`** est acceptée, puis la lecture via 15021 donne **setpoint=4.0**. La tentative **`setpoint 6 --port 15021`** est refusée : **`Modbus operation failed: Modbus exception code 1`**. Les lectures suivantes via 15021 et en direct indiquent toutes deux **temp=5.8**, **setpoint=4.0**, **compressor=1**, **alarm=0**, **door=0**, **sensor_fault=0**, **auto=1**. Le refus et la consigne inchangée sont établis ; les paramètres finaux attendus sont rétablis, même si la température n’est pas encore revenue dans sa bande nominale.

### Conclusion de cette série

**Établi :** écriture de consigne et lectures cohérentes par les deux accès, température progressive, états de porte modifiés avec séries horodatées, défaut actif avec compresseur arrêté, état ultérieur sans défaut en marche, refus d’écriture via proxy et paramètres finaux restaurés.

**Partiel :** cycle normal complet à 4 °C, identification de l’hystérésis chargée, comparaison porte ouverte/fermée à conditions initiales identiques, arrêt précisément provoqué par le défaut et délai de reprise. La présence du formateur et son appréciation ne sont pas déduites des captures.

La série documente donc des comportements cohérents dans son contexte, sans déclarer les six scénarios intégralement validés dans toutes les conditions du protocole.

## 3 — Vérifier les limites du jumeau simplifié

| Limite identifiée | Conséquence pour une modification destinée au réel |
| --- | --- |
| **Compresseur réduit à un booléen et un coefficient** | Impossible de conclure sur usure, pression, puissance, consommation ou temps minimaux de marche/arrêt. Vérifier les prescriptions et tester sur une cible adaptée. |
| **Absence de capteurs et actionneurs réels** | Aucun contrôle du câblage, des étalonnages, délais, saturations ou retours matériels. Une commande affichée ne prouve pas une action réelle. |
| **Modèle thermique simplifié et non calibré** | Une température unique ne représente pas les produits, gradients, humidité, dégivrage ou charge. Les délais calculés ne prédisent pas ceux d’une enceinte physique. |
| **Pas de synchronisation avec une installation réelle** | Les états sont calculés, sans mesures de terrain actualisées ; la fidélité à un équipement ne peut pas être affirmée. |
| **Protections et défaillances limitées** | L’arrêt sur défaut est une hypothèse ; ni toutes les pannes ni les fonctions de sûreté ne sont couvertes. Une modification doit être évaluée avec l’exploitation et les spécialistes du procédé. |
| **Contrôle, physique et réseau dans le même environnement logiciel** | Le comportement d’équipements distribués, des bus de terrain et de leurs pertes de liaison n’est pas entièrement représenté. Le redémarrage de la simulation ne reproduit pas l’évolution d’une installation réelle pendant une panne. |

**Conséquence générale :** valider ces scénarios confirme uniquement les comportements couverts, sur la version et dans les conditions observées. Avant un déploiement réel, il faudrait définir des exigences et tolérances, comparer à des mesures indépendantes, vérifier les protections et préparer une validation adaptée à l’équipement. Aucun seuil alimentaire ni état de sécurité industriel n’est certifié par ce TP.

## Bilan à discuter avec le formateur

> Le laboratoire permet de vérifier des enchaînements cohérents entre écritures, régulation et température simulée. Les échanges via passerelle et le refus de FC06 sont déjà documentés. Les scénarios thermiques nécessitent des observations espacées et des conditions comparables ; leurs résultats ne se déduisent pas d’un simple écho d’écriture. La validation reste limitée à la représentation numérique fictive et aux comportements réellement testés.

Avant de terminer, restaurer consigne 4 °C, porte fermée, défaut inactif et mode automatique actif, puis conserver `status`. Noter si la température et les compteurs ont été conservés ou réinitialisés. L’analyse collective des résultats, les éventuels écarts et la décision finale du formateur restent à consigner.

[Retour à l’itération 1](index.md) · [Atelier précédent — Assemblage](assembler-composants-jumeau-numerique.md)
