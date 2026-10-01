# Identifier ce qui manque dans l’audit

## Objectif

Déterminer quelles informations sur le conteneur File Browser ne sont pas encore
couvertes par l’audit consolidé du J2, avant toute analyse avec Trivy.

**Statut au 1er octobre 2026 : analyse des limites réalisée à partir des preuves
du J2.** L’image et sa configuration d’exécution sont identifiées. Les composants
logiciels internes, leurs versions complètes et leurs vulnérabilités applicables
restent à établir par un scanner d’image.

## Outils déjà utilisés et portée réelle

| Source | Ce qu’elle a observé | Ce qu’elle ne démontre pas sur l’image |
| --- | --- | --- |
| Greenbone sans authentification | Services et ports accessibles depuis le réseau | Contenu des couches, paquets internes et dépendances du binaire |
| Greenbone avec le compte SSH `gvm-audit` | Paquets et configuration lisibles sur la VM Ubuntu | Inventaire authentifié de l’environnement Alpine interne |
| Lynis sur la VM | Comptes, SSH, services, noyau, journaux, paquets Ubuntu et présence de Docker | Analyse des composants de l’image File Browser ; Lynis n’est pas exécuté dans le conteneur |
| Vérifications manuelles | État Docker, image référencée, montages, ports, utilisateur, permissions et quelques fichiers internes | Correspondance exhaustive entre composants, versions et vulnérabilités connues |

Ces outils apportent des vues complémentaires. Leur absence de constat propre à
File Browser ne constitue pas une preuve d’absence de vulnérabilité.

## Ce qui est déjà connu

### Image et application

| Information | Valeur observée | Portée de la preuve |
| --- | --- | --- |
| Référence | `filebrowser/filebrowser:v2.15.0` | Tag déclaré par le conteneur ; un tag peut être déplacé dans un registre |
| Version applicative | File Browser 2.15.0, révision déclarée `73ccbe912fc1848957d8b2f6bbe5243804769d85` | Version retournée par le binaire et label de l’image ; authenticité de la provenance non démontrée |
| ImageID | `sha256:a68f43720ea6ff331fa4b92becced20af14b72f4c3a22ca1f764076a8e42e1a5` | Identité exacte de l’image locale référencée par le conteneur |
| RepoDigest | `filebrowser/filebrowser@sha256:1595cf9b36528113a18178996d9ff9ee8bc7814699bb5f8e1d8ad8ec48aa89ac` | Digest de registre relevé localement, distinct de l’ImageID |
| Plateforme | `linux/amd64` | Métadonnée Docker de l’image |
| Création de l’image | 6 avril 2021 | Ancienneté établie ; ne prouve pas à elle seule une vulnérabilité |
| Environnement interne | Alpine Linux 3.13.4 | Relevé ponctuel de `/etc/os-release` dans le conteneur |

### Configuration d’exécution

| Information | Valeur observée | Conclusion limitée |
| --- | --- | --- |
| Processus principal | `/filebrowser`, UID/GID 0 | Application exécutée en root dans le conteneur ; aucun accès root à la VM démontré |
| Mode privilégié | `Privileged=false` | Le mode privilégié Docker n’est pas activé |
| Système de fichiers racine | `ReadonlyRootfs=false` | Couche modifiable pendant l’exécution |
| Seccomp | Mode 2, un filtre | Filtrage seccomp actif ; politique exacte non évaluée |
| `NoNewPrivs` | `0` | Protection `no-new-privileges` non activée pour le processus observé |
| Montage | `/srv/filebrowser -> /srv`, `RW=true` | Données de l’hôte accessibles en lecture-écriture selon les droits applicables |
| Port | Hôte 8080 vers conteneur 80/tcp | Publication configurée sur IPv4 et IPv6 lorsque le conteneur fonctionne |
| Redémarrage | `RestartPolicy=no` | Pas de reprise automatique configurée |

Ces informations décrivent l’exécution. Elles ne donnent pas la liste complète
des fichiers et bibliothèques incorporés dans l’image.

## Ce qui reste inconnu

| Question | Information manquante | Pourquoi elle est nécessaire |
| --- | --- | --- |
| Quels composants sont présents ? | Inventaire des paquets Alpine, bibliothèques, fichiers applicatifs et dépendances embarquées | Une vulnérabilité doit être reliée à un composant réellement présent |
| Quelles versions exactes ? | Version complète, révision du paquet, architecture et origine de chaque composant | Un même nom de paquet peut être corrigé par rétroportage sans changer de version amont |
| Le binaire est-il statique ? | Bibliothèques liées, modules intégrés et informations de compilation | Certaines dépendances ne figurent pas dans le gestionnaire de paquets |
| Quelles CVE sont associées ? | Correspondance entre composants détectés et base de vulnérabilités datée | Une CVE publiée ne suffit pas si le composant ou la condition n’est pas présent |
| Les correctifs sont-ils intégrés ? | Avis Alpine, éditeur File Browser et état de maintenance de l’image | Une comparaison de numéros seule peut produire des faux positifs |
| Les vulnérabilités sont-elles exploitables ? | Fonction concernée, configuration, entrée contrôlée, privilèges et exposition | La sévérité générique ne fixe pas la priorité dans ce serveur |
| Certains éléments sont-ils non détectés ? | Erreurs, fichiers ignorés, paquets inconnus, dépendances compilées ou supprimées des métadonnées | Le silence du scanner peut venir d’une limite de couverture |

## Pourquoi Greenbone ne suffit pas

Greenbone observe la cible depuis le réseau et, avec SSH, la VM Ubuntu selon les
droits du compte `gvm-audit`. Les exports étudiés montrent le port 8080, mais
n’identifient pas File Browser ni les composants Alpine de l’image. Un service
HTTP accessible ne révèle pas automatiquement les couches et dépendances qui le
composent.

## Pourquoi Lynis ne suffit pas

Lynis a été exécuté sur la VM conformément à la consigne de la formatrice. Il a
détecté Docker et évalué l’hôte, mais il n’a pas inventorié l’image. Le test
`CONT-8106` porte sur la cohérence de l’inventaire Docker, pas sur les CVE des
paquets internes. Lynis ne doit pas être installé ni exécuté dans File Browser.

## Pourquoi les vérifications manuelles ne suffisent pas

Les commandes Docker ont établi l’identité de l’image, ses montages, ses ports,
son utilisateur et quelques propriétés d’isolation. La lecture de
`/etc/os-release` a identifié Alpine 3.13.4. Ces contrôles ciblés ne construisent
pas une SBOM et ne rapprochent pas automatiquement chaque composant d’une base
de vulnérabilités.

Une collecte manuelle exhaustive serait difficile à reproduire et manquerait
les dépendances compilées, les fichiers ajoutés hors gestionnaire de paquets ou
les composants dont les métadonnées sont absentes.

## Informations à conserver avant le scan d’image

| Élément | Valeur ou action attendue |
| --- | --- |
| Objet | ImageID exact référencé par `filebrowser` |
| Référence | Tag et RepoDigest conservés séparément |
| Plateforme | `linux/amd64` |
| Outil | Version exacte de Trivy |
| Base | Date ou version de la base de vulnérabilités |
| Commande | Cible, scanners, sévérités, exclusions et format de sortie |
| Résultat | Rapport, heure, code de retour, erreurs et composants non reconnus |
| Intégrité | Empreinte SHA-256 du rapport conservé |

Ne pas télécharger silencieusement une image portant le même tag avant le scan :
elle pourrait différer de celle actuellement rattachée au conteneur. L’analyse
doit cibler l’objet identifié et documenter tout changement de digest.

## Conclusion

Le J2 décrit correctement l’hôte et plusieurs propriétés d’exécution de File
Browser. Il ne répond pas encore aux questions « quels composants ? », « quelles
versions ? » et « quelles vulnérabilités applicables ? ». Une analyse de l’image
exacte avec Trivy doit compléter ces preuves, puis chaque résultat devra être
qualifié avec l’avis de sécurité et le contexte du service.

- [Retour à l’itération 3](index.md)
- [Activité suivante — Analyser l’image avec Trivy](analyser-image-trivy.md)
- [Preuves préparatoires du J2](../it-2/limites-audit-preparer-analyse-conteneur.md)
- [Observation du conteneur sans Lynis](../it-2/etendre-audit-conteneur.md)
- [Dossier de preuves](../dossier-preuves.md)
