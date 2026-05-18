# Hygiène numérique

L'hygiène numérique regroupe les bons réflexes de base pour limiter les risques au quotidien.

## Mots de passe et MFA/2FA

Un bon mot de passe doit être **unique**, **long** et **difficile à deviner**.

L'authentification multifacteur ajoute une couche de protection au processus de connexion. Pour accéder à un compte, l'utilisateur doit confirmer son identité avec un second facteur, par exemple un code reçu sur téléphone ou une application d'authentification.

Règles importantes :

- utiliser un mot de passe différent pour chaque compte,
- choisir au moins `12` caractères quand c'est possible,
- mélanger majuscules, minuscules, chiffres et caractères spéciaux,
- éviter les informations personnelles comme une date de naissance ou un prénom,
- activer la double authentification quand elle est disponible,
- changer le mot de passe en cas de doute ou pour les comptes sensibles.

## Gestionnaire de mots de passe

Un gestionnaire de mots de passe permet de centraliser ses identifiants dans une base protégée.

Il aide à utiliser des mots de passe différents, longs et complexes sans devoir tous les mémoriser.

## Sauvegarde

Les sauvegardes permettent de récupérer les données en cas de panne, suppression accidentelle, vol ou ransomware.

Une bonne méthode est la règle **3-2-1-1** :

- `3` copies des données,
- `2` supports différents,
- `1` copie hors site,
- `1` copie hors ligne.

Bon réflexe :

- sauvegarder régulièrement,
- protéger les sauvegardes,
- vérifier que la sauvegarde s'est bien terminée,
- tester une restauration pour s'assurer que les données sont récupérables.

!!! warning "Important"
    Une sauvegarde non testée n'est pas totalement fiable. Il faut vérifier qu'on peut vraiment restaurer les données.

## Pare-feu

Les pare-feux filtrent les flux réseau entrants et sortants.

Ils permettent de limiter les accès non autorisés et de réduire la surface d'attaque d'une machine ou d'un réseau.

Exemple de paramétrage pour un serveur web avec `ufw` :

```bash
sudo ufw default deny incoming   # bloque les connexions entrantes par défaut
sudo ufw default allow outgoing  # autorise les connexions sortantes
sudo ufw allow 22/tcp            # autorise SSH
sudo ufw allow 80/tcp            # autorise HTTP
sudo ufw allow 443/tcp           # autorise HTTPS
sudo ufw enable                  # active le pare-feu
sudo ufw status                  # affiche les règles actives
```

Dans cet exemple :

- le port `22` permet l'administration à distance avec SSH,
- le port `80` permet l'accès au site en HTTP,
- le port `443` permet l'accès au site en HTTPS,
- les autres connexions entrantes sont bloquées par défaut.

!!! warning "Attention"
    Avant d'activer un pare-feu à distance, il faut toujours autoriser SSH, sinon on risque de perdre l'accès au serveur.

## Mises à jour logiciels et OS

Les mises à jour servent à corriger des bugs et des failles de sécurité.

Un système non mis à jour peut garder des vulnérabilités connues, donc plus faciles à exploiter.

Bon réflexe :

- mettre à jour régulièrement l'OS,
- mettre à jour les logiciels installés,
- vérifier si un redémarrage est nécessaire,
- appliquer rapidement les correctifs de sécurité importants.

Exemple sur Debian ou Ubuntu :

```bash
sudo apt update
sudo apt upgrade
```

## Logs

Les logs sont des journaux qui enregistrent les événements d'une machine.

Ils permettent de comprendre ce qu'il s'est passé, par exemple :

- une erreur système,
- un service qui ne démarre pas,
- une tentative de connexion,
- un problème réseau,
- une action utilisateur.

On les trouve souvent dans :

```text
/var/log
```

Commandes utiles :

```bash
journalctl -xe
tail -f /var/log/syslog
```

!!! tip "À retenir"
    Quand un service ne fonctionne pas, les logs sont souvent le meilleur endroit pour commencer le diagnostic.
