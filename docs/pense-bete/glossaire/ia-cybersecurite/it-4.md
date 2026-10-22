# IA et Cybersécurité — Itération 4 : Critiquer

## Objectif du J4

Évaluer le modèle sur la période suivante, comprendre ses erreurs et ses possibilités de contournement, puis fixer les conditions d'une utilisation maîtrisée. Travail individuel, autonome le matin et guidé l'après-midi, sur une journée.

## Repères du contexte

| Repère | À retenir |
| --- | --- |
| Séparation temporelle | Septembre entraîne ; octobre évalue les deux semaines suivantes. Ne pas apprendre sur le futur réservé à l'évaluation |
| Changement d'infrastructure | Peut modifier les caractéristiques et les comportements légitimes ; effets à vérifier sur les données |
| Coût pour l'astreinte | Comptage réel par semaine, erreurs, temps de traitement et arbitrage ; ne pas s'arrêter à une accuracy élevée |
| Modèle pré-entraîné | Vérifier sa provenance et son intégrité avant chargement ; une empreinte locale n'est pas une référence de confiance indépendante |
| Décision humaine | L'analyste qualifie les alertes ; aucun blocage automatique prévu |

## Kit reçu et état

Dossier : **`livrables/ia-cybersecurite/it-4/IA_J4_ressources_apprenant/ia01-j4/`**.

Les deux CSV, les notebooks 02/03/04, le fichier `.joblib` et `requirements.txt` sont présents. Le CSV octobre contient 2 119 lignes du 28 septembre au 11 octobre ; septembre est identique au J3. Les quatre versions de bibliothèques sont inchangées : réutiliser **`~/ia01-j3/.venv`** dans la VM.

À produire dans `ia01-j4` : rapport d'évaluation, script V2 commenté et dépendances, alertes d'octobre, carnet J4 et notebooks 03/04 complétés/exécutés. Séquences 4.1 à 4.3 intégrées, V2 exécutée dans la VM et résultats sur octobre illustrés par deux captures. Le modèle pré-entraîné a depuis été vérifié et utilisé en inférence locale en4.7. Les prochaines séquences seront ajoutées à réception des consignes.

## Docs associées

- [Itération 4 — Critiquer : ce que vaut votre modèle](../../../ia-cybersecurite/it-4/index.md)
- [Script et limites du J3](../../../ia-cybersecurite/it-3/le-script-de-detection.md)
- [Installation locale, tunnel et jeton Jupyter](../../../ia-cybersecurite/it-3/installer-son-environnement.md)

## Séquence 4.1 — 99 %

Trois hypothèses renseignées : mauvais protocole de mesure, volumes mal préparés et profils nouveaux. Chronologie : hypothèses reconstituées après exploration anticipée, non aveugles. Score réentraîné sur octobre ≠ évaluation du modèle figé de septembre ; alertes produites ≠ alertes traitées. Le récit232/8,5Go ne remplace pas les sorties de l’exercice. Dernier essai corrigé259 alertes, mais branche de l’arbre différente du J3 : identité du modèle encore à confirmer. Carnet J4 commencé, pas de rapport final ni V2 à ce stade.

- [99 %](../../../ia-cybersecurite/it-4/99-pour-cent.md)

## Séquence 4.2 — Relancer et réparer

Journal DSI désormais disponible via le PDF : sonde Ko le29/09 à8h, proxy Zabbix10.20.1.7 le30/09 à10h, nouvelle passerelle VPN le01/10, panne NetFlow04/10 14–18h, scan06/10 à21h. Les rôles ne sont plus de simples hypothèses, mais ne légitiment pas tout trafic.

Sans conversion : notre J3 supprime1 953 lignes et ne garde que166, dont9 attaques. Le corrigé générique impute par médiane : mécanisme différent, également trompeur sans prise en charge des Ko. Après conversion,14 vrais manques et2 105 lignes conservées,211 attaques ; garder les exclusions hors couverture visibles. Contrat de données, unités, taux de manques et couverture temporelle à vérifier avant prédiction. Une sortie99,7% réentraînée sur octobre ne mesure pas le transfert depuis septembre. Tableau comparatif et trois réponses de préparation renseignés,4.3 non préparée.

- [Relancer et réparer](../../../ia-cybersecurite/it-4/relancer-et-reparer.md)

## Séquence 4.3 — Évaluation temporelle et V2

Protocole J3 reproduit : ordre des variables, graine42, profondeur3, contamination0,03 ; septembre seul entraîne, octobre converti Ko/1024 puis vrais manques exclus. Octobre évalué2 105 lignes,211 attaques. Arbre26FP/17FN ; IF11FP/175FN ; union37FP/9FN/202VP, précision84,52%, rappel95,73%. fail2ban0FP/150FN/61VP, rappel28,91%. Union239 alertes,104 puis135/semaine :179 au-delà du budget cumulé60, sans pouvoir dire lesquelles seront effectivement lues.

FP : proxy Zabbix26, sauvegarde10, scanner1. FN :4 transferts VPN,3 activités internes sur3 comptes,2 succès externes sur1 compte. Cas09/10 3h,10.20.250.151 :8 898 637Ko convertis en8 690,075Mo ; IF True, arbre0, retrouvé après conversion.

V2 et CSV produits avec assistance ; deux exécutions identiques, prédictions/export identiques sans étiquettes octobre, schéma inconnu et seuil manques0 refusés. Seuil défaut10% pédagogique non approuvé. Preuves locales dans le kit ; deux captures documentent aussi l’exécution dans la VM : 239 alertes annoncées, 104 puis 135 par semaine. La répétabilité dans la VM reste à vérifier. Rapport4.4 non préparé.

- [Évaluer en conditions réelles](../../../ia-cybersecurite/it-4/evaluer-en-conditions-reelles.md)


## Séquence 4.4 — Le rapport d’évaluation

Rapport du matin rédigé : **différer la mise en service opérationnelle**, poursuivre en observation supervisée. 37 FP × 10 minutes = **6 h 10** ; 239 alertes × 10 minutes = **39 h 50** sur deux semaines. Neuf attaques manquées parmi les lignes évaluées ; quatre autres hors couverture faute de mesure. Pas de réglage supplémentaire sur octobre. Réentraînement proposé, non réalisé ; parties 4.6/4.8 à compléter après les activités.

- [Le rapport d’évaluation](../../../ia-cybersecurite/it-4/le-rapport-evaluation.md)


## Séquence 4.5 — Le mur des matrices

Tableau du cours : FP hebdomadaires à10 min = **A2h35, B6h55, C4h20**. Priorité au rappel : B>C>A>D, mais aucune A/B/C ne tient30 alertes/semaine. Sur quatre semaines B :504 alertes,166FP (27h40),384 au-delà de la capacité120. Projection, pas observation.

Essais locaux distincts de la VM, protocole V2 : A26FP/17FN ; B(IF0,10)55FP/48FN ; C(union0,05)51FP/4FN. Ne pas remplacer les chiffres du cours par ceux du TP ni modifier la V2 à0,03 :239 alertes restent la référence de remise. Rappel à suivre avec précision, charge, couverture et gravité ; collectif entre apprenants encore à faire. PDF intermédiaire conservé, remise groupée en fin d’itération.

- [Le mur des matrices](../../../ia-cybersecurite/it-4/le-mur-des-matrices.md)


## Séquence 4.6 — Attaquer son modèle

Notebook03 complété/exécuté **localement hors VM**, source conservée ; kit médiane/0,05 ≠ V2 exclusion/0,03. Kit : sondes4 comptes/9h trouvées en10 appels ; spraying150 essais/j/IP non signalés, mais même plan détecté aux24h par la V2. Fractionnement5×1000Mo de9à13h non signalé dans les deux variantes. IP blanche : masque9000Mo pourtant signalés ; aucune exemption ajoutée au script.

Étiquettes : premières tailles réussies testées5 lignes kit,4 V2. À20 V2, attaque ciblée manquée avec matrice globale inchangée. Comportement : à80 observations ajoutées, IF kit2/9 VPN détectés ; V2 0/9 contre5/9 initialement. Effets non monotones, aucun seuil universel. Protéger corpus, annotations, provenance, intégrité et validation du remplacement ; pas de réentraînement automatique sur toute trace récente. Rapport enrichi, conditions4.8 encore à compléter ; PDF intermédiaire conservé pour actualisation finale.

- [Attaquer son modèle](../../../ia-cybersecurite/it-4/attaquer-son-modele.md)


**Captures 4.6 corrigées :** six images utiles conservées ; liste blanche à10:04:43 correctement renseignée avec `["10.20.8.30"]`, **185 avant,19 supprimées,166 après**. Quatre images remplacées ou redondantes supprimées. La dernière phrase sur le masquage du transfert synthétique est un texte explicatif, pas un résultat de filtrage de cette observation. Les essais V2 supplémentaires restent distincts.


## Séquence 4.7 — Et le Deep Learning ?

SHA-256 du modèle conforme au PDF4.7 avant/après ; autoencodeur inchangé, inférence seule. Réseau7→8→3→8→7 :186 paramètres (160 poids+26 biais), seuil2,7615. Notebook04 complété/exécuté localement hors VM, source conservée ; JSON et sortie texte dans preuves. Capture10:14:57 ajoutée : SHA-256 calculé dans la VM Debian et conforme au PDF ; quatre autres vues10:17:41 à10:19:17 documentent contrôle Python,186 paramètres, inférence et reconstruction, sans afficher l’environnement exact. Résultats2119 :70VP/145FN/6FP ; coquille «24 poids» à lire56 (7×8).

Périmètre kit2119 avec médiane : AE6FP/145FN/70VP, précision92,11%, rappel32,56%,9/9 VPN et4FP sauvegarde ; IF0,05 :22FP/154FN/61VP,9/9 VPN et19FP sauvegarde. Trois attaques IF seulement, douze AE seulement. Sur2105 mêmes lignes que V2 : AE6FP/141FN/70VP, rappel33,18% ; ne remplace pas l’union V2. Erreur volume exfil928,97 sur données normalisées, pas enMo ; pas preuve d’intention.

Empreinte ≠ innocuité ou qualité ; joblib/pickle peuvent exécuter du code. Référence authentifiée, provenance et validation nécessaires ; alternatives skops.io/ONNX selon besoin. Poids nombreux ≠ explication simple ; autoencodeur ≠ architecture d’un LLM.

- [Et le Deep Learning ?](../../../ia-cybersecurite/it-4/et-le-deep-learning.md)


## Séquence 4.8 — Exploiter sans se fier aveuglément

Chaîne cible dessinée : journaux→qualité→préparation→modèles→file enrichie→analyste→décision, fail2ban indépendant. Automatique/humain, responsables proposés et pannes renseignés. V2 actuelle = CSV, pas intégration SOC déployée.

Avis : pas de production générale ; pilote local supervisé4semaines si charge réellement prise en compte, revue hebdomadaire et immédiate après incident/changement. Capacité30/semaine ≠ troncature de l’export. Cibles proposées à valider : rappel≥95%, précision≥85%, cas critiques sans régression, charge qualifiable ; V2 précision84,52% et104/135 alertes, donc pas validée.

Corpus/étiquettes/artefacts protégés et revus, versions/empreintes de référence, retour arrière ; contexte métier pour priorité, stock visible, aucun blocage modèle. Conditions et résumé complétés dans le rapport ; cinq questions à l’éditeur rédigées. Aucun accord RSSI ni déploiement revendiqué.

- [Exploiter sans se fier aveuglément](../../../ia-cybersecurite/it-4/exploiter-sans-se-fier-aveuglement.md)


**Remise finale préparée :** PDF13pages, dont rapport3pages ; archive `Remise-J4-Hexalp-Olivier-HIMBLOT.zip` avec fichiers exécutables, données et preuves. Manifeste SHA-256 et note de portée inclus. Ancien PDF intermédiaire conservé séparément, aucun envoi au formateur.
