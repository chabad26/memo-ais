# Politique de messagerie

## 1. Objet

Cette politique définit les règles de fonctionnement de la future messagerie
interne d'Embedded Solutions. Elle servira de référence pour la configuration
de Postfix, Dovecot, Roundcube et des comptes OpenLDAP.

Les valeurs proposées sont adaptées à un environnement de travaux pratiques et
devront être confirmées par la direction avant une mise en production.

## 2. Domaine de messagerie

Le domaine de laboratoire retenu est :

```text
embedded.local
```

Le domaine devra être remplacé par un domaine officiellement détenu et
configuré dans DNS avant toute exposition Internet.

## 3. Convention de nommage des adresses

### Utilisateurs

Le format principal est :

```text
prenom.nom@embedded.local
```

Exemple :

```text
alice.martin@embedded.local
```

L'identifiant technique OpenLDAP reste court et cohérent avec l'existant,
par exemple `amartin`. L'adresse principale est stockée dans l'attribut LDAP
`mail`.

### Homonymes

En cas d'homonymie, utiliser successivement :

1. `prenom.nom2@embedded.local` ;
2. `p.nom@embedded.local` si la première forme est déjà utilisée.

Une adresse déjà attribuée ne doit jamais être réutilisée immédiatement après
le départ d'un collaborateur. Elle doit rester réservée pendant la période de
conservation définie par l'entreprise.

### Alias

Les alias sont documentés dans l'annuaire et ne remplacent pas l'adresse
principale. Ils peuvent être utilisés pour une ancienne adresse ou une
variation courante du nom.

## 4. Boîtes fonctionnelles

Les boîtes fonctionnelles sont associées à un besoin métier et non à une
personne :

| Adresse | Usage | Responsables |
| --- | --- | --- |
| `direction@embedded.local` | échanges avec la direction | groupe Direction |
| `administration@embedded.local` | échanges administratifs | groupe Administration |
| `commercial@embedded.local` | clients et prospects | groupe Commercial |
| `support@embedded.local` | demandes des clients | groupe Support |
| `bureau-etudes@embedded.local` | échanges liés aux études | groupe Bureau d'études |
| `informatique@embedded.local` | demandes infrastructure | groupe Informatique |

Les droits d'accès sont attribués à des groupes LDAP. L'accès à une boîte
fonctionnelle doit être nominatif, validé et révisé lors d'un changement de
service ou d'un départ.

Les boîtes fonctionnelles ne doivent pas être utilisées comme comptes
administrateurs techniques.

## 5. Listes de diffusion

Les listes de diffusion servent à envoyer un message à plusieurs personnes
sans créer une boîte partagée :

| Liste | Membres initiaux | Usage |
| --- | --- | --- |
| `dl-direction@embedded.local` | Direction | décisions et informations de direction |
| `dl-all@embedded.local` | tous les collaborateurs | communications générales |
| `dl-technique@embedded.local` | Développement, Intégration, Informatique | informations techniques |
| `dl-projet@embedded.local` | membres d'un projet | coordination temporaire |

Règles retenues :

- les listes sont administrées à partir des groupes LDAP ;
- `dl-all` est réservée aux communications importantes ;
- les envois externes vers une liste nécessitent une validation ;
- les membres sont revus à chaque changement d'organisation ;
- une liste temporaire possède une date d'expiration documentée.

Cette séparation évite de confondre une boîte fonctionnelle, qui reçoit et
conserve des messages, avec une liste de diffusion, qui distribue un message.

## 6. Taille des messages et pièces jointes

Limites proposées :

| Élément | Limite |
| --- | ---: |
| Message entrant ou sortant | 25 MiB |
| Pièces jointes cumulées | 20 MiB conseillés |
| Nombre de destinataires internes | 100 |
| Taille de boîte utilisateur initiale | 2 GiB |
| Taille de boîte fonctionnelle | 5 GiB |

La limite de 25 MiB inclut l'encodage MIME ; la taille réellement disponible
pour le fichier est donc légèrement inférieure. Les fichiers plus volumineux
doivent être déposés dans un espace partagé ou transmis par un lien contrôlé.

La limite doit être identique ou compatible dans Postfix, Dovecot, Roundcube
et les éventuels relais SMTP afin d'éviter des comportements différents selon
le chemin d'envoi.

## 7. Conservation des messages

### Boîtes utilisateur

- les messages restent disponibles tant que le compte est actif ;
- l'utilisateur est responsable du classement de sa boîte ;
- les messages anciens peuvent être archivés après 24 mois ;
- la suppression automatique n'est pas activée sans validation de la
  direction et du responsable légal.

### Départs

Lorsqu'un collaborateur quitte l'entreprise :

1. le compte est désactivé ;
2. les délégations et accès aux boîtes fonctionnelles sont retirés ;
3. la boîte est conservée temporairement selon la décision de l'entreprise ;
4. les messages nécessaires sont transférés vers une boîte fonctionnelle ou une
   archive contrôlée ;
5. la suppression est réalisée après validation et traçabilité.

### Boîtes fonctionnelles

Les boîtes fonctionnelles sont conservées tant que le besoin métier existe.
Lorsqu'elles sont remplacées, leur contenu est archivé avant suppression.

### Sauvegarde et archivage

Une sauvegarde technique permet de restaurer après incident. Elle ne constitue
pas automatiquement un archivage légal. Les durées d'archivage définitives
doivent être fixées avec la direction et les responsables concernés.

## 8. Sécurité et usage

- l'authentification utilise les identités OpenLDAP ;
- les connexions IMAP, SMTP submission et Webmail doivent être chiffrées ;
- l'accès SMTP au relais est réservé aux utilisateurs authentifiés ;
- les mots de passe ne sont jamais transmis dans les fichiers Compose versionnés ;
- les boîtes et listes sont gérées par groupes, avec le moindre privilège ;
- les transferts automatiques vers des adresses externes sont interdits par
  défaut ;
- les journaux sont conservés assez longtemps pour analyser un incident, sans
  remplacer une politique d'archivage.

## 9. Attributs LDAP à prévoir

| Attribut | Usage |
| --- | --- |
| `uid` | identifiant technique |
| `cn` | nom affiché |
| `mail` | adresse principale |
| `mailAlias` ou attribut retenu | alias |
| `memberUid` | membres des groupes et listes |
| `accountStatus` ou mécanisme de verrouillage | état du compte |

Le schéma retenu devra être vérifié avant l'installation de Postfix et
Dovecot. Les comptes techniques de recherche LDAP doivent être en lecture
seule.

## 10. Révision

Cette politique est révisée :

- avant la mise en production ;
- après un incident de messagerie ;
- après une évolution de l'annuaire ou des services ;
- au minimum une fois par an.

Toute modification doit être documentée dans Git et validée par le
responsable de l'infrastructure.
