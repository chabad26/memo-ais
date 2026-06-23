# Carnet de bord itération 2

## Objectif du carnet

Ce carnet de bord centralise les preuves et justifications de l'itération 2 :

- permissions POSIX avec `chmod` et `chown` ;
- ACL avec `setfacl` et `getfacl` ;
- recherche et interprétation d'événements dans les logs.

Il doit pouvoir être relu par une personne qui n'était pas présente pendant les manipulations.

## En-tête standard

À compléter :

```text
Nom : HIMBLOT
Prénom : Olivier
Site : AlpesNet
Module : Administration des systèmes - Linux
Itération : IT-2 - Permissions, ACL et logs
Date : 23 juin 2026
Machine : srv-oliv
Distribution : Debian GNU/Linux 12 (bookworm)
```

## Partie 1 - Permissions POSIX sur /srv/alpesnet

### Commandes exécutées

```bash
sudo mkdir -p /srv/alpesnet/{projets,logs,secrets,web}
sudo chown alice.martin:devops /srv/alpesnet/projets
sudo chown root:root /srv/alpesnet/secrets
sudo chown www-nginx:www-nginx /srv/alpesnet/web
sudo chown root:adm /srv/alpesnet/logs
sudo chmod 750 /srv/alpesnet/projets
sudo chmod 700 /srv/alpesnet/secrets
sudo chmod 755 /srv/alpesnet/web
sudo chmod 750 /srv/alpesnet/logs
ls -la /srv/alpesnet/
```

### Résultat attendu

La commande suivante doit montrer les quatre répertoires avec les bons propriétaires et permissions :

```bash
ls -la /srv/alpesnet/
```

À coller ici :

```text
[Coller ici la sortie de ls -la /srv/alpesnet/]
```

### Justification des permissions

| Répertoire | Propriétaire:groupe | Mode | Justification |
| --- | --- | --- | --- |
| `/srv/alpesnet/projets` | `alice.martin:devops` | `750` | Alice administre les projets, le groupe `devops` peut lire et traverser, les autres n'ont aucun droit. |
| `/srv/alpesnet/secrets` | `root:root` | `700` | Répertoire sensible réservé à `root`. Aucun autre compte ne doit lire ou entrer. |
| `/srv/alpesnet/web` | `www-nginx:www-nginx` | `755` | Le service web possède le contenu. Les autres peuvent lire/traverser, mais pas écrire. |
| `/srv/alpesnet/logs` | `root:adm` | `750` | `root` administre les logs, le groupe `adm` peut consulter, les autres sont exclus. |

### Test de sécurité

Commande :

```bash
sudo touch /srv/alpesnet/secrets/test-secret.txt
sudo chmod 600 /srv/alpesnet/secrets/test-secret.txt
sudo -u bob.dupont cat /srv/alpesnet/secrets/test-secret.txt
```

À coller ici :

```text
cat: /srv/alpesnet/secrets/test-secret.txt: Permission non accordée
```

Conclusion :

```text
bob.dupont ne peut pas lire le fichier secret. Le principe du moindre privilège est respecté.
```

## Partie 2 - ACL sur projets et logs

### Commandes exécutées partie 2

```bash
sudo setfacl -m u:bob.dupont:rx /srv/alpesnet/projets
getfacl /srv/alpesnet/projets

sudo setfacl -m g:readonly:r-x /srv/alpesnet/logs
getfacl /srv/alpesnet/logs

sudo setfacl -d -m u:bob.dupont:rx /srv/alpesnet/projets

sudo mkdir -p /backup
sudo getfacl -R /srv/alpesnet > /tmp/acl-alpesnet-$(date +%Y%m%d).txt
sudo cp /tmp/acl-alpesnet-$(date +%Y%m%d).txt /backup/
ls -l /backup/acl-alpesnet-*.txt
```

### Sortie getfacl pour /srv/alpesnet/projets

Commande :

```bash
getfacl /srv/alpesnet/projets
```

À coller ici :

```text
oliv@srv-oliv:~$ getfacl /srv/alpesnet/projets
getfacl : suppression du premier « / » des noms de chemins absolus
# file: srv/alpesnet/projets
# owner: alice.martin
# group: devops
user::rwx
user:bob.dupont:r-x
group::r-x
mask::r-x
other::---
default:user::rwx
default:user:bob.dupont:r-x
default:group::r-x
default:mask::r-x
default:other::---
```

Interprétation attendue :

```text
La ligne user:bob.dupont:r-x indique que bob.dupont peut lire et traverser le répertoire projets.
Il ne possède pas le droit w, donc il ne peut pas créer, modifier ou supprimer de fichiers dans ce répertoire.
```

### Test bob.dupont sur projets

Commandes :

```bash
su - bob.dupont
ls /srv/alpesnet/projets
touch /srv/alpesnet/projets/test-bob.txt
exit
```

À coller ici :

```text
oliv@srv-oliv:~$ su - bob.dupont
Mot de passe : 
bob.dupont@srv-oliv:~$ ls /srv/alpesnet/projets
projet-alpha.txt  projet-beta.txt
bob.dupont@srv-oliv:~$ touch /srv/alpesnet/projets/test-bob.txt
touch: impossible de faire un touch '/srv/alpesnet/projets/test-bob.txt': Permission non accordée
bob.dupont@srv-oliv:~$ exit
déconnexion
oliv@srv-oliv:~$ 
```

Conclusion :

```text
bob.dupont peut lister /srv/alpesnet/projets mais ne peut pas y écrire.
```

### Sortie getfacl pour /srv/alpesnet/logs

Commande :

```bash
getfacl /srv/alpesnet/logs
```

À coller ici :

```text
oliv@srv-oliv:~$ getfacl /srv/alpesnet/logs
getfacl : suppression du premier « / » des noms de chemins absolus
# file: srv/alpesnet/logs
# owner: root
# group: adm
user::rwx
group::r-x
group:readonly:r-x
mask::r-x
other::---

```

Interprétation attendue :

```text
La ligne group:readonly:r-x indique que les membres du groupe readonly peuvent lire et traverser /srv/alpesnet/logs.
Le droit w n'est pas présent, donc le groupe readonly ne peut pas écrire dans ce répertoire.
```

### Test groupe readonly sur logs

Commandes :

```bash
id bob.dupont
su - bob.dupont
ls /srv/alpesnet/logs
touch /srv/alpesnet/logs/test-bob.log
exit
```

À coller ici :

```text

oliv@srv-oliv:~$ id bob.dupont
uid=1002(bob.dupont) gid=1002(readonly) groupes=1002(readonly)
oliv@srv-oliv:~$ su - bob.dupont
Mot de passe : 
bob.dupont@srv-oliv:~$ ls /srv/alpesnet/logs
system.log
bob.dupont@srv-oliv:~$ touch /srv/alpesnet/logs/test-bob.log
touch: impossible de faire un touch '/srv/alpesnet/logs/test-bob.log': Permission non accordée
bob.dupont@srv-oliv:~$ exit
déconnexion
oliv@srv-oliv:~$ 

```

Conclusion :

```text
bob.dupont appartient au groupe readonly. Il peut lire les logs mais ne peut pas écrire dans /srv/alpesnet/logs.
```

### Sauvegarde des ACL

Commande de vérification :

```bash
ls -l /backup/acl-alpesnet-*.txt
```

À coller ici :

```text
oliv@srv-oliv:~$ ls -l /backup/acl-alpesnet-*.txt
-rw-r--r-- 1 root root 1130 23 juin  11:57 /backup/acl-alpesnet-20260623.txt
```

Conclusion :

```text
Les ACL de /srv/alpesnet ont été sauvegardées dans /backup/acl-alpesnet-[date].txt.
```

## Partie 3 - Logs système et journalctl

### Événement 1 - Tentative SSH avec utilisateur inexistant

Commande de recherche :

```bash
journalctl -u ssh --since "5 minutes ago"
```

Ou :

```bash
sudo tail -n 80 /var/log/auth.log
```

Ligne copiée :

```text
2026-06-23T13:51:25.155760+02:00 srv-oliv sudo:     oliv : TTY=pts/0 ; PWD=/home/oliv ; USER=bob.dupont ; COMMAND=/usr/bin/cat /srv/alpesnet/secrets/test-secret.txt
2026-06-23T13:51:25.165431+02:00 srv-oliv sudo: pam_unix(sudo:session): session opened for user bob.dupont(uid=1002) by oliv(uid=1000)
2026-06-23T13:51:25.165458+02:00 srv-oliv sudo: pam_unix(sudo:session): session closed for user bob.dupont
2026-06-23T13:51:57.600146+02:00 srv-oliv su[2117]: (to bob.dupont) oliv on pts/0
2026-06-23T13:51:57.600362+02:00 srv-oliv su[2117]: pam_unix(su-l:session): session opened for user bob.dupont(uid=1002) by oliv(uid=1000)
2026-06-23T13:52:09.134424+02:00 srv-oliv su[2117]: pam_unix(su-l:session): session closed for user bob.dupont
2026-06-23T13:52:46.556428+02:00 srv-oliv su[2138]: (to bob.dupont) oliv on pts/0
2026-06-23T13:52:46.556773+02:00 srv-oliv su[2138]: pam_unix(su-l:session): session opened for user bob.dupont(uid=1002) by oliv(uid=1000)
2026-06-23T13:52:57.884636+02:00 srv-oliv su[2138]: pam_unix(su-l:session): session closed for user bob.dupont
2026-06-23T13:53:31.903626+02:00 srv-oliv sudo:     oliv : TTY=pts/0 ; PWD=/home/oliv ; USER=root ; COMMAND=/usr/bin/journalctl -u ssh --since '5 minutes ago'
2026-06-23T13:53:31.904597+02:00 srv-oliv sudo: pam_unix(sudo:session): session opened for user root(uid=0) by oliv(uid=1000)
2026-06-23T13:53:31.909653+02:00 srv-oliv sudo: pam_unix(sudo:session): session closed for user root
2026-06-23T13:53:39.703272+02:00 srv-oliv sudo:     oliv : TTY=pts/0 ; PWD=/home/oliv ; USER=root ; COMMAND=/usr/bin/tail -n 80 /var/log/auth.log
2026-06-23T13:53:39.704301+02:00 srv-oliv sudo: pam_unix(sudo:session): session opened for user root(uid=0) by oliv(uid=1000)
```

Interprétation :

```text
Date/heure :
Hôte :
Service/programme :
Utilisateur concerné :
Adresse IP source :
Action observée :
Résultat :
Conclusion :
```

### Événement 2 - sudo refusé pour alice.martin

Commande de recherche :

```bash
journalctl --since "5 minutes ago" | grep -i sudo
```

Ou :

```bash
sudo tail -n 80 /var/log/auth.log | grep -i sudo
```

Ligne copiée :

```text
juin 23 13:51:25 srv-oliv sudo[2113]:     oliv : TTY=pts/0 ; PWD=/home/oliv ; USER=bob.dupont ; COMMAND=/usr/bin/cat /srv/alpesnet/secrets/test-secret.txt
juin 23 13:51:25 srv-oliv sudo[2113]: pam_unix(sudo:session): session opened for user bob.dupont(uid=1002) by oliv(uid=1000)
juin 23 13:51:25 srv-oliv sudo[2113]: pam_unix(sudo:session): session closed for user bob.dupont
juin 23 13:53:31 srv-oliv sudo[2149]:     oliv : TTY=pts/0 ; PWD=/home/oliv ; USER=root ; COMMAND=/usr/bin/journalctl -u ssh --since '5 minutes ago'
juin 23 13:53:31 srv-oliv sudo[2149]: pam_unix(sudo:session): session opened for user root(uid=0) by oliv(uid=1000)
juin 23 13:53:31 srv-oliv sudo[2149]: pam_unix(sudo:session): session closed for user root
juin 23 13:53:39 srv-oliv sudo[2153]:     oliv : TTY=pts/0 ; PWD=/home/oliv ; USER=root ; COMMAND=/usr/bin/tail -n 80 /var/log/auth.log
juin 23 13:53:39 srv-oliv sudo[2153]: pam_unix(sudo:session): session opened for user root(uid=0) by oliv(uid=1000)
juin 23 13:53:39 srv-oliv sudo[2153]: pam_unix(sudo:session): session closed for user root
```

Interprétation :

```text
Date/heure :
Hôte :
Programme :
Utilisateur source :
Utilisateur cible :
Commande demandée :
Résultat :
Conclusion :
```

### Événement 3 - Message logger TEST-AUDIT

Commande de recherche :

```bash
journalctl --since "5 minutes ago" | grep "TEST-AUDIT"
```

Ou :

```bash
sudo grep "TEST-AUDIT" /var/log/auth.log /var/log/syslog
```

Ligne copiée :

```text
oliv@srv-oliv:~$ sudo grep "TEST-AUDIT" /var/log/auth.log /var/log/syslog
/var/log/auth.log:2026-06-23T13:27:41.730261+02:00 srv-oliv oliv: TEST-AUDIT alice.martin 2026-06-23
/var/log/auth.log:2026-06-23T13:55:13.819151+02:00 srv-oliv sudo:     oliv : TTY=pts/0 ; PWD=/home/oliv ; USER=root ; COMMAND=/usr/bin/grep TEST-AUDIT /var/log/auth.log /var/log/syslog
```

Interprétation :

```text
Date/heure :
Hôte :
Programme ou utilisateur émetteur :
Priorité/facility si visible :
Message :
Compte mentionné :
Conclusion :
```

## Partie 4 - Politique rsyslog et logrotate AlpesNet

### Preuve 1 - Répertoire de logs dédié

Commande :

```bash
ls -ld /var/log/alpesnet
```

À coller ici :

```text
[Coller ici la sortie de ls -ld /var/log/alpesnet]
```

Interprétation :

```text
Le répertoire /var/log/alpesnet existe. Il appartient à root:adm et ses permissions limitent l'accès aux administrateurs et au groupe adm.
```

### Preuve 2 - Validation de la configuration rsyslog

Commande :

```bash
sudo rsyslogd -N1
```

À coller ici :

```text
[Coller ici la sortie de sudo rsyslogd -N1]
```

Interprétation :

```text
La configuration rsyslog est syntaxiquement valide. La règle /etc/rsyslog.d/50-alpesnet-ssh.conf peut être chargée par le service.
```

### Preuve 3 - Message de test dans le log SSH dédié

Commande :

```bash
sudo tail -n 20 /var/log/alpesnet/ssh-auth.log
```

À coller ici :

```text
[Coller ici les lignes contenant TEST-RSYSLOG]
```

Interprétation :

```text
Le message TEST-RSYSLOG apparaît dans /var/log/alpesnet/ssh-auth.log. La règle rsyslog route bien les messages du programme sshd vers le fichier dédié AlpesNet.
```

### Preuve 4 - Simulation logrotate sans erreur

Commande :

```bash
sudo logrotate -d /etc/logrotate.d/alpesnet-ssh
```

À coller ici :

```text
[Coller ici la sortie de simulation logrotate]
```

Interprétation :

```text
La simulation logrotate ne signale pas d'erreur bloquante. La politique /etc/logrotate.d/alpesnet-ssh est lisible et prise en compte.
```

### Preuve 5 - Fichiers présents après rotation

Commande :

```bash
ls -l /var/log/alpesnet/
```

À coller ici :

```text
[Coller ici la liste des fichiers dans /var/log/alpesnet/]
```

Interprétation :

```text
Le fichier ssh-auth.log et ses fichiers de rotation sont présents. La rotation forcée a bien créé des fichiers historiques et rsyslog peut continuer à écrire dans le fichier courant.
```

## Conclusion générale

```text
Les permissions POSIX de /srv/alpesnet sont configurées selon le moindre privilège.
Les ACL ajoutent des droits précis pour bob.dupont et le groupe readonly sans modifier les propriétaires POSIX.
Les événements de sécurité provoqués sont retrouvables dans les logs et peuvent être interprétés.
La politique rsyslog/logrotate dédiée à SSH route les messages vers un fichier AlpesNet et prévoit leur rotation pour éviter le remplissage de /var.
```
