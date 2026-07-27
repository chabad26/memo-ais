# Comment optimiser les performances d'une infrastructure virtualisée ?

## Mise en situation

Depuis la mise en production de la plateforme virtualisée, les utilisateurs signalent des ralentissements ponctuels sur certains services. L'objectif est d'identifier les ressources limitantes, de corriger les déséquilibres démontrés et de vérifier objectivement les résultats.

!!! question "Problématique"
    **Comment améliorer les performances sans déplacer le problème vers une autre ressource ni compromettre la disponibilité du cluster ?**

## Périmètre réel du laboratoire

Le scénario pédagogique évoque plusieurs VM, mais l'environnement actuellement disponible comprend :

- `PVE1`, `PVE2` et `PVE3`, trois VM Proxmox imbriquées dans Hyper-V ;
- `NFS1`, stockage partagé à l'adresse `10.42.0.134` ;
- `WEB1`, VM 100 et seule VM applicative encore présente ;
- `LABO_CORE`, hôte physique commun disposant d'environ 12 processeurs logiques et 15,8 Gio de RAM.

`WEB1` possède actuellement un processeur virtuel et 2 Gio de RAM. Les trois nœuds Proxmox partagent le même processeur, la même mémoire, le même vSwitch et le même stockage physique de `LABO_CORE`.

!!! warning "Interprétation des mesures"
    Une migration de `WEB1` entre `PVE1`, `PVE2` et `PVE3` déplace la charge entre des hyperviseurs logiques, mais pas vers un autre serveur physique. Une saturation de `LABO_CORE` affecte donc potentiellement les trois nœuds à la fois.

---

## Activité 1 — Étudier les performances

### Indicateurs essentiels

| Ressource | Indicateurs | Interprétation |
| --- | --- | --- |
| CPU | utilisation, charge, temps d'attente, fréquence, saturation prolongée | une pointe brève est normale ; une saturation durable accompagnée de latence indique un manque de capacité |
| Mémoire | mémoire utilisée/disponible, swap, ballooning, OOM, PSI mémoire | du cache Linux n'est pas automatiquement un manque de RAM ; le swap actif et la pression mémoire sont plus significatifs |
| Stockage | espace, inodes, latence, IOPS, débit, temps d'attente I/O | un stockage peu rempli peut néanmoins être lent |
| Réseau | débit, erreurs, pertes, retransmissions, latence | distinguer saturation du lien, perte de paquets et mauvaise configuration |
| VM | consommation réelle, ressources allouées, temps de réponse du service | comparer la demande de la VM à ses limites |
| Cluster | répartition des VM, quorum, migration, HA | une répartition homogène ne doit pas sacrifier les dépendances ou la réserve HA |
| Application | temps de réponse HTTP, taux d'erreur, disponibilité | mesure finale du point de vue utilisateur |

Les graphiques RRD de Proxmox offrent une tendance dans le temps. Une mesure instantanée avec `top` ou `free` doit être rapprochée de l'heure exacte du ralentissement.

### Risques du surengagement

Le surengagement consiste à attribuer aux VM plus de ressources virtuelles que la capacité physique immédiatement disponible.

#### Processeur

Attribuer de nombreux vCPU n'ajoute pas de puissance physique. En cas de demandes simultanées, les VM se disputent les cœurs et la latence augmente. Une VM dotée de trop de vCPU peut également être plus difficile à planifier par l'ordonnanceur.

#### Mémoire

Lorsque les besoins simultanés dépassent la RAM disponible, l'hôte peut compresser, récupérer de la mémoire, utiliser le swap ou déclencher l'arrêt de processus par l'OOM killer. Une pression mémoire sur un nœud Proxmox imbriqué s'ajoute à celle de la VM Hyper-V qui l'héberge.

#### Stockage et réseau

Plusieurs sauvegardes, migrations ou VM peuvent saturer le même disque NFS ou le même lien réseau. Corosync est particulièrement sensible à la latence : une saturation provoquée par une migration ou le stockage peut perturber le cluster.

#### Risque de disponibilité

Une plateforme remplie à 100 % peut fonctionner en régime normal tout en étant incapable de reprendre `WEB1` après la perte d'un nœud. L'optimisation doit conserver une réserve pour la haute disponibilité.

### Preuve de travail — Analyse du surengagement en cinq points

#### Situation constatée

Les trois nœuds Proxmox reçoivent chacun 3 Gio de RAM, soit 9 Gio attribués au total. Leur demande cumulée atteint environ 11,34 Gio :

- `PVE1` demande environ 3,72 Gio pour 3 Gio attribués ;
- `PVE2` demande environ 4,95 Gio pour 3 Gio attribués ;
- `PVE3` demande environ 2,67 Gio pour 3 Gio attribués.

La cause principale est l'imbrication des trois hyperviseurs et de leurs charges sur le même hôte physique `LABO_CORE`, limité à environ 15,8 Gio de RAM. `PVE2`, qui héberge `WEB1`, présente la pression la plus importante.

1. **Saturation de la mémoire**

   **Cause :** les besoins cumulés de `PVE1` et `PVE2` dépassent la mémoire qui leur est attribuée.  
   **Impact :** le système peut utiliser davantage le swap, ralentir les VM ou provoquer l'arrêt de processus si la mémoire devient insuffisante.  
   **Mesure corrective :** éviter de déployer une nouvelle charge sur `PVE2`, arrêter les systèmes inutiles et ajuster la RAM uniquement après avoir vérifié la marge disponible sur `LABO_CORE`.

2. **Contention du processeur**

   **Cause :** les trois hyperviseurs imbriqués, `NFS1` et les charges virtuelles utilisent les mêmes processeurs physiques.  
   **Impact :** les VM attendent plus longtemps avant d'obtenir du temps CPU, ce qui augmente le temps de réponse des services.  
   **Mesure corrective :** limiter le nombre de vCPU au besoin réel, supprimer les charges inutiles et décaler les opérations lourdes.

3. **Dégradation des performances du stockage**

   **Cause :** `WEB1`, les migrations et le stockage NFS reposent indirectement sur les ressources d'un même serveur physique.  
   **Impact :** une forte activité peut augmenter la latence des disques, ralentir `WEB1` et faire échouer une migration ou une sauvegarde.  
   **Mesure corrective :** planifier les migrations et sauvegardes en dehors des périodes de charge et surveiller l'attente d'entrées-sorties.

4. **Perturbation du réseau et du cluster**

   **Cause :** les flux des VM, de NFS, des migrations et de Corosync partagent la même infrastructure réseau physique.  
   **Impact :** une saturation peut augmenter la latence de Corosync, provoquer une perte temporaire de communication entre les nœuds et menacer le quorum.  
   **Mesure corrective :** séparer les flux par VLAN, éviter les migrations simultanées et réserver un réseau stable à Corosync dans une architecture de production.

5. **Perte de capacité de reprise**

   **Cause :** les ressources disponibles sont presque entièrement consommées en fonctionnement normal.  
   **Impact :** un autre nœud peut ne pas disposer de la mémoire ou du CPU nécessaires pour reprendre `WEB1` après une panne. La haute disponibilité devient alors théorique.  
   **Mesure corrective :** conserver une réserve permettant la perte d'un nœud, placer `WEB1` sur le nœud disposant de la meilleure marge et augmenter les ressources physiques pour toute évolution future.

!!! success "Conclusion de l'analyse"
    Le surengagement provient principalement du manque de mémoire et de l'empilement de plusieurs niveaux de virtualisation sur `LABO_CORE`. Il peut dégrader les performances de `WEB1`, perturber le stockage et réduire la capacité de reprise du cluster. La correction prioritaire consiste à réduire les charges simultanées et à ne pas ajouter de VM sur `PVE2`. Une augmentation de la RAM physique sera nécessaire avant une extension durable de l'infrastructure.

### Composants prioritaires

1. `LABO_CORE`, car il porte tous les composants imbriqués ;
2. la RAM des trois VM Proxmox ;
3. `NFS1`, utilisé par le disque de `WEB1` ;
4. le vSwitch Hyper-V et les interfaces virtuelles ;
5. le nœud qui exécute `WEB1` ;
6. les ressources et le service Apache dans `WEB1` ;
7. Corosync, dont la latence doit rester stable.

### Bonnes pratiques

- mesurer pendant une période représentative avant de modifier ;
- dimensionner selon les consommations observées et non au maximum théorique ;
- conserver une marge CPU, RAM et stockage pour la HA ;
- éviter d'exécuter simultanément migration, sauvegarde et charge intensive ;
- utiliser les pilotes VirtIO pour le disque et le réseau ;
- installer et activer le QEMU Guest Agent dans les VM compatibles ;
- utiliser un contrôleur SCSI VirtIO et `iothread` lorsque le contexte le justifie ;
- activer `discard` uniquement si toute la chaîne de stockage le prend en charge ;
- séparer autant que possible Corosync, stockage, migration et trafic des VM ;
- surveiller les tendances, fixer des seuils et centraliser les métriques ;
- ne pas déployer Ceph dans ce laboratoire : `nfs-shared` suffit et Ceph augmenterait fortement la consommation.

---

## Activité 2 — Évaluer l'état de santé

### 1. Établir un relevé avant optimisation

Effectuer les mesures avec `WEB1` en fonctionnement normal, puis répéter pendant un ralentissement si celui-ci est reproductible.

Sur chaque nœud Proxmox :

```bash
hostname
date
uptime
free -h
swapon --show
df -h
df -i
pvesm status
pvecm status
qm list
```

Pour observer l'activité pendant une minute :

```bash
vmstat 2 30
```

Interprétation rapide de `vmstat` :

- `r` durablement supérieur au nombre de vCPU : attente CPU probable ;
- `si` et `so` non nuls de façon répétée : activité swap ;
- `wa` élevé : attente de stockage ;
- `us` et `sy` élevés : CPU occupé par les applications ou le noyau.

### 2. Contrôler le processeur

```bash
nproc
lscpu
top
ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head
```

Dans Proxmox : **Nœud → Résumé → Utilisation CPU** et **VM 100 → Résumé**. Comparer une période courte, une journée et une semaine.

### 3. Contrôler la mémoire

```bash
free -h
grep -E 'MemAvailable|SwapTotal|SwapFree' /proc/meminfo
systemctl --failed
journalctl -k --since "-24 hours" |
  grep -Ei 'out of memory|oom|killed process'
```

Dans `WEB1` :

```bash
free -h
ps -eo pid,comm,%mem,%cpu --sort=-%mem | head
```

### 4. Contrôler le stockage

```bash
pvesm status
df -h
df -i
mount | grep nfs
findmnt -t nfs,nfs4
```

État déjà observé :

| Stockage | État | Utilisation relevée |
| --- | --- | ---: |
| `local` | actif | environ 20,17 % |
| `nfs-shared` | actif | environ 10,82 % |

L'espace disponible est satisfaisant au moment du relevé. Ce résultat ne mesure cependant ni la latence ni les IOPS.

Si `iostat` est déjà disponible :

```bash
command -v iostat >/dev/null && iostat -xz 2 10
```

Ne pas installer un paquet uniquement pendant un incident sans en documenter l'impact.

### 5. Contrôler le réseau

```bash
ip -s link
ip -br address
ip route
bridge vlan show
ss -s
ping -c 20 10.42.0.134
```

Rechercher les compteurs `errors`, `dropped`, une latence instable et une incohérence de MTU. Dans cette architecture imbriquée, vérifier également le vSwitch et les cartes réseau des VM Proxmox dans Hyper-V.

### 6. Contrôler la répartition

```bash
pvesh get /cluster/resources --type vm
qm list
ha-manager status
```

Avec une seule VM, il n'existe pas de déséquilibre applicatif significatif à corriger. Le choix du nœud doit principalement tenir compte de sa mémoire disponible, de son état et de la possibilité de maintenir le quorum.

### 7. Contrôler l'hôte Hyper-V

Depuis `LABO_CORE` :

```powershell
Get-VM |
  Select-Object `
    Name,
    State,
    CPUUsage,
    @{
      Name = "RAM attribuée (Gio)"
      Expression = {
        [math]::Round(
          $_.MemoryAssigned / 1GB,
          2
        )
      }
    },
    @{
      Name = "RAM demandée (Gio)"
      Expression = {
        [math]::Round(
          $_.MemoryDemand / 1GB,
          2
        )
      }
    },
    Uptime
```

Les chemins `Get-Counter` sont traduits sur Windows français. Pour éviter l'erreur « objet spécifié introuvable », utiliser les classes CIM, indépendantes de la langue :

```powershell
Get-CimInstance Win32_Processor |
  Measure-Object LoadPercentage -Average |
  Select-Object @{
    Name = "CPU moyen (%)"
    Expression = {
      [math]::Round($_.Average, 2)
    }
  }

Get-CimInstance Win32_OperatingSystem |
  Select-Object `
    @{
      Name = "RAM totale (Gio)"
      Expression = {
        [math]::Round(
          $_.TotalVisibleMemorySize / 1MB,
          2
        )
      }
    },
    @{
      Name = "RAM disponible (Gio)"
      Expression = {
        [math]::Round(
          $_.FreePhysicalMemory / 1MB,
          2
        )
      }
    }

Get-CimInstance `
  Win32_PerfFormattedData_PerfDisk_PhysicalDisk |
  Select-Object `
    Name,
    AvgDisksecPerTransfer,
    DiskBytesPersec

Get-CimInstance `
  Win32_PerfFormattedData_Tcpip_NetworkInterface |
  Select-Object `
    Name,
    BytesTotalPersec,
    PacketsReceivedErrors,
    PacketsOutboundErrors
```

Ce relevé est indispensable : Proxmox ne peut pas voir directement la contention imposée par les autres VM Hyper-V.

### Premier constat sur `LABO_CORE`

Le relevé Hyper-V obtenu montre :

| VM Hyper-V | RAM attribuée | RAM demandée | Analyse |
| --- | ---: | ---: | --- |
| `NFS1` | 0,50 Gio | environ 0,20 Gio | marge disponible |
| `PVE1` | 3 Gio | environ 3,72 Gio | demande supérieure à l'allocation |
| `PVE2` | 3 Gio | environ 4,95 Gio | pression mémoire importante |
| `PVE3` | 3 Gio | environ 2,67 Gio | allocation actuellement suffisante |

`PVE2` héberge la VM Proxmox 100 `WEB1`, ce qui explique probablement sa demande supérieure. La VM Hyper-V nommée `WEB1` est arrêtée : elle correspond à l'ancienne VM directe et non à la VM 100 imbriquée dans Proxmox.

!!! warning "Déséquilibre identifié"
    L'ensemble des nœuds Proxmox reçoit 9 Gio, mais leur demande cumulée atteint environ 11,34 Gio. Ajouter des conteneurs sur `PVE2` aggraverait la pression. Placer les LXC de test sur `PVE3`, ou migrer `WEB1` vers le nœud offrant la meilleure marge, avant d'augmenter les allocations.

### Tableau d'analyse

| Composant | Mesure | Valeur avant | Seuil ou comparaison | Conclusion |
| --- | --- | --- | --- | --- |
| `LABO_CORE` | CPU moyen/pointe | | tendance | |
| `LABO_CORE` | mémoire disponible | | marge pour Hyper-V | |
| Nœud hébergeant `WEB1` | charge et mémoire | | autres nœuds | |
| `WEB1` | CPU et RAM | | ressources allouées | |
| `nfs-shared` | espace et latence | | avant/après | |
| Réseau | pertes et latence | | état normal | |
| Apache | temps de réponse | | avant/après | |

### Déséquilibres probables

Dans ce laboratoire, les risques les plus plausibles sont :

- RAM totale insuffisante sur `LABO_CORE` ;
- concurrence CPU entre Hyper-V, les trois PVE, `NFS1` et `WEB1` ;
- double virtualisation ajoutant de la latence ;
- trafic cluster, NFS, migration et VM sur le même support physique ;
- mesure trompeuse donnant trois nœuds logiques alors qu'un seul hôte fournit les ressources ;
- allocation excessive à `WEB1` qui priverait les nœuds Proxmox de leur faible marge.

---

## Activité 3 — Mettre en œuvre et comparer

### Principe de décision

Une ressource ne doit être augmentée que si les mesures démontrent qu'elle limite le service. Pour `WEB1`, la configuration actuelle d'un vCPU et de 2 Gio est cohérente avec un serveur Apache léger. L'ajout automatique de vCPU ou de RAM n'est donc pas retenu sans preuve de saturation.

### Optimisations adaptées au laboratoire

#### Option 0 — Simuler des postes avec des conteneurs LXC

Des conteneurs LXC Debian ou Alpine permettent de simuler plusieurs clients ou services sans déployer de nouvelles VM complètes. Ils sont adaptés aux tests réseau, DNS, HTTP, VLAN et pare-feu.

Dimensionnement proposé :

| Conteneur | Rôle simulé | VLAN | vCPU | RAM | Disque |
| --- | --- | ---: | ---: | ---: | ---: |
| `CT201` | client utilisateur | 50 | 1 | 256 Mio | 2 Gio |
| `CT202` | serveur interne de test | 20 | 1 | 256 Mio | 2 Gio |

Un seul conteneur client peut suffire pour tester l'accès à `WEB1`. Le second ne doit être créé que si la mémoire de `LABO_CORE` le permet.

Dans Proxmox :

1. ouvrir un stockage acceptant les modèles de conteneurs ;
2. télécharger un modèle Debian ou Alpine ;
3. créer un conteneur non privilégié ;
4. sélectionner `vmbr0` ;
5. affecter le tag VLAN prévu ;
6. limiter le conteneur à un vCPU et 256 Mio de RAM ;
7. placer son disque sur un stockage compatible avec les migrations attendues.

Contrôles en ligne de commande :

```bash
pveam available |
  grep -E 'debian|alpine'
pct list
pct config 201
pct status 201
```

!!! warning "Créer le conteneur avant `pct set`"
    `pct set 201` modifie un conteneur existant ; cette commande ne crée pas le CT. Si `nodes/pve1/lxc/201.conf does not exist` apparaît, créer d'abord le conteneur 201.

Procédure simple dans l'interface :

1. **local (pve1) → CT Templates → Templates** ;
2. télécharger un modèle Debian ou Alpine ;
3. cliquer sur **Créer un conteneur** ;
4. utiliser l'ID `201`, un nom d'hôte et un mot de passe non documenté ;
5. sélectionner le modèle téléchargé ;
6. allouer 2 Gio de disque, un vCPU et 256 Mio de RAM ;
7. configurer `vmbr0`, le VLAN 50 et DHCP ;
8. terminer la création puis vérifier avec `pct config 201`.

Exemple de configuration réseau **après création** du conteneur :

```bash
pct set 201 \
  -net0 name=eth0,bridge=vmbr0,tag=50,ip=dhcp,firewall=1
```

Si aucun serveur DHCP n'existe dans le VLAN 50, utiliser une adresse statique correspondant au plan réellement déployé :

```bash
pct set 201 \
  -net0 name=eth0,bridge=vmbr0,tag=50,ip=10.42.50.201/24,gw=10.42.50.1,firewall=1
```

!!! warning "Limites des LXC"
    Un conteneur partage le noyau Linux du nœud Proxmox. Il ne reproduit donc pas fidèlement un poste Windows, un démarrage de VM, un pilote matériel ou la consommation d'un système complet. Il convient néanmoins très bien pour générer une charge légère et valider la segmentation.

#### Option 1 — Réduire la concurrence

- arrêter les VM Hyper-V qui ne sont pas nécessaires à l'exercice ;
- ne conserver que `PVE1`, `PVE2`, `PVE3`, `NFS1` et `WEB1` ;
- décaler sauvegardes et migrations hors des périodes de mesure ;
- ne pas déployer d'OSD Ceph.

#### Option 2 — Déplacer `WEB1`

Si le nœud courant est réellement plus chargé qu'un autre :

```bash
# Contrôler avant toute migration
pvecm status
pvesm status
qm status 100

# Exemple : migrer vers pve1
qm migrate 100 pve1 --online
```

La cible doit être remplacée par le nœud possédant la meilleure marge mesurée. Dans ce cluster imbriqué, le bénéfice restera limité puisque les trois nœuds utilisent `LABO_CORE`.

#### Option 3 — Ajuster `WEB1`

Afficher d'abord la configuration :

```bash
qm config 100
```

Exemples, uniquement si les mesures le justifient :

```bash
# Deux vCPU si le CPU de WEB1 est durablement saturé
qm set 100 --cores 2

# 2 Gio fixes avec ballooning à 1 Gio si le pilote est fonctionnel
qm set 100 --memory 2048 --balloon 1024
```

!!! warning "Ballooning"
    Le ballooning nécessite le pilote approprié dans la VM. Avec seulement 2 Gio et un laboratoire très contraint, une limite minimale trop basse peut dégrader Apache. Tester sous charge avant de conserver ce réglage.

### Mesure du service avant et après

Depuis un poste pouvant atteindre `WEB1` :

```powershell
1..10 | ForEach-Object {
  $Mesure = Measure-Command {
    Invoke-WebRequest "http://10.42.0.125" `
      -UseBasicParsing |
      Out-Null
  }

  [pscustomobject]@{
    Essai = $_
    Millisecondes = [math]::Round(
      $Mesure.TotalMilliseconds,
      2
    )
  }
}
```

Depuis Linux :

```bash
for i in $(seq 1 10); do
  curl -o /dev/null -s \
    -w 'code=%{http_code} total=%{time_total}s\n' \
    http://10.42.0.125/
done
```

Réaliser les mesures dans des conditions comparables : même poste, même URL, même nombre d'essais et absence de migration ou sauvegarde concurrente.

### Comparaison

| Indicateur | Avant | Après | Évolution | Conclusion |
| --- | ---: | ---: | ---: | --- |
| Temps HTTP moyen | | | | |
| Temps HTTP maximal | | | | |
| CPU de `WEB1` | | | | |
| RAM disponible dans `WEB1` | | | | |
| CPU du nœud | | | | |
| RAM du nœud | | | | |
| Latence vers `NFS1` | | | | |
| CPU de `LABO_CORE` | | | | |
| RAM disponible sur `LABO_CORE` | | | | |

Une amélioration n'est validée que si elle est reproductible et ne dégrade ni le quorum, ni NFS, ni les autres ressources.

## Conclusion proposée

### Optimisations réalisées

À compléter avec les seules actions réellement appliquées : arrêt des charges inutiles, migration de `WEB1`, modification de CPU/RAM ou planification des tâches.

### Bénéfices

- réduction de la contention mesurée ;
- temps de réponse plus stable ;
- meilleure marge pour les nœuds et la haute disponibilité ;
- comportement plus prévisible lors des migrations.

### Limites

- tous les nœuds dépendent du même `LABO_CORE` ;
- la migration ne change pas d'hôte physique ;
- les ressources sont trop faibles pour reproduire une infrastructure de production ;
- une seule VM ne permet pas d'étudier un véritable équilibrage multi-charge ;
- le NFS et les réseaux ne sont pas physiquement redondants.

### Recommandations

- déployer les nœuds Proxmox sur trois serveurs physiques distincts ;
- dimensionner le cluster avec une réserve permettant la perte d'un nœud ;
- séparer les réseaux Corosync, stockage, migration et VM ;
- superviser l'hôte, les nœuds, NFS et les services applicatifs ;
- définir des seuils et conserver un historique de capacité ;
- tester les changements sur une période représentative ;
- prévoir l'augmentation de RAM de `LABO_CORE` si le laboratoire doit accueillir d'autres VM ;
- préférer une optimisation mesurée à une augmentation systématique des ressources.

## Preuves à intégrer

- graphiques CPU et mémoire avant optimisation ;
- état de `WEB1` et configuration `qm config 100` ;
- occupation de `local` et `nfs-shared` ;
- mesures réseau et latence NFS ;
- répartition des VM ;
- ressources Hyper-V de `LABO_CORE` ;
- action d'optimisation réalisée ;
- même série de mesures après modification ;
- tableau comparatif et conclusion.

## Références officielles

- [Proxmox VE — Administration Guide](https://pve.proxmox.com/pve-docs/pve-admin-guide.pdf)
- [Proxmox VE — qm](https://pve.proxmox.com/pve-docs/qm.1.html)
- [Proxmox VE — Cluster Manager](https://pve.proxmox.com/pve-docs/chapter-pvecm.html)
- [Proxmox VE — pvesm](https://pve.proxmox.com/pve-docs/pvesm.1.html)
- [Proxmox VE — Network Configuration](https://pve.proxmox.com/wiki/Network_Configuration)
