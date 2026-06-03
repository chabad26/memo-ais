# TP GNS3 - NAT/PAT avec serveur public

## Objectif

Mettre en place un NAT overload, aussi appele PAT, sur `R1` afin que les postes des reseaux internes puissent joindre un serveur public simule derriere `R-Internet`.

Le test principal du TP est :

```text
PC-Admin -> Serveur-Public 203.0.113.2
```

Le ping vers `8.8.8.8` ne fonctionne que si la topologie GNS3 dispose d'un acces Internet reel. Dans ce TP, `8.8.8.8` n'est pas le bon indicateur de validation.

![Topologie GNS3 NAT](../../assets/img/admin-reseau/it-4/gns3%20nat.png)

---

## Plan d'adressage utilise

| Equipement | Interface | Adresse IP | Role |
| --- | --- | --- | --- |
| `R1` | `G0/0` | `192.168.10.1` | LAN interne, NAT inside |
| `R1` | `G0/1.20` | `192.168.10.129` | VLAN 20, NAT inside |
| `R1` | `G0/1.30` | `192.168.10.146` | VLAN 30, NAT inside |
| `R1` | `G0/1.40` | `192.168.10.153` | VLAN 40, NAT inside |
| `R1` | `G0/2` | `10.0.0.1/30` | Vers `R-Internet`, NAT outside |
| `R-Internet` | `G0/0` | `10.0.0.2/30` | Vers `R1` |
| `R-Internet` | `G0/1` | `203.0.113.1/30` | Vers `Serveur-Public` |
| `Serveur-Public` | `ens3` | `203.0.113.2/30` | Serveur Debian public |

Le reseau `203.0.113.0/24` est reserve a la documentation. Il est utilisable dans GNS3 pour un laboratoire, mais il ne represente pas un acces Internet reel.

---

## Preparer le serveur Debian dans GNS3

Pour le serveur public, il faut utiliser une image Debian fonctionnelle dans GNS3.

Point important rencontre pendant le TP : la carte reseau par defaut de la VM Debian peut ne pas etre detectee. Si la commande `ip link` n'affiche que `lo`, la VM ne voit aucune carte Ethernet.

Dans ce cas :

1. eteindre la VM Debian ;
2. ouvrir les proprietes de la VM dans GNS3 ;
3. changer le type de carte reseau pour une carte virtuelle compatible ;
4. verifier que la carte est bien connectee au routeur ;
5. redemarrer la VM ;
6. verifier avec `ip link`.

Une fois corrige, l'interface peut apparaitre sous le nom `ens3`, avec parfois l'alias `enp0s3`.

Configuration Debian :

```ini
source-directory /etc/network/interfaces.d

auto lo
iface lo inet loopback

auto ens3
iface ens3 inet static
        address 203.0.113.2
        netmask 255.255.255.252
        gateway 203.0.113.1
        dns-nameservers 10.0.0.1
```

Redemarrage du service reseau :

```bash
sudo systemctl restart networking.service
```

Verification :

```bash
ip a
ip route
ping 203.0.113.1
```

Le serveur doit afficher :

```text
ens3 ... inet 203.0.113.2/30
default via 203.0.113.1
```

---

## Configuration de R-Internet

`R-Internet` simule le routeur situe entre `R1` et le serveur public.

```cisco
enable
configure terminal

interface GigabitEthernet0/0
 ip address 10.0.0.2 255.255.255.252
 description Rinternet-to-R1
 no shutdown
exit

interface GigabitEthernet0/1
 ip address 203.0.113.1 255.255.255.252
 description Rinternet-to-serveur_public
 no shutdown
exit

end
write memory
```

Attention : avec un masque `/30`, l'adresse `203.0.113.12` est une adresse de reseau, donc elle ne peut pas etre assignee a une interface. Le couple correct utilise ici est :

```text
203.0.113.1/30 pour R-Internet
203.0.113.2/30 pour Serveur-Public
```

---

## Configuration de R1

### Interfaces NAT

Les interfaces internes doivent etre declarees en `ip nat inside`.

Dans ce TP, `R1` utilise aussi des sous-interfaces VLAN sur `G0/1`. Il faut donc mettre `ip nat inside` sur les sous-interfaces, pas seulement sur l'interface physique `G0/1`.

```cisco
enable
configure terminal

interface GigabitEthernet0/0
 ip nat inside
exit

interface GigabitEthernet0/1.20
 ip nat inside
exit

interface GigabitEthernet0/1.30
 ip nat inside
exit

interface GigabitEthernet0/1.40
 ip nat inside
exit

interface GigabitEthernet0/2
 ip address 10.0.0.1 255.255.255.252
 ip nat outside
 description R1-to-Rinternet
 no shutdown
exit
```

### ACL des reseaux internes

L'ACL indique quels reseaux internes ont le droit d'etre translates.

Les sous-reseaux utilises dans le TP sont :

```text
192.168.10.0/25
192.168.10.128/28
192.168.10.144/29
192.168.10.152/29
```

Configuration :

```cisco
no access-list 1
access-list 1 permit 192.168.10.0 0.0.0.127
access-list 1 permit 192.168.10.128 0.0.0.15
access-list 1 permit 192.168.10.144 0.0.0.7
access-list 1 permit 192.168.10.152 0.0.0.7
```

Une ACL plus large peut aussi fonctionner pour le lab :

```cisco
access-list 1 permit 192.168.10.0 0.0.0.255
```

Mais l'ACL detaillee correspond mieux au plan d'adressage reel.

### NAT overload

```cisco
ip nat inside source list 1 interface GigabitEthernet0/2 overload
```

Lecture :

- `inside source` : on traduit l'adresse source des machines internes ;
- `list 1` : seules les IP autorisees par l'ACL 1 sont concernees ;
- `interface GigabitEthernet0/2` : on utilise l'adresse de sortie de `R1`, donc `10.0.0.1` ;
- `overload` : plusieurs machines partagent la meme adresse grace aux ports.

### Route par defaut

```cisco
ip route 0.0.0.0 0.0.0.0 10.0.0.2
end
write memory
```

La commande `write memory` se lance en mode privilegie `Router#`, pas en mode configuration globale `Router(config)#`.

---

## Configuration attendue du PC-Admin

Si `PC-Admin` est sur le LAN `192.168.10.0/25`, il doit avoir une passerelle vers `R1`.

Exemple :

```text
IP       : 192.168.10.10
Masque   : 255.255.255.128
Gateway  : 192.168.10.1
```

Si le poste est dans un VLAN, la passerelle doit etre l'adresse de la sous-interface correspondante :

| Reseau | Passerelle |
| --- | --- |
| VLAN 20 | `192.168.10.129` |
| VLAN 30 | `192.168.10.146` |
| VLAN 40 | `192.168.10.153` |

---

## Tests de validation

### Depuis R1

```cisco
ping 10.0.0.2
ping 203.0.113.1
ping 203.0.113.2
```

### Depuis R-Internet

```cisco
ping 203.0.113.2
```

### Depuis le serveur Debian

```bash
ping 203.0.113.1
ping 10.0.0.1
```

### Depuis PC-Admin

```text
ping 203.0.113.2
```

Le ping vers `8.8.8.8` peut echouer dans cette topologie, car aucun equipement GNS3 ne porte cette adresse et la maquette n'est pas forcement connectee a Internet.

---

## Verification NAT

Apres un ping depuis `PC-Admin` vers `203.0.113.2`, afficher les translations sur `R1` :

```cisco
show ip nat translations
```

On doit observer une translation entre l'IP privee du poste interne et l'IP de sortie de `R1`.

Exemple de lecture :

| Champ Cisco | Signification |
| --- | --- |
| `Inside local` | Adresse reelle du PC interne, par exemple `192.168.10.x` |
| `Inside global` | Adresse utilisee apres NAT, ici `10.0.0.1` |
| `Outside global` | Adresse du serveur public, ici `203.0.113.2` |

![Show ip nat translations](../../assets/img/admin-reseau/it-4/show%20ip%20nat%20.png)

Commandes utiles :

```cisco
show ip nat translations
show ip nat statistics
show access-lists
show ip route
show ip interface brief
show running-config | include ip nat|access-list|ip route
```

Pour vider la table avant de refaire un test :

```cisco
clear ip nat translation *
```

---

## Resume rapide

Pour que le NAT/PAT fonctionne :

1. les interfaces LAN de `R1` doivent etre en `ip nat inside` ;
2. les sous-interfaces VLAN doivent aussi etre en `ip nat inside` ;
3. l'interface de `R1` vers `R-Internet` doit etre en `ip nat outside` ;
4. l'ACL doit couvrir les sous-reseaux internes ;
5. le NAT overload doit utiliser l'interface externe de `R1` ;
6. `R1` doit avoir une route par defaut vers `R-Internet` ;
7. le serveur Debian public doit avoir une carte reseau detectee et une passerelle vers `203.0.113.1` ;
8. le test de validation est `PC-Admin -> 203.0.113.2`, puis `show ip nat translations`.

---

# Suite du TP - Sortie Internet et DNS Bind9

## Objectif de la suite

Ajouter un serveur DNS Bind9 dans la maquette, creer une zone DNS interne `alpesnet.local`, distribuer l'adresse du serveur DNS par DHCP, puis verifier les requetes DNS depuis un VPCS et avec Wireshark.

Points a valider :

1. la topologie GNS3 peut sortir sur Internet ;
2. Bind9 est installe sur le serveur Ubuntu/Debian ;
3. la zone `alpesnet.local` contient 3 enregistrements `A` ;
4. le DHCP distribue l'IP du serveur DNS ;
5. un VPCS resout `routeur1.alpesnet.local` ;
6. Wireshark montre la requete DNS et la reponse.

---

## 1. Faire sortir GNS3 sur Internet

Pour installer Bind9 avec `apt`, le serveur doit pouvoir joindre Internet.

Dans GNS3, ajouter un noeud `NAT`, puis le connecter a `R-Internet` sur `G0/2`.

Configuration attendue sur `R-Internet` :

```cisco
enable
configure terminal

interface GigabitEthernet0/2
 ip address dhcp
 ip nat outside
 no shutdown
exit

interface GigabitEthernet0/0
 ip nat inside
exit

interface GigabitEthernet0/1
 ip nat inside
exit

access-list 10 permit 10.0.0.0 0.0.0.3
access-list 10 permit 203.0.113.0 0.0.0.3

ip nat inside source list 10 interface GigabitEthernet0/2 overload
end
write memory
```

Dans le TP, `G0/2` a recu par DHCP :

```text
192.168.122.200
```

La passerelle du NAT GNS3 est generalement :

```text
192.168.122.1
```

Il vaut mieux mettre la route par defaut vers la passerelle plutot que seulement vers l'interface Ethernet :

```cisco
configure terminal
no ip route 0.0.0.0 0.0.0.0 GigabitEthernet0/2
ip route 0.0.0.0 0.0.0.0 192.168.122.1
end
write memory
```

Verification sur `R-Internet` :

```cisco
show ip interface brief
show ip route
ping 192.168.122.1
ping 8.8.8.8
```

Important : un ping lance directement depuis `R-Internet` ne cree pas forcement de translation NAT visible. Pour voir une translation, il faut tester depuis une machine derriere `R-Internet`, par exemple le serveur Debian.

Depuis le serveur Debian :

```bash
ping 203.0.113.1
ping 8.8.8.8
sudo apt update
```

Si `ping 8.8.8.8` fonctionne mais pas `ping google.com`, c'est un probleme DNS, pas un probleme de routage.

---

## 2. Installer Bind9 sur le serveur Ubuntu/Debian

Sur le serveur DNS, ici le serveur joignable en `203.0.113.2` :

```bash
sudo apt update
sudo apt install bind9 bind9utils dnsutils
```

Verifier que le service tourne :

```bash
sudo systemctl status bind9
named -v
```

Verifier que le serveur ecoute sur le port DNS :

```bash
sudo ss -lntup | grep :53
```

Si le serveur ecoute seulement sur `127.0.0.1`, il faut verifier la configuration Bind9. Pour le lab, Bind9 doit repondre sur l'adresse du serveur, par exemple `203.0.113.2`.

---

## 3. Declarer la zone `alpesnet.local`

Editer :

```bash
sudo nano /etc/bind/named.conf.local
```

Ajouter :

```conf
zone "alpesnet.local" {
    type master;
    file "/etc/bind/db.alpesnet.local";
};
```

Copier un modele de zone :

```bash
sudo cp /etc/bind/db.local /etc/bind/db.alpesnet.local
```

Editer :

```bash
sudo nano /etc/bind/db.alpesnet.local
```

Exemple de zone simple avec 3 enregistrements `A` demandes dans le TP :

```dns
$TTL    604800
@   IN  SOA     ns1.alpesnet.local. admin.alpesnet.local. (
                    2026060301  ; Serial
                    604800      ; Refresh
                    86400       ; Retry
                    2419200     ; Expire
                    604800 )    ; Negative Cache TTL

@           IN  NS      ns1.alpesnet.local.

ns1         IN  A       203.0.113.2
routeur1    IN  A       192.168.10.1
pc-admin    IN  A       192.168.10.10
serveur1    IN  A       192.168.10.5
```

Les 3 enregistrements principaux sont :

| Nom DNS | Adresse IP | Role |
| --- | --- | --- |
| `routeur1.alpesnet.local` | `192.168.10.1` | R1 |
| `pc-admin.alpesnet.local` | `192.168.10.10` | un PC |
| `serveur1.alpesnet.local` | `192.168.10.5` | serveur |

`ns1.alpesnet.local` pointe vers `203.0.113.2`, c'est l'adresse du serveur DNS interroge dans ce TP.

Note : `dig` peut afficher un avertissement avec `.local`, car ce suffixe est reserve a mDNS. Pour un TP, cela reste utilisable, mais en production on eviterait `.local`.

Verifier la configuration :

```bash
sudo named-checkconf
sudo named-checkzone alpesnet.local /etc/bind/db.alpesnet.local
sudo systemctl restart bind9
sudo systemctl status bind9
```

Tester localement depuis le serveur DNS :

```bash
dig @203.0.113.2 routeur1.alpesnet.local A
dig @203.0.113.2 pc-admin.alpesnet.local A
dig @203.0.113.2 serveur1.alpesnet.local A
```

Une reponse correcte contient :

```text
status: NOERROR
ANSWER SECTION
```

---

## 4. Configurer le DHCP pour distribuer le DNS

Sur `R1`, ajouter l'adresse du serveur DNS dans les pools DHCP.

Exemple pour le LAN Admin :

```cisco
configure terminal
ip dhcp pool LAN_ADMIN
 dns-server 203.0.113.2
 domain-name alpesnet.local
exit
end
write memory
```

Faire la meme chose dans les autres pools DHCP si les VLANs doivent aussi utiliser le DNS Bind9 :

```cisco
configure terminal
ip dhcp pool VLAN20
 dns-server 203.0.113.2
 domain-name alpesnet.local
exit

ip dhcp pool VLAN30
 dns-server 203.0.113.2
 domain-name alpesnet.local
exit

ip dhcp pool VLAN40
 dns-server 203.0.113.2
 domain-name alpesnet.local
exit
end
write memory
```

Verifier :

```cisco
show running-config | section ip dhcp pool
show ip dhcp binding
```

Sur un VPCS, renouveler l'adresse DHCP :

```text
ip dhcp
show ip
```

Le DNS affiche doit etre :

```text
DNS server: 203.0.113.2
```

---

## 5. Tester depuis un VPCS

Depuis `PC-Admin` ou un autre VPCS :

```text
ping 203.0.113.2
nslookup routeur1.alpesnet.local 203.0.113.2
```

Resultat attendu :

```text
Name: routeur1.alpesnet.local
Address: 192.168.10.1
```

Tester aussi :

```text
nslookup pc-admin.alpesnet.local 203.0.113.2
nslookup serveur1.alpesnet.local 203.0.113.2
```

Si `nslookup serveur1.alpesnet.local 192.168.10.5` echoue, c'est normal si `192.168.10.5` n'est pas le serveur DNS. La syntaxe `nslookup nom ip_dns` demande a `ip_dns` de resoudre le nom.

Dans ce TP, le serveur DNS est :

```text
203.0.113.2
```

---

## 6. Observer avec Wireshark

Lancer une capture sur le lien entre le client et le routeur, ou sur le lien vers le serveur DNS.

Filtre Wireshark :

```text
dns
```

Puis relancer depuis le VPCS :

```text
nslookup routeur1.alpesnet.local 203.0.113.2
```

On doit observer :

| Paquet | Contenu attendu |
| --- | --- |
| Requete DNS | `Standard query A routeur1.alpesnet.local` |
| Reponse DNS | `Standard query response A 192.168.10.1` |

Si la capture est faite cote sortie NAT, l'adresse source peut etre translatee. C'est normal : le client interne sort via le NAT de `R1`.

---

## 7. Tester depuis le laptop reel

Depuis le laptop, `203.0.113.2` n'est pas forcement joignable directement, car cette adresse est dans la topologie GNS3.

Deux methodes existent.

### Methode A : interroger via l'IP NAT de R-Internet

Si `R-Internet` a recu `192.168.122.200` sur `G0/2`, creer une redirection DNS vers le serveur Bind9 :

```cisco
configure terminal
ip nat inside source static udp 203.0.113.2 53 interface GigabitEthernet0/2 53
ip nat inside source static tcp 203.0.113.2 53 interface GigabitEthernet0/2 53
end
write memory
```

Depuis le laptop :

```bash
dig @192.168.122.200 routeur1.alpesnet.local A
```

### Methode B : ajouter une route sur le laptop

Sur un laptop Linux, si le reseau `192.168.122.0/24` de GNS3 est joignable :

```bash
sudo ip route add 203.0.113.0/30 via 192.168.122.200
dig @203.0.113.2 routeur1.alpesnet.local A
```

La methode A est souvent plus simple pour un TP, car elle expose seulement le port DNS.

---

## Checklist finale DNS

1. `R-Internet` sort vers le NAT GNS3.
2. Le serveur DNS ping `8.8.8.8`.
3. Bind9 est installe et actif.
4. La zone `alpesnet.local` est declaree dans `/etc/bind/named.conf.local`.
5. Le fichier `/etc/bind/db.alpesnet.local` contient les enregistrements `A`.
6. `named-checkconf` ne retourne pas d'erreur.
7. `named-checkzone alpesnet.local /etc/bind/db.alpesnet.local` retourne `OK`.
8. Le DHCP distribue `203.0.113.2` comme DNS.
9. Le VPCS resout `routeur1.alpesnet.local`.
10. Wireshark affiche une requete DNS et une reponse DNS.
