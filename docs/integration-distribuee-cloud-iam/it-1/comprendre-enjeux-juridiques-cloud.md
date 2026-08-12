# Comprendre les enjeux juridiques du choix cloud

!!! info "Durée indicative"
    1 h.

## Objectif

Comprendre les enjeux juridiques qui pèsent sur le choix d'un fournisseur cloud pour la migration de **DIST-01a** : localisation des données, droit applicable, RGPD, Cloud Act, transferts hors UE et souveraineté numérique.

Le but n'est pas de faire une analyse juridique complète. Il s'agit de savoir identifier les risques, poser les bonnes questions et justifier un choix de fournisseur devant une PME, un formateur ou un jury.

## Ce que tu vas faire, et pourquoi

La souveraineté numérique interroge trois questions simples :

- où sont hébergées les données ?
- sous quelle juridiction le fournisseur et ses sous-traitants opèrent-ils ?
- qui peut légalement demander l'accès aux données ?

Un choix cloud ne se limite donc pas au prix ou aux performances. Pour une infrastructure qui contient des identités, des journaux, de la messagerie ou des données métier, le cadre juridique devient un critère d'architecture.

## Rappel des notions

| Notion | Définition opérationnelle | Impact pour DIST-01a |
| --- | --- | --- |
| RGPD | Règlement européen qui encadre le traitement des données personnelles. | Les comptes LDAP, boîtes mail, journaux et traces d'authentification peuvent contenir des données personnelles. |
| Donnée personnelle | Information se rapportant à une personne identifiée ou identifiable. | Nom, prénom, adresse mail, identifiant, adresse IP, journal de connexion. |
| Transfert hors UE/EEE | Communication ou accès à des données personnelles vers un pays hors Union européenne ou Espace économique européen. | Un fournisseur ou sous-traitant soumis à une juridiction hors UE peut créer un point d'attention. |
| Cloud Act | Loi américaine pouvant permettre aux autorités américaines de demander des données à une entreprise soumise au droit américain. | Un hyperscaler américain reste un choix à analyser, même si la région technique est européenne. |
| Souveraineté numérique | Capacité à garder la maîtrise juridique, technique et opérationnelle des données et services. | Le choix OVHcloud/AWS doit être justifié selon les données hébergées et le niveau de sensibilité. |
| SecNumCloud | Qualification de sécurité de l'ANSSI pour des offres cloud de confiance. | À rechercher si le contexte devient sensible ou régulé. |

!!! warning "Nuance importante"
    Un datacenter situé en Europe ne suffit pas à garantir la souveraineté. Il faut aussi regarder l'entité juridique qui fournit le service, les sous-traitants, l'accès administrateur, les clés de chiffrement, les clauses contractuelles et les qualifications éventuelles.

## Application à DIST-01a

| Donnée ou service | Données concernées | Sensibilité | Point juridique |
| --- | --- | --- | --- |
| OpenLDAP | Identités, groupes, comptes techniques | Élevée | Données personnelles et dépendance centrale d'authentification. |
| Messagerie | Adresses, contenus de mails, pièces jointes, traces SMTP/IMAP | Élevée | Données personnelles et parfois contenu métier. |
| Roundcube | Sessions webmail, préférences, carnet éventuel, accès à la messagerie | Élevée | Interface exposée aux utilisateurs. |
| Samba | Fichiers partagés, droits d'accès, documents métier | Variable à élevée | Dépend fortement de la nature des fichiers stockés. |
| Supervision ELK | Logs, adresses IP, identifiants, erreurs d'authentification | Moyenne à élevée | Les journaux peuvent révéler des comportements utilisateurs. |
| Sauvegardes BorgBackup | Copies de données et configurations | Élevée | Une sauvegarde contient souvent plus de données qu'un service isolé. |
| Step CA / certificats | Clés, certificats, chaîne de confiance | Critique | Impact sur la confiance TLS et l'usurpation possible. |

## Comparaison juridique OVHcloud / AWS

| Critère | OVHcloud | AWS |
| --- | --- | --- |
| Type de fournisseur | Fournisseur européen/français | Hyperscaler américain |
| Intérêt principal | Souveraineté et proximité juridique européenne | Large catalogue de services, maturité, écosystème |
| Point de vigilance | Vérifier l'offre exacte, la région, les sous-traitants et les garanties contractuelles | Entreprise soumise au droit américain, donc analyse Cloud Act et transfert hors UE à documenter |
| Données sensibles | Plus favorable si l'offre et le contrat restent dans un cadre européen maîtrisé | Possible techniquement, mais nécessite une analyse juridique et contractuelle plus poussée |
| Secteurs régulés | Rechercher une offre qualifiée ou alignée SecNumCloud si nécessaire | Examiner les exigences sectorielles, les clauses et les mesures complémentaires |

Cette comparaison ne signifie pas qu'AWS est interdit. Elle signifie que le risque juridique et contractuel doit être expliqué. Pour une PME, le bon choix dépend de la nature des données, du niveau de conformité attendu, du budget, des compétences disponibles et des exigences client.

## Analyse Cloud Act

Le Cloud Act est un point d'attention pour les fournisseurs américains. L'enjeu n'est pas seulement l'emplacement physique des données, mais la possibilité qu'une autorité étrangère s'adresse à une entreprise soumise à sa loi.

Pour DIST-01a, les questions à poser sont :

| Question | Réponse à documenter |
| --- | --- |
| Les données sont-elles personnelles ? | Oui pour les identités, mails, journaux et adresses IP. |
| Les données sont-elles sensibles ou réglementées ? | À déterminer selon le contexte métier. |
| Le fournisseur est-il soumis à un droit extra-européen ? | Oui pour AWS, à analyser dans le dossier. |
| Les données peuvent-elles être chiffrées avec des clés maîtrisées par le client ? | À vérifier selon l'offre retenue. |
| Existe-t-il des clauses ou garanties adaptées ? | À vérifier dans les documents contractuels et le cadre RGPD. |

## Analyse RGPD

Le RGPD impose de garder la maîtrise du traitement des données personnelles. Pour une migration cloud, il faut notamment documenter :

- le responsable du traitement ;
- le sous-traitant cloud ;
- la localisation des données ;
- les catégories de données traitées ;
- les mesures de sécurité ;
- les éventuels transferts hors UE/EEE ;
- les garanties contractuelles et techniques ;
- les durées de conservation et de sauvegarde.

!!! tip "Lecture pratique"
    Pour DIST-01a, OpenLDAP, la messagerie, les journaux et les sauvegardes doivent être traités comme des périmètres contenant potentiellement des données personnelles.

## Mesures de réduction du risque

| Mesure | Effet attendu |
| --- | --- |
| Choisir une région européenne | Réduit certains risques de localisation, mais ne suffit pas seul. |
| Choisir un fournisseur européen ou qualifié | Réduit l'exposition à certains droits extra-européens. |
| Chiffrer les données au repos et en transit | Limite l'exposition technique en cas d'accès non autorisé. |
| Maîtriser les clés de chiffrement | Réduit la dépendance au fournisseur pour l'accès aux données. |
| Limiter les données migrées | Respecte le principe de minimisation. |
| Pseudonymiser les logs | Réduit l'exposition des utilisateurs dans la supervision. |
| Documenter les sous-traitants | Clarifie la chaîne de responsabilité. |
| Tester la réversibilité | Évite l'enfermement fournisseur et facilite une sortie du cloud. |

## Position argumentée pour le dossier

Pour une PME qui migre DIST-01a, la position peut être formulée ainsi :

> OVHcloud est privilégié lorsque la priorité est la souveraineté, la localisation européenne et la réduction de l'exposition à un droit extra-européen. AWS reste pertinent pour son écosystème et ses services, mais il demande une analyse plus complète du Cloud Act, des transferts hors UE, des garanties contractuelles, du chiffrement et de la maîtrise des clés.

Cette conclusion doit rester liée au contexte : une messagerie contenant des données métier, des comptes LDAP et des journaux d'authentification ne se traite pas comme un simple site vitrine statique.

## Tableau de décision

| Critère | Poids | OVHcloud | AWS | Commentaire |
| --- | ---: | --- | --- | --- |
| Localisation européenne | Fort | Favorable selon région choisie | Possible en région UE | La localisation ne suffit pas seule. |
| Droit applicable | Fort | Cadre européen/français à vérifier contractuellement | Droit américain à prendre en compte | Point Cloud Act. |
| Données personnelles | Fort | Compatible RGPD avec contrat adapté | Compatible RGPD avec garanties adaptées | Vérifier transferts et sous-traitants. |
| Données sensibles/régulées | Fort | Rechercher SecNumCloud si besoin | Analyse plus exigeante | Dépend du secteur. |
| Coût | Moyen | À comparer dans la feuille coût | À comparer dans la feuille coût | Ne pas choisir uniquement au prix. |
| Services disponibles | Moyen | Catalogue plus ciblé | Catalogue très large | AWS peut être plus riche techniquement. |
| Réversibilité | Moyen | À documenter | À documenter | Export, sauvegarde, IaC, formats ouverts. |

## Preuves à conserver

| Preuve | Contenu attendu |
| --- | --- |
| Liste des données concernées | Comptes LDAP, mails, logs, sauvegardes, certificats. |
| Analyse juridique courte | RGPD, Cloud Act, localisation, droit applicable. |
| Comparaison fournisseur | OVHcloud / AWS avec risques et avantages. |
| Mesures de sécurité retenues | Chiffrement, clés, minimisation, logs, sauvegardes. |
| Sources officielles | ANSSI, CNIL, pages fournisseur si utilisées. |

## État final attendu

À la fin de cette feuille :

- les données personnelles de DIST-01a sont identifiées ;
- la différence entre localisation technique et droit applicable est comprise ;
- le risque Cloud Act est expliqué sans caricature ;
- le RGPD est relié aux données réellement migrées ;
- OVHcloud et AWS sont comparés selon le risque juridique, pas seulement selon le coût ;
- les sources officielles sont citées.

## Ressources

- [ANSSI - SecNumCloud pour les fournisseurs de services cloud](https://www.ssi.gouv.fr/secnumcloud-pour-les-fournisseurs-de-services-cloud/)
- [ANSSI - Catalogue des produits et services qualifiés](https://www.ssi.gouv.fr/fr/produits-et-prestataires/prestataires-de-services-de-confiance-qualifies/)
- [CNIL - Transférer des données hors de l'UE](https://www.cnil.fr/fr/les-outils-de-la-conformite/transferer-des-donnees-hors-de-lue)
- [CNIL - Adéquation des États-Unis : questions-réponses](https://www.cnil.fr/fr/adequation-des-etats-unis-les-premieres-questions-reponses)
- [CNIL - Cloud et accès par autorités étrangères](https://www.cnil.fr/fr/cloud-les-risques-dune-certification-europeenne-permettant-lacces-des-autorites-etrangeres)
