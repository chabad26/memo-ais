# Commandes Linux

## Le terminal

Le terminal est une **console** dans laquelle on saisit des commandes.

Une commande est une suite de caractères qui permet d'exécuter une action.

Exemple :

- `rm` pour supprimer,
- `cd` pour changer de dossier,
- `ls` pour afficher le contenu d'un dossier.

## Quelques commandes de base

| Commande | Rôle |
| -------- | ---- |
| `rm` | Supprimer un fichier ou un dossier |
| `cd` | Changer de répertoire |
| `ls` | Voir les répertoires et les fichiers |
| `pwd` | Afficher le chemin du répertoire courant |
| `sudo` | Exécuter une commande avec des privilèges élevés |

!!! warning "`sudo`"
    `sudo`, c'est un peu le bouton **j'ai les pouvoirs maintenant**. Très pratique, mais à manier sans faire danser la tronçonneuse dans la salle des serveurs.

## Détails utiles

### `pwd`

Affiche le dossier dans lequel on se trouve actuellement.

Exemple :

```bash
pwd
```

### `ls`

Affiche les fichiers et dossiers présents dans le répertoire courant.

Exemple :

```bash
ls
```

### `cd`

Permet de se déplacer dans l'arborescence des dossiers.

Exemple :

```bash
cd Documents
```

### `rm`

Permet de supprimer un fichier ou un dossier.

Exemple :

```bash
rm fichier.txt
```

### `sudo`

Permet d'exécuter une commande avec les droits administrateur.

Exemple :

```bash
sudo apt update
```

## Utilisateur, sudo et root

Un utilisateur Linux peut ouvrir une session et utiliser les applications auxquelles il a accès.

Quand il a besoin de privilèges supplémentaires, il peut utiliser `sudo`.

Cela permet par exemple de :

- supprimer certains fichiers système,
- installer des logiciels,
- modifier la configuration du système.

### Root

`root` est le **super-utilisateur**.

Il possède tous les droits sur la machine.

En pratique :

- un utilisateur classique a des droits limités,
- `sudo` permet de lancer ponctuellement une commande avec plus de droits,
- `root` a tous les droits, tout le temps.

!!! danger "Root"
    Avec `root`, on peut presque tout faire. Le problème, c'est qu'on peut aussi presque tout casser.
