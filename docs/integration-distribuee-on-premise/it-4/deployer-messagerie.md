# Déploiement de l'infrastructure de messagerie

## Objectif

Déployer les services Postfix, Dovecot, Roundcube et MariaDB dans le projet
`messaging-compose`, puis vérifier leur état, leurs réseaux et leurs volumes.

## 1. Adaptations réalisées

Le fichier préparé a nécessité deux adaptations avant le démarrage :

- le tag Roundcube `1.6-apache` n'existait pas ; il a été remplacé par
  `1.6.x-apache` ;
- l'image Postfix exigeait la variable `ALLOWED_SENDER_DOMAINS`, définie sur
  `embedded.local` ;
- l'image Dovecot `latest` utilisait une syntaxe 2.4 incompatible avec la
  configuration préparée ; le tag `dovecot/dovecot:2.3.21` a été retenu ;
- `dovecot/dovecot.conf` et `dovecot-ldap.conf.ext` ont été ajoutés dans
  `dovecot/`.

La configuration TLS n'est pas encore activée : elle fera l'objet de
l'activité de sécurisation prévue.

## 2. Démarrage

```bash
cd ~/on-premise/messaging-compose
docker compose up -d
docker compose ps
```

Services déployés :

| Conteneur | Service | Rôle |
| --- | --- | --- |
| `mail-db` | MariaDB | base Roundcube |
| `mail-postfix` | Postfix | SMTP et soumission |
| `mail-dovecot` | Dovecot | IMAP et LMTP |
| `mail-roundcube` | Roundcube | Webmail |

## 3. Vérification des journaux

```bash
docker compose logs --tail=100 db
docker compose logs --tail=100 postfix
docker compose logs --tail=100 dovecot
docker compose logs --tail=100 roundcube
```

Les journaux vérifiés montrent :

- MariaDB prête à accepter les connexions ;
- Postfix démarré et en état `healthy` ;
- Dovecot démarré sans boucle de redémarrage ;
- Roundcube configuré et servi par Apache.

## 4. Vérification de Roundcube

```bash
curl -I http://localhost:8082
```

Résultat obtenu : réponse HTTP `200 OK`.

L'interface est accessible à l'adresse :

```text
http://localhost:8082
```

## 5. Vérification des ports

```bash
docker compose ps
```

Ports publiés :

| Port | Service | État |
| ---: | --- | --- |
| 25/TCP | Postfix SMTP | publié |
| 587/TCP | Postfix submission | publié |
| 143/TCP | Dovecot IMAP | publié |
| 993/TCP | Dovecot IMAPS, TLS à finaliser | publié |
| 8082/TCP | Roundcube HTTP de laboratoire | publié |

Les certificats TLS ne sont pas encore installés. Les ports 993 et 8082
seront sécurisés lors de l'activité dédiée.

## 6. Vérification des réseaux

```bash
docker network inspect mail_default
docker network inspect openldap_default
```

Le réseau `mail_default` contient les quatre services de messagerie.
Postfix et Dovecot rejoignent également `openldap_default`, avec OpenLDAP,
LAM et Samba, afin de pouvoir atteindre l'annuaire.

## 7. Vérification de la persistance

Volumes créés :

```bash
docker volume ls | grep messaging-compose
```

- `messaging-compose_postfix_spool` ;
- `messaging-compose_dovecot_mail` ;
- `messaging-compose_roundcube_db` ;
- `messaging-compose_roundcube_config`.

Une marque de test a été écrite dans le volume Roundcube, puis les quatre
conteneurs ont été redémarrés. La marque a été retrouvée après redémarrage,
puis supprimée. La persistance du volume est donc vérifiée.

Ne jamais utiliser `docker compose down -v` pendant les tests : cette
commande supprimerait les volumes de messagerie.

## 8. État et limites

Le socle des conteneurs est opérationnel. Les tests fonctionnels d'envoi,
réception, authentification LDAP et pièce jointe sont décrits dans
`documentation/validation-mail.md`.

Restent à finaliser :

- compte technique LDAP réellement créé pour Postfix et Dovecot ;
- synchronisation complète des identités mail ;
- certificats TLS ;
- relais SMTP et DNS MX ;
- tests fonctionnels M-01 à M-07.

## Livrables

Conserver :

- `messaging-compose/docker-compose.yml` ;
- `messaging-compose/.env.example` ;
- `messaging-compose/dovecot/dovecot.conf` ;
- `messaging-compose/dovecot/dovecot-ldap.conf.ext` ;
- les paramètres utilisés ;
- les adaptations et vérifications consignées ici.
