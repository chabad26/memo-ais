# Administrer les accès et préparer la récupération d'un volume LUKS


## Objectif

Le volume LUKS créé pendant l'activité précédente fonctionne. Vous allez
maintenant vous placer dans une situation d'administration réelle : les moyens
d'accès doivent pouvoir évoluer lorsqu'un administrateur quitte l'organisation
ou lorsqu'une politique de sécurité change.

Vous allez :

- examiner les keyslots LUKS ;
- ajouter et tester un nouveau moyen d'accès ;
- retirer l'ancien moyen d'accès sans perdre les données ;
- sauvegarder le header LUKS dans un emplacement distinct ;
- créer une preuve qui permettra de vérifier une récupération en itération 4.

## Règles de sécurité

- continuez à utiliser uniquement `~/DATA01-J3/luks-disk.img` ;
- vérifiez le nouveau moyen d'accès avant de supprimer l'ancien ;
- ne supprimez jamais le dernier moyen d'accès fonctionnel ;
- ne détruisez et ne restaurez pas encore le header LUKS ;
- conservez l'image et la sauvegarde du header pour l'itération 4 ;
- ne notez aucune phrase de passe dans le compte rendu, les captures ou Git.

!!! danger "Risque de perte définitive"
    Une suppression de keyslot mal préparée peut rendre le volume inutilisable.
    Avant tout retrait, vous devez avoir identifié les slots, testé le nouveau
    moyen d'accès et confirmé que les données sont encore lisibles.

## Partie 1 - Retrouver le volume de travail

Placez-vous dans le répertoire de l'activité précédente :

```bash
cd ~/DATA01-J3
IMAGE=$(realpath luks-disk.img)
test -f "$IMAGE" && printf 'Image : %s\n' "$IMAGE"
```

Recherchez une association loop existante :

```bash
sudo losetup -j "$IMAGE"
```

S'il n'existe aucune association, créez-en une :

```bash
LOOP_DEVICE=$(sudo losetup --find --show "$IMAGE")
```

S'il en existe exactement une, récupérez son nom sans en créer une autre :

```bash
LOOP_DEVICE=$(sudo losetup -j "$IMAGE" | cut -d: -f1)
```

Vérifiez la valeur et l'association avant de continuer :

```bash
printf 'Cible : %s -> %s\n' "$LOOP_DEVICE" "$IMAGE"
sudo losetup -l "$LOOP_DEVICE"
sudo blkid "$LOOP_DEVICE"
sudo cryptsetup isLuks "$LOOP_DEVICE"
printf 'Code retour isLuks : %s\n' "$?"
```

| Contrôle | Valeur observée |
| --- | --- |
| Fichier image | `luks-disk.img` |
| Loop device | `loop0` |
| Format de volume détecté par `blkid` | `crypto_LUKS` |
| Code retour de `isLuks` | 0 |

!!! warning "Associations multiples"
    Si `losetup -j` affiche plusieurs loop devices pour la même image,
    arrêtez-vous et nettoyez les associations inutiles avant de poursuivre.

## Partie 2 - Comprendre les keyslots

Examinez le header :

```bash
sudo cryptsetup luksDump "$LOOP_DEVICE"
```

| Élément | Valeur observée |
| --- | --- |
| Version LUKS | 2 |
| Slots actifs | Slot `0` uniquement |
| Fonction de dérivation | `argon2id` |
| Chiffrement du volume | `aes-xts-plain64` avec une clé XTS de 512 bits |
| UUID | `62dc82ca-89be-41b9-9f12-a376fa95ff5f` |

### Chaîne d'accès aux données

```text
Phrase de passe
      |
      v
Fonction de dérivation de clé, par exemple Argon2id
      |
      v
Keyslot contenant une copie protégée de la clé du volume
      |
      v
Clé de chiffrement du volume
      |
      v
Données chiffrées
```

La phrase de passe n'est pas utilisée directement pour chiffrer toutes les
données. Elle permet de dériver une clé qui ouvre un keyslot. Ce keyslot protège
une copie de la clé principale du volume. Plusieurs phrases de passe peuvent
donc donner accès à la même clé de volume sans rechiffrer toutes les données.

## Partie 3 - Ajouter un nouveau moyen d'accès

Ajoutez une nouvelle phrase de passe :

```bash
sudo cryptsetup luksAddKey "$LOOP_DEVICE"
```

La commande demande d'abord un moyen d'accès existant, puis la nouvelle phrase
de passe deux fois. Ne réutilisez pas l'ancienne.

Examinez les slots après l'ajout :

```bash
sudo cryptsetup luksDump "$LOOP_DEVICE"
```

| Contrôle | Résultat |
| --- | --- |
| Ancien slot toujours actif | oui |
| Nouveau slot actif | oui |
| Numéro du nouveau slot | 1 |

À ce stade, ne supprimez encore aucun slot.

## Partie 4 - Tester le nouveau moyen d'accès

Fermez proprement le volume s'il est encore monté ou ouvert :

```bash
findmnt /mnt/data-secure && sudo umount /mnt/data-secure
test -e /dev/mapper/data-secure && sudo cryptsetup close data-secure
```

Ouvrez-le avec le nouveau moyen d'accès :

```bash
sudo cryptsetup open "$LOOP_DEVICE" data-secure
sudo mkdir -p /mnt/data-secure
sudo mount /dev/mapper/data-secure /mnt/data-secure
sudo ls -la /mnt/data-secure
sudo cat /mnt/data-secure/secret.txt
```

| Vérification | Résultat |
| --- | --- |
| Le nouveau moyen d'accès ouvre le volume | oui |
| Le système de fichiers se monte | oui |
| Les fichiers de l'activité précédente sont présents | oui |
| `secret.txt` est lisible | oui |

Ne poursuivez que si ces quatre contrôles réussissent.

## Partie 5 - Retirer l'ancien moyen d'accès

Démontez et fermez de nouveau le volume :

```bash
sync
sudo umount /mnt/data-secure
sudo cryptsetup close data-secure
```

La méthode la plus lisible pour l'exercice consiste à retirer la phrase de
passe devenue obsolète :

```bash
sudo cryptsetup luksRemoveKey "$LOOP_DEVICE"
```

Saisissez uniquement l'ancienne phrase de passe lorsqu'elle est demandée.
`cryptsetup` supprime le keyslot correspondant.

Vous pouvez aussi supprimer explicitement un slot après validation avec le
formateur :

```bash
sudo cryptsetup luksKillSlot "$LOOP_DEVICE" NUMERO_DU_SLOT
```

!!! danger "Choix du slot"
    N'exécutez `luksKillSlot` qu'après avoir identifié sans ambiguïté le slot de
    l'ancien moyen d'accès. Ne copiez pas aveuglément un numéro d'exemple.

Vérifiez l'état du header :

```bash
sudo cryptsetup luksDump "$LOOP_DEVICE"
```

| Contrôle | Résultat |
| --- | --- |
| Ancien slot supprimé | oui |
| Nouveau slot toujours actif | oui |
| Au moins un moyen d'accès fonctionnel demeure | oui |

## Partie 6 - Vérifier la rotation des accès

Testez l'ancienne phrase de passe sans créer de mapping :

```bash
sudo cryptsetup open --test-passphrase "$LOOP_DEVICE"
printf 'Code retour ancien moyen : %s\n' "$?"
```

Le test doit échouer avec l'ancienne phrase de passe. Rejouez ensuite la même
commande avec la nouvelle phrase de passe : le code retour attendu est `0`.

Ouvrez enfin le volume avec le nouveau moyen d'accès et contrôlez les données :

```bash
sudo cryptsetup open "$LOOP_DEVICE" data-secure
sudo mount /dev/mapper/data-secure /mnt/data-secure
sudo ls -la /mnt/data-secure
sudo cat /mnt/data-secure/secret.txt
```

| Vérification finale | Résultat |
| --- | --- |
| Ancien moyen refusé | oui |
| Nouveau moyen accepté | oui |
| Données toujours présentes | oui |

## Partie 7 - Préparer la récupération

Le header contient les métadonnées nécessaires à l'interprétation du volume et
les keyslots. Sa perte peut rendre les données irrécupérables même si les blocs
chiffrés sont encore présents.

Créez un emplacement de récupération distinct du fichier image :

```bash
RECOVERY_DIR="$HOME/DATA01-recovery"
install -d -m 700 "$RECOVERY_DIR"
```

Sauvegardez le header après la rotation des accès :

```bash
sudo cryptsetup luksHeaderBackup "$LOOP_DEVICE" \
  --header-backup-file "$RECOVERY_DIR/luks-header.img"
sudo chmod 600 "$RECOVERY_DIR/luks-header.img"
sudo ls -lh "$RECOVERY_DIR/luks-header.img"
```

Calculez également l'empreinte de la sauvegarde :

```bash
sudo sha256sum "$RECOVERY_DIR/luks-header.img" \
  | sudo tee "$RECOVERY_DIR/luks-header.img.sha256"
```

!!! warning "Protection de la sauvegarde"
    Une sauvegarde du header ne contient pas les données du volume, mais elle
    contient les keyslots et permet des tentatives hors ligne contre les moyens
    d'accès présents au moment de la sauvegarde. Elle doit être protégée et,
    hors laboratoire, conservée sur un support distinct et chiffré.

| Élément de récupération | Valeur observée |
| --- | --- |
| Chemin du header sauvegardé | /home/oliv/DATA01-recovery/luks-header.img |
| Taille du fichier | 16M |
| Droits |`R+W` root |
| Empreinte SHA-256 | cf67b467b9837d803ee4d48b558f62714a31f34de9d3e2215e888d127ff3fb42 |

## Partie 8 - Créer un fichier témoin

Le volume doit être ouvert et monté. Créez un fichier qui permettra de vérifier
que les données récupérées en itération 4 sont bien celles présentes avant
l'incident :

```bash
sudo sh -c 'date --iso-8601=seconds > /mnt/data-secure/temoin.txt'
sudo sh -c 'hostname >> /mnt/data-secure/temoin.txt'
sudo cat /mnt/data-secure/temoin.txt
```

Calculez son empreinte et conservez-la en dehors du volume :

```bash
sudo sha256sum /mnt/data-secure/temoin.txt \
  | sudo tee "$RECOVERY_DIR/temoin.sha256"
sudo cat "$RECOVERY_DIR/temoin.sha256"
```

| Preuve | Valeur |
| --- | --- |
| Contenu attendu du fichier témoin | Date et nom de la VM |
| Empreinte SHA-256 | 7dfb625668a8b5e2db230bfdc817d0319fb0ee5616e2dd6c7e8a5a268507c4bd |
| Fichier contenant l'empreinte | `~/DATA01-recovery/temoin.sha256` |

L'empreinte ne permet pas de reconstruire le fichier. Elle permettra seulement
de vérifier que le fichier récupéré n'a pas changé.

## Partie 9 - Préparer la procédure de récupération

Consultez l'aide sans exécuter de restauration :

```bash
cryptsetup --help | less
man cryptsetup
```

La commande à identifier pour l'itération 4 est :

```bash
# Ne pas exécuter pendant cette activité.
sudo cryptsetup luksHeaderRestore "$LOOP_DEVICE" \
  --header-backup-file "$RECOVERY_DIR/luks-header.img"
```

### Procédure préparée pour l'itération 4

1. Identifier le fichier image et vérifier son association avec le loop device.
2. Retrouver `~/DATA01-recovery/luks-header.img` et contrôler son empreinte.
3. Disposer de la nouvelle phrase de passe et de l'empreinte du fichier témoin.
4. Restaurer le header avec `luksHeaderRestore` après validation de la cible.
5. Ouvrir le volume avec `cryptsetup open`.
6. Monter `/dev/mapper/data-secure` sur `/mnt/data-secure`.
7. Recalculer l'empreinte de `temoin.txt` et la comparer à la valeur conservée.

Cette procédure est préparée, mais elle n'est pas encore testée. Sa validation
aura lieu pendant l'itération 4.

## Partie 10 - Fermer proprement et vérifier les éléments disponibles

```bash
sync
sudo umount /mnt/data-secure
sudo cryptsetup close data-secure
sudo losetup --detach "$LOOP_DEVICE"
```

Contrôlez l'état final :

```bash
findmnt /mnt/data-secure || true
test ! -e /dev/mapper/data-secure && echo "Mapping fermé"
sudo losetup -j "$IMAGE"
sudo ls -l "$RECOVERY_DIR"
```

La commande `losetup -j` ne doit rien afficher. Conservez sans les modifier :

- `~/DATA01-J3/luks-disk.img` ;
- `~/DATA01-recovery/luks-header.img` ;
- `~/DATA01-recovery/luks-header.img.sha256` ;
- `~/DATA01-recovery/temoin.sha256` ;
- la nouvelle phrase de passe, hors du compte rendu.

## Passage à l'échelle

| Parc | Limite d'une gestion manuelle |
| --- | --- |
| 10 machines | Les ajouts, tests et retraits peuvent déjà être oubliés ou appliqués différemment. |
| 100 machines | Le suivi des responsables, versions de clés et preuves devient difficile sans inventaire et automatisation. |
| 1 000 machines | Une gestion centralisée, des rôles, une rotation automatisée, une traçabilité et des procédures de récupération deviennent indispensables. |

La conception d'une gestion des clés à l'échelle d'un parc sera étudiée pendant
l'itération 5.

## Preuves à conserver

- `luksDump` avant et après l'ajout du nouveau moyen d'accès ;
- ouverture réussie avec le nouveau moyen avant toute suppression ;
- `luksDump` après suppression de l'ancien moyen ;
- refus de l'ancien moyen et succès du nouveau, sans capturer les secrets ;
- présence des données après la rotation ;
- existence, droits et empreinte de la sauvegarde du header ;
- contenu et empreinte du fichier témoin ;
- contrôles de fermeture et de détachement du loop device.

## Livrable attendu

Remettez un compte rendu contenant :

- le schéma expliquant phrase de passe, keyslot et clé du volume ;
- les keyslots observés avant et après la rotation ;
- les résultats des tests de l'ancien et du nouveau moyen d'accès ;
- les éléments de récupération préparés, sans aucun secret ;
- la procédure en sept étapes prévue pour l'itération 4 ;
- une courte explication des limites d'une gestion manuelle à grande échelle.
