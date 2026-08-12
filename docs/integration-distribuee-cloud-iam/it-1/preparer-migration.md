# Itération 1 - Préparer la migration

!!! info "J1 matin"
    Cette séquence se fait une seule fois au début du module. Si un compte ou un outil est déjà en place, il ne faut pas le recréer : passer directement à la vérification.

## Objectif

Cette première feuille prépare le terrain avant la migration cloud de l'infrastructure **DIST-01a**.

L'objectif n'est pas encore de déployer des ressources cloud. Il s'agit de vérifier que les accès, les outils et les prérequis sont prêts avant les travaux suivants :

- comparer OVH et AWS ;
- préparer le projet Public Cloud ;
- installer les outils d'automatisation ;
- vérifier les commandes de base ;
- anticiper les blocages liés aux comptes, crédits d'essai et cartes bancaires.

## Ce que tu vas faire, et pourquoi

| Étape | Pourquoi c'est important |
| --- | --- |
| Créer ou vérifier le compte OVH | Disposer d'un fournisseur européen pour comparer souveraineté, localisation et services. |
| Créer ou vérifier le compte AWS | Disposer d'un fournisseur non européen pour comparer les modèles et contraintes. |
| Installer OpenTofu | Préparer le provisionnement reproductible de l'infrastructure. |
| Installer Ansible | Préparer la configuration automatisée des machines et services. |
| Installer Git, SOPS et git-crypt | Versionner le travail sans exposer les secrets en clair. |

## 0.1 - Créer ou vérifier le compte OVH

Se rendre sur :

[ovhcloud.com/fr](https://www.ovhcloud.com/fr/)

Créer un compte OVH si nécessaire. Un compte de base ne demande normalement pas de carte bancaire.

### Vérification optionnelle via l'API OVH

```bash
curl -s https://api.ovh.com/1.0/ | head -20
```

Résultat attendu :

- la commande répond ;
- l'API OVH est joignable ;
- aucune authentification n'est encore nécessaire pour cette vérification simple.

!!! warning "Crédit Public Cloud"
    L'activation du crédit d'essai Public Cloud, par exemple 200 euros, peut demander une carte bancaire pour vérification d'identité. Il faut créer le projet Public Cloud dès aujourd'hui pour lever ce point avant J3.

## 0.2 - Créer ou vérifier le compte AWS

Se rendre sur :

[aws.amazon.com/fr](https://aws.amazon.com/fr/)

Créer un compte AWS et choisir le **Free Plan**.

!!! warning "Carte bancaire obligatoire"
    AWS demande une carte bancaire valide dès l'inscription, y compris avec le Free Plan. Cette étape sert à la vérification d'identité et à l'ouverture du compte. Il faut donc anticiper ce point avant les séances de déploiement.

### Installer l'AWS CLI

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
```

### Configurer l'AWS CLI

```bash
aws configure
```

Renseigner :

- `Access Key ID` ;
- `Secret Access Key` ;
- région par défaut ;
- format de sortie, par exemple `json`.

!!! danger "Secrets AWS"
    Ne jamais coller une Access Key ou une Secret Key dans la documentation, dans Git, dans une capture publique ou dans un ticket. La preuve attendue doit montrer que la CLI fonctionne, pas révéler les secrets.

## 0.3 - Installer OpenTofu

OpenTofu servira à décrire et provisionner l'infrastructure cloud sous forme de code.

```bash
curl --proto '=https' --tlsv1.2 -fsSL https://get.opentofu.org/install-opentofu.sh -o install-opentofu.sh
chmod +x install-opentofu.sh
./install-opentofu.sh --install-method deb
tofu version
```

Résultat attendu :

- la commande `tofu` est disponible ;
- `tofu version` affiche la version installée ;
- le script d'installation peut ensuite être supprimé ou archivé hors du dépôt si inutile.

## 0.4 - Installer Ansible, Git, SOPS et git-crypt

Ansible servira à configurer les systèmes après leur création. Git servira au versionnement. SOPS et git-crypt serviront à protéger les secrets.

```bash
sudo apt update
sudo apt install -y ansible git git-crypt
ansible --version
git --version
git-crypt --version
```

### Installer SOPS

```bash
curl -sLO https://github.com/getsops/sops/releases/download/v3.13.3/sops-v3.13.3.checksums.txt
curl -sLO https://github.com/getsops/sops/releases/download/v3.13.3/sops-v3.13.3.linux.amd64
sha256sum --check --ignore-missing sops-v3.13.3.checksums.txt
chmod +x sops-v3.13.3.linux.amd64
sudo mv sops-v3.13.3.linux.amd64 /usr/local/bin/sops
sops --version
```

Résultat attendu :

- Ansible est disponible ;
- Git est disponible ;
- git-crypt est disponible ;
- SOPS est disponible dans `/usr/local/bin/sops`.

## Vérifications à conserver

Les preuves de cette feuille doivent rester simples et ne doivent pas exposer de secrets.

| Élément | Commande ou preuve | À conserver |
| --- | --- | --- |
| API OVH joignable | `curl -s https://api.ovh.com/1.0/ \| head -20` | Sortie courte ou capture terminal. |
| AWS CLI installée | `aws --version` | Version affichée. |
| AWS CLI configurée | `aws configure list` | Capture sans secret visible. |
| OpenTofu installé | `tofu version` | Version affichée. |
| Ansible installé | `ansible --version` | Version affichée. |
| Git installé | `git --version` | Version affichée. |
| git-crypt installé | `git-crypt --version` | Version affichée. |
| SOPS installé | `sops --version` | Version affichée. |

!!! tip "Capture propre"
    Avant de capturer le terminal, vérifier qu'aucune clé d'accès, aucun token et aucun mot de passe ne sont visibles.

## État final attendu

À la fin de cette feuille :

- les comptes OVH et AWS sont créés ou leur création est planifiée avec les contraintes connues ;
- les éventuels besoins de carte bancaire sont identifiés avant les séances de déploiement ;
- OpenTofu, Ansible, Git, SOPS et git-crypt sont installés ;
- les commandes de version fonctionnent ;
- aucune information sensible n'est stockée en clair dans la documentation ou dans Git.

## Ressources

- [OVH Public Cloud](https://www.ovhcloud.com/fr/public-cloud/)
- [AWS Free Tier](https://aws.amazon.com/free/)
- [OpenTofu - Installation](https://opentofu.org/docs/intro/install/)
- [Ansible - Installation guide](https://docs.ansible.com/ansible/latest/installation_guide/)
- [SOPS](https://github.com/getsops/sops)
- [git-crypt](https://github.com/AGWA/git-crypt)
