# Observer le conteneur sans y exécuter Lynis

## Consigne de la formatrice

**Lynis doit être exécuté sur la VM Ubuntu 20.04 cible, pas dans le conteneur
File Browser.** Aucun paquet, script ou répertoire Lynis ne doit être installé,
copié ou lancé dans le conteneur.

Cette feuille conserve uniquement les informations déjà récupérées et décrit ce
qui peut être observé depuis Docker. Une limite documentée est un résultat
valable : il ne faut pas modifier l’image pour augmenter artificiellement la
couverture de l’audit.

## Objectif

Décrire le périmètre réellement couvert par Lynis sur la VM et recueillir les
métadonnées disponibles sur File Browser sans transformer le conteneur.

**Statut au 1er octobre 2026 : observations internes limitées réalisées à
11:49:04 +02:00 ; aucun audit Lynis exécuté dans le conteneur.** Le conteneur a
été démarré pendant les observations, puis arrêté volontairement. Les
métadonnées complètes de l’image sont conservées dans la
[feuille précédente](limites-audit-preparer-analyse-conteneur.md).

## Périmètres à distinguer

| Périmètre | Outil ou méthode | Ce qui est couvert | Limite principale |
| --- | --- | --- | --- |
| VM Ubuntu 20.04 | Lynis exécuté sur la VM | Comptes de l’hôte, SSH, services, paquets Ubuntu, noyau, journaux et configuration Docker visible depuis l’hôte | Ne parcourt pas les composants internes de l’image comme un scanner d’image |
| Conteneur File Browser | `docker inspect`, `docker image inspect`, historique et observation ponctuelle | Configuration d’exécution, utilisateur déclaré, montages, ports, état, image référencée et quelques fichiers internes | Pas d’audit Lynis interne et pas d’inventaire exhaustif des dépendances |
| Image File Browser | Analyse d’image prévue avec l’outil du module, notamment Trivy | Paquets et dépendances reconnus, vulnérabilités associées et éventuellement mauvaises configurations selon les scanners activés | Résultats dépendants de la base, de la couverture et de l’identification des composants |
| Données montées | `stat`, `namei`, ACL et tests fonctionnels avec données fictives | Propriétaires, permissions Unix, ACL et comportement applicatif | Un scan d’image ne couvre pas automatiquement les données ajoutées lors de l’exécution |

## Informations déjà récupérées

| Contrôle | Résultat observé | Conclusion limitée |
| --- | --- | --- |
| État initial | `Status=exited`, ImageID `sha256:a68f43720ea6ff331fa4b92becced20af14b72f4c3a22ca1f764076a8e42e1a5` | Conteneur arrêté et image locale précisément rattachée au relevé |
| Démarrage de contrôle | `Up Less than a second (health: starting)`, publication `0.0.0.0:8080->80/tcp` et `:::8080->80/tcp` | Démarrage et publication IPv4/IPv6 observés ; l’état `healthy` n’est pas prouvé par cette sortie immédiate |
| Distribution interne | Alpine Linux 3.13.4 d’après `/etc/os-release` | Environnement utilisateur identifié ; provenance exacte de l’image de base non démontrée |
| Noyau visible | `5.15.0-139-generic` | Noyau partagé avec la VM, pas un noyau propre à Alpine |
| Lynis | Commande absente du `PATH` | Conforme au périmètre retenu ; aucune installation à effectuer |
| Gestionnaire et outils | `apk`, `tar`, `curl`, `wget`, `ps` présents | Inventaire ponctuel, sans installation supplémentaire |
| Outils absents du `PATH` | `lynis`, `apt-get`, `dpkg-query`, `rpm` | Image Alpine réduite ; aucune tentative d’installation à effectuer |
| Shell d’observation | UID/GID 0, groupes `root`, `bin`, `daemon`, `sys`, `adm`, `disk`, `wheel`, `floppy`, `tape` et `video` | Session `docker exec` root observée ; ne prouve pas un accès root à la VM |
| Processus File Browser | PID 1 `/filebrowser`, quatre UID et GID à 0, `Umask: 0022` | Processus applicatif root confirmé pour cette exécution |
| Répertoires | `/tmp` en `root:root 1777`, `/var/log` en `root:root 755` | Permissions observées sans modification |
| Restrictions | `NoNewPrivs: 0`, `Seccomp: 2`, un filtre, `CapEff=00000000a80425fb` | Seccomp actif et capacités non nulles ; isolation complète non démontrée |
| Montage de données | `/srv/filebrowser -> /srv`, lecture-écriture | Le processus du conteneur peut agir sur les données selon les droits du montage et de l’hôte |
| Configuration Docker | `Privileged=false`, `ReadonlyRootfs=false`, réseau `bridge` | Mode privilégié désactivé ; racine du conteneur modifiable |
| Publication | Port hôte 8080 vers `80/tcp` | Publication configurée ; accessibilité dépend de l’état du conteneur et du filtrage |

Ces éléments complètent le constat sur l’isolation et l’exécution en root. Ils
ne constituent pas un audit Lynis du conteneur et ne prouvent aucune
vulnérabilité exploitable à eux seuls.

## Relever les métadonnées depuis la VM

Ces commandes s’exécutent sur la **VM cible** et fonctionnent même si le
conteneur est arrêté :

```bash
date -Is
hostname
sudo docker ps -a --no-trunc \
  --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'

sudo docker inspect --type container filebrowser --format \
  'ContainerID={{.Id}} Reference={{.Config.Image}} ImageID={{.Image}} Status={{.State.Status}}'

FB_IMAGE_ID=$(sudo docker inspect --type container filebrowser --format '{{.Image}}')
sudo docker image inspect "$FB_IMAGE_ID" --format \
  'ImageID={{.Id}} RepoTags={{json .RepoTags}} RepoDigests={{json .RepoDigests}} OS={{.Os}} Architecture={{.Architecture}}'

sudo docker inspect --type container filebrowser --format \
  'User={{json .Config.User}} Privileged={{.HostConfig.Privileged}} ReadonlyRootfs={{.HostConfig.ReadonlyRootfs}} RestartPolicy={{.HostConfig.RestartPolicy.Name}} NetworkMode={{.HostConfig.NetworkMode}}'

sudo docker inspect --type container filebrowser --format \
  '{{range .Mounts}}{{println .Type .Source "->" .Destination "RW=" .RW}}{{end}}'

sudo docker inspect --type container filebrowser --format \
  'DeclaredPorts={{json .Config.ExposedPorts}} PortBindings={{json .HostConfig.PortBindings}} RuntimePorts={{json .NetworkSettings.Ports}}'
```

Ne pas publier un `docker inspect` brut : les variables d’environnement et les
labels peuvent contenir des informations internes. Les formats ciblés réduisent
ce risque.

## Observation interne déjà réalisée

Les commandes suivantes expliquent les preuves déjà obtenues. Il n’est pas
nécessaire de les répéter ni de redémarrer le conteneur uniquement pour cette
feuille :

```sh
cat /etc/os-release
id
uname -r
command -v lynis
command -v apk
ps
cat /proc/1/status
```

Si une nouvelle observation interne est demandée ultérieurement, elle devra
rester limitée à la lecture. Ne pas exécuter `apk add`, copier Lynis, lancer
`lynis audit system`, ajouter des privilèges, monter le socket Docker ou
partager les espaces de noms de la VM.

## Ce que ces observations ne permettent pas de conclure

- Elles ne donnent pas un inventaire exhaustif des paquets, bibliothèques et
  dépendances compilées dans le binaire File Browser.
- Elles ne démontrent pas l’absence ou la présence d’une CVE applicable.
- Elles ne prouvent pas que le processus root du conteneur peut devenir root sur
  la VM.
- Elles ne valident pas les permissions applicatives entre `public`,
  `partenaires` et `interne`.
- Elles ne remplacent pas l’analyse de l’image exacte ni un test fonctionnel
  réalisé avec des données fictives.

## Travail restant

1. conserver l’ImageID et le RepoDigest déjà relevés ;
2. analyser cette image exacte avec Trivy lors de l’activité prévue ;
3. dater la version de Trivy et sa base de vulnérabilités ;
4. distinguer les résultats de l’image, ceux de la VM et les permissions des
   données montées ;
5. vérifier chaque résultat avec les références de l’avis concerné avant de le
   déclarer applicable.

## Conclusion

L’audit Lynis documenté concerne uniquement la VM Ubuntu. Pour le conteneur, les
preuves disponibles se limitent aux métadonnées Docker et aux observations
internes déjà réalisées. Cette couverture partielle est explicitement conservée
au lieu d’installer Lynis dans une image applicative qui n’a pas été conçue pour
l’héberger.

- [Activité précédente — Limites de l’audit et préparation de l’analyse](limites-audit-preparer-analyse-conteneur.md)
- [Retour à l’itération 2](index.md)
- [Dossier de preuves](../dossier-preuves.md)
