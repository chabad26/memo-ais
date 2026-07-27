# Mémo personnel — Module Virtualisation

## Ce que je retiens

### 1. Proxmox et Hyper-V

J'ai utilisé deux solutions de virtualisation. Hyper-V héberge les machines du laboratoire sur `LABO_CORE`, tandis que Proxmox fournit l'interface de gestion, le cluster, la migration et la haute disponibilité de `WEB1`. Les deux permettent de créer des VM, des réseaux et des disques virtuels, mais Proxmox m'a permis de découvrir plus directement le fonctionnement d'un cluster. Dans mon montage, Proxmox est lui-même virtualisé dans Hyper-V : c'est utile pour apprendre, mais cela ne remplace pas trois serveurs physiques indépendants.

### 2. La haute disponibilité dépend de plusieurs éléments

Un cluster ne suffit pas à lui seul. Proxmox utilise Corosync et le quorum pour éviter que des nœuds isolés prennent des décisions contradictoires. Le disque de la VM doit aussi être accessible depuis le nœud de reprise : c'est le rôle de `nfs-shared` pour `WEB1`. Une migration à chaud sert surtout aux maintenances planifiées ; après une panne brutale, la HA redémarre la VM sur un autre nœud. Dans mon montage imbriqué, cette disponibilité reste logique et non physique.

### 3. La gestion des ressources

La virtualisation ne crée pas de puissance supplémentaire. Les vCPU, la RAM, le réseau et le stockage attribués aux VM utilisent les ressources physiques de l'hôte. Un surengagement peut provoquer des lenteurs, du swap, une saturation du stockage ou empêcher la reprise d'une VM. Je dois donc comparer les ressources attribuées à la consommation réelle, surveiller les tendances et conserver une marge pour la haute disponibilité. Dans mon laboratoire, `PVE2` demande plus de mémoire que les 3 Gio attribués, ce qui montre concrètement cette limite.

## Ce qui reste à approfondir

- La possibilité de le reproduire en prod avec moins de contraintes de ressources.
- Je souhaite mieux interpréter les indicateurs avancés de performances : latence disque, attente CPU, pression mémoire et seuils d'alerte réellement adaptés, pourquoi pas faire un serveur zabbix pour surveiller plus précisement le tout.
- Je dois encore pratiquer une restauration complète de VM et une architecture sans point unique de panne, avec plusieurs hôtes physiques et un stockage redondant.

## Bilan personnel

Je sais désormais déployer et vérifier une VM, créer un cluster Proxmox, utiliser un stockage partagé, effectuer une migration, préparer la HA, segmenter un réseau et suivre une méthode de diagnostic. Le principal enseignement est qu'une infrastructure virtualisée fiable repose autant sur les dépendances physiques, les tests et la documentation que sur l'hyperviseur lui-même.
