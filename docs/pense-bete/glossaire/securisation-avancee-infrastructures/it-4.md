# Pense-bête — Sécurisation avancée : Wazuh en collectif

## Périmètre

Itération 4 de la progression prévisionnelle du module. Cette fiche prépare
les notions et les gestes ; les résultats seront ajoutés après les activités.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Agent Wazuh | Composant installé sur une machine pour collecter des informations et événements. |
| Serveur Wazuh | Composant central qui analyse les événements reçus. |
| Indexer | Composant de stockage et de recherche des données indexées. |
| Dashboard | Interface de consultation et d'exploration des résultats. |
| Décodeur | Mécanisme qui extrait les champs d'un événement pour l'analyse. |
| Corrélation | Rapprochement d'événements selon le temps, l'actif et d'autres éléments pertinents. |
| SID Suricata / règle Wazuh | Deux identifiants différents à conserver lors du suivi d'une alerte. |

## Manipulations faites

Aucune manipulation de cette itération n'est encore documentée. La préparation
de la fiche ne constitue pas une preuve d'audit, de déploiement ou de test.

## Gestes et commandes à retenir

- Associer chaque machine et agent au bon apprenant ou groupe.
- Configurer la lecture EVE sur l'agent qui a accès au journal Suricata.
- Produire un événement neuf et le retrouver de la source au dashboard.
- Commencer par le filtre `rule.groups:suricata`, puis préciser période et agent.
- Vérifier aussi la collecte après rotation des journaux et redémarrage.

## Preuves attendues

Événement suivi de bout en bout, recherche reproductible et contributions attribuées.

## Docs associées

- [Feuille de l'itération 4](../../../securisation-avancee-infrastructures/it-4/index.md)
- [Dossier de preuves](../../../securisation-avancee-infrastructures/dossier-preuves.md)
- [Vue d'ensemble du module](../../../securisation-avancee-infrastructures/README.md)
