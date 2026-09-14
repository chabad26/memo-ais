# Glossaire Cloud & IAM — Itération 4 : second fournisseur et exploitation

## Sujet

Reproduire le socle sur Infomaniak, contrôler les coûts, superviser et préparer la restauration.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| Provider | Composant OpenTofu propre à l’API du fournisseur. |
| Idempotence | Une configuration déjà conforme ne nécessite pas de nouveau changement. |
| FinOps | Suivi des usages et des coûts pour justifier les ressources conservées. |
| Ressource orpheline | Ressource sans usage ou dépendance utile, à vérifier avant suppression. |
| Coût mensuel évité | Estimation du coût qui aurait continué si les ressources avaient été conservées. |
| Gnocchi / Aodh | Services OpenStack de métriques / alarmes, dont la disponibilité doit être vérifiée. |
| RTO | Objectif maximal de délai de rétablissement, à comparer au délai réellement mesuré. |
| RPO | Objectif maximal de perte de données dans le temps, à comparer au point effectivement restauré. |

## Gestes et commandes à retenir

Ces rappels ne constituent pas une preuve d’exécution.

| Besoin | Commande ou action |
| --- | --- |
| Prévisualiser | `tofu plan` dans le dossier du fournisseur concerné. |
| Inventorier en lecture seule | `openstack server list`, `openstack volume list`, `openstack floating ip list` avec le bon projet chargé. |
| Réutiliser Ansible | Adapter l’inventaire et conserver les rôles de configuration réutilisables. |
| Préparer une alerte | Définir métrique, seuil, durée, destinataire et réponse ; distinguer préparation et test reçu. |
| Mesurer une restauration | Noter début d’incident, retour fonctionnel et horodatage des données restaurées. |
| Auditer les coûts | Utiliser le script d’audit lié dans la fiche FinOps et examiner les dépendances. |

## Points de vigilance

Les fiches documentent la clôture du laboratoire : ne pas présenter les anciennes VM comme actives. Un RTO mesuré ne suffit pas à calculer un RPO sans sauvegarde horodatée. Préserver les dépendances du backend OpenTofu avant tout nettoyage.

## Docs associées

- [Déclencher une alerte de supervision](../../../integration-distribuee-cloud-iam/it-4/declencher-alerte-supervision.md)
- [Itération 4 - Reproduire et exploiter sur le second fournisseur](../../../integration-distribuee-cloud-iam/it-4/index.md)
- [Optimisation des coûts FinOps](../../../integration-distribuee-cloud-iam/it-4/optimisation-couts-finops.md)
- [Reproduire et exploiter le second fournisseur](../../../integration-distribuee-cloud-iam/it-4/reproduire-exploiter-second-fournisseur.md)
- [Supervision cloud native](../../../integration-distribuee-cloud-iam/it-4/supervision-cloud-native.md)
- [Tester une restauration cloud et mesurer RTO/RPO](../../../integration-distribuee-cloud-iam/it-4/tester-restauration-rto-rpo-cloud.md)
