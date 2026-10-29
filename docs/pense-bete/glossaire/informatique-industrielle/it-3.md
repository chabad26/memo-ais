# Informatique industrielle — Itération 3 : J4, protections réseau

## Objectif et état des travaux

Concevoir puis mettre en œuvre une segmentation adaptée à Montval, définir et vérifier les flux. Matinée accompagnée, après-midi autonome. Seule la consigne 4.1 est intégrée à ce stade ; aucune configuration ni recette J4 attestée.

## 4.1 — Intégrer les services IT

- **STOCK-01** reçoit températures/alarmes ; **ORDER-01** lit le stock et échange commandes/confirmations avec **SUPPLIER-01**, portail externe commercial.
- **IT-ADMIN** administre ses services autorisés ; **BACKUP-01** sauvegarde données/configurations. Ne pas confondre sauvegarde et historique 90 jours.
- Cible proposée : SUP publie vers **relais de données DMZ**, STOCK le consulte ; pas de commande directe STOCK/ORDER/fournisseur vers REG.
- Copies OT : SUP → dépôt OT DMZ → collecte BACKUP ; dépôt distinct fonctionnellement du relais métier. Méthodes et droits à confirmer, restauration exceptionnelle à concevoir séparément.
- FrigoMaint utilise l’accès contrôlé/bastion proposé pendant les interventions ; les fournisseurs commerciaux n’ont pas ses droits.
- Choisir l’initiateur et documenter données, droits, fréquence et effet de panne pour chaque flux. Protocole/port/authentification non fournis = à confirmer.
- Liaisons en sessions séparées ≠ diode physique. Vérifier dépendances partagées et absence de blocage de SUP par la publication.
- Lots : mapping zone/période à obtenir ; donnée fraîche/horodatée et qualité transmises. Une température d’enceinte ne décide pas de la conformité d’un produit (EXP-12).

[4.1 — Analyse et schéma SVG/draw.io](../../../informatique-industrielle/it-3/integrer-services-informatiques-magasin.md) · [Sommaire J4](../../../informatique-industrielle/it-3/index.md)

## 4.2 — Politique de filtrage

- Zones IT, OT-SUP, OT-CTRL, OT-SERV, DMZ, accès maintenance et externe commercial ; vérifier où passent réellement les paquets.
- **TCP 502** fourni par 4.2 pour SUP → REG ; hypothèses HTTPS 443 (métier/relais/interface/export), accès distant 443 et NTP UDP 123 clairement identifiées. Administration/sauvegarde non connues : paramètres symboliques, règles inactives.
- TCP 502 autorisé ≠ lecture seule ; contrôle applicatif requis. Le relais PoC 01–04 ne ferme pas le port direct et ne constitue pas une segmentation.
- IT-ADMIN → REG direct **refusé faute de besoin** ; maintenance via accès/bastion autorisés, droits et cibles bornés.
- Refus explicites et contrôle des autorisations temporaires avant poursuite `established` ; fermer les sessions existantes à révocation, pas seulement les nouvelles. Ne pas purger toutes les sessions de supervision.
- `forward` pour transit routé ; `input`/`output` pour l’hôte ; boucle locale PoC ≠ transit interzones. Couvrir IPv4/IPv6 et chemins latéraux réellement présents.
- Refus final avec logs limités et compteur ; hypothèses à valider avant application. Essais et résultats non encore attestés.

[4.2 — Fiche et règles proposées](../../../informatique-industrielle/it-3/definir-acces-regles-pare-feu.md) · [Liste CSV](../../../assets/files/informatique-industrielle/it-3/Montval-4.2-regles-filtrage-proposees.csv).

## 4.3 — REG-02 obsolète

- Nouvelle contrainte : REG-02/ZF-02 sans support, correctif ou authentification Modbus ; remplacement non financé cette année. SIT-03 J3 reste l’état antérieur, pas un correctif actuellement disponible.
- Cible : GW-02 seule source réseau vers REG-02. SUP → endpoint lecteur ; FrigoMaint via bastion → endpoint maintenance séparé et autorisé ; pas de direct SUP/bastion/IT/voisin OT.
- H8 : TCP 502 proposé pour écoute GW-LECT ; H9/H10 : maintenance/administration GW inconnues, inactives avant qualification. Registres et opérations exactes à obtenir.
- R10/R22 retirent REG-02 ; Q00–Q02 avant established, Q10–Q13 permissions conditionnelles, Q90 refus GW ; politique consolidée **32 règles**. Fermer aussi les sessions de maintenance existantes à révocation.
- Le proxy PoC 01–04 n’a pas d’endpoint d’écriture autorisée, de filtre de plages ni d’authentification humaine ; port direct à bloquer pour empêcher son contournement.
- Panne protection : visibilité/maintenance perdues, contrôle local attendu si indépendant, à vérifier. Aucun bypass permissif automatique ; relève locale nécessaire.
- Isolation, sources limitées et surveillance réduisent l’exposition sans corriger le logiciel ni l’absence d’authentification. Remplacement à préparer ; aucun risque résiduel accepté ou test de conformité acquis par ce dossier.

[4.3 — Modèle, mesures, règles et limites](../../../informatique-industrielle/it-3/proteger-regulateur-industriel-obsolete.md).

## 4.4 — Briefing et plan d’essais

- PoC : serveur/modèle 15020, passerelle lecture 15021, supervision HTTP 18080 par défaut, tous sur localhost initialement. Les valeurs de la topologie séparée restent à fournir ; NETWORK.md propose IT/DMZ/OT sans plan IP/namespaces détaillé.
- Relever environnements, interfaces, routes, écoutes, cible amont de GW et cible Modbus du dashboard. Celui-ci utilise le serveur direct par défaut.
- T00–T10 : disponibilité, lecture GW → OT, lecture IT → GW, refus FC06/FC05 via GW, direct IT → OT bloqué, source/service interdit, supervision si incluse, perte/reprise du GW et révocation si implémentée.
- Exception Modbus 01 = refus applicatif ; timeout ≠ preuve de pare-feu. Combiner écoute/chemin disponible, capture et compteur.
- La CLI ouvre un socket par requête : deux commandes ne testent pas une session persistante. T09 demande un outil adapté.
- Stopper GW seulement pour tester la continuité locale ; arrêter le serveur réinitialise le modèle. Versions/seuils et état initial à consigner.
- Plan préparé, pas de réseau/règle créé ni résultat attesté. Compléter au briefing avant autonomie.

[4.4 — Fiche et exemples](../../../informatique-industrielle/it-3/preparer-essais-segmentation.md) · [Plan CSV](../../../assets/files/informatique-industrielle/it-3/Montval-4.4-plan-essais-segmentation.csv).

## 4.5 — VM Debian 192.168.122.105

- SSH par clé établi, Debian 13.7/nft 1.1.3/iproute2 6.15.0/Python/tcpdump présents. Sudo exigeait une saisie locale ; après exécution utilisateur, quatre namespaces et règles appliqués, résultats récupérés.
- Paquet VM : `~/ais-it-ot-j4`. Lancement : `sudo bash ~/ais-it-ot-j4/lab-it-ot.sh all`. Original `~/ot-refrigeration-poc` conservé.
- Espaces proposés : IT `ais45-it` 10.77.10.2 ; FW `ais45-fw` .1 sur 10.77.10/20/30 ; GW `ais45-gw` 10.77.20.2 ; OT `ais45-ot` 10.77.30.2. Tous /24, aucun lien gestion/LAN/Internet.
- Filtre `forward`, table `inet ais45`, **dans ais45-fw seulement** : IT→GW TCP15021/18080, GW→OT TCP15020, retours précis ; direct IT/OT et autres refusés. Modbus lecture seule assuré par proxy, pas par le port TCP.
- Dashboard lit GW15021 ; API `/api`. HTTP testé depuis IT du TP, sans publication d’un port sur la VM.
- `setup`, `apply`, `verify`, `inspect` ; `reset-filter` revient à la référence privée permissive ; `teardown` arrête le modèle et conserve les preuves. Aucun nft/sysctl/routage hôte modifié par les scripts.
- Export après application : `evidence/run-.../regles-it-ot.nft`, JSON et relevés des règles/écoutes/routes. Source `.nft` préparée ≠ export de règles réellement appliquées.
- T01/T02/T03/T04/T05/T07 et compteurs prévus par le vérificateur ; panne/reprise, session persistante et REG physique non couverts automatiquement.

[4.5 — Fiche, fichiers et état des preuves](../../../informatique-industrielle/it-3/mettre-en-oeuvre-filtrage-it-ot.md).

### Résultats 4.5 du 29 octobre

Run `20261029T094737Z` : **8 contrôles conformes** ; lecture via GW autorisée ; FC06/FC05 refusées par exception 01 ; relecture consigne 4,0 et porte 0 ; direct IT/OT refusé avec compteur **0 → 3** et serveur disponible via GW ; HTTP `/api` 200 ; compteurs de chemins admis non nuls. Ruleset hôte identique avant/après.

[Règles réellement appliquées](../../../assets/files/informatique-industrielle/it-3/Montval-4.5-applique-regles-it-ot.nft) · [Résultats JSON](../../../assets/files/informatique-industrielle/it-3/Montval-4.5-applique-verification.json). Pas de preuve de panne/reprise, révocation persistante, IPv6 de production ou REG-02 réel.

### Captures 4.5 et essais complémentaires

Douze captures utilisateur intégrées, dont les quatre premières : lancement complet, ruleset (compteur direct **6 paquets**, relevé ultérieur distinct du 0 → 3 initial), lecture via GW à 4,0 °C/compresseur 1 et timeout direct de 11:14. Ce timeout seul ne fournit pas le compteur avant/après de cette tentative.

Complément réalisé : HTTP temporaire **18081** disponible depuis GW (200), timeout depuis IT et `other_drop` **0 → 3 paquets / 180 octets**. Le PCAP fourni contient **39 trames**, des lectures FC03/FC04/FC01 et des SYN directs sans réponse visible ; **aucune FC06**. Le refus des écritures est attesté dans le run automatique antérieur. Panne/reprise et révocation persistante restent à tester.

[Captures et commandes complémentaires](../../../informatique-industrielle/it-3/mettre-en-oeuvre-filtrage-it-ot.md#essais-complementaires-procedures-et-etat-des-preuves).

## 4.6 — Recette des protections et fonctionnement

La [fiche 4.6](../../../informatique-industrielle/it-3/tester-protections-fonctionnement.md) rassemble les six tests réseau déjà documentés. Nouvelle vérification à 11:36 : huit contrôles conformes. Sept captures ajoutées : refus direct 18 → 21, puis 21 → 24 dans le JSON ; pendant coupure, température 3,6 → 4,5 → 4,1 °C et compresseur 0 → 1. Reprise attestée à 11:41:45 : fw-dmz UP/LOWER_UP, deux lectures réussies, consigne 4 °C et HTTP 200. Cycle complet et délai exact non établis. Le message de ruleset hôte différent correspond uniquement à un compteur Docker 6 → 12 dans les exports comparés, sans différence de politique.

- Coupure observée : `sudo ip -n ais45-fw link set fw-dmz down` ; lecture locale dans `ais45-ot`, sans redémarrer le modèle.
- Reprise : `sudo ip -n ais45-fw link set fw-dmz up`, puis lectures via GW et HTTP `/api`.
- Observer plusieurs températures et états du compresseur ; quelques mesures ne prouvent pas un cycle complet.
- Sauvegarder les preuves avant de relancer `lab-it-ot.sh verify`, qui actualise les résultats du run courant.

## 4.7 — Dossier C4 et PDF formateur

[Dossier J4 — configuration et tests de sécurité IT/OT](../../../informatique-industrielle/it-3/documenter-protections-limites.md) : architecture Montval proposée, 32 règles et protections REG-02 ; configuration nft réellement appliquée dans `ais45-fw`, matrice des tests et cinq captures représentatives dans le PDF autonome.

- Montval : DMZ/bastion/GW-02 proposés ; le proxy Python n’est pas une passerelle industrielle qualifiée.
- Laboratoire : refus direct, lectures, refus d’écritures, collecte HTTP, refus par défaut, contrôle local pendant coupure et reprise documentés.
- Non déployés : journalisation dédiée, Suricata, accès de maintenance temporaire, révocation persistante, sauvegarde/restauration du régulateur.
- Conserver configuration et preuves pour J5 ; ne pas réinitialiser les règles ni détruire les namespaces.
- Convention fournie : Iteration2-Atelier7 ; classement du mémo : itération 3/J4 ; site à renseigner, non inventé.
