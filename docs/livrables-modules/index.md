# Livrables des modules

Livrables retrouvés dans `/home/oliv/Documents/entreprise/AIS/Modules`, classés par module le **28 octobre 2026**. Les sources restent à leur emplacement d’origine. Les copies intégrées au mémo permettent de relire les documents et les fichiers techniques sans dépendre de ce chemin local.

## Catalogue

| Ensemble | Contenu |
| --- | --- |
| [Infrastructure on-premise](on-premise.md) | Architecture, annuaire, Samba, messagerie, PKI, sauvegarde, PCA/PRA, exploitation et validations. |
| [Cloud et IAM](cloud-iam.md) | Patrons OpenTofu et Ansible, inventaires et déploiement distribué. |
| [Supervision et observabilité](observabilite.md) | Stack, collecte, tableaux de bord, règles et injects pédagogiques. |
| [Audits Greenbone et Trivy](securisation.md) | Exports de rapports et configurations du laboratoire d’audit. |
| [Configurations réseau GNS3](reseaux.md) | Configurations initiales et projet du simulateur si exploitable en texte. |

## Portée des preuves

L’import rend les travaux consultables : il ne valide pas une infrastructure actuelle. Les résultats datés sont ceux des documents, les exercices simulés restent simulés, et les patrons de déploiement ne prouvent pas un déploiement. Les fiches pédagogiques existantes restent la référence de lecture contextualisée.

Les lignes susceptibles de contenir des identifiants ou des secrets sont retirées de manière conservatrice, y compris certains exemples. Les fichiers techniques sont donc des **copies de consultation**, pas une configuration directement réutilisable. Les originaux ne sont ni modifiés ni déplacés.

## Tri et conservation locale

Les doublons exacts des copies sont reliés à une seule copie par ensemble. Les variantes de contenu et les documents datés sont conservés séparément. Les historiques Git, caches fournisseurs, images disque, archives Docker, dépôts Borg, clés privées, accès cloud, états OpenTofu, fichiers d’environnement réels et listes d’identités restent locaux. Les sauvegardes intermédiaires et fichiers vides sont inventoriés sans être ajoutés au site. La copie du portfolio dans le rôle Ansible reste également locale.

[Inventaire complet du tri — JSON](../assets/files/livrables-modules/inventaire.json) : chaque fichier source, sa taille, la décision de tri et, pour les copies publiées, leur chemin et empreinte SHA-256. Les liens symboliques ne sont pas suivis comme livrables à publier.

| Décision | Nombre de fichiers |
| --- | --- |
| Configuration privée, état ou identité | 29 |
| Copie de consultation expurgée | 71 |
| Copie documentaire | 102 |
| Copie du portfolio déployé, hors livrable pédagogique de cette sélection | 21 |
| Données de travail, identités, secrets ou preuves brutes conservés localement | 61 |
| Doublon exact de la copie de consultation | 2 |
| Dépôt de sauvegarde, accès cloud privé ou dossier hors publication | 16 |
| Fichier vide | 3 |
| Image disque, archive, certificat ou autre binaire conservé localement | 66 |
| Métadonnées, cache ou dépendance générée | 925 |
| Sauvegarde intermédiaire, original conservé | 9 |

Le dossier `inject-backups` est vide au moment de l’inventaire. `cloud-iam-ovh` et les dépôts Borg sont référencés dans l’inventaire mais ne fournissent pas de copie publique.
