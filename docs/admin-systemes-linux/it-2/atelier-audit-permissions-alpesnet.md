# Atelier - Audit des permissions AlpesNet

## Objectif

Auditer les permissions sur `/srv/alpesnet` et `/var/log/alpesnet`, identifier les écarts au principe du moindre privilège, les corriger et documenter chaque action.

L'audit doit répondre à quatre questions :

1. Qui possède chaque répertoire ?
2. Quel groupe peut y accéder ?
3. Quelles permissions POSIX sont appliquées ?
4. Quelles ACL éventuelles modifient les droits de base ?

## Consigne

Le DSI d'AlpesNet transmet le message suivant :

> Avant la mise en production, j'ai besoin d'un audit complet des permissions sur `/srv/alpesnet` et `/var/log/alpesnet`. Le prestataire a laissé la structure mais je ne suis pas sûr que tout soit correct.

Travail à réaliser :

- auditer les permissions de tous les répertoires `/srv/alpesnet/*` et `/var/log/alpesnet` ;
- pour chaque répertoire, noter le propriétaire, le groupe, les permissions et les ACL éventuelles ;
- identifier chaque écart au principe du moindre privilège ;
- justifier pourquoi chaque écart est un problème ;
- corriger les écarts ;
- documenter chaque correction avec l'état avant, la commande appliquée et l'état après.

## Étape 1 - Préparer le fichier d'audit

Créer un fichier de rapport :

```bash
nano audit-permissions-alpesnet.txt
```

En-tête standard :

```text
Nom :
Prénom :
Site : AlpesNet
Module : Administration des systèmes - Linux
Atelier : Audit des permissions AlpesNet
Date :
Machine : srv-[prenom]
Distribution : Debian GNU/Linux 12 (bookworm)
Périmètre : /srv/alpesnet et /var/log/alpesnet
```

## Étape 2 - Lister les chemins à auditer

Commande :

```bash
find /srv/alpesnet /var/log/alpesnet -maxdepth 1 -type d -print
```

Résultat attendu :

```text
/srv/alpesnet
/srv/alpesnet/projets
/srv/alpesnet/logs
/srv/alpesnet/secrets
/srv/alpesnet/web
/var/log/alpesnet
```

À documenter : vérifier que tous les répertoires attendus sont présents.

## Étape 3 - Relever les permissions POSIX

Commande :

```bash
ls -ld /srv/alpesnet /srv/alpesnet/* /var/log/alpesnet
```

Commande plus détaillée :

```bash
stat -c '%A %a %U %G %n' /srv/alpesnet /srv/alpesnet/* /var/log/alpesnet
```

À recopier dans le rapport :

| Chemin | Propriétaire | Groupe | Mode octal | Permissions | Conforme ? |
| --- | --- | --- | --- | --- | --- |
| `/srv/alpesnet` | à relever | à relever | à relever | à relever | à décider |
| `/srv/alpesnet/projets` | à relever | à relever | à relever | à relever | à décider |
| `/srv/alpesnet/logs` | à relever | à relever | à relever | à relever | à décider |
| `/srv/alpesnet/secrets` | à relever | à relever | à relever | à relever | à décider |
| `/srv/alpesnet/web` | à relever | à relever | à relever | à relever | à décider |
| `/var/log/alpesnet` | à relever | à relever | à relever | à relever | à décider |

## Étape 4 - Relever les ACL

Commande :

```bash
getfacl /srv/alpesnet /srv/alpesnet/* /var/log/alpesnet
```

Pour sauvegarder la preuve complète :

```bash
mkdir -p ~/audit-alpesnet
getfacl -R /srv/alpesnet /var/log/alpesnet > ~/audit-alpesnet/acl-audit-avant.txt
```

À documenter pour chaque répertoire :

- ACL utilisateur nommée, par exemple `user:bob.dupont:r-x` ;
- ACL groupe nommée, par exemple `group:readonly:r-x` ;
- ligne `mask::` ;
- ACL par défaut, par exemple `default:user:bob.dupont:r-x`.

## Étape 5 - Définir l'état attendu

État attendu pour l'infrastructure AlpesNet :

| Chemin | Propriétaire:groupe attendu | Mode attendu | ACL attendue | Justification |
| --- | --- | --- | --- | --- |
| `/srv/alpesnet` | `root:root` | `755` | aucune obligatoire | Racine de service traversable pour atteindre les sous-répertoires |
| `/srv/alpesnet/projets` | `alice.martin:devops` | `750` | `user:bob.dupont:r-x` possible | Projets gérés par Alice et DevOps, Bob en lecture seulement |
| `/srv/alpesnet/logs` | `root:adm` | `750` | `group:readonly:r-x` possible | Logs consultables par un groupe autorisé, écriture réservée |
| `/srv/alpesnet/secrets` | `root:root` | `700` | aucune | Données sensibles réservées à root |
| `/srv/alpesnet/web` | `www-nginx:www-nginx` | `755` | aucune obligatoire | Contenu web lisible, écriture réservée au service |
| `/var/log/alpesnet` | `root:adm` | `750` | aucune obligatoire | Logs dédiés consultables par `adm`, non accessibles aux autres |

!!! note "ACL attendues"
    Une ACL n'est pas mauvaise en soi. Elle doit simplement être minimale, lisible et justifiée.

## Étape 6 - Identifier les écarts

Comparer l'état observé avec l'état attendu.

Exemples d'écarts :

| Écart | Pourquoi c'est un problème |
| --- | --- |
| Mode `777` | Tout le monde peut lire, écrire et entrer : aucun moindre privilège |
| Mode `755` sur `secrets` | Les autres utilisateurs peuvent lire ou traverser un répertoire sensible |
| Propriétaire incorrect sur `web` | Le service web peut ne pas pouvoir écrire ou un mauvais compte possède le contenu |
| Groupe trop large sur `logs` | Des utilisateurs non concernés peuvent consulter des journaux |
| ACL `user:bob.dupont:rwx` sur `projets` | Bob peut écrire alors qu'il doit seulement lire |
| ACL `other::r-x` sur un répertoire sensible | Tous les comptes locaux peuvent accéder au contenu |

Modèle à remplir :

```text
Chemin :
État observé :
Écart :
Risque :
Correction prévue :
```

## Étape 7 - Corriger les permissions POSIX

Appliquer uniquement les corrections nécessaires.

Commandes de référence :

```bash
sudo chown root:root /srv/alpesnet
sudo chmod 755 /srv/alpesnet

sudo chown alice.martin:devops /srv/alpesnet/projets
sudo chmod 750 /srv/alpesnet/projets

sudo chown root:adm /srv/alpesnet/logs
sudo chmod 750 /srv/alpesnet/logs

sudo chown root:root /srv/alpesnet/secrets
sudo chmod 700 /srv/alpesnet/secrets

sudo chown www-nginx:www-nginx /srv/alpesnet/web
sudo chmod 755 /srv/alpesnet/web

sudo chown root:adm /var/log/alpesnet
sudo chmod 750 /var/log/alpesnet
```

!!! warning "Correction ciblée"
    Ne pas appliquer aveuglément toutes les commandes si un élément est déjà conforme. Dans le rapport, indiquer uniquement les corrections réellement nécessaires.

## Étape 8 - Corriger les ACL si nécessaire

ACL attendue pour Bob sur `projets` :

```bash
sudo setfacl -m u:bob.dupont:rx /srv/alpesnet/projets
```

ACL attendue pour le groupe `readonly` sur `logs` :

```bash
sudo setfacl -m g:readonly:r-x /srv/alpesnet/logs
```

Supprimer une ACL trop large :

```bash
sudo setfacl -x u:nom_utilisateur /chemin
sudo setfacl -x g:nom_groupe /chemin
```

Supprimer toutes les ACL étendues d'un chemin si elles sont injustifiées :

```bash
sudo setfacl -b /chemin
```

Vérifier :

```bash
getfacl /srv/alpesnet/projets
getfacl /srv/alpesnet/logs
```

## Étape 9 - Vérifier l'état final

Commandes :

```bash
stat -c '%A %a %U %G %n' /srv/alpesnet /srv/alpesnet/* /var/log/alpesnet
getfacl /srv/alpesnet /srv/alpesnet/* /var/log/alpesnet
```

Sauvegarder l'état final :

```bash
getfacl -R /srv/alpesnet /var/log/alpesnet > ~/audit-alpesnet/acl-audit-apres.txt
stat -c '%A %a %U %G %n' /srv/alpesnet /srv/alpesnet/* /var/log/alpesnet > ~/audit-alpesnet/permissions-audit-apres.txt
```

Point de contrôle :

- les modes POSIX correspondent à l'état attendu ;
- les propriétaires et groupes sont cohérents ;
- les ACL présentes sont justifiées ;
- les autres utilisateurs n'ont pas de droits inutiles ;
- les répertoires sensibles ne sont pas accessibles à tous.

## Étape 10 - Documenter chaque correction

Pour chaque correction, écrire :

```text
Correction n° :
Chemin :
État avant :
Écart identifié :
Risque :
Commande appliquée :
État après :
Vérification :
Conclusion :
```

Exemple :

```text
Correction n°1
Chemin : /srv/alpesnet/secrets
État avant : drwxr-xr-x root root /srv/alpesnet/secrets
Écart identifié : le répertoire secrets est lisible/traversable par tous.
Risque : un utilisateur non autorisé peut accéder à des informations sensibles.
Commande appliquée : sudo chmod 700 /srv/alpesnet/secrets
État après : drwx------ root root /srv/alpesnet/secrets
Vérification : stat -c '%A %a %U %G %n' /srv/alpesnet/secrets
Conclusion : l'accès est limité à root, conforme au moindre privilège.
```

## Résultat attendu

Le rapport d'audit doit contenir :

- la liste des répertoires audités ;
- les permissions POSIX avant correction ;
- les ACL avant correction ;
- les écarts identifiés ;
- une justification du risque pour chaque écart ;
- les corrections appliquées ;
- les permissions et ACL après correction ;
- une conclusion de conformité.

Conclusion type :

```text
Après audit et correction, les permissions de /srv/alpesnet et /var/log/alpesnet respectent le principe du moindre privilège. Les droits POSIX sont cohérents avec les rôles des comptes et services. Les ACL restantes sont limitées et justifiées.
```
