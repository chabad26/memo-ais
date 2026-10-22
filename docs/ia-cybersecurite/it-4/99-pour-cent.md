# 99 %

## Lundi 12 octobre — Le premier lundi d'exploitation

Dans la suite du **scénario fictif Hexalp**, le script a été adopté par la supervision. Sofia le relance sur les deux semaines suivantes.

> **Sofia [08:58]** Bonjour ! J'ai relancé votre script sur les deux semaines du 28/09 au 11/10, j'ai juste changé le nom du fichier 🙂  
> Il affiche **99 % d'accuracy** 🎉 Par contre il a sorti **232 alertes**, l'astreinte n'en a lu qu'une vingtaine.

> **Hugo [09:12]** J'ai étiqueté les deux semaines, avec l'aide du CERT régional qui nous a signalé une campagne de password spraying sur les bastions de la région.  
> Et vendredi, en fouillant NetFlow à la main, j'ai trouvé **8,5 Go sortis par le bastion le 9/10 à 3 h**, depuis une adresse du VPN. Le script n'a rien dit.

> **Nadia [09:20]** 99 % et une exfiltration ratée ? 🤨  
> Avant de mettre quoi que ce soit en service, je veux un vrai rapport d'évaluation. Pour midi.

La date du 12 octobre et les chiffres 99 % / 232 / 8,5 Go sont les éléments de la consigne. Ce ne sont ni une date d'exécution réelle ni des résultats calculés ici. L'adoption racontée ne constitue pas une preuve de déploiement sur un SI réel.

## Mission — Trois hypothèses avant exploration

Avant d'ouvrir les fichiers, consigner dans `carnet_J4.md` trois explications possibles. Relire **A2 du J3** et **« j'ai juste changé le nom du fichier »**. Chaque hypothèse doit ensuite être confrontée aux données et au code, avec une conclusion : corroborée, infirmée ou non tranchée.

!!! note "Attribution et chronologie du travail"
    Cette fiche est intégrée le **22 octobre 2026**, après l'exploration anticipée du notebook 02 pendant la panne de Moodle et les sorties transmises dans la conversation le 21 octobre. Les hypothèses ci-dessous sont donc une **reconstitution pédagogique après exploration**, pas une preuve qu'elles ont été formulées à l'aveugle avant ouverture des fichiers. Le carnet conserve cette limite.

## Trois hypothèses proposées et leur vérification

| Hypothèse formulée | Pourquoi elle explique le paradoxe | Comment la vérifier | État au moment de cette fiche |
| --- | --- | --- | --- |
| **H1 — Le 99 % ne mesure pas la bonne situation d'exploitation** | En changeant seulement le fichier, Sofia peut avoir relancé l'entraînement et le test sur octobre, avec les réponses de Hugo. Ce n'est pas appliquer le modèle de septembre à des semaines nouvelles. De plus, un score global élevé peut masquer des attaques manquées parmi beaucoup de lignes normales | Lire le chargement, `fit`, le découpage et l'usage de `etiquette` ; identifier les périodes d'apprentissage/test ; mesurer rappel, FN et score d'une prédiction toujours normal | **Mécanisme corroboré** : la section 3 du notebook réentraîne sur une partie d'octobre et évalue sur l'autre. La sortie transmise affiche **0,997** après correction, pas une mesure de transfert septembre→octobre. Ce chiffre ne permet pas d'attribuer à lui seul la cause de l'exfiltration manquée du récit |
| **H2 — La mesure de volume a changé ou été mal préparée** | Un changement Mo/Ko ou une absence de mesure traitée comme zéro/valeur fixe peut masquer le volume inhabituel. Les entrées ne représentent alors plus la même réalité qu'en septembre | Comparer schéma, types, unités, valeurs manquantes et dates de changement ; contrôler la ligne du 9/10 à 3 h et convertir les mesures avant de prédire | **Changement et erreur de préparation observés** : nouvelle colonne `octets_sortants_ko`, relais de la mesure à partir du 29/09 ; un premier essai remplissait de nombreuses lignes avec **1 024 Mo**, corrigé ensuite par `Ko / 1024`. Après conversion, **14 lignes** restent sans volume. Le lien exact avec la ligne de 8,5 Go et son absence d'alerte reste à établir |
| **H3 — Le modèle généralise mal aux nouveaux comportements et à la nouvelle infrastructure** | Une connexion réussie depuis le VPN peut ressembler à une activité interne ordinaire ; une attaque lente ou un nouveau poste n'a pas forcément le profil des exemples appris. Un modèle peut aussi ne pas utiliser le volume dans ses règles | Comparer origine, IP nouvelles, profils, règles apprises, faux négatifs et période ; examiner la ligne ciblée et son chemin de décision, pas seulement un score moyen | **Indices corroborés, cause du cas précis non tranchée** : nouvelles IP internes dont `10.20.1.7` ; observations normales et attaques sous `10.20.250.*` ; proportion brute d'attaques passant d'environ **6,9 % à 10,1 %**. L'arbre J3 observé ne teste pas directement le volume. Les derniers résultats transmis montrent toutefois une branche différente : vérifier paramètres, ordre des caractéristiques et identité du modèle avant d'attribuer une erreur au même arbre |

Ces trois explications peuvent se cumuler. Ni le volume élevé, ni une source VPN/interne, ni une étiquette ne suffisent à expliquer seuls tout l'incident.

## Retour à A2 du J3 — Pourquoi 99 % ne suffit pas

Au J3, prédire toujours **normal** donnait environ **93,13 % de justesse sur les données brutes**, tout en manquant **les 117 attaques**. Ce résultat ne rendait pas la détection utile.

La question pour Nadia n'est donc pas seulement « combien de lignes sont bien classées ? », mais **quelles attaques sont manquées, combien d'alertes inutiles sont produites et lesquelles sont réellement traitées**. Une exfiltration grave peut se trouver parmi les quelques erreurs restantes d'un modèle apparemment excellent.

Le message de Sofia contient aussi un problème opérationnel distinct : **232 alertes pour une vingtaine lues**, soit un ordre de grandeur d'une alerte sur dix examinée. Ce n'est pas un décompte exact puisque « une vingtaine » est approximatif. Il faut distinguer une attaque **non signalée par le modèle** d'une attaque **signalée mais non examinée** : le récit affirme le premier cas pour l'exfiltration ; la saturation peut en ajouter d'autres.

## Ce que les résultats anticipés permettent déjà de dire

L'exploration transmise après correction de la conversion contient **2 105 observations évaluées**, dont **211 attaques**, et une file union annoncée de **259 alertes** : **114 puis 145 par semaine**, **53 faux positifs et 5 faux négatifs**. Ce sont des **sorties rapportées par l'apprenant**, pas les 232 alertes du récit ni une reproduction indépendante du protocole J3 strict.

**Ne pas confondre les versions :** le premier essai à 1 024 Mo fixes est à conserver comme erreur de préparation, non comme évaluation finale. Le dernier arbre imprimé utilise `echecs_auth ≤ 58,5` dans une branche interne, alors que l'arbre J3 à graine 42 utilisait `heure ≤ 19,5`. L'ordre exact des caractéristiques et les paramètres sont encore à confirmer dans la VM. Les chiffres du dernier essai ne sont donc pas présentés comme le résultat définitivement validé du modèle J3 figé.

Le rapport d'évaluation devra relier **version des données → préparation → modèle et paramètres → période d'évaluation → résultats → limites**. Aucun script V2 ni rapport final n'est produit à la place des consignes suivantes dans cette fiche d'ouverture.

## Travail attendu pour la matinée

Travailler en autonomie, sélectionner les cellules utiles du **notebook 02 comme boîte à outils**, puis consigner pour H1, H2 et H3 la preuve et la conclusion. Garder les résultats infirmant une hypothèse autant que ceux qui la soutiennent. Les rôles précis des nouvelles machines et les changements autorisés seront à rapprocher du journal DSI lorsqu'il sera fourni.

**Livrable commencé :** `livrables/ia-cybersecurite/it-4/IA_J4_ressources_apprenant/ia01-j4/carnet_J4.md`. La mission est renseignée avec sa chronologie réelle ; la qualification exacte de l'exfiltration et l'identité du modèle restent à vérifier.

## Liens

- [J3 — A2 et la référence toujours normal](../it-3/explorer-preparer-journaux.md)
- [J3 — Résultats et règles du classifieur](../it-3/le-classifieur-supervise.md)
- [J3 — Script, alertes et limites d'exploitation](../it-3/le-script-de-detection.md)
- [Retour à l'itération 4](index.md)
