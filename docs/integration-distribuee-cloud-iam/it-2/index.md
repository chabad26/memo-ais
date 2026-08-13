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

## Feuilles de l'itération

- [Déployer et automatiser OVH](deployer-automatiser-ovh.md)
- [Construire un réseau isolé OVH à la main](construire-reseau-isole-ovh.md)
- [Comprendre l'IaC et le cycle OpenTofu](comprendre-iac-cycle-opentofu.md)

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
