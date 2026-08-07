# Valider TLS depuis une machine cliente

## Objectif

Depuis un poste client qui fait confiance à `Campus CA`, vérifier le certificat
présenté par chaque service : chaîne de confiance, nom DNS et période de
validité. Cette feuille est un contrôle après déploiement ; elle ne modifie
aucun service.

## Préparer le poste client Docker

Pour rejouer la validation hors cours, le client est un conteneur Debian
jetable. Son image installe seulement la racine publique Campus CA dans son
magasin de confiance, jamais les clés privées ni les certificats de service.

```bash
cd ~/on-premise/client-validation
docker compose build
docker compose run --rm tls-client
```

Le fichier `compose.yaml` associe les noms `*.embedded.local` à
`host-gateway`. Le conteneur atteint ainsi les ports publiés par les services
de l'hôte Docker, tout en utilisant les noms présents dans les SAN. Le résultat
attendu est un `Verify return code: 0 (ok)` pour chaque service et `HTTP 200`
pour Roundcube.

## Alternative : préparer un poste client classique

Le client doit résoudre les noms des services et posséder la racine de
confiance. Pour un client Debian/Ubuntu :

```bash
sudo install -m 644 Campus-CA-root.crt \
  /usr/local/share/ca-certificates/Campus-CA-root.crt
sudo update-ca-certificates
```

Dans le laboratoire, si aucun DNS n'est disponible, ajouter temporairement les
noms dans `/etc/hosts`, avec l'adresse IP du serveur de laboratoire :

```text
192.168.1.199 ldap.embedded.local smtp.embedded.local imap.embedded.local webmail.embedded.local
```

Ne jamais remplacer le nom DNS par l'adresse IP dans les tests TLS : les
certificats sont émis pour les noms `*.embedded.local`, pas pour cette adresse.

Définir ensuite le chemin de la racine et vérifier qu'elle est lisible :

```bash
CA=/usr/local/share/ca-certificates/Campus-CA-root.crt
test -r "$CA" && openssl x509 -in "$CA" -noout -subject -issuer -dates
```

## Vérifications réalisées

Exécuter les commandes suivantes depuis le client. L'option `-servername`
active SNI et `-verify_hostname` contrôle le nom réellement présenté par le
serveur.

```bash
# OpenLDAP en LDAPS
openssl s_client -connect ldap.embedded.local:636 \
  -servername ldap.embedded.local \
  -verify_hostname ldap.embedded.local -CAfile "$CA" </dev/null

# Dovecot en IMAPS
openssl s_client -connect imap.embedded.local:993 \
  -servername imap.embedded.local \
  -verify_hostname imap.embedded.local -CAfile "$CA" </dev/null

# Postfix en SMTP Submission avec STARTTLS
openssl s_client -starttls smtp -connect smtp.embedded.local:587 \
  -servername smtp.embedded.local \
  -verify_hostname smtp.embedded.local -CAfile "$CA" </dev/null

# Reverse proxy Nginx devant Roundcube
openssl s_client -connect webmail.embedded.local:8443 \
  -servername webmail.embedded.local \
  -verify_hostname webmail.embedded.local -CAfile "$CA" </dev/null
curl --fail --verbose https://webmail.embedded.local:8443/
```

Pour chaque commande `openssl`, relever :

- `Verify return code: 0 (ok)` : la chaîne Campus CA est reconnue ;
- `subject` et `X509v3 Subject Alternative Name` : le nom DNS couvert ;
- `notBefore` et `notAfter` : les dates de début et de fin de validité ;
- `issuer` : l'autorité intermédiaire Campus CA qui a délivré le certificat.

Pour isoler les informations à conserver dans le compte rendu, enregistrer le
certificat présenté puis l'inspecter :

```bash
openssl s_client -connect imap.embedded.local:993 \
  -servername imap.embedded.local -CAfile "$CA" -showcerts </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates -ext subjectAltName
```

Adapter uniquement le nom et le port pour LDAP, SMTP et Roundcube. La date est
conforme si l'heure du client est comprise entre `notBefore` et `notAfter`.

## Résultats au 7 août 2026

| Vérification | Résultat | Preuve attendue |
| --- | --- | --- |
| Chaîne de confiance OpenLDAP | Valide | `Verify return code: 0 (ok)` sur `ldap.embedded.local:636` |
| Chaîne de confiance Dovecot | Valide | `Verify return code: 0 (ok)` sur `imap.embedded.local:993` |
| Chaîne de confiance Postfix | Valide | `Verify return code: 0 (ok)` après `STARTTLS` sur `smtp.embedded.local:587` |
| Chaîne de confiance Roundcube | Valide | `Verify return code: 0 (ok)` et réponse HTTP `200` sur `webmail.embedded.local:8443` |
| Nom du serveur | Conforme | SAN égal au nom utilisé dans chaque commande |
| Dates de validité | Conformes au moment du contrôle | Les dates affichées encadrent la date du client |

![Contrôles de chaînes TLS et accès HTTPS réussis](../../assets/img/integration-distribuee-on-premise/it-6/tls-services-chaine-validee.png)

*Les validations LDAP, IMAPS et SMTP retournent `0 (ok)` ; Roundcube répond en
HTTPS. L'identifiant de session HTTP est masqué.*

## Anomalies possibles et solutions

Les erreurs ci-dessous constituent des cas de diagnostic à utiliser si le
formateur provoque une anomalie. Elles ne sont pas constatées dans les contrôles
valides présentés ci-dessus.

| Anomalie observée | Origine probable | Vérification | Solution proposée |
| --- | --- | --- | --- |
| `certificate has expired` | Certificat de service ou intermédiaire expiré ; horloge client erronée | Relever `notAfter` et contrôler `date -u` | Renouveler le certificat, déployer le `fullchain`, redémarrer le service ; corriger NTP si nécessaire. |
| `hostname mismatch` ou erreur de vérification du nom | Nom utilisé absent du SAN, mauvais certificat ou mauvais DNS | Afficher `subjectAltName` et `getent hosts <nom>` | Émettre un certificat avec le bon SAN, corriger le DNS ou utiliser le nom réellement couvert. |
| `unable to get local issuer certificate` | Racine Campus CA absente ou chaîne incomplète | Contrôler la racine installée et le certificat présenté | Installer la racine dans le magasin client et servir le fichier `*.fullchain.crt`. |
| `self-signed certificate` | Service configuré avec un certificat auto-signé | Relever `issuer` et la chaîne `-showcerts` | Remplacer par un certificat signé par Campus CA ; ne pas désactiver la vérification TLS. |
| Connexion refusée ou délai dépassé | Service arrêté, mauvais port, pare-feu ou publication Compose manquante | `ss -ltn`, `docker compose ps`, journaux du service | Redémarrer le service, corriger le port ou la règle réseau, puis refaire le contrôle TLS. |
| STARTTLS non proposé | Paramètres Postfix/Dovecot TLS non chargés | Lire la bannière et les journaux du conteneur | Vérifier les chemins certificat/clé, les montages et redémarrer le conteneur. |

Après toute correction, reprendre la commande `openssl s_client` concernée et
conserver la sortie montrant `Verify return code: 0 (ok)`.

## Livrable formateur

Présenter le tableau de résultats, les sorties de vérification de chaîne, les
SAN et dates relevés, puis le diagnostic et la correction appliquée au cas
d'erreur proposé.

## Termes à retenir

- **SNI** : nom envoyé au serveur TLS afin qu'il sélectionne le bon certificat.
- **SAN** : liste des noms DNS ou adresses couverts par un certificat.
- **Chaîne de confiance** : certificat serveur, éventuel intermédiaire et
  autorité racine reconnue par le client.
- **Vérification de nom** : contrôle que le nom demandé correspond à un SAN du
  certificat présenté.

## Docs associées

- [Distribuer le certificat racine sur un client](distribuer-certificat-racine-client.md)
- [Générer les certificats des services](generer-certificats-services.md)
- [Déployer les certificats sur les services](deployer-certificats-services.md)
