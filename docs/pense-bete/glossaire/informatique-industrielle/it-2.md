# Informatique industrielle — Itération 2 : Spécificités de l’OT

## J3 — Exigences d’exploitation de Montval

Source : **MAN-OT-01 v1.0, 14 octobre 2022**, sections 1 à 6, scénario fictif. Analyse documentaire renseignée ; fonctionnement réel et restitution collective non attestés.

- Trois zones ZF-01 à ZF-03 ; régulateurs REG-01 à REG-03, sondes, contacts de porte, groupes et avertisseurs locaux. Consigne nominale **+4 °C**.
- **EXP-01–03 :** contrôle local maintenu sans SUP-01/OPS-01 si composants locaux opérationnels ; consignes conservées localement ; redémarrage supervision sans imposer de consigne.
- **EXP-04–06 :** température horodatée et données périmées identifiables ; au moins une valeur/minute, événements de consigne/alarme/acquittement, **90 jours** de conservation ; chronologie cohérente. Rafraîchissement écran souhaité **5 s**, sans contrainte temps réel sur le contrôle.
- **EXP-07–09 :** alarme après **10 minutes à T > +8 °C**, signalement local disponible sans SUP-01 ; acquittement sans effet sur la commande. Le PoC utilise **10 secondes**, pas Montval.
- **EXP-10–12 :** reprise sur états courants sans changer les paramètres ; vérifier physiquement les zones ; décisions sur les denrées par l’exploitation.
- **MAI-01–04 :** écritures autorisées et tracées ; accès distant lors d’interventions, sans nécessité permanente pour la régulation ; urgence sollicitée par l’exploitation.
- **MAI-05–08 :** impact, vérifications et retour arrière si réalisable ; coordination exploitation/FrigoMaint ; mardi **06 h–08 h à confirmer**, sans autorisation automatique de coupure ; correctifs évalués et recette fonctionnelle.
- **ORG-01–02 :** accord sur fonctions à préserver et vérifications ; signalement à exploitation/maintenance, et IT pour réseau/supervision.
- Défaut capteur : comportement de sortie **à confirmer dans la notice**, pas d’arrêt automatique universel. Délai minimum entre démarrages prévu mais valeur inconnue.
- Restent inconnus : topologie/IP, table complète des registres, configurations d’accès, sauvegardes et tampons, notices et procédures détaillées. Le PoC J1–J2 ne démontre pas leur mise en œuvre.

[3.1 — Analyse et matrice](../../../informatique-industrielle/it-2/analyser-exigences-exploitation-ot.md) · [Manuel fourni](../../../informatique-industrielle/it-2/MAN-OT-01_Manuel_exploitation_installation_frigorifique.md) · [Sommaire J3](../../../informatique-industrielle/it-2/index.md)

## 3.2 — OT → IT

- Exigence documentaire → besoin IT → option technique → information à confirmer. Une option n’est pas une configuration déjà présente.
- Avant : dépendances, autorisation, impact, surveillance locale, sauvegarde et retour arrière si possible. Après : états courants, consignes, températures, commandes, alarmes, fraîcheur et historique.
- EXP-05 : **388 800 valeurs de température minimum** pour trois zones, une valeur/minute, 90 jours ; hors événements, métadonnées et sauvegardes. La rétention ne fixe ni délai de reprise ni perte admissible.
- EXP-10 : restaurer ou redémarrer SUP-01 ne doit pas écraser les paramètres locaux. EXP-11 : vérifier les zones, pas seulement le réseau.
- Cinq demandes : topologie/dépendances ; notices/configurations/registres ; accès distants/responsabilités ; sauvegardes/restauration ; reprise/urgence/contrats.
- Absence de document dans le manuel ≠ absence de protection confirmée. Aucun choix de produit ou coût demandé.

[3.2 — Matrice et tableaux renseignés](../../../informatique-industrielle/it-2/traduire-exigences-ot-besoins-informatiques.md).

## 3.3 — Purdue et cible d’entreprise

- N0 : zones, sondes, contacts et groupes ; N1 : REG ; N2 : SUP/OPS ; N3 : fonction historique de SUP, sans serveur supplémentaire.
- N4 : EXP-IT ; FrigoMaint/MAINT-01 hors OT. Placement selon les fonctions, pas selon le nom ou la forme de l’équipement.
- **N3.5 / DMZ et bastion proposés** : extérieur ou administration IT → accès contrôlé → bastion → cibles autorisées. Filtrage aux frontières ; accès de maintenance distinct de la collecte normale.
- Modbus TCP documenté entre SUP et REG. Liaison terrain, protocole OPS/SUP, accès distant, administration et adresses/ports : à confirmer. Ne pas recopier les ports du PoC.
- Collecte périodique et historique utiles en exploitation ; écritures et accès de maintenance seulement sur autorisation. EXP-01 et MAI-03 : régulation indépendante de la supervision et de l’accès distant sous les conditions locales prévues.
- Un niveau Purdue n’impose pas un VLAN ; une DMZ dessinée ne démontre pas une segmentation déployée.

[3.3 — Schéma, source draw.io, flux et réponses](../../../informatique-industrielle/it-2/organiser-installation-modele-purdue.md).

## 3.4 — Débrief exigences / conséquences IT

- Comparer le texte de l’exigence, le besoin IT déduit, les options et les informations manquantes ; ne pas confondre option et décision collective.
- Points communs : contrôle local autonome sous conditions ; supervision fraîche ; historique 90 jours ; alarmes et chronologie ; accès autorisés/tracés ; changements coordonnés.
- SUP-01 porte plusieurs fonctions : placement N2/N3 à justifier sans inventer deux serveurs. DMZ et bastion restent une cible proposée.
- Conserver les flux F0–F6 et compléter les services associés quand leurs dépendances sont connues. Ni VLAN par niveau imposé, ni protocole absent à inventer.
- Tracer en séance : retours du groupe/formateur, décision, justification, vérification et responsable. Ces éléments ne sont pas encore attestés.

[3.4 — Support de débrief et tableau à compléter](../../../informatique-industrielle/it-2/mettre-en-commun-exigences-consequences-it.md).

## 3.5 — Architecture de référence pour J4

- Zones proposées : contrôle local ; supervision/conduite ; services OT de temps/sauvegarde ; DMZ avec accès distant et bastion ; IT magasin ; prestataire externe. SUP-01 porte aussi l’historique.
- Matrice : C00–C03 (terrain, collecte, consultation/acquittement, historique), A01–A05 (accès, bastion, administration et maintenance), S01–S04 (temps, sauvegarde/restauration, temps REG si compatible).
- Distinguer consultation, acquittement et écriture de consigne/configuration. Les capacités de filtrage applicatif et des REG doivent être confirmées.
- Aucun protocole OPS/SUP, administration ou sauvegarde imposé ; Modbus TCP est documenté, pas les ports/adresses réels. Le schéma illustre une sauvegarde poussée ; sens définitif à choisir.
- Pannes à analyser : IT, SUP, lien REG-02, accès urgent, temps. Contrôle local maintenu sous EXP-01 ; données périmées visibles sous EXP-04 ; chronologie sous EXP-06 ; reprise sans écrasement sous EXP-10 ; accès distant non permanent pour réguler sous MAI-03.
- Services OT et DMZ dessinés ≠ autonomie mesurée : vérifier alimentations, identités, réseau et services communs. Recette J4 proposée, non exécutée.

[3.5 — Schéma et dossier de conception](../../../informatique-industrielle/it-2/concevoir-architecture-it-ot-montval.md).

## 3.6 — Décider d’une intervention

- **SIT-01 / SUP-01 :** redémarrage conditionné à la maîtrise des dépendances, surveillance locale et reprise ; ne pas écraser les consignes. Perte possible de vue, collecte et historique des trois zones.
- **SIT-02 / accès distant :** distinguer disponibilité du point d’entrée et droit/session permanente ; urgence autorisée, cibles limitées, traces et fermeture. DMZ/bastion toujours proposés.
- **SIT-03 / REG-02 :** interruption possible de la boucle ZF-02 ; **45 minutes fournisseur hors validation**, pas une durée tolérable de coupure du froid. Mainteneur, qualification, reprise et protection des produits à organiser.
- **SIT-04 / historique :** préserver les sources et leurs temps, analyser sur copies ; aucune température inventée. Valeurs normales après panne ≠ absence d’excursion pendant la panne. Sans source couvrant le trou, reconstitution des mesures impossible.
- Traces d’accès et autorisations aident à attribuer une intervention ; elles ne remplacent pas les mesures. Les horodatages doivent être rapprochés avec leurs incertitudes.
- Décisions proposées, sans intervention ni accord collectif attestés ; cadre technique, pas analyse de risques formelle ou dossier réglementaire.

[3.6 — Situations et quatre décisions techniques](../../../informatique-industrielle/it-2/decider-intervention-contraintes-ot.md).

## 3.7 — Dossier de validation C3

[Fiche 3.7](../../../informatique-industrielle/it-2/finaliser-dossier-analyse-it-ot.md) et [PDF formateur — 12 pages](../../../assets/files/informatique-industrielle/it-2/J3-analyse-exigences-architecture-IT-OT-Olivier-HIMBLOT.pdf).

- Titre : `J3-analyse-exigences-architecture-IT-OT`. Matrice OT → IT, Purdue, architecture/flux et quatre décisions d’intervention dans un document unique.
- C3 : dépendances techniques, traduction des exigences, cartographie et justification des communications/conditions d’intervention.
- Exigences du manuel, inconnues et propositions séparées. PDF constitué ≠ approbation du formateur ou déploiement de la cible.
- Deux schémas en A3 ; autres pages A4 paysage ; sources draw.io et dossier Markdown conservés.
- Avant J4 : confirmer adresses, ports, capacités, droits et dépendances ; préparer essais et recette. Convention `[Nom]-[Prénom]-[Site]-Iteration2-Atelier7`, site à confirmer.
