# Risques, incidents et enjeux SI

## Données qu'un ransomware vise en priorité

| Priorité | Données ou systèmes | Pourquoi |
| --- | --- | --- |
| 1 | dossier patient, prescriptions, résultats | bloque directement les soins |
| 2 | comptes, AD/IAM, droits administrateurs | permet la propagation |
| 3 | sauvegardes | empêche une restauration rapide |
| 4 | données administratives et RH | augmente l'impact métier |
| 5 | journaux et configurations | gêne l'analyse et la reprise |

## Utilisateurs et facteurs humains

Un utilisateur n'est pas seulement un risque : c'est un acteur du SI avec des contraintes.

| Profil | Besoin | Risque possible |
| --- | --- | --- |
| Médecins | accéder vite au dossier et prescrire | session ouverte, urgence, mobilité |
| Infirmiers | suivre les soins sur postes partagés | partage de session ou de carte |
| Administratif | gérer admissions, rendez-vous, messages | phishing, pièce jointe, erreur de saisie |
| DSI / IT | administrer, dépanner, restaurer | compte admin utilisé trop largement |
| Prestataires | maintenir à distance | accès VPN trop large ou permanent |

Question clé :

**Dans quelles conditions quelqu'un est-il poussé à contourner la sécurité ?**

Réponses fréquentes :

- urgence ;
- outil trop lent ;
- manque de postes ;
- authentification trop lourde ;
- droits insuffisants ;
- procédure de support trop longue.

## Enjeux et risques

Il faut savoir faire l'analyse des enjeux et des risques.

Les 5 enjeux principaux sont :

- **disponibilité** ;
- **sécurité** ;
- **évolutivité** ;
- **intégration** ;
- **conformité**.

Pour la disponibilité, il faut savoir raisonner avec :

- **RTO** : temps maximal acceptable avant reprise ;
- **RPO** : perte de données maximale acceptable.

Ensuite, les risques doivent être classés par nature :

- **techniques** ;
- **organisationnels** ;
- **humains**.

## Normes et obligations

Les normes et règlements comme **RGPD**, **NIS2**, **DORA** et **ISO 27001** aident à relier les risques aux obligations, à la gouvernance et au travail concret d'administration système.

Synthèse à garder :

- un enjeu explique ce qu'on veut protéger ;
- un risque décrit ce qui peut mal se passer ;
- une norme donne un cadre ou des exigences ;
- un exemple réel permet de vérifier que l'analyse reste concrète.
