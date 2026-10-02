# Finaliser le compte-rendu de durcissement

**Itération 4 — 1 h — Travail individuel — 2 octobre 2026**

## 🎯 Objectif

Documenter les remédiations réalisées et préparer la vérification globale du
J5. Cette feuille constitue le **compte-rendu de durcissement de J4**, à compléter
en J5 pour constituer le **compte-rendu de durcissement et de vérification**
utilisé pour la validation de C2. La validation globale de C2 n’est pas acquise
par la seule réalisation des changements.

**Auteur des interventions : Olivier.** Les résultats proviennent des commandes,
captures, tests fonctionnels déclarés et rapports transmis. Le
[journal détaillé de mise en œuvre](mettre-en-oeuvre-verifier-remediations.md)
conserve les étapes, les captures et les retours arrière. Cette synthèse distingue
les lots vérifiés des risques et investigations encore ouverts.

## Déroulement — Finaliser à partir des preuves de la journée

| Temps indicatif | Travail | Résultat attendu |
| --- | --- | --- |
| 15 min | Rapprocher le plan initial des changements réalisés | Tableau des remédiations avec statut et preuve |
| 15 min | Expliquer adaptations, incidents et diagnostic | Écarts motivés et problèmes attribuables |
| 15 min | Séparer risques résiduels et investigations | Actions non réalisées justifiées |
| 15 min | Préparer la comparaison et les tests J5 | Matrice de vérification globale à compléter |

Ces durées organisent l’activité ; elles ne mesurent pas le temps réel des
interventions réalisées dans le laboratoire.

## 1. Périmètre et état de référence

Le [rapport d’audit J3](../it-3/finaliser-rapport-plan-remediation.md) et la
[préparation J4](preparer-remediations.md) constituent les références du plan.
Le laboratoire est une VM administrée par SSH, hébergeant File Browser dans
Docker sur le port 8080. Greenbone est sur le poste hôte et utilise un compte
`gvm-audit` avec sa propre clé SSH. L’exposition Internet du cas pédagogique
n’est pas une exposition Internet démontrée du laboratoire.

| Composant | État initial documenté | État actuel documenté |
| --- | --- | --- |
| OS | Ubuntu 20.04.6 LTS | Ubuntu 26.04.1 LTS, noyau 7.0.0-38-generic |
| Stockage | Disque virtuel 25 Gio, racine proche de la saturation pour une migration | Disque 40 Gio, racine ext4 environ 39 Gio, environ 19 Gio libres lors des contrôles |
| SSH | Mot de passe permis, root prohibit-password, deux MAC UMAC-64 offerts | Paquet 1:10.2p1-2ubuntu3.6 ; root/password/interactif interdits, clés permises, deux MAC retirés |
| Moteurs | Versions anciennes inventoriées dans l’audit | docker.io 29.1.3-0ubuntu4.1 ; containerd 2.2.2-0ubuntu1.1 |
| Application | File Browser 2.15.0 ; identifiants admin par défaut acceptés selon le test utilisateur | Version 2.63.23 ; ancien mot de passe refusé, nouveau accès confirmé |
| Audit ciblé | auditd absent | auditd actif, sept règles b64 persistantes, lost 0 |
| Impression | CUPS actif sur loopback, aucune imprimante configurée | Trois unités masquées/inactives ; aucune écoute 631 |

La nouvelle image est fixée au digest
`sha256:a469ea076d4a1b4b1d86a41d130f2f536cd9da996a2b1fb39c0d7635f9d89b9a`.
Les répertoires config, database et documents sont montés depuis
`/srv/filebrowser-persistent.QkyszX`. Conserver l’association de chaque scan à
son image exacte ; une étiquette ou un nom de fichier seul ne suffit pas.

## 2. Remédiations réalisées et vérifiées

| Action | Modification réalisée | Vérification et résultat | Statut J4 / limite |
| --- | --- | --- | --- |
| R01 — OS et moteurs | Migration par étapes 20.04 → 22.04 → 24.04 → 26.04 ; agrandissement du disque | Versions et captures, mises à jour sans paquet restant, aucune unité en échec, accès et application fonctionnels | Réalisée ; clôture de chaque CVE distincte du fonctionnement |
| R02 — SSH | Fragment local : root interdit, clés conservées, password/interactif désactivés, deux MAC UMAC-64 exclus | Configuration effective, essai password refusé, nouvelle connexion par clé depuis le poste hôte et sudo réussi | Premier lot validé ; autres suggestions SSH non appliquées |
| R03 — Application | Test de migration sur copie, bascule vers 2.63.23 avec données persistantes | Version visible, healthy, téléchargement/upload/suppression validés ; Trivy examiné | Réalisée ; maintenance future et dix HIGH résiduels ouverts |
| R04 — Conteneur | UID 1000 observé ; cap-drop ALL et no-new-privileges | Processus applicatif : CapEff/CapBnd nuls, NoNewPrivs 1, Seccomp 2 ; parcours sur 8080 réussi | Lot validé ; racine en lecture seule hors lot |
| R05 — Audit | Installation, sept règles ciblées b64, rotation/rétention | Création/suppression ais_ssh retrouvées avant et après reboot ; règles persistantes ; rotations manuelles réussies ; lost 0 | Validée dans ce périmètre ; rotation automatique au seuil et autres règles non testées individuellement |
| R06 — CUPS | Arrêt puis masquage des trois unités après reprise inattendue | masked/inactive après reboot ; aucune écoute 631 ; service applicatif maintenu | Arrêt persistant validé ; paquets conservés, CVE non corrigées par l’arrêt seul |
| R07 — sysctl | FIFO et restriction adresses noyau à 2 ; redirections IPv4/IPv6 à 0 | Valeurs effectives après reboot ; SSH et opérations applicatives confirmés | Deux lots validés ; pas de test d’exploitation ciblé |
| R08 — Reprise | Docker activé, unless-stopped, montages persistants | File Browser healthy après plusieurs redémarrages | Reprise validée sur les redémarrages observés ; pas un engagement de disponibilité |
| R09 — Identifiants | Mot de passe administrateur changé selon Olivier | Ancien identifiant refusé en session privée, capture Wrong credentials ; nouveau accès réussi | Test utilisateur validé ; révocation d’anciens jetons non vérifiée |

Le contrôle final du **2 octobre à 13:36:51 +02:00** corrobore l’absence d’unité
en échec, audit enabled 1/lost 0/backlog 0, CUPS masked/inactive sans écoute et
File Browser healthy avec cap-drop ALL, no-new-privileges et unless-stopped.
La [capture finale et son analyse](mettre-en-oeuvre-verifier-remediations.md#releve-final-de-sante-2-octobre-2026-133651-0200)
constituent la preuve de santé, pas un scan de vulnérabilités.

## 3. Commandes et configurations utilisées

Les extraits ci-dessous documentent les opérations déjà réalisées. Ils ne
constituent pas un script à relancer globalement. La chronologie complète,
les sauvegardes et les commandes propres à chaque étape sont dans le journal.

### SSH — /etc/ssh/sshd_config.d/00-ais-hardening.conf

```text
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
KbdInteractiveAuthentication no
MACs -umac-64-etm@openssh.com,umac-64@openssh.com
```

Contrôles utilisés : `sudo sshd -t`, `sudo sshd -T -C ...`, nouvelle connexion
avec `ControlMaster=no`/`ControlPath=none`, essai password seul refusé, puis
`sudo -v` réussi. Ne pas confondre absence de sortie et capture d’un code de
retour : le dernier contrôle syntaxique n’affichait pas d’erreur, sans code
relevé séparément.

### Docker — options de déploiement et contrôles

```text
--restart=unless-stopped
--cap-drop=ALL
--security-opt=no-new-privileges:true
-p 8080:80
```

Montages bind conservés : config → `/config`, database → `/database`, documents
→ `/srv`. Le digest est fixé dans la commande de création. Contrôles utilisés :
`docker inspect`, `docker ps`, logs et lecture des champs UID/GID, capacités,
NoNewPrivs et Seccomp du processus File Browser dans `/proc`. Le test initial
était sur copie et port 8081 ; les essais du principal étaient sur 8080.

### Audit — /etc/audit/rules.d/50-ais.rules

```text
-a always,exit -F arch=b64 -F path=/etc/passwd -F perm=wa -k ais_identity
-a always,exit -F arch=b64 -F path=/etc/group -F perm=wa -k ais_identity
-a always,exit -F arch=b64 -F path=/etc/shadow -F perm=wa -k ais_identity
-a always,exit -F arch=b64 -F path=/etc/gshadow -F perm=wa -k ais_identity
-a always,exit -F arch=b64 -F path=/etc/sudoers -F perm=wa -k ais_sudo
-a always,exit -F arch=b64 -F dir=/etc/sudoers.d/ -F perm=wa -k ais_sudo
-a always,exit -F arch=b64 -F dir=/etc/ssh/ -F perm=wa -k ais_ssh
```

Fichier mode 640, chargement par `sudo augenrules --load`, vérifications par
`sudo auditctl -l`, `sudo auditctl -s` et `sudo ausearch -k ais_ssh -ts recent -i`.
Rotation manuelle : `sudo auditctl --signal rotate`. Configuration relevée :
max_log_file 8 Mio, num_logs 5, action ROTATE ; seuils espace 75/50 Mio,
actions SYSLOG/SUSPEND ; disque plein ou erreur : SUSPEND. La rétention n’est
pas exprimée en jours ; ces seuils nécessitent une surveillance de l’espace.

### CUPS — arrêt persistant retenu

```bash
sudo systemctl disable --now cups.service cups.socket cups.path
# Après réactivation constatée au reboot :
sudo systemctl mask --now cups.service cups.socket cups.path
```

Validation : `systemctl is-enabled`, `systemctl is-active` et
`sudo ss -lntup 'sport = :631'`, puis contrôle après reboot. Retour arrière
prévu : démasquer et restaurer l’activation initiale si l’impression devient
nécessaire. Aucun besoin d’impression n’a été identifié dans ce laboratoire.

### sysctl — deux fichiers locaux

`/etc/sysctl.d/99-ais-hardening.conf` :

```text
fs.protected_fifos = 2
kernel.kptr_restrict = 2
```

`/etc/sysctl.d/99-ais-network.conf` :

```text
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.*.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
net.ipv4.conf.*.send_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv6.conf.default.accept_redirects = 0
net.ipv6.conf.*.accept_redirects = 0
```

Application fichier par fichier avec `sysctl -p`, contrôles all/default/enp1s0/
docker0 puis reboot et tests fonctionnels. `net.ipv4.ip_forward=1` et
`rp_filter=2` conservés pour le réseau Docker observé ; ne pas désactiver
le forwarding pour satisfaire aveuglément un profil de scan.

## 4. Adaptations par rapport au plan initial

| Prévision / contrainte | Choix réalisé et justification |
| --- | --- |
| Migration OS avec risque d’espace insuffisant | Agrandir le disque avant poursuite ; migrations par versions LTS successives |
| Ordre documentaire des priorités | Migration File Browser/persistance/reprise puis OS ; historique conservé, essais sur copie et sauvegardes avant bascule |
| Durcir plusieurs options SSH | Appliquer le lot d’accès et de MAC vérifié ; transferts, MaxAuthTries, MaxSessions et journalisation complémentaire différés faute d’usage qualifié |
| Arrêter/désactiver CUPS | Passer au masquage après preuve de reprise au reboot ; justification par absence de besoin d’impression |
| Réduire les privilèges Docker et étudier read-only | CapDrop ALL et NoNewPrivs validés ; conserver les écritures nécessaires aux données, base et configuration |
| R07 initialement en investigation | Deux lots limités après lecture des interfaces et routes ; maintenir les paramètres utiles à Docker et aux diagnostics |
| R08 conditionnelle au besoin | Politique unless-stopped et données persistantes pour le service conservé ; reprise réellement observée |

## 5. Problèmes rencontrés et diagnostic

| Problème / observation | Diagnostic fondé sur les preuves | Résolution ou limite |
| --- | --- | --- |
| Faible espace avant migration | df et table de partitions : ext4 logique dans partition étendue MBR | Disque qcow2 agrandi, partitions et système de fichiers étendus ; racine environ 39 Gio |
| Retour arrière Docker lancé après une bascule healthy | Historique des commandes : stop/rename/start exécutés, sans panne applicative démontrée | Conteneur durci réactivé et inspecté ; nom hardening-failed ne prouve pas un échec |
| CUPS revient malgré disabled | Contrôle post-reboot : service/socket actifs et écoute 631 | mask --now puis reboot : masked/inactive et plus d’écoute |
| Message No rules pendant chargement audit | Liste finale des sept règles et événement ais_ssh retrouvé | Ne pas interpréter la sortie transitoire comme état final ; lost 0 |
| Inventaire effectué sur le poste hôte par erreur | Invite ubuntu-oliv différente de la VM | Refaire sur la VM à 13:32:17 ; inventaire hôte exclu des preuves VM |
| rg absent et recherches sudo sans résultat | Fichier snappy/dpkg.list au format tableau dpkg -l, pas au format Package: | grep plus large et lecture de l’en-tête : sudo core24 identifié |
| Alertes de version malgré paquets récents | Comparaison composant/chemin/version complète et correctifs éditeur | Exclusions ciblées ; ne pas classer globalement toutes les alertes comme faux positifs |
| Rapport attribue tous les résultats à 127.0.0.1 | Auth-SSH-Success gvm-audit et OS Ubuntu 26.04 cohérents ; cause de l’adresse non établie | Garder la réserve d’attribution, sans inventer un tunnel ni conclure au scan du poste hôte |

## 6. Actions non réalisées et risques résiduels

| Action ou risque | Pourquoi ce n’est pas clôturé | Suite retenue pour le dossier |
| --- | --- | --- |
| Maintenance de File Browser | Application annonce sa fin de maintenance ; version mise à jour ne rétablit pas un suivi futur | Recommander un remplacement dans une suite distincte ; aucune acceptation formelle du risque revendiquée |
| Dix HIGH Trivy dans la nouvelle image | Applicabilité pas entièrement vérifiée, pas d’exploitation démontrée ; JSON complet absent de cette feuille | Garder les dix associations comme risques à qualifier, identifier les chemins/composants et versions corrigées |
| Qualification de tous les résultats Greenbone | Faible QoD fréquente, multiples copies et correctifs Ubuntu rétroportés | Traiter par composant et chemin ; réserve sur adresse exportée et comparabilité des bases |
| Racine Docker read-only | Non incluse dans le lot testé ; chemins d’écriture applicatifs à qualifier | Différée, sans prétendre qu’elle est active |
| Révocation des anciennes sessions File Browser | Refus du mot de passe par défaut ne teste pas les jetons existants | Test spécifique en J5 si nécessaire à la clôture C13 |
| Restrictions SSH complémentaires | Utilité des transferts et impacts non établis | Qualifier l’usage avant modification ; ne pas changer le port comme preuve suffisante de sécurité |
| Autres sysctl | Forwarding/rp_filter, modules, diagnostics et BPF à contextualiser ; BPF non privilégié déjà restreint | Maintenir les décisions documentées ; bpf_jit_harden/log_martians encore à qualifier |
| Audit étendu et collecte externe | Périmètre actuel b64 ciblé ; pas de b32, pas de collecte distante ni de test de tous les chemins | Ne pas revendiquer couverture complète ni rétention automatique testée |
| Droits/CVE des paquets CUPS | Unités arrêtées, paquets conservés | Réduction de surface validée ; correction logicielle et permissions distinctes |

## 7. Comparer sans perdre les preuves initiales

Conserver les pièces sous des noms distincts, les dates, les filtres, la cible,
le profil, les versions des outils/bases et l’identité de l’image. Les
[sept journaux et rapports conservés](mettre-en-oeuvre-verifier-remediations.md#inventaire-complet-des-journaux-et-rapports)
et les captures du journal détaillé permettent de revenir aux observations.

| Source | Résultat disponible | Limite de comparaison |
| --- | --- | --- |
| Trivy ancienne/nouvelle image | Exports texte : 156 associations HIGH/CRITICAL sur deux cibles anciennes ; 10 HIGH et 0 CRITICAL sur le binaire de la nouvelle image | Ce n’est pas une preuve de 146 CVE corrigées ; bases/options et identité des pièces anciennes à rattacher |
| Lynis 11:56 puis 13:23 | Version 3.1.6 ; indice 65 → 67 ; écarts sysctl 15 → 9 ; auditd trouvé, CUPS non trouvé | Indice pas un pourcentage de sécurité ; profil et lancement exacts à conserver |
| Greenbone 12:11 puis 13:38 | Deux scans terminés ; mêmes identifiants tâche/cible et filtres ; 204 résultats sécurité + 44 Log chacun | Les deux sont post-migration OS ; pas une comparaison complète avec le J3 initial ; noms/sévérités/ports identiques, pas preuve d’identité de toutes les détections |

Le dernier [rapport Greenbone](../../assets/files/securisation-avancee-infrastructures/it-4/report-934f13f0-28fc-4f03-95e7-337d8f08a5db.xml)
couvre **13:38:59–13:44:33 +02:00**, après les derniers lots : 10 Critical,
73 High, 113 Medium et 8 Low. Les compteurs sont inchangés ; les contrôles
manuels restent nécessaires pour vérifier les remédiations de configuration.

Exemples d’investigation déjà aboutie : libcurl système 8.18.0 hors plage de
CVE-2023-38545 ; OpenSSH système 10.2p1 hors des plages de CVE-2025-26466 et
CVE-2024-39894 ; sudo core24 **1.9.15p5-3ubuntu5.24.04.2**, après la révision
Ubuntu corrigée `.24.04.1` pour CVE-2025-32462/32463. Voir les sources officielles
et les limites par copie dans la [qualification détaillée](mettre-en-oeuvre-verifier-remediations.md#qualification-ciblee-des-resultats-greenbone).

## 8. Préparer la vérification globale J5 — À réaliser

La clôture des interventions J4 ne remplace pas cette vérification globale.
Reprendre chaque constat C01–C13 du plan, maintenir C11 écarté comme panne
spontanée selon l’explication des arrêts volontaires, et renseigner le verdict
sans déduire une correction de la simple disparition d’une alerte.

| Groupe de constats | Vérification J5 prévue | Preuve attendue | Verdict J5 |
| --- | --- | --- | --- |
| C01–C03, C07 — Versions et maintenance hôte | Rattacher paquet actuel et correctif à chaque scénario initial ; vérifier cible du scan | Inventaire, avis éditeur, résultat pertinent et justification | À compléter |
| C04–C05 — SSH | Nouvelle connexion par clé, refus password/root selon protocole retenu, offre MAC effective | Sorties datées et session distincte ; usages des transferts qualifiés | À compléter |
| C06 — CUPS | Recontrôler unités et écoute ; distinguer paquet conservé et service arrêté | masked/inactive, aucune écoute 631 | À compléter |
| C08 — Traçabilité | Vérifier règles et événement ciblé, pertes et espace | auditctl, ausearch, rotation/rétention observées | À compléter |
| C09 — Paramètres noyau/réseau | Comparer valeurs et décisions justifiées avec le constat initial | sysctl effectif, fichiers persistants, fonctionnement Docker | À compléter |
| C10 — Conteneur | Contrôler le processus applicatif, droits et protections ; tester les opérations utiles | UID/capacités/NoNewPrivs, inspect, essais navigateur | À compléter |
| C12 — Image/application | Scan complet de l’image exacte et qualification ; décision sur maintenance | Digest, Trivy complet, analyse des dix HIGH et recommandation | À compléter |
| C13 — Identifiants | Refus des anciens identifiants, accès légitime ; traiter sessions si retenu | Test en session distincte, secret masqué, limites explicites | À compléter |
| Service global / R08 | Vérifier accès SSH, données, download/upload/delete et reprise si nouveau test nécessaire | Parcours horodaté et données persistantes | À compléter |

Pour chaque ligne, compléter : **corrigé et vérifié**, **partiellement corrigé**,
**non corrigé**, **non applicable avec justification** ou **non concluant**.
Un résultat non concluant doit préciser la preuve manquante. L’acceptation
éventuelle d’un risque est une décision à documenter, pas un état déduit du scan.

## 📦 Livrable et état final attendu

**Compte-rendu de durcissement J4 préparé**, comprenant actions, commandes,
configurations, validations, problèmes/diagnostics, écarts au plan, travaux
non réalisés et risques résiduels. Les preuves détaillées restent accessibles
sans recopier les secrets, bases applicatives ou clés SSH dans la synthèse.

En J5, compléter la matrice, dater les nouveaux contrôles et relier chaque
verdict à ses preuves pour constituer le compte-rendu de durcissement et de
vérification utilisé pour C2. **J5 et validation C2 : à compléter.**

- [Journal et captures des interventions](mettre-en-oeuvre-verifier-remediations.md)
- [Plan préparatoire](preparer-remediations.md)
- [Retour à l’itération 4](index.md)
- [Retour au module](../README.md)
