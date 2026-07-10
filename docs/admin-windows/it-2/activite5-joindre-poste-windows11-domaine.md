# Activité 5 - Joindre un poste Windows 11 au domaine

## Objectif de l'activité

Cette activité sert à intégrer un poste client Windows 11 au domaine Active Directory `corp.local`.

L'objectif est de :

- préparer un poste Windows 11 ;
- vérifier la connectivité avec `SRV-AD01` ;
- configurer le DNS vers le contrôleur de domaine ;
- joindre le domaine ;
- déplacer l'objet ordinateur dans l'OU `Ordinateurs` ;
- tester une ouverture de session avec `user.rh1`.

## Vue d'ensemble

| Élément | Configuration attendue |
| --- | --- |
| Poste client | `POSTE-01` ou poste Windows 11 existant |
| OS | Windows 11 |
| vCPU si VM | 2 |
| RAM si VM | 4 Go |
| Disque si VM | 60 Go |
| TPM virtuel | Activé si VM Hyper-V |
| DNS client | IP de `SRV-AD01` |
| Domaine | `corp.local` |
| OU cible | `OU=Ordinateurs,DC=corp,DC=local` |
| Test utilisateur | `CORP\user.rh1` |

!!! note "Dans notre cas"
    Si un Windows 11 existe déjà sur le laptop et communique avec `SRV-AD01`, il peut être réutilisé. Il faut surtout vérifier le DNS, joindre le domaine et tester la connexion.

## Étape 1 - Créer ou réutiliser le poste Windows 11

Deux possibilités :

- créer une VM `POSTE-01` dans Hyper-V ;
- réutiliser un Windows 11 déjà présent.

Si une VM est créée, utiliser les paramètres suivants :

| Paramètre | Valeur |
| --- | --- |
| Nom VM | `POSTE-01` |
| Génération | 2 |
| vCPU | 2 |
| RAM | 4 Go |
| Disque | 60 Go |
| Réseau | Même réseau que `SRV-AD01` |
| Sécurité | TPM virtuel activé |

En PowerShell Hyper-V, exemple :

```powershell
New-VM `
  -Name "POSTE-01" `
  -Generation 2 `
  -MemoryStartupBytes 4GB `
  -NewVHDPath "C:\Hyper-V\VHDX\POSTE-01.vhdx" `
  -NewVHDSizeBytes 60GB `
  -Path "C:\Hyper-V\VMs" `
  -SwitchName "vSwitch-Externe"

Set-VMProcessor -VMName "POSTE-01" -Count 2
Set-VMKeyProtector -VMName "POSTE-01" -NewLocalKeyProtector
Enable-VMTPM -VMName "POSTE-01"
```

!!! warning "TPM virtuel"
    Windows 11 et BitLocker nécessitent le TPM. Sur Hyper-V, il faut utiliser une VM de génération 2 et activer le TPM virtuel.

## Étape 2 - Installer Windows 11

Installer Windows 11 normalement depuis l'ISO.

Points de contrôle :

- Windows démarre ;
- le compte local ou Microsoft initial fonctionne ;
- le poste accède au réseau du laboratoire.

Si le poste Windows 11 existe déjà, passer directement à l'étape réseau.

## Étape 3 - Configurer le nom du poste

Renommer le poste :

```powershell
Rename-Computer -NewName "POSTE-01" -Restart
```

Après redémarrage :

```powershell
hostname
```

## Étape 4 - Configurer l'IP et le DNS

Identifier la carte réseau :

```powershell
Get-NetAdapter
```

Configurer une IP dans le range du laboratoire.

Exemple avec DHCP pour l'IP, mais DNS forcé vers `SRV-AD01` :

```powershell
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses 10.42.0.10
```

Exemple avec IP fixe :

```powershell
New-NetIPAddress `
  -InterfaceAlias "Ethernet" `
  -IPAddress 10.42.0.20 `
  -PrefixLength 24 `
  -DefaultGateway 10.42.0.1

Set-DnsClientServerAddress `
  -InterfaceAlias "Ethernet" `
  -ServerAddresses 10.42.0.10
```

Adapter :

| Élément | Exemple |
| --- | --- |
| IP poste | `10.42.0.20` |
| Passerelle | `10.42.0.1` |
| DNS | `10.42.0.10` |

Vérifier :

```powershell
ipconfig /all
nslookup corp.local
nslookup SRV-AD01.corp.local
```

!!! warning "DNS obligatoire"
    Pour joindre le domaine, le DNS du poste doit pointer vers `SRV-AD01`. Ne pas utiliser seulement un DNS Internet comme `1.1.1.1` ou `8.8.8.8`.

## Étape 5 - Joindre le domaine corp.local

Depuis le poste Windows 11, lancer PowerShell en administrateur :

```powershell
Add-Computer -DomainName "corp.local" -Credential "CORP\Administrateur" -Restart
```

Saisir le mot de passe du compte administrateur du domaine.

Le poste redémarre automatiquement.

Point de contrôle :

- la jonction au domaine ne retourne pas d'erreur ;
- le poste redémarre ;
- l'écran de connexion permet d'utiliser un compte de domaine.

## Étape 6 - Vérifier l'objet ordinateur dans Active Directory

Sur `SRV-AD01`, vérifier que le poste apparaît :

```powershell
Get-ADComputer -Identity "POSTE-01" -Properties DistinguishedName
```

Par défaut, l'objet peut être dans :

```text
CN=Computers,DC=corp,DC=local
```

## Étape 7 - Déplacer l'objet dans OU=Ordinateurs

Sur `SRV-AD01`, déplacer l'objet ordinateur :

```powershell
Get-ADComputer -Identity "POSTE-01" |
  Move-ADObject -TargetPath "OU=Ordinateurs,DC=corp,DC=local"
```

Vérifier :

```powershell
Get-ADComputer -Identity "POSTE-01" -Properties DistinguishedName |
  Select-Object Name, DistinguishedName
```

Point de contrôle :

- l'objet `POSTE-01` est dans `OU=Ordinateurs`.

## Étape 8 - Tester la connexion avec user.rh1

Sur le poste Windows 11, ouvrir une session avec :

```text
CORP\user.rh1
```

ou :

```text
user.rh1@corp.local
```

Vérifier l'identité :

```powershell
whoami
```

Résultat attendu :

```text
corp\user.rh1
```

Si le système demande un changement de mot de passe à la première connexion, définir un nouveau mot de passe conforme à la stratégie du domaine.

## Dépannage rapide

### Le domaine est introuvable

Vérifier DNS :

```powershell
ipconfig /all
nslookup corp.local
nslookup SRV-AD01.corp.local
```

Le DNS du poste doit être l'IP de `SRV-AD01`.

### La jonction échoue avec un problème d'identifiants

Vérifier le compte utilisé :

```text
CORP\Administrateur
```

ou un autre compte ayant le droit de joindre une machine au domaine.

### Le login user.rh1 échoue

Sur `SRV-AD01`, vérifier le compte :

```powershell
Get-ADUser user.rh1 -Properties Enabled,LockedOut,PasswordExpired
```

Réinitialiser le mot de passe si nécessaire :

```powershell
$Password = Read-Host "Nouveau mot de passe user.rh1" -AsSecureString
Set-ADAccountPassword -Identity "user.rh1" -NewPassword $Password -Reset
Enable-ADAccount -Identity "user.rh1"
Set-ADUser -Identity "user.rh1" -ChangePasswordAtLogon $true
```

## Livrables et preuves attendues

Convention de nommage :

```text
[Nom]-[Prénom]-[Site]-Activite5-[NomLivrable]
```

Livrables possibles :

| Livrable | Preuve attendue | Exemple |
| --- | --- | --- |
| Capture poste joint au domaine | Informations système ou `whoami` | `Nom-Prenom-Site-Activite5-Poste-Domaine.png` |
| Capture objet ordinateur | `Get-ADComputer POSTE-01` dans `OU=Ordinateurs` | `Nom-Prenom-Site-Activite5-ObjetOrdinateur.png` |
| Capture login user.rh1 | `whoami` retourne `corp\user.rh1` | `Nom-Prenom-Site-Activite5-Whoami-user-rh1.png` |

## Exemples de preuves

Vérification du compte de domaine depuis Windows 11 :

![Vérification utilisateur domaine](<../../assets/img/admin-windows/it-2/vérifuserdomain.png>)

Connexion de `user.rh1` sur le poste Windows 11 :

![Connexion user.rh1 Windows 11](<../../assets/img/admin-windows/it-2/userlogerwinn11.png>)

## Checklist finale

- [ ] Le poste Windows 11 existe ou est réutilisé.
- [ ] Le poste est nommé `POSTE-01`.
- [ ] Le poste communique avec `SRV-AD01`.
- [ ] Le DNS du poste pointe vers `SRV-AD01`.
- [ ] Le domaine `corp.local` est joignable.
- [ ] Le poste est joint au domaine.
- [ ] L'objet ordinateur est déplacé dans `OU=Ordinateurs`.
- [ ] La connexion `user.rh1` fonctionne.
