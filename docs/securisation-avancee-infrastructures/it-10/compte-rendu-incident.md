# Produire le compte-rendu d’incident

**Itération 10 — 12 octobre 2026 — Olivier HIMBLOT — Travail individuel**

## 🎯 Objectif et état du rapport

Formaliser l’investigation, les résultats et les décisions prises à partir
des pièces disponibles de J9 et J10. Ce compte-rendu constitue la version
remise **avant communication du scénario réellement exécuté par le formateur**.
La rédaction est finalisée à ce stade ; la qualification reste provisoire.

**Conclusion actuelle :** une reproduction contrôlée montre une exploration
de ports puis 22 requêtes HTTP vers File Browser, avec 99 alertes Suricata
sur le volume SYN. Aucune compromission n’est démontrée. Le déroulement
complet de l’activité initiale et ses conséquences restent insuffisamment
établis. La reproduction ne remplace pas les preuves de cette activité.

## 1. Signalement initial et périmètre

> Plusieurs accès à des pages ou ressources inattendues ont été observés sur le service File Browser.

Le signalement ne donne initialement ni origine, ni intention, ni conséquence.
La borne **13:20 le 9 octobre 2026** a été choisie pour les recherches ;
elle ne constitue pas un début d’activité prouvé ou une période confirmée
par le formateur.

Le périmètre étudié comprend la VM File Browser **192.168.122.229:8080**,
l’hôte **192.168.122.1**, le capteur Suricata sur **virbr0** et le manager
Wazuh **192.168.122.37**, agent **001 — vm-filebrowser** installé sur la VM.
Les contrôles disponibles sont datés ; ils ne certifient pas l’état actuel
ou permanent du dispositif.

Olivier indique avoir reçu un script de son formateur. Le code transmis et
sa reproduction sont connus ; **ils ne constituent pas la révélation du
scénario réellement exécuté par le formateur**. Trois séquences restent
séparées : invocations locales initiales, navigation Firefox, reproduction
sur trajet réseau observable.

## 2. Sources utilisées et portée

| Référence | Source / pièce | Apport établi | Limite |
| --- | --- | --- | --- |
| P1 | [Analyse J9, extraits EVE, sortie du script et captures](../it-9/incident-premiers-elements.md) | Métadonnées réseau, URI, réponses HTTP, alertes et résultats Nmap de reproduction | Extraits, sans corps HTTP ; pas capture exhaustive de l’activité initiale |
| P2 | Script `j9-filebrowser-incident.sh` transmis | Enchaînement prévu des tests et temporisations | Code ≠ preuve d’exécution complète ; scénario formateur non communiqué |
| P3 | [Chronologie J10, journald et auditd de la VM, captures](completer-chronologie.md) | Commandes sudo, sessions, installation Nmap, identification de PackageKit | Pas journal de chaque GET ; état historique limité aux traces conservées |
| P4 | Archives Wazuh agent 001, reprises dans P1/P3 | Contexte système initial et réception d’événements locaux | Heure de réception distincte de l’activité ; recherches Docker de reproduction sans résultat |
| P5 | Logs Docker File Browser et recherches documentées dans P1 | Résultat vide sur la fenêtre de reproduction, commande Docker terminée avec code 0 | Ne prouve ni absence d’accès ni panne de collecte ; journalisation des GET réussis non établie |
| P6 | Relevés `ip route get`, contrôles Docker et [tests de capacité J9](../it-9/verifier-capacite-detection.md) | Trajet local VM / trajet hôte, fonctionnement démontré sur certains tests distincts | Ne pas transférer les résultats des ports 65001–65003 au scénario reproduit |

Les captures et sorties sont les pièces fournies par Olivier. Leur intégration
au mémo ne garantit pas la conservation indépendante et complète des journaux
originaux. Les objets, commandes, filtres et fenêtres détaillés restent dans
les feuilles référencées ; aucun export intégral ni empreinte n’est présumé réalisé.

## 3. Chronologie consolidée

**Événements du 9 octobre 2026, heures CEST (UTC+02:00).** Les recherches
complémentaires ont été réalisées le 12 octobre. Les heures UTC des journaux
locaux/Wazuh sont converties ; réception et heure locale ne sont pas confondues.

| Heure | Source | Fait observé | Interprétation / limite | Confiance |
| --- | --- | --- | --- | --- |
| 13:20 | Choix de fenêtre, P1 | Borne de recherche retenue | Pas début démontré des accès | Élevée pour le choix |
| 13:58:05–13:58:06 | Journald, P3 | Session SSH oliv depuis l’hôte, acceptation de clé puis déconnexion | Session réussie ; lien avec le script non établi | Élevée |
| 13:59:59.576382 | Journald, P3 | Invocation du script sans argument, contexte fermé immédiatement | Sortie réelle non fournie | Élevée pour invocation |
| 14:00:14.389756–14:01:17.061689 | Journald/auditd, P3 | Invocation avec cible VM, puis fermeture du contexte | Phases et résultat non démontrés | Élevée pour contexte |
| 14:01:27–14:01:56 | Journald, dpkg/Wazuh, P1/P3/P4 | apt update, apt install nmap et installation documentés | Préparation administrative, pas conséquence hostile prouvée | Élevée |
| 14:01:59.367435–14:04:28.275425 | Journald/auditd, P3 ; Wazuh P4 | Nouvelle invocation vers la propre adresse VM, PID 159232, fin du contexte | Routage local relevé ultérieurement ; déroulement détaillé manquant | Élevée pour contexte |
| 14:06:18–14:06:31 | Suricata HTTP, P1 | Dix requêtes Firefox depuis l’hôte, login/liste/polices/réglages, réponses 200 | Compatible avec navigation normale ; identité et autorisation applicative non prouvées | Élevée pour champs |
| 14:06:58.250834–.253069 | Journald/auditd, P3 ; Wazuh P4 | Arrêt du daemon PackageKit et service désactivé | Ne constitue pas un arrêt File Browser ; causalité au scénario non établie | Élevée |
| 14:33:13 | Terminal hôte, P1 | Début de la reproduction vers VM:8080 | Nouvelle activité contrôlée distincte de l’essai initial | Élevée |
| Phase de reconnaissance | Nmap, P1/P2 | 22 et 8080 ouverts ; 80,443,8000,8443 fermés ; second scan 1–1000 : 22 ouvert, 999 fermés | États rapportés par le client ; horaires précis et flows de refus à compléter | Élevée pour sortie |
| 14:33:35.132231–.137781 | Suricata, P1 | 99 alertes SID 1009001, source hôte vers VM, action allowed | Volume SYN détecté ; ni 99 scans ni blocage démontrés | Élevée |
| 14:34:05.148812 et 14:34:10.158378 | Suricata/curl, P1 | Deux GET `/`, réponses 200 | Accès au service observés | Élevée |
| 14:34:30.167933–14:34:51.227912 | Suricata/curl, P1 | Huit GET : `/admin`, `/backup`, `/private`, `/config`, `/config.json`, `/.env`, `/debug`, `/old`, tous 200 | Exploration de chemins, pas preuve de fichiers lus | Élevée |
| 14:35:14.245318–14:35:36.343031 | Suricata, P1 | Douze GET `/admin`, tous 200, environ 2 s entre accès | Répétition observée ; aucun SID HTTP correspondant dans l’extrait | Élevée |
| 14:35:38 | Terminal, P1 | Fin affichée du scénario | 22 GET confirmés par EVE, dont 13 `/admin` au total | Élevée |
| Recherches sur 14:33:13–14:36:00 | Docker/Wazuh P1/P5 ; auditd P3 | Sélections sans résultat sur les fenêtres documentées | Couverture limitée ; ne contredit pas les traces réseau | Élevée pour résultats transmis |

Les copies Wazuh et journaux locaux corroborent le contexte initial, mais
ne sont pas deux activités indépendantes. Suricata et la sortie client
corroborent la reproduction. Aucun rapprochement ne permet d’attribuer tous
les événements voisins au même script.

## 4. Faits établis, hypothèses et limites

| Proposition | Éléments | Statut |
| --- | --- | --- |
| Reproduction depuis 192.168.122.1 vers 192.168.122.229 | Terminal et adresses EVE, P1 | **Établie** |
| Exploration de ports, accès au service, exploration HTTP puis répétition | Nmap, script et ordre des 22 GET, P1/P2 | **Établie pour la reproduction** |
| Détection du volume SYN | 99 alertes SID 1009001, P1 | **Établie** ; allowed ne signifie pas autorisation métier |
| Réponses HTTP 200 aux chemins inhabituels | Curl et EVE, P1 | **Établie** pour le protocole, sans preuve du contenu |
| Manque de visibilité initiale lié au trajet local | Invocation VM vers elle-même, route lo relevée et capteur virbr0, P3/P6 | **Probable** ; pas capture du trajet historique |
| Les 200 correspondent à une page applicative de repli | Comportement compatible, corps absents | **Hypothèse à vérifier** |
| Exploitation, accès non autorisé, divulgation, modification applicative ou persistance | Pas de preuve directe de ces effets dans les pièces | **Non démontrés** ; absence absolue non certifiée |
| Scénario initial exécuté intégralement comme la reproduction | Invocations seules, sortie initiale manquante | **Non démontré** |
| Scénario réel et intention du formateur connus | Information explicitement non communiquée | **Non établis** |

Restent à rechercher : corps/routage applicatif des réponses, contexte de
compte et droits, état avant/après des données, traces locales de l’essai
initial, flows des ports refusés, couverture et rétention des journaux.
Une recherche vide doit garder ses filtres et sa fenêtre ; une nouvelle
expérience ne créera pas la preuve historique manquante.

## 5. Qualification

**Activité de reconnaissance et d’exploration HTTP démontrée dans une
reproduction pédagogique. Situation initiale à qualification provisoire ;
compromission non démontrée.** Une succession scan → accès au service →
exploration HTTP ne prouve pas à elle seule une attaque réussie.

Aucune indisponibilité mesurée, exfiltration ou modification applicative n’est
établie. L’arrêt PackageKit ne démontre pas une interruption de File Browser.
Les conséquences au-delà des réponses réseau restent inconnues. Le rapport
ne conclut ni à une compromission certaine ni à l’absence certaine d’incident.

## 6. Actions immédiates et décisions prises

Les [décisions de traitement](decider-traitement.md) sont documentées ; leur
exécution technique ne doit pas être présumée.

| Action | Décision / état | Justification et impact | Vérification attendue |
| --- | --- | --- | --- |
| Documenter les pièces et lectures | **Réalisé :** feuilles, captures, chronologie et résultats transmis intégrés | Traçabilité du raisonnement ; ne remplace pas les originaux | Références et distinction des fenêtres contrôlées dans le mémo |
| Conserver les journaux originaux utiles | **Priorité immédiate**, exports complets à compléter si disponibles | Limiter pertes par rotation ; copie ciblée, stockage à maîtriser | Provenance, couverture, lisibilité des copies et empreintes si réalisées |
| Observation et lectures ciblées | **Retenues pour la suite**, hors lectures historiques déjà réalisées | Préciser les hypothèses avec faible impact ; éviter d’altérer l’état | Disponibilité actuelle des sources, période, résultats et limites consignés |
| Restriction, blocage, isolation ou arrêt | **Différés et conditionnels ; non exécutés dans cette activité** | Aucune menace active ou conséquence établie justifiant l’impact sur service et preuves | Réévaluation si accès non autorisé, exploitation ou impact mesuré ; périmètre et retour arrière à prévoir |

## 7. Remédiations proposées et prochaines investigations

| Proposition | Échéance / priorité | But et vérification | Impact à encadrer |
| --- | --- | --- | --- |
| Clarifier journalisation des accès applicatifs et collecte Wazuh | Prochaine investigation ciblée | Expliquer le silence sur les GET réussis ; contrôler collecte de bout en bout lors d’un test distinct, pas preuve rétroactive | Volume/rétention, données sensibles et éventuel changement de configuration |
| Adapter détection HTTP et réglage du bruit SYN | Préparation différée | Règles actuelles ne couvrent pas tous les chemins/répétitions ; tests positifs et usages normaux, SID distincts, comparaison avant/après | Faux positifs, coût et rechargement à planifier ; aucune nouvelle règle déclarée installée |
| Compléter la visibilité de l’essai local | Investigation selon pièces disponibles | Rechercher traces historiques ; envisager point de capture adapté pour tests futurs | État courant distinct du passé, ne pas multiplier les injections |
| Vérifier réponses applicatives, droits et état des données | Priorité selon hypothèse précise | Distinguer page de repli, accès réel et modification ; conserver références avant/après | Lectures autorisées et ciblées ; nouvelle réponse ne prouve pas ancien contenu |
| Vérifier besoin de maintenance / mises à jour | Différé | Versions et applicabilité à qualifier ; sauvegarde, retour arrière et test fonctionnel | Interruption et compatibilité possibles ; pas correction supposée d’une exploitation non établie |

Limiter ou interrompre le service deviendrait à réexaminer si un nouvel
élément établissait une exposition sensible, une activité non autorisée,
une exploitation ou une dégradation en cours. Consigner alors décideur,
heure, périmètre, impact sur preuves et service, contrôle et retour arrière.

## 📦 Remise et suite

Ce rapport rassemble le signalement, la chronologie, les sources, les faits,
les hypothèses, la qualification et les décisions. Les pièces détaillées
restent accessibles dans les références P1 à P6 et les feuilles J10.

**À réception du scénario réel du formateur :** comparer les faits attendus
aux événements retrouvés, expliquer les écarts de visibilité et réviser la
qualification avec les nouvelles pièces. Garder cette version antérieure
pour distinguer ce qui était démontré de ce qui sera appris ensuite.
La situation reste ouverte ; aucune clôture d’incident n’est prononcée.

- [Qualification détaillée](qualifier-situation.md)
- [Décisions et impacts](decider-traitement.md)
- [Chronologie et captures J10](completer-chronologie.md)
- [Retour à l’itération 10](index.md)
- [Retour au module](../README.md)

## Complément — REX du 12 octobre 2026

Le [REX](realiser-rex.md) compare le script fourni aux événements et aux
conclusions. La version ci-dessus est conservée comme état antérieur à cette
étape ; la copie disponible du script sert de référence, sans nouvelle
variante transmise ni preuve rétroactive de l’essai initial.

**Bilan :** scans et 22 GET confirmés dans la reproduction ; 99 alertes SYN,
pas alerte HTTP correspondante dans l’extrait. Écarts expliqués par point
d’observation local, règles visant d’autres ports/URI, absence de corps et
de traces applicatives. Firefox reste distinct ; PackageKit est identifié.
Compromission, divulgation et persistance demeurent non démontrées.

**Suite proposée :** améliorer couverture des routes/répétitions, collecte
applicative et traçabilité des tests ; désigner responsables, organiser veille
et plan de remplacement de File Browser non maintenu. Le REX détaille causes,
priorités, validation et impacts. Ces améliorations ne sont pas déclarées
déployées ; le service n’est pas arrêté et la situation n’est pas clôturée.
