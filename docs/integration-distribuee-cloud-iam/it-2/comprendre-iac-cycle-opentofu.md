# Comprendre l'IaC et le cycle OpenTofu

!!! info "Avant d'automatiser OVH"
    Cette feuille sert à comprendre le principe de l'Infrastructure as Code et
    le cycle de commandes OpenTofu avant de créer des ressources réelles.

## Objectif

Comprendre comment OpenTofu décrit une infrastructure dans des fichiers `.tf`,
comment il utilise des providers, et pourquoi le cycle de commandes reste le
même quel que soit le fournisseur cloud.

À la fin de la feuille, tu dois savoir expliquer :

- ce qu'est l'Infrastructure as Code ;
- le rôle d'un fichier `.tf` ;
- le rôle d'un provider ;
- la différence entre `tofu init`, `tofu plan`, `tofu apply` et
  `tofu destroy` ;
- pourquoi `plan` doit être lu avant toute application réelle.

## Principe de l'Infrastructure as Code

L'Infrastructure as Code, ou **IaC**, consiste à décrire une infrastructure avec
du code déclaratif plutôt qu'avec des clics dans une console.

Avec OpenTofu, tu n'écris pas toutes les étapes manuelles comme :

1. cliquer sur `Create network` ;
2. choisir une région ;
3. créer une VM ;
4. ajouter une règle réseau.

Tu décris plutôt l'état final attendu :

- je veux un réseau ;
- je veux un sous-réseau ;
- je veux une instance ;
- je veux un groupe de sécurité ;
- je veux telles règles d'entrée.

OpenTofu compare ensuite ce qui est écrit dans les fichiers avec ce qui existe
réellement chez le fournisseur, puis calcule les actions nécessaires.

## OpenTofu, fichiers `.tf` et état réel

Un projet OpenTofu est généralement un dossier contenant des fichiers `.tf`.
Ces fichiers peuvent décrire :

| Fichier | Rôle courant |
| --- | --- |
| `main.tf` | Ressources principales à créer. |
| `variables.tf` | Paramètres attendus par le projet. |
| `outputs.tf` | Informations à afficher après création. |
| `providers.tf` | Providers et configuration d'accès. |
| `terraform.tfvars` | Valeurs réelles des variables, souvent non versionnées. |

OpenTofu maintient aussi un fichier d'état, souvent nommé `terraform.tfstate`.
Ce fichier sert à relier le code aux ressources réellement créées.

!!! danger "État et secrets"
    Le fichier d'état peut contenir des informations sensibles. Il ne doit pas
    être publié sans vérification. Un fichier `terraform.tfvars` réel peut aussi
    contenir des secrets et doit rester hors Git ou être chiffré.

## Le rôle du provider

OpenTofu ne sait pas créer directement une instance OVH, AWS ou Azure. Il
utilise un **provider**, c'est-à-dire un plugin qui sait parler à l'API d'un
fournisseur.

Exemples :

| Fournisseur ou service | Provider |
| --- | --- |
| OVHcloud | `ovh/ovh` |
| AWS | `hashicorp/aws` |
| Azure | `hashicorp/azurerm` |
| GitHub | `integrations/github` |

Le provider doit être déclaré avant d'utiliser ses ressources.

Forme générale :

```hcl
terraform {
  required_providers {
    nom_local = {
      source  = "namespace/type"
      version = "contrainte-de-version"
    }
  }
}
```

Exemple OVH, à adapter au projet réel :

```hcl
terraform {
  required_providers {
    ovh = {
      source  = "ovh/ovh"
      version = "~> 2.0"
    }
  }
}
```

!!! note "Version datée"
    Le registry OpenTofu affiche le provider OVH `ovh/ovh` en version `v2.0.0`
    au 13 août 2026. La version exacte doit être vérifiée au moment du TP avant
    de figer une contrainte.

## Forme générale d'une ressource

Une ressource décrit un objet à gérer.

Forme générale :

```hcl
resource "type_de_ressource" "nom_local" {
  # attributs propres à cette ressource
}
```

Exemple pédagogique fictif :

```hcl
resource "ovh_cloud_project_network_private" "lab" {
  service_name = var.service_name
  name         = "dist01b-lab-net"
  regions      = [var.region]
}
```

Dans cet exemple :

| Élément | Signification |
| --- | --- |
| `resource` | Déclare un objet géré par OpenTofu. |
| `ovh_cloud_project_network_private` | Type de ressource fourni par le provider OVH. |
| `lab` | Nom local utilisé dans le code. |
| `service_name`, `name`, `regions` | Attributs attendus par cette ressource. |

!!! warning "Documentation provider"
    Les attributs exacts changent selon le type de ressource et la version du
    provider. Avant d'écrire une ressource réelle, il faut ouvrir la
    documentation du provider et copier uniquement les attributs valides.

## Le cycle de commandes OpenTofu

Le cycle reste toujours le même :

```bash
tofu init
tofu fmt
tofu validate
tofu plan
tofu apply
tofu destroy
```

Chaque commande a un rôle précis.

| Commande | Ce qu'elle fait | Modifie l'infrastructure ? |
| --- | --- | --- |
| `tofu init` | Initialise le dossier et télécharge les providers. | Non |
| `tofu fmt` | Reformate les fichiers `.tf`. | Non |
| `tofu validate` | Vérifie la syntaxe et la cohérence locale. | Non |
| `tofu plan` | Calcule les changements prévus. | Non |
| `tofu apply` | Applique réellement les changements. | Oui |
| `tofu destroy` | Détruit les ressources gérées par ce code. | Oui |

## Étape 1 - Initialiser le dossier

Depuis le dossier qui contient les fichiers `.tf` :

```bash
tofu init
```

Cette commande :

- lit les blocs `terraform.required_providers` ;
- contacte le registry ;
- télécharge les providers nécessaires ;
- prépare le dossier de travail.

Preuve à conserver :

```bash
tofu init
```

Résultat attendu :

```text
OpenTofu has been successfully initialized
```

## Étape 2 - Mettre en forme et valider

```bash
tofu fmt
tofu validate
```

`tofu fmt` rend le code plus lisible. `tofu validate` vérifie que la
configuration est compréhensible pour OpenTofu.

Preuves à conserver :

| Preuve | Attendu |
| --- | --- |
| Formatage | Pas de fichier restant à reformater. |
| Validation | Message de réussite de `tofu validate`. |

## Étape 3 - Lire le plan

```bash
tofu plan
```

Le plan est la commande la plus importante avant toute action réelle. Il indique
ce qu'OpenTofu prévoit de créer, modifier ou supprimer.

Symboles fréquents :

| Symbole | Sens |
| --- | --- |
| `+` | Ressource à créer. |
| `~` | Ressource à modifier. |
| `-` | Ressource à supprimer. |
| `-/+` | Ressource à remplacer. |

Avant un `apply`, tu dois pouvoir expliquer le plan avec tes mots.

Questions à se poser :

| Question | Pourquoi |
| --- | --- |
| Les ressources créées sont-elles attendues ? | Éviter une création hors périmètre. |
| Une ressource va-t-elle être supprimée ? | Éviter une perte de service. |
| Une ressource va-t-elle être remplacée ? | Anticiper coupure, coût ou perte de données. |
| Des secrets apparaissent-ils dans la sortie ? | Éviter une preuve compromettante. |

## Étape 4 - Appliquer seulement après validation

```bash
tofu apply
```

OpenTofu affiche de nouveau le plan et demande confirmation. Cette commande
modifie réellement l'infrastructure.

Règle de travail :

| Situation | Décision |
| --- | --- |
| Plan compris et conforme | `apply` possible. |
| Plan flou | Stopper et relire le code. |
| Suppression inattendue | Stopper. |
| Remplacement inattendu | Stopper. |
| Secret visible dans la sortie | Stopper et corriger la gestion des variables. |

## Étape 5 - Détruire les ressources de test

```bash
tofu destroy
```

Cette commande détruit les ressources suivies par l'état OpenTofu. Elle est
utile pour nettoyer un laboratoire, mais dangereuse sur un environnement réel.

Avant de confirmer :

- vérifier le projet cloud ciblé ;
- vérifier la région ;
- vérifier la liste des ressources concernées ;
- conserver les preuves utiles ;
- confirmer que la ressource n'est plus nécessaire.

!!! danger "Production"
    Ne jamais lancer `tofu destroy` sur un dossier dont le périmètre n'est pas
    parfaitement compris.

## Mini-exercice sans création cloud

Créer un dossier local de test :

```bash
mkdir -p ~/cloud-iam-ovh/iac-cycle
cd ~/cloud-iam-ovh/iac-cycle
```

Créer un fichier `main.tf` contenant uniquement le bloc provider :

```hcl
terraform {
  required_providers {
    ovh = {
      source  = "ovh/ovh"
      version = "~> 2.0"
    }
  }
}
```

Puis exécuter :

```bash
tofu init
tofu fmt
tofu validate
```

Ce mini-exercice permet de vérifier que le provider se télécharge et que le
cycle commence correctement, sans créer de ressource OVH.

## Tableau de validation

| Point de contrôle | Statut | Preuve |
| --- | --- | --- |
| Principe IaC reformulé | À compléter | Phrase personnelle ou note de cours. |
| Provider identifié | À compléter | `ovh/ovh` dans le bloc `required_providers`. |
| `tofu init` compris | À compléter | Provider téléchargé. |
| `tofu fmt` exécuté | À compléter | Code formaté. |
| `tofu validate` exécuté | À compléter | Validation réussie. |
| `tofu plan` expliqué | À compléter | Création, modification ou suppression identifiée. |
| Risque de `apply` compris | À compléter | Note personnelle. |
| Risque de `destroy` compris | À compléter | Note personnelle. |

## Ressources

Sources consultées le 13 août 2026 :

- [OpenTofu - Getting Started](https://opentofu.org/docs/intro/)
- [OpenTofu Registry - Provider OVH](https://search.opentofu.org/provider/ovh/ovh/v2.0.0)
