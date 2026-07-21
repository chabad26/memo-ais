# Glossaire Administration Windows — Activité 13

## Sujet

PKI interne, autorité de certification AD CS et activation de LDAPS.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| PKI | Infrastructure gérant certificats, clés, autorités et relations de confiance. |
| AD CS | Rôle Windows Server fournissant les services de certification. |
| Enterprise Root CA | Autorité racine intégrée à Active Directory. |
| Modèle de certificat | Paramètres communs définissant usage, durée, sécurité et droits d'inscription. |
| Auto-inscription | Délivrance ou renouvellement automatique d'un certificat par GPO. |
| LDAPS | LDAP protégé par TLS, généralement sur TCP 636. |
| SAN | Extension contenant notamment les noms DNS couverts par le certificat. |
| EKU | Extension définissant les usages autorisés, comme l'authentification serveur. |
| `RootDSE` | Entrée LDAP exposant les informations de base du service d'annuaire. |

## Contrôles essentiels

| Contrôle | Résultat attendu |
| --- | --- |
| Chaîne de confiance | Le certificat du contrôleur remonte à `CORP-ROOT-CA`. |
| Identité | Le FQDN `SRV-AD01.corp.local` figure dans le SAN. |
| Usage | L'EKU autorise l'authentification serveur. |
| Clé privée | Le contrôleur de domaine possède la clé associée au certificat. |
| Réseau | TCP 636 est accessible depuis le poste de validation. |
| Test LDAP | `LDP.exe` établit la session TLS et lit `RootDSE`. |

## Docs associées

- [Déployer une PKI interne et activer LDAPS](../../../admin-windows/activite13-deploiement-pki-ldaps.md)

