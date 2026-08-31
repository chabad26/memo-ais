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

- un inventaire OVH pour `dist01b-ovh`, `d2-2-01` et `d2-2-02` ;
- le playbook plat `ansible/playbooks/base-system.yml` ;
- une clé SSH et des VM joignables par Ansible ;
- un dépôt Git local initialisé avec un premier commit.

Le déploiement d'un service Nginx, le découpage en rôles et l'envoi vers le
bucket restent à exécuter et à prouver. Le backend S3 de l'état OpenTofu doit
être opérationnel avant de considérer le stockage comme une preuve finale.

## Étape 1 - Choisir et définir le service

Pour cet exercice, le service cible est Nginx :

| Élément | État attendu |
| --- | --- |
| Paquet | `nginx` installé par Ansible |
| Service | `nginx` démarré et activé |
| Contenu | page d'accueil de démonstration versionnée |
| Vérification | réponse HTTP locale sur le port 80 |
| Réseau | port 80 non publié par UFW dans le prototype actuel |

Le port 80 peut rester fermé depuis Internet : la vérification peut être faite
localement sur la VM avec `curl http://127.0.0.1` ou avec le module Ansible
`uri`.

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
├── templates/
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

- name: Déployer la page du service
  ansible.builtin.template:
    src: index.html.j2
    dest: /var/www/html/index.html
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

Exemple de template `ansible/roles/web/templates/index.html.j2` :

```html
<!doctype html>
<html lang="fr">
  <head><meta charset="utf-8"><title>DIST-01b</title></head>
  <body><h1>Service web OVH</h1><p>Déployé par Ansible.</p></body>
</html>
```

## Étape 3 - Appeler le rôle depuis un playbook

Créer `ansible/playbooks/web-service.yml` :

```yaml
---
- name: Déployer le service web DIST-01b
  hosts: ovh
  become: true
  roles:
    - web
```

Vérifier la syntaxe puis exécuter :

```bash
ansible-playbook -i ansible/inventory/ovh.ini \
  ansible/playbooks/web-service.yml --syntax-check

ansible-playbook -i ansible/inventory/ovh.ini \
  ansible/playbooks/web-service.yml
```

Vérifier le service sans ouvrir le port 80 dans le Security Group ou UFW :

```bash
ansible -i ansible/inventory/ovh.ini ovh \
  -m ansible.builtin.uri -a 'url=http://127.0.0.1 status_code=200'
```

## Étape 4 - Prouver l'idempotence

Exécuter exactement le même playbook une seconde fois :

```bash
ansible-playbook -i ansible/inventory/ovh.ini \
  ansible/playbooks/web-service.yml
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
git add ansible/roles/web ansible/playbooks/web-service.yml
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
  "s3://NOM_DU_BUCKET/kit4/nginx/$backup_name"
```

Vérifier la présence et la taille de l'objet :

```bash
aws --profile ovh-s3 \
  --endpoint-url https://s3.gra.io.cloud.ovh.net/ \
  s3api head-object --bucket NOM_DU_BUCKET \
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
| Rôle Ansible réutilisable | À réaliser |
| Service Nginx déployé | À réaliser |
| Première exécution réussie | À prouver |
| Deuxième exécution idempotente | À prouver |
| Vérification HTTP 200 | À prouver |
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
