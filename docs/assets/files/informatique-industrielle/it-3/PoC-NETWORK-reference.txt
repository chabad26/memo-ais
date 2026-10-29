# IT/OT separation (optional supervised lab)

**Tested core:** localhost server + a read-only Modbus function gateway. **Not tested in this environment:** Linux namespaces, firewall rule application, Docker/Podman.

Recommended course topology: three isolated networks: (1) OT plant/controller (port 502 or 15020), (2) DMZ gateway/HMI, (3) IT maintenance workstation. Only authorized DMZ service(s) may reach the PLC's direct Modbus port; IT clients communicate only with DMZ services. Use container networks or Linux network namespaces with IP forwarding disabled by default; grant explicit narrow forwarding paths. Keep internet and campus LAN disconnected from all lab OT networks.

## Firewall pseudocode (not executable configuration)

```text
INPUT on OT PLC:
  accept established/related
  accept TCP from authorized OT/DMZ gateway address to PLC port
  drop all other TCP to PLC port
IT -> DMZ:
  allow TCP to monitored gateway port only
DMZ -> OT:
  allow TCP from gateway IP to PLC port
all other inter-zone forwarding: deny
```

For nftables, implement those policies against the **actual interface names and addresses** of the class VMs/containers; prefer drop-by-default. Never blindly run rules against a remote SSH teaching host: it could disconnect the instructor.

**Security consideration:** Blocking Modbus writes using function codes 5/6 in a sample gateway is insufficient if an operator can bypass it and reach the direct PLC endpoint. Other Modbus function codes supporting writes (e.g. FC15/FC16) would also need consideration in a full-featured gateway. The prototype server does not support those codes, but real devices may.

Capture packet traces from the network namespace containing the relevant inter-zone link, not necessarily from the host's external network interface.
