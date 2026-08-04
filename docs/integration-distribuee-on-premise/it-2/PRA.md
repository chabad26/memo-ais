# Plan de Reprise d'Activité (PRA)

**Société :** Embedded Solutions  
**Version :** 1.8.1  
**Date :** Juillet 2021  
**Classification :** Interne  
**Responsable du document :** Responsable Informatique

## 1. Objet

Le présent Plan de Reprise d'Activité (PRA) décrit les opérations permettant de restaurer les principaux services informatiques de l'entreprise après une panne majeure.

Il complète le Plan de Continuité d'Activité (PCA) en détaillant les procédures de remise en service des systèmes.

## 2. Périmètre

Le présent document couvre les services suivants :

- Authentification des utilisateurs
- Partage de fichiers
- Messagerie électronique
- Sauvegardes
- Supervision

Les autres systèmes disposent de procédures spécifiques.

## 3. Priorités de reprise

| Ordre | Service | Délai cible |
| ------- | ---------- | ------------ |
| 1 | Authentification | 2 heures |
| 2 | Partage de fichiers | 8 heures |
| 3 | Sauvegardes | 24 heures |
| 4 | Messagerie | 24 heures |
| 5 | Supervision | 48 heures |

## 4. Conditions de déclenchement

Le PRA peut être déclenché notamment dans les cas suivants :

- panne matérielle d'un serveur ;
- corruption importante des données ;
- indisponibilité prolongée d'un service ;
- sinistre affectant la salle informatique.

La décision appartient au Responsable Informatique.

## 5. Procédure générale

1. Identifier l'origine de l'incident.
2. Informer la Direction.
3. Évaluer les systèmes impactés.
4. Prioriser les opérations de reprise.
5. Restaurer les services selon leur ordre de priorité.
6. Vérifier le bon fonctionnement.
7. Informer les utilisateurs.
8. Clôturer l'incident et documenter les actions réalisées.

## 6. Reprise du contrôleur de domaine

### Préparation

- Vérifier l'état de l'hyperviseur.
- Vérifier la disponibilité des sauvegardes.

### Procédure

1. Restaurer la machine virtuelle du contrôleur de domaine.
2. Démarrer la machine.
3. Vérifier le fonctionnement des services Active Directory.
4. Vérifier la connexion des utilisateurs.
5. Contrôler les journaux d'événements.

## 7. Reprise du serveur de fichiers

### Préparation

- Vérifier la disponibilité du stockage.
- Identifier la dernière sauvegarde disponible.

### Procédure

1. Restaurer la machine virtuelle.
2. Restaurer les données si nécessaire.
3. Vérifier les droits d'accès.
4. Contrôler les partages réseau.
5. Informer les utilisateurs.

## 8. Reprise de la messagerie

### Procédure

1. Restaurer le serveur de messagerie.
2. Vérifier le fonctionnement des services SMTP et IMAP.
3. Tester l'envoi et la réception d'un message.
4. Informer les utilisateurs de la remise en service.

## 9. Reprise du serveur de sauvegarde

### Procédure

1. Restaurer la machine virtuelle.
2. Vérifier l'accès aux sauvegardes existantes.
3. Contrôler la planification des sauvegardes.
4. Lancer une sauvegarde de test.
5. Vérifier les journaux.

## 10. Reprise de la supervision

### Procédure

1. Restaurer le serveur de supervision.
2. Vérifier la collecte des informations.
3. Contrôler l'envoi des alertes.
4. Vérifier les journaux système.

## 11. Vérifications finales

Avant de clôturer l'incident, vérifier :

- les utilisateurs peuvent se connecter ;
- les fichiers sont accessibles ;
- les sauvegardes fonctionnent ;
- la messagerie est opérationnelle ;
- la supervision fonctionne correctement.

Le Responsable Informatique valide la reprise.

## 12. Contacts

| Fonction | Téléphone |
| ---------- | ----------- |
| Responsable Informatique | Voir annuaire interne |
| Direction | Voir annuaire interne |
| Prestataire matériel | Contrat de maintenance |
| Fournisseur Internet | Contrat opérateur |

## 13. Documents associés

- Plan de Continuité d'Activité (PCA)
- Inventaire des serveurs
- Inventaire des sauvegardes
- Contrats de maintenance
- Inventaire matériel

## 14. Révision du document

Le présent document est révisé :

- après chaque exercice de reprise ;
- après chaque incident majeur ;
- après toute évolution importante de l'infrastructure ;
- au minimum une fois par an.

## 15. Historique des versions

| Version | Date | Auteur | Description |
| ---------- | ------ | --------- | ------------- |
| 1.0 | Février 2019 | Service informatique | Création du document |
| 1.5 | Novembre 2020 | Service informatique | Mise à jour des procédures |
| 1.8 | Juin 2021 | Responsable informatique | Révision annuelle |
| 1.8.1 | Juillet 2021 | Responsable informatique | Maj |

## Mise à jour du projet — 3 août 2026

### Reprise de l'annuaire OpenLDAP

L'annuaire OpenLDAP est déployé avec Docker Compose dans ~/on-premise/openldap.

Paramètres à restaurer :

- image osixia/openldap:2.6.10-alpha ;
- base DN dc=embedded,dc=local ;
- DN administrateur cn=admin,dc=embedded,dc=local ;
- port publié 389 vers le port interne 3890 ;
- volumes ldap_data, ldap_config et ldap_backups ;
- variables de configuration et secret administrateur conservés hors du dépôt Git.

### Procédure de reprise

1. Vérifier la disponibilité de Docker et l'espace de stockage.
2. Restaurer compose.yaml, .env depuis l'emplacement protégé et .env.example si nécessaire.
3. Vérifier les volumes LDAP et leur emplacement.
4. Démarrer le service avec docker compose up -d.
5. Vérifier l'état avec docker compose ps.
6. Consulter les journaux avec docker compose logs openldap.
7. Tester l'authentification avec ldapwhoami sur ldap://localhost:3890.
8. Vérifier le contenu de l'annuaire avec ldapsearch sur la base dc=embedded,dc=local.
9. Vérifier que les données et la configuration sont toujours présentes après un redémarrage.
10. Documenter le résultat et faire valider la remise en service.

Commandes de vérification :

~~~bash
docker compose up -d
docker compose ps
docker compose logs openldap
docker compose exec openldap ldapwhoami -x -H ldap://localhost:3890 -D "cn=admin,dc=embedded,dc=local" -W
docker compose exec openldap ldapsearch -x -H ldap://localhost:3890 -D "cn=admin,dc=embedded,dc=local" -W -b "dc=embedded,dc=local" "(objectClass=*)"
~~~

La sauvegarde et la restauration des volumes doivent encore être testées dans un exercice dédié. Une simple recréation du conteneur ne constitue pas une sauvegarde.

**Version de suivi :** 1.9 — août 2026 — ajout de la procédure de reprise OpenLDAP.

## Mise à jour du projet — LDAP Account Manager

LAM est un outil d'administration Web placé devant OpenLDAP. Il n'est pas le stockage de référence : les données et la configuration critiques restent dans OpenLDAP et ses volumes persistants.

### Reprise de LAM

1. Vérifier que le conteneur OpenLDAP est opérationnel.
2. Vérifier que le réseau Docker openldap_default existe.
3. Restaurer le répertoire Compose de LAM et le fichier .env depuis l'emplacement protégé.
4. Démarrer LAM avec docker compose up -d.
5. Vérifier l'accès Web sur http://localhost:8081.
6. Vérifier la connexion à ldap://openldap:3890.
7. Tester la connexion avec le DN administrateur OpenLDAP.
8. Vérifier la consultation et la modification d'un objet de test.
9. Si LAM est indisponible, utiliser ldapsearch et ldapmodify directement.

### Données à restaurer

- compose.yaml ;
- .env ou les paramètres secrets équivalents ;
- la configuration éventuellement enregistrée dans LAM ;
- les volumes OpenLDAP et leurs sauvegardes, qui restent prioritaires.

LAM ne nécessite pas une procédure de restauration de données métier indépendante dans cette configuration. Une reconstruction du conteneur suffit si la configuration peut être rejouée. Le PRA doit toutefois conserver les paramètres de connexion et une preuve de fonctionnement.

Après restauration, vérifier également la présence des unités `ou=People,dc=embedded,dc=local` et `ou=Groups,dc=embedded,dc=local` avant de recréer ou de modifier les comptes utilisateurs et les groupes.

## Vérification de l'annuaire après création — 3 août 2026

L'état de référence validé pour le laboratoire comprend :

- 6 groupes dans `ou=Groups` ;
- 6 utilisateurs dans `ou=People` ;
- les unités de service et d'organisation attendues ;
- une recherche LDAP terminée par `result: 0 Success`.

Après toute reprise, comparer l'annuaire restauré avec cet inventaire, puis
vérifier les identifiants UID/GID et les appartenances aux groupes dans LAM.
Cette preuve valide le fonctionnement courant de l'annuaire ; elle ne remplace
pas un exercice de restauration des volumes `ldap_data`, `ldap_config` et
`ldap_backups`, qui reste à planifier.

## Mise à jour du projet — Reprise de Samba avec OpenLDAP — 4 août 2026

Samba est désormais un serveur autonome dont le backend d'identités est
OpenLDAP. Le contrôleur AD initial n'est pas nécessaire à la reprise de ce
service et ne doit pas être démarré en parallèle.

### Procédure de reprise

1. Restaurer et démarrer OpenLDAP dans `~/on-premise/openldap`.
2. Vérifier le bind de `cn=admin,dc=embedded,dc=local`.
3. Vérifier la présence du schéma `samba` dans `cn=schema,cn=config`.
4. Restaurer les fichiers de `~/on-premise/samba-ad`.
5. Restaurer les volumes `samba_state` et `samba_share`.
6. Construire et démarrer Samba avec `docker compose up -d --build`.
7. Vérifier `testparm -s` et l'état du conteneur.
8. Vérifier la résolution NSS de `amartin` avec `getent passwd amartin`.
9. Vérifier le backend avec `pdbedit -L -b ldapsam:ldap://openldap:3890`.
10. Tester l'authentification et la lecture du partage avec `smbclient`.

### Données critiques

- volumes OpenLDAP `ldap_data`, `ldap_config` et `ldap_backups` ;
- schéma `samba.ldif` ;
- volume Samba `samba_state`, notamment `secrets.tdb` ;
- volume Samba `samba_share` ;
- configurations Compose et `smb.conf` ;
- secrets présents uniquement dans les fichiers locaux protégés.

La perte d'OpenLDAP rend l'authentification Samba indisponible. La reprise doit
donc restaurer l'annuaire avant le serveur SMB.
