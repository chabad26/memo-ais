# Glossaire Integration distribuee Cloud & IAM - Iteration 2

## Sujet

Deployer et automatiser le premier fournisseur cloud du module : **OVHcloud**.
Cette iteration couvre le socle Public Cloud, OpenTofu, Ansible, SSH, pare-feu
et preuves de validation.

## Termes a retenir

| Terme | Definition courte |
| --- | --- |
| Projet Public Cloud | Espace OVHcloud qui regroupe les ressources, quotas, facturation et regions. |
| Region | Emplacement geographique ou sont creees les ressources cloud. |
| Flavor | Profil d'instance : vCPU, RAM, disque ou performance associee. |
| Image | Systeme d'exploitation utilise pour creer l'instance. |
| Instance | Machine virtuelle creee chez le fournisseur cloud. |
| Cle SSH | Moyen d'authentification admin ; seule la cle publique est transmise au cloud. |
| API OVH | Interface utilisee par OpenTofu pour creer, lire ou supprimer les ressources. |
| Application key | Identifiant applicatif OVH ; secret a proteger. |
| Application secret | Secret associe a l'application OVH ; ne doit jamais etre expose. |
| Consumer key | Jeton d'autorisation OVH donne a l'application ; secret a proteger. |
| OpenTofu | Outil IaC utilise pour decrire l'instance, la cle SSH et les parametres cloud. |
| Provider OVH | Plugin OpenTofu/Terraform qui sait dialoguer avec l'API OVHcloud. |
| `tofu init` | Initialise le dossier IaC et telecharge les providers. |
| `tofu validate` | Controle la syntaxe et la coherence de la configuration. |
| `tofu plan` | Affiche les changements prevus sans les appliquer. |
| `tofu apply` | Cree ou modifie les ressources declarees. |
| State | Fichier d'etat OpenTofu qui relie le code aux ressources creees. |
| Inventaire Ansible | Fichier listant les machines a configurer et leurs variables de connexion. |
| Playbook | Fichier YAML qui decrit les taches Ansible a appliquer. |
| UFW | Pare-feu simple utilise pour autoriser SSH et bloquer le reste par defaut. |

## Commandes a retenir

| Besoin | Commande |
| --- | --- |
| Charger les variables OVH locales | `source ~/cloud-iam-ovh/env/ovh.env` |
| Formater OpenTofu | `tofu fmt` |
| Initialiser OpenTofu | `tofu init` |
| Valider OpenTofu | `tofu validate` |
| Previsualiser le deploiement | `tofu plan` |
| Deployer | `tofu apply` |
| Lire les sorties | `tofu output` |
| Lister l'etat | `tofu state list` |
| Tester SSH | `ssh debian@IP_PUBLIQUE` |
| Tester Ansible | `ansible -i ansible/inventory/ovh.ini ovh -m ping` |
| Lancer le playbook | `ansible-playbook -i ansible/inventory/ovh.ini ansible/playbooks/base-system.yml` |
| Verifier le pare-feu | `ansible -i ansible/inventory/ovh.ini ovh -a "sudo ufw status verbose"` |
| Chercher un secret suivi par Git | `git ls-files \| grep -E 'ovh\\.env|APPLICATION_SECRET|CONSUMER_KEY' || true` |

## Points de vigilance

- Ne pas versionner les cles API OVH ni le fichier `ovh.env`.
- Ne jamais capturer une cle privee SSH ou une consumer key dans les preuves.
- Verifier les noms exacts de region, flavor et image dans le projet OVHcloud
  au moment du TP.
- Executer `tofu plan` avant `tofu apply`.
- Proteger le fichier d'etat OpenTofu s'il contient des informations sensibles.
- Tester SSH avant d'activer une politique pare-feu restrictive.
- Distinguer ce qui est reellement deploye de ce qui reste prevu ou bloque.

## Preuves attendues

| Preuve | Contenu attendu |
| --- | --- |
| OpenTofu | `tofu fmt`, `tofu validate`, `tofu plan`, puis `tofu apply` si realise. |
| Ressources OVH | Instance `d2-8-2026_08_31-09-17`, region `GRA9`, flavor `d2-8`, image Ubuntu 26.04 - UEFI, IP publique masquee si besoin. |
| SSH | Connexion reussie sans mot de passe ; instance et SSH declares valides le 31/08/2026 avec utilisateur `ubuntu`. |
| Ansible | Playbook applique le 31/08/2026 (`ok=5`, `changed=3`, `failed=0`) et controles hostname, UFW, Git visibles dans `ansible-base-system-ok-5-changed-3-2026-08-31.png`. |
| Securite | Secrets absents de Git, pare-feu actif, acces SSH autorise. |
| Ecart | Blocage compte, quota, paiement, region, image ou provider documente. |

## Docs associees

- [Vue d'ensemble de l'iteration 2](../../../integration-distribuee-cloud-iam/it-2/index.md)
- [Deployer et automatiser OVH](../../../integration-distribuee-cloud-iam/it-2/deployer-automatiser-ovh.md)
