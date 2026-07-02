# Validation CTF AlpesNet

## Objectif du sous-module

Ce sous-module sert à valider le challenge final SYS-01a à partir de preuves vérifiables sur la VM CTF AlpesNet compromise.

Le but n'est pas seulement de récupérer des flags. Il faut montrer que l'on sait :

1. identifier un compte non autorisé et des permissions dangereuses ;
2. appliquer un durcissement Linux complet et vérifiable ;
3. produire un rapport d'incident lisible, structuré et contrôlable.

## Livrables utilisés

| Élément | Fichier ou preuve | Rôle |
| --- | --- | --- |
| F2 | `/flags/F2.txt` | Compte intrus identifié |
| F4 | `/flags/F4.txt` | Permission dangereuse identifiée |
| F5 | `/flags/F5.txt`, `/flags/F5_avant.txt`, `/flags/F5_apres.txt` | Durcissement avant/après |
| F8 | `/flags/rapport_Olivier.txt`, `/flags/rapport_Olivier.md` | Rapport d'incident final |

## F1 - Accès root et mot de passe caché

Le formateur a indiqué qu'un mot de passe peut être caché dans la VM. Pour F1, je ne me contente donc pas de dire que je suis root : je montre aussi comment j'ai cherché l'indice.

Ne pas utiliser `.ctf_answer` ou `.ctf_answers` : ce sont les réponses formateur. La recherche doit porter sur les dossiers home et leurs fichiers cachés, par exemple `.bash_history`, `.profile`, `.bashrc`, `.ssh/config` ou d'autres fichiers utilisateur.

Commandes à montrer :

```bash
id
whoami
sudo -l
sshd -T | grep -Ei '^(permitrootlogin|passwordauthentication)'
systemctl is-active ssh || systemctl is-active sshd
ss -tlnp | grep ':22'
ssh root@192.168.56.103
sudo find /home -mindepth 1 -maxdepth 1 -type d ! -name oliv ! -name olivier -print
sudo find /home/investigateur /home/backdoor-sys -xdev -maxdepth 3 -type f -name '.*' ! -name '.ctf_answer' ! -name '.ctf_answers' -printf '%m %u:%g %p\n' 2>/dev/null
sudo grep -RInEi --exclude='.ctf_answer' --exclude='.ctf_answers' 'investigateur|backdoor-sys|Inv3st1g4t3ur!|root.{0,40}(pass|passwd|password|mdp|su|login|secret|credential|creds)|((pass|passwd|password|mdp|su|login|secret|credential|creds).{0,40}root)' /home/investigateur /home/backdoor-sys 2>/dev/null | head -80
```

Si le mot de passe est retrouvé, la méthode F1 à documenter est :

```text
mot de passe caché retrouvé dans la VM puis utilisation de su/root ou ssh root@[IP]
```

Le script accepte aussi une formulation forcée si je veux coller exactement à la correction :

```bash
sudo ./ctf-alpesnet.sh --task F1 --f1-method "mot de passe cache retrouve dans la VM puis su root"
```

## Preuve en direct avec le script

Le script `ctf-alpesnet.sh` affiche une preuve guidée pour chaque étape :

- `=== F? - prerequis, actions et validation ===` : ce qu'il faut avoir avant de lancer l'étape ;
- `[INFO]` : ce que le script va faire ;
- `[OK]` : preuve vérifiée ;
- `[A VERIFIER]` : preuve générée mais contrôle manuel encore nécessaire ;
- `[KO]` : étape inconnue ou erreur bloquante.

Exemple de lancement en mode menu :

```bash
sudo ./ctf-alpesnet.sh --menu --prenom Olivier --ip 192.168.56.103
```

Exemple pour appliquer les corrections qui demandent confirmation :

```bash
sudo ./ctf-alpesnet.sh --all --apply --prenom Olivier --ip 192.168.56.103
```

Pendant la démonstration, je peux lire les prérequis affichés, montrer l'action réalisée, puis m'arrêter sur les lignes `[OK]` ou `[A VERIFIER]` qui prouvent l'état réel de la VM.

## Validation 1 - Comptes et permissions

### But

Identifier des comptes non autorisés et des permissions dangereuses sur un système compromis.

### Critères

Le compte intrus et les permissions dangereuses `777` ou SUID sont identifiés avec les commandes correctes.

### Preuve de travail

Je dois expliquer ce que font les commandes, puis montrer leur résultat sur la VM CTF.

Commandes à montrer :

```bash
awk -F: '($3==0){print $1":"$3":"$6":"$7}' /etc/passwd
getent passwd backdoor-sys
while IFS=: read -r user _ uid _ _ _ _; do
  [ "$uid" -ge 1000 ] || [ "$uid" -eq 0 ] || continue
  printf '%s: %s\n' "$user" "$(id -nG "$user" 2>/dev/null || echo groupes_inaccessibles)"
done < /etc/passwd
sudo find /etc/sudoers.d -maxdepth 1 -type f ! -name '*~' ! -name '*.*' ! -name README \
  -exec grep -Hve '^[[:space:]]*#' -e '^[[:space:]]*$' {} \;
lastlog
sudo stat /home/backdoor-sys
sudo chage -l backdoor-sys
sudo grep -E "useradd|adduser|new user|backdoor-sys" /var/log/auth.log /var/log/syslog 2>/dev/null
lastlog -u backdoor-sys
last backdoor-sys
sudo find / -xdev -perm 0777 -printf '%m %u:%g %p\n' 2>/dev/null
sudo find / -xdev -perm /4000 -printf '%m %u:%g %p\n' 2>/dev/null
stat -c '%a %A %U:%G %n' /var/www/upload
sudo userdel -r backdoor-sys
getent passwd backdoor-sys || echo "Compte absent apres correction"
```

### Explication attendue

`awk -F: '($3==0)' /etc/passwd` lit `/etc/passwd` avec `:` comme séparateur. Le champ 3 correspond à l'UID. Un UID `0` donne les privilèges root. Tout compte UID 0 autre que `root` est donc critique.

`find / -perm /4000` recherche les fichiers qui ont le bit SUID. Un programme SUID s'exécute avec les droits de son propriétaire. Si un binaire inattendu est SUID root, il peut permettre une escalade de privilèges.

`find / -perm 0777` recherche les chemins modifiables par tout le monde. Sur un serveur compromis, un répertoire web en `777`, comme `/var/www/upload`, peut permettre à un attaquant de déposer ou modifier du contenu.

La date de création du compte est estimée par recoupement : date du dossier `/home/backdoor-sys`, informations `chage`, traces `useradd/adduser` dans les logs et premières connexions `lastlog/last`.

`userdel -r backdoor-sys` supprime le compte suspect et son home. `getent passwd backdoor-sys` ne doit plus rien retourner après correction.

### Résultat attendu

| Point contrôlé | Résultat |
| --- | --- |
| Compte intrus | `backdoor-sys` |
| Vérification compte | `getent passwd backdoor-sys` |
| Résultat F2 à expliquer | le compte existe, possède un shell/home cohérent avec un compte humain et ressort dans les indices groupes/sudoers/connexions |
| Date de création estimée | recoupement `stat`, `chage`, logs et connexions |
| Suppression compte | `userdel -r backdoor-sys` puis `getent passwd backdoor-sys` vide |
| Permission dangereuse | `/var/www/upload` |
| Correction attendue | `chmod 750 /var/www/upload` |
| Vérification permission | `stat -c '%a %A %U:%G %n' /var/www/upload` |

## Validation 2 - Durcissement complet

### But

Appliquer le durcissement complet d'un système Linux compromis.

### Critères

Le durcissement est vérifiable par commandes :

- SSH durci ;
- `ufw` actif ;
- `fail2ban` actif ;
- services inutiles désactivés.

### Preuve de travail

Commandes à montrer :

```bash
ssh oliv@192.168.56.103
ssh root@192.168.56.103
ssh autre_compte@192.168.56.103
sudo grep -E '^(AllowUsers|PasswordAuthentication|PubkeyAuthentication|PermitEmptyPasswords)' /etc/ssh/sshd_config
sudo ufw status verbose
sudo fail2ban-client status
sudo fail2ban-client status sshd
ss -tulpn
systemctl is-enabled avahi-daemon cups rpcbind nfs-server smbd 2>/dev/null
systemctl is-active avahi-daemon cups rpcbind nfs-server smbd 2>/dev/null
```

### Explication attendue

`ssh root@[IP]` doit être refusé parce que `AllowUsers oliv` limite SSH au compte autorisé pour l'administration distante. Le mot de passe `root` n'est pas modifié.

`PasswordAuthentication yes` est conservé pendant le CTF pour ne pas casser l'accès `scp` et SSH du compte `oliv`, tant que les clés publiques ne sont pas toutes déployées. Le durcissement porte donc sur la restriction des comptes SSH, les mots de passe vides, le pare-feu et la surveillance.

`ufw status verbose` prouve que le filtrage local est actif. Les règles doivent autoriser SSH `22/tcp`, HTTP `80/tcp` et HTTPS `443/tcp`, tout en refusant les entrées non prévues.

`fail2ban-client status sshd` prouve que la jail SSH surveille les tentatives d'authentification et peut bannir les sources abusives.

Les services inutiles désactivés réduisent la surface d'attaque.

### Résultat attendu

| Point contrôlé | Résultat attendu |
| --- | --- |
| SSH `oliv` | fonctionnel |
| SSH `root` | refusé |
| SSH autre compte | refusé |
| `AllowUsers` | `oliv` |
| `PermitEmptyPasswords` | `no` |
| `ufw` | actif |
| `fail2ban` | jail `sshd` active |
| Services inutiles | stoppés ou absents |

## Validation 3 - Rapport d'incident

### But

Produire un rapport d'incident lisible et vérifiable.

### Critères

Le rapport contient :

- une timeline ;
- les causes ;
- les actions correctives avec commandes ;
- un état final vérifiable ;
- des recommandations.

### Preuve de travail

Fichiers à montrer :

```bash
ls -l /flags/rapport_Olivier.txt /flags/rapport_Olivier.md
sed -n '1,180p' /flags/rapport_Olivier.md
grep -n "DETAIL STEP BY STEP" /flags/rapport_Olivier.md
grep -n "F2 - Compte non autorise" /flags/rapport_Olivier.md
grep -n "F5 - Durcissement" /flags/rapport_Olivier.md
```

Points à lire à l'oral :

- les grandes lignes de la timeline ;
- la cause principale ;
- le vecteur d'intrusion ;
- le compte intrus ;
- la permission dangereuse ;
- les actions F1 à F7 ;
- le détail step by step des preuves F1 à F7 dans F8 ;
- les sections F2 et F5 détaillées dans le rapport final ;
- l'état final.

### Vérifications finales

```bash
getent passwd backdoor-sys || echo "Compte intrus absent"
stat -c '%a %A %U:%G %n' /var/www/upload
sudo ufw status verbose
sudo fail2ban-client status sshd
curl -I -H 'Cache-Control: no-cache' http://192.168.56.103
sudo sha256sum -c /backup/ctf-alpesnet-*.tar.gz.sha256
```

### Résultat attendu

| Rubrique du rapport | Attendu |
| --- | --- |
| Timeline | événements principaux F1 à F7 |
| Causes | service ou compte exposé, accès SSH compromis |
| Actions | chaque correction avec commande de vérification |
| État final | SSH limité à `oliv`, ufw/fail2ban actifs, HTTP 200, sauvegarde vérifiée |
| Détail step by step | F1 à F7 intégrés dans F8, avec F2 et F5 développés |
| Recommandations | mesures durables après incident |

## Script de validation orale

Je peux présenter la validation en trois temps :

1. **Investigation** : j'ai vérifié les comptes avec `awk -F: '($3==0)'`, les sudoers, les connexions, puis les permissions dangereuses avec `find`.
2. **Durcissement** : j'ai limité SSH au compte `oliv`, activé `ufw`, configuré `fail2ban` et désactivé les services inutiles.
3. **Rapport** : j'ai produit un rapport contenant timeline, causes, actions correctives avec commandes et état final vérifiable.

La validation repose sur des commandes rejouables, pas sur une simple déclaration.
