# Activité 2 - Préparer SRV-AD01 pour Active Directory et DNS

## Objectif de l'activité

Cette activité prépare la VM **SRV-AD01** pour devenir le futur contrôleur de domaine.

L'objectif est de configurer correctement :

- le nom de la machine ;
- l'adresse IP fixe ;
- le DNS local ;
- les rôles **Active Directory Domain Services** et **DNS Server** ;
- les outils d'administration.

Cette activité installe les rôles nécessaires. La promotion en contrôleur de domaine et la création du domaine seront réalisées dans l'activité suivante.

## Vue d'ensemble

| Élément | Configuration attendue |
| --- | --- |
| Serveur | `SRV-AD01` |
| OS | Windows Server Core |
| Rôle prévu | Futur contrôleur de domaine |
| Adresse IP | Fixe |
| DNS préféré | Adresse locale de `SRV-AD01` |
| Rôles à installer | AD DS et DNS Server |
| Outils | Outils d'administration inclus |

!!! warning "Point critique"
    Un futur contrôleur de domaine ne doit pas rester en DHCP. Active Directory dépend fortement du DNS et d'une adresse IP stable.

## Étape 1 - Se connecter à SRV-AD01

Depuis la console Windows Admin Center ou une session PowerShell distante, se connecter à `SRV-AD01`.

Si l'administration distante est déjà active :

```powershell
Enter-PSSession -ComputerName IP_DE_SRV_AD01 -Credential Administrateur
```

Vérifier que l'on travaille bien sur la bonne machine :

```powershell
hostname
whoami
```

Point de contrôle :

- la session est ouverte sur `SRV-AD01` ;
- l'utilisateur possède les droits administrateur local.

## Étape 2 - Renommer la machine SRV-AD01

Vérifier le nom actuel :

```powershell
hostname
```

Renommer le serveur :

```powershell
Rename-Computer -NewName "SRV-AD01" -Restart
```

Après redémarrage, vérifier :

```powershell
hostname
```

Point de contrôle :

- le nom affiché est `SRV-AD01` ;
- la machine a redémarré correctement.

## Étape 3 - Identifier la carte réseau

Lister les interfaces :

```powershell
Get-NetAdapter
```

Noter le nom de la carte connectée au réseau du laboratoire.

Exemple :

```text
Ethernet
```

Afficher la configuration actuelle :

```powershell
Get-NetIPConfiguration
```

## Étape 4 - Configurer une IP fixe

Adapter les valeurs au plan d'adressage du laboratoire.

Exemple :

| Paramètre | Exemple |
| --- | --- |
| Interface | `Ethernet` |
| IP SRV-AD01 | `10.42.0.10` |
| Préfixe | `24` |
| Passerelle | `10.42.0.1` |
| DNS | `10.42.0.10` |

Supprimer une ancienne configuration IPv4 si nécessaire :

```powershell
Get-NetIPAddress -InterfaceAlias "Ethernet" -AddressFamily IPv4 |
  Remove-NetIPAddress -Confirm:$false
```

Créer l'adresse IP fixe :

```powershell
New-NetIPAddress `
  -InterfaceAlias "Ethernet" `
  -IPAddress 10.42.0.10 `
  -PrefixLength 24 `
  -DefaultGateway 10.42.0.1
```

Point de vigilance :

- ne pas copier aveuglément `10.42.0.10` si votre range est différent ;
- l'adresse choisie doit être libre ;
- la passerelle doit correspondre au réseau utilisé.

## Étape 5 - Configurer le DNS sur l'adresse locale

Pour un futur contrôleur de domaine, le DNS préféré doit pointer vers lui-même.

Configurer le DNS :

```powershell
Set-DnsClientServerAddress `
  -InterfaceAlias "Ethernet" `
  -ServerAddresses 10.42.0.10
```

Vérifier :

```powershell
Get-DnsClientServerAddress -InterfaceAlias "Ethernet" -AddressFamily IPv4
ipconfig /all
```

Point de contrôle :

- l'IP est fixe ;
- le DNS préféré est l'adresse locale de `SRV-AD01` ;
- la passerelle est correcte.

!!! warning "DNS et AD"
    Le DNS est critique pour Active Directory. Un mauvais DNS peut empêcher la création du domaine, la connexion des clients et la résolution des services AD.

## Étape 6 - Tester la connectivité

Tester la passerelle :

```powershell
ping 10.42.0.1
```

Tester Internet si le laboratoire y donne accès :

```powershell
ping 1.1.1.1
```

Tester la résolution DNS actuelle :

```powershell
nslookup microsoft.com
```

!!! note "Avant l'installation DNS"
    Si le DNS pointe déjà vers `SRV-AD01` mais que le rôle DNS n'est pas encore installé, la résolution Internet peut échouer temporairement. Ce n'est pas bloquant pour installer AD DS/DNS, mais il faut le savoir.

## Étape 7 - Installer Active Directory Domain Services

Installer le rôle AD DS avec les outils d'administration :

```powershell
Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools
```

Vérifier :

```powershell
Get-WindowsFeature -Name AD-Domain-Services
```

Point de contrôle :

- `Install State` doit être `Installed` ;
- les outils d'administration AD DS sont inclus.

## Étape 8 - Installer DNS Server

Installer le rôle DNS :

```powershell
Install-WindowsFeature -Name DNS -IncludeManagementTools
```

Vérifier :

```powershell
Get-WindowsFeature -Name DNS
```

Point de contrôle :

- le rôle DNS est installé ;
- les outils DNS sont inclus.

!!! note "AD DS et DNS"
    Lors de la promotion d'un premier contrôleur de domaine avec `Install-ADDSForest`, DNS peut aussi être installé automatiquement. Ici, on l'installe explicitement pour respecter les consignes et rendre l'état du serveur clair.

## Étape 9 - Vérifier les rôles et outils

Vérifier les rôles principaux :

```powershell
Get-WindowsFeature -Name AD-Domain-Services,DNS
```

Vérifier les outils disponibles :

```powershell
Get-Command -Module ADDSDeployment
Get-Command -Module DnsServer
```

Vérifier les services :

```powershell
Get-Service DNS
```

Point de contrôle :

- AD DS est installé ;
- DNS Server est installé ;
- les modules PowerShell sont disponibles.

## Étape 10 - Préparer le journal des commandes

Pour garder une preuve PowerShell, utiliser une transcription.

Démarrer le journal :

```powershell
Start-Transcript -Path "C:\Activite2-SRV-AD01-commandes.txt"
```

Exécuter les commandes importantes de l'activité.

Arrêter le journal :

```powershell
Stop-Transcript
```

Vérifier le fichier :

```powershell
Get-ChildItem C:\Activite2-SRV-AD01-commandes.txt
```

## Vérifications finales

Commandes de synthèse :

```powershell
hostname
ipconfig /all
Get-WindowsFeature -Name AD-Domain-Services,DNS
Get-Service DNS
```

Résultat attendu :

- nom serveur : `SRV-AD01` ;
- IP fixe configurée ;
- DNS préféré : IP de `SRV-AD01` ;
- rôle AD DS installé ;
- rôle DNS installé.

Exemple de preuve nom/IP :

![Activité 2 - preuve nom et IP](../../assets/img/admin-windows/it-1/Activit%C3%A9%202%20a.png)

Exemple de preuve rôles AD DS et DNS :

![Activité 2 - rôles AD DS et DNS](../../assets/img/admin-windows/it-1/activit%C3%A92b.png)

## Livrables et preuves attendues

Convention de nommage :

```text
[Nom]-[Prénom]-[Site]-Activite2-[NomLivrable]
```

Livrables :

| Livrable | Preuve attendue | Exemple |
| --- | --- | --- |
| Capture nom/IP | `hostname` et `ipconfig /all` | `Nom-Prenom-Site-Activite2-Nom-IP.png` |
| Capture rôles AD DS et DNS | `Get-WindowsFeature -Name AD-Domain-Services,DNS` | `Nom-Prenom-Site-Activite2-Roles-ADDS-DNS.png` |
| Journal PowerShell | Fichier transcript des commandes | `Nom-Prenom-Site-Activite2-JournalCommandes.txt` |

## Checklist finale

- [ ] `SRV-AD01` est renommé.
- [ ] `SRV-AD01` possède une IP fixe.
- [ ] Le DNS préféré pointe vers l'adresse locale de `SRV-AD01`.
- [ ] Le rôle AD DS est installé.
- [ ] Le rôle DNS Server est installé.
- [ ] Les outils d'administration sont inclus.
- [ ] Les rôles sont vérifiés avec PowerShell.
- [ ] Le journal des commandes est sauvegardé.

## Ressources

- Microsoft Learn - Installer AD DS : <https://learn.microsoft.com/windows-server/identity/ad-ds/deploy/install-active-directory-domain-services--level-100->
- Microsoft Learn - Vue d'ensemble AD DS : <https://learn.microsoft.com/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview>
