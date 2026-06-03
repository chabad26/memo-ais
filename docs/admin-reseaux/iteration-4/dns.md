# Synthèse — DNS interne avec BIND9

## 1. Pourquoi utiliser un DNS interne ?

Sans DNS interne, les utilisateurs et administrateurs doivent retenir les adresses IP des serveurs.

Exemple :

```bash
ssh 192.168.10.5
```

Avec un DNS interne, on utilise un nom lisible :

```bash
ssh serveur1.alpesnet.local
```

Le DNS interne apporte plusieurs avantages :

- les noms sont plus faciles à retenir que les adresses IP ;
- si un serveur change d'adresse IP, on modifie seulement l'enregistrement DNS ;
- les services internes deviennent plus propres à administrer ;
- c'est une base pour des services plus avancés comme Active Directory, Kubernetes ou des applications internes.

!!! note "Dans le lab"
    La zone utilisée est `alpesnet.local`. Dans une infrastructure réelle, il faut vérifier les conventions de nommage de l'entreprise, car le suffixe `.local` est aussi utilisé par mDNS dans certains environnements.

---

## 2. Enregistrements DNS à connaître

| Type | Signification | Exemple |
| --- | --- | --- |
| `A` | Nom vers adresse IPv4 | `serveur1.alpesnet.local.` → `192.168.10.5` |
| `AAAA` | Nom vers adresse IPv6 | `serveur1.alpesnet.local.` → `2001:db8::5` |
| `CNAME` | Alias vers un nom canonique | `www` → `serveur1.alpesnet.local.` |
| `MX` | Serveur de messagerie de la zone | `alpesnet.local.` → `mail.alpesnet.local.` |
| `PTR` | Adresse IP vers nom | `5.10.168.192.in-addr.arpa.` → `serveur1.alpesnet.local.` |
| `NS` | Serveur DNS autoritaire pour la zone | `alpesnet.local.` → `ns1.alpesnet.local.` |
| `SOA` | Métadonnées de la zone | Serial, refresh, retry, expire |

À retenir :

- `A` est l'enregistrement le plus courant en IPv4 ;
- `CNAME` sert à créer un alias, par exemple `www` ;
- `PTR` sert à la résolution inverse ;
- `SOA` existe une fois au début de chaque zone ;
- le point final dans `serveur1.alpesnet.local.` indique un nom pleinement qualifié.

---

## 3. Installer BIND9

**BIND9** (*Berkeley Internet Name Domain 9*) est un serveur DNS très utilisé sur Unix/Linux.

Installation sur Debian/Ubuntu :

```bash
sudo apt update
sudo apt install bind9 bind9utils bind9-doc dsniff  dnstracer dnstop dnsutils 

```

Vérifier la version :

```bash
named -v
```

Vérifier l'état du service :

```bash
sudo systemctl status bind9
```

Le service doit être en état `active (running)`.

---

## 4. Déclarer la zone forward

La zone forward permet de résoudre un nom vers une adresse IP.

Fichier :

```text
/etc/bind/named.conf.local
```

Configuration :

```conf
zone "alpesnet.local" {
    type master;
    file "/etc/bind/db.alpesnet.local";
};
```

Lecture :

| Directive | Rôle |
| --- | --- |
| `zone "alpesnet.local"` | Déclare la zone DNS interne |
| `type master` | Ce serveur possède la version principale de la zone |
| `file` | Indique le fichier qui contient les enregistrements |

---

## 5. Créer le fichier de zone

Fichier :

```text
/etc/bind/db.alpesnet.local
```

Exemple complet :

```dns
$TTL    604800
@   IN  SOA     ns1.alpesnet.local. admin.alpesnet.local. (
                    2026052901  ; Serial
                    604800      ; Refresh
                    86400       ; Retry
                    2419200     ; Expire
                    604800 )    ; Negative Cache TTL

; --- Serveurs de noms de la zone ---
@       IN  NS      ns1.alpesnet.local.

; --- Enregistrements A : nom vers IP ---
ns1         IN  A       192.168.10.5
serveur1    IN  A       192.168.10.5
routeur1    IN  A       192.168.10.1
routeur2    IN  A       192.168.20.1
pc-admin    IN  A       192.168.10.10

; --- Alias ---
www         IN  CNAME   serveur1.alpesnet.local.
```

### Comprendre le SOA

| Champ | Exemple | Rôle |
| --- | --- | --- |
| Serveur primaire | `ns1.alpesnet.local.` | Serveur DNS autoritaire principal |
| Contact admin | `admin.alpesnet.local.` | Contact administratif, forme DNS de `admin@alpesnet.local` |
| Serial | `2026052901` | Version de la zone |
| Refresh | `604800` | Délai avant vérification par un secondaire |
| Retry | `86400` | Délai de nouvel essai si le refresh échoue |
| Expire | `2419200` | Durée avant expiration de la zone sur un secondaire |
| Negative Cache TTL | `604800` | Durée de cache des réponses négatives |

!!! warning "Serial DNS"
    À chaque modification du fichier de zone, il faut incrémenter le `Serial`. Sinon, les serveurs secondaires ou certains caches peuvent continuer à considérer l'ancienne version comme valide.

---

## 6. Vérifier la configuration

Vérifier la syntaxe de la zone :

```bash
named-checkzone alpesnet.local /etc/bind/db.alpesnet.local
```

Redémarrer BIND9 :

```bash
sudo systemctl restart bind9
```

Contrôler le service :

```bash
sudo systemctl status bind9
```

Tester la résolution avec `nslookup` :

```bash
nslookup serveur1.alpesnet.local 192.168.10.5
```

Tester avec `dig` :

```bash
dig @192.168.10.5 serveur1.alpesnet.local A
```

Tester le SOA :

```bash
dig @192.168.10.5 alpesnet.local SOA
```

Tester l'alias :

```bash
dig @192.168.10.5 www.alpesnet.local CNAME
```

---

## 7. Dépannage rapide

| Symptôme | Vérification |
| --- | --- |
| Le service ne démarre pas | `sudo systemctl status bind9` |
| Erreur dans la zone | `named-checkzone alpesnet.local /etc/bind/db.alpesnet.local` |
| Le nom ne résout pas | Vérifier l'enregistrement `A` et l'adresse du serveur DNS interrogé |
| L'ancien résultat revient encore | Vérifier le TTL et incrémenter le `Serial` |
| Les clients n'utilisent pas le DNS interne | Vérifier l'option DHCP `dns-server` |

Dans le lab AlpesNet, si le DHCP distribue le DNS `192.168.10.5`, les clients doivent pouvoir interroger directement le serveur BIND9 :

```bash
dig @192.168.10.5 serveur1.alpesnet.local
```

---

## 8. Résumé express

| Élément | À retenir |
| --- | --- |
| DNS interne | Transforme les noms internes en adresses IP |
| Zone forward | Nom vers IP |
| `A` | Enregistrement IPv4 |
| `CNAME` | Alias |
| `NS` | Serveur DNS de la zone |
| `SOA` | Métadonnées et version de zone |
| `Serial` | À incrémenter à chaque modification |
| BIND9 | Serveur DNS courant sous Linux |
| Test | `dig @IP_DNS nom type` |

---

## Sources

- [RFC 1034 — Domain Names: Concepts and Facilities](https://datatracker.ietf.org/doc/html/rfc1034)
- [RFC 1035 — Domain Names: Implementation and Specification](https://datatracker.ietf.org/doc/html/rfc1035)
- [BIND9 Documentation officielle](https://bind9.readthedocs.io/)
- [ISC — BIND](https://www.isc.org/bind/)
