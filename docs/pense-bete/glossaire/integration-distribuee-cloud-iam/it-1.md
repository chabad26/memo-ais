# Glossaire Integration distribuee Cloud & IAM - Iteration 1

## Sujet

Preparation de la migration cloud de l'infrastructure DIST-01a : comparaison
OVHcloud, AWS et Scaleway, analyse des responsabilites cloud, estimation des
couts, cadrage juridique et preparation des outils d'automatisation.

Cette iteration ne deploye pas encore les ressources cloud. Elle prepare les
comptes, les outils, les hypotheses et les livrables de decision.

## Termes a retenir

| Terme | Definition courte |
| --- | --- |
| OVHcloud | Fournisseur cloud europeen utilise comme option principale de souverainete. |
| AWS | Fournisseur cloud non europeen utilise pour comparer l'ecosysteme, les couts et les contraintes juridiques. |
| Scaleway | Fournisseur souverain ajoute comme alternative economique et technique. |
| IaaS | Modele ou le fournisseur gere l'infrastructure physique et la virtualisation, tandis que le client administre les VM, l'OS, les services et les donnees. |
| PaaS | Modele ou le fournisseur gere aussi une partie de la plateforme ou du runtime ; le client garde le code, les donnees, les acces et la configuration. |
| SaaS | Application prete a l'emploi ; le client gere surtout les utilisateurs, les droits, les donnees et les usages. |
| Responsabilite partagee | Frontiere entre ce que securise le fournisseur et ce que le client doit encore configurer, proteger et prouver. |
| Souverainete numerique | Maitrise du lieu, du droit applicable, des dependances fournisseur et des conditions d'acces aux donnees. |
| Cloud Act | Cadre juridique americain a prendre en compte quand un fournisseur comme AWS est retenu. |
| RGPD | Reglement europeen qui encadre les donnees personnelles, les sous-traitants, la localisation et les garanties associees. |
| SLA | Engagement de service a lire avec ses exclusions, conditions et compensations. |
| IAM | Gestion des identites, utilisateurs, groupes, roles, MFA et identites de service. |
| Moindre privilege | Donner uniquement les droits necessaires a chaque utilisateur, role ou service. |
| OpenTofu | Outil d'Infrastructure as Code utilise pour decrire et provisionner les ressources cloud. |
| Ansible | Outil de configuration automatisee utilise apres la creation des machines ou services. |
| Git | Outil de versionnement des livrables, scripts, inventaires et decisions. |
| SOPS | Outil de chiffrement de secrets dans des fichiers versionnes, souvent couple a une cle KMS, age ou GPG. |
| git-crypt | Outil qui chiffre certains fichiers dans un depot Git selon des regles declarees. |
| Secret | Information sensible : mot de passe, token, cle d'API, access key, passphrase ou cle privee. |
| RTO | Duree maximale ou observee avant retour d'un service apres incident. |
| RPO | Perte de donnees maximale ou observee depuis la derniere sauvegarde saine. |

## Manipulations et commandes a retenir

| Manipulation | Commande ou action |
| --- | --- |
| Verifier OVHcloud | Creer ou verifier le compte OVH, puis tester l'API publique avec `curl -s https://api.ovh.com/1.0/ \| head -20`. |
| Verifier AWS | Creer ou verifier le compte AWS, installer l'AWS CLI, puis controler `aws --version` et `aws configure list` sans afficher de secret. |
| Installer OpenTofu | Installer l'outil puis verifier `tofu version`. |
| Installer Ansible | Installer le paquet puis verifier `ansible --version`. |
| Installer Git | Verifier `git --version` et versionner les livrables de migration. |
| Installer git-crypt | Installer l'outil puis verifier `git-crypt --version`. |
| Installer SOPS | Telecharger le binaire, controler le checksum, installer dans `/usr/local/bin/sops`, puis verifier `sops --version`. |
| Classer les services | Distinguer IaaS, PaaS et SaaS pour les composants DIST-01a. |
| Cartographier les dependances | Lister OpenLDAP, LAM, messagerie, Samba, Step CA, BorgBackup, Filebeat, Elasticsearch, Kibana, reseau et volumes. |
| Estimer les couts | Comparer une VM compacte OVHcloud, AWS et Scaleway avec date, region, stockage, egress et options. |
| Lire les SLA | Identifier disponibilite, exclusions, obligations client et compensations. |
| Produire le cadrage | Rediger plan de migration, matrice de decision, note de cadrage et preuves. |

## Points de vigilance

- Ne jamais stocker en clair une Access Key AWS, une Secret Key, un token OVH,
  une passphrase Borg, une cle privee ou un mot de passe dans Git.
- Les captures doivent prouver que les commandes fonctionnent sans exposer les
  secrets ni les moyens de paiement.
- Les prix cloud doivent etre dates : ils dependent de la region, du stockage,
  du trafic sortant, de l'engagement et des options reseau.
- Une VM OVHcloud, une instance AWS EC2 et une offre Scaleway ne sont pas
  strictement equivalentes : comparer CPU, RAM, stockage inclus, architecture
  processeur, SLA et support.
- Avec AWS `t4g.medium`, verifier la compatibilite ARM des images Docker,
  paquets et outils avant de conclure.
- Le cloud ne supprime pas la responsabilite client : IAM, MFA, secrets,
  chiffrement, sauvegardes, pare-feu et donnees restent a maitriser.
- OpenTofu provisionne les ressources ; Ansible configure les systemes. Les deux
  roles ne doivent pas etre confondus dans le dossier de preuves.
- SOPS et git-crypt protegent des fichiers versionnes, mais ne corrigent pas un
  secret deja commite en clair : il faut alors traiter l'historique Git.

## Docs associees

- [Vue d'ensemble Cloud & IAM](../../../integration-distribuee-cloud-iam/README.md)
- [Preparer la migration](../../../integration-distribuee-cloud-iam/it-1/preparer-migration.md)
- [Comprendre les modeles cloud et la responsabilite partagee](../../../integration-distribuee-cloud-iam/it-1/comprendre-modeles-cloud-responsabilite.md)
- [Classer les services et responsabilites](../../../integration-distribuee-cloud-iam/it-1/classer-services-responsabilites.md)
- [Analyser les dependances d'une infrastructure](../../../integration-distribuee-cloud-iam/it-1/analyser-dependances-infrastructure.md)
- [Estimer et comparer les couts de migration](../../../integration-distribuee-cloud-iam/it-1/estimer-comparer-couts-migration.md)
- [Comprendre les enjeux juridiques du choix cloud](../../../integration-distribuee-cloud-iam/it-1/comprendre-enjeux-juridiques-cloud.md)
- [Rediger une note de cadrage de migration](../../../integration-distribuee-cloud-iam/it-1/rediger-note-cadrage-migration.md)
- [Lire et interpreter un SLA cloud](../../../integration-distribuee-cloud-iam/it-1/lire-interpreter-sla-cloud.md)
- [Produire les livrables DIST01b - Plan de migration](../../../integration-distribuee-cloud-iam/it-1/produire-livrables-dist01b-plan-migration.md)
