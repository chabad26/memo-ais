# Itération 4 - Reproduire et exploiter sur le second fournisseur

!!! info "Second fournisseur"
    Cette itération reprend le socle déjà automatisé et le rejoue sur
    **Infomaniak Public Cloud**. L'objectif n'est pas de refaire une découverte
    complète, mais de prouver que la méthode fonctionne hors du premier
    fournisseur.

## Objectif

Reproduire l'infrastructure DIST01b sur le second fournisseur, vérifier les
services déployés, relever les écarts avec OVHcloud et préparer les preuves
d'exploitation.

Cette itération sert à montrer une compétence transférable : mêmes besoins,
même logique OpenTofu et Ansible, mais contraintes fournisseur différentes.

## Feuille de l'itération

- [Reproduire et exploiter le second fournisseur](reproduire-exploiter-second-fournisseur.md)
- [Optimisation des coûts FinOps](optimisation-couts-finops.md)
- [Supervision cloud native](supervision-cloud-native.md)
- [Déclencher une alerte de supervision](declencher-alerte-supervision.md)
- [Déployer et automatiser Infomaniak](../it-2/deployer-automatiser-infomaniak.md)

## État final attendu

- le second fournisseur est identifié avec ses paramètres réels ;
- le code OpenTofu est adapté sans modifier le déploiement OVH ;
- l'inventaire Ansible pointe vers les VM Infomaniak ;
- les services principaux répondent sur les bonnes machines ;
- les écarts fournisseur sont documentés ;
- les preuves d'exploitation sont conservées sans exposer de secret ;
- les ressources inutilisées sont repérées et leur coût est estimé ;
- les principes de supervision cloud native sont compris ;
- une alerte de supervision est préparée et testable lors d'un prochain déploiement ;
- les ressources coûteuses sont arrêtées ou supprimées si l'exercice est clos.
