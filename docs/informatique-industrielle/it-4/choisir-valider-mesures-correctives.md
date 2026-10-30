# 5.5 — Atelier 5 | Choisir et valider les mesures correctives

## 🎯 Objectif et modalités

Proposer des corrections techniques, tester celles reproductibles dans le laboratoire et identifier les protections restant nécessaires.

**Modalité :** atelier technique en binôme. **Durée :** à compléter, non précisée. Supports : dossier J4, analyse 5.2 et essais 5.4.

!!! info "Correction appliquée et preuves partielles de recette — 30 octobre 2026"
    Les cinq nouvelles captures attestent le chargement de **inet ais55_trace** dans **ais45-fw**, le refus direct et son compteur **0 → 3**, la collecte NFLOG et les tests positifs/applicatifs. Le PCAP NFLOG de trois paquets a été récupéré en lecture seule sur la VM et vérifié. Le nouvel export **regles-apres-c01.nft** confirme désormais les deux tables et le compteur C01 à **3 paquets / 180 octets**. Les anciens relevés de 10:26 restent distincts ; le cycle complet de contrôle local et le retour arrière ne sont pas attestés.

## 1 — État des protections et comparaison avec l’incident

| Protection / chemin | État prouvé ou proposé | Ce que les faits permettent de conclure |
| --- | --- | --- |
| Montval : architecture, bastion, GW-02 et 32 règles | Proposition J4, pas configuration de production fournie. | Le trafic direct SUP/MAINT → REG-02 du dossier ne démontre pas un contournement d’une passerelle déjà installée. Présence, absence ou mauvaise configuration au moment des faits restent à établir. |
| PoC : refus IT → OT direct | Test J4 et capture 5.4 du premier essai : timeout, OT disponible depuis GW et compteur 3 → 6. | Filtrage effectif pour cette origine et ce chemin testés. Pas une preuve de couverture de toutes les origines. |
| PoC : IT → proxy lecteur 15021 | Lectures autorisées ; écriture consigne 6 refusée avec exception 01 et consigne 12 conservée. | Contrôle applicatif effectif sur ce chemin ; ne prouve pas l’interdiction des écritures sur un autre chemin. |
| PoC : GW → OT direct 15020 | Capture longue : écriture 12 °C acceptée, puis écriture 4 °C acceptée. | Le réseau accepte GW quelle que soit la fonction. Un autre processus dans GW peut écrire sans passer par le proxy lecteur. Limite du montage, pas vulnérabilité exploitée ou compromission démontrée. |
| Supervision et régulation | API avant premier essai, mesures et dynamique capturées au second. | Fonctions disponibles lors des essais documentés ; leur maintien après C01 devra être retesté. |
| Surveillance | Compteurs et PCAP présents ; pas de journalisation dédiée déployée attestée. | Possibilité d’enrichir la traçabilité des refus, sans prétendre que la capture est un système d’alerte opérationnel. |

La modification de 09:14 dans le dossier part de MAINT-01 ; celle du TP part de GW dans un contexte pédagogique autorisé. Les adresses, identités et configurations ne sont pas interchangeables. La conclusion sur Montval est **configuration effective inconnue**, tandis que le PoC montre une **séparation lecture/écriture insuffisante pour les autres processus de GW**.

## 2 — Mesures correctives envisageables

| Mesure | Objectif / composant | Conditions et conséquences | Limite / état |
| --- | --- | --- | --- |
| **C01 — Tracer les refus IT directs** | Journaliser un chemin interdit au pare-feu du TP. | Ajouter une table dédiée, compteur intégral et NFLOG limité ; collecteur nécessaire. Maintenir refus et flux utiles. | Appliquée et collecte de trois refus attestée ci-dessous ; ne bloque pas davantage GW et ne corrige pas REG-02. |
| **C02 — Séparer collecte et maintenance** | Empêcher un autre client de collecte d’écrire directement vers REG-02. | Origines/environnements réellement séparés, accès aval obligatoire par passerelle qualifiée, rôle lecteur et endpoint de maintenance borné. Qualifier chemins locaux et latéraux. | Proposition ; pas obtenue en bloquant toute l’adresse GW, ce qui supprimerait aussi la collecte actuelle. |
| **C03 — Restreindre la maintenance** | Accès nominatif, temporaire et autorisé via entrée contrôlée/bastion. | Identités et droits, cibles/fonctions, durée, urgence, traçabilité et fermeture des sessions ; coordination exploitation/FrigoMaint. | Non déployée dans ce TP. Compte partagé et simple IP ne prouvent pas une personne. |
| **C04 — Contrôler les écritures et valeurs** | Limiter fonctions, registres et valeurs selon l’intervention. | Contrôle applicatif qualifié et notice ; refus explicite et vérification après action. Tester erreurs et fragmentation. | Le registre de limite 80 du PoC est indicatif. REG-02 non modifiable : contrôle externe compensatoire, pas correctif interne. Aucun seuil métier universel n’est inventé. |
| **C05 — Détecter les changements inhabituels** | Signaler consigne hors cadre ou changement non associé à une autorisation. | Source de consigne fiable, horodatage, référence autorisée, journal et destinataire des alertes ; calibrer cadence et faux positifs. | Proposition ; aucun détecteur ni règle Suricata nouvellement testé en 5.5. Une alerte ne bloque pas la commande. |
| **C06 — Contrôler et sauvegarder la configuration** | Connaître état avant/après et préparer une reprise. | Exports datés, droits de collecte, sauvegarde si possible, contrôle d’intégrité et restauration qualifiée. | Moyens du REG et procédure réelle à confirmer ; une copie de fichier n’est pas un test de restauration. |
| **C07 — Préparer le remplacement de REG-02** | Retrouver maintenance constructeur et capacités adaptées. | Inventaire, notice, compatibilité terrain et protocoles, tests, financement, fenêtre et retour arrière. | Pas de remplacement financé cette année ; les mesures compensatoires ne suppriment pas ce besoin. |

## 3 — Correction retenue pour le TP : journalisation limitée des refus

[Fichier nftables C01 à télécharger](../../assets/files/informatique-industrielle/it-4/Montval-5.5-journalisation.nft).

**Choix volontairement borné :** ajouter une preuve de refus réseau sur IT → OT:15020. Ce chemin était déjà bloqué ; le progrès attendu est sa **traçabilité exploitable**, pas la fermeture du chemin GW utilisé pendant la reproduction. C02–C04 restent nécessaires pour séparer les capacités d’une origine autorisée.

La nouvelle table **inet ais55_trace** est placée **dans ais45-fw**, sur le hook `forward` à priorité **−5**, avant la chaîne J4 à priorité 0. Trois règles : compter tous les paquets ciblés, journaliser au plus au rythme prévu, puis **drop inconditionnel** pour ce chemin. Le dépassement de la limite de logs ne doit jamais autoriser les paquets.

La politique `accept` de cette chaîne supplémentaire laisse les autres flux poursuivre vers le filtrage **inet ais45** ; elle ne remplace pas sa politique DROP. L’ordre des chaînes et la poursuite après accept sont décrits dans la [documentation nftables sur les chaînes](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains).

```nft
# Ajouter UNIQUEMENT dans ais45-fw ; conserver inet ais45.
# Table supplementaire avant forward J4 (priorite 0).
table inet ais55_trace {
    counter it_ot_refus { }
    chain forward_trace {
        type filter hook forward priority -5; policy accept;
        iifname "fw-it" oifname "fw-ot" ip saddr 10.77.10.2 ip daddr 10.77.30.2 tcp dport 15020 counter name it_ot_refus
        iifname "fw-it" oifname "fw-ot" ip saddr 10.77.10.2 ip daddr 10.77.30.2 tcp dport 15020 limit rate 2/second burst 5 packets log prefix "AIS55_IT_OT " group 55 snaplen 128 queue-threshold 1
        iifname "fw-it" oifname "fw-ot" ip saddr 10.77.10.2 ip daddr 10.77.30.2 tcp dport 15020 drop
    }
}
```

NFLOG groupe **55** permet une collecte dans le namespace sans changer le sysctl global de journalisation des namespaces de la VM. Le collecteur doit fonctionner au moment des essais ; les messages ne sont pas automatiquement stockés durablement par cette règle. [nftables — journalisation et groupes NFLOG](https://wiki.nftables.org/wiki-nftables/index.php/Logging_traffic).

### A — Préparer les fichiers et l’état initial

Depuis le PC, copier le fichier fourni dans le dossier du laboratoire sur la VM, par exemple après téléchargement :

```bash
scp ~/Downloads/Montval-5.5-journalisation.nft oliv@192.168.122.105:~/ais-it-ot-j4/
```

Sur la VM, dans le terminal de travail :

```bash
cd ~/ais-it-ot-j4/poc
J55_PREUVES="$HOME/j5-55-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$J55_PREUVES"
test -w "$J55_PREUVES"
printf '%s\n' "$J55_PREUVES"
date -Is | tee "$J55_PREUVES/debut.txt"
sudo ip netns exec ais45-fw nft -a list ruleset > "$J55_PREUVES/avant.nft"
sudo ip netns exec ais45-it python3 -m lab.client status --host 10.77.20.2 --port 15021 | tee "$J55_PREUVES/etat-avant.txt"
```

Le dossier est créé sous le compte `oliv`, dans son répertoire personnel, pour éviter le problème des preuves précédentes sous un parent root. Si un test de droit ou une commande échoue, arrêter la préparation et résoudre l’écart avant de continuer.

Vérifier namespaces et services J4 présents, consigne **4 °C**, porte/défaut 0 et auto 1 ; noter température et compresseur. Conserver les anciens exports. Si le laboratoire est absent, suivre sa procédure de démarrage ; cette fiche n’implique aucune réinitialisation automatique.

### B — Vérifier puis appliquer dans le pare-feu isolé

Contrôler d’abord que la nouvelle table n’existe pas déjà :

```bash
sudo ip netns exec ais45-fw nft list table inet ais55_trace
```

Une erreur **No such file or directory** indique ici une table absente ; si elle est présente, l’examiner et conserver ses preuves avant toute réapplication. Ne pas charger deux fois le fichier sur une table existante.

```bash
sudo ip netns exec ais45-fw nft -c -f ~/ais-it-ot-j4/Montval-5.5-journalisation.nft
```

Seulement si la vérification retourne sans erreur :

```bash
sudo ip netns exec ais45-fw nft -f ~/ais-it-ot-j4/Montval-5.5-journalisation.nft
sudo ip netns exec ais45-fw nft -a list table inet ais55_trace
sudo ip netns exec ais45-fw nft list table inet ais45
```

Conserver la source utilisée et son empreinte. Aucun `flush ruleset`, aucune modification du pare-feu hôte et aucun blocage GW → OT n’est nécessaire.

### C — Démarrer le collecteur avant la tentative

Dans un **deuxième terminal sur la VM**, choisir un fichier neuf, puis attendre le message `listening` :

```bash
J55_LOG="$HOME/j5-55-nflog-$(date -u +%Y%m%dT%H%M%SZ).pcap"
printf '%s\n' "$J55_LOG"
sudo ip netns exec ais45-fw tcpdump -i nflog:55 -nn -s 0 -U -w "$J55_LOG"
```

Le support NFLOG de tcpdump/libpcap et du noyau doit être disponible. Si l’ouverture échoue, conserver l’erreur : la journalisation n’est pas validée, même si le filtrage et les compteurs fonctionnent. Ne pas modifier des paramètres globaux hôte ou ouvrir le trafic pour masquer cet échec.

### D — Déclencher le test négatif et corréler la trace

Dans le premier terminal :

```bash
sudo ip netns exec ais45-gw python3 -m lab.client status --host 10.77.30.2 --port 15020
sudo ip netns exec ais45-fw nft list counter inet ais55_trace it_ot_refus
sudo ip netns exec ais45-it python3 -m lab.client status --host 10.77.30.2 --port 15020
sudo ip netns exec ais45-fw nft list counter inet ais55_trace it_ot_refus
```

Attendus : contrôle positif GW réussi, timeout IT, compteur **ais55_trace/it_ot_refus** en hausse et paquets reçus par le collecteur NFLOG. La valeur initiale doit être relevée, pas supposée nulle.

**Le compteur J4 `ais45/it_direct_drop` peut ne plus augmenter pour cette tentative**, puisque le paquet est désormais rejeté plus tôt par C01. Ce n’est pas une disparition de la protection. Le vérificateur J4 attend ce compteur historique : il peut déclarer T04 en échec après C01, même si le nouveau compteur et les traces prouvent le refus. Pour la recette C01, utiliser les tests et le compteur de cette fiche ; ne pas renommer cet écart en réussite du script initial.

Arrêter le collecteur par Ctrl+C, puis relire le fichier dont le chemin a été affiché dans ce même terminal :

```bash
sudo tcpdump -nn -tttt -r "$J55_LOG"
```

Conserver source/destination/port et heure, ainsi que le préfixe NFLOG s’il est affiché par l’outil. Le nombre de messages journalisés peut être inférieur au compteur à cause de la limitation de débit. Un fichier vide ne prouve pas la journalisation ; rapprocher trafic, compteur, disponibilité du collecteur et erreur éventuelle.

## 4 — Tests de non-régression

[Plan C01 et non-régression — CSV](../../assets/files/informatique-industrielle/it-4/Montval-5.5-plan-validation.csv).

| Test | Résultat attendu | Résultat observé |
| --- | --- | --- |
| V01 — IT direct | Timeout, OT disponible par GW, hausse du nouveau compteur et trace NFLOG pertinente. | Confirmé : timeout, OT disponible, compteur 0 → 3 et PCAP NFLOG trois SYN. |
| V02 — Consultation par proxy | État lu depuis IT par 10.77.20.2:15021. | Confirmé en capture 12:35:18 : lecture IT → proxy réussie. |
| V03 — Écriture par proxy | Exception 01 pour consigne 6 ; consigne nominale 4 inchangée après relecture. | Confirmé : exception 01 et consigne 4 °C inchangée. |
| V04 — Supervision | API HTTP200 et mesures fraîches, consigne 4. | Confirmé en capture 12:35:28 : HTTP200, consigne 4 °C et mesures. |
| V05 — Contrôle local | Relevés successifs, température/commande cohérentes, pas de défaut induit. Un instantané ne prouve pas un cycle complet. | Partiel : états locaux exposés disponibles, aucun défaut visible ; suivi continu et cycle complet non fournis. |
| V06 — Intervention pédagogique | Écriture de **4 °C**, déjà valeur nominale, depuis GW direct acceptée et relue ; aucune ouverture IT. | Confirmé : réécriture nominale 4 °C depuis GW acceptée puis relue. |
| V07 — Règles et état final | Tables ais45 et ais55_trace présentes, paramètres nominaux, sources et exports conservés. | Configuration et paramètres attestés : deux tables dans le nouvel export, compteur C01 3/180 ; états nominaux dans les captures. Retour arrière non exécuté, distinct de ce test. |

Commandes positives et test applicatif :

```bash
sudo ip netns exec ais45-it python3 -m lab.client status --host 10.77.20.2 --port 15021
sudo ip netns exec ais45-it python3 -m lab.client setpoint 6 --host 10.77.20.2 --port 15021
sudo ip netns exec ais45-it python3 -m lab.client status --host 10.77.20.2 --port 15021
sudo ip netns exec ais45-gw python3 -m lab.client setpoint 4 --host 10.77.30.2 --port 15020
sudo ip netns exec ais45-it python3 -m lab.client status --host 10.77.20.2 --port 15021
```

L’écriture 6 par le proxy doit échouer. Si elle réussit, arrêter le test, noter l’écart, rétablir 4 par le chemin autorisé et diagnostiquer le proxy. Le chemin GW utilisé est seulement **autorisé par le réseau du TP** : ce test ne prouve ni identité, bastion ni restrictions d’intervention de production.

```bash
sudo ip netns exec ais45-it python3 - <<'PY'
import urllib.request
with urllib.request.urlopen('http://10.77.20.2:18080/api', timeout=4) as r:
    print(r.status)
    print(r.read().decode())
PY
```

Pour V05, répéter les lectures datées à plusieurs instants sans redémarrer le modèle ; garder température, consigne, commande, porte, défaut, auto et alarmes. La vérification de continuité doit porter sur la période de la correction, sans recycler la courbe de 5.4 comme résultat de 5.5.

Exporter la configuration après recette, dans le premier terminal qui conserve `J55_PREUVES` :

```bash
date -Is | tee "$J55_PREUVES/fin.txt"
sudo ip netns exec ais45-fw nft -a list ruleset > "$J55_PREUVES/apres.nft"
sudo ip netns exec ais45-it python3 -m lab.client status --host 10.77.20.2 --port 15021 | tee "$J55_PREUVES/etat-apres.txt"
sha256sum ~/ais-it-ot-j4/Montval-5.5-journalisation.nft | tee "$J55_PREUVES/source.sha256"
```

### Retour arrière ciblé

Si nécessaire, après conservation des preuves :

```bash
sudo ip netns exec ais45-fw nft delete table inet ais55_trace
sudo ip netns exec ais45-fw nft list table inet ais45
```

Seule la table ajoutée est retirée ; le refus direct J4 reprend son traitement dans ais45. Refaire lecture, API et refus avec compteur J4 pour vérifier le retour. Ne pas vider les règles pour obtenir une recette positive. Si C01 est conservée, documenter que le script de démarrage J4 ne la recharge pas automatiquement après reconstruction des namespaces.

## Preuves reçues — application et tests de C01

[Archive des pièces](../../assets/files/informatique-industrielle/it-4/Montval-5.5-preuves.zip) · [Inventaire, empreintes et limites](../../assets/files/informatique-industrielle/it-4/Montval-5.5-inventaire-preuves.json) · [PCAP NFLOG](../../assets/files/informatique-industrielle/it-4/Montval-5.5-nflog.pcap) · [Décodage daté](../../assets/files/informatique-industrielle/it-4/Montval-5.5-nflog-decode.txt).

### Source et dates des fichiers fournis

Le dossier `livrables/informatique-industrielle/it-4/j5-54-20261030T091556Z/` contient le **fichier C01**, identique octet pour octet à la source préparée, et trois anciens relevés : `fin.txt` = **10:26:43+01:00**, `etat-final.txt` = **4,4 °C / consigne 4 °C**, et `regles-apres.nft` contenant seulement **inet ais45**. Ce sont des pièces antérieures à l’application visible vers 12:33, pas la configuration complète après C01. Elles sont conservées avec cette qualification, sans les réhorodater ni leur ajouter des règles. Le fichier **regles-apres-c01.nft**, ajouté ensuite, constitue désormais l’export réel après correction.

Les captures et le NFLOG constituent les preuves nouvelles. Le nom de dossier commençant par `j5-54` ne change pas leur rattachement à l’activité 5.5. L’heure d’une capture d’écran ne fixe pas l’ordre d’exécution des commandes qui y figurent ; certaines vues montrent le contenu antérieur du terminal.

### 12:34:02 — Chargement et coexistence des tables

![Chargement C01 dans ais45-fw et présence des tables ais55_trace et ais45](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2012-34-02.png)

La commande `nft -f` est exécutée dans **ais45-fw**. La vue affiche **inet ais55_trace**, hook `forward` à priorité **filter − 5**, compteur, règle NFLOG groupe 55 à débit limité et drop distinct. Elle montre également **inet ais45**, toujours à policy DROP avec les autorisations J4. Le compteur C01 vaut **0** dans ce relevé de chargement, malgré l’heure de capture d’écran postérieure à celle de la vue suivante ; ne pas en déduire une remise à zéro ultérieure non documentée. La validation préalable `nft -c` n’est pas visible, mais le chargement et les règles présentes le sont.

### 12:33:48 — Refus ciblé avec disponibilité OT

![Lecture GW réussie et refus IT avec compteur C01 de zéro à trois](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2012-33-48.png)

La lecture depuis GW retourne **3,8 °C**, consigne **4 °C**, compresseur **1**, alarme/porte/défaut **0**, auto **1**. Le compteur **ais55_trace/it_ot_refus** passe explicitement de **0 paquet / 0 octet** à **3 paquets / 180 octets** autour du timeout de **IT → OT:15020**. Le chemin autorisé disponible et cette hausse corrélée attestent le refus au nouveau point de contrôle.

### 12:34:24 — Trois messages NFLOG lisibles et PCAP récupéré

![Relecture du journal NFLOG avec trois SYN IT vers OT](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2012-34-24.png)

La relecture de `/home/oliv/j5-55-nflog-20261030T113304Z.pcap` affiche **trois SYN** de **10.77.10.2:55196 → 10.77.30.2:15020** à **12:33:22,183218**, **12:33:23,191399** et **12:33:24,215799**. Ils utilisent la même séquence TCP et correspondent à des répétitions d’une tentative, pas trois personnes ou trois opérations Modbus. La connexion est bloquée avant qu’une requête Modbus soit envoyée.

Le fichier a été copié depuis la VM **en lecture seule**, sans relancer le test : **624 octets, liaison NFLOG (239), trois paquets**. Sa relecture locale concorde avec la capture. La collecte NFLOG est donc effectivement démontrée ; la limitation de débit configurée n’a pas été éprouvée sous charge. Aucun préfixe textuel n’est visible dans cette sortie tcpdump : la preuve est le format NFLOG et les paquets décodés, pas un préfixe inventé.

### 12:35:18 — Lectures, refus proxy et intervention nominale

![Lecture proxy, refus de setpoint six, réécriture quatre et relecture](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2012-35-18.png)

Les commandes visibles et leurs retours attestent :

- Lecture **IT → proxy:15021** : **4,2 °C**, consigne **4 °C**, compresseur **1**, alarme/porte/défaut **0**, auto **1**.
- Tentative `setpoint 6` via le proxy : **Modbus exception code 1** ; relecture conservant **4 °C**.
- Écriture `setpoint 4` depuis GW vers **OT:15020** : **write accepted**, puis relecture par le proxy à **4 °C**.

Les fonctions utiles restent donc disponibles pour ces requêtes après C01. L’intervention reste celle du chemin pédagogique GW, pas une session humaine de maintenance authentifiée ou un bastion validé.

### 12:35:28 — Collecte de supervision disponible

![API HTTP 200 après correction C01](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2012-35-28.png)

La requête **depuis IT** vers `http://10.77.20.2:18080/api` retourne **200**, température **4,5 °C**, consigne **4 °C**, compresseur `true`, alarme et porte `false`. La collecte de supervision est maintenue. Les états à 3,8, 4,2 et 4,5 °C proviennent de relevés distincts ; ils ne constituent pas un suivi continu ni un cycle complet. Le système ne présente aucun défaut induit dans les états visibles, mais la continuité de toute la régulation n’est pas certifiée par ces seuls instantanés.

### Bilan d’application et pièces restant à compléter

**Application C01 et trace de refus : attestées.** Consultation, refus proxy, collecte HTTP et écriture nominale : observés après application. Le [nouvel export réel après C01](../../assets/files/informatique-industrielle/it-4/Montval-5.5-regles-apres-c01.nft) est maintenant fourni : **inet ais45** reste à politique DROP et **inet ais55_trace** est présente à priorité −5 avec compteur, NFLOG limité et drop distinct. Le compteur **it_ot_refus** vaut **3 paquets / 180 octets**, le compteur direct J4 **18 / 1080**. Les autorisations J4 et retours sont conservés. Cet export, sa source préparée et les vues de test sont des pièces distinctes et concordantes.

L’export reçu n’a pas de date interne : ne pas lui attribuer l’heure de `fin.txt` (10:26), ni une heure précise non enregistrée. Pour les prochains exports, conserver une date associée dans un dossier neuf, par exemple :

```bash
J55_EXPORT="$HOME/j5-55-export-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$J55_EXPORT"
date -Is | tee "$J55_EXPORT/date.txt"
sudo ip netns exec ais45-fw nft -a list ruleset > "$J55_EXPORT/regles-apres-c01.nft"
sudo ip netns exec ais45-it python3 -m lab.client status --host 10.77.20.2 --port 15021 | tee "$J55_EXPORT/etat-apres-c01.txt"
```

Ce modèle de collecte ne signifie pas qu’un nouvel export est encore requis pour attester la configuration C01 reçue. Toute collecte ultérieure aura son propre repère et ne reconstituera pas l’instant de 12:35. **Retour arrière non exécuté dans les preuves reçues** ; maintenir cette distinction. C01 reste une amélioration de traçabilité du refus direct, sans fermer le chemin d’écriture GW/OT.

## 5 — Cas de REG-02 : exposition réduite, défauts internes persistants

1. **Les protections suppriment-elles les défauts internes ?** Non. C01 ajoute des traces ; segmentation et passerelle réduisent les chemins/opérations possibles. Aucun correctif du régulateur n’est installé, aucune CVE précise n’est démontrée.
2. **Si un système autorisé est compromis ?** Il peut exploiter les capacités de son chemin. Le PoC prouve déjà qu’un client GW peut écrire 12 °C ; C01 ne filtre pas ce flux. Nécessité de C02/C04, qualification des lectures permises et surveillance du contrôle ; aucun dispositif n’est déclaré infaillible.
3. **Que reste-t-il en urgence ?** Intervention locale FrigoMaint/exploitation, ou chemin distinct de confiance réellement disponible et autorisé, durée/opérations bornées, traçabilité et fermeture de session. Ne pas inventer un endpoint de maintenance que le proxy lecteur ne possède pas.
4. **Compléments utiles ?** Séparation effective de la maintenance, identités, journal d’intervention, données fraîches, détection des changements, sauvegarde/restauration qualifiées, relève locale et tests de panne/reprise de la protection. Les capacités exactes restent à confirmer.
5. **Pourquoi remplacer ?** Fin du support et absence de correctifs persistent, avec dépendance à des protections externes et des capacités de diagnostic limitées. Préparer remplacement et validation avec l’exploitation, même si le budget ne permet pas une action immédiate.

Le maintien du froid, la supervision et la maintenance utile doivent être vérifiés après toute correction. L’exploitation et FrigoMaint valident les effets sur le processus (EXP-01/02/04/10/11, MAI-01/02/05/08, ORG-01). Les denrées et leur conformité ne sont pas évaluées par ce laboratoire.

## Production attendue et ressources

**À remettre après réalisation :** état avant, fichier exact appliqué, emplacement, journal NFLOG/compteurs, tests attendus et observés, effets et écarts, retour arrière testé ou procédure conservée, limitations C01 et corrections C02–C07 encore nécessaires. La source seule ne suffisait pas : les captures et le NFLOG attestent désormais application et tests précisés ci-dessus ; les contrôles manquants restent signalés.

- [Dossier J4](../it-3/documenter-protections-limites.md), [incident 5.2](analyser-traces-reconstituer-evenements.md), [preuves des deux essais 5.4](reproduire-incident-jumeau-numerique.md).
- [Manuel MAN-OT-01](../it-2/MAN-OT-01_Manuel_exploitation_installation_frigorifique.md).
- [nftables — Logging traffic](https://wiki.nftables.org/wiki-nftables/index.php/Logging_traffic), [Configuring chains](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains).

[Retour à l’itération 4](index.md) · [Pense-bête](../../pense-bete/glossaire/informatique-industrielle/it-4.md).
