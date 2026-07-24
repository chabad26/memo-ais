# Installer trois Proxmox VE dans Hyper-V

## Objectif

Déployer trois nœuds Proxmox VE virtuels dans l'hôte Hyper-V `LABO_CORE` afin de construire un cluster pédagogique.

!!! warning "Méthode retenue pour Hyper-V"
    Les ISO Proxmox VE 9.1 et 9.2 ne fonctionnent pas correctement dans notre environnement Hyper-V. Les trois nœuds seront donc installés avec **Debian 13 minimal**, puis transformés en serveurs **Proxmox VE 9.2** grâce aux paquets officiels.

## Plan de déploiement

| VM | Nom complet | Adresse | vCPU | RAM fixe | Disque |
|---|---|---:|---:|---:|---:|
| `PVE1` | `pve1.alpesnet.local` | `10.42.0.131/24` | 2 | 3 Gio | 32 Go |
| `PVE2` | `pve2.alpesnet.local` | `10.42.0.132/24` | 2 | 3 Gio | 32 Go |
| `PVE3` | `pve3.alpesnet.local` | `10.42.0.133/24` | 2 | 3 Gio | 32 Go |

Paramètres communs :

- passerelle : `10.42.0.1` ;
- DNS interne : `10.42.0.10` ;
- commutateur Hyper-V : `vSwitch-Externe` ;
- support d'installation : `C:\Iso\debian.iso`.

!!! note "Ressources du laboratoire"
    Les trois nœuds utilisent ensemble 6 vCPU et 9 Gio de RAM. Il pourra être nécessaire d'arrêter temporairement `DC1` et `WEB1` si l'hôte manque de mémoire. Ce dimensionnement convient à un exercice, pas à la production.

## Étape 1 — Vérifier l'ISO et l'hôte

Ouvrir PowerShell en tant qu'administrateur sur `LABO_CORE` :

```powershell
Test-Path "C:\Iso\debian.iso"
Get-Item "C:\Iso\debian.iso" |
  Select-Object Name, Length, LastWriteTime
Get-FileHash "C:\Iso\debian.iso" -Algorithm SHA256

Get-VMSwitch
Get-CimInstance Win32_ComputerSystem |
  Select-Object TotalPhysicalMemory, NumberOfLogicalProcessors
Get-Volume |
  Select-Object DriveLetter, SizeRemaining, Size
```

Le premier résultat doit être `True`. L'image utilisée doit être une ISO d'installation **Debian 13 amd64**.

## Étape 2 — Créer les trois VM Hyper-V

Les commandes suivantes créent les disques et les VM, montent l'ISO Debian et activent la virtualisation imbriquée :

```powershell
$IsoPath = "C:\Iso\debian.iso"
$VmRoot = "C:\Hyper-V\Virtual Hard Disks"
$SwitchName = "vSwitch-Externe"
$VmNames = "PVE1", "PVE2", "PVE3"

New-Item -ItemType Directory -Path $VmRoot -Force

foreach ($VmName in $VmNames) {
    $VhdPath = Join-Path $VmRoot "$VmName.vhdx"

    New-VHD `
      -Path $VhdPath `
      -SizeBytes 32GB `
      -Dynamic

    New-VM `
      -Name $VmName `
      -Generation 2 `
      -MemoryStartupBytes 3GB `
      -VHDPath $VhdPath `
      -SwitchName $SwitchName

    Set-VM `
      -Name $VmName `
      -AutomaticCheckpointsEnabled $false

    Set-VMMemory `
      -VMName $VmName `
      -DynamicMemoryEnabled $false

    Set-VMProcessor `
      -VMName $VmName `
      -Count 2 `
      -ExposeVirtualizationExtensions $true

    Set-VMNetworkAdapter `
      -VMName $VmName `
      -MacAddressSpoofing On

    Add-VMDvdDrive `
      -VMName $VmName `
      -Path $IsoPath

    $Dvd = Get-VMDvdDrive -VMName $VmName

    Set-VMFirmware `
      -VMName $VmName `
      -EnableSecureBoot Off `
      -FirstBootDevice $Dvd
}
```

Les réglages importants sont :

- génération 2 et démarrage UEFI ;
- démarrage sécurisé désactivé ;
- mémoire dynamique désactivée ;
- extensions de virtualisation exposées à Proxmox/KVM ;
- usurpation MAC autorisée pour les futures VM imbriquées.

## Étape 3 — Contrôler la configuration

```powershell
Get-VM -Name PVE1, PVE2, PVE3 |
  Select-Object Name, State, Generation, ProcessorCount, MemoryStartup

Get-VMProcessor -VMName PVE1, PVE2, PVE3 |
  Select-Object VMName, Count, ExposeVirtualizationExtensions

Get-VMNetworkAdapter -VMName PVE1, PVE2, PVE3 |
  Select-Object VMName, SwitchName, MacAddressSpoofing

Get-VMDvdDrive -VMName PVE1, PVE2, PVE3 |
  Select-Object VMName, Path
```

Les VM doivent être connectées à `vSwitch-Externe`, associées à l'ISO Debian et posséder les extensions de virtualisation.

## Étape 4 — Installer Debian 13 sur PVE1

Démarrer `PVE1` depuis Windows Admin Center :

```powershell
Start-VM PVE1
```

Depuis un poste Linux, la console Hyper-V peut être ouverte avec FreeRDP :

```bash
xfreerdp3 \
  /v:10.42.0.2 \
  /u:'LABO_CORE\Administrateur' \
  /vmconnect:ID-DE-LA-VM \
  /cert:ignore
```

L'identifiant peut être obtenu sur l'hôte :

```powershell
(Get-VM PVE1).Id
```

Dans l'installateur Debian :

1. sélectionner **Install** ou **Graphical install** ;
2. choisir le français, la France et le clavier français ;
3. configurer le nom `pve1` et le domaine `alpesnet.local` ;
4. attribuer l'adresse fixe `10.42.0.131/24` ;
5. indiquer la passerelle `10.42.0.1` et le DNS `10.42.0.10` ;
6. définir un mot de passe robuste pour `root` ;
7. créer un utilisateur local, par exemple `oliv` ;
8. utiliser le disque virtuel entier avec le partitionnement assisté ;
9. sélectionner uniquement **serveur SSH** et **utilitaires usuels du système** ;
10. ne pas installer d'environnement de bureau ;
11. terminer l'installation et arrêter la VM.

Retirer ensuite l'ISO et démarrer sur le disque :

```powershell
Stop-VM PVE1
Set-VMDvdDrive -VMName PVE1 -Path $null
$Disk = Get-VMHardDiskDrive -VMName PVE1
Set-VMFirmware -VMName PVE1 -FirstBootDevice $Disk
Start-VM PVE1
```

## Étape 5 — Préparer Debian

Se connecter en SSH :

```bash
ssh oliv@10.42.0.131
su -
```

La connexion SSH directe de `root` est généralement interdite par défaut sur Debian. La commande `su -` permet de passer administrateur avec le mot de passe `root`.

Définir le nom complet :

```bash
hostnamectl set-hostname pve1.alpesnet.local
nano /etc/hosts
```

Contenu à conserver sur chacun des trois nœuds :

```text
127.0.0.1 localhost
10.42.0.131 pve1.alpesnet.local pve1
10.42.0.132 pve2.alpesnet.local pve2
10.42.0.133 pve3.alpesnet.local pve3
```

Vérifier la résolution et Internet :

```bash
hostname --fqdn
getent hosts pve1.alpesnet.local
ping -c 4 10.42.0.1
ping -c 4 download.proxmox.com
```

Le nom complet doit retourner l'adresse réelle du nœud, jamais une adresse de boucle locale.

## Étape 6 — Ajouter le dépôt Proxmox VE 9

Sur Debian :

```bash
apt update
apt full-upgrade -y
apt install -y wget
```

Télécharger la clé officielle :

```bash
wget \
  https://enterprise.proxmox.com/debian/proxmox-archive-keyring-trixie.gpg \
  -O /usr/share/keyrings/proxmox-archive-keyring.gpg
```

Vérifier la clé téléchargée :

```bash
sha256sum /usr/share/keyrings/proxmox-archive-keyring.gpg
```

Somme attendue lors de la rédaction :

```text
136673be77aba35dcce385b28737689ad64fd785a797e57897589aed08db6e45
```

Créer `/etc/apt/sources.list.d/proxmox.sources` :

```text
Types: deb
URIs: http://download.proxmox.com/debian/pve
Suites: trixie
Components: pve-no-subscription
Signed-By: /usr/share/keyrings/proxmox-archive-keyring.gpg
```

Mettre à jour les index :

```bash
apt update
```

## Étape 7 — Installer Proxmox VE

Installer d'abord le noyau Proxmox :

```bash
apt install -y proxmox-default-kernel
reboot
```

Après le redémarrage :

```bash
uname -r
apt install -y proxmox-ve postfix open-iscsi chrony
```

Pendant la configuration de Postfix, sélectionner **Site local uniquement**. Redémarrer ensuite :

```bash
update-grub
reboot
```

Vérifier :

```bash
pveversion
uname -r
systemctl status pveproxy --no-pager
systemctl --failed
```

`pveversion` doit annoncer `pve-manager/9.2...` et le service `pveproxy` doit être actif.

## Étape 8 — Configurer le bridge Proxmox

Identifier le nom de la carte physique virtuelle :

```bash
ip -br link
ip -br address
```

Dans cet exemple, la carte est appelée `eth0`. Adapter le nom si Debian affiche `ens18`, `enp1s0` ou une autre valeur.

Modifier `/etc/network/interfaces` :

```text
auto lo
iface lo inet loopback

iface eth0 inet manual

auto vmbr0
iface vmbr0 inet static
    address 10.42.0.131/24
    gateway 10.42.0.1
    bridge-ports eth0
    bridge-stp off
    bridge-fd 0
```

Appliquer la configuration depuis la console, car une erreur peut couper SSH :

```bash
ifreload -a
ip -br address
ip route
```

L'adresse de gestion doit maintenant appartenir au bridge `vmbr0`.

## Étape 9 — Installer PVE2 et PVE3

Répéter les étapes précédentes avec :

| VM | Nom | Adresse |
|---|---|---|
| `PVE2` | `pve2.alpesnet.local` | `10.42.0.132/24` |
| `PVE3` | `pve3.alpesnet.local` | `10.42.0.133/24` |

La passerelle reste `10.42.0.1`, le DNS reste `10.42.0.10` et le bridge reste `vmbr0`.

## Étape 10 — Vérifier les interfaces Web

Depuis un poste du réseau, ouvrir :

- `https://10.42.0.131:8006` ;
- `https://10.42.0.132:8006` ;
- `https://10.42.0.133:8006`.

L'avertissement de certificat est normal : Proxmox utilise initialement un certificat autosigné.

Se connecter avec :

- utilisateur : `root` ;
- domaine : `Linux PAM standard authentication` ;
- mot de passe : celui défini pendant l'installation de Debian.

## Étape 11 — Vérifier les trois nœuds

Sur chaque nœud :

```bash
ping -c 4 10.42.0.131
ping -c 4 10.42.0.132
ping -c 4 10.42.0.133

getent hosts pve1.alpesnet.local
getent hosts pve2.alpesnet.local
getent hosts pve3.alpesnet.local

pveversion
timedatectl
```

!!! danger "Ne pas créer le cluster trop tôt"
    Terminer le réseau, la résolution des noms et les mises à jour avant de créer le cluster. Les trois nœuds doivent utiliser la même version et avoir une heure synchronisée.

## Validation finale

Depuis Hyper-V :

```powershell
Get-VM -Name PVE1, PVE2, PVE3 |
  Select-Object Name, State, Uptime, CPUUsage, MemoryAssigned

Test-NetConnection 10.42.0.131 -Port 8006
Test-NetConnection 10.42.0.132 -Port 8006
Test-NetConnection 10.42.0.133 -Port 8006
```

La préparation est validée si :

- [ ] les trois VM démarrent sans ISO ;
- [ ] les trois interfaces Web répondent sur le port `8006` ;
- [ ] chaque nœud possède une adresse fixe et un nom unique ;
- [ ] les trois nœuds communiquent entre eux ;
- [ ] les extensions de virtualisation sont visibles ;
- [ ] les trois nœuds utilisent la même version de Proxmox VE.

Le cluster pourra ensuite être créé depuis `PVE1`, puis rejoint par `PVE2` et `PVE3`.
