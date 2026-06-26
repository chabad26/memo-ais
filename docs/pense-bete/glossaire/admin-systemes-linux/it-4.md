# Glossaire Systèmes Linux - Itération 4

## Sujet

Services Linux et durcissement : partage NFS AlpesNet, partage Samba SMB/CIFS, durcissement SSH, UFW, Fail2ban et sécurité des accès.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| NFS | Network File System, service permettant de monter à distance un répertoire exporté par un serveur Linux. |
| Export | Répertoire serveur rendu accessible aux clients NFS. |
| `/etc/exports` | Fichier de configuration des répertoires exportés par NFS. |
| `exportfs` | Commande qui applique, recharge et affiche les exports NFS. |
| Client NFS | Machine qui monte un export NFS dans son arborescence locale. |
| Point de montage | Dossier local où apparaît le partage distant, par exemple `/mnt/alpesnet-projets`. |
| `nfs-kernel-server` | Paquet serveur NFS sur Debian/Ubuntu. |
| `nfs-common` | Paquet client nécessaire pour monter un partage NFS. |
| `root_squash` | Option qui transforme le root du client en utilisateur non privilégié côté serveur. |
| `sync` | Option qui force les écritures synchrones, plus sûre que `async`. |
| `no_subtree_check` | Option qui évite certains problèmes de vérification de sous-arborescence. |
| Samba | Service Linux qui implémente SMB/CIFS pour partager des fichiers avec Windows ou Linux. |
| SMB/CIFS | Protocole de partage de fichiers utilisé notamment par Windows. |
| `smb.conf` | Fichier principal de configuration Samba. |
| `smbpasswd` | Commande qui ajoute ou modifie un utilisateur dans la base Samba. |
| `testparm` | Commande qui vérifie la syntaxe de la configuration Samba. |
| `smbclient` | Client en ligne de commande pour lister ou utiliser un partage SMB. |
| Sticky bit | Droit spécial empêchant un utilisateur de supprimer les fichiers des autres dans un dossier partagé. |
| Durcissement | Ensemble de mesures qui réduisent la surface d'attaque d'un serveur. |
| `PermitRootLogin no` | Paramètre SSH qui interdit la connexion directe du compte `root`. |
| `PasswordAuthentication no` | Paramètre SSH qui impose l'authentification par clés. |
| `AllowUsers` | Liste blanche des utilisateurs autorisés en SSH. |
| UFW | Pare-feu simplifié pour gérer les règles réseau Linux. |
| Fail2ban | Outil qui bannit automatiquement les IP après trop d'échecs d'authentification. |
| Jail Fail2ban | Bloc de configuration qui surveille un service précis, par exemple `sshd`. |
| Surface d'attaque | Ensemble des services, ports et accès exposés à un attaquant. |

## Manipulations faites

| Manipulation | Commandes ou actions |
| --- | --- |
| Créer l'export | `mkdir -p /exports/projets-alpesnet`, `chown`, `chmod 770`. |
| Configurer NFS | Modifier `/etc/exports` avec le sous-réseau autorisé. |
| Appliquer les exports | `sudo exportfs -arv`, `sudo exportfs -v`. |
| Activer le service | `systemctl enable --now nfs-kernel-server`. |
| Restreindre avec ufw | `sudo ufw allow from 192.168.0.0/24 to any port nfs`. |
| Monter côté client | `sudo mount [IP-SERVEUR]:/exports/projets-alpesnet /mnt/alpesnet-projets`. |
| Vérifier le montage | `df -h | grep nfs`, `mount | grep alpesnet-projets`. |
| Tester les droits | Créer un fichier avec `alice.martin`, vérifier côté client et serveur. |
| Tester `root_squash` | Tenter `sudo touch` depuis le client et vérifier le refus attendu. |
| Créer un partage Samba | Configurer `[equipe-alpesnet]` dans `/etc/samba/smb.conf`. |
| Restreindre Samba | `valid users = @devops` pour limiter l'accès au groupe. |
| Ajouter un utilisateur Samba | `sudo smbpasswd -a alice.martin`. |
| Tester Samba | `smbclient -L //[IP] -U alice.martin`, puis connexion au partage. |
| Refuser un utilisateur | Tester `bob.dupont` et vérifier `NT_STATUS_ACCESS_DENIED`. |
| Capturer l'état avant | `ss -tulnp`, `systemctl list-units --type=service --state=active`. |
| Durcir SSH | `PermitRootLogin no`, `PasswordAuthentication no`, `AllowUsers adm-[prenom]`. |
| Vérifier SSH | `sudo sshd -t`, puis test depuis un nouveau terminal. |
| Filtrer avec UFW | `ufw default deny incoming`, règle SSH limitée au sous-réseau campus. |
| Protéger avec Fail2ban | jail `sshd`, `maxretry = 3`, test de ban contrôlé. |
| Comparer avant/après | `diff /tmp/ports-avant.txt /tmp/ports-apres.txt`. |
| Générer le rapport automatisé | Lancer `alpesnet-it4-exercices.sh` pour produire un log commande/résultat/explication. |

## Point clé sécurité : `root_squash`

`root_squash` évite que le compte `root` du client NFS puisse agir comme `root` sur le serveur. C'est une protection importante, car NFS s'appuie beaucoup sur les UID/GID et les droits Unix.

Ligne type :

```text
/exports/projets-alpesnet  192.168.0.0/24(rw,sync,no_subtree_check,root_squash)
```

À retenir :

- limiter l'export au bon sous-réseau ;
- garder des droits Unix restrictifs ;
- tester depuis un vrai client ;
- vérifier que root côté client ne contourne pas les droits serveur.

## Point clé Samba : compte Linux + compte Samba

Samba utilise les comptes Linux comme base, mais un compte Linux ne suffit pas. Chaque utilisateur autorisé doit aussi exister dans la base Samba.

Exemple :

```bash
sudo smbpasswd -a alice.martin
```

À retenir :

- le compte Linux doit exister ;
- le compte Samba doit être créé avec `smbpasswd` ;
- le partage doit restreindre l'accès avec `valid users = @devops` ;
- les droits Unix du dossier `/samba/equipe` restent appliqués.

## Point clé durcissement : tester avant de fermer

Avant de recharger SSH ou d'activer UFW, garder la session active ouverte et tester depuis un nouveau terminal.

À retenir :

- `sudo sshd -t` doit ne rien afficher ;
- `root` doit être refusé ;
- l'utilisateur `adm-[prenom]` doit passer avec clé SSH ;
- UFW doit limiter le port 22 au sous-réseau prévu ;
- Fail2ban doit montrer une IP bannie après les tentatives échouées ;
- le rapport doit comparer l'état avant et l'état après.

## Docs associées

- [Vue d'ensemble itération 4](../../../admin-systemes-linux/it-4/index.md)
- [NFS AlpesNet - partage réseau Linux](../../../admin-systemes-linux/it-4/nfs-alpesnet.md)
- [Samba AlpesNet - partage SMB/CIFS](../../../admin-systemes-linux/it-4/samba-alpesnet.md)
- [Durcissement Linux AlpesNet](../../../admin-systemes-linux/it-4/durcissement-linux-alpesnet.md)
- [Rapport de durcissement Linux AlpesNet](../../../admin-systemes-linux/it-4/rapport-durcissement-linux-alpesnet.md)
- [Script automatisation Itération 4](../../../admin-systemes-linux/it-4/script-automatisation-it4.md)
