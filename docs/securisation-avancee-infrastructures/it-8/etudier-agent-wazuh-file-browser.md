# Peut-on installer un agent Wazuh dans le conteneur File Browser ?

**Itération 8 — Note d’intégration et investigation**

## 🎯 Objectif et statut

Étudier puis réaliser, si possible, l’intégration d’un agent Wazuh **dans
le conteneur applicatif File Browser**, sans perdre le fonctionnement du
service ni son durcissement. Une incompatibilité expliquée constitue aussi
un résultat valable.

**Investigation réalisée à partir des sorties fournies par le participant :
image identifiée et connectivité TCP confirmée. Aucun agent installé ou
connecté dans le conteneur n’est démontré. L’alternative avec agent sur la VM
est désormais documentée et sa collecte confirmée dans la section 7.** La VM Wazuh utilise l’adresse
`192.168.122.37` dans la sortie fournie ; l’adresse est dynamique et doit
être confirmée avant configuration. Le succès de connexion au dashboard
est déclaré par le participant, pas une preuve de collecte depuis File Browser.

## Résultats de l’investigation — éléments à présenter au formateur

Les résultats ci-dessous proviennent des commandes exécutées par le
participant et collées dans la conversation. Ils décrivent l’état observé,
sans constituer une preuve d’installation de l’agent.

| Élément examiné | Résultat observé |
| --- | --- |
| Image applicative | File Browser **2.63.23**, Linux/amd64 |
| Digest de l’image configurée | `sha256:a469ea076d4a1b4b1d86a41d130f2f536cd9da996a2b1fb39c0d7635f9d89b9a` |
| Révision indiquée par les labels | `e8a388f840173580116f2743813d03b22286e44e` |
| Base finale du Dockerfile correspondant | `busybox:1.37.0-musl` ; Alpine est une étape de préparation, pas la base finale |
| Identification interne | `/etc/os-release` absent ; `/lib` et `/usr/lib` absents |
| Outils trouvés | `dpkg`, `rpm`, `busybox`, `nc`, `wget` ; `apk`, `apt-get`, `bash`, `ldd`, `getent`, `curl` non trouvés par `command -v` |
| BusyBox | Version 1.37.0 ; `nc --help` identifie explicitement une commande BusyBox |
| Utilisateur effectif | `uid=1000(user)`, `gid=1000(user)` |
| Démarrage | `tini -- /init.sh` ; le script prépare la configuration puis termine par `exec filebrowser "$@"` |
| Durcissement | `CapDrop=["ALL"]`, `no-new-privileges:true`, capacités effectives nulles, `NoNewPrivs: 1` ; racine non configurée en lecture seule |
| Persistance applicative | Trois bind mounts accessibles en écriture vers `/config`, `/database` et `/srv` |
| Publication réseau | Port 8080 de la VM vers 80 du conteneur, sur toutes les adresses IPv4 et IPv6 ; filtrage non prouvé par cette publication |

Source de construction examinée :
[Dockerfile File Browser à la révision indiquée par l’image](https://github.com/filebrowser/filebrowser/blob/e8a388f840173580116f2743813d03b22286e44e/Dockerfile).
Cette source est cohérente avec les observations internes ; le label seul
ne constitue pas une attestation complète du contenu de l’image.

`dpkg`, `rpm`, `nc` et `busybox` présentent la même taille et un nombre de
liens de 400 dans la sortie `ls -l`. Cela est cohérent avec des commandes
multi-appels BusyBox ; la présence de ces noms ne démontre pas un environnement
Debian ou RPM complet ni la capacité à exécuter les scripts d’un paquet Wazuh.

### Connectivité vérifiée depuis le conteneur

```text
192.168.122.37 (192.168.122.37:1515) open
Code retour 1515 : 0
192.168.122.37 (192.168.122.37:1514) open
Code retour 1514 : 0
```

Les essais `nc -vz -w 3` montrent que les connexions TCP aux ports
d’enrôlement et de transport sont possibles depuis le conteneur.
Ils ne prouvent ni l’enrôlement, ni l’authentification, ni la remontée d’événements.

### Conclusion et décision à discuter

**La connectivité est disponible ; l’environnement minimal est le principal
obstacle identifié à une installation classique.** La base musl, l’absence
d’environnement de paquets complet et le démarrage prévu pour File Browser
seul ne justifient pas l’installation directe d’un paquet Debian/RPM.
Aucun échec d’installation Wazuh n’a été observé : la compatibilité de ses
binaires et dépendances reste à vérifier, et l’impossibilité absolue n’est
pas démontrée.

Une piste réaliste à discuter est une **image de test sur une base compatible
avec l’agent**, intégrant File Browser et un mécanisme de démarrage des deux
services. Ce serait une reconstruction de l’environnement applicatif, à
distinguer d’une simple installation dans l’image BusyBox existante. Elle
exigerait de vérifier les dépendances, les UID/GID, la persistance, le
fonctionnement applicatif et le maintien du durcissement.

**Aucune modification de conteneur ou installation d’agent n’est documentée
à ce stade.** Le participant prévoit de discuter cette stratégie avec le
formateur avant de poursuivre l’essai. Le conteneur existant et ses données
restent la référence à préserver.

## 1. Examiner l’existant avant de modifier

Exécuter les commandes Docker **dans la VM File Browser**, pas dans la VM
Wazuh. Vérifier le nom du conteneur ; remplacer `filebrowser` si nécessaire.

```bash
sudo docker ps --format 'table {{.Names}}	{{.Image}}	{{.Ports}}'
sudo docker inspect --format \
  'Image={{.Config.Image}} User={{.Config.User}} ReadonlyRootfs={{.HostConfig.ReadonlyRootfs}}' filebrowser
sudo docker inspect --format '{{json .Mounts}}' filebrowser
sudo docker inspect --format \
  'Entrypoint={{json .Config.Entrypoint}} Cmd={{json .Config.Cmd}}' filebrowser
sudo docker inspect --format \
  'CapDrop={{json .HostConfig.CapDrop}} SecurityOpt={{json .HostConfig.SecurityOpt}}' filebrowser
sudo docker top filebrowser
sudo docker exec -it filebrowser /bin/sh
```

Ne pas publier un inspect complet : variables, arguments et montages peuvent
révéler des informations sensibles. Le champ `User` peut être vide ; identifier
également l’utilisateur effectif du processus. Si `/bin/sh` est absent,
conserver cette erreur et poursuivre avec les inspections Docker : absence
de shell ne signifie pas absence de l’application.

Dans le conteneur, **si le shell existe**, chercher les outils sans les installer :

```sh
cat /etc/os-release
uname -m
id
ps
for outil in apk apt-get dpkg rpm bash busybox ldd getent nc curl wget; do
  command -v "$outil"
done
ls -ld /bin /usr/bin /lib /usr/lib /var /tmp
cat /proc/1/status
```

Noter chaque commande absente au lieu de supposer une distribution. Ne pas
confondre le noyau partagé montré par `uname` avec le système de base de
l’image. Si disponible, relever `ldd --version` et les bibliothèques utilisées
par les binaires de confiance examinés ; la présence d’un binaire File Browser
statique ne garantit pas la compatibilité d’un agent dynamique.

Si `nc` existe et accepte ces options, vérifier depuis le conteneur :

```sh
nc -z -w 3 192.168.122.37 1514
nc -z -w 3 192.168.122.37 1515
```

1514/TCP sert habituellement aux événements, 1515/TCP à l’enrôlement.
Un port accessible ne prouve pas l’authentification de l’agent. Une commande
absente ne prouve pas une panne réseau. Un test depuis la VM seule ne démontre
pas le chemin du conteneur. Adapter aux outils trouvés et à la configuration
réelle du manager ; ne pas ajouter de paquets dans le service pour ce diagnostic.

## 2. Comparer avec les besoins de l’agent

Consulter la [procédure Linux officielle](https://documentation.wazuh.com/current/installation-guide/wazuh-agent/wazuh-agent-package-linux.html)
pour choisir un paquet et une procédure adaptés au système réellement trouvé.
L’[enrôlement](https://documentation.wazuh.com/current/user-manual/agent/agent-enrollment/requirements.html)
nécessite aussi une identité et une communication avec le manager.
Un paquet Debian/RPM ne doit pas être considéré compatible avec toute image
Linux ; vérifier ABI, bibliothèques et architecture. Choisir une version
compatible avec celle du manager.

| Besoin de l’agent Wazuh | Disponible dans le conteneur ? | Modification nécessaire |
| --- | --- | --- |
| Architecture et système pris en charge par le paquet retenu | À relever | Sélection d’un paquet compatible, ou réexamen de la stratégie |
| Chargeur et bibliothèques nécessaires | À relever | Dépendances validées pour cette base ; ne pas copier au hasard un binaire |
| Outils d’installation et scripts du paquet | À relever | Construction reproductible et installation lors du build |
| Droits et chemins accessibles en écriture, notamment `/var/ossec` | À relever | Répertoires, propriétaires et montages limités aux besoins établis |
| Démarrage des processus de l’agent | À relever | Supervision adaptée au conteneur ; systemd n’est pas présumé disponible |
| Coexistence avec File Browser | À relever | Gestion des deux services, signaux, arrêt et détection d’échec |
| Route vers le manager et ports requis | 1514/TCP et 1515/TCP accessibles, codes 0 | Adresse stable et flux autorisés selon enrôlement/transport retenus |
| Identité et clé de l’agent | Non vérifiées | Enrôlement propre à cette instance et stockage persistant protégé |
| Journaux ou fichiers utiles accessibles | À identifier | Configurer des sources réellement présentes et leurs permissions |

L’agent doit être adapté à cette base et à cette exécution sans système
complet d’init. Les commandes `systemctl` d’un tutoriel VM ne s’appliquent
pas automatiquement à un conteneur.

## 3. Choisir et justifier une stratégie

**Piste à étudier : une image dérivée reproductible**, construite à partir
de la référence File Browser réellement utilisée et testée sur une copie
isolée. Cette piste n’est retenue définitivement qu’après vérification des
besoins ci-dessus ; aucun Dockerfile universel n’est fourni avant ces résultats.

Consigner avant l’essai :

- la référence et le digest de l’image d’origine, les dépendances nécessaires et leur source ;
- la façon de lancer l’agent et File Browser, de gérer PID 1, les signaux et l’arrêt des services ;
- les UID/GID : conserver les droits limités de File Browser, même si certaines opérations de l’agent nécessitent d’autres droits ;
- la configuration d’enrôlement et la persistance de l’identité, sans intégrer la clé d’un agent dans une image distribuée ;
- les sources à collecter, leur portée et les limites des espaces de noms ;
- les sauvegardes, la copie des données et la méthode de retour à l’image initiale.

Une installation via `docker exec` dans la couche writable peut servir à
une expérimentation **sur la copie**, mais disparaît à la recréation et ne
constitue pas une livraison maintenable. Ne pas retirer `read_only`,
`cap_drop` ou `no-new-privileges` sans besoin établi et documenté.
Ni `--privileged`, ni le socket Docker, ni le partage global des espaces de
noms ne sont des solutions à ajouter par défaut.

Si la base est incompatible ou l’image devient trop complexe, expliquer
pourquoi. Un agent sur la VM Docker ou une collecte distincte des journaux
peut être proposé en conclusion comme autre architecture ; cela ne valide
pas l’objectif spécifique d’un agent **dans le même conteneur**.

## 4. Réaliser l’essai sur une copie isolée

1. Relever la configuration fonctionnelle et sauvegarder les données, la base et la configuration File Browser selon leurs montages réels.
2. Préparer une image dérivée et un déploiement de test avec données copiées et port distinct. Ne pas faire écrire deux instances sur la même base applicative.
3. Installer l’agent selon la procédure officielle correspondant au système vérifié. Conserver les étapes de build et les erreurs ; vérifier les signatures des sources selon cette procédure.
4. Configurer le manager `192.168.122.37` après confirmation de l’adresse, le transport et un nom d’agent distinct pour cette instance.
5. Prévoir un enrôlement au démarrage selon la méthode choisie ; ne pas inscrire de secret dans le Dockerfile ou Git.
6. Démarrer avec le mécanisme de supervision retenu et vérifier les deux services.

Si l’agent a été installé sous `/var/ossec`, les contrôles possibles sont,
dans le conteneur de test, avec les droits appropriés :

```sh
/var/ossec/bin/wazuh-control status
tail -n 80 /var/ossec/logs/ossec.log
```

Le lancement avec `wazuh-control start`, lorsqu’il est applicable, ne remplace
pas à lui seul la gestion du cycle de vie des deux services dans le conteneur.

## 5. Vérifier le résultat de bout en bout

| Contrôle | Preuve attendue | État actuel |
| --- | --- | --- |
| File Browser reste utilisable | Accès, authentification et opération sur fichier de test, avec résultat attendu | Non vérifiable |
| Agent lancé | État des processus et logs sans erreur bloquante | Non vérifiable |
| Agent connecté | Identité distincte, statut actif et dernière connexion dans Wazuh | Non vérifiable |
| Source locale collectée | Événement horodaté du conteneur, associé au bon agent dans Wazuh | Non vérifiable |
| Redémarrage / recréation | Deux services repris, configuration et identité persistantes sans duplications | Non vérifiable |
| Durcissement préservé | Droits File Browser, montages et options comparés à l’état initial | Non vérifiable |

Pour l’événement de test, choisir une source configurée : modification inerte
sur un fichier de test surveillé par FIM, ou ligne d’un journal de test
collecté. Vérifier la réception et le traitement attendus ; tous les événements
collectés ne deviennent pas automatiquement des alertes indexées dans le
dashboard. Noter règle, niveau, index ou journal utilisé pour établir la preuve.
Un agent actif seul ne prouve pas la collecte applicative.

## 6. Diagnostic à compléter pendant l’essai

| Symptôme | Message exact | Vérifications | Cause établie ou hypothèse | Modification essayée | Résultat |
| --- | --- | --- | --- | --- | --- |
| À renseigner | Extrait sans secret | Commandes et résultats | Distinguer cause prouvée et piste | Changement précis | Réussi, échoué ou non vérifiable |

Pistes : gestionnaire absent, dépendance/chargeur incompatible, système de
fichiers en lecture seule, permission insuffisante, absence de systemd,
agent non relancé, route ou enrôlement refusé, identité dupliquée, source
non journalisée. Conserver le message observé avant de choisir une correction.
Un échec local de permissions n’est pas un motif pour élargir tous les droits.

## 7. Alternative proposée par le formateur : collecte depuis la VM

Après l’investigation BusyBox, le formateur a proposé d’envoyer les logs du
conteneur. La solution essayée installe **l’agent sur la VM File Browser**,
sans l’intégrer à son image. Elle fournit une visibilité sur les traces
applicatives, mais ne valide pas l’installation dans le même conteneur.

```text
File Browser → stdout/stderr → fichier Docker json-file
                                      |
                     Agent Wazuh sur la VM 192.168.122.229
                                      |
                     Manager Wazuh sur la VM 192.168.122.37
```

| Étape vérifiée | Résultat dans les sorties fournies |
| --- | --- |
| OS de la VM File Browser | Ubuntu 26.04.1 LTS |
| Versions | Agent et manager 4.14.8 ; manager révision rc2 |
| Enrôlement | Clé reçue pour vm-filebrowser ; agent 001 actif côté manager |
| Connexion | État connected et connexion à 192.168.122.37:1514/TCP |
| Source applicative | Driver json-file ; logs de démarrage/arrêt, réponses 404 et /api/renew 401 |
| Configuration du collecteur | Validation wazuh-logcollector -t, code 0 ; Analyzing file sur le fichier Docker |
| Réception | Trois messages /api/renew 401 retrouvés dans archives.json du manager |
| Décodage | Décodeur json ; message applicatif dans data.log, avec stream et time |
| Alerte / dashboard pour ces messages | Non démontrée ; aucune règle spécifique validée |

### Captures du test et du diagnostic

![Agent connecté, fichier Docker surveillé et requêtes HTTP 401](../../assets/img/securisation-avancee-infrastructures/it-8/Capture%20d’écran%20du%202026-10-08%2016-38-18.png)

À gauche : connexion, test du collecteur avec code 0 et fichier Docker
analysé. En bas à droite : requêtes depuis l’hôte retournant 401 ; en bas à
gauche : traces applicatives correspondantes. La politique SCA Ubuntu 22.04
est ignorée sur Ubuntu 26.04. À droite, une inspection File Browser exécutée
sur la VM Wazuh échoue : ce conteneur doit être inspecté sur sa propre VM.

![Traces Docker, agent connecté et diagnostic des archives](../../assets/img/securisation-avancee-infrastructures/it-8/Capture%20d’écran%20du%202026-10-08%2016-50-47.png)

À gauche : nouvelles traces Docker et état connected. À droite : archives
JSON présentes, avec des événements auditd de vm-filebrowser visibles dans
cet extrait. Les erreurs de chemin sur l’hôte viennent de commandes destinées
à la VM Wazuh. La réception des messages File Browser ci-dessous est établie
par la sortie texte fournie ensuite, pas par les seules lignes auditd affichées.

![Agent vm-filebrowser actif dans le dashboard Wazuh](../../assets/img/securisation-avancee-infrastructures/it-8/Capture%20d’écran%20du%202026-10-08%2016-52-44.png)

La vue Explore agent affiche **001 — vm-filebrowser**, groupe default,
version **v4.14.8**, OS **Ubuntu 26.04.1 LTS**, statut **active**.
Cette capture confirme l’identité et la connexion de l’agent installé sur
la VM ; elle ne signifie pas que l’agent fonctionne dans le conteneur.

![Dashboard MITRE Wazuh avec événements associés à vm-filebrowser](../../assets/img/securisation-avancee-infrastructures/it-8/Capture%20d’écran%20du%202026-10-08%2016-51-51.png)

Le dashboard MITRE affiche des agrégations pour vm-filebrowser, avec les
filtres manager.name=wazuh.manager et présence de rule.mitre.id.
Les catégories affichées sont des associations des règles Wazuh : elles
ne prouvent pas une attaque, une compromission ou une alerte File Browser
sur /api/renew. Les événements détaillés doivent être examinés pour
distinguer les opérations normales du laboratoire des activités suspectes.

### Pourquoi les premières recherches ne trouvaient rien

L’archivage était désactivé (logall_json=no). Le fichier source monté sous
/wazuh-config-mount/etc/ossec.conf passait à yes, tandis que la configuration
effective /var/ossec/etc/ossec.conf, dans un volume persistant, restait à no,
même après recréation. Les inspections ont confirmé les deux valeurs ; le
mécanisme exact de cette divergence n’a pas été établi.

Le participant a sauvegardé puis changé le paramètre dans la configuration
effective. Après redémarrage, yes était conservé. Une nouvelle requête après
reconnexion a ensuite permis de retrouver les messages dans archives.json.
L’échec d’une recherche dans alerts.json ne prouvait donc pas un échec de
transmission. L’archivage complet reste activé au dernier état observé ; sa
désactivation après diagnostic est à prévoir et à vérifier pour limiter le
volume. Le fichier source et la configuration effective doivent rester cohérents.

### Preuve de réception fournie en texte

Extrait des champs du dernier événement, relevé dans les archives du manager :

```json
{
  "timestamp": "2026-10-08T14:50:07.851+0000",
  "agent": {"id": "001", "name": "vm-filebrowser", "ip": "192.168.122.229"},
  "manager": {"name": "wazuh.manager"},
  "decoder": {"name": "json"},
  "data": {
    "log": "2026/10/08 14:50:07 /api/renew: 401 192.168.122.1 <nil>\n",
    "stream": "stdout",
    "time": "2026-10-08T14:50:07.29758532Z"
  }
}
```

C’est un extrait, pas l’objet brut complet. La source originale location est
le fichier Docker du conteneur f9810c6225f6592e3b219b4dbcf304db333253c1772fd3e25576183d2d89ec66.
Les deux autres événements sont reçus à 14:49:05.845 et 14:49:43.848 UTC.
14:50 UTC correspond à 16:50 en heure locale CEST ; ne pas confondre
horodatage applicatif, Docker et réception.

### Configuration et limites à conserver

Le bloc ajouté sur la VM File Browser est un localfile, log_format=json,
avec le chemin exact retourné par docker inspect --format '{{.LogPath}}'.
Ce chemin dépend de l’identité du conteneur : vérifier et adapter la collecte
après recréation. La configuration fonctionne pour le conteneur observé ;
sa continuité après rotation ou recréation n’est pas démontrée.

Le 401 correspond à un renouvellement de session refusé, pas à une attaque
prouvée. Le décodeur JSON extrait le champ log, mais ne structure pas encore
son chemin HTTP, son statut et son IP en champs applicatifs distincts.
L’indexation d’une alerte exige une règle adaptée ; l’activation des archives
locales ne les rend pas automatiquement visibles dans le dashboard.
Les logs ne démontrent pas l’enregistrement de tous les accès réussis.

**Résultat : collecte applicative de bout en bout prouvée depuis la VM.**
Le conteneur BusyBox n’a pas besoin d’être reconstruit pour cette collecte.
L’intégration d’un agent à l’intérieur reste non réalisée ; cette alternative
répond au besoin de traces selon la piste proposée par le formateur.

## 📦 Note d’intégration à rendre

| Rubrique | Contenu à compléter |
| --- | --- |
| Environnement trouvé | Image/digest, distribution, architecture, libc, outils, utilisateur et processus |
| Besoins de l’agent | Tableau de compatibilité complété et références consultées |
| Stratégie | Décision justifiée, démarrage, droits, réseau et persistance |
| Modifications réalisées | Dockerfile/configuration/scripts, versions et différences réelles |
| Difficultés | Messages, vérifications, causes, essais et résultats |
| Résultat final | Fonctionnel avec preuves, partiel ou non fonctionnel avec diagnostic |
| Conclusion | Faisabilité, visibilité obtenue, maintenance et alternative éventuelle |

**Conclusion provisoire : installation classique non justifiée dans la base
BusyBox-musl observée ; intégration à étudier sur une image de test compatible.**
La connectivité aux deux ports est confirmée, mais aucun agent fonctionnel
n’est démontré. Le formateur a proposé la collecte des logs depuis la VM ; cette alternative
a été réalisée et sa réception est prouvée dans la section 7.
La qualité de l’investigation compte autant que le succès de l’installation.

- [Points d’observation et limites](concevoir-points-observation.md)
- [Plateforme Wazuh single-node](installer-wazuh-single-node.md)
- [Retour à l’itération 8](index.md)
- [Retour au module](../README.md)
