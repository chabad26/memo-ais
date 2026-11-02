# RES-01a — L5 | Fiche de dépannage Packet Tracer

[Télécharger la synthèse PDF pour le formateur](../../assets/files/admin-reseaux/Synthese-depannage-OSI-Packet-Tracer-Olivier-HIMBLOT.pdf)

**Auteur :** Olivier HIMBLOT · **Date de préparation :** 2 novembre 2026.

**Statut :** inventaire initial en cours à partir des captures fournies le 2 novembre 2026 et des raccordements relevés par l’apprenant. Paramètres des deux laptops et des serveurs TFTP/DHCP observés. Correction NAT C01-PT exécutée et validée pour ICMP et DNS explicite depuis Laptop4 ; traduction UDP observée. DNS DHCP de Laptop4 corrigé et accès HTTPS affiché dans les captures de sa séquence ; le nom du poste est hors cadrage dans les captures de validation. Laptop5 reçoit désormais un bail cohérent et réussit les tests répétés ; preuve HTTPS nommée de Laptop4 et contrôle positif sur PC2 reçus. Projet sauvegardé joint ; cartographie exhaustive et limites de couverture OSI précisées ci-dessous.

**Sources :** `TP Diagnostic.pdf` (consigne, 4 pages) et `TP Diagnostic.pkt` (projet fourni, à conserver intact). Travailler sur une copie enregistrée sous un autre nom ; conserver un état initial avant toute modification.

## 1. Symptôme et périmètre

**Symptôme fourni :** sur le site principal, Laptop4 et Laptop5 n’accèdent pas à **https://tracer.co**. Certains autres postes fonctionnent selon la consigne et peuvent servir de comparaison après vérification.

| Élément | Relevé réel / preuve |
| --- | --- |
| Version Packet Tracer et nom de la copie de travail | À relever |
| Message exact du navigateur sur Laptop4 | Page vide rapportée par l’apprenant ; capture commune 10:47:04 sans nom de poste visible, URL HTTPS affichée. Aucun message d’erreur lisible. |
| Message exact du navigateur sur Laptop5 | Même page vide rapportée par l’apprenant ; pas de seconde capture fournie. Aucun diagnostic DNS/TCP déduit de ce seul constat. |
| Poste de comparaison accédant à la même URL | PC2, capture nommée 11:48:58 après corrections. Aucun résultat initial sur ce poste fourni. |
| Depuis quand / changement antérieur | Non précisé dans la consigne |

## 2. Cartographie préalable de la configuration

La consigne demande l’inventaire **avant les tests de dépannage**. Relever les paramètres en lecture seule ; observer une configuration ne prouve pas qu’elle est correcte. Aucun plan d’adressage de l’ancien TP AlpesNet ne doit être réutilisé sans constat dans ce projet.

| Équipement réel | Rôle | Interfaces / voisin | VLAN / mode du port | IP / masque | Passerelle / routes | Services | Source du relevé |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Laptop4 | Client affecté | FastEthernet0 → ASW4 Fa0/13 (relevé apprenant) | VLAN 999 MANAGEMENT (table ASW4) | 10.99.0.10 / 255.255.255.0 | 10.99.0.1 | DHCP sélectionné ; DNS 9.9.9.1 | Capture Desktop 09:50:40 ; raccordement déclaré |
| Laptop5 | Client affecté | FastEthernet0 → ASW4 Fa0/20 (relevé apprenant) | VLAN 999 MANAGEMENT (table ASW4) | 10.0.99.10 / 255.255.255.0 | 10.0.99.1 | Statique ; DNS 9.9.9.10 | Capture Desktop 09:50:28 ; raccordement déclaré |
| SRV-TFTP | Serveur TFTP nommé dans la topologie ; service à vérifier | ASW4 Fa0/1 (relevé apprenant) | VLAN 30 SERVEURS (table ASW4) | 10.30.0.11 / 255.255.255.0 | 10.30.0.1 | Statique ; DNS 9.9.9.10 ; TFTP non testé | Capture Desktop 09:50:53 ; raccordement déclaré |
| SRV-DHCP | Serveur DHCP nommé dans la topologie ; service/pools à vérifier | ASW4 Fa0/2 (relevé apprenant) | VLAN 30 SERVEURS (table ASW4) | 10.30.0.10 / 255.255.255.0 | 10.30.0.1 | Statique ; DNS 9.9.9.10 ; DHCP non testé | Capture Desktop 09:51:04 ; raccordement déclaré |
| Poste témoin à identifier | Comparaison | À relever | À relever | À relever | À relever | À relever | À relever |
| Équipements intermédiaires, une ligne chacun | À relever | À relever | À relever | À relever | À relever | Routage, filtrage, NAT si présents | Configuration / commande exacte |
| SRV-DNS | Serveur DNS nommé dans la topologie | Liaison vers R1 visible ; interfaces à relever | À relever | 9.9.9.10 / 255.255.255.252 | 9.9.9.9 | Statique ; DNS configuré 9.9.9.10 ; service DNS à vérifier | Capture Desktop 10:00:46 |
| Serveurs utiles, une ligne chacun | DNS, DHCP, HTTPS selon présence | À relever | À relever | À relever | À relever | État et paramètres à relever | Écran exact / capture |

**Schéma à joindre :** clients → accès local → commutation → routage → WAN → serveur cible, avec les dépendances DNS/DHCP réellement présentes. Annoter interfaces, VLAN, sous-réseaux et sources. Distinguer constat et élément à confirmer.

### Écarts constatés, sans conclusion prématurée

- Les deux laptops appartiennent au VLAN 999 selon les ports relevés et la table VLAN, mais affichent deux réseaux IPv4 différents : **10.99.0.0/24** et **10.0.99.0/24**. La configuration de la passerelle effective du VLAN doit permettre de déterminer le réseau attendu ; le numéro du VLAN ne suffit pas à déduire ce réseau.
- Laptop4 affiche **9.9.9.1** comme DNS ; Laptop5 et les deux serveurs affichent **9.9.9.10**. SRV-DNS affiche maintenant **9.9.9.10/30**, passerelle **9.9.9.9** (capture 10:00:46). La capture Services 11:04:42 montre le service DNS **On** et l’enregistrement A **tracer.co → 9.9.9.34**. Cet état configuré ne démontre pas sa joignabilité depuis les laptops. La majorité des paramètres ne prouve pas leur exactitude.
- La sélection DHCP sur Laptop4 et ses champs affichés ne prouvent ni le contenu d’un pool ni l’identité du serveur ayant attribué ces valeurs. Le pool POOL-ROUGE visible contient une adresse de début, une passerelle et un DNS cohérents avec les valeurs affichées sur Laptop4 ; l’attribution effective et le relais éventuel restent à vérifier avant modification.
- ASW4 : Po4, Fa0/23 et Fa0/24 sont affichés en trunk ; VLAN 999 en forwarding sur Po4, pas sur Fa0/23–24 dans l’extrait reçu. Cela ne constitue pas une preuve de panne STP.
- Les MAC des deux laptops ne figurent pas dans l’extrait de table MAC reçu. L’absence d’entrée à cet instant ne démontre pas une panne physique ni une mauvaise affectation VLAN.

### Inventaire DHCP et interfaces de DSW1

La capture **10:00:15** montre le service DHCP sur **On**. Les valeurs suivantes sont relevées dans la liste des pools, sans modification ni renouvellement de bail. Le nom d’un pool n’établit pas son association effective à un VLAN.

| Pool visible | Passerelle | DNS | Début de plage | Maximum utilisateurs |
| --- | --- | --- | --- | --- |
| POOL-ROUGE | 10.99.0.1 | **9.9.9.1** | 10.99.0.10 | 100 |
| serverPool, sélectionné dans l’écran | 10.30.0.1 | 9.9.9.10 | 10.30.0.10 | 0 |
| POOL-VOIP | 10.40.0.1 | 9.9.9.10 | 10.40.0.10 | 100 |
| POOL-BLEU | 10.20.0.1 | 9.9.9.10 | 10.20.0.10 | 100 |
| POOL-VERT | 10.10.0.1 | 9.9.9.10 | 10.10.0.10 | 100 |

Le masque de POOL-ROUGE est tronqué dans le tableau : sélectionner ce pool pour relever sa valeur complète avant correction. Le masque **255.255.255.0** affiché dans le formulaire correspond à **serverPool**, pas automatiquement aux autres pools.

**Écart établi :** POOL-ROUGE annonce 9.9.9.1, différent de l’adresse 9.9.9.10 configurée sur SRV-DNS. **Hypothèse à tester :** cette option DNS erronée empêche la résolution de tracer.co sur Laptop4. La causalité n’est pas encore démontrée : aucun résultat DNS ni service HTTPS final n’est fourni. Ne pas présenter le masque ou l’adresse de Laptop5 comme corrigés.

La capture de remplacement **10:45:30** montre les interfaces VLAN de `DSW1# show ip interface brief`. L’ancienne capture paginée 09:57:48 a été retirée à la demande de l’apprenant.

| Interface DSW1 | Adresse affichée | État / protocole |
| --- | --- | --- |
| GigabitEthernet0/1 | 172.16.0.129 | up / up |
| Vlan10 | 10.10.0.1 | up / up |
| Vlan20 | 10.20.0.1 | up / up |
| Vlan30 | 10.30.0.1 | up / up |
| Vlan40 | 10.40.0.1 | up / up |
| Vlan999 | **10.99.0.1** | **up / up** |

Ce relevé confirme l’adresse de l’interface VLAN 999 et sa disponibilité déclarée, pas sa joignabilité depuis les clients. Son masque reste à relever dans la configuration. Laptop4 affiche la même passerelle ; Laptop5 affiche **10.0.99.1**, différente de l’interface observée. C’est un écart de configuration établi, mais son effet sur le symptôme reste à démontrer par les tests et le correctif validé. Aucun paramètre n’est encore modifié.

![DSW1 — interfaces et passerelles VLAN visibles](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2010-45-30.png)

![SRV-DHCP — pools visibles avant correction](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2010-00-15.png)

![SRV-DNS — paramètres IP initiaux](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2010-00-46.png)

### Captures des paramètres initiaux

![Laptop5 — configuration statique](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2009-50-28.png)

![Laptop4 — configuration DHCP affichée](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2009-50-40.png)

![SRV-TFTP — paramètres IP](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2009-50-53.png)

![SRV-DHCP — paramètres IP](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2009-51-04.png)

## 3. Journal descendant OSI — hypothèse avant chaque test

**Ordre retenu : L7 → L1.** La consigne emploie aussi la formulation « du poste et de ses paramètres vers les services applicatifs » ; cette phrase ne définit pas un ordre OSI descendant. La cartographie préalable collecte les paramètres ; le journal de diagnostic suit ensuite les couches depuis l’application vers le physique. Faire préciser l’ordre si le formateur attend autre chose.

Les exemples ci-dessous sont des **hypothèses à formuler avant exécution**, pas des pannes établies. Ajouter autant de lignes que nécessaire, avec heure et preuve. Un échec ne démontre pas à lui seul la couche responsable.

| N° / heure | Couche / équipement | Hypothèse formulée avant le test | Test ou action exacte | Résultat observé / preuve | Conclusion / suite |
| --- | --- | --- | --- | --- | --- |
| D01 / heure du test non fournie | L7 — Laptop4 | L’accès à l’URL demandée échoue sur ce poste (hypothèse proposée avant le test). | Desktop → Web Browser → `https://tracer.co`. | Page vide selon l’apprenant ; capture 10:47:04 fournie pour illustrer le constat commun, sans nom de poste. Aucun message explicite. | Symptôme rapporté ; ni cause DNS ni couche responsable établies. |
| D02 / heure du test non fournie | L7 — Laptop5 | Le second poste présente le même symptôme (hypothèse proposée avant le test). | Même URL et même manipulation selon l’apprenant. | Page vide rapportée ; seconde capture volontairement non fournie. | Constat déclaré distinct de la preuve visuelle commune ; poursuivre les tests discriminants. |
| D03 / à renseigner | L7 — poste témoin | Le service reste accessible depuis au moins un autre poste. | Identifier un témoin et ouvrir exactement `https://tracer.co`. | À exécuter | Un succès borne la panne, sans valider tout le chemin des postes affectés. |
| D04a / heure exacte du test non fournie | L7 — Laptop4, attribution contextuelle | Le serveur DNS configuré sur ce poste permet de résoudre tracer.co (hypothèse proposée avant le test). | `nslookup tracer.co` dans Desktop → Command Prompt. | Capture 10:53:41 : serveur 9.9.9.1, trois délais affichés de 15000 ms puis `Request to 9.9.9.1 timed-out`. Nom du poste hors cadrage ; attribution à Laptop4 cohérente avec son DNS et les essais demandés. | Échec de la requête vers le DNS configuré ; aucun résultat A fourni. Ne prouve pas seul la cause du silence ni l’accessibilité du DNS réel. |
| D04b / heure exacte du test non fournie | L7 — Laptop5 | Le serveur DNS configuré sur ce poste permet de résoudre tracer.co (hypothèse proposée avant le test). | `nslookup tracer.co` dans Desktop → Command Prompt. | Capture 10:51:47 identifiée Laptop5 : serveur 9.9.9.10, `DNS request timed out`, délai affiché 15000 ms. La fin de commande n’est pas visible. | Au moins une attente sans réponse du serveur configuré ; pas de réponse DNS positive visible. Son adresse est cohérente avec SRV-DNS, mais sa joignabilité depuis ce poste reste à vérifier. |
| D04c / heure exacte du test non fournie | L7 — Laptop4 selon le contexte, nom hors cadrage | Le DNS réel répond pour tracer.co depuis Laptop4 ; l’échec précédent est lié au résolveur configuré 9.9.9.1 (hypothèse proposée avant le test). | `nslookup tracer.co 9.9.9.10` | Capture 11:04:56 : serveur 9.9.9.10, trois délais de 15000 ms, puis `Request to 9.9.9.10 timed-out`. | Hypothèse de réponse du DNS réel infirmée pour cet essai. L’option DNS incorrecte ne suffit donc pas à expliquer tous les échecs ; transport/acheminement/réponse restent à analyser. |
| D05 / à renseigner | L6 — représentation / chiffrement | L’échec concerne la prise en charge du service HTTPS plutôt que le seul nom. | Examiner le service HTTPS de la cible et les détails simulés disponibles, sans modifier son état. | À exécuter | Noter les limites de simulation ; ne pas inventer une validation de certificat ou TLS réel. |
| D06 / à renseigner | L5 — session | L’échange applicatif n’arrive pas à s’établir ou à se maintenir. | Observer la tentative du navigateur en mode Simulation et les événements exposés. | À exécuter | Si la couche n’est pas observable séparément, l’indiquer ; ne pas fabriquer un test indépendant. |
| D07 / à renseigner | L4 — transport | La connexion TCP au service HTTPS n’aboutit pas sur le chemin affecté. | Observer TCP vers le port du service, normalement 443, et les réponses en mode Simulation ; relever adresses et ports effectifs. | À exécuter | Distinguer absence de réponse et refus. Un timeout peut aussi venir des couches inférieures. |
| D08a / heure exacte du test non fournie | L3 — Laptop4 selon la séquence, nom hors cadrage | La passerelle locale répond depuis Laptop4 (hypothèse proposée avant le test). | `ping 10.99.0.1` | Capture 11:09:46 : 4 envoyés, 4 reçus, 0 perdu ; réponses TTL 255, temps < 1 ms. | Joignabilité ICMP de la passerelle prouvée pour cet essai ; chemin local opérationnel pour ce trafic. Ne valide pas l’acheminement WAN ni tous les mécanismes L2. |
| D08b / heure exacte du test non fournie | L3 — Laptop4 selon la séquence, nom hors cadrage | Le serveur DNS réel est joignable en ICMP depuis Laptop4 (hypothèse proposée avant le test). | `ping 9.9.9.10` | Même capture : 4 envoyés, 0 reçu, 4 perdus, 100 % de perte ; quatre `Request timed out`. | Pas de réponse ICMP à cette tentative. Localiser au-delà de la passerelle : route, retour, filtrage, traduction éventuelle, liens et cible restent à distinguer. |
| D08c / heure exacte du test non fournie | L3 — DSW1 | DSW1 possède une route utilisable vers 9.9.9.10 (hypothèse proposée avant le test). | `show ip route` | Capture 11:11:56 : route par défaut `S* 0.0.0.0/0 [1/0] via 172.16.0.142` ; réseau 172.16.0.128/28 connecté sur Gi0/1. | Route candidate présente vers la destination par défaut ; l’identité et la joignabilité du prochain saut, ainsi que le trajet retour, ne sont pas encore prouvés. |
| D08d / heure exacte du test non fournie | L3 — DSW1 | DSW1 lui-même peut joindre le serveur DNS (hypothèse proposée avant le test). | `ping 9.9.9.10` | Même capture : cinq points, `Success rate is 0 percent (0/5)`. | Aucune réponse ICMP reçue ; le problème n’est pas limité au test depuis Laptop4. La présence d’une route ne garantit pas un acheminement réussi. |
| D08e / heure exacte non fournie | L3 — DSW1 | Le prochain saut configuré répond sur le lien de sortie (hypothèse proposée avant le test). | `ping 172.16.0.142` | Capture 11:14:10 : 100 %, 5/5 réponses. | Prochain saut joignable depuis DSW1 ; ce lien ne suffit pas à expliquer les timeouts distants. |
| D08f / heure exacte non fournie | L3 — DR1 | DR1 possède l’adresse utilisée comme prochain saut par DSW1 (hypothèse proposée avant le test). | `show ip interface brief` | Capture 11:15:37 : Fa0/0 = 172.16.0.142 up/up ; Fa0/1 = 9.9.9.1 up/up. | L’adresse de prochain saut de DSW1 correspond bien à Fa0/0 de DR1. |
| D08g / heure exacte non fournie | L3 — DR1 | DR1 possède une route vers le réseau du serveur DNS (hypothèse proposée avant le test). | `show ip route` | Même capture : défaut via 9.9.9.2 ; connecté 9.9.9.0/30 sur Fa0/1 ; statique 10.0.0.0/8 via 172.16.0.129 ; connecté 172.16.0.128/28 sur Fa0/0. | Route candidate vers le DNS via le défaut, retour vers les réseaux 10/8 via DSW1. L’acheminement réel, les routes suivantes et les éventuels filtres restent à contrôler. |
| D08h / heure exacte non fournie | L3 — DSW1, test lancé sur l’équipement non prévu | Les deux hypothèses avaient été proposées pour DR1 ; l’apprenant a signalé après exécution avoir utilisé DSW1. | `ping 9.9.9.2`, puis `ping 9.9.9.10` | Capture 11:21:16 : prompt DSW1, deux résultats 0/5. | Conserver comme tests DSW1 ; ne pas les attribuer à DR1 ni prétendre que des hypothèses propres à DSW1 ont été formulées avant ces essais. |
| D08i / heure exacte non fournie | L3 — DR1 | Le prochain saut WAN répond depuis DR1 (hypothèse proposée avant le test). | `ping 9.9.9.2` | Capture 11:23:17 : prompt DR1, 100 %, 5/5 réponses, min/moy/max 0/1/5 ms. | Voisin WAN joignable depuis DR1 ; aucun défaut de ce lien démontré par cet essai. |
| D08j / heure exacte non fournie | L3 — DR1 | DR1 peut joindre le serveur DNS (hypothèse proposée avant le test). | `ping 9.9.9.10` | Même capture : 100 %, 5/5 réponses, min/moy/max 5/9/13 ms. | ICMP vers le DNS réussi depuis DR1, contrairement à DSW1/Laptop4. Examiner l’acheminement et le retour selon les sources ; ne valide ni DNS ni HTTPS. |
| D08k / heure exacte non fournie | L3 — R0 | Le routeur WAN possède les routes de retour vers les réseaux derrière DR1 (hypothèse proposée avant le test). | `show ip route` | Capture 11:26:26 : réseaux 9.9.9.x connectés/OSPF ; aucune route 10/8 ou 172.16.0.128/28 affichée ; `Gateway of last resort is not set`. R0 possède 9.9.9.2 sur Gi0/0/0. | Pas de route de retour visible vers les sources internes non traduites ; identité du voisin WAN 9.9.9.2 corroborée. |
| D08l / heure exacte non fournie | L3 — DR1 / NAT-PAT | Une règle ou un paramètre de transit distingue le trafic interne de celui émis par DR1 (hypothèse proposée avant le test). | `show running-config` | Captures 11:27:38, 11:28:04 et 11:28:29 : Fa0/0 inside, Fa0/1 outside, PAT via ACL 1 ; seuls 10.10.0.0/24, 10.20.0.0/24 et 10.30.0.0/24 sont permis dans cette ACL. | Réseau Laptop4 10.99.0.0/24 exclu de la sélection NAT. L’ACL ne bloque pas à elle seule tout paquet : le trafic ne correspondant pas reste non traduit et manque de retour sur R0. Correction ciblée puis validation nécessaires. |
| D08 / à renseigner | L3 — adressage / routage | Un paramètre IP ou un chemin aller/retour empêche l’accès. | Comparer IP, masque, passerelle, routes et éventuels NAT/ACL au plan réellement observé ; tester une cible connue avec hypothèse préalable. | À exécuter | Un ping réussi ne valide pas HTTPS ; un ping échoué ne prouve pas seul un défaut de routage. |
| D09 / à renseigner | L2 — accès / VLAN / ARP | Le poste n’est pas dans le segment attendu ou ne résout pas son voisin utile. | Vérifier port/VLAN, trunks éventuels, MAC et ARP sur le chemin local identifié. Écrire les commandes réellement utilisées. | À exécuter | Établir le lien entre le paramètre constaté et le trafic affecté. |
| D10 / à renseigner | L1 — liaison | Un lien utile au chemin est inactif ou mal raccordé. | Examiner câbles, interfaces et états réels sur les équipements concernés. | À exécuter | Un voyant vert ne valide ni VLAN, ni IP, ni service. |

**Si une cause est isolée avant L1 :** la prouver, appliquer une correction à la fois et retester le symptôme. Documenter pourquoi les couches suivantes n’ont pas été testées ; si le critère impose leur examen, les vérifier en lecture seule. Ne pas marquer une couche « OK » sans preuve.

### Preuve du symptôme applicatif avant correction

L’apprenant indique que **les deux laptops n’affichent rien** et fournit une capture unique pour éviter un doublon. L’image montre `https://tracer.co` dans la barre du navigateur et une page vide, sans nom de poste visible ni erreur explicite. Elle ne prouve pas à elle seule les deux essais, leur durée ou la nature de l’échec ; le second constat est conservé comme déclaration de l’apprenant.

![Navigateur — URL HTTPS et page vide avant correction](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2010-47-04.png)

### Résultats des requêtes DNS initiales

**Constat :** les deux captures montrent des attentes sans réponse DNS, avec des destinations différentes : **9.9.9.1** pour l’essai attribué à Laptop4 et **9.9.9.10** pour Laptop5. Le premier résultat ne prouve pas que le DNS réel 9.9.9.10 est accessible ; le second ne prouve pas que le service DNS est arrêté. Un défaut d’adressage, de routage ou de filtrage peut également empêcher la réponse.

![Laptop5 — requête DNS vers 9.9.9.10, timeout visible](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2010-51-47.png)

![Essai attribué à Laptop4 — requête DNS vers 9.9.9.1 expirée, nom du poste hors cadrage](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2010-53-41.png)

Le test explicite proposé a maintenant été réalisé : voir D04c et les nouvelles captures ci-dessous. Aucun succès DNS ni rétablissement HTTPS ne sont démontrés.

### DNS réel configuré, mais interrogation explicite toujours en échec

La capture **11:04:42**, identifiée SRV-DNS, montre le service **On** et deux enregistrements A : `test → 8.8.8.8` et **`tracer.co → 9.9.9.34`**. Cette dernière adresse est une valeur DNS configurée ; elle reste à comparer à l’adresse réelle du serveur HTTPS. Aucun enregistrement n’a été modifié.

La capture **11:04:56** montre `nslookup tracer.co 9.9.9.10` et un échec final après trois attentes de 15000 ms. Le nom du poste n’est pas visible ; l’attribution à Laptop4 repose sur la séquence demandée, pas sur le cadrage. **La réponse attendue n’arrive pas même en visant le DNS réel.** L’écart DNS du pool reste réel, mais le corriger seul ne constitue pas une résolution prouvée.

![SRV-DNS — service actif et enregistrement tracer.co](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-04-42.png)

![Requête explicite vers 9.9.9.10 — timeout final](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-04-56.png)

**Orientation du diagnostic descendant :** le premier échec applicatif est la résolution DNS. L’établissement HTTPS, sa représentation et sa session (L6/L5) ne sont pas validés et ne sont pas testables séparément par ces seules captures. Le timeout n’établit pas non plus un défaut L4 : les paquets et réponses restent à observer. On poursuit l’isolement vers les couches inférieures du chemin DNS, puis on reprendra la validation HTTPS. Le journal ne doit pas présenter L6, L5 ou L4 comme « OK ».

Les contrôles ciblés L3 proposés ont maintenant été fournis dans la capture 11:09:46 : voir D08a/D08b et la synthèse ci-dessous. Un échec ICMP ne démontre pas à lui seul une route absente ou un serveur arrêté ; un succès ne valide pas DNS/HTTPS.

### Localisation L3 : passerelle joignable, DNS distant sans réponse ICMP

La capture **11:09:46** montre successivement `ping 10.99.0.1` avec **4/4 réponses** et `ping 9.9.9.10` avec **0/4 réponse**. Le poste n’est donc pas totalement isolé : sa passerelle répond. Les accès au DNS distant échouent en DNS et en ICMP dans les essais reçus. Cela oriente vers l’acheminement ou la réponse au-delà du segment local, mais **ne démontre pas encore un défaut précis de route, NAT ou ACL**. Aucun de ces mécanismes ne doit être modifié sur la seule base des timeouts. Le nom du poste n’est pas visible ; l’attribution à Laptop4 reste contextuelle.

![Laptop4 selon la séquence — passerelle 4 sur 4, DNS distant 0 sur 4](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-09-46.png)

Les sorties DSW1 demandées sont maintenant reçues dans la capture 11:11:56 : voir D08c/D08d. L’adresse source effective du ping n’est pas affichée ; ne pas la supposer identique à celle de Laptop4.

### DSW1 : route par défaut présente, destination toujours sans réponse

La capture **11:11:56**, prompt DSW1 visible, montre les routes connectées **10.10.0.0/24**, **10.20.0.0/24**, **10.30.0.0/24**, **10.40.0.0/24** et **10.99.0.0/24**, sur les SVI correspondantes. Le lien de sortie est le réseau **172.16.0.128/28** sur **GigabitEthernet0/1** ; la capture des interfaces précédente indique l’adresse locale **172.16.0.129**. La route statique par défaut pointe vers **172.16.0.142**, adresse appartenant au sous-réseau de sortie.

Le ping de DSW1 vers **9.9.9.10** échoue avec **0/5 réponse**. Une route par défaut est donc bien configurée ; son prochain saut doit maintenant être confronté à l’adressage réel du voisin. Les vérifications suivantes ont depuis confirmé que **172.16.0.142 appartient à DR1 et répond** (D08e/D08f). Aucun changement de cette route n’est justifié par les pièces reçues.

![DSW1 — routes connectées, défaut via 172.16.0.142 et ping DNS sans réponse](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-11-56.png)

Ces contrôles sont maintenant reçus : voir D08e à D08g et les deux captures suivantes.

### Prochain saut confirmé et routes de DR1

Le ping **DSW1 → 172.16.0.142 réussit 5/5**. DR1 possède **Fa0/0 = 172.16.0.142**, up/up, et **Fa0/1 = 9.9.9.1**, up/up. La route par défaut de DSW1 pointe donc vers un voisin joignable et identifié. DR1 dispose du réseau de sortie connecté **9.9.9.0/30**, d’un défaut **via 9.9.9.2** et d’une route statique **10.0.0.0/8 via 172.16.0.129**, qui couvre les VLAN observés derrière DSW1.

**Précision DNS :** l’adresse **9.9.9.1** annoncée dans POOL-ROUGE est aussi celle de Fa0/1 de DR1 ; ce n’est pas l’adresse **9.9.9.10** observée sur SRV-DNS. Les captures ne montrent aucun rôle de relais DNS sur DR1 : ne pas lui en attribuer un ni déduire ce rôle de son adresse.

![DSW1 — prochain saut 172.16.0.142 joignable](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-14-10.png)

![DR1 — interfaces et routes observées](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-15-37.png)

Ces tests sont désormais reçus et réussissent depuis DR1 : voir D08i/D08j. La capture précédente 11:21:16 provenait de DSW1, ce que l’apprenant a corrigé explicitement ; ses échecs ne sont pas des échecs DR1.

### Comparaison des origines : succès depuis DR1, échec depuis DSW1

La capture **11:23:17** montre explicitement le prompt **DR1** et **5/5 réponses** pour chacune des destinations **9.9.9.2** et **9.9.9.10**. Le DNS distant répond donc en ICMP depuis DR1 aux instants testés ; l’hypothèse d’une inaccessibilité globale du DNS n’est pas retenue. Cela ne démontre pas son service applicatif pour les clients.

La capture **11:21:16**, également conservée, montre le prompt **DSW1**, avec **0/5 réponse** pour les deux mêmes destinations. L’apprenant a confirmé l’erreur de machine, puis refait les tests sur DR1. La fiche conserve cette différence d’origine sans transformer les premiers résultats en tests DR1.

![DSW1 — essais effectués sur la mauvaise machine, deux échecs ICMP](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-21-16.png)

![DR1 — voisin WAN et serveur DNS répondent chacun 5 sur 5](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-23-17.png)

**Interprétation bornée :** le trajet fonctionne pour les paquets émis par DR1, mais pas pour ceux émis depuis DSW1 ou Laptop4. Les adresses sources sélectionnées par les pings routeurs ne sont pas affichées dans ces sorties. Une route de retour manquante, une politique de filtrage, une traduction éventuellement nécessaire selon l’architecture ou un autre traitement du trafic transitant restent des hypothèses ; aucune commande NAT ni ACL corrective ne doit être appliquée sans configuration probante.

Les relevés proposés ont maintenant été reçus : voir D08k/D08l et l’analyse NAT ci-dessous. R0 affiche l’adresse locale 9.9.9.2 sur Gi0/0/0, corroborant son identité comme voisin WAN de DR1.

### Configuration déterminante : NAT sélectif ne couvrant pas le VLAN 999

Sur **R0**, la capture **11:26:26** montre le réseau DNS **9.9.9.8/30** appris par OSPF via **9.9.9.14**, une adresse locale **9.9.9.2** et **aucune route par défaut**. Aucune route vers **10.99.0.0/24**, une synthèse **10.0.0.0/8** ou **172.16.0.128/28** n’est affichée. Le chemin de retour vers une source interne non traduite n’est donc pas présent dans cette table.

![R0 — table WAN sans route de retour interne ni défaut](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-26-26.png)

**Transcription des seules lignes pertinentes de DR1**, relevées dans les captures 11:27:38 et 11:28:04 ; les captures originales contiennent aussi des paramètres d’authentification et sont conservées dans un dossier privé extérieur au dépôt, sans lien public.

```cisco
interface FastEthernet0/0
 description LAN connection to DSW1
 ip address 172.16.0.142 255.255.255.240
 ip nat inside
!
interface FastEthernet0/1
 description WAN connection to R0
 ip address 9.9.9.1 255.255.255.252
 ip nat outside
!
ip nat inside source list 1 interface FastEthernet0/1 overload
ip route 10.0.0.0 255.0.0.0 172.16.0.129
ip route 0.0.0.0 0.0.0.0 9.9.9.2
access-list 1 permit 10.10.0.0 0.0.0.255
access-list 1 permit 10.20.0.0 0.0.0.255
access-list 1 permit 10.30.0.0 0.0.0.255
```

**Mécanisme identifié :** l’ACL 1 sélectionne les sources traduites par PAT, mais **ne couvre pas 10.99.0.0/24**, réseau observé sur Vlan999 et Laptop4. Le trafic de Laptop4 ne correspond donc pas aux autorisations de sélection NAT ; il conserve sa source interne, pour laquelle R0 n’a pas de route de retour. Il ne faut pas décrire le refus implicite de cette ACL NAT comme une ACL de filtrage appliquée à une interface : son rôle ici est la sélection de traduction. Les pings émis par DR1 peuvent fonctionner avec une source WAN joignable ; leur source exacte n’est toutefois pas affichée dans les captures.

**Correction C01-PT proposée puis appliquée (preuves reçues à 11:33–11:36) :** ajouter seulement le réseau 10.99.0.0/24 à l’ACL de sélection, en conservant les trois autorisations existantes. Ne pas élargir à tous les réseaux ni ajouter une route WAN à la place sans changer explicitement le choix d’architecture.

```cisco
enable
configure terminal
access-list 1 permit 10.99.0.0 0.0.0.255
end
```

**Avant/après attendu :** avant, ACL 1 = trois réseaux 10.10/10.20/10.30 ; après, ces trois entrées plus 10.99.0.0/24. Le réseau voix 10.40.0.0/24 et le réseau de transit 172.16.0.128/28 ne sont pas ajoutés par cette correction ciblée, faute de besoin établi dans ce test.

**Recette proposée avant exécution, désormais reçue dans les captures ci-dessous :** après relecture `show access-lists 1`, depuis Laptop4, hypothèse « la correction NAT permet désormais le retour ICMP depuis le DNS », puis `ping 9.9.9.10`. Sur DR1, hypothèse « cet essai de Laptop4 crée une traduction utilisant l’adresse WAN », puis `show ip nat translations` immédiatement après le trafic. Enfin sur Laptop4, hypothèse « le DNS réel répond désormais pour tracer.co », puis `nslookup tracer.co 9.9.9.10`. Capturer les résultats avant toute autre correction. Une traduction peut expirer : une table vide tardive ne prouve pas qu’aucune traduction n’a eu lieu.

**Résultat applicatif encore attendu :** le DNS configuré de Laptop4 reste 9.9.9.1 tant que le pool et le bail ne sont pas corrigés ; Laptop5 conserve son adressage distinct. Un succès ICMP ou DNS explicite après C01-PT ne suffira donc pas à déclarer le service HTTPS rétabli sur les deux postes. Le ping standard depuis DSW1 peut aussi rester non traduit si sa source est le réseau de transit : ne pas élargir l’ACL uniquement pour faire réussir ce test de diagnostic.

**Retour arrière prévu :** sur DR1, retirer uniquement `access-list 1 permit 10.99.0.0 0.0.0.255` avec sa commande `no` si l’essai doit être annulé, sans supprimer l’ACL entière. Retour arrière proposé, pas exécuté. Conserver la copie initiale du projet.

### C01-PT exécutée : effet NAT confirmé, HTTPS encore à valider

| Preuve reçue | Observation après correction | Portée |
| --- | --- | --- |
| Capture 11:33:36, DR1 | Ajout `access-list 1 permit 10.99.0.0 0.0.0.255` accepté ; `show access-lists 1` affiche les quatre autorisations 10.10/10.20/10.30/10.99. | Correction effective de la sélection PAT ; les autres réseaux permis sont conservés. Deux variantes erronées de la commande de lecture ont été rejetées avant la bonne syntaxe : elles n’ont pas annulé l’ajout accepté. |
| Capture 11:35:16, poste selon la séquence Laptop4, nom hors cadrage | `ping 9.9.9.10` : 4/4 réponses, 0 % de perte, TTL 123, min/moy/max 9/11/13 ms. | L’essai précédemment en échec réussit après le changement. |
| Même capture | `nslookup tracer.co 9.9.9.10` : serveur 9.9.9.10, réponse `tracer.co = 9.9.9.34`, libellée « Non-authoritative answer ». | Résolution explicite effective vers l’adresse attendue dans l’enregistrement observé ; ce libellé n’est pas une erreur. Le résolveur configuré 9.9.9.1 n’a pas encore été remplacé dans les preuves. |
| Capture 11:35:54, DR1 | Traduction UDP : inside local `10.99.0.10:1030`, inside global `9.9.9.1:1030`, outside local/global `9.9.9.10:53`. | Traduction de la requête DNS du client vers l’adresse WAN observée, cohérente avec l’architecture PAT. |

![DR1 — correction NAT et contrôle de l’ACL](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-33-36.png)

![Laptop4 selon la séquence — ping et DNS explicite réussis](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-35-16.png)

![DR1 — traduction UDP du client vers le DNS](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-35-54.png)

**Bilan borné :** l’effet de l’ajout NAT est démontré par les tests avant/après et la traduction reçue. La cause NAT n’est plus une simple hypothèse de configuration. Ce résultat n’est pas encore une validation de `https://tracer.co` avec le DNS normalement configuré, ni une résolution du cas Laptop5.

**Correction C02-PT proposée puis exécutée, preuves reçues 11:39–11:40 :** dans SRV-DHCP → Services → DHCP, sélectionner **POOL-ROUGE**, relever son formulaire complet, remplacer uniquement **DNS Server 9.9.9.1 par 9.9.9.10**, puis **Save**. Conserver réseau/plage, masque, passerelle et maximum utilisateurs. Sur Laptop4, renouveler le bail avec `ipconfig /renew` si la commande est disponible, puis contrôler les paramètres réellement reçus ; ne pas déclarer le DNS changé avant lecture. Formuler avant les tests : « la requête sans serveur explicite utilise désormais le bon DNS et résout tracer.co », puis `nslookup tracer.co` ; ensuite « le service initial est rétabli sur Laptop4 », puis Web Browser → `https://tracer.co`. Capturer les résultats et le nom du poste si possible. Si le navigateur échoue, reprendre l’investigation sur la nouvelle étape sans annoncer le rétablissement.

### C02-PT exécutée : DNS DHCP corrigé et service HTTPS rétabli dans la séquence Laptop4

| Capture | Résultat observé | Conclusion / limite |
| --- | --- | --- |
| 11:39:31, SRV-DHCP identifié | Dans la table, POOL-ROUGE annonce désormais DNS **9.9.9.10**, passerelle 10.99.0.1, maximum 100. Le formulaire sélectionné reste serverPool ; le début de plage et le masque POOL-ROUGE sont tronqués dans cette table. | Valeur DNS du pool corrigée par rapport à 9.9.9.1 avant intervention ; ne pas lire les champs serverPool comme ceux de POOL-ROUGE. |
| 11:39:21, CLI du poste dans la séquence Laptop4 | `ipconfig /renew` retourne **10.99.0.10**, masque **255.255.255.0**, passerelle **10.99.0.1**, DNS **9.9.9.10**. | Le client affiche les bons paramètres après renouvellement ; nom du poste non visible dans le cadrage. |
| 11:39:57, CLI du poste | `nslookup tracer.co`, sans serveur explicite : serveur **9.9.9.10**, réponse **9.9.9.34**. | Résolution avec le DNS configuré effective ; plus besoin de forcer l’adresse du résolveur dans la commande. |
| 11:40:18, navigateur | URL **https://tracer.co** et page « Cisco Packet Tracer », texte d’accueil et liens affichés. | Service initial rendu dans la séquence Laptop4 ; capture sans nom de poste. L’attribution repose sur la suite demandée et reçue, pas sur le cadrage. Ne valide pas Laptop5 ni un TLS réel hors simulation. |

![SRV-DHCP — DNS du pool ROUGE corrigé dans la table](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-39-31.png)

![Laptop4 selon la séquence — renouvellement et DNS reçu](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-39-21.png)

![Laptop4 selon la séquence — résolution sans serveur explicite réussie](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-39-57.png)

![Laptop4 selon la séquence — page HTTPS affichée](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-40-18.png)

**Bilan des deux corrections séparées :** C01-PT a rétabli le ping et le DNS explicite ; C02-PT a changé l’option DNS du pool, le client l’a reçue après renouvellement et la résolution standard puis la page HTTPS ont réussi. Les preuves ne démontrent pas un cycle complet de chiffrement/certificat : le service est vérifié dans les limites de Packet Tracer.

**Cas Laptop5, correction C03-PT proposée puis exécutée, preuves 11:43–11:44 :** poste Fa0/20, VLAN 999, configuration statique **10.0.99.10/24**, passerelle **10.0.99.1**, alors que le réseau connecté DSW1 est **10.99.0.0/24**, passerelle **10.99.0.1**. Une attribution par le pool DHCP existant est une solution de TP à tester, sans prétendre qu’une politique impose DHCP. Elle évite de choisir arbitrairement une adresse statique pouvant être déjà utilisée ou distribuée par le pool. Hypothèse préalable : « une configuration DHCP cohérente avec le VLAN 999 permettra à Laptop5 d’atteindre les services attendus ». Conserver les paramètres initiaux déjà capturés ; passer seulement le mode IPv4 de Laptop5 sur DHCP, puis relever toutes les valeurs reçues avant tests. Ne pas supposer l’adresse qui sera attribuée ni l’identité du serveur sans preuve.

**Recette C03-PT proposée avant exécution, résultats reçus ci-dessous :** après réception du bail, hypothèse « Laptop5 atteint sa passerelle 10.99.0.1 », puis `ping 10.99.0.1` ; « le DNS configuré résout tracer.co », puis `nslookup tracer.co` ; « l’accès initial est rétabli sur Laptop5 », puis Web Browser → `https://tracer.co`. Capturer les paramètres et la page avec le nom du poste visible. Refaire aussi l’accès sur Laptop4 et sur un poste témoin identifié pour contrôler la non-régression. Retour arrière prévu : rétablir les valeurs statiques initiales sur la copie si nécessaire, pas exécuté.

### C03-PT exécutée : Laptop5 reçoit les paramètres du bon réseau et accède au service

| Capture | Observation | Portée et limites |
| --- | --- | --- |
| 11:43:28, nom **Laptop5** visible | DHCP sélectionné, « DHCP request successful » ; **10.99.0.11/24**, passerelle **10.99.0.1**, DNS **9.9.9.10**. | Remplacement effectif des paramètres statiques initiaux 10.0.99.10/24 et 10.0.99.1. Le serveur ayant délivré le bail n’est pas identifié par cet écran seul. |
| 11:43:59, nom **Laptop5** visible | Un premier `nslookup tracer.co` affiche deux attentes DNS de 15000 ms ; un premier `ping 10.99.0.1` échoue **0/4**. La répétition du ping réussit ensuite **4/4**, puis `nslookup tracer.co` renvoie **9.9.9.34** depuis **9.9.9.10**. | Ne pas supprimer les premiers échecs du journal. Les essais ultérieurs démontrent la réussite après répétition, sans établir la cause du délai initial. Aucune trace ARP/STP/DHCP n’autorise à l’attribuer précisément à une convergence ou à un apprentissage. |
| Même capture | `clear` est rejeté par `Invalid Command`. | Tentative d’effacement d’écran, pas un correctif réseau ni une cause du rétablissement ; aucune modification de configuration montrée par cette commande. |
| 11:44:20, navigateur **Laptop5 identifié** | **https://tracer.co** affiché avec page « Cisco Packet Tracer », texte d’accueil et liens. | Succès du service applicatif sur Laptop5 identifié ; aucune validation de TLS réel hors simulation. |

![Laptop5 identifié — DHCP et nouveaux paramètres IP](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-43-28.png)

![Laptop5 identifié — premiers échecs puis ping et DNS réussis](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-43-59.png)

![Laptop5 selon la séquence — page HTTPS affichée](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-44-20.png)

**Bilan :** trois défauts de configuration sont étayés : sélection NAT ne couvrant pas le réseau client, option DNS erronée dans POOL-ROUGE, adressage statique de Laptop5 hors du réseau de son VLAN. Les corrections ont été introduites séparément, puis les services vérifiés. Le remplacement du mode statique de Laptop5 par DHCP corrige simultanément son adresse et sa passerelle dans une seule action de configuration ; il ne prouve pas lequel de ces paramètres aurait suffi à lui seul.

**Contrôles finaux désormais reçus :** Laptop4 identifié affiche la page HTTPS en capture 11:48:27 ; PC2 identifié affiche la même page en capture 11:48:58. Aucun succès initial PC2 n’avait été fourni : il s’agit d’un contrôle positif après intervention, pas d’une comparaison avant/après mesurée. Le projet sauvegardé est joint sous `TP Diagnostic corrigé.pkt`. La cartographie exhaustive des autres équipements, chemins et services demandée par la consigne reste à compléter ; les preuves recueillies portent sur les équipements utiles examinés, pas sur toute la topologie.

## 4. Causes établies

| Cause précise | Équipement / paramètre | Valeur constatée | Valeur attendue et justification | Tests établissant le lien au symptôme |
| --- | --- | --- | --- | --- |
| Exclusion de 10.99.0.0/24 de la sélection NAT, effet du correctif validé sur ICMP et DNS explicite | DR1, ACL 1 utilisée par PAT | Autorisations 10.10/10.20/10.30 uniquement | Autoriser aussi 10.99.0.0/24 pour la traduction PAT existante | D08k/D08l avant ; captures 11:33:36, 11:35:16 et 11:35:54 après ; HTTPS final confirmé sur Laptop4 identifié en capture 11:48:27 |
| DNS incorrect annoncé au client DHCP ; correction suivie de résolution standard et HTTPS réussis dans la séquence Laptop4 | SRV-DHCP, POOL-ROUGE, option DNS | 9.9.9.1, adresse observée sur DR1, pas celle de SRV-DNS | 9.9.9.10, adresse réelle et service DNS observés | Timeout initial ; C02-PT : pool corrigé, renouvellement, résolution standard et page HTTPS ; confirmation HTTPS sur Laptop4 identifié en capture 11:48:27 |
| Adressage statique de Laptop5 incohérent avec son réseau de VLAN ; remplacement par DHCP suivi de tests réussis | Laptop5, Fa0/20 VLAN 999 | 10.0.99.10/24, passerelle 10.0.99.1 | Réseau 10.99.0.0/24, passerelle 10.99.0.1 ; bail reçu 10.99.0.11/24 | Configuration initiale, routes DSW1, capture DHCP nommée 11:43:28, tests répétés 11:43:59 et page HTTPS 11:44:20 ; premiers échecs conservés |

Plusieurs erreurs peuvent coexister ; ne pas s’arrêter à une première correction si l’un des deux postes échoue toujours.

## 5. Corrections — une modification à la fois

| Cause / équipement | État initial conservé | Commande ou manipulation exacte appliquée | État après | Retour arrière prévu | Preuve |
| --- | --- | --- | --- | --- | --- |
| C01-PT — DR1 / sélection NAT | ACL 1 autorise 10.10/10.20/10.30 ; 10.99 absent | `configure terminal`, `access-list 1 permit 10.99.0.0 0.0.0.255`, `end` | `show access-lists 1` : quatre autorisations, dont 10.99.0.0/24 ; ping et DNS explicite depuis Laptop4 réussis | `configure terminal`, `no access-list 1 permit 10.99.0.0 0.0.0.255`, `end` ; retrait non exécuté | Captures 11:33:36, 11:35:16, 11:35:54 |
| C02-PT — SRV-DHCP / POOL-ROUGE | DNS 9.9.9.1 | Services → DHCP → POOL-ROUGE → DNS Server 9.9.9.10 → Save (manipulation proposée ; état obtenu capturé), puis `ipconfig /renew` sur le client de la séquence Laptop4 | DNS du pool et du client = 9.9.9.10 ; nslookup standard et HTTPS réussis | Remettre DNS 9.9.9.1 dans le seul pool puis renouveler si annulation nécessaire ; non exécuté | Captures 11:39:21, 11:39:31, 11:39:57 et 11:40:18 |
| C03-PT — Laptop5 / IPv4 | Statique 10.0.99.10/24, passerelle 10.0.99.1, DNS 9.9.9.10 | Desktop → IP Configuration → DHCP | DHCP réussi ; 10.99.0.11/24, passerelle 10.99.0.1, DNS 9.9.9.10 ; ping et DNS réussis après répétition, page HTTPS affichée | Repasser en Static et restaurer les valeurs initiales si annulation nécessaire ; non exécuté | Captures 11:43:28, 11:43:59 et 11:44:20 |

Une commande de consultation n’est pas un correctif. Conserver la copie initiale et enregistrer séparément le projet corrigé.

## 6. Validation fonctionnelle et non-régression

| Poste / contrôle | Test | Résultat observé / preuve | Conclusion |
| --- | --- | --- | --- |
| Laptop4 identifié | Ouvrir exactement `https://tracer.co` dans Web Browser. | Capture 11:48:27 : titre Laptop4, URL HTTPS, page Cisco Packet Tracer, texte et liens | Accès initial rétabli sur le poste identifié. |
| Laptop5 identifié | Ouvrir exactement `https://tracer.co` dans Web Browser. | Capture 11:44:20 : titre Laptop5, URL HTTPS et page affichés | Succès applicatif capturé sur le poste identifié, après DHCP et répétition des tests. |
| PC2 identifié | Ouvrir la même URL après correction. | Capture 11:48:58 : titre PC2, URL HTTPS et page affichée | Contrôle positif sur un autre poste ; aucun état initial fourni, pas de mesure exhaustive de non-régression. |
| Paramètres modifiés / sauvegarde | Relire ACL, DNS DHCP et configuration Laptop5 ; conserver une copie distincte | Captures C01/C02/C03 et `TP Diagnostic corrigé.pkt` reçu | Sauvegarde conservée avec empreinte ; réouverture du fichier et persistance des états non retestées par l’assistant. |

La preuve attendue montre **le poste, l’URL HTTPS et le contenu retourné**, pas seulement un ping, un port actif ou une page HTTP. Noter tout comportement non concluant.

### Dernières preuves applicatives

![Laptop4 identifié — validation finale HTTPS](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-48-27.png)

![PC2 identifié — contrôle après correction](../../assets/img/admin-reseau/tppackettracer/Capture%20d%E2%80%99%C3%A9cran%20du%202026-11-02%2011-48-58.png)

## 7. Synthèse pour la restitution

« Laptop4 et Laptop5 n’accédaient pas à https://tracer.co. J’ai inventorié leurs paramètres et leur VLAN, puis formulé les hypothèses avant les tests applicatifs. Les requêtes DNS ont échoué, y compris en visant le DNS réel depuis Laptop4. La passerelle locale répondait, mais pas le DNS distant. En comparant les origines, j’ai constaté que DR1 atteignait le DNS alors que DSW1 et Laptop4 ne l’atteignaient pas. L’examen du routage WAN et du NAT a révélé que l’ACL de traduction excluait 10.99.0.0/24. Après ajout de ce seul réseau, ping, résolution explicite et traduction UDP ont réussi. J’ai ensuite corrigé l’option DNS du pool DHCP et renouvelé le bail de Laptop4 : résolution standard et HTTPS ont fonctionné. Enfin, Laptop5 avait une adresse et une passerelle statiques hors du réseau de son VLAN ; son passage à DHCP lui a donné 10.99.0.11/24 et la bonne passerelle. Après des premiers échecs conservés dans le journal, les tests répétés puis HTTPS ont réussi. J’ai enfin revérifié Laptop4 et contrôlé l’accès sur PC2. »

### Couverture de la démarche par couches — ce qui est effectivement démontré

Le diagnostic a démarré par le service et sa dépendance DNS (L7), puis s’est orienté vers l’acheminement (L3) après l’absence de réponse. Les relevés L2/L1 ont aussi été collectés pendant la cartographie préalable. **Il ne s’agit pas d’une suite de tests indépendants prouvant chacune des sept couches dans l’ordre strict.** Cette limite doit être expliquée au formateur, pas masquée par une reconstruction du journal.

| Couche | Preuves ou observations disponibles | Limite |
| --- | --- | --- |
| L7 — application | Échecs DNS initiaux, réponses après corrections, pages HTTPS finales sur Laptop4, séquence Laptop5 et PC2 | Les premiers échecs du navigateur n’ont qu’une capture commune ; Le succès final de Laptop5 est identifié directement par le titre de la fenêtre. |
| L6 — présentation | Contenu web rendu au travers de l’URL HTTPS du simulateur | Pas de contrôle indépendant de chiffrement, certificat ou format négocié. |
| L5 — session | Échange applicatif abouti après correction | Aucune trace indépendante de mécanisme de session ; ne pas inventer une validation TLS réelle. |
| L4 — transport | Traduction UDP du client vers le DNS en port 53 ; réponses DNS reçues | Pas de capture détaillée d’établissement TCP/443 ni de filtrage de transport testé séparément. |
| L3 — réseau | Adressage, passerelles, routes, comparaisons ICMP, NAT/PAT, trois corrections distinctes | Sources exactes des pings routeurs non affichées ; pas de retour arrière testé ni de contrôle de tout le WAN. |
| L2 — liaison | Ports/VLAN relevés, trunks et états de forwarding sur ASW4, table MAC initiale, tests du chemin local | Pas de capture ARP ; premiers timeouts de Laptop5 non attribuables précisément à l’apprentissage. |
| L1 — physique | Interfaces DR1/DSW1 up/up, états des ports et liens visibles dans la topologie | Pas de test matériel de câblage ; résultats dans un simulateur. |

### Sauvegarde et éléments joints

- `TP Diagnostic.pkt` : original reçu dans le dossier livrable, conservé intact.
- `TP Diagnostic corrigé.pkt` : fichier ajouté par l’apprenant dans le dossier livrable après les corrections ; contenu binaire non décodé et réouverture non exécutée ici.
- `TP Diagnostic.pdf` : consigne fournie.
- `Inventaire-preuves-TP-Diagnostic.json` : empreintes SHA-256 des projets et de la consigne ; une empreinte prouve l’identité d’un fichier, pas sa conformité technique.
- Captures publiques référencées ; deux captures contenant des paramètres d’authentification conservées dans un dossier privé extérieur au dépôt, avec transcription des seules lignes réseau utiles dans la fiche.

### Réserves avant remise

La cartographie utile au diagnostic est documentée, mais le relevé exhaustif de tous les ports, VLAN et configurations des autres sites/routeurs demandé par le PDF n’est pas encore fourni. L’adresse 9.9.9.34 est celle de l’enregistrement DNS et de la réponse observée ; la configuration IP et le service du serveur HTTPS lui-même restent à relever directement. Il reste à confirmer la réouverture de la sauvegarde corrigée et, si nécessaire pour le critère du formateur, à compléter les contrôles de couches non observées séparément. La validation de compétence relève du formateur ; les succès applicatifs ne rendent pas ces réserves inexistantes.
