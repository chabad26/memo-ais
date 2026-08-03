# Glossaire Intégration distribuée on-premise — Itération 2

## Sujet

Conception du premier annuaire LDAP de l'entreprise Embedded Solutions.

## LDAP en une phrase

LDAP est un protocole qui permet de consulter et d'administrer un annuaire centralisé.

Un annuaire LDAP stocke des identités et leurs informations dans une structure organisée. Les services peuvent ensuite utiliser cet annuaire pour authentifier les utilisateurs et vérifier leurs groupes.

On peut le comparer à un annuaire d'entreprise dans lequel chaque personne, groupe, service ou ordinateur possède une fiche identifiable.

## Termes à retenir

| Terme | Définition simple |
| --- | --- |
| LDAP | Protocole utilisé pour accéder à un annuaire d'identités et de ressources. |
| Annuaire LDAP | Base organisée qui contient des utilisateurs, groupes, services et équipements. |
| Entrée LDAP | Objet enregistré dans l'annuaire, par exemple un utilisateur ou une OU. |
| Attribut | Information stockée dans une entrée, par exemple uid, mail ou description. |
| DN | Distinguished Name : chemin complet et unique d'une entrée dans l'annuaire. |
| RDN | Relative Distinguished Name : première partie du DN qui identifie l'entrée dans son parent. |
| DC | Domain Component : composant du suffixe, par exemple dc=embedded. |
| Suffixe LDAP | Racine de l'annuaire, par exemple dc=embedded,dc=local. |
| OU | Organizational Unit : unité organisationnelle utilisée pour ranger les entrées. |
| CN | Common Name : nom courant d'une entrée, souvent utilisé pour un groupe. |
| UID | User ID : identifiant unique d'un utilisateur, par exemple alice.martin. |
| Groupe | Entrée qui rassemble plusieurs utilisateurs pour gérer une autorisation. |
| Compte technique | Identité utilisée par un service et non par une personne. |
| Schéma LDAP | Ensemble des règles qui définit les objets et attributs autorisés. |
| ObjectClass | Type d'une entrée LDAP, par exemple inetOrgPerson ou posixGroup. |
| LDIF | Format texte utilisé pour décrire, importer ou modifier des entrées LDAP. |
| Bind | Opération d'authentification auprès du serveur LDAP. |
| ldapsearch | Commande qui recherche et affiche des entrées LDAP. |
| ldapadd | Commande qui ajoute des entrées à un annuaire LDAP. |
| ldapmodify | Commande qui modifie des entrées existantes. |
| RootDSE | Entrée spéciale qui fournit des informations générales sur le serveur LDAP. |
| DN de base | Point de départ d'une recherche, par exemple dc=embedded,dc=local. |
| Groupe métier | Groupe correspondant à une équipe, par exemple grp-developpement. |
| Groupe de ressource | Groupe utilisé pour donner accès à une ressource, par exemple res-share-validation-rw. |

## Exemple de DN

~~~text
uid=alice.martin,ou=Developpement,ou=People,dc=embedded,dc=local
~~~

Lecture de droite à gauche :

~~~text
dc=embedded,dc=local
  └── ou=People
      └── ou=Developpement
          └── uid=alice.martin
~~~

Cet utilisateur est donc placé dans l'OU Developpement, elle-même placée dans People.

## Exemple d'entrée utilisateur

~~~ldif
dn: uid=alice.martin,ou=Developpement,ou=People,dc=embedded,dc=local
objectClass: inetOrgPerson
uid: alice.martin
cn: Alice Martin
sn: Martin
givenName: Alice
mail: alice.martin@embedded.local
ou: Developpement
description: Compte de laboratoire
~~~

Le DN indique l'emplacement. Les lignes suivantes décrivent l'utilisateur et ses attributs.

## Exemple d'entrée groupe

~~~ldif
dn: cn=grp-developpement,ou=Groups,dc=embedded,dc=local
objectClass: posixGroup
cn: grp-developpement
gidNumber: 10001
memberUid: alice.martin
memberUid: bob.dupont
~~~

Le groupe permet de regrouper plusieurs comptes et de réutiliser cette appartenance dans Samba, une application ou un autre service.

## Arborescence retenue

~~~text
dc=embedded,dc=local
├── ou=People
│   ├── ou=Developpement
│   ├── ou=Validation
│   ├── ou=Infrastructure
│   ├── ou=Administration
│   ├── ou=Direction
│   └── ou=Externes
├── ou=Groups
├── ou=Services
├── ou=Computers
└── ou=Certificates
~~~

## Conventions de nommage

| Objet | Format | Exemple |
| --- | --- | --- |
| Utilisateur | prenom.nom | alice.martin |
| Groupe métier | grp-equipe | grp-developpement |
| Groupe de service | svc-service-users | svc-git-users |
| Groupe de ressource | res-ressource-droit | res-share-developpement-rw |
| Compte technique | svc-service | svc-backup |
| Serveur | srv-role-numero | srv-ldap-01 |
| Poste | poste-numero | poste-01 |

Règles simples :

- utiliser des minuscules pour les identifiants techniques ;
- éviter les espaces et les accents dans les DN ;
- utiliser des noms explicites ;
- séparer les comptes humains et les comptes techniques ;
- donner les droits aux groupes plutôt qu'aux utilisateurs directement.

## Commandes de découverte

Ces commandes servent à consulter un annuaire existant. Elles ne sont pas à exécuter pendant l'activité de conception si le formateur demande uniquement une proposition.

~~~bash
ldapwhoami -x
ldapsearch -x -LLL -b "dc=embedded,dc=local" "(objectClass=organizationalUnit)" dn ou
ldapsearch -x -LLL -b "ou=People,dc=embedded,dc=local" "(uid=alice.martin)" dn uid cn mail
ldapsearch -x -LLL -b "ou=Groups,dc=embedded,dc=local" "(objectClass=posixGroup)" cn memberUid
~~~

## À ne pas confondre

| Élément | Différence |
| --- | --- |
| LDAP | Protocole d'accès à l'annuaire. |
| Annuaire LDAP | Données organisées consultées avec LDAP. |
| OU | Conteneur logique pour ranger des entrées. |
| Groupe | Ensemble d'utilisateurs utilisé pour les autorisations. |
| Utilisateur | Identité d'une personne. |
| Compte technique | Identité d'un service. |
| DN | Chemin complet d'une entrée. |
| UID | Identifiant court d'un utilisateur. |
| LDIF | Fichier texte décrivant les entrées et les modifications. |

## Docs associées

- [Concevoir l'annuaire LDAP](../../../integration-distribuee-on-premise/it-2/concevoir-annuaire-ldap.md)
- [Premier annuaire de l'entreprise](../../../integration-distribuee-on-premise/it-2/premier-annuaire.md)
- [Glossaire de l'itération 1](it-1.md)

## À retenir

LDAP sert à centraliser les identités et les groupes.

Le DN répond à la question « où se trouve cette entrée ? ».

L'UID répond à la question « quel est l'identifiant de cet utilisateur ? ».

Les groupes répondent à la question « à quelles équipes ou ressources cet utilisateur est-il rattaché ? ».

L'activité actuelle est une conception : aucune installation ni création réelle ne doit être faite avant validation du formateur.

