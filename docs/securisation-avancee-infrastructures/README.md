# Sécurisation avancée des infrastructures

## Objectif global

Mettre en œuvre une démarche complète de sécurisation d'une infrastructure :
**auditer, analyser, corriger, vérifier, détecter et traiter un incident**, puis
traduire les enseignements obtenus en règles de sécurité.

## Cas fil rouge

En **2021**, un service de l'organisation a demandé un serveur pour échanger
des documents avec des partenaires externes. L'infrastructure a fourni un
serveur **Ubuntu 20.04** et le service demandeur y a déployé
**File Browser 2.15.0 dans un conteneur**.

Le service est toujours accessible depuis Internet en **2026**. La maintenance
de l'application devait être assurée par le service demandeur, mais la
répartition exacte des responsabilités et le suivi réalisé depuis l'installation
ne sont pas clairement documentés.

La mission porte sur l'état technique du serveur et sur son exploitation : qui
maintient le système, l'application et ses dépendances ? Qui décide des
corrections, surveille les événements et intervient en cas d'incident ?

L'audit produit un état initial. Les corrections sont ensuite contrôlées. Une
détection réseau avec Suricata, puis une centralisation collective avec Wazuh,
servent à analyser un incident affectant ce même serveur. Le retour d'expérience
alimente une proposition d'évolution d'un fragment de la PSSI de l'Université
de Poitiers étudiée en formation.

!!! info "Module préparé — premiers résultats documentés"
    Les six itérations ci-dessous constituent une progression **prévisionnelle**
    à adapter aux consignes du formateur. La
    [fiche de préparation](it-1/preparer-cible-installer-greenbone.md) rassemble
    les premiers résultats et sept captures : File Browser accessible depuis
    l'hôte, Greenbone démarré et feeds en cours de synchronisation au moment
    de la capture. Deux tâches de scan sont ensuite attestées terminées dans le
    [premier audit Greenbone](it-1/premier-audit-greenbone.md). Leurs rapports
    détaillés prouvent la réussite du scan SSH authentifié et documentent cinq
    constats qualifiés. Le durcissement et les activités
    suivantes restent à réaliser. Les identifiants L1 à L6 sont des repères internes
    de préparation, pas une numérotation officielle d'évaluation.

## Vous apprendrez à

- auditer avec Greenbone Community Edition/OpenVAS, Lynis et Trivy ;
- qualifier les constats et les prioriser selon le contexte, l'exposition,
  l'exploitabilité et l'impact métier ;
- durcir l'infrastructure, documenter les changements et vérifier leur efficacité ;
- mettre en œuvre et tester des règles de détection réseau avec Suricata ;
- centraliser et exploiter les événements avec Wazuh, dont ceux de Suricata ;
- qualifier un incident, reconstruire sa chronologie, contribuer au confinement
  et à la remédiation, puis réaliser un retour d'expérience ;
- analyser une PSSI existante et proposer un fragment révisé, justifié et vérifiable.

## Pour commencer

1. Compléter le [cadrage du laboratoire et des responsabilités](cadrage-laboratoire.md).
2. Suivre la [préparation de la cible et l'installation de Greenbone](it-1/preparer-cible-installer-greenbone.md).
3. Distinguer les constats avec [Vulnérabilité ou autre problème ?](it-1/vulnerabilite-ou-autre-probleme.md).
4. [Lire et analyser trois entrées CVE](it-1/lire-analyser-entrees-cve.md), puis comparer correctifs et conséquences résiduelles.
5. [Comprendre CVSS](it-1/comprendre-cvss.md) et distinguer sévérité et priorité de traitement.
6. [Observer la cible](it-1/observer-cible.md) avec les commandes déjà connues, avant le scan.
7. Ouvrir le [dossier de preuves et les modèles de suivi](dossier-preuves.md).
8. Réaliser le [premier audit avec Greenbone](it-1/premier-audit-greenbone.md), sans puis avec authentification SSH.
9. Poursuivre l'[audit et la priorisation](it-1/index.md), en conservant l'état initial.

## Environnement des exercices

| Système | Rôle et configuration imposés |
| --- | --- |
| Système hôte | Machine d'audit ; outils d'audit et Greenbone Community Edition |
| VM cible | Ubuntu Server **20.04**, **2 vCPU**, **4 Go de RAM** ; Docker et image `filebrowser/filebrowser:v2.15.0` |
| Accès applicatif | Depuis l'hôte vers l'adresse de la VM, sur le port **8080** |
| Fichiers servis | `/srv/filebrowser` sur la VM, monté dans `/srv` du conteneur |

**Les scans portent uniquement sur sa propre VM cible, jamais sur les machines
des autres apprenants.** L'exposition Internet appartient au cas fil rouge ;
le laboratoire conserve une portée locale et des données fictives.

Les adresses, ressources disponibles sur l'hôte, versions des outils d'audit
et modalités du travail collectif restent à renseigner.
Le document exact de PSSI reste à identifier avec sa version et ses pages.

## Progression prévisionnelle

| Étape | Activité | Production attendue | Pense-bête |
| --- | --- | --- | --- |
| [Itération 1](it-1/index.md) | Auditer et prioriser avec Greenbone/OpenVAS, Lynis et Trivy | L1 : rapport d'audit et registre des constats | [Termes et méthode](../pense-bete/glossaire/securisation-avancee-infrastructures/it-1.md) |
| [Itération 2](it-2/index.md) | Corriger, durcir et vérifier | L2 : journal des changements et comparaison avant/après | [Termes et méthode](../pense-bete/glossaire/securisation-avancee-infrastructures/it-2.md) |
| [Itération 3](it-3/index.md) | Détecter avec Suricata, individuellement | L3 : emplacement de la sonde, règles et tests | [Termes et méthode](../pense-bete/glossaire/securisation-avancee-infrastructures/it-3.md) |
| [Itération 4](it-4/index.md) | Centraliser avec Wazuh, collectivement | L4 : chaîne de collecte et corrélation démontrées | [Termes et méthode](../pense-bete/glossaire/securisation-avancee-infrastructures/it-4.md) |
| [Itération 5](it-5/index.md) | Traiter l'incident sur le serveur étudié | L5 : chronologie, décisions, remédiation et REX | [Termes et méthode](../pense-bete/glossaire/securisation-avancee-infrastructures/it-5.md) |
| [Itération 6](it-6/index.md) | Analyser et faire évoluer un fragment de PSSI | L6 : analyse sourcée et proposition de règles contrôlables | [Termes et méthode](../pense-bete/glossaire/securisation-avancee-infrastructures/it-6.md) |

## Fil de preuve

Chaque constat reçoit un identifiant conservé jusqu'à la proposition de règle :

**Constat d'audit → priorité → correction → contrôle → détection → incident/REX → règle de sécurité.**

Une vulnérabilité remontée par un outil reste à qualifier. Une correction reste
à vérifier. Une alerte reste à analyser. Une nouvelle règle de PSSI reste une
proposition tant qu'elle n'a pas été approuvée par l'autorité compétente.

## Liens avec les modules précédents

- [Durcissement Linux](../admin-systemes-linux/it-4/durcissement-linux-alpesnet.md) : accès, services et configuration système.
- [Sécurisation des réseaux](../admin-reseaux-securisation/index.md) : segmentation, filtrage et observation du trafic.
- [Sécurité des données](../securite-donnees/index.md) : TLS, chiffrement, clés et récupération.
- [Supervision et optimisation des performances](../supervision-optimisation-performances/README.md) : journaux, alertes, diagnostic et exploitation.

Ces acquis peuvent être réutilisés, mais les résultats de leurs laboratoires
ne constituent pas automatiquement des preuves pour le nouveau serveur étudié.

## État attendu en fin de module

Un dossier permet de comprendre les risques du serveur, les décisions prises,
les changements réellement vérifiés, les événements détectés et les limites
restantes. Il relie les enseignements techniques aux responsabilités et aux
règles de sécurité proposées.
