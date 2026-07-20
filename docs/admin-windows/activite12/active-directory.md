# Active Directory : OU, comptes et groupes

## Inventaire constaté

L'export du **10 juillet 2026 à 13:37** recense :

- 9 utilisateurs, comptes intégrés compris ;
- 58 groupes, groupes intégrés compris ;
- 46 relations d'appartenance ;
- 3 ordinateurs ;
- 6 unités d'organisation.

## Organisation des OU

| OU | Contenu et finalité |
| --- | --- |
| `Domain Controllers` | `SRV-AD01` et les futurs contrôleurs de domaine |
| `Utilisateurs` | Comptes utilisateurs métiers |
| `Groupes` | Groupes globaux et locaux de domaine |
| `Ordinateurs` | `POSTE-01` et futurs postes clients |
| `Serveurs` | `SRV-FIC01` et futurs serveurs membres |
| `Administration` | Comptes et groupes d'administration dédiés |

![OU principales dans Active Directory](<../../assets/img/admin-windows/it-2/OU principales.png>)

**Contexte :** cette vue contrôle l'arborescence utilisée pour cibler les GPO et déléguer l'administration.

## Comptes métiers constatés

| Compte | État | OU | Groupe(s) métier |
| --- | --- | --- | --- |
| `user.rh1` | Actif | Utilisateurs | `GG_RH` |
| `user.rh2` | Actif | Utilisateurs | `GG_RH` |
| `user.it1` | Actif | Utilisateurs | `GG_IT`, `GG_ADMIN` |
| `user.rh3` — Alice Martin | Actif | Utilisateurs | `GG_RH` |
| `user.it2` — Bruno Durand | Actif | Utilisateurs | `GG_IT` |
| `user.rh4` — Claire Bernard | Actif | Utilisateurs | `GG_RH` |

Les comptes intégrés `Invité` et `krbtgt` apparaissent désactivés dans l'export. Le compte `Administrateur` reste privilégié et doit être réservé aux opérations nécessitant réellement ce niveau de droit.

## Groupes fonctionnels

| Groupe | Portée | Fonction |
| --- | --- | --- |
| `GG_RH` | Globale | Comptes du service RH |
| `GG_IT` | Globale | Comptes du service IT |
| `GG_ADMIN` | Globale | Administration déléguée |
| `DL_RH_RW` | Locale de domaine | Modification de la ressource RH |
| `DL_IT_RW` | Locale de domaine | Modification de la ressource IT |
| `DL_COMMUN_RW` | Locale de domaine | Modification de la ressource COMMUN |

## Cycle de vie recommandé

1. Créer le compte nominatif dans l'OU appropriée.
2. L'affecter à un groupe global métier.
3. Ne jamais attribuer directement une ACL de dossier à un utilisateur.
4. Désactiver immédiatement un compte lors d'un départ.
5. Retirer les appartenances sensibles et archiver selon la politique interne.
6. Supprimer seulement après validation et expiration de la conservation.

## Commandes d'inventaire

```powershell
Get-ADOrganizationalUnit -Filter * -Properties Description
Get-ADUser -Filter * -Properties Enabled,MemberOf
Get-ADGroup -Filter * -Properties GroupScope,GroupCategory
Get-ADComputer -Filter * -Properties OperatingSystem,Enabled
Get-ADGroupMember GG_RH
Get-ADGroupMember GG_IT
```

