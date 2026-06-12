# Synthèse — pfSense

---

## 1. Rôle de pfSense

pfSense est un système basé sur **FreeBSD** qui transforme une machine physique ou virtuelle en **routeur / pare-feu** administrable par interface web.

Dans une architecture réseau, il sert principalement à :

- séparer plusieurs zones réseau : `WAN`, `LAN`, `DMZ`, VLANs ;
- filtrer les communications entre ces zones ;
- faire du NAT et de la redirection de ports ;
- distribuer ou relayer du DHCP ;
- journaliser les flux ;
- ajouter des services comme un proxy, du filtrage web ou un VPN.

> Idée clé : pfSense devient le **point de passage obligatoire** entre les réseaux. Si un flux doit aller du LAN vers Internet, de la DMZ vers Internet ou du WAN vers un serveur publié, il doit passer par une règle pfSense.

---

## 2. Architecture type LAN / DMZ / WAN

Une mise en place classique utilise au minimum deux interfaces réseau, mais trois interfaces rendent l'architecture plus propre :

| Interface | Rôle | Exemple |
| --- | --- | --- |
| `WAN` | Sortie vers Internet ou réseau amont | NAT VMware, box, routeur physique |
| `LAN` | Réseau interne des utilisateurs | postes clients, admin |
| `DMZ` / `OPT1` | Zone isolée pour services exposés | serveur web Apache |

```text
Internet / réseau amont
        |
      WAN
        |
     pfSense
      /   \
   LAN     DMZ
   |        |
Clients   Serveur web
```

La **DMZ** contient les machines qui peuvent être jointes depuis l'extérieur, par exemple un serveur web. Elle reste séparée du LAN pour éviter qu'un serveur exposé donne un accès direct au réseau interne en cas de compromission.

---

## 3. Installation et premier démarrage

pfSense peut être installé sur une machine physique ou dans VMware/GNS3. Pour un lab, une VM légère suffit généralement :

| Ressource | Valeur de lab possible |
| --- | --- |
| RAM | `512 Mo` minimum pour un petit TP |
| Disque | `8 Go` ou plus |
| Cartes réseau | 2 minimum, 3 recommandé pour LAN/DMZ/WAN |

Étapes importantes :

1. Démarrer sur l'ISO pfSense.
2. Lancer l'installation.
3. Choisir une installation rapide.
4. Redémarrer sans laisser l'ISO montée.
5. Assigner les interfaces au premier boot.

Sous pfSense, les interfaces ne s'appellent pas `eth0` ou `ens33`, mais plutôt :

| Nom possible | Exemple de matériel |
| --- | --- |
| `em0`, `em1` | cartes Intel émulées |
| `re0` | Realtek |
| `vtnet0` | VirtIO |

Il faut donc repérer les interfaces avec leur **adresse MAC** côté VMware/GNS3.

---

## 4. Assignation des interfaces

Au premier démarrage, pfSense propose d'assigner les interfaces depuis la console.

Exemple avec trois cartes :

```text
WAN  -> em0
LAN  -> em1
OPT1 -> em2
```

Dans les fiches, l'interface `OPT1` est ensuite renommée en `DMZ` depuis l'interface web :

```text
Interfaces > OPT1 > Description : DMZ
```

À retenir :

- le `WAN` reçoit une passerelle amont ;
- le `LAN` ne doit pas avoir de passerelle amont ;
- la `DMZ` ne doit pas avoir de passerelle amont ;
- les clients utilisent l'adresse pfSense de leur réseau comme passerelle par défaut.

---

## 5. Adressage et DHCP

La console pfSense permet de configurer les adresses avec l'option :

```text
2) Set interface(s) IP address
```

Exemple d'adressage :

| Zone | Adresse pfSense | DHCP |
| --- | --- | --- |
| `WAN` | adresse du réseau amont | souvent DHCP ou statique selon le lab |
| `LAN` | `192.168.10.1/24` | possible, ex. `192.168.10.100-200` |
| `DMZ` | `192.168.20.1/24` | souvent désactivé pour les serveurs |

Sur une interface interne, quand pfSense demande une passerelle :

```text
For a LAN, press ENTER for none
```

Il faut laisser vide. Une interface interne est déjà la passerelle des machines de son réseau.

---

## 6. Interface web

Une fois le LAN configuré, l'administration se fait depuis un navigateur :

```text
https://adresse-lan-pfsense
```

Identifiants par défaut :

| Login | Mot de passe |
| --- | --- |
| `admin` | `pfsense` |

À la première connexion :

- suivre le setup wizard ;
- définir le nom de machine et le domaine si besoin ;
- vérifier le DNS et le fuseau horaire ;
- vérifier le WAN et le LAN ;
- changer le mot de passe administrateur ;
- appliquer les changements.

> Bon réflexe : après chaque modification dans l'interface web, cliquer sur `Save`, puis sur `Apply changes`.

---

## 7. Logique des règles pare-feu

pfSense applique une logique de filtrage explicite :

```text
ce qui n'est pas autorisé est bloqué
```

Une règle peut notamment faire :

| Action | Effet |
| --- | --- |
| `Pass` | autorise le flux |
| `Block` | bloque silencieusement |
| `Reject` | refuse avec un retour TCP RST ou ICMP |

Les règles se lisent en fonction :

- de l'interface d'entrée ;
- de l'adresse source ;
- de l'adresse destination ;
- du protocole ;
- du port source ;
- du port destination.

Exemple : autoriser un serveur web en DMZ à faire ses mises à jour.

| Source | Destination | Protocole | Port | Rôle |
| --- | --- | --- | --- | --- |
| serveur DMZ | Internet | UDP | `53` | DNS |
| serveur DMZ | Internet | TCP | `80` | HTTP |
| serveur DMZ | Internet | TCP | `443` | HTTPS |

Ces règles permettent à la machine de résoudre les noms et d'utiliser `apt update`, sans ouvrir toute la DMZ vers le LAN.

---

## 8. Port forwarding

Le **port forwarding** sert à publier un service interne vers l'extérieur.

Exemple : publier un serveur web situé dans la DMZ.

```text
Client externe -> IP WAN pfSense:80 -> serveur web DMZ:80
```

Configuration :

```text
Firewall > NAT > Port Forward > Add
```

Champs principaux :

| Champ | Valeur pour HTTP |
| --- | --- |
| Interface | `WAN` |
| Protocol | `TCP` |
| Destination port range | `HTTP (80)` |
| Redirect target IP | IP du serveur web en DMZ |
| Redirect target port | `HTTP (80)` |
| Description | courte et claire |

pfSense peut créer automatiquement la règle firewall associée sur le `WAN`. Ensuite, le test se fait en allant sur :

```text
http://adresse-wan-pfsense
```

Pour diagnostiquer :

```text
Status > System Logs > Firewall
```

ou un scan depuis le côté WAN pour vérifier que le port attendu est ouvert.

---

## 9. DHCP server ou DHCP relay

pfSense peut fonctionner de deux façons :

| Mode | Usage |
| --- | --- |
| DHCP server | pfSense distribue directement les adresses |
| DHCP relay | pfSense relaie les requêtes vers un serveur DHCP central |

Le **DHCP relay** est utile quand plusieurs réseaux doivent recevoir leur adressage depuis un seul serveur DHCP.

Exemple :

```text
Réseau A : serveur DHCP Ubuntu
Réseau B : clients derrière pfSense
pfSense : relaie les requêtes DHCP du réseau B vers le serveur DHCP
```

Configuration générale :

```text
Services > DHCP Relay
```

À faire :

- activer le service ;
- sélectionner les interfaces concernées ;
- renseigner l'adresse IP du serveur DHCP ;
- désactiver le serveur DHCP local sur les interfaces concernées si le relay ne démarre pas.

Point important : pour que les clients du réseau secondaire sortent, il faut aussi une règle firewall sur l'interface concernée, par exemple :

| Champ | Valeur |
| --- | --- |
| Action | `Pass` |
| Interface | réseau secondaire / `LAN2` / `OPT1` |
| Address Family | `IPv4` |
| Protocol | `Any` |
| Source | réseau de l'interface |

---

## 10. Proxy transparent avec Squid

pfSense peut être étendu avec des paquets.

Pour mettre en place un proxy :

```text
System > Package Manager > Available Packages
```

Paquets vus dans les fiches :

| Paquet | Rôle |
| --- | --- |
| `Squid` | proxy HTTP/HTTPS |
| `SquidGuard` | filtrage d'URL, domaines, mots-clés |

Le proxy transparent intercepte les flux HTTP sortants du LAN. Les postes clients n'ont pas besoin de configurer manuellement un proxy.

Fonctions utiles :

- cache web local ;
- journalisation des connexions ;
- filtrage par domaines ;
- filtrage par expressions ;
- page de blocage personnalisée.

Attention : journaliser l'activité web des utilisateurs implique un cadre légal. Dans les fiches, la durée de conservation évoquée est de **31 jours** et la déclaration/information doit être prise en compte.

Pour HTTPS, il ne suffit pas d'activer Squid : il faut une autorité de certification et une configuration de filtrage SSL, ce qui est plus sensible techniquement et juridiquement.

---

## 11. VPN avec OpenVPN

pfSense peut aussi fournir un accès VPN pour des utilisateurs nomades.

Objectif :

```text
Utilisateur nomade -> Internet -> pfSense/OpenVPN -> réseau local entreprise
```

Intérêt :

- accès sécurisé au LAN depuis l'extérieur ;
- tunnel chiffré ;
- usage possible depuis ordinateur ou smartphone ;
- centralisation de l'accès distant sur le pare-feu.

Le VPN ne remplace pas les règles firewall : une fois l'utilisateur connecté, il faut encore définir précisément ce qu'il a le droit de joindre.

---

## 12. Checklist de validation

| Point à vérifier | Résultat attendu |
| --- | --- |
| Interfaces assignées | `WAN`, `LAN`, `DMZ/OPT1` correspondent aux bonnes cartes |
| Adresses IP | chaque zone a une IP pfSense cohérente |
| Passerelles internes | aucune gateway amont sur LAN/DMZ |
| Accès web admin | disponible depuis le LAN en HTTPS |
| Mot de passe admin | changé après première connexion |
| Règles firewall | seules les communications nécessaires sont autorisées |
| NAT / port forwarding | le service publié répond depuis le WAN |
| Logs firewall | les blocages et passages sont visibles |
| DHCP | serveur local ou relay, mais pas les deux sur la même interface |
| DMZ | le serveur exposé ne communique pas librement avec le LAN |

---

## 13. Résumé à retenir

pfSense est à la fois un **routeur**, un **pare-feu stateful**, une plateforme de **NAT**, un serveur ou relais **DHCP**, et une base extensible pour ajouter du **proxy**, du **filtrage web** ou du **VPN**.

La bonne méthode consiste à raisonner par zones :

```text
Qui parle ?
Depuis quelle interface ?
Vers quelle destination ?
Avec quel protocole ?
Sur quel port ?
Pourquoi ce flux est-il nécessaire ?
```

Une règle pfSense doit toujours répondre à ces questions. C'est ce qui évite de transformer le pare-feu en simple routeur ouvert entre toutes les zones.

---

***Sources de travail : fiches du dossier `Pare-Feu - PFSENSE` — installation pfSense, interfaces LAN/DMZ, port forwarding, règles firewall, proxy transparent, DHCP relay et OpenVPN.***
