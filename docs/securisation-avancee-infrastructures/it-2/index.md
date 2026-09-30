# Itération 2 — Corriger, durcir et vérifier

## Objectif

Réduire les risques identifiés dans l'audit et démontrer les effets des mesures
sans perdre les fonctions attendues de l'application.

**Statut : activité préparatoire, à réaliser.** Les changements seront choisis
à partir des constats réels de l'[itération 1](../it-1/index.md).

## Préparer une modification

Pour chaque constat retenu, compléter le
[journal des changements](../dossier-preuves.md#journal-des-changements) :

| Information | Contenu attendu |
| --- | --- |
| Justification | Constat, preuve et risque à réduire |
| Cible | Machine, service, fichier ou composant exact |
| Action | Configuration ou version avant/après, avec auteur et date |
| Effets attendus | Réduction du risque et fonctions métier à préserver |
| Dépendances | Application, bibliothèques, réseau, certificats et accès |
| Retour arrière | Sauvegarde, commande ou procédure, conditions de déclenchement |
| Validation | Contrôle de sécurité et test fonctionnel à effectuer |

## Choisir les mesures selon les constats

| Famille | Mesures possibles, à justifier |
| --- | --- |
| Correctifs | Mettre à jour l'OS, l'application ou une dépendance réellement affectée |
| Exposition | Retirer un service inutile, limiter un flux ou restreindre l'administration |
| Identités | Supprimer un accès obsolète, limiter les privilèges, clarifier les comptes de service |
| Configuration | Adapter les permissions et les paramètres du service au besoin |
| Secrets et TLS | Renouveler un secret exposé, corriger sa conservation ou la configuration TLS |
| Exploitation | Désigner les responsables, organiser maintenance, sauvegardes et journalisation |

Un correctif traite un défaut identifié ; le durcissement réduit la surface
d'attaque ou les possibilités d'abus. Une mesure compensatoire limite un risque
en attendant une correction, avec un responsable et une date de réexamen.

## Travail à réaliser

1. Choisir un premier lot cohérent à partir des priorités et dépendances.
2. Conserver la configuration initiale et vérifier le moyen de reprise.
3. Pour une modification SSH ou réseau, garder une console et un accès de secours
   vérifiés avant d'appliquer le changement.
4. Modifier un élément à la fois lorsque cela permet d'attribuer son effet.
5. Contrôler la syntaxe avec l'outil du service avant rechargement, si disponible.
6. Exécuter les tests de sécurité et de fonctionnement prévus.
7. Réaliser un nouveau contrôle d'audit avec un périmètre comparable.
8. Si la modification doit survivre au redémarrage, vérifier aussi sa persistance
   lors d'un redémarrage maîtrisé du laboratoire.
9. Documenter le résultat, le risque restant et les éventuels effets indésirables.

## Comparer avant et après

| Contrôle | Avant | Après | Conclusion à documenter |
| --- | --- | --- | --- |
| Défaut initial | Preuve et condition d'observation | Nouveau contrôle du même défaut | Corrigé, réduit, inchangé ou non concluant |
| Accessibilité | Flux utiles et exposition constatée | Flux permis et refusés | Restriction effective depuis le bon point d'observation |
| Application | Parcours utilisateur de référence | Même parcours, données de test | Fonctionnement conservé ou régression |
| Administration | Accès autorisé et console | Accès autorisé toujours possible | Exploitabilité de la maintenance |
| Journaux | Événement ou collecte initiale | Événement après changement | Détection et diagnostic toujours possibles |
| Redémarrage si pertinent | Configuration persistante attendue | État observé après redémarrage | Correction durable ou reprise à compléter |

Conserver les paramètres et la date des deux scans. Documenter les changements
de version, de base de vulnérabilités, de privilèges ou de digest d'image qui
peuvent expliquer une différence. Un meilleur score global ne démontre pas à
lui seul la correction du constat choisi.

## État final attendu et preuves L2

Un tableau relie chaque constat traité à une modification, un retour arrière,
une preuve avant/après et un test fonctionnel. Les constats non corrigés restent
visibles avec une justification, un responsable et une prochaine action.

Les configurations et rapports sont relus avant diffusion. Les commandes de
changement seront détaillées après identification des systèmes et des services,
pour éviter d'appliquer une procédure à une cible différente.

- [Pense-bête de l'itération](../../pense-bete/glossaire/securisation-avancee-infrastructures/it-2.md)
- [Étape suivante — Détection Suricata](../it-3/index.md)
- [Retour au module](../README.md)
