# Bonus - Préparer un serveur bare metal chez OVHcloud

!!! info "Bonus d'architecture"
    Ce bonus complète le déploiement des VM OVHcloud par la préparation d'une
    cible **bare metal** existante, c'est-à-dire un serveur dédié dont le
    système d'exploitation est installé directement sur le matériel.

## Objectif

Préparer le serveur dédié existant `fleender`, le sécuriser et le rendre
administrable avec Ansible. L'objectif est de savoir expliquer les différences
entre une VM Public Cloud et un serveur physique, puis de produire des preuves
d'exploitation propres.

Le serveur `fleender` est un serveur de production qui héberge déjà un site.
Le test Docker a donc été réalisé temporairement, avec un périmètre limité,
puis entièrement démonté après la collecte des preuves. Aucun secret, aucune
donnée bancaire et aucune donnée personnelle ne doivent apparaître dans les
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
    réinstallation. Ici, le serveur existe déjà : l'objectif est de préparer
    son exploitation avec Ansible.

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

Le serveur `fleender` existe déjà. Les services doivent être choisis en
fonction de sa mémoire, de son stockage, du nombre de cœurs et du besoin réel
en I/O. Ses caractéristiques sont à relever avant le déploiement applicatif.

### Cible du projet

Le serveur bare metal retenu pour la suite du projet est joignable sur
`51.255.196.223`. Cette adresse est utilisée dans l'inventaire Ansible local.

| Élément | Valeur |
| --- | --- |
| Groupe Ansible | `baremetal` |
| Nom logique | `fleender` |
| Adresse SSH | `51.255.196.223` |
| Utilisateur SSH | À confirmer selon l'image installée |
| Services visés | Socle DIST-01a conteneurisé |

## Étape 1 - Relever l'existant

Avant de préparer Ansible, relever sur `fleender` :

- le système d'exploitation et sa version ;
- les disques, volumes, RAID et l'espace disponible ;
- le compte SSH administrateur et la clé utilisée ;
- les ports déjà ouverts et les services actifs ;
- la destination de sauvegarde hors du serveur.

Conserver les sorties de contrôle sans publier de clé privée, de mot de passe
ou de donnée sensible.

## Étape 2 - Vérifier l'accès au serveur existant

Le serveur est déjà installé. Vérifier seulement que l'accès SSH fonctionne
avec la clé conservée hors du dépôt :

Exemple de première connexion :

```bash
ssh -i ~/.ssh/ovh-baremetal_ed25519 UTILISATEUR_SSH@51.255.196.223
```

Remplacer `UTILISATEUR_SSH` par le compte réellement présent sur `fleender`.
Ne pas supposer que `root` est autorisé par SSH ; vérifier l'accès `sudo`.

## Étape 3 - Contrôler le socle avant de déployer

!!! warning "Serveur en production"
  `fleender` héberge déjà un site. Ne pas lancer de mise à jour globale,
  modifier UFW, redémarrer des services ou appliquer un playbook complet
  sans fenêtre d'intervention, sauvegarde vérifiée et retour arrière prévu.
  La première intervention Ansible doit rester en lecture seule.

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
fleender ansible_host=51.255.196.223 ansible_user=ubuntu

[baremetal:vars]
ansible_python_interpreter=/usr/bin/python3
```

Remplacer `ubuntu` par le compte réellement créé lors de l'installation. La
clé privée SSH reste hors du dépôt.

Tester uniquement la connexion et le mode simulation :

```bash
cd ~/cloud-iam
ansible -i ansible/inventory/ovh-baremetal.ini baremetal -m ping
ansible-playbook -i ansible/inventory/ovh-baremetal.ini \
  ansible/playbooks/base-system.yml --check --diff
```

Avant toute modification, conserver au minimum la configuration des services,
des ports et du pare-feu. Le playbook applicatif ne doit être lancé qu'après
identification précise des tâches qui touchent le site.

```bash
ansible -i ansible/inventory/ovh-baremetal.ini baremetal -b -m shell \
  -a 'systemctl --type=service --state=running; ss -tulpen; ufw status verbose'
```

Après validation explicite et sur une fenêtre d'intervention, vérifier d'abord
la syntaxe du playbook de déploiement :

```bash
ansible-playbook -i ansible/inventory/ovh-baremetal.ini \
  ansible/playbooks/deploy-on-premise.yml --syntax-check
```

Ne pas lancer le déploiement applicatif avant d'avoir vérifié le stockage,
l'espace disque, les ports nécessaires et la destination de sauvegarde. Les VM
cloud existantes ne doivent pas être modifiées par cet inventaire.

Si une modification est validée, elle doit être ciblée et documentée. Le socle
à contrôler, sans l'appliquer automatiquement, couvre notamment :

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

## Étape 6 - Déployer temporairement les services de test

Pour préserver le site Apache existant, aucun Nginx ni WordPress n'a été
installé sur `fleender`. Le test a porté uniquement sur LDAP, la messagerie et
la supervision Docker, avec vérification des ports avant démarrage.

Les contrôles réalisés ont confirmé que :

- Apache conserve les ports `80` et `443` ;
- LAM répond sur le port `8081` ;
- Elasticsearch répond localement sur le port configuré ;
- les services de messagerie utilisent les ports dédiés `25`, `587`, `143`,
  `993` et `8443`.

Après les captures, les conteneurs, volumes et réseaux créés pour le test ont
été supprimés. Docker et les fichiers temporaires copiés sur le serveur ont
également été retirés afin de laisser `fleender` dans son état de production.

## Résultats et preuves du test

![Interface LAM accessible sur fleender](../../assets/img/integration-distribuee-cloud-iam/it-2/Capture%20d’écran%20du%202026-09-07%2011-30-31.png)

_LAM est accessible sur `http://51.255.196.223:8081` et utilise le service
OpenLDAP du test._

![Elasticsearch répond localement](../../assets/img/integration-distribuee-cloud-iam/it-2/Capture%20d’écran%20du%202026-09-07%2011-31-19.png)

_La réponse JSON confirme qu'Elasticsearch fonctionne pendant le test de
supervision. Le service est lié localement et n'a pas été exposé sur Internet._

## Sauvegarde et exploitation

Avant toute donnée métier, définir :

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
