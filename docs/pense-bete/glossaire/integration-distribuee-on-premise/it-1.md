# Glossaire Intégration distribuée on-premise — Itération 1

## Sujet

Préparation d'une machine Ubuntu, installation de Docker, construction d'images, déploiement de services avec Docker Compose et première analyse PCA/PRA.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Image Docker | Modèle immuable utilisé pour créer un ou plusieurs conteneurs. |
| Conteneur | Instance en exécution créée à partir d'une image Docker. |
| Dockerfile | Fichier décrivant les étapes reproductibles de construction d'une image. |
| Layer | Couche produite par une instruction d'image et réutilisable par Docker. |
| Docker Engine | Moteur qui construit les images et exécute les conteneurs. |
| Docker Compose | Outil qui décrit et orchestre plusieurs services dans un fichier Compose. |
| Service Compose | Définition logique d'un conteneur dans compose.yaml. |
| Volume nommé | Espace de stockage géré par Docker et indépendant du cycle de vie d'un conteneur. |
| Réseau Compose | Réseau créé automatiquement pour permettre aux services de communiquer. |
| Nom DNS de service | Nom, comme db, résolu par les autres services sur le réseau Compose. |
| Port publié | Port de l'hôte redirigé vers un port interne du conteneur, par exemple 8085:80. |
| Variable d'environnement | Paramètre injecté dans un service au démarrage. |
| Fichier .env | Fichier local contenant les valeurs d'environnement, notamment les secrets de TP. |
| Fichier .env.example | Modèle partageable indiquant les variables attendues sans leurs valeurs réelles. |
| PCA | Plan de Continuité d'Activité : maintien des activités essentielles pendant un incident. |
| PRA | Plan de Reprise d'Activité : remise en service après une interruption majeure. |
| RTO | Durée maximale cible avant la remise en service d'un élément. |
| RPO | Quantité maximale de données que l'organisation accepte de perdre. |
| Analyse d'écarts | Comparaison entre une documentation existante et l'état actuel de l'infrastructure. |

## Organisation des fichiers

~~~text
~/on-premise/
├── documentation/
│   ├── architecture.md
│   ├── inventory.md
│   ├── journal.md
│   └── commands.md
├── dockerfile-demo/
├── nginx-demo/
└── wordpress-compose/
~~~

## Manipulations faites

| Manipulation | Commandes ou actions |
| --- | --- |
| Préparer Ubuntu | Vérification de la version, du réseau, des mises à jour et de l'état initial. |
| Installer Docker | Installation de Docker Engine et du plugin Compose. |
| Construire Figlet | Dockerfile Ubuntu, installation de figlet et tags 1.0/2.0. |
| Construire Nginx | Dockerfile, copie de index.html, publication du port 8080. |
| Gérer un volume | Création, inspection, réutilisation et suppression explicite d'un volume MariaDB. |
| Déployer Compose | WordPress, MariaDB, réseau Compose et volume db_data. |
| Vérifier la persistance | docker compose down sans -v, puis recréation des services. |
| Documenter avec Git | Dépôt local, deux commits, diff et historique. |
| Analyser PCA/PRA | Tableau des écarts, priorités de mise à jour et questions à valider. |

## Commandes Docker essentielles

~~~bash
docker --version
docker compose version
docker image ls
docker build -t nom-image:version .
docker run nom-image:version
docker ps
docker ps -a
docker logs nom-conteneur
docker stop nom-conteneur
docker rm -f nom-conteneur
docker volume ls
docker volume inspect nom-volume
docker network ls
docker network inspect nom-reseau
~~~

## Commandes Compose essentielles

~~~bash
cd ~/on-premise/wordpress-compose
docker compose config
docker compose up -d
docker compose ps
docker compose logs
docker compose exec wordpress getent hosts db
docker compose down
~~~

Ne pas utiliser docker compose down -v avant d'avoir vérifié la persistance : l'option supprime aussi les volumes du projet.

## Points de vigilance

- Un Dockerfile est préférable à docker commit pour reconstruire une image de façon lisible et reproductible.
- Un conteneur supprimé ne conserve pas ses modifications hors volume.
- Un volume n'est pas supprimé par docker compose down sans l'option -v.
- Le fichier .env ne chiffre pas les secrets.
- Le fichier .env ne doit jamais être ajouté à Git.
- Une machine physique ne possède pas de snapshot d'hyperviseur.
- Un PCA/PRA ancien doit être analysé avant d'être modifié.
- Une information non confirmée doit rester marquée comme hypothèse.

## Docs associées

- [Vue d'ensemble de l'itération 1](../../../integration-distribuee-on-premise/it-1/index.md)
- [Installer Docker Engine](../../../integration-distribuee-on-premise/it-1/installer-docker-engine.md)
- [Construire une image avec un Dockerfile](../../../integration-distribuee-on-premise/it-1/construire-image-dockerfile.md)
- [Construire une image Nginx](../../../integration-distribuee-on-premise/it-1/construire-image-nginx-web.md)
- [Persistance avec un volume MariaDB](../../../integration-distribuee-on-premise/it-1/persistance-volume-mariadb.md)
- [Déployer WordPress et MariaDB avec Compose](../../../integration-distribuee-on-premise/it-1/deployer-wordpress-compose.md)
- [Gérer la documentation avec Git](../../../integration-distribuee-on-premise/it-1/gerer-documentation-avec-git.md)
- [Analyser le PCA et le PRA](../../../integration-distribuee-on-premise/it-2/analyser-pca-pra.md)
