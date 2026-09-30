# Pense-bête — Sécurisation avancée : Auditer et prioriser

## Périmètre

Itération 1 de la progression prévisionnelle du module. Cette fiche rassemble
les notions, les gestes et les premiers résultats observés sur la VM cible.

## Environnement imposé

- **Hôte** : machine d'audit et installation de Greenbone Community Edition.
- **VM cible** : Ubuntu Server 20.04, 2 vCPU, 4 Go de RAM.
- **Application** : `filebrowser/filebrowser:v2.15.0`, conteneur `filebrowser`.
- **URL vérifiée depuis l'hôte** : `http://192.168.122.229:8080` ; relever de nouveau l'IP si le bail DHCP change.
- **Montage** : `/srv/filebrowser` sur la VM → `/srv` dans le conteneur.
- **Périmètre** : sa propre VM, jamais les machines des autres apprenants.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Greenbone Community Edition / OpenVAS | Plateforme d'audit de vulnérabilités et son composant de scan. |
| Lynis | Outil d'audit local de configuration et de durcissement du système. |
| Trivy | Outil d'analyse d'artefacts : images, fichiers ou dépôts selon la cible choisie. |
| CVE | Identifiant d'une vulnérabilité connue ; sa présence dans un rapport reste à qualifier. |
| CVSS | Mesure de sévérité technique, à compléter par le contexte pour prioriser. |
| Exploitabilité | Conditions nécessaires pour exploiter un défaut dans le contexte étudié. |
| Faux positif | Signalement qui ne correspond pas à un problème applicable à la cible. |
| Feed | Données de tests ou de vulnérabilités mises à jour pour l'outil. |
| Bind mount | Montage d'un répertoire de la VM dans le conteneur. |
| `8080:80` | Port 8080 de la VM redirigé vers le port 80 du conteneur. |
| Digest d'image | Référence de contenu permettant d'identifier l'image récupérée. |

## Manipulations faites

Contrôle initial réalisé par l'apprenant, d'après les sorties de terminal fournies :

- `/etc/os-release` : Ubuntu **20.04.6 LTS**, Focal Fossa ;
- `nproc` : **2** processeurs disponibles ;
- `free -h` : **3,8 GiB** de mémoire visible ;
- `ip -br address` : `enp1s0` UP, **`192.168.122.229/24`** ;
- `ip route` : passerelle par défaut **`192.168.122.1`**, route fournie par DHCP.

Contrôle de l'hôte réalisé par l'apprenant, d'après les nouvelles sorties fournies :

- Ubuntu **26.04.1 LTS**, Resolute Raccoon ;
- Docker **29.1.3**, client et serveur accessibles ;
- Docker Compose **v5.5.1**, plugin reconnu ;
- **20** processeurs logiques vus par Docker, **19 GiB** de mémoire disponible ;
- **80 Go** de disque libre, partagés entre le dossier personnel et `/var/lib/docker` ;
- **0 conteneur** dans le contexte Docker `default` au moment du contrôle.

Captures du **30 septembre 2026** fournies par l'apprenant :

- image `filebrowser/filebrowser:v2.15.0` téléchargée, digest conservé dans la fiche détaillée ;
- conteneur `filebrowser` créé et `Up (healthy)`, binaire `v2.15.0/73ccbe91` ;
- montage `/srv/filebrowser -> /srv` confirmé par `docker inspect` ;
- dossiers `interne`, `partenaires` et `public` visibles ; sous-dossiers des partenaires à documenter ;
- **HTTP 200** dans la VM sur `127.0.0.1:8080` ;
- depuis l'hôte, ping vers `192.168.122.229` réussi (3/3) et **HTTP 200** sur le port 8080 ;
- page de connexion File Browser affichée, sans preuve d'authentification.

Le nouveau relevé local du **30 septembre 2026**, repéré à **11:51:09 +02:00**,
complète ces preuves dans la [fiche d'observation](../../../securisation-avancee-infrastructures/it-1/observer-cible.md) :

- IP `192.168.122.229/24` confirmée, noyau **5.15.0-139-generic** ;
- Docker **26.1.3** côté client et serveur de la VM, containerd **1.7.24** ;
- un conteneur en fonctionnement listé : `filebrowser`, **healthy**, version **2.15.0/73ccbe91** ;
- SSH écoute sur **TCP 22** en IPv4 et IPv6 ; accès TCP IPv4 depuis l'hôte confirmé dans le relevé suivant, version OpenSSH à vérifier ;
- File Browser publié sur **TCP 8080** en IPv4 et IPv6 ; accès HTTP IPv4 déjà prouvé lors de la préparation ;
- DNS local sur **53**, CUPS en boucle locale sur **631**, socket containerd local sur **37517** ;
- Avahi sur UDP **5353**, plus deux sockets UDP **36609/35745** au moment du relevé ;
- **34 services actifs**, dont `gdm`, `cups` et `avahi-daemon` : utilité des composants de bureau, d'impression et de découverte à justifier.

Le relevé depuis **`ubuntu-oliv`**, repéré à **11:53:01 +02:00**, complète les
écoutes locales :

- route vers `192.168.122.229` via **`virbr0`**, source **`192.168.122.1`** ;
- ping **3/3**, aucune perte, RTT moyen **0,268 ms** ;
- `nc` disponible dans `/usr/bin/nc`, connexions TCP **22 et 8080 réussies** ;
- `curl` sur `http://192.168.122.229:8080/` : **HTTP 200**.

L'accès TCP à SSH est confirmé, pas une authentification. Ces tests IPv4 depuis
l'hôte ne prouvent pas une exposition Internet ni l'accessibilité IPv6 ou UDP.
Aucun changement de service n'est documenté dans ces relevés.

La capture de validation Compose de 09:49:40 provient de la **VM**,
alors que le déploiement Greenbone attendu est sur l'**hôte**. La capture
`ps -a` de 10:06:09 confirme ensuite les conteneurs sur `ubuntu-oliv`.

Erreur rapportée pendant la préparation de Greenbone :
`docker compose -p ais-greenbone config --services` avait renvoyé
`unknown shorthand flag: 'p' in -p`. L'apprenant a ensuite confirmé l'absence de
Compose dans le terminal utilisé. Le dernier contrôle sur l'hôte montre désormais
Compose v5.5.1 opérationnel. Le déploiement a ensuite atteint le démarrage des
conteneurs, avec le conflit de port décrit ci-dessous.

**Conflit de port Greenbone corrigé par l'assistant :**

- erreur rapportée : `127.0.0.1:443/tcp: address already in use` ;
- sauvegarde du fichier Compose puis remplacement par `127.0.0.1:8443:443` ;
- fichier Compose validé et seul Nginx recréé, en conservant le service sur 443 ;
- Nginx `Up`, accès à **`https://127.0.0.1:8443/`** vérifié : **HTTP 200**, titre `OPENVAS`.

La capture du tableau de bord montre une session Greenbone ouverte et une
**synchronisation des feeds en cours**, avec les scans indisponibles pendant
cette phase. Les conteneurs sont démarrés sur l'hôte. La fin de l'import, la
disponibilité du scanner n'étaient pas établies par cette capture. Les exports
de tâches fournis ensuite confirment deux scans terminés, comme détaillé plus bas.
Le changement du mot de passe initial reste non documenté.

## Exercice de qualification réalisé

Les quatre classements proposés par l'apprenant dans
[Vulnérabilité ou autre problème ?](../../../securisation-avancee-infrastructures/it-1/vulnerabilite-ou-autre-probleme.md)
sont corrects ; les justifications ont été précisées avec l'assistant :

| Situation | Classement | Nuance à retenir |
| --- | --- | --- |
| SSH direct de `root` par mot de passe | Défaut de configuration | L'énoncé ne dit pas « sans mot de passe » ; prévoir un autre accès administrateur avant modification |
| Bibliothèque concernée par une CVE | Vulnérabilité logicielle | Vérifier la version exacte et les conditions d'exploitation |
| Version publiée il y a quatre ans | Version ancienne sans vulnérabilité démontrée | L'âge seul ne prouve pas une faille ; vérifier support et correctifs |
| Administration exposée sur Internet sans besoin externe décrit | Service inutilement exposé | Confirmer le besoin réel et les possibilités d'accès restreint |

Ces situations sont pédagogiques et ne constituent pas des résultats de scan
de la VM du laboratoire.

## Lire une CVE — synthèse documentaire

La [fiche des trois CVE](../../../securisation-avancee-infrastructures/it-1/lire-analyser-entrees-cve.md)
réunit les sources vérifiées par l'assistant :

- **Debian OpenSSL, CVE-2008-0166** : corriger la génération aléatoire puis remplacer les clés faibles.
- **Heartbleed, CVE-2014-0160** : arrêter la fuite mémoire puis traiter les secrets potentiellement exposés.
- **Log4Shell, CVE-2021-44228** : corriger la dépendance et rechercher une éventuelle compromission antérieure.

Lire la description, les versions et les références ensemble : des champs
`n/a` ou des formulations divergentes nécessitent un recoupement avec l'avis
de l'éditeur. **Un correctif ne supprime pas nécessairement les conséquences
antérieures.** Cette recherche documentaire ne prouve aucune de ces failles
sur la VM File Browser.

## CVSS — sévérité et priorité

La [fiche Comprendre CVSS](../../../securisation-avancee-infrastructures/it-1/comprendre-cvss.md)
documente les évaluations NVD consultées : **7,5 / 7,5 / 10,0 en CVSS 3.1**
pour Debian OpenSSL, Heartbleed et Log4Shell respectivement.

- Conserver la **version**, le score, le vecteur, la source et la date ensemble.
- `AV`, `AC`, `PR`, `UI` décrivent les conditions d'attaque ; `C`, `I`, `A` les impacts en v3.1.
- Utiliser le calculateur correspondant au vecteur ; un vecteur 3.1 ne devient pas 4.0 en changeant son préfixe.
- Le score de base ne fixe pas seul la priorité : examiner notamment l'exposition réelle et la criticité métier.

La recherche est documentaire ; l'utilisation du calculateur par l'apprenant
reste à illustrer par une capture.

## Gestes et commandes à retenir

- Pour [observer la cible](../../../securisation-avancee-infrastructures/it-1/observer-cible.md), réutiliser `ip`, `/etc/os-release`, `ss`, `systemctl` et les commandes Docker dans la VM, puis `ping`, `nc` et `curl` depuis l'hôte.
- Croiser écoute locale, publication Docker et accès distant ; ces trois observations ne prouvent pas la même chose.
- Associer chaque service à sa version et à son rôle ; noter « à investiguer » si le rôle est inconnu.
- L'inventaire local et l'accès distant TCP 22/8080 sont documentés ; compléter la version OpenSSH et le rôle des services supplémentaires.
- Dans la VM : contrôler Docker, créer les répertoires puis utiliser exactement l'image historique demandée.
- Vérifier `sudo docker ps -a`, `sudo docker logs --tail 50 filebrowser` et le montage de `/srv` ; relire les logs avant diffusion.
- Depuis l'hôte : tester l'URL avec l'IP de la VM ; `localhost:8080` désignerait l'hôte lui-même.
- Sur l'hôte : valider le fichier Greenbone avec `docker compose -f CHEMIN/compose.yaml config --quiet` avant `pull` puis `up -d`.
- Si `-p` est refusé : vérifier `hostname` et `docker compose version` dans le même terminal avant de modifier les commandes ou d'installer un paquet.
- Pour l'interface Greenbone de ce laboratoire, ouvrir `https://127.0.0.1:8443` sur l'hôte.
- Distinguer images téléchargées, conteneurs démarrés et feeds réellement chargés.
- Relever la cible, le point d'observation, le profil, les versions et la date des bases.
- Conserver les rapports initiaux avant les corrections.
- Identifier l'artefact réellement analysé par Trivy : digest ou révision.
- Regrouper les doublons et vérifier l'applicabilité de chaque constat.
- Justifier la priorité par l'exposition, les prérequis d'exploitation et l'impact métier.

## Preuves attendues

Rapports contextualisés, registre de constats qualifiés et ordre de traitement justifié.

Pour le [premier audit Greenbone](../../../securisation-avancee-infrastructures/it-1/premier-audit-greenbone.md),
les exports de tâches et de rapports prouvent les éléments suivants :

- A : `A192.168.122.229`, **Done**, 12:02:19–12:17:33 (UTC+02:00), durée **15 min 14 s**, compteur de tâche **17**, sévérité du résumé **2,6** ;
- B : `AIS-B-Full-and-fast-SSH`, **Done**, 12:13:19–12:29:37, durée **16 min 18 s**, compteur de tâche **240**, sévérité du résumé **9,9** ;
- les deux utilisent **Full and fast** et **OpenVAS Default**, avec un chevauchement de **4 min 14 s** ;
- les rapports détaillés utilisent le même feed `202609300604` et contiennent **3 résultats dans A contre 200 dans B**, hors niveaux Log filtrés ;
- la somme des catégories diffère d'une unité du total de tâche pour chaque export : écart à éclaircir, sans additionner les anciens champs dupliqués ;
- B contient `Auth-SSH-Success` pour `gvm-audit` sur le port 22 et des contrôles locaux de paquets avec une QoD de **97 %** ;
- le format Anonymous XML remplace l'adresse réelle par `127.0.0.1` ; cette valeur ne désigne pas la cible réellement scannée ;
- cinq constats sont qualifiés : containerd, Docker/BuildKit, OpenSSH, CUPS et MAC SSH faible.

Les mises à jour manquantes sont confirmées par inventaire authentifié et avis
Ubuntu. Les conditions d'exploitation restent à vérifier CVE par CVE, ainsi que
l'utilité et l'exposition de CUPS et le nom exact du MAC SSH faible.

Rappels de procédure :

- vérifier le chargement des feeds, le scanner et **Full and fast** ;
- cibler uniquement la VM, conserver la même liste de ports pour les scans A et B ;
- réaliser A sans identifiant puis B avec un compte SSH dédié sans droits administrateur ;
- installer la clé **publique** sur la VM, importer la clé **privée** dans le credential Greenbone et l'associer à la cible ;
- vérifier l'authentification dans B, indépendamment de l'état **Done** ;
- qualifier cinq constats avec les références CVE et les statuts **Confirmé / À vérifier / Non pertinent**.

La réussite de l'usage du compte `gvm-audit` est attestée ; les commandes de
création du compte et de la clé ne le sont pas. La clé privée et sa phrase
secrète doivent rester hors des captures et du dépôt. Le plan de remédiation
définitif viendra ensuite.

## Docs associées

- [Préparer la cible et installer Greenbone](../../../securisation-avancee-infrastructures/it-1/preparer-cible-installer-greenbone.md)
- [Vulnérabilité ou autre problème ?](../../../securisation-avancee-infrastructures/it-1/vulnerabilite-ou-autre-probleme.md)
- [Lire et analyser trois entrées CVE](../../../securisation-avancee-infrastructures/it-1/lire-analyser-entrees-cve.md)
- [Comprendre CVSS](../../../securisation-avancee-infrastructures/it-1/comprendre-cvss.md)
- [Observer la cible](../../../securisation-avancee-infrastructures/it-1/observer-cible.md)
- [Premier audit avec Greenbone](../../../securisation-avancee-infrastructures/it-1/premier-audit-greenbone.md)
- [Feuille de l'itération 1](../../../securisation-avancee-infrastructures/it-1/index.md)
- [Dossier de preuves](../../../securisation-avancee-infrastructures/dossier-preuves.md)
- [Vue d'ensemble du module](../../../securisation-avancee-infrastructures/README.md)
