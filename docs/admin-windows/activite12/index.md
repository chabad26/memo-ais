# Activité 12 — Dossier d'exploitation SYS01b

## Objectif

Ce dossier rassemble l'état documenté de l'environnement Windows construit pendant les activités 1 à 11. Il doit permettre à un autre administrateur de comprendre l'architecture, vérifier les services et reprendre l'exploitation.

!!! warning "Sécurité documentaire"
    Aucun mot de passe, secret LAPS, mot de passe DSRM ou clé de récupération BitLocker n'est publié. Les captures susceptibles d'afficher un secret en clair sont volontairement exclues.

## Identification du livrable

| Champ | Valeur |
| --- | --- |
| Auteur | HIMBLOT Olivier |
| Site | Labo |
| Domaine | `corp.local` |
| Activité | Activité 12 — Dossier exploitation |
| Version | 1.0 |
| Date | 20 juillet 2026 |
| Convention | `HIMBLOT-Olivier-Labo-Activite12-Dossier-Exploitation-SYS01b` |

## Sommaire

1. [Architecture, domaine et adressage](architecture-domaine.md)
2. [Active Directory : OU, comptes et groupes](active-directory.md)
3. [GPO, BitLocker et Windows LAPS](gpo-bitlocker-laps.md)
4. [SRV-FIC01, partages et AGDLP](serveur-fichiers-agdlp.md)
5. [Shadow Copies, sauvegarde et restauration](sauvegarde-restauration.md)
6. [Scripts PowerShell et inventaire firewall](powershell-firewall.md)
7. [Supervision, reprise et points ouverts](reprise-exploitation.md)

## Sources utilisées

| Source | Utilisation |
| --- | --- |
| `docs/admin-windows/it-1` à `it-4` | Procédures et configuration de référence |
| `docs/admin-windows/it-4/AD-Inventory.html` | Inventaire AD du 10 juillet 2026 |
| `docs/assets/files/admin-windows/it-4` | Scripts, exports AD et firewall |
| `docs/assets/img/admin-windows/it-1` à `it-4` | Preuves visuelles contextualisées |

!!! info "État documenté"
    Les adresses de `SRV-AD01`, `SRV-FIC01` et `POSTE-01`, ainsi que le site Labo, ont été confirmés le 20 juillet 2026.
