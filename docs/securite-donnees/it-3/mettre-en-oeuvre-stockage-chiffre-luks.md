# Mettre en œuvre et comprendre un stockage chiffré avec LUKS

## Objectif

Après la protection des données en transit avec TLS, cette activité porte sur
les données au repos. Un disque retiré d'un serveur, une sauvegarde copiée ou
un ordinateur portable volé peut exposer les données qu'il contient.

Vous allez utiliser LUKS pour créer un stockage chiffré sous Linux. Un fichier
de 512 Mio simulera un disque et sera associé à un périphérique loop.

À la fin de l'activité, vous devrez être capables de :

- expliquer ce que protège le chiffrement des données au repos ;
- créer un stockage chiffré avec LUKS ;
- l'ouvrir, le monter, l'utiliser et le fermer ;
- identifier chaque couche entre le fichier et les données ;
- retrouver les informations importantes d'un volume LUKS.

## Prérequis et règles de sécurité

- travailler sur une machine ou une VM Linux avec `sudo` ;
- disposer de `cryptsetup`, `losetup`, `lsblk` et `mkfs.ext4` ;
- utiliser uniquement le fichier et le périphérique loop de cet exercice ;
- vérifier la cible avant chaque commande `cryptsetup`, `mkfs` ou `losetup` ;
- conserver les commandes et les observations, sans révéler la phrase de passe ;
- ne pas détruire ni sauvegarder le header LUKS aujourd'hui : cette manipulation
  sera étudiée pendant l'itération 4.

!!! danger "Une erreur de périphérique peut détruire des données"
    Ne remplacez jamais `/dev/loopX` par un disque réel comme `/dev/sda`,
    `/dev/vda` ou `/dev/nvme0n1`. Avant le formatage, vérifiez que le loop device
    pointe exactement vers `~/DATA01-J3/luks-disk.img`.

## Partie 1 - Comprendre le besoin

Imaginez un serveur arrêté dont un attaquant retire le disque pour le connecter
à une autre machine.

| Propriété | Protection apportée par LUKS seul | Justification |
| --- | --- | --- |
| Confidentialité | Oui, lorsque le volume est fermé | Sans moyen d'ouverture valide, les blocs stockés ne sont pas lisibles en clair. |
| Intégrité | Non, pas complètement par défaut | Le chiffrement standard avec dm-crypt ne garantit pas que toute modification malveillante des blocs sera détectée. |
| Disponibilité | Non | Un attaquant peut supprimer, endommager ou rendre indisponible le support ou le header. |
| Authenticité | Non | LUKS ne prouve pas à lui seul l'identité de la personne ou de la machine qui a produit les données. |

Lorsque le volume est ouvert, le système peut accéder aux données en clair via
le périphérique mapper. Les droits Unix et la sécurité du système restent donc
nécessaires.

## Partie 2 - Identifier les couches

Avant de commencer, observez les périphériques existants :

```bash
lsblk -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS
```

L'activité construit la chaîne suivante :

```text
fichier image
    |
    v
périphérique loop
    |
    v
conteneur LUKS
    |
    v
périphérique device mapper
    |
    v
système de fichiers ext4
    |
    v
point de montage
    |
    v
données
```

## Partie 3 - Créer le support simulé

### Installer les outils sur Debian 13

Installez les paquets nécessaires avant de créer le support :

```bash
sudo apt update
sudo apt install cryptsetup util-linux e2fsprogs
```

Ces paquets fournissent notamment :

| Paquet | Outils utilisés pendant l'activité |
| --- | --- |
| `cryptsetup` | Création, ouverture, inspection et fermeture du volume LUKS |
| `util-linux` | `losetup`, `lsblk`, `blkid`, `findmnt` et `mount` |
| `e2fsprogs` | Création du système de fichiers avec `mkfs.ext4` |

Vérifiez ensuite la présence des outils et leurs versions :

```bash
command -v lsblk
ls -l /usr/sbin/cryptsetup /usr/sbin/losetup /usr/sbin/mkfs.ext4

sudo cryptsetup --version
sudo losetup --version
sudo mkfs.ext4 -V
```

!!! info "Commandes placées dans `/usr/sbin`"
    Sur Debian, `cryptsetup`, `losetup` et `mkfs.ext4` peuvent être installés
    dans `/usr/sbin`, sans que ce répertoire soit présent dans le `PATH` d'un
    utilisateur standard. Dans ce cas, `command -v` peut ne retourner que
    `/usr/bin/lsblk`, alors que les commandes fonctionnent correctement avec
    `sudo`.

Créez le répertoire de travail et le fichier image :

```bash
mkdir -p ~/DATA01-J3
cd ~/DATA01-J3
truncate -s 512M luks-disk.img
ls -lh luks-disk.img
```

Associez le fichier au premier périphérique loop disponible et conservez le nom
retourné dans une variable :

```bash
IMAGE=$(realpath luks-disk.img)
LOOP_DEVICE=$(sudo losetup --find --show "$IMAGE")
printf 'Loop device : %s\n' "$LOOP_DEVICE"
```

Contrôlez immédiatement l'association :

```bash
sudo losetup -l "$LOOP_DEVICE"
lsblk -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS "$LOOP_DEVICE"
```

| Observation | Valeur relevée |
| --- | --- |
| Chemin absolu du fichier image | |
| Loop device obtenu | |
| Taille observée | |
| Type avant LUKS | |

!!! warning "Point de contrôle obligatoire"
    La colonne `BACK-FILE` de `losetup -l` doit correspondre au fichier
    `luks-disk.img` créé dans `DATA01-J3`. Arrêtez-vous si ce n'est pas le cas.

## Partie 4 - Initialiser le conteneur LUKS

Affichez une dernière fois la cible, puis initialisez explicitement un conteneur
LUKS2 :

```bash
printf 'Cible vérifiée : %s -> %s\n' "$LOOP_DEVICE" "$IMAGE"
sudo cryptsetup luksFormat --type luks2 "$LOOP_DEVICE"
```

Lisez l'avertissement avant de confirmer. Choisissez une phrase de passe propre
à l'exercice, ne l'écrivez ni dans la documentation ni dans l'historique du
terminal.

Vérifiez le résultat :

```bash
sudo blkid "$LOOP_DEVICE"
sudo cryptsetup isLuks "$LOOP_DEVICE"
printf 'Code retour isLuks : %s\n' "$?"
```

Examinez ensuite les métadonnées sans afficher de secret :

```bash
sudo cryptsetup luksDump "$LOOP_DEVICE"
```

| Information du header | Valeur observée |
| --- | --- |
| Version LUKS | |
| Chiffrement et mode | |
| Taille de secteur | |
| Fonction de dérivation de clé | |
| Slots de clés actifs | |
| UUID | |

Le header contient les paramètres nécessaires à l'ouverture et les slots de
clés. Il ne contient pas la phrase de passe en clair.

### Preuve observée - Création et inspection du volume

![Création du volume LUKS2, contrôle isLuks et inspection du header](<../../assets/img/securite-donnees/it-3/Capture d’écran du 2026-09-24 10-11-28.png>)

*Capture du 24 septembre 2026 sur la VM Debian 13 : `/dev/loop1` est reconnu
comme `crypto_LUKS`, `isLuks` retourne `0` et `luksDump` affiche un volume
LUKS2 utilisant `aes-xts-plain64`, Argon2id et le slot de clé 0. La phrase
secrète n'est pas affichée.*

## Partie 5 - Ouvrir le volume

Ouvrez le conteneur sous le nom `data-secure` :

```bash
sudo cryptsetup open "$LOOP_DEVICE" data-secure
```

Observez les deux niveaux de périphériques :

```bash
lsblk -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS "$LOOP_DEVICE"
ls -l /dev/mapper/data-secure
sudo cryptsetup status data-secure
```

| Élément | Rôle |
| --- | --- |
| `$LOOP_DEVICE` | Contient les blocs chiffrés et le header LUKS. |
| `/dev/mapper/data-secure` | Présente les blocs déchiffrés tant que le volume reste ouvert. |

## Partie 6 - Créer et monter le système de fichiers

Le système de fichiers doit être créé sur le périphérique mapper, jamais
directement sur le loop device :

```bash
sudo mkfs.ext4 /dev/mapper/data-secure
lsblk -f "$LOOP_DEVICE"
```

Créez le point de montage et montez le système de fichiers :

```bash
sudo mkdir -p /mnt/data-secure
sudo mount /dev/mapper/data-secure /mnt/data-secure
findmnt /mnt/data-secure
```

### Preuve observée - Ouverture, formatage et montage

![Ouverture du mapping LUKS, création du système de fichiers ext4 et montage](<../../assets/img/securite-donnees/it-3/Capture d’écran du 2026-09-24 10-15-27.png>)

*Capture du 24 septembre 2026 sur la VM Debian 13 : le mapping
`/dev/mapper/data-secure` est actif au-dessus de `/dev/loop1`, le système de
fichiers ext4 est créé sur le mapper puis monté sur `/mnt/data-secure`.*

Créez trois fichiers de test :

```bash
echo "Données confidentielles - DATA-01" | sudo tee /mnt/data-secure/secret.txt
echo "Compte rendu de test LUKS" | sudo tee /mnt/data-secure/compte-rendu.txt
date --iso-8601=seconds | sudo tee /mnt/data-secure/date-creation.txt
sudo ls -la /mnt/data-secure
```

### Preuve observée - Écriture des données

![Création et liste des trois fichiers dans le volume LUKS monté](<../../assets/img/securite-donnees/it-3/Capture d’écran du 2026-09-24 10-16-45.png>)

*Capture du 24 septembre 2026 sur la VM Debian 13 : `findmnt` confirme le
montage ext4 et les fichiers `secret.txt`, `compte-rendu.txt` et
`date-creation.txt` sont présents dans le volume ouvert.*

## Partie 7 - Reconstituer la chaîne de stockage

Complétez le tableau avec les valeurs réellement observées :

| Couche | Valeur attendue ou observée |
| --- | --- |
| Fichier image | `~/DATA01-J3/luks-disk.img` |
| Périphérique loop | `loop1` |
| Volume LUKS | Le conteneur présent sur le loop device |
| Device mapper | `/dev/mapper/data-secure` |
| Système de fichiers | `ext4` |
| Point de montage | `/mnt/data-secure` |
| Données | `secret.txt` et les deux autres fichiers créés |

Utilisez ces commandes pour justifier vos réponses :

```bash
lsblk -f "$LOOP_DEVICE"
sudo blkid "$LOOP_DEVICE" /dev/mapper/data-secure
sudo cryptsetup status data-secure
findmnt /mnt/data-secure
```

## Partie 8 - Fermer puis retrouver les données

Synchronisez les écritures, démontez le système de fichiers et fermez le
mapping :

```bash
sync
sudo umount /mnt/data-secure
sudo cryptsetup close data-secure
lsblk -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS "$LOOP_DEVICE"
```

À ce stade, `/dev/mapper/data-secure` ne doit plus exister et les fichiers ne
sont plus accessibles par `/mnt/data-secure`.

Sans recréer le système de fichiers, rouvrez et remontez le volume :

```bash
sudo cryptsetup open "$LOOP_DEVICE" data-secure
sudo mount /dev/mapper/data-secure /mnt/data-secure
sudo ls -la /mnt/data-secure
sudo cat /mnt/data-secure/secret.txt
```

| Vérification | Résultat observé |
| --- | --- |
| Le mapping réapparaît | oui |
| Le système de fichiers se monte | oui |
| Les trois fichiers sont présents | oui |
| Le contenu de `secret.txt` est lisible | oui |

### Preuve observée - Fermeture et réouverture

![Fermeture du mapping LUKS, réouverture et récupération des fichiers](<../../assets/img/securite-donnees/it-3/Capture d’écran du 2026-09-24 10-19-50.png>)

*Capture du 24 septembre 2026 sur la VM Debian 13 : après démontage et
fermeture, le volume est rouvert et remonté. Les trois fichiers réapparaissent
et le contenu de `secret.txt` est retrouvé. Cette capture ne prouve pas encore
le nettoyage final ni le détachement du loop device.*

## Partie 9 - Nettoyer proprement

Fermez toutes les couches dans l'ordre inverse de leur création :

```bash
sync
sudo umount /mnt/data-secure
sudo cryptsetup close data-secure
sudo losetup --detach "$LOOP_DEVICE"
```

Vérifiez qu'il ne reste ni montage, ni mapping, ni association loop :

```bash
findmnt /mnt/data-secure || true
test ! -e /dev/mapper/data-secure && echo "Mapping fermé"
sudo losetup -j "$IMAGE"
```

La dernière commande ne doit produire aucune ligne. Si le fichier image a été
associé plusieurs fois pendant les essais, détachez uniquement les loop devices
qui pointent vers ce fichier :

```bash
while IFS=: read -r LOOP_RESTANT _; do
  sudo losetup --detach "$LOOP_RESTANT"
done < <(sudo losetup -j "$IMAGE")

sudo losetup -j "$IMAGE"
```

Une sortie vide lors du dernier contrôle confirme que toutes les associations
loop de cette image ont disparu. N'utilisez pas `losetup --detach-all`, qui
toucherait aussi les loop devices étrangers à l'exercice.

### Preuve observée - Contrôle du nettoyage

![Contrôle du démontage, de la fermeture du mapping et des associations loop restantes](<../../assets/img/securite-donnees/it-3/Capture d’écran du 2026-09-24 10-23-59.png>)

*Capture du 24 septembre 2026 sur la VM Debian 13 : `findmnt` ne retourne plus
de montage et le message `Mapping fermé` confirme la disparition de
`/dev/mapper/data-secure`. Le contrôle final détecte toutefois trois
associations résiduelles du fichier image sur `/dev/loop0`, `/dev/loop1` et
`/dev/loop2` ; un détachement complémentaire reste donc nécessaire pour valider
le nettoyage complet.*

Conservez `luks-disk.img` pour la suite du module. Si vous devez le réutiliser
après une nouvelle connexion, recréez seulement l'association loop :

```bash
cd ~/DATA01-J3
IMAGE=$(realpath luks-disk.img)
LOOP_DEVICE=$(sudo losetup --find --show "$IMAGE")
sudo cryptsetup open "$LOOP_DEVICE" data-secure
sudo mount /dev/mapper/data-secure /mnt/data-secure
```

## Preuves à conserver

- sortie de `losetup -l` montrant le lien entre le fichier et le loop device ;
- sortie de `cryptsetup luksDump` sans phrase de passe ni secret ;
- sortie de `lsblk -f` montrant les différentes couches ;
- sortie de `cryptsetup status data-secure` ;
- sortie de `findmnt` et liste des fichiers après réouverture ;
- suite des commandes de fermeture et résultat des contrôles de nettoyage.

## Bilan

| Question | Réponse |
| --- | --- |
| Que protège principalement LUKS ? | La confidentialité des données stockées lorsque le volume est fermé. |
| Où se trouvent les données chiffrées ? | Dans le fichier image, vu par le système à travers le loop device. |
| Où les données deviennent-elles accessibles en clair ? | Via `/dev/mapper/data-secure` après ouverture réussie du conteneur. |
| Pourquoi faut-il démonter avant de fermer LUKS ? | Pour terminer les écritures et retirer proprement le système de fichiers avant de supprimer le mapping. |
| Que faut-il conserver pour retrouver les données ? | Le fichier image intact, son header LUKS et un moyen d'ouverture valide. |

## Livrable attendu

Remettez un court compte rendu contenant :

- le tableau des propriétés de sécurité ;
- les valeurs observées pour chaque couche ;
- les informations principales du header LUKS ;
- les preuves demandées ;
- les commandes nécessaires pour fermer puis rouvrir le stockage ;
- une conclusion distinguant ce que LUKS protège de ce qu'il ne protège pas.
