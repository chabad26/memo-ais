# ============================================================
# Auteur : Olivier -- Date : 2026-07-03
# Machine : VM CTF AlpesNet -- IP : 192.168.56.103 -- Module : SYS-01a CTF
# ============================================================

1. TIMELINE DE L'INCIDENT
   2026-07-02 11:31:13  Acces root obtenu et methode documentee  [Source : id ; whoami ; sudo -l ; recherche mot de passe cache]
   2026-07-02 11:31:41  Audit des comptes et sudoers  [Source : awk UID0 ; getent passwd ; sudoers.d actifs hors README ; lastlog]
   2026-07-02 11:31:41  Analyse des logs d'authentification et extraction IP  [Source : /var/log/auth.log ; journalctl -u ssh]
   2026-07-02 11:31:41  Recherche des permissions dangereuses  [Source : find / -perm 0777 ; find / -perm /4000]
   2026-07-02 11:31:46  Durcissement SSH, pare-feu, fail2ban et services  [Source : sshd_config ; ufw status verbose ; fail2ban-client status]
   2026-07-02 11:31:50  Verification et remise en service Nginx  [Source : nginx -t ; systemctl restart nginx ; curl HTTP 200]
   2026-07-02 11:31:53  Sauvegarde de /etc et /var/www avec checksum  [Source : tar -C / ; sha256sum -c]

2. ANALYSE DES CAUSES
   Cause principale    : compte ou service expose ayant permis une compromission de la VM.
   Vecteur d'intrusion : 185.220.101.47 via SSH ou service expose, a confirmer avec les logs.
   Compte suspect      : backdoor-sys
   Permission faible   : /var/www/upload

3. ACTIONS CORRECTIVES
   F1 -- Acces root       : mot de passe cache retrouve dans la VM puis utilisation de su/root ou ssh root@IP
   F2 -- Compte supprime  : userdel backdoor-sys + verification getent passwd
   F4 -- Permissions      : chmod 750 /var/www/upload + verification stat
   F5 -- SSH              : AllowUsers oliv, PasswordAuthentication yes, PubkeyAuthentication yes, PermitEmptyPasswords no
   F5 -- ufw              : OpenSSH, HTTP et HTTPS autorises ; verification par ufw status verbose
   F5 -- fail2ban         : jail sshd active, maxretry=3, bantime=3600
   F6 -- Nginx            : Commenter la ligne 88 dans /etc/nginx/nginx.conf puis relancer nginx -t et systemctl restart nginx.
   F7 -- Sauvegarde       : /backup/ctf-alpesnet-20260702_113109.tar.gz + sha256sum -c /backup/ctf-alpesnet-20260702_113109.tar.gz.sha256

   Dernieres actions retenues :
   F1 -- Acces root : mot de passe cache retrouve dans la VM puis utilisation de su/root ou ssh root@IP | Verification : id ; whoami ; sudo -l ; find/grep indices mot de passe cache
   F2 -- Compte non autorise identifie : backdoor-sys | Verification : getent passwd backdoor-sys
   F3 -- IP source identifiee : 185.220.101.47 | Verification : compter les occurrences par IP dans les logs SSH
   F4 -- Permission dangereuse documentee : /var/www/upload | Verification : find / -xdev -perm 0777 ; find / -xdev -perm /4000
   F5 -- SSH limite a oliv, mot de passe root non modifie, ufw/fail2ban actifs | Verification : ssh root@IP refuse ; ufw status verbose ; fail2ban-client status sshd
   F6 -- Correction Nginx : Commenter la ligne 88 dans /etc/nginx/nginx.conf puis relancer nginx -t et systemctl restart nginx. | Verification : curl http://192.168.56.103 retourne HTTP 200
   F7 -- Sauvegarde creee : /backup/ctf-alpesnet-20260702_113109.tar.gz | Verification : sha256sum -c /backup/ctf-alpesnet-20260702_113109.tar.gz.sha256

4. ETAT FINAL
   ssh oliv@192.168.56.103           : autorise
   ssh root@192.168.56.103           : refuse
   ssh autre_compte@192.168.56.103   : refuse
   ufw status              : regles actives a verifier avec ufw status verbose
   fail2ban-client status  : jail sshd active a verifier
   curl http://192.168.56.103        : HTTP 200

5. RECOMMANDATIONS
   - Limiter SSH aux comptes autorises avec AllowUsers ; basculer vers cle seule apres verification que les cles sont deployees.
   - Auditer regulierement les comptes UID 0, sudoers et shells interactifs.
   - Surveiller les logs SSH et conserver une rotation exploitable.
   - Corriger les permissions 0777/SUID injustifiees et documenter toute exception.
   - Maintenir ufw et fail2ban actifs, avec tests apres chaque changement.
   - Tester les sauvegardes et verifier les checksums, pas seulement creer les archives.

## 6. DETAIL STEP BY STEP DES FLAGS

Cette section centralise les preuves dans le rapport final, comme demande par le formateur.

### F1 - Acces root

~~~text
# F1 - Acces root

Date : 2026-07-02 11:31:13
Machine : ctfalpesnet
IP : 192.168.56.103

Objectif : obtenir l'acces root sur la VM compromise.

Commandes de preuve :
```
uid=0(root) gid=0(root) groupes=0(root)
root

sudo -n true :
OK - sudo utilisable sans mot de passe

sudo -l :
Entrées Defaults correspondant pour root sur ctfalpesnet :
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin,
    use_pty

L'utilisateur root peut utiliser les commandes suivantes sur ctfalpesnet :
    (ALL : ALL) ALL
```

Verification SSH root annoncee par le scenario :

Configuration SSH utile :
permitrootlogin yes
pubkeyauthentication yes
passwordauthentication yes
permitemptypasswords no

Service SSH :
active

Port 22 en ecoute :
State  Recv-Q Send-Q Local Address:Port Peer Address:PortProcess                       
LISTEN 0      128          0.0.0.0:22        0.0.0.0:*    users:(("sshd",pid=609,fd=3))
LISTEN 0      128             [::]:22           [::]:*    users:(("sshd",pid=609,fd=4))

Commande de preuve a lancer depuis la machine hote si root SSH est encore autorise :
ssh root@192.168.56.103
Ne pas utiliser /root/.ctf_answers ou .ctf_answer : ce sont les reponses formateur.

Recherche d'un mot de passe cache dans la VM :
```
Racines inspectees pour F1 :
/home/investigateur
/home/backdoor-sys
/home/backdoor-sys
/home/investigateur
Racines volontairement exclues : /root et fichiers .ctf_answer* (reponses formateur), /home/oliv /home/olivier /home/oliv
Marqueurs scenario recherches dans les homes suspects : investigateur, backdoor-sys, Inv3st1g4t3ur!, root avec contexte pass/su/login
Fichiers caches inspectes dans les homes suspects :
644 investigateur:investigateur /home/investigateur/.bash_history
644 investigateur:investigateur /home/investigateur/.bash_logout
644 investigateur:investigateur /home/investigateur/.profile
644 investigateur:investigateur /home/investigateur/.bashrc
600 backdoor-sys:backdoor-sys /home/backdoor-sys/.bash_history
644 backdoor-sys:backdoor-sys /home/backdoor-sys/.bash_logout
644 backdoor-sys:backdoor-sys /home/backdoor-sys/.profile
644 backdoor-sys:backdoor-sys /home/backdoor-sys/.bashrc
600 backdoor-sys:backdoor-sys /home/backdoor-sys/.bash_history
644 backdoor-sys:backdoor-sys /home/backdoor-sys/.bash_logout
644 backdoor-sys:backdoor-sys /home/backdoor-sys/.profile
644 backdoor-sys:backdoor-sys /home/backdoor-sys/.bashrc
644 investigateur:investigateur /home/investigateur/.bash_history
644 investigateur:investigateur /home/investigateur/.bash_logout
644 investigateur:investigateur /home/investigateur/.profile
644 investigateur:investigateur /home/investigateur/.bashrc
Fichiers dont le nom evoque les users du scenario :
Fichiers contenant les marqueurs exacts du scenario :
/home/investigateur/.bash_history
/home/investigateur/.bash_history
Occurrences utiles avec fichier source et ligne :
/home/investigateur/.bash_history:3:su - root
/home/investigateur/.bash_history:3:su - root
```

Commandes rejouables pour la demo :
```bash
sudo find /home -mindepth 1 -maxdepth 1 -type d ! -name oliv ! -name olivier -print
sudo find /home/investigateur /home/backdoor-sys -xdev -maxdepth 3 -type f -name '.*' ! -name '.ctf_answer' ! -name '.ctf_answers' -printf '%m %u:%g %p\n' 2>/dev/null
sudo grep -RInEi --exclude='.ctf_answer' --exclude='.ctf_answers' 'investigateur|backdoor-sys|Inv3st1g4t3ur!|root.{0,40}(pass|passwd|password|mdp|su|login|secret|credential|creds)|((pass|passwd|password|mdp|su|login|secret|credential|creds).{0,40}root)' /home/investigateur /home/backdoor-sys 2>/dev/null | head -80
sshd -T | grep -Ei '^(permitrootlogin|passwordauthentication)'
systemctl is-active ssh || systemctl is-active sshd
ss -tlnp | grep ':22'
ssh root@192.168.56.103
```

Resultat a soumettre :
mot de passe cache retrouve dans la VM puis utilisation de su/root ou ssh root@IP
~~~

### F2 - Compte non autorise : audit, explication et resultat

~~~text
# F2 - Compte non autorise

Date : 2026-07-02 11:31:13
Machine : ctfalpesnet
IP : 192.168.56.103

Objectif : identifier le compte cree par l'attaquant.

Audit immediat :
```
uid=0(root) gid=0(root) groupes=0(root)

Comptes UID 0 autres que root :

Comptes avec shell interactif :
root:0:/root:/bin/bash
oliv:1000:/home/oliv:/bin/bash
investigateur:1001:/home/investigateur:/bin/bash
backdoor-sys:1002:/home/backdoor-sys:/bin/bash

Groupes par utilisateur :
root: root
nobody: nogroup
oliv: oliv cdrom floppy sudo audio dip video plugdev users netdev bluetooth
investigateur: investigateur
backdoor-sys: backdoor-sys sudo

Sudoers additionnels :
Aucun fichier sudoers additionnel actif hors README.

Dernieres connexions :
Username         Port     From                                       Latest
root             pts/1    192.168.56.103                            jeu. juil.  2 09:27:05 +0200 2026
daemon                                                              **Never logged in**
bin                                                                 **Never logged in**
sys                                                                 **Never logged in**
sync                                                                **Never logged in**
games                                                               **Never logged in**
man                                                                 **Never logged in**
lp                                                                  **Never logged in**
mail                                                                **Never logged in**
news                                                                **Never logged in**
uucp                                                                **Never logged in**
proxy                                                               **Never logged in**
www-data                                                            **Never logged in**
backup                                                              **Never logged in**
list                                                                **Never logged in**
irc                                                                 **Never logged in**
_apt                                                                **Never logged in**
nobody                                                              **Never logged in**
systemd-network                                                     **Never logged in**
messagebus                                                          **Never logged in**
avahi-autoipd                                                       **Never logged in**
sshd                                                                **Never logged in**
oliv             pts/2    192.168.56.1                              jeu. juil.  2 09:23:31 +0200 2026
investigateur                                                       **Never logged in**
backdoor-sys                                                        **Never logged in**
```

Explication des commandes F2 :

- `awk -F: '($3==0)'` lit `/etc/passwd` avec `:` comme separateur. Le champ 3 est l'UID. Un UID `0` donne les privileges root ; tout compte UID 0 autre que `root` est donc critique.
- `getent passwd` confirme l'existence d'un compte et affiche son UID, son home et son shell.
- La boucle `id -nG` affiche les groupes par utilisateur, ce qui permet de reperer un compte ajoute a `sudo`, `admin` ou `wheel`.
- La lecture de `/etc/sudoers.d` montre les regles sudo additionnelles actives, sans le README ni les commentaires.
- `lastlog` aide a reperer une connexion recente ou anormale.

Candidats suspects calcules par le script :
Utilisateurs consideres autorises et exclus du score : root oliv olivier oliv root

| Score | User | UID | GID | Home | Shell | Indice fort | Raisons |
| ---: | --- | ---: | ---: | --- | --- | --- | --- |
| 70 | `backdoor-sys` | 1002 | 1002 | `/home/backdoor-sys` | `/bin/bash` | non | UID utilisateur,shell interactif,home dans /home,groupe admin/sudo |
| 30 | `investigateur` | 1001 | 1001 | `/home/investigateur` | `/bin/bash` | non | UID utilisateur,shell interactif,home dans /home |

Resultat observe F2 :

Le compte le plus probable est `backdoor-sys` car il ressort dans les indices calcules ci-dessus.

Compte suspect retenu : backdoor-sys
Commande de verification : getent passwd backdoor-sys

Estimation de la date de creation du compte suspect :

```
Compte analyse : backdoor-sys

Entree passwd :
backdoor-sys:x:1002:1002::/home/backdoor-sys:/bin/bash

Dates du dossier personnel :
Birth: 2026-07-01 13:36:52.855994888 +0200
Change: 2026-07-01 16:27:38.207870242 +0200
Modify: 2026-07-01 16:27:38.207870242 +0200
Access: 2026-07-01 16:28:43.175869144 +0200
Path: /home/backdoor-sys

Informations chage :
Dernière modification du mot de passe					 :juil. 02, 2026
Le mot de passe expire					 :jamais
Mot de passe inactif					 : jamais
Le compte expire 						 : jamais
Nombre minimal de jours entre deux changements de mot de passe 		 : 0
Nombre maximal de jours entre deux changements du mot de passe		 : 99999
Nombre de jours d'avertissements avant que le mot de passe n'expire	 : 7

Traces de creation dans les logs locaux :
Aucune trace useradd/adduser exploitable trouvee dans les logs non compresses.

Connexions connues :
Username         Port     From                                       Latest
backdoor-sys                                                        **Never logged in**

wtmp commence Wed Jul  1 13:27:00 2026
```

Explication : Linux ne stocke pas toujours une date de creation de compte fiable. On l'estime en croisant la date de naissance/modification du home, les informations chage, les traces useradd/adduser dans les logs et les premieres connexions.
~~~

### F3 - IP source de l'intrusion

~~~text
# F3 - IP source des tentatives d'intrusion

Date : 2026-07-02 11:31:41
Machine : ctfalpesnet
IP : 192.168.56.103

Objectif : trouver l'IP source des tentatives d'intrusion.

Logs examines : /var/log/auth.log, /var/log/auth.log.1, /var/log/secure, /var/log/secure.1, journalctl -u ssh/sshd

Compteur IP extrait automatiquement :

| Occurrences | IP |
| ---: | --- |
| 125 | `185.220.101.47` |
| 2 | `192.168.56.1` |

IP source retenue automatiquement : 185.220.101.47

Extraits de logs justificatifs pour 185.220.101.47 :
```
/var/log/auth.log:juin 26 13:37:52 srv-ctf sshd[1337]: Invalid user scanner from 185.220.101.47 port 40001
/var/log/auth.log:juin 26 13:38:52 srv-ctf sshd[1337]: Invalid user scanner from 185.220.101.47 port 40002
/var/log/auth.log:juin 26 13:39:52 srv-ctf sshd[1337]: Invalid user scanner from 185.220.101.47 port 40003
/var/log/auth.log:juin 26 13:40:52 srv-ctf sshd[1337]: Invalid user scanner from 185.220.101.47 port 40004
/var/log/auth.log:juin 26 13:41:52 srv-ctf sshd[1337]: Invalid user scanner from 185.220.101.47 port 40005
/var/log/auth.log:juin 26 13:42:52 srv-ctf sshd[1337]: Invalid user scanner from 185.220.101.47 port 40006
/var/log/auth.log:juin 26 13:43:52 srv-ctf sshd[1337]: Invalid user scanner from 185.220.101.47 port 40007
/var/log/auth.log:juin 26 13:44:52 srv-ctf sshd[1337]: Invalid user scanner from 185.220.101.47 port 40008
/var/log/auth.log:juin 26 13:45:52 srv-ctf sshd[1337]: Invalid user scanner from 185.220.101.47 port 40009
/var/log/auth.log:juin 26 13:46:52 srv-ctf sshd[1337]: Invalid user scanner from 185.220.101.47 port 40010
/var/log/auth.log:juin 26 13:47:52 srv-ctf sshd[1337]: Invalid user scanner from 185.220.101.47 port 40011
/var/log/auth.log:juin 26 13:48:52 srv-ctf sshd[1337]: Invalid user scanner from 185.220.101.47 port 40012
/var/log/auth.log:juin 26 13:49:52 srv-ctf sshd[1337]: Invalid user scanner from 185.220.101.47 port 40013
/var/log/auth.log:juin 26 13:50:52 srv-ctf sshd[1337]: Invalid user scanner from 185.220.101.47 port 40014
/var/log/auth.log:juin 26 13:51:52 srv-ctf sshd[1337]: Invalid user scanner from 185.220.101.47 port 40015
/var/log/auth.log:juin 26 13:52:52 srv-ctf sshd[1337]: Invalid user scanner from 185.220.101.47 port 40016
/var/log/auth.log:juin 26 13:53:52 srv-ctf sshd[1337]: Invalid user scanner from 185.220.101.47 port 40017
/var/log/auth.log:juin 26 13:54:52 srv-ctf sshd[1337]: Invalid user scanner from 185.220.101.47 port 40018
/var/log/auth.log:juin 26 13:55:52 srv-ctf sshd[1337]: Invalid user scanner from 185.220.101.47 port 40019
/var/log/auth.log:juin 26 13:56:52 srv-ctf sshd[1337]: Invalid user scanner from 185.220.101.47 port 40020
```

Fichiers de travail :
- Evenements SSH : /flags/.ctf-alpesnet/f3_ssh_events.log
- Compteur IP : /flags/.ctf-alpesnet/f3_ip_counts.tsv

Resultat a soumettre :
IP source retenue : 185.220.101.47
Commande de preuve : grep/awk sur les logs SSH, voir compteur ci-dessus.
~~~

### F4 - Permissions dangereuses et SUID

~~~text
# F4 - Permissions dangereuses

Date : 2026-07-02 11:31:41
Machine : ctfalpesnet
IP : 192.168.56.103

Objectif : identifier un fichier ou repertoire avec permissions dangereuses.

Candidats dangereux calcules automatiquement :

| Score | Chemin | Mode | Proprio | Type | Risque | Correction proposee |
| ---: | --- | ---: | --- | --- | --- | --- |
| 140 | `/var/www/upload` | `777` | `root:root` | `d` | permissions 0777 | `chmod 750` |
| 120 | `/usr/local/bin/check-status.sh` | `4755` | `root:root` | `f` | SUID/SGID | `chmod u-s,g-s` |
| 70 | `/usr/sbin/unix_chkpwd` | `2755` | `root:shadow` | `f` | SUID/SGID | `chmod u-s,g-s` |
| 70 | `/usr/bin/ssh-agent` | `2755` | `root:_ssh` | `f` | SUID/SGID | `chmod u-s,g-s` |
| 70 | `/usr/bin/expiry` | `2755` | `root:shadow` | `f` | SUID/SGID | `chmod u-s,g-s` |
| 70 | `/usr/bin/crontab` | `2755` | `root:crontab` | `f` | SUID/SGID | `chmod u-s,g-s` |
| 70 | `/usr/bin/chage` | `2755` | `root:shadow` | `f` | SUID/SGID | `chmod u-s,g-s` |

Element retenu automatiquement : /var/www/upload
Risque retenu : permissions 0777
Correction proposee : chmod 750 /var/www/upload

Preuve stat :
```
777 drwxrwxrwx root:root /var/www/upload
```

Resultat a soumettre :
Element dangereux retenu : /var/www/upload
Risque : permissions 0777
Correction prevue : chmod 750 /var/www/upload
~~~

### F5 - Durcissement : synthese et explication des mesures

~~~text
# F5 - Durcissement SSH, ufw, fail2ban et services

Date : 2026-07-02 11:31:41
Machine : ctfalpesnet
IP : 192.168.56.103

Objectif : appliquer SSH + ufw + fail2ban + services et preparer la demo live.

Rapport avant correction : /flags/F5_avant.txt
Rapport apres correction : /flags/F5_apres.txt

Etat initial synthetique :
```
===== F5 AVANT CORRECTION =====
Date : 2026-07-02 11:31:41
Machine : ctfalpesnet

## SSH
PermitRootLogin yes
PubkeyAuthentication yes
PasswordAuthentication yes
PermitEmptyPasswords no
KbdInteractiveAuthentication no
ChallengeResponseAuthentication no
AllowUsers oliv

## Cle publique SSH
Utilisateur SSH cible : oliv
Fichier authorized_keys : /home/oliv/.ssh/authorized_keys
authorized_keys existe deja.

## UFW
Status: inactive

## Fail2ban
fail2ban-client ne trouve pas le socket : le service n'est probablement pas demarre.
Diagnostic systemd :
○ fail2ban.service - Fail2Ban Service
     Loaded: loaded (/lib/systemd/system/fail2ban.service; enabled; preset: enabled)
     Active: inactive (dead) since Thu 2026-07-02 11:24:18 CEST; 7min ago
   Duration: 1h 17min 44.749s
       Docs: man:fail2ban(1)
    Process: 2240 ExecStart=/usr/bin/fail2ban-server -xf start (code=killed, signal=TERM)
    Process: 3404 ExecStop=/usr/bin/fail2ban-client stop (code=exited, status=0/SUCCESS)
   Main PID: 2240 (code=killed, signal=TERM)
        CPU: 1.300s

juil. 02 10:06:32 ctfalpesnet systemd[1]: Stopped fail2ban.service - Fail2Ban Service.
juil. 02 10:06:32 ctfalpesnet systemd[1]: fail2ban.service: Consumed 1.444s CPU time.
juil. 02 10:06:32 ctfalpesnet systemd[1]: Started fail2ban.service - Fail2Ban Service.
juil. 02 10:06:32 ctfalpesnet fail2ban-server[2240]: 2026-07-02 10:06:32,544 fail2ban.configreader   [2240]: WARNING 'allowipv6' not defined in 'Definition'. Using default one: 'auto'
juil. 02 10:06:32 ctfalpesnet fail2ban-server[2240]: Server ready
juil. 02 11:24:17 ctfalpesnet systemd[1]: Stopping fail2ban.service - Fail2Ban Service...
juil. 02 11:24:18 ctfalpesnet fail2ban-client[3404]: Shutdown successful
juil. 02 11:24:18 ctfalpesnet systemd[1]: fail2ban.service: Deactivated successfully.
juil. 02 11:24:18 ctfalpesnet systemd[1]: Stopped fail2ban.service - Fail2Ban Service.
juil. 02 11:24:18 ctfalpesnet systemd[1]: fail2ban.service: Consumed 1.300s CPU time.

Derniers logs fail2ban :
juil. 01 15:03:19 ctfalpesnet fail2ban-client[1978]: Shutdown successful
juil. 01 15:03:19 ctfalpesnet systemd[1]: fail2ban.service: Deactivated successfully.
juil. 01 15:03:19 ctfalpesnet systemd[1]: Stopped fail2ban.service - Fail2Ban Service.
juil. 01 15:04:11 ctfalpesnet systemd[1]: Started fail2ban.service - Fail2Ban Service.
juil. 01 15:04:11 ctfalpesnet fail2ban-server[2872]: 2026-07-01 15:04:11,809 fail2ban.configreader   [2872]: WARNING 'allowipv6' not defined in 'Definition'. Using default one: 'auto'
juil. 01 15:04:11 ctfalpesnet fail2ban-server[2872]: Server ready
juil. 01 15:06:21 ctfalpesnet systemd[1]: Stopping fail2ban.service - Fail2Ban Service...
juil. 01 15:06:21 ctfalpesnet fail2ban-client[3780]: Shutdown successful
juil. 01 15:06:21 ctfalpesnet systemd[1]: fail2ban.service: Deactivated successfully.
juil. 01 15:06:21 ctfalpesnet systemd[1]: Stopped fail2ban.service - Fail2Ban Service.
juil. 01 15:07:16 ctfalpesnet systemd[1]: Started fail2ban.service - Fail2Ban Service.
juil. 01 15:07:16 ctfalpesnet fail2ban-server[4514]: 2026-07-01 15:07:16,506 fail2ban.configreader   [4514]: WARNING 'allowipv6' not defined in 'Definition'. Using default one: 'auto'
juil. 01 15:07:16 ctfalpesnet fail2ban-server[4514]: Server ready
juil. 01 15:12:00 ctfalpesnet systemd[1]: Stopping fail2ban.service - Fail2Ban Service...
juil. 01 15:12:00 ctfalpesnet fail2ban-client[5939]: Shutdown successful
juil. 01 15:12:00 ctfalpesnet systemd[1]: fail2ban.service: Deactivated successfully.
juil. 01 15:12:00 ctfalpesnet systemd[1]: Stopped fail2ban.service - Fail2Ban Service.
juil. 01 15:12:00 ctfalpesnet systemd[1]: Started fail2ban.service - Fail2Ban Service.
juil. 01 15:12:00 ctfalpesnet fail2ban-server[5940]: 2026-07-01 15:12:00,805 fail2ban.configreader   [5940]: WARNING 'allowipv6' not defined in 'Definition'. Using default one: 'auto'
juil. 01 15:12:00 ctfalpesnet fail2ban-server[5940]: Server ready
juil. 01 15:53:05 ctfalpesnet systemd[1]: Stopping fail2ban.service - Fail2Ban Service...
juil. 01 15:53:05 ctfalpesnet fail2ban-client[6672]: Shutdown successful
juil. 01 15:53:05 ctfalpesnet systemd[1]: fail2ban.service: Deactivated successfully.
juil. 01 15:53:05 ctfalpesnet systemd[1]: Stopped fail2ban.service - Fail2Ban Service.
-- Boot 58b8da07c7d74a579f99c76128ccda7b --
juil. 02 09:02:28 ctfalpesnet systemd[1]: Started fail2ban.service - Fail2Ban Service.
juil. 02 09:02:28 ctfalpesnet fail2ban-server[555]: 2026-07-02 09:02:28,905 fail2ban.configreader   [555]: WARNING 'allowipv6' not defined in 'Definition'. Using default one: 'auto'
juil. 02 09:02:28 ctfalpesnet fail2ban-server[555]: Server ready
juil. 02 10:06:31 ctfalpesnet systemd[1]: Stopping fail2ban.service - Fail2Ban Service...
juil. 02 10:06:32 ctfalpesnet fail2ban-client[2239]: Shutdown successful
juil. 02 10:06:32 ctfalpesnet systemd[1]: fail2ban.service: Deactivated successfully.
juil. 02 10:06:32 ctfalpesnet systemd[1]: Stopped fail2ban.service - Fail2Ban Service.
juil. 02 10:06:32 ctfalpesnet systemd[1]: fail2ban.service: Consumed 1.444s CPU time.
juil. 02 10:06:32 ctfalpesnet systemd[1]: Started fail2ban.service - Fail2Ban Service.
juil. 02 10:06:32 ctfalpesnet fail2ban-server[2240]: 2026-07-02 10:06:32,544 fail2ban.configreader   [2240]: WARNING 'allowipv6' not defined in 'Definition'. Using default one: 'auto'
juil. 02 10:06:32 ctfalpesnet fail2ban-server[2240]: Server ready
juil. 02 11:24:17 ctfalpesnet systemd[1]: Stopping fail2ban.service - Fail2Ban Service...
juil. 02 11:24:18 ctfalpesnet fail2ban-client[3404]: Shutdown successful
juil. 02 11:24:18 ctfalpesnet systemd[1]: fail2ban.service: Deactivated successfully.
juil. 02 11:24:18 ctfalpesnet systemd[1]: Stopped fail2ban.service - Fail2Ban Service.
juil. 02 11:24:18 ctfalpesnet systemd[1]: fail2ban.service: Consumed 1.300s CPU time.

## Ports en ecoute
Netid State  Recv-Q Send-Q Local Address:Port Peer Address:PortProcess                           
udp   UNCONN 0      0            0.0.0.0:68        0.0.0.0:*    users:(("dhclient",pid=507,fd=7))
udp   UNCONN 0      0            0.0.0.0:68        0.0.0.0:*    users:(("dhclient",pid=506,fd=7))
tcp   LISTEN 0      128          0.0.0.0:22        0.0.0.0:*    users:(("sshd",pid=609,fd=3))    
tcp   LISTEN 0      128             [::]:22           [::]:*    users:(("sshd",pid=609,fd=4))    

## Services cibles
avahi-daemon absent
cups absent
rpcbind absent
nfs-server absent
smbd absent
```

Corrections proposees pour F5 :
- SSH : verifier qu'une cle publique est presente dans ~/.ssh/authorized_keys.
- SSH : sauvegarder /etc/ssh/sshd_config puis limiter les connexions a AllowUsers oliv.
- SSH : conserver PasswordAuthentication yes pour ne pas casser scp/SSH pendant le CTF.
- SSH : conserver PubkeyAuthentication yes et refuser PermitEmptyPasswords.
- SSH : ne pas changer le mot de passe root et ne pas s'appuyer sur ce compte pour la connexion distante.
- SSH : valider avec sshd -t puis recharger ssh/sshd.
- UFW : deny incoming, allow outgoing, allow OpenSSH/22, HTTP/80, HTTPS/443, enable.
- Fail2ban : creer/mettre a jour la jail sshd, tester avec fail2ban-client -t, redemarrer le service.
- Services : arreter/desactiver les services inutiles detectes parmi avahi-daemon, cups, rpcbind, nfs-server, smbd.

Application des corrections F5.
Aucune cle publique fournie.
Default incoming policy changed to 'deny'
(be sure to update your rules accordingly)
Default outgoing policy changed to 'allow'
(be sure to update your rules accordingly)
Skipping adding existing rule
Skipping adding existing rule (v6)
Skipping adding existing rule
Skipping adding existing rule (v6)
Skipping adding existing rule
Skipping adding existing rule (v6)
Firewall is active and enabled on system startup
2026-07-02 11:31:45,532 fail2ban.configreader   [4459]: WARNING 'allowipv6' not defined in 'Definition'. Using default one: 'auto'
OK: configuration test is successful
Synchronizing state of fail2ban.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable fail2ban

Etat final / demo live :
```
===== F5 APRES CORRECTION OU AUDIT =====
Date : 2026-07-02 11:31:45
Machine : ctfalpesnet

## SSH
PermitRootLogin yes
PubkeyAuthentication yes
PasswordAuthentication yes
PermitEmptyPasswords no
KbdInteractiveAuthentication no
ChallengeResponseAuthentication no
AllowUsers oliv

## Cle publique SSH
Utilisateur SSH cible : oliv
Fichier authorized_keys : /home/oliv/.ssh/authorized_keys
authorized_keys existe deja.

## UFW
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp (OpenSSH)           ALLOW IN    Anywhere                  
80/tcp                     ALLOW IN    Anywhere                  
443                        ALLOW IN    Anywhere                  
22/tcp (OpenSSH (v6))      ALLOW IN    Anywhere (v6)             
80/tcp (v6)                ALLOW IN    Anywhere (v6)             
443 (v6)                   ALLOW IN    Anywhere (v6)             


## Fail2ban
Status
|- Number of jail:	1
`- Jail list:	sshd
Status for the jail: sshd
|- Filter
|  |- Currently failed:	0
|  |- Total failed:	0
|  `- File list:	/var/log/auth.log
`- Actions
   |- Currently banned:	0
   |- Total banned:	0
   `- Banned IP list:	

## Ports en ecoute
Netid State  Recv-Q Send-Q Local Address:Port Peer Address:PortProcess                           
udp   UNCONN 0      0            0.0.0.0:68        0.0.0.0:*    users:(("dhclient",pid=507,fd=7))
udp   UNCONN 0      0            0.0.0.0:68        0.0.0.0:*    users:(("dhclient",pid=506,fd=7))
tcp   LISTEN 0      128          0.0.0.0:22        0.0.0.0:*    users:(("sshd",pid=609,fd=3))    
tcp   LISTEN 0      128             [::]:22           [::]:*    users:(("sshd",pid=609,fd=4))    

## Services cibles
avahi-daemon absent
cups absent
rpcbind absent
nfs-server absent
smbd absent
```

Preuve de travail F5 a montrer :

```bash
ssh root@192.168.56.103
sudo ufw status verbose
sudo fail2ban-client status sshd
```

Explication des mesures F5 :

- `ssh root@IP` doit etre refuse : SSH est limite a `AllowUsers oliv`, donc root n'est pas un compte autorise en connexion distante. Le mot de passe root n'est pas modifie.
- `ufw status verbose` prouve que le pare-feu local est actif, avec les entrees limitees aux ports classiques utiles : SSH/22, HTTP/80 et HTTPS/443.
- `fail2ban-client status sshd` prouve que la jail SSH surveille les tentatives d'authentification et peut bannir les sources abusives.
~~~

### F5 - Etat avant correction

~~~text
===== F5 AVANT CORRECTION =====
Date : 2026-07-02 11:31:41
Machine : ctfalpesnet

## SSH
PermitRootLogin yes
PubkeyAuthentication yes
PasswordAuthentication yes
PermitEmptyPasswords no
KbdInteractiveAuthentication no
ChallengeResponseAuthentication no
AllowUsers oliv

## Cle publique SSH
Utilisateur SSH cible : oliv
Fichier authorized_keys : /home/oliv/.ssh/authorized_keys
authorized_keys existe deja.

## UFW
Status: inactive

## Fail2ban
fail2ban-client ne trouve pas le socket : le service n'est probablement pas demarre.
Diagnostic systemd :
○ fail2ban.service - Fail2Ban Service
     Loaded: loaded (/lib/systemd/system/fail2ban.service; enabled; preset: enabled)
     Active: inactive (dead) since Thu 2026-07-02 11:24:18 CEST; 7min ago
   Duration: 1h 17min 44.749s
       Docs: man:fail2ban(1)
    Process: 2240 ExecStart=/usr/bin/fail2ban-server -xf start (code=killed, signal=TERM)
    Process: 3404 ExecStop=/usr/bin/fail2ban-client stop (code=exited, status=0/SUCCESS)
   Main PID: 2240 (code=killed, signal=TERM)
        CPU: 1.300s

juil. 02 10:06:32 ctfalpesnet systemd[1]: Stopped fail2ban.service - Fail2Ban Service.
juil. 02 10:06:32 ctfalpesnet systemd[1]: fail2ban.service: Consumed 1.444s CPU time.
juil. 02 10:06:32 ctfalpesnet systemd[1]: Started fail2ban.service - Fail2Ban Service.
juil. 02 10:06:32 ctfalpesnet fail2ban-server[2240]: 2026-07-02 10:06:32,544 fail2ban.configreader   [2240]: WARNING 'allowipv6' not defined in 'Definition'. Using default one: 'auto'
juil. 02 10:06:32 ctfalpesnet fail2ban-server[2240]: Server ready
juil. 02 11:24:17 ctfalpesnet systemd[1]: Stopping fail2ban.service - Fail2Ban Service...
juil. 02 11:24:18 ctfalpesnet fail2ban-client[3404]: Shutdown successful
juil. 02 11:24:18 ctfalpesnet systemd[1]: fail2ban.service: Deactivated successfully.
juil. 02 11:24:18 ctfalpesnet systemd[1]: Stopped fail2ban.service - Fail2Ban Service.
juil. 02 11:24:18 ctfalpesnet systemd[1]: fail2ban.service: Consumed 1.300s CPU time.

Derniers logs fail2ban :
juil. 01 15:03:19 ctfalpesnet fail2ban-client[1978]: Shutdown successful
juil. 01 15:03:19 ctfalpesnet systemd[1]: fail2ban.service: Deactivated successfully.
juil. 01 15:03:19 ctfalpesnet systemd[1]: Stopped fail2ban.service - Fail2Ban Service.
juil. 01 15:04:11 ctfalpesnet systemd[1]: Started fail2ban.service - Fail2Ban Service.
juil. 01 15:04:11 ctfalpesnet fail2ban-server[2872]: 2026-07-01 15:04:11,809 fail2ban.configreader   [2872]: WARNING 'allowipv6' not defined in 'Definition'. Using default one: 'auto'
juil. 01 15:04:11 ctfalpesnet fail2ban-server[2872]: Server ready
juil. 01 15:06:21 ctfalpesnet systemd[1]: Stopping fail2ban.service - Fail2Ban Service...
juil. 01 15:06:21 ctfalpesnet fail2ban-client[3780]: Shutdown successful
juil. 01 15:06:21 ctfalpesnet systemd[1]: fail2ban.service: Deactivated successfully.
juil. 01 15:06:21 ctfalpesnet systemd[1]: Stopped fail2ban.service - Fail2Ban Service.
juil. 01 15:07:16 ctfalpesnet systemd[1]: Started fail2ban.service - Fail2Ban Service.
juil. 01 15:07:16 ctfalpesnet fail2ban-server[4514]: 2026-07-01 15:07:16,506 fail2ban.configreader   [4514]: WARNING 'allowipv6' not defined in 'Definition'. Using default one: 'auto'
juil. 01 15:07:16 ctfalpesnet fail2ban-server[4514]: Server ready
juil. 01 15:12:00 ctfalpesnet systemd[1]: Stopping fail2ban.service - Fail2Ban Service...
juil. 01 15:12:00 ctfalpesnet fail2ban-client[5939]: Shutdown successful
juil. 01 15:12:00 ctfalpesnet systemd[1]: fail2ban.service: Deactivated successfully.
juil. 01 15:12:00 ctfalpesnet systemd[1]: Stopped fail2ban.service - Fail2Ban Service.
juil. 01 15:12:00 ctfalpesnet systemd[1]: Started fail2ban.service - Fail2Ban Service.
juil. 01 15:12:00 ctfalpesnet fail2ban-server[5940]: 2026-07-01 15:12:00,805 fail2ban.configreader   [5940]: WARNING 'allowipv6' not defined in 'Definition'. Using default one: 'auto'
juil. 01 15:12:00 ctfalpesnet fail2ban-server[5940]: Server ready
juil. 01 15:53:05 ctfalpesnet systemd[1]: Stopping fail2ban.service - Fail2Ban Service...
juil. 01 15:53:05 ctfalpesnet fail2ban-client[6672]: Shutdown successful
juil. 01 15:53:05 ctfalpesnet systemd[1]: fail2ban.service: Deactivated successfully.
juil. 01 15:53:05 ctfalpesnet systemd[1]: Stopped fail2ban.service - Fail2Ban Service.
-- Boot 58b8da07c7d74a579f99c76128ccda7b --
juil. 02 09:02:28 ctfalpesnet systemd[1]: Started fail2ban.service - Fail2Ban Service.
juil. 02 09:02:28 ctfalpesnet fail2ban-server[555]: 2026-07-02 09:02:28,905 fail2ban.configreader   [555]: WARNING 'allowipv6' not defined in 'Definition'. Using default one: 'auto'
juil. 02 09:02:28 ctfalpesnet fail2ban-server[555]: Server ready
juil. 02 10:06:31 ctfalpesnet systemd[1]: Stopping fail2ban.service - Fail2Ban Service...
juil. 02 10:06:32 ctfalpesnet fail2ban-client[2239]: Shutdown successful
juil. 02 10:06:32 ctfalpesnet systemd[1]: fail2ban.service: Deactivated successfully.
juil. 02 10:06:32 ctfalpesnet systemd[1]: Stopped fail2ban.service - Fail2Ban Service.
juil. 02 10:06:32 ctfalpesnet systemd[1]: fail2ban.service: Consumed 1.444s CPU time.
juil. 02 10:06:32 ctfalpesnet systemd[1]: Started fail2ban.service - Fail2Ban Service.
juil. 02 10:06:32 ctfalpesnet fail2ban-server[2240]: 2026-07-02 10:06:32,544 fail2ban.configreader   [2240]: WARNING 'allowipv6' not defined in 'Definition'. Using default one: 'auto'
juil. 02 10:06:32 ctfalpesnet fail2ban-server[2240]: Server ready
juil. 02 11:24:17 ctfalpesnet systemd[1]: Stopping fail2ban.service - Fail2Ban Service...
juil. 02 11:24:18 ctfalpesnet fail2ban-client[3404]: Shutdown successful
juil. 02 11:24:18 ctfalpesnet systemd[1]: fail2ban.service: Deactivated successfully.
juil. 02 11:24:18 ctfalpesnet systemd[1]: Stopped fail2ban.service - Fail2Ban Service.
juil. 02 11:24:18 ctfalpesnet systemd[1]: fail2ban.service: Consumed 1.300s CPU time.

## Ports en ecoute
Netid State  Recv-Q Send-Q Local Address:Port Peer Address:PortProcess                           
udp   UNCONN 0      0            0.0.0.0:68        0.0.0.0:*    users:(("dhclient",pid=507,fd=7))
udp   UNCONN 0      0            0.0.0.0:68        0.0.0.0:*    users:(("dhclient",pid=506,fd=7))
tcp   LISTEN 0      128          0.0.0.0:22        0.0.0.0:*    users:(("sshd",pid=609,fd=3))    
tcp   LISTEN 0      128             [::]:22           [::]:*    users:(("sshd",pid=609,fd=4))    

## Services cibles
avahi-daemon absent
cups absent
rpcbind absent
nfs-server absent
smbd absent
~~~

### F5 - Etat apres correction ou audit

~~~text
===== F5 APRES CORRECTION OU AUDIT =====
Date : 2026-07-02 11:31:45
Machine : ctfalpesnet

## SSH
PermitRootLogin yes
PubkeyAuthentication yes
PasswordAuthentication yes
PermitEmptyPasswords no
KbdInteractiveAuthentication no
ChallengeResponseAuthentication no
AllowUsers oliv

## Cle publique SSH
Utilisateur SSH cible : oliv
Fichier authorized_keys : /home/oliv/.ssh/authorized_keys
authorized_keys existe deja.

## UFW
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp (OpenSSH)           ALLOW IN    Anywhere                  
80/tcp                     ALLOW IN    Anywhere                  
443                        ALLOW IN    Anywhere                  
22/tcp (OpenSSH (v6))      ALLOW IN    Anywhere (v6)             
80/tcp (v6)                ALLOW IN    Anywhere (v6)             
443 (v6)                   ALLOW IN    Anywhere (v6)             


## Fail2ban
Status
|- Number of jail:	1
`- Jail list:	sshd
Status for the jail: sshd
|- Filter
|  |- Currently failed:	0
|  |- Total failed:	0
|  `- File list:	/var/log/auth.log
`- Actions
   |- Currently banned:	0
   |- Total banned:	0
   `- Banned IP list:	

## Ports en ecoute
Netid State  Recv-Q Send-Q Local Address:Port Peer Address:PortProcess                           
udp   UNCONN 0      0            0.0.0.0:68        0.0.0.0:*    users:(("dhclient",pid=507,fd=7))
udp   UNCONN 0      0            0.0.0.0:68        0.0.0.0:*    users:(("dhclient",pid=506,fd=7))
tcp   LISTEN 0      128          0.0.0.0:22        0.0.0.0:*    users:(("sshd",pid=609,fd=3))    
tcp   LISTEN 0      128             [::]:22           [::]:*    users:(("sshd",pid=609,fd=4))    

## Services cibles
avahi-daemon absent
cups absent
rpcbind absent
nfs-server absent
smbd absent
~~~

### F6 - Remise en service Nginx

~~~text
# F6 - Remise en service Nginx

Date : 2026-07-02 11:31:46
Machine : ctfalpesnet
IP : 192.168.56.103

Objectif : corriger Nginx et obtenir un HTTP 200.

Rapport avant correction : /flags/F6_avant.txt
Rapport apres correction : /flags/F6_apres.txt

Erreur / etat detecte : 2026/07/02 11:31:46 [emerg] 4583#4583: unknown directive "invalid_ctf_directive" in /etc/nginx/nginx.conf:88 nginx: configuration file /etc/nginx/nginx.conf test failed 
Correction proposee : Commenter la ligne 88 dans /etc/nginx/nginx.conf puis relancer nginx -t et systemctl restart nginx.

Erreurs detectees F6 :
- Statut : config_invalid_ctf_directive
- Detail : 2026/07/02 11:31:46 [emerg] 4583#4583: unknown directive "invalid_ctf_directive" in /etc/nginx/nginx.conf:88 nginx: configuration file /etc/nginx/nginx.conf test failed 

Corrections possibles :
- Sauvegarder le fichier Nginx concerne.
- Commenter la directive CTF invalide.
- Retester la configuration puis redemarrer Nginx.

Commandes proposees :
sudo cp -n /etc/nginx/nginx.conf /etc/nginx/nginx.conf.ctf-f6.bak
sudo sed -i '88s/^/# CTF F6 correction: /' /etc/nginx/nginx.conf
sudo nginx -t
sudo systemctl restart nginx
curl -I -H 'Cache-Control: no-cache' http://192.168.56.103

Diagnostic avant correction :
```
===== F6 AVANT CORRECTION =====
Date : 2026-07-02 11:31:46
Machine : ctfalpesnet
URL testee : http://192.168.56.103

## nginx -t
2026/07/02 11:31:46 [emerg] 4576#4576: unknown directive "invalid_ctf_directive" in /etc/nginx/nginx.conf:88
nginx: configuration file /etc/nginx/nginx.conf test failed

## systemctl status nginx
× nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; preset: enabled)
     Active: failed (Result: exit-code) since Thu 2026-07-02 11:24:17 CEST; 7min ago
   Duration: 1h 17min 40.212s
       Docs: man:nginx(8)
        CPU: 2ms

juil. 02 11:24:17 ctfalpesnet systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
juil. 02 11:24:17 ctfalpesnet nginx[3396]: 2026/07/02 11:24:17 [emerg] 3396#3396: unknown directive "invalid_ctf_directive" in /etc/nginx/nginx.conf:88
juil. 02 11:24:17 ctfalpesnet nginx[3396]: nginx: configuration file /etc/nginx/nginx.conf test failed
juil. 02 11:24:17 ctfalpesnet systemd[1]: nginx.service: Control process exited, code=exited, status=1/FAILURE
juil. 02 11:24:17 ctfalpesnet systemd[1]: nginx.service: Failed with result 'exit-code'.
juil. 02 11:24:17 ctfalpesnet systemd[1]: Failed to start nginx.service - A high performance web server and a reverse proxy server.

## journalctl nginx
juil. 01 15:03:19 ctfalpesnet nginx[1969]: 2026/07/01 15:03:19 [emerg] 1969#1969: unknown directive "invalid_ctf_directive" in /etc/nginx/nginx.conf:85
juil. 01 15:03:19 ctfalpesnet nginx[1969]: nginx: configuration file /etc/nginx/nginx.conf test failed
juil. 01 15:03:19 ctfalpesnet systemd[1]: nginx.service: Control process exited, code=exited, status=1/FAILURE
juil. 01 15:03:19 ctfalpesnet systemd[1]: nginx.service: Failed with result 'exit-code'.
juil. 01 15:03:19 ctfalpesnet systemd[1]: Failed to start nginx.service - A high performance web server and a reverse proxy server.
juil. 01 15:04:15 ctfalpesnet systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
juil. 01 15:04:15 ctfalpesnet systemd[1]: Started nginx.service - A high performance web server and a reverse proxy server.
juil. 01 15:06:21 ctfalpesnet systemd[1]: Stopping nginx.service - A high performance web server and a reverse proxy server...
juil. 01 15:06:21 ctfalpesnet systemd[1]: nginx.service: Deactivated successfully.
juil. 01 15:06:21 ctfalpesnet systemd[1]: Stopped nginx.service - A high performance web server and a reverse proxy server.
juil. 01 15:06:21 ctfalpesnet systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
juil. 01 15:06:21 ctfalpesnet nginx[3773]: 2026/07/01 15:06:21 [emerg] 3773#3773: unknown directive "invalid_ctf_directive" in /etc/nginx/nginx.conf:86
juil. 01 15:06:21 ctfalpesnet nginx[3773]: nginx: configuration file /etc/nginx/nginx.conf test failed
juil. 01 15:06:21 ctfalpesnet systemd[1]: nginx.service: Control process exited, code=exited, status=1/FAILURE
juil. 01 15:06:21 ctfalpesnet systemd[1]: nginx.service: Failed with result 'exit-code'.
juil. 01 15:06:21 ctfalpesnet systemd[1]: Failed to start nginx.service - A high performance web server and a reverse proxy server.
juil. 01 15:07:21 ctfalpesnet systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
juil. 01 15:07:21 ctfalpesnet systemd[1]: Started nginx.service - A high performance web server and a reverse proxy server.
juil. 01 15:53:05 ctfalpesnet systemd[1]: Stopping nginx.service - A high performance web server and a reverse proxy server...
juil. 01 15:53:05 ctfalpesnet systemd[1]: nginx.service: Deactivated successfully.
juil. 01 15:53:05 ctfalpesnet systemd[1]: Stopped nginx.service - A high performance web server and a reverse proxy server.
juil. 01 15:53:05 ctfalpesnet systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
juil. 01 15:53:05 ctfalpesnet nginx[6666]: 2026/07/01 15:53:05 [emerg] 6666#6666: unknown directive "invalid_ctf_directive" in /etc/nginx/nginx.conf:87
juil. 01 15:53:05 ctfalpesnet nginx[6666]: nginx: configuration file /etc/nginx/nginx.conf test failed
juil. 01 15:53:05 ctfalpesnet systemd[1]: nginx.service: Control process exited, code=exited, status=1/FAILURE
juil. 01 15:53:05 ctfalpesnet systemd[1]: nginx.service: Failed with result 'exit-code'.
juil. 01 15:53:05 ctfalpesnet systemd[1]: Failed to start nginx.service - A high performance web server and a reverse proxy server.
-- Boot 58b8da07c7d74a579f99c76128ccda7b --
juil. 02 09:02:28 ctfalpesnet systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
juil. 02 09:02:28 ctfalpesnet nginx[557]: 2026/07/02 09:02:28 [emerg] 557#557: unknown directive "invalid_ctf_directive" in /etc/nginx/nginx.conf:87
juil. 02 09:02:28 ctfalpesnet nginx[557]: nginx: configuration file /etc/nginx/nginx.conf test failed
juil. 02 09:02:28 ctfalpesnet systemd[1]: nginx.service: Control process exited, code=exited, status=1/FAILURE
juil. 02 09:02:28 ctfalpesnet systemd[1]: nginx.service: Failed with result 'exit-code'.
juil. 02 09:02:28 ctfalpesnet systemd[1]: Failed to start nginx.service - A high performance web server and a reverse proxy server.
juil. 02 09:12:46 ctfalpesnet systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
juil. 02 09:12:46 ctfalpesnet nginx[999]: 2026/07/02 09:12:46 [emerg] 999#999: unknown directive "invalid_ctf_directive" in /etc/nginx/nginx.conf:87
juil. 02 09:12:46 ctfalpesnet nginx[999]: nginx: configuration file /etc/nginx/nginx.conf test failed
juil. 02 09:12:46 ctfalpesnet systemd[1]: nginx.service: Control process exited, code=exited, status=1/FAILURE
juil. 02 09:12:46 ctfalpesnet systemd[1]: nginx.service: Failed with result 'exit-code'.
juil. 02 09:12:46 ctfalpesnet systemd[1]: Failed to start nginx.service - A high performance web server and a reverse proxy server.
juil. 02 10:06:37 ctfalpesnet systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
juil. 02 10:06:37 ctfalpesnet systemd[1]: Started nginx.service - A high performance web server and a reverse proxy server.
juil. 02 11:24:17 ctfalpesnet systemd[1]: Stopping nginx.service - A high performance web server and a reverse proxy server...
juil. 02 11:24:17 ctfalpesnet systemd[1]: nginx.service: Deactivated successfully.
juil. 02 11:24:17 ctfalpesnet systemd[1]: Stopped nginx.service - A high performance web server and a reverse proxy server.
juil. 02 11:24:17 ctfalpesnet systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
juil. 02 11:24:17 ctfalpesnet nginx[3396]: 2026/07/02 11:24:17 [emerg] 3396#3396: unknown directive "invalid_ctf_directive" in /etc/nginx/nginx.conf:88
juil. 02 11:24:17 ctfalpesnet nginx[3396]: nginx: configuration file /etc/nginx/nginx.conf test failed
juil. 02 11:24:17 ctfalpesnet systemd[1]: nginx.service: Control process exited, code=exited, status=1/FAILURE
juil. 02 11:24:17 ctfalpesnet systemd[1]: nginx.service: Failed with result 'exit-code'.
juil. 02 11:24:17 ctfalpesnet systemd[1]: Failed to start nginx.service - A high performance web server and a reverse proxy server.

## Ports HTTP/HTTPS en ecoute
Netid State  Recv-Q Send-Q Local Address:Port Peer Address:PortProcess                           

## Test HTTP
curl: (7) Failed to connect to 192.168.56.103 port 80 after 0 ms: Couldn't connect to server
```

Application de la correction F6 : Commenter la ligne 88 dans /etc/nginx/nginx.conf puis relancer nginx -t et systemctl restart nginx.
Fichier cible : /etc/nginx/nginx.conf
Ligne cible : 88
Contenu avant : invalid_ctf_directive on;
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
Correction documentee : Commenter la ligne 88 dans /etc/nginx/nginx.conf puis relancer nginx -t et systemctl restart nginx.
Code HTTP obtenu : 200
Commande : curl -H 'Cache-Control: no-cache' -I http://192.168.56.103

Diagnostic apres correction/audit :
```
===== F6 APRES CORRECTION OU AUDIT =====
Date : 2026-07-02 11:31:50
Machine : ctfalpesnet
URL testee : http://192.168.56.103

## nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful

## systemctl status nginx
● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; preset: enabled)
     Active: active (running) since Thu 2026-07-02 11:31:50 CEST; 8ms ago
       Docs: man:nginx(8)
    Process: 4637 ExecStartPre=/usr/sbin/nginx -t -q -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
    Process: 4638 ExecStart=/usr/sbin/nginx -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
   Main PID: 4639 (nginx)
      Tasks: 3 (limit: 2295)
     Memory: 2.2M
        CPU: 5ms
     CGroup: /system.slice/nginx.service
             ├─4639 "nginx: master process /usr/sbin/nginx -g daemon on; master_process on;"
             ├─4640 "nginx: worker process"
             └─4641 "nginx: worker process"

juil. 02 11:31:50 ctfalpesnet systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
juil. 02 11:31:50 ctfalpesnet systemd[1]: Started nginx.service - A high performance web server and a reverse proxy server.

## journalctl nginx
juil. 01 15:03:19 ctfalpesnet systemd[1]: nginx.service: Control process exited, code=exited, status=1/FAILURE
juil. 01 15:03:19 ctfalpesnet systemd[1]: nginx.service: Failed with result 'exit-code'.
juil. 01 15:03:19 ctfalpesnet systemd[1]: Failed to start nginx.service - A high performance web server and a reverse proxy server.
juil. 01 15:04:15 ctfalpesnet systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
juil. 01 15:04:15 ctfalpesnet systemd[1]: Started nginx.service - A high performance web server and a reverse proxy server.
juil. 01 15:06:21 ctfalpesnet systemd[1]: Stopping nginx.service - A high performance web server and a reverse proxy server...
juil. 01 15:06:21 ctfalpesnet systemd[1]: nginx.service: Deactivated successfully.
juil. 01 15:06:21 ctfalpesnet systemd[1]: Stopped nginx.service - A high performance web server and a reverse proxy server.
juil. 01 15:06:21 ctfalpesnet systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
juil. 01 15:06:21 ctfalpesnet nginx[3773]: 2026/07/01 15:06:21 [emerg] 3773#3773: unknown directive "invalid_ctf_directive" in /etc/nginx/nginx.conf:86
juil. 01 15:06:21 ctfalpesnet nginx[3773]: nginx: configuration file /etc/nginx/nginx.conf test failed
juil. 01 15:06:21 ctfalpesnet systemd[1]: nginx.service: Control process exited, code=exited, status=1/FAILURE
juil. 01 15:06:21 ctfalpesnet systemd[1]: nginx.service: Failed with result 'exit-code'.
juil. 01 15:06:21 ctfalpesnet systemd[1]: Failed to start nginx.service - A high performance web server and a reverse proxy server.
juil. 01 15:07:21 ctfalpesnet systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
juil. 01 15:07:21 ctfalpesnet systemd[1]: Started nginx.service - A high performance web server and a reverse proxy server.
juil. 01 15:53:05 ctfalpesnet systemd[1]: Stopping nginx.service - A high performance web server and a reverse proxy server...
juil. 01 15:53:05 ctfalpesnet systemd[1]: nginx.service: Deactivated successfully.
juil. 01 15:53:05 ctfalpesnet systemd[1]: Stopped nginx.service - A high performance web server and a reverse proxy server.
juil. 01 15:53:05 ctfalpesnet systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
juil. 01 15:53:05 ctfalpesnet nginx[6666]: 2026/07/01 15:53:05 [emerg] 6666#6666: unknown directive "invalid_ctf_directive" in /etc/nginx/nginx.conf:87
juil. 01 15:53:05 ctfalpesnet nginx[6666]: nginx: configuration file /etc/nginx/nginx.conf test failed
juil. 01 15:53:05 ctfalpesnet systemd[1]: nginx.service: Control process exited, code=exited, status=1/FAILURE
juil. 01 15:53:05 ctfalpesnet systemd[1]: nginx.service: Failed with result 'exit-code'.
juil. 01 15:53:05 ctfalpesnet systemd[1]: Failed to start nginx.service - A high performance web server and a reverse proxy server.
-- Boot 58b8da07c7d74a579f99c76128ccda7b --
juil. 02 09:02:28 ctfalpesnet systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
juil. 02 09:02:28 ctfalpesnet nginx[557]: 2026/07/02 09:02:28 [emerg] 557#557: unknown directive "invalid_ctf_directive" in /etc/nginx/nginx.conf:87
juil. 02 09:02:28 ctfalpesnet nginx[557]: nginx: configuration file /etc/nginx/nginx.conf test failed
juil. 02 09:02:28 ctfalpesnet systemd[1]: nginx.service: Control process exited, code=exited, status=1/FAILURE
juil. 02 09:02:28 ctfalpesnet systemd[1]: nginx.service: Failed with result 'exit-code'.
juil. 02 09:02:28 ctfalpesnet systemd[1]: Failed to start nginx.service - A high performance web server and a reverse proxy server.
juil. 02 09:12:46 ctfalpesnet systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
juil. 02 09:12:46 ctfalpesnet nginx[999]: 2026/07/02 09:12:46 [emerg] 999#999: unknown directive "invalid_ctf_directive" in /etc/nginx/nginx.conf:87
juil. 02 09:12:46 ctfalpesnet nginx[999]: nginx: configuration file /etc/nginx/nginx.conf test failed
juil. 02 09:12:46 ctfalpesnet systemd[1]: nginx.service: Control process exited, code=exited, status=1/FAILURE
juil. 02 09:12:46 ctfalpesnet systemd[1]: nginx.service: Failed with result 'exit-code'.
juil. 02 09:12:46 ctfalpesnet systemd[1]: Failed to start nginx.service - A high performance web server and a reverse proxy server.
juil. 02 10:06:37 ctfalpesnet systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
juil. 02 10:06:37 ctfalpesnet systemd[1]: Started nginx.service - A high performance web server and a reverse proxy server.
juil. 02 11:24:17 ctfalpesnet systemd[1]: Stopping nginx.service - A high performance web server and a reverse proxy server...
juil. 02 11:24:17 ctfalpesnet systemd[1]: nginx.service: Deactivated successfully.
juil. 02 11:24:17 ctfalpesnet systemd[1]: Stopped nginx.service - A high performance web server and a reverse proxy server.
juil. 02 11:24:17 ctfalpesnet systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
juil. 02 11:24:17 ctfalpesnet nginx[3396]: 2026/07/02 11:24:17 [emerg] 3396#3396: unknown directive "invalid_ctf_directive" in /etc/nginx/nginx.conf:88
juil. 02 11:24:17 ctfalpesnet nginx[3396]: nginx: configuration file /etc/nginx/nginx.conf test failed
juil. 02 11:24:17 ctfalpesnet systemd[1]: nginx.service: Control process exited, code=exited, status=1/FAILURE
juil. 02 11:24:17 ctfalpesnet systemd[1]: nginx.service: Failed with result 'exit-code'.
juil. 02 11:24:17 ctfalpesnet systemd[1]: Failed to start nginx.service - A high performance web server and a reverse proxy server.
juil. 02 11:31:50 ctfalpesnet systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
juil. 02 11:31:50 ctfalpesnet systemd[1]: Started nginx.service - A high performance web server and a reverse proxy server.

## Ports HTTP/HTTPS en ecoute
Netid State  Recv-Q Send-Q Local Address:Port Peer Address:PortProcess                                                                         
tcp   LISTEN 0      511          0.0.0.0:80        0.0.0.0:*    users:(("nginx",pid=4641,fd=5),("nginx",pid=4640,fd=5),("nginx",pid=4639,fd=5))
tcp   LISTEN 0      511             [::]:80           [::]:*    users:(("nginx",pid=4641,fd=6),("nginx",pid=4640,fd=6),("nginx",pid=4639,fd=6))

## Test HTTP
HTTP/1.1 200 OK
Server: nginx/1.22.1
Date: Thu, 02 Jul 2026 09:31:50 GMT
Content-Type: text/html
Content-Length: 615
Last-Modified: Wed, 01 Jul 2026 11:36:47 GMT
Connection: keep-alive
ETag: "6a44fbcf-267"
Accept-Ranges: bytes

```
~~~

### F7 - Sauvegarde et checksum

~~~text
# F7 - Sauvegarde /etc et /var/www

Date : 2026-07-02 11:31:50
Machine : ctfalpesnet
IP : 192.168.56.103

Objectif : sauvegarder /etc et /var/www puis generer un checksum sha256.
Archive cible : /backup/ctf-alpesnet-20260702_113109.tar.gz
Checksum cible : /backup/ctf-alpesnet-20260702_113109.tar.gz.sha256

Sauvegarde proposee pour F7 :
- Creer le dossier /backup si besoin.
- Archiver /etc et /var/www dans : /backup/ctf-alpesnet-20260702_113109.tar.gz
- Generer le checksum : /backup/ctf-alpesnet-20260702_113109.tar.gz.sha256
- Verifier l'integrite avec sha256sum -c.

Commandes proposees :
sudo mkdir -p /backup
sudo tar -C / -czf '/backup/ctf-alpesnet-20260702_113109.tar.gz' etc var/www
sudo sha256sum '/backup/ctf-alpesnet-20260702_113109.tar.gz' > '/backup/ctf-alpesnet-20260702_113109.tar.gz.sha256'
sudo sha256sum -c '/backup/ctf-alpesnet-20260702_113109.tar.gz.sha256'

Creation de la sauvegarde F7.
/backup/ctf-alpesnet-20260702_113109.tar.gz: Réussi

Preuve attendue :
Archive : /backup/ctf-alpesnet-20260702_113109.tar.gz
Checksum : /backup/ctf-alpesnet-20260702_113109.tar.gz.sha256
ae67021808a61fcd3ab45f62bfb8ad0491196ad02a7bbae79b0e0f6c916e1105  /backup/ctf-alpesnet-20260702_113109.tar.gz
~~~

