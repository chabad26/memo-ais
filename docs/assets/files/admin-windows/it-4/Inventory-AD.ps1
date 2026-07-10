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
