# Administration des systèmes — Linux

## Objectif global

Ce module est le module pivot systèmes Linux de la formation AIS. Il couvre l'ensemble des compétences d'administration Linux nécessaires pour préparer le titre professionnel Administrateur d'Infrastructures Sécurisées (RNCP n°37680, niveau 6). Chaque séquence s'appuie sur l'infrastructure fictive AlpesNet, construite progressivement du J1 au J10.

## Vous apprendrez à

- Installer et configurer une distribution Linux serveur (Debian 12) dans VirtualBox : partitionnement, SSH durci, principe du moindre privilège depuis J1.
- Gérer les utilisateurs, groupes et permissions : comptes humains et comptes service, sudo restreint, chmod, chown, umask, ACL setfacl/getfacl.
- Configurer et analyser les logs système : rsyslog personnalisé, journalctl avec filtres, logrotate, identification d'événements suspects.
- Automatiser des tâches d'administration avec Bash : scripts robustes (set -euo pipefail), fonctions, arguments, planification cron.
- Configurer un serveur de fichiers sécurisé : NFS et Samba avec droits restreints, testés depuis un client.
- Sécuriser un système Linux : ufw, fail2ban, désactivation des services inutiles, durcissement SSH complet.
- Sauvegarder et restaurer une infrastructure : rsync/tar, vérification sha256sum, restauration testée.
- Déployer un serveur web Nginx sécurisé en autonomie et répondre à un scénario d'incident (CTF).

## En fin de module

Tu es capable d'administrer, sécuriser, automatiser et documenter une infrastructure Linux de A à Z, du partitionnement initial au rapport d'incident CTF, selon les standards ANSSI et les exigences du titre professionnel AIS.

## Démarche pédagogique

La trajectoire du module est : configurer → observer → sécuriser. Chaque séquence suit : introduction contextuelle → exemples commentés → exercice d'application → compétence à valider. Tout s'articule autour de l'infrastructure fictive AlpesNet, construite progressivement.

1. **Kit Install + Kit 1 — Environnement et identités (J1-J2)** — Installation de la VM Debian 12, partitionnement, SSH, gestion des utilisateurs et groupes AlpesNet, audit en autonomie.
2. **Kit 2 — Permissions et logs (J2-J3)** — chmod/chown/ACL sur l'infrastructure AlpesNet, configuration rsyslog et logrotate, identification d'événements suspects.
3. **Kit 3 — Bash et automatisation (J4-J5)** — Scripts d'administration robustes, fonctions, arguments, planification cron, autonomie sur script de production.
4. **Kit 4 — Services et durcissement (J6-J7)** — NFS, Samba, durcissement SSH complet, ufw, fail2ban, rapport de durcissement avant/après.
5. **Kit 5 — Sauvegarde et projet intégrateur Nginx (J8-J9)** — rsync, tar, sha256sum, déploiement Nginx sécurisé en autonomie, rapport de déploiement.
6. **Kit 6 — CTF et clôture (J10)** — Challenge individuel sur VM compromise, rapport d'incident, mémo CC-01, archivage RNCP.

Les quatre séquences d'autonomie (~14h cumulées, ~20%) ancrent les apprentissages en situation réelle : consigne écrite, livrable défini, accès aux ressources explicite (usage IA limité à la recherche documentaire, pas de génération de code).
