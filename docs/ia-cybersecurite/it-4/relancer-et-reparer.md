# Relancer et réparer

**Séquence 4.2 — 1 h 15 — Autonomie**

## Le problème à résoudre

Un modèle apprend sur une photographie du passé. Une modification de collecte, de machines ou d'usages peut changer ses entrées alors qu'il continue à produire un résultat. La première étape est donc de **comparer les données et le journal des changements**, avant de croire un score.

Cette feuille reprend **uniquement la section 4.2 du PDF fourni** : `Kit_apprenant_IA-01_Iteration_4.pdf`, lu depuis le dossier Downloads le **22 octobre 2026**. Les missions sont renseignées à partir du journal DSI, du kit et des sorties déjà transmises par l'apprenant. La 4.3 n'est pas préparée ici.

## Vocabulaire clé

| Terme | Repère |
| --- | --- |
| **Dérive — drift** | Les données ou comportements changent par rapport à l'entraînement. Un changement observé ne prouve pas à lui seul une dégradation du modèle : elle doit être mesurée |
| **Données non représentatives** | Exemples d'apprentissage qui couvrent mal les situations rencontrées ensuite |
| **Échec silencieux** | Le programme se termine et produit une sortie, mais son sens, sa couverture ou ses résultats ne correspondent plus au besoin |
| **Contrôle de qualité** | Vérification avant prédiction : schéma, unités, types, manques, valeurs plausibles et couverture conservée |

## Le journal des changements de la DSI

| Date | Changement fourni dans le PDF | Par |
| --- | --- | --- |
| **29/09, 8 h** | Remplacement de la sonde NetFlow ; volumes exportés dans une nouvelle colonne en kilooctets | Sofia |
| **30/09, 10 h** | Mise en service du proxy Zabbix **10.20.1.7**, qui collecte des métriques en SSH avec deux comptes de service | Sofia |
| **01/10** | Nouvelle passerelle VPN : **10.20.250.10 à .99** pour l'équipe infra ; **.100 à .200** pour les autres salariés | Julien |
| **04/10, 14–18 h** | Redémarrage de la sonde NetFlow après mise à jour | Sofia |
| **06/10, 21 h** | Scan de vulnérabilités mensuel depuis **10.20.1.250** | Hugo |

Ces informations sont des faits du **scénario**, pas des opérations réalisées sur une infrastructure réelle. Elles permettent maintenant d'identifier le rôle de nouvelles adresses ; elles ne légitiment pas automatiquement tout le trafic qui en provient.

## Mission 1 — Relancer et examiner le « 99 % »

### Essai de relance simple : préserver le script J3

Le PDF demande de changer le nom du fichier dans le script. Notre version dispose d'une option qui évite de modifier l'original. Dans la VM, depuis `~/ia01-j4`, après copie du script J3 :

```bash
source ~/ia01-j3/.venv/bin/activate
python detection_ssh.py --entree hexalp_ssh_oct2026.csv --sortie alertes_relance_simple.csv
```

**Cette relance précise n'est pas attestée par une sortie fournie.** Ne pas lui attribuer les chiffres de Sofia ni ceux d'un notebook déjà réparé. La lecture du script et le comptage du CSV montrent néanmoins son problème : sans conversion Ko→Mo, il retire les **1 953 valeurs vides de l'ancienne colonne**, même quand une mesure existe en Ko, et ne conserve que **166 lignes**, dont **9 attaques**. La couverture se limite alors à la première partie de la période ; aucune performance de cette relance n'est inventée.

### Pourquoi le score de Sofia n'est-il pas la bonne évaluation ?

La section 3 du notebook **réentraîne sur une partie d'octobre avec les étiquettes de Hugo**, puis teste sur une autre partie d'octobre. La dernière sortie transmise affiche **0,997** après la correction de préparation, contre **0,991** lors de l'essai erroné à volumes fixes. Ces valeurs correspondent à des versions différentes, pas à deux performances directement comparables.

**Le lundi matin, les nouvelles étiquettes qualifiées ne sont pas nécessairement disponibles.** Le protocole de Sofia ne répond donc pas à la question « comment le modèle de septembre se comporte-t-il sur la période suivante ? ». Le programme n'a pas besoin d'utiliser la colonne `etiquette` comme caractéristique pour que l'évaluation soit inadaptée : l'entraînement sur le mois à évaluer suffit à changer la question posée.

Le **99 % et les 232 alertes** du récit restent des éléments de contexte : les retrouver exactement n'est pas un critère de réussite si notre préparation, notre contamination ou nos paramètres diffèrent. Conserver la configuration précise de chaque essai.

## Mission 2 — Au moins cinq différences entre les périodes

Les comptes ci-dessous portent sur les **CSV bruts**, sauf mention contraire. Les colonnes statistiques de volume ne sont comparables qu'après harmonisation des unités.

| Ce qui a changé | Où je l'ai vu : cellule ou chiffre | Prévu au journal ? | Effet probable sur le modèle |
| --- | --- | --- | --- |
| **Nouvelle colonne `octets_sortants_ko`** | Section 1 : septembre **1 704 × 11**, octobre **2 119 × 12** ; aucune colonne disparue | **Oui**, sonde du 29/09 à 8 h | Ignorer la nouvelle mesure supprime des observations ou leur attribue un volume erroné ; conversion obligatoire |
| **La colonne Mo devient massivement vide** | **1 953** Mo absents en octobre ; seules **166** lignes ont des Mo renseignés. Les comptes par jour montrent le relais vers les Ko le 29/09 | **Oui**, même changement de sonde | Ne pas interpréter tous ces vides comme une panne ou du trafic nul ; risque d'échec silencieux malgré un tableau numérique complet |
| **Une panne réelle affecte les deux mesures** | Après rapprochement Mo/Ko : **14 lignes sans aucun volume**, le **04/10 aux heures 14 à 18 incluses** ; aucune ligne avec les deux volumes renseignés dans le fichier reçu | **Oui**, redémarrage du 04/10 | Perte réelle de couverture ; une conversion ne récupère pas une mesure jamais collectée. Les tranches horaires ne donnent pas à elles seules les instants précis de panne |
| **Nouveau proxy Zabbix `10.20.1.7`** | Cellule des IP nouvelles : **278 observations**, toutes étiquetées normal ; des pics d'essais sur plusieurs comptes apparaissent dans les sorties | **Oui**, mise en service du 30/09 à 10 h | Profil légitime non appris ; faux positifs possibles. Le journal mentionne deux comptes, mais certaines lignes affichent quatre comptes distincts : écart à investiguer, pas à effacer par une liste blanche |
| **Nouvelles adresses VPN `10.20.250.*`** | Nouvelles IP internes, normales et attaques, dans la cellule de comparaison | **Oui**, passerelle du 01/10 et plages attribuées | Une source classée interne peut correspondre à un accès VPN compromis ; ne pas confondre origine réseau et confiance |
| **Part d'attaques plus élevée** | Septembre **117/1 704 = 6,87 %** ; octobre **215/2 119 = 10,15 %** (affichage arrondi 0,101) | **Non** dans ce journal ; campagne signalée par Hugo en 4.1 | Changement de distribution et charge potentielle ; comparer rappel, FP/FN et alertes, pas seulement accuracy |
| **Attaques internes et accès externes légitimes** | Octobre : **17 attaques internes / 1 891 normales internes**, **198 attaques externes / 13 normales externes** | VPN prévu ; intentions et attaques **non déductibles du journal** | Un raccourci « interne = normal » ou « externe = attaque » se trompe |
| **Nouveau pic journalier d'attaques étiquetées** | Graphique : hausse à partir du **03/10**, maximum **31 observations** le 06/10 | **Pas de justification suffisante** dans le journal | Peut traduire des méthodes ou une activité différentes ; une observation IP/heure n'est pas un incident distinct et le total quotidien ne donne pas un taux sans dénominateur |
| **Scanner autorisé en octobre** | Journal du **06/10 à 21 h** ; sorties avec **10.20.1.250** et étiquettes normales | **Oui** | Ses essais peuvent ressembler à des attaques. L'autorisation n'exempte pas toute activité future de l'IP ; comparer au périmètre et à la fenêtre réellement prévus |

Les rôles du proxy et des plages VPN sont désormais documentés par le PDF, contrairement aux premières hypothèses d'exploration. La plage **.100–.200 n'est pas malveillante par définition** : elle désigne les autres salariés. Les comptes d'alertes du modèle ne sont pas utilisés pour déclarer un rôle ou une autorisation.

## Mission 3 — Adapter la préparation

### Conversion correcte et choix de nettoyage du J3

**Ne pas modifier le CSV d'octobre à la main.** Recharger les sources si une ancienne cellule a inséré du texte ou une constante, puis appliquer une transformation reproductible :

```python
septembre = pd.read_csv(FICHIER_SEPT)
octobre = pd.read_csv(FICHIER_OCT)

# Convention explicitement donnée dans le kit : 1 Mo = 1024 Ko.
octobre["octets_sortants_mo"] = octobre["octets_sortants_mo"].fillna(
    octobre["octets_sortants_ko"] / 1024
)

print("Volumes manquants septembre :", septembre["octets_sortants_mo"].isna().sum())
print("Volumes manquants octobre :", octobre["octets_sortants_mo"].isna().sum())

# Même stratégie que notre J3, pas celle du corrigé générique par médiane.
septembre = septembre.dropna(subset=["octets_sortants_mo"]).copy()
octobre = octobre.dropna(subset=["octets_sortants_mo"]).copy()

for jeu in [septembre, octobre]:
    if not jeu["origine"].isin(["interne", "externe"]).all():
        raise ValueError("Origine inconnue : codage à vérifier")
    jeu["externe"] = (jeu["origine"] == "externe").astype(int)
```

**Comptages de référence vérifiés en lecture seule sur les fichiers :** septembre perd 90 lignes, dont 9 attaques, et conserve **1 614 / 108 attaques** ; octobre perd 14 lignes, dont 4 attaques, et conserve **2 105 / 211 attaques**. Les sorties corrigées de l'apprenant concordent avec les effectifs d'octobre ; le code exact et l'identité du modèle devront rester traçables pour la suite.

Lors du premier essai, les **1 024 Mo constants** observés n'étaient pas une conversion : **671 Ko / 1 024 ≈ 0,655 Mo**, et **2 171 Ko / 1 024 ≈ 2,120 Mo**. Zéro case vide ne signifie donc pas automatiquement préparation correcte.

### 1. Que se passe-t-il sans adaptation ? Pourquoi pas d'erreur ?

**Dans le chemin générique par médiane du kit**, les nouvelles mesures Ko ne sont pas lues : les trous de la colonne Mo sont remplacés par une valeur centrale artificielle. Le tableau reste numérique et complet, donc le modèle peut prédire sans erreur Python ; la signification de ses entrées est pourtant fausse. Le volume d'une exfiltration peut disparaître dans ce remplacement.

**Dans notre script réellement produit au J3**, le choix était différent : suppression des volumes absents. Sans adaptation, **1 953 lignes sont exclues et seulement 166 conservées**, malgré les 1 939 mesures disponibles en Ko. Le programme peut poursuivre avec une couverture très insuffisante parce qu'il vérifie les colonnes requises et les valeurs, sans exiger une couverture minimale ni bloquer tout nouveau schéma. Il affiche le nombre de lignes exclues : le signal existe, mais aucune alerte bloquante de qualité n'est imposée.

Ces mécanismes ne sont pas interchangeables : écrire « notre script remplace les trous par la médiane » serait inexact. Un remplissage à zéro ou par une constante serait une troisième erreur de sens.

### 2. Quel contrôle ajouter pour s'arrêter plutôt que se tromper ?

Avant toute prédiction, contrôler **schéma et unités attendus**, présence du changement Ko, validité des mesures, chevauchement éventuel des deux unités et proportion/période de mesures réellement absentes. Le contrat doit distinguer un changement inconnu — arrêt — d'un changement reconnu avec conversion validée.

Exemple de **contrôle à ajouter à l'ancienne préparation J3**, pour empêcher une relance naïve ; il est illustratif et n'est pas encore une V2 :

```python
if "octets_sortants_ko" in df.columns:
    raise ValueError(
        "Nouveau format NetFlow : conversion Ko vers Mo à valider avant détection"
    )
```

Une fois la conversion intégrée, ce contrôle doit évoluer : ne pas continuer à refuser un format désormais pris en charge. Mesurer les volumes manquants **après conversion**, vérifier les types et plages, signaler les périodes hors couverture et arrêter selon un seuil convenu avec Nadia. Une limite de couverture arbitraire ne doit pas devenir une décision métier cachée dans le code.

Contrôler aussi les effectifs par jour et la période traitée : un fichier de sortie présent ne prouve pas que les deux semaines ont été analysées. Les mesures hors couverture restent visibles et suivies, pas classées normales.

### 3. Qui devait prévenir qui, quand ?

**Avant le remplacement du 29 septembre**, Sofia et le responsable du changement de collecte devaient informer l'équipe qui maintient le détecteur et l'astreinte, avec schéma, unité, heure de bascule et procédure de retour arrière. Les changements de proxy/VPN et les audits devaient également être communiqués avant leur mise en service ou leur fenêtre prévue, à la supervision et au SOC ; Nadia doit pouvoir arbitrer les impacts et conditions d'exploitation.

Il s'agit d'une responsabilité d'organisation et de coordination : la seule lecture du journal ne permet pas de conclure qui a effectivement reçu ou ignoré une information.

| À ajouter à la procédure de changement | Preuve attendue |
| --- | --- |
| Identifier les consommateurs des données et le responsable de chaque modèle | Liste des équipes dépendantes et propriétaire du détecteur |
| Décrire schéma, unités, plages d'adresses, comptes et dates d'effet | Contrat de données versionné, exemples et journal accessible |
| Tester la compatibilité avant bascule | Contrôles sur échantillon fictif/autorisé, conversion et couverture vérifiées |
| Décider arrêt, mode dégradé et retour arrière | Procédure validée, seuils et personnes habilitées |
| Vérifier après changement et conserver les traces | Comptages par période, traitement des pannes et revue des alertes |

**Le modèle ne lit pas le journal des changements. L'équipe, elle, doit le relier à la chaîne de préparation.** Une modification planifiée de l'infrastructure n'est pas automatiquement une raison de réentraîner : vérifier d'abord si la collecte ou l'unité est en cause.

## Carnet et limites de preuve

Les trois missions sont consignées dans **`livrables/ia-cybersecurite/it-4/IA_J4_ressources_apprenant/ia01-j4/carnet_J4.md`**. Les faits du journal proviennent du PDF ; effectifs et colonnes sont vérifiés dans le kit ; les sorties du notebook ont été transmises par l'apprenant. Aucune exécution de la relance simple sur les 166 lignes n'est revendiquée, aucun score supplémentaire ni V2 généré pour cette fiche.

La section 3 fournit un score de réentraînement sur octobre ; le contrôle du modèle figé et son évaluation temporelle seront traités **en 4.3**, à la demande suivante. Le fichier `.joblib` reste non chargé.

## Ressources

- **Source du cours :** PDF local `Kit_apprenant_IA-01_Iteration_4.pdf`, section **4.2 — Relancer et réparer**, consulté le 22 octobre 2026.
- [Scikit-learn — Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html), référence de méthode déjà consultée pendant le J3.
- [J3 — Fiche et script du modèle](../it-3/le-script-de-detection.md)
- [Retour à l'itération 4](index.md)
