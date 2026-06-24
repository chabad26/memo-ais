# Carnet de bord itération 3

## Objectif du carnet

Ce carnet centralise les preuves et explications des exercices Bash et automatisation de l'itération 3.

## En-tête standard

```text
Nom : HIMBLOT
Prénom : Olivier
Site : AlpesNet
Module : Administration des systèmes - Linux
Itération : IT-3 - Bash et automatisation
Date : 23 juin 2026
Machine : srv-oliv
Distribution : Debian GNU/Linux 12 (bookworm)
```

## Partie 1 - Fondamentaux Bash

### Commandes à copier

```bash
ls -l /opt/scripts/fondamentaux.sh
bash /opt/scripts/fondamentaux.sh
getent passwd www-nginx
```

### Preuve 1 - Script fondamentaux.sh

Commande :

```bash
ls -l /opt/scripts/fondamentaux.sh
```

À coller ici :

```text
[Coller ici la sortie de ls -l /opt/scripts/fondamentaux.sh]
```

Interprétation :

```text
Le script /opt/scripts/fondamentaux.sh existe. Le droit x indique qu'il est exécutable.
```

### Preuve 2 - Exécution du script

Commande :

```bash
bash /opt/scripts/fondamentaux.sh
```

À coller ici :

```text
[Coller ici la sortie complète du script]
```

Interprétation :

```text
Le script affiche le serveur, la date, le répertoire de logs et vérifie les comptes AlpesNet.
Les comptes présents affichent OK. Une alerte doit apparaître si un compte service possède un shell actif.
```

### Preuve 3 - Shell de www-nginx

Commande :

```bash
getent passwd www-nginx
```

À coller ici :

```text
[Coller ici la ligne getent passwd www-nginx]
```

Interprétation :

```text
Le dernier champ de la ligne correspond au shell. Pour un compte service, le shell attendu est /usr/sbin/nologin.
```

## Explications demandées

### Rôle de set -euo pipefail

```text
set -euo pipefail rend le script plus sûr :
- -e arrête le script si une commande échoue ;
- -u arrête le script si une variable non définie est utilisée ;
- pipefail détecte les erreurs dans les pipelines.
Cette ligne évite qu'un script d'administration continue après une erreur.
```

### Rôle du tableau COMPTES

```text
Le tableau COMPTES contient la liste des comptes à vérifier.
Il permet d'éviter de répéter le même bloc de code pour chaque utilisateur.
Dans ce script, il contient alice.martin, bob.dupont, www-nginx et backup-agent.
```

### Rôle de la boucle for

```text
La boucle for parcourt chaque élément du tableau COMPTES.
À chaque tour, la variable compte contient un nom différent.
Le script vérifie alors si ce compte existe, récupère son shell et affiche le résultat.
```

### Rôle du test sur LOG_DIR

```text
Le test if [ -d "${LOG_DIR}" ] vérifie que /var/log/alpesnet existe bien comme répertoire.
Si le répertoire existe, le script affiche OK.
Sinon, il affiche une alerte.
```

### Rôle de la condition sur www-nginx

```text
La condition vérifie que le compte service www-nginx utilise bien /usr/sbin/nologin.
Si www-nginx utilise un shell actif, le script affiche ALERTE : compte service avec shell actif.
Cela permet de détecter un compte service pouvant ouvrir une session interactive.
```

## Partie 2 - Scripts d'administration pratiques

### audit-comptes.sh

Chemin du script :

```text
/opt/scripts/audit-comptes.sh
```

Commande d'exécution :

```bash
sudo /opt/scripts/audit-comptes.sh
```

Log créé :

```text
[Coller ici le chemin du log créé dans /var/log/alpesnet/]
```

Commande utile pour trouver le log :

```bash
sudo bash -c 'ls -l /var/log/alpesnet/audit-comptes-*.log'
```

Trois lignes importantes du log :

```text
[Coller ici 3 lignes importantes du log audit-comptes]
```

Explication du test UID 0 :

```text
Le script recherche les comptes dont l'UID vaut 0 avec awk.
Sur Linux, l'UID 0 donne les privilèges root.
Le seul compte attendu avec UID 0 est root.
Si un autre compte apparaît, c'est une anomalie critique.
```

Explication du cas bob.dupont verrouillé :

```text
Le script récupère le statut du compte avec passwd -S.
Si bob.dupont a le statut L, cela signifie que son compte est verrouillé.
Dans le contexte AlpesNet, ce verrouillage peut être normal après un départ.
Le script affiche alors : INFO : bob.dupont est verrouillé — normal après départ.
```

### archivage-logs.sh

Chemin du script :

```text
/opt/scripts/archivage-logs.sh
```

Commande d'exécution :

```bash
sudo /opt/scripts/archivage-logs.sh
```

Valeur `RETENTION_JOURS` :

```text
RETENTION_JOURS=3
```

Explication de `find` :

```text
find parcourt un répertoire et sélectionne les fichiers qui correspondent aux critères donnés.
Dans le script, il cherche dans /var/log/alpesnet les fichiers de type fichier (-type f), dont le nom finit par .log (-name "*.log"), et qui sont plus anciens que la durée de rétention (-mtime +RETENTION_JOURS).
Chaque fichier trouvé est ensuite lu par la boucle while.
```

Explication de `-mtime +3` :

```text
-mtime +3 signifie : fichiers modifiés il y a plus de 3 jours complets.
Ce n'est pas exactement 3 jours, mais strictement plus ancien que 3 jours.
Avec RETENTION_JOURS=3, seuls les logs assez anciens sont archivés.
```

Résultat dans `/backup/logs-alpesnet` :

```text
total 0
```

Interprétation :

```text
Le dossier /backup/logs-alpesnet contient les archives compressées générées par le script.
S'il est vide, aucun fichier .log ne correspondait au critère -mtime +3 au moment de l'exécution.
```

## Partie 3 - Planification cron

### Commandes à copier

```bash
sudo crontab -l
sudo grep -a CRON /var/log/syslog | tail -20
sudo tail -n 30 /var/log/alpesnet/cron-audit.log
```

### Preuve 1 - Crontab finale

Commande :

```bash
sudo crontab -l
```

À coller ici :

```text
[Coller ici la sortie de sudo crontab -l]
```

Interprétation :

```text
La crontab root contient les deux règles finales :
- audit-comptes.sh tous les jours à 02h00 ;
- archivage-logs.sh tous les lundis à 03h00.
La règle temporaire toutes les 2 minutes n'est plus présente.
```

### Preuve 2 - Traces CRON dans syslog

Commande :

```bash
sudo grep -a CRON /var/log/syslog | tail -20
```

À coller ici :

```text
[Coller ici les lignes CRON visibles dans syslog]
```

Interprétation :

```text
Les lignes CRON dans /var/log/syslog prouvent que le service cron a bien déclenché des commandes planifiées.
On y retrouve l'utilisateur qui exécute la tâche, souvent root, et la commande lancée.
```

### Preuve 3 - Log d'audit cron

Commande :

```bash
sudo tail -n 30 /var/log/alpesnet/cron-audit.log
```

À coller ici :

```text
[Coller ici la sortie de cron-audit.log]
```

Interprétation :

```text
Le fichier /var/log/alpesnet/cron-audit.log reçoit la sortie de la tâche cron d'audit.
Il permet de consulter les messages ou erreurs produits par le script planifié.
```

## Explications cron demandées

### Rôle de chaque champ cron

```text
Une ligne cron contient 5 champs de temps suivis de la commande :
minute heure jour_du_mois mois jour_de_semaine commande.
Exemple : 0 2 * * * signifie tous les jours à 02h00.
Exemple : 0 3 * * 1 signifie tous les lundis à 03h00.
```

### Pourquoi rediriger les sorties vers /var/log/alpesnet

```text
Les scripts planifiés s'exécutent sans terminal visible.
La redirection >> /var/log/alpesnet/cron-audit.log permet de conserver la sortie standard.
La redirection 2>&1 ajoute aussi les erreurs dans le même fichier.
Cela donne une trace consultable après l'exécution.
```

### Pourquoi supprimer la règle temporaire

```text
La règle temporaire */2 * * * * sert uniquement à tester rapidement cron.
Si elle reste en place, le script s'exécute toutes les deux minutes, ce qui peut remplir les logs et lancer trop souvent une action d'administration.
Après validation, on ne garde que les deux règles finales.
```

### Ce que prouvent les lignes CRON dans syslog

```text
Les lignes CRON dans syslog prouvent que le service cron a bien déclenché une tâche.
Elles indiquent la date, l'heure, l'utilisateur d'exécution et la commande lancée.
Elles permettent de confirmer que la planification fonctionne réellement.
```

## Partie 4 - Fonctions, arguments et trap Bash

### Commandes à copier

```bash
ls -l /opt/scripts/audit-comptes-arguments.sh
/opt/scripts/audit-comptes-arguments.sh
/opt/scripts/audit-comptes-arguments.sh alice.martin bob.dupont
/opt/scripts/audit-comptes-arguments.sh compte.inexistant
```

### Preuve 1 - Script avec arguments

Commande :

```bash
ls -l /opt/scripts/audit-comptes-arguments.sh
```

À coller ici :

```text
[Coller ici la sortie de ls -l /opt/scripts/audit-comptes-arguments.sh]
```

Interprétation :

```text
Le script audit-comptes-arguments.sh existe et possède le droit d'exécution.
```

### Preuve 2 - Exécution sans argument

Commande :

```bash
/opt/scripts/audit-comptes-arguments.sh
```

À coller ici :

```text
[Coller ici la sortie sans argument]
```

Interprétation :

```text
Sans argument, le script utilise la liste de comptes par défaut et audite les comptes AlpesNet.
```

### Preuve 3 - Exécution avec arguments

Commande :

```bash
/opt/scripts/audit-comptes-arguments.sh alice.martin bob.dupont
```

À coller ici :

```text
[Coller ici la sortie avec alice.martin et bob.dupont]
```

Interprétation :

```text
Avec des arguments, le script audite uniquement les comptes fournis sur la ligne de commande.
```

### Preuve 4 - Compte inexistant

Commande :

```bash
/opt/scripts/audit-comptes-arguments.sh compte.inexistant
```

À coller ici :

```text
[Coller ici la sortie avec compte.inexistant]
```

Interprétation :

```text
Le script affiche une ligne [ERROR] lorsque le compte demandé n'existe pas.
```

## Explications fonctions, arguments et trap

### Rôle de $#

```text
$# contient le nombre d'arguments passés au script.
Il permet de choisir entre le mode par défaut et le mode ciblé.
Si $# vaut 0, aucun argument n'a été fourni.
```

### Rôle de "$@"

```text
"$@" représente tous les arguments passés au script, en conservant chaque argument séparé.
Il permet de faire une boucle sur tous les comptes fournis par l'utilisateur.
```

### Rôle de local

```text
local limite une variable à la fonction dans laquelle elle est déclarée.
Cela évite qu'une variable interne modifie accidentellement une variable du reste du script.
```

### Différence entre log_info et log_error

```text
log_info sert à afficher un message normal avec horodatage.
log_error sert à afficher une erreur avec horodatage et l'envoie sur la sortie d'erreur avec >&2.
Les deux rendent les logs plus lisibles.
```

### Rôle de trap cleanup EXIT

```text
trap cleanup EXIT exécute la fonction cleanup à la fin du script.
Cela permet d'afficher un message final ou de nettoyer des fichiers temporaires, même si le script s'arrête après une erreur.
```

## Partie 5 - Script administration robuste AlpesNet

### Commandes à copier

```bash
ls -l /opt/scripts/admin-alpesnet.sh
/opt/scripts/admin-alpesnet.sh --help
sudo /opt/scripts/admin-alpesnet.sh
sudo /opt/scripts/admin-alpesnet.sh --compte alice.martin
sudo bash -c 'tail -n 40 "$(ls -t /var/log/alpesnet/rapport-admin-*.log | head -1)"'
sudo crontab -l
```

### Preuve 1 - Script robuste

Commande :

```bash
ls -l /opt/scripts/admin-alpesnet.sh
```

À coller ici :

```text
[Coller ici la sortie de ls -l /opt/scripts/admin-alpesnet.sh]
```

Interprétation :

```text
Le script admin-alpesnet.sh existe dans /opt/scripts et possède le droit d'exécution.
```

### Preuve 2 - Aide du script

Commande :

```bash
/opt/scripts/admin-alpesnet.sh --help
```

À coller ici :

```text
[Coller ici la sortie de l'aide]
```

Interprétation :

```text
L'option --help affiche le mode d'utilisation du script et les arguments disponibles.
```

### Preuve 3 - Exécution sans argument

Commande :

```bash
sudo /opt/scripts/admin-alpesnet.sh
```

À coller ici :

```text
[Coller ici la sortie du mode complet]
```

Interprétation :

```text
Sans argument, le script réalise l'audit complet des comptes AlpesNet, lance l'archivage des logs et génère un rapport.
```

### Preuve 4 - Exécution avec --compte

Commande :

```bash
sudo /opt/scripts/admin-alpesnet.sh --compte alice.martin
```

À coller ici :

```text
[Coller ici la sortie du mode ciblé]
```

Interprétation :

```text
Avec --compte alice.martin, le script audite uniquement ce compte pour la partie comptes, tout en conservant les autres actions prévues.
```

### Preuve 5 - Rapport généré

Commande :

```bash
sudo bash -c 'tail -n 40 "$(ls -t /var/log/alpesnet/rapport-admin-*.log | head -1)"'
```

À coller ici :

```text
[Coller ici les dernières lignes du rapport généré]
```

Interprétation :

```text
Le rapport contient les messages INFO et ERROR horodatés, les comptes audités, l'archivage des logs et le chemin du rapport généré.
```

### Preuve 6 - Planification cron

Commande :

```bash
sudo crontab -l
```

À coller ici :

```text
[Coller ici la crontab contenant admin-alpesnet.sh]
```

Interprétation :

```text
La crontab planifie le script admin-alpesnet.sh à la fréquence choisie et redirige sa sortie vers /var/log/alpesnet/cron-admin.log.
```

## Explications script robuste

### Pourquoi set -euo pipefail est obligatoire

```text
set -euo pipefail sécurise l'exécution :
- le script s'arrête si une commande échoue ;
- le script s'arrête si une variable non définie est utilisée ;
- les erreurs dans les pipelines sont détectées.
C'est indispensable pour un script d'administration lancé avec sudo ou cron.
```

### Rôle de log_info

```text
log_info écrit un message informatif horodaté.
Il permet de suivre les étapes normales du script dans le terminal et dans le rapport.
```

### Rôle de log_error

```text
log_error écrit un message d'erreur horodaté.
Il envoie le message sur la sortie d'erreur, ce qui permet de distinguer les anomalies des informations normales.
```

### Comportement sans argument

```text
Sans argument, le script fonctionne en mode complet.
Il audite les comptes définis dans le tableau, archive les logs anciens et produit un rapport.
```

### Comportement avec --compte

```text
Avec --compte NOM, le script fonctionne en mode ciblé pour l'audit des comptes.
Il permet de vérifier rapidement un compte précis sans modifier le script.
```

### Fréquence cron choisie

```text
La fréquence choisie est quotidienne à 02h30.
Ce créneau est adapté car il se situe la nuit, hors période d'activité habituelle, et après les autres tâches d'audit déjà planifiées.
```

### Intérêt de rediriger la sortie cron vers un log

```text
cron exécute les scripts sans terminal visible.
La redirection >> /var/log/alpesnet/cron-admin.log 2>&1 conserve la sortie standard et les erreurs.
Cela permet de vérifier après coup si le script s'est exécuté correctement.
```
