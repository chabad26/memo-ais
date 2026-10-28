# Cloud IAM


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/cloud-iam/README.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


Patrons de travail pour le prototype Cloud/IAM OVHcloud et Infomaniak.

Les instances OVHcloud Public Cloud sont pilotées par l'API OpenStack du projet.
Le dossier `opentofu/ovh/` utilise donc le provider OpenStack, avec les
variables `OS_*` fournies par le fichier OpenRC OVHcloud.

## Arborescence

```text
cloud-iam/
├── opentofu/
│   └── ovh/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── terraform.tfvars.example
│   └── infomaniak/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── terraform.tfvars.example
└── ansible/
    ├── inventory/
    ├── playbooks/
    └── roles/
```

## Précautions

- Ne pas versionner le fichier OpenRC complet, le fichier `terraform.tfvars`,
  les fichiers `.env`, les clés SSH privées ou les fichiers `tfstate`.
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
- Lancer `tofu plan` et relire les changements avant tout `tofu apply`.
- Ne pas lancer `tofu apply` avec un nom d'instance déjà créé manuellement sans
  décider d'abord si l'objectif est de créer une nouvelle VM ou d'importer
  l'existante dans l'état OpenTofu.
- Le prototype reste temporairement sur le Security Group `default`, car le
  quota réseau GRA9 autorise actuellement zéro Security Group et zéro règle.
  Le filtrage SSH est appliqué dans UFW par Ansible, depuis `admin_ssh_cidr`.
- Le dimensionnement cible est `1 × d2-4 + 2 × d2-2` ; les deux petites
  instances utilisent aussi `default` et le réseau privé GRA9.

## Validation locale

Depuis `opentofu/ovh/` :

```bash
tofu fmt
tofu init
tofu validate
tofu plan
```

Le `plan` nécessite un fichier local `terraform.tfvars` ou des variables
d'environnement contenant les valeurs réelles du projet OVHcloud.

Pour Infomaniak, utiliser `opentofu/infomaniak/` et le profil
`clouds.yaml` téléchargé depuis le Manager. Le fichier doit être placé dans
`~/.config/openstack/clouds.yaml` et ne doit pas être versionné.

Exemple de préparation côté terminal :

```bash
source ~/cloud-iam-ovh/env/openrc.sh
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars
tofu plan
```
