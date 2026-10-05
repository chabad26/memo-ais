# Finaliser le compte-rendu de durcissement et de vérification

**Itération 5 — Travail individuel — 5 octobre 2026**

## 🎯 Objectif

Conclure sur l’efficacité des mesures de sécurisation mises en œuvre depuis
l’audit initial. Ce document complète le compte-rendu commencé en J4 pour
présenter les changements, leurs vérifications, les diagnostics et l’état final.

**Bilan documentaire renseigné à partir des preuves J4 et du retour J5
d’Olivier.** Le 5 octobre, Olivier indique avoir refait les contrôles manuels,
Greenbone et Lynis, sans changement par rapport au vendredi 2 octobre.
Les sorties et rapports J5 ne sont pas encore joints : la stabilité est
**déclarée par l’apprenant**, pas reconstituée à partir de nouveaux exports.
Trivy n’a pas été relancé, l’image étant déclarée inchangée. Les risques
résiduels connus restent ouverts. La validation de C2 relève de l’évaluation
et n’est pas déduite de la rédaction de cette feuille.

## 1. Documents et démarche de vérification

- [Rapport d’audit et plan J3](../it-3/finaliser-rapport-plan-remediation.md) : constats initiaux, contexte, priorités et actions R01–R09.
- [Compte-rendu de durcissement J4](../it-4/finaliser-compte-rendu-durcissement.md) : interventions et configurations détaillées.
- [Journal J4 avec captures et rapports](../it-4/mettre-en-oeuvre-verifier-remediations.md) : preuves techniques, états intermédiaires et validations finales.
- [Vérifications après remédiation J5](verifier-etat-systeme-apres-remediation.md) : contrôles refaits déclarés, limites et matrice à étayer.

La démarche sépare **configuration effective**, **effet de sécurité** et
**maintien du fonctionnement**. Les contrôles et scans sont attribués à la VM
ou à l’image exacte ; un nom de fichier ou un compteur ne remplace pas cette
attribution. Les commandes ci-dessous sont des références des opérations
réalisées, pas un script de modification à relancer.

## 2. Traçabilité de chaque remédiation

### R01 — OS et moteurs : maintenance et versions anciennes

**Constats initiaux :** C07 et constats logiciels hôte C01–C03 selon les
composants et scénarios du rapport J3. Ubuntu 20.04.6 et moteurs anciens.

**Modification :** migration par étapes 22.04, 24.04 puis 26.04.1 ; disque
virtuel porté de 25 à 40 Gio et racine ext4 agrandie. Le journal conserve les
étapes de migration et de redimensionnement ; la seule collecte de versions
ne démontre pas la correction de chaque CVE.

**Vérification :** OS/noyau, `dpkg-query -W`, mises à jour, `systemctl --failed`,
SSH et File Browser. Versions finales J4 : OpenSSH 1:10.2p1-2ubuntu3.6,
docker.io 29.1.3-0ubuntu4.1 et containerd 2.2.2-0ubuntu1.1. Aucune unité en
échec au contrôle final ; service fonctionnel.

**Problème et diagnostic :** espace limité sur la racine ; `df`, `lsblk` et
table de partitions ont identifié une partition logique ext4 dans une
partition étendue MBR. Extension du disque, des partitions et du système de
fichiers avant poursuite.

**État final :** migration réalisée, fonctionnement vérifié en J4 et stabilité
déclarée en J5. Qualification de toutes les CVE hôte non achevée.

### R02 — SSH : accès et offre cryptographique

**Constats initiaux :** C04–C05 et volet logiciel C03. Mot de passe permis,
root prohibit-password et deux MAC UMAC-64 offerts.

**Configuration réalisée**, dans `/etc/ssh/sshd_config.d/00-ais-hardening.conf` :

```text
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
KbdInteractiveAuthentication no
MACs -umac-64-etm@openssh.com,umac-64@openssh.com
```

**Vérification :** `sshd -t`, `sshd -T -C` avec le contexte de connexion,
essai password seul refusé, nouvelle connexion par clé depuis le poste hôte
avec ControlMaster/ControlPath désactivés, puis `sudo -v` réussi (code 0).
Configuration effective et refus du password conservés en captures.

**Diagnostic / adaptation :** examen Include/Match et paramètres effectifs
avant changement ; activité de ssh.socket prise en compte. Les transferts,
MaxAuthTries, MaxSessions et réglages complémentaires n’ont pas été appliqués
sans qualification d’usage.

**État final :** premier lot vérifié, accès légitime maintenu ; stabilité J5
déclarée. Les restrictions complémentaires restent à qualifier.

### R03 — File Browser : image ancienne

**Constat initial :** C12, avec risque accru par les privilèges C10.
Version 2.15.0 et dépendances anciennes.

**Modification :** sauvegarde et test sur copie, puis bascule vers 2.63.23,
avec bind mounts persistants config/base/documents. Image fixée au digest
`sha256:a469ea076d4a1b4b1d86a41d130f2f536cd9da996a2b1fb39c0d7635f9d89b9a`.
La commande de déploiement exacte et les montages sont conservés dans le journal.

**Vérification :** version visible, `docker inspect`, logs, healthy et tests
de téléchargement, téléversement et suppression sur 8080. Trivy J4 indique
dix HIGH et zéro CRITICAL dans le binaire de la nouvelle image.

**Diagnostic / limite :** la migration a été testée sur une copie pour vérifier
la compatibilité des données. Les compteurs anciens/nouveaux ne démontrent pas
une correction CVE par CVE. L’application annonce sa fin de maintenance.

**État final :** image remplacée et service fonctionnel ; risque réduit,
maintenance non rétablie et dix HIGH à qualifier. Pas de Trivy J5 : image
déclarée inchangée. Une base de vulnérabilités actualisée pourrait néanmoins
produire de nouvelles associations ; aucun résultat Trivy J5 n’est revendiqué.

### R04 — Docker : privilèges du conteneur

**Constat initial :** C10, privilèges et écritures à réduire selon les besoins.

**Options appliquées** lors de la création du conteneur :

```text
--cap-drop=ALL
--security-opt=no-new-privileges:true
```

**Vérification :** processus File Browser UID/GID 1000 ; CapEff/CapBnd nuls,
NoNewPrivs 1, Seccomp 2. Inspection du processus applicatif, pas seulement de
`tini` PID 1. Essais sur copie/8081 puis sur principal/8080 ; opérations utiles
réussies, conteneur healthy.

**Problème et diagnostic :** retour arrière stop/rename/start exécuté après
une bascule healthy ; aucune panne applicative démontrée. Conteneur durci
réactivé et inspecté. Le nom hardening-failed n’a pas été interprété comme une
preuve d’échec.

**État final :** lot de protections actif et testé ; stabilité J5 déclarée.
Racine read-only non appliquée ; écritures nécessaires conservées.

### R05 — Audit : absence d’audit ciblé

**Constat initial :** C08, auditd absent.

**Modification :** auditd installé ; fichier mode 640
`/etc/audit/rules.d/50-ais.rules`, sept règles always,exit, arch=b64, perm=wa :
passwd/group/shadow/gshadow (ais_identity), sudoers/sudoers.d (ais_sudo),
répertoire SSH (ais_ssh). Règles intégrales dans le compte-rendu J4.

**Commandes et vérifications :** `augenrules --load`, `auditctl -l`,
`auditctl -s`, `ausearch -k ais_ssh -ts recent -i`. Création puis suppression
d’un fichier temporaire sous /etc/ssh retrouvées avant/après reboot.
Rotation par `auditctl --signal rotate`, archives présentes et lost 0.
Rétention relevée : 8 Mio, cinq journaux, ROTATE ; seuils espace SYSLOG/SUSPEND.

**Diagnostic :** message transitoire No rules confronté à la liste finale et
aux événements ; sept règles effectives. `failure 1` est un mode de traitement
des erreurs, pas un compteur de pertes.

**État final :** audit ciblé b64 vérifié et stabilité J5 déclarée. Autres
chemins non testés individuellement, rotation automatique au seuil non
provoquée, collecte externe non réalisée ; surveiller l’espace.

### R06 — CUPS : service sans besoin identifié

**Constat initial :** C06 ; service actif sur loopback, aucune imprimante.

**Modification et adaptation :** `systemctl disable --now` des unités
cups.service/cups.socket/cups.path, puis `systemctl mask --now` des trois
unités après reprise inattendue.

**Vérification :** `systemctl is-enabled`, `systemctl is-active`,
`ss -lntup 'sport = :631'`, puis contrôle post-reboot : masked/inactive et
aucune écoute. File Browser reste healthy.

**Problème et diagnostic :** disabled n’avait pas suffi ; contrôle post-reboot
montrait service/socket actifs et écoute 631. Le masquage a été vérifié après
un nouveau redémarrage.

**État final :** surface active retirée dans le laboratoire ; stabilité J5
déclarée. Paquets conservés : aucune purge ni correction de CVE par l’arrêt
seul, droits de configuration non revendiqués comme corrigés.

### R07 — sysctl : paramètres à contextualiser

**Constat initial :** C09 et écarts Lynis KRNL-6000.

**Modification :** dans `99-ais-hardening.conf`, protected_fifos et
kptr_restrict à 2 ; dans `99-ais-network.conf`, accept_redirects IPv4/IPv6 et
send_redirects IPv4 à 0 pour all/default/*. Application fichier par fichier
avec `sysctl -p` ; configurations complètes conservées dans J4.

**Vérification :** valeurs effectives, reboot et contrôles sur all/default/
enp1s0/docker0 ; SSH et opérations applicatives confirmés. Lynis : écarts
sysctl 15 → 9.

**Diagnostic / adaptation :** interfaces et routes montrent Docker en bridge
IPv4 ; ip_forward 1 et rp_filter 2 conservés. Modules, diagnostics et BPF ne
sont pas modifiés pour satisfaire aveuglément le profil.

**État final :** deux lots validés ; stabilité J5 déclarée. Certains paramètres
restent à qualifier et aucun test d’exploitation ciblé n’a été réalisé.

### R08 — Reprise et persistance du service

**Constat / besoin initial :** continuité à confirmer ; des arrêts étaient
volontaires, pas une panne spontanée C11 démontrée.

**Modification :** Docker activé, option `--restart=unless-stopped`, montages
persistants config/base/documents.

**Vérification :** `docker inspect` et service healthy après plusieurs reboots,
avec données et opérations accessibles selon les tests utilisateur.

**État final :** reprise corroborée sur les redémarrages observés ; aucune
nouvelle panne signalée en J5. Ce résultat n’est ni un test complet de PRA ni
un engagement de disponibilité.

### R09 — Identifiants administrateur par défaut

**Constat initial :** C13 ; connexion admin/admin acceptée selon le test
utilisateur.

**Modification :** mot de passe remplacé par Olivier dans l’application.
Le secret n’est pas conservé dans la documentation.

**Vérification :** ancien identifiant refusé en session privée selon Olivier,
capture Wrong credentials ; nouveau accès et opérations utiles confirmés.

**État final :** accès par ancien mot de passe supprimé selon les preuves J4,
stabilité globale déclarée en J5. Révocation des jetons/sessions déjà ouverts
non testée : ne pas l’assimiler au changement de mot de passe.

## 3. Bilan des risques et des écarts

| Catégorie | Conclusion | Limite / action restante |
| --- | --- | --- |
| Risques corrigés dans le périmètre vérifié | Accès avec anciens identifiants refusé ; password/root SSH interdits par configuration ; MAC ciblés retirés ; absence d’audit ciblé traitée | Preuves détaillées J4 ; sorties J5 à joindre, anciens jetons non vérifiés |
| Risques réduits mais présents | Image renouvelée, capacités supprimées et NoNewPrivs actif ; CUPS arrêté ; sysctl ciblés durcis ; OS migré | Vulnérabilités applicatives et maintenance File Browser, paquets CUPS conservés, couverture audit limitée |
| Mesure qui n’a pas fonctionné comme prévu | Désactivation initiale CUPS insuffisante après reboot | Masquage adapté et persistance vérifiée ; échec intermédiaire résolu |
| Incident de procédure | Retour arrière Docker exécuté malgré état healthy | Réactivation vérifiée ; ne pas conclure à une panne du lot de durcissement |
| Actions différées | read-only Docker, transferts SSH, autres sysctl, collecte distante, qualification exhaustive et révocation des sessions | Besoins/impacts non établis ou hors du lot ; qualification avant nouvelle modification |
| Risques structurels ouverts | Fin de maintenance File Browser et dix HIGH de l’export Trivy | Remplacement recommandé dans une suite distincte ; aucune acceptation formelle du risque attribuée à Olivier |

Les règles de sécurité appliquées ne remplacent pas les mises à jour des
composants vulnérables. Une alerte de scanner corrigée par rétroportage doit
être justifiée par la version complète, le chemin et une source éditeur.

## 4. Résultats des audits et investigations restantes

**Lynis J4 :** version 3.1.6, indice 65 → 67, écarts sysctl 15 → 9, auditd
trouvé et CUPS non trouvé. **Greenbone final J4 :** 10 Critical, 73 High,
113 Medium, 8 Low et 44 Log ; mêmes compteurs que le scan post-migration
précédent, pas une comparaison complète avec l’état initial J3.

**J5 :** contrôles manuels, Greenbone et Lynis refaits avec résultats inchangés
selon Olivier. Ne pas recopier les compteurs J4 comme nouvelle mesure exacte
sans les pièces J5. Aucun nouveau problème n’est signalé dans ce retour.

Investigations et pièces nécessaires :

- Joindre les exports/journaux J5 et le détail des contrôles manuels ; dater les tests et vérifier cible, filtres, authentification et profil.
- Expliquer l’adresse `127.0.0.1` des exports Greenbone, sans inventer un tunnel ni attribuer automatiquement le scan au poste hôte.
- Qualifier les alertes restantes par copie, chemin, version complète et scénario. Les exclusions libcurl/OpenSSH système et sudo core24 déjà motivées ne s’étendent pas aux autres copies.
- Conserver le digest actuel et actualiser Trivy si l’objectif devient la recherche de nouvelles CVE : les bases évoluent même à image constante.
- Compléter l’effet de sécurité ou les usages lorsque les tests actuels démontrent seulement une configuration/persistance.

## 5. Conclusion sur l’évolution du niveau de sécurité

Le système bénéficie de versions plus récentes, d’un accès administratif
restreint, de privilèges Docker réduits, d’une traçabilité ciblée et d’une
surface de services diminuée. Les contrôles J4 ont montré le maintien de
l’accès et des opérations applicatives ; les vérifications J5 déclarées ne
signalent pas de régression.

**Le niveau de sécurité a été amélioré dans le périmètre des mesures
vérifiées, sans suppression de tous les risques.** Le score Lynis et les
compteurs Greenbone ne quantifient pas cette amélioration globale. La fin de
maintenance de File Browser, les vulnérabilités non qualifiées et les limites
d’attribution/comparaison restent à traiter. La conclusion J5 doit être étayée
par les pièces nouvelles avant une validation indépendante complète.

## 📦 Livrable

Compte-rendu de durcissement et de vérification renseigné, avec traçabilité des
remédiations, résultats, diagnostics, état final et risques résiduels.
**Annexes J5 à joindre ; validation C2 à apprécier par la formatrice.**

- [Vérifier l’état du système après remédiation](verifier-etat-systeme-apres-remediation.md)
- [Compte-rendu J4](../it-4/finaliser-compte-rendu-durcissement.md)
- [Retour à l’itération 5](index.md)
- [Retour au module](../README.md)
