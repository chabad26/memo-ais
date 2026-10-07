# Tester le fragment de PSSI

***Itération 6 — Travail individuel — 6 octobre 2026***

## 🎯 Objectif et méthode

Vérifier par cinq situations que le fragment permet d’identifier actions,
pilote, décideur et preuves. Il s’agit d’un **test documentaire sur scénarios**,
sans déploiement, incident ou exception réellement exécutés. Le fragment et
ses délais restent proposés à validation.

Documents utilisés : [périmètre](definir-perimetre-fragment-pssi.md),
[rôles](definir-roles-responsabilites.md),
[règles CV01–CV11](definir-regles-cycle-vie-service.md) et
[contrôles et exceptions](definir-controles-exceptions.md).

## Situation A — Nouveau service

**Décision : la VM fournie ne suffit pas à autoriser l’application ni sa publication externe.**

1. Le demandeur décrit application, partenaires, données/sensibilité, besoin, durée et disponibilité attendue ; le propriétaire constitue le dossier d’autorisation.
2. Nommer propriétaire, responsable technique, mainteneurs et suppléants. Répartir explicitement VM/OS, Docker, image/application, dépendances, réseau, données et sauvegardes ; vérifier compétences et moyens.
3. Inventorier versions, digest, stockage persistant et fins de support. Préparer procédures, veille, correctifs, supervision, restauration et calendrier des contrôles.
4. Pour les partenaires, faire approuver les flux, chiffrement, habilitations et accès administratifs restreints. Retirer les secrets initiaux ; tester accès permis/interdits et persistance/restauration des données.
5. L’autorité approuve après avis sécurité et tests fonctionnels ; les réserves bloquantes sont levées ou couvertes par une exception valide. Une publication ajoutée ultérieurement reçoit sa propre approbation CV04.

**Règles utilisées :** CV01–CV07, CV08 pour les contrôles futurs, CV09 si dérogation.
**Preuves attendues :** dossier, répartition acceptée, inventaire, matrice de flux,
tests, décision datée et calendrier. Sans décision, ne pas ouvrir aux utilisateurs.

**Informations manquantes dans le scénario :** personnes, délégations, données,
architecture, ports, support et moyens. Le fragment fournit les champs et
le circuit, mais ces valeurs doivent être renseignées avant ouverture.
**Lacune de règle :** aucune bloquante identifiée pour cette situation.

## Situation B — Changement de responsable

**Décision : poursuivre uniquement avec une prise en charge explicite et opérationnelle.**

Le propriétaire désigne un entrant ayant accepté les tâches ou active le
suppléant. Le responsable technique transmet inventaire, procédures, tickets,
alertes, exceptions et échéances. L’entrant teste ses accès et sa capacité de
maintenance ; les destinataires d’alertes sont mis à jour. Retirer les droits
du sortant à son départ et renouveler les secrets partagés qu’il connaît
lorsque nécessaire, sans copier sa clé privée personnelle.

Si le départ est imprévu, activer le suppléant dès notification. Sans couverture,
l’autorité doit décider d’une prise en charge temporaire, restriction ou
suspension avant poursuite ; le besoin métier ne suffit pas à accepter le risque.

**Règles utilisées :** CV02, CV03, CV05, CV10 ; CV09 si dérogation et CV11 si absence
de maintenance durable. **Preuves :** passation acceptée, accès et alertes testés,
révocation du sortant, fiche actualisée et décision éventuelle de continuité.

**Informations manquantes :** entrant/suppléant, date, compétences, accès de secours
et mandat de décision. **Lacune de règle :** aucune bloquante ; vérifier les
valeurs de la fiche, notamment que le suppléant dispose réellement des moyens.

## Situation C — Vulnérabilité

**Décision : qualifier l’alerte, affecter une réponse et vérifier sa réalisation.**

| Question | Réponse issue du fragment complété |
| --- | --- |
| Qui détecte ? | Référent sécurité et mainteneurs nommés, destinataires de la veille éditeur/CERT et des scans ; l’administration métier ne les dispense pas de CV07 |
| Qui informer ? | Le premier informé ouvre un ticket et notifie sécurité, responsable technique, mainteneur concerné et propriétaire sous un jour ouvré ; immédiatement en cas d’urgence crédible. Informer l’équipe principale si ses couches/interfaces sont affectées |
| Qui qualifie ? | Mainteneur et référent sécurité : composant/version, applicabilité, exposition, exploitation, impacts, protections et correction disponible |
| Qui décide ? | Responsable technique coordonne la correction dans son mandat ; propriétaire valide les impacts métier ; autorité arbitre exceptions, restriction/suspension ou dépassement du mandat, sur avis sécurité |
| Comment vérifier ? | Contrôler version/configuration effective, correctif pertinent ou mitigation testée, puis fonctionnement métier. Le référent sécurité examine les preuves ; une simple commande ou baisse du nombre d’alertes ne suffit pas |

Une alerte d’exploitation active crédible sur composant exposé est qualifiée
sous un jour ouvré ; décision de correction/restriction sous 24 heures après
confirmation. Sinon, qualification sous cinq jours ouvrés et traitement sous
15 jours calendaires pour risque élevé, 60 pour les autres après qualification,
ou exception CV09. « Importante » ne suffit pas à établir la priorité locale.

**Règles utilisées :** CV02, CV03, CV06, CV07, CV08 ; CV09 si report.
**Preuves :** ticket horodaté, avis, qualification, notifications, décision,
versions avant/après et contrôles de sécurité/fonctionnement.

**Informations manquantes :** composant/version, applicabilité, exposition,
exploitabilité, correctif et contacts. **Lacune trouvée et corrigée :** CV07
précise désormais notification, correction courante, arbitrage et clôture.
Une compensation temporaire laisse la vulnérabilité ouverte avec exception liée.

## Situation D — Mise à jour impossible

**Décision : documenter l’incompatibilité et arbitrer une solution temporaire, sans report tacite.**

Le mainteneur conserve le test qui montre l’incompatibilité ; le propriétaire
confirme que la fonction est nécessaire. Étudier correction de compatibilité,
version alternative, désactivation de la fonction vulnérable, restriction
d’accès, remplacement ou suspension. Sécurité qualifie le risque résiduel ;
une sauvegarde ou une surveillance seules ne neutralisent pas automatiquement
la possibilité d’exploitation.

Si le délai de correction doit être dépassé, le propriétaire demande une
exception ciblant CV06/CV07 : justification, risque, décideur habilité,
compensations et leurs tests, responsable de suivi, durée, réexamen et plan
de sortie. L’autorité approuve ou refuse après avis sécurité. Les mesures
requises doivent être effectives avant activation. La durée maximale proposée
est 90 jours, ajustée au risque ; revue mensuelle et anticipée si aggravation.
Sans approbation, ou à expiration sans renouvellement, appliquer la règle ou
la restriction/suspension prévue. L’incompatibilité ne clôture pas l’alerte.

**Règles utilisées :** CV05, CV06, CV07, CV09 et circuit des exceptions ; CV11
si remplacement/retrait. **Preuves :** tests d’incompatibilité, alternatives,
fiche approuvée, compensations vérifiées, échéances et preuve de sortie.

**Informations manquantes :** fonction, résultats des tests, risque,
compensations efficaces, décideur et dates. **Lacune de règle :** aucune
bloquante ; le modèle d’exception fournit les champs nécessaires.

## Situation E — Service ancien

**Décision : ouvrir une enquête attribuée et une revue de l’exposition, sans supposer l’abandon.**

1. Dès découverte, notifier sécurité et autorité. Celle-ci désigne sous un jour ouvré un pilote provisoire ; l’enquête ne dépend pas d’un propriétaire encore inconnu.
2. Examiner flux/publication, versions/support, données, accès et sauvegardes. Rechercher service demandeur, utilisateurs et dépendances ; consulter l’activité disponible en tenant compte des usages saisonniers.
3. Constituer le dossier sous dix jours ouvrés. L’autorité consigne dans ce délai une décision : maintien justifié avec responsables et conditions, restriction pendant investigation, remplacement ou retrait. Une dérogation exige CV09.
4. Si risque urgent, suivre immédiatement le circuit de restriction prévu ; ne pas attendre dix jours. Ne pas effacer de données pendant la recherche sans décision sur leur sort.
5. Si retrait décidé, appliquer CV11 : restitution/conservation, fermeture des publications et flux, révocation des accès, retrait des ressources dédiées, contrôle externe et inventaire clôturé.

**Règles utilisées :** CV02, CV03, CV04, CV07, CV08, CV11 ; CV09 si maintien dérogatoire.
**Preuves :** ticket, nomination provisoire, enquête, contacts/indices d’usage,
analyse de risque, décision datée et contrôles de son effet.

**Informations manquantes :** propriétaire, besoin, utilisateurs, dépendances,
données et support. **Lacune trouvée et corrigée :** CV11 inclut désormais le
besoin inconnu et prévoit pilote provisoire, délai d’enquête/décision et traitement
immédiat d’un risque urgent. Absence de trafic ne signifie pas absence d’usage.

## Bilan du test et compléments intégrés

| Situation | Résultat documentaire | Complément intégré |
| --- | --- | --- |
| A | Circuit de mise en service déterminable | Aucun ajout de règle nécessaire |
| B | Continuité et passation déterminables | Aucun ajout de règle nécessaire |
| C | Circuit désormais explicite | CV07 : destinataires, délai de notification, mandat de correction, arbitrage et clôture |
| D | Exception et sortie déterminables | Aucun ajout de règle nécessaire |
| E | Prise en charge désormais possible sans propriétaire connu | CV11 : pilote provisoire, besoin inconnu, délai et décision |

Les cinq scénarios peuvent être traités avec le fragment **après les compléments**.
Ce résultat porte sur la cohérence rédactionnelle, pas sur une conformité
opérationnelle. Avant adoption, renseigner les nominations, délégations et
contacts, valider les moyens et délais, ainsi que le canal urgent et la
procédure autorisant restriction/suspension. Aucun risque réel n’est accepté
par cet exercice.

- [Règles complétées](definir-regles-cycle-vie-service.md)
- [Contrôles et exceptions](definir-controles-exceptions.md)
- [Retour à l’itération 6](index.md)
- [Retour au module](../README.md)
