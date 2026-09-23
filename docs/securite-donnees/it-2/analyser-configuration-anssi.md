# Analyser une configuration avec les recommandations ANSSI

## Objectif

Cette activité est réalisée en autonomie pendant 3h30. Le formateur n'est pas
présent pendant cette demi-journée.

L'objectif est de confronter deux configurations déjà utilisées dans le
parcours aux recommandations cryptographiques de l'ANSSI : une sauvegarde
on-premise et le stockage d'un état OpenTofu dans le cloud. Il ne s'agit pas de
vérifier mécaniquement tout le document : vous devez sélectionner les
recommandations applicables, retrouver les paramètres réels, identifier les
écarts et distinguer ce qui est prouvé de ce qui ne l'est pas.

## Corpus de l'analyse

Le travail porte sur les deux dossiers suivants :

| Dossier | Système étudié | Fonction cryptographique principale |
| --- | --- | --- |
| A - On-premise | Sauvegarde BorgBackup | Chiffrement et intégrité des archives |
| B - Cloud/IAM | État OpenTofu dans OVHcloud Object Storage | Chiffrement côté serveur et protection des secrets d'accès |

Les modules sont disponibles dans :

```text
/home/oliv/Documents/entreprise/AIS/Modules/on-premise
/home/oliv/Documents/entreprise/AIS/Modules/cloud-iam
```

### Dossier A - Sauvegarde on-premise

Examinez en priorité :

- `on-premise/backup/backup.sh` ;
- `on-premise/backup/README.md` ;
- `on-premise/documentation/backup-implementation.md` ;
- `on-premise/documentation/backup-strategy-validation.md`.

Vous devrez notamment retrouver le mode de chiffrement Borg, le traitement de
la phrase secrète, l'emplacement de la clé, les droits appliqués et les
commandes de contrôle d'intégrité.

### Dossier B - État OpenTofu dans le cloud

Examinez en priorité :

- `cloud-iam/README.md` ;
- `cloud-iam/opentofu/ovh/backend.tf` ;
- `cloud-iam/opentofu/ovh-object-storage/main.tf` ;
- `cloud-iam/opentofu/ovh-object-storage/variables.tf` ;
- `cloud-iam/opentofu/ovh/variables.tf`.

Vous devrez notamment retrouver le chiffrement déclaré pour le bucket, la
version de protocole imposée ou non pour les échanges, la gestion des
identifiants d'accès, la protection de l'état OpenTofu et la clé SSH attendue.

Pour approfondir l'analyse des données en transit, vous pouvez aussi examiner :

- `on-premise/messaging-compose/dovecot/dovecot.conf` ;
- `on-premise/messaging-compose/nginx/roundcube.conf` ;
- `on-premise/pki/scripts/issue-service-certificates.sh`.

Ne modifiez aucun de ces fichiers pendant la première phase. Commencez par les
analyser, puis proposez seulement les améliorations nécessaires.

!!! danger "Secrets et données sensibles"
    N'ouvrez, ne copiez et ne déposez jamais un fichier `.env`, `OpenRC`,
    `terraform.tfvars`, `tfstate`, une clé privée ou une phrase secrète. Les
    modèles, les noms de variables et les extraits de configuration sans valeur
    sensible suffisent pour l'analyse.

## Ressources

- document ANSSI indiqué en J1 ;
- sections ANSSI indiquées en J1 ;
- modules `on-premise` et `cloud-iam` ;
- fichiers de configuration, commandes, captures ou extraits permettant de
  retrouver les paramètres utilisés.

Une information absente ne doit pas être inventée. Utilisez `Non vérifiable` et
expliquez ce qui manque.

## Tableau récapitulatif du référentiel ANSSI

Ce tableau synthétise les règles et recommandations de la version 3.00. Les
formulations sont volontairement résumées : le document ANSSI reste la source à
consulter pour les conditions complètes, les modèles d'attaque et les limites
d'emploi. `PQ` signifie que l'exigence concerne la sécurité post-quantique.

Les deux dernières colonnes reprennent les classements explicitement donnés par
l'ANSSI ou, lorsqu'aucun exemple n'est nommé, un critère directement déduit de
la règle. L'absence d'exemple est indiquée par `Non précisé` et ne signifie pas
qu'aucun mécanisme conforme ou non conforme n'existe.

| Domaine | Type et identifiant | Synthèse | Exemples ou critères conformes | Exemples non conformes ou limites |
| --- | --- | --- | --- | --- |
| Principes généraux | Reco `RecoSécuLongTerme` ; Reco `RecoMécanismesÉprouvés` | Viser une protection post-quantique si l'usage dépasse 2030 ou permet une attaque rétroactive ; employer des mécanismes reconnus par la communauté académique. | Mécanisme standardisé, documenté et largement analysé. | Algorithme propriétaire ou durée de protection non étudiée. |
| Taille des clés symétriques | Règle `RègleTailleCléSym` ; RecoPQ `RecoPQTailleCléSym` | Minimum classique : 128 bits. Pour une marge post-quantique substantielle : au moins 192 bits. | AES-128 respecte la règle classique ; AES-192 et AES-256 respectent aussi la recommandation PQ. | Triple-DES à deux clés : 112 bits effectifs, donc insuffisant. |
| Chiffrement par bloc | Règles `RègleTailleBlocSym`, `RèglePrimChiffBloc`, `RèglePQPrimChiffBloc` ; RecoPQ `RecoPQPrimChiffBloc` | Blocs d'au moins 128 bits et résistance minimale aux attaques classiques ; exigences supplémentaires contre les attaques quantiques. | AES-128, AES-192 et AES-256 pour les règles ; AES-192 et AES-256 pour la recommandation PQ. | Triple-DES : blocs de 64 bits ; Triple-DES à trois clés n'atteint pas la résistance classique exigée. |
| Modes de chiffrement | Règle `RègleModeChiff` ; Reco `RecoModeChiff` | Employer un mode robuste dans son contexte, non déterministe et, de préférence, assurant aussi l'intégrité. | AES-GCM ; AES-CBC avec IV aléatoire pour la confidentialité, sous réserve d'ajouter séparément l'intégrité. | CBC, CTR, OFB ou CFB employés seuls ne protègent pas l'intégrité ; réutiliser un IV GCM sous une même clé compromet la sécurité. |
| Chiffrement par flot | Règles `RègleChiffFlot`, `RèglePQChiffFlot` ; Reco `RecoChiffFlot` | Exiger une résistance classique suffisante, un état interne d'au moins 256 bits pour le PQ et une protection d'intégrité complémentaire. | ChaCha20 respecte les règles et la taille d'état recommandée. | ChaCha20 employé sans mécanisme d'intégrité ne respecte pas `RecoChiffFlot.2`. |
| Codes d'authentification de message | Règles `RègleMAC`, `RèglePQMAC` ; Reco `RecoMAC` ; RecoPQ `RecoPQMAC` | Utiliser une primitive conforme, viser un motif d'intégrité d'au moins 128 bits et conserver la robustesse des briques sous-jacentes en contexte PQ. | HMAC-SHA-256 ; CMAC-AES-128 et GMAC-AES-128 sous les conditions indiquées dans le guide. | CBC-MAC sur des messages de tailles variables ; CBC-MAC « retail » fondé sur DES ou Triple-DES. |
| Fonctions de hachage | Règle `RègleHachage` ; Reco `RecoHachage` ; RecoPQ `RecoPQHachage` | Empreinte d'au moins 256 bits, résistance aux collisions et préimages ; éviter les fonctions avec attaque partielle connue ; viser 384 bits en contexte PQ. | SHA2-256 et SHA3-256 pour les règles classiques ; SHA3-384 respecte aussi la recommandation PQ. | SHA-1 ; SHA3-224 ; SHAKE-128 avec sortie de 256 bits lorsqu'il est utilisé comme fonction de hachage. |
| Fonctions à sortie extensible | Règles `RègleXOF`, `RèglePQXOF` ; Reco `RecoXOF` ; RecoPQ `RecoPQXOF` | Dimensionner la résistance aux collisions et préimages selon la longueur de sortie, avec des seuils renforcés en contexte PQ. | SHAKE-256 respecte les règles et recommandations. | SHAKE-128 respecte les règles mais pas toutes les recommandations de marge classique et PQ. |
| Fondements asymétriques | Règles `RègleSécuAsym`, `RèglePQSécuAsym` | Fonder la sécurité classique sur un problème éprouvé ou une primitive symétrique conforme ; pour le PQ, utiliser un problème présumé résistant au quantique ou une primitive symétrique conforme. | Factorisation, logarithme discret ou courbes adaptées pour la sécurité classique ; problèmes LWE et SIS pour le PQ, avec paramètres suffisants. | RSA, Diffie-Hellman ou courbes classiques employés seuls ne fournissent pas de sécurité post-quantique. |
| RSA et factorisation | Règle `RègleFactorisation` ; Reco `RecoFactorisation` | RSA : module d'au moins 2048 bits jusqu'à fin 2030, puis 3072 bits ; 3072 bits sont recommandés dès maintenant. Les exposants et nombres premiers doivent aussi respecter les contraintes du guide. | RSA avec module et paramètres respectant toutes les contraintes ; exposant public usuel 65537. | RSA 1024 bits ; exposant public trop petit ; nombres premiers mal choisis ou exposant secret réduit. |
| Logarithme discret dans `GF(p)` | Règle `RègleLogDiscretGFp` ; Reco `RecoLogDiscretGFp` | Module d'au moins 2048 bits jusqu'à fin 2030 puis 3072 bits ; sous-groupe contenant un facteur premier d'au moins 250 bits, idéalement d'ordre premier. | Paramètres respectant les tailles et l'ordre de sous-groupe demandés. | Modules trop petits ou sous-groupes comportant de petits facteurs ; absence de résistance PQ. |
| Courbes elliptiques | Règles `RègleCourbeElliptiqueGFp`, `RègleCourbeElliptiqueGF2n` ; Reco `RecoCourbeElliptiqueGFp`, `RecoCourbeElliptiqueGF2n` | Employer un sous-groupe comportant un facteur premier d'au moins 250 bits, idéalement d'ordre premier ; pour `GF(2^n)`, `n` doit être premier. | FRP256v1, P-256, P-384, P-521, certaines Brainpool ; B-283, B-409 et B-571 pour `GF(2^n)`. | Courbes ou sous-groupes ne respectant pas ces paramètres ; aucune de ces courbes classiques n'apporte seule une sécurité PQ. |
| Réseaux euclidiens | RèglePQ `RèglePQRéseauEuclidien` ; RecoPQ `RecoPQRéseauEuclidien` | Pour `(M)LWE` ou `(M)SIS`, atteindre au moins la difficulté d'un SVP générique de dimension 400 ; la recommandation vise 600. | Jeux de paramètres démontrant les niveaux de difficulté demandés. | Paramètres sans analyse suffisante ou sous les seuils ; le guide ne donne pas ici une simple liste binaire d'algorithmes. |
| Encapsulation et chiffrement asymétrique | Reco `RecoConfidentialitéAsym` | Choisir des mécanismes disposant d'une preuve de sécurité ; en hybridation, conserver le modèle de sécurité le plus fort des composants. | ECIES-KEM ; RSAES-OAEP correctement dimensionné ; ML-KEM-512 ou Frodo-KEM-640 hybridés avec un mécanisme classique, avec préférence pour leurs niveaux supérieurs. | ML-KEM seul ne respecte pas la règle de sécurité classique ; RSAES PKCS#1 v1.5 est vulnérable dans un contexte avec oracle de padding. |
| Signature numérique | Reco `RecoSignature` | Employer une signature avec preuve de sécurité et une hybridation conservant les propriétés attendues. | RSA-SSA-PSS correctement dimensionné ; ECDSA ou ECKCDSA avec les courbes admises ; SLH-DSA. | RSA-SSA PKCS#1 v1.5 avec petit exposant et mauvaise vérification du padding ; ML-DSA seul ne satisfait pas la règle classique. |
| Établissement de clé et confidentialité persistante | Reco `RecoConfidentialitéPersistante` ; RecoPQ `RecoPQConfidentialitéPersistante` | Une compromission future des secrets de long terme ne doit pas révéler les sessions passées ; effacer les secrets temporaires en fin de session, y compris face à un adversaire quantique lorsque ce besoin est retenu. | Échange authentifié utilisant des secrets éphémères, avec effacement effectif ; mécanisme hybride classique et PQ adapté. | Diffie-Hellman hybridé seulement avec une clé pré-partagée ne conserve pas la confidentialité persistante face à un adversaire quantique après compromission de cette clé. |
| Secrets de faible entropie | Règle `RègleSecretFaibleEntropie` | Empêcher toute recherche exhaustive hors ligne lorsqu'un mot de passe, une donnée biométrique ou un autre secret faible est utilisé. | Protocole résistant aux attaques hors ligne et limitant les essais en ligne. | Empreintes ou échanges permettant de tester librement des hypothèses de mots de passe hors ligne. |
| Architecture du générateur d'aléa | Règle `RègleArchiGénAléa` ; Reco `RecoArchiGénAléa` | Utiliser un retraitement algorithmique avec un état interne d'au moins 192 bits ; 256 bits, mémoire non volatile et rafraîchissement régulier sont recommandés. | Générateur physique évalué selon une méthodologie reconnue et associé à un retraitement conforme. | Source physique brute sans retraitement, simple lissage ou état interne trop petit. |
| Générateur physique d'aléa | Règle `RègleGénPhysAléa` ; Reco `RecoGénPhysAléa` | Documenter le fonctionnement, vérifier statistiquement l'absence de défaut manifeste et justifier la qualité de la source. | Générateur documenté, testé et appuyé par un raisonnement de sécurité. | Source non documentée, non testée ou dont les pannes ne sont pas traitées. |
| Retraitement de l'aléa | Règle `RègleGénAléaRetraitement` | Employer des primitives conformes, protéger l'état interne et assurer la résistance arrière après compromission. | HMAC_DRBG ou Hash_DRBG avec SHA-384 ; CTR_DRBG avec AES-256, selon NIST SP 800-90Ar1. | Non précisé dans le guide ; tout mécanisme ne satisfaisant pas les trois propriétés est hors référentiel. |

!!! note "Lire correctement les statuts"
    Une `Règle` est nécessaire pour déclarer un mécanisme conforme au
    référentiel. Une `Reco` ajoute une marge de sécurité correspondant à l'état
    de l'art. Une `RèglePQ` devient nécessaire lorsqu'une sécurité
    post-quantique est recherchée ; une `RecoPQ` ajoute alors une marge
    supplémentaire. Un mécanisme peut donc être conforme aux règles classiques
    tout en ne respectant pas une recommandation ou les objectifs
    post-quantiques.

## Partie 1 - Retrouver votre environnement de travail

Avant de commencer l'analyse, vérifiez que vous disposez :

- du document ANSSI indiqué en J1 ;
- des sections à étudier ;
- de la configuration à analyser ;
- des éléments permettant de retrouver les paramètres utilisés.

### Configurations analysées

| Élément | Dossier A - On-premise | Dossier B - Cloud/IAM |
| --- | --- | --- |
| Système ou service | BorgBackup | OpenTofu et OVHcloud Object Storage |
| Fonction de la configuration | Sauvegarder les données de l'infrastructure | Stocker l'état de l'infrastructure déclarée |
| Fichiers disponibles | `backup/backup.sh`, `backup/README.md`, `documentation/backup-implementation.md`, `documentation/backup-strategy-validation.md` | `README.md`, `opentofu/ovh/backend.tf`, `opentofu/ovh-object-storage/main.tf`, `opentofu/ovh-object-storage/variables.tf`, `.gitignore` |
| Éléments manquants ou incertains | Paramètres cryptographiques internes du mode `repokey`, emplacement réel de la clé exportée, robustesse de la phrase secrète, preuve récente d'une restauration | Configuration effective du bucket, version et suites TLS négociées, mode AES et mécanisme d'intégrité employés par le fournisseur, stockage et rotation des identifiants d'accès |

## Partie 2 - Identifier les recommandations applicables

Parcourez les sections ANSSI indiquées. À ce stade, ne cherchez pas encore à
conclure sur la conformité. Commencez par décider si chaque recommandation est
applicable à votre situation.

Pour chaque recommandation retenue, relevez :

- son identifiant ;
- son objet ;
- le mécanisme ou paramètre concerné ;
- l'information nécessaire pour la vérifier.

| Dossier | Recommandation | Objet | Applicable ? | Information nécessaire pour la vérifier |
| --- | --- | --- | --- | --- |
| A et B | `RecoMécanismesÉprouvés` | Employer des mécanismes reconnus et éprouvés | Oui | Mécanisme, bibliothèque, logiciel et version utilisés |
| A et B | `RègleTailleCléSym` | Utiliser une clé symétrique d'au moins 128 bits | Oui | Algorithme et taille effective de la clé |
| A et B | `RègleModeChiff` et `RecoModeChiff` | Employer un mode sûr, non déterministe et complété par une protection de l'intégrité | Oui | Mode, gestion des IV ou nonces et mécanisme d'intégrité |
| A et B | `RecoSécuLongTerme` | Viser une sécurité post-quantique si la protection doit dépasser 2030 ou en cas d'attaque rétroactive | À déterminer | Durée de conservation et sensibilité des sauvegardes et états |
| A | Guide de sélection, section 2.2.4 | Maîtriser le cycle de vie des clés | Oui | Génération, stockage, sauvegarde, rotation, révocation et destruction de la clé Borg |
| B | Guide de sélection, sections 2.2.3 et 2.2.4 | Séparer les usages et protéger les secrets d'accès | Oui | Emplacement, droits, durée de vie et rotation des identifiants OVHcloud |

Si une recommandation n'est pas comprise, notez-la pour le débrief de
l'après-midi.

## Partie 3 - Examiner la configuration

Recherchez maintenant dans votre configuration les informations permettant de
répondre aux recommandations retenues.

Selon le système étudié, vous pouvez notamment rechercher :

- les mécanismes cryptographiques utilisés ;
- les algorithmes configurés ;
- les tailles de clés ;
- les paramètres associés ;
- la manière dont les clés sont générées ;
- la manière dont les clés ou secrets sont stockés ;
- les mécanismes de protection de l'intégrité ;
- les versions des protocoles ou logiciels concernés.

Pour chaque observation importante, conservez une preuve : extrait de
configuration, commande et résultat, capture ou autre élément permettant de
justifier votre analyse.

### Preuves relevées dans les fichiers

| Dossier | Preuve | Ce qu'elle permet d'affirmer | Limite de la preuve |
| --- | --- | --- | --- |
| A | `backup.sh` utilise `umask 077` | Les nouveaux fichiers créés par le script sont limités au propriétaire par défaut | Ne prouve pas les droits de fichiers créés auparavant ou hors du script |
| A | `borg init --encryption=repokey` | Le dépôt Borg est initialisé avec un chiffrement et une clé stockée dans sa configuration | Le fichier ne donne pas la taille de clé, le mode exact ni la gestion des nonces |
| A | La phrase secrète est lue avec `read -rsp`, puis retirée avec `unset` | La saisie interactive n'est pas affichée et la variable est supprimée lors du nettoyage | En exécution planifiée, la phrase secrète peut provenir d'un fichier `.env` en clair |
| A | `borg check` est exécuté après la sauvegarde | Un contrôle Borg est prévu après chaque création d'archive | La présence de la commande ne prouve pas le succès de la dernière exécution |
| B | `sse_algorithm = "AES256"` | La ressource OpenTofu demande un chiffrement serveur AES-256 | Ne prouve ni l'application effective sur le bucket ni le mode AES utilisé |
| B | Le backend utilise une URL `https://` | Le client vise un transport TLS vers l'Object Storage | Ne précise ni la version TLS minimale ni les suites négociées |
| B | Le versionnement du bucket est déclaré `enabled` | Une protection contre l'écrasement accidentel de l'état est demandée | Le versionnement n'est pas un mécanisme cryptographique et son activation réelle n'est pas prouvée |
| B | `.gitignore` exclut les fichiers `tfstate` et le README interdit OpenRC, clés privées et `terraform.tfvars` | Les secrets et états ne doivent pas être versionnés | Ne prouve pas leur stockage sécurisé, leur rotation ou leur absence de l'historique Git |

### Commandes de repérage

Ces commandes recherchent les paramètres utiles sans afficher le contenu des
fichiers secrets :

```bash
cd /home/oliv/Documents/entreprise/AIS/Modules

rg -n "borg init|encryption|BORG_PASSPHRASE|umask|borg check|key export" \
  on-premise/backup on-premise/documentation

rg -n "backend|endpoint|encryption|sse_algorithm|versioning|sensitive|ssh_public_key" \
  cloud-iam/opentofu cloud-iam/README.md

rg -n "ssl_min_protocol|ssl_protocols|ssl_certificate|ssl_key" \
  on-premise/messaging-compose
```

Pour Borg, les commandes suivantes peuvent constituer une preuve seulement si
le dépôt existe encore et si vous êtes autorisé à l'interroger :

```bash
borg info /home/oliv/borg-infrastructure-backup
borg check /home/oliv/borg-infrastructure-backup
```

Ne lancez pas `tofu apply`. La lecture des fichiers et, si l'environnement est
déjà initialisé, un `tofu validate` suffisent pour cette activité.

!!! warning "Limite importante"
    Ne concluez pas à la conformité d'un élément simplement parce qu'aucune
    configuration contraire n'a été trouvée.

## Partie 4 - Confronter recommandations et configuration

Le tableau suivant constitue une proposition de corrigé fondée sur les fichiers
disponibles. Les conclusions devront être réévaluées si de nouvelles preuves
d'exécution sont fournies.

| Dossier | Recommandation ANSSI | Applicable ? | Configuration observée | Conforme / Écart / Non vérifiable | Modification proposée | Preuve ou justification |
| --- | --- | --- | --- | --- | --- | --- |
| A | `RecoMécanismesÉprouvés` | Oui | BorgBackup 1.4.4 observé localement ; dépôt initialisé avec `repokey` | Conforme | Documenter la version réellement utilisée par la tâche planifiée et joindre la documentation cryptographique correspondante | BorgBackup est un mécanisme public et éprouvé ; les paramètres internes sont évalués séparément dans les lignes suivantes. La version locale observée ne garantit pas celle d'un autre hôte |
| A | `RègleTailleCléSym` | Oui | Le mode `repokey` est déclaré, sans taille de clé dans les fichiers étudiés | Non vérifiable | Relever les paramètres du dépôt et la documentation de la version Borg utilisée | L'identifiant `repokey` ne suffit pas, dans ce corpus, à prouver la taille effective de la clé |
| A | `RègleModeChiff` et `RecoModeChiff.3` | Oui | Borg assure chiffrement et contrôle d'intégrité ; `borg check` est exécuté | Non vérifiable | Documenter le mode de chiffrement, le mécanisme d'intégrité et la gestion des IV ou nonces de Borg 1.4.4 | Le script prouve l'usage de Borg, mais n'expose pas ces paramètres cryptographiques |
| A | Cycle de vie des clés, guide de sélection section 2.2.4 | Oui | `.env` exclu de Git et limité à `600`, `umask 077`, export de clé recommandé hors du dépôt | Écart | Mettre la phrase secrète dans un gestionnaire de secrets, définir la rotation et prouver une copie chiffrée de la clé sur un emplacement distinct | Le stockage en clair dans `.env` reste possible et l'export sécurisé de la clé est seulement décrit, pas prouvé |
| B | `RecoMécanismesÉprouvés` et `RègleTailleCléSym` | Oui | `sse_algorithm = "AES256"` | Conforme | Contrôler après déploiement la configuration effective du bucket et conserver une sortie expurgée | AES est éprouvé et 256 bits dépassent le minimum de 128 bits. Cette conclusion porte sur la configuration déclarée ; le fichier OpenTofu ne prouve pas son application effective |
| B | `RègleModeChiff` et `RecoModeChiff.3` | Oui | Le fournisseur reçoit uniquement la valeur générique `AES256` | Non vérifiable | Obtenir dans la documentation OVHcloud le mode AES, la gestion des IV et la protection d'intégrité du chiffrement serveur | Aucun de ces paramètres n'apparaît dans les fichiers étudiés |
| B | Protection cryptographique du transport | Oui | Le backend S3 cible `https://s3.gra.io.cloud.ovh.net/` | Non vérifiable | Tester la négociation TLS et relever version, suite, certificat et chaîne de confiance | `https://` indique l'usage attendu de TLS, sans imposer ni prouver ses paramètres effectifs |
| B | Cycle de vie des secrets, guide de sélection section 2.2.4 | Oui | OpenRC, `terraform.tfvars`, clés privées et `tfstate` sont interdits dans Git ; les valeurs réelles ne sont pas versionnées | Non vérifiable | Utiliser un gestionnaire de secrets, limiter les droits, définir une durée de vie et une rotation, puis auditer l'historique Git | Les règles documentaires ne prouvent pas le stockage ni la rotation réels des identifiants |
| A et B | `RecoSécuLongTerme` | À déterminer | Aucune durée de confidentialité au-delà de 2030 n'est définie | Non vérifiable | Faire fixer la durée de conservation et le besoin de résistance aux attaques rétroactives par le responsable métier ou le RSSI | Sans durée de protection attendue, l'applicabilité de la recommandation post-quantique ne peut pas être décidée |

Utilisez :

- `Conforme` lorsque vous disposez d'éléments permettant de montrer que la
  configuration respecte la recommandation ;
- `Écart` lorsque la configuration observée ne respecte pas la recommandation ;
- `Non vérifiable` lorsque les informations disponibles ne permettent pas de
  conclure.

Pour un élément `Non vérifiable`, précisez dans la justification :

1. quelle information manque ;
2. où ou auprès de qui vous pourriez la rechercher.

## Partie 5 - Proposer des améliorations

Reprenez les écarts identifiés. Pour chaque écart, proposez une modification
réaliste de la configuration.

Votre proposition doit préciser :

- ce qui doit être modifié ;
- la recommandation à laquelle cette modification répond ;
- l'impact éventuel de la modification sur le système.

Ne cherchez pas nécessairement à appliquer les modifications pendant cette
activité.

| Question | Réponse |
| --- | --- |
| Quel écart vous paraît prioritaire, parmi les deux dossiers ? | La gestion de la phrase secrète et de la clé Borg du dossier A. |
| Pourquoi ? | La sauvegarde contient les données LDAP, les boîtes mail, des configurations et des exports de base. Une phrase secrète compromise ou une clé perdue compromet respectivement la confidentialité ou la capacité de restauration. |
| Quelle modification proposeriez-vous ? | Remplacer le fichier `.env` contenant la phrase secrète par un gestionnaire de secrets ou un mécanisme protégé équivalent, exporter la clé Borg vers un support chiffré distinct, formaliser sa rotation et tester une restauration avec ces éléments. |
| Quel impact opérationnel faut-il anticiper ? | Adapter la tâche cron, autoriser uniquement le compte de sauvegarde à lire le secret, organiser une procédure de récupération et prévoir une fenêtre de test de restauration. |

## Partie 6 - Préparer le débrief

Avant de déposer votre travail, identifiez les points qui seront repris avec le
formateur l'après-midi.

| Point de débrief | Réponse |
| --- | --- |
| Une recommandation facile à appliquer à une configuration réelle | Choisir AES avec une clé d'au moins 128 bits ; le dossier B déclare explicitement AES-256. |
| Une recommandation dont l'interprétation vous a posé problème | `RecoSécuLongTerme`, car son applicabilité dépend de la durée de confidentialité attendue et du risque d'attaque rétroactive, absents du corpus. |
| Une information technique qui vous manquait pour conclure | Le mode AES, la gestion des IV ou nonces et le mécanisme d'intégrité employés par le chiffrement serveur OVHcloud et par le mode Borg `repokey`. |
| Un choix cryptographique de votre configuration que vous comprenez maintenant mieux | Un nom comme `AES256` ou `repokey` ne suffit pas à démontrer toute la robustesse : il faut aussi connaître le mode opératoire, l'intégrité, la génération d'aléa et le cycle de vie des clés. |

## Livrable attendu

Déposez avant la fin de la demi-journée :

- l'identification des deux configurations analysées ;
- le tableau des recommandations applicables ;
- au moins deux preuves pour le dossier A et deux pour le dossier B ;
- le tableau de confrontation ;
- les écarts et améliorations proposées ;
- les points préparés pour le débrief.

Le livrable doit permettre de distinguer clairement une preuve tirée d'un
fichier versionné, une observation faite sur un système en fonctionnement et
une information `Non vérifiable` avec les seuls éléments disponibles.

## Références

- [ANSSI - Mécanismes cryptographiques](https://messervices.cyber.gouv.fr/guides/mecanismes-cryptographiques) ;
- [Règles et recommandations concernant le choix et le dimensionnement des mécanismes cryptographiques, version 3.00](https://messervices.cyber.gouv.fr/documents-guides/anssi-guide-mecanismes-crypto-3.00.pdf) ;
- [Guide de sélection d'algorithmes cryptographiques, version 1.0](https://messervices.cyber.gouv.fr/documents-guides/anssi-guide-selection_crypto-1.0.pdf).
