# Définir les contrôles et les exceptions

**Itération 6 — Travail individuel — 6 octobre 2026**

## 🎯 Objectif et place dans le fragment

Vérifier l’application des [règles CV01–CV11](definir-regles-cycle-vie-service.md)
et encadrer les situations où elles ne peuvent pas être respectées.
Cette section complète le fragment composé du
[périmètre](definir-perimetre-fragment-pssi.md), des
[responsabilités](definir-roles-responsabilites.md) et des règles du cycle de vie.

**Statut : proposition à valider.** Les fréquences et délais reprennent les
choix proposés dans les règles CV. Aucun contrôle ci-dessous n’est présenté
comme exécuté et aucune exception n’est déclarée accordée au service File Browser.

## 1. Organiser les contrôles

Le responsable technique tient le calendrier et rassemble les preuves des
mainteneurs. Le propriétaire confirme le besoin métier et les responsables.
Le référent sécurité examine les résultats, suit les écarts et alerte
l’autorité d’autorisation. Lorsque cela est possible, la personne qui valide
le contrôle est distincte de celle qui a réalisé le changement ; sinon,
documenter le cumul et faire relire les résultats par un autre rôle compétent.

Chaque contrôle porte sur un service identifié et couvre toutes ses couches
applicables. Les tests réseau et restaurations sont réalisés avec autorisation,
dans un périmètre défini et sans altérer les données de production.

| Contrôle / règles | Méthode et critère de respect | Fréquence ou déclencheur proposé | Réalisation → revue | Preuves à conserver |
| --- | --- | --- | --- | --- |
| Autorisation — CV01 | Comparer ouverture effective, décision signée et conditions ; aucune réserve bloquante sans traitement ou exception valide | Avant ouverture ou remplacement ; revue trimestrielle des décisions applicables | Responsable technique → autorité | Fiche du service, décision, tests et réserves levées |
| Responsables — CV02, CV10 | Confirmer propriétaire, suppléants et mainteneurs par couche ; tester contact, réception d’une alerte et capacité de reprise. Chaque couche possède un porteur ayant accepté la tâche | Chaque trimestre ; avant changement prévu, dès notification d’une absence imprévue | Propriétaire et responsable technique → référent sécurité | Désignations, confirmations, passation et tests d’accès/alerte |
| Utilité — CV08, CV11 | Faire confirmer usage, partenaires, données et durée par le propriétaire ; rapprocher cette confirmation d’indices d’activité disponibles. Une absence de connexion seule ne justifie pas un retrait si l’usage est saisonnier | Chaque trimestre ; disparition du besoin signalée | Propriétaire → autorité pour décision de maintien/retrait | Confirmation datée, indicateurs contextualisés, décision et prochaine revue |
| Inventaire et support — CV03, CV06 | Comparer inventaire aux versions réelles, digest, montages, dépendances et fins de support ; toute inconnue possède responsable et échéance | Chaque trimestre ; à chaque changement avant clôture | Mainteneurs, coordination technique → référent sécurité | Inventaire daté, sorties utiles, références de support et tickets |
| Maintenance — CV05 | Examiner alertes et échecs ; restaurer dans un environnement isolé et vérifier données et parcours métier | Suivi hebdomadaire ; restauration avant ouverture, trimestrielle et après modification du mécanisme | Mainteneurs → responsable technique et propriétaire pour le fonctionnel | Rapports de sauvegarde/restauration, résultats et tickets d’échec |
| Mises à jour — CV06 | Rapprocher correctifs disponibles, versions installées et tickets ; vérifier tests, retour arrière et reports approuvés. Aucune échéance dépassée sans exception valide | Chaque mois ; après mise à jour avant clôture | Mainteneurs → responsable technique | Veille de versions, ticket avant/après, tests et éventuelle exception |
| Vulnérabilités — CV07 | Vérifier réception des avis, applicabilité, priorité contextualisée, affectation et respect des délais CV07 ; vérifier la correction ou la compensation, et motiver chaque exclusion | Veille hebdomadaire ; traitement selon CV07 ; revue mensuelle des retards | Mainteneurs → référent sécurité | Registre, sources, qualification, horodatages, décisions et recontrôles |
| Exposition — CV04, CV08 | Faire confirmer le besoin d’exposition ; comparer flux approuvés, pare-feu, publication et écoute réelle ; tester accès autorisés/refusés et chiffrement depuis les zones pertinentes | Avant ouverture/modification ; chaque trimestre | Équipe réseau et mainteneurs → référent sécurité ; propriétaire confirme le besoin | Matrice approuvée, configuration, tests datés et justification métier |
| Exceptions — CV09 | Vérifier approbation, délégation, échéance, justification toujours actuelle, compensations effectives et progression du plan de sortie | Chaque mois ; avant échéance ; immédiatement si risque aggravé | Responsable de suivi → référent sécurité ; autorité renouvelle ou retire | Registre, tests des compensations, avis, décisions et plan de sortie |
| Retrait — CV11 | Vérifier restitution/conservation des données, fermeture des flux/publications, révocation des accès et retrait des ressources dédiées ; contrôler les dépendances partagées | À la date du retrait ; aux échéances de suppression des sauvegardes conservées | Responsable technique et mainteneurs → propriétaire et autorité | Checklist, tests d’inaccessibilité, révocations, inventaire clôturé et sort des sauvegardes |

Pour File Browser, comparer séparément hôte, runtime, image/application,
données et exposition. Un digest inchangé ne dispense pas de revoir les
nouvelles vulnérabilités connues. Un scan ne démontre pas à lui seul que le
besoin métier, la responsabilité ou l’autorisation restent valides.

En cas de service exposé sans usage confirmé ou propriétaire identifié,
appliquer le circuit ajouté à **CV11** : alerte dès constat, pilote provisoire
sous un jour ouvré et dossier/décision sous dix jours ouvrés. Pour les alertes
de vulnérabilité, appliquer le circuit de notification et de clôture de **CV07**.
Ces déclencheurs priment sur la revue périodique.

## 2. Enregistrer le résultat et traiter les écarts

Chaque fiche de contrôle contient : identifiant, service/périmètre, règle CV,
date et contrôleur, méthode, résultat attendu et observé, référence des preuves,
conclusion, relecteur, action, responsable et échéance.

| Conclusion | Traitement |
| --- | --- |
| Conforme | Preuves actuelles couvrant les exigences ; noter la prochaine revue |
| Non conforme | Ouvrir une action ; corriger ou demander une exception avant dépassement de l’échéance |
| Non vérifiable | Signaler la preuve manquante ; affecter sa collecte ou le contrôle avec échéance, sans conclure à la conformité |
| Non applicable | Documenter et faire valider le motif pour le périmètre ; réexaminer si celui-ci change |

Une exception approuvée est référencée comme **écart temporairement autorisé** ;
elle ne transforme pas le résultat en conformité à la règle d’origine.
Les actions échues sont examinées mensuellement par le référent sécurité.
Un danger urgent ou une compensation défaillante suit immédiatement le circuit
d’incident et de décision, sans attendre la revue mensuelle.

Conserver les pièces dans un espace à accès maîtrisé, avec auteur, date,
périmètre et référence du ticket. La fiche publique ne contient ni secrets
ni diagnostics internes complets. La durée de conservation des preuves doit
être fixée avant adoption selon les besoins de suivi de l’organisation.

## 3. Circuit d’une exception

1. **Demander :** le propriétaire identifie la règle précise et l’exigence impossible à respecter, le périmètre, la cause et les solutions examinées. Il propose une durée, un responsable de suivi et un plan de retour à la règle.
2. **Analyser :** les mainteneurs et le référent sécurité décrivent le scénario de risque, l’exposition, les données et impacts, les protections existantes et le risque résiduel après compensation. Un simple score de scanner ne suffit pas.
3. **Décider :** une personne nommée disposant de la délégation appropriée approuve ou refuse par écrit. Le demandeur ou l’administrateur ne s’autorise pas une dérogation sans mandat. L’avis du référent sécurité ne remplace pas cette décision.
4. **Activer :** vérifier les compensations requises avant la prise d’effet, enregistrer les dates, notifier les exploitants et programmer les contrôles. Une demande en attente n’autorise pas à dépasser une règle ; maintenir les restrictions nécessaires jusqu’à décision.
5. **Suivre :** vérifier mensuellement justification et compensations, suivre les étapes du plan de sortie ; réexaminer immédiatement tout changement d’exposition, de vulnérabilité ou de responsabilité affectant le risque.
6. **Réexaminer et clôturer :** avant échéance, apporter la preuve de correction ou demander une nouvelle décision justifiée. Aucun renouvellement tacite. À expiration sans renouvellement, appliquer la règle ou la restriction/suspension prévue par la procédure approuvée ; conserver la preuve de clôture.

La durée maximale proposée par **CV09 est de 90 jours**, avec une date de
réexamen antérieure ou égale à l’expiration. Ce plafond n’impose pas d’accepter
90 jours si le risque demande une durée moindre. Une exception ne peut couvrir
que le périmètre et les exigences expressément autorisés par le décideur.

## 4. Modèle de fiche d’exception

| Champ obligatoire | Contenu attendu |
| --- | --- |
| Identifiant et service | Référence EX, service, composants/versions et périmètre exact |
| Règle concernée | Identifiant CV et exigence précise non respectée |
| Demandeur / propriétaire du risque | Personne nommée et contact |
| Justification | Cause, contrainte, solutions examinées et motif du choix temporaire |
| Risque accepté | Scénario, exposition, données/impacts et risque résiduel après compensation |
| Mesures compensatoires | Mesures, exécutants, preuves d’efficacité et fréquence des tests ; si aucune, justification explicite |
| Avis sécurité | Analyse datée, réserves et recommandation |
| Autorisation | Nom du décideur, délégation, décision datée et conditions ; refus possible |
| Durée | Date de prise d’effet, expiration et date de réexamen, dans la limite CV09 |
| Suivi | Responsable, contrôles prévus, alertes et critères de réexamen anticipé |
| Sortie | Correction/remplacement/retrait prévu, étapes, responsables et échéances |
| État et clôture | Demandée, refusée, approuvée, échue ou clôturée ; références des preuves et dernière décision |

### Exemple pédagogique — Report d’une mise à jour

**Exemple fictif, aucune dérogation réellement accordée.** Un service de
partage doit reporter une correction au-delà du délai CV07 parce qu’un test
de compatibilité a échoué. La demande vise explicitement **CV06 et CV07**.
Le risque proposé à l’acceptation est l’exploitation de la vulnérabilité
qualifiée pouvant donner accès aux documents ; l’absence de compatibilité
n’annule pas ce risque.

Une proposition de compensation limite temporairement l’accès à un VPN et
aux partenaires autorisés, avec surveillance des accès. L’équipe réseau
doit prouver le refus depuis Internet et le mainteneur tester la collecte.
Si ces mesures ne réduisent pas suffisamment le scénario d’exploitation,
le référent sécurité recommande la suspension ou une autre protection.
L’autorité doit décider ; son nom et sa délégation restent à renseigner.

La demande propose 30 jours, un réexamen à J+15 et une sortie par correction
testée ou remplacement. Ces dates sont fixées à partir de la prise d’effet
approuvée. Avant cette approbation et les tests des compensations, l’état
reste **demandée**. Les alertes Trivy du laboratoire ne sont pas acceptées
par cet exemple et doivent conserver leur qualification propre.

## 📦 Livrable

Une matrice de contrôles reliée aux règles CV, une fiche de résultat et un
circuit d’exception avec autorisation, risque, compensations, durée et sortie.
Avant adoption du fragment, valider les personnes, délégations, calendriers,
moyens de contrôle et procédure de restriction/suspension.

- [Règles du cycle de vie](definir-regles-cycle-vie-service.md)
- [Rôles et responsabilités](definir-roles-responsabilites.md)
- [Retour à l’itération 6](index.md)
- [Retour au module](../README.md)
