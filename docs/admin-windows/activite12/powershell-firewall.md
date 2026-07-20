# Scripts PowerShell et inventaire firewall

## Scripts disponibles

| Script | Fonction | Source |
| --- | --- | --- |
| `Create-Users.ps1` | Créer des comptes depuis un CSV et produire un rapport | [Afficher le script](../../assets/files/admin-windows/it-4/Create-Users.ps1) |
| `Inventory-AD.ps1` | Exporter utilisateurs, groupes, membres, ordinateurs et OU | [Afficher le script](../../assets/files/admin-windows/it-4/Inventory-AD.ps1) |
| `Users-Source.csv` | Jeu de données source pour la création de comptes | [Afficher le CSV](../../assets/files/admin-windows/it-4/Users-Source.csv) |

## Utilisation contrôlée

```powershell
# Toujours commencer par une simulation
.\Create-Users.ps1 -CsvPath .\Users-Source.csv -WhatIf

# Puis produire un inventaire horodaté
.\Inventory-AD.ps1 -GenerateHtml

# Journaliser les opérations administratives
Start-Transcript -Path "C:\Logs\Exploitation-$(Get-Date -Format yyyyMMdd-HHmmss).txt"
# ... opérations ...
Stop-Transcript
```

!!! warning "Précautions"
    Tester sur un jeu limité, relire les chemins d'OU et les groupes, conserver `-WhatIf` lors de la première exécution et protéger les exports contenant des données d'annuaire. Aucun mot de passe définitif ne doit apparaître dans un script ou un CSV.

## Politique pare-feu

Les profils Domaine doivent rester actifs. La configuration attendue bloque le trafic entrant par défaut et autorise le trafic sortant, puis ouvre seulement les services justifiés.

### SRV-AD01 — règles constatées dans l'export

| Règle | Port / protocole | Direction | Action |
| --- | --- | --- | --- |
| `AD-DNS-TCP-53` | 53 TCP | Entrant | Autoriser |
| `AD-DNS-UDP-53` | 53 UDP | Entrant | Autoriser |
| `AD-Kerberos-TCP-88` | 88 TCP | Entrant | Autoriser |
| `AD-Kerberos-UDP-88` | 88 UDP | Entrant | Autoriser |
| `AD-LDAP-TCP-389` | 389 TCP | Entrant | Autoriser |
| `AD-LDAP-UDP-389` | 389 UDP | Entrant | Autoriser |
| `AD-LDAPS-TCP-636` | 636 TCP | Entrant | Autoriser |
| `AD-GlobalCatalog-TCP-3268-3269` | 3268-3269 TCP | Entrant | Autoriser |
| `AD-SMB-TCP-445` | 445 TCP | Entrant | Autoriser |
| `AD-RPC-TCP-135` | 135 TCP | Entrant | Autoriser |
| `AD-RDP-TCP-3389-Admin` | 3389 TCP | Entrant | Autoriser |

[Ouvrir l'export CSV SRV-AD01](../../assets/files/admin-windows/it-4/GPO-FW-SRV-AD01-Rules.csv)

### SRV-FIC01 — règles constatées dans l'export

| Règle | Port / protocole | Direction | Action |
| --- | --- | --- | --- |
| `FIC-SMB-TCP-445` | 445 TCP | Entrant | Autoriser |
| `FIC-RPC-TCP-135` | 135 TCP | Entrant | Autoriser |
| `FIC-RDP-TCP-3389-Admin` | 3389 TCP | Entrant | Autoriser |

[Ouvrir l'export CSV SRV-FIC01](../../assets/files/admin-windows/it-4/GPO-FW-SRV-FIC01-Rules.csv)

## Contrôles

```powershell
Get-NetFirewallProfile |
  Select-Object Name,Enabled,DefaultInboundAction,DefaultOutboundAction

Get-NetFirewallRule -PolicyStore "corp.local\GPO-FW-SRV-AD01" |
  Select-Object DisplayName,Enabled,Direction,Action

Test-NetConnection SRV-AD01 -Port 53
Test-NetConnection SRV-AD01 -Port 445
Test-NetConnection SRV-FIC01 -Port 445

# Contrôler également qu'un service inutile reste fermé
Test-NetConnection SRV-FIC01 -Port 80
Test-NetConnection SRV-FIC01 -Port 21
```

![Tests réseau vers SRV-FIC01](<../../assets/img/admin-windows/it-4/test SRV-FIC01.png>)

**Contexte :** les tests depuis `POSTE-01` valident l'accès aux services autorisés. Les ports inutiles doivent aussi être testés afin de prouver leur fermeture.

!!! note "Points à revalider"
    L'export CSV ne contient pas l'adresse distante autorisée pour RDP. Vérifier que la règle est limitée au réseau d'administration `10.42.0.0/24`. Valider aussi les besoins RPC dynamiques et ne conserver LDAPS 636 que si un certificat et un usage réel existent.

