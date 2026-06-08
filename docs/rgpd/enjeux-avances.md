# Enjeux avancés du RGPD

## Responsabilisation

Le RGPD repose sur le principe d'**accountability**, souvent traduit par **responsabilisation**.

Cela signifie qu'une organisation ne doit pas seulement respecter le RGPD : elle doit aussi être capable de le démontrer.

Exemples de preuves attendues :

- registre des traitements,
- politiques de sécurité,
- procédures de gestion des droits,
- contrats avec les sous-traitants,
- preuves d'information des personnes,
- analyses d'impact,
- journalisation des incidents,
- documentation des mesures techniques.

## Registre des activités de traitement

Le **registre des activités de traitement** est un document qui recense les traitements de données personnelles réalisés par un organisme.

Il permet d'avoir une vue d'ensemble de ce qui est fait avec les données personnelles.

Il aide à répondre à des questions simples :

- quelles données sont traitées ?
- pourquoi sont-elles traitées ?
- qui est concerné ?
- qui peut accéder aux données ?
- à qui les données sont-elles transmises ?
- combien de temps sont-elles conservées ?
- quelles mesures de sécurité sont prévues ?

Le registre est un outil central de conformité, car il permet de documenter les traitements et de montrer que l'organisme maîtrise ses usages des données personnelles.

Pour un AIS, il peut aussi servir à identifier les systèmes concernés :

- applications métier,
- bases de données,
- serveurs,
- sauvegardes,
- journaux de connexion,
- prestataires d'hébergement,
- outils SaaS,
- flux entre services.

!!! tip "Réflexe AIS"
    Un registre utile ne doit pas rester purement administratif. Il doit aider à retrouver les applications, serveurs, comptes, flux, sauvegardes et prestataires liés à chaque traitement.

## Exemple de ligne de registre

| Élément | Exemple |
| --- | --- |
| Traitement | Gestion des comptes utilisateurs |
| Finalité | Créer et administrer les accès aux services internes |
| Données | Nom, prénom, e-mail professionnel, identifiant, rôle |
| Personnes concernées | Salariés |
| Accès | Service informatique, responsables habilités |
| Conservation | Durée du contrat puis archivage limité |
| Sécurité | MFA, droits par rôle, journalisation, révocation des accès |

## Privacy by design et by default

La protection des données doit être pensée dès la conception d'un service.

### Privacy by design

La protection des données est intégrée dès le départ dans le projet.

Exemple : prévoir dès la conception d'une application une séparation des rôles, des durées de conservation et une méthode de suppression des comptes.

### Privacy by default

Les réglages par défaut doivent être les plus protecteurs possible.

Exemple : ne pas activer par défaut une option de partage public de profil ou de suivi marketing.

## Analyse d'impact : AIPD

Une **AIPD** est une analyse d'impact relative à la protection des données.

Elle est nécessaire lorsqu'un traitement est susceptible d'engendrer un risque élevé pour les droits et libertés des personnes.

Elle sert à analyser :

- le traitement prévu,
- les données utilisées,
- la nécessité et la proportionnalité,
- les risques pour les personnes,
- les mesures de sécurité à mettre en place.

Exemples de traitements pouvant nécessiter une AIPD :

- surveillance systématique,
- données de santé à grande échelle,
- données biométriques,
- scoring ou profilage,
- traitements concernant des personnes vulnérables,
- croisement massif de données.

## Violations de données personnelles

Une violation de données personnelles correspond à une perte de confidentialité, d'intégrité ou de disponibilité.

Exemples :

- fuite d'une base de données,
- accès non autorisé à un compte administrateur,
- perte d'un ordinateur non chiffré,
- suppression accidentelle de données sans sauvegarde,
- ransomware bloquant l'accès aux dossiers clients,
- erreur d'envoi d'un fichier contenant des données personnelles.

En cas de violation, l'organisation doit :

1. qualifier l'incident,
2. documenter ce qui s'est passé,
3. évaluer le risque pour les personnes,
4. notifier la CNIL si la violation présente un risque,
5. informer les personnes concernées si le risque est élevé.

!!! warning "Délai important"
    Si la violation doit être notifiée à la CNIL, la notification doit être faite dans les meilleurs délais et, si possible, dans les **72 heures** après en avoir pris connaissance.

## Rôle actuel de la CNIL

Dans le cadre du RGPD, la CNIL est l'autorité française de contrôle.

Elle n'est pas seulement là pour sanctionner. Elle a aussi un rôle d'accompagnement, de conseil et de pédagogie.

Concrètement, la CNIL peut :

- publier des guides et recommandations,
- proposer des outils comme l'Atelier RGPD ou les ressources AIPD,
- recevoir les plaintes des personnes,
- contrôler une organisation,
- demander des corrections,
- prononcer des mises en demeure,
- sanctionner financièrement certains manquements,
- coopérer avec les autres autorités européennes.

Pour une organisation, la CNIL est donc à la fois :

- une source de documentation,
- un interlocuteur en cas de doute ou de violation de données,
- une autorité de contrôle en cas de non-respect du RGPD.

!!! tip "Réflexe AIS"
    Quand une question RGPD touche la sécurité technique, les droits d'accès, les logs, les violations de données ou les sauvegardes, le site de la CNIL est souvent le premier endroit à consulter.

## Sous-traitance et chaîne de responsabilité

Le RGPD distingue notamment :

- le **responsable de traitement**, qui décide pourquoi et comment les données sont traitées,
- le **sous-traitant**, qui traite les données pour le compte du responsable de traitement.

Exemples de sous-traitants :

- hébergeur cloud,
- prestataire de sauvegarde,
- outil de ticketing,
- solution de paie,
- prestataire d'e-mailing,
- infogérant.

Pour un AIS, c'est un point important : un prestataire technique peut avoir accès à des données personnelles, même s'il ne les exploite pas pour son propre compte.

## Sécurité technique et organisationnelle

Le RGPD ne donne pas une liste unique de mesures applicables partout. Les mesures doivent être adaptées aux risques.

Mesures fréquentes :

- gestion stricte des comptes,
- principe du moindre privilège,
- MFA pour les accès sensibles,
- chiffrement des supports et flux,
- sauvegardes testées,
- segmentation réseau,
- supervision et logs,
- mises à jour régulières,
- durcissement des serveurs,
- politique de mots de passe,
- procédure de révocation des accès,
- sensibilisation des utilisateurs.

## Transferts hors Union européenne

Le RGPD encadre aussi les transferts de données personnelles hors de l'Union européenne.

Le sujet devient sensible quand une organisation utilise :

- un hébergeur étranger,
- un outil SaaS mondial,
- une solution de support externalisée,
- une plateforme d'analyse ou de marketing,
- un prestataire qui sous-traite lui-même hors UE.

L'enjeu est de vérifier que les données gardent un niveau de protection suffisant.

## Enjeu pour un administrateur d'infrastructures sécurisées

Pour un AIS, le RGPD n'est pas seulement une affaire de documents juridiques.

Il influence directement :

- la configuration des accès,
- la sécurité des serveurs,
- la gestion des sauvegardes,
- la journalisation,
- le chiffrement,
- le choix des prestataires,
- la réaction aux incidents,
- la documentation technique,
- la suppression ou l'archivage des données.

## À retenir

- La conformité RGPD doit être prouvable.
- Le registre permet de recenser les traitements et de piloter la conformité.
- Les risques doivent être anticipés dès la conception des traitements.
- Une AIPD est nécessaire pour certains traitements à risque élevé.
- Les violations de données doivent être détectées, documentées et parfois notifiées.
- La CNIL accompagne, contrôle et sanctionne les organismes concernés par le RGPD.
- La sécurité technique est une partie concrète de la conformité.

## Sources utiles

- [L'analyse d'impact relative à la protection des données - CNIL](https://www.cnil.fr/fr/RGPD-analyse-impact-protection-des-donnees-aipd)
- [Analyse d'impact - définition CNIL](https://www.cnil.fr/fr/definition/analyse-dimpact-aipd)
- [Les violations de données personnelles - CNIL](https://www.cnil.fr/fr/cybersecurite/les-violations-de-donnees-personnelles)
- [Notifier une violation de données personnelles - CNIL](https://www.cnil.fr/fr/notifier-une-violation-de-donnees-personnelles)
- [Comprendre le RGPD - CNIL](https://www.cnil.fr/comprendre-le-rgpd-0)
- [Le registre des activités de traitement - CNIL](https://www.cnil.fr/fr/RGPD-le-registre-des-activites-de-traitement)
- [Règlement (UE) 2016/679 - EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj?locale=fr)
