# Supervision cloud native

!!! info "Fiche de compréhension"
    Cette feuille explique les principes de la supervision cloud native. Dans
    l'état actuel du module, les VM et IP d'exercice ont été détruites après
    validation : les manipulations ci-dessous sont donc des commandes et
    contrôles à retenir pour un prochain déploiement, pas une preuve de
    supervision active.

## Objectif

Comprendre les principes de la supervision cloud native.

La supervision cloud native s'appuie sur des services managés de métriques,
de logs, de tableaux de bord et d'alertes. Elle permet de suivre l'état des
ressources cloud sans installer toute la pile de supervision soi-même.

Dans le module, cela complète la supervision applicative déjà vue avec Kibana :
Kibana aide à exploiter les logs et services du socle DIST01b, tandis que la
supervision cloud native aide à surveiller les ressources du fournisseur :
VM, réseau, stockage, quotas et coût.

## Ce que tu vas faire, et pourquoi

| Action | Pourquoi |
| --- | --- |
| Identifier les métriques cloud utiles. | Savoir quoi surveiller avant de créer une alerte. |
| Distinguer métriques, logs et alertes. | Ne pas mélanger mesure, trace et réaction. |
| Définir quelques seuils simples. | Détecter une anomalie avant l'incident. |
| Relier supervision et FinOps. | Repérer les ressources qui consomment ou coûtent sans valeur métier. |
| Préparer les preuves attendues. | Pouvoir montrer au jury une démarche d'exploitation, même si les VM ont été détruites. |

## Notions clés

| Notion | Définition courte | Exemple |
| --- | --- | --- |
| Métrique | Valeur numérique mesurée dans le temps. | CPU, RAM, trafic réseau, disque utilisé. |
| Log | Événement textuel ou structuré produit par un service. | Connexion SSH, erreur HTTP, redémarrage de conteneur. |
| Dashboard | Vue graphique regroupant plusieurs métriques. | État des VM, trafic réseau, saturation disque. |
| Alerte | Notification déclenchée par une condition. | CPU supérieur à 80 % pendant 10 minutes. |
| Seuil | Limite à partir de laquelle une situation devient anormale. | Disque utilisé supérieur à 85 %. |
| FinOps | Suivi technique et financier de l'usage cloud. | Supprimer une VM oubliée ou un volume détaché. |

## Métriques à surveiller

| Ressource | Métriques utiles | Pourquoi |
| --- | --- | --- |
| VM principale | CPU, RAM, disque, trafic entrant et sortant | Détecter surcharge, saturation ou exposition inhabituelle. |
| VM fichiers | disque, I/O, trafic SMB/HTTP | Surveiller l'espace et les accès aux services de fichiers. |
| VM mail | CPU, disque, trafic SMTP/IMAP/HTTPS | Détecter blocage mail, file d'attente ou abus réseau. |
| Réseau | débit, paquets, erreurs, IP publiques utilisées | Vérifier l'exposition et les flux entre services. |
| Volumes | capacité utilisée, volumes détachés | Éviter panne disque et coûts cachés. |
| Coûts | ressources actives, durée d'exécution, stockage restant | Détecter les ressources oubliées après exercice. |

## Exemples de seuils

| Contrôle | Seuil indicatif | Réaction attendue |
| --- | --- | --- |
| CPU VM | supérieur à 80 % pendant 10 minutes | Vérifier processus, conteneurs et charge applicative. |
| Disque | supérieur à 85 % | Nettoyer logs, vérifier volumes, augmenter capacité si besoin. |
| Trafic entrant | pic inhabituel | Vérifier firewall, logs web, origine des connexions. |
| VM active hors exercice | ressource encore présente après clôture | Confirmer l'utilité ou supprimer pour éviter la facturation. |
| Volume détaché | volume `available` non documenté | Supprimer après vérification des sauvegardes et dépendances. |

Ces seuils sont des repères pédagogiques. En production, ils doivent être
adaptés au comportement normal du service.

## Application à notre contexte

| Sujet | État réel | Preuve possible |
| --- | --- | --- |
| OVHcloud | Les ressources d'exercice ont été détruites après validation. | Capture console ou sortie CLI montrant l'absence de VM/volume/IP résiduel. |
| Infomaniak | Les ressources d'exercice ont été détruites après validation. | Capture console ou sortie CLI montrant l'absence de VM/volume/IP résiduel. |
| Services DIST01b | Les preuves de fonctionnement existent dans les fiches de déploiement. | Captures LAM, WordPress, Roundcube, Kibana, Docker et Ansible. |
| Supervision cloud native | Non activée sur une infrastructure encore en ligne. | Fiche de méthode, seuils proposés et contrôles à rejouer au prochain déploiement. |
| FinOps | Clôture déjà faite par destruction des ressources. | Fiche FinOps et script d'audit de ressources résiduelles. |

## Commandes et contrôles à retenir

Pour un fournisseur OpenStack comme OVHcloud ou Infomaniak :

```bash
export OS_CLOUD=PROFIL_OPENSTACK

openstack cloud list
openstack server list
openstack volume list
openstack floating ip list
openstack security group list
openstack quota show
```

Pour vérifier les ressources résiduelles après destruction :

```bash
docs/assets/scripts/integration-distribuee-cloud-iam/it-4/audit-ressources-orphelines.sh \
  openstack PROFIL_OPENSTACK
```

Pour conserver une preuve datée :

```bash
mkdir -p preuves/supervision
docs/assets/scripts/integration-distribuee-cloud-iam/it-4/audit-ressources-orphelines.sh \
  openstack PCP-LDG88UE-dc3-a \
  | tee preuves/supervision/audit-cloud-native-infomaniak-AAAA-MM-JJ.txt
```

## Supervision et FinOps

La supervision cloud native ne sert pas seulement à détecter les pannes. Elle
sert aussi à éviter les coûts inutiles :

- une VM sans trafic peut être un oubli ;
- un volume détaché peut continuer à être facturé ;
- une IP publique non utilisée peut signaler une ressource abandonnée ;
- un snapshot ancien peut coûter du stockage sans utilité réelle ;
- une hausse brutale de trafic peut créer un coût ou révéler un abus.

Le lien avec le FinOps est donc direct : surveiller, c'est aussi vérifier que
chaque ressource active a encore une raison d'exister.

## Preuves à conserver

| Preuve | Contenu attendu |
| --- | --- |
| Capture du dashboard cloud | Métriques visibles : CPU, réseau, disque ou état des instances. |
| Capture d'une règle d'alerte | Seuil, ressource concernée, canal de notification. |
| Sortie CLI | Liste des VM, volumes, IP et quotas. |
| Décision FinOps | Ressource conservée, supprimée ou absente après clôture. |
| Limites de l'exercice | Mention claire si aucune VM active ne permet de déclencher une vraie alerte. |

## État final attendu

À la fin de cette feuille :

- les notions métrique, log, dashboard, seuil et alerte sont comprises ;
- les métriques utiles pour les VM cloud sont identifiées ;
- le lien entre supervision et FinOps est expliqué ;
- l'absence actuelle de ressources actives est documentée honnêtement ;
- les commandes à rejouer lors d'un prochain déploiement sont prêtes ;
- aucune preuve de supervision active n'est inventée.

## Ressources

- [OVHcloud - Understanding metrics in OVHcloud Public Cloud](https://docs.ovhcloud.com/en/guides/public-cloud/cross-functional/metrics-informations)
- [OVHcloud - Observability & Monitoring](https://ovh-docs.mintlify.app/manage/observability)
- [OVHcloud - Metrics Data Platform](https://help.ovhcloud.com)
