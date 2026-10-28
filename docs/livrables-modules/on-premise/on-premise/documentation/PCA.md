# Plan de Continuité d'Activité - état du projet


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/PCA.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


## Services couverts

Le périmètre de l'itération comprend les services Docker suivants :

- WordPress et MariaDB pour l'application Web et ses données persistantes ;
- OpenLDAP pour l'annuaire et les futures authentifications centralisées ;
- LDAP Account Manager pour l'administration Web d'OpenLDAP ;
- Samba et les espaces de partage de l'entreprise ;
- Postfix, Dovecot, Roundcube et MariaDB pour la messagerie interne ;
- Campus CA, les certificats de service et la racine publique utilisée par les
  clients internes ;
- Elasticsearch, Kibana et Filebeat pour la centralisation des journaux et les
  tableaux de bord d'exploitation.

## Mesures de continuité

- conserver les fichiers Compose dans Git ;
- conserver les volumes MariaDB et LDAP sur un stockage sauvegardé ;
- protéger les fichiers `.env` et ne versionner que les `.env.example` ;
- vérifier les conteneurs, les journaux et les ports après un redémarrage ;
- conserver une procédure LDAP en ligne de commande si LAM est indisponible ;
- maintenir une liste des utilisateurs et groupes dans `users.md` ;
- maintenir les procédures d'exploitation et le plan de validation dans
  `operations.md` et `validation.md` ;
- conserver le serveur Samba et son volume de partages dans le périmètre de
  continuité ;
- utiliser `infrastructure-compose/` pour redémarrer OpenLDAP et LAM dans un
  ordre documenté ;
- appliquer la stratégie définie dans `backup-strategy.md` ;
- conserver une copie chiffrée hors de l'hôte Docker principal ;
- vérifier les sauvegardes chaque jour et tester les restaurations chaque mois ;
- conserver le certificat racine public `pki/certs/Campus-CA-root.crt`, le
  registre des certificats et la procédure de renouvellement ;
- surveiller l'âge de la dernière sauvegarde, les redémarrages de conteneurs,
  les erreurs LDAP/messagerie et l'expiration des certificats depuis Kibana.

OpenLDAP est prioritaire pour les futures authentifications. LAM est un outil
d'administration secondaire : son indisponibilité ne doit pas empêcher les
contrôles LDAP directs.

## État vérifié

- WordPress est accessible sur le port local `8085` ;
- le volume `wordpress-compose_db_data` est conservé par `docker compose down` ;
- OpenLDAP utilise la base `dc=embedded,dc=local` et le port `389` ;
- LAM est accessible sur le port `8081` ;
- six utilisateurs et six groupes LDAP ont été vérifiés ;
- une recherche LDAP se termine par `result: 0 Success` ;
- LDAPS, IMAPS, SMTP STARTTLS et HTTPS Roundcube ont été validés le
  7 août 2026 avec la chaîne Campus CA ;
- Elasticsearch, Kibana, Filebeat et cinq tableaux de bord de supervision ont
  été validés les 6 et 7 août 2026.

## Points restant à tester

- démarrage complet d'un service OpenLDAP depuis les volumes restaurés ;
- reprise après perte du conteneur OpenLDAP ;
- fonctionnement dégradé des services dépendant de LDAP ;
- raccordement de la supervision à des alertes externes ;
- renouvellement automatique ou planifié des certificats courts de laboratoire ;
- respect réel des délais de reprise après restauration LDAP, Samba et
  messagerie ;
- reprise de Kibana/Filebeat depuis les volumes restaurés et réimport contrôlé
  des tableaux de bord.

Le scénario de corruption LDAP est analysé dans
`backup-strategy-validation.md`. Le temps de reprise est estimé à 1 h 20,
compatible avec les objectifs, mais doit encore être mesuré lors d'un exercice
complet.

## Sauvegardes

Les exigences sont documentées dans `backup-requirements.md`. La stratégie
3-2-1, les fréquences, la rétention et les tests sont définis dans
`backup-strategy.md`. Les sauvegardes ne seront déclarées opérationnelles
qu'après un test de restauration consigné dans le journal technique.

## Samba et espaces de partage

Le serveur Samba fournit les partages `Commun`, `Developpement`,
`Bureau-etudes` et `Administration`. Les droits reposent sur les groupes
OpenLDAP. En cas d'indisponibilité, les modifications de groupes sont
suspendues et les utilisateurs sont informés avant toute reprise.

## Certificats et supervision

Le certificat racine Campus CA est versionné car il est public. Les clés
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
certificats de service OpenLDAP, Postfix, Dovecot et Roundcube ont été validés
le 7 août 2026, mais leur durée courte impose un contrôle d'expiration et un
renouvellement avant tout exercice de reprise ultérieur.

La plateforme de supervision centralise les journaux Docker et BorgBackup dans
`logs-infrastructure*`. Elle contribue au PCA en donnant une preuve rapide de
disponibilité, d'erreurs d'authentification, de sauvegarde et de certificats.
Elle ne remplace pas encore une alerte externe.
