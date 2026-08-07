# Distribuer le certificat racine sur un client

## Objectif

Installer le certificat racine de `Campus CA` sur une machine cliente et
vérifier que le système reconnaît la chaîne de confiance de l'autorité.

Cette activité est individuelle. Elle concerne la machine cliente : elle ne
modifie ni la clé privée de la CA, ni le provisionneur, ni les certificats des
services.

## 1. Préparer la distribution

Le certificat racine public à distribuer est :

```text
~/on-premise/pki/certs/Campus-CA-root.crt
```

Avant de le copier vers un client, comparer son empreinte avec la valeur
obtenue sur le serveur Step CA par un canal fiable :

```bash
step certificate fingerprint ~/on-premise/pki/certs/Campus-CA-root.crt
```

Ne pas distribuer les fichiers de `~/.step/secrets/`, le fichier
`password.txt` ou le secret du provisionneur. Les clients ont seulement besoin
du certificat racine public.

## 2. Installer la racine sur un client Debian ou Ubuntu

Copier le certificat sur la machine cliente par un canal maîtrisé, par exemple
avec `scp`, un partage d'administration ou le dépôt interne :

```bash
scp ~/on-premise/pki/certs/Campus-CA-root.crt \
  utilisateur@client:/tmp/Campus-CA-root.crt
```

Sur le client, vérifier le certificat puis l'installer dans le magasin de
confiance système :

```bash
openssl x509 -in /tmp/Campus-CA-root.crt -noout -subject -issuer -dates
sudo install -m 0644 /tmp/Campus-CA-root.crt \
  /usr/local/share/ca-certificates/Campus-CA-root.crt
sudo update-ca-certificates
```

La commande `update-ca-certificates` doit signaler l'ajout d'un certificat. Le
client peut aussi utiliser le script versionné avec l'infrastructure :

```bash
cd ~/on-premise
./pki/scripts/install-campus-ca-root.sh
```

## 3. Vérifier le magasin de confiance

Vérifier la présence du certificat installé et sa reconnaissance par OpenSSL :

```bash
ls -l /usr/local/share/ca-certificates/Campus-CA-root.crt
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt \
  /usr/local/share/ca-certificates/Campus-CA-root.crt
```

Le résultat attendu de la seconde commande est :

```text
/usr/local/share/ca-certificates/Campus-CA-root.crt: OK
```

## 4. Vérifier la chaîne avec l'autorité

Le client doit résoudre le nom de la CA. Vérifier le DNS ou ajouter une entrée
temporaire dans `/etc/hosts` uniquement pour le laboratoire :

```bash
getent hosts ca.campus.test
curl --fail --silent --show-error https://ca.campus.test/health
openssl s_client -connect ca.campus.test:443 \
  -servername ca.campus.test \
  -CApath /etc/ssl/certs </dev/null
```

`curl` doit répondre `{"status":"ok"}` sans option `--cacert`. La sortie
d'OpenSSL doit finir par `Verify return code: 0 (ok)`. Cela prouve que les
outils utilisent le magasin système dans lequel Campus CA a été importée.

![Réponse du endpoint health de Campus CA depuis le client](../../assets/img/integration-distribuee-on-premise/it-6/client-curl-health-campus-ca.png)

## 6. CA connue et certificat auto-signé

| Situation | Chaîne de confiance | Résultat client |
| --- | --- | --- |
| Certificat de service signé par Campus CA, dont la racine est installée | Le certificat remonte à une racine connue du magasin système | Accepté si le nom DNS et les dates sont valides. |
| Certificat de service auto-signé non installé | Le certificat est sa propre racine, absente du magasin système | Refusé par défaut avec une erreur de certificat inconnu. |
| Certificat racine Campus CA | Il est techniquement auto-signé, comme toute racine | Accepté parce qu'il a été explicitement importé dans le magasin de confiance. |

Un certificat auto-signé n'est donc pas intrinsèquement invalide. Il n'est pas
reconnu tant que le client ne l'a pas choisi comme ancre de confiance. La
différence essentielle est la distribution contrôlée de cette confiance.

## 7. Livrable formateur

Présenter au formateur :

1. la méthode de distribution du certificat racine ;
2. l'empreinte vérifiée avant installation ;
3. les sorties de vérification du magasin et de la chaîne TLS ;
4. la distinction entre une CA reconnue et un certificat de service auto-signé
   non distribué.

## Résultat

La machine cliente fait confiance à Campus CA après l'import du certificat
racine public. Les outils système valident alors la chaîne TLS de la CA sans
recevoir manuellement un fichier `--cacert`.

## Termes à retenir

- **Magasin de confiance** : ensemble des autorités reconnues par le système
  ou une application.
- **Ancre de confiance** : certificat racine explicitement approuvé par le
  client.
- **Certificat auto-signé** : certificat signé par sa propre clé ; il est
  refusé tant qu'il n'est pas configuré comme ancre de confiance.
- **Chaîne de confiance** : suite de certificats permettant de relier un
  certificat de service à une racine reconnue.

## Ressources

- [Identifier les besoins en certificats numériques](inventorier-besoins-certificats.md)
- [Installer et initialiser une autorité Step CA](installer-initialiser-step-ca.md)
- [Documentation Step CA](https://smallstep.com/docs/step-ca/)
