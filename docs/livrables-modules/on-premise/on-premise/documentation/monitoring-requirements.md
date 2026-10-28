# Besoins de supervision


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/monitoring-requirements.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Périmètre

Cette analyse définit le périmètre de supervision et sert de référence au
déploiement Filebeat, Elasticsearch et Kibana. Les services conteneurisés
utilisent en priorité leurs sorties standard, complétées par les journaux
internes nécessaires au diagnostic.

Dans l'ordre corrigé du module, `step-ca` appartient à l'itération 6 et la
supervision à l'itération 7 optionnelle. Les événements de certificats sont
suivis comme une cible d'exploitation ; le tableau Kibana correspondant reste
préparatoire tant que les journaux Step CA ne sont pas collectés de bout en
bout.

## Tableau de collecte

| Service | Sources à collecter | Événements et informations attendus |
|---|---|---|
| OpenLDAP | `docker logs openldap`, journal `slapd` si activé | binds refusés, erreurs de schéma/base, modifications sensibles, codes LDAP, client et durée |
| Samba | `docker logs samba-ldap`, `/var/log/samba/log.smbd`, `log.<client>` | redémarrage, erreur LDAP, refus SMB, partage, utilisateur, client et NTSTATUS |
| Postfix | `docker logs mail-postfix`, `mail.log` si activé, `postqueue -p` | messages sent/deferred/bounced, SASL/TLS, relais, code SMTP et taille de file |
| Dovecot | `docker logs mail-dovecot`, journaux Dovecot | authentification, IMAP/LMTP, quota, Maildir, TLS, compte et IP cliente |
| Roundcube | `docker logs mail-roundcube`, Apache/PHP, erreurs Roundcube | connexions, erreurs HTTP/PHP, accès IMAP/SMTP/SQL et latence |
| MariaDB | `docker logs mail-db`, journal d'erreurs | disponibilité, connexions, requêtes lentes, verrous, InnoDB et espace |
| step-ca (itération 6) | `docker logs step-ca`, journal JSON si activé | émission, renouvellement, révocation, provisioner, numéro de série et expiration |
| BorgBackup | `backup/logs/`, `last-run.status` | résultat, code retour, archive, âge, durée, taille, intégrité, prune et verrou |
| Docker | `journalctl -u docker`, `docker events`, logs et inspect | arrêt, restart count, healthcheck, OOM, réseau, volume, CPU/RAM et espace |
| LAM | `docker logs lam`, Apache/PHP | disponibilité Web, connexion LDAP, code HTTP et exception |
| WordPress/MariaDB | logs des conteneurs Web et base | erreur HTTP/PHP/SQL, disponibilité, latence et capacité |

## Indicateurs prioritaires

- conteneur arrêté ou `unhealthy` : alerte immédiate ;
- plus de trois redémarrages en dix minutes : alerte ;
- dernière archive Borg âgée de plus de 36 heures : erreur ;
- stockage utilisé à 80 % : avertissement, à 90 % : critique ;
- certificat expirant sous 30 jours : avertissement, sous 7 jours : critique ;
- hausse des échecs d'authentification : analyse de sécurité ;
- croissance continue de la file Postfix pendant quinze minutes : incident.

## Informations à protéger

[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
de clé privée, de jeton ou de contenu complet de message. Les DN, adresses,
utilisateurs et identifiants de session doivent être accessibles uniquement aux
administrateurs autorisés et pseudonymisés dans les preuves partagées.

## Priorités

1. disponibilité et redémarrages des conteneurs ;
2. authentification LDAP, Samba et messagerie ;
3. résultat et ancienneté des sauvegardes ;
4. capacité des volumes et file Postfix ;
5. erreurs Web Roundcube/LAM ;
6. certificats et registre PKI.
