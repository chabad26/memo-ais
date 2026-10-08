# Identifier le point d’observation

## 🎯 Objectif

Comprendre où placer l’IDS et déterminer quels échanges il peut observer.
Suricata est installé directement sur **l’hôte** ; la VM hébergeant File Browser
reste la cible surveillée. L’énoncé la désigne comme Ubuntu 20.04 ; après la
migration rapportée dans le mémo, relever son OS actuel sans revenir à 20.04.

Cette feuille précède [Comprendre les événements produits](comprendre-evenements-produits.md)
dans le parcours. Elle est ajoutée après les manipulations : les preuves
ci-dessous restent attribuées à leurs horaires réels, sans inventer une exécution
antérieure de l’activité.

## 1. Reconstituer l’architecture — 10 min

| Élément | État observé le 7 octobre | Limite |
| --- | --- | --- |
| IP cible | `192.168.122.229` | Vérifiée par route, ping et échanges HTTP du laboratoire |
| Bridge de l’hôte | `virbr0`, `192.168.122.1/24`, UP | Point retenu pour les tests hôte → VM |
| Interface virtuelle côté hôte | `vnet1` présente | Association à la VM/bridge à confirmer avec libvirt |
| Interface physique hôte | `enp8s0`, UP | Ne prouve pas que tous les échanges de la VM y sont visibles |
| Interface dans la VM | Nom non fourni | À relever dans la VM avec `ip -br addr` |
| Route hôte → VM | `dev virbr0 src 192.168.122.1` | La route de la VM vers l’extérieur reste à relever |

```text
Réseau extérieur
       |
Interface physique hôte (enp8s0)
       |
Routage / filtrage / NAT éventuel à confirmer
       |
Bridge virbr0 — Suricata sur l’hôte
       |
Interface virtuelle de la VM (association à confirmer)
       |
VM 192.168.122.229 — Docker — File Browser :8080
                       └ serveur HTTP temporaire :18080 (essais)
```

Le NAT est une hypothèse à vérifier dans la configuration libvirt, pas une
conclusion tirée uniquement du sous-réseau `192.168.122.0/24`. Un ping réussi
montre la joignabilité ICMP ; il ne prouve pas la capture HTTP par Suricata.

## 2. Examiner les interfaces et le trajet — 10 min

Commandes à retenir sur l’hôte :

```bash
ip -br addr
ip route
ip route get 192.168.122.229
bridge link
virsh list --all
```

Avec la connexion libvirt qui gère réellement la VM (système ou session),
remplacer les noms avant exécution :

```bash
virsh domiflist NOM_VM
virsh net-list --all
virsh net-dumpxml NOM_RESEAU
```

Rapprocher interface virtuelle, bridge, MAC et réseau de la VM. Si celle-ci
n’apparaît pas, vérifier la connexion utilisée par virt-manager ; ne pas
recréer un réseau pour contourner cette différence.

Dans la VM :

```bash
ip -br addr
ip route
cat /etc/os-release
sudo ss -lntup
sudo docker ps --format 'table {{.Names}}\t{{.Ports}}'
```

Ces relevés identifient interface, passerelle, services en écoute et ports
publiés. Une écoute ne prouve pas l’accessibilité depuis toutes les zones :
la comparer au routage, au filtrage et à un essai autorisé depuis la zone étudiée.

## 3. Répondre aux questions — 15 min

| Question | Réponse fondée sur les éléments disponibles | À compléter |
| --- | --- | --- |
| Quels flux atteignent File Browser ? | Le déploiement documenté publie TCP 8080 vers le port 80 du conteneur pour les opérations HTTP. Les essais récents sur 18080 concernent un autre serveur | Capture et essai applicatif actuels sur 8080 ; sources et zones autorisées |
| Quels flux quittent la VM ? | Les réponses TCP/HTTP du serveur temporaire vers l’hôte sont visibles dans la capture. D’autres sorties sont possibles selon les usages | Observer DNS, téléchargements/mises à jour et autres échanges réellement générés ; relever destinations et protocole, sans les déclarer observés avant capture |
| Quels services sont exposés ? | Le dossier antérieur documente SSH/22 et File Browser/8080. Le serveur temporaire/18080 est accessible depuis l’hôte pendant les essais | Inventaire actuel avec `ss` et Docker ; distinguer exposition au réseau virtuel, au LAN et à Internet. Internet non démontré ; arrêt de 18080 à confirmer |
| Sur quelle interface écouter ? | **`virbr0` pour le trajet hôte → VM testé**. `eth0` n’existe pas sur l’hôte et provoquait l’échec de démarrage | Confirmer chaque trajet supplémentaire par capture ; une interface correcte pour un trajet ne garantit pas la visibilité de tous les flux |
| Quels trafics peuvent rester invisibles ? | Loopback dans la VM, échanges internes au conteneur/réseau Docker de la VM, autre interface/réseau virtuel, flux ne traversant pas ce point | Tester les trajets utiles. Sur HTTPS, les paquets peuvent être visibles mais le contenu HTTP chiffré reste inaccessible à ces signatures |

La présence d’un bridge ne garantit pas l’observation de tous les échanges
entre invités ; vérifier selon leur trajet et la configuration de capture.
Sur l’interface extérieure, un NAT éventuel peut modifier les adresses observées.
Suricata en IDS ne bloque pas les flux et ne corrige pas le filtrage Docker/8080.

## 4. Prouver la visibilité — 10 min

Sur l’hôte, observer un flux connu en utilisant le port réellement testé :

```bash
sudo tcpdump -ni virbr0 'host 192.168.122.229 and tcp port 8080'
```

Depuis un autre terminal hôte, un GET non authentifié vers File Browser peut
servir de contrôle de trajet, sans opérations sur les documents :

```bash
curl --max-time 5 -I http://192.168.122.229:8080/
```

Pour les tests du serveur temporaire de la feuille suivante, utiliser **18080**
dans le filtre. Un filtre sur 8080 ne montre pas les paquets envoyés vers 18080.
Ne pas générer de trafic public ni ouvrir un flux Internet pour cet exercice.
Comparer source/destination, ports, heure et interface ; rapprocher ensuite
les événements Suricata. La visibilité avec tcpdump seule ne prouve pas que
Suricata capture ni qu’une signature se déclenche.

### Preuves disponibles

![Route vers la VM, interfaces et premiers tests](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2010-25-13.png)

**10:25:13 :** route hôte → VM par `virbr0`, bridge UP, interface `vnet1`,
ping réussi et requêtes reçues par le serveur temporaire. Le filtre tcpdump
porte encore sur 8080 : cette image ne prouve pas la capture du test 18080.

![Échanges TCP sur 18080 et événements EVE](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2010-30-55.png)

**10:30:55 :** échanges TCP hôte/VM sur 18080 et quatre alertes EVE corrélées.
Cela établit la visibilité et la détection pour ce test, pas pour tous les
flux de la VM. L’analyse des SID figure dans la feuille suivante.
Les captures restent dans leur dossier de dépôt `it-7` et sont liées ici.

## 📚 Notion acquise — Point d’observation

Un point d’observation est l’endroit du réseau où l’on capture le trafic.
Sa position détermine les flux et adresses visibles ; la présence des paquets
ne garantit pas l’accès à leur contenu, notamment en cas de chiffrement.

## 📦 Livrable

Architecture annotée, relevés d’interfaces/IP/routes, inventaire des services,
justification de `virbr0`, flux effectivement observés et angles morts.
**Établi :** route et test hôte/VM sur 18080 avec alertes. **À compléter :**
interface interne VM, association libvirt, mode NAT/routé, sorties extérieures,
inventaire actuel et contrôle de File Browser/8080. Conserver les preuves
utiles ; ne pas publier secrets ou diagnostics internes sans anonymisation.

- [Étape suivante — Comprendre les événements produits](comprendre-evenements-produits.md)
- [Retour à l’itération 8](index.md)
- [Retour au module](../README.md)
