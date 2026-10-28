# Validation de la confiance client


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/client-ca-validation.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.


## Objectif

Installer le certificat racine public de Campus CA sur un client Debian ou
Ubuntu, puis vérifier que le magasin de confiance système valide la chaîne TLS.

## Installation

Le script suivant utilise uniquement le certificat public versionné :

```bash
cd ~/on-premise
./pki/scripts/install-campus-ca-root.sh
```

Il installe `pki/certs/Campus-CA-root.crt` dans
`/usr/local/share/ca-certificates/`, exécute `update-ca-certificates`, puis
vérifie le certificat avec le bundle système. Il ne doit jamais être exécuté
sur une machine qui ne doit pas faire confiance à Campus CA.

## Vérifications

```bash
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt \
  /usr/local/share/ca-certificates/Campus-CA-root.crt
curl --fail --silent --show-error https://ca.campus.test/health
openssl s_client -connect ca.campus.test:443 \
  -servername ca.campus.test -CApath /etc/ssl/certs </dev/null
```

Le résultat attendu est `OK` pour OpenSSL, `{"status":"ok"}` pour l'endpoint
de santé et `Verify return code: 0 (ok)` pour la connexion TLS.

## Différence importante

La racine Campus CA est elle-même auto-signée, mais elle devient reconnue après
son import explicite dans le magasin de confiance. Un certificat de service
auto-signé qui n'a pas été distribué comme ancre de confiance reste refusé par
défaut.
