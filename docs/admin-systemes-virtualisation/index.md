# Administration des systèmes — Virtualisation

!!! info "Module en préparation"
    Cette page pose le cadre général du module. Les cours, activités, procédures et retours d'expérience seront ajoutés au fil de la formation.

## Objectif global

Ce module introduit la couche de virtualisation qui structure les infrastructures modernes. L'objectif est d'acquérir les bases opérationnelles nécessaires pour déployer, administrer, sécuriser et superviser des machines virtuelles sur les deux écosystèmes de référence : **Microsoft Hyper-V** et **VMware ESXi**.

La virtualisation constitue également une passerelle vers les services distribués, les infrastructures *on-premise* et le cloud. Dans une infrastructure IaaS (*Infrastructure as a Service*), la machine virtuelle reste l'un des blocs de base.

## Vous apprendrez à

- Comprendre les concepts fondamentaux : hyperviseur de type 1 ou 2, machine virtuelle, conteneur, abstraction matérielle et ressources partagées.
- Déployer des machines virtuelles Windows et Linux avec Hyper-V.
- Configurer les ressources d'une VM : processeur, mémoire, stockage VHDX et réseau virtuel.
- Administrer un environnement VMware composé d'ESXi et de vCenter.
- Gérer les datastores, les commutateurs virtuels et les modèles de déploiement.
- Comprendre et mettre en œuvre vMotion, HA (*High Availability*) et DRS (*Distributed Resource Scheduler*).
- Isoler les VMs, durcir les hyperviseurs et contrôler l'accès au plan de gestion.
- Distinguer un snapshot d'une sauvegarde pérenne.
- Mesurer l'utilisation des ressources et ajuster leur allocation sans surengagement incontrôlé.
- Documenter l'architecture, l'inventaire des VMs, les choix de dimensionnement et les performances.

## Progression prévue

La trajectoire pédagogique suit quatre actions : **concevoir → déployer → orchestrer → durcir**.

| Phase | Sujet | Résultat attendu |
|---|---|---|
| 1 | Comprendre la virtualisation | Expliquer les rôles de l'hyperviseur, de la VM et du conteneur, puis comparer infrastructure physique et virtuelle. |
| 2 | Déployer avec Hyper-V | Créer des VMs Windows et Linux, configurer les VHDX, snapshots et vSwitch, puis intégrer les systèmes Windows à Active Directory. |
| 3 | Déployer avec VMware ESXi | Installer ESXi, administrer avec vCenter et gérer VMs, datastores, réseaux virtuels et modèles. |
| 4 | Orchestrer avec vMotion, HA et DRS | Préparer la migration à chaud, la haute disponibilité et le placement automatique des charges. |
| 5 | Sécuriser, optimiser et documenter | Durcir la plateforme, isoler les réseaux, organiser les sauvegardes, suivre les performances et produire les livrables. |

!!! warning "Point de vigilance"
    Un snapshot conserve un état temporaire utile avant une modification ou pour un retour arrière rapide. Il ne remplace pas une sauvegarde indépendante et durable.

## Livrables du module

### VMs Hyper-V opérationnelles

- VMs Windows et Linux fonctionnelles ;
- disques virtuels VHDX ;
- snapshots configurés ;
- vSwitch documenté.

### Environnement VMware ESXi et vCenter

- ESXi installé ;
- cluster administré avec vCenter ;
- VMs déployées depuis des modèles ;
- datastores configurés.

### Démonstration vMotion et HA

- migration à chaud d'une VM réussie ;
- procédure, captures et prérequis documentés ;
- HA configurée sur un cluster de test.

### Rapport de sécurité et de performance

- isolation des VMs justifiée ;
- durcissement des hyperviseurs documenté ;
- sauvegardes opérationnelles ;
- métriques de performance relevées et ajustements expliqués.

### Schéma d'architecture virtualisée

- cluster, datastores et réseaux virtuels représentés ;
- inventaire des VMs intégré ;
- dimensionnement justifié ;
- schéma lisible et exploitable par un tiers.

## En fin de module

Tu devrais être capable de déployer et d'administrer des VMs sur Hyper-V et VMware ESXi, de comprendre les mécanismes de migration et de haute disponibilité, de sécuriser l'isolation des charges, d'ajuster les ressources et de documenter une infrastructure virtualisée dans un format professionnel.

## État d'avancement

- [x] Présentation générale du module
- [ ] Cours et notions détaillées
- [ ] Travaux pratiques Hyper-V
- [ ] Travaux pratiques VMware ESXi et vCenter
- [ ] Mise en œuvre de vMotion, HA et DRS
- [ ] Sécurisation, optimisation et documentation finale
