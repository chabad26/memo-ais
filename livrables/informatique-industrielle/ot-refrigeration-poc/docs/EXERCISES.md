# Instructor proof-of-concept checks (AIS J1–J5)

All examples are confined to the fictional lab.

## J1: Understand the installation

Start `lab.server` and `lab.dashboard` as in README. Describe sensors, compressor, thermostat hysteresis, high-temperature threshold, maintenance pathway. Observe the temperature trend via repeated `python3 -m lab.client status` (browser dashboard also updates). Reset server between independent scenarios.

## J2: Modbus and a model of an installation

Capture `tcp port 15020 or tcp port 15021` on **loopback** with Wireshark/tcpdump if installed. Use `python3 -m lab.client setpoint 6`, `status`, `door 1` and `door 0`. Identify MBAP transaction ID, protocol ID 0, unit ID, FC03/FC04/FC05/FC06, PDU address, response. This is a simplified digital representation of a documented installation; not connected to an actual field device.

## J3: Maintenance, unwanted write

Change setpoint to 50 °C using `python3 -m lab.client setpoint 50`. Observe that the nominal limit shown by holding register 1 is 8 °C yet the controller accepts 50 °C. It illustrates *lack of controller-side validation* in this fictional design. Note timing: temperature changes gradually; an alarm appears only after threshold plus delay. Reset with `setpoint 4` or server restart.

## J4: Protection

Start gateway (`python3 -m lab.gateway`). Read with `python3 -m lab.client status --port 15021`. Attempt `python3 -m lab.client setpoint 50 --port 15021` and observe Modbus exception 1. Confirm direct TCP port 15020 remains writable: **the gateway alone does not provide segmentation**. See NETWORK.md for an isolated network topology and firewall requirements. Test that reads remain possible through gateway.

## J5: Incident simulation and operational tradeoffs

Provide fictitious maintenance work order, asset inventory, vendor advisory, packet capture and timestamps. Learners should: reconstruct an unauthorized change, decide where to intervene, demonstrate blocked writes at the IT/OT boundary, ensure local controller continues running, and propose an update/maintenance test plan.

### Reference acceptance checks

1. `python3 -m unittest discover -s tests -v` returns OK.
2. Browser `http://127.0.0.1:18080` shows changing status.
3. Direct Modbus FC06 modifies setpoint and appears in FC03 and the browser.
4. Gateway supports FC03/FC04 but rejects FC06.
5. PLC direct port cannot be reached from an untrusted zone **only after actual network isolation is configured**.
6. Optional FUXA and OpenPLC exercises are separately evaluated; do not count them as passed core acceptance tests.

### Reset

For a fresh physical/process state stop and restart `lab.server`. There is no on-disk persistence or database.
