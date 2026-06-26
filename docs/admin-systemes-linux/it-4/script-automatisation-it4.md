# Script d'automatisation - Itération 4 AlpesNet

## Objectif

Ce script reprend les exercices de l'itération 4 :

- configuration du partage NFS AlpesNet ;
- configuration du partage Samba AlpesNet ;
- durcissement SSH ;
- configuration UFW ;
- configuration Fail2ban ;
- vérifications avant/après ;
- génération d'un log final avec commandes, résultats et explications.

Le livrable principal est un rapport Markdown généré automatiquement dans :

```text
/var/log/alpesnet-it4/
```

Pendant l'exécution, le script affiche aussi l'avancement en direct :

```text
[01] Installer les paquets necessaires
     Commande: apt-get update && apt-get install -y ...
     Execution...
     Statut: OK
     Rapport mis a jour: /var/log/alpesnet-it4/rapport-it4-YYYYMMDD_HHMMSS.md
```

## Fichier du script

Le script est disponible ici :

[alpesnet-it4-exercices.sh](../../assets/scripts/admin-systemes-linux/it-4/alpesnet-it4-exercices.sh)

Pour l'utiliser sur la VM Debian, copier ou télécharger le fichier, puis le rendre exécutable :

```bash
chmod +x alpesnet-it4-exercices.sh
```

## Étape 1 - Lire les variables importantes

Avant exécution, adapter les variables suivantes.

| Variable | Rôle | Exemple |
| --- | --- | --- |
| `CAMPUS_SUBNET` | Sous-réseau autorisé pour SSH, NFS et Samba | `192.168.56.0/24` |
| `SSH_ALLOW_USERS` | Comptes autorisés en SSH après durcissement | `"adm-oliv oliv"` |
| `CONFIRM_SSH_KEYS` | Confirmation que les clés SSH sont prêtes | `yes` |
| `CONFIRM_UFW` | Confirmation que le sous-réseau UFW est correct | `yes` |
| `SAMBA_PASSWORD` | Mot de passe Samba de test pour Alice et Bob | `AlpesNet-2026!` |

!!! warning "Sécurité SSH"
    Le script refuse de désactiver l'authentification par mot de passe si `CONFIRM_SSH_KEYS=yes` n'est pas fourni. Il vérifie aussi qu'au moins un utilisateur autorisé possède un fichier `authorized_keys`.

!!! warning "Sécurité UFW"
    Le script refuse d'activer UFW si `CONFIRM_UFW=yes` n'est pas fourni. Vérifier le sous-réseau avant de lancer, sinon SSH peut être bloqué.

## Étape 2 - Faire un dry-run

Le dry-run génère le rapport sans appliquer les commandes.

```bash
sudo ./alpesnet-it4-exercices.sh --dry-run
```

Résultat attendu :

```text
Done.
Report: /var/log/alpesnet-it4/rapport-it4-YYYYMMDD_HHMMSS.md
Raw log: /var/log/alpesnet-it4/execution-it4-YYYYMMDD_HHMMSS.log
```

## Étape 3 - Lancer le script complet

Exemple adapté au lab VirtualBox :

```bash
sudo CONFIRM_SSH_KEYS=yes \
  CONFIRM_UFW=yes \
  SSH_ALLOW_USERS="adm-oliv oliv" \
  CAMPUS_SUBNET="192.168.56.0/24" \
  ./alpesnet-it4-exercices.sh --client-tests
```

Explication :

| Option | Rôle |
| --- | --- |
| `CONFIRM_SSH_KEYS=yes` | autorise le script à appliquer `PasswordAuthentication no` |
| `CONFIRM_UFW=yes` | autorise le script à activer le pare-feu |
| `SSH_ALLOW_USERS` | évite de bloquer le compte d'administration |
| `CAMPUS_SUBNET` | limite les accès réseau au lab |
| `--client-tests` | ajoute des tests locaux NFS/Samba depuis le serveur |

## Étape 4 - Ce que le script exécute

### Préparation

- installe `nfs-kernel-server`, `nfs-common`, `samba`, `smbclient`, `fail2ban` et `ufw` ;
- capture les ports avant dans `/tmp/ports-avant.txt` ;
- capture les services actifs avant dans `/tmp/services-avant.txt` ;
- prépare `alice.martin`, `bob.dupont` et le groupe `devops`.

### NFS

- crée `/exports/projets-alpesnet` ;
- applique `alice.martin:devops` ;
- applique les droits `770` ;
- configure `/etc/exports` avec :

```text
/exports/projets-alpesnet  CAMPUS_SUBNET(rw,sync,no_subtree_check,root_squash)
```

- recharge les exports avec `exportfs -arv` ;
- démarre `nfs-kernel-server` ;
- teste la création de fichier par Alice ;
- teste le refus attendu pour Bob.

### Samba

- crée `/samba/equipe` ;
- applique `root:devops` ;
- applique les droits `1770` ;
- configure le partage `[equipe-alpesnet]` ;
- ajoute Alice et Bob dans la base Samba ;
- valide `testparm -s` ;
- teste l'accès autorisé d'Alice ;
- teste le refus attendu pour Bob.

### Durcissement

- sauvegarde `sshd_config` ;
- écrit le durcissement dans `/etc/ssh/sshd_config.d/99-alpesnet-hardening.conf` ;
- vérifie `sshd -t` ;
- recharge SSH ;
- configure UFW avec une politique entrante restrictive ;
- configure Fail2ban pour la jail `sshd` ;
- liste les services à analyser ;
- désactive `avahi-daemon` si présent ;
- capture les ports après dans `/tmp/ports-apres.txt` ;
- produit un `diff` avant/après.

## Étape 5 - Lire le rapport final

Lister les rapports :

```bash
sudo ls -lh /var/log/alpesnet-it4/
```

Lire le dernier rapport :

```bash
sudo less /var/log/alpesnet-it4/rapport-it4-*.md
```

Chaque bloc contient :

- le titre de l'étape ;
- la commande exécutée ;
- le code retour ;
- la sortie de commande ;
- l'explication pédagogique.

## Étape 6 - Tests à garder manuels

Le script automatise la majorité des preuves, mais deux tests restent mieux à faire manuellement :

| Test | Pourquoi |
| --- | --- |
| Connexion SSH depuis un nouveau terminal | éviter de fermer la session active avant validation |
| Bannissement Fail2ban depuis le laptop | un vrai ban doit venir d'un client externe |

Commandes utiles :

```bash
ssh root@[IP-VM]
ssh adm-oliv@[IP-VM]
sudo fail2ban-client status sshd
sudo fail2ban-client set sshd unbanip [IP-CLIENT]
```

## Dépannage - Fail2ban socket absent

Si le rapport affiche :

```text
Failed to access socket path: /var/run/fail2ban/fail2ban.sock. Is fail2ban running?
```

Cela signifie généralement que Fail2ban n'a pas démarré. La cause la plus fréquente dans ce TP est un ancien fichier `/etc/fail2ban/jail.local` incomplet ou incorrect.

Le script sauvegarde maintenant cet ancien fichier sous la forme :

```text
/etc/fail2ban/jail.local.bak.YYYYMMDD_HHMMSS
/etc/fail2ban/jail.local.disabled.YYYYMMDD_HHMMSS
```

Puis il crée une configuration propre dans :

```text
/etc/fail2ban/jail.d/alpesnet-sshd.local
```

Commandes utiles pour diagnostiquer :

```bash
sudo fail2ban-client -t
sudo systemctl status fail2ban
sudo journalctl -u fail2ban -n 80 --no-pager
```

## Résultat attendu

À la fin, le dossier `/var/log/alpesnet-it4/` contient :

| Fichier | Contenu |
| --- | --- |
| `rapport-it4-YYYYMMDD_HHMMSS.md` | rapport final lisible pour le dossier |
| `execution-it4-YYYYMMDD_HHMMSS.log` | log brut complet |

Le rapport final montre les commandes exécutées, leurs résultats et l'explication de chaque mesure.
