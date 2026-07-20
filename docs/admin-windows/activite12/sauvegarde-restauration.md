# Shadow Copies, sauvegarde et restauration

## Périmètre

| Paramètre | Valeur |
| --- | --- |
| Serveur | `SRV-FIC01` |
| Données | `D:\DATA` |
| Outil de sauvegarde | Windows Server Backup |
| Destination laboratoire | `E:\BACKUP` ou volume `E:` |
| Versions précédentes | Activées sur `D:` avec VSS |
| Tests | Version antérieure, fichier supprimé et dossier supprimé |

## Différence entre VSS et sauvegarde

| Mécanisme | Usage | Limite |
| --- | --- | --- |
| Cliché VSS / version précédente | Revenir rapidement à une version sur le même volume | Ne protège pas contre la perte du disque ou du serveur |
| Windows Server Backup | Restaurer depuis une version enregistrée sur un autre volume | Dépend de la disponibilité du support de sauvegarde |

## Shadow Copies

```powershell
vssadmin list shadowstorage /for=D:
vssadmin list shadows /for=D:

# Configuration de laboratoire si le stockage VSS est absent
vssadmin add shadowstorage /for=D: /on=D: /maxsize=10GB
vssadmin create shadow /for=D:
```

![Cliché VSS créé](../../assets/img/admin-windows/it-3/cliche-instant-ok.png)

**Contexte :** vérifier qu'un point de restauration est disponible pour les versions précédentes du volume `D:`.

![Test de version précédente](../../assets/img/admin-windows/it-3/version-precedente-ok.png)

**Contexte :** valider depuis un poste autorisé qu'une version antérieure peut être ouverte ou copiée. Il est préférable de choisir **Copier** avant **Restaurer** afin d'éviter un écrasement involontaire.

## Sauvegarde Windows Server Backup

```powershell
Get-WindowsFeature Windows-Server-Backup

wbadmin start backup `
  -backupTarget:E: `
  -include:D:\DATA `
  -quiet

wbadmin get versions -backupTarget:E:
wbadmin get items -version:<VERSION> -backupTarget:E:
```

![Sauvegarde ponctuelle réussie](../../assets/img/admin-windows/it-3/backup-once-ok.png)

**Contexte :** démontrer qu'une version de sauvegarde de `D:\DATA` a été créée sur la cible de laboratoire.

## Procédure de restauration contrôlée

1. Qualifier la demande : objet, chemin, date, propriétaire et urgence.
2. Choisir VSS pour une version récente ou WSB pour une suppression/situation plus large.
3. Identifier et consigner la version retenue.
4. Restaurer dans un emplacement alternatif lorsque possible.
5. Vérifier le contenu et les permissions.
6. Obtenir la validation du propriétaire métier.
7. Replacer l'objet en production et consigner le résultat.

![Dossier IT restauré](../../assets/img/admin-windows/it-3/it-dossier-restaure-ok.png)

**Interprétation :** le scénario de suppression puis restauration du dossier IT a abouti. Ce test confirme la restaurabilité, qui est plus importante que le seul statut « sauvegarde réussie ».

!!! warning "Limite du laboratoire"
    Un volume `E:` attaché au même hôte ne protège pas contre la perte totale du serveur ou de l'hôte Hyper-V. En production, ajouter une copie externalisée ou hors ligne selon une stratégie de type 3-2-1.

