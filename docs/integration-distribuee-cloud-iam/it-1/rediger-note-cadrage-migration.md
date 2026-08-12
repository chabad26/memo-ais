# Rédiger une note de cadrage de migration

## Objectif

Rédiger une note de cadrage synthétique validant le principe de la migration cloud de **DIST-01a**.

Cette note s'adresse à la direction fictive de la PME **Embedded Solutions**. Elle doit permettre de décider si le principe de la migration est validé avant de produire un plan de migration détaillé.

## Ce que tu vas faire, et pourquoi

Avant de plonger dans les scénarios techniques, il faut expliquer simplement :

- pourquoi migrer ;
- ce que la migration doit améliorer ;
- quelles contraintes doivent être respectées ;
- comment mesurer le succès ;
- quels risques peuvent faire échouer le projet.

La note de cadrage est un outil de communication. Elle doit tenir sur **une page maximum** : claire, lisible et orientée décision.

## Méthode

| Étape | Contenu attendu |
| --- | --- |
| 1 | Rappeler le contexte Embedded Solutions et l'existant DIST-01a. |
| 2 | Formuler les objectifs de la migration. |
| 3 | Lister les contraintes principales : budget, souveraineté, délai, sécurité, réversibilité. |
| 4 | Définir les critères de succès. |
| 5 | Ajouter les risques et les mesures d'anticipation. |
| 6 | Conclure par une recommandation de validation ou de réserve. |

## Modèle de note de cadrage

### Note de cadrage - Migration cloud DIST-01a

| Élément | Contenu |
| --- | --- |
| Destinataire | Direction de la PME Embedded Solutions |
| Objet | Validation du principe de migration de l'infrastructure DIST-01a vers le cloud |
| Date | 2026-08-12 |
| Auteur | Olivier Himblot |

### 1. Contexte

L'infrastructure DIST-01a est actuellement exploitée en environnement on-premise. Elle regroupe des services structurants pour une PME : annuaire OpenLDAP, messagerie, partages Samba, supervision, sauvegarde BorgBackup et certificats internes.

La migration cloud est étudiée pour améliorer la souplesse d'exploitation, la reproductibilité du déploiement, la capacité de reprise et la maîtrise des coûts. Les analyses préalables ont identifié une approche minimale basée sur une VM principale regroupant les services, afin de rester cohérent avec le périmètre réel de l'infrastructure on-premise.

### 2. Objectifs

| Objectif | Résultat attendu |
| --- | --- |
| Réduire la dépendance au poste ou serveur local | Les services peuvent être redéployés sur une infrastructure cloud documentée. |
| Améliorer la reprise après incident | Les sauvegardes, exports et procédures permettent une restauration contrôlée. |
| Comparer deux fournisseurs | OVHcloud et AWS sont évalués selon coût, souveraineté, contraintes techniques et risques juridiques. |
| Préparer l'automatisation | Le futur déploiement doit pouvoir être décrit avec OpenTofu et Ansible. |
| Garder la maîtrise des secrets | Les `.env`, clés, passphrases et tokens ne doivent pas être exposés dans Git. |

### 3. Contraintes

| Contrainte | Cadrage retenu |
| --- | --- |
| Budget | Estimation mensuelle à documenter avec les calculateurs OVHcloud et AWS. |
| Souveraineté | OVHcloud est favorable pour réduire l'exposition à un droit extra-européen ; AWS nécessite une analyse Cloud Act/RGPD plus poussée. |
| Délai | Migration progressive, sans interrompre tous les services simultanément. |
| Sécurité | Chiffrement, sauvegardes, contrôle des accès et protection des secrets obligatoires. |
| Réversibilité | Les données et configurations doivent pouvoir être exportées et restaurées hors du fournisseur choisi. |
| Compatibilité | Les images, paquets et scripts doivent être vérifiés, notamment si une instance ARM AWS est retenue. |

### 4. Critères de succès

La migration sera considérée comme réussie si :

- les services principaux démarrent sur l'environnement cible ;
- OpenLDAP, messagerie, Samba, supervision et sauvegardes sont validés par tests ;
- les données critiques sont restaurables ;
- les accès et secrets ne sont pas exposés ;
- le coût mensuel est cohérent avec le budget PME ;
- les contraintes RGPD, Cloud Act et souveraineté sont documentées ;
- un retour arrière reste possible.

### 5. Risques et anticipation

| Risque | Impact | Anticipation |
| --- | --- | --- |
| Sous-dimensionnement de la VM | Services lents ou instables | Partir sur une taille réaliste pour toute l'infra et mesurer CPU/RAM après migration. |
| Dépendance LDAP mal migrée | Authentifications impossibles | Migrer ou rendre OpenLDAP accessible avant les services dépendants. |
| Perte de données | Interruption métier et reprise difficile | Tester les sauvegardes BorgBackup et les exports avant toute bascule. |
| Coûts sous-estimés | Dépassement budgétaire | Inclure compute, stockage, egress, snapshots et options réseau. |
| Risque juridique mal évalué | Choix fournisseur contestable | Documenter RGPD, Cloud Act, localisation, sous-traitants et chiffrement. |
| Secrets exposés | Compromission des accès | Utiliser SOPS, git-crypt ou coffre-fort ; ne jamais publier `.env` ou clés privées. |

### 6. Recommandation

Le principe de migration peut être validé pour une phase d'étude et de prototype, sous réserve de conserver une approche progressive :

1. finaliser le chiffrage OVHcloud/AWS ;
2. confirmer le fournisseur privilégié selon coût et souveraineté ;
3. tester la restauration des données ;
4. automatiser le socle avec OpenTofu et Ansible ;
5. documenter les preuves et les écarts avant toute bascule définitive.

## Version ultra-courte à remettre

> La migration cloud de DIST-01a est pertinente pour améliorer la reproductibilité, la reprise après incident et la maîtrise de l'infrastructure. Le périmètre retenu est volontairement compact : une VM principale regroupant les services actuels, avec stockage, sauvegarde et supervision à valider. OVHcloud présente un avantage de souveraineté et de coût on-demand dans l'estimation actuelle ; AWS reste intéressant par son écosystème et ses engagements tarifaires, mais demande une analyse renforcée RGPD/Cloud Act et une vérification de compatibilité ARM. La direction peut valider le principe d'une phase de prototype, à condition de confirmer les coûts, tester les restaurations et protéger les secrets.

## Preuves à conserver

| Preuve | Contenu attendu |
| --- | --- |
| Note de cadrage | Une page maximum, compréhensible par une direction non technique. |
| Hypothèses | Périmètre, fournisseur comparé, budget, souveraineté, délai. |
| Critères de succès | Tests attendus et état final mesurable. |
| Risques | Risques principaux et mesures d'anticipation. |

## État final attendu

À la fin de cette feuille :

- la direction fictive d'Embedded Solutions dispose d'une note claire ;
- le principe de migration est justifié ;
- les contraintes majeures sont visibles ;
- les critères de succès sont mesurables ;
- les risques sont anticipés avant le plan détaillé.
