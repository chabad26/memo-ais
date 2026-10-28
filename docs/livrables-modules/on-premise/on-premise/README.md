# Infrastructure on-premise


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/README.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


Ce dépôt contient les projets Docker Compose, configurations, scripts et
documents produits pendant le module.

## Comprendre les fichiers

Le document [`documentation/technical-files-guide.md`](documentation/technical-files-guide.md)
explique le rôle de chaque Compose, volume, réseau, fichier externe et script.

## Documentation d'exploitation

| Document | Usage |
|---|---|
| [`documentation/inventory.md`](documentation/inventory.md) | inventaire des services, volumes, ports et documents de référence |
| [`documentation/operations.md`](documentation/operations.md) | procédures courantes LDAP et Samba |
| [`documentation/PCA.md`](documentation/PCA.md) | continuité d'activité, services couverts, contrôles et limites |
| [`documentation/PRA.md`](documentation/PRA.md) | ordre de reprise et procédures de restauration par service |
| [`documentation/incident-majeur-ldap.md`](documentation/incident-majeur-ldap.md) | compte rendu, décisions et plan d'actions de crise LDAP |
| [`documentation/rapport-restauration-pra.md`](documentation/rapport-restauration-pra.md) | rapport d'execution PRA, services restaures, RTO et RPO observes |
| [`documentation/gestion-certificats-roundcube.md`](documentation/gestion-certificats-roundcube.md) | revocation et remplacement du certificat Roundcube compromis |
| [`documentation/retour-experience-pca-pra.md`](documentation/retour-experience-pca-pra.md) | retour d'experience simule et ameliorations PCA/PRA |
| [`documentation/backup-strategy.md`](documentation/backup-strategy.md) | fréquence, rétention, chiffrement et tests de sauvegarde |
| [`documentation/restore-procedure.md`](documentation/restore-procedure.md) | restauration BorgBackup en environnement isolé |
| [`documentation/tls-deployment.md`](documentation/tls-deployment.md) | déploiement TLS OpenLDAP, Postfix, Dovecot et Roundcube |
| [`documentation/monitoring-dashboards.md`](documentation/monitoring-dashboards.md) | tableaux de bord Kibana et réimport des objets |
| [`documentation/cloud-migration-deployment.md`](documentation/cloud-migration-deployment.md) | cible de répartition et déploiement multi-hôte OVHcloud |

## Projets principaux

| Répertoire | Fonction |
|---|---|
| `wordpress-compose/` | WordPress et MariaDB |
| `openldap/` | annuaire OpenLDAP |
| `ldap-account-manager/` | interface d'administration LDAP |
| `infrastructure-compose/` | démarrage commun OpenLDAP et LAM |
| `samba-ad/` | serveur de fichiers Samba utilisant OpenLDAP |
| `messaging-compose/` | Postfix, Dovecot, Roundcube et MariaDB |
| `backup/` | sauvegarde et contrôle BorgBackup |
| `monitoring-compose/` | Elasticsearch et Kibana |
| `pki/` | certificat racine public et éléments d'intégration de Campus CA |

Chaque projet doit être lancé depuis son propre répertoire :

```bash
cd ~/on-premise/<projet>
docker compose config
docker compose up -d
docker compose ps
docker compose logs --tail=100
```

Le fichier `.env` reste local. Le fichier `.env.example` documente les
variables nécessaires sans publier les valeurs utilisées.

## Certificats internes

La CA `Campus CA` est précédée d'un
[inventaire des certificats](documentation/certificate-inventory.md), puis
décrite dans
[`documentation/pki-architecture.md`](documentation/pki-architecture.md). Son
certificat racine public est conservé dans
`pki/certs/Campus-CA-root.crt` (`pki/certs/Campus-CA-root.crt`, conservé dans la source locale). Les clés
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]

Le déploiement effectif sur OpenLDAP, Postfix, Dovecot et Roundcube est décrit
dans [`documentation/tls-deployment.md`](documentation/tls-deployment.md).
Les procédures de renouvellement, révocation et remplacement sont dans
[`documentation/certificate-lifecycle.md`](documentation/certificate-lifecycle.md).
