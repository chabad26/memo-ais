# Diagnostiquer la suppression d'une boîte Inbox

## Objectif

Diagnostiquer puis traiter la suppression accidentelle de la boîte de
réception `Inbox` d'un compte IMAP sans écraser les autres dossiers.

## Incident retenu

Un utilisateur a supprimé sa boîte de réception depuis un client IMAP ou
Roundcube. Les messages ne sont plus visibles et la boîte peut être vide,
absente ou recréée automatiquement.

## 1. Symptômes

- `Inbox` n'apparaît plus ou est vide ;
- les autres dossiers restent accessibles ;
- Dovecot accepte toujours l'authentification ;
- les nouveaux messages peuvent encore être livrés.

Ne pas supprimer le volume Dovecot et ne pas recréer le compte LDAP.

## 2. Diagnostic

1. Faire fermer Roundcube et les clients IMAP.
2. Noter le compte, l'heure et l'action réalisée.
3. Vérifier l'authentification et les dossiers :

```bash
cd ~/on-premise/messaging-compose
docker compose exec dovecot doveadm auth test utilisateur@embedded.local
docker compose exec dovecot doveadm mailbox list -u utilisateur@embedded.local
```

4. Consulter les journaux :

```bash
docker compose logs --since=2h dovecot
docker compose logs --since=2h roundcube
docker compose logs --since=2h postfix
```

Rechercher `DELETE`, `EXPUNGE`, `mailbox`, `INBOX` et l'identifiant du compte.

5. Contrôler le volume sans le supprimer :

```bash
docker volume inspect messaging-compose_dovecot_mail
docker compose exec dovecot find /var/mail/vhosts -maxdepth 4 -type d
```

## 3. Solution retenue

Restaurer uniquement le Maildir du compte concerné depuis la dernière
sauvegarde ou le dernier snapshot :

1. conserver le volume actuel comme copie de preuve ;
2. restaurer la sauvegarde dans un volume temporaire ;
3. recopier uniquement les messages d'Inbox ;
4. ne pas écraser `Sent`, `Drafts` ou `Trash` ;
5. corriger les permissions ;
6. reconstruire les index :

```bash
docker compose exec dovecot doveadm force-resync -u \
  utilisateur@embedded.local INBOX
docker compose exec dovecot doveadm mailbox status -u \
  utilisateur@embedded.local messages INBOX
```

Sans sauvegarde, snapshot ou corbeille IMAP, la récupération n'est pas
garantie. Ne jamais tenter une récupération directement sur le seul volume
actif.

## 4. Vérification finale

- l'utilisateur peut s'authentifier ;
- `Inbox` est visible dans Roundcube ;
- les messages restaurés sont consultables ;
- les autres dossiers n'ont pas été modifiés ;
- un nouveau message est livré dans `Inbox` ;
- l'incident est consigné dans le journal technique.

