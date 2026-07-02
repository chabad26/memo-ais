# Glossaire Systèmes Linux - Itération 6

## Sujet

Challenge final CTF AlpesNet : investigation sur VM compromise, récupération de flags, corrections de sécurité et rapport d'incident final.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| CTF | Challenge technique où il faut trouver des preuves appelées flags. |
| VM compromise | Machine volontairement vulnérable ou déjà attaquée, utilisée pour enquêter et corriger. |
| Flag | Fichier ou valeur qui prouve qu'une étape du challenge est validée. |
| `/flags` | Dossier où sont déposées les preuves finales du CTF. |
| Accès root | Accès administrateur complet sur la machine Linux. |
| Compte intrus | Compte non autorisé créé ou utilisé par l'attaquant. |
| UID 0 suspect | Compte autre que `root` possédant l'UID `0`, donc les droits administrateur complets. |
| Shell interactif suspect | Shell comme `/bin/bash` attribué à un compte qui ne devrait pas se connecter. |
| IP source | Adresse IP d'où viennent les tentatives d'intrusion observées dans les logs. |
| Permission dangereuse | Droit trop ouvert, par exemple `777`, ou bit spécial inattendu sur un fichier sensible. |
| SUID suspect | Bit SUID placé sur un binaire non prévu, pouvant permettre une escalade de privilèges. |
| Durcissement post-incident | Corrections appliquées après investigation pour réduire la surface d'attaque. |
| État avant/après | Comparaison entre la configuration initiale compromise et l'état corrigé. |
| Preuve rejouable | Commande dont le résultat peut être relancé devant le formateur pour vérifier l'analyse. |
| Démo live | Validation orale où l'on montre les commandes et les résultats sur la VM. |
| Rapport d'incident | Document final qui explique timeline, causes, actions correctives, état final et recommandations. |
| Timeline | Chronologie des constats, actions et corrections effectuées pendant l'incident. |
| Cause racine | Faiblesse principale ayant permis ou facilité la compromission. |
| Recommandation | Mesure durable proposée après correction immédiate. |

## Manipulations faites

| Manipulation | Commandes ou actions |
| --- | --- |
| Lancer le script CTF | `sudo ./ctf-alpesnet.sh --menu --prenom Olivier --ip X.X.X.X`. |
| Valider une étape précise | `sudo ./ctf-alpesnet.sh --task F2 --prenom Olivier --ip X.X.X.X`. |
| Appliquer les corrections | Ajouter `--apply` seulement quand l'action est comprise et voulue. |
| Prouver l'accès root | `id`, `whoami`, `sudo -l`, test `sudo su` ou connexion root selon le scénario. |
| Chercher un indice dans les homes | `find /home ...`, `grep -RInEi ...` en évitant les fichiers `.ctf_answer*`. |
| Auditer les UID 0 | `awk -F: '($3==0){print $1":"$3":"$6":"$7}' /etc/passwd`. |
| Vérifier un compte suspect | `getent passwd compte`, `id compte`, `lastlog -u compte`, `chage -l compte`. |
| Lire les sudoers actifs | `find /etc/sudoers.d ... -exec grep ...`. |
| Supprimer le compte intrus | `sudo userdel -r compte_suspect`, puis `getent passwd compte_suspect`. |
| Extraire l'IP source | `grep` dans `/var/log/auth.log`, puis comptage des IP avec `awk`, `sort`, `uniq -c`. |
| Rechercher un `777` dangereux | `sudo find / -xdev -perm 0777 -printf '%m %u:%g %p\n' 2>/dev/null`. |
| Rechercher les SUID | `sudo find / -xdev -perm /4000 -printf '%m %u:%g %p\n' 2>/dev/null`. |
| Corriger une permission | `sudo chmod 750 /chemin/dangereux`, puis `stat -c '%a %A %U:%G %n' /chemin/dangereux`. |
| Vérifier le durcissement SSH | `sshd -T`, `grep` dans `sshd_config`, tests `ssh oliv`, `ssh root`, `ssh autre_compte`. |
| Vérifier UFW | `sudo ufw status verbose`. |
| Vérifier Fail2ban | `sudo fail2ban-client status`, `sudo fail2ban-client status sshd`. |
| Diagnostiquer Nginx | `sudo nginx -t`, `systemctl status nginx`, `journalctl -u nginx -n 50`. |
| Prouver HTTP 200 | `curl -I -H 'Cache-Control: no-cache' http://X.X.X.X`. |
| Créer la sauvegarde CTF | `tar -C / -czf /backup/ctf-alpesnet-DATE.tar.gz etc var/www`. |
| Vérifier le checksum | `sha256sum -c /backup/ctf-alpesnet-*.tar.gz.sha256`. |
| Générer le rapport final | `sudo ./ctf-alpesnet.sh --task F8 --prenom Olivier --ip X.X.X.X`. |

## Point clé : un flag doit être justifié

Un flag seul ne suffit pas. Pour chaque étape, il faut garder :

- la commande utilisée ;
- le résultat observé ;
- l'explication du risque ;
- la correction appliquée si nécessaire ;
- la commande de vérification finale.

Exemple de logique :

```text
Constat : /var/www/upload est en 777
Risque : tout utilisateur local peut écrire ou modifier le contenu
Correction : chmod 750 /var/www/upload
Vérification : stat -c '%a %A %U:%G %n' /var/www/upload
```

## Point clé : ne pas confondre enquête et correction

Pendant un CTF d'incident, l'ordre compte :

1. observer l'état initial ;
2. collecter les preuves ;
3. identifier le problème ;
4. appliquer la correction ;
5. vérifier l'état corrigé ;
6. écrire le rapport.

Corriger trop vite peut faire disparaître une preuve utile. Le bon réflexe est de capturer l'avant/après avec des commandes rejouables.

## Point clé : durcissement adapté au scénario

Dans cette itération, certaines règles diffèrent d'un durcissement idéal complet. Par exemple, `PasswordAuthentication yes` peut être conservé pendant le CTF pour ne pas casser l'accès SSH ou `scp` du compte autorisé.

À retenir :

- `AllowUsers oliv` limite les comptes autorisés en SSH ;
- `PermitEmptyPasswords no` refuse les mots de passe vides ;
- `ufw` doit être actif avec seulement les ports utiles ;
- `fail2ban` doit surveiller `sshd` ;
- les services inutiles doivent être arrêtés, désactivés ou absents.

## Point clé : structure du rapport d'incident

Le rapport final doit permettre à quelqu'un d'autre de comprendre et rejouer le raisonnement.

Structure minimale :

| Partie | Contenu attendu |
| --- | --- |
| Timeline | Quand les étapes F1 à F7 ont été traitées. |
| Causes | Compte, service, permission ou configuration ayant facilité l'incident. |
| Actions correctives | Commandes appliquées et raisons. |
| État final | SSH limité, pare-feu actif, Fail2ban actif, Nginx HTTP 200, sauvegarde vérifiée. |
| Recommandations | Mesures à garder après le CTF. |
| Détail step by step | Preuves détaillées pour chaque flag. |

## Docs associées

- [Guide CTF AlpesNet et script d'automatisation](../../../admin-systemes-linux/it-6/ctf-challenge-final.md)
- [Validation du challenge CTF](../../../admin-systemes-linux/it-6/validation-ctf-alpesnet.md)
- [Rapport automatique Challenge final CTF](../../../admin-systemes-linux/it-6/rapport_Olivier.md)
- [Script CTF AlpesNet](../../../assets/scripts/admin-systemes-linux/it-6/ctf-alpesnet.sh)
