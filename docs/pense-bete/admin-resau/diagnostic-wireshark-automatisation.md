# Diagnostic, Wireshark et automatisation

## Méthode de diagnostic

Face à une panne, éviter deux réflexes :

- redémarrer un service sans vérifier les couches basses ;
- appliquer plusieurs correctifs au hasard.

La méthode professionnelle :

1. recueillir le symptôme précis ;
2. délimiter le périmètre ;
3. tester par couches de L1 vers L7 ;
4. appliquer un correctif minimal ;
5. vérifier et documenter.

## OSI comme grille de dépannage

| Couche | Question principale | Commandes utiles |
|---|---|---|
| L1 Physique | Le lien est-il UP ? | `ip link show`, LEDs, câble |
| L2 Liaison | La MAC est-elle résolue ? | `ip neigh show`, `arp -a`, Wireshark `arp` |
| L3 Réseau | IP et routes correctes ? | `ip addr`, `ip route`, `ping`, `traceroute` |
| L4 Transport | Le port répond ? | `ss -tulnp`, `nc -zv ip port`, `telnet ip port` |
| L5/L6 Session/Présentation | TLS/session OK ? | `openssl s_client -connect ip:443` |
| L7 Application | Le service répond ? | `curl -v`, logs, `dig`, `nslookup` |

Phrase à garder : **on s'arrête dès qu'un test échoue, car on vient de trouver la couche du problème**.

## Fiche de dépannage

Structure minimale :

```text
SYMPTÔME
Description précise du problème initial.

PÉRIMÈTRE
Qui est affecté ? Depuis quand ? Qu'est-ce qui fonctionne encore ?

DÉMARCHE
Couche | Hypothèse | Commande | Résultat | Conclusion

CAUSE IDENTIFIÉE
Cause racine précise.

CORRECTIF
Commande ou action exacte.

VÉRIFICATION
Commande + résultat prouvant la résolution.
```

## Wireshark — filtres à connaître

| Filtre | Usage |
|---|---|
| `arp` | Résolution IP/MAC |
| `icmp` | Ping, echo request/reply |
| `dns` | Requêtes/réponses DNS |
| `bootp` | DHCP DORA |
| `ospf` | Paquets OSPF |
| `tcp` | Connexions TCP |
| `udp` | Trafic UDP |
| `ip.addr == 192.168.10.1` | Tout trafic lié à une IP |
| `eth.dst == ff:ff:ff:ff:ff:ff` | Broadcast Ethernet |
| `ip.dst == 224.0.0.251` | mDNS IPv4 |

## Lire une capture `.pcapng`

Commandes utiles :

```bash
capinfos fichier.pcapng
tcpdump -nn -r fichier.pcapng -c 50
tcpdump -nn -r fichier.pcapng arp
tcpdump -nn -r fichier.pcapng icmp
tcpdump -nn -r fichier.pcapng port 67 or port 68
tcpdump -nn -r fichier.pcapng udp port 5353
```

Repères :

- `capinfos` donne le volume, la durée, l'interface, le format et les métadonnées ;
- `tcpdump -r` lit une capture sans relancer de capture réseau ;
- `-nn` évite la résolution DNS et garde les IP/ports lisibles ;
- `-c 50` limite la sortie aux 50 premiers paquets.

## GNS3 vs réseau physique

| Critère | GNS3 | Réseau physique |
|---|---|---|
| Bruit réseau | Faible et contrôlé | Beaucoup plus élevé |
| Reproductibilité | Forte | Variable |
| Protocoles visibles | Ceux de la topologie simulée | ARP, DHCP, mDNS, IPv6, HTTPS, découverte réseau |
| Capture | Facile sur un lien précis | Dépend de l'interface et du support |
| Analyse | Idéale pour apprendre | Plus proche du terrain |

Exemples observés :

- GNS3 AlpesNet : DHCP, ARP, ICMP, STP, CDP, DTP ;
- OSPF isolé : Hello vers `224.0.0.5` ;
- physique `laptop.pcapng` : ARP, DHCP, mDNS `224.0.0.251`, IPv6 `ff02::fb`, trafic HTTPS.

## Bash — automatiser les vérifications

Un script sert à rendre une tâche :

- fiable ;
- reproductible ;
- traçable.

Structure de base :

```bash
#!/bin/bash
set -euo pipefail

HOSTS_FILE="${1:-hosts.txt}"
TIMEOUT=3

check_host() {
    local ip="$1"

    if ping -c 1 -W "$TIMEOUT" "$ip" &>/dev/null; then
        echo "[OK]   $ip"
        return 0
    else
        echo "[DOWN] $ip"
        return 1
    fi
}

while IFS= read -r line; do
    [[ -z "$line" || "$line" == \#* ]] && continue
    check_host "$line"
done < "$HOSTS_FILE"
```

## Bash — réflexes pro

| Élément | Rôle |
|---|---|
| `"$variable"` | Évite les erreurs avec espaces ou valeurs vides |
| `$?` | Code retour de la dernière commande |
| `return 0` | Succès dans une fonction |
| `return 1` | Échec dans une fonction |
| `>&2` | Écrire sur la sortie d'erreur |
| `tee fichier.log` | Afficher et écrire dans un log |
| `mkdir -p` | Créer un dossier si absent |
| `ShellCheck` | Vérifier la qualité d'un script |

## Commandes à retenir

```bash
# Diagnostic local
ip link show
ip addr show
ip route show
ip neigh show

# Connectivité
ping -c 4 192.168.10.1
traceroute 8.8.8.8
mtr --report 8.8.8.8

# Ports et services
ss -tulnp
nc -zv 192.168.10.5 443
curl -v http://192.168.10.5
openssl s_client -connect 192.168.10.5:443

# DNS
dig @192.168.10.5 serveur1.alpesnet.local
nslookup serveur1.alpesnet.local 192.168.10.5
```
