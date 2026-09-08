# Mémo personnel de synthèse

!!! info "Mémo remis avant débrief final"
    Cette page tient sur une synthèse courte. Elle reformule les notions que je
    retiens du module Cloud & IAM après les manipulations réalisées sur OVHcloud
    et Infomaniak.

## 1. Le cloud ne supprime pas mes responsabilités

Le fournisseur cloud met à disposition des ressources prêtes à l'emploi :
machines virtuelles, réseau, stockage, IAM, métriques ou stockage objet. Mais
il ne décide pas à ma place quelles règles de pare-feu ouvrir, quels comptes
créer, où mettre les secrets ou comment sauvegarder mes données.

Ce que je retiens du modèle de responsabilité partagée, c'est que le cloud
déplace une partie du travail, mais ne le fait pas disparaître. Le fournisseur
gère l'infrastructure physique et une partie des services managés. De mon côté,
je reste responsable de la configuration, des accès, des données et des erreurs
d'exposition.

## 2. OpenTofu et Ansible n'ont pas le même rôle

OpenTofu sert à créer les ressources cloud : VM, réseau, règles, volumes ou
stockage. C'est la couche de provisionnement. Elle change selon le fournisseur,
car chaque plateforme a ses noms de ressources, ses images, ses flavors et ses
contraintes.

Ansible intervient ensuite pour configurer les machines : paquets, Docker,
services, fichiers, pare-feu et déploiements applicatifs. Cette partie change
beaucoup moins d'un fournisseur à l'autre. Le module m'a surtout montré qu'il
ne faut pas tout réécrire quand on change de cloud : il faut adapter la couche
fournisseur, puis rejouer la configuration.

## 3. Exploiter, c'est mesurer et nettoyer

Une infrastructure qui fonctionne n'est pas forcément une infrastructure bien
exploitée. Il faut aussi savoir vérifier les métriques, déclencher une alerte,
nettoyer les ressources inutilisées et mesurer le temps de restauration après
incident.

Le test de restauration m'a permis de relier les notions de RTO et RPO à du
concret : le RTO dépend du temps nécessaire pour recréer les VM avec OpenTofu,
relancer Ansible et vérifier les services. Le RPO dépend de l'âge réel de la
sauvegarde restaurée. S'il manque une sauvegarde ou son horodatage, je ne peux
pas prétendre que le RPO est maîtrisé.

## Ce que je retiens pour la suite

Le point le plus important pour moi est que le cloud doit rester reproductible.
Si l'infrastructure dépend uniquement de clics faits dans une console, elle est
difficile à expliquer, à restaurer et à auditer. Avec du code, des captures, des
horodatages et des validations, je peux prouver ce qui a été fait et identifier
ce qui reste fragile.

Pour un prochain projet, je garderais donc trois réflexes : limiter les droits,
automatiser ce qui peut l'être, et vérifier régulièrement que la restauration
fonctionne vraiment.
