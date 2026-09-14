# Glossaire Cloud & IAM — Itération 3 : IAM et chiffrement

## Sujet

Sécuriser les identités, les secrets et les services, puis constituer le livrable IAM.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| IAM | Gestion des identités et de leurs autorisations. |
| Identité de service | Compte utilisé par un programme, à distinguer des comptes humains. |
| Groupe / rôle | Le groupe rassemble des identités ; le rôle définit des autorisations. |
| Moindre privilège | Limiter les droits à la mission et à la durée nécessaires. |
| MFA | Authentification combinant plusieurs facteurs distincts. |
| SOPS | Chiffrement des valeurs sensibles dans des fichiers structurés. |
| PKI interne | Chaîne de confiance administrée pour les usages internes. |
| Certificat public | Certificat dont la chaîne doit être reconnue par les clients visés. |
| Rotation / révocation | Remplacer un secret / retirer son droit d’usage. |

## Gestes et commandes à retenir

Ces rappels ne constituent pas une preuve d’exécution.

| Besoin | Commande ou action |
| --- | --- |
| Préparer la revue | Inventorier utilisateurs, groupes, rôles et identités de service. |
| Valider les droits | Tester une action autorisée et une action qui doit être refusée. |
| Contrôler les secrets | Vérifier les fichiers suivis et les règles d’exclusion sans afficher leurs valeurs. |
| Documenter TLS | Noter usage, émetteur, expiration, chaîne de confiance et procédure de renouvellement. |
| Livrable L3 | Rassembler matrice des droits, revue des accès, MFA, chiffrement et contrôle de l’âge des clés API. |

## Points de vigilance

Les commandes de configuration et les captures illustratives des cours ne prouvent pas une validation réelle. Ne jamais recopier une clé privée ou une valeur de récupération MFA.

## Docs associées

- [3.7 | Appliquer le bon type de certificat selon le service](../../../integration-distribuee-cloud-iam/it-3/appliquer-certificat-selon-service.md)
- [Auditer une configuration IAM](../../../integration-distribuee-cloud-iam/it-3/auditer-configuration-iam-moindre-privilege.md)
- [Comprendre les briques IAM et le MFA](../../../integration-distribuee-cloud-iam/it-3/comprendre-briques-iam-et-mfa.md)
- [Configurer l'IAM sur le premier fournisseur](../../../integration-distribuee-cloud-iam/it-3/configurer-iam-premier-fournisseur.md)
- [3.4 | Gestion des secrets avec SOPS](../../../integration-distribuee-cloud-iam/it-3/gestion-secrets-sops.md)
- [Itération 3 - Migrer et sécuriser les services (IAM)](../../../integration-distribuee-cloud-iam/it-3/index.md)
- [3.8 | Livrable L3 : documentation IAM et chiffrement](../../../integration-distribuee-cloud-iam/it-3/livrable-l3-documentation-iam.md)
- [3.6 | PKI interne ou certificat public : comment choisir](../../../integration-distribuee-cloud-iam/it-3/pki-interne-ou-certificat-public.md)
