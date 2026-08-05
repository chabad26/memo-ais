# Identifier les exigences de sauvegarde

## Objectif

Analyser les exigences du PCA et du PRA existants et les adapter aux services
déployés dans l'infrastructure du projet.

## Périmètre analysé

- OpenLDAP et LDAP Account Manager ;
- Samba et ses espaces de partage ;
- Postfix, Dovecot, Roundcube et MariaDB ;
- volumes Docker, fichiers Compose et configurations ;
- documentation technique et dépôt Git.

Aucun déploiement ni test de restauration n'est réalisé pendant cette
activité.

## 1. Évolution des exigences existantes

| Exigence du PCA/PRA | Source | Statut | Adaptation nécessaire |
|---|---|---|---|
| Sauvegarde nocturne des serveurs | PCA §7 | À adapter | Inclure les volumes Docker et vérifier le résultat chaque matin. |
| Copie hebdomadaire sur un support séparé | PCA §7 | À compléter | Chiffrer la copie et la conserver sur un emplacement distinct. |
| Vérification de l'espace disponible et des journaux | PCA §7 | Toujours applicable | Ajouter les journaux Docker, Postfix, Dovecot et LDAP. |
| Restauration du contrôleur de domaine | PRA §6 | À adapter | Distinguer le Samba AD historique du serveur Samba LDAP actuellement utilisé. |
| Restauration du serveur de fichiers | PRA §7 | Toujours applicable | Restaurer les partages Samba et vérifier les droits par groupe. |
| Restauration du serveur de messagerie | PRA §8 | À compléter | Ajouter Postfix, Dovecot, Roundcube, MariaDB et les boîtes Maildir. |
| Accès aux sauvegardes existantes | PRA §9 | Toujours applicable | Documenter les volumes, les fichiers Compose et les secrets locaux. |
| Vérification des services après reprise | PCA §11 / PRA §11 | À compléter | Ajouter des tests LDAP, SMB, IMAP, SMTP et Roundcube. |
| Révision annuelle des documents | PCA §11 / PRA §14 | Toujours applicable | Réviser aussi après chaque changement de volume ou de service. |

## 2. Nouvelles exigences

| Élément à sauvegarder | Contenu | Fréquence proposée | Priorité |
|---|---|---:|---:|
| OpenLDAP | volumes `ldap_data`, `ldap_config`, `ldap_backups` et export LDIF | Quotidienne | Critique |
| Identités LDAP | utilisateurs, groupes, OU et attributs de messagerie | Quotidienne | Critique |
| Partages Samba | volume `samba_share` et configuration `smb.conf` | Quotidienne | Haute |
| Boîtes Dovecot | volume `dovecot_mail` et index utiles | Quotidienne | Critique |
| File Postfix | volume `postfix_spool` si des messages sont en attente | Selon activité | Haute |
| Roundcube | volume `roundcube_config` et base `roundcube_db` | Quotidienne | Haute |
| Configurations | Compose, `.env.example`, Dovecot, Postfix, scripts et LAM | À chaque changement | Haute |
| Documentation | fichiers Markdown, procédures, PCA/PRA et journal | À chaque commit | Moyenne |
| Git | historique du dépôt et branches utiles | À chaque commit | Moyenne |

Les fichiers `.env` et les mots de passe ne doivent pas être copiés dans un
dépôt public. Ils doivent être sauvegardés dans un emplacement protégé et
chiffré, avec un accès limité aux administrateurs autorisés.

## 3. Règles de protection

- chiffrer les sauvegardes au repos et pendant leur transfert ;
- séparer au moins une copie du serveur de production et des volumes Docker ;
- limiter l'accès aux sauvegardes au groupe d'administration ;
- conserver les clés de chiffrement dans un emplacement distinct des archives ;
- documenter la durée de conservation et la date d'expiration de chaque copie ;
- journaliser les sauvegardes réussies, échouées, restaurées et supprimées.

## 4. Vérification et restauration

Une sauvegarde n'est considérée comme valide qu'après :

1. vérification automatique de sa présence et de son intégrité ;
2. contrôle de sa taille et de sa date ;
3. restauration périodique dans un environnement isolé ;
4. vérification des données et des droits restaurés ;
5. consignation du résultat dans le journal technique.

Les tests doivent couvrir au minimum :

- une recherche et une authentification LDAP ;
- un fichier de chaque partage Samba ;
- une boîte Dovecot et un message avec pièce jointe ;
- la base et la configuration Roundcube ;
- la reconstruction des services avec les fichiers Compose.

## 5. Priorités proposées

1. Sauvegarder OpenLDAP, les boîtes Dovecot et les partages Samba.
2. Protéger les configurations et les secrets nécessaires à la reprise.
3. Mettre en place une copie chiffrée et séparée.
4. Automatiser les contrôles d'intégrité et les alertes.
5. Réaliser un test de restauration complet et documenté.
6. Mettre à jour le PCA et le PRA avec les résultats du test.

## Livrable

Cette feuille constitue la proposition d'exigences à présenter au formateur.
Le déploiement, l'automatisation et les tests de restauration seront traités
dans les activités suivantes.
