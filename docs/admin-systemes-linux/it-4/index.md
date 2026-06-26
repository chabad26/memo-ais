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
| [Durcissement Linux AlpesNet](durcissement-linux-alpesnet.md) | SSH, UFW, Fail2ban et services inutiles | SSH durci, pare-feu actif, bannissement testé et rapport avant/après produit |
| [Rapport de durcissement Linux AlpesNet](rapport-durcissement-linux-alpesnet.md) | Rapport RNCP avant/après | Synthèse des mesures, preuves, résultats et points de vigilance production |
| [Script automatisation Itération 4](script-automatisation-it4.md) | Script Bash de reprise des exercices | Exécution NFS, Samba, durcissement et log final commande/résultat/explication |
| [Rapport automatique Itération 4](rapport-it4-20260626_120855.md) | Rapport généré par le script | Trace automatique des commandes, résultats et explications |

## À retenir

Un service réseau ne se valide pas seulement côté serveur. Il faut aussi tester depuis un client, vérifier les droits réels et conserver des preuves : commande, montage, fichier créé, refus attendu.
