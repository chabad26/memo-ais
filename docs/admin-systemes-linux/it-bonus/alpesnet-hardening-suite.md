# Projet bonus - AlpesNet Hardening Suite

## Objectif

Le projet consiste à construire une suite de scripts Bash capable de préparer, durcir, auditer et sauvegarder un serveur Debian 12 fraîchement installé.

L'idée n'est pas de lancer une suite de commandes au hasard. On veut un outil reproductible : un administrateur clone le dossier, adapte la configuration, lance `main.sh`, puis obtient un serveur configuré avec un rapport lisible.

Le script complet est disponible ici :

[hardening-suite/main.sh](../../assets/scripts/admin-systemes-linux/it-bonus/hardening-suite/main.sh)

## Étape 1 - Comprendre l'architecture

La suite est organisée en modules indépendants :

```text
hardening-suite/
  main.sh
  modules/
    01-systeme.sh
    02-utilisateurs.sh
    03-ssh.sh
    04-firewall.sh
    05-services.sh
    06-logs.sh
    07-sauvegarde.sh
    08-audit.sh
    _common.sh
  config/
    alpesnet.conf
  rapports/
  README.md
```

`main.sh` est le point d'entrée unique. Il vérifie l'environnement, charge la configuration, empêche deux exécutions simultanées, contrôle les dépendances entre modules, mesure les durées et affiche un récapitulatif final.

## Étape 2 - Adapter la configuration

Le fichier à modifier avant exécution est :

[alpesnet.conf](../../assets/scripts/admin-systemes-linux/it-bonus/hardening-suite/config/alpesnet.conf)

Les points à vérifier en priorité :

| Variable | Pourquoi |
| --- | --- |
| `SSH_ALLOW_USERS` | éviter de couper son propre accès SSH |
| `UFW_RULES` | autoriser seulement les ports nécessaires |
| `COMPTES` | créer les comptes attendus et les comptes service |
| `SERVICES_AUTORISES` | définir les services qui doivent rester actifs |
| `BACKUP_DIRS` | choisir les dossiers à sauvegarder |

!!! warning "Anti auto-blocage SSH"
    Si le module SSH est lancé, indiquer explicitement le compte à conserver autorisé :

    ```bash
    sudo ./main.sh --all --sshuser oliv
    ```

    L'argument `--sshuser` remplace temporairement `SSH_ALLOW_USERS` pendant l'exécution. Il évite de rester bloqué avec une valeur générique comme `adm-prenom`.

    Si `--sshuser` n'est pas fourni et que la configuration contient une valeur vide ou générique (`adm-prenom`, `adm-[prenom]`, `CHANGE_ME`), le script demande automatiquement quel utilisateur SSH doit rester autorisé. En mode non interactif, il refuse de continuer et demande de relancer avec `--sshuser`.

## Étape 3 - Faire un dry-run

Le dry-run permet de vérifier l'enchaînement sans modifier la machine.

```bash
cd hardening-suite
sudo ./main.sh --all --dry-run --sshuser oliv
```

Le script doit afficher les modules exécutés, les statuts et les durées. En dry-run, les commandes sont journalisées mais simulées.

## Étape 4 - Utiliser le menu

Pour éviter de devoir deviner les noms des modules, lancer :

```bash
sudo ./main.sh --menu
```

Le menu affiche les modules et demande le compte SSH à conserver si le module `03-ssh` est sélectionné et que `--sshuser` n'a pas déjà été fourni.

Il affiche :

```text
01  Mise a jour systeme et outils de base
02  Comptes, groupes et sudo restreint
03  Durcissement SSH
04  Pare-feu UFW et Fail2ban
05  Services inutiles et ports ouverts
06  Rsyslog et logrotate SSH
07  Rsync, cron et checksum
08  Rapport d'audit PASS/FAIL/WARN
```

Choix possibles :

| Choix | Effet |
| --- | --- |
| `all` | lance tous les modules |
| `audit` | lance seulement le module 08 |
| `dry-run` | active ou désactive le mode simulation |
| `1 2 3` | lance les modules 01, 02 et 03 |
| `01,02,03` | même chose, au format liste |
| `q` | quitte sans rien lancer |

## Étape 5 - Lancer seulement quelques modules

Pour tester progressivement :

```bash
sudo ./main.sh --modules 01,02
sudo ./main.sh --modules 03,04,08 --sshuser oliv
sudo ./main.sh --audit-only
```

Même avec `--modules`, les dépendances restent appliquées. Par exemple, `04-firewall` ne s'exécute pas si `03-ssh` n'a pas le statut `OK` dans la run en cours.

## Étape 6 - Module 01 : système

Le module met à jour Debian et installe les outils listés dans `OUTILS_BASE`.

Actions principales :

- `apt-get update` ;
- `apt-get upgrade -y` ;
- installation des paquets définis dans la configuration ;
- journalisation du nombre de paquets qui étaient disponibles avant la mise à jour.

Validation :

```bash
dpkg -l ufw fail2ban rsyslog logrotate rsync nginx
```

## Étape 7 - Module 02 : utilisateurs et sudo

Le module crée les groupes et comptes définis dans `alpesnet.conf`. Il reste idempotent : un compte existant n'est pas recréé, il est seulement réaligné.

Contrôles obligatoires :

- aucun compte non-root avec UID `0` ;
- aucune règle `NOPASSWD: ALL` dans sudoers ;
- sudo restreint pour le groupe prévu.

Validation :

```bash
getent passwd alice.martin
getent group devops
sudo visudo -cf /etc/sudoers.d/alpesnet-devops
```

## Étape 8 - Module 03 : SSH

Le module écrit un fichier dédié :

```text
/etc/ssh/sshd_config.d/99-alpesnet-hardening.conf
```

Il applique les paramètres `PermitRootLogin`, `PasswordAuthentication`, `AllowUsers`, `MaxAuthTries` et `LoginGraceTime`, puis valide la syntaxe avec :

```bash
sudo sshd -t
```

SSH n'est rechargé que si ce test réussit.

## Étape 9 - Module 04 : UFW et Fail2ban

Le module applique une politique entrante restrictive, ajoute les règles UFW depuis `UFW_RULES`, active UFW, configure la jail SSH Fail2ban et vérifie les services.

Validation :

```bash
sudo ufw status verbose
sudo fail2ban-client status sshd
```

## Étape 10 - Module 05 : services inutiles

Le module capture les ports et services actifs avant/après, compare les services actifs à `SERVICES_AUTORISES`, puis désactive les services non autorisés.

En mode interactif (`MODE_INTERACTIF=1` dans la configuration), il demande confirmation avant chaque désactivation.

Preuves générées :

```text
/tmp/alpesnet-services-avant.txt
/tmp/alpesnet-ports-avant.txt
/tmp/alpesnet-ports-apres.txt
```

## Étape 11 - Module 06 : logs

Le module configure rsyslog et logrotate pour les événements SSH AlpesNet.

Fichiers créés :

```text
/etc/rsyslog.d/30-alpesnet-ssh.conf
/etc/logrotate.d/alpesnet-ssh
```

Validation :

```bash
sudo rsyslogd -N1
sudo logrotate -d /etc/logrotate.d/alpesnet-ssh
```

## Étape 12 - Module 07 : sauvegarde

Le module sauvegarde les répertoires listés dans `BACKUP_DIRS`, génère un checksum SHA-256 et installe une tâche cron.

Fichiers importants :

```text
/usr/local/sbin/alpesnet-backup.sh
/etc/cron.d/alpesnet-backup
/backup/alpesnet-[date]/checksums.sha256
```

Validation :

```bash
sudo ls -lh /backup/
sudo cat /etc/cron.d/alpesnet-backup
```

## Étape 13 - Module 08 : audit

Le module ne modifie pas la configuration. Il vérifie l'état final et génère :

```text
rapports/audit-[hostname]-[date].txt
```

Le rapport contient :

- l'en-tête machine : hostname, IP, date, OS, durée totale ;
- les comptes avec shell actif, UID 0 et membres sudo ;
- les paramètres SSH actifs ;
- l'état UFW et Fail2ban ;
- les ports et services actifs ;
- les validations rsyslog et logrotate ;
- l'état des sauvegardes ;
- les durées de modules ;
- un score `PASS`, `FAIL`, `WARN`.

## Étape 14 - Lancer la démonstration complète

Avant de lancer, faire un snapshot VirtualBox et vérifier l'utilisateur autorisé en SSH.

```bash
sudo ./main.sh --all --sshuser oliv
```

Résultat attendu :

- le script va jusqu'au bout ;
- un rapport d'audit est créé ;
- un second lancement reste cohérent ;
- le récapitulatif final affiche les statuts et durées ;
- le verrou bloque un deuxième lancement parallèle ;
- si `03-ssh` échoue, `04-firewall` est sauté.

## Étape 15 - Vérifier la syntaxe

Depuis le dossier `hardening-suite` :

```bash
bash -n main.sh modules/*.sh
```

Cette commande doit retourner sans erreur.

## Points de vigilance

Ne jamais désactiver l'authentification par mot de passe SSH sans avoir testé une connexion par clé dans un autre terminal.

Ne jamais activer UFW sans avoir vérifié que le sous-réseau d'administration est autorisé.

Toujours relancer le script une deuxième fois : l'idempotence se vérifie surtout au second passage.
