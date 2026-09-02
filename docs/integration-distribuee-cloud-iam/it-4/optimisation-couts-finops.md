# Optimisation des coûts FinOps

!!! info "Durée indicative : 1h30"
    Cette feuille sert à repérer les ressources cloud inutilisées sur les deux
    fournisseurs réellement utilisés dans le module, **OVHcloud** et
    **Infomaniak**, et à documenter les économies possibles. Les suppressions
    ne sont faites qu'après vérification. Dans notre cas, les ressources
    d'exercice ont déjà été détruites après validation.

## Objectif

Repérer et supprimer les ressources cloud inutilisées, sources de coûts cachés.

Une infrastructure qui grandit accumule vite des ressources orphelines :
volumes détachés, IP publiques non utilisées, instances de test oubliées,
snapshots anciens ou objets de sauvegarde devenus inutiles. Chacune peut
coûter, même si aucun service ne l'utilise réellement.

L'objectif est donc de faire l'inventaire de ce qui a été réellement déployé
depuis le début du module, puis de décider ce qui doit être conservé,
supprimé ou revu.

## Situation réelle du module

Les exercices de déploiement OVHcloud et Infomaniak ont été validés, puis les
ressources cloud ont été détruites pour éviter une facturation inutile. Il n'y
a donc plus de VM, d'IP publique ou de volume actif à auditer comme si
l'infrastructure était encore en ligne.

La fiche FinOps ne doit pas inventer une ressource orpheline. Elle sert ici à
documenter trois choses :

1. les ressources qui avaient été créées pendant l'exercice ;
2. la décision de destruction après réussite des tests ;
3. le contrôle final d'absence de ressources résiduelles.

Le nettoyage est donc déjà fait. La preuve attendue devient une preuve de
clôture : les listes de ressources doivent être vides ou ne contenir que des
éléments explicitement conservés.

!!! note "Écart avec le cours"
    Le support de cours peut citer AWS pour illustrer un second fournisseur.
    Dans ce dossier, le second fournisseur pratique reste **Infomaniak Public
    Cloud**. Les commandes et preuves attendues sont donc centrées sur
    OpenStack : OVHcloud d'un côté, Infomaniak de l'autre.

!!! warning "Prix et économies"
    Les montants utilisés ici reprennent les estimations de la séquence
    [Estimer et comparer le coût mensuel d'une migration](../it-1/estimer-comparer-couts-migration.md),
    consultées le `2026-08-12`. Les économies réelles doivent être confirmées
    dans la facture ou le calculateur du fournisseur avant d'être présentées
    comme un gain définitif.

## Ce que tu vas faire, et pourquoi

| Action | Pourquoi |
| --- | --- |
| Reprendre les preuves du déploiement réussi. | Savoir quelles ressources ont réellement existé. |
| Documenter la destruction déjà faite. | Montrer que l'exercice a été clôturé proprement. |
| Lister les VM, volumes, IP publiques et snapshots restants. | Vérifier qu'aucun coût caché ne subsiste. |
| Noter les ressources absentes ou conservées. | Éviter d'inventer un nettoyage non réalisé. |
| Calculer le coût mensuel évité. | Transformer la clôture technique en preuve FinOps. |

## Ressources à contrôler

| Ressource | Risque FinOps | Indice de ressource orpheline |
| --- | --- | --- |
| Instance / VM | Facturation compute continue | VM de test arrêtée ou oubliée, nom hors convention, aucun service attendu. |
| Volume bloc | Stockage facturé sans usage | Volume `available` ou détaché d'une instance. |
| IP publique | Adresse facturée ou ressource rare | IP non associée à un port, une VM ou une interface. |
| Snapshot | Stockage accumulé | Ancien snapshot sans lien avec un point de restauration attendu. |
| Stockage objet | Coût de stockage ou requêtes | Bucket d'exercice oublié, sauvegardes de test non conservées. |

## Déroulement

| Étape | Travail à faire | Preuve attendue |
| --- | --- | --- |
| 1 | Reprendre l'inventaire des ressources qui avaient été créées sur OVHcloud et Infomaniak. | Captures de déploiement ou sorties OpenTofu/Ansible déjà conservées. |
| 2 | Documenter que les ressources d'exercice ont été détruites après réussite. | Note de décision datée : exercice validé, ressources supprimées pour stopper la facturation. |
| 3 | Lister les ressources restantes sur chaque fournisseur. | Capture console ou sortie CLI montrant l'absence de VM, volume ou IP non utilisée. |
| 4 | Calculer le coût mensuel évité. | Calcul simple basé sur les tarifs de la séquence 1.4 et les flavors réellement utilisés. |

## Commandes à retenir

### OpenStack OVHcloud ou Infomaniak

Ces commandes sont valables pour les fournisseurs exposant une API OpenStack.
Adapter `OS_CLOUD` au profil local, par exemple `ovh` ou
`PCP-LDG88UE-dc3-a`.

!!! tip "Nom du profil Infomaniak"
    Le nom passé à `--os-cloud` doit être le nom exact d'une entrée dans
    `~/.config/openstack/clouds.yaml`. Ce n'est pas forcément le nom court du
    projet `PCP-XXXXXXX`, et ce n'est pas le nom utilisateur `PCU-XXXXXXX`.
    Pour Infomaniak, le profil contient souvent la région, par exemple
    `PCP-LDG88UE-dc3-a`.

```bash
export OS_CLOUD=PROFIL_OPENSTACK

openstack cloud list
openstack server list
openstack volume list
openstack floating ip list
openstack image list --private
openstack security group list
```

Repérer les volumes détachés :

```bash
openstack volume list --status available
```

Repérer les IP publiques sans port associé :

```bash
openstack floating ip list
```

Avant suppression, afficher le détail :

```bash
openstack server show NOM_OU_ID
openstack volume show NOM_OU_ID
openstack floating ip show IP_OU_ID
```

Commandes de suppression à utiliser seulement après validation :

```bash
openstack server delete NOM_OU_ID
openstack volume delete NOM_OU_ID
openstack floating ip delete IP_OU_ID
```

!!! danger "Suppression"
    Une suppression cloud est souvent définitive ou coûteuse à restaurer.
    Vérifier les sauvegardes, les dépendances et l'accord de suppression avant
    d'exécuter une commande destructive.

## Tableau d'inventaire

| Fournisseur | Ressources d'exercice | État actuel | Décision | Preuve à conserver |
| --- | --- | --- | --- | --- |
| OVHcloud | VM principales et secondaires, IP, volumes associés | Supprimé après réussite de l'exercice | Clôture pour éviter les coûts | Capture console ou sortie `openstack server list`, `volume list`, `floating ip list`. |
| Infomaniak | Trois VM, IP publiques, volumes associés | Supprimé après réussite de l'exercice | Clôture pour éviter les coûts | Capture console ou sortie `openstack server list`, `volume list`, `floating ip list`. |

## Exemple de décision documentée

| Champ | Exemple |
| --- | --- |
| Date | `AAAA-MM-JJ` |
| Fournisseur | `OVHcloud` ou `Infomaniak` |
| Ressource | Ressources d'exercice du module Cloud & IAM |
| Type | VM, IP publiques et volumes associés |
| Constat | Les exercices sont terminés et les services ont été validés. |
| Vérification | Les preuves de déploiement existent dans les fiches précédentes. |
| Décision | Suppression des ressources d'exercice pour arrêter la facturation. |
| Preuve avant | Captures de déploiement, sorties OpenTofu ou captures console déjà conservées. |
| Preuve après | Sorties `openstack server list`, `openstack volume list`, `openstack floating ip list`. |
| Économie estimée | Coût mensuel évité si les ressources étaient restées actives. |

## Calculer l'économie mensuelle

Reprendre les montants de la séquence 1.4 et compléter avec les tarifs réels
du fournisseur :

| Ressource supprimée | Base de calcul | Économie mensuelle estimée |
| --- | --- | ---: |
| VM OVHcloud `d2-4` inutile | `0,0206 EUR/h x 730 h` | `15,04 EUR/mois` |
| VM Infomaniak principale inutile | tarif mensuel Infomaniak du flavor réel | `A_COMPLETER` |
| VM Infomaniak secondaire inutile | tarif mensuel Infomaniak du flavor réel | `A_COMPLETER` |
| Volume bloc détaché | prix du Go/mois x taille du volume | `A_COMPLETER` |
| IP publique inutilisée | prix mensuel de l'adresse | `A_COMPLETER` |
| Snapshot ancien | prix du Go/mois x taille conservée | `A_COMPLETER` |

Formule :

```text
économie mensuelle = coût mensuel avant nettoyage - coût mensuel après nettoyage
```

Pour plusieurs ressources :

```text
économie totale = économie ressource 1 + économie ressource 2 + économie ressource 3
```

Dans le cas présent, parler de **coût évité** est plus précis que parler
d'économie réalisée sur une ressource orpheline : les VM n'ont pas été
oubliées, elles ont été détruites volontairement à la fin de l'exercice.

## Pour aller plus loin : script d'audit

Le script
[`audit-ressources-orphelines.sh`](../../assets/scripts/integration-distribuee-cloud-iam/it-4/audit-ressources-orphelines.sh)
liste automatiquement les ressources probablement orphelines ou résiduelles.
Il ne supprime rien. Après destruction, une sortie vide ou limitée aux en-têtes
devient une preuve utile : elle montre qu'il ne reste plus de VM, volume ou IP
publique à facturer.

Exemple OpenStack :

```bash
docs/assets/scripts/integration-distribuee-cloud-iam/it-4/audit-ressources-orphelines.sh \
  openstack PROFIL_OPENSTACK
```

Pour auditer deux profils OpenStack :

```bash
docs/assets/scripts/integration-distribuee-cloud-iam/it-4/audit-ressources-orphelines.sh \
  openstack ovh

docs/assets/scripts/integration-distribuee-cloud-iam/it-4/audit-ressources-orphelines.sh \
  openstack PCP-LDG88UE-dc3-a
```

Conserver la sortie dans un fichier daté :

```bash
mkdir -p preuves/finops
docs/assets/scripts/integration-distribuee-cloud-iam/it-4/audit-ressources-orphelines.sh \
  openstack PCP-LDG88UE-dc3-a \
  | tee preuves/finops/audit-infomaniak-AAAA-MM-JJ.txt
```

## État final attendu

À la fin de cette feuille :

- l'inventaire des ressources qui avaient été créées est documenté ;
- la destruction des ressources d'exercice est expliquée ;
- l'absence de ressources résiduelles est vérifiée par console ou CLI ;
- le coût mensuel évité est calculé ou explicitement marqué `A_COMPLETER` ;
- les preuves de déploiement et de clôture sont conservées ;
- aucun secret ni identifiant sensible n'est publié.
