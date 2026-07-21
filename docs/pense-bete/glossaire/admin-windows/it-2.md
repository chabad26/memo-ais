# Glossaire Administration Windows — Itération 2

## Sujet

Organisation Active Directory, poste client, GPO, BitLocker et Windows LAPS.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| OU | Unité d'organisation servant à classer les objets AD et cibler les GPO. |
| Groupe global | Groupe regroupant généralement les utilisateurs d'un même rôle métier. |
| GPO | Ensemble centralisé de paramètres appliqués aux utilisateurs ou ordinateurs. |
| `gpupdate` | Commande qui actualise l'application des stratégies de groupe. |
| BitLocker | Chiffrement des volumes Windows avec possibilité d'archiver la clé dans AD. |
| Windows LAPS | Gestion automatique d'un mot de passe administrateur local unique par machine. |
| Tiering | Séparation des niveaux d'administration pour limiter les mouvements d'un attaquant. |

## Manipulations faites

| Manipulation | Commandes ou actions |
| --- | --- |
| Structurer AD | Créer OU, utilisateurs et groupes, puis affecter les membres. |
| Joindre un client | Intégrer `POSTE-01` au domaine et tester l'ouverture de session. |
| Appliquer des GPO | Mot de passe, panneau de configuration et déploiement de 7-Zip. |
| Protéger les postes | Configurer BitLocker et sauvegarder les informations de récupération dans AD. |
| Gérer l'administrateur local | Déployer Windows LAPS et contrôler la récupération autorisée du secret. |

## Docs associées

- [Vue d'ensemble](../../../admin-windows/it-2/index.md)
- [OU, utilisateurs et groupes](../../../admin-windows/it-2/activite4-organisation-ou-utilisateurs-groupes.md)
- [Joindre Windows 11 au domaine](../../../admin-windows/it-2/activite5-joindre-poste-windows11-domaine.md)
- [GPO et déploiement logiciel](../../../admin-windows/it-2/activite6-gpo-password-panel-deploiement-7zip.md)
- [BitLocker](../../../admin-windows/it-2/activite6bis-gpo-bitlocker-recuperation-ad.md)
- [Windows LAPS](../../../admin-windows/it-2/activite6ter-windows-laps.md)

