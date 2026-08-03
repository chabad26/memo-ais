# Déployer un serveur OpenLDAP avec Docker Compose

## Objectif

Déployer un serveur OpenLDAP dans un conteneur Docker avec Docker Compose, puis vérifier son fonctionnement et la persistance de ses données après un redémarrage.

Cette activité utilise la génération v2 de l'image osixia/openldap indiquée sur Docker Hub.

!!! warning "Version de l'image et variables"
    La génération v2 utilise `OPENLDAP_BOOTSTRAP_ORGANIZATION` et `OPENLDAP_BOOTSTRAP_SUFFIX`. Elle utilise les chemins `/var/lib/openldap/openldap-data` et `/etc/openldap/slapd.d`, ainsi que le port interne `3890` par défaut. Le port `389` de la machine hôte est redirigé vers ce port interne.

## Spécifications

- Travail individuel.
- Utiliser Docker Compose.
- Conserver les données LDAP dans des volumes Docker.
- Séparer les paramètres sensibles des fichiers partageables.
- Les mots de passe utilisés sont réservés à l'environnement de travaux pratiques.

## 1. Créer le répertoire de travail

~~~bash
mkdir -p ~/on-premise/openldap
cd ~/on-premise/openldap
~~~

Le projet sera organisé ainsi :

~~~text
openldap/
├── compose.yaml
├── .env
├── .env.example
└── .gitignore
~~~

## 2. Préparer les paramètres d'environnement

Créer le fichier local .env :

~~~bash
touch .env
~~~

Ajouter les paramètres de laboratoire :

~~~dotenv
OPENLDAP_BOOTSTRAP_ORGANIZATION=Embedded Solutions
OPENLDAP_BOOTSTRAP_SUFFIX=dc=embedded,dc=local
OPENLDAP_BOOTSTRAP_TLS=false
~~~

Paramètres utilisés :

| Variable | Rôle |
| --- | --- |
| OPENLDAP_BOOTSTRAP_ORGANIZATION | Nom de l'organisation affiché par l'annuaire. |
| OPENLDAP_BOOTSTRAP_SUFFIX | Base DN de l'annuaire. |
| OPENLDAP_BOOTSTRAP_TLS | Désactive TLS pendant le premier test du laboratoire. |

La génération v2 crée les mots de passe administrateur si les valeurs hachées ne sont pas fournies et les affiche dans les journaux de démarrage. Retrouvez la valeur générée avec :

~~~bash
docker compose logs openldap | grep -iE 'password|generated|admin'
~~~

Conservez la valeur générée dans les notes locales de laboratoire, sans la publier dans Git. Pour un déploiement reproductible, fournissez plutôt les variables hachées `OPENLDAP_BOOTSTRAP_DATA_ROOT_PASSWORD_HASHED` et `OPENLDAP_BOOTSTRAP_CONFIG_ROOT_PASSWORD_HASHED` avant le premier démarrage.

Le fichier `.env` contient la configuration locale et ne doit pas être ajouté au dépôt Git.

Créer le modèle partageable :

~~~bash
touch .env.example
~~~

Contenu de .env.example :

~~~dotenv
OPENLDAP_BOOTSTRAP_ORGANIZATION=Embedded Solutions
OPENLDAP_BOOTSTRAP_SUFFIX=dc=embedded,dc=local
OPENLDAP_BOOTSTRAP_TLS=false
~~~

Créer .gitignore :

~~~bash
printf '%s\n' '.env' > .gitignore
~~~

Vérifier les fichiers cachés :

~~~bash
ls -la
~~~

## 3. Créer le fichier Compose

Créer compose.yaml :

~~~bash
touch compose.yaml
~~~

Ajouter la définition du service :

~~~yaml
services:
  openldap:
    image: osixia/openldap:2.6.10-alpha
    container_name: openldap
    hostname: ldap.embedded.local
    restart: unless-stopped
    environment:
      OPENLDAP_BOOTSTRAP_ORGANIZATION: ${OPENLDAP_BOOTSTRAP_ORGANIZATION}
      OPENLDAP_BOOTSTRAP_SUFFIX: ${OPENLDAP_BOOTSTRAP_SUFFIX}
      OPENLDAP_BOOTSTRAP_TLS: ${OPENLDAP_BOOTSTRAP_TLS}
    ports:
      - "389:3890"
    volumes:
      - ldap_data:/var/lib/openldap/openldap-data
      - ldap_config:/etc/openldap/slapd.d
      - ldap_backups:/var/lib/openldap/openldap-backups

volumes:
  ldap_data:
  ldap_config:
  ldap_backups:
~~~

Points importants :

| Élément | Rôle |
| --- | --- |
| osixia/openldap:2.6.10-alpha | Image v2 du serveur OpenLDAP utilisée pour le TP. |
| OPENLDAP_BOOTSTRAP_SUFFIX | Base DN de l'annuaire. |
| 389:3890 | Port LDAP publié sur le port 389 de la machine hôte et le port 3890 du conteneur. |
| ldap_data | Conserve les données de l'annuaire. |
| ldap_config | Conserve la configuration et le schéma LDAP. |
| ldap_backups | Conserve les sauvegardes OpenLDAP. |
| restart: unless-stopped | Redémarre le service après un redémarrage Docker ou système. |

Les répertoires `/var/lib/openldap/openldap-data`, `/etc/openldap/slapd.d` et `/var/lib/openldap/openldap-backups` sont utilisés pour conserver les données, la configuration et les sauvegardes OpenLDAP en dehors du conteneur.

## 4. Vérifier la configuration Compose

Affichez la configuration résolue :

~~~bash
docker compose config
~~~

Cette commande peut afficher les valeurs chargées depuis .env. Ne partagez pas sa sortie sans masquer les mots de passe.

Vérifiez les volumes déclarés :

~~~bash
docker compose config --volumes
~~~

Résultat attendu :

~~~text
ldap_data
ldap_config
~~~

## 5. Démarrer le serveur OpenLDAP

Démarrez le service en arrière-plan :

~~~bash
docker compose up -d
~~~

Affichez son état :

~~~bash
docker compose ps
docker ps
~~~

Le conteneur openldap doit être démarré et les ports 389 et 636 doivent être publiés.

Consultez les journaux :

~~~bash
docker compose logs openldap
~~~

!!! note "Démarrage initial"
    Le premier démarrage peut prendre quelques secondes, voire quelques minutes selon la machine. Tant que les journaux restent sur `Init new ldap server...`, le service n'est pas encore prêt. Si une commande renvoie `Can't contact LDAP server`, attendez la fin de l'initialisation puis recommencez le test. Au-delà de cinq minutes sans nouveau message, considérez le démarrage comme bloqué et appliquez le diagnostic ci-dessous.

### Diagnostiquer un démarrage qui semble bloqué

Ne lancez pas immédiatement `docker compose down -v`. Commencez par vérifier l'état du conteneur et suivez les journaux :

~~~bash
docker compose ps
docker inspect -f '{{.State.Status}} - exit={{.State.ExitCode}}' openldap
docker compose logs -f openldap
docker compose exec openldap ps -ef
docker compose exec openldap ss -lntp
~~~

Le conteneur doit rester dans l'état `running` et les journaux doivent finalement indiquer que `slapd` est démarré. Arrêtez le suivi avec `Ctrl+C`, puis relancez `ldapwhoami`.

Si `ps -ef` montre encore `dpkg-reconfigure ... slapd` et que `ss -lntp` ne montre pas les ports `389` ou `636`, le serveur LDAP n'est pas démarré. Conservez cette sortie comme preuve de l'incident avant de réinitialiser le déploiement.

Si le conteneur est arrêté ou si l'initialisation reste bloquée après plusieurs minutes, conservez les journaux et vérifiez d'abord les ressources disponibles :

~~~bash
docker compose ps -a
docker system df
docker volume ls
~~~

Dans un environnement de travaux pratiques où aucune donnée LDAP n'a encore été créée, une réinitialisation des volumes peut être envisagée après validation par le formateur. Cette opération supprime définitivement les données stockées dans les volumes :

~~~bash
docker compose down -v
docker compose up -d
docker compose logs -f openldap
~~~

Ne réalisez pas cette dernière procédure après la création de comptes ou de groupes sans sauvegarde préalable.

## 6. Vérifier la base DN et le compte administrateur

La variable `OPENLDAP_BOOTSTRAP_SUFFIX` vaut `dc=embedded,dc=local`.

~~~text
dc=embedded,dc=local
~~~

Vérifiez que le serveur répond avec ldapwhoami :

~~~bash
docker compose exec openldap ldapwhoami \
  -x \
  -D "cn=admin,dc=embedded,dc=local" \
  -W
~~~

Saisissez le mot de passe administrateur généré et affiché dans les journaux du premier démarrage.

Résultat attendu :

~~~text
dn:cn=admin,dc=embedded,dc=local
~~~

## 7. Rechercher le contenu de l'annuaire

Recherchez toutes les entrées de la base :

~~~bash
docker compose exec openldap ldapsearch \
  -x \
  -H ldap://localhost:3890 \
  -D "cn=admin,dc=embedded,dc=local" \
  -W \
  -b "dc=embedded,dc=local" \
  "(objectClass=*)"
~~~

Recherchez uniquement la base de l'organisation :

~~~bash
docker compose exec openldap ldapsearch \
  -x \
  -H ldap://localhost:3890 \
  -D "cn=admin,dc=embedded,dc=local" \
  -W \
  -b "dc=embedded,dc=local" \
  -s base \
  "(objectClass=*)"
~~~

Les résultats doivent montrer au minimum l'entrée de base et les informations de l'organisation.

## 8. Vérifier les volumes Docker

Affichez les volumes du projet :

~~~bash
docker volume ls
~~~

Inspectez les volumes :

~~~bash
docker volume inspect openldap_ldap_data
docker volume inspect openldap_ldap_config
~~~

Le nom réel peut être préfixé par le nom du répertoire Compose. Utilisez docker compose config --volumes et docker volume ls pour confirmer le nom exact.

Vérifiez que les volumes sont montés dans le conteneur :

~~~bash
docker inspect openldap
~~~

Repérez les montages vers :

~~~text
/var/lib/openldap/openldap-data
/etc/openldap/slapd.d
/var/lib/openldap/openldap-backups
~~~

## 9. Redémarrer le conteneur

Redémarrez le service :

~~~bash
docker compose restart openldap
~~~

Vérifiez son état et ses journaux :

~~~bash
docker compose ps
docker compose logs --tail=50 openldap
~~~

Testez à nouveau l'authentification :

~~~bash
docker compose exec openldap ldapwhoami \
  -x \
  -D "cn=admin,dc=embedded,dc=local" \
  -W
~~~

Puis relancez une recherche :

~~~bash
docker compose exec openldap ldapsearch \
  -x \
  -H ldap://localhost:3890 \
  -D "cn=admin,dc=embedded,dc=local" \
  -W \
  -b "dc=embedded,dc=local" \
  "(objectClass=*)"
~~~

La base DN et l'entrée administrateur doivent toujours être présentes.

## 10. Vérifier la persistance après recréation

Pour vérifier que les données ne dépendent pas uniquement du conteneur, supprimez et recréez le conteneur sans supprimer les volumes :

~~~bash
docker compose down
docker compose up -d
~~~

Vérifiez les volumes :

~~~bash
docker compose config --volumes
docker volume ls
~~~

Vérifiez à nouveau l'annuaire :

~~~bash
docker compose exec openldap ldapsearch \
  -x \
  -H ldap://localhost:3890 \
  -D "cn=admin,dc=embedded,dc=local" \
  -W \
  -b "dc=embedded,dc=local" \
  "(objectClass=*)"
~~~

!!! warning "Ne pas supprimer les volumes"
    N'exécutez pas docker compose down -v pendant cette vérification. L'option -v supprimerait ldap_data et ldap_config avec les données et la configuration de l'annuaire.

## 11. Vérifier la connectivité depuis l'hôte

Vérifiez que les ports sont en écoute :

~~~bash
ss -lnt | grep -E ':(389|636)'
~~~

Depuis l'hôte, si les outils LDAP sont installés :

~~~bash
ldapsearch \
  -x \
  -H ldap://localhost:3890 \
  -D "cn=admin,dc=embedded,dc=local" \
  -W \
  -b "dc=embedded,dc=local" \
  -s base \
  "(objectClass=*)"
~~~

Le test démontre que le service est accessible via le port publié par Docker.

## 12. Répondre aux questions

### Quel est le rôle d'un Distinguished Name (DN) ?

Le DN est le chemin complet et unique d'une entrée dans l'annuaire. Il indique à la fois l'identité de l'entrée et son emplacement dans l'arborescence.

Exemple :

~~~text
cn=admin,dc=embedded,dc=local
~~~

### Quelle différence existe entre un DN et un UID ?

Le DN identifie l'entrée de manière complète dans l'arborescence. L'UID est un attribut court utilisé pour identifier un utilisateur, par exemple alice.martin.

Un UID peut être recherché dans l'annuaire, mais il ne décrit pas à lui seul l'emplacement complet de l'entrée.

### Pourquoi utilise-t-on des volumes Docker ?

Les volumes stockent les données en dehors de la couche éphémère du conteneur. Ils permettent de supprimer ou recréer un conteneur sans perdre la base LDAP ni sa configuration.

### Pourquoi Docker Compose facilite-t-il l'administration de plusieurs services ?

Compose rassemble dans un fichier les images, variables, ports, volumes, réseaux et politiques de redémarrage. Les services peuvent ensuite être démarrés, arrêtés, consultés et recréés avec des commandes cohérentes.

## Livrables à conserver

Dans ~/on-premise/openldap/ :

- compose.yaml ;
- .env.example ;
- .gitignore ;
- la liste des paramètres utilisés ;
- les sorties ou captures de docker compose ps ;
- les journaux du démarrage ;
- la sortie de ldapwhoami ;
- la sortie de ldapsearch ;
- la preuve de présence des volumes après redémarrage.

Le fichier .env peut être conservé localement pour le TP, mais il ne doit pas être ajouté au dépôt Git.

## État final vérifiable

- le conteneur openldap est démarré ;
- la base DN est dc=embedded,dc=local ;
- le compte admin répond à ldapwhoami ;
- ldapsearch retourne la base de l'annuaire ;
- les ports 389 et 636 sont publiés ;
- ldap_data et ldap_config existent ;
- les données restent présentes après docker compose restart ;
- les données restent présentes après docker compose down puis docker compose up -d ;
- aucun secret n'est présent dans un fichier partageable.

## Ressources

- [osixia/container-openldap — dépôt GitHub](https://github.com/osixia/container-openldap)
- [Guide de démarrage OpenLDAP du projet](https://github.com/osixia/container-openldap#quick-start)
- [Documentation Docker Compose](https://docs.docker.com/compose/)

## Notions acquises

- OpenLDAP
- Docker Compose
- Base DN
- Distinguished Name
- UID
- ldapwhoami
- ldapsearch
- Volumes persistants
- Persistance après recréation d'un conteneur
