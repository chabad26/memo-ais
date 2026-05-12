# Commandes Linux

## Le terminal

Le terminal est une **console** dans laquelle on saisit des commandes.

Une commande est une suite de caractères qui permet d'exécuter une action.

Exemple :

- `rm` pour supprimer,
- `cd` pour changer de dossier,
- `ls` pour afficher le contenu d'un dossier.

## Quelques commandes de base

| Commande | Rôle |
| -------- | ---- |
| `rm` | Supprimer un fichier ou un dossier |
| `cd` | Changer de répertoire |
| `ls` | Voir les répertoires et les fichiers |
| `pwd` | Afficher le chemin du répertoire courant |
| `sudo` | Exécuter une commande avec des privilèges élevés |

!!! warning "`sudo`"
    `sudo`, c'est un peu le bouton **j'ai les pouvoirs maintenant**. Très pratique, mais à manier sans faire danser la tronçonneuse dans la salle des serveurs.

## Détails utiles

### `pwd`

Affiche le dossier dans lequel on se trouve actuellement.

Exemple :

```bash
pwd
```

### `ls`

Affiche les fichiers et dossiers présents dans le répertoire courant.

Exemple :

```bash
ls
```

### `cd`

Permet de se déplacer dans l'arborescence des dossiers.

Exemple :

```bash
cd Documents
```

### `rm`

Permet de supprimer un fichier ou un dossier.

Exemple :

```bash
rm fichier.txt
```

### `sudo`

Permet d'exécuter une commande avec les droits administrateur.

Exemple :

```bash
sudo apt update
```

## Utilisateur, sudo et root

Un utilisateur Linux peut ouvrir une session et utiliser les applications auxquelles il a accès.

Quand il a besoin de privilèges supplémentaires, il peut utiliser `sudo`.

Cela permet par exemple de :

- supprimer certains fichiers système,
- installer des logiciels,
- modifier la configuration du système.

### Root

`root` est le **super-utilisateur**.

Il possède tous les droits sur la machine.

En pratique :

- un utilisateur classique a des droits limités,
- `sudo` permet de lancer ponctuellement une commande avec plus de droits,
- `root` a tous les droits, tout le temps.

!!! danger "Root"
    Avec `root`, on peut presque tout faire. Le problème, c'est qu'on peut aussi presque tout casser.

## Commandes utiles pour l'AIS

Dans la vie d'un AIS, on utilise souvent le terminal pour observer l'état d'une machine, comprendre un problème, vérifier le réseau ou lire des logs.

### Se repérer dans le système

| Commande | Rôle |
| -------- | ---- |
| `whoami` | Afficher l'utilisateur actuel |
| `hostname` | Afficher le nom de la machine |
| `date` | Afficher la date et l'heure |
| `uptime` | Voir depuis combien de temps la machine est allumée |
| `uname -a` | Afficher des informations sur le système et le kernel |
| `history` | Afficher l'historique des commandes utilisées |

Exemple :

```bash
whoami
hostname
uname -a
```

### Explorer les fichiers

| Commande | Rôle |
| -------- | ---- |
| `cat fichier` | Afficher tout le contenu d'un fichier |
| `less fichier` | Lire un fichier page par page |
| `head fichier` | Afficher le début d'un fichier |
| `tail fichier` | Afficher la fin d'un fichier |
| `tail -f fichier` | Suivre un fichier en direct |
| `find` | Rechercher un fichier ou un dossier |
| `grep` | Rechercher du texte dans un fichier |

Exemples :

```bash
less /var/log/syslog
tail -f /var/log/syslog
grep "error" /var/log/syslog
find /etc -name "*.conf"
```

!!! tip "`less`"
    Dans `less`, on quitte avec la touche `q`.

### Copier, déplacer et créer

| Commande | Rôle |
| -------- | ---- |
| `cp` | Copier un fichier ou un dossier |
| `mv` | Déplacer ou renommer un fichier |
| `mkdir` | Créer un dossier |
| `touch` | Créer un fichier vide ou mettre à jour sa date |
| `nano` | Modifier un fichier simplement dans le terminal |

Exemples :

```bash
mkdir sauvegarde
cp fichier.txt sauvegarde/
mv ancien-nom.txt nouveau-nom.txt
nano notes.txt
```

### Voir l'espace disque et la mémoire

| Commande | Rôle |
| -------- | ---- |
| `df -h` | Voir l'espace disponible sur les disques |
| `du -sh dossier` | Voir la taille d'un dossier |
| `free -h` | Voir l'utilisation de la mémoire RAM |
| `lsblk` | Voir les disques et partitions |

Exemples :

```bash
df -h
du -sh /var/log
free -h
lsblk
```

### Processus et ressources

| Commande | Rôle |
| -------- | ---- |
| `ps aux` | Afficher les processus en cours |
| `top` | Surveiller les processus en temps réel |
| `htop` | Version plus lisible de `top`, si installée |
| `kill PID` | Arrêter un processus avec son identifiant |

Exemples :

```bash
ps aux
top
kill 1234
```

!!! warning "`kill`"
    Avant d'arrêter un processus, il faut vérifier à quoi il correspond. Sur un serveur, arrêter le mauvais service peut provoquer une panne.

### Réseau

| Commande | Rôle |
| -------- | ---- |
| `ip a` | Afficher les interfaces réseau et les adresses IP |
| `ip route` | Afficher les routes et la passerelle |
| `ping` | Tester la connectivité réseau |
| `ss -tulpn` | Voir les ports en écoute |
| `curl` | Tester une URL ou une API |
| `dig` | Interroger le DNS, si la commande est installée |
| `traceroute` | Voir le chemin réseau vers une destination, si installé |

Exemples :

```bash
ip a
ip route
ping 8.8.8.8
ping google.com
ss -tulpn
curl https://example.com
dig google.com
```

### Services et démarrage

Sur beaucoup de distributions Linux modernes, les services sont gérés avec `systemctl`.

| Commande | Rôle |
| -------- | ---- |
| `systemctl status service` | Voir l'état d'un service |
| `sudo systemctl start service` | Démarrer un service |
| `sudo systemctl stop service` | Arrêter un service |
| `sudo systemctl restart service` | Redémarrer un service |
| `sudo systemctl enable service` | Activer un service au démarrage |
| `sudo systemctl disable service` | Désactiver un service au démarrage |

Exemple avec SSH :

```bash
systemctl status ssh
sudo systemctl restart ssh
```

### Logs

Les logs permettent de comprendre ce qu'il s'est passé sur une machine.

| Commande | Rôle |
| -------- | ---- |
| `journalctl` | Lire les logs gérés par systemd |
| `journalctl -xe` | Afficher les erreurs récentes avec du contexte |
| `journalctl -u service` | Voir les logs d'un service précis |
| `dmesg` | Afficher les messages du kernel |

Exemples :

```bash
journalctl -xe
journalctl -u ssh
dmesg
```

### Paquets et mises à jour

Sur Debian, Ubuntu et leurs dérivés, on utilise souvent `apt`.

| Commande | Rôle |
| -------- | ---- |
| `sudo apt update` | Mettre à jour la liste des paquets |
| `sudo apt upgrade` | Installer les mises à jour disponibles |
| `sudo apt install paquet` | Installer un logiciel |
| `sudo apt remove paquet` | Supprimer un logiciel |
| `apt search paquet` | Rechercher un paquet |

Exemples :

```bash
sudo apt update
sudo apt install curl
apt search openssh
```

### Droits et propriétaires

| Commande | Rôle |
| -------- | ---- |
| `ls -l` | Voir les droits et propriétaires |
| `chmod` | Modifier les droits |
| `chown` | Modifier le propriétaire |
| `groups` | Voir les groupes de l'utilisateur |

Exemples :

```bash
ls -l
chmod 600 fichier.txt
sudo chown user:user fichier.txt
groups
```

!!! note "Exemple de droit"
    `chmod 600 fichier.txt` signifie que seul le propriétaire peut lire et modifier le fichier.

## Réflexes utiles

- Lire le message d'erreur avant de relancer une commande.
- Vérifier le dossier courant avec `pwd`.
- Utiliser `ls -l` pour voir les droits.
- Tester le réseau avec `ping`, `ip a` et `ip route`.
- Consulter les logs avec `journalctl` quand un service ne fonctionne pas.
- Faire attention aux commandes lancées avec `sudo`.
