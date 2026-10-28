# PKI Campus CA


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/pki/README.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


Ce dossier regroupe les éléments publics nécessaires à l'utilisation de la CA
interne par les services du dépôt `on-premise`.

## Contenu versionné

| Chemin | Rôle |
| --- | --- |
| `certs/Campus-CA-root.crt` | Certificat racine public à importer dans les magasins de confiance. |
| `scripts/install-campus-ca-root.sh` | Installation et vérification de la racine sur un client Debian ou Ubuntu. |
| `scripts/issue-service-certificates.sh` | Délivrance interactive des certificats de service avec Step CA. |
| `service-certificate-plan.tsv` | Sujets, SAN et usages prévus pour chaque service. |
| `../documentation/certificate-inventory.md` | Inventaire analytique des services ayant besoin d'un certificat. |
| `../documentation/pki-architecture.md` | Architecture, rôles, renouvellement et révocation. |
| `../documentation/client-ca-validation.md` | Procédure et résultats attendus de validation côté client. |
| `../documentation/certificate-register.md` | Registre des certificats réellement délivrés. |

Empreinte SHA-256 de référence du certificat racine actuel :

```text
55883ddce49eb7234120fb08cf8f1b44b83c11ae68e8688e830620ff05eb9af4
```

Contrôler le certificat avant distribution :

```bash
step certificate fingerprint pki/certs/Campus-CA-root.crt
step certificate inspect pki/certs/Campus-CA-root.crt
```

## Éléments interdits dans ce dépôt

[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
provisionneur, les certificats clients et les clés privées des services ne
doivent jamais être ajoutés à Git. Les règles de `pki/.gitignore` les excluent
par défaut.

La CA est actuellement exécutée par le service `step-ca` de l'hôte. Sa
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
Avant la mise en production, ils seront transférés vers un hôte ou une VM dédiée
et sauvegardés dans un emplacement chiffré à accès restreint.

## Déploiement

1. Importer `Campus-CA-root.crt` dans les hôtes, postes et applications qui
   doivent joindre les services internes en TLS.
2. Délivrer un certificat distinct pour OpenLDAP, Postfix, Dovecot, Roundcube,
   LAM et Kibana, avec les noms DNS réellement utilisés.
3. Monter les certificats et clés privées via un mécanisme protégé, jamais par
   une variable d'environnement ou un fichier Compose versionné.
4. Activer TLS, tester la chaîne de confiance et documenter le renouvellement.

Au 7 août 2026, OpenLDAP, Postfix, Dovecot et Roundcube ont été validés avec la
chaîne Campus CA. LAM, Kibana et Elasticsearch restent à traiter selon le
registre `../documentation/certificate-register.md`.

## Délivrer les certificats de service

Après validation des noms DNS, exécuter :

```bash
./pki/scripts/issue-service-certificates.sh
```

[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
clés privées et relevés d'inspection sont écrits dans `pki/issued/`, exclu de
Git. La durée effective est celle autorisée par la politique Step CA et doit
être reportée dans `documentation/certificate-register.md`. Chaque dossier de
service contient aussi un fichier `*.fullchain.crt` : certificat de service
suivi du certificat intermédiaire, à présenter aux clients TLS.
