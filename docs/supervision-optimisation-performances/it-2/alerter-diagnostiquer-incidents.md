# Mise en situation — Alerter et diagnostiquer les incidents

## Situation professionnelle

Vous poursuivez votre mission au sein de l’équipe Infrastructure d’AlpesNet.

L’équipe dispose désormais d’une plateforme d’observabilité fonctionnelle. Les dashboards permettent de visualiser les métriques, les sondes vérifient certains services et les journaux sont centralisés dans ELK.

Mais les administrateurs ne peuvent pas surveiller les dashboards en permanence. Une anomalie peut donc rester invisible jusqu’à ce qu’un utilisateur signale un problème.

Le responsable Infrastructure demande de mettre en place un mécanisme permettant de :

- détecter automatiquement les situations anormales ;
- distinguer les niveaux de criticité ;
- prévenir les personnes concernées ;
- indiquer quoi faire lorsqu’une alerte apparaît ;
- utiliser ensuite les données d’observabilité pour rechercher la cause de l’incident.

## Problématique

**Comment transformer les données de supervision en alertes réellement exploitables, puis utiliser ces informations pour diagnostiquer un incident ?**

## Réutilisation obligatoire de l’itération 1

Réutiliser la plateforme et les dashboards existants. Il n’est pas demandé de redéployer un nouveau laboratoire.

| Élément existant | Rôle dans l’itération 2 |
| --- | --- |
| Laptop et virt-manager | Hébergement des VM du laboratoire |
| VM supervision — `192.168.122.80` | Prometheus, Grafana, Blackbox Exporter et ELK |
| Endpoint Debian — `192.168.122.158` | Métriques Linux, service HTTP et journaux journald |
| Endpoint Windows Server Core — `192.168.122.25` | Métriques Windows, service IIS et événements Windows |
| [Dashboard Grafana](../it-1/construire-dashboard-grafana.md) | Examiner les états, ressources, durées et évolutions |
| [Dashboard Kibana](../it-1/construire-dashboard-kibana.md) | Rechercher les événements, leur origine et leur contexte |
| [Sondes HTTP](../it-1/creer-configurer-sondes.md) | Vérifier le fonctionnement des services depuis la supervision |
| [Collecte des journaux](../it-1/ajouter-source-logs.md) | Conserver les éléments utiles au diagnostic |

Ces adresses correspondent aux réservations DHCP documentées dans le lab. Vérifier l’accessibilité et la fraîcheur des données à la reprise : un dashboard contenant l’historique de la veille ne prouve pas la collecte du jour.

## Démarche attendue

1. Identifier les situations qui justifient une intervention.
2. Relier chaque situation à une donnée disponible et à un impact possible.
3. Définir une condition, une durée, une criticité et un destinataire.
4. Configurer et tester les règles et notifications dans les activités suivantes.
5. Préparer une procédure de première réponse et de retour au nominal.
6. Corréler métriques, sondes et journaux pour expliquer un incident.

La criticité dépend de l’impact, de l’urgence et du service concerné. Le déclenchement d’une règle, l’envoi d’une notification et sa réception sont des étapes distinctes, à vérifier séparément.

!!! note "État de cette nouvelle itération"
    Cette fiche expose la mission. Elle ne déclare aucune nouvelle règle configurée, notification reçue ou cause d’incident démontrée. Les captures de l’itération 1 servent de point de départ et seront complétées par des preuves datées des nouveaux essais.

## Dossier de déploiement et de configuration

Conserver pour chaque alerte : situation, source, requête, seuil, durée, périmètre, criticité justifiée, responsable et première action. Ajouter ensuite la configuration réellement appliquée, les essais de déclenchement et de retour au nominal, la preuve de réception et les résultats du diagnostic.

Distinguer une proposition, une configuration appliquée et un résultat vérifié. Ne pas publier de secrets de notification dans les captures ou le dépôt.

[Commencer : identifier les situations nécessitant une alerte](identifier-situations-alerte.md) · [Sommaire de l’itération](index.md)
