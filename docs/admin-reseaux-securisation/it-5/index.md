# Réponse à incident et automatisation sécurité

## Contexte de l'itération

Une machine Linux utilisée pour l'analyse de données présente un comportement anormal :

- forte lenteur ;
- charge CPU élevée ;
- services qui répondent difficilement ;
- installation Spark proche des valeurs par défaut.

L'objectif de cette itération est d'analyser une installation Spark insuffisamment sécurisée, d'identifier les risques, puis d'appliquer une démarche de remédiation inspirée des recommandations ANSSI.

## Ateliers

| Atelier | Sujet | Objectif |
| --- | --- | --- |
| Atelier 1 | Réponse à incident et sécurisation d'une installation Spark | Identifier les faiblesses, reproduire une exposition contrôlée, durcir Spark et documenter l'incident |
| Atelier 2 | Fail2ban SSH et script de bannissement IP | Protéger SSH contre les tentatives incorrectes et automatiser un bannissement IP avec nftables |

## Ressources

- Spark Security Documentation : <https://spark.apache.org/docs/latest/security.html>
- Spark Standalone Mode : <https://spark.apache.org/docs/latest/spark-standalone.html>
- ANSSI — Cyberattaques et remédiation : <https://messervices.cyber.gouv.fr/guides/cyberattaques-et-remediation-les-cles-de-decision>
- Fail2ban Documentation : <https://www.fail2ban.org/wiki/>
- nftables Wiki : <https://wiki.nftables.org/>
