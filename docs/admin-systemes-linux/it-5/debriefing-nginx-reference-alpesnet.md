# Débriefing Nginx - comparer et améliorer

## Objectif

Comparer le serveur Nginx livré pendant l'Autonomie 3 avec la configuration de référence AlpesNet, identifier les écarts, corriger ce qui doit l'être et compléter le carnet avec les preuves de conformité.

!!! note "Moment de cette feuille"
    Cette feuille se fait après l'Autonomie 3. Elle sert au débriefing, à la finalisation et à la préparation du dossier RNCP.

## Référence Debian 12

Structure attendue sur Debian 12 :

```text
/etc/nginx/nginx.conf            -> configuration principale
/etc/nginx/sites-available/      -> vhosts disponibles
/etc/nginx/sites-enabled/        -> liens symboliques actifs
```

Points de contrôle :

| Élément | Référence |
| --- | --- |
| Utilisateur Nginx | `www-nginx` |
| Configuration principale | `/etc/nginx/nginx.conf` |
| Vhost | `/etc/nginx/sites-available/intranet` |
| Vhost actif | lien symbolique dans `/etc/nginx/sites-enabled/` |
| Site par défaut | désactivé |
| Racine web de référence | `/var/www/intranet` |
| Nom HTTP | `intranet.alpesnet.local` |
| Logs | `intranet_access.log`, `intranet_error.log` |

## Étape 1 - Vérifier la directive `user`

Afficher la directive active :

```bash
grep '^user ' /etc/nginx/nginx.conf
```

Résultat attendu :

```nginx
user www-nginx;
```

Si la directive n'est pas conforme, la corriger :

```bash
sudo sed -i "s/^user .*/user www-nginx;/" /etc/nginx/nginx.conf
```

Vérifier à nouveau :

```bash
grep '^user ' /etc/nginx/nginx.conf
```

À noter dans le carnet :

```text
Directive user présente : oui/non
Valeur observée avant correction :
Valeur observée après correction :
```

## Étape 2 - Comparer le vhost avec la référence

Afficher le vhost livré :

```bash
sudo sed -n '1,120p' /etc/nginx/sites-available/intranet
```

Configuration de référence :

```nginx
# ============================================================
# Auteur : [Prénom NOM] - Date : 2026-07-01
# Service : nginx - Machine : srv-[prenom]
# Objet : Vhost intranet AlpesNet
# ============================================================
server {
    listen 80;
    server_name intranet.alpesnet.local;
    root /var/www/intranet;
    index index.html;
    access_log /var/log/nginx/intranet_access.log;
    error_log  /var/log/nginx/intranet_error.log;
    location / { try_files $uri $uri/ =404; }
}
```

Comparer les points suivants :

| Point | Question à se poser |
| --- | --- |
| En-tête | Le fichier contient-il auteur, date, service, machine et objet ? |
| `listen` | Le vhost écoute-t-il sur le port `80` ? |
| `server_name` | Le nom est-il `intranet.alpesnet.local` ? |
| `root` | La racine web est-elle cohérente avec la page réellement créée ? |
| `index` | `index.html` est-il déclaré ? |
| Logs | Les logs dédiés sont-ils configurés ? |
| `location` | `try_files $uri $uri/ =404;` est-il présent ? |

!!! info "Écart acceptable à justifier"
    Si ta solution utilise `/var/www/intranet.alpesnet.local/html` au lieu de `/var/www/intranet`, ce n'est pas forcément une erreur. C'est une convention plus proche des vhosts multi-sites. Il faut simplement vérifier que le `root` du vhost pointe bien vers le dossier qui contient `index.html`, puis justifier la différence dans le carnet.

## Étape 3 - Activer correctement le vhost

Vérifier le lien symbolique :

```bash
ls -l /etc/nginx/sites-enabled/
```

Résultat attendu :

```text
intranet -> /etc/nginx/sites-available/intranet
```

Si nécessaire, recréer le lien :

```bash
sudo ln -sfn /etc/nginx/sites-available/intranet /etc/nginx/sites-enabled/intranet
```

Désactiver le site par défaut :

```bash
sudo rm -f /etc/nginx/sites-enabled/default
```

Vérifier :

```bash
ls -l /etc/nginx/sites-enabled/
```

## Étape 4 - Vérifier la racine web et la page d'accueil

Cas référence :

```bash
sudo mkdir -p /var/www/intranet
sudo chown www-nginx:www-nginx /var/www/intranet
```

Vérifier où se trouve réellement la page :

```bash
sudo grep -n 'root ' /etc/nginx/sites-available/intranet
sudo find /var/www -maxdepth 3 -name index.html -print
```

Afficher le contenu :

```bash
sudo sed -n '1,120p' /var/www/intranet/index.html
```

Si la racine est différente, adapter le chemin à ta configuration :

```bash
sudo sed -n '1,120p' /var/www/intranet.alpesnet.local/html/index.html
```

Le contenu attendu doit permettre d'identifier :

- ton prénom ;
- la date ;
- le nom du serveur.

## Étape 5 - Tester la syntaxe puis recharger Nginx

Vérification obligatoire avant reload :

```bash
sudo nginx -t
```

Résultat attendu :

```text
syntax is ok
test is successful
```

Recharger sans couper brutalement le service :

```bash
sudo systemctl reload nginx
```

Vérifier le service :

```bash
systemctl status nginx --no-pager
```

## Étape 6 - Vérifier les processus Nginx

Afficher les processus :

```bash
ps aux | grep nginx
```

Commande plus lisible pour le carnet :

```bash
ps -eo user,pid,ppid,comm,args | grep "[n]ginx"
```

Résultat attendu :

```text
root       ... nginx: master process
www-nginx  ... nginx: worker process
```

À retenir : le master peut rester en `root`, car il ouvre le port `80`. Les workers doivent tourner sous `www-nginx`.

## Étape 7 - Contrôler UFW

Afficher les règles :

```bash
sudo ufw status verbose
```

Conformité attendue :

| Règle | Attendu |
| --- | --- |
| Politique entrante | `deny incoming` |
| Politique sortante | `allow outgoing` |
| SSH | port `22` autorisé uniquement depuis le sous-réseau campus |
| HTTP | `80/tcp` ouvert |
| Règles ouvertes inutiles | aucune |

Exemple de correction si le sous-réseau campus est `192.168.56.0/24` :

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow from 192.168.56.0/24 to any port 22
sudo ufw allow 80/tcp
sudo ufw status verbose
```

!!! warning "Attention SSH"
    Ne supprime jamais une règle SSH active sans garder une session ouverte et sans vérifier que la nouvelle règle autorise bien ton laptop.

## Étape 8 - Résoudre le nom local pour le test

Si aucun DNS local ne fournit `intranet.alpesnet.local`, ajouter une entrée locale :

```bash
echo "127.0.0.1 intranet.alpesnet.local" | sudo tee -a /etc/hosts
```

Vérifier :

```bash
getent hosts intranet.alpesnet.local
```

Depuis le client, si tu testes depuis le laptop, l'entrée doit pointer vers l'IP de la VM :

```text
192.168.56.102 intranet.alpesnet.local
```

## Étape 9 - Tester avec `curl`

Faire une requête détaillée :

```bash
curl -v http://intranet.alpesnet.local
```

Pour isoler le code HTTP :

```bash
curl -s -o /tmp/intranet.html -w "%{http_code}\n" http://intranet.alpesnet.local
```

Résultat attendu :

```text
200
```

Vérifier le contenu récupéré :

```bash
cat /tmp/intranet.html
```

Le carnet doit indiquer :

```text
Code HTTP :
Prénom visible : oui/non
Date visible : oui/non
Nom serveur visible : oui/non
```

## Étape 10 - Compléter le carnet de débriefing

Tableau conseillé :

| Contrôle | Référence | Résultat observé | Correction faite | Preuve |
| --- | --- | --- | --- | --- |
| Directive user | `user www-nginx;` |  |  | `grep '^user '` |
| Vhost | `/etc/nginx/sites-available/intranet` |  |  | `sed -n` |
| Racine web | `/var/www/intranet` ou justification |  |  | `grep root`, `find` |
| Worker | `www-nginx` |  |  | `ps aux` |
| UFW | SSH restreint + HTTP ouvert |  |  | `ufw status verbose` |
| HTTP | `200` |  |  | `curl` |
| Contenu | prénom, date, serveur |  |  | `cat /tmp/intranet.html` |

## Exercice 2 - Débriefing du projet : comparer et améliorer

L'Autonomie 3 est terminée. Tu compares ta solution avec la référence et identifies les différences.

Ce que tu dois faire :

1. Compare ton `/etc/nginx/nginx.conf` avec la référence : la directive `user www-nginx;` est-elle présente ?
2. Compare ton vhost avec la référence. Y a-t-il des différences de configuration ? Des commentaires manquants ?
3. Exécute `ps aux | grep nginx`. Le worker tourne-t-il bien sous `www-nginx` ? Sinon, identifie et corrige.
4. Exécute `sudo ufw status verbose`. Les règles sont-elles conformes au cahier des charges ?
5. Fais une requête `curl` et note le résultat dans ton carnet. La page contient-elle ton prénom, la date et le nom du serveur ?

Résultat attendu : solution conforme aux critères du cahier des charges, différences identifiées et corrigées, carnet à jour.

## Ressources

- [Documentation officielle Nginx](https://nginx.org/en/docs/)
- [Nginx Beginner's Guide](https://nginx.org/en/docs/beginners_guide.html)
- `man nginx`
- `man logrotate`
