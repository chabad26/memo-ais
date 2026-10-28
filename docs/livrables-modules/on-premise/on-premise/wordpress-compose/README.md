# WordPress et MariaDB


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/wordpress-compose/README.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.


Le rôle détaillé des fichiers est décrit dans
[`../documentation/technical-files-guide.md`](../documentation/technical-files-guide.md).

## Comment fonctionne le Compose

- `db` démarre MariaDB et écrit ses données dans `db_data` ;
- `wordpress` joint la base avec le nom DNS Docker `db` ;
- les variables `${MARIADB_*}` doivent être identiques des deux côtés ;
- `${WORDPRESS_PORT}:80` publie le port choisi sur l'hôte ;
- `.env` contient les valeurs locales et `.env.example` sert de modèle.

```bash
docker compose config
docker compose up -d
docker compose ps
docker compose logs
```

Ne pas utiliser `docker compose down -v` si les pages et la base doivent être
conservées.
