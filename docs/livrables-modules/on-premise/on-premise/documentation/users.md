# Utilisateurs et groupes LDAP


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/users.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Référence de l'annuaire

| Élément | Valeur |
| --- | --- |
| Base DN | `dc=embedded,dc=local` |
| OU utilisateurs | `ou=People,dc=embedded,dc=local` |
| OU groupes | `ou=Groups,dc=embedded,dc=local` |
| Convention UID | initiale du prénom suivie du nom |
| Convention groupes | préfixe `grp-` |

## Utilisateurs vérifiés

| UID | Nom affiché | UID numérique | GID principal |
| --- | --- | ---: | ---: |
| `amartin` | Alice Martin | 10000 | 10004 |
| `bdupont` | Bob Dupont | 10001 | 10003 |
| `cdurand` | Claire Durand | 10002 | 10005 |
| `dbernard` | David Bernard | 10003 | 10002 |
| `erobert` | Emilie Robert | 10004 | 10001 |
| `oadmin` | Olivier ADMIN | 10005 | 10007 |

[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
conservés dans ce document ni dans Git.

## Groupes vérifiés

| Groupe | GID observé | Membres visibles dans LAM |
| --- | ---: | --- |
| `grp-administration` | 10002 | `erobert`, `oadmin` |
| `grp-bureau-etudes` | 10003 | `amartin` |
| `grp-developpement` | 10004 | `bdupont`, `cdurand` |
| `grp-direction` | 10001 | `dbernard` |
| `grp-informatique` | 10006 | À compléter |
| `grp-integration` | 10005 | À compléter |

Les groupes utilisent une classe structurelle `groupOfNames` complétée par
`posixGroup` et un `gidNumber`. Cette organisation permet de les retrouver
dans le navigateur LDAP et de les utiliser dans les profils Unix de LAM.

## Vérifications réalisées

La liste LAM affiche six utilisateurs et six groupes. Une recherche LDAP de
l'arborescence se termine par `result: 0 Success`.

Commandes de contrôle :

~~~bash
cd ~/on-premise/openldap
docker compose exec openldap ldapsearch -x \
  -H ldap://localhost:3890 \
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
  -b "dc=embedded,dc=local" "(objectClass=*)"

docker compose exec openldap ldapsearch -x \
  -H ldap://localhost:3890 \
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
  -b "ou=People,dc=embedded,dc=local" "(uid=amartin)"
~~~

## Règles d'administration

- attribuer les droits par groupes ;
- retirer les appartenances lors d'un changement de service ;
- retirer les groupes d'accès lors d'un départ ;
- désactiver avant suppression lorsqu'un mécanisme de verrouillage est configuré ;
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
- conserver la trace des créations, modifications et suppressions.

## Import rapide par CSV

Les fichiers d'import préparés pour LAM sont conservés dans `ldap-import/` :

- `lam-groups.csv` pour les groupes Unix ;
- `lam-users.csv` pour les utilisateurs Personal + Unix ;
- `README.md` pour l'ordre d'import et le diagnostic des classes d'objets.

[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
dans LAM avant validation, puis vérifié avec `ldapsearch`.
