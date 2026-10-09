# Incident : premiers éléments

**Itération 9 — 9 octobre 2026 — Travail individuel**

## 🎯 Objectif

Analyser une activité inhabituelle sans partir d’une conclusion prédéterminée.
Appliquer la [méthode d’investigation préparée](preparer-analyse-situation-inhabituelle.md)
et compléter progressivement la chronologie avec des preuves référencées.

## Bilan final de l’analyse avec les pièces disponibles

**Investigation documentée :** le scénario fourni par le formateur est
identifié, l’écart de placement initial est expliqué, et une reproduction
séparée depuis l’hôte est corrélée aux événements Suricata. Les recherches
applicatives sans résultat sont conservées comme limites, sans résultat inventé.
Les sections de suivi ci-dessous gardent l’ordre de réception des preuves ;
les tableaux de cadrage, fréquence, chronologie et hypothèses sont consolidés
au dernier état disponible.

| Question | Réponse étayée | Limite restante |
| --- | --- | --- |
| Que s’est-il passé ? | Script pédagogique : deux scans, exploration de huit chemins et répétition de `/admin` ; 22 GET retrouvés dans la reproduction | Résultats complets de l’exécution initiale sur la VM non conservés dans les pièces |
| Quand ? | Invocation VM à 14:01:59 UTC+02 ; contexte sudo terminé à 14:04:29. Reproduction hôte 14:33:13–14:35:38 ; premières alertes fournies à 14:33:35 | Horaires Wazuh de réception ; début réel de toute activité inconnue non établi |
| Origine ? | Script invoqué sur la VM initialement ; reproduction depuis hôte 192.168.122.1 vers VM 192.168.122.229 | IP seule ne fournit pas l’identité ; attribution à Olivier repose aussi sur sa déclaration et la sortie terminal |
| Ressource ? | VM, ports sondés, File Browser:8080 et URI listées dans EVE | Corps HTTP non fournis ; ressource demandée ≠ fichier existant ou lu |
| Autorisée ? | Contexte d’exercice, script fourni par le formateur, test réalisé par Olivier sur son laboratoire | Pas de décision formelle ni de journal des droits applicatifs transmis ; `allowed` IDS ne vaut pas autorisation métier |
| Événements liés ? | Invocation dans Wazuh ; code/sortie client et cadence EVE concordent pour la reproduction | Navigation Firefox 14:06 distincte ; Docker/Wazuh ne confirment pas les GET de reproduction |
| Conséquences ? | Réponses 200 et activité réseau ; service répondant pendant les essais | Aucune lecture sensible, modification, suppression, compromission ou indisponibilité établie ; absence de conséquence non prouvée |
| Incident ? | **Simulation pédagogique documentée**, pas incident réel confirmé | Comportement exploratoire observable ; intention et gravité ne sont pas déduites des signatures |

## 1. Signalement reçu et état initial

> Plusieurs accès à des pages ou ressources inattendues ont été observés
> sur le service File Browser.

**Fait disponible :** ce signalement est fourni dans l’énoncé du formateur.
Il ne contient ni événements techniques, ni adresses ni ressources exactes.
Olivier choisit ensuite **13:20 le 9 octobre 2026, heure de Paris (CEST,
UTC+02:00)** comme début de la fenêtre de recherche. Cette borne est une
convention de travail, pas l’heure de début prouvée des accès ni une période
confirmée par le formateur. L’activité elle-même reste à retrouver dans les sources.
Le titre de l’exercice ne constitue pas une qualification d’incident établie.

| Élément | État au début de l’analyse |
| --- | --- |
| Fenêtre de recherche | **Début choisi : 2026-10-09 13:20 CEST (11:20 UTC)** ; fin à préciser ; période du formateur à confirmer |
| Origine des accès | Non vérifiable |
| Ressources inattendues | À identifier dans les événements |
| Fréquence et début de l’activité | À mesurer sur la période disponible |
| Alertes associées | À rechercher, sans les présumer |
| Autorisation et conséquences | Non établies |
| Qualification | Situation inhabituelle signalée, investigation à commencer |

**Les essais contrôlés précédents ne sont pas les preuves de cette situation.**
Les chemins `/ais-lab-inhabituel-a/b/c`, scans et GET normaux documentés
précédemment doivent être identifiés comme tests connus s’ils apparaissent
dans la période. Ne pas attribuer automatiquement le signalement à ces essais.

## Premiers événements fournis — analyse de l’extrait EVE

Olivier indique avoir dû lancer un script sur la VM File Browser. **Cette
exécution est déclarée** : Olivier précise ensuite que le script a été
fourni par le formateur et exécuté **à 14:06** (heure locale du laboratoire
retenue pour le rapprochement, à confirmer si nécessaire). Nom, commande
et contenu ne sont pas fournis. Les événements reçus ne permettent pas encore de lui attribuer
une activité réseau. L’extrait transmis contient **34 objets : 24 avant
13:20 et 10 après**, avec des champs sélectionnés, pas les objets bruts complets.

### Écarter les anciens tests de la situation recherchée

Les **neuf alertes** de l’extrait sont toutes antérieures à 13:20 : SID
**1009003**, GET `/ais-lab-inhabituel-a/b/c`, à **12:07:35**, **12:34:11**
et **12:34:22**, source hôte `192.168.122.1` → VM:8080, curl/8.18.0,
réponse 200, `action:allowed`. Chaque alerte est accompagnée d’un objet
HTTP sur le même flux : cela représente **neuf transactions**, pas dix-huit
requêtes. Les six autres objets antérieurs sont des GET `/` à 12:11–12:12.
Ces éléments concordent avec les tests déjà documentés et ne sont pas
utilisés comme preuves de la situation débutant à la borne choisie de 13:20.

### Après 13:20 : dix événements HTTP à 14:06

Tous ont pour source **192.168.122.1**, destination
**192.168.122.229:8080**, user-agent **Firefox/157.0 sous Ubuntu**, statut
**200** et `alert:null` dans les objets HTTP. Aucun objet `alert` après
13:20 n’est présent dans l’extrait ; cela ne constitue pas une recherche
exhaustive des alertes ou des événements de la période.

| Heure CEST | Source | Événement / fait | Interprétation | Niveau de confiance | À vérifier |
| --- | --- | --- | --- | --- | --- |
| 14:06:18.671355 | EVE HTTP, flux `718187752754059` | POST `/api/login`, 200 ; référent `/login?logout-reason=inactivity` | Compatible avec une reprise de connexion après inactivité ; compte et authentification effective non établis par ces champs seuls | Élevée pour les champs, moyenne pour l’explication | Compte, logs applicatifs et confirmation de l’usage |
| 14:06:18.716673–.716876 | EVE HTTP | GET `/api/usage/` et `/api/resources/`, 200 ; référent `/files/` | Compatible avec chargement de la liste des fichiers | Élevée pour les requêtes, moyenne pour la navigation | Contenu et opérations applicatives réellement effectuées |
| 14:06:27.605602–.618849 | EVE HTTP | Quatre GET de polices woff2 (latin-ext, greek, cyrillic, vietnamese), 200 ; référent CSS | Chargement de ressources statiques compatible avec le navigateur ; répétition de ressources ≠ attaque | Élevée pour les requêtes | Comparaison aux usages si nécessaire |
| 14:06:30.611881–.653860 | EVE HTTP, flux `718187752754059` | GET `/api/shares` puis `/api/users`, 200 ; référent `/settings/shares` | Compatible avec consultation des réglages de partage ; ressources sensibles à contextualiser | Élevée pour les champs, moyenne pour le contexte | Identité, droits et autorisation de la consultation |
| 14:06:31.785297 | EVE HTTP, flux `718187752754059` | GET `/api/settings`, 200 ; référent `/settings/global` | Compatible avec consultation des réglages globaux ; aucune modification prouvée par ce GET | Élevée pour le fait, moyenne pour l’explication | Autorisation, logs et changements éventuels avant/après |

**Fréquence mesurable dans l’extrait :** dix transactions HTTP sur environ
13,114 secondes, dont quatre ressources statiques. C’est le volume de ce
petit extrait, pas un taux général ni la preuve d’une fréquence anormale.
Le premier événement fourni après 13:20 est à 14:06:18 ; le début réel de
l’activité et la couverture de 13:20–14:06 restent inconnus.

**Origine observée :** l’hôte du laboratoire, pas l’adresse VM
`192.168.122.229` comme source. Le user-agent et le référent sont déclarés
par le client : ils orientent vers une navigation Firefox sans identifier
la personne ou exclure une imitation. Ces objets ne prouvent pas l’activité
du script déclaré sur la VM, notamment un trafic local qui pourrait échapper
au point d’observation `virbr0`.

### Précision du participant : script du formateur à 14:06

Olivier confirme que le script a été **fourni par son formateur** et exécuté
**à 14:06**, sur la VM selon sa déclaration précédente. Cette information
donne un contexte d’exercice et un repère temporel. Elle n’établit pas encore
les opérations du script, son périmètre autorisé exact ou ses conséquences.

Les événements EVE à 14:06 coïncident avec cet horaire déclaré, mais leur
source reste **l’hôte 192.168.122.1**, avec Firefox comme user-agent. Il
faut donc départager une navigation simultanée, des actions indirectement
liées au script ou une autre explication en examinant son contenu et les
traces sur la VM. Aucun lien causal n’est déduit de la coïncidence seule.

| Heure | Source | Événement / fait | Interprétation | Niveau de confiance | À vérifier |
| --- | --- | --- | --- | --- | --- |
| 14:06, déclaré | Précision d’Olivier | Script fourni par le formateur et exécuté ; VM indiquée par la déclaration initiale | Contexte pédagogique ; lien avec les requêtes Firefox non établi | Déclaration attribuée, exécution technique non vérifiée | Nom, commande, contenu, cible et traces produites |

### Conclusion provisoire et pistes prioritaires

Les événements récents fournis sont **compatibles avec une navigation du
service et de ses réglages**. Aucun chemin inattendu nouveau, nouvelle alerte,
modification ou conséquence dommageable n’est établi par cet extrait.
Les accès aux réglages/utilisateurs nécessitent néanmoins de vérifier le
compte et l’autorisation. Un incident ne peut pas être conclu à ce stade.

1. Identifier le script fourni par le formateur, sa commande et la cible utilisée, sans publier ses secrets ; horaire déclaré : 14:06. Conserver la déclaration séparée des faits techniques.
2. Rechercher toute la fenêtre depuis 13:20, puis avant/après l’heure réelle du script ; conserver filtres, fichiers et limites de capture.
3. Retrouver les logs Docker et archives Wazuh autour de **12:06:18–12:06:32 UTC** pour rapprocher la navigation observée, sans présumer une trace de chaque succès.
4. Vérifier contexte utilisateur, droits et opérations prévues pour `/api/shares`, `/api/users` et `/api/settings` ; ne pas confondre réponse 200 et autorisation démontrée.

Cette chronologie technique complète la ligne de signalement ci-dessous.
Les anciennes alertes restent exclues avec leur justification temporelle.

## Complément Wazuh : exécution du script retrouvée

Le nouvel extrait contient **170 objets JSON complets lisibles**, précédés
d’une ligne tronquée et suivis du prompt. Sources : **52 auditd**, **58
journald**, **38 dpkg** et **22 sorties `df -P`**. Ces objets proviennent de
l’agent 001 ; aucune source Docker File Browser n’apparaît dans cet extrait.
Les objets sont projetés et certains ont `data:null` : leur message original
n’est pas accessible ici. Il ne s’agit pas d’un export exhaustif des sources.

### Chronologie complémentaire, heures de réception converties en CEST

| Heure CEST (UTC dans Wazuh) | Source | Fait observé | Interprétation / confiance | À vérifier |
| --- | --- | --- | --- | --- |
| 13:58:05–13:58:07 (11:58) | auditd/journald | Événements SSH associés à oliv et source 192.168.122.1, dont USER_START session 11 | Contexte de session SSH documenté ; ne fournit pas à lui seul toutes les commandes | Messages originaux et session utilisée pour le script |
| 13:59:15–13:59:53 (11:59) | journald, décodeur sudo | Commandes chmod -x puis +x sur le fichier du script | Préparation des permissions documentée ; effet exact non vérifié | Sorties des commandes si utiles |
| 13:59:59.955 (11:59:59.955) | journald/sudo | `/home/oliv/j9-filebrowser-incident.sh`, utilisateur oliv vers root | Invocation sans argument enregistrée, confiance élevée sur la commande | Résultat et contenu du script |
| 14:00:15.958 (12:00:15.958) | journald/sudo | `/home/oliv/j9-filebrowser-incident.sh 192.168.122.229` | Invocation avec la propre adresse VM comme cible | Résultat de ce premier essai et actions réellement exécutées |
| 14:01:27.965 et 14:01:41.968 (12:01) | journald/sudo | apt update puis apt install nmap | Préparation d’outil documentée ; ne prouve pas son utilisation par le script | Sorties et contenu du script |
| 14:01:55.859 (12:01:55.859) | dpkg | nmap 7.98+dfsg-1, statut installed | Installation enregistrée ; confiance élevée sur cet événement | Pas de scan déduit de l’installation seule |
| 14:01:59.967 (12:01:59.967) | journald/sudo | `/home/oliv/j9-filebrowser-incident.sh 192.168.122.229` | Nouvelle invocation enregistrée avant 14:06 | Sortie complète, contenu et opérations produites |
| 14:04:29.817 (12:04:29.817) | auditd | USER_END, sudo PID 159232, session 2, res success | Fin de session sudo associée au contexte de la dernière invocation ; ne prouve pas la réussite de chaque action du script | Code de sortie et messages du script |
| 14:06:59.831 (12:06:59.831) | auditd | SERVICE_STOP, systemd, res success ; service non identifié dans la projection | Arrêt de service enregistré, sans attribution à File Browser ou au script | Objet brut/full_log et nom du service |

Ces horaires sont ceux des événements reçus dans Wazuh ; conserver les
horodatages originaux pour dater plus précisément les actions si nécessaire.
**La dernière invocation retrouvée est à 14:01:59 CEST**, pas 14:06.
Le repère 14:06 donné par Olivier est donc une approximation déclarée,
complétée par ces traces. La navigation Firefox de 14:06 reste distincte,
sans lien causal établi avec le script.

**Hypothèse de visibilité à vérifier :** le script est invoqué sur la VM
avec sa propre adresse comme cible. Si ses requêtes utilisent cette cible,
leur trajet peut rester local et ne pas traverser `virbr0`. Cela expliquerait
l’absence de ces requêtes dans l’extrait Suricata sans prouver qu’aucune
activité n’a été générée. Contenu et sortie du script restent nécessaires.

### Lecture Docker fournie sans résultat

La commande collée `sudo docker logs --timestamps --since "$APP_DEBUT" \ filebrowser 2>&1`
est suivie d’un prompt sans ligne de log. La valeur de `APP_DEBUT` et le
code retour ne sont pas fournis. Si `\ filebrowser` a réellement été saisi
sur une seule ligne, le backslash échappe l’espace ; ce n’est pas une
continuation de ligne et l’argument peut être incorrect. Ne pas conclure
« aucun log applicatif » sur cette seule sortie.

Sur la VM, reprendre une lecture sans variable ni backslash, à partir du
début choisi et sans borne de fin supplémentaire :

```bash
sudo docker logs --timestamps --since '2026-10-09T13:20:00+02:00' filebrowser 2>&1
echo "Code Docker : $?"
```

Si la lecture réussit et reste vide, cela établit l’absence de lignes
retournées par Docker sur ce périmètre, pas l’absence de requêtes ou de
conséquences. Ne pas relancer le script pour obtenir des logs : conserver
son contenu et sa sortie avant tout nouveau scénario.

## Analyse du script fourni — lecture seule

Le fichier `j9-filebrowser-incident.sh`, fourni par le formateur et transmis
par Olivier, a été lu **sans exécution**. Son contenu décrit un scénario
pédagogique ; ses commentaires sont une indication de conception, pas une
preuve de résultat ni une instruction exécutée par le mémo.

### Activités prévues par le code

| Phase | Commandes / cibles prévues | Ce qui reste à prouver à l’exécution |
| --- | --- | --- |
| 1 — reconnaissance | Nmap `-Pn` sur 22,80,443,8000,8080,8443, puis 1–1000 | États retournés, mode de scan effectif et événements correspondants |
| 2 — accès normal | Deux GET `/`, espacés de cinq secondes | Réponses réelles ; aucun résultat HTTP fourni pour cette invocation |
| 3 — chemins inhabituels | GET `/admin`, `/backup`, `/private`, `/config`, `/config.json`, `/.env`, `/debug`, `/old`, espacés de trois secondes | URI et statuts réellement reçus ; existence ou contenu des ressources non établis |
| 4 — répétition | Douze GET `/admin`, espacés de deux secondes | Exécution complète, fréquence réelle et alertes éventuelles |

La cible vient du premier argument ; le port utilise `FILEBROWSER_PORT`
ou **8080 par défaut**. Le script prévoit **22 requêtes HTTP**, dont
**13 vers `/admin`**, et deux scans. Ce sont des quantités prévues par le
code, pas des activités toutes observées. Les pauses totalisent **143 s**,
auxquelles s’ajoute le temps des commandes ; la durée de contexte sudo
retrouvée, environ 150 s, est compatible sans prouver la réussite des phases.

Sans argument, le script affiche l’usage et quitte avec code 1 : cela
explique une issue possible de l’invocation sans argument de 13:59:59,
sans que sa sortie soit fournie. `set -u` est présent mais pas `set -e` ;
un échec Nmap n’interrompt donc pas automatiquement les phases suivantes.
Les curl n’ont pas de délai maximal et masquent leur progression ; la phase
4 ne rapporte pas les statuts. Le message final seul ne prouverait pas la
réussite de chaque requête.

### Écart de placement et visibilité du capteur

Le commentaire d’en-tête précise **Run from a machine different from the
target VM**. Les logs Wazuh montrent pourtant l’invocation sur la VM avec
**sa propre adresse `192.168.122.229` comme cible**, sous sudo.
Cela documente un écart par rapport au placement prévu par le script.

Les requêtes vers sa propre adresse sont normalement routées localement ;
ce trajet peut rester hors du bridge `virbr0` surveillé sur l’hôte.
**L’absence de ces chemins dans l’extrait Suricata n’est donc pas une preuve
de non-exécution ou de non-détection sur un trajet effectivement capturé.**
Les requêtes Firefox de 14:06, source hôte, ne correspondent pas aux curl
et aux URI de ce scénario ; elles restent une activité distincte.

Pour vérifier le trajet sans reproduire l’activité, sur la VM :

```bash
ip route get 192.168.122.229
```

Conserver le résultat avant de conclure définitivement au chemin local.
Le relevé actuel documentera le routage au contrôle, pas une capture des
paquets de l’exécution passée.

### Couverture des règles existantes

| Règle | Comparaison avec le script |
| --- | --- |
| 1009001 — volume SYN | Peut reconnaître le volume des scans si le capteur voit les paquets et si le seuil est atteint ; ne prouve pas Nmap à elle seule |
| 1009002 — RST des ports 65001–65003 | Ces ports ne font pas partie des scans du script : aucune couverture dédiée de ses ports fermés par cette règle ciblée |
| 1009003 — préfixe `/ais-lab-inhabituel-` | **Aucun des chemins du script ne correspond** au préfixe proposé ; ne pas attendre cette alerte pour `/admin` ou `/.env` |
| 1008002 — cinq GET exacts `/` en dix secondes | Seulement deux GET `/` espacés de cinq secondes sont prévus ; les répétitions concernent `/admin`, hors condition URI |
| 1008001 / signatures de motifs encodés | Aucun marqueur `%2e%2e` ou motif script/traversée correspondant n’est prévu dans les URI listées |
| 1008003 — réponse 401 | Peut déclencher si une réponse réelle 401 est visible ; aucun statut n’est garanti par le script |

Deux limites distinctes sont donc identifiées : **placement du trafic hors
point de capture possible** et **règles spécifiques ne couvrant pas tous les
chemins ou ports de ce scénario**. Une éventuelle adaptation doit partir des
événements réellement retrouvés, avec contrôle de configuration et tests
séparés ; aucune nouvelle règle n’est installée par cette analyse.

### Logs Docker et qualification de la situation

Olivier rapporte une lecture Docker sans ligne avec **code 0** depuis
13:20. La lecture a réussi sans retourner de journal sur ce périmètre ;
rotation, journalisation applicative et comportement du script restent à
considérer. Ne pas déduire de cette absence que les 22 GET n’ont pas été
émis, ni que les ressources ont été lues ou modifiées.

**Conclusion actualisée :** un script pédagogique de reconnaissance et
exploration HTTP a été invoqué sur la VM, avec la VM elle-même comme cible.
Les logs Wazuh prouvent l’invocation ; la lecture du code explique le scénario
prévu. Exécution complète, résultats HTTP, alertes du scénario et conséquences
ne sont pas établis par les pièces disponibles. Le contexte formateur explique
l’origine déclarée du test ; aucune attaque réelle n’est déduite de ces éléments.

**Prochaines pièces utiles sans relance :** sortie initiale du script,
résultat du routage local, et traces disponibles autour de
**14:01:59–14:04:30 CEST / 12:01:59–12:04:30 UTC**. Si une nouvelle exécution
sur l’hôte est retenue avec le formateur, l’identifier comme **reproduction
distincte**, avec sa propre fenêtre, et conserver les preuves initiales.

## Routage confirmé sur les deux machines

Les deux commandes fournies distinguent les trajets :

| Machine du contrôle | Résultat de `ip route get 192.168.122.229` | Conclusion |
| --- | --- | --- |
| Hôte `ubuntu-oliv` | `192.168.122.229 dev virbr0 src 192.168.122.1 uid 1000` | Les essais depuis l’hôte vers la VM passent par le bridge surveillé |
| VM File Browser | `local 192.168.122.229 dev lo src 192.168.122.229 uid 1000`, `cache <local>` | Les connexions de la VM vers sa propre adresse utilisent le loopback |

**Limite de visibilité confirmée au contrôle :** les connexions du script
lancé sur la VM vers sa propre adresse suivent un trajet local, hors de
`virbr0`. Le relevé confirme le routage actuel ; il ne constitue pas une
capture de paquets de l’exécution passée. Il explique pourquoi les activités
attendues peuvent manquer dans Suricata sur l’hôte, tandis que Wazuh reçoit
les traces système de l’invocation.

Une éventuelle reproduction depuis l’hôte utiliserait le trajet observable
prévu par le script. Elle devra être distinguée de l’exécution initiale :
nouvelle fenêtre, résultats client et objets EVE à conserver, sans transformer
ces nouvelles preuves en observations rétroactives de la première exécution.

## Reproduction depuis l’hôte — 14:33:13 à 14:35:38 CEST

Olivier transmet la sortie de `bash ./j9-filebrowser-incident.sh
192.168.122.229` depuis **l’hôte ubuntu-oliv**, dossier Downloads.
Début **2026-10-09T14:33:13+02:00**, fin **14:35:38+02:00**, soit
**145 secondes**. Cette reproduction utilise le trajet hôte → virbr0 → VM
confirmé précédemment. Elle reste distincte de l’invocation initiale sur la VM.

| Phase | Résultat client fourni | Conclusion permise / limite |
| --- | --- | --- |
| Scan des six ports | 22 et 8080 ouverts ; 80,443,8000,8443 fermés | États distants retournés par Nmap 7.98 ; aucun service/version précis établi par les noms de ports |
| Scan 1–1000 | 22 ouvert ; 999 fermés, motif conn-refused ; durée affichée 1,02 s | Recherche plus large réalisée ; 8080 est hors de ce second périmètre. Mode effectif non affiché par la commande ; sans sudo, connect TCP attendu sous droits ordinaires |
| Deux GET `/` | HTTP 200 pour les deux | Service répondant ; pas d’identité utilisateur ou d’authentification démontrée |
| Huit chemins inhabituels | `/admin`, `/backup`, `/private`, `/config`, `/config.json`, `/.env`, `/debug`, `/old` : tous HTTP 200 | Requêtes émises et statuts retournés ; ni fichier réel, ni contenu sensible lu, ni exploitation prouvés |
| Douze accès `/admin` | Phase 4 annoncée puis message de fin ; cette boucle du script n’affiche pas les statuts | Passage dans la phase cohérent avec le code ; nombre de succès et statuts à établir par EVE, pas par le message final seul |

### Chronologie de reproduction

| Heure | Source | Événement / fait | Interprétation | Niveau de confiance | À vérifier |
| --- | --- | --- | --- | --- | --- |
| 14:33:13 CEST | Terminal hôte et sortie du script | Début de la reproduction, cible VM:8080 | Test pédagogique exécuté depuis le point prévu | Élevée pour la sortie fournie | Événements réseau correspondants |
| Entre 14:33:13 et 14:35:38 | Sortie Nmap | Deux scans, résultats ci-dessus | Reconnaissance contrôlée | Élevée pour les résultats client | Heures détaillées, flux et alertes EVE |
| Même fenêtre, après scans | Sortie curl | Deux GET normaux et huit chemins, dix statuts 200 affichés | Activités HTTP contrôlées ; caractère inhabituel dépend du contexte | Élevée pour les statuts | URI/heures/flux, réponses effectives et traces applicatives |
| Même fenêtre, phase 4 | Sortie script et code | Annonce de répétition `/admin`, pas de statuts affichés | Douze GET prévus, résultats à rechercher | Moyenne pour l’exécution de toute la boucle | Transactions HTTP effectivement journalisées |
| 14:35:38 CEST | Terminal hôte et sortie du script | Message de fin et heure finale | Fin rapportée du scénario | Élevée pour le message | Code de sortie non fourni ; réussite détaillée non déduite |

### Recherche EVE de la reproduction, sans refaire le scénario

Depuis l’hôte, rechercher **14:33:13 inclus à 14:35:39 exclu**, en conservant
les deux sens et tous les ports :

```bash
sudo jq -c '
  select(.timestamp >= "2026-10-09T14:33:13"
     and .timestamp < "2026-10-09T14:35:39")
  | select(.src_ip == "192.168.122.229" or .dest_ip == "192.168.122.229")
  | select(.event_type == "http" or .event_type == "alert")
  | {timestamp,event_type,flow_id,src_ip,src_port,dest_ip,dest_port,http,alert}
' /var/log/suricata/eve.json
```

Relever les URI et compter les **objets HTTP** séparément des alertes :
attendus par le code, deux GET `/`, treize GET `/admin` et sept autres
chemins, soit 22 transactions si toute l’activité a été journalisée.
Comparer au résultat réellement retrouvé, sans forcer ce nombre.

Chercher également les flows du scan par leur `flow.start` : ils peuvent
être émis après la fin du script. Pour les alertes, examiner le SID et ses
conditions ; 1009003 cible un autre préfixe, 1009002 cible d’autres ports,
et 1008002 compte GET `/`, pas `/admin`. Une absence de ces alertes ne
signifie donc pas absence de l’activité HTTP.

Côté Docker/Wazuh, utiliser la fenêtre locale **14:33:13–14:35:39 +02:00**
ou **12:33:13–12:35:39 UTC** selon la source. Aucun événement de réception,
objet EVE ou alerte de cette reproduction n’est encore transmis.

**Conclusion de reproduction au dernier état :** activités client exécutées
sur un trajet visible du capteur ; détection/journalisation et alertes à
rapprocher des prochaines pièces. Le contexte pédagogique et l’origine
connue sont conservés, sans qualification d’attaque réelle.

## Reproduction : événements EVE retrouvés et analysés

La sortie transmise pour la fenêtre de reproduction contient **121 objets
JSON lisibles : 99 alertes et 22 événements HTTP**. Le comptage porte sur
cet extrait sélectionné, pas sur tous les paquets ou tous les types EVE.
Les objets HTTP correspondent exactement aux **22 GET prévus par le code**,
tous depuis **192.168.122.1** vers **192.168.122.229:8080**, statut **200**.

| Heure CEST | Source | Fait observé | Interprétation | Confiance / limite |
| --- | --- | --- | --- | --- |
| 14:33:35.132231–.137781 | EVE alert | **99 alertes SID 1009001**, révision 1, « AIS LAB volume SYN vers VM », sévérité 3, `action:allowed` | Volume SYN détecté pendant la phase de scan 1–1000, cohérent avec l’ordre et les pauses du script | Élevée pour les alertes ; nombre d’alertes ≠ nombre de ports fermés ou de scans |
| 14:34:05.148812 et 14:34:10.158378 | EVE HTTP | Deux GET `/`, 200, environ cinq secondes d’intervalle | Accès normaux de la phase 2 retrouvés | Élevée pour méthode/URI/statut |
| 14:34:30.167933–14:34:51.227912 | EVE HTTP | Huit GET, `/admin`, `/backup`, `/private`, `/config`, `/config.json`, `/.env`, `/debug`, `/old`, tous 200, environ trois secondes entre chaque | Exploration contrôlée de chemins, phase 3 retrouvée | Élevée pour les transactions ; existence/contenu des ressources non établis |
| 14:35:14.245318–14:35:36.343031 | EVE HTTP | Douze GET `/admin`, tous 200, environ deux secondes entre chaque | Répétition de la phase 4 effectivement retrouvée, y compris les statuts absents de la sortie script | Élevée pour les faits ; intention connue par le contexte pédagogique, pas déduite du réseau |

### Fréquence et ressources

- **GET `/` : 2** ; **GET `/admin` : 13** (un en exploration, douze en répétition).
- **Sept autres chemins : un GET chacun**. Pas de double comptage avec les alertes de scan.
- La boucle répétitive contient douze transactions sur **22,098 secondes** du premier au dernier événement, avec intervalles proches de deux secondes.
- Les GET d’exploration sont espacés d’environ trois secondes ; cette cadence concorde avec le script, sans constituer à elle seule une preuve d’attaque.

Les 99 alertes sont toutes **1009001** : aucun autre SID n’apparaît dans
l’extrait. Les objets HTTP ont `alert:null` et aucune alerte HTTP distincte
n’est présente dans cette sélection. C’est cohérent avec les limites des
règles : 1009003 cible `/ais-lab-inhabituel-`, 1008002 vise `/`, pas
`/admin`, et 1009002 vise 65001–65003, hors scans de ce script.
La reconnaissance réseau est donc alertée, tandis que l’exploration et
la répétition HTTP sont **visibles sans alerte correspondante dans l’extrait**.

### Ce qui peut être conclu

**La reproduction depuis l’hôte est observable par Suricata :** les scans
produisent des alertes de volume et les 22 GET sont journalisés. Le script,
les résultats client et l’ordre/rythme des événements concordent ; la phase 4
est désormais prouvée par EVE, pas seulement annoncée par le code.

Cette reproduction reste un **scénario pédagogique généré par Olivier**.
Elle ne transforme pas l’exécution initiale sur le loopback en activité
capturée rétroactivement et ne démontre aucune compromission. HTTP 200 ne
prouve pas la lecture de fichiers sensibles ; `allowed` confirme l’absence
de blocage par l’alerte IDS. Les 99 alertes pour une courte rafale soulignent
un bruit possible du seuil, à évaluer avant usage en exploitation.

**Manques conservés :** confirmation applicative/Docker/Wazuh de ces GET,
corps des réponses, identité/autorisation métier pour une situation inconnue,
conséquences et objets sources complets. Le texte fourni est une projection
EVE utile à l’analyse, pas un export exhaustif du journal.

**Piste de réglage à étudier, non réalisée :** choisir une règle ou une
corrélation couvrant les URI réellement observées et/ou la répétition de
`/admin`, puis tester un usage normal comparable. Justifier les routes et le
seuil ; ne pas décrire ces chemins comme malveillants par nature. Garder
visibilité, alerte et qualification d’incident comme trois conclusions distinctes.

## Recherches complémentaires Docker et Wazuh — aucun résultat rapporté

Olivier rapporte que les deux recherches proposées restent **sans résultat** :

| Source | Périmètre de recherche | Résultat rapporté | Portée / limite |
| --- | --- | --- | --- |
| Docker File Browser | Logs du conteneur, 14:33:13 inclus à 14:35:39 exclu CEST | Aucune ligne | Aucun message retourné pour cette fenêtre ; code 0 visible dans la capture de 14:41:37 |
| Archives Wazuh | Agent 001, 12:33:13 inclus à 12:36:00 exclu UTC, location sous `/var/lib/docker/containers/` | Aucun objet | Aucun message Docker retrouvé avec ce filtre ; pas une recherche de tous les événements système ou de tous les journaux tournés |

Ces résultats, initialement déclarés par Olivier, sont désormais illustrés
par la capture de **14:41:37** : lecture Docker vide avec **code 0** et
recherche Wazuh vide avec retour au prompt. Le code de la chaîne Wazuh
n’est pas affiché. Ils ne prouvent ni absence d’activité ni panne de transmission.
Les **22 GET EVE** restent les preuves réseau de la reproduction.

**Interprétation compatible, à distinguer du fait :** File Browser peut ne
pas émettre de message pour ces GET réussis. Sans message source, Wazuh ne
peut pas fournir une copie applicative correspondante. Les essais 401
précédents ont prouvé la chaîne de collecte pour ces messages, pas la
journalisation de tous les succès ni son fonctionnement actuel sur toutes
les sources. Rotation, rétention, filtre et état de collecte restent des
explications alternatives à vérifier si une trace source est attendue.

**Bilan de corrélation :** commandes/sortie client et Suricata concordent ;
aucune confirmation applicative Docker/Wazuh n’est retrouvée sur les
périmètres cherchés. Cela constitue une **limite de visibilité documentée**,
pas une contradiction des événements réseau ou une preuve d’absence de
conséquences. Ne pas modifier la collecte ou relancer le scénario pour
transformer cette absence en preuve positive.

## Captures de la reproduction et des recherches complémentaires

![Alertes Suricata de volume SYN à 14:33:35](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2014-37-48.png)

**14:37:48 :** l’image montre une partie des objets `alert` à 14:33:35,
SID 1009001, signature « AIS LAB volume SYN vers VM », source hôte,
destination VM et `action:allowed`. Le total **99** provient du comptage
du texte EVE fourni, pas du nombre de lignes visibles dans cette seule image.

![Sortie du scénario depuis l’hôte](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2014-37-56.png)

**14:37:56 :** début du script à 14:33:13, deux scans, deux GET `/` et
huit chemins HTTP 200 sont affichés ; la phase 4 est annoncée. L’heure de
fin 14:35:38 reste établie par la sortie texte transmise précédemment,
non visible dans le recadrage de cette image.

![Lectures Docker et archives Wazuh sans résultat](../../assets/img/securisation-avancee-infrastructures/it-9/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-09%2014-41-37.png)

**14:41:37 :** à gauche, la lecture Docker pour
14:33:13–14:35:39 CEST ne retourne aucune ligne et affiche **Code Docker : 0**.
Le résultat `local … dev lo` visible au-dessus est celui du contrôle du
routage sur la VM, distinct de la reproduction ensuite réalisée depuis l’hôte.
À droite, les archives du manager sont filtrées sur agent 001,
12:33:13–12:36:00 UTC et location Docker ; aucun objet n’est affiché et le
prompt revient. Aucune valeur de code retour Wazuh n’est montrée.

**Preuve de limite conservée :** source réseau exploitable, mais absence
de traces applicatives retournées pour cette reproduction dans les recherches
montrées. Les corps de réponse et conséquences restent inconnus. La chaîne
Wazuh validée auparavant pour les 401 ne démontre pas la journalisation des
GET réussis ici.

## 2. Cadrer avant de chercher

Renseigner la période précise, la cible et la provenance du signalement.
Si la période manque, consulter la disponibilité et la rétention des journaux,
mais ne pas choisir arbitrairement l’heure de nos captures précédentes.

| Paramètre | Valeur à renseigner |
| --- | --- |
| Début choisi, fuseau | 2026-10-09T13:20:00+02:00 — choix d’Olivier, période du formateur non confirmée |
| Fin du périmètre consolidé | Reproduction jusqu’à 14:35:38 CEST ; recherche EVE fin exclue 14:35:39, archives applicatives jusqu’à 14:36:00 CEST |
| Fenêtre étendue avant/après, justification | Reprise du contexte dès 13:58 pour SSH/préparation du script ; recherches Wazuh de reproduction prolongées jusqu’à 14:36 pour la réception |
| Cible et port confirmés | 192.168.122.229:8080 ; scans six ports puis 1–1000 ; routage hôte virbr0 et VM lo confirmés |
| Source du signalement / référence de la pièce | Énoncé du formateur ; script fourni et sorties EVE/Wazuh/terminal transmises par Olivier ; captures référencées dans cette feuille |
| Journaux disponibles et éventuelles rotations | EVE courant exploité ; Wazuh auditd/journald/dpkg ; Docker consulté sans résultat pour la reproduction. Rotation/rétention exhaustive non vérifiée |
| Tests connus dans cette fenêtre | Invocation initiale VM, navigation Firefox à 14:06, reproduction pédagogique hôte 14:33–14:35 ; contexte fourni par Olivier |

Dernier état documenté : Suricata sur l’hôte, `virbr0`, VM File Browser
`192.168.122.229:8080` ; agent Wazuh **001 — vm-filebrowser** sur la VM.
Confirmer ces éléments pour la période analysée. Conserver les pièces utiles
avant tout changement de règles ou redémarrage. Ne pas générer de nouveaux
accès inhabituels pendant la recherche : ils brouilleraient la chronologie.

## 3. Rechercher d’abord les événements HTTP et les alertes

### Sur l’hôte Suricata

Les horodatages EVE observés dans les preuves J9 sont en **UTC+02:00**.
Après obtention de la période, remplacer les deux valeurs ci-dessous par
des horodatages **dans le même format et fuseau que les événements EVE**.
Les bornes lexicales ne convertissent pas les fuseaux : ne pas mélanger UTC
et heure locale. La fin de fenêtre est exclue.

```bash
# Remplacer les deux valeurs avant exécution ; aucune période n’est présumée.
EVT_DEBUT='2026-10-09T13:20:00'
EVT_FIN='AAAA-MM-JJTHH:MM:SS'
sudo jq -c --arg debut "$EVT_DEBUT" --arg fin "$EVT_FIN" '
  select(.timestamp >= $debut and .timestamp < $fin)
  | select((.dest_ip == "192.168.122.229" and .dest_port == 8080)
      or (.src_ip == "192.168.122.229" and .src_port == 8080))
  | select(.event_type == "http" or .event_type == "alert")
  | {timestamp,event_type,flow_id,src_ip,src_port,dest_ip,dest_port,http,alert}
' /var/log/suricata/eve.json
```

Conserver les objets originaux correspondants dans un dossier de preuves
local à accès adapté ; cette projection retire des champs. Si la période
est dans un journal tourné, adapter la lecture au fichier concerné. Un
résultat vide sur le seul fichier courant ne suffit pas à écarter l’activité.

Relever méthode, URI, statut, origine/destination, ports, `flow_id`, user-agent,
référent et alertes éventuelles. Ne pas limiter immédiatement aux seuls chemins
connus de nos tests : les ressources du signalement ne sont pas encore identifiées.

### Début et fréquence

Pour chaque source ou groupe d’URI pertinent, établir : premier et dernier
événement, nombre de transactions HTTP, durée et répartition temporelle.
Compter les objets `event_type:http` séparément des alertes et `fileinfo`,
sans additionner leurs copies de contexte comme de nouvelles requêtes.

Le premier événement **retrouvé** n’est pas nécessairement le début réel :
élargir avant la fenêtre et vérifier la couverture/rétention. Un `flow_id`
peut porter plusieurs transactions. Une cadence inhabituelle exige une
comparaison avec les usages normaux, sans seuil inventé après coup.

| Groupe / origine | Premier retrouvé | Dernier retrouvé | Transactions HTTP | Durée / cadence | Comparaison et limite |
| --- | --- | --- | --- | --- | --- |
| Navigation Firefox depuis hôte | 14:06:18.671355 | 14:06:31.785297 | 10 | 13,114 s ; quatre polices | Compatible avec navigation ; autorisation du compte non établie |
| GET normaux de reproduction depuis hôte | 14:34:05.148812 | 14:34:10.158378 | 2 | Environ 5 s entre accès | Conforme à la phase 2 du script |
| Huit chemins explorés depuis hôte | 14:34:30.167933 | 14:34:51.227912 | 8 | Environ 3 s entre accès | Conforme à la phase 3 ; 200 ne prouve pas un fichier réel |
| Répétition /admin depuis hôte | 14:35:14.245318 | 14:35:36.343031 | 12 | 22,098 s, intervalles environ 2 s | Conforme à la phase 4 ; activité visible sans alerte HTTP dans l’extrait |

### Avant et après

Étendre autour des accès selon ce que montrent les premières pièces.
Rechercher navigation normale, refus, répétitions, changement de source,
réponses différentes, connexions administratives et événements système utiles.
Consulter les `flow.start/end` pour dater les flux, plutôt que le seul moment
d’émission du bilan. Les événements d’autres ports ou sorties réseau exigent
une vue complémentaire à la sélection HTTP/8080.

## 4. Confirmer avec les traces applicatives et Wazuh

### Sur la VM File Browser

Après renseignement des bornes avec leur fuseau réel :

```bash
APP_DEBUT='2026-10-09T13:20:00+02:00'
APP_FIN='AAAA-MM-JJTHH:MM:SS+02:00'
sudo docker logs --timestamps --since "$APP_DEBUT" --until "$APP_FIN" \
  filebrowser 2>&1
```

Rechercher les messages correspondant aux URI/statuts retrouvés dans EVE.
Tous les accès réussis ne sont pas nécessairement journalisés. Une absence
locale conserve cette limite ; elle n’annule pas une observation réseau.
Ne pas publier des sorties contenant jetons, contenus internes ou secrets.

### Sur la VM Wazuh

Les preuves précédentes du manager utilisent UTC. Convertir la période
fournie et renseigner les bornes UTC ci-dessous, puis chercher l’agent et
les sources disponibles avant de restreindre à un message précis :

```bash
WAZ_DEBUT='2026-10-09T11:20:00'
WAZ_FIN='AAAA-MM-JJTHH:MM:SS'
sudo docker exec single-node-wazuh.manager-1 \
  cat /var/ossec/logs/archives/archives.json | jq -c \
  --arg debut "$WAZ_DEBUT" --arg fin "$WAZ_FIN" '
  select(.timestamp >= $debut and .timestamp < $fin)
  | select(.agent.id == "001")
  | {timestamp,agent,location,decoder,data}'
```

Les valeurs à remplacer doivent être au format `AAAA-MM-JJTHH:MM:SS`,
en UTC comme les timestamps recherchés.
Vérifier rotation et archivage effectif. Les archives locales ne sont pas
nécessairement indexées dans le dashboard ; chercher aussi les alertes
réellement disponibles dans la bonne vue avec agent et période.

La réception des logs Docker dans Wazuh fournit provenance et heure de
réception ; ce sont deux étapes d’une même chaîne, pas deux preuves d’activité
indépendantes. Une catégorie MITRE ne démontre pas à elle seule une attaque.
Une connexion réseau vers le manager ne prouve pas la réception d’un message précis.

## 5. Expliquer les observations sans attribuer une intention

| Piste | Éléments à rechercher | Ce qui reste nécessaire pour conclure |
| --- | --- | --- |
| Utilisation normale | Navigation et ressources cohérentes, contexte utilisateur, droits et opération prévue | Confirmation de l’usage et journaux pertinents ; HTTP 200 seul insuffisant |
| Exploration | Série de chemins variés, répétitions, alternance de ressources, cadence et réponses | Comparaison aux usages, contexte de l’émetteur ; outil et intention non prouvés par la seule séquence |
| Activité potentiellement malveillante | Motifs de règle applicables, tentatives sur ressources sensibles, refus répétés ou conséquence anormale étayée | Conditions exactes, autorisation, résultat réel et conséquences ; alerte seule insuffisante |

Lire la règle déclenchée : SID, révision, condition, sens, seuil et périmètre.
Nos signatures 1009001–1009003 reconnaissent des comportements précis ; elles
ne couvrent pas automatiquement toutes les explorations ou tous les chemins.
`action:allowed` signifie absence de blocage IDS, pas autorisation métier.

Distinguer accès demandé, réponse obtenue et action applicative réussie.
Un 200 peut être une page de repli ; un 401 n’est pas automatiquement un essai
de mot de passe ; une IP n’identifie pas une personne. Vérifier comptes/droits,
exposition, filtrage et état de la ressource seulement lorsque cela répond à
une hypothèse précise. Ne pas confondre « conséquences inconnues » avec « aucune ».

## 6. Chronologie consolidée

Heures du **9 octobre 2026, CEST (UTC+02:00)**. Les lignes Wazuh utilisent
l’heure de réception convertie ; les détails originaux sont conservés dans
les tableaux précédents. Les anciens tests d’avant 13:20 restent exclus.

| Heure | Source | Événement / fait | Interprétation | Niveau de confiance | À vérifier / limite |
| --- | --- | --- | --- | --- | --- |
| Non fournie | Énoncé du formateur | Signalement d’accès inattendus | Point de départ, pas preuve d’incident | Signalement attribué | Période du signalement non confirmée indépendamment |
| 13:20 | Choix d’Olivier | Borne de recherche choisie | Organisation de l’analyse, pas début d’activité | Élevée sur le choix | Aucun événement présumé à cette heure |
| 13:58:05–13:58:07 | Wazuh auditd/journald | Session SSH, compte oliv, source hôte | Contexte administratif | Élevée sur les champs | Pas de lien complet établi entre toutes les sessions |
| 13:59:15–13:59:59 | Wazuh journald/sudo | chmod du script puis invocation sans argument | Préparation et essai ; code prévoit sortie usage sans argument | Élevée sur commandes, moyenne sur résultat | Sortie initiale non fournie |
| 14:00:15 | Wazuh sudo | Script avec argument adresse VM | Premier essai local enregistré | Élevée sur invocation | Résultat complet indisponible |
| 14:01:27–14:01:55 | Wazuh sudo/dpkg | apt update, installation Nmap, statut installed | Outil installé, pas preuve de scan à lui seul | Élevée | Opérations détaillées non déduites |
| 14:01:59–14:04:29 | Wazuh sudo/auditd et script | Nouvelle invocation avec adresse VM ; fin de contexte sudo | Exécution initiale cohérente avec durée du scénario | Élevée sur invocation ; moyenne sur déroulement | Pas de sortie détaillée ; routage local confirmé au contrôle ultérieur |
| 14:06:18–14:06:31 | Suricata HTTP | Dix requêtes Firefox, login/liste/polices/réglages, 200 | Navigation distincte, compatible avec usage normal | Élevée sur événements | Personne et autorisation applicative non établies |
| 14:06:59 | Wazuh auditd | SERVICE_STOP, service non identifié | Événement système, lien causal non établi | Élevée sur type | Nom du service manquant dans la projection |
| 14:33:13 | Terminal hôte | Début reproduction du script | Nouvelle exécution depuis trajet observable | Élevée | Distincte de l’exécution VM |
| 14:33:35.132231–.137781 | Suricata alert | 99 alertes 1009001, allowed | Volume SYN pendant scan | Élevée | Nombre d’alertes ≠ nombre de scans ; pas de blocage |
| 14:34:05 et 14:34:10 | Suricata HTTP et client | Deux GET /, 200 | Phase normale du script | Élevée | Pas de trace applicative correspondante retrouvée |
| 14:34:30–14:34:51 | Suricata HTTP et client | Huit chemins distincts, 200 | Exploration contrôlée | Élevée | Corps et existence de ressources non établis |
| 14:35:14–14:35:36 | Suricata HTTP | Douze GET /admin, 200 | Répétition contrôlée sans alerte HTTP dans l’extrait | Élevée | Règles ne couvrant pas cette répétition |
| 14:35:38 | Terminal hôte | Fin rapportée du scénario | Fin de reproduction | Élevée | Code global non fourni ; les 22 statuts sont vérifiés via EVE |
| Après reproduction, capture 14:41:37 | Docker et archives Wazuh | Lecture Docker vide code 0 ; sélection Wazuh vide | Limite de visibilité applicative documentée | Élevée sur captures | Ni absence d’activité ni panne de collecte démontrée |

## 7. Faits, hypothèses et informations indisponibles

### Faits établis

Le script et ses cibles sont connus. Wazuh retrouve ses invocations initiales
et l’installation de Nmap. Les relevés de routage distinguent loopback VM
et bridge depuis l’hôte. La reproduction est corrélée à 22 GET 200 et
99 alertes réseau, avec phases et cadence conformes au code. Les recherches
Docker/Wazuh sur la reproduction n’ont retourné aucune trace applicative
correspondante dans les périmètres montrés.

### Hypothèses examinées

| Hypothèse | Éléments utilisés | État au dernier bilan |
| --- | --- | --- |
| Les alertes anciennes de 12:07/12:34 expliquent l’activité après 13:20 | Horaires et chemins des tests déjà documentés | **Écartée pour cette fenêtre** : événements antérieurs, conservés hors chronologie de situation |
| La navigation Firefox à 14:06 est le trafic du script VM | Source hôte, user-agent Firefox, URI différentes ; script curl local | **Lien non établi** ; navigation traitée séparément |
| L’exécution initiale échappe au capteur du bridge par son placement | Invocation VM vers sa propre adresse ; route actuelle local dev lo | **Explication étayée** ; pas de capture rétroactive du trafic initial |
| La reproduction génère une exploration et une répétition HTTP | Code, sortie terminal et 22 objets HTTP concordants | **Confirmée pour la reproduction** ; contexte pédagogique, pas intention hostile déduite |
| Les GET réussis ne produisent pas de messages applicatifs exploitables | Docker vide code 0 et archives Docker Wazuh vides | **Compatible, cause exacte non établie** ; journalisation/rotation/rétention non vérifiées exhaustivement |
| Aucune alerte HTTP signifie aucune activité inhabituelle | Huit chemins et douze GET /admin visibles ; règles spécifiques à d’autres conditions | **Écartée** : visibilité sans alerte liée dans l’extrait |
| Incident réel, exploitation ou compromission | Aucun corps sensible, changement ou impact démontré ; test fourni par formateur | **Non démontré** ; ne pas présenter une simulation comme une attaque réelle |

### Informations non obtenues et conséquences pour l’analyse

| Information | État et raison connue | Conséquence / piste si nécessaire |
| --- | --- | --- |
| Sortie complète de l’exécution initiale VM | Non fournie ; invocation seulement retrouvée | Impossible de confirmer toutes ses phases ; conserver cette limite plutôt que relancer rétroactivement |
| Logs applicatifs de reproduction | Recherches montrées sans résultat | Suricata reste la source des GET ; pas de confirmation applicative inventée |
| Contenu des réponses HTTP | Script jette le corps, EVE fourni décrit les métadonnées | 200 ne prouve pas lecture de fichier sensible ; examen contrôlé de réponse serait une nouvelle vérification séparée |
| Identité/droits de la navigation Firefox | IP/user-agent/référent et compte non fourni dans ces objets | Autorisation de cette navigation non vérifiable avec ces seules pièces |
| Service arrêté à 14:06:59 | Nom absent de la projection auditd | Lien avec File Browser non établi ; objet original utile seulement si cette piste devient pertinente |
| Intégrité passée/conséquences sur les fichiers | Pas d’état avant/après ou événement de modification fourni | Aucun dommage prouvé ; absence de dommage non démontrée |
| Rotation/rétention exhaustives et objets originaux complets | Sélections et captures partielles | Conclusions limitées aux fichiers, fenêtres et champs disponibles |

Ces absences ne sont pas des travaux à déclarer réalisés ni une faute à
attribuer. **Elles constituent le résultat des recherches et la frontière
de ce que le dispositif permet d’établir.** Aucune collecte, règle nouvelle
ou preuve positive n’est ajoutée pour masquer un manque.

### Conclusion consolidée

La situation est expliquée dans le contexte d’un **scénario pédagogique
fourni par le formateur**. L’investigation a identifié l’origine des tests,
reconstruit les horaires, distingué une exécution sur loopback d’une
reproduction observable et rapproché code, résultats client et événements
Suricata. Le scan déclenche une alerte ; les accès inhabituels et répétés
sont journalisés sans alerte HTTP correspondante dans l’extrait.

**Aucun incident réel ni compromission n’est établi.** Les conséquences
applicatives restent inconnues au-delà des réponses 200, et les recherches
sans résultat dans Docker/Wazuh documentent une limite de visibilité.
Une évolution des règles HTTP et une étude de journalisation peuvent être
proposées pour améliorer le dispositif, mais ne sont pas des actions déjà
réalisées. Le livrable d’analyse est complété avec les pièces disponibles.

## 📦 Livrables à conserver

- Chronologie en cours et référence de chaque événement utilisé.
- Événements sources et critères de sélection, sans secret.
- Faits établis, interprétations et hypothèses séparés.
- Informations manquantes, limites de visibilité et prochaines recherches.
- Conclusion provisoire justifiée et révisable.

**Conclusion au signalement, conservée comme état initial :** une activité
inhabituelle est signalée. Il manque
la période confirmée et les événements pour la caractériser ou parler
d’incident. La recherche débutera à la borne choisie de 13:20 CEST ; aucune
activité à cette heure n’est présumée.
La prochaine étape est leur recherche dans les sources disponibles, sans
reproduire l’activité ni présumer son intention.

- [Méthode d’investigation](preparer-analyse-situation-inhabituelle.md)
- [Vue exploitable](construire-vue-exploitable-evenements.md)
- [Retour à l’itération 9](index.md)
- [Retour au module](../README.md)
