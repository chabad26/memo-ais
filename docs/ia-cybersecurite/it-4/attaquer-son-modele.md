# Attaquer son modèle

**Séquence 4.6 — 1 h 30 — Présentiel**

## Objectif et périmètre des expériences

Un modèle peut divulguer ses règles, être contourné à la prédiction ou être empoisonné lors d’un prochain entraînement. La mission consiste à exécuter les parties A à D du notebook 03, répondre à A1–D4, puis compléter le rapport et le tableau de synthèse.

**Toutes les expériences décrites ici sont des simulations locales sur les données fictives du kit.** Aucun compte, bastion ou service réel n’a été attaqué. Le notebook a été complété et exécuté avec assistance dans un environnement distinct de la VM de l’apprenant, le 22 octobre 2026. Une démonstration sur un système réel nécessiterait l’autorisation écrite de son propriétaire.

### Deux modèles à ne pas confondre

| Paramètre | Variante pédagogique du notebook 03 | V2 retenue pour la remise |
| --- | --- | --- |
| Volumes manquants | Médiane en septembre ; conversion puis médiane en octobre | Conversion Ko/1 024 en octobre ; exclusion des vrais manques |
| Ordre des variables | Échecs, succès, comptes, durée, volume, heure, externe | Heure, externe, échecs, succès, comptes, durée, volume |
| Contamination | **0,05** | **0,03** |
| Arbre et graine | Profondeur 3, graine 42 | Profondeur 3, graine 42 |
| Septembre préparé | 1 704 lignes ; entraînement arbre 1 192, test 512 | 1 614 lignes ; entraînement arbre 1 129, test 485 |

L’affirmation du notebook source « exactement le modèle du J3 » ne s’applique donc pas à nos choix. Les missions initiales sont exécutées sur la **variante du kit** ; une vérification séparée de la **V2** est ajoutée en fin de notebook. Le script V2 et son CSV d’octobre ne sont pas remplacés, ni empoisonnés sur disque.

## Partie A — Interroger le modèle

### A1 — Seuils et nombre de requêtes

Sur le scénario précis de `sonde()` (10 échecs, aucun succès, origine externe, durée et volume nuls), la variante du kit signale **à partir de quatre comptes à 14 h**. Avec deux comptes, elle ne signale plus **à partir de 9 h**.

| Recherche | Valeurs interrogées, dans l’ordre | Conclusion |
| --- | --- | --- |
| Comptes à 14 h | 32, 16, 8, 4, 2, 3 | 4 repéré ; 3 non repéré — **6 requêtes** |
| Heure avec deux comptes | 12, 6, 9, 8 | 8 h repéré ; 9 h non repéré — **4 requêtes** |

Soit **10 appels enregistrés à `sonde()`** pour les deux recherches. L’export de l’arbre confirme ses coupures à 3,5 comptes et 8,5 h pour ce profil. Cela révèle une frontière locale, pas tout le fonctionnement de l’Isolation Forest. La dichotomie suppose une transition ordonnée dans l’intervalle étudié ; elle ne garantit pas la recherche d’une frontière arbitraire non monotone.

**V2 : le même spraying est signalé aux 24 heures testées.** Sa branche « durée ≤ 0,5 min et au plus trois comptes » classe ces observations en attaque. Les seuils 4 comptes/9 h du kit ne sont donc pas transposables à notre V2.


![Sondes sur les comptes et les horaires, puis export de l’arbre](../../assets/img/ia-cybersecurite/it-4/Capture%20d’écran%20du%202026-10-22%2009-59-44.png)

*Capture fournie par l’apprenant, 09:59:44 : six sondes pour les comptes, quatre pour les heures ; les coupures à 3,5 comptes et 8,5 h sont visibles dans l’arbre de la variante du kit. Ce sont des frontières locales du scénario, pas une extraction complète de la forêt.*

### A2 — Jusqu’à 1 000 comptes

Pour localiser une frontière monotone parmi environ 1 000 possibilités, une dichotomie nécessite **au plus 10 requêtes au pire cas**, car 2¹⁰ = 1 024. Ce n’est pas dix requêtes obligatoires pour chaque cas : une frontière favorable peut être trouvée plus vite. Il faut aussi vérifier l’existence de la transition et les bornes ; un modèle non monotone ne respecte pas nécessairement cette hypothèse.

### A3 — Où trouver les règles chez Hexalp ?

Dans le script et les paramètres, le dépôt de code, un export `export_text`, des journaux de debug, un modèle sérialisé ou un partage réseau trop ouvert. Le CSV d’alertes et ses scores donnent des indices sur les réactions, sans contenir nécessairement tout l’arbre. Ici, le notebook fournit un oracle explicite ; en exploitation, aucun blocage automatique n’existe dans la V2, donc l’attaquant ne dispose pas forcément d’un signal observable aussi précis. Restreindre accès et diffusion, journaliser les consultations ; la confidentialité des seuils seule ne suffit pas à protéger le système.

## Partie B — Passer sous le radar

### B1 — Le spraying dans le laboratoire

Le scénario testé utilise **10 échecs par heure, deux comptes, à 14 h**. Sur la variante du kit, il ne lève aucune alerte de **9 h à 23 h inclus**, soit 15 créneaux : **150 essais par jour par IP**, ou **30 000 avec 200 IP**, si les comportements sont indépendants et que les autres contrôles ne les arrêtent pas. Ce scénario illustre le défaut d’une observation limitée à une IP et une heure ; ce n’est pas un maximum global démontré.

Sur la V2, ce même scénario lève une alerte à chaque heure : **le contournement par ce plan n’est pas réussi**. Cela ne prouve pas une résistance à tous les autres plans.

### B2 — Et fail2ban ?

Dix échecs dans une heure ne disent pas comment ils sont espacés. En rafale, cinq dans dix minutes déclenchent la règle. Régulièrement espacés de six minutes, ces dix essais restent sous le seuil décrit, sous réserve du filtrage et des autres événements de la même IP.

Pour éviter ce seuil dans le modèle simplifié, il faut rester à **quatre échecs au maximum dans toute fenêtre de dix minutes** : un ordre de grandeur inférieur ou égal à 24 par heure en régime régulier, avec marge pour les bornes et l’horodatage. Ce n’est pas une autorisation de 24 essais concentrés dans une même minute. Le modèle horaire ne contient pas ces horodatages fins : **conserver fail2ban et une corrélation par compte/source**, plutôt que remplacer l’un par l’autre.

### B3 — Fractionner une exfiltration

Dans le kit, transférer **5 000 Mo en une heure à 23 h** est signalé. Pour les volumes échantillonnés, la première alerte apparaît à 2 000 Mo à 1 h et 23 h, et à 3 000 Mo à 3 h. À 10 h et 14 h, aucune alerte jusqu’à 4 000 Mo testés. Ces essais ne donnent pas un seuil exact entre deux valeurs ni une garantie au-delà de la grille.

Un scénario fictif de **cinq transferts de 1 000 Mo, de 9 h à 13 h**, avec un compte, un succès et une session de 45 minutes à chaque heure, n’est signalé par **aucune des deux variantes**, kit et V2. L’adversaire met cinq heures au lieu d’une, doit conserver son accès et augmente son exposition à d’autres contrôles. Les simulations décrivent des vecteurs d’observation ; elles n’exécutent aucun transfert réseau.


![Spraying sans alerte et transfert de 5 000 Mo signalé](../../assets/img/ia-cybersecurite/it-4/Capture%20d’écran%20du%202026-10-22%2009-59-57.png)

*Capture fournie par l’apprenant, 09:59:57 : le scénario à dix échecs et deux comptes passe de 9 h à 23 h, soit 150 essais/jour/IP. Le transfert synthétique de 5 000 Mo à 23 h est signalé ; la grille teste quelques volumes et horaires. Le plan fractionné de cinq heures n’est pas visible sur cette capture et reste attribué à la vérification locale.*

### B4 — Ce qui manque au modèle

Le **volume cumulé par identité sur plusieurs heures ou jours**, comparé au rôle et aux destinations habituelles, révélerait mieux ce fractionnement. Ajouter une fenêtre glissante, le contexte VPN et la destination est une piste ; elle doit être évaluée sur les usages légitimes. Une IP seule n’identifie pas toujours une personne ni un hôte derrière un VPN/NAT.

## Partie C — La liste blanche

### C1 — Gain visible, perte de couverture

Sur la variante du kit, exclure `10.20.8.30` supprime **19 alertes en deux semaines** : 10 puis 9. La file passe de **185 à 166**. Gain théorique : **1 h 40 puis 1 h 30**, soit **1 h 35 par semaine en moyenne**, à dix minutes par alerte.

Sur la V2, la même IP est à l’origine de **10 alertes** sur deux semaines : **1 h 40 au total**, soit 50 minutes par semaine en moyenne. Les deux chiffres ne décrivent pas le même modèle. Aucune liste blanche n’a été ajoutée à `detection_ssh_v2.py`.


![Liste blanche corrigée : 19 alertes supprimées sur 185](../../assets/img/ia-cybersecurite/it-4/Capture%20d’écran%20du%202026-10-22%2010-04-43.png)

*Capture fournie par l’apprenant, 10:04:43 : `LISTE_BLANCHE = ["10.20.8.30"]` est renseignée ; les compteurs affichent **185 avant, 19 supprimées et 166 après**. Elle confirme le filtrage des observations d’octobre de cette IP dans la variante du kit. Le transfert synthétique de 9 000 Mo reste signalé par le modèle. La dernière phrase sur ce que verra l’analyste est imprimée par le notebook ; l’insertion puis le filtrage de cette observation synthétique ne sont pas montrés.*

La capture corrigée remplace l’essai incomplet précédent. Les 19 suppressions sont désormais illustrées par la preuve de l’apprenant et concordent avec la vérification locale. La liste blanche reste une simulation du notebook, sans modification du script V2.

### C2 — Comment l’adversaire en profite

L’expérience synthétique de **9 000 Mo à 1 h** lève une alerte dans les deux variantes. Une exemption globale de l’IP la supprimerait après la prédiction, indépendamment du score : la perte de visibilité vient alors de la politique, pas du classifieur.

Un adversaire qui compromet le serveur exempté peut profiter de cette suppression. Connaître l’IP ne donne pas, à lui seul, la capacité d’émettre une session SSH depuis ce serveur. Proposer que les modifications soient réalisées par l’équipe supervision habilitée, après validation RSSI/SOC, avec revue et traçabilité ; le dossier ne prouve pas que cette gouvernance existe déjà.

### C3 — Une exception plus étroite

Rapprocher l’événement d’une **tâche de sauvegarde connue**, d’une identité de service, de destinations autorisées, d’une fenêtre et d’une enveloppe de volume validées. Diminuer la priorité des événements concordants, conserver leur trace et alerter sur un écart. Prévoir expiration et revue de l’exception. Avec les colonnes actuelles, l’identité et la destination manquent : cette règle complète n’est pas implémentable sans enrichissement. Ne pas fabriquer un seuil universel à partir des seules fausses alertes du TP.

## Partie D — Empoisonner l’apprentissage

### D1 — Ajouter de fausses étiquettes

L’expérience ajoute des profils de spraying étiquetés `normal` à l’entraînement, puis teste le profil préparé de six échecs sur cinq comptes à 14 h. Elle ne modifie aucun fichier source.

| Fausses lignes testées | Attaque préparée : arbre du kit | Attaque préparée : union V2 après empoisonnement de son arbre |
| ---: | --- | --- |
| 0 | Signalée | Signalée |
| 2 | Signalée | Signalée |
| 4 | Signalée | **Non signalée** |
| 5 | **Non signalée** | Non signalée |
| 10 | Non signalée | Non signalée |
| 20 | Non signalée | Non signalée |

Premières quantités réussies **parmi les valeurs testées** : **cinq lignes dans le kit**, soit 5 / 1 197 = **0,42 %** de l’entraînement empoisonné ; **quatre pour la V2**, soit 4 / 1 133 = **0,35 %**. Les simulations régénèrent les lignes avec la même graine pour chaque taille : les ensembles ne sont pas nécessairement des préfixes les uns des autres. Ces nombres ne sont donc pas des seuils universels de compromission. Deux composantes peuvent se compléter, mais ici l’Isolation Forest V2 ne rattrape pas le profil quand l’arbre est empoisonné.


![Début des expériences d’empoisonnement des étiquettes](../../assets/img/ia-cybersecurite/it-4/Capture%20d’écran%20du%202026-10-22%2010-04-57.png)

*Capture fournie par l’apprenant, 10:04:57 : le profil préparé est d’abord signalé, puis la boucle sur 0, 2, 4, 5, 10, 20 lignes est visible ; zéro, deux et quatre lignes ne suffisent pas à faire classer le profil préparé en normal dans la variante du kit.*


![Empoisonnement réussi dès cinq lignes testées dans le kit](../../assets/img/ia-cybersecurite/it-4/Capture%20d’écran%20du%202026-10-22%2010-05-12.png)

*Capture fournie par l’apprenant, 10:05:12 : à cinq lignes, le profil préparé est classé normal et le rappel attaque tombe à 0,80 ; à dix et vingt lignes il reste classé normal. Le test contient 512 lignes et 35 attaques : il s’agit de la variante du kit, pas du test V2 de 485 lignes.*

### D2 — Les métriques permettraient-elles de le voir ?

Le kit montre une baisse du rappel de l’arbre d’environ **89 % à 80 %** entre zéro et cinq fausses lignes, tandis que l’accuracy arrondie reste autour de 98–99 %. Une lecture des erreurs par classe peut donc alerter.

Sur la V2 :

| Fausses lignes | VN | FP | FN | VP | Rappel attaque |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 453 | 0 | 4 | 28 | 87,50 % |
| 4 | 452 | 1 | 7 | 25 | 78,13 % |
| 20 | 453 | 0 | 4 | 28 | 87,50 % |

**À vingt lignes, la matrice globale du test est identique à l’originale, mais l’attaque préparée passe.** Même une matrice stable ne suffit donc pas à exclure un empoisonnement ciblé. Contrôler aussi la provenance des ajouts, les changements de règles et des cas de test de sécurité indépendants. Le test de septembre ne représente pas tous les scénarios possibles.

### D3 — Empoisonner sans étiquette

On ajoute au corpus d’apprentissage des observations synthétiques de transferts nocturnes importants. Un « nombre de nuits » est ici un **nombre de lignes ajoutées**, pas des nuits réellement attendues ni une durée minimale réaliste démontrée.

| Observations nocturnes ajoutées | VPN repérés par IF du kit, sur 9 | VPN repérés par IF V2, sur 9 |
| ---: | ---: | ---: |
| 0 | 9 | 5 |
| 10 | 9 | 8 |
| 20 | 5 | 5 |
| 40 | 6 | 5 |
| 80 | 2 | 0 |

Pour le kit, les premières pertes apparaissent **à vingt observations parmi les tailles testées** ; après quatre-vingts, **sept passent**. La V2 en manque déjà quatre à l’état initial ; à quatre-vingts ajouts, **les neuf passent devant son Isolation Forest**. L’arbre initial classe ces neuf VPN en normal dans notre V2 ; il ne les rattrape donc pas.

La réponse n’est pas monotone : dix ajouts améliorent même ce résultat de la V2, et quarante ajouts donnent six détections dans le kit contre cinq avec vingt. Le réentraînement change les arbres et la distribution des scores, pas seulement un compteur de cas connus.

L’adversaire n’a pas besoin d’écrire directement les étiquettes ou le fichier si ses activités réelles finissent dans le futur corpus : il lui faut un accès permettant ces activités, du temps, et **une réutilisation insuffisamment contrôlée de ces traces à l’entraînement**. Le script actuel réentraîne sur septembre figé : l’usage hostile d’octobre ne le modifie pas spontanément.


![Empoisonnement comportemental et détections des neuf VPN](../../assets/img/ia-cybersecurite/it-4/Capture%20d’écran%20du%202026-10-22%2010-03-02.png)

*Capture fournie par l’apprenant, 10:03:02 : la boucle parcourt 0, 10, 20, 40 et 80 observations ajoutées ; les détections après empoisonnement sont respectivement 9, 9, 5, 6 et 2 sur neuf. Ces résultats illustrent un effet non monotone dans la variante du kit à contamination 0,05.*

### D4 — Trois protections

1. **Accès et provenance** : sources et corpus validés en lecture seule pour l’exploitation, séparation des droits de collecte, annotation et validation ; journaliser les ajouts et conserver les versions.
2. **Intégrité et qualité** : comparer empreintes et versions à une référence approuvée, faire relire les étiquettes et mettre les périodes suspectes en quarantaine. Une empreinte calculée après altération ne prouve pas l’authenticité.
3. **Validation avant remplacement** : comparer l’ancien et le nouveau modèle sur une période indépendante et des cas de sécurité ciblés, examiner dérives et erreurs par profil, approbation RSSI/SOC et retour arrière possible. Ne pas apprendre automatiquement que « fréquent = légitime ».

## Tableau de synthèse de la mission

| Attaque | Résultat obtenu dans le laboratoire | Mesure préventive ou de visibilité proposée | Responsable proposé chez Hexalp |
| --- | --- | --- | --- |
| **Extraction** | Frontières locales du kit trouvées en dix sondes ; règles lisibles à l’export. Pas d’extraction complète de la forêt ni de transfert des seuils à la V2 | Restreindre script, artefacts et scores ; tracer les consultations ; surveiller les sondes | DSI / équipe supervision / SOC |
| **Contournement : spraying** | Kit : 150 essais/jour/IP pour le scénario testé ; même plan repéré par la V2 | Garder fail2ban ; corréler essais par compte et plusieurs sources/heures | Administrateurs bastion et SOC |
| **Contournement : exfiltration** | Cinq observations de 1 000 Mo de 9 h à 13 h passent dans les deux variantes | Volumes cumulés par identité, destinations et contexte VPN | SOC / réseau / supervision |
| **Liste blanche** | 9 000 Mo signalés par les deux modèles mais masqués par une exemption globale simulée | Exception contextualisée, traçable, temporaire ; pas d’exemption globale | Supervision, validation RSSI/SOC |
| **Empoisonnement des étiquettes** | Profil préparé non signalé dès cinq lignes testées dans le kit, quatre dans la V2 ; test global parfois inchangé | Restreindre les écritures, revoir les annotations, tests ciblés avant remplacement | Responsable corpus / Hugo, équipe modèle, RSSI |
| **Empoisonnement comportemental** | À 80 observations ajoutées : sept VPN non détectés dans le kit, neuf dans la V2 | Revue des nouvelles périodes, quarantaine, validation et retour arrière | SOC / équipe modèle / RSSI |

Les responsabilités de ce tableau sont **proposées**, pas des habilitations établies par les pièces. Aucune mesure n’est démontrée comme bloquant toutes les variantes d’une attaque.

## Captures de l’apprenant et limites

Six captures du 22 octobre illustrent les parties A à D et concordent avec les résultats de la variante du kit, y compris la liste blanche corrigée (185 → 166, soit 19 suppressions). Elles ne montrent ni l’exécution des vérifications supplémentaires V2 ni l’environnement Python et le poste utilisés : ces résultats V2 restent attribués à l’environnement local de l’assistant. Les captures ne démontrent aucun transfert ou attaque sur un système réel.

## Fichiers et portée de la preuve

Dans `livrables/ia-cybersecurite/it-4/IA_J4_ressources_apprenant/ia01-j4/` :

- **`03_attaquer_le_modele.ipynb`** : complété et exécuté localement, sorties conservées, avec distinction kit/V2 et vérifications supplémentaires.
- **`03_attaquer_le_modele.source.ipynb`** : original fourni, conservé avant modification.
- **`preuves/execution_attaques_46.txt`** : sorties textuelles du notebook.
- **`preuves/attaques_46_v2.json`** : comptes et matrices des essais V2.
- **`carnet_J4.md`**, **`rapport_evaluation.md`** : réponses et synthèse mises à jour.

Le générateur `livrables/ia-cybersecurite/it-4/completer_notebook_46.py` reproduit les compléments à partir de la source conservée. L’exécution utilise Python 3.14.4, pandas 3.0.6 et Scikit-learn 1.9.1 dans l’environnement local de vérification ; elle ne prouve pas une exécution dans la VM. Le PDF intermédiaire n’est pas régénéré : la remise groupée sera actualisée en fin d’itération.

- [Le mur des matrices — 4.5](le-mur-des-matrices.md)
- [Rapport d’évaluation — 4.4](le-rapport-evaluation.md)
