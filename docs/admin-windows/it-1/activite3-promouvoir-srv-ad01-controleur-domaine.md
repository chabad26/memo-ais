# Activité 3 - Promouvoir SRV-AD01 en contrôleur de domaine

## Objectif de l'activité

Cette activité transforme `SRV-AD01` en premier contrôleur de domaine Active Directory.

L'objectif est de :

- créer une nouvelle forêt Active Directory ;
- utiliser un domaine en `.local`, par exemple `corp.local` ;
- définir le mot de passe DSRM ;
- valider les prérequis ;
- redémarrer le serveur ;
- vérifier les consoles AD, DNS et GPO ;
- tester une connexion avec un compte de domaine.

## Vue d'ensemble

| Élément | Valeur attendue |
| --- | --- |
| Serveur | `SRV-AD01` |
| Rôle | Premier contrôleur de domaine |
| Forêt | Nouvelle forêt |
| Domaine | `corp.local` ou autre nom en `.local` |
| NetBIOS | `CORP` |
| DNS | Installé et intégré à AD |
| Méthode principale | PowerShell avec `Install-ADDSForest` |

!!! warning "Avant de commencer"
    Vérifier que `SRV-AD01` possède une IP fixe et que son DNS préféré pointe vers lui-même. Un mauvais DNS est une cause classique d'échec Active Directory.

## Étape 1 - Vérifier l'état de SRV-AD01

Vérifier le nom :

```powershell
hostname
```

Vérifier l'adresse IP et le DNS :

```powershell
ipconfig /all
```

Vérifier les rôles installés :

```powershell
Get-WindowsFeature -Name AD-Domain-Services,DNS
```

Résultat attendu :

- le serveur s'appelle `SRV-AD01` ;
- l'adresse IP est fixe ;
- le DNS préféré est l'adresse locale de `SRV-AD01` ;
- AD DS et DNS sont installés.

## Étape 2 - Préparer le journal PowerShell

Créer un journal de commandes pour garder une preuve :

```powershell
Start-Transcript -Path "C:\Activite3-Promotion-ADDS.txt"
```

Le journal sera arrêté à la fin avec :

```powershell
Stop-Transcript
```

## Étape 3 - Préparer le mot de passe DSRM

Le mot de passe **DSRM** sert au mode de restauration des services d'annuaire.

Il doit être robuste et différent d'un mot de passe utilisateur classique.

Créer une variable sécurisée :

```powershell
$DSRMPassword = Read-Host "Mot de passe DSRM" -AsSecureString
```

!!! warning "Important"
    Conserver ce mot de passe dans un emplacement autorisé. Il peut être nécessaire en cas de restauration Active Directory.

## Étape 4 - Promouvoir avec Install-ADDSForest

Créer une nouvelle forêt `corp.local` :

```powershell
Install-ADDSForest `
  -DomainName "corp.local" `
  -DomainNetbiosName "CORP" `
  -SafeModeAdministratorPassword $DSRMPassword `
  -InstallDns `
  -Force
```

Adapter si besoin :

| Paramètre | Exemple | Rôle |
| --- | --- | --- |
| `-DomainName` | `corp.local` | Nom DNS du domaine |
| `-DomainNetbiosName` | `CORP` | Nom court NetBIOS |
| `-InstallDns` | activé | Installe/configure DNS |
| `-SafeModeAdministratorPassword` | variable sécurisée | Mot de passe DSRM |

La commande vérifie les prérequis, installe les composants nécessaires, configure AD DS/DNS, puis redémarre le serveur.

### Avertissement DNS sur la délégation

Pendant la promotion, un avertissement peut apparaître :

```text
Il est impossible de créer une délégation pour ce serveur DNS car la zone parente faisant autorité est introuvable...
```

Dans ce laboratoire, avec un domaine comme `corp.local`, cet avertissement est **normal**.

Il signifie que Windows ne trouve pas de zone DNS parente capable de déléguer `corp.local`.

Cas typique :

```text
corp.local
```

Il n'existe pas de vraie zone parente `.local` à administrer dans le labo, donc aucune délégation DNS ne peut être créée automatiquement.

Conclusion :

- en laboratoire isolé : aucune action requise ;
- en entreprise avec une infrastructure DNS existante : créer manuellement la délégation dans la zone parente ;
- pour ce TP : continuer la promotion.

!!! note "Assistant graphique"
    Avec Windows Admin Center ou Server Manager sur une machine d'administration, il est aussi possible de lancer l'assistant de promotion. Dans ce module, PowerShell est prioritaire car il est plus rapide et plus reproductible.

## Étape 5 - Attendre le redémarrage

Après la promotion, `SRV-AD01` redémarre automatiquement.

Attendre quelques minutes, puis tester :

```powershell
ping SRV-AD01
```

ou avec l'adresse IP :

```powershell
ping IP_DE_SRV_AD01
```

Se reconnecter ensuite avec un compte de domaine :

```powershell
Enter-PSSession -ComputerName SRV-AD01 -Credential CORP\Administrateur
```

Si la résolution DNS n'est pas encore disponible, utiliser l'IP :

```powershell
Enter-PSSession -ComputerName IP_DE_SRV_AD01 -Credential CORP\Administrateur
```

## Étape 6 - Vérifier le domaine

Vérifier le domaine Active Directory :

```powershell
Get-ADDomain
Get-ADForest
```

Vérifier le contrôleur de domaine :

```powershell
Get-ADDomainController
```

Vérifier les partages SYSVOL et NETLOGON :

```powershell
net share
```

Résultat attendu :

- domaine `corp.local` créé ;
- forêt `corp.local` créée ;
- `SRV-AD01` est contrôleur de domaine ;
- les partages `SYSVOL` et `NETLOGON` existent.

## Étape 7 - Vérifier DNS

Vérifier le service DNS :

```powershell
Get-Service DNS
```

Lister les zones DNS :

```powershell
Get-DnsServerZone
```

Tester la résolution du domaine :

```powershell
nslookup corp.local
nslookup SRV-AD01.corp.local
```

Point de contrôle :

- la zone `corp.local` existe ;
- `SRV-AD01.corp.local` se résout ;
- DNS répond localement.

### Dépannage nslookup avec ::1

Si `nslookup corp.local` affiche un serveur DNS en `::1` puis un timeout, vérifier d'abord la configuration DNS du serveur :

```powershell
ipconfig /all
Get-DnsClientServerAddress -AddressFamily IPv4
Get-DnsClientServerAddress -AddressFamily IPv6
```

Sur un contrôleur de domaine de laboratoire, le DNS préféré peut pointer vers l'adresse IPv4 locale du serveur, par exemple :

```powershell
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses 10.42.0.10
```

Tester ensuite directement le serveur DNS IPv4 :

```powershell
nslookup SRV-AD01.corp.local 10.42.0.10
nslookup -type=SRV _ldap._tcp.dc._msdcs.corp.local 10.42.0.10
```

Interprétation :

| Test | Résultat attendu |
| --- | --- |
| `Get-DnsServerZone` | Zones `corp.local` et `_msdcs.corp.local` présentes |
| `nslookup SRV-AD01.corp.local` | Retourne l'adresse IP du contrôleur de domaine |
| `_ldap._tcp.dc._msdcs.corp.local` | Retourne un enregistrement SRV vers `SRV-AD01` |

!!! note "Nom du domaine"
    `corp.local` seul ne retourne pas toujours une adresse IP utile. Le test le plus parlant est souvent `SRV-AD01.corp.local` ou les enregistrements SRV Active Directory.

## Étape 8 - Ouvrir les consoles d'administration

Depuis Windows Admin Center ou un poste Windows avec RSAT, ouvrir :

- **Active Directory Users and Computers** ;
- **DNS Manager** ;
- **Group Policy Management**.

Commandes utiles sur un poste Windows avec RSAT :

```powershell
dsa.msc
dnsmgmt.msc
gpmc.msc
```

### Dépannage RSAT introuvable

Si `dsa.msc`, `dnsmgmt.msc` ou `gpmc.msc` ne sont pas trouvés sur le poste Windows, vérifier d'abord que les composants RSAT sont réellement installés.

Sur le poste Windows d'administration :

```powershell
Get-WindowsCapability -Online -Name "Rsat.ActiveDirectory*" |
  Select-Object Name, State

Get-WindowsCapability -Online -Name "Rsat.Dns*" |
  Select-Object Name, State

Get-WindowsCapability -Online -Name "Rsat.GroupPolicy*" |
  Select-Object Name, State
```

Installer ou réinstaller les outils :

```powershell
Add-WindowsCapability -Online -Name Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0
Add-WindowsCapability -Online -Name Rsat.Dns.Tools~~~~0.0.1.0
Add-WindowsCapability -Online -Name Rsat.GroupPolicy.Management.Tools~~~~0.0.1.0
```

Si `Add-WindowsCapability` retourne `0x800f0950`, vérifier d'abord les noms exacts disponibles sur le poste :

```powershell
Get-WindowsCapability -Online |
  Where-Object Name -like "Rsat*" |
  Select-Object Name, State
```

Installer uniquement un nom présent dans cette liste.

Méthode alternative par l'interface graphique Windows 11 :

```text
Paramètres > Système > Fonctionnalités facultatives > Afficher les fonctionnalités
```

Rechercher et installer :

- `RSAT: Active Directory Domain Services and Lightweight Directory Services Tools`
- `RSAT: DNS Server Tools`
- `RSAT: Group Policy Management Tools`

Si le poste vient d'être joint au domaine, une stratégie peut empêcher le téléchargement des fonctionnalités facultatives depuis Windows Update. Dans ce cas, vérifier les stratégies Windows Update ou installer RSAT avant d'appliquer les GPO du domaine.

Si l'erreur `0x800f0950` persiste :

1. Vérifier que Windows Update fonctionne.

```powershell
Get-Service wuauserv
Start-Service wuauserv
```

2. Réparer l'image Windows.

```powershell
DISM /Online /Cleanup-Image /RestoreHealth
sfc /scannow
```

3. Redémarrer le poste Windows 11.

4. Réessayer l'installation RSAT.

```powershell
Add-WindowsCapability -Online -Name Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0
Add-WindowsCapability -Online -Name Rsat.Dns.Tools~~~~0.0.1.0
Add-WindowsCapability -Online -Name Rsat.GroupPolicy.Management.Tools~~~~0.0.1.0
```

Si l'erreur reste présente, continuer le TP en PowerShell depuis `SRV-AD01`. Les consoles graphiques RSAT sont pratiques pour les captures, mais les vérifications AD peuvent être faites avec :

```powershell
Get-ADOrganizationalUnit -Filter *
Get-ADUser -Filter *
Get-ADGroup -Filter *
Get-DnsServerZone
Get-GPO -All
```

Redémarrer le poste si nécessaire.

Vérifier ensuite les fichiers :

```powershell
Get-ChildItem C:\Windows\System32\dsa.msc
Get-ChildItem C:\Windows\System32\dnsmgmt.msc
Get-ChildItem C:\Windows\System32\gpmc.msc
```

Lancer avec le chemin complet si besoin :

```powershell
C:\Windows\System32\dsa.msc
C:\Windows\System32\dnsmgmt.msc
C:\Windows\System32\gpmc.msc
```

Il est aussi possible de les retrouver dans :

```text
Menu Démarrer > Outils Windows
```

!!! note "Attention"
    Les RSAT doivent être installés sur le poste Windows d'administration, pas sur Server Core. Sur Server Core, les consoles graphiques MMC ne sont pas disponibles localement.

Sur Server Core, les consoles graphiques ne sont pas locales. Il faut les ouvrir depuis :

- Windows Admin Center ;
- un poste Windows d'administration avec RSAT ;
- Server Manager sur un poste qui dispose des outils.

Point de contrôle :

- la console DNS affiche la zone `corp.local` ;
- la console ADUC affiche le domaine ;
- la console GPMC affiche la forêt et le domaine.

## Étape 9 - Créer un compte de test

Créer une OU de test :

```powershell
New-ADOrganizationalUnit -Name "Utilisateurs" -Path "DC=corp,DC=local"
```

Créer un utilisateur de test :

```powershell
$Password = Read-Host "Mot de passe utilisateur test" -AsSecureString

New-ADUser `
  -Name "Test Domaine" `
  -GivenName "Test" `
  -Surname "Domaine" `
  -SamAccountName "test.domaine" `
  -UserPrincipalName "test.domaine@corp.local" `
  -Path "OU=Utilisateurs,DC=corp,DC=local" `
  -AccountPassword $Password `
  -Enabled $true
```

Vérifier :

```powershell
Get-ADUser test.domaine
```

## Étape 10 - Tester une ouverture de session domaine

Depuis une machine jointe au domaine, ouvrir une session avec :

```text
CORP\test.domaine
```

ou :

```text
test.domaine@corp.local
```

Vérifier l'identité :

```powershell
whoami
```

Résultat attendu :

```text
corp\test.domaine
```

!!! note "Si aucun poste n'est encore joint au domaine"
    Garder cette preuve pour l'activité suivante, lorsque le premier poste client sera intégré au domaine. Pour cette activité, une preuve avec `Get-ADUser test.domaine` peut compléter temporairement.

## Étape 11 - Option avancée : exécuter dcdiag

Installer l'outil si nécessaire avec les outils AD DS.

Lancer un diagnostic général :

```powershell
dcdiag
```

Enregistrer le résultat dans un fichier :

```powershell
dcdiag /v > C:\Activite3-dcdiag.txt
```

Vérifier les erreurs :

```powershell
Select-String -Path C:\Activite3-dcdiag.txt -Pattern "failed","erreur","error"
```

### Interpréter un échec DFSREvent récent

Juste après la promotion du premier contrôleur de domaine, `dcdiag` peut signaler un échec du test `DFSREvent`.

Exemple :

```text
Le test DFSREvent de SRV-AD01 a échoué
Erreur : 1355 (Le domaine spécifié n'existe pas ou n'a pas pu être contacté.)
```

Si les autres tests passent et que `SYSVOL` est prêt, ce message peut venir d'événements DFSR générés pendant la phase de démarrage initiale du domaine.

Vérifier les points importants :

```powershell
net share
dcdiag /test:SysVolCheck
dcdiag /test:NetLogons
dcdiag /test:Advertising
```

Résultat attendu :

- les partages `SYSVOL` et `NETLOGON` existent ;
- `SysVolCheck` réussit ;
- `NetLogons` réussit ;
- `Advertising` réussit ;
- le contrôleur de domaine s'annonce comme DC, LDAP, KDC, DNS et GC.

Relancer ensuite `dcdiag` après quelques minutes :

```powershell
dcdiag /v > C:\Activite3-dcdiag-apres-attente.txt
```

!!! note "À documenter"
    Si seul `DFSREvent` échoue à cause d'événements récents, mais que `SYSVOL`, `NETLOGON`, `Advertising`, `KCC`, `Services`, `Replications` et `LocatorCheck` réussissent, l'état du contrôleur de domaine est globalement bon pour le laboratoire. Il faut noter l'avertissement et relancer le test après stabilisation.

Point de contrôle :

- documenter les erreurs éventuelles ;
- corriger les erreurs DNS avant de continuer le module.

## Étape 12 - Arrêter le journal PowerShell

Arrêter la transcription :

```powershell
Stop-Transcript
```

Vérifier le fichier :

```powershell
Get-ChildItem C:\Activite3-Promotion-ADDS.txt
```

## Vérifications finales

Commandes de synthèse :

```powershell
hostname
whoami
Get-ADDomain
Get-ADForest
Get-ADDomainController
Get-DnsServerZone
net share
```

Exemples de preuves pour l'activité 3 :

![Activité 3 - Get-ADDomain résultat 1](../../assets/img/admin-windows/it-1/act3%20Get-ADDomain1.png)

![Activité 3 - Get-ADDomain résultat 2](../../assets/img/admin-windows/it-1/act3%20Get-ADDomain2.png)

![Activité 3 - Get-ADForest](../../assets/img/admin-windows/it-1/act3%20Get-ADForest.png)

![Activité 3 - Get-ADDomainController](../../assets/img/admin-windows/it-1/act3%20Get-ADDomainController.png)

![Activité 3 - nslookup](../../assets/img/admin-windows/it-1/act3%20nslookup.png)

Résultat attendu :

- `SRV-AD01` est contrôleur de domaine ;
- le domaine `corp.local` existe ;
- DNS fonctionne ;
- les consoles AD/DNS/GPO sont accessibles ;
- un compte de domaine peut être créé et testé.

## Livrables et preuves attendues

Convention de nommage :

```text
[Nom]-[Prénom]-[Site]-Activite3-[NomLivrable]
```

Livrables :

| Livrable | Preuve attendue | Exemple |
| --- | --- | --- |
| Capture console DNS | Zone `corp.local` visible | `Nom-Prenom-Site-Activite3-ConsoleDNS.png` |
| Preuve connexion domaine | `whoami` avec `corp\utilisateur` | `Nom-Prenom-Site-Activite3-Whoami-Domaine.png` |
| Journal PowerShell | Transcript promotion AD DS | `Nom-Prenom-Site-Activite3-JournalCommandes.txt` |
| Option avancée dcdiag | Résultat `dcdiag` | `Nom-Prenom-Site-Activite3-dcdiag.txt` |

## Checklist finale

- [ ] Le mot de passe DSRM est défini.
- [ ] `Install-ADDSForest` a été exécuté.
- [ ] Le serveur a redémarré.
- [ ] Le domaine `corp.local` est créé.
- [ ] DNS contient la zone du domaine.
- [ ] ADUC est accessible.
- [ ] DNS Manager est accessible.
- [ ] GPMC est accessible.
- [ ] Un compte de test domaine existe.
- [ ] Une preuve `whoami` est réalisée ou planifiée après jonction d'un client.
- [ ] `dcdiag` est exécuté si l'option avancée est demandée.

## Ressources

- Microsoft Learn - Installer AD DS : <https://learn.microsoft.com/windows-server/identity/ad-ds/deploy/install-active-directory-domain-services--level-100->
- Microsoft Learn - Vue d'ensemble AD DS : <https://learn.microsoft.com/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview>
