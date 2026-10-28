# Register map — Modbus TCP

**Server:** `127.0.0.1:15020`; **gateway:** `127.0.0.1:15021`; unit ID 1 is used in examples. **Zero-based PDU addresses** (not 40001/30001 human-facing labels).

| Type | PDU address | Meaning | Scale / allowed value |
|---|---:|---|---|
| Holding (FC03) | 0 | temperature setpoint | integer deci-°C; 0..500, writable FC06 |
| Holding (FC03) | 1 | documented recommended upper limit | 80 = 8.0 °C, read-only *advisory*, not enforced |
| Holding (FC03) | 2 | automatic mode | 1 auto / 0 pause auto control; writable FC06 |
| Input (FC04) | 0 | current temperature | unsigned 16-bit, deci-°C; toy model clamps at −10 °C but values below zero would require signed handling; normal exercises stay above zero |
| Input (FC04) | 1 | compressor command | 1 on / 0 off |
| Input (FC04) | 2 | alarm | 1 after temp > 8 °C for 10 s |
| Input (FC04) | 3 | sensor fault | 1 fault |
| Coil (FC01/FC05) | 0 | door open | true/false |
| Coil (FC01/FC05) | 1 | injected sensor fault | true/false |
| Discrete input (FC02) | 0 | compressor command | true/false |
| Discrete input (FC02) | 1 | high-temp alarm | true/false |

FC05 on = `0xFF00`; off = `0x0000`. FC06 echoes the written register/address. Invalid addresses yield Modbus exception codes; invalid values yield exception 3. Only the minimal listed function codes are implemented.

**Important:** The 'limit' holding register is deliberately only a documented recommendation. It is not an independently enforced setpoint bound. Learners discover this security/operational discrepancy in J3–J5.
