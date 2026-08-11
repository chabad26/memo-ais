# Retour d'experience et mise a jour PCA/PRA

## Objectif

Realiser un retour d'experience apres l'exercice de gestion de crise et de
restauration, puis mettre a jour le PCA/PRA avec les enseignements tires.

Cette feuille utilise des **resultats simules** afin de fournir un modele
propre. Les valeurs doivent etre remplacees par les mesures reelles lorsque
l'exercice est rejoue sur une autre configuration.

## Documents de travail

| Document | Role |
| --- | --- |
| `/home/oliv/on-premise/documentation/incident-majeur-ldap.md` | Decisions de crise. |
| `/home/oliv/on-premise/documentation/rapport-restauration-pra.md` | Chronologie, services restaures, RTO/RPO. |
| `/home/oliv/on-premise/documentation/PCA-exercice-crise-ldap.md` | PCA propre a l'exercice, sans modifier le PCA general. |
| `/home/oliv/on-premise/documentation/PRA-exercice-crise-ldap.md` | PRA propre a l'exercice, sans modifier le PRA general. |
| `/home/oliv/on-premise/documentation/retour-experience-pca-pra.md` | Livrable REX de l'exercice. |

## Resultats simules de l'exercice

| Service | Etat simule | Verification simulee | RTO simule | RPO simule |
| --- | --- | --- | --- | --- |
| OpenLDAP | Restaure | `ldapwhoami` et `ldapsearch` reussis | 1 h 55 | 18 h |
| LAM | Restaure | Connexion Web et bind LDAP valides | 2 h 25 | 18 h |
| Samba | Restaure | Acces au partage `Commun` et refus hors groupe | 3 h 40 | 18 h |
| Messagerie | Partiel | Authentification a revalider apres retour LDAP | 5 h 15 | 18 h |
| Supervision | Partiel | Kibana accessible, alertes externes non validees | 5 h 50 | Index non critiques |
| WordPress/MariaDB | Non restaure | Temps insuffisant, service non prioritaire | Non mesure | Non mesure |

!!! note "Limite du memo"
    La partie certificats n'a pas ete traitee dans cet exercice. Le retour
    d'experience reste donc centre sur la crise LDAP, la restauration depuis
    sauvegarde et l'ordre de reprise des services dependants. Si les
    certificats avaient fait partie de la crise, le REX aurait aussi mesure le
    temps de revocation, de remplacement des cles, de redeploiement TLS et de
    verification client.

## Points ayant bien fonctionne

- Le plan de crise a permis d'isoler le serveur compromis sans modifier ses
  donnees.
- La priorite OpenLDAP avant Samba et messagerie a evite des tests inutiles.
- Les fichiers Compose versionnes ont accelere la reconstruction.
- Les commandes `ldapwhoami` et `ldapsearch` ont donne une preuve claire du
  retour de l'annuaire.
- Le redemarrage sous surveillance des services dependants a limite les risques
  de reprise dans le mauvais ordre.

## Difficultes rencontrees

| Difficulté | Impact | Correction proposee |
| --- | --- | --- |
| Archive saine selectionnee trop tardivement | Perte de temps au debut de l'exercice | Ajouter une commande standard de selection d'archive dans le PRA. |
| Perimetre de reprise a clarifier | Risque de melanger crise LDAP et sujets certificats | Noter explicitement que les certificats sont seulement un cas conditionnel. |
| Validation applicative incomplete | Certains services dependants doivent etre retestes apres LDAP | Ajouter une checklist par service dependant. |
| Tests Samba disperses | Validation plus lente | Ajouter une checklist unique par partage et par groupe. |
| Alertes externes non validees | Supervision partielle | Prevoir un canal de notification hors messagerie. |

## Procedures incompletes

| Procedure | Manque identifie | Mise a jour attendue |
| --- | --- | --- |
| Restauration LDAP | Selection de l'archive saine a formaliser | Ajouter les commandes Borg et les criteres de choix. |
| Restauration messagerie | Tests apres retour LDAP trop implicites | Rendre l'ordre de reprise explicite. |
| Perimetre certificats | Non traite dans ce poste | L'annoncer comme cas conditionnel : revocation, nouvelle cle, redeploiement et verification client. |
| Validation Samba | Tests d'acces insuffisamment formalises | Ajouter tests autorise/refuse par groupe. |
| Supervision | Alertes externes non integrees au PRA | Ajouter une procedure de notification manuelle ou alternative. |

## Nouveaux besoins identifies

- Disposer d'un environnement de restauration LDAP isole et preconfigure.
- Conserver une checklist de validation par service.
- Mesurer automatiquement les heures de debut et de fin de reprise.
- Augmenter la frequence de sauvegarde LDAP si un RPO de 18 h est juge trop
  eleve.
- Prevoir un canal de communication de crise qui ne depend pas de la messagerie
  interne.

## Modifications proposees

| Element | Modification proposee | Justification |
| --- | --- | --- |
| Procedure de restauration LDAP | Ajouter extraction Borg, controle des LDIF et import dans un LDAP sain. | Ce sont les actions reellement realisees pendant le poste. |
| Procedure de restauration messagerie | Ajouter les tests d'authentification apres retour LDAP. | La messagerie depend de l'annuaire pour les comptes. |
| Perimetre de l'iteration | Garder les certificats comme annonce conditionnelle, sans feuille technique dediee. | Le poste ne contenait pas cette partie, mais le jury peut voir la reaction attendue si elle avait existe. |
| Strategie de sauvegarde LDAP | Revoir la frequence si RPO cible inferieur a 24 h. | RPO simule de 18 h, acceptable seulement si valide metier. |
| Plan d'alertes | Ajouter un canal hors messagerie. | La messagerie peut etre indisponible pendant la crise. |
| Rapport PRA | Ajouter tableau RTO/RPO par service. | Comparaison plus rapide avec les objectifs PCA/PRA. |

## Livrable attendu

Dans `/home/oliv/on-premise/documentation/retour-experience-pca-pra.md`,
conserver :

- le compte rendu du retour d'experience ;
- les resultats simules ou reels de l'exercice ;
- les points positifs ;
- les difficultes ;
- les procedures incompletes ;
- les nouveaux besoins ;
- la liste des ameliorations apportees ;
- les sections de PCA/PRA mises a jour.

## Questions de synthese

1. Quel ecart principal existe entre le PRA theorique et l'exercice simule ?
2. Le RTO LDAP respecte-t-il les objectifs ?
3. Le RPO simule est-il acceptable pour les comptes et groupes LDAP ?
4. Quelle procedure doit etre amelioree en priorite ?
5. Quelle modification reduirait le plus le temps de reprise ?
