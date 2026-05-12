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

## Protocoles

Un protocole est une règle ou un langage de communication entre machines.

Exemples :

- `HTTP` / `HTTPS` pour le web
- `POP3` pour la messagerie
- `SSH` pour l'administration distante

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

## Exemple d'analyse avec `ip a`

### Sortie observée

```bash
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
- **Passerelle** : `172.22.114.1`
- **Interface** : `eno1` avec l'altname `enp0s31f6`

## Adresse IP

Une adresse IPv4 est composée de **4 octets**, par exemple :

```text
192.168.1.1
```

Chaque octet peut contenir une valeur de `0` à `255`.
