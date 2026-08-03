# Gérer le cycle de vie des identités LDAP

## Objectif

Appliquer les opérations courantes d'administration des identités dans LDAP,
vérifier chaque modification et identifier les services qui devront être mis à
jour lorsqu'un utilisateur change de situation.

## Spécifications

- Travail individuel ou en binôme selon les consignes du formateur.
- Utiliser LDAP Account Manager.
- Réaliser les manipulations sur des comptes de laboratoire.
- Ne pas modifier ou supprimer un compte indispensable au fonctionnement de l'annuaire.
- Conserver une trace de chaque opération et de sa vérification.

## 1. Préparer la vérification

Vérifier que les conteneurs OpenLDAP et LAM sont actifs :

~~~bash
cd ~/on-premise/openldap
docker compose ps

cd ~/on-premise/ldap-account-manager
docker compose ps
~~~

Ouvrir LAM sur `http://localhost:8081` et se connecter avec le profil LDAP
du TP. Les utilisateurs existants de référence sont `amartin`, `bdupont`,
`cdurand`, `dbernard`, `erobert` et `oadmin`.

Pour éviter une suppression accidentelle, créer ou utiliser des comptes de
test dédiés aux opérations de départ et de suppression.

## 2. Arrivée d'un nouveau collaborateur

Dans LAM, ouvrir le type **Utilisateur**, sélectionner l'unité correspondant
au service d'affectation, puis créer le compte suivant :

| Attribut | Valeur de test |
| --- | --- |
| UID | `test.arrivee` |
| Prénom | Test |
| Nom | Arrivee |
| Unité | `ou=Developpement,ou=People,dc=embedded,dc=local` |
| Groupe | `grp-developpement` |
| Mot de passe | Mot de passe temporaire du TP |

1. Créer le compte avec les attributs obligatoires.
2. Définir le mot de passe temporaire.
3. Ajouter l'utilisateur au groupe de son service.
4. Enregistrer la fiche.
5. Rechercher `test.arrivee` dans LAM.
6. Vérifier son DN, son UID et son appartenance au groupe.

Vérification en ligne de commande :

~~~bash
docker compose exec openldap ldapsearch -x \
  -H ldap://localhost:3890 \
  -D "cn=admin,dc=embedded,dc=local" -W \
  -b "dc=embedded,dc=local" \
  "(uid=test.arrivee)" dn uid cn memberOf
~~~

![Recherche LDAP réussie après l'arrivée d'un collaborateur](../../assets/img/integration-distribuee-on-premise/it-2/arriv%C3%A9eajout%C3%A9.png)

*La recherche LDAP se termine par `result: 0 Success`, ce qui confirme que la commande a été exécutée correctement.*

## 3. Changement de service

Utiliser un compte de test, par exemple `test.mobilite` :

1. Ouvrir sa fiche utilisateur dans LAM.
2. Déplacer son entrée vers la nouvelle unité, par exemple
   `ou=Integration,ou=People,dc=embedded,dc=local`.
3. Retirer son appartenance au groupe de l'ancien service.
4. Ajouter son appartenance à `grp-integration`.
5. Enregistrer la modification.
6. Vérifier le nouveau DN et les groupes associés.

Un changement de service doit modifier à la fois la position de l'entrée dans
l'arborescence et les autorisations héritées des groupes. Le déplacement de
l'utilisateur seul ne modifie pas automatiquement ses droits.

![État de la liste des utilisateurs après les changements de groupe](../../assets/img/integration-distribuee-on-premise/it-2/changementgroupe%2Badmingrouperesponsable.png)

*La liste permet de contrôler l'état des comptes après les opérations de mobilité et de gestion des groupes.*

## 4. Promotion d'un responsable d'équipe

Utiliser un compte de test, par exemple `test.promotion` :

1. Ajouter l'attribut `title` avec la valeur `Responsable d'équipe`.
2. Renseigner éventuellement `description` ou `employeeType` selon le schéma retenu.
3. Conserver son groupe de service.
4. Ajouter le groupe fonctionnel de responsabilité, par exemple
   `grp-responsables` s'il a été validé par le formateur.
5. Enregistrer puis relire la fiche.

La promotion ne doit pas entraîner l'ajout de droits administrateur généraux.
Les droits doivent rester liés à un groupe fonctionnel documenté et justifié.

## 5. Départ d'un collaborateur

Dans la configuration LAM utilisée pour ce TP, les groupes sont des objets
`groupOfNames` complétés par `posixGroup`. L'écran **Utilisateur Unix** ne
permet donc pas toujours de retirer directement un membre, et la liste des
groupes peut être vide selon le profil LAM actif.

Pour un compte de test, par exemple `test.depart` :

1. Ouvrir la fiche de l'utilisateur et relever son DN complet.
2. Ouvrir le **Navigateur LDAP**, puis chaque groupe dont l'attribut `member`
   contient ce DN.
3. Retirer le DN de l'attribut `member` du groupe, ou utiliser l'action de
   modification des membres si elle est proposée par le profil LAM.
4. Enregistrer le groupe et vérifier que le DN n'est plus présent.
5. Conserver temporairement l'entrée utilisateur si une conservation légale ou
   opérationnelle est nécessaire.
6. Documenter la date, le motif et le responsable de l'opération.

Vérifier les groupes concernés avec :

~~~bash
docker compose exec openldap ldapsearch -x \
  -H ldap://localhost:3890 \
  -D "cn=admin,dc=embedded,dc=local" -W \
  -b "ou=Groups,dc=embedded,dc=local" \
  "(member=uid=test.depart,ou=Developpement,ou=People,dc=embedded,dc=local)" \
  dn cn member
~~~

Avant toute suppression, contrôler les ressources qui peuvent encore utiliser
le DN : fichiers, messagerie, certificats, tâches planifiées et services automatisés.

## 6. Désactivation puis suppression

Le profil LAM du TP ne propose pas de bouton général **Désactiver** pour un
compte utilisateur LDAP générique. Une désactivation fiable nécessite un
module de verrouillage configuré, par exemple Password Policy (`pwdAccountLockedTime`),
ou un attribut de verrouillage pris en charge par le service qui authentifie
les utilisateurs. Il ne faut donc pas prétendre qu'un compte est désactivé si
aucun mécanisme de verrouillage n'est configuré.

Pour l'activité actuelle, documenter honnêtement l'opération ainsi :

1. retirer les appartenances aux groupes d'accès depuis le Navigateur LDAP ;
2. vérifier que le compte ne possède plus de groupe donnant accès à un service ;
3. conserver l'entrée LDAP comme compte archivé si cela est nécessaire ;
4. faire valider la suppression par le responsable ;
5. supprimer l'entrée avec l'action de suppression du Navigateur LDAP ;
6. relancer une recherche LDAP et vérifier que le DN ne retourne plus de résultat.

Si le verrouillage par mot de passe est installé ultérieurement, la procédure
devra être complétée par l'activation du mécanisme de verrouillage, un test de
connexion refusée, puis la conservation de la preuve dans le journal technique.

La désactivation est préférable à la suppression lorsqu'elle est réellement
prise en charge par le schéma et le service d'authentification. Elle laisse le
temps de vérifier les dépendances. Dans le profil actuel, le retrait des groupes
est une mesure de réduction des accès, mais ce n'est pas une désactivation
complète du compte LDAP.

![Suppression réussie d'un utilisateur dans LAM](../../assets/img/integration-distribuee-on-premise/it-2/arriv%C3%A9eestrepartie.png)

*LAM confirme la suppression de l'utilisateur et affiche la liste restante des comptes.*

## 7. Vérifier les opérations

Recherche d'un utilisateur :

~~~bash
docker compose exec openldap ldapsearch -x \
  -H ldap://localhost:3890 \
  -D "cn=admin,dc=embedded,dc=local" -W \
  -b "ou=People,dc=embedded,dc=local" \
  "(uid=test.arrivee)" dn uid cn
~~~

Recherche des membres d'un groupe :

~~~bash
docker compose exec openldap ldapsearch -x \
  -H ldap://localhost:3890 \
  -D "cn=admin,dc=embedded,dc=local" -W \
  -b "ou=Groups,dc=embedded,dc=local" \
  "(cn=grp-developpement)" cn member gidNumber
~~~

Après chaque opération, conserver la date, le compte concerné, l'ancien et le
nouvel état, les groupes avant et après, la commande utilisée, le résultat
observé et la capture LAM correspondante si elle est nécessaire à la preuve.

## 8. Impacts sur les futurs services

| Service | Informations réutilisables | Mise à jour attendue |
| --- | --- | --- |
| Samba | UID, groupes, DN, appartenance au service | synchroniser les groupes et les accès aux partages |
| Messagerie | UID, nom, prénom, adresse, service, statut | créer, modifier ou bloquer la boîte aux lettres |
| Autorité de certification | identité, service, statut, DN | émettre, renouveler ou révoquer les certificats |
| Serveur de fichiers | groupes et appartenance aux équipes | appliquer ou retirer les droits d'accès |
| Supervision | comptes techniques et groupes d'administration | retirer les accès inutiles et maintenir les alertes |
| Scripts d'administration | UID, DN et événements de cycle de vie | automatiser les contrôles et conserver les journaux |

## 9. Réponses aux questions

### Quels accès supprimer lors du départ ?

Les accès au LDAP, aux groupes, aux partages Samba, à la messagerie, aux VPN,
aux certificats, aux outils d'administration et aux comptes techniques doivent
être supprimés ou révoqués. Les sessions actives et les clés ou jetons doivent
également être traités selon les procédures de chaque service.

### Quels accès conserver temporairement ?

Une copie d'archive ou une boîte aux lettres peut être conservée pendant la
durée définie par la politique de l'entreprise. Cette conservation doit être
réalisée sans laisser au salarié un accès actif et doit avoir un responsable,
une durée et une justification documentés.

### Pourquoi désactiver avant de supprimer ?

La désactivation bloque l'utilisation du compte tout en conservant son
historique, son DN et les informations nécessaires à l'audit. Elle permet de
vérifier les dépendances et de revenir en arrière. La suppression ne doit
intervenir qu'après validation.

### Quelles informations peuvent être réutilisées ?

Les services peuvent réutiliser le DN, l'UID, le nom et le prénom, l'adresse
électronique, le service, les groupes, le statut du compte, les numéros UID/GID
et les attributs liés aux certificats. Les mots de passe ne doivent jamais être
copiés dans les applications ou les journaux.

## 10. Bonnes pratiques retenues

- utiliser un identifiant stable et documenté ;
- gérer les droits par groupes plutôt que par utilisateur ;
- appliquer le moindre privilège ;
- séparer les comptes nominatifs des comptes techniques ;
- désactiver avant de supprimer lorsqu'un mécanisme de verrouillage est configuré ;
- à défaut, retirer immédiatement les groupes d'accès et documenter que le compte n'est pas désactivé au niveau LDAP ;
- vérifier les appartenances après chaque changement ;
- journaliser les opérations d'administration ;
- ne jamais mettre de mot de passe dans Git ou dans une capture publique ;
- faire valider les suppressions définitives.

## Livrables

Conserver dans la documentation :

- les opérations réalisées ;
- les vérifications LAM et LDAP ;
- les impacts sur Samba, la messagerie, les certificats et les scripts ;
- les réponses aux questions ;
- les bonnes pratiques retenues ;
- les captures et sorties de commandes utiles.

## Notions acquises

- Cycle de vie d'une identité ;
- désactivation et suppression ;
- appartenance aux groupes ;
- gestion des départs et mobilités ;
- dépendances entre LDAP et les services d'infrastructure.
