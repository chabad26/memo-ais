# Registre des certificats délivrés


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/certificate-register.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Règle de tenue

Compléter ce registre après chaque émission avec les valeurs relevées par
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]

| Service | Sujet et SAN | Fichier certificat | Date de début | Date de fin | Émetteur | Numéro de série | Statut |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OpenLDAP | `ldap.embedded.local` | `pki/issued/openldap/openldap.crt` | 7 août 2026 12:43 UTC | 8 août 2026 12:44 UTC | Campus CA Intermediate CA | `75188a05d86da384c63fe3e4417821da` | Déployé et validé le 7 août ; expiré, à renouveler avant réutilisation. |
| Postfix | `smtp.embedded.local`, `mail.embedded.local` | `pki/issued/postfix/postfix.crt` | 7 août 2026 13:09 UTC | 8 août 2026 13:10 UTC | Campus CA Intermediate CA | `a5ba7ce288683aa6b63fae856154c326` | Déployé et validé le 7 août ; expiré, à renouveler avant réutilisation. |
| Dovecot | `imap.embedded.local`, `mail.embedded.local` | `pki/issued/dovecot/dovecot.crt` | 7 août 2026 13:09 UTC | 8 août 2026 13:10 UTC | Campus CA Intermediate CA | `90caa5a069dc1949202067124c885c29` | Déployé et validé le 7 août ; expiré, à renouveler avant réutilisation. |
| Roundcube | `webmail.embedded.local` | `pki/issued/roundcube/roundcube.crt` | 7 août 2026 13:09 UTC | 8 août 2026 13:10 UTC | Campus CA Intermediate CA | `ab3d8b5f0896978e607b0649a6a8a141` | Déployé et validé le 7 août avec `HTTP 200` ; expiré, à renouveler avant réutilisation. |
| LAM | `lam.embedded.local` | À compléter | À compléter | À compléter | Campus CA | À compléter | Prévu |
| Kibana | `kibana.embedded.local` | À compléter | À compléter | À compléter | Campus CA | À compléter | Prévu |
| Elasticsearch | `elasticsearch.embedded.local` | À compléter | À compléter | À compléter | Campus CA | À compléter | Prévu |

Les fichiers de chaque émission sont enregistrés dans `pki/issued/<service>/`.
Ce répertoire est exclu de Git car il contient les clés privées.

Les certificats délivrés le 7 août 2026 avaient une validité d'environ
24 heures. La durée cible de 90 jours nécessite une politique Step CA qui
l'autorise. À partir du 8 août 2026, ces certificats servent de preuve de
validation historique et doivent être renouvelés avant tout nouveau test TLS.
