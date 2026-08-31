# Itération 2 - Déployer et automatiser sur OVH

!!! info "J3-J5 matin"
    Cette itération correspond au premier fournisseur cloud du module. Le
    fournisseur retenu pour le prototype est **OVHcloud**.

## Objectif

Cette itération transforme le plan de migration en premier socle technique
déployable.

Le but n'est pas encore de migrer toute l'infrastructure DIST-01a. Il s'agit de
créer une première cible OVHcloud, de la rendre reproductible avec
**OpenTofu**, puis de configurer la machine avec **Ansible**.

## Fil conducteur

| Étape | Travail attendu |
| --- | --- |
| 1 | Créer ou vérifier le projet Public Cloud OVHcloud. |
| 2 | Préparer les identifiants API sans les exposer dans Git. |
| 3 | Déployer une première instance OVHcloud. |
| 4 | Automatiser l'infrastructure avec OpenTofu. |
| 5 | Générer ou maintenir un inventaire Ansible. |
| 6 | Configurer le socle système avec Ansible. |
| 7 | Valider l'accès, le pare-feu, les mises à jour et les preuves. |

## Avancement réel

| Date | Élément | Statut | Preuve à joindre |
| --- | --- | --- | --- |
| 31/08/2026 | Première instance OVHcloud `d2-8-2026_08_31-09-17` | Réalisé | Capture OVHcloud `ovh-instance-active-ssh-ok-2026-08-31.png`. |
| 31/08/2026 | Connexion SSH depuis le poste d'administration | Validée | Accès `ubuntu@135.125.57.xxx`; capture du prompt SSH à joindre si possible. |
| 31/08/2026 | Paramètres relevés | Documenté | `GRA9`, `d2-8`, Ubuntu 26.04 - UEFI, IP privée `10.42.10.123`. |
| À compléter | OpenTofu | À faire ou à documenter | `tofu fmt`, `tofu init`, `tofu validate`, `tofu plan`. |
| 31/08/2026 | Ansible | Réalisé | Playbook : `ok=5`, `changed=3`, `failed=0`; contrôles hostname, UFW et Git dans `ansible-base-system-ok-5-changed-3-2026-08-31.png`. |

## Feuilles de l'itération

- [Déployer et automatiser OVH](deployer-automatiser-ovh.md)
- [Construire un réseau isolé OVH à la main](construire-reseau-isole-ovh.md)
- [Comprendre l'IaC et le cycle OpenTofu](comprendre-iac-cycle-opentofu.md)
- [Utiliser le stockage objet OVH comme backend OpenTofu](stockage-objet-backend-opentofu.md)
- [Automatiser avec Ansible](automatiser-avec-ansible.md)
- [Playbook et versionnement](playbook-versionnement-service.md)
- [DNS et répartition de charge cloud](dns-repartition-charge-cloud.md)

## État final attendu

À la fin de l'itération :

- le projet OVHcloud est prêt ou ses blocages sont documentés ;
- l'instance cible est décrite dans du code OpenTofu ;
- les secrets OVH ne sont pas commites ;
- l'accès SSH est maîtrisé ;
- Ansible peut joindre la machine ;
- les mises à jour, comptes d'administration et règles réseau de base sont
  documentés ;
- les preuves techniques sont conservées sans exposer de secret.
