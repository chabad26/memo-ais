# Déploiement TLS de la messagerie


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/tls-deployment.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.


## État validé le 7 août 2026

| Service | Point d'accès | Résultat |
| --- | --- | --- |
| OpenLDAP | LDAPS `ldap.embedded.local:636` | Certificat Campus CA et chaîne validés. |
| Dovecot | IMAPS `imap.embedded.local:993` | Certificat Campus CA et chaîne validés. |
| Postfix | STARTTLS `smtp.embedded.local:587` | Certificat Campus CA et chaîne validés ; conteneur `healthy`. |
| Roundcube | HTTPS `webmail.embedded.local:8443` | Réponse `HTTP 200` et certificat Campus CA validé. |

Le port `8443` est retenu pour Roundcube dans le laboratoire car Step CA
utilise déjà le port hôte `443`. Le port HTTP de Roundcube n'est plus publié
sur l'hôte : seul Nginx y accède sur le réseau Docker `mail`.

## Fichiers et volumes

Les certificats émis restent dans `pki/issued/<service>/`, qui est ignoré par
Git. Les clés ne sont pas montées directement dans les services. Les scripts
de préparation les copient dans des volumes Docker avec des permissions
adaptées :

| Service | Volume Docker | Chemin dans le conteneur |
| --- | --- | --- |
| OpenLDAP | `openldap_tls` | `/container/services/openldap/assets/certs` |
| Postfix | `mail_postfix_tls` | `/etc/postfix/tls` |
| Dovecot | `mail_dovecot_tls` | `/etc/dovecot/tls` |
| Nginx Roundcube | `mail_roundcube_tls` | `/etc/nginx/tls` |

Les certificats complets sont en `644 root:root` et les clés en
`600 root:root` dans ces volumes. La racine publique
`pki/certs/Campus-CA-root.crt` est intégrée aux trois images locales
`campus-postfix:tls`, `campus-dovecot:tls` et `campus-roundcube:tls` au
moyen de `update-ca-certificates`.

Après un renouvellement, mettre à jour les volumes avant le redémarrage :

```bash
cd ~/on-premise/infrastructure-compose
./prepare-openldap-tls.sh

cd ~/on-premise/messaging-compose
./prepare-tls-volumes.sh
docker compose up -d --force-recreate postfix dovecot roundcube nginx
```

## Configuration appliquée

- `infrastructure-compose/compose.yaml` pilote le conteneur OpenLDAP actif.
  Il publie `636:6360`, monte la racine Campus CA et le volume `openldap_tls`.
- `infrastructure-compose/configure-openldap-tls.sh` ajoute les attributs
  `olcTLS*` à la configuration OpenLDAP persistante. Il est nécessaire car le
  bootstrap de l'image est ignoré lorsque les volumes LDAP existent déjà.
- Dovecot exige TLS, présente `dovecot.fullchain.crt` et consulte LDAP avec
  `ldaps://ldap.embedded.local:6360` en exigeant un certificat valide.
- Postfix présente `postfix.fullchain.crt`, interdit l'authentification SMTP
  en clair et effectue ses recherches LDAP via LDAPS avec validation de CA.
- Les alias Docker `imap.embedded.local`, `smtp.embedded.local` et
  `ldap.embedded.local` correspondent aux SAN des certificats.
- Roundcube utilise IMAPS et SMTP STARTTLS. Nginx termine HTTPS avec
  `roundcube.fullchain.crt`.

## Vérifications réalisées

```bash
# Exécuter depuis ~/on-premise/messaging-compose.
openssl s_client -connect 127.0.0.1:993 \
  -servername imap.embedded.local \
  -CAfile ../pki/certs/Campus-CA-root.crt </dev/null

openssl s_client -starttls smtp -connect 127.0.0.1:587 \
  -servername smtp.embedded.local \
  -CAfile ../pki/certs/Campus-CA-root.crt </dev/null

curl --fail --resolve webmail.embedded.local:8443:127.0.0.1 \
  --cacert ../pki/certs/Campus-CA-root.crt \
  https://webmail.embedded.local:8443/
```

Pour LDAPS, exécuter depuis `~/on-premise/infrastructure-compose` :

```bash
openssl s_client -connect 127.0.0.1:636 \
  -servername ldap.embedded.local \
  -CAfile ../pki/certs/Campus-CA-root.crt </dev/null
```

Les quatre contrôles retournent une chaîne valide ; Roundcube retourne
`HTTP 200`. L'authentification et l'envoi depuis l'interface Roundcube restent
à tester avec un compte LDAP de test autorisé.

## Résolution des noms clients

Au moment de la validation, les noms de messagerie n'étaient pas encore publiés
par un DNS accessible au poste client. Pour le laboratoire, ajouter ces entrées
sur le client avec l'adresse actuelle du serveur (`192.168.1.199`) ou créer les
enregistrements équivalents dans le DNS local :

```text
192.168.1.199 ldap.embedded.local smtp.embedded.local imap.embedded.local webmail.embedded.local
```

Après cette résolution, le navigateur peut ouvrir
`https://webmail.embedded.local:8443/` et les clients de messagerie utilisent
les noms présents dans les SAN. Ne pas remplacer les noms par une adresse IP :
elle n'est pas couverte par les certificats délivrés.

## Client Docker de validation

Un client Debian jetable permet de rejouer les contrôles sans installer la
racine Campus CA sur le système hôte. Il installe uniquement la racine publique
dans son propre magasin de confiance et résout les noms des certificats vers
`host-gateway`.

```bash
cd ~/on-premise/client-validation
docker compose build
docker compose run --rm tls-client
```

Le script contrôle LDAPS, IMAPS, SMTP STARTTLS et HTTPS Roundcube. Il exige un
nom valide, une chaîne de confiance reconnue et une réponse HTTP réussie.
Consulter `client-validation/README.md` pour le diagnostic interactif.

## Difficultés rencontrées

| Difficulté | Correction appliquée |
| --- | --- |
| Bootstrap OpenLDAP ignoré sur des volumes existants | Ajout des attributs TLS avec `slapmodify` hors ligne. |
| Clé OpenLDAP non lisible par l'UID du conteneur | Distribution dans le volume `openldap_tls` avec l'UID `911`. |
| Port 443 déjà utilisé par Step CA | Publication Nginx sur `8443:443`. |
| Répertoire de certificat Postfix signalé par les contrôles | Volumes dédiés contenant seulement la clé et la chaîne complète. |
| URL LDAPS rejetée par Dovecot | Utilisation du paramètre `uris`, requis par Dovecot 2.3. |
