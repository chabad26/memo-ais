# AIS / OT — Refrigeration digital-twin proof of concept

**Reference training laboratory, tested core, dated 13 October 2026.**

This archive implements a **fictional** refrigeration installation: process physics, a software-simulated controller, a standard Modbus TCP subset, browser supervision, a read-only Modbus gateway and tests. The installation is described in the scenario; learners do **not** have access to a real refrigerator or PLC. It is a *digital-twin prototype of the specification*, not a live synchronized twin or a safety-certified controller.

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
2. **Not tested here:** Wireshark GUI capture, Linux nftables and namespaces, Podman/Docker, FUXA and OpenPLC runtime. No container runtime and no external Python package installation are available in the test environment.
3. The included controller is **Python software**, not an IEC 61131-3 PLC runtime. `optional/` documents how to expand the lab to OpenPLC, but does not falsely claim that the PLC is already connected to the thermal process.
4. This subset intentionally omits Modbus RTU, multiple unit IDs, advanced function codes and authentication. Use upstream tooling for production or broader Modbus conformance tests.
5. Multi-client writes in this demonstration are unrestricted on the direct endpoint. This is deliberate, to illustrate the absence of built-in access control in standard Modbus TCP.
6. The high-temperature alarm occurs above 8 °C after 10 seconds in accelerated demonstration time. The controller accepts setpoints up to 50 °C for the incident demonstration.

## Dependencies / licensing

Core: Python 3 standard library; scripts in this archive released under MIT (see `LICENSE`). Optional products are separate upstream projects under their own licenses and are **not bundled** into this archive. Review their licenses and versions before distribution.
