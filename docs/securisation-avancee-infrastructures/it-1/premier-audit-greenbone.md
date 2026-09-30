# Premier audit avec Greenbone

**Durée prévue : 2 h 15.**

## Objectif et état du travail

Réaliser un premier scan de vulnérabilités, comparer ses résultats à l'inventaire
et qualifier cinq constats avant de construire le plan de remédiation.

**Statut : deux scans terminés et rapports détaillés analysés.** Les exports de
tâches prouvent l'état **Done**. Les exports de rapports permettent de comparer
les contrôles distants et authentifiés, de confirmer la réussite SSH du scan B
et de qualifier cinq constats. Ils sont anonymisés : l'adresse `127.0.0.1`
présente dans les résultats remplace l'adresse réelle de la cible.

Le déroulement du formateur comporte deux lancements. Cette fiche les organise
en **scan A sans authentification**, puis **scan B avec authentification SSH**,
en conservant les deux rapports pour comparer leur couverture.

| Repère du laboratoire | Valeur à utiliser après vérification |
| --- | --- |
| Machine d'audit | Hôte `ubuntu-oliv`, projet Compose `ais-greenbone` |
| Répertoire Greenbone sur l'hôte | `~/lab-securisation-avancee/greenbone` |
| Interface | `https://127.0.0.1:8443` sur l'hôte |
| Cible unique | VM Ubuntu 20.04.6, dernière IP observée **`192.168.122.229`** |
| Inventaire déjà prouvé | SSH sur TCP 22 ; File Browser 2.15.0 sur TCP 8080, HTTP 200 depuis l'hôte |
| Compte proposé pour le scan B | `gvm-audit`, compte dédié sans privilèges administrateur |

**Ne pas saisir `192.168.122.0/24` ni une plage réseau.** Ne pas inclure l'hôte
d'audit, les autres VM ou les machines des autres apprenants.

## Étape 1 — Vérifier Greenbone

Les étapes suivantes conservent la procédure de référence. Les résultats
effectivement fournis sont regroupés dans la
[lecture des exports](#lecture-des-deux-exports-fournis-30-septembre-2026).

### Services et journaux sur l'hôte

```bash
hostname
cd "$HOME/lab-securisation-avancee/greenbone"
docker compose -p ais-greenbone config --quiet
docker compose -p ais-greenbone ps -a
docker compose -p ais-greenbone logs --tail 100 gvmd ospd-openvas
```

Examiner l'état des composants concernés : `nginx` et `gsad` pour l'interface,
`gvmd` et `pg-gvm` pour la gestion, `ospd-openvas` et les composants de scan pour
l'exécution. Un conteneur d'initialisation terminé avec `Exited (0)` ne signifie
pas à lui seul une panne.

### Données et scanner dans l'interface

Ouvrir l'interface et vérifier les éléments suivants. Les intitulés peuvent
varier avec la version de l'interface ; les menus du manuel servent de repères.

| Contrôle avant lancement | Preuve à relever |
| --- | --- |
| État des feeds, généralement **Administration → Feed Status** | Types de données, dates et état du chargement ; absence d'import encore bloquant |
| Tests de vulnérabilité disponibles | Tests visibles, pas uniquement images Docker téléchargées |
| Scanner, généralement **Configuration → Scanners** | Scanner OpenVAS joignable ; résultat de sa vérification de connexion si proposée |
| Configuration de scan | **Full and fast** disponible |
| Objets nécessaires | Listes de ports et formats de rapport disponibles |

L'import suit le téléchargement des données ; l'interface accessible ne prouve
pas que cet import est terminé. Les journaux doivent être cohérents avec l'état
affiché. Un scan démarré sans données chargées peut produire des résultats
incomplets. [Source : chargement des feeds Greenbone](https://greenbone.github.io/docs/latest/22.4/container/workflows.html#loading-the-feed-changes).

En cas de problème : identifier le composant, lire ses journaux, rechercher
l'erreur dans la [documentation de dépannage](https://greenbone.github.io/docs/latest/22.4/container/troubleshooting.html),
puis solliciter le formateur si elle persiste. Ajouter le nom du service à
`docker compose -p ais-greenbone logs --tail 100` pour cibler la lecture.
Conserver l'erreur et l'heure. Ne pas supprimer les volumes ni utiliser
`--remove-orphans` pour accélérer une initialisation.

## Étape 2 — Scan A sans authentification

### Confirmer l'adresse et choisir la couverture

**Dans la VM**, vérifier `hostname` et `ip -br address`. **Depuis l'hôte**,
recontrôler les ports connus :

```bash
CIBLE_IP="192.168.122.229"
nc -vz -w 3 "$CIBLE_IP" 22
nc -vz -w 3 "$CIBLE_IP" 8080
```

Adapter l'adresse si le bail DHCP a changé. Ces tests depuis l'hôte ne
garantissent pas à eux seuls le chemin réseau du scanner conteneurisé.

Dans **Configuration → Port Lists**, préparer une liste nommée
`AIS-VM-TCP-complet`, avec **`T:1-65535`**, ou réutiliser une liste existante
couvrant exactement ces ports TCP. Cela couvre tous les ports TCP de **la seule
VM**, y compris 22 et 8080 ; aucune couverture UDP n'est revendiquée. Conserver
la même liste pour les deux scans. Une plage de ports n'est pas une plage d'hôtes.

### Créer la cible puis la tâche

Dans **Configuration → Targets**, créer :

| Champ | Valeur proposée |
| --- | --- |
| Name | `AIS-Ubuntu20-sans-auth` |
| Hosts | **`192.168.122.229` seule**, après confirmation |
| Port List | `AIS-VM-TCP-complet` |
| Alive Test | Conserver et noter le test choisi par défaut |
| SSH Credentials | Aucun pour ce premier scan |

Dans **Scans → Tasks**, créer `AIS-A-Full-and-fast-sans-auth` : sélectionner
cette cible, le scanner OpenVAS et **Full and fast**. Vérifier le récapitulatif,
puis lancer la tâche. Attendre **Done** et relever l'heure de fin avant
d'interpréter le rapport. Ne pas lancer les deux scans en parallèle sur cette
VM de 2 vCPU et 4 Go.

Les actions de création des cibles, listes de ports et tâches sont décrites
dans le [manuel Greenbone — Scanning a System](https://docs.greenbone.net/GSM-Manual/gos-24.10/en/scanning.html).

Si le rapport indique zéro hôte vivant, un arrêt ou une erreur, traiter d'abord
la portée, le test de présence, le routage du scanner et les journaux. Ne pas
interpréter ce résultat comme « aucune vulnérabilité » et ne pas élargir la cible.

Exporter le rapport A, de préférence en **XML** pour conserver les détails,
avec un export lisible complémentaire si disponible. Noter les filtres appliqués
à l'export : sévérité, QoD, résultats informatifs, dérogations éventuelles.

## Étape 3 — Préparer l'authentification SSH

### Créer un compte dédié dans la VM

**Dans la VM**, vérifier d'abord si le compte existe :

```bash
getent passwd gvm-audit
```

S'il existe, examiner son usage et ses droits avant de le réutiliser. Sinon :

```bash
sudo adduser --disabled-password --gecos "Compte audit Greenbone" gvm-audit
id gvm-audit
```

Conserver le shell permettant les contrôles SSH. Ne pas ajouter ce compte aux
groupes `sudo` ou `docker`. Greenbone recommande un compte dédié avec les droits
nécessaires ; sous Linux, un compte non privilégié permet déjà de nombreux
contrôles locaux. Les informations inaccessibles seront une limite à documenter.
[Source : contrôles authentifiés Greenbone](https://docs.greenbone.net/GSM-Manual/gos-24.10/en/scanning.html#configuring-an-authenticated-scan-using-local-security-checks).

### Générer la clé sur l'hôte

**Sur l'hôte**, utiliser une clé propre à ce laboratoire, hors du dépôt Git :

```bash
umask 077
mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"
ls -l "$HOME/.ssh/ais-greenbone-audit"* 2>/dev/null
```

Si ces fichiers existent, les conserver et vérifier leur usage. Pour une nouvelle
paire, sans écraser une clé existante :

```bash
ssh-keygen -t rsa -b 3072 -m PEM \
  -f "$HOME/.ssh/ais-greenbone-audit" -C "ais-greenbone-audit"
```

Saisir une phrase secrète à l'invite et la conserver dans le gestionnaire de
mots de passe. Le fichier sans extension est **privé** ; le fichier `.pub` est
**public**. La clé privée sera importée dans Greenbone ; seule la clé publique
doit être installée sur la VM. Ne publier ni la clé privée ni sa phrase secrète.

### Installer la clé publique dans la VM

**Depuis l'hôte**, transférer la clé publique avec le compte administrateur
habituel, ici `oliv`, si cet accès SSH est opérationnel :

```bash
scp "$HOME/.ssh/ais-greenbone-audit.pub" \
  oliv@192.168.122.229:ais-greenbone-audit.pub
```

À la première connexion, vérifier l'empreinte de la clé d'hôte présentée.
Les empreintes publiques peuvent être relevées **dans la console de la VM** :

```bash
for cle_hote in /etc/ssh/ssh_host_*_key.pub; do
  ssh-keygen -lf "$cle_hote"
done
```

Si l'accès administrateur SSH n'est pas disponible, copier le contenu du fichier
**public** via la console de la VM dans `~/ais-greenbone-audit.pub` du compte
`oliv`. Ne pas activer une connexion SSH directe de `root` pour ce transfert.

**Dans la VM, connecté comme `oliv`**, ajouter la clé sans écraser les clés existantes :

```bash
sudo install -d -m 700 -o gvm-audit -g gvm-audit /home/gvm-audit/.ssh
sudo -u gvm-audit touch /home/gvm-audit/.ssh/authorized_keys
sudo chmod 600 /home/gvm-audit/.ssh/authorized_keys
sudo -u gvm-audit tee -a /home/gvm-audit/.ssh/authorized_keys \
  < "$HOME/ais-greenbone-audit.pub" > /dev/null
```

Exécuter l'ajout une seule fois pour cette clé. **Sur l'hôte**, tester ensuite :

```bash
ssh -o IdentitiesOnly=yes -o PreferredAuthentications=publickey \
  -i "$HOME/.ssh/ais-greenbone-audit" gvm-audit@192.168.122.229 \
  'id; cat /etc/os-release; dpkg-query -W openssh-server'
```

La phrase secrète demandée déverrouille la clé locale ; ce n'est pas un mot de
passe du compte cible. Conserver le résultat de `id` et les versions, sans
secret. Ce test confirme l'accès depuis l'hôte, pas encore celui du scanner.
En cas d'échec, vérifier le compte, les permissions, la clé publique et les
journaux SSH dans la VM : `sudo journalctl -u ssh --since "10 minutes ago" --no-pager`.

## Étape 4 — Scan B avec authentification

Dans **Configuration → Credentials**, créer un identifiant :

| Champ | Valeur |
| --- | --- |
| Name | `AIS-SSH-gvm-audit` |
| Type | **Username + SSH Key** |
| Auto-generate, si proposé | **No**, puisque la clé est déjà créée |
| Username | `gvm-audit` |
| Private Key | Importer `~/.ssh/ais-greenbone-audit`, **sans `.pub`** |
| Passphrase | Phrase secrète de la clé, saisie dans le champ prévu |

Greenbone accepte notamment les clés RSA au format PEM et prévoit une phrase
secrète pour l'import. Il faut ensuite **associer l'identifiant à la cible** :
le créer seul ne rend pas un scan authentifié.
[Source : création des credentials](https://docs.greenbone.net/GSM-Manual/gos-24.10/en/scanning.html#creating-credentials).

Créer une seconde cible `AIS-Ubuntu20-avec-auth`, avec **la même IP unique**,
la même liste de ports et le même test de présence. Sélectionner
`AIS-SSH-gvm-audit` comme **SSH credential**, sur le port **22**. Créer la tâche
`AIS-B-Full-and-fast-SSH` avec **Full and fast**, puis la lancer et attendre **Done**.

### Vérifier l'authentification et conserver le rapport

Dans le rapport B, consulter aussi les messages informatifs et résultats de
connexion SSH, ainsi que les éléments collectés localement : identification
du système et inventaire des paquets. Conserver le message exact confirmant
ou refusant l'authentification ; son intitulé peut varier selon le feed.

Un état **Done** ne prouve pas que SSH a réussi. En cas d'échec ou de preuve
absente, noter **« authentification échouée / non démontrée »** et la couverture
qui manque. Les journaux `ssh` de la VM peuvent compléter les messages du rapport.
Exporter B séparément, sans écraser A. Relever les dates des feeds des deux scans :
si elles ont changé, l'authentification n'est pas la seule différence possible.

Le compte SSH ouvre une vue sur les paquets de **la VM**, pas automatiquement
sur tous les composants à l'intérieur de l'image File Browser. Une absence de
résultat sur le conteneur ne prouve pas qu'il est exempt de vulnérabilités.

Après les analyses prévues, retirer la clé autorisée de la VM et désassocier
puis supprimer le credential inutilisé dans Greenbone. Conserver les rapports
et documenter la fermeture de cet accès d'audit.

## Lecture des deux exports fournis — 30 septembre 2026

### Fichiers et tâches identifiés

- [Export de la tâche A](../../assets/files/securisation-avancee-infrastructures/it-1/task-44d752f6-27a8-4635-b409-1b4c0b33d8d6.xml).
- [Export de la tâche B](../../assets/files/securisation-avancee-infrastructures/it-1/task-d716288e-367a-4248-b20d-ba37cac13be0.xml).
- [Rapport détaillé A](../../assets/files/securisation-avancee-infrastructures/it-1/report-d9692337-64e4-450a-8659-c123aeb5c9c1.xml).
- [Rapport détaillé B](../../assets/files/securisation-avancee-infrastructures/it-1/report-aeb90e4a-b789-4ef3-ab1b-7fd7afcae1ee.xml).

Les noms des cibles indiquent l'intention « sans authentification » / « avec
authentification ». Le détail des adresses, des credentials et des listes de
ports n'est pas embarqué ; ces réglages restent à vérifier dans les rapports
ou dans la configuration des cibles.

| Élément exporté | A | B |
| --- | --- | --- |
| Nom de tâche réel | `A192.168.122.229` | `AIS-B-Full-and-fast-SSH` |
| Nom de cible | `AIS-Ubuntu20-sans-auth` | `AIS-Ubuntu20-avec-auth` |
| Configuration | Full and fast | Full and fast |
| Scanner | OpenVAS Default | OpenVAS Default |
| État | **Done** | **Done** |
| Début UTC | 10:02:19Z | 10:13:19Z |
| Fin UTC | 10:17:33Z | 10:29:37Z |
| Créneau local, UTC+02:00 | **12:02:19–12:17:33** | **12:13:19–12:29:37** |
| Durée calculée | **15 min 14 s** | **16 min 18 s** |
| Champ `task/result_count` | **17** | **240** |
| Champ `last_report/report/severity` | **2,6** | **9,9** |
| UUID du rapport | `d9692337-64e4-450a-8659-c123aeb5c9c1` | `aeb90e4a-b789-4ef3-ab1b-7fd7afcae1ee` |
| Résultats détaillés exportés | **3** | **200** |
| Version du feed | `202609300604` | `202609300604` |

Les scans se sont **chevauchés pendant 4 min 14 s**, contrairement à la procédure
séquentielle proposée. Cela ne démontre pas une erreur de scan, mais constitue
une limite de comparaison des durées et de la charge de la VM.

### Compteurs de sévérité : conserver les valeurs et leurs limites

| Champ du résumé du dernier rapport | A | B |
| --- | --- | --- |
| `critical` | 0 | **18** |
| `high` | 0 | **82** |
| `medium` | 0 | **95** |
| `low` | **3** | **5** |
| `log` | **15** | **41** |
| `false_positive` | 0 | 0 |

Les champs historiques `hole`, `warning` et `info`, marqués `deprecated`,
reprennent ici les valeurs de `high`, `medium` et `low` : ne pas les additionner
comme des catégories supplémentaires. Même sans ces doublons, la somme des
catégories affichées donne **18 pour A** et **241 pour B**, alors que les totaux
de tâche indiquent **17 et 240**. Cet écart est conservé comme **à expliquer**
avec les rapports détaillés ; aucun total corrigé n'est inventé.

Les rapports portent `min_qod=70`, `apply_overrides=0` et
`levels=chml` : seuls les niveaux Critical, High, Medium et Low sont inclus.
Cela explique les **3** résultats de A et les **200** résultats de B ; les
résultats de type Log ne figurent pas dans ces exports détaillés. Les compteurs
restent des résultats de tests, pas un décompte de CVE uniques.

### Preuve du scan authentifié

Le rapport B contient le détail hôte `Auth-SSH-Success` avec la valeur
`Protocol SSH, Port 22, User gvm-audit`. Il indique également que l'identification
d'Ubuntu 20.04 LTS et la liste des paquets proviennent du test
`Determine OS and list of installed packages via SSH login`. Les nombreux
contrôles Ubuntu sur le port logique `package`, avec une QoD de **97 %**, sont
donc issus de l'inventaire local authentifié. Le scan A ne contient pas ce
marqueur et identifie seulement Ubuntu 20.04 à partir de la bannière SSH.

Les deux rapports ont utilisé le même feed `202609300604` et ont observé les
ports TCP **22 et 8080**. La différence de couverture provient donc bien de
l'authentification, sous réserve du chevauchement de quatre minutes déjà relevé.
Le format **Anonymous XML** remplace l'IP réelle par `127.0.0.1` ; cette valeur
ne signifie pas que Greenbone a scanné sa propre boucle locale.

## Étape 5 — Comparer à l'inventaire

| Élément connu | Preuve avant scan | Rapport A | Rapport B et limites |
| --- | --- | --- | --- |
| Ubuntu 20.04.6, noyau 5.15.0-139-generic | Relevé dans la VM | Ubuntu 20.04 déduit de la bannière SSH | Ubuntu 20.04 LTS déterminé par connexion SSH ; le rapport anonymisé ne restitue pas ici le noyau complet |
| SSH, TCP 22 accessible | `sshd`, unité active et `nc` réussi | Port 22 et bannière `OpenSSH_8.2p1 Ubuntu-4ubuntu0.13` | Même service ; authentification SSH réussie avec `gvm-audit` |
| File Browser 2.15.0, TCP 8080 | Version du binaire, publication Docker et HTTP 200 | Port 8080 ouvert, sans identification de File Browser dans les résultats exportés | Même limite : les contrôles de paquets de l'hôte ne prouvent pas la version contenue dans l'image |
| Docker 26.1.3, containerd 1.7.24 | `docker version` dans la VM | Non identifié par les trois résultats distants | Paquets détectés par les contrôles locaux ; plusieurs avis Ubuntu sont signalés |
| Autres services locaux : CUPS, Avahi… | Inventaire `ss` et `systemctl` | Non visible dans les trois résultats | Paquets visibles par inventaire local ; cela ne prouve pas une exposition réseau |

Un composant ancien, une bannière et une correspondance de version sont des
indices à qualifier. Pour les paquets Ubuntu, examiner la version complète
et les correctifs de la distribution, pas seulement le numéro amont.

## Étape 6 — Qualifier cinq résultats significatifs

Choisir cinq résultats utiles à l'analyse, pas nécessairement les cinq scores
les plus élevés. Relever le rapport A ou B, l'hôte, le port, l'identifiant du
test (VT/OID), la méthode de détection et la **QoD** lorsqu'elle est fournie.
La QoD décrit la qualité de détection annoncée ; elle ne remplace pas la preuve
d'applicabilité au système observé.

Pour une CVE, appliquer **CVE.org → références de l'entrée → avis de l'éditeur
ou de la distribution**, comme dans la [fiche CVE](lire-analyser-entrees-cve.md).
Conserver la version et la source du [CVSS](comprendre-cvss.md), ainsi que les
conditions d'exploitation vérifiées. « Pas de CVE » n'invalide pas un défaut
de configuration. Si moins de cinq résultats sont disponibles, consigner cette
limite et la soumettre au formateur, sans inventer de résultats.

| Statut | Sens retenu |
| --- | --- |
| Confirmé | Preuves et conditions vérifiées suffisantes pour établir l'applicabilité |
| À vérifier | Version, condition ou preuve encore manquante |
| Non pertinent | Inapplicabilité démontrée et justifiée pour cet environnement |

Les cinq fiches suivantes s'appuient sur les rapports détaillés et les avis
Ubuntu officiels consultés le 30 septembre 2026. **Ne pas commencer le plan de
remédiation définitif à cette étape.**

### Constat G01

| Élément analysé | Analyse |
| --- | --- |
| Constat Greenbone | `Ubuntu: Security Advisory (USN-8472-1)`, rapport B, résultat `6592efdf-215a-4df9-ba01-f0dfce7ecbc8` |
| Service ou composant concerné | `containerd-app`, paquet de la VM ; résultat sur le port logique `package` |
| CVE associée, si applicable | [CVE-2026-33814](https://www.cve.org/CVERecord?id=CVE-2026-33814), CVE-2026-47262, CVE-2026-50195, CVE-2026-53488, CVE-2026-53489 et CVE-2026-53492. L'avis précise que certaines ne concernent pas Ubuntu 20.04. |
| CVSS, si disponible | CVSS 3.1 : **9,9**, `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` — valeur du VT Greenbone pour l'avis |
| Ce que Greenbone a effectivement observé | Le contrôle local authentifié déclare une version vulnérable du paquet. VT/OID `1.3.6.1.4.1.25623.1.1.12.2026.8472.1`, QoD **97 %**. |
| Informations vérifiées dans l’entrée CVE et ses références | L'[USN-8472-1](https://ubuntu.com/security/notices/USN-8472-1) inclut Ubuntu 20.04 et fixe notamment des dénis de service, une exécution de code et des contournements liés aux conteneurs. Version corrigée Focal : `1.7.24-0ubuntu1~20.04.2+esm2`. |
| Applicabilité à votre environnement | La VM Ubuntu 20.04 exécute containerd 1.7.24 pour le conteneur File Browser. Le suffixe complet du paquet doit être conservé avec `dpkg-query`, mais le test local identifie déjà la révision vulnérable. Le correctif Focal est fourni via Ubuntu Pro/ESM Apps. |
| Statut | **Confirmé** |
| Justification | Détection locale authentifiée, QoD 97 %, version d'OS applicable et avis éditeur concordant. L'exploitabilité de chaque CVE dépend encore des fonctions de containerd réellement utilisées. |

### Constat G02

| Élément analysé | Analyse |
| --- | --- |
| Constat Greenbone | `Ubuntu: Security Advisory (USN-8230-1)`, rapport B, résultat `b81502e2-b3fb-41f7-8877-84f32d396b44` |
| Service ou composant concerné | `docker.io-app` / BuildKit, paquet de la VM ; résultat sur `package` |
| CVE associée, si applicable | [CVE-2026-33747](https://www.cve.org/CVERecord?id=CVE-2026-33747) et [CVE-2026-33748](https://www.cve.org/CVERecord?id=CVE-2026-33748) |
| CVSS, si disponible | CVSS 3.1 : **9,8**, `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` — valeur du VT Greenbone pour l'avis |
| Ce que Greenbone a effectivement observé | Une version vulnérable de `docker.io-app` dans l'inventaire authentifié. VT/OID `1.3.6.1.4.1.25623.1.1.12.2026.8230.1`, QoD **97 %**. |
| Informations vérifiées dans l’entrée CVE et ses références | L'[USN-8230-1](https://ubuntu.com/security/notices/USN-8230-1) décrit deux validations de chemin défaillantes dans BuildKit : écriture hors du répertoire d'état et lecture hors de la racine Git. Version corrigée Focal : `26.1.3-0ubuntu1~20.04.1+esm2`, puis redémarrage de Docker. |
| Applicabilité à votre environnement | La version relevée avant scan est `26.1.3-0ubuntu1~20.04.1`, antérieure à la révision `+esm2`. Le correctif Focal est disponible via Ubuntu Pro/ESM Apps. Les fonctions BuildKit réellement exposées restent à inventorier pour apprécier la priorité. |
| Statut | **Confirmé** |
| Justification | La version locale relevée, le contrôle authentifié et l'avis Ubuntu concordent. Le score élevé ne suffit pas seul à fixer l'ordre de traitement. |

### Constat G03

| Élément analysé | Analyse |
| --- | --- |
| Constat Greenbone | `Ubuntu: Security Advisory (USN-8804-1)`, rapport B, résultat `09b2d4b4-f20e-49d3-a9fc-db5e57edb1eb` |
| Service ou composant concerné | `openssh-server`, TCP 22 ; bannière `OpenSSH_8.2p1 Ubuntu-4ubuntu0.13` |
| CVE associée, si applicable | Dix CVE dans l'avis ; Ubuntu 20.04 est explicitement concerné notamment par CVE-2026-35414, CVE-2026-59999 et [CVE-2026-60001](https://www.cve.org/CVERecord?id=CVE-2026-60001). |
| CVSS, si disponible | CVSS 3.1 : **8,1**, `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` — valeur du VT Greenbone pour l'avis global |
| Ce que Greenbone a effectivement observé | Une version vulnérable du paquet par contrôle local et une bannière SSH distante. VT/OID `1.3.6.1.4.1.25623.1.1.12.2026.8804.1`, QoD **97 %**. |
| Informations vérifiées dans l’entrée CVE et ses références | L'[USN-8804-1](https://ubuntu.com/security/notices/USN-8804-1) inclut Focal et fournit `1:8.2p1-4ubuntu0.13+esm3` comme version corrigée. Les conséquences et conditions diffèrent selon chaque CVE et selon la configuration SSH. |
| Applicabilité à votre environnement | SSH est réellement accessible sur le port 22 et la bannière ne contient pas le suffixe corrigé `+esm3`. Le correctif Focal est disponible via Ubuntu Pro. Il faut encore vérifier GSSAPI, le transfert de ports et les restrictions d'`authorized_keys` avant d'affirmer que chaque scénario est exploitable. |
| Statut | **Confirmé** pour la mise à jour manquante ; conditions d'exploitation **à vérifier** CVE par CVE |
| Justification | Le service est exposé, la version locale est identifiée et l'avis officiel couvre Ubuntu 20.04. L'avis agrège cependant plusieurs vulnérabilités aux préconditions différentes. |

### Constat G04

| Élément analysé | Analyse |
| --- | --- |
| Constat Greenbone | `Ubuntu: Security Advisory (USN-7897-1)`, rapport B, résultat `8f21877d-7fc4-4dab-801e-31632a2445f7` |
| Service ou composant concerné | Paquets `cups` / `cups-daemon` de la VM ; résultat sur `package` |
| CVE associée, si applicable | [CVE-2025-61915](https://www.cve.org/CVERecord?id=CVE-2025-61915), absente des balises du VT mais présente dans l'avis Ubuntu |
| CVSS, si disponible | CVSS 3.1 : **6,7**, `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` — valeur du VT Greenbone |
| Ce que Greenbone a effectivement observé | Une version vulnérable du paquet CUPS dans l'inventaire authentifié. VT/OID `1.3.6.1.4.1.25623.1.1.12.2025.7897.1`, QoD **97 %**. |
| Informations vérifiées dans l’entrée CVE et ses références | L'[USN-7897-1](https://ubuntu.com/security/notices/USN-7897-1) relie le défaut des réglages web à un déni de service ou une exécution de code. Version corrigée Focal : `2.3.1-9ubuntu1.9+esm3`. |
| Applicabilité à votre environnement | Le paquet est concerné, mais son rôle est inattendu sur ce serveur d'échange. L'inventaire antérieur montrait CUPS local ; le rapport ne prouve pas son exposition sur Internet. Le besoin métier, l'état du daemon, son écoute et la version exacte restent à vérifier. |
| Statut | **Confirmé** pour le paquet vulnérable ; exposition et utilité **à vérifier** |
| Justification | Le contrôle local et l'avis Ubuntu concordent. La priorité dépend davantage de l'activation et de l'utilité de CUPS que du seul score. |

### Constat G05

| Élément analysé | Analyse |
| --- | --- |
| Constat Greenbone | `Weak MAC Algorithm(s) Supported (SSH)`, résultats `99a15602-6911-47dc-a035-a408f106761d` dans A et `42c95623-8854-4aae-8eeb-8942f56eafd1` dans B |
| Service ou composant concerné | OpenSSH sur TCP 22 |
| CVE associée, si applicable | Sans objet : défaut de configuration cryptographique, pas une CVE précise |
| CVSS, si disponible | CVSS v2 : **2,6**, `AV:N/AC:H/Au:N/C:P/I:N/A:N` — valeur du VT Greenbone |
| Ce que Greenbone a effectivement observé | Le serveur accepte au moins un MAC classé faible par le VT lors de la négociation SSH distante. VT/OID `1.3.6.1.4.1.25623.1.0.105610`, QoD **80 %**. Le rapport anonymisé ne conserve pas le nom de l'algorithme. |
| Informations vérifiées dans l’entrée CVE et ses références | Le VT classe comme faibles les MAC fondés sur MD5, tronqués à 96 ou 64 bits, ainsi que `none`, et recommande de désactiver les algorithmes signalés. Aucune entrée CVE n'est associée. |
| Applicabilité à votre environnement | Le même résultat a été obtenu dans les deux scans sur le port 22 réellement accessible. Il faut relever la liste exacte avec la configuration effective d'OpenSSH et une nouvelle négociation avant toute modification. |
| Statut | **Confirmé** pour l'acceptation d'un MAC faible ; algorithme exact **à vérifier** |
| Justification | Observation distante répétée et indépendante de l'authentification. L'absence du détail exact dans l'export interdit de désigner ou supprimer un algorithme précis à ce stade. |

## Preuves à conserver

- État du scanner et des feeds avant lancement ; paramètres et portée des deux tâches.
- Rapports A et B terminés, dates, durées, versions des feeds et filtres d'export.
- Résultat du test SSH et preuve d'authentification du scan B, sans clé privée ni phrase secrète.
- Comparaison à l'inventaire et cinq fiches qualifiées, avec leurs sources.

Les rapports complets peuvent contenir des informations internes : les garder
dans le dossier de preuves privé et publier seulement les extraits nécessaires.

## Ressources

- [Greenbone Community Containers](https://greenbone.github.io/docs/latest/22.4/container/index.html).
- [Manuel officiel des scans et de l'authentification SSH](https://docs.greenbone.net/GSM-Manual/gos-24.10/en/scanning.html).
- [CVE.org](https://www.cve.org/).
- Ressources complémentaires fournies par le formateur : [Vulnerability Scanning with OpenVAS](https://medtrigui.github.io/vulnerability-scanning/openvas-vulnerability-scanning/) et [Set Up OpenVAS Vulnerability Scanning in 12 Steps](https://futuretweets.com/set-up-openvas-vulnerability-scanning-2026/). Pour ce laboratoire déjà conteneurisé, suivre la documentation officielle et conserver le projet existant.

- [Activité précédente — Observer la cible](observer-cible.md)
- [Retour à l'itération 1](index.md)
- [Pense-bête de l'itération](../../pense-bete/glossaire/securisation-avancee-infrastructures/it-1.md)
- [Dossier de preuves](../dossier-preuves.md)
