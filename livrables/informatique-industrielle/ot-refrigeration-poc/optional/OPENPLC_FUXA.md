# Optional integrations — NOT part of the tested reference core

The reference controller is Python, not a deployed OpenPLC runtime. These are **follow-up proof-of-concept tracks**, not claimed working integrations.

## FUXA HMI (container runtime required)

Upstream project: https://github.com/frangoteam/FUXA

Run upstream container in a **private isolated lab network**, following upstream instructions; FUXA commonly listens on 1881. In its Modbus TCP device setup, point to an address **reachable from inside its container** (not `127.0.0.1` unless server shares its network namespace), TCP 15020 or the corresponding forwarded port. Define tags for holding address 0 (setpoint, multiply 0.1), input address 0 (temperature, multiply 0.1), input addresses 1/2 (compressor/alarm), and coil 0 (door). Some UI drivers number tags from 1 rather than zero: verify by reading the known 4.0 °C setpoint first. Do not expose FUXA's web UI to the public Internet; set up authentication/network isolation.

Expected acceptance: correct values shown; one authorized setpoint write reaches the controller; packet capture matches. The exact FUXA tag import/project format has **not** been validated here.

## OpenPLC v4 IEC 61131-3 runtime

Upstream: https://github.com/Autonomy-Logic/openplc-runtime

OpenPLC runtime v4 exposes its management UI by default on HTTPS port 8443. Download/deploy only after verifying exact version and platform compatibility with the Editor. Its Modbus slave plugin and I/O mapping must be configured, and a **bidirectional** Python-process-model link still needs to be designed and tested. `thermostat.st` is example Structured Text logic only, not a compiled or deployed OpenPLC project. It must be adapted for the chosen target addresses, toolchain and control cycle.

Required acceptance before teaching as an OpenPLC exercise:

1. Upload/compile a pinned IEC 61131-3 program in the Editor; start it in the runtime.
2. Confirm actual Modbus TCP plugin bind and register mapping, including read and write access from FUXA.
3. Define process-to-PLC sensor update and PLC-to-process compressor command paths and verify closed-loop execution.
4. Repeat abnormal setpoint, alarm and network-gateway tests with the real OpenPLC runtime substituted for the Python controller.

If any of these fail, use the thoroughly tested Python controller for J3–J5 and describe OpenPLC as an optional demonstration, not part of a validated digital twin.
