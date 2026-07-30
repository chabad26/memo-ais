# Journal technique - Itération 1

## Notes techniques de l'itération

Ce journal sert à garder une trace personnelle des manipulations Docker réalisées pendant l'itération 1.

Il sera complété pendant la seconde journée de l'itération.

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

## Points à compléter pendant la seconde journée

- commandes Dockerfile utilisées ;
- différences observées entre `docker commit` et `docker build` ;
- erreurs rencontrées pendant la construction automatisée ;
- explication personnelle de la reproductibilité d'une image ;
- commandes de nettoyage final.
