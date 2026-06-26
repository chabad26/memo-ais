# Glossaire Systèmes Linux - Itération 5

## Sujet

Sauvegarde, restauration testée, intégrité des archives et préparation de la partie Nginx.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Sauvegarde | Copie de données ou configurations destinée à permettre une reprise après incident. |
| Restauration | Action de récupérer des données depuis une sauvegarde. |
| Restauration testée | Extraction ou remise en place contrôlée dans un dossier de test pour prouver que la sauvegarde est exploitable. |
| `rsync` | Outil de synchronisation efficace, souvent utilisé pour les sauvegardes incrémentales. |
| Incrémental | Ne recopie que ce qui a changé depuis la dernière synchronisation. |
| `--delete` | Option `rsync` qui supprime côté destination ce qui n'existe plus côté source. |
| `--dry-run` | Simulation sans modification réelle. |
| `--checksum` | Compare le contenu des fichiers plutôt que seulement leur date ou taille. |
| `tar` | Outil d'archivage permettant de regrouper plusieurs fichiers dans une archive. |
| `tar.gz` | Archive `tar` compressée avec gzip. |
| Checksum | Empreinte calculée à partir d'un fichier pour vérifier son intégrité. |
| `sha256sum` | Commande qui calcule ou vérifie une empreinte SHA-256. |
| `/backup` | Dossier local utilisé pour stocker les sauvegardes du TP. |
| `/tmp/restauration-test` | Dossier temporaire utilisé pour tester la restauration sans toucher aux fichiers de production. |
| Procédure de restauration | Suite d'étapes écrites permettant de restaurer proprement après incident. |
| Nginx | Serveur web léger, prévu dans la suite de l'itération 5. |
| Vhost | Virtual host, configuration Nginx permettant d'héberger un site ou service précis. |
| `server_name` | Nom DNS ou local auquel le vhost Nginx répond. |
| Worker Nginx | Processus qui traite les requêtes HTTP. Il doit tourner sous un utilisateur non privilégié. |
| `www-nginx` | Utilisateur système dédié au service Nginx dans l'autonomie. |
| `/usr/sbin/nologin` | Shell empêchant une connexion interactive pour un compte de service. |
| Logs séparés | Fichiers de logs dédiés à un vhost, utiles pour l'audit et le dépannage. |
| `access_log` | Directive Nginx qui définit le fichier des accès HTTP. |
| `error_log` | Directive Nginx qui définit le fichier des erreurs du vhost. |
| Logrotate | Outil qui archive, compresse et supprime les anciens logs selon une politique définie. |
| HTTP 200 | Code de réponse indiquant que la page est servie correctement. |

## Manipulations faites

| Manipulation | Commandes ou actions |
| --- | --- |
| Créer le dossier de sauvegarde | `sudo mkdir -p /backup`, `sudo chmod 750 /backup`. |
| Sauvegarder avec rsync | `sudo rsync -avz --delete /srv/alpesnet/ /backup/alpesnet-$DATE/`. |
| Vérifier rsync | `sudo rsync -avz --dry-run --checksum source/ destination/`. |
| Créer une archive configs | `sudo tar -czf /backup/configs-$DATE.tar.gz /etc/ssh /etc/rsyslog.d`. |
| Lister une archive | `sudo tar -tzf /backup/configs-$DATE.tar.gz`. |
| Tester la restauration | `sudo tar -xzf archive.tar.gz -C /tmp/restauration-test/`. |
| Vérifier les fichiers restaurés | `ls`, `sed`, comparaison avec les fichiers attendus. |
| Générer un checksum | `sha256sum archive.tar.gz > /backup/checksums.txt`. |
| Vérifier un checksum | `sha256sum -c /backup/checksums.txt`. |
| Automatiser l'itération | Lancer `alpesnet-it5-sauvegarde.sh` pour produire rapport et log. |
| Créer un utilisateur Nginx | `useradd --system --no-create-home --shell /usr/sbin/nologin www-nginx`. |
| Configurer le worker Nginx | directive `user www-nginx;` dans `/etc/nginx/nginx.conf`. |
| Créer le vhost intranet | `/etc/nginx/sites-available/intranet`, lien dans `sites-enabled`. |
| Tester Nginx | `nginx -t`, `systemctl reload nginx`, `curl`. |
| Vérifier le worker | `ps aux | grep nginx`. |
| Filtrer avec UFW | SSH restreint au campus, `80/tcp` ouvert. |
| Sauvegarder le web | `rsync -avz --delete /var/www/ /backup/www/`. |

## Point clé : une sauvegarde doit être restaurée

Une sauvegarde n'est pas seulement un fichier présent dans `/backup`. Elle doit être testée.

Méthode minimale :

```bash
mkdir -p /tmp/restauration-test
sudo tar -xzf /backup/configs-$DATE.tar.gz -C /tmp/restauration-test/
ls /tmp/restauration-test/etc/ssh/
```

À retenir :

- ne jamais restaurer directement dans `/etc` sans test ;
- vérifier que les fichiers sont lisibles ;
- conserver une trace de la restauration ;
- documenter la procédure de retour arrière.

## Point clé : checksum

Le checksum sert à vérifier qu'une archive n'a pas changé depuis sa création.

Exemple :

```bash
sha256sum /backup/configs-$DATE.tar.gz | sudo tee /backup/checksums.txt
cd / && sudo sha256sum -c /backup/checksums.txt
```

Résultat attendu :

```text
/backup/configs-YYYYMMDD.tar.gz: OK
```

## Point clé : script évolutif

Le script `alpesnet-it5-sauvegarde.sh` sert de base pour l'itération 5.

Aujourd'hui, il automatise :

- préparation de `/backup` ;
- sauvegarde `rsync` ;
- vérification `rsync --dry-run --checksum` ;
- archive `tar` ;
- restauration testée ;
- checksum ;
- rapport Markdown final.

Il intègre aussi l'autonomie Nginx :

- installation ;
- vhost ;
- utilisateur dédié ;
- logs séparés ;
- durcissement ;
- rapport de déploiement.

## Point clé : worker Nginx non privilégié

Le master Nginx peut rester lancé par `root`, car il ouvre le port 80. Les workers, eux, doivent tourner sous un compte dédié.

Vérification :

```bash
ps -eo user,comm,args | grep "[n]ginx: worker"
```

Résultat attendu : `www-nginx` apparaît comme utilisateur des workers.

## Point clé : logs séparés et rotation

Chaque vhost important doit avoir ses propres logs :

```nginx
access_log /var/log/nginx/intranet_access.log;
error_log /var/log/nginx/intranet_error.log warn;
```

La rotation limite la taille et la durée de conservation :

```text
daily
rotate 7
compress
```

## Docs associées

- [Vue d'ensemble itération 5](../../../admin-systemes-linux/it-5/index.md)
- [Sauvegarde et restauration AlpesNet](../../../admin-systemes-linux/it-5/sauvegarde-restauration-alpesnet.md)
- [Autonomie 3 - Déploiement Nginx sécurisé AlpesNet](../../../admin-systemes-linux/it-5/autonomie-3-nginx-securise-alpesnet.md)
- [Script Itération 5](../../../assets/scripts/admin-systemes-linux/it-5/alpesnet-it5-sauvegarde.sh)
