# Identifier ce que la technique ne règle pas

**Itération 5 — Travail individuel — 5 octobre 2026**

## 🎯 Objectif

Identifier les problèmes organisationnels mis en évidence par le cas fil rouge
File Browser et proposer des règles qui évitent leur réapparition. Les règles
ci-dessous sont des **propositions à valider**, pas une politique déjà adoptée
ni une description prouvée de l’organisation réelle.

## 1. Revenir au contexte du serveur

**Contexte pédagogique fourni :** en 2021, un service demande un serveur pour
partager des documents avec des partenaires externes. L’infrastructure fournit
Ubuntu 20.04 et le service demandeur déploie File Browser. En 2026, le service
reste accessible depuis Internet avec une application ancienne ; les
responsabilités de maintenance et de suivi n’ont pas été clairement définies.

L’exposition Internet appartient à ce cas fil rouge. Dans le laboratoire,
l’accès observé depuis le poste hôte ne démontre pas une exposition Internet.
La présente analyse ne suppose pas non plus que toute procédure était absente :
elle identifie ce qui n’est pas défini dans le contexte et doit être clarifié.

Les [remédiations J4](../it-4/finaliser-compte-rendu-durcissement.md) ont traité
versions, accès, privilèges, audit et services. Le
[bilan de vérification J5](finaliser-compte-rendu-durcissement-verification.md)
conserve les risques résiduels. Une commande ne désigne pas le propriétaire
futur du service, ne finance pas son remplacement et ne garantit pas qu’une
alerte sera prise en charge.

**Question directrice : quelles règles auraient permis d’éviter d’arriver à
cette situation ?**

## 2. Problèmes, responsabilités, règles et contrôles

Les fonctions proposées doivent être attribuées à des personnes ou équipes
nommées dans la fiche de service. Plusieurs équipes peuvent intervenir, mais
un responsable de décision doit être identifiable pour chaque sujet.

| Problème | Qui devrait être responsable ? | Quelle règle manque ? | Quel contrôle pourrait être réalisé ? |
| --- | --- | --- | --- |
| Serveur livré sans partage explicite des responsabilités OS/application | Responsable du service métier pour l’usage ; infrastructure pour l’OS/runtime ; mainteneur applicatif désigné pour File Browser | Avant mise en service, documenter qui maintient chaque couche, qui remplace les absents et qui arbitre les désaccords | Fiche de service approuvée ; exercice de routage d’une alerte OS puis application vers le bon interlocuteur |
| Application déployée par le demandeur puis laissée sans suivi clair | Responsable du service, avec mainteneur applicatif désigné | Aucun service exploité sans responsable applicatif, suppléant, procédure de maintenance et moyen d’intervention | Revue de la liste des services : propriétaire et suppléant joignables, dernière maintenance et prochaine échéance |
| Anciennes versions maintenues en exploitation | Infrastructure pour OS/Docker ; mainteneur pour application/image ; responsable de service pour planifier les interruptions | Tenir l’inventaire des versions, dates de support et dépendances ; planifier les mises à niveau avant fin de support | Rapprocher inventaire réel, calendrier de support et tickets de migration ; signaler toute échéance sans plan |
| Mise à jour différée pour préserver le fonctionnement, sans date de résolution | Responsable technique exécute ; responsable du service organise les tests et la fenêtre ; direction arbitre si nécessaire | Toute correction doit avoir priorité, responsable, échéance et validation fonctionnelle ; tout report doit être motivé et réexaminé | Ticket comportant versions avant/après, tests, retour arrière et date ; revue des corrections en retard |
| Alertes de vulnérabilités sans traitement attribué | Référent sécurité coordonne la qualification ; mainteneurs analysent ; responsable habilité décide du traitement | Définir réception, triage, applicabilité, action et escalade des alertes ; adapter l’urgence à l’exposition et à l’impact | Échantillon d’alertes reliées à un composant, un responsable, une décision et une preuve de clôture |
| Service exposé à Internet sans réexamen du besoin | Responsable métier justifie le partage ; sécurité examine le risque ; infrastructure met en œuvre l’exposition autorisée | Toute publication externe nécessite périmètre, approbation, protections, responsable et date de revue ; retirer les accès inutiles | Inventaire des services publiés rapproché des règles réseau et tests externes autorisés ; justification encore valide |
| Comptes ou accès partenaires conservés au-delà du besoin | Responsable métier valide les habilitations ; administrateur applicatif les applique | Accès nominatifs adaptés au besoin, durée définie, revue et retrait au départ ou à la fin du partenariat | Revue des comptes, partages et échéances ; preuve de désactivation et test d’un accès expiré |
| Livraison avec identifiants par défaut ou secret partagé | Mainteneur applicatif pour la configuration ; responsable du service pour la réception | Changer les secrets initiaux avant ouverture, organiser leur conservation et les accès d’administration ; prévoir la gestion des sessions | Checklist de réception, refus de l’ancien identifiant, comptes autorisés et secret conservé hors documentation |
| Application sans maintenance future | Responsable du service porte la décision de continuité ; mainteneur et sécurité évaluent les options ; direction alloue les moyens | Définir critères de choix, suivi de maintenance et plan de remplacement ; une fin de maintenance doit déclencher une décision avec échéance | Avis de fin de maintenance relié à une analyse, un budget/plan et un responsable ; exception suivie jusqu’à expiration |
| Sauvegardes et retour arrière non assumés entre équipes | Infrastructure et mainteneur selon les données ; responsable du service fixe les besoins de reprise | Identifier données/configuration/base, responsabilités de sauvegarde, objectifs de reprise et tests de restauration | Restauration sur environnement de test avec contrôle des fichiers et de la base ; compte-rendu attribué |
| Logs produits mais personne chargée de les consulter | Exploitant surveille ; référent sécurité définit les événements utiles ; responsable de service fixe les contacts | Définir sources, rétention, protection, seuils, destinataires et procédure de traitement ; surveiller aussi les pertes de collecte | Événement test reçu et pris en charge ; contrôle des pertes, espace et droits ; ticket de traitement |
| Serveur qui reste disponible après disparition du besoin | Responsable du service décide ; infrastructure et mainteneur exécutent le retrait | Revoir périodiquement l’utilité du service et formaliser sa sortie : données, accès, DNS, exposition, sauvegardes et inventaire | Procès-verbal de retrait, test d’inaccessibilité et mise à jour des inventaires ; conservation des données justifiée |

## 3. Organiser la responsabilité sans créer un angle mort

Le service métier reste responsable du **besoin**, des partenaires, des données
et de la validation des parcours. L’infrastructure assure les couches qui lui
sont confiées : OS, virtualisation, réseau et moteurs, selon l’accord établi.
Le mainteneur applicatif suit l’application, ses images et dépendances, et ses
migrations de base. Le référent sécurité contribue à la veille, à la
qualification et aux exigences ; il ne devient pas automatiquement l’exécutant
de toutes les corrections.

Si le service demandeur ne peut pas maintenir File Browser, il faut désigner
un autre mainteneur et organiser le transfert de compétences, des accès et des
moyens. La formule « chacun s’en occupe » ne permet pas de savoir qui agit.

Un risque résiduel ne doit pas être accepté implicitement par l’administrateur.
Une éventuelle exception précise le risque, les mesures compensatoires, le
responsable habilité, l’échéance et les conditions de réexamen. Le responsable
de décision et les exécutants techniques sont distingués.

## 4. Règles qui auraient changé le parcours 2021–2026

| Moment | Décision ou règle proposée | Trace attendue |
| --- | --- | --- |
| Demande en 2021 | Définir usage, données, partenaires, durée et propriétaire du service | Demande et fiche de service validées |
| Livraison du serveur | Définir la frontière de maintenance OS/runtime/application et les suppléants | Répartition des responsabilités et réception |
| Avant publication | Vérifier accès, secrets, sauvegardes, support et protections selon le risque | Autorisation d’exposition et tests de réception |
| Pendant l’exploitation | Revoir versions, correctifs, accès externes, utilité et alertes | Inventaire actualisé, tickets et comptes rendus de revue |
| À l’approche d’une fin de support | Planifier migration ou remplacement ; décider explicitement d’une exception si nécessaire | Plan avec responsable, échéance et moyens |
| En fin d’usage | Retirer les accès et la publication, traiter les données et fermer le service | Checklist de retrait et inventaire mis à jour |

La périodicité des revues et les délais de correction doivent être arrêtés par
l’organisation selon criticité, exposition et obligations applicables. Ils
ne sont pas inventés ici comme des exigences déjà en vigueur.

## 5. Ce que le durcissement ne règle pas durablement

| Intervention technique réalisée | Problème organisationnel encore à résoudre |
| --- | --- |
| Mise à niveau Ubuntu et File Browser | Qui assurera la prochaine mise à jour et avec quels moyens ? |
| Changement du mot de passe et restrictions SSH | Qui autorise les comptes et retire les accès devenus inutiles ? |
| Réduction des privilèges Docker | Qui valide une nouvelle image et vérifie que le déploiement conserve les protections ? |
| Installation auditd et rotation | Qui surveille les événements, les pertes et la saturation, puis intervient ? |
| Arrêt CUPS | Qui valide le catalogue de services autorisés et empêche une réactivation non justifiée ? |
| Re-scans et faux positifs qualifiés | Qui suit les alertes ouvertes et réévalue les exclusions lorsque les versions changent ? |
| Constat de fin de maintenance File Browser | Qui décide du remplacement, du financement et du calendrier ? |

L’absence de baisse du compteur Greenbone ne remplace pas cette analyse, et
une baisse ne prouverait pas non plus que les responsabilités sont organisées.
Le contrôle doit porter sur la décision et sa mise en œuvre, pas seulement sur
la présence d’une procédure écrite.

## 📦 Résultat attendu

Un tableau problèmes/responsabilités/règles/contrôles renseigné et une liste
de décisions organisationnelles à faire valider. Les propositions peuvent
alimenter une évolution de la PSSI ou des procédures d’exploitation après
lecture de leurs versions réelles ; aucune conformité à une PSSI non fournie
n’est revendiquée.

**Conclusion du cas :** fournir un serveur et corriger ses défauts ne suffit
pas à organiser cinq années d’exploitation. Un propriétaire identifié, une
maintenance attribuée, un suivi des alertes, une publication réexaminée et un
cycle de vie prévu rendent les corrections durables et vérifiables.

- [Compte-rendu de durcissement et de vérification](finaliser-compte-rendu-durcissement-verification.md)
- [Retour à l’itération 5](index.md)
- [Analyse et évolution de la PSSI](../it-7/index.md)
- [Retour au module](../README.md)
