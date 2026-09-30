# Itération 3 — Détecter avec Suricata, individuellement

## Objectif

Installer une détection réseau sur le laboratoire, configurer des règles et
prouver qu'elles réagissent au trafic attendu.

**Statut : activité préparatoire, à réaliser individuellement.** L'installation
et les règles seront adaptées à la version retenue et aux interfaces observées.

## Définir ce que la sonde voit

Compléter le [cadrage réseau](../cadrage-laboratoire.md#preparer-les-flux-et-la-visibilite)
avant les tests. Indiquer l'emplacement de Suricata, l'interface de capture,
le réseau protégé et le chemin du trafic entre le client et le serveur.

Suricata est d'abord utilisé ici en **IDS** : il observe et alerte. Un blocage
nécessiterait un déploiement IPS et une validation distincte. Ne pas attribuer
un blocage au seul déclenchement d'une alerte.

## Travail à réaliser

1. Choisir une version compatible avec le système et conserver sa référence.
2. Configurer l'interface et `HOME_NET` selon le laboratoire réel.
3. Activer la sortie EVE JSON et identifier son emplacement effectif.
4. Vérifier avec un trafic connu que la sonde reçoit les paquets utiles.
5. Charger les règles prévues, puis ajouter une règle locale de test identifiable.
6. Vérifier la configuration avant rechargement et noter les erreurs éventuelles.
7. Réaliser un test positif puis un test négatif pour la règle choisie.
8. Conserver les événements EVE, la règle, sa révision et les conditions de test.

La sortie EVE permet d'examiner les événements structurés de Suricata. Le
[guide officiel de démarrage](https://docs.suricata.io/en/suricata-7.0.15/quickstart.html)
illustre la capture et la lecture des alertes ; utiliser la documentation
correspondant à la version effectivement installée.

## Décrire une règle avant de l'écrire

| Élément | Question à documenter |
| --- | --- |
| Intention | Quel comportement du cas fil rouge veut-on détecter ? |
| Périmètre | Quel protocole, sens de circulation, réseau et service ? |
| Condition | Quel indicateur réellement observable déclenche la règle ? |
| Identifiant | Quel SID local disponible, quelle révision et quel message ? |
| Test positif | Quel trafic inoffensif de laboratoire doit déclencher cette règle ? |
| Test négatif | Quel trafic témoin doit passer sans déclencher cette règle précise ? |
| Limites | Quels faux positifs, angles morts ou effets du chiffrement ? |

Un marqueur de test valide le fonctionnement technique de la règle. Il ne
démontre pas la couverture de toutes les attaques sur l'application.

## Gestes à retenir après installation

Sur la machine portant la sonde, avec les chemins par défaut à vérifier :

```bash
suricata --build-info
sudo suricata -T -c /etc/suricata/suricata.yaml
sudo tail -n 100 /var/log/suricata/eve.json | jq 'select(.event_type == "alert")'
```

Ces commandes sont des contrôles prévus, non exécutés dans cette préparation.
Le test de configuration doit réussir avant application. Il ne prouve ni la
visibilité réseau ni la réception d'un événement réel. La lecture des cent
dernières lignes sert à une vérification rapide, pas à conclure à l'absence
d'alerte sur toute une période.

## Matrice de validation

| Test | Résultat attendu | Preuve à conserver |
| --- | --- | --- |
| Configuration | Règles et paramètres acceptés | Sortie du contrôle et version |
| Visibilité | Trafic de test observé sur la bonne interface | Compteurs ou capture limitée et horodatée |
| Positif | Alerte correspondant au SID attendu | Heure, SID, révision, source et destination |
| Négatif | Absence de cette alerte sur la fenêtre du test témoin | Trafic témoin observé et recherche sur la période |
| Redémarrage du service | Configuration et détection toujours présentes | Nouveau test positif après redémarrage |

## État final attendu et preuves L3

Une sonde dont la visibilité est expliquée, au moins une règle documentée et des
tests positif/négatif attribuables à l'apprenant. Conserver les limites, notamment
le trafic non visible et les contenus TLS inaccessibles à la sonde.

- [Pense-bête de l'itération](../../pense-bete/glossaire/securisation-avancee-infrastructures/it-3.md)
- [Étape suivante — Centralisation Wazuh](../it-4/index.md)
- [Retour au module](../README.md)
