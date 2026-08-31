# Automatiser avec Ansible

!!! info "Durée indicative : 30 minutes"
    Cette feuille présente le principe d'idempotence et la structure d'un
    playbook Ansible après la création des VM par OpenTofu.

## Objectif

Comprendre comment Ansible se connecte en SSH à un inventaire de machines et
applique un état attendu avec un playbook.

À la fin, il faut savoir :

- distinguer inventaire, playbook, tâche et module ;
- expliquer l'idempotence ;
- exécuter un playbook sans exposer de secret ;
- vérifier le résultat et conserver une preuve exploitable.

## Principe

OpenTofu crée les ressources d'infrastructure. Ansible intervient ensuite pour
configurer les systèmes : paquets, services, comptes et pare-feu.

Un playbook idempotent décrit un état cible. Une première exécution peut
retourner `changed` lorsqu'elle modifie la machine. Une seconde exécution doit
normalement retourner `ok` sans répéter inutilement les changements.

| Élément | Rôle |
| --- | --- |
| Inventaire | Liste des hôtes et variables de connexion. |
| Playbook | Fichier YAML décrivant les plays et les tâches. |
| Module | Action spécialisée, par exemple `apt` ou `ufw`. |
| Tâche | Appel d'un module avec un état attendu. |
| Idempotence | Résultat stable lorsque le playbook est rejoué. |

## Étape 1 - Préparer l'inventaire

Exemple générique :

```ini
[web]
192.0.2.10 ansible_user=ubuntu
```

Dans le prototype OVH, l'inventaire réel est
`ansible/inventory/ovh.ini`. Les adresses publiques y sont des données
d'exploitation et ne doivent pas être confondues avec des secrets.

Tester d'abord la connexion SSH Ansible :

```bash
ansible -i ansible/inventory/ovh.ini ovh -m ping
```

Résultat attendu : `pong` pour chaque hôte joignable.

!!! warning "Clés et mots de passe"
    Ne pas mettre de mot de passe, de clé privée ou de token dans l'inventaire.
    Utiliser la clé SSH locale et un mécanisme de secrets adapté si une
    authentification supplémentaire est nécessaire.

## Étape 2 - Lire un playbook

Structure minimale :

```yaml
---
- name: Configurer les serveurs web
  hosts: web
  become: true

  tasks:
    - name: Installer nginx
      ansible.builtin.apt:
        name: nginx
        state: present
        update_cache: true
```

`hosts` sélectionne les machines de l'inventaire. `become: true` permet
d'exécuter les tâches avec les privilèges nécessaires. Le module `apt` garantit
que le paquet est présent.

## Étape 3 - Appliquer le socle OVH

Le playbook du prototype est
`ansible/playbooks/base-system.yml`. Il installe les paquets de base et active
UFW avec une politique entrante restrictive. SSH est autorisé uniquement depuis
`admin_ssh_cidr`, défini localement dans l'inventaire.

Vérifier la syntaxe avant l'exécution :

```bash
ansible-playbook -i ansible/inventory/ovh.ini \
  ansible/playbooks/base-system.yml --syntax-check
```

Exécuter ensuite :

```bash
ansible-playbook -i ansible/inventory/ovh.ini \
  ansible/playbooks/base-system.yml
```

!!! danger "Pare-feu et accès SSH"
    Garder une session SSH de secours ouverte pendant une modification UFW.
    Vérifier que l'adresse publique d'administration est correcte avant de
    restreindre SSH.

## Étape 4 - Vérifier l'idempotence

Relancer le même playbook après une première exécution réussie :

```bash
ansible-playbook -i ansible/inventory/ovh.ini \
  ansible/playbooks/base-system.yml
```

Une exécution stable doit montrer peu ou pas de changements. Une tâche qui
retourne toujours `changed` doit être analysée : commande impérative, fichier
réécrit à chaque passage, règle UFW dupliquée ou état mal décrit.

## Avancement réel au 31 août 2026

Une première exécution corrigée sur `dist01b-ovh` a produit :

```text
ok=6    changed=2    unreachable=0    failed=0
```

Les deux changements correspondaient à la suppression de l'ancienne règle SSH
générale et à l'ajout de la règle limitée au poste d'administration. Le contrôle
UFW a confirmé :

```text
Status: active
Default: deny (incoming), allow (outgoing)
22/tcp ALLOW IN 90.38.162.195
```

Après l'ajout des deux petites instances `d2-2`, le test Ansible `ping` a
retourné `pong` pour `dist01b-ovh`, `d2-2-01` et `d2-2-02`. L'application du
playbook sur les trois machines reste la preuve finale à conserver si elle est
réalisée.

## État final attendu

| Point de contrôle | Attendu | Statut |
| --- | --- | --- |
| Inventaire | Hôtes OVH et utilisateur SSH corrects | Réalisé pour les trois VM |
| Connexion Ansible | `pong` pour chaque hôte | Réalisé |
| Syntaxe | `--syntax-check` sans erreur | Réalisé |
| Socle système | Paquets de base présents | Réalisé sur `dist01b-ovh` |
| Pare-feu | UFW actif, entrée refusée par défaut | Réalisé sur `dist01b-ovh` |
| SSH | Limité à l'IP d'administration | Réalisé sur `dist01b-ovh` |
| Idempotence | Seconde exécution sans changements inattendus | À confirmer sur les trois VM |

## Preuves à conserver

- inventaire sans secret ;
- sortie `ansible -m ping` ;
- sortie `--syntax-check` ;
- récapitulatif du playbook avec `failed=0` ;
- sortie UFW montrant la règle SSH limitée ;
- seconde exécution documentant l'idempotence ;
- capture terminal sans mot de passe, clé privée ou token.

## Ressources

- [Ansible - Playbooks](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html)
- [Ansible - Introduction aux modules](https://docs.ansible.com/ansible/latest/module_plugin_guide/modules_intro.html)
