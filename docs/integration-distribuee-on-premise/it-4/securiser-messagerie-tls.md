# Préparer la sécurisation TLS de la messagerie

## Objectif

Identifier les échanges et les services qui devront être protégés par TLS
après le déploiement fonctionnel de Postfix, Dovecot et Roundcube.

Aucun certificat n'est généré ou installé pendant cette activité.

## 1. Échanges à protéger

| Échange | Port | Protection attendue | Certificat présenté par |
|---|---:|---|---|
| Navigateur vers Roundcube | 443 | HTTPS avec TLS | Roundcube ou reverse proxy |
| Client vers Dovecot | 993 | IMAPS avec TLS direct | Dovecot |
| Client vers Dovecot | 143 | IMAP avec STARTTLS si utilisé | Dovecot |
| Client vers Postfix | 587 | SMTP submission avec STARTTLS | Postfix |
| Serveurs SMTP entre eux | 25 | STARTTLS opportuniste ou obligatoire selon le relais | Postfix |
| Postfix/Dovecot vers LDAP | 636 ou StartTLS sur 389 | LDAPS ou StartTLS | OpenLDAP |
| Roundcube vers ses services internes | réseau Docker | TLS selon l'exposition et le niveau de confiance | Service concerné |
| Administration Web LAM | 443 | HTTPS | LAM ou reverse proxy |

Le chiffrement des flux internes Docker devra être décidé selon le modèle de
menace. Le réseau Docker ne doit pas être considéré comme une preuve
suffisante de confiance pour les flux qui sortent de l'hôte.

## 2. Services nécessitant un certificat

### Roundcube

Roundcube doit être accessible en HTTPS. Le certificat doit couvrir le nom
utilisé par les navigateurs, par exemple :

```text
mail.embedded.local
```

En production, le nom devra appartenir à un domaine maîtrisé par l'entreprise.

### Dovecot

Dovecot présente un certificat pour les connexions IMAPS sur le port 993 et
pour IMAP avec STARTTLS sur le port 143.

Le certificat doit contenir le nom utilisé par les clients de messagerie. Les
anciens protocoles et suites cryptographiques obsolètes devront être
désactivés.

### Postfix

Postfix présente un certificat pour la soumission SMTP sur le port 587 et pour
les connexions SMTP configurées avec STARTTLS.

Le port 25 entre serveurs doit être configuré avec une politique documentée :
TLS opportuniste pour la compatibilité générale ou TLS obligatoire lorsqu'un
relais de confiance est utilisé.

### OpenLDAP

Postfix et Dovecot utilisent l'annuaire existant pour les recherches et
l'authentification. Le flux devra utiliser LDAPS sur le port 636 ou StartTLS
sur le port 389 afin que les identifiants et les recherches ne circulent pas en
clair.

### LDAP Account Manager

LAM est une interface d'administration. Son accès doit être protégé par
HTTPS, surtout lorsqu'il est accessible depuis un réseau autre que
l'administration locale.

## 3. Risques d'une messagerie sans certificats

Une messagerie sans TLS expose notamment :

- les identifiants IMAP et SMTP à l'interception ;
- le contenu des messages et des pièces jointes ;
- les noms d'utilisateurs et les adresses électroniques ;
- les recherches LDAP et les mots de passe de comptes techniques ;
- les sessions Web Roundcube au vol de session ;
- les échanges SMTP à l'écoute ou à la modification sur le réseau ;
- les utilisateurs aux attaques de type interception ou serveur usurpé.

Le chiffrement ne suffit pas à garantir l'authenticité d'un serveur. Le
certificat doit être valide, correspondre au nom demandé et être signé par une
autorité reconnue par le poste client.

## 4. Vérification de l'identité des serveurs

Les postes clients vérifieront :

1. que le nom demandé correspond à un nom présent dans le SAN du certificat ;
2. que la période de validité est correcte ;
3. que le certificat n'est pas révoqué selon le mécanisme retenu ;
4. que la chaîne remonte à une autorité de certification de confiance ;
5. que le certificat n'est pas auto-signé ou remplacé par une autorité
   inconnue.

Pour les services internes, deux solutions sont possibles :

- une autorité de certification interne déployée dans le magasin de confiance
  des postes gérés ;
- un certificat délivré par une autorité publique pour un nom de domaine
  contrôlé par l'entreprise.

Un certificat auto-signé peut servir à un test isolé, mais il ne doit pas être
retenu comme solution d'exploitation normale.

## 5. Emplacement des certificats

| Service | Certificat et clé privée à installer |
|---|---|
| Roundcube | dans le reverse proxy ou le serveur Web ; clé lisible uniquement par le service |
| Dovecot | chemins TLS dans la configuration Dovecot |
| Postfix | chemins TLS dans la configuration Postfix |
| OpenLDAP | certificat, clé privée et chaîne dans la configuration TLS de slapd |
| LAM | dans le serveur Web ou le reverse proxy |
| Postes clients | certificat de l'autorité racine dans le magasin de confiance |

Les clés privées ne doivent pas être copiées dans Git, dans les captures ou dans
les fichiers Compose versionnés. Elles devront être injectées par un secret,
un volume protégé ou un mécanisme de gestion de certificats.

## 6. Noms à prévoir

Le certificat principal de messagerie devra au minimum couvrir :

```text
mail.embedded.local
imap.embedded.local
smtp.embedded.local
webmail.embedded.local
```

Les noms effectivement retenus devront être cohérents avec DNS, Roundcube,
Postfix, Dovecot et la configuration des clients.

## 7. Réponses aux questions

### Quels services auront besoin d'un certificat ?

Roundcube, Dovecot, Postfix et OpenLDAP auront besoin de certificats pour
protéger leurs connexions. LAM devra également être servi en HTTPS. Les postes
clients devront faire confiance à l'autorité qui signe ces certificats.

### Quels risques présente une messagerie sans certificats ?

Les identifiants, messages et pièces jointes peuvent être interceptés ou
modifiés. Un attaquant peut aussi usurper un serveur, voler une session
Roundcube ou récupérer le mot de passe d'un compte technique LDAP.

### Comment les postes clients pourront-ils vérifier l'identité des serveurs ?

Ils vérifieront le nom du serveur dans le SAN, la chaîne de certification, la
validité temporelle et la confiance accordée à l'autorité de certification.
Les noms DNS utilisés par les clients devront donc être stables.

### Où les certificats devront-ils être installés ?

Les certificats seront installés sur Roundcube ou son reverse proxy, Dovecot,
Postfix, OpenLDAP et LAM. Le certificat racine de l'autorité interne sera
déployé dans le magasin de confiance des postes clients.

## 8. Suite prévue

Les certificats seront mis en œuvre après le déploiement fonctionnel :

1. choisir l'autorité de certification ;
2. définir les noms DNS ;
3. générer les demandes de certificats ;
4. installer les certificats et les clés avec des permissions minimales ;
5. activer TLS dans chaque service ;
6. tester les connexions valides et les certificats invalides ;
7. documenter le renouvellement et la révocation.
