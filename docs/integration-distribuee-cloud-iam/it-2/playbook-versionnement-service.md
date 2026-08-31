# Playbook et versionnement

!!! info "Durée indicative : 2 h 45"
    Cette feuille prolonge l'automatisation de base. Elle propose Nginx comme
    service réel, mais le service peut être remplacé par un autre composant
    simple de DIST-01a.

## Objectif

Automatiser le déploiement d'un service réel avec Ansible, le rendre rejouable,
organiser le code en rôles et versionner chaque étape dans Git.

L'activité ajoute aussi une sauvegarde horodatée de la configuration du service
dans le bucket Object Storage préparé précédemment. Cette sauvegarde constituera
un point de restauration exploitable au Kit 4.

## Pré-requis et état réel

Le dépôt opérationnel `/home/oliv/cloud-iam` contient déjà :

- un inventaire OVH limité à `dist01b-ovh` ;
- le playbook `ansible/playbooks/base-system.yml` et le rôle `web` ;
- une clé SSH et des VM joignables par Ansible ;
- un dépôt Git local initialisé avec un premier commit.

Le déploiement Nginx et le découpage en rôle ont été réalisés sur la VM
principale. La sauvegarde dans le bucket reste à exécuter et à prouver. Le
backend S3 de l'état OpenTofu est configuré, mais les vérifications finales
restent à conserver dans les preuves.

## Étape 1 - Choisir et définir le service

Pour cet exercice, le service cible est Nginx :

| Élément | État attendu |
| --- | --- |
| Paquet | `nginx` installé par Ansible |
| Service | `nginx` démarré et activé |
| Contenu | page d'accueil de démonstration versionnée |
| Vérification | réponse HTTP locale sur le port 80 |
| Réseau | port 80 autorisé par UFW sur la VM principale |

La réponse HTTP a été vérifiée depuis l'extérieur sur l'IP publique de la VM
et avec le nom local `cloud.olidev.ovh` défini dans `/etc/hosts`.

## Étape 2 - Créer un rôle Ansible

Depuis le dépôt opérationnel :

```bash
cd /home/oliv/cloud-iam
ansible-galaxy init ansible/roles/web
```

Le rôle doit notamment contenir :

```text
ansible/roles/web/
├── defaults/main.yml
├── handlers/main.yml
├── tasks/main.yml
├── files/site/
└── meta/main.yml
```

Exemple de tâches dans `ansible/roles/web/tasks/main.yml` :

```yaml
---
- name: Installer Nginx
  ansible.builtin.apt:
    name: nginx
    state: present
    update_cache: true

- name: Déployer le site Olidev
  ansible.builtin.copy:
    src: site/
    dest: /var/www/html/
    owner: root
    group: root
    mode: "0644"
  notify: Redémarrer Nginx

- name: Activer et démarrer Nginx
  ansible.builtin.service:
    name: nginx
    state: started
    enabled: true
```

Exemple de handler dans `ansible/roles/web/handlers/main.yml` :

```yaml
---
- name: Redémarrer Nginx
  ansible.builtin.service:
    name: nginx
    state: restarted
```

Le rôle copie le site existant depuis
`ansible/roles/web/files/site/`, notamment `index.html`, les feuilles CSS, le
JavaScript et les images nécessaires.

## Étape 3 - Appeler le rôle depuis le playbook principal

Le rôle est appelé depuis `ansible/playbooks/base-system.yml` :

```yaml
---
- name: Deployer le site web
  ansible.builtin.include_role:
    name: web
```

Vérifier la syntaxe puis exécuter :

```bash
ansible-playbook -i ansible/inventory/ovh.ini \
  ansible/playbooks/base-system.yml --syntax-check

ansible-playbook -i ansible/inventory/ovh.ini \
  ansible/playbooks/base-system.yml
```

Vérifier le service après l'ouverture du port 80 dans UFW :

```bash
ansible -i ansible/inventory/ovh.ini ovh \
  -m ansible.builtin.uri -a 'url=http://127.0.0.1 status_code=200'
```

## Étape 4 - Prouver l'idempotence

Exécuter exactement le même playbook une seconde fois :

```bash
ansible-playbook -i ansible/inventory/ovh.ini \
  ansible/playbooks/base-system.yml
```

La première exécution peut produire des `changed`. La seconde doit produire
`failed=0` et ne doit pas réinstaller ou redémarrer Nginx sans raison. Si le
handler redémarre à chaque passage, vérifier le template, ses attributs et les
notifications.

Preuves à conserver : les deux récapitulatifs Ansible et la réponse HTTP 200.

## Étape 5 - Versionner par étapes logiques

Contrôler les fichiers avant le commit :

```bash
git status --short
git diff --check
git diff -- ansible/
```

Créer des commits compréhensibles, par exemple :

```bash
    git add ansible.cfg ansible/roles/web ansible/playbooks/base-system.yml
git commit -m "Ajouter le role Ansible du service web"

git log --oneline --decorate --graph -10
```

Chaque commit doit correspondre à une étape identifiable : rôle, vérification,
intégration OpenTofu ou sauvegarde. Ne jamais committer `terraform.tfvars`, un
fichier OpenRC, une clé privée, un secret S3 ou un état contenant des données
confidentielles.

## Étape 6 - Sauvegarder la configuration du service

Cette étape dépend du bucket Object Storage créé en 2.5 et des clés S3 associées.
Utiliser un préfixe dédié au service et un nom UTC horodaté :

```bash
backup_name="nginx-config-$(date -u +%Y%m%dT%H%M%SZ).tar.gz"
sudo tar -czf "/tmp/$backup_name" /etc/nginx
sudo chown "$USER:$USER" "/tmp/$backup_name"

aws --profile ovh-s3 \
  --endpoint-url https://s3.gra.io.cloud.ovh.net/ \
  s3 cp "/tmp/$backup_name" \
  "s3://tan-thouless/kit4/nginx/$backup_name"
```

Vérifier la présence et la taille de l'objet :

```bash
aws --profile ovh-s3 \
  --endpoint-url https://s3.gra.io.cloud.ovh.net/ \
  s3api head-object --bucket tan-thouless \
  --key "kit4/nginx/$backup_name"
```

La sortie de `head-object` peut être conservée en preuve, mais jamais les clés
S3. Le nom exact de l'endpoint doit être remplacé par celui fourni par OVH.

## Pour aller plus loin - Durcissement

Ajouter un rôle séparé, par exemple `ansible/roles/hardening`, avec des tâches
pour :

- désactiver l'authentification SSH par mot de passe après validation de la clé ;
- installer les mises à jour de sécurité automatiques ;
- conserver une règle UFW SSH limitée au poste d'administration.

Tester chaque ajout séparément et garder une session SSH de secours ouverte.

## État final attendu

| Point de contrôle | Statut initial |
| --- | --- |
| Rôle Ansible réutilisable | Réalisé |
| Service Nginx déployé | Réalisé sur `dist01b-ovh` |
| Première exécution réussie | Réalisé (`ok=12`, `changed=2`) |
| Deuxième exécution idempotente | Réalisé (`ok=11`, `changed=0`) |
| Vérification HTTP 200 | Réalisé depuis l'IP et `cloud.olidev.ovh` |
| Commits logiques et lisibles | Dépôt local initial déjà créé |
| Sauvegarde horodatée dans S3 | À réaliser |
| Point de restauration Kit 4 | À préparer |

## Preuves à conserver

- arborescence du rôle et playbook appelant ;
- sortie `--syntax-check` ;
- sorties des deux exécutions ;
- contrôle HTTP 200 ;
- `git log --oneline` et messages de commit ;
- `head-object` de la sauvegarde dans le bucket ;
- contrôle Git des fichiers ignorés et absence de secrets.

## Ressources

- [Ansible - rôles](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html)
- [Ansible - idempotence et modules](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html)
- [Ansible Galaxy - init](https://docs.ansible.com/ansible/latest/cli/ansible-galaxy.html)
- [AWS CLI - commande S3](https://docs.aws.amazon.com/cli/latest/reference/s3/)
