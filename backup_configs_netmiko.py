#!/usr/bin/env python3
"""
Sauvegarde des configurations AlpesNet avec Netmiko.

Installation avancee:
    pip install netmiko --break-system-packages

Usage:
    NET_USER=admin NET_PASSWORD='motdepasse' python3 backup_configs_netmiko.py
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

from netmiko import ConnectHandler


EQUIPMENT_FILE = Path("equipements.txt")
BACKUP_DIR = Path("backups")
NET_USER = os.environ.get("NET_USER", "admin")
NET_PASSWORD = os.environ.get("NET_PASSWORD", "")
DEVICE_TYPE = os.environ.get("NET_DEVICE_TYPE", "cisco_ios")


def read_equipment(path: Path) -> list[tuple[str, str]]:
    equipment: list[tuple[str, str]] = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) != 2:
            raise ValueError(f"Ligne invalide dans {path}: {raw_line}")

        equipment.append((parts[0], parts[1]))

    return equipment


def build_header(name: str, ip_address: str) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return (
        "! ============================================================\n"
        "! ALPESNET - SAUVEGARDE CONFIGURATION EQUIPEMENT\n"
        f"! Equipement : {name}\n"
        f"! Adresse IP : {ip_address}\n"
        f"! Date       : {now}\n"
        "! Auteur     : Olivier\n"
        "! Commande   : show running-config\n"
        "! ============================================================\n\n"
    )


def backup_device(ip_address: str, name: str) -> Path:
    device = {
        "device_type": DEVICE_TYPE,
        "host": ip_address,
        "username": NET_USER,
        "password": NET_PASSWORD,
    }

    backup_date = datetime.now().strftime("%Y%m%d")
    backup_file = BACKUP_DIR / f"backup_{name}_{backup_date}.cfg"

    with ConnectHandler(**device) as connection:
        connection.send_command("terminal length 0")
        running_config = connection.send_command("show running-config")

    backup_file.write_text(
        build_header(name, ip_address) + running_config + "\n",
        encoding="utf-8",
    )

    return backup_file


def main() -> int:
    if not EQUIPMENT_FILE.exists():
        print(f"ERREUR: fichier introuvable: {EQUIPMENT_FILE}")
        return 1

    if not NET_PASSWORD:
        print("ERREUR: definir NET_PASSWORD avant de lancer le script.")
        return 1

    BACKUP_DIR.mkdir(exist_ok=True)

    ok_count = 0
    error_count = 0

    for ip_address, name in read_equipment(EQUIPMENT_FILE):
        try:
            backup_file = backup_device(ip_address, name)
        except Exception as exc:  # Netmiko remonte plusieurs types d'erreurs SSH.
            error_count += 1
            print(f"[ERROR] {name} ({ip_address}) -> {exc}")
            continue

        ok_count += 1
        print(f"[OK]   {name} ({ip_address}) -> {backup_file}")

    print(f"Resume: {ok_count} sauvegardes OK / {error_count} erreurs")
    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
