# Plan de validation de la messagerie


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/validation-mail.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Objectif

Vérifier le fonctionnement de l'infrastructure après le déploiement de
Postfix, Dovecot et Roundcube.

Les tests utilisent des comptes de laboratoire et des adresses internes
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
inscrits dans Git.

## Préparation commune

Validation exécutée le 4 août 2026 avec deux comptes LDAP temporaires :
`test.mail@embedded.local` et `test.destinataire@embedded.local`. Le mot de
passe de TP a été saisi uniquement dans les commandes de test et n'est pas
conservé dans Git.

### Prérequis

- Postfix, Dovecot, Roundcube et la base Roundcube démarrés ;
- OpenLDAP accessible sur le réseau de messagerie ;
- DNS ou résolution locale configurée ;
- certificats TLS installés ou renouvelés pour le nom utilisé ;
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

Résultat obtenu : `mail-db`, `mail-postfix`, `mail-dovecot` et `mail-roundcube`
sont démarrés ; Postfix est `healthy`.

## M-01 - Authentification d'un utilisateur

### Prérequis

- `test.mail` existe dans OpenLDAP ;
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
- Dovecot est configuré pour interroger LDAP.

### Actions

1. Vérifier l'identité dans LDAP :

```bash
cd ~/on-premise/openldap
docker compose exec openldap ldapsearch -x \
  -H ldap://localhost:3890 \
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
  -b "ou=People,dc=embedded,dc=local" \
  "(uid=test.mail)" dn uid mail
```

2. Tester l'authentification Dovecot avec l'outil prévu par l'image :

```bash
docker compose exec dovecot doveadm auth test test.mail@embedded.local
```

### Résultat attendu

L'utilisateur est retrouvé dans LDAP et Dovecot accepte son authentification
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]

### Résultat obtenu

```text
passdb: test.mail@embedded.local auth succeeded
```

Le test négatif avec `absent.mail@embedded.local` retourne `auth failed`.

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

### Résultat obtenu

Postfix a accepté l'authentification SMTP et a journalisé :

```text
235 2.7.0 Authentication successful
sasl_username=test.mail@embedded.local
```

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

### Résultat obtenu

Après correction du contrôle des utilisateurs LMTP, Postfix a journalisé :

```text
5E0BE6A3C7F: to=<test.destinataire@embedded.local> ... status=sent
```

Le message a été retrouvé dans le Maildir du destinataire et consulté par
IMAP.

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

### Résultat obtenu

Le test TLS a été repris dans l'activité de sécurisation du 7 août 2026 avec
les noms `imap.embedded.local`, `smtp.embedded.local` et
`webmail.embedded.local`. Les contrôles détaillés sont dans
`tls-deployment.md` et doivent être rejoués après chaque renouvellement.

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

### Résultat obtenu

```text
HTTP/1.1 200 OK
```

L'accès Web initial a été validé sur `http://localhost:8082`. Après
sécurisation, l'accès HTTPS Roundcube est validé sur
`https://webmail.embedded.local:8443/` avec une réponse `HTTP 200`. Les chemins
IMAP et SMTP utilisés par Roundcube ont également été validés séparément avec
le compte LDAP de test.

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

### Résultat obtenu

La pièce jointe `piece-jointe-validation.txt` a été retrouvée dans le message.
Les empreintes SHA-256 du fichier envoyé et du fichier récupéré sont
identiques :

```text
965ec755826dffb000bd0b1139b13824e679cb16bf2fd4528b47bda77833e463
```

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
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
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

### Résultat obtenu

```text
passdb: absent.mail@embedded.local auth failed
535 5.7.8 Error: authentication failed
```

## Tableau de compte rendu

| Test | Date | Résultat | Preuve | Anomalie | Correctif |
|---|---|---|---|---|---|
| M-01 | 2026-08-04 | Validé | `doveadm auth test`, LDAP | Compte de test absent au départ | Création de deux comptes LDAP temporaires |
| M-02 | 2026-08-04 | Validé | SMTP AUTH, Postfix | Auth SASL TCP instable | Passage au socket Unix Dovecot/Postfix |
| M-03 | 2026-08-04 | Validé | ID `5E0BE6A3C7F`, LMTP | LMTP ne trouvait pas les utilisateurs | `allow_all_users=yes` côté userdb statique, avec validation LDAP par Postfix |
| M-04 | 2026-08-07 | Validé côté TLS | `openssl s_client`, chaîne Campus CA | Certificats absents le 4 août | Activation TLS documentée dans `tls-deployment.md` |
| M-05 | 2026-08-04 puis 2026-08-07 | Validé | HTTP puis HTTPS `200 OK`, tests IMAP/SMTP | Aucune | Passage HTTPS via Nginx Roundcube |
| M-06 | 2026-08-04 | Validé | SHA-256 identique | Aucune | Aucune |
| M-07 | 2026-08-04 | Validé | `auth failed`, SMTP `535`, puis `554` au destinataire | Le réseau Docker contournait l'authentification SMTP | Restrictions dédiées au service `submission` |

Un test est validé uniquement lorsque le résultat obtenu correspond au résultat
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
