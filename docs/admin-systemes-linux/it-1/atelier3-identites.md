# Atelier 3 - Identités Linux - Auditer passwd, shadow et group

## Objectif

Lire `/etc/passwd`, `/etc/shadow` et `/etc/group` pour auditer un système Linux et identifier les comptes dangereux.

Ces trois fichiers forment la base locale des identités du système. Leur contenu détermine :

- quels comptes existent ;
- quels comptes peuvent ouvrir une session ;
- quels UID et GID sont attribués ;
- quels groupes donnent des droits particuliers ;
- quels comptes présentent un risque de sécurité.

Dans l'incident déclencheur, l'attaquant exploitait un compte présent dans `/etc/passwd` avec `UID 0`. C'était donc un second compte root, moins visible que `root`, mais avec les mêmes privilèges. Savoir lire ces fichiers est une compétence de base pour administrer et auditer Linux.

## Les trois fichiers d'identité

| Fichier | Rôle | Lisibilité |
| --- | --- | --- |
| `/etc/passwd` | Liste des comptes, UID, GID, home et shell | Lisible par tous |
| `/etc/shadow` | Hashs de mots de passe et informations d'expiration | Lisible par root uniquement |
| `/etc/group` | Liste des groupes et de leurs membres | Lisible par tous |

## Format de `/etc/passwd`

Dans `/etc/passwd`, une ligne correspond à un compte.

Exemple :

```text
alice.martin:x:1001:1001:Alice Martin Lead DevOps:/home/alice.martin:/bin/bash
```

Lecture des champs :

| Champ | Exemple | Signification |
| --- | --- | --- |
| 1 | `alice.martin` | Login |
| 2 | `x` | Mot de passe stocké dans `/etc/shadow` |
| 3 | `1001` | UID, identifiant numérique de l'utilisateur |
| 4 | `1001` | GID principal |
| 5 | `Alice Martin Lead DevOps` | Commentaire ou description |
| 6 | `/home/alice.martin` | Répertoire personnel |
| 7 | `/bin/bash` | Shell de connexion |

!!! warning "Compte critique"
    Tout compte avec `UID 0` autre que `root` est un compte compromis ou gravement mal configuré. Pour Linux, l'UID fait l'identité réelle : un compte avec `UID 0` a les privilèges root.

## Étape 1 - Lister les comptes avec shell actif

Afficher les comptes qui semblent pouvoir ouvrir une session interactive :

```bash
grep -Ev "nologin|false|sync" /etc/passwd
```

Point de contrôle : repérer les comptes humains ou administrateurs, par exemple `root`, `oliv` ou `adm-[prenom]`.

## Étape 2 - Détecter les comptes UID 0

Chercher tous les comptes ayant l'UID `0` :

```bash
awk -F: '($3==0){print "UID 0 :",$1}' /etc/passwd
```

Résultat attendu sur un système sain :

```text
UID 0 : root
```

Point de contrôle : aucun autre compte que `root` ne doit apparaître.

![Audit des comptes actifs, UID 0 et shadow](../../assets/img/admin-systemes-linux/it-1/passwd-shadow-audit.png)

## Étape 3 - Lire `/etc/shadow` avec sudo

Le fichier `/etc/shadow` contient les informations sensibles liées aux mots de passe. Il n'est pas lisible par un utilisateur standard.

Tester :

```bash
cat /etc/shadow
```

Puis avec les droits administrateur :

```bash
sudo head /etc/shadow
```

Point de contrôle : l'accès direct doit être refusé, mais l'accès avec `sudo` doit fonctionner.

## Étape 4 - Détecter les comptes sans mot de passe

Chercher les comptes dont le champ mot de passe est vide ou anormal :

```bash
sudo awk -F: '($2=="" || $2=="!*"){print "SANS MOT DE PASSE :",$1}' /etc/shadow
```

Point de contrôle : aucun compte humain actif ne doit apparaître dans cette liste.

!!! note "Interprétation"
    Un compte système verrouillé peut avoir une valeur spéciale dans `/etc/shadow`. Ce n'est pas forcément une anomalie. Le risque principal concerne les comptes humains ou les comptes de service actifs.

## Étape 5 - Lire les groupes importants

Afficher les groupes qui donnent souvent des droits particuliers :

```bash
cat /etc/group | grep -E "^sudo|^devops|^readonly"
```

Selon la VM, certains groupes comme `devops` ou `readonly` peuvent ne pas encore exister.

Pour afficher tous les groupes :

```bash
cat /etc/group
```

Point de contrôle : identifier les membres du groupe `sudo`.

![Lecture du fichier group](../../assets/img/admin-systemes-linux/it-1/group-list.png)

## Étape 6 - Identifier les groupes système

Les groupes système ont généralement un GID inférieur à `100`.

```bash
awk -F: '($3 < 100){print $1,$3}' /etc/group
```

Point de contrôle : repérer quelques groupes système comme `root`, `daemon`, `adm`, `sudo`, `www-data` selon les paquets installés.

![Groupes système avec GID inférieur à 100](../../assets/img/admin-systemes-linux/it-1/system-groups-gid.png)

## Étape 7 - Comparer deux identités avec `id`

Comparer l'identité de `root` avec celle d'un compte administrateur.

```bash
id root
id adm-[prenom]
```

Exemple avec `oliv` :

```bash
id root
id oliv
```

Point de contrôle :

- `root` doit avoir `uid=0`.
- l'utilisateur normal ne doit pas avoir `uid=0`.
- l'utilisateur administrateur peut appartenir au groupe `sudo`.

![Comparaison id oliv et id root](../../assets/img/admin-systemes-linux/it-1/id-root-oliv.png)

## Ressources

- `man passwd` section 5 - format du fichier `/etc/passwd`
- `man shadow` section 5 - format du fichier `/etc/shadow`
- `man group` section 5 - format du fichier `/etc/group`
- Debian Handbook - Gestion des utilisateurs : <https://www.debian.org/doc/manuals/debian-handbook/users.fr.html>
- Linux PAM - authentification pluggable : <https://www.linux-pam.org/Linux-PAM-html/>

## Synthèse à retenir

Sur Linux, l'identité est d'abord numérique : l'UID et le GID comptent plus que le nom affiché. Un compte nommé autrement que `root`, mais avec `UID 0`, est root techniquement.

L'audit de base consiste donc à lire `/etc/passwd`, contrôler `/etc/shadow`, vérifier `/etc/group`, puis interpréter les résultats avec `id`. Ces réflexes permettent d'éviter les comptes oubliés, les droits sudo excessifs et les comptes de service dangereux.
