# Preuves de travail - Itération 5 sauvegarde


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/iteration-5-evidence.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.


## Couverture des critères

| Critère | Preuve dans le dépôt | État |
|---|---|---|
| Analyse du PCA et du PRA | `backup-requirements.md`, `PCA.md`, `PRA.md` | Tableau adapté et statuts actualisés |
| Stratégie justifiée | `backup-strategy.md` | Fréquence nocturne, rétention 7/4/6, chiffrement et contrôles documentés |
| Mise en œuvre BorgBackup | `backup/backup.sh`, `.env.example`, `backup-implementation.md` | Dépôt `repokey`, compression LZ4 et archives créées |
| Vérification d'intégrité | `backup.sh`, `check-backup.sh`, `backup-implementation.md` | `borg check` retourne `0` |
| Restauration de données | `restore-procedure.md` | Compose et document Samba revalidés le 6 août depuis l'archive actuelle, avec SHA-256 identiques et `cmp=0` |
| Automatisation | `run-backup-cron.sh`, `check-backup.sh`, `crontab.example`, `backup-automation.md` | Crontab installée et lancement manuel automatisé en `SUCCESS` |
| Scénario d'incident | `backup-strategy-validation.md` | Corruption LDAP, reprise estimée à 1 h 20 |
| Documentation mise à jour | `inventory.md`, `PCA.md`, `PRA.md`, historique Git | Références et limites consignées |

## État technique contrôlé le 6 août 2026

```text
Dernière archive : embedded-infra-ubuntu-oliv-2026-08-05T12-55-10
État de la dernière exécution : SUCCESS
Contrôle quotidien : CONFORME
borg check : code retour 0
Scripts : syntaxe Bash valide, permissions 700
```

Archives présentes dans `/home/oliv/borg-infrastructure-backup` :

```text
embedded-infra-ubuntu-oliv-2026-08-05T12-14-01
embedded-infra-ubuntu-oliv-2026-08-05T12-55-10
```

Le dépôt Borg contient les sauvegardes et reste donc hors de Git. Sa
configuration reproductible, les scripts et les preuves textuelles sont
versionnés.

## Livrables disponibles

- tableau des exigences : `documentation/backup-requirements.md` ;
- stratégie : `documentation/backup-strategy.md` ;
- configuration et dépôt Borg : `backup/` et dépôt local chiffré ;
- scripts : `backup.sh`, `run-backup-cron.sh`, `check-backup.sh` ;
- procédure et résultats de restauration : `restore-procedure.md` ;
- automatisation et journaux : `backup-automation.md`, `backup/logs/` ;
- scénario PCA/PRA : `backup-strategy-validation.md` ;
- documentation générale : `PCA.md`, `PRA.md`, `inventory.md`.

## Limites encore ouvertes

1. La machine était arrêtée aux horaires planifiés du 6 août : cron ne rejoue
   pas une tâche manquée. Le lancement manuel du même wrapper est validé, mais
   une exécution nocturne sans intervention reste à observer sur un hôte actif.
2. La copie chiffrée hors de l'hôte principal n'est pas encore prouvée.
3. Les volumes et fichiers sont extractibles, mais le démarrage complet d'un
   OpenLDAP restauré n'a pas encore été chronométré.
4. Les avertissements de checksum `slapd.d` sont documentés et ne bloquent pas
   Borg, mais doivent être corrigés avant une mise en production.

Ces limites n'annulent pas les restaurations déjà réalisées. Elles empêchent
simplement de présenter la stratégie comme totalement éprouvée en production.

## Commandes de démonstration

```bash
cd ~/on-premise

git log --oneline --all
crontab -l
backup/check-backup.sh

set -a
source backup/.env
set +a
borg list "$BORG_REPO"
borg check "$BORG_REPO"
```

Ne jamais afficher la phrase secrète Borg ni ajouter `backup/.env` à Git.
