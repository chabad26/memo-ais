# Glossaire Réseaux sécurisés - Itération 5

## Sujet

Réponse à incident, sécurisation Spark, Fail2ban et script de bannissement.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Réponse à incident | Démarche structurée pour détecter, qualifier, contenir, corriger et capitaliser. |
| ISO 27035 | Référence méthodologique pour la gestion d'incident de sécurité. |
| Spark Web UI | Interface d'administration Spark, sensible si exposée sans contrôle. |
| Exposition | Service accessible depuis un réseau où il ne devrait pas l'être. |
| Fail2ban | Outil qui bannit automatiquement des IP selon des motifs de logs. |
| Jail | Configuration Fail2ban associant filtre, log et action. |
| Filtre | Expression qui détecte un événement dans les logs. |
| Bannissement | Blocage temporaire ou permanent d'une adresse IP. |

## Manipulations faites

| Manipulation | Commandes ou actions |
| --- | --- |
| Analyser Spark | Identifier port exposé, interface, risque et remédiation. |
| Réduire l'exposition | Bind local, firewall, arrêt du service ou filtrage. |
| Installer Fail2ban | Jail SSH, filtre, statut et logs. |
| Tester le bannissement | Tentatives contrôlées, `fail2ban-client status`. |
| Ecrire un script | Ban/unban/list, validation IP, traces. |

## Docs associées

- [Vue d'ensemble](../../../admin-reseaux-securisation/it-5/index.md)
- [Réponse à incident et sécurisation d'une installation Spark](../../../admin-reseaux-securisation/it-5/atelier1.md)
- [Fail2ban SSH et script de bannissement IP](../../../admin-reseaux-securisation/it-5/atelier2.md)

