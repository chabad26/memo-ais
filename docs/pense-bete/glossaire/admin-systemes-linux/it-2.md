# Glossaire Systèmes Linux - Itération 2

## Sujet

Permissions Linux, ACL, journaux système, rsyslog, logrotate et audit des droits.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Permission POSIX | Droits lecture, écriture, exécution pour propriétaire, groupe et autres. |
| `chmod` | Commande qui modifie les permissions. |
| `chown` | Commande qui modifie propriétaire et groupe. |
| `umask` | Masque qui définit les permissions par défaut des nouveaux fichiers. |
| ACL | Liste de contrôle d'accès plus fine que les permissions POSIX classiques. |
| `getfacl` | Commande qui affiche les ACL. |
| `setfacl` | Commande qui modifie les ACL. |
| Journal | Trace produite par un service ou le système. |
| `journalctl` | Outil de lecture du journal systemd. |
| `rsyslog` | Service de collecte et routage de logs. |
| `logrotate` | Outil de rotation et rétention des fichiers de logs. |

## Manipulations faites

| Manipulation | Commandes ou actions |
| --- | --- |
| Modifier des droits | `chmod`, `chown`, `chgrp`, tests avec plusieurs utilisateurs. |
| Poser une ACL | `setfacl -m`, `setfacl -d`, vérification avec `getfacl`. |
| Lire les logs | `journalctl`, `/var/log/auth.log`, `/var/log/syslog`. |
| Créer une règle rsyslog | Fichier dans `/etc/rsyslog.d/`, redémarrage service. |
| Tester logrotate | Fichier de politique, simulation et rotation forcée. |
| Auditer les permissions | `find`, `ls -l`, `getfacl`, rapport de conformité. |

## Docs associées

- [Synthèse chmod, chown et umask](../../../admin-systemes-linux/it-2/synthese-permissions-chmod-chown-umask.md)
- [ACL Linux sur AlpesNet](../../../admin-systemes-linux/it-2/atelier-acl-alpesnet.md)
- [Logs système et journalctl AlpesNet](../../../admin-systemes-linux/it-2/atelier-logs-journalctl-alpesnet.md)
- [Rsyslog et logrotate SSH AlpesNet](../../../admin-systemes-linux/it-2/atelier-rsyslog-logrotate-alpesnet.md)
- [Audit des permissions AlpesNet](../../../admin-systemes-linux/it-2/atelier-audit-permissions-alpesnet.md)
- [Rapport audit permissions AlpesNet](../../../admin-systemes-linux/it-2/audit-permissions-alpesnet.md)
- [Carnet de bord](../../../admin-systemes-linux/it-2/carnet-bord-it2.md)

