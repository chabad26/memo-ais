# Bonus - Déployer un serveur bare metal chez OVHcloud

!!! info "Bonus d'architecture"
    Ce bonus complète le déploiement des VM OVHcloud par une cible **bare
    metal**, c'est-à-dire un serveur dédié dont le système d'exploitation est
    installé directement sur le matériel.

## Objectif

Déployer un serveur dédié OVHcloud, le sécuriser et le rendre administrable
avec Ansible. L'objectif est de savoir expliquer les différences entre une VM
Public Cloud et un serveur physique, puis de produire des preuves de mise en
service propres.

Le serveur est une cible de laboratoire. Aucun secret, aucune adresse IP
publique complète et aucune donnée personnelle ne doivent apparaître dans les
captures publiées.

## Ce qui change par rapport à une VM OVH

| Sujet | VM Public Cloud | Serveur bare metal |
| --- | --- | --- |
| Provisionnement | API OpenStack ou OpenTofu | Commande depuis le Manager OVHcloud |
| Matériel | Mutualisé ou virtualisé | Ressources physiques réservées |
| Système | Image cloud | Installation via l'interface OVH, netboot ou ISO selon l'offre |
| Réseau | Réseau privé et security groups | IP publiques, vRack si disponible, pare-feu hôte |
| Automatisation | OpenTofu peut créer la VM | Ansible configure l'OS après l'installation ; l'API peut compléter l'automatisation |
| Reprise | Recréation rapide d'une VM | Réinstallation ou restauration sur un autre serveur |

!!! warning "Ne pas confondre"
    Un serveur dédié n'est pas une VM plus grosse. Il faut traiter séparément
    le cycle de vie matériel, le réseau, les sauvegardes et la procédure de
    réinstallation.

## Architecture retenue

```text
Poste d'administration
        |
        | SSH depuis une IP autorisée
        v
Serveur dédié OVHcloud
  - Ubuntu Server LTS
  - clé SSH administrateur
  - UFW / nftables
  - Docker ou services du projet
  - agent de supervision
        |
        | réseau privé vRack si souscrit et configuré
        v
Autres hôtes OVH ou site on-premise
```

Pour un premier essai, un seul serveur suffit. Les services doivent être
choisis en fonction de la mémoire, du stockage, du nombre de cœurs et du
besoin réel en I/O. Le modèle commercial et les caractéristiques exactes du
serveur sont à relever dans le Manager au moment du déploiement.

### Cible du projet

Le serveur bare metal retenu pour la suite du projet est joignable sur
`51.255.196.223`. Cette adresse est utilisée dans l'inventaire Ansible local.

| Élément | Valeur |
| --- | --- |
| Groupe Ansible | `baremetal` |
| Nom logique | `ovh-baremetal-01` |
| Adresse SSH | `51.255.196.223` |
| Utilisateur SSH | À confirmer selon l'image installée |
| Services visés | Socle DIST-01a conteneurisé |

## Étape 1 - Préparer la commande

Avant de commander ou d'installer :

- choisir une gamme et une région adaptées au besoin ;
- vérifier le prix, les frais d'installation et la durée d'engagement ;
- vérifier les disques, le RAID matériel ou logiciel et la possibilité de
  réinstaller le serveur ;
- prévoir une clé SSH dédiée au serveur ;
- définir le nom d'hôte, le domaine et le reverse DNS souhaités ;
- décider si un vRack est nécessaire pour joindre d'autres environnements ;
- écrire la stratégie de sauvegarde avant de stocker des données utiles.

Conserver comme preuve le récapitulatif de la configuration en masquant le
numéro de commande, l'adresse IP, les identifiants et les données de facturation.

## Étape 2 - Installer le système depuis le Manager

Dans l'espace OVHcloud :

1. ouvrir le serveur dédié et vérifier son état de livraison ;
2. choisir **Installer** ou **Réinstaller** ;
3. sélectionner une distribution supportée et son mode de partitionnement ;
4. sélectionner la clé SSH publique ;
5. choisir le RAID et les volumes selon le besoin ;
6. lancer l'installation et attendre la fin de l'opération ;
7. relever uniquement les informations nécessaires à l'inventaire local ;
8. tester la connexion SSH avec la clé privée conservée hors du dépôt.

Exemple de première connexion :

```bash
ssh -i ~/.ssh/ovh-baremetal_ed25519 admin@IP_PUBLIQUE
```

Le compte et l'utilisateur exacts dépendent de l'image choisie. Ne pas
supposer que `root` est autorisé par SSH : vérifier la politique de l'image et
utiliser un compte nominatif avec `sudo`.

## Étape 3 - Contrôler le socle avant de déployer

Depuis le serveur, relever les informations utiles sans publier les adresses
complètes :

```bash
hostnamectl
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINTS
ip -brief address
sudo systemctl --failed
sudo ss -tulpen
sudo ufw status verbose
```

Vérifier ensuite :

- version et support de l'OS ;
- heure synchronisée avec `timedatectl` ;
- partitions et espace disponible ;
- état SMART ou état RAID selon le matériel ;
- présence d'un compte administrateur nominatif ;
- désactivation de l'authentification SSH par mot de passe ;
- règle pare-feu minimale avant toute publication de service.

## Étape 4 - Préparer Ansible

Dans le dépôt du projet, créer `ansible/inventory/ovh-baremetal.ini` localement
et ne pas le commiter s'il contient des adresses d'exploitation :

```ini
[baremetal]
ovh-baremetal-01 ansible_host=51.255.196.223 ansible_user=ubuntu

[baremetal:vars]
ansible_python_interpreter=/usr/bin/python3
```

Remplacer `ubuntu` par le compte réellement créé lors de l'installation. La
clé privée SSH reste hors du dépôt.

Tester puis appliquer un socle dédié :

```bash
cd ~/cloud-iam
ansible -i ansible/inventory/ovh-baremetal.ini baremetal -m ping
ansible-playbook -i ansible/inventory/ovh-baremetal.ini \
  ansible/playbooks/base-system.yml
```

Après validation du socle, réutiliser le playbook de déploiement du projet :

```bash
ansible-playbook -i ansible/inventory/ovh-baremetal.ini \
  ansible/playbooks/deploy-on-premise.yml --syntax-check
ansible-playbook -i ansible/inventory/ovh-baremetal.ini \
  ansible/playbooks/deploy-on-premise.yml
```

Ne pas lancer le déploiement applicatif avant d'avoir vérifié le stockage,
l'espace disque, les ports nécessaires et la destination de sauvegarde. Les VM
cloud existantes ne doivent pas être modifiées par cet inventaire.

Le playbook doit au minimum :

- appliquer les mises à jour de sécurité ;
- créer les comptes nominatifs et leurs clés ;
- configurer `sudo` sans mot de passe partagé ;
- désactiver SSH par mot de passe et l'accès direct root ;
- limiter SSH à l'adresse ou au réseau d'administration ;
- activer le pare-feu et les journaux ;
- installer les outils de supervision et de sauvegarde ;
- configurer le fuseau horaire et la synchronisation NTP.

Relancer le playbook une seconde fois et conserver le résultat `changed=0` ou
l'explication des changements légitimes.

## Étape 5 - Réseau et exposition

La règle de départ est de n'exposer que SSH depuis le poste d'administration,
puis d'ajouter les ports nécessaires au service déployé.

| Flux | Décision attendue |
| --- | --- |
| SSH/22 | Autorisé uniquement depuis l'administration |
| HTTP/HTTPS | Ouvert seulement si le serveur publie un site |
| Interfaces d'administration | Jamais ouvertes à Internet sans restriction supplémentaire |
| Réseau privé vRack | Autorisé uniquement entre hôtes attendus |
| Sortie Internet | Conservée pour les mises à jour, avec surveillance si nécessaire |

Le vRack ne remplace pas le pare-feu. Tester séparément le routage, les routes,
les VLAN éventuels et la résolution DNS. Documenter les différences entre une
adresse publique, une adresse privée et le reverse DNS.

## Étape 6 - Déployer le service et sauvegarder

Déployer un seul service démonstrateur, par exemple Nginx, puis vérifier :

```bash
curl -I http://127.0.0.1
sudo journalctl -u nginx --since "10 minutes ago"
sudo systemctl status nginx --no-pager
```

Avant toute donnée métier, définir :

- la destination de sauvegarde hors du serveur ;
- la fréquence et la durée de rétention ;
- le chiffrement des sauvegardes ;
- un test de restauration ;
- la procédure de réinstallation du serveur et de récupération DNS.

Une sauvegarde stockée sur le même serveur ne constitue pas une stratégie de
reprise suffisante.

## Validation attendue

| Contrôle | Preuve sans secret |
| --- | --- |
| Installation terminée | Capture Manager avec IP et identifiants masqués |
| Connexion SSH par clé | Sortie `ssh -v` tronquée ou prompt sans clé affichée |
| Durcissement SSH | Extraits contrôlés de `sshd -T` |
| Pare-feu | `ufw status verbose` avec IP masquées si nécessaire |
| Ansible idempotent | Résultats des deux exécutions |
| Service actif | `systemctl status` et `curl -I` |
| Réseau privé | Test `ping` ou `nc` depuis un hôte autorisé |
| Sauvegarde | Liste d'archive et restauration d'un fichier de test |
| Réinstallation | Procédure écrite et date du dernier test |

## Limites et retour d'expérience

Le bare metal apporte des ressources prévisibles et un bon rapport coût/puissance,
mais il augmente la responsabilité d'exploitation. La panne matérielle, la
réinstallation et la récupération des données doivent être anticipées. Pour un
service critique, compléter ce bonus par un second hôte, une réplication ou une
procédure de restauration régulièrement testée.

Le livrable final doit conclure sur le choix :

- **bare metal** si la charge est stable, exigeante en ressources ou sensible
  au coût d'une VM équivalente ;
- **VM Public Cloud** si la priorité est la rapidité de création, la souplesse
  de dimensionnement et la recréation automatisée ;
- **architecture mixte** si le serveur dédié porte les charges lourdes et que
  les VM portent les services éphémères ou périphériques.
