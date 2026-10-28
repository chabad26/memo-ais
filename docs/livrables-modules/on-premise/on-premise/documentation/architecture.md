# Architecture du projet


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/architecture.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.


## Contexte

L'entreprise conçoit et intègre des logiciels embarqués. Les équipes de développement, d'intégration et de validation utilisent des outils partagés pour produire, tester et documenter les livrables.

L'équipe infrastructure conserve les configurations et les scripts dans un espace organisé et versionné avec Git.

## Organisation logique

~~~text
Entreprise
├── Développement embarqué
├── Intégration et validation
├── Infrastructure
├── Administration
└── Documentation technique
~~~

## Services déployés pendant l'itération

- une image Ubuntu contenant l'outil figlet ;
- un serveur Web Nginx dans un conteneur ;
- une application WordPress ;
- une base MariaDB associée à WordPress ;
- un volume Docker pour conserver les données MariaDB ;
- un dépôt Git local pour suivre la documentation et les scripts.

## Organisation des fichiers

~~~text
~/on-premise/
├── documentation/
├── dockerfile-demo/
├── nginx-demo/
└── wordpress-compose/
~~~

Le fichier wordpress-compose/.env contient les paramètres locaux et reste exclu du dépôt Git. Le fichier .env.example documente les variables nécessaires sans exposer les valeurs utilisées.

## Principes retenus

- séparer les sources, la configuration et la documentation ;
- utiliser un volume pour les données persistantes ;
- utiliser un nom de service Docker comme nom DNS ;
- vérifier chaque déploiement avec des commandes et des captures ;
- enregistrer les évolutions dans Git.

## Services LDAP ajoutés pendant l'itération 2

L'annuaire de laboratoire est déployé avec OpenLDAP et administré avec LDAP
Account Manager :

~~~text
OpenLDAP
├── base DN : dc=embedded,dc=local
├── ou=People
├── ou=Groups
├── ou=Services
└── ou=Computers
        ▲
        │ réseau Docker openldap_default
        │
LDAP Account Manager (LAM)
~~~

OpenLDAP reste le service de référence. LAM fournit l'interface Web
d'administration et peut être reconstruit sans remplacer les données LDAP.

## Organisation actuelle du dépôt

~~~text
~/on-premise/
├── documentation/
│   ├── architecture.md
│   ├── inventory.md
│   ├── users.md
│   ├── journal.md
│   ├── commands.md
│   ├── PCA.md
│   └── PRA.md
├── dockerfile-demo/
├── nginx-demo/
├── wordpress-compose/
├── openldap/
├── ldap-account-manager/
├── samba-ad/
├── samba-ldap/
└── infrastructure-compose/
~~~

Les fichiers `.env` contenant des paramètres locaux restent exclus du dépôt.
Seuls les modèles `.env.example` sont versionnés.

## Architecture actuelle Samba et OpenLDAP

Le serveur Samba autonome `samba-ldap` utilise OpenLDAP sur le réseau Docker
externe `openldap_default`. OpenLDAP conserve les identités et les groupes ;
Samba fournit les sessions SMB et les espaces de partage.

| Partage | Groupe principal |
|---|---|
| `Commun` | groupes de service autorisés |
| `Developpement` | `grp-developpement` |
| `Bureau-etudes` | `grp-bureau-etudes` |
| `Administration` | `grp-administration` |

Le contrôleur AD historique est conservé dans `samba-ad/compose.ad.yaml` et
n'est pas démarré avec le serveur Samba LDAP actuel.

Le dossier `infrastructure-compose/` fournit un démarrage commun validé pour
OpenLDAP et LDAP Account Manager. Samba reste dans son propre Compose car il
possède son image, son état et son cycle de redémarrage.

## Architecture de la messagerie

Le schéma détaillé, le tableau des services et les flux validés sont conservés
dans `documentation/mail-architecture.md`. La messagerie réutilise OpenLDAP
comme source d'identités et sépare les rôles Postfix, Dovecot et Roundcube.
