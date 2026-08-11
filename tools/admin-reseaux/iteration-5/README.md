# Outils iteration 5 - automatisation reseau

Ce dossier regroupe les fichiers executables et les entrees de l'atelier
`admin-reseaux/iteration-5`.

Depuis la racine du depot :

```bash
tools/admin-reseaux/iteration-5/check_connectivity.sh
SSH_USER=admin tools/admin-reseaux/iteration-5/backup_configs.sh
NET_USER=admin NET_PASSWORD='motdepasse' python3 tools/admin-reseaux/iteration-5/backup_configs_netmiko.py
```

Par defaut, les scripts utilisent les fichiers `hosts.txt` et `equipements.txt`
du meme dossier. Les rapports de connectivite sont ecrits dans `reports/`, et
les sauvegardes de configuration dans `reports/backups/`.
