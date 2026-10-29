# 4.4 — Atelier 4 | Préparer les essais de segmentation

## 🎯 Objectif et modalités

Préparer la mise en œuvre et la validation des règles de filtrage dans un environnement simulé.

**Modalité :** démonstration et briefing avec le formateur. **Environnement :** laboratoire frigorifique Python/Modbus et Linux. L’après-midi d’autonomie sera consacré à la configuration, aux essais et à leur documentation.

!!! info "État des éléments disponibles"
    Le code et `docs/NETWORK.md` du laboratoire ont été examinés. Ce document propose une organisation IT/DMZ/OT et un pseudocode de filtrage ; **il ne donne pas les noms des espaces réseau, interfaces ou adresses de la topologie du TP**. Ceux-ci restent à relever dans le complément du formateur. La présente fiche prépare les tests, sans créer d’espace réseau, charger de règle, démarrer de service ou déclarer la démonstration effectuée.

!!! note "Complément préparé en 4.5"
    Une [topologie de substitution à quatre namespaces](mettre-en-oeuvre-filtrage-it-ot.md) est désormais proposée et déposée sur la VM Debian 192.168.122.105, avec IP/interfaces précises. Elle n’est pas présentée comme fournie/validée par le formateur ; création et application sont désormais attestées par le run de 4.5 après sudo local, avec résultats et limites précisés dans cette fiche. Le constat ci-dessus concerne le document NETWORK.md initial.

## 1 — Identifier les composants du laboratoire

| Élément logiciel | Fonction réelle dans le PoC | Point d’attention pour la segmentation |
| --- | --- | --- |
| `lab/model.py` | Objet `Plant` : physique simplifiée, capteur/porte, régulation, commande et alarme. | Ce contrôleur est du Python, pas REG-02 physique ni un Runtime OpenPLC. |
| `lab/server.py` | Héberge le modèle et le serveur Modbus ; par défaut `127.0.0.1:15020`. | Son arrêt arrête la simulation ; son redémarrage réinitialise l’état. Écoute et adresse à adapter uniquement selon la topologie fournie. |
| `lab/gateway.py` | Passerelle de lecture : écoute `127.0.0.1:15021`, relaie vers `127.0.0.1:15020` par défaut ; seules FC01–FC04 autorisées. | Les écritures sont refusées applicativement. Si le port direct reste joignable, cette restriction est contournable. |
| `lab/dashboard.py` | Supervision HTTP, `127.0.0.1:18080` par défaut ; interroge le serveur Modbus. | Cible Modbus directe par défaut, pas passerelle automatique. Vérifier ses paramètres `--plc-host` et `--plc-port` selon le chemin de consultation retenu. |
| `lab/client.py` | Client de lecture et commande, cible réglable par `--host` / `--port`. | `status` émet FC03, FC04 et FC01 ; chaque requête ouvre une nouvelle connexion TCP. |

Ce PoC ne reproduit pas les trois zones Montval, le logiciel obsolète de REG-02, l’intégration STOCK/ORDER/SUPPLIER ni toutes les capacités de GW-02 imaginées en 4.3. La passerelle fournie n’a pas de rôle de maintenance avec écritures autorisées. Une partie seulement de la politique 4.2–4.3 pourra être représentée ; noter ce qui est testé, non représenté ou à préparer.

## 2 — Découvrir et renseigner la topologie de test

### Principes documentés dans le laboratoire

Le fichier [NETWORK.md fourni — copie de référence](../../assets/files/informatique-industrielle/it-3/PoC-NETWORK-reference.txt) décrit une cible de cours avec un environnement **OT**, une **DMZ/passerelle** et un **client IT**. Le chemin recherché est :

```text
Client IT → point de filtrage / service DMZ autorisé → passerelle → serveur OT
Client IT ── accès direct au serveur OT interdit
```

Le lieu exact du filtrage (routeur, hôte, bridge ou combinaison) dépend de la topologie fournie. Le document source marque les namespaces et règles comme non testés dans son environnement de rédaction : ce statut ne constitue ni un résultat actuel ni une topologie déjà préparée sur la VM de l’apprenant. Son pseudocode n’est pas un fichier à charger.

### Fiche de topologie à compléter au briefing

Les symboles ci-dessous sont des **champs à renseigner**, pas des noms ou adresses déjà présents.

| Paramètre | Information à relever | État actuel |
| --- | --- | --- |
| `NS_IT`, `NS_GW`, `NS_OT` | Espaces réseau ou environnements séparés des clients, passerelle et serveur. | À fournir/confirmer ; si VM/conteneurs, adapter la méthode d’exécution. |
| `NS_FW` | Espace contenant le point de filtrage, s’il est distinct. | À confirmer ; ne pas supposer que GW route les paquets. |
| Interfaces IT/DMZ/OT | Noms, voisinages, adresses, routes et points de passage réels. | À relever ; aucun `veth` ni sous-réseau inventé. |
| `IP_GW_IT` / `IP_GW_OT` | Adresses d’entrée de consultation et de sortie vers le serveur, si interfaces distinctes. | À fournir ; vérifier la source réellement vue par le serveur. |
| `IP_OT` | Adresse de service du serveur OT accessible au seul chemin autorisé. | À fournir. |
| `PORT_OT` / `PORT_GW` | Ports réellement retenus dans le TP. | Valeurs PoC **15020 / 15021**, à confirmer ; **502** vient de la conception Montval, pas d’un changement automatique du PoC. |
| `PORT_HTTP`, origine navigateur | Port et chemin de consultation web si inclus. | **18080** par défaut ; adresse d’écoute et éventuel tunnel à préciser. |
| Paramètres des services | Écoutes serveur/GW, cible amont GW, cible Modbus dashboard et environnement Python. | À relever avec les commandes de lancement réellement utilisées. |
| Filtrage et administration | Hook, interfaces, règles existantes, accès de gestion à préserver et procédure de retour arrière. | À convenir avec le formateur avant configuration. |
| Capture / preuves | Interface et espace de capture de chaque côté du filtre ; fichiers, horaires et responsable. | À renseigner. |

**Localhost n’est pas une liaison interzones.** `127.0.0.1` désigne la boucle locale de l’espace réseau où s’exécute le processus. Après séparation, conserver ces valeurs partout ne connecte pas les espaces entre eux. Inversement, garder tous les processus sur le même loopback et ne filtrer que `forward` ne prouve pas une segmentation. Choisir `input`, `output`, `forward` ou un point adapté aux paquets réellement traversants ; voir [4.2](definir-acces-regles-pare-feu.md#5-traduction-nftables-emplacement-et-limites).

Une consultation via tunnel SSH peut être vue côté service comme une connexion issue de l’extrémité du tunnel : consigner ce chemin pour interpréter les sources. Ne pas ouvrir globalement une écoute pour résoudre une erreur de routage ; utiliser l’interface privée prévue pour le TP et les contrôles convenus.

### État de départ à consigner

Avant les essais, relever date, version/copie du code (notamment seuils modifiés en J1), consigne, température, compresseur, porte, défaut capteur et mode auto. Pour comparer les états, éviter un redémarrage non documenté de `lab.server`. Relever aussi écoutes, routes et règles **dans chaque espace concerné**, pas uniquement sur l’hôte.

## 3 — Plan de vérification préparé

[Télécharger le plan d’essais CSV](../../assets/files/informatique-industrielle/it-3/Montval-4.4-plan-essais-segmentation.csv)

Les tests sont sélectionnés à partir de R10, R01/R99 et Q00/Q10/Q11 de la conception : lecture par le chemin admis, absence de chemin direct et refus applicatif des écritures. **Ils illustrent ces objectifs sans prouver que les règles Montval sont déployées à l’identique.** La recette de maintenance avec écriture autorisée n’est pas fournie par le simple proxy de lecture.

| Test | Origine → destination, protocole/port | Résultat attendu | Méthode et preuves à préparer |
| --- | --- | --- | --- |
| **T00 — Prérequis** | Environnements OT/GW ; écoutes sur leurs adresses et ports retenus. | Serveur et passerelle disponibles ; état initial connu. | `ss` dans les bons espaces, paramètres de lancement et chemins/routage ; noter les versions et états. |
| **T01 — GW vers OT** | Client exécuté dans l’environnement GW → `IP_OT:PORT_OT`, Modbus TCP. | Lecture depuis la source aval autorisée. | `status`, capture amont OT et compteur ; vérifier l’adresse source vue au point de filtrage. |
| **T02 — Consultation IT** | Client IT → `IP_GW_IT:PORT_GW`, Modbus TCP. | Lecture via passerelle possible avant/après filtrage ; paramètres cohérents avec le modèle. | `status` et captures des requêtes/réponses côté IT/GW et GW/OT. Température progressive, pas nécessairement identique entre relevés espacés. |
| **T03 — Écriture de consigne via GW** | Client IT → passerelle, FC06 sur `PORT_GW`. | Refus **applicatif**, exception 01 ; consigne inchangée. | Essai `setpoint 6` seulement sur le modèle convenu ; relever exception puis relire. Si accepté par erreur, constater l’écart et rétablir la consigne par un chemin autorisé. |
| **T04 — Direct IT vers OT** | Client IT → `IP_OT:PORT_OT`, Modbus TCP. | Refus **réseau** après filtrage ; aucun accès direct au serveur. | Tentative de lecture, capture et compteurs du point de refus ; T01 confirme en parallèle la disponibilité du serveur. Ne pas conclure sur un timeout seul. |
| **T05 — Écriture de porte via GW** | Client IT → passerelle, FC05 sur `PORT_GW`. | Exception 01 ; état de porte inchangé. | Essai `door 1` uniquement sur le modèle ; relever l’état initial et relire après refus. Si anomalie, consigner et restaurer par voie autorisée. |
| **T06 — Source/service non autorisé** | Origine, cible et port fournis par le formateur, distincts des permissions. | Refus conforme à la matrice. | Préparer une cible de service effectivement disponible et la source non autorisée ; sinon test non prêt, pas « réussi ». |
| **T07 — Supervision** | Navigateur autorisé → dashboard HTTP, `PORT_HTTP` ; cible Modbus selon paramètres effectifs. | Vue disponible par le chemin prévu, données de collecte accessibles. | Relevés HTTP/CLI horodatés et paramètres de collecte. Si la vue est hors du périmètre fourni, marquer test non représenté. |
| **T08 — Perte du GW** | Arrêt de la passerelle seulement ; observation locale autorisée du serveur/modèle. | Lecture via GW perdue ; processus et contrôle local continuent si indépendants. | Vérifier le processus serveur et des relevés locaux OT ; documenter l’indisponibilité de la vue. Ne pas arrêter le serveur ni présumer que l’IHM signale correctement une valeur périmée. |
| **T09 — Révocation d’accès** | Session persistante du service temporaire réellement implémenté. | Plus de nouvelle ouverture ni poursuite non autorisée après révocation ; collecte normale maintenue. | Client gardant réellement le même socket, session/conntrack ciblés et capture. À préparer si le TP couvre ce scénario : la CLI standard ne démontre pas ce cas. |
| **T10 — Reprise du GW** | Client autorisé → passerelle relancée et observation locale OT. | Lectures courantes rétablies, paramètres inchangés ; serveur non réinitialisé par le redémarrage du GW. | Relecture des valeurs et consigne ; état du serveur et compte rendu de reprise. |

Les états T06/T09 sont **à préparer au briefing** ; les autres restent **à réaliser** dans la topologie confirmée. Aucun résultat observé n’est prérempli.

### Trois diagnostics à distinguer

| Observation | Ce qu’elle permet de dire | Ce qu’elle ne démontre pas |
| --- | --- | --- |
| Réponse Modbus d’exception 01 | Un service a reçu la requête et l’a rejetée applicativement ; attendu du proxy pour FC05/FC06. | Pas une preuve de blocage réseau du port direct. |
| Connexion refusée immédiatement | Un refus actif/RST peut provenir de la cible ou d’un contrôle réseau. | Ne permet pas seul de distinguer service arrêté, mauvaise écoute et règle de rejet. |
| Timeout / absence de réponse | Aucun résultat obtenu dans le délai du client. | Ne prouve pas une règle `drop` : contrôler routage, écoute, compteurs et capture aux bons points. |

Un compteur qui augmente atteste un passage dans la règle, pas nécessairement la réussite applicative. Une lecture réussie via GW ne prouve pas que le chemin direct a été fermé : tester les deux séparément. Les refus n’ont de sens qu’avec une cible et un chemin de référence connus disponibles.

## 4 — Commandes à préparer, sans exécution dans cette fiche

Ces exemples sont à adapter à une topologie **confirmée utilisant des namespaces**. Ils ne créent aucun réseau ni règle. Pour des VM/conteneurs, exécuter les mêmes opérations dans leurs consoles/environnements réels. Depuis la racine de la copie de laboratoire choisie, avec Python et `lab/` accessibles à la commande lancée :

```bash
# Variables à renseigner avec le formateur, sans reprendre des valeurs fictives.
: "${NS_IT:?Renseigner le namespace du client IT}"
: "${IP_GW_IT:?Renseigner l’adresse de la passerelle côté IT}"
: "${PORT_GW:?Renseigner le port de consultation}"

sudo ip netns exec "$NS_IT" python3 -m lab.client status   --host "$IP_GW_IT" --port "$PORT_GW"
```

Pour T03, seulement sur le modèle de simulation et dans le cadre d’essai convenu :

```bash
: "${NS_IT:?Renseigner le namespace du client IT}"
: "${IP_GW_IT:?Renseigner l’adresse de la passerelle côté IT}"
: "${PORT_GW:?Renseigner le port de consultation}"

sudo ip netns exec "$NS_IT" python3 -m lab.client setpoint 6   --host "$IP_GW_IT" --port "$PORT_GW"

sudo ip netns exec "$NS_IT" python3 -m lab.client status   --host "$IP_GW_IT" --port "$PORT_GW"
```

**Attendu T03, non observé ici :** message `Modbus exception code 1`, puis consigne toujours égale à l’état initial. Le client fourni ouvre un nouveau socket par requête ; exécuter deux commandes successives ne valide donc pas T09 sur une session existante.

Pour T04 :

```bash
: "${NS_IT:?Renseigner le namespace du client IT}"
: "${IP_OT:?Renseigner l’adresse du serveur OT}"
: "${PORT_OT:?Renseigner le port du serveur OT}"

sudo ip netns exec "$NS_IT" python3 -m lab.client status   --host "$IP_OT" --port "$PORT_OT"
```

**Attendu T04, non observé ici :** absence d’accès direct corrélée aux traces du filtrage. Définir aussi où exécuter les captures : `lo` convient au PoC initial, mais une topologie séparée impose les interfaces et espaces où passent effectivement les échanges.

## 5 — Briefing et preuves pour l’autonomie

Avant de commencer l’après-midi, confirmer avec le formateur :

- La topologie, les adresses/interfaces/routes, les écoutes et les paramètres des services ; le périmètre réellement représenté et les tests non couverts.
- Les règles à appliquer, leur emplacement et l’accès d’administration à préserver ; méthode de retour arrière et responsable en cas d’écart.
- L’état initial, les opérations d’écriture permises **sur le modèle**, les critères de réussite et d’arrêt d’essai.
- Les points de capture et la distinction refus réseau/refus applicatif ; preuve d’une cible disponible et d’un passage par la règle.
- Les essais de panne/reprise et, si retenu, l’outil de session persistante pour T09.

Conserver ensuite : plan rempli (origine, destination, protocole, port), versions et état initial, règles réellement utilisées, résultats attendus/observés, captures/traces avec horaires, écarts, restauration de l’état et limites. Une modification de filtrage ne doit pas être confondue avec une protection complète de REG-02 réel.

**Production actuelle :** préparation des essais et CSV renseignés avec attentes et champs manquants. Démonstration, paramètres définitifs, configuration, résultats et bilan collectif restent à documenter.

## Ressources

- Laboratoire fourni : `livrables/informatique-industrielle/ot-refrigeration-poc/`, `README.md`, `docs/NETWORK.md`, `docs/REGISTER_MAP.md`, `lab/server.py`, `lab/gateway.py`, `lab/dashboard.py`, `lab/client.py` et `lab/modbus.py` examinés.
- [Copie de référence de NETWORK.md](../../assets/files/informatique-industrielle/it-3/PoC-NETWORK-reference.txt) — document source, pas procédure d’installation de la topologie du TP.
- [4.2 — Politique de filtrage](definir-acces-regles-pare-feu.md) et [4.3 — Protection REG-02](proteger-regulateur-industriel-obsolete.md).

[Retour à l’itération 3](index.md) · [Pense-bête](../../pense-bete/glossaire/informatique-industrielle/it-3.md)
