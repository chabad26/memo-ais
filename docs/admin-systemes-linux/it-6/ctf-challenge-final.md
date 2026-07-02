# CTF AlpesNet - challenge final SYS-01a

## Contexte du kit

Le CTF est le challenge final du module. Tu interviens en tant qu'administrateur mandaté par AlpesNet sur une VM Linux compromise fournie par le formateur.

Ton rôle : reprendre le contrôle du serveur de production, identifier les traces de compromission, corriger les faiblesses visibles et produire un rapport d'incident exploitable. La qualité du rapport d'incident F8 compte autant que les flags récupérés : c'est le livrable RNCP principal.

!!! warning "Principe important"
    Ne fais pas seulement des commandes. Pour chaque flag, note la preuve, la commande utilisée, le résultat observé et la correction appliquée. Le rapport final se construit pendant l'enquête, pas à la fin dans la panique.

## Livrables et points

Chaque flag se dépose dans `/flags/FN.txt`. Le rapport d'incident F8 se dépose dans `/flags/rapport_[prenom].txt`. Le script génère aussi `/flags/rapport_[prenom].md` pour faciliter le rapatriement et la relecture.

| Flag | Thème | Objectif | Points | Format |
| --- | --- | --- | ---: | --- |
| F1 | Accès | Obtenir l'accès root sur la VM compromise | 20 | `/flags/F1.txt` |
| F2 | Comptes | Identifier le compte non autorisé créé par l'attaquant | 20 | `/flags/F2.txt` |
| F3 | Logs | Trouver l'IP source des tentatives d'intrusion | 20 | `/flags/F3.txt` |
| F4 | Permissions | Identifier fichier/répertoire avec permissions dangereuses | 20 | `/flags/F4.txt` |
| F5 | Durcissement | Appliquer SSH + ufw + fail2ban + services, puis démontrer en live | 30 | Démo live + traces |
| F6 | Nginx | Remettre Nginx en service, `curl` retourne 200 | 20 | `/flags/F6.txt` |
| F7 | Sauvegarde | Sauvegarde `/etc` + `/var/www` + checksum `sha256sum` | 20 | `/flags/F7.txt` |
| F8 | Rapport | Rapport d'incident complet avec timeline + causes + recommandations | 50 | `/flags/rapport_[prenom].txt` + copie `.md` |

Total : **200 points**. Seuil de validation SA-11 : **120 points**.

## Script d'aide

Le script d'aide se trouve ici :

```bash
docs/assets/scripts/admin-systemes-linux/it-6/ctf-alpesnet.sh
```

Sur la VM CTF, copie-le puis rends-le exécutable :

```bash
chmod +x ctf-alpesnet.sh
```

Mode recommandé, avec menu étape par étape :

```bash
sudo ./ctf-alpesnet.sh --menu --prenom Olivier --ip X.X.X.X
```

Mode complet :

```bash
sudo ./ctf-alpesnet.sh --all --prenom Olivier --ip X.X.X.X
```

Exécuter un flag précis :

```bash
sudo ./ctf-alpesnet.sh --task F3 --prenom Olivier --ip X.X.X.X
```

Appliquer les corrections lorsque tu es sûr de toi :

```bash
sudo ./ctf-alpesnet.sh --task F5 --apply --prenom Olivier --ip X.X.X.X
```

!!! note "Ce que fait le script"
    Le script aide à auditer, structurer les preuves, déposer les fichiers dans `/flags` et générer le rapport F8. Il ne remplace pas ton analyse : pour F1, F2, F4 et F6, il te demande de confirmer les éléments importants observés sur la VM. Pour F3, l'IP est extraite automatiquement depuis les logs SSH.

## Démarche globale

1. Connexion initiale, escalade root, preuve dans `/flags/F1.txt`.
2. Audit immédiat : `id`, UID 0, comptes interactifs, sudoers, dernières connexions.
3. Analyse des logs SSH pour identifier l'IP source.
4. Recherche des permissions dangereuses : `0777`, SUID, SGID.
5. Correction des problèmes trouvés, en documentant chaque action.
6. Durcissement SSH, ufw, fail2ban et services inutiles.
7. Remise en service Nginx jusqu'à obtenir un HTTP 200.
8. Sauvegarde de `/etc` et `/var/www`, puis vérification checksum.
9. Génération du rapport F8 et relecture avec la grille RNCP.

## F1 - Accès root

Objectif : obtenir un shell root sur la VM compromise et noter la méthode.

Commandes utiles :

```bash
id
whoami
sudo -l
sudo -n true && echo "sudo sans mot de passe"
sudo su
id
whoami
find / -perm /4000 -type f 2>/dev/null
```

Pour chercher l'indice F1, ne pas utiliser `.ctf_answer` ou `.ctf_answers` : ce sont les réponses formateur. Cherche plutôt dans les fichiers cachés des homes suspects :

```bash
sudo find /home -mindepth 1 -maxdepth 1 -type d ! -name oliv ! -name olivier -print
sudo find /home/investigateur /home/backdoor-sys -xdev -maxdepth 3 -type f -name '.*' ! -name '.ctf_answer' ! -name '.ctf_answers' -printf '%m %u:%g %p\n' 2>/dev/null
sudo grep -RInEi --exclude='.ctf_answer' --exclude='.ctf_answers' 'investigateur|backdoor-sys|Inv3st1g4t3ur!|root.{0,40}(pass|passwd|password|mdp|su|login|secret|credential|creds)|((pass|passwd|password|mdp|su|login|secret|credential|creds).{0,40}root)' /home/investigateur /home/backdoor-sys 2>/dev/null | head -80
```

Fichier attendu :

```bash
sudo mkdir -p /flags
sudo nano /flags/F1.txt
```

Contenu minimal :

```text
F1 - Accès root
Méthode utilisée : sudo su sans mot de passe
Faille observée : le compte initial possède des droits sudo sans demande de mot de passe
Preuve :
sudo -n true
sudo su
id
whoami
```

Avec le script :

```bash
sudo ./ctf-alpesnet.sh --task F1 --prenom Olivier --ip X.X.X.X
```

## F2 - Compte non autorisé

Objectif : identifier le compte créé par l'attaquant.

Commandes d'audit :

```bash
id
awk -F: '($3==0){print $1":"$3":"$6":"$7}' /etc/passwd
getent passwd
while IFS=: read -r user _ uid _ _ _ _; do
  [ "$uid" -ge 1000 ] || [ "$uid" -eq 0 ] || continue
  printf '%s: %s\n' "$user" "$(id -nG "$user" 2>/dev/null || echo groupes_inaccessibles)"
done < /etc/passwd
sudo find /etc/sudoers.d -maxdepth 1 -type f ! -name '*~' ! -name '*.*' ! -name README \
  -exec grep -Hve '^[[:space:]]*#' -e '^[[:space:]]*$' {} \;
lastlog
sudo stat /home/compte_suspect
sudo chage -l compte_suspect
sudo grep -E "useradd|adduser|new user|compte_suspect" /var/log/auth.log /var/log/syslog 2>/dev/null
lastlog -u compte_suspect
last compte_suspect
```

Points à regarder :

- utilisateur UID 0 autre que `root` ;
- compte humain avec shell interactif inattendu ;
- compte membre d'un groupe sensible (`sudo`, `admin`, `wheel`) ;
- compte ajouté dans `/etc/sudoers.d` ;
- dernière connexion suspecte.
- date de création estimée par le home, `chage`, les logs et les premières connexions.

Explication à donner :

- `awk -F: '($3==0)' /etc/passwd` lit `/etc/passwd` avec `:` comme séparateur. Le champ 3 est l'UID. Un UID `0` donne les privilèges root ; un compte UID 0 autre que `root` est donc critique.
- `getent passwd` confirme qu'un compte existe et montre son UID, son dossier personnel et son shell.
- la boucle `id -nG` affiche les groupes par utilisateur pour repérer un compte ajouté à `sudo`, `admin` ou `wheel`.
- la lecture de `/etc/sudoers.d` montre les droits sudo additionnels actifs.
- `lastlog` permet de vérifier si le compte a eu une connexion récente ou anormale.
- Linux ne stocke pas toujours une date de création fiable du compte. On l'estime avec `stat /home/compte`, `chage -l`, les logs `useradd/adduser` et les premières connexions.

Résultat à montrer :

- la sortie de `awk` permet de dire s'il existe un UID 0 autre que `root` ;
- la sortie de `getent passwd compte_suspect` prouve que le compte intrus existe ;
- la sortie des groupes et sudoers explique pourquoi le compte est suspect ;
- la sortie `stat/chage/logs/lastlog` donne une date ou une période probable de création ;
- la conclusion F2 doit nommer le compte retenu et la commande de vérification.

Le script fait cette recherche avant de te demander de confirmer le compte. Il attribue un score aux comptes suspects :

| Indice | Poids |
| --- | ---: |
| UID 0 autre que `root` | +100 |
| référence dans sudoers | +50 |
| groupe `sudo`, `admin` ou `wheel` | +40 |
| UID utilisateur humain | +15 |
| shell interactif | +10 |
| home dans `/home` | +5 |

Le compte avec le meilleur score n'est proposé automatiquement que s'il contient un indice fort, par exemple UID 0 hors `root` ou référence explicite dans sudoers. Un compte humain légitime membre de `sudo` peut apparaître dans le tableau, mais il ne doit pas être retenu sans preuve supplémentaire.

Par défaut, le script exclut `root`, `oliv`, `olivier`, l'utilisateur courant et l'utilisateur `sudo` d'origine du score. Si le formateur donne un ou plusieurs comptes légitimes, ajoute-les avec `--authorized-users` :

```bash
sudo ./ctf-alpesnet.sh --task F2 --authorized-users "root oliv olivier admin-alpesnet" --prenom Olivier --ip X.X.X.X
```

Si le compte est confirmé, correction obligatoire à la fin de F2 :

```bash
sudo userdel -r compte_suspect
getent passwd compte_suspect
```

La vérification attendue est que `getent passwd compte_suspect` ne retourne rien. En mode non interactif, `--apply` applique cette suppression à la fin de F2. En mode menu, le script demande de taper `SUPPRIMER` pour éviter une suppression accidentelle :

```bash
sudo ./ctf-alpesnet.sh --menu --apply --prenom Olivier --ip X.X.X.X
```

Fichier attendu :

```text
F2 - Compte non autorisé
Compte suspect : [nom]
Preuves : [commande + extrait]
Correction : userdel -r [nom]
Vérification : getent passwd [nom] ne retourne rien
```

Avec le script :

```bash
sudo ./ctf-alpesnet.sh --task F2 --apply --prenom Olivier --ip X.X.X.X
```

## F3 - IP source des tentatives d'intrusion

Objectif : trouver l'IP qui tente ou a tenté d'entrer sur la VM.

Commandes utiles :

```bash
sudo grep -E "Invalid user|Failed password|authentication failure" /var/log/auth.log
sudo grep -E "Invalid user|Failed password|authentication failure" /var/log/auth.log \
  | awk '{ for(i=1;i<=NF;i++) if($i ~ /^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/) print $i }' \
  | sort | uniq -c | sort -nr
journalctl -u ssh -u sshd --no-pager
```

Le script ne te demande pas de deviner l'IP. Il :

1. collecte les événements SSH suspects dans les logs disponibles ;
2. extrait les IPv4 présentes dans ces événements ;
3. compte les occurrences par IP ;
4. retient automatiquement l'IP la plus présente ;
5. ajoute dans `/flags/F3.txt` les lignes de log qui justifient ce choix.

Le résultat F3 vient du compteur et des extraits de logs : pas de saisie manuelle de l'IP.

Fichier attendu :

```text
F3 - IP source intrusion
IP retenue : [X.X.X.X]
Source : /var/log/auth.log
Preuve : [extrait de log ou compteur awk]
```

Avec le script :

```bash
sudo ./ctf-alpesnet.sh --task F3 --prenom Olivier --ip X.X.X.X
```

## F4 - Permissions dangereuses

Objectif : identifier un fichier ou répertoire dangereux, puis proposer ou appliquer la correction.

Commandes utiles :

```bash
sudo find / -xdev -perm 0777 -printf '%m %u:%g %p\n' 2>/dev/null
sudo find / -xdev -perm /4000 -printf '%m %u:%g %p\n' 2>/dev/null
sudo find / -xdev -perm /2000 -printf '%m %u:%g %p\n' 2>/dev/null
```

Le script ne te demande pas de deviner le chemin. Il :

1. recherche les permissions `0777`, SUID et SGID sur la partition racine ;
2. écarte les chemins attendus comme `/tmp` ou les SUID système classiques ;
3. score les chemins suspects, surtout dans `/home`, `/opt`, `/srv`, `/var/www`, `/usr/local` et les fichiers temporaires anormaux ;
4. retient automatiquement le meilleur candidat seulement si le score est assez fort ;
5. ajoute la preuve `stat` dans `/flags/F4.txt`.

Si seuls des SUID système classiques ressortent, le script les liste pour transparence mais ne les retient pas comme flag.

Correction type, à adapter au fichier trouvé :

```bash
sudo chmod 750 /chemin/dangereux
stat -c '%a %U:%G %n' /chemin/dangereux
```

Fichier attendu :

```text
F4 - Permissions dangereuses
Chemin : [/chemin]
Risque : [0777, SUID injustifié, SGID injustifié]
Correction : chmod [mode] [/chemin]
Vérification : stat -c '%a %U:%G %n' [/chemin]
```

Avec le script :

```bash
sudo ./ctf-alpesnet.sh --task F4 --apply --prenom Olivier --ip X.X.X.X
```

## F5 - Durcissement SSH, ufw, fail2ban et services

Objectif : sécuriser le serveur et préparer une démonstration live.

Le script génère automatiquement un rapport avant/après :

- `/flags/F5_avant.txt` : état initial SSH, ufw, fail2ban, ports et services ;
- `/flags/F5_apres.txt` : état après correction ou après audit ;
- `/flags/F5.txt` : synthèse avec liste des corrections proposées et preuves.

En mode menu, le script affiche la liste des corrections puis demande si elles doivent être appliquées. En mode non interactif, ajoute `--apply` pour appliquer directement.

```bash
sudo ./ctf-alpesnet.sh --menu --prenom Olivier --ip X.X.X.X
sudo ./ctf-alpesnet.sh --task F5 --apply --prenom Olivier --ip X.X.X.X
```

Avant de durcir SSH, envoie ta clé publique depuis ton poste local :

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub oliv@X.X.X.X
```

Si `ssh-copy-id` n'est pas disponible :

```bash
cat ~/.ssh/id_ed25519.pub | ssh oliv@X.X.X.X 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys'
```

Le script F5 vérifie aussi `authorized_keys`. Si la clé n'est pas présente, tu peux la fournir directement au script :

```bash
sudo ./ctf-alpesnet.sh --task F5 --ssh-public-key "$(cat ~/.ssh/id_ed25519.pub)" --apply --prenom Olivier --ip X.X.X.X
```

Avant modification, garde une preuve :

```bash
sudo cp -n /etc/ssh/sshd_config /etc/ssh/sshd_config.ctf-alpesnet.bak
grep -E '^(AllowUsers|PasswordAuthentication|PubkeyAuthentication|PermitEmptyPasswords)' /etc/ssh/sshd_config
ss -tulpn
```

Paramètres SSH attendus :

```text
AllowUsers oliv
PasswordAuthentication yes
PubkeyAuthentication yes
PermitEmptyPasswords no
```

!!! warning "Ne pas casser scp/SSH pendant le CTF"
    On garde `PasswordAuthentication yes` pour le compte `oliv`, sinon `scp` échoue si aucune clé publique n'est déjà installée. Le durcissement attendu ici est surtout : seul `oliv` autorisé en SSH, mots de passe vides refusés, ufw actif et fail2ban actif. On ne change pas le mot de passe `root`.

Si le SSH a été durci trop fort et que `scp` répond `Permission denied (publickey)`, réparer sur la VM via la console locale :

```bash
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config
sudo sed -i 's/^#\?KbdInteractiveAuthentication.*/KbdInteractiveAuthentication yes/' /etc/ssh/sshd_config
sudo sshd -t
sudo systemctl reload ssh || sudo systemctl reload sshd
```

Vérification SSH :

```bash
sudo sshd -t
sudo systemctl reload ssh || sudo systemctl reload sshd
ssh oliv@X.X.X.X
ssh root@X.X.X.X
ssh autre_compte@X.X.X.X
```

Le test `ssh oliv@X.X.X.X` doit fonctionner. Les tests `ssh root@X.X.X.X` et `ssh autre_compte@X.X.X.X` doivent être refusés par `AllowUsers oliv`.

Pare-feu ufw :

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow http
sudo ufw allow https
sudo ufw --force enable
sudo ufw status verbose
```

Les ports classiques autorisés sont donc SSH `22/tcp`, HTTP `80/tcp` et HTTPS `443/tcp`.

Fail2ban :

```bash
sudo mkdir -p /etc/fail2ban/jail.d
sudo nano /etc/fail2ban/jail.d/ctf-sshd.local
```

Contenu :

```ini
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
```

Activation :

```bash
sudo fail2ban-client -t
sudo systemctl enable --now fail2ban
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

Si tu obtiens l'erreur `Failed to access socket path: /var/run/fail2ban/fail2ban.sock`, le service n'a probablement pas démarré. Vérifie d'abord la cause :

```bash
sudo fail2ban-client -t
sudo systemctl status fail2ban --no-pager
sudo journalctl -u fail2ban --no-pager -n 50
```

Sur certaines VM, `/var/log/auth.log` n'existe pas. Dans ce cas, utilise le backend `systemd` dans `/etc/fail2ban/jail.d/ctf-sshd.local` :

```ini
[sshd]
enabled = true
port = ssh
filter = sshd
backend = systemd
maxretry = 3
bantime = 3600
findtime = 600
```

Puis relance :

```bash
sudo systemctl restart fail2ban
sudo fail2ban-client ping
sudo fail2ban-client status sshd
```

Services inutiles à vérifier :

```bash
systemctl list-unit-files avahi-daemon.service cups.service rpcbind.service nfs-server.service smbd.service
sudo systemctl disable --now avahi-daemon cups rpcbind nfs-server smbd
```

Avec le script :

```bash
sudo ./ctf-alpesnet.sh --task F5 --apply --prenom Olivier --ip X.X.X.X
```

Preuves attendues en démo live :

- `ssh root@X.X.X.X` refusé ;
- `sudo ufw status verbose` actif ;
- `sudo fail2ban-client status sshd` actif ;
- `ss -tulpn` cohérent avec les services réellement nécessaires.

Explication à donner :

- `ssh root@X.X.X.X` est refusé parce que `AllowUsers oliv` limite les connexions SSH au compte `oliv`. Le mot de passe `root` n'est pas modifié.
- `sudo ufw status verbose` prouve que le pare-feu local est actif et que seuls les ports classiques utiles sont autorisés : SSH `22/tcp`, HTTP `80/tcp`, HTTPS `443/tcp`.
- `sudo fail2ban-client status sshd` prouve que la jail SSH est active et surveille les tentatives d'authentification abusives.

## F6 - Nginx HTTP 200

Objectif : remettre Nginx en service.

Le script génère automatiquement un diagnostic avant/après :

- `/flags/F6_avant.txt` : `nginx -t`, état du service, logs, ports HTTP/HTTPS et test `curl` ;
- `/flags/F6_apres.txt` : même contrôle après correction ou audit ;
- `/flags/F6.txt` : erreurs détectées, corrections possibles, commandes proposées et résultat HTTP.

Le script affiche ce qui va être corrigé :

- si `nginx -t` indique `unknown directive "invalid_ctf_directive"` : il sauvegarde le fichier, commente la ligne signalée, reteste puis redémarre Nginx ;
- si `nginx -t` est invalide : il montre l'erreur et le fichier à corriger, sans modifier au hasard ;
- si `nginx -t` est OK mais le service arrêté : il propose `systemctl restart nginx` ;
- si le service tourne mais HTTP n'est pas `200` : il propose de vérifier le vhost, le site activé, le `root/index` et le pare-feu ;
- si HTTP `200` est déjà obtenu : aucune correction n'est appliquée.

Dans tous les cas, F6 affiche un bloc clair :

- erreurs détectées ;
- causes probables ;
- corrections possibles ;
- commandes à lancer ;
- preuve finale attendue avec `curl -I`.

Diagnostic :

```bash
sudo nginx -t
sudo systemctl status nginx --no-pager
journalctl -u nginx --no-pager -n 50
```

Cas CTF fréquent :

```bash
sudo cp -n /etc/nginx/nginx.conf /etc/nginx/nginx.conf.ctf-f6.bak
sudo sed -i '84s/^/# CTF F6 correction: /' /etc/nginx/nginx.conf
sudo nginx -t
sudo systemctl restart nginx
curl -I -H 'Cache-Control: no-cache' http://192.168.56.103
```

Correction puis relance :

```bash
sudo nginx -t
sudo systemctl restart nginx
curl -I -H 'Cache-Control: no-cache' http://X.X.X.X
```

Fichier attendu :

```text
F6 - Nginx
Erreur trouvée : [extrait nginx -t ou journalctl]
Correction appliquée : [fichier modifié/action]
Vérification : curl http://X.X.X.X retourne HTTP 200
```

Avec le script :

```bash
sudo ./ctf-alpesnet.sh --task F6 --apply --prenom Olivier --ip X.X.X.X
```

## F7 - Sauvegarde et checksum

Objectif : sauvegarder `/etc` et `/var/www`, puis vérifier l'intégrité.

Le script affiche la sauvegarde prévue avant de la créer :

- archive cible dans `/backup` ;
- commande `tar -C / -czf ... etc var/www` ;
- fichier checksum `.sha256` ;
- vérification `sha256sum -c`.

En mode menu, il demande confirmation avant création. En mode non interactif, utilise `--apply`.

Commandes recommandées :

```bash
sudo mkdir -p /backup
sudo tar -C / -czf /backup/ctf-alpesnet-$(date +%Y%m%d_%H%M%S).tar.gz etc var/www
sudo sha256sum /backup/ctf-alpesnet-*.tar.gz | sudo tee /backup/ctf-alpesnet.sha256
sudo sha256sum -c /backup/ctf-alpesnet.sha256
```

Fichier attendu :

```text
F7 - Sauvegarde
Archive : /backup/ctf-alpesnet-[date].tar.gz
Checksum : [sha256]
Vérification : sha256sum -c OK
```

Avec le script :

```bash
sudo ./ctf-alpesnet.sh --task F7 --apply --prenom Olivier --ip X.X.X.X
```

## F8 - Rapport d'incident final détaillé

Objectif : produire le livrable RNCP principal, avec toutes les étapes détaillées dans le même document.

Génération avec le script :

```bash
sudo ./ctf-alpesnet.sh --task F8 --prenom Olivier --ip X.X.X.X
```

Emplacement :

```bash
/flags/rapport_Olivier.txt
/flags/rapport_Olivier.md
```

Le rapport final reprend d'abord la synthèse classique, puis ajoute un détail step by step complet des flags F1 à F7. Les sections F2 et F5 reprennent les preuves détaillées déjà vues dans leurs rapports dédiés.

Format attendu :

```text
# ============================================================
# Auteur : [Prénom NOM] -- Date : 2026-07-03
# Machine : VM CTF AlpesNet -- IP : [X.X.X.X] -- Module : SYS-01a CTF
# ============================================================

1. TIMELINE DE L'INCIDENT
   [Heure estimée]  [Événement identifié]  [Source : fichier/commande]

2. ANALYSE DES CAUSES
   Cause principale    : ...
   Vecteur d'intrusion : ...

3. ACTIONS CORRECTIVES
   F1 -- Accès root       : méthode utilisée
   F2 -- Compte supprimé  : userdel [compte] + commande de vérification
   F4 -- Permissions      : chmod [X] [fichier] + vérification
   F5 -- SSH              : paramètres modifiés
   F5 -- ufw              : règles actives (ufw status verbose)
   F5 -- fail2ban         : jail active, maxretry, bantime
   F6 -- Nginx            : erreur trouvée, correction appliquée
   F7 -- Sauvegarde       : emplacement + sha256sum -c résultat

4. ÉTAT FINAL
   ssh oliv@[IP]           : autorisé
   ssh root@[IP]           : refusé
   ssh autre_compte@[IP]   : refusé
   ufw status              : [règles actives]
   fail2ban-client status  : [jail active]
   curl http://[IP]        : HTTP [code]

5. RECOMMANDATIONS
   - ...

6. DETAIL STEP BY STEP DES FLAGS
   F1 - Accès root : preuve complète
   F2 - Compte non autorisé : commandes, explications, groupes, sudoers, résultat
   F3 - IP source : logs et conclusion
   F4 - Permissions/SUID : commandes et résultat
   F5 - Durcissement : preuve ssh root refusé, ufw, fail2ban, explication des mesures, avant/après
   F6 - Nginx : erreur, correction, HTTP 200
   F7 - Sauvegarde : archive et checksum
```

## Checklist finale avant soumission

- `/flags/F1.txt` existe et explique la méthode root.
- `/flags/F2.txt` identifie le compte non autorisé et la vérification.
- `/flags/F3.txt` contient l'IP source et la preuve log.
- `/flags/F4.txt` contient le chemin dangereux et la correction.
- La démo F5 montre `ssh root@[IP]` refusé, `ufw` actif et `fail2ban` actif.
- `/flags/F6.txt` montre Nginx corrigé et HTTP 200.
- `/flags/F7.txt` contient l'archive, le checksum et `sha256sum -c`.
- `/flags/rapport_[prenom].txt` contient timeline, causes, actions, état final, recommandations et détail step by step F1 à F7.
- `/flags/rapport_[prenom].md` existe aussi pour le rapatriement/retravail en Markdown.

## Ressources

- `man ss`
- `man find`
- `man systemctl`
- `man journalctl`
- `man nginx`
- [CERT-FR - Réponse à incident Linux](https://www.cert.ssi.gouv.fr/)
- [ANSSI - Guide gestion d'une crise d'origine cyber](https://www.ssi.gouv.fr/guide/gestion-dune-crise-dorigine-cyber/)
- [SANS - Incident Response on Linux](https://www.sans.org/white-papers/incident-response-linux-systems/)
