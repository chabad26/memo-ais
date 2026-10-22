# Le mur des matrices

**Séquence 4.5 — 30 min — Présentiel**

## Le problème à résoudre

Sofia compare trois versions dont les taux globaux sont proches. L’objectif est de choisir en fonction des attaques manquées et de la charge réelle, puis de confronter les résultats entre apprenants. Source : kit apprenant, section 4.5, lu le 22 octobre 2026.

**Deux périmètres distincts :** le tableau du cours ci-dessous est un cas pédagogique sur 2 119 observations et 215 attaques. Nos calculs V2 portent sur **2 105 observations et 211 attaques**, après exclusion de 14 volumes réellement manquants. De plus, notre V2 utilise une contamination de **0,03**, contre **0,05** pour la version C de l’énoncé. Les chiffres de l’un ne remplacent pas ceux de l’autre.

## Mission 1 — Notre matrice pour le tableau collectif

| Référence réelle / prédiction de l’union V2 à 0,03 | Normal | Alerte |
| --- | ---: | ---: |
| Normal | **1 857 VN** | **37 FP** |
| Attaque | **9 FN** | **202 VP** |

Précision : **84,52 %** ; rappel : **95,73 %** ; 239 alertes, réparties en 104 et 135 par semaine. Les quatre attaques exclues faute de volume ne figurent pas dans cette matrice.

![Matrice d’octobre de l’union V2](../../assets/img/ia-cybersecurite/it-4/Capture%20d’écran%20du%202026-10-22%2009-23-59.png)

La comparaison collective reste à réaliser : **aucun résultat des collègues n’a été fourni**. Pour expliquer un écart, comparer les fichiers/périodes, les exclusions ou imputations, la conversion Ko/Mo, les caractéristiques et leur ordre, la graine, le découpage d’entraînement et les hyperparamètres. Avec le même jeu et la même graine, changer l’ordre des caractéristiques peut modifier un choix de séparation en cas d’égalité. Vérifier aussi que tous entraînent sur septembre et prédisent octobre, sans réentraîner sur octobre.

## Mission 2 — Le tableau de Sofia, calculé

Les matrices sont reconstituées avec 1 904 normales et 215 attaques : VP = 215 − FN ; VN = 1 904 − FP. Une fausse alerte coûte **10 minutes**. Les valeurs hebdomadaires sont des **moyennes sur deux semaines**, pas une répartition observée.

| Version du cours | Accuracy | VN / FP / FN / VP | Précision | Rappel | Alertes / semaine en moyenne | Coût FP / semaine |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| **A — arbre seul** | 94,2 % | 1 873 / 31 / 92 / 123 | 79,87 % | 57,21 % | 77 | **155 min = 2 h 35** |
| **B — Isolation Forest 0,10** | 93,9 % | 1 821 / 83 / 46 / 169 | 67,06 % | 78,60 % | 126 | **415 min = 6 h 55** |
| **C — union à 0,05** | 93,7 % | 1 852 / 52 / 82 / 133 | 71,89 % | 61,86 % | 92,5 | **260 min = 4 h 20** |
| **D — toujours normal** | 89,9 % | 1 904 / 0 / 215 / 0 | Non définie, aucune alerte | **0 %** | 0 | 0 |

Exemple : pour B, **83 × 10 / 2 = 415 minutes par semaine**. Le taux global de D est élevé uniquement parce que les normales sont majoritaires.

### Quelles attaques chaque version rate-t-elle sur nos fichiers ?

Le tableau agrégé du cours ne contient ni les prédictions ni les profils des attaques manquées. On ne peut donc pas attribuer ses 92/46/82 FN à des scénarios précis. Pour mener la mission, une **comparaison supplémentaire a été exécutée par l’assistant dans un environnement distinct de la VM**, en gardant le protocole V2 (septembre seul, profondeur 3, graine 42, mêmes sept variables). Seule la variante demandée change : arbre seul, IF à 0,10 ou union à 0,05. La V2 à 0,03 et son CSV restent conservés.

| Version rejouée localement | VN / FP / FN / VP | Alertes S40 / S41 | Attaques manquées internes / externes | Exfiltration du 09/10 à 3 h |
| --- | --- | --- | --- | --- |
| **A — arbre seul** | 1 868 / 26 / 17 / 194 | 93 / 127 | 12 / 5 | Manquée |
| **B — IF 0,10** | 1 839 / 55 / 48 / 163 | 96 / 122 | 5 / 43 | Repérée |
| **C — union 0,05** | 1 843 / 51 / 4 / 207 | 111 / 147 | 3 / 1 | Repérée |
| **D — toujours normal** | 1 894 / 0 / 211 / 0 | 0 / 0 | 16 / 195 | Manquée |

- **A** manque neuf observations VPN à un compte, trois activités internes sur trois comptes et cinq connexions externes sur un compte. Les neuf VPN incluent le transfert de 8 690 Mo : une durée et un nombre de comptes ordinaires suffisent à suivre la branche normale, même avec un gros volume.
- **B** manque 48 attaques, dont 43 externes : une attaque fréquente dans les données n’est pas nécessairement atypique pour Isolation Forest. L’origine seule ne permet pas de nommer leur méthode exacte ; les lignes détaillées sont conservées pour analyse.
- **C** manque les trois observations internes `10.20.3.50` (01/10 à 14 h), `.118` (05/10 à 10 h), `.57` (09/10 à 11 h), et la connexion externe `198.51.100.67` (05/10 à 8 h). Leur profil reste trop ordinaire pour les deux modèles ; leur étiquette du kit constitue la référence.

Les versions ne manquent donc pas seulement des quantités différentes, mais aussi **des profils différents**. Passer de notre union 0,03 à 0,05 fait passer de 9 à 4 FN, mais de 37 à 51 FP et de 239 à 258 alertes. C’est un résultat exploratoire sur un mois déjà consulté, pas la validation d’un nouveau réglage pour production.

**Preuves conservées dans le kit :** `preuves/comparaison_versions_45.json` et `preuves/comparaison_45_FN_A.csv` à `D.csv`. Le script de comparaison est `livrables/ia-cybersecurite/it-4/comparer_versions_45.py`. Ces essais n’ont pas été exécutés dans la VM de l’apprenant et ne modifient pas son protocole de remise.

## Réponses pour Nadia

### 1. Quel classement, et suit-il l’accuracy ?

**Sur le tableau du cours, si la priorité est de réduire les attaques manquées : B, puis C, puis A, puis D.** B manque 46 attaques contre 82 pour C et 92 pour A, mais coûte beaucoup plus de qualification. Ce classement ne suit pas l’accuracy, qui donnerait A, B, C, D.

**Sur nos essais locaux, la même priorité donne C, A, B, D.** Ce changement de classement vient des résultats mesurés avec notre préparation et nos réglages, pas d’une contradiction : les chiffres pédagogiques ne sont pas les sorties de notre V2.

Pour une exploitation limitée à **30 alertes par semaine**, aucune des versions A/B/C ne tient la capacité, dans les deux périmètres. Le classement technique ne vaut donc pas autorisation de mise en service. Proposer un pilote supervisé et travailler regroupement, enrichissement, moyens de qualification et priorités. D reste une référence de comparaison sans capacité de détection ; ne pas supprimer fail2ban.

### 2. Un FP et un FN ont-ils le même coût ?

**Non.** Un FP coûte ici environ **10 minutes** de qualification ; 6 FP représentent une heure. Un FN peut n’avoir aucun coût immédiat visible, puis permettre une interruption, une fuite ou une propagation. Son coût dépend du scénario, pas seulement de la case dans la matrice.

Ordre de grandeur **illustratif, non mesuré chez Hexalp** : un incident mobilisant deux techniciens pendant quatre heures représente déjà **8 heures de travail**, soit 48 qualifications de FP, avant même d’ajouter l’indisponibilité métier ou une fuite. Une attaque manquée ne coûte pas systématiquement huit heures : il faut chiffrer selon sa gravité réelle. Ne pas inventer une perte financière à partir des seuls logs.

### 3. Que devient l’astreinte après un mois avec B ?

Sur **quatre semaines au rythme moyen du tableau du cours**, B produit environ **504 alertes**, dont **166 FP**. Les seuls FP demandent **27 h 40** ; toute la file demanderait **84 heures** si chaque alerte prend dix minutes. Avec 30 lectures par semaine, la capacité est 120 : **384 alertes excédentaires** s’accumulent sans renfort ou réduction de la charge.

C’est le mécanisme de la **fatigue d’alerte** : trop de notifications répétées ou peu utiles usent l’attention, retardent la qualification et favorisent les signaux ignorés, y compris les vrais incidents. C’est une projection, pas un constat observé chez l’équipe. Avec nos résultats locaux de B, le calcul serait différent : 218 alertes sur deux semaines, pas 252.

### 4. Un seul chiffre chaque semaine ?

Je choisirais **le rappel des attaques qualifiées**, parce qu’il mesure ce qui échappe au dispositif : VP / (VP + FN). Mais il faut une référence indépendante et suffisamment complète, disponible souvent avec retard ; les alertes lues seules ne permettent pas de connaître les FN.

Un rappel élevé peut coûter une file ingérable, masquer l’absence de couverture de collecte ou ignorer la gravité des attaques manquées. Le tableau de bord minimal doit donc aussi suivre **précision, alertes et stock non qualifié, couverture des données, types et gravité des erreurs**. Lorsqu’on ne connaît pas encore les FN de la semaine, afficher « non encore mesurable », plutôt qu’un faux rappel de 100 %.

## À retenir pour le carnet et la remise

La comparaison collective est à renseigner après échange avec les collègues. Les calculs du tableau du cours et les résultats locaux restent séparés. Les versions B/C explorées ici ne remplacent pas la V2 figée à 0,03. Le PDF formateur est conservé comme version intermédiaire : **mise à jour et remise groupée à la fin**, selon le choix de l’apprenant.

- [Rapport du matin — 4.4](le-rapport-evaluation.md)
- [Résultats et captures de la V2 — 4.3](evaluer-en-conditions-reelles.md)
