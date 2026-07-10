# Activité 1 - Installer LABO, Windows Admin Center, Hyper-V et créer SRV-AD01

## Objectif de l'activité

Cette activité sert à préparer la plateforme Windows du module.

Le serveur **LABO** est installé en **Windows Server Core**. Comme il n'a pas d'interface graphique locale, l'administration se fera principalement avec **Windows Admin Center** depuis un navigateur.

À la fin, il faut pouvoir :

- administrer LABO depuis le navigateur du laptop ;
- gérer Hyper-V dans Windows Admin Center ;
- créer ou vérifier la VM `SRV-AD01` ;
- ouvrir la console de la VM depuis Windows Admin Center ;
- installer `SRV-AD01` en **Windows Server Core**.

## Architecture cible

```text
Laptop Windows 11 Pro
Navigateur Edge ou Chrome
        |
        | HTTPS
        v
LABO - Windows Server Core
Windows Admin Center
Hyper-V
        |
        +-- VM SRV-AD01
            Windows Server Core
            Futur contrôleur de domaine
```

## Vue d'ensemble

| Élément | Configuration attendue |
| --- | --- |
| Machine physique | `LABO` |
| OS de LABO | Windows Server Core |
| Rôle de LABO | Hôte Hyper-V et passerelle Windows Admin Center |
| Accès d'administration | Navigateur via Windows Admin Center |
| Port Windows Admin Center | `6516` dans cette feuille |
| Commutateur virtuel | Externe |
| VM | `SRV-AD01` |
| OS de la VM | Windows Server Core |
| CPU VM | 2 vCPU |
| RAM VM | 4 Go |
| Disque VM | 60 Go |

!!! note "Pourquoi Windows Admin Center ?"
    Windows Admin Center permet d'administrer un Windows Server Core depuis une interface web. Il permet aussi de gérer Hyper-V, voir les VM et ouvrir leur console depuis le navigateur.

## Étape 1 - Installer Windows Server Core sur LABO

Installer Windows Server sur la machine **LABO**.

Pendant l'installation :

1. Démarrer sur l'ISO Windows Server.
2. Choisir la langue et le clavier.
3. Sélectionner une édition **Windows Server Core**.
4. Installer le système sur le disque de LABO.
5. Définir le mot de passe administrateur local.
6. Se connecter avec `Administrateur` ou `Administrator` selon la langue.

Point de contrôle :

- LABO démarre en ligne de commande ;
- `sconfig` est disponible ;
- le mot de passe administrateur est connu.

## Étape 2 - Renommer LABO

Dans PowerShell administrateur :

```powershell
Rename-Computer -NewName "LABO-PRENOM" -Restart
```

Après redémarrage :

```powershell
hostname
```

Point de contrôle :

- le nom affiché correspond au nom choisi ;
- le nom est noté dans la fiche d'installation.

## Étape 3 - Donner Internet à LABO via le laptop

Si LABO est relié directement au laptop par câble Ethernet, le laptop peut partager sa connexion Internet.

### Depuis Ubuntu

Sur Ubuntu :

1. Connecter le laptop à Internet en Wi-Fi.
2. Brancher le câble Ethernet entre le laptop et LABO.
3. Ouvrir les paramètres réseau.
4. Aller dans la carte Ethernet.
5. Dans IPv4, choisir **Partagé avec d'autres ordinateurs**.
6. Enregistrer puis réactiver la connexion Ethernet.

Ubuntu donne souvent l'adresse suivante à sa carte Ethernet :

```text
10.42.0.1/24
```

LABO reçoit souvent une adresse du type :

```text
10.42.0.x/24
```

### Depuis Windows 11

Sur Windows 11 :

1. Ouvrir `ncpa.cpl`.
2. Clic droit sur la carte qui a Internet.
3. **Propriétés** > **Partage**.
4. Autoriser le partage vers la carte Ethernet reliée à LABO.

Windows utilise souvent :

```text
192.168.137.1/24
```

### Vérifier côté LABO

Lister les cartes :

```powershell
Get-NetAdapter
```

Mettre la carte Ethernet en DHCP :

```powershell
Set-NetIPInterface -InterfaceAlias "Ethernet" -Dhcp Enabled
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ResetServerAddresses
```

Vérifier :

```powershell
ipconfig /all
ping 1.1.1.1
nslookup microsoft.com
```

## Étape 4 - Configurer LABO

### Fuseau horaire

```powershell
Set-TimeZone -Id "Romance Standard Time"
Get-TimeZone
```

### Bureau distant

```powershell
Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections" -Value 0
Get-NetFirewallRule -Name "RemoteDesktop*" | Enable-NetFirewallRule
```

### Administration distante

Dans `sconfig`, vérifier :

| Option | Action |
| --- | --- |
| `4` | Administration distante activée |
| `7` | Bureau distant activé |
| `8` | Configuration réseau |

Activer PowerShell Remoting :

```powershell
Enable-PSRemoting -Force
```

## Étape 5 - Installer Hyper-V sur LABO

Installer le rôle Hyper-V :

```powershell
Install-WindowsFeature -Name Hyper-V -IncludeManagementTools -Restart
```

Après redémarrage :

```powershell
Get-WindowsFeature -Name Hyper-V
Get-Command -Module Hyper-V
```

Point de contrôle :

- le rôle Hyper-V est installé ;
- les commandes Hyper-V sont disponibles.

## Étape 6 - Installer Windows Admin Center sur LABO

Windows Admin Center peut être installé directement sur **Windows Server Core**.

Créer un dossier :

```powershell
New-Item -ItemType Directory -Path "C:\Install" -Force
Set-Location C:\Install
```

Télécharger l'installateur :

```powershell
$parameters = @{
  Source = "https://aka.ms/WACdownload"
  Destination = ".\WindowsAdminCenter.exe"
}
Start-BitsTransfer @parameters
```

Installer Windows Admin Center sur le port `6516` :

```powershell
Start-Process -FilePath ".\WindowsAdminCenter.exe" -ArgumentList "/VERYSILENT /HTTPSPortNumber=6516" -Wait
```

Démarrer le service si nécessaire :

```powershell
Start-Service -Name WindowsAdminCenter
Get-Service -Name WindowsAdminCenter
```

Autoriser le port dans le pare-feu :

```powershell
New-NetFirewallRule `
  -DisplayName "Windows Admin Center 6516" `
  -Direction Inbound `
  -Protocol TCP `
  -LocalPort 6516 `
  -Action Allow
```

Point de contrôle :

- le service `WindowsAdminCenter` est en cours d'exécution ;
- le port `6516` est autorisé ;
- LABO est joignable depuis le laptop.

!!! tip "Si LABO n'a pas Internet"
    Télécharger `WindowsAdminCenter.exe` depuis le laptop, puis le copier sur LABO par clé USB, partage réseau ou serveur HTTP temporaire.

## Étape 7 - Accéder à Windows Admin Center depuis le navigateur

Depuis le laptop, ouvrir Edge ou Chrome :

```text
https://IP_DU_LABO:6516
```

Exemple :

```text
https://10.42.0.2:6516
```

Le navigateur peut afficher une alerte de certificat. Dans un laboratoire, accepter le certificat auto-signé.

Se connecter avec un compte administrateur local de LABO :

```text
LABO-PRENOM\Administrateur
```

ou :

```text
IP_DU_LABO\Administrateur
```

Point de contrôle :

- l'interface Windows Admin Center s'ouvre ;
- LABO apparaît comme serveur administrable ;
- les outils système sont accessibles.

### Dépannage - impossible d'accéder à Windows Admin Center

Windows Admin Center s'ouvre sur le serveur où il est installé.

Exemples :

| Installation de WAC | URL à ouvrir depuis le laptop |
| --- | --- |
| WAC installé sur LABO | `https://IP_DU_LABO:6516` |
| WAC installé sur SRV-AD01 | `https://IP_DE_SRV_AD01:6516` |

Si le navigateur n'accède pas à WAC, vérifier sur le serveur concerné.

Vérifier l'IP :

```powershell
ipconfig /all
```

Vérifier que le service Windows Admin Center existe et tourne :

```powershell
Get-Service *Admin*Center*
Get-Service | Where-Object {
  $_.Name -like "*Admin*" -or
  $_.DisplayName -like "*Admin Center*" -or
  $_.DisplayName -like "*Windows Admin*"
}
```

Si aucun service n'apparaît, Windows Admin Center n'est probablement pas installé sur ce serveur.

Vérifier aussi la présence des fichiers :

```powershell
Get-ChildItem "C:\Program Files" -Recurse -Filter "*AdminCenter*" -ErrorAction SilentlyContinue
Get-ChildItem "C:\Program Files" -Recurse -Filter "*ServerManagement*" -ErrorAction SilentlyContinue
```

Démarrer le service trouvé si nécessaire. Exemple avec un service dont le nom contient `Admin` :

```powershell
Get-Service | Where-Object {
  $_.Name -like "*Admin*" -or $_.DisplayName -like "*Windows Admin*"
} | Start-Service
```

Vérifier que le port `6516` écoute :

```powershell
netstat -ano | findstr 6516
```

Autoriser le port dans le pare-feu :

```powershell
New-NetFirewallRule `
  -DisplayName "Windows Admin Center 6516" `
  -Direction Inbound `
  -Protocol TCP `
  -LocalPort 6516 `
  -Action Allow
```

Vérifier le profil réseau :

```powershell
Get-NetConnectionProfile
```

Si le profil est `Public`, passer le réseau en privé dans le labo :

```powershell
Set-NetConnectionProfile -InterfaceAlias "Ethernet" -NetworkCategory Private
```

Depuis le laptop, tester le port :

```powershell
Test-NetConnection IP_DU_SERVEUR -Port 6516
```

Si `TcpTestSucceeded` vaut `False`, le problème est réseau, pare-feu, mauvaise IP ou service WAC arrêté.

!!! warning "LABO ou SRV-AD01 ?"
    Si WAC est installé sur LABO, il faut ouvrir `https://IP_DU_LABO:6516`, pas l'IP de `SRV-AD01`. Depuis WAC sur LABO, on ajoute ensuite `SRV-AD01` comme serveur géré.

## Étape 8 - Créer le commutateur virtuel externe

Depuis Windows Admin Center :

1. Ouvrir la connexion vers LABO.
2. Aller dans **Virtual switches** ou **Commutateurs virtuels**.
3. Créer un commutateur de type **External**.
4. Sélectionner la carte réseau physique connectée au réseau.
5. Nommer le commutateur :

```text
vSwitch-Externe
```

En PowerShell, équivalent :

```powershell
Get-NetAdapter
New-VMSwitch -Name "vSwitch-Externe" -NetAdapterName "Ethernet" -AllowManagementOS $true
Get-VMSwitch
```

Point de contrôle :

- le commutateur `vSwitch-Externe` existe ;
- son type est `External`.

!!! warning "Attention réseau"
    La création d'un commutateur externe peut provoquer une coupure réseau courte sur LABO.

## Étape 9 - Préparer l'ISO Windows Server

Créer le dossier ISO :

```powershell
New-Item -ItemType Directory -Path "C:\ISO" -Force
```

Copier l'ISO Windows Server dans :

```text
C:\ISO\WindowsServer.iso
```

Vérifier :

```powershell
Get-ChildItem C:\ISO
```

## Étape 10 - Créer la VM SRV-AD01

La VM peut être créée depuis Windows Admin Center.

Dans Windows Admin Center :

1. Ouvrir LABO.
2. Aller dans **Virtual Machines**.
3. Ouvrir l'onglet **Inventory**.
4. Cliquer sur **Add** > **New**.
5. Configurer la VM :

| Paramètre | Valeur |
| --- | --- |
| Nom | `SRV-AD01` |
| Génération | `2` |
| Processeurs | `2` |
| Mémoire | `4 Go` |
| Disque | `60 Go` |
| Réseau | `vSwitch-Externe` |
| ISO | `C:\ISO\WindowsServer.iso` |

Équivalent PowerShell :

```powershell
New-Item -ItemType Directory -Path "C:\Hyper-V\VMs" -Force
New-Item -ItemType Directory -Path "C:\Hyper-V\VHDX" -Force

New-VM `
  -Name "SRV-AD01" `
  -Generation 2 `
  -MemoryStartupBytes 4GB `
  -NewVHDPath "C:\Hyper-V\VHDX\SRV-AD01.vhdx" `
  -NewVHDSizeBytes 60GB `
  -Path "C:\Hyper-V\VMs" `
  -SwitchName "vSwitch-Externe"

Set-VMProcessor -VMName "SRV-AD01" -Count 2
Set-VMMemory -VMName "SRV-AD01" -DynamicMemoryEnabled $false -StartupBytes 4GB
Add-VMDvdDrive -VMName "SRV-AD01" -Path "C:\ISO\WindowsServer.iso"
```

Point de contrôle :

- `SRV-AD01` apparaît dans Windows Admin Center ;
- CPU, RAM, disque et réseau sont visibles.

## Étape 11 - Ouvrir la console de la VM dans Windows Admin Center

Dans Windows Admin Center :

1. Aller dans **Virtual Machines**.
2. Ouvrir **Inventory**.
3. Sélectionner `SRV-AD01`.
4. Cliquer sur **Start** si la VM est arrêtée.
5. Cliquer sur **Connect**.

Windows Admin Center peut proposer :

- une console web intégrée ;
- ou un fichier RDP à télécharger pour ouvrir la console via VMConnect.

Utiliser les identifiants administrateur de LABO si demandés.

Point de contrôle :

- la console de `SRV-AD01` s'affiche ;
- l'écran d'installation Windows Server est visible.

### Dépannage - la console VM ne reçoit pas le clavier

Si la console de la VM s'affiche dans Windows Admin Center mais ne reçoit pas le clavier :

1. Cliquer une fois dans l'écran noir ou bleu de la VM pour donner le focus.
2. Essayer `Ctrl` + `Alt` + `End` au lieu de `Ctrl` + `Alt` + `Del`.
3. Passer le navigateur en plein écran avec `F11`.
4. Tester avec Microsoft Edge si Chrome pose problème, ou inversement.
5. Désactiver temporairement les extensions navigateur qui capturent le clavier.
6. Vérifier que la fenêtre Windows Admin Center n'est pas ouverte dans un onglet en arrière-plan.
7. Télécharger le fichier RDP proposé par Windows Admin Center si l'option est disponible.

Si le problème vient de la disposition clavier pendant l'installation :

- essayer de passer le clavier en français dans l'installateur ;
- taper le mot de passe dans le champ utilisateur pour vérifier les caractères ;
- éviter les caractères spéciaux complexes dans le mot de passe temporaire d'installation.

!!! tip "Option la plus fiable"
    Si Windows Admin Center propose **Download RDP file**, télécharger le fichier et l'ouvrir avec le client Bureau distant. La saisie clavier est souvent plus fiable qu'avec la console web intégrée.

## Étape 12 - Installer SRV-AD01 en Server Core

Dans la console de la VM :

1. Démarrer sur l'ISO Windows Server.
2. Choisir la langue et le clavier.
3. Sélectionner l'édition **Windows Server Core**.
4. Installer sur le disque de `60 Go`.
5. Définir le mot de passe administrateur local.
6. Laisser la VM redémarrer.
7. Se connecter dans la console Server Core.

Après installation, dans `SRV-AD01` :

```powershell
sconfig
```

Configurer :

| Option | Action |
| --- | --- |
| `2` | Renommer en `SRV-AD01` |
| `8` | Configurer l'adresse IP |
| `7` | Activer Bureau distant si besoin |
| `15` | Revenir à PowerShell |

Point de contrôle :

- `SRV-AD01` démarre en Server Core ;
- la VM est visible dans Windows Admin Center ;
- la console VM reste accessible.

## Dépannage - ISO Windows et fichier autounattend

### ISO Windows Server défectueux

Si la VM reste bloquée au démarrage, consomme peu ou pas de CPU, ou revient toujours au firmware, vérifier l'ISO Windows Server.

Symptômes possibles :

- la VM démarre mais l'installation ne commence pas ;
- CPU à `0 %` après quelques secondes ;
- aucun affichage exploitable dans la console ;
- aucune IP et aucun heartbeat ;
- comportement différent avec un autre ISO.

Bon réflexe :

1. Retélécharger l'ISO depuis une source fiable.
2. Vérifier le hash si disponible.
3. Remplacer l'ISO dans `C:\ISO\WindowsServer.iso`.
4. Redémarrer la VM sur le nouvel ISO.

### Le fichier autounattend.iso n'est pas lu

Windows Setup ne lit pas toujours un fichier `autounattend.xml` placé dans un **second ISO** attaché à la VM.

Le comportement dépend notamment :

- de l'ordre des lecteurs DVD virtuels ;
- du support reconnu par Windows Setup ;
- du moment où le fichier de réponse est recherché ;
- de la structure exacte de l'ISO contenant `autounattend.xml`.

Méthodes plus fiables :

- mettre `autounattend.xml` à la racine d'une clé USB connectée à la VM ;
- intégrer `autounattend.xml` directement à la racine de l'ISO Windows Server ;
- utiliser Windows Admin Center pour ouvrir la console et faire l'installation interactive ;
- préparer un VHDX déjà installé avec `dism` et `bcdboot` si l'installation interactive est impossible.

Dans ce TP, la méthode recommandée reste :

```text
Windows Admin Center > Virtual Machines > SRV-AD01 > Connect
```

Puis installation interactive de Windows Server Core dans la console de la VM.

## Étape 13 - Documenter les paramètres

### Fiche installation LABO

Exemple de preuve pour le serveur LABO :

![Serveur LABO](../../assets/img/admin-windows/it-1/Serveur%20Labo.png)

| Paramètre | Valeur |
| --- | --- |
| Nom LABO |  |
| OS LABO | Windows Server Core |
| IP LABO |  |
| Fuseau horaire | Romance Standard Time |
| Bureau distant | Activé / Désactivé |
| Hyper-V | Installé / Non installé |
| Windows Admin Center | Installé / Non installé |
| URL Windows Admin Center | `https://IP_DU_LABO:6516` |
| Nom du commutateur externe | `vSwitch-Externe` |

### Fiche VM SRV-AD01

Exemple de preuve pour le serveur `SRV-AD01` :

![Serveur SRV-AD01](../../assets/img/admin-windows/it-1/Serveur%20AD.png)

| Paramètre | Valeur |
| --- | --- |
| Nom VM | `SRV-AD01` |
| OS | Windows Server Core |
| Rôle prévu | Futur contrôleur de domaine AD DS / DNS |
| Génération | 2 |
| vCPU | 2 |
| RAM | 4 Go |
| Disque | 60 Go |
| Emplacement VM | `C:\Hyper-V\VMs` |
| Emplacement VHDX | `C:\Hyper-V\VHDX\SRV-AD01.vhdx` |
| Commutateur | `vSwitch-Externe` |
| ISO utilisée | `C:\ISO\WindowsServer.iso` |
| IP SRV-AD01 |  |

## Livrables et preuves attendues

Convention de nommage :

```text
[Nom]-[Prénom]-[Site]-Activite1-[NomLivrable]
```

Livrables :

| Livrable | Preuve attendue |
| --- | --- |
| Fiche installation LABO | Nom, IP, fuseau horaire, Hyper-V, WAC |
| Capture Windows Admin Center | Interface web ouverte sur LABO |
| Capture Hyper-V installé | Rôle Hyper-V ou page Virtual Machines |
| Capture VM SRV-AD01 | VM visible dans Windows Admin Center |
| Capture console SRV-AD01 | Écran d'installation ou Server Core démarré |

## Checklist finale

- [ ] LABO est installé en Windows Server Core.
- [ ] LABO est renommé.
- [ ] LABO a une IP joignable depuis le laptop.
- [ ] Hyper-V est installé.
- [ ] Windows Admin Center est installé.
- [ ] Le navigateur accède à `https://IP_DU_LABO:6516`.
- [ ] Le commutateur `vSwitch-Externe` existe.
- [ ] La VM `SRV-AD01` existe.
- [ ] La console de `SRV-AD01` s'ouvre depuis Windows Admin Center.
- [ ] `SRV-AD01` est installé en Windows Server Core.
- [ ] Les livrables sont prêts.

## Ressources

- Microsoft Learn - Windows Admin Center overview : <https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/overview>
- Microsoft Learn - Install Windows Admin Center : <https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/deploy/install>
- Microsoft Learn - Manage virtual machines with Windows Admin Center : <https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/use/manage-virtual-machines>
