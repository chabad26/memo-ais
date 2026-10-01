# Itération 1 — Auditer et prioriser les constats

## Objectif

Construire un état initial du serveur exposé, croiser les résultats de plusieurs
outils et proposer un ordre de traitement justifié.

**Statut : environnement observé, deux scans Greenbone terminés et cinq constats
qualifiés.** Les rapports détaillés du 30 septembre 2026 prouvent la réussite du
scan SSH authentifié et documentent les résultats retenus. Les vérifications
locales se poursuivent dans l'[itération 2](../it-2/reprendre-constats-j1.md).

## Activités fournies par le formateur

- [Préparation de l'environnement et installation de Greenbone](preparer-cible-installer-greenbone.md) :
  hôte comme machine d'audit, VM Ubuntu Server 20.04 (2 vCPU, 4 Go), Docker,
  File Browser 2.15.0, accès sur le port 8080 et démarrage de Greenbone sur l'hôte.
- [Vulnérabilité ou autre problème ?](vulnerabilite-ou-autre-probleme.md) — **30 min** :
  quatre situations à classer et à justifier, avec les réponses de l'apprenant
  et les précisions apportées lors de la relecture.
- [Lire et analyser trois entrées CVE](lire-analyser-entrees-cve.md) :
  Debian OpenSSL, Heartbleed et Log4Shell ; entrées CVE.org, JSON, références,
  corrections et conséquences qui peuvent subsister après une mise à jour.
- [Comprendre CVSS](comprendre-cvss.md) — **30 min** : scores et vecteurs des
  trois CVE, lecture du vecteur Log4Shell et distinction entre sévérité et priorité.
- [Observer la cible](observer-cible.md) — **30 min** : commandes connues sur la
  VM et depuis l'hôte, inventaire des services et rôles, résultats prouvés et relevé à compléter.
- [Premier audit avec Greenbone](premier-audit-greenbone.md) — **2 h 15** :
  vérifier les feeds, réaliser les scans sans puis avec authentification SSH,
  comparer à l'inventaire et qualifier cinq résultats réels.

La fiche de préparation regroupe la procédure et les sept captures du laboratoire.
Les activités d'audit ci-dessous
seront menées ensuite sur **sa propre VM**, sans scanner les autres apprenants.

## Prérequis

- [Cadrage du laboratoire](../cadrage-laboratoire.md) complété : cible, application,
  responsabilités, périmètre et fenêtre d'audit.
- Accès réseau pour Greenbone et accès local autorisé pour Lynis.
- Artefact applicatif accessible pour Trivy : image de conteneur, dépôt ou
  répertoire adapté au déploiement réellement observé.
- [Dossier de preuves](../dossier-preuves.md) prêt et test fonctionnel initial conservé.

## Choisir les outils selon leur couverture

| Outil | Angle d'observation | Éléments à conserver |
| --- | --- | --- |
| Greenbone Community Edition/OpenVAS | Vulnérabilités des services de la cible, avec ou sans authentification selon le scan | Cible, ports, profil, résultat d'authentification, date des feeds et rapport |
| Lynis | Audit local de la configuration et du durcissement du système | Privilèges utilisés, avertissements, suggestions, identifiants des tests et rapport |
| Trivy | Analyse d'images ou de fichiers applicatifs : composants vulnérables, configurations et secrets selon les scanners activés | Type de cible, digest d'image ou révision du dépôt, scanners, date de base et rapport |

Greenbone Community Edition désigne l'ensemble de la plateforme ; OpenVAS en
est un composant de scan. Préparer les feeds et vérifier la disponibilité du
scanner avant d'interpréter un résultat vide. Référence :
[documentation Greenbone](https://greenbone.github.io/docs/latest/).

Lynis complète la vue réseau par des contrôles locaux ; ses suggestions doivent
être étudiées dans le contexte du serveur. Référence :
[guide d'utilisation Lynis](https://cisofy.com/documentation/lynis/).

Trivy analyse un artefact accessible, pas une URL applicative comme un scanner
web. Choisir explicitement le type de cible et les scanners utiles. Références :
[analyse de fichiers](https://trivy.dev/docs/latest/guide/target/filesystem/) et
[détection des vulnérabilités](https://trivy.dev/docs/latest/scanner/vulnerability/).

## Travail à réaliser

1. Relever l'OS, les versions, les services, les dépendances et les ports attendus.
2. Noter le point d'observation du scan : réseau de test représentant Internet
   ou réseau d'administration. La visibilité peut être différente.
3. Enregistrer les versions et dates des bases, puis réaliser les trois analyses
   dans le périmètre défini. Si un accès manque, consigner la couverture manquante.
4. Exporter les rapports avant de corriger le serveur.
5. Créer un constat par problème, regrouper les doublons et citer les preuves.
6. Vérifier l'applicabilité : composant réellement présent, version corrigée par
   l'éditeur, configuration effective, prérequis et éventuel faux positif.
7. Proposer une priorité, un responsable, une action et une échéance à valider.

## Qualifier avant de prioriser

| Dimension | Question à traiter |
| --- | --- |
| Fiabilité | Quelle preuve confirme le constat ? Qu'est-ce qui reste une hypothèse ? |
| Exposition | Le composant est-il accessible depuis le point d'entrée concerné ? |
| Exploitabilité | Quels droits et conditions sont nécessaires ? Une exploitation connue est-elle documentée ? |
| Impact | Quelles conséquences sur le service, les données et les autres machines ? |
| Protection existante | Un filtrage ou un autre contrôle limite-t-il réellement le scénario ? |
| Faisabilité | Correctif disponible, compatibilité, interruption et solution compensatoire ? |

Une CVE est un identifiant de vulnérabilité ; le CVSS renseigne sa sévérité
technique. La priorité de traitement ajoute le contexte métier et l'exposition.
Un score élevé ou un nombre de résultats ne suffit pas à décider seul.

| Priorité proposée | Critère de décision à justifier |
| --- | --- |
| Urgente | Risque important et accessible, avec exploitation plausible ou indices d'exploitation à qualifier |
| Haute | Défaut confirmé à impact important, nécessitant une correction planifiée rapidement |
| Planifiée | Réduction du risque à intégrer à une fenêtre de maintenance |
| À investiguer | Informations insuffisantes ; désigner un responsable de vérification |

Cette grille est une proposition pédagogique. Les délais seront fixés avec les
responsables ; « à investiguer » ne signifie pas « sans risque ».

## État final attendu et preuves L1

- Périmètre et état initial reproductibles.
- Rapports des trois outils, ou justification précise d'une analyse non réalisée.
- Registre de constats avec preuves, qualification et priorités argumentées.
- Liste des limites : accès, périmètre, outil, base de vulnérabilités ou test non concluant.

Une absence de résultat ne prouve pas l'absence de vulnérabilité. Vérifier
d'abord la réussite du scan et sa couverture. Conserver les rapports contenant
des secrets dans le dossier privé et anonymiser les extraits publiés.

- [Pense-bête de l'itération](../../pense-bete/glossaire/securisation-avancee-infrastructures/it-1.md)
- [Étape suivante — Corriger et vérifier](../it-2/index.md)
- [Retour au module](../README.md)
