# Itération 1 - Docker

## Objectif de l'itération

Cette première itération sert à préparer la machine qui sera utilisée pendant tout le module **Intégration distribuée on-premise**.

Avant de déployer Docker et les futurs services conteneurisés, il faut disposer d'un système Ubuntu Server propre, connecté au réseau, à jour et administrable avec les droits nécessaires.

## Spécifications

| Élément | Attendu |
| --- | --- |
| Mode de travail | Travail individuel |
| Machine utilisée | Machine polyvalente |
| Durée de conservation | La machine est conservée pendant les dix jours du module |
| Système à installer | Ubuntu 24.04 LTS |

!!! note "Point important"
    Cette machine devient la base de travail du module. Il faut donc éviter les installations temporaires ou les configurations non documentées.

## Déroulement

### Feuilles de l'itération

- [Découverte de l'entreprise fictive](decouverte-entreprise-fictive.md)
- [Installer Docker Engine](installer-docker-engine.md)
- [1.6 - Manipuler un conteneur Ubuntu](manipuler-conteneur-ubuntu.md)
- [Créer une image à partir d'un conteneur](creer-image-depuis-conteneur.md)
- [Construire une image avec un Dockerfile](construire-image-dockerfile.md)
- [Construire une image contenant une application Web simple](construire-image-nginx-web.md)
- [Persistance des données avec un volume Docker](persistance-volume-mariadb.md)
- [Déployer WordPress et MariaDB avec Docker Compose](deployer-wordpress-compose.md)
- [Gérer la documentation avec Git](gerer-documentation-avec-git.md)
- [Journal technique du module](../journal-technique.md)

### 1. Installer Ubuntu Server 24.04 LTS

Installez **Ubuntu 24.04 LTS** sur la machine polyvalente.

Pendant l'installation, préparez une configuration simple et exploitable :

- un nom de machine clair ;
- un compte utilisateur personnel ;
- un mot de passe robuste ;
- une configuration réseau fonctionnelle ;
- OpenSSH si l'administration distante est nécessaire.

### 2. Connecter la machine au réseau

Une fois l'installation terminée, vérifiez que la machine est bien raccordée au réseau.

Contrôles à réaliser :

- câble réseau ou interface active ;
- adresse IP attribuée ;
- passerelle configurée ;
- DNS fonctionnel.

### 3. Créer et vérifier le compte utilisateur

Le compte utilisateur créé pendant l'installation doit permettre d'administrer la machine.

Vérifiez que le compte dispose des droits `sudo` :

```bash
sudo -v
```

Si la commande demande le mot de passe puis revient sans erreur, les droits d'administration sont disponibles.

### 4. Mettre à jour le système

Exécutez les mises à jour disponibles :

```bash
sudo apt update
sudo apt full-upgrade -y
```

Ces commandes permettent de récupérer la liste des paquets disponibles puis d'appliquer les mises à jour système.

### 4 bis. Prévoir un point de retour adapté au support

Si la machine Ubuntu est une **machine virtuelle**, le point de retour attendu peut être un snapshot de l'hyperviseur.

Si la machine Ubuntu est une **machine physique**, il n'y a pas de snapshot d'hyperviseur possible. Il faut produire une preuve équivalente :

- sauvegarde des fichiers importants sur un support externe ou réseau ;
- image disque avec un outil comme Clonezilla si le temps et le matériel le permettent ;
- snapshot LVM ou Btrfs uniquement si le système a été installé avec ce type de volume ;
- journal des commandes et état de référence avant modification importante.

!!! note "Formulation à retenir"
    Sur une machine physique, je ne peux pas faire un snapshot de VM. Je documente donc un point de retour équivalent : sauvegarde ou image système, preuve de l'état initial, puis procédure de restauration si nécessaire.

### 5. Vérifier la version installée

Contrôlez que la machine utilise bien Ubuntu 24.04 LTS :

```bash
lsb_release -a
```

Le résultat doit indiquer une version Ubuntu 24.04 LTS.

### 6. Vérifier la connectivité Internet

Vérifiez d'abord la connectivité IP directe :

```bash
ping -c 4 8.8.8.8
```

Puis vérifiez la résolution DNS :

```bash
ping -c 4 ubuntu.com
```

Si le ping vers `8.8.8.8` fonctionne mais pas celui vers `ubuntu.com`, le réseau est probablement actif mais la résolution DNS doit être corrigée.

## Commandes récapitulatives

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

## Preuves attendues

À la fin de l'itération, conservez les éléments suivants :

- version Ubuntu affichée par `lsb_release -a` ;
- preuve des mises à jour appliquées ;
- résultat du ping vers `8.8.8.8` ;
- résultat du ping vers `ubuntu.com` ;
- preuve que le compte utilisateur peut utiliser `sudo` ;
- preuve du point de retour choisi : snapshot si VM, ou sauvegarde/image système si machine physique.

## Résultat attendu

La machine est prête pour la suite du module :

- Ubuntu 24.04 LTS est installé ;
- le réseau fonctionne ;
- Internet est accessible ;
- la résolution DNS fonctionne ;
- le compte utilisateur est opérationnel ;
- les droits d'administration sont disponibles ;
- le système est à jour ;
- un point de retour est documenté avant les changements importants.

## Ressources

- [Ubuntu Server](https://ubuntu.com/download/server)
