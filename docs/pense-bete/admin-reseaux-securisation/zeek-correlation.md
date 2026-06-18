# Zeek, scans et corrélation

## Rôle de Zeek

Zeek est un capteur d'analyse réseau. Il transforme le trafic observé en journaux structurés.

| Outil | Rôle |
|---|---|
| pfSense | Filtrer, autoriser, bloquer et journaliser les décisions firewall |
| Wireshark | Lire les paquets en détail |
| Zeek | Produire des logs exploitables : connexions, DNS, HTTP, SSH, anomalies |

Phrase à retenir : **Zeek décrit ce qu'il voit, il ne bloque pas le trafic**.

## Placement du capteur

Zeek ne voit que le trafic qui arrive sur son interface.

| Placement | Ce que Zeek peut voir | Limite |
|---|---|---|
| VLAN 10 | Trafic visible depuis le VLAN 10 | Ne voit pas forcément le VLAN 20 |
| VLAN 20 | Trafic visible depuis le VLAN 20 | Ne voit pas forcément le VLAN 10 |
| Entre pfSense et le switch | Flux inter-VLAN selon la topologie | Demande un bon branchement ou une duplication de trafic |
| Réseau OpenVPN | Tunnel et flux VPN visibles sur le segment | Le contenu interne peut rester chiffré |
| Port miroir / hub / SPAN | Trafic copié vers Zeek | Dépend de la configuration du switch ou de GNS3 |

Réflexe : si Zeek ne produit pas le log attendu, vérifier d'abord le placement et l'interface capturée.

## Installation et lancement rapide

Vérifier les interfaces :

```bash
ip -br addr
ip link
ip route
```

Vérifier que l'interface reçoit du trafic :

```bash
sudo tcpdump -i ens3 -n
```

Lancer Zeek dans un dossier de travail :

```bash
mkdir -p ~/zeek-lab
cd ~/zeek-lab
sudo /opt/zeek/bin/zeek -i ens3
```

Arrêter avec `Ctrl + C`, puis lister les logs :

```bash
ls -lh
```

Selon le mode utilisé, les logs peuvent aussi se trouver dans :

```bash
logs/current/
```

## Logs Zeek essentiels

| Log | Utilité |
|---|---|
| `conn.log` | Connexions : IP, ports, protocole, service, durée, état |
| `dns.log` | Requêtes et réponses DNS |
| `http.log` | Requêtes HTTP visibles |
| `ssh.log` | Connexions SSH observées |
| `ssl.log` | Connexions TLS observées |
| `weird.log` | Événements réseau inhabituels |
| `notice.log` | Alertes ou événements notables si générés |

Le premier fichier à lire est souvent `conn.log`.

## Lire `conn.log`

Extraction lisible avec `zeek-cut` :

```bash
zeek-cut id.orig_h id.orig_p id.resp_h id.resp_p proto service duration conn_state < conn.log
```

Champs utiles :

| Champ | Sens |
|---|---|
| `id.orig_h` | IP source |
| `id.orig_p` | Port source |
| `id.resp_h` | IP destination |
| `id.resp_p` | Port destination |
| `proto` | Protocole : TCP, UDP, ICMP |
| `service` | Service reconnu : DNS, HTTP, SSH |
| `duration` | Durée de la connexion |
| `conn_state` | État de la connexion |

États fréquents :

| État | Interprétation rapide |
|---|---|
| `SF` | Connexion établie et terminée normalement |
| `S0` | SYN vu, pas de réponse complète |
| `REJ` | Connexion refusée |
| `RSTO` | Connexion réinitialisée par l'origine |
| `OTH` | Échange incomplet ou difficile à reconstruire |

## Filtres rapides

```bash
grep "192.168.20.10" conn.log
grep "192.168.10.100" conn.log
grep "192.168.20.10" conn.log | grep "tcp"
grep -i scan notice.log
cat http.log
cat ssh.log
cat dns.log
```

Filtrer par port avec `awk` :

```bash
awk '$6=="80"' conn.log
```

## Générer du trafic de test

Depuis Kali ou une machine de test :

```bash
ping <IP_cible>
ssh utilisateur@<IP_cible>
curl http://<IP_cible>
dig example.com
nslookup example.com
```

Repères attendus :

| Trafic | Log probable |
|---|---|
| Ping | `conn.log` |
| DNS | `dns.log` et `conn.log` |
| HTTP non chiffré | `http.log` et `conn.log` |
| SSH | `ssh.log` et `conn.log` |

## Scans Nmap à reconnaître

Scan TCP SYN :

```bash
sudo nmap -sS 192.168.20.10
```

Scan TCP Connect :

```bash
nmap -sT 192.168.20.10
```

Scan d'une plage de ports :

```bash
nmap -p 1-1024 192.168.20.10
```

À observer :

| Source | Indices |
|---|---|
| Zeek | Nombreuses connexions vers une même cible, ports variés, états `S0`, `REJ`, `RSTO` |
| Wireshark | Paquets SYN, SYN/ACK, RST, connexions complètes ou refusées |
| pfSense | Pass/block selon les règles, interface, source, destination, port |

## SYN flood limité

À faire uniquement dans le lab :

```bash
sudo hping3 -S --flood -p 80 192.168.20.10
```

Arrêter rapidement avec `Ctrl + C`.

Signes attendus :

- répétition rapide de paquets TCP SYN ;
- même source, même destination, même port ;
- beaucoup de lignes proches dans `conn.log` ;
- états comme `S0` ou `OTH` ;
- pas forcément d'alerte explicite dans `notice.log`.

## Corrélation d'un événement

Pour reconstituer une chronologie, relever les mêmes éléments dans chaque outil.

| Élément | Zeek | Wireshark | pfSense | OpenVPN si actif |
|---|---|---|---|---|
| Heure | Timestamp du log | Heure de capture | Timestamp firewall | Timestamp VPN |
| Source | `id.orig_h` | IP source | Source | Client/tunnel |
| Destination | `id.resp_h` | IP destination | Destination | IP distante |
| Port | `id.resp_p` | Port TCP/UDP | Port | Service via tunnel |
| Résultat | État de connexion | Flags/réponses | Pass ou block | Tunnel actif ou erreur |

Filtres Wireshark utiles :

```text
ip.addr == <IP_cible>
ip.addr == <IP_Kali>
tcp.flags.syn == 1
tcp.port == 80
icmp
```

## Réflexes de conclusion

- Toujours préciser où Zeek était placé.
- Distinguer visibilité et blocage : Zeek voit, pfSense décide.
- Comparer les heures entre Zeek, Wireshark, pfSense et OpenVPN.
- Ne pas conclure trop vite si `notice.log` est vide.
- Documenter la commande de test, l'IP source, l'IP cible, le port et la durée.
