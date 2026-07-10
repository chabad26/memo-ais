# Activité 6ter - Windows LAPS pour les mots de passe administrateur locaux

## Mise en situation

L'entreprise interdit le même mot de passe administrateur local sur tous les postes.

Chaque poste doit avoir un secret unique, renouvelé régulièrement et récupérable uniquement par les administrateurs autorisés. Windows LAPS permet de gérer automatiquement le mot de passe du compte administrateur local sur les postes joints au domaine.

## Objectif de l'activité

Cette activité sert à déployer Windows LAPS sur `POSTE-01`.

L'objectif est de :

- vérifier la présence des commandes LAPS ;
- mettre à jour le schéma Active Directory si nécessaire ;
- déléguer les droits d'écriture LAPS aux ordinateurs de l'OU `Ordinateurs` ;
- créer et lier `GPO-LAPS` ;
- configurer `System > LAPS` ;
- sauvegarder le mot de passe dans Active Directory ;
- imposer longueur 14, complexité élevée et expiration 30 jours ;
- forcer le traitement LAPS sur `POSTE-01` ;
- récupérer le secret depuis `SRV-AD01` ;
- documenter l'intérêt de LAPS.

## Vue d'ensemble

| Élément | Valeur |
| --- | --- |
| Domaine | `corp.local` |
| Contrôleur de domaine | `SRV-AD01` |
| Poste cible | `POSTE-01` |
| OU cible | `OU=Ordinateurs,DC=corp,DC=local` |
| GPO | `GPO-LAPS` |
| Sauvegarde | Active Directory |
| Longueur | `14` caractères |
| Complexité | élevée |
| Expiration | `30` jours |

!!! warning "Windows LAPS, pas legacy LAPS"
    Windows LAPS est intégré aux versions modernes de Windows. Ne pas installer l'ancien package MSI Microsoft LAPS sur Windows 11 récent, sauf consigne explicite.

## Étape 1 - Vérifier les commandes LAPS

Sur `SRV-AD01`, ouvrir PowerShell en administrateur.

Vérifier les commandes disponibles :

```powershell
Get-Command *Laps*
```

Commandes attendues :

```text
Update-LapsADSchema
Set-LapsADComputerSelfPermission
Get-LapsADPassword
Invoke-LapsPolicyProcessing
```

Si aucune commande n'apparaît, vérifier que le serveur est à jour et que Windows LAPS est présent.

## Étape 2 - Démarrer le journal PowerShell

Sur `SRV-AD01` :

```powershell
Start-Transcript -Path "C:\Activite6ter-Windows-LAPS.txt"
```

Définir les variables :

```powershell
$DomainDN = "DC=corp,DC=local"
$ComputerOU = "OU=Ordinateurs,$DomainDN"
$GpoName = "GPO-LAPS"
```

## Étape 3 - Mettre à jour le schéma AD si nécessaire

Vérifier si les attributs Windows LAPS existent :

```powershell
Get-ADObject `
  -SearchBase (Get-ADRootDSE).SchemaNamingContext `
  -LDAPFilter "(lDAPDisplayName=msLAPS-PasswordExpirationTime)" `
  -ErrorAction SilentlyContinue
```

Si aucun résultat n'est retourné, mettre à jour le schéma :

```powershell
Update-LapsADSchema -Verbose
```

!!! warning "Opération forêt"
    `Update-LapsADSchema` est une opération à faire une seule fois par forêt Active Directory.

Vérifier après mise à jour :

```powershell
Get-ADObject `
  -SearchBase (Get-ADRootDSE).SchemaNamingContext `
  -LDAPFilter "(lDAPDisplayName=msLAPS-PasswordExpirationTime)" |
  Select-Object Name, ObjectClass
```

## Étape 4 - Déléguer les permissions à OU=Ordinateurs

Les postes doivent pouvoir écrire leur mot de passe LAPS dans leur objet ordinateur.

Sur `SRV-AD01` :

```powershell
Set-LapsADComputerSelfPermission -Identity $ComputerOU
```

Vérifier les droits étendus :

```powershell
Find-LapsADExtendedRights -Identity $ComputerOU
```

Point de contrôle :

- les ordinateurs de l'OU peuvent mettre à jour leurs attributs LAPS ;
- seuls les administrateurs autorisés doivent pouvoir lire le secret.

## Étape 5 - Créer GPO-LAPS

Créer la GPO :

```powershell
New-GPO -Name $GpoName -Comment "Windows LAPS - mot de passe administrateur local unique par poste"
```

Lier la GPO à `OU=Ordinateurs` :

```powershell
New-GPLink `
  -Name $GpoName `
  -Target $ComputerOU `
  -LinkEnabled Yes
```

Vérifier :

```powershell
Get-GPInheritance -Target $ComputerOU
```

## Étape 6 - Configurer System > LAPS

### Méthode A - GPMC si disponible

Depuis un poste avec RSAT/GPMC :

```text
gpmc.msc
```

Modifier `GPO-LAPS`, puis aller dans :

```text
Configuration ordinateur
Stratégies
Modèles d'administration
Système
LAPS
```

Configurer :

| Paramètre | Valeur |
| --- | --- |
| Backup Directory | Active Directory |
| Password Length | `14` |
| Password Complexity | complexité élevée |
| Password Age Days | `30` |

### Méthode B - PowerShell par valeurs de stratégie

Si GPMC n'est pas disponible, configurer les valeurs de stratégie Windows LAPS dans la GPO.

Chemin de stratégie Windows LAPS :

```powershell
$LapsPolicyKey = "HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\LAPS"
```

Sauvegarder dans Active Directory :

```powershell
Set-GPRegistryValue `
  -Name $GpoName `
  -Key $LapsPolicyKey `
  -ValueName "BackupDirectory" `
  -Type DWord `
  -Value 2
```

Configurer longueur 14 :

```powershell
Set-GPRegistryValue `
  -Name $GpoName `
  -Key $LapsPolicyKey `
  -ValueName "PasswordLength" `
  -Type DWord `
  -Value 14
```

Configurer complexité élevée :

```powershell
Set-GPRegistryValue `
  -Name $GpoName `
  -Key $LapsPolicyKey `
  -ValueName "PasswordComplexity" `
  -Type DWord `
  -Value 4
```

Configurer expiration 30 jours :

```powershell
Set-GPRegistryValue `
  -Name $GpoName `
  -Key $LapsPolicyKey `
  -ValueName "PasswordAgeDays" `
  -Type DWord `
  -Value 30
```

Vérifier :

```powershell
Get-GPRegistryValue -Name $GpoName -Key $LapsPolicyKey
```

Valeurs importantes :

| Valeur | Signification |
| --- | --- |
| `BackupDirectory = 2` | Sauvegarde vers Windows Server Active Directory |
| `PasswordLength = 14` | Mot de passe de 14 caractères |
| `PasswordComplexity = 4` | Majuscules, minuscules, chiffres, caractères spéciaux |
| `PasswordAgeDays = 30` | Renouvellement tous les 30 jours |

## Étape 7 - Appliquer la GPO sur POSTE-01

Sur `POSTE-01`, PowerShell en administrateur :

```powershell
gpupdate /force
```

Vérifier que la GPO s'applique :

```powershell
gpresult /r
```

## Étape 8 - Forcer le traitement Windows LAPS

Sur `POSTE-01`, vérifier les commandes LAPS :

```powershell
Get-Command *Laps*
```

Forcer le traitement de la stratégie :

```powershell
Invoke-LapsPolicyProcessing
```

Vérifier les événements LAPS :

```powershell
Get-WinEvent -LogName "Microsoft-Windows-LAPS/Operational" -MaxEvents 10 |
  Select-Object TimeCreated, Id, ProviderName, Message
```

Point de contrôle :

- un événement indique que le mot de passe a été sauvegardé dans Active Directory ;
- le poste ne doit pas afficher d'erreur de stratégie.

## Étape 9 - Récupérer le mot de passe depuis SRV-AD01

Sur `SRV-AD01`, récupérer le secret :

```powershell
Get-LapsADPassword POSTE-01 -AsPlainText
```

Résultat attendu :

```text
ComputerName        : POSTE-01
Account             : Administrator
Password            : **************
ExpirationTimestamp : ...
Source              : ...
```

!!! danger "Masquer le secret"
    Pour la capture, masquer le champ `Password`. Le formateur doit voir que la récupération fonctionne, pas le secret en clair.

Version de preuve sans afficher le mot de passe :

```powershell
Get-LapsADPassword POSTE-01 |
  Select-Object ComputerName, Account, PasswordUpdateTime, ExpirationTimestamp, Source
```

## Étape 10 - Documenter l'intérêt de LAPS

Windows LAPS apporte plusieurs bénéfices :

- chaque poste possède un mot de passe administrateur local unique ;
- le secret est renouvelé automatiquement ;
- un mot de passe compromis sur un poste ne donne pas accès aux autres postes ;
- la récupération est centralisée dans Active Directory ;
- les accès au secret sont contrôlés par les permissions AD ;
- cela limite les attaques par réutilisation de mot de passe et les déplacements latéraux.

## Dépannage rapide

### Get-Command *Laps* ne retourne rien

Vérifier la version de Windows et les mises à jour.

Windows LAPS est disponible nativement sur les systèmes récents et mis à jour. Ne pas confondre avec l'ancien Microsoft LAPS.

### Le schéma semble déjà à jour

Si la commande suivante retourne un objet, ne pas relancer inutilement le schéma :

```powershell
Get-ADObject `
  -SearchBase (Get-ADRootDSE).SchemaNamingContext `
  -LDAPFilter "(lDAPDisplayName=msLAPS-PasswordExpirationTime)"
```

### Aucun mot de passe n'est récupéré

Sur `POSTE-01` :

```powershell
gpupdate /force
Invoke-LapsPolicyProcessing
```

Puis vérifier le journal :

```powershell
Get-WinEvent -LogName "Microsoft-Windows-LAPS/Operational" -MaxEvents 20 |
  Select-Object TimeCreated, Id, Message
```

Sur `SRV-AD01`, vérifier que `POSTE-01` est bien dans l'OU ciblée :

```powershell
Get-ADComputer POSTE-01 -Properties DistinguishedName |
  Select-Object Name, DistinguishedName
```

### Accès refusé avec Get-LapsADPassword

Par défaut, les administrateurs du domaine peuvent lire le secret.

Pour déléguer la lecture à un groupe dédié :

```powershell
Set-LapsADReadPasswordPermission `
  -Identity $ComputerOU `
  -AllowedPrincipals "CORP\GG_ADMIN"
```

## Livrables et preuves attendues

Convention de nommage :

```text
[Nom]-[Prénom]-[Site]-Activite6ter-[NomLivrable]
```

Livrables :

| Livrable | Preuve attendue | Exemple |
| --- | --- | --- |
| Capture GPO-LAPS | Paramètres LAPS ou valeurs de stratégie | `Nom-Prenom-Site-Activite6ter-GPO-LAPS.png` |
| Capture récupération | `Get-LapsADPassword`, secret masqué | `Nom-Prenom-Site-Activite6ter-RecuperationLAPS.png` |
| Journal PowerShell | Commandes exécutées | `Nom-Prenom-Site-Activite6ter-JournalCommandes.txt` |
| Note courte | Intérêt de LAPS | `Nom-Prenom-Site-Activite6ter-InteretLAPS.md` |

## Exemples de preuves

Traitement LAPS opérationnel côté `POSTE-01` :

![LAPS OK côté client](<../../assets/img/admin-windows/it-2/LAPS OK Coté client.png>)

Récupération du mot de passe LAPS depuis `SRV-AD01` :

![LAPS OK côté serveur](<../../assets/img/admin-windows/it-2/LAPS OK coté serveur.png>)

!!! danger "Masquage obligatoire"
    Masquer la valeur du champ `Password` avant remise du livrable. Le but est de prouver que la récupération fonctionne, pas d'exposer le secret.

## Checklist finale

- [ ] `Get-Command *Laps*` vérifié.
- [ ] Schéma mis à jour si nécessaire.
- [ ] `Set-LapsADComputerSelfPermission` appliqué sur `OU=Ordinateurs`.
- [ ] `GPO-LAPS` créée.
- [ ] `GPO-LAPS` liée à `OU=Ordinateurs`.
- [ ] Sauvegarde Active Directory configurée.
- [ ] Longueur `14` configurée.
- [ ] Complexité élevée configurée.
- [ ] Expiration `30` jours configurée.
- [ ] `gpupdate /force` exécuté sur `POSTE-01`.
- [ ] `Invoke-LapsPolicyProcessing` exécuté si nécessaire.
- [ ] `Get-LapsADPassword POSTE-01 -AsPlainText` validé.
- [ ] Secret masqué dans les captures.
- [ ] Intérêt de LAPS documenté.

## Références

- Microsoft Learn - Windows LAPS overview : <https://learn.microsoft.com/windows-server/identity/laps/laps-overview>
- Microsoft Learn - Get started with Windows LAPS and Windows Server Active Directory : <https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-scenarios-windows-server-active-directory>
- Microsoft Learn - Configure policy settings for Windows LAPS : <https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-management-policy-settings>
- IT-Connect - Configurer Windows LAPS Active Directory : <https://www.it-connect.fr/tuto-configurer-windows-laps-active-directory>
