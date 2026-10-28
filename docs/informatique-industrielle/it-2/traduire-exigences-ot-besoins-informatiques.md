# 3.2 — Atelier 2 | Traduire les exigences OT en besoins informatiques

## 🎯 Objectif et modalités

Déduire les besoins de l’infrastructure IT à partir des exigences opérationnelles de Montval.

- **Modalité :** analyse technique individuelle ou en binôme, en autonomie.
- **Durée :** à compléter ; non précisée dans la consigne.
- **Support :** MAN-OT-01, version 1.0 du 14 octobre 2022, sections 3 à 6 et 8.

Le formateur n’est pas présent pendant cette séance. S’appuyer sur les ressources fournies et l’entraide du groupe.

!!! info "Portée de l’analyse"
    Les exigences sont issues du [manuel Montval](MAN-OT-01_Manuel_exploitation_installation_frigorifique.md). Les besoins IT sont déduits de ces exigences ; les solutions sont des propositions à instruire. Aucun produit, coût ou déploiement n’est retenu ici. Une information absente du manuel n’est pas un défaut de sécurité confirmé. Aucun essai d’intervention ni validation collective n’est attesté.

## 1 — Étudier les dépendances informatiques

Partir de la fonction à préserver, puis identifier ce qui pourrait l’interrompre ou la rendre invisible. Une exigence peut concerner plusieurs domaines :

| Domaine | Dépendance et question à examiner pour Montval |
| --- | --- |
| Architecture réseau | Quels chemins relient SUP-01 aux trois régulateurs et OPS-01 à la supervision ? Quelles écritures sont nécessaires à MAINT-01 ? |
| Administration des systèmes | Un redémarrage, un service d’initialisation ou une configuration restaurée peut-il modifier une consigne ? |
| Supervision | Les données périmées sont-elles reconnues ? L’exploitation conserve-t-elle un moyen local de surveiller les zones ? |
| Temps et conservation | Comment rapprocher mesures, alarmes, autorisations et interventions ? Comment conserver les données attendues pendant 90 jours ? |
| Sauvegarde et restauration | Quels éléments permettent de restaurer SUP-01, son historique et ses réglages sans écraser les consignes locales ? |
| Maintenance | Qui autorise, ouvre, utilise et ferme l’accès distant, y compris en urgence ? |
| Mises à jour | Quel service ou régulateur s’arrête, pendant combien de temps, et avec quels contrôles de remise en service ? |

La régulation locale doit fonctionner sans SUP-01 et OPS-01 si ses composants restent opérationnels (**EXP-01**). Cela ne dispense pas d’identifier les dépendances physiques et les services communs réels avant une intervention.

## 2 — Matrice OT → IT renseignée

Les huit références demandées sont complétées par six exigences utiles à l’exploitation informatique. Les solutions ci-dessous restent envisageables, sous réserve des capacités des équipements et de l’accord des responsables.

| Référence OT | Besoin ou contrainte IT | Solution ou principe technique envisageable | Information à confirmer |
| --- | --- | --- | --- |
| **EXP-01**, §3.1 | Préserver le contrôle local pendant la maintenance IT. | Séparer les dépendances de la boucle locale des services de supervision ; cartographier alimentations et communications ; organiser la surveillance locale pendant l’arrêt de SUP-01. | Dépendances réelles des régulateurs, alimentations et équipements partagés ; conséquences d’une coupure réseau. |
| **EXP-04**, §3.2 ; §2.3 | Afficher les états utiles et leur fraîcheur ; rafraîchissement nominal souhaité de 5 s. | Horodater les mesures, afficher leur âge ou un état périmé, détecter la perte de communication ; vérifier le rafraîchissement sans surcharger les régulateurs. | Capacités de collecte, nombre de variables, seuil de péremption acceptable et origine des horodatages. |
| **EXP-05**, §3.2 | Conserver au moins une température/minute, changements de consigne, alarmes et acquittements pendant 90 jours. | Dimensionner stockage et rétention, surveiller la collecte et l’espace ; sauvegarder données et configuration ; examiner un tampon de collecte si disponible. | Volume réel, taille des événements, tampon local éventuel, sauvegardes, pertes de données et délais de restauration acceptables. |
| **EXP-06**, §3.2 | Permettre une chronologie cohérente des incidents. | Définir une référence horaire et un service de synchronisation compatible, par exemple NTP pour les systèmes qui le supportent ; surveiller les écarts et documenter fuseaux et sources d’heure. | Précision nécessaire, support des régulateurs, comportement sans source d’heure et chemins autorisés. Le manuel ne choisit pas de protocole. |
| **EXP-10**, §4 | Récupérer les états courants après retour de SUP-01 sans modifier les paramètres locaux. | Reprise par lecture ; désactiver ou maîtriser les écritures d’initialisation ; tester une restauration en environnement d’essai. | Comportement du logiciel au démarrage, cache de consignes, scripts et ordre de lancement des services. |
| **MAI-01**, §5.1 | Réserver les écritures aux interventions expressément autorisées. | Séparer consultation et administration ; comptes nominatifs et droits limités sur les systèmes compatibles ; contrôler les chemins d’écriture et l’ouverture des sessions de maintenance. | Authentification disponible, fonctions réellement requises, filtrage possible, autorité d’approbation et accès existants. |
| **MAI-05**, §5.3 | Préparer les changements selon leur effet sur l’exploitation. | Fiche de changement : périmètre, impacts, sauvegarde vérifiée, essai, critères de réussite et retour arrière si réalisable ; validation conjointe. | Configuration de référence, environnement d’essai, restauration possible, durée et procédure de retour arrière. |
| **MAI-07**, §5.3 | Évaluer les correctifs avec le mainteneur avant déploiement. | Inventaire des versions, suivi des avis, qualification de compatibilité ; planification selon l’effet sur le froid ; mesures temporaires de réduction d’exposition si le déploiement est différé. | Compatibilité fournisseur, arrêt nécessaire, remplacement éventuel, conséquences du report et validation du programme. |
| **EXP-08**, §3.3 | Garder un signalement local sans SUP-01 et identifier zone/heure sur OPS-01. | Vérifier indépendance de l’avertissement local ; procédure de relève ; recette de transmission et de présentation des alarmes. | Moyens locaux, alimentation, génération et acheminement des alarmes, organisation de leur prise en charge. |
| **EXP-11**, §4 | Vérifier l’état réel des zones après une panne. | Liste de contrôles de reprise : mesures locales, commandes, alarmes, consignes et fraîcheur des données ; validation par l’exploitation. | Intervenant disponible sur place, moyen de mesure indépendant et procédure détaillée. |
| **MAI-02**, §5.1 | Rattacher chaque changement à son motif, son autorisation, son heure et sa vérification. | Registre d’intervention relié aux traces de session et aux événements de supervision ; contrôle avant/après des valeurs. | Journaux disponibles et attribution de l’identité humaine : le seul échange Modbus ne fournit pas toute la traçabilité demandée. |
| **MAI-03–04**, §5.2 | Accès distant pendant les interventions et possibilité d’urgence, sans dépendance permanente de la régulation. | Accès activable sur autorisation et limité aux cibles nécessaires ; passerelle d’accès ou bastion envisageable ; procédure d’astreinte, fermeture en fin d’intervention. | Configuration actuelle, contacts et moyens d’ouverture hors horaires, durée de session et portée justifiée sur les trois régulateurs. |
| **MAI-06, MAI-08**, §5.3 | Planifier les interruptions et contrôler la remise en service. | Préparer la fenêtre avec exploitation/FrigoMaint, surveillance compensatoire et recette des températures, commandes, alarmes et consignes. | Mardi 06 h–08 h à confirmer ; durée d’interruption acceptable ; ce créneau n’autorise pas une coupure de froid. |
| **ORG-01–02**, §6 | Coordonner changements et diagnostic entre exploitation, maintenance et IT. | Désigner approbateur et contacts ; partager fonctions à préserver, plan de vérification et modalités d’escalade. | Responsabilités opérationnelles, disponibilité, délégations et contrats applicables. |

**Dimensionnement initial de l’historique :** pour les seules températures des trois zones, à une valeur/minute pendant 90 jours, prévoir au minimum **3 × 60 × 24 × 90 = 388 800 valeurs**, hors métadonnées, événements, index, marges et sauvegardes. Ce nombre ne constitue pas un dimensionnement en octets ni une politique de sauvegarde.

Une rétention de 90 jours ne fixe pas la perte de données admissible ni le délai de reprise. Un stockage redondant ne remplace pas une sauvegarde restaurable ; un éventuel tampon ne permet de récupérer un trou d’historique que si sa présence et son fonctionnement sont confirmés.

## 3 — Précautions avant et après six opérations IT

Les opérations restent envisageables ; leur autorisation dépend de leurs conséquences sur Montval. Une vérification après changement doit porter sur le procédé et les fonctions utiles, au-delà du seul état des services informatiques.

| Opération | Avant l’opération | Après l’opération | Références |
| --- | --- | --- | --- |
| **1. Redémarrer SUP-01** | Identifier les services partagés et la collecte interrompue ; coordonner la surveillance locale ; préserver données et configuration ; vérifier que le démarrage n’écrit pas de consigne. Faire autoriser l’impact sur l’exploitation. | Vérifier lecture des états courants, fraîcheur, consignes inchangées, alarmes et reprise de collecte ; identifier les lacunes d’historique ; faire confirmer l’état réel des zones. | EXP-01, 03–05, 08, 10–11 ; MAI-05, 08 ; ORG-01. |
| **2. Modifier une règle de pare-feu** | Identifier sources, destinations, sens, protocoles et fonctions nécessaires ; sauvegarder la règle ; préparer un retour arrière et un accès d’administration préservé ; coordonner la modification. | Tester les lectures, alarmes, horodatage et accès autorisés ; vérifier les refus attendus et les journaux sans lancer d’écritures inutiles ; confirmer données fraîches et contrôle local intact. | EXP-01, 04, 06, 08 ; MAI-01, 03, 05, 08. |
| **3. Interrompre un réseau** | Déterminer ce qui utilise le segment, y compris les services partagés ; vérifier que la boucle locale n’est pas interrompue ; prévoir contrôle sur place, durée, collecte et alarmes pendant la coupure ; planifier et autoriser. | Confirmer retour des échanges et des états courants sans écrasement des paramètres ; vérifier chaque zone, les alarmes, l’horodatage et la reprise d’historique ; déclarer les pertes non récupérables. | EXP-01, 04–06, 08, 10–11 ; MAI-05–06, 08. |
| **4. Appliquer une mise à jour système** | Préciser la cible : SUP-01, OPS-01 ou infrastructure commune ; vérifier compatibilité, redémarrage et dépendances ; préparer sauvegarde/restauration et essais avec responsable supervision, exploitation et mainteneur. Un correctif régulateur demande une qualification spécifique. | Vérifier services et communications, collecte, affichage, consignes, alarmes et contrôles locaux concernés ; consigner version et résultat de recette ; déclencher le retour arrière selon les critères prévus. | MAI-05–08 ; EXP-03–06, 10–11 ; ORG-01. |
| **5. Restaurer une sauvegarde** | Définir périmètre et date ; vérifier intégrité, compatibilité et procédure ; identifier paramètres ou comptes anciens et risque d’écrasement de données récentes ; tester si possible hors production ; autoriser l’impact. | Comparer configuration restaurée et référence attendue ; lire les consignes locales sans les remplacer aveuglément ; vérifier droits, temps, alarmes, historique et état des trois zones ; consigner les pertes de données. | EXP-02–06, 10–11 ; MAI-01–02, 05, 08. |
| **6. Désactiver un compte ou accès de maintenance** | Identifier son titulaire, ses usages, sessions et dépendances ; vérifier qu’il ne sert pas aussi de compte technique de collecte ; coordonner fin d’intervention et solution d’urgence autorisée. En cas de suspicion d’abus, décider du confinement avec les responsables concernés. | Vérifier que l’accès visé est bien bloqué et traiter les sessions déjà ouvertes selon le mécanisme ; confirmer continuité de lecture/régulation, traces et possibilité d’une future intervention autorisée. | MAI-01–04, 08 ; ORG-01–02. |

**Particularité OT :** une opération IT peut interrompre la visibilité sans arrêter le froid, ou toucher une dépendance du contrôle et affecter une zone. Les paramètres, alarmes, températures et moyens de surveillance doivent donc entrer dans les critères de réussite. Le retour d’un écran ne suffit pas (**EXP-11**).

## 4 — Cinq informations à obtenir avant intervention

Sélection fondée sur la section 8 du manuel. Les interlocuteurs sont proposés selon leurs responsabilités (§6) ; l’existence et la qualité des documents restent à confirmer.

| Information à obtenir | Pourquoi elle est nécessaire | Interlocuteurs proposés | Décision technique influencée |
| --- | --- | --- | --- |
| **1. Topologie, adressage et dépendances de SUP-01/OPS-01/MAINT-01** | Délimiter ce qui sera affecté par une coupure, une règle ou un redémarrage ; identifier les services communs. | Équipe IT et responsable supervision, avec FrigoMaint pour les liaisons terrain. | Périmètre de maintenance, règles de flux, isolation des dépendances et surveillance de remplacement. |
| **2. Notices et configurations des régulateurs, avec table complète des registres** | Connaître réactions aux défauts et redémarrages, accès lecture/écriture et paramètres à préserver ; éviter de réutiliser les adresses du PoC. | FrigoMaint, avec documentation fournisseur. | Commandes autorisées, méthode de vérification, durée d’arrêt, compatibilité du correctif et retour arrière possible. |
| **3. Configuration des accès distants et responsabilités d’administration** | Savoir qui peut atteindre quelles cibles, comment une session s’ouvre/se ferme et quelles traces existent. | IT, FrigoMaint et responsable d’exploitation pour autorisation/astreinte. | Périmètre des accès, contrôle des écritures, procédure d’urgence et éventuel bastion ; besoin réel d’accès aux trois régulateurs. |
| **4. Sauvegardes exploitables et procédure de restauration de SUP-01 et des configurations REG** | Évaluer la capacité de reprise et le risque de réinjecter d’anciens paramètres ou de perdre l’historique. | Responsable supervision et IT ; FrigoMaint pour les régulateurs ; exploitation pour les objectifs de reprise. | Faisabilité du changement, sauvegarde préalable, tests de restauration, perte acceptable et durée de maintenance. |
| **5. Procédures de reprise/urgence, contacts et niveaux de service applicables** | Savoir qui contrôle les zones, autorise l’arrêt, décide pour les denrées et intervient hors horaires ; ne pas inventer de durée d’interruption acceptable. | Responsable d’exploitation et FrigoMaint, avec IT pour les engagements sur les services. | Fenêtre confirmée, surveillance locale, escalade, critères de remise en service et décision de reporter l’intervention. |

**Absence documentaire ≠ vulnérabilité établie.** Par exemple, la section 8 ne fournit pas la procédure de restauration ; cela justifie une demande de preuve, pas l’affirmation « aucune sauvegarde n’existe ».

## Production et état attendu

Conserver la matrice OT → IT, le tableau avant/après et les cinq demandes d’information avec leurs références. Présenter les solutions comme des options jusqu’à confirmation des capacités et dépendances. La présente fiche constitue une **analyse documentaire renseignée**, pas un compte rendu d’intervention ou une architecture déjà déployée. La confrontation collective reste à effectuer.

## Ressources

- [Manuel MAN-OT-01](MAN-OT-01_Manuel_exploitation_installation_frigorifique.md), sections 3 à 6 et 8 ; §2 pour les composants et communications.
- [3.1 — Analyse des exigences OT](analyser-exigences-exploitation-ot.md).
- Réseaux, systèmes et administration Linux : mobiliser les compétences déjà acquises en cartographie, filtrage, services, journaux, temps et restauration selon les systèmes réellement présents ; aucun système Linux en production à Montval n’est identifié par le manuel.

[Retour à l’itération 2](index.md) · [Pense-bête](../../pense-bete/glossaire/informatique-industrielle/it-2.md)
