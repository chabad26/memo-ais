# Activité 1 - Installer LABO, Hyper-V et créer SRV-AD01

## Objectif de l'activité

Cette activité sert à préparer la plateforme Windows du module.

À la fin, la machine **LABO** doit être installée, configurée et prête à héberger une VM Windows Server nommée **SRV-AD01**.

La VM `SRV-AD01` sera installée en **Windows Server Core** pour travailler dans une logique plus professionnelle, plus légère et administrable à distance.

## Vue d'ensemble

| Élément | Configuration attendue |
| --- | --- |
| Machine physique | `LABO` |
| OS de LABO | Windows Server |
| Rôle de LABO | Hôte Hyper-V et machine d'administration |
| Nom de LABO | Libre, mais documenté |
| Réseau LABO | IP dans votre range |
| Accès distant | Bureau distant activé |
| Hyperviseur | Hyper-V |
| Commutateur virtuel | Externe |
| VM | `SRV-AD01` |
| OS de la VM | Windows Server Core |
| CPU VM | 2 vCPU |
| RAM VM | 4 Go |
| Disque VM | 60 Go |

!!! note "Choix avancé intégré"
    Dans cette feuille, `SRV-AD01` est installé en **Server Core**. L'administration se fera ensuite depuis `LABO` avec PowerShell, RSAT ou Windows Admin Center.

## Étape 1 - Installer Windows Server sur LABO

Installer Windows Server sur la machine multifonction **LABO**.

Pendant l'installation :

1. Démarrer sur l'ISO Windows Server.
2. Choisir la langue et le clavier.
3. Sélectionner l'édition Windows Server demandée par le formateur.
4. Installer le système sur le disque prévu pour LABO.
5. Définir le mot de passe administrateur local.
6. Se connecter une première fois avec le compte `Administrator`.

Point de contrôle :

- la session Windows Server s'ouvre correctement ;
- le serveur démarre sans erreur ;
- le mot de passe administrateur est connu et stocké dans un endroit autorisé.

## Étape 2 - Renommer la machine LABO

Donner un nom clair à la machine LABO.

Exemples de noms possibles :

```text
LABO-OLIVIER
LABO-ROUEN-01
LABO-[PRENOM]
```

Depuis PowerShell en administrateur :

```powershell
Rename-Computer -NewName "LABO-PRENOM" -Restart
```

Après redémarrage, vérifier le nom :

```powershell
hostname
```

Point de contrôle :

- le nom affiché correspond au nom choisi ;
- le nom est noté dans la fiche d'installation.

## Étape 3 - Donner Internet à LABO via le laptop

Si le PC **LABO** est relié directement au laptop avec un câble Ethernet, le laptop peut partager sa connexion Internet vers LABO.

Dans ce cas, le laptop joue temporairement le rôle de passerelle réseau.

Architecture :

```text
Internet
   |
Wi-Fi du laptop
   |
Laptop
   |
Câble Ethernet
   |
PC LABO
```

### Sur le laptop Ubuntu

1. Connecter le laptop à Internet, par exemple en Wi-Fi.
2. Brancher le câble Ethernet entre le laptop Ubuntu et le PC LABO.
3. Ouvrir les paramètres réseau d'Ubuntu.
4. Aller dans les paramètres de la carte **Ethernet** reliée à LABO.
5. Dans IPv4, choisir la méthode **Partagé avec d'autres ordinateurs**.
6. Enregistrer.
7. Désactiver puis réactiver la connexion Ethernet si nécessaire.

Ubuntu configure généralement automatiquement la carte Ethernet du laptop avec une adresse du type :

```text
10.42.0.1/24
```

LABO recevra normalement une adresse automatiquement par DHCP, par exemple :

```text
10.42.0.x/24
```

### Variante en ligne de commande sur Ubuntu

Identifier les connexions réseau :

```bash
nmcli connection show
```

Identifier les interfaces :

```bash
ip link
```

Configurer la connexion Ethernet en partage. Adapter le nom de connexion si besoin :

```bash
nmcli connection modify "Wired connection 1" ipv4.method shared
nmcli connection down "Wired connection 1"
nmcli connection up "Wired connection 1"
```

Vérifier l'adresse côté Ubuntu :

```bash
ip addr show
```

Point de contrôle côté laptop :

```text
La carte Ethernet reliée à LABO possède une IP, souvent 10.42.0.1/24.
```

### Sur LABO

Sur la machine LABO, configurer la carte réseau en automatique, ou mettre une IP compatible avec le partage de connexion.

Configuration DHCP :

```powershell
Set-NetIPInterface -InterfaceAlias "Ethernet" -Dhcp Enabled
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ResetServerAddresses
```

Configuration manuelle possible :

```powershell
New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 10.42.0.10 -PrefixLength 24 -DefaultGateway 10.42.0.1
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses 1.1.1.1,8.8.8.8
```

Vérifier :

```powershell
ipconfig /all
ping 10.42.0.1
ping 1.1.1.1
nslookup microsoft.com
```

Points de contrôle :

- LABO possède une IP dans le réseau partagé, souvent `10.42.0.0/24` ;
- LABO ping l'adresse Ethernet du laptop, souvent `10.42.0.1` ;
- LABO ping une IP Internet comme `1.1.1.1` ;
- LABO résout un nom DNS avec `nslookup`.

!!! warning "Attention au réseau"
    Si le formateur impose un range précis, il faut utiliser ce range pour le laboratoire. Le partage de connexion Ubuntu utilise souvent `10.42.0.0/24`, ce qui peut être différent du plan d'adressage demandé.

!!! tip "Dépannage rapide"
    Si LABO n'a pas Internet, vérifier d'abord que le laptop Ubuntu a bien Internet, puis que la carte Ethernet est bien en mode `Partagé avec d'autres ordinateurs`. Désactiver/réactiver la connexion Ethernet peut aussi relancer le DHCP.

## Étape 4 - Configurer le réseau, le fuseau horaire et le bureau distant

### Identifier la carte réseau

Lister les interfaces réseau :

```powershell
Get-NetAdapter
```

Noter le nom de l'interface utilisée, par exemple :

```text
Ethernet
```

### Configurer une IP dans votre range

Adapter les valeurs à votre plan d'adressage.

!!! note "Cas du partage Ubuntu"
    Si LABO passe par le laptop Ubuntu pour avoir Internet, garder une IP compatible avec le partage, souvent `10.42.0.x/24` avec la passerelle `10.42.0.1`. Ne pas remplacer cette configuration par un autre range tant que le laptop sert de passerelle.

Exemple :

```powershell
New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 192.168.10.20 -PrefixLength 24 -DefaultGateway 192.168.10.1
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses 192.168.10.1
```

Vérifier :

```powershell
ipconfig /all
ping 192.168.10.1
```

Point de contrôle :

- l'adresse IP est dans votre range ;
- la passerelle répond ;
- la configuration est notée dans la fiche d'installation.

### Configurer le fuseau horaire

Afficher les fuseaux disponibles :

```powershell
Get-TimeZone
```

Configurer le fuseau France métropolitaine :

```powershell
Set-TimeZone -Id "Romance Standard Time"
```

Vérifier :

```powershell
Get-TimeZone
```

### Activer le Bureau distant

Activer l'accès Bureau distant :

```powershell
Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections" -Value 0
Get-NetFirewallRule -Name "RemoteDesktop*" | Enable-NetFirewallRule
```

Vérifier que la règle pare-feu est active :

```powershell
Get-NetFirewallRule -Name "RemoteDesktop*" | Select-Object Name, DisplayName, Enabled
```

Si aucune règle n'est trouvée, rechercher les règles liées au Bureau distant :

```powershell
Get-NetFirewallRule | Where-Object {
  $_.DisplayName -like "*Bureau*" -or $_.DisplayName -like "*Remote*"
} | Select-Object Name, DisplayName, Enabled
```

Sur certains Windows en français, la commande avec `-DisplayGroup "Remote Desktop"` ne fonctionne pas car le groupe affiché est traduit. Le filtre par `Name` est plus fiable.

Point de contrôle :

- le Bureau distant est activé ;
- la règle pare-feu Remote Desktop est autorisée ;
- un test de connexion RDP peut être réalisé depuis un autre poste autorisé.

!!! warning "Sécurité"
    L'accès RDP doit rester limité au réseau du laboratoire. Ne pas exposer le Bureau distant directement sur Internet.

### Cas Windows Server 2025 Core

Sur **Windows Server 2025 sans interface graphique**, utiliser d'abord `sconfig`.

Lancer l'outil :

```powershell
sconfig
```

Actions utiles dans `sconfig` :

| Option | Action |
| --- | --- |
| `2` | Renommer le serveur |
| `7` | Activer le Bureau distant |
| `8` | Configurer le réseau |
| `9` | Régler la date et l'heure |
| `15` | Quitter vers PowerShell |

Pour activer le Bureau distant depuis PowerShell :

```powershell
Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections" -Value 0
Get-NetFirewallRule -Name "RemoteDesktop*" | Enable-NetFirewallRule
```

Si les règles `RemoteDesktop*` ne sont pas trouvées, utiliser les groupes de règles pare-feu :

```powershell
Get-NetFirewallRule | Where-Object {
  $_.DisplayName -like "*Bureau*" -or $_.DisplayName -like "*Remote*"
} | Select-Object Name, DisplayName, Enabled
```

Puis activer les règles trouvées avec leur `Name`, par exemple :

```powershell
Enable-NetFirewallRule -Name "RemoteDesktop-UserMode-In-TCP"
Enable-NetFirewallRule -Name "RemoteDesktop-UserMode-In-UDP"
```

Vérifier que le service RDP écoute bien :

```powershell
Get-Service TermService
Test-NetConnection -ComputerName localhost -Port 3389
```

Depuis le laptop ou un autre poste, tester ensuite une connexion Bureau distant vers l'IP du serveur :

```text
mstsc /v:IP_DU_SERVEUR
```

!!! note "Depuis Ubuntu"
    Depuis un laptop Ubuntu, utiliser un client RDP comme **Remmina**. Renseigner l'adresse IP de LABO ou de `SRV-AD01`, puis se connecter avec le compte administrateur autorisé.

## Étape 5 - Installer le rôle Hyper-V

Installer Hyper-V depuis PowerShell en administrateur :

```powershell
Install-WindowsFeature -Name Hyper-V -IncludeManagementTools -Restart
```

Après redémarrage, vérifier l'installation :

```powershell
Get-WindowsFeature -Name Hyper-V
```

Vérifier aussi que les commandes Hyper-V sont disponibles :

```powershell
Get-Command -Module Hyper-V
```

Point de contrôle :

- le rôle Hyper-V est installé ;
- la console Hyper-V Manager est disponible ;
- une capture d'écran doit être prise pour le livrable.

## Étape 6 - Créer un commutateur virtuel externe

Un commutateur externe permet aux VM de communiquer avec le réseau physique.

Lister les cartes réseau disponibles :

```powershell
Get-NetAdapter
```

Créer le commutateur externe en adaptant le nom de l'interface :

```powershell
New-VMSwitch -Name "vSwitch-Externe" -NetAdapterName "Ethernet" -AllowManagementOS $true
```

Vérifier :

```powershell
Get-VMSwitch
```

Point de contrôle :

- le commutateur `vSwitch-Externe` existe ;
- son type est `External` ;
- l'OS de gestion garde l'accès réseau grâce à `-AllowManagementOS $true`.

!!! warning "Attention réseau"
    La création d'un commutateur externe peut provoquer une courte coupure réseau sur LABO. Il faut éviter de faire cette action pendant une opération critique.

## Étape 7 - Créer la VM SRV-AD01

Avant de créer les dossiers, vérifier les lecteurs disponibles :

```powershell
Get-PSDrive -PSProvider FileSystem
```

Si le lecteur `D:` n'existe pas, utiliser `C:\Hyper-V`.

Créer un dossier de stockage pour les VM :

```powershell
New-Item -ItemType Directory -Path "C:\Hyper-V\VMs" -Force
New-Item -ItemType Directory -Path "C:\Hyper-V\VHDX" -Force
```

!!! note "Avec un lecteur D:"
    Si un second disque existe, il est possible d'utiliser `D:\Hyper-V` à la place de `C:\Hyper-V`. Il faut simplement adapter tous les chemins dans les commandes suivantes.

Définir les chemins dans des variables pour éviter les erreurs :

```powershell
$VMPath = "C:\Hyper-V\VMs"
$VHDXPath = "C:\Hyper-V\VHDX\SRV-AD01.vhdx"
```

Créer la VM :

```powershell
New-VM `
  -Name "SRV-AD01" `
  -Generation 2 `
  -MemoryStartupBytes 4GB `
  -NewVHDPath $VHDXPath `
  -NewVHDSizeBytes 60GB `
  -Path $VMPath `
  -SwitchName "vSwitch-Externe"
```

Configurer les processeurs :

```powershell
Set-VMProcessor -VMName "SRV-AD01" -Count 2
```

Désactiver la mémoire dynamique si le formateur demande une configuration fixe :

```powershell
Set-VMMemory -VMName "SRV-AD01" -DynamicMemoryEnabled $false -StartupBytes 4GB
```

Vérifier la configuration :

```powershell
Get-VM -Name "SRV-AD01"
Get-VMProcessor -VMName "SRV-AD01"
Get-VMHardDiskDrive -VMName "SRV-AD01"
Get-VMNetworkAdapter -VMName "SRV-AD01"
```

Point de contrôle :

- la VM `SRV-AD01` existe ;
- elle possède `2` vCPU ;
- elle possède `4 Go` de RAM ;
- le disque VHDX fait `60 Go` ;
- elle est connectée au commutateur externe.

## Étape 8 - Installer SRV-AD01 en Windows Server Core

### Transférer l'ISO depuis le laptop Ubuntu vers Server Core

Si l'ISO est sur le laptop Ubuntu, la méthode la plus simple est de le partager temporairement en HTTP.

Sur Ubuntu, se placer dans le dossier où se trouve l'ISO :

```bash
cd ~/Téléchargements
```

Lancer un petit serveur web temporaire :

```bash
python3 -m http.server 8000
```

Si le port `8000` est déjà utilisé, choisir un autre port, par exemple :

```bash
python3 -m http.server 8080
```

Trouver l'adresse IP du laptop Ubuntu :

```bash
ip addr
```

Exemple : si le laptop partage Internet à LABO, son IP Ethernet est souvent :

```text
10.42.0.1
```

Sur Windows Server Core, créer le dossier de destination :

```powershell
New-Item -ItemType Directory -Path "C:\ISO" -Force
```

Télécharger l'ISO depuis le serveur Core :

```powershell
Invoke-WebRequest -Uri "http://10.42.0.1:8000/WindowsServer.iso" -OutFile "C:\ISO\WindowsServer.iso"
```

Adapter le nom du fichier ISO selon son vrai nom.

### Dépanner une erreur 404

Une erreur `404 File not found` signifie que le serveur Core arrive bien à contacter Ubuntu, mais que le fichier demandé n'existe pas à cette URL exacte.

Sur Ubuntu, vérifier le nom exact de l'ISO :

```bash
ls -lh
```

Exemple : si le fichier s'appelle :

```text
fr-fr_windows_server_2025_x64_dvd.iso
```

Alors la commande côté Server Core doit utiliser ce nom exact :

```powershell
Invoke-WebRequest -Uri "http://10.42.0.1:8080/fr-fr_windows_server_2025_x64_dvd.iso" -OutFile "C:\ISO\WindowsServer.iso"
```

Autre vérification utile : depuis le laptop Ubuntu, ouvrir dans un navigateur :

```text
http://10.42.0.1:8080/
```

La page doit afficher la liste des fichiers du dossier partagé. Si l'ISO n'apparaît pas, c'est que le serveur HTTP Python n'a pas été lancé dans le bon dossier.

Vérifier que le fichier est présent :

```powershell
Get-ChildItem C:\ISO
```

Quand le transfert est terminé, arrêter le serveur web sur Ubuntu avec `Ctrl+C`.

!!! warning "Sécurité"
    Le serveur HTTP Python partage tout le dossier courant. Il faut donc le lancer uniquement dans le dossier de l'ISO, le temps du transfert, puis l'arrêter.

### Alternative avec SCP

Si OpenSSH Server est installé et démarré sur Windows Server Core, il est possible d'envoyer l'ISO depuis Ubuntu avec `scp`.

Sur Windows Server Core, vérifier le service SSH :

```powershell
Get-Service sshd
```

Depuis Ubuntu :

```bash
scp WindowsServer.iso Administrateur@10.42.0.2:/C:/ISO/WindowsServer.iso
```

Cette méthode est pratique, mais elle demande que SSH soit déjà disponible côté Windows.

Monter l'ISO Windows Server dans la VM :

```powershell
Add-VMDvdDrive -VMName "SRV-AD01" -Path "C:\ISO\WindowsServer.iso"
```

Adapter le chemin de l'ISO selon son emplacement réel. Pour rechercher rapidement les ISO disponibles :

```powershell
Get-ChildItem -Path C:\ -Filter *.iso -Recurse -ErrorAction SilentlyContinue
```

Vérifier le lecteur DVD :

```powershell
Get-VMDvdDrive -VMName "SRV-AD01"
```

Démarrer la VM :

```powershell
Start-VM -Name "SRV-AD01"
```

Ouvrir la console Hyper-V, puis installer Windows Server en choisissant une édition **Server Core**.

Pendant l'installation :

1. Démarrer sur l'ISO.
2. Choisir l'édition Windows Server sans interface graphique, donc **Server Core**.
3. Installer sur le disque de `60 Go`.
4. Définir le mot de passe administrateur local.
5. Se connecter à la console de `SRV-AD01`.

Point de contrôle :

- `SRV-AD01` démarre en console Server Core ;
- l'outil `sconfig` peut être utilisé ;
- le serveur est prêt pour la configuration réseau et le futur rôle Active Directory.

!!! tip "Server Core"
    Server Core consomme moins de ressources, réduit la surface d'attaque et se rapproche des pratiques d'administration serveur. En échange, il demande d'être à l'aise avec PowerShell et l'administration distante.

## Étape 9 - Préparer l'administration distante de SRV-AD01

Sur `SRV-AD01`, ouvrir `sconfig` si nécessaire :

```powershell
sconfig
```

Actions à réaliser dans `sconfig` :

1. Renommer la machine en `SRV-AD01`.
2. Configurer l'adresse IP selon votre range.
3. Configurer le DNS temporaire selon les consignes du laboratoire.
4. Activer l'administration distante.
5. Activer le Bureau distant si demandé.
6. Redémarrer le serveur.

Vérifier le nom :

```powershell
hostname
```

Vérifier la configuration IP :

```powershell
ipconfig /all
```

Depuis LABO, tester la connectivité :

```powershell
ping SRV-AD01
```

Si la résolution DNS n'est pas encore disponible, tester avec l'adresse IP :

```powershell
ping 192.168.10.30
```

Point de contrôle :

- `SRV-AD01` répond au ping selon les règles du laboratoire ;
- son nom, son IP et son rôle futur sont documentés.

## Étape 10 - Documenter tous les paramètres

Compléter une fiche d'installation avec les informations suivantes.

### Fiche installation LABO

| Paramètre | Valeur |
| --- | --- |
| Nom de la machine LABO |  |
| Modèle / numéro de poste |  |
| OS installé | Windows Server |
| Adresse IP |  |
| Masque / préfixe |  |
| Passerelle |  |
| DNS |  |
| Fuseau horaire | Romance Standard Time |
| Bureau distant | Activé / Désactivé |
| Rôle Hyper-V | Installé / Non installé |
| Nom du commutateur externe | `vSwitch-Externe` |

### Fiche VM SRV-AD01

| Paramètre | Valeur |
| --- | --- |
| Nom de la VM | `SRV-AD01` |
| Nom Windows | `SRV-AD01` |
| Rôle prévu | Futur contrôleur de domaine AD DS / DNS |
| OS | Windows Server Core |
| Génération VM | 2 |
| vCPU | 2 |
| RAM | 4 Go |
| Disque | 60 Go |
| Emplacement VM | `D:\Hyper-V\VMs` |
| Emplacement VHDX | `D:\Hyper-V\VHDX\SRV-AD01.vhdx` |
| Commutateur virtuel | `vSwitch-Externe` |
| Adresse IP |  |
| Masque / préfixe |  |
| Passerelle |  |
| DNS temporaire |  |

## Livrables et preuves attendues

Les livrables doivent respecter la convention :

```text
[Nom]-[Prénom]-[Site]-Activite1-[NomLivrable]
```

Livrables attendus :

| Livrable | Preuve attendue | Exemple de nom |
| --- | --- | --- |
| Fiche installation LABO | Document avec nom, IP, fuseau horaire, RDP, Hyper-V | `Nom-Prenom-Site-Activite1-FicheInstallationLABO.pdf` |
| Capture Hyper-V installé | Capture du rôle installé ou de Hyper-V Manager | `Nom-Prenom-Site-Activite1-HyperVInstalle.png` |
| Capture VM SRV-AD01 | Capture de la VM dans Hyper-V avec CPU/RAM/disque visibles | `Nom-Prenom-Site-Activite1-VM-SRV-AD01.png` |

## Checklist finale

- [ ] Windows Server est installé sur LABO.
- [ ] LABO est renommé.
- [ ] LABO possède une IP dans le bon range.
- [ ] Le fuseau horaire est configuré.
- [ ] Le Bureau distant est activé.
- [ ] Hyper-V est installé.
- [ ] Le commutateur virtuel externe est créé.
- [ ] La VM `SRV-AD01` est créée avec `2` vCPU, `4 Go` RAM et `60 Go` disque.
- [ ] `SRV-AD01` est installé en Server Core.
- [ ] Les paramètres LABO et VM sont documentés.
- [ ] Les captures attendues sont prêtes.

## Résumé rapide

Cette activité prépare la base du laboratoire Windows.

`LABO` devient l'hôte Hyper-V et la machine d'administration. `SRV-AD01` est créé en Server Core pour devenir ensuite le serveur Active Directory principal.

La qualité de la documentation est importante : elle permet de retrouver rapidement les noms, IP, chemins VHDX, paramètres VM et preuves d'installation.
