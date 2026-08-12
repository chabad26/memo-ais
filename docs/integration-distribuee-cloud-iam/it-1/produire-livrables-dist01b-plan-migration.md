# Produire les livrables DIST01b - Plan de migration

!!! info "Durée indicative"
    4 h 15.

## Objectif

Produire les deux premiers livrables du module à partir de l'infrastructure construite en **DIST-01a** et des travaux des séquences précédentes :

- cartographie des dépendances ;
- estimation de coût ;
- analyse souveraineté/RGPD/Cloud Act ;
- lecture des SLA ;
- note de cadrage.

Le livrable attendu doit permettre à **Embedded Solutions** de valider un scénario de migration cloud réaliste, argumenté et versionné dans le dépôt Git du module.

## Livrable attendu

Convention de nommage :

```text
Nom-Prénom-Grenoble-DIST01b-PlanMigration
```

Contenu attendu :

| Partie | Contenu |
| --- | --- |
| Plan de migration | Composants, dépendances, ordre de migration justifié. |
| Matrice de décision fournisseurs | Comparaison pondérée OVHcloud / AWS / Scaleway sur au moins 5 critères. |
| Note de cadrage | Version synthétique validant le principe de migration. |
| Preuves | Hypothèses, captures des calculateurs, liens SLA/juridiques, revue croisée. |

## Étape 1 - Auditer l'infrastructure on-premise

Reprendre la cartographie de dépendances et l'estimation de coût déjà réalisées.

### Synthèse du périmètre DIST-01a

| Domaine | Composants | Dépendances principales |
| --- | --- | --- |
| Identités | OpenLDAP, LAM | Volumes LDAP, secrets, réseau Docker, comptes applicatifs. |
| Messagerie | Postfix, Dovecot, Roundcube, MariaDB Roundcube | OpenLDAP, volumes mail, base Roundcube, certificats TLS. |
| Fichiers | Samba, partages | OpenLDAP, schéma Samba, volumes de partage, droits d'accès. |
| Sécurité | Step CA, certificats | Clé intermédiaire, provisionneur, certificats de services, chaîne de confiance. |
| Sauvegarde | BorgBackup | Exports LDAP, volumes, base Roundcube, passphrase Borg. |
| Supervision | Filebeat, Elasticsearch, Kibana | Journaux Docker/services, index `logs-infrastructure*`, tableaux de bord. |
| Réseau | Docker, DNS interne, ports publiés | Communication inter-services, accès client, validation TLS. |

### Hypothèse d'infrastructure cloud

L'hypothèse retenue pour l'estimation reste volontairement compacte :

| Fournisseur | VM retenue | Ressources | Coût compute estimé |
| --- | --- | --- | ---: |
| OVHcloud | `d2-4` | 2 vCPU, 4 Go RAM, 50 Go disque inclus | 15,04 EUR/mois |
| AWS | `t4g.medium` | 2 vCPU, 4 GiB RAM, EBS séparé | 27,45/mois On-Demand |
| AWS engagé 1 an | `t4g.medium` | 2 vCPU, 4 GiB RAM, EBS séparé | 10,29/mois sur le compute |
| Scaleway | `VPS-PRO-2-S` | 2 vCPU, 4 Go RAM, 75 Go SSD NVMe inclus | 10,49 EUR/mois |

!!! warning "Hypothèse à confirmer"
    Ces montants sont issus d'une estimation datée. Le stockage EBS, les sauvegardes, l'egress, les snapshots, le support et les options réseau doivent être confirmés dans les calculateurs officiels avant remise finale.

### Ordre de migration justifié

| Ordre | Lot | Justification | Critère de validation |
| ---: | --- | --- | --- |
| 1 | Sauvegardes et exports | Sécuriser les données avant toute modification. | Export LDAP, sauvegarde Borg, archive configs et base Roundcube vérifiés. |
| 2 | Socle réseau, DNS et accès admin | Préparer l'environnement cible sans impacter la production. | VM joignable, ports maîtrisés, accès SSH/VPN sécurisé. |
| 3 | PKI et certificats | Garantir TLS avant exposition des services. | Certificat racine distribué, certificats services validés. |
| 4 | OpenLDAP et LAM | L'annuaire est une dépendance centrale. | Bind LDAP, recherche utilisateur et accès LAM validés. |
| 5 | Messagerie | Postfix, Dovecot, Roundcube et MariaDB doivent être cohérents. | SMTP, IMAP, Roundcube et base Roundcube validés. |
| 6 | Samba et partages | Les droits dépendent des identités et des volumes. | Accès SMB, droits groupes et fichiers restaurés validés. |
| 7 | Supervision | Observer l'état final et les incidents post-migration. | Filebeat envoie les logs, Elasticsearch indexe, Kibana affiche les tableaux de bord. |
| 8 | Revue finale et bascule | Documenter les écarts et valider le retour arrière. | Tests finaux, journal de migration, décision go/no-go. |

## Étape 2 - Construire la matrice de décision pondérée

La matrice doit comparer au minimum cinq critères. La note finale est calculée ainsi :

```text
score pondéré = poids x note
```

Échelle proposée :

- poids de 1 à 5 ;
- note fournisseur de 1 à 5 ;
- 5 = très favorable ;
- 1 = défavorable ou risqué.

### Matrice OVHcloud / AWS / Scaleway

| Critère | Poids | OVHcloud - score | AWS - score | Scaleway - score | Justification |
| --- | ---: | ---: | ---: | ---: | --- |
| Technique | 4 | 16 | 16 | 16 | Les trois offres couvrent le besoin minimal : 2 vCPU et environ 4 Go de RAM. AWS impose de vérifier ARM Graviton et EBS séparé. |
| Économique | 4 | 20 | 12 | 20 | Scaleway est le moins cher en prix brut ; OVHcloud reste compétitif ; AWS On-Demand est plus coûteux hors engagement. |
| Opérationnel | 3 | 12 | 12 | 12 | Les trois fournisseurs sont exploitables pour une VM compacte, avec plus de paramètres côté AWS. |
| Contractuel / SLA | 3 | 12 | 9 | 9 | OVHcloud est mieux positionné dans l'analyse SLA retenue ; AWS instance seule est moins favorable ; Scaleway doit être vérifié sur le SLA/support exacts de l'offre. |
| Souveraineté / juridique | 5 | 25 | 15 | 25 | OVHcloud et Scaleway sont favorables au critère de souveraineté ; AWS demande une analyse Cloud Act/RGPD renforcée. |
| Réversibilité | 3 | 12 | 12 | 12 | Les trois restent réversibles si l'IaC, les sauvegardes et les exports sont correctement maintenus. |
| **Total** |   | **97** | **76** | **94** | OVHcloud garde l'avantage global, mais Scaleway devient une alternative souveraine très proche et moins chère. |

### Conclusion de la matrice

Dans le scénario actuel, **OVHcloud** est le fournisseur recommandé pour le prototype de migration de DIST-01a :

- coût On-Demand plus faible pour une VM proche du besoin ;
- stockage inclus dans l'offre retenue ;
- souveraineté plus favorable pour les données LDAP, mails, logs et sauvegardes ;
- SLA plus lisible dans un scénario à une seule VM.

L'ajout de **Scaleway** ne renverse pas complètement la conclusion, mais il change l'analyse économique : l'offre `VPS-PRO-2-S` est moins chère que l'offre OVHcloud retenue et inclut 75 Go de SSD NVMe. Scaleway devient donc une alternative souveraine crédible si Embedded Solutions privilégie le coût mensuel brut.

AWS reste pertinent si Embedded Solutions privilégie l'écosystème AWS, accepte un engagement d'un an, ou prévoit une architecture plus avancée multi-AZ. Dans ce cas, il faut intégrer le coût EBS, l'egress, la compatibilité ARM et l'analyse Cloud Act/RGPD.

## Note de cadrage intégrée

> La migration cloud de DIST-01a est pertinente pour Embedded Solutions afin d'améliorer la reproductibilité, la reprise après incident et la maîtrise de l'infrastructure. Le scénario retenu reste compact : une VM principale hébergeant les services actuels, avec stockage, sauvegarde, supervision et sécurité à valider. OVHcloud reste recommandé pour le prototype en raison de son équilibre entre coût, stockage inclus, souveraineté et lisibilité du SLA. Scaleway devient une alternative souveraine très compétitive grâce à son prix mensuel plus bas et à ses 75 Go de SSD NVMe inclus. AWS reste une option crédible pour son écosystème et ses engagements tarifaires, mais exige une analyse renforcée du stockage EBS, de la compatibilité ARM, du SLA instance seule et des enjeux Cloud Act/RGPD. La direction peut valider une phase de prototype, sous réserve de confirmer les coûts, tester les restaurations et documenter les écarts.

## Preuves à conserver

| Preuve | Contenu attendu |
| --- | --- |
| Plan de migration | Ordre des lots, dépendances et critères de validation. |
| Matrice de décision | Critères, poids, notes, scores et conclusion. |
| Coûts | Captures ou exports des calculateurs OVHcloud/AWS. |
| SLA | Liens/captures des engagements de service consultés. |
| Souveraineté | Analyse RGPD, Cloud Act, localisation et données concernées. |
| Revue croisée | 2 points forts, 2 points à clarifier, corrections apportées. |
| Git | Fichier versionné avec le nom demandé. |

## Pour aller plus loin

Ajouter un fournisseur souverain supplémentaire, par exemple 3DS Outscale, puis comparer avec la matrice déjà étendue à Scaleway :

| Critère | Poids | OVHcloud | AWS | Scaleway | 3DS Outscale | Commentaire |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Technique | 4 | 16 | 16 | 16 | À compléter | Comparer VM, stockage, réseau, IaC. |
| Économique | 4 | 20 | 12 | 20 | À compléter | Comparer compute, stockage, egress, engagement. |
| Opérationnel | 3 | 12 | 12 | 12 | À compléter | Support, documentation, outillage. |
| Contractuel / SLA | 3 | 12 | 9 | 9 | À compléter | Disponibilité, exclusions, crédits. |
| Souveraineté | 5 | 25 | 15 | 25 | À compléter | Droit applicable, qualification, sous-traitants. |

La conclusion doit indiquer si l'ajout d'un fournisseur supplémentaire change réellement la recommandation ou s'il confirme le choix initial.

## État final attendu

À la fin de cette feuille :

- le plan de migration DIST01b est structuré ;
- l'ordre de migration est justifié par les dépendances ;
- OVHcloud, AWS et Scaleway sont comparés avec une matrice pondérée ;
- la note de cadrage est intégrée ;
- la revue croisée est prévue ;
- le livrable peut être versionné dans Git avec la convention demandée.
