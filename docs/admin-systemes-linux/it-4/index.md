# Itération 4 - Services Linux et durcissement

## Objectif

Cette itération ouvre la partie **services Linux** du module. L'objectif est de configurer des services utiles à une infrastructure d'entreprise, puis de les sécuriser et de les valider depuis un client.

## Compétences travaillées

- Installer et configurer un service réseau Linux.
- Restreindre l'accès à un service à un sous-réseau précis.
- Contrôler les droits côté serveur et côté client.
- Vérifier les exports, montages et journaux.
- Documenter les preuves d'un service fonctionnel et sécurisé.

## Feuilles de l'itération

| Feuille | Sujet | Résultat attendu |
| --- | --- | --- |
| [NFS AlpesNet](nfs-alpesnet.md) | Partage réseau Linux avec NFS | Répertoire exporté, monté depuis un client, droits testés et `root_squash` vérifié |
| [Samba AlpesNet](samba-alpesnet.md) | Partage SMB/CIFS avec Samba | Partage restreint au groupe `devops`, `alice.martin` autorisée, `bob.dupont` refusé |

## À retenir

Un service réseau ne se valide pas seulement côté serveur. Il faut aussi tester depuis un client, vérifier les droits réels et conserver des preuves : commande, montage, fichier créé, refus attendu.
