# Commandes utiles


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/commands.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Git

~~~bash
git status
git add .
git commit -m "Message explicite"
git log --oneline --decorate --graph --all
git diff
git diff --cached
git ls-files
git check-ignore -v wordpress-compose/.env
~~~

## Images Docker

~~~bash
docker build -t figlet-demo:1.0 .
docker image ls
docker history figlet-demo:1.0
docker run figlet-demo:1.0
~~~

## Conteneurs

~~~bash
docker ps
docker ps -a
docker stop NOM
docker start NOM
docker logs NOM
docker rm -f NOM
~~~

## Volumes

~~~bash
docker volume create wordpress-db
docker volume ls
docker volume inspect wordpress-db
docker volume rm wordpress-db
~~~

## Docker Compose

~~~bash
cd ~/on-premise/wordpress-compose
docker compose config
docker compose up -d
docker compose ps
docker compose logs
docker compose exec wordpress getent hosts db
docker compose down
docker compose down -v
~~~

Attention : docker compose down -v supprime aussi les volumes associés au projet.

## Réseau

~~~bash
docker network ls
docker network inspect wordpress-compose_default
~~~

## OpenLDAP

~~~bash
cd ~/on-premise/openldap
cp .env.example .env
docker compose config
docker compose up -d
docker compose ps
docker compose logs openldap
docker compose exec openldap ldapwhoami -x -D "cn=admin,dc=embedded,dc=local" -W
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
docker compose restart openldap
~~~

Ne pas publier `.env` ni la sortie complète de `docker compose config`.

## LDAP Account Manager

~~~bash
cd ~/on-premise/ldap-account-manager
cp .env.example .env
docker network ls
docker compose config
docker compose up -d
docker compose ps
docker compose logs lam
~~~

LAM dépend du réseau externe `openldap_default`, créé par le projet OpenLDAP.
L'interface est accessible sur `http://localhost:8081`.

## Stack OpenLDAP et LAM

~~~bash
cd ~/on-premise/infrastructure-compose
cp .env.example .env
docker compose --env-file .env config
docker compose --env-file .env up -d
docker compose --env-file .env ps
docker compose --env-file .env logs
docker compose --env-file .env down
~~~

Ce Compose partage les volumes LDAP et le réseau `openldap_default` avec la
configuration de référence. Ne pas lancer en parallèle les Compose unitaires
`openldap/` et `ldap-account-manager/`.

## Vérifications du projet

~~~bash
find ~/on-premise -maxdepth 3 -type f | sort
docker compose ps
docker volume ls
git status
~~~
