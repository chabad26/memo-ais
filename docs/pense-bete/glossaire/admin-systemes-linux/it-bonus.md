# Glossaire Linux — Bonus : AlpesNet Hardening Suite

## Sujet

Retrouver la logique de la suite Bash de préparation, durcissement, audit et sauvegarde Debian.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Durcissement | Réduction de la surface d’attaque selon les besoins réels. |
| Module | Bloc de tâches spécialisé, piloté par le script principal. |
| Dry-run | Simulation des actions, à distinguer d’une application réelle. |
| Audit | Contrôle produisant des constats PASS, FAIL ou WARN. |
| Checksum | Empreinte utilisée pour vérifier l’intégrité d’un fichier. |

## Gestes et commandes à retenir

Ces rappels ne constituent pas une preuve d’exécution.

| Besoin | Commande ou action |
| --- | --- |
| Préparer | Lire le README de la suite et adapter `config/alpesnet.conf`. |
| Préserver SSH | Vérifier `SSH_ALLOW_USERS`, le compte à conserver et les règles UFW avant application. |
| Simuler | Depuis le dossier de la suite : `sudo ./main.sh --all --dry-run --sshuser UTILISATEUR` ; remplacer le compte. |
| Relire | Examiner les rapports et les modules avant toute exécution réelle. |
| Valider | Contrôler accès, services et sauvegarde après application ; conserver les résultats réels. |

## Points de vigilance

Le projet source vise Debian 12. Ne pas lancer le durcissement sur la nouvelle VM sans vérifier sa version, sa configuration et les accès à conserver. Les commandes sont des rappels, pas des opérations exécutées ici.

## Docs associées

- [Projet bonus - AlpesNet Hardening Suite](../../../admin-systemes-linux/it-bonus/alpesnet-hardening-suite.md)
