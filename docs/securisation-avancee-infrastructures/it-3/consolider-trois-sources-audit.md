# Consolider les trois sources d’audit

**Date de consolidation : 1er octobre 2026**

## Objectif

Intégrer l’analyse Trivy au tableau d’audit construit avec Greenbone, Lynis et
les vérifications manuelles, sans transformer chaque résultat d’outil en un
constat indépendant.

**Statut : consolidation documentaire réalisée.** Aucun changement de
configuration ni nouveau plan de remédiation définitif n’est présenté comme
appliqué.

## Sources utilisées

| Code | Source | Apport principal | Limite |
| --- | --- | --- | --- |
| **GB** | [Premier audit Greenbone](../it-1/premier-audit-greenbone.md) | Vue distante et authentifiée de la VM, services, paquets Ubuntu et avis associés | Ne fournit pas l’inventaire complet de l’image File Browser |
| **LY** | [Audit et analyse Lynis](../it-2/analyser-prioriser-resultats-lynis.md) | Configuration locale de la VM, services, journalisation, noyau et recommandations de durcissement | Lynis 2.6.2 audite l’hôte et n’a pas été exécuté dans le conteneur |
| **TR** | [Analyse de l’image avec Trivy](analyser-image-trivy.md) | 20 paquets Alpine, 53 composants Go et 294 associations composant–vulnérabilité | Détection fondée sur la présence et la version ; n’établit pas seule l’atteignabilité |
| **VM** | [Vérifications manuelles](../it-2/verifier-configuration-systeme.md) et contrôles du conteneur | Versions, services, écoutes, droits, configuration SSH, exécution root et montage `/srv` | Observations ponctuelles ; aucune exploitation réalisée |
| **CVE** | [Vérification de cinq résultats Trivy](analyser-verifier-resultats-trivy.md) | Conditions d’exploitation, versions affectées, corrections et applicabilité | Une analyse statique ne remplace pas une analyse complète des chemins d’appel |

La cible reste la VM Ubuntu 20.04.6 LTS qui héberge le conteneur
`filebrowser/filebrowser:v2.15.0`. Le service répondait en HTTP/1.1 sur
`192.168.122.229:8080` lors du dernier contrôle. L’exposition à Internet est le
contexte du cas pédagogique ; seule la joignabilité depuis la machine d’audit a
été démontrée dans le laboratoire.

## Méthode de regroupement

- Un constat décrit un **problème réel à traiter**, pas une ligne de scanner.
- Les résultats portant sur une même cause sont regroupés lorsqu’ils conduisent
  à la même décision.
- Une version affectée est distinguée d’une vulnérabilité effectivement
  atteignable.
- Les résultats non pertinents sont retirés du tableau actif, mais conservés
  avec la preuve et la justification de leur exclusion.
- **Confirmé** qualifie l’état ou le défaut observé ; il ne signifie pas qu’une
  exploitation a été reproduite.

## Tableau d’audit consolidé

Les constats C01 à C10 proviennent du tableau J2. Trivy ajoute le constat C12 sur
le cycle de vie de l’image. L’ancien C11, relatif à l’arrêt volontaire de la VM,
est déplacé dans le registre des décisions non pertinentes.

| Constat | Source(s) | Éléments observés | Vérifications effectuées | Statut | Risque dans le contexte du serveur | Action envisagée | Justification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **C01 — Correctifs containerd manquants sur l’hôte** | GB G01, VM | `containerd 1.7.24-0ubuntu1~20.04.2`, service actif et utilisé par Docker | Scan authentifié, `dpkg-query`, `apt-cache policy`, services, socket et écoute locale | **Confirmé** pour l’écart de version ; fonctions vulnérables **à vérifier** | Atteinte possible au moteur de conteneurs ou à la disponibilité selon les fonctions et accès requis | Préparer la mise à jour ou la migration de l’hôte et tester Docker/File Browser après maintenance | Le composant est réellement utilisé ; son socket restreint et l’absence d’exposition réseau directe réduisent certains scénarios sans corriger le paquet |
| **C02 — Correctifs Docker/BuildKit manquants** | GB G02, VM | Docker `26.1.3-0ubuntu1~20.04.1`, socket `root:docker 660` | Scan authentifié, versions APT, permissions et groupe Docker | **Confirmé** pour l’écart ; usage de BuildKit **à vérifier** | Accès indu à des fichiers pendant une construction si les conditions de l’avis sont réunies | Mettre à jour ou migrer ; inventorier les constructions, utilisateurs et contextes avant intervention | La présence de Docker est confirmée, mais aucun scénario BuildKit malveillant n’est démontré |
| **C03 — OpenSSH ancien sur un service d’administration joignable** | GB G03, VM | OpenSSH `1:8.2p1-4ubuntu0.13`, TCP 22 joignable ; GSSAPI désactivé | Scan authentifié, version locale, `sshd -T`, test réseau | **Confirmé** pour l’écart ; CVE individuellement **à vérifier** | Compromission ou indisponibilité de l’accès d’administration selon la CVE et les options actives | Préparer une version maintenue, conserver un accès de secours et retester l’authentification par clé | Le service a un rôle essentiel et est joignable ; GSSAPI désactivé écarte seulement les scénarios qui l’exigent |
| **C04 — Configuration SSH permissive** | LY `SSH-7408`, VM | Mot de passe accepté, root possible par clé, six essais, transferts TCP/agent et X11 autorisés | `sshd -t`, `sshd -T`, lecture des fragments ; compte `gvm-audit` sans sudo | **Confirmé** ; besoins de transfert **à vérifier** | Facilite les tentatives et le rebond après compromission d’un compte ou d’une clé | Préparer les restrictions déjà documentées, puis valider les usages et une session de secours avant application | Défaut de configuration distinct de la version du paquet ; les droits corrects de la clé d’audit constituent une mesure atténuante limitée |
| **C05 — MAC SSH de 64 bits proposés** | GB G05, VM | `umac-64-etm@openssh.com` et `umac-64@openssh.com` dans la configuration effective | Détection distante et confirmation par `sshd -T` | **Confirmé** pour l’offre ; négociation réelle non mesurée | Un client compatible peut négocier un mécanisme classé faible par Greenbone | Préparer leur retrait après inventaire et test des clients SSH | Le constat est confirmé par deux méthodes et demande une correction cryptographique dédiée |
| **C06 — CUPS ancien et sans rôle métier identifié** | GB G04, LY `PRNT-2307/2308`, VM | CUPS `2.3.1-9ubuntu1.9`, service/socket actifs, écoute limitée à localhost, aucune imprimante | Versions, unités, `ss`, `lpstat`, configuration et permissions | **Confirmé** ; dépendances **à vérifier** | Surface d’attaque locale inutile ; le scénario d’attaque distante directe n’est pas observé | Valider l’absence de besoin puis désactiver les unités ; si le service reste, le mettre à jour | Les constats paquet, service inutile et configuration décrivent le même service et sont regroupés |
| **C07 — Maintenance Ubuntu/ESM non assurée** | GB G01–G04, VM | Ubuntu 20.04 non rattachée à Pro ; correctifs ESM non disponibles dans l’état relevé | `pro status`, versions et candidats APT | **Confirmé** pour le non-rattachement ; fraîcheur des index **à vérifier** | Plusieurs écarts de sécurité persistent sur l’hôte et peuvent s’accumuler | Décider entre accès aux correctifs applicables et migration vers une version maintenue | Cause de gestion commune aux écarts de paquets de l’hôte ; elle ne constitue pas une CVE supplémentaire |
| **C08 — Audit système spécialisé absent** | LY `ACCT-9628`, VM | `auditd` et `audispd-plugins` absents ; journald et rsyslog actifs | Paquets, unités, volume des journaux et recherche de configuration | **Confirmé** pour l’absence ; règles et rétention **à vérifier** | Chronologie moins précise pour les actions sensibles lors d’un incident | Étudier l’installation d’auditd, des règles ciblées et la rétention avant l’intégration Wazuh | Les journaux existants empêchent de conclure à une absence totale de traces, mais ne remplacent pas un audit ciblé |
| **C09 — Paramètres noyau à adapter au rôle** | LY `KRNL-6000`, VM | Forwarding IPv4, restrictions dmesg, core dumps, `rp_filter`, redirects et SysRq relevés | `sysctl` et recherche de leur persistance | **À vérifier** | Une valeur trop permissive peut exposer des informations ou modifier le comportement réseau ; une modification aveugle peut casser Docker | Déterminer les besoins Docker et réseau, puis retenir uniquement les changements compatibles | Lynis signale un écart de profil ; le contexte fonctionnel manque pour qualifier toutes les valeurs comme défauts |
| **C10 — File Browser exécuté en root avec montage documentaire RW** | VM, TR | PID 1 UID/GID 0, `NoNewPrivs=0`, capacités actives, montage `/srv/filebrowser:/srv` en lecture-écriture ; conteneur non privilégié | `docker inspect`, `/proc/1/status`, permissions et montages ; analyse de l’image exacte | **Confirmé** | Une compromission applicative aurait accès aux documents montés avec les droits du processus et pourrait amplifier les conséquences sur confidentialité et intégrité | Étudier un UID non privilégié, réduire les capacités et tester les droits sur des données fictives avant changement | Le risque de configuration est indépendant de l’applicabilité des cinq CVE étudiées ; l’image ancienne augmente toutefois la probabilité d’un défaut exploitable non encore qualifié |
| **C12 — Image File Browser obsolète et hors support** | TR, VM, CVE | File Browser `2.15.0`, Alpine `3.13.4` avec `EOSL=true`, Go `1.16.2`, 20 paquets Alpine, 53 composants Go et 294 associations dont 13 `CRITICAL` | ImageID et empreintes contrôlés ; scan Trivy 0.74.0 ; cinq résultats vérifiés dans les entrées CVE, le code, le binaire et le réseau | **Confirmé** pour l’obsolescence et la fin de support ; CVE-2022-23806 **à vérifier** | Le service échange des documents et utilise une chaîne logicielle figée qui ne reçoit plus de corrections ; l’exécution root et le montage RW augmentent l’impact potentiel | Évaluer une image File Browser maintenue, tester la migration des données et de la configuration, rescanner la nouvelle image et réaliser des tests fonctionnels | Les 294 lignes ne deviennent pas 294 constats. Quatre CVE étudiées sont non pertinentes ici, mais l’accumulation, l’EOL et une condition encore ouverte justifient un constat structurel unique |

## Apport propre de chaque source

| Question | Réponse consolidée |
| --- | --- |
| Que voit Greenbone ? | L’exposition réseau de la VM et, avec le compte SSH, plusieurs versions de paquets Ubuntu. Il ne décrit pas complètement les composants intégrés au binaire File Browser |
| Que voit Lynis ? | La configuration locale et le durcissement de l’hôte : SSH, services, noyau, journalisation et permissions. Il n’analyse pas l’image comme un inventaire de composants |
| Que voit Trivy ? | Les paquets Alpine et dépendances Go de l’image exacte. Il n’établit pas automatiquement que File Browser appelle le symbole vulnérable dans les conditions de la CVE |
| Que prouvent les contrôles manuels ? | Les valeurs effectives, les écoutes, l’exécution root, le montage RW, le protocole HTTP/1.1 et le caractère statique du binaire |
| À quoi servent les sources CVE ? | À vérifier les versions, les fonctions nécessaires, les impacts et les corrections afin de passer d’une correspondance de version à une décision d’applicabilité |

## Registre des résultats écartés

Ces éléments ne figurent pas comme risques actifs dans le tableau final, mais la
décision reste traçable.

| Résultat écarté | Source(s) | Décision | Justification conservée |
| --- | --- | --- | --- |
| CVE-2020-26160, contournement d’audience JWT | TR, CVE, code File Browser | **Non pertinent** | File Browser utilise `StandardClaims`, ne renseigne pas `Audience` et n’appelle pas `MapClaims.VerifyAudience`, fonction nécessaire au scénario |
| CVE-2021-44716, consommation mémoire HTTP/2 | TR, CVE, code, test réseau | **Non pertinent dans la configuration observée** | Le point d’entrée répond en HTTP/1.1 et refuse le test HTTP/2 direct ; aucun `h2c` ou serveur HTTP/2 explicite n’est configuré |
| CVE-2021-3711, déchiffrement SM2 OpenSSL | TR, CVE, analyse ELF | **Non pertinent pour le processus exposé** | `/filebrowser` est statique et ne charge pas `libssl`/`libcrypto` ; aucun appel SM2 `EVP_PKEY_decrypt` n’est démontré |
| CVE-2022-37434, dépassement zlib | TR, CVE, analyse ELF et code | **Non pertinent pour le processus exposé** | Le binaire ne charge pas la zlib Alpine et le code serveur n’appelle pas `inflateGetHeader` |
| C11, arrêt de File Browser après arrêt de la VM | Journaux VM et déclaration de l’utilisateur | **Non pertinent comme panne spontanée** | L’arrêt de la VM était volontaire et les journaux concordent ; la politique de reprise reste un besoin de disponibilité séparé |
| CUPS directement exposé sur le réseau | GB, LY, VM | **Non pertinent dans l’état observé** | CUPS écoute uniquement sur les boucles locale IPv4 et IPv6 |
| Absence totale de journalisation | LY, VM | **Non pertinent** | journald et rsyslog sont actifs ; le constat conservé C08 porte sur l’absence d’audit spécialisé |

## Points encore ouverts

1. Déterminer si un chemin d’entrée contrôlable atteint
   `crypto/elliptic.(*CurveParams).IsOnCurve` pour CVE-2022-23806. Une analyse
   de graphe d’appels avec un outil adapté reste nécessaire.
2. Prouver ou écarter l’exposition réelle à Internet, distincte de la
   joignabilité depuis la machine d’audit.
3. Vérifier les dépendances avant de désactiver CUPS ou les fonctions SSH.
4. Définir la version cible de File Browser et tester la compatibilité des
   données, de la base et de la configuration avant migration.
5. Réaliser un nouveau scan Greenbone, Lynis et Trivy après les corrections afin
   de comparer les preuves avant/après.

## Conclusion

Trivy complète l’audit sans remplacer Greenbone ni Lynis. Le principal apport
n’est pas une liste supplémentaire de 294 problèmes : c’est la confirmation que
l’application repose sur une image hors support et une chaîne Go ancienne. Les
vérifications CVE réduisent le bruit en écartant quatre scénarios, tout en
conservant une condition cryptographique ouverte.

Le tableau final compte donc un nouveau constat structurel, C12, et enrichit C10
sur les conséquences d’une compromission du conteneur. Les décisions écartées
restent auditables dans le registre ci-dessus.

- [Activité précédente — Analyser et vérifier les résultats Trivy](analyser-verifier-resultats-trivy.md)
- [Retour à l’itération 3](index.md)
- [Tableau consolidé J2](../it-2/consolider-resultats-greenbone-lynis.md)
- [Dossier de preuves](../dossier-preuves.md)
