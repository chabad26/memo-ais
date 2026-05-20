# Réseau

## Qu'est-ce qu'un réseau ?

Un réseau sert à relier des ordinateurs et d'autres équipements entre eux.

Il permet par exemple de :

- naviguer sur Internet,
- utiliser une imprimante réseau,
- accéder à des dossiers partagés,
- échanger des données entre machines.

On peut l'imaginer comme une toile reliant plusieurs équipements.

## LAN et Internet

### LAN

Le **LAN** (*Local Area Network*) est un réseau privé local.

Il relie les ordinateurs, téléphones, imprimantes et autres équipements dans une maison ou une entreprise.

### Internet

Internet est un ensemble mondial de réseaux interconnectés.

### Différence entre les deux

- Le **LAN** reste local
- **Internet** permet une communication mondiale

## Réseau domestique et réseau d'entreprise

### Réseau domestique

Un réseau domestique est généralement simple.

Souvent, la box gère presque tout automatiquement :

- attribution des adresses IP,
- accès à Internet,
- Wi-Fi,
- configuration de base.

### Réseau d'entreprise

Un réseau d'entreprise est plus structuré et plus sécurisé.

On y trouve souvent :

- des firewalls,
- une gestion plus poussée des ports,
- une gestion des privilèges,
- un découpage des réseaux par zone ou service.

L'objectif est de limiter les accès au strict nécessaire.

## Équipements réseau

### Routeur

Le **routeur** permet de faire circuler les données entre plusieurs réseaux.

Dans un réseau classique, il relie souvent le réseau local à Internet.

### Switch

Le **switch** permet de relier plusieurs équipements dans un même réseau local.

Il distribue les communications entre les machines connectées.

### Point d'accès Wi-Fi

Le **point d'accès Wi-Fi** permet aux appareils sans fil de rejoindre le réseau.

Il peut être intégré à une box, à un routeur ou être indépendant.

## Protocoles

Un protocole est une règle ou un langage de communication entre machines.

Exemples :

- `HTTP` / `HTTPS` pour le web
- `POP3` pour la messagerie
- `IMAP` pour consulter ses mails sur le serveur
- `SMTP` pour envoyer des mails
- `SSH` pour l'administration distante
- `DNS` pour la résolution de noms
- `DHCP` pour l'attribution automatique des paramètres réseau

## DNS

Le **DNS** est l'annuaire d'Internet.

Quand on saisit un nom de domaine comme `google.com`, le DNS permet de retrouver l'adresse IP correspondante.

!!! note "Attention"
    `8.8.8.8` est une adresse IP d'un serveur DNS de Google. Ce n'est pas "l'adresse IP du site Google" au sens du site web lui-même.

## DHCP

Le **DHCP** permet d'attribuer automatiquement à une machine :

- une adresse IP,
- un masque réseau,
- une passerelle,
- parfois les serveurs DNS.

Il peut être configuré pour distribuer les adresses dans une plage précise.

## HTTP et HTTPS

`HTTP` et `HTTPS` sont des protocoles utilisés pour accéder aux pages web.

- **HTTP** : communication non chiffrée
- **HTTPS** : communication chiffrée

HTTPS est donc plus sécurisé.

## SSH

Le **SSH** permet d'établir une connexion sécurisée à un ordinateur ou à un serveur distant.

L'authentification peut se faire :

- par mot de passe,
- par clé SSH.

## Adresse IP

Une adresse IPv4 est composée de **4 octets**, par exemple :

```text
192.168.1.1
```

Chaque octet peut contenir une valeur de `0` à `255`.

Une adresse IP permet d'identifier une machine sur un réseau.

## Adresse IP privée et publique

### IP privée

Une adresse IP privée est utilisée dans un réseau local.

Exemples de plages privées fréquentes :

- `192.168.x.x`
- `10.x.x.x`
- `172.16.x.x` à `172.31.x.x`

### IP publique

Une adresse IP publique est visible sur Internet.

C'est généralement celle de la box ou du routeur côté Internet.

Plusieurs machines d'un réseau local peuvent partager une même IP publique grâce au **NAT**.

## NAT

Le **NAT** (*Network Address Translation*) permet de faire correspondre plusieurs adresses IP privées à une seule adresse IP publique.

C'est ce qui permet à plusieurs appareils d'un réseau local d'accéder à Internet via une seule connexion.

## Masque réseau

Le masque réseau permet de distinguer la partie réseau de la partie hôte dans une adresse IP.

Exemple :

```text
adresse IP : 192.168.1.42
masque : 255.255.255.0
notation CIDR : /24
```

Avec un `/24`, les trois premiers octets correspondent généralement au réseau, et le dernier identifie la machine.

## Passerelle

La passerelle est l'équipement vers lequel une machine envoie les données destinées à un autre réseau, notamment à Internet.

Dans un réseau local, la passerelle est souvent l'adresse IP de la box ou du routeur.

Exemple :

```text
192.168.1.1
```

## Ports réseau

Un port permet d'identifier un service sur une machine.

Exemples courants :

- `80` : HTTP
- `443` : HTTPS
- `22` : SSH
- `25` : SMTP
- `53` : DNS

Une adresse IP identifie une machine, un port identifie un service sur cette machine.

## IPv4 et IPv6

### IPv4

IPv4 est le format d'adressage le plus connu.

Exemple :

```text
192.168.1.10
```

### IPv6

IPv6 est le format plus récent, conçu pour offrir beaucoup plus d'adresses.

Exemple :

```text
2001:db8::1
```

Il est de plus en plus utilisé sur les réseaux modernes.

## Exemple d'analyse avec `ip a`

### Sortie observée

```text
2: eno1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether dc:4a:3e:73:80:e6 brd ff:ff:ff:ff:ff:ff
    altname enp0s31f6
    inet 172.22.114.89/24 brd 172.22.114.255 scope global dynamic noprefixroute eno1
       valid_lft 675592sec preferred_lft 675592sec
    inet6 fe80::de4a:3eff:fe73:80e6/64 scope link
       valid_lft forever preferred_lft forever
```

### Informations à retenir

- **Adresse IPv4** : `172.22.114.89`
- **Masque réseau** : `/24`, soit `255.255.255.0`
- **Broadcast** : `172.22.114.255`
- **Interface** : `eno1` avec l'altname `enp0s31f6`
- **Adresse MAC** : `dc:4a:3e:73:80:e6`
- **Adresse IPv6 locale** : `fe80::de4a:3eff:fe73:80e6/64`

!!! note "Passerelle"
    La passerelle n'apparaît pas directement dans `ip a`. Pour l'afficher, on utilise plutôt `ip route`.

Exemple :

```bash
ip route
```

Exemple de résultat :

```text
default via 172.22.114.1 dev eno1 proto dhcp src 172.22.114.89 metric 100
172.22.114.0/24 dev eno1 proto kernel scope link src 172.22.114.89 metric 100
```

On peut alors en déduire :

- **Passerelle** : `172.22.114.1`

## Commandes utiles

### Tester la connectivité

```bash
ping 8.8.8.8
```

Permet de tester si une machine peut joindre une autre machine par le réseau.

### Tester la résolution DNS

```bash
ping google.com
```

Permet de vérifier à la fois la connectivité réseau et la résolution DNS.

### Voir la configuration IP

```bash
ip a
```

Affiche les interfaces réseau et leurs adresses.

### Voir les routes

```bash
ip route
```

Affiche la table de routage et notamment la passerelle par défaut.

### Voir les ports en écoute

```bash
ss -tulpn
```

Affiche les services réseau actifs et les ports utilisés.

## Notion de client et serveur

Dans un échange réseau :

- le client envoie une requête,
- le serveur répond à cette requête.

Exemple :

- un navigateur web est un client,
- un serveur web héberge le site et répond.

## Sécurité réseau

Dans un réseau, la sécurité consiste notamment à :

- limiter les accès inutiles,
- filtrer les connexions,
- chiffrer les échanges,
- segmenter les réseaux,
- surveiller les activités anormales.

Des outils comme les firewalls, les VPN, les VLAN et les systèmes de supervision participent à cette sécurité.

!!! tip "À ne pas confondre"
    Le switch relie des équipements dans un même réseau local, alors que le routeur relie plusieurs réseaux entre eux.

!!! info "Résumé rapide"
    Une machine a souvent besoin au minimum de quatre éléments pour communiquer correctement :
    - une adresse IP
    - un masque réseau
    - une passerelle
    - un ou plusieurs serveurs DNS

## IP Privé/publique

![Différence IP public/private](/docs/assets/img/schema/schema-difIP.jpg)

## Masque de sous-réseau

![calcul masque](/docs/assets/img/schema/schema-mask.jpg)
