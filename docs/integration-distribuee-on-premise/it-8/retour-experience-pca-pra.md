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
| `/home/oliv/on-premise/documentation/gestion-certificats-roundcube.md` | Traitement du certificat Roundcube compromis. |
| `/home/oliv/on-premise/documentation/PCA.md` | Plan de continuite a mettre a jour. |
| `/home/oliv/on-premise/documentation/PRA.md` | Plan de reprise a mettre a jour. |
| `/home/oliv/on-premise/documentation/retour-experience-pca-pra.md` | Livrable REX de l'exercice. |

## Resultats simules de l'exercice

| Service | Etat simule | Verification simulee | RTO simule | RPO simule |
| --- | --- | --- | --- | --- |
| OpenLDAP | Restaure | `ldapwhoami` et `ldapsearch` reussis | 1 h 55 | 18 h |
| LAM | Restaure | Connexion Web et bind LDAP valides | 2 h 25 | 18 h |
| Samba | Restaure | Acces au partage `Commun` et refus hors groupe | 3 h 40 | 18 h |
| Messagerie | Partiel | IMAPS et SMTP OK, Roundcube bloque par certificat | 5 h 15 | 18 h |
| Roundcube TLS | Restaure apres remplacement | Nouveau numero de serie observe cote client | 6 h 10 | Sans perte de donnees |
| Supervision | Partiel | Kibana accessible, alertes externes non validees | 6 h 45 | Index non critiques |
| WordPress/MariaDB | Non restaure | Temps insuffisant, service non prioritaire | Non mesure | Non mesure |

## Points ayant bien fonctionne

- Le plan de crise a permis d'isoler le serveur compromis sans modifier ses
  donnees.
- La priorite OpenLDAP avant Samba et messagerie a evite des tests inutiles.
- Les fichiers Compose versionnes ont accelere la reconstruction.
- Les commandes `ldapwhoami` et `ldapsearch` ont donne une preuve claire du
  retour de l'annuaire.
- Le client TLS dedie a permis de verifier rapidement les certificats de
  service.

## Difficultes rencontrees

| Difficulté | Impact | Correction proposee |
| --- | --- | --- |
| Archive saine selectionnee trop tardivement | Perte de temps au debut de l'exercice | Ajouter une commande standard de selection d'archive dans le PRA. |
| Procedure CRL insuffisamment detaillee | Validation de revocation incomplete | Documenter l'URL CRL, la commande de controle et les limites Step CA. |
| Dependances TLS decouvertes pendant la reprise | Retard sur Roundcube | Ajouter une verification certificat avant remise en service messagerie. |
| Tests Samba disperses | Validation plus lente | Ajouter une checklist unique par partage et par groupe. |
| Alertes externes non validees | Supervision partielle | Prevoir un canal de notification hors messagerie. |

## Procedures incompletes

| Procedure | Manque identifie | Mise a jour attendue |
| --- | --- | --- |
| Restauration LDAP | Validation TLS non systematique | Ajouter LDAPS et controle certificat apres `ldapsearch`. |
| Restauration messagerie | Ordre entre certificats, Dovecot, Postfix et Roundcube trop implicite | Rendre l'ordre de reprise explicite. |
| Revocation certificat | Publication CRL non prouvee | Ajouter controle `step crl inspect` et emplacement de publication. |
| Validation Samba | Tests d'acces insuffisamment formalises | Ajouter tests autorise/refuse par groupe. |
| Supervision | Alertes externes non integrees au PRA | Ajouter une procedure de notification manuelle ou alternative. |

## Nouveaux besoins identifies

- Disposer d'un environnement de restauration LDAP isole et preconfigure.
- Conserver une checklist de validation par service.
- Mesurer automatiquement les heures de debut et de fin de reprise.
- Publier une CRL accessible aux clients ou documenter clairement la limite.
- Augmenter la frequence de sauvegarde LDAP si un RPO de 18 h est juge trop
  eleve.
- Prevoir un canal de communication de crise qui ne depend pas de la messagerie
  interne.

## Modifications proposees

| Element | Modification proposee | Justification |
| --- | --- | --- |
| Procedure de restauration LDAP | Ajouter verification LDAPS et certificat apres restauration. | Plusieurs services consomment LDAP en TLS. |
| Procedure de restauration messagerie | Ajouter un jalon TLS avant Roundcube. | La cle Roundcube compromise a retarde la reprise. |
| Gestion des certificats | Ajouter revocation, CRL, nouvelle cle et preuve client. | Une cle compromise ne doit jamais etre renouvelee. |
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
