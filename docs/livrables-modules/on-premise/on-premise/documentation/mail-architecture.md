# Architecture de la messagerie


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/mail-architecture.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.


## Schéma

```text
                         +----------------------+
                         |      OpenLDAP        |
                         | identités et groupes |
                         +----------+-----------+
                                    |
                         LDAP :3890 | recherche/auth
                                    |
       +----------------------------+----------------------------+
       |                                                         |
+------v-------+       SMTP AUTH       +--------------------------v+
|   Dovecot    |<----------------------|        Postfix            |
| IMAP / LMTP  |                       | SMTP / submission :587  |
| boîtes mail  |---------------------->| livraison LMTP           |
+------+-------+                       +--------------------------+
       ^                                           ^
       | IMAP :143                                 | SMTP :587
       |                                           |
       +------------------+------------------------+
                          |
                 +--------v---------+
                 |    Roundcube     |
                 | Webmail :8082    |
                 +--------+---------+
                          |
                 +--------v---------+
                 |     MariaDB      |
                 | base Roundcube  |
                 +------------------+
```

## Services nécessaires

| Service | Rôle | Présence dans le projet |
|---|---|---|
| OpenLDAP | Source centralisée des comptes, groupes et attributs `mail` | Déployé dans `openldap/` |
| Postfix | Réception SMTP, soumission authentifiée et routage local | Déployé dans `messaging-compose/` |
| Dovecot | Authentification LDAP, IMAP et livraison LMTP | Déployé dans `messaging-compose/` |
| Roundcube | Interface Web de consultation et d'envoi | Déployé dans `messaging-compose/` |
| MariaDB | Stockage de la configuration et des préférences Roundcube | Déployé dans `messaging-compose/` |
| DNS | Résolution de `mail.embedded.local` et futurs enregistrements MX | À intégrer selon l'environnement |
| TLS / certificats | Protection des connexions Web, IMAP, SMTP et LDAP | Préparé, non activé |

## Flux validés

- Roundcube utilise Dovecot sur le port `143` pour IMAP.
- Roundcube utilise Postfix sur le port `587` pour SMTP submission.
- Postfix délègue l'authentification SMTP à Dovecot par le socket Unix
  `private/auth`.
- Postfix recherche les destinataires dans OpenLDAP avec le compte technique
  en lecture seule.
- Postfix remet les messages à Dovecot par le socket LMTP
  `private/dovecot-lmtp`.
- Dovecot authentifie les utilisateurs par `auth_bind` dans OpenLDAP.

## Fichiers de référence

- `messaging-compose/docker-compose.yml` : services, réseaux, ports et volumes ;
- `messaging-compose/dovecot/dovecot.conf` : IMAP, LMTP et sockets ;
- `messaging-compose/dovecot/dovecot-ldap.conf.ext` : authentification LDAP ;
- `messaging-compose/postfix-init.sh` : table LDAP et restrictions SMTP ;
- `documentation/mail-deployment.md` : déploiement et vérifications ;
- `documentation/mail-ldap-auth.md` : paramètres d'intégration LDAP ;
- `documentation/validation-mail.md` : tests et résultats ;
- `documentation/mail-validation-corrections.md` : incident et résolution ;
- `documentation/mail-tls-security.md` : préparation de la sécurisation.

