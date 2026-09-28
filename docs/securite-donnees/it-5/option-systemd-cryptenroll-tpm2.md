# Option 1 - Ouvrir LUKS avec systemd-cryptenroll et TPM2

## Objectif

Évaluer une ouverture automatique LUKS2 liée au TPM2 d'une machine, tout en
conservant une clé de récupération indépendante. Cette option convient surtout
aux postes et serveurs disposant d'un TPM2 ou d'un vTPM persistant.

La procédure commence sur une image LUKS de laboratoire. L'enrôlement du volume
racine ne doit être envisagé qu'après réussite des tests, sauvegarde du header
et validation du moyen de secours.

## Architecture

```text
État mesuré au démarrage        Volume LUKS2
          |                         |
          v                         v
        TPM2 ---- token TPM2 dans le header
          |                         |
          +---- libération du secret ----> ouverture automatique

Coffre-fort externe
    |-- clé de récupération unique
    `-- sauvegarde du header LUKS
```

Le TPM2 ne remplace ni le chiffrement LUKS ni la récupération. Il protège un
moyen d'ouverture supplémentaire. La clé de récupération reste nécessaire si
le TPM, la carte mère ou la politique de démarrage change.

## Cas d'usage retenus

| Catégorie | Pertinence | Condition |
| --- | --- | --- |
| Portable | Oui, de préférence avec PIN | TPM2 réel, démarrage mesuré et récupération centralisée |
| Poste fixe | Oui | Inventaire matériel et procédure de remplacement |
| Serveur physique | Oui selon le modèle de menace | Redémarrage autonome et contrôle des mises à jour |
| VM | Possible avec vTPM | État du vTPM persistant, sauvegardé et lié à la VM |
| Image cloud clonée | À éviter sans préparation spécifique | Chaque instance doit conserver une clé de volume distincte |

## Prérequis

- volume au format LUKS2 ;
- système utilisant systemd avec `systemd-cryptenroll` ;
- TPM2 visible sous `/dev/tpmrm0` ou équivalent ;
- outil `cryptsetup` ;
- sauvegarde externe du header ;
- phrase ou clé de récupération testée ;
- snapshot de la VM de laboratoire avant modification du démarrage.

Dans virt-manager, ajoutez un matériel **TPM** à la VM arrêtée. Pour une VM,
préférez un vTPM 2.0 avec un stockage persistant. Notez toute modification de
firmware BIOS/UEFI, car elle peut modifier le comportement du démarrage mesuré.

## Partie 1 - Vérifier le TPM2

Dans la VM :

```bash
ls -l /dev/tpm* 2>/dev/null
systemd-cryptenroll --tpm2-device=list
systemd-analyze has-tpm2
```

Selon la distribution, installez les outils TPM2 depuis les dépôts officiels,
puis contrôlez le TPM :

```bash
tpm2_getcap properties-fixed
tpm2_pcrread sha256:7
```

| Contrôle | Résultat |
| --- | --- |
| TPM2 détecté | À compléter |
| Périphérique TPM | À compléter |
| Banque SHA-256 disponible | À compléter |
| PCR retenus pour le test | À décider et justifier |

!!! warning "Choix des PCR"
    Un enrôlement sans PCR lie le secret au TPM, mais pas à un état mesuré
    précis. Une politique PCR trop stricte peut bloquer le volume après une mise
    à jour du noyau, du firmware ou du chargeur. Le choix doit être testé sur le
    matériel et la chaîne de démarrage réels.

## Partie 2 - Créer un volume de laboratoire

```bash
LAB_DIR="$HOME/tpm2-luks-lab"
IMAGE="$LAB_DIR/tpm2-luks.img"
RECOVERY_DIR="$HOME/tpm2-luks-recovery"

install -d -m 700 "$LAB_DIR" "$RECOVERY_DIR"
truncate -s 512M "$IMAGE"
LOOP_DEVICE=$(sudo losetup --find --show "$IMAGE")

printf 'Image : %s\nPériphérique : %s\n' "$IMAGE" "$LOOP_DEVICE"
sudo losetup -l "$LOOP_DEVICE"
sudo cryptsetup luksFormat --type luks2 "$LOOP_DEVICE"
sudo cryptsetup luksDump "$LOOP_DEVICE"
```

Ne réutilisez pas un volume contenant des données réelles. Conservez au moins
un keyslot par phrase de passe tant que le mécanisme TPM2 n'est pas validé.

## Partie 3 - Préparer la récupération

Sauvegardez le header avant l'enrôlement :

```bash
sudo cryptsetup luksHeaderBackup "$LOOP_DEVICE" \
  --header-backup-file "$RECOVERY_DIR/header-avant-tpm2.img"
sudo chown "$USER:$USER" "$RECOVERY_DIR/header-avant-tpm2.img"
chmod 600 "$RECOVERY_DIR/header-avant-tpm2.img"
sha256sum "$RECOVERY_DIR/header-avant-tpm2.img"
```

Créez ensuite une clé de récupération systemd. La commande affiche un secret :
ne le capturez pas et stockez-le immédiatement dans le coffre-fort de test.

```bash
sudo systemd-cryptenroll "$LOOP_DEVICE" --recovery-key
sudo systemd-cryptenroll "$LOOP_DEVICE"
sudo cryptsetup luksDump "$LOOP_DEVICE"
```

Testez cette clé sans ouvrir durablement le volume :

```bash
sudo cryptsetup open --test-passphrase "$LOOP_DEVICE"
printf 'Code retour récupération : %s\n' "$?"
```

Ne poursuivez que si le code retour est `0` avec le moyen de récupération.

## Partie 4 - Enrôler le TPM2

Pour un premier test fonctionnel, enrôlez le TPM détecté automatiquement :

```bash
sudo systemd-cryptenroll "$LOOP_DEVICE" --tpm2-device=auto
sudo systemd-cryptenroll "$LOOP_DEVICE"
sudo cryptsetup luksDump "$LOOP_DEVICE"
```

Pour une politique liée à des PCR, remplacez le test précédent uniquement
après avoir déterminé les PCR compatibles avec la plateforme :

```bash
sudo systemd-cryptenroll "$LOOP_DEVICE" \
  --wipe-slot=tpm2 \
  --tpm2-device=auto \
  --tpm2-pcrs=7
```

La valeur `7` est un exemple à valider, pas une recommandation universelle.

| Contrôle | Résultat |
| --- | --- |
| Token TPM2 présent | À compléter |
| Keyslot de récupération toujours présent | À compléter |
| UUID LUKS inchangé | À compléter |
| Header sauvegardé après enrôlement | À compléter |

Sauvegardez de nouveau le header après l'ajout du token :

```bash
sudo cryptsetup luksHeaderBackup "$LOOP_DEVICE" \
  --header-backup-file "$RECOVERY_DIR/header-apres-tpm2.img"
sudo chown "$USER:$USER" "$RECOVERY_DIR/header-apres-tpm2.img"
chmod 600 "$RECOVERY_DIR/header-apres-tpm2.img"
sha256sum "$RECOVERY_DIR/header-apres-tpm2.img"
```

## Partie 5 - Tester l'ouverture automatique

Fermez tout mapping de test, puis demandez à systemd d'utiliser le token TPM2 :

```bash
sudo systemd-cryptsetup attach tpm2-lab "$LOOP_DEVICE" none tpm2-device=auto
sudo cryptsetup status tpm2-lab
ls -l /dev/mapper/tpm2-lab
sudo systemd-cryptsetup detach tpm2-lab
```

Résultat attendu : création du mapping sans saisie de la phrase de passe. Si
une saisie est demandée, conservez l'erreur et vérifiez le token, le TPM et la
politique PCR au lieu de supprimer le moyen de secours.

## Partie 6 - Tester la récupération

Simulez l'indisponibilité du TPM en désactivant temporairement le vTPM de la VM
de laboratoire ou en utilisant un contexte ne satisfaisant pas la politique.
Le token TPM2 doit échouer, mais la clé de récupération doit encore ouvrir le
volume :

```bash
sudo cryptsetup open --test-passphrase "$LOOP_DEVICE"
printf 'Code retour récupération sans TPM : %s\n' "$?"
```

| Scénario | Résultat attendu |
| --- | --- |
| TPM disponible et politique satisfaite | Ouverture automatique |
| TPM absent | Refus du token TPM2, récupération manuelle possible |
| PCR modifié | Refus du token lié aux PCR, récupération manuelle possible |
| Carte mère remplacée | Ancien TPM inutilisable, nouvel enrôlement après récupération |

## Partie 7 - Retirer ou renouveler l'enrôlement

Avant tout retrait, testez encore la clé de récupération. Supprimez ensuite
uniquement les tokens TPM2 :

```bash
sudo systemd-cryptenroll "$LOOP_DEVICE" --wipe-slot=tpm2
sudo systemd-cryptenroll "$LOOP_DEVICE"
sudo cryptsetup luksDump "$LOOP_DEVICE"
```

Pour renouveler l'enrôlement, systemd permet de combiner ajout et retrait afin
de laisser le nouveau token en place. Cette opération doit d'abord être testée
sur le volume de laboratoire.

## Partie 8 - Adapter au volume racine

Cette phase n'est autorisée qu'après validation du laboratoire.

1. identifiez le volume racine par `lsblk`, `findmnt` et son UUID ;
2. sauvegardez son header hors de la VM ;
3. créez et testez une clé de récupération ;
4. enrôlez le TPM2 ;
5. ajoutez `tpm2-device=auto` à la ligne correspondante de `/etc/crypttab` ;
6. reconstruisez l'initramfs avec l'outil de la distribution, par exemple
   `dracut -f` sur openSUSE ;
7. conservez la console de la VM pour le premier redémarrage ;
8. testez ensuite un démarrage sans TPM et la récupération manuelle.

Ne supprimez jamais le keyslot de secours après un unique démarrage réussi.

## Preuves attendues

| Preuve | État |
| --- | --- |
| TPM2 ou vTPM détecté | À produire |
| Volume de laboratoire LUKS2 | À produire |
| Header sauvegardé avant et après enrôlement | À produire |
| Clé de récupération testée | À produire sans afficher le secret |
| Token TPM2 visible | À produire |
| Ouverture automatique réussie | À produire |
| Échec contrôlé sans TPM | À produire |
| Ouverture par récupération après l'échec | À produire |
| Retrait ou renouvellement du token | À produire |

## Avantages, limites et choix

| Avantages | Limites |
| --- | --- |
| Pas de service réseau nécessaire au déverrouillage | Dépendance au TPM et à la carte mère |
| Secret non stocké en clair sur le disque | Politique PCR sensible aux mises à jour |
| Intégration native à systemd et LUKS2 | vTPM à protéger et sauvegarder correctement |
| Possibilité d'ajouter un PIN et une récupération | Déploiement hétérogène si le parc matériel varie |

**Choisir cette option** si le parc dispose de TPM2 maîtrisés, si le démarrage
mesuré est testé et si la dépendance à chaque machine est acceptable.

## Nettoyage du laboratoire

```bash
test -e /dev/mapper/tpm2-lab && sudo systemd-cryptsetup detach tpm2-lab
sudo losetup -d "$LOOP_DEVICE"
rm -f "$IMAGE"
```

Conservez les preuves non secrètes. Détruisez les clés de récupération de test
et les headers lorsqu'ils ne sont plus nécessaires.

## Ressources

- [Documentation amont de systemd-cryptenroll](https://github.com/systemd/systemd/blob/main/man/systemd-cryptenroll.xml)
- [Architecture globale de gestion des clés](concevoir-gestion-cles-parc.md)
- [Glossaire de l'itération 5](../../pense-bete/glossaire/securite-donnees/it-5.md)
