# Exigences de sauvegarde


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/backup-requirements.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Évolution des exigences PCA/PRA

| Exigence | Source | Statut actuel | Adaptation et preuve |
|---|---|---|---|
| Sauvegarde nocturne | PCA | Mise en œuvre | `backup.sh` archive les exports applicatifs, les volumes Docker, les configurations et la documentation. |
| Copie hebdomadaire séparée | PCA | Partielle | Borg conserve quatre archives hebdomadaires et chiffre le dépôt ; la copie hors de l'hôte reste à prouver. |
| Contrôle quotidien | PCA | Mis en œuvre | `check-backup.sh`, la crontab de 08 h 15, `last-run.status` et les journaux assurent le contrôle. |
| Reprise de l'authentification | PRA | Partielle | Les LDIF et volumes OpenLDAP sont sauvegardés et extractibles ; le démarrage d'un LDAP restauré reste à chronométrer. |
| Reprise des fichiers | PRA | Mise en œuvre pour les données | Un document du volume `samba_share` a été restauré et comparé avec SHA-256 et `cmp=0`. |
| Reprise de la messagerie | PRA | Partielle | Le volume Dovecot a été extrait et les Maildir retrouvés ; la réinjection et le test IMAP restent à réaliser. |
| Test après restauration | PCA/PRA | Partiel | Les fichiers et volumes ont été contrôlés ; les tests fonctionnels complets LDAP, SMB et IMAP restent à chronométrer. |
| Reprise TLS | PRA | Partielle | La racine Campus CA est versionnée et les procédures existent ; les clés privées et certificats actifs doivent venir du coffre protégé ou être réémis. |
| Reprise de la supervision | PCA/PRA | Partielle | Les tableaux de bord Kibana sont exportés ; la restauration complète du volume Elasticsearch et le réimport restent à exercer. |

## Nouvelles exigences

- sauvegarder les volumes LDAP et produire un export LDIF ;
- sauvegarder les volumes `samba_config`, `samba_state` et `samba_share` ;
- sauvegarder les boîtes du volume `dovecot_mail` ;
- exporter la base MariaDB de Roundcube ;
- conserver les fichiers Compose, Dockerfiles, scripts et configurations ;
- conserver la documentation, le PCA, le PRA et l'historique Git ;
- conserver la racine publique Campus CA, le registre des certificats et les
  procédures de renouvellement ;
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
  chiffré hors Git ;
- conserver l'export des tableaux de bord Kibana et, si nécessaire, les volumes
  Elasticsearch/Filebeat ;
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
- vérifier automatiquement chaque sauvegarde ;
- tester régulièrement les restaurations dans un environnement isolé ;
- conserver au moins une copie hors de l'hôte Docker principal.

La mise en œuvre, l'extraction de fichiers et de volumes ainsi que
l'automatisation ont été vérifiées. Le démarrage complet d'un service restauré
et la mesure réelle du délai de reprise restent à effectuer. Une sauvegarde
n'est pas considérée comme totalement validée uniquement parce qu'un fichier
d'archive existe.
