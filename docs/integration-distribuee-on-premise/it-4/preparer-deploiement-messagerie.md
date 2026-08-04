# Préparer le déploiement de la messagerie

## Objectif

Préparer les fichiers nécessaires au futur déploiement de Postfix, Dovecot et
Roundcube sans démarrer de conteneur.

## 1. Créer l'arborescence

Dans le dépôt de travail :

```bash
cd ~/on-premise
mkdir -p messaging-compose/{postfix,dovecot,roundcube}
cd messaging-compose
```

L'arborescence préparée est :

```text
messaging-compose/
├── docker-compose.yml
├── .env
├── .env.example
├── .gitignore
├── README.md
├── postfix/
├── dovecot/
└── roundcube/
```

Les répertoires de configuration sont préparés mais ne contiennent pas encore
les fichiers définitifs du guide de déploiement.

## 2. Préparer le fichier Compose

Le fichier `docker-compose.yml` décrit quatre services :

| Service | Fonction | Données persistantes |
| --- | --- | --- |
| `db` | Base MariaDB dédiée à Roundcube | `roundcube_db` |
| `postfix` | SMTP et soumission | `postfix_spool` |
| `dovecot` | IMAP, authentification et livraison LMTP | `dovecot_mail` |
| `roundcube` | Webmail | `roundcube_config` |

Postfix et Dovecot rejoignent le réseau externe `openldap_default` afin de
consulter l'annuaire existant. Les quatre services rejoignent aussi le réseau
interne `mail_default`.

## 3. Préparer les paramètres

Créer le fichier local à partir du modèle :

```bash
cd ~/on-premise/messaging-compose
cp .env.example .env
```

Les paramètres à renseigner sont :

| Variable | Rôle |
| --- | --- |
| `POSTFIX_IMAGE` | Image du service Postfix à valider avec le guide |
| `DOVECOT_IMAGE` | Image du service Dovecot à valider avec le guide |
| `ROUNDCUBE_IMAGE` | Version de l'image Roundcube |
| `MAIL_HOSTNAME` | Nom complet du serveur de messagerie |
| `MAIL_DOMAIN` | Domaine utilisé dans les adresses |
| `ROUNDCUBE_PORT` | Port Web publié sur l'hôte |
| `LDAP_URI` | Adresse du serveur OpenLDAP sur le réseau Docker |
| `LDAP_BASE_DN` | Base de recherche LDAP |
| `LDAP_BIND_DN` | Compte technique de lecture LDAP |
| `LDAP_BIND_PASSWORD` | Secret du compte technique LDAP |
| `ROUNDCUBE_DB_NAME` | Nom de la base Roundcube |
| `ROUNDCUBE_DB_USER` | Utilisateur de la base Roundcube |
| `ROUNDCUBE_DB_PASSWORD` | Mot de passe de la base Roundcube |
| `MARIADB_ROOT_PASSWORD` | Mot de passe administrateur MariaDB |

Le fichier `.env` est local et ne doit pas être ajouté à Git. Le fichier
`.env.example` contient uniquement les noms et exemples de paramètres.

## 4. Identifier les volumes

Les volumes seront créés par Docker lors du déploiement :

- `postfix_spool` conserve les files et l'état Postfix ;
- `dovecot_mail` conserve les boîtes et les index ;
- `roundcube_db` conserve la base de données du Webmail ;
- `roundcube_config` conserve la configuration Roundcube.

Les volumes de messagerie devront être sauvegardés avec les configurations
Postfix, Dovecot, Roundcube et le fichier `.env` protégé.

## 5. Vérifier sans démarrer

Pendant cette activité, seules les commandes de contrôle de configuration sont
autorisées :

```bash
cd ~/on-premise/messaging-compose
docker compose --env-file .env.example config
docker compose --env-file .env.example config --quiet
```

Ne pas exécuter `docker compose up` avant la séance de déploiement.

La commande `config` doit afficher les quatre services, les quatre volumes,
les réseaux `mail_default` et `openldap_default`, ainsi que les ports prévus.

## Points à faire valider

- les images Postfix et Dovecot retenues par le guide ;
- le compte technique LDAP et ses droits minimaux ;
- la présence du schéma LDAP nécessaire aux attributs de messagerie ;
- le domaine de messagerie et les enregistrements DNS ;
- le choix des certificats TLS ;
- la politique de sauvegarde des quatre volumes.

## Livrables

Conserver dans le dépôt :

- `messaging-compose/docker-compose.yml` ;
- `messaging-compose/.env.example` ;
- `messaging-compose/.gitignore` ;
- `messaging-compose/README.md` ;
- les répertoires `postfix/`, `dovecot/` et `roundcube/` ;
- la liste des paramètres et des volumes persistants.
