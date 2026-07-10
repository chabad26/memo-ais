# Activité 6 - GPO : mot de passe, restriction panneau et déploiement 7-Zip

## Objectif de l'activité

Cette activité sert à appliquer les premières stratégies de groupe du domaine `corp.local`.

L'objectif est de :

- définir une stratégie de mot de passe ;
- interdire l'accès au panneau de configuration ;
- créer un partage réseau pour les packages ;
- préparer un MSI 7-Zip ;
- déployer 7-Zip par GPO sur les ordinateurs ;
- forcer l'application de la GPO sur `POSTE-01` ;
- générer un rapport `gpresult`.

## Vue d'ensemble

| Élément | Valeur |
| --- | --- |
| Domaine | `corp.local` |
| Contrôleur de domaine | `SRV-AD01` |
| Partage packages | `\\SRV-AD01\Packages` |
| Dossier 7-Zip | `\\SRV-AD01\Packages\7zip` |
| OU cible déploiement logiciel | `OU=Ordinateurs,DC=corp,DC=local` |
| GPO mot de passe | `GPO-PasswordPolicy` |
| GPO restriction panneau | `GPO-Restriction-Panel` |
| GPO déploiement logiciel | `GPO-Deploy-7Zip` |
| Poste de test | `POSTE-01` |

!!! warning "Point important sur les mots de passe"
    Dans Active Directory, la stratégie de mot de passe du domaine ne s'applique pas comme une GPO classique liée à une OU. Pour une stratégie globale de domaine, on utilise la stratégie du domaine ou la commande `Set-ADDefaultDomainPasswordPolicy`.

## Étape 1 - Démarrer le journal PowerShell

Sur `SRV-AD01`, ouvrir PowerShell en administrateur.

Créer une trace des commandes :

```powershell
Start-Transcript -Path "C:\Activite6-GPO-7Zip.txt"
```

Définir les variables :

```powershell
$DomainName = "corp.local"
$DomainDN = "DC=corp,DC=local"
$ComputerOU = "OU=Ordinateurs,$DomainDN"
$PackagesPath = "C:\Packages"
$SevenZipPath = "C:\Packages\7zip"
```

## Étape 2 - Créer GPO-PasswordPolicy

Créer une GPO pour tracer le livrable demandé :

```powershell
New-GPO -Name "GPO-PasswordPolicy" -Comment "Documentation de la stratégie de mot de passe du domaine"
```

Appliquer la stratégie de mot de passe au domaine :

```powershell
Set-ADDefaultDomainPasswordPolicy `
  -Identity $DomainName `
  -MinPasswordLength 12 `
  -ComplexityEnabled $true `
  -PasswordHistoryCount 10
```

Vérifier :

```powershell
Get-ADDefaultDomainPasswordPolicy |
  Select-Object MinPasswordLength, ComplexityEnabled, PasswordHistoryCount
```

Résultat attendu :

| Paramètre | Valeur attendue |
| --- | --- |
| `MinPasswordLength` | `12` |
| `ComplexityEnabled` | `True` |
| `PasswordHistoryCount` | `10` |

!!! note "Pourquoi la GPO existe quand même ?"
    Le nom `GPO-PasswordPolicy` permet de conserver une preuve conforme à la consigne. La configuration réellement efficace est celle du domaine, vérifiée avec `Get-ADDefaultDomainPasswordPolicy`.

## Étape 3 - Créer GPO-Restriction-Panel

Créer la GPO :

```powershell
New-GPO -Name "GPO-Restriction-Panel" -Comment "Interdire l'accès au panneau de configuration"
```

Configurer l'interdiction du panneau de configuration :

```powershell
Set-GPRegistryValue `
  -Name "GPO-Restriction-Panel" `
  -Key "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" `
  -ValueName "NoControlPanel" `
  -Type DWord `
  -Value 1
```

Lier la GPO à l'OU `Utilisateurs` :

```powershell
New-GPLink `
  -Name "GPO-Restriction-Panel" `
  -Target "OU=Utilisateurs,$DomainDN" `
  -LinkEnabled Yes
```

!!! info "Pourquoi OU=Utilisateurs ?"
    Le blocage du panneau de configuration est un paramètre utilisateur (`HKCU`). Il s'applique donc aux comptes utilisateurs, pas directement aux ordinateurs.

## Étape 4 - Créer le partage \\SRV-AD01\Packages

Créer les dossiers :

```powershell
New-Item -ItemType Directory -Path $PackagesPath -Force
New-Item -ItemType Directory -Path $SevenZipPath -Force
```

Créer le partage SMB :

```powershell
New-SmbShare `
  -Name "Packages" `
  -Path $PackagesPath `
  -Description "Packages MSI de déploiement logiciel"
```

Identifier le groupe `Domain Computers`, même sur un Windows en français :

```powershell
$DomainComputersSid = (Get-ADDomain).DomainSID.Value + "-515"
$DomainComputers = New-Object System.Security.Principal.SecurityIdentifier($DomainComputersSid)
$DomainComputersName = $DomainComputers.Translate([System.Security.Principal.NTAccount]).Value
$DomainComputersName
```

Donner l'accès en lecture au partage :

```powershell
Grant-SmbShareAccess `
  -Name "Packages" `
  -AccountName $DomainComputersName `
  -AccessRight Read `
  -Force
```

Donner l'accès NTFS en lecture :

```powershell
$Acl = Get-Acl $PackagesPath
$Rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
  $DomainComputersName,
  "ReadAndExecute",
  "ContainerInherit,ObjectInherit",
  "None",
  "Allow"
)
$Acl.SetAccessRule($Rule)
Set-Acl -Path $PackagesPath -AclObject $Acl
```

Vérifier :

```powershell
Get-SmbShareAccess -Name "Packages"
Get-Acl $PackagesPath | Select-Object -ExpandProperty Access
```

## Étape 5 - Télécharger et déposer le MSI 7-Zip

Créer un dossier temporaire :

```powershell
New-Item -ItemType Directory -Path "C:\Temp" -Force
```

Télécharger automatiquement le MSI 64 bits depuis le site officiel :

```powershell
$SevenZipDownloadPage = "https://www.7-zip.org/download.html"
$SevenZipPage = Invoke-WebRequest -Uri $SevenZipDownloadPage

$SevenZipMsiLink = $SevenZipPage.Links |
  Where-Object {
    $_.href -match "\.msi$" -and
    $_.outerHTML -match "64-bit Windows x64"
  } |
  Select-Object -First 1

$SevenZipMsiUrl = if ($SevenZipMsiLink.href -match "^https?://") {
  $SevenZipMsiLink.href
}
else {
  "https://www.7-zip.org/$($SevenZipMsiLink.href)"
}

$SevenZipMsiFile = Join-Path "C:\Temp" (Split-Path $SevenZipMsiUrl -Leaf)

Invoke-WebRequest `
  -Uri $SevenZipMsiUrl `
  -OutFile $SevenZipMsiFile
```

Vérifier le fichier téléchargé :

```powershell
Get-Item $SevenZipMsiFile
```

Si la détection automatique ne fonctionne pas, ouvrir la page officielle :

```text
https://www.7-zip.org/download.html
```

Choisir la ligne :

```text
64-bit Windows x64 - MSI installer
```

Déposer le fichier `.msi` téléchargé dans :

```text
\\SRV-AD01\Packages\7zip
```

Depuis `SRV-AD01`, le chemin local correspondant est :

```text
C:\Packages\7zip
```

Copier le MSI téléchargé vers le dossier de déploiement :

```powershell
Copy-Item $SevenZipMsiFile -Destination $SevenZipPath
```

Si le MSI est sur le poste Windows 11, copier le fichier vers le partage :

```powershell
Copy-Item "$env:USERPROFILE\Downloads\7z*.msi" -Destination "\\SRV-AD01\Packages\7zip"
```

Vérifier :

```powershell
Get-ChildItem $SevenZipPath
```

!!! warning "Chemin réseau obligatoire"
    Dans la GPO, il faut sélectionner le MSI via le chemin réseau `\\SRV-AD01\Packages\7zip\NomDuFichier.msi`, pas via `C:\Packages\7zip\...`.

## Étape 6 - Créer GPO-Deploy-7Zip

Créer la GPO :

```powershell
New-GPO -Name "GPO-Deploy-7Zip" -Comment "Déploiement de 7-Zip par MSI"
```

Lier la GPO à l'OU `Ordinateurs` :

```powershell
New-GPLink `
  -Name "GPO-Deploy-7Zip" `
  -Target $ComputerOU `
  -LinkEnabled Yes
```

Vérifier le lien :

```powershell
Get-GPInheritance -Target $ComputerOU
```

## Étape 7 - Ajouter le MSI au déploiement

Deux méthodes sont possibles.

### Méthode A - Software Installation avec GPMC

Cette méthode correspond exactement à la consigne, mais elle nécessite la console graphique `Group Policy Management`.

!!! warning "Limite en Server Core"
    Sur Server Core, les consoles graphiques ne sont pas locales. Si RSAT ne fonctionne pas sur le poste Windows 11 et si Windows Admin Center ne donne pas accès à l'éditeur complet des GPO, cette méthode n'est pas praticable dans le lab.

Depuis un poste avec RSAT fonctionnel, ouvrir :

```text
gpmc.msc
```

Aller dans :

```text
Forêt : corp.local
Domaines
corp.local
Objets de stratégie de groupe
GPO-Deploy-7Zip
```

Modifier la GPO :

```text
Configuration ordinateur
Paramètres du logiciel
Installation de logiciel
```

Ajouter le package :

1. Clic droit sur `Installation de logiciel`.
2. Choisir `Nouveau`.
3. Choisir `Package`.
4. Saisir le chemin réseau du MSI :

```text
\\SRV-AD01\Packages\7zip\7zXXXX-x64.msi
```

5. Choisir `Attribué` (`Assigned`).
6. Valider.

Point de contrôle :

- le package 7-Zip apparaît dans `Software Installation` ;
- le chemin affiché commence par `\\SRV-AD01\Packages`.

### Méthode B - Secours PowerShell par script de démarrage

Cette méthode garde l'objectif pédagogique : 7-Zip est installé automatiquement sur les ordinateurs de l'OU `Ordinateurs`, mais sans utiliser la console `Software Installation`.

Créer un script d'installation dans le partage :

```powershell
$InstallScriptPath = "C:\Packages\7zip\install-7zip.ps1"

@'
$Msi = Get-ChildItem "\\SRV-AD01\Packages\7zip\7z*-x64.msi" | Select-Object -First 1

if (-not (Test-Path "C:\Program Files\7-Zip\7zFM.exe")) {
  Start-Process msiexec.exe -ArgumentList "/i `"$($Msi.FullName)`" /qn /norestart" -Wait
}
'@ | Set-Content -Path $InstallScriptPath -Encoding UTF8
```

Créer un dossier de scripts dans `SYSVOL` :

```powershell
$Gpo = Get-GPO -Name "GPO-Deploy-7Zip"
$GpoScriptFolder = "\\corp.local\SYSVOL\corp.local\Policies\{$($Gpo.Id)}\Machine\Scripts\Startup"

New-Item -ItemType Directory -Path $GpoScriptFolder -Force
Copy-Item $InstallScriptPath -Destination $GpoScriptFolder -Force
```

Ajouter le script dans la GPO avec la console si elle devient disponible :

```text
Configuration ordinateur
Stratégies
Paramètres Windows
Scripts (démarrage/arrêt)
Démarrage
Ajouter
```

Nom du script :

```text
install-7zip.ps1
```

Paramètres :

```text
-ExecutionPolicy Bypass
```

!!! note "Si aucune console GPO n'est disponible"
    Continuer avec une installation distante pour valider le package et produire la preuve d'installation. Documenter clairement que la partie `Software Installation` n'a pas pu être réalisée à cause de l'absence de RSAT/GPMC.

Installation distante de secours depuis `SRV-AD01`, uniquement si PowerShell Remoting est actif sur `POSTE-01` :

```powershell
Invoke-Command -ComputerName "POSTE-01" -ScriptBlock {
  $Msi = Get-ChildItem "\\SRV-AD01\Packages\7zip\7z*-x64.msi" | Select-Object -First 1
  Start-Process msiexec.exe -ArgumentList "/i `"$($Msi.FullName)`" /qn /norestart" -Wait
}
```

Si cette commande échoue avec une erreur WinRM, utiliser la méthode C.

### Méthode C - Secours depuis POSTE-01

Cette méthode est la plus simple quand :

- RSAT/GPMC ne fonctionne pas ;
- Windows Admin Center ne propose pas l'éditeur complet des GPO ;
- WinRM est bloqué sur `POSTE-01`.

Sur `POSTE-01`, ouvrir PowerShell en administrateur et tester le partage :

```powershell
Test-Path "\\SRV-AD01\Packages\7zip"
Get-ChildItem "\\SRV-AD01\Packages\7zip"
```

Installer 7-Zip depuis le chemin réseau :

```powershell
cmd /c msiexec /i "\\SRV-AD01\Packages\7zip\7z2602-x64.msi" /qn /norestart
```

Vérifier :

```powershell
Test-Path "C:\Program Files\7-Zip\7zFM.exe"
```

!!! warning "À documenter dans le livrable"
    Cette méthode ne remplace pas `Software Installation` dans une infrastructure complète. Elle sert de contournement de labo : le package est bien centralisé sur `\\SRV-AD01\Packages`, mais l'installation est déclenchée depuis le poste car RSAT/GPMC et WinRM ne sont pas disponibles.

Point de contrôle :

- le MSI est accessible depuis le chemin réseau ;
- le script d'installation existe ;
- 7-Zip s'installe silencieusement sur `POSTE-01`.

## Étape 8 - Vérifier l'accès depuis POSTE-01

Sur `POSTE-01`, tester l'accès au partage :

```powershell
Test-Path "\\SRV-AD01\Packages\7zip"
Get-ChildItem "\\SRV-AD01\Packages\7zip"
```

Résultat attendu :

- `Test-Path` retourne `True` ;
- le MSI est visible.

Si l'accès échoue, vérifier :

- le DNS du poste ;
- les droits SMB ;
- les droits NTFS ;
- le pare-feu du serveur ;
- le chemin réseau utilisé.

## Étape 9 - Appliquer la GPO sur POSTE-01

Sur `POSTE-01`, forcer la mise à jour :

```powershell
gpupdate /force
```

Redémarrer le poste :

```powershell
Restart-Computer
```

!!! note "Installation au démarrage"
    Un logiciel attribué côté ordinateur s'installe généralement au redémarrage, avant l'ouverture de session.

## Étape 10 - Vérifier l'installation de 7-Zip

Sur `POSTE-01`, vérifier dans PowerShell :

```powershell
Get-Item "C:\Program Files\7-Zip\7zFM.exe"
```

Autre vérification :

```powershell
Get-Package | Where-Object Name -like "*7-Zip*"
```

Ou via l'interface :

```text
Paramètres
Applications
Applications installées
```

Point de contrôle :

- 7-Zip apparaît dans les applications installées ;
- le dossier `C:\Program Files\7-Zip` existe.

## Étape 11 - Générer gpresult

Sur `POSTE-01`, créer le rapport HTML :

```powershell
gpresult /h C:\Activite6-gpresult.html
```

Ouvrir le rapport :

```powershell
Start-Process C:\Activite6-gpresult.html
```

Vérifier dans le rapport :

- `GPO-Deploy-7Zip` appliquée côté ordinateur ;
- `GPO-Restriction-Panel` appliquée côté utilisateur ;
- absence d'erreur de filtrage de sécurité.

## Dépannage rapide

### 7-Zip ne s'installe pas

Si la GPO `GPO-Deploy-7Zip` est liée mais que 7-Zip ne s'installe pas automatiquement, vérifier d'abord ce point :

!!! info "GPO liée ne veut pas dire logiciel déployé"
    Une GPO vide ou seulement liée à une OU ne lance aucune installation. Pour un vrai déploiement `Software Installation`, le MSI doit être ajouté dans `Configuration ordinateur > Paramètres du logiciel > Installation de logiciel`. Dans notre lab, cette étape est bloquée si RSAT/GPMC n'est pas disponible.

Vérifier que le poste est bien dans l'OU `Ordinateurs` :

```powershell
Get-ADComputer "POSTE-01" -Properties DistinguishedName |
  Select-Object Name, DistinguishedName
```

Vérifier les GPO appliquées :

```powershell
gpresult /r
```

Vérifier l'accès au MSI :

```powershell
Test-Path "\\SRV-AD01\Packages\7zip\7zXXXX-x64.msi"
```

Si PowerShell Remoting échoue :

```powershell
Test-WSMan POSTE-01
```

Une erreur WinRM signifie que `Invoke-Command` ne peut pas être utilisé tant que la gestion à distance n'est pas activée côté `POSTE-01`.

### Le panneau de configuration reste accessible

Vérifier que l'utilisateur est dans l'OU `Utilisateurs` :

```powershell
Get-ADUser "user.rh1" -Properties DistinguishedName |
  Select-Object SamAccountName, DistinguishedName
```

Forcer la mise à jour côté utilisateur :

```powershell
gpupdate /force
```

Fermer puis rouvrir la session.

### Le rapport gpresult indique une GPO refusée

Vérifier :

- le lien de la GPO ;
- le filtrage de sécurité ;
- l'OU de l'objet ordinateur ou utilisateur ;
- les droits de lecture et d'application de la GPO.

## Option avancée - Déployer Notepad++

!!! warning "MSI ou EXE ?"
    Notepad++ fournit généralement un installeur officiel au format `.exe`, pas toujours un MSI. Pour `Software Installation`, il faut un MSI. Si aucun MSI fiable n'est disponible, utiliser la méthode de secours PowerShell avec installation silencieuse.

Créer un dossier sur `SRV-AD01` :

```powershell
New-Item -ItemType Directory -Path "C:\Packages\NotepadPlusPlus" -Force
```

Télécharger le dernier installeur officiel x64 depuis GitHub :

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$NotepadPath = "C:\Packages\NotepadPlusPlus"
$Release = Invoke-RestMethod -Uri "https://api.github.com/repos/notepad-plus-plus/notepad-plus-plus/releases/latest"

$NotepadAsset = $Release.assets |
  Where-Object {
    $_.name -match "Installer\.x64\.exe$"
  } |
  Select-Object -First 1

$NotepadInstaller = Join-Path $NotepadPath $NotepadAsset.name

Invoke-WebRequest `
  -Uri $NotepadAsset.browser_download_url `
  -OutFile $NotepadInstaller `
  -UseBasicParsing
```

Vérifier :

```powershell
Get-ChildItem "C:\Packages\NotepadPlusPlus"
```

Le chemin réseau correspondant est :

```text
\\SRV-AD01\Packages\NotepadPlusPlus
```

Créer une GPO dédiée et la lier à `OU=Ordinateurs` :

```powershell
New-GPO -Name "GPO-Deploy-NotepadPlusPlus" -Comment "Déploiement de Notepad++ par MSI"
New-GPLink -Name "GPO-Deploy-NotepadPlusPlus" -Target $ComputerOU -LinkEnabled Yes
```

### Si un MSI Notepad++ est disponible

Ajouter le MSI dans :

```text
Configuration ordinateur
Paramètres du logiciel
Installation de logiciel
```

Choisir `Attribué`.

### Si seul l'installeur EXE officiel est disponible

Créer un script d'installation silencieuse :

```powershell
$NotepadScriptPath = "C:\Packages\NotepadPlusPlus\install-notepadplusplus.ps1"

@'
$Installer = Get-ChildItem "\\SRV-AD01\Packages\NotepadPlusPlus\npp.*.Installer.x64.exe" | Select-Object -First 1

if (-not (Test-Path "C:\Program Files\Notepad++\notepad++.exe")) {
  Start-Process $Installer.FullName -ArgumentList "/S" -Wait
}
'@ | Set-Content -Path $NotepadScriptPath -Encoding UTF8
```

Installation distante de secours depuis `SRV-AD01` :

```powershell
Invoke-Command -ComputerName "POSTE-01" -ScriptBlock {
  $Installer = Get-ChildItem "\\SRV-AD01\Packages\NotepadPlusPlus\npp.*.Installer.x64.exe" | Select-Object -First 1

  if (-not (Test-Path "C:\Program Files\Notepad++\notepad++.exe")) {
    Start-Process $Installer.FullName -ArgumentList "/S" -Wait
  }
}
```

Si WinRM est bloqué, lancer l'installation directement depuis `POSTE-01` :

```powershell
cmd /c start /wait "" "\\SRV-AD01\Packages\NotepadPlusPlus\npp.8.9.6.4.Installer.x64.exe" /S
```

Vérifier sur `POSTE-01` :

```powershell
Get-Item "C:\Program Files\Notepad++\notepad++.exe"
```

Point de contrôle :

- Notepad++ est téléchargé dans `\\SRV-AD01\Packages\NotepadPlusPlus` ;
- l'installation silencieuse fonctionne ;
- Notepad++ est visible dans les applications installées.

## Option avancée - Assigned ou Published

| Mode | Disponible pour | Comportement |
| --- | --- | --- |
| `Assigned` | Utilisateur ou ordinateur | Installation imposée automatiquement |
| `Published` | Utilisateur uniquement | Application proposée dans l'ancien panneau d'ajout de programmes |

Pour un déploiement automatique sur les postes, utiliser `Assigned` côté ordinateur.

## Arrêter le journal PowerShell

Sur `SRV-AD01` :

```powershell
Stop-Transcript
```

Vérifier :

```powershell
Get-ChildItem C:\Activite6-GPO-7Zip.txt
```

## Livrables et preuves attendues

Convention de nommage :

```text
[Nom]-[Prénom]-[Site]-Activite6-[NomLivrable]
```

Livrables :

| Livrable | Preuve attendue | Exemple |
| --- | --- | --- |
| Capture Software Installation | MSI 7-Zip visible dans la GPO | `Nom-Prenom-Site-Activite6-SoftwareInstallation.png` |
| Preuve méthode secours | Script ou commande de déploiement utilisé si GPMC indisponible | `Nom-Prenom-Site-Activite6-DeploiementSecours.png` |
| Capture 7-Zip installé | 7-Zip visible sur `POSTE-01` | `Nom-Prenom-Site-Activite6-7ZipInstalle.png` |
| Rapport gpresult | Rapport HTML généré | `Nom-Prenom-Site-Activite6-gpresult.html` |
| Journal PowerShell | Commandes exécutées | `Nom-Prenom-Site-Activite6-JournalCommandes.txt` |

## Exemples de preuves

7-Zip installé sur `POSTE-01` :

![7-Zip installé](<../../assets/img/admin-windows/it-2/7zipok.png>)

Connexion avec `user.rh1` et vérification de 7-Zip :

![POSTE-01 user.rh1 7-Zip OK](<../../assets/img/admin-windows/it-2/POSTE-01 & userr.h1 7zip ok.png>)

Rapport `gpresult` généré :

![Rapport gpresult](<../../assets/img/admin-windows/it-2/gpohtml.png>)

Notepad++ installé :

![Notepad++ installé](<../../assets/img/admin-windows/it-2/notepadok.png>)

## Checklist finale

- [ ] Stratégie de mot de passe configurée : 12 caractères, complexité, historique 10.
- [ ] `GPO-Restriction-Panel` créée.
- [ ] Restriction panneau de configuration configurée.
- [ ] Partage `\\SRV-AD01\Packages` créé.
- [ ] Dossier `\\SRV-AD01\Packages\7zip` créé.
- [ ] MSI 7-Zip déposé dans le dossier.
- [ ] `Domain Computers` a accès en lecture.
- [ ] `GPO-Deploy-7Zip` créée.
- [ ] MSI ajouté avec le chemin réseau, ou méthode de secours documentée.
- [ ] Mode `Assigned` choisi si GPMC est disponible.
- [ ] GPO liée à `OU=Ordinateurs`.
- [ ] `gpupdate /force` exécuté sur `POSTE-01`.
- [ ] `POSTE-01` redémarré.
- [ ] 7-Zip installé.
- [ ] Rapport `gpresult /h` généré.
