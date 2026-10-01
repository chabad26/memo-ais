# Installer et découvrir Lynis

**Durée indicative : 1 h**

## Objectif

Installer Lynis sur la VM Ubuntu 20.04, réaliser un audit local et identifier
les informations affichées et conservées par l'outil.

**Périmètre imposé : Lynis est installé et exécuté sur la VM cible uniquement.**
Il n’est ni installé ni exécuté dans le conteneur File Browser.

**Statut au 1er octobre 2026 : activité réalisée en grande partie.** Lynis 2.6.2
est installé et deux audits ont été exécutés. La consultation de `lynis --help`
n'est pas encore attestée. Les empreintes du second rapport et de son journal
restent également à relever.

## Environnement

| Élément | Valeur observée |
| --- | --- |
| VM cible | `oliv-Standard-PC-Q35-ICH9-2009` |
| Système | Ubuntu 20.04.6 LTS |
| Noyau relevé avant l'audit | 5.15.0-139-generic |
| Lynis | 2.6.2 |
| Privilèges | `sudo` nécessaire pour l'audit complet et la lecture des résultats |

## Étape 1 — Installer Lynis

Confirmer d'abord son absence et la version disponible dans les dépôts
configurés :

```bash
command -v lynis || echo "Lynis absent du PATH"
dpkg-query -W -f='${binary:Package}\t${Version}\t${db:Status-Abbrev}\n' \
  lynis 2>&1
apt-cache policy lynis
```

Installer ensuite le paquet :

```bash
sudo apt update
sudo apt install --no-install-recommends lynis
```

Vérifier le résultat sans lancer Lynis :

```bash
command -v lynis
dpkg-query -W -f='${binary:Package}\t${Version}\t${db:Status-Abbrev}\n' \
  lynis
```

La version 2.6.2 a été observée sur la VM. La sortie d'installation APT et la
version exacte du paquet restent à ajouter si elles ont été conservées.

## Étape 2 — Consulter l'aide et la version

L'exercice demande :

```bash
lynis --help
lynis show version
```

L'aide présente les commandes, les modes d'audit et les options. Sa consultation
reste à documenter par quelques options utiles, par exemple `audit system`,
`--quick`, `--nocolors` et `--auditor`.

!!! warning "Consulter la version avant l'audit"
    Avec Lynis 2.6.2 sur cette VM, `sudo lynis show version` a réécrit
    `/var/log/lynis-report.dat`. Exécuter cette commande avant le scan, puis
    utiliser `dpkg-query` ou le champ `lynis_version` du rapport après le scan.

## Étape 3 — Lancer l'audit local

La commande minimale demandée est :

```bash
sudo lynis audit system
```

La commande réellement utilisée pour le second audit est :

```bash
sudo lynis audit system --quick --nocolors --auditor "AIS-lab"
```

`--quick` supprime les pauses interactives, `--nocolors` facilite la conservation
du texte et `--auditor` inscrit l'identifiant `AIS-lab` dans le résultat. Ces
options ne changent pas le périmètre `system` demandé.

## Étape 4 — Observer les catégories contrôlées

Le second audit a notamment parcouru les catégories suivantes :

- démarrage, services et GRUB ;
- noyau, mémoire et processus ;
- comptes, groupes, PAM et politiques de mots de passe ;
- systèmes de fichiers, stockage et permissions ;
- réseau, DNS, ports et pare-feu ;
- CUPS, SSH et services applicatifs ;
- journaux, bannières, comptabilité et synchronisation du temps ;
- cryptographie, conteneurs Docker et AppArmor ;
- intégrité des fichiers et durcissement du noyau.

Les états `OK`, `WARNING`, `ATTENTION`, `SUGGESTION`, `NON TROUVÉ` ou
`DIFFERENT` décrivent le résultat d'un test Lynis. Ils ne constituent pas à eux
seuls une preuve de vulnérabilité ni une priorité de correction.

## Étape 5 — Lire les résultats produits

À la fin du second audit, Lynis affiche :

| Élément | Résultat observé |
| --- | --- |
| Version Lynis | 2.6.2 ; l'outil annonce une version 3.1.6 disponible |
| Système reconnu | Ubuntu 20.04, noyau 5.15.0, architecture x86_64 |
| Auditeur | `AIS-lab` |
| Tests effectués | 221 |
| Indice de durcissement | 57 |
| Avertissements | 4 |
| Suggestions | 52 |
| Pare-feu | Actif, avec des règles inutilisées signalées |
| Journalisation | journald et rsyslog détectés ; auditd non détecté |
| Conteneurs | Docker actif ; quantité de conteneurs indéterminée par Lynis |
| Cadre de sécurité | AppArmor actif |
| Scanner de logiciels malveillants | Non détecté |

Les quatre avertissements affichés concernent :

- l'ancienneté de Lynis (`LYNIS`) ;
- le mode mono-utilisateur sans mot de passe (`AUTH-9308`) ;
- l'absence de réponse du résolveur `127.0.0.53` (`NETW-2704`) ;
- l'absence de deux serveurs DNS réactifs (`NETW-2705`).

Ces résultats devront être qualifiés avec le contexte et des vérifications
locales dans l'activité suivante.

## Étape 6 — Consulter le journal et le rapport

```bash
sudo less /var/log/lynis.log
sudo less /var/log/lynis-report.dat
```

| Source | Contenu utile |
| --- | --- |
| Sortie du terminal | Progression par catégorie, états synthétiques et résumé final |
| `/var/log/lynis.log` | Détails techniques des tests, commandes, valeurs et identifiants |
| `/var/log/lynis-report.dat` | Données structurées destinées à l'exploitation et à la comparaison |

Rechercher quelques éléments sans modifier les fichiers :

```bash
sudo grep -E '^(warning|suggestion)\[\]=' \
  /var/log/lynis-report.dat
sudo grep -E \
  '^(hardening_index|lynis_version|os|os_name|os_version|linux_kernel_version|scan_mode|auditor)=' \
  /var/log/lynis-report.dat
```

## Incident de conservation observé

| Heure | Fichier | Taille | SHA-256 | Interprétation |
| --- | --- | ---: | --- | --- |
| 10:00:56 | `lynis-report.dat` | 77 580 octets | `a4fc524ad37dc993838e609e78f7315a52c3c5a7450a16d848f0e794538f1e41` | Premier rapport complet, non disponible localement sauf copie antérieure |
| 10:00:56 | `lynis.log` | 533 312 octets | `30ba958ab5a17b8914d99582b25097b135ef4f02011474515193931ba71ee401` | Journal du premier audit encore inchangé à 10:01:09 |
| 10:01:09 | `lynis-report.dat` | 694 octets | `7ec9c2c689019b082076557c75fd9fa5e8d7afd371cbf09f116382ea2dbe4545` | Fichier réécrit par `lynis show version`, insuffisant pour analyser l'audit |

Le rapport de 694 octets ne contenait plus que la suggestion générique sur
l'ancienneté de Lynis. Le second audit a restauré un jeu complet de résultats,
mais ses métadonnées et empreintes ne sont pas encore fournies.

## Étape 7 — Conserver les preuves du second audit

Ne plus exécuter de commande Lynis avant cette copie :

```bash
date -Is
sudo stat -c '%n | %s octets | %y | %U:%G | %a' \
  /var/log/lynis-report.dat /var/log/lynis.log
sudo sha256sum /var/log/lynis-report.dat /var/log/lynis.log

LYNIS_PROOF_DIR="$HOME/preuves-lynis-20261001"
install -d -m 700 "$LYNIS_PROOF_DIR"
sudo install -m 600 -o "$USER" -g "$(id -gn)" \
  /var/log/lynis-report.dat "$LYNIS_PROOF_DIR/lynis-report-second-audit.dat"
sudo install -m 600 -o "$USER" -g "$(id -gn)" \
  /var/log/lynis.log "$LYNIS_PROOF_DIR/lynis-second-audit.log"
sha256sum "$LYNIS_PROOF_DIR"/*
```

Le rapport et le journal peuvent contenir des comptes, chemins et informations
internes. Les conserver dans le dossier privé et ne publier que les extraits
nécessaires et anonymisés.

## Comparaison demandée

La sortie du terminal permet de suivre l'audit et de repérer immédiatement les
résultats majeurs. Le journal explique plus finement ce que chaque test a fait.
Le rapport structuré facilite l'extraction des avertissements, suggestions,
versions et identifiants. L'analyse doit donc partir du rapport, puis revenir au
journal et à la configuration locale pour confirmer chaque constat.

## Ressources

- [Documentation Lynis](https://cisofy.com/documentation/lynis/)
- [Dépôt Lynis](https://github.com/CISOfy/lynis)

- [Activité précédente — Reprendre les constats du J1](reprendre-constats-j1.md)
- [Activité suivante — Analyser et prioriser les résultats de Lynis](analyser-prioriser-resultats-lynis.md)
- [Retour à l'itération 2](index.md)
