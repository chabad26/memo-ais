# Journal technique - Itération 1

## Notes techniques de l'itération

Ce journal sert à garder une trace personnelle des manipulations Docker réalisées pendant l'itération 1.

Il regroupe les commandes utilisées, les fichiers produits, les preuves obtenues et les points restant à vérifier.

## Versions installées

| Élément | Version relevée |
| --- | --- |
| Ubuntu | 24.04 |
| Docker | 29.6.2 |

Commandes de vérification :

```bash
lsb_release -a
docker --version
docker compose version
```

## Commandes utilisées

### Préparation Ubuntu

```bash
sudo apt update
sudo apt full-upgrade -y
lsb_release -a
ping -c 4 8.8.8.8
ping -c 4 ubuntu.com
sudo -v
lsblk
df -h
```

### Point de retour sur machine physique

Le formateur parle de snapshot, mais mon Ubuntu est installé sur une machine physique.

Dans ce contexte, je ne peux pas faire un snapshot d'hyperviseur comme avec une VM. Je dois donc documenter un équivalent :

- sauvegarde des fichiers importants ;
- image disque si possible avec un outil comme Clonezilla ;
- snapshot LVM ou Btrfs seulement si le partitionnement le permet ;
- relevé de l'état de référence avant modification.

Phrase de justification :

```text
Machine Ubuntu physique : pas de snapshot VM possible. Point de retour retenu : sauvegarde/image système + preuves de l'état initial.
```

### Installation Docker Engine

```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do
  sudo apt-get remove -y "$pkg"
done

sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y \
  docker-ce \
  docker-ce-cli \
  containerd.io \
  docker-buildx-plugin \
  docker-compose-plugin

sudo systemctl status docker
sudo docker --version
sudo docker compose version
sudo usermod -aG docker "$USER"
```

### Manipulation d'un conteneur Ubuntu

```bash
docker pull ubuntu
docker run -it ubuntu bash
cat /etc/os-release
uname -a
apt update
apt install -y figlet
figlet "Hello Campus"
exit
docker ps -a
docker start <nom-ou-id-du-conteneur>
docker attach <nom-ou-id-du-conteneur>
docker exec -it <nom-ou-id-du-conteneur> bash
docker system prune
docker image ls
```

### Création d'une image avec docker commit

```bash
docker run -it ubuntu bash
apt update
apt install -y figlet
figlet "Image personnalisee"
docker ps
docker commit <nom-ou-id-du-conteneur> ubuntu-figlet:1.0
docker image ls
docker run -it ubuntu-figlet:1.0 bash
figlet "Hello Campus"
```


## Productions conservées pendant l'itération

Les fichiers suivants sont les productions de travail à conserver dans l'environnement de TP. Ils peuvent être repris par une autre personne pour comprendre ou relancer les manipulations.

### 1. Image figlet-demo

Répertoire de travail : ~/dockerfile-demo/.

Fichier conservé : Dockerfile.

~~~dockerfile
FROM ubuntu:24.04

RUN apt update && \
    apt install -y figlet

CMD ["figlet","Bienvenue"]
~~~

Commandes et preuves associées :

~~~bash
cd ~/dockerfile-demo
docker build -t figlet-demo:1.0 .
docker run figlet-demo:1.0
docker history figlet-demo:1.0
docker build -t figlet-demo:2.0 .
docker image ls
docker history figlet-demo:2.0
~~~

La première version affiche Hello Campus. La seconde version affiche Bienvenue. Les captures de construction, d'exécution et d'historique sont conservées dans la fiche [Construire une image avec un Dockerfile](construire-image-dockerfile.md).

### 2. Image Nginx et page Web

Répertoire de travail : ~/nginx-demo/.

Fichier index.html :

~~~html
<!DOCTYPE html>
<html>
<head>
    <title>Campus Numérique</title>
</head>
<body>
<h1>Mon premier conteneur Web</h1>
<p>Déployé avec Docker.</p>
</body>
</html>
~~~

Fichier Dockerfile :

~~~dockerfile
FROM nginx:latest

COPY index.html /usr/share/nginx/html/index.html
~~~

Commandes et preuves associées :

~~~bash
cd ~/nginx-demo
docker build -t campus-nginx:1.0 .
docker run -d --name campus-web -p 8080:80 campus-nginx:1.0
curl http://localhost:8080
docker stop campus-web
docker start campus-web
docker logs campus-web
docker rm -f campus-web
~~~

La page est servie par Nginx depuis /usr/share/nginx/html/index.html. Les captures du build, du navigateur et des journaux sont conservées dans la fiche [Image Nginx avec page Web](construire-image-nginx-web.md).

### 3. Déploiement WordPress et MariaDB

Répertoire de travail : ~/on-premise/wordpress-compose/.

Fichiers à conserver :

| Fichier | Rôle |
| --- | --- |
| compose.yaml | Décrit les services WordPress et MariaDB, leurs variables, leur réseau et le volume db_data. |
| .env.example | Documente les variables attendues sans contenir les valeurs réelles. |
| .gitignore | Exclut .env du dépôt Git. |
| README.md | Explique le démarrage, la vérification, l'arrêt et le rôle des fichiers locaux. |

Extrait central de compose.yaml :

~~~yaml
services:
  db:
    image: mariadb:11
    restart: unless-stopped
    environment:
      MARIADB_ROOT_PASSWORD: ${MARIADB_ROOT_PASSWORD}
      MARIADB_DATABASE: ${MARIADB_DATABASE}
      MARIADB_USER: ${MARIADB_USER}
      MARIADB_PASSWORD: ${MARIADB_PASSWORD}
    volumes:
      - db_data:/var/lib/mysql

  wordpress:
    image: wordpress:latest
    restart: unless-stopped
    depends_on:
      - db
    ports:
      - "${WORDPRESS_PORT}:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: ${MARIADB_USER}
      WORDPRESS_DB_PASSWORD: ${MARIADB_PASSWORD}
      WORDPRESS_DB_NAME: ${MARIADB_DATABASE}

volumes:
  db_data:
~~~

Fichier .env.example :

~~~dotenv
MARIADB_ROOT_PASSWORD=<mot-de-passe-administrateur>
MARIADB_DATABASE=wordpress
MARIADB_USER=wordpress
MARIADB_PASSWORD=<mot-de-passe-wordpress>
WORDPRESS_PORT=8080
~~~

Fichier .gitignore :

~~~text
.env
~~~

Le fichier .env contient les valeurs propres à l'environnement de TP et ne doit pas être copié dans le dépôt. La commande docker compose config peut afficher ces valeurs : sa sortie ne doit donc pas être enregistrée ou partagée sans vérification.

Commandes et preuves associées :

~~~bash
cd ~/on-premise/wordpress-compose
docker compose config
docker compose up -d
docker compose ps
docker compose logs
docker compose exec wordpress getent hosts db
docker compose down
docker volume ls
docker compose up -d
~~~

Le déploiement est documenté dans la fiche [Déployer WordPress et MariaDB avec Docker Compose](deployer-wordpress-compose.md). Le volume db_data est conservé après docker compose down et ne doit être supprimé avec docker compose down -v qu'après validation de la persistance.

### 4. Documentation commune du module

Répertoire de travail : ~/on-premise/documentation/.

| Fichier | Contenu attendu |
| --- | --- |
| architecture.md | Présentation de l'entreprise, catégories d'utilisateurs, types de postes, schéma logique et besoins identifiés. |
| inventory.md | Inventaire des images, conteneurs, ports, données persistantes et répertoires. |
| journal.md | Difficultés rencontrées, erreurs de commande, corrections et points restant à vérifier. |
| commands.md | Commandes utiles regroupées par construction d'images, conteneurs, volumes, Compose et journaux. |

Organisation attendue :

~~~text
~/on-premise/
├── dockerfile-demo/
├── nginx-demo/
├── wordpress-compose/
└── documentation/
    ├── architecture.md
    ├── inventory.md
    ├── journal.md
    └── commands.md
~~~

Contrôle de l'organisation :

~~~bash
find ~/on-premise -maxdepth 2 -type f -o -type d
~~~

Le fichier .env reste local et le fichier .env.example peut être partagé. Les fichiers Markdown servent de documentation de reprise pour une autre personne.

## Erreurs rencontrées et résolution

| Date | Erreur ou symptôme | Cause probable | Résolution |
| --- | --- | --- | --- |
| À compléter | À compléter | À compléter | À compléter |

## Différence entre une image et un conteneur

Une **image Docker** est un modèle de départ. Elle contient un système de fichiers et des éléments nécessaires pour lancer un environnement, mais elle ne s'exécute pas toute seule.

Un **conteneur** est une instance lancée à partir d'une image. Il correspond à un environnement en cours d'utilisation, avec ses processus, son état et les modifications faites pendant son exécution.

Exemple personnel :

- `ubuntu` est l'image de départ ;
- le conteneur lancé avec `docker run -it ubuntu bash` est l'environnement dans lequel j'ai installé `figlet`.

## Ce qui est conservé ou perdu lorsqu'un conteneur est supprimé

Quand un conteneur est arrêté, ses modifications restent présentes tant que le conteneur existe encore.

Quand le conteneur est supprimé avec `docker rm` ou par un nettoyage comme `docker system prune`, les modifications faites dans ce conteneur sont perdues si elles n'ont pas été sauvegardées ailleurs.

À retenir :

- installer `figlet` dans un conteneur modifie ce conteneur ;
- relancer le même conteneur permet de retrouver `figlet` ;
- supprimer ce conteneur supprime aussi cette modification ;
- l'image `ubuntu` d'origine n'est pas modifiée.

## Comparaison entre docker commit et Dockerfile

| Méthode | Avantage | Limite |
| --- | --- | --- |
| `docker commit` | Rapide pour capturer l'état d'un conteneur modifié | Les étapes exactes de construction ne sont pas clairement documentées |
| Dockerfile | Reproductible, lisible et versionnable | Demande d'écrire les étapes de construction à l'avance |

`docker commit` permet de créer rapidement une image à partir d'un conteneur déjà modifié, par exemple `ubuntu-figlet:1.0`.

Le problème est que l'image obtenue ne raconte pas clairement comment elle a été construite. Une autre personne ne voit pas immédiatement quelles commandes ont été lancées dans le conteneur.

Un Dockerfile sera préférable parce qu'il documentera les étapes de construction sous forme de fichier texte. Il pourra être relu, corrigé, versionné et rejoué pour reconstruire la même image.

## Bilan de l'itération

- Les images `figlet-demo:1.0` et `figlet-demo:2.0` ont été construites avec un Dockerfile.
- Le conteneur Nginx a servi une page HTML personnalisée sur le port `8080`.
- WordPress et MariaDB ont été déployés ensemble avec Docker Compose.
- Le réseau Compose a permis de joindre MariaDB avec le nom DNS `db`.
- Le volume `db_data` a séparé les données MariaDB du cycle de vie des conteneurs.
- Les fichiers sensibles ont été séparés de `compose.yaml` et `.env` a été ajouté à `.gitignore`.
- Les fichiers de configuration et de documentation sont regroupés dans des répertoires identifiés.

Avant de considérer l'itération comme complètement terminée, il reste à reporter dans `documentation/journal.md` les erreurs réellement rencontrées pendant les manipulations et à conserver les captures ou sorties de commandes utiles.
