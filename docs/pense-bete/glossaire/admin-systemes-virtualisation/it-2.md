# Glossaire Virtualisation — Itération 2

## Sujet

Déploiement d'un hyperviseur Hyper-V, création de VM Windows/Linux, dimensionnement, VHDX, vSwitch, réseau virtuel et points de restauration.

## Termes à retenir

| Terme | Définition simple |
| --- | --- |
| **Hyper-V** | Hyperviseur Microsoft de type 1 intégré à Windows Server. |
| **Rôle Hyper-V** | Fonction Windows Server permettant d'héberger et d'administrer des machines virtuelles. |
| **Hôte Hyper-V** | Serveur physique qui fournit CPU, RAM, stockage et réseau aux VM. |
| **Gestionnaire Hyper-V** | Console graphique utilisée pour créer et administrer les VM. |
| **Windows Admin Center** | Interface web d'administration Windows Server et Hyper-V. |
| **VM Generation 2** | VM moderne utilisant UEFI, Secure Boot et du matériel virtuel récent. |
| **VHDX** | Format de disque virtuel Hyper-V. |
| **VHDX dynamique** | Disque virtuel qui grandit selon l'espace réellement utilisé, jusqu'à une taille maximale. |
| **Mémoire dynamique** | Ajustement automatique de la RAM attribuée à une VM selon ses besoins et les limites définies. |
| **vCPU** | Processeur logique attribué à une VM. |
| **vRAM** | Mémoire attribuée à une VM. |
| **vSwitch** | Commutateur virtuel reliant les cartes réseau des VM au réseau physique ou interne. |
| **vSwitch externe** | Commutateur virtuel lié à une carte physique pour donner accès au réseau réel. |
| **vNIC** | Carte réseau virtuelle attachée à une VM. |
| **Secure Boot** | Fonction UEFI vérifiant que le système démarre depuis un chargeur approuvé. |
| **Point de contrôle / checkpoint** | Instantané temporaire d'une VM avant une modification. |
| **Snapshot** | État temporaire d'une VM ; utile pour retour arrière, mais ce n'est pas une sauvegarde. |
| **ISO** | Image disque utilisée pour installer l'OS invité. |
| **OS invité** | Système installé dans la VM, par exemple Windows Server ou Debian. |
| **Surallocation** | Attribution de trop de ressources virtuelles par rapport aux capacités réelles. |

## Manipulations faites

| Action | Commandes ou contrôles |
| --- | --- |
| Vérifier les prérequis Hyper-V | `systeminfo.exe` |
| Installer Hyper-V | `Install-WindowsFeature -Name Hyper-V -IncludeManagementTools -Restart` |
| Vérifier l'hôte | `Get-WindowsFeature Hyper-V`, `Get-Service vmms,vmcompute`, `Get-VMHost` |
| Préparer les dossiers VM/VHDX | `New-Item -Path "C:\Hyper-V\VM" -ItemType Directory` |
| Créer un vSwitch | `New-VMSwitch -Name "vSwitch-Externe" -NetAdapterName "Ethernet" -AllowManagementOS $true` |
| Lister les vSwitch | `Get-VMSwitch` |
| Créer une VM Windows | `New-VM -Name "DC1" -Generation 2 -MemoryStartupBytes 4GB ...` |
| Créer une VM Linux | `New-VM -Name "WEB1" -Generation 2 -MemoryStartupBytes 2GB ...` |
| Régler les processeurs | `Set-VMProcessor -VMName "DC1" -Count 2` |
| Régler la mémoire dynamique | `Set-VMMemory -VMName "WEB1" -DynamicMemoryEnabled $true ...` |
| Ajouter une ISO | `Add-VMDvdDrive -VMName "WEB1" -Path "C:\ISO\debian.iso"` |
| Choisir le démarrage sur ISO | `Set-VMFirmware -VMName "WEB1" -FirstBootDevice $Web1Dvd` |
| Retirer l'ISO après installation | `Set-VMDvdDrive -VMName "WEB1" -Path $null` |
| Contrôler les VM | `Get-VM`, `Get-VMNetworkAdapter`, `Get-VMHardDiskDrive` |
| Créer un point de contrôle | `Checkpoint-VM -Name "WEB1" -SnapshotName "avant-modification"` |
| Lister les checkpoints | `Get-VMSnapshot -VMName "WEB1"` |

## Repères de dimensionnement

| VM | Rôle | vCPU | RAM | Disque | Remarque |
| --- | --- | ---: | ---: | --- | --- |
| `DC1` | AD DS / DNS | 2 | 4 Gio | VHDX 60 Gio | Service critique, IP stable, DNS maîtrisé |
| `WEB1` | Serveur web Debian | 2 | 2 Gio | VHDX 40 Gio | Charge légère, service HTTP à tester |

## À ne pas confondre

| Notions | Différence essentielle |
| --- | --- |
| Snapshot et sauvegarde | Le snapshot dépend de la VM et du stockage ; la sauvegarde doit être indépendante et restaurable. |
| VHDX dynamique et espace illimité | Le fichier grandit, mais il peut remplir le volume hôte si on ne surveille pas. |
| vSwitch externe et réseau interne | Le vSwitch externe sort vers le réseau physique ; l'interne reste local à l'hôte et aux VM. |
| Démarrer une VM et valider un service | Une VM allumée ne prouve pas que DNS, HTTP ou SSH fonctionne. |

## Docs associées

- [Vue d'ensemble de l'itération 2](../../../admin-systemes-virtualisation/it-2/index.md)
- [Déployer Hyper-V pas à pas](../../../admin-systemes-virtualisation/it-2/comment-deployer-hyper-v.md)
- [Dimensionner et déployer DC1 et WEB1](../../../admin-systemes-virtualisation/it-2/dimensionner-et-deployer-dc1-web1.md)
- [Intégrer WEB1 au domaine et déployer Apache](../../../admin-systemes-virtualisation/it-2/integrer-web1-au-domaine-et-deployer-apache.md)
- [Permettre aux machines virtuelles de communiquer](../../../admin-systemes-virtualisation/it-2/comment-permettre-aux-machines-virtuelles-de-communiquer.md)
- [Sécuriser une opération d'administration](../../../admin-systemes-virtualisation/it-2/comment-securiser-une-operation-administration.md)
