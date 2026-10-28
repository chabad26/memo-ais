# 3.4 — Atelier 4 | Mettre en commun les exigences et leurs conséquences IT

## 🎯 Objectif et modalités

Confronter les analyses réalisées en autonomie et identifier les besoins techniques à prendre en compte dans la conception d’une infrastructure IT/OT.

**Modalité :** débrief collectif avec le formateur. S’appuyer sur les matrices 3.1–3.2 et le schéma Purdue 3.3.

!!! info "Statut du support"
    Les points de comparaison ci-dessous sont préparés à partir du manuel Montval **MAN-OT-01 v1.0 du 14 octobre 2022** et des fiches de la matinée. Ils ne constituent pas un compte rendu de séance. Les propositions des autres participants, arbitrages du formateur et décisions collectives restent à renseigner.

## 1 — Comparer les analyses

Présenter une exigence avec sa référence, ses conséquences IT et les hypothèses de la solution proposée. Une différence de proposition peut être justifiée ; une divergence sur l’exigence doit être rapprochée du texte source.

| Thème | Socle documentaire commun | Questions à confronter dans les matrices |
| --- | --- | --- |
| Continuité du contrôle local | **EXP-01–03** : régulation locale maintenue sans SUP-01/OPS-01 si composants locaux opérationnels ; consignes conservées localement et non imposées au redémarrage de SUP-01. | Quelles dépendances communes pourraient toucher les régulateurs ? Le redémarrage IT préserve-t-il effectivement leurs paramètres ? |
| Disponibilité de la supervision | **EXP-04, EXP-10–11** : informations horodatées et péremption visible ; reprise sur états courants ; contrôle réel des zones après panne. | Quelle surveillance pendant l’arrêt ? Quels délais d’indisponibilité acceptables ? Ne pas confondre affichage rétabli et procédé vérifié. |
| Conservation des historiques | **EXP-05** : au moins une température/minute, changements de consigne, alarmes et acquittements, pendant **90 jours**. | Comment dimensionner, sauvegarder et restaurer ? Existe-t-il un tampon permettant de récupérer une interruption de collecte ? Rétention et perte admissible sont-elles distinguées ? |
| Alarmes et horodatage | **EXP-06–09** : chronologie cohérente, alarme après **10 minutes à T > +8 °C**, zone/heure affichées, avertissement local, acquittement sans effet sur le contrôle. | Où sont générées les alarmes ? Comment détecter une donnée périmée et maintenir le signalement local ? Quelle précision temporelle et quels moyens de synchronisation ? |
| Accès de maintenance | **MAI-01–04** : écritures autorisées et tracées ; accès distant pendant les interventions ; urgence organisée par l’exploitation. | Quelle cible, quel droit et quelle durée ? Comment ouvrir/fermer l’accès et assurer l’astreinte ? L’accès permanent demandé par le prestataire n’est pas une nécessité de la régulation. |
| Changements et mises à jour | **MAI-05–08, ORG-01–02** : impact, vérification, retour arrière si réalisable, planification et recette avec les responsables. | Compatibilité, durée, sauvegarde et surveillance compensatoire sont-elles connues ? Le mardi 06 h–08 h reste à confirmer et n’autorise pas automatiquement une coupure. |

### Différences à examiner explicitement

- **Montval / PoC :** alarme après 10 minutes dans le manuel, 10 secondes dans le PoC. Réaction Montval au défaut capteur à confirmer dans la notice ; ne pas généraliser l’arrêt du PoC.
- **Panne de SUP-01 / panne locale :** la première peut supprimer visibilité et collecte ; la seconde peut supprimer la régulation de la zone. Une panne commune d’alimentation ou d’infrastructure exige une analyse distincte.
- **Historique / sauvegarde / tampon :** l’historique répond au suivi ; la sauvegarde permet une restauration selon son périmètre ; le tampon peut éventuellement récupérer des mesures. Aucun ne garantit à lui seul la présence de toutes les données manquantes.
- **Besoin / choix de produit :** une exigence de traçabilité ne désigne pas automatiquement un bastion particulier ; une chronologie cohérente ne fixe pas à elle seule le service de temps à déployer.

## 2 — Distinguer exigences et solutions

Les variantes suivantes sont des options de discussion. Leur pertinence dépend des équipements, de l’exploitation et des informations complémentaires du §8 du manuel.

| Besoin de l’exploitation | Conséquence pour l’IT | Solutions ou principes possibles | À vérifier avant de choisir |
| --- | --- | --- | --- |
| **EXP-01 :** maintien du contrôle local. | La maintenance de la supervision doit éviter d’affecter les dépendances de la boucle locale. | Préserver les communications terrain ; limiter les dépendances partagées ; séparer les périmètres de maintenance ; organiser une surveillance locale. | Topologie, câblage, alimentation, services communs et comportement de reprise des régulateurs. |
| **EXP-04 :** information opérateur fraîche et identifiable. | Détecter défaut de collecte et données périmées. | Date de mesure et âge affichés ; état de communication ; seuil de péremption validé ; contrôle du rafraîchissement. | Origine de l’heure, capacités du logiciel, délai acceptable et charge de lecture sur les régulateurs. |
| **EXP-05 :** historique conservé 90 jours. | Capacité, collecte, protection des données et restauration adaptées. | Stockage dimensionné et rétention contrôlée ; sauvegarde/restauration testée ; tampon local ou de collecte si compatible. | Volume, source de rattrapage éventuelle, objectifs de reprise et perte de données acceptable. Ne pas promettre de reconstituer un trou sans source. |
| **EXP-06 :** chronologie exploitable. | Horloges suffisamment cohérentes et écarts maîtrisés. | Référence horaire interne ; synchronisation des systèmes compatibles ; documentation de l’origine des horodatages et surveillance des écarts. | Précision nécessaire, protocoles supportés, autonomie et comportement en perte de référence. |
| **EXP-10 :** reprise de la supervision sans changement des paramètres. | Éviter l’écrasement des consignes locales par un état mémorisé ou une sauvegarde ancienne. | Reprise par lecture ; maîtrise des écritures d’initialisation ; test du redémarrage et de la restauration. | Comportement de l’application, scripts, configuration et version restaurée ; recette des valeurs avant/après. |
| **MAI-01–03 :** maintenance autorisée et attribuable. | Limiter les écritures et rattacher l’action à l’intervention. | DMZ et bastion proposés ; comptes et droits adaptés ; accès activé pour l’intervention ; registre d’autorisation et traces de session. Autres mécanismes possibles si les mêmes besoins sont démontrés. | Méthodes supportées, accès actuels, outils de maintenance, cibles nécessaires et organisation de l’urgence. |
| **MAI-05, MAI-07 :** changement maîtrisé et correctifs évalués. | Préparer compatibilité, interruption et vérifications sans automatisme de déploiement. | Essai sur environnement représentatif, sauvegarde de configuration, plan de retour arrière si possible et fenêtre validée ; traitement du risque pendant un report. | Avis fournisseur, arrêt nécessaire, état matériel, moyens d’essai et conséquences sur le froid. |

**Méthode de comparaison :** demander quelle exigence justifie chaque option, quelles hypothèses elle ajoute et comment on vérifiera le résultat. Une option plus complexe n’est pas automatiquement mieux adaptée. L’absence d’une information dans le manuel appelle une demande, pas un constat de vulnérabilité.

## 3 — Comparer les architectures Purdue

Présenter le [schéma de la matinée](organiser-installation-modele-purdue.md#2-schema-fonctionnel-et-cible-dentreprise) et sa [source draw.io](../../assets/files/informatique-industrielle/it-2/Montval-Purdue-cible.drawio). Les placements suivants constituent la proposition de l’apprenant, à confronter aux autres schémas.

| Placement proposé | Justification et discussion |
| --- | --- |
| N0 : ZF-01 à ZF-03, sondes, contacts et groupes | Procédé et interaction physique. Le détail des liaisons terrain reste à obtenir. |
| N1 : REG-01 à REG-03 | Régulation locale et commande, indépendantes de la supervision sous les conditions d’EXP-01. |
| N2 : SUP-01 et OPS-01 | Supervision/conduite. La vue opérateur ne remplace pas la boucle locale. |
| N3 : fonction d’historisation de SUP-01 | Fonction de suivi à l’échelle du site portée par le même serveur. Un schéma plaçant le serveur au niveau 3 peut se discuter s’il conserve son rôle de supervision et ses communications. Ne pas inventer deux actifs pour représenter deux fonctions. |
| N3.5 : DMZ et bastion **proposés** | Cible d’entreprise retenue dans notre dessin pour médiatiser les accès extérieurs et l’administration IT ; déploiement non attesté. |
| N4 : EXP-IT ; extérieur : FrigoMaint / MAINT-01 | Informatique générale du magasin et intervenant externe distingués de la conduite OT. Le placement réel des postes reste à confirmer. |

### Communications à retenir pour la conception de sécurité

| Échange | Besoin et point d’attention |
| --- | --- |
| **F0 — terrain ↔ régulation** | Maintenir les boucles locales ; liaison et cycle à confirmer. Ne pas introduire le bastion dans ce chemin. |
| **F1 — SUP-01 → REG, réponses associées** | Lectures Modbus TCP documentées et périodiques. Paramètres réseau et registres réels à obtenir ; filtrer selon les capacités et fonctions nécessaires. |
| **F2 — OPS-01 → SUP-01** | Consultation/alarmes, protocole inconnu. Interne OT dans la cible ; frontière à examiner si OPS-01 est en réalité sur l’IT général. |
| **F3 — collecte → historique SUP-01** | Fonction documentée ; stockage et découpage applicatif inconnus. Aucun nouveau flux réseau supposé pour une fonction éventuellement interne. |
| **F4–F5 — FrigoMaint → DMZ/bastion → cibles autorisées** | Chemins proposés ; distinguer diagnostic et écriture, autorisation et durée ; prévoir l’urgence et la traçabilité. Le bastion ne confère pas un accès général à tout l’OT. |
| **F6 — administration IT → DMZ/bastion → SUP-01** | Chemin proposé, origine et protocole à confirmer. Préserver la consultation courante et le contrôle pendant les changements. |
| **Services associés** | Temps, sauvegarde, restauration et mises à jour : identifier sources, destinations et mécanismes avant d’ajouter leurs règles de communication. |

Les frontières **extérieur/DMZ**, **IT/DMZ** et **DMZ/OT** sont à prendre en compte dans la cible proposée. Les niveaux Purdue organisent les fonctions ; ils ne constituent pas à eux seuls des règles de pare-feu ni une obligation d’un réseau par niveau. La collecte normale entre SUP-01 et REG n’a pas à traverser le bastion de maintenance.

## 4 — Trace du débrief à compléter en séance

| Sujet | Proposition préparée | Retour du groupe / du formateur | Décision et justification | Vérification ou responsable |
| --- | --- | --- | --- | --- |
| Maintien du contrôle pendant une maintenance IT | Préserver dépendances locales et vérifier la reprise. | À renseigner. | À renseigner. | À renseigner. |
| SUP-01 : supervision et historique | Serveur unique, fonctions N2/N3. | À renseigner. | À renseigner. | À renseigner. |
| DMZ, bastion et urgence FrigoMaint | Cible proposée ; accès autorisés, bornés et tracés. | À renseigner. | À renseigner. | À renseigner. |
| Historique et cohérence temporelle | Rétention, collecte et reprise à distinguer. | À renseigner. | À renseigner. | À renseigner. |
| Flux et informations absentes | Compléter la matrice avec le §8 et les intervenants. | À renseigner. | À renseigner. | À renseigner. |

**Résultat attendu :** une synthèse des exigences partagées, des divergences justifiées, des solutions encore ouvertes et des informations à demander. Mettre à jour matrices et schéma selon les décisions effectivement prises, en conservant leur statut. Aucun accord collectif ni choix définitif n’est renseigné par anticipation dans cette fiche.

## Ressources

- [Manuel Montval MAN-OT-01](MAN-OT-01_Manuel_exploitation_installation_frigorifique.md), §2–6 et §8.
- [3.1 — Exigences d’exploitation](analyser-exigences-exploitation-ot.md).
- [3.2 — Besoins informatiques](traduire-exigences-ot-besoins-informatiques.md).
- [3.3 — Schéma Purdue et flux](organiser-installation-modele-purdue.md).

[Retour à l’itération 2](index.md) · [Pense-bête](../../pense-bete/glossaire/informatique-industrielle/it-2.md)
