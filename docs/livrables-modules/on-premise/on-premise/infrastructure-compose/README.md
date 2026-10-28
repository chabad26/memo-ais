# Stack OpenLDAP et LDAP Account Manager


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/infrastructure-compose/README.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


Le rôle détaillé des fichiers est décrit dans
[`../documentation/technical-files-guide.md`](../documentation/technical-files-guide.md).

Ce dossier fournit un Compose commun pour démarrer OpenLDAP et LDAP Account
Manager avec le même réseau Docker, les mêmes volumes LDAP et les mêmes
paramètres de connexion.

## Préparer les paramètres

Créer le fichier local `.env` à partir du modèle :

```bash
cd ~/on-premise/infrastructure-compose
cp .env.example .env
```

[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
reste local et est exclu de Git.

Le réseau partagé doit exister avant le premier démarrage :

```bash
docker network create openldap_default 2>/dev/null || true
```

Sur une machine neuve, créer également les volumes persistants avant le
démarrage :

```bash
docker volume create openldap_ldap_data
docker volume create openldap_ldap_config
docker volume create openldap_ldap_backups
```

## Démarrer le stack

```bash
docker compose config
docker compose up -d
docker compose ps
```

OpenLDAP est accessible sur `ldap://localhost:389` et LAM sur
`http://localhost:8081`.

## Vérifier le fonctionnement

```bash
docker compose logs openldap
docker compose logs lam
docker compose exec openldap ldapwhoami -x \
  -H ldap://localhost:3890 \
  -D "cn=admin,dc=embedded,dc=local" -W
docker compose exec lam getent hosts openldap
```

Dans LAM, utiliser le serveur `openldap`, le port interne `3890`, la base
`dc=embedded,dc=local` et le compte administrateur indiqué dans `.env`.

## Arrêter et redémarrer

```bash
docker compose stop
docker compose start
docker compose ps
```

Pour recréer les conteneurs sans supprimer les données :

```bash
docker compose down
docker compose up -d
```

Ne pas utiliser `docker compose down -v` : cela supprimerait les volumes
`ldap_data`, `ldap_config` et `ldap_backups`.

## Compatibilité avec les anciens Compose

Les fichiers `openldap/compose.yaml` et
`ldap-account-manager/compose.yaml` restent disponibles pour les déploiements
unitaires. Ne pas démarrer simultanément deux projets qui publient les mêmes
ports ou utilisent les mêmes noms de conteneurs.

Le serveur Samba utilise lui aussi le réseau `openldap_default`. Pour démarrer
le stack complet, lancer d'abord ce Compose, puis `samba-ad/compose.yaml`.

Les volumes utilisés portent les noms historiques `openldap_ldap_data`,
`openldap_ldap_config` et `openldap_ldap_backups` afin de réutiliser les
données créées par le Compose OpenLDAP unitaire.
