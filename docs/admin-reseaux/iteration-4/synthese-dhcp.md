# Synthèse — DHCP

## 1. À quoi sert DHCP ?

Sans DHCP, chaque poste doit être configuré à la main :

- adresse IP ;
- masque de sous-réseau ;
- passerelle par défaut ;
- serveurs DNS.

Sur un réseau de 500 postes, cela représente 500 configurations à maintenir. Si la passerelle ou le DNS change, chaque machine doit être modifiée.

Le protocole **DHCP** (*Dynamic Host Configuration Protocol*) automatise cette attribution. Il fournit automatiquement les paramètres réseau nécessaires à un client pour communiquer sur le réseau.

!!! info "Référence"
    DHCP est défini principalement par la **RFC 2131**. Les options DHCP, comme le masque, la passerelle ou le DNS, sont décrites dans la **RFC 2132**.

---

## 2. Le processus DORA

Le fonctionnement classique de DHCP repose sur 4 messages : **DORA**.

| Étape | Message | Sens | Rôle |
| --- | --- | --- | --- |
| 1 | `DHCP Discover` | Client → réseau | Le client cherche un serveur DHCP. |
| 2 | `DHCP Offer` | Serveur → client | Le serveur propose une adresse IP et des paramètres. |
| 3 | `DHCP Request` | Client → réseau | Le client accepte une offre DHCP. |
| 4 | `DHCP ACK` | Serveur → client | Le serveur confirme l'attribution. |

```text
CLIENT                                      SERVEUR DHCP
  │                                               │
  │ -- DHCP Discover (broadcast) ---------------> │
  │    src: 0.0.0.0:68                            │
  │    dst: 255.255.255.255:67                    │
  │    "Y a-t-il un serveur DHCP ?"               │
  │                                               │
  │ <--------------- DHCP Offer ----------------- │
  │    "Je propose 192.168.10.50 pendant 8h"      │
  │                                               │
  │ -- DHCP Request (broadcast) ----------------> │
  │    "J'accepte l'offre de ce serveur"          │
  │                                               │
  │ <---------------- DHCP ACK ------------------ │
  │    IP: 192.168.10.50/24                       │
  │    Passerelle: 192.168.10.1                   │
  │    DNS: 192.168.10.5                          │
  │    Bail: 8 heures                             │
```

Le `DHCP Request` est envoyé en broadcast pour informer les autres serveurs DHCP éventuels que le client a choisi une offre précise.

---

## 3. Pourquoi DHCP utilise UDP ?

DHCP utilise **UDP**, avec les ports suivants :

| Port | Utilisation |
| --- | --- |
| `67/UDP` | Serveur DHCP |
| `68/UDP` | Client DHCP |

Au moment du `DHCP Discover`, le client n'a pas encore d'adresse IP. Il ne peut donc pas établir une connexion TCP complète.

UDP permet d'envoyer directement un message en **broadcast**, sans connexion préalable.

---

## 4. La durée de bail

Le **bail DHCP** correspond à la durée pendant laquelle une adresse IP est réservée pour un client.

Exemple : si le serveur donne `192.168.10.50` avec un bail de 8 heures, cette adresse est considérée comme attribuée à ce client pendant 8 heures.

### Renouvellement du bail

| Moment | Comportement du client |
| --- | --- |
| À 50 % du bail | Le client tente un renouvellement en unicast. |
| À 87,5 % du bail | Si le renouvellement a échoué, il retente plus largement. |
| À expiration | Si aucun renouvellement ne fonctionne, il recommence depuis `DHCP Discover`. |

### Bail court ou bail long ?

| Type de bail | Avantage | Inconvénient |
| --- | --- | --- |
| Court, par exemple 1 heure | Libère vite les adresses des clients partis | Génère plus de trafic DHCP |
| Long, par exemple 24 heures | Stable et peu bavard | Peut garder des adresses inutilisées trop longtemps |

---

## 5. Observer DHCP avec Wireshark

Dans Wireshark, on peut filtrer les échanges DHCP avec :

```text
bootp
```

Selon la version de Wireshark, le filtre suivant peut aussi fonctionner :

```text
dhcp
```

Options DHCP importantes à repérer :

| Option | Nom | Rôle |
| --- | --- | --- |
| `53` | DHCP Message Type | Type de message : Discover, Offer, Request, ACK |
| `1` | Subnet Mask | Masque de sous-réseau |
| `3` | Router | Passerelle par défaut |
| `6` | DNS Servers | Serveurs DNS |
| `51` | IP Address Lease Time | Durée du bail |

Valeurs fréquentes de l'option `53` :

| Valeur | Message |
| --- | --- |
| `1` | Discover |
| `2` | Offer |
| `3` | Request |
| `5` | ACK |

---

## 6. Configuration DHCP sur Cisco IOS

### Exclure les adresses réservées

Les adresses de passerelle, serveurs, imprimantes ou équipements réseau fixes ne doivent pas être distribuées par DHCP.

```bash
R1(config)# ip dhcp excluded-address 192.168.10.1 192.168.10.10
```

Ici, les adresses de `192.168.10.1` à `192.168.10.10` ne seront jamais données automatiquement.

### Créer un pool DHCP

```bash
R1(config)# ip dhcp pool LAN-Administration
R1(dhcp-config)# network 192.168.10.0 /24
R1(dhcp-config)# default-router 192.168.10.1
R1(dhcp-config)# dns-server 192.168.10.5
R1(dhcp-config)# domain-name alpesnet.local
R1(dhcp-config)# lease 0 8 0
R1(dhcp-config)# exit
```

Lecture de la configuration :

| Commande | Rôle |
| --- | --- |
| `network 192.168.10.0 /24` | Définit le réseau concerné par le pool |
| `default-router 192.168.10.1` | Indique la passerelle fournie aux clients |
| `dns-server 192.168.10.5` | Indique le serveur DNS fourni aux clients |
| `domain-name alpesnet.local` | Définit le domaine DNS local |
| `lease 0 8 0` | Définit un bail de 0 jour, 8 heures, 0 minute |

### Commandes de vérification

```bash
R1# show ip dhcp binding
```

Affiche les adresses actuellement attribuées.

```bash
R1# show ip dhcp server statistics
```

Affiche le nombre de `Discover`, `Offer`, `Request`, `ACK`, etc. Si les compteurs progressent dans le bon ordre, le processus DORA fonctionne.

```bash
R1# show ip dhcp pool
```

Affiche l'état du pool : nombre d'adresses disponibles, utilisées et exclues.

```bash
R1# show ip dhcp conflict
```

Liste les conflits détectés, par exemple une adresse déjà utilisée manuellement sur le réseau.

---

## 7. Sécurité : DHCP Starvation

!!! warning "Attaque DHCP Starvation"
    Un attaquant peut envoyer un grand nombre de `DHCP Discover` avec des adresses MAC falsifiées. Le serveur réserve alors des adresses pour de faux clients jusqu'à épuiser le pool DHCP.

Conséquence : les vrais clients ne peuvent plus obtenir d'adresse IP.

La contre-mesure principale côté switch est **DHCP Snooping**. Le switch distingue les ports de confiance, où un serveur DHCP est autorisé, des ports non autorisés, où les réponses DHCP suspectes sont bloquées.

À retenir :

- les ports vers les vrais serveurs DHCP sont configurés comme **trusted** ;
- les ports utilisateurs restent **untrusted** ;
- les messages DHCP anormaux peuvent être filtrés ;
- cette protection limite les attaques de type faux serveur DHCP ou saturation DHCP.

---

## 8. Résumé express

| Élément | À retenir |
| --- | --- |
| DHCP | Automatise la configuration IP des clients |
| DORA | Discover, Offer, Request, ACK |
| Transport | UDP `67` serveur, UDP `68` client |
| Broadcast | Nécessaire au début, car le client n'a pas encore d'IP |
| Bail | Durée de réservation d'une adresse |
| Wireshark | Filtre `bootp` ou `dhcp` |
| Cisco IOS | `ip dhcp pool`, `default-router`, `dns-server`, `lease` |
| Sécurité | DHCP Snooping contre les abus DHCP |

---

## Sources

- [RFC 2131 — Dynamic Host Configuration Protocol](https://datatracker.ietf.org/doc/html/rfc2131)
- [RFC 2132 — DHCP Options and BOOTP Vendor Extensions](https://datatracker.ietf.org/doc/html/rfc2132)
- [RFC 1034 — Domain Names: Concepts and Facilities](https://datatracker.ietf.org/doc/html/rfc1034)
- [Cisco — Catalyst 6500 Series Switches documentation](https://www.cisco.com/c/en/us/support/switches/catalyst-6500-series-switches/series.html)
