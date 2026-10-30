# 5.4 — Atelier 4 | Reproduire l’incident sur le jumeau numérique

## 🎯 Objectif et modalités

Utiliser le modèle frigorifique pour observer les conséquences d’une modification non autorisée et expérimenter des mesures correctives.

**Modalité :** TP accompagné en binôme. **Durée :** à compléter, non précisée. **Environnement :** PoC Python/Modbus, supervision et protections J4, sur la VM Debian **192.168.122.105**.

!!! info "Procédure et preuves partielles reçues le 30 octobre 2026"
    La nouvelle capture du TP contient **2 630 trames sur environ 21 minutes**. Elle confirme l’écriture de **12 °C**, une hausse jusqu’à **12,1 °C**, une alarme, l’écriture corrective à **4 °C**, puis une baisse à **3,8 °C** et l’alarme inactive. Les lots antérieurs sont conservés séparément. Les **24 captures** ajoutées documentent aussi les tests IT/proxy et l’API du **premier essai**, distincts du PCAP long. Une API après restauration du second essai n’est pas montrée ; aucune validation réelle de denrées ou d’installation n’en est déduite.

## 1 — Préparer l’environnement et les preuves

Le PoC ne simule qu’une seule zone ; elle représente ici **ZF-02 simplifiée**. Ses adresses `10.77.*` et ses ports ne sont pas les adresses `10.30.*:502` du PCAP d’incident. Les actions du TP sont autorisées pédagogiquement ; leur effet permet d’étudier une modification qui n’était pas justifiée dans le scénario, sans transformer cet essai en attribution d’attaque réelle.

### Vérifier le montage réellement présent

Sur la VM, commencer par :

```bash
cd ~/ais-it-ot-j4/poc
sudo ip netns list
sudo ip -n ais45-fw -br addr
sudo ip -n ais45-fw -br link show fw-dmz
sudo ip netns exec ais45-fw nft list table inet ais45
sudo ip netns exec ais45-ot ss -lnt
sudo ip netns exec ais45-gw ss -lnt
```

Attendus : namespaces **ais45-it / ais45-fw / ais45-gw / ais45-ot**, lien `fw-dmz` UP, serveur **10.77.30.2:15020**, proxy **10.77.20.2:15021**, dashboard **10.77.20.2:18080**, table `inet ais45` et refus par défaut.

Si le montage est absent, conserver d’abord les preuves J4 et reprendre la [procédure de démarrage 4.5](../it-3/mettre-en-oeuvre-filtrage-it-ot.md), selon les consignes du formateur. Ne pas lancer `all` sur un environnement déjà préparé ni redémarrer le modèle pour masquer un écart. Si seul `fw-dmz` est resté coupé et que la reprise est prévue : `sudo ip -n ais45-fw link set fw-dmz up`.

La version actuelle de `docs/NETWORK.md` dans le laboratoire décrit aussi un **montage Docker avec réseaux 172.30.81/82/83**. Les commandes de cette fiche concernent les **namespaces J4** ; vérifier la topologie retenue avant emploi et adapter si le formateur choisit Docker. Le client `python3 -m lab.client setpoint 12` sans options viserait `127.0.0.1:15020` dans le namespace courant, pas automatiquement le serveur séparé.

### Conserver un état initial et un suivi daté

Les preuves de ce TP doivent être séparées des exports J4 et du PCAP synthétique du 8 octobre. Dans le terminal de suivi, sur la VM :

```bash
cd ~/ais-it-ot-j4/poc
J5_PREUVES="$HOME/ais-it-ot-j4/evidence/j5-54-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$J5_PREUVES"
printf '%s\n' "$J5_PREUVES"
date -Is | tee "$J5_PREUVES/debut.txt"
sudo ip netns exec ais45-fw nft -a list ruleset > "$J5_PREUVES/regles-avant.nft"
sudo ip netns exec ais45-it python3 -m lab.client status --host 10.77.20.2 --port 15021 | tee "$J5_PREUVES/etat-initial.txt"
```

Vérifier **consigne 4 °C, porte fermée, défaut absent, auto actif**. Noter la température et le compresseur tels qu’ils sont ; ne pas inventer un état initial à 5 °C. En cas d’écart, l’expliquer puis faire valider sa correction ciblée avant de commencer. Ne pas comparer des températures à la même seconde : les requêtes successives ne sont pas une lecture atomique.

Collecte de supervision depuis IT, à effectuer avant et après les actions :

```bash
sudo ip netns exec ais45-it python3 - <<'PY'
import urllib.request
with urllib.request.urlopen('http://10.77.20.2:18080/api', timeout=4) as r:
    print(r.status)
    print(r.read().decode())
PY
```

Attendu : **HTTP 200** avec température, consigne, compresseur, porte et alarme. Une capture du JSON atteste la collecte, pas l’affichage d’un navigateur.

## 2 — Reproduire la modification de consigne

Le montage J4 n’a **pas de poste de maintenance dédié ni de bastion déployé**. La règle autorise **GW 10.77.20.2 → OT 10.77.30.2:15020**. Un client exécuté dans `ais45-gw` peut utiliser ce chemin direct pour le TP accompagné. Il ne passe pas par le proxy lecteur, sans modification des règles. Ce chemin ne démontre ni une identité de mainteneur ni une séparation de rôles industrielle.

Dans un deuxième terminal sur la VM :

```bash
cd ~/ais-it-ot-j4/poc
date -Is
sudo ip netns exec ais45-gw python3 -m lab.client setpoint 12 --host 10.77.30.2 --port 15020
sudo ip netns exec ais45-it python3 -m lab.client status --host 10.77.20.2 --port 15021
```

Attendu à vérifier : **write accepted**, puis consigne **12 °C** à la relecture. La commande envoie **FC06, PDU 0, valeur 120**. Le code accepte 0 à 500 pour ce registre ; le Holding Register 1 qui contient `80` est une limite **recommandée**, pas un contrôle bloquant l’écriture à 12 °C. Une acceptation technique ne vaut pas autorisation métier.

### Suivre les effets progressifs

Dans le premier terminal, qui conserve `J5_PREUVES`, lancer le suivi pendant les manipulations :

```bash
while true; do
    date -Is
    sudo ip netns exec ais45-it python3 -m lab.client status --host 10.77.20.2 --port 15021 2>&1
    sleep 15
done | tee "$J5_PREUVES/suivi-etats.txt"
```

Arrêter la boucle par **Ctrl+C** après les observations de restauration. Elle n’arrête ni le modèle ni les autres services. Une erreur de lecture doit être conservée et analysée, pas interprétée comme une température normale.

| Variable | Comportement attendu d’après le code, pas résultat observé |
| --- | --- |
| Consigne | Change après écriture, sans attendre la réponse thermique. |
| Compresseur | À consigne 12 °C : arrêt si température ≤ 11,5 °C, démarrage si température ≥ 12,5 °C, maintien entre les deux ; mise à jour au cycle du modèle. |
| Température | Évolue progressivement ; elle ne passe pas immédiatement à 12 °C. Plusieurs minutes peuvent être nécessaires avant d’atteindre le seuil d’alarme. |
| Alarme | Active après température **strictement > 8 °C pendant 10 secondes** dans le PoC ; le dossier Montval utilise **10 minutes**. |
| Supervision | Relit les données via le proxy ; disponibilité et valeurs à vérifier à plusieurs instants. |

Noter les heures d’écriture, de changement du compresseur, du premier relevé > 8 °C et de l’alarme. Un échantillonnage toutes les 15 secondes ne donne pas l’instant exact du franchissement. Si le TP est interrompu avant l’alarme, noter **non observée pendant la durée de l’essai**. Garder la porte fermée ; ne pas injecter de défaut ni modifier le code pour obtenir plus vite le résultat attendu. Convenir de la durée avec le formateur.

## 3 — Vérifier les protections

### A — IT direct : refus réseau

Dans le deuxième terminal :

```bash
sudo ip netns exec ais45-gw python3 -m lab.client status --host 10.77.30.2 --port 15020
sudo ip netns exec ais45-fw nft list counter inet ais45 it_direct_drop
sudo ip netns exec ais45-it python3 -m lab.client status --host 10.77.30.2 --port 15020
sudo ip netns exec ais45-fw nft list counter inet ais45 it_direct_drop
```

Attendu : OT disponible depuis GW, timeout direct depuis IT et hausse du compteur de refus. Ce rapprochement distingue le refus d’un service arrêté ou d’un routage défaillant. Les compteurs sont cumulés : garder les valeurs avant/après sans les remettre à zéro.

### B — Consultation et refus d’écriture via la passerelle

```bash
sudo ip netns exec ais45-it python3 -m lab.client status --host 10.77.20.2 --port 15021
sudo ip netns exec ais45-it python3 -m lab.client setpoint 6 --host 10.77.20.2 --port 15021
sudo ip netns exec ais45-it python3 -m lab.client status --host 10.77.20.2 --port 15021
```

Attendus : lecture réussie, **exception Modbus code 1**, consigne encore **12 °C**. La connexion TCP est permise ; le refus vient du proxy. Si l’écriture est acceptée au lieu d’être refusée, garder l’écart, interrompre le scénario et rétablir 4 °C par le chemin ci-dessous ; ne pas déclarer le proxy conforme.

### C — Chemin d’écriture pédagogique

La première écriture depuis GW, puis la correction depuis GW, vérifient ce chemin. **Ne pas ouvrir IT → OT** pour obtenir une écriture. La règle autorise une origine réseau GW, pas une personne ni une fonction Modbus : un processus ou poste autorisé peut encore envoyer une consigne inadaptée. Cela illustre une limite, sans prouver une compromission de GW ou de MAINT-01.

### Capture facultative, à lancer avant les écritures

Dans un terminal dédié, `fw-ot` voit les échanges GW → serveur :

```bash
sudo ip netns exec ais45-fw tcpdump -i fw-ot -nn -s 0 -U   -w /home/oliv/ais-it-ot-j4/evidence/j5-54-modbus-$(date -u +%Y%m%dT%H%M%SZ).pcap   'tcp port 15020'
```

Arrêter par Ctrl+C après restauration. Ce point montre les lectures relayées et les écritures directes autorisées ; une tentative IT bloquée avant sortie peut ne pas apparaître sur `fw-ot`. Compléter par les compteurs ou une capture côté `fw-it` pour le refus direct.

Dans Wireshark, associer TCP15020 à Modbus/TCP si nécessaire, puis filtrer `modbus.func_code == 6`. Distinguer ce PCAP réel du TP du PCAP **synthétique sur TCP502** du dossier. Le proxy réémet les requêtes : son adresse aval n’est pas une identité humaine.

## 4 — Restaurer le fonctionnement

Avant de terminer, dans le deuxième terminal :

```bash
date -Is
sudo ip netns exec ais45-gw python3 -m lab.client setpoint 4 --host 10.77.30.2 --port 15020
sudo ip netns exec ais45-it python3 -m lab.client status --host 10.77.20.2 --port 15021
```

Attendu : écriture acceptée, consigne **4 °C** relue. Si température ≥ 4,5 °C, le modèle doit commander le compresseur au cycle suivant ; dans la bande 3,5–4,5 °C, il peut conserver son état. Continuer les mesures et l’API : la baisse est progressive. **Ne pas redémarrer le serveur pour retrouver artificiellement l’état initial.**

Dans le terminal de suivi, après Ctrl+C :

```bash
date -Is | tee "$J5_PREUVES/fin.txt"
sudo ip netns exec ais45-it python3 -m lab.client status --host 10.77.20.2 --port 15021 | tee "$J5_PREUVES/etat-final.txt"
sudo ip netns exec ais45-fw nft -a list ruleset > "$J5_PREUVES/regles-apres.nft"
```

Rejouer la collecte HTTP et les consultations nécessaires. Attendus finaux : **consigne 4 °C, porte 0, défaut 0, auto 1**, lien et règles présents, lectures et API disponibles. Noter température, alarme et tendance ; une température encore élevée doit rester visible dans le compte rendu. Restaurer la consigne ne prouve pas le retour immédiat du régime thermique nominal.

Conserver le laboratoire et les preuves pour la suite. Aucun retour au service réel ni décision sur des denrées n’est déduit de ce modèle sans produits.

## Premier lot reçu — état final et ancienne capture vide

[Archive des quatre fichiers](../../assets/files/informatique-industrielle/it-4/Montval-5.4-preuves-utilisateur.zip) · [Inventaire et SHA-256](../../assets/files/informatique-industrielle/it-4/Montval-5.4-inventaire-preuves.json).

Les relevés et le nouveau PCAP sont conservés au niveau `livrables/informatique-industrielle/it-4/`, séparément du sous-dossier `Incident_dossier` fictif. L’ancien PCAP vide, remplacé dans le dossier de travail, reste conservé dans l’archive du premier lot avec son inventaire ; le nouveau fichier a une archive et une empreinte distinctes.

| Fichier reçu | Observation vérifiée | Portée et limite |
| --- | --- | --- |
| [fin.txt](../../assets/files/informatique-industrielle/it-4/Montval-5.4-fin.txt) | **2026-10-30T10:26:43+01:00**. | Repère de fin exporté ; `etat-final.txt` ne porte pas d’horodatage interne. Ne pas lui attribuer une heure indépendante non enregistrée. |
| [etat-final.txt](../../assets/files/informatique-industrielle/it-4/Montval-5.4-etat-final.txt) | **Température 4,4 °C, consigne 4 °C, compresseur 1, alarme 0, porte 0, défaut 0, auto 1.** | État final compatible avec maintien du froid et hystérésis ; ne prouve pas à lui seul l’écriture précédente à 12 °C, le retour thermique complet ni la collecte HTTP. |
| [regles-apres.nft](../../assets/files/informatique-industrielle/it-4/Montval-5.4-regles-apres.nft) | Table `inet ais45`, chaîne `forward` policy DROP, refus IT/OT direct, autorisations ciblées GW et retours établis. | Configuration exportée présente ; placement `ais45-fw` selon la commande utilisateur fournie. Pas de mesure avant/après de chaque test dans ce lot. |
| j5-54-modbus-20261030T091746Z.pcap | **24 octets, en-tête PCAP classique uniquement, zéro paquet.** | Capture inexploitable pour confirmer les écritures, réponses, lectures ou refus. Sa vacuité ne prouve pas une absence de communication. |

Compteurs de l’export reçu : `it_direct_drop` **12 paquets / 720 octets** ; `it_gateway_accept` **546 / 30434** ; `gateway_ot_accept` **624 / 34528** ; `replies_accept` **784 / 45458** ; `other_drop` **0 / 0**. Ils sont cumulatifs et ne permettent pas d’attribuer douze paquets à douze essais ou à une tentative particulière. Sans export initial correspondant, aucune hausse de compteur propre à 5.4 n’est calculée.

Le message terminal précédemment transmis dans la conversation montrait **6,2 °C, consigne 4 °C et compresseur 1** à proximité de 10:19:50. Il est compatible avec une baisse vers le relevé final de 4,4 °C, mais les fichiers de suivi continu et le relevé initial ne sont pas fournis. Le considérer comme un **relevé communiqué par l’utilisateur**, pas comme une courbe enregistrée ni une preuve de toute la séquence.

### Difficulté d’export rencontrée

L’utilisateur a signalé un dossier absent puis un dossier de preuves **root:root en 755** et un fichier **root:root en 660**. Le `sudo` placé devant `nft` n’élève pas les droits de la redirection `>` exécutée par le shell. Un fichier 660 reste inaccessible en écriture à `oliv` s’il n’en est ni propriétaire ni membre du groupe autorisé ; créer un nouveau fichier exige également l’écriture sur le dossier.

Pour les prochains relevés, créer `J5_PREUVES` avec le compte `oliv`, puis vérifier existence et droits **avant** les manipulations :

```bash
printf '%s\n' "$J5_PREUVES"
ls -ld "$J5_PREUVES"
test -d "$J5_PREUVES" && test -w "$J5_PREUVES"
```

Si le test échoue, régler le dossier ciblé avant de poursuivre ; ne pas utiliser `chmod 777`. Les exports refaits après correction reflètent de nouveaux instants, pas une récupération de traces perdues. Les erreurs précédentes n’invalident pas automatiquement les actions du modèle, mais expliquent les lacunes du lot de preuves.

### Compléter une capture, sans rejouer l’incident pour la seule image

Une capture vide peut provenir de sa période, du point choisi, du filtre, d’un arrêt trop tôt ou d’un autre problème ; **la cause n’est pas établie ici**. Pour éprouver la collecte, lancer une nouvelle capture sur `fw-ot`, puis effectuer une **lecture** depuis GW dans un second terminal et arrêter la capture proprement. Une lecture suffit à vérifier ce point de capture sans réécrire 12 °C.

```bash
# Terminal capture, sur la VM : fw-ot vers serveur OT.
sudo ip netns exec ais45-fw tcpdump -i fw-ot -nn -s 0 -U \
  -w /home/oliv/ais-it-ot-j4/evidence/j5-54-controle-lecture.pcap \
  'tcp port 15020'
```

```bash
# Deuxième terminal, sur la VM.
cd ~/ais-it-ot-j4/poc
sudo ip netns exec ais45-gw python3 -m lab.client status --host 10.77.30.2 --port 15020
```

Après Ctrl+C dans tcpdump, contrôler son bilan et ouvrir le nouveau fichier. Vérifier que ce nom n’existe pas déjà avant la capture, ou choisir un nom daté pour conserver les preuves précédentes. Si le relevé reste vide malgré une lecture réussie, examiner interfaces et chemin réel ; ne pas en déduire un refus réseau. Une nouvelle lecture ne reconstitue pas les écritures manquantes. Une éventuelle reproduction complète reste un essai distinct à convenir avec le formateur.

## Deuxième capture — 130 trames, contrôle antérieur à la reproduction complète

[PCAP complété](../../assets/files/informatique-industrielle/it-4/Montval-5.4-capture-completee.pcap) · [Décodage CSV](../../assets/files/informatique-industrielle/it-4/Montval-5.4-pcap-decode.csv) · [Analyse JSON et empreinte](../../assets/files/informatique-industrielle/it-4/Montval-5.4-analyse-pcap.json) · [Archive actualisée, ancien lot conservé séparément](../../assets/files/informatique-industrielle/it-4/Montval-5.4-preuves-completees.zip).

Le fichier `j5-54-modbus-20261030T093221Z.pcap` contient **11 228 octets, 130 trames et 26 messages Modbus**, soit **13 paires requête/réponse**. Fenêtre vérifiée : **30 octobre 2026, 10:32:53,905886–10:33:17,086498, heure de Paris**. Il est postérieur au relevé de fin de 10:26:43 et ne doit pas être fusionné avec lui comme un instant unique.

Toutes les transactions observées relient **10.77.20.2** à **10.77.30.2:15020**, sur le chemin aval GW/OT. Quatre séries FC03/FC04/FC01 sont présentes, plus une FC06. L’analyse vérifie les adresses/ports, transaction et unité pour apparier chaque réponse ; les quantités retournées correspondent aux demandes, contrairement aux FC03 synthétiques de l’incident.

| Trames | Heure locale / opération | Valeur observée |
| --- | --- | --- |
| **4/6, 14/16, 24/26** | 10:32:53 ; FC03, FC04 puis FC01 | Consigne **4 °C**, limite recommandée 8 °C, auto 1 ; température **3,8 °C**, compresseur 1, alarme/défaut 0 ; porte et défaut injecté 0. |
| **34/36, 44/46, 54/56** | 10:33:04,56 ; même série de lectures | Consigne **4 °C**, température **3,5 °C**, compresseur 1, alarme/défaut/porte 0, auto 1. |
| **64/66, 74/76, 84/86** | 10:33:04,63 ; nouvelle série de lectures | Mêmes valeurs encodées que la série précédente ; ce sont des lectures distinctes. |
| **94/96** | **10:33:17,050884 / 10:33:17,051207** ; FC06 | Client **10.77.20.2:39000 → 10.77.30.2:15020**, PDU **0**, valeur **40** (`0x0028`) = **4 °C**. Réponse normale qui répète adresse et valeur, après **323 µs**. |
| **104/106, 114/116, 124/126** | 10:33:17,08 ; lectures après l’écriture | Consigne **4 °C**, température **3,7 °C**, compresseur **0**, alarme/défaut/porte 0, auto 1. |

Unité **1**, identifiant de transaction **1** pour ces échanges : le client ouvre une nouvelle connexion à chaque opération. La transaction seule ne constitue donc pas une clé unique ; utiliser aussi les extrémités et le flux TCP.

**Ce qui est établi :** la capture fonctionne, les lectures GW/OT répondent, l’écriture de 4 °C est acceptée et la consigne est relue à 4 °C. **Ce qui n’est pas établi :** la capture commence avec une consigne déjà à 4 °C ; la FC06 est donc une **réécriture à 4 °C**, pas la preuve d’un passage de 12 à 4 °C dans cette fenêtre. Aucun 12 °C, aucune alarme haute ni exception d’écriture par le proxy n’est présent. Le point aval ne permet pas d’identifier à lui seul l’origine d’une lecture en amont du proxy ou une tentative IT bloquée.

La séquence compresseur 1 à 3,8/3,5 °C puis 0 à 3,7 °C est compatible avec le cycle d’hystérésis et les valeurs arrondies. Elle ne doit pas être attribuée à un changement de consigne qui n’a pas lieu dans cette fenêtre. Les températures ne décroissent pas sur toute la capture : ne pas transformer ce contrôle en preuve d’un refroidissement continu depuis 12 °C.

### Trames à ouvrir dans Wireshark

Décoder TCP **15020** comme Modbus/TCP si nécessaire, puis :

```wireshark
frame.number in {94,96,104,106,114,116}
```

Les **94/96** montrent FC06, PDU 0, valeur 40 et la réponse ; **104/106** confirment la relecture de consigne ; **114/116** montrent la température et la commande après écriture. Filtre de toutes les écritures : `modbus.func_code == 6`. Cette capture n’a pas les numéros de trame ni les adresses du dossier synthétique de 5.2.

SHA-256 :

```text
5554ee3dbe0a6abc6d3658249e07c75e5c144f987bbfef446145701bdff44aeb
```

Pour reproduire le décodage de cette ancienne fenêtre, utiliser le script avec le chemin du [PCAP de 130 trames archivé](../../assets/files/informatique-industrielle/it-4/Montval-5.4-capture-completee.pcap) et un préfixe de sortie distinct. Sans argument, le script analyse désormais la dernière capture complète. Aucun paquet n’est envoyé.

## Reproduction complète — 2 630 trames, montée et restauration observées

[PCAP complet](../../assets/files/informatique-industrielle/it-4/Montval-5.4-reproduction-complete.pcap) · [Décodage CSV](../../assets/files/informatique-industrielle/it-4/Montval-5.4-reproduction-complete-decode.csv) · [Analyse JSON](../../assets/files/informatique-industrielle/it-4/Montval-5.4-reproduction-complete-analyse.json) · [Archive de ce nouvel essai](../../assets/files/informatique-industrielle/it-4/Montval-5.4-reproduction-complete.zip).

Le nouveau fichier `j5-54-controle-lecture.pcap`, malgré son nom de contrôle de lecture, contient aussi les **deux écritures pédagogiques**. Il remplace le PCAP de travail précédent ; les archives publiques des deux lots antérieurs sont conservées. Les fichiers `fin.txt`, `etat-final.txt` et `regles-apres.nft` du lot précédent restent des relevés antérieurs, pas les exports de fin de ce nouvel essai.

**Fenêtre : 30 octobre 2026, 10:39:16,144633–11:00:08,887138, heure de Paris.** Taille **226 726 octets**, **2 630 trames**, **526 messages Modbus**, **263 transactions** : 87 lectures FC03, 87 FC04, 87 FC01 et 2 écritures FC06, avec leurs réponses. Les messages complets ont été décodés et appariés par extrémités TCP, transaction et unité. Les quantités des lectures correspondent aux réponses.

![Montée de température, alarme et correction sur le PoC](../../assets/files/informatique-industrielle/it-4/Montval-5.4-reproduction-complete-evolution.svg)

| Heure locale / trames utiles | Observation décodée | Conclusion permise |
| --- | --- | --- |
| **10:39:16** ; réponses **6, 16, 26** | Consigne **4 °C**, température **3,8 °C**, compresseur 0, alarme/défaut/porte 0, auto 1. | État initial de cette capture documenté. |
| **10:40:48,959751 / ,960118** ; **274/276** | FC06 PDU **0**, valeur **120** depuis **10.77.20.2:44246 → 10.77.30.2:15020** ; réponse normale avec même adresse/valeur après **367 µs**. | Écriture de **12 °C acceptée** par le serveur. |
| **10:40:48,994727** ; réponse **286** | FC03 : `[120, 80, 1]`. | Consigne **12 °C relue**, limite recommandée 8 °C non bloquante, mode automatique actif. |
| **10:40:54,189158** ; réponse **326** | Température **3,6 °C**, compresseur **0**, alarme 0. | Commande arrêtée après la modification ; température encore basse. Le relevé 296 juste après l’écriture montrait encore compresseur 1 : ne pas confondre réponse d’écriture et cycle instantané de régulation. |
| **10:47:41,308514** ; réponse **1136** | Température **8,2 °C**, compresseur 0, **alarme 1**. | Alarme haute observée. Premier relevé > 8 °C et première alarme active vus dans cette capture ; l’instant précis du seuil et les 10 secondes ne sont pas résolus par les lectures espacées. |
| **10:55:27,542210** ; réponse **2066** | Température **12,0 °C**, compresseur 0, alarme 1 ; consigne précédente toujours 12 °C. | Température mesurée simulée atteignant 12 °C, pas seulement consigne. |
| **10:55:34,989945 / ,990155** ; **2084/2086** | FC06 PDU **0**, valeur **40** depuis **10.77.20.2:38798** ; réponse normale après **210 µs**. | Écriture corrective à **4 °C acceptée**. |
| **10:55:35,033664** ; réponse **2096** | FC03 : `[40, 80, 1]`. | Consigne **4 °C relue** après la correction. |
| **10:55:35,034422** ; réponse **2106** | Température **12,1 °C**, compresseur **1**, alarme **1**. | Maximum enregistré et commande de refroidissement active ; la température n’est pas revenue à 4 °C avec le seul paramètre. |
| **10:57:53,526940** ; réponse **2346** | Température **7,7 °C**, compresseur 1, **alarme 0**. | Baisse et première alarme inactive observées après correction. |
| **11:00:08** ; réponses **2606, 2616, 2626** | Consigne **4 °C**, température **3,8 °C**, compresseur **1**, alarme/défaut/porte 0, auto 1. | Retour thermique près de la consigne et états nominaux observés. Le compresseur peut rester actif dans la bande d’hystérésis ; son arrêt bas et un cycle complet après restauration ne sont pas montrés. |

La consigne à 12 °C est conservée environ **14 min 46 s** entre les deux écritures ; le PCAP couvre ensuite environ **4 min 34 s** de suivi après correction. La baisse des lectures est progressive, de 12,1 °C à 3,8 °C. Les mesures représentent le modèle, pas les denrées ni les durées du dossier Montval réel supposé.

**Limites de la preuve :** capture aval **GW 10.77.20.2 ↔ OT 10.77.30.2:15020**. Elle n’identifie pas la personne, ne démontre pas le chemin amont de chaque lecture, l’API HTTP, une tentative IT directe bloquée ou un refus d’écriture par le proxy. Elle ne remplace donc pas les tests positifs/négatifs J4 et les vérifications spécifiques qui restent à documenter en J5. Aucun redémarrage du serveur n’est montré ; la capture seule ne certifie pas l’absence de toute action extérieure à sa visibilité.

### Sélection pour Wireshark

```wireshark
frame.number in {274,276,286,1136,2066,2084,2086,2096,2106,2346,2616}
```

Pour les quatre paquets d’écriture : `modbus.func_code == 6`. Vérifier le décodage TCP **15020**. Les numéros sont propres à ce PCAP de **2 630 trames**, et différents des captures de 130 trames ou du dossier fictif de 18 trames.

SHA-256 :

```text
f68acc9508c0f5a7f7c3761db6d2f786f87859fd7abbb154de90354ea96b1a8c
```

Reproduction hors ligne de l’analyse :

```bash
python3 livrables/informatique-industrielle/it-4/analyser_capture_poc_54.py
```

Les CSV, JSON et figure de cette fenêtre sont régénérés depuis le fichier reçu ; le script n’envoie aucune requête au modèle. Les lectures initiales/finales et les écritures constituent des preuves de TP réellement capturées, distinctes des sources synthétiques de l’incident.

## Captures utilisateur — 24 preuves visuelles complémentaires

Les **24 nouvelles captures** sont conservées dans `assets/img/informatique-industrielle/it-5/` selon le classement utilisateur par journée ; elles relèvent ici de **J5 / itération 4**. Les huit captures précédentes de la fiche 5.2 restent dans leur analyse du dossier fictif. Toutes les nouvelles images ont été examinées et intégrées ; elles couvrent des contrôles et instants différents.

### Premier essai : préparation et tests réseau de 10:14 à 10:20

Les douze captures suivantes ne sont pas des vues du PCAP long de 10:39–11:00. Elles documentent la préparation et un premier essai, avec les erreurs de sauvegarde qui expliquent l’absence de certains exports.

#### 10:14:20 — Recréation du laboratoire et contrôles automatiques

![Recréation du laboratoire et contrôles automatiques](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2010-14-20.png)

La commande `lab-it-ot.sh all` recrée le montage après disparition des namespaces. Le run **20261030T091401Z** affiche lectures, refus FC05/FC06, refus direct, relecture, HTTP et compteurs **OK**, puis comparaison du ruleset hôte inchangé. Cela documente un **nouveau démarrage**, distinct du J4 et de la capture longue suivante ; le modèle a donc un nouvel état initial. Les avertissements iptables-nft accompagnent les exports hôte, pas un échec du filtrage namespace.

#### 10:14:29 — Présence des quatre namespaces

![Présence des quatre namespaces](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2010-14-29.png)

La liste contient **ais45-ot, ais45-gw, ais45-fw, ais45-it**. Les interfaces du pare-feu portent **10.77.10.1/24, 10.77.20.1/24 et 10.77.30.1/24**, toutes UP.

#### 10:14:49 — Adresses et état du lien fw-dmz

![Adresses et état du lien fw-dmz](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2010-14-49.png)

Le relevé détaillé confirme **fw-dmz UP/LOWER_UP**, avec l’adressage attendu. Ce contrôle précède les manipulations, sans prouver à lui seul le fonctionnement de tous les services.

#### 10:15:15 — Table nftables réellement présente

![Table nftables réellement présente](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2010-15-15.png)

La table **inet ais45**, chaîne **forward policy drop**, et les règles ciblées sont visibles. Compteur direct **3 paquets / 180 octets**, autorisations et retours non nuls, `other_drop` à 0. Ce relevé servira de valeur avant la tentative manuelle de 10:17.

#### 10:15:37 — Services en écoute

![Services en écoute](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2010-15-37.png)

Dans OT : **10.77.30.2:15020** ; dans GW : **10.77.20.2:15021** et **:18080**. Les services sont exposés sur les adresses du montage, pas une preuve d’écoute accessible depuis toutes les zones.

#### 10:16:04 — Échec de création des preuves, état initial néanmoins affiché

![Échec de création des preuves, état initial néanmoins affiché](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2010-16-04.png)

Le `mkdir` échoue pour droits insuffisants, puis les exports échouent car le dossier n’existe pas. La commande de lecture affiche néanmoins **température 4,3 °C, consigne 4 °C, compresseur 0, alarme/porte/défaut 0, auto 1**. La capture conserve ce résultat terminal ; elle ne prouve pas l’existence des fichiers qui n’ont pas été écrits. La date visible est **10:15:56+01:00**.

#### 10:16:21 — Collecte de supervision HTTP réussie

![Collecte de supervision HTTP réussie](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2010-16-21.png)

La requête depuis **ais45-it** vers **10.77.20.2:18080/api** retourne **200**, température **4,4 °C**, consigne **4 °C**, compresseur `false`, alarme et porte `false`. Cela atteste l’API avant le premier essai ; aucune réponse HTTP après le second essai long n’est fournie.

#### 10:16:36 — Première écriture pédagogique à 12 °C

![Première écriture pédagogique à 12 °C](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2010-16-36.png)

Le terminal est daté **10:16:28+01:00**. `setpoint 12` depuis GW vers le serveur direct renvoie **write accepted** ; la lecture depuis IT par le proxy indique **consigne 12 °C**, température **4,1 °C**, compresseur 1. Ce relevé immédiatement après écriture ne prouve pas le changement instantané de commande au cycle du modèle. Il appartient au premier essai, pas à l’écriture de 10:40 du nouveau PCAP.

#### 10:17:17 — Refus IT direct et compteur avant/après

![Refus IT direct et compteur avant/après](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2010-17-17.png)

Le serveur répond d’abord depuis GW : **4,6 °C, consigne 12 °C, compresseur 0**. La tentative **ais45-it → 10.77.30.2:15020** expire ; `it_direct_drop` passe de **3 paquets / 180 octets** à **6 paquets / 360 octets**. La disponibilité du chemin autorisé et le delta constituent une preuve rapprochée du filtrage, distincte des compteurs cumulés exportés plus tard.

#### 10:17:32 — Consultation par proxy et refus d’écriture

![Consultation par proxy et refus d’écriture](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2010-17-32.png)

Avant et après tentative de `setpoint 6` via **10.77.20.2:15021**, la lecture indique **4,8 °C et consigne 12 °C**, porte/défaut/alarme 0, auto 1. L’écriture reçoit **Modbus exception code 1**. Le proxy laisse consulter mais refuse l’écriture ; la consigne reste à 12 °C. Ce test applicatif est désormais prouvé par cette capture.

#### 10:19:59 — Retour à 4 °C visible malgré échec des exports

![Retour à 4 °C visible malgré échec des exports](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2010-19-59.png)

Le relevé daté **10:19:50+01:00** affiche **6,2 °C, consigne 4 °C, compresseur 1**, alarme/porte/défaut 0, auto 1. Les écritures de fichiers échouent encore : la capture atteste le résultat terminal et les erreurs, pas les exports manquants. L’écriture corrective elle-même n’est pas affichée dans cette image.

#### 10:20:06 — Bilan tcpdump d’une autre collecte

![Bilan tcpdump d’une autre collecte](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2010-20-06.png)

Le terminal affiche **250 packets captured, 250 packets received by filter, 0 packets dropped by kernel** après arrêt. Il ne montre pas le nom développé du fichier daté, et aucun PCAP reçu de 250 trames n’a été identifié. Ne pas assimiler ce bilan au premier fichier vide, au contrôle de 130 trames ou à la capture longue de 2 630 trames sans pièce correspondante.

### Second essai : détails Wireshark de la capture longue

Les douze vues suivantes ont été réalisées vers **11:05–11:06**, après le TP. Leur heure de capture d’écran n’est pas l’heure de l’événement : les paquets appartiennent à la fenêtre **10:39:16–11:00:08** du PCAP long. Le décodage Modbus est ici détaillé, avec valeurs des registres et associations requête/réponse visibles ; l’avertissement de classification du PCAP synthétique analysé en 5.2 n’apparaît pas dans ces vues.

#### 11:05:19 — Trame 274 — demande de consigne 12 °C

![Trame 274 — demande de consigne 12 °C](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2011-05-19.png)

FC06 de **10.77.20.2:44246 → 10.77.30.2:15020**, PDU **0**, valeur **120**, transaction 1, unité 1, longueur MBAP 6. Les octets `00 78` confirment 120 en dixièmes de degré.

#### 11:05:25 — Trame 276 — réponse normale à l’écriture

![Trame 276 — réponse normale à l’écriture](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2011-05-25.png)

La réponse référence explicitement la **requête 274**, affiche **367 µs**, FC06, adresse 0 et valeur 120, sans exception. Elle confirme l’acceptation Modbus, au-delà d’un simple ACK TCP.

#### 11:05:31 — Trame 286 — relecture de la consigne

![Trame 286 — relecture de la consigne](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2011-05-31.png)

FC03, six octets de données, registres **0 = 120, 1 = 80, 2 = 1** : consigne 12 °C, limite recommandée 8 °C non imposée, mode automatique actif.

#### 11:05:37 — Trame 1136 — température haute et alarme

![Trame 1136 — température haute et alarme](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2011-05-37.png)

FC04, registres **[82, 0, 1, 0]** : **8,2 °C**, compresseur 0, alarme 1, défaut capteur 0. La première alarme observée dans la capture est bien visible ; cela ne mesure pas exactement la temporisation de 10 secondes.

#### 11:05:42 — Trame 2066 — température atteignant 12 °C

![Trame 2066 — température atteignant 12 °C](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2011-05-42.png)

FC04, **[120, 0, 1, 0]** : température simulée **12,0 °C**, compresseur arrêté, alarme active, défaut absent. Il s’agit cette fois de la température mesurée simulée, et pas seulement de la consigne.

#### 11:05:45 — Trame 2084 — demande corrective à 4 °C

![Trame 2084 — demande corrective à 4 °C](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2011-05-45.png)

FC06 depuis GW:38798 vers OT:15020, adresse **0**, valeur **40** (`00 28`) = **4 °C**. La correction est une nouvelle transaction sur une autre connexion TCP.

#### 11:05:50 — Trame 2086 — correction acceptée

![Trame 2086 — correction acceptée](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2011-05-50.png)

La réponse renvoie adresse 0 et valeur 40, sans exception ; Wireshark la relie à la **requête 2084**, avec **210 µs** de délai.

#### 11:05:53 — Trame 2096 — consigne nominale relue

![Trame 2096 — consigne nominale relue](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2011-05-53.png)

FC03 : **[40, 80, 1]**, soit consigne **4 °C**, limite recommandée 8 °C et mode automatique actif. La baisse de température n’est pas encore démontrée par cette seule relecture de paramètres.

#### 11:05:56 — Trame 2106 — effets physiques encore présents

![Trame 2106 — effets physiques encore présents](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2011-05-56.png)

FC04 : **[121, 1, 1, 0]**, soit **12,1 °C**, compresseur actif, alarme encore active et défaut absent. La correction du paramètre n’efface donc pas instantanément la conséquence thermique.

#### 11:05:59 — Trame 2346 — refroidissement et alarme éteinte

![Trame 2346 — refroidissement et alarme éteinte](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2011-05-59.png)

FC04 : **[77, 1, 0, 0]**, soit **7,7 °C**, compresseur actif, alarme inactive et défaut absent. La baisse est observée après la correction.

#### 11:06:02 — Trame 2616 — température finale près de la consigne

![Trame 2616 — température finale près de la consigne](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2011-06-02.png)

FC04 : **[38, 1, 0, 0]**, soit **3,8 °C**, compresseur actif, alarme et défaut inactifs. Le compresseur peut rester actif dans la bande d’hystérésis ; son arrêt à la limite basse n’est pas montré.

#### 11:06:17 — Vue d’ensemble — onze trames représentatives

![Vue d’ensemble — onze trames représentatives](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2011-06-17.png)

Le filtre regroupe **274, 276, 286, 1136, 2066, 2084, 2086, 2096, 2106, 2346, 2616**. Les mentions Query/Response et les fonctions sont visibles. La colonne Time est relative au premier paquet : **92,815118 s** pour la trame 274 et **978,845312 s** pour la 2084 ; ne pas les lire comme des heures absolues.

**Bilan des preuves :** l’écriture, l’alarme et la restauration sont documentées par le PCAP long et ses détails Wireshark. Les captures du premier essai apportent les tests IT/proxy et l’API avant modification ; elles ne sont pas fusionnées artificiellement dans une seule exécution continue. Une réponse HTTP après la restauration du second essai et un cycle complet après retour à 4 °C ne sont toujours pas montrés.

## 5 — Matrice de résultats actualisée

[Plan de reproduction — CSV](../../assets/files/informatique-industrielle/it-4/Montval-5.4-plan-reproduction.csv).

| Test | Résultat attendu | Résultat observé / preuve |
| --- | --- | --- |
| P0 — Initial | Consigne 4 °C, états vérifiés, API disponible. | Premier essai : état 4,3 °C/consigne 4 et API 200 à 4,4 °C capturés ; second essai : paramètres initiaux du PCAP long. |
| P1 — Écriture directe GW | 12 °C accepté et relu. | Confirmé : 274/276 = 120 accepté, puis 286 = consigne 12 °C. |
| P2 — Effet progressif | Commande adaptée, température évolutive et alarme si seuil/durée atteints. | Confirmé : montée jusqu’à 12,1 °C et alarme active ; temporisation exacte non résolue par les relevés. |
| P3 — IT direct | Timeout, compteur en hausse et OT disponible depuis GW. | Confirmé au premier essai : OT disponible depuis GW, timeout IT direct, compteur 3 → 6 (10:17:17). |
| P4 — Consultation par proxy | Lecture autorisée. | Confirmé au premier essai via IT → proxy (10:17:32) ; lectures aval du second essai également capturées. |
| P5 — Écriture par proxy | Exception 01, consigne inchangée. | Confirmé au premier essai : setpoint 6 via proxy refusé code 1, consigne 12 inchangée (10:17:32). |
| P6 — Correction directe GW | 4 °C accepté et relu. | Confirmé : 2084/2086 = 40 accepté après 12 °C, relecture 2096 = 4 °C. |
| P7 — Retour thermique | Baisse progressive et commande cohérente, sans réinitialisation. | Confirmé : 12,1 → 3,8 °C après correction, compresseur actif ; alarme éteinte à 7,7 °C observés. |
| P8 — Fin | Paramètres nominaux, communications nécessaires et règles vérifiés. | États nominaux et lectures finaux du PCAP long ; filtre et services prouvés au premier essai. API après seconde restauration non fournie. |

## 6 — Comparer l’incident et la simulation

| Question | Réponse préparatoire, à confronter aux essais |
| --- | --- |
| Comportements reproductibles ? | Acceptation de 12 °C, commande adaptée, hausse de température, alarme et effet du retour à 4 °C. Ne pas forcer les heures ou courbes pour copier l’export du 8 octobre. |
| Conséquences visibles ? | Température simulée, commande et états, supervision, opérations et refus réseau/applicatifs. Un bit de commande ne constitue pas un retour mécanique. |
| Conséquences non représentées ? | Produits et inertie des lots, conformité, mécanique détaillée et délais constructeur, trois zones, identités humaines, chaîne VPN/MAINT-01 et éventuelle compromission. |
| Protections vérifiables ? | Refus IT direct, consultation par proxy, refus d’écriture du proxy, chemin GW/OT et collecte après correction. Renseigner seulement les essais réalisés. |
| Vérifications avant intervention réelle ? | Notice/configuration, chemins et droits réels, autonomie locale, comportement aux pannes, cycles du groupe, sauvegarde/reprise, qualification du filtrage applicatif et accord exploitation/maintenance. |

Le dossier utilise une alarme de 8 °C pendant **10 min**, le PoC **10 s**. Les lectures FC03 du dossier sont incohérentes ; le client du PoC demande trois Holding Registers pour `status`, selon son code. Le TP ne valide ni la conformité du PCAP synthétique ni les causes historiques de l’incident.

## Ressources

- [Dossier et preuves J4](../it-3/documenter-protections-limites.md), [montage namespaces 4.5](../it-3/mettre-en-oeuvre-filtrage-it-ot.md).
- Laboratoire : `lab/model.py`, `lab/client.py`, `lab/gateway.py`, `docs/REGISTER_MAP.md`, `docs/NETWORK.md` ; vérifier les versions du montage retenu.
- [Chronologie 5.2](analyser-traces-reconstituer-evenements.md), [réponse proposée 5.3](determiner-premieres-actions-reponse.md).

[Retour à l’itération 4](index.md) · [Pense-bête](../../pense-bete/glossaire/informatique-industrielle/it-4.md).
