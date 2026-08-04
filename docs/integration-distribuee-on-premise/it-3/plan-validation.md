# Plan de validation de l'infrastructure

## Objectif

Vérifier l'authentification LDAP, les accès Samba et les opérations courantes
d'administration.

Les tests qui modifient une identité utilisent des comptes de test et non des
comptes réels sans validation préalable.

## Préparation commune

```bash
cd ~/on-premise/openldap
docker compose ps

cd ~/on-premise/samba-ad
docker compose ps
docker compose exec samba testparm -s
```

Comptes de test recommandés :

| Compte | Usage | Groupe attendu |
|---|---|---|
| `test.acces` | authentification et accès autorisé | `grp-bureau-etudes` |
| `test.refus` | contrôle du moindre privilège | aucun groupe ciblé |
| `test.arrivee` | ajout d'un collaborateur | groupe choisi pendant le test |
| `test.mobilite` | changement de service | ancien et nouveau groupes |
| `test.depart` | désactivation | groupe retiré avant le test |

Les mots de passe sont saisis interactivement et ne sont jamais écrits dans le
dépôt.

## V-01 - Authentification d'un utilisateur

### Prérequis

- OpenLDAP et Samba démarrés ;
- `test.acces` présent dans `ou=People` ;
- mot de passe LDAP et mot de passe Samba définis ;
- appartenance à `grp-bureau-etudes`.

### Actions

```bash
cd ~/on-premise/openldap
docker compose exec openldap ldapsearch -x \
  -H ldap://localhost:3890 \
  -D "cn=admin,dc=embedded,dc=local" -W \
  -b "ou=People,dc=embedded,dc=local" \
  "(uid=test.acces)" dn uid cn

cd ~/on-premise/samba-ad
docker compose exec samba getent passwd test.acces
docker compose exec samba smbclient -L //localhost -U test.acces
```

### Résultat attendu

L'entrée est retrouvée dans LDAP, l'utilisateur est résolu par NSS et
`smbclient` accepte l'authentification.

## V-02 - Accès aux espaces de partage

### Prérequis

- comptes membres des groupes adaptés ;
- les quatre partages sont présents dans `smb.conf` ;
- `testparm -s` ne retourne aucune erreur.

### Actions

```bash
cd ~/on-premise/samba-ad
docker compose exec samba smbclient //localhost/Commun -U test.acces -c 'ls'
docker compose exec samba smbclient //localhost/Bureau-etudes -U test.acces -c 'ls'
docker compose exec samba smbclient //localhost/Developpement -U test.developpement -c 'ls'
docker compose exec samba smbclient //localhost/Administration -U test.administration -c 'ls'
```

Tester aussi l'écriture :

```bash
docker compose exec samba sh -c 'printf "validation\\n" > /tmp/validation.txt'
docker compose exec samba smbclient //localhost/Bureau-etudes -U test.acces \
  -c 'put /tmp/validation.txt validation.txt; ls'
```

### Résultat attendu

Chaque compte autorisé ouvre le partage prévu. L'écriture réussit uniquement
sur les espaces où elle est autorisée.

## V-03 - Refus d'accès d'un utilisateur non autorisé

### Prérequis

- `test.refus` existe ;
- il n'appartient pas au groupe du partage testé ;
- `guest ok = no` et `valid users` sont configurés.

### Actions

```bash
cd ~/on-premise/samba-ad
docker compose exec samba smbclient //localhost/Administration -U test.refus -c 'ls'
docker compose exec samba getent group grp-administration
```

### Résultat attendu

La connexion retourne un refus d'accès. Aucun accès invité ne doit contourner
le contrôle de groupe.

## V-04 - Ajout d'un nouveau collaborateur

### Prérequis

- arrivée validée ;
- identifiant `test.arrivee` disponible ;
- groupe du service existant.

### Actions

1. Créer `test.arrivee` dans LAM sous `ou=People`.
2. Renseigner identité, courriel et mot de passe.
3. Ajouter le compte au groupe métier prévu.
4. Ajouter les attributs Samba et le mot de passe SMB si nécessaire.
5. Vérifier :

```bash
cd ~/on-premise/openldap
docker compose exec openldap ldapsearch -x \
  -H ldap://localhost:3890 \
  -D "cn=admin,dc=embedded,dc=local" -W \
  -b "dc=embedded,dc=local" "(uid=test.arrivee)" dn uid cn

cd ~/on-premise/samba-ad
docker compose exec samba getent passwd test.arrivee
```

### Résultat attendu

Le compte existe dans LDAP, est résolu par Samba et possède uniquement les
groupes validés.

## V-05 - Changement de service

### Prérequis

- `test.mobilite` existe ;
- ancien et nouveau groupes identifiés ;
- mobilité validée.

### Actions

1. Retirer le compte de l'ancien groupe dans LAM.
2. L'ajouter au nouveau groupe.
3. Vérifier :

```bash
cd ~/on-premise/openldap
docker compose exec openldap ldapsearch -x \
  -H ldap://localhost:3890 \
  -D "cn=admin,dc=embedded,dc=local" -W \
  -b "ou=Groups,dc=embedded,dc=local" \
  "(memberUid=test.mobilite)" dn cn

cd ~/on-premise/samba-ad
docker compose exec samba getent group | grep test.mobilite
```

### Résultat attendu

Le nouveau groupe est présent, l'ancien ne l'est plus et les accès SMB
correspondent au nouveau service.

## V-06 - Désactivation d'un compte

### Prérequis

- `test.depart` existe ;
- groupes et dépendances relevés ;
- désactivation demandée au lieu d'une suppression immédiate.

### Actions

1. Retirer le compte des groupes d'accès dans LAM.
2. Appliquer le verrouillage LDAP prévu par le profil.
3. Désactiver le compte Samba :

```bash
cd ~/on-premise/samba-ad
docker compose exec samba smbpasswd -d test.depart
```

4. Vérifier l'entrée et tenter une connexion :

```bash
cd ~/on-premise/openldap
docker compose exec openldap ldapsearch -x \
  -H ldap://localhost:3890 \
  -D "cn=admin,dc=embedded,dc=local" -W \
  -b "dc=embedded,dc=local" "(uid=test.depart)" dn pwdAccountLockedTime

cd ~/on-premise/samba-ad
docker compose exec samba smbclient //localhost/Commun -U test.depart -c 'ls'
```

### Résultat attendu

L'entrée peut rester conservée pour la traçabilité, mais le compte ne doit plus
s'authentifier sur un partage SMB.

## Compte rendu

Pour chaque test, consigner la date, l'administrateur, le compte utilisé, le
résultat, la capture éventuelle et toute anomalie dans `journal.md`.

Un test est validé uniquement si le résultat correspond à l'attendu et si
aucune donnée sensible n'est ajoutée au dépôt.
