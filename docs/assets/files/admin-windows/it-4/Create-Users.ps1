<#
.SYNOPSIS
  Cree des utilisateurs Active Directory depuis un CSV.

.DESCRIPTION
  Importe un fichier CSV contenant Prenom, Nom, Login, Service, Groupe.
  Verifie si les comptes existent deja.
  Cree les comptes dans la bonne OU.
  Ajoute les comptes au groupe demande.
  Exporte un rapport CSV.

.PARAMETER CsvPath
  Chemin du fichier CSV source.

.PARAMETER ReportPath
  Chemin du rapport CSV genere.

.PARAMETER WhatIf
  Simule les actions sans creer de compte.

.NOTES
  Activite 9 - Administration Windows
  Ne pas stocker de secret sensible en clair.
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param(
  [string]$CsvPath = "C:\Scripts\Activite9\Users-Source.csv",
  [string]$ReportPath = "C:\Scripts\Activite9\Create-Users-Report.csv",
  [string]$DomainSuffix = "corp.local",
  [string]$UserOu = "OU=Utilisateurs,DC=corp,DC=local"
)

Import-Module ActiveDirectory

function New-TemporaryPassword {
  $Length = 16
  $Chars = "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789!*-_"
  $Random = [System.Security.Cryptography.RandomNumberGenerator]::Create()
  $Bytes = New-Object byte[] $Length
  $Random.GetBytes($Bytes)

  $Password = -join ($Bytes | ForEach-Object { $Chars[$_ % $Chars.Length] })
  ConvertTo-SecureString $Password -AsPlainText -Force
}

$Users = Import-Csv -Path $CsvPath
$Report = @()

foreach ($User in $Users) {
  $Status = "Pending"
  $Message = ""

  try {
    $Login = $User.Login.Trim()
    $Group = $User.Groupe.Trim()
    $DisplayName = "$($User.Prenom.Trim()) $($User.Nom.Trim())"
    $UserPrincipalName = "$Login@$DomainSuffix"

    $ExistingUser = Get-ADUser -Filter "SamAccountName -eq '$Login'" -ErrorAction SilentlyContinue
    $ExistingGroup = Get-ADGroup -Identity $Group -ErrorAction SilentlyContinue

    if (-not $ExistingGroup) {
      throw "Groupe introuvable : $Group"
    }

    if ($ExistingUser) {
      $Status = "Skipped"
      $Message = "Utilisateur deja existant"
    }
    else {
      $TemporaryPassword = New-TemporaryPassword

      if ($PSCmdlet.ShouldProcess($Login, "Creation utilisateur AD et ajout au groupe $Group")) {
        New-ADUser `
          -Name $DisplayName `
          -GivenName $User.Prenom `
          -Surname $User.Nom `
          -SamAccountName $Login `
          -UserPrincipalName $UserPrincipalName `
          -DisplayName $DisplayName `
          -Path $UserOu `
          -AccountPassword $TemporaryPassword `
          -Enabled $true `
          -ChangePasswordAtLogon $true `
          -Description "Service $($User.Service)"

        Add-ADGroupMember -Identity $Group -Members $Login
      }

      $Status = "Created"
      $Message = "Compte cree et ajoute au groupe $Group"
    }
  }
  catch {
    $Status = "Error"
    $Message = $_.Exception.Message
  }

  $Report += [PSCustomObject]@{
    Prenom  = $User.Prenom
    Nom     = $User.Nom
    Login   = $User.Login
    Service = $User.Service
    Groupe  = $User.Groupe
    Statut  = $Status
    Message = $Message
  }
}

$Report | Export-Csv -Path $ReportPath -NoTypeInformation -Encoding UTF8
$Report
