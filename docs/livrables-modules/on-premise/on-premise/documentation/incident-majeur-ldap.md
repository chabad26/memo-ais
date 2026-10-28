# Gestion de crise - incident majeur OpenLDAP


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/incident-majeur-ldap.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Contexte de l'exercice

Le formateur annonce une attaque ayant compromis le serveur OpenLDAP. La base
LDAP est corrompue et la configuration du serveur ne peut plus etre consideree
comme fiable.

Regle principale : le serveur compromis doit etre arrete ou isole sans modifier
ses donnees afin de permettre une analyse forensique ulterieure. La reprise
doit s'appuyer sur le PCA, le PRA et les sauvegardes disponibles.

## Documents de reference

| Document | Utilisation |
| --- | --- |
| `memo-ais/docs/integration-distribuee-on-premise/it-8/gestion-crise-ldap.md` | Feuille pedagogique de l'iteration 8. |
| `documentation/PCA-exercice-crise-ldap.md` | Mesures de continuite propres a l'exercice. |
| `documentation/PRA-exercice-crise-ldap.md` | Ordre de reprise propre a la crise OpenLDAP. |
| `documentation/inventory.md` | Inventaire des services, ports, volumes et dependances. |
| `documentation/backup-strategy-validation.md` | Scenario de corruption LDAP, RTO estime et RPO actuel. |
| `documentation/restore-procedure.md` | Commandes BorgBackup et restauration en volume isole. |
| `documentation/monitoring-dashboards.md` | Controle des erreurs LDAP et de l'etat d'exploitation dans Kibana. |

## Compte rendu de reunion de crise

| Element | Valeur |
| --- | --- |
| Date de l'exercice | 10 aout 2026 |
| Objet | Compromission du serveur OpenLDAP |
| Participants | Binome d'administration infrastructure |
| Decision initiale | Declenchement du PRA pour le service d'authentification |
| Priorite metier | Retablir une authentification fiable avant les services dependants |
| Contrainte forensique | Ne pas modifier le serveur compromis |
| Validation requise | Presenter ce plan au formateur avant intervention |

### Synthese de situation

OpenLDAP est le service de reference pour les identites et les groupes du
laboratoire. Sa compromission rend l'authentification centralisee indisponible
ou non fiable. Les services dependants ne doivent pas etre remis en production
tant qu'une source LDAP saine n'a pas ete restauree et verifiee.

### Hypotheses retenues

- Les fichiers Compose et `.env.example` sont disponibles dans Git.
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
- Les sauvegardes BorgBackup contiennent les volumes `ldap_data`,
  `ldap_config` et les exports LDAP necessaires.
- Une archive anterieure a la compromission peut etre identifiee.
- La supervision peut aider au diagnostic, mais ne bloque pas la restauration
  de l'authentification.

## Evaluation des consequences

| Service | Dependances LDAP | Consequences | Priorite de controle |
| --- | --- | --- | --- |
| OpenLDAP | Service source | Donnees et configuration non fiables. | P1 |
| LDAP Account Manager | OpenLDAP | Administration Web impossible ou dangereuse. | P3 |
| Samba | Groupes et comptes LDAP | Acces aux partages perturbes ou refus d'authentification. | P2 |
| Dovecot/Postfix/Roundcube | Comptes LDAP | Connexion mail et webmail perturbee. | P2 |
| Sauvegardes BorgBackup | Aucune dependance directe a LDAP | Source principale de restauration. | P1 |
| TLS/PKI | Certificats de service | Cas conditionnel : si un certificat ou une cle est touche, il faut revoquer, regenerer et revalider cote client. | P2 |
| Supervision Kibana/Filebeat | Journaux Docker | Diagnostic et preuves d'exploitation. | P3 |
| WordPress/MariaDB | Pas de dependance directe actuelle | Impact indirect uniquement. | P4 |

## Decisions prises

| Decision | Motif | Responsable |
| --- | --- | --- |
| Declencher le PRA OpenLDAP. | L'authentification est prioritaire et non fiable. | Coordinateur |
| Isoler ou arreter le serveur compromis sans nettoyage. | Preserver les preuves et eviter l'aggravation. | Administrateur systeme |
| Suspendre les modifications LDAP. | Eviter d'ajouter des donnees dans une base corrompue. | Coordinateur |
| Restaurer d'abord en environnement isole. | Controler l'integrite avant toute bascule. | Administrateur systeme |
| Restaurer OpenLDAP avant LAM, Samba et messagerie. | Les services dependants ont besoin d'une source d'identite saine. | Binome |
| Utiliser une archive anterieure a la compromission. | Eviter de restaurer des donnees deja corrompues. | Responsable sauvegarde |
| Presenter le plan au formateur avant execution. | Respecter la consigne de l'exercice. | Coordinateur |

## Repartition des roles

| Role | Responsable | Taches |
| --- | --- | --- |
| Coordinateur de crise | Membre 1 | Tenir le compte rendu, faire valider le plan, communiquer. |
| Administrateur systeme | Membre 2 | Isoler le service compromis, preparer l'environnement de reprise. |
| Responsable sauvegarde | Membre 1 | Identifier l'archive saine, executer les controles BorgBackup. |
| Responsable validation | Membre 2 | Tester LDAP, Samba, messagerie et supervision ; verifier TLS seulement si le scenario certificats est declenche. |
| Communication | Binome | Informer les utilisateurs et noter l'etat de remise en service. |

## Plan d'actions valide avant intervention

| Action | Priorite | Responsable | Validation attendue |
| --- | --- | --- | --- |
| Ouvrir le journal d'incident et noter l'heure de declaration. | Immediate | Coordinateur | Compte rendu initialise. |
| Isoler ou arreter OpenLDAP compromis sans modifier ses donnees. | Immediate | Administrateur systeme | Action consignee, aucune correction locale. |
| Geler les changements de comptes, groupes et droits. | Immediate | Coordinateur | Decision communiquee au binome. |
| Inventorier les services impactes. | P1 | Binome | Tableau d'impact complete. |
| Verifier les sauvegardes BorgBackup. | P1 | Responsable sauvegarde | `borg check` sans erreur bloquante. |
| Identifier une archive saine anterieure a la compromission. | P1 | Responsable sauvegarde | Nom et horodatage de l'archive notes. |
| Restaurer les volumes LDAP dans un emplacement isole. | P1 | Administrateur systeme | Volume de test distinct de la production. |
| Demarrer un OpenLDAP de test. | P1 | Administrateur systeme | Conteneur actif et journaux controles. |
| Tester l'authentification administrateur et la recherche LDAP. | P1 | Responsable validation | `ldapwhoami` et `ldapsearch` reussis. |
| Verifier OU, groupes et utilisateurs. | P1 | Responsable validation | Objets attendus presents. |
| Basculer vers l'annuaire restaure apres accord. | P1 | Binome | Heure de bascule et decision notees. |
| Redemarrer LAM puis verifier l'administration. | P2 | Administrateur systeme | Acces Web et connexion LDAP valides. |
| Redemarrer Samba et tester les partages. | P2 | Responsable validation | Acces aux partages controles. |
| Redemarrer la messagerie et tester IMAP/SMTP/Roundcube. | P2 | Responsable validation | Connexion et message de test valides. |
| Si des certificats sont declares compromis, appliquer la procedure de revocation et remplacement. | P2 | Responsable validation | Ancienne cle isolee, certificat revoque, nouveau certificat verifie cote client. |
| Consulter Kibana pour les erreurs et les evenements de reprise. | P3 | Responsable validation | Evenements de reprise visibles. |
| Informer les utilisateurs du retour de service. | P3 | Coordinateur | Message conserve. |
| Cloturer l'incident et lister les actions correctives. | P3 | Binome | Compte rendu finalise. |

## Commandes de controle prevues

### Sauvegardes

```bash
cd ~/on-premise/backup
set -a
source .env
set +a

borg check "$BORG_REPO"
borg list "$BORG_REPO"
```

### Restauration LDAP isolee

Les commandes detaillees sont conservees dans
`documentation/restore-procedure.md`. La restauration doit creer un volume de
test distinct, par exemple `restore-openldap-test`, puis extraire le contenu de
l'archive sans ecraser les volumes de production.

### Validation LDAP

```bash
ldapwhoami -x \
  -H ldap://localhost:389 \
  -D "cn=admin,dc=embedded,dc=local" \
  -W
```

```bash
ldapsearch -x \
  -H ldap://localhost:389 \
  -D "cn=admin,dc=embedded,dc=local" \
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
  -b "dc=embedded,dc=local" \
  "(objectClass=*)"
```

### Validation des services dependants

```bash
cd ~/on-premise/infrastructure-compose
docker compose ps
docker compose logs --tail=100 openldap
```

```bash
cd ~/on-premise/samba-ad
docker compose ps
testparm -s
```

```bash
cd ~/on-premise/messaging-compose
docker compose ps
docker compose logs --tail=100 postfix dovecot roundcube
```

## Preuves a collecter

| Preuve | Etat |
| --- | --- |
| Heure de declaration de l'incident | A completer pendant l'exercice |
| Decision d'isolement du serveur compromis | A completer pendant l'exercice |
| Resultat `borg check` | A completer pendant l'exercice |
| Archive saine selectionnee | A completer pendant l'exercice |
| Restauration LDAP en volume isole | A completer pendant l'exercice |
| Resultat `ldapwhoami` | A completer pendant l'exercice |
| Resultat `ldapsearch` | A completer pendant l'exercice |
| Test LAM | A completer pendant l'exercice |
| Test Samba | A completer pendant l'exercice |
| Test messagerie | A completer pendant l'exercice |
| Controle Kibana | A completer pendant l'exercice |
| Communication de retour de service | A completer pendant l'exercice |

## Limites identifiees

- Le temps de restauration OpenLDAP est estime a 1 h 20 dans
  `backup-strategy-validation.md`, mais doit etre mesure pendant un exercice
  complet.
- Le RPO actuel depend de la derniere sauvegarde saine disponible et peut aller
  jusqu'a environ 24 heures de modifications LDAP perdues.
- La copie hors hote et la restauration complete d'un OpenLDAP demarre depuis
  volumes restaures restent a prouver si elles ne sont pas executees pendant
  l'exercice.
- La supervision fournit des indices et des preuves, mais elle ne remplace pas
  les tests fonctionnels LDAP, Samba et messagerie.

## Etat final attendu

L'exercice est considere reussi si le binome presente le plan au formateur
avant intervention, restaure ou decrit la restauration d'une source LDAP saine,
valide les services dependants dans l'ordre du PRA et conserve les decisions
prises dans ce document.
