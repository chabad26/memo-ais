# Itération 1 - Plateforme Windows et domaine

## Objectif de l'itération

Cette première itération sert à installer la plateforme de laboratoire Windows et à préparer la création du domaine Active Directory.

Le travail se fait en deux grandes étapes :

- préparer la machine **LABO** avec Windows Server et Hyper-V ;
- créer la VM **SRV-AD01**, qui deviendra ensuite le premier contrôleur de domaine.

## Architecture cible

| Élément | Rôle |
| --- | --- |
| `LABO` | Machine multifonction de l'apprenant, hôte Hyper-V |
| Hyper-V | Hyperviseur local pour créer les VM |
| Commutateur externe | Connexion réseau des VM vers le réseau physique |
| `SRV-AD01` | Futur serveur Active Directory et DNS |
| Windows Server Core | Installation minimale de `SRV-AD01` |

## Activités prévues

1. Installer et préparer la plateforme LABO.
2. Créer la VM `SRV-AD01` en version Server Core.
3. Documenter les paramètres techniques.
4. Préparer la création du domaine Active Directory.

## Livrables attendus

Les preuves doivent permettre de vérifier :

- que `LABO` est installé et configuré ;
- que Hyper-V est installé ;
- que le commutateur virtuel externe existe ;
- que la VM `SRV-AD01` est créée ;
- que les paramètres importants sont documentés.

Convention de nommage :

```text
[Nom]-[Prénom]-[Site]-Activite1-[NomLivrable]
```

Exemples :

```text
Dupont-Alice-Rouen-Activite1-FicheInstallationLABO.pdf
Dupont-Alice-Rouen-Activite1-HyperVInstalle.png
Dupont-Alice-Rouen-Activite1-VM-SRV-AD01.png
```
