# Administration du cycle de vie des certificats


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/certificate-lifecycle.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Règles d'exploitation

Le responsable PKI contrôle chaque semaine le registre
`documentation/certificate-register.md`. Avec les certificats courts du
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
provisionneur restent hors Git, des scripts et des captures.

Les fichiers d'un service sont dans `pki/issued/<service>/` : certificat PEM,
clé privée, chaîne complète et relevé d'inspection.

## Scénario : certificat expirant prochainement

La procédure est déclenchée à moins de sept jours de l'échéance. Les
certificats de ce laboratoire durant environ 24 heures, le seuil opérationnel
est de huit heures avant `notAfter`.

| Étape | Opération | Impact utilisateur |
| --- | --- | --- |
| Contrôler | Relever le sujet, les SAN, la série et l'échéance. | Aucun. |
| Renouveler | Émettre un nouveau certificat avant l'expiration. | Aucun si anticipé. |
| Préparer | Recréer la chaîne complète et vérifier le résultat. | Aucun. |
| Déployer | Actualiser les volumes TLS et recréer le service. | Courte interruption des nouvelles connexions. |
| Valider | Lancer le client Docker et mettre à jour le registre. | Aucun après validation. |

### Contrôler l'échéance

```bash
cd ~/on-premise
openssl x509 -in pki/issued/dovecot/dovecot.crt -noout \
  -subject -serial -dates -ext subjectAltName
openssl x509 -in pki/issued/dovecot/dovecot.crt -noout -checkend 28800
```

La seconde commande retourne `1` lorsque le seuil de huit heures est atteint.
Remplacer `dovecot` par le service concerné.

### Renouveler une clé fiable

Ne réaliser ce renouvellement que si la clé privée n'est pas compromise. Il
conserve cette clé et écrit le certificat renouvelé au même emplacement.

```bash
cd ~/on-premise
SERVICE=dovecot
DIR="pki/issued/$SERVICE"

step ca renew --force \
  --ca-url https://ca.campus.test \
  --root pki/certs/Campus-CA-root.crt \
  "$DIR/$SERVICE.crt" "$DIR/$SERVICE.key"

cat "$DIR/$SERVICE.crt" ~/.step/certs/intermediate_ca.crt \
  > "$DIR/$SERVICE.fullchain.crt"
chmod 644 "$DIR/$SERVICE.fullchain.crt"
step certificate inspect "$DIR/$SERVICE.crt" | tee "$DIR/$SERVICE.inspect.txt"
openssl verify -CAfile pki/certs/Campus-CA-root.crt \
  -untrusted ~/.step/certs/intermediate_ca.crt "$DIR/$SERVICE.crt"
```

Le résultat de `openssl verify` doit être `OK`. Arrêter la procédure si le
sujet, les SAN ou l'émetteur ne correspondent pas au service attendu.

### Déployer et valider

Pour Postfix, Dovecot et Roundcube :

```bash
cd ~/on-premise/messaging-compose
./prepare-tls-volumes.sh
docker compose up -d --force-recreate postfix dovecot roundcube nginx
```

Pour OpenLDAP :

```bash
cd ~/on-premise/infrastructure-compose
./prepare-openldap-tls.sh
docker compose up -d --force-recreate openldap
```

Puis vérifier depuis le client indépendant :

```bash
cd ~/on-premise/client-validation
docker compose run --rm tls-client
```

Mettre à jour le registre avec les dates, SAN, nouveau numéro de série et état
« Déployé, chaîne validée ».

## Révocation et remplacement d'une clé compromise

Une clé suspecte ne doit jamais être renouvelée. Isoler ou arrêter le service,
prévenir l'administrateur PKI, relever la série puis révoquer le certificat :

```bash
openssl x509 -in pki/issued/postfix/postfix.crt -noout -serial
step ca revoke <numero_de_serie> \
  --reason "private key compromise" \
  --reasonCode KeyCompromise \
  --ca-url https://ca.campus.test \
  --root ~/on-premise/pki/certs/Campus-CA-root.crt
```

Créer ensuite une **nouvelle clé** et un certificat dans un emplacement
temporaire, les vérifier, créer le `fullchain`, puis seulement remplacer les
fichiers actifs et actualiser le volume TLS :

```bash
cd ~/on-premise
mkdir -p pki/issued/postfix/replacement
chmod 700 pki/issued/postfix/replacement
step ca certificate smtp.embedded.local \
  pki/issued/postfix/replacement/postfix.crt \
  pki/issued/postfix/replacement/postfix.key \
  --san smtp.embedded.local --san mail.embedded.local \
  --ca-url https://ca.campus.test \
  --root pki/certs/Campus-CA-root.crt --provisioner admin
chmod 600 pki/issued/postfix/replacement/postfix.key
```

Documenter le motif de révocation, l'ancien et le nouveau numéro de série,
l'heure, le service touché et le résultat de la validation. Une indisponibilité
courte est possible ; les clients vérifiant OCSP ou CRL rejettent l'ancien
certificat après révocation.

## Ajout ou remplacement de serveur

Pour un nouveau service ou un serveur remplacé, valider d'abord le nom DNS et
les SAN, générer une nouvelle clé sur le serveur cible, déployer la racine aux
clients concernés, puis valider TLS. Révoquer l'ancien certificat avec le motif
`Superseded` ou `CessationOfOperation` lorsqu'il ne doit plus être utilisé.
