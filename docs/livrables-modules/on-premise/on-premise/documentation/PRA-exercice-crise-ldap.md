# PRA exercice - crise OpenLDAP


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/PRA-exercice-crise-ldap.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.


## Perimetre

Ce document est une variante de travail pour l'exercice du 10 aout 2026. Il ne
remplace pas le `PRA.md` general du projet.

L'objectif est de reprendre OpenLDAP depuis une sauvegarde saine, puis de
redemarrer les services dependants dans l'ordre. Le serveur compromis reste
isole pour permettre une analyse ulterieure.

## Priorite de reprise

| Ordre | Service | Raison |
| --- | --- | --- |
| 1 | OpenLDAP | Source des comptes et groupes. |
| 2 | LDAP Account Manager | Administration apres validation LDAP. |
| 3 | Samba | Droits et acces dependant des groupes LDAP. |
| 4 | Messagerie | Authentification utilisateur dependante de LDAP. |
| 5 | Supervision | Diagnostic et preuve de reprise. |
| 6 | WordPress/MariaDB | Service moins directement touche dans ce scenario. |

## Chronologie de reference

| Etape | Heure debut | Heure fin | Duree | Resultat attendu |
| --- | --- | --- | --- | --- |
| Preparation et sauvegardes | 14:10 | 14:35 | 25 min | Plan relu, depot Borg controle, archive saine choisie. |
| Reconstruction OpenLDAP | 14:35 | 15:50 | 1 h 15 | Nouveau service ou volume propre prepare. |
| Validation OpenLDAP | 15:50 | 16:05 | 15 min | Bind, recherche LDAP et objets attendus. |
| Reprise LAM | 16:05 | 16:35 | 30 min | Interface et bind LDAP. |
| Reprise Samba | 16:35 | 17:50 | 1 h 15 | Partages et droits. |
| Reprise messagerie | 17:50 | 19:25 | 1 h 35 | Connexion et message de test. |
| Reprise supervision | 19:25 | 20:00 | 35 min | Journaux et tableaux de bord. |
| Controles applicatifs | 20:00 | 20:55 | 55 min | Verification progressive des dependances. |
| Cloture | 20:55 | 21:10 | 15 min | RTO/RPO et limites documentes. |

## Procedure de reprise LDAP

1. Confirmer que le serveur compromis reste isole.
2. Charger les variables de sauvegarde depuis l'emplacement protege.
3. Executer `borg check "$BORG_REPO"`.
4. Lister les archives avec `borg list "$BORG_REPO"`.
5. Choisir une archive anterieure a la compromission.
6. Extraire les donnees dans un repertoire temporaire controle.
7. Verifier la presence des fichiers `.ldif` et de la configuration utile.
8. Reconstruire OpenLDAP dans un environnement sain.
9. Importer utilisateurs et groupes.
10. Valider avec `ldapwhoami` et `ldapsearch`.

## Resultats simules

| Service | Etat | RTO simule | RPO simule | Verification |
| --- | --- | --- | --- | --- |
| OpenLDAP | Restaure | 1 h 55 | 18 h | `ldapwhoami`, `ldapsearch`. |
| LAM | Restaure | 2 h 25 | 18 h | Acces Web et bind LDAP. |
| Samba | Restaure | 3 h 40 | 18 h | Acces partage et refus hors groupe. |
| Messagerie | Partielle | 5 h 15 | 18 h | Authentification a revalider apres retour LDAP. |
| Supervision | Partielle | 5 h 50 | Non critique | Kibana accessible, alertes externes non validees. |
| WordPress/MariaDB | Non restaure | Non mesure | Non mesure | Temps insuffisant et priorite basse. |

## Cas conditionnel certificats

La compromission de certificats Roundcube n'a pas ete realisee dans ce poste.
Si elle avait ete annoncee, il aurait fallu ajouter une etape dediee :

1. isoler l'ancienne cle ;
2. relever le numero de serie du certificat ;
3. revoquer le certificat avec le motif `KeyCompromise` ;
4. generer une nouvelle paire cle/certificat ;
5. redeployer les fichiers TLS ;
6. verifier depuis un client que le nouveau certificat est presente.

La fiche `gestion-certificats-roundcube.md` conserve les commandes de reference
pour ce cas uniquement.

## Actions d'amelioration

| Priorite | Amelioration | Preuve attendue |
| --- | --- | --- |
| P1 | Preparer un compose de restauration LDAP isole. | Service LDAP restaure sans toucher la production. |
| P1 | Formaliser le choix de l'archive saine. | Date, nom d'archive et resultat `borg check`. |
| P2 | Formaliser les tests Samba. | Tableau utilisateur/groupe/partage. |
| P2 | Ajouter une checklist messagerie apres retour LDAP. | Connexion et message de test documentes. |
| P2 | Garder le cas certificats separe. | Procedure disponible, sans preuve declaree si non jouee. |
