# Pense-bête

## Rappels rapides

- La **carte mère** relie les composants.
- Le **CPU** effectue les calculs.
- La **RAM** stocke temporairement les données.
- Le **HDD/SSD** conserve les données.
- L'**OS** pilote l'ensemble.
- **Linux** est un noyau open source utilisé dans des distributions.
- Le **réseau** relie les machines entre elles.
- Le **DNS** traduit les noms de domaine en adresses IP.
- Le **DHCP** distribue automatiquement les paramètres réseau.
- **SSH** permet un accès distant sécurisé.
- `sudo` donne des privilèges élevés.
- `root` a tous les droits, donc tous les risques.

## Version simple à relire avant un cours

### Le PC

Un ordinateur est composé de plusieurs éléments qui travaillent ensemble :

- la carte mère relie les composants,
- le processeur calcule,
- la RAM garde les données temporaires,
- le disque garde les données sur le long terme.

### Le système

Le système d'exploitation gère l'ensemble.

C'est lui qui fait le lien entre :

- l'utilisateur,
- le matériel,
- les logiciels.

### Linux

Linux est le noyau utilisé par de nombreuses distributions.

Il est open source, ce qui signifie que son code est accessible et modifiable selon sa licence.

### Le réseau

Le réseau sert à faire communiquer les machines entre elles.

Il permet aussi bien :

- l'accès à Internet,
- le partage de fichiers,
- l'impression réseau,
- l'administration distante.

## Besoins courants

### Savoir où on est

Commandes utiles :

```bash
pwd
ls
whoami
hostname
```

- `pwd` indique le dossier courant.
- `ls` affiche les fichiers et dossiers.
- `whoami` indique l'utilisateur connecté.
- `hostname` affiche le nom de la machine.

### Vérifier l'état général d'une machine

```bash
uptime
df -h
free -h
top
```

- `uptime` montre depuis combien de temps la machine est allumée.
- `df -h` affiche l'espace disque disponible.
- `free -h` affiche l'utilisation de la RAM.
- `top` affiche les processus en cours.

### Vérifier le réseau

```bash
ip a
ip route
ping 8.8.8.8
ping google.com
ss -tulpn
```

- `ip a` affiche les adresses IP.
- `ip route` affiche la passerelle et les routes.
- `ping 8.8.8.8` teste la connectivité Internet.
- `ping google.com` teste aussi la résolution DNS.
- `ss -tulpn` affiche les ports en écoute.

!!! tip "Diagnostic réseau rapide"
    Si `ping 8.8.8.8` fonctionne mais pas `ping google.com`, le problème vient probablement du DNS.

### Lire les logs

```bash
journalctl -xe
journalctl -u ssh
tail -f /var/log/syslog
```

- `journalctl -xe` affiche des erreurs récentes avec du contexte.
- `journalctl -u ssh` affiche les logs du service SSH.
- `tail -f` permet de suivre un fichier de log en direct.

### Gérer un service

```bash
systemctl status ssh
sudo systemctl restart ssh
sudo systemctl enable ssh
```

- `status` permet de voir si un service fonctionne.
- `restart` redémarre un service.
- `enable` active un service au démarrage.

### Installer ou mettre à jour

Sur Debian ou Ubuntu :

```bash
sudo apt update
sudo apt upgrade
sudo apt install nom-du-paquet
```

- `apt update` met à jour la liste des paquets.
- `apt upgrade` installe les mises à jour.
- `apt install` installe un logiciel.

### Droits et fichiers

```bash
ls -l
chmod 600 fichier.txt
sudo chown user:user fichier.txt
```

- `ls -l` affiche les droits et propriétaires.
- `chmod` modifie les droits.
- `chown` modifie le propriétaire.

!!! warning "Droits"
    Ne pas mettre des droits trop ouverts comme `777` sans raison précise.

## Réflexes de dépannage

Quand quelque chose ne fonctionne pas, vérifier dans cet ordre :

1. Est-ce que la machine est allumée et accessible ?
2. Est-ce que je suis sur le bon utilisateur ?
3. Est-ce que le réseau fonctionne ?
4. Est-ce que le service est démarré ?
5. Est-ce que les logs indiquent une erreur ?
6. Est-ce que l'espace disque est plein ?
7. Est-ce que les droits bloquent l'accès ?

Commandes utiles pour ce réflexe :

```bash
whoami
ip a
ip route
systemctl status nom-du-service
journalctl -xe
df -h
ls -l
```

## Mini glossaire

| Terme | Signification |
| ----- | ------------- |
| IP | Adresse qui identifie une machine sur un réseau |
| DNS | Service qui traduit un nom de domaine en adresse IP |
| DHCP | Service qui distribue automatiquement les paramètres réseau |
| NAT | Mécanisme qui permet de partager une IP publique entre plusieurs machines privées |
| Port | Numéro qui identifie un service sur une machine |
| Kernel | Noyau du système d'exploitation |
| Processus | Programme en cours d'exécution |
| Service | Programme qui tourne souvent en arrière-plan |
| Log | Trace écrite d'un événement système ou applicatif |
| Root | Super-utilisateur avec tous les droits |

## Sécurité de base

Quelques réflexes simples :

- éviter d'utiliser `root` directement,
- utiliser `sudo` seulement quand c'est nécessaire,
- garder le système à jour,
- ne pas ouvrir de ports inutiles,
- utiliser des mots de passe solides,
- privilégier SSH avec des clés quand c'est possible,
- lire les logs en cas de comportement anormal,
- documenter les changements importants.

!!! info "Phrase à garder en tête"
    Avant de corriger, il faut comprendre. Avant de modifier, il faut vérifier.

## Note perso

Résumé général : les bases vont bien, mais il manque parfois de la précision entre les modules et les compétences.

Ce mémo sert justement à remettre tout ça au clair, morceau par morceau.
