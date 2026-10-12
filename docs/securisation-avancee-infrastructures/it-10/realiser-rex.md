# Réaliser le REX

**Itération 10 — 12 octobre 2026 — Olivier HIMBLOT — Travail individuel — 1 h**

## 🎯 Objectif et référence du scénario

Comparer l’investigation au script fourni, expliquer les écarts et proposer
des améliorations techniques et organisationnelles. Ce REX complète le
[compte-rendu d’incident](compte-rendu-incident.md), dont la version précédente
conserve les conclusions formulées avant cette étape.

**Référence examinée :** `j9-filebrowser-incident.sh`, fichier déjà transmis
par Olivier comme provenant du formateur, disponible dans Downloads.
Aucune nouvelle variante n’est jointe à cette consigne : la comparaison porte
sur cette copie. Si la version révélée diffère, le tableau devra être révisé.
Empreinte SHA-256 calculée lors de cette rédaction :

```text
e185f5da52fbab1f6327803046b78736b769a18a78b3fee49d8938ebe731689d
```

Le script a été **lu, pas relancé** pour réaliser le REX. Son code décrit
les activités prévues ; leur réalisation est établie séparément par les
preuves. Les résultats de reproduction depuis l’hôte ne certifient pas
rétroactivement chaque phase de l’essai initial sur la VM.

## 1. Ce que génère le script

Le commentaire demande une exécution depuis une machine différente de la
VM cible. Le port HTTP par défaut est 8080, modifiable par
`FILEBROWSER_PORT`. Deux commandes Nmap suivent :

- `nmap -Pn -p 22,80,443,8000,8080,8443 "$TARGET"` ;
- `nmap -Pn -p 1-1000 "$TARGET"`, après une pause de 20 secondes.

Après 30 secondes, deux GET `/` sont espacés de 5 secondes. Après une pause
de 20 secondes, huit chemins sont demandés, avec une pause de 3 secondes
après chacun : `/admin`, `/backup`, `/private`, `/config`, `/config.json`,
`/.env`, `/debug`, `/old`. Après 20 secondes supplémentaires, douze GET
`/admin` sont exécutés avec une pause de 2 secondes après chacun.

**Total prévu : 22 GET, dont 13 `/admin`.** Les pauses représentent 143
secondes, auxquelles s’ajoutent les temps de commandes. La reproduction
observée dure 145 secondes. Les codes HTTP de la dernière boucle ne sont
pas affichés, mais ses douze réponses sont retrouvées dans EVE.

Le code ne prévoit ni connexion applicative, ni POST `/api/renew`, ni accès
`/ais-lab-inhabituel-*`, ni scan des ports 65001–65003, ni commande d’écriture,
d’exploitation ou de persistance. Une requête GET peut avoir un effet selon
le serveur : le code seul ne prouve pas l’absence de conséquence.
`set -u` ne fait pas arrêter le script à chaque échec ; sans `set -e` ni
contrôle des retours, la ligne de fin ne garantit pas la réussite de toutes
les phases. Les corps HTTP sont jetés et curl n’a pas de délai maximal fixé.

## 2. Comparaison avec les preuves disponibles

« Détectée » distingue **événement retrouvé** et **alerte**. Les horaires et
résultats ci-dessous concernent la reproduction du **9 octobre,
14:33:13–14:35:38 CEST**, sauf indication contraire.

| Activité réellement générée | Détectée ? | Correctement interprétée ? | Source | Écart / explication |
| --- | --- | --- | --- | --- |
| Premier scan de six ports | Oui, sortie client : 22/8080 ouverts, 80/443/8000/8443 fermés ; alerte individuelle de ce premier scan non isolée | Oui : exploration contrôlée, pas preuve de compromission | Nmap, script ; EVE pour le contexte réseau | Horaires détaillés et attribution des alertes aux deux scans restent à compléter ; ne pas attribuer toutes les alertes au premier |
| Second scan TCP 1–1000 | Oui, sortie Nmap : 22 ouvert, 999 fermés ; 99 alertes SYN SID 1009001 pendant la phase | Oui : volume SYN, sans compter 99 scans | Nmap et Suricata alert | Alerte de volume, pas signature prouvant Nmap ou intention hostile ; détail par flux manquant |
| Connexions vers ports fermés pendant les scans | Oui dans les résultats client ; détail réseau des refus incomplet | Oui, limites conservées ; pas assimilation à une intrusion réussie | Nmap ; flows EVE à rechercher | SID 1009002 limité à 65001–65003, hors scénario : absence de couverture dédiée par cette règle ; ports fermés connus sans tous les échanges SYN/RST |
| Deux GET `/` | Oui, deux objets HTTP 200 à 14:34:05 et 14:34:10 ; pas alerte dédiée attendue | Oui : accès au service, pas authentification démontrée | Curl et Suricata HTTP | SID 1008002 vise cinq GET `/` en dix secondes ; seulement deux ici |
| Huit chemins inhabituels | Oui, huit GET HTTP 200 entre 14:34:30 et 14:34:51 ; pas alerte HTTP correspondante dans l’extrait | Oui : exploration d’URI ; existence et lecture de fichiers non démontrées | Curl, Suricata HTTP | SID 1009003 vise `/ais-lab-inhabituel-`, pas ces chemins ; corps absents, 200 ≠ divulgation |
| Douze GET répétés `/admin` | Oui, douze objets HTTP 200 entre 14:35:14 et 14:35:36 ; pas alerte HTTP correspondante | Oui : répétition à environ 2 s, pas attaque automatiquement | Suricata HTTP et code du script | Règle de répétition sur `/`, pas `/admin` ; dernière boucle sans affichage client des statuts |
| Essai initial VM vers sa propre adresse | Invocation établie, pas phases réseau complètes | Interprétation corrigée/précisée : angle mort probable, pas non-exécution prouvée | Journald/auditd et archives Wazuh ; route relevée | Trajet local `lo` au contrôle, capteur `virbr0` ; exécution différente du placement demandé par le script |
| GET de reproduction dans les logs applicatifs | Aucun résultat retrouvé dans les recherches documentées | Oui : absence dans le périmètre recherché, sans déclarer Wazuh défaillant | Docker et archives Wazuh agent 001 | Journalisation des accès réussis non établie ; configuration, rotation et couverture à vérifier |

Les [preuves J9](../it-9/incident-premiers-elements.md) et la
[chronologie J10](completer-chronologie.md) donnent les pièces et fenêtres.
Les 99 alertes sont toutes SID 1009001 dans l’extrait analysé ; il ne contient
pas d’alerte HTTP correspondante. Cette observation n’est pas une recherche
exhaustive de tous les journaux.

## 3. Interprétations revues et hypothèses non confirmées

| Proposition ou piste | Résultat du REX | Cause / enseignement |
| --- | --- | --- |
| Navigation Firefox de 14:06 = activité du script | Non confirmée : le script utilise curl et ne demande ni login ni polices ; navigation distincte conservée | **Corrélation** : proximité temporelle et même service ne suffisent pas |
| Arrêt de service voisin = File Browser interrompu par le scénario | Piste résolue par journald/auditd : PackageKit ; aucun lien causal au script démontré | **Événement non identifié**, puis correction par la source locale |
| Essai initial vers 14:06 | Horaire déclaré approximatif précisé : invocation locale à 14:01:59.367435, contexte fermé à 14:04:28.275425 | **Information initialement imprécise** : séparer souvenir, heure locale et réception Wazuh |
| 13:20 = début des accès | Non : borne de recherche choisie | **Interprétation temporelle** : filtre ≠ début prouvé |
| HTTP 200 sur `/.env` = secret lu | Non confirmé par le script ou les métadonnées ; corps absent | **Information absente / interprétation** ; page de repli possible mais non vérifiée |
| Scans puis exploration = exploitation ou persistance | Le script ne contient pas de phase d’exploitation ou de persistance ; aucune preuve de ces effets fournie | **Interprétation** : distinguer comportement, intention et conséquence ; pas certificat d’absence absolue |
| Pas de résultat Docker/Wazuh = pas de requête | Contradit par les 22 GET EVE de reproduction | **Couverture / information absente** : un silence applicatif ne réfute pas une preuve réseau |
| Une alerte de test préalable garantit la couverture du scénario | Non : chemins, volumes et ports différents | **Règle inadaptée au besoin**, malgré fonctionnement sur son propre test |

Ces lignes distinguent les pistes écartées des erreurs effectivement
corrigées. Elles ne prétendent pas que chaque hypothèse avait été adoptée
comme conclusion : le rapport avait déjà gardé la compromission non démontrée.

## 4. Principaux écarts et améliorations techniques

**Propositions, non déployées dans cette activité.** Aucun scan, blocage,
changement de règle ou configuration supplémentaire n’est exécuté ici.

| Écart / cause | Amélioration proposée | Priorité et validation | Impact |
| --- | --- | --- | --- |
| Point d’observation hors trajet local initial | Définir machine d’injection et trajet avant le test ; observer le trajet pertinent, avec source locale complémentaire si nécessaire | Haute pour prochains exercices : relevé route/interface et événement témoin connu ; résultats futurs séparés du passé | Ajout de capture/stockage, risque de doublons à maîtriser |
| Règle HTTP limitée au préfixe de test | Définir une détection de l’exploration des routes sensibles au contexte du service ; ne pas qualifier tout GET de malveillant | Moyenne : besoin, SID distinct, test de syntaxe, positifs et navigation normale | Faux positifs et rechargement possibles |
| Répétition ciblée sur la mauvaise URI | Détecter une fréquence pertinente par origine/service/URI sur fenêtre documentée, dont `/admin` | Moyenne : vérifier scénario et seuil sur référence normale ; conserver avant/après | Bruit et coût ; ne pas compter transactions comme utilisateurs |
| Ports fermés hors règle 65001–65003 | Compléter l’analyse de flows/refus sur les ports réellement sondés ; corréler avec volume SYN | Haute pour compléter dossier si traces conservées ; nouveau test dédié pour valider détection future | Volume de journaux ; RST seul n’identifie ni un scanner ni une intention |
| 99 alertes SYN sur une courte phase | Regrouper par origine, destination, règle et fenêtre ; mesurer avant d’ajuster seuils | Moyenne : comparer tests pertinents et trafic normal, conserver détection utile | Moins de bruit sans perdre les événements nécessaires |
| GET absents des recherches applicatives | Vérifier journalisation réelle, chemins/rotations et collecte ; envisager journal d’accès au point d’entrée | Haute pour visibilité : test distinct HTTP → log → collecte → recherche ; protéger tokens/cookies | Coût, données sensibles et rétention à définir |
| Information de contenu et historique absente | Conserver métadonnées suffisantes, référence de réponse non sensible et état avant/après sur un test autorisé | Selon hypothèse : preuve ciblée, pas capture générale de secrets | Conservation et accès aux preuves à contrôler |
| Confusion potentielle de séquences et heures | Identifiant de test, origine, version/hash du script, UTC/offset, début/fin, code retour et chronologie faits/interprétations | Haute, préparation documentaire ; horloges et réception distinctes | Faible ; ne pas modifier silencieusement le scénario original |

Le prochain contrôle doit associer à chaque activité : événement attendu,
alerte attendue ou simple visibilité, fichier source, filtre et résultat.
Un test négatif pertinent est nécessaire après modification de règle.
Conserver anciennes règles et fenêtre du changement pour pouvoir expliquer
les différences. Les décisions conditionnelles restent dans
[Décider du traitement](decider-traitement.md).

## 5. File Browser : logiciel, exposition et cycle de vie

Le dossier de durcissement décrit une version **2.15.0** historique, puis
une migration vers **2.63.23** et des risques résiduels. Ne pas présenter
la version initiale comme celle du scénario sans relever la version réelle.
La mise à niveau ne prouve ni la correction de tous les défauts ni une
maintenance pérenne. Voir le
[compte-rendu de durcissement](../it-4/finaliser-compte-rendu-durcissement.md).

Au contrôle documentaire du **12 octobre 2026**, le dépôt officiel est
archivé et annonce l’arrêt des nouvelles versions et corrections de sécurité.
Il signale des limites des fonctions d’exécution de commandes et des sessions
JWT. Ces constats justifient un plan de remplacement ; ils ne démontrent pas
leur exploitation dans J9. [Source officielle : File Browser](https://github.com/filebrowser/filebrowser).

Les avertissements de l’éditeur et ses
[avis de sécurité](https://github.com/filebrowser/filebrowser/security/advisories)
sont à intégrer à la veille. Leur applicabilité doit être reliée à la version,
à l’image exacte et aux fonctions/configurations utilisées.

**Exposition démontrée :** publication Docker de 8080 vers 80 sur IPv4/IPv6,
accès HTTP depuis l’hôte du laboratoire. Une écoute sur toutes les interfaces
ne prouve pas une accessibilité depuis Internet. Le périmètre réel doit être
vérifié par trajet et depuis les sources autorisées/interdites ; la présence
d’une règle UFW seule ne prouve pas le filtrage d’un port publié par Docker.

## 6. Améliorations organisationnelles

**Responsables proposés par fonction, à désigner ; aucune adoption de politique
ou action d’entreprise n’est présumée dans ce laboratoire individuel.**

| Besoin | Action organisationnelle proposée | Responsable à désigner | Échéance / preuve attendue |
| --- | --- | --- | --- |
| Propriété du service | Documenter finalité, données servies, utilisateurs autorisés, exposition et dépendances | Propriétaire du service | Avant tout maintien durable : fiche de service validée |
| Inventaire et maintenance | Suivre version applicative, digest d’image, OS, configurations, volumes et fin de support | Administrateur du service | À chaque changement, revue périodique ; inventaire daté et preuve du déploiement |
| Veille et risques résiduels | Suivre avis éditeur/dépendances ; qualifier applicabilité et exposition, assigner traitement avec délai | Référent sécurité et administrateur | À réception d’avis et revue régulière ; registre de risques et suivi des actions |
| Logiciel non maintenu | Décider remplacement ou maintien temporaire explicite, daté, avec restrictions et date de sortie | Propriétaire et responsable sécurité | Prioritaire pour décision de cycle de vie ; échéance et critères de migration, sans promettre des correctifs éditeur inexistants |
| Exposition maîtrisée | Définir sources et ressources autorisées ; vérifier filtrage Docker IPv4/IPv6 et accès effectifs ; étudier point d’entrée TLS/authentification si service conservé | Administrateur réseau/service | Avant exposition élargie ; tests autorisé/refusé et continuité d’administration |
| Droits et sessions | Revoir comptes/droits et gestion des sessions à la lumière des limites documentées ; garder exécution de commandes désactivée si inutile | Propriétaire et administrateur | Configuration effective et tests autorisés ; changement de mot de passe ne certifie pas révocation de tous les jetons |
| Qualité de détection | Tenir matrice activité → source → règle → contrôle positif/négatif, avec propriétaire de chaque règle | Responsable supervision/sécurité | À chaque changement et exercice ; résultats datés et bruit mesuré |
| Conservation et procédure d’investigation | Définir rétention, accès aux preuves, export, fuseaux, escalade et conservation des recherches sans résultat | Responsable sécurité/exploitation | Avant prochain exercice ; procédure testée et pièces accessibles sans secrets dans Git |
| Changements et continuité | Préparer sauvegarde/restauration, validation, fenêtre et retour arrière ; suivre risques après migration | Administrateur et propriétaire | Avant bascule ; test fonctionnel/restauration, décision de remise en service |

Pour le laboratoire, Olivier tient ces rôles pour les tâches individuelles,
le formateur fournit le scénario et les consignes. Dans une organisation,
la responsabilité de maintien d’un service non maintenu et d’acceptation du
risque doit être attribuée explicitement, pas laissée au seul outil de détection.

## 📦 Bilan du REX et suite

**Points solides :** reproduction observable, scans retrouvés, 22 GET et
cadence établis, distinction HTTP 200/contenu réel, rapprochement
journald/auditd/Wazuh, identification PackageKit et prudence sur compromission.

**Écarts principaux :** essai initial local peu visible au capteur, règles
HTTP/ports fermés spécifiques aux anciens tests, bruit SYN, absence de
preuve applicative des GET et de corps/état avant-après. Les causes sont
séparées : placement, couverture de règle, données absentes et corrélation.

Le script explique la reproduction ; il ne prouve pas seul les résultats de
l’essai initial. Ni exploitation ni persistance n’est démontrée par les
pièces. Le plan proposé améliore couverture, traçabilité et gouvernance ;
son efficacité reste à vérifier après mise en œuvre. Aucun incident réel
n’est déclaré résolu par ce REX.

- [Compte-rendu complété](compte-rendu-incident.md)
- [Chronologie et pièces J10](completer-chronologie.md)
- [Qualification](qualifier-situation.md)
- [Retour à l’itération 10](index.md)
- [Retour au module](../README.md)
