# TP 4.5 — Filtrage IT/OT dans la VM Debian

Cible de préparation vérifiée en SSH le 29 octobre 2026 : `oliv@192.168.122.105`, Debian 13.7, Python 3.13, nftables 1.1.3 et iproute2 6.15.0 présents. `sudo -n` nécessite un mot de passe : aucun espace ni règle n’a été appliqué par l’agent pendant la préparation. Ce dossier contient une topologie de substitution proposée, pas la topologie validée du formateur.

## Périmètre

Quatre namespaces indépendants du réseau de gestion de la VM :

| Espace | Interface / IP | Route / rôle |
| --- | --- | --- |
| `ais45-it` | `it0`, `10.77.10.2/24` | Défaut `10.77.10.1`, client IT. |
| `ais45-fw` | `fw-it` `10.77.10.1/24`, `fw-dmz` `10.77.20.1/24`, `fw-ot` `10.77.30.1/24` | Routeur et seul point `forward`, IPv4 activé dans cet espace seulement. |
| `ais45-gw` | `dmz0`, `10.77.20.2/24` | Défaut `10.77.20.1`, proxy 15021 et dashboard 18080. |
| `ais45-ot` | `ot0`, `10.77.30.2/24` | Défaut `10.77.30.1`, serveur/modèle 15020. |

Aucun lien avec l’interface de gestion `enp1s0`, `192.168.122.105`, le LAN ou Internet. Aucun changement de règles/routage/sysctl de l’hôte. IPv6 désactivé dans les quatre espaces de ce TP IPv4 ; cela ne démontre pas une politique IPv6 de production. Aucun NAT n’est requis.

Le proxy initie une nouvelle connexion vers OT. IT ne route pas à travers le processus proxy : ses connexions directes routées vers OT sont bloquées par `ais45-fw`. Les liaisons locales sont des veth. La vue web consulte le proxy, pas le serveur direct.

## Fichiers

- `lab-it-ot.sh` : préparation, relevés, application ciblée, vérifications et export ; ne modifie pas les règles hôte.
- `filtrage-it-ot.nft` : règles à appliquer uniquement dans `ais45-fw`. Ce fichier est la source ; `evidence/.../regles-it-ot.nft` est l’export après application réelle.
- `verify.py` : vérificateur réel T01/T02/T03/T04/T05/T07 et compteurs ; génère des JSON, sort en erreur si un contrôle échoue.
- `poc/` sur la VM : copie des `.py` du laboratoire déjà présent dans `~/ot-refrigeration-poc`, avec README et licence, sans son historique Git ni ses captures. Le laboratoire original n’est pas modifié.

## Exécuter dans la VM

```bash
cd ~/ais-it-ot-j4
sudo bash ./lab-it-ot.sh all
```

Le mot de passe sudo est saisi dans le terminal de l’utilisateur, pas dans le chat. `all` prépare un réseau privé initialement permissif pour relever le chemin direct, applique le filtrage dans `ais45-fw`, teste et exporte. Il refuse d’écraser des espaces existants portant ces noms. Si un lancement échoue, inspecter les journaux et ne pas relancer `all` aveuglément.

Pour travailler étape par étape à la place de `all` :

```bash
sudo bash ./lab-it-ot.sh setup
sudo bash ./lab-it-ot.sh inspect
sudo bash ./lab-it-ot.sh apply
sudo bash ./lab-it-ot.sh verify
```

`apply` contrôle d’abord le fichier avec `nft -c`, puis charge uniquement la table `inet ais45` dans `ais45-fw`. Une réapplication remplace cette table dans un seul lot ; les autres tables ne sont pas effacées. Le fichier `chargement.nft` conserve le lot exact utilisé.

## Observer après application

```bash
sudo ip netns exec ais45-fw nft -a list ruleset
sudo ip netns exec ais45-it python3 -m lab.client status --host 10.77.20.2 --port 15021
```

Pour cette deuxième commande, se placer dans `~/ais-it-ot-j4/poc` pour que le module Python soit trouvé. Les namespaces partagent le système de fichiers de la VM.

Le navigateur de l’hôte n’a aucune route vers ce réseau isolé. La vérification HTTP utilise `/api` depuis le client IT du TP ; elle ne prouve pas l’ouverture d’une vue graphique depuis le poste utilisateur. Aucun tunnel ou port de la VM n’est publié par ce script.

## Preuves

`evidence/run-<date UTC>/` conserve : état initial, adresses/routes/écoutes par namespace, code source de la règle, lot de chargement, exports nft avant/après application et après tests, JSON des résultats, journaux des services et relevés hôte avant/après en lecture seule. Les règles annotées et les résultats sont à examiner après exécution : leur présence n’est pas présumée lors de la préparation.

Les refus FC05/FC06 via proxy sont des refus applicatifs. Le refus direct est vérifié par l’échec du client, la disponibilité OT depuis GW et l’augmentation du compteur `it_direct_drop`. Le proxy n’a pas de chemin d’écriture autorisée ; la révocation persistante T09, la panne/reprise T08/T10 et le REG-02 physique ne sont pas testés automatiquement.

## Réinitialisation et arrêt

```bash
sudo bash ./lab-it-ot.sh reset-filter
```

Cette commande enlève uniquement `inet ais45` de l’espace pare-feu : le réseau privé redevient permissif comme avant application. Elle ne remet pas à zéro le modèle et ne modifie pas l’hôte. Pour remettre le filtrage : `apply`, puis `verify`.

```bash
sudo bash ./lab-it-ot.sh teardown
```

`teardown` arrête les processus des seuls espaces `ais45-*` créés pour ce dossier puis les supprime ; le modèle s’arrête et ses états en mémoire sont perdus. Les preuves sur disque restent conservées. Ne pas utiliser ces espaces pour un autre travail.
