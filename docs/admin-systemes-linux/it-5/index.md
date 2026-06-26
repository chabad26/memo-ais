# Itération 5 Sauvegarde et Nginx

## Objectif

Itération coupé en 2 parties :

-Itération 5a - Sauvegarde & Autonomie 3 📌 Contexte de ce kit — Ce kit est le point culminant du module. La sauvegarde t'apprend à protéger les données. Le projet intégrateur (Autonomie 3) te demande de mobiliser tout ce que tu as appris depuis J1 — sans aide — pour déployer un serveur web sécurisé. C'est ton livrable le plus complet pour le dossier RNCP

-Itération 5b - Nginx — Configuration de référence 📌 Note — Cette séquence est disponible après la clôture de l'Autonomie 3. Elle sert au débriefing et à la finalisation. Comparer ta solution avec cette référence est une partie de l'apprentissage.

## Compétences travaillées

itération 5a :

1. SA-09a — Sauvegarder avec rsync et vérifier avec --checksum
2. SA-09b — Créer une archive tar et tester la restauration
3. SA-09c — Vérifier l'intégrité d'une sauvegarde avec sha256sum

itération 5b :

1. SA-10a — Déployer Nginx avec vhost, utilisateur dédié et logs séparés
2. SA-10b — Sécuriser le serveur web selon le principe du moindre privilège
3. SA-10c — Produire un rapport de déploiement avec procédure de restauration testée

## Feuilles de l'itération

| Feuille | Sujet | Résultat attendu |
| --- | --- | --- |
| [Sauvegarde et restauration AlpesNet](sauvegarde-restauration-alpesnet.md) | Sauvegarde `rsync`, archive `tar`, checksum et restauration testée | Sauvegarde créée, archive vérifiée, restauration testée et procédure documentée |
| [Autonomie 3 - Déploiement Nginx sécurisé AlpesNet](autonomie-3-nginx-securise-alpesnet.md) | Serveur intranet Nginx sécurisé | Vhost intranet, worker dédié, UFW, Fail2ban, logs, sauvegarde et restauration testée |
| [Script d'itération 5](../../assets/scripts/admin-systemes-linux/it-5/alpesnet-it5-sauvegarde.sh) | Automatisation évolutive sauvegarde puis Nginx | Rapport Markdown et log brut avec commandes, résultats et explications |

## À retenir

Une sauvegarde non testée n'est pas une sauvegarde. Pour chaque sauvegarde importante, il faut conserver une preuve de création, une preuve d'intégrité et une preuve de restauration.
