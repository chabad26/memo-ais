# Activité 4 - Organiser Active Directory avec OU, utilisateurs et groupes

## Objectif de l'activité

Cette activité sert à créer une première arborescence Active Directory propre dans le domaine `corp.local`.

L'objectif est de :

- créer les OU principales ;
- créer des utilisateurs de test ;
- créer des groupes globaux ;
- affecter les utilisateurs aux groupes ;
- renseigner des descriptions ;
- éviter les conteneurs par défaut.

## Vue d'ensemble

| Élément | Valeur |
| --- | --- |
| Domaine | `corp.local` |
| OU à créer | `Utilisateurs`, `Groupes`, `Ordinateurs`, `Serveurs`, `Administration` |
| Utilisateurs | `user.rh1`, `user.rh2`, `user.it1` |
| Groupes globaux | `GG_RH`, `GG_IT`, `GG_ADMIN` |
| Méthode principale | PowerShell |

## Preuve de travail à remettre

**Premier annuaire de l'entreprise**

| Critère du formateur | Éléments apportés dans cette activité |
| --- | --- |
| Arborescence LDAP adaptée à l'organisation | OU `Utilisateurs`, `Groupes`, `Ordinateurs`, `Serveurs` et `Administration` dans `corp.local`. |
| OU, groupes et utilisateurs créés conformément au besoin | Comptes `user.rh1`, `user.rh2`, `user.it1` et groupes `GG_RH`, `GG_IT`, `GG_ADMIN`. |
| Conventions de nommage cohérentes | Préfixe `user.` pour les comptes, préfixe `GG_` pour les groupes globaux et noms d'OU explicites. |
| Annuaire vérifié par les outils d'administration | PowerShell Active Directory et console `dsa.msc`. |
| Annuaire vérifié par recherche LDAP | Recherche `Get-ADObject -LDAPFilter` et lecture de `RootDSE` avec `ldp.exe`. |

Pièces à remettre :

- capture de l'arborescence dans `dsa.msc` ;
- capture ou export PowerShell des OU, utilisateurs et groupes ;
- journal `C:\Activite4-Organisation-AD.txt` ;
- sortie de recherche LDAP montrant les objets créés.

!!! warning "Points de vigilance"
    Éviter les conteneurs par défaut comme `Users` et `Computers` pour l'organisation courante. Éviter aussi les droits directs aux utilisateurs : on passe par des groupes.

## Étape 1 - Se connecter au contrôleur de domaine

Se connecter à `SRV-AD01` avec un compte administrateur du domaine.

Depuis une session PowerShell distante :

```powershell
Enter-PSSession -ComputerName SRV-AD01 -Credential CORP\Administrateur
```

Vérifier le domaine :

```powershell
Get-ADDomain
```

Définir une variable pour le DN du domaine :

```powershell
$DomainDN = "DC=corp,DC=local"
```

## Étape 2 - Démarrer le journal PowerShell

Créer une preuve des commandes :

```powershell
Start-Transcript -Path "C:\Activite4-Organisation-AD.txt"
```

## Étape 3 - Créer les OU principales

Créer les OU demandées :

```powershell
New-ADOrganizationalUnit -Name "Utilisateurs" -Path $DomainDN -Description "Comptes utilisateurs du domaine"
New-ADOrganizationalUnit -Name "Groupes" -Path $DomainDN -Description "Groupes de sécurité globaux"
New-ADOrganizationalUnit -Name "Ordinateurs" -Path $DomainDN -Description "Postes clients joints au domaine"
New-ADOrganizationalUnit -Name "Serveurs" -Path $DomainDN -Description "Serveurs membres du domaine"
New-ADOrganizationalUnit -Name "Administration" -Path $DomainDN -Description "Comptes et groupes d'administration"
```

Vérifier :

```powershell
Get-ADOrganizationalUnit -Filter * -SearchBase $DomainDN |
  Select-Object Name, DistinguishedName
```

Point de contrôle :

- les cinq OU existent à la racine du domaine ;
- les descriptions sont renseignées.

## Étape 4 - Créer les groupes globaux

Créer les groupes dans l'OU `Groupes` :

```powershell
$GroupPath = "OU=Groupes,$DomainDN"

New-ADGroup `
  -Name "GG_RH" `
  -SamAccountName "GG_RH" `
  -GroupScope Global `
  -GroupCategory Security `
  -Path $GroupPath `
  -Description "Groupe global des utilisateurs du service RH"

New-ADGroup `
  -Name "GG_IT" `
  -SamAccountName "GG_IT" `
  -GroupScope Global `
  -GroupCategory Security `
  -Path $GroupPath `
  -Description "Groupe global des utilisateurs du service informatique"

New-ADGroup `
  -Name "GG_ADMIN" `
  -SamAccountName "GG_ADMIN" `
  -GroupScope Global `
  -GroupCategory Security `
  -Path $GroupPath `
  -Description "Groupe global des comptes d'administration"
```

Vérifier :

```powershell
Get-ADGroup -Filter 'Name -like "GG_*"' -Properties Description |
  Select-Object Name, GroupScope, GroupCategory, Description
```

## Étape 5 - Créer les utilisateurs

Définir un mot de passe temporaire :

```powershell
$Password = Read-Host "Mot de passe temporaire des utilisateurs" -AsSecureString
```

!!! warning "Complexité du mot de passe"
    Le mot de passe doit respecter la stratégie du domaine : longueur minimale, complexité, historique. Exemple de mot de passe de labo acceptable : `Azerty123!` ou `Formation2026!`.

Créer les utilisateurs dans l'OU `Utilisateurs`. Cette version peut être relancée : si l'utilisateur existe déjà, elle met à jour sa description, son mot de passe et son état.

```powershell
$UserPath = "OU=Utilisateurs,$DomainDN"

$Users = @(
  @{ Sam = "user.rh1"; Name = "user.rh1"; UPN = "user.rh1@corp.local"; Description = "Utilisateur RH 1" }
  @{ Sam = "user.rh2"; Name = "user.rh2"; UPN = "user.rh2@corp.local"; Description = "Utilisateur RH 2" }
  @{ Sam = "user.it1"; Name = "user.it1"; UPN = "user.it1@corp.local"; Description = "Utilisateur IT 1" }
)

foreach ($User in $Users) {
  $ExistingUser = Get-ADUser -Filter "SamAccountName -eq '$($User.Sam)'" -ErrorAction SilentlyContinue

  if (-not $ExistingUser) {
    New-ADUser `
      -Name $User.Name `
      -SamAccountName $User.Sam `
      -UserPrincipalName $User.UPN `
      -Path $UserPath `
      -AccountPassword $Password `
      -Enabled $true `
      -ChangePasswordAtLogon $true `
      -Description $User.Description
  }
  else {
    Set-ADUser `
      -Identity $User.Sam `
      -Description $User.Description `
      -UserPrincipalName $User.UPN `
      -Enabled $true `
      -ChangePasswordAtLogon $true

    Set-ADAccountPassword `
      -Identity $User.Sam `
      -NewPassword $Password `
      -Reset
  }
}
```

Vérifier :

```powershell
Get-ADUser -Filter 'SamAccountName -like "user.*"' -Properties Description |
  Select-Object SamAccountName, Enabled, Description, DistinguishedName
```

## Étape 6 - Affecter les utilisateurs aux groupes

Affecter les utilisateurs RH :

```powershell
Add-ADGroupMember -Identity "GG_RH" -Members "user.rh1","user.rh2"
```

Affecter l'utilisateur IT :

```powershell
Add-ADGroupMember -Identity "GG_IT" -Members "user.it1"
```

Ajouter `user.it1` au groupe d'administration de test si demandé :

```powershell
Add-ADGroupMember -Identity "GG_ADMIN" -Members "user.it1"
```

Vérifier les membres :

```powershell
Get-ADGroupMember "GG_RH" | Select-Object Name, SamAccountName
Get-ADGroupMember "GG_IT" | Select-Object Name, SamAccountName
Get-ADGroupMember "GG_ADMIN" | Select-Object Name, SamAccountName
```

## Étape 7 - Vérifier l'arborescence AD

Afficher les OU :

```powershell
Get-ADOrganizationalUnit -Filter * -SearchBase $DomainDN |
  Sort-Object DistinguishedName |
  Select-Object Name, DistinguishedName
```

Afficher les objets créés :

```powershell
Get-ADUser -Filter 'SamAccountName -like "user.*"' -Properties Description |
  Select-Object SamAccountName, Description, DistinguishedName

Get-ADGroup -Filter 'Name -like "GG_*"' -Properties Description |
  Select-Object Name, Description, DistinguishedName
```

Depuis un poste avec RSAT, ouvrir :

```powershell
dsa.msc
```

Capture attendue :

- OU `Utilisateurs` ;
- OU `Groupes` ;
- OU `Ordinateurs` ;
- OU `Serveurs` ;
- OU `Administration` ;
- utilisateurs dans la bonne OU ;
- groupes dans la bonne OU.

## Étape 8 - Vérifier l'annuaire avec une recherche LDAP

La console Active Directory vérifie l'administration graphique. Une recherche LDAP permet de vérifier que les objets sont réellement présents dans l'annuaire selon leur `distinguishedName` et leurs attributs.

Depuis PowerShell sur `SRV-AD01`, rechercher les OU créées :

```powershell
Get-ADObject `
  -LDAPFilter "(&(objectCategory=organizationalUnit)(|(ou=Utilisateurs)(ou=Groupes)(ou=Ordinateurs)(ou=Serveurs)(ou=Administration)))" `
  -SearchBase $DomainDN `
  -Properties description |
  Select-Object Name, DistinguishedName, Description
```

Rechercher les utilisateurs de l'entreprise :

```powershell
Get-ADObject `
  -LDAPFilter "(&(objectCategory=person)(objectClass=user)(sAMAccountName=user.*))" `
  -SearchBase "OU=Utilisateurs,$DomainDN" `
  -Properties sAMAccountName,description |
  Select-Object Name, SamAccountName, DistinguishedName, Description
```

Rechercher les groupes globaux :

```powershell
Get-ADObject `
  -LDAPFilter "(&(objectCategory=group)(name=GG_*))" `
  -SearchBase "OU=Groupes,$DomainDN" `
  -Properties groupType,description |
  Select-Object Name, DistinguishedName, Description
```

Vérifier également l'annuaire avec l'outil graphique LDAP :

```powershell
ldp.exe
```

Dans `ldp.exe` :

1. sélectionner `Connection > Connect` vers `SRV-AD01` sur le port `389` ;
2. sélectionner `Connection > Bind` avec le compte administrateur du domaine ;
3. sélectionner `Browse > Search` avec la base `DC=corp,DC=local` ;
4. utiliser un filtre comme `(objectClass=organizationalUnit)` ou `(sAMAccountName=user.rh1)` ;
5. conserver une capture du résultat retourné.

Résultats attendus :

- les OU retournées possèdent un `distinguishedName` cohérent ;
- les utilisateurs sont placés dans `OU=Utilisateurs` ;
- les groupes sont placés dans `OU=Groupes` ;
- la recherche LDAP retourne `user.rh1`, `user.rh2`, `user.it1`, `GG_RH`, `GG_IT` et `GG_ADMIN`.

## Étape 9 - Option avancée : structure Tier 0 / Tier 1 / Tier 2

Le Tiering Model consiste à séparer les comptes et ressources d'administration par niveau de criticité.

Résumé :

| Tier | Contenu typique |
| --- | --- |
| Tier 0 | Active Directory, contrôleurs de domaine, identités critiques |
| Tier 1 | Serveurs applicatifs et serveurs métiers |
| Tier 2 | Postes utilisateurs et support de proximité |

Créer une OU `Tiering` :

```powershell
New-ADOrganizationalUnit -Name "Tiering" -Path $DomainDN -Description "Structure d'administration par tiers"
```

Créer les sous-OU :

```powershell
$TierRoot = "OU=Tiering,$DomainDN"

New-ADOrganizationalUnit -Name "Tier0" -Path $TierRoot -Description "Tier 0 - Identités et contrôleurs de domaine"
New-ADOrganizationalUnit -Name "Tier1" -Path $TierRoot -Description "Tier 1 - Serveurs"
New-ADOrganizationalUnit -Name "Tier2" -Path $TierRoot -Description "Tier 2 - Postes utilisateurs"
```

Créer des comptes d'administration séparés :

```powershell
$AdminPassword = Read-Host "Mot de passe temporaire des comptes admin tier" -AsSecureString

New-ADUser -Name "adm.t0.olivier" -SamAccountName "adm.t0.olivier" -UserPrincipalName "adm.t0.olivier@corp.local" -Path "OU=Tier0,$TierRoot" -AccountPassword $AdminPassword -Enabled $true -ChangePasswordAtLogon $true -Description "Compte admin Tier 0"
New-ADUser -Name "adm.t1.olivier" -SamAccountName "adm.t1.olivier" -UserPrincipalName "adm.t1.olivier@corp.local" -Path "OU=Tier1,$TierRoot" -AccountPassword $AdminPassword -Enabled $true -ChangePasswordAtLogon $true -Description "Compte admin Tier 1"
New-ADUser -Name "adm.t2.olivier" -SamAccountName "adm.t2.olivier" -UserPrincipalName "adm.t2.olivier@corp.local" -Path "OU=Tier2,$TierRoot" -AccountPassword $AdminPassword -Enabled $true -ChangePasswordAtLogon $true -Description "Compte admin Tier 2"
```

!!! warning "Important"
    Ces comptes ne suffisent pas à sécuriser l'AD. Il faudra ensuite ajouter les GPO, restrictions de connexion et délégations adaptées.

## Étape 10 - Arrêter le journal PowerShell

```powershell
Stop-Transcript
```

Vérifier :

```powershell
Get-ChildItem C:\Activite4-Organisation-AD.txt
```

## Livrables et preuves attendues

Convention de nommage :

```text
[Nom]-[Prénom]-[Site]-Activite4-[NomLivrable]
```

Livrable :

| Livrable | Preuve attendue | Exemple |
| --- | --- | --- |
| Capture arborescence AD | OU, utilisateurs et groupes visibles | `Nom-Prenom-Site-Activite4-ArborescenceAD.png` |
| Journal PowerShell | Commandes de création | `Nom-Prenom-Site-Activite4-JournalCommandes.txt` |

## Exemples de preuves

OU principales créées à la racine du domaine :

![OU principales](<../../assets/img/admin-windows/it-2/OU principales.png>)

Utilisateurs créés dans l'OU `Utilisateurs` :

![Utilisateurs Active Directory](<../../assets/img/admin-windows/it-2/Users.png>)

Groupes globaux créés dans l'OU `Groupes` :

![Groupes globaux](<../../assets/img/admin-windows/it-2/groupes globaux.png>)

Affectation des utilisateurs aux groupes :

![Affectation utilisateurs groupes](<../../assets/img/admin-windows/it-2/affectations users groups.png>)

## Checklist finale

- [ ] OU `Utilisateurs` créée.
- [ ] OU `Groupes` créée.
- [ ] OU `Ordinateurs` créée.
- [ ] OU `Serveurs` créée.
- [ ] OU `Administration` créée.
- [ ] Utilisateurs `user.rh1`, `user.rh2`, `user.it1` créés.
- [ ] Groupes `GG_RH`, `GG_IT`, `GG_ADMIN` créés.
- [ ] Utilisateurs affectés aux bons groupes.
- [ ] Descriptions renseignées.
- [ ] Capture arborescence AD réalisée.
- [ ] Option Tier 0 / Tier 1 / Tier 2 réalisée si demandée.

## Ressource

- IT-Connect - Active Directory : les fondamentaux du Tiering Model : <https://www.it-connect.fr/active-directory-tiering-model-les-fondamentaux/>
