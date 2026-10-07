# Itération 8 — Première détection réseau avec Suricata

## Objectifs de la journée

Après audit, durcissement et rédaction de la PSSI V1, mettre en place un premier
IDS réseau sur **la machine hôte**, directement, sans installation dans la VM
ni dans un conteneur. Suricata observe le trafic visible depuis son interface
de capture et génère des événements/alertes ; une alerte ne prouve pas un incident.

```text
Réseau extérieur
       |
Machine hôte — Suricata (IDS)
       |
Réseau virtuel de la VM
       |
VM — File Browser (conteneur)
```

L’énoncé mentionne Ubuntu 20.04 ; le mémo rapporte une migration ultérieure.
Relever l’OS réel de la cible sans réinstaller ni revenir à 20.04 pour cet exercice.
Le schéma indique le point d’observation souhaité, pas une visibilité déjà prouvée :
identifier interface, réseau virtuel, NAT et trajet effectif des échanges.

## Parcours de la journée

- [Identifier le point d’observation — 45 min](identifier-point-observation.md)
- [Comprendre les événements produits](comprendre-evenements-produits.md)
- [Installer et tester des règles Suricata — 1 h 15](installer-tester-regles-suricata.md)
- [Observer l’activité autour de File Browser](observer-activite-file-browser.md)
- [Faire le bilan du dispositif de détection](bilan-dispositif-detection.md)
- [Pense-bête de l’itération](../../pense-bete/glossaire/securisation-avancee-infrastructures/it-8.md)

**État attendu :** trafic de la VM visible, règles lues et sélectionnées (10
maximum), configuration acceptée, événements retrouvés et analysés avec limites.
**État au 7 octobre :** Suricata 8.0.3 et quatre règles chargées vérifiés par
les sorties fournies ; correction `eth0` → `virbr0` et service actif documentés à 10 h 18.
Capture de 10 h 30 : trafic sur 18080 et quatre alertes EVE observés sur le
serveur temporaire ; aucune exploitation ni détection sur File Browser/8080
n’est démontrée par ces essais. Voir les captures dans la feuille de test.

- [V1 du fragment de PSSI conservée](../it-6/fragment-pssi-v1.md)
- [Retour au module](../README.md)
