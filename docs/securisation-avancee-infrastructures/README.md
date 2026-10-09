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
    Les sept itérations ci-dessous constituent une progression **prévisionnelle**
    à adapter aux consignes du formateur. La
    [fiche de préparation](it-1/preparer-cible-installer-greenbone.md) rassemble
    les premiers résultats et sept captures : File Browser accessible depuis
    l'hôte, Greenbone démarré et feeds en cours de synchronisation au moment
    de la capture. Deux tâches de scan sont ensuite attestées terminées dans le
    [premier audit Greenbone](it-1/premier-audit-greenbone.md). Leurs rapports
    détaillés prouvent la réussite du scan SSH authentifié et documentent cinq
    constats qualifiés. Le durcissement et les activités
    suivantes restent à réaliser. Les identifiants L1 à L7 sont des repères internes
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
9. [Reprendre les constats du J1](it-2/reprendre-constats-j1.md) et préparer les
   vérifications locales sans modifier la cible.
10. [Installer et découvrir Lynis](it-2/installer-decouvrir-lynis.md), puis
    produire et conserver le rapport d'audit local.
11. [Analyser et prioriser les résultats de Lynis](it-2/analyser-prioriser-resultats-lynis.md)
    avant de sélectionner les modifications.
12. [Vérifier la configuration du système](it-2/verifier-configuration-systeme.md)
    et confirmer manuellement les constats retenus sans modifier la cible.
13. [Consolider les résultats Greenbone et Lynis](it-2/consolider-resultats-greenbone-lynis.md)
    dans une analyse unique avant toute modification.
14. [Identifier les limites de l’audit et préparer l’analyse du conteneur](it-2/limites-audit-preparer-analyse-conteneur.md)
    avant l’analyse de l’image au J3.
15. [Observer le conteneur sans y exécuter Lynis](it-2/etendre-audit-conteneur.md)
    et conserver uniquement les informations disponibles depuis Docker.
16. [Évaluer les risques et définir les priorités](it-3/evaluer-risques-definir-priorites.md)
    avec un classement contextualisé de tous les constats.
17. Poursuivre l'[itération 2](it-2/index.md) avec les corrections, le
    durcissement et les contrôles avant/après.
17. Ouvrir l'[itération 3](it-3/index.md) en identifiant
    [ce qui manque dans l’audit](it-3/identifier-manques-audit.md) avant
    l’analyse de l’image avec Trivy.
18. [Analyser l’image avec Trivy](it-3/analyser-image-trivy.md), conserver le
    rapport complet et qualifier les résultats dans le contexte du serveur.
19. [Analyser et vérifier les résultats Trivy](it-3/analyser-verifier-resultats-trivy.md)
    à partir des entrées CVE, du code File Browser et de l’exposition observée.
20. [Consolider les trois sources d’audit](it-3/consolider-trois-sources-audit.md)
    dans un tableau unique et conserver la justification des résultats écartés.

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
| [Itération 1](it-1/index.md) | Observer et auditer avec Greenbone/OpenVAS | L1 : premier rapport et constats distants/authentifiés | [Termes et méthode](../pense-bete/glossaire/securisation-avancee-infrastructures/it-1.md) |
| [Itération 2](it-2/index.md) | Auditer localement avec Lynis, vérifier et consolider | L2 : audit local, vérifications manuelles et analyse consolidée | [Termes et méthode](../pense-bete/glossaire/securisation-avancee-infrastructures/it-2.md) |
| [Itération 3](it-3/index.md) | Identifier les limites puis analyser l’image avec Trivy | L3 : inventaire de l’image et vulnérabilités qualifiées | [Termes et méthode](../pense-bete/glossaire/securisation-avancee-infrastructures/it-3.md) |
| [Itération 4](it-4/index.md) | Préparer les remédiations puis détecter avec Suricata, individuellement | L4 : actions préparées, validations/retours arrière ; sonde, règles et tests | [Termes et méthode](../pense-bete/glossaire/securisation-avancee-infrastructures/it-4.md) |
| [Itération 5](it-5/index.md) | Bilan du durcissement et préparation du fragment de PSSI | L5 : compte-rendu, analyse organisationnelle, propositions de règles et plan J6 | [Termes et méthode](../pense-bete/glossaire/securisation-avancee-infrastructures/it-5.md) |
| [Itération 6](it-6/index.md) | Élaborer le fragment de PSSI | L6 : périmètre et première version des règles à valider | [Termes et méthode](../pense-bete/glossaire/securisation-avancee-infrastructures/it-6.md) |
| [Itération 7](it-7/index.md) | Analyser et faire évoluer un fragment de PSSI | L7 : analyse sourcée et proposition de règles contrôlables | [Termes et méthode](../pense-bete/glossaire/securisation-avancee-infrastructures/it-7.md) |

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

## Rapport final et préparation du J4

[Finaliser le rapport d’audit et le plan de remédiation](it-3/finaliser-rapport-plan-remediation.md) — **2 h** :
synthèse des preuves Greenbone, Lynis, Trivy et manuelles, priorités, lots
de traitement, investigations et validations futures.

## Itération 4 — Préparation des remédiations

[Préparer les remédiations](it-4/preparer-remediations.md) : reprendre le plan du
J3, sélectionner les actions prioritaires (dont les identifiants File Browser),
préparer impacts, validations et retours arrière avant mise en œuvre.

[Mettre en œuvre et vérifier les remédiations](it-4/mettre-en-oeuvre-verifier-remediations.md) :
rechercher la méthode, appliquer les changements retenus, valider sécurité et
fonctionnement, diagnostiquer les échecs et documenter chaque résultat.

[Finaliser le compte-rendu de durcissement](it-4/finaliser-compte-rendu-durcissement.md) — **1 h** :
synthèse des remédiations réalisées, écarts, diagnostics et risques résiduels ;
préparation de la vérification globale J5 et du livrable utilisé pour C2.

## Itération 5 — Bilan du durcissement et préparation du fragment de PSSI

[Vérifier l’état du système après remédiation](it-5/verifier-etat-systeme-apres-remediation.md) :
comparer aux constats J3, reprendre les preuves J4 et compléter les verdicts J5
avec des contrôles pertinents. Contrôles manuels, Greenbone et Lynis refaits
selon Olivier ; résultats stables, pièces J5 à joindre. Risques résiduels et
investigations conservés dans le compte-rendu utilisé pour C2.

[Finaliser le compte-rendu de durcissement et de vérification](it-5/finaliser-compte-rendu-durcissement-verification.md) :
conclusion J5, résultats par remédiation, difficultés et risques résiduels ;
contrôles refaits déclarés, annexes J5 encore à joindre.

[Identifier ce que la technique ne règle pas](it-5/identifier-ce-que-technique-ne-regle-pas.md) :
analyser les problèmes organisationnels du cas File Browser et proposer
responsables, règles de maintenance et contrôles du cycle de vie.

[Analyser une PSSI existante — Université de Poitiers](it-5/analyser-pssi-existante-poitiers.md) :
lecture du document fourni, analyse de règles sourcées et adaptations au cas
File Browser ; responsabilités, maintenance, accès, réseau et preuves de contrôle.

[Proposer des règles adaptées au cas fil rouge](it-5/proposer-regles-adaptees-cas-fil-rouge.md) :
premières propositions sur maintenance, vulnérabilités, mises à jour, exposition,
contrôles, exceptions, cycle de vie et accès ; adoption à valider.

[Préparer le fragment de PSSI](it-5/preparer-fragment-pssi.md) :
cinq sujets regroupant P01–P08, ancrage dans le cas File Browser et plan
de rédaction J6 ; décisions et adoption encore à valider.

## Itération 6 — Élaborer le fragment de PSSI

[Définir le périmètre du fragment de PSSI](it-6/definir-perimetre-fragment-pssi.md) :
situations d’administration hors équipe principale, ressources, acteurs,
responsabilités, cycle de vie, exclusions et interfaces ; préparation J6 à valider.

[Définir les rôles et responsabilités](it-6/definir-roles-responsabilites.md) :
répartition proposée des décisions et tâches pendant le cycle de vie, application
à File Browser et continuité lors d’un départ ou d’un changement de fonction.

[Définir les règles du cycle de vie d’un service](it-6/definir-regles-cycle-vie-service.md) :
onze règles précisant attentes, destinataires, responsables et preuves de contrôle ;
fréquences et délais proposés, adoption à valider.

[Définir les contrôles et les exceptions](it-6/definir-controles-exceptions.md) :
contrôles des règles CV01–CV11, preuves, écarts et exceptions avec décision,
compensations, durée, réexamen et clôture ; section du fragment à valider.

[Tester le fragment de PSSI](it-6/tester-fragment-pssi.md) :
cinq situations A–E, décisions, règles mobilisées et informations manquantes ;
circuits CV07 et CV11 précisés à la suite du test documentaire.

[Fragment de PSSI — V1](it-6/fragment-pssi-v1.md) :
version autonome consolidée et conservée le 6 octobre 2026, intégrant le test A–E ;
référence pour les journées suivantes, adoption à valider et future V2 après REX.

## Itération 7 — Première détection réseau avec Suricata

[Contexte et objectifs du 7 octobre 2026](it-8/index.md) : Suricata directement
sur l’hôte, visibilité du trafic VM et analyse d’événements.

[Identifier le point d’observation — 45 min](it-7/identifier-point-observation.md) :
interfaces, IP, trajets, services exposés, visibilité et limites ; à lire avant les règles.

[Comprendre les événements produits](it-7/comprendre-evenements-produits.md) :
localiser EVE sur l’hôte, générer DNS/connexions normales depuis la VM et accès
File Browser depuis l’hôte, retrouver et analyser les objets ; nouveaux essais à réaliser.

[Installer et tester des règles Suricata — 1 h 15](it-7/installer-tester-regles-suricata.md) :
lecture du dépôt, quatre signatures proposées, dix maximum, validation et tests
inertes sur serveur temporaire ; tableau des quatre règles testé/résultat et
extrait EVE observé et export brut documenté sur l’hôte.

[Observer l’activité autour de File Browser](it-7/observer-activite-file-browser.md) :
accès contrôlés, ressources, SSH et échecs ; grille événement/alerte et limites
des déductions. Huit captures HTTP sur 8080 intégrées ; SSH/22 reste à documenter.

[Faire le bilan du dispositif de détection](it-7/bilan-dispositif-detection.md) :
installation, preuves normales/alertes, six réponses, angles morts et pistes
de réglage pour la prochaine journée, avant centralisation.

[Pense-bête de l’itération 7](../pense-bete/glossaire/securisation-avancee-infrastructures/it-7.md).

## Itération 8 — Des constats d’audit au réglage de la détection

[Vue d’ensemble](it-8/index.md) — 8 octobre 2026.

[Des vulnérabilités aux besoins de détection — 1 h](it-8/vulnerabilites-besoins-detection.md) :
constats J1–J3, conditions d’exploitation, visibilité sur virbr0 et signaux possibles ;
états historiques distingués des remédiations et limites actuelles.

[Pense-bête](../pense-bete/glossaire/securisation-avancee-infrastructures/it-8.md).

[Rechercher et adapter des règles de détection — 1 h 15](it-8/rechercher-adapter-regles-detection.md) :
recherche directe/comportementale, trois règles locales proposées, tests et limites ;
configuration validée et alerte 1008001 observée ; autres déclenchements à confirmer.

[Relier les détections à MITRE ATT&CK](it-8/relier-detections-mitre-attack.md) :
tactiques, techniques et rapprochements conditionnels à partir des événements ;
limites et informations manquantes explicites.

[Concevoir les différents points d’observation](it-8/concevoir-points-observation.md) :
architecture cible Suricata et agent Wazuh dans le conteneur, visibilité,
corrélation, limites et preuves de validation attendues.

[Installer Wazuh en single-node — travail en groupe](it-8/installer-wazuh-single-node.md) :
stack Docker officielle, prérequis, certificats, diagnostic et preuves
de fonctionnement et d’accès au dashboard à conserver.

[Peut-on installer un agent Wazuh dans le conteneur File Browser ?](it-8/etudier-agent-wazuh-file-browser.md) :
investigation de compatibilité, stratégie reproductible, essai isolé,
diagnostic et note d’intégration ; faisabilité à établir.

## Itération 9 — Reprise du dispositif de détection

[Vue d’ensemble](it-9/index.md) — 9 octobre 2026.

[Reprendre le dispositif de détection](it-9/reprendre-dispositif-detection.md) :
contrôler File Browser, Suricata, les règles et Wazuh ; générer des activités
connues, retrouver leurs traces et compléter le tableau des sources et limites.
Contrôles J9 à réaliser ; agent J8 installé sur la VM, pas dans le conteneur.

[Pense-bête de l’itération 9](../pense-bete/glossaire/securisation-avancee-infrastructures/it-9.md).

[Construire une vue exploitable des événements — 1 h](it-9/construire-vue-exploitable-evenements.md) :
activités contrôlées, comparaison Suricata/Docker/Wazuh, corrélation temporelle
et distinction signal, bruit, redondances et informations manquantes ; nouveaux essais à réaliser.

[Vérifier votre capacité de détection](it-9/verifier-capacite-detection.md) :
scan Nmap borné, ports fermés, chemins HTTP inhabituels ; observation,
recherche/adaptation de règles et interprétation sans attribution d’intention.
Essais à réaliser, trois signatures locales proposées à valider.

[Préparer l’analyse d’une situation inhabituelle](it-9/preparer-analyse-situation-inhabituelle.md) :
questions d’investigation, ordre des sources, conservation des preuves,
chronologie vide et distinction fait/interprétation/hypothèse ; préparation
avant réception des premiers éléments, sans incident présumé.

[Incident : premiers éléments](it-9/incident-premiers-elements.md) :
signalement d’accès inattendus, recherches EVE/Docker/Wazuh, chronologie
en cours et hypothèses ; période à obtenir et faits techniques à rechercher,
sans incident présumé ni confusion avec les tests contrôlés.

[Qualifier la situation et préparer la suite](it-9/qualifier-situation-preparer-suite.md) :
état provisoire, faits/hypothèses/manques, risques conditionnels et impacts
des actions ; conservation pour J10 et investigations priorisées, sans
restriction/isolation/arrêt automatique ni clôture de la situation.
