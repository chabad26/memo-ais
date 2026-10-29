# AIS / OT — Refrigeration digital-twin proof of concept

**Reference training laboratory, tested core, dated 13 October 2026.**

This archive implements a **fictional** refrigeration installation: process physics, a software-simulated controller, a standard Modbus TCP subset, browser supervision, a read-only Modbus gateway and tests. The installation is described in the scenario; learners do **not** have access to a real refrigerator or PLC. It is a *digital-twin prototype of the specification*, not a live synchronized twin or a safety-certified controller.

## Lancer le labo avec Docker (Linux, Windows ou macOS)

Installer Docker Engine avec le plugin Compose V2, ou Docker Desktop démarré
(en mode conteneurs Linux). Git sert à récupérer le dépôt. Aucune installation
locale de Python ni de paquet pip n'est nécessaire.

Depuis la racine du dépôt `memo-ais` :

```bash
cd livrables/informatique-industrielle/ot-refrigeration-poc
docker compose up --build -d --wait
```

Compose construit deux images locales et démarre cinq services : automate
`plc`, passerelle Modbus `gateway`, supervision `dashboard`, pare-feu `firewall`
et poste IT `maintenance`. Le premier lancement télécharge Python et les outils
réseau. Ouvrir **http://127.0.0.1:18080**.

### Tests de pare-feu et de Modbus

Suivre le [TP réseau et pare-feu](docs/NETWORK.md) : lecture autorisée via la
passerelle, écriture refusée par Modbus, accès direct bloqué par nftables,
ouverture temporaire, écriture directe puis fermeture et nouvelle vérification.
Le guide fournit les commandes et les résultats attendus, ainsi que les compteurs
et la capture tcpdump. Seul le port HTTP `18080` est publié sur l'hôte ; les
anciens ports directs `15020` et `15021` ne sont plus publiés.

Les commandes de maintenance locale restent disponibles pour le formateur :

```bash
docker compose exec plc python -m lab.client status
docker compose exec plc python -m lab.client setpoint 4
docker compose exec plc python -m lab.client door 1
docker compose exec plc python -m lab.client door 0
docker compose exec plc python -m lab.client sensor-fault 1
docker compose exec plc python -m lab.client sensor-fault 0
docker compose exec plc python -m unittest discover -s tests -v
```

`docker compose exec plc` contourne volontairement le réseau pour administrer
le simulateur ; les tests de filtrage doivent partir du service `maintenance`.

### Arrêter et réinitialiser

```bash
docker compose logs --tail=50
docker compose down
# Repartir avec la politique initiale et un procédé neuf
docker compose up --build -d --wait
# Purger les ressources du projet, images incluses
docker compose down --rmi all --volumes --remove-orphans
```

Aucun volume persistant : état du procédé et modifications des règles à chaud
sont perdus à la recréation des conteneurs. Modifier `network/firewall.nft`, puis
reconstruire avec `up --build -d --wait` pour conserver une politique modifiée.
Les sous-réseaux `172.30.81.0/24`, `172.30.82.0/24`, `172.30.83.0/24` doivent être
libres ; en cas de conflit VPN/réseau Docker, adapter ensemble Compose, les règles
et les adresses des commandes du TP. Un port HTTP occupé nécessite de changer
le port à gauche de `127.0.0.1:18080:18080`.

Le pare-feu dispose de `NET_ADMIN` pour nftables et `NET_RAW` pour les captures,
dans son propre espace réseau. Aucun mode `privileged`, réseau hôte ou socket
Docker n'est utilisé. Les autres conteneurs n'ont aucune capacité Linux ajoutée.
La machine hôte et l'utilisateur autorisé à administrer Docker restent hors du
périmètre de protection du TP.

Ce montage reproduit le **simulateur Python**, sans automate matériel, OpenPLC,
FUXA ou interface Wireshark. Tcpdump est fourni dans le conteneur pare-feu.

### Validation Docker réalisée le 29 octobre 2026

Sous Linux, Docker Engine 29.1.3 et Compose V2 2.40.3 : construction, démarrage,
API HTTP, lecture via passerelle, refus Modbus des écritures, blocage réseau,
ouverture temporaire et écriture directe, restauration à 4 °C et nouveau blocage
vérifiés. Les 12 tests existants passent dans le conteneur. Windows et macOS
n'ont pas été testés ici.

## Quick start (Linux, Python >= 3.10, no pip packages)

Open four shells **from the archive's root directory**:

```bash
python3 -m lab.server                 # Modbus TCP 127.0.0.1:15020
python3 -m lab.dashboard              # browser http://127.0.0.1:18080
python3 -m lab.gateway                # read-only Modbus gateway 127.0.0.1:15021
python3 -m lab.client status
```

Explore in the fourth shell:

```bash
python3 -m lab.client setpoint 50     # intentionally unsafe write, direct PLC endpoint
python3 -m lab.client status
python3 -m lab.client status --port 15021        # read through gateway
python3 -m lab.client setpoint 4 --port 15021    # Modbus exception: gateway blocks writes
python3 -m lab.client setpoint 4                 # restore directly
python3 -m lab.client door 1
python3 -m lab.client sensor-fault 1
python3 -m lab.client sensor-fault 0
python3 -m lab.client door 0
```

Read-only browser supervision: **http://127.0.0.1:18080**. The browser HTTP service queries the Modbus controller rather than reading internal Python state.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

Core uses **Python standard library only**. The included test suite covers the thermal model, real TCP request/response framing, client read/write, Modbus errors, gateway filtering, subprocess start-up, and HTTP dashboard.

## Architecture

```text
      HTTP browser              maintenance station (scenario)
           |                                 |
    read-only dashboard                  Modbus client
           |                                 |
           |                   +-------------+-------------+
           |                   |                           |
      [Modbus TCP 15020]  direct port 15020          gateway 15021
           |                   |                    (read-only Modbus)
           +------------- software controller ------------+
                                 |
                         thermal process model
                                 |
                      fictional refrigeration unit
```

**Important security distinction:** The gateway offers application-level filtering of Modbus function codes, but cannot prevent direct access to port 15020 if the network exposes it. The default lab binds all services to loopback; the network-segmentation exercise must apply separate container networks or namespaces and a firewall. Do not expose the deliberately permissive Modbus controller to public networks.

The process model is not intended to represent actual refrigeration thermodynamics, safeguards or food safety standards. Sensor failure intentionally stops the compressor as one **scenario assumption**, not a claim that this is a universally safe industrial design.

## Files

- `lab/model.py`: configurable simulated physics and PLC thermostat logic.
- `lab/modbus.py`, `lab/server.py`, `lab/client.py`: minimal Modbus TCP subset with function codes 1, 2, 3, 4, 5, 6.
- `lab/dashboard.py`: standalone read-only browser HMI.
- `lab/gateway.py`: demonstrator read-only Modbus gateway.
- `tests/`: unit, TCP, gateway, and black-box integration tests.
- `docs/REGISTER_MAP.md`: register mapping and convention.
- `docs/EXERCISES.md`: instructor proof-of-concept checks.
- `docs/NETWORK.md`: network segmentation exercise.
- `optional/`: FUXA/OpenPLC instructions and example Ladder-equivalent Structured Text; **not integrated/tested**.

## Technical scope and limitations

1. **Tested:** standard-library plant/controller, Modbus subset over real TCP, web HMI, read-only gateway.
2. **Not tested here:** Wireshark GUI capture, Linux nftables and namespaces, Podman, FUXA and OpenPLC runtime. Docker Compose validation is recorded separately below.
3. The included controller is **Python software**, not an IEC 61131-3 PLC runtime. `optional/` documents how to expand the lab to OpenPLC, but does not falsely claim that the PLC is already connected to the thermal process.
4. This subset intentionally omits Modbus RTU, multiple unit IDs, advanced function codes and authentication. Use upstream tooling for production or broader Modbus conformance tests.
5. Multi-client writes in this demonstration are unrestricted on the direct endpoint. This is deliberate, to illustrate the absence of built-in access control in standard Modbus TCP.
6. The high-temperature alarm occurs above 8 °C after 10 seconds in accelerated demonstration time. The controller accepts setpoints up to 50 °C for the incident demonstration.

## Dependencies / licensing

Core: Python 3 standard library; scripts in this archive released under MIT (see `LICENSE`). Optional products are separate upstream projects under their own licenses and are **not bundled** into this archive. Review their licenses and versions before distribution.
