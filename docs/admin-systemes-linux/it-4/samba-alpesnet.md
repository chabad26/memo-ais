# Samba AlpesNet - partage SMB/CIFS

## Objectif

Configurer un partage Samba pour l'équipe AlpesNet, accessible uniquement aux membres du groupe `devops`, puis valider qu'un utilisateur autorisé peut créer des fichiers alors qu'un utilisateur non autorisé est refusé.

Samba implémente le protocole **SMB/CIFS**, utilisé pour partager des fichiers avec des clients Windows ou Linux. Contrairement à NFS, Samba possède sa propre base d'utilisateurs : un compte Linux doit exister, mais il faut aussi l'ajouter à Samba avec `smbpasswd`.

## Architecture de l'atelier

| Élément | Rôle | Exemple |
| --- | --- | --- |
| Serveur Samba | VM Debian 12 AlpesNet | `[IP-SERVEUR]` |
| Client de test | Ubuntu 24.04 ou client Windows/Linux | même réseau de lab |
| Groupe autorisé | Groupe Linux autorisé | `devops` |
| Partage Samba | Nom visible côté client | `equipe-alpesnet` |
| Dossier serveur | Répertoire réellement partagé | `/samba/equipe` |
| Utilisateur autorisé | Membre du groupe `devops` | `alice.martin` |
| Utilisateur refusé | Hors groupe `devops` | `bob.dupont` |

!!! warning "Comptes Samba"
    Un utilisateur Samba doit d'abord exister comme compte Linux local, puis être ajouté dans la base Samba avec `sudo smbpasswd -a utilisateur`. Le mot de passe Samba peut être différent du mot de passe Linux.

## Étape 1 - Installer Samba et les outils client

Sur le serveur :

```bash
sudo apt update
sudo apt install -y samba smbclient
```

Vérifier les services disponibles :

```bash
systemctl status smbd
systemctl status nmbd
```

Si les services ne sont pas encore démarrés, ce sera fait après la configuration.

## Étape 2 - Vérifier les comptes et le groupe `devops`

Vérifier que les utilisateurs Linux existent :

```bash
getent passwd alice.martin
getent passwd bob.dupont
```

Vérifier le groupe `devops` :

```bash
getent group devops
id alice.martin
id bob.dupont
```

Résultat attendu :

- `alice.martin` doit être membre du groupe `devops` ;
- `bob.dupont` ne doit pas être membre de `devops`.

Si besoin :

```bash
sudo usermod -aG devops alice.martin
```

!!! note "Session utilisateur"
    Après modification de groupe, l'utilisateur doit rouvrir sa session pour que l'appartenance soit prise en compte.

## Étape 3 - Créer le répertoire partagé

Créer le dossier :

```bash
sudo mkdir -p /samba/equipe
```

Attribuer le groupe :

```bash
sudo chown root:devops /samba/equipe
```

Appliquer les droits :

```bash
sudo chmod 1770 /samba/equipe
```

Vérifier :

```bash
ls -ld /samba/equipe
```

Résultat attendu :

```text
drwxrwx--T ... root devops ... /samba/equipe
```

Explication :

| Élément | Rôle |
| --- | --- |
| `1` dans `1770` | active le sticky bit |
| `7` propriétaire | `root` a tous les droits |
| `7` groupe | les membres de `devops` peuvent lire, écrire et traverser |
| `0` autres | aucun accès pour les autres utilisateurs |
| sticky bit | seul le propriétaire d'un fichier, le propriétaire du dossier ou root peut supprimer ce fichier |

## Étape 4 - Sauvegarder la configuration Samba

Avant modification :

```bash
sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.bak
```

Vérifier la sauvegarde :

```bash
ls -l /etc/samba/smb.conf /etc/samba/smb.conf.bak
```

## Étape 5 - Configurer le partage dans `smb.conf`

Éditer le fichier :

```bash
sudo vim /etc/samba/smb.conf
```

Ajouter à la fin :

```ini
[equipe-alpesnet]
   comment = Partage équipe AlpesNet
   path = /samba/equipe
   browseable = yes
   writable = yes
   valid users = @devops
   create mask = 0664
   directory mask = 0775
```

Explication :

| Directive | Rôle |
| --- | --- |
| `[equipe-alpesnet]` | nom du partage visible côté client |
| `comment` | description du partage |
| `path` | chemin local réellement partagé |
| `browseable = yes` | le partage peut être listé |
| `writable = yes` | autorise l'écriture |
| `valid users = @devops` | seuls les membres du groupe `devops` sont autorisés |
| `create mask = 0664` | permissions par défaut des fichiers créés |
| `directory mask = 0775` | permissions par défaut des dossiers créés |

!!! info "Différence droits Unix / droits Samba"
    Samba vérifie d'abord ses règles d'accès, puis le système Linux applique aussi les permissions du dossier. Il faut donc que `valid users = @devops` et les droits Unix `/samba/equipe` soient cohérents.

## Étape 6 - Vérifier la configuration avec `testparm`

Lancer :

```bash
sudo testparm -s
```

Résultat attendu :

- aucune erreur bloquante ;
- le partage `[equipe-alpesnet]` apparaît ;
- `valid users = @devops` est bien présent.

Si `testparm` signale une erreur, corriger `smb.conf` avant de démarrer le service.

## Étape 7 - Créer l'utilisateur Samba autorisé

Ajouter `alice.martin` dans la base Samba :

```bash
sudo smbpasswd -a alice.martin
```

Activer le compte si nécessaire :

```bash
sudo smbpasswd -e alice.martin
```

Lister les utilisateurs Samba :

```bash
sudo pdbedit -L
```

!!! note "Compte Linux obligatoire"
    `smbpasswd -a alice.martin` échoue si `alice.martin` n'existe pas comme utilisateur Linux local.

## Étape 8 - Démarrer et activer Samba

Démarrer les services :

```bash
sudo systemctl enable --now smbd nmbd
```

Vérifier :

```bash
systemctl status smbd
systemctl status nmbd
```

Si `ufw` est actif :

```bash
sudo ufw allow samba
sudo ufw status numbered
```

!!! warning "Filtrage réseau"
    En production, éviter d'ouvrir Samba à tous les réseaux. Limiter l'accès au sous-réseau d'administration ou au VLAN prévu quand c'est possible.

## Étape 9 - Lister les partages depuis un client Linux

Depuis le client :

```bash
smbclient -L //[IP-SERVEUR] -U alice.martin
```

Exemple :

```bash
smbclient -L //192.168.56.102 -U alice.martin
```

Résultat attendu : le partage `equipe-alpesnet` apparaît dans la liste.

## Étape 10 - Se connecter au partage avec `alice.martin`

Depuis le client :

```bash
smbclient //[IP-SERVEUR]/equipe-alpesnet -U alice.martin
```

Dans l'invite `smb: \>` :

```text
ls
put test-samba-alice.txt
ls
quit
```

Pour créer rapidement un fichier local à envoyer :

```bash
echo "test samba alice" > test-samba-alice.txt
smbclient //[IP-SERVEUR]/equipe-alpesnet -U alice.martin -c "put test-samba-alice.txt; ls"
```

Vérifier côté serveur :

```bash
sudo ls -l /samba/equipe
```

Résultat attendu : `alice.martin` peut se connecter et déposer un fichier dans le partage.

## Étape 11 - Vérifier que `bob.dupont` est refusé

Tester la connexion avec `bob.dupont` :

```bash
smbclient //[IP-SERVEUR]/equipe-alpesnet -U bob.dupont
```

Résultat attendu :

```text
NT_STATUS_ACCESS_DENIED
```

ou un message équivalent indiquant que l'accès est refusé.

Ce refus est normal si `bob.dupont` n'est pas membre du groupe `devops` ou s'il n'a pas de compte Samba autorisé.

## Étape 12 - Vérifier les logs Samba

Sur le serveur :

```bash
sudo tail /var/log/samba/log.smbd | grep "alice\|bob"
```

Si aucune ligne ne sort, inspecter les fichiers de logs disponibles :

```bash
sudo ls -l /var/log/samba/
sudo grep -R "alice\|bob" /var/log/samba/ | tail -20
```

Résultat attendu :

- les connexions ou tentatives apparaissent dans les logs ;
- les tentatives refusées de `bob.dupont` peuvent être retrouvées selon le niveau de log.

## Exercice 2 - Configurer et sécuriser le partage Samba AlpesNet

Le partage Samba doit être accessible uniquement aux membres du groupe `devops`. `bob.dupont` ne doit pas pouvoir s'y connecter.

Ce que tu dois faire :

1. Configurer `smb.conf` avec le partage `[equipe-alpesnet]` restreint à `@devops`, puis vérifier avec :

```bash
sudo testparm -s
```

2. Créer l'utilisateur Samba `alice.martin` :

```bash
sudo smbpasswd -a alice.martin
```

3. Tester la connexion de `alice.martin` :

```bash
smbclient //[IP]/equipe-alpesnet -U alice.martin
```

Créer un fichier dans le partage.

4. Tenter de se connecter avec `bob.dupont` :

```bash
smbclient //[IP]/equipe-alpesnet -U bob.dupont
```

Noter le message obtenu et vérifier que le refus est attendu.

5. Vérifier les logs Samba :

```bash
sudo tail /var/log/samba/log.smbd | grep "alice\|bob"
```

Résultat attendu :

- `alice.martin` peut se connecter et créer des fichiers ;
- `bob.dupont` est refusé ;
- les tentatives sont visibles dans les logs Samba.

## Preuves à conserver

| Preuve | Commande |
| --- | --- |
| Droits du dossier partagé | `ls -ld /samba/equipe` |
| Bloc de configuration Samba | `grep -A8 "\[equipe-alpesnet\]" /etc/samba/smb.conf` |
| Validation syntaxe | `sudo testparm -s` |
| Utilisateur Samba | `sudo pdbedit -L` |
| Services actifs | `systemctl status smbd nmbd` |
| Liste des partages | `smbclient -L //[IP-SERVEUR] -U alice.martin` |
| Connexion autorisée | `smbclient //[IP-SERVEUR]/equipe-alpesnet -U alice.martin` |
| Refus bob | `smbclient //[IP-SERVEUR]/equipe-alpesnet -U bob.dupont` |
| Logs Samba | `sudo grep -R "alice\|bob" /var/log/samba/` |

## Dépannage rapide

| Symptôme | Vérifications |
| --- | --- |
| `tree connect failed: NT_STATUS_ACCESS_DENIED` | vérifier `valid users`, groupe `devops`, compte Samba |
| `session setup failed` | vérifier mot de passe Samba et existence du compte avec `pdbedit -L` |
| Partage absent dans `smbclient -L` | vérifier `smb.conf`, `testparm`, service `smbd` |
| Écriture refusée | vérifier permissions Unix `/samba/equipe`, `create mask`, groupe Linux |
| Connexion impossible | vérifier IP, firewall, service `smbd`, ports Samba |

## Ressources

- `man smb.conf`
- `man smbpasswd`
- `man testparm`
- [Samba documentation officielle](https://www.samba.org/samba/docs/)
- [Samba - Debian Wiki](https://wiki.debian.org/Samba/ServerSimple)

## Synthèse à retenir

Samba partage des fichiers via SMB/CIFS. Pour sécuriser un partage, il faut aligner trois couches :

1. les permissions Linux du dossier ;
2. les règles Samba dans `smb.conf` ;
3. les utilisateurs Samba créés avec `smbpasswd`.

Un compte Linux seul ne suffit pas pour Samba : il doit aussi exister dans la base Samba.

