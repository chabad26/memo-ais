# Cas conditionnel - certificats Roundcube


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/gestion-certificats-roundcube.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.


## Contexte

Cette fiche ne correspond pas a une manipulation realisee pendant le poste de
gestion de crise LDAP. Elle decrit seulement ce qu'il aurait fallu faire si le
formateur avait aussi annonce la compromission de la cle privee Roundcube.

Dans ce cas, le certificat associe ne doit plus etre utilise. Il faut isoler
l'ancienne cle, revoquer le certificat, generer une nouvelle paire
cle/certificat, redeployer TLS puis verifier depuis un client que le service
presente le nouveau certificat.

## Documents utiles

| Document | Utilisation |
| --- | --- |
| `documentation/certificate-lifecycle.md` | Procedure de revocation et remplacement d'une cle compromise. |
| `documentation/tls-deployment.md` | Deploiement TLS de Roundcube et validation client. |
| `documentation/certificate-register.md` | Registre des certificats a mettre a jour si le cas est joue. |
| `pki/service-certificate-plan.tsv` | Sujet et SAN attendus : `webmail.embedded.local`. |
| `client-validation/validate-tls.sh` | Controle TLS depuis un client independant. |

## Elements a identifier

| Element | Valeur attendue |
| --- | --- |
| Service | Roundcube HTTPS |
| Point d'acces | `webmail.embedded.local:8443` |
| Ancien certificat | `pki/issued/roundcube/roundcube.crt` |
| Ancienne cle | `pki/issued/roundcube/roundcube.key` |
| Chaine complete | `pki/issued/roundcube/roundcube.fullchain.crt` |
| Volume TLS | `mail_roundcube_tls` |
| Ancien numero de serie | A relever si le scenario est declenche |
| Nouveau numero de serie | A relever apres generation |

Commande de releve :

```bash
cd ~/on-premise
openssl x509 -in pki/issued/roundcube/roundcube.crt -noout \
  -subject -issuer -serial -dates -ext subjectAltName
```

## Actions qui auraient ete a realiser

| Action | Commande ou preuve attendue |
| --- | --- |
| Isoler l'ancienne cle | Arret du service ou archivage protege des fichiers compromis. |
| Relever l'ancien numero de serie | `openssl x509 -serial`. |
| Revoquer l'ancien certificat | `step ca revoke` avec `KeyCompromise`. |
| Controler la CRL ou noter la limite labo | `step crl inspect` ou limite documentee. |
| Generer une nouvelle cle et un nouveau certificat | `step ca certificate webmail.embedded.local ...`. |
| Verifier la chaine | `openssl verify` avec la racine Campus CA. |
| Redeployer TLS | `./prepare-tls-volumes.sh` puis recreation de `nginx`/`roundcube`. |
| Verifier cote client | `openssl s_client`, `curl --cacert` ou `docker compose run --rm tls-client`. |
| Mettre a jour le registre | Ancien certificat revoque, nouveau certificat deploye. |

## Commandes de reference

### Revoquer l'ancien certificat

```bash
cd ~/on-premise

OLD_SERIAL="<numero_de_serie_roundcube>"

step ca revoke "$OLD_SERIAL" \
  --reason "Roundcube private key compromise" \
  --reasonCode KeyCompromise \
  --ca-url https://ca.campus.test \
  --root ~/on-premise/pki/certs/Campus-CA-root.crt
```

### Generer une nouvelle paire cle/certificat

```bash
cd ~/on-premise

mkdir -p pki/issued/roundcube/replacement
chmod 700 pki/issued/roundcube/replacement

step ca certificate webmail.embedded.local \
  pki/issued/roundcube/replacement/roundcube.crt \
  pki/issued/roundcube/replacement/roundcube.key \
  --san webmail.embedded.local \
  --ca-url https://ca.campus.test \
  --root pki/certs/Campus-CA-root.crt \
  --provisioner admin

chmod 600 pki/issued/roundcube/replacement/roundcube.key
```

### Verifier le nouveau certificat

```bash
cd ~/on-premise

cat pki/issued/roundcube/replacement/roundcube.crt \
  ~/.step/certs/intermediate_ca.crt \
  > pki/issued/roundcube/replacement/roundcube.fullchain.crt

openssl verify -CAfile pki/certs/Campus-CA-root.crt \
  -untrusted ~/.step/certs/intermediate_ca.crt \
  pki/issued/roundcube/replacement/roundcube.crt
```

### Verifier depuis un client

```bash
cd ~/on-premise/messaging-compose

openssl s_client -showcerts -connect 127.0.0.1:8443 \
  -servername webmail.embedded.local \
  -CAfile ../pki/certs/Campus-CA-root.crt </dev/null

curl --fail --resolve webmail.embedded.local:8443:127.0.0.1 \
  --cacert ../pki/certs/Campus-CA-root.crt \
  https://webmail.embedded.local:8443/
```

## A retenir

- Une cle privee compromise ne se reutilise pas.
- Le remplacement d'un fichier certificat ne suffit pas : il faut aussi
  revoquer l'ancien certificat si la CA le permet.
- La preuve finale doit venir d'un client qui voit le nouveau certificat.
- Dans le poste realise, ce scenario est seulement annonce ; il n'est pas une
  preuve de manipulation effectuee.
