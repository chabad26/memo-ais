# 2.2 — Atelier 2 | Analyser les échanges Modbus dans Wireshark

**Itération 1 · Journée 2 · TP en autonomie, individuel ou en binôme.**

## Objectif et statut

**Capturer des communications industrielles, identifier les requêtes Modbus et interpréter les principales informations transportées.** Le formateur est absent pendant cette séance : utiliser les ressources et l’entraide du groupe.

Cette fiche propose la procédure et les réponses attendues à partir du laboratoire fourni. **Dix captures utilisateur sont désormais intégrées** : TCP, décodage initial puis correction, requêtes et réponses FC06. Le fichier PCAP Modbus brut n’a pas été fourni ; les détails FC03/FC04 restent à documenter. Les observations établies sont distinguées des valeurs attendues du code.

## 1 — Démarrer et vérifier le modèle

Dans la VM Debian, se placer dans le dossier contenant `lab/`, `docs/` et `tests/`, puis lancer :

```bash
python3 -m lab.server
```

Dans un autre terminal, depuis le même dossier :

```bash
python3 -m lab.client status
ss -ltn '( sport = :15020 )'
```

Le serveur doit écouter sur **127.0.0.1:15020**. Client et serveur étant locaux à la VM, leurs paquets passent par **`lo`**, pas par `virbr0` sur l’hôte ni par l’interface réseau externe de la VM.

Si un serveur fonctionne déjà, l’utiliser après identification au lieu de lancer une deuxième instance sur le même port. Noter la copie et les seuils utilisés ; le serveur redémarré recrée ses valeurs initiales. La modification d’hystérésis de l’atelier 1.5 et sa restauration doivent rester identifiables.

Pour une capture lisible, arrêter temporairement **le seul `lab.dashboard`** s’il interroge encore le serveur : ses lectures périodiques ajouteraient du trafic. Ne pas arrêter le serveur pendant la capture.

## 2 — Capturer les communications

### Parcours adapté à la VM sans interface graphique

Si `tcpdump` n’est pas installé :

```bash
sudo apt update
sudo apt install tcpdump
```

Depuis le dossier du laboratoire, démarrer la capture dans un terminal distinct :

```bash
sudo tcpdump -i lo -nn -s 0 -w modbus-j2.pcap 'tcp port 15020'
```

Attendre son message d’écoute, puis exécuter **une commande par ligne**, dans le terminal client :

```bash
python3 -m lab.client status
python3 -m lab.client setpoint 6
python3 -m lab.client status
python3 -m lab.client setpoint 4
python3 -m lab.client status
```

La dernière lecture est ajoutée pour confirmer la restauration. Arrêter ensuite **tcpdump uniquement** avec Ctrl + C dans son terminal.

Comme la capture a été écrite avec `sudo`, rendre le fichier à l’utilisateur de la session si nécessaire :

```bash
sudo chown "$(id -u):$(id -g)" modbus-j2.pcap
ls -lh modbus-j2.pcap
sha256sum modbus-j2.pcap
```

Conserver chemin et empreinte. La commande écrase le fichier de même nom lors d’une nouvelle capture : donner un autre nom à chaque essai à préserver.

Depuis **le poste graphique**, copier le fichier en remplaçant le chemin par celui obtenu avec `pwd` dans la VM :

```bash
scp oliv@192.168.122.106:/chemin/du/laboratoire/modbus-j2.pcap .
```

Ouvrir ce PCAP dans Wireshark sur le poste. Un tunnel vers le port Modbus n’est pas nécessaire pour lire le fichier ; capturer le réseau de l’hôte ne montre pas automatiquement les échanges de bouclage internes à la VM.

### Variante avec Wireshark sur la machine du laboratoire

Si Wireshark y est utilisable avec les droits de capture appropriés, sélectionner **`lo`**, démarrer la capture, exécuter la même séquence, arrêter puis enregistrer. Le filtre de capture est :

```text
tcp port 15020
```

### Filtrer et forcer le décodage

Le **filtre d’affichage** à saisir dans Wireshark est différent :

```text
tcp.port == 15020
```

Sélectionner un paquet de la connexion, puis **Analyze → Decode As…** (ou le menu contextuel). Associer le **port TCP 15020** au décodeur **Modbus/TCP**, puis appliquer. Le nom affiché dépend de la langue/version. Cette sélection est nécessaire si le port non standard n’est pas reconnu. [Guide officiel — Decode As](https://www.wireshark.org/docs/wsug_html_chunked/ChCustProtocolDissectionSection.html).

Si seuls certains flux sont reconnus, ou si Query/Response sont inversés, vérifier dans les préférences du protocole Modbus/TCP le **port serveur TCP 15020** (502 par défaut), puis les éventuelles associations Decode As. Une association à un port client éphémère peut produire un décodage partiel ou trompeur ; ce cas est documenté dans les captures ci-dessous.

Après décodage, les filtres suivants facilitent le repérage :

```text
tcp.port == 15020 && modbus.func_code == 3
tcp.port == 15020 && modbus.func_code == 4
tcp.port == 15020 && modbus.func_code == 6
```

Ils sélectionnent aussi les réponses correspondantes ; utiliser le sens et les ports pour les distinguer. Les champs sont documentés dans les références officielles [Modbus](https://www.wireshark.org/docs/dfref/m/modbus.html) et [Modbus/TCP](https://www.wireshark.org/docs/dfref/m/mbtcp.html).

## 3 — Identifier les messages

### Adresses et rôles attendus

| Sens | Source | Destination |
| --- | --- | --- |
| Requête | **127.0.0.1:port_client_éphémère** | **127.0.0.1:15020** |
| Réponse | **127.0.0.1:15020** | **127.0.0.1:port_client_éphémère** |

Les deux adresses IP sont identiques : **les ports et le sens de l’échange distinguent les rôles**. Relever le vrai port client, sans l’inventer. Dans `Client.request()`, chaque requête ouvre une nouvelle connexion TCP ; une commande `status` ouvre donc plusieurs connexions pour ses différentes lectures.

Les paquets SYN, ACK et FIN appartiennent à TCP : ils ne portent pas nécessairement une opération Modbus. Un ACK TCP ne suffit pas à prouver l’acceptation d’une écriture applicative.

### Opérations à retrouver

| Requête issue de la séquence | Adresse / quantité attendues | Réponse attendue selon le code |
| --- | --- | --- |
| FC03 de `status` | Holding **0**, **3 registres** | Consigne, limite conseillée 80 et mode auto. Consigne 40 avant changement, 60 après écriture à 6 °C, puis 40 après restauration. |
| FC04 de `status` | Input **0**, **4 registres** | Température ×10, commande compresseur, alarme et défaut. Valeurs exactes à relever, variables avec le temps et l’état. |
| FC06 de `setpoint 6` | Holding **0**, valeur **60 / 0x003C** | Écho normal de la fonction, de l’adresse et de la valeur. |
| FC06 de `setpoint 4` | Holding **0**, valeur **40 / 0x0028** | Écho normal de la fonction, de l’adresse et de la valeur. |

`status` envoie aussi une **FC01** pour les deux coils porte/défaut. Cette opération supplémentaire n’est pas une anomalie. Sans autre client ni perte de capture, la séquence enrichie ci-dessus produit **11 requêtes applicatives** : trois `status` × trois lectures, plus deux écritures. Ce nombre n’est pas celui des paquets TCP.

### En-tête MBAP et contenu attendu

L’en-tête MBAP fait **7 octets**. Dans l’implémentation locale :

| Champ | Taille | Attendu dans le laboratoire / interprétation |
| --- | --- | --- |
| Transaction Identifier | 2 octets | **1** : fixé dans chaque appel du client, pas un compteur incrémenté. Le serveur le reprend dans sa réponse. |
| Protocol Identifier | 2 octets | **0**, pour Modbus. |
| Length | 2 octets | Nombre d’octets qui suivent ce champ : **Unit Identifier + PDU**. Ce n’est ni la taille du paquet réseau ni celle de l’en-tête MBAP entier. |
| Unit Identifier | 1 octet | **1**, valeur choisie par le client ; pas une identité utilisateur. |

Exemples de longueurs calculées pour ce code : requête FC03/FC04/FC06 **6** ; réponse FC03 lisant 3 registres **9** ; réponse FC04 lisant 4 registres **11** ; réponse normale FC06 **6**.

**Pour apparier les messages :** utiliser connexion/flux TCP, sens, fonction, adresse et identifiant de transaction. Le seul Transaction ID ne suffit pas entre les connexions de ce client puisqu’il reste à 1. Champs Wireshark utiles : `tcp.stream`, `mbtcp.trans_id`, `mbtcp.prot_id`, `mbtcp.len`, `mbtcp.unit_id`.

### Exemple de requête FC06 construite par le code

```text
00 01 | 00 00 | 00 06 | 01 | 06 | 00 00 | 00 3C
 TID    Proto  Long.  Unit   FC  Adresse   Valeur
  1       0      6      1     6      0       60
```

La réponse normale contient ici les mêmes octets applicatifs. Cet exemple est **déduit du code**, pas extrait d’un PCAP utilisateur. Pour les structures de référence : [Modbus TCP/IP Implementation Guide](https://www.modbus.org/file/secure/messagingimplementationguide.pdf) et [spécification applicative, FC06](https://www.modbus.org/file/secure/modbusprotocolspecification.pdf).

### Tableau de relevé — observations et éléments à compléter

| Opération | Trames requête / réponse | Flux TCP / port client | Transaction / unité | Adresse / quantité ou valeur | Réponse observée |
| --- | --- | --- | --- | --- | --- |
| FC03 | À relever | À relever | À relever | À relever | À relever |
| FC04 | À relever | À relever | À relever | À relever | À relever |
| FC06 vers 6 °C | **34 / 36** | Port client **60894**, serveur **15020** ; flux non affiché | **1 / 1** | Holding **0**, **60 / 0x003C** | Écho FC06 sans exception ; délai **284 µs**. |
| FC06 vers 4 °C | **74 / 76** | Port client **60928**, serveur **15020** ; flux non affiché | **1 / 1** | Holding **0**, **40 / 0x0028** | Écho FC06 sans exception ; délai **486 µs**. |

## 4 — Interpréter la modification de consigne : réponses

1. **Code de fonction : FC06**, Write Single Register.
2. **Registre modifié : holding register à l’adresse PDU 0**, contenant la consigne. Ne pas le confondre avec l’input register 0 de température.
3. **Valeur transmise : 60**, soit **0x003C**, encodée sur deux octets `00 3C`.
4. **Pourquoi pas 6 ?** La convention du laboratoire exprime les températures en dixièmes de degré : 6,0 °C × 10 = 60. Cette échelle vient du mapping, pas d’une règle universelle de Modbus.
5. **Comment le client sait-il que l’écriture a été acceptée ?** Le serveur renvoie une réponse FC06 normale reprenant adresse et valeur. `Client.request()` vérifie notamment le MBAP, l’absence de code d’exception, la fonction et l’écho exact de la PDU ; le client affiche ensuite `write accepted`. Une lecture FC03 suivante à 60 confirme la valeur stockée. Cela ne signifie pas que l’enceinte est déjà à 6 °C.
6. **Peut-on identifier un utilisateur humain dans la requête ? Non.** Le message conventionnel ne contient pas son compte ni une preuve d’identité. L’IP, le port, l’unité et le Transaction ID décrivent l’échange, pas l’auteur humain. Des journaux de poste, de session ou de bastion seraient nécessaires pour étayer cette attribution ; aucune preuve de ce type n’est produite dans cet atelier.

## Captures utilisateur du 27 octobre — déroulement et preuves

Les heures des titres proviennent des noms des fichiers, pas des horodatages internes des paquets. Les dix originaux sont conservés dans `docs/assets/img/informatique-industrielle/it-1/`.

### 09:19:55 — Trafic local capturé avant décodage applicatif

![Trafic local capturé avant décodage applicatif](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2009-19-55.png)

La liste montre des connexions entre **127.0.0.1 et 127.0.0.1**, avec le serveur sur **15020** et plusieurs ports clients éphémères. SYN, ACK, données et fermeture sont visibles. Le protocole est encore affiché **TCP** : cette image atteste les échanges, mais pas leurs fonctions Modbus ni leurs valeurs.

### 09:22:30 — Trame 102 : réponse SYN/ACK du serveur

![Trame 102 : réponse SYN/ACK du serveur](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2009-22-30.png)

La trame **102** vient de **127.0.0.1:15020** vers **127.0.0.1:60964**. Le détail TCP indique **SYN/ACK**, **Len=0** et **Stream index 10**. C’est l’ouverture de la connexion, pas une réponse Modbus ni une acceptation d’écriture.

### 09:22:34 — Trame 101 : demande SYN du client

![Trame 101 : demande SYN du client](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2009-22-34.png)

La trame **101** vient de **127.0.0.1:60964** vers **127.0.0.1:15020**, avec **SYN**, **Len=0** et **Stream index 10**. Elle identifie le client de cette connexion. Ce port **60964** ne doit pas être confondu avec les ports des écritures FC06 analysées plus bas.

### 09:28:56 — Premier décodage : MBAP visible, sens à corriger

![Premier décodage : MBAP visible, sens à corriger](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2009-28-56.png)

Le détail affiche **Transaction ID 1**, **Protocol ID 0**, **Length 6**, **Unit ID 1** et **Read Coils (FC01)**. Mais **Byte Count 0** apparaît sur un contenu de requête : cet affichage initial est incohérent avec la structure attendue. Il ne faut pas en déduire qu’une lecture valide renvoie zéro octet ; la capture suivante met en évidence l’inversion du sens de décodage.

### 09:30:43 — Filtre de données et inversion requête/réponse

![Filtre de données et inversion requête/réponse](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2009-30-43.png)

Le filtre **`tcp.port == 15020 && tcp.len > 0`** isole les segments transportant des données. Les trames **104 et 106** sont initialement affichées comme Response puis Query, alors que **104 va du client 60964 vers le serveur 15020** et **106 dans le sens inverse**. Le marquage **Malformed Packet** de ce décodage n’établit pas, à lui seul, une trame réellement mal formée. L’association doit porter sur le port serveur **15020**, pas sur le port client éphémère.

### 09:32:12 — Décodage corrigé : deux écritures FC06 et leurs réponses

![Décodage corrigé : deux écritures FC06 et leurs réponses](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2009-32-12.png)

Le filtre **`modbus.func_code == 6`** affiche **34 Query / 36 Response**, puis **74 Query / 76 Response**, en **Write Single Register**. Transaction ID et Unit ID valent **1**. Cette vue atteste les deux paires applicatives, indépendamment des ACK TCP ; les quatre captures suivantes établissent les adresses et valeurs.

### 09:33:13 — Trame 34 : écriture de la consigne à 6 °C

![Trame 34 : écriture de la consigne à 6 °C](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2009-33-13.png)

Requête **127.0.0.1:60894 → 127.0.0.1:15020**, **FC06**, **Reference Number 0**, valeur **60**. Les octets sélectionnés sont **`00 3c`**, soit 0x003C. L’échelle du laboratoire donne **60 / 10 = 6 °C**. Le MBAP affiche transaction **1**, protocole **0**, longueur **6**, unité **1** ; TCP transporte **12 octets** applicatifs. Cette requête seule ne prouve pas encore l’acceptation.

### 09:33:27 — Trame 74 : restauration de la consigne à 4 °C

![Trame 74 : restauration de la consigne à 4 °C](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2009-33-27.png)

Requête **127.0.0.1:60928 → 127.0.0.1:15020**, **FC06**, registre **0**, valeur **40**, octets **`00 28`**. L’échelle donne **4 °C**. Le MBAP porte les mêmes valeurs **1 / 0 / 6 / 1**. Le changement de port client confirme que cette opération utilise une autre connexion TCP ; l’identifiant de transaction identique ne suffit pas à apparier les échanges entre connexions.

### 09:34:07 — Trame 36 : acceptation de l’écriture à 6 °C

![Trame 36 : acceptation de l’écriture à 6 °C](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2009-34-07.png)

Réponse **127.0.0.1:15020 → 127.0.0.1:60894**. Wireshark référence explicitement **Request Frame 34** et indique **284 microsecondes** depuis la requête. Le serveur reprend **FC06, registre 0, valeur 60**, avec **Exception: No**. L’écho attendu confirme l’acceptation technique de l’écriture ; il ne prouve ni une autorisation métier ni une température physique déjà à 6 °C.

### 09:34:14 — Trame 76 : acceptation du retour à 4 °C

![Trame 76 : acceptation du retour à 4 °C](../../assets/img/informatique-industrielle/it-1/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-27%2009-34-14.png)

Réponse **127.0.0.1:15020 → 127.0.0.1:60928**, liée à **Request Frame 74**, délai **486 microsecondes**. Le serveur reprend **FC06, registre 0, valeur 40**, sans exception. L’acceptation technique de la restauration est attestée. Ce délai est celui de la réponse applicative observée dans la capture, pas un délai de refroidissement de l’enceinte.

### Complément apporté par l’atelier 2.3

Les [huit captures de l’atelier 2.3](cartographier-variables-tester-modbus.md#captures-utilisateur-du-27-octobre-lectures-et-porte) documentent désormais une requête FC03 (adresse 0, quantité 3) et une requête FC04 (adresse 0, quantité 4), ainsi que des réponses FC03 en liste. Les valeurs des réponses restent à développer. La numérotation de cette autre session n’est pas celle des captures FC06 ci-dessus.

### Résultat établi et limites

> La capture montre deux écritures FC06 vers le holding register d’adresse 0 : valeur 60 pour demander 6 °C, puis valeur 40 pour restaurer 4 °C. Les réponses 36 et 76 reprennent la fonction, l’adresse et les valeurs des requêtes 34 et 74, sans exception. Les délais affichés sont respectivement 284 et 486 µs. Le contenu applicatif reste lisible dans Wireshark, sans champ d’identité humaine dans ces requêtes conventionnelles.

**À compléter :** détails des requêtes/réponses FC03 et FC04, lecture attestant la consigne initiale puis sa relecture, PCAP brut, empreinte et commande/interface de capture. Les adresses locales sont visibles ; la sélection de l’interface `lo` n’est pas photographiée. La restauration est confirmée par son écho FC06 ; une lecture FC03 de contrôle fournirait une preuve complémentaire de la valeur stockée.

La correction du décodage est attestée par le résultat final ; la fenêtre du réglage exact n’est pas capturée. Le marquage initial « malformed » ne doit pas être conservé comme constat de défaut du serveur après cette correction.

## Résultat attendu et preuves à conserver

- PCAP complet du laboratoire, nom de fichier, date, interface **lo**, filtre et empreinte SHA-256.
- Captures d’écran FC03, FC04 et FC06 avec requête/réponse et champs développés.
- Tableau rempli avec les vrais numéros de trames, ports clients et valeurs.
- Lecture avant/après montrant **40 → 60 → 40**, sans confondre consigne et température.
- Conclusion sur la visibilité des données et l’absence d’identité humaine native.

**État :** dix captures utilisateur intégrées ; requêtes/réponses FC06, MBAP, valeurs et acceptation établis. Détails FC03/FC04, relectures de consigne et PCAP brut restent à fournir. Les tests réseau locaux du J1 et les captures de son tableau de bord ne remplacent pas ce PCAP.

## Ressources

- [Wireshark — User’s Guide](https://www.wireshark.org/docs/wsug_html_chunked/).
- [Wireshark — Decode As](https://www.wireshark.org/docs/wsug_html_chunked/ChCustProtocolDissectionSection.html).
- [Champs Modbus/TCP](https://www.wireshark.org/docs/dfref/m/mbtcp.html) et [Modbus](https://www.wireshark.org/docs/dfref/m/modbus.html).
- `docs/REGISTER_MAP.md`, `docs/EXERCISES.md`, `lab/modbus.py` et `lab/client.py` du laboratoire.

Sources Wireshark consultées le **27 octobre 2026**. Les valeurs fixes et longueurs présentées sont vérifiées dans l’implémentation Python fournie.

[Retour à l’itération 1](index.md) · [Atelier 2.1 — Principes de Modbus TCP](decouvrir-communications-modbus-tcp.md)
