# Glossaire Administration Windows — Itération 1

## Sujet

Plateforme LABO, Hyper-V, Windows Server Core, AD DS et DNS.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Hyper-V | Hyperviseur Microsoft permettant de créer et administrer des machines virtuelles. |
| vSwitch externe | Commutateur virtuel reliant les VMs au réseau physique. |
| Server Core | Installation Windows Server minimale, sans bureau graphique complet. |
| AD DS | Service d'annuaire centralisant identités, groupes et ressources du domaine. |
| Contrôleur de domaine | Serveur qui héberge AD DS et authentifie les comptes du domaine. |
| DNS | Service de résolution de noms indispensable au fonctionnement d'Active Directory. |
| DSRM | Mode de restauration des services d'annuaire, protégé par un mot de passe dédié. |
| Windows Admin Center | Interface web d'administration des serveurs Windows et d'Hyper-V. |

## Manipulations faites

| Manipulation | Commandes ou actions |
| --- | --- |
| Préparer LABO | Nom, réseau, accès distant, Windows Admin Center et rôle Hyper-V. |
| Créer `SRV-AD01` | VM Server Core, ressources, disque et connexion au vSwitch externe. |
| Préparer le serveur | IP fixe, DNS, renommage et installation des rôles AD DS/DNS. |
| Créer le domaine | Promotion de `SRV-AD01` en contrôleur du domaine `corp.local`. |

## Docs associées

- [Vue d'ensemble](../../../admin-windows/it-1/index.md)
- [Installer LABO, Hyper-V et SRV-AD01](../../../admin-windows/it-1/activite1-installation-labo-hyperv-srv-ad01.md)
- [Préparer AD DS et DNS](../../../admin-windows/it-1/activite2-preparer-srv-ad01-ad-ds-dns.md)
- [Promouvoir le contrôleur de domaine](../../../admin-windows/it-1/activite3-promouvoir-srv-ad01-controleur-domaine.md)

