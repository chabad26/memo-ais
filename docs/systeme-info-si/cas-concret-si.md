# Cas concret SI (Système d'information)

## Cyberattaque du CHU de Rouen, novembre 2019

Le CHU de Rouen a subi le 15 novembre 2019 une cyberattaque de type rançongiciel, publiquement associée à Clop / CryptoMix Clop. L’incident a rendu indisponible une large partie du système d’information : applications métiers, postes de travail, serveurs et usages critiques comme admissions, prescriptions, analyses, radiologie, urgences et comptes rendus. L’établissement a basculé en mode dégradé, avec arrêt des ordinateurs, usage du papier, transmissions téléphoniques et ralentissement de plusieurs services. Les sources disponibles confirment une tentative d’extorsion et une plainte contre X, mais ne permettent pas d’affirmer avec certitude le point d’entrée exact, l’étendue complète du chiffrement, l’identité des auteurs ou l’absence définitive d’exfiltration de données.

### Éléments factuels structurants

| Point | Faits vérifiables |
| --- | --- |
| Date de l’incident | L’attaque est signalée le vendredi 15 novembre 2019, vers 19 h / 19 h 45 selon les sources. Le CHU indique une attaque « vers 19 heures » ; un retour d’expérience évoque un appel au support vers 19 h 45. |
| Établissement touché | Le CHU de Rouen, réparti sur cinq sites, avec plus de 10 000 salariés et près de 2 500 lits selon Le Monde. |
| Nature de l’attaque | Attaque par rançongiciel / cryptovirus : chiffrement de fichiers sur le système d’information. Le CHU parle de chiffrement de fichiers sur des ordinateurs et serveurs ; Le Monde et L’Usine Digitale identifient le rançongiciel Clop / CryptoMix Clop. |
| Mode opératoire général de Clop | L’ANSSI indique que Clop chiffre les documents présents sur les SI, ajoute une extension de type .CIop ou .Clop, et que le chiffrement peut être précédé d’une propagation manuelle dans le réseau victime pendant plusieurs jours. |
| Vecteur probable général | L’ANSSI rattache les attaques Clop observées en France à une vaste campagne d’hameçonnage autour du 16 octobre 2019, liée au groupe cybercriminel TA505. |
| Systèmes impactés | Le CHU indique que l’attaque a rendu inaccessible la plupart des applications métiers, infecté une partie des postes de travail, et chiffré des fichiers sur des ordinateurs et serveurs. |
| Applications / usages touchés | Les admissions, prescriptions, analyses, comptes rendus, gestion des urgences, imagerie médicale, analyses, pharmacie et gestion des blocs sont cités comme touchés ou perturbés selon Le Monde et L’Usine Digitale. |
| Mesure de crise | Pour éviter la propagation, l’arrêt de tous les ordinateurs a été décidé rapidement ; le CHU a fonctionné en mode dégradé. |
| Conséquences opérationnelles | Retour au papier et au téléphone : observations médicales sur papier, transmissions papier, admissions et prescriptions en mode dégradé, résultats d’examens récupérés physiquement, laboratoire et radiologie ralentis. |
| Continuité des soins | Le CHU affirme qu’à ce stade les difficultés n’ont eu aucune conséquence directe sur le suivi des patients, et qu’une reprise progressive a permis une prise en charge quasi normale. |
| Données personnelles / médicales | Le CHU indique qu’aucune fuite de données médicales ou personnelles n’a été constatée à la date de son communiqué. |
| Suites judiciaires | Le CHU a porté plainte contre X pour accès frauduleux dans un système de traitement automatisé de données et tentative d’extorsion de fonds auprès du parquet de Paris. |

### Ce qui est certain / ce qui est inconnu

| Ce qui est certain | Ce qui est inconnu ou non confirmé dans les sources |
| --- | --- |
| Une cyberattaque a touché le CHU de Rouen le 15 novembre 2019. | Le point d’entrée exact dans le SI du CHU n’est pas déterminé avec certitude dans les sources consultées. Le Monde mentionne qu’il n’était pas encore établi. |
| L’attaque a provoqué le chiffrement de fichiers sur des ordinateurs et serveurs. | L’étendue exacte du chiffrement, machine par machine ou serveur par serveur, n’est pas détaillée publiquement. |
| Le CHU a fonctionné en mode dégradé, avec recours au papier et au téléphone. | La durée exacte de retour à la normale complète n’est pas précisée dans les sources utilisées ici. |
| Les applications métiers ont été fortement impactées : admissions, prescriptions, comptes rendus, urgences, analyses, radiologie. | Le niveau précis d’impact sur chaque service hospitalier n’est pas quantifié. |
| Le rançongiciel identifié publiquement est Clop / CryptoMix Clop. | L’identité exacte des auteurs individuels n’est pas établie publiquement. |
| L’ANSSI relie les attaques Clop observées à une campagne d’hameçonnage et au groupe cybercriminel TA505. | L’attribution judiciaire définitive de l’attaque du CHU à des personnes précises n’est pas fournie dans les sources. |
| Aucune fuite de données médicales ou personnelles n’avait été constatée à la date du communiqué du CHU. | L’absence absolue et définitive d’exfiltration ne peut pas être affirmée uniquement à partir de ces sources. |
| Une plainte contre X a été déposée pour accès frauduleux et tentative d’extorsion. | Le montant exact de la rançon, son éventuel paiement, ou les échanges avec les attaquants ne sont pas confirmés par les sources principales retenues. |
