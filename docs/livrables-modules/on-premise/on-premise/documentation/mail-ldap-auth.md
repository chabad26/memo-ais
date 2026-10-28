# Authentification LDAP de la messagerie


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/mail-ldap-auth.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Objectif

Les comptes de messagerie sont ceux deja presents dans OpenLDAP. Aucun compte
utilisateur n'est cree separement dans Postfix, Dovecot ou Roundcube.

## Architecture

```text
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
                   |
                   +----------SMTP-> Postfix --SASL interne--> Dovecot
                                           |
                                           +-- table LDAP des destinataires
```

Parametres retenus :

| Parametre | Valeur de laboratoire |
|---|---|
| Base LDAP | `dc=embedded,dc=local` |
| Utilisateurs | `ou=People,dc=embedded,dc=local` |
| Groupes | `ou=Groups,dc=embedded,dc=local` |
| Serveur LDAP vu des conteneurs | `openldap:3890` |
| Compte technique Postfix | `cn=mail-reader,ou=Services,dc=embedded,dc=local` |
| Authentification IMAP | Dovecot avec `auth_bind` LDAP |
| Authentification SMTP | Postfix SASL deleguee a Dovecot |
| Webmail | Roundcube via IMAP et SMTP |

## Dovecot

`dovecot/dovecot-ldap.conf.ext` utilise le DN de l'utilisateur :

```conf
hosts = openldap:3890
base = ou=People,dc=embedded,dc=local
auth_bind = yes
auth_bind_userdn = uid=%n,ou=People,dc=embedded,dc=local
user_filter = (&(objectClass=posixAccount)(uid=%n))
pass_filter = (&(objectClass=posixAccount)(uid=%n))
```

Postfix utilise le socket Unix `private/auth` partage dans le volume de
spool. La livraison LMTP utilise le socket `private/dovecot-lmtp` du même
volume.

## Postfix

Le fichier `postfix-init.sh` cree au demarrage la table LDAP des
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
ignore par Git.

Le userdb statique de Dovecot utilise `allow_all_users=yes` pour permettre la
verification LMTP. La liste des destinataires acceptes reste controlee par la
table LDAP Postfix : un destinataire inexistant est donc rejete avant la
livraison.

Verification realisee :

```bash
cd ~/on-premise/messaging-compose
docker compose exec postfix \
  postmap -q amartin@embedded.local ldap:/etc/postfix/ldap-users.cf
```

Resultat :

```text
amartin
```

Le compte technique LDAP dispose d'un droit de lecture sur l'annuaire. Les
droits ont ete verifies avec :

```bash
docker exec openldap ldapwhoami -x -H ldap://localhost:3890 \
  -D "cn=mail-reader,ou=Services,dc=embedded,dc=local" -W
```

## Roundcube

Roundcube utilise :

```text
IMAP : dovecot:143
SMTP : postfix:587
```

Il ne contient pas de base d'utilisateurs locale. La saisie d'un identifiant
LDAP dans Roundcube est transmise a Dovecot, qui realise l'authentification.
Le port IMAP non chiffre est temporaire pour le laboratoire ; le TLS sera
configure dans l'activite dediee.

## Verifications

```bash
docker compose config --quiet
docker compose ps
docker compose exec dovecot doveconf -n
docker compose exec postfix postconf -n
curl -I http://localhost:8082
```

Resultats observes : services demarres, Postfix configure avec SASL Dovecot,
table LDAP fonctionnelle et Roundcube en `HTTP/1.1 200 OK`.

Le test final d'authentification a été réalisé avec des comptes de TP dédiés,
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
dans Git.

## Reponses

### Quels services interrogent directement LDAP ?

Dovecot interroge LDAP pour authentifier les utilisateurs. Postfix interroge
LDAP pour rechercher les destinataires, mais delegue le controle du mot de
passe a Dovecot. Roundcube ne parle pas directement a LDAP.

### Quels avantages presente une authentification centralisee ?

Elle fournit une identite unique, simplifie les changements de service et la
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]

### Pourquoi ne pas creer les utilisateurs dans chaque service ?

Des comptes locaux separes peuvent rester actifs apres le depart d'un salarie
et produire des divergences. LDAP devient le referentiel unique et les
services reutilisent les memes comptes.

## Documents associes

- `messaging-compose/docker-compose.yml`
- `messaging-compose/dovecot/dovecot.conf`
- `messaging-compose/dovecot/dovecot-ldap.conf.ext`
- `messaging-compose/postfix-init.sh`
- `documentation/validation-mail.md`
