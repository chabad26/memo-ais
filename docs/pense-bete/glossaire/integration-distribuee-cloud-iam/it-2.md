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
| OpenTofu | Outil IaC utilise pour decrire l'instance principale, la cle SSH et les parametres cloud. |
| Provider OVH | Plugin OpenTofu/Terraform qui sait dialoguer avec l'API OVHcloud. |
| `tofu init` | Initialise le dossier IaC et telecharge les providers. |
| `tofu validate` | Controle la syntaxe et la coherence de la configuration. |
| `tofu plan` | Affiche les changements prevus sans les appliquer. |
| `tofu apply` | Cree ou modifie les ressources declarees. |
| State | Fichier d'etat OpenTofu qui relie le code aux ressources creees. |
| Inventaire Ansible | Fichier listant les machines a configurer et leurs variables de connexion. |
| Playbook | Fichier YAML qui decrit les taches Ansible a appliquer. |
| UFW | Pare-feu simple utilise pour autoriser SSH et bloquer le reste par defaut. |
| Role Ansible | Ensemble reutilisable de taches, fichiers et handlers, ici utilise pour deployer Nginx et le site Olidev. |
| Backend S3 | Stockage distant de l'etat OpenTofu dans le bucket Object Storage `tan-thouless`. |
| Alias `/etc/hosts` | Association locale entre `cloud.olidev.ovh` et l'IP de la VM, sans DNS public. |

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
| Tester le site par IP | `curl -4 -I http://IP_PUBLIQUE` |
| Tester le nom local | `getent hosts cloud.olidev.ovh && curl -I http://cloud.olidev.ovh` |
| Initialiser le backend S3 | `source ~/cloud-iam-ovh/env/openrc.sh`, puis `AWS_PROFILE=ovh-s3 tofu init -migrate-state` |
| Chercher un secret suivi par Git | `git ls-files \| grep -E 'ovh\\.env|APPLICATION_SECRET|CONSUMER_KEY' || true` |

## Points de vigilance

- Ne pas versionner les cles API OVH ni le fichier `ovh.env`.
- `openrc.sh` charge l'authentification OpenStack ; `AWS_PROFILE=ovh-s3` charge les identifiants du backend S3. Les deux sont nécessaires lorsque l'état est distant.
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
| Ressources OVH | Instance principale `d2-8-2026_08_31-09-17`, region `GRA9`, flavor `d2-4`, image Ubuntu 26.04 - UEFI ; deux `d2-2` a recreer pour les services. |
| SSH | Connexion reussie sans mot de passe ; instance et SSH declares valides le 31/08/2026 avec utilisateur `ubuntu`. |
| Ansible | Playbook applique sur la VM principale (`ok=12`, `changed=2`, `failed=0`), puis rejoue avec `changed=0`; Nginx et le site Olidev sont actifs. |
| Securite | Secrets absents de Git, pare-feu actif, acces SSH autorise. |
| Ecart | Blocage compte, quota, paiement, region, image ou provider documente. |

## Compléments à retenir

| Notion | Repère |
| --- | --- |
| Réseau privé | Séparer les échanges internes des accès publics ; limiter SSH à l’adresse d’administration autorisée. |
| Backend distant | Partager et protéger l’état OpenTofu ; vérifier ses dépendances avant nettoyage. |
| Idempotence | Rejouer Ansible et vérifier que la configuration conforme ne change plus. |
| DNS et répartition de charge | La résolution de nom et la distribution des requêtes remplissent des rôles différents. |
| Trois VM | Répartir les services et vérifier leurs communications inter-hôtes. |
| Infomaniak | Adapter le provisionnement au fournisseur, puis réutiliser les rôles Ansible. |
| Bare metal | Variante sur serveur physique dédié, distincte du Public Cloud ; consulter les limites de la fiche. |

Les noms et résultats présents dans les preuves ci-dessus décrivent le laboratoire historique. Ils ne constituent pas un inventaire de ressources encore actives.

## Docs associees

- [Vue d'ensemble de l'iteration 2](../../../integration-distribuee-cloud-iam/it-2/index.md)
- [Deployer et automatiser OVH](../../../integration-distribuee-cloud-iam/it-2/deployer-automatiser-ovh.md)

- [Automatiser avec Ansible](../../../integration-distribuee-cloud-iam/it-2/automatiser-avec-ansible.md)
- [Bonus - Déployer un serveur bare metal chez OVHcloud](../../../integration-distribuee-cloud-iam/it-2/bonus-deploiement-bare-metal-ovh.md)
- [Comprendre l'IaC et le cycle OpenTofu](../../../integration-distribuee-cloud-iam/it-2/comprendre-iac-cycle-opentofu.md)
- [Construire un réseau isolé OVH à la main](../../../integration-distribuee-cloud-iam/it-2/construire-reseau-isole-ovh.md)
- [Déployer et automatiser Infomaniak](../../../integration-distribuee-cloud-iam/it-2/deployer-automatiser-infomaniak.md)
- [Déployer le socle on-premise sur trois VM OVH](../../../integration-distribuee-cloud-iam/it-2/deployer-socle-on-premise-sur-trois-vm.md)
- [DNS et répartition de charge cloud](../../../integration-distribuee-cloud-iam/it-2/dns-repartition-charge-cloud.md)
- [Playbook et versionnement](../../../integration-distribuee-cloud-iam/it-2/playbook-versionnement-service.md)
- [Utiliser le stockage objet OVH comme backend OpenTofu](../../../integration-distribuee-cloud-iam/it-2/stockage-objet-backend-opentofu.md)
