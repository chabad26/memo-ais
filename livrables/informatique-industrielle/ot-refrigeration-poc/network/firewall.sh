#!/bin/sh
set -eu
# Seule la table de ce labo, dans le namespace du conteneur, est remplacée.
nft list table ip lab >/dev/null 2>&1 || nft add table ip lab
nft -f /app/network/firewall.nft
exec sleep infinity
