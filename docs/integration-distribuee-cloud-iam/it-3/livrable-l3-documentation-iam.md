# 3.8 | Livrable L3 : documentation IAM et chiffrement

!!! info "Convention de nommage"
    Le livrable final est nommé
    `Nom-Prénom-Grenoble-DIST01b-DocIAM`.

## Objectif

Consolider la configuration IAM, l'audit du moindre privilège et les contrôles
de chiffrement dans un document exploitable par un tiers. Le lecteur doit
pouvoir comprendre qui accède à quoi, pourquoi, comment l'accès est revu et
quelles preuves permettent de vérifier les choix.

!!! warning "Règle de sécurité"
    Cette fiche ne doit contenir aucun mot de passe, token, clé privée, secret
    S3 ou valeur complète de clé API. Les captures doivent être expurgées avant
    d'être ajoutées au dépôt.

## 1. Périmètre et état des preuves

Le périmètre couvre le projet cloud de laboratoire, les utilisateurs OVHcloud,
les rôles attribués, l'identité de service utilisée par OpenTofu, le bucket S3
du backend d'état et les services déployés sur les VM.

| Élément | Source de vérification | État à renseigner |
| --- | --- | --- |
| Utilisateurs et rôles OVHcloud | Console `Users & Roles` ou API | Validé / à vérifier |
| Groupe `operateurs` | Console ou état OpenTofu | Validé / à vérifier |
| Politique OpenTofu limitée au projet | Configuration IAM et `tofu apply` | Validé / à vérifier |
| MFA du compte administrateur | Console OVHcloud | Validé avec capture / à vérifier |
| Clé API d'OpenTofu | Métadonnées de la clé uniquement | Validé / à vérifier |
| Chiffrement du bucket S3 | Informations générales du bucket | Validé / à vérifier |
| Chiffrement des volumes de VM | Détails du fournisseur | Validé / non disponible |

Un élément non vérifié doit rester explicitement marqué comme tel dans le
livrable final.

## 2. Matrice utilisateurs, groupes, rôles et identités de service

Cette matrice répond à quatre questions : qui est l'identité, à quel groupe ou
rôle est-elle rattachée, sur quel périmètre agit-elle et pourquoi cet accès est
nécessaire.

| Identité | Type | Groupe / rôle | Périmètre | Accès autorisé | Justification | MFA / clé |
| --- | --- | --- | --- | --- | --- | --- |
| Compte administrateur principal | Humain | Administrator | Projet cloud et IAM | Administration complète nécessaire au bootstrap | Création initiale et gestion exceptionnelle | MFA à vérifier ou prouver par capture |
| `operateur1` | Humain | `operateurs` / rôle de lecture | Projet cloud | Consultation des ressources ; pas de création ni suppression | Exploitation et contrôle sans privilège d'administration | Pas de clé de déploiement |
| Identité OpenTofu | Service | Politique `tofu-project-limited` | Projet cloud ciblé | Actions OpenTofu strictement nécessaires, par exemple compute | Déployer l'infrastructure sans donner la gestion de l'IAM | Clé dédiée, restreinte et renouvelée |
| Ansible via SSH | Service technique | Compte ou clé d'administration système | VM ciblées | Configuration système et services après provisionnement | Séparer le provisionnement cloud de la configuration OS | Clé SSH protégée et limitée aux hôtes |
| Fournisseur S3 backend | Service technique | Clé S3 dédiée au bucket | Bucket d'état | Lecture/écriture de l'état OpenTofu uniquement | Éviter l'accès aux autres buckets ou projets | Clés hors Git, rotation planifiée |

Les noms exacts, identifiants et rôles doivent être remplacés par ceux de la
configuration réelle. Une identité de service ne doit pas être remplacée par
un compte humain partagé.

## 3. Règles de moindre privilège

| Règle | Application | Vérification |
| --- | --- | --- |
| Séparer humains et services | `operateur1` ne sert pas à OpenTofu ou Ansible | Rechercher les clés rattachées aux utilisateurs humains |
| Limiter le périmètre | La politique OpenTofu vise le projet nécessaire uniquement | Vérifier le champ `resources` de la politique |
| Limiter les actions | OpenTofu ne reçoit pas de droits IAM par défaut | Vérifier `allow` et tester une action interdite |
| Éviter les secrets partagés | Une clé est dédiée à un seul service | Inventorier les propriétaires et dates de création |
| Révoquer rapidement | Une clé ou un compte inutilisé est désactivé puis supprimé | Conserver la date et l'auteur de la revue |
| Protéger les privilèges élevés | Le compte administrateur est protégé par MFA | Capture expurgée ou export de configuration |

Les écarts doivent être justifiés. Exemple : un compte administrateur peut
conserver temporairement un rôle élevé pour le bootstrap, mais cette exception
doit avoir un responsable, une date de revue et une procédure de retrait.

## 4. Procédure de revue des accès

### Fréquence et responsabilité

| Revue | Fréquence | Responsable | Déclencheur supplémentaire |
| --- | --- | --- | --- |
| Comptes humains et rôles | Mensuelle | Administrateur cloud | Départ, changement de mission ou incident |
| Clés API et identités de service | Mensuelle | Responsable OpenTofu / sécurité | Rotation, fuite suspectée ou changement d'outil |
| Droits du bucket S3 | Trimestrielle | Administrateur cloud | Changement du backend ou restauration |
| MFA des comptes privilégiés | À chaque revue mensuelle | Administrateur cloud | Réinitialisation ou perte du second facteur |

### Étapes opératoires

1. Exporter la liste des identités, groupes, rôles, politiques, clés et dates de
   dernière utilisation sans exporter les secrets.
2. Comparer chaque accès à la mission actuelle de son propriétaire.
3. Identifier les comptes inactifs, les rôles trop larges et les clés âgées de
   plus de 90 jours.
4. Faire valider les exceptions par le responsable du projet.
5. Désactiver une clé ou un compte avant suppression, puis vérifier l'impact.
6. Supprimer l'accès devenu inutile et consigner l'opération dans le journal.
7. Rejouer les tests de moindre privilège et archiver la preuve expurgée.

Une révocation urgente doit suivre le même principe, mais sans attendre la
prochaine revue : désactiver la clé suspecte, analyser les journaux, remplacer
le secret et documenter l'incident.

## 5. Vérifier le MFA

Le livrable doit indiquer séparément :

- le compte administrateur principal et son état MFA ;
- les autres comptes disposant d'un rôle élevé ;
- les comptes de service, qui n'utilisent généralement pas un MFA interactif
  mais doivent être protégés par une clé dédiée, limitée et rotée ;
- les comptes ne pouvant pas bénéficier du MFA selon les capacités réelles du
  fournisseur.

Une capture du tableau de rôles ne prouve pas le MFA. Il faut une preuve issue
de la page de sécurité du compte ou une sortie d'API non sensible.

## 6. Section chiffrement

| Donnée / flux | Au repos | En transit | État / preuve |
| --- | --- | --- | --- |
| État OpenTofu dans le bucket S3 | Chiffrement serveur du bucket | HTTPS vers l'endpoint S3 | À prouver par la console du bucket et la configuration backend |
| Volumes des VM | Selon l'option du fournisseur | Sans objet pour le stockage | À vérifier dans les détails des volumes |
| SSH d'administration | Sans objet | Chiffré par SSH | Test de connexion et configuration SSH |
| LDAP entre services | Volumes selon configuration | LDAPS ou StartTLS si configuré | Certificat Step CA et test `openssl` |
| Interfaces web internes | Volumes selon configuration | HTTPS si configuré | Certificat interne et chaîne de confiance |
| Site web public | Stockage selon le fournisseur | HTTPS avec Let's Encrypt | Capture navigateur et vérification du renouvellement |
| Secrets Git | Fichier chiffré SOPS ou git-crypt | Transport Git à protéger séparément | Vérifier qu'aucun secret en clair n'est suivi |

Un certificat TLS ne chiffre pas les données au repos. Inversement, le
chiffrement d'un volume ne sécurise pas une connexion HTTP non protégée.

## 7. Script de contrôle des clés API

Le script versionné dans le dépôt est
[`check-iam-api-key-age.sh`](../../assets/scripts/integration-distribuee-cloud-iam/it-3/check-iam-api-key-age.sh).
Il reçoit un fichier de métadonnées local au format suivant, qui ne contient
aucun secret :

```json
[
  {
    "identity": "tofu",
    "key_id": "metadata-only-id",
    "created_at": "2026-01-15T10:00:00Z"
  }
]
```

Exécution :

```bash
chmod +x check-iam-api-key-age.sh
./check-iam-api-key-age.sh iam-credentials-metadata.json
echo $?
```

Le script retourne `0` si toutes les clés ont au plus 90 jours, `1` si au
moins une clé dépasse cette durée et `2` en cas d'erreur de fichier ou de date.
Le seuil peut être ajusté pour un test avec `MAX_AGE_DAYS=30`, mais la règle du
livrable reste 90 jours. Le fichier de métadonnées local doit être ignoré par
Git s'il contient des informations internes non destinées au dépôt.

## 8. Livrable et preuves

Le dossier remis sous le nom `Nom-Prénom-Grenoble-DIST01b-DocIAM` contient :

- cette matrice complétée avec les identités réelles ;
- les justifications des droits et des exceptions ;
- la procédure de revue et de révocation ;
- les preuves MFA et chiffrement expurgées ;
- le script de contrôle et un exemple de sortie ;
- un historique Git montrant une étape logique de versionnement.

Avant remise, effectuer ces contrôles :

```bash
git grep -n -I -E 'AKIA[0-9A-Z]{16}|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|password=|secret=' \
  -- ':!site'
git check-ignore -v iam-credentials-metadata.json
bash -n docs/assets/scripts/integration-distribuee-cloud-iam/it-3/check-iam-api-key-age.sh
```

Une recherche vide ne prouve pas à elle seule l'absence de secret, mais elle
complète la relecture manuelle des fichiers, captures et historiques Git.

## Résultat attendu

- un tiers comprend les identités et leurs permissions sans demander les
  secrets ;
- chaque droit possède une justification et un périmètre ;
- la revue des accès est planifiée et réversible ;
- le MFA et le chiffrement sont distingués et prouvés séparément ;
- le script signale les clés API dépassant 90 jours ;
- le livrable est versionné sous la convention demandée.
