# Vérifier la configuration du système

**Durée indicative : 1 h 15**

## Objectif

Vérifier manuellement les éléments de configuration qui permettent de confirmer,
nuancer ou écarter les constats de Lynis sur la VM Ubuntu 20.04.

La vérification respecte la consigne de la formatrice : **aucun audit Lynis
n’est exécuté dans le conteneur**. Les informations File Browser proviennent des
commandes Docker lancées sur la VM et des observations internes limitées déjà
réalisées.

**Statut au 1er octobre 2026 : activité partiellement réalisée.** Les versions
de plusieurs paquets, l'état des services, la configuration SSH, le compte
`gvm-audit`, les comptes et groupes privilégiés et CUPS ont été contrôlés.
Les permissions de `/srv/filebrowser` et son montage Docker sont désormais
relevés. L’absence d’auditd et l’activité de journald/rsyslog sont confirmées.
Les règles sudo du compte principal, la rétention des journaux, l’origine
et la persistance des valeurs sysctl restent à vérifier.
L’inventaire Docker est cohérent, mais File Browser est désormais observé
arrêté avec le code 1. L’arrêt volontaire de la VM explique cet état ; la reprise attendue et l’identité du processus lors
d’une exécution restent à vérifier.

## Règle de travail

Toutes les commandes de cette feuille servent à lire l'état du système. Ne pas
installer ou supprimer de paquet, modifier un fichier, changer des permissions,
arrêter un service, recharger SSH ou appliquer une valeur sysctl.

Pour chaque contrôle, conserver quatre éléments :

| Élément | Contenu attendu |
| --- | --- |
| Origine | Identifiant Lynis ou question issue des audits précédents |
| Vérification | Commande exécutée ou fichier lu |
| État observé | Valeur exacte, datée et rattachée à la VM |
| Conclusion | Confirmé, infirmé, atténué ou encore à vérifier |

Ne pas publier de mot de passe, de clé privée, de contenu brut
d'`authorized_keys`, de jeton ou de donnée déposée dans File Browser.

## État commun de la vérification

Dans la **VM cible** :

```bash
date -Is
hostname
cat /etc/os-release
uname -r
```

L'état déjà observé correspond à
`oliv-Standard-PC-Q35-ICH9-2009`, Ubuntu 20.04.6 LTS, noyau
`5.15.0-139-generic`. Ces informations sont confirmées par les sorties
transmises du **1er octobre 2026 à 10:27:23 +02:00**.

## 1. Comptes utilisateurs et privilèges

### Vérifications à effectuer

```bash
getent passwd
getent group sudo
getent group adm
getent group docker

awk -F: '($3 == 0) {print $1, $3, $7}' /etc/passwd
awk -F: '($3 >= 1000 && $3 < 65534) {print $1, $3, $7}' /etc/passwd

id gvm-audit
sudo -l -U gvm-audit
```

La liste complète de `passwd` peut contenir des comptes internes : conserver
une synthèse des comptes interactifs, des UID 0 et des groupes privilégiés.

### Résultat déjà observé

| Origine | Vérification | État observé | Conclusion |
| --- | --- | --- | --- |
| Compte utilisé par Greenbone | `getent passwd gvm-audit`, `id gvm-audit`, `sudo -l -U gvm-audit` | UID/GID 1001, shell `/bin/bash`, aucun groupe supplémentaire et aucun droit sudo | Le compte d'audit n'est pas administrateur ; le périmètre réel du scan authentifié dépend donc des fichiers lisibles par ce compte |
| Comptes UID 0 | Filtre de `/etc/passwd` | Seul `root`, shell `/bin/bash` | **Confirmé** pour les comptes locaux recensés |
| Comptes locaux UID 1000 à 65533 | Filtre de `/etc/passwd` | `oliv` (1000) et `gvm-audit` (1001), tous deux avec `/bin/bash` | Deux comptes dans cette plage ; leur shell ne prouve pas une connexion active |
| Groupes privilégiés | `getent group sudo`, `adm`, `docker` | `sudo` : `oliv` ; `adm` : `syslog,oliv` ; `docker` : liste de membres vide | Appartenances déclarées **confirmées** ; règles sudo de `oliv` et accès effectif au socket Docker à compléter |

Ces sorties reconfirment aussi l’absence de droits sudo et de groupe
supplémentaire pour `gvm-audit`. Une liste vide dans `getent group docker`
ne suffit pas à exclure tout accès au démon : vérifier aussi les groupes
effectifs, les permissions du socket et les éventuelles ACL. Pour préciser
les droits administratifs du compte principal, relever `id oliv` et
`sudo -l -U oliv`.

L'appartenance au groupe `docker` doit être traitée comme un privilège fort, car
elle permet généralement de contrôler le démon Docker et d'agir sur l'hôte.

## 2. Authentification et configuration SSH

Le test `SSH-7408` recommande plusieurs valeurs plus strictes. Vérifier la
configuration réellement appliquée, puis rechercher les directives explicites :

```bash
sudo sshd -t
sudo sshd -T | grep -E \
  '^(permitrootlogin|passwordauthentication|pubkeyauthentication|maxauthtries|maxsessions|allowtcpforwarding|allowagentforwarding|x11forwarding|compression|loglevel|clientalivecountmax|clientaliveinterval|permittunnel|gssapiauthentication|macs) '

sudo grep -RInE \
  '^[[:space:]]*(Include|Match|PermitRootLogin|PasswordAuthentication|PubkeyAuthentication|MaxAuthTries|MaxSessions|AllowTcpForwarding|AllowAgentForwarding|X11Forwarding|Compression|LogLevel|ClientAliveCountMax|ClientAliveInterval|PermitTunnel|GSSAPIAuthentication|MACs)[[:space:]]' \
  /etc/ssh/sshd_config /etc/ssh/sshd_config.d 2>/dev/null
```

Un bloc `Match` peut produire une valeur différente selon le compte ou l'adresse.
La documentation locale de la version installée est accessible avec :

```bash
man sshd_config
```

### Résultats observés

Les sorties transmises le **1er octobre 2026** montrent que `sudo sshd -t`
ne produit aucun diagnostic. La configuration effective affichée par
`sshd -T` confirme les valeurs ci-dessous ; ce contrôle ne constitue pas un
test de connexion ni une preuve de la configuration chargée par le démon actif.

La recherche des directives actives ne retourne que
`Include /etc/ssh/sshd_config.d/*.conf` (ligne 13) et
`X11Forwarding yes` (ligne 91) dans `/etc/ssh/sshd_config`.
Aucun bloc `Match` n'apparaît dans les résultats fournis. Les erreurs étant
masquées par `2>/dev/null`, cette recherche ne prouve pas à elle seule que tous
les fichiers inclus ont été lus. Les valeurs effectives peuvent provenir des
valeurs par défaut, même si aucune directive explicite n'est affichée.

| Origine | État observé | Conclusion |
| --- | --- | --- |
| `SSH-7408` — accès root | `PermitRootLogin without-password` | Le mot de passe root est refusé, mais une connexion directe par clé reste possible si une clé root existe |
| `SSH-7408` — essais | `MaxAuthTries 6` | Valeur plus permissive que la recommandation Lynis ; pertinence forte pour un service d'administration exposé |
| `SSH-7408` — transfert | `AllowTcpForwarding yes`, `DisableForwarding no`, `PermitTunnel no` | Le tunnel réseau est interdit, mais le transfert TCP peut servir de rebond après compromission d'un compte |
| Authentification | `PasswordAuthentication yes`, `PubkeyAuthentication yes`, `AuthenticationMethods any` | Le mot de passe reste accepté ; vérifier les usages administratifs avant de proposer sa désactivation |
| GSSAPI | `GSSAPIAuthentication no` | Fonction non utilisée et surface associée réduite |
| Greenbone G05 | `umac-64-etm@openssh.com` et `umac-64@openssh.com` acceptés | Le constat sur les MAC 64 bits est confirmé |
| `SSH-7408` — X11 et agent | `X11Forwarding yes`, `AllowAgentForwarding yes` | Fonctions autorisées ; leur utilité et les restrictions par clé restent à examiner |
| `SSH-7408` — sessions et compression | `MaxSessions 10`, `Compression yes` | Valeurs effectives confirmées ; besoin à confronter aux usages |
| `SSH-7408` — journalisation | `LogLevel INFO` | Niveau effectif confirmé ; vérifier les événements réellement collectés |
| `SSH-7408` — maintien de session | `ClientAliveInterval 0`, `ClientAliveCountMax 3` | Les sondes périodiques ClientAlive sont désactivées ; ces valeurs ne prouvent pas une déconnexion automatique des sessions inactives |

## 3. Permissions du compte d'audit et des fichiers SSH

```bash
sudo stat -c '%U:%G %a %n' \
  /home/gvm-audit /home/gvm-audit/.ssh \
  /home/gvm-audit/.ssh/authorized_keys
sudo namei -l /home/gvm-audit/.ssh/authorized_keys
sudo -u gvm-audit ssh-keygen -lf \
  /home/gvm-audit/.ssh/authorized_keys
```

| Origine | État observé | Conclusion |
| --- | --- | --- |
| Authentification du scan Greenbone | Répertoire personnel `755`, `.ssh` en `700`, `authorized_keys` en `600`, propriétaire `gvm-audit` | Les deux éléments sensibles respectent des permissions restrictives ; le répertoire personnel reste traversable par les autres utilisateurs |
| Clé d'audit | Clé RSA 3072 bits présente | La clé publique est inventoriée ; son empreinte et son contenu ne sont pas publiés |

Les sorties transmises le **1er octobre 2026** reconfirment ces modes et une
clé RSA de 3072 bits. `namei -l` montre aussi `/` et `/home` appartenant à
`root:root` en `755` : aucun composant du chemin affiché n’est modifiable
par les autres utilisateurs selon ces modes. L’empreinte reste hors du mémo.

Il reste à vérifier si la clé possède des restrictions dans `authorized_keys`
(`from=`, `restrict`, interdiction de transfert) sans recopier la clé dans la
documentation.

## 4. Permissions de `/srv/filebrowser`

Le répertoire contient les documents servis et est monté dans `/srv` du
conteneur. Greenbone distant et le résumé Lynis ne suffisent pas à déterminer
qui peut lire ou modifier ces fichiers.

```bash
sudo stat -c '%U:%G %a %n' \
  /srv /srv/filebrowser \
  /srv/filebrowser/public \
  /srv/filebrowser/partenaires \
  /srv/filebrowser/partenaires/partenaire-alpha \
  /srv/filebrowser/partenaires/partenaire-beta \
  /srv/filebrowser/interne

sudo namei -l /srv/filebrowser/interne
sudo find /srv/filebrowser -xdev -maxdepth 3 \
  -printf '%M %u:%g %p\n' | sort

if command -v getfacl >/dev/null 2>&1; then
  sudo getfacl -p /srv/filebrowser /srv/filebrowser/*
else
  echo "getfacl absent : aucune installation pendant la vérification"
fi

sudo docker inspect filebrowser \
  --format 'User={{.Config.User}} Privileged={{.HostConfig.Privileged}} ReadonlyRootfs={{.HostConfig.ReadonlyRootfs}}'
sudo docker inspect filebrowser \
  --format '{{range .Mounts}}{{println .Source "->" .Destination "RW=" .RW}}{{end}}'
```

### Résultats transmis le 1er octobre 2026

| Vérification | État observé | Conclusion |
| --- | --- | --- |
| `stat` et `namei` | `/srv` et les sept répertoires relevés sous ce chemin sont `root:root`, mode `755` | Les autres utilisateurs locaux peuvent lister et traverser ces répertoires selon les modes ; ils ne peuvent pas y créer ou supprimer des entrées |
| Inventaire `find` | Seuls les répertoires sont affichés, aucun fichier jusqu’à la profondeur 3 sur le même système de fichiers | Aucun droit de lecture sur des documents existants n’est démontré ; le contrôle ne couvre pas d’éventuels fichiers plus profonds ou sur un autre montage |
| ACL | ACL de base seulement sur `/srv/filebrowser`, `interne`, `partenaires`, `public` ; aucune ACL étendue ni par défaut affichée | Absence d’ACL supplémentaires confirmée pour ces quatre chemins ; les deux sous-répertoires partenaires ne sont pas couverts par cette sortie `getfacl` |
| Configuration du conteneur | `User=` vide, `Privileged=false`, `ReadonlyRootfs=false` | Aucun utilisateur explicitement défini dans `Config.User`, mode privilégié désactivé et racine non configurée en lecture seule ; l’identité effective du processus reste à relever, car un script de démarrage peut changer d’utilisateur |
| Montage | `/srv/filebrowser -> /srv`, `RW=true` | Montage autorisé en lecture-écriture ; l’écriture effective dépend aussi de l’identité du processus et des permissions du système de fichiers |

Les noms `interne` et `partenaires` n’imposent aucune séparation d’accès au
niveau des modes Unix observés. Les droits applicatifs File Browser restent
à tester avec les comptes concernés. Ces sorties ne prouvent ni une fuite de
documents ni un accès distant non autorisé.

Pour relever l’identité des processus sans afficher leurs arguments :

```bash
sudo docker top filebrowser -eo pid,user,group,comm
sudo getfacl -p /srv/filebrowser/partenaires/partenaire-alpha \
  /srv/filebrowser/partenaires/partenaire-beta
```

## 5. Mises à jour et disponibilité des correctifs

```bash
dpkg-query -W \
  -f='${binary:Package}\t${Version}\t${db:Status-Abbrev}\n' \
  docker.io containerd openssh-server cups cups-daemon
apt-cache policy docker.io containerd openssh-server cups cups-daemon

if command -v pro >/dev/null 2>&1; then
  sudo pro status
else
  echo "Commande pro absente"
fi
```

Ne pas lancer `apt update` ou `apt upgrade` pendant cette activité : la première
commande modifierait les listes APT et la seconde modifierait le système.

| Composant | Version installée et candidate observée | Conclusion |
| --- | --- | --- |
| containerd | `1.7.24-0ubuntu1~20.04.2` | La révision ESM attendue n'est pas installée ; VM non rattachée à Ubuntu Pro |
| Docker | `26.1.3-0ubuntu1~20.04.1` | Même conclusion ; usage de BuildKit encore à établir |
| OpenSSH | `1:8.2p1-4ubuntu0.13` | Correctif ESM attendu absent du paquet observé |
| CUPS et cups-daemon | `2.3.1-9ubuntu1.9` | Correctif ESM attendu absent ; service actif mais limité à la boucle locale |

Les sorties transmises le **1er octobre 2026** confirment le statut `ii`
(installé) des cinq paquets et l’égalité entre version installée et candidate
pour chacun dans les listes APT locales. Les sources affichées sont
`focal`, `focal-updates` et `focal-security` ; aucune source ESM n’apparaît
dans ces sorties pour les paquets contrôlés.

`sudo pro status` indique explicitement que la machine **n’est pas rattachée
à un abonnement Ubuntu Pro**. `esm-apps` et `esm-infra` portent la valeur
`AVAILABLE yes` : cette colonne décrit leur disponibilité, pas leur activation
sur la VM. Le résultat ne montre donc pas une couverture ESM active.

L’absence de candidat plus récent dans ces listes ne prouve pas l’absence de
correctif : la fraîcheur des listes APT n’est pas établie et l’état observé ne
comprend pas de couverture ESM active. La présence ou l’absence d’un correctif
précis doit être rapprochée de l’avis de sécurité et de sa révision corrigée,
comme dans les constats Greenbone précédents. Aucun rattachement Pro ni aucune
mise à jour n’a été réalisé dans ce contrôle.

## 6. Journalisation et auditd

Lynis détecte journald et rsyslog, mais signale auditd absent avec `ACCT-9628`.
Les commandes suivantes ont été exécutées dans la VM :

```bash
systemctl is-active systemd-journald rsyslog auditd
systemctl is-enabled rsyslog auditd
systemctl status systemd-journald rsyslog auditd --no-pager
dpkg-query -W -f='${binary:Package}\t${Version}\t${db:Status-Abbrev}\n' \
  rsyslog auditd audispd-plugins 2>&1

sudo journalctl --disk-usage
sudo grep -RInE \
  '^[[:space:]]*(Storage|SystemMaxUse|RuntimeMaxUse|MaxRetentionSec)=' \
  /etc/systemd/journald.conf /etc/systemd/journald.conf.d 2>/dev/null
```

| Origine | État observé | Conclusion |
| --- | --- | --- |
| Journalisation générale | journald et rsyslog actifs depuis le 1er octobre 2026 vers 09:37 +02:00 ; rsyslog activé au démarrage, paquet `8.2001.0-1ubuntu1.3` installé (`ii`) | Activité **confirmée** ; journald est une unité `static`, ce qui n’indique pas un défaut de démarrage |
| `ACCT-9628` | Unité `auditd.service` introuvable ; aucun paquet correspondant à `auditd` ni `audispd-plugins` dans `dpkg-query` | Absence du service et des paquets **confirmée** ; une installation et des règles adaptées restent à préparer si ce besoin est retenu |
| Stockage des journaux | Journal système observé dans `/var/log/journal`, 48,0 Mo ; `journalctl --disk-usage` indique aussi 48,0 Mo | Stockage sur disque **observé** ; durée de conservation et disponibilité après redémarrage non testées |
| Paramètres de rétention | Aucune ligne active correspondant aux quatre paramètres recherchés dans la sortie `grep` | Aucune surcharge explicite affichée dans ce périmètre ; valeurs effectives et historique conservé à compléter |

Les sorties ont été transmises le **1er octobre 2026**. La seule réponse
`inactive` de `is-active` ne suffisait pas à distinguer un service arrêté d’un
service absent ; les résultats `status`, `is-enabled` et `dpkg-query`
confirment ici l’absence. Le socket `systemd-journald-audit.socket` affiché
par systemd ne prouve pas la présence du démon auditd ni de règles d’audit.

La recherche `grep` masque les erreurs avec `2>/dev/null` : son silence
ne garantit pas que chaque chemin a pu être lu. Le statut mentionne aussi
une rotation des journaux, donc son extrait peut être incomplet.

Vérifier encore la rétention : un service actif et un volume de 48,0 Mo ne
prouvent pas une durée suffisante pour reconstruire un incident. Sans modifier
la configuration, relever :

```bash
sudo journalctl --list-boots --no-pager
sudo ls -ld /var/log/journal
sudo sed -n '1,200p' /etc/systemd/journald.conf
sudo find /etc/systemd/journald.conf.d /run/systemd/journald.conf.d \
  /usr/lib/systemd/journald.conf.d -maxdepth 1 -type f -name '*.conf' -print
```

Des répertoires de fragments peuvent être absents ; conserver ce diagnostic.
Ne pas publier le contenu des événements ni les identifiants des démarrages.

## 7. Paramètres du noyau

`KRNL-6000` signale plusieurs écarts avec le profil Lynis. Relever les valeurs
réelles en une seule commande :

```bash
sysctl \
  fs.suid_dumpable \
  kernel.core_uses_pid \
  kernel.dmesg_restrict \
  kernel.kptr_restrict \
  kernel.sysrq \
  net.ipv4.ip_forward \
  net.ipv4.conf.all.forwarding \
  net.ipv4.conf.all.log_martians \
  net.ipv4.conf.all.rp_filter \
  net.ipv4.conf.all.send_redirects \
  net.ipv4.conf.default.accept_redirects \
  net.ipv4.conf.default.accept_source_route \
  net.ipv4.conf.default.log_martians \
  net.ipv6.conf.all.accept_redirects \
  net.ipv6.conf.default.accept_redirects

sudo grep -RInE \
  '^[[:space:]]*(fs\.suid_dumpable|kernel\.(core_uses_pid|dmesg_restrict|kptr_restrict|sysrq)|net\.ipv[46]\.)' \
  /etc/sysctl.conf /etc/sysctl.d 2>/dev/null
```

### Résultats transmis le 1er octobre 2026

| Paramètre | Valeur effective | Lecture du contrôle |
| --- | --- | --- |
| `fs.suid_dumpable` | `2` | Mode `suidsafe` ; examiner `kernel.core_pattern` et le traitement des dumps avant de conclure sur leur confidentialité |
| `kernel.core_uses_pid` | `0` | Valeur confirmée ; interprétation à rapprocher de `core_pattern` |
| `kernel.dmesg_restrict` | `0` | Restriction spécifique de lecture du journal noyau désactivée ; aucun test de lecture par un compte non privilégié fourni |
| `kernel.kptr_restrict` | `1` | Valeur effective et directive dans `10-kernel-hardening.conf:15` concordantes |
| `kernel.sysrq` | `176` | Masque de fonctions, et non simple booléen ; directive concordante dans `10-magic-sysrq.conf:26` |
| `net.ipv4.ip_forward`, `net.ipv4.conf.all.forwarding` | `1`, `1` | Transfert IPv4 activé ; origine à établir en tenant compte de Docker |
| `net.ipv4.conf.all.rp_filter` | `2` | Filtrage de chemin retour en mode souple ; directive concordante dans `10-network-security.conf:5`, qui fixe aussi `default.rp_filter=2` |
| `net.ipv4.conf.all.log_martians`, `net.ipv4.conf.default.log_martians` | `0`, `0` | Valeurs confirmées ; journalisation correspondante désactivée à ces niveaux |
| `net.ipv4.conf.all.send_redirects` | `1` | Valeur globale activée ; vérifier aussi les interfaces |
| `net.ipv4.conf.default.accept_redirects`, `net.ipv4.conf.default.accept_source_route` | `1`, `1` | Valeurs par défaut relevées ; elles ne prouvent pas les valeurs de chaque interface existante |
| `net.ipv6.conf.all.accept_redirects`, `net.ipv6.conf.default.accept_redirects` | `1`, `1` | Valeurs relevées ; vérifier les interfaces et leur rôle réseau |

La recherche affiche aussi `all.use_tempaddr=2` et `default.use_tempaddr=2`
dans `10-ipv6-privacy.conf` ; leurs valeurs effectives ne figurent pas dans
la commande `sysctl` fournie. Pour les autres valeurs, aucune directive ne
ressort de cette recherche dans `/etc/sysctl.conf` et `/etc/sysctl.d`.
Cela n’établit pas leur origine : les répertoires fournisseurs et d’exécution,
les valeurs par défaut et les changements effectués par les services ne sont
pas tous couverts. Les erreurs de recherche sont également masquées.

**Conclusion `KRNL-6000` : valeurs effectives confirmées**, mais aucune
modification globale ne doit être déduite du seul écart au profil Lynis.
La présence d’une directive concordante ne constitue pas un test de persistance
après redémarrage. Docker peut nécessiter le transfert IPv4 ; sa désactivation
peut couper le réseau du conteneur File Browser.

Les valeurs `default` servent de référence pour les nouvelles interfaces ;
l’interprétation de `all` dépend du paramètre. En particulier, le mode
`rp_filter=2` est un filtrage souple, pas une absence de filtrage, et
`default.accept_source_route=1` ne démontre pas à lui seul une acceptation
sur les interfaces actuelles. Voir la
[documentation réseau du noyau](https://kernel.org/doc/html/latest/networking/ip-sysctl.html)
et la [documentation de suid_dumpable](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/fs.html).

Pour compléter sans appliquer de valeur :

```bash
sysctl kernel.core_pattern
ip -br link
sysctl -a 2>/dev/null | LC_ALL=C sort | \
  grep -E '^net\.ipv[46]\.conf\.[^.]+\.(forwarding|rp_filter|accept_redirects|send_redirects|accept_source_route|log_martians) ='
```

Consulter `man sysctl`, `man sysctl.d` et la documentation du paramètre avant de
proposer une valeur persistante.

## 8. Docker et le constat `CONT-8106`

Lynis n'a pas déterminé le nombre de conteneurs et demande de comparer les
informations Docker :

```bash
sudo docker ps -a \
  --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
sudo docker info --format \
  'Containers={{.Containers}} Running={{.ContainersRunning}} Paused={{.ContainersPaused}} Stopped={{.ContainersStopped}}'
sudo stat -c '%U:%G %a %n' \
  /var/run/docker.sock /run/containerd/containerd.sock
getent group docker
```

### Résultats transmis le 1er octobre 2026

| Vérification | État observé | Conclusion |
| --- | --- | --- |
| `docker ps -a` | Un seul conteneur `filebrowser`, image `filebrowser/filebrowser:v2.15.0`, état `Exited (1) 20 hours ago`, colonne ports vide | Conteneur arrêté avec code de sortie 1 ; arrêt rattaché au 30 septembre à 14:42:59 +02:00 et à l’arrêt volontaire de la VM |
| `docker info` | `Containers=1 Running=0 Paused=0 Stopped=1` | Compteurs cohérents avec la liste : un conteneur arrêté et aucun en cours d’exécution |
| Socket Docker | `/var/run/docker.sock`, `root:docker`, `660` | Lecture/écriture accordées au propriétaire et au groupe selon les modes ; ACL et accès via sudo non évalués ici |
| Socket containerd | `/run/containerd/containerd.sock`, `root:root`, `660` | Lecture/écriture accordées au propriétaire et au groupe root selon les modes |
| Groupe Docker | `docker:x:135:` | Aucun membre supplémentaire déclaré dans la liste du groupe ; ne suffit pas à exclure tous les moyens d’accès au démon |

**Conclusion `CONT-8106` : inventaire manuel cohérent.** Le compteur indéterminé
signalé par Lynis n’est pas reproduit par ces commandes. La cause de son échec
de collecte reste inconnue ; cette comparaison ne constitue pas un nouveau
passage Lynis.

**État File Browser actualisé : arrêté.** L’observation précédente d’un
conteneur actif et sain correspond à un état antérieur. L’application ne
fonctionne pas dans ce conteneur au moment du relevé. La colonne ports vide
ne suffit pas à établir la configuration des ports publiés ; aucune mesure
d’accessibilité distante n’est fournie ici. Le code 1 seul ne permet pas de distinguer une panne d’une sortie lors
d’un arrêt demandé.

Le complément reçu à **11:17:25 +02:00 le 1er octobre** précise l’arrêt :
`StartedAt` correspond au 30 septembre à **09:39:25 +02:00**, et `FinishedAt`
au même jour à **14:42:59 +02:00**. Docker indique `OOMKilled=false`,
`Error=""`, `RestartCount=0`, `RestartPolicy=no`. Les logs montrent
`Caught signal terminated: shutting down.` puis la fermeture du listener TCP.
L’utilisateur confirme avoir arrêté la VM à cette heure. Le journal Docker
et containerd montre la terminaison demandée et les deux unités arrêtées
avec succès : l’arrêt volontaire est corroboré. Le code 1 ne suffit pas à conclure à une panne spontanée. Les
requêtes HTTP 404 antérieures ne prouvent ni exploitation ni causalité.
Voir le [complément C11 de l’analyse consolidée](consolider-resultats-greenbone-lynis.md#complement-c11-etat-et-journaux-recus-a-111725-0200).

Conserver l’état avant de relancer ou recréer le conteneur. Dans la VM,
recueillir les éléments suivants, sans modification :

```bash
date -Is
sudo docker inspect filebrowser --format \
  'Status={{.State.Status}} ExitCode={{.State.ExitCode}} OOMKilled={{.State.OOMKilled}} Error={{json .State.Error}} StartedAt={{.State.StartedAt}} FinishedAt={{.State.FinishedAt}} RestartCount={{.RestartCount}} RestartPolicy={{.HostConfig.RestartPolicy.Name}}'
sudo docker logs --timestamps --tail 80 filebrowser
```

Relire les journaux avant de les transmettre : masquer les éventuels secrets
et données internes. `docker top` ne permettra de relever l’identité du
processus qu’une fois le conteneur en cours d’exécution.

## 9. CUPS et permissions associées

Lynis signale `PRNT-2307` et une attention sur les permissions. Les contrôles
réseau et fonctionnels ont déjà établi :

- `cups.service` et `cups.socket` actifs et activés ;
- écoute limitée à `127.0.0.1:631`, `[::1]:631` et au socket Unix ;
- `Browsing Off`, interface web locale et opérations sensibles restreintes ;
- aucune imprimante configurée.

Les commandes suivantes ont été exécutées pour préciser le constat :

```bash
sudo grep -nF 'PRNT-2307' /var/log/lynis.log
sudo stat -c '%U:%G %a %n' \
  /etc/cups /etc/cups/cupsd.conf /etc/cups/cups-files.conf \
  /run/cups/cups.sock
sudo namei -l /etc/cups/cupsd.conf
```

### Résultats transmis le 1er octobre 2026

Le journal Lynis indique à **10:02:37** le test `PRNT-2307`
(`Check CUPSd configuration file permissions`), puis la suggestion de
restreindre davantage l’accès à la configuration. L’extrait complémentaire identifie `/etc/cups/cupsd.conf` comme fichier
trouvé, puis relève `rw-r--r--` pendant `PRNT-2307` : la suggestion est donc
rattachée au mode `644` de ce fichier. Lynis attribue **1 point sur 2** à ce
contrôle. Le mode exact attendu n’est pas indiqué dans cet extrait.

| Chemin | Propriétaire et mode | Conclusion selon les modes Unix observés |
| --- | --- | --- |
| `/etc/cups` | `root:lp`, `755` | Répertoire listable et traversable par les autres utilisateurs ; seul root peut modifier ses entrées |
| `/etc/cups/cupsd.conf` | `root:root`, `644` | Fichier lisible par les autres utilisateurs locaux, modifiable seulement par root |
| `/etc/cups/cups-files.conf` | `root:root`, `644` | Même constat de lecture et d’écriture |
| `/run/cups/cups.sock` | `root:root`, `666` | Permissions du socket ouvertes aux utilisateurs locaux ; elles ne prouvent pas une autorisation d’administration dans CUPS |

`namei -l` confirme `/` et `/etc` en `root:root 755`, puis le répertoire
et le fichier avec les modes ci-dessus. Aucun composant affiché du chemin
`cupsd.conf` n’est modifiable par les autres utilisateurs selon ces modes.
Les ACL n’ont pas été relevées dans ce contrôle.

**Conclusion : suggestion Lynis confirmée dans le journal et permissions
précises documentées, avec `/etc/cups/cupsd.conf` en `644` comme fichier
concerné par `PRNT-2307`.** Ces sorties ne prouvent pas une modification non
autorisée, la présence de secrets dans les fichiers ou un contournement des
règles d’autorisation CUPS. Le mode cible attendu par cette version de Lynis reste à
préciser avant de choisir un changement.

Dans le même extrait, `PRNT-2308` relève `localhost:631` et conclut
`CUPS daemon only running on localhost`, avec **2 points sur 2** pour ce
contrôle réseau. Cette preuve concorde avec l’écoute locale déjà documentée ;
le résultat du test de permissions et celui du test réseau sont distincts.

L’écoute locale atténue l’exposition distante déjà observée ; elle ne supprime
pas l’accès local aux fichiers et au socket. CUPS n’a aucun rôle métier
identifié sur ce serveur. Ne pas appliquer de `chmod` au socket à ce stade :
le besoin du service et ses règles d’accès doivent d’abord être examinés.

Commande utilisée pour relever le contexte du test, sans modifier la VM :

```bash
sudo sed -n '6628,6645p' /var/log/lynis.log
```

Relire cet extrait avant diffusion et masquer les éventuelles données internes.

## Tableau de synthèse

| Constat Lynis ou question | Vérification | État réellement observé | Conclusion |
| --- | --- | --- | --- |
| `SSH-7408` | `sshd -t`, `sshd -T`, configurations SSH | Plusieurs valeurs permissives confirmées | **Confirmé** ; changement à préparer avec accès de secours |
| Compte Greenbone | `getent`, `id`, `sudo -l`, `stat` | Compte non privilégié, `.ssh` 700, clés 600 | **Confirmé** ; périmètre du scan limité aux droits du compte |
| Comptes administratifs | UID 0 et groupes privilégiés | Seul `root` UID 0 ; `oliv` dans `sudo` et `adm` ; liste Docker vide | **Confirmé** pour l’inventaire ; règles sudo de `oliv` et accès effectif Docker à compléter |
| Permissions de `/srv/filebrowser` | `stat`, `namei`, `find`, ACL et montage Docker | Répertoires `root:root` 755, aucun fichier affiché, ACL de base sur quatre chemins, montage RW | **Confirmé** pour ces observations ; identité du processus, ACL des sous-répertoires et droits applicatifs à compléter |
| Correctifs | `dpkg-query`, `apt-cache policy`, Ubuntu Pro | Cinq paquets installés, versions candidates identiques ; VM non rattachée à Pro | **Confirmé** pour les versions et le non-rattachement ; fraîcheur APT et accès aux correctifs ESM à compléter |
| `ACCT-9628` | systemd, paquets et rétention | journald/rsyslog actifs, auditd et audispd-plugins absents ; 48,0 Mo de journaux sur disque | Absence auditd **confirmée** ; durée de rétention à compléter |
| `KRNL-6000` | `sysctl` et fichiers persistants | Quinze valeurs effectives relevées ; trois paramètres avec directives concordantes | **Confirmé** pour les valeurs ; interfaces, origine et persistance à compléter avec les besoins Docker |
| `CONT-8106` | `docker ps -a`, `docker info`, sockets | Un conteneur, arrêté avec code 1 ; compteurs concordants ; sockets 660 | Inventaire **cohérent** ; arrêt VM volontaire expliqué ; besoin de reprise à préciser |
| `PRNT-2307` | CUPS, journal Lynis et permissions | `PRNT-2307` : cupsd.conf 644, 1/2 point ; `PRNT-2308` : localhost:631, 2/2 points ; socket 666 | Fichier concerné et écoute locale **confirmés** ; mode cible à préciser, exposition distante atténuée |

## Conclusion attendue

Une recommandation Lynis devient exploitable seulement lorsque la valeur
effective, son origine, son usage et ses conséquences sont compris. Les
contrôles déjà réalisés confirment plusieurs points SSH et l'absence de besoin
visible pour CUPS. Les modes des répertoires File Browser sont relevés ; les
droits applicatifs, l’identité du processus, les privilèges Docker,
la rétention des journaux et le contexte des paramètres noyau doivent encore être complétés avant toute
modification.

## Ressources

- [Documentation Lynis](https://cisofy.com/documentation/lynis/)
- [Manuel OpenSSH `sshd_config`](https://man.openbsd.org/sshd_config)
- [Documentation des paramètres noyau Linux](https://docs.kernel.org/admin-guide/sysctl/)
- [Documentation Docker Engine](https://docs.docker.com/engine/)

- [Activité précédente — Analyser et prioriser les résultats de Lynis](analyser-prioriser-resultats-lynis.md)
- [Activité suivante — Consolider les résultats Greenbone et Lynis](consolider-resultats-greenbone-lynis.md)
- [Retour à l'itération 2](index.md)
