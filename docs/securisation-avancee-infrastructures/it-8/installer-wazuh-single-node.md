# Installer Wazuh en single-node

**Itération 8 — Travail en groupe**

## 🎯 Objectif et statut

Déployer la **single-node stack Docker officielle** de Wazuh et vérifier
son fonctionnement ainsi que l’accès au dashboard.
**Déploiement illustré par les captures du participant : composants 4.14.8,
processus du manager démarrés, indexer green et dashboard ouvert.**
La liste des participants du groupe reste à compléter. Cette feuille ne lance aucune
installation sur la machine du mémo.

Source à suivre pendant l’exercice :
[Wazuh — Single-node stack](https://documentation.wazuh.com/current/deployment-options/docker/wazuh-container.html#single-node-stack).
La documentation consultée le 8 octobre 2026 indique la référence `v4.14.8`.
Vérifier la référence prescrite au moment du déploiement et consigner le
commit effectivement utilisé ; conserver un ensemble cohérent de versions.

## 1. Organisation et déploiement attendu

Le déploiement retenu est une **VM dédiée sous Ubuntu Server 26.04**,
distincte de la VM File Browser. Docker Engine et Docker Compose seront
installés dans cette VM ; les trois composants Wazuh y fonctionneront en
conteneurs avec la stack single-node officielle. Suricata reste sur la
machine hôte. Ce choix décrit la cible, pas une installation déjà vérifiée.

Le groupe note l’adresse de la VM Wazuh, les participants et qui réalise
chaque opération. Le navigateur des postes du groupe accède au dashboard
sur l’adresse de cette VM. Son adresse et son raccordement réseau restent
à renseigner.

```text
 Navigateur du groupe
         | HTTPS : port publié du dashboard (443 par défaut)
 +-------v--------------------------------------------------+
 | VM Wazuh — Ubuntu Server 26.04 — Docker                    |
 |                                                          |
 | wazuh.dashboard ---> wazuh.indexer : 9200                  |
 |        |                     ^                            |
 |        +---> API manager     | Filebeat                   |
 |                 : 55000      |                            |
 |                       wazuh.manager                       |
 |                                                          |
 | Réseau Compose, volumes persistants et certificats        |
 +-----------------------------^----------------------------+
                               | futurs événements d’agents
```

| Composant central | Rôle |
| --- | --- |
| `wazuh.manager` | Réception et analyse des événements, règles, gestion des agents et API ; Filebeat assure l’envoi des alertes vers l’indexer dans cette stack |
| `wazuh.indexer` | Stockage, indexation et recherche des données |
| `wazuh.dashboard` | Interface web et accès aux données et fonctions Wazuh |

Le générateur de certificats est un outil ponctuel, pas un quatrième
composant central permanent. Single-node signifie ici un conteneur par
composant central. Reprendre les fichiers officiels du dossier `single-node`.

## 2. Prérequis dans la VM Wazuh

La documentation consultée demande au moins **4 cœurs, 8 Go de RAM et
50 Go de stockage** pour les images et volumes. Vérifier également
l’architecture compatible, Docker Engine, Compose et Git. Allouer les
ressources à la VM elle-même et vérifier que la machine physique conserve
assez de ressources pour les autres VM et Suricata. Les commandes de
préparation et de déploiement suivantes se lancent **dans la VM Wazuh**.

```bash
uname -m
nproc
free -h
df -h
docker version
docker compose version
git --version
sysctl vm.max_map_count
sudo ss -lntup
```

Si Docker nécessite des droits administrateur, utiliser `sudo docker` de
manière cohérente dans les commandes suivantes. Vérifier aussi l’espace du
stockage Docker si son emplacement diffère du répertoire de travail.

Sur la machine qui exécute Docker, appliquer le prérequis noyau officiel
si la valeur actuelle est inférieure à 262144 :

```bash
sudo sysctl -w vm.max_map_count=262144
sysctl vm.max_map_count
```

Cette modification est temporaire. Si le groupe conserve la plateforme
après redémarrage, documenter sa persistance via la configuration sysctl
locale et vérifier la valeur après redémarrage.

Les ports publiés par la stack officielle incluent 1514/TCP, 1515/TCP,
514/UDP, 55000/TCP, 9200/TCP et 443/TCP. Examiner les publications réelles
et les conflits avant démarrage. L’exposition des ports Docker doit être
vérifiée depuis les machines autorisées : le seul état du pare-feu hôte
ne démontre pas le filtrage des ports publiés, comme pour File Browser.
Ne pas exécuter simultanément les stacks single-node et multi-node sur
la même machine Docker.

## 3. Récupérer la stack et générer les certificats

Commandes à exécuter dans un répertoire de travail du groupe où
`wazuh-docker` n’existe pas déjà. Si un déploiement existe, examiner son état
avant de le modifier ou de réutiliser ses volumes.

```bash
git clone https://github.com/wazuh/wazuh-docker.git -b v4.14.8
cd wazuh-docker/single-node/
git rev-parse HEAD
docker compose config --quiet
docker compose config --services
```

Lire les fichiers fournis : images, volumes, ports, noms et configuration.
La sortie complète de `docker compose config` peut contenir des secrets ;
utiliser la validation silencieuse pour la preuve partageable.

Suivre l’option officielle de certificats auto-signés pour le laboratoire :

```bash
docker compose -f generate-indexer-certs.yml run --rm generator
ls -l config/wazuh_indexer_ssl_certs/
```

Vérifier la fin sans erreur et les fichiers attendus par les montages du
Compose. Ne pas copier les clés privées ou les secrets dans le mémo,
les captures ou Git. Si un proxy est nécessaire, appliquer la configuration
prévue dans la documentation officielle.

## 4. Démarrer et vérifier les composants

Depuis `wazuh-docker/single-node/` :

```bash
docker compose up -d
docker compose ps -a
docker compose images
docker compose logs --tail=100 wazuh.indexer
docker compose logs --tail=100 wazuh.manager
docker compose logs --tail=100 wazuh.dashboard
docker compose exec wazuh.manager /var/ossec/bin/wazuh-control status
```

Le premier démarrage nécessite une phase d’initialisation. Des messages
indiquant que l’indexer n’est pas encore joignable peuvent être transitoires.
Attendre sa disponibilité puis vérifier de nouveau ; s’ils persistent,
diagnostiquer leur cause. **Des conteneurs “Up” ne suffisent pas à prouver
que la plateforme est fonctionnelle.**

## 5. Accéder au dashboard et établir la preuve

Depuis le navigateur d’une machine du groupe, ouvrir
`https://ADRESSE_MACHINE_DOCKER` avec le port réellement publié si différent
de 443. Utiliser les informations d’authentification du déploiement officiel,
sans les inclure dans les preuves. La procédure officielle de
[changement des mots de passe](https://documentation.wazuh.com/current/deployment-options/docker/changing-default-password.html)
doit être suivie pour coordonner les identifiants entre composants.

Avec les certificats auto-signés, vérifier que l’adresse et le certificat
présentés correspondent au déploiement du groupe avant de poursuivre.
Après authentification, afficher une page Wazuh et vérifier la connexion
au manager ainsi que l’accès à l’indexer. L’absence d’agents est possible
à ce stade : l’inscription des agents et la collecte Suricata sont des
étapes distinctes, non prouvées par l’accès au dashboard.

Pour contrôler les services sans inscrire de secret dans une commande,
les contrôles suivants demandent le mot de passe interactivement.
Remplacer les valeurs d’exemple par l’adresse et l’utilisateur du groupe :

```bash
curl --cacert /CHEMIN/root-ca.pem -u UTILISATEUR_INDEXER \
  'https://NOM_INDEXER_PRESENT_DANS_CERTIFICAT:9200/_cluster/health?pretty'
```

Le nom doit être résolu vers la machine Docker et correspondre au certificat.
Si ce contrôle n’est pas réalisable depuis le poste, utiliser l’état de
l’indexer visible dans le dashboard et les journaux, en précisant la limite.
Un état `yellow` peut correspondre à des répliques non allouées sur un nœud
unique : l’expliquer ; un état `red` exige une investigation.

## 6. Diagnostiquer à partir des faits

| Symptôme | Vérifications | Suite à donner |
| --- | --- | --- |
| Conteneur arrêté ou redémarrages répétés | `docker compose ps -a`, logs du composant, mémoire et disque disponibles | Corriger la cause indiquée avant relance ; conserver l’erreur initiale |
| Indexer ne démarre pas | `vm.max_map_count`, ressources, droits des volumes, certificats et logs | Vérifier les prérequis et les montages officiels |
| Port déjà utilisé | `sudo ss -lntup`, autres publications Docker | Identifier le service en conflit ; documenter tout ajustement de port sans changer l’architecture |
| Dashboard “not ready” persistant | Logs dashboard et indexer, noms de services, réseau Compose et certificats | Distinguer initialisation normale et échec durable de connexion |
| Erreur d’authentification intercomposants | Identifiants configurés et procédure officielle de changement | Corriger leur cohérence sans publier les valeurs |
| Dashboard inaccessible depuis le poste | Adresse, routage, port publié, filtrage effectif Docker et logs | Comparer accès local et distant pour localiser la panne |
| Interface accessible mais manager indisponible | Logs manager/dashboard et configuration de l’API | Vérifier la connexion interne à 55000 et l’authentification API |

Pour examiner les réseaux et publications sans afficher les variables
contenant les mots de passe :

```bash
docker compose ps
docker network ls
```

Utiliser les noms de réseau et les identifiants de conteneur réellement
observés pour les inspections ciblées. Retirer secrets et données internes
des extraits de journaux partagés. Ne pas supprimer les volumes avec
`down -v` pour tenter de résoudre une panne : ils contiennent l’état persistant.

## 7. Captures du déploiement — 8 octobre 2026

![Prérequis de la VM Wazuh](../../assets/img/securisation-avancee-infrastructures/it-8/Capture%20d’écran%20du%202026-10-08%2013-56-58.png)

VM x86_64, quatre processeurs, 7,2 Gio visibles et racine 48 Go. À cet instant, vm.max_map_count vaut 1048576, au-dessus du minimum ; une sortie ultérieure montre 262144. Le client Docker sans sudo reçoit une erreur de permissions. Les valeurs sont des états successifs.

![Fichiers des certificats Wazuh](../../assets/img/securisation-avancee-infrastructures/it-8/Capture%20d’écran%20du%202026-10-08%2013-58-13.png)

Les fichiers attendus sont présents ; seuls leurs noms et permissions sont montrés, aucun contenu de clé privée.

![Images Wazuh et initialisation de l’indexer](../../assets/img/securisation-avancee-infrastructures/it-8/Capture%20d’écran%20du%202026-10-08%2014-01-39.png)

Trois images centrales 4.14.8 sont listées. Le journal montre une transition de l’indexer vers GREEN. La première commande ps sans sudo échoue : cette capture ne constitue pas une liste des états des trois conteneurs.

![Processus du manager Wazuh](../../assets/img/securisation-avancee-infrastructures/it-8/Capture%20d’écran%20du%202026-10-08%2014-01-51.png)

Les processus essentiels et l’API sont running. Les fonctions non démarrées ne constituent pas à elles seules une panne : leur état dépend de la configuration.

![Chargement du dashboard](../../assets/img/securisation-avancee-infrastructures/it-8/Capture%20d’écran%20du%202026-10-08%2014-02-46.png)

Écran de chargement intermédiaire, insuffisant comme preuve de fonctionnement complet.

![Dashboard Wazuh après connexion](../../assets/img/securisation-avancee-infrastructures/it-8/Capture%20d’écran%20du%202026-10-08%2014-03-40.png)

Vue Overview ouverte avec des compteurs d’alertes. Aucun agent n’est encore enregistré à cet instant ; ces compteurs ne prouvent pas une collecte File Browser.

![État de santé de l’indexer](../../assets/img/securisation-avancee-infrastructures/it-8/Capture%20d’écran%20du%202026-10-08%2014-16-03.png)

Requête HTTPS avec CA et authentification interactive : status green, un nœud, aucune partition non allouée. Le mot de passe n’est pas affiché.

La VM Wazuh est identifiée par la sortie réseau fournie : **192.168.122.37**, interface enp1s0. Les captures et sorties sont des preuves à leur date, pas une garantie de disponibilité permanente.

### Interface après connexion de l’agent

![Dashboard MITRE Wazuh avec événements associés à vm-filebrowser](../../assets/img/securisation-avancee-infrastructures/it-8/Capture%20d’écran%20du%202026-10-08%2016-51-51.png)

Le dashboard MITRE affiche des agrégations pour vm-filebrowser, avec les
filtres manager.name=wazuh.manager et présence de rule.mitre.id.
Les catégories affichées sont des associations des règles Wazuh : elles
ne prouvent pas une attaque, une compromission ou une alerte File Browser
sur /api/renew. Les événements détaillés doivent être examinés pour
distinguer les opérations normales du laboratoire des activités suspectes.

La [note de collecte File Browser](etudier-agent-wazuh-file-browser.md)
contient également la capture de l’agent 001 actif et la preuve de réception
des logs Docker dans les archives du manager.

## 📦 Livrables et critères de réussite

| Preuve à conserver | Ce qu’elle doit montrer | État actuel |
| --- | --- | --- |
| Schéma complété | Machine Docker, adresse, trois composants et chemins d’accès | VM dédiée Ubuntu Server 26.04 retenue ; adresse et réalisation à confirmer |
| Versions et source | Référence du dépôt, commit et images réellement utilisées | À compléter |
| Stack démarrée | Trois composants stables et état des services du manager | Processus du manager illustrés ; état stable des trois conteneurs à compléter |
| Communication interne | Indexer disponible et absence d’erreurs persistantes entre composants | Indexer green et dashboard ouvert dans les captures |
| Dashboard accessible | Capture horodatée après connexion, page Wazuh ouverte et connexion manager fonctionnelle | Overview après connexion visible à 14:03:40 |
| Compte rendu du groupe | Participants, opérations réalisées, problèmes et corrections | À compléter |

Une page de connexion seule prouve que l’interface répond, pas que
l’ensemble de la stack fonctionne. Conserver une capture de l’état des
conteneurs et une capture de l’interface après authentification ; compléter
par les contrôles du manager et de l’indexer. Les commandes ci-dessus sont
une procédure, pas des résultats d’installation.

- [Architecture et points d’observation](concevoir-points-observation.md)
- [Retour à l’itération 8](index.md)
- [Retour au module](../README.md)
