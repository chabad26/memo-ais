# Administrer le cycle de vie des certificats

## Objectif

Définir les opérations d'administration des certificats Campus CA pendant leur
cycle de vie : contrôle d'échéance, renouvellement, déploiement, révocation et
remplacement.

## Scénario retenu : certificat expirant prochainement

Le scénario retenu est un certificat qui expire dans une semaine. Les
certificats du laboratoire ayant une durée d'environ 24 heures, la procédure
est déclenchée huit heures avant `notAfter`.

| Situation | Certificats concernés | Action retenue | Impact utilisateur |
| --- | --- | --- | --- |
| Certificat Dovecot bientôt expiré | `dovecot.crt`, `dovecot.key`, `dovecot.fullchain.crt` | Renouveler avant l'échéance, recréer la chaîne, actualiser le volume TLS, redémarrer Dovecot et valider. | Brève interruption des nouvelles connexions IMAP. |

La procédure s'applique aussi à OpenLDAP, Postfix et Roundcube. Elle est
réalisée par l'administrateur PKI autorisé à utiliser le provisionneur `admin`.

## Procédure de renouvellement

### Contrôler l'échéance

```bash
cd ~/on-premise
openssl x509 -in pki/issued/dovecot/dovecot.crt -noout \
  -subject -serial -dates -ext subjectAltName
openssl x509 -in pki/issued/dovecot/dovecot.crt -noout -checkend 28800
```

La seconde commande retourne `1` lorsque le seuil est atteint. Relever alors
les SAN, la série et les dates dans le registre des certificats.

### Renouveler une clé fiable

Ne jamais faire cette opération si la clé est compromise : le renouvellement
conserve la clé privée. Pour un certificat encore valide :

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

Le résultat attendu est `OK`. Interrompre si le sujet, les SAN ou l'émetteur ne
correspondent pas au service prévu.

### Déployer et vérifier

Pour la messagerie et Roundcube :

```bash
cd ~/on-premise/messaging-compose
./prepare-tls-volumes.sh
docker compose up -d --force-recreate postfix dovecot roundcube nginx

cd ~/on-premise/client-validation
docker compose run --rm tls-client
```

Le client Docker doit présenter les SAN, dates, émetteur et
`Verify return code: 0 (ok)`, puis `HTTP 200` pour Roundcube. Mettre à jour le
registre avec le nouveau numéro de série, les dates et l'état final.

## Révocation ou remplacement

| Situation | Action retenue | Impact utilisateur |
| --- | --- | --- |
| Clé privée compromise | Isoler le service, révoquer avec `KeyCompromise`, générer une nouvelle clé et un nouveau certificat, déployer et tester. | Interruption possible jusqu'au redémarrage ; l'ancien certificat est rejeté par les clients vérifiant la révocation. |
| Serveur remplacé | Émettre une nouvelle clé sur le serveur cible, déployer, tester, puis révoquer l'ancien certificat avec `Superseded`. | Bascule courte avec conservation du même nom DNS. |
| Nouveau service | Valider le nom DNS et les SAN, émettre le certificat, installer la racine chez les clients et tester. | Aucun impact sur les services existants. |

Commande de révocation exécutée par l'administrateur PKI :

```bash
step ca revoke <numero_de_serie> \
  --reason "private key compromise" \
  --reasonCode KeyCompromise \
  --ca-url https://ca.campus.test \
  --root ~/on-premise/pki/certs/Campus-CA-root.crt
```

Après une compromission, ne pas écraser immédiatement les fichiers actifs :
générer la nouvelle clé et le nouveau certificat dans un répertoire temporaire,
les vérifier, puis les déployer. Documenter le motif, les deux numéros de
série, l'heure, le service concerné et le contrôle TLS final.

## Mise à jour de l'exploitation

La procédure détaillée est ajoutée à
`~/on-premise/documentation/certificate-lifecycle.md` : seuil de
renouvellement, commandes Step CA, volumes à actualiser, validation par le
client Docker et révocation d'urgence.

## Livrable formateur

Présenter le scénario choisi, le contrôle d'échéance, le renouvellement, la
validation depuis le client Docker et la procédure de remplacement.

## Termes à retenir

- **Renouvellement** : nouveau certificat pour une clé encore fiable avant son
  expiration.
- **Révocation** : invalidation anticipée d'un certificat avant son échéance.
- **Remplacement** : certificat créé avec une nouvelle clé, nécessaire si
  l'ancienne clé ne peut plus être considérée comme sûre.
- **KeyCompromise** : motif de révocation indiquant une compromission réelle ou
  présumée de la clé privée.

## Docs associées

- [Générer les certificats des services](generer-certificats-services.md)
- [Déployer les certificats sur les services](deployer-certificats-services.md)
- [Valider TLS depuis une machine cliente](valider-tls-depuis-client.md)
