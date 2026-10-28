# Retour d'experience PCA/PRA - exercice simule


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/retour-experience-pca-pra.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.


## Avertissement

Ce retour d'experience contient des **resultats simules**. Il sert de modele
propre pour l'exercice. Les valeurs doivent etre remplacees par les mesures
reelles lorsque la restauration est executee sur la configuration cible.

## Contexte

L'exercice simule fait suite a une compromission OpenLDAP. Le binome a applique
le plan de crise et le PRA afin de restaurer l'annuaire depuis une sauvegarde
saine, puis de reprendre les services dependants dans un ordre controle.

La compromission d'un certificat Roundcube est conservee comme **cas
conditionnel** : si elle avait ete annoncee pendant la crise, il aurait fallu
revoquer le certificat, regenerer une nouvelle cle, redeployer TLS et verifier
le resultat depuis un client.

| Element | Valeur simulee |
| --- | --- |
| Date | 10 aout 2026 |
| Duree disponible | 7 h |
| Debut | 14:10 CEST |
| Fin | 21:10 CEST |
| Scenario | Compromission OpenLDAP ; certificats uniquement en cas conditionnel |
| Objectif | Restaurer le maximum de services et mettre a jour PCA/PRA |

## Resultats simules

| Service | Restaure | Verification | RTO simule | RPO simule | Commentaire |
| --- | --- | --- | --- | --- | --- |
| OpenLDAP | Oui | `ldapwhoami` et `ldapsearch` reussis | 1 h 55 | 18 h | Objectif PRA respecte. |
| LDAP Account Manager | Oui | Connexion Web et bind LDAP valides | 2 h 25 | 18 h | Service secondaire retabli apres LDAP. |
| Samba | Oui | Acces partage `Commun` et refus hors groupe | 3 h 40 | 18 h | Validation dependante des groupes LDAP. |
| Messagerie | Partiel | Authentification a revalider apres retour LDAP | 5 h 15 | 18 h | Tests applicatifs a completer. |
| Supervision | Partiel | Kibana accessible, alertes externes non validees | 5 h 50 | Non critique | Utile pour preuve, pas bloquant. |
| WordPress/MariaDB | Non | Non teste | Non mesure | Non mesure | Temps insuffisant et priorite basse. |

## Points ayant bien fonctionne

- Le serveur compromis a ete isole sans tentative de correction locale.
- Le plan d'actions a donne un ordre clair : OpenLDAP, LAM, Samba, messagerie,
  supervision.
- Les Compose et les `.env.example` ont permis de reconstruire les services.
- Les tests LDAP ont donne une validation rapide et lisible.
- La separation entre service source LDAP et interface LAM a evite de bloquer
  la reprise sur l'outil d'administration.
- Le cas certificats a ete identifie comme procedure conditionnelle, sans etre
  presente comme manipulation realisee.

## Difficultes rencontrees

| Difficulté | Impact | Decision prise |
| --- | --- | --- |
| Choix de l'archive saine trop manuel | 20 min perdues | Ajouter une procedure de selection d'archive. |
| Perimetre certificats a clarifier | Risque de melanger crise LDAP et PKI | Le conserver comme cas conditionnel distinct. |
| Validation applicative incomplete | Certains services dependants doivent etre retestes apres LDAP | Ajouter une checklist par service. |
| Tests Samba pas assez formalises | Validation plus lente | Creer une checklist par partage et groupe. |
| Alertes externes non testees | Supervision partielle | Ajouter canal hors messagerie. |

## Procedures incompletes

| Procedure | Manque | Correction |
| --- | --- | --- |
| PRA OpenLDAP | Selection de l'archive saine trop manuelle | Ajouter les criteres et commandes Borg. |
| PRA messagerie | Tests apres retour LDAP trop implicites | Ajouter une checklist de reprise messagerie. |
| Cas certificats | Non realise dans ce poste | Garder la procedure comme hypothese : revocation, nouvelle cle, redeploiement et controle client. |
| Validation Samba | Pas de matrice simple utilisateur/groupe/partage | Ajouter tests autorises et refus attendus. |
| PCA communication | Messagerie interne non disponible pendant incident | Ajouter telephone, canal externe ou messagerie de secours. |

## Nouveaux besoins identifies

- Automatiser la selection de la derniere archive saine.
- Preparer un compose de restauration LDAP isole.
- Documenter le cas conditionnel certificats sans le confondre avec l'exercice
  realise.
- Maintenir une checklist de validation par service.
- Ajouter un canal de communication de crise hors messagerie interne.
- Revoir le RPO LDAP avec le responsable metier si 18 h de perte potentielle
  sont trop importantes.

## Ameliorations apportees au PCA/PRA

| Element | Modification apportee | Justification |
| --- | --- | --- |
| PCA - Authentification | Ajout d'un mode degrade et d'un rappel sur les services dependants. | OpenLDAP conditionne Samba et la messagerie. |
| PCA - Certificats | Rappel du traitement a appliquer seulement si une cle est compromise. | Le poste LDAP ne contenait pas cette partie, mais le cas doit etre connu. |
| PCA - Communication | Ajout d'un canal hors messagerie. | La messagerie peut dependre de LDAP. |
| PRA - OpenLDAP | Ajout de criteres de choix d'archive et de validation LDAP apres restauration. | L'annuaire est le service source. |
| PRA - Messagerie | Ajout des tests d'authentification apres retour LDAP. | La messagerie depend de l'annuaire. |
| PRA - RTO/RPO | Ajout d'un tableau de mesure par service. | Comparer les objectifs aux resultats observes. |

## PCA d'exercice cree

Le document `documentation/PCA-exercice-crise-ldap.md` conserve les ajustements
propres a cette crise, sans modifier le PCA general du projet. Il precise :

- le role critique d'OpenLDAP pour Samba et la messagerie ;
- la necessite d'un canal de communication hors messagerie ;
- le rappel du cas conditionnel des certificats compromis ;
- le besoin de revoir le RPO LDAP si la perte maximale acceptable est
  inferieure a la frequence actuelle des sauvegardes.

## PRA d'exercice cree

Le document `documentation/PRA-exercice-crise-ldap.md` conserve les procedures
propres a cette crise, sans modifier le PRA general du projet. Il precise :

- la selection d'une archive saine avant restauration ;
- la restauration OpenLDAP dans un environnement isole ;
- la validation `ldapwhoami` et `ldapsearch` ;
- l'ordre de reprise LAM, Samba, messagerie et supervision ;
- la mesure RTO/RPO par service.

## Comparaison aux objectifs

| Critere | Objectif | Resultat simule | Analyse |
| --- | --- | --- | --- |
| RTO OpenLDAP | 2 h PRA | 1 h 55 | Conforme mais marge faible. |
| Interruption authentification | 4 h PCA | 1 h 55 | Conforme. |
| RPO LDAP | Sauvegarde quotidienne | 18 h | Compatible si accepte metier. |
| Reprise Samba | Apres LDAP | 3 h 40 | Conforme a la priorisation. |
| Messagerie | 24 h | Partielle en 5 h 15 | Objectif compatible, tests applicatifs a completer. |
| Supervision | 48 h | Partielle en 5 h 50 | Compatible, alertes externes a completer. |

## Plan d'amelioration

| Priorite | Action | Responsable | Validation attendue |
| --- | --- | --- | --- |
| P1 | Ajouter une checklist de restauration OpenLDAP isolee. | Administrateur systeme | Service restaure et teste hors production. |
| P1 | Formaliser le cas conditionnel certificats. | Responsable PKI | Procedure revocation, nouvelle cle et controle client disponible. |
| P2 | Formaliser les tests Samba par groupe. | Administrateur systeme | Acces autorises/refuses documentes. |
| P2 | Ajouter canal de communication de crise hors messagerie. | Coordinateur | Contact et procedure disponibles. |
| P2 | Revoir la frequence de sauvegarde LDAP. | Responsable sauvegarde | RPO cible valide par le metier. |

## Conclusion

L'exercice simule montre que le PRA permet de retablir l'authentification dans
les objectifs, mais que les validations applicatives doivent etre mieux
formalisees. Le cas certificats reste annonce comme extension possible de la
crise, sans etre compte comme une action realisee pendant ce poste.
