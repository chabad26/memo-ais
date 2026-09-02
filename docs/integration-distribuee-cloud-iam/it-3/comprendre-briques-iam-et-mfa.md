# Comprendre les briques IAM et le MFA

!!! info "Activité - comprendre avant de configurer"
    Les commandes AWS de cette feuille sont des illustrations. Elles ne
    doivent être exécutées qu'avec un compte de laboratoire et après contrôle
    des permissions, des coûts éventuels et du périmètre du projet.

## Objectif

Comprendre les quatre briques de l'**Identity and Access Management** cloud et
le rôle de l'authentification multi-facteurs (**MFA**).

Le fil rouge `[I]` traverse tout le parcours AIS : du moindre privilège Linux
à l'IAM cloud. Le principe reste identique : n'accorder que les permissions
strictement nécessaires à la tâche.

## Les quatre briques

| Brique | Définition | Exemple de responsabilité |
| --- | --- | --- |
| Utilisateur | Identité d'une personne qui se connecte au cloud. | Administrateur, développeur ou opérateur identifié. |
| Groupe | Regroupement d'utilisateurs auquel on rattache des permissions communes. | Groupe `read-only`, `operators` ou `administrators`. |
| Rôle | Ensemble de permissions assumable temporairement par une identité autorisée. | Rôle de déploiement ou de lecture d'un bucket. |
| Identité de service | Identité utilisée par une application, un script ou une VM, pas par une personne. | Pipeline CI/CD ou sauvegarde vers Object Storage. |

Un utilisateur ne doit pas recevoir des droits d'administrateur simplement
parce qu'il appartient au projet. Les droits doivent correspondre à sa mission,
à sa durée et à son niveau de responsabilité.

## Où intervient le MFA ?

Le MFA ajoute un facteur supplémentaire au mot de passe, par exemple une
application d'authentification, une clé matérielle ou un mécanisme approuvé
par le fournisseur.

Il est prioritaire pour :

- le compte racine ou propriétaire du projet ;
- les comptes qui peuvent modifier l'IAM ;
- les comptes qui peuvent supprimer des données ou des ressources ;
- les comptes d'administration utilisés depuis une console web.

Le MFA ne remplace pas le moindre privilège : un compte MFA conserve des
permissions excessives si sa politique d'accès est trop large.

!!! warning "Humain et service"
    Une identité de service ne doit pas être partagée entre plusieurs
    personnes. Elle doit utiliser des permissions limitées, des credentials
    rotatifs et, lorsque c'est possible, un rôle temporaire plutôt qu'une clé
    longue durée.

## Principe du moindre privilège

Pour chaque identité, répondre à quatre questions :

1. Quelle action doit-elle réaliser ?
2. Sur quelles ressources cette action est-elle nécessaire ?
3. Pendant combien de temps le droit est-il requis ?
4. Comment vérifier et retirer ce droit ?

Exemple de matrice simple :

| Identité | Besoin | Droit minimal | Durée | Preuve |
| --- | --- | --- | --- | --- |
| Opérateur | Consulter l'état des VM | Lecture compute | Pendant l'exploitation | Liste des droits |
| Déploiement | Créer une VM de laboratoire | Compute ciblé | Pendant le déploiement | Journal CI ou terminal |
| Sauvegarde | Écrire dans un préfixe S3 | Écriture sur le préfixe prévu | Permanente mais rotative | Test d'envoi sans secret |
| Administrateur IAM | Gérer les identités | Droits IAM complets, MFA obligatoire | Exception contrôlée | Journal et revue |

## Commandes AWS illustratives

Ces commandes montrent la forme générale de l'API AWS IAM. Les valeurs entre
chevrons doivent rester des paramètres de laboratoire et ne doivent pas être
remplacées par des secrets dans le dépôt.

```bash
aws iam create-group --group-name <nom-du-groupe>
aws iam attach-group-policy \
  --group-name <nom-du-groupe> \
  --policy-arn <arn-de-la-politique>
aws iam create-user --user-name <nom-de-l-utilisateur>
aws iam add-user-to-group \
  --user-name <nom-de-l-utilisateur> \
  --group-name <nom-du-groupe>
```

Avant toute création, consulter les comptes existants et le contexte utilisé :

```bash
aws sts get-caller-identity
aws iam list-users
aws iam list-groups
aws iam list-roles
```

Pour un compte de laboratoire, utiliser un profil AWS séparé :

```bash
aws configure --profile iam-lab
AWS_PROFILE=iam-lab aws sts get-caller-identity
```

Ne jamais afficher `~/.aws/credentials`, une clé d'accès ou un token dans une
capture. La vérification doit porter sur l'identité utilisée et les permissions
observables, pas sur la valeur secrète elle-même.

## Mise en situation

À partir d'une petite équipe fictive, proposer :

| Personne ou service | Groupe ou rôle proposé | Accès refusé à vérifier |
| --- | --- | --- |
| Olivier, exploitation | `operators` | Modifier l'IAM ou supprimer le projet |
| Développeur | `developers` | Lire les secrets de production |
| Pipeline de déploiement | Identité de service dédiée | Utiliser une clé personnelle |
| Sauvegarde | Rôle ou identité limitée au bucket | Lire les autres buckets |

Documenter une autorisation, une restriction et une action de retrait. Une
bonne preuve peut être une liste de groupes ou de rôles sans secret, complétée
par une capture MFA où les codes et QR codes sont masqués.

## Application aux VM du module

Dans les VM OVH et Infomaniak, l'IAM cloud complète mais ne remplace pas :

- les comptes Linux et leurs groupes ;
- les clés SSH et la restriction UFW ;
- les comptes LDAP et les groupes applicatifs ;
- les permissions Docker et les secrets Compose ;
- la rotation et la sauvegarde des credentials.

La frontière doit être explicitement documentée : le fournisseur contrôle
l'identité du projet cloud, tandis que le client reste responsable des comptes,
des clés, des services, des données et des permissions déployées dans les VM.

## Preuves et nettoyage

Conserver :

- la matrice utilisateurs, groupes, rôles et identités de service ;
- la justification du MFA pour les comptes privilégiés ;
- des sorties CLI sans secrets ;
- la politique de moindre privilège retenue ;
- la preuve de suppression du compte ou du groupe de laboratoire.

Supprimer les ressources de test et révoquer les credentials temporaires après
l'exercice. Ne jamais commiter les fichiers AWS, les secrets, les tokens ou les
codes MFA.

## Ressources

- [AWS IAM - User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- [AWS CLI - IAM](https://docs.aws.amazon.com/cli/latest/reference/iam/)
- [OVHcloud - gestion des identités](https://help.ovhcloud.com/csm?id=csm_search&spa=1&q=IAM)
