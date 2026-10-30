# 5.2 — Atelier 2 | Analyser les traces et reconstituer les événements

## 🎯 Objectif et modalités

Exploiter les données disponibles pour reconstruire la chronologie d’un incident industriel.

**Modalité :** investigation en binôme. **Durée :** à compléter, non précisée. **Environnement :** dossier fictif Montval fourni par le formateur, Wireshark et outils Linux.

!!! info "Analyse documentaire réalisée le 30 octobre 2026"
    Le PCAP et les CSV reçus ont été analysés hors ligne avec Python et tcpdump. Les résultats ci-dessous portent sur les **traces synthétiques du 8 octobre**, pas sur une installation réelle. Aucun nouveau test PoC ni entretien n’est déclaré réalisé. Huit captures utilisateur sont désormais intégrées : exécution locale du script et de tcpdump, vue Wireshark et détails des trames 3/4, 9/10 et 15/16. Les valeurs des registres restent établies par les octets du fichier, car elles ne sont pas affichées dans ces détails Wireshark.

## 1 — Examiner les sources et leurs limites

L’[inventaire 5.1](prendre-connaissance-incident.md#2-inventaire-des-sources-recues) décrit les sept fichiers originaux. Les empreintes initiales sont conservées ; les résultats dérivés n’écrasent pas les sources.

| Source effectivement analysée | Ce qu’elle établit dans le dossier | Limite |
| --- | --- | --- |
| PCAP, 18 trames | Deux clients, FC03/FC06, trois paires d’écriture et réponses ; valeurs encodées des réponses de lecture. | Synthétique et partiel ; incohérence de quantité dans les six lectures FC03 ; pas d’authentification humaine. |
| Mesures, 181 lignes de données | États enregistrés chaque minute de 08:30 à 11:30 ; évolution des consignes, températures, commandes et alarmes. | Mesures d’enceinte, pas produits ; commande compresseur ≠ vérification mécanique. |
| SUP-01 | Changements, signalement d’alarme, acquittement et suivi. | Journal applicatif ; ne constitue pas une identité humaine authentifiée. |
| VPN, six événements | Trois plages de session vers MAINT-01 après correction temporelle. | Compte partagé pour les deux premières ; identité, intégrité du poste et autorisation ne découlent pas du seul journal. |
| Maintenance, huit événements | FM-426, déclarations et autorisation corrective INC-881. | Ticket et déclaration à confronter aux traces ; pièces éventuellement manquantes. |

[Archive originale](../../assets/files/informatique-industrielle/it-4/Montval-J5-Incident_dossier.zip) · [Décodage des trames CSV](../../assets/files/informatique-industrielle/it-4/Montval-5.2-modbus-decode.csv) · [VPN normalisé CSV](../../assets/files/informatique-industrielle/it-4/Montval-5.2-vpn-normalise.csv) · [Synthèse calculée JSON](../../assets/files/informatique-industrielle/it-4/Montval-5.2-synthese-analyse.json).

Le script reproductible `livrables/informatique-industrielle/it-4/analyser_traces_j5.py` lit uniquement ces fichiers. Il prend en charge ce format PCAP Ethernet/IPv4/TCP avec un ADU complet par paquet ; il ne remplace pas un analyseur général avec réassemblage TCP.

## 2 — Analyser les communications Modbus dans Wireshark

Ouvrir `modbus_REG02_capture.pcap` depuis le dossier original ou une copie de l’archive. Pour les heures, choisir un affichage absolu via **View → Time Display Format**, puis vérifier le fuseau effectivement affiché : **09:14 CEST = 07:14 UTC**. Le format relatif « secondes depuis le premier paquet » ne suffit pas à corréler directement les CSV. [Wireshark — affichage des temps](https://www.wireshark.org/docs/wsug_html_chunked/ChWorkTimeFormatsSection.html).

Filtre du régulateur et des écritures :

```wireshark
ip.addr == 10.30.10.22 && tcp.port == 502
```

```wireshark
modbus.func_code == 6
```

Pour ne conserver que les requêtes d’écriture :

```wireshark
ip.dst == 10.30.10.22 && tcp.dstport == 502 && modbus.func_code == 6
```

Ces champs sont documentés dans la [référence officielle des filtres Modbus](https://www.wireshark.org/docs/dfref/m/modbus.html). Le port est ici **502**, pas 15020 ou 15021 du PoC J4. Si le décodage manque, vérifier l’association du trafic TCP à Modbus/TCP.

### Clients et fonctions effectivement présents

- **SUP-01 `10.30.20.10`** : six requêtes FC03 ; ports source 40310 à 40315, selon les échanges.
- **MAINT-01 `10.30.20.15`** : trois requêtes FC06 ; ports source 41001, 41002 et 41004.
- **REG-02 `10.30.10.22:502`** : réponses correspondantes, unité Modbus **1**.
- **Consultation `10.30.20.30`** : adresse documentée mais absente de cet échantillon. Cette absence ne prouve pas qu’elle n’a jamais communiqué.

### Les trois écritures à examiner en priorité

| Heure locale du 8 octobre | Requête / réponse | Transaction MBAP | Opération et réponse |
| --- | --- | --- | --- |
| 08:46:00 / 08:46:00,030 | **3 / 4** ; MAINT-01:41001 ↔ REG-02:502 | **2** | FC06, PDU **0**, valeur **40** (`0x0028`) = **4 °C** ; réponse normale avec même adresse et valeur. Réécriture sans changement selon les journaux. |
| 09:14:00 / 09:14:00,030 | **9 / 10** ; MAINT-01:41002 ↔ REG-02:502 | **5** | FC06, PDU **0**, valeur **120** (`0x0078`) = **12 °C** ; réponse normale identique, sans exception. |
| 10:21:00 / 10:21:00,030 | **15 / 16** ; MAINT-01:41004 ↔ REG-02:502 | **9** | FC06, PDU **0**, valeur **40** = **4 °C** ; réponse normale identique. |

Chaque réponse arrive **30 ms** après sa requête dans cette trace. L’association utilise transaction, unité et extrémités TCP ; un simple ACK TCP n’aurait pas suffi à prouver l’acceptation Modbus. Ici les FC06 sont correctement appariées, et les exports SUP/mesures corroborent les valeurs de consigne.

Filtre pour préparer une capture des écritures :

```wireshark
frame.number in {3,4,9,10,15,16}
```

### Lectures : valeurs visibles et anomalie du jeu synthétique

| Heure locale | Trames / transaction | Valeur encodée dans la réponse FC03 |
| --- | --- | --- |
| 08:40 | 1/2 ; 1 | 40 = 4 °C |
| 08:47 | 5/6 ; 3 | 40 = 4 °C |
| 09:11 | 7/8 ; 4 | 40 = 4 °C |
| 09:15 | 11/12 ; 6 | 120 = 12 °C |
| 09:47 | 13/14 ; 8 | 120 = 12 °C |
| 10:22 | 17/18 ; 10 | 40 = 4 °C |

**Limite vérifiée dans les octets :** les requêtes FC03 portent l’adresse PDU 0 puis une quantité **40** (`00 28`), ou **120** (`00 78`) aux trames 11 et 13. Les réponses annoncent **2 octets**, soit un seul registre. La quantité demandée en FC03 n’est pas une valeur de consigne ; une réponse normale de lecture doit correspondre à la quantité demandée. Ces six paires sont donc incohérentes comme transactions de lecture complète.

Conserver les valeurs encodées comme indices corroborés par les autres sources, **sans présenter les six lectures comme des échanges conformes**. Signaler cette limite au formateur ; ne pas modifier le PCAP original pour le rendre cohérent. Les trois FC06 et leurs échos ne présentent pas cette incohérence de quantité.

### Comparaison avec la politique J4 proposée

| Chemin observé | Comparaison avec J4 | Conclusion limitée |
| --- | --- | --- |
| SUP-01 → REG-02 direct | La cible J4 remplace R10 pour REG-02 par Q10/Q11 via GW-02-LECT. | Le chemin capturé diffère de cette cible ; pas de preuve que GW-02 avait été installé. |
| MAINT-01 → REG-02 direct, FC06 | La cible prévoit entrée contrôlée, bastion et GW-02-MAINT temporaire, source aval GW-02 seule. | Chemin et contrôle applicatif à confirmer dans l’état réellement en service. L’échantillon ne révèle pas l’architecture complète. |
| Session partagée au-delà de l’intervention planifiée | FM-426 porte une autorisation 08:30–09:00 ; session suivante 09:12–09:19. | La seconde session n’est pas justifiée par cette fenêtre. Une autre autorisation éventuelle reste à rechercher. |

## 3 — Corréler les heures et la température

**Référence retenue :** heure locale du scénario, **UTC+02:00** le 8 octobre 2026. Les heures UTC brutes du PCAP et les heures VPN brutes restent conservées dans les CSV dérivés.

| Session | VPN brut | Référence SUP après −00:02:10 | Compte / source et contexte |
| --- | --- | --- | --- |
| Première | 08:41:10–08:54:10 | **08:39–08:52** | maint-shared / 198.51.100.44 ; FM-426 déclaré. |
| Deuxième | 09:14:10–09:21:10 | **09:12–09:19** | maint-shared / 203.30.113.77 ; ticket non fourni dans le journal VPN. |
| Corrective | 10:21:10–10:28:10 | **10:19–10:26** | maint-oncall / 198.51.100.51 ; INC-881. |

L’écriture à 09:14 se situe dans la deuxième plage ; celle de 10:21 dans la plage corrective. C’est une corrélation temporelle et de destination, **pas une chaîne d’attribution humaine complète**. Les IP publiques sont recopiées telles quelles, sans déduction géographique ni recherche de propriétaire.

![Évolution des températures et de la consigne de ZF-02](../../assets/files/informatique-industrielle/it-4/Montval-5.2-evolution-ZF02.svg)

L’export passe de **4 à 12 °C de consigne à 09:14** ; la commande compresseur est à 0 jusqu’au retour à 4 °C à **10:21**, où elle passe à 1. La hausse puis la baisse observées sont cohérentes avec l’effet de cette modification dans le scénario, sans exclure d’autres facteurs physiques.

Premier échantillon strictement supérieur à 8 °C : **09:42, 8,13 °C** ; alarme active à **09:52, 9,55 °C**. Cette différence est cohérente avec les **10 minutes** du manuel, à la précision de l’export : l’instant exact de franchissement entre mesures n’est pas connu. Le PoC accéléré utilise 10 secondes, qui ne s’appliquent pas à cet historique.

Le premier maximum enregistré est **11,55 °C à 10:07**. À **10:45**, l’export indique 8,00 °C avec alarme encore active ; à **10:46**, 7,85 °C et alarme inactive, conformément à l’événement SUP. La règle exacte d’effacement n’est pas décrite : ne pas en inventer une. Dernière mesure fournie à **11:30 : 4,18 °C**. La température des produits et leur conformité restent hors de ce que cet export établit.

## 4 — Chronologie documentée

[Tableau complet téléchargeable CSV](../../assets/files/informatique-industrielle/it-4/Montval-5.2-chronologie.csv). Toutes les heures suivantes sont locales au **8 octobre 2026**. Les numéros de ligne CSV incluent l’en-tête.

| Heure | Événement | Source | Fait établi ou limite |
| --- | --- | --- | --- |
| 08:22 | FM-426 ouvert ; lecture paramètres autorisée 08:30–09:00 | maintenance ligne 2 | Autorisation consignée |
| 08:39–08:52 | Session maint-shared ; source 198.51.100.44 | VPN lignes 2–3 corrigées ; maintenance lignes 3–5 | Session enregistrée ; identité humaine déclarée dans ticket |
| 08:46:00 | FC06 PDU 0 = 40, réponse normale ; réécriture à 4 °C | PCAP 3/4 ; maintenance ligne 4 ; SUP ligne 3 | Échange établi dans la trace ; portée exacte de l’autorisation à confirmer |
| 09:11:00 | Réponse FC03 contenant 40 (4 °C) | PCAP 7/8 | Valeur encodée ; incohérence quantité FC03 |
| 09:12–09:19 | Session maint-shared ; source 203.30.113.77, ticket non fourni | VPN lignes 4–5 corrigées | Session enregistrée ; auteur et autorisation non établis |
| 09:14:00 | MAINT-01 écrit PDU 0 = 120 ; réponse identique +30 ms | PCAP 9/10 ; SUP ligne 4 ; mesures ligne 46 | Modification confirmée par sources du scénario |
| 09:15:00 | Réponse de lecture SUP contenant 120 | PCAP 11/12 | Corroboration de valeur ; incohérence quantité FC03 |
| 09:42 | Premier échantillon > 8 °C : 8,13 °C | Mesures ligne 74 | Premier échantillon disponible ; instant exact de franchissement inconnu |
| 09:45 | 8,55 °C et régulation locale déclarée active | SUP ligne 5 ; mesures ligne 77 | Valeur et événement enregistrés |
| 09:50 | INC-881 ouvert pour anomalie de température | Maintenance ligne 6 | Signalement consigné |
| 09:52 | Alarme haute active ; mesure 9,55 °C | SUP ligne 6 ; mesures ligne 84 | Déclenchement enregistré, cohérent avec 10 minutes depuis premier échantillon haut |
| 10:04 | Acquittement OPS-01 et sollicitation IT | SUP ligne 7 ; mission | Prise en compte, pas correction de consigne |
| 10:07 | Premier maximum enregistré : 11,55 °C | Mesures ligne 99 | Mesure d’enceinte ; pas température produit |
| 10:11 | FrigoMaint ne déclare pas de changement à 12 °C | Maintenance ligne 7 | Déclaration à confronter aux traces |
| 10:18 | Retour à 4 °C autorisé, contrôle sur place requis | Maintenance ligne 8 | Autorisation consignée |
| 10:19–10:26 | Session maint-oncall ; source 198.51.100.51 | VPN lignes 6–7 corrigées | Session enregistrée, correspondance INC-881 |
| 10:21:00 | MAINT-01 écrit 40 ; réponse normale +30 ms ; commande compresseur = 1 | PCAP 15/16 ; SUP ligne 8 ; maintenance ligne 9 ; mesures ligne 113 | Retour à 4 °C confirmé dans sources ; contrôle terrain à vérifier |
| 10:22:00 | Réponse de lecture SUP contenant 40 | PCAP 17/18 | Valeur encodée ; incohérence quantité FC03 |
| 10:45 | Mesure 8,00 °C ; alarme encore active dans export | Mesures ligne 137 | Observation ; règle de disparition non détaillée |
| 10:46 | Alarme effacée ; mesure 7,85 °C | SUP ligne 9 ; mesures ligne 138 | Fin d’alarme enregistrée ; pas décision de conformité des produits |
| 11:15 | Mesures en baisse et consigne à 4 °C | SUP ligne 10 | Suivi enregistré |
| 11:30 | Dernière mesure disponible : 4,18 °C | Mesures ligne 182 | Fin de l’export, pas fin de toute investigation |


Les fenêtres de session ne prouvent pas l’identité de la personne au clavier. Les événements de ticket sont des déclarations consignées ; les paquets prouvent des échanges techniques dans cette trace synthétique. Aucun horodatage n’est déplacé pour faire coïncider artificiellement les sources.

## 5 — Premier diagnostic à présenter au formateur

| Question | Réponse provisoire et niveau de preuve |
| --- | --- |
| Modification confirmée ? | **Oui dans le dossier fictif** : FC06 9/10, PDU 0 = 120, réponse normale, journal SUP et consigne exportée à 12 °C. Les réponses de lecture contiennent ensuite 120, avec la réserve de quantité FC03. |
| Système émetteur identifié ? | **Origine technique observée : MAINT-01, 10.30.20.15:41002**, destination REG-02:502. Pas d’identification de la personne, du processus local ou de la machine d’origine au-delà de ce point de capture. |
| Action non autorisée démontrée ? | **Autorisation non retrouvée dans les pièces reçues.** La modification est hors fenêtre FM-426 et contredite par les déclarations disponibles. Cela constitue un fort écart de justification ; l’absence de toute autorisation et une intention malveillante ne sont pas démontrées de façon exhaustive. |
| Autres explications ? | Erreur de saisie ou d’outil, automatisation ou essai mal maîtrisé, usage d’un compte partagé hors procédure, autorisation non transmise, compromission du poste ou du compte. Les éléments fournis ne départagent pas ces causes. |
| Informations manquantes ? | Sessions/utilisateurs/processus sur MAINT-01 ; authentification détaillée et affectation du compte partagé ; demandes et autorisations complètes ; topologie et règles réellement actives ; journaux du REG si disponibles ; exhaustivité des captures et contrôle indépendant du processus et des produits. |

**Synthèse orale proposée :** une écriture de consigne de 4 à 12 °C depuis MAINT-01 est confirmée à 09:14 dans les sources synthétiques. Elle se situe dans une session VPN corrigée à 09:12–09:19, hors de l’autorisation FM-426 connue. La température augmente, l’alarme apparaît à 09:52 et est acquittée à 10:04. Le retour autorisé à 4 °C est documenté à 10:21, suivi d’une baisse. L’auteur humain, l’intention et l’exhaustivité des autorisations restent à établir ; le PCAP comporte une incohérence FC03 à signaler.

## Captures utilisateur du 30 octobre — analyse et affichage Wireshark

Les huit images sont conservées dans `assets/img/informatique-industrielle/it-5/`, selon le classement utilisateur par journée. Elles documentent **J5 / itération 4** du mémo ; aucune nouvelle itération n’est créée. Elles sont complémentaires et toutes utilisées.

### 09:30:02 — Exécution locale et lecture des paquets en UTC

![Exécution du script et affichage tcpdump du PCAP en UTC](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2009-30-02.png)

La commande du script et sa sortie sont visibles : **18 trames**, clients **10.30.20.10 / 10.30.20.15**, fonctions **3 et 6**, **six lectures incohérentes** et **181 mesures**. Le premier maximum ressort à **11,55 °C à 10:07**, le premier échantillon > 8 °C à **09:42, 8,13 °C**. Le SHA-256 affiché correspond au PCAP analysé. La commande `TZ=UTC tcpdump` affiche notamment l’écriture et sa réponse à **07:14:00 / 07:14:00,030 UTC**, soit **09:14 CEST**. Cette capture atteste l’exécution de l’analyse par l’utilisateur ; elle ne montre pas une action sur le régulateur réel.

### 09:31:26 et 09:31:34 — Détails des trames 4 et 3

![Trame 4, sens REG-02 vers MAINT-01 et fonction 6](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2009-31-26.png)

![Trame 3, sens MAINT-01 vers REG-02 et fonction 6](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2009-31-34.png)

La **trame 3** montre MAINT-01 **10.30.20.15:41001 → REG-02 10.30.10.22:502** ; la **trame 4** présente le sens inverse. Transaction **2**, protocole **0**, longueur MBAP **6**, unité **1**, fonction **6**, bit d’exception **No**. Il s’agit de la paire de **08:46**, et non de la modification à 12 °C de 09:14. Les champs adresse/valeur du registre ne sont pas détaillés dans ces vues : la valeur **40** demeure établie par le décodage du fichier source.

Les deux images affichent **« Cannot classify packet type »**. Wireshark reconnaît MBAP et le code de fonction, mais ne classe pas automatiquement requête/réponse dans cet affichage. Cet avertissement n’est ni une exception Modbus du régulateur ni une preuve d’attaque. Son origine exacte n’est pas établie par les captures. Vérifier la préférence de port Modbus/TCP pour **502** dans le profil actif avant de reprendre les détails, sans modifier le PCAP original. Cette difficulté de classification est distincte de l’incohérence de quantité des FC03 vérifiée dans les octets.

### 09:32:13 — Vue d’ensemble des 18 trames

![Liste des 18 trames Modbus et avertissements de classification](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2009-32-13.png)

La vue confirme la présence des paires **3/4**, **9/10**, **15/16** en FC06 et des échanges FC03, avec les deux origines techniques documentées. La colonne Time est **relative au premier paquet** : les trames 9/10 sont à **2040 / 2040,03 secondes**, soit 34 minutes après le premier paquet de 08:40. Cette colonne ne se lit pas comme une heure absolue. Les indications `unknown` et `Unable to classify as query or response` restent visibles ; l’appariement décrit dans cette fiche repose aussi sur les extrémités et les octets analysés hors ligne.

### 09:34:18 et 09:34:25 — Paire 9/10, écriture de la transaction 5

![Trame 9, MAINT-01 vers REG-02, transaction 5 fonction 6](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2009-34-18.png)

![Trame 10, REG-02 vers MAINT-01, transaction 5 fonction 6](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2009-34-25.png)

La trame **9** montre **10.30.20.15:41002 → 10.30.10.22:502** ; la trame **10** montre le retour **502 → 41002**. Les deux vues affichent transaction **5**, protocole **0**, longueur **6**, unité **1**, fonction **6** et **Exception: No**. Elles complètent la preuve visuelle du sens des échanges et de la fonction utilisée à **09:14**, selon les horodatages du PCAP déjà décodés. Les heures absolues ne sont pas ouvertes dans ces images.

**Limite visuelle :** l’avertissement de classification subsiste et les champs adresse/valeur ne sont pas affichés. L’écriture **PDU 0 = 120**, et l’écho correspondant, restent confirmés par les octets du fichier : fin de l’ADU `01 06 00 00 00 78` (unité, fonction, adresse, valeur). Ne pas attribuer la lecture visuelle de « 120 » à ces captures.

### 09:34:32 et 09:34:37 — Paire 15/16, retour de la transaction 9

![Trame 15, MAINT-01 vers REG-02, transaction 9 fonction 6](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2009-34-32.png)

![Trame 16, REG-02 vers MAINT-01, transaction 9 fonction 6](../../assets/img/informatique-industrielle/it-5/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-30%2009-34-37.png)

La trame **15** montre **10.30.20.15:41004 → 10.30.10.22:502** ; la **16** montre le retour **502 → 41004**. Transaction **9**, protocole **0**, longueur **6**, unité **1**, fonction **6**, **Exception: No** : ces vues correspondent au retour à **4 °C à 10:21**, horodaté dans le fichier source. L’avertissement de classification est encore présent.

La valeur **40** et l’adresse **0** ne sont pas visibles dans les champs affichés ; le décodage de la fin de l’ADU `01 06 00 00 00 28` confirme ces données et leur écho. Les captures et le décodage hors ligne sont donc complémentaires ; aucune attribution humaine supplémentaire n’est obtenue.

## Preuves à conserver et reproduction de l’analyse

Depuis la racine du mémo, commandes **hors ligne**, sans sudo ni modification du laboratoire :

```bash
python3 livrables/informatique-industrielle/it-4/analyser_traces_j5.py
TZ=UTC tcpdump -nn -tttt -r livrables/informatique-industrielle/it-4/Incident_dossier/modbus_REG02_capture.pcap
```

Le script régénère les CSV, le JSON et la figure depuis les originaux ; les heures locales utilisent explicitement `Europe/Paris`. Le relevé tcpdump ne remplace pas le décodage des fonctions et valeurs Modbus.

Les détails des trames **9/10** et **15/16** sont maintenant intégrés. Pour montrer aussi les valeurs dans une vue Wireshark, compléter éventuellement avec le volet des octets (fins `00 78` et `00 28`) et les heures absolues, ou un décodage détaillé après résolution de l’avertissement. La paire **11/12** peut illustrer la réserve FC03. Les données sont déjà établies dans le CSV de décodage ; ces compléments visuels ne sont pas déclarés réalisés.

Empreinte SHA-256 du PCAP original :

```text
7881738323e12ab626e6d2f6d37f1dd6498b8335b62de461d8e0db0ea2acf97e
```

[Retour à l’itération 4](index.md) · [Prise de connaissance 5.1](prendre-connaissance-incident.md) · [Politique proposée J4](../it-3/definir-acces-regles-pare-feu.md).
