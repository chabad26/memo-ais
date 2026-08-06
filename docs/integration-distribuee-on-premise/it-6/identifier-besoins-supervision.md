# Identifier les besoins de supervision

## Objectif

Recenser les journaux et événements nécessaires pour suivre la disponibilité,
la sécurité et les performances de l'infrastructure, sans déployer de nouvel
outil pendant cette activité.

## Périmètre analysé

L'infrastructure repose principalement sur des conteneurs Docker. Les sorties
standard et d'erreur de chaque service sont donc une première source commune,
consultable avec `docker logs`. Les fichiers internes restent utiles lorsqu'un
service produit un journal plus détaillé ou séparé par client.

`step-ca` n'est pas encore déployé dans l'infrastructure actuelle. Ses besoins
de supervision sont préparés pour sa future intégration ; aucune collecte
step-ca n'est présentée comme déjà opérationnelle.

## Journaux et informations attendues

| Service | Journaux ou sources à collecter | Événements importants | Informations utiles au diagnostic |
|---|---|---|---|
| OpenLDAP | `docker logs openldap` ; journal `slapd` ou syslog si activé | démarrage/arrêt, échecs de bind, erreurs de base ou de schéma, modifications sensibles, indisponibilité LDAP | date, IP cliente, type d'opération, DN concerné à protéger, code LDAP (`0`, `32`, `49`, `50`), durée de réponse |
| Samba | `docker logs samba-ldap` ; `/var/log/samba/log.smbd` ; `/var/log/samba/log.<client>` | arrêt ou redémarrage, erreur LDAP, authentification refusée, accès interdit, échec de lecture/écriture, saturation d'un partage | utilisateur, groupe, partage, client, code NTSTATUS, fichier concerné, espace disponible, rôle Samba chargé |
| Postfix | `docker logs mail-postfix` ; `/var/log/mail.log` si activé ; file `postqueue -p` | message envoyé, différé ou rejeté, erreur DNS, relais refusé, échec SASL/TLS, croissance de la file | identifiant de file, expéditeur/destinataire à pseudonymiser, relais, délai, statut SMTP, cause du rejet |
| Dovecot | `docker logs mail-dovecot` ; journaux Dovecot dédiés si configurés | échec d'authentification, ouverture/fermeture IMAP, livraison LMTP, quota dépassé, erreur Maildir ou index, erreur TLS | compte, IP cliente, protocole, boîte concernée, durée de session, volume occupé, code d'erreur |
| Roundcube | `docker logs mail-roundcube` ; journaux Apache/PHP ; journal d'erreurs Roundcube si activé | échec de connexion, erreur PHP, indisponibilité IMAP/SMTP, erreur MariaDB, réponses HTTP 4xx/5xx | utilisateur sans mot de passe, URL, code HTTP, exception, serveur joint, temps de réponse, identifiant de session pseudonymisé |
| MariaDB messagerie | `docker logs mail-db` ; journal d'erreurs MariaDB | arrêt, échec de connexion, requête lente, verrouillage, corruption, espace disque faible | base, compte technique, durée, code SQL, connexions actives, taille des données, état InnoDB |
| step-ca (prévu) | `docker logs step-ca` ; journal JSON de l'autorité lorsqu'il sera activé | émission, renouvellement ou révocation, échec d'autorisation, certificat proche de l'expiration, erreur de base ou de provisioner | numéro de série, sujet, SAN, provisioner, date d'expiration, résultat, adresse cliente ; ne jamais journaliser une clé privée |
| BorgBackup | `backup/logs/backup-*.log` ; `cron.log` ; `daily-check.log` ; `last-run.status` | échec ou absence de sauvegarde, archive trop ancienne, verrou, erreur d'intégrité, échec de prune/compact, dépôt inaccessible | archive, heure, durée, code retour, tailles originale/compressée/dédupliquée, nombre de fichiers, âge de la dernière archive |
| Docker | `journalctl -u docker` ; `docker events` ; `docker logs <conteneur>` ; santé et état via `docker inspect` | création/suppression, redémarrages répétés, conteneur unhealthy, OOM, image introuvable, erreur réseau/volume, espace Docker faible | conteneur, image et tag, exit code, restart count, healthcheck, consommation CPU/RAM, montage, réseau, espace disque |
| LDAP Account Manager | `docker logs lam` ; journaux Apache/PHP du conteneur | indisponibilité Web, échec de connexion LDAP, erreur PHP, modification impossible | code HTTP, serveur LDAP, profil LAM, exception, temps de réponse ; ne pas conserver les mots de passe saisis |
| WordPress | `docker logs` des services WordPress/MariaDB ; journaux Web/PHP | erreur HTTP, échec de connexion SQL, erreur d'extension, espace disque faible | URL, code HTTP, exception, base concernée, latence, version applicative |

## Indicateurs prioritaires

Les journaux seuls ne suffisent pas. La supervision devra également produire
des indicateurs mesurables :

| Domaine | Indicateur | Seuil initial proposé |
|---|---|---|
| Disponibilité | état du conteneur et résultat du healthcheck | alerte immédiate si arrêté ou `unhealthy` |
| Stabilité | nombre de redémarrages | alerte si plus de 3 en 10 minutes |
| Authentification | taux d'échecs LDAP, Samba, SMTP ou IMAP | alerte sur hausse brutale ou répétition depuis une même source |
| Messagerie | messages différés dans la file Postfix | alerte si la file augmente pendant 15 minutes |
| Sauvegarde | âge de la dernière archive Borg | erreur au-delà de 36 heures |
| Capacité | espace des volumes et de l'hôte Docker | avertissement à 80 %, critique à 90 % |
| Certificats | jours avant expiration | avertissement à 30 jours, critique à 7 jours |
| Performance | latence LDAP, IMAP, Web et base | établir d'abord une valeur normale, puis alerter sur dérive |

Ces seuils sont des valeurs de départ. Ils devront être ajustés après une
période d'observation pour éviter les faux positifs.

## Commandes utiles au diagnostic

```bash
# Vue générale et redémarrages
docker ps -a
docker inspect <conteneur> \
  --format 'status={{.State.Status}} exit={{.State.ExitCode}} restart={{.RestartCount}}'

# Journaux récents avec horodatage
docker logs --since 30m --timestamps <conteneur>

# Événements Docker récents
docker events --since 30m

# Consommation instantanée
docker stats --no-stream
docker system df

# Messagerie et sauvegarde
docker exec mail-postfix postqueue -p
~/on-premise/backup/check-backup.sh
```

Les commandes de diagnostic doivent être lancées en lecture seule lorsque cela
est possible. Une collecte ne doit jamais afficher les fichiers `.env`, les
mots de passe, les clés privées, les jetons ou le contenu complet des messages.

## Organisation proposée de la collecte

1. conserver les sorties des conteneurs avec le pilote de journalisation
   Docker et une rotation limitée en taille ;
2. collecter les fichiers applicatifs nécessaires dans des volumes dédiés en
   lecture seule ;
3. centraliser les événements avec l'heure, le service, le niveau et l'hôte ;
4. définir une durée de conservation adaptée au diagnostic et aux obligations
   de l'entreprise ;
5. restreindre l'accès aux journaux contenant des identifiants ou des adresses ;
6. relier chaque alerte à une procédure de diagnostic et d'escalade.

## Priorités de mise en œuvre

1. disponibilité des conteneurs et redémarrages répétés ;
2. échecs d'authentification OpenLDAP, Samba et messagerie ;
3. âge et résultat des sauvegardes Borg ;
4. file Postfix, stockage Dovecot et espace des volumes ;
5. erreurs applicatives Roundcube et LAM ;
6. expiration des certificats lors du déploiement de step-ca.

## Livrable

Le tableau recense pour chaque service les journaux à collecter, les événements
à surveiller et les informations attendues pour diagnostiquer un incident.

## Notions acquises

- journal applicatif ;
- événement ;
- indicateur ;
- seuil d'alerte ;
- rétention des journaux ;
- diagnostic ;
- protection des données de journalisation.
