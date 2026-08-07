# Analyser un incident avec les journaux centralisés

## Objectif

Utiliser Kibana pour retrouver l'origine probable d'un incident à partir des
journaux centralisés dans `logs-infrastructure*`.

L'analyse porte sur cinq signaux possibles :

- échec d'authentification LDAP ;
- erreur SMTP ;
- certificat invalide ;
- arrêt d'un conteneur ;
- échec d'une sauvegarde.

Le but n'est pas de regarder chaque service séparément, mais de corréler les
événements pour comprendre la chronologie complète.

## 1. Préparer la recherche dans Kibana

Dans Kibana :

1. ouvrir **Discover** ;
2. choisir la vue **Journaux infrastructure** ;
3. sélectionner la période de l'incident ;
4. afficher au minimum les champs `@timestamp`, `container.name`,
   `service.name`, `log_source` et `message` ;
5. trier les événements du plus ancien au plus récent.

Filtre large de départ :

```text
message: (failed OR error OR reject* OR invalid OR certificate OR TLS OR stopped OR exited OR échec OR "err=49")
```

Ce premier filtre sert à repérer les événements anormaux. Ensuite, chaque piste
est vérifiée avec un filtre plus précis.

## 2. Recherches réalisées

| Hypothèse | Filtre KQL utilisé | Journaux concernés |
|---|---|---|
| Échec d'authentification LDAP | `container.name: "openldap" AND message: ("err=49" OR invalid OR BIND)` | OpenLDAP |
| Erreur SMTP | `container.name: "mail-postfix" AND message: (error OR warning OR failed OR reject* OR SASL)` | Postfix |
| Problème d'authentification mail | `container.name: "mail-dovecot" AND message: (auth OR login OR failed)` | Dovecot |
| Certificat invalide | `message: (certificate OR certificat OR x509 OR TLS OR SSL) AND message: (invalid OR expired OR verify OR error)` | Services TLS, reverse proxy ou autorité de certification |
| Arrêt d'un conteneur | `message: ("exited" OR "stopped" OR "Killed with signal" OR "entered FATAL state")` | Journaux Docker collectés par Filebeat |
| Échec d'une sauvegarde | `service.name: "borgbackup" AND message: (ERROR OR failed OR échec OR "exit code")` | BorgBackup |

Pour élargir la recherche autour d'un événement précis, utiliser une fenêtre de
temps courte dans Kibana, par exemple cinq minutes avant et après l'erreur.

## 3. Chronologie de l'incident

| Heure | Source | Événement observé | Interprétation |
|---|---|---|---|
| 09:14 | `openldap` | plusieurs réponses LDAP avec `err=49` | Les identifiants envoyés à l'annuaire sont refusés. |
| 09:15 | `mail-dovecot` | échecs d'authentification utilisateur | Le service de messagerie ne parvient plus à valider les comptes. |
| 09:16 | `mail-postfix` | rejet SMTP lié à l'authentification | L'envoi de messages échoue parce que l'authentification dépend de LDAP. |
| 09:18 | journaux TLS | erreur de vérification de certificat | Une connexion sécurisée échoue ou un certificat n'est plus accepté. |
| 09:21 | journaux Docker | arrêt ou redémarrage d'un conteneur de service | Le service instable peut aggraver l'incident ou interrompre la collecte. |
| 09:30 | `borgbackup` | sauvegarde terminée en erreur | La sauvegarde ne peut pas confirmer un point de reprise sain après l'incident. |

La première anomalie significative est l'échec LDAP. Les erreurs SMTP et Dovecot
arrivent ensuite et semblent dépendre de cette authentification. L'erreur de
certificat doit être contrôlée, car elle peut expliquer une rupture de liaison
TLS entre services ou une configuration LDAPS incorrecte.

## 4. Cause probable

| Incident | Cause identifiée | Action proposée |
|---|---|---|
| Échec SMTP | Authentification LDAP impossible | Vérifier la disponibilité d'OpenLDAP, le DN de bind et le mot de passe utilisé par la messagerie. |
| Échec LDAP | Identifiants invalides ou compte de service modifié | Tester le bind LDAP avec le compte applicatif et contrôler les derniers changements de mot de passe. |
| Certificat invalide | Certificat expiré, mauvais nom DNS ou chaîne de confiance absente | Renouveler le certificat, vérifier le CN/SAN et déployer la CA sur les services clients. |
| Arrêt d'un conteneur | Crash applicatif, redémarrage manuel ou manque de ressources | Consulter les journaux juste avant l'arrêt, contrôler `docker compose ps` et limiter les redémarrages en boucle. |
| Échec de sauvegarde | Service indisponible ou dépôt Borg inaccessible pendant l'incident | Relancer la sauvegarde après correction, vérifier le code retour et tester une restauration. |

Conclusion retenue pour la présentation :

> L'incident semble commencer par un problème d'authentification LDAP. Les
> erreurs SMTP et Dovecot sont probablement des conséquences, car la messagerie
> dépend de l'annuaire pour valider les utilisateurs. Le certificat invalide et
> l'arrêt de conteneur doivent être vérifiés comme causes techniques possibles.
> La sauvegarde en échec augmente le risque, car elle empêche de prouver qu'un
> point de reprise récent est disponible.

## 5. Actions correctives à vérifier

| Action | Commande ou contrôle | Résultat attendu |
|---|---|---|
| Vérifier que les conteneurs sont actifs | `docker compose ps` | OpenLDAP, Postfix, Dovecot, Kibana, Elasticsearch et Filebeat sont `running` ou `healthy`. |
| Tester l'annuaire | `ldapsearch -x -H ldap://127.0.0.1:389 -D "cn=admin,dc=alpesnet,dc=local" -W -b "dc=alpesnet,dc=local"` | Le bind LDAP réussit. |
| Contrôler les journaux LDAP | `container.name: "openldap" AND message: (BIND OR RESULT)` | Les nouveaux tests retournent `err=0`. |
| Contrôler la messagerie | `container.name: "mail-postfix" AND message: (status=sent OR reject* OR failed)` | Les envois réussissent et les rejets disparaissent. |
| Contrôler le certificat | `openssl s_client -connect service:443 -servername service` | Le certificat présenté correspond au nom attendu et n'est pas expiré. |
| Relancer la sauvegarde | procédure BorgBackup du module sauvegarde | Le journal BorgBackup indique un succès et un code retour `0`. |

## 6. Livrable formateur

À présenter au formateur :

1. capture Kibana Discover avec le filtre large ;
2. capture Kibana ou extrait des événements LDAP ;
3. capture Kibana ou extrait des événements SMTP ;
4. chronologie triée par heure ;
5. tableau incident, cause identifiée et action proposée ;
6. vérification finale après correction.

## Résultat

L'analyse d'incident relie les événements applicatifs, conteneurs et sauvegardes
dans une même chronologie. La cause probable est un défaut d'authentification
LDAP, avec impacts sur la messagerie et risque supplémentaire sur la sauvegarde.
La correction prioritaire consiste à rétablir l'authentification LDAP, puis à
retester SMTP, les certificats et la sauvegarde.

## Termes à retenir

- **Corrélation** : croisement de plusieurs journaux pour comprendre un même incident.
- **Chronologie** : ordre des événements observés pendant l'incident.
- **Cause probable** : explication la plus cohérente avec les journaux disponibles.
- **Action corrective** : mesure appliquée pour supprimer la cause ou réduire le risque.
- **KQL** : langage de filtre utilisé dans Kibana.

## Ressources

- [Configurer la collecte centralisée avec Filebeat](configurer-collecte-filebeat.md)
- [Créer les tableaux de bord Kibana](creer-tableaux-bord-kibana.md)
- [Valider la stratégie de sauvegarde](../it-5/valider-strategie-sauvegarde.md)
