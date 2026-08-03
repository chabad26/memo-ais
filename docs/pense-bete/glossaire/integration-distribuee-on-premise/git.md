# Mémo Git — Documentation et scripts du projet

## Rôle de Git

Git conserve l'historique des fichiers et permet de distinguer le répertoire de travail, la zone de préparation et les commits enregistrés.

Dans ce module, le dépôt local se trouve dans :

~~~bash
cd ~/on-premise
~~~

## Cycle quotidien

~~~text
Modifier un fichier
      ↓
git status
      ↓
git diff
      ↓
git add fichier
      ↓
git diff --cached
      ↓
git commit -m "message"
      ↓
git log --oneline
~~~

## Configuration initiale

~~~bash
git --version
git config --global user.name "Prénom Nom"
git config --global user.email "prenom.nom@example.com"
git config --global --list
~~~

## Initialiser ou vérifier le dépôt

~~~bash
cd ~/on-premise
git init
git status
git branch --show-current
git rev-parse --show-toplevel
~~~

git init ne doit être exécuté qu'à la racine du projet. Vérifier le chemin avant de l'utiliser.

## Préparer un commit

~~~bash
git status
git add documentation/journal.md
git add documentation/
git add dockerfile-demo/
git add nginx-demo/
git add wordpress-compose/compose.yaml
git add wordpress-compose/.env.example
git add wordpress-compose/.gitignore
git add wordpress-compose/README.md
git diff --cached
git diff --cached --stat
git diff --cached --name-status
~~~

## Créer et lire un commit

~~~bash
git commit -m "Décrire clairement la modification"
git log --oneline --decorate --graph --all
git show --stat --oneline HEAD
git show HEAD
~~~

Exemples de messages :

- Initialiser la documentation et les scripts ;
- Documenter le déploiement WordPress ;
- Ajouter les preuves du premier commit ;
- Mettre à jour l'inventaire de l'infrastructure.

## Comparer les versions

~~~bash
git diff
git diff -- documentation/journal.md
git diff --cached
git diff HEAD~1 HEAD
git show HEAD~1:documentation/journal.md
~~~

## Corriger une préparation

Retirer un fichier de la zone de préparation sans supprimer son contenu :

~~~bash
git restore --staged documentation/journal.md
~~~

Restaurer les modifications du fichier après vérification :

~~~bash
git restore documentation/journal.md
~~~

Cette dernière commande supprime les modifications non commitées du fichier ciblé. L'utiliser uniquement après avoir vérifié le diff.

## Renommer et supprimer

~~~bash
git mv ancien-nom.md nouveau-nom.md
git rm fichier-obsolete.md
~~~

## Vérifier les secrets

Le fichier suivant doit rester local :

~~~text
wordpress-compose/.env
~~~

Commandes de contrôle :

~~~bash
git status --short
git check-ignore -v wordpress-compose/.env
git ls-files | grep -E '(^|/)\.env$' || true
~~~

Le fichier .env.example peut être partagé. Le fichier .env ne doit pas apparaître dans git ls-files.

## Livrables du module

Le dépôt doit contenir :

- documentation/architecture.md ;
- documentation/inventory.md ;
- documentation/journal.md ;
- documentation/commands.md ;
- les sources Dockerfile et index.html ;
- compose.yaml, .env.example, .gitignore et README.md ;
- au moins deux commits ;
- un historique consultable avec git log.

## Vérification finale

~~~bash
cd ~/on-premise
git status
git log --oneline --decorate --graph --all
git ls-files
git check-ignore -v wordpress-compose/.env
~~~

## Docs associées

- [Gérer la documentation avec Git](../../../integration-distribuee-on-premise/it-1/gerer-documentation-avec-git.md)
- [Journal technique du module](../../../integration-distribuee-on-premise/journal-technique.md)
