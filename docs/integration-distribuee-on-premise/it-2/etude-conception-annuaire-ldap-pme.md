# Étude de conception d'un annuaire LDAP pour une PME

## Objectif

Concevoir une organisation LDAP adaptée à une PME, justifier les choix
réalisés et comparer cette proposition avec celles des autres groupes.

## 1. Besoin identifié

| Service | Effectif |
| --- | ---: |
| Direction | 2 |
| Administration | 4 |
| Commercial | 6 |
| Support client | 8 |
| Développement logiciel | 8 |
| **Total** | **28** |

Chaque collaborateur possède un ordinateur portable, une adresse électronique,
un accès VPN et un espace de stockage partagé. Les responsables disposent de
droits supplémentaires.

## 2. Arborescence LDAP proposée

Le suffixe retenu pour l'exercice est `dc=pme,dc=local`.

~~~text
dc=pme,dc=local
├── ou=People
│   ├── ou=Direction
│   ├── ou=Administration
│   ├── ou=Commercial
│   ├── ou=SupportClient
│   └── ou=Developpement
├── ou=Groups
├── ou=Computers
├── ou=Services
│   ├── ou=Mail
│   ├── ou=VPN
│   └── ou=FileShares
└── ou=Disabled
~~~

### Justification

- `ou=People` contient les comptes nominatifs.
- Une OU par service rend les recherches et le rattachement initial lisibles.
- `ou=Groups` regroupe les groupes d'accès et les groupes fonctionnels.
- `ou=Computers` pourra accueillir les ordinateurs portables et leur inventaire.
- `ou=Services` sépare les comptes techniques des comptes personnels.
- `ou=Disabled` permet de conserver temporairement les comptes désactivés.

Les OU `Mail`, `VPN` et `FileShares` sont des emplacements logiques pour les
futurs objets techniques. Elles ne signifient pas que ces services sont déjà
déployés.

## 3. Groupes nécessaires

### Groupes de service

| Groupe | Membres | Usage |
| --- | ---: | --- |
| `grp-direction` | 2 | ressources de la Direction |
| `grp-administration` | 4 | ressources administratives |
| `grp-commercial` | 6 | ressources commerciales |
| `grp-support-client` | 8 | outils du support client |
| `grp-developpement` | 8 | dépôts et ressources de développement |

### Groupes transverses

| Groupe | Usage |
| --- | --- |
| `grp-tous-utilisateurs` | accès communs |
| `grp-vpn-utilisateurs` | accès VPN standard |
| `grp-stockage-utilisateurs` | espace partagé général |
| `grp-messagerie-utilisateurs` | accès à la messagerie |
| `grp-postes-portables` | rattachement logique des portables |

### Groupes de responsables

| Groupe | Usage |
| --- | --- |
| `grp-responsables` | responsables de service |
| `grp-responsables-direction` | responsable de la Direction |
| `grp-responsables-administration` | responsable de l'Administration |
| `grp-responsables-commercial` | responsable du Commercial |
| `grp-responsables-support-client` | responsable du Support client |
| `grp-responsables-developpement` | responsable du Développement logiciel |

Les droits supplémentaires sont attribués par ces groupes dédiés. Il ne faut
pas créer un groupe administrateur global pour les responsables de service.

## 4. Convention de nommage des utilisateurs

La convention retenue est l'initiale du prénom suivie du nom, en minuscules et
sans accent :

| Identité | UID |
| --- | --- |
| Alice Martin | `amartin` |
| Bruno Dupont | `bdupont` |
| Claire Durand | `cdurand` |

Règles complémentaires :

- aucun espace ni caractère spécial ;
- un homonyme reçoit un suffixe numérique, par exemple `amartin2` ;
- l'UID ne change pas lors d'un changement de service ;
- un compte technique utilise le préfixe `svc-`, par exemple `svc-backup` ;
- un ordinateur utilise le préfixe `pc-`, par exemple `pc-commercial-01` ;
- un groupe utilise le préfixe `grp-`.

## 5. Informations à enregistrer

| Information | Attribut ou usage | Justification |
| --- | --- | --- |
| Identifiant | `uid` | recherche et authentification |
| Prénom | `givenName` | identité affichée |
| Nom | `sn` | identité affichée |
| Nom complet | `cn` ou `displayName` | affichage dans les outils |
| Adresse électronique | `mail` | messagerie et notifications |
| Téléphone professionnel | `telephoneNumber` | contact interne |
| Service | `ou` ou attribut dédié | rattachement organisationnel |
| Fonction | `title` | rôle de la personne |
| Responsable | `manager` | hiérarchie éventuelle |
| Statut | attribut de verrouillage ou de gestion | actif ou sorti |
| Numéros Unix | `uidNumber`, `gidNumber` | si un service Unix le nécessite |
| Identité complète | DN LDAP | emplacement unique dans l'annuaire |

Les mots de passe ne doivent pas apparaître dans cette documentation. Les
équipements peuvent être décrits dans `ou=Computers` avec un propriétaire, un
numéro d'inventaire et un statut. Les comptes techniques sont placés dans
`ou=Services`.

## 6. Justification des droits

Un utilisateur appartient à son groupe de service et aux groupes transverses
nécessaires. Exemple pour une développeuse :

- `grp-developpement` ;
- `grp-tous-utilisateurs` ;
- `grp-messagerie-utilisateurs` ;
- `grp-vpn-utilisateurs` ;
- `grp-stockage-utilisateurs`.

Si elle devient responsable, on ajoute `grp-responsables-developpement`. Les
droits restent ainsi attribués par fonction, sont auditables et peuvent être
retirés lors d'une mobilité ou d'un départ.

## 7. Comparaison avec les autres propositions

Compléter ce tableau après la présentation des autres groupes :

| Point comparé | Notre proposition | Groupe 2 | Groupe 3 |
| --- | --- | --- | --- |
| Suffixe LDAP | `dc=pme,dc=local` | À compléter | À compléter |
| OU par service | Oui | À compléter | À compléter |
| Groupes responsables | Oui, séparés | À compléter | À compléter |
| Comptes désactivés | `ou=Disabled` | À compléter | À compléter |
| Comptes techniques séparés | `ou=Services` | À compléter | À compléter |
| Convention UID | initiale + nom | À compléter | À compléter |

### Points communs à rechercher

- une base DN et une OU utilisateurs ;
- une séparation entre utilisateurs et groupes ;
- des groupes correspondant aux services ;
- un identifiant utilisateur unique ;
- des droits spécifiques pour les responsables ;
- des informations réutilisables par la messagerie et le VPN.

### Différences à analyser

- une OU par service ou une OU unique ;
- droits portés par les groupes ou par des attributs individuels ;
- emplacement des comptes désactivés ;
- convention `prenom.nom`, initiale + nom ou identifiant numérique ;
- présence d'OU pour les ordinateurs et les comptes techniques.

## 8. Avantages et limites

### OU par service

**Avantages :** arborescence lisible, recherches simples et administration
facilitée.

**Limites :** un changement de service implique un déplacement d'entrée et les
OU peuvent devenir nombreuses.

### OU utilisateurs unique

**Avantages :** structure simple et peu de déplacements d'entrées.

**Limites :** le service est moins visible et doit être porté par les groupes
ou les attributs ; les erreurs sont plus difficiles à repérer.

### Gestion par groupes

**Avantages :** droits cohérents, changements rapides, audits facilités et
meilleure application du moindre privilège.

**Limites :** les groupes doivent être documentés et nettoyés lors des
mobilités ou des départs.

## Conclusion

La proposition sépare les utilisateurs, les groupes, les comptes techniques et
les équipements. Les droits sont attribués par groupes et les responsables
disposent de groupes fonctionnels dédiés. Cette organisation reste lisible et
réutilisable par les futurs services LDAP, VPN, messagerie et stockage partagé.

## Livrables

- arborescence LDAP proposée ;
- liste des groupes ;
- convention de nommage ;
- attributs utilisateurs ;
- justifications ;
- comparaison avec les autres groupes ;
- avantages et limites des organisations étudiées.

## Notions acquises

- Conception d'une arborescence LDAP ;
- groupes de service et groupes fonctionnels ;
- convention de nommage ;
- séparation des comptes utilisateurs, techniques et équipements.
