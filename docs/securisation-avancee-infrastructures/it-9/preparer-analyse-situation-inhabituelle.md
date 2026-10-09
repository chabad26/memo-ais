# Préparer l’analyse d’une situation inhabituelle

**Itération 9 — 9 octobre 2026 — Travail individuel**

## 🎯 Objectif

Définir une méthode d’investigation avant de recevoir les éléments d’un
incident. Utiliser le dispositif pour examiner une activité que l’on n’a
pas générée soi-même, sans décider à l’avance qu’elle est malveillante.

**Statut : méthode préparatoire.** Aucun premier élément de la situation
à investiguer n’est encore fourni. La chronologie reste vide ; les tests
contrôlés précédents prouvent certaines capacités du dispositif, pas un incident.

## 1. Séparer faits, interprétations et hypothèses

| Nature | Définition | Exemple pédagogique, hors situation à recevoir |
| --- | --- | --- |
| **Fait observé** | Information directement présente dans une pièce identifiée | Un objet EVE porte un POST `/api/renew`, statut 401, heure, IP et SID |
| **Interprétation** | Sens attribué au fait en tenant compte du fonctionnement et du contexte | Le renouvellement de session a été refusé ; ce n’est pas nécessairement un mauvais mot de passe |
| **Hypothèse** | Explication possible, encore à tester | Session expirée, absence de jeton ou utilisation anormale ; rechercher des éléments permettant de les départager |

Conserver la référence de la pièce pour chaque fait. Une capture, une sortie
projetée par `jq` et un objet brut complet n’offrent pas le même niveau de
détail. Une déclaration du participant constitue une information attribuée,
pas une observation technique indépendante.

Une alerte établit une correspondance avec une règle, pas automatiquement
une attaque. Une IP, un user-agent ou un référent ne prouvent pas une identité
humaine. L’absence de résultat ne prouve pas l’absence d’activité si source,
couverture, fenêtre ou rétention sont insuffisantes.

## 2. Questions et informations à chercher

| Question | Informations nécessaires | Sources à consulter | Limite de conclusion |
| --- | --- | --- | --- |
| Que s’est-il passé ? | Type d’événement, méthode, URI, statut, signature et conditions de règle ; action réellement exécutée | Pièce initiale, EVE, logs File Browser, archives/alertes Wazuh | Un motif ou statut ne prouve pas une exploitation |
| Quand ? | Heure de l’action, fuseau, début/fin du flux, horodatage Docker et réception manager | EVE `timestamp`/`flow.start`/`flow.end`, Docker, Wazuh `data.time`/`timestamp` | L’émission tardive d’un flow n’est pas l’heure de début ; décalages à vérifier |
| Quelle origine ? | IP/port source, trajet, initiateur réel, éventuel NAT/proxy, compte si journalisé | EVE, réseau, logs applicatifs/authentification disponibles | Sur une réponse, la source réseau est le serveur ; IP seule ≠ personne |
| Quelle ressource ? | VM/service/port, URI demandée, objet applicatif concerné, réponse effective | EVE HTTP, routes File Browser, logs et métadonnées accessibles | HTTP 200 ne prouve pas un fichier existant ou lu |
| Était-ce autorisé ? | Compte et droits à l’heure des faits, périmètre permis, changement ou test prévu, confirmation du responsable | Journaux d’accès disponibles, configuration des droits, planning/consignes, responsable du service | `action:allowed` indique l’absence de blocage IDS, pas une autorisation métier |
| D’autres événements liés ? | Même fenêtre, origine/destination, compte ou ressource ; séquence avant/après ; erreurs ou changements système | EVE, Docker, Wazuh, journaux SSH/Docker/système si pertinents | Proximité temporelle ou même IP ne suffit pas à établir un lien causal |
| Quelles conséquences ? | Échec/réussite réel, accès/modification/suppression, disponibilité, changement de droits, transfert et intégrité | Logs applicatifs disponibles, état du service, fichiers/métadonnées et référence antérieure, sauvegardes si nécessaires | État actuel seul ne reconstitue pas l’état passé ; volume réseau seul ≠ exfiltration |
| Peut-on parler d’incident ? | Écart établi aux usages/règles, caractère non autorisé, impact ou compromission étayés ; incertitudes restantes | Ensemble des preuves et qualification avec le responsable/formateur | Employer « situation inhabituelle à investiguer » tant que les éléments ne suffisent pas |

Ne pas recopier les mots de passe, jetons ou contenus internes dans les
preuves partagées. Examiner uniquement les données nécessaires à la question
et conserver les originaux utiles avec accès adapté.

## 3. Sources disponibles et ordre d’investigation

### Étape 1 — Cadrer le premier élément et préserver son contexte

Relever qui fournit l’élément, sa source, son heure/fuseau, sa référence et
ce qu’il montre réellement. Définir VM, service et fenêtre initiale, puis
étendre autour de celle-ci selon les nouveaux indices. Ne pas mélanger les
scénarios de test connus avec la situation inconnue.

Conserver les pièces sources avant filtrage ou modification, les commandes
utilisées et les critères de recherche. Vérifier existence des journaux,
rotation/rétention et horodatages. En cas de copie, noter origine et date ;
un condensat peut contrôler l’intégrité de la copie, sans authentifier le
contenu ou son auteur.

### Étape 2 — Retrouver l’activité dans la source initiale

Si le premier élément est une alerte Suricata, commencer par l’objet EVE
et la règle correspondante ; si c’est un événement Wazuh, commencer par
son détail, l’agent, la `location`, le décodeur et la règle éventuelle.
L’ordre s’adapte au premier indice, plutôt que d’ouvrir toutes les sources
sans question précise.

Suricata observe `virbr0` sur l’hôte ; la VM File Browser utilisait
`192.168.122.229:8080` aux dernières preuves. Relire les deux directions
et tous les ports pertinents : les réponses 401 ont pour source la VM,
les scans peuvent viser d’autres ports. Distinguer HTTP, alertes et flows.

### Étape 3 — Rapprocher réseau, application et réception

Chercher l’activité dans les logs Docker File Browser sur sa VM. Dans les
archives Wazuh du manager, rechercher l’agent **001 — vm-filebrowser**,
la fenêtre et le message pertinent, avec la source Docker exacte.
Les archives, alertes et événements indexés dans le dashboard sont des
vues distinctes ; consulter celle qui peut effectivement contenir l’information.

| Source | Apport documenté dans le laboratoire | Vigilance |
| --- | --- | --- |
| Suricata EVE | IP/ports, URI/statuts HTTP, flux et signatures ; tests positifs/négatif documentés | Capture limitée au trajet visible ; chiffrement et règles spécifiques |
| Logs Docker File Browser | Messages applicatifs 401 observés | Tous les accès réussis ne sont pas nécessairement journalisés ; chemin/rotation à confirmer |
| Archives Wazuh | Réception des messages Docker, agent, décodeur JSON et heures | Copie de la même trace, pas une deuxième activité ; alerte applicative dédiée et ingestion EVE non démontrées |
| Dashboard/alertes Wazuh | Événements et contexte effectivement disponibles à examiner | Catégorie MITRE ≠ attaque prouvée ; archives locales pas automatiquement visibles |
| Journaux système, SSH, Docker/audit disponibles | Contexte d’authentification, redémarrage, changement ou erreur à rechercher selon l’indice | Leur collecte et les événements utiles à la situation restent à vérifier |
| Droits applicatifs, consignes et responsable | Autorisation et contexte métier | Configuration actuelle ou déclaration seule ne prouve pas l’état exact à l’heure des faits |

Normaliser les heures, en gardant aussi les valeurs originales : les preuves
J9 montrent CEST côté EVE et UTC côté Docker/manager. Vérifier cela pour
les nouveaux éléments, sans appliquer automatiquement le décalage à toutes
les sources. Un `flow_id` peut porter plusieurs transactions et n’est pas un
identifiant commun avec Wazuh.

### Étape 4 — Qualifier l’autorisation et les conséquences

Comparer l’activité aux usages attendus, comptes/droits et opérations prévues.
Chercher une conséquence directement observable, en distinguant état initial,
état après l’activité et état actuel. Si une information n’est pas journalisée,
noter le manque et le moyen de vérification possible, sans le remplacer par
une certitude.

Commencer par les lectures et copies utiles. Ne pas redémarrer, modifier les
règles ou relancer un scénario pour « reproduire » la situation avant d’avoir
conservé les éléments susceptibles d’être perdus. Si un impact en cours est
établi, préciser les faits et le besoin de décision au responsable/formateur ;
ne pas déduire une mesure de confinement d’une alerte isolée.

### Étape 5 — Construire la chronologie et tester les hypothèses

Inscrire les événements dans l’ordre du temps de l’activité, avec la provenance
et les éventuels écarts d’horloge. Rapprocher les pièces indépendantes et
identifier les copies : Docker puis archives Wazuh constituent une chaîne de
réception du même message.

Pour chaque hypothèse, écrire quel résultat la renforcerait et quel résultat
la contredirait. Une recherche sans résultat conserve son périmètre et ses
limites. Mettre à jour la conclusion lorsque les preuves évoluent, sans effacer
les étapes qui expliquent le changement de qualification.

## 4. Chronologie vide à compléter

**Aucun événement de la situation inconnue n’est encore reçu.** Les lignes
restent volontairement vides ; les scénarios pédagogiques précédents ne sont
pas insérés comme éléments d’un incident.

| Heure | Source | Événement / fait | Interprétation | Niveau de confiance | À vérifier |
| --- | --- | --- | --- | --- | --- |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |

Dans « Événement / fait », indiquer la référence de pièce et les champs
observés. Dans « Interprétation », séparer explicitement **interprétation**
et **hypothèse** si plusieurs explications sont possibles. Conserver heure
originale/fuseau et heure normalisée lorsqu’elles diffèrent.

| Confiance | Quand l’utiliser |
| --- | --- |
| Élevée | Fait directement documenté, source/temps identifiés et contexte cohérent ; préciser les limites restantes |
| Moyenne | Élément partiel ou rapprochement plausible, avec une vérification importante manquante |
| Faible | Hypothèse peu étayée, provenance incertaine ou contradictions non résolues |
| Non vérifiable | Source ou information indispensable indisponible pour statuer |

La confiance porte sur la **proposition écrite**, pas sur la gravité supposée.
Un fait technique fiable peut soutenir une interprétation encore incertaine.

## 5. Suivi des hypothèses et conclusion provisoire

| Hypothèse | Faits qui la soutiennent | Vérification / source | Élément qui la contredirait | État |
| --- | --- | --- | --- | --- |
| À définir après réception | | | | |
| À définir après réception | | | | |

Préparer une conclusion en quatre points : faits établis, explications
possibles, conséquences démontrées ou inconnues, prochaines vérifications.
Retenir une qualification justifiée : activité normale expliquée, activité
inhabituelle encore indéterminée, ou incident étayé par les éléments réunis.
Ne pas confondre « conséquences inconnues » avec « aucune conséquence ».

## 📦 Livrable préparatoire

- Méthode d’investigation et ordre de consultation des sources.
- Questions/informations nécessaires et limites du dispositif.
- Chronologie vide et tableau d’hypothèses prêts à compléter.
- Distinction explicite fait observé / interprétation / hypothèse.

**État attendu avant réception :** savoir où commencer, quoi conserver et
comment vérifier une explication. L’analyse effective commencera avec les
premiers éléments fournis.

- [Capacité de détection vérifiée](verifier-capacite-detection.md)
- [Vue exploitable des événements](construire-vue-exploitable-evenements.md)
- [Retour à l’itération 9](index.md)
- [Retour au module](../README.md)
