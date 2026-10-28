# Client Docker de validation TLS


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/client-validation/README.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.


Ce dossier fournit un client Debian jetable pour vérifier les certificats
Campus CA sans modifier le magasin de confiance de la machine hôte.

L'image installe uniquement la racine publique `pki/certs/Campus-CA-root.crt`.
Elle ne contient ni clé privée ni certificat de service. Les noms
`*.embedded.local` sont résolus vers `host-gateway`, donc vers les ports publiés
par les conteneurs OpenLDAP et de messagerie exécutés sur l'hôte Docker.

## Lancer la validation

```bash
cd ~/on-premise/client-validation
docker compose build
docker compose run --rm tls-client
```

Le script vérifie LDAPS sur 636, IMAPS sur 993, SMTP STARTTLS sur 587 et HTTPS
Roundcube sur 8443. Chaque contrôle TLS doit terminer par
`Verify return code: 0 (ok)` ; le dernier contrôle doit afficher `HTTP 200`.

## Diagnostic

Le conteneur est éphémère. Pour ouvrir un shell et lancer une commande ciblée :

```bash
docker compose run --rm --entrypoint sh tls-client
openssl s_client -connect imap.embedded.local:993 \
  -servername imap.embedded.local -verify_hostname imap.embedded.local
```

Si le nom de la passerelle Docker ne convient pas à un environnement donné,
remplacer les entrées `extra_hosts` dans `compose.yaml` par l'adresse IP du
serveur de laboratoire. Conserver les noms DNS dans les commandes TLS afin que
la validation du SAN reste effective.
