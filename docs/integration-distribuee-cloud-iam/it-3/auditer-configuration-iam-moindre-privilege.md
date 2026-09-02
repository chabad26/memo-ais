# Auditer une configuration IAM

!!! info "Atelier pas à pas - posture d'audit"
    Les données de cette feuille sont fictives. Ne pas remplacer les valeurs
    par un vrai mot de passe, token, secret ou identifiant de production.

## Objectif

Repérer les écarts au principe de moindre privilège dans une configuration IAM,
proposer des corrections priorisées et transformer l'analyse en règles
applicables à l'infrastructure.

## Configuration à analyser

Cette configuration volontairement vulnérable contient deux identités :

```json
{
  "utilisateur": "stagiaire-marketing",
  "groupe": "administrateurs",
  "mfa": false,
  "cle_api_creee_le": "2023-01-15",
  "derniere_utilisation": "2023-02-02"
}
{
  "utilisateur": "service-backup",
  "type": "identite_de_service",
  "permissions": ["*:*"],
  "cle_api_partagee_avec": [
    "service-monitoring",
    "service-deploiement"
  ]
}
```

Les deux objets sont présentés séparément pour faciliter la lecture ; ils ne
forment pas un document JSON unique valide.

## Déroulement

### Étape 1 - Lire l'identité humaine

Relever les champs un par un :

| Champ | Question d'audit |
| --- | --- |
| `utilisateur` | La mission de la personne est-elle connue ? |
| `groupe` | Les droits du groupe correspondent-ils à cette mission ? |
| `mfa` | Une authentification renforcée protège-t-elle le compte ? |
| `cle_api_creee_le` | La clé est-elle encore nécessaire et suivie ? |
| `derniere_utilisation` | La date d'usage est-elle compatible avec l'activité actuelle ? |

Constat initial : un compte de stagiaire placé dans `administrateurs` doit être
considéré comme suspect tant que son besoin d'administration n'est pas démontré.

### Étape 2 - Lire l'identité de service

Pour un service, vérifier séparément :

1. son propriétaire et sa fonction exacte ;
2. les actions réellement nécessaires ;
3. les ressources et environnements ciblés ;
4. la date de rotation de ses secrets ;
5. l'absence de partage entre applications.

La permission `*:*` signifie « toutes les actions sur toutes les ressources ».
Elle contredit directement le moindre privilège et augmente fortement l'impact
d'une fuite ou d'une compromission.

### Étape 3 - Identifier les anomalies

Il faut relever au moins les anomalies suivantes :

| # | Anomalie | Risque | Urgence |
| --- | --- | --- | --- |
| 1 | `stagiaire-marketing` appartient à `administrateurs` sans justification | accès potentiel à toutes les ressources et actions | **critique** |
| 2 | `mfa` vaut `false` pour un compte privilégié | compromission possible avec le seul mot de passe | **critique** |
| 3 | la clé créée le 15/01/2023 n'a pas été utilisée depuis le 02/02/2023 | secret ancien, inutile et exploitable | **à corriger** |
| 4 | `service-backup` possède `*:*` | compromission du service = compromission globale | **critique** |
| 5 | la clé de `service-backup` est partagée avec deux services | traçabilité impossible et révocation dangereuse | **critique** |
| 6 | aucune expiration, rotation ou propriétaire n'est indiqué | absence de cycle de vie contrôlé | **à corriger** |

Une date ancienne n'est pas une preuve suffisante qu'une clé est inutilisée :
elle doit être confirmée par les journaux d'accès du fournisseur. Dans un vrai
audit, noter la source et la date de chaque constat.

### Étape 4 - Proposer les corrections

| Anomalie | Correction concrète | Vérification attendue |
| --- | --- | --- |
| Groupe administrateur injustifié | retirer l'utilisateur de `administrateurs` et créer un groupe adapté à sa mission, par exemple lecture seule | l'utilisateur ne peut plus créer, modifier ou supprimer |
| MFA désactivé | activer le MFA pour le compte privilégié et conserver les codes de secours dans un gestionnaire sécurisé | nouvelle connexion avec second facteur |
| Clé ancienne | vérifier les journaux, désactiver puis supprimer la clé si elle n'est plus utilisée | aucune authentification avec la clé supprimée |
| `*:*` | remplacer par une liste d'actions précises, limitée aux ressources de sauvegarde | une action hors périmètre renvoie un refus |
| Clé partagée | créer une identité et une clé distinctes pour chaque service | les journaux identifient le service appelant |
| Cycle de vie absent | nommer un propriétaire, une date d'expiration et une fréquence de rotation | fiche d'inventaire mise à jour après rotation |

### Étape 5 - Prioriser l'intervention

Traiter les corrections dans cet ordre :

1. désactiver ou isoler les accès `*:*` et les clés partagées ;
2. retirer le compte humain du groupe administrateur si son besoin n'est pas
   confirmé ;
3. activer le MFA du compte privilégié ;
4. auditer puis supprimer les clés anciennes ;
5. mettre en place la rotation, l'expiration et le suivi des propriétaires.

Ne pas supprimer une clé active sans avoir identifié ses dépendances. Préparer
une nouvelle clé, tester la connexion et révoquer l'ancienne après validation.

### Étape 6 - Vérifier la correction

Réaliser un second audit avec cette grille :

```text
[ ] chaque utilisateur a une mission et un propriétaire identifiés
[ ] aucun compte privilégié n'est dépourvu de MFA
[ ] aucun service ne possède *:*
[ ] chaque service possède sa propre identité
[ ] aucune clé n'est partagée entre services
[ ] les clés anciennes sont désactivées ou supprimées après vérification
[ ] chaque accès est limité à des actions et ressources explicites
[ ] une date d'expiration et une procédure de rotation existent
[ ] un test de refus est conservé comme preuve
```

Le test de refus doit utiliser une ressource de laboratoire. Ne pas supprimer
une VM, un bucket ou une politique utile à DIST-01b uniquement pour produire une
preuve.

## Règles à appliquer à sa propre configuration

Reformuler les corrections sous forme de règles générales :

- une personne reçoit le niveau de droit correspondant à sa mission, jamais un
  rôle administrateur par défaut ;
- tout compte privilégié est protégé par MFA lorsque le fournisseur le permet ;
- une identité de service est dédiée à une application ou un automatisme ;
- une clé n'est jamais partagée entre deux services ;
- les permissions sont limitées par actions, ressources, projet et environnement ;
- les clés ont un propriétaire, une durée de vie et une procédure de rotation ;
- toute permission refusée est testée avec une preuve non sensible ;
- les secrets restent dans un gestionnaire dédié ou un environnement local
  protégé, jamais dans Git ou une capture.

## Application au parcours OVH

Dans le projet Public Cloud OVH utilisé ici, la page `Users & Roles` attribue
des rôles OpenStack prédéfinis aux utilisateurs du projet. Elle ne fournit pas
de rôle général `Compute Reader` ni de groupe personnalisé dans la matrice
observée. L'audit doit donc distinguer :

- ce qui est réellement prouvé par Horizon, comme le refus de création pour
  `operateur1` ;
- ce qui reste une limite de l'interface, comme la lecture seule générale ;
- ce qui relève de l'IAM global OVH, si cette fonction est accessible au compte.

Ne pas transformer un rôle spécialisé comme `AI Reader` ou `KeyManager Read` en
permission générale de lecture des VM.

## Preuves à conserver

| Preuve | Contenu acceptable |
| --- | --- |
| inventaire | identités, rôles, propriétaire et dates, sans secret |
| analyse | anomalies, risques et urgences justifiés |
| correction | rôle retiré, clé désactivée ou politique réduite |
| test | réussite d'une lecture autorisée et refus d'une écriture interdite |
| suivi | date de rotation et résultat du nouvel audit |

## Pour aller plus loin : cas réel

Rechercher un bulletin ANSSI ou un rapport public d'incident lié à une mauvaise
configuration IAM cloud. Résumer en cinq lignes :

1. le service ou l'organisation concernée ;
2. la permission ou le secret exposé ;
3. la cause racine de la configuration ;
4. l'impact constaté ;
5. la mesure préventive applicable à DIST-01b.

Conserver le lien et la date de consultation. Ne pas recopier de données
personnelles ou de secrets issus du rapport.

### Étude de cas : Capital One (2019)

Capital One est un cas d'école utile pour relier mauvaise configuration IAM,
stockage objet et vulnérabilité applicative. Le résumé ci-dessous s'appuie sur
les documents judiciaires américains et une analyse AWS ; les chiffres souvent
cités varient selon le périmètre retenu, mais l'incident a concerné environ 100
millions de personnes.

1. Une mauvaise configuration d'un pare-feu applicatif a permis à une
   attaquante d'envoyer des requêtes SSRF depuis un composant exposé.
2. Ces requêtes ont atteint le service de métadonnées EC2 et récupéré des
   identifiants temporaires associés au rôle IAM de l'instance.
3. Le rôle disposait de droits de lecture et de copie beaucoup trop larges sur
   des compartiments S3 contenant des données clients.
4. Les identifiants temporaires ont alors permis l'exfiltration de données,
   malgré leur durée de vie limitée.
5. La cause racine à retenir est le cumul d'une vulnérabilité SSRF et d'un rôle
   IAM sur-privilégié, aggravé par l'absence de cloisonnement suffisant.

**Mesures de prévention à retenir :** limiter chaque rôle aux actions et
ressources nécessaires, segmenter les buckets, journaliser les appels S3 et
réduire l'accès aux métadonnées. Sur EC2, activer et imposer IMDSv2 ajoute une
barrière contre de nombreuses attaques SSRF, mais ne remplace ni la correction
de la faille applicative ni le moindre privilège.

Sources : [acte d'accusation du Department of Justice](https://www.justice.gov/usao-wdwa/page/file/1405446/dl?inline=),
[analyse AWS sur la protection des métadonnées](https://aws.amazon.com/blogs/security/defense-in-depth-open-firewalls-reverse-proxies-ssrf-vulnerabilities-ec2-instance-metadata-service/)
et [analyse technique Snyk](https://snyk.io/blog/a-technical-analysis-of-the-capital-one-cloud-misconfiguration-breach/).

## Ressource

- [AWS IAM - Bonnes pratiques de sécurité](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
