# PCA exercice - crise OpenLDAP


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/PCA-exercice-crise-ldap.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.


## Perimetre

Ce document est une variante de travail pour l'exercice du 10 aout 2026. Il ne
remplace pas le `PCA.md` general du projet.

Le scenario realise porte sur la compromission d'OpenLDAP, son isolement, puis
la reprise des services dependants apres restauration depuis une sauvegarde
saine.

La partie certificats Roundcube est seulement un cas conditionnel : si une cle
ou un certificat avait ete annonce compromis, une procedure de revocation,
regeneration et verification client aurait ete ajoutee.

## Objectifs de continuite de l'exercice

| Domaine | Objectif pendant la crise | Justification |
| --- | --- | --- |
| Authentification | Retablir un OpenLDAP fiable avant les services dependants. | Samba, LAM et la messagerie dependent des comptes et groupes LDAP. |
| Communication | Utiliser un canal hors messagerie interne. | La messagerie peut etre indisponible pendant l'incident LDAP. |
| Sauvegardes LDAP | Identifier une archive saine anterieure a la compromission. | Une sauvegarde recente peut deja contenir des donnees corrompues. |
| Services dependants | Redemarrer progressivement apres validation LDAP. | Eviter de tester des services contre un annuaire non fiable. |
| Supervision | Utiliser Kibana comme aide au diagnostic. | La supervision aide a prouver la reprise, mais ne bloque pas le retour LDAP. |
| Certificats | Garder la procedure comme hypothese seulement. | Le poste realise ne contient pas de compromission de certificat. |

## Mode degrade

| Situation | Mesure de continuite |
| --- | --- |
| OpenLDAP compromis | Isoler le serveur et geler les modifications de comptes/groupes. |
| LAM indisponible | Utiliser les commandes LDAP directes apres restauration. |
| Messagerie indisponible | Communiquer hors messagerie interne. |
| Samba perturbe | Suspendre les modifications de droits et informer les utilisateurs. |
| Supervision partielle | Conserver les journaux disponibles et documenter les limites. |

## Points de verification

| Service | Verification minimale |
| --- | --- |
| OpenLDAP | `ldapwhoami`, `ldapsearch`, OU, groupes et utilisateurs presents. |
| LAM | Acces Web et bind vers l'annuaire restaure. |
| Samba | Acces autorise et refus hors groupe. |
| Messagerie | Connexion et message de test apres retour LDAP. |
| Supervision | Journaux de reprise visibles si la plateforme est disponible. |
| Certificats conditionnels | Revocation, nouvelle cle, redeploiement TLS et verification client uniquement si le scenario est declenche. |

## RPO accepte pour l'exercice

Le RPO simule est de 18 h pour LDAP, selon l'ecart entre la derniere sauvegarde
saine et l'heure estimee de l'incident. Ce chiffre doit etre valide par le
responsable metier si l'exercice est rejoue en conditions reelles.

## Ameliorations proposees

| Priorite | Action | Preuve attendue |
| --- | --- | --- |
| P1 | Formaliser la selection de l'archive saine. | Commandes Borg et horodatage conserves. |
| P1 | Preparer un environnement de restauration LDAP isole. | Service restaure sans toucher au serveur compromis. |
| P2 | Ajouter une checklist par service dependant. | Tests LAM, Samba et messagerie reproductibles. |
| P2 | Prevoir un canal de communication hors messagerie. | Contact et procedure disponibles. |
| P2 | Garder une fiche certificats conditionnelle. | Procedure disponible sans l'annoncer comme realisee. |
