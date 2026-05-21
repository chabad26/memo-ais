# Préparation de la restitution

## Objectif

Préparer une présentation claire de **5 minutes** sur l'analyse du SI d'une mairie.

La restitution doit être compréhensible par une personne qui ne connaît pas le dossier.

## Plan de présentation

| Temps | Partie | Message principal |
| --- | --- | --- |
| 0:00 - 1:00 | Présentation du SI | Le SI d'une mairie relie des agents, des applications métier, des données sensibles et des accès externes. |
| 1:00 - 3:00 | Points critiques | Les risques principaux concernent les accès, les sauvegardes, les données personnelles, les prestataires et les points d'entrée externes. |
| 3:00 - 4:30 | Améliorations | Les améliorations doivent être réalistes : mieux gérer les droits, tester les sauvegardes, former les agents, documenter les outils et segmenter progressivement le réseau. |
| 4:30 - 5:00 | Conclusion | L'objectif est de rendre le SI plus sûr, plus lisible et plus résilient sans bloquer le travail quotidien des agents. |

## 1. Présentation du SI

Le cas étudié est une **mairie de taille moyenne**.

Son système d'information sert à :

- accueillir les citoyens ;
- gérer l'état civil ;
- traiter les dossiers d'urbanisme ;
- gérer les finances et les ressources humaines ;
- communiquer par messagerie ;
- utiliser des portails administratifs externes ;
- stocker et sauvegarder des documents.

L'architecture est **hybride** :

- une partie interne : postes, réseau, fichiers, sauvegardes ;
- une partie cloud ou externalisée : messagerie, démarches en ligne, applications métier ;
- des accès externes : citoyens, prestataires, portails publics.

## 2. Points critiques

Les principaux points critiques sont :

| Point critique | Pourquoi c'est important |
| --- | --- |
| Comptes utilisateurs | un compte compromis peut donner accès à des données sensibles |
| Accès administrateur | droits élevés, impact important en cas d'erreur ou d'attaque |
| Données personnelles | habitants et agents doivent être protégés |
| Sauvegardes | indispensables pour reprendre l'activité après panne ou ransomware |
| Accès internet | nécessaire pour la messagerie, les démarches et les portails |
| Prestataires | utiles pour la maintenance, mais leurs accès doivent être encadrés |
| Postes d'accueil | exposés au public et utilisés quotidiennement |

Les risques principaux sont :

- phishing ;
- partage de mots de passe ;
- droits trop larges ;
- absence de test de restauration ;
- dépendance à un prestataire ;
- réseau insuffisamment segmenté ;
- documentation incomplète.

## 3. Améliorations proposées

Les améliorations prioritaires sont :

**1) Tester les sauvegardes**
   Vérifier régulièrement que les données importantes peuvent être restaurées.

**2) Mieux gérer les comptes et les droits**
   Supprimer les comptes inutiles, limiter les droits et activer le MFA sur les accès sensibles.

**3) Former les agents**
   Faire une formation courte sur le phishing, les mots de passe, les pièces jointes et les données personnelles.

**4) Documenter les outils critiques**
   Créer une fiche simple par outil : rôle, utilisateurs, prestataire, données, sauvegarde, procédure incident.

**5) Segmenter progressivement le réseau**
   Séparer au minimum le Wi-Fi invité, les équipements exposés et les zones sensibles.

## Conclusion possible

Le SI d'une mairie n'est pas forcément très complexe, mais il est important car il contient des données sensibles et supporte des services publics quotidiens.

Les améliorations proposées ne cherchent pas à tout reconstruire. Elles visent surtout à réduire les risques les plus probables, améliorer la continuité de service et rendre le SI plus facile à administrer.

