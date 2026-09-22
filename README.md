# Mémo AIS

Ce dépôt contient un petit site de documentation pour centraliser des notes de formation **AIS**.

Le site est construit avec **MkDocs** et le thème **Material for MkDocs**.

## Module Sécurité des données

Ce module présente les mécanismes cryptographiques qui protègent les données
d'une infrastructure, qu'elles circulent sur le réseau, soient stockées sur les
machines ou conservées dans des sauvegardes. La progression va des notions de
base (confidentialité, intégrité, authenticité, clés et certificats) à la
vérification de TLS, puis à la mise en œuvre de volumes chiffrés avec LUKS.

Les activités abordent également l'aléa cryptographique, la sauvegarde du
header LUKS et la restauration après perte contrôlée des informations de
récupération. La dernière étape élargit la réflexion à la gestion du cycle de
vie des clés dans un parc : stockage, sauvegarde, récupération, rotation,
révocation et destruction, avec une comparaison de systemd-cryptenroll/TPM2,
Clevis/Tang et des services de gestion de clés cloud.

En fin de module, l'apprenant sait choisir un mécanisme adapté à un besoin,
analyser une configuration au regard de recommandations de sécurité, vérifier
une connexion TLS, récupérer un stockage LUKS et documenter une architecture de
gestion des clés. Les livrables sont une analyse de configuration, un stockage
LUKS opérationnel, une procédure de récupération et une architecture de gestion
des clés pour un parc.

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
