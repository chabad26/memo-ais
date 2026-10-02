# Finaliser le rapport d’audit et le plan de remédiation

**Durée indicative : 2 h — Rapport documentaire au 1er octobre 2026, complété le 2 octobre 2026**

## Objectif et statut

Présenter une synthèse compréhensible sans avoir participé aux scans, puis
préparer les mesures à mettre en œuvre à partir du J4. Ce rapport reprend la
[consolidation des trois sources](consolider-trois-sources-audit.md) et complète
la [priorisation](evaluer-risques-definir-priorites.md) avec C12, identifié au J3.

**Plan initial préparé ; R09, R03 et R08 désormais appliquées selon les retours utilisateur. Voir le bilan actualisé en fin de page.** Les validations
après changement sont des critères attendus, pas des résultats acquis.
Les actions restent conditionnées aux dépendances et investigations indiquées.

## Tests manuels applicatifs et retours du 2 octobre 2026

À la demande de la formatrice, Olivier a complété les audits automatisés par
des tests manuels de File Browser. Il confirme une connexion réussie avec
**`admin` / `admin`** et indique que **« le reste [est] ok »** pour les autres
tests proposés. Ces résultats sont déclarés par l’utilisateur ; les captures,
la date exacte d’exécution et le détail des comptes de test restent à joindre.
Aucun de ces tests n’a été exécuté par l’assistant.

| Test manuel | Retour utilisateur | Qualification / preuve restante |
| --- | --- | --- |
| Connexion avec les identifiants par défaut `admin` / `admin` | Connexion réussie | **C13 confirmé selon le test déclaré** ; capture de la session et confirmation du rôle à joindre |
| Accès à l’application sans authentification | Déclaré conforme | Résultat détaillé et capture à joindre |
| Accès direct à un fichier protégé sans session | Déclaré conforme | Préciser le fichier fictif et l’absence de partage public volontaire ; capture à joindre |
| Séparation des comptes et accès hors du dossier autorisé | Déclarée conforme | Compte limité, périmètre et refus à documenter |
| Téléversement et suppression avec un compte en lecture seule | Déclarés conformes | Résultats des deux opérations à documenter |
| Déconnexion puis nouvelle opération protégée | Déclarée conforme | Nouvelle authentification exigée à documenter ; distinguer contenu en cache et accès actif |

### C13 — Identifiants par défaut File Browser actifs

**Source : test manuel d’Olivier, communiqué le 2 octobre 2026.** Le couple
`admin` / `admin` permet de se connecter. Ce constat applicatif complète
Greenbone, Lynis et Trivy : les versions et les configurations techniques ne
suffisent pas à valider l’authentification de l’application.

**Risque élevé ; P1 correction prioritaire.** Une personne pouvant joindre
l’application et connaissant ces identifiants peut accéder au compte
administrateur et aux fonctions permises à ce compte. L’impact potentiel
concerne la confidentialité et l’intégrité des documents et de la
configuration. Aucune utilisation par un tiers, fuite de données ou exposition
Internet n’est démontrée. Les autres tests déclarés conformes ne compensent
pas la faiblesse des identifiants de ce compte.

### R09 — Changer le mot de passe administrateur

**Statut : correction à effectuer**, conformément à la demande utilisateur.
Le changement n’est pas présenté comme déjà réalisé.

1. Conserver la preuve de connexion avec les identifiants par défaut, sans
   afficher de documents internes.
2. Remplacer le mot de passe du compte administrateur par une valeur forte et
   unique ; vérifier les autres comptes administrateurs et les partages.
3. Évaluer la révocation des sessions existantes en préservant un accès
   administrateur valide.
4. Dans une nouvelle session privée, vérifier une fois que `admin` / `admin`
   est refusé, puis que le nouvel accès fonctionne.
5. Vérifier les opérations légitimes sur des fichiers fictifs et joindre les
   preuves avant/après, sans publier le nouveau mot de passe.

**Clôture attendue :** anciens identifiants refusés, nouvel accès validé,
fonctionnement applicatif conservé et comportement des sessions documenté.
Le responsable et l’échéance de correction restent à renseigner.

## 1. Système, périmètre et méthodes

Le système étudié est une VM Ubuntu 20.04.6 LTS, noyau
`5.15.0-139-generic`, exécutant Docker/containerd et File Browser 2.15.0.
Le service applicatif est publié en HTTP sur le port hôte 8080 vers le port
80 du conteneur. SSH fournit l’administration sur le port 22. CUPS est actif,
limité à localhost, sans rôle d’impression identifié.

Le cas fil rouge prévoit des documents publics, internes et partenaires.
Les répertoires correspondants sont montés depuis `/srv/filebrowser` vers
`/srv` en lecture-écriture. File Browser est observé avec UID/GID 0 dans le
conteneur, qui n’est pas privilégié. La sensibilité des données appartient au
contexte pédagogique ; aucune exfiltration ni accès croisé aux documents
n’a été démontré.

**Exposition établie : depuis la machine d’audit du laboratoire.** L’accès
Internet prévu dans le cas n’est pas prouvé. Les observations concernent
l’état relevé ; les arrêts VM et conteneur ont été expliqués comme volontaires.

| Méthode / outil | Périmètre et résultat exploitable | Limites |
| --- | --- | --- |
| Greenbone/OpenVAS J1 | Scans A distant et B avec compte SSH gvm-audit ; couverture TCP 1–65535 de la VM, dont 22/8080 ; écarts de paquets hôte et MAC SSH | Compte sans sudo ; pas d’inventaire exhaustif de l’image ; aucune couverture UDP revendiquée ; absence d’identification File Browser dans les exports |
| Lynis 2.6.2 J2 | Audit local de la VM : 221 tests, 4 avertissements, 52 suggestions, indice 57 ; recommandations SSH, auditd, CUPS, noyau et Docker | Audit interne au conteneur non réalisé ; indice de durcissement non assimilable à un niveau de risque ; métadonnées/empreintes du second rapport à compléter |
| Docker et contrôles manuels | Image et digests, versions, services, écoutes, droits, UID du processus, montages, configuration SSH et journaux | Observations ponctuelles ; aucune exploitation ni validation générale après redémarrage |
| Trivy 0.74.0 J3 | Image exacte exportée/transférée avec empreinte concordante ; 20 paquets Alpine et 53 composants Go ; 294 associations composant–vulnérabilité, dont 13 critiques | Associations non assimilables à 294 vulnérabilités exploitables ou CVE uniques ; version/date des bases à conserver dans les preuves |
| Qualification CVE, code et binaire | Cinq résultats étudiés : quatre écartés dans le périmètre observé, CVE-2022-23806 encore à vérifier | Qualification limitée à ces cinq résultats ; les autres associations ne sont pas toutes analysées |

L’image analysée est identifiée par
`sha256:a68f43720ea6ff331fa4b92becced20af14b72f4c3a22ca1f764076a8e42e1a5`,
avec RepoDigest
`filebrowser/filebrowser@sha256:1595cf9b36528113a18178996d9ff9ee8bc7814699bb5f8e1d8ad8ec48aa89ac`.
Trivy relève Alpine 3.13.4 avec `EOSL=true` et Go 1.16.2. La date de création
Docker est le 6 avril 2021 ; le diagnostic de fin de support repose sur les
preuves du J3, pas sur cette seule date.

## 2. Principaux constats et ordre de traitement

**Confirmé** qualifie l’état ou le défaut décrit, sans affirmer qu’une attaque
a été reproduite. P1 désigne la première séquence de préparation, P2 un
traitement haut mais conditionnel, P3 un traitement planifié ou une investigation
à exposition limitée. Les scores CVSS historiques restent consultables dans
les fiches J1 ; ils ne déterminent pas cet ordre.

| Constats | Preuves déterminantes | Risque et priorité finale |
| --- | --- | --- |
| **C13 — Identifiants par défaut File Browser** | Connexion `admin` / `admin` réussie selon le test manuel utilisateur ; capture à joindre | **P1 correction prioritaire** : changer le mot de passe et valider le refus des anciens identifiants |
| **C07 — Maintenance hôte** | Pro non rattaché, plusieurs écarts de versions, candidats locaux identiques | **P1 décision** : choisir une voie de maintenance avant les correctifs ; disponibilité actuelle et fraîcheur APT à vérifier |
| **C03/C04 — SSH logiciel et accès** | Version locale et avis J1 ; port 22 joint ; mot de passe et transferts autorisés, root par clé possible | **P1 préparation** : point d’administration joignable ; distinguer conditions CVE et usages légitimes avant changement |
| **C12 — Image hors support** | ImageID précis, Alpine EOSL, composants Go anciens et résultats Trivy qualifiés | **P1 préparation de migration** : chaîne applicative non maintenue au contact des documents ; priorité structurelle, aucune compromission ni applicabilité de toutes les CVE affirmée |
| **C10 — UID 0 et données RW** | PID 1 UID/GID 0, montage RW, permissions observées | **P2 investigation puis réduction** : limiter les conséquences d’une compromission ; droits effectifs et compatibilité à tester |
| **C01/C02 — containerd et Docker/BuildKit** | Versions confirmées, avis GB, services/sockets présents | **P2** : risque moteur conditionnel ; inventorier fonctions et constructions, puis traiter avec la maintenance hôte |
| **C08 — Audit ciblé absent** | Paquets et unité auditd absents ; journald/rsyslog actifs | **P2 préparation** : mieux reconstruire les actions sensibles ; dimensionner règles, volume et rétention |
| **C05 — MAC SSH** | Deux MAC 64 bits proposés à distance et dans sshd -T | **P2 planification** : retirer les algorithmes signalés après test des clients, dans le lot SSH |
| **C06 — CUPS** | Version ancienne, localhost, aucune imprimante, permissions confirmées | **P3** : réduire une surface locale sans besoin établi ; dépendances à vérifier avant désactivation |
| **C09 — Paramètres noyau** | Valeurs sysctl et fragments relevés | **P3 investigation** : contexte réseau incomplet ; une modification globale pourrait casser Docker |
| **C11 — Arrêts volontaires / reprise** | Déclaration utilisateur et journaux d’arrêt concordants | **Non pertinent comme panne** ; **P3 besoin d’exploitation** pour la reprise automatique éventuelle |

C12 complète la priorisation antérieure qui portait sur C01–C11. Son rang est
justifié par le rôle applicatif et le cycle de maintenance, pas par les 13
lignes critiques seules. Si l’accès Internet est démontré, les accès SSH/HTTP
et la migration applicative doivent être réexaminés en première séquence.

## Décision de migration précisée au J4 — 2 octobre 2026

La préparation retient **Ubuntu 26.04 LTS** comme cible R01 (cible actualisée par Olivier) et une mise à
niveau de **File Browser vers sa dernière release publiée** pour R03. Ces
migrations traitent plusieurs écarts logiciels ensemble ; la réduction des
failles devra être démontrée par les versions et scans avant/après. Les défauts
de mot de passe, configuration et privilèges restent des actions séparées.

Le [détail des choix et parcours de migration](../it-4/preparer-remediations.md#choix-retenu-traiter-les-versions-legacy-par-deux-migrations-prioritaires)
précise les étapes Ubuntu 20.04 → 22.04 → 24.04 → 26.04 ou la migration vers une nouvelle
VM. File Browser **2.63.23** est la dernière release relevée le 2 octobre ;
le [projet original est archivé](https://github.com/filebrowser/filebrowser)
et n’annonce plus de corrections futures. La dernière release est donc une
cible de mise à niveau à tester, sans la qualifier de solution maintenue.

## 3. Plan de remédiation regroupé pour le J4

Les lots regroupent les changements qui traitent plusieurs constats. Les
investigations préalables restent explicites. Les versions cibles ne sont pas
inventées : elles seront choisies et vérifiées avant l’intervention.

| Lot / constats | Action proposée | Priorité | Effet attendu | Impact ou contrainte possible | Vérification après modification |
| --- | --- | --- | --- | --- | --- |
| **R09 — C13** | Changer le mot de passe administrateur, vérifier comptes/partages et gestion des sessions | **P1 correction prioritaire** | Supprimer l’accès par identifiants par défaut | Préserver un accès administrateur valide ; ne pas diffuser le nouveau secret | En session privée : anciens identifiants refusés, nouvel accès accepté ; opérations sur fichiers fictifs validées ; captures à joindre |
| **R01 — C07, C01, C02, C03 ; C06 si conservé** | Migrer vers Ubuntu 26.04 LTS (nouvelle VM ou étapes 22.04, 24.04 puis 26.04) ; choisir les versions corrigées, sauvegarder l’état, mettre à jour l’hôte et les moteurs dans une fenêtre prévue | **P1 préparation** ; correctifs moteurs P2 | Restaurer une voie de maintenance et réduire les écarts logiciels confirmés | Coût/éligibilité, compatibilité, redémarrages et interruption Docker/SSH ; ne pas faire une migration non testée sur les données seules | Versions exactes et source des paquets ; services actifs ; nouvelle connexion SSH ; conteneur et HTTP ; nouveau GB et LY de périmètre comparable ; reprise après redémarrage si concernée |
| **R02 — C03/C04/C05** | Coordonner correctif SSH et durcissement : PermitRootLogin no, MaxAuthTries 3, transferts TCP/agent et X11 no, LogLevel VERBOSE ; préparer liste MAC sans les deux umac-64 ; mot de passe à traiter séparément après validation des clés | **P1 préparation** pour accès, MAC P2 | Réduire connexion root directe, fonctions de rebond et offre cryptographique faible ; améliorer traces | Tunnels et clients incompatibles ; perte d’administration possible ; ordre des fragments/Match à vérifier | sshd -t et configuration effective par contexte ; connexion administrateur et gvm-audit par clé ; refus des transferts/root attendus ; négociation MAC ; journaux et scan GB |
| **R03 — C12, avec C10** | Préparer la dernière release File Browser publiée (2.63.23 relevée le 2 octobre), vérifier image/digest et traiter la fin de maintenance du projet original, préparer migration de la base/configuration/données en environnement de test ; rescanner avant bascule ; tester UID non privilégié et droits minimaux | **P1 préparation migration**, restrictions C10 P2 | Réduire les vulnérabilités historiques et les conséquences d’un défaut applicatif ; maintenance future non rétablie par la dernière release | Format de base, options et permissions pouvant changer ; interruption et retour arrière après écritures à prévoir | Trivy sur l’image cible exacte avec bases datées ; examiner résultats résiduels ; version/processus/montages ; connexion, téléchargement et téléversement de fichiers fictifs ; séparation des rôles et intégrité des données |
| **R04 — C10** | Après tests, limiter UID, capacités, privilèges supplémentaires et écritures aux chemins utiles ; étudier no-new-privileges et racine en lecture seule avec chemins d’écriture adaptés | **P2**, coordonné avec R03 | Limiter droits et surface d’écriture du processus | L’application et sa base doivent pouvoir écrire aux emplacements requis ; un durcissement aveugle peut empêcher le démarrage | UID réel, capabilities et NoNewPrivs ; fichiers nécessaires accessibles ; opérations non autorisées refusées ; tests fonctionnels et redémarrage ; aucune modification globale de propriétaire des documents sans justification |
| **R05 — C08** | Préparer auditd avec règles ciblées pour identité et configuration SSH ; dimensionner rotation/rétention et collecte future | **P2** | Traces structurées des actions sensibles | Bruit, espace disque, CPU et doublons ; chemins à valider | Règles chargées, événements de test retrouvés, rotation et stockage ; fonctionnement SSH/Docker conservé ; intégration Wazuh seulement si mise en œuvre |
| **R06 — C06** | Valider absence de dépendances ; désactiver cups.service, cups.socket, cups.path ; si conservé, correctif et permissions à examiner | **P3** | Réduire une fonction locale inutile | Impression ou applications desktop dépendantes interrompues | États des unités, absence de listener/socket attendu, application métier et dépendances vérifiées ; ne pas confondre arrêt du service et correction du paquet |
| **R07 — C09** | Qualifier interfaces, core_pattern, besoins Docker et origine/persistance ; appliquer seulement les sysctl retenus | **P3 investigation**, modification conditionnelle | Réduire un risque précis sans casser le réseau | Forwarding Docker, routage asymétrique et diagnostics impactés | Valeurs effectives et après redémarrage ; flux conteneur/hôte et accès SSH ; tests de refus correspondant au risque identifié |
| **R08 — C11** | Définir besoin de reprise ; si service attendu au démarrage, choisir et documenter une politique adaptée | **P3 conditionnelle** | Disponibilité conforme au besoin validé | Un redémarrage automatique peut remettre en écoute un service volontairement arrêté | Démarrage VM contrôlé, état/health du conteneur, HTTP et parcours applicatif ; comportement après arrêt volontaire et retour à l’état prévu |

## 4. Investigations avant de choisir ou appliquer une mesure

| Question ouverte | Décision qu’elle conditionne | Preuve attendue |
| --- | --- | --- |
| Exposition externe et filtrage | Urgence des lots SSH et applicatif ; restriction des flux éventuelle | Règles effectives, routage et test autorisé depuis le point pertinent |
| Versions corrigées disponibles et cible maintenue | R01/R03 | Avis et sources de paquets/image vérifiés, versions et plateforme compatibles, résultat de scan conservé |
| BuildKit et fonctions containerd utilisées | Applicabilité et ordre C01/C02 | Constructions, utilisateurs, contextes et configurations réellement utilisés |
| Données, base File Browser et UID/mappage | R03/R04 | Inventaire privé, sauvegarde restaurable, test migration et permissions avec données fictives |
| Dépendances SSH et CUPS | R02/R06 | Liste des usages, clients, clés et applications à préserver |
| CVE-2022-23806 | Qualification du risque spécifique dans C12 | Chemin d’appel vers CurveParams.IsOnCurve et entrée contrôlable ; la migration structurelle n’exige pas d’affirmer cette CVE exploitable |
| Rétention et volume des événements | R05 | Configuration et historique, capacité disque, simulation limitée de règles |
| Rapport LY et bases TR | Reproductibilité des comparaisons | Métadonnées, empreintes, versions/bases et options manquantes complétées |

## 5. Décisions de non-intervention dans le périmètre actuel

| Élément | Décision et justification | Condition de réexamen |
| --- | --- | --- |
| Arrêts File Browser | Pas de traitement d’incident : arrêts volontaires expliqués | Arrêt inattendu nouveau ou exigence de reprise validée |
| CVE-2020-26160, CVE-2021-44716, CVE-2021-3711, CVE-2022-37434 | Pas de correction spécifique fondée sur ces scénarios : exclus pour le périmètre qualifié dans la feuille CVE | Changement de code, protocole, bibliothèques ou chemin d’usage ; cette exclusion ne dispense pas R03 |
| CUPS exposé à distance / absence totale de logs | Ne pas traiter ces scénarios non observés ; C06 et C08 restent retenus pour leurs défauts propres | Nouvelle écoute externe ou interruption de la collecte |
| Forwarding IPv4 | Pas de désactivation globale sur la seule suggestion Lynis | Analyse réseau démontrant une valeur alternative compatible |
| Reconstruction pour exécuter Lynis interne | Ne pas transformer l’image en système complet uniquement pour l’outil | Méthode légère compatible identifiée ; aucune absence de scan assimilée à une absence de risque |
| Mot de passe SSH et permissions du socket CUPS | Pas de modification immédiate sans usages/critères établis | Clés administrateurs validées et besoin métier établi ; permissions service documentées |

## 6. Préparer la mise en œuvre et le retour arrière

Pour chaque lot, renseigner au J4 le responsable réel, la fenêtre, les objets
exactement modifiés et les critères d’arrêt. Archiver les versions et
configurations initiales en privé. Vérifier une sauvegarde restaurable de la
base/configuration et des données avant R03 ; conserver l’ancienne image par
son identité. Un simple retour à l’ancien tag ne restaure pas une base migrée
ou les documents modifiés : prévoir un état cohérent et contrôler les écritures
pendant la bascule.

Pour SSH, garder console et session de secours jusqu’à validation d’une nouvelle
connexion. Pour les règles audit/sysctl, restaurer uniquement les fichiers et
valeurs du lot concerné ; ne pas purger globalement des règles ou traces.
Éviter de cumuler tous les lots avant vérification : attribuer chaque effet au
changement qui l’a produit.

**Critère de clôture d’un lot :** preuve avant/après sur le défaut ciblé,
validation fonctionnelle, risque résiduel explicite et résultat du retour
arrière ou de sa préparation. Un score amélioré seul ne ferme pas le constat.

## 7. Preuves et livrables finaux

Le dossier de preuves doit relier chaque constat aux rapports originaux et
chaque action à ses validations. Conserver rapports GB A/B, rapport et journal
LY, export d’image et empreintes, rapport TR avec options/bases, qualifications
CVE et contrôles manuels datés. Les fichiers bruts restent privés ; masquer
secrets, identifiants et données internes dans les copies diffusées.

| Source détaillée | Usage pour ce rapport |
| --- | --- |
| [Greenbone J1](../it-1/premier-audit-greenbone.md) | Versions, avis, QoD, couverture et scores historiques |
| [Vérifications J2](../it-2/verifier-configuration-systeme.md) | Valeurs effectives, permissions, journalisation et arrêts expliqués |
| [Image et conteneur](../it-2/limites-audit-preparer-analyse-conteneur.md) | Identité de l’image, montages et limites de couverture |
| [Scan Trivy](analyser-image-trivy.md) | Inventaire et analyse reproductible de l’image |
| [Qualification CVE](analyser-verifier-resultats-trivy.md) | Scénarios exclus et condition encore ouverte |
| [Consolidation finale](consolider-trois-sources-audit.md) | Registre unique des constats et exclusions |

**Livrables documentaires produits :** synthèse du système et des méthodes,
constats prioritaires, neuf lots de remédiation, investigations et décisions de
non-intervention. **Mise en œuvre à partir du J4**, avec preuves de validation
à compléter ; aucun changement n’est annoncé comme réalisé.

- [Activité précédente — Évaluer les risques et définir les priorités](evaluer-risques-definir-priorites.md)
- [Retour à l’itération 3](index.md)
- [Dossier de preuves et journal des changements](../dossier-preuves.md)

## Suivi R09 — Retour du 2 octobre 2026

Olivier confirme le **changement du mot de passe administrateur** et le
**refus de l’ancien mot de passe, y compris en navigation privée**. R09 est
appliquée selon ce retour ; le nouvel accès, le test fonctionnel et les
captures restent à confirmer avant clôture complète. Les mentions « à
effectuer » dans la préparation décrivent l’état avant ce retour.

[Résultat détaillé et limites](../it-4/mettre-en-oeuvre-verifier-remediations.md#r09-mot-de-passe-administrateur-change-retour-du-2-octobre-2026).

## Bilan des remédiations réalisées — Actualisation du 2 octobre 2026

Ce bilan actualise le plan initial, dont les tableaux décrivent les actions
préparées avant intervention. Les modifications et tests fonctionnels sont
**déclarés réussis par Olivier** ; les sorties de sauvegarde, d’inspection de
l’image et le rapport Trivy ont été examinés. Les captures de bascule et de
validation applicative restent à joindre.

| Action | Modification et résultat | Statut et preuve restante |
| --- | --- | --- |
| **R09 / C13 — Identifiants par défaut** | Mot de passe administrateur changé ; ancien mot de passe refusé, y compris en navigation privée ; nouvel accès et opérations fictives déclarés réussis | **Appliquée et validée selon le retour utilisateur** ; captures à joindre. Révocation des anciennes sessions non démontrée |
| **R03 / C12 — Image File Browser** | Migration **2.15.0 → 2.63.23**, test préalable sur copies puis bascule déclarés réussis ; ancien conteneur et sauvegardes conservés | **Appliquée ; fonctionnement déclaré validé** ; 10 HIGH résiduels à qualifier et maintenance future à traiter |
| **Persistance applicative** | Documents, base et configuration montés dans des répertoires hôte distincts ; conservation des comptes et fichier après redémarrage déclarée réussie | **Configurée selon retour utilisateur** ; chemin hôte exact et inspection finale à joindre. Nouvelle recréation de validation non explicitement rapportée |
| **R08 — Reprise automatique** | Politique `unless-stopped` et activation de Docker au démarrage ; reprise après redémarrage VM déclarée réussie | **Appliquée et validée selon retour utilisateur** ; preuves de politique et reprise à joindre ; un arrêt manuel reste respecté |
| **R01 — Ubuntu** | Cible documentaire Ubuntu 26.04 ; dernier état initial fourni : Ubuntu 20.04.6 | **À réaliser**, après les travaux File Browser ; aucun changement de l’hôte démontré |

Image cible examinée : ImageID
`sha256:b3983274c0375dda1722f8e2b65c30d1b9001435e441f0a34855c2e5f8da462e`,
RepoDigest
`filebrowser/filebrowser@sha256:a469ea076d4a1b4b1d86a41d130f2f536cd9da996a2b1fb39c0d7635f9d89b9a`.

### Vérification Trivy après migration

| Niveau | Avant : relevé historique 2.15.0 | Après : export 2.63.23 examiné |
| --- | --- | --- |
| HIGH | 143 | 10 |
| CRITICAL | 13 | 0 |
| Total HIGH/CRITICAL | 156 | 10 |

Le compteur diminue de **146 associations, soit environ 93,6 %**. Ce résultat
ne prouve pas que 146 vulnérabilités exploitables ont été corrigées : bases,
options et périmètres doivent être documentés pour une comparaison précise.
Le rapport actuel porte sur `bin/filebrowser` (gobinary), avec dépendances Go ;
absence d’objet OS dans ce JSON ne signifie pas absence de vulnérabilité OS.
Les 10 HIGH concernent x/crypto (1), x/image (1) et stdlib Go (8).
`fixed` indique une correction disponible selon le scanner, pas installée.

**Limite de preuve initiale :** le JSON actuellement nommé
`trivy-filebrowser-v2.15.0.json` contient aussi la nouvelle image et 10 HIGH.
Retrouver une copie de l’export initial ou rescanner l’ancienne image conservée
sous un nouveau nom, avec bases/options comparables. La colonne « avant »
provient du relevé précédemment examiné et documenté.

Le [projet original File Browser est archivé](https://github.com/filebrowser/filebrowser).
La mise à niveau réduit les détections historiques, sans garantir la maintenance
future ni supprimer tous les risques résiduels. Ubuntu ne corrigera pas les
dépendances Go compilées dans cette image. Les autres lots de durcissement
restent à appliquer et vérifier selon leur état réel.

[Suivi détaillé des interventions et preuves](../it-4/mettre-en-oeuvre-verifier-remediations.md).
