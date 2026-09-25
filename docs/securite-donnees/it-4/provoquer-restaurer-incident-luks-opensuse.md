# Provoquer et restaurer un incident LUKS sur openSUSE Leap 16.0

## Objectif

Déployer une VM complète openSUSE Leap 16.0 sur un disque `qcow2`, chiffrer
son système pendant l'installation, supprimer volontairement les keyslots LUKS
hors ligne, puis restaurer le header sauvegardé et vérifier l'intégrité d'un
fichier témoin.

Cette feuille décrit une manipulation **à réaliser**. Les tableaux de résultats
doivent être complétés uniquement à partir des commandes et captures réellement
obtenues.

## Environnement retenu

| Élément | Valeur prévue ou observée |
| --- | --- |
| Hyperviseur | KVM/libvirt sur le poste hôte |
| Gestion de la VM | virt-manager ou `virt-install` |
| Système invité | openSUSE Leap 16.0 |
| ISO | `Leap-16.0-offline-installer-x86_64.install.iso` |
| Nom final de la VM | `opensuse-factory` |
| Disque virtuel | `/var/lib/libvirt/images/data01-j4.qcow2`, `qcow2`, 20 Gio |
| Chiffrement | LUKS configuré dans l'installateur Agama |
| Accès hors ligne | `qemu-nbd`, VM arrêtée |

Agama est l'installateur d'openSUSE Leap 16.0. Son interface présente notamment
les rubriques stockage et authentification avant le lancement de l'installation.

## Règles de sécurité

!!! danger "Manipulation volontairement destructive"
    `cryptsetup luksErase` supprime les keyslots du volume ciblé. Une erreur de
    périphérique peut rendre un autre volume irrécupérable. Ne remplacez jamais
    `/dev/nbd0pX` par un numéro supposé : retrouvez la partition et comparez son
    UUID avec celui enregistré dans la VM.

- la VM doit être arrêtée avant toute connexion de son image avec `qemu-nbd` ;
- le header, son empreinte, l'UUID LUKS et l'empreinte du fichier témoin doivent
  être conservés sur l'hôte avant l'incident ;
- l'image `qcow2` ne doit être attachée qu'une seule fois ;
- aucune phrase de passe ne doit apparaître dans les captures ou le dépôt Git ;
- ne poursuivez pas si un contrôle demandé est négatif ou ambigu.

## Partie 1 - Préparer l'hôte KVM

Vérifiez les outils sans rien installer inutilement :

```bash
command -v virsh qemu-img virt-install qemu-nbd
virsh --version
qemu-img --version
virt-install --version
qemu-nbd --version
virsh list --all
```

Sur un hôte Debian, les paquets généralement nécessaires sont :

```bash
sudo apt update
sudo apt install qemu-kvm qemu-utils libvirt-daemon-system \
  libvirt-clients virtinst virt-manager cryptsetup parted
```

Définissez les chemins réels sur l'hôte :

```bash
VM_NAME=data01-j4
ISO=/home/oliv/Downloads/Leap-16.0-offline-installer-x86_64.install.iso
DISK=/var/lib/libvirt/images/${VM_NAME}.qcow2
RECOVERY_DIR="$HOME/DATA01-J4-RECOVERY"

test -r "$ISO" && printf 'ISO : %s\n' "$ISO"
install -d -m 700 "$RECOVERY_DIR"
```

| Contrôle | Résultat observé |
| --- | --- |
| Les quatre outils sont présents | Oui, utilisés pendant la création et l'accès NBD |
| libvirt répond | Oui, inventaire des domaines obtenu |
| Chemin absolu de l'ISO | `/home/oliv/Downloads/Leap-16.0-offline-installer-x86_64.install.iso` |
| Chemin du disque `qcow2` | `/var/lib/libvirt/images/data01-j4.qcow2` |

## Partie 2 - Créer et installer la VM

Créez le disque :

```bash
sudo qemu-img create -f qcow2 "$DISK" 20G
sudo qemu-img info "$DISK"
```

Créez ensuite la VM avec virt-manager, ou avec :

```bash
sudo virt-install \
  --name "$VM_NAME" \
  --memory 4096 \
  --vcpus 2 \
  --disk "path=$DISK,format=qcow2" \
  --cdrom "$ISO" \
  --os-variant detect=on,require=off \
  --network network=default \
  --graphics spice
```

Dans Agama :

1. sélectionnez openSUSE Leap 16.0 ;
2. configurez l'utilisateur et l'authentification ;
3. ouvrez la rubrique **Storage** et choisissez uniquement le disque virtuel de
   20 Gio de cette VM ;
4. activez le chiffrement du système lors du partitionnement ;
5. relisez le récapitulatif avant de lancer l'installation ;
6. terminez l'installation, retirez l'ISO puis démarrez le système installé.

Les libellés exacts peuvent évoluer. Conservez une capture du récapitulatif de
stockage montrant le chiffrement avant de confirmer l'installation.

| Élément | Valeur observée |
| --- | --- |
| Nom final du domaine libvirt | `opensuse-factory` |
| RAM et vCPU | 4 096 Mio et 2 vCPU dans la commande de création |
| Taille et format du disque | `qcow2`, 20 Gio ; image non signalée comme corrompue par `qemu-img info` |
| Option de chiffrement choisie dans Agama | Chiffrement LUKS du système et du swap |
| Capture du partitionnement | Voir les preuves de la partie 3 |

### Dépannage observé au premier démarrage

Sur la VM testée, GRUB a d'abord refusé une phrase de passe contenant des
caractères dont la position diffère entre les claviers AZERTY et QWERTY. Pour
écarter cette ambiguïté dans le laboratoire, utilisez une phrase suffisamment
longue composée uniquement de lettres communes aux deux dispositions. Évitez
notamment `a`, `q`, `w`, `z`, `m`, les accents, les chiffres et les symboles.
Ne publiez pas la phrase réellement choisie.

Après le déverrouillage par GRUB, le démarrage peut rester bloqué sur des
messages concernant `cr_root`, `cr_swap`, `90-crypt.sh` ou
`dm-uuid-CRYPT-LUKS`. GRUB et l'initramfs sont deux étapes distinctes : le mot de
passe demandé par GRUB ne garantit pas que les demandes suivantes de
l'initramfs seront visibles. Plymouth peut masquer ces invites.

Pour rendre les demandes visibles et neutraliser temporairement la reprise sur
le swap :

1. affichez le menu GRUB et sélectionnez l'entrée openSUSE ;
2. appuyez sur `e` pour modifier cette entrée ;
3. repérez la ligne commençant par `linux /boot/vmlinuz` ;
4. ne modifiez ni `root=UUID=...`, ni `cryptomount`, ni les UUID ;
5. remplacez les paramètres suivants :

```text
${extra_cmdline} splash=silent resume=/dev/mapper/cr_swap mitigations=auto quiet
```

par :

```text
${extra_cmdline} plymouth.enable=0 rd.plymouth=0 noresume mitigations=auto
```

6. démarrez avec `Ctrl+X` ou `F10` ;
7. saisissez la phrase LUKS à chaque demande visible pour `cr_root` et, si elle
   est demandée, pour `cr_swap`.

Cette modification est temporaire et disparaît au redémarrage suivant.
`noresume` désactive seulement la reprise depuis le swap pour ce démarrage. Sur
la VM testée, cette procédure a permis de dépasser le blocage et de poursuivre
le démarrage. Une fois connecté, conservez les diagnostics avant toute
correction permanente :

```bash
systemctl --failed
sudo systemctl status systemd-cryptsetup@cr_swap.service --no-pager -l
lsblk -o NAME,TYPE,SIZE,FSTYPE,UUID,MOUNTPOINTS
sudo cat /etc/crypttab
swapon --show
```

### Rendre la correction GRUB permanente

Après validation du démarrage temporaire, sauvegardez la configuration puis
modifiez les paramètres par défaut :

```bash
sudo cp -a /etc/default/grub /etc/default/grub.avant-correction
sudo nano /etc/default/grub
```

Dans `GRUB_CMDLINE_LINUX_DEFAULT`, retirez `splash=silent`, `quiet` et
`resume=/dev/mapper/cr_swap`, puis conservez les autres options et ajoutez :

```text
plymouth.enable=0 rd.plymouth=0 noresume
```

La configuration appliquée sur la VM est :

```bash
GRUB_CMDLINE_LINUX_DEFAULT="plymouth.enable=0 rd.plymouth=0 noresume mitigations=auto security=selinux selinux=1"
```

Régénérez et contrôlez GRUB :

```bash
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
grep -E 'plymouth|noresume|splash|quiet|resume=' /etc/default/grub
sudo grep -E 'plymouth|noresume' /boot/grub2/grub.cfg | head
sudo reboot
```

Le fichier généré contient bien `plymouth.enable=0 rd.plymouth=0 noresume`.
Le redémarrage suivant a réussi sans nouvelle modification manuelle de GRUB.
Cette correction désactive la reprise après hibernation, mais n'interdit pas
l'utilisation normale du swap, à contrôler avec `swapon --show`.

### Activer SSH dès le premier démarrage

Une fois connecté localement avec le compte utilisateur créé dans Agama,
installez et démarrez le serveur SSH :

```bash
sudo zypper refresh
sudo zypper install openssh-server firewalld
sudo systemctl enable --now sshd
sudo systemctl enable --now firewalld
```

Ouvrez uniquement le service SSH dans le pare-feu, puis contrôlez la
configuration :

```bash
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
sudo firewall-cmd --list-services
sudo sshd -t
systemctl --no-pager --full status sshd
ss -lntp | grep ':22'
ip -br address
```

Si un doute subsiste sur la zone associée à l'interface IPv4, contrôlez-la puis
appliquez la règle SSH à cette zone précise :

```bash
ip -4 -br address
sudo firewall-cmd --get-active-zones

INTERFACE=$(ip route show default | awk '/default/{print $5; exit}')
ZONE=$(sudo firewall-cmd --get-zone-of-interface "$INTERFACE")
printf 'Interface : %s\nZone : %s\n' "$INTERFACE" "$ZONE"

sudo firewall-cmd --permanent --zone="$ZONE" --add-service=ssh
sudo firewall-cmd --reload
sudo firewall-cmd --zone="$ZONE" --list-all
sudo firewall-cmd --zone="$ZONE" --query-service=ssh
```

Le message `Warning: ALREADY_ENABLED: ssh` n'est pas une erreur : il indique
que le service était déjà autorisé dans la zone. La commande
`--query-service=ssh` doit répondre `yes`.

Repérez l'adresse IP de la VM, puis testez depuis l'hôte avec le compte non
privilégié créé pendant l'installation :

```bash
ssh oliv@ADRESSE_IP_VM
```

Pour installer immédiatement la clé publique de l'hôte :

```bash
ssh-copy-id oliv@ADRESSE_IP_VM
ssh oliv@ADRESSE_IP_VM
```

Ne réactivez pas l'accès SSH de `root` par mot de passe. Sur une nouvelle
installation de Leap 16.0, cet accès est désactivé par défaut. Utilisez le
compte utilisateur avec `sudo` et conservez une première session SSH ouverte
pendant les tests de configuration.

| Contrôle SSH | Résultat observé |
| --- | --- |
| Interface réseau | `enp1s0` |
| Adresse IPv4 de la VM | `192.168.122.128/24` |
| Zone `firewalld` active | `public` |
| Service `sshd` activé au démarrage | Oui, lien créé vers `sshd.service` |
| Port TCP 22 en écoute | À vérifier avec `ss -lntp` |
| Service `ssh` autorisé par `firewalld` | Oui, présent dans la zone `public` |
| Connexion depuis l'hôte | À compléter |
| Connexion par clé publique | À compléter |

![Activation de SSH, adresse IPv4 et service autorisé dans la zone public](<../../assets/img/securite-donnees/it4/Capture d’écran du 2026-09-25 10-47-11.png>)

## Partie 3 - Identifier le stockage dans la VM

Dans la VM openSUSE :

```bash
command -v cryptsetup lsblk findmnt blkid sha256sum
sudo zypper install cryptsetup
lsblk -o NAME,TYPE,SIZE,FSTYPE,UUID,MOUNTPOINTS
lsblk -f
findmnt
sudo blkid
```

La commande `zypper install` n'est nécessaire que si `cryptsetup` manque.
Identifiez d'abord tous les périphériques dont le type est `crypto_LUKS` :

```bash
lsblk -rpo NAME,TYPE,SIZE,FSTYPE,UUID,MOUNTPOINTS
sudo blkid | grep 'TYPE="crypto_LUKS"'
```

La VM finale présente son disque sous le nom `/dev/vda`. Il existe ici deux
partitions LUKS, une pour `cr_root` et une pour `cr_swap`. Ne choisissez pas une partition uniquement à
partir de son numéro : comparez son UUID, sa taille et son rôle dans `lsblk`.

Définissez ensuite la partition LUKS réellement destinée à l'exercice, par
exemple `/dev/vda2` lorsque les résultats précédents le confirment :

```bash
LUKS_PART=/dev/vda2
printf 'Partition à contrôler : %s\n' "$LUKS_PART"
sudo cryptsetup isLuks "$LUKS_PART"
printf 'Code retour isLuks : %s\n' "$?"
sudo cryptsetup luksUUID "$LUKS_PART"
sudo cryptsetup luksDump "$LUKS_PART"
```

Adaptez `/dev/vda2` si votre résultat diffère. Un code retour `0`
pour `isLuks` confirme le format LUKS. Le message `Device /dev/vdXY does not
exist` signifie simplement que le texte d'exemple n'a pas été remplacé par un
périphérique réel.

| Élément | Valeur observée |
| --- | --- |
| Disque système | `/dev/vda`, 20 Gio |
| Partition LUKS racine | `/dev/vda2`, 18 Gio, mapping `cr_root` |
| UUID LUKS racine | `d0538fc9-d73c-4e91-beef-8147a4aced91` |
| Partition LUKS swap | `/dev/vda3`, 2 Gio, mapping `cr_swap` |
| UUID LUKS swap | `5f0ea05a-48f8-4ec1-8275-93d153504998` |
| Version LUKS racine | LUKS2 |
| Algorithme et mode | `aes-xts-plain64`, clé XTS de 512 bits |
| Dérivation du keyslot racine | PBKDF2 avec SHA-256, keyslot `0` actif |
| Élément non chiffré | `/dev/vda1`, partition d'amorçage BIOS de 8 Mio |
| Éléments contenus dans LUKS | Racine Btrfs et sous-volumes `/home`, `/var`, `/root`, `/opt`, `/srv`, `/usr/local`, `/.snapshots` et `/boot/grub2` ; swap séparé chiffré |

Représentez l'organisation réellement obtenue :

```text
/dev/vda                         disque qcow2 de 20 Gio
|-- /dev/vda1                    amorçage BIOS, 8 Mio, non chiffré
|-- /dev/vda2                    LUKS2, 18 Gio
|   `-- /dev/mapper/cr_root      Btrfs
|       |-- /                    racine et instantané Btrfs actif
|       |-- /home, /var, /root   sous-volumes Btrfs
|       `-- /boot/grub2/...      sous-volumes situés dans cr_root
`-- /dev/vda3                    LUKS2, 2 Gio
    `-- /dev/mapper/cr_swap      swap
```

![Identification des partitions LUKS racine et swap avec lsblk](<../../assets/img/securite-donnees/it4/Capture d’écran du 2026-09-25 10-49-35.png>)

![Systèmes de fichiers et points de montage Btrfs dans cr_root](<../../assets/img/securite-donnees/it4/Capture d’écran du 2026-09-25 10-49-56.png>)

![UUID observés avec blkid](<../../assets/img/securite-donnees/it4/Capture d’écran du 2026-09-25 10-50-07.png>)

![Filtrage des deux partitions de type crypto_LUKS](<../../assets/img/securite-donnees/it4/Capture d’écran du 2026-09-25 10-51-32.png>)

![Validation du volume racine LUKS2 avec luksDump](<../../assets/img/securite-donnees/it4/Capture d’écran du 2026-09-25 10-52-42.png>)

## Partie 4 - Créer les preuves avant incident

Dans la VM :

```bash
{
  date --iso-8601=seconds
  hostname 2>/dev/null || cat /etc/hostname
  echo "DATA-01 - récupération J4"
} > "$HOME/temoin-recuperation.txt"

cat "$HOME/temoin-recuperation.txt"
sha256sum "$HOME/temoin-recuperation.txt" | tee /tmp/temoin-recuperation.sha256
```

Sauvegardez le header de la partition LUKS identifiée :

```bash
sudo cryptsetup luksHeaderBackup "$LUKS_PART" \
  --header-backup-file /tmp/root-luks-header.img
sudo chmod 600 /tmp/root-luks-header.img
sudo ls -lh /tmp/root-luks-header.img
sudo sha256sum /tmp/root-luks-header.img
```

Copiez vers le répertoire `DATA01-J4-RECOVERY` de l'hôte :

- `root-luks-header.img` ;
- `temoin-recuperation.sha256` ;
- un fichier texte indiquant le nom de la VM, le chemin du `qcow2`, la
  partition LUKS dans la VM et son UUID.

La copie peut être faite avec `scp` ou un partage temporaire adapté à votre
environnement. Sur l'hôte, protégez et vérifiez les preuves :

```bash
chmod 700 "$RECOVERY_DIR"
chmod 600 "$RECOVERY_DIR/root-luks-header.img"
ls -lh "$RECOVERY_DIR"
sha256sum "$RECOVERY_DIR/root-luks-header.img"
stat "$RECOVERY_DIR/root-luks-header.img"
```

| Preuve sortie de la VM | Valeur ou chemin sur l'hôte |
| --- | --- |
| Header LUKS | `/home/oliv/DATA01-J4-RECOVERY/root-luks-header.img`, 16 Mio |
| SHA-256 du header | `744baf17f55da681259bb081c54e475cfc20ee474cc27c03fe5cfc3a631da272` |
| UUID LUKS | `d0538fc9-d73c-4e91-beef-8147a4aced91` |
| Partition LUKS dans la VM | `/dev/vda2` (`cr_root`) |
| SHA-256 du fichier témoin | `00423b3d2a7e4f3f3a968494c5d02ecc464ef0ccb6d113e0184439385b4e6d14` |

La commande `hostname` n'était pas disponible lors de la création observée du
fichier témoin. Le fichier contient donc la date
`2026-09-25T10:52:51+02:00` et le texte `DATA-01 - récupération J4`, mais pas le
nom de la machine. Cette limite est conservée dans le compte rendu ; elle
n'empêche pas la comparaison future de l'empreinte SHA-256.

![Création du témoin, calcul de son empreinte et sauvegarde du header](<../../assets/img/securite-donnees/it4/Capture d’écran du 2026-09-25 11-29-12.png>)

![Copie du header et du témoin depuis la VM vers l'hôte](<../../assets/img/securite-donnees/it4/Capture d’écran du 2026-09-25 11-29-30.png>)

![Présence du header sur l'hôte et calcul de son empreinte](<../../assets/img/securite-donnees/it4/Capture d’écran du 2026-09-25 11-29-43.png>)

## Partie 5 - Raccorder le disque arrêté avec qemu-nbd

Arrêtez la VM depuis openSUSE, puis contrôlez son état sur l'hôte :

```bash
sudo poweroff
VM_NAME=opensuse-factory
DISK=/var/lib/libvirt/images/data01-j4.qcow2

sudo virsh domstate "$VM_NAME"
sudo test -f "$DISK"
printf 'Code retour présence qcow2 : %s\n' "$?"
sudo qemu-img info "$DISK"
```

Les variables définies dans un ancien terminal ne sont pas conservées dans un
nouveau terminal. Une variable `$DISK` vide produit l'erreur
`The 'file' block driver requires a file name` et laisse `/dev/nbd0` à `0B`.
La sortie de `domstate` doit être `shut off` ou son équivalent localisé et le
code retour de `test` doit être `0`.

Sur l'hôte, raccordez ensuite l'image :

```bash
sudo modprobe nbd max_part=16
lsblk -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS /dev/nbd0 2>/dev/null || true

: "${DISK:?La variable DISK est vide}"
sudo qemu-nbd --connect=/dev/nbd0 "$DISK"
sudo partprobe /dev/nbd0
lsblk -o NAME,TYPE,SIZE,FSTYPE,UUID,MOUNTPOINTS /dev/nbd0
sudo blkid /dev/nbd0p*
```

Identifiez la ou les partitions `crypto_LUKS`. Ne saisissez pas littéralement
`pX` et n'utilisez jamais une valeur contenant `^C`, qui représente une
interruption clavier. Définissez ensuite la partition réelle, par exemple
`/dev/nbd0p2` uniquement si les sorties précédentes le confirment :

```bash
NBD_LUKS=/dev/nbd0pX
printf 'Partition LUKS à contrôler : %s\n' "$NBD_LUKS"
sudo cryptsetup isLuks "$NBD_LUKS"
printf 'Code retour isLuks : %s\n' "$?"
sudo cryptsetup luksUUID "$NBD_LUKS"
sudo cryptsetup luksDump "$NBD_LUKS"
```

| Contrôle impératif | Valeur |
| --- | --- |
| État de la VM | Domaine `opensuse-factory` fermé ; association avec le `qcow2` à confirmer par `domblklist` |
| Image raccordée à `/dev/nbd0` | Oui, disque de 20 Gio |
| Partition LUKS depuis l'hôte | `/dev/nbd0p2`, 18 Gio |
| UUID enregistré dans la VM | `d0538fc9-d73c-4e91-beef-8147a4aced91` |
| UUID observé via NBD | `d0538fc9-d73c-4e91-beef-8147a4aced91` |
| UUID strictement identiques | Oui |
| Header externe présent et non vide | Oui, fichier de 16 Mio |
| Empreinte du témoin conservée | Oui |

!!! warning "Point d'arrêt"
    Ne lancez pas la partie suivante si toutes les réponses ne sont pas
    positives et si les UUID ne sont pas strictement identiques.

## Partie 6 - Provoquer et diagnostiquer l'incident

Sur la seule partition validée :

```bash
printf 'Cible destructive : %s\n' "$NBD_LUKS"
sudo cryptsetup luksErase "$NBD_LUKS"
sudo cryptsetup luksDump "$NBD_LUKS"
sudo cryptsetup open "$NBD_LUKS" test-recovery
```

Le header LUKS peut encore être reconnu, mais les keyslots permettant de
retrouver la clé de volume doivent avoir disparu. Si un mapping est créé,
fermez-le et ne poursuivez pas avant d'avoir expliqué le résultat.

```bash
test -e /dev/mapper/test-recovery && sudo cryptsetup close test-recovery
sudo virsh domblklist "$VM_NAME" --details
sudo qemu-nbd --disconnect /dev/nbd0
sudo virsh start "$VM_NAME"
```

Avant la déconnexion, `domblklist` doit confirmer que le domaine
`opensuse-factory` utilise bien
`/var/lib/libvirt/images/data01-j4.qcow2`. Ne démarrez jamais le domaine tant
que l'image est raccordée à `/dev/nbd0`.

Observez le démarrage sans réparer immédiatement.

| Observation | Résultat réel |
| --- | --- |
| Cible détruite | `/dev/nbd0p2`, UUID `d0538fc9-d73c-4e91-beef-8147a4aced91` |
| État des keyslots après `luksErase` | Section `Keyslots` vide ; aucun keyslot actif |
| Header et UUID encore détectables | Oui, LUKS2 et même UUID |
| Résultat de la tentative d'ouverture | Échec : `Aucun emplacement de clé utilisable est disponible.` |
| Message affiché au démarrage | `Invalid passphrase`, puis disque `cryptouuid/...` introuvable |
| Étape exacte où le démarrage s'arrête | GRUB bascule dans l'invite `grub rescue>` avant le chargement du noyau |
| Hypothèse de diagnostic | Le volume racine ne peut plus livrer sa clé de volume, car tous ses keyslots ont été supprimés. |

Diagnostic attendu à confirmer par les preuves : le système ne peut plus
ouvrir son volume LUKS, car aucun keyslot utilisable ne permet de retrouver la
clé de chiffrement du volume.

![Contrôle du volume et du keyslot avant l'incident](<../../assets/img/securite-donnees/it4/Capture d’écran du 2026-09-25 11-40-21.png>)

![Suppression des keyslots et échec de l'ouverture du volume](<../../assets/img/securite-donnees/it4/Capture d’écran du 2026-09-25 11-43-14.png>)

![Association du domaine au qcow2, déconnexion NBD et démarrage](<../../assets/img/securite-donnees/it4/Capture d’écran du 2026-09-25 11-44-09.png>)

![Échec de démarrage et passage en mode grub rescue](<../../assets/img/securite-donnees/it4/Capture d’écran du 2026-09-25 11-46-01.png>)

## Partie 7 - Restaurer le header

Arrêtez de nouveau la VM. Sur l'hôte :

```bash
VM_NAME=opensuse-factory
DISK=/var/lib/libvirt/images/data01-j4.qcow2
RECOVERY_DIR="$HOME/DATA01-J4-RECOVERY"

sudo virsh domstate "$VM_NAME"
sudo qemu-nbd --connect=/dev/nbd0 "$DISK"
sudo partprobe /dev/nbd0
lsblk -o NAME,TYPE,SIZE,FSTYPE,UUID,MOUNTPOINTS /dev/nbd0

NBD_LUKS=/dev/nbd0p2
printf 'Cible : %s\nSauvegarde : %s\n' \
  "$NBD_LUKS" "$RECOVERY_DIR/root-luks-header.img"
sudo cryptsetup isLuks "$NBD_LUKS"
sudo stat "$RECOVERY_DIR/root-luks-header.img"
```

Après une dernière vérification des deux chemins, restaurez :

```bash
sudo cryptsetup luksHeaderRestore "$NBD_LUKS" \
  --header-backup-file "$RECOVERY_DIR/root-luks-header.img"
sudo cryptsetup luksDump "$NBD_LUKS"
sudo cryptsetup luksUUID "$NBD_LUKS"
sudo qemu-nbd --disconnect /dev/nbd0
sudo virsh start "$VM_NAME"
```

| Contrôle après restauration | Résultat réel |
| --- | --- |
| Fichier de sauvegarde utilisé | `/home/oliv/DATA01-J4-RECOVERY/root-luks-header.img`, 16 Mio |
| Keyslot restauré | Keyslot `0`, LUKS2, PBKDF2/SHA-256 |
| UUID conforme à la valeur initiale | Oui : `d0538fc9-d73c-4e91-beef-8147a4aced91` |
| Demande de phrase de passe au démarrage | Oui, déverrouillage de nouveau fonctionnel |
| Démarrage complet d'openSUSE | Oui, cible multi-utilisateur et interface graphique atteintes ; connexion locale réussie |

Une première tentative de `stat` a ciblé `/root-luks-header.img`, car la
variable `RECOVERY_DIR` n'était plus définie. Après utilisation du chemin réel
dans `~/DATA01-J4-RECOVERY`, le fichier de 16 Mio a été retrouvé et utilisé
pour la restauration.

![Reconnexion du qcow2 et contrôle du fichier de sauvegarde](<../../assets/img/securite-donnees/it4/Capture d’écran du 2026-09-25 11-48-05.png>)

![Restauration du header et retour du keyslot 0](<../../assets/img/securite-donnees/it4/Capture d’écran du 2026-09-25 11-48-38.png>)

![UUID restauré, déconnexion NBD et redémarrage du domaine](<../../assets/img/securite-donnees/it4/Capture d’écran du 2026-09-25 11-49-14.png>)

![Démarrage complet et connexion locale à openSUSE Leap 16.0](<../../assets/img/securite-donnees/it4/Capture d’écran du 2026-09-25 11-52-15.png>)

## Partie 8 - Vérifier l'intégrité des données

Dans la VM restaurée :

```bash
cat "$HOME/temoin-recuperation.txt"
sha256sum "$HOME/temoin-recuperation.txt"
```

Comparez exactement cette empreinte avec celle conservée sur l'hôte.

| Validation finale | Résultat |
| --- | --- |
| Fichier témoin présent dans la copie externe | Oui |
| SHA-256 avant incident | `00423b3d2a7e4f3f3a968494c5d02ecc464ef0ccb6d113e0184439385b4e6d14` |
| SHA-256 de la copie externe après redémarrage | `00423b3d2a7e4f3f3a968494c5d02ecc464ef0ccb6d113e0184439385b4e6d14` |
| Fichier témoin présent dans la VM restaurée | Oui, contenu relu avec succès |
| SHA-256 du fichier relu dans la VM restaurée | `00423b3d2a7e4f3f3a968494c5d02ecc464ef0ccb6d113e0184439385b4e6d14` |
| Empreintes du fichier dans la VM avant/après | Oui, strictement identiques |
| Données récupérées | Oui, démarrage et intégrité du témoin confirmés |

![Nettoyage de NBD, domaine actif et empreinte de la copie externe du témoin](<../../assets/img/securite-donnees/it4/Capture d’écran du 2026-09-25 11-53-48.png>)

![Lecture et empreinte identique du témoin dans la VM restaurée](<../../assets/img/securite-donnees/it4/Capture d’écran du 2026-09-25 11-57-22.png>)

## Nettoyage technique

À la fin, vérifiez qu'aucune image n'est encore raccordée :

```bash
sudo qemu-nbd --disconnect /dev/nbd0 2>/dev/null || true
lsblk /dev/nbd0 2>/dev/null || true
sudo virsh list --all
```

Ne supprimez ni la VM ni les preuves de récupération avant validation du
livrable. Le header sauvegardé est sensible : conservez-le avec des permissions
restrictives et hors du dépôt Git.

## Livrable

Le compte rendu doit contenir :

- le choix d'openSUSE Leap 16.0 et les caractéristiques de la VM ;
- le partitionnement réellement observé, avec les zones chiffrées et non
  chiffrées ;
- la preuve de sauvegarde du header hors de la VM, sans secret ;
- l'identification du volume LUKS dans le `qcow2` arrêté ;
- les contrôles de cible et la comparaison des UUID ;
- l'état des keyslots après `luksErase` et le symptôme au démarrage ;
- le diagnostic formulé ;
- la preuve de restauration du header et du redémarrage ;
- les empreintes SHA-256 identiques du fichier témoin avant et après incident.

## Preuves à capturer

1. récapitulatif de stockage chiffré dans Agama ;
2. `lsblk -f` et `luksDump` dans la VM ;
3. header et fichiers de preuve présents sur l'hôte ;
4. identification du même UUID via `/dev/nbd0pX` ;
5. disparition des keyslots après `luksErase` ;
6. erreur de démarrage de la VM ;
7. retour des keyslots après `luksHeaderRestore` ;
8. démarrage réussi et comparaison des empreintes du témoin.

## Conclusion

Le système openSUSE était protégé par deux volumes LUKS2 : une racine Btrfs
chiffrée dans `/dev/vda2` et un swap chiffré dans `/dev/vda3`. L'incident
provoqué avec `luksErase` sur la racine a supprimé tous ses keyslots sans
effacer immédiatement les blocs de données chiffrés. GRUB ne pouvait alors
plus obtenir la clé de volume et basculait dans `grub rescue>`.

La restauration du header sauvegardé hors de la VM a rétabli le keyslot `0`,
conservé le même UUID LUKS et permis à openSUSE de démarrer complètement. La
lecture du témoin dans la VM restaurée et la comparaison de son empreinte
SHA-256 avec la valeur initiale démontrent que le fichier récupéré est
strictement identique à celui créé avant l'incident.

## Ressources

- [Documentation de l'installateur Agama](https://agama-project.github.io/docs/overview)
- [Installation interactive avec Agama](https://agama-project.github.io/docs/overview/webui)
- [Glossaire de l'itération 4](../../pense-bete/glossaire/securite-donnees/it-4.md)
