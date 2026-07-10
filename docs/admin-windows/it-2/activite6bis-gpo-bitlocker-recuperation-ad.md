# Activité 6bis - GPO BitLocker et récupération dans Active Directory

## Objectif de l'activité

Cette activité sert à préparer le chiffrement BitLocker des postes du domaine `corp.local`.

L'objectif est de :

- créer une GPO BitLocker ;
- lier la GPO à l'OU `Ordinateurs` ;
- configurer le stockage des informations de récupération dans AD DS ;
- exiger la sauvegarde de la clé de récupération avant chiffrement ;
- utiliser `XTS-AES 128` pour le labo ;
- activer BitLocker sur `POSTE-01` ;
- vérifier l'état du chiffrement ;
- contrôler la présence de la clé de récupération dans Active Directory.

## Vue d'ensemble

| Élément | Valeur |
| --- | --- |
| Domaine | `corp.local` |
| Contrôleur de domaine | `SRV-AD01` |
| Poste cible | `POSTE-01` |
| OU cible | `OU=Ordinateurs,DC=corp,DC=local` |
| GPO | `GPO-BitLocker` |
| Chiffrement labo | `XTS-AES 128` |
| Preuve poste | `manage-bde -status` |
| Preuve AD | Objet de récupération BitLocker masqué |

!!! danger "Point de vigilance"
    Ne jamais chiffrer un poste sans méthode de récupération. Dans les livrables, masquer la valeur complète de la clé de récupération.

## Étape 1 - Démarrer le journal PowerShell

Sur `SRV-AD01`, ouvrir PowerShell en administrateur.

Créer une trace des commandes :

```powershell
Start-Transcript -Path "C:\Activite6bis-BitLocker.txt"
```

Définir les variables :

```powershell
$DomainDN = "DC=corp,DC=local"
$ComputerOU = "OU=Ordinateurs,$DomainDN"
$GpoName = "GPO-BitLocker"
```

## Étape 2 - Créer GPO-BitLocker

Créer la GPO :

```powershell
New-GPO -Name $GpoName -Comment "Configuration BitLocker avec sauvegarde de récupération dans AD DS"
```

Lier la GPO à l'OU `Ordinateurs` :

```powershell
New-GPLink `
  -Name $GpoName `
  -Target $ComputerOU `
  -LinkEnabled Yes
```

Vérifier :

```powershell
Get-GPInheritance -Target $ComputerOU
```

Point de contrôle :

- `GPO-BitLocker` existe ;
- la GPO est liée à `OU=Ordinateurs`.

## Étape 3 - Configurer BitLocker Drive Encryption

### Méthode A - Console GPMC si disponible

Depuis un poste avec RSAT/GPMC fonctionnel, ouvrir :

```text
gpmc.msc
```

Modifier `GPO-BitLocker`, puis aller dans :

```text
Configuration ordinateur
Stratégies
Modèles d'administration
Composants Windows
Chiffrement de lecteur BitLocker
```

Configurer l'algorithme :

```text
Choisir la méthode de chiffrement de lecteur et la force du chiffrement
```

Valeur attendue pour le labo :

```text
XTS-AES 128 bits
```

Configurer la récupération des lecteurs du système d'exploitation :

```text
Lecteurs du système d'exploitation
Choisir la façon dont les lecteurs du système d'exploitation protégés par BitLocker peuvent être récupérés
```

Activer :

- enregistrer les informations de récupération BitLocker dans AD DS ;
- ne pas activer BitLocker tant que les informations de récupération ne sont pas stockées dans AD DS.

!!! note "Pourquoi lecteurs du système d'exploitation ?"
    `POSTE-01` chiffre le disque `C:`. Les paramètres importants sont donc dans la partie `Lecteurs du système d'exploitation`.

### Méthode B - Configuration PowerShell par valeurs de stratégie

Si GPMC n'est pas disponible, configurer les paramètres principaux dans la GPO avec `Set-GPRegistryValue`.

Définir `XTS-AES 128` pour les lecteurs du système d'exploitation :

```powershell
Set-GPRegistryValue `
  -Name $GpoName `
  -Key "HKLM\Software\Policies\Microsoft\FVE" `
  -ValueName "EncryptionMethodWithXtsOs" `
  -Type DWord `
  -Value 6
```

Activer la stratégie de récupération pour le disque système :

```powershell
Set-GPRegistryValue -Name $GpoName -Key "HKLM\Software\Policies\Microsoft\FVE" -ValueName "OSRecovery" -Type DWord -Value 1
Set-GPRegistryValue -Name $GpoName -Key "HKLM\Software\Policies\Microsoft\FVE" -ValueName "OSRecoveryPassword" -Type DWord -Value 2
Set-GPRegistryValue -Name $GpoName -Key "HKLM\Software\Policies\Microsoft\FVE" -ValueName "OSActiveDirectoryBackup" -Type DWord -Value 1
Set-GPRegistryValue -Name $GpoName -Key "HKLM\Software\Policies\Microsoft\FVE" -ValueName "OSActiveDirectoryInfoToStore" -Type DWord -Value 1
Set-GPRegistryValue -Name $GpoName -Key "HKLM\Software\Policies\Microsoft\FVE" -ValueName "OSRequireActiveDirectoryBackup" -Type DWord -Value 1
```

Vérifier les paramètres :

```powershell
Get-GPRegistryValue -Name $GpoName -Key "HKLM\Software\Policies\Microsoft\FVE"
```

Valeur utile :

| Valeur | Signification |
| --- | --- |
| `EncryptionMethodWithXtsOs = 6` | XTS-AES 128 pour le disque système |
| `OSActiveDirectoryBackup = 1` | Sauvegarde AD DS activée |
| `OSRequireActiveDirectoryBackup = 1` | Sauvegarde AD exigée avant chiffrement |

## Étape 4 - Préparer POSTE-01

Sur `POSTE-01`, vérifier que le poste est bien dans le domaine et dans le bon réseau :

```powershell
whoami
ipconfig /all
nslookup corp.local
```

Vérifier le TPM :

```powershell
Get-Tpm
```

Résultat attendu :

```text
TpmPresent : True
TpmReady   : True
```

!!! warning "TPM requis"
    Pour un Windows 11 en VM, le TPM virtuel doit être actif. Sans TPM prêt, BitLocker peut demander une autre méthode de protection, moins adaptée au labo.

## Étape 5 - Appliquer la GPO sur POSTE-01

Sur `POSTE-01`, PowerShell en administrateur :

```powershell
gpupdate /force
```

Vérifier que la GPO apparaît dans le résultat :

```powershell
gpresult /r
```

Option rapport HTML :

```powershell
gpresult /h C:\Activite6bis-gpresult-bitlocker.html
```

## Étape 6 - Activer BitLocker avec sauvegarde de récupération

Sur `POSTE-01`, ouvrir PowerShell en administrateur.

Ajouter un protecteur de récupération :

```powershell
Add-BitLockerKeyProtector `
  -MountPoint "C:" `
  -RecoveryPasswordProtector
```

Récupérer l'identifiant du protecteur :

```powershell
$RecoveryProtector = (Get-BitLockerVolume -MountPoint "C:").KeyProtector |
  Where-Object KeyProtectorType -eq "RecoveryPassword" |
  Select-Object -First 1
```

Sauvegarder le protecteur dans AD DS :

```powershell
Backup-BitLockerKeyProtector `
  -MountPoint "C:" `
  -KeyProtectorId $RecoveryProtector.KeyProtectorId
```

Activer BitLocker en `XTS-AES 128` :

```powershell
Enable-BitLocker `
  -MountPoint "C:" `
  -EncryptionMethod XtsAes128 `
  -UsedSpaceOnly `
  -TpmProtector
```

!!! note "UsedSpaceOnly"
    Pour un labo, `-UsedSpaceOnly` accélère fortement le chiffrement. En production, le choix dépend de la politique de sécurité.

Redémarrer si demandé :

```powershell
Restart-Computer
```

## Étape 7 - Vérifier manage-bde -status

Sur `POSTE-01` :

```powershell
manage-bde -status C:
```

Points attendus :

- lecteur `C:` protégé par BitLocker ;
- méthode de chiffrement en `XTS-AES 128` ;
- pourcentage de chiffrement en cours ou terminé ;
- état de protection activé après finalisation.

Autre vérification PowerShell :

```powershell
Get-BitLockerVolume -MountPoint "C:" |
  Select-Object MountPoint, VolumeStatus, ProtectionStatus, EncryptionMethod
```

## Étape 8 - Vérifier la clé de récupération dans AD

### Méthode A - ADUC si disponible

Depuis un poste avec RSAT :

```text
dsa.msc
```

Activer :

```text
Affichage
Fonctionnalités avancées
```

Aller sur l'objet ordinateur :

```text
corp.local
Ordinateurs
POSTE-01
```

Ouvrir les propriétés de `POSTE-01`, puis vérifier l'onglet :

```text
Récupération BitLocker
```

Preuve attendue :

- un objet de récupération existe ;
- la valeur de la clé est masquée dans la capture.

### Méthode B - Vérification PowerShell depuis SRV-AD01

Si ADUC n'est pas disponible, vérifier depuis `SRV-AD01` :

```powershell
$Computer = Get-ADComputer "POSTE-01"

Get-ADObject `
  -Filter 'objectClass -eq "msFVE-RecoveryInformation"' `
  -SearchBase $Computer.DistinguishedName `
  -Properties msFVE-RecoveryGuid, whenCreated |
  Select-Object Name, msFVE-RecoveryGuid, whenCreated
```

!!! danger "Masquer les clés"
    Ne jamais afficher ou capturer `msFVE-RecoveryPassword` en clair dans un livrable. Pour une preuve, le nom de l'objet, le GUID et la date suffisent.

## Dépannage rapide

### La GPO ne s'applique pas

Vérifier que `POSTE-01` est bien dans `OU=Ordinateurs` :

```powershell
Get-ADComputer "POSTE-01" -Properties DistinguishedName |
  Select-Object Name, DistinguishedName
```

Vérifier côté poste :

```powershell
gpresult /r
```

### BitLocker refuse de démarrer

Vérifier le TPM :

```powershell
Get-Tpm
```

Vérifier l'édition Windows :

```powershell
Get-ComputerInfo | Select-Object WindowsProductName
```

BitLocker nécessite une édition compatible, comme Windows 11 Pro, Enterprise ou Education.

### La clé n'apparaît pas dans AD

Vérifier que le poste voit le domaine :

```powershell
nltest /dsgetdc:corp.local
nslookup corp.local
```

Relancer la sauvegarde du protecteur depuis `POSTE-01` :

```powershell
$RecoveryProtector = (Get-BitLockerVolume -MountPoint "C:").KeyProtector |
  Where-Object KeyProtectorType -eq "RecoveryPassword" |
  Select-Object -First 1

Backup-BitLockerKeyProtector `
  -MountPoint "C:" `
  -KeyProtectorId $RecoveryProtector.KeyProtectorId
```

Puis revérifier dans AD.

## Livrables et preuves attendues

Convention de nommage :

```text
[Nom]-[Prénom]-[Site]-Activite6bis-[NomLivrable]
```

Livrables :

| Livrable | Preuve attendue | Exemple |
| --- | --- | --- |
| Capture GPO-BitLocker | Paramètres BitLocker ou valeurs de stratégie | `Nom-Prenom-Site-Activite6bis-GPO-BitLocker.png` |
| Sortie manage-bde | `manage-bde -status C:` | `Nom-Prenom-Site-Activite6bis-manage-bde.txt` |
| Capture clé dans AD | Objet de récupération BitLocker, clé masquée | `Nom-Prenom-Site-Activite6bis-RecoveryAD.png` |
| Rapport gpresult | GPO appliquée sur `POSTE-01` | `Nom-Prenom-Site-Activite6bis-gpresult.html` |
| Journal PowerShell | Commandes exécutées | `Nom-Prenom-Site-Activite6bis-JournalCommandes.txt` |

## Exemples de preuves

État BitLocker sur `POSTE-01` :

![BitLocker OK](<../../assets/img/admin-windows/it-2/bitlocker OK.png>)

Informations de récupération vues depuis `SRV-AD01` :

![BitLocker vu par le serveur](<../../assets/img/admin-windows/it-2/bitlocker vue par le SRV.png>)

Protecteur de récupération BitLocker sur `POSTE-01` :

![Code BitLocker POSTE-01](<../../assets/img/admin-windows/it-2/codebitlockervmposte01.png>)

!!! danger "Masquage obligatoire"
    Si une capture affiche une clé de récupération complète, masquer la valeur avant remise du livrable. Le formateur doit voir que la récupération existe, pas la clé en clair.

## Checklist finale

- [ ] `GPO-BitLocker` créée.
- [ ] GPO liée à `OU=Ordinateurs`.
- [ ] BitLocker Drive Encryption configuré.
- [ ] Sauvegarde AD DS activée.
- [ ] Sauvegarde AD exigée avant chiffrement.
- [ ] `XTS-AES 128` choisi pour le labo.
- [ ] `gpupdate /force` exécuté sur `POSTE-01`.
- [ ] BitLocker activé sur `POSTE-01`.
- [ ] `manage-bde -status C:` vérifié.
- [ ] Récupération BitLocker visible dans AD.
- [ ] Clé masquée dans les livrables.

## Références

- Microsoft Learn - BitLocker : <https://learn.microsoft.com/windows/security/operating-system-security/data-protection/bitlocker/>
- Microsoft Learn - BitLocker recovery overview : <https://learn.microsoft.com/windows/security/operating-system-security/data-protection/bitlocker/recovery-overview>
