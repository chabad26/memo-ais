# 2.4 — Atelier 4 | Mettre en commun les observations sur Modbus

**Itération 1 · Journée 2 · Débrief collectif et démonstration avec le formateur.**

## Objectif et statut

**Consolider la compréhension du protocole et relier les communications observées au fonctionnement de l’installation.**

Ce support de restitution est renseigné à partir des fichiers du laboratoire et des preuves individuelles des ateliers 2.1 à 2.3. Il ne constitue pas un compte rendu d’échanges collectifs déjà réalisés : comparaison avec les autres tables et corrections du formateur restent à consigner.

## 1 — Comparer les résultats de la matinée

### Synthèse à présenter

| Point | Résultat à expliquer | Preuve / limite |
| --- | --- | --- |
| Catégories de données | Coils et discrete inputs : bits ; input et holding registers : mots de 16 bits. Les droits effectifs dépendent du serveur. | [Table complète 2.3](cartographier-variables-tester-modbus.md#1-construire-la-table-des-variables), confrontée au code. |
| Lectures | FC01 coils, FC02 discrete inputs, FC03 holding, FC04 input. `status` utilise FC03, FC04 et FC01. | Requêtes FC03 à partir de 0 pour 3 registres et FC04 à partir de 0 pour 4 registres capturées en 2.3 ; réponse FC01 avec porte à 1, défaut à 0. FC02 n’est pas documentée en capture utilisateur. |
| Écritures | FC05 pour la porte ; FC06 pour la consigne ou le mode automatique. | Deux paires FC05 visibles et fermeture à 0x0000 détaillée en 2.3 ; FC06 détaillées en 2.2. |
| Températures | Les registres de consigne et de température utilisent les dixièmes de °C : 60 = 6 °C, 40 = 4 °C. | [Trames 34 et 74 de la capture 2.2](analyser-echanges-modbus-wireshark.md#captures-utilisateur-du-27-octobre-deroulement-et-preuves). Le facteur vient du mapping, pas du protocole lui-même. |
| Réponses normales | FC06 renvoie un écho de l’adresse et de la valeur. Un ACK TCP ne suffit pas à prouver une écriture Modbus acceptée. | Réponses **36** (60) et **76** (40), liées respectivement aux requêtes **34** et **74**, sans exception. |
| Exceptions | Une adresse non permise peut produire une réponse d’exception ; ce n’est pas une absence de réponse. | Script utilisateur `request(3, 100, 1)` → **`ProtocolError Modbus exception code 2`**. La PDU 83 02 n’est pas encore capturée par l’apprenant. |
| Décodage | Le port serveur du laboratoire est **15020**, pas le port conventionnel 502. | Décodage initial partiel et Query/Response inversés, puis résultat corrigé en 2.2. Le « malformed » initial n’a pas établi un défaut du serveur. |

### Points à comparer entre les tables des binômes

- **Table et adresse ensemble** : holding 0 est la consigne ; input 0 est la température ; coil 0 est la porte.
- **Base d’adressage** : utiliser les adresses PDU à partir de zéro, sans ajouter 1 arbitrairement.
- **Unités et codages** : dixièmes de degré pour les valeurs thermiques ; FC05 vrai = **0xFF00**, faux = **0x0000**.
- **Accès réel** : le défaut est modifiable par coil 1 et lu aussi par input 3 ; l’input register reste en lecture seule.
- **Doublons de représentation** : compresseur et alarme sont exposés dans les input registers et les discrete inputs ; ce sont les mêmes états du modèle.
- **Mode automatique** : `auto=0` suspend l’hystérésis, sans garantir l’arrêt du compresseur.
- **Limite conseillée** : holding 1 = 80, soit 8 °C, mais ce n’est pas une borne de consigne imposée par le programme.

### Exceptions et diagnostic : réponse proposée

Le test d’adresse 100 démontre un refus applicatif explicite. Le serveur reste joignable et répond **02 — Illegal Data Address**. Cela oriente vers la table, l’adresse ou la quantité demandée, plutôt que vers un redémarrage du serveur. Un timeout ou une connexion refusée demanderait d’autres vérifications. La signification normative et l’essai sont détaillés dans l’[atelier 2.3](cartographier-variables-tester-modbus.md#3-tester-une-adresse-invalide).

## 2 — Relier une écriture au processus

### Chaîne complète : consigne 4 → 6 °C

Exemple repris des écritures capturées en 2.2. Pour interpréter les effets de contrôle, vérifier **mode automatique actif, défaut inactif** et la version des seuils. La description ci-dessous utilise le modèle initial **±0,5 °C** ; la restauration de la variante ±1 °C reste à confirmer.

| Étape | Mécanisme dans le laboratoire | Temporalité et preuve disponible |
| --- | --- | --- |
| **1. Commande du client** | `python3 -m lab.client setpoint 6` convertit 6 en **60**, puis envoie **FC06**, holding **0**. | Requête **34**, client 127.0.0.1:60894 → serveur 127.0.0.1:15020 : capturée. |
| **2. Écriture du registre** | Le serveur traite FC06 ; `Plant.write_register(0, 60)` accepte la valeur et affecte `self.setpoint = 6.0`. | Réponse **36** avec registre 0 et valeur 60, sans exception, reçue **284 µs** après la requête selon Wireshark. |
| **3. Consigne du contrôleur** | Le registre holding 0 est une vue de `self.setpoint`, pas une copie externe à recopier dans un PLC séparé. | Étapes 2 et 3 correspondent ici à la même affectation interne. Une nouvelle lecture FC03 fournirait une vérification complémentaire. |
| **4. Commande du compresseur** | Au prochain appel de `advance()`, le contrôleur réévalue les seuils : avec consigne 6 °C, arrêt à **5,5 °C ou moins**, marche à **6,5 °C ou plus** ; état conservé entre les deux. | Pas nominal **0,1 s**, sans garantie de délai mural exact. Si la température est autour de 4 °C, le compresseur s’arrête s’il était en marche, ou reste arrêté. La requête ne prouve pas cette transition à elle seule. |
| **5. Évolution de température** | Le modèle calcule l’apport thermique de l’ambiance et le refroidissement selon la commande. | Évolution progressive, avec inertie simplifiée ; la température ne devient pas instantanément 6 °C. Les délais d’échange réseau ne sont pas des délais thermiques. |

Dans ce code, **la consigne change dès le traitement de l’écriture**, puis la commande est calculée au pas de simulation suivant. Les accès et le calcul sont protégés par un verrou : l’instant précis dépend de l’ordonnancement. L’affichage ajoute encore son propre rythme de rafraîchissement.

### Retour à 4 °C et limites de la preuve

La requête **74**, depuis le port client **60928**, écrit **40** dans le holding register 0. La réponse **76** reprend la valeur sans exception, après **486 µs**. Cela établit l’acceptation technique de la restauration, pas une remise instantanée de la température à 4 °C.

Les captures J1 de l’[atelier 1.3](prendre-en-main-modele-frigorifique.md) montrent aussi une consigne à 6 °C puis à 4 °C dans la supervision. **Elles appartiennent à une autre session** : elles illustrent les interfaces mais ne doivent pas être présentées comme une trace thermique synchronisée avec le PCAP du J2.

### Démonstration collective proposée

Si le formateur reprend l’essai : conserver le programme et ses seuils, les états initiaux, les lectures CLI et l’affichage, puis repérer la requête et sa réponse dans une capture. Relever séparément :

1. L’instant d’écriture et celui de la réponse.
2. La consigne relue après écriture.
3. Le changement éventuel de commande du compresseur.
4. Les températures successives et leurs instants d’observation.

Le résultat peut être cohérent même si la commande ne change pas : elle était peut-être déjà dans l’état demandé par les nouveaux seuils. Cette démonstration reste **à confirmer en collectif**, sans attribution au formateur d’un résultat non reçu.

## 3 — Identifier les limites du modèle

| Dimension | Modèle fourni | Installation réelle : ce qu’il faudrait connaître |
| --- | --- | --- |
| Interfaces physiques | Capteur et actionneur représentés par des variables de `Plant`. | Câblage, interfaces électriques, calibration, qualité de mesure et retours d’état. |
| Commande de froid | Un booléen active un coefficient de refroidissement. | Fonctionnement effectif du compresseur, puissance, pressions, inerties et défauts mécaniques. Une commande de marche ne prouve pas la production de froid. |
| Temps | Pas de 0,1 s avec attente nominale équivalente ; logique, physique et réseau partagent le serveur. | Cycle de contrôle, latences, gigue, délais de capteurs/actionneurs et limites temporelles admissibles. |
| Sûreté | Défaut injecté → arrêt du compresseur, selon le scénario. | Analyse de risques, protections, interverrouillages et état de sécurité validé. L’arrêt n’est pas une règle universelle. |
| Mesure en défaut | La température continue à être calculée et affichée ; le défaut n’est pas affiché par le dashboard. | Valeurs absentes, figées ou aberrantes, indication de qualité, redondance et alarmes de défaut dédiées. |
| Alarmes | Seuil > 8 °C pendant 10 s calculées, sans acquittement ni mémorisation indépendante. | Seuils applicables au procédé, temporisations, diffusion, acquittement et responsabilités. |
| Communications terrain | Pas de réseau matériel entre température, contrôleur et compresseur. Modbus relie surtout maintenance/supervision au serveur. | Bus et protocoles réels, topologie, mapping, comportement en perte de liaison et responsabilités des différents équipements. |
| Sécurité et validation | Modbus conventionnel sans authentification native ; protections du schéma cible non déployées par les essais. | Accès autorisés, segmentation, règles, traçabilité et tests de validation. Le bastion dessiné reste une proposition d’architecture. |

La réussite des échanges et des tests logiciels confirme un comportement dans le **périmètre fictif documenté**. Elle ne valide pas à elle seule une installation physique, ses protections ou la conservation de produits alimentaires.

## Synthèse proposée pour l’oral

> J’ai associé les variables aux tables et aux fonctions Modbus. Les captures montrent une consigne écrite à 60 puis restaurée à 40, avec deux réponses FC06 normales ; le laboratoire interprète ces valeurs comme 6 et 4 °C. L’exception 02 obtenue sur l’adresse 100 est une réponse de refus, distincte d’un timeout. Dans ce programme, écrire le registre modifie directement la consigne ; le compresseur est ensuite réévalué, puis la température évolue progressivement. Les échanges et leurs effets doivent être distingués : une réponse en microsecondes ne mesure pas la réaction thermique. Le modèle reste une simulation simplifiée sans matériel de terrain.

## Trace du débrief à compléter

| Élément | État |
| --- | --- |
| Support de restitution et comparaison des variables | Préparés sur les preuves individuelles. |
| Points de divergence entre binômes | À consigner après échange. |
| Corrections / confirmations du formateur | À consigner. |
| Démonstration collective et observations synchronisées | À confirmer et documenter. |
| Version de l’hystérésis utilisée et restauration finale | À vérifier avant les essais suivants. |

[Retour à l’itération 1](index.md) · [Table des variables et essais 2.3](cartographier-variables-tester-modbus.md)
