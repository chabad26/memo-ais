# Activité 10 - Inventaire Active Directory avec PowerShell

## Mise en situation

L'administrateur doit produire un état de l'annuaire pour le dossier d'exploitation.

L'inventaire doit fournir une vision claire des utilisateurs, groupes, ordinateurs et unités d'organisation du domaine.

## Objectif de l'activité

Cette activité sert à créer un script d'inventaire Active Directory.

L'objectif est de :

- créer `Inventory-AD.ps1` ;
- créer un dossier `Exports` horodaté ;
- exporter les utilisateurs, leur OU et leurs groupes ;
- exporter les groupes et leurs membres ;
- exporter les ordinateurs avec leur OU ;
- exporter les OU et leurs sous-OU ;
- sélectionner des propriétés utiles ;
- exporter en CSV ;
- générer une page HTML si en avance ;
- documenter l'usage du script.

## Vue d'ensemble

| Élément | Valeur |
| --- | --- |
| Serveur d'exécution | `SRV-AD01` |
| Script | `Inventory-AD.ps1` |
| Dossier export | `C:\Scripts\Activite10\Exports\yyyyMMdd-HHmmss` |
| Formats | CSV, HTML optionnel |
| Module requis | ActiveDirectory |

## Fichier fourni

Un modèle est disponible :

```text
docs/assets/files/admin-windows/it-4/Inventory-AD.ps1
```

Copier le script sur `SRV-AD01`, par exemple dans :

```text
C:\Scripts\Activite10
```

## Étape 1 - Préparer le dossier de travail

Sur `SRV-AD01`, PowerShell en administrateur :

```powershell
New-Item -ItemType Directory -Path "C:\Scripts\Activite10" -Force
```

Copier `Inventory-AD.ps1` dans ce dossier.

Vérifier :

```powershell
Get-ChildItem "C:\Scripts\Activite10"
```

## Étape 2 - Créer Inventory-AD.ps1

Le script doit contenir :

- un en-tête commenté ;
- l'import du module Active Directory ;
- la création d'un dossier export horodaté ;
- les exports CSV ;
- une option HTML.

## Étape 3 - Script complet

Créer `Inventory-AD.ps1` :

```powershell
<#
.SYNOPSIS
  Exporte un inventaire Active Directory.

.DESCRIPTION
  Genere des exports CSV pour les utilisateurs, groupes, membres de groupes,
  ordinateurs et unites d'organisation.
  Cree un dossier d'export horodate.
  Peut generer une synthese HTML avec -GenerateHtml.

.PARAMETER ExportRoot
  Dossier racine des exports.

.PARAMETER GenerateHtml
  Genere une page HTML de synthese.

.NOTES
  Activite 10 - Administration Windows
  Executer depuis SRV-AD01 ou un poste avec RSAT Active Directory.
#>

[CmdletBinding()]
param(
  [string]$ExportRoot = "C:\Scripts\Activite10\Exports",
  [switch]$GenerateHtml
)

Import-Module ActiveDirectory

$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$ExportPath = Join-Path $ExportRoot $Timestamp
New-Item -ItemType Directory -Path $ExportPath -Force | Out-Null

$Domain = Get-ADDomain
$DomainDN = $Domain.DistinguishedName

function Get-ParentOu {
  param([string]$DistinguishedName)

  $Parts = $DistinguishedName -split ","
  ($Parts | Where-Object { $_ -like "OU=*" }) -join ","
}

$Users = Get-ADUser -Filter * -SearchBase $DomainDN -Properties DisplayName, Enabled, Department, Description, LastLogonDate, PasswordLastSet, MemberOf |
  Select-Object `
    SamAccountName,
    GivenName,
    Surname,
    DisplayName,
    Enabled,
    Department,
    Description,
    LastLogonDate,
    PasswordLastSet,
    DistinguishedName,
    @{ Name = "OU"; Expression = { Get-ParentOu $_.DistinguishedName } },
    @{ Name = "Groups"; Expression = {
      ($_.MemberOf | ForEach-Object {
        ($_ -split ",")[0] -replace "^CN=", ""
      }) -join ";"
    }}

$Groups = Get-ADGroup -Filter * -SearchBase $DomainDN -Properties Description, GroupScope, GroupCategory |
  Select-Object Name, SamAccountName, GroupScope, GroupCategory, Description, DistinguishedName,
    @{ Name = "OU"; Expression = { Get-ParentOu $_.DistinguishedName } }

$GroupMembers = foreach ($Group in Get-ADGroup -Filter * -SearchBase $DomainDN) {
  $Members = Get-ADGroupMember -Identity $Group -ErrorAction SilentlyContinue

  foreach ($Member in $Members) {
    [PSCustomObject]@{
      GroupName         = $Group.Name
      GroupSamAccount   = $Group.SamAccountName
      MemberName        = $Member.Name
      MemberSamAccount  = $Member.SamAccountName
      MemberObjectClass = $Member.ObjectClass
      MemberDN          = $Member.DistinguishedName
    }
  }
}

$Computers = Get-ADComputer -Filter * -SearchBase $DomainDN -Properties OperatingSystem, Enabled, LastLogonDate, Description |
  Select-Object Name, DNSHostName, Enabled, OperatingSystem, LastLogonDate, Description, DistinguishedName,
    @{ Name = "OU"; Expression = { Get-ParentOu $_.DistinguishedName } }

$Ous = Get-ADOrganizationalUnit -Filter * -SearchBase $DomainDN -Properties Description |
  Select-Object Name, Description, DistinguishedName,
    @{ Name = "ParentOU"; Expression = {
      $Parts = $_.DistinguishedName -split ","
      ($Parts | Select-Object -Skip 1 | Where-Object { $_ -like "OU=*" }) -join ","
    }}

$Users | Export-Csv -Path (Join-Path $ExportPath "AD-Users.csv") -NoTypeInformation -Encoding UTF8
$Groups | Export-Csv -Path (Join-Path $ExportPath "AD-Groups.csv") -NoTypeInformation -Encoding UTF8
$GroupMembers | Export-Csv -Path (Join-Path $ExportPath "AD-GroupMembers.csv") -NoTypeInformation -Encoding UTF8
$Computers | Export-Csv -Path (Join-Path $ExportPath "AD-Computers.csv") -NoTypeInformation -Encoding UTF8
$Ous | Export-Csv -Path (Join-Path $ExportPath "AD-OUs.csv") -NoTypeInformation -Encoding UTF8

$Summary = [PSCustomObject]@{
  Domain        = $Domain.DNSRoot
  ExportPath    = $ExportPath
  Users         = $Users.Count
  Groups        = $Groups.Count
  GroupMembers  = $GroupMembers.Count
  Computers     = $Computers.Count
  OUs           = $Ous.Count
  ExportDate    = Get-Date
}

$Summary | Export-Csv -Path (Join-Path $ExportPath "AD-Summary.csv") -NoTypeInformation -Encoding UTF8

if ($GenerateHtml) {
  $HtmlPath = Join-Path $ExportPath "AD-Inventory.html"

  $Html = @()
  $Html += "<html><head><meta charset='utf-8'><title>Inventaire Active Directory</title>"
  $Html += "<style>body{font-family:Segoe UI,Arial,sans-serif;margin:24px;} table{border-collapse:collapse;margin-bottom:24px;} th,td{border:1px solid #ccc;padding:6px 10px;} th{background:#f2f2f2;}</style>"
  $Html += "</head><body>"
  $Html += "<h1>Inventaire Active Directory - $($Domain.DNSRoot)</h1>"
  $Html += "<h2>Resume</h2>"
  $Html += ($Summary | ConvertTo-Html -Fragment)
  $Html += "<h2>Utilisateurs</h2>"
  $Html += ($Users | Select-Object SamAccountName, DisplayName, Enabled, OU, Groups | ConvertTo-Html -Fragment)
  $Html += "<h2>Groupes</h2>"
  $Html += ($Groups | Select-Object Name, GroupScope, GroupCategory, OU | ConvertTo-Html -Fragment)
  $Html += "<h2>Ordinateurs</h2>"
  $Html += ($Computers | Select-Object Name, OperatingSystem, Enabled, OU | ConvertTo-Html -Fragment)
  $Html += "<h2>Unites d'organisation</h2>"
  $Html += ($Ous | Select-Object Name, ParentOU, Description | ConvertTo-Html -Fragment)
  $Html += "</body></html>"

  $Html -join "`n" | Out-File -FilePath $HtmlPath -Encoding UTF8
}

Write-Host "Export termine : $ExportPath"
Get-ChildItem $ExportPath
```

## Étape 4 - Exécuter le script

Depuis `SRV-AD01` :

```powershell
Set-Location "C:\Scripts\Activite10"

.\Inventory-AD.ps1
```

Résultat attendu :

- un dossier `Exports` est créé ;
- un sous-dossier horodaté est créé ;
- les CSV sont générés.

## Étape 5 - Vérifier les exports CSV

Lister les fichiers :

```powershell
Get-ChildItem "C:\Scripts\Activite10\Exports" -Recurse
```

Vérifier les utilisateurs :

```powershell
Import-Csv "C:\Scripts\Activite10\Exports\DOSSIER_HORODATE\AD-Users.csv" |
  Select-Object SamAccountName, OU, Groups
```

Vérifier les groupes et membres :

```powershell
Import-Csv "C:\Scripts\Activite10\Exports\DOSSIER_HORODATE\AD-Groups.csv"
Import-Csv "C:\Scripts\Activite10\Exports\DOSSIER_HORODATE\AD-GroupMembers.csv"
```

Vérifier les ordinateurs :

```powershell
Import-Csv "C:\Scripts\Activite10\Exports\DOSSIER_HORODATE\AD-Computers.csv" |
  Select-Object Name, OperatingSystem, OU
```

Vérifier les OU :

```powershell
Import-Csv "C:\Scripts\Activite10\Exports\DOSSIER_HORODATE\AD-OUs.csv"
```

!!! note "Remplacer DOSSIER_HORODATE"
    Remplacer `DOSSIER_HORODATE` par le nom réel généré, par exemple `20260710-103000`.

## Étape 6 - Générer le rapport HTML optionnel

Si en avance :

```powershell
.\Inventory-AD.ps1 -GenerateHtml
```

Ouvrir le HTML :

```powershell
Start-Process "C:\Scripts\Activite10\Exports\DOSSIER_HORODATE\AD-Inventory.html"
```

## Étape 7 - Documenter l'usage du script

Ajouter dans le dossier de remise une courte documentation :

```text
Utilisation :
1. Copier Inventory-AD.ps1 sur SRV-AD01.
2. Ouvrir PowerShell en administrateur.
3. Exécuter .\Inventory-AD.ps1.
4. Récupérer les exports dans C:\Scripts\Activite10\Exports.
5. Option : .\Inventory-AD.ps1 -GenerateHtml.
```

## Exports générés

| Fichier | Contenu |
| --- | --- |
| `AD-Users.csv` | utilisateurs, OU, groupes, état, dates utiles |
| `AD-Groups.csv` | groupes, type, portée, OU |
| `AD-GroupMembers.csv` | membres de chaque groupe |
| `AD-Computers.csv` | ordinateurs, OS, OU |
| `AD-OUs.csv` | OU et sous-OU |
| `AD-Summary.csv` | résumé chiffré |
| `AD-Inventory.html` | rapport HTML optionnel |

## Dépannage rapide

### Le module ActiveDirectory est introuvable

Exécuter le script depuis `SRV-AD01` ou installer RSAT Active Directory sur le poste d'administration.

Vérifier :

```powershell
Get-Command Get-ADUser
```

### Un CSV est vide

Vérifier le domaine et le `SearchBase` :

```powershell
Get-ADDomain
```

Vérifier qu'il existe bien des objets :

```powershell
Get-ADUser -Filter *
Get-ADComputer -Filter *
Get-ADGroup -Filter *
```

### Le rapport HTML ne s'ouvre pas

Vérifier le chemin généré :

```powershell
Get-ChildItem "C:\Scripts\Activite10\Exports" -Recurse -Filter "*.html"
```

## Livrables et preuves attendues

Convention de nommage :

```text
[Nom]-[Prénom]-[Site]-Activite10-[NomLivrable]
```

Livrables :

| Livrable | Preuve attendue | Exemple |
| --- | --- | --- |
| Script | `Inventory-AD.ps1` commenté | `Nom-Prenom-Site-Activite10-Inventory-AD.ps1` |
| Exports CSV | CSV générés | `Nom-Prenom-Site-Activite10-Exports.zip` |
| Rapport HTML | Si réalisé | `Nom-Prenom-Site-Activite10-AD-Inventory.html` |
| Capture | Dossier exports horodaté | `Nom-Prenom-Site-Activite10-Exports.png` |

## Exemple de rapport

Rapport HTML généré pendant l'activité :

[Ouvrir le rapport AD-Inventory](AD-Inventory.html)

Le rapport contient notamment :

- un résumé du domaine ;
- les utilisateurs et leurs groupes ;
- les groupes ;
- les ordinateurs ;
- les unités d'organisation.

## Checklist finale

- [ ] `Inventory-AD.ps1` créé.
- [ ] Dossier `Exports` horodaté créé.
- [ ] Utilisateurs exportés.
- [ ] OU des utilisateurs exportée.
- [ ] Groupes des utilisateurs exportés.
- [ ] Groupes exportés.
- [ ] Membres des groupes exportés.
- [ ] Ordinateurs exportés avec leur OU.
- [ ] OU et sous-OU exportées.
- [ ] Propriétés utiles sélectionnées.
- [ ] Exports CSV générés.
- [ ] Rapport HTML généré si en avance.
- [ ] Usage du script documenté.

## Références

- Microsoft Learn - PowerShell : <https://learn.microsoft.com/powershell/>
- Microsoft Learn - Module Active Directory : <https://learn.microsoft.com/powershell/module/activedirectory/>
