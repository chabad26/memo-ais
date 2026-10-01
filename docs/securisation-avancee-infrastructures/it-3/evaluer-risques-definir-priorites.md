# Évaluer les risques et définir les priorités

**Durée indicative : 1 h 15**

## Objectif

Prioriser les constats de l’[audit consolidé](../it-2/consolider-resultats-greenbone-lynis.md)
en fonction du risque pour le serveur File Browser, et justifier les décisions
sans appliquer de correction. Les identifiants C01 à C11 sont conservés pour
éviter de créer une seconde liste indépendante.

**Statut au 1er octobre 2026 : classement documentaire établi à partir des
preuves disponibles.** L’exploitation de vulnérabilités n’est pas reproduite.
Les investigations gardent leur place dans l’ordre de travail sans être
présentées comme des défauts déjà prouvés.

## 1. Contexte qui détermine les risques

| Dimension | Éléments établis | Limite à respecter |
| --- | --- | --- |
| Exposition | SSH accessible depuis la machine d’audit ; écoute sur les interfaces de la VM. File Browser publie 8080 vers 80 en IPv4/IPv6 lorsqu’il tourne | Publication sur toutes les interfaces ne prouve pas un accès depuis Internet ; filtrage et chemin réseau restent à vérifier |
| Composants | VM Ubuntu 20.04.6, Docker/containerd, SSH, CUPS ; image File Browser 2.15.0 identifiée, environnement Alpine 3.13.4 | Contenu complet et vulnérabilités de l’image non analysés ; ancienneté seule ne prouve pas une CVE |
| Données | Bind mount /srv/filebrowser vers /srv en RW ; répertoires public, partenaires et interne | Sensibilité issue du cas fil rouge ; aucun fichier affiché dans l’inventaire limité, aucun vol de document prouvé |
| Identités | oliv dans sudo/adm ; gvm-audit sans sudo ; File Browser PID 1 UID/GID 0 dans le conteneur | Root dans le conteneur ne signifie pas automatiquement root sur la VM ; mappage et accès effectifs restent à examiner |
| Protections | Permissions SSH restrictives, CUPS local, sockets 660, conteneur non privilégié, filtre seccomp observé, journald/rsyslog actifs | Aucun bilan complet du pare-feu, du profil seccomp, de la rétention ou des droits applicatifs |
| Disponibilité | Démarrage File Browser sans erreur déclaré par l’utilisateur ; arrêts volontaires expliqués ; RestartPolicy no | Pas de panne spontanée retenue ; reprise automatique et test fonctionnel complet à définir |
| Maintenance | Non-rattachement Ubuntu Pro confirmé ; écarts de versions documentés au J1 | Fraîcheur APT et disponibilité actuelle des correctifs non vérifiées ; versions corrigées J1 conservées comme références historiques |

## 2. Méthode de décision

Pour chaque constat, relier une **condition d’accès** à une **conséquence** sur
les documents, l’administration ou la disponibilité. Relever les protections
qui réduisent ce scénario, puis préciser ce qui manque pour choisir la mesure.
L’impact du changement fait partie du risque : une correction qui coupe SSH
ou le réseau Docker doit être préparée avec accès de secours et tests.

| Priorité | Sens dans cette analyse | Nature de l’action |
| --- | --- | --- |
| **P1 — première séquence** | Risque important sur un service joignable ou décision bloquant plusieurs corrections | Préparer en premier ; ne signifie pas appliquer immédiatement une modification non validée |
| **P2 — haute** | Risque important mais conditionnel, ou investigation essentielle aux données et à la traçabilité | Traiter après les prérequis, avec vérifications ciblées |
| **P3 — planifiée** | Exposition limitée ou scénario restant très incertain | Planifier sans masquer les preuves manquantes |
| **Non pertinent comme incident** | Observation expliquée ne constituant pas une panne ou attaque démontrée | Écarter ce scénario ; garder les besoins d’exploitation distincts |

Un statut **À vérifier** et une priorité P2 sont compatibles : il s’agit alors
d’une priorité d’investigation, pas d’une autorisation de correction.

## 3. Classement justifié de tous les constats

Les scores sont ceux des VT relevés dans le [rapport J1](../it-1/premier-audit-greenbone.md),
pas des scores calculés pour ce serveur. Ils ne sont pas réévalués en direct.

| Rang / ID | Statut et priorité | Scénario et conditions | Conséquences / données concernées | Protections et limites | Traitement envisagé et impact possible | Justification du rang |
| --- | --- | --- | --- | --- | --- | --- |
| **1 — C07, voie de maintenance** | Non-rattachement Pro **confirmé** ; **P1 décision** | Des écarts de correction persistent tant qu’aucune voie de maintenance applicable n’est choisie ; disponibilité actuelle à vérifier | Plusieurs services de la même VM restent concernés ; administration, documents et disponibilité | Candidats APT identiques aux versions installées, mais cache non daté ; aucune exploitation établie | Choisir accès ESM applicable ou migration, vérifier versions corrigées, coûts et compatibilité ; migration pouvant modifier réseau, Docker et applications | Dépendance commune à C01/C02/C03/C06 ; se traite en premier sans compter comme une CVE supplémentaire |
| **2 — C03, correctifs SSH** | Écart de version **confirmé**, conditions CVE à vérifier ; **P1 préparation** | Service joignable depuis l’auditeur ; scénario dépendant de chaque CVE et option ; CVSS VT 8,1 | Atteinte possible au point d’administration et à l’hôte selon l’avis | GSSAPI désactivé réduit les scénarios exigeant cette fonction ; exposition Internet non prouvée | Préparer correctif ou migration et validation par clé ; conserver console et session de secours | Service d’administration réellement joignable, plus directement exposé que les moteurs locaux, malgré un CVSS inférieur à C01/C02 |
| **3 — C04, restrictions SSH** | Valeurs **confirmées**, usages à vérifier ; **P1 préparation** | Tentatives par mot de passe ; root par clé si clé autorisée ; rebond après compromission via transferts | Accès aux droits du compte, puis potentiellement à l’administration et aux données | gvm-audit sans sudo, droits des clés restrictifs ; aucune clé root ni faiblesse de mot de passe prouvée | Préparer le lot SSH décrit dans l’analyse consolidée ; vérifier tunnels, agent, X11 et secours ; risque de verrouillage administratif | Même point d’entrée que C03 ; actions distinctes à coordonner dans une maintenance, sans compter deux fois une compromission |
| **4 — C10, données et UID 0** | UID 0 et RW **confirmés**, accès non autorisé à vérifier ; **P2 investigation** | Compromission applicative ou accès local, puis opérations dans le périmètre permis par UID, montages et règles applicatives | Confidentialité/intégrité des espaces interne et partenaires, si des documents y sont présents | Conteneur non privilégié et seccomp ; aucun document exposé démontré, mappage UID inconnu | Tester séparation avec données fictives, mappage, ACL, compatibilité utilisateur moins privilégié ; changer UID/droits trop tôt peut empêcher l’accès légitime aux fichiers | Concerne directement la fonction métier ; investigation prioritaire malgré l’absence de CVSS, sans affirmer une fuite |
| **5 — C01, containerd** | Écart de version **confirmé**, fonctions concernées à vérifier ; **P2 correction à préparer** | Atteinte au moteur selon usages et accès requis par chaque CVE ; CVSS VT 9,9 pour l’avis | Hôte et disponibilité des conteneurs ; données indirectement concernées | Socket root:root 660 et écoute locale observée ; aucune exposition réseau externe démontrée | Inventorier fonctions, préparer correctif avec C07 et tests Docker ; maintenance pouvant interrompre File Browser | Impact potentiel fort mais conditions d’accès non établies ; score élevé ne suffit pas à dépasser SSH |
| **6 — C02, Docker/BuildKit** | Écart de version **confirmé**, usage BuildKit à vérifier ; **P2 investigation puis correction** | Contextes de construction et validations de chemins concernés selon l’avis ; CVSS VT 9,8 | Lecture/écriture hors du périmètre de construction si les conditions sont réunies | Aucun usage de BuildKit démontré ; socket root:docker 660, pas de membre déclaré, mais sudo et autres accès à examiner | Identifier builds et sources, préparer mise à jour ; redémarrage Docker pouvant interrompre le service | Risque conditionnel ; distinguer héberger un conteneur et exécuter une construction vulnérable |
| **7 — C08, audit ciblé** | auditd absent **confirmé** ; **P2 préparation** | Actions sensibles après accès au système insuffisamment documentées pour l’enquête | Détection et reconstitution d’un incident, plutôt qu’ouverture directe d’un accès | journald/rsyslog actifs ; événements de la veille conservés ; durée et couverture non établies | Dimensionner rétention, règles ciblées et intégration future ; risques de bruit, disque plein ou charge | Nécessaire au scénario d’investigation du module, mais ne remplace pas la réduction des accès |
| **8 — C05, MAC SSH** | Offre de deux MAC 64 bits **confirmée** ; **P2 planification** | Négociation d’un algorithme signalé faible ; aucune attaque reproduite ; CVSS v2 VT 2,6 | Risque cryptographique décrit par le VT ; conséquences concrètes non mesurées ici | Algorithmes plus robustes aussi proposés ; choix négocié non observé | Préparer liste excluant les deux MAC, vérifier clients et gvm-audit ; incompatibilités possibles | Action ciblée coordonnée avec C03/C04, sans urgence fondée sur une exploitation démontrée |
| **9 — C06, CUPS** | Paquet/service et permissions **confirmés**, dépendances à vérifier ; **P3 planifiée** | Scénario local ou conditions de l’avis J1 ; CVSS VT 6,7 ; fichier cupsd.conf lisible, pas modifiable par les autres selon modes | Atteinte au service ou au système selon conditions ; surface sans besoin métier identifié | Écoute localhost et autorisations applicatives ; aucune imprimante ; socket 666 ne prouve pas l’administration | Valider dépendances puis désactivation ; si conservé, correctif et mode attendu à étudier ; risque de casser une fonction d’impression/desktop | Écoute locale limite l’exposition ; inférieur aux services joignables et aux données métier |
| **10 — C09, sysctl** | Valeurs **confirmées**, défaut contextuel **À vérifier** ; **P3 investigation** | Informations noyau et fonctions réseau selon interfaces et usages ; aucun scénario exploité | Confidentialité locale et comportement réseau ; risque de coupure si mauvais durcissement | rp_filter 2 filtre en mode souple ; noyau partagé ; forwarding potentiellement nécessaire à Docker | Examiner interfaces, core_pattern, origine/persistance ; choisir ensuite des valeurs ciblées ; pas de désactivation globale du forwarding | Un écart de profil ne démontre pas un défaut exploitable ; dépendances réseau à établir avant toute mesure |
| **11 — C11, arrêts et reprise** | **Non pertinent comme panne spontanée** ; **P3 besoin d’exploitation** | Arrêts volontaires VM/conteneur expliqués ; risque seulement si une reprise automatique est attendue après démarrage | Disponibilité future selon le service attendu, pas incident observé | Démarrage sans erreur déclaré ; politique no connue ; test fonctionnel complet non fourni | Définir besoin de reprise et préparer test ultérieur ; une politique de relance peut remettre en écoute un service volontairement arrêté | Aucun indice justifiant une priorité d’incident ; maintenir la question d’exploitation sans la confondre avec une panne |

C09 et C11 reçoivent ici une priorité de travail explicite, en complément des
mentions « À investiguer » de la consolidation. C10 est actualisé avec les
preuves internes de 11:49. Les premières priorités restent des préparations,
pas des changements déjà autorisés dans cet exercice.

## 4. Vérifier la cohérence du classement

| Contrôle de cohérence | Conclusion |
| --- | --- |
| Pourquoi SSH avant containerd malgré 8,1 contre 9,9 ? | SSH est effectivement joignable et protège l’administration ; containerd n’est pas observé comme service externe, et les fonctions vulnérables utilisées restent inconnues |
| Pourquoi C10 sans CVSS reste haut ? | Le processus applicatif et le montage concernent directement les données du cas ; il faut établir les accès effectifs avant de déclarer un défaut de confidentialité |
| Pourquoi auditd sans urgence de mise à jour ? | L’absence touche la traçabilité, avec une journalisation générale existante ; bénéfice important pour l’enquête mais pas une preuve d’accès ouvert |
| Pourquoi CUPS reste P3 ? | Écoute locale et aucun rôle métier identifié ; permissions lisibles ne prouvent pas une écriture ou une administration libre |
| Pourquoi C09 n’est pas corrigé immédiatement ? | Paramètres partiellement dépendants des interfaces et des besoins Docker ; modifier sur le seul profil pourrait créer une indisponibilité |
| Pourquoi C11 n’est pas un incident P1 ? | L’utilisateur a expliqué les arrêts volontaires et les journaux corroborent celui de la VM ; code 1 seul ne démontre pas une panne |
| Double comptage ? | C07 est une dépendance de maintenance, pas une CVE ; C03/C04/C05 sont des actions distinctes sur SSH, pas trois compromissions ; C06 regroupe les sous-actions CUPS |
| Peut-on affirmer une exposition Internet ? | Non. Confirmer filtrage, routage et accès depuis un point externe avant d’augmenter la priorité pour cette raison |

## 5. Conditions qui feraient réviser les priorités

- **SSH/8080 réellement accessibles depuis Internet** : réexaminer en premier
  les contrôles d’accès et le lot applicatif ; conserver le point de test.
- **BuildKit avec contextes non fiables ou accès élargi au socket** : remonter
  C02 après confirmation des conditions de l’avis.
- **Accès croisé aux documents ou écriture excessive démontrés** : remonter
  C10 en P1 et préparer une mesure ciblée sans détruire les preuves.
- **CUPS exposé hors localhost ou fonction vulnérable atteignable** : réviser
  C06 ; une hypothèse ne suffit pas à changer son statut.
- **Analyse J3 identifiant une vulnérabilité applicable à l’image** : ajouter
  un constat distinct justifié ou enrichir un constat existant, sans déduire
  une CVE de la seule date 2021 ou de la distribution Alpine 3.13.4.
- **Besoin de service continu après redémarrage validé** : réévaluer C11 comme
  exigence de disponibilité, avec test de reprise et impact prévu.

## 6. Livrable et suite

Conserver ce classement avec date, preuves et hypothèses ; le relier au journal
des changements lors de la préparation des mesures. Pour chaque action future,
prévoir responsable, fenêtre, dépendances, retour arrière, test de sécurité et
test fonctionnel. Aucune échéance ni responsabilité réelle n’est inventée.

**État final : tous les constats C01 à C11 ont une priorité ou un classement
explicite, un scénario contextuel, une justification et une action suivante.**
Les investigations restent ouvertes et aucun correctif n’est appliqué.

- [Analyse consolidée et preuves](../it-2/consolider-resultats-greenbone-lynis.md)
- [Activité précédente — Étendre l’audit au conteneur (optionnel)](../it-2/etendre-audit-conteneur.md)
- [Retour à l’itération 3](index.md)
- [Journal des changements](../dossier-preuves.md#journal-des-changements)

- [Activité suivante — Finaliser le rapport et le plan de remédiation](finaliser-rapport-plan-remediation.md) :
  intégrer également C12 issu de Trivy et préparer les lots du J4.
