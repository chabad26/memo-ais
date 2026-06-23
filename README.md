# Mémo AIS

Ce dépôt contient un petit site de documentation pour centraliser des notes de formation **AIS**.

Il sert à garder au propre des rappels sur :

- le matériel informatique,
- Linux et le terminal,
- les commandes utiles,
- le réseau,
- la cybersécurité,
- l'administration des systèmes Linux,
- les réflexes de dépannage.

Le site est construit avec **MkDocs** et le thème **Material for MkDocs**.

## Prérequis

Avant de commencer, il faut avoir :

- Python 3 installé,
- Git installé,
- un terminal.

Pour vérifier :

```bash
python3 --version
git --version
```

## Récupérer le projet

Si vous avez forké le dépôt sur GitHub, clonez votre fork :

```bash
git clone https://github.com/VOTRE-UTILISATEUR/memo-ais.git
cd memo-ais
```

Sinon, clonez directement le dépôt d'origine :

```bash
git clone https://github.com/UTILISATEUR-ORIGINAL/memo-ais.git
cd memo-ais
```

## Installation

Créer un environnement virtuel Python :

```bash
python3 -m venv .venv
```

Activer l'environnement virtuel :

```bash
source .venv/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Lancer le site en local

Démarrer le serveur MkDocs :

```bash
mkdocs serve
```

Puis ouvrir l'adresse affichée dans le terminal.

En général :

```text
http://127.0.0.1:8000
```

Pour arrêter le serveur, utiliser `Ctrl + C` dans le terminal.

## Modifier le contenu

Les pages du site sont dans le dossier `docs/`.

Exemples :

```text
docs/index.md
docs/pense-bete.md
docs/intro-ais/reseau.md
docs/intro-ais/commandes-linux.md
docs/admin-systemes-linux/index.md
```

Après modification d'un fichier, MkDocs recharge souvent la page automatiquement.

## Générer le site

Pour générer la version HTML du site :

```bash
mkdocs build
```

Le site généré se trouve dans le dossier `site/`.

Ce dossier peut être supprimé puis recréé avec `mkdocs build`.

## Mettre à jour son fork

Après avoir modifié des fichiers :

```bash
git status
git add .
git commit -m "Mise à jour du mémo"
git push
```

## Problèmes fréquents

Si la commande `mkdocs` n'est pas trouvée, vérifiez que l'environnement virtuel est activé :

```bash
source .venv/bin/activate
```

Si les dépendances ne sont pas installées :

```bash
pip install -r requirements.txt
```
