# Activité 3.1 - Création de SRV-FIC01, serveur de fichiers dédié

## Mise en situation

Le serveur de fichiers ne doit pas être hébergé sur le contrôleur de domaine.

`SRV-FIC01` porte les données utilisateurs et prépare les futurs partages `RH`, `IT` et `COMMUN`.

## Objectif de l'activité

Cette activité sert à créer un serveur membre dédié au stockage de fichiers.

L'objectif est de :

- créer la VM `SRV-FIC01` ;
- ajouter un disque système de 60 Go ;
- ajouter un disque données de 40 Go pour `D:` ;
- prévoir un disque `E:` pour la sauvegarde ;
- activer TPM/chiffrement VM si disponible ;
- installer Windows Server ;
- configurer une IP fixe et le DNS vers `SRV-AD01` ;
- joindre le domaine `corp.local` ;
- déplacer l'objet ordinateur dans `OU=Serveurs` ;
- installer le rôle `FS-FileServer` ;
- créer l'arborescence `D:\DATA` ;
- créer des fichiers de test.

## Vue d'ensemble

| Élément | Configuration attendue |
| --- | --- |
| Nom serveur | `SRV-FIC01` |
| Rôle | Serveur de fichiers |
| vCPU | 2 |
| RAM | 4 Go |
| Disque système | 60 Go |
| Disque données | 40 Go, volume `D:` |
| Disque sauvegarde | Volume `E:` prévu |
| Domaine | `corp.local` |
| DNS | IP de `SRV-AD01` |
| OU cible | `OU=Serveurs,DC=corp,DC=local` |
| Rôle Windows | `FS-FileServer` |

!!! warning "Points de vigilance"
    Les données ne doivent pas être placées sur `C:`. Le contrôleur de domaine `SRV-AD01` ne doit pas héberger les partages métiers.

## Étape 1 - Créer la VM SRV-FIC01

Depuis `LABO`, créer une VM avec les paramètres suivants :

| Paramètre | Valeur |
| --- | --- |
| Nom | `SRV-FIC01` |
| Génération | 2 |
| vCPU | 2 |
| RAM | 4 Go |
| Disque système | 60 Go |
| Réseau | Même réseau que `SRV-AD01` |

Exemple PowerShell Hyper-V :

```powershell
New-VM `
  -Name "SRV-FIC01" `
  -Generation 2 `
  -MemoryStartupBytes 4GB `
  -NewVHDPath "C:\Hyper-V\VHDX\SRV-FIC01-OS.vhdx" `
  -NewVHDSizeBytes 60GB `
  -Path "C:\Hyper-V\VMs" `
  -SwitchName "vSwitch-Externe"

Set-VMProcessor -VMName "SRV-FIC01" -Count 2
```

## Étape 2 - Ajouter les disques données et sauvegarde

Créer le disque données de 40 Go :

```powershell
New-VHD `
  -Path "C:\Hyper-V\VHDX\SRV-FIC01-DATA.vhdx" `
  -SizeBytes 40GB `
  -Dynamic

Add-VMHardDiskDrive `
  -VMName "SRV-FIC01" `
  -Path "C:\Hyper-V\VHDX\SRV-FIC01-DATA.vhdx"
```

Prévoir le disque de sauvegarde :

```powershell
New-VHD `
  -Path "C:\Hyper-V\VHDX\SRV-FIC01-BACKUP.vhdx" `
  -SizeBytes 40GB `
  -Dynamic

Add-VMHardDiskDrive `
  -VMName "SRV-FIC01" `
  -Path "C:\Hyper-V\VHDX\SRV-FIC01-BACKUP.vhdx"
```

!!! note "Pourquoi un disque E: ?"
    Le disque `E:` prépare les futures activités de sauvegarde. En production, une sauvegarde ne doit pas rester uniquement sur le même serveur, mais en labo cela permet de manipuler les outils.

## Étape 3 - Activer TPM/chiffrement VM si disponible

Si la plateforme Hyper-V le permet :

```powershell
Set-VMKeyProtector -VMName "SRV-FIC01" -NewLocalKeyProtector
Enable-VMTPM -VMName "SRV-FIC01"
```

Vérifier :

```powershell
Get-VMSecurity -VMName "SRV-FIC01"
```

## Étape 4 - Installer Windows Server

Monter l'ISO Windows Server sur la VM :

```powershell
Set-VMDvdDrive `
  -VMName "SRV-FIC01" `
  -Path "C:\ISO\WindowsServer.iso"
```

Démarrer la VM :

```powershell
Start-VM "SRV-FIC01"
```

Installer Windows Server.

Choix possible :

- Server Core pour rester cohérent avec le lab ;
- Desktop Experience si l'activité nécessite une interface graphique.

## Étape 5 - Renommer le serveur

Sur `SRV-FIC01`, PowerShell en administrateur :

```powershell
Rename-Computer -NewName "SRV-FIC01" -Restart
```

Après redémarrage :

```powershell
hostname
```

## Étape 6 - Initialiser les disques D: et E:

Sur `SRV-FIC01`, afficher les disques :

```powershell
Get-Disk
```

Initialiser le disque de données de 40 Go :

```powershell
Get-Disk |
  Where-Object PartitionStyle -eq "RAW" |
  Sort-Object Number |
  Select-Object -First 1 |
  Initialize-Disk -PartitionStyle GPT -PassThru |
  New-Partition -UseMaximumSize -DriveLetter D |
  Format-Volume -FileSystem NTFS -NewFileSystemLabel "DATA" -Confirm:$false
```

Initialiser le disque de sauvegarde :

```powershell
Get-Disk |
  Where-Object PartitionStyle -eq "RAW" |
  Sort-Object Number |
  Select-Object -First 1 |
  Initialize-Disk -PartitionStyle GPT -PassThru |
  New-Partition -UseMaximumSize -DriveLetter E |
  Format-Volume -FileSystem NTFS -NewFileSystemLabel "BACKUP" -Confirm:$false
```

Vérifier :

```powershell
Get-Volume | Where-Object DriveLetter -in "C","D","E"
```

## Étape 7 - Configurer IP fixe et DNS

Identifier la carte réseau :

```powershell
Get-NetAdapter
```

Configurer une IP fixe dans le range du labo.

Exemple :

```powershell
New-NetIPAddress `
  -InterfaceAlias "Ethernet" `
  -IPAddress 10.42.0.30 `
  -PrefixLength 24 `
  -DefaultGateway 10.42.0.1

Set-DnsClientServerAddress `
  -InterfaceAlias "Ethernet" `
  -ServerAddresses 10.42.0.10
```

Adapter les valeurs :

| Élément | Exemple |
| --- | --- |
| IP `SRV-FIC01` | `10.42.0.30` |
| Passerelle | `10.42.0.1` |
| DNS | `10.42.0.10` |

Vérifier :

```powershell
ipconfig /all
nslookup corp.local
ping SRV-AD01
```

!!! warning "DNS obligatoire"
    Pour joindre le domaine, le DNS du serveur doit pointer vers `SRV-AD01`, pas vers un DNS Internet.

## Étape 8 - Joindre le domaine corp.local

Sur `SRV-FIC01`, PowerShell en administrateur :

```powershell
Add-Computer `
  -DomainName "corp.local" `
  -Credential "CORP\Administrateur" `
  -Restart
```

Après redémarrage :

```powershell
whoami
nltest /dsgetdc:corp.local
```

## Étape 9 - Déplacer SRV-FIC01 dans OU=Serveurs

Sur `SRV-AD01`, PowerShell en administrateur :

```powershell
Get-ADComputer "SRV-FIC01" |
  Move-ADObject -TargetPath "OU=Serveurs,DC=corp,DC=local"
```

Vérifier :

```powershell
Get-ADComputer "SRV-FIC01" -Properties DistinguishedName |
  Select-Object Name, DistinguishedName
```

## Étape 10 - Installer le rôle serveur de fichiers

Sur `SRV-FIC01` :

```powershell
Install-WindowsFeature FS-FileServer -IncludeManagementTools
```

Vérifier :

```powershell
Get-WindowsFeature FS-FileServer
```

Résultat attendu :

```text
Install State : Installed
```

## Étape 11 - Créer l'arborescence de données

Sur `SRV-FIC01` :

```powershell
New-Item -ItemType Directory -Path "D:\DATA" -Force
New-Item -ItemType Directory -Path "D:\DATA\RH" -Force
New-Item -ItemType Directory -Path "D:\DATA\IT" -Force
New-Item -ItemType Directory -Path "D:\DATA\COMMUN" -Force
```

Vérifier :

```powershell
Get-ChildItem "D:\DATA"
```

## Étape 12 - Créer des fichiers de test

Créer un fichier par dossier :

```powershell
"Fichier de test RH" | Out-File "D:\DATA\RH\test-rh.txt"
"Fichier de test IT" | Out-File "D:\DATA\IT\test-it.txt"
"Fichier de test commun" | Out-File "D:\DATA\COMMUN\test-commun.txt"
```

Vérifier :

```powershell
Get-ChildItem "D:\DATA" -Recurse
```

## Dépannage rapide

### SRV-FIC01 ne rejoint pas le domaine

Vérifier :

```powershell
ipconfig /all
nslookup corp.local
nltest /dsgetdc:corp.local
```

Le DNS doit être `10.42.0.10`.

### Le disque D: n'apparaît pas

Vérifier les disques non initialisés :

```powershell
Get-Disk | Where-Object PartitionStyle -eq "RAW"
```

Si aucun disque RAW n'apparaît, vérifier dans Hyper-V que le disque `SRV-FIC01-DATA.vhdx` est bien attaché à la VM.

### Le rôle FS-FileServer ne s'installe pas

Vérifier le nom de la fonctionnalité :

```powershell
Get-WindowsFeature *File*
```

Puis relancer :

```powershell
Install-WindowsFeature FS-FileServer
```

## Livrables et preuves attendues

Convention de nommage conseillée :

```text
[Nom]-[Prénom]-[Site]-Activite31-[NomLivrable]
```

Livrables :

| Livrable | Preuve attendue | Exemple |
| --- | --- | --- |
| Capture VM | `SRV-FIC01` avec CPU/RAM/disques | `Nom-Prenom-Site-Activite31-VM-SRV-FIC01.png` |
| Capture IP/domaine | IP fixe, DNS vers `SRV-AD01`, domaine `corp.local` | `Nom-Prenom-Site-Activite31-IP-Domaine.png` |
| Capture rôle | `FS-FileServer` installé | `Nom-Prenom-Site-Activite31-Role-FS.png` |
| Capture volumes | volumes `D:` et `E:` visibles | `Nom-Prenom-Site-Activite31-Volumes.png` |
| Capture arborescence | `D:\DATA\RH`, `IT`, `COMMUN` | `Nom-Prenom-Site-Activite31-Arborescence.png` |

## Checklist finale

- [ ] VM `SRV-FIC01` créée.
- [ ] 2 vCPU configurés.
- [ ] 4 Go RAM configurés.
- [ ] Disque système 60 Go configuré.
- [ ] Disque données 40 Go ajouté.
- [ ] Disque `E:` prévu pour sauvegarde.
- [ ] TPM/chiffrement VM activé si disponible.
- [ ] Windows Server installé.
- [ ] IP fixe configurée.
- [ ] DNS configuré vers `SRV-AD01`.
- [ ] `SRV-FIC01` joint à `corp.local`.
- [ ] Objet ordinateur déplacé dans `OU=Serveurs`.
- [ ] Rôle `FS-FileServer` installé.
- [ ] `D:\DATA`, `RH`, `IT`, `COMMUN` créés.
- [ ] Fichiers de test créés.

## Références

- Microsoft Learn - SMB File Sharing : <https://learn.microsoft.com/windows-server/storage/file-server/file-server-smb-overview>
- Microsoft Learn - NTFS overview : <https://learn.microsoft.com/windows-server/storage/file-server/ntfs-overview>
