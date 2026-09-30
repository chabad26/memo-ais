# Itération 4 — Centraliser avec Wazuh, collectivement

## Objectif

Construire une chaîne de collecte collective et retrouver dans Wazuh les
événements du serveur étudié et ceux produits par Suricata.

**Statut : activité préparatoire, à réaliser collectivement.** La réussite
individuelle de la détection Suricata doit être vérifiée avant l'intégration.

## Répartir les fonctions

| Composant | Fonction dans le laboratoire |
| --- | --- |
| Agent sur la machine portant Suricata | Lire le journal EVE JSON et transmettre les événements |
| Agent sur le serveur applicatif, si machine distincte | Collecter les sources système et applicatives sélectionnées |
| Serveur Wazuh | Analyser les événements avec les décodeurs et règles |
| Indexer | Stocker et rendre recherchables les données indexées |
| Dashboard | Rechercher les alertes et présenter les résultats |

L'hébergement et les flux seront renseignés dans le cadrage collectif.
Les rôles des composants sont décrits dans
l'[architecture officielle Wazuh](https://documentation.wazuh.com/current/getting-started/architecture.html).

## Travail à réaliser

1. Désigner les responsables de la plateforme, de l'enrôlement et des tests.
2. Documenter les versions, les composants, les accès et les flux nécessaires.
3. Enrôler les agents avec des identifiants permettant de retrouver leur machine
   et leur apprenant. Protéger les clés d'enrôlement.
4. Raccorder une source système/applicative utile et le fichier EVE de Suricata.
5. Vérifier que l'agent peut lire le fichier, y compris après rotation des logs.
6. Produire un nouvel événement de test et noter heure, source, destination et SID.
7. Retrouver cet événement localement, puis dans Wazuh avec le bon agent.
8. Documenter le décodage, la règle Wazuh, le délai de collecte et les limites.
9. Croiser une alerte réseau avec un événement hôte ou applicatif pertinent,
   en distinguant la corrélation réalisée par l'analyste d'une règle automatique.

## Préparer la collecte Suricata

Exemple à intégrer, après sauvegarde, dans la configuration existante de l'agent
qui a accès au fichier EVE ; adapter le chemin réel :

```xml
<localfile>
  <log_format>json</log_format>
  <location>/var/log/suricata/eve.json</location>
</localfile>
```

Ce bloc appartient à la configuration `ossec_config` de l'agent. Il ne remplace
pas le fichier complet. Vérifier les permissions nécessaires et les erreurs de
configuration avant de tester la collecte. La documentation fournit cette
[intégration Suricata/Wazuh](https://documentation.wazuh.com/current/proof-of-concept-guide/integrate-network-ids-suricata.html).

Pour rechercher les alertes Suricata, commencer par le groupe `rule.groups:suricata`,
puis limiter la période et l'agent. Examiner l'événement effectivement indexé
avant de choisir les champs complémentaires. Le SID Suricata et l'identifiant
de règle Wazuh sont deux références différentes à conserver.

## Vérifier la chaîne complète

| Étape | Question | Preuve attendue |
| --- | --- | --- |
| Source | Suricata a-t-il produit l'alerte attendue ? | Événement EVE local |
| Lecture | Le bon agent lit-il le bon fichier ? | Configuration, droits et diagnostics de collecte |
| Transmission | L'agent est-il relié au serveur ? | État de connexion et absence d'erreur bloquante |
| Analyse | L'événement est-il décodé et associé à une règle ? | Alerte Wazuh et champs reconnus |
| Recherche | Le résultat est-il retrouvé sur la bonne période ? | Filtre, agent, heure et événement consultable |
| Continuité | La collecte reste-t-elle fonctionnelle après redémarrage/rotation ? | Nouvel événement de test reçu |

Un agent connecté ne prouve pas la collecte de chaque source. Un dashboard
accessible ne prouve pas qu'un événement de test a traversé la chaîne.

## État final attendu et preuves L4

Un événement identifiable est suivi de Suricata jusqu'à Wazuh. Une recherche
documentée rapproche les événements réseau et hôte utiles à la qualification.
Le dossier collectif attribue les configurations, les tests et les conclusions
aux personnes qui les ont réalisés.

Conserver les extraits de configuration sans clé, la matrice machine/agent,
les filtres et les événements anonymisés. La réponse automatique reste une
fonction distincte ; aucun blocage n'est déduit de la simple centralisation.

- [Pense-bête de l'itération](../../pense-bete/glossaire/securisation-avancee-infrastructures/it-4.md)
- [Étape suivante — Traitement d'incident](../it-5/index.md)
- [Retour au module](../README.md)
