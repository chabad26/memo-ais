# Réviser le fragment de PSSI

**Itération 10 — 12 octobre 2026 — Travail individuel — 1 h 30**

## 🎯 Objectif

Faire évoluer les règles à partir de l’audit et du REX : attente explicite,
responsabilité attribuée et contrôle permettant de constater un résultat.
La PSSI définit les exigences ; les procédures choisissent les moyens adaptés.

**Travail produit :** tableau de révision et [fragment V2 proposé](fragment-pssi-v2.md),
autonome, conservant les exigences de la [V1](../it-6/fragment-pssi-v1.md).
**V1 conservée sans modification ; V2 non adoptée.** Aucune configuration,
restriction ou validation d’entreprise n’est réalisée par cette rédaction.

## 1. Base de révision et limites

Le [REX](realiser-rex.md) établit scans, 22 GET et 99 alertes SYN dans la
reproduction ; il explique les écarts de règles et le point d’observation.
Les GET réussis ne sont pas retrouvés dans les recherches Docker/Wazuh
montrées. Une invocation locale initiale ne prouve pas toutes les phases.
Ni exploitation ni exposition Internet du laboratoire n’est démontrée.

L’audit et le cycle de vie File Browser justifient inventaire par couche,
maintenance attribuée, risques résiduels et décision de remplacement ou
maintien temporaire encadré. Une mise à niveau ne rétablit pas la maintenance
d’un produit abandonné. Les conclusions de laboratoire ne sont pas une
preuve de manquement d’une équipe métier ou IT réelle.

## 2. Tableau des évolutions

| Enseignement du REX | Règle V1 | Modification | Contrôle |
| --- | --- | --- | --- |
| Un service utilisable peut rester insuffisamment surveillé | CV01 : dossier et autorisation avant ouverture | Ajouter besoin de surveillance, sources/limites, contacts et tests de visibilité selon risque ; prévoir cycle de vie | Responsable technique apporte résultats ; propriétaire présente dossier ; autorité vérifie décision antérieure à ouverture, réserves ou exception valide |
| Le traitement d’une alerte exige des rôles distincts | CV02 : responsables et mainteneurs par couche | Attribuer réception, qualification, conservation, coordination et pouvoir de décision ; maintenir distinction IT/métier | Propriétaire et responsable technique font attribuer un signalement, une alerte OS et une alerte applicative ; référent sécurité relève tout rôle sans moyens |
| Trajet local hors capteur et collecte applicative limitée | CV03 : inventaire composants/flux | Ajouter points d’entrée, périmètres observés, chaîne de collecte, rétention et responsables ; dater inconnues | Mainteneurs rapprochent inventaire et configuration ; responsable technique documente les angles morts et affecte actions/décisions |
| Écoute réseau et publication ne prouvent pas le filtrage | CV04 : matrice et tests admis/interdits | Contrôler trajet effectif, relais/redirections et familles d’adresses applicables ; distinguer Internet supposé et accès testé | Équipe réseau/mainteneurs testent depuis zones pertinentes ; référent sécurité compare résultats et autorisations, propriétaire confirme besoin |
| Source active ≠ événement retrouvable | CV05 : supervision et diagnostic | Documenter chaîne de collecte, conservation et recherche des événements utiles | Mainteneurs génèrent un événement autorisé de référence et le retrouvent ; responsable technique contrôle sa provenance et sa portée |
| Dernière version installée ≠ logiciel maintenu | CV06 : mises à jour et migrations | Conserver ticket/tests/retour arrière, ajouter suivi du support et du risque résiduel après mise à niveau | Mainteneur vérifie version réelle et support ; responsable technique relie risque non clos à CV07/CV09/CV11 |
| Avis et compteurs ne prouvent pas exploitation/correction | CV07 : veille contextualisée et délais | Suivre fin de maintenance/limites non corrigées ; relier chaque décision à composant exact et preuves, sans clôture par compteur seul | Référent sécurité examine applicabilité, exposition, délais, recontrôle et exclusions justifiées |
| Règles de test fonctionnelles mais hors chemins/ports du scénario | CV08 : contrôles trimestriels | Ajouter matrice activité/source/événement/alerte, positifs et usages normaux ; vérifier trajet, bruit et limites avant ouverture, trimestriellement et après changement pertinent | Mainteneurs réalisent tests autorisés ; référent sécurité vérifie événement, alerte attendue ou limite ; absence d’alerte n’est pas conformité globale |
| Maintien d’un produit abandonné et visibilité insuffisante sont des risques ouverts | CV09 : exception ≤ 90 jours, compensations et sortie | Préciser couverture réelle, risque non compensé et sortie datée ; exercice réussi ≠ acceptation ; pas renouvellement implicite | Autorité approuve dans son mandat ; suivi mensuel des compensations et échéances, décision avant renouvellement |
| Nouvelle personne doit pouvoir recevoir et investiguer | CV10 : passation acceptée et droits testés | Transmettre dossiers ouverts, preuves, règles/limites et circuit d’incident ; contrôler notification et recherche par entrant | Propriétaire organise, responsable technique vérifie réception/recherche habilitée et retrait des droits inutiles |
| Produit téléchargeable sans corrections et preuves à conserver | CV11 : fin de support, décision sous dix jours ouvrés | Inclure arrêt de maintenance, plan de sortie/continuité et sort des preuves avant destruction | Propriétaire prépare décision ; autorité arbitre ; responsable technique vérifie retrait complet, données et pièces conservées selon décision |
| Scans, 200 ou silences ne suffisent pas à qualifier ; coupure systématique disproportionnée | CV05/CV07/CV08 : circuit d’incident évoqué, sans règle complète autonome | **Ajouter CV12** : dossier, faits/hypothèses, chronologie, qualification, mesures proportionnées, validation reprise/clôture et REX suivi | Référent sécurité examine un dossier/exercice ; autorité vérifie mandat et décisions ; responsables démontrent effet des mesures, limites et actions de REX |

La V2 ne réécrit pas les règles comme si elles étaient absentes de la V1 :
CV01–CV11 sont précisées ; CV12 comble la description incomplète du circuit
d’incident. Les délais V1 sont conservés et restent à valider avec les moyens.

## 3. Formulation attendue et liberté des moyens

Une règle indique **résultat, périmètre, responsable et vérification**.
Par exemple : « les activités retenues dans la matrice de surveillance
produisent des événements retrouvables ; les alertes attendues et angles
morts sont documentés ». La procédure peut employer un capteur réseau,
des journaux applicatifs ou une autre source adaptée.

La V2 n’impose ni Suricata, ni Wazuh, ni Docker, ni une règle sur `/admin`
pour tous les services. Ces outils et chemins sont des exemples du laboratoire.
Le résultat attendu est une couverture utile et vérifiée pour le service.
De même, les décisions d’arrêt/isolation répondent à un risque et un mandat,
pas au simple déclenchement d’une alerte.

## 4. Contrôle documentaire de la proposition

| Question de relecture | Résultat documentaire | Limite / suite |
| --- | --- | --- |
| Les neuf thèmes demandés sont-ils couverts ? | CV01 nouveaux services ; CV02 responsabilités ; CV03/CV04 inventaire/exposition ; CV06/CV07 vulnérabilités ; CV08 contrôles ; CV12 incidents ; CV10 changement de responsable ; CV09 exceptions ; CV11 fin de vie | Couverture écrite, pas exécution prouvée |
| Une autorité et des exécutants sont-ils identifiables ? | Rôles conservés, circuit incident précisé | Personnes, délégations, suppléants et moyens à désigner/valider |
| Peut-on vérifier une détection ? | Matrice, événement retrouvé, alerte attendue ou limite et tests de référence exigés | Résultats opérationnels de V2 non produits par la rédaction |
| Les conséquences et décisions restent-elles proportionnées ? | Faits/hypothèses séparés, impact service/preuves et contrôle de reprise exigés | Décision réelle nécessaire avant mesure hors mandat |
| Exception ou fin de vie peuvent-elles être suivies ? | Échéance, compensations, risque résiduel, sortie et conservation des preuves | Acceptation du risque non effectuée |
| V1, V2 et adoption sont-elles distinguées ? | V1 inchangée, V2 proposée et versionnée séparément | Aucune date d’effet ou approbation inventée |

Cette relecture vérifie la précision des exigences. Elle ne constitue pas
un test technique du dispositif ni une adoption de PSSI.

## 5. Étapes de validation restantes

1. Faire relire la proposition par propriétaire, responsable technique et référent sécurité ; valider interfaces avec les autres procédures/politiques.
2. Désigner personnes, suppléants et délégations ; fixer moyens, rétention selon sensibilité et faisabilité des délais proposés.
3. Tester documentairement un nouveau service, un incident à visibilité partielle, une passation et un maintien temporaire sans support ; traiter les ambiguïtés.
4. Faire décider périmètre, réserves, approbateur et date d’effet par l’autorité compétente ; communiquer aux rôles concernés après adoption réelle.
5. Planifier contrôles et actions de mise en conformité ; conserver écarts et exceptions, puis vérifier les résultats après application.

## 📦 Livrables

Tableau REX → V1 → modification → contrôle, fragment V2 autonome proposé,
relecture documentaire et étapes de validation. Les risques et preuves du
compte-rendu restent distincts de ces règles. Aucun incident n’est déclaré
clos par la révision de PSSI.

- [Fragment de PSSI V2 proposé](fragment-pssi-v2.md)
- [V1 conservée](../it-6/fragment-pssi-v1.md)
- [REX](realiser-rex.md)
- [Retour à l’itération 10](index.md)
- [Retour au module](../README.md)
