# Préparer le fragment de PSSI

**Itération 5 — Préparation de J6 — Travail individuel — 5 octobre 2026**

## 🎯 Objectif

Définir les sujets qui seront développés dans le fragment de PSSI en J6.
Regrouper les règles proposées pour le cas File Browser en conservant leur
problème d’origine, leur objectif, les rôles, les règles et les contrôles.

**Statut : préparation documentaire.** Le fragment n’est pas encore rédigé
comme une politique adoptée. Les responsables nominatifs, délais, périodicités
et autorités de validation restent à définir. La première version sera
élaborée en J6 à partir de cette sélection.

## 1. Délimiter le fragment

**Titre de travail proposé :** « Gouvernance et maintien en sécurité d’un
service de partage documentaire avec des partenaires externes ».

Le périmètre couvre le service File Browser et ses couches de maintenance,
ses accès, son exposition, le traitement des vulnérabilités et son cycle de
vie. L’exposition Internet est celle du scénario pédagogique ; elle n’est
pas démontrée pour la VM du laboratoire.

Le fragment s’appuie sur les [problèmes organisationnels](identifier-ce-que-technique-ne-regle-pas.md),
l’[analyse de la PSSI de référence](analyser-pssi-existante-poitiers.md) et les
[huit propositions P01–P08](proposer-regles-adaptees-cas-fil-rouge.md).
Les identifiants sont conservés pour relier les sujets aux règles déjà proposées.
Le [compte-rendu technique](finaliser-compte-rendu-durcissement-verification.md)
fournit les exemples de preuves et les risques résiduels.

Ce périmètre ne cherche pas à couvrir toute la sécurité de l’organisation.
La sécurité physique, un dispositif complet de gestion de crise ou l’ensemble
des obligations juridiques ne sont pas ajoutés sans besoin établi. Les commandes
SSH, Docker et auditd restent dans les procédures et comptes rendus, plutôt
que de devenir le contenu principal du fragment.

## 2. Regrouper les règles par sujet

| Sujet retenu | Problème auquel il répond | Objectif recherché | Rôles concernés | Règles envisagées | Contrôles possibles |
| --- | --- | --- | --- | --- | --- |
| **S01 — Responsabilités et transmission** | Serveur livré par l’infrastructure, application déployée par le demandeur, maintenance mal définie dans le scénario | Éviter toute couche sans responsable et assurer la continuité des responsabilités | Propriétaire du service, infrastructure, mainteneur applicatif et suppléants | **P01** : fiche de service avant exploitation ; répartition OS/runtime/application/données/exposition ; transfert des accès et procédures lors d’un changement d’équipe | Vérifier fiche approuvée, personnes joignables et périmètres ; faire suivre une alerte OS et une alerte application jusqu’au responsable |
| **S02 — Maintenance et suivi des vulnérabilités** | Versions anciennes ; alertes nombreuses et applicabilité parfois incertaine ; mises à jour pouvant affecter le service | Maintenir les composants et transformer les alertes en actions traçables sans casser l’usage | Mainteneur applicatif, infrastructure, référent sécurité, propriétaire | **P02–P03** : inventaire/support ; veille et qualification par composant ; responsable/priorité/échéance ; mises à jour avec sauvegarde, tests et retour arrière | Comparer inventaire réel ; examiner tickets et exclusions ; contrôler versions/digest, échéances de support et preuves avant/après |
| **S03 — Exposition et accès des partenaires** | Service toujours exposé dans le scénario ; identifiants par défaut observés au test initial ; durée des accès partenaires à organiser | Limiter la publication et les accès au besoin légitime | Propriétaire, référent sécurité, infrastructure, mainteneur et partenaires | **P04–P08** : exposition autorisée et revue ; accès administratifs distingués ; habilitations et durée validées ; secrets initiaux remplacés ; retrait en fin de besoin | Rapprocher flux autorisés et ouverts ; revue comptes/partages ; essais autorisés d’accès légitime/refus ; preuve de retrait d’un accès expiré |
| **S04 — Contrôles, écarts et exceptions** | Désactivation CUPS insuffisante au reboot ; risques résiduels et actions différées ; mesures susceptibles de disparaître après changement | Vérifier la durée des protections et empêcher une acceptation implicite des écarts | Exploitants, référent sécurité, propriétaire et autorité habilitée | **P05–P06** : contrôles après changement et périodiques ; suivi des écarts ; exceptions motivées, approuvées et limitées dans le temps | Rapports avec effet et fonctionnement ; échantillon d’écarts suivis ; registre des exceptions, expiration et compensations réellement actives |
| **S05 — Cycle de vie, remplacement et retrait** | Service conservé de 2021 à 2026 ; fin de maintenance File Browser annoncée dans le laboratoire | Prévoir la sortie d’un service sans besoin, sans responsable ou sans maintenance | Propriétaire, mainteneur, infrastructure, autorité de décision | **P07** : revue de l’utilité et du support ; décision de remplacement/retrait/exception ; traitement des données, accès, publication et sauvegardes | Décision datée, plan avec moyens/échéance ; test de migration ou d’inaccessibilité ; inventaire et accès mis à jour |

**Articulations :** S02 ouvre un écart vers S04 si une correction est reportée.
S05 s’appuie sur S02 pour les fins de support et sur S03 pour retirer les accès.
S01 désigne les porteurs de tous les autres sujets. Ne pas recopier la même
règle dans plusieurs sections : conserver son identifiant et utiliser un renvoi.

## 3. Vérifier l’ancrage dans les faits du cas

| Sujet | Fait ou preuve qui justifie sa présence | Limite à conserver |
| --- | --- | --- |
| S01 | Contexte pédagogique : partage OS/application et responsabilités de maintenance non définies | Ce n’est pas un audit de l’organigramme réel de l’université ou d’une entreprise |
| S02 | Anciennes versions, migration effectuée, alertes et faux positifs de versions qualifiés en J4 | Toutes les alertes ne sont pas des vulnérabilités confirmées ; pièces J5 encore à joindre |
| S03 | Exposition externe du scénario ; connexion initiale admin/admin selon Olivier, puis refus après changement | Pas de preuve d’exposition Internet de la VM ni de revue réelle de tous les comptes partenaires |
| S04 | CUPS revenu après reboot malgré disabled ; masquage ensuite vérifié ; dix HIGH Trivy et actions différées | Une difficulté intermédiaire résolue n’est pas un échec de l’état final ; aucun risque formellement accepté |
| S05 | Logs applicatifs annonçant la fin de maintenance ; service maintenu dans le temps dans le scénario | Aucun remplacement ou retrait exécuté ; décision et budget restent à obtenir |

Cette grille évite une liste générique : chaque sujet répond à une difficulté
ou à un risque de ce cas. Les mesures techniques déjà vérifiées deviennent
exemples de contrôles, sans être transformées en obligations universelles.

## 4. Préparer la structure à rédiger en J6

| Partie du futur fragment | Contenu à développer |
| --- | --- |
| Objet et périmètre | Service de partage, données et partenaires ; limites et vocabulaire |
| Rôles et responsabilités | S01, responsables désignés, suppléants et autorité de décision |
| Maintien en sécurité | S02, inventaire, veille, qualification, correction et validation |
| Publication et habilitations | S03, décisions d’exposition, flux, comptes et retrait des accès |
| Vérification et dérogations | S04, calendrier, preuves, écarts, escalade et exceptions |
| Fin de vie et transition | S05, déclencheurs, remplacement, retrait et traitement des données |
| Adoption et révision | Approbateur, version, diffusion, réexamen et lien aux procédures |

Pour chaque règle développée en J6, conserver le même format : **destinataire,
action attendue, périmètre, condition ou échéance, responsable de validation
et preuve de contrôle**. Les formulations des P01–P08 constituent le matériau
de départ ; elles restent à discuter avec les acteurs concernés.

## 5. Éléments à arbitrer avant adoption

- Affecter chaque rôle à une personne ou équipe et identifier les suppléants.
- Qualifier les données, la criticité et le besoin des partenaires pour fixer des exigences proportionnées.
- Choisir les délais de correction, les fréquences de revue et les circuits d’escalade selon le risque.
- Définir l’autorité qui approuve l’exposition, les exceptions et les décisions de remplacement.
- Désigner le registre des services, alertes, preuves et exceptions ; prévoir son accès et sa tenue.
- Estimer les moyens de maintenance, les interruptions et le remplacement d’une application sans maintenance.

Ces décisions ne sont pas inventées comme déjà prises. Une fréquence ou un
délai chiffré ajouté en J6 devra être identifié comme proposition et motivé.
Le fragment ne devra pas prétendre qu’une règle est appliquée simplement
parce qu’elle est écrite.

## 📦 Livrable préparatoire

Cinq sujets délimités, reliés aux huit règles proposées et aux problèmes du
cas, avec objectifs, rôles et contrôles. Cette feuille constitue le plan de
travail pour **élaborer une première version du fragment de PSSI en J6**.
Elle ne remplace ni cette rédaction ni son approbation.

- [Règles proposées P01–P08](proposer-regles-adaptees-cas-fil-rouge.md)
- [Problèmes organisationnels](identifier-ce-que-technique-ne-regle-pas.md)
- [Analyse de la PSSI de référence](analyser-pssi-existante-poitiers.md)
- [Retour à l’itération 5](index.md)
- [Retour au module](../README.md)
