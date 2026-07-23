# Dimensionner et déployer les VM DC1 et WEB1

## Contexte

AlpesNet prépare la migration de ses deux premiers serveurs vers la plateforme Hyper-V :

- `DC1`, futur contrôleur de domaine et serveur DNS ;
- `WEB1`, futur serveur Web.

Le dimensionnement doit garantir le fonctionnement des services sans épuiser les ressources de l'hôte `LABO_CORE`, qui dispose de **12 processeurs logiques**, d'environ **15,8 Gio de RAM** et d'un disque de **238,47 Go**.

!!! question "Problématique"
    Comment attribuer à chaque VM les ressources adaptées à son rôle tout en conservant une réserve suffisante pour Hyper-V et les autres charges ?

## Activité 1 — Concevoir les machines virtuelles

### Préconisations

| VM | Rôle | Système d'exploitation | vCPU | vRAM | Stockage | Interfaces réseau |
|---|---|---|---:|---:|---:|---:|
| `DC1` | Active Directory Domain Services et DNS | Windows Server 2025 Standard, Server Core | 2 | 4 Gio, dynamique de 2 à 6 Gio | 60 Gio en VHDX dynamique | 1 |
| `WEB1` | Serveur Web Apache ou Nginx | Debian 13 stable, installation minimale sans interface graphique | 2 | 2 Gio, dynamique de 1 à 4 Gio | 40 Gio en VHDX dynamique | 1 |

### Justification du dimensionnement

#### DC1

`DC1` reçoit davantage de mémoire, car Active Directory et DNS sont des services critiques qui doivent rester réactifs. Deux vCPU suffisent pour un petit environnement de préproduction. Le disque de 60 Gio laisse de la place au système, aux journaux, aux mises à jour et à la base Active Directory.

L'installation **Server Core** réduit la consommation de ressources et la surface d'attaque. Une version avec interface graphique peut être retenue si le cahier des charges ou le niveau d'autonomie de l'équipe l'exige.

#### WEB1

Un serveur Debian minimal avec Apache ou Nginx consomme peu de ressources. Deux vCPU, 2 Gio de RAM et 40 Gio de stockage constituent une base cohérente pour un site de préproduction. Les performances devront ensuite être mesurées selon le nombre de connexions, le contenu servi et les journaux produits.

### Capacité conservée sur l'hôte

Au démarrage, les deux VM utilisent environ 6 Gio de RAM et 4 vCPU virtuels. L'hôte conserve ainsi de la mémoire pour Windows Server, Hyper-V et les opérations d'administration.

| Ressource | Hôte | Allocation initiale des VM | Observation |
|---|---:|---:|---|
| Processeurs logiques / vCPU | 12 | 4 vCPU | Marge suffisante pour le laboratoire |
| Mémoire | Environ 15,8 Gio | 6 Gio | Conserver une réserve pour l'hôte |
| Stockage disponible relevé | Environ 197,6 Go | 100 Go maximum logique | VHDX dynamiques, espace réel à surveiller |

!!! warning "VHDX dynamique"
    Un disque dynamique n'occupe initialement que l'espace réellement utilisé, mais il peut grandir jusqu'à sa taille maximale. Il faut surveiller l'espace libre de `C:` pour éviter l'arrêt ou la corruption des VM.

## Préparation du déploiement

### Éléments à vérifier

- le rôle Hyper-V est installé et les services sont actifs ;
- le commutateur `vSwitch-Externe` existe ;
- les ISO de Windows Server et Debian proviennent des sites officiels ;
- leur empreinte a été vérifiée ;
- les chemins `C:\Hyper-V\VM` et `C:\Hyper-V\VHDX` existent ;
- les adresses IP, le VLAN et les noms DNS sont validés ;
- l'espace libre est suffisant.

```powershell
Get-VMHost
Get-VMSwitch
Get-Volume -DriveLetter C
Get-ChildItem "C:\ISO"
```

Les commandes suivantes utilisent des chemins d'ISO symboliques. Ils doivent être remplacés par les noms réellement présents sur le serveur.

## Activité 2 — Déployer les machines virtuelles

## Méthode graphique avec le Gestionnaire Hyper-V

Pour chaque VM :

1. ouvrir **Gestionnaire Hyper-V** ;
2. sélectionner l'hôte `LABO_CORE` ;
3. choisir **Nouveau > Machine virtuelle** ;
4. saisir le nom `DC1` ou `WEB1` ;
5. sélectionner **Génération 2** ;
6. attribuer la mémoire de démarrage ;
7. activer la mémoire dynamique si elle convient à la charge ;
8. connecter la VM à `vSwitch-Externe` ;
9. créer le disque VHDX avec la capacité prévue ;
10. sélectionner l'image ISO du système ;
11. vérifier le récapitulatif et terminer ;
12. ajuster le nombre de processeurs et les limites de mémoire dans les paramètres ;
13. démarrer la VM et lancer l'installation.

## Création de DC1 avec PowerShell

Définir d'abord le chemin réel de l'ISO Windows Server :

```powershell
$IsoDc1 = "C:\ISO\Windows-Server-2025.iso"
Test-Path $IsoDc1
```

La commande doit retourner `True` avant de poursuivre.

```powershell
New-VM `
  -Name "DC1" `
  -Generation 2 `
  -MemoryStartupBytes 4GB `
  -NewVHDPath "C:\Hyper-V\VHDX\DC1.vhdx" `
  -NewVHDSizeBytes 60GB `
  -Path "C:\Hyper-V\VM" `
  -SwitchName "vSwitch-Externe"

Set-VMProcessor -VMName "DC1" -Count 2

Set-VMMemory `
  -VMName "DC1" `
  -DynamicMemoryEnabled $true `
  -MinimumBytes 2GB `
  -StartupBytes 4GB `
  -MaximumBytes 6GB

Add-VMDvdDrive -VMName "DC1" -Path $IsoDc1

$Dc1Dvd = Get-VMDvdDrive -VMName "DC1"
Set-VMFirmware -VMName "DC1" -FirstBootDevice $Dc1Dvd
```

## Création de WEB1 avec PowerShell

Définir le chemin réel de l'ISO Debian :

```powershell
$IsoWeb1 = "C:\ISO\debian-13-amd64-netinst.iso"
Test-Path $IsoWeb1
```

Créer ensuite la VM :

```powershell
New-VM `
  -Name "WEB1" `
  -Generation 2 `
  -MemoryStartupBytes 2GB `
  -NewVHDPath "C:\Hyper-V\VHDX\WEB1.vhdx" `
  -NewVHDSizeBytes 40GB `
  -Path "C:\Hyper-V\VM" `
  -SwitchName "vSwitch-Externe"

Set-VMProcessor -VMName "WEB1" -Count 2

Set-VMMemory `
  -VMName "WEB1" `
  -DynamicMemoryEnabled $true `
  -MinimumBytes 1GB `
  -StartupBytes 2GB `
  -MaximumBytes 4GB

Set-VMFirmware `
  -VMName "WEB1" `
  -EnableSecureBoot On `
  -SecureBootTemplate "MicrosoftUEFICertificateAuthority"

Add-VMDvdDrive -VMName "WEB1" -Path $IsoWeb1

$Web1Dvd = Get-VMDvdDrive -VMName "WEB1"
Set-VMFirmware -VMName "WEB1" -FirstBootDevice $Web1Dvd
```

Le modèle `MicrosoftUEFICertificateAuthority` permet à une VM Linux compatible d'utiliser Secure Boot. En cas d'échec de démarrage, vérifier d'abord l'intégrité et la compatibilité de l'ISO avant d'envisager sa désactivation.

## Installer les systèmes d'exploitation

### DC1 — Windows Server

1. démarrer `DC1` et ouvrir sa console ;
2. lancer l'installation de Windows Server 2025 ;
3. choisir l'édition validée, idéalement Server Core ;
4. installer le système sur le disque virtuel de 60 Gio ;
5. définir un mot de passe administrateur robuste ;
6. installer les mises à jour ;
7. renommer le système en `DC1` ;
8. configurer une adresse IP fixe ;
9. vérifier la date, l'heure et le DNS ;
10. installer AD DS et DNS seulement après validation de la configuration de base.

### WEB1 — Debian

1. démarrer `WEB1` et ouvrir sa console ;
2. sélectionner l'installation Debian sans environnement graphique ;
3. configurer le nom `WEB1` et le réseau selon le plan d'adressage ;
4. utiliser le partitionnement guidé adapté au laboratoire ;
5. installer le serveur SSH et les utilitaires système ;
6. redémarrer puis retirer l'ISO ;
7. installer les mises à jour ;
8. installer Apache ou Nginx selon le cahier des charges ;
9. activer le service au démarrage ;
10. tester l'accès HTTP depuis un poste autorisé.

## Démarrer et ouvrir les consoles

```powershell
Start-VM -Name "DC1","WEB1"
vmconnect.exe localhost "DC1"
vmconnect.exe localhost "WEB1"
```

Après l'installation, retirer les ISO du lecteur virtuel afin d'éviter un nouveau démarrage sur l'installateur :

```powershell
Set-VMDvdDrive -VMName "DC1" -Path $null
Set-VMDvdDrive -VMName "WEB1" -Path $null
```

## Activité 3 — Vérifier le fonctionnement

### Contrôler les VM depuis l'hôte

```powershell
Get-VM -Name "DC1","WEB1" |
  Select-Object Name, State, Status, CPUUsage,
                MemoryAssigned, Uptime

Get-VMProcessor -VMName "DC1","WEB1" |
  Select-Object VMName, Count

Get-VMMemory -VMName "DC1","WEB1" |
  Select-Object VMName, DynamicMemoryEnabled,
                Minimum, Startup, Maximum

Get-VMHardDiskDrive -VMName "DC1","WEB1"
Get-VMNetworkAdapter -VMName "DC1","WEB1" |
  Select-Object VMName, SwitchName, Status, IPAddresses
```

### Contrôler DC1 dans Windows

```powershell
hostname
Get-ComputerInfo | Select-Object WindowsProductName, OsVersion
Get-NetIPConfiguration
Get-CimInstance Win32_ComputerSystem |
  Select-Object NumberOfLogicalProcessors, TotalPhysicalMemory
```

### Contrôler WEB1 dans Debian

```bash
hostnamectl
lscpu
free -h
lsblk
ip address
ip route
systemctl --failed
```

Si le service Web est déjà installé :

```bash
systemctl status nginx --no-pager
curl -I http://localhost
```

Remplacer `nginx` par `apache2` si Apache a été choisi.

## Analyse du dimensionnement

### Les ressources sont-elles adaptées ?

Oui pour une infrastructure de préproduction de petite taille. `DC1` dispose de suffisamment de mémoire pour Windows Server, AD DS et DNS. `WEB1` bénéficie d'une configuration légère adaptée à Debian et à un serveur Web peu chargé. Cette conclusion devra être confirmée par des mesures après installation.

### Conséquences d'un sous-dimensionnement

- lenteurs et temps de réponse élevés ;
- pagination mémoire et forte activité disque ;
- échec ou ralentissement des mises à jour ;
- indisponibilité du site Web lors des pics de charge ;
- authentifications et résolutions DNS ralenties ;
- manque d'espace empêchant l'écriture des journaux ou des mises à jour.

### Conséquences d'un surdimensionnement

- ressources immobilisées alors qu'elles pourraient servir à d'autres VM ;
- pression inutile sur la RAM de l'hôte ;
- ordonnancement des vCPU potentiellement moins efficace ;
- VHDX autorisés à grandir au-delà de l'espace physique disponible ;
- augmentation possible des coûts de licences selon les produits utilisés.

### Paramètres à modifier ?

Aucun changement immédiat n'est nécessaire avant les premiers tests. Les allocations devront être réévaluées après observation du processeur, de la mémoire, du stockage et du réseau. Une hausse doit répondre à une saturation mesurée ; une baisse doit être validée sans dégrader le service.

!!! warning "Spécificité d'un contrôleur de domaine"
    Pour une future production, AlpesNet devra conserver au moins deux contrôleurs de domaine sur des hôtes distincts. Un unique `DC1` virtualisé reste un point de défaillance.

## Documentation officielle

- [Microsoft Learn — Créer une machine virtuelle dans Hyper-V](https://learn.microsoft.com/fr-fr/windows-server/virtualization/hyper-v/get-started/create-a-virtual-machine-in-hyper-v)
- [Microsoft Learn — Configuration matérielle requise pour Windows Server](https://learn.microsoft.com/fr-fr/windows-server/get-started/hardware-requirements)
- [Microsoft Learn — Systèmes invités pris en charge par Hyper-V](https://learn.microsoft.com/fr-fr/windows-server/virtualization/hyper-v/supported-windows-guest-operating-systems-for-hyper-v-on-windows)
- [Guide officiel d'installation de Debian stable](https://www.debian.org/releases/stable/amd64/)
