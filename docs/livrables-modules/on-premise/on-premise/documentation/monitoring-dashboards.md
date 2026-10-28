# Tableaux de bord de supervision


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/on-premise/documentation/monitoring-dashboards.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Le statut proposé, simulé ou observé indiqué par l’auteur est conservé.


## Tableaux créés

| Tableau de bord | Filtre principal | Objectif d'exploitation |
|---|---|---|
| Supervision - Messagerie | `container.name: ("mail-postfix" OR "mail-dovecot" OR "mail-roundcube")` | suivre l'activité et rechercher les erreurs SMTP/IMAP |
| Supervision - Authentifications LDAP | `container.name: "openldap" AND message: (BIND OR RESULT)` | contrôler les connexions et les erreurs LDAP |
| Supervision - Sauvegardes BorgBackup | `service.name: "borgbackup"` | vérifier l'exécution et le résultat des sauvegardes |
| Supervision - Redémarrages des conteneurs | messages de démarrage, arrêt ou signal | repérer les services instables |
| Supervision - Certificats (préparation) | termes TLS, X.509 et `step-ca` | préparer le suivi des certificats |

Les tableaux utilisent la vue `logs-infrastructure*`, le champ temporel
`@timestamp` et une période enregistrée de sept jours.

## Filtres de diagnostic

```text
container.name: "mail-postfix" AND message: (error OR warning OR failed OR reject*)
container.name: "openldap" AND message: "err=49"
service.name: "borgbackup" AND message: (ERROR OR failed OR échec)
message: ("starting" OR "started" OR "Killed with signal")
container.name: "step-ca" AND message: (issued OR renewed OR revoked OR expired OR error)
```

Le tableau des redémarrages repose sur les messages applicatifs. Une mesure
exacte du compteur de redémarrages nécessiterait une source de métriques ou
d'événements Docker supplémentaire.

Le tableau des certificats est préparé avant l'arrivée de `step-ca`. Les
événements actuels sont des mentions TLS génériques et ne valident pas encore
la supervision de l'autorité de certification.

## Export et restauration

L'export versionné se trouve dans
`monitoring-compose/kibana/dashboards.ndjson`.

```bash
cd ~/on-premise/monitoring-compose

curl -X POST 'http://127.0.0.1:5601/api/saved_objects/_import?overwrite=true' \
  -H 'kbn-xsrf: true' \
  --form file=@kibana/dashboards.ndjson
```

Vérification :

```bash
curl -s 'http://127.0.0.1:5601/api/saved_objects/_find?type=dashboard&per_page=100' \
  -H 'kbn-xsrf: true' |
  jq -r '.saved_objects[] | .attributes.title'
```

Résultat du 7 août 2026 : cinq tableaux de bord présents dans Kibana.
