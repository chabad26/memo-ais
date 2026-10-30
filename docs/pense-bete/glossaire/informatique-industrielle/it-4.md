# Pense-bête — Informatique industrielle — Itération 4 / J5

[Sommaire J5](../../../informatique-industrielle/it-4/index.md) · [5.1 — Prendre connaissance de l’incident](../../../informatique-industrielle/it-4/prendre-connaissance-incident.md).

## Premiers repères

- Scénario fictif : ZF-02 / REG-02, événements du **8 octobre 2026** ; analyse documentaire du **30 octobre**.
- Dossier source : `livrables/informatique-industrielle/it-4/Incident_dossier/`, sept fichiers conservés ; [archive et inventaire](../../../informatique-industrielle/it-4/prendre-connaissance-incident.md#2-inventaire-des-sources-recues).
- Horloge VPN **+2 min 10 s** : soustraire ce décalage, garder brut et corrigé. PCAP en UTC, heures SUP en CEST UTC+02:00.
- REG-02 `10.30.10.22:502` ; MAINT-01 `.20.15`, SUP-01 `.20.10`, consultation `.20.30` dans le préfixe `10.30`. Aucun rapport avec les adresses `10.77.*` du PoC.
- PDU 0 = consigne en dixièmes : 40 = 4 °C, 120 = 12 °C ; FC03 lecture, FC06 écriture.
- Alarme du manuel : **> 8 °C pendant 10 min** ; PoC accéléré : **10 s**. Acquitter ne rétablit pas la température.

## Preuves et prudence d’attribution

Le journal de supervision indique la modification à 12 °C ; l’analyse du PCAP, préparée en 5.1, est désormais réalisée en 5.2. Les tickets rapportent une autorisation à 10:18 et un retour à 4 °C à 10:21 : vérifier ce qui a déjà été fait avant de proposer de le refaire.

Une IP, un compte partagé, une session VPN ou l’absence de ticket reçu ne suffisent pas à désigner une personne ni une attaque. Séparer trace technique, déclaration, hypothèse et inconnu. Température d’enceinte ≠ température produit ; l’exploitation décide du devenir des denrées selon ses procédures.

REG-02 sans correctif disponible : pas d’exploitation de CVE présumée. Architecture J4 proposée ≠ protections présentes le jour des faits. Ne pas réinitialiser le laboratoire ni interrompre le contrôle local pour cette prise de connaissance.

## 5.2 — Chronologie et diagnostic provisoire

[Analyse 5.2](../../../informatique-industrielle/it-4/analyser-traces-reconstituer-evenements.md) : PCAP décodé hors ligne, 18 trames, deux clients (SUP-01 / MAINT-01), fonctions 03 et 06.

- Écritures FC06 : **3/4** à 08:46 = 40 ; **9/10** à 09:14 = 120 ; **15/16** à 10:21 = 40. PDU 0, transaction 2/5/9, réponses normales à +30 ms.
- VPN corrigé : **08:39–08:52**, **09:12–09:19**, **10:19–10:26**. Session partagée et proximité temporelle ne prouvent pas une identité humaine.
- Six lectures FC03 incohérentes : demande de 40 ou 120 registres, réponse contenant un seul registre. Valeurs visibles à corroborer, ne pas présenter ces transactions comme conformes.
- Premier échantillon > 8 °C : 09:42 ; alarme 09:52 ; acquittement 10:04 ; retour consigne 4 °C 10:21 ; alarme effacée 10:46. Maximum enregistré 11,55 °C (premier à 10:07).
- Modification confirmée ; autorisation absente des pièces pour 09:14, hors FM-426 connu. Auteur, intention, processus et éventuelles pièces manquantes à établir.
- CSV chronologique, VPN normalisé, décodage, JSON et figure téléchargeables ; aucune nouvelle exécution PoC. Huit captures utilisateur attestent désormais l’analyse locale et les vues Wireshark : liste des 18 trames, détails 3/4, 9/10 et 15/16. Avertissement de classification persistant ; adresse/valeur non affichées dans ces images. Les octets du PCAP confirment PDU 0 = 120 (00 78), puis 40 (00 28).

## 5.3 — Premières actions de réponse

[Fiche 5.3 et matrice téléchargeable](../../../informatique-industrielle/it-4/determiner-premieres-actions-reponse.md) : huit actions évaluées et réponse proposée, non exécutée.

- Exploitation/FrigoMaint vérifient le froid et les produits ; IT conserve les traces et propose le confinement ciblé.
- Retour à 4 °C déjà documenté à 10:21 : vérifier l’état actuel avant toute nouvelle écriture.
- Suspendre un accès ne clôt pas automatiquement toutes ses sessions ; vérifier VPN, poste et connexions utiles, sans supprimer globalement les flux légitimes.
- Pas de redémarrage REG-02 par défaut ; maintien local dépend des composants réels. Perdre la supervision peut masquer une nouvelle anomalie.
- Préserver les preuves en parallèle, sans retarder une action urgente décidée par les responsables du processus.
- Accès prestataire urgent : intervention sur place ou moyen de confiance autorisé, durée/cibles/opérations bornées, puis fermeture vérifiée.
- Aucune attribution humaine, acceptation collective, décision sur les produits ni nouvelle action technique déclarée réalisée.

## 5.4 — Reproduction sur le PoC, preuves partielles

[Fiche 5.4](../../../informatique-industrielle/it-4/reproduire-incident-jumeau-numerique.md) : vérifier les namespaces J4 ; documentation Docker 172.30.* = montage distinct.

- Écriture pédagogique : **ais45-gw → 10.77.30.2:15020**, `setpoint 12`, puis **setpoint 4** avant de terminer.
- Consultation et refus d’écriture : **ais45-it → 10.77.20.2:15021** ; écrire 6 doit produire exception 01 sans modifier 12.
- IT direct reste interdit, sans ouverture ni réinitialisation du filtre.
- Même origine GW pour lecture et écriture directe : pas d’identité de maintenance ni de bastion déployé démontrés.
- Température progressive ; alarme > 8 °C pendant 10 s dans le PoC, 10 min dans le dossier ; pas de redémarrage du serveur pour simuler une récupération.
- Nouveau dossier de preuves daté ; capture fw-ot pour les écritures autorisées. Au dépôt des fichiers : état final 4,4 °C, consigne 4 °C, compresseur 1, alarme/porte/défaut 0, auto 1 ; repère fin 10:26:43+01:00. Filtre exporté, compteur direct 12. Ancien PCAP vide conservé dans son archive. **Nouveau PCAP : 130 trames**, 10:32:53–10:33:17 ; lectures FC03/04/01 et écriture FC06 **94/96**, PDU 0 = 40 acceptée, relecture **104/106**. Consigne déjà 4 °C au début : réécriture, pas preuve du passage 12 → 4. Aucune consigne 12 °C, alarme haute ou exception proxy dans cette fenêtre. Archives et empreintes distinctes, suivi continu de reproduction encore manquant.


### Nouvel essai complet — 10:39 à 11:00

PCAP **2 630 trames / 263 transactions** : écriture 12 °C **274/276**, relecture **286** ; alarme observée à 8,2 °C **1136** ; température 12 °C **2066** ; correction 4 °C **2084/2086**, relecture **2096** ; maximum 12,1 °C et compresseur actif **2106**, alarme éteinte à 7,7 °C **2346**, final 3,8 °C **2616**. États finaux : consigne 4, porte/défaut/alarme 0, auto 1, compresseur 1 compatible avec hystérésis.

La capture longue complète désormais la preuve de montée/alarme/restauration ; les réserves « 12 °C non capturé » ci-dessus décrivent seulement les lots précédents. API HTTP, refus IT/proxy et cycle complet après correction restent hors de cette nouvelle capture aval. Archives et horodatages sont conservés séparément.


### 24 captures ajoutées — preuves des deux essais

- Premier essai 10:14–10:20 : recréation et contrôles automatiques, namespaces/interfaces/règles/écoutes ; état nominal et **API 200** avant modification ; écriture **12 °C** acceptée à 10:16:28 ; refus direct **compteur 3 → 6** ; refus proxy **exception 01** et consigne 12 inchangée ; état de retour 6,2 °C/consigne 4, avec exports échoués par droits.
- Second essai : douze vues Wireshark montrent les valeurs et associations des trames **274/276, 286, 1136, 2066, 2084/2086, 2096, 2106, 2346, 2616**, plus la liste filtrée. Les captures d’écran sont datées 11:05–11:06, les paquets de 10:39–11:00.
- Ces captures complètent désormais les refus IT/proxy et l’API avant le premier essai, absents du seul PCAP long. API après restauration du second essai et cycle complet restent non fournis. Le bilan tcpdump **250 paquets** d’une autre collecte n’est attribué à aucun PCAP reçu sans correspondance établie.


## 5.5 — C01 appliquée, recette partiellement documentée

[Fiche 5.5](../../../informatique-industrielle/it-4/choisir-valider-mesures-correctives.md) : C01 = journaliser les tentatives IT directes avec NFLOG groupe 55, compteur intégral et logs limités ; table **inet ais55_trace** dans **ais45-fw**, priorité −5, table J4 conservée.

- Ajouter uniquement dans le pare-feu isolé après `nft -c` ; collecteur `tcpdump -i nflog:55` à démarrer avant le test. Collecte désormais prouvée : PCAP NFLOG de trois SYN, 624 octets, 12:33:22–12:33:24 ; compteur C01 0 → 3. Le taux de logs sous charge n’a pas été testé.
- Nouveau compteur **ais55_trace/it_ot_refus** : le refus a lieu avant la règle J4, dont le compteur peut rester stable. Le vérificateur J4 peut donc échouer à son ancien contrôle de delta : utiliser la recette C01 et documenter l’écart.
- Drop inconditionnel après limitation des logs ; débit de journalisation limité ≠ débit de refus limité. Les autres flux passent ensuite dans la politique DROP J4.
- Tester lecture, exception proxy, API, contrôle local et réécriture nominale 4 depuis GW ; ne pas rejouer 12 pour cette recette.
- Retour arrière : supprimer **seulement inet ais55_trace** dans le namespace ; conserver la table ais45 et refaire les tests.
- C01 améliore les traces mais ne bloque pas le GW autorisé à écrire. Séparation collecte/maintenance, droits et contrôle des valeurs à qualifier ; REG-02 reste obsolète et non corrigé.


### Preuves reçues pour 5.5

Cinq captures : tables ais55_trace + ais45, timeout IT direct/counter 0 → 3, NFLOG lisible, lecture proxy et exception 01/consigne conservée, réécriture 4 depuis GW acceptée, API HTTP200. NFLOG brut récupéré en lecture seule et archivé avec empreinte.

**Le dossier fourni j5-54-20261030T091556Z contient encore les anciens fin/état/règles de 10:26**, pas les exports finaux après C01. La source C01 y est identique au fichier préparé. **Nouvel export regles-apres-c01.nft désormais reçu** : tables ais45 et ais55_trace, compteur C01 3 paquets/180 octets, règles et retours J4 conservés. Export sans date interne, distinct de fin.txt 10:26. Suivi continu du contrôle local et retour arrière restent non fournis ; la preuve de configuration appliquée est maintenant complète pour ces deux tables.


## 5.6 — Retour maîtrisé : périmètre technique et décision d’exploitation

[Fiche 5.6 et liste de contrôle](../../../informatique-industrielle/it-4/verifier-retour-fonctionnement-maitrise.md) : dix contrôles, statut laboratoire, preuves et vérifications nécessaires sur Montval.

- Preuves : correction 4 °C, baisse 12,1 → 3,8 °C, alarme éteinte ; C01 appliquée, NFLOG et règles exportées, lectures/API utiles maintenues dans les fenêtres observées.
- Réserves : contrôle local continu après C01, cycle complet, retour arrière, accès nominatif et persistance non validés ; origine GW peut encore écrire.
- Scénario du 8 octobre : 181 mesures à la minute ; **63 échantillons > 8 °C de 09:42 à 10:44**, extrémités séparées de 62 min. Pas une durée exacte d’exposition des produits ; 4 → 12 → 4 de consigne et alarme sont des repères distincts.
- Qualité CSV OK déclarée ≠ capteur indépendant étalonné. Mesures d’enceinte ≠ température produit ; pas de donnée hors 08:30–11:30.
- L’AIS transmet chronologie, incertitudes, mesures/actions, preuves et réserves. Exploitation/maintenance et acteurs qualité selon procédure valident la réalité terrain et le devenir des lots.
- Aucun accord de reprise normale, signature, clôture d’incident ou décision sanitaire inventés. REX : préservation des preuves, séparation des accès, collecte pérenne et remplacement REG-02 à préparer.


## 5.7 — Compte-rendu C5 prêt pour restitution

[Document unique J5-investigation-remediation-OT](../../../informatique-industrielle/it-4/finaliser-compte-rendu-investigation-remediation.md) : sept parties, chronologie, analyse, décisions, C01, tests et limites ; PDF pour la formatrice et archive Markdown/PDF avec annexes et empreintes.

- Trois périmètres séparés : scénario fictif du 8 octobre, reproduction PoC du 30 octobre et recette C01.
- Écriture12 et retour4 confirmés ; pas d’auteur humain ou intention attribués. Une absence de justificatif reçu n’est pas une preuve exhaustive d’absence d’autorisation.
- C01 appliquée et collectée ; ne corrige ni REG-02 ni le droit d’écriture de GW. Cycles complets après C01 et retour arrière non attestés.
- Aucune décision sur les produits, reprise opérationnelle Montval, signature ou validation du formateur inventée.
- Convention fournie Iteration3-Atelier7 ; classement mémo itération4/J5 ; site à compléter, pas inventé.
