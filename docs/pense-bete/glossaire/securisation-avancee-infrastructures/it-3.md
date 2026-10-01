# Pense-bête — Sécurisation avancée : analyser l’image du conteneur

## Périmètre

Itération 3 du module. Greenbone et Lynis ont analysé la VM selon leurs
périmètres. Cette étape identifie les informations manquantes sur l’image File
Browser et prépare son analyse avec Trivy.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Image | Ensemble immuable de couches utilisé pour créer un conteneur. |
| Conteneur | Instance d’exécution d’une image, avec sa configuration et sa couche modifiable. |
| Tag | Référence lisible pouvant être déplacée vers une autre image. |
| ImageID | Identifiant local du contenu de l’image Docker. |
| RepoDigest | Digest du manifeste publié dans un registre. |
| SBOM | Inventaire structuré des composants logiciels et dépendances. |
| Scanner d’image | Outil rapprochant les composants reconnus d’une base de vulnérabilités et d’autres contrôles activés. |
| Applicabilité | Vérification qu’un résultat concerne réellement le composant, la version et les conditions du système étudié. |

## Manipulations faites

L’image `filebrowser/filebrowser:v2.15.0` est identifiée par son ImageID et son
RepoDigest. Alpine 3.13.4, l’exécution root, le montage RW et plusieurs
paramètres Docker sont observés. Trivy 0.74.0 est installé sur la machine
d’audit. L’image exacte a été exportée et l’empreinte SHA-256 de l’archive a été
conservée sur les deux machines. Le scan Trivy a réussi avec un code retour nul
et produit un rapport JSON empreinté. Trivy a reconnu Alpine 3.13.4, 20 paquets
système et 53 composants dans le binaire Go. La distribution est signalée en
fin de support. Le rapport contient 294 associations composant–vulnérabilité,
dont 13 critiques. Sur cinq résultats vérifiés, quatre sont non pertinents dans
la configuration observée et un reste à vérifier. Trois exports contrôlés
séparent les résultats `CRITICAL`, `HIGH` et leur ensemble. La consolidation
retient un constat unique sur l’obsolescence de l’image.

## Gestes à retenir

- Distinguer hôte, conteneur, image, application et données montées.
- Cibler l’image exacte référencée par le conteneur, pas seulement son tag.
- Conserver version de Trivy, date de base, commande, erreurs et rapport.
- Relier chaque CVE à un composant et une version réellement détectés.
- Consulter l’avis éditeur avant de confirmer l’applicabilité.
- Conserver les composants inconnus et limites de couverture dans la conclusion.
- Ne pas exécuter Lynis dans le conteneur.

## Preuves attendues

Inventaire reproductible de l’image, rapport daté et empreinté, résultats
qualifiés et limites explicites.

## Docs associées

- [Feuille de l’itération 3](../../../securisation-avancee-infrastructures/it-3/index.md)
- [Identifier ce qui manque dans l’audit](../../../securisation-avancee-infrastructures/it-3/identifier-manques-audit.md)
- [Analyser l’image avec Trivy](../../../securisation-avancee-infrastructures/it-3/analyser-image-trivy.md)
- [Analyser et vérifier les résultats Trivy](../../../securisation-avancee-infrastructures/it-3/analyser-verifier-resultats-trivy.md)
- [Consolider les trois sources d’audit](../../../securisation-avancee-infrastructures/it-3/consolider-trois-sources-audit.md)
- [Dossier de preuves](../../../securisation-avancee-infrastructures/dossier-preuves.md)
- [Vue d’ensemble du module](../../../securisation-avancee-infrastructures/README.md)

## Rapport final et remédiation

Le [rapport et plan](../../../securisation-avancee-infrastructures/it-3/finaliser-rapport-plan-remediation.md)
regroupe les actions en huit lots. C12 complète le classement initial avec
la migration de l’image hors support. Distinguer preuves, investigations,
non-intervention justifiée et validations attendues ; aucune mesure appliquée
n’est déduite de la rédaction du plan.
