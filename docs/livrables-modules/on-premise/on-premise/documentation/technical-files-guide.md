# Guide des fichiers Docker Compose et des scripts


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/technical-files-guide.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Principe général

Les fichiers du module ont des responsabilités différentes :

| Type | Responsabilité |
|---|---|
| `Dockerfile` | construire une image personnalisée |
| Compose | déclarer les services, réseaux, ports, volumes et dépendances |
| VALEUR RETIRÉE | VALEUR RETIRÉE |
| VALEUR RETIRÉE | VALEUR RETIRÉE |
| configuration externe | décrire le comportement de Samba, Postfix ou Dovecot |
| script | effectuer des actions ordonnées impossibles à exprimer seulement en YAML |
| volume | conserver l'état et les données après recréation d'un conteneur |

Compose est déclaratif : il décrit l'état souhaité. Les scripts sont
impératifs : ils contrôlent et exécutent des opérations dans un ordre précis.

## Cycle d'un `docker compose up -d`

1. Compose lit `.env` et remplace les expressions `${VARIABLE}`.
2. Il télécharge `image:` ou construit `build:` avec le `Dockerfile`.
3. Il crée les réseaux et volumes absents.
4. Il crée les conteneurs avec leurs variables, ports et montages.
5. L'entrypoint de chaque image prépare puis lance l'application.
6. Le `healthcheck`, lorsqu'il existe, confirme que le service répond.

Le nom d'un service devient un nom DNS sur son réseau Docker. Une application
peut donc joindre `db`, `openldap`, `postfix` ou `dovecot` sans adresse IP fixe.

## Volumes et fichiers montés

```yaml
volumes:
  - db_data:/var/lib/mysql
  - ./dovecot:/etc/dovecot:ro
```

- `db_data` est un volume Docker persistant ;
- `./dovecot` est un dossier du dépôt rendu visible dans le conteneur ;
- `:ro` interdit au conteneur de modifier le fichier source.

Un volume contient l'état vivant. Un fichier du dépôt permet de reconstruire
la configuration. Il faut sauvegarder les deux.

## Projets du module

### WordPress

`wordpress-compose/compose.yaml` crée MariaDB (`db`) et WordPress
(`wordpress`). WordPress utilise `db` comme nom DNS. `db_data` conserve la base
et donc l'installation WordPress. `${WORDPRESS_PORT}:80` change le port de
l'hôte sans modifier le port interne d'Apache.

`depends_on` impose un ordre de création, mais ne vérifie pas à lui seul que
MariaDB accepte déjà les connexions.

### OpenLDAP et LAM

[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
schémas dans trois volumes : données, configuration et sauvegardes. Les
variables `OPENLDAP_BOOTSTRAP_*` agissent principalement sur un volume vide ;
les modifier ne réécrit pas un annuaire déjà initialisé.

Le schéma Samba est fourni par un bind mount en lecture seule depuis
`samba-ldap/schema/`.

`ldap-account-manager/compose.yaml` ne contient pas les utilisateurs. LAM
joint OpenLDAP sur le réseau externe `openldap_default` et affiche ou modifie
les objets de l'annuaire.

`infrastructure-compose/compose.yaml` réunit les deux services et réutilise les
volumes historiques avec `external: true`. Ces volumes doivent donc déjà
exister et ne sont pas créés silencieusement par ce projet.

### Samba

| Fichier | Fonction |
|---|---|
| `samba-ad/Dockerfile` | installe Samba, LDAP, NSS et NSLCD dans une image Debian |
| `samba-ad/compose.yaml` | construit l'image, publie SMB et monte les trois volumes |
| `config/smb.conf` | définit le backend LDAP, les partages et les groupes autorisés |
| `config/nsswitch.conf` | ajoute LDAP aux sources d'utilisateurs et de groupes Linux |
| VALEUR RETIRÉE | VALEUR RETIRÉE |
| `entrypoint.sh` | initialise les fichiers, vérifie LDAP et lance `smbd` |

Les modèles sont copiés dans l'image puis, au premier démarrage, dans le volume
`samba_config`. Le script n'écrase pas ce volume à chaque démarrage afin de ne
pas détruire une adaptation persistante.

`entrypoint.sh` exécute `testparm`, génère temporairement `nslcd.conf` avec
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
termine par `exec smbd`. Grâce à `exec`, Samba devient le processus principal
et reçoit les signaux d'arrêt Docker.

Les volumes séparent la configuration (`samba_config`), l'état Samba
(`samba_state`) et les documents (`samba_share`). `compose.ad.yaml` est une
ancienne tentative conservée comme historique et ne doit pas être démarrée en
parallèle.

### Messagerie

`messaging-compose/docker-compose.yml` assemble :

- MariaDB pour les préférences Roundcube ;
- Postfix pour SMTP et la distribution ;
- Dovecot pour IMAP, LMTP et l'authentification LDAP ;
- Roundcube pour le webmail.

Le réseau `mail` relie la messagerie. Postfix et Dovecot rejoignent également
`openldap_default`. Le volume `postfix_spool` est partagé entre eux afin
d'exposer les sockets Unix d'authentification et de livraison LMTP sans port
réseau supplémentaire.

`postfix-init.sh` génère `ldap-users.cf` depuis les variables locales, active la
recherche LDAP des destinataires et limite le port `587` aux comptes
authentifiés.

`dovecot/dovecot.conf` configure IMAP, LMTP, les boîtes Maildir et les sockets.
`dovecot-ldap.conf.ext` décrit la recherche de l'utilisateur et le bind LDAP.
Roundcube ne joint pas LDAP directement : il teste les identifiants auprès de
Dovecot en IMAP.

### PKI et certificats internes

`pki/certs/Campus-CA-root.crt` est le certificat racine public de Campus CA.
Il peut être distribué aux hôtes, navigateurs et applications qui doivent faire
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
du service Step CA.

TLS est activé dans le laboratoire pour OpenLDAP, Postfix, Dovecot et
Roundcube. Les certificats et clés de service sont générés dans
`pki/issued/<service>/`, répertoire ignoré par Git, puis copiés dans des
volumes Docker dédiés par les scripts de préparation. Les fichiers Compose ne
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]

`infrastructure-compose/configure-openldap-tls.sh` applique les attributs TLS
OpenLDAP sur des volumes déjà initialisés. `prepare-openldap-tls.sh` et
`messaging-compose/prepare-tls-volumes.sh` distribuent les certificats dans les
volumes avec les permissions attendues. Après renouvellement, relancer ces
scripts puis recréer les services concernés.

### BorgBackup

```text
cron
  -> run-backup-cron.sh
       -> backup.sh
       -> last-run.status
  -> check-backup.sh
```

`backup.sh` exporte LDAP avec `slapcat`, MariaDB avec `mariadb-dump`, puis copie
les volumes en lecture seule dans des archives temporaires. Certains
conteneurs sont brièvement mis en pause pour éviter une copie incohérente. Le
script crée ensuite l'archive Borg, applique la rétention et contrôle le dépôt.

`set -Eeuo pipefail` évite de continuer après une erreur. `trap cleanup` réactive
les conteneurs et efface le dossier temporaire même si une commande échoue.

`run-backup-cron.sh` ajoute un verrou `flock` pour empêcher deux sauvegardes en
même temps et écrit un état atomique. `check-backup.sh` vérifie le statut, le
code retour, l'âge inférieur à 36 heures, l'archive et le marqueur de fin du
journal. `crontab.example` programme la sauvegarde à 02 h 00 et le contrôle à
08 h 15.

### Elasticsearch, Kibana et Filebeat

`monitoring-compose/compose.yaml` démarre un Elasticsearch mono-nœud, Kibana et
Filebeat sur le réseau `monitoring`. Le volume
`monitoring_elasticsearch_data` conserve les index. Le tas Java est limité à
1 Gio.

Le `healthcheck` interroge `_cluster/health`. Kibana utilise
`condition: service_healthy`, donc il attend une réponse réelle
d'Elasticsearch. Les ports sont liés à `127.0.0.1` et ne sont pas accessibles
depuis une autre machine. La désactivation temporaire de la sécurité Elastic
est réservée au TP local.

`filebeat.yml` contient deux inputs `filestream` :

- `docker-containers` lit les fichiers JSON de tous les conteneurs, les passe
  dans le parseur Docker et ajoute le nom de l'image et du conteneur ;
- `borgbackup-files` lit les journaux et le statut de la sauvegarde Borg.

Le volume `monitoring_filebeat_data` conserve le registre des fichiers et des
positions déjà lues. Sans ce volume, une recréation de Filebeat pourrait
réindexer d'anciennes lignes.

Le montage du socket Docker permet au processeur `add_docker_metadata`
d'identifier Postfix, Dovecot, OpenLDAP et Samba. Ce socket est très privilégié
même avec un montage `:ro` et doit rester limité à un agent de confiance. Le
processeur `drop_event` exclut les propres journaux de Filebeat pour éviter une
boucle de collecte.

## Après une modification

| Fichier modifié | Action |
|---|---|
| `.env` | `docker compose up -d` pour recréer le conteneur |
| Compose | `docker compose up -d` |
| `Dockerfile` ou fichier copié | `docker compose up -d --build` |
| fichier monté | redémarrer le service pour qu'il relise sa configuration |
| données d'un volume | utiliser l'outil de l'application, pas éditer le volume à la main |

Un `docker compose restart` ne recrée pas le conteneur et ne recharge donc pas
les nouvelles variables de `.env`.

## Commandes d'explication et de diagnostic

```bash
docker compose config
docker compose ps
docker compose logs --tail=100 <service>
docker compose exec <service> <commande>
docker inspect <conteneur>
docker volume inspect <volume>
docker network inspect <reseau>
git check-ignore -v .env
```

`docker compose down` conserve les volumes nommés. L'option `-v` les supprime
et peut donc effacer les données persistantes.
