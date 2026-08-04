# Plan de validation de la messagerie

## Objectif

Vérifier le fonctionnement de l'infrastructure après le déploiement de
Postfix, Dovecot et Roundcube.

Les tests utilisent des comptes de laboratoire et des adresses internes
dédiées. Les mots de passe sont saisis interactivement et ne sont jamais
inscrits dans Git.

## Préparation commune

### Prérequis

- Postfix, Dovecot, Roundcube et la base Roundcube démarrés ;
- OpenLDAP accessible sur le réseau de messagerie ;
- DNS ou résolution locale configurée ;
- certificats TLS installés ;
- compte `test.mail` créé dans OpenLDAP ;
- compte inexistant `absent.mail` réservé au test négatif ;
- deux adresses internes de test, par exemple :
  - `test.mail@embedded.local` ;
  - `test.destinataire@embedded.local`.

### Vérifications initiales

```bash
cd ~/on-premise/messaging-compose
docker compose ps
docker compose logs --tail=50 postfix
docker compose logs --tail=50 dovecot
docker compose logs --tail=50 roundcube
```

Tous les services doivent être démarrés et aucune erreur bloquante ne doit
apparaître dans les journaux.

## M-01 - Authentification d'un utilisateur

### Prérequis

- `test.mail` existe dans OpenLDAP ;
- l'adresse électronique et le mot de passe sont définis ;
- Dovecot est configuré pour interroger LDAP.

### Actions

1. Vérifier l'identité dans LDAP :

```bash
cd ~/on-premise/openldap
docker compose exec openldap ldapsearch -x \
  -H ldap://localhost:3890 \
  -D "cn=admin,dc=embedded,dc=local" -W \
  -b "ou=People,dc=embedded,dc=local" \
  "(uid=test.mail)" dn uid mail
```

2. Tester l'authentification Dovecot avec l'outil prévu par l'image :

```bash
docker compose exec dovecot doveadm auth test test.mail@embedded.local
```

### Résultat attendu

L'utilisateur est retrouvé dans LDAP et Dovecot accepte son authentification
sans exposer le mot de passe dans la sortie.

## M-02 - Envoi d'un courrier électronique

### Prérequis

- soumission SMTP activée sur le port 587 ;
- authentification SMTP obligatoire ;
- compte `test.mail` actif ;
- destinataire interne disponible.

### Actions

Utiliser Roundcube ou un client SMTP de test avec :

- serveur : `mail.embedded.local` ;
- port : `587` ;
- chiffrement : STARTTLS ;
- authentification : compte `test.mail@embedded.local`.

Envoyer un message vers `test.destinataire@embedded.local` avec un objet
identifiable, par exemple `Validation SMTP M-02`.

Contrôler les journaux :

```bash
cd ~/on-premise/messaging-compose
docker compose logs --tail=100 postfix
```

### Résultat attendu

Le message est accepté par Postfix, remis au destinataire et aucune erreur
d'authentification ou de relais ouvert n'est enregistrée.

## M-03 - Réception d'un courrier électronique

### Prérequis

- domaine local déclaré dans Postfix ;
- destinataire présent dans LDAP ;
- livraison locale vers Dovecot configurée ;
- enregistrement DNS nécessaire disponible.

### Actions

1. Envoyer un message depuis un compte de test externe autorisé ou depuis un
   relais de laboratoire.
2. Rechercher le message dans la boîte du destinataire.
3. Contrôler Postfix et Dovecot :

```bash
cd ~/on-premise/messaging-compose
docker compose logs --tail=100 postfix
docker compose logs --tail=100 dovecot
```

### Résultat attendu

Postfix reconnaît le destinataire local, remet le message à Dovecot via LMTP
ou le mécanisme prévu, et le message apparaît dans la boîte.

## M-04 - Connexion IMAP

### Prérequis

- Dovecot écoute sur IMAPS 993 ;
- certificat TLS valide pour le nom utilisé ;
- compte de test actif.

### Actions

Tester l'ouverture TLS :

```bash
openssl s_client -connect mail.embedded.local:993 \
  -servername mail.embedded.local
```

Puis utiliser un client IMAP avec :

- serveur : `mail.embedded.local` ;
- port : `993` ;
- chiffrement : SSL/TLS ;
- identifiant : `test.mail@embedded.local`.

### Résultat attendu

La négociation TLS réussit, le certificat correspond au nom utilisé et le
client affiche les dossiers de la boîte.

## M-05 - Connexion à Roundcube

### Prérequis

- Roundcube démarré ;
- base MariaDB Roundcube accessible ;
- accès HTTPS ou HTTP de laboratoire ;
- Dovecot et Postfix accessibles depuis Roundcube.

### Actions

1. Ouvrir l'URL publiée par Roundcube, par exemple
   `https://mail.embedded.local/`.
2. S'authentifier avec `test.mail@embedded.local`.
3. Ouvrir la boîte de réception.
4. Envoyer un message de test à
   `test.destinataire@embedded.local`.

### Résultat attendu

Roundcube affiche l'interface, accepte l'utilisateur, récupère les messages
via IMAP et transmet un message via SMTP submission.

## M-06 - Envoi d'une pièce jointe

### Prérequis

- test M-02 réussi ;
- taille maximale configurée dans Postfix, Roundcube et éventuellement PHP ;
- fichier de test non sensible inférieur à la limite définie dans la politique.

### Actions

1. Créer un fichier de test, par exemple `piece-jointe-validation.txt`.
2. L'ajouter à un message dans Roundcube.
3. Envoyer le message à `test.destinataire@embedded.local`.
4. Télécharger la pièce jointe depuis la boîte du destinataire.
5. Comparer le fichier reçu avec le fichier envoyé :

```bash
sha256sum piece-jointe-validation.txt
sha256sum piece-jointe-recue.txt
```

### Résultat attendu

La pièce jointe est acceptée sous la limite configurée, transmise sans
corruption et récupérable par le destinataire.

Un fichier dépassant la limite doit être refusé avec un message explicite.

## M-07 - Refus d'un utilisateur inexistant

### Prérequis

- le compte `absent.mail` n'existe pas dans LDAP ;
- Dovecot et Postfix imposent l'authentification ;
- aucun compte local de même nom ne masque l'absence LDAP.

### Actions

1. Vérifier l'absence du compte :

```bash
cd ~/on-premise/openldap
docker compose exec openldap ldapsearch -x \
  -H ldap://localhost:3890 \
  -D "cn=admin,dc=embedded,dc=local" -W \
  -b "dc=embedded,dc=local" "(uid=absent.mail)" dn
```

2. Tenter une connexion Roundcube ou IMAP avec
   `absent.mail@embedded.local`.
3. Tenter une soumission SMTP avec les mêmes identifiants.
4. Contrôler les journaux :

```bash
cd ~/on-premise/messaging-compose
docker compose logs --tail=100 dovecot
docker compose logs --tail=100 postfix
```

### Résultat attendu

L'authentification est refusée. Aucun message n'est envoyé et aucun accès à
une boîte n'est accordé.

Un test est validé uniquement lorsque le résultat obtenu correspond au résultat
attendu et que la preuve ne contient aucun mot de passe ou secret.

## Compte rendu du 4 août 2026

Deux comptes LDAP temporaires ont été utilisés :
`test.mail@embedded.local` et `test.destinataire@embedded.local`.

| Test | Résultat | Preuve ou anomalie |
|---|---|---|
| M-01 Authentification LDAP | Validé | `doveadm auth test` retourne `auth succeeded` |
| M-02 Envoi SMTP | Validé | SMTP AUTH `235`, utilisateur journalisé par Postfix |
| M-03 Réception LMTP | Validé | Message `5E0BE6A3C7F`, statut `sent` |
| M-04 IMAPS TLS | Non validé | `ssl = no`, certificats à installer dans l'activité TLS |
| M-05 Roundcube | Validé | `HTTP/1.1 200 OK`, IMAP et SMTP testés séparément |
| M-06 Pièce jointe | Validé | SHA-256 envoyé et reçu : `965ec755826dffb000bd0b1139b13824e679cb16bf2fd4528b47bda77833e463` |
| M-07 Compte inexistant | Validé | Dovecot `auth failed`, SMTP `535`, puis `554` au destinataire |

### Corrections réalisées

- ajout de `first_valid_uid = 100` dans Dovecot pour accepter l'UID du compte
  virtuel utilisé par l'image ;
- partage du volume Postfix avec Dovecot ;
- remplacement de l'authentification SASL TCP par le socket Unix
  `private/auth` ;
- remplacement du transport LMTP TCP par `private/dovecot-lmtp` ;
- ajout de `allow_all_users=yes` au userdb statique, tandis que Postfix
  continue de valider les destinataires avec sa table LDAP.
