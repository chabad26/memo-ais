# Analyse des incidents et mitigation

## Objectif

L'objectif est de comparer deux incidents réels pour comprendre :

- ce qui s'est passé ;
- quel système a été touché ;
- quels impacts ont été provoqués ;
- quelle cause racine explique réellement l'incident ;
- quelles mesures réalistes permettraient de réduire le risque.

Les deux cas étudiés sont :

- la fuite de données Free / Free Mobile d'octobre 2024 ;
- l'incident CrowdStrike du 19 juillet 2024.

## Analyse des incidents

| Incident | Type | Système concerné | Impact | Cause racine |
| --- | --- | --- | --- | --- |
| Fuite de données Free / Free Mobile | Fuite de données / compromission du SI | SI interne Free / Free Mobile, accès VPN, bases de données clients | **Technique** : accès non autorisé à des données personnelles. **Métier** : risque de fraude, hameçonnage, usurpation d'identité, perte de confiance client. **Organisationnel** : notification aux personnes concernées, plaintes, contrôle CNIL, sanction financière. | Authentification VPN insuffisamment robuste, détection inefficace des comportements anormaux, conservation excessive de certaines données. |
| Incident CrowdStrike | Panne logicielle / indisponibilité massive | Postes et serveurs Windows équipés de CrowdStrike Falcon Sensor | **Technique** : crash système / écrans bleus sur des hôtes Windows. **Métier** : interruption d'activité pour des organisations dépendantes de ces postes. **Organisationnel** : mobilisation de crise, correction manuelle de postes, reprise progressive. | Mise à jour de contenu Falcon Channel File 291 mal validée : le capteur attendait 20 champs d'entrée, la mise à jour en fournissait 21, provoquant une lecture mémoire hors limites et un crash. |

## Symptôme ou cause ?

| Incident | Symptôme visible | Cause plus profonde |
| --- | --- | --- |
| Free / Free Mobile | Des données clients sont exposées. | Les contrôles d'accès et de détection n'ont pas suffisamment limité l'intrusion, et trop de données étaient encore conservées. |
| CrowdStrike | Des machines Windows redémarrent ou affichent un écran bleu. | Le processus de validation et de déploiement d'une mise à jour critique n'a pas bloqué un contenu incompatible avec le capteur. |

## Enjeux associés

| Incident | Confidentialité | Intégrité | Disponibilité |
| --- | --- | --- | --- |
| Free / Free Mobile | Très fort : données personnelles et IBAN exposés. | Moyen : risque d'utilisation frauduleuse des données. | Faible à moyen : l'incident porte surtout sur la confidentialité. |
| CrowdStrike | Faible : ce n'est pas une fuite de données. | Moyen : confiance dans la chaîne de mise à jour affectée. | Très fort : indisponibilité massive de postes et serveurs Windows. |

## Plan de mitigation

| Risque | Cause | Mesure | Type | Impact attendu |
| --- | --- | --- | --- | --- |
| Fuite massive de données clients | Accès distant trop faible, détection insuffisante, données conservées trop longtemps | Renforcer l'accès VPN avec MFA robuste, règles conditionnelles et comptes nominatifs | Technique | Réduit le risque d'intrusion par vol ou compromission d'identifiants. |
| Fuite massive de données clients | Comportements anormaux mal détectés | Mettre en place une supervision des accès sensibles : alertes sur export massif, connexion inhabituelle, accès hors horaires | Technique | Permet de détecter plus vite une compromission et de limiter l'exfiltration. |
| Fuite massive de données clients | Trop de données conservées | Définir une procédure de purge des anciennes données et la contrôler régulièrement | Organisationnelle | Réduit le volume de données exposables en cas d'incident. |
| Fuite massive de données clients | Réaction utilisateur difficile après notification | Préparer des messages clairs pour les clients : risques, bons réflexes, canaux officiels | Humaine / organisationnelle | Limite les fraudes secondaires et améliore la confiance après incident. |
| Indisponibilité massive après mise à jour critique | Dépendance forte à un outil déployé partout | Déployer les mises à jour critiques par anneaux : pilote, petit périmètre, généralisation progressive | Technique / organisationnelle | Évite qu'une erreur touche tout le parc en même temps. |
| Indisponibilité massive après mise à jour critique | Contrôles de validation insuffisants | Ajouter des tests automatiques, contrôles de compatibilité et mécanismes de rollback | Technique | Réduit la probabilité qu'une mise à jour défectueuse atteigne la production. |
| Indisponibilité massive après mise à jour critique | Dépendance à un fournisseur unique | Identifier les dépendances critiques et prévoir un mode dégradé pour les postes essentiels | Organisationnelle | Améliore la continuité d'activité même si un fournisseur tombe en panne. |
| Indisponibilité massive après mise à jour critique | Remédiation manuelle longue | Préparer une procédure de reprise : démarrage sans échec, consignes support, priorisation des postes critiques | Humaine / organisationnelle | Accélère la remise en service et réduit la désorganisation. |

## Mesures communes

Les deux incidents sont différents, mais plusieurs mesures reviennent :

- contrôler les accès sensibles ;
- superviser les comportements anormaux ;
- limiter le périmètre touché en cas d'erreur ou d'attaque ;
- tester avant de généraliser ;
- préparer une procédure de crise compréhensible ;
- réduire les dépendances critiques non maîtrisées.

## Ce qui change selon l'incident

| Point de comparaison | Free / Free Mobile | CrowdStrike |
| --- | --- | --- |
| Nature principale | Sécurité / confidentialité | Disponibilité / continuité |
| Déclencheur | Intrusion dans le SI | Mise à jour défectueuse |
| Données exposées | Oui | Non indiqué comme fuite de données |
| Réponse prioritaire | Contenir l'accès, informer, renforcer les contrôles, réduire les données conservées | Restaurer les postes, corriger la mise à jour, revoir le processus de déploiement |
| Mesure clé | MFA robuste + détection + purge des données | Déploiement progressif + tests + rollback |

## Présentation courte

| Incident | Cause racine | Mesure clé à présenter |
| --- | --- | --- |
| Free / Free Mobile | Accès distant et détection insuffisants, avec conservation excessive de données | Renforcer les accès VPN, superviser les accès sensibles et réduire les données conservées. |
| CrowdStrike | Mise à jour critique insuffisamment validée avant diffusion large | Déployer par anneaux avec tests automatiques et possibilité de rollback rapide. |

## Sources

- CNIL, [Violation de données : sanction de 42 millions d'euros à l'encontre des sociétés FREE MOBILE et FREE](https://www.cnil.fr/fr/sanction-free-2026), 14 janvier 2026.
- CrowdStrike, [Channel File 291 Incident: Root Cause Analysis is Available](https://www.crowdstrike.com/en-us/blog/channel-file-291-rca-available/), 6 août 2024.
- CrowdStrike, [Executive Summary: Root Cause Analysis - Channel File 291](https://www.crowdstrike.com/wp-content/uploads/2024/08/Executive-Summary_Root-Cause-Analysis_Channel-File-291.pdf), 6 août 2024.
