# Commandes Linux

## Commandes ajoutées

| Commande | Rôle | Exemple | À retenir |
| --- | --- | --- | --- |
| `screen` | Lancer une session terminal détachable, utile pour laisser tourner une commande même si la connexion SSH se coupe. | `screen -S sauvegarde` | Détacher : `Ctrl+a` puis `d`. Reprendre : `screen -r sauvegarde`. Lister : `screen -ls`. |
| `ls -of` | Afficher les fichiers en format long sans la colonne groupe, triés par nom. | `ls -of /etc` | `-o` affiche comme `ls -l` mais sans le groupe. `-f` ne trie pas et affiche aussi les entrées dans l'ordre du répertoire ; avec GNU `ls`, `-f` active aussi l'affichage des fichiers cachés. |

### `screen`

`screen` sert à garder une commande active dans une session indépendante du terminal courant. C'est pratique en SSH pour une sauvegarde, une mise à jour ou une commande longue.

```bash
screen -S sauvegarde
./backup_configs.sh
```

Raccourcis utiles :

| Action | Commande |
| --- | --- |
| Détacher la session | `Ctrl+a` puis `d` |
| Lister les sessions | `screen -ls` |
| Reprendre une session nommée | `screen -r sauvegarde` |
| Quitter une session | `exit` dans la session |

### `ls -of`

`ls -of` affiche les fichiers avec un format proche de `ls -l`, mais sans la colonne du groupe.

```bash
ls -of
ls -of /var/log
```

Exemple de lecture :

```text
-rw-r--r-- 1 root  1234 juin 25 10:12 syslog
```

Dans cette sortie, on voit le type, les permissions, le nombre de liens, le propriétaire, la taille, la date et le nom. La colonne groupe n'est pas affichée à cause de `-o`.

!!! note "Attention à `-f`"
    Sur GNU/Linux, `ls -f` désactive le tri et affiche les entrées dans l'ordre du système de fichiers. Il peut aussi afficher les fichiers cachés. Pour un affichage long classique avec propriétaire mais sans groupe, `ls -o` suffit souvent.

## Ubuntu CLI Cheat Sheet 2025

<div class="pdf-viewer-panel" aria-label="Visionneuse PDF commandes Linux">
  <div class="pdf-viewer-toolbar">
    <h2>Ubuntu CLI Cheat Sheet 2025</h2>
    <div class="pdf-viewer-actions">
      <a
        class="pdf-viewer-link"
        href="../../assets/img/ubuntu_cli_cheat_sheet_2025.pdf"
        target="_blank"
        rel="noopener"
      >
        Ouvrir
      </a>
      <a
        class="pdf-viewer-link"
        href="../../assets/img/ubuntu_cli_cheat_sheet_2025.pdf"
        download
      >
        Télécharger
      </a>
    </div>
  </div>
  <iframe
    class="pdf-frame"
    title="Ubuntu CLI Cheat Sheet 2025"
    src="../../assets/img/ubuntu_cli_cheat_sheet_2025.pdf"
  ></iframe>
</div>
