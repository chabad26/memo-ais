# 4.5 — Atelier 5 | Mettre en œuvre le filtrage IT/OT

## 🎯 Objectif et modalités

Configurer des règles de pare-feu limitant les communications entre un environnement IT et une installation OT.

- **Modalité :** TP en autonomie, individuel ou en binôme ; formateur absent, ressources et entraide du groupe.
- **Environnement retenu :** VM **Debian `192.168.122.105`**, accès SSH utilisateur `oliv`, laboratoire Python/Modbus et nftables.

!!! info "État vérifié : laboratoire et filtrage appliqués sur la VM"
    Le 29 octobre 2026, les fichiers ont d’abord été préparés en SSH ; `sudo -n` exigeait une saisie locale. Après exécution dans le terminal utilisateur, les quatre namespaces et la table de filtrage sont présents. Les preuves du run **20261029T094737Z**, relues sur la VM et récupérées dans le dépôt, attestent **8 contrôles conformes** à 09:47:41 UTC (**10:47:41, heure de Paris**). Le ruleset hôte est inchangé entre les relevés. Les tests de panne/reprise, source supplémentaire, révocation persistante et REG-02 physique ne sont pas couverts par ce résultat.

## 1 — Vérifier et préparer la topologie

La documentation initiale ne fournissait pas de plan IP détaillé. La topologie suivante est une **proposition de TP isolé**, préparée pour cette VM ; ce n’est ni une topologie Montval relevée ni une approbation du formateur.

| Espace réseau | Interface / adresse | Rôle et route |
| --- | --- | --- |
| `ais45-it` | `it0` : **10.77.10.2/24** | Client IT ; défaut via 10.77.10.1. |
| `ais45-fw` | `fw-it` : **10.77.10.1/24** ; `fw-dmz` : **10.77.20.1/24** ; `fw-ot` : **10.77.30.1/24** | Pare-feu routant ; seul espace où le forwarding IPv4 est activé. |
| `ais45-gw` | `dmz0` : **10.77.20.2/24** | Passerelle Modbus **15021**, dashboard HTTP **18080** ; défaut via 10.77.20.1. |
| `ais45-ot` | `ot0` : **10.77.30.2/24** | Serveur/modèle Modbus **15020** ; défaut via 10.77.30.1. |

```text
IT 10.77.10.2 → ais45-fw → GW 10.77.20.2:15021
                                  ↓ nouvelle connexion initiée par GW
                               ais45-fw → OT 10.77.30.2:15020

IT 10.77.10.2 → ais45-fw → OT direct : REFUSÉ après application
IT 10.77.10.2 → ais45-fw → GW:18080 : consultation HTTP autorisée
```

Les trois liaisons sont des veth entre namespaces. **Aucune liaison vers le réseau de gestion, Internet ou le LAN**, aucun NAT. Le script ne modifie ni le ruleset, ni les routes, ni les sysctl de l’hôte ; l’interface SSH **`enp1s0`, 192.168.122.105** reste hors du chemin de données du TP. IPv6 est désactivé dans ces seuls namespaces : cette simplification ne démontre pas une politique IPv6 de production.

Le dashboard est configuré pour lire **la passerelle 15021**, contrairement au défaut du PoC qui vise le port direct. Le proxy utilise ensuite son adresse DMZ pour joindre le serveur. Les deux connexions traversent le pare-feu, tandis que la régulation s’exécute localement dans le serveur OT.

### Fichiers disponibles

- [Archive reproductible complète ZIP](../../assets/files/informatique-industrielle/it-3/Montval-4.5-lab-it-ot.zip) : scripts, règles, source PoC, licence et README.
- [README du laboratoire](../../assets/files/informatique-industrielle/it-3/Montval-4.5-README.md).
- [Script de préparation/application/export](../../assets/files/informatique-industrielle/it-3/Montval-4.5-lab-it-ot.sh).
- [Source nftables](../../assets/files/informatique-industrielle/it-3/Montval-4.5-filtrage-it-ot.nft).
- [Vérificateur Python](../../assets/files/informatique-industrielle/it-3/Montval-4.5-verify.py) et [manifeste de préparation sur VM](../../assets/files/informatique-industrielle/it-3/Montval-4.5-preparation-vm.json).

La copie `~/ais-it-ot-j4/poc` reprend les fichiers Python du PoC présent sur la VM ; leurs empreintes ont été comparées aux sources incluses dans l’archive. L’original `~/ot-refrigeration-poc`, ses captures et son historique Git restent en place. Le code observé utilise les seuils **±0,5 °C**. Cette vérification de fichiers ne prouve pas l’exécution du modèle dans les nouveaux espaces.

### Exécution guidée dans le terminal SSH — pour reproduire

```bash
ssh oliv@192.168.122.105
cd ~/ais-it-ot-j4
sudo bash ./lab-it-ot.sh all
```

`all` prépare le réseau privé, relève un état de référence avec accès direct encore possible, vérifie la syntaxe nftables dans le namespace, applique le filtrage puis lance les contrôles et exporte. Le réseau permissif de référence reste entièrement interne aux namespaces. Le script refuse d’écraser un TP déjà présent.

Pour travailler étape par étape **à la place de `all`** :

```bash
cd ~/ais-it-ot-j4
sudo bash ./lab-it-ot.sh setup
sudo bash ./lab-it-ot.sh inspect
sudo bash ./lab-it-ot.sh apply
sudo bash ./lab-it-ot.sh verify
```

En cas d’échec, examiner les journaux et l’état existant ; ne pas relancer `all` en boucle. Les commandes suivantes ne sont utilisables qu’après préparation réussie :

```bash
sudo ip netns exec ais45-it ip -br addr
sudo ip netns exec ais45-it ip route
sudo ip netns exec ais45-gw ss -lnt
sudo ip netns exec ais45-ot ss -lnt
sudo ip netns exec ais45-fw ip -br addr
sudo ip netns exec ais45-fw ip route
```

## 2 — Examiner et conserver les règles initiales

Sur le pare-feu du TP, dans **le bon espace** :

```bash
sudo ip netns exec ais45-fw nft list ruleset
```

`setup` conserve l’état initial de chaque espace dans `evidence/run-<date UTC>/avant/` ainsi qu’un relevé **en lecture seule** du ruleset hôte dans `hote-avant.nft`. Les namespaces nouvellement créés ont une référence vide ; le script n’efface pas les règles d’un environnement préexistant pour obtenir ce résultat.

Identifier tables, chaînes, hooks, priorités, politique et règles. La source de filtrage crée une table **`inet ais45`**, chaîne **`forward`**, politique **`drop`**, uniquement dans `ais45-fw`. Les communications passent effectivement par cet espace routant : il ne s’agit plus d’un filtrage `forward` sur des processus communiquant entre eux sur le loopback de l’hôte.

Le script et son README expliquent `reset-filter` et `teardown` avant utilisation ; aucune commande de remise à zéro générale de l’hôte n’est fournie.

## 3 — Configurer et comprendre le filtrage

| Source → destination | Service | Politique mise en fichier | Contrôle attendu après application |
| --- | --- | --- | --- |
| IT **10.77.10.2** → GW **10.77.20.2** | TCP **15021** | Autoriser nouvelles connexions et poursuite de ce tuple. | Consultation Modbus possible via GW. |
| IT **10.77.10.2** → GW **10.77.20.2** | TCP **18080** | Autoriser consultation HTTP de ce TP. | Réponse HTTP/API et collecte via GW disponibles. |
| GW **10.77.20.2** → OT **10.77.30.2** | TCP **15020** | Autoriser nouvelles connexions et poursuite de ce tuple. | Seule cette origine DMZ initie le transport Modbus vers OT dans la topologie fournie. |
| GW → IT et OT → GW | Réponses des services autorisés | Autoriser uniquement `established`, sources/destinations et ports de service correspondants. | Retour des communications permises sans ouverture générale dans le sens inverse. |
| IT ↔ OT direct | Tous protocoles/ports | Refus explicite **avant** les acceptations de sessions. | Accès direct impossible, même si une connexion ancienne subsistait. |
| Paquets invalides ; IPv6 ; autres flux interzones | Non autorisés | Refus et compteurs ; erreurs ICMP `related` utiles admises selon la règle du fichier. | Pas d’ouverture implicite d’un nouveau service ; autres paquets rejetés. |

La [source nftables complète](../../assets/files/informatique-industrielle/it-3/Montval-4.5-filtrage-it-ot.nft) est fournie, pas seulement une capture. `apply` effectue `nft -c -f` puis `nft -f` **dans `ais45-fw`** ; `chargement.nft` conserve le lot exact utilisé. Une réapplication remplace uniquement la table `inet ais45` de cet espace dans un lot, sans vider les autres tables.

**Limite applicative :** autoriser TCP 15020 ou 15021 ne distingue pas une lecture d’une écriture. Le proxy fourni refuse les fonctions hors 01–04. Le pare-feu empêche le client IT de contourner ce proxy en joignant le serveur direct. Le TP ne réalise ni les deux rôles lecture/maintenance du GW-02 industriel de 4.3, ni un contrôle de plages/registres de production.

## 4 — Vérifier la politique par défaut et les effets réels

La source est fondée sur des tuples précis, pas une acceptation universelle `established,related`. Le refus direct IT/OT précède les permissions de retour. Les compteurs nommés indiquent le passage dans les autorisations IT/GW, GW/OT, les retours et les refus. Une ancienne session n’est pas une autorisation en soi ; aucun essai de révocation d’une session persistante de maintenance n’est réalisé par ce vérificateur.

Le script contrôle les points suivants **lorsque l’utilisateur l’exécute** :

| Vérification | Attendu | Preuve générée |
| --- | --- | --- |
| Référence avant filtrage | IT peut lire directement OT et via GW dans le réseau privé initial. | `baseline.json`, relevés et écoutes `avant/`. |
| T01 / T02 | GW lit OT ; IT lit via GW après filtrage. | Sorties clients et codes de retour dans `verification.json`. |
| T03 / T05 | Écritures FC06 et FC05 via GW refusées par exception 01 ; consigne/porte inchangées après relecture. | Erreurs applicatives et relevés avant/après ; aucune écriture directe de test sur OT. |
| T04 | Client IT ne lit plus OT directement ; serveur disponible depuis GW et compteur `it_direct_drop` en hausse. | Échec client corrélé à l’augmentation du compteur et au contrôle positif autorisé. Un timeout seul n’est pas qualifié de preuve. |
| T07 | HTTP `/api` accessible depuis IT, valeurs Modbus lues via la passerelle. | Code HTTP et données JSON. Pas une capture de navigateur. |
| Traversée des règles | Compteurs IT/GW, GW/OT et réponses non nuls. | JSON et export nft après essais. |
| État hôte | Comparaison des exports hôte avant/après ; aucun ordre de modification hôte dans les scripts. | `comparaison-hote.txt` ; examiner toute différence, par exemple due à un autre service. |

Le vérificateur retourne un code non nul si un contrôle échoue et conserve ses observations ; un échec doit être analysé, pas renommé « protection réussie ». Les tests de panne/reprise T08/T10, source supplémentaire T06, révocation persistante T09 et équipements physiques restent hors de la validation automatique.

### Vérifications manuelles dans le TP préparé

Depuis `~/ais-it-ot-j4/poc` :

```bash
# Chemin permis
sudo ip netns exec ais45-it python3 -m lab.client status   --host 10.77.20.2 --port 15021

# Chemin direct interdit après application
sudo ip netns exec ais45-it python3 -m lab.client status   --host 10.77.30.2 --port 15020

# Règles et compteurs au point de passage
sudo ip netns exec ais45-fw nft -a list ruleset
```

Pour une capture facultative, sur une interface réellement traversée :

```bash
sudo ip netns exec ais45-fw tcpdump -i fw-it -nn -s 0   -w /home/oliv/ais-it-ot-j4/capture-it-j4.pcap   'tcp port 15020 or tcp port 15021 or tcp port 18080'
```

Exécuter les requêtes depuis un autre terminal puis arrêter tcpdump. Une capture côté IT ne montre pas nécessairement ce qui atteint OT : compléter côté `fw-ot` si besoin. Ces PCAP ne sont pas produits par la simple préparation des fichiers.

Le navigateur du poste ne possède aucune route vers les namespaces ; aucun port de la VM n’est publié. La consultation HTTP automatisée se fait depuis IT du TP. Les commandes ne touchent ni le réseau de l’établissement ni une machine extérieure au périmètre de cette VM et de ses namespaces.

## 5 — Sauvegarder, reproduire et remettre en état

Après exécution, le dossier `~/ais-it-ot-j4/evidence/run-<date UTC>/` contient les règles sources, `chargement.nft`, relevés par espace, JSON, journaux et export réel final **`regles-it-ot.nft`**. Pour exporter manuellement la configuration **du pare-feu isolé** :

```bash
cd ~/ais-it-ot-j4
sudo ip netns exec ais45-fw nft -a list ruleset > regles-it-ot.nft
```

Le fichier sans namespace `sudo nft list ruleset` viserait l’hôte, pas les règles de ce TP. Garder ensemble la source et les commandes d’application : un export final n’explique pas à lui seul comment les interfaces/routes ont été préparées. Pour rejouer, utiliser `apply` avec son remplacement ciblé plutôt que charger à l’aveugle un export sur un environnement déjà configuré.

- **`sudo bash ./lab-it-ot.sh reset-filter`** : retire seulement `inet ais45` du namespace pare-feu ; le réseau privé redevient permissif. Ne pas confondre ce retour de référence avec un état protégé.
- **`sudo bash ./lab-it-ot.sh apply`**, puis **`verify`** : remet et vérifie la protection.
- **`sudo bash ./lab-it-ot.sh teardown`** : arrête les processus des quatre espaces du TP et les supprime ; modèle et état en mémoire perdus, preuves sur disque conservées. Ne pas utiliser ces espaces pour d’autres travaux.

## État des preuves et résultats observés

**Préparation établie :** accès SSH, versions/outils, fichiers déposés, syntaxe Bash/Python et concordance des sources PoC. **Exécution désormais attestée :** état initial, application de `inet ais45` dans `ais45-fw`, vérifications et export réel du run ci-dessous. L’agent a relu les résultats après leur production ; il n’a pas contourné la saisie sudo.

### Exports et preuves récupérés

- [Règles réellement appliquées — export nft avec handles et compteurs](../../assets/files/informatique-industrielle/it-3/Montval-4.5-applique-regles-it-ot.nft).
- [Résultats observés — JSON](../../assets/files/informatique-industrielle/it-3/Montval-4.5-applique-verification.json).
- [Référence avant filtrage — JSON](../../assets/files/informatique-industrielle/it-3/Montval-4.5-applique-baseline.json).
- [Comparaison du ruleset hôte](../../assets/files/informatique-industrielle/it-3/Montval-4.5-applique-comparaison-hote.txt).
- [Dossier des preuves du TP — ZIP](../../assets/files/informatique-industrielle/it-3/Montval-4.5-preuves-20261029.zip) : règles initiales/finales du namespace, lot de chargement, interfaces/routes/écoutes, journaux et résultats ; les relevés hôte détaillés sont conservés dans le dépôt sans être inclus dans ce téléchargement.

| Contrôle réel | Résultat observé |
| --- | --- |
| Référence avant filtrage | Les lectures IT → serveur direct et IT → GW réussissent dans le réseau privé initial ; le serveur n’était pas simplement indisponible. |
| T01 | GW lit OT ; état initial lu : 5,0 °C, consigne 4,0 °C, compresseur actif. |
| T02 | IT lit via GW ; consigne 4,0 °C, porte fermée, défaut inactif et auto actif. |
| T03 | Tentative de consigne 6 °C via GW refusée : **Modbus exception code 1**, code retour client 1. |
| T05 | Tentative `door 1` via GW refusée par la même exception. |
| T04 | Direct IT → OT en timeout ; **compteur `it_direct_drop` passé de 0 à 3** avec lecture GW → OT disponible. Le refus est donc corrélé au point de filtrage, pas déduit du timeout seul. |
| Relecture après écritures refusées | Consigne toujours **4,0 °C**, porte toujours **0** ; température 4,9 °C et compresseur actif. |
| T07 | HTTP **200** sur `/api` depuis IT ; température 4,9 °C, consigne 4,0 °C, compresseur actif, porte fermée et alarme inactive. Pas de capture de navigateur produite. |
| Compteurs / hôte | Les trois compteurs autorisations IT/GW, GW/OT et retours sont non nuls ; règles et réponses réellement traversées. Exports hôte avant/après identiques. |

Le JSON `verification.json` contient **8 contrôles conformes** (T01, T02, T03, T05, T04, relecture, T07 et compteurs). Les valeurs de compteurs du JSON sont celles du moment du contrôle ; l’export final peut être plus élevé après les requêtes HTTP et la relecture. Le compteur `other_drop` reste à 0 dans cet export : la politique par défaut est bien `drop`, mais tous les cas de refus de services non listés ne sont pas couverts par cette série.

Les sources, le lot réellement chargé et les exports sont conservés dans `livrables/informatique-industrielle/it-3/lab-it-ot/`, avec preuves sous `preuves-20261029/run-20261029T094737Z/`. Le manifeste de préparation téléchargeable garde son statut historique « avant application » ; les résultats et exports de cette section constituent la preuve d’exécution ultérieure.

**Limites :** essais du simulateur sur une topologie IPv4 proposée, pas installation Montval réelle, pas application intégrale des 32 règles d’entreprise, pas validation du GW-02 industriel ni de session de maintenance persistante. Les namespaces ont été laissés actifs après vérification ; `teardown` reste une action explicite de l’utilisateur. Aucun PCAP ni résultat graphique n’est inventé.

## Captures utilisateur — compléments du 29 octobre

Douze captures J4 ont été examinées et intégrées, dont huit nouvelles pour les essais complémentaires. Elles sont conservées dans `assets/img/informatique-industrielle/it-4/` selon le classement fourni ; elles complètent **l’itération 3 / J4**, sans créer une nouvelle itération. Aucun secret saisi n’est visible et aucune de ces images n’est écartée comme doublon.

### 10:55:08 — Lancement du TP et contrôles automatiques

![Lancement du TP et contrôles automatiques](../../assets/img/informatique-industrielle/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-29%2010-55-08.png)

La commande `sudo bash ~/ais-it-ot-j4/lab-it-ot.sh all` est visible. La référence initiale autorise le direct dans le réseau privé, puis les contrôles de lecture, refus FC05/FC06, refus direct, relecture, HTTP et compteurs sont affichés conformes. Le message de comparaison indique le ruleset hôte inchangé. Les avertissements sur les tables gérées par `iptables-nft` accompagnent les relevés hôte effectués en lecture seule ; les règles du TP sont appliquées dans la table `inet ais45` du namespace pare-feu, pas dans ces tables hôte.

### 10:55:57 — Ruleset réellement présent dans ais45-fw

![Ruleset réellement présent dans ais45-fw](../../assets/img/informatique-industrielle/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-29%2010-55-57.png)

La table `inet ais45`, la chaîne `forward` à politique `drop`, les interfaces et règles sont visibles. Le compteur `it_direct_drop` vaut **6 paquets / 360 octets**, contre **3 paquets** dans l’export de fin du run initial. Ce relevé ultérieur est distinct ; il ne faut ni remplacer le premier export ni interpréter six paquets comme six essais utilisateur. Les autorisations et retours ont des compteurs non nuls ; `other_drop` est encore à **0** sur cette capture.

### 10:56:16 — Lecture permise par la passerelle

![Lecture permise par la passerelle](../../assets/img/informatique-industrielle/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-29%2010-56-16.png)

La commande depuis `ais45-it` vise **10.77.20.2:15021**. L’état affiché est **4,0 °C**, consigne **4,0 °C**, compresseur **1**, alarme **0**, porte **0**, défaut **0**, auto **1**. Le compresseur actif à 4 °C est compatible avec le maintien d’état dans la bande d’hystérésis ; cette image seule ne prouve pas un cycle complet.

### 11:14:06 — Tentative directe vers OT et timeout

![Tentative directe vers OT et timeout](../../assets/img/informatique-industrielle/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-29%2011-14-06.png)

La commande depuis `ais45-it` vise **10.77.30.2:15020** et se termine par `TimeoutError: timed out`. C’est cohérent avec le chemin direct interdit, mais cette capture ne fournit pas à elle seule une preuve du filtre : la disponibilité du serveur, le chemin autorisé et les compteurs doivent être rapprochés. Le compteur avant/après de **cette tentative précise de 11:14** n’est pas visible ; le run automatique antérieur fournit déjà sa propre corrélation 0 → 3.

### 11:19 — Relecture et compteur du chemin direct

![Relecture autorisée et compteur direct à neuf paquets](../../assets/img/informatique-industrielle/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-29%2011-19-26.png)

La lecture par **10.77.20.2:15021** reste disponible : température **4,4 °C**, consigne **4 °C**, compresseur actif, porte fermée, alarme et défaut inactifs. Le compteur `it_direct_drop` atteint **9 paquets / 540 octets**. Il s’agit d’un relevé cumulé ultérieur, sans paire avant/après propre à la tentative de 11:14.

### 11:20–11:22 — T06 : refus par défaut confirmé sur TCP 18081

![Serveur HTTP temporaire et requête locale acceptée](../../assets/img/informatique-industrielle/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-29%2011-21-30.png)

![Contrôle positif HTTP 200 depuis GW](../../assets/img/informatique-industrielle/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-29%2011-21-37.png)

Le serveur temporaire écoute sur **10.77.20.2:18081** dans `ais45-gw`. Son journal montre un GET accepté à **11:20:48** ; la commande exécutée depuis GW retourne **HTTP 200**. Le service est donc disponible au moment du contrôle positif.

![Compteur other_drop avant et tentative HTTP depuis IT](../../assets/img/informatique-industrielle/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-29%2011-21-56.png)

![Fin du timeout et compteur other_drop après](../../assets/img/informatique-industrielle/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-29%2011-22-25.png)

Les deux captures se complètent : `other_drop` vaut d’abord **0 paquet / 0 octet** ; la requête depuis `ais45-it` expire avec `URLError: <urlopen error timed out>` ; le compteur atteint ensuite **3 paquets / 180 octets**. Le contrôle positif et cette progression attestent le refus du port non autorisé dans cette topologie. **T06 est désormais documenté pour un service supplémentaire**, sans test d’une nouvelle adresse source. Le JSON du run initial reste son instantané historique ; il n’est pas réécrit. L’arrêt du serveur HTTP temporaire n’est pas montré dans ces captures.

### 11:24–11:26 — PCAP du chemin IT : lectures autorisées et SYN directs

![Vue des communications directes et des lectures par la passerelle](../../assets/img/informatique-industrielle/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-29%2011-24-44.png)

![SYN direct vers OT sans données Modbus](../../assets/img/informatique-industrielle/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-29%2011-26-04.png)

![Réponse FC03 par la passerelle](../../assets/img/informatique-industrielle/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-29%2011-26-29.png)

Le [PCAP original téléchargeable](../../assets/files/informatique-industrielle/it-3/Montval-4.5-capture-it-j4.pcap) contient **39 trames**, vérifiées dans le fichier fourni, dont les échanges suivants :

| Trames | Chemin et opération | Observation |
| :-- | :-- | :-- |
| 1–3, 4–6, 37–39 | IT 10.77.10.2 → OT 10.77.30.2:15020 | Trois séries de SYN, sans réponse visible ni charge utile Modbus. |
| 10 / 12 | IT:55372 ↔ GW 10.77.20.2:15021, FC03 | Lecture de trois Holding Registers à partir de 0 : **40, 80, 1** (consigne 4 °C, limite recommandée 8 °C non imposée par ce registre, mode automatique). |
| 20 / 22 | IT:55388 ↔ GW:15021, FC04 | Lecture de quatre Input Registers à partir de 0 : **37, 0, 0, 0**, dont température 3,7 °C à cet instant. |
| 30 / 32 | IT:55396 ↔ GW:15021, FC01 | Lecture de deux coils à partir de 0 ; les deux bits retournés sont à 0. |

La réponse 12 correspond à la requête 10 : transaction **1**, protocole **0**, unité **1**, longueur MBAP **9**, fonction **03**, six octets de valeurs. Wireshark indique **408 µs** entre requête et réponse. Les températures de ces relevés successifs n’ont pas à être identiques.

**Ce PCAP ne contient aucune FC06 ni FC05.** Il complète les preuves de lecture et du chemin direct ; le refus des écritures demeure attesté par le run automatique antérieur. Le point `fw-it` ne montre pas les échanges GW → OT ; l’absence de réponse dans ce fichier s’interprète avec les règles et compteurs déjà vérifiés, pas isolément.

Filtre pour retrouver les trames représentatives :

```wireshark
frame.number in {1,2,3,10,12,20,22,30,32,37,38,39}
```

Empreinte SHA-256 du PCAP conservé :

```text
2138953a3cf6c0fea0ed4094ec9f38e6c858a7388af82e750bd3aea5de005f5f
```

## Essais complémentaires — procédures et état des preuves

Le test du port 18081 et la capture réseau sont maintenant réalisés et commentés ci-dessus. La capture manuelle du refus FC06 reste à compléter ; les essais de panne/reprise et de révocation persistante restent hors des preuves recueillies.

### 1. Priorité : refus par défaut sur un service réellement disponible

L’accès direct OT est déjà testé par une règle explicite. Pour éprouver le **refus des autres ports**, lancer un service temporaire sur le GW en **TCP 18081**, absent de la liste autorisée, confirmer qu’il répond localement puis constater le refus depuis IT et la hausse de `other_drop`. **Ne pas ajouter de règle d’autorisation** pour ce test.

**Terminal A, sur la VM :** utiliser un répertoire temporaire vide pour ne pas publier des fichiers du laboratoire.

```bash
TEST_HTTP_DIR=$(mktemp -d /tmp/ais45-http.XXXXXX)
sudo ip netns exec ais45-gw python3 -m http.server 18081   --bind 10.77.20.2 --directory "$TEST_HTTP_DIR"
```

**Terminal B, sur la même VM :**

```bash
# Contrôle positif : le service est bien disponible depuis son propre espace.
sudo ip netns exec ais45-gw python3 -c   'import urllib.request; print(urllib.request.urlopen("http://10.77.20.2:18081/", timeout=3).status)'

# Relever le compteur avant la tentative IT.
sudo ip netns exec ais45-fw nft list counter inet ais45 other_drop

# Contrôle négatif : port non autorisé depuis IT ; timeout attendu, pas encore observé.
sudo ip netns exec ais45-it python3 -c   'import urllib.request; print(urllib.request.urlopen("http://10.77.20.2:18081/", timeout=3).status)'

# Relever à nouveau le compteur : une hausse doit corroborer le refus.
sudo ip netns exec ais45-fw nft list counter inet ais45 other_drop
```

**À capturer :** réponse HTTP 200 depuis GW, valeur avant, tentative depuis IT et valeur après. Si la tentative réussit ou si le compteur ne bouge pas, conserver l’écart et examiner le chemin ; ne pas annoncer le test réussi. Un traceback de timeout est attendu côté négatif, mais doit être rapproché des autres éléments.

À la fin, arrêter **uniquement le serveur HTTP temporaire** avec `Ctrl+C` dans le terminal A, puis `rmdir "$TEST_HTTP_DIR"` si le répertoire est toujours vide. Ne pas arrêter `lab.gateway` ou `lab.server` pour cet essai. `http.server` est utilisé ici comme cible éphémère dans le réseau privé du TP, pas comme service de production. [Python 3.13 — http.server](https://docs.python.org/3.13/library/http.server.html)

### 2. Capture ciblée du refus d’écriture et de l’état préservé

Le run JSON atteste déjà ce comportement. Une capture rapprochant les messages bruts et la relecture sera plus parlante pour le dossier :

```bash
cd ~/ais-it-ot-j4/poc
sudo ip netns exec ais45-it python3 -m lab.client status   --host 10.77.20.2 --port 15021
sudo ip netns exec ais45-it python3 -m lab.client setpoint 6   --host 10.77.20.2 --port 15021
sudo ip netns exec ais45-it python3 -m lab.client status   --host 10.77.20.2 --port 15021
```

**Attendu :** exception 01, consigne inchangée ; température possiblement différente parce que la simulation continue. Essai uniquement sur ce modèle ; si une écriture est acceptée par erreur, consigner puis restaurer la consigne par une voie autorisée. Ne pas réinitialiser le modèle pour masquer l’écart.

### 3. Conserver un PCAP du chemin autorisé et du refus

Utiliser la commande tcpdump de la section 4, dans un terminal dédié sur `fw-it`, pendant les lectures et le refus FC06. Arrêter la capture ensuite, conserver le fichier et relever les trames représentatives. Un second point sur `fw-ot` peut montrer les lectures relayées et l’absence de transfert de l’écriture rejetée.

Pour la preuve : rapprocher les captures amont/aval et les heures ; un paquet absent d’un seul fichier n’est pas une preuve suffisante de filtrage si le point de capture n’est pas validé. La segmentation et le proxy sont deux contrôles différents : refus direct réseau d’un côté, réponse Modbus d’exception de l’autre.

**Suite possible du plan 4.4 :** panne et reprise de la passerelle (T08/T10), en préservant `lab.server` et en observant le contrôle local. Ces essais restent à préparer séparément pour identifier précisément le processus à arrêter ; ils ne sont pas déclarés réalisés par les captures actuelles.

Les compteurs nftables comptent paquets et octets, éventuellement pour plusieurs règles partageant le même compteur, et non le nombre de sessions humaines. Ne pas les remettre à zéro pour obtenir une capture plus nette : conserver les valeurs avant/après. [nftables — Counters](https://wiki.nftables.org/wiki-nftables/index.php/Counters)

## Ressources

- [Plan d’essais 4.4](preparer-essais-segmentation.md), [politique 4.2](definir-acces-regles-pare-feu.md), [REG-02 et limites 4.3](proteger-regulateur-industriel-obsolete.md).
- [nftables Wiki](https://wiki.nftables.org/) et [suivi des connexions](https://wiki.nftables.org/wiki-nftables/index.php/Matching_connection_tracking_stateful_metainformation).
- Laboratoire original : `livrables/informatique-industrielle/ot-refrigeration-poc/`. Scripts de reproduction du TP : `livrables/informatique-industrielle/it-3/lab-it-ot/`.

[Retour à l’itération 3](index.md) · [Pense-bête](../../pense-bete/glossaire/informatique-industrielle/it-3.md)
