# 5.3 — Atelier 3 | Déterminer les premières actions de réponse

## 🎯 Objectif et modalités

Choisir des actions de réponse à l’incident en tenant compte du fonctionnement du processus industriel.

**Modalité :** étude de situation et décision en binôme, avec échanges collectifs. **Durée :** non précisée, à compléter.

!!! info "Proposition documentaire au 30 octobre 2026"
    Les décisions ci-dessous sont des **propositions à discuter et valider** avec l’exploitation, la maintenance et le formateur. Aucun accès n’est suspendu, aucun équipement isolé, aucune règle ni consigne modifiée pour cet atelier. Le dossier concerne un scénario fictif ; les traces analysées en 5.2 et les tests du PoC J4 restent des preuves distinctes.

## 1 — Point de départ pour décider

La [chronologie 5.2](analyser-traces-reconstituer-evenements.md) confirme, dans les sources du scénario, une écriture FC06 de **12 °C à 09:14 depuis MAINT-01**, hors de la fenêtre FM-426 connue ; aucune autorisation correspondante n’est fournie. Le compte partagé et la session VPN corrigée ne permettent pas d’identifier l’auteur humain ni de démontrer une compromission.

Le responsable a **autorisé le retour à 4 °C à 10:18** ; l’écriture corrective et sa réponse sont présentes à **10:21**, avec corroboration par SUP-01 et les mesures. L’alarme est effacée à 10:46 ; le dernier échantillon disponible est 4,18 °C à 11:30. **Ces événements historiques ne prouvent ni l’état actuel du site ni le devenir des produits.**

Deux points de vue doivent rester distincts :

- **Au moment de la réponse initiale :** lire l’état réel, décider avec l’exploitation des actions urgentes et du confinement.
- **Après lecture du dossier complet :** vérifier le retour à 4 °C déjà documenté, ses contrôles et les accès encore présents ; ne pas rejouer une écriture comme si elle n’avait pas eu lieu.

Le maintien en service de REG-02 sans correctif est une contrainte du scénario. Les protections J4 sont une architecture proposée, pas un état déployé supposé au moment des faits.

## 2 — Évaluer les huit actions possibles

[Télécharger la matrice des actions et décisions proposées — CSV](../../assets/files/informatique-industrielle/it-4/Montval-5.3-matrice-actions-reponse.csv).

| Action envisagée | Objectif | Effet attendu sur l’incident | Conséquences possibles sur l’exploitation | Vérifications préalables | Équipes à associer | Décision proposée / statut |
| --- | --- | --- | --- | --- | --- | --- |
| Déconnecter complètement REG-02 du réseau | Couper les chemins de commande et empêcher de nouvelles écritures réseau | Réduit l’exposition uniquement si aucun autre chemin ne subsiste | Perte de collecte, alarmes distantes et maintenance ; boucle locale attendue autonome mais dépendances à confirmer | Identifier liaison réseau distincte des E/S et de l’alimentation ; état local, relève sur place, chemins alternatifs, moyen de reprise | Exploitation + FrigoMaint/automaticien + IT | Dernier recours ciblé, pas première action automatique |
| Suspendre l’accès distant de FrigoMaint | Contenir un chemin d’accès suspect | Ferme les accès suspendus ; sessions déjà ouvertes à traiter explicitement | Peut empêcher le diagnostic et une intervention corrective urgente ; n’arrête pas nécessairement la régulation locale | Inventorier comptes/sessions dont compte partagé, destination, droits, urgence en cours et moyen de contact/intervention alternatif | IT accès distants + exploitation + FrigoMaint | Suspension ciblée à proposer avec chemin d’urgence ; pas d’attribution au prestataire |
| Bloquer les communications Modbus | Empêcher les commandes indésirables vers REG-02 | Un blocage TCP global empêche écritures et lectures | Perte de visibilité et de commande distante ; maintien du contrôle local à confirmer | Distinguer collecte autorisée, écriture corrective et accès suspect ; vérifier chemin, sessions établies, lecture seule réelle et retour arrière | IT réseau + exploitation + FrigoMaint/automaticien | Préférer contrôle ciblé et qualifié ; pas de blocage général par défaut |
| Redémarrer le régulateur | Reprendre un équipement défaillant si diagnostic le justifie | Effet sur cause inconnue ; peut ne rien corriger et effacer des traces volatiles | Interruption possible de la commande du froid ; paramètres et états au redémarrage inconnus | Justification, notice et comportement de reprise, alimentation/groupe, sauvegarde si possible, intervention autorisée, relève et contrôles | Exploitation autorise ; FrigoMaint/automaticien exécute ; IT coordonne | Non retenu en première intention pour un simple changement de consigne |
| Rétablir la consigne normale | Rétablir le fonctionnement attendu du froid | Corrige le paramètre sans supprimer le chemin qui a permis son changement | Effet thermique progressif ; limites des cycles du compresseur à respecter | Lire l’état actuel ; enregistrer avant/après, autorisation, identité technique et humaine documentée, paramètres exacts, retour mécanique et thermique | Exploitation + FrigoMaint/automaticien ; IT conserve les traces | Dans le dossier : accord 10:18 et retour 4 °C à 10:21 déjà documentés ; vérifier plutôt que réécrire |
| Isoler MAINT-01 | Réduire les possibilités d’émission du poste impliqué techniquement | Bloque son chemin s’il est effectivement isolé ; n’exclut pas d’autres origines | Peut supprimer l’outil de diagnostic et maintenance, affecter des sessions légitimes | Cartographier dépendances et connexions, préserver traces utiles, préparer poste/chemin alternatif validé ; ne pas éteindre ou réinstaller sans plan | IT poste/réseau + exploitation + FrigoMaint | À proposer de façon ciblée et coordonnée ; compromission non démontrée |
| Conserver les traces avant modification | Maintenir la possibilité d’analyser et de justifier les décisions | N’interrompt pas à elle seule l’incident mais conserve les preuves disponibles | Collecte intrusive ou longue susceptible de retarder une action nécessaire ; éviter surcharge du REG | Prioriser exports déjà accessibles, horloges brutes/corrigées, empreintes, provenance et accès limité ; ne pas retarder une urgence de protection | IT collecte dans son périmètre ; SUP/FrigoMaint fournissent leurs traces ; exploitation priorise | À poursuivre immédiatement en parallèle des vérifications de terrain |
| Renforcer la surveillance | Détecter nouvelles écritures, perte de visibilité et évolution thermique | Permet d’observer ; ne bloque pas à elle seule une action | Charge et volume des captures ; données périmées ou collecte arrêtée possibles | Choisir point de capture réel, collecte passive autorisée, débit/rétention, contrôle indépendant local et destinataire des alertes | IT + responsable SUP + exploitation + FrigoMaint | À proposer sans modifier la boucle locale ; nouvelles détections non testées |

**Décision directrice proposée :** préserver le contrôle frigorifique, limiter le chemin de commande suspect au périmètre nécessaire, conserver une consultation fiable et organiser un accès correctif maîtrisé. Si une aggravation exige une action immédiate de protection, la collecte ne doit pas la retarder : tracer la décision, l’autorité, les éléments disponibles avant action et la conséquence sur les preuves.

Suspendre un compte ou ajouter un refus pour de nouvelles connexions ne garantit pas la fermeture des sessions existantes. Examiner VPN, session distante du poste et connexions industrielles ; les interrompre de façon ciblée si la décision l’exige, en préservant les flux légitimes. Ne pas vider globalement le suivi des connexions ni ouvrir un accès général pour contourner le confinement.

## 3 — Distinguer les interventions IT et OT

| Question | Réponse pour Montval, avec référence au manuel |
| --- | --- |
| Une coupure réseau arrête-t-elle nécessairement la régulation ? | **Non selon EXP-01**, si régulateur, capteurs, alimentation et groupe restent fonctionnels. Cela ne garantit pas l’absence d’autres dépendances réelles : identifier précisément la liaison coupée et vérifier le contrôle local avec le mainteneur. Une coupure réseau n’est ni une coupure d’alimentation ni une coupure des E/S. |
| Une perte de supervision peut-elle masquer une nouvelle anomalie ? | **Oui** : perte d’actualisation, alarmes non consultables à distance, données potentiellement périmées. EXP-04/08 imposent fraîcheur et signalement ; prévoir relève locale et moyens d’alarme réellement disponibles. EXP-05/06 concernent historique et horodatage. |
| Quelles précautions avant redémarrage REG-02 ? | MAI-05/06 : diagnostic justifiant l’arrêt, décision de l’exploitation, notice et comportement de reprise, paramètres sauvegardés si possible, conséquences sur le compresseur et possibilité de retour arrière. MAI-08/EXP-11 : contrôle terrain, températures, commande, alarmes et supervision après action. La valeur du délai minimum entre démarrages n’est pas fournie ; ne pas l’inventer. |
| Comment rétablir une consigne sans perdre les preuves ? | Lire et dater l’état avant, conserver sources déjà accessibles et autorisation, effectuer une action ciblée validée, puis relire et tracer auteur, commande, réponse et effets. MAI-01/02 et EXP-02. Une écriture changera nécessairement l’état courant ; les exports antérieurs doivent rester conservés. Dans le dossier, le retour à 4 °C est déjà établi à 10:21. |
| Que faire si FrigoMaint doit intervenir pendant la suspension ? | Contacter exploitation et mainteneur ; privilégier intervention sur place ou moyen alternatif de confiance validé. Si un accès distant est indispensable, autorisation nominative, durée/cibles/opérations bornées, supervision de session et fermeture vérifiée. MAI-03/04 et ORG-01. Ne pas rouvrir le compte partagé ou MAINT-01 suspect sans justification et vérifications. Les capacités réelles du site restent à confirmer. |

Le filtre réseau classique IP/TCP ne sépare pas à lui seul les lectures des écritures Modbus. Si le chemin doit être strictement lecteur, utiliser un contrôle applicatif adapté et qualifié, puis vérifier l’absence de chemin direct. L’accès permettant la correction doit être distinct et expressément autorisé ; les capacités GW-02 proposées en J4 ne sont pas présumées installées.

## 4 — Proposition de réponse immédiate coordonnée

### A — Vérifications urgentes et coordination

1. **Exploitation et FrigoMaint vérifient l’état réel de ZF-02** : mesure indépendante si nécessaire, consigne et mode locaux, sonde, porte, groupe frigorifique, commandes et alarmes. Vérifier aussi si les autres zones sont concernées.
2. **L’exploitation traite les denrées** et choisit les mesures conservatoires selon ses procédures (EXP-12). L’équipe IT fournit durées et limites des traces ; elle ne décide pas seule de leur conformité à partir de la température d’enceinte.
3. **Nommer les interlocuteurs et ouvrir un journal de décision** : incident, heure/fuseau, demandeur, exécutant, autorisation, objectif, effet prévu, conditions d’arrêt et contrôles attendus. Confirmer les moyens de communication même si l’accès distant est suspendu.

### B — Limiter l’incident sans supprimer les fonctions nécessaires

- Identifier les sessions encore actives, les droits et chemins vers REG-02 ; préserver leurs traces accessibles.
- Soumettre à décision le confinement **du chemin MAINT-01/compte concerné**, avec maintien de la collecte et du diagnostic local. L’implication technique de MAINT-01 justifie des vérifications ; elle n’établit pas sa compromission.
- Faire valider les conséquences avant d’isoler le poste ou REG-02. Si le seul moyen disponible supprime toute supervision, mettre en place une relève sur place et convenir de la durée acceptable, sans inventer une durée garantie par le manuel.
- Prévoir l’intervention urgente par un chemin contrôlé ou sur place. Tester le flux autorisé et les refus après tout changement de filtre, avec retour arrière ciblé s’il dégrade une fonction nécessaire.

### C — Maintenir ou rétablir le froid

Lire la consigne actuelle. **Si elle est déjà à 4 °C, ne pas réécrire pour le seul exercice.** Vérifier l’efficacité du retour documenté et l’absence de nouveaux changements. Si une consigne anormale persiste ou réapparaît, l’exploitation et FrigoMaint décident d’une correction traçable sur le chemin autorisé, après préservation proportionnée des éléments disponibles. Surveiller l’effet progressif et le comportement du compresseur selon sa notice.

Éviter le redémarrage non justifié : il peut interrompre la commande et effacer des états sans retirer la cause du changement de consigne. Si un arrêt devient indispensable, il relève d’un plan coordonné avec relève du froid et vérification de reprise.

### D — Conserver et surveiller

| Élément à préserver ou à obtenir | Condition de collecte et état actuel |
| --- | --- |
| Sept sources reçues et SHA-256 | Déjà archivées dans le mémo ; garder les originaux et travailler sur copies. Les empreintes assurent la référence reçue, pas l’authenticité historique. |
| États REG-02 et configuration pertinente | À obtenir avec FrigoMaint ; privilégier consultation/documentation disponible, sans interrogation intrusive non qualifiée du régulateur obsolète. |
| Sessions VPN, droits et règles actives | À exporter avec dates, fuseaux et périmètre ; conserver aussi les heures brutes et la correction VPN −2 min 10 s. |
| Traces MAINT-01 | Sessions, processus/outils, journaux, configuration et éléments volatils pertinents, par personnel compétent ; ne pas redémarrer/réinstaller pour simplifier l’analyse. |
| Tickets et décisions | FM-426, INC-881, demandes éventuelles manquantes, appels et validations ; séparer déclaration et preuve technique. |
| Trafic et mesures après action | Capture passive au point utile, volume maîtrisé, début/fin et filtre enregistrés ; relever aussi fraîcheur des mesures et observations locales. La surveillance proposée n’est pas un nouveau test réalisé. |

## 5 — Contrôles de retour à une situation maîtrisée

| Contrôle à faire valider | Critère proposé / preuve attendue | État dans ce dossier |
| --- | --- | --- |
| Fonctionnement local | Mesure indépendante et états capteur/groupe/commande cohérents, vérifiés sur place par le mainteneur. | Les mesures exportées ne suffisent pas ; contrôle terrain à confirmer. |
| Paramètres et évolutions | Consigne nominale 4 °C, mode prévu, absence de nouveau changement inexpliqué ; tendance et cycles suivis sur une durée convenue avec FrigoMaint. | Retour historique à 4 °C et baisse documentés ; état actuel et durée de suivi à établir. |
| Supervision et alarmes | Mesures fraîches et horodatées, alarmes visibles, voie locale vérifiée, acquittement distingué de correction. | Événements historiques disponibles ; remise en service complète non certifiée. |
| Confinement ciblé | Chemin non autorisé refusé, collecte nécessaire maintenue, session retirée effectivement close ; relevés avant/après et accès d’urgence testé si prévu. | Aucune nouvelle mesure appliquée en 5.3. |
| Traçabilité | Actions, autorisations, sources, heures et résultats conservés ; limites explicites. | Analyse et archives disponibles ; validations opérationnelles à recueillir. |
| Produits et décision d’exploitation | Responsable d’exploitation statue selon procédures et données nécessaires. | Aucune décision sur les denrées fournie. |

Les critères sont proposés pour discussion ; aucun délai de surveillance, seuil de libération des produits ou automatisme de reprise non documenté n’est ajouté. Le service n’est pas déclaré rétabli sur le seul retour d’un écran, d’une connexion ou d’une consigne nominale.

## 6 — Débrief collectif : périmètre AIS et responsabilités OT

| Domaine | Contribution d’un administrateur AIS dans son périmètre autorisé | Intervention / validation complémentaire |
| --- | --- | --- |
| Preuves et chronologie | Export des journaux IT, empreintes, horloges, analyse réseau, tenue du journal d’action. | SUP/FrigoMaint pour leurs traces ; exploitation pour la compréhension terrain. |
| Confinement réseau et accès | Proposer puis appliquer les restrictions validées, fermeture ciblée des sessions, contrôles positifs/négatifs, retour arrière. | Exploitation et mainteneur valident les fonctions à préserver ; responsabilités d’administration à confirmer. |
| Diagnostic du froid et réglages | Fournir les données et vérifier le chemin technique ; ne pas déduire un état mécanique d’un bit réseau. | FrigoMaint/automaticien : diagnostic, modification de paramètres/contrôle et notice ; exploitation autorise. |
| Redémarrage ou intervention sur REG-02 | Préparer impacts IT et collecte, sans redémarrage autonome du régulateur. | Exploitation, maintenance et automaticien organisent l’arrêt et la remise en service. |
| Gestion des produits et continuité magasin | Fournir les faits et leurs limites ; maintenir les services sous sa responsabilité. | Exploitation décide du traitement des denrées et des procédures d’urgence. |

**À discuter avec le formateur :** une coupure totale trop rapide peut réduire la visibilité et retarder une correction ; une suspension incomplète peut laisser une session active ; une réouverture générale peut recréer l’exposition ; une collecte trop lente peut retarder la protection des denrées. Pour chaque décision, vérifier à la fois ce qu’elle limite et ce qu’elle empêche de faire.

### Décision courte à présenter

**Proposition non exécutée :** vérifier le froid et les produits avec l’exploitation/FrigoMaint, préserver les traces accessibles en parallèle, puis restreindre les accès et écritures non nécessaires par une mesure ciblée validée. Garder la consultation et une possibilité d’intervention maîtrisée. Vérifier le retour à 4 °C déjà documenté ; ne corriger de nouveau que si l’état actuel le justifie. Ne pas redémarrer REG-02 sans diagnostic et plan de reprise. Confirmer le fonctionnement sur place, les accès réellement fermés et la traçabilité avant toute clôture.

## Ressources et état final de l’atelier

- [Manuel MAN-OT-01](../it-2/MAN-OT-01_Manuel_exploitation_installation_frigorifique.md) : EXP-01/02/04–12, MAI-01–08, ORG-01/02.
- [Analyse et chronologie 5.2](analyser-traces-reconstituer-evenements.md) ; [protection REG-02 proposée en J4](../it-3/proteger-regulateur-industriel-obsolete.md).
- Pour la méthode de préservation : conserver provenance, personne ayant collecté, date/fuseau et empreintes ; ces principes sont décrits par l’[ASD/ACSC — Incident response planning, evidence collection and preservation](https://www.cyber.gov.au/publication/cyber-security-incident-response-planning-practitioner-guidance). Ce complément méthodologique ne remplace pas les exigences du manuel Montval.

**Production préparée :** matrice de huit actions, proposition coordonnée, preuves à conserver, contrôles et responsabilités. **À compléter après débrief :** décisions retenues/refusées, responsables, autorisations, conditions d’exécution et résultats éventuels. Aucun accord collectif ni action technique n’est présenté comme déjà obtenu ou réalisé.

[Retour à l’itération 4](index.md) · [Pense-bête](../../pense-bete/glossaire/informatique-industrielle/it-4.md).
