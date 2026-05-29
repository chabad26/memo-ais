# Installation des outils réseau

## GNS3

GNS3 sert à construire des topologies réseau et à faire tourner des images Cisco pour s'entraîner dans un environnement proche du réel.

```bash
sudo add-apt-repository ppa:gns3/ppa
sudo apt update
sudo apt install gns3-gui gns3-server
sudo usermod -aG ubridge,libvirt,kvm,wireshark $USER
```

Après installation, se déconnecter puis se reconnecter.

```bash
gns3 --version
groups $USER
```

À retenir :

- `ubridge`, `libvirt`, `kvm` et `wireshark` doivent apparaître dans les groupes.
- Au premier lancement, choisir **Run the topologies on my local computer**.
- Si l'état est **Connected**, GNS3 est prêt.

## Wireshark

Wireshark sert à capturer et lire le trafic réseau.

```bash
sudo apt install wireshark tshark
sudo usermod -aG wireshark $USER
```

```bash
wireshark
wireshark capture.pcapng
tshark -i eth0 -w capture.pcapng
```

## Outils réseau utiles

```bash
sudo apt install net-tools ipcalc nmap traceroute mtr dnsutils bind9-utils
```

Outils console pour accès à distance :

```bash
sudo apt install screen minicom
screen /dev/ttyUSB0 9600
```

Quitter `screen` : `Ctrl+A`, puis `K`.
