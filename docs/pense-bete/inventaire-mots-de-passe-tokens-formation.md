# Inventaire des mots de passe et tokens de formation

Date de l'inventaire : 2026-08-12.

Cet inventaire compte les secrets **documentés ou nécessaires** dans les modules de formation actuellement présents dans le dépôt. Il ne lit pas les fichiers `.env` locaux hors Git et ne remplace donc pas un audit de coffre-fort ou de poste.

## Méthode de comptage

- Un mot de passe propre à un compte est compté comme 1.
- Un mot de passe partagé par plusieurs comptes est compté comme 1 secret logique, avec la réutilisation signalée.
- Une passphrase, un secret de service, un secret de provisionneur ou une clé d'accès cloud est compté comme 1.
- Les clés privées de certificats sont signalées à part : ce sont des secrets cryptographiques, mais pas des mots de passe ou tokens.
- Les mots de passe déjà écrits en clair dans un exemple de laboratoire doivent être changés s'ils ont été réutilisés ailleurs.

## Synthèse

| Domaine de formation | Mots de passe / secrets / tokens | Tokens de challenge | Remarque |
| --- | ---: | ---: | --- |
| Intro AIS, RGPD, système d'information | 0 | 0 | Notions théoriques seulement. |
| Administration systèmes Linux | 4 | 0 | Comptes Linux, Samba local, CTF final Linux. |
| Administration Windows | 11 | 0 | AD DS, utilisateurs, BitLocker, LAPS, import CSV. |
| Administration réseaux | 1 | 0 | Mot de passe d'équipement utilisé par le script Netmiko. |
| Réseaux sécurisés | 5 | 2 | pfSense/Spark/CTF réseau ; les flags sont séparés. |
| Administration systèmes - Virtualisation | 2 | 0 | Mots de passe administrateur de VM/lab. |
| Intégration distribuée on-premise | 22 | 0 | Docker, LDAP, LAM, Samba, messagerie, Borg, Step CA. |
| Intégration distribuée cloud IAM | 1 | 0 | Paire d'accès cloud à ne jamais publier. |
| **Total minimum** | **46** | **2** | Hors `.env` locaux non versionnés. |

Total opérationnel à suivre : **46 éléments sensibles minimum**, plus **2 flags/tokens de challenge** si les exercices CTF sont inclus dans le périmètre.

## Détail par module

### Administration systèmes Linux

| Module | Compte |
| --- | ---: |
| Itération 1 - comptes `alice.martin` et `bob.dupont` | 2 |
| Itération 4 - mot de passe Samba de test partagé par Alice et Bob | 1 |
| Itération 6 - mot de passe caché du scénario CTF final | 1 |
| **Sous-total** | **4** |

### Administration Windows

| Module | Compte |
| --- | ---: |
| Itération 1 - administrateur local du serveur | 1 |
| Itération 1 - mot de passe DSRM | 1 |
| Itération 1 - utilisateur de test AD | 1 |
| Itération 2 - mot de passe temporaire partagé des utilisateurs RH/IT | 1 |
| Itération 2 - mot de passe temporaire partagé des comptes admin tier | 1 |
| Itération 2 - réinitialisation de `user.rh1` | 1 |
| Itération 2 - récupération BitLocker de `POSTE-01` | 1 |
| Itération 2 - secret LAPS de `POSTE-01` | 1 |
| Itération 4 - import CSV, 3 mots de passe temporaires générés | 3 |
| **Sous-total** | **11** |

Le mot de passe du compte administrateur de domaine est aussi utilisé pour certaines opérations, mais il est compté comme secret existant plutôt que comme nouveau secret de module.

### Administration réseaux

| Module | Compte |
| --- | ---: |
| Itération 5 - `NET_PASSWORD` pour sauvegarde Netmiko | 1 |
| **Sous-total** | **1** |

### Réseaux sécurisés

| Module | Compte |
| --- | ---: |
| Itération 2 - mot de passe administrateur pfSense à changer | 1 |
| Itération 5 - fichier secret Spark | 1 |
| Itération 6 - mot de passe faible du compte visiteur | 1 |
| Itération 6 - mot de passe du compte admin trouvé par wordlist | 1 |
| Itération 6 - mot de passe VPN du scénario | 1 |
| Itération 6 - flags CTF | 2 tokens |
| **Sous-total mots de passe/secrets** | **5** |

### Administration systèmes - Virtualisation

| Module | Compte |
| --- | ---: |
| Itération 2 - mot de passe administrateur robuste de VM | 1 |
| Itération 3 - mot de passe défini pendant l'installation Debian/Proxmox | 1 |
| **Sous-total** | **2** |

### Intégration distribuée on-premise

| Module | Compte |
| --- | ---: |
| Itération 1 - MariaDB root de démonstration | 1 |
| Itération 1 - MariaDB root du Compose WordPress | 1 |
| Itération 1 - mot de passe de l'utilisateur base WordPress | 1 |
| Itération 2 - mots de passe administrateur OpenLDAP générés au bootstrap | 2 |
| Itération 2 - mot de passe du profil LAM | 1 |
| Itération 2 - 6 mots de passe utilisateurs LDAP de laboratoire | 6 |
| Itération 2 - mot de passe temporaire `test.arrivee` | 1 |
| Itération 3 - `DOMAINPASS` Samba AD de laboratoire | 1 |
| Itération 3 - `LDAP_ADMIN_PASSWORD` utilisé par Samba/NSS LDAP | 1 |
| Itération 3 - mot de passe de test utilisateur Samba/LDAP | 1 |
| Itération 4 - `LDAP_BIND_PASSWORD` messagerie | 1 |
| Itération 4 - `ROUNDCUBE_DB_PASSWORD` | 1 |
| Itération 4 - `MARIADB_ROOT_PASSWORD` messagerie | 1 |
| Itération 5 - `BORG_PASSPHRASE` | 1 |
| Itération 6 - mot de passe de la clé intermédiaire Step CA | 1 |
| Itération 6 - secret du provisionneur Step CA | 1 |
| Itération 7 - supervision | 0 |
| Itération 8 - crise LDAP/PCA/PRA | 0 |
| **Sous-total** | **22** |

### Intégration distribuée cloud IAM

| Module | Compte |
| --- | ---: |
| Itération 1 - paire d'accès cloud, Access Key ID + Secret Access Key | 1 |
| **Sous-total** | **1** |

## Points d'attention

- Plusieurs exemples de laboratoire contiennent une valeur en clair ou très faible. Ces valeurs doivent rester des exemples et être remplacées si elles ont servi dans un environnement réel.
- Les captures BitLocker, LAPS, LDAP, Step CA et cloud doivent masquer les secrets complets.
- Les secrets réutilisés pour plusieurs comptes facilitent le TP, mais ils doivent être renouvelés ou séparés pour un dossier d'exploitation réaliste.
- Les clés privées de certificats, les fichiers `~/.step/secrets/`, `password.txt`, `.env`, keystores et fichiers de clés cloud ne doivent jamais être ajoutés au dépôt.
