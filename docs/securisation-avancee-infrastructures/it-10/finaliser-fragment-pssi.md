# Finaliser le fragment de PSSI

**Itération 10 — 12 octobre 2026 — Travail individuel — 1 h**

## 🎯 Objectif et résultat

Produire le fragment finalisé, intégrer les enseignements de l’audit et du
REX et vérifier que les règles permettent d’identifier attendu, responsable
et preuve. Cette feuille termine l’itération ; elle ne clôture pas un incident.

**Livrable final de formation : [fragment de PSSI V2](fragment-pssi-v2.md).**
Il consolide CV01–CV11 et CV12 dédiée aux incidents. La V1 est conservée,
les évolutions sont justifiées dans la [feuille de révision](reviser-fragment-pssi.md).
**Finalisé documentairement ne signifie pas adopté ni appliqué** : désignations,
mandats, moyens et date d’effet organisationnelle restent à valider.

## 1. Cas File Browser depuis 2021

Le [cas pédagogique](../it-6/definir-perimetre-fragment-pssi.md) décrit un
serveur demandé en 2021, une VM Ubuntu 20.04 fournie par l’infrastructure,
puis File Browser déployé par le demandeur. En 2026, le service demeure
exposé et les responsabilités de maintenance sont insuffisamment définies.
L’exposition Internet appartient au scénario, pas aux preuves de la VM du
laboratoire. Aucun départ précis, avis de vulnérabilité daté ou incident
intermédiaire entre 2021 et 2026 n’est inventé ci-dessous.

L’analyse suivante est **contrefactuelle** : elle indique les décisions et
contrôles qu’une application effective de la PSSI aurait exigés. Elle ne
prouve pas que toute attaque aurait été évitée, ni que les mesures auraient
toujours été exécutées correctement.

| Moment / déclencheur | Règles | Ce qui aurait été différent | Effet attendu | Preuve qui aurait dû exister |
| --- | --- | --- | --- | --- |
| Demande du serveur en 2021 | CV01, CV02 | Besoin, données, durée, propriétaire et mainteneurs formalisés ; fourniture de VM distinguée de l’autorisation de publier | Prévenir une ouverture sans décision ; clarifier métier / IT | Fiche, accord des mainteneurs, autorisation et réserves |
| Déploiement de File Browser, avant ouverture | CV03, CV04, CV05 | Inventaire par couche, support et données ; exposition approuvée, secrets initiaux retirés, restauration et visibilité testées | Réduire exposition injustifiée et défaut de reprise ; rendre l’activité observable | Inventaire/version, matrice, tests autorisé/refusé, restauration et événements de référence |
| Exploitation à partir de 2021 | CV05–CV08 | Suivi hebdomadaire, examen mensuel des correctifs et contrôles trimestriels ; besoin et responsabilités revus | Détecter plus tôt écarts de maintenance, collecte ou exposition | Calendrier, rapports, tickets et responsables des actions |
| Réception d’un avis pertinent | CV07, CV06 | Applicabilité, exposition, impact et priorité qualifiés ; correctif ou protection décidé dans les délais proposés | Traiter un risque contextualisé, sans attendre un incident | Avis, qualification, échéance, ticket et recontrôle |
| Changement de personne ou prestataire, s’il survient | CV02, CV10 | Passation acceptée, accès/alertes testés, dossiers et exceptions transmis ; suppléance si imprévu | Éviter une couche sans porteur ; préserver la capacité de traitement | Désignations, passation, notification reçue et droits actualisés |
| Report de correction ou protection incomplète | CV09 | Dérogation explicite, limitée, compensation vérifiée et plan de sortie ; renouvellement décidé avant échéance | Éviter un maintien par inertie et rendre le risque visible | Exception approuvée, risque résiduel, contrôle mensuel et sortie datée |
| Disparition du besoin ou fin de maintenance annoncée | CV07, CV11 | Dossier de décision sous dix jours ouvrés ; remplacement/retrait ou exception, continuité des données organisée | Éviter conservation durable d’un produit sans support | Décision, échéance, migration/restitution, retrait de publication et sort des preuves |
| Signalement de J9 | CV08, CV12 | Sources et contacts déjà identifiés ; pièces préservées, faits/hypothèses séparés, chronologie et limites documentées | Faciliter qualification ; éviter de confondre scan, 200 et compromission | Dossier sourcé, fuseaux, recherches sans résultat, interprétations et inconnues |
| Décision de traitement | CV12, CV09 | Mesures motivées par risque et impact, exécutées dans un mandat, puis vérifiées ; pas arrêt automatique | Préserver service et preuves tout en traitant un danger établi | Décision, avant/après, résultat, retour arrière et éventuelle exception |
| Après investigation / REX | CV08, CV12 | Écarts affectés avec échéances ; tests de couverture et révision des règles | Transformer les limites constatées en améliorations suivies | REX, plan d’actions, responsable et validation des résultats |

Les délais cités sont ceux de la V2 locale, repris de V1 ; ils ne sont pas
présentés comme une norme externe. Une fin de maintenance n’est pas un fait
que les équipes de 2021 auraient nécessairement pu connaître à l’avance :
la veille et le déclencheur de décision auraient servi au moment de l’annonce.

## 2. Applicabilité et contrôlabilité des principales règles

| Règles | Déclencheur / périmètre | Responsabilité | Critère contrôlable | Limite à traiter avant adoption |
| --- | --- | --- | --- | --- |
| CV01–CV02 | Nouveau service et ouverture | Propriétaire, autorité, responsables techniques | Décision antérieure à ouverture ; chaque couche avec porteur ayant accepté ses tâches | Noms, délégations et moyens à valider |
| CV03–CV04 | Inventaire, exposition et changements | Responsable technique, mainteneurs, équipe réseau | Versions/flux rapprochés de l’état réel ; accès autorisé et refusé testés depuis zones pertinentes | Tests habilités, familles d’adresses et périmètre définis |
| CV05–CV06 | Exploitation et mise à jour | Mainteneurs ; coordination technique ; propriétaire pour fonctionnement | Restauration utile et tests avant/après, version réelle et retour arrière documentés | Environnement isolé, fenêtres et moyens nécessaires |
| CV07 | Avis ou résultat de scan | Référent sécurité et mainteneurs ; autorité pour arbitrages | Applicabilité, priorité, responsable, délais, décision et recontrôle retrouvables | Veille et délais réalistes, aucune clôture par compteur seul |
| CV08 | Avant ouverture, chaque trimestre, changement pertinent | Responsable technique et mainteneurs ; revue sécurité | Rapport daté, activité de référence retrouvée, alerte attendue ou limite, référence normale et action d’écart | Couverture adaptée au risque ; source active seule insuffisante |
| CV09 | Dérogation et échéance | Propriétaire, sécurité, autorité, responsable de suivi | Approbation valable, durée ≤ 90 jours, compensation vérifiée et sortie suivie | Mandat d’acceptation, contrôle et restrictions approuvées |
| CV10 | Changement prévu ou absence imprévue | Propriétaire, technique, équipes habilitées | Entrant/suppléant reçoit une notification et retrouve un événement ; droits inutiles retirés | Suppléance et accès effectifs, pas simple nom dans une fiche |
| CV11 | Fin de besoin/support ou mainteneur absent | Propriétaire et autorité ; exécution technique | Décision, dépendances/données traitées, accès révoqués, publication fermée et inventaire clôturé | Conservation des preuves et ressources partagées à préserver |
| CV12 | Signalement, traitement, reprise et REX | Sécurité coordonne ; technique exécute ; métier apprécie impact ; autorité décide | Chronologie sourcée, statuts, décision versus exécution, impact/contrôle et actions du REX | Circuit d’urgence, délégations et rétention validés |

**Résultat de relecture :** les règles principales ont une attente, un
périmètre, un rôle et une preuve identifiables. Leur faisabilité opérationnelle
reste conditionnée aux moyens et validations ci-dessus ; leur respect sur
une organisation réelle n’est pas démontré par cette feuille.

Pour les contrôles, conserver les statuts **Conforme, Non conforme,
Non vérifiable, Non applicable** de V2. Une exception ne transforme pas un
écart en conformité ; une preuve manquante reste Non vérifiable.

## 3. Vérifications finales de rédaction

- CV01–CV11 restent identifiables ; CV12 formalise détection, investigation, décisions proportionnées et REX.
- Les rôles IT/métier sont attribués par couche et par décision ; fourniture de serveur et maintenance applicative ne sont pas confondues.
- Les règles fixent résultats et contrôles ; les procédures choisissent les outils et points d’observation selon le service.
- Les exceptions, changements de responsable, risques résiduels et fins de vie sont suivis avec preuves et échéances.
- Le scénario depuis 2021, les observations J9 et l’exercice contrefactuel sont distingués ; aucune compromission n’est inventée.
- V1 est conservée, V2 finalisée pour la formation ; adoption organisationnelle et application ne sont pas déclarées réalisées.

## 📦 Livrables de fin d’itération

Fragment V2 consolidé, analyse des moments où la PSSI aurait changé les
décisions depuis 2021, grille d’applicabilité/contrôle et limites d’adoption.
L’itération documentaire est finalisée pour les éléments disponibles.
Les actions techniques proposées, l’adoption de la PSSI et les pièces encore
manquantes restent suivies séparément ; cette conclusion ne clôture pas l’incident.

- [Fragment finalisé — V2](fragment-pssi-v2.md)
- [Tableau de révision](reviser-fragment-pssi.md)
- [REX](realiser-rex.md)
- [V1 conservée](../it-6/fragment-pssi-v1.md)
- [Retour à l’itération 10](index.md)
- [Retour au module](../README.md)
