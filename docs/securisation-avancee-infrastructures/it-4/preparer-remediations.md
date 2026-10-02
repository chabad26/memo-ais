# Préparer les remédiations

**Itération 4 — Préparation à partir du plan du J3 — 2 octobre 2026**

## 🎯 Objectif

Sélectionner et préparer les modifications à réaliser à partir du
[rapport d’audit et du plan de remédiation du J3](../it-3/finaliser-rapport-plan-remediation.md),
en commençant par les problèmes prioritaires. Pour chaque modification,
distinguer le bénéfice de sécurité, les conséquences fonctionnelles et les
preuves qui permettront de valider le changement.

**Statut : préparation documentaire réalisée ; modifications à mettre en œuvre.**
Aucun changement de mot de passe, mise à jour, migration, durcissement ou test
après correction n’est présenté comme effectué dans cette feuille. Les
commandes exactes seront recherchées lors de la mise en œuvre, selon les
versions et les configurations réellement présentes.

## 1. Reprendre les constats et les retours du J3

Le laboratoire concerne la VM Ubuntu 20.04 hébergeant Docker/containerd et
File Browser 2.15.0, accessible sur le port 8080 depuis la machine d’audit.
SSH assure l’administration sur le port 22. L’exposition Internet appartient
au cas pédagogique ; elle n’est pas démontrée pour le laboratoire.

Le plan croise Greenbone, Lynis, Trivy et les contrôles manuels. Les
[tests applicatifs communiqués par Olivier](../it-3/finaliser-rapport-plan-remediation.md#tests-manuels-applicatifs-et-retours-du-2-octobre-2026)
ajoutent un problème directement vérifié : **la connexion avec `admin` / `admin`
réussit**. Les autres tests proposés sont déclarés conformes ; leurs détails et
captures restent à joindre. Ce retour ne prouve pas que le mot de passe a
ensuite été changé.

Les identifiants **C01 à C13** et **R01 à R09** du plan sont conservés. C11 est
écarté comme panne spontanée : les arrêts ont été expliqués comme volontaires.
Une ligne Trivy HIGH ou CRITICAL ne devient pas automatiquement une correction
indépendante ; l’image ancienne est traitée dans le lot R03.

## Actualisation de la cible Ubuntu — 2 octobre 2026

Olivier a remplacé la cible Ubuntu 24.04 par **Ubuntu 26.04** dans cette
préparation, en indiquant que la version 26 est proposée depuis Ubuntu 24.
Olivier précise avoir **uniquement modifié la cible dans la documentation**.
La mise à niveau de la VM reste **à réaliser**. Aucune clôture des constats ni
validation de Docker, SSH ou File Browser n’est déduite de cette modification.

Pour relever l’état réel sur la VM, conserver une capture de :

```bash
date -Is
cat /etc/os-release
uname -r
dpkg-query -W openssh-server docker.io containerd
sudo systemctl is-active ssh docker containerd
sudo docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
```

Ces commandes sont à exécuter, non exécutées lors de cette mise à jour.
Un paquet absent de `dpkg-query` demande de relever le paquet réellement
utilisé ; ne pas en conclure automatiquement que le service est absent.
Compléter par une nouvelle connexion SSH et un parcours File Browser dans
le navigateur, puis les scans avant/après prévus.

## Choix retenu — Traiter les versions legacy par deux migrations prioritaires

**Décision documentaire du 2 octobre 2026 :** les versions anciennes de l’hôte
et de l’application sont une cause commune à plusieurs constats. Les lots
principaux retenus sont **R01 : Ubuntu 20.04 vers Ubuntu 26.04 LTS** et
**R03 : File Browser 2.15.0 vers la dernière version publiée, vérifiée avant
intervention**. Le changement du mot de passe par défaut R09 reste prioritaire
et ne doit pas attendre ces migrations.

La mise à niveau doit réduire les vulnérabilités des composants remplacés.
L’affirmation « la plupart des failles sont corrigées » reste une hypothèse à
mesurer : comparer les constats Greenbone et les associations Trivy avant/après,
avec des périmètres, filtres et bases documentés. La migration Ubuntu ne met
pas à jour les composants Alpine/Go embarqués dans l’image File Browser.

| Migration / action | Constats concernés | Résultat attendu et limite |
| --- | --- | --- |
| **Ubuntu 26.04 LTS — R01** | C07 et écarts de paquets C01/C02/C03 ; C06 si CUPS conservé | Hôte maintenu avec versions corrigées des paquets réellement installés ; vérifier chaque avis applicable, les dépôts et les nouveaux scans |
| **Dernière version publiée File Browser — R03** | C12 et associations Trivy des composants remplacés | Réduction des vulnérabilités présentes dans l’ancienne image ; scanner le digest exact de la nouvelle image et qualifier les résultats résiduels |
| **Durcissement complémentaire** | C13, C04/C05, C10, C08 et C09 selon vérification | Mot de passe existant, réglages SSH, droits/montages, journalisation et sysctl peuvent persister : vérifier puis corriger séparément |

### Ubuntu : préparer le chemin vers 26.04 LTS

Pour une mise à niveau sur place, Ubuntu impose les LTS successives :
**20.04 → 22.04 → 24.04 → 26.04**, avec validation de chaque étape. L’autre méthode
est de préparer une **nouvelle VM Ubuntu 26.04 LTS**, restaurer les données et
configurations nécessaires, tester puis basculer. Le choix de méthode reste à
établir avant intervention ; la cible 26.04 est retenue.
[Source : guide officiel Ubuntu](https://ubuntu.com/server/docs/how-to/software/upgrade-your-release/).

### File Browser : dernière version publiée et maintenance future

Au contrôle du **2 octobre 2026**, la page officielle désigne
[**v2.63.23** comme dernière release](https://github.com/filebrowser/filebrowser/releases/tag/v2.63.23).
Ce numéro est une référence de préparation ; vérifier la disponibilité de
l’image correspondante, ses notes de migration et son digest avant bascule.
Le tag flottant `latest` ne constitue pas une identité de déploiement suffisante.

**Correction de la qualification « image maintenue » :** le
[dépôt original](https://github.com/filebrowser/filebrowser) est archivé et
annonce l’arrêt des nouvelles versions et corrections de sécurité. Passer à
la dernière release peut corriger des défauts historiques, mais ne rétablit
pas une maintenance pérenne. R03 inclut donc la décision de maintien temporaire
avec risque résiduel explicite ou de remplacement par une solution maintenue,
à étudier sans prétendre que cette migration est déjà réalisée.

Le projet signale notamment des limites non résolues sur l’exécution de
commandes et la gestion des sessions/JWT. Ne pas supposer qu’un changement de
mot de passe ou une déconnexion révoque tous les jetons : vérifier le comportement
réel de la version cible et les mesures compensatoires nécessaires.

## 2. Sélection et ordre de mise en œuvre

| Ordre | Action retenue | Priorité et justification | Condition avant intervention |
| --- | --- | --- | --- |
| 1 | **R09 — Remplacer les identifiants par défaut** | **P1 correction prioritaire** : connexion réellement réussie selon le test utilisateur ; accès au compte administrateur avec un secret connu | Conserver la preuve, identifier le compte et préparer un nouvel accès valide |
| 2 | **R01 — Migrer vers Ubuntu 26.04 LTS** | **P1 décision/préparation** : conditionne plusieurs correctifs de l’hôte | Choisir nouvelle VM ou parcours 20.04 → 22.04 → 24.04 → 26.04 ; vérifier dépôts, sauvegarde et compatibilité |
| 3 | **R02 — Corriger et durcir SSH** | **P1 préparation**, retrait des MAC en P2 : point d’administration joignable | Accès par clé et console de secours validés, usages des tunnels et clients identifiés |
| 4 | **R03 — Mettre à niveau File Browser vers la dernière release publiée** | **P1 préparation** : chaîne applicative ancienne, Alpine signalé hors support, documents servis | Release 2.63.23 relevée, image/digest à vérifier ; sauvegarde et migration testées ; maintenance future à traiter |
| 5 | **R04 — Réduire les privilèges du conteneur** | **P2**, coordonné avec R03 : UID 0 et montage documentaire RW augmentent l’impact potentiel | Déterminer les écritures nécessaires, les droits et la compatibilité avec un UID non privilégié |
| 6 | **R01 — Corriger containerd/Docker** | **P2**, après décision de maintenance : moteurs réellement utilisés, scénarios CVE conditionnels | Inventorier usages containerd/BuildKit, accès aux sockets et versions corrigées |
| 7 | **R05 — Préparer l’audit ciblé** | **P2** : auditd absent, mais journald/rsyslog présents | Dimensionner règles, stockage et rétention |
| 8 | **R06 — Retirer CUPS si inutile** | **P3** : écoute locale et absence de rôle identifié | Confirmer l’absence de dépendance métier ou graphique |

Cet ordre distingue une correction limitée immédiatement préparée (R09) des
migrations et changements nécessitant une validation préalable. Les actions
R02 et R03 peuvent être préparées en parallèle ; leur application reste
séquentielle pour attribuer les effets à chaque changement.

**Actions différées :** R07 (sysctl) reste une investigation P3 tant que les
besoins réseau Docker ne sont pas établis. R08 (reprise automatique) reste
conditionnelle au besoin de disponibilité. Aucune désactivation globale du
forwarding ni politique de redémarrage n’est sélectionnée à ce stade.

## 3. Modifications envisagées, bénéfices et conséquences

| Action / constat | Modification envisagée | Effet de sécurité attendu | Composants concernés | Conséquences possibles sur le fonctionnement |
| --- | --- | --- | --- | --- |
| **R09 / C13** | Remplacer le mot de passe du compte administrateur par une valeur forte et unique ; examiner comptes, partages et révocation des sessions | Supprimer l’accès avec les identifiants par défaut | Compte admin, authentification et sessions File Browser | Perte d’accès si le nouveau secret n’est pas conservé ; reconnexion des sessions révoquées |
| **R01 / C07, C01, C02, C03 ; C06 si conservé** | Migrer Ubuntu 20.04 vers 26.04 LTS par une nouvelle VM ou par étapes 22.04 puis 24.04 et enfin 26.04 ; installer les correctifs disponibles et versions compatibles après tests | Rétablir une maintenance suivie et réduire les écarts logiciels documentés | OS, dépôts, Docker, containerd, OpenSSH, CUPS si conservé | Redémarrages, interruption de File Browser/SSH, changements de réseau ou de compatibilité ; coûts éventuels à examiner |
| **R02 / C03, C04, C05** | Coordonner correction OpenSSH et restrictions : root direct interdit, MaxAuthTries 3, transferts TCP/agent et X11 désactivés si inutiles, LogLevel VERBOSE ; retirer les deux MAC umac-64 signalés ; désactiver le mot de passe seulement après validation des clés | Réduire les accès et fonctions inutiles et l’offre cryptographique signalée faible | Paquet OpenSSH, configuration principale et fragments, blocs Match, comptes/clients d’administration | Verrouillage administratif, tunnels ou clients incompatibles ; volume de logs supérieur |
| **R03 / C12, lié à C10** | Préparer la dernière release File Browser publiée (2.63.23 au contrôle), vérifier l’image/digest ; tester base, configuration et données ; traiter séparément la fin de maintenance du projet | Réduire les vulnérabilités historiques de la chaîne embarquée ; qualifier les défauts résiduels et la maintenance future | Image File Browser, conteneur, base, configuration, volumes et documents | Incompatibilité de base/options, interruption ; anciennes versions pouvant ne plus lire une base migrée |
| **R04 / C10** | Tester UID non privilégié, capacités minimales et no-new-privileges ; étudier racine en lecture seule avec chemins d’écriture adaptés | Limiter les conséquences d’une compromission applicative | Configuration Docker, UID/GID, capacités, montages, permissions/ACL | Démarrage impossible ou échec des téléversements si base et chemins utiles deviennent inaccessibles |
| **R05 / C08** | Installer/configurer auditd avec règles ciblées pour identité et SSH ; préparer rotation/rétention | Améliorer la reconstitution des actions sensibles | auditd, règles, journaux, stockage ; collecte future si retenue | Charge, bruit, saturation disque ou doublons avec une future collecte |
| **R06 / C06** | Après confirmation du besoin, arrêter/désactiver cups.service, cups.socket et cups.path ; si conservé, corriger le paquet | Réduire une surface locale sans fonction utile identifiée | CUPS, ses unités et dépendances | Perte d’impression ou impact sur une application dépendante ; l’arrêt seul ne corrige pas le paquet |

Les paramètres exacts restent à valider avant application. Ubuntu 26.04 LTS
est la cible retenue ; File Browser 2.63.23 est la dernière release relevée,
avec image et maintenance future à valider. Aucune CVE conditionnelle n’est
déclarée exploitée.
Le remplacement du mot de passe ne résout pas l’obsolescence de l’image ; la
migration de l’image ne garantit pas le changement d’un mot de passe conservé
dans une base persistante.

## 4. Vérifier la sécurité et le service séparément

Les deux validations sont nécessaires : une application indisponible peut
refuser une connexion sans que l’authentification ait été correctement corrigée.
Un simple HTTP 200 ne prouve pas le bon fonctionnement des droits applicatifs.

| Action | Vérification de l’effet de sécurité | Vérification du maintien du service |
| --- | --- | --- |
| **R09** | Dans une nouvelle session privée, un essai `admin` / `admin` doit être refusé ; vérifier les comptes administrateurs et le comportement des anciennes sessions | Connexion avec le nouveau secret acceptée ; navigation, téléchargement et téléversement autorisés sur fichiers fictifs |
| **R01** | Relever versions et sources exactes ; comparer aux correctifs retenus ; rescanner les constats GB concernés avec périmètre/filtres comparables | SSH par clé opérationnel ; Docker/containerd actifs ; conteneur démarré et parcours applicatif réussi ; reprise après redémarrage si concernée |
| **R02** | Validation syntaxique et configuration effective, y compris Match ; refus root/transferts attendus, algorithmes négociés vérifiés et nouveau contrôle Greenbone | Nouvelle connexion administrateur et gvm-audit par clé ; usages légitimes identifiés encore opérationnels ; console/session de secours conservées jusque-là |
| **R03** | Trivy sur l’image cible exacte avec options/bases conservées ; qualifier les résultats résiduels ; retester les identifiants par défaut et les autorisations | Connexion, téléchargement et téléversement fictifs ; séparation des comptes ; intégrité des données et compatibilité de la base ; redémarrage contrôlé |
| **R04** | UID réel, capacités, NoNewPrivs et montages conformes à la cible ; opérations hors droits refusées | Démarrage, accès à la base, opérations autorisées, persistance des fichiers après redémarrage |
| **R05** | Règles chargées et événement de test retrouvé ; rotation/rétention conformes au besoin choisi | SSH/Docker/File Browser fonctionnels ; charge et espace disque compatibles ; aucune saturation lors du test |
| **R06** | Unités et écoute/socket CUPS absents selon la cible retenue ; si conservé, version corrigée vérifiée | File Browser et les dépendances recensées fonctionnent ; test d’impression si une fonction doit être conservée |

**État actuel : toutes ces validations après changement sont attendues, non
réalisées.** Les tests applicatifs précédemment déclarés conformes servent de
référence, mais devront être répétés après les changements concernés.

## 5. Conserver l’état initial et préparer le retour arrière

| Action | État initial à conserver en privé | Retour à l’état précédent / point d’arrêt |
| --- | --- | --- |
| **R09** | Identité/rôle du compte, méthode de récupération, paramètres de session ; sauvegarde applicative protégée si nécessaire | En cas de perte d’accès, utiliser la procédure de récupération propre à la version ou l’accès administratif de secours ; rétablir un secret sûr, sans remettre volontairement admin/admin |
| **R01** | Versions, dépôts, réseau et configuration des services ; sauvegarde restaurable de la VM et des données ; état Docker | Si incompatibilité ou perte d’accès, arrêter le lot et restaurer un état cohérent validé ; ne pas compter sur un simple downgrade non testé |
| **R02** | Configuration SSH complète, fragments/Match, versions et liste des accès requis | Via console ou session de secours, restaurer les fichiers du lot, valider la syntaxe et rétablir le service ; ne fermer le secours qu’après une nouvelle connexion réussie |
| **R03** | Ancienne image exacte/digest, configuration Docker, sauvegarde cohérente de base/configuration/documents et preuve de restauration | Stopper les écritures pendant la bascule ; en cas d’échec, restaurer ensemble image et données compatibles. Revenir au tag seul ne restaure pas une base migrée |
| **R04** | Configuration du conteneur, UID/GID, modes/ACL et droits initiaux des seuls chemins concernés | Restaurer seulement les paramètres et droits modifiés ; aucun changement récursif global de propriétaire sans inventaire |
| **R05** | Règles existantes, réglages de rotation/rétention et état initial du service | Retirer les seules règles ajoutées et restaurer les réglages concernés ; conserver les traces, ne pas purger globalement l’audit |
| **R06** | États activés/inactifs/masqués des trois unités et configuration CUPS | Restaurer chaque état initial ; redémarrer et vérifier uniquement si la fonction doit être rétablie |

Les sauvegardes, bases, secrets et exports bruts restent hors du dépôt. Un
snapshot facilite un retour technique mais ne dispense pas d’une sauvegarde
restaurable et de la maîtrise des écritures intervenues après sa création.

## 6. Déroulement prévu et preuves à conserver

1. Archiver les résultats du J3 et les preuves de tests applicatifs.
2. Pour chaque action sélectionnée, préciser responsable, fenêtre, cible exacte,
   prérequis, critères d’arrêt et état initial à conserver.
3. Rechercher les commandes adaptées aux versions réellement installées et
   tester les migrations dans un environnement séparé avec données fictives.
4. Appliquer une action ou un lot cohérent, puis vérifier son effet de sécurité
   et le fonctionnement du service avant de poursuivre.
5. Si un critère échoue, arrêter le lot et utiliser le retour arrière prévu.
6. Compléter le [journal des changements](../dossier-preuves.md#journal-des-changements)
   avec résultat, date, preuves et risque résiduel.

| Preuve à conserver | Contenu attendu |
| --- | --- |
| Avant modification | Constat, cible, date, versions/configuration pertinente et résultat du test initial |
| Changement | Objets modifiés et paramètres choisis, sans secret ; identité de l’image/version si remplacée |
| Après modification — sécurité | Refus ou réduction du défaut ciblé ; résultat du scan pertinent et limites |
| Après modification — fonctionnement | Parcours applicatif ou accès d’administration réellement réussi |
| Retour arrière | Méthode préparée et restauration testée quand nécessaire ; préciser si le retour a réellement été exécuté |

Pour R09, conserver la capture avant changement et celle du refus des anciens
identifiants après changement, puis la preuve du nouvel accès **sans afficher
le nouveau mot de passe**. Les captures doivent être datées et rattachées à
leur constat, pas seulement montrer un écran de connexion.

## État final attendu

Une sélection ordonnée et justifiée d’actions, chacune reliée au constat, à la
modification envisagée, au bénéfice de sécurité, aux composants, aux impacts,
aux deux validations et au retour arrière. La préparation est complète lorsque
ces éléments sont renseignés ; une action ne sera clôturée qu’après une mise
en œuvre et des preuves de validation réelles.

## 📚 Notions acquises — Plan de remédiation

Un **plan de remédiation** transforme les constats qualifiés en actions
priorisées. La préparation précise comment changer sans perdre le service,
comment démontrer le bénéfice et comment revenir à un état maîtrisé. Un
correctif proposé, un correctif appliqué et un correctif validé sont trois
états distincts.

- [Rapport et plan du J3](../it-3/finaliser-rapport-plan-remediation.md)
- [Priorisation contextualisée](../it-3/evaluer-risques-definir-priorites.md)
- [Dossier de preuves et journal](../dossier-preuves.md)
- [Activité suivante — Mettre en œuvre et vérifier les remédiations](mettre-en-oeuvre-verifier-remediations.md)
- [Retour à l’itération 4](index.md)
- [Retour au module](../README.md)

## Suivi R09 — Retour du 2 octobre 2026

Olivier confirme le **changement du mot de passe administrateur** et le
**refus de l’ancien mot de passe, y compris en navigation privée**. R09 est
appliquée selon ce retour ; le nouvel accès, le test fonctionnel et les
captures restent à confirmer avant clôture complète. Les mentions « à
effectuer » dans la préparation décrivent l’état avant ce retour.

[Résultat détaillé et limites](mettre-en-oeuvre-verifier-remediations.md#r09-mot-de-passe-administrateur-change-retour-du-2-octobre-2026).

## Ordre révisé par Olivier — File Browser avant Ubuntu

**Décision du 2 octobre 2026 :** commencer par **R03**, avec persistance
des données applicatives et reprise automatique **R08**, puis réaliser
**R01 — Ubuntu**. R09 a déjà été appliquée selon le retour utilisateur ;
son test fonctionnel reste à confirmer. Cet ordre remplace la séquence
prévisionnelle du tableau initial. Aucune migration n’est encore démontrée.

1. Localiser et sauvegarder les documents, la base et la configuration actuels.
2. Préparer la nouvelle image et tester la compatibilité avec une copie cohérente
   des données, en conservant un retour à l’image et à la base initiales.
3. Déployer des montages persistants pour les chemins réellement utilisés
   et conserver comptes, paramètres et nouveau mot de passe.
4. Retenir `unless-stopped` pour la reprise Docker ; confirmer que Docker
   est activé au démarrage. Un arrêt manuel reste respecté par cette politique.
5. Vérifier version/image, authentification, droits, fichiers et persistance
   après recréation ; tester ensuite la reprise après redémarrage de la VM
   depuis un conteneur en fonctionnement, sans arrêt manuel préalable.
6. Réaliser les contrôles Trivy et documenter les risques résiduels, puis
   passer à la migration Ubuntu.

Le montage `/srv/filebrowser` vers `/srv` conserve déjà les documents. Aucun
montage de base ou configuration n’apparaît dans l’inspection reçue : localiser
ces fichiers avant de supprimer ou recréer le conteneur. Activer une politique
de redémarrage ne rend pas les fichiers de sa couche modifiable persistants
après recréation.
