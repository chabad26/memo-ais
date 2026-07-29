# 1.6 - Manipuler un conteneur Ubuntu

## Objectif de la feuille

Cette feuille sert à manipuler un premier conteneur Ubuntu avec Docker.

L'objectif est de comprendre les gestes de base : télécharger une image, lancer un conteneur, installer un programme dedans, observer ce qui persiste, puis comparer le conteneur modifié avec l'image Ubuntu d'origine.

## Pré-requis

Avant de commencer, Docker Engine doit être installé et utilisable sans `sudo`.

Vérifiez :

```bash
docker version
docker compose version
```

Si ces commandes ne fonctionnent pas, reprenez la feuille [Installer Docker Engine](installer-docker-engine.md).

## Déroulement

### 1. Télécharger l'image Ubuntu

Téléchargez l'image officielle Ubuntu :

```bash
docker pull ubuntu
```

Vérifiez que l'image est présente localement :

```bash
docker images
```

### 2. Lancer un conteneur interactif

Vous pouvez également lancer directement l'image. Docker la téléchargera automatiquement si elle n'est pas disponible localement :

```bash
docker run -it ubuntu bash
```

Vous êtes maintenant dans un shell exécuté à l'intérieur du conteneur.

Explication rapide :

| Option | Rôle |
| --- | --- |
| `docker run` | Crée et démarre un nouveau conteneur |
| `-it` | Ouvre un terminal interactif |
| `ubuntu` | Image utilisée |
| `bash` | Commande lancée dans le conteneur |

### 3. Observer le système dans le conteneur

Vérifiez le système :

```bash
cat /etc/os-release
uname -a
```

Ces commandes permettent de vérifier que vous êtes dans un environnement Ubuntu isolé.

!!! note "À retenir"
    Un conteneur partage le noyau de la machine hôte, mais il possède son propre espace de processus, son propre système de fichiers et son propre environnement d'exécution.

### 4. Installer figlet dans le conteneur

Mettez à jour l'index des paquets :

```bash
apt update
```

Installez `figlet` :

```bash
apt install -y figlet
```

Testez le programme :

```bash
figlet "Hello Campus"
```

Cette manipulation montre qu'un conteneur peut être modifié pendant son exécution.

### 5. Quitter le conteneur

Quittez le shell du conteneur :

```bash
exit
```

Le conteneur s'arrête automatiquement, car la commande principale `bash` est terminée.

### 6. Afficher les conteneurs

Affichez tous les conteneurs :

```bash
docker ps -a
```

Identifiez votre conteneur Ubuntu et relevez :

- son identifiant ;
- son nom ;
- son image ;
- son statut ;
- la commande exécutée.

### 7. Redémarrer le conteneur

Redémarrez le conteneur :

```bash
docker start <nom-ou-id-du-conteneur>
```

Attachez-vous à son processus principal :

```bash
docker attach <nom-ou-id-du-conteneur>
```

Vous pouvez aussi ouvrir un nouveau shell dans un conteneur actif :

```bash
docker exec -it <nom-ou-id-du-conteneur> bash
```

Vérifiez que `figlet` est toujours installé :

```bash
figlet "Hello Campus"
```

Quittez à nouveau le conteneur :

```bash
exit
```

Cette vérification montre que les modifications faites dans un conteneur restent présentes tant que ce conteneur n'est pas supprimé.

### 8. Nettoyer les éléments inutilisés

Supprimez les conteneurs arrêtés, les réseaux inutilisés et les images sans référence :

```bash
docker system prune
```

Lisez attentivement la liste des éléments qui seront supprimés, puis confirmez.

Vérifiez le résultat :

```bash
docker ps -a
docker image ls
```

### 9. Relancer un nouveau conteneur depuis l'image d'origine

Lancez maintenant un nouveau conteneur depuis l'image Ubuntu d'origine :

```bash
docker run -it ubuntu bash
```

Testez :

```bash
figlet "Hello"
```

La commande ne doit plus être disponible dans ce nouveau conteneur.

Répondez aux questions suivantes :

- Pourquoi la commande n'est-elle plus disponible ?
- Où la modification précédente avait-elle été enregistrée ?
- Pourquoi l'image Ubuntu d'origine n'a-t-elle pas été modifiée ?

Quittez le conteneur :

```bash
exit
```

!!! note "À retenir"
    Installer `figlet` a modifié le système de fichiers du conteneur précédent, pas l'image Ubuntu d'origine. Un nouveau conteneur créé depuis la même image repart donc de l'état initial de cette image.

## Commandes récapitulatives

```bash
docker pull ubuntu
docker images
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
figlet "Hello Campus"
exit

docker system prune
docker ps -a
docker image ls

docker run -it ubuntu bash
figlet "Hello"
exit
```

## Preuves attendues

Conservez :

- la preuve que l'image `ubuntu` est présente ;
- le résultat de `cat /etc/os-release` dans le conteneur ;
- la liste des conteneurs avec `docker ps -a` ;
- l'identifiant, le nom, l'image, le statut et la commande du conteneur Ubuntu ;
- la preuve que `figlet` fonctionne après redémarrage du conteneur ;
- la preuve du nettoyage avec `docker system prune` ;
- la réponse aux trois questions sur la persistance des modifications.

## Résultat attendu

Vous savez lancer un conteneur Ubuntu, interagir avec son shell, installer un paquet, redémarrer le conteneur, vérifier la persistance des modifications dans ce conteneur et expliquer pourquoi l'image Ubuntu d'origine reste inchangée.

## Ressources

- [Docker command reference](https://docs.docker.com/reference/cli/docker/)
