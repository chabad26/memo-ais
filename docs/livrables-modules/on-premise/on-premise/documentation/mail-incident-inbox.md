# Incident messagerie : suppression de la boîte Inbox


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/mail-incident-inbox.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.


## Description

Un utilisateur a supprimé accidentellement sa boîte de réception IMAP. Les
messages ne sont plus visibles dans Roundcube ou dans son client IMAP, tandis
que l'authentification et les autres dossiers peuvent rester fonctionnels.

## Diagnostic

1. Faire fermer les clients IMAP et noter le compte ainsi que l'heure de
   l'incident.
2. Vérifier l'état des dossiers et l'authentification :

```bash
cd ~/on-premise/messaging-compose
docker compose exec dovecot doveadm auth test utilisateur@embedded.local
docker compose exec dovecot doveadm mailbox list -u utilisateur@embedded.local
```

3. Consulter les journaux et rechercher `DELETE`, `EXPUNGE`, `INBOX` et le
   compte concerné :

```bash
docker compose logs --since=2h dovecot
docker compose logs --since=2h roundcube
docker compose logs --since=2h postfix
```

4. Identifier le volume persistant sans le supprimer :

```bash
docker volume inspect messaging-compose_dovecot_mail
docker compose exec dovecot find /var/mail/vhosts -maxdepth 4 -type d
```

## Solution retenue

Restaurer uniquement le Maildir du compte concerné depuis la dernière
sauvegarde ou le dernier snapshot disponible :

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

Sans sauvegarde, snapshot ou mécanisme de corbeille IMAP, la récupération des
messages supprimés n'est pas garantie. Une récupération doit être tentée sur
une copie du volume, jamais directement sur le seul stockage actif.

## Vérification et traçabilité

- l'utilisateur peut s'authentifier ;
- `Inbox` est visible dans Roundcube ;
- les messages restaurés sont consultables ;
- les autres dossiers n'ont pas été modifiés ;
- un nouveau message est livré dans `Inbox`.

Conserver les journaux, la date de l'incident, le compte concerné, la
sauvegarde utilisée et les commandes exécutées. La fiche pédagogique associée
est `docs/integration-distribuee-on-premise/it-4/diagnostiquer-suppression-inbox.md`.

