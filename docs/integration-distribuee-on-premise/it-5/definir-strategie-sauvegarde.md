# Définir la stratégie de sauvegarde

## Objectif

Définir une stratégie de sauvegarde compatible avec les exigences identifiées,
le PCA et le PRA de l'entreprise, avant toute mise en œuvre technique.

## 1. Principes retenus

La stratégie applique la règle **3-2-1** :

- trois copies des données, dont la copie de production ;
- deux supports ou emplacements distincts ;
- une copie hors de l'hôte Docker principal.

Les sauvegardes sont automatisées, chiffrées, contrôlées et accompagnées de
tests de restauration. Une simple copie présente sur le même disque que les
conteneurs ne constitue pas une sauvegarde suffisante.

## 2. Plan de sauvegarde

| Élément | Méthode prévue | Fréquence | Rétention | Chiffrement | Vérification |
|---|---|---|---|---|---|
| Annuaire LDAP | Export LDIF des données et de `cn=config`, plus sauvegarde des volumes LDAP | Export toutes les 6 h, volumes chaque nuit | 7 quotidiennes, 4 hebdomadaires, 6 mensuelles | Oui | Import LDAP mensuel dans un environnement isolé |
| Partages Samba | Sauvegarde incrémentale du volume `samba_share` et de `smb.conf` | Chaque nuit | 14 quotidiennes, 8 hebdomadaires, 6 mensuelles | Oui | Restauration mensuelle d'un fichier et contrôle des droits |
| Boîtes Dovecot | Sauvegarde cohérente du volume `dovecot_mail` | Chaque nuit | 14 quotidiennes, 8 hebdomadaires, 6 mensuelles | Oui | Restauration mensuelle d'une boîte et lecture IMAP |
| Base Roundcube | Export MariaDB cohérent | Chaque nuit | 7 quotidiennes, 4 hebdomadaires, 6 mensuelles | Oui | Import mensuel dans une base temporaire |
| Configuration Roundcube | Volume `roundcube_config` | Chaque nuit et après modification | 7 quotidiennes, 4 hebdomadaires | Oui | Démarrage d'un conteneur de test |
| Configurations Docker | Compose, Dockerfiles, scripts, Dovecot, Postfix, Samba et `.env.example` | À chaque commit | Historique Git et 6 archives mensuelles | Dépôt privé et archive chiffrée | Reconstruction trimestrielle des services |
| Secrets locaux | `.env`, clés et mots de passe nécessaires à la reprise | Après chaque modification | 4 versions précédentes | Oui, dépôt de secrets séparé | Contrôle d'accès trimestriel |
| Documentation | PCA, PRA, procédures, inventaire et journal technique | À chaque commit | Historique Git et 6 archives mensuelles | Archive chiffrée | Lecture et restauration trimestrielles |

## 3. Données exclues

Les éléments suivants peuvent être reconstruits et sont exclus des sauvegardes
quotidiennes :

- images Docker disponibles dans un registre ;
- conteneurs, réseaux Docker et couches de construction ;
- caches, fichiers temporaires et sessions Web Roundcube ;
- index Dovecot reconstructibles avec `doveadm force-resync` ;
- journaux déjà centralisés et arrivés à expiration ;
- file Postfix en fonctionnement normal, car sa restauration pourrait remettre
  en circulation des messages anciens ou déjà délivrés.

Les Dockerfiles, fichiers Compose, configurations et données persistantes ne
sont jamais considérés comme reconstructibles sans sauvegarde.

## 4. Chiffrement et accès

Les archives sont stockées dans un dépôt chiffré, par exemple avec un outil de
sauvegarde comme Restic. Les transferts utilisent SSH ou TLS.

- la clé de chiffrement est séparée du dépôt de sauvegarde ;
- seuls les administrateurs autorisés peuvent restaurer les données ;
- les mots de passe ne sont jamais placés dans Git en clair ;
- une copie de la clé est conservée dans un emplacement sécurisé prévu par le
  PRA ;
- la perte de la clé est intégrée aux risques, car elle rendrait les archives
  inutilisables.

## 5. Intégrité et supervision

Après chaque exécution, le système doit contrôler :

- le code retour de la sauvegarde ;
- la présence, la date et la taille de l'archive ;
- l'empreinte cryptographique ou le contrôle d'intégrité du dépôt ;
- l'espace disponible et la politique de rétention ;
- la transmission d'une alerte en cas d'échec.

Un contrôle complet du dépôt est réalisé chaque semaine. Le résultat est
consigné dans le journal technique et vérifié par l'administrateur.

## 6. Tests de restauration

| Périodicité | Test |
|---|---|
| Mensuelle | Restaurer un utilisateur LDAP, un fichier Samba, une boîte IMAP et la base Roundcube dans un environnement isolé. |
| Trimestrielle | Reconstruire l'ensemble des services depuis Git, les secrets protégés et les sauvegardes. |
| Annuelle | Réaliser un exercice PRA complet avec mesure des délais de reprise. |
| Après incident ou évolution majeure | Rejouer le test du service concerné et mettre à jour la procédure. |

Un test est réussi uniquement si les données sont lisibles, les droits sont
corrects et le service répond aux tests fonctionnels prévus.

## 7. Compatibilité avec le PCA et le PRA

| Service | Objectif existant | Réponse de la stratégie |
|---|---|---|
| Authentification | Reprise prioritaire, cible PRA de 2 h | Export LDAP fréquent, volumes nocturnes et test mensuel |
| Partage de fichiers | Reprise sous 8 h | Sauvegarde quotidienne et restauration régulière des droits |
| Messagerie | Reprise sous 24 h | Sauvegarde quotidienne des boîtes et de la base Roundcube |
| Sauvegardes | Retour sous 24 h | Dépôt séparé, chiffré, contrôlé et documenté |
| Documentation | Procédures disponibles pendant l'incident | Git et copie chiffrée hors de l'hôte principal |

La fréquence quotidienne limite généralement la perte maximale à 24 heures.
Pour LDAP, l'export toutes les six heures réduit ce risque sur le service
d'authentification prioritaire. Les délais devront être mesurés lors des tests
de restauration : ils ne sont pas considérés comme validés tant qu'un exercice
réel n'a pas été réalisé.

## 8. Justification

Cette stratégie concentre les sauvegardes sur les données irremplaçables et
évite de stocker les éléments Docker facilement reconstruits. Le chiffrement
protège les identités, messages, fichiers et secrets. Les contrôles d'intégrité
détectent une archive absente ou corrompue, tandis que les restaurations
régulières démontrent que les sauvegardes sont réellement exploitables.

## Livrable

Cette feuille constitue la stratégie à présenter au formateur. Sa mise en
œuvre devra produire des scripts, des journaux d'exécution et des preuves de
restauration.

