# Autonomie 3 - Déploiement Nginx sécurisé AlpesNet

## Objectif

Déployer un serveur intranet Nginx opérationnel pour AlpesNet, avec un compte système dédié, un vhost propre, des logs séparés, un pare-feu minimal, Fail2ban actif, une sauvegarde de `/var/www` et une restauration testée.

!!! warning "Règles de l'autonomie"
    Documentation officielle, man pages et notes personnelles autorisées. L'IA est limitée à la recherche documentaire : pas de génération de code ou de configuration pendant l'épreuve. Pas d'aide entre apprenants.

## Contexte

Message du DSI AlpesNet :

```text
Nous avons besoin d'un serveur intranet opérationnel d'ici cet après-midi.
Toutes les exigences de sécurité sont non-négociables.
```

## Contraintes obligatoires

| Exigence | Attendu |
| --- | --- |
| Utilisateur dédié | `www-nginx`, shell `/usr/sbin/nologin`, pas de home |
| Processus Nginx | directive `user www-nginx;` dans `nginx.conf` |
| Vhost | `/etc/nginx/sites-available/intranet` |
| Nom du site | `intranet.alpesnet.local` |
| Logs séparés | `/var/log/nginx/intranet_access.log`, `/var/log/nginx/intranet_error.log` |
| Pare-feu | port `22` restreint au sous-réseau campus, port `80/tcp` ouvert |
| Protection SSH | Fail2ban actif sur `sshd` |
| Page web | prénom, date, nom du serveur |
| Rotation logs | 7 jours, compression |
| Sauvegarde | `/var/www` vers `/backup/www` avec checksum |
| Restauration | testée depuis la sauvegarde |

## Étape 1 - Installer les paquets nécessaires

Installer Nginx et les outils de sécurité :

```bash
sudo apt update
sudo apt install -y nginx ufw fail2ban logrotate curl
```

Vérifier :

```bash
nginx -v
systemctl status nginx
```

## Étape 2 - Créer l'utilisateur système dédié

Créer le compte `www-nginx` sans shell interactif et sans home :

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin www-nginx
```

Si le compte existe déjà, vérifier simplement :

```bash
getent passwd www-nginx
```

Résultat attendu :

```text
www-nginx:x:...:/nonexistent:/usr/sbin/nologin
```

Explication : le compte sert uniquement à exécuter les workers Nginx. Il ne doit pas permettre de connexion interactive.

## Étape 3 - Configurer Nginx pour utiliser `www-nginx`

Sauvegarder la configuration :

```bash
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
```

Modifier la directive `user` :

```bash
sudo vim /etc/nginx/nginx.conf
```

Ligne attendue :

```nginx
user www-nginx;
```

Vérifier :

```bash
grep '^user ' /etc/nginx/nginx.conf
```

## Étape 4 - Créer la racine web intranet

Créer l'arborescence :

```bash
sudo mkdir -p /var/www/intranet.alpesnet.local/html
```

Créer la page `index.html` :

```bash
sudo vim /var/www/intranet.alpesnet.local/html/index.html
```

Exemple de contenu :

```html
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Intranet AlpesNet</title>
</head>
<body>
  <h1>Intranet AlpesNet</h1>
  <p>Prénom : Oliv</p>
  <p>Date : 2026-06-26</p>
  <p>Serveur : srv-oliv</p>
</body>
</html>
```

Appliquer les droits :

```bash
sudo chown -R root:www-nginx /var/www/intranet.alpesnet.local
sudo chmod -R 750 /var/www/intranet.alpesnet.local
```

## Étape 5 - Configurer le vhost `intranet`

Créer le fichier :

```bash
sudo vim /etc/nginx/sites-available/intranet
```

Configuration attendue :

```nginx
server {
    listen 80;
    server_name intranet.alpesnet.local;

    root /var/www/intranet.alpesnet.local/html;
    index index.html;

    access_log /var/log/nginx/intranet_access.log;
    error_log /var/log/nginx/intranet_error.log warn;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

Activer le site :

```bash
sudo ln -sfn /etc/nginx/sites-available/intranet /etc/nginx/sites-enabled/intranet
sudo rm -f /etc/nginx/sites-enabled/default
```

Vérifier la syntaxe :

```bash
sudo nginx -t
```

## Étape 6 - Résoudre le nom intranet pour le test

Si aucun DNS local n'existe, ajouter une résolution locale :

```bash
echo "127.0.0.1 intranet.alpesnet.local" | sudo tee -a /etc/hosts
```

Vérifier :

```bash
getent hosts intranet.alpesnet.local
```

## Étape 7 - Démarrer et tester Nginx

Démarrer et recharger Nginx :

```bash
sudo systemctl enable --now nginx
sudo systemctl reload nginx
```

Tester HTTP :

```bash
curl -s -o /tmp/intranet.html -w "%{http_code}\n" http://intranet.alpesnet.local
```

Résultat attendu :

```text
200
```

Vérifier le contenu :

```bash
cat /tmp/intranet.html
```

## Étape 8 - Vérifier que le worker tourne sous `www-nginx`

Lister les processus Nginx :

```bash
ps aux | grep nginx
```

Vérifier les workers :

```bash
ps -eo user,comm,args | grep "[n]ginx: worker"
```

Résultat attendu : les workers sont exécutés par `www-nginx`. Le processus master peut rester sous `root`, c'est normal.

## Étape 9 - Configurer UFW

Politique par défaut :

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

Autoriser SSH uniquement depuis le sous-réseau campus :

```bash
sudo ufw allow from 192.168.56.0/24 to any port 22 proto tcp
```

Autoriser HTTP :

```bash
sudo ufw allow 80/tcp
```

Activer et vérifier :

```bash
sudo ufw --force enable
sudo ufw status verbose
```

Résultat attendu : seules les règles utiles apparaissent, notamment `22/tcp` restreint et `80/tcp`.

## Étape 10 - Vérifier Fail2ban sur SSH

Créer ou vérifier une jail SSH :

```bash
sudo mkdir -p /etc/fail2ban/jail.d
sudo vim /etc/fail2ban/jail.d/alpesnet-sshd.local
```

Contenu minimal :

```ini
[sshd]
enabled = true
```

Tester et redémarrer :

```bash
sudo fail2ban-client -t
sudo systemctl enable --now fail2ban
sudo systemctl restart fail2ban
sudo fail2ban-client status sshd
```

## Étape 11 - Configurer la rotation des logs intranet

Créer le fichier logrotate :

```bash
sudo vim /etc/logrotate.d/nginx-intranet
```

Configuration :

```text
/var/log/nginx/intranet_access.log /var/log/nginx/intranet_error.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    create 0640 www-nginx adm
    sharedscripts
    postrotate
        [ -s /run/nginx.pid ] && kill -USR1 $(cat /run/nginx.pid)
    endscript
}
```

Tester en mode debug :

```bash
sudo logrotate -d /etc/logrotate.d/nginx-intranet
```

## Étape 12 - Sauvegarder `/var/www`

Créer la destination :

```bash
sudo mkdir -p /backup/www
```

Sauvegarder :

```bash
sudo rsync -avz --delete /var/www/ /backup/www/
```

Vérifier :

```bash
sudo find /backup/www -maxdepth 4 -type f -ls
```

## Étape 13 - Générer et vérifier le checksum

Créer les empreintes :

```bash
sudo find /backup/www -type f -print0 | sort -z | sudo xargs -0 sha256sum | sudo tee /backup/www-checksums.txt
```

Vérifier :

```bash
cd /
sudo sha256sum -c /backup/www-checksums.txt
```

Résultat attendu : chaque fichier affiche `OK`.

## Étape 14 - Tester la restauration de `/var/www`

Restaurer dans un dossier de test :

```bash
sudo rm -rf /tmp/restauration-www-test
sudo mkdir -p /tmp/restauration-www-test
sudo rsync -avz /backup/www/ /tmp/restauration-www-test/
```

Vérifier la page restaurée :

```bash
test -f /tmp/restauration-www-test/intranet.alpesnet.local/html/index.html
sed -n '1,20p' /tmp/restauration-www-test/intranet.alpesnet.local/html/index.html
```

!!! important "Preuve RNCP"
    La restauration testée est obligatoire. Une sauvegarde `/backup/www` non restaurée dans un répertoire de test ne suffit pas.

## Étape 15 - Vérifier les critères de réussite

HTTP 200 :

```bash
curl -s -o /tmp/intranet.html -w "%{http_code}\n" http://intranet.alpesnet.local
```

Worker Nginx :

```bash
ps aux | grep nginx
```

UFW :

```bash
sudo ufw status verbose
```

Checksums :

```bash
cd /
sudo sha256sum -c /backup/www-checksums.txt
```

## Étape 16 - Générer le rapport automatique

Le script de l'itération 5 a été adapté pour cette autonomie :

[alpesnet-it5-sauvegarde.sh](../../assets/scripts/admin-systemes-linux/it-5/alpesnet-it5-sauvegarde.sh)

Prévisualisation :

```bash
./alpesnet-it5-sauvegarde.sh --dry-run
```

Exécution :

```bash
sudo PRENOM=Oliv CAMPUS_SUBNET="192.168.56.0/24" ./alpesnet-it5-sauvegarde.sh
```

Le script affiche les étapes en direct et génère :

```text
/var/log/alpesnet-it5/rapport-it5-YYYYMMDD_HHMMSS.md
/var/log/alpesnet-it5/execution-it5-YYYYMMDD_HHMMSS.log
```

## Livrable attendu

| Élément | Preuve |
| --- | --- |
| Serveur Nginx actif | `systemctl status nginx`, `curl` HTTP 200 |
| Utilisateur dédié | `getent passwd www-nginx`, `ps aux | grep nginx` |
| Vhost intranet | `/etc/nginx/sites-available/intranet`, `nginx -t` |
| Logs séparés | présence de `intranet_access.log` et `intranet_error.log` |
| UFW | `ufw status verbose` |
| Fail2ban | `fail2ban-client status sshd` |
| Sauvegarde `/var/www` | `/backup/www` |
| Checksum | `sha256sum -c /backup/www-checksums.txt` |
| Restauration testée | `/tmp/restauration-www-test` |
| Rapport | rapport Markdown avec configurations annotées et justification sécurité |

## Ressources

- `man nginx`
- `man nginx.conf`
- `man useradd`
- `man ufw`
- `man fail2ban-client`
- `man logrotate`
- `man rsync`
- `man sha256sum`

## Synthèse à retenir

Un serveur web sécurisé se valide sur quatre axes :

1. le service répond ;
2. les processus tournent avec un compte dédié ;
3. le réseau est filtré ;
4. la configuration et les fichiers web sont sauvegardés, vérifiés et restaurables.
