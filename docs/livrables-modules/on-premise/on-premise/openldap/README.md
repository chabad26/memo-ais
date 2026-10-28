# OpenLDAP


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/openldap/README.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


Le rôle détaillé des fichiers est décrit dans
[`../documentation/technical-files-guide.md`](../documentation/technical-files-guide.md).

## Comment fonctionne le Compose

- `compose.yaml` configure l'image, le port, les schémas et les volumes ;
- `.env` fournit les paramètres locaux et les hashes administrateur ;
- `ldap_data` conserve les entrées ;
- `ldap_config` conserve la configuration dynamique `slapd.d` ;
- `ldap_backups` conserve les sauvegardes internes de l'image ;
- `../samba-ldap/schema` fournit le schéma Samba en lecture seule.

Les variables de bootstrap initialisent un volume vide. Elles ne remplacent
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]

```bash
docker compose config
docker compose up -d
docker compose ps
docker compose logs --tail=100 openldap
```
