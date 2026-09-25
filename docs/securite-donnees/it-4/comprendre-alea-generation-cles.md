# Comprendre l'aléa et la génération des clés

## Objectif

Comprendre pourquoi une clé cryptographique doit être imprévisible, distinguer
taille de clé et entropie réelle, reconnaître les sources manifestement
prévisibles et utiliser les mécanismes cryptographiques fournis par Linux.

Cette activité guidée réutilise les exemples LUKS, SSH, TLS, VPN et certificats.
Elle prépare la gestion des clés à l'échelle d'un parc étudiée en J5.

## Partie 1 - Débrief de la récupération

La première colonne reprend la VM openSUSE Leap 16.0 observée pendant le TP de
récupération. Les deux autres colonnes sont à compléter pendant le débrief à
partir des installations des autres groupes.

| Élément | VM 1 | VM 2 | VM 3 |
| --- | --- | --- | --- |
| Distribution | openSUSE Leap 16.0 | À compléter | À compléter |
| Démarrage | BIOS avec partition de 8 Mio | À compléter | À compléter |
| EFI chiffrée ? | Sans objet : aucune partition EFI observée | À compléter | À compléter |
| `/boot` chiffré ? | Oui, `/boot/grub2` est dans `cr_root` | À compléter | À compléter |
| `/` chiffré ? | Oui, Btrfs dans `/dev/mapper/cr_root` | À compléter | À compléter |
| `/home` séparé ? | Sous-volume Btrfs séparé, pas une partition distincte | À compléter | À compléter |
| Swap présent ? | Oui, 2 Gio | À compléter | À compléter |
| Swap chiffré ? | Oui, `/dev/vda3` vers `cr_swap` | À compléter | À compléter |
| LVM utilisé ? | Non | À compléter | À compléter |

### Les distributions ont-elles produit la même organisation ?

À déterminer pendant le débrief. Une distribution peut utiliser des partitions
classiques, LVM, des sous-volumes Btrfs ou une combinaison de ces mécanismes.
Le résultat dépend également des choix effectués dans l'installateur.

### Quelles parties sont restées accessibles sans ouvrir LUKS ?

Sur la VM openSUSE observée, seule la partition d'amorçage BIOS de 8 Mio était
hors LUKS. La racine, les sous-volumes Btrfs, `/home`, `/boot/grub2` et le swap
étaient protégés par les deux volumes LUKS.

### Quels choix dépendent de la distribution et de l'administrateur ?

La distribution fournit des valeurs par défaut et les possibilités de son
installateur. L'administrateur choisit notamment le disque ciblé, les points de
montage, le chiffrement, la séparation éventuelle de `/home`, la présence du
swap et la méthode d'ouverture au démarrage.

## Partie 2 - Comparer plusieurs usages

| Machine | Données à protéger | Contraintes |
| --- | --- | --- |
| Poste de travail | Documents, profils, caches, secrets applicatifs | Ouverture simple pour l'utilisateur, sauvegarde et récupération |
| Ordinateur portable | Données locales et identifiants exposés au vol physique | Chiffrement complet, verrouillage rapide, récupération maîtrisée |
| Serveur dans un datacenter | Données applicatives, journaux, bases et secrets | Disponibilité, exploitation distante, procédures d'urgence |
| Serveur devant redémarrer sans intervention humaine | Données du service et clés techniques | Déverrouillage automatisé sans conserver un secret en clair sur le même disque |
| VM dans un cloud | Disques virtuels, instantanés, secrets et données clients | Gestion distante des clés, automatisation, séparation entre données et clés |

### Les mêmes choix conviennent-ils à toutes ces machines ?

Non. Une phrase de passe saisie au démarrage convient à un poste ou un portable,
mais empêche le redémarrage autonome d'un serveur. Un serveur peut nécessiter un
TPM, un service de gestion de clés ou un mécanisme réseau comme Clevis/Tang.
L'automatisation doit préserver la séparation entre la donnée chiffrée et le
moyen qui permet de l'ouvrir.

## Partie 3 - Pourquoi la génération d'une clé est importante

**Situation A :** une clé est tirée parmi toutes les valeurs possibles avec une
méthode cryptographiquement sûre.

**Situation B :** une valeur de même longueur est produite par un programme qui
ne peut générer qu'un petit ensemble de résultats.

| Question | Réponse |
| --- | --- |
| La taille affichée peut-elle être identique ? | Oui. Les deux fichiers peuvent contenir 32 octets et être présentés comme des clés de 256 bits. |
| Le nombre de possibilités à tester est-il nécessairement identique ? | Non. Il dépend de l'espace réellement exploré par le générateur. |
| Qu'est-ce qui compte en plus de la longueur ? | L'imprévisibilité, l'entropie effective, la qualité de la source et l'absence de biais exploitable. |

Une sortie longue n'est donc pas nécessairement forte. Si elle est entièrement
déterminée par une heure connue à quelques minutes près, son espace de recherche
réel est très inférieur à `2^256`.

## Partie 4 - Identifier des valeurs prévisibles

| Source ou méthode | Prévisible ? | Adaptée directement à une clé ? | Pourquoi ? |
| --- | --- | --- | --- |
| Heure actuelle | Oui, dans une plage étroite | Non | Elle peut être estimée ou retrouvée dans les journaux. |
| PID d'un processus | Oui | Non | Son espace est limité et sa valeur observable ou devinable. |
| Nom de la machine | Oui | Non | Il est stable et souvent public sur le réseau. |
| Compteur incrémental | Oui | Non | Sa prochaine valeur découle de la précédente. |
| Générateur sans garantie cryptographique | Potentiellement | Non | Une suite différente peut rester déterministe et reproductible. |
| Générateur cryptographique du système | Conçu pour résister à la prédiction | Oui | Il collecte et mélange l'entropie puis fournit une interface système adaptée. |

Une valeur différente à chaque exécution n'est pas nécessairement imprévisible.
Un compteur, l'heure ou un générateur déterministe mal initialisé peuvent produire
des valeurs différentes tout en restant faciles à reproduire.

## Partie 5 - Observer les mécanismes Linux

Observez l'estimation d'entropie exposée par le noyau :

```bash
cat /proc/sys/kernel/random/entropy_avail
```

| Contrôle | Valeur observée |
| --- | --- |
| Entropie disponible | 256 |

Consultez ensuite la documentation locale :

```bash
man 4 random
```

Linux expose notamment :

- l'appel système `getrandom(2)`, utilisé par les applications modernes ;
- `/dev/urandom`, adapté aux usages courants après l'initialisation du générateur
  du noyau ;
- `/dev/random`, dont le comportement de blocage historique est décrit dans la
  page de manuel.

L'administrateur doit privilégier les API et outils du système plutôt que
fabriquer lui-même une source d'aléa.

## Partie 6 - Générer avec les outils du système

```bash
head -c 32 /dev/urandom | xxd
openssl rand -hex 32
```

Si `xxd` n'est pas installé :

```bash
head -c 32 /dev/urandom | od -An -tx1
```

Répétez les commandes et conservez une capture sans réutiliser les valeurs
comme secrets réels.

| Question | Réponse attendue |
| --- | --- |
| Combien d'octets sont demandés ? | 32 octets |
| Combien de bits cela représente-t-il ? | 256 bits (`32 × 8`) |
| Les sorties sont-elles identiques ? | Non, sauf événement extraordinairement improbable. |
| La différence des sorties prouve-t-elle à elle seule la sûreté ? | Non. Elle montre seulement que les sorties diffèrent. |

La sûreté dépend du mécanisme de génération, de son initialisation, de son état
interne et de sa résistance à la prédiction.

## Partie 7 - Expérimenter un mauvais générateur

Créez `weak_random.py` :

```python
import random
import time

seed = int(time.time())
rng = random.Random(seed)
key = rng.randbytes(32)

print("Seed:", seed)
print("Key:", key.hex())
```

Exécutez-le plusieurs fois :

```bash
python3 weak_random.py
python3 weak_random.py
python3 weak_random.py
```

Ce programme est une démonstration volontairement vulnérable. Le module
`random` ne doit pas être utilisé pour générer des secrets cryptographiques.

| Question | Réponse |
| --- | --- |
| D'où vient la seed ? | Du nombre de secondes Unix retourné par `time.time()`. |
| Que faut-il connaître pour reproduire la clé ? | La seconde approximative de génération et le programme utilisé. |
| Faut-il tester toutes les clés de 256 bits ? | Non. Il suffit de rejouer les seeds plausibles. |
| Entre 14 h 00 et 14 h 05, combien de seeds environ ? | Environ 300, soit une par seconde pendant cinq minutes. |
| Une sortie de 32 octets suffit-elle à la rendre sûre ? | Non. Sa longueur ne compense pas une seed prévisible. |

Pour une valeur secrète produite en Python, utilisez l'API dédiée :

```python
import secrets

key = secrets.token_bytes(32)
print(key.hex())
```

## Partie 8 - Retrouver l'aléa dans les services

| Mécanisme ou service | Où l'aléa intervient-il ? | Conséquence d'une mauvaise génération |
| --- | --- | --- |
| LUKS | Clé de volume, sels et paramètres de protection des keyslots | Clé devinable ou attaques facilitées contre les accès |
| SSH | Clés d'hôte, clés utilisateur, nonces et clés de session | Usurpation du serveur, sessions prévisibles ou compromission des échanges |
| TLS | Clés privées, nonces et secrets de session | Déchiffrement, usurpation ou répétition de sessions |
| VPN | Clés privées, secrets partagés, nonces et clés de session | Déchiffrement du tunnel ou usurpation d'un pair |
| Certificats et clés privées | Génération de la clé privée et numéros de série selon le mécanisme | Clé privée reproductible, collision ou usurpation |
| Jeton de réinitialisation | Création du jeton temporaire | Prise de contrôle d'un compte si le jeton est devinable |

## Partie 9 - Observer la génération de clés

Deux exemples reproductibles sans afficher une clé privée existante :

| Outil ou service | Commande ou mécanisme | Source utilisée |
| --- | --- | --- |
| SSH | `ssh-keygen -t ed25519 -f ./cle_test_ed25519` | Générateur cryptographique du système appelé par OpenSSH |
| OpenSSL | `openssl genpkey -algorithm ED25519 -out cle_test.pem` | Générateur cryptographique du système utilisé par OpenSSL |

Réalisez les essais dans un répertoire temporaire puis supprimez les clés de
test :

```bash
TEST_DIR=$(mktemp -d)
cd "$TEST_DIR"
ssh-keygen -t ed25519 -f ./cle_test_ed25519 -N ''
openssl genpkey -algorithm ED25519 -out cle_test.pem
ls -l
cd -
rm -rf "$TEST_DIR"
```

L'administrateur ne doit généralement pas inventer lui-même les octets d'une
clé. Il choisit l'algorithme et les paramètres, puis laisse l'outil utiliser le
générateur cryptographique du système.

Une phrase de passe est mémorisable et saisie par une personne. Elle protège un
moyen d'accès et doit être renforcée par une fonction de dérivation comme
PBKDF2 ou Argon2. Une clé cryptographique est une valeur binaire générée par le
système avec une forte imprévisibilité ; elle n'est normalement ni choisie ni
mémorisée par une personne.

## Partie 10 - Préparer J5

| Opération | Problème à résoudre à l'échelle d'un parc |
| --- | --- |
| Génération | Garantir une source sûre et des paramètres homogènes sans dupliquer les clés. |
| Déploiement | Transmettre ou enrôler les secrets sans les exposer. |
| Stockage | Protéger les clés au repos, séparer les rôles et journaliser les accès. |
| Ouverture des volumes | Autoriser le redémarrage attendu sans stocker une clé en clair avec les données. |
| Accès administrateur | Appliquer le moindre privilège, l'authentification forte et la traçabilité. |
| Récupération | Disposer d'un moyen testé, protégé et accessible aux seules personnes autorisées. |
| Remplacement | Faire tourner les moyens d'accès sans rechiffrer inutilement toutes les données. |
| Révocation | Retirer rapidement un accès compromis ou devenu inutile. |
| Machine retirée du parc | Révoquer ses accès, effacer les clés et traiter ses sauvegardes et supports. |

En J5, ces problèmes seront abordés avec `systemd-cryptenroll` ou Clevis/Tang.

## Synthèse

- une longueur de 256 bits ne garantit pas 256 bits d'entropie ;
- une valeur différente n'est pas forcément imprévisible ;
- heure, PID, nom d'hôte et compteurs ne sont pas des sources directes de clés ;
- les outils cryptographiques doivent s'appuyer sur le générateur du système ;
- phrase de passe et clé de volume ont des rôles différents ;
- à l'échelle d'un parc, génération, stockage, ouverture, rotation, révocation
  et récupération doivent être organisés ensemble.

- [Glossaire de l'itération 4](../../pense-bete/glossaire/securite-donnees/it-4.md)
