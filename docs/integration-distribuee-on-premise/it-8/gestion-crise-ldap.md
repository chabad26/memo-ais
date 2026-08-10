# Itération 8 - Gestion de crise LDAP

## Objectif

Mettre en oeuvre le PCA/PRA face a un incident majeur affectant le service
d'authentification centralisee.

Le scenario impose une decision de crise avant toute action technique : la base
LDAP est corrompue, la configuration du serveur n'est plus fiable, le serveur
doit etre arrete immediatement et aucun element du serveur compromis ne doit
etre modifie afin de permettre une analyse forensique ulterieure.

## Documents de travail

La feuille d'exercice est conservee dans cette iteration du memo. La documentation
operationnelle a produire et a mettre a jour se trouve dans le depot
`/home/oliv/on-premise`.

| Document | Role dans l'exercice |
| --- | --- |
| `/home/oliv/on-premise/documentation/PCA.md` | Mesures de continuite et services couverts. |
| `/home/oliv/on-premise/documentation/PRA.md` | Ordre de reprise et procedures par service. |
| `/home/oliv/on-premise/documentation/inventory.md` | Inventaire des services, ports, volumes et dependances. |
| `/home/oliv/on-premise/documentation/backup-strategy-validation.md` | Scenario de corruption LDAP et estimation de restauration. |
| `/home/oliv/on-premise/documentation/restore-procedure.md` | Commandes de restauration BorgBackup en environnement isole. |
| `/home/oliv/on-premise/documentation/incident-majeur-ldap.md` | Livrable de gestion de crise pour cet exercice. |

!!! warning "Regle de conservation"
    Le serveur compromis ne doit pas etre repare, nettoye, redemarre ou modifie
    directement. Les actions de reprise doivent utiliser une restauration
    controlee dans un environnement sain ou isole.

## Situation annoncee

Le formateur informe le binome qu'une attaque a compromis le serveur LDAP.

Elements connus :

- la base LDAP est corrompue ;
- la configuration du serveur ne peut plus etre consideree comme fiable ;
- le serveur doit etre immediatement arrete ou isole ;
- aucun element du serveur ne doit etre modifie pour conserver les preuves ;
- les services dependants de l'authentification peuvent etre impactes.

## Services impactes

| Service | Consequence probable | Niveau d'impact |
| --- | --- | --- |
| OpenLDAP | Authentification centralisee indisponible ou non fiable. | Critique |
| LDAP Account Manager | Administration Web LDAP inutilisable tant qu'OpenLDAP est compromis. | Eleve |
| Samba | Acces aux partages dependant des groupes LDAP perturbe. | Eleve |
| Messagerie | Authentification Dovecot/Postfix/Roundcube par LDAP perturbee. | Eleve |
| Supervision | Les journaux aident au diagnostic, mais ne doivent pas bloquer la reprise. | Moyen |
| Sauvegardes | Necessaires pour selectionner une archive saine avant corruption. | Critique |
| WordPress | Impact indirect sauf dependance future a LDAP. | Faible a moyen |

## Reunion de crise

Avant toute intervention, organiser une reunion courte avec un ordre du jour
strict.

| Point | Decision attendue |
| --- | --- |
| Qualification | Confirmer l'incident majeur sur OpenLDAP. |
| Gel | Interdire toute modification sur le serveur compromis. |
| Perimetre | Identifier les services dependants : Samba, messagerie, LAM, supervision. |
| Priorites | Restaurer l'authentification avant les services qui en dependent. |
| Roles | Designer coordination, systeme, sauvegarde, validation et communication. |
| Preuves | Lister les journaux, captures et commandes a conserver. |
| Validation formateur | Presenter le plan avant intervention technique. |

## Repartition des roles

| Role | Responsable | Mission |
| --- | --- | --- |
| Coordinateur de crise | Membre 1 | Animer la reunion, tenir le compte rendu, faire valider le plan. |
| Administrateur systeme | Membre 2 | Isoler le serveur compromis sans modifier ses donnees, preparer la reprise. |
| Responsable sauvegarde | Membre 1 | Identifier la derniere archive saine et verifier son integrite. |
| Responsable validation | Membre 2 | Tester LDAP, Samba, messagerie et supervision apres restauration. |
| Communication utilisateurs | Binome | Informer des indisponibilites et du retour progressif des services. |

## Plan d'actions retenu

| Action | Priorite | Responsable | Preuve attendue |
| --- | --- | --- | --- |
| Declarer l'incident majeur LDAP et ouvrir le compte rendu. | Immediate | Coordinateur | Heure de declaration et participants. |
| Isoler ou arreter le serveur LDAP compromis sans modifier ses donnees. | Immediate | Administrateur systeme | Action notee, aucun nettoyage realise. |
| Geler les changements LDAP, Samba et messagerie dependants de LDAP. | Immediate | Coordinateur | Decision inscrite dans le compte rendu. |
| Evaluer les impacts sur LAM, Samba, messagerie et supervision. | P1 | Binome | Tableau d'impact complete. |
| Selectionner une archive saine anterieure a la compromission. | P1 | Responsable sauvegarde | Nom d'archive, date, resultat `borg check`. |
| Restaurer les donnees LDAP dans un volume ou repertoire isole. | P1 | Administrateur systeme | Commandes de restauration et chemin isole. |
| Demarrer un OpenLDAP de test depuis les donnees restaurees. | P1 | Administrateur systeme | `docker compose ps`, journaux et recherche LDAP. |
| Verifier la base, les OU, les groupes et les utilisateurs. | P1 | Responsable validation | `ldapwhoami` et `ldapsearch` reussis. |
| Basculer vers l'annuaire restaure apres validation. | P1 | Binome | Decision de bascule et heure de remise en service. |
| Redemarrer LAM, Samba et la messagerie dans l'ordre du PRA. | P2 | Administrateur systeme | Tests fonctionnels par service. |
| Controler les tableaux de bord et journaux de supervision. | P2 | Responsable validation | Evenements visibles dans Kibana. |
| Informer les utilisateurs de l'etat du service. | P2 | Coordinateur | Message de communication conserve. |
| Cloturer l'exercice avec decisions, limites et actions correctives. | P3 | Binome | Livrable `incident-majeur-ldap.md` complete. |

## Commandes de reference

Ces commandes ne doivent pas etre executees sur le serveur compromis si elles
modifient son etat. Elles servent a preparer la restauration depuis les
sauvegardes et a valider un environnement sain.

```bash
cd /home/oliv/on-premise/backup
set -a
source .env
set +a

borg check "$BORG_REPO"
borg list "$BORG_REPO"
```

```bash
cd /home/oliv/on-premise/infrastructure-compose
docker compose config
docker compose up -d
docker compose ps
docker compose logs --tail=100 openldap
```

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

## Livrable attendu

Dans `/home/oliv/on-premise/documentation/incident-majeur-ldap.md`, conserver :

- le compte rendu de la reunion de crise ;
- les consequences identifiees sur les autres services ;
- les roles attribues ;
- le plan d'actions valide avant intervention ;
- les decisions prises ;
- les preuves de restauration ou les preuves restant a produire ;
- les limites de l'exercice.

## Questions de synthese

1. Pourquoi ne faut-il pas reparer directement le serveur LDAP compromis ?
2. Quels services doivent etre testes apres la restauration d'OpenLDAP ?
3. Quelle difference faites-vous entre PCA et PRA dans ce scenario ?
4. Quelle preuve permet de dire qu'une archive est saine ?
5. Pourquoi LAM n'est-il pas prioritaire par rapport a OpenLDAP ?

## Resultat attendu

Le binome doit etre capable de presenter au formateur un plan coherent avant
intervention, avec un ordre de reprise justifie, des roles clairs et une
documentation exploitable dans le depot `/home/oliv/on-premise`.
