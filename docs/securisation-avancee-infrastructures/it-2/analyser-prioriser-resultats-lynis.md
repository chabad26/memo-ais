# Analyser et prioriser les résultats de Lynis

## Objectif

Évaluer les avertissements et suggestions de Lynis, sélectionner ceux qui
présentent le plus de risque pour le serveur File Browser et analyser précisément
deux à trois modifications possibles avant toute remédiation.

**Prérequis réalisé :** l'[installation et la découverte de Lynis](installer-decouvrir-lynis.md)
ont produit un second audit exploitable avec l'auditeur `AIS-lab` : 4
avertissements, 52 suggestions, 221 tests et un indice de durcissement de 57.
Les nouvelles tailles et empreintes des fichiers restent à relever pour fermer
la chaîne de preuve.

Les résultats analysés décrivent la **VM Ubuntu hôte**. La détection de Docker
par Lynis ne constitue pas une analyse du contenu de l’image File Browser.

## Règle de travail

Une fois le rapport produit, ne pas modifier les fichiers de configuration,
installer un autre paquet, activer ou arrêter un service, changer une règle de
filtrage ou recharger un daemon. Une recommandation générique de Lynis ne devient
pas automatiquement une modification adaptée au serveur.

La documentation officielle précise que les avertissements et suggestions sont
associés à un identifiant de test. Le rapport se trouve normalement dans
`/var/log/lynis-report.dat` et le détail technique dans `/var/log/lynis.log`.
Les fichiers peuvent être remplacés par une nouvelle exécution de Lynis. Sur la
version 2.6.2 observée, même `lynis show version` a réécrit le rapport. Après un
audit, ne plus lancer Lynis avant d'avoir copié le rapport et le journal. Le
détail de cet incident figure dans la feuille précédente.

## Étape 1 — Identifier le rapport analysé

Dans la **VM cible**, relever les métadonnées sans exécuter de nouveau Lynis :

```bash
date -Is
hostname
dpkg-query -W -f='${binary:Package}\t${Version}\t${db:Status-Abbrev}\n' \
  lynis
sudo stat -c '%n | %s octets | %y | %U:%G | %a' \
  /var/log/lynis-report.dat /var/log/lynis.log
sudo sha256sum /var/log/lynis-report.dat /var/log/lynis.log
```

Si `lynis` reste introuvable après l'installation, rechercher son emplacement :

```bash
command -v lynis
sudo find /usr /opt /root -maxdepth 3 -type f -name lynis 2>/dev/null
```

Ne pas exécuter Lynis uniquement pour retrouver sa version : utiliser le paquet
installé ou le champ `lynis_version` du rapport déjà sauvegardé.

Extraire ensuite les données utiles du rapport :

```bash
sudo grep -E '^(warning|suggestion)\[\]=' \
  /var/log/lynis-report.dat

sudo grep -E \
  '^(hardening_index|lynis_version|os|os_name|os_version|linux_kernel_version|scan_mode|auditor)=' \
  /var/log/lynis-report.dat
```

Pour chaque identifiant retenu, retrouver ce que Lynis a réellement testé :

```bash
TEST_ID='IDENTIFIANT-LYNIS'
sudo grep -nF "$TEST_ID" /var/log/lynis.log
sudo grep -nF "$TEST_ID" /var/log/lynis-report.dat
```

Remplacer `IDENTIFIANT-LYNIS` par l'identifiant exact, par exemple une valeur de
la forme `SSH-####` ou `KRNL-####`. Conserver l'extrait avec quelques lignes de
contexte si le motif seul ne suffit pas à comprendre l'observation. Tant que la
valeur littérale `IDENTIFIANT-LYNIS` n'est pas remplacée, l'absence de résultat
est normale et ne prouve pas l'absence de constat.

## Étape 2 — Construire la liste des constats

Un **warning** demande généralement une attention forte ; une **suggestion**
signale souvent une amélioration possible. Ce type ne suffit pas à fixer la
priorité. Le nombre de suggestions et l'indice de durcissement ne remplacent pas
l'analyse du risque propre au serveur.

Recopier les résultats significatifs sans les reformuler trop tôt :

| Rang provisoire | Identifiant Lynis | Type | Texte exact abrégé | Élément concerné | Preuve dans le journal | Doublon d'un constat Greenbone ? |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `SSH-7408` | Suggestion | Durcir plusieurs paramètres SSH | `sshd` | `AllowTcpForwarding`, `MaxAuthTries`, `PermitRootLogin` et huit autres paramètres signalés | Oui, complète le constat Greenbone SSH |
| 2 | `ACCT-9628` | Suggestion | Activer auditd | Traçabilité système | `Checking auditd [NON TROUVÉ]` | Non |
| 3 | `PRNT-2307` | Suggestion | Restreindre l'accès à la configuration CUPS | CUPS | Permissions en attention et accès jugé perfectible | Non |
| 4 | `CONT-8106` | Suggestion | Comparer `docker ps -a` et `docker info` | Docker | Nombre de conteneurs indéterminé par Lynis | Oui, complète l'inventaire local |
| 5 | `KRNL-6000` | Suggestion | Plusieurs valeurs sysctl diffèrent du profil | Noyau et réseau | Liste des valeurs `DIFFERENT` dans la sortie | Non |

Regrouper les tests qui décrivent le même problème. Par exemple, une suggestion
sur un paramètre SSH et le constat Greenbone sur le service SSH peuvent alimenter
un seul risque, tout en conservant leurs preuves distinctes.

## Étape 3 — Prioriser dans le contexte du serveur

Attribuer une priorité après avoir répondu aux questions suivantes :

| Dimension | Question pour le cas fil rouge |
| --- | --- |
| Problème | Quel défaut précis Lynis signale-t-il ? S'agit-il d'une absence de contrôle, d'une configuration faible ou d'un composant inutile ? |
| Exposition | Le composant est-il joignable depuis Internet, seulement depuis la VM, ou uniquement par un compte déjà privilégié ? |
| Exploitabilité | Quels accès, droits, entrées contrôlées ou options doivent être réunis ? |
| Conséquences | Le défaut peut-il compromettre les documents, les comptes, l'hôte Docker ou la disponibilité du service ? |
| Protections présentes | Filtrage, boucle locale, AppArmor, droits Unix, authentification, journalisation ou autre mesure réduisent-ils réellement le scénario ? |
| Rôle du serveur | La mesure protège-t-elle l'échange de documents et ses partenaires ? Le composant a-t-il un besoin métier ? |
| Faisabilité | La modification risque-t-elle de couper SSH, File Browser, Docker ou l'accès aux documents ? |

Utiliser l'échelle suivante :

| Priorité | Sens retenu |
| --- | --- |
| **P1 — immédiate** | Défaut confirmé, exposé ou facilement atteignable, avec impact fort et protection insuffisante |
| **P2 — haute** | Risque important mais soumis à une condition, à un accès préalable ou à une mesure compensatoire |
| **P3 — planifiée** | Amélioration utile dont l'exploitation est limitée ou l'impact modéré dans ce contexte |
| **P4 — faible** | Mesure d'hygiène ou d'optimisation avec faible effet direct sur le risque étudié |
| **À investiguer** | Preuve, configuration effective, dépendance ou conséquence encore inconnue |

Les faits déjà observés servent de contexte, sans être présentés comme des
résultats Lynis : SSH écoute sur toutes les interfaces, Docker héberge File
Browser, CUPS est actif mais limité aux boucles locales, et plusieurs correctifs
Focal nécessitent d'étudier l'accès ESM. Un test Lynis lié à ces composants doit
être confronté à ces preuves.

### Classement final

| Rang | Identifiant et constat Lynis | Priorité | Exposition | Impact principal | Protection existante | Justification synthétique |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `SSH-7408` — paramètres SSH permissifs | **P1** | Port 22 joignable depuis la machine d'audit ; serveur supposé exposé dans le cas fil rouge | Accès privilégié, tentatives répétées et création de tunnels | Clés publiques disponibles ; `gvm-audit` sans sudo ; tunnel SSH désactivé mais transfert TCP autorisé | Plusieurs paramètres sont confirmés localement et concernent directement le service d'administration |
| 2 | `ACCT-9628` — auditd absent | **P2** | Après accès au système | Perte de traces utiles pour détecter et reconstruire un incident | journald et rsyslog actifs | Le module doit ensuite traiter un incident et centraliser les événements avec Wazuh |
| 3 | `PRNT-2307` — CUPS actif sans imprimante | **P3** | Boucles locales uniquement | Surface logicielle et fonctions d'administration inutiles | Écoute limitée à `127.0.0.1` et `::1`, découverte désactivée | Le risque distant est réduit, mais aucun besoin métier d'impression n'est établi |
| 4 | `CONT-8106` — inventaire Docker incohérent | **À investiguer** | Hôte Docker | Visibilité incomplète sur le conteneur qui fournit le service métier | Un conteneur File Browser a déjà été inventorié avec `docker ps` | Il faut déterminer si l'écart vient de Lynis 2.6.2, des droits ou de Docker avant de conclure |
| 5 | `KRNL-6000` — valeurs sysctl différentes | **À investiguer** | Noyau local et fonctions réseau | Divulgation d'informations ou comportement réseau moins strict | ASLR, protections des liens et SYN cookies conformes au profil | Certaines valeurs peuvent être durcies, mais `ip_forward=1` peut être nécessaire à Docker |

Les paramètres SSH arrivent en tête car ils protègent l'accès d'administration
joignable sur le réseau. L'absence d'auditd n'ouvre pas directement un accès,
mais elle réduit la capacité à comprendre les actions réalisées lors de
l'incident prévu dans le module. CUPS est moins prioritaire grâce à son écoute
locale ; son absence de rôle métier justifie néanmoins d'étudier sa désactivation.

## Étape 4 — Choisir les vérifications manuelles

Employer les commandes correspondant au composant signalé. Cette liste sert de
repère ; seules les commandes liées aux constats retenus sont nécessaires.

| Famille de constat | Vérifications en lecture | Sources à consulter |
| --- | --- | --- |
| SSH | `sudo sshd -t`, `sudo sshd -T`, lecture de `/etc/ssh/sshd_config` et de `sshd_config.d` | `man sshd_config`, documentation OpenSSH et Ubuntu |
| Service ou port | `systemctl status`, `systemctl is-enabled`, `systemctl cat`, `sudo ss -lntup` | page de manuel de l'unité et documentation du service |
| Comptes et privilèges | `getent passwd`, `id`, `sudo -l -U`, `passwd -S`, `chage -l` | `man passwd`, `man sudoers`, politique locale |
| Permissions | `stat`, `namei -l`, `getfacl` si disponible | `man chmod`, `man chown`, documentation de l'application |
| Pare-feu | `sudo ufw status verbose`, `sudo nft list ruleset`, `sudo iptables-save` | documentation du mécanisme réellement actif |
| Paramètre noyau | `sysctl NOM_DU_PARAMETRE`, lecture de `/etc/sysctl.conf` et `/etc/sysctl.d` | `man sysctl`, `man sysctl.d`, documentation Ubuntu |
| Journalisation | `systemctl status rsyslog auditd`, `journalctl`, lecture des fichiers concernés | `man journald.conf`, `man rsyslog.conf`, `man auditd.conf` |
| Correctifs | `dpkg-query -W`, `apt-cache policy`, `pro status` si présent | avis Ubuntu et documentation Ubuntu Pro |
| Conteneurs | `docker version`, `docker info`, `docker inspect` avec formats ciblés, permissions des sockets | documentation Docker et avis Ubuntu |

Une commande absente ou un service inexistant est un résultat à documenter. Ne
pas installer un outil pendant cette phase uniquement pour faire disparaître
une suggestion Lynis.

## Étape 5 — Décrire une modification sans l'appliquer

Pour chaque modification envisagée, préciser :

1. le fichier, l'unité, le paquet ou la règle concernés ;
2. la valeur actuelle observée ;
3. la valeur proposée, écrite exactement ;
4. la commande de contrôle de syntaxe ;
5. le rechargement ou redémarrage qui serait nécessaire plus tard ;
6. le test de sécurité et le test fonctionnel à réaliser ;
7. le retour arrière prévu.

Ne pas écrire seulement « durcir SSH » ou « activer le pare-feu ». Une action
est exploitable lorsqu'elle désigne, par exemple, la directive et sa valeur,
le fichier prévu, la validation de syntaxe et les flux qui devront rester
autorisés. Cette description ne vaut pas autorisation d'exécution.

## Analyse détaillée 1

| Élément | Analyse |
| --- | --- |
| Constat ou suggestion Lynis | `SSH-7408` — durcir la configuration SSH |
| Risque identifié | Des options permissives facilitent les tentatives d'authentification, l'accès direct à `root` par clé et l'utilisation du serveur comme relais après compromission d'un compte. |
| Raisons de sa priorité | SSH écoute sur toutes les interfaces de la VM et sert à l'administration. Une compromission donne accès à l'hôte qui exécute File Browser et stocke les documents. |
| Configuration actuelle | `MaxAuthTries 6`, `PermitRootLogin without-password`, `PasswordAuthentication yes`, `AllowTcpForwarding yes`. Lynis signale aussi `X11Forwarding yes`, `AllowAgentForwarding yes`, `LogLevel INFO` et `MaxSessions 10`, à confirmer avec la configuration effective complète. |
| Vérification effectuée | Le 1er octobre : `sudo sshd -t` ne retourne aucune erreur ; `sudo sshd -T` confirme les quatre premières valeurs ; `ss` confirme l'écoute sur `0.0.0.0:22` et `[::]:22`. |
| Modification nécessaire | Après vérification de tous les accès administratifs, créer `/etc/ssh/sshd_config.d/99-hardening.conf` avec `PermitRootLogin no`, `MaxAuthTries 3`, `AllowTcpForwarding no`, `X11Forwarding no`, `AllowAgentForwarding no` et `LogLevel VERBOSE`. Valider avec `sudo sshd -t`, garder une console ouverte, puis prévoir `sudo systemctl reload ssh`. Sauvegarder le fichier et le supprimer pour le retour arrière. |
| Effet attendu sur la sécurité | Supprimer la connexion directe de `root`, réduire les essais par connexion, limiter les fonctions de rebond et améliorer les traces. |
| Impact possible sur le fonctionnement | Les tunnels, X11 et le transfert d'agent cesseraient de fonctionner. Une erreur pourrait couper l'administration ; les scans Greenbone par clé et l'accès habituel doivent être testés avant fermeture de la session existante. |
| Décision | **À appliquer**, après vérification des dépendances et de l'accès de secours |
| Justification | Les valeurs faibles sont confirmées et concernent le point d'administration. La désactivation de l'authentification par mot de passe reste à étudier séparément après vérification des clés de tous les administrateurs. |

## Analyse détaillée 2

| Élément | Analyse |
| --- | --- |
| Constat ou suggestion Lynis | `ACCT-9628` — auditd non détecté |
| Risque identifié | Les événements sensibles du noyau et certaines actions d'administration peuvent ne pas être tracés avec le niveau de détail nécessaire à une enquête. |
| Raisons de sa priorité | Le module prévoit une détection Wazuh et la reconstruction d'une chronologie d'incident sur ce serveur. |
| Configuration actuelle | Lynis détecte journald et rsyslog, mais indique `Checking auditd [NON TROUVÉ]`. L'état du paquet et de l'unité reste à confirmer manuellement. |
| Vérification effectuée | À faire en lecture : `dpkg-query -W auditd audispd-plugins`, `systemctl status auditd --no-pager` et `sudo auditctl -s` si la commande existe. |
| Modification nécessaire | Si l'absence est confirmée, prévoir `sudo apt install --no-install-recommends auditd audispd-plugins`, puis définir un jeu limité de règles dans `/etc/audit/rules.d/ais.rules`. Contrôler avec `sudo augenrules --check`, charger lors d'une fenêtre prévue et vérifier avec `sudo auditctl -s` et `sudo ausearch`. Conserver les fichiers initiaux pour le retour arrière. |
| Effet attendu sur la sécurité | Fournir des événements structurés pour les changements sensibles et améliorer la chronologie transmise à Wazuh. |
| Impact possible sur le fonctionnement | Consommation de disque et de CPU, bruit important ou doublons avec journald/Wazuh si les règles sont trop larges. Les limites de rotation doivent être dimensionnées. |
| Décision | **À investiguer**, puis à appliquer avec un jeu de règles ciblé |
| Justification | Le bénéfice est fort pour l'investigation, mais l'installation, les règles exactes et leur volume doivent être validés avant activation. |

## Analyse détaillée 3

| Élément | Analyse |
| --- | --- |
| Constat ou suggestion Lynis | `PRNT-2307` — accès à la configuration CUPS perfectible |
| Risque identifié | Un service sans rôle métier augmente la surface d'attaque et maintient une interface d'administration locale inutile. |
| Raisons de sa priorité | Le serveur héberge File Browser et aucune fonction d'impression n'est attendue. Le risque immédiat reste limité par l'écoute locale. |
| Configuration actuelle | `cups.service` et `cups.socket` sont actifs et activés. CUPS écoute seulement sur `127.0.0.1:631` et `[::1]:631`, `Browsing Off`, avec interface web locale ; aucune destination d'impression n'est configurée. |
| Vérification effectuée | `systemctl`, `ss`, lecture ciblée de `cupsd.conf` et `lpstat -r -v -p` le 1er octobre 2026. Les permissions précises signalées par Lynis restent à identifier dans le journal. |
| Modification nécessaire | Si aucune dépendance n'utilise CUPS, prévoir `sudo systemctl disable --now cups.service cups.socket cups.path`, puis éventuellement masquer ces trois unités. Vérifier l'absence d'écoute 631 et le fonctionnement de File Browser. Le retour arrière consiste à démasquer les unités, puis réactiver `cups.socket`. |
| Effet attendu sur la sécurité | Retirer un service et une interface d'administration sans fonction attendue sur ce serveur. |
| Impact possible sur le fonctionnement | Toute impression locale ou application dépendant de CUPS cesserait de fonctionner ; aucun besoin de ce type n'est actuellement identifié. |
| Décision | **À appliquer** après validation du propriétaire du service |
| Justification | La mesure correspond au rôle du serveur et réduit la surface locale, mais la décision métier doit précéder la désactivation. |

## État final attendu

- Lynis est installé depuis une source documentée et sa version est conservée.
- Le second rapport et son journal Lynis sont identifiés par date et empreinte.
- Les résultats significatifs sont reliés à leur identifiant de test et à la
  preuve correspondante dans le journal.
- Un classement contextualisé explique les premières priorités.
- Deux à trois constats possèdent une vérification manuelle et une modification
  exacte proposée, avec effet attendu, impact fonctionnel et décision.
- Aucune modification n'a encore été appliquée.

## Ressources

- [Documentation officielle Lynis](https://cisofy.com/documentation/lynis/).
- [Démarrage, rapport et journal Lynis](https://cisofy.com/documentation/lynis/get-started/).
- [Catalogue officiel des contrôles Lynis](https://cisofy.com/lynis/controls/).

- [Activité précédente — Installer et découvrir Lynis](installer-decouvrir-lynis.md)
- [Activité suivante — Vérifier la configuration du système](verifier-configuration-systeme.md)
- [Retour à l'itération 2](index.md)
- [Pense-bête de l'itération](../../pense-bete/glossaire/securisation-avancee-infrastructures/it-2.md)
- [Dossier de preuves](../dossier-preuves.md)
