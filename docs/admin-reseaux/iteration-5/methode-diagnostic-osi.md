# Méthode de diagnostic réseau par couches OSI

## Contexte — Pourquoi une méthode ?

Face à une panne, deux comportements sont improductifs :

- **Commencer par la fin** : « Le service ne répond pas » → on redémarre le service sans vérifier si le problème n'est pas au niveau réseau.
- **Appliquer des correctifs au hasard** : on fait des changements en espérant que ça fonctionne. Si ça marche, on ne sait pas pourquoi. Si ça ne marche pas, on a ajouté du bruit.

La méthode professionnelle repose sur deux principes :

- **isoler par couches** ;
- **formuler une hypothèse avant chaque test**.

## Le modèle OSI à 7 couches — outil de diagnostic

Le modèle OSI (*Open Systems Interconnection*, ISO 7498, 1984) est plus granulaire que TCP/IP. Il est utilisé comme cadre de diagnostic : on descend de L7 vers L1 pour trouver à quel niveau se situe le problème.

| Couche | Nom | Questions à se poser | Outils de diagnostic |
|---|---|---|---|
| L7 | Application | Le service répond ? La configuration est correcte ? | `curl -v http://ip` · logs service · `nslookup` |
| L6 | Présentation | Le format ou l'encodage est-il correct ? | Logs application · Wireshark données applicatives |
| L5 | Session | La session s'établit ? TLS est valide ? | `openssl s_client -connect ip:443` |
| L4 | Transport | Le port est-il ouvert ? TCP s'établit ? | `ss -tulnp` · `telnet ip port` · `nc -zv ip port` |
| L3 | Réseau | L'IP est-elle correcte ? La route existe ? | `ip addr` · `ping` · `traceroute` · `show ip route` |
| L2 | Liaison | La MAC est-elle résolue ? ARP fonctionne ? | `arp -a` · `ip neigh` · Wireshark ARP |
| L1 | Physique | Le câble est-il branché ? Le lien est-il UP ? | `ip link show` · LEDs · test câble |

En pratique, on commence par **L1** parce que les problèmes physiques sont fréquents et rapides à vérifier, puis on remonte vers **L7**. On s'arrête dès qu'un test échoue : on a trouvé la couche où se situe le problème.

## La démarche en 5 étapes

### Étape 1 — Recueillir le symptôme précis

Ne pas se contenter de « ça marche pas ». Poser les questions :

- Qui est affecté ? Une machine, tout un site, tout le réseau ?
- Depuis quand ? Une mise à jour récente ? Une intervention ?
- Qu'est-ce qui fonctionne encore ? Exemple : ping OK mais SSH KO = L4.
- C'est permanent ou intermittent ?

### Étape 2 — Délimiter le périmètre

Tester par dichotomie pour réduire le champ des possibles :

- Le problème est-il local à une machine ou global à tout le réseau ?
- Est-il unidirectionnel ? Exemple : A → B KO mais B → A OK = asymétrie de routage ou NAT.
- Le test échoue-t-il depuis la machine elle-même ou seulement depuis le routeur ? Cela permet d'isoler un problème de NAT.

### Étape 3 — Descendre par couches, de L1 vers L7

Pour chaque couche :

- Formuler une hypothèse : « J'émets l'hypothèse que le problème se situe à L3 car le ping échoue ».
- Exécuter la commande de test.
- Analyser le résultat : il confirme ou infirme l'hypothèse.
- Si l'hypothèse est confirmée, la couche est trouvée : passer à l'identification de la cause.
- Si l'hypothèse est infirmée, passer à la couche suivante.

### Étape 4 — Appliquer le correctif minimal

Ne faire qu'une seule modification à la fois.

Si tu fais 3 changements simultanément et que ça marche, tu ne sais pas lequel a résolu le problème. Si tu fais 3 changements et que ça ne marche pas, tu ne sais pas si tu n'as pas empiré la situation.

### Étape 5 — Vérifier et documenter

Confirmer que le symptôme initial est résolu en reproduisant le test qui échouait. Documenter ensuite dans une fiche de dépannage.

## Commandes de diagnostic — Ubuntu

```bash
# L1 — État physique des interfaces
ip link show                       # UP/DOWN, erreurs
ip link show eth0                  # une interface spécifique
ethtool eth0                       # vitesse, duplex, lien détecté

# L2 — ARP, résolution MAC
ip neigh show                      # cache ARP
arp -a                             # syntaxe legacy
arping -I eth0 192.168.10.1        # ping ARP direct

# L3 — IP, routes, ping, traceroute
ip addr show                       # adresses IP configurées
ip route show                      # table de routage
ping -c 4 192.168.10.1             # test ICMP
ping -c 1 -W 2 192.168.10.1        # 1 paquet, timeout 2s
traceroute 8.8.8.8                 # tracer la route
mtr --report 8.8.8.8               # traceroute continu

# L4 — Ports, connexions
ss -tulnp                          # ports en écoute
ss -tnp                            # connexions TCP actives
telnet 192.168.10.5 80             # tester un port TCP
nc -zv 192.168.10.5 443            # tester un port moderne

# L7 — Tests applicatifs
nslookup serveur1.alpesnet.local 192.168.10.5
dig @192.168.10.5 serveur1.alpesnet.local
curl -v http://192.168.10.5
openssl s_client -connect 192.168.10.5:443
```

## Commandes de diagnostic — Cisco IOS

```text
! L1/L2
show interfaces                    ! état détaillé
show interfaces status             ! tableau résumé
show mac address-table             ! table MAC

! L3
show ip interface brief            ! toutes les interfaces et leurs IPs
show ip route                      ! table de routage
ping 192.168.20.10                 ! ICMP depuis le routeur
traceroute 192.168.30.10           ! traceroute depuis le routeur

! Services
show ip dhcp binding               ! attributions DHCP actives
show ip dhcp server statistics     ! statistiques DHCP
show ip nat translations           ! translations NAT actives
show ip ospf neighbor              ! adjacences OSPF
show ip ospf database summary      ! résumé de la LSDB
```

## Structure de la fiche de dépannage

```text
=== FICHE DE DÉPANNAGE ===
Auteur     : [Nom]
Date/Heure : [Date]
Topologie  : AlpesNet RES-01a

SYMPTÔME
[Description précise du symptôme initial — pas "ça marche pas"]

PÉRIMÈTRE
Affecte : [qui / quoi / depuis quand]
Fonctionne encore : [...]

DÉMARCHE DE DIAGNOSTIC
│ Couche │ Hypothèse avant le test │ Commande exécutée │ Résultat │ Conclusion │
│--------│-------------------------│-------------------│----------│------------│
│ L1     │ ...                     │ ip link show      │ UP/UP    │ L1 OK      │
│ L2     │ ...                     │ ip neigh show     │ ...      │ L2 OK      │
│ L3     │ ...                     │ show ip route     │ ...      │ CAUSE L3   │

CAUSE IDENTIFIÉE
[Description précise de la cause racine — pas "il y avait un problème"]
[Exemple : "L'interface GigabitEthernet0/2 de R3 était en administratively down,
 ce qui a coupé l'adjacence OSPF et supprimé la route vers 192.168.30.0/24"]

CORRECTIF APPLIQUÉ
[Commande(s) exacte(s)]
R3(config)# interface GigabitEthernet0/2
R3(config-if)# no shutdown

VÉRIFICATION
[Commande + résultat prouvant la résolution]
show ip ospf neighbor → R3 est revenu en état Full
ping 192.168.30.10 → OK (0% packet loss)
```

## Ressources diagnostic

- `man ping` · `man traceroute` · `man mtr` · `man ss` · `man ip`
- [CERT-FR — Méthodes d'investigation incident](https://cert.ssi.gouv.fr/)
- [ANSSI — Guide de gestion d'incidents](https://cyber.gouv.fr/securisation/gestion-de-crise/piloter-la-remediation-dun-incident-cyber/)
- [Wireshark Network Analysis Guide](https://www.wireshark.org/docs/wsug_html_chunked/)
