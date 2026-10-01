# Mémo — Journée IA & Cybersécurité

## 29 septembre 2026 — MIAI Cluster, MaCI, Saint-Martin-d'Hères

> **Objectif** : regrouper les notes, définitions, tableaux et conclusions travaillés ensemble autour de la journée IA & Cybersécurité, avec une structure prête à accueillir les PDF des conférences.

---

## 0. Programme de la journée

### Matin — conférence d'ouverture

- **09:30 – 10:00** : Café d'accueil
- **10:00 – 12:00** : **Cyber-risques et ingérences**  
  Conférence non enregistrée et inaccessible à distance.
- **12:00 – 13:30** : Pause déjeuner

### Après-midi scientifique

- **13:30 – 14:00** : **AI for security and security for AI** — Kavé Salamatian, Université Savoie Mont Blanc
- **14:00 – 14:30** : **Rethinking Cybersecurity Regulation in an Age of Uncertainty** — Karine Bannelier & Theodoros Karathanasis, CyberAlps / UGA
- **14:30 – 15:00** : **Evolution of Machine Learning Intrusion Detection Systems Resiliency to Network Traffic** — Maxime Puys, Université Clermont Auvergne
- **15:00 – 15:30** : **Secured and Safe Embedded Artificial Intelligence for Cyber-Physical Systems** — Louis Morge-Rollet, Grenoble INP – UGA / LCIS
- **15:30 – 16:00** : Discussions et échanges

---

## 1. Conférence d'ouverture — Cyber-risques, ingérences et souveraineté

### 1.1 DGSI

La **DGSI — Direction générale de la sécurité intérieure** est le principal service français de renseignement intérieur.

Ses missions couvrent notamment :

- le contre-espionnage ;
- la lutte contre le terrorisme ;
- les ingérences étrangères ;
- la protection du patrimoine scientifique et économique ;
- la cybersécurité ;
- la protection des intérêts stratégiques nationaux.

## 1.2 Définition large de la sécurité

La sécurité vise à protéger :

- l'État ;
- les citoyens ;
- les infrastructures ;
- l'économie ;
- les systèmes d'information ;
- les données ;
- la souveraineté.

Elle cherche surtout à garantir :

- **continuité** ;
- **résilience** ;
- **souveraineté**.

> Même lorsqu'une attaque ou une crise survient, les fonctions essentielles doivent continuer à fonctionner et pouvoir être restaurées rapidement.

### 1.3 Domaines de risque

| Domaine | Menaces | Ce qui est protégé | Protections |
| --- | --- | --- | --- |
| Géopolitique | Espionnage, ingérence, désinformation, sabotage | Souveraineté, institutions, défense | Renseignement, contre-espionnage, protection des données |
| Économique | Espionnage industriel, fraude, ransomware, dépendance | Entreprises, innovation, compétitivité | Cyber, secret industriel, supply chain |
| Sociétal | Désinformation, manipulation, fuite de données | Population, confiance, vie privée | Protection des données, sensibilisation |
| Systèmes critiques | Attaques sur énergie, santé, eau, transport | Fonctionnement du pays | Segmentation, redondance, continuité |
| Cyber | Phishing, malware, DDoS, vulnérabilités | SI, données, services | Pare-feu, EDR, MFA, SIEM, SOC |
| Physique | Intrusion, sabotage, destruction | Datacenters, réseaux, équipements | Contrôle d'accès, surveillance, secours |

#### Six grands boucliers

1. Protection de l'information
2. Protection des infrastructures
3. Résilience et continuité
4. Détection et réaction
5. Protection humaine
6. Souveraineté et autonomie stratégique

> **À retenir :** la sécurité moderne protège autant les chaînes de dépendance et les capacités stratégiques que les machines.

### 1.4 IA et sécurité : gouvernance

| Axe | Objectif | Mesures clés | Acteurs |
| --- | --- | --- | --- |
| Données & modèles | Réduire vol, fuite, manipulation | Chiffrement, accès, cloisonnement, traçabilité | RSSI, DSI, Data/IA |
| Conformité & gouvernance | Encadrer usages et responsabilités | Charte IA, inventaire, validation | Direction, juridique, DPO |
| Robustesse | Éviter dérive et erreurs | Tests, red team, suivi du drift | Data, cyber, métiers |
| Formation | Réduire le risque humain | Sensibilisation, règles d'usage | RH, RSSI |
| Dépendances | Réduire le lock-in | Multi-fournisseurs, stratégie de sortie | DSI, achats, juridique |
| Résilience | Continuer malgré incident | Redondance, sauvegardes, PRA/PCA | DSI, production |
| Ressources | Maîtriser coût et consommation | Edge, modèles adaptés, optimisation | DSI, Data/IA |

**Fil conducteur :** Gouverner → limiter → surveiller → résister

---

## 2. AI for security & security for AI

[DGSI conférences](assets/files/Presentation_IA_Cyber_DGSI.pdf)

### 2.1 IA comme aide à la cybersécurité

L'IA permet :

- d'analyser de gros volumes de données ;
- de détecter des comportements inhabituels ;
- de corréler des événements ;
- d'extraire des informations ;
- d'accélérer les investigations ;
- d'assister les analystes SOC.

#### Comprendre des données complexes

Sources typiques :

- logs ;
- flux réseau ;
- événements cloud ;
- données applicatives ;
- authentifications ;
- alertes EDR.

#### Extraire des informations

Exemples :

- IP ;
- utilisateurs ;
- dates ;
- vulnérabilités ;
- systèmes touchés ;
- IoC.

#### Faire correspondre des règles

Comparaison avec :

- ISO 27001 ;
- NIS2 ;
- politiques internes ;
- règles de durcissement.

### 2.2 La cybersécurité est primordiale pour l'IA

Chaîne à protéger :

***Données → Modèle → API → Infrastructure → Utilisateur → Connecteurs***

Risques :

- vol du modèle ;
- fuite de données ;
- prompt injection ;
- jailbreak ;
- poisoning ;
- compromission d'API ;
- supply chain.

### 2.3 Gouvernance négligée

Questions à poser :

- Qui peut utiliser l'IA ?
- Avec quelles données ?
- Pour quel usage ?
- Avec quels privilèges ?
- Qui valide ?
- Qui surveille ?
- Qui est responsable ?

#### Shadow AI

Usage d'outils IA sans validation officielle.

Risques :

- fuite de données ;
- non-conformité ;
- perte de contrôle ;
- responsabilités floues.

### 2.4 L'humain dans la boucle

Risques d'une confiance excessive :

- biais d'automatisation ;
- faux positifs ;
- faux négatifs ;
- perte de compétences ;
- erreurs amplifiées.

---

## 3. Attaques spécifiques contre l'IA

| Attaque | Définition simple | Risque |
| --- | --- | --- |
| Jailbreak | Contourner les restrictions du modèle | Réponses / actions interdites |
| Prompt Injection | Faire ignorer les instructions initiales | Fuite, détournement |
| Injection indirecte | Instruction malveillante dans une source externe | Une donnée devient une consigne |
| Data Poisoning | Corrompre les données d'entraînement | Décisions biaisées |
| Model Poisoning | Modifier directement le modèle | Backdoor / comportement caché |
| Backdoor | Déclencheur secret | Mauvaise réponse ciblée |
| Adversarial Attack | Modifier légèrement une entrée | Mauvaise classification |
| Model Extraction | Copier le comportement d'un modèle | Vol de propriété intellectuelle |
| Model Inversion | Retrouver des données d'entraînement | Fuite d'informations |

### 3.1 Jailbreak vs Prompt Injection

- **Jailbreak** : l'utilisateur tente de contourner les garde-fous.
- **Prompt injection** : une instruction malveillante cherche à prendre le dessus sur les instructions système.
- **Injection indirecte** : l'instruction malveillante vient d'un document, mail, PDF ou site consulté par l'IA.

---

## 4. IA offensive

### Hameçonnage à grande échelle

L'IA facilite :

- messages crédibles ;
- personnalisation ;
- imitation du ton d'un dirigeant ou fournisseur.

### Deepfake

Création ou modification de :

- voix ;
- images ;
- vidéos.

### Malware et exploits

Accélération de :

- compréhension de code ;
- adaptation de malware ;
- analyse de vulnérabilités ;
- production de variantes.

### Découverte de vulnérabilités

Double usage :

- défense : correction plus rapide ;
- attaque : identification plus rapide des cibles.

---

## 5. Supply chain IA et modèles externes

Télécharger un modèle revient à faire confiance à :

- un fichier ;
- une configuration ;
- des dépendances ;
- un script ;
- parfois du code exécutable.

### Bonnes pratiques

- vérifier la provenance ;
- vérifier la réputation ;
- privilégier `safetensors` ;
- éviter l'exécution distante non maîtrisée ;
- scanner les fichiers ;
- isoler l'environnement ;
- appliquer le moindre privilège.

> **À retenir :** un modèle IA doit être traité comme un composant logiciel tiers.

---

## 6. Rethinking Cybersecurity Regulation in an Age of Uncertainty

[Rethinking Cybersécurity for IA](assets/files/IA_Cybersecurite_apres_midi.pdf)

### 6.1 La cyber est partout

Secteurs concernés :

- administrations ;
- santé ;
- énergie ;
- transports ;
- finance ;
- eau ;
- télécommunications ;
- industrie ;
- cloud ;
- espaces publics ;
- entreprises ;
- IA.

### 6.2 Principaux textes européens

| Texte | Domaine | Objectif |
| --- | --- | --- |
| RGPD | Données personnelles | Protection des données |
| NIS2 | Entités essentielles/importantes | Gestion des risques et incidents |
| DORA | Finance | Résilience opérationnelle numérique |
| AI Act | IA | Encadrer les systèmes selon le risque |
| CRA | Produits numériques | Cybersécurité dès la conception |
| CSA | Certification cyber | Certification européenne |
| Chips Act | Semi-conducteurs | Souveraineté technologique |

### 6.3 AI Act — contrôles

- gestion des risques ;
- cybersécurité ;
- qualité des données ;
- documentation ;
- tests et validation ;
- journalisation ;
- supervision humaine ;
- surveillance après déploiement.

#### Internal control

Contrôle réalisé par le fournisseur ou l'organisation.

#### Third-party assessment

Évaluation indépendante lorsque nécessaire.

### 6.4 Standards harmonisés

Le droit fixe :

- robustesse ;
- sécurité ;
- gouvernance ;
- traçabilité.

Les standards doivent permettre de répondre :
> « Comment démontrer concrètement la conformité ? »

### 6.5 Digital Omnibus

#### Digital Omnibus on AI

- simplification ;
- clarification ;
- adaptation de certains délais ;
- réduction de certaines charges.

#### Digital Omnibus général

Concerne :

- données ;
- cyber ;
- vie privée ;
- articulation des textes.

Objectif :
**réduire les chevauchements réglementaires.**

---

## 7. Connexions AI Act, CRA, CSA, Chips Act

### AI Act ↔ CRA

- AI Act : sécurité et gouvernance du système IA.
- CRA : sécurité du produit numérique.

### CSA ↔ CRA

- CSA : certification.
- CRA : exigences obligatoires.

Une certification CSA ne vaut pas automatiquement conformité CRA.

### CSA ↔ AI Act

Les certifications cyber et IA restent encore partiellement séparées.

### AI Act ↔ supply chain

Le système dépend :

- de modèles ;
- datasets ;
- bibliothèques ;
- API ;
- cloud ;
- fournisseurs.

### Chips Act ↔ CRA

Une puce produite localement ne garantit pas la sécurité du firmware ou du produit final.

### Chips Act ↔ AI Act

- Chips Act : souveraineté matérielle / capacité de calcul.
- AI Act : usage, gouvernance et risques.

---

## 8. 5G Toolbox

La **5G Toolbox** marque un changement de logique.

Elle intègre :

- sécurité technique ;
- dépendance aux fournisseurs ;
- concentration ;
- supply chain ;
- risque géopolitique ;
- impact systémique.

> Le risque cyber devient technique, économique et stratégique.

---

## 9. Exemple : onduleurs solaires connectés

Un onduleur connecté dépend potentiellement :

- du fabricant ;
- du cloud ;
- du firmware ;
- des mises à jour ;
- du contrôle distant.

Une compromission massive peut provoquer :

- perturbation du réseau ;
- impact systémique ;
- problème de souveraineté ;
- dépendance fournisseur.

### Question moderne

Pas seulement :
> « L'équipement est-il sécurisé ? »

Mais :
> « Qui peut le contrôler et que se passe-t-il si tout le parc est affecté ? »

---

## 10. SecNumCloud 3.2

SecNumCloud est le référentiel français de confiance cloud.

Il couvre :

- sécurité technique ;
- organisation ;
- accès ;
- continuité ;
- sous-traitance ;
- aspects juridiques ;
- lois extraterritoriales.

**Idée clé :** Sécurité + confiance + souveraineté juridique.

---

## 11. CSA 2.0

Évolution vers :

- certification ;
- supply chain ;
- fournisseurs à haut risque ;
- vulnérabilités ;
- résilience ;
- gouvernance européenne.

### Avant

> « Le produit est-il assez sécurisé ? »

### Maintenant

> « De qui dépend-il, qui le contrôle et quel serait l'impact d'une compromission massive ? »

---

## 12. Dépendances et gouvernance numérique

| Risque | Exemple | Conséquence |
| --- | --- | --- |
| Fournisseur étranger | Cloud hors UE | Perte d'autonomie |
| Concentration | Hyperscalers | Effet domino |
| Vendor lock-in IA | API unique | Coûts, dépendance |
| Dépendance hardware | GPU rares | Pénurie |
| Dépendance données | Dataset externe | Difficulté d'audit |
| Gouvernance fragmentée | DSI/RSSI/juridique dispersés | Responsabilité floue |
| Shadow AI | IA publique non validée | Fuite de données |
| Absence de sortie | Application non portable | Maintien forcé |
| Conflit de juridictions | Données sous plusieurs droits | Incertitude |
| Perte de compétences | Externalisation totale | Dépendance durable |

### Conclusion réglementation

#### Avant réglementation

***« Est-ce que le système est sécurisé ? »***

#### Aujourd'hui

***« De qui dépend-il ? Qui peut le contrôler ? Où sont les données ? Quels fournisseurs interviennent ? Quel serait l'impact d'une compromission à grande échelle ? »***

---

## 13. Secured and Safe Embedded Artificial Intelligence for Cyber-Physical Systems

> PDF à intégrer : **Secured and Safe Embedded Artificial Intelligence for Cyber-Physical Systems**

### 13.1 LCIS

Le **LCIS — Laboratoire de Conception et d'Intégration des Systèmes** est situé à Valence, dans la Drôme, et rattaché à Grenoble INP - UGA.

Domaines :

- systèmes embarqués ;
- réseaux ;
- cybersécurité ;
- IA ;
- traitement du signal ;
- systèmes complexes.

### 13.2 Système embarqué

Système informatique intégré à un appareil pour réaliser une fonction précise.

Exemples :

- drone ;
- calculateur automobile ;
- montre ;
- robot ;
- dispositif médical.

### 13.3 CPS

***Cyber-Physical System***

Chaîne :
**Capteurs → Traitement → Décision → Action**

> Une cyberattaque peut donc produire une conséquence physique.

---

## 14. Rôle de l'IA dans embarqué et CPS

### Système embarqué

L'IA :

- reconnaît ;
- optimise ;
- détecte ;
- automatise.

### CPS

L'IA :

- analyse les capteurs ;
- décide ;
- commande parfois une action physique.

---

## 15. BLERP

| Lettre | Signification | Question |
| --- | --- | --- |
| B | Bandwidth | Combien de données ? |
| L | Latency | Quelle rapidité ? |
| E | Economics | Quel coût ? |
| R | Reliability | Faut-il fonctionner hors ligne ? |
| P | Privacy | Les données peuvent-elles sortir ? |

---

## 16. Security vs Safety

| | Security | Safety |
| --- | --- | --- |
| But | Éviter attaque | Éviter accident |
| Origine | Intentionnelle | Souvent accidentelle |
| Auto | Piratage à distance | Capteur défaillant |
| Industrie | Automate compromis | Robot dangereux |
| IA | Protéger modèle/données | Éviter décision dangereuse |

> **Une faille de Security peut provoquer un problème de Safety.**

---

## 17. Attaques hardware / IA

| Attaque | Principe |
| --- | --- |
| Data Poisoning | Corrompre les données |
| Side-Channel | Observer le fonctionnement physique |
| Fault Injection | Provoquer une erreur matérielle |
| Hardware Trojan | Ajouter une fonction cachée |
| Model Poisoning | Modifier le modèle |
| Backdoor | Déclencheur secret |
| Adversarial Attack | Tromper le modèle via l'entrée |
| Model Extraction | Copier le comportement |
| Model Inversion | Retrouver des données sensibles |

---

## 18. Exemple : essaim de drones

Risques :

- poisoning ;
- adversarial attack ;
- spoofing ;
- brouillage ;
- compromission d'un drone ;
- hardware Trojan ;
- fault injection ;
- side-channel ;
- attaque sur la coordination.

> Un seul élément compromis peut influencer tout le système collectif.

---

## 19. Hardware pour améliorer et protéger l'IA

### Performance

- GPU ;
- NPU ;
- accélérateurs ;
- edge computing.

### Sécurité

- TPM ;
- Secure Boot ;
- enclaves ;
- mémoire protégée ;
- modules cryptographiques.

> Le hardware peut devenir une racine de confiance.

---

## 20. Cross-Layer Descriptor

Couches analysées :

- PHY ;
- liaison ;
- réseau ;
- transport ;
- application.

### Pipeline

1. Acquisition du signal
2. Extraction des caractéristiques
3. Fusion en vecteur
4. Échange de caractéristiques
5. Classification
6. Trafic normal / intrusion

Classifieurs :

- local ;
- centralisé ;
- décentralisé.

> Le Cross-Layer Descriptor donne à l'IA une vision globale permettant de repérer des corrélations anormales entre couches.

---

## 21. Conclusion IA embarquée

Chaîne à protéger :

***Données → Modèle → Logiciel → Réseau → Hardware → Environnement → Action***

L'objectif final est une IA :

- performante ;
- robuste ;
- explicable ;
- sécurisée ;
- sûre dans des conditions réelles.

---

## 22. ML-based NIDS

> PDF / présentation à intégrer : **Evolution of Machine Learning Intrusion Detection Systems Resiliency to Network Traffic**

Un **NIDS basé sur le machine learning** apprend les comportements réseau afin de détecter :

- anomalies ;
- attaques connues ;
- attaques nouvelles ;
- comportements inhabituels.

### Différence

NIDS classique :
> « Je reconnais une signature. »

ML-NIDS :
> « Je détecte quelque chose qui sort de la normale. »

---

## 23. Difficultés des NIDS ML

| Terme | Définition |
| --- | --- |
| Diversity of network traffic | Trafic très varié |
| Outlier detection | Détection de comportements anormaux |
| Semantic gap | Anormal statistiquement ≠ attaque |
| High cost of errors | Faux positifs / négatifs coûteux |
| Difficulties with evaluation | Difficile de reproduire le réel |
| Adversarial setting | L'attaquant tente de tromper le modèle |

### Problèmes d'évaluation

| Terme | Définition |
| --- | --- |
| Lab-only evaluation | Tests trop contrôlés |
| Label shift | Les classes changent avec le temps |
| Temporal snooping | Des données futures contaminent l'évaluation |

---

## 24. Data drift

Le **data drift** apparaît lorsque les données réelles ne ressemblent plus suffisamment aux données d'entraînement.

Exemples :

- nouveaux hôtes ;
- nouveaux protocoles ;
- nouveaux services ;
- nouveaux usages.

> Un modèle performant aujourd'hui peut devenir moins fiable demain.

---

## 25. Question de recherche NIDS

> Comment le data drift provoqué par de nouveaux hôtes ou protocoles affecte-t-il un NIDS IA entraîné dans une hypothèse de monde fermé ?

Objectifs :

- mesurer l'impact de l'évolution de l'infrastructure ;
- évaluer la robustesse ;
- construire des scénarios réalistes.

---

## 26. Dataset

Environnement :

- Windows ;
- Ubuntu ;
- macOS ;
- serveur web ;
- DNS ;
- SSH ;
- FTP ;
- HTTP ;
- HTTPS ;
- NTP ;
- LDAP ;
- SMB ;
- Kerberos.

Attaques :

- Heartbleed ;
- bruteforce ;
- DoS ;
- DDoS ;
- attaques web ;
- infiltration ;
- port scanning.

---

## 27. Flows réseau

Les paquets partageant :

- IP source ;
- IP destination ;
- port source ;
- port destination ;
- protocole

sont regroupés en **flow**.

Le ML travaille sur :

- nombre de paquets ;
- octets ;
- durée ;
- taille ;
- débit.

---

## 28. Répartition principale des protocoles

| Port | Service | Part |
| --- | --- | ---: |
| 53 | DNS | 51 % |
| 80 | HTTP | 24 % |
| 443 | HTTPS | 21 % |
| autres | Divers | < 2 % chacun |

Les trois principaux représentent environ **96 % des flux**.

---

## 29. Autoencodeur

Le modèle est entraîné sur du **trafic bénin**.

Principe :

1. encoder ;
2. compresser ;
3. reconstruire ;
4. mesurer l'erreur.

La **MSE** sert de score d'anomalie.

- trafic connu → faible erreur ;
- trafic inhabituel → forte erreur.

---

## 30. Scénarios de drift

### Scope 1 — nouveaux hôtes

- Ubuntu ;
- Windows ;
- Mac.

### Scope 2 — nouveaux protocoles

- SSH ;
- FTP ;
- HTTP ;
- NTP ;
- NetBIOS ;
- SMB ;
- LDAP.

### Scope 3 — changement de débit

- +10 % ;
- +50 %.

---

## 31. Résultats marquants

| Élément | Connu à l'entraînement | Absent à l'entraînement |
| --- | ---: | ---: |
| Windows | ~96 % | ~68 % |
| SSH | ~96 % | ~51 % |
| SMB | ~96 % | ~13 % |
| FTP | ~95 % | ~62 % |
| HTTP | ~95 % | ~71 % |
| NTP | ~95 % | ~79 % |

***Cas SMB : ~96 % → ~13 %***

---

## 32. Les métriques globales peuvent tromper

| Scénario | F1 global | Précision sur le nouvel élément |
| --- | ---: | ---: |
| Baseline | 0,87 | — |
| Windows | 0,71 | 0,68 |
| Mac | 0,89 | 0,76 |
| SSH | 0,90 | 0,51 |
| SMB | 0,89 | 0,13 |

> Un bon F1 global peut masquer un échec presque total sur un protocole nouveau.

---

## 33. Variation de débit

| Scénario | Accuracy | F1 | FPR | FNR |
| --- | ---: | ---: | ---: | ---: |
| Baseline | 0,95 | 0,87 | 0,04 | 0,12 |
| +10 % | 0,93 | 0,83 | 0,05 | 0,14 |
| +50 % | 0,93 | 0,83 | 0,05 | 0,11 |

Conclusion :

- variation de débit peu impactante ;
- nouveaux hôtes / protocoles beaucoup plus critiques.

---

## 34. Conclusion NIDS

Le principal défi n'est pas seulement :
> **détecter une attaque**

mais :
> **rester fiable quand le réseau réel évolue.**

Perspectives :

- benchmarks ;
- autres modèles ;
- online learning ;
- continual learning ;
- datasets réalistes ;
- explicabilité.

---

## 35. Glossaire express

| Terme | Définition |
| --- | --- |
| IA | Intelligence artificielle |
| CPS | Cyber-Physical System |
| NIDS | Network Intrusion Detection System |
| ML | Machine Learning |
| F1-score | Compromis précision / rappel |
| FPR | Taux de faux positifs |
| FNR | Taux de faux négatifs |
| MSE | Mean Squared Error |
| SOC | Security Operations Center |
| SIEM | Corrélation / supervision d'événements |
| EDR | Détection et réponse endpoint |
| TPM | Module matériel de confiance |
| BLERP | Bandwidth, Latency, Economics, Reliability, Privacy |
| CRA | Cyber Resilience Act |
| CSA | Cybersecurity Act |
| DORA | Digital Operational Resilience Act |
| NIS2 | Directive européenne cybersécurité |
| AI Act | Règlement européen IA |
| Data drift | Évolution des données par rapport à l'entraînement |
| Shadow AI | Usage IA hors gouvernance officielle |

---

## 36. Fil rouge de la journée

Les quatre conférences de l'après-midi racontent la même histoire sous quatre angles :

### 1. L'IA peut renforcer la cybersécurité

Elle peut :

- détecter ;
- corréler ;
- analyser ;
- prioriser ;
- automatiser.

### 2. L'IA devient elle-même une surface d'attaque

Elle peut être :

- trompée ;
- empoisonnée ;
- jailbreakée ;
- compromise ;
- volée.

### 3. La réglementation doit suivre

Il faut regarder :

- fournisseurs ;
- dépendances ;
- supply chain ;
- souveraineté ;
- hardware ;
- gouvernance.

### 4. Le monde réel évolue

Il faut surveiller :

- drift ;
- mises à jour ;
- nouveaux usages ;
- nouveaux hôtes ;
- nouveaux protocoles ;
- environnement physique.

---

## 37. Conclusion générale

> **La cybersécurité de l'IA relie données, modèles, logiciels, réseaux, matériel, humains, réglementation et souveraineté.**

L'enjeu n'est plus seulement de construire une IA performante.

Il faut construire une IA :

- **sécurisée** ;
- **robuste** ;
- **explicable** ;
- **gouvernée** ;
- **résiliente** ;
- **sûre dans le monde réel**.

Et inversement :

> **L'IA peut devenir un formidable outil de cybersécurité, à condition que l'outil lui-même soit protégé, surveillé et maîtrisé.**

---

## 38. PDF / présentations à intégrer

### Matin

- Présentation DGSI / Cyber-risques et ingérences

### Après-midi

- AI for security & security for AI — Kavé Salamatian
- Rethinking Cybersecurity Regulation in an Age of Uncertainty
- Evolution of Machine Learning Intrusion Detection Systems Resiliency to Network Traffic
- Secured and Safe Embedded Artificial Intelligence for Cyber-Physical Systems

---
