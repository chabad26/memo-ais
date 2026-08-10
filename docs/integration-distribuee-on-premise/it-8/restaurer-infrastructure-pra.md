# Restaurer l'infrastructure avec le PRA

## Objectif

Restaurer le maximum de services possibles en appliquant les procedures
definies dans le PRA et le plan d'actions etabli pendant la gestion de crise.

L'exercice dure **7 heures**. Il n'est pas attendu que toute l'infrastructure
soit necessairement restauree avant la fin du temps imparti. Un service est
considere comme restaure uniquement lorsque son fonctionnement a ete verifie.

## Documents de travail

| Document | Role dans l'exercice |
| --- | --- |
| `/home/oliv/on-premise/documentation/incident-majeur-ldap.md` | Plan de crise et ordre d'action valide. |
| `/home/oliv/on-premise/documentation/PRA.md` | Procedures de reprise par service. |
| `/home/oliv/on-premise/documentation/PCA.md` | Objectifs de continuite et priorites. |
| `/home/oliv/on-premise/documentation/restore-procedure.md` | Restauration depuis BorgBackup. |
| `/home/oliv/on-premise/documentation/backup-strategy-validation.md` | Estimation initiale RTO/RPO pour LDAP. |
| `/home/oliv/on-premise/documentation/rapport-restauration-pra.md` | Rapport de restauration a completer. |

## Notions a mesurer

| Notion | Definition pratique dans l'exercice |
| --- | --- |
| RTO | Temps observe entre le debut de la restauration et le retour verifie du service. |
| RPO | Perte de donnees estimee entre la derniere sauvegarde saine et l'incident. |

La ressource TechTarget rappelle que le RTO mesure le temps d'indisponibilite
acceptable, tandis que le RPO mesure la quantite ou l'anciennete maximale des
donnees perdues apres incident.

## Contraintes

- Travail en binome.
- Temps total disponible : **7 heures**.
- Restaurer d'abord un nouveau serveur LDAP sain.
- Ne pas reutiliser directement le serveur compromis.
- Restaurer les configurations et donnees necessaires depuis les sauvegardes.
- Verifier chaque service avant de passer au suivant.
- Documenter les services non restaures et la raison de l'arret.

## Priorites de reprise

| Ordre | Service | Justification |
| --- | --- | --- |
| 1 | OpenLDAP | Service source pour les identites et les groupes. |
| 2 | LDAP Account Manager | Administration des comptes apres validation LDAP. |
| 3 | Samba | Acces aux partages metiers dependant des groupes LDAP. |
| 4 | Messagerie | Authentification Dovecot/Postfix/Roundcube via LDAP. |
| 5 | Supervision | Controle des journaux et preuve de reprise. |
| 6 | WordPress/MariaDB | Service moins directement touche par la compromission LDAP actuelle. |

## Chronometrage

Hypothese de depart : exercice demarre le **10 aout 2026 a 14:10 CEST**.
Fin des 7 heures : **10 aout 2026 a 21:10 CEST**.

| Phase | Heure debut | Heure fin | Duree | Commentaire |
| --- | --- | --- | --- | --- |
| Preparation et selection de l'archive | 14:10 | 14:35 | 25 min | BorgBackup, archive saine et rappel du plan de crise. |
| Reconstruction OpenLDAP | 14:35 | 15:50 | 1 h 15 | Nouveau serveur ou nouveaux volumes. |
| Validation LDAP | 15:50 | 16:05 | 15 min | `ldapwhoami`, `ldapsearch`, objets attendus. |
| Reprise LAM | 16:05 | 16:35 | 30 min | Acces Web et connexion LDAP. |
| Reprise Samba | 16:35 | 17:50 | 1 h 15 | Partages et droits. |
| Reprise messagerie | 17:50 | 19:25 | 1 h 35 | Connexion, envoi et reception. |
| Reprise supervision | 19:25 | 20:00 | 35 min | Journaux et tableaux de bord. |
| Controle des services dependants | 20:00 | 20:55 | 55 min | Redemarrage surveille et verification applicative. |
| WordPress/MariaDB et cloture | 20:55 | 21:10 | 15 min | WordPress non restaure ; synthese RTO/RPO. |
| Cloture et rapport | 20:55 | 21:10 | 15 min | RTO/RPO et comparaison PCA/PRA. |

## Plan d'execution

### 1. Demarrage de l'exercice

1. Noter l'heure de debut.
2. Relire le plan d'actions valide dans `incident-majeur-ldap.md`.
3. Confirmer que le serveur compromis reste isole et non modifie.
4. Charger les variables de sauvegarde depuis l'emplacement protege.
5. Verifier le depot BorgBackup et lister les archives.

```bash
cd /home/oliv/on-premise/backup
set -a
source .env
set +a

borg check "$BORG_REPO"
borg list "$BORG_REPO"
```

### 2. Reconstruction du service LDAP

1. Selectionner une archive saine anterieure a l'incident.
2. Restaurer les donnees LDAP dans un volume isole.
3. Restaurer les configurations necessaires sans ecraser les donnees
   compromises.
4. Reconstruire un OpenLDAP propre depuis les fichiers Compose versionnes.
5. Demarrer le service restaure.
6. Verifier les journaux et l'etat du conteneur.

```bash
cd /home/oliv/on-premise/infrastructure-compose
docker compose config
docker compose up -d
docker compose ps
docker compose logs --tail=100 openldap
```

### 3. Verification LDAP

```bash
ldapwhoami -x \
  -H ldap://localhost:389 \
  -D "cn=admin,dc=embedded,dc=local" \
  -W

ldapsearch -x \
  -H ldap://localhost:389 \
  -D "cn=admin,dc=embedded,dc=local" \
  -W \
  -b "dc=embedded,dc=local" \
  "(objectClass=*)"
```

Points a verifier :

- bind administrateur fonctionnel ;
- base `dc=embedded,dc=local` presente ;
- OU `People`, `Groups`, `Services` et `Computers` presentes ;
- utilisateurs et groupes attendus presents ;
- aucune erreur bloquante dans les journaux OpenLDAP.

### 4. Reprise progressive des services dependants

| Service | Actions principales | Verification |
| --- | --- | --- |
| LAM | Redemarrer l'interface apres LDAP. | Connexion a `ldap://openldap:3890`. |
| Samba | Restaurer volumes/configuration puis demarrer. | Acces aux partages et controle des droits. |
| Messagerie | Restaurer Maildir, base Roundcube puis demarrer. | Connexion IMAP/Webmail et message de test. |
| Supervision | Relancer Elasticsearch, Kibana et Filebeat. | Journaux visibles et tableaux de bord exploitables. |
| WordPress | Relancer si le temps restant le permet. | Acces Web et donnees presentes. |

!!! note "Cas ou les certificats auraient ete touches"
    La gestion des certificats n'a pas ete traitee pendant ce poste. Si elle
    avait ete incluse, il aurait fallu ajouter une etape apres la reprise des
    services : identifier les certificats ou cles compromis, revoquer les
    certificats concernes, generer de nouvelles paires cle/certificat,
    redeployer les fichiers TLS et verifier cote client que le nouveau
    certificat est presente. Dans ce memo, les controles attendus portent donc
    sur le retour du service LDAP, la presence des utilisateurs et groupes, puis
    le redemarrage surveille des services dependants.

## Tableau de resultat attendu

| Service | Restaure | Verification | RTO observe | RPO estime | Commentaire |
| --- | --- | --- | --- | --- | --- |
| OpenLDAP | A completer | A completer | A completer | A completer | Service prioritaire. |
| LDAP Account Manager | A completer | A completer | A completer | A completer | Service d'administration. |
| Samba | A completer | A completer | A completer | A completer | Partages metiers. |
| Messagerie | A completer | A completer | A completer | A completer | Postfix, Dovecot, Roundcube. |
| Supervision | A completer | A completer | A completer | A completer | Kibana et journaux. |
| WordPress/MariaDB | A completer | A completer | A completer | A completer | Service non prioritaire dans ce scenario. |

## Rapport de restauration

Dans `/home/oliv/on-premise/documentation/rapport-restauration-pra.md`,
documenter :

- les etapes de restauration realisees ;
- les services effectivement remis en production ;
- les verifications effectuees ;
- les services restant indisponibles et leur justification ;
- l'estimation des pertes de donnees, donc le RPO observe ;
- le temps de reprise observe, donc le RTO reel ;
- la comparaison entre les objectifs prevus et les resultats obtenus.

## Questions de synthese

1. Quel service a ete restaure en premier et pourquoi ?
2. Quelle verification prouve que LDAP est de nouveau utilisable ?
3. Quels services n'ont pas ete restaures dans les 7 heures ?
4. Le RTO observe respecte-t-il l'objectif du PRA ?
5. Le RPO observe est-il acceptable pour l'entreprise ?
6. Quelles actions permettraient de reduire le RTO ou le RPO lors d'un futur
   exercice ?

## Ressource

- [RPO vs. RTO: Key differences explained with examples](https://www.techtarget.com/searchstorage/feature/What-is-the-difference-between-RPO-and-RTO-from-a-backup-perspective)
