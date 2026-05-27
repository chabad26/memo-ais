# Fondations TCP/IP et adressage

l'itération est coupé en 2 modules distinct:

## bloc 1

📌 Au programme de ce bloc

Comprendre comment les données voyagent sur un réseau (modèle TCP/IP, 7 protocoles fondamentaux, encapsulation), observer ces protocoles en action sur des captures Wireshark réelles, puis maîtriser l'adressage IPv4 et le découpage CIDR jusqu'à produire un plan d'adressage pour AlpesNet.

## bloc 2

📌 Au programme de ce bloc

Apprendre à produire un schéma réseau professionnel (L1/L2/L3), implémenter la topologie AlpesNet dans GNS3 à partir du plan d'adressage du J1, puis produire en autonomie le schéma annoté complet de l'infrastructure — premier livrable RNCP du module. Débrief collectif en fin de journée.

## Pré-requis : outils à installer

Avant de commencer les travaux pratiques, deux outils doivent être installés sur Ubuntu 24.04 : GNS3 pour simuler les équipements réseau et Wireshark pour analyser les captures de trafic.

### GNS3 — Simulateur réseau

GNS3 (Graphical Network Simulator 3) permet de construire des topologies réseau réalistes et d'exécuter de vraies images Cisco IOS. Il est plus proche d'un environnement de production que Packet Tracer, car les commandes, limitations et comportements viennent directement des systèmes Cisco utilisés.

- Site officiel : <https://www.gns3.com>
- Documentation : <https://docs.gns3.com>

Installation :

```bash
sudo add-apt-repository ppa:gns3/ppa
sudo apt update
sudo apt install gns3-gui gns3-server
sudo usermod -aG ubridge,libvirt,kvm,wireshark $USER
```

Pendant l'installation, répondre **Oui** aux questions autorisant les utilisateurs non administrateurs à capturer des paquets et à utiliser Wireshark. Il faut ensuite se déconnecter puis se reconnecter pour activer les groupes.

Vérification :

```bash
gns3 --version
groups $USER
```

Au premier lancement avec `gns3`, choisir **Run the topologies on my local computer**. Si l'état passe à **Connected**, l'installation est fonctionnelle.

Les fichiers nécessaires pour les images et appliances GNS3 sont à télécharger ici :

- Images Cisco pour GNS3 : <https://files.repinger.com/misc/cisco_gns3/>
- Image de configuration IOSv : <https://sourceforge.net/projects/gns-3/files/Qemu%20Appliances/IOSv_startup_config.img/download>
- Appliance Cisco IOSvL2 : <https://www.gns3.com/gns3/appliance/download?url=https%3A%2F%2Fraw.githubusercontent.com%2FGNS3%2Fgns3-registry%2Fmaster%2Fappliances%2Fcisco-iosvl2.gns3a>
- Appliance Cisco vWLC : <https://www.gns3.com/gns3/appliance/download?url=https%3A%2F%2Fraw.githubusercontent.com%2FGNS3%2Fgns3-registry%2Fmaster%2Fappliances%2Fcisco-vWLC.gns3a>

Dans GNS3, importer les images via **Edit > Preferences > Dynamips > IOS Routers > New**, puis sélectionner le fichier fourni. Laisser la RAM proposée et lancer **Idle-PC finder**.

Pour vérifier que tout fonctionne, créer un projet `test-install`, ajouter un routeur IOSv et un VPCS, les relier avec un câble, puis démarrer les équipements. Si la console du routeur affiche `Router>` en moins de 90 secondes, GNS3 est prêt.

> Les images Cisco sont propriétaires et doivent être utilisées uniquement dans le cadre pédagogique prévu.

Ressources utiles :

- Installation Ubuntu : <https://docs.gns3.com/docs/getting-started/installation/linux/>
- Premier projet : <https://docs.gns3.com/docs/using-gns3/beginners/the-gns3-gui>
- Forum : <https://community.gns3.com>

### Wireshark — Analyseur de trafic réseau

Wireshark sert à capturer et analyser le trafic réseau en temps réel. Il permet d'observer concrètement les protocoles étudiés : ICMP, ARP, DNS, DHCP, TCP, OSPF, etc.

- Site officiel : <https://www.wireshark.org>

Installation :

```bash
sudo apt install wireshark tshark
sudo usermod -aG wireshark $USER
```

Pendant l'installation, répondre **Oui** à la question autorisant les utilisateurs non administrateurs à capturer des paquets. Il faut ensuite se déconnecter puis se reconnecter.

Vérification :

```bash
groups $USER | grep wireshark
wireshark --version
```

Commandes utiles :

```bash
wireshark
wireshark fichier.pcapng
tshark -i eth0 -w capture.pcapng
```

L'interface Wireshark contient trois zones principales : la liste des paquets, le détail du paquet sélectionné et les données brutes en hexadécimal.

Filtres essentiels :

| Filtre | Affiche |
| --- | --- |
| `icmp` | Pings |
| `tcp` | Trafic TCP |
| `dns` | Requêtes et réponses DNS |
| `arp` | Résolution d'adresses ARP |
| `bootp` | DHCP |
| `ospf` | Trafic de routage OSPF |
| `ip.addr == 192.168.10.1` | Trafic impliquant cette adresse IP |

Ressources utiles :

- Guide officiel : <https://www.wireshark.org/docs/wsug_html_chunked/>
- Référence des filtres : <https://www.wireshark.org/docs/dfref/>
- Captures d'exemple : <https://wiki.wireshark.org/SampleCaptures>
- Pages manuelles : `man wireshark`, `man tshark`

### Outils réseau complémentaires

Installer aussi les utilitaires réseau utilisés pendant le module :

```bash
sudo apt install net-tools ipcalc nmap traceroute mtr dnsutils bind9-utils
```

| Outil | Utilisation | Usage |
| --- | --- | --- |
| `ipcalc` | J1-J2 | Vérifier les calculs de sous-réseaux |
| `traceroute`, `mtr` | J7-J8 | Tracer une route et diagnostiquer un chemin réseau |
| `nslookup`, `dig` | J6-J7 | Tester la résolution DNS |
| `nmap` | Diagnostics réseau | Scanner des hôtes et ports ouverts |

Commandes Ubuntu à connaître :

| Commande | Usage | Exemple |
| --- | --- | --- |
| `ip addr show` | Afficher les interfaces et adresses IP | `ip addr show eth0` |
| `ip link show` | Vérifier l'état UP/DOWN des interfaces | `ip link show` |
| `ip route show` | Afficher la table de routage | `ip route show` |
| `ip neigh show` | Afficher le cache ARP | `ip neigh show` |
| `ping -c N` | Tester la connectivité | `ping -c 4 8.8.8.8` |
| `traceroute` | Tracer le chemin vers une destination | `traceroute 8.8.8.8` |
| `ss -tulnp` | Afficher les ports ouverts | `ss -tulnp` |
| `ipcalc` | Calculer ou vérifier un sous-réseau | `ipcalc 192.168.10.0/26` |

Ressources utiles :

- Ubuntu Server Networking : <https://ubuntu.com/server/docs/network-configuration>
- Référence iproute2 : <https://baturin.org/docs/iproute2/>
- Pages manuelles : `man ip`, `man ss`, `man ping`, `man traceroute`

### Console série RS232

La console série RS232 sera utilisée en J3 pour les switchs physiques et en J7 pour les captures physiques. Installer les outils à l'avance évite de perdre du temps pendant les séances.

```bash
sudo apt install screen minicom
```

Après avoir branché l'adaptateur USB-RS232, vérifier le port détecté :

```bash
ls /dev/ttyUSB*
dmesg | tail -5
```

Connexion à une console Cisco :

```bash
screen /dev/ttyUSB0 9600
```

Pour quitter `screen` : `Ctrl+A`, puis `K`.

Paramètres Cisco standard : 9600 bauds, 8 bits, aucune parité, 1 bit d'arrêt, aucun contrôle de flux.

Si le port série n'apparaît pas :

```bash
lsmod | grep -E "ch341|cp210x"
sudo modprobe ch341
```

Ressources utiles : `man screen`, `man minicom`.

### Standard de documentation

Tout fichier de configuration produit dans ce module doit commencer par l'en-tête suivant :

```text
! ============================================================
! Auteur     : [Prénom NOM]
! Date       : [YYYY-MM-DD]
! Équipement : [Nom - type]
! Module     : RES-01a
! Objet      : [Description en une ligne]
! Version    : 1.0
! ============================================================
```
