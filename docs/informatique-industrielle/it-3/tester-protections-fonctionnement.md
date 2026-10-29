# 4.6 — Atelier 6 | Tester les protections et le fonctionnement

## 🎯 Objectif et modalités

Vérifier l’efficacité du filtrage et la disponibilité des communications indispensables au fonctionnement de l’installation.

**TP en autonomie**, individuel ou en binôme, avec les ressources et l’entraide du groupe ; formateur absent. Support : VM Debian **192.168.122.105**, laboratoire isolé préparé en [4.5](mettre-en-oeuvre-filtrage-it-ot.md).

!!! info "État des preuves au 29 octobre 2026"
    Les résultats ci-dessous reprennent le run `20261029T094737Z`, les douze captures et le PCAP examinés en 4.5. Ces preuves antérieures sont complétées par sept captures du TP 4.6 : nouvelle vérification à 11:36, observations locales pendant la coupure à 11:37–11:38 et **reprise des lectures et de l’API à 11:41:45**. La fin de la boucle et le délai exact de reprise ne sont pas montrés.

## 1 — Préparer la matrice de tests

La topologie comporte IT `10.77.10.2`, GW `10.77.20.2`, OT `10.77.30.2` et le pare-feu `ais45-fw`. Le dashboard installé dans GW consulte le contrôleur **par la passerelle**, et non par un accès direct à ses variables Python.

| Test adapté au laboratoire | Résultat attendu | Résultat observé et preuve disponible |
| :-- | :-- | :-- |
| IT → OT direct, TCP 15020 (T04) | Refus réseau | **Conforme dans le run initial** : timeout, OT disponible depuis GW, compteur `it_direct_drop` de 0 à 3. PCAP ultérieur : SYN directs sans réponse visible. |
| Client autorisé GW → OT:15020 (T01) | Lecture autorisée | **Conforme dans le run initial** : `status` réussi ; règle `gateway_ot_accept` traversée. |
| IT → GW:15021 (T02) | Consultation autorisée | **Conforme** : états lus en CLI et FC03/FC04/FC01 dans le PCAP. |
| Écriture IT → GW:15021 (T03/T05) | Refus applicatif Modbus | **Conforme dans le run initial** : FC06 et FC05 rejetées avec exception 01 ; consigne et porte inchangées à la relecture. Aucune écriture dans le PCAP ultérieur. |
| Supervision → passerelle → contrôleur (T07) | Mesures accessibles | **Conforme dans le run initial** : HTTP 200 sur `/api`, JSON de mesures et compteurs du chemin autorisé. Pas de preuve d’affichage graphique supplémentaire. |
| IT → GW:18081, service non autorisé (T06 adapté) | Refus par défaut | **Conforme dans les captures complémentaires** : HTTP 200 depuis GW, timeout depuis IT, `other_drop` de 0 à 3 paquets / 180 octets. Nouvelle source non testée. |
| Régulation locale pendant une coupure | Processus et contrôle locaux maintenus | **Observé pendant une partie de la coupure** : mesures locales accessibles, température montante puis descendante, compresseur passé de 0 à 1. Fin de séquence non fournie. |
| Communications après rétablissement | Lectures et collecte HTTP à nouveau disponibles | **Conforme à 11:41:45** : `fw-dmz` UP/LOWER_UP, lectures GW → OT et IT → GW réussies, API HTTP 200 ; consigne 4 °C. |

**Preuves :** [captures commentées](mettre-en-oeuvre-filtrage-it-ot.md#captures-utilisateur-complements-du-29-octobre), [résultats JSON du run](../../assets/files/informatique-industrielle/it-3/Montval-4.5-applique-verification.json), [règles réellement exportées](../../assets/files/informatique-industrielle/it-3/Montval-4.5-applique-regles-it-ot.nft), [PCAP de 39 trames](../../assets/files/informatique-industrielle/it-3/Montval-4.5-capture-it-j4.pcap).

## 2 — Rejouer les communications depuis les zones concernées

Sur la VM, depuis le répertoire du PoC :

```bash
cd ~/ais-it-ot-j4/poc
# Chemin autorisé du client GW vers le serveur OT.
sudo ip netns exec ais45-gw python3 -m lab.client status --host 10.77.30.2 --port 15020
# Consultation IT par la passerelle.
sudo ip netns exec ais45-it python3 -m lab.client status --host 10.77.20.2 --port 15021
# Écriture rejetée par la passerelle ; traceback attendu avec exception code 1.
sudo ip netns exec ais45-it python3 -m lab.client setpoint 6 --host 10.77.20.2 --port 15021
# Relecture : comparer consigne et porte ; la température peut évoluer normalement.
sudo ip netns exec ais45-it python3 -m lab.client status --host 10.77.20.2 --port 15021
```

Pour vérifier le refus direct, relever le compteur avant et après la tentative, avec le contrôle positif GW → OT effectué à proximité :

```bash
sudo ip netns exec ais45-fw nft list counter inet ais45 it_direct_drop
sudo ip netns exec ais45-it python3 -m lab.client status --host 10.77.30.2 --port 15020
sudo ip netns exec ais45-fw nft list counter inet ais45 it_direct_drop
```

Le timeout est attendu ici ; conserver sa sortie. Il n’est interprétable comme filtrage qu’avec le chemin autorisé disponible et la hausse du compteur correspondant. Pour le refus par défaut, reprendre le [test HTTP temporaire 18081](mettre-en-oeuvre-filtrage-it-ot.md#essais-complementaires-procedures-et-etat-des-preuves) ; un port fermé sans service disponible ne suffit pas.

Collecte de la supervision depuis IT :

```bash
sudo ip netns exec ais45-it python3 - <<'PY'
import urllib.request
with urllib.request.urlopen('http://10.77.20.2:18080/api', timeout=4) as r:
    print(r.status)
    print(r.read().decode())
PY
```

Pour rejouer l’ensemble des contrôles automatisés :

```bash
sudo bash ~/ais-it-ot-j4/lab-it-ot.sh verify
```

Cette commande relance de vraies requêtes et actualise les fichiers de vérification du run courant. **Copier d’abord le dossier de preuves indiqué par `inspect`** pour conserver le relevé antérieur. Elle ne réalise ni la coupure ni le test 18081.

Dans Wireshark, décoder le TCP **15021** comme Modbus si nécessaire. Pour le PCAP déjà fourni : FC03 requête/réponse **10/12**, FC04 **20/22**, FC01 **30/32**. Un filtre FC06 vide est normal pour ce fichier. Sur `fw-it`, on observe le chemin IT ; une capture sur `fw-ot` est nécessaire pour examiner le trafic relayé vers le contrôleur.

## 3 — Vérifier le fonctionnement OT pendant une interruption

### Procédure exécutée partiellement dans les preuves fournies

L’essai coupe **`fw-dmz` dans le seul namespace `ais45-fw`**. Il interrompt les communications réseau de GW avec IT et OT, tout en laissant le modèle et son serveur fonctionner dans `ais45-ot`. Il ne simule pas une panne du processus GW. L’interface de gestion SSH de la VM reste hors de cette topologie.

1. Relever l’état initial via GW et `/api` ; vérifier consigne 4 °C, porte fermée, défaut absent, mode automatique actif. Si ce n’est pas le cas, identifier l’écart avant de commencer.
2. Dans un premier terminal, lancer la procédure ci-dessous. Elle affiche des relevés locaux pendant environ trois minutes et restaure le lien à la sortie normale ou sur interruption habituelle du shell. Une destruction brutale du processus peut empêcher cette restauration : la commande de reprise explicite est fournie plus bas.
3. Dans un second terminal, pendant la coupure, essayer la lecture IT → GW et HTTP `/api` : une indisponibilité est attendue. La coupure est volontaire ; ne pas l’attribuer à une nouvelle règle de filtrage.
4. Après restauration, refaire la lecture IT → GW, la lecture GW → OT et HTTP `/api` ; noter le délai de reprise et tout écart.

**Premier terminal sur la VM :**

```bash
sudo bash <<'SH'
set -eu
cd /home/oliv/ais-it-ot-j4/poc
restore_link() { ip -n ais45-fw link set fw-dmz up; }
trap restore_link EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
ip -n ais45-fw link set fw-dmz down
for n in $(seq 1 19); do
    date -Is
    ip netns exec ais45-ot python3 -m lab.client status --host 10.77.30.2 --port 15020
    if [ "$n" -lt 19 ]; then sleep 10; fi
done
SH
```

**Reprise explicite si nécessaire :**

```bash
sudo ip -n ais45-fw link set fw-dmz up
```

Les relevés faits **depuis OT** vérifient la disponibilité locale malgré la coupure. Suivre température, consigne, état du compresseur, alarme, défaut et mode. Dans le modèle initial, démarrage à **consigne + 0,5 °C**, arrêt à **consigne − 0,5 °C**, maintien de l’état entre ces seuils. Une poignée de valeurs ou un compresseur resté actif ne suffit pas à démontrer un cycle complet : prolonger l’observation si nécessaire et noter les transitions réellement vues. Ne pas redémarrer `lab.server`, ce qui réinitialiserait le processus.

| Phase | Mesures locales / régulation | Consultation IT et HTTP | Consigne / porte / défaut / mode |
| :-- | :-- | :-- | :-- |
| Avant coupure | Mesures disponibles | Lectures et API HTTP 200 à 11:35–11:36 | Consigne 4 °C, porte fermée, défaut absent, auto actif |
| Pendant coupure | 3,6 → 4,5 → 4,1 °C ; compresseur 0 → 1 | Indisponibilité attendue, mais tentative IT/HTTP non capturée | États maintenus dans les relevés |
| Après reprise | 4,1 °C ; compresseur 0 | Deux lectures réussies et HTTP 200 à 11:41:45 ; délai exact non mesuré | Consigne 4 °C, porte 0, défaut 0, alarme 0, auto 1 |

Les traces de coupure volontaire et les transitions observées constituent les preuves à ajouter ; aucun résultat n’est prérempli.

## Captures du 29 octobre — tests et coupure

### 11:35:52 — Lectures permises et écriture refusée

![Lectures directe depuis GW et par la passerelle, puis écriture refusée](../../assets/img/informatique-industrielle/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-29%2011-35-52.png)

Les deux chemins autorisés répondent : température **3,7 °C**, consigne **4 °C**, compresseur arrêté, porte fermée, défaut et alarme inactifs, mode automatique actif. La tentative de consigne 6 °C par GW renvoie **Modbus exception code 1** ; la relecture conserve la consigne 4 °C et la porte fermée.

### 11:36:19 — Refus direct corrélé au compteur

![Timeout direct et compteur de refus avant et après](../../assets/img/informatique-industrielle/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-29%2011-36-19.png)

La tentative IT → OT:15020 expire. Le compteur `it_direct_drop` passe de **18 à 21 paquets**, soit **1080 à 1260 octets**, tandis que la lecture autorisée précédente atteste le serveur disponible. Ce relevé est distinct du 0 → 3 du run initial.

### 11:36:40 — Collecte de supervision disponible

![HTTP 200 et mesures disponibles par API](../../assets/img/informatique-industrielle/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-29%2011-36-40.png)

L’API retourne **HTTP 200**, température **4,5 °C**, consigne **4 °C**, compresseur `false`, alarme et porte `false`. C’est un instantané de collecte ; la valeur arrondie affichée ne suffit pas à déterminer l’ordre exact du franchissement de seuil et de l’actualisation de commande.

### 11:36:58 — Huit contrôles conformes, écart hôte expliqué

![Nouvelle vérification et avertissement de comparaison hôte](../../assets/img/informatique-industrielle/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-29%2011-36-58.png)

Les huit contrôles sont affichés **OK**. Le [JSON récupéré sur la VM](../../assets/files/informatique-industrielle/it-3/Montval-4.6-verification-113651.json), daté **11:36:51 heure de Paris**, confirme ces résultats, avec refus direct et compteur **21 → 24**. Cette nouvelle exécution a actualisé le fichier du run courant sur la VM ; la copie initiale du dépôt est conservée séparément.

Le message **« Ruleset hôte différent »** a été examiné en comparant les deux exports réels en lecture seule. **L’unique différence textuelle est un compteur de la chaîne NAT PREROUTING Docker : 6 paquets / 360 octets → 12 paquets / 720 octets.** Aucune différence de règle, de politique ou de handle n’apparaît dans ces exports. La comparaison brute du script inclut les compteurs : ce message ne démontre donc pas une modification de politique. L’origine des paquets supplémentaires n’est pas établie. Les avertissements `iptables-nft` concernent les tables hôte relevées ; ne pas les modifier pour faire disparaître le message.

### 11:37–11:38 — Contrôle local pendant la coupure de fw-dmz

![Début de la coupure et premières mesures locales](../../assets/img/informatique-industrielle/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-29%2011-37-41.png)

![Mesures locales ultérieures et compresseur actif](../../assets/img/informatique-industrielle/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-29%2011-38-47.png)

La procédure affiche la mise hors service de **fw-dmz** dans `ais45-fw`, puis interroge le serveur depuis **ais45-ot**, sans redémarrer le modèle.

| Horodatage visible, heure de Paris | Température | Compresseur | Autres états |
| :-- | :-- | :-- | :-- |
| 11:37:08 | 3,6 °C | 0 | Consigne 4 °C, porte 0, défaut 0, alarme 0, auto 1 |
| 11:37:18 | 3,7 °C | 0 | Identiques |
| 11:37:28 | 3,8 °C | 0 | Identiques |
| 11:38:19 | 4,5 °C | 1 | Identiques |
| 11:38:29 | 4,3 °C | 1 | Identiques |
| 11:38:39 | 4,1 °C | 1 | Identiques |

Ces relevés montrent une hausse de température avec compresseur arrêté, puis le compresseur actif et une baisse de température pendant la coupure. Ils sont cohérents avec le maintien de la logique locale de régulation. **Ils ne montrent ni un cycle complet jusqu’à l’arrêt bas, ni une tentative IT/HTTP pendant la coupure, ni, à ce stade de la séquence, la restauration du lien et le retour des communications, documentés dans la capture suivante.** La dernière image est prise avant la fin prévue de la boucle ; le `trap` de restauration est présent dans la commande, mais son exécution finale n’est pas visible.

### 11:41:45 — Lien rétabli, lectures et API de nouveau disponibles

![Rétablissement du lien et reprise des lectures et de l’API](../../assets/img/informatique-industrielle/it-4/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-29%2011-41-52.png)

La commande explicite de remise en service de `fw-dmz` est suivie d’un relevé daté **2026-10-29T11:41:45+01:00**. L’interface affiche **UP** et les drapeaux **UP, LOWER_UP**. Les consultations **GW → OT:15020** puis **IT → GW:15021** réussissent : température **4,1 °C**, consigne **4 °C**, compresseur **0**, alarme **0**, porte **0**, défaut **0**, mode automatique **1**. L’API retourne **HTTP 200** et des valeurs concordantes.

La reprise des communications autorisées est donc **attestée après rétablissement explicite du lien**. Le délai exact de reprise, la fin des dix-neuf relevés et l’exécution automatique du `trap` ne sont pas établis par cette image. Le compresseur arrêté à 4,1 °C est compatible avec le maintien d’état dans la bande d’hystérésis ; les observations intermédiaires ne permettent pas de reconstituer un cycle complet.

## 4 — Corriger un problème sans élargir toute la politique

Pour tout écart, noter la source, la destination, le port, l’heure et le résultat attendu. Vérifier successivement écoute du service, adresses/routes/interfaces, chemin réel puis compteur de la règle concernée. Un refus Modbus avec exception est différent d’un timeout TCP.

Si un flux nécessaire manque, justifier sa présence dans la matrice de flux, sauvegarder le ruleset courant, corriger la seule autorisation concernée dans le fichier source, vérifier sa syntaxe et appliquer dans **`ais45-fw` uniquement**. Rejouer le test positif et les tests négatifs pour éviter une ouverture involontaire. Ne pas vider les règles pour masquer un défaut de diagnostic.

| Écart réellement rencontré | Cause vérifiée | Correction appliquée | Test après correction et preuve |
| :-- | :-- | :-- | :-- |
| À compléter si nécessaire | À documenter | À documenter | À documenter |

Aucune correction de règle n’est attestée par les éléments actuels : les timeouts des chemins interdits sont des résultats attendus.

## 5 — État final et éléments à conserver

- Lien `fw-dmz` rétabli, services du laboratoire disponibles et filtrage toujours actif.
- Consigne 4 °C, porte fermée, défaut absent et mode automatique actif, vérifiés par relecture.
- Serveur HTTP temporaire 18081 arrêté après son essai, si encore présent ; arrêter son terminal dédié plutôt qu’un ensemble de processus Python.
- Matrice attendus/observés, commandes et sorties datées, export nft, compteurs avant/après, PCAP représentatif et corrections éventuelles.
- Régulation locale pendant coupure : observations ci-dessus ; reprise des lectures et de l’API attestée à 11:41:45 ; cycle complet et délai de reprise non mesurés.

Le laboratoire reste une simulation simplifiée ; ces essais ne valident ni un régulateur REG-02 réel ni toutes les protections de l’architecture Montval.

[Retour à l’itération 3](index.md) · [Pense-bête](../../pense-bete/glossaire/informatique-industrielle/it-3.md)
