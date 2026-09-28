# Concevoir une gestion des clés adaptée à un parc de machines

## Objectif

Passer d'une récupération LUKS réalisée sur une machine isolée à une
architecture capable de gérer les moyens d'ouverture et de récupération de
240 machines pendant tout leur cycle de vie.

Cette feuille constitue une **proposition d'architecture**. Elle ne prouve pas
le déploiement de TPM2, Clevis/Tang ou d'un KMS. Les essais techniques seront
documentés séparément lorsqu'ils auront été réalisés.

## Scénario

| Catégorie | Nombre | Contrainte principale |
| --- | ---: | --- |
| Ordinateurs portables Linux | 150 | Exposition au vol ; interaction humaine possible au démarrage |
| Postes fixes Linux | 40 | Interaction humaine possible ; récupération par le support |
| Serveurs Linux en datacenter | 30 | Redémarrage autonome après une coupure électrique |
| VM Linux dans un cloud public | 20 | Automatisation et dépendance aux services du fournisseur |
| Administrateurs système | 6 | Accès limités, nominatifs et auditables |
| **Total des machines** | **240** | Plusieurs mécanismes adaptés aux usages |

L'entreprise veut chiffrer les données au repos, éviter tout secret commun au
parc, récupérer une machine, révoquer une machine sortante et auditer les
opérations sensibles.

## Partie 1 - Inventorier ce qui doit être géré

| Élément | Portée recommandée | Sensibilité | Usage |
| --- | --- | --- | --- |
| Clé de volume LUKS | Unique par volume | Critique | Chiffrement effectif des données |
| Phrase de passe utilisateur | Individuelle ou propre à la machine | Élevée | Ouverture locale d'un poste |
| Keyslots LUKS | Propres à chaque volume | Critique | Protection des différents moyens d'ouverture |
| Clé de récupération | Unique par machine ou volume | Critique | Secours lorsque l'ouverture normale échoue |
| Sauvegarde du header LUKS | Propre à chaque volume et à son état | Critique | Restauration des métadonnées et keyslots |
| Secret d'ouverture automatique | Unique par machine | Critique | Démarrage autonome d'un serveur |
| Enrôlement TPM2 | Lié à une machine et à sa politique PCR | Élevée | Ouverture conditionnée à l'état mesuré du système |
| Liaison Clevis/Tang | Propre au volume et à la politique | Élevée | Ouverture conditionnée à un service réseau |
| Identifiant KMS ou cloud | Propre à la ressource et au compte technique | Élevée | Autorisation d'utiliser une clé distante |
| Métadonnées d'inventaire | Identifiant machine, volume, UUID, mécanismes | Interne | Exploitation, audit et récupération |
| Journaux d'administration | Événements horodatés et nominatifs | Sensible | Traçabilité et détection d'abus |

### Principes retenus

- une clé de volume et une clé de récupération différentes par machine ;
- aucun secret global partagé par les 240 machines ;
- deux moyens d'ouverture au minimum pour les systèmes critiques ;
- sauvegarde du header hors de la machine chiffrée ;
- séparation entre inventaire, orchestration, stockage des secrets et journaux ;
- accès humain nominatif avec authentification forte ;
- procédures testées avant tout retrait de keyslot.

## Partie 2 - Rôle et limites d'Ansible

Ansible peut installer les paquets, déployer les fichiers de configuration,
exécuter `systemd-cryptenroll` ou Clevis, vérifier les keyslots et remonter un
état d'inventaire.

Ansible ne doit cependant pas devenir le coffre-fort du parc.

| Fonction | Ansible adapté ? | Justification |
| --- | --- | --- |
| Installer `cryptsetup`, Clevis ou les outils TPM2 | Oui | Déploiement reproductible de paquets |
| Appliquer une configuration | Oui | Orchestration et contrôle de conformité |
| Déclencher un enrôlement | Oui, avec contrôle | Exécution coordonnée d'une procédure |
| Inventorier UUID, version LUKS et slots | Oui | Collecte d'informations non secrètes |
| Conserver toutes les clés de récupération en clair | Non | Un dépôt ou un contrôleur compromis exposerait tout le parc |
| Décider seul qui peut récupérer une machine | Non | Cette autorisation relève du contrôle d'accès et de la gouvernance |
| Assurer une preuve d'audit infalsifiable | Non, seul | Les journaux doivent être centralisés et protégés séparément |

Les secrets nécessaires à une automatisation doivent être récupérés à la
demande depuis un coffre-fort ou un KMS, utilisés le moins longtemps possible
et absents des playbooks, sorties de commandes, captures et dépôts Git.

## Partie 3 - Classer les fonctions

| Domaine | Fonctions |
| --- | --- |
| Orchestration | Installation, configuration, enrôlement, vérification, collecte d'inventaire |
| Gestion de clés | Génération, stockage protégé, délivrance contrôlée, rotation, révocation, destruction |
| Contrôle d'accès | Rôles, MFA, approbation, moindre privilège, séparation des responsabilités |
| Continuité | Header sauvegardé, clé de récupération, redondance Tang/KMS, procédure hors ligne |
| Audit | Qui, quoi, quelle machine, quel motif, quelle date, quel résultat |

Confondre ces domaines créerait un point de compromission unique. Par exemple,
un compte Ansible autorisé à déployer une configuration ne doit pas obtenir
automatiquement toutes les clés de récupération.

## Partie 4 - Choisir un mécanisme par catégorie

| Catégorie | Ouverture normale | Récupération | Justification |
| --- | --- | --- | --- |
| Portables Linux | Phrase de passe locale forte, éventuellement TPM2 avec PIN | Clé de récupération unique et header externe | L'utilisateur est présent ; le TPM seul ne protège pas contre une session automatiquement ouverte |
| Postes fixes Linux | Phrase de passe locale ou TPM2 avec PIN | Clé de récupération unique et header externe | Équilibre entre ergonomie et intervention du support |
| Serveurs datacenter | Clevis/Tang redondé ou TPM2 selon le matériel et le modèle de menace | Keyslot de secours, clé de récupération et header externe | Redémarrage autonome nécessaire, avec solution de repli hors du mécanisme automatique |
| VM cloud | KMS du fournisseur avec identité de service et politique restrictive | Clé de récupération dans un coffre-fort distinct et header externe | Le TPM physique local n'est pas toujours disponible ou pertinent ; intégration aux identités cloud |

Un seul mécanisme n'est pas imposé à tout le parc. Le niveau d'automatisation,
le risque de vol, la disponibilité réseau et les possibilités matérielles sont
différents selon les catégories.

## Partie 5 - Évaluer TPM2 et systemd-cryptenroll

Un TPM2 peut protéger un secret lié à un volume LUKS et ne le libérer que si la
politique définie est satisfaite. `systemd-cryptenroll` permet d'ajouter ce
moyen d'ouverture dans un token ou un keyslot LUKS2.

Avant de généraliser TPM2, il faut vérifier :

| Question | Réponse attendue avant déploiement |
| --- | --- |
| Toutes les machines disposent-elles d'un TPM2 utilisable ? | Inventaire matériel et firmware nécessaire |
| Les VM exposent-elles un vTPM persistant ? | Validation par plateforme et par cycle de vie de la VM |
| Quels PCR sont utilisés ? | Politique documentée et testée après mises à jour |
| Une mise à jour firmware ou bootloader bloque-t-elle l'ouverture ? | Tests de non-régression et procédure de secours obligatoires |
| Que se passe-t-il après remplacement de la carte mère ? | Récupération par un keyslot indépendant du TPM |
| Le TPM permet-il un redémarrage sans interaction ? | Oui selon la politique, mais cela modifie le modèle de menace |
| Comment révoquer l'ancien enrôlement ? | Retrait contrôlé du token ou keyslot après validation du nouveau moyen |

TPM2 n'est donc pas une sauvegarde. Une clé de récupération indépendante et un
header sauvegardé restent nécessaires.

## Partie 6 - Évaluer Clevis/Tang

Clevis applique côté client une politique d'ouverture. Tang participe au
déverrouillage lorsque le client peut joindre le service réseau prévu. Le
serveur Tang n'a pas vocation à stocker directement les phrases de passe LUKS
de toutes les machines.

| Aspect | Analyse |
| --- | --- |
| Avantage | Redémarrage automatique limité au réseau autorisé |
| Dépendance | Réseau, DNS ou routage et disponibilité des serveurs Tang |
| Disponibilité | Au moins deux instances et une politique tolérant la perte d'une instance |
| Cloisonnement | Tang dans un segment d'administration protégé, non exposé publiquement |
| Secours | Keyslot avec clé de récupération indépendante de Tang |
| Révocation | Retirer ou remplacer la liaison Clevis sur le volume concerné |
| Audit | Corréler les demandes réseau, les changements de politiques et les opérations LUKS |

Une panne Tang ne doit pas rendre tout le datacenter impossible à redémarrer.
La haute disponibilité et la procédure manuelle de secours doivent être testées.

## Partie 7 - Architecture proposée

```text
                         Équipe de 6 administrateurs
                     comptes nominatifs + MFA + bastion
                                  |
                 +----------------+----------------+
                 |                                 |
          Orchestration Ansible              Coffre-fort / KMS
      configuration et inventaire       clés de récupération uniques
                 |                       headers LUKS chiffrés
                 |                                 |
    +------------+-------------+                   |
    |                          |                    |
190 postes                 30 serveurs          20 VM cloud
LUKS2                      LUKS2                LUKS2 / chiffrement cloud
phrase locale              Clevis/Tang          KMS + identité de service
ou TPM2 + PIN              ou TPM2              politiques cloud
    |                          |                    |
    +------------+-------------+--------------------+
                 |
        Journalisation centralisée
   SIEM / stockage protégé et horodaté
```

### Composants

| Composant | Rôle | Protection attendue |
| --- | --- | --- |
| Inventaire central | Associer machine, propriétaire, UUID LUKS, méthode et état | Écriture limitée, historique des changements |
| Contrôleur Ansible | Déployer et vérifier | Compte technique limité, aucun secret permanent en clair |
| Coffre-fort | Conserver clés de récupération et headers | Chiffrement, MFA, rôles, double approbation, sauvegarde |
| Tang redondé | Autoriser l'ouverture réseau des serveurs | Segmentation, supervision, sauvegarde de configuration |
| KMS cloud | Fournir les clés ou autorisations aux VM | Identités de service, politiques minimales, journaux natifs |
| Collecteur de journaux | Centraliser les événements | Accès en lecture contrôlé, rétention et intégrité |

## Partie 8 - Répartir les rôles

| Rôle | Autorisations | Interdictions principales |
| --- | --- | --- |
| Administrateur poste | Enrôler et vérifier les postes de son périmètre | Lire toutes les clés de récupération |
| Administrateur serveur | Gérer Clevis/TPM2 sur les serveurs autorisés | Modifier seul le coffre-fort et ses journaux |
| Opérateur récupération | Demander une clé pour une machine identifiée | Exporter en masse les secrets |
| Responsable sécurité | Approuver une récupération sensible, auditer | Utiliser quotidiennement les comptes d'exploitation |
| Automate Ansible | Installer, configurer et inventorier | Accès permanent à l'ensemble des clés |
| Auditeur | Lire inventaire et journaux | Modifier les volumes, secrets ou politiques |

Une récupération de serveur critique nécessite une demande avec motif et une
approbation par une seconde personne. Les six administrateurs n'obtiennent pas
tous les mêmes droits par défaut.

## Partie 9 - Décrire le cycle de vie

### Génération et enrôlement

1. créer une clé de volume propre à LUKS avec le générateur du système ;
2. générer une clé de récupération unique dans le coffre-fort ;
3. ajouter le mécanisme normal dans un keyslot distinct ;
4. tester les deux moyens avant tout retrait ;
5. sauvegarder le header après la configuration finale ;
6. enregistrer uniquement les métadonnées nécessaires dans l'inventaire.

### Déploiement

Ansible installe les dépendances, applique la politique de la catégorie,
contrôle LUKS2 et remonte l'UUID ainsi que les mécanismes présents. Les secrets
sont fournis à la demande par le coffre-fort sans apparaître dans les journaux.

### Ouverture normale

- postes : interaction locale ou TPM2 avec PIN ;
- serveurs : politique Clevis/Tang ou TPM2 testée ;
- cloud : identité de service autorisée par le KMS.

### Récupération

1. ouvrir un ticket lié à la machine et à l'incident ;
2. faire approuver l'opération selon sa criticité ;
3. récupérer le header ou la clé strictement nécessaire ;
4. restaurer ou ouvrir le volume sur un poste contrôlé ;
5. vérifier les données ;
6. faire tourner le moyen exposé et sauvegarder le nouveau header ;
7. fermer le ticket avec les preuves non secrètes.

### Rotation et révocation

Ajouter le nouveau moyen, le tester, puis supprimer l'ancien keyslot. Une
rotation de phrase, de token ou de clé de récupération ne signifie pas
nécessairement rechiffrer tous les blocs du volume.

### Sortie du parc

Retirer les identités et mécanismes d'ouverture, révoquer les autorisations
KMS, effacer les clés locales, traiter les sauvegardes selon la politique de
rétention et mettre à jour l'inventaire. Le support est ensuite effacé ou
détruit selon sa destination.

## Partie 10 - Journaliser et auditer

| Événement à conserver | Informations minimales |
| --- | --- |
| Enrôlement | Machine, volume, mécanisme, opérateur, date, résultat |
| Ajout ou retrait d'un keyslot | UUID LUKS, numéro de slot, ticket, opérateur, résultat |
| Consultation d'une clé de récupération | Demandeur, approbateur, machine, motif, heure |
| Restauration d'un header | Machine, empreinte du fichier, opérateur, résultat |
| Changement TPM2, Tang ou KMS | Ancienne et nouvelle politique, approbation, date |
| Échec d'ouverture automatique | Machine, mécanisme, cause connue, action engagée |
| Révocation ou sortie du parc | Machine, secrets retirés, support traité, validation |

Les journaux ne doivent contenir ni phrase de passe, ni clé, ni contenu du
header. Ils doivent être centralisés, horodatés, protégés contre la modification
et conservés selon une durée définie.

## Partie 11 - Répondre aux incidents

| Incident | Réponse de l'architecture |
| --- | --- |
| TPM indisponible ou carte mère remplacée | Utiliser la clé de récupération, enrôler le nouveau TPM, tester puis retirer l'ancien token. |
| Panne réseau au démarrage | Utiliser le secours local autorisé ; rétablir le réseau avant de réenrôler. |
| Un serveur Tang indisponible | La politique redondée utilise l'autre instance ; sinon procédure de récupération approuvée. |
| Perte ou corruption du header | Restaurer la sauvegarde correspondant exactement à l'UUID, puis vérifier et renouveler les moyens exposés. |
| Départ d'un administrateur | Désactiver son compte nominatif, révoquer ses sessions et revoir les secrets auxquels il a accédé. |
| Machine retirée du parc | Révoquer KMS/Tang/identité, supprimer l'inventaire actif et effacer ou détruire le support. |
| Indisponibilité du KMS cloud | Utiliser la redondance prévue par le fournisseur ou la procédure de reprise ; ne pas contourner le contrôle avec une clé en clair. |
| Compromission du contrôleur Ansible | Isoler le contrôleur, révoquer son identité, analyser les déploiements et faire tourner les secrets accessibles. |

## Risques résiduels

| Risque | Réduction prévue |
| --- | --- |
| Coffre-fort indisponible | Redondance, sauvegarde testée et procédure de continuité |
| Compte privilégié compromis | MFA, bastion, droits limités, alertes et double approbation |
| Mauvaise cible lors d'une opération LUKS | Contrôle UUID, inventaire, prévisualisation et validation humaine |
| Header sauvegardé obsolète | Nouvelle sauvegarde après chaque changement de keyslot |
| Dépendance réseau excessive | Secours indépendant et tests de panne réguliers |
| Secret dans un log ou Git | Masquage des sorties, coffre-fort, revue et détection de secrets |

## Livrable synthétique

L'architecture proposée distingue trois familles d'ouverture : interaction
locale pour les postes, ouverture automatique contrôlée pour les serveurs et
KMS avec identité de service pour le cloud. Chaque volume conserve un moyen de
récupération unique et indépendant. Les headers et clés de récupération sont
stockés dans un coffre-fort séparé, accessible par rôles et sous contrôle
d'audit.

Ansible orchestre le parc mais ne détient pas durablement les secrets. Les
opérations sensibles sont nominatives, approuvées, journalisées et suivies
d'une rotation lorsque le secret a été exposé. Cette combinaison répond au
besoin de disponibilité sans créer un secret commun aux 240 machines.

- [Glossaire de l'itération 5](../../pense-bete/glossaire/securite-donnees/it-5.md)
