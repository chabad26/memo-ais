# Glossaire Sécurité des données - Itération 3

| Terme | Définition courte |
| --- | --- |
| Données au repos | Données stockées sur un support et non en cours de transmission. |
| LUKS | Format Linux de chiffrement de périphériques de stockage. |
| Header LUKS | Métadonnées contenant notamment les paramètres et emplacements de clés. |
| Slot de clé | Emplacement permettant d'associer un moyen d'ouverture à un volume LUKS. |
| `cryptsetup` | Outil Linux de création et de gestion de volumes chiffrés. |
| Périphérique loop | Périphérique bloc permettant d'utiliser un fichier comme support. |
| Volume ouvert | Volume dont la couche de chiffrement est accessible via un mapping. |
| Montage | Association d'un système de fichiers à un répertoire. |
| Clé du volume | Clé aléatoire utilisée par LUKS pour chiffrer les données du volume. |
| Rotation d'accès | Ajout et validation d'un nouveau moyen d'accès avant retrait de l'ancien. |
| Fichier témoin | Fichier dont l'empreinte permet de contrôler les données après récupération. |

## Gestes et commandes à retenir

Ces commandes constituent un rappel de la procédure. Elles ne prouvent pas que
la manipulation a été exécutée sur une machine donnée.

```bash
LOOP_DEVICE=$(sudo losetup --find --show luks-disk.img)
sudo cryptsetup luksFormat --type luks2 "$LOOP_DEVICE"
sudo cryptsetup open "$LOOP_DEVICE" data-secure
sudo mkfs.ext4 /dev/mapper/data-secure
sudo mount /dev/mapper/data-secure /mnt/data-secure

sudo umount /mnt/data-secure
sudo cryptsetup close data-secure
sudo losetup --detach "$LOOP_DEVICE"
```

## Docs associées

- [Mettre en œuvre et comprendre un stockage chiffré avec LUKS](../../../securite-donnees/it-3/mettre-en-oeuvre-stockage-chiffre-luks.md)
- [Administrer les accès et préparer la récupération d'un volume LUKS](../../../securite-donnees/it-3/administrer-acces-preparer-recuperation-luks.md)
