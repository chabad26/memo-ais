# Décider du traitement

**Itération 10 — 12 octobre 2026 — Travail individuel**

## 🎯 Objectif

Définir des actions proportionnées aux faits et au risque, en tenant compte
de leur impact sur File Browser et sur l’investigation. Une décision de
traitement ne signifie pas que toutes les mesures possibles doivent être exécutées.

**Statut : décisions documentées, exécution technique non présumée.**
Les lectures et preuves déjà fournies restent référencées dans la
[chronologie](completer-chronologie.md). Aucune nouvelle sauvegarde, règle,
restriction, mise à jour ou interruption n’est réalisée par cette feuille.

## 1. Base de décision

La [qualification de la situation](qualifier-situation.md) établit une
reproduction pédagogique : scans, 22 GET HTTP 200 et 99 alertes de volume
SYN. L’exploration et la répétition HTTP sont visibles sans alerte correspondante
dans l’extrait. L’essai initial sur la VM présente un angle mort expliqué
par le routage local ; les recherches applicatives de reproduction restent
sans résultat sur les périmètres montrés.

**Exploitation, accès non autorisé, modification applicative, persistance
malveillante et dommage ne sont pas démontrés.** Leur absence absolue n’est
pas certifiée. L’arrêt de service retrouvé est PackageKit, pas File Browser.
Ces éléments justifient de préserver et préciser les preuves, sans couper
automatiquement le service ni assimiler le scénario à une attaque réelle.

## 2. Actions retenues et mesures conditionnelles

Dans « immédiate / différée », indiquer la **décision**, pas un résultat
d’exécution. Une mesure différée peut être réévaluée dès qu’un fait nouveau
établit une menace ou un impact en cours.

| Action | Immédiate / différée | Justification | Impact | Vérification |
| --- | --- | --- | --- | --- |
| Conserver les événements et références utiles | **Immédiate, prioritaire** ; captures/pages conservées, export des objets originaux à compléter si disponibles | Rétention/rotation peuvent faire perdre la possibilité de corréler ; distinguer essai initial et reproduction | Service : faible pour copie ciblée, stockage à maîtriser. Investigation : préserve provenance et contexte ; éviter une copie brute contenant des secrets dans Git | Inventaire avec machine, fichier, fenêtre/fuseau et format ; ouvrir les copies, comparer aux sources, empreinte si utilisée. Ne pas déclarer export/empreinte sans preuve |
| Maintenir une surveillance ciblée et les sources existantes | **Immédiate**, observation à poursuivre selon période de travail | Détecter un nouvel événement sans générer une nouvelle injection ; dispositif réseau déjà exploitable | Service : faible en lecture, coût journalisation/stockage à mesurer. Investigation : contexte continu, sans changements de règles masqués | Source actuelle disponible, événements récents sur activité normale prévue, période et filtres enregistrés ; ne pas reprendre J9 comme preuve de fonctionnement actuel |
| Vérifier le système et les points de visibilité par lectures ciblées | **Immédiate pour les questions ouvertes**, sans audit exhaustif automatique | Rétention, configuration de capture/collecte et logs applicatifs nécessaires pour expliquer les manques | Service : faible si lectures limitées. Investigation : ne pas confondre état actuel et état du 9 octobre ; éviter sortie de secrets | Relevés datés des sources, chemins/rotations, interface et configuration effective ; confirmer une hypothèse précise ou conserver Non vérifiable |
| Rechercher les flows des ports refusés et pièces historiques complémentaires | **Immédiate si journaux encore disponibles**, sinon limite à conserver | Compléter l’ordre/cibles avec flow.start ; contextualiser la sortie Nmap sans compter alertes comme ports | Service : lecture pouvant solliciter disque/CPU, cibler fichiers utiles. Investigation : enrichit sans reproduire le passé | Objets référencés et corrélés aux fenêtres ; recherches vides documentées avec fichier et couverture |
| Adapter la détection HTTP et évaluer le bruit SYN | **Différée : préparation retenue**, installation non réalisée | Règles actuelles spécifiques à d’autres chemins ; 99 alertes pendant une courte phase peuvent produire du bruit | Service : rechargement/redémarrage à encadrer, coût et faux positifs possibles. Investigation : conserve jeu précédent et date des changements pour distinguer avant/après | Besoin et conditions écrits, SID sans collision, sauvegarde datée, test de configuration, positifs/négatifs séparés et comparaison des usages normaux |
| Limiter temporairement certains accès | **Différée / conditionnelle, non justifiée actuellement** | À envisager si compte, origine ou ressource réellement non autorisés sont établis | Service : utilisateurs légitimes potentiellement affectés, IP partagée/NAT à considérer. Investigation : activité interrompue ou déplacée, traces du changement à garder | Périmètre et décideur documentés, accès autorisés préservés, scénario refusé effectivement testé et retour arrière vérifié |
| Bloquer une origine ou un comportement réseau | **Différée / conditionnelle, non exécutée** | Scénario connu et aucune menace active établie ; un blocage global de l’hôte pourrait bloquer l’administration | Service : réseau/applicatif/administration affectés selon règle. Investigation : coupe l’observation, peut masquer d’autres événements ; filtrage Docker à vérifier au point effectif | Sauvegarde/retour arrière et accès console prévus ; test depuis une source concernée et une autorisée ; preuve du blocage réel, pas seulement règle affichée |
| Mettre à jour un composant | **Différée, dans le suivi de maintenance** ; pas remédiation déduite de ces GET | Aucune vulnérabilité exploitée n’est établie par le scénario ; une mise à jour doit répondre à un besoin/version qualifié | Service : interruption/compatibilité possibles, données et retour arrière à préparer. Investigation : versions et journaux peuvent changer, conserver l’état utile auparavant | Versions avant/après, applicabilité, sauvegarde vérifiée, tests fonctionnels et nouveau contrôle ciblé ; vérifier le risque résiduel sans promettre une solution globale |
| Isoler un composant | **Différée / conditionnelle, non exécutée** | À réévaluer si compromission ou propagation étayée ; pas mesure systématique d’un exercice de scan | Service : perte d’accès et possible coupure de l’agent/gestion. Investigation : état local et canal console à préserver ; traces distantes interrompues | Périmètre/isolation réels, canal d’administration conservé, preuve de conservation préalable si possible, réversibilité et remise en service contrôlées |
| Arrêter temporairement File Browser | **Différée / conditionnelle, non justifiée actuellement** | Pas d’impact en cours démontré exigeant cet arrêt ; ne pas confondre avec l’arrêt PackageKit historique | Service : indisponibilité immédiate. Investigation : disparition d’état volatil et fin des traces d’activité, heure/raison de l’arrêt à consigner | Décision motivée, état utile conservé selon urgence, arrêt effectif puis reprise fonctionnelle/données/persistance vérifiées |

## 3. Ordre de traitement retenu

1. **Préserver les pièces et leur provenance** : garder fenêtres, fuseaux, originaux utiles s’ils existent et critères des recherches sans résultat. Les pages/captures du mémo ne remplacent pas une conservation indépendante des sources.
2. **Poursuivre les lectures ciblées et l’observation**, sans relancer le scénario pour combler une preuve passée. Le nom PackageKit est désormais établi : ne pas recommencer cette piste sans nouvel indice.
3. **Préparer une évolution de détection**, avec besoin documenté et validation séparée, plutôt que considérer tout chemin demandé comme une attaque.
4. **Reporter restrictions, blocage, isolation et arrêt** tant qu’aucun élément nouveau ne les justifie. Une action doit réduire un risque identifié, pas seulement faire disparaître une alerte.
5. **Traiter la maintenance séparément**, avec versions/applicabilité/continuité vérifiées ; aucun nouveau déploiement n’est décidé sur la seule présence de scans et de 200.

## 4. Quand réévaluer les décisions ?

| Nouveau fait possible | Décision à réexaminer | Éléments nécessaires |
| --- | --- | --- |
| Accès réellement non autorisé ou contenu sensible exposé | Restriction ciblée, vérification des droits et éventuellement blocage | Compte/ressource, réponse ou journal probant, périmètre affecté et maintien des accès légitimes |
| Dégradation mesurée et liée à l’activité | Limitation de fréquence ou arrêt temporaire si nécessaire | Mesures, erreurs, lien temporel/cause, alternatives moins perturbantes et validation du service |
| Exploitation ou persistance étayée | Confinement/isolation et conservation adaptée | Pièces techniques, état des données/processus, périmètre et décision du responsable/formateur |
| Source non visible ou journaux insuffisants | Collecte ou point d’observation supplémentaires | Besoin précis, droits/volumes/rétention, preuve de collecte de bout en bout sur test distinct |
| Faux positifs mesurés de la règle SYN | Réglage ciblé de la règle/vue | Référence normale, volume, avant/après et maintien de détection des tests pertinents |

Un impact réel en cours peut justifier une décision rapide : préserver les
preuves accessibles sans retarder une mesure nécessaire, consigner les
pertes de visibilité et la raison du choix. Sans ce déclencheur, les pièces
actuelles ne justifient pas une interruption automatique.

## 5. Suivi des décisions et de leur vérification

| Décision | État actuel | Résultat de vérification |
| --- | --- | --- |
| Conservation dans le mémo | Feuilles et captures intégrées ; objets originaux complets non déclarés exportés | Documentation contrôlée ; rétention des journaux d’origine non garantie |
| Lectures historiques | Journald/auditd J10 et recherches J9 documentés | Contexte du script précisé, PackageKit identifié, limites applicatives conservées |
| Nouvelles règles / restriction / blocage / mise à jour / isolation / arrêt | **Non réalisés dans cette activité** | Aucun effet technique ni résultat de contrôle inventé |
| Suite d’observation et investigations utiles | À conduire selon les pièces nouvelles et la disponibilité des sources | Ajouter commande, date, résultat, impact et décision révisée après réalisation |

Si une action est effectivement exécutée ensuite, conserver : décideur,
objectif, périmètre, heure, état avant/après, effets sur le service et les
preuves, vérification et retour arrière. Ne pas changer rétroactivement la
qualification des événements précédents.

## 📦 Décision provisoire

**Priorité à la conservation, à l’observation et aux vérifications ciblées.**
Préparer une détection mieux adaptée aux routes et répétitions observées.
Aucune restriction, isolation ou coupure immédiate n’est justifiée par les
preuves actuelles du scénario pédagogique. Les mesures restent révisables
si de nouveaux faits établissent un risque ou un impact en cours.

Cette décision décrit le traitement envisagé, pas une liste d’opérations
déjà appliquées. La situation reste ouverte aux compléments du formateur.

- [Qualification de la situation](qualifier-situation.md)
- [Chronologie complétée](completer-chronologie.md)
- [État provisoire et préparation J10](../it-9/qualifier-situation-preparer-suite.md)
- [Retour à l’itération 10](index.md)
- [Retour au module](../README.md)
