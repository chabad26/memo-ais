# Glossaire Intégration distribuée on-premise — Itération 5

## Sujet

Sauvegarde, contrôle et restauration de l'infrastructure avec BorgBackup.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| BorgBackup | Outil de sauvegarde chiffrée avec déduplication. |
| Dépôt Borg | Emplacement qui contient les archives de sauvegarde. |
| Archive | Point de sauvegarde identifié par un nom et une date. |
| Déduplication | Conservation unique des blocs identiques entre archives. |
| Rétention | Règle qui définit quelles archives sont conservées ou supprimées. |
| `borg check` | Contrôle de l'intégrité d'un dépôt ou d'une archive. |
| RPO | Perte de données maximale acceptable après un incident. |
| RTO | Temps maximal accepté avant le retour du service. |
| `flock` | Verrou qui empêche deux sauvegardes de s'exécuter simultanément. |
| Restauration de test | Récupération contrôlée de données pour vérifier que la sauvegarde est exploitable. |

## Manipulations faites

| Manipulation | Commande ou action |
| --- | --- |
| Lister les archives | `borg list <depot>` |
| Contrôler l'intégrité | `borg check <depot>` |
| Exécuter la sauvegarde | `~/on-premise/backup/run-backup-cron.sh` |
| Vérifier le dernier état | `cat ~/on-premise/backup/logs/last-run.status` |
| Contrôle quotidien | `~/on-premise/backup/check-backup.sh` |
| Restaurer | Extraire dans un répertoire temporaire, puis comparer les données. |

## Points de vigilance

- Le dépôt et la phrase secrète Borg ne doivent pas être supprimés ou publiés.
- Une archive créée ne prouve pas à elle seule qu'une restauration fonctionne.
- Ne pas utiliser `docker compose down -v` avant les contrôles de persistance.
- Une sauvegarde en erreur ou âgée de plus de 36 heures doit être traitée.
- Les journaux et l'état `SUCCESS` ou `FAILURE` servent de preuve d'exploitation.

## Docs associées

- [Vue d'ensemble de l'itération 5](../../../integration-distribuee-on-premise/it-5/index.md)
- [Définir la stratégie de sauvegarde](../../../integration-distribuee-on-premise/it-5/definir-strategie-sauvegarde.md)
- [Mettre en œuvre la sauvegarde BorgBackup](../../../integration-distribuee-on-premise/it-5/mettre-en-oeuvre-sauvegarde-borg.md)
- [Restaurer une sauvegarde BorgBackup](../../../integration-distribuee-on-premise/it-5/restaurer-sauvegarde-borg.md)
- [Automatiser et contrôler les sauvegardes](../../../integration-distribuee-on-premise/it-5/automatiser-sauvegardes-borg.md)
