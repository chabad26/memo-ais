# Outils cyber et notions d'attaque

## Sujet

Fiche transversale pour relier les outils cyber aux notions déjà vues : durcissement Linux, logs, permissions, services réseau, filtrage, supervision et préparation de challenge.

L'objectif n'est pas de faire de l'attaque avancée, mais de comprendre à quoi servent les outils et ce qu'un administrateur doit vérifier pour défendre un système.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| SELinux | Module de sécurité Linux qui applique des règles obligatoires sur les processus, fichiers, ports et services. |
| AppArmor | Module de sécurité Linux qui limite ce qu'un programme a le droit de faire avec des profils. |
| MAC | Mandatory Access Control : règles de sécurité imposées par le système, même si les droits Unix semblent autoriser l'action. |
| DAC | Discretionary Access Control : droits classiques Linux basés sur propriétaire, groupe et permissions. |
| `chroot` | Change la racine apparente d'un processus pour le limiter à une partie du système de fichiers. |
| `lsof` | Liste les fichiers, sockets et ports ouverts par les processus. Utile pour savoir quel service utilise quoi. |
| Tripwire | Outil de contrôle d'intégrité : il détecte si des fichiers sensibles ont été modifiés. |
| `chkrootkit` | Outil qui cherche des indices de rootkit connus sur un système Linux. |
| `rkhunter` | Outil d'audit qui recherche rootkits, fichiers suspects, permissions faibles et configurations risquées. |
| Logwatch | Outil qui résume les logs système pour repérer les événements importants. |
| LNAV | Logfile Navigator : lecteur de logs en terminal avec coloration, filtres et recherche. |
| PAM | Pluggable Authentication Modules : mécanisme Linux qui gère les règles d'authentification. |
| Rootkit | Ensemble de fichiers ou techniques utilisés pour cacher une compromission et garder un accès privilégié. |
| IOC | Indicator of Compromise : indice possible d'incident, par exemple un compte inconnu, un port anormal ou un fichier modifié. |
| Injection SQL | Technique d'attaque qui tente d'injecter du SQL dans une entrée mal filtrée. |
| Bruteforce | Tentatives répétées de mots de passe ou de clés jusqu'à trouver un accès. |
| Escalade de privilèges | Passage d'un compte limité à un compte plus puissant, souvent `root` ou administrateur. |
| Surface d'attaque | Ensemble des services, ports, comptes, applications et droits exposés à un risque. |

## Manipulations faites ou à savoir refaire

| Objectif | Commandes ou actions |
| --- | --- |
| Voir les ports et services exposés | `ss -tulnp`, `sudo lsof -i -P -n`. |
| Identifier quel processus utilise un fichier ou un port | `sudo lsof /chemin/fichier`, `sudo lsof -i :22`. |
| Lire les logs d'authentification | `sudo journalctl -u ssh`, `sudo tail -f /var/log/auth.log`. |
| Résumer les logs | `sudo logwatch --detail High --range today`. |
| Explorer plusieurs logs rapidement | `sudo lnav /var/log/auth.log /var/log/syslog`. |
| Vérifier AppArmor | `sudo aa-status`, vérifier les profils en mode `enforce` ou `complain`. |
| Vérifier SELinux | `getenforce`, `sestatus` si SELinux est installé. |
| Comprendre un environnement `chroot` | Vérifier la racine isolée, les bibliothèques nécessaires, les droits et les montages accessibles. |
| Lancer une recherche d'indices rootkit | `sudo rkhunter --check`, `sudo chkrootkit`. |
| Surveiller l'intégrité de fichiers sensibles | Initialiser Tripwire puis comparer l'état de référence avec l'état actuel. |
| Contrôler les règles PAM | Lire `/etc/pam.d/`, vérifier les règles appliquées à `sudo`, `login` ou `sshd`. |
| Réduire la surface d'attaque | Désactiver les services inutiles, fermer les ports, limiter SSH, appliquer UFW/nftables. |
| Réagir à un indice suspect | Sauvegarder les preuves, noter l'heure, vérifier comptes, processus, ports, logs et fichiers modifiés. |

## À quoi ça sert côté défense

| Besoin | Outils utiles | Ce qu'on cherche |
| --- | --- | --- |
| Durcir un service | SELinux, AppArmor, PAM, UFW, nftables | Limiter ce qu'un service peut faire et qui peut s'y connecter. |
| Cloisonner une application | `chroot`, conteneur, droits Unix restrictifs | Réduire ce que l'application voit du système si elle est compromise. |
| Surveiller les accès | Logwatch, LNAV, `journalctl`, Fail2ban | Connexions échouées, comptes inconnus, bruteforce SSH. |
| Comprendre l'exposition | `ss`, `lsof`, Nmap en contexte autorisé | Ports ouverts, services inutiles, processus inattendus. |
| Détecter une modification suspecte | Tripwire, `find`, checksums | Fichier sensible modifié, binaire remplacé, permission anormale. |
| Chercher des traces de compromission | `rkhunter`, `chkrootkit`, logs, comptes | Rootkit connu, utilisateur suspect, cron anormal, service caché. |
| Préparer un challenge ou audit | Documentation, captures, tableau de tests | Preuves de sécurité et corrections vérifiables. |

## Exemples simples

### Exemple 1 : port ouvert inattendu

```bash
sudo ss -tulnp
sudo lsof -i -P -n
```

Questions à se poser :

- quel processus écoute ?
- est-ce un service attendu ?
- quel utilisateur lance ce processus ?
- faut-il fermer le port avec UFW/nftables ou arrêter le service ?

### Exemple 2 : échecs SSH répétés

```bash
sudo journalctl -u ssh --since today
sudo fail2ban-client status sshd
```

À relier aux notions vues :

- logs système ;
- durcissement SSH ;
- limitation des accès ;
- bannissement temporaire avec Fail2ban.

### Exemple 3 : injection SQL, version défense

Une injection SQL arrive quand une application construit une requête SQL avec une entrée utilisateur mal contrôlée.

Exemple d'entrée dangereuse à reconnaître en log :

```text
' OR '1'='1
```

Bonnes réactions côté administrateur :

- ne pas tester sur un système sans autorisation ;
- chercher les traces dans les logs applicatifs et web ;
- vérifier les erreurs SQL visibles côté utilisateur ;
- signaler au développeur que les requêtes doivent utiliser des paramètres préparés ;
- vérifier que les droits de la base sont limités.

## Points à ne pas confondre

| À ne pas confondre | Différence |
| --- | --- |
| `lsof` et `ss` | `ss` montre surtout les sockets réseau ; `lsof` relie fichiers, ports et processus. |
| AppArmor et SELinux | Les deux limitent les actions des programmes, mais avec des modèles et outils différents. |
| `chroot` et vraie isolation | `chroot` limite la vue du système de fichiers, mais ne remplace pas les droits, les mises à jour, AppArmor/SELinux ou un conteneur bien configuré. |
| Logwatch et LNAV | Logwatch produit un résumé ; LNAV aide à lire et filtrer les logs en direct. |
| `rkhunter` et `chkrootkit` | Les deux cherchent des indices de rootkit, mais aucun ne prouve seul qu'une machine est saine. |
| Détection et remédiation | Détecter un indice ne suffit pas : il faut isoler, sauvegarder les preuves, corriger et vérifier. |
| Outil cyber et preuve | Un outil donne un résultat ; la preuve est la capture, le log, la commande et l'explication associée. |

## Réflexe méthode

1. Identifier ce qui est exposé : ports, services, comptes.
2. Lire les logs autour de l'heure suspecte.
3. Comparer avec l'état attendu : services, droits, fichiers, règles firewall.
4. Corriger sans effacer les preuves utiles.
5. Vérifier après correction avec une commande claire.
6. Documenter : commande, résultat, conclusion.

## Docs associées

- [Bases cybersécurité](../../intro-ais/securite.md)
- [Menaces et cyberattaque du CHU de Rouen](../../intro-ais/securite-menaces.md)
- [Glossaire Systèmes Linux - Itération 2](admin-systemes-linux/it-2.md)
- [Glossaire Systèmes Linux - Itération 4](admin-systemes-linux/it-4.md)
- [Glossaire Réseaux sécurisés - Itération 5](admin-reseaux-securisation/it-5.md)
- [Glossaire Réseaux sécurisés - Itération 6](admin-reseaux-securisation/it-6.md)
