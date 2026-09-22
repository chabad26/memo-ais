# Retrouver la cryptographie dans les services administrés

## Objectif

Vous connaissez maintenant les principales briques de la cryptographie. Cette
activité consiste à les retrouver dans des services, protocoles et mécanismes
déjà utilisés ou administrés pendant la formation.

L'inventaire doit répondre à trois questions :

1. Où utilise-t-on de la cryptographie ?
2. Pourquoi l'utilise-t-on ?
3. Quelles briques cryptographiques sont mobilisées ?

Il sera réutilisé pour les activités sur TLS, le chiffrement des données au
repos et la gestion des clés.

> Ne cherchez pas immédiatement le nom exact de tous les algorithmes. Si une
> information n'est pas démontrée par la configuration, indiquez `?` plutôt que
> de la deviner.

## Périmètre étudié

L'inventaire s'appuie sur les travaux déjà réalisés dans :

- `integration-distribuee-on-premise` ;
- `Modules/on-premise`, notamment Docker Compose, la PKI et BorgBackup ;
- `integration-distribuee-cloud-iam` ;
- `Modules/cloud-iam`, notamment Ansible, OpenTofu, SSH et SOPS.

Les chemins ci-dessous désignent les fichiers de référence du laboratoire :

| Sujet | Fichiers à consulter |
| --- | --- |
| PKI interne | `pki/README.md`, `pki/scripts/issue-service-certificates.sh`, `documentation/pki-architecture.md` |
| TLS OpenLDAP | `infrastructure-compose/compose.yaml`, `infrastructure-compose/prepare-openldap-tls.sh` |
| TLS messagerie | `messaging-compose/docker-compose.yml`, `messaging-compose/dovecot/dovecot.conf`, `messaging-compose/prepare-tls-volumes.sh` |
| Sauvegardes | `backup/backup.sh`, `backup/README.md`, `documentation/backup-implementation.md` |
| Déploiement cloud | `cloud-iam/ansible/playbooks/base-system.yml`, `deploy-on-premise.yml` |
| Secrets cloud | `cloud-iam/.sops.yaml`, `cloud-iam/secrets/cloud-lab.env` |

## Partie 1 - Inventorier les services

Pour chaque service, cochez uniquement les mécanismes que vous pouvez justifier
à partir d'une configuration, d'une commande ou de votre expérience. Un même
service peut utiliser plusieurs briques.

| Service ou mécanisme | Aléa | Symétrique | Asymétrique | Hash | MAC | Signature | Certificat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SSH / Ansible | Oui | ? | Oui | ? | ? | Oui | ? |
| LDAPS OpenLDAP | Oui | Oui | Oui | ? | ? | Oui | Oui |
| IMAPS Dovecot | Oui | Oui | Oui | ? | ? | Oui | Oui |
| SMTP STARTTLS Postfix | Oui | Oui | Oui | ? | ? | Oui | Oui |
| HTTPS Roundcube / Nginx | Oui | Oui | Oui | ? | ? | Oui | Oui |
| Sauvegarde BorgBackup | ? | Oui | ? | ? | ? | ? | ? |
| Secrets SOPS / age | Oui | Oui | Oui | Oui | ? | Oui | ? |
| Mots de passe LDAP | ? | ? | ? | Oui | ? | ? | ? |
| Mises à jour APT | ? | ? | ? | Oui | ? | Oui | ? |
| Wi-Fi ou VPN étudié précédemment | ? | ? | ? | ? | ? | ? | ? |

### Ce que montrent les fichiers

- La PKI `Campus CA` délivre des certificats distincts pour OpenLDAP, Postfix,
  Dovecot, Roundcube et d'autres services prévus.
- OpenLDAP présente `openldap.fullchain.crt` et `openldap.key`, tandis que les
  clients utilisent `Campus-CA-root.crt` pour vérifier la chaîne de confiance.
- Dovecot impose TLS, désactive l'authentification en clair et utilise au
  minimum TLS 1.2.
- Postfix utilise STARTTLS et interdit l'authentification SMTP en clair.
- Borg initialise le dépôt avec `--encryption=repokey` et protège l'accès par
  une phrase secrète ; l'algorithme exact doit être vérifié dans la version de
  Borg utilisée.
- Le fichier `cloud-lab.env` est chiffré par SOPS avec AES-256-GCM et une clé
  de chiffrement age. La clé privée age n'est pas stockée dans le dépôt.

### Ajoutez vos exemples

Pour chaque exemple ajouté, notez :

- **Service ou mécanisme :**
- **Pourquoi la cryptographie est-elle utilisée ?**
- **Brique à confirmer :**

## Partie 2 - Identifier les propriétés protégées

Reprenez les services de votre inventaire et indiquez les propriétés de la
triade CIA concernées. Ajoutez l'authenticité lorsque l'identité d'un service,
d'un utilisateur ou de l'émetteur est vérifiée.

| Service ou mécanisme | Confidentialité | Intégrité | Disponibilité | Authenticité |
| --- | --- | --- | --- | --- |
| SSH / Ansible | Oui | Oui | ? | Oui |
| LDAPS OpenLDAP | Oui | Oui | ? | Oui |
| IMAPS / SMTP STARTTLS | Oui | Oui | ? | Oui |
| HTTPS Roundcube | Oui | Oui | ? | Oui |
| Sauvegarde BorgBackup | Oui | Oui | Oui | ? |
| Secrets SOPS / age | Oui | Oui | ? | Oui |

Toutes les propriétés ne sont pas assurées directement par la cryptographie.
Par exemple, la disponibilité dépend également des sauvegardes, du
renouvellement des certificats, de la conservation des clés et du fonctionnement
des services.

### Question de réflexion

Dans quelles situations l'utilisation de la cryptographie peut-elle créer un
problème de disponibilité ?

Exemples à examiner :

- perte de la phrase secrète ou de la clé exportée d'un dépôt Borg ;
- expiration d'un certificat TLS ;
- perte de la clé privée d'une autorité de certification ;
- impossibilité de déchiffrer le fichier SOPS ;
- corruption ou indisponibilité d'un magasin de clés.

Réponse :

................................................................................

................................................................................

## Partie 3 - Identifier les clés et secrets

Pour quelques services, identifiez le secret ou la clé, son emplacement et les
personnes ou services qui doivent y accéder.

| Service / mécanisme | Clé ou secret | Emplacement observé ou prévu | Accès nécessaire |
| --- | --- | --- | --- |
| OpenLDAP TLS | Clé privée `openldap.key` | Volume Docker `openldap_tls`, exclu de Git | OpenLDAP et administrateurs autorisés |
| Campus CA | Clé privée de CA / secret de provisionneur | Hors dépôt, dans l'environnement Step CA | Administrateurs PKI autorisés |
| BorgBackup | Clé `repokey` et phrase secrète | Dépôt Borg et emplacement de secours séparé | Administrateurs de sauvegarde |
| SOPS / age | Clé privée age | Poste ou coffre de l'administrateur | Administrateurs autorisés à déchiffrer |
| SSH / Ansible | Clé privée SSH | Poste d'administration, hors dépôt | Administrateur et client SSH |
| Postfix / Dovecot | Clés privées TLS | Volumes Docker dédiés, droits `600` | Service concerné |

À compléter pour chaque ligne :

- que se passe-t-il si la clé est perdue ?
- que se passe-t-il si elle est compromise ?
- existe-t-il une procédure de renouvellement ou de récupération ?

Si la réponse n'est pas connue, utilisez `?` et indiquez le fichier ou la
commande qui permettra de la vérifier.

## Partie 4 - Étudier trois services

Choisissez trois services utilisant la cryptographie de manière différente.
Les trois exemples suivants constituent un point de départ directement relié
aux modules précédents.

### Exemple A - LDAPS et la PKI Campus CA

1. **Service :** OpenLDAP, accessible en LDAPS sur le port 636.
2. **Propriété recherchée :** confidentialité des échanges, intégrité du flux
   et authenticité du serveur.
3. **Briques :** aléa de session, chiffrement symétrique de la session,
   cryptographie asymétrique, signature et certificat X.509.
4. **Clés à protéger :** `openldap.key`, clé intermédiaire et clés de la CA.
5. **Clé perdue :** le service ne peut plus présenter son identité ; il faut
   réémettre ou restaurer le certificat et la clé selon la procédure prévue.
6. **Clé compromise :** un attaquant peut usurper le service jusqu'à révocation
   et remplacement du certificat.

À vérifier dans la configuration : chaîne `Campus CA`, SAN du certificat,
validation côté client et procédure de révocation.

### Exemple B - Sauvegarde BorgBackup

1. **Service :** dépôt Borg `/home/oliv/borg-infrastructure-backup`.
2. **Propriété recherchée :** confidentialité et intégrité des sauvegardes,
   avec disponibilité lors d'une restauration.
3. **Briques :** chiffrement symétrique du dépôt ; hash, MAC ou mécanismes
   internes de vérification à confirmer dans la version de Borg.
4. **Clés à protéger :** clé `repokey`, phrase secrète et clé exportée.
5. **Clé perdue :** les archives peuvent devenir irrécupérables, même si le
   dépôt est encore présent.
6. **Clé compromise :** un attaquant peut tenter de lire ou de manipuler les
   sauvegardes selon les accès qu'il possède au dépôt.

À vérifier dans la configuration : `borg key export`, séparation de la clé et
du dépôt, droits du fichier `.env`, tests de restauration et résultat de
`borg check`.

### Exemple C - Secrets SOPS / age et administration Ansible

1. **Service :** gestion des variables sensibles de l'infrastructure cloud.
2. **Propriété recherchée :** confidentialité des identifiants OVH et
   intégrité du fichier de secrets.
3. **Briques :** AES-256-GCM pour les valeurs chiffrées et age pour protéger la
   clé de données ; les signatures et l'authentification SSH sont à distinguer
   de ce chiffrement.
4. **Clés à protéger :** clé privée age, clés SSH privées, OpenRC et variables
   OpenTofu sensibles.
5. **Clé perdue :** les secrets SOPS ne peuvent plus être déchiffrés ; il faut
   disposer d'une procédure de récupération ou de rotation.
6. **Clé compromise :** l'attaquant peut déchiffrer les secrets accessibles et
   potentiellement administrer l'infrastructure.

À vérifier dans la configuration : identité age autorisée par `.sops.yaml`,
emplacement de la clé privée, droits des fichiers, rotation et journalisation.

## Partie 5 - Mise en commun

Présentez vos trois exemples et enrichissez l'inventaire avec les services
identifiés par les autres groupes. Corrigez les mécanismes mal attribués et
marquez avec `?` ceux qui restent à vérifier.

Les contextes à comparer sont notamment :

- SSH et Ansible ;
- HTTPS, LDAPS, IMAPS et SMTP STARTTLS ;
- PKI et certificats ;
- sauvegardes et chiffrement des données au repos ;
- stockage des mots de passe ;
- paquets et mises à jour APT ;
- services cloud, OpenTofu et secrets SOPS ;
- VPN ou Wi-Fi étudiés précédemment.

## Partie 6 - Préparer l'autonomie du J2

Le lendemain, confrontez une configuration déjà réalisée aux recommandations
cryptographiques de l'ANSSI. Il ne s'agit pas de construire une nouvelle
infrastructure, mais d'analyser une configuration réelle, notamment la
protection ou le chiffrement des sauvegardes.

### Vérifications avant la fin du J1

- [ ] accès au [guide ANSSI sur les mécanismes cryptographiques](https://messervices.cyber.gouv.fr/guides/mecanismes-cryptographiques) ;
- [ ] parties du guide à étudier identifiées ;
- [ ] configuration choisie retrouvée ;
- [ ] paramètres et fichiers nécessaires disponibles ;
- [ ] algorithmes connus relevés, sans inventer ceux qui ne le sont pas ;
- [ ] livrable et emplacement de dépôt connus ;
- [ ] questions bloquantes posées au formateur.

### Tableau d'analyse ANSSI

| Recommandation ANSSI | Applicable ? | Configuration observée | Conforme / Écart / Non vérifiable | Modification proposée | Justification |
| --- | --- | --- | --- | --- | --- |
| Utiliser des mécanismes cryptographiques robustes pour protéger les sauvegardes | Oui | Borg initialise le dépôt avec `--encryption=repokey` ; phrase secrète demandée hors Git | Non vérifiable | Relever la version de Borg et le détail de l'algorithme utilisé, puis le comparer au guide ANSSI | Le mode de chiffrement est identifié, mais l'algorithme exact n'apparaît pas dans les fichiers consultés. |
| Protéger les communications par TLS avec une version minimale récente | Oui | Dovecot impose TLS et `ssl_min_protocol = TLSv1.2` ; LDAPS, IMAPS, SMTP STARTTLS et HTTPS sont déployés | Conforme pour Dovecot ; à vérifier pour les autres services | Contrôler la version minimale et les suites négociées avec `openssl s_client` pour chaque service | Les contrôles TLS existent dans `documentation/tls-deployment.md`, mais les suites cryptographiques ne sont pas détaillées partout. |
| Vérifier l'authenticité des certificats et leur chaîne de confiance | Oui | Certificats émis par `Campus CA`, racine distribuée, vérification avec `openssl verify` | Conforme pour les services validés | Rejouer les contrôles après chaque renouvellement et documenter les résultats | OpenLDAP, Postfix, Dovecot et Roundcube ont été validés avec la chaîne Campus CA. |
| Protéger les clés privées et limiter leur diffusion | Oui | Clés exclues de Git, permissions `600`, volumes Docker dédiés ; Ansible synchronise certaines clés vers les hôtes de service | Écart à analyser | Vérifier les droits sur les hôtes cibles et limiter les comptes, répertoires et journaux accessibles | La protection est prévue dans les scripts, mais le niveau réel de protection après déploiement cloud doit être contrôlé. |
| Prévoir le renouvellement et la révocation des certificats | Oui | Durée cible de 90 jours, renouvellement à 30 jours ; révocation/CRL encore à tester | Écart | Mettre en œuvre et tester la révocation, puis vérifier les alertes d'expiration | L'architecture décrit le cycle de vie, mais le mécanisme de révocation n'est pas encore validé. |
| Chiffrer les secrets d'administration et contrôler les clés de déchiffrement | Oui | `cloud-lab.env` est chiffré par SOPS avec AES-256-GCM et une clé age définie dans `.sops.yaml` | Non vérifiable | Vérifier la conservation, la rotation et la sauvegarde de la clé privée age | Le dépôt montre le chiffrement et le destinataire, mais pas la gestion opérationnelle de la clé privée. |
| Restreindre l'administration distante aux postes autorisés | Oui | Ansible limite SSH à `admin_ssh_cidr` via UFW ; les clés SSH privées ne sont pas versionnées | Non vérifiable | Contrôler la configuration SSH effective et les algorithmes négociés sur les VM | Le filtrage réseau est documenté, mais les paramètres cryptographiques SSH ne sont pas présents dans les fichiers étudiés. |

Utilisez **Non vérifiable** lorsqu'une information manque. Précisez alors :

- quelle information est indisponible ;
- dans quel fichier, journal ou outil elle pourrait être obtenue ;
- pourquoi cette absence empêche de conclure.

L'objectif est de relier chaque recommandation à une configuration réelle et de
justifier la conclusion, pas de déclarer artificiellement le plus grand nombre
d'éléments conformes.

## Ressources de travail

- [Guide ANSSI - Mécanismes cryptographiques](https://messervices.cyber.gouv.fr/guides/mecanismes-cryptographiques)
- `Modules/on-premise/documentation/pki-architecture.md`
- `Modules/on-premise/documentation/tls-deployment.md`
- `Modules/on-premise/documentation/backup-implementation.md`
- `Modules/cloud-iam/ansible/playbooks/deploy-on-premise.yml`
- `Modules/cloud-iam/secrets/cloud-lab.env`
