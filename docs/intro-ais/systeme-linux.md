# Système d'exploitation et Linux

## Qu'est-ce qu'un système d'exploitation ?

Un **système d'exploitation** (OS) est le chef d'orchestre de l'ordinateur.

C'est lui qui gère :

- les demandes de l'utilisateur,
- le matériel,
- le lancement des programmes,
- la stabilité du système.

Exemples :

- Windows
- Linux
- macOS

## Linux

Linux est un **kernel** open source sous licence **GPL**.

Il est utilisé dans de nombreuses distributions pour proposer un système complet.

Exemples de distributions :

- Ubuntu
- Debian
- Pop!_OS

Sans ce noyau, le système ne pourrait pas démarrer ni dialoguer correctement avec le matériel.

## Système propriétaire

Un système propriétaire est un système **fermé**.

En général :

- il est développé par une entreprise,
- son code n'est pas ouvert au public,
- sa modification est limitée ou interdite.

Exemple : **Windows**.

## Open source

Un système open source est un système dont le code source est disponible.

Cela signifie qu'il peut être :

- consulté,
- modifié,
- amélioré,
- redistribué selon les règles de sa licence.

## Linux, version simple

Linux est le cœur de nombreuses machines.

C'est lui qui fait en sorte que :

- le PC démarre,
- le matériel fonctionne,
- les programmes puissent s'exécuter.

Au début, son fonctionnement peut sembler moins accessible que celui de Windows, mais une fois les bases comprises, il devient très puissant et très souple.

## Kernel, distribution et environnement graphique

Il ne faut pas confondre **Linux** et une **distribution Linux**.

- **Linux** : le kernel, c'est-à-dire le noyau du système
- **Distribution Linux** : un système complet construit autour du kernel
- **Environnement graphique** : l'interface visuelle avec fenêtres, menus et icônes

Exemples de distributions :

- Debian
- Ubuntu
- Fedora
- Arch Linux

Exemples d'environnements graphiques :

- GNOME
- KDE Plasma
- XFCE

!!! tip "À retenir"
    Quand on dit "j'utilise Linux", on utilise souvent en réalité une distribution Linux, comme Ubuntu ou Debian.

## Rôle du kernel

Le **kernel** fait le lien entre les logiciels et le matériel.

Il gère notamment :

- le processeur,
- la mémoire,
- les disques,
- les périphériques,
- les droits d'accès,
- les processus.

Un logiciel ne parle généralement pas directement au matériel. Il passe par le système d'exploitation, qui s'appuie sur le kernel.

## Arborescence Linux

Linux organise les fichiers sous forme d'arborescence.

Tout commence à la racine :

```text
/
```

Quelques dossiers importants :

| Dossier | Rôle |
| ------- | ---- |
| `/home` | Dossiers personnels des utilisateurs |
| `/etc` | Fichiers de configuration du système |
| `/var` | Données variables, comme les logs |
| `/bin` | Commandes essentielles |
| `/usr` | Programmes et fichiers partagés |
| `/tmp` | Fichiers temporaires |
| `/root` | Dossier personnel de l'utilisateur root |

!!! note "Différence avec Windows"
    Sous Linux, il n'y a pas de lecteur `C:` comme sous Windows. Tout part de `/`.

## Utilisateurs, groupes et droits

Linux est un système multi-utilisateur.

Cela signifie que plusieurs utilisateurs peuvent exister sur la même machine, avec des droits différents.

On distingue souvent :

- l'utilisateur classique,
- les groupes,
- l'utilisateur `root`,
- les droits sur les fichiers.

Les droits permettent de contrôler qui peut :

- lire un fichier,
- modifier un fichier,
- exécuter un fichier.

Exemple de droits affichés avec `ls -l` :

```text
-rw-r--r-- 1 alice alice 1200 mai 12 10:00 notes.txt
```

Dans cet exemple, le propriétaire peut lire et modifier le fichier, alors que les autres peuvent seulement le lire.

## Processus et services

Un **processus** est un programme en cours d'exécution.

Exemples :

- un navigateur ouvert,
- un terminal,
- un serveur web,
- un service SSH.

Un **service** est un programme qui tourne souvent en arrière-plan.

Exemples :

- service réseau,
- serveur web,
- serveur SSH,
- base de données.

Sur beaucoup de distributions modernes, les services sont gérés avec `systemd`.

Exemple :

```bash
systemctl status ssh
```

## Gestion des paquets

Sous Linux, on installe souvent les logiciels avec un **gestionnaire de paquets**.

Le gestionnaire de paquets permet de :

- installer des logiciels,
- mettre à jour le système,
- supprimer des logiciels,
- gérer les dépendances.

Sur Debian et Ubuntu, on utilise souvent `apt`.

Exemples :

```bash
sudo apt update
sudo apt install curl
```

## Logs

Les **logs** sont des fichiers ou journaux qui enregistrent ce qu'il se passe sur le système.

Ils sont très utiles pour comprendre :

- une erreur,
- un démarrage raté,
- un service qui ne fonctionne pas,
- une tentative de connexion,
- un problème matériel.

On trouve souvent des logs dans :

```text
/var/log
```

On peut aussi les consulter avec :

```bash
journalctl
```

## Démarrage d'un système Linux

Au démarrage, plusieurs étapes s'enchaînent :

1. Le BIOS ou l'UEFI initialise le matériel.
2. Le chargeur de démarrage lance le système.
3. Le kernel Linux démarre.
4. Les services système se lancent.
5. L'utilisateur peut ouvrir une session.

Le chargeur de démarrage le plus courant sous Linux est **GRUB**.

## Linux côté serveur

Linux est très utilisé sur les serveurs.

On le retrouve souvent pour :

- héberger des sites web,
- faire tourner des bases de données,
- gérer des services réseau,
- héberger des applications,
- administrer des infrastructures.

Il est apprécié parce qu'il est stable, flexible, automatisable et adapté au fonctionnement en ligne de commande.

## Réflexes pour un AIS

Quand on découvre une machine Linux, quelques questions utiles reviennent souvent :

- Quelle distribution est installée ?
- Quel utilisateur suis-je ?
- Quelle est l'adresse IP de la machine ?
- Quels services tournent ?
- Y a-t-il des erreurs dans les logs ?
- L'espace disque est-il suffisant ?
- Les mises à jour sont-elles faites ?

Commandes souvent utiles :

```bash
whoami
hostname
ip a
df -h
systemctl status ssh
journalctl -xe
```

!!! info "Résumé rapide"
    Linux repose sur un kernel, une arborescence de fichiers, des utilisateurs, des droits, des processus, des services et des logs. Ces notions sont essentielles pour administrer ou dépanner une machine.
