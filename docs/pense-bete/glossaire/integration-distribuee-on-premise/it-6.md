# Glossaire Intégration distribuée on-premise — Itération 6

## Sujet

Mise en place d'une autorité de certification interne Step CA et conception de
l'architecture PKI utilisée par les services on-premise.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| PKI | Infrastructure qui gère les certificats, les clés, la confiance et leur cycle de vie. |
| CA | Autorité de certification qui signe des certificats. |
| Step CA | Service Smallstep qui délivre et gère des certificats internes. |
| Certificat racine | Certificat public qui constitue l'ancre de confiance des clients. |
| Certificat intermédiaire | Certificat utilisé par la CA pour signer les certificats de services sans utiliser directement la clé racine. |
| Chaîne de confiance | Chemin de certificats allant du certificat serveur à une racine reconnue par le client. |
| Provisionneur | Mécanisme qui autorise une demande de certificat selon un rôle ou une politique. |
| JWK | Type de provisionneur basé sur une clé JSON, utilisé pour le provisionneur `admin` du laboratoire. |
| SAN | Subject Alternative Name : liste des noms DNS ou adresses couverts par un certificat. |
| Empreinte | Valeur SHA-256 qui permet de comparer un certificat reçu à une référence fiable. |
| Magasin de confiance | Emplacement où un système, un navigateur ou une application conserve les CA reconnues. |
| `update-ca-certificates` | Commande Debian/Ubuntu qui met à jour le magasin de confiance système. |
| Renouvellement | Émission d'un nouveau certificat avant l'expiration de l'ancien. |
| Révocation | Annulation anticipée d'un certificat compromis ou devenu invalide. |
| CRL | Liste publiée des certificats révoqués, à activer et tester avant une exploitation en production. |
| Certificat de service | Certificat présenté par un service TLS, par exemple OpenLDAP, Postfix ou Kibana. |
| Terminaison TLS | Composant qui reçoit une connexion TLS et la transmet au service interne selon une politique définie. |
| Chaîne complète | Certificat de service accompagné du certificat intermédiaire nécessaire à sa validation. |
| STARTTLS | Commande qui fait évoluer une connexion SMTP, IMAP ou LDAP vers TLS. |
| IMAPS | Variante d'IMAP chiffrée dès la connexion, habituellement sur le port 993. |

## Organisation retenue

```text
Campus CA (Step CA)
├── certificat racine public
│   └── importé chez les clients concernés
├── certificat intermédiaire
│   └── signe les certificats des services
├── provisionneur admin
│   └── réservé à l'administrateur PKI
└── certificats de service
    ├── OpenLDAP
    ├── Postfix et Dovecot
    ├── Roundcube et LAM
    └── Kibana
```

Dans le laboratoire, la configuration Step CA se trouve dans `~/.step`. Le
certificat racine public est aussi copié dans
`~/on-premise/pki/certs/Campus-CA-root.crt` afin d'être référencé par les
services et la documentation. Les clés privées et les fichiers de mot de passe
restent hors du dépôt Git.

## Manipulations faites

| Manipulation | Commande ou action |
| --- | --- |
| Initialiser la CA | `step ca init --name "Campus CA" --dns "ca.campus.test" --address ":443" --provisioner "admin"` |
| Démarrer la CA | Service `step-ca` avec le fichier `~/.step/config/ca.json`. |
| Contrôler le service | `sudo systemctl status step-ca --no-pager` |
| Lire les journaux | `sudo journalctl -u step-ca -n 50 --no-pager` |
| Tester la santé | `curl --cacert ~/.step/certs/root_ca.crt https://ca.campus.test/health` |
| Obtenir l'empreinte | `step certificate fingerprint ~/.step/certs/root_ca.crt` |
| Inspecter la chaîne | `step certificate inspect ~/.step/certs/root_ca.crt` |
| Vérifier TLS | `openssl s_client -connect ca.campus.test:443 -servername ca.campus.test -CAfile ~/.step/certs/root_ca.crt </dev/null` |
| Installer la racine sur un client | `./pki/scripts/install-campus-ca-root.sh` depuis `~/on-premise`. |
| Vérifier la confiance client | `curl https://ca.campus.test/health` sans `--cacert`, après installation de la racine. |
| Délivrer les certificats de service | `./pki/scripts/issue-service-certificates.sh` depuis `~/on-premise`. |
| Contrôler un certificat délivré | `step certificate inspect pki/issued/<service>/<service>.crt` |
| Valider Roundcube HTTPS | `openssl s_client -connect webmail.embedded.local:8443 -servername webmail.embedded.local -CAfile pki/certs/Campus-CA-root.crt </dev/null` |
| Valider IMAPS | `openssl s_client -connect imap.embedded.local:993 -servername imap.embedded.local -CAfile pki/certs/Campus-CA-root.crt </dev/null` |
| Valider SMTP STARTTLS | `openssl s_client -starttls smtp -connect smtp.embedded.local:587 -servername smtp.embedded.local -CAfile pki/certs/Campus-CA-root.crt </dev/null` |

## Valeurs de référence du laboratoire

| Élément | Valeur |
| --- | --- |
| Nom de la CA | `Campus CA` |
| URL de la CA | `https://ca.campus.test:443` |
| Provisionneur initial | `admin` |
| Certificat racine local | `~/.step/certs/root_ca.crt` |
| Certificat racine du dépôt | `~/on-premise/pki/certs/Campus-CA-root.crt` |
| Durée cible serveur | 90 jours |
| Alerte de renouvellement | 30 jours, puis 7 jours avant expiration |

## À ne jamais faire

- Exécuter `step-ca init` : l'initialisation est faite avec `step ca init`.
- Ajouter `~/.step/secrets/`, une clé privée ou `password.txt` à Git.
- Utiliser le secret du provisionneur sur un poste client.
- Ajouter le répertoire `pki/issued/`, les clés ou les certificats de service à Git.
- Importer le certificat racine sur un poste hors périmètre sans justification.
- Considérer un certificat valide si son nom DNS, sa chaîne ou ses dates ne
  correspondent pas à la connexion attendue.
- Confondre la racine auto-signée explicitement importée avec un certificat de
  service auto-signé non reconnu par le client.

## Docs associées

- [Installer et initialiser une autorité Step CA](../../../integration-distribuee-on-premise/it-6/installer-initialiser-step-ca.md)
- [Distribuer le certificat racine sur un client](../../../integration-distribuee-on-premise/it-6/distribuer-certificat-racine-client.md)
- [Générer les certificats des services](../../../integration-distribuee-on-premise/it-6/generer-certificats-services.md)
- [Déployer les certificats sur les services](../../../integration-distribuee-on-premise/it-6/deployer-certificats-services.md)
- [Concevoir l'architecture de certification](../../../integration-distribuee-on-premise/it-6/concevoir-architecture-certification.md)
- [Préparer la sécurisation TLS de la messagerie](../../../integration-distribuee-on-premise/it-4/securiser-messagerie-tls.md)
- [Pense-bête LDAP - itération 2](it-2.md)
