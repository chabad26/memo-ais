# Atelier 1 - Découverte de Zeek et architecture d'analyse réseau

## Objectif

Cet atelier a pour objectif de découvrir Zeek et de l'intégrer dans l'infrastructure de TP afin d'observer le trafic réseau du groupe.

Zeek est une plateforme d'analyse réseau et de supervision de sécurité. Contrairement à un pare-feu, Zeek ne bloque pas le trafic. Il observe les communications, les analyse et génère des journaux détaillés.

Zeek est utilisé pour :

- détecter des comportements anormaux ;
- identifier des scans réseau ;
- analyser des connexions suspectes ;
- produire des logs exploitables pour l'investigation ;
- comprendre les échanges réseau sans lire manuellement chaque paquet.

## Zeek, pfSense et Wireshark

Zeek ne joue pas le même rôle qu'un firewall ou qu'un analyseur paquet classique.

| Outil | Rôle principal | Exemple d'utilisation |
| --- | --- | --- |
| pfSense | Filtrer, autoriser, bloquer et journaliser les décisions firewall | Autoriser ICMP de VLAN 10 vers VLAN 20 |
| Wireshark | Observer précisément les paquets un par un | Lire une trame ARP, ICMP, TCP ou OpenVPN |
| Zeek | Produire automatiquement des événements et logs réseau | Lister les connexions, DNS, HTTP, scans et anomalies |

Wireshark est utile pour observer précisément les paquets. Zeek est utile pour transformer le trafic en journaux structurés exploitables.

## Principe de fonctionnement

Zeek observe le trafic qui passe sur une interface réseau. Il analyse les protocoles et écrit des fichiers de logs.

Exemples de logs courants :

| Fichier | Contenu |
| --- | --- |
| `conn.log` | Connexions observées : IP source, IP destination, ports, protocole, durée |
| `dns.log` | Requêtes DNS observées |
| `http.log` | Requêtes HTTP observées si du trafic HTTP est visible |
| `ssl.log` | Informations sur les connexions TLS observées |
| `weird.log` | Événements réseau inhabituels |
| `notice.log` | Alertes ou événements notables |

Le fichier le plus important pour commencer est `conn.log`, car il donne une vue synthétique des communications réseau.

## Architecture attendue

Le lab reprend l'infrastructure déjà construite :

```text
VLAN 10 Administration
VLAN 20 Production
pfSense
Kali Linux
machines Linux
machine Zeek
OpenVPN si actif
```

La machine Zeek doit pouvoir observer du trafic. Elle peut être déplacée selon l'objectif du test.

## Choisir l'emplacement de la machine Zeek

Le placement de Zeek dépend de ce que l'on veut observer.

| Emplacement | Ce que Zeek peut voir | Limite |
| --- | --- | --- |
| Dans le VLAN 10 | Trafic local du VLAN 10 visible depuis ce segment | Ne voit pas forcément VLAN 20 |
| Dans le VLAN 20 | Trafic local du VLAN 20 visible depuis ce segment | Ne voit pas forcément VLAN 10 |
| Entre pfSense et un switch | Flux inter-VLAN qui passent par pfSense selon la topologie | Nécessite un bon branchement ou une duplication de trafic |
| Sur le réseau de transit OpenVPN | Flux OpenVPN chiffré | Ne voit pas directement les flux internes chiffrés |
| Sur une interface miroir / SPAN | Trafic copié depuis un port ou VLAN choisi | Demande une configuration de switch adaptée |

Dans GNS3, si aucun port miroir n'est disponible, il est possible de déplacer temporairement la machine Zeek sur différents segments pour comparer les observations.

## Déroulement

### 1. Identifier la machine Zeek

Choisir une machine Linux qui sera utilisée comme capteur Zeek.

À documenter :

| Élément | Valeur |
| --- | --- |
| Nom de la machine Zeek | À compléter |
| Interface d'observation | À compléter |
| Segment observé | À compléter |
| Adresse IP de la machine | À compléter |
| Rôle dans le lab | Capteur réseau |

### 2. Vérifier les interfaces disponibles

Sur la machine Zeek :

```bash
ip -br addr
ip link
ip route
```

Identifier :

- l'interface de gestion ;
- l'interface d'observation ;
- le VLAN ou segment sur lequel la machine est connectée ;
- la passerelle utilisée si nécessaire.

Si la machine possède deux interfaces, une interface peut être utilisée pour l'administration et l'autre pour l'observation.

### 3. Vérifier la connectivité de base

Depuis la machine Zeek :

```bash
ping -c 3 <passerelle_du_segment>
ping -c 3 <machine_du_meme_vlan>
```

Depuis une autre machine du lab, générer du trafic :

```bash
ping -c 3 <adresse_cible>
curl http://<adresse_cible>
ssh <utilisateur>@<adresse_cible>
```

Les commandes exactes dépendent des services disponibles dans le lab.

### 4. Vérifier les VLANs, le routage et pfSense

Avant d'interpréter les logs Zeek, vérifier que l'infrastructure fonctionne :

| Élément | Vérification |
| --- | --- |
| VLAN 10 | Les machines du VLAN 10 ont une IP cohérente |
| VLAN 20 | Les machines du VLAN 20 ont une IP cohérente |
| pfSense | Les interfaces et règles attendues sont présentes |
| Routage | Les passerelles répondent |
| Filtrage | Les flux autorisés passent, les flux interdits sont bloqués |
| OpenVPN | Si actif, le tunnel et les routes sont fonctionnels |

Commandes utiles :

```bash
ip route
ping -c 3 <passerelle_vlan>
traceroute <adresse_cible>
```

Dans pfSense :

```text
Firewall > Rules
Status > System Logs > Firewall
```

### 5. Installer Zeek

Sur Debian ou Ubuntu, une installation simple peut être faite avec les paquets disponibles :

```bash
sudo apt update
sudo apt install zeek -y
```

Selon la distribution, le paquet peut aussi s'appeler différemment ou nécessiter le dépôt officiel Zeek. Si `apt install zeek` ne fonctionne pas, consulter la documentation officielle :

```text
https://docs.zeek.org/
```

Vérifier l'installation :

```bash
zeek --version
which zeek
```

### 6. Lancer une première analyse en direct

Créer un dossier de travail :

```bash
mkdir -p ~/zeek-lab
cd ~/zeek-lab
```

Lancer Zeek sur l'interface d'observation :

```bash
sudo zeek -i <interface>
```

Exemple :

```bash
sudo zeek -i ens3
```

Pendant que Zeek tourne, générer du trafic depuis une autre machine :

```bash
ping -c 3 <adresse_cible>
curl http://<adresse_cible>
```

Arrêter Zeek avec :

```text
Ctrl + C
```

Lister les logs générés :

```bash
ls -lh
```

Les premiers fichiers attendus sont souvent :

```text
conn.log
packet_filter.log
loaded_scripts.log
```

Selon le trafic observé, d'autres fichiers peuvent apparaître : `dns.log`, `http.log`, `ssl.log`, `weird.log`.

### 7. Lire les logs Zeek

Afficher les connexions :

```bash
less conn.log
```

Ou en colonnes plus lisibles :

```bash
zeek-cut id.orig_h id.orig_p id.resp_h id.resp_p proto service duration conn_state < conn.log
```

Champs utiles dans `conn.log` :

| Champ | Signification |
| --- | --- |
| `id.orig_h` | Adresse IP source |
| `id.orig_p` | Port source |
| `id.resp_h` | Adresse IP destination |
| `id.resp_p` | Port destination |
| `proto` | Protocole, par exemple TCP, UDP ou ICMP |
| `service` | Service reconnu, par exemple DNS, HTTP, SSH |
| `duration` | Durée de la connexion |
| `conn_state` | État de la connexion |

Exemple :

```bash
zeek-cut ts id.orig_h id.resp_h id.resp_p proto service conn_state < conn.log
```

### 8. Comparer avec Wireshark

Faire une capture Wireshark sur le même segment que Zeek.

Comparer :

| Question | Wireshark | Zeek |
| --- | --- | --- |
| Quels paquets précis sont visibles ? | Oui | Non, pas paquet par paquet |
| Quelle machine parle à quelle machine ? | Oui | Oui, dans `conn.log` |
| Quels ports sont utilisés ? | Oui | Oui |
| Le service est-il identifié ? | Par analyse manuelle | Souvent automatiquement |
| Peut-on produire un résumé exploitable ? | Manuellement | Oui, via les logs |

L'objectif est de comprendre que Wireshark et Zeek sont complémentaires.

## Tests proposés

### Test 1 : ICMP entre deux machines

Depuis une machine du VLAN 10 :

```bash
ping -c 5 <machine_ou_passerelle>
```

Dans Zeek :

```bash
zeek-cut id.orig_h id.resp_h proto service conn_state < conn.log
```

Observation attendue :

- présence d'un flux ICMP ;
- IP source et destination visibles ;
- état de connexion renseigné dans `conn.log`.

### Test 2 : connexion SSH

Depuis une machine autorisée :

```bash
ssh <utilisateur>@<adresse_cible>
```

Dans Zeek :

```bash
zeek-cut id.orig_h id.resp_h id.resp_p proto service conn_state < conn.log
```

Observation attendue :

- port destination `22` ;
- protocole TCP ;
- service `ssh` si Zeek l'identifie ;
- connexion visible même si le contenu SSH est chiffré.

### Test 3 : scan simple depuis Kali

Depuis Kali :

```bash
nmap -sS <adresse_cible>
```

ou plus simplement :

```bash
nmap <adresse_cible>
```

Dans Zeek, rechercher :

```bash
ls
less conn.log
less notice.log
```

Selon la configuration et le trafic, Zeek peut produire des traces dans `conn.log` et parfois dans `notice.log`.

## Cas OpenVPN actif

Si OpenVPN est actif, le placement de Zeek change ce qu'il voit.

| Placement de Zeek | Observation |
| --- | --- |
| Réseau externe entre client VPN et R2 | Flux OpenVPN chiffré, port UDP/1194 |
| Côté `tun0` ou réseau interne après R2 | Communications internes après décapsulation |
| Derrière pfSense côté VLAN | Trafic autorisé vers les VLANs |

Si Zeek observe seulement le réseau de transit OpenVPN, il ne verra pas directement les communications applicatives internes. Il verra principalement :

- IP physique du client VPN ;
- IP de R2 ;
- UDP/1194 ;
- volume et durée des échanges ;
- pas le contenu applicatif interne.

## Documentation de l'architecture d'analyse

Compléter le tableau suivant :

| Élément | Réponse |
| --- | --- |
| Machine utilisée pour Zeek | À compléter |
| Interface observée | À compléter |
| Segment observé | À compléter |
| Trafic attendu | À compléter |
| Trafic réellement observé | À compléter |
| VLANs visibles | À compléter |
| pfSense traversé ? | Oui / Non |
| OpenVPN actif ? | Oui / Non |
| Logs Zeek générés | À compléter |
| Limites de l'observation | À compléter |

## Captures à ajouter

Les captures suivantes pourront être ajoutées après réalisation :

| Capture | Emplacement conseillé |
| --- | --- |
| Topologie GNS3 avec machine Zeek | Architecture attendue |
| `ip -br addr` sur la machine Zeek | Vérification des interfaces |
| Lancement de `sudo zeek -i <interface>` | Première analyse en direct |
| Liste des logs générés | Après lancement de Zeek |
| Extrait de `conn.log` | Lecture des logs |
| Comparaison Wireshark / Zeek | Comparaison avec Wireshark |
| Scan Kali visible dans Zeek | Tests proposés |

## Résultat attendu

À la fin de l'atelier, le groupe doit avoir :

- identifié une machine Zeek ;
- choisi et justifié son emplacement réseau ;
- vérifié que Zeek observe du trafic ;
- généré au moins un `conn.log` ;
- relié les observations aux VLANs, à pfSense et au VPN si actif ;
- documenté les limites de visibilité selon l'emplacement de Zeek.

## Ressources

- Zeek Documentation : <https://docs.zeek.org/>
- Zeek logs : <https://docs.zeek.org/en/current/logs/index.html>
