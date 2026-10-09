# Qualifier la situation et préparer la suite

**Itération 9 — 9 octobre 2026 — Travail individuel — État provisoire pour J10**

## 🎯 Objectif

Établir un état de situation provisoire à partir des sources disponibles et
justifier les prochaines investigations ainsi que les éventuelles mesures
immédiates. Évaluer l’effet des actions sur File Browser et sur les preuves
avant toute décision.

**Qualification provisoire :** scénario pédagogique fourni par le formateur,
comportements de reconnaissance et d’exploration documentés dans une
reproduction contrôlée ; **incident réel et compromission non établis**.
L’analyse et le traitement de la situation restent ouverts pour **J10**.
Aucune restriction, isolation ou interruption n’est réalisée par cette feuille.

## 1. Faits établis

Les références détaillées et les captures sont conservées dans
[Incident : premiers éléments](incident-premiers-elements.md).

| Fait démontré | Preuve disponible | Portée de la conclusion |
| --- | --- | --- |
| Le script prévoit deux scans et 22 GET, dont 13 vers `/admin` | Lecture de `j9-filebrowser-incident.sh` transmis par Olivier | Décrit le scénario prévu ; ne prouve pas chaque exécution passée |
| Le script a été invoqué sur la VM avec sa propre adresse cible | Journald/sudo reçus par Wazuh, agent 001 ; invocation à 14:01:59 CEST, fin de contexte sudo à 14:04:29 | Invocation démontrée ; résultat détaillé de l’essai initial non fourni |
| La VM atteint sa propre adresse par `lo`, l’hôte l’atteint par `virbr0` | Deux sorties `ip route get 192.168.122.229` | Routage confirmé au contrôle ; limite de capture expliquée, sans reconstitution des paquets initiaux |
| Une reproduction a été réalisée depuis l’hôte de 14:33:13 à 14:35:38 CEST | Sortie du script et capture 14:37:56 | Nouvelle exécution distincte de l’essai initial |
| Nmap retrouve 22/8080 ouverts sur le premier périmètre, puis 22 ouvert et 999 ports fermés sur 1–1000 | Sortie Nmap de reproduction | États sur les ports testés ; pas d’inventaire exhaustif ni de version applicative démontrée |
| Suricata produit 99 alertes SID 1009001 à 14:33:35 pendant la reproduction | Texte EVE compté, capture 14:37:48 | Volume SYN reconnu, `action:allowed` ; pas de blocage ni d’intention déduite |
| Les 22 GET sont retrouvés dans EVE, tous en 200 | Texte EVE : deux GET `/`, huit chemins, douze GET `/admin` | Requêtes et réponses observées ; existence de fichiers sensibles non établie |
| Aucun autre SID n’apparaît dans l’extrait de reproduction | 121 objets transmis : 99 alertes 1009001 et 22 HTTP | Pas d’alerte HTTP correspondante dans cet extrait, pas conclusion sur tous les journaux |
| Docker ne retourne aucune ligne et Wazuh aucun objet Docker pour les fenêtres recherchées | Capture 14:41:37 ; Docker code 0 | Limite de visibilité applicative ; ni absence d’activité ni panne Wazuh prouvée |
| Une navigation Firefox à 14:06 est visible séparément | Dix objets HTTP, login/liste/polices/réglages, source hôte, statut 200 | Navigation compatible avec usage normal ; personne, autorisation et lien au script non établis |

**Contexte attribué :** Olivier indique que le script a été donné par le
formateur et qu’il l’a exécuté dans son laboratoire. Cette déclaration
explique le cadre pédagogique ; elle ne remplace pas une preuve technique
ou une vérification des droits applicatifs.

## 2. Hypothèses

| Hypothèse | Appui actuel | Vérification restante / critère de décision |
| --- | --- | --- |
| L’essai initial reste hors du capteur du bridge à cause de son trajet local | Invocation VM vers sa propre adresse ; routage `lo` confirmé | Résultats initiaux non disponibles ; conserver cette limite, sans recréer rétroactivement des traces |
| Les GET réussis ne sont pas journalisés de façon exploitable par l’application | Docker et sélection Wazuh sans résultat, alors que les 22 GET EVE existent | Vérifier journalisation, rotation/rétention et configuration effective si nécessaire ; cause exacte non établie |
| La navigation Firefox de 14:06 est un usage normal parallèle | URI et référents cohérents, origine hôte et user-agent navigateur | Confirmation du contexte, compte/droits et éventuels logs ; ne pas l’attribuer au script sans lien |
| Les règles sont trop spécifiques pour alerter sur l’exploration `/admin` et les autres chemins | 1009003 vise `/ais-lab-inhabituel-`, 1008002 vise `/`, 1009002 vise d’autres ports | Lire les fichiers effectivement chargés ; définir un besoin de détection adapté et tester normal/inhabituel |
| Des conséquences applicatives ont eu lieu | Aucun élément fourni ne les établit | Logs ou référence avant/après nécessaires ; rester « conséquences inconnues » au-delà des réponses HTTP |

La répétition et l’exploration sont établies pour la reproduction. Leur
caractère malveillant n’est pas une hypothèse à retenir comme vraie par défaut :
le contexte pédagogique est connu et aucun dommage n’est démontré.

## 3. Informations manquantes

| Information nécessaire | Ce qu’elle permettrait de décider | État / limite |
| --- | --- | --- |
| Sortie détaillée de l’exécution initiale sur la VM | Phases réellement exécutées et résultats | Non fournie ; les invocations restent les seules preuves système directes de cet essai |
| Corps HTTP et correspondance avec les routes File Browser | Distinguer page de repli, ressource réelle et réponse sensible | Non conservés par le script (`-o /dev/null`) ; toute vérification future doit être distincte |
| Configuration de journalisation et rotation/rétention | Expliquer l’absence de traces applicatives | Cause non vérifiée ; absence de résultat documentée |
| Compte, droits et contexte de la navigation Firefox | Qualifier son autorisation | Non fournis par IP/user-agent/référent seuls |
| État avant/après des données, droits et service | Établir une conséquence | Pas de comparaison probante disponible |
| Objet original du SERVICE_STOP à 14:06:59 | Identifier le service et juger la pertinence de cette piste | Nom absent de la projection ; aucun lien à File Browser démontré |
| Événements originaux complets et périmètre de rétention | Consolider l’investigation et les recherches sans résultat | Textes projetés/captures disponibles ; exhaustivité non prouvée |

Une information introuvable doit rester un **résultat limité et justifié**,
pas être remplacée par une affirmation favorable ou défavorable.

## 4. Risques immédiats — conditionnels

Les risques suivants décrivent ce qui pourrait arriver **si une activité
semblable était réellement malveillante**. Ils ne sont pas des impacts
observés dans ce laboratoire.

| Risque conditionnel | Indices nécessaires pour le renforcer | État actuel |
| --- | --- | --- |
| Découverte de services ou de routes utiles à une exploitation ultérieure | Source inconnue, poursuite non autorisée, sondes applicables et contexte | Scans/exploration contrôlés observés ; exploitation non démontrée |
| Accès à une ressource sensible ou divulgation | Corps sensible, journal d’accès pertinent, compte/droits et résultat réel | HTTP 200 seul insuffisant ; aucune divulgation établie |
| Dégradation de disponibilité par répétition | Volume, latence/erreurs, saturation et lien temporel | Aucun effet mesuré ; faible volume pédagogique ne prouve pas un déni de service |
| Modification de données ou de droits | Action d’écriture, audit applicatif, différence avant/après | Aucune modification établie par les GET fournis |
| Perte de preuves utiles | Rotation, nettoyage, redémarrage/recréation ou nouvelle injection brouillant les heures | Risque pratique pour la suite ; conserver les pièces dès maintenant |
| Activité non vue par une source | Trajet hors capteur, contenu chiffré, logs absents, règle hors périmètre | Limites déjà documentées : loopback initial, règles spécifiques et absence de traces applicatives retrouvées |

## 5. Actions possibles et impact

| Action envisagée | Justification / déclencheur | Impact sur le service | Impact sur l’investigation | Décision provisoire |
| --- | --- | --- | --- | --- |
| Conserver les éléments disponibles | Préparer J10 et éviter pertes/ambiguïtés | Faible ; copie ciblée, consommation de stockage à maîtriser | Positif : provenance, horaires et états conservés | **Prioritaire** ; pièces déjà reçues référencées, export des originaux à préparer |
| Poursuivre une observation ciblée | Repérer poursuite et nouveaux éléments sans injecter du trafic | Faible si lecture seule ; éviter collecte illimitée | Positif si période, filtres et rétention explicités | **À poursuivre sans modifier le dispositif** selon les consignes de J10 |
| Rechercher d’autres événements | Tester une hypothèse précise, contexte avant/après | Faible pour lectures ciblées | Positif ; éviter confusion des copies et rapprochements arbitraires | **Prochaine investigation** priorisée ci-dessous |
| Adapter les règles HTTP | Couverture insuffisante des routes/répétitions réelles | Risque de bruit ; redémarrage/rechargement à encadrer | Peut modifier les résultats futurs ; conserver état précédent | **À préparer**, sans installation automatique ; tester séparément |
| Limiter temporairement certains accès | Source ou ressource réellement non autorisée, impact établi ou menace en cours | Peut bloquer utilisateurs légitimes/NAT partagé ; filtrage Docker à vérifier | Peut interrompre l’activité observable et déplacer les trajets | **Non justifié à ce stade** ; décision à réexaminer avec de nouveaux faits |
| Isoler un composant | Compromission ou propagation étayée nécessitant confinement | Coupure applicative ; possible perte de gestion/agent | Collecte distante interrompue ; preuves locales à préserver | **Non exécuté** ; prévoir accès console et conservation si devient nécessaire |
| Arrêter un service | Impact en cours impossible à contenir autrement ou ordre motivé | Indisponibilité directe | Perte d’état volatil, fin des activités observables ; arrêt à tracer | **Non exécuté** ; pas justifié par les seuls scans/GET de ce scénario |

Les restrictions, l’isolation et l’arrêt ne sont pas des validations de
l’exercice à appliquer toutes ensemble. En cas de nouveaux éléments graves,
réévaluer le besoin de confinement avec le formateur/responsable ; préserver
les preuves disponibles sans retarder une décision justifiée par un impact
réel en cours. Documenter périmètre, décideur, heure, effet et retour arrière.

## 6. Ce qui doit être fait maintenant et ce qui peut attendre

### Mesures immédiates retenues

**Conserver et organiser les preuves**, garder les fenêtres et la séparation
entre essai initial, navigation Firefox et reproduction. Cette feuille et
les captures sont intégrées au mémo. Les objets sources complets restent
à exporter si disponibles : ne pas prétendre les avoir déjà sauvegardés.

Éviter une nouvelle injection, un nettoyage des logs, une recréation du
conteneur ou une modification des règles pour embellir le résultat.
Ces opérations pourraient faire perdre du contexte ou mélanger les essais.
**Aucune mesure de coupure n’est justifiée par les pièces actuelles** :
le scénario pédagogique est connu, aucun dommage ni activité hostile en cours
n’est établi. Cette décision est provisoire, pas une garantie d’absence de risque.

### Prochaines investigations pour J10

1. Conserver les objets EVE et Wazuh originaux utiles s’ils sont encore disponibles, avec provenance, fuseaux, filtres et références ; contrôler la rétention sans effacer les sources.
2. Qualifier l’absence de logs Docker : examiner la configuration de journalisation et les rotations, puis vérifier la configuration effective de collecte sans présumer une panne.
3. Examiner les réponses/routes si la consigne J10 le demande ; distinguer ressource réelle et page de repli, sans ouvrir de données sensibles ni assimiler cette vérification future à la capture passée.
4. Confirmer contexte et droits de la navigation Firefox ; rechercher l’objet SERVICE_STOP seulement si cette piste est pertinente pour l’état du service.
5. Proposer une détection HTTP adaptée à la répétition et aux routes observées, avec seuil justifié, usage normal de comparaison et tests séparés. Évaluer le bruit des 99 alertes SYN sans supprimer globalement des événements.
6. Mettre à jour qualification, conséquences et décision de mesures à partir des nouveaux éléments fournis par le formateur.

## 7. Dossier à conserver pour J10

| Élément | État en fin de J9 |
| --- | --- |
| Méthode d’investigation et séparation fait/interprétation/hypothèse | [Feuille préparatoire](preparer-analyse-situation-inhabituelle.md) |
| Chronologie, hypothèses et limites de recherche | [Analyse des premiers éléments](incident-premiers-elements.md) |
| Capture et capacité des règles | [Vérification de détection](verifier-capacite-detection.md) |
| Vue multi-source et signal/bruit | [Vue exploitable](construire-vue-exploitable-evenements.md) |
| Script fourni et sorties texte reçues | Analysés et référencés dans les feuilles ; conservation indépendante des fichiers originaux à vérifier |
| Captures J9 | Présentes dans `docs/assets/img/securisation-avancee-infrastructures/it-9/` et liées aux résultats correspondants |
| Objets bruts complets, empreintes et inventaire d’export | À préparer si disponibles ; non déclarés comme réalisés |
| État de situation et décisions | Présente feuille, qualification provisoire et mesures conditionnelles |

Conserver les originaux utiles dans un espace local à accès adapté ; réserver
au mémo les extraits et captures nécessaires sans secrets. Le mémo ne garantit
pas à lui seul la rétention des journaux d’origine.

## 📦 État provisoire à transmettre

La reconnaissance et l’exploration du scénario sont observées dans la
reproduction depuis l’hôte ; le scan génère des alertes, les 22 GET sont
visibles sans alerte HTTP correspondante dans l’extrait. L’exécution initiale
sur la VM présente un angle mort de capture expliqué par le loopback.
Aucune trace applicative de la reproduction n’a été retrouvée dans les
périmètres Docker/Wazuh cherchés ; conséquences et contenus restent inconnus.

**Décision actuelle :** préserver les preuves et poursuivre les recherches
ciblées ; aucune restriction, isolation ou coupure réalisée. **La situation
reste ouverte pour J10.** Les pièces disponibles ne démontrent pas un incident
réel et ne permettent pas de certifier l’absence de toute conséquence.

- [Analyse et chronologie](incident-premiers-elements.md)
- [Retour à l’itération 9](index.md)
- [Retour au module](../README.md)
