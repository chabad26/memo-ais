# Architecture de certification


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/pki-architecture.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Décision retenue

L'[inventaire des certificats](certificate-inventory.md) précède cette
architecture et ne modifie aucun service. Il fixe le périmètre des services et
clients qui doivent utiliser Campus CA.

L'infrastructure utilise l'autorité interne Step CA `Campus CA`, accessible sur
`https://ca.campus.test:443`. La CA est actuellement exécutée sur l'hôte de
laboratoire ; la cible d'exploitation est une VM ou un serveur dédié à
l'administration.

| Élément | Choix retenu | Justification |
| --- | --- | --- |
| Autorité de certification | Step CA sur serveur d'administration dédié | Isole la base de la CA, les journaux et la clé intermédiaire des conteneurs applicatifs. |
| Certificat racine public | `pki/certs/Campus-CA-root.crt` | Référence versionnée pour les clients internes. |
| VALEUR RETIRÉE | VALEUR RETIRÉE | VALEUR RETIRÉE |
| Émission | Provisionneurs distincts par administrateur ou automatisation | Les droits sont attribuables et limités. |
| Journalisation | Journaux systemd Step CA et inventaire des certificats | Les émissions, renouvellements et révocations restent traçables. |

## Périmètre de confiance

Le certificat racine est distribué aux hôtes Linux, aux postes
d'administration, aux navigateurs utilisés pour LAM, Roundcube et Kibana, et
aux clients de messagerie. Les services concernés recevront chacun un
certificat propre : OpenLDAP, Postfix, Dovecot, Roundcube, LAM et Kibana.

Les systèmes hors périmètre et les postes personnels non administrés ne doivent
pas recevoir le certificat racine.

## Cycle de vie

| Certificat | Durée cible | Action avant expiration |
| --- | --- | --- |
| Racine | 10 ans | Préparer la rotation 12 mois avant l'échéance. |
| Intermédiaire | 5 ans | Préparer la rotation 6 mois avant l'échéance. |
| Serveur | 90 jours | Renouveler automatiquement à 30 jours. |
| Client administrateur | 30 jours | Renouveler automatiquement ou après validation du rôle. |

Une alerte est créée à 30 jours, puis à 7 jours avant l'expiration. En cas de
compromission ou d'erreur, le certificat est identifié par son numéro de série,
révoqué, remplacé et le service est rechargé. La mise en production devra
inclure un mécanisme de révocation testé, tel qu'une CRL.

## État de mise en œuvre

La CA et son endpoint de santé sont validés. Le 7 août 2026, les certificats
OpenLDAP, Postfix, Dovecot et Roundcube ont été délivrés puis validés avec la
chaîne Campus CA. LDAPS, IMAPS, SMTP STARTTLS et HTTPS Roundcube sont décrits
dans `tls-deployment.md`.

LAM, Kibana et Elasticsearch restent au stade prévu dans le registre. Les
certificats courts du laboratoire imposent un suivi quotidien ou une politique
Step CA autorisant une durée plus longue avant une mise en production.
