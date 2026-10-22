# Le rapport d’évaluation

**Séquence 4.4 — 1 h — Autonomie**

## La demande de Nadia

> **Nadia [11:20]** J’ai un comité vendredi. Je dois répondre à une question simple : on le met en service, oui ou non ? Je veux des faits, pas un pourcentage. Et je veux savoir ce que vous ne savez pas.

L’objectif est de transformer les résultats de la [séquence 4.3](evaluer-en-conditions-reelles.md) en une décision argumentée. Le rapport ci-dessous est rédigé avec assistance ; chaque chiffre doit pouvoir être expliqué au formateur.

## PDF pour le formateur

**`livrables/ia-cybersecurite/it-4/Evaluation-modele-SSH-Hexalp-Olivier-HIMBLOT.pdf`** : **13 pages**, dont les trois pages du rapport complet (pages2–4), puis chaîne de décision et captures sélectionnées. Les expériences4.6/4.7 et conditions proposées4.8 sont intégrées. Le PDF intermédiaire est conservé séparément ; la remise groupée est préparée dans **`Remise-J4-Hexalp-Olivier-HIMBLOT.zip`**. Aucun fichier n’a été envoyé au formateur. Générateur : `generer_rapport_j4.py`.

## Livrable rédigé

Fichier : **`livrables/ia-cybersecurite/it-4/IA_J4_ressources_apprenant/ia01-j4/rapport_evaluation.md`**. Le texte est reproduit ci-dessous pour lecture dans le mémo. La consigne fixe trois pages maximum : cette version Markdown est compacte ; la pagination a été vérifiée : trois pages de rapport dans le PDF final.

La section « Résistance aux attaques » est complétée après les simulations locales de 4.6. Les conditions finales sont maintenant proposées en 4.8. Le PDF final intègre ces essais ; l’ancienne version intermédiaire reste conservée séparément.

Le rapport a été complété jusqu’à la séquence4.8 : résistance, inférence et conditions proposées. Le PDF final est actualisé pour la remise groupée. Les conditions sont documentaires et n’attestent pas leur application.

---

## Rapport d’évaluation — Détection SSH Hexalp

**Olivier HIMBLOT — 22 octobre 2026 — Itération 4, version complète**  
Données fictives. Rédaction et vérifications locales avec assistance ; conditions d’exploitation proposées, non déployées.

### Résumé pour Nadia

**Pas de mise en service opérationnelle générale en l’état ; poursuite d’un pilote local supervisé pendant quatre semaines.**  
Le modèle reste une aide, avec fail 2ban et les contrôles existants ; aucune action de blocage ne lui est déléguée.  
Le pilote exige des données contrôlées, des versions protégées et des alertes réellement qualifiées, surplus compris.  
Avant élargissement, Nadia et le SOC doivent valider la capacité, les erreurs acceptables et une évaluation sur une période future intacte.  
Réévaluation hebdomadaire, bilan formel au plus tard à quatre semaines, et immédiate après incident manqué ou changement significatif.

### Données et préparation

Une ligne = une IP pendant une heure. **Septembre (14–27/09)** : 1 704 lignes, 117 attaques (6,87 %) ; après exclusion des 90 volumes absents, **1 614 lignes et 108 attaques**. **Octobre (28/09–11/10)** : 2 119 lignes, 215 attaques (10,15 %) ; après préparation, **2 105 lignes et 211 attaques**.

Changements : nouvelle sonde en Ko le 29/09, proxy Zabbix le 30/09, plage VPN le 01/10, panne NetFlow le 04/10, scan le 06/10. Le journal DSI aide à qualifier sans légitimer automatiquement chaque activité.

La V2 complète les Mo absents par **Ko/1 024**, puis conserve le choix J3 : suppression des vrais volumes manquants. Les **14 exclusions d’octobre, dont quatre attaques**, restent hors couverture. Origine codée `externe` 0/1. Ordre des entrées : heure, externe, échecs, succès, comptes, durée, volume. IP/date restent pour l’analyse ; fail 2ban et étiquette exclus des entrées. Contrôles de schéma, valeurs, périodes et manques ; arrêt au-delà de **10 %**, seuil pédagogique non approuvé. Un contrôle réussi ne garantit pas toute la qualité du lot.

### Protocole et résultats

Graine **42**, profondeur **3**, contamination **0,03**. L’arbre apprend sur 1 129 lignes de septembre, contrôle sur 485 ; IF sur tout septembre préparé, sans étiquette. Aucun ajustement sur octobre ; les étiquettes ne servent qu’au bilan. Le script J3 simplement relancé sur octobre réentraîne et teste dans ce mois : le « 99 % » ne mesure pas le transfert temporel. Une accuracy élevée masque aussi déséquilibre des classes et exclusions.

| Octobre, 2 105 lignes | VN | FP | FN | VP | Précision | Rappel | Alertes S40 / S41 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Arbre | 1 868 | 26 | 17 | 194 | 88,18 % | 91,94 % | 93 / 127 |
| Isolation Forest | 1 883 | 11 | 175 | 36 | 76,60 % | 17,06 % | 29 / 18 |
| Union | 1 857 | 37 | 9 | 202 | 84,52 % | 95,73 % | 104 / 135 |
| fail 2ban historique | 1 894 | 0 | 150 | 61 | 100 % | 28,91 % | 61 au total |

VN/FP/FN/VP = normales correctement ignorées / fausses alertes / attaques manquées / attaques repérées. Septembre : arbre testé **453 VN,0 FP,4 FN,28 VP**, précision 100 %, rappel 87,5 %. Le rappel octobre augmente ; la précision baisse. Sur septembre connu, IF affichait 89,80 %/40,74 % et union 95,50 %/98,15 % (précision/rappel), mesures incluant l’entraînement, comparaison descriptive seulement. Union :45/66 puis 104/135 alertes/semaine.

L’union repère 142 attaques non signalées par fail 2ban, mais manque une des 61 que celui-ci signale (60 communes). **Conserver les deux moyens.** L’exfiltration du 09/10 à 3 h est retrouvée par IF après conversion :8 898 637 Ko =8 690,075 Mo ; l’arbre l’ignore.

### Erreurs et coût

Les 37 FP : **proxy Zabbix 26** (quatre comptes, branche de l’arbre), **sauvegarde 10**, **scanner 1** (IF). À10 min :4 h 20 +1 h 40 +10 min = **6 h 10** théoriques de fausses alertes. Les 239 alertes demanderaient 39 h 50 ; capacité 60 sur deux semaines, **179 en excédent**. Leur ordre réel de lecture est inconnu ; score faible ne signifie pas gravité élevée. Pas de liste blanche globale.

Les **neuf FN** : quatre transferts VPN de 6 629–7 617 Mo, trois activités internes sur trois comptes, deux succès externes sur un compte. Durées/comptes paraissent ordinaires à l’arbre, IF ne franchit pas son seuil. Étiquettes de référence, scénarios complets non fournis. Ces neuf FN n’incluent pas les quatre attaques exclues faute de volume.

### Limites et pistes

Apprentissage de deux semaines peu représentatif des rôles nouveaux ; annotations de Hugo à relire en cas d’ambiguïté ; agrégation horaire sans identité/destination ni cumul long ; dérive et pertes de collecte ; octobre déjà exploré. Un meilleur score sur ce mois après réglage ne serait pas un nouveau test indépendant.

Ajouter contexte VPN/rôle/destination et fenêtres glissantes, revoir corpus/étiquettes. Piste notebook 02 : réentraîner sur septembre + première semaine d’octobre, tester sur la seconde (**non exécuté**, semaine déjà connue) ; confirmer ensuite sur une période future intacte.

### Résistance et inférence

Simulations 4.6 locales, hors système réel : kit médiane/IF 0,05 distinct de V2 exclusion/0,03. Dix sondes révèlent deux frontières locales du kit. Son spraying passe, mais le même plan est repéré par la V2 aux 24 h testées. Fractionner 5 000 Mo en cinq heures passe dans les deux. Une exemption d’IP masquerait 9 000 Mo pourtant signalés.

Parmi les tailles testées, **quatre fausses lignes** suffisent à faire passer le profil ciblé dans la V2 ; avec vingt, il passe malgré une matrice test inchangée. Après 80 observations nocturnes ajoutées à l’entraînement IF, neuf VPN passent, contre quatre initialement. Effets non monotones, aucun seuil universel. Ces essais supposent un futur corpus altéré, pas une modification spontanée du modèle figé.

Autoencodeur 4.7 : SHA-256 conforme au PDF avant/après, fichier inchangé, inférence seule. Sur 2 105 lignes : **6 FP,141 FN,70 VP**, précision 92,11 %, rappel 33,18 %, neuf VPN repérés ; insuffisant pour remplacer l’union. Résultats pédagogiques sur 2 119 lignes séparés. Les captures corroborent les exercices ; les essais complémentaires restent attribués à l’environnement local de vérification.

### Conditions d’exploitation

| Rubrique | Conditions proposées — validation RSSI/SOC requise |
| --- | --- |
| Données | Avant chaque lot : schéma/unités/valeurs, périodes, doublons, manques et journal DSI. Refus si contrat invalide, incident de collecte et exclusions visibles ; seuil 10 % à arbitrer. |
| Réévaluation | Revue hebdomadaire, bilan à 4 semaines ; immédiate après changement/incident. Candidat sur données futures intactes et étiquettes revues ; cibles proposées rappel≥95 %, précision≥85 %, scénarios critiques sans régression, charge qualifiable. La V2 ne satisfait pas charge/précision ; aucun remplacement automatique. |
| Protection | Écritures réservées aux mainteneurs/corpus habilités ; revue des ajouts et étiquettes, versions/empreintes confrontées à référence approuvée, retour arrière ; exceptions contextuelles validées, jamais IP entière sans contrôle. |
| Alertes | Capacité 30/semaine sans suppression du surplus ; priorité métier puis score, stock/âge et escalade. Analyste reçoit mesures/avis/déclencheurs et contexte ; ajouter identifiant, versions, couverture et liens aux sources (pas tous présents dans le CSV). |
| Interdits | Modèle : aucun ban, désactivation, commande ou changement de configuration ; ni mise à jour ni exemption autonomes. fail 2ban reste indépendant. |
| Indicateurs | Couverture, alertes/stock/âge, temps, FP/FN et précision/rappel par profil/gravité ; rappel non mesurable tant que FN inconnus. |
| Responsabilités | Sofia exploite ; administrateurs maintiennent sources/fail 2ban ; Hugo/SOC qualifient/annotent ; mainteneurs préparent les mises à jour ; Nadia décide charge/risque et validation. Rôles proposés, non habilitations établies. |

**Preuves :** V2, requirements,239 alertes, notebook 03/04 exécutés localement, JSON/journaux sous `preuves/`, captures de l’apprenant. Deux relances V2 identiques vérifiées localement ; répétabilité et identité des fichiers VM par empreinte non démontrées. SHA-256 aussi contrôlé dans la VM. Aucun déploiement ni accord de mise en service établi. Référence : kit J4,4.1–4.8 ; détails et cinq questions à l’éditeur dans le carnet/fiche 4.8.
