# Glossaire Systèmes Linux - Itération 1

## Sujet

Installation Debian 12, arborescence Linux, identités, comptes utilisateurs et audit sudo.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Debian | Distribution Linux stable souvent utilisée côté serveur. |
| FHS | Standard d'organisation de l'arborescence Linux : `/etc`, `/var`, `/home`, `/usr`, etc. |
| Utilisateur | Identité locale possédant un UID. |
| Groupe | Ensemble d'utilisateurs identifié par un GID. |
| `/etc/passwd` | Base des comptes utilisateurs et informations publiques. |
| `/etc/shadow` | Fichier protégé contenant les empreintes de mots de passe. |
| `/etc/group` | Liste des groupes et membres. |
| `sudo` | Mécanisme d'exécution de commandes avec privilèges contrôlés. |
| Compte de service | Compte non humain utilisé par un service applicatif ou système. |
| Cycle de vie | Création, modification, verrouillage, déverrouillage et suppression d'un compte. |

## Manipulations faites

| Manipulation | Commandes ou actions |
| --- | --- |
| Installer Debian 12 | Création VM, installation, snapshot, configuration SSH. |
| Lire l'arborescence | `ls /`, `tree`, `find`, lecture de `/etc` et `/var`. |
| Inspecter les identités | `id`, `getent passwd`, `getent group`, `last`, `lastlog`. |
| Gérer les comptes | `adduser`, `usermod`, `passwd`, `chage`, `usermod -L/-U`. |
| Contrôler sudo | `sudo -l`, lecture sudoers, test d'une commande autorisée/refusée. |

## Docs associées

- [Vue d'ensemble Systèmes Linux](../../../admin-systemes-linux/index.md)
- [Kit Install - Environnement de travail](../../../admin-systemes-linux/it-1/atelier1-kit-install.md)
- [FHS - Arborescence Linux](../../../admin-systemes-linux/it-1/atelier2-fhs.md)
- [Identités Linux - passwd shadow group](../../../admin-systemes-linux/it-1/atelier3-identites.md)
- [Comptes AlpesNet - utilisateurs et services](../../../admin-systemes-linux/it-1/atelier4-comptes-alpesnet.md)
- [Cycle de vie des comptes Linux](../../../admin-systemes-linux/it-1/atelier5-cycle-vie-comptes.md)
- [Audit des comptes et droits sudo AlpesNet](../../../admin-systemes-linux/it-1/atelier6-audit-comptes-sudo.md)
- [Carnet de bord](../../../admin-systemes-linux/it-1/carnet-bord-it1.md)
- [Audit AlpesNet](../../../admin-systemes-linux/it-1/audit-comptes-sudo-alpesnet.md)

