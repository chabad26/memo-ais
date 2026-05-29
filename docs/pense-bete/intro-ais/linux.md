# Pense-bête Linux et commandes

## Savoir où on est

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

## Vérifier l'état général d'une machine

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

## Lire les logs

```bash
journalctl -xe
journalctl -u ssh
tail -f /var/log/syslog
```

- `journalctl -xe` affiche des erreurs récentes avec du contexte.
- `journalctl -u ssh` affiche les logs du service SSH.
- `tail -f` permet de suivre un fichier de log en direct.

## Gérer un service

```bash
systemctl status ssh
sudo systemctl restart ssh
sudo systemctl enable ssh
```

- `status` permet de voir si un service fonctionne.
- `restart` redémarre un service.
- `enable` active un service au démarrage.

## Installer ou mettre à jour

Sur Debian ou Ubuntu :

```bash
sudo apt update
sudo apt upgrade
sudo apt install nom-du-paquet
```

- `apt update` met à jour la liste des paquets.
- `apt upgrade` installe les mises à jour.
- `apt install` installe un logiciel.

## Droits et fichiers

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

Commandes utiles :

```bash
whoami
ip a
ip route
systemctl status nom-du-service
journalctl -xe
df -h
ls -l
```
