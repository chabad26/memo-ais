# Traiter la compromission du certificat Roundcube

## Objectif

Traiter la compromission de la cle privee utilisee par Roundcube en appliquant
les procedures PKI : revocation, publication de la CRL, generation d'une
nouvelle cle, deploiement d'un nouveau certificat et verification cote client.

Le scenario fait suite a l'incident OpenLDAP. Pendant l'analyse, le binome
decouvre que la cle privee du certificat HTTPS Roundcube est egalement
compromise.

## Documents de travail

| Document | Role dans l'exercice |
| --- | --- |
| `/home/oliv/on-premise/documentation/certificate-lifecycle.md` | Procedure de revocation et remplacement d'une cle compromise. |
| `/home/oliv/on-premise/documentation/tls-deployment.md` | Deploiement TLS de la messagerie et de Roundcube. |
| `/home/oliv/on-premise/documentation/certificate-register.md` | Registre des certificats delivres, numeros de serie et statuts. |
| `/home/oliv/on-premise/pki/service-certificate-plan.tsv` | Sujet et SAN attendus pour Roundcube. |
| `/home/oliv/on-premise/client-validation/validate-tls.sh` | Verification cliente TLS, dont Roundcube HTTPS. |
| `/home/oliv/on-premise/documentation/gestion-certificats-roundcube.md` | Livrable de l'exercice. |

!!! warning "Cle compromise"
    Une cle privee compromise ne doit pas etre renouvelee. Il faut revoquer le
    certificat associe, generer une nouvelle paire cle/certificat et remplacer
    les fichiers deployes.

## Perimetre touche

| Element | Valeur |
| --- | --- |
| Service | Roundcube via Nginx HTTPS |
| Nom DNS | `webmail.embedded.local` |
| Port de test | `8443` |
| Certificat actif | `pki/issued/roundcube/roundcube.crt` |
| Cle compromise | `pki/issued/roundcube/roundcube.key` |
| Chaine complete | `pki/issued/roundcube/roundcube.fullchain.crt` |
| Volume TLS | `mail_roundcube_tls` |
| Service Compose a recreer | `nginx` et, si necessaire, `roundcube` |

## Plan d'actions

| Action | Resultat attendu |
| --- | --- |
| Isoler l'ancienne cle Roundcube. | La cle compromise n'est plus reutilisee. |
| Relever l'ancien numero de serie. | Le certificat a revoquer est identifie. |
| Revoquer le certificat. | Le motif `KeyCompromise` est enregistre dans la CA. |
| Publier ou verifier la CRL. | Les clients disposant de la CRL peuvent refuser l'ancien certificat. |
| Generer une nouvelle cle et un nouveau certificat. | Le SAN `webmail.embedded.local` est conserve. |
| Construire une nouvelle chaine complete. | Le service presente certificat + intermediaire. |
| Deployer dans le volume TLS Roundcube. | Nginx utilise les nouveaux fichiers. |
| Recréer le service. | Les nouvelles connexions utilisent le nouveau certificat. |
| Verifier depuis un client. | Le certificat presente a un nouveau numero de serie et la chaine est valide. |
| Mettre a jour le registre. | Ancien certificat revoque, nouveau certificat deploye. |

## Commandes de reference

### 1. Relever l'ancien certificat

```bash
cd /home/oliv/on-premise

openssl x509 -in pki/issued/roundcube/roundcube.crt -noout \
  -subject -issuer -serial -dates -ext subjectAltName
```

Conserver la sortie dans le livrable. Le numero de serie obtenu sert a la
revocation.

### 2. Revoquer le certificat compromis

```bash
OLD_SERIAL="<numero_de_serie_roundcube>"

step ca revoke "$OLD_SERIAL" \
  --reason "Roundcube private key compromise" \
  --reasonCode KeyCompromise \
  --ca-url https://ca.campus.test \
  --root /home/oliv/on-premise/pki/certs/Campus-CA-root.crt
```

Le secret du provisionneur peut etre demande a l'execution. Ne pas l'ecrire
dans la documentation.

### 3. Publier et controler la CRL

La publication depend de la configuration de la CA. Si une URL de CRL est
exposee par Campus CA, la controler et conserver son contenu :

```bash
CRL_URL="https://ca.campus.test/crls/campus-ca.crl"

step crl inspect "$CRL_URL" \
  --roots /home/oliv/on-premise/pki/certs/Campus-CA-root.crt
```

Si la CRL est publiee dans un fichier local avant exposition HTTP :

```bash
CRL_FILE="/home/oliv/on-premise/pki/crl/campus-ca.crl"

step crl inspect "$CRL_FILE" \
  --ca /home/oliv/.step/certs/intermediate_ca.crt
```

Le livrable doit indiquer l'URL ou le chemin publie, la date `thisUpdate`,
la date `nextUpdate` et la presence de l'ancien numero de serie Roundcube.

!!! note "Limite de laboratoire"
    Si la CA de laboratoire ne publie pas encore de CRL exploitable, noter la
    revocation comme realisee et la publication CRL comme limite a corriger.
    L'ancien certificat doit quand meme etre retire du service.

### 4. Generer une nouvelle cle et un nouveau certificat

```bash
cd /home/oliv/on-premise

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

### 5. Verifier le nouveau certificat

```bash
cd /home/oliv/on-premise

cat pki/issued/roundcube/replacement/roundcube.crt \
  /home/oliv/.step/certs/intermediate_ca.crt \
  > pki/issued/roundcube/replacement/roundcube.fullchain.crt

chmod 644 pki/issued/roundcube/replacement/roundcube.fullchain.crt

openssl x509 -in pki/issued/roundcube/replacement/roundcube.crt -noout \
  -subject -issuer -serial -dates -ext subjectAltName

openssl verify -CAfile pki/certs/Campus-CA-root.crt \
  -untrusted /home/oliv/.step/certs/intermediate_ca.crt \
  pki/issued/roundcube/replacement/roundcube.crt
```

Le resultat de `openssl verify` doit etre `OK`. Le nouveau numero de serie doit
etre different de l'ancien.

### 6. Remplacer les fichiers actifs

```bash
cd /home/oliv/on-premise

mkdir -p pki/issued/roundcube/compromised-2026-08-10
chmod 700 pki/issued/roundcube/compromised-2026-08-10

mv pki/issued/roundcube/roundcube.crt \
  pki/issued/roundcube/compromised-2026-08-10/
mv pki/issued/roundcube/roundcube.key \
  pki/issued/roundcube/compromised-2026-08-10/
mv pki/issued/roundcube/roundcube.fullchain.crt \
  pki/issued/roundcube/compromised-2026-08-10/

cp pki/issued/roundcube/replacement/roundcube.crt \
  pki/issued/roundcube/roundcube.crt
cp pki/issued/roundcube/replacement/roundcube.key \
  pki/issued/roundcube/roundcube.key
cp pki/issued/roundcube/replacement/roundcube.fullchain.crt \
  pki/issued/roundcube/roundcube.fullchain.crt

chmod 600 pki/issued/roundcube/roundcube.key
chmod 644 pki/issued/roundcube/roundcube.crt \
  pki/issued/roundcube/roundcube.fullchain.crt
```

### 7. Deployer sur Roundcube

```bash
cd /home/oliv/on-premise/messaging-compose

./prepare-tls-volumes.sh
docker compose up -d --force-recreate nginx roundcube
docker compose ps
docker compose logs --tail=100 nginx
```

### 8. Verifier depuis un client

```bash
cd /home/oliv/on-premise/client-validation
docker compose run --rm tls-client
```

Verification ciblee Roundcube :

```bash
cd /home/oliv/on-premise/messaging-compose

openssl s_client -showcerts -connect 127.0.0.1:8443 \
  -servername webmail.embedded.local \
  -CAfile ../pki/certs/Campus-CA-root.crt </dev/null \
  2>/tmp/roundcube-tls.txt \
  | sed -n '/-----BEGIN CERTIFICATE-----/,/-----END CERTIFICATE-----/p' \
  > /tmp/roundcube-server.crt

openssl x509 -in /tmp/roundcube-server.crt -noout \
  -subject -issuer -serial -dates -ext subjectAltName

curl --fail --resolve webmail.embedded.local:8443:127.0.0.1 \
  --cacert ../pki/certs/Campus-CA-root.crt \
  https://webmail.embedded.local:8443/
```

## Tableau de resultat attendu

| Action | Resultat |
| --- | --- |
| Ancien numero de serie releve | A completer |
| Certificat Roundcube revoque | A completer |
| CRL publiee ou limite documentee | A completer |
| Nouvelle cle generee | A completer |
| Nouveau certificat genere | A completer |
| Nouveau certificat verifie | A completer |
| Volume TLS Roundcube mis a jour | A completer |
| Service Roundcube recree | A completer |
| Client validant le nouveau certificat | A completer |
| Registre des certificats mis a jour | A completer |

## Livrable attendu

Dans `/home/oliv/on-premise/documentation/gestion-certificats-roundcube.md`,
conserver :

- les operations realisees ;
- les commandes utilisees ;
- l'ancien et le nouveau numero de serie ;
- le motif de revocation ;
- la preuve de publication ou de controle de CRL ;
- la preuve de generation du nouveau certificat ;
- la preuve de deploiement sur Roundcube ;
- la verification client montrant le nouveau certificat.

## Questions de synthese

1. Pourquoi une cle compromise ne doit-elle pas etre renouvelee ?
2. Quel motif de revocation correspond a ce scenario ?
3. Quelle difference y a-t-il entre revoquer un certificat et remplacer le
   fichier deploye sur le service ?
4. Comment prouver que le client voit bien le nouveau certificat ?
5. Que faut-il documenter si la CRL n'est pas encore publiee par la CA de
   laboratoire ?
