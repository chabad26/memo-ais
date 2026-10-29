# TP Docker : filtrer les échanges IT / DMZ / OT

Le procédé et l'automate sont simulés en Python. Les échanges TCP et le filtrage
nftables sont réellement exécutés dans les conteneurs Linux.

Depuis la racine du labo :

```bash
docker compose up --build -d --wait
docker compose ps
```

## Topologie et chemin des paquets

| Zone | Réseau | Service | Adresse |
| --- | --- | --- | --- |
| IT | 172.30.81.0/24 | maintenance | 172.30.81.10 |
| DMZ | 172.30.82.0/24 | gateway | 172.30.82.10 |
| DMZ | 172.30.82.0/24 | dashboard | attribuée par Docker |
| OT | 172.30.83.0/24 | plc | 172.30.83.10 |
| Trois zones | Chaque réseau | firewall | .254 dans chaque zone |

Le pare-feu active le routage IPv4 et applique une politique `forward drop`.
Les services utilisent ses adresses comme points d'entrée NAT :

- IT → `172.30.81.254:15021` → DNAT vers gateway DMZ : autorisé.
- Gateway → `172.30.82.254:15020` → DNAT vers plc OT : autorisé.
- IT → `172.30.81.254:15020` → DNAT vers plc OT : bloqué par défaut.
- Dashboard → gateway : accès dans la même DMZ, puis passage par le pare-feu vers OT.

Le SNAT (`masquerade`) assure le chemin retour sans ajouter de routes dans les
conteneurs applicatifs. Il masque l'adresse source au destinataire ; les règles
`forward` la voient avant SNAT. Il s'agit d'un TP de routage avec NAT, pas d'un
routage transparent entre les trois sous-réseaux. Les réseaux IT et OT sont
`internal`; aucun port Modbus n'est publié sur l'hôte.

## 1. Lecture autorisée via la passerelle

```bash
docker compose exec maintenance python -m lab.client status --host 172.30.81.254 --port 15021
```

Attendu : température, consigne et états. La réponse confirme le chemin
IT → pare-feu → passerelle → pare-feu → automate.

## 2. Écriture refusée par la passerelle Modbus

```bash
docker compose exec maintenance python -m lab.client setpoint 50 --host 172.30.81.254 --port 15021
```

Attendu : `Modbus operation failed`, code de sortie 1. La connexion TCP est
permise ; le refus vient du filtrage applicatif de la passerelle.

## 3. Accès direct bloqué par le pare-feu

```bash
docker compose exec maintenance python -m lab.client status --host 172.30.81.254 --port 15020
docker compose exec firewall nft list counters ip lab
```

Attendu : délai d'attente d'environ trois secondes, `TimeoutError`, sortie non
nulle. Le compteur `blocked` augmente. Un timeout isolé ne prouve pas un blocage :
le corréler aux compteurs et à l'ouverture contrôlée de l'étape suivante.

## 4. Ouvrir temporairement le flux direct et simuler une mauvaise consigne

```bash
docker compose exec firewall nft add rule ip lab exercise ip saddr 172.30.81.10 ip daddr 172.30.83.10 tcp dport 15020 counter name direct_test accept
docker compose exec maintenance python -m lab.client status --host 172.30.81.254
docker compose exec maintenance python -m lab.client setpoint 50 --host 172.30.81.254
docker compose exec maintenance python -m lab.client status --host 172.30.81.254
```

Attendu : lecture et écriture acceptées, consigne affichée à 50 °C. Le pare-feu
filtre des flux TCP, il ne distingue pas lecture et écriture Modbus. Autoriser
ce chemin permet donc de contourner la passerelle applicative.

## 5. Restaurer le procédé, refermer et retester

```bash
docker compose exec plc python -m lab.client setpoint 4
docker compose exec firewall nft flush chain ip lab exercise
docker compose exec maintenance python -m lab.client status --host 172.30.81.254
docker compose exec maintenance python -m lab.client status --host 172.30.81.254 --port 15021
docker compose exec firewall nft list table ip lab
```

Attendu : accès direct de nouveau en timeout ; lecture via passerelle toujours
possible, consigne à 4 °C. Les commandes CLI créent de nouvelles connexions.
Une session TCP déjà établie reste autorisée par la règle `established,related`
jusqu'à sa fermeture ou expiration.

## Observer et conserver des preuves

```bash
docker compose exec firewall nft -a list table ip lab
docker compose exec firewall ip -br address
docker compose exec firewall tcpdump -ni any -p tcp port 15020 or tcp port 15021
```

Lancer tcpdump dans un second terminal, puis les tests depuis `maintenance`.
Arrêter avec Ctrl+C. Pour enregistrer une capture dans le dossier courant
(depuis un shell Bash, par exemple sous Linux ou WSL) :

```bash
docker compose exec -T firewall tcpdump -ni any -p -U -w - 'tcp port 15020 or tcp port 15021' > capture-ot.pcap
```

Ouvrir ensuite le fichier dans Wireshark sur l'hôte. Associer captures, compteurs,
commandes et résultats attendus au compte rendu. `docker compose logs` montre
les journaux des applications ; les paquets bloqués sont observés ici via
compteurs et tcpdump, sans dépendre des journaux noyau de l'hôte.

## Revenir à la configuration fournie

```bash
docker compose exec firewall nft -f /app/network/firewall.nft
```

Cette commande recharge uniquement la table `ip lab` du conteneur. Ne pas lancer
les règles sur l'hôte. Les utilisateurs ayant accès au démon Docker peuvent
contourner le montage ; ce TP ne les isole pas. Le noyau Docker doit prendre en
charge nftables et les capacités réseau ; en cas d'erreur de permission ou de
module absent, consulter `docker compose logs firewall`.

Validation effectuée sous Linux le 29 octobre 2026 : les cinq étapes ci-dessus,
l'API HTTP et les 12 tests du simulateur passent. Windows/macOS non vérifiés.

Référence de conception : [réseaux bridge Docker](https://docs.docker.com/engine/network/drivers/bridge/).
