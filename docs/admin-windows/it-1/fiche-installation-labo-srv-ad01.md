# Fiche d'installation - LABO et SRV-AD01

## Objectif

Cette fiche sert à documenter les deux machines principales de l'itération 1 :

- **LABO** : serveur physique ou hôte Hyper-V ;
- **SRV-AD01** : VM Windows Server destinée à devenir contrôleur de domaine.

Elle permet de garder une trace claire :

- du nom des serveurs ;
- de l'adressage IP ;
- de la configuration DNS ;
- de l'activation du Bureau distant ;
- des rôles installés.

## Informations générales

| Élément | Valeur |
| --- | --- |
| Nom apprenant | HIMBLOT |
| Prénom apprenant | Olivier |
| Site |  |
| Date | 9/07/2026 |
| Activité | Itération 1 - Plateforme Windows et domaine |

## Fiche LABO

### Identité du serveur

| Paramètre | Valeur |
| --- | --- |
| Nom du serveur | labo_core |
| Type | Serveur physique / machine multifonction |
| Système installé | Windows Server Core |
| Rôle principal | Hôte Hyper-V / Windows Admin Center |

### Adressage IP

| Paramètre | Valeur |
| --- | --- |
| Interface réseau | Ethernet |
| Adresse IP | 10.42.0.2 |
| Masque / préfixe CIDR | /24 |
| Passerelle | 10.42.0.1 |
| Mode d'adressage | Statique |

### Configuration DNS

| Paramètre | Valeur |
| --- | --- |
| DNS préféré | 1.1.1.1 |
| DNS auxiliaire | 8.8.8.8 |
| Résolution DNS testée | Oui  |
| Commande de vérification | `ipconfig /all` |

### Accès distant

| Paramètre | Valeur |
| --- | --- |
| Bureau distant activé | Oui |
| PowerShell Remoting activé | Oui |
| Windows Admin Center installé | Oui |
| URL Windows Admin Center | `https://10.42.0.2` |

### Rôles installés

| Rôle | Installé | Preuve / commande |
| --- | --- | --- |
| Hyper-V | Oui / Non | `Get-WindowsFeature -Name Hyper-V` |
| AD DS | Non attendu sur LABO | admin_labo |
| DNS | Non attendu sur LABO | 10.42.0.10 |

## Fiche SRV-AD01

### Identité du serveur

| Paramètre | Valeur |
| --- | --- |
| Nom du serveur | `SRV-AD01` |
| Type | Machine virtuelle Hyper-V |
| Système installé | Windows Server Core |
| Rôle principal | Futur contrôleur de domaine AD DS / DNS |
| Hôte Hyper-V | LABO |

### Paramètres VM

| Paramètre | Valeur |
| --- | --- |
| Génération VM | 2 |
| vCPU | 2 |
| RAM | 4 Go |
| Disque | 60 Go |
| Emplacement VM | C:\Hyper-V\VMs\SRV-AD01 |
| Emplacement VHDX | C:\Hyper-V\VHDX\SRV-AD01.vhdx |
| Commutateur virtuel | `vSwitch-Externe` |

### Adressage IP

| Paramètre | Valeur |
| --- | --- |
| Interface réseau | Ethernet |
| Adresse IP | 10.42.0.10 |
| Masque / préfixe CIDR | /24 |
| Passerelle | 10.42.0.1 |
| Mode d'adressage | Statique |

!!! warning "Important"
    `SRV-AD01` ne doit pas rester en DHCP. Un futur contrôleur de domaine doit utiliser une adresse IP fixe.

### Configuration DNS

| Paramètre | Valeur |
| --- | --- |
| DNS préféré | Adresse IP locale de `SRV-AD01` |
| DNS préféré réel | 10.42.0.10 |
| DNS auxiliaire | / |
| Résolution DNS testée | Oui / Non |
| Commande de vérification | `ipconfig /all` |

!!! warning "DNS critique"
    Le DNS est indispensable au bon fonctionnement d'Active Directory. Pour le futur contrôleur de domaine, le DNS préféré doit pointer vers lui-même.

### Accès distant

| Paramètre | Valeur |
| --- | --- |
| Bureau distant activé | Oui  |
| PowerShell Remoting activé | Oui  |
| Accessible via Windows Admin Center | Oui (via remote) |

### Rôles installés

| Rôle | Installé | Preuve / commande |
| --- | --- | --- |
| Hyper-V | Non attendu sur SRV-AD01 |  |
| AD DS | Oui / Non | `Get-WindowsFeature -Name AD-Domain-Services` |
| DNS | Oui / Non | `Get-WindowsFeature -Name DNS` |

## Commandes de vérification utiles

### Sur LABO

```powershell
hostname
ipconfig /all
Get-WindowsFeature -Name Hyper-V
Get-Service -Name WindowsAdminCenter
```

### Sur SRV-AD01

```powershell
hostname
ipconfig /all
Get-WindowsFeature -Name AD-Domain-Services,DNS
Get-Service DNS
```
