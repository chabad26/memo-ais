# Concevoir l'annuaire LDAP d'Embedded Solutions

## 1. Organisation de l'entreprise

L'entreprise conçoit, intègre et maintient des systèmes électroniques et logiciels.

Les principales catégories d'utilisateurs sont :

| Catégorie | Besoin principal |
| --- | --- |
| Développement embarqué | Accéder aux dépôts, aux outils de compilation et aux espaces de développement. |
| Intégration et validation | Accéder aux plateformes de test, aux résultats et aux espaces de validation. |
| Infrastructure | Administrer les serveurs, les services, les sauvegardes et la supervision. |
| Administration et direction | Accéder aux documents administratifs et aux services internes autorisés. |
| Prestataires | Accès temporaire et limité à des ressources identifiées. |
| Comptes techniques | Faire fonctionner un service sans représenter une personne. |

## 2. Services qui utiliseront l'annuaire

L'annuaire doit pouvoir être réutilisé par les services suivants :

| Service | Utilisation prévue de LDAP |
| --- | --- |
| Samba | Authentifier les utilisateurs et appliquer les groupes aux partages. |
| Messagerie | Authentifier les comptes et stocker les adresses électroniques. |
| Certificats | Associer une identité, un service ou un équipement à des informations d'annuaire. |
| Applications internes | Centraliser les connexions et les groupes autorisés. |
| Supervision | Identifier les comptes techniques et les responsables d'alertes. |
| VPN | Autoriser les utilisateurs ou groupes habilités. |
| Documentation et Git | Identifier les propriétaires et les responsables des ressources. |

!!! note "Principe de conception"
    L'annuaire stocke l'identité et les appartenances. Les droits précis sont ensuite appliqués par le service concerné, par exemple Samba ou une application interne.

## 3. Suffixe et arborescence proposée

Le suffixe proposé pour le laboratoire est :

~~~text
dc=embedded,dc=local
~~~

Si le formateur impose un autre suffixe, il devra être remplacé dans toute la documentation avant la mise en œuvre.

Arborescence proposée :

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
│   ├── ou=Global
│   ├── ou=Services
│   └── ou=Resources
├── ou=Services
├── ou=Computers
│   ├── ou=Servers
│   └── ou=Workstations
└── ou=Certificates
~~~

## 4. Rôle des unités organisationnelles

| OU | Contenu | Justification |
| --- | --- | --- |
| People | Comptes humains. | Séparer les personnes des comptes techniques. |
| People/Developpement | Développeurs embarqués. | Appliquer les groupes et règles du développement. |
| People/Validation | Intégration et validation. | Isoler les accès aux plateformes de test. |
| People/Infrastructure | Administrateurs système et réseau. | Contrôler les accès d'administration. |
| People/Administration | Fonctions administratives et commerciales. | Séparer les accès aux documents de gestion. |
| People/Direction | Direction et responsables. | Gérer les besoins spécifiques de validation et d'accès. |
| People/Externes | Prestataires et comptes temporaires. | Faciliter l'expiration et l'audit des accès externes. |
| Groups/Global | Groupes représentant les équipes. | Regrouper les utilisateurs par métier. |
| Groups/Services | Groupes liés aux applications et services. | Autoriser l'accès à une application ou une ressource. |
| Groups/Resources | Groupes associés aux partages ou ressources. | Préparer l'attribution des droits par groupe. |
| Services | Comptes techniques. | Éviter de mélanger comptes humains et comptes de service. |
| Computers | Objets représentant les équipements. | Préparer l'intégration des serveurs et postes. |
| Certificates | Objets ou informations liés à la PKI. | Préparer les usages certificats et identités machine. |

## 5. Groupes proposés

### Groupes métiers

| Groupe | Membres prévus | Utilisation |
| --- | --- | --- |
| grp-developpement | Développeurs embarqués | Dépôts, compilation et documentation technique. |
| grp-validation | Équipe d'intégration et validation | Plateformes et résultats de tests. |
| grp-infrastructure | Administrateurs système et réseau | Administration des services. |
| grp-administration | Fonctions administratives et commerciales | Ressources administratives. |
| grp-direction | Direction et responsables | Accès validés aux ressources de direction. |
| grp-externes | Prestataires autorisés | Accès temporaire et contrôlé. |

### Groupes de services

| Groupe | Rôle |
| --- | --- |
| svc-samba-users | Utilisateurs autorisés à ouvrir une session sur Samba. |
| svc-git-users | Utilisateurs autorisés à utiliser le service Git. |
| svc-vpn-users | Utilisateurs autorisés à utiliser le VPN. |
| svc-monitoring-admins | Administrateurs de la supervision. |
| svc-mail-users | Utilisateurs autorisés à utiliser la messagerie. |

### Groupes de ressources

| Groupe | Ressource |
| --- | --- |
| res-share-developpement-rw | Partage développement en lecture/écriture. |
| res-share-validation-rw | Partage validation en lecture/écriture. |
| res-share-commun-ro | Partage commun en lecture seule. |
| res-share-commun-rw | Partage commun en lecture/écriture. |
| res-build-admins | Administration de la ferme de compilation. |
| res-test-admins | Administration de la plateforme de tests. |

Les groupes métiers représentent les personnes. Les groupes de ressources représentent les autorisations. Cette séparation facilite l'évolution des droits sans modifier les comptes utilisateurs.

## 6. Utilisateurs de conception

Les utilisateurs suivants servent à valider la proposition :

| Identifiant | OU | Groupe métier | Fonction |
| --- | --- | --- | --- |
| alice.martin | People/Developpement | grp-developpement | Développement embarqué. |
| bob.dupont | People/Developpement | grp-developpement | Développement embarqué. |
| claire.durand | People/Validation | grp-validation | Intégration et validation. |
| olivier.admin | People/Infrastructure | grp-infrastructure | Administration de l'infrastructure. |
| direction.1 | People/Direction | grp-direction | Compte de démonstration de la direction. |
| prestataire.1 | People/Externes | grp-externes | Compte temporaire de prestataire. |

Ces identifiants sont des exemples de conception. Ils ne doivent pas être créés avant validation du formateur.

## 7. Comptes techniques éventuels

Les comptes techniques sont séparés des comptes humains et ne doivent pas être utilisés pour une connexion interactive.

| Compte | OU | Service | Usage |
| --- | --- | --- | --- |
| svc-samba | Services | Samba | Connexion ou intégration du service de fichiers selon la configuration retenue. |
| svc-git | Services | Git | Service de dépôt ou automatisation Git. |
| svc-backup | Services | Sauvegarde | Exécution des sauvegardes. |
| svc-monitoring | Services | Supervision | Collecte des métriques et envoi des alertes. |
| svc-mail | Services | Messagerie | Relais ou automatisation de messagerie. |
| svc-cert | Services | PKI | Automatisation contrôlée liée aux certificats. |

Principes :

- pas de mot de passe écrit dans la documentation publique ;
- pas de shell interactif si le service n'en a pas besoin ;
- droits limités au service concerné ;
- responsable et date d'expiration documentés ;
- rotation du secret prévue ;
- journalisation des utilisations privilégiées.

## 8. Convention de nommage

### Utilisateurs

Format retenu :

~~~text
prenom.nom
~~~

Exemples :

~~~text
alice.martin
bob.dupont
claire.durand
~~~

Cas particuliers :

- les homonymes utilisent une règle validée, par exemple prenom.nom2 ;
- les comptes externes gardent un identifiant identifiable et une date d'expiration documentée ;
- les comptes d'administration utilisent un préfixe distinct, par exemple adm.prenom.nom ;
- un compte technique utilise le préfixe svc-.

### Groupes

Format retenu :

~~~text
grp-<equipe>
svc-<service>
res-<ressource>-<niveau>
~~~

Exemples :

~~~text
grp-developpement
svc-vpn-users
res-share-developpement-rw
~~~

Le suffixe de permission doit rester explicite :

- ro : lecture seule ;
- rw : lecture et écriture ;
- admin : administration ;
- use : utilisation d'un service.

### OUs

Les OUs utilisent des noms courts et stables :

~~~text
People
Groups
Services
Computers
Certificates
~~~

Les caractères accentués, espaces et noms dépendant d'une personne sont évités dans les valeurs techniques.

## 9. Attributs utilisateurs à prévoir

| Attribut LDAP | Utilisation |
| --- | --- |
| uid | Identifiant de connexion unique. |
| cn | Nom commun affiché. |
| sn | Nom de famille. |
| givenName | Prénom. |
| displayName | Nom affiché dans les applications. |
| mail | Adresse électronique. |
| telephoneNumber | Numéro professionnel si nécessaire. |
| title | Fonction ou rôle. |
| ou | Équipe ou unité de rattachement. |
| employeeNumber | Identifiant interne si l'entreprise en définit un. |
| employeeType | Salarié, prestataire ou compte de service. |
| preferredLanguage | Langue préférée si une application l'utilise. |
| description | Information courte et non sensible. |
| accountStatus | État documentaire : actif, suspendu ou à désactiver. |
| pwdChangedTime | Date de changement de mot de passe selon le schéma utilisé. |

Les mots de passe, certificats et attributs sensibles doivent respecter le schéma LDAP et la politique de sécurité retenue. Ils ne sont pas renseignés pendant cette activité de conception.

## 10. Réutilisation par les futurs services

### Samba

Samba pourra réutiliser :

- uid pour identifier l'utilisateur ;
- les groupes métiers pour les appartenances ;
- les groupes de ressources pour les partages ;
- mail et displayName pour l'affichage.

### Certificats

La PKI pourra réutiliser :

- cn et displayName pour identifier une personne ;
- uid ou employeeNumber pour le lien avec l'identité ;
- les groupes pour limiter les demandes de certificats ;
- l'OU Computers pour les certificats machine.

### Messagerie

La messagerie pourra réutiliser :

- uid comme identifiant ;
- mail comme adresse principale ;
- givenName, sn et displayName pour le carnet d'adresses ;
- les groupes pour les listes de diffusion.

### Applications internes

Une application pourra utiliser :

- uid pour la connexion ;
- les groupes pour l'autorisation ;
- title et ou pour les rôles métier ;
- accountStatus et les dates de validité pour contrôler l'accès.

## 11. Schéma de synthèse

~~~text
Entreprise Embedded Solutions
└── Annuaire LDAP : dc=embedded,dc=local
    ├── People
    │   ├── Developpement
    │   ├── Validation
    │   ├── Infrastructure
    │   ├── Administration
    │   ├── Direction
    │   └── Externes
    ├── Groups
    │   ├── Global
    │   ├── Services
    │   └── Resources
    ├── Services
    ├── Computers
    │   ├── Servers
    │   └── Workstations
    └── Certificates
~~~

## 12. Validation de la conception

Présenter au formateur :

- le suffixe LDAP proposé ;
- le schéma de l'arborescence ;
- la liste des OUs ;
- la liste des groupes ;
- les utilisateurs de démonstration ;
- les comptes techniques envisagés ;
- les conventions de nommage ;
- les attributs nécessaires aux futurs services ;
- les points restant à arbitrer.

Aucune commande d'installation, de création ou de recherche LDAP n'est exécutée pendant cette activité.

## Livrable conservé

Le document de conception doit contenir :

- le schéma de l'arborescence LDAP ;
- la liste des unités organisationnelles ;
- la liste des groupes ;
- la liste des utilisateurs de conception ;
- la liste des comptes techniques éventuels ;
- les conventions de nommage ;
- les attributs utilisateurs ;
- les usages futurs pour Samba, les certificats et la messagerie ;
- les décisions validées par le formateur.

## Questions à faire valider

- Le suffixe dc=embedded,dc=local est-il accepté ?
- Les noms des équipes correspondent-ils à l'organisation présentée ?
- Les comptes externes doivent-ils être séparés dans une autre base ?
- Les groupes de ressources doivent-ils suivre un modèle particulier ?
- Samba utilisera-t-il directement LDAP ou un mécanisme intermédiaire ?
- Quelle solution de messagerie sera intégrée ?
- La PKI utilisera-t-elle LDAP pour publier les certificats ?
- Quels attributs sont obligatoires dans le schéma retenu ?
- Quelle politique de mot de passe et d'expiration doit être appliquée ?
- Quels comptes techniques sont réellement nécessaires ?

## Ressources

- [A brief introduction to LDAP](https://www.openldap.org/doc/admin26/guide.html)
- [OpenLDAP Software 2.6 Administrator's Guide](https://www.openldap.org/doc/admin26/)
- [Premier annuaire de l'entreprise](premier-annuaire.md)
