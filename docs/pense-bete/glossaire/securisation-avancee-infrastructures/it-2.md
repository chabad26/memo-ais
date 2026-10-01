# Pense-bête — Sécurisation avancée : Corriger, durcir et vérifier

## Périmètre

Itération 2 de la progression prévisionnelle du module. Cette fiche prépare
les notions et les gestes ; les résultats seront ajoutés après les activités.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Correctif | Modification qui traite un défaut identifié. |
| Durcissement | Réduction de la surface d'attaque et des possibilités d'abus. |
| Mesure compensatoire | Protection limitant un risque en attendant son traitement complet. |
| Retour arrière | Procédure préparée pour revenir à un état maîtrisé si le changement échoue. |
| Non-régression | Vérification que les fonctions attendues restent disponibles. |
| Risque résiduel | Risque restant après les mesures appliquées. |
| Persistance | Maintien de la configuration après redémarrage. |
| Audit local | Observation réalisée depuis le système pour vérifier versions, paramètres, permissions, comptes et états de services. |
| Configuration effective | Valeur réellement appliquée après prise en compte des valeurs par défaut, inclusions et règles conditionnelles. |
| Activation par socket | Démarrage d'un service lorsqu'une connexion arrive sur un socket géré par systemd. |
| Identifiant de test Lynis | Repère unique d'un contrôle, à rechercher dans `lynis.log` pour comprendre ce qui a été testé. |
| Warning Lynis | Résultat qui demande généralement une attention forte, à confirmer dans le contexte. |
| Suggestion Lynis | Piste d'amélioration qui ne constitue pas automatiquement une vulnérabilité ni une priorité. |

## Manipulations faites

Contrôles locaux en lecture réalisés le **1er octobre 2026** sur la VM Ubuntu
20.04.6 :

- versions complètes relevées pour containerd, Docker, OpenSSH et CUPS ; les
  suffixes correctifs ESM attendus ne sont pas présents ;
- services Docker, containerd, SSH, CUPS et `cups.socket` actifs et activés ;
- SSH en écoute sur toutes les interfaces IPv4/IPv6, CUPS limité aux boucles locales ;
- configuration effective SSH relevée : mot de passe et clés autorisés,
  transfert TCP autorisé, GSSAPI et tunnel désactivés ;
- MAC faibles identifiés : `umac-64-etm@openssh.com` et `umac-64@openssh.com` ;
- compte `gvm-audit` sans sudo ni groupe supplémentaire, avec `.ssh` en `700`
  et `authorized_keys` en `600` ;
- CUPS actif, interface web locale, découverte désactivée et aucune imprimante.

L'état Ubuntu Pro, les droits des sockets Docker/containerd et l'usage de
BuildKit ne sont pas encore documentés. **Lynis 2.6.2 est maintenant installé.**
Un premier audit a produit un rapport de 77 580 octets et un journal de 533 312
octets. La commande `lynis show version` a ensuite remplacé le rapport par un
fichier de 694 octets. Un second audit a relevé **4 avertissements, 52
suggestions, 221 tests et un indice de durcissement de 57**. Ses nouvelles
empreintes restent à relever. Aucun changement de configuration de sécurité n'a
été appliqué par les commandes fournies.

## Gestes et commandes à retenir

- Commencer par la [reprise des constats du J1](../../../securisation-avancee-infrastructures/it-2/reprendre-constats-j1.md) sans modifier la cible.
- Relever les versions complètes avec `dpkg-query` et distinguer paquet installé, version candidate et correctif ESM accessible.
- Croiser `systemctl`, `ss` et la configuration effective : paquet installé, service actif et exposition réseau sont trois faits différents.
- Pour SSH, utiliser `sshd -T` et relever les blocs `Match` ; ne pas déduire l'algorithme faible du seul score Greenbone.
- Pour le compte d'audit, relever identité, groupes, droits et permissions sans afficher le contenu d'`authorized_keys`.
- Pour CUPS, examiner ensemble `cups.service`, `cups.socket`, l'écoute 631, la configuration et le besoin métier.
- Suivre l'activité [Installer et découvrir Lynis](../../../securisation-avancee-infrastructures/it-2/installer-decouvrir-lynis.md), vérifier l'installation avec `dpkg-query`, puis produire l'audit avec `sudo lynis audit system --quick --nocolors --auditor "AIS-lab"`.
- Copier immédiatement `lynis-report.dat` et `lynis.log` avec leurs empreintes avant toute autre commande `lynis` ; avec la version 2.6.2 observée, même `lynis show version` a réécrit le rapport.
- Remplacer la valeur d'exemple `IDENTIFIANT-LYNIS` par un véritable identifiant de test avant de rechercher celui-ci dans le journal.
- Prioriser avec l'exposition, l'impact, les protections et le rôle du serveur ; ne pas trier uniquement par type de message ou indice de durcissement.
- Décrire une modification par son fichier, sa valeur actuelle, sa valeur proposée, son contrôle de syntaxe, son impact et son retour arrière, sans l'appliquer pendant l'analyse.
- Dans la [vérification du système](../../../securisation-avancee-infrastructures/it-2/verifier-configuration-systeme.md), relier chaque commande au test Lynis d'origine, à la valeur observée et à une conclusion.
- Vérifier en priorité les permissions de `/srv/filebrowser`, les groupes privilégiés, auditd, les valeurs sysctl et les droits du socket Docker encore non documentés.
- Relier chaque changement à un constat et à un responsable.
- Préparer le retour arrière et garder un accès console pour les changements d'accès.
- Comparer la configuration avant/après et tester l'application.
- Refaire un contrôle de sécurité dans des conditions comparables.
- Documenter la persistance après redémarrage lorsque la modification le nécessite.

## Preuves attendues

Journal de changements, contrôles avant/après, test fonctionnel et risques restants.

## Docs associées

- [Reprendre les constats du J1](../../../securisation-avancee-infrastructures/it-2/reprendre-constats-j1.md)
- [Installer et découvrir Lynis](../../../securisation-avancee-infrastructures/it-2/installer-decouvrir-lynis.md)
- [Analyser et prioriser les résultats de Lynis](../../../securisation-avancee-infrastructures/it-2/analyser-prioriser-resultats-lynis.md)
- [Vérifier la configuration du système](../../../securisation-avancee-infrastructures/it-2/verifier-configuration-systeme.md)
- [Feuille de l'itération 2](../../../securisation-avancee-infrastructures/it-2/index.md)
- [Dossier de preuves](../../../securisation-avancee-infrastructures/dossier-preuves.md)
- [Vue d'ensemble du module](../../../securisation-avancee-infrastructures/README.md)

## Consolidation des audits

La [feuille de consolidation](../../../securisation-avancee-infrastructures/it-2/consolider-resultats-greenbone-lynis.md)
regroupe les preuves Greenbone, Lynis et manuelles dans 11 constats. Elle
reprend les propositions SSH, auditd et CUPS sans les appliquer. L’inventaire
Docker est cohérent ; File Browser est arrêté avec code 1 après l’arrêt
volontaire de la VM déclaré par l’utilisateur et corroboré par les journaux.
Le besoin de reprise automatique reste à préciser. Les valeurs confirmées ne prouvent pas toutes les
conditions d’exploitation ni la persistance après redémarrage.

## Préparer l’analyse de l’image au J3

La [nouvelle feuille](../../../securisation-avancee-infrastructures/it-2/limites-audit-preparer-analyse-conteneur.md)
distingue version applicative, tag, ID d’image et digest. Examiner l’image
référencée par le conteneur, même arrêté, avec des formats Docker ciblés.
Les audits de la VM ne prouvent pas le contenu ni la sécurité de l’image ;
les métadonnées et l’inventaire interne restent à compléter.

## Observation du conteneur

[Observer le conteneur sans y exécuter Lynis](../../../securisation-avancee-infrastructures/it-2/etendre-audit-conteneur.md) :
la formatrice limite Lynis à la VM Ubuntu. Conserver les métadonnées Docker et
les observations internes déjà obtenues, sans installer, copier ou lancer Lynis
dans File Browser. L’analyse de l’image exacte sera réalisée avec l’outil prévu,
notamment Trivy, en conservant les différences de périmètre.

## Évaluer les risques

Le [classement contextualisé](../../../securisation-avancee-infrastructures/it-3/evaluer-risques-definir-priorites.md)
conserve C01 à C11 et distingue priorité de correction, préparation et
investigation. CVSS est une information, pas un ordre automatique. Expliquer
accès requis, données, protections et risque de régression ; ne pas transformer
les arrêts volontaires en incidents ni supposer une exposition Internet.
