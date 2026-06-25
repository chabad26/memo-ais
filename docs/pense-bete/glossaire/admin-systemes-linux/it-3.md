# Glossaire Systèmes Linux - Itération 3

## Sujet

Bash, scripts d'administration, fonctions, arguments, gestion d'erreurs, `cron` et traces d'exécution.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Script Bash | Fichier contenant une suite de commandes exécutables. |
| Shebang | Première ligne indiquant l'interpréteur : `#!/usr/bin/env bash`. |
| Variable | Nom associé à une valeur dans un script. |
| Argument | Valeur passée à un script ou une fonction. |
| Code retour | Valeur indiquant succès (`0`) ou erreur (`!=0`). |
| `set -euo pipefail` | Options Bash pour rendre les scripts plus stricts. |
| Fonction | Bloc réutilisable dans un script. |
| `trap` | Mécanisme qui réagit à un signal ou une sortie de script. |
| `cron` | Planificateur de tâches récurrentes. |
| Lock | Verrou empêchant deux exécutions simultanées du même script. |
| `/var/lock` | Répertoire prévu pour stocker des fichiers de verrouillage temporaires. |
| `flock` | Commande qui prend un verrou sur un fichier avant de lancer une action. |
| Journalisation | Ecriture de traces datées pour prouver l'exécution. |

## Manipulations faites

| Manipulation | Commandes ou actions |
| --- | --- |
| Créer un script | Fichier `.sh`, `chmod +x`, lancement manuel. |
| Gérer les arguments | `$1`, `$@`, valeurs par défaut et aide `--help`. |
| Contrôler les erreurs | Tests `if`, code retour, messages explicites. |
| Planifier une tâche | `crontab -e`, `/etc/cron.d/`, vérification syslog. |
| Sécuriser une tâche cron | `flock -n /var/lock/script.lock /chemin/script.sh` pour éviter les doublons. |
| Produire des traces | Redirection `>>`, `logger`, fichiers dans `/var/log`. |

## Point clé cron : verrou dans `/var/lock`

Une tâche cron ne sait pas si son exécution précédente est encore en cours. Si un script est long, cron peut le relancer et créer deux traitements concurrents.

Exemple :

```cron
0 2 * * * flock -n /var/lock/alpesnet-audit.lock /opt/scripts/audit-comptes.sh >> /var/log/alpesnet/cron-audit.log 2>&1
```

À retenir :

- `flock -n` tente de prendre le verrou sans attendre ;
- si le verrou est déjà pris, le script n'est pas relancé ;
- `/var/lock` sert à ranger ces verrous temporaires ;
- c'est une sécurité utile pour les sauvegardes, audits, archivages et rotations de logs.

## Docs associées

- [Fondamentaux Bash et scripts simples](../../../admin-systemes-linux/it-3/atelier1-bash-fondamentaux.md)
- [Scripts d'administration pratiques](../../../admin-systemes-linux/it-3/scripts-administration-pratiques.md)
- [Planification cron AlpesNet](../../../admin-systemes-linux/it-3/planification-cron-alpesnet.md)
- [Script administration robuste AlpesNet](../../../admin-systemes-linux/it-3/script-administration-robuste-alpesnet.md)
- [Fonctions, arguments et trap Bash](../../../admin-systemes-linux/it-3/fonctions-arguments-trap-bash.md)
- [Carnet de bord](../../../admin-systemes-linux/it-3/carnet-bord-it3.md)
