# Comment déployer Hyper-V — pas à pas

## Objectif

Déployer l'hyperviseur Microsoft Hyper-V sur un serveur physique et réaliser sa configuration initiale.

!!! question "Problématique"
    Quelle solution de virtualisation répond le mieux aux besoins d'AlpesNet ?

    Hyper-V est pertinent pour AlpesNet si l'entreprise utilise déjà l'écosystème Microsoft et dispose des licences Windows Server adaptées. Il permet de consolider les serveurs, de créer des réseaux virtuels, des points de contrôle, des migrations à chaud et, avec plusieurs hôtes, un cluster hautement disponible.

!!! info "Périmètre de cette procédure"
    Cette fiche décrit l'installation du **rôle Hyper-V sur Windows Server 2022 ou 2025** installé directement sur le serveur physique. Les noms d'interfaces, adresses IP, volumes et chemins sont à adapter au cahier des charges d'AlpesNet.

## Activité 1 — Choisir la solution

### Qu'est-ce qu'Hyper-V ?

Hyper-V est la technologie de virtualisation de Microsoft intégrée à Windows Server. Elle permet de créer et d'administrer des machines virtuelles Windows ou Linux, chacune disposant de processeurs, de mémoire, de disques et de cartes réseau virtuels.

Hyper-V est un **hyperviseur de type 1**. Lorsque le rôle est activé, la couche d'hypervision s'exécute directement sur le matériel. Windows Server fonctionne alors dans la partition racine, qui fournit les services d'administration et l'accès aux périphériques ; Hyper-V ne devient pas pour autant un hyperviseur de type 2.

### Prérequis matériels

| Prérequis | Rôle | Contrôle conseillé |
| --- | --- | --- |
| Processeur 64 bits | Exécuter Windows Server et Hyper-V | Vérifier la documentation du constructeur |
| SLAT | Traduction d'adresses mémoire de second niveau | `systeminfo.exe` |
| Intel VT-x ou AMD-V | Virtualisation assistée par le matériel | Activer dans le BIOS/UEFI |
| VM Monitor Mode Extensions | Exécution de l'hyperviseur | `systeminfo.exe` |
| DEP matériel, bit Intel XD ou AMD NX | Protection de l'exécution mémoire | Activer dans le BIOS/UEFI |
| RAM suffisante | Alimenter l'hôte et toutes les VM | Dimensionner selon le cahier des charges |
| Stockage adapté | Héberger l'OS, les VHDX et les points de contrôle | Vérifier capacité, RAID et performances |
| Interfaces réseau | Séparer gestion et trafic des VM si possible | Inventorier ports, débits et VLAN |

Microsoft indique un minimum de 4 Go de RAM pour Hyper-V, mais cette valeur ne suffit pas à dimensionner une plateforme réelle : il faut additionner la mémoire de l'hôte, celle des VM simultanées et une marge de sécurité.

### Vérifier les prérequis

Dans une console PowerShell ou une invite de commandes ouverte en administrateur :

```powershell
systeminfo.exe
```

Avant l'installation d'Hyper-V, les quatre exigences affichées à la fin du rapport doivent être à `Oui` :

```text
Extensions du mode moniteur d'ordinateur virtuel : Oui
Virtualisation activée dans le microprogramme       : Oui
Traduction d'adresses de second niveau              : Oui
Prévention de l'exécution des données disponible    : Oui
```

!!! note
    Après l'activation d'Hyper-V, `systeminfo` peut simplement indiquer qu'un hyperviseur a été détecté. Les exigences détaillées ne sont alors plus affichées.

### Avantages pour AlpesNet

- intégration avec Windows Server, Active Directory et PowerShell ;
- consolidation de plusieurs services sur moins de serveurs physiques ;
- administration locale avec le Gestionnaire Hyper-V ou distante avec Windows Admin Center ;
- automatisation des tâches par PowerShell ;
- prise en charge de VM Windows et de nombreuses distributions Linux ;
- création de commutateurs virtuels et segmentation par VLAN ;
- points de contrôle avant les opérations d'administration ;
- migration à chaud entre plusieurs hôtes ;
- haute disponibilité avec le clustering de basculement Windows Server ;
- possibilités de réplication et de reprise d'activité.

### Fonctionnalités utiles pour la suite

| Fonction | Utilité pour le projet |
| --- | --- |
| Commutateur virtuel | Relier les VM entre elles et aux réseaux physiques. |
| VHDX | Stocker les systèmes et données des VM dans des disques virtuels. |
| Point de contrôle de production | Créer un état cohérent avant une modification. |
| Mémoire dynamique | Adapter la mémoire de certaines VM selon leur activité. |
| Live Migration | Déplacer une VM en fonctionnement vers un autre hôte. |
| Storage Migration | Déplacer les fichiers d'une VM vers un autre stockage. |
| Failover Clustering | Redémarrer les VM sur un autre nœud après une panne. |
| Hyper-V Replica | Répliquer une VM vers un autre hôte pour la reprise d'activité. |

### Synthèse destinée au responsable

Hyper-V est l'hyperviseur de type 1 intégré à Windows Server. Il s'exécute directement sur le matériel et permet d'héberger plusieurs machines virtuelles isolées sur un même serveur physique. Son déploiement nécessite un processeur 64 bits compatible SLAT, la virtualisation matérielle activée, la protection DEP et suffisamment de mémoire, de stockage et d'interfaces réseau. Pour AlpesNet, il facilite la consolidation des serveurs et s'intègre à l'environnement Microsoft existant. Les VM peuvent être administrées avec une interface graphique ou automatisées avec PowerShell. Les commutateurs virtuels permettront de construire les réseaux de préproduction. Les points de contrôle sécuriseront les modifications ponctuelles, sans remplacer les sauvegardes. Avec un second hôte, la migration à chaud et le clustering pourront réduire les interruptions de service. Hyper-V constitue donc une solution cohérente, évolutive et administrable pour préparer la modernisation d'AlpesNet, sous réserve de valider le dimensionnement et les licences.

## Activité 2 — Déployer l'hyperviseur

## Étape 1 — Préserver l'existant

Avant toute réinstallation ou modification du serveur physique :

- identifier les données et services encore présents ;
- réaliser une sauvegarde indépendante ;
- tester l'accès aux données sauvegardées ;
- relever la configuration RAID, réseau, BIOS/UEFI et les licences ;
- obtenir l'autorisation de réutiliser ou de réinstaller le serveur ;
- prévoir un accès local ou une console distante de secours.

!!! danger "Risque de perte de données"
    L'installation ou la réinstallation de Windows Server peut supprimer les partitions existantes. Ne pas continuer tant que la sauvegarde, le support d'installation et la cible exacte n'ont pas été vérifiés.

## Étape 2 — Préparer le BIOS/UEFI

1. Redémarrer le serveur et ouvrir le BIOS/UEFI.
2. Activer **Intel Virtualization Technology / VT-x** ou **AMD-V / SVM**.
3. Activer **Intel XD** ou **AMD NX** pour la prévention d'exécution des données.
4. Activer **VT-d / IOMMU** si les fonctions prévues le nécessitent.
5. Vérifier l'ordre de démarrage et le mode UEFI.
6. Enregistrer les changements et redémarrer.

Les intitulés diffèrent selon le constructeur. Ils doivent être vérifiés dans la documentation du serveur.

## Étape 3 — Préparer Windows Server

Installer Windows Server directement sur le serveur physique, puis réaliser la configuration de base avant d'ajouter Hyper-V.

### Renommer le serveur

Exemple à adapter à la convention AlpesNet :

```powershell
Rename-Computer -NewName "HV-ALPESNET-01" -Restart
```

### Configurer une adresse IP fixe

Commencer par identifier le nom exact de l'interface :

```powershell
Get-NetAdapter
Get-NetIPConfiguration
```

Exemple à adapter au plan d'adressage :

```powershell
New-NetIPAddress `
  -InterfaceAlias "Ethernet" `
  -IPAddress "192.0.2.10" `
  -PrefixLength 24 `
  -DefaultGateway "192.0.2.1"

Set-DnsClientServerAddress `
  -InterfaceAlias "Ethernet" `
  -ServerAddresses "192.0.2.20","192.0.2.21"
```

!!! warning "Adresses d'exemple"
    Le réseau `192.0.2.0/24` est utilisé uniquement comme exemple documentaire. Remplacer ces valeurs par les adresses validées pour AlpesNet avant toute exécution.

### Mettre le serveur à jour

Installer les mises à jour Windows, les pilotes et les firmwares validés par le constructeur, puis redémarrer. Vérifier également la date, l'heure et la synchronisation temporelle.

## Étape 4 — Vérifier le matériel depuis Windows

```powershell
systeminfo.exe
Get-CimInstance Win32_ComputerSystem |
  Select-Object Manufacturer, Model, TotalPhysicalMemory

Get-CimInstance Win32_Processor |
  Select-Object Name, NumberOfCores, NumberOfLogicalProcessors

Get-NetAdapter |
  Select-Object Name, InterfaceDescription, Status, LinkSpeed, MacAddress

Get-Disk
Get-Volume
```

Conserver les résultats utiles dans le dossier de déploiement.

## Étape 5 — Installer le rôle Hyper-V avec PowerShell

Ouvrir PowerShell **en tant qu'administrateur**, puis exécuter :

```powershell
Install-WindowsFeature `
  -Name Hyper-V `
  -IncludeManagementTools `
  -Restart
```

Le serveur redémarre automatiquement. Sur une installation Server Core, l'option ajoute le module PowerShell, mais l'interface graphique Gestionnaire Hyper-V doit être utilisée depuis un autre poste.

### Variante avec le Gestionnaire de serveur

1. Ouvrir **Gestionnaire de serveur**.
2. Sélectionner **Gérer > Ajouter des rôles et fonctionnalités**.
3. Choisir **Installation basée sur un rôle ou une fonctionnalité**.
4. Sélectionner le serveur de destination.
5. Cocher **Hyper-V**, puis ajouter les outils proposés.
6. Vérifier les pages relatives aux commutateurs virtuels, à la migration et aux emplacements par défaut.
7. Autoriser le redémarrage automatique si cela est validé.
8. Lancer l'installation, puis attendre le redémarrage.

## Étape 6 — Vérifier l'installation

```powershell
Get-WindowsFeature Hyper-V
Get-Service vmms, vmcompute
Get-VMHost
```

Résultats attendus :

- le rôle Hyper-V apparaît comme installé ;
- le service `vmms` est en cours d'exécution ;
- `Get-VMHost` retourne les propriétés de l'hôte sans erreur.

## Étape 7 — Préparer le stockage Hyper-V

Séparer si possible le système de l'hôte, les fichiers de configuration des VM et leurs disques virtuels. Créer les dossiers sur les volumes validés, puis définir les chemins par défaut.

```powershell
New-Item -Path "C:\Hyper-V\VM" -ItemType Directory
New-Item -Path "C:\Hyper-V\VHDX" -ItemType Directory

Set-VMHost `
  -VirtualMachinePath "C:\Hyper-V\VM" `
  -VirtualHardDiskPath "C:\Hyper-V\VHDX"
```

Adapter la lettre de lecteur et les chemins au stockage réellement disponible. Ne pas placer les fichiers sur un volume inexistant ou non redondé sans justification.

## Étape 8 — Créer le commutateur virtuel

Hyper-V propose trois types principaux :

| Type | Communication permise | Usage |
| --- | --- | --- |
| Externe | VM, hôte et réseau physique | Accès au réseau AlpesNet |
| Interne | VM et hôte uniquement | Laboratoire avec communication vers l'hôte |
| Privé | VM entre elles uniquement | Réseau totalement isolé de l'hôte |

Identifier d'abord l'interface physique :

```powershell
Get-NetAdapter
```

Créer ensuite un commutateur externe, en adaptant le nom de l'interface :

```powershell
New-VMSwitch `
  -Name "vSwitch-Externe" `
  -NetAdapterName "Ethernet" `
  -AllowManagementOS $true
```

!!! warning "Risque de coupure réseau"
    La création d'un commutateur externe reconfigure l'interface physique et peut interrompre temporairement l'accès distant. Réaliser cette opération depuis la console locale ou une console de gestion hors bande. Vérifier que l'adresse IP de gestion est bien portée par l'interface virtuelle créée pour l'OS de gestion.

Contrôler la configuration :

```powershell
Get-VMSwitch
Get-VMNetworkAdapter -ManagementOS
Get-NetIPConfiguration
```

## Étape 9 — Configurer les premiers réglages

- appliquer les mises à jour de sécurité ;
- utiliser des comptes d'administration nominatifs ;
- ajouter uniquement les administrateurs autorisés au groupe `Hyper-V Administrators` ;
- limiter les flux entrants avec le pare-feu Windows ;
- configurer la supervision et la collecte des journaux ;
- documenter les chemins de stockage et le réseau virtuel ;
- vérifier la stratégie de sauvegarde de l'hôte et des VM ;
- préférer les points de contrôle de production pour les charges compatibles ;
- ne pas activer la migration à chaud ou le clustering avant d'avoir préparé les autres hôtes, l'authentification, les réseaux et le stockage nécessaires.

Exemple d'ajout d'un compte déjà créé au groupe local :

```powershell
Add-LocalGroupMember `
  -Group "Hyper-V Administrators" `
  -Member "ALPESNET\adm-hyperv"
```

## Étape 10 — Vérifier l'accès à l'administration

### Administration locale

1. Ouvrir **Gestionnaire Hyper-V**.
2. Sélectionner **Se connecter au serveur**.
3. Choisir **Ordinateur local**.
4. Vérifier que l'hôte apparaît et qu'aucune erreur de connexion n'est affichée.

### Administration distante

Depuis un poste d'administration autorisé disposant des outils Hyper-V :

1. ouvrir le Gestionnaire Hyper-V ;
2. sélectionner **Se connecter au serveur** ;
3. indiquer le nom DNS de l'hôte ;
4. s'authentifier avec un compte autorisé ;
5. vérifier l'affichage des réseaux, du stockage et des VM.

Un environnement joint au domaine simplifie généralement l'authentification. Dans un groupe de travail, des réglages supplémentaires de confiance, d'identifiants et de pare-feu peuvent être nécessaires.

## Activité 3 — Contrôler le fonctionnement

### Contrôle global

```powershell
Get-ComputerInfo |
  Select-Object CsName, WindowsProductName, WindowsVersion, OsBuildNumber

Get-VMHost |
  Select-Object Name, LogicalProcessorCount, MemoryCapacity,
                VirtualMachinePath, VirtualHardDiskPath

Get-VMSwitch
Get-NetAdapter
Get-Disk
Get-Volume
```

### Récapitulatif du serveur déployé

![Récapitulatif PowerShell du serveur Hyper-V](<../../assets/img/admin-systemes-virtualisation/it-2/récap serveur.png>)

La capture confirme que l'hôte Hyper-V est opérationnel et fournit les informations suivantes :

| Élément contrôlé | Valeur relevée |
| --- | --- |
| Nom de l'hôte | `LABO_CORE` |
| Système | Windows Server 2025 Datacenter, build `26100` |
| Processeurs logiques | 12 |
| Mémoire détectée | Environ 15,8 Gio |
| Chemin des VM | `C:\Hyper-V\VM` |
| Chemin des disques virtuels | `C:\Hyper-V\VHDX` |
| Commutateur virtuel | `vSwitch-Externe`, de type externe |
| Interface physique | Intel Ethernet, lien à 1 Gbit/s |
| Disque physique | Toshiba de 238,47 Go, sain et en ligne |
| Volume système | `C:`, 237,48 Go dont environ 197,64 Go disponibles |

Cette configuration est suffisante pour le laboratoire de préproduction. Elle repose toutefois sur un disque physique unique et stocke les VM sur `C:`. Pour une infrastructure de production, il faudrait prévoir un stockage distinct et redondant, dimensionné selon les performances et la disponibilité attendues.

### Vérification des journaux

Ouvrir l'Observateur d'événements et contrôler notamment :

```text
Journaux des applications et des services
└─ Microsoft
   └─ Windows
      └─ Hyper-V-VMMS
         └─ Admin
```

La présence d'événements doit être analysée selon leur niveau. Une erreur critique non résolue empêche de déclarer la plateforme prête.

### Tests de connectivité

```powershell
Test-NetConnection -ComputerName "PASSERELLE_OU_SERVEUR"
Resolve-DnsName "NOM_DNS_A_TESTER"
```

Remplacer les valeurs symboliques par les cibles du cahier des charges.

## Tableau de validation

| Contrôle | Preuve à conserver | Résultat |
| --- | --- | --- |
| Rôle Hyper-V installé | Sortie de `Get-WindowsFeature Hyper-V` | ☐ Conforme |
| Services actifs | Sortie de `Get-Service vmms, vmcompute` | ☐ Conforme |
| Interface d'administration accessible | Capture du Gestionnaire Hyper-V | ☐ Conforme |
| CPU et RAM détectés | Sortie de `Get-VMHost` | ☐ Conforme |
| Cartes réseau détectées | Sortie de `Get-NetAdapter` | ☐ Conforme |
| vSwitch présent | Sortie de `Get-VMSwitch` | ☐ Conforme |
| Volumes disponibles | Sorties de `Get-Disk` et `Get-Volume` | ☐ Conforme |
| Chemins Hyper-V définis | Propriétés retournées par `Get-VMHost` | ☐ Conforme |
| DNS et passerelle joignables | Résultats des tests réseau | ☐ Conforme |
| Journaux sans erreur bloquante | Capture ou export des événements | ☐ Conforme |

## Documentation officielle

- [Présentation de la virtualisation Hyper-V](https://learn.microsoft.com/fr-fr/windows-server/virtualization/hyper-v/overview)
- [Installer Hyper-V dans Windows Server](https://learn.microsoft.com/fr-fr/windows-server/virtualization/hyper-v/get-started/install-hyper-v)
- [Prérequis matériels d'Hyper-V](https://learn.microsoft.com/fr-fr/windows-server/virtualization/hyper-v/host-hardware-requirements)
- [Créer et configurer un commutateur virtuel](https://learn.microsoft.com/fr-fr/windows-server/virtualization/hyper-v/get-started/create-a-virtual-switch)
- [Présentation de la migration dynamique](https://learn.microsoft.com/fr-fr/windows-server/virtualization/hyper-v/manage/live-migration-overview)
