# Déploiement du socle on-premise sur OVHcloud


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/cloud-migration-deployment.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Objectif

Reproduire le socle `on-premise` sur trois VM OVHcloud et vérifier les
communications entre les hôtes. Cette cible est une préparation de déploiement
: elle ne doit pas être considérée comme réalisée tant que les commandes et
les tests réseau n'ont pas été exécutés sur les VM.

## Répartition cible

| VM | Flavor | IP publique | IP privée | Services principaux |
| --- | --- | --- | --- | --- |
| `dist01b-ovh` | `d2-4` | `135.125.57.223` | `10.42.10.123` | OpenLDAP, LAM, Elasticsearch, Kibana, Filebeat |
| `files-ovh` | `d2-2` | `51.83.112.41` | `10.42.10.42` | Samba LDAP, WordPress et MariaDB |
| `mail-ovh` | `d2-2` | `54.36.253.197` | `10.42.10.139` | Postfix, Dovecot, Roundcube, MariaDB, sauvegarde |

Les deux VM `d2-2` avaient été supprimées pendant la phase de réduction des
coûts. Elles ont été recréées par OpenTofu avant ce déploiement et leurs
adresses privées sont reportées dans l'inventaire Ansible.

## Réseau inter-hôtes

Les réseaux Docker `openldap_default`, `mail_default` et `monitoring` ne sont
pas des réseaux multi-hôtes. Un réseau Docker créé sur une VM n'est donc pas
visible directement depuis une autre VM.

Les communications inter-hôtes utilisent le réseau privé OVH :

| Flux | Destination | Usage |
| --- | --- | --- |
| TCP 389/636 | VM annuaire | LDAP et LDAPS depuis Samba et la messagerie |
| TCP 139/445 | VM fichiers | Accès SMB depuis les clients autorisés |
| TCP 25/587/143/993 | VM messagerie | SMTP, submission et IMAP |
| TCP 8081/8082/5601 | Selon besoin | Interfaces Web de laboratoire |
| ICMP | Toutes les VM | Diagnostic réseau |

Ansible autorise les flux du CIDR privé `10.42.10.0/24`. Les services publiés
sur Internet doivent rester limités aux ports nécessaires et ne doivent pas
être confondus avec les communications privées.

## Adaptations obligatoires des Compose

Avant le démarrage multi-hôte :

1. remplacer les noms Docker distants comme `openldap` ou
   `ldap.embedded.local` par l'IP privée ou un nom résolu localement ;
2. conserver les noms de service Docker uniquement pour les conteneurs du même
   Compose ;
3. publier LDAP sur la VM annuaire et utiliser ce point d'accès depuis Samba et
   la messagerie ;
4. ne pas déclarer `external: true` en pensant créer un réseau partagé entre
   les VM ;
5. modifier Filebeat pour collecter les journaux nécessaires sur chaque hôte
   ou envoyer les événements vers la supervision centrale ;
6. adapter la sauvegarde, car `backup.sh` actuel voit les volumes Docker de
   son propre hôte uniquement.

Les fichiers `.env` et les clés privées restent locaux. Utiliser des variables
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]

## Ordre de déploiement

```text
OpenTofu : réseau, clé SSH et trois VM
    -> Ansible : Docker, UFW et réseau privé
        -> OpenLDAP + LAM
            -> Samba et WordPress
            -> Postfix, Dovecot, Roundcube
        -> Elasticsearch, Kibana et Filebeat
        -> sauvegardes
```

Chaque étape doit être validée avant de passer à la suivante. En particulier,
LDAP doit répondre depuis les deux VM dépendantes avant de démarrer Samba et la
messagerie.

## Vérifications minimales

Depuis chaque hôte :

```bash
ping -c 2 IP_PRIVEE_DES_AUTRES_VM
nc -vz IP_PRIVEE_LDAP 389
nc -vz IP_PRIVEE_LDAP 636
```

Depuis la VM messagerie :

```bash
openssl s_client -connect IP_PRIVEE_LDAP:636 -servername ldap.embedded.local
```

Depuis la VM fichiers :

```bash
nc -vz IP_PRIVEE_SAMBA 445
```

Puis vérifier les services :

```bash
docker compose ps
docker compose logs --tail=100 <service>
```

Un service “démarré” ne suffit pas : la preuve doit montrer la communication
avec sa dépendance, l'authentification LDAP, la réponse Web ou le flux réseau
attendu.

## Accès à la supervision

Elasticsearch et Kibana restent liés à `127.0.0.1` sur `dist01b-ovh`. Ils ne
sont donc pas exposés directement sur Internet. Depuis le poste
d'administration :

```bash
ssh -L 5601:127.0.0.1:5601 ubuntu@135.125.57.223
```

Ouvrir ensuite `http://127.0.0.1:5601`. Pour l'API Elasticsearch, créer un
second tunnel avec `-L 9200:127.0.0.1:9200`.

## État

| Point | Statut |
| --- | --- |
| VM principale `d2-4` | Réalisée |
| Deux VM `d2-2` | Créées par OpenTofu ; fichiers `10.42.10.42`, mail `10.42.10.139` |
| Réseau privé OVH | Validé entre les trois VM, 0 % de perte |
| Socle Ansible | Réalisé sur les trois VM ; seconde exécution sans changement |
| Adaptation des Compose au multi-hôte | Réalisée par le playbook OVH et overrides distants |
| Déploiement des services | Stacks démarrées sur les trois VM |
| Tests de communication inter-hôtes | Réalisés : ping entre les trois VM, 0 % de perte |
| Tests LDAP privés | Réalisés depuis les VM fichiers et mail sur `389/636` |
| Tests SMB et IMAP/IMAPS | Réalisés depuis le poste d'administration |
| Test SMTP entrant `25` | À poursuivre : délai observé malgré les autres flux mail actifs |
