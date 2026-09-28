# Option 2 - Ouvrir LUKS avec Clevis et Tang

## Objectif

Évaluer une ouverture automatique LUKS2 liée à la présence d'un service Tang
sur un réseau maîtrisé. Cette option cible principalement les serveurs qui
doivent redémarrer sans intervention humaine tout en restant dépendants de leur
environnement réseau autorisé.

La procédure utilise d'abord un volume de laboratoire. Elle ne doit pas être
appliquée directement au volume racine d'un serveur de production.

## Architecture

```text
                   Réseau d'administration protégé
                              |
                 +------------+------------+
                 |                         |
             Tang 1                     Tang 2
          haute disponibilité et clés d'annonce
                 |                         |
                 +------------+------------+
                              |
                        Client Clevis
                              |
                    token JWE dans LUKS2
                              |
                       volume chiffré

Coffre-fort externe : clé de récupération + sauvegarde du header
```

Tang lie le déchiffrement à la présence réseau. Le serveur Tang ne conserve pas
directement les phrases de passe LUKS des clients. Clevis ajoute une nouvelle
clé LUKS et stocke dans le header les métadonnées JWE nécessaires à sa politique.

## Cas d'usage retenus

| Catégorie | Pertinence | Justification |
| --- | --- | --- |
| Portable hors site | Faible seul | Le poste peut être privé du réseau d'entreprise au démarrage |
| Poste fixe sur site | Possible | Réseau stable, mais interaction humaine déjà acceptable |
| Serveur datacenter | Forte | Redémarrage autonome sur un réseau contrôlé |
| VM cloud | Selon connectivité | Nécessite un Tang joignable, redondé et correctement segmenté |

## Prérequis

- une VM Tang dédiée avec adresse stable ;
- une VM cliente distincte ;
- réseau disponible dès l'initramfs pour un volume racine ;
- résolution DNS ou adresse stable ;
- volume LUKS2 avec un keyslot manuel fonctionnel ;
- clé de récupération et header sauvegardé hors du client ;
- console disponible pour tous les tests de démarrage.

## Partie 1 - Préparer le serveur Tang

Installez le paquet Tang depuis les dépôts de la distribution. Le nom du socket
systemd est généralement `tangd.socket` : vérifiez-le localement avant de
l'activer.

```bash
command -v tangd
systemctl list-unit-files | grep -E 'tang.*socket'
sudo systemctl enable --now tangd.socket
sudo systemctl status tangd.socket --no-pager
sudo ss -lntp
```

Depuis le client, récupérez l'annonce publique :

```bash
TANG_URL=http://ADRESSE_TANG
curl -fsS "$TANG_URL/adv" | head
```

N'utilisez pas `-y` lors du premier enrôlement : vérifiez explicitement
l'empreinte de l'annonce Tang par un canal indépendant avant de lui faire
confiance.

| Contrôle serveur | Résultat |
| --- | --- |
| Adresse ou nom Tang | À compléter |
| Port en écoute | À compléter |
| Empreinte de l'annonce vérifiée | À compléter |
| Accès limité au réseau attendu | À compléter |

## Partie 2 - Prévoir la disponibilité

Un unique serveur Tang créerait un point de panne. Pour une architecture réelle,
prévoyez deux instances et une politique Clevis SSS de seuil `1 sur 2` :

```json
{
  "t": 1,
  "pins": {
    "tang": [
      {"url": "http://tang1.example.internal"},
      {"url": "http://tang2.example.internal"}
    ]
  }
}
```

Une seule instance disponible suffit alors à satisfaire la politique. Cette
redondance ne remplace pas la clé de récupération hors ligne.

## Partie 3 - Créer un volume client de laboratoire

Sur le client :

```bash
LAB_DIR="$HOME/clevis-luks-lab"
IMAGE="$LAB_DIR/clevis-luks.img"
RECOVERY_DIR="$HOME/clevis-luks-recovery"

install -d -m 700 "$LAB_DIR" "$RECOVERY_DIR"
truncate -s 512M "$IMAGE"
LOOP_DEVICE=$(sudo losetup --find --show "$IMAGE")

printf 'Image : %s\nPériphérique : %s\n' "$IMAGE" "$LOOP_DEVICE"
sudo losetup -l "$LOOP_DEVICE"
sudo cryptsetup luksFormat --type luks2 "$LOOP_DEVICE"
sudo cryptsetup luksDump "$LOOP_DEVICE"
```

Installez sur le client les paquets Clevis fournis par la distribution, incluant
le support LUKS et l'unlocker Dracut si le test doit aller jusqu'au démarrage.

## Partie 4 - Sauvegarder avant l'enrôlement

```bash
sudo cryptsetup luksHeaderBackup "$LOOP_DEVICE" \
  --header-backup-file "$RECOVERY_DIR/header-avant-clevis.img"
sudo chown "$USER:$USER" "$RECOVERY_DIR/header-avant-clevis.img"
chmod 600 "$RECOVERY_DIR/header-avant-clevis.img"
sha256sum "$RECOVERY_DIR/header-avant-clevis.img"

sudo cryptsetup open --test-passphrase "$LOOP_DEVICE"
printf 'Code retour moyen manuel : %s\n' "$?"
```

Le moyen manuel doit fonctionner avant tout ajout Clevis.

## Partie 5 - Lier Clevis à Tang

Pour une seule instance de laboratoire :

```bash
sudo clevis luks bind -d "$LOOP_DEVICE" tang \
  '{"url":"http://ADRESSE_TANG"}'
```

Vérifiez soigneusement l'empreinte proposée avant d'accepter l'annonce. Listez
ensuite la politique et les métadonnées LUKS :

```bash
sudo clevis luks list -d "$LOOP_DEVICE"
sudo cryptsetup luksDump "$LOOP_DEVICE"
```

Pour les deux serveurs de l'architecture cible, utilisez le pin `sss` avec la
politique `1 sur 2` après validation séparée de chaque annonce.

| Contrôle | Résultat |
| --- | --- |
| Pin Clevis visible | À compléter |
| Token ou slot utilisé | À compléter |
| Keyslot manuel conservé | À compléter |
| UUID LUKS inchangé | À compléter |

Sauvegardez le header après l'enrôlement :

```bash
sudo cryptsetup luksHeaderBackup "$LOOP_DEVICE" \
  --header-backup-file "$RECOVERY_DIR/header-apres-clevis.img"
sudo chown "$USER:$USER" "$RECOVERY_DIR/header-apres-clevis.img"
chmod 600 "$RECOVERY_DIR/header-apres-clevis.img"
sha256sum "$RECOVERY_DIR/header-apres-clevis.img"
```

## Partie 6 - Tester l'ouverture avec Tang

Fermez tout mapping existant, puis demandez l'ouverture Clevis :

```bash
sudo clevis luks unlock -d "$LOOP_DEVICE"
lsblk -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS "$LOOP_DEVICE"
sudo clevis luks list -d "$LOOP_DEVICE"
```

Identifiez le nom du mapping créé avec `lsblk`, puis fermez-le avec
`cryptsetup close NOM_MAPPING` avant le test suivant.

Résultat attendu : ouverture sans phrase de passe lorsque Tang est joignable et
que son annonce correspond à la politique enregistrée.

## Partie 7 - Tester les pannes

### Tang indisponible

Arrêtez temporairement le socket Tang dans le laboratoire ou bloquez le flux
entre le client et le serveur :

```bash
sudo systemctl stop tangd.socket
```

L'ouverture Clevis doit échouer. Le keyslot manuel doit encore fonctionner :

```bash
sudo cryptsetup open --test-passphrase "$LOOP_DEVICE"
printf 'Code retour récupération : %s\n' "$?"
```

### Une instance sur deux indisponible

Avec une politique SSS `1 sur 2`, arrêtez Tang 1 et vérifiez l'ouverture via
Tang 2, puis inversez. Arrêtez enfin les deux : seule la récupération manuelle
doit rester disponible.

| Scénario | Résultat attendu |
| --- | --- |
| Tang accessible | Ouverture automatique |
| Tang unique arrêté | Échec Clevis, récupération manuelle possible |
| Tang 1 arrêté avec SSS 1/2 | Ouverture par Tang 2 |
| Deux Tang arrêtés | Échec automatique, récupération manuelle possible |
| Réseau indisponible | Échec automatique, récupération manuelle possible |

## Partie 8 - Activer l'ouverture au démarrage

Pour un volume racine, Clevis doit être présent dans l'initramfs et le réseau
doit être disponible assez tôt. Sur un système utilisant Dracut :

```bash
sudo dracut -f
lsinitrd | grep -i clevis
```

Selon la distribution et le réseau, ajoutez la configuration nécessaire pour
l'initramfs, notamment `rd.neednet=1` lorsque requis. Conservez la console pour
le premier redémarrage et ne retirez pas le keyslot manuel.

Vérifiez successivement :

1. démarrage avec Tang disponible ;
2. démarrage avec Tang 1 indisponible dans la politique redondée ;
3. démarrage sans aucun Tang et ouverture manuelle ;
4. retour au fonctionnement normal après rétablissement du réseau.

## Partie 9 - Révoquer ou renouveler une liaison

Listez d'abord les liaisons et identifiez le slot exact :

```bash
sudo clevis luks list -d "$LOOP_DEVICE"
sudo cryptsetup luksDump "$LOOP_DEVICE"
```

Après validation du moyen manuel, retirez uniquement le slot Clevis identifié :

```bash
sudo clevis luks unbind -d "$LOOP_DEVICE" -s NUMERO_SLOT
sudo clevis luks list -d "$LOOP_DEVICE"
sudo cryptsetup luksDump "$LOOP_DEVICE"
```

Ne copiez jamais un numéro d'exemple. Pour renouveler une annonce Tang, ajoutez
et testez la nouvelle politique avant de retirer l'ancienne.

## Partie 10 - Exploitation et audit

| Élément | Mesure proposée |
| --- | --- |
| Disponibilité | Deux serveurs Tang sur domaines de panne distincts |
| Réseau | Segment d'administration, filtrage client-vers-Tang uniquement |
| Confiance initiale | Empreinte de l'annonce vérifiée hors bande |
| Inventaire | Machine, UUID LUKS, politique, URLs Tang, slot et date d'enrôlement |
| Récupération | Clé unique et header dans un coffre-fort indépendant |
| Supervision | Socket, port, HTTP, latence et échecs d'ouverture |
| Journalisation | Enrôlement, modification, révocation et récupération |

Tang ne doit pas être exposé sur Internet pour simplifier l'accès. Une VM cloud
doit joindre le service par un réseau privé ou utiliser le KMS du fournisseur.

## Preuves attendues

| Preuve | État |
| --- | --- |
| Annonce Tang récupérée et empreinte vérifiée | À produire |
| Volume LUKS2 de laboratoire | À produire |
| Header sauvegardé avant et après liaison | À produire |
| Liaison visible avec `clevis luks list` | À produire |
| Ouverture automatique avec Tang | À produire |
| Échec contrôlé sans Tang | À produire |
| Récupération manuelle réussie | À produire |
| Test de redondance 1 sur 2 | À produire si deux Tang sont déployés |
| Révocation du slot Clevis | À produire |

## Avantages, limites et choix

| Avantages | Limites |
| --- | --- |
| Redémarrage autonome sur le réseau autorisé | Dépendance au réseau et à Tang |
| Pas de secret LUKS global stocké sur Tang | Infrastructure supplémentaire à maintenir |
| Redondance possible avec une politique SSS | Réseau requis dans l'initramfs pour la racine |
| Révocation et changement de politique par volume | Confiance initiale dans l'annonce à organiser |

**Choisir cette option** pour des serveurs regroupés sur un réseau maîtrisé,
lorsque la dépendance réseau est acceptable et que Tang peut être redondé.

## Nettoyage du laboratoire

```bash
sudo clevis luks list -d "$LOOP_DEVICE"
sudo losetup -d "$LOOP_DEVICE"
rm -f "$IMAGE"
```

Redémarrez le socket Tang si vous l'avez arrêté pour le test. Détruisez ensuite
les secrets et headers de laboratoire qui ne doivent pas être conservés.

## Ressources

- [Documentation amont de Clevis](https://github.com/latchset/clevis)
- [Documentation amont de Tang](https://github.com/latchset/tang)
- [Architecture globale de gestion des clés](concevoir-gestion-cles-parc.md)
- [Glossaire de l'itération 5](../../pense-bete/glossaire/securite-donnees/it-5.md)
