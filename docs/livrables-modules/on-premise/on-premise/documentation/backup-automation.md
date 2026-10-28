# Automatisation des sauvegardes BorgBackup


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/backup-automation.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Mécanisme retenu

| Élément | Solution |
|---|---|
| Exécution | Cron utilisateur, tous les jours à 02 h 00 |
| Script principal | `backup/backup.sh` |
| Lanceur automatique | `backup/run-backup-cron.sh` |
| Verrou | `flock` sur `/tmp/embedded-infra-borg-backup.lock` |
| Journal d'une sauvegarde | `backup/logs/backup-<date>.log` |
| État de la dernière exécution | `backup/logs/last-run.status` |
| Contrôle quotidien | `backup/check-backup.sh`, tous les jours à 08 h 15 |
| Journaux cron | `backup/logs/cron.log` et `daily-check.log` |

## Installation

```bash
cd ~/on-premise/backup
chmod 700 backup.sh run-backup-cron.sh check-backup.sh
chmod 600 .env

crontab -l > /tmp/crontab.before 2>/dev/null || true
crontab -e
```

Ajouter les deux tâches présentes dans `crontab.example`, puis vérifier :

```bash
crontab -l
```

[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
cron ne peut pas répondre à une demande interactive de phrase secrète.

Les deux tâches ont été installées le 5 août 2026 et vérifiées avec
`crontab -l` : sauvegarde à 02 h 00 et contrôle à 08 h 15.

## Test manuel avant activation

```bash
~/on-premise/backup/run-backup-cron.sh
cat ~/on-premise/backup/logs/last-run.status
~/on-premise/backup/check-backup.sh
echo "Code retour du contrôle : $?"
```

Un contrôle conforme retourne le code `0`. Une sauvegarde en erreur, trop
ancienne, sans archive ou sans marqueur de fin retourne un code non nul.

## Résultat validé

L'exécution manuelle du lanceur automatique a produit :

| Élément | Résultat |
|---|---|
| Archive | `embedded-infra-ubuntu-oliv-2026-08-05T12-55-10` |
| Fichiers | 87 |
| État | `SUCCESS` |
| Code retour | `0` |
| Journal | `backup/logs/backup-2026-08-05T12-55-07.log` |
| Contrôle quotidien | `CONFORME` |

Le contrôle confirme que l'archive est récente et que le journal contient le
marqueur de fin. Les avertissements de checksum OpenLDAP déjà documentés ne
bloquent pas Borg, mais doivent être corrigés avant la production.

## Contrôle quotidien

Chaque matin, l'administrateur consulte :

```bash
cat ~/on-premise/backup/logs/last-run.status
tail -n 30 ~/on-premise/backup/logs/daily-check.log
tail -n 50 "$(find ~/on-premise/backup/logs -name 'backup-*.log' \
  -printf '%T@ %p\n' | sort -nr | head -n 1 | cut -d' ' -f2-)"
```

Il vérifie la valeur `SUCCESS`, le code retour `0`, une archive de moins de
36 heures, le nom de la dernière archive et la ligne `Sauvegarde terminée`.
Une vérification Borg complète reste exécutée par `backup.sh` après chaque
création d'archive.

## Gestion des erreurs

- `backup.sh` s'arrête sur une commande en erreur et remet en route les
  conteneurs mis en pause grâce à son gestionnaire de sortie ;
- `run-backup-cron.sh` enregistre `SUCCESS`, `FAILURE` ou `SKIPPED` ;
- `flock` empêche deux sauvegardes de s'exécuter simultanément ;
- `check-backup.sh` retourne un code non nul lorsque le dernier état est
  incorrect ou trop ancien ;
- les journaux permettent de retrouver la commande fautive et son heure.

En production, le code d'erreur du contrôle doit être relié à la supervision
ou à une alerte électronique. La consultation du journal seule ne remplace pas
une alerte automatique ni les tests périodiques de restauration.
