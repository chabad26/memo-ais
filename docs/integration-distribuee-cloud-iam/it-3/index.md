# Itération 3 - Migrer et sécuriser les services (IAM)

!!! info "J5 après-midi - J6"
    Cette itération introduit la gestion des identités et des accès dans le
    cloud, puis applique le principe du moindre privilège aux utilisateurs,
    aux services et aux secrets.

## Objectif

Comprendre les quatre briques de l'IAM cloud, le rôle du MFA et la manière de
relier les droits accordés à une mission réelle.

## Feuille de l'itération

- [Comprendre les briques IAM et le MFA](comprendre-briques-iam-et-mfa.md)
- [Configurer l'IAM sur le premier fournisseur](configurer-iam-premier-fournisseur.md)
- [Auditer une configuration IAM](auditer-configuration-iam-moindre-privilege.md)
- [3.4 | Gestion des secrets avec SOPS](gestion-secrets-sops.md)
- [3.6 | PKI interne ou certificat public](pki-interne-ou-certificat-public.md)
- [3.7 | Appliquer le bon type de certificat selon le service](appliquer-certificat-selon-service.md)
- [3.8 | Livrable L3 : documentation IAM et chiffrement](livrable-l3-documentation-iam.md)

## État final attendu

- les utilisateurs humains sont distingués des identités de service ;
- les groupes facilitent l'attribution de droits cohérents ;
- les rôles et permissions sont accordés selon le moindre privilège ;
- le MFA protège les comptes à privilèges ;
- aucun mot de passe, token ou secret n'est publié dans Git ;
- les choix IAM sont justifiés et accompagnés de preuves non sensibles.
