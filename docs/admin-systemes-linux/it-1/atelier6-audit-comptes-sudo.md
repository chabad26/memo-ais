# Atelier 6 - Audit des comptes et des droits sudo AlpesNet

## Contexte

Le DSI d'AlpesNet transmet le message suivant :

> Notre serveur a été configuré il y a 6 mois par un prestataire qui n'est plus joignable. Avant de le mettre en production, j'ai besoin d'un audit complet des comptes et des droits sudo. Je veux savoir qui peut faire quoi et si c'est normal.

L'objectif n'est pas seulement d'exécuter des commandes. Il faut analyser, décider si l'état observé est normal, corriger les écarts, puis produire un rapport lisible par une personne qui n'était pas présente pendant l'audit.

## Objectif

Réaliser un audit complet des comptes locaux et des droits `sudo` sur la VM AlpesNet.

À la fin de l'atelier, tu dois savoir :

- lister les comptes avec un shell actif ;
- repérer un compte anormal avec UID `0` ;
- contrôler les comptes service `www-nginx` et `backup-agent` ;
- vérifier les droits `sudo` compte par compte ;
- corriger les écarts de configuration ;
- documenter l'état initial, les corrections et l'état final.

## Règles de sécurité

!!! warning "Avant de corriger"
    Toujours noter l'état observé avant modification. Un audit sans trace avant/après ne permet pas de justifier les corrections.

!!! danger "UID 0"
    Tout compte autre que `root` avec UID `0` est une anomalie critique. Il possède les mêmes privilèges système que `root`, même si son nom semble inoffensif.

## Étape 1 - Préparer le fichier de rapport

Créer un fichier texte dédié au rapport :

```bash
nano audit-comptes-sudo-alpesnet.txt
```

Ajouter l'en-tête standard :

```text
Nom :
Prénom :
Site :
Module : Administration des systèmes - Linux
Atelier : Audit des comptes et des droits sudo AlpesNet
Date :
Machine : srv-[prenom]
Distribution : Debian GNU/Linux 12 (bookworm)
Objet : Audit des comptes locaux, UID 0, comptes service et droits sudo
```

Point de contrôle : le rapport doit être compréhensible sans captures d'écran obligatoires. Les commandes, résultats importants et décisions doivent être écrits dans le fichier.

## Étape 2 - Identifier la distribution et la machine

Relever le contexte technique :

```bash
hostnamectl
cat /etc/os-release
whoami
date
```

À documenter :

- nom de la machine ;
- distribution ;
- utilisateur qui réalise l'audit ;
- date de l'audit.

## Étape 3 - Sauvegarder les fichiers sensibles avant audit

Créer un dossier de travail local :

```bash
mkdir -p ~/audit-alpesnet
```

Sauvegarder les fichiers utiles :

```bash
sudo cp /etc/passwd ~/audit-alpesnet/passwd.avant
sudo cp /etc/group ~/audit-alpesnet/group.avant
sudo cp /etc/sudoers ~/audit-alpesnet/sudoers.avant
sudo cp -R /etc/sudoers.d ~/audit-alpesnet/sudoers.d.avant
```

Vérifier :

```bash
ls -l ~/audit-alpesnet
```

Point de contrôle : les fichiers `.avant` doivent exister. Ils servent de preuve si une correction doit être justifiée.

## Étape 4 - Lister tous les comptes avec un shell actif

Afficher les shells considérés comme interactifs :

```bash
awk -F: '$7 !~ /(nologin|false|sync)$/ {print $1, "UID="$3, "HOME="$6, "SHELL="$7}' /etc/passwd
```

Version plus détaillée :

```bash
awk -F: '$7 !~ /(nologin|false|sync)$/ {printf "%-20s UID=%-5s HOME=%-25s SHELL=%s\n",$1,$3,$6,$7}' /etc/passwd
```

Pour chaque compte affiché, vérifier s'il est légitime :

```bash
id root
id alice.martin
id bob.dupont
```

Point de contrôle attendu :

- `root` peut avoir `/bin/bash`, mais son usage doit rester exceptionnel ;
- les utilisateurs humains légitimes peuvent avoir `/bin/bash` ;
- les comptes service ne doivent pas apparaître dans cette liste ;
- tout compte inconnu avec shell actif doit être étudié.

À documenter dans le rapport :

| Compte | UID | Home | Shell | Légitime ? | Justification |
| --- | --- | --- | --- | --- | --- |
| `root` | `0` | `/root` | `/bin/bash` | Oui | Compte administrateur système |
| `alice.martin` | à relever | `/home/alice.martin` | `/bin/bash` | Oui | Lead DevOps AlpesNet |
| `bob.dupont` | à relever | `/home/bob.dupont` | `/bin/bash` | À décider | Compte humain, vérifier s'il est encore actif |

## Étape 5 - Vérifier qu'aucun compte hors root n'a UID 0

Lister tous les comptes avec UID `0` :

```bash
awk -F: '($3==0){print $1, "UID="$3, "GID="$4, "HOME="$6, "SHELL="$7}' /etc/passwd
```

Point de contrôle attendu :

```text
root UID=0 GID=0 HOME=/root SHELL=/bin/bash
```

Si un autre compte apparaît, relever l'écart dans le rapport :

```text
Écart critique : le compte [nom] possède UID 0. Il dispose des privilèges root.
```

Correction possible si le compte doit être conservé :

```bash
sudo usermod -u 1001 nom_du_compte
sudo groupmod -g 1001 nom_du_compte
```

Correction possible si le compte est illégitime et doit être désactivé :

```bash
sudo usermod -L nom_du_compte
sudo usermod -s /usr/sbin/nologin nom_du_compte
```

Vérifier après correction :

```bash
awk -F: '($3==0){print $1, "UID="$3}' /etc/passwd
```

Point de contrôle final : seul `root` doit apparaître.

## Étape 6 - Vérifier les comptes service

Contrôler les comptes `www-nginx` et `backup-agent` :

```bash
getent passwd www-nginx backup-agent
id www-nginx
id backup-agent
```

Vérifier le shell :

```bash
getent passwd www-nginx backup-agent | awk -F: '{print $1, "HOME="$6, "SHELL="$7}'
```

Vérifier l'absence de home actif :

```bash
ls -ld /home/www-nginx /home/backup-agent
```

Résultat attendu :

- shell : `/usr/sbin/nologin` ;
- aucun home actif dans `/home` ;
- UID de type système, généralement inférieur à `1000` sur Debian.

Si un compte service a un shell interactif, corriger :

```bash
sudo usermod -s /usr/sbin/nologin www-nginx
sudo usermod -s /usr/sbin/nologin backup-agent
```

Si un home inutile existe, vérifier avant suppression :

```bash
sudo find /home/www-nginx -maxdepth 2 -ls
sudo find /home/backup-agent -maxdepth 2 -ls
```

Puis désactiver le home dans la fiche du compte :

```bash
sudo usermod -d /nonexistent www-nginx
sudo usermod -d /nonexistent backup-agent
```

!!! note "Suppression d'un home service"
    Ne supprime pas un répertoire sans avoir vérifié son contenu. Dans un audit, on documente d'abord, puis on décide.

Vérifier après correction :

```bash
getent passwd www-nginx backup-agent
```

## Étape 7 - Lister les groupes sensibles

Afficher les membres des groupes d'administration :

```bash
getent group sudo
getent group adm
getent group root
```

Vérifier les groupes de chaque compte AlpesNet :

```bash
id alice.martin
id bob.dupont
id www-nginx
id backup-agent
```

Point de contrôle :

- un utilisateur dans le groupe `sudo` peut souvent obtenir des droits larges selon `/etc/sudoers` ;
- un compte service ne doit pas être dans `sudo` ;
- un compte humain doit avoir uniquement les groupes nécessaires.

Si un compte service est membre de `sudo`, corriger :

```bash
sudo gpasswd -d www-nginx sudo
sudo gpasswd -d backup-agent sudo
```

Vérifier :

```bash
getent group sudo
```

## Étape 8 - Vérifier les droits sudo de chaque compte

Lister les comptes à auditer :

```bash
printf "%s\n" root alice.martin bob.dupont www-nginx backup-agent
```

Vérifier les droits `sudo` compte par compte :

```bash
sudo -l -U root
sudo -l -U alice.martin
sudo -l -U bob.dupont
sudo -l -U www-nginx
sudo -l -U backup-agent
```

Point de contrôle attendu :

- `alice.martin` peut avoir des droits restreints et listés explicitement ;
- `bob.dupont` ne doit pas avoir de droits sudo, sauf justification écrite ;
- `www-nginx` et `backup-agent` ne doivent pas avoir de droits sudo interactifs ;
- aucun compte ne doit avoir une règle dangereuse non justifiée.

## Étape 9 - Rechercher les règles sudo dangereuses

Afficher les règles actives :

```bash
sudo grep -R "NOPASSWD\\|ALL=(ALL:ALL) ALL\\|ALL=(ALL) ALL" /etc/sudoers /etc/sudoers.d
```

Afficher les fichiers sudoers sans commentaires :

```bash
sudo grep -RhvE "^[[:space:]]*#|^[[:space:]]*$" /etc/sudoers /etc/sudoers.d
```

Écart à signaler :

```text
NOPASSWD: ALL
```

ou :

```text
utilisateur ALL=(ALL:ALL) NOPASSWD: ALL
```

Correction : éditer uniquement avec `visudo` :

```bash
sudo visudo -f /etc/sudoers.d/nom_du_fichier
```

Exemple de règle acceptable pour Alice :

```sudoers
alice.martin ALL=(root) /bin/systemctl, /usr/bin/apt, /usr/sbin/useradd, /usr/sbin/usermod, /usr/sbin/userdel, /usr/sbin/groupadd
```

Vérifier la syntaxe :

```bash
sudo visudo -cf /etc/sudoers
sudo visudo -cf /etc/sudoers.d/nom_du_fichier
```

Point de contrôle : `visudo` doit indiquer que la syntaxe est correcte.

## Étape 10 - Corriger les écarts trouvés

Pour chaque écart, utiliser la logique suivante :

| Écart | Risque | Correction possible | Vérification |
| --- | --- | --- | --- |
| Compte inconnu avec shell actif | Connexion interactive non maîtrisée | `sudo usermod -s /usr/sbin/nologin compte` ou verrouillage | `getent passwd compte` |
| Compte hors `root` avec UID `0` | Privilèges root complets | Changer UID ou verrouiller le compte | `awk -F: '($3==0){print $1}' /etc/passwd` |
| Compte service avec `/bin/bash` | Connexion interactive possible | `sudo usermod -s /usr/sbin/nologin compte` | `getent passwd compte` |
| Compte service avec home actif | Surface inutile, fichiers non maîtrisés | `sudo usermod -d /nonexistent compte` après vérification | `getent passwd compte` |
| `NOPASSWD: ALL` | Élévation sans mot de passe | Remplacer par commandes limitées ou supprimer la règle | `sudo -l -U compte` |
| Membre inutile du groupe `sudo` | Droits admin trop larges | `sudo gpasswd -d compte sudo` | `getent group sudo` |

Dans le rapport, documenter chaque correction avec cette forme :

```text
Écart identifié :
Commande de constat :
Risque :
Correction appliquée :
Commande de vérification :
État final :
```

## Étape 11 - Vérification finale globale

Relancer les commandes de contrôle :

```bash
awk -F: '$7 !~ /(nologin|false|sync)$/ {print $1, "UID="$3, "HOME="$6, "SHELL="$7}' /etc/passwd
awk -F: '($3==0){print $1, "UID="$3}' /etc/passwd
getent passwd www-nginx backup-agent
getent group sudo
sudo -l -U alice.martin
sudo -l -U bob.dupont
sudo -l -U www-nginx
sudo -l -U backup-agent
sudo grep -R "NOPASSWD.*ALL" /etc/sudoers /etc/sudoers.d
```

Point de contrôle final :

- seuls les comptes humains légitimes ont un shell interactif ;
- seul `root` possède UID `0` ;
- `www-nginx` et `backup-agent` ont `/usr/sbin/nologin` ;
- les comptes service n'ont pas de home actif ;
- aucun `NOPASSWD: ALL` non justifié n'est présent ;
- les droits sudo restants sont explicitement listés.

## Étape 12 - Produire la fiche de configuration initiale AlpesNet

Créer une fiche séparée :

```bash
nano fiche-configuration-initiale-alpesnet.txt
```

Structure attendue :

```text
FICHE DE CONFIGURATION INITIALE ALPESNET

Nom :
Prénom :
Date :
Machine :

Compte : root
UID :
Shell :
Home :
Groupes :
Droits sudo :
Décision : compte système légitime

Compte : alice.martin
UID :
Shell :
Home :
Groupes :
Droits sudo :
Décision :

Compte : bob.dupont
UID :
Shell :
Home :
Groupes :
Droits sudo :
Décision :

Compte : www-nginx
UID :
Shell :
Home :
Groupes :
Droits sudo :
Décision : compte service, pas de connexion interactive attendue

Compte : backup-agent
UID :
Shell :
Home :
Groupes :
Droits sudo :
Décision : compte service, pas de connexion interactive attendue
```

Commandes utiles pour remplir la fiche :

```bash
getent passwd root alice.martin bob.dupont www-nginx backup-agent
id root
id alice.martin
id bob.dupont
id www-nginx
id backup-agent
sudo -l -U alice.martin
sudo -l -U bob.dupont
sudo -l -U www-nginx
sudo -l -U backup-agent
```

## Livrables L1

Deux fichiers sont attendus.

### Rapport d'audit

Le rapport doit contenir :

- l'en-tête standard ;
- la liste des comptes analysés ;
- les commandes exécutées ;
- les écarts identifiés ;
- les corrections appliquées avec les commandes ;
- l'état final vérifié par commande ;
- une conclusion claire : serveur conforme ou non conforme après correction.

Conclusion type :

```text
Conclusion :
Après audit et corrections, les comptes interactifs sont identifiés, seul root possède UID 0, les comptes service www-nginx et backup-agent sont non interactifs, et aucun NOPASSWD ALL non justifié n'est présent. L'état final est conforme aux attentes AlpesNet.
```

### Fiche de configuration initiale AlpesNet

La fiche doit contenir, pour chaque compte :

- nom du compte ;
- UID ;
- shell ;
- home ;
- groupes ;
- droits sudo ;
- décision ou justification.

## Synthèse à retenir

Un audit de comptes Linux repose sur trois questions simples : qui peut ouvrir une session, qui peut devenir administrateur, et est-ce justifié ?

La partie technique tient en quelques commandes, mais la valeur professionnelle vient de la documentation : constater, corriger, vérifier, puis laisser une trace claire.
