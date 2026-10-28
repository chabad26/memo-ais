# LDAP Account Manager


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/ldap-account-manager/README.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


Le rôle détaillé des fichiers est décrit dans
[`../documentation/technical-files-guide.md`](../documentation/technical-files-guide.md).

LAM est une interface d'administration : les utilisateurs et groupes restent
dans OpenLDAP. Le Compose transmet l'adresse LDAP, les suffixes et le compte
administrateur, puis relie LAM au réseau externe `openldap_default`.

[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
du DN `cn=admin,dc=embedded,dc=local`, utilisé pour modifier l'annuaire.

```bash
docker compose config
docker compose up -d
docker compose logs --tail=100 lam
```
