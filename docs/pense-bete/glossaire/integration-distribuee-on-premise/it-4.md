# Glossaire Intégration distribuée on-premise — Itération 4

## Sujet

Messagerie interne avec Postfix, Dovecot, Roundcube et authentification LDAP.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| MTA | Mail Transfer Agent : service qui achemine les messages, ici Postfix. |
| MDA | Mail Delivery Agent : service qui livre les messages dans les boîtes. |
| IMAP | Protocole de consultation des messages sur le serveur, fourni par Dovecot. |
| SMTP | Protocole d'envoi et de transfert des messages, fourni par Postfix. |
| Submission | Service SMTP d'envoi authentifié, généralement sur le port 587. |
| LMTP | Protocole de livraison locale utilisé entre Postfix et Dovecot. |
| Roundcube | Webmail qui utilise IMAP et SMTP pour l'utilisateur. |
| SASL | Mécanisme d'authentification utilisé par Postfix avec Dovecot. |
| STARTTLS | Passage d'une connexion existante vers TLS. |
| File d'attente | Messages que Postfix doit encore délivrer. |

## Manipulations faites

| Manipulation | Commande ou action |
| --- | --- |
| Valider le Compose | `docker compose config --quiet` |
| Démarrer la messagerie | `docker compose up -d` |
| Contrôler les services | `docker compose ps` et `docker compose logs --tail=100` |
| Examiner la file SMTP | `docker compose exec postfix postqueue -p` |
| Tester LDAP | Vérifier le compte technique et les recherches LDAP de Postfix/Dovecot. |
| Vérifier TLS | Contrôler le nom DNS, la chaîne et la validité du certificat présenté. |

## Points de vigilance

- Les comptes techniques LDAP restent dans `.env`, jamais dans Git.
- Une file Postfix qui augmente indique une livraison dégradée, même si le conteneur est actif.
- TLS doit protéger HTTPS, IMAPS, Submission SMTP et les échanges LDAP sensibles.
- Les journaux doivent éviter les mots de passe, tout en gardant les échecs d'authentification exploitables.

## Docs associées

- [Vue d'ensemble de l'itération 4](../../../integration-distribuee-on-premise/it-4/index.md)
- [Concevoir l'architecture de messagerie](../../../integration-distribuee-on-premise/it-4/concevoir-architecture-messagerie.md)
- [Préparer la sécurisation TLS](../../../integration-distribuee-on-premise/it-4/securiser-messagerie-tls.md)
- [Authentifier la messagerie avec LDAP](../../../integration-distribuee-on-premise/it-4/authentification-ldap-messagerie.md)
