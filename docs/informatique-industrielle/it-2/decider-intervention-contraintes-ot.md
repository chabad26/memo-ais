# 3.6 — Atelier 6 | Décider d’une intervention en tenant compte des contraintes OT

## 🎯 Objectif et modalités

Analyser des demandes d’intervention informatique et déterminer les conditions techniques nécessaires pour préserver le fonctionnement de l’installation.

- **Modalité :** étude en binôme et échanges avec le formateur.
- **Support :** MAN-OT-01, section 7 ; exigences des sections 3 à 6 et informations manquantes de la section 8.

!!! info "Statut des décisions"
    Réponses techniques proposées à partir du manuel **v1.0 du 14 octobre 2022**. Les situations sont ouvertes dans le scénario : aucune autorisation, intervention, restauration ou validation collective n’est attestée. Les actions « immédiates » ci-dessous sont des propositions de préparation ou de constat sans modification du contrôle. Cette fiche n’est ni une analyse de risques formelle ni un dossier de conformité réglementaire.

!!! note "Évolution du scénario en J4"
    SIT-03 ci-dessous traite l’annonce d’un correctif dans le scénario J3. La [nouvelle fiche REG-02 de l’atelier 4.3](../it-3/proteger-regulateur-industriel-obsolete.md) indique ensuite une fin de support sans nouveau correctif et sans remplacement financé cette année. Les protections compensatoires remplacent donc l’option de déploiement d’un correctif pour ce nouvel état ; le dossier J3 reste la trace de l’analyse antérieure.

## 1 — Identifier les enjeux des quatre demandes

| Situation | Composants et fonctions concernés | Exigences principales | Informations nécessaires et participants à la décision |
| --- | --- | --- | --- |
| **SIT-01 — Redémarrer SUP-01 pour mise à jour**, éventuellement en heures d’ouverture. | SUP-01, OPS-01, collecte des trois REG, affichage, historique et alarmes centrales ; régulation locale à préserver. | **EXP-01, EXP-03–06, EXP-08, EXP-10–11 ; MAI-05–08 ; ORG-01–02.** | Dépendances réelles, durée, compatibilité, comportement au redémarrage, sauvegardes et moyen local de surveillance. Décision : exploitation, IT et responsable supervision ; FrigoMaint pour confirmer les effets sur le contrôle et la relève locale. |
| **SIT-02 — Accès distant permanent FrigoMaint aux trois REG**, avec urgence hors horaires. | MAINT-01, chemins d’accès, REG-01 à REG-03, consignes et traces ; DMZ/bastion dans la cible proposée. | **EXP-02, EXP-06 ; MAI-01–04, MAI-08 ; ORG-01–02.** | Accès actuels, opérations utiles, cibles, identité, outils, journalisation, astreinte et ouverture/fermeture. Décision : exploitation, FrigoMaint et IT ; responsable supervision si SUP-01 fait partie des cibles. |
| **SIT-03 — Correctif de REG-02 avec redémarrage**. | REG-02 et boucle de ZF-02, capteur, groupe, alarmes locales ; collecte SUP-01/OPS-01. ZF-01/03 à préserver si indépendantes. | **EXP-01–03, EXP-07–08, EXP-11–12 ; MAI-05–08 ; ORG-01–02.** | Notice, compatibilité, sauvegarde de configuration/programme, état après redémarrage, retour arrière ou remplacement, durée totale et surveillance/prise en charge des denrées. Décision : exploitation et FrigoMaint, fournisseur pour la qualification ; IT et responsable supervision pour les dépendances et contrôles associés. |
| **SIT-04 — Trou d’historique après panne de SUP-01**. | Historique SUP-01, collecte, journaux, horloges, éventuels tampons des REG et traces de maintenance. | **EXP-04–06, EXP-10–12 ; MAI-02, MAI-05 si correction ; ORG-02.** | Bornes du trou, sources réellement enregistrées, horodatages, sauvegardes, intégrité et mécanisme de rattrapage. Décision : exploitation, responsable supervision et IT ; FrigoMaint pour les données locales et les interventions pendant la panne. |

## 2 — Réponses techniques par situation

### SIT-01 — Mise à jour et redémarrage de la supervision

**Proposition : réalisable sous conditions, sans autoriser d’emblée l’opération pendant l’ouverture.** Le manuel exige la continuité du contrôle local en l’absence de SUP-01 si les composants locaux sont opérationnels (**EXP-01**). Il ne garantit pas que tout redémarrage soit sans conséquence : affichage, collecte et signalement central peuvent être interrompus, et les dépendances communes restent inconnues.

| Étape | Réponse proposée |
| --- | --- |
| **Préparer immédiatement** | Relever version et cible de la mise à jour, services/dépendances, état des trois zones et consignes ; informer les responsables et préparer le changement. Consulter les journaux sans modifier la configuration. |
| **Vérifier avant intervention** | Compatibilité et durée estimée ; sauvegarde exploitable de la configuration et des données ; procédure de retour arrière si possible ; absence d’écritures de consignes au redémarrage ; moyens de surveillance locale et pertes de collecte acceptables. Vérifier tout tampon au lieu de supposer son existence. |
| **Coordonner** | Faire approuver la fenêtre et les impacts par l’exploitation avec IT/responsable supervision, et FrigoMaint selon les contrôles locaux nécessaires. Prévoir qui relève températures et avertissements pendant l’arrêt. Le mardi 06 h–08 h est un créneau privilégié **à confirmer**, pas une autorisation automatique ni une obligation d’intervention en heures d’ouverture. |
| **Après intervention** | Contrôler les trois zones, la reprise des lectures courantes, les horodatages, la fraîcheur, consignes inchangées, commandes et alarmes ; vérifier collecte/historique et consigner les lacunes. Documenter version, durée et résultat de recette (**MAI-08**). |
| **Reporter si** | Dépendances ou effets du redémarrage non maîtrisés ; relève locale indisponible ; absence de moyen de reprise adapté ; mise à jour non qualifiée ; dérive de température ou absence d’accord de l’exploitation. Si une urgence impose un autre arbitrage, la faire décider explicitement par les responsables concernés. |

**Inconnues restantes :** système et logiciel SUP-01, durée d’arrêt, dépendances IT, sauvegardes, capacités de rattrapage, tolérance à l’interruption et validation de la fenêtre.

### SIT-02 — Demande d’accès distant permanent du prestataire

**Proposition : ne pas ouvrir par défaut un accès permanent général aux trois régulateurs.** Traduire la demande de rapidité en une capacité d’intervention autorisée, y compris urgente. **MAI-03** exige l’accès distant lors des interventions, sans le rendre nécessaire à la régulation permanente. La disponibilité d’un point d’entrée contrôlé peut être permanente sans qu’une session ou un droit d’écriture le soit.

| Étape | Réponse proposée |
| --- | --- |
| **Préparer immédiatement** | Faire préciser diagnostic, écritures, régulateurs réellement nécessaires, plages et urgences ; inventorier les accès déjà présents et les responsables. Enregistrer la demande, sans ouvrir un nouveau chemin. |
| **Vérifier avant ouverture** | Comptes et identité de l’intervenant, compatibilité de l’outil, séparation lecture/écriture, cibles et fonctions, moyens d’ouverture/fermeture, traces et horodatage. Confirmer les contrôles possibles sur les REG : le seul protocole Modbus ne fournit pas une attribution humaine complète. |
| **Coordonner** | Exploitation autorise l’intervention et le périmètre ; FrigoMaint fournit le besoin et les outils ; IT met en œuvre le chemin convenu. Prévoir astreinte, délégation d’autorisation, lien disponible et solution de recours sur place en cas d’indisponibilité distante. |
| **Chemin envisagé** | MAINT-01 → point d’entrée sécurisé → **bastion en DMZ proposé** → outil/cibles autorisés. Une session de consultation n’autorise pas une modification. Chaque changement de consigne porte motif, autorisation, heure et vérification (**EXP-02, MAI-01–02**). DMZ/bastion ne sont pas attestés comme déployés. |
| **Après intervention / lors de la recette d’accès** | Vérifier accès aux seules cibles autorisées, refus des opérations non accordées, traces et rattachement à l’intervention ; contrôler températures, consignes, commandes et alarmes ; fermer droits temporaires et sessions selon le mécanisme retenu. Tester la procédure d’urgence et sa fermeture dans un cadre convenu. |
| **Reporter l’ouverture si** | Identité, cible, droit d’écriture, autorité ou traçabilité indéterminés ; outillage incompatible ; urgence hors horaires sans procédure praticable. Une urgence ne justifie pas un contournement non autorisé du dispositif. |

**Inconnues restantes :** mécanismes actuels, capacité d’attribution des actions, implantation/gestion de MAINT-01, protocoles, portée utile sur les trois REG et organisation effective de l’astreinte.

### SIT-03 — Correctif de sécurité sur REG-02

**Proposition : préparer le correctif avec FrigoMaint et planifier l’interruption de ZF-02 avant déploiement.** Le régulateur exécute la boucle locale ; son redémarrage peut interrompre directement la commande et le signalement de la zone. Les **45 minutes annoncées par le fournisseur sont hors validation fonctionnelle** : elles ne fixent ni la durée totale d’intervention ni la durée tolérable sans froid.

| Étape | Réponse proposée |
| --- | --- |
| **Préparer immédiatement** | Recueillir l’avis fournisseur, les versions et le périmètre exact du correctif ; relever l’état de ZF-02, consigne et configuration ; faire évaluer urgence de sécurité et effet d’un report avec le mainteneur et l’exploitation. Aucun redémarrage immédiat proposé. |
| **Vérifier avant intervention** | Compatibilité matériel/programme, sauvegarde exploitable, méthode d’installation et état des sorties après redémarrage ; retour arrière ou remplacement disponible si réalisable ; test sur équipement/environnement représentatif lorsque possible. Vérifier dépendances avec les autres zones et durée de recette. |
| **Coordonner** | Exploitation et FrigoMaint décident de la fenêtre et des dispositions pour maintenir des conditions acceptables : surveillance indépendante, éventuel transfert des produits selon procédure, technicien sur place si nécessaire. IT/responsable supervision préparent les contrôles réseau et remontées d’états. |
| **Après intervention** | Vérifier programme/version, configuration et consigne, mesure par un moyen approprié, commandes et cycles selon la notice, protection contre redémarrages trop rapprochés, alarmes locales/centrales et échanges avec SUP-01. Observer le retour à un état d’exploitation acceptable ; ne pas tester une alarme en exposant des denrées. Vérifier ZF-01/03 si elles pouvaient être affectées. |
| **Reporter le déploiement si** | Compatibilité ou état des sorties inconnu, pas de plan de reprise adapté, durée globale non compatible avec l’exploitation, surveillance ou prise en charge des produits impossible, accord ou mainteneur indisponible. Le report doit rester tracé et réévalué ; étudier des restrictions d’accès compatibles pendant l’attente si le risque de sécurité le justifie. |

**Inconnues restantes :** nature/urgence du correctif, notice de REG-02, comportement au redémarrage, valeur du délai minimum entre démarrages, durée de vérification et retour arrière possible. La conformité des denrées relève de l’exploitation (**EXP-12**).

### SIT-04 — Historique incomplet après interruption de supervision

**Proposition : rechercher une reconstitution fondée sur des données existantes, sans promettre de combler le trou.** Les valeurs normales après reprise ne prouvent pas l’absence d’excursion pendant la panne. Le fonctionnement des régulateurs ne prouve pas non plus qu’ils ont stocké les températures.

| Étape | Réponse proposée |
| --- | --- |
| **Préparer immédiatement** | Délimiter l’intervalle manquant, conserver exports et journaux disponibles avant rotation/écrasement, relever horloges et changements d’heure, consigner les informations des opérateurs et interventions connues. Ne pas écraser l’historique actuel pour tenter une récupération. |
| **Vérifier avant récupération** | Existence, granularité, intégrité et dates d’éventuels tampons REG/collecteurs, copies de base, sauvegardes, journaux d’alarmes/consignes et traces de maintenance. Vérifier les écarts temporels entre sources. Une sauvegarde ne contient que les données effectivement acquises avant sa création. |
| **Coordonner** | Responsable supervision et IT examinent stockage/collecte ; FrigoMaint recherche les données locales et traces d’intervention ; exploitation précise événements, relevés locaux et décisions concernant les produits. |
| **Récupération envisageable** | Analyser les copies en environnement isolé ; reconstituer une chronologie avec source, horodatage et niveau de certitude. Si des mesures authentiques couvrent le trou, tester leur rapprochement et leur import sans altérer les données courantes. Séparer mesures, témoignages et déductions ; ne pas fabriquer des points interpolés présentés comme enregistrés. |
| **Après récupération ou correction** | Vérifier couverture, doublons, ordre temporel, unités et origine des données ; comparer avant/après import et conserver les lacunes restantes. Vérifier reprise de collecte, alerte de péremption et conservation de 90 jours ; tester un éventuel mécanisme de rattrapage en laboratoire ou sous conditions convenues. |
| **Reporter une restauration/import si** | Intégrité, horodatage, compatibilité ou risque d’écrasement non maîtrisés ; pas de sauvegarde de l’état courant ni de retour arrière adapté. Ne pas reporter la conservation des preuves ni le signalement : si aucune source ne couvre la période, déclarer la reconstitution impossible pour ces mesures. |

**Inconnues restantes :** bornes précises du trou, sources réellement conservées et leur couverture, capacité des REG, sauvegardes, cohérence des horloges et cause de la perte. Aucune vulnérabilité ou action malveillante ne se déduit à elle seule d’un historique incomplet.

## 3 — Comparer les traitements

### SIT-01 / SIT-03 — Deux redémarrages, deux fonctions touchées

| Point | SUP-01 (SIT-01) | REG-02 (SIT-03) |
| --- | --- | --- |
| Fonction directement interrompue | Supervision, collecte et historique central des trois zones. | Régulation/commande locale de ZF-02, selon comportement matériel et configuration. |
| Continuité attendue | Régulateurs opérationnels maintiennent leurs boucles (**EXP-01**), sous réserve des dépendances communes. | Pas de maintien de la régulation par REG-02 pendant son indisponibilité ; aucune reprise automatique par SUP-01 n’est documentée. |
| Contrôle décisif de reprise | Lire les états courants sans écraser les paramètres (**EXP-10**), vérifier visibilité et collecte. | Vérifier programme, paramètres, mesure, sorties et fonctionnement physique de la zone, pas seulement la présence réseau. |
| Durée à considérer | Arrêt, redémarrage et vérification ; estimation à obtenir. | 45 minutes annoncées **plus** préparation et validation ; durée de coupure réelle à qualifier. |

Le périmètre d’un serveur partagé peut être large, même sans commande directe d’automate. Le redémarrage de REG-02 peut toucher une seule zone plus directement, si les autres restent indépendantes. Dans les deux cas, l’exploitation participe à la décision et vérifie le service réel (**EXP-11**, **MAI-05–08**).

### SIT-02 / SIT-04 — Accès, traçabilité et reconstitution

Un accès distant attribué à une identité et rattaché à une intervention aide à savoir **qui a fait quoi, sur quelle cible, avec quelle autorisation et à quelle heure** (**MAI-02**, **EXP-06**). Les journaux du bastion proposé, de l’outil de maintenance et de SUP-01 peuvent se compléter ; leur présence, leur précision et leur conservation doivent être confirmées. Un simple compte partagé ou un échange réseau ne garantit pas une attribution humaine.

Les traces de maintenance peuvent éclairer un changement de consigne pendant la panne de SUP-01, mais **ne remplacent pas les températures manquantes**. Inversement, une courbe de température ne suffit pas à attribuer un changement à une personne. Une reconstitution exploitable rapproche mesures, alarmes, consignes et interventions avec leurs limites temporelles. L’absence de trace ne prouve ni absence d’intervention ni absence d’incident.

## 4 — Synthèse : quatre décisions courtes proposées

| Situation | Décision technique proposée | Conditions et vérifications clés | Non confirmé |
| --- | --- | --- | --- |
| **SIT-01** | Autoriser seulement après préparation un redémarrage SUP-01 dans une fenêtre approuvée ; l’ouverture du magasin n’est ni une interdiction ni une autorisation automatique. | Contrôle local préservé, surveillance locale, sauvegarde/reprise ; relire états courants, vérifier consignes, alarmes et historique. | Durée, compatibilité, dépendances, tampon et accord d’exploitation. |
| **SIT-02** | Proposer un accès distant contrôlé, activable en urgence et limité à l’intervention ; ne pas ouvrir par défaut une écriture permanente sur trois REG. | Identité, autorisation, cibles/droits, bastion/DMZ proposés, traces et fermeture ; recette du parcours normal/urgent. | Accès existant, protocoles, compatibilité des outils et astreinte. |
| **SIT-03** | Planifier le correctif REG-02 avec exploitation et mainteneur, après qualification et préparation de l’interruption. | Reprise adaptée, produits/surveillance pris en charge ; recette du programme, paramètres, commandes, alarmes et état thermique. | 45 min hors validation, durée totale et interruption tolérable, comportement après reboot et retour arrière. |
| **SIT-04** | Préserver et analyser les sources ; récupérer uniquement ce qui peut être attesté ; déclarer explicitement les périodes non reconstructibles. | Analyse isolée, horodatages contrôlés, pas d’écrasement ; vérifier couverture et collecte après correction/import. | Sources couvrant le trou, intégrité, capacités de rattrapage et cause de la perte. |

**Production préparée :** analyse des quatre situations et quatre décisions techniques courtes. À confronter en binôme et avec le formateur ; noter l’autorité, la date, les conditions retenues et les vérifications réellement effectuées si une décision est prise. Aucun accord ou résultat d’intervention n’est prérempli.

## Ressources

- [Manuel Montval MAN-OT-01](MAN-OT-01_Manuel_exploitation_installation_frigorifique.md), section 7 pour les situations, sections 3 à 6 pour les exigences et section 8 pour les inconnues.
- [3.2 — Besoins IT et précautions](traduire-exigences-ot-besoins-informatiques.md), [3.4 — Débrief](mettre-en-commun-exigences-consequences-it.md), [3.5 — Architecture et flux proposés](concevoir-architecture-it-ot-montval.md).

[Retour à l’itération 2](index.md) · [Pense-bête](../../pense-bete/glossaire/informatique-industrielle/it-2.md)
