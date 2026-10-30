# 5.6 — Atelier 6 | Vérifier le retour à un fonctionnement maîtrisé

## 🎯 Objectif et modalités

Définir les vérifications techniques après un incident et identifier les limites de la validation sur un environnement simulé.

**Modalité :** analyse et restitution en binôme. **Durée :** à compléter, non précisée.

!!! info "Synthèse des preuves disponibles au 30 octobre 2026"
    Cette fiche réutilise les sources du scénario, les deux essais PoC et la recette partielle C01. **Aucun nouveau test ni accord de remise en service n’est exécuté ou obtenu pour la rédiger.** Les résultats de laboratoire, les contrôles à réaliser sur Montval et les décisions de l’exploitation restent séparés.

## 1 — Liste de contrôle du retour technique

[Liste de contrôle téléchargeable — CSV](../../assets/files/informatique-industrielle/it-4/Montval-5.6-liste-controle.csv).

**Attesté** signifie observé dans le périmètre et à l’instant indiqués, pas garanti pour toute la journée ou l’installation réelle. **Partiel** signale une preuve utile avec un contrôle manquant. Le classement n’est pas une décision de certification.

| Contrôle | Fonction | État du laboratoire | Preuves disponibles | Contrôles nécessaires Montval | Acteurs |
| --- | --- | --- | --- | --- | --- |
| R01 | Régulation locale | Partiel | PCAP long : température, commande et retour 12,1 vers 3,8 °C ; après C01 états ponctuels sans défaut | Notice, contrôle indépendant sonde/groupe, alimentation, E/S et cycles ; preuve terrain et autonomie aux pannes | FrigoMaint/automaticien + exploitation |
| R02 | Consignes et modes | Attesté dans les fenêtres observées | FC06 274/276 = 120 puis 2084/2086 = 40 ; relecture 4 ; après C01 consigne 4 et auto 1 | Paramètres locaux actuels, autorisations et absence de changement ultérieur inexpliqué | Exploitation + FrigoMaint ; IT fournit traces |
| R03 | Alarmes | Partiel | PoC : alarme active à 8,2 °C et inactive à 7,7 °C ; pas de nouvelle recette complète après C01 | Temporisation réelle 10 minutes, signal local/OPS, acquittement, défauts et perte de communication | FrigoMaint + responsable SUP + exploitation |
| R04 | Supervision | Attesté pour API du TP | Après C01 HTTP 200, consigne 4/température 4,5/compresseur actif ; pas preuve graphique | Fraîcheur/horodatage, périmée, trois zones, OPS-01 et reprise sans modification de consigne | Responsable SUP + IT + exploitation |
| R05 | Communications nécessaires | Attesté pour les chemins testés | IT via proxy lit ; IT direct timeout, compteur C01 0→3, NFLOG trois SYN | Matrice réelle complète, chemins latéraux/locaux et autres protocoles ; pas seulement le plan J4 proposé | IT réseau + FrigoMaint + exploitation |
| R06 | Maintenance autorisée | Partiel | GW direct peut réécrire4 ; proxy refuse6 avec exception01 | Identité, bastion/accès réel, périmètre/durée, urgence et fermeture des sessions | IT accès + FrigoMaint + exploitation |
| R07 | Configuration appliquée | Attesté par export reçu | Export regles-apres-c01.nft : ais45 DROP et ais55_trace priorité-5/NFLOG/drop, compteur3/180 | Persistance après redémarrage et cohérence du déploiement réel ; associer date aux futurs exports | IT réseau + exploitation |
| R08 | Journaux et données utiles | Partiel | Sources, empreintes, archives et PCAP NFLOG récupéré ; anciens exports distingués | Collecte durable, droits, rétention 90 jours prévue, complétude hors fenêtre, horloges et sauvegarde/restauration | IT + responsable SUP + FrigoMaint |
| R09 | Reprise et retour arrière | Non validé intégralement | J4 : coupure et reprise du lien ; C01 : procédure de retrait préparée mais non exécutée | Scénario de panne/reprise de protection, retour arrière C01, collecte et froid sous contrôle | IT + FrigoMaint + exploitation |
| R10 | Conséquences sur les produits | Hors périmètre de validation IT | Mesures enceinte uniquement ; aucun produit simulé ni lot évalué | Lots, exposition et mesures indépendantes, procédures magasin, décision et autorité de remise en service | Responsable exploitation avec acteurs qualité/maintenance désignés |

### Preuves de référence et fenêtres distinctes

| Ensemble | Résultats à retenir | Ce qu’il ne faut pas en déduire |
| --- | --- | --- |
| Incident fictif du **8 octobre**, analysé en [5.2](analyser-traces-reconstituer-evenements.md) | Modification à 12 °C depuis MAINT-01, alarme, acquittement puis retour à 4 °C documentés ; VPN normalisé −2 min 10 s. | Auteur humain, intention, identité des produits ou conformité ; PCAP synthétique partiel et lectures FC03 incohérentes. |
| Premier essai du **30 octobre, 10:14–10:20**, captures [5.4](reproduire-incident-jumeau-numerique.md#captures-utilisateur-24-preuves-visuelles-complementaires) | Namespaces et services, API, refus IT direct compteur 3 → 6, refus proxy et maintien consigne 12. | Une séquence continue avec le PCAP long ; les exports ont d’abord échoué par droits. |
| Second essai **10:39–11:00**, [PCAP long](../../assets/files/informatique-industrielle/it-4/Montval-5.4-reproduction-complete.pcap) | Écriture 12 **274/276**, relecture 286, alarme 1136, écriture 4 **2084/2086**, relecture 2096, maximum 12,1 °C (trame 2106) puis 3,8 °C (trame 2616), alarme 0. | Température produit, seuil réel ou temporisation 10 min ; API HTTP et refus IT non visibles à ce point aval. |
| Après C01 **vers 12:33–12:35**, [fiche 5.5](choisir-valider-mesures-correctives.md#preuves-recues-application-et-tests-de-c01) | Nouveau compteur 0 → 3, [NFLOG trois SYN](../../assets/files/informatique-industrielle/it-4/Montval-5.5-nflog.pcap), lecture proxy, refus d’écriture, réécriture 4 et HTTP 200. [Export C01 reçu](../../assets/files/informatique-industrielle/it-4/Montval-5.5-regles-apres-c01.nft) : deux tables. | Cycle complet de régulation après correction, débit de logs sous charge ou retour arrière effectivement réalisé. L’export n’a pas d’horodatage interne. |

Les preuves de 5.4 montrent que la température peut encore être **12,1 °C juste après la consigne remise à 4 °C**, avant sa baisse. Après C01, l’API et les lectures attestent des valeurs nominales dans les instants visibles ; elles ne remplacent pas un suivi de disponibilité sur une durée convenue avec l’exploitation.

### Conditions à vérifier avant de clore le volet technique

- Paramètres nominaux relus, mode et commande cohérents, défauts traités, collecte fraîche et alarmes visibles selon les moyens réels.
- Chemins nécessaires disponibles, accès non nécessaires restreints, maintenance utile et urgence organisées ; les droits temporaires sont fermés après intervention.
- Configuration appliquée identifiée, source et export conservés, éventuelle persistance et reprise vérifiées.
- Incertitudes, réserves et contrôles non réalisés remis aux responsables ; accord de l’exploitation et du mainteneur enregistré lorsque le processus est concerné.

Pour le **laboratoire**, on peut conclure à un retour thermique observé et à une journalisation C01 opérationnelle pour le refus testé. On ne peut pas déclarer tous les scénarios validés : suivi complet après C01, cycle bas, retour arrière, panne du processus passerelle et persistance restent hors des preuves reçues.

## 2 — Conséquences opérationnelles : questions qui dépassent l’IT

Le retour d’un écran, d’une consigne ou d’une température d’enceinte ne statue pas sur les produits. Le manuel **EXP-12** confie leur évaluation au responsable d’exploitation, selon les procédures applicables au magasin. Aucune limite sanitaire de libération des lots n’est introduite dans cette fiche.

| Question | Informations techniques à fournir par l’AIS | Réponse / décision à obtenir auprès de l’exploitation |
| --- | --- | --- |
| Combien de temps la température est-elle restée anormale ? | Définition du seuil utilisé, dates/fuseaux, échantillons, trous et bornes d’observation. Distinguer consigne anormale, dépassement de bande et seuil d’alarme. | Définition opérationnelle pertinente selon zones/produits ; impact et conduite à tenir. |
| Les mesures sont-elles complètes ? | Cadence réelle, qualité déclarée, fraîcheur, périodes absentes et différence entre export et capteur indépendant. | Suffisance pour l’exploitation et nécessité d’une relève ou d’un contrôle terrain. |
| Faut-il isoler ou contrôler des produits ? | Période concernée, emplacement, données mesurées et incertitudes ; pas une température produit déduite de l’air. | Lots, mouvements, contrôles qualité, dispositions conservatoires et devenir des produits. |
| L’exploitation normale peut-elle reprendre ? | Vérifications techniques réussies et réserves, paramètres actuels, accès/communications, alarmes et reprise. | Accord de l’exploitation avec FrigoMaint et les responsables qualité désignés selon procédure. |
| Qui valide ? | Journal des actions et résultats, intervenants techniques et éventuelles autorisations reçues. | Nom/fonction de l’autorité de décision, date, conditions et réserves ; informations non fournies à ce stade. |

### Quantifier ce que l’export fictif permet réellement de dire

[Calcul documentaire et bornes — JSON](../../assets/files/informatique-industrielle/it-4/Montval-5.6-periode-haute-scenario.json).

L’export de l’incident contient **181 mesures**, de **08:30 à 11:30 le 8 octobre 2026**, toutes espacées de **60 secondes** ; la qualité renseignée est toujours `OK`. Cela démontre la régularité de ce fichier, pas l’étalonnage du capteur, l’intégrité de l’historique complet ni la présence de données en dehors de la fenêtre reçue.

Pour le critère **strictement > 8 °C**, choisi ici parce que c’est le seuil d’alarme du manuel :

- Dernier échantillon inférieur au seuil avant la hausse : **09:41, 7,98 °C**.
- **63 échantillons** au-dessus de 8 °C, de **09:42, 8,13 °C** à **10:44, 8,14 °C**.
- À **10:45**, mesure **8,00 °C**, qui n’est pas strictement supérieure à 8 °C.

Les deux extrémités des échantillons hauts sont séparées de **62 minutes**. **63 échantillons ne signifient pas 63 minutes d’exposition exacte.** Le franchissement entre relevés n’est pas connu ; les valeurs intermédiaires ne sont pas mesurées par cet export. La consigne 12 °C est documentée de 09:14 à 10:21, soit **67 minutes entre ces deux événements**, ce qui est encore une autre durée. Ces calculs ne donnent pas la température à cœur, l’exposition de chaque lot ou une conclusion sanitaire.

Le scénario mentionne une hausse pendant plusieurs heures ; le présent calcul décrit uniquement la fenêtre de données fournie et le critère > 8 °C. Ne pas élargir les observations au-delà de l’export, ni confondre cette fenêtre avec la simulation du 30 octobre.

### Contenu de la transmission aux responsables

**Synthèse AIS proposée :** état des services et paramètres, chronologie normalisée, plage d’anomalie selon le critère explicite, maximum et limites des mesures, actions réellement exécutées, autorisations connues, communications et protections testées, preuves accessibles et réserves.

Joindre l’inventaire/empreintes, les exports de configuration, les PCAP et décodages utiles, ainsi que la liste des contrôles terrain restant nécessaires. Indiquer clairement : **aucune décision sur les denrées ni autorisation de reprise normale n’est fournie par le dossier**. L’AIS rend un constat technique dans son périmètre ; il ne remplace pas la responsabilité d’exploitation.

## 3 — Préparer le retour d’expérience

| Constat | Ce qui a été détecté / compris | Donnée manquante ou limite | Amélioration à envisager |
| --- | --- | --- | --- |
| Consigne passée à 12 °C | Traces Modbus, SUP et mesures du dossier ; reproduction réussie sur le PoC. | Motif, auteur humain et autorisation exhaustive du changement historique. | Identités nominatives, journal d’intervention, lien changement/autorisation et alerte sur écart de consigne. |
| Accès partagé maint-shared | Sessions VPN corrélées après correction de 2 min 10 s. | Processus et utilisateur sur MAINT-01, exhaustivité des autorisations et état du poste. | Compte nominatif, périmètre/durée, accès contrôlé et collecte de traces poste ; ne pas déclarer une compromission sans preuve. |
| IT direct vers OT bloqué | Test avant C01 et après C01 ; compteurs et trois SYN NFLOG. | Autres origines, chemins latéraux, persistance et charge non testés. | Étendre les essais de couverture au plan réel ; collecte durable et signalement du refus selon besoin. |
| Proxy lecteur efficace sur son endpoint | Exception 01 et consigne inchangée pour écriture via 15021. | Un autre client dans GW peut écrire directement sur 15020. | Séparer collecte et maintenance et imposer le passage par les contrôles applicatifs qualifiés. Ne pas bloquer GW entier au prix de la supervision. |
| C01 améliore la traçabilité | Paquets interdits journalisés en NFLOG et compteur intégral ; flux utiles maintenus. | Pas de collecte permanente prouvée, débit limité non éprouvé sous charge, C01 ne contrôle pas les écritures GW. | Pérenniser collecte/rétention, surveiller ses pannes et qualifier les accès autorisés ; ne pas présenter C01 comme correctif interne du REG. |
| Température revenue près de la consigne | Long PCAP :12,1 →3,8 °C après correction, alarme éteinte. | Cycle complet après correction, décision produits et mesures terrain absents. | Recette exploitation/maintenance avec durée convenue, vérification indépendante et clôture documentée. |
| Exports initialement perdus | Captures de permission refusée, exports refaits puis dates séparées. | Certains relevés avant action n’ont pas été sauvegardés ; un export ultérieur ne les recrée pas. | Répertoire sous compte utilisateur, test d’écriture avant TP, noms datés et conservation des erreurs. |
| Première capture PCAP vide | En-tête seul 24 octets ; nouvelle capture a ensuite fourni les données. | Cause exacte de la capture vide non établie. | Démarrer collecteur avant action, contrôle positif par lecture, bilan de capture et vérification du fichier avant fin de séance. |
| REG-02 reste obsolète | Fin du support et correctifs indisponibles documentés. | Modèle/version/notice complète et capacité de sauvegarde réelle absents. | Inventaire et plan de remplacement, qualification des protections compensatoires et de la reprise, financement à préparer. |

### Ordre de travail proposé après la restitution

1. **Compléter les réserves opérationnelles :** contrôles terrain, décision sur les produits, identité des validateurs et conditions de remise en service. Ce sont des besoins pour Montval, pas des actions déjà faites sur site.
2. **Stabiliser la preuve technique :** observations répétées après C01, cycle complet et scénario de retour arrière, exports datés et conservation du collecteur. Les tests doivent être convenus et ne pas interrompre le contrôle sans coordination.
3. **Réduire le risque résiduel :** séparation réelle des rôles collecte/maintenance, droits et traces nominatives, contrôle applicatif des écritures et détection des changements. Ces mesures restent proposées.
4. **Préparer le remplacement et les reprises :** aucune journalisation ni segmentation ne corrige le logiciel interne de REG-02 ; maintenir un plan industriel et une relève adaptés.

## 4 — Proposition de restitution et état de clôture

**Constat technique du laboratoire :** la modification de consigne et ses effets ont été reproduits ; la consigne a été rétablie à 4 °C avec baisse observée jusqu’à 3,8 °C. Le refus IT direct, le proxy lecteur et les flux nécessaires ont été testés dans les fenêtres documentées. C01 et la collecte NFLOG sont appliquées et observées ; l’export des deux tables est reçu. Les réserves de continuité complète et de retour arrière restent ouvertes.

**Pour Montval :** le diagnostic historique reste provisoire quant à l’auteur et à l’intention. Les moyens réels, les vérifications sur place, l’état des lots et la décision de reprise normale ne sont pas établis par le PoC. **Aucune clôture opérationnelle n’est prononcée ici.**

| Validation à renseigner après restitution | Responsable / avis / date / réserve |
| --- | --- |
| Vérifications IT du périmètre convenu | À renseigner par l’intervenant habilité ; pas de signature simulée. |
| Contrôle frigorifique et maintenance | À confirmer avec FrigoMaint/automaticien. |
| Supervision, alarmes et reprise | À confirmer avec responsable SUP et exploitation. |
| Produits et autorisation d’exploitation normale | Décision du responsable d’exploitation selon procédure ; non reçue. |
| Réserves et actions de suivi acceptées | À consigner après échange ; aucun accord collectif supposé. |

**Production préparée :** liste de contrôle, transmission AIS et retour d’expérience. Les faits, réserves et propositions sont disponibles pour la restitution en binôme ; ni l’analyse documentaire ni le fichier CSV n’est présenté comme une remise en service réelle.

## Ressources

- [Manuel MAN-OT-01](../it-2/MAN-OT-01_Manuel_exploitation_installation_frigorifique.md) : EXP-01/02/04–12, MAI-01/02/05/08, ORG-01/02.
- [Chronologie 5.2](analyser-traces-reconstituer-evenements.md), [réponse 5.3](determiner-premieres-actions-reponse.md), [reproduction et captures 5.4](reproduire-incident-jumeau-numerique.md), [correction et preuves 5.5](choisir-valider-mesures-correctives.md).

[Retour à l’itération 4](index.md) · [Pense-bête](../../pense-bete/glossaire/informatique-industrielle/it-4.md).
