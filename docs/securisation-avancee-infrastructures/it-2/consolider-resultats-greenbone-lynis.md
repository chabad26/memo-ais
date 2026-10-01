# Consolider les résultats Greenbone et Lynis

## Objectif

Construire une seule analyse d’audit du serveur File Browser à partir des
résultats Greenbone du J1, de Lynis et des vérifications manuelles. Chaque
constat possède un identifiant unique, même lorsque plusieurs sources le
justifient. **Aucune modification de configuration n’est réalisée.**

Cette consolidation J2 est prolongée par la
[consolidation des trois sources avec Trivy](../it-3/consolider-trois-sources-audit.md).

**État au 1er octobre 2026 : consolidation documentaire réalisée à partir des
preuves disponibles.** Les conditions d’exploitation, les dépendances et les
contrôles encore manquants restent explicitement ouverts. Cette feuille ne
constitue ni un nouveau scan ni une preuve de remédiation.

## Périmètre et sources

La cible est la VM Ubuntu 20.04.6 LTS, noyau `5.15.0-139-generic`, qui héberge
Docker et File Browser. Le port SSH a été joint depuis la machine d’audit ;
une exposition publique sur Internet n’est pas démontrée. L’exposition publique
prévue par le cas pédagogique reste une hypothèse de contexte.

| Référence | Preuve utilisée | Limite |
| --- | --- | --- |
| **GB** | [Premier audit Greenbone](../it-1/premier-audit-greenbone.md) : scans A sans authentification et B authentifié, constats G01 à G05 | La réussite SSH de `gvm-audit` est prouvée ; ce compte n’a pas de droits administrateur. Les rapports Anonymous XML ne conservent pas toutes les valeurs locales |
| **LY** | [Analyse Lynis, exercice 2.3](analyser-prioriser-resultats-lynis.md) : audit local du 1er octobre, 4 avertissements, 52 suggestions, 221 tests, indice 57 | Les métadonnées et empreintes du second rapport restent à relever ; Lynis 2.6.2 présente une limite de collecte Docker |
| **VM** | [Vérifications manuelles](verifier-configuration-systeme.md) : sorties transmises le 1er octobre | Observations ponctuelles, sans changement ni test après redémarrage |
| **J1-local** | [Reprise des constats J1](reprendre-constats-j1.md) : versions, écoutes et services | Certains contrôles y étaient encore ouverts ; les résultats plus récents de VM prévalent |

File Browser, précédemment observé actif, est désormais `Exited (1)`.
L’analyse utilise cet état récent sans effacer l’observation antérieure.

## Règles de consolidation

**Confirmé** signifie que le défaut ou l’état décrit est étayé ; il ne signifie
pas que chaque scénario d’attaque a été reproduit. **À vérifier** conserve un
besoin de preuve. **Non pertinent** écarte un scénario ou une recommandation
pour le périmètre observé, avec justification, sans déclarer le serveur sûr.

Les priorités reprennent l’échelle de l’exercice 2.3 : P1 immédiate, P2 haute,
P3 planifiée, P4 faible. Elles dépendent de l’exposition et des conséquences,
pas du seul score d’un outil. Une priorité « À investiguer » indique qu’une
preuve manque pour décider. Les sous-actions conservent le même identifiant de
constat : elles ne créent pas des doublons.

## Tableau d’audit consolidé

Les références GB, LY et VM renvoient aux preuves ci-dessus. Les versions
corrigées citées dans les analyses J1 servent de comparaison historique ; elles
ne constituent pas une vérification en direct des dépôts ni des derniers avis.

| ID et constat | Source(s) | Éléments observés | Vérification effectuée | Statut | Risque dans le contexte du serveur | Priorité | Action envisagée | Justification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **C01 — Correctifs containerd manquants** | GB G01, USN-8472-1 ; VM | `1.7.24-0ubuntu1~20.04.2`, antérieur au `+esm2` cité au J1 ; service actif ; socket `root:root 660`, écoute réseau locale | Scan B authentifié ; `dpkg-query`, `apt-cache policy`, services, écoutes et `stat` | **Confirmé** pour l’écart de version ; fonctions vulnérables utilisées **à vérifier** | Atteinte au moteur de conteneurs, à l’hôte ou à la disponibilité selon les fonctions et accès requis ; aucune exploitation prouvée | **P2** | Préparer l’accès aux correctifs ou une migration de version supportée ; inventorier les usages de containerd avant maintenance | Composant réellement utilisé par Docker ; socket restreint et absence d’exposition externe observée nuancent l’urgence |
| **C02 — Correctifs Docker/BuildKit manquants** | GB G02, USN-8230-1 ; VM | Docker `26.1.3-0ubuntu1~20.04.1`, antérieur au `+esm2` cité au J1 ; socket `root:docker 660`, groupe Docker sans membre déclaré | Scan B ; versions et candidats APT ; `stat`, `getent group docker` | **Confirmé** pour l’écart de version ; usage de BuildKit **à vérifier** | Lecture/écriture hors du périmètre de construction selon l’avis étudié au J1, si les conditions BuildKit sont réunies | **P2**, à réévaluer selon les constructions | Préparer le correctif ; identifier les builds, leurs utilisateurs et la provenance des contextes | L’absence de membre déclaré dans Docker ne supprime pas l’accès via root, sudo ou d’autres permissions |
| **C03 — Correctifs OpenSSH manquants** | GB G03, USN-8804-1 ; VM | `1:8.2p1-4ubuntu0.13`, antérieur au `+esm3` cité au J1 ; TCP 22 joignable ; `GSSAPIAuthentication no` | Scan B ; versions ; écoute et accès J1 ; `sshd -T` | **Confirmé** pour l’écart de version ; exploitabilité CVE par CVE **à vérifier** | Compromission ou indisponibilité du service d’administration selon la CVE et les options nécessaires | **P1** pour préparer le traitement | Préparer mise à jour ou migration et tests d’accès ; examiner les conditions de chaque CVE | Service joignable et essentiel ; GSSAPI désactivé nuance les scénarios qui exigent cette fonction, sans corriger le paquet |
| **C04 — Configuration SSH permissive** | LY `SSH-7408` ; VM | Root par clé possible, mots de passe acceptés, 6 essais, transferts TCP/agent et X11 autorisés, niveau INFO | `sshd -t`, `sshd -T`, recherche des directives ; compte d’audit sans sudo, `.ssh` 700 et clés 600 | **Confirmé** pour les valeurs ; besoins des administrateurs **à vérifier** | Tentatives d’accès et fonctions de rebond après compromission d’un compte ; root autorisé par clé si une clé existe | **P1** de préparation, sans preuve d’exposition Internet | Proposition détaillée SSH ci-dessous ; préserver l’accès de secours | Complète C03 mais relève d’un défaut de configuration : une mise à jour ne remplace pas les restrictions d’accès |
| **C05 — MAC SSH de 64 bits proposés** | GB G05, scans A et B ; VM | `umac-64-etm@openssh.com`, `umac-64@openssh.com` dans la liste effective | Détection distante GB ; `sshd -T` précise les noms | **Confirmé** pour l’offre ; négociation réelle par un client non mesurée | Possibilité de négocier un MAC classé faible par le VT ; aucune attaque cryptographique démontrée | **P2** | Préparer une liste de MAC excluant les deux algorithmes signalés, après inventaire des clients et test par clé | Défaut cryptographique distinct de C03 et C04 ; LY `SSH-7408` ne prouve pas directement ce constat |
| **C06 — CUPS vulnérable et sans rôle métier identifié** | GB G04, USN-7897-1 ; LY `PRNT-2307`, `PRNT-2308` ; VM | CUPS/cups-daemon `2.3.1-9ubuntu1.9`, antérieurs au `+esm3` cité au J1 ; service/socket actifs ; localhost:631 ; aucune imprimante ; cupsd.conf 644, socket 666 | Versions, services, écoutes, `lpstat`, lecture ciblée ; journal LY à 10:02:37 : permissions 1/2 point, réseau 2/2 points ; `stat`, `namei` | **Confirmé** ; dépendances **à vérifier** | Surface d’attaque locale et risque de l’avis J1 ; fichiers lisibles localement, mais aucune écriture non autorisée ou fuite de secret prouvée | **P3** ; à réévaluer si exposition changée | Étudier la désactivation détaillée ci-dessous ; si CUPS doit rester, préparer correctif et examen du mode attendu par Lynis | Un seul constat de service avec trois sous-actions : besoin métier, correctif et permissions. Écoute locale atténuante ; le mode 666 du socket n’accorde pas à lui seul l’administration |
| **C07 — Couverture des correctifs ESM non active dans l’état relevé** | VM ; contexte des avis GB G01–G04 | VM non rattachée à Pro ; ESM `AVAILABLE yes` sans activation démontrée ; candidats APT identiques aux versions installées | `pro status`, `apt-cache policy`, `dpkg-query` | **Confirmé** pour le non-rattachement ; fraîcheur APT **à vérifier** | Maintien d’écarts de correction affectant plusieurs composants ; candidat identique ne signifie pas absence de correctif | **P1** de décision de maintenance | Choisir une voie de maintenance : accès ESM applicable ou migration supportée, avec dépendances et budget | Cause de gestion commune aux écarts C01, C02, C03 et C06 ; ne compte pas comme une vulnérabilité supplémentaire |
| **C08 — Audit système spécialisé absent** | LY `ACCT-9628` ; VM | Unité et paquets auditd/audispd-plugins absents ; journald et rsyslog actifs ; 48 Mo de journaux sur disque | `systemctl`, `dpkg-query`, `journalctl --disk-usage`, recherche de rétention | **Confirmé** pour l’absence ; règles et rétention **à vérifier** | Traçabilité moins détaillée pour enquêter sur les actions sensibles ; aucune absence totale de journaux | **P2** | Proposition auditd ci-dessous ; dimensionner rétention et collecte Wazuh | Absence confirmée manuellement ; journalisation existante atténuante mais ne prouve pas une couverture d’audit ciblée |
| **C09 — Paramètres noyau à adapter au rôle du serveur** | LY `KRNL-6000` ; VM | 15 valeurs relevées : forwarding IPv4 1, dmesg_restrict 0, suid_dumpable 2, rp_filter 2, redirects activés à certains niveaux ; kptr_restrict 1 et sysrq 176 | `sysctl`, recherche `/etc/sysctl*` ; directives concordantes pour rp_filter, kptr_restrict et sysrq | **À vérifier** pour le défaut contextuel ; valeurs **confirmées** | Informations noyau ou comportement réseau moins strict selon interfaces et usages ; casser Docker serait aussi un risque | **À investiguer** | Examiner `core_pattern`, valeurs des interfaces, origines et persistance ; définir ensuite un lot ciblé | Différence au profil ne suffit pas à prouver un défaut ; rp_filter 2 filtre en mode souple, sysrq 176 est un masque |
| **C10 — Droits des données et exécution root de File Browser** | VM | Répertoires `root:root 755`, aucun fichier affiché à profondeur 3 ; ACL de base sur quatre chemins ; montage RW ; non privilégié ; contrôle interne à 11:49 : PID 1 et shell UID/GID 0 | `stat`, `namei`, `find`, `getfacl`, `docker inspect` | **Confirmé** pour l’exécution root ; accès aux documents **à vérifier** | Les utilisateurs locaux peuvent lister/traverser les répertoires ; noms interne/partenaires ne garantissent pas la confidentialité | **P2** de vérification | Relever ACL restantes et mappage des UID ; étudier une exécution moins privilégiée et tester les droits avec données fictives | UID 0 confirmé dans le conteneur ; mappage vers l’hôte et accès effectifs non testés ; aucune fuite ni sortie du conteneur prouvée |
| **C11 — Reprise de File Browser après arrêt volontaire de la VM** | VM et déclaration de l’utilisateur ; contrôle LY `CONT-8106` | Arrêt VM déclaré le 30 septembre à 14:42:59 +02:00 ; Docker/containerd arrêtés proprement ; File Browser code 1, OOMKilled false, RestartPolicy no | État détaillé, logs applicatifs et journal systemd Docker/containerd concordants | **Non pertinent** comme panne spontanée ; besoin de reprise automatique **à vérifier** | Aucun incident de sécurité démontré ; absence de reprise pouvant affecter la disponibilité si le service est attendu après démarrage | **À investiguer** selon le besoin de disponibilité | Définir le comportement attendu après démarrage de la VM et préparer un test de reprise ultérieur | Arrêt volontaire attribué à l’utilisateur et corroboré par les journaux ; aucune modification de politique à ce stade |

Les scénarios « CUPS directement exposé sur le réseau » et « absence totale de
journalisation » sont **Non pertinents pour l’état observé** : écoute locale
pour le premier, journald/rsyslog actifs pour le second. Leurs constats parents
C06 et C08 restent retenus. Aucun test de sécurité n’est effacé pour améliorer
artificiellement le bilan.

## Trois recommandations de l’exercice 2.3 reprises dans l’analyse

Les décisions ci-dessous sont documentaires et conditionnelles : **À appliquer**
ne vaut pas exécution pendant cet exercice. Les commandes de changement ne
sont pas à lancer maintenant.

### C04 — SSH, `SSH-7408`

| Élément | Analyse |
| --- | --- |
| Configuration actuelle | `PermitRootLogin without-password`, `MaxAuthTries 6`, `AllowTcpForwarding yes`, `X11Forwarding yes`, `AllowAgentForwarding yes`, `LogLevel INFO`. Les trois derniers paramètres sont maintenant confirmés manuellement. `PasswordAuthentication yes` reste traité séparément |
| Modification exacte envisagée | Préparer `/etc/ssh/sshd_config.d/99-hardening.conf` avec les six directives ci-dessous. Vérifier ensuite les valeurs obtenues : l’ordre des fichiers et un éventuel bloc Match peuvent affecter le résultat |
| Effet attendu | Refuser root en connexion directe, réduire les essais par connexion, supprimer les transferts inutiles et enrichir les traces |
| Conséquences possibles | Perte des tunnels, de X11 et du transfert d’agent ; perte de l’accès direct root ; risque de coupure d’administration si les dépendances sont ignorées |
| Décision | **À appliquer**, après validation des usages et d’un accès de secours ; désactivation du mot de passe **À investiguer** |
| Justification | Configuration confirmée d’un service joignable. `MaxAuthTries 3` ne constitue pas une limitation globale des tentatives et le durcissement ne remplace pas C03 |
| Validation future | Syntaxe `sshd -t`, valeurs `sshd -T` avec contexte si Match, nouvelle connexion administrateur et scan par clé gvm-audit ; contrôler le refus des transferts avant fermeture de la session de secours |
| Retour arrière prévu | Conserver l’état initial et l’accès console ; retirer uniquement le fragment ajouté, contrôler la syntaxe puis recharger SSH |

Contenu proposé, **non déployé** :

```text
PermitRootLogin no
MaxAuthTries 3
AllowTcpForwarding no
X11Forwarding no
AllowAgentForwarding no
LogLevel VERBOSE
```

### C08 — auditd, `ACCT-9628`

| Élément | Analyse |
| --- | --- |
| Configuration actuelle | auditd et audispd-plugins absents ; journald/rsyslog actifs, rsyslog activé ; rétention effective non établie |
| Modification exacte envisagée | Installation future d’`auditd` et `audispd-plugins`, puis fichier `/etc/audit/rules.d/ais.rules` avec les deux règles ciblées proposées ci-dessous ; préparer également rotation et capacité disque avant chargement |
| Effet attendu | Tracer les modifications des fichiers d’identité et de politique SSH pour reconstruire une chronologie |
| Conséquences possibles | Charge CPU/disque et événements supplémentaires ; bruit ou doublons lors de l’intégration Wazuh ; ces deux règles ne couvrent pas toutes les actions d’administration |
| Décision | **À investiguer** : dimensionner la rétention, valider les chemins et la disponibilité des paquets avant de retenir le lot |
| Justification | L’absence est confirmée ; le besoin de traces ciblées est établi par l’exercice, mais aucun volume ni intégration Wazuh ne sont encore validés |
| Validation future | `augenrules --check`, puis contrôle du service et des règles chargées ; modification contrôlée d’un fichier de test dans le périmètre retenu et recherche avec `ausearch`, sans changement réel de compte |
| Retour arrière prévu | Sauvegarder les règles existantes si présentes ; retirer les seules règles ajoutées et recharger un état connu. Ne pas purger globalement les règles ni supprimer les traces collectées |

Exemple de règles proposé, **non chargé**, à valider sur cette VM :

```text
-w /etc/passwd -p wa -k ais_identity
-w /etc/ssh/ -p wa -k ais_ssh_config
```

### C06 — CUPS, `PRNT-2307`

| Élément | Analyse |
| --- | --- |
| Configuration actuelle | CUPS actif et déclenchable, aucune imprimante ; écoute locale ; cupsd.conf et cups-files.conf 644, répertoire 755, socket 666 ; PRNT-2307 attribue 1/2 point à cupsd.conf |
| Modification exacte envisagée | Après validation des dépendances, désactiver et arrêter `cups.service`, `cups.socket`, `cups.path` ; étudier leur masquage seulement si nécessaire pour empêcher une réactivation. Ne pas appliquer de chmod au socket |
| Effet attendu | Retirer l’écoute et la fonction d’impression inutiles du serveur ; réduire sa surface d’attaque locale |
| Conséquences possibles | Arrêt de l’impression et des applications qui en dépendent ; vérifier aussi les dépendances d’une éventuelle session graphique sur cette VM |
| Décision | **À appliquer**, sous réserve de validation du besoin métier. Changement du mode de cupsd.conf **À investiguer** si CUPS est conservé |
| Justification | L’absence de rôle identifié justifie de préparer la désactivation ; le test de permissions ne prouve pas une écriture non autorisée. Cette mesure ne met pas à jour le paquet vulnérable |
| Validation future | Absence d’écoute 631 et de socket actif, unités inactives ; test File Browser lors de la reprise prévue en C11 ; vérifier les applications éventuellement dépendantes |
| Retour arrière prévu | Conserver l’état activé/inactif initial des trois unités ; démasquer si nécessaire, restaurer leurs états initiaux et vérifier l’impression |

## Comparaison des sources

| Question | Réponse consolidée |
| --- | --- |
| Quels constats Greenbone sont confirmés ou précisés ? | G01 à G04 : les versions locales précisent les écarts de correctifs ; C07 explique le non-rattachement Pro. G03 : GSSAPI désactivé et transferts précisent les conditions. G04 : LY PRNT-2308 et les écoutes atténuent le scénario distant. G05 : VM nomme les deux MAC de 64 bits |
| Quels problèmes sont identifiés uniquement par Greenbone parmi les sources retenues ? | Les avis de vulnérabilité G01 à G04 et la classification des MAC G05 sont apportés par GB ; VM les corrobore. Les extraits LY ne prouvent pas ces CVE ni ce défaut cryptographique |
| Quels problèmes proviennent de l’audit local ? | Les restrictions SSH C04, l’absence d’auditd C08, les écarts sysctl C09 et le mode cupsd.conf de C06 viennent de LY, avec confirmations VM. C10 et l’arrêt C11 sont des observations manuelles, pas des détections de vulnérabilité GB |
| Quels résultats décrivent un même problème ? | C06 rassemble paquet CUPS vulnérable, service sans rôle identifié et permissions de sa configuration, avec sous-actions distinctes. C07 est une cause de maintenance commune aux paquets. SSH conserve C03/C04/C05 distincts : défaut logiciel, contrôle d’accès et algorithmes demandent des corrections différentes |
| Quels résultats sont nuancés ou contredits ? | CONT-8106 : collecte LY indéterminée, mais inventaire manuel cohérent ; aucun conteneur caché prouvé. KRNL-6000 : forwarding peut servir à Docker. CUPS : écoute locale, pas d’exposition distante démontrée. auditd absent ne signifie pas zéro journal. File Browser actif au relevé antérieur et arrêté maintenant décrit une évolution, pas une contradiction entre outils |

## Complément C11 — état et journaux reçus à 11:17:25 +02:00

| Élément | Preuve et interprétation |
| --- | --- |
| Début de la dernière exécution | `StartedAt=2026-09-30T07:39:25.150904379Z`, soit **09:39:25 +02:00** le 30 septembre |
| Fin | `FinishedAt=2026-09-30T12:42:59.49439413Z`, soit **14:42:59 +02:00** le 30 septembre |
| État Docker | `exited`, code `1`, `OOMKilled=false`, `Error=""`, `RestartCount=0`, `RestartPolicy=no` |
| Dernières lignes | `Caught signal terminated: shutting down.` puis `accept tcp [::]:80: use of closed network connection`, immédiatement avant FinishedAt |
| Conclusion | Arrêt après signal de terminaison observé ; fermeture du listener pendant l’arrêt compatible avec la dernière erreur. Aucun OOM déclaré par Docker ; arrêt volontaire de la VM déclaré par l’utilisateur, corroboré par les journaux Docker/containerd |

Les requêtes HTTP précédentes, vers des chemins PHP/CGI/PHPUnit, ont reçu des
réponses **404** vers **12:18 +02:00**, plus de deux heures avant l’arrêt.
Leur répétition est compatible avec un balayage automatisé ; l’attribution à
Greenbone nécessite une corrélation avec les horaires des tâches. Elles ne
prouvent ni la présence de PHP/PHPUnit, ni une exploitation réussie, ni un lien
causal avec l’arrêt. L’adresse interne source n’est pas reproduite ici.

La politique `no` ne prévoit pas de redémarrage automatique du conteneur.
Ce résultat ne justifie pas à lui seul de changer la politique : il faut
définir le besoin de disponibilité après démarrage de la VM. L’utilisateur
confirme avoir arrêté la VM à cet horaire : la qualification de panne
spontanée est écartée. La reprise automatique reste un besoin à valider.

Contrôle effectué dans la VM, sans modification :

```bash
sudo journalctl -u docker.service -u containerd.service \
  --since '2026-09-30 14:35:00' --until '2026-09-30 14:50:00' \
  --no-pager -o short-iso
```

Cette fenêtre utilise l’heure locale de Paris de la VM. Les résultats montrent
à **14:42:59 +02:00** `Processing signal 'terminated'`, l’arrêt des unités,
`Daemon shutdown complete` et `docker.service: Succeeded`, puis
`containerd.service: Succeeded`. Ils corroborent la déclaration de l’utilisateur
sur l’arrêt volontaire de la VM. Le nettoyage des shims accompagne cet arrêt
et ne démontre pas une attaque.

Le journal consulté le 1er octobre conserve des événements du 30 septembre :
une conservation entre ces deux sessions est donc observée, sans établir la
durée maximale de rétention. Les identifiants internes ne sont pas publiés.
Aucune relance ni modification de politique n’est réalisée.

## Ordre de travail proposé et preuves restantes

1. Clore le diagnostic d’arrêt **C11** : arrêt volontaire expliqué. Définir
   le besoin de reprise de File Browser après démarrage, sans modification
   pendant cette analyse.
2. Préparer la décision de maintenance **C07**, le lot OpenSSH **C03/C04/C05**
   et ses tests d’accès ; distinguer les conditions CVE des options de service.
3. Examiner les usages containerd/BuildKit **C01/C02** et les accès réels aux
   sockets ; compléter les règles sudo d’oliv.
4. Vérifier la séparation des documents **C10** avec des données fictives,
   puis préparer l’audit ciblé **C08** et les dépendances CUPS **C06**.
5. Terminer l’analyse des interfaces et de la persistance **C09** avant de
   choisir des valeurs ; ne pas désactiver globalement le forwarding.

Conserver les rapports GB et LY originaux, leurs dates et empreintes, les
extraits pertinents et les sorties manuelles datées dans le dossier de preuves.
Les nouvelles empreintes LY restent à relever ; ne pas relancer Lynis avant
archivage. Ne pas publier clés, identifiants de démarrage, secrets, journaux
bruts ou documents internes.

## Limite de couverture — contenu de l’image File Browser

La [feuille de préparation du J3](limites-audit-preparer-analyse-conteneur.md)
complète cette analyse : version applicative, tag, ImageID et RepoDigest connus,
plateforme linux/amd64, création de l’image le 6 avril 2021 et configuration
détaillée relevées à 11:36:10 +02:00. Aucun inventaire des composants
internes ni scan de l’image n’est prouvé par GB ou LY. L’absence de constat
applicatif ne permet pas de conclure à l’absence de vulnérabilités. Ce complément
prolonge C10/C11 sans créer une vulnérabilité confirmée supplémentaire.

Le relevé récent `Exited (1) 4 seconds ago` est expliqué par l’utilisateur :
démarrage de contrôle sans erreur constatée, puis arrêt volontaire du conteneur
pour continuer l’activité. **C11 est écarté comme panne spontanée pour cette
nouvelle observation également.** Le succès du démarrage est déclaré par
l’utilisateur ; aucun test HTTP ou fonctionnel complet n’est fourni. Le besoin
de reprise automatique reste distinct et à définir.

Le [contrôle interne optionnel](etendre-audit-conteneur.md) à **11:49:04
+02:00** identifie Alpine 3.13.4, les outils disponibles et File Browser PID 1
avec UID/GID 0. Il précise C10. Lynis n’est pas trouvé dans le PATH ; aucun
audit interne n’a encore été exécuté. Le démarrage montre `health: starting`,
ce qui ne constitue pas une validation healthy.

## Priorités contextualisées

La [feuille d’évaluation des risques](../it-3/evaluer-risques-definir-priorites.md)
justifie le rang de chaque constat et les conditions de révision. Elle précise
C09 en **P3 investigation** et C11 en **P3 besoin d’exploitation**, écarté comme
panne spontanée. Ce classement complète le tableau consolidé et sert de
référence pour préparer les traitements ; aucune mesure n’est appliquée.

## État final de l’exercice

Une seule analyse regroupe **11 constats**, les trois recommandations détaillées
de l’exercice 2.3, leurs décisions et les limites de preuve. Les constats
« À vérifier » restent ouverts. Aucun correctif, fragment SSH, règle auditd,
arrêt CUPS ou changement sysctl n’est appliqué par cette feuille.

- [Activité précédente — Vérifier la configuration du système](verifier-configuration-systeme.md)
- [Retour à l’itération 2](index.md)
- [Dossier de preuves et journal des changements](../dossier-preuves.md)
- [Pense-bête de l’itération](../../pense-bete/glossaire/securisation-avancee-infrastructures/it-2.md)
