# Estimer et comparer le coût mensuel d'une migration

## Objectif

Estimer et comparer le coût mensuel d'une migration de l'infrastructure **DIST-01a** sur deux fournisseurs cloud : **OVHcloud** et **AWS**.

Un plan de migration sans estimation de coût n'est pas exploitable pour une PME. Le but n'est pas d'obtenir un chiffre exact au centime près, mais un ordre de grandeur réaliste, daté, justifié et reproductible.

!!! warning "Prix cloud"
    Les prix évoluent régulièrement et diffèrent selon la région, l'engagement, le type d'instance, le stockage, le trafic sortant et les options retenues. Toujours documenter la date et les hypothèses utilisées.

## Ce que tu vas faire, et pourquoi

| Étape | Travail à faire | Pourquoi |
| --- | --- | --- |
| 1 | Reprendre l'inventaire de composants DIST-01a. | Ne pas estimer une infrastructure imaginaire. |
| 2 | Définir le nombre de VM de production à retenir. | Garder un périmètre réaliste pour une PME. |
| 3 | Estimer une VM équivalente chez OVHcloud. | Obtenir un coût mensuel fournisseur européen. |
| 4 | Estimer une instance EC2 équivalente chez AWS. | Obtenir un coût mensuel fournisseur non européen. |
| 5 | Ajouter stockage et sortie de données. | Éviter de ne compter que le CPU/RAM. |
| 6 | Comparer les deux résultats. | Justifier le choix économique et technique. |

## Cadrage du périmètre

Si l'infrastructure DIST-01a compte de nombreuses VM annexes, postes de test, sauvegardes ponctuelles ou environnements temporaires, ne pas les compter une par une.

Pour une PME, retenir en général un ordre de grandeur de **3 à 6 VM de production** :

- serveur web ou frontal applicatif ;
- base de données ;
- service applicatif ;
- annuaire ou IAM ;
- bastion ou service d'administration ;
- supervision ou service annexe.

Le nombre retenu doit venir de ton inventaire. Dans cette feuille, l'hypothèse choisie est volontairement plus compacte : **1 VM principale** qui regroupe les services DIST-01a, car l'infrastructure on-premise observée correspond davantage à un laboratoire PME consolidé qu'à plusieurs serveurs de production séparés.

Cette hypothèse est acceptable si elle est clairement présentée comme une estimation de migration minimale. Elle évite de gonfler artificiellement le coût avec des VM annexes ou des postes de test qui ne seraient pas migrés tels quels.

## Hypothèses à documenter

| Hypothèse | OVHcloud | AWS | Scaleway |
| --- | --- | --- | --- |
| Date de consultation | `2026-08-12` | `2026-08-12` | `2026-08-12` |
| Région | Europe | Europe | Europe |
| Devise | EUR HT ou TTC à préciser | EUR HT ou TTC à préciser | EUR HT ou TTC à préciser |
| Durée | 1 mois | 1 mois | 1 mois |
| Engagement | À la demande / sans engagement | On-Demand | Mensuel / sans engagement à confirmer |
| Nombre de VM retenu | 1 VM | 1 VM | 1 VM |
| Type de VM retenu | `d2-4` | `t4g.medium` | `VPS-PRO-2-S` |
| vCPU par VM | 2 vCPU | 2 vCPU | 2 vCPU |
| RAM par VM | 4 Go | 4 GiB | 4 Go |
| Stockage par VM | 50 Go inclus | EBS séparé | 75 Go SSD NVMe inclus |
| Bande passante | 250 Mbit/s public max., 250 Mbit/s privé | Jusqu'à 5 Gbit/s | 400 Mbit/s |
| Sortie de données estimée | 2 Go | 2 Go | 2 Go |
| Services managés inclus | Non | Non | Non |

!!! tip "Règle de preuve"
    Une capture du calculateur doit montrer les hypothèses et le total, mais pas de clé d'accès, token, identifiant de facturation privé ou moyen de paiement.

## Inventaire de coût DIST-01a

Partir des dépendances déjà cartographiées, puis regrouper les services qui peuvent vivre sur une même VM.

Pour cette estimation, les services sont regroupés sur **une VM unique**. Ce choix correspond à une migration économique et simple du laboratoire on-premise : les conteneurs restent regroupés, et les coûts de services managés sont exclus.

| Groupe technique | Services DIST-01a possibles | VM retenue ? | Justification |
| --- | --- | --- | --- |
| Annuaire | OpenLDAP, LAM | Inclus dans la VM principale | Dépendance centrale, mais charge faible dans le contexte de formation. |
| Messagerie | Postfix, Dovecot, Roundcube, MariaDB Roundcube | Inclus dans la VM principale | Regroupement cohérent avec l'existant on-premise. |
| Fichiers | Samba et partages | Inclus dans la VM principale | Les volumes restent à estimer, mais pas de VM séparée retenue. |
| Supervision | Filebeat, Elasticsearch, Kibana | Inclus dans la VM principale | Choix économique ; à séparer seulement si la charge augmente. |
| PKI | Step CA | Inclus dans la VM principale | Service léger dans ce périmètre de laboratoire. |
| Sauvegarde | BorgBackup, dépôt de sauvegarde | Stockage additionnel estimé séparément | Le service ne justifie pas une VM dédiée dans cette estimation. |
| Bastion | Accès admin SSH/VPN | Non retenu | Pas de bastion dédié dans l'hypothèse minimale. |

## Estimation OVHcloud

Utiliser le simulateur OVHcloud :

- <https://www.ovhcloud.com/fr/public-cloud/prices/>
- <https://pricelist.ovh/calculator.html>

À compléter avec le simulateur :

| Élément | Hypothèse | Coût mensuel |
| --- | --- | ---: |
| VM principale équivalente DIST-01a | `d2-4` : 2 vCPU, 4 Go RAM | `0,0206 EUR/h` |
| Nombre de VM retenu | `1` VM | Inclus dans le calcul |
| Stockage bloc ou volume additionnel | 50 Go inclus dans la VM | 0 EUR si le disque inclus suffit |
| Stockage objet ou sauvegarde | `2` Go | À renseigner |
| Sortie de données estimée | `2` Go/mois | À renseigner |
| IP publique, snapshot ou option éventuelle | Non retenu dans l'hypothèse de base | À renseigner si facturé |
| **Total compute OVHcloud estimé** | `0,0206 x 730 h` | **15,04 EUR/mois** |
| **Total OVHcloud estimé** | Compute + stockage/sauvegarde/egress à confirmer | **15,04 EUR/mois + options** |

Notes à conserver :

- région choisie ;
- type d'instance ou flavor ;
- stockage inclus ou ajouté ;
- règle appliquée au trafic sortant ;
- engagement ou absence d'engagement.

## Estimation AWS

Utiliser l'AWS Pricing Calculator :

- <https://calculator.aws/>
- <https://aws.amazon.com/aws-cost-management/aws-pricing-calculator/>

À compléter avec l'AWS Pricing Calculator :

| Élément | Hypothèse | Coût mensuel |
| --- | --- | ---: |
| Instance EC2 équivalente DIST-01a | `t4g.medium` : 2 vCPU, 4 GiB RAM, ARM Graviton | `0.0376/h` |
| Nombre d'instances retenu | `1` instance | Inclus dans le calcul |
| EBS par instance | `10` Go, type à préciser | À renseigner |
| Snapshot ou sauvegarde | `2` Go | À renseigner |
| Sortie de données estimée | `2` Go/mois | À renseigner |
| IP publique, NAT Gateway ou option éventuelle | Non retenu dans l'hypothèse de base | À renseigner si facturé |
| **Total compute AWS On-Demand estimé** | `0.0376 x 730 h` | **27,45 par mois, devise du calculateur à confirmer** |
| **Total compute AWS engagé 1 an estimé** | `0.0141 x 730 h`, soit environ `62 %` d'économie | **10,29 par mois, devise du calculateur à confirmer** |
| **Total AWS estimé** | Compute + EBS/sauvegarde/egress à confirmer | **27,45 par mois + options** |

Notes à conserver :

- région choisie ;
- type d'instance EC2 ;
- architecture processeur, ici ARM Graviton pour `t4g.medium` ;
- système d'exploitation ;
- type de volume EBS ;
- quantité de données sortantes ;
- On-Demand, Reserved Instance ou Savings Plan.

!!! warning "Comparaison technique"
    `d2-4` et `t4g.medium` sont plus proches pour l'infrastructure complète : 2 vCPU et environ 4 Go de RAM. Elles ne sont toutefois pas strictement équivalentes : OVHcloud inclut 50 Go de stockage, tandis que `t4g.medium` nécessite un volume EBS séparé. `t4g.medium` utilise aussi une architecture ARM Graviton : il faut vérifier que les images Docker, paquets et outils utilisés par DIST-01a sont compatibles ARM.

## Estimation Scaleway

Estimation relevée pour un troisième fournisseur souverain :

| Élément | Hypothèse | Coût mensuel |
| --- | --- | ---: |
| VM principale équivalente DIST-01a | `VPS-PRO-2-S` : 2 vCPU, 4 Go RAM | Inclus dans l'offre |
| Nombre de VM retenu | `1` VM | Inclus dans le calcul |
| Stockage bloc ou volume additionnel | 75 Go SSD NVMe inclus | 0 EUR si le disque inclus suffit |
| Bande passante | 400 Mbit/s | Inclus selon l'offre relevée |
| Stockage objet ou sauvegarde | `2` Go | À renseigner si service séparé |
| Sortie de données estimée | `2` Go/mois | À confirmer selon conditions réseau |
| IP publique, snapshot ou option éventuelle | Non retenu dans l'hypothèse de base | À renseigner si facturé |
| **Total Scaleway estimé** | 1 mois, hypothèses ci-dessus | **10,49 EUR/mois + options** |

Notes à conserver :

- offre exacte : `VPS-PRO-2-S` ;
- type de disque : SSD NVMe ;
- bande passante : 400 Mbit/s ;
- conditions de trafic sortant ;
- SLA et support associés à l'offre.

## Tableau comparatif final

| Critère | OVHcloud | AWS | Scaleway | Commentaire |
| --- | ---: | ---: | ---: | --- |
| Coût VM / compute | 15,04 EUR/mois | 27,45/mois, devise à confirmer | 10,49 EUR/mois | Calcul sur 1 VM, hors options. |
| Coût stockage | 50 Go inclus dans la VM | EBS à ajouter | 75 Go SSD NVMe inclus | Inclure volumes persistants et sauvegardes. |
| Coût sortie de données | À renseigner | À renseigner | À confirmer | Documenter l'hypothèse d'egress. |
| Options réseau ou IP | À renseigner | À renseigner | À renseigner | Attention aux services réseau facturés. |
| Total mensuel estimé | 15,04 EUR/mois + options | 27,45/mois + EBS/options | 10,49 EUR/mois + options | Montant à dater et devise AWS à confirmer. |
| Écart mensuel vs OVHcloud | Référence | +12,41/mois hors EBS/options | -4,55 EUR/mois | Différence brute sur l'offre principale. |
| Avantage principal | 4 Go RAM, 50 Go inclus, fournisseur européen | Écosystème AWS, engagement 1 an fortement réduit | Prix le plus bas, 75 Go NVMe inclus, fournisseur souverain | Scaleway devient très compétitif économiquement. |
| Risque principal | Moins de services cloud avancés que l'écosystème AWS | EBS séparé, architecture ARM à vérifier, coût On-Demand plus élevé | SLA/support et conditions exactes à vérifier | Ne pas comparer uniquement le prix mensuel. |
| souveraintée | respecte le RGPD | American Act, qui autorise à la lecture & à la suppression des données | Respecte le RGPD | Ovh & Scaleway sont les meilleurs candidats |

Formule d'écart :

```text
écart = coût AWS - coût OVHcloud
écart en % = (écart / coût OVHcloud) x 100
```

## Exemple de calcul à compléter

!!! example "Exemple à remplacer par les vrais calculateurs"
    Les valeurs ci-dessous ne sont pas un devis. Elles servent uniquement à montrer comment additionner les postes de coût une fois les montants récupérés dans les calculateurs officiels.

| Hypothèse retenue | Valeur |
| --- | --- |
| Nombre de VM | 1 |
| Profil OVHcloud | `d2-4`, 2 vCPU, 4 Go RAM, 50 Go disque |
| Profil AWS | `t4g.medium`, 2 vCPU, 4 GiB RAM, EBS only |
| Profil Scaleway | `VPS-PRO-2-S`, 2 vCPU, 4 Go RAM, 75 Go SSD NVMe |
| Stockage bloc | 50 Go inclus côté OVHcloud, 10 Go EBS à chiffrer côté AWS, 75 Go inclus côté Scaleway |
| Sauvegarde ou stockage additionnel | 2 Go |
| Sortie de données | 2 Go/mois |
| Engagement | À la demande, 1 mois |

| Fournisseur | Compute | Stockage | Egress | Total mensuel |
| --- | ---: | ---: | ---: | ---: |
| OVHcloud | 15,04 EUR/mois | 0 EUR si 50 Go inclus suffisent | À renseigner | 15,04 EUR/mois + egress/options |
| AWS On-Demand | 27,45/mois, devise à confirmer | À renseigner pour 10 Go EBS | À renseigner | 27,45/mois + EBS/egress/options |
| AWS engagé 1 an | 10,29/mois, devise à confirmer | À renseigner pour 10 Go EBS | À renseigner | 10,29/mois + EBS/egress/options |
| Scaleway | 10,49 EUR/mois | 0 EUR si 75 Go inclus suffisent | À confirmer | 10,49 EUR/mois + egress/options |

Lecture :

- l'hypothèse porte sur une VM consolidée, pas sur une architecture multi-VM ;
- les montants réels doivent venir des calculateurs officiels ;
- la devise doit être normalisée avant comparaison finale ;
- les taxes doivent être indiquées comme incluses ou non incluses ;
- si le calculateur impose un profil légèrement différent, noter le profil réellement choisi ;
- l'engagement AWS réduit fortement le coût compute, mais le stockage EBS et la compatibilité ARM doivent être ajoutés à l'analyse.

## Pour aller plus loin

Recalculer le coût avec un engagement de 1 an :

| Fournisseur | Tarif à la demande | Tarif engagé 1 an | Économie | Économie en % |
| --- | ---: | ---: | ---: | ---: |
| OVHcloud | 15,04 EUR/mois + options | À renseigner | À calculer | À calculer |
| AWS | 27,45/mois + options | 10,29/mois + options | 17,16/mois sur le compute | 62 % sur le compute |
| Scaleway | 10,49 EUR/mois + options | À renseigner | À calculer | À calculer |

Formule :

```text
économie = coût à la demande - coût engagé
économie en % = (économie / coût à la demande) x 100
```

Comparer ensuite le gain financier avec les contraintes :

- engagement plus long ;
- flexibilité réduite ;
- risque de surdimensionnement ;
- évolution possible de l'infrastructure pendant l'année.

## Preuves à conserver

| Preuve | Contenu attendu |
| --- | --- |
| Inventaire des VM retenues | Nombre de VM de production et justification. |
| Capture OVHcloud | Hypothèses visibles, région, type d'instance, stockage, total. |
| Capture AWS Calculator | Hypothèses visibles, région, instance EC2, EBS, egress, total. |
| Tableau comparatif | Coûts mensuels et écart calculé. |
| Hypothèses datées | Date, région, devise, engagement, limites de l'estimation. |
| Variante 1 an | Coût engagé et pourcentage d'économie, si réalisé. |

## État final attendu

À la fin de cette feuille :

- le nombre de VM de production DIST-01a est cadré ;
- le coût mensuel OVHcloud est estimé avec le calculateur officiel ;
- le coût mensuel AWS est estimé avec le calculateur officiel ;
- le stockage et la sortie de données sont inclus ;
- les hypothèses sont datées et vérifiables ;
- le choix économique peut être expliqué à une PME.

## Ressources

- [OVHcloud - Public Cloud prices](https://www.ovhcloud.com/fr/public-cloud/prices/)
- [OVHcloud - Cost Calculator](https://pricelist.ovh/calculator.html)
- [AWS Pricing Calculator](https://calculator.aws/)
- [AWS Pricing Calculator - Présentation](https://aws.amazon.com/aws-cost-management/aws-pricing-calculator/)
