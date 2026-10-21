# Qualifier le risque et choisir une mesure

**30 min — Présentiel**

## Le concept

Qualifier un risque consiste à décrire un événement redouté, puis à apprécier sa **gravité** et sa **vraisemblance** dans un contexte précis. Le statut « shadow IA » ne suffit pas à déterminer son niveau. Cette fiche traite les étapes **6. Qualification** et **7. Mesure** de la [méthode d'analyse](shadow-ia-de-quoi-parle-t-on.md).

### Échelles de l'exercice

| Niveau | Gravité | Vraisemblance — repères de la consigne |
| --- | --- | --- |
| **1** | Mineure : aucune donnée C2/C3, impact négligeable | Peu vraisemblable : usage ponctuel, compte professionnel avec garanties |
| **2** | Significative : données C1 ou quelques données C2, impact interne | Vraisemblable : usage occasionnel ou garanties partielles |
| **3** | Grave : C2 en volume, données personnelles, impact client ou réglementaire | Très vraisemblable : usage régulier, compte personnel, données conservées par le fournisseur |
| **4** | Critique : secrets donnant accès au SI, C3, capacité d'agir sur le SI | Quasi certain : usage quotidien ou automatisé, données déjà exposées, accès permanent |

Ces repères guident la cotation sans remplacer le raisonnement : un usage quotidien ne rend pas toute attaque quasi certaine, et un compte personnel ne démontre pas une exploitation. Pour chaque cas, préciser **quel événement est coté**, les hypothèses et les informations manquantes. Les scores ci-dessous sont des estimations pédagogiques initiales, sans fréquence statistique mesurée.

**Risque = gravité × vraisemblance.** La multiplication et les seuils sont ceux de cet exercice ; ils ne constituent pas à eux seuls une analyse EBIOS Risk Manager complète. L'ANSSI présente une méthode en cinq ateliers, avec scénarios, traitement et suivi des risques résiduels. [ANSSI — EBIOS Risk Manager](https://cyber.gouv.fr/securisation/analyse-des-risques/methode-ebios-rm/), consulté le **20 octobre 2026**.

| Gravité ↓ / Vraisemblance → | **1** | **2** | **3** | **4** |
| --- | --- | --- | --- | --- |
| **1** | 1 — Faible | 2 — Faible | 3 — Faible | 4 — Modéré |
| **2** | 2 — Faible | 4 — Modéré | 6 — Modéré | 8 — Élevé |
| **3** | 3 — Faible | 6 — Modéré | 9 — Élevé | 12 — Critique |
| **4** | 4 — Modéré | 8 — Élevé | 12 — Critique | 16 — Critique |

**Seuils :** 1–3 faible ; 4–6 modéré ; 8–9 élevé ; 12–16 critique. Les produits 7, 10, 11, 13, 14 et 15 sont impossibles avec deux entiers de 1 à 4.

## Choisir une mesure

| Option | Principe | Exemple adapté à Hexalp |
| --- | --- | --- |
| **Remplacer** | Fournir une solution validée qui couvre le besoin | Assistant professionnel administré par Hexalp et validé pour les données concernées |
| **Réduire** | Limiter techniquement l'exposition ou les capacités | Filtrer les secrets, limiter les droits OAuth et les destinations réseau |
| **Encadrer** | Organiser les pratiques et la décision | Circuit de validation, formation et délai suivi pour les demandes de dérogation |
| **Accepter** | Décider explicitement de conserver un risque justifié | Usage local délimité, après validation et examen des risques ; décision écrite du responsable habilité, avec échéance de revue |
| **Interdire** | Écarter un usage incompatible avec les exigences et fournir une autre voie | Interdire les secrets dans les prompts ; dépanner avec un extrait minimisé ou un outil interne autorisé |

Ces options peuvent se combiner. Une offre entreprise ne rend pas tous les contenus acceptables. Une acceptation de risque ne vaut pas dérogation automatique à la PSSI : suivre la procédure applicable. Les interdictions explicites de la PSSI restent applicables, même pendant la recherche d'une alternative.

## Mission — Trois usages qualifiés

### 1. Cotation initiale et besoin métier

Les deux premiers cas sont **contrefactuels imposés par la mission** : on suppose l'envoi de Thomas depuis un compte personnel et l'acceptation d'InboxPilot. Cela ne transforme pas ces événements en faits observés dans les activités précédentes. Le troisième cas reprend la **situation 5 de 2.2 : modèle local hors ligne pour relire du code**.

| Usage et événement redouté | Gravité | Vraisemblance | Niveau et justification en une ligne | Besoin métier |
| --- | --- | --- | --- | --- |
| **Thomas : perte de maîtrise de secrets et de données WMS envoyés à un assistant externe depuis un compte personnel** | **4 — Critique** | **4 — Quasi certain pour l'exposition supposée** | **4 × 4 = 16 — Critique** : les secrets C3 figurent dans l'extrait et leur envoi hors du cadre autorisé est posé par l'énoncé ; leur exploitation n'est pas démontrée. | Comprendre les timeouts nocturnes du WMS et rétablir un service fiable |
| **InboxPilot accepté : lecture/divulgation ou actions non désirées à la suite d'un détournement de l'assistant** | **4 — Critique** | **3 — Très vraisemblable, hypothèse prudente à confirmer** | **4 × 3 = 12 — Critique** : droits de lecture, écriture et envoi, avec renouvellement d'accès ; aucun contrôle humain ni dispositif de sécurité n'est documenté, mais le détournement n'est pas certain. | Résumer les mails et préparer les réponses commerciales |
| **Modèle local hors ligne : altération du code après intégration d'une suggestion erronée** | **2 — Significative** | **2 — Vraisemblable** | **2 × 2 = 4 — Modéré** : hypothèse d'un poste de développement isolé de la production, sans secrets accessibles ; erreurs de code possibles et garanties de revue non précisées. | Accélérer la relecture du code et aider le développeur à repérer des problèmes |

**Justification des hypothèses :** pour InboxPilot, la cote 3 est un jugement conservateur fondé sur les capacités accordées et les garanties inconnues, pas une statistique de réussite d'injection. Une cote 4 nécessiterait un événement mieux établi que le simple consentement. Pour le modèle local, l'isolement de la production et l'absence de secrets sont des **hypothèses ajoutées**, pas des faits de 2.2 : s'ils ne sont pas confirmés, il faut recoter. Une dépendance malveillante exécutée avec des droits élevés ou une modification de code critique pourrait rendre ce cas beaucoup plus grave.

### 2. Mesures et continuité du travail

| Usage | Mesure technique proposée | Mesure organisationnelle proposée | Option(s) | La personne peut-elle encore travailler ? |
| --- | --- | --- | --- | --- |
| **Thomas** | Révoquer/renouveler les secrets exposés, examiner leurs traces d'usage ; pour les futures demandes, utiliser un extrait minimisé avec détection de secrets avant transmission à un outil validé pour ce contenu | Signaler à Nadia selon **8.1**, qualifier l'étendue de l'exposition et organiser une procédure de dépannage sans données clients ni secrets ; rappeler **2.3, 5.2 et 5.5** | **Réduire + remplacer + encadrer** ; interdire les secrets dans les prompts | **Oui** : il conserve horaires relatifs, erreurs et rôles des services dans l'[extrait caviardé de 2.4](quelles-donnees-sont-envoyees.md) ; les investigations sensibles restent dans le SI avec les outils de diagnostic habituels |
| **InboxPilot** | Révoquer les consentements/jetons accordés et vérifier les accès ; proposer un outil approuvé avec `Mail.Read` seulement si nécessaire, sans accès fichiers/calendrier ni envoi. Réponse préparée en texte puis envoyée manuellement | Évaluer fournisseur, contrat, données et conservation ; mettre en place une approbation DSI des connecteurs, une revue des droits et un suivi des demandes. Si une fonction d'action est autorisée plus tard, imposer sa validation humaine hors du modèle | **Réduire + remplacer + encadrer** | **Oui**, après mise à disposition du périmètre validé : résumé et proposition de réponse restent possibles sans `Mail.Send`. En attendant, traitement manuel dans Outlook ; aucun connecteur non validé n'est nécessaire |
| **Modèle local** | Valider modèle, moteur et dépendances ; limiter l'exécution à un environnement sans secrets ni accès production, vérifier l'absence de flux sortants et soumettre les changements de code à des tests avant intégration | Faire instruire l'installation selon **4.1** et le traitement du code C2 selon **2.3** ; définir les dépôts autorisés et imposer une revue humaine avant fusion. Documenter ensuite la décision sur le risque résiduel | **Réduire + encadrer**, puis **accepter** uniquement par décision habilitée si justifié | **Oui** : assistance à la relecture dans le périmètre approuvé ; tant que la validation manque, revue humaine et outils du catalogue DSI |

Les mesures de réaction sont proposées **dans les hypothèses de la mission**. Aucune clé n'a été révoquée, aucun tenant inspecté et aucun modèle installé pour cette fiche. Révoquer l'accès d'un connecteur ne supprime pas les copies déjà reçues par son fournisseur ; le traitement de ces données doit être vérifié séparément.

### 3. Comment vérifier l'efficacité des mesures ?

| Cas | Responsable opérationnel proposé | Preuves à rechercher avant réévaluation |
| --- | --- | --- |
| **Thomas** | Nadia pour le suivi d'incident ; administrateurs des secrets et équipe WMS pour les actions techniques | Révocation confirmée sans recopier le secret, examen des accès sur la période, périmètre des données envoyées, extrait minimisé revu et validation du service de remplacement |
| **InboxPilot** | Administrateur identité/M365 et DSI ; DPO pour l'exigence contractuelle applicable aux données personnelles | Consentements retirés, sessions/jetons traités et accès contrôlés ; liste des droits réellement accordés au nouvel outil et compte rendu du test fonctionnel avec données fictives |
| **Modèle local** | Responsable développement et DSI | Installation validée, provenance des composants, restrictions effectives de droits et de réseau, absence de secrets dans le contexte, revue et résultats des tests du code |

**Le risque résiduel reste à évaluer après vérification de ces preuves.** Un plan écrit ne démontre pas une baisse de vraisemblance ; il ne faut pas annoncer un passage automatique de « critique » à « faible ». Pour les données déjà sorties, les mesures préventives ne suppriment pas l'exposition passée.

## Un même outil peut-il présenter deux niveaux de risque différents ?

**Oui : le risque dépend de l'usage, des données, des droits et des garanties, pas seulement du nom de l'outil.**

| Même assistant, deux usages hypothétiques | Cotation avec l'échelle de l'exercice | Pourquoi le niveau change |
| --- | --- | --- |
| Reformuler ponctuellement une offre d'emploi déjà publique, sans connecteur, dans un espace professionnel validé | **G1 × V1 = 1 — Faible** | Contenu C0, absence de secret et d'action sur le SI ; une personne relit avant publication |
| Lui envoyer depuis un compte personnel le `.env` contenant les secrets de production du kit | **G4 × V4 = 16 — Critique pour l'exposition supposée** | Contenu C3 et exposition externe posée par le scénario ; l'exploitation ultérieure demeure une autre question |

Même dans le premier cas, « faible » ne veut pas dire absence de règle ou d'erreur possible. Inversement, un outil validé ne rend pas acceptable l'envoi de secrets interdit par la PSSI.

## Ressources et portée du travail

- [ANSSI — La méthode EBIOS Risk Manager](https://cyber.gouv.fr/securisation/analyse-des-risques/methode-ebios-rm/) : référence méthodologique ; le présent exercice ne remplace pas ses cinq ateliers.
- [ANSSI — Développer la confiance dans l'IA par une approche par les risques cyber](https://messervices.cyber.gouv.fr/guides/developper-la-confiance-dans-lia-par-une-approche-par-les-risques-cyber) : ressource pour approfondir l'analyse des risques des systèmes d'IA.
- [PSSI Hexalp et rattachements de 2.6](ce-que-dit-la-pssi.md) ; [permissions InboxPilot en 2.5](connecteurs-quand-ia-a-les-cles.md).

Sources externes consultées le **20 octobre 2026**. Les échelles, seuils et options proviennent de la consigne ; les trois cotations sont des propositions argumentées pour les scénarios fictifs, pas des résultats d'audit ni des décisions d'acceptation déjà prises.

[Retour à l'itération 2](index.md)
