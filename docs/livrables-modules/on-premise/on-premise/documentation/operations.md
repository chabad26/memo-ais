# Procédures courantes d'administration


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/operations.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Périmètre

Ce document décrit les opérations courantes sur OpenLDAP et le serveur de
fichiers Samba du laboratoire Embedded Solutions.

- Base DN : `dc=embedded,dc=local`
- Utilisateurs : `ou=People,dc=embedded,dc=local`
- Groupes : `ou=Groups,dc=embedded,dc=local`
- Interface LDAP : LDAP Account Manager
- Serveur de fichiers : conteneur Samba `samba-ldap`

## Prérequis communs

- demande validée par le responsable concerné ;
- compte administrateur autorisé ;
- conteneurs OpenLDAP et Samba démarrés ;
- dépendances et données vérifiées avant toute suppression ;
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]

```bash
cd ~/on-premise/openldap
docker compose ps
cd ~/on-premise/samba-ad
docker compose ps
```

Les identités sont administrées dans LAM. Les commandes LDAP servent aux
recherches et aux vérifications, sauf indication contraire.

## 1. Ajouter un collaborateur

### Prérequis

- arrivée validée ;
- identité, identifiant, service et adresse électronique connus ;
- groupe LDAP du service existant ;
- identifiant unique vérifié.

### Étapes

1. Ouvrir LAM et sélectionner le suffixe `ou=People`.
2. Créer l'utilisateur avec la convention `prenominitiale + nom`, par
   exemple `amartin` pour Alice Martin.
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
   temporaire.
4. Sélectionner le groupe principal et les groupes complémentaires nécessaires.
5. Enregistrer l'entrée LDAP.
6. Ajouter les accès SMB uniquement s'ils sont validés.

### Vérifications

```bash
cd ~/on-premise/openldap
docker compose exec openldap ldapsearch -x \
  -H ldap://localhost:3890 \
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
  -b "ou=People,dc=embedded,dc=local" \
  "(uid=amartin)" dn uid cn mail

cd ~/on-premise/samba-ad
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
docker compose exec samba getent group grp-bureau-etudes
```

Le compte doit être retrouvé dans LDAP et résolu par NSS dans Samba.

## 2. Changer le service d'un collaborateur

### Prérequis

- mobilité validée ;
- ancien et nouveau service identifiés ;
- date d'application connue ;
- accès à conserver ou à retirer évalués.

### Étapes

1. Ouvrir la fiche de l'utilisateur dans LAM.
2. Retirer l'utilisateur de l'ancien groupe métier.
3. L'ajouter au groupe du nouveau service.
4. Conserver seulement les groupes transverses justifiés.
5. Enregistrer les modifications.
6. Recharger Samba si la liste d'un partage a été modifiée.

### Vérifications

```bash
cd ~/on-premise/openldap
docker compose exec openldap ldapsearch -x \
  -H ldap://localhost:3890 \
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
  -b "ou=Groups,dc=embedded,dc=local" \
  "(memberUid=amartin)" dn cn

cd ~/on-premise/samba-ad
docker compose exec samba getent group | grep amartin
docker compose exec samba smbclient -L //localhost -U amartin
```

Le nouveau groupe doit apparaître et l'ancien ne doit plus apparaître, sauf
conservation temporaire documentée.

## 3. Désactiver un compte

### Prérequis

- désactivation validée ;
- date et motif documentés ;
- fichiers, messagerie, certificats et tâches vérifiés ;
- conservation de l'entrée LDAP décidée.

### Étapes

1. Relever le DN et les groupes de l'utilisateur.
2. Retirer le compte des groupes d'accès qui ne doivent plus être utilisés.
3. Dans LAM, appliquer le verrouillage prévu par le profil LDAP.
4. Désactiver également l'accès SMB :

```bash
cd ~/on-premise/samba-ad
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
```

5. Journaliser la date, le motif, l'administrateur et le résultat.

### Vérifications

```bash
cd ~/on-premise/openldap
docker compose exec openldap ldapsearch -x \
  -H ldap://localhost:3890 \
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
  -b "dc=embedded,dc=local" \
  "(uid=amartin)" dn pwdAccountLockedTime loginShell

cd ~/on-premise/samba-ad
docker compose exec samba pdbedit -L -v -u amartin
```

Le compte désactivé ne doit plus ouvrir de session SMB. L'entrée reste
conservée pour permettre une réactivation ou l'analyse des dépendances.

## 4. Supprimer un compte

### Prérequis

- suppression explicitement validée ;
- délai de conservation terminé ;
- aucune dépendance vers le DN ;
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]

### Étapes

1. Désactiver d'abord le compte.
2. Vérifier les groupes, partages, certificats et automatisations.
3. Exporter uniquement les attributs nécessaires :

```bash
cd ~/on-premise/openldap
docker compose exec openldap ldapsearch -x \
  -H ldap://localhost:3890 \
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
  -b "uid=amartin,ou=People,dc=embedded,dc=local" \
  -s base dn uid cn mail > /tmp/amartin-suppression.ldif
```

4. Supprimer l'entrée dans LAM, ou après validation :

```bash
docker compose exec openldap ldapdelete -x \
  -H ldap://localhost:3890 \
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
  "uid=amartin,ou=People,dc=embedded,dc=local"
```

5. Retirer le compte du backend Samba si nécessaire.
6. Documenter la suppression dans le journal technique.

### Vérifications

```bash
docker compose exec openldap ldapsearch -x \
  -H ldap://localhost:3890 \
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
  -b "dc=embedded,dc=local" "(uid=amartin)" dn

cd ~/on-premise/samba-ad
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
```

La recherche LDAP ne doit plus retourner l'entrée et le compte ne doit plus
être résolu par NSS.

## 5. Créer un nouvel espace de partage

### Prérequis

- nom et objectif validés ;
- groupe LDAP responsable identifié ;
- droits lecture/écriture définis ;
- sauvegarde prévue.

### Étapes

1. Ajouter une section dans `~/on-premise/samba-ad/config/smb.conf` :

```ini
[Projet-test]
   comment = Espace de test
   path = /srv/samba/projet-test
   browseable = yes
   read only = no
   guest ok = no
   valid users = @grp-developpement
   create mask = 0660
   directory mask = 0770
   force user = nobody
   force group = nogroup
```

2. Créer le répertoire dans le volume du conteneur :

```bash
cd ~/on-premise/samba-ad
docker compose exec samba mkdir -p /srv/samba/projet-test
docker compose exec samba chown nobody:nogroup /srv/samba/projet-test
docker compose exec samba chmod 2770 /srv/samba/projet-test
```

3. Reconstruire l'image, copier explicitement la configuration versionnée dans
   le volume persistant, puis relancer Samba :

```bash
docker compose build samba
docker compose run --rm --entrypoint sh samba -c \
  'install -m 0644 /usr/local/share/samba-config/smb.conf /var/lib/samba-config/smb.conf'
docker compose up -d
docker compose exec samba testparm -s
```

### Vérifications

```bash
docker compose exec samba smbclient -L //localhost -U amartin
docker compose exec samba smbclient //localhost/Projet-test -U amartin -c 'ls'
```

Le partage doit apparaître et seuls les membres du groupe autorisé doivent
pouvoir l'ouvrir.

## 6. Attribuer un groupe à un espace de partage

### Prérequis

- groupe LDAP existant et correctement peuplé ;
- autorisation validée ;
- impact sur les utilisateurs évalué.

### Étapes

1. Vérifier le groupe dans LAM ou par recherche LDAP :

```bash
cd ~/on-premise/openldap
docker compose exec openldap ldapsearch -x \
  -H ldap://localhost:3890 \
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
  -b "ou=Groups,dc=embedded,dc=local" \
  "(cn=grp-developpement)" cn memberUid
```

2. Modifier `valid users` dans `samba-ad/config/smb.conf` :

```ini
valid users = @grp-developpement
```

3. Synchroniser, valider et recharger :

```bash
cd ~/on-premise/samba-ad
docker compose build samba
docker compose run --rm --entrypoint sh samba -c \
  'install -m 0644 /usr/local/share/samba-config/smb.conf /var/lib/samba-config/smb.conf'
docker compose up -d
docker compose exec samba testparm -s
```

4. Tester avec un membre puis avec un compte hors groupe.

### Vérifications

```bash
docker compose exec samba getent group grp-developpement
docker compose exec samba smbclient //localhost/Developpement -U amartin -c 'ls'
```

Le membre doit accéder au partage et l'utilisateur hors groupe doit recevoir un
refus. Toute modification est reportée dans `journal.md`.

## Traçabilité Git

Après vérification :

```bash
cd ~/on-premise
git status
git diff --check
git add documentation/operations.md samba-ad/config/smb.conf samba-ad/entrypoint.sh
git commit -m "Documenter les operations courantes Samba et LDAP"
```

[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]

## Plan de validation associé

Les tests d'authentification, d'accès, de refus, d'ajout, de mobilité et de
désactivation sont décrits dans `documentation/validation.md`. Toute procédure
modifiée doit être rejouée ou marquée comme nécessitant une nouvelle validation.
