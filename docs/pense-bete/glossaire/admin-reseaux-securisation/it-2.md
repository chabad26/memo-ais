# Glossaire Réseaux sécurisés - Itération 2

## Sujet

Déploiement pfSense, règles de filtrage, ACL et journalisation.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| pfSense | Distribution pare-feu basée sur FreeBSD. |
| Interface firewall | Zone réseau traitée séparément dans pfSense. |
| Règle firewall | Condition actionnant un passage ou blocage de flux. |
| `Pass` | Action qui autorise un flux. |
| `Block` | Action qui bloque silencieusement ou journalise selon configuration. |
| Journalisation | Enregistrement des décisions firewall. |
| Alias | Objet pfSense réutilisable pour IP, réseau ou port. |
| Cloisonnement | Séparation contrôlée des zones réseau. |

## Manipulations faites

| Manipulation | Commandes ou actions |
| --- | --- |
| Déployer pfSense | Interfaces, adressage, passerelles des VLANs. |
| Créer des règles | ADMIN vers PROD, blocages PROD/RH vers ADMIN. |
| Tester les flux | `ping`, `ssh`, `curl`, `nmap`. |
| Lire les logs | Logs pfSense, décision pass/block, source/destination/port. |
| Produire une synthèse | Tableau règles, justification, résultats. |

## Docs associées

- [Vue d'ensemble](../../../admin-reseaux-securisation/it-2/index.md)
- [Déploiement de pfSense](../../../admin-reseaux-securisation/it-2/atelier1.md)
- [Règles de filtrage et ACL avec pfSense](../../../admin-reseaux-securisation/it-2/atelier2.md)
- [Journalisation et analyse des logs pfSense](../../../admin-reseaux-securisation/it-2/atelier3.md)
- [Synthèse pfSense](../../../admin-reseaux-securisation/it-2/synthese-pfsense.md)

