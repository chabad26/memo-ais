# Revue de l'itération


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/review.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.


## Éléments vérifiés

- OpenLDAP est la source des utilisateurs et des groupes.
- Samba utilise le backend `ldapsam` pour l'authentification SMB.
- Les partages `Commun`, `Developpement`, `Bureau-etudes` et
  `Administration` sont déclarés dans `samba-ad/config/smb.conf`.
- Les données OpenLDAP et Samba sont conservées dans des volumes Docker.
- Les procédures sont regroupées dans `operations.md`.
- Le plan de validation est décrit dans `validation.md`.

## Points restant à valider

- exécuter V-01 à V-06 avec des comptes de test dédiés ;
- réaliser un refus d'accès sur chaque partage sensible ;
- vérifier la désactivation LDAP selon le profil LAM utilisé ;
- démarrer un service complet à partir des volumes restaurés et mesurer le
  délai de reprise ;
- documenter la supervision et les alertes ;
- tester une restauration sur une autre machine.

## Choix d'architecture

Les projets Compose restent séparés :

- `openldap/` pour l'annuaire ;
- `ldap-account-manager/` pour l'interface ;
- `samba-ad/` pour le serveur de fichiers ;
- `wordpress-compose/` pour l'application Web ;
- `infrastructure-compose/` pour le démarrage commun d'OpenLDAP et LAM.

Le Compose fédérateur ne regroupe volontairement qu'OpenLDAP et LAM. Il fixe
le réseau `openldap_default`, les volumes LDAP et l'ordre de démarrage de LAM.
Samba reste séparé car il possède une image construite localement, son état et
un cycle de reprise distinct. WordPress reste également indépendant.

Le fichier `infrastructure-compose/README.md` précise que les anciens
Compose unitaires ne doivent pas être démarrés simultanément avec ce stack.

## Décision

L'itération est documentée mais reste partiellement validée tant que les tests
V-01 à V-06 n'ont pas été exécutés et consignés.
