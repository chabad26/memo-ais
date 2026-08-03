# Activité 2.4 — Premier annuaire de l'entreprise

## Preuve de travail

***Premier annuaire de l'entreprise***

## Critères du formateur

| Critère | Preuve attendue dans cette activité |
| --- | --- |
| Arborescence LDAP adaptée à l'organisation | OUs séparées pour les personnes, les groupes, les services et les ordinateurs. |
| OUs, groupes et utilisateurs créés conformément au besoin | Entrées LDAP créées à partir du fichier LDIF et vérifiées par recherche. |
| Conventions de nommage cohérentes | Préfixes et noms identiques dans l'arborescence, les groupes et les comptes. |
| Fonctionnement vérifié avec les outils d'administration | Vérifications avec ldapadd, ldapmodify, ldapsearch et un outil graphique LDAP si disponible. |
| Fonctionnement vérifié par recherche LDAP | Requêtes ciblées sur les OUs, groupes et utilisateurs créés. |

## Objectif

Construire un premier annuaire LDAP correspondant à l'organisation d'Embedded Solutions, puis produire les preuves permettant de vérifier sa structure et son contenu.

L'annuaire centralisera les premières identités de l'entreprise :

- équipe de développement embarqué ;
- équipe d'intégration et de validation ;
- équipe infrastructure et administration ;
- direction et fonctions support ;
- comptes de service.

!!! note "Suffixe LDAP"
    L'exemple utilise le suffixe dc=embedded,dc=local. Si le formateur fournit un autre nom de domaine LDAP, remplacer ce suffixe dans les fichiers LDIF et les commandes.

## 1. Arborescence proposée

L'arborescence proposée est la suivante :

~~~text
dc=embedded,dc=local
├── ou=People
│   ├── ou=Developpement
│   ├── ou=Validation
│   ├── ou=Administration
│   └── ou=Direction
├── ou=Groups
├── ou=Services
└── ou=Computers
~~~

Cette organisation sépare :

- les personnes selon leur équipe ;
- les groupes de sécurité ;
- les comptes techniques des services ;
- les ordinateurs qui pourront être intégrés ultérieurement.

## 2. Conventions de nommage

| Objet | Convention | Exemple |
| --- | --- | --- |
| Organisation | Nom court de l'entreprise | Embedded Solutions |
| Domaine LDAP | Deux composants DNS | dc=embedded,dc=local |
| OUs | Nom en anglais, singulier logique | ou=Developpement |
| Utilisateur | prenom.nom ou role.prenom | alice.martin |
| Groupe | Préfixe grp- suivi du service | grp-developpement |
| Compte de service | Préfixe svc- suivi du service | svc-git |
| Ordinateur | Préfixe poste ou srv suivi d'un numéro | poste-01, srv-ldap-01 |
| Description | Rôle explicite et compréhensible | Équipe développement embarqué |

Règles retenues :

- pas d'espaces dans les identifiants ;
- pas d'accent dans les valeurs techniques ;
- noms en minuscules pour les UID, groupes et comptes de service ;
- un compte humain ne doit pas être utilisé comme compte de service ;
- les droits doivent être attribués aux groupes plutôt qu'aux utilisateurs individuellement.

## 3. Groupes et utilisateurs prévus

### Groupes

| Groupe | Rôle |
| --- | --- |
| grp-developpement | Membres de l'équipe de développement embarqué. |
| grp-validation | Membres de l'équipe d'intégration et de validation. |
| grp-administration | Administrateurs de l'infrastructure. |
| grp-direction | Direction et fonctions support autorisées. |
| grp-infrastructure | Comptes autorisés à exploiter les services techniques. |

### Utilisateurs de démonstration

| UID | OU cible | Groupe principal | Rôle |
| --- | --- | --- | --- |
| alice.martin | ou=Developpement | grp-developpement | Développement embarqué. |
| bob.dupont | ou=Developpement | grp-developpement | Développement embarqué. |
| claire.durand | ou=Validation | grp-validation | Intégration et validation. |
| olivier.admin | ou=Administration | grp-administration | Administration de l'infrastructure. |

Les noms sont des comptes de laboratoire. Les mots de passe ne doivent pas être écrits dans un dépôt Git.

## 4. Préparer le répertoire de travail

Créer un répertoire local pour les fichiers de l'activité :

~~~bash
mkdir -p ~/on-premise/ldap-annuaire
cd ~/on-premise/ldap-annuaire
~~~

Créer le fichier LDIF :

~~~bash
touch premier-annuaire.ldif
~~~

Le fichier LDIF doit être conservé dans le répertoire de travail et documenté dans le journal du projet.

## 5. Créer les OUs et les groupes

Ajouter dans premier-annuaire.ldif :

~~~ldif
dn: ou=People,dc=embedded,dc=local
objectClass: top
objectClass: organizationalUnit
ou: People
description: Personnes de l'entreprise

dn: ou=Developpement,ou=People,dc=embedded,dc=local
objectClass: top
objectClass: organizationalUnit
ou: Developpement
description: Equipe de developpement embarque

dn: ou=Validation,ou=People,dc=embedded,dc=local
objectClass: top
objectClass: organizationalUnit
ou: Validation
description: Equipe d'integration et de validation

dn: ou=Administration,ou=People,dc=embedded,dc=local
objectClass: top
objectClass: organizationalUnit
ou: Administration
description: Equipe infrastructure et administration

dn: ou=Direction,ou=People,dc=embedded,dc=local
objectClass: top
objectClass: organizationalUnit
ou: Direction
description: Direction et fonctions support

dn: ou=Groups,dc=embedded,dc=local
objectClass: top
objectClass: organizationalUnit
ou: Groups
description: Groupes de securite de l'entreprise

dn: ou=Services,dc=embedded,dc=local
objectClass: top
objectClass: organizationalUnit
ou: Services
description: Comptes techniques des services

dn: ou=Computers,dc=embedded,dc=local
objectClass: top
objectClass: organizationalUnit
ou: Computers
description: Ordinateurs integres a l'annuaire

dn: cn=grp-developpement,ou=Groups,dc=embedded,dc=local
objectClass: top
objectClass: posixGroup
cn: grp-developpement
gidNumber: 10001
description: Equipe de developpement embarque

dn: cn=grp-validation,ou=Groups,dc=embedded,dc=local
objectClass: top
objectClass: posixGroup
cn: grp-validation
gidNumber: 10002
description: Equipe d'integration et de validation

dn: cn=grp-administration,ou=Groups,dc=embedded,dc=local
objectClass: top
objectClass: posixGroup
cn: grp-administration
gidNumber: 10003
description: Equipe infrastructure et administration

dn: cn=grp-direction,ou=Groups,dc=embedded,dc=local
objectClass: top
objectClass: posixGroup
cn: grp-direction
gidNumber: 10004
description: Direction et fonctions support

dn: cn=grp-infrastructure,ou=Groups,dc=embedded,dc=local
objectClass: top
objectClass: posixGroup
cn: grp-infrastructure
gidNumber: 10005
description: Exploitation des services techniques
~~~

## 6. Créer les utilisateurs

Ajouter les utilisateurs dans le même fichier LDIF :

~~~ldif
dn: uid=alice.martin,ou=Developpement,ou=People,dc=embedded,dc=local
objectClass: top
objectClass: inetOrgPerson
objectClass: posixAccount
uid: alice.martin
cn: Alice Martin
sn: Martin
givenName: Alice
uidNumber: 11001
gidNumber: 10001
homeDirectory: /home/alice.martin
loginShell: /bin/bash
mail: alice.martin@embedded.local
ou: Developpement
title: Developpeuse embarquee
description: Compte de laboratoire - developpement embarque

dn: uid=bob.dupont,ou=Developpement,ou=People,dc=embedded,dc=local
objectClass: top
objectClass: inetOrgPerson
objectClass: posixAccount
uid: bob.dupont
cn: Bob Dupont
sn: Dupont
givenName: Bob
uidNumber: 11002
gidNumber: 10001
homeDirectory: /home/bob.dupont
loginShell: /bin/bash
mail: bob.dupont@embedded.local
ou: Developpement
title: Developpeur embarque
description: Compte de laboratoire - developpement embarque

dn: uid=claire.durand,ou=Validation,ou=People,dc=embedded,dc=local
objectClass: top
objectClass: inetOrgPerson
objectClass: posixAccount
uid: claire.durand
cn: Claire Durand
sn: Durand
givenName: Claire
uidNumber: 11003
gidNumber: 10002
homeDirectory: /home/claire.durand
loginShell: /bin/bash
mail: claire.durand@embedded.local
ou: Validation
title: Ingenieure validation
description: Compte de laboratoire - integration et validation

dn: uid=olivier.admin,ou=Administration,ou=People,dc=embedded,dc=local
objectClass: top
objectClass: inetOrgPerson
objectClass: posixAccount
uid: olivier.admin
cn: Olivier Admin
sn: Admin
givenName: Olivier
uidNumber: 11004
gidNumber: 10003
homeDirectory: /home/olivier.admin
loginShell: /bin/bash
mail: olivier.admin@embedded.local
ou: Administration
title: Administrateur infrastructure
description: Compte de laboratoire - administration

dn: cn=grp-developpement,ou=Groups,dc=embedded,dc=local
changetype: modify
add: memberUid
memberUid: alice.martin
memberUid: bob.dupont

dn: cn=grp-validation,ou=Groups,dc=embedded,dc=local
changetype: modify
add: memberUid
memberUid: claire.durand

dn: cn=grp-administration,ou=Groups,dc=embedded,dc=local
changetype: modify
add: memberUid
memberUid: olivier.admin

dn: cn=grp-infrastructure,ou=Groups,dc=embedded,dc=local
changetype: modify
add: memberUid
memberUid: olivier.admin
~~~

!!! warning "Mot de passe"
    Les entrées précédentes ne contiennent pas de mot de passe. La méthode d'authentification et le stockage des mots de passe doivent être définis avec le formateur avant la création de comptes utilisables.

## 7. Charger l'annuaire

Depuis le serveur LDAP, vérifier d'abord la configuration et la disponibilité du service :

~~~bash
systemctl status slapd
ldapwhoami -x
~~~

Charger les entrées :

~~~bash
ldapadd -x -D "cn=admin,dc=embedded,dc=local" -W -f premier-annuaire.ldif
~~~

Une erreur signale souvent :

- une entrée déjà existante ;
- un DN incorrect ;
- une O avec une lettre accentuée dans une valeur technique ;
- un suffixe différent de celui configuré sur le serveur ;
- un schéma LDAP ne prenant pas en charge un attribut utilisé.

## 8. Vérifier l'arborescence avec ldapsearch

Rechercher les OUs :

~~~bash
ldapsearch -x -LLL   -b "dc=embedded,dc=local"   "(objectClass=organizationalUnit)"   dn ou description
~~~

Rechercher les groupes :

~~~bash
ldapsearch -x -LLL   -b "ou=Groups,dc=embedded,dc=local"   "(objectClass=posixGroup)"   cn gidNumber memberUid description
~~~

Rechercher les utilisateurs :

~~~bash
ldapsearch -x -LLL   -b "ou=People,dc=embedded,dc=local"   "(objectClass=inetOrgPerson)"   uid cn mail ou title
~~~

Rechercher un utilisateur précis :

~~~bash
ldapsearch -x -LLL   -b "dc=embedded,dc=local"   "(uid=alice.martin)"   dn uid cn mail
~~~

## 9. Vérifier avec un outil d'administration

Si un outil graphique est disponible, par exemple Apache Directory Studio ou LDAP Account Manager :

1. créer une connexion vers le serveur LDAP ;
2. utiliser le suffixe dc=embedded,dc=local ;
3. s'authentifier avec le compte d'administration autorisé ;
4. afficher les OUs People, Groups, Services et Computers ;
5. ouvrir les groupes et vérifier leurs membres ;
6. ouvrir les utilisateurs et vérifier leur OU, leur UID et leur description ;
7. conserver une capture de l'arborescence et des objets.

Les commandes ldapsearch restent la preuve reproductible à conserver avec le journal de l'activité.

## État final attendu

L'annuaire fournit une première organisation cohérente de l'entreprise :

- les identités sont séparées par équipe ;
- les groupes correspondent aux besoins métiers ;
- les comptes techniques sont séparés des comptes humains ;
- les noms permettent une recherche et une administration compréhensibles ;
- les preuves montrent à la fois la structure graphique et les résultats de recherche LDAP.

## Ressources

- [OpenLDAP Software Documentation](https://www.openldap.org/doc/)
- [ldapsearch — OpenLDAP](https://www.openldap.org/software/man.cgi?query=ldapsearch)
