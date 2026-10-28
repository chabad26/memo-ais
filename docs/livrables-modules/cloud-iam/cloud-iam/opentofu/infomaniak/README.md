# OpenTofu Infomaniak


> **Copie de livrable — import du 28 octobre 2026.** Source : `Modules/cloud-iam/opentofu/infomaniak/README.md`. Les résultats ci-dessous sont ceux rapportés dans le document à sa date, sans réexécution ni nouvelle validation. Des lignes sensibles potentielles ont été retirées ; consulter l’original local pour travailler.


Cette variante porte le socle OpenStack du prototype DIST01b vers
Infomaniak Public Cloud. Elle utilise le profil `clouds.yaml` fourni par
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]

## Préparer l'accès

Placer le fichier téléchargé depuis Infomaniak dans :

```bash
mkdir -p ~/.config/openstack
cp ~/Downloads/clouds.yaml ~/.config/openstack/clouds.yaml
chmod 600 ~/.config/openstack/clouds.yaml
[LIGNE RETIRÉE : identifiant, secret ou référence sensible potentielle]
```

Le nom du profil doit correspondre à `cloud_name` dans `terraform.tfvars`.

## Déployer prudemment

```bash
cd ~/cloud-iam/opentofu/infomaniak
cp terraform.tfvars.example terraform.tfvars
${EDITOR:-nano} terraform.tfvars
tofu init
tofu fmt
tofu validate
tofu plan
```

Ne lancer `tofu apply` qu'après vérification des quotas, de la région, de
l'image, des flavors et des réseaux retournés par le projet Infomaniak.
