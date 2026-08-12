# Lire et interpréter un SLA cloud

!!! info "Durée indicative"
    1 h.

## Objectif

Savoir lire et interpréter un **SLA cloud** avant de choisir un fournisseur ou de valider une architecture de migration pour **DIST-01a**.

Un SLA, ou **Service Level Agreement**, précise le niveau de service annoncé par un fournisseur : disponibilité, périmètre couvert, exclusions, responsabilités du client, compensations possibles et procédure de déclaration d'incident.

## Ce que tu vas faire, et pourquoi

Un pourcentage de disponibilité peut sembler très rassurant. Pourtant, il faut toujours vérifier :

- quel service est réellement couvert ;
- sur quelle période la disponibilité est calculée ;
- quelles pannes sont exclues ;
- quelles actions restent à la charge du client ;
- quelle compensation est prévue ;
- comment déclarer l'incident dans les délais.

Pour une PME comme **Embedded Solutions**, un SLA ne doit pas être lu comme une garantie magique. C'est un engagement contractuel limité, qui complète mais ne remplace pas une architecture résiliente, des sauvegardes et un plan de reprise.

## Calculer l'indisponibilité tolérée

| Disponibilité annoncée | Indisponibilité annuelle approximative | Lecture simple |
| ---: | ---: | --- |
| 99 % | 3 jours 15 h 36 min | Insuffisant pour un service critique. |
| 99,5 % | 1 jour 19 h 48 min | Acceptable seulement pour des services peu critiques. |
| 99,9 % | 8 h 45 min | Niveau courant, mais encore plusieurs heures d'arrêt possibles par an. |
| 99,95 % | 4 h 23 min | Meilleur niveau, mais pas zéro panne. |
| 99,99 % | 52 min | Niveau élevé, souvent plus coûteux ou conditionné. |
| 99,999 % | 5 min | Très exigeant, rarement atteint sans architecture multi-zone. |

Formule :

```text
indisponibilité annuelle = 365 jours x 24 h x (1 - taux de disponibilité)
```

Exemple :

```text
99,9 % = 0,1 % d'indisponibilité
365 x 24 x 0,001 = 8,76 h/an
```

## Grille de lecture d'un SLA

| Point à lire | Question à poser | Pourquoi c'est important |
| --- | --- | --- |
| Service couvert | Le SLA concerne-t-il la VM, le stockage, le réseau, la base, le DNS ou le support ? | Un fournisseur peut avoir un SLA différent pour chaque service. |
| Taux annoncé | 99,9 %, 99,99 %, autre ? | Le pourcentage se traduit en temps d'arrêt acceptable. |
| Période de mesure | Mensuelle, annuelle, par région, par compte ? | Un incident court peut ne pas déclencher de compensation selon la période retenue. |
| Périmètre géographique | Région, zone, datacenter, service global ? | Une architecture mono-zone n'a pas les mêmes garanties qu'une architecture multi-zone. |
| Exclusions | Maintenance planifiée, force majeure, mauvaise configuration client ? | Certaines indisponibilités ne comptent pas dans le SLA. |
| Responsabilités client | Redondance, sauvegarde, supervision, déclaration d'incident ? | Le fournisseur ne couvre pas les erreurs d'architecture du client. |
| Compensation | Crédit de service, remboursement partiel, aucun crédit ? | La compensation est souvent limitée et ne couvre pas la perte métier. |
| Procédure de réclamation | Délai, preuves, ticket, logs, identifiants de ressources ? | Sans dossier complet, le crédit SLA peut être refusé. |
| Support associé | Standard, Business, Enterprise ? | Le SLA technique et le niveau de support ne sont pas toujours la même chose. |

!!! warning "SLA, SLO et support"
    Un SLA est un engagement contractuel. Un SLO est un objectif de niveau de service. Un niveau de support définit surtout les moyens d'assistance, les délais de réponse et l'escalade. Il ne faut pas mélanger ces trois notions.

## Application à DIST-01a

L'estimation actuelle retient une migration compacte sur une VM principale :

- OVHcloud `d2-4` ;
- AWS `t4g.medium`.

Pour cette architecture, le SLA à lire ne doit pas seulement couvrir la VM. Il faut aussi regarder les dépendances autour.

| Élément DIST-01a | SLA ou engagement à vérifier | Risque si oublié |
| --- | --- | --- |
| VM principale | Disponibilité compute, redémarrage, panne hôte | Tous les services regroupés tombent ensemble. |
| Stockage | Persistance disque, volume attaché, sauvegardes, snapshots | Perte ou indisponibilité des données. |
| Réseau public | Bande passante, IP publique, filtrage, incident réseau | Services web/mail/SSH inaccessibles. |
| Réseau privé | Communication entre composants si l'architecture évolue | Rupture entre VM, base, annuaire ou sauvegarde. |
| DNS | Résolution des noms de service | Clients incapables de trouver les services. |
| Support | Délai de réponse et procédure d'escalade | Incident prolongé faute de prise en charge rapide. |
| Sauvegardes | Engagement sur stockage, restauration et disponibilité des dépôts | PRA impossible malgré un compute disponible. |

## Comparer OVHcloud et AWS

| Critère | OVHcloud | AWS |
| --- | --- | --- |
| Où lire les engagements | Pages d'engagements, support levels, contrats du service retenu | Page centrale AWS Service Level Agreements, puis SLA du service concerné |
| Structure habituelle | Engagements dépendants de l'offre, du support et du produit | SLA séparés par service AWS |
| Point de vigilance | Distinguer support, SLO et SLA contractuel | Lire le SLA EC2 mais aussi EBS, réseau, DNS ou autres services utilisés |
| Réclamation | Vérifier procédure, délais et preuves attendues | Vérifier service credits, seuils et procédure par service |
| Impact pour DIST-01a | Simple si une seule VM, mais forte dépendance à ce point unique | SLA compute seul insuffisant si EBS ou réseau ne sont pas intégrés dans l'analyse |

## Comparaison objective des engagements

À partir du SLA Public Cloud d'OVHcloud et du SLA Compute/EC2 d'AWS, compléter ou vérifier le tableau suivant.

| Critère | OVHcloud Public Cloud Instance | AWS EC2 |
| --- | --- | --- |
| Disponibilité annoncée | 99,99 % de disponibilité mensuelle pour les Public Cloud Instances. | 99,5 % pour une instance EC2 seule ; 99,99 % au niveau région si les instances tournent sur au moins deux AZ ou régions selon les conditions AWS. |
| Principales exclusions | Maintenance planifiée ou sans impact, mauvaise utilisation du service, équipements ou logiciels client, version obsolète ou mise à jour non appliquée, incidents hors contrôle direct OVHcloud, problèmes réseau au-delà du routeur de bordure, attaques, force majeure, responsabilités de sécurité client non respectées. | Force majeure ou facteurs hors contrôle AWS, problèmes Internet hors point de démarcation EC2, actions ou inactions du client, équipement ou logiciel client, suspension ou résiliation du droit d'utiliser EC2. |
| Compensation en cas de manquement | Crédit de service si la disponibilité mensuelle confirmée passe sous l'engagement. Pour les Public Cloud Instances, le tableau SLA indique notamment 10 % de crédit si la disponibilité est inférieure à 99,99 % et supérieure ou égale à 95 %, puis jusqu'à 100 % selon le niveau confirmé. Les crédits sont le seul recours prévu. | Crédit de service sur la facture EC2 concernée : 10 %, 30 % ou 100 % selon le niveau de disponibilité atteint. Le crédit s'applique sur des paiements futurs et constitue le recours exclusif prévu par le SLA. |
| Procédure de déclaration d'incident | Ouvrir une demande via l'espace client OVHcloud dans les 60 jours calendaires suivant l'incident supposé. L'indisponibilité commence à être comptée quand le cas support est créé. OVHcloud utilise ses propres outils et enregistrements pour valider l'incident. | Ouvrir un cas dans l'AWS Support Center avant la fin du deuxième cycle de facturation suivant l'incident. La demande doit inclure le libellé SLA requis, dates/heures, région/AZ, identifiants de ressources et logs. Les informations sensibles doivent être masquées. |

!!! warning "Lecture pour notre scénario"
    Avec une seule instance `t4g.medium`, l'engagement AWS pertinent est l'**Instance-Level SLA** à 99,5 %, pas le Region-Level SLA à 99,99 %. Pour bénéficier du niveau régional, il faut une architecture redondée sur plusieurs zones de disponibilité ou régions, ce qui change le coût et la complexité.

## Indisponibilité annuelle tolérée

| Fournisseur / scénario | Disponibilité utilisée | Indisponibilité annuelle approximative | Indisponibilité en minutes |
| --- | ---: | ---: | ---: |
| OVHcloud Public Cloud Instance | 99,99 % | 52 min 34 s | 53 min |
| AWS EC2 - instance seule | 99,5 % | 1 jour 19 h 48 min | 2 628 min |
| AWS EC2 - architecture multi-AZ/région | 99,99 % | 52 min 34 s | 53 min |

Lecture :

- OVHcloud et AWS peuvent être comparables à **99,99 %** seulement si l'architecture AWS respecte les conditions du SLA régional ;
- dans l'hypothèse actuelle à **une seule VM**, AWS annonce un niveau beaucoup plus bas pour l'instance isolée ;
- le SLA ne couvre pas automatiquement la perte de données, une mauvaise configuration, un service applicatif mal déployé ou une sauvegarde absente.

## Comparaison avec un RTO PME

Pour un service critique de PME, on peut retenir comme hypothèse de travail :

| Service DIST-01a | RTO acceptable estimé | Commentaire |
| --- | ---: | --- |
| OpenLDAP | 1 h | Sans annuaire, les authentifications des services dépendants deviennent fragiles. |
| Messagerie | 4 h | Une interruption courte est acceptable, mais une journée perdue devient bloquante. |
| Samba / fichiers | 4 h | Dépend de la criticité des documents partagés. |
| Supervision | 8 h | Moins visible utilisateur, mais critique pendant un incident. |
| Sauvegardes | 24 h | Le RPO compte autant que le RTO : il faut éviter la perte de données. |

Conclusion pour DIST-01a :

- 99,99 % correspond à environ **53 minutes/an**, cohérent avec un RTO critique d'environ 1 h ;
- 99,5 % correspond à environ **2 628 minutes/an**, soit plus de 43 h, trop élevé pour un annuaire ou une messagerie critique si aucune solution de reprise n'est prévue ;
- une VM unique reste acceptable pour un prototype ou une petite infrastructure de formation, mais pas comme seule garantie de continuité pour un service PME critique.

## Exemple d'interprétation

Si une VM unique héberge OpenLDAP, messagerie, Samba, supervision et sauvegarde locale, un SLA compute de 99,9 % signifie que l'indisponibilité annuelle tolérée peut atteindre environ **8 h 45**.

Pour DIST-01a, cela veut dire :

- les utilisateurs peuvent perdre l'accès à la messagerie ;
- les authentifications LDAP peuvent échouer ;
- les partages Samba peuvent devenir inaccessibles ;
- la supervision peut ne plus recevoir de logs ;
- la sauvegarde locale peut être interrompue.

Conclusion : le SLA fournisseur doit être complété par des mesures client :

- sauvegardes restaurables ;
- export régulier des configurations ;
- supervision externe ou indépendante ;
- procédure de redémarrage et restauration ;
- documentation d'escalade support.

## Questions à poser avant validation

| Question | Réponse attendue |
| --- | --- |
| Quel SLA couvre la VM choisie ? | À relever dans le contrat ou la page officielle du service. |
| Le stockage est-il couvert séparément ? | Oui/non, avec lien vers l'engagement applicable. |
| Les maintenances planifiées sont-elles exclues ? | À documenter. |
| Une erreur de configuration client est-elle couverte ? | En général non. |
| Quel crédit est prévu en cas de non-respect ? | Pourcentage ou crédit de service à relever. |
| Comment prouver l'incident ? | Ticket, logs, heures de début/fin, ressources impactées. |
| Quel niveau de support est nécessaire ? | Standard, Business, Enterprise ou équivalent. |

## Pour aller plus loin

Comparer deux scénarios :

| Scénario | Lecture SLA | Limite |
| --- | --- | --- |
| 1 VM unique | Simple et économique | Point unique de défaillance. |
| 2 VM ou architecture redondée | Meilleure résilience possible | Coût, complexité et configuration plus élevés. |

L'objectif est d'expliquer que le SLA du fournisseur et l'architecture du client travaillent ensemble. Un bon SLA ne compense pas une architecture fragile.

## Preuves à conserver

| Preuve | Contenu attendu |
| --- | --- |
| Capture ou lien SLA AWS | Page AWS SLA du service utilisé, par exemple EC2 si instance retenue. |
| Capture ou lien OVHcloud | Page d'engagement ou contrat associé à l'offre retenue. |
| Tableau d'indisponibilité | Conversion du pourcentage en durée annuelle. |
| Analyse DIST-01a | Impact d'une indisponibilité sur LDAP, mail, Samba, supervision et sauvegarde. |
| Procédure d'escalade | Où ouvrir un ticket, quelles preuves collecter, délai de réclamation. |

## État final attendu

À la fin de cette feuille :

- tu sais convertir un taux de disponibilité en durée d'indisponibilité ;
- tu sais distinguer SLA, SLO et support ;
- tu sais lire les exclusions et responsabilités client ;
- tu sais relier le SLA à l'architecture réelle de DIST-01a ;
- tu sais expliquer pourquoi un SLA ne remplace pas les sauvegardes, la supervision et le PRA.

## Ressources

- [AWS - Service Level Agreements](https://aws.amazon.com/legal/service-level-agreements/)
- [AWS - Amazon Compute Service Level Agreement](https://aws.amazon.com/compute/sla/)
- [AWS - What is a Service Level Agreement?](https://aws.amazon.com/what-is/service-level-agreement/)
- [OVHcloud - Support levels](https://www.ovhcloud.com/en/support-levels/plans/)
- [OVHcloud - Standard Support](https://www.ovhcloud.com/en/support-levels/standard/)
