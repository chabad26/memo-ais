# Administrer OpenLDAP avec LDAP Account Manager

## Objectif

Installer LDAP Account Manager (LAM) dans un conteneur Docker Compose et le connecter au serveur OpenLDAP déjà déployé.

LAM est une interface Web d'administration. Il facilite la consultation et la modification des entrées LDAP, mais il ne remplace pas le serveur OpenLDAP ni les commandes de vérification.

## Spécifications

- Travail individuel.
- Utiliser Docker Compose.
- Conserver le mot de passe LAM dans un fichier local non versionné.
- Utiliser le réseau Docker partagé avec OpenLDAP.
- Ne pas exposer directement le mot de passe LDAP dans la documentation publique.

## 1. Vérifier le serveur OpenLDAP

Le serveur OpenLDAP doit être démarré avant LAM.

~~~bash
cd ~/on-premise/openldap
docker compose ps
docker network ls
docker network inspect openldap_default
~~~

Le réseau openldap_default doit exister et le conteneur OpenLDAP doit être actif.

Vérifier également que le serveur répond :

~~~bash
docker compose exec openldap ldapwhoami \
  -x \
  -H ldap://localhost:3890 \
  -D "cn=admin,dc=embedded,dc=local" \
  -W
~~~

## 2. Créer le répertoire LAM

~~~bash
mkdir -p ~/on-premise/ldap-account-manager
cd ~/on-premise/ldap-account-manager
~~~

Créer les fichiers locaux :

~~~bash
touch compose.yaml .env .env.example .gitignore
printf '%s\n' '.env' > .gitignore
~~~

## 3. Préparer les variables

Le fichier .env contient le mot de passe de l'interface LAM et les paramètres de connexion à OpenLDAP. Il ne doit pas être ajouté à Git.

Contenu de .env :

~~~dotenv
LAM_PASSWORD=ChangeMe-LAM-2026
LDAP_SERVER=ldap://openldap:3890
LDAP_DOMAIN=embedded.local
LDAP_BASE_DN=dc=embedded,dc=local
LDAP_USERS_DN=ou=People,dc=embedded,dc=local
LDAP_GROUPS_DN=ou=Groups,dc=embedded,dc=local
LDAP_ADMIN_USER=cn=admin,dc=embedded,dc=local
~~~

Le fichier .env.example ne contient pas la valeur réelle du mot de passe :

~~~dotenv
LAM_PASSWORD=<mot-de-passe-interface-lam>
LDAP_SERVER=ldap://openldap:3890
LDAP_DOMAIN=embedded.local
LDAP_BASE_DN=dc=embedded,dc=local
LDAP_USERS_DN=ou=People,dc=embedded,dc=local
LDAP_GROUPS_DN=ou=Groups,dc=embedded,dc=local
LDAP_ADMIN_USER=cn=admin,dc=embedded,dc=local
~~~

Différence entre les deux mots de passe :

| Paramètre | Utilisation |
| --- | --- |
| LAM_PASSWORD | Protège l'accès au profil de configuration LAM. |
| Mot de passe LDAP | Authentifie le compte cn=admin auprès d'OpenLDAP. |

## 4. Créer le Compose

Contenu de compose.yaml :

~~~yaml
services:
  lam:
    image: ghcr.io/ldapaccountmanager/lam:9.6
    container_name: lam
    hostname: lam.embedded.local
    restart: unless-stopped
    environment:
      LAM_PASSWORD: "${LAM_PASSWORD}"
      LAM_LANG: fr_FR
      LDAP_SERVER: "${LDAP_SERVER}"
      LDAP_DOMAIN: "${LDAP_DOMAIN}"
      LDAP_BASE_DN: "${LDAP_BASE_DN}"
      LDAP_USERS_DN: "${LDAP_USERS_DN}"
      LDAP_GROUPS_DN: "${LDAP_GROUPS_DN}"
      LDAP_ADMIN_USER: "${LDAP_ADMIN_USER}"
    ports:
      - "8081:80"
    networks:
      - openldap_default

networks:
  openldap_default:
    external: true
~~~

Le réseau est déclaré external car il a été créé par le projet OpenLDAP. LAM utilise le nom du conteneur openldap comme nom DNS Docker.

Afficher la configuration résolue :

~~~bash
docker compose config
~~~

Vérifier que le mot de passe n'est pas enregistré dans une capture ou un fichier public.

## 5. Démarrer LAM

~~~bash
docker compose up -d
docker compose ps
docker compose logs lam
~~~

Résultat attendu :

- le conteneur lam est Up ;
- le port 8081 est publié ;
- le conteneur lam est connecté au réseau openldap_default.

![Conteneur LAM démarré et journaux Apache consultables](../../assets/img/integration-distribuee-on-premise/it-2/LDAP%20Account%20Manager%20create.png)

La capture conserve la preuve du téléchargement de l'image, du démarrage du conteneur et de la consultation des journaux LAM.

Ouvrir l'interface dans un navigateur :

~~~text
http://localhost:8081
~~~

## 6. Se connecter à LAM

Dans l'interface :

1. ouvrir le profil de configuration LAM ;
2. utiliser le mot de passe défini par LAM_PASSWORD ;
3. vérifier que le serveur LDAP est ldap://openldap:3890 ;
4. vérifier que la base est dc=embedded,dc=local ;
5. vérifier que le compte administrateur est cn=admin,dc=embedded,dc=local ;
6. enregistrer la configuration ;
7. se connecter avec le DN administrateur OpenLDAP et son mot de passe.

Le mot de passe LAM et le mot de passe LDAP sont distincts.

![Interface LDAP Account Manager accessible après connexion](../../assets/img/integration-distribuee-on-premise/it-2/LDAP%20Account%20Manager%20connexion%20ok.png)

La capture confirme l'accès à l'interface Web LAM avec le compte d'administration.

LAM peut afficher le message suivant lors de la première connexion :

~~~text
Les suffixes suivants sont absent du LDAP :
ou=People,dc=embedded,dc=local
ou=Groups,dc=embedded,dc=local
~~~

Ce message est attendu : les unités organisationnelles prévues par la conception LDAP n'ont pas encore été créées. Accepter la création proposée par LAM, puis vérifier leur présence dans l'arborescence.

Les deux entrées attendues sont :

- `ou=People,dc=embedded,dc=local` pour les utilisateurs ;
- `ou=Groups,dc=embedded,dc=local` pour les groupes.

Vérifier ensuite avec :

~~~bash
docker compose exec openldap ldapsearch \
  -x \
  -H ldap://localhost:3890 \
  -D "cn=admin,dc=embedded,dc=local" \
  -W \
  -b "dc=embedded,dc=local" \
  "(|(ou=People)(ou=Groups))"
~~~

![Recherche LDAP réussie des unités People et Groups](../../assets/img/integration-distribuee-on-premise/it-2/Ldap%20ok.png)

La capture confirme que les deux unités organisationnelles existent dans l'annuaire et que la recherche retourne le résultat `Success`.

## 7. Vérifier les fonctions d'administration

Dans LAM :

1. parcourir la base dc=embedded,dc=local ;
2. vérifier la présence de l'entrée principale ;
3. créer une unité organisationnelle de test, par exemple ou=Tests ;
4. modifier sa description ;
5. enregistrer la modification ;
6. vérifier l'objet avec une recherche LDAP en ligne de commande.

Exemple de vérification :

~~~bash
docker compose exec openldap ldapsearch \
  -x \
  -H ldap://localhost:3890 \
  -D "cn=admin,dc=embedded,dc=local" \
  -W \
  -b "dc=embedded,dc=local" \
  "(ou=Tests)"
~~~

Après le test, supprimer l'objet de test si aucune activité ne doit le conserver.

## 8. Vérifier la communication entre les conteneurs

Depuis le conteneur LAM, vérifier la résolution du nom OpenLDAP :

~~~bash
docker compose exec lam getent hosts openldap
~~~

Depuis le conteneur OpenLDAP, vérifier la présence des deux conteneurs sur le réseau :

~~~bash
docker network inspect openldap_default
~~~

## 9. Arrêter et redémarrer LAM

~~~bash
docker compose stop
docker compose start
docker compose ps
docker compose logs lam
~~~

LAM est une interface d'administration reconstructible. Les données LDAP restent stockées dans les volumes du projet OpenLDAP.

## Questions

### Quels paramètres sont nécessaires pour établir une connexion LDAP ?

Il faut notamment :

- l'adresse et le port du serveur LDAP ;
- le protocole utilisé, par exemple ldap ou ldaps ;
- la base DN ;
- le DN du compte de connexion ;
- le mot de passe ;
- les unités contenant les utilisateurs et les groupes ;
- les paramètres TLS si une connexion sécurisée est utilisée.

### Quels avantages présente une interface graphique ?

Une interface graphique :

- facilite la lecture de l'arborescence ;
- limite les erreurs de syntaxe LDIF ;
- permet de rechercher et modifier rapidement une entrée ;
- rend l'administration accessible à des personnes moins habituées aux commandes LDAP ;
- fournit une représentation visuelle des attributs et des objets.

### Dans quels cas les commandes LDAP restent-elles utiles ?

Les commandes restent utiles pour :

- vérifier objectivement le fonctionnement du serveur ;
- automatiser des créations ou des contrôles ;
- intégrer LDAP dans des scripts ;
- diagnostiquer un problème de connexion ;
- exporter ou sauvegarder des entrées ;
- disposer d'une méthode d'administration lorsque l'interface Web est indisponible.

## Livrables

Conserver :

- compose.yaml ;
- .env.example ;
- .gitignore ;
- les paramètres de connexion sans les secrets ;
- les captures de l'interface Web ;
- la preuve de connexion ;
- la création et la modification d'un objet ;
- les commandes ldapsearch utilisées ;
- une note sur le réseau Docker et l'architecture.

## Architecture du déploiement

~~~text
Navigateur
    |
    | http://localhost:8081
    v
LAM
    |
    | réseau Docker openldap_default
    | ldap://openldap:3890
    v
OpenLDAP
    |
    +-- ldap_data
    +-- ldap_config
    +-- ldap_backups
~~~

## Points de sécurité

- ne pas publier .env ;
- ne pas utiliser les mots de passe de laboratoire en production ;
- ne pas exposer LAM sur Internet sans HTTPS et contrôle d'accès ;
- privilégier LDAPS ou un réseau interne de confiance pour un environnement réel ;
- conserver les commandes LDAP comme moyen de vérification indépendant de LAM.

## Ressources

- [LDAP Account Manager](https://www.ldap-account-manager.org/)
- [Conteneur LDAP Account Manager](https://github.com/LDAPAccountManager/docker/pkgs/container/lam)

## Notions acquises

- LDAP Account Manager ;
- administration LDAP par interface Web ;
- réseau Docker inter-conteneurs ;
- paramètres de connexion LDAP ;
- complémentarité entre interface graphique et ligne de commande.
