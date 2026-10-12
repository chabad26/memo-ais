# Qualifier la situation

**Itération 10 — 12 octobre 2026 — Travail individuel — 1 h**

## 🎯 Objectif

Établir ce que les éléments disponibles permettent réellement de conclure.
Qualifier origine, nature, cibles et résultats des activités, sans assimiler
la séquence **scan → accès au service → exploration HTTP** à une compromission.

**État de travail : qualification documentaire réalisée à partir des preuves
J9 et des compléments J10.** Aucun nouveau scan ou test n’est exécuté pour
rédiger cette feuille. La situation reste ouverte aux nouveaux éléments.

## 1. Périmètre et statuts

Distinguer trois séquences : invocation initiale du script sur la VM vers
elle-même, navigation Firefox à 14:06, reproduction du script depuis l’hôte
à 14:33–14:35 le **9 octobre 2026**. Les recherches J10 du 12 octobre
complètent les preuves de ces événements passés.

| Statut | Usage |
| --- | --- |
| **Établie** | Proposition directement appuyée par les pièces disponibles, dans le périmètre indiqué |
| **Probable** | Explication compatible et étayée, avec une vérification nécessaire encore manquante |
| **Non démontrée** | Preuve insuffisante ; ne signifie pas que la proposition est fausse ni que le risque est nul |

Chaque conclusion ci-dessous porte sur une proposition précise. Les horaires
sont en **CEST, UTC+02:00**, sauf indication contraire.

## 2. Origine, nature, ports et services

| Conclusion | Éléments qui la supportent | Statut |
| --- | --- | --- |
| Le scénario est pédagogique et le script est fourni par le formateur | Déclaration attribuée d’Olivier et script transmis intitulé J9 Injection incident File Browser | **Établie comme contexte déclaré** ; ne remplace pas une preuve d’autorisation métier formelle |
| Le script a été invoqué sur la VM avec sa propre adresse cible | Journald/sudo local : `/home/oliv/j9-filebrowser-incident.sh 192.168.122.229`, 14:01:59.367435, PID 159232 ; copie reçue par Wazuh | **Établie** pour l’invocation ; exécution complète de cet essai non démontrée |
| Le trajet VM vers sa propre adresse est local au contrôle | `ip route get` : `local 192.168.122.229 dev lo src 192.168.122.229` | **Établie** au relevé ; trajet historique non capturé |
| Le placement explique le manque de visibilité Suricata de l’essai initial | Cible locale et capteur sur virbr0 ; pas de capture réseau de l’essai initial fournie | **Probable**, cohérent avec le routage ; pas preuve de non-exécution |
| La reproduction provient de l’hôte 192.168.122.1 vers VM 192.168.122.229 | Terminal hôte, route via virbr0 et champs source/destination EVE ; fenêtre 14:33:13–14:35:38 | **Établie** ; identité d’Olivier également attribuée par sa déclaration, pas IP seule |
| La reproduction suit reconnaissance, accès normaux, exploration puis répétition | Script, sortie client et ordre/cadence des 22 objets HTTP et alertes | **Établie** pour ce scénario contrôlé |
| Le premier scan vise 22,80,443,8000,8080,8443 | Code et sortie Nmap : 22/8080 ouverts, quatre autres fermés | **Établie** sur les ports testés |
| Le second scan vise TCP 1–1000 | Code et sortie Nmap : 22 ouvert, 999 fermés ; 8080 hors périmètre | **Établie** sur ce périmètre ; pas inventaire de tous les ports |
| SSH et la publication File Browser sont les services attendus sur 22 et 8080 | Relevé ss J9 : sshd sur 22, docker-proxy sur 8080 ; docker publie 8080 → 80 ; HTTP File Browser observé | **Établie** dans les relevés disponibles ; aucun service/version précis déduit des seuls noms Nmap |
| Suricata alerte sur le volume SYN pendant le scan | 99 objets alert, SID 1009001, 14:33:35.132231–.137781, action allowed | **Établie** ; ni 99 scans ni blocage ni intention hostile prouvés |
| La navigation Firefox de 14:06 est l’activité du script | Source hôte, Firefox, URI login/liste/polices/réglages ; script invoqué localement sur VM, curl et autres URI | **Non démontrée** ; séquences conservées séparément |

## 3. Chemins HTTP et requêtes ayant obtenu une réponse

Les **22 GET** de la reproduction sont retrouvés dans EVE avec statut **200**,
source hôte, destination VM:8080. Le mot « réussi » est ici limité à la
**réponse HTTP obtenue** : il ne prouve ni une authentification ni l’accès à
un fichier correspondant au nom de l’URI.

| Chemin | Nombre observé | Moment / rythme | Résultat établi |
| --- | --- | --- | --- |
| `/` | 2 | 14:34:05.148812 puis 14:34:10.158378 | Deux réponses HTTP 200 |
| `/admin` | 13 | Une à 14:34:30.167933 ; douze entre 14:35:14.245318 et 14:35:36.343031, environ 2 s entre requêtes | Treize réponses HTTP 200 |
| `/backup` | 1 | 14:34:33.177589 | HTTP 200 |
| `/private` | 1 | 14:34:36.185648 | HTTP 200 |
| `/config` | 1 | 14:34:39.194424 | HTTP 200 |
| `/config.json` | 1 | 14:34:42.202018 | HTTP 200 |
| `/.env` | 1 | 14:34:45.211033 | HTTP 200 |
| `/debug` | 1 | 14:34:48.218398 | HTTP 200 |
| `/old` | 1 | 14:34:51.227912 | HTTP 200 |

| Conclusion | Éléments qui la supportent | Statut |
| --- | --- | --- |
| Les huit chemins inhabituels ont été demandés et ont répondu | Curl et objets HTTP EVE de la phase 3, tous 200 | **Établie** |
| La répétition de /admin a effectivement eu lieu | Douze objets HTTP distincts et cadence conforme au code | **Établie** |
| Une alerte HTTP correspondante figure dans l’extrait de reproduction | Extrait compté : 99 alertes 1009001 et 22 HTTP ; aucun autre SID | **Non démontrée** ; absence dans cet extrait établie, pas absence exhaustive dans tous les journaux |
| Les réponses 200 sont des pages de repli applicatives | Comportement compatible avec File Browser ; corps non conservés par le script | **Probable**, à vérifier ; ne pas en faire un fait établi |
| Les fichiers /backup, /config.json ou /.env existent et ont été lus | Noms des URI et 200 seulement, aucun corps ou journal de lecture fourni | **Non démontrée** |
| Les GET de reproduction sont confirmés par des messages Docker/Wazuh | Docker sans ligne, code 0 ; sélection d’archives Docker Wazuh sans objet sur les fenêtres documentées | **Non démontrée** ; les événements réseau restent valides |

## 4. Exploitation, autorisation, modification et persistance

| Conclusion | Éléments qui la supportent | Statut |
| --- | --- | --- |
| Une vulnérabilité a été exploitée | Aucun effet d’exploitation, corps sensible, exécution de code liée aux requêtes ou preuve applicative fourni | **Non démontrée** |
| Un accès non autorisé est établi | Pas de compte/droits ou décision métier démontrant une violation ; contexte de scénario fourni par le formateur | **Non démontrée** ; allowed IDS n’est pas une autorisation métier |
| Une modification des fichiers, comptes ou réglages File Browser est établie | GET et métadonnées HTTP ; pas d’écriture, audit applicatif ou comparaison avant/après | **Non démontrée** |
| Des opérations d’administration ont modifié l’environnement de la VM | Journald : chmod du script, apt update et apt install nmap ; dpkg statut installed pour Nmap | **Établie** pour opérations et installation ; sans les présenter comme conséquence hostile des GET |
| Un mécanisme de persistance malveillante a été installé | Aucune tâche/service/compte/clé ou mécanisme de relance suspect démontré | **Non démontrée** ; aucune recherche exhaustive de persistance réalisée |
| Le chmod +x du script prouve une persistance | Commande de changement de permission seulement | **Non démontrée** ; rendre un fichier exécutable ne prouve pas son lancement automatique |
| L’arrêt système à 14:06:58 est un arrêt File Browser | Journald et auditd événement 742 identifient PackageKit ; fin du daemon et deactivated successfully | **Non démontrée pour File Browser** ; **arrêt PackageKit établi**, sans lien causal au scénario prouvé |
| Une indisponibilité ou une exfiltration est établie | Aucun impact de disponibilité mesuré, contenu ou transfert sensible qualifié | **Non démontrée** |
| Aucune conséquence n’a eu lieu | Visibilité limitée, pas de comparaison d’état ni journaux applicatifs des GET | **Non démontrée** ; conséquences inconnues au-delà des réponses observées |

Une chaîne de comportements compatibles avec une reconnaissance peut
orienter l’analyse ; elle ne fournit pas seule la preuve d’une compromission.
Le scénario pédagogique explique ici les activités de reproduction. Ne pas
transférer cette explication à toute activité inconnue sans pièces correspondantes.

## 5. Informations encore manquantes et leur utilité

| Information | État des recherches | Ce qu’elle permettrait de qualifier |
| --- | --- | --- |
| Déroulement complet de l’exécution initiale VM | Invocations et sessions établies, sortie initiale non fournie ; auditd sans résultat sur la reproduction | Réussite/échec de chaque phase initiale, sans preuve rétroactive créée par la reproduction |
| Corps de réponse et routes réellement traitées | Script jette les corps ; métadonnées EVE seules | Page de repli versus contenu réel, existence de ressource et divulgation éventuelle |
| Identité/droits de la navigation Firefox | Champs réseau et référents, pas de compte/autorisation applicative prouvés | Usage autorisé ou non ; ne pas attribuer une personne par IP seule |
| Traces applicatives / journalisation | Recherches Docker/Wazuh documentées sans résultat pour reproduction | Cause du silence et capacité à enregistrer les accès réussis |
| État des données/droits avant et après | Pas de comparaison probante fournie | Modification, conséquence ou absence de différence constatée sur un périmètre précis |
| Détail des flows/ports refusés de reproduction | Résultats Nmap et alertes SYN disponibles ; compléments flows à rechercher | Réponses réseau, ports distincts et horaires précis ; ne pas compter les alertes comme ports |
| Recherche de persistance | Aucune investigation exhaustive réalisée | Mécanisme persistant éventuel ; absence non certifiée |

Les informations indisponibles sont des limites du dossier. Ne pas multiplier
les changements ou essais pour remplacer une pièce historique absente.
Conserver chaque recherche avec fichier, filtre, fenêtre, résultat et portée.

## 6. Qualification provisoire à retenir

**Établi :** reconnaissance de ports, accès au service, exploration de chemins
et répétition HTTP dans une reproduction pédagogique depuis l’hôte. Les
requêtes sont observées et les scans produisent des alertes réseau.
Les journaux locaux complètent le contexte administratif initial, et l’arrêt
anciennement indéterminé est identifié comme PackageKit.

**Probable :** le placement local explique l’angle mort de l’exécution
initiale ; les 200 sur chemins inhabituels peuvent correspondre à une page
applicative de repli, dont le contenu reste à vérifier.

**Non démontré :** exploitation, accès non autorisé, modification applicative,
persistance malveillante, exfiltration ou indisponibilité. Leur absence absolue
n’est pas certifiée non plus. **Aucune compromission n’est établie par la
succession scan → accès au service → exploration HTTP.**

Poursuivre les investigations seulement sur les informations utiles à une
hypothèse ou à la consigne du formateur ; conserver la situation ouverte pour
les nouveaux éléments et les décisions motivées, sans confinement automatique.

## 📦 Livrable

Tableaux de conclusions complétés avec preuves et statuts, distinction du
résultat HTTP et de la réussite applicative, informations manquantes et
qualification provisoire. Les références détaillées demeurent dans les
feuilles de chronologie, sans inventer de nouveaux événements.

- [Chronologie J10 et compléments journald/auditd](completer-chronologie.md)
- [Analyse et pièces J9](../it-9/incident-premiers-elements.md)
- [État provisoire et actions envisagées J9](../it-9/qualifier-situation-preparer-suite.md)
- [Retour à l’itération 10](index.md)
- [Retour au module](../README.md)
