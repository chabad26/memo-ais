# Créer une image à partir d'un conteneur

**Durée estimée : 45 min**

## Objectif

Créer une image personnalisée à partir de l'état d'un conteneur et identifier les limites de cette méthode.

L'activité permet de comprendre qu'un conteneur peut servir de base à une nouvelle image avec `docker commit`, mais aussi que cette méthode documente mal les étapes de construction.

## Pré-requis

Avant de commencer, vous devez savoir :

- lancer un conteneur Ubuntu interactif ;
- installer un paquet dans un conteneur ;
- identifier un conteneur avec `docker ps` ;
- distinguer une image d'un conteneur.

## Déroulement

### 1. Relancer un conteneur Ubuntu

Lancez un conteneur Ubuntu interactif :

```bash
docker run -it ubuntu bash
```

### 2. Installer figlet dans le conteneur

Dans le conteneur, mettez à jour l'index des paquets puis installez `figlet` :

```bash
apt update
apt install -y figlet
figlet "Image personnalisee"
```

Laissez ce conteneur ouvert.

### 3. Identifier le conteneur depuis un second terminal

Dans un second terminal, identifiez le conteneur en cours d'exécution :

```bash
docker ps
```

Relevez son nom ou son identifiant.

### 4. Créer une image à partir du conteneur

Créez une nouvelle image à partir de l'état actuel du conteneur :

```bash
docker commit <nom-ou-id-du-conteneur> ubuntu-figlet:1.0
```

Cette commande capture l'état du système de fichiers du conteneur et crée une nouvelle image nommée `ubuntu-figlet` avec le tag `1.0`.

### 5. Vérifier que l'image existe

Affichez les images locales :

```bash
docker image ls
```

L'image `ubuntu-figlet:1.0` doit apparaître dans la liste.

### 6. Lancer un conteneur depuis l'image personnalisée

Lancez un nouveau conteneur à partir de l'image créée :

```bash
docker run -it ubuntu-figlet:1.0 bash
```

Testez immédiatement :

```bash
figlet "Hello Campus"
```

Si `figlet` fonctionne, la modification a bien été conservée dans l'image personnalisée.

## Questions

Répondez aux questions suivantes :

- Quelle est la différence entre l'image `ubuntu` et l'image `ubuntu-figlet:1.0` ?
- Quelle modification a été conservée ?
- Quelle information sur la construction de l'image n'est pas documentée par cette méthode ?
- Pourquoi une construction automatisée avec un Dockerfile sera-t-elle préférable ?

## Nettoyage

Nettoyez uniquement les conteneurs créés pendant l'exercice.

Affichez tous les conteneurs :

```bash
docker ps -a
```

Supprimez les conteneurs concernés :

```bash
docker rm <nom-ou-id-du-conteneur>
```

!!! warning "À conserver"
    Ne supprimez pas encore l'image `ubuntu-figlet:1.0`. Elle pourra servir de comparaison lors de l'activité sur les Dockerfile.

## Commandes récapitulatives

Terminal 1 :

```bash
docker run -it ubuntu bash
apt update
apt install -y figlet
figlet "Image personnalisee"
```

Terminal 2 :

```bash
docker ps
docker commit <nom-ou-id-du-conteneur> ubuntu-figlet:1.0
docker image ls
docker run -it ubuntu-figlet:1.0 bash
figlet "Hello Campus"
exit
docker ps -a
docker rm <nom-ou-id-du-conteneur>
```

## Preuves attendues

Conservez :

- l'identifiant ou le nom du conteneur Ubuntu modifié ;
- la preuve que `figlet` fonctionne dans le conteneur initial ;
- la preuve que l'image `ubuntu-figlet:1.0` existe ;
- la preuve que `figlet` fonctionne dans un nouveau conteneur lancé depuis `ubuntu-figlet:1.0` ;
- les réponses aux questions sur les limites de `docker commit`.

## Résultat attendu

Vous savez créer une image avec `docker commit`, vérifier qu'elle existe, l'utiliser pour lancer un nouveau conteneur et expliquer pourquoi cette méthode reste moins propre et moins reproductible qu'un Dockerfile.
