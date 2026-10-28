# Inventaire des certificats


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/certificate-inventory.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Périmètre

Ce document recense les certificats nécessaires à l'infrastructure on-premise.
Il sert à préparer puis contrôler les certificats réellement délivrés. Au
7 août 2026, OpenLDAP, Postfix, Dovecot et Roundcube disposent d'une validation
TLS consignée dans `tls-deployment.md` et `certificate-register.md`.

| Service | Protocole | Rôle du certificat | Clients qui doivent faire confiance |
| --- | --- | --- | --- |
| Step CA `ca.campus.test` | HTTPS | Authentifier la CA et protéger les demandes de certificats | Administrateurs PKI, automatisations et hôtes Linux. |
| OpenLDAP | LDAPS ou StartTLS | Authentifier l'annuaire et chiffrer les recherches LDAP | Postfix, Dovecot, Samba, LAM et administrateurs LDAP. |
| Postfix | Submission STARTTLS et SMTP TLS | Authentifier le serveur SMTP | Clients de messagerie, Roundcube et relais internes. |
| Dovecot | IMAPS ou IMAP STARTTLS | Authentifier le serveur de boîtes aux lettres | Clients de messagerie et Roundcube. |
| Roundcube et LAM | HTTPS | Protéger les interfaces Web et les sessions | Navigateurs des utilisateurs et administrateurs. |
| Kibana | HTTPS | Protéger les recherches de journaux | Navigateurs des exploitants. |
| Elasticsearch | HTTPS | Protéger l'API et authentifier le nœud | Kibana, Filebeat et administrateurs d'API. |
| Nginx ou WordPress publié | HTTPS | Protéger les sessions et formulaires | Navigateurs concernés. |

MariaDB, Samba SMB et Filebeat ne présentent pas de certificat serveur dans le
périmètre initial. Filebeat devra cependant faire confiance à Campus CA lorsque
la connexion à Elasticsearch passera en TLS.

## Règle de confiance

Les clients reçoivent le certificat racine public
`pki/certs/Campus-CA-root.crt`, après vérification de son empreinte. Les clés
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
