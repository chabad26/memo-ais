# Rapport de restauration PRA - incident OpenLDAP


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/rapport-restauration-pra.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.


## Contexte

Ce rapport documente l'exercice de restauration realise apres la gestion de
crise OpenLDAP. Le binome dispose de **7 heures** pour restaurer le maximum de
services possible en appliquant le PRA et le plan d'actions valide.

Un service est declare restaure uniquement lorsque son fonctionnement a ete
verifie. Les services non remis en production doivent etre justifies.

> **Rapport simule** : les horaires, etats et preuves ci-dessous constituent
> un scenario de reference. Ils devront etre remplaces par les mesures et
> sorties de commandes de la configuration cible.

## Documents utilises

| Document | Utilisation |
| --- | --- |
| `memo-ais/docs/integration-distribuee-on-premise/it-8/restaurer-infrastructure-pra.md` | Feuille pedagogique de restauration PRA. |
| `documentation/incident-majeur-ldap.md` | Plan d'actions valide pendant la gestion de crise. |
| `documentation/PRA-exercice-crise-ldap.md` | Priorites et procedures de reprise propres a l'exercice. |
| `documentation/PCA-exercice-crise-ldap.md` | Objectifs de continuite propres a l'exercice. |
| `documentation/restore-procedure.md` | Restauration BorgBackup en environnement isole. |
| `documentation/backup-strategy-validation.md` | Estimation initiale RTO/RPO du scenario LDAP. |
| `documentation/inventory.md` | Inventaire des services et dependances. |

## Chronologie de restauration

Hypothese de depart : exercice demarre le **10 aout 2026 a 14:10 CEST**.
Fin des 7 heures : **10 aout 2026 a 21:10 CEST**.

| Etape | Heure debut | Heure fin | Duree | Resultat |
| --- | --- | --- | --- | --- |
| Preparation et sauvegardes | 14:10 | 14:35 | 25 min | Rappel du plan, `borg check`, `borg list` et archive saine. |
| Reconstruction OpenLDAP | 14:35 | 15:50 | 1 h 15 | Nouveau serveur ou nouveaux volumes. |
| Validation OpenLDAP | 15:50 | 16:05 | 15 min | Bind et recherche LDAP. |
| Reprise LDAP Account Manager | 16:05 | 16:35 | 30 min | Interface d'administration. |
| Reprise Samba | 16:35 | 17:50 | 1 h 15 | Partages et droits. |
| Reprise messagerie | 17:50 | 19:25 | 1 h 35 | Postfix, Dovecot, Roundcube. |
| Reprise supervision | 19:25 | 20:00 | 35 min | Journaux et tableaux de bord. |
| Controle des services dependants | 20:00 | 20:55 | 55 min | Redemarrage surveille et verification applicative. |
| WordPress/MariaDB et cloture | 20:55 | 21:10 | 15 min | WordPress non restaure ; synthese RTO/RPO. |

## Etapes realisees

| Etape | Commandes ou actions | Preuve conservee | Etat |
| --- | --- | --- | --- |
| Controle BorgBackup | `borg check`, `borg list` | A completer | A completer |
| Restauration LDAP isolee | Voir `restore-procedure.md` | A completer | A completer |
| Reconstruction OpenLDAP | `docker compose config`, `docker compose up -d` | A completer | A completer |
| Validation LDAP | `ldapwhoami`, `ldapsearch` | A completer | A completer |
| Reprise LAM | `docker compose ps`, test Web | A completer | A completer |
| Reprise Samba | `docker compose ps`, `testparm -s`, acces partage | A completer | A completer |
| Reprise messagerie | journaux Postfix/Dovecot/Roundcube, test message | A completer | A completer |
| Reprise supervision | controle Kibana et index `logs-infrastructure*` | A completer | A completer |

## Services remis en production

| Service | Restaure | Verification | Heure de retour | Commentaire |
| --- | --- | --- | --- | --- |
| OpenLDAP | Oui, simule | `ldapwhoami` et `ldapsearch` reussis | 16:05 | Bind, base et groupes presents. |
| LDAP Account Manager | Oui, simule | Connexion Web et bind LDAP valides | 16:35 | Retabli apres OpenLDAP. |
| Samba | Oui, simule | Acces `Commun` autorise et refus hors groupe | 17:50 | Droits dependants de LDAP valides. |
| Messagerie | Partiel, simule | Authentification a revalider apres retour LDAP | 19:25 | Tests applicatifs a completer. |
| Supervision | Partiel, simule | Kibana accessible et journaux presents | 20:00 | Alertes externes non validees. |
| WordPress/MariaDB | Non, simule | Non teste | Non mesure | Temps consomme par les priorites critiques. |

> **Cas conditionnel certificats** : si l'incident avait aussi inclus une cle
> ou un certificat compromis, une etape supplementaire aurait ete ajoutee :
> isoler l'ancienne cle, revoquer le certificat, generer une nouvelle paire,
> redeployer TLS et verifier le certificat depuis un client.

## Services restant indisponibles

| Service | Cause | Impact | Action corrective |
| --- | --- | --- | --- |
| WordPress/MariaDB | Temps insuffisant apres les services prioritaires. | Service Web non verifie. | Prevoir une plage dediee ou un second scenario PRA. |

## Mesure du RTO

Dans ce scenario, le chronometre RTO demarre a 14:10, au lancement de
l'exercice. Le RTO simule correspond donc au temps ecoule jusqu'a la
verification fonctionnelle du service.

| Service | Objectif PRA/PCA | RTO observe | Conforme | Commentaire |
| --- | --- | --- | --- | --- |
| OpenLDAP | PRA : 2 h ; PCA : 4 h | 1 h 55, simule | Oui | Priorite 1, marge de 5 min. |
| Samba | PRA : selon ordre de reprise ; PCA : service metier prioritaire | 3 h 40, simule | Oui | Depend de LDAP. |
| Messagerie | PRA/PCA : 24 h dans les documents projet | 5 h 15, partiel | Oui | Tests applicatifs a completer apres retour LDAP. |
| Supervision | PRA/PCA : 48 h dans les documents projet | 5 h 50, partiel | Oui | Alertes externes a completer. |

## Estimation du RPO

Le RPO observe correspond a l'ecart entre l'heure de la derniere sauvegarde
saine restauree et l'heure estimee de l'incident.

| Donnee | Derniere sauvegarde saine | Heure incident estimee | RPO observe | Commentaire |
| --- | --- | --- | --- | --- |
| Donnees LDAP | 09 aout 2026 20:10 | 10 aout 2026 14:10 | 18 h, simule | Comptes, groupes et OU. |
| Configuration LDAP | 09 aout 2026 20:10 | 10 aout 2026 14:10 | 18 h, simule | Compose, volumes et configuration restauree. |
| Donnees Samba | 09 aout 2026 20:10 | 10 aout 2026 14:10 | 18 h, simule | Documents partages. |
| Donnees messagerie | 09 aout 2026 20:10 | 10 aout 2026 14:10 | 18 h, simule | Maildir et base Roundcube. |

## Comparaison aux objectifs

| Critere | Objectif | Resultat observe | Analyse |
| --- | --- | --- | --- |
| Restaurer OpenLDAP en priorite | Oui | Oui, simule | Priorite respectee. |
| RTO OpenLDAP | 2 h PRA, 4 h PCA | 1 h 55, simule | Conforme, marge faible. |
| RPO OpenLDAP | Sauvegarde quotidienne, perte maximale proche de 24 h | 18 h, simule | Acceptabilite a confirmer avec le metier. |
| Reprendre les services dependants selon priorite | Oui | Oui, simule | LAM, Samba puis messagerie. |
| Verifier chaque service avant de poursuivre | Oui | Oui, simule | Preuves attendues dans chaque etape. |
| Restaurer toute l'infrastructure en 7 h | Non obligatoire | Non, simule | WordPress reste a traiter. |

## Bilan final

| Question | Reponse |
| --- | --- |
| Services restaures | OpenLDAP, LAM, Samba ; messagerie et supervision partielles. |
| Services non restaures | WordPress/MariaDB. |
| Cause principale des indisponibilites restantes | Temps consomme par les dependances critiques et les validations applicatives. |
| RTO le plus critique observe | Messagerie partielle : 5 h 15, simule. |
| RPO le plus critique observe | 18 h, simule, sur LDAP et les donnees dependantes. |
| Objectifs respectes | OpenLDAP, Samba, messagerie et supervision dans les delais cibles. |
| Ameliorations proposees | Selection d'archive saine, checklist Samba/messagerie et canal de crise hors messagerie. |

## Actions d'amelioration

| Action | Effet attendu | Priorite |
| --- | --- | --- |
| Mesurer regulierement une restauration OpenLDAP complete. | RTO plus fiable. | P1 |
| Augmenter la frequence des sauvegardes LDAP si le RPO observe est trop eleve. | RPO reduit. | P1 |
| Preparer un environnement de restauration isole reproductible. | Moins de temps perdu pendant la crise. | P1 |
| Documenter les tests Samba et messagerie sous forme de checklist. | Validation plus rapide. | P2 |
| Automatiser l'export des preuves de supervision. | Cloture d'incident plus solide. | P2 |
