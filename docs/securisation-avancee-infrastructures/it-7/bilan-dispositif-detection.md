# Faire le bilan du dispositif de détection

**7 octobre 2026 — Travail individuel — Bilan de la journée Suricata**

## 🎯 Objectif et portée

Évaluer les capacités du dispositif actuel et préparer son réglage en J8,
avant intégration dans une supervision centralisée. Cette feuille clôt le
parcours Suricata classé **itération 8 dans le mémo** ; « J8 » désigne ici
la prochaine journée annoncée dans l’énoncé, pas un changement de numérotation
ni une activité déjà réalisée.

Le bilan repose sur les commandes et captures des feuilles précédentes.
Aucun nouveau scan, incident, réglage définitif ou raccordement Wazuh n’est
déduit de sa rédaction.

## 1. Installation actuelle

| Élément | État documenté | Preuve / limite |
| --- | --- | --- |
| Système surveillé | VM `192.168.122.229`, File Browser en conteneur, publication TCP 8080 → 80 | L’énoncé mentionne Ubuntu 20.04 ; migration rapportée dans le dossier. Relever l’OS effectif si nécessaire, sans revenir à l’ancienne version |
| Capteur | Suricata **8.0.3** installé directement sur l’hôte | Test de configuration et service actif visibles dans les captures |
| Point d’observation | Hôte, réseau virtuel de la VM | Route hôte → VM par le bridge ; visibilité prouvée pour les trajets testés |
| Interface surveillée | **virbr0**, adresse hôte `192.168.122.1/24` | EVE montre `in_iface:virbr0`. Ancien `eth0` absent : configuration corrigée |
| Trafic entrant visible | HTTP hôte → VM:8080, ressources navigateur, essais sur VM:18080 | Hôte extérieur à la VM ; aucune exposition Internet démontrée |
| Trafic sortant visible | DNS VM → résolveur hôte:53, TLS vers serveur externe:443 ; HTTP de contrôle de connectivité et flux NTP également visibles | Visibilité limitée aux échanges présents dans les captures ; pas d’inventaire exhaustif de tous les trajets |
| Événements disponibles | `dns`, `tls`, `http`, `flow`, `fileinfo`, `alert` ; un événement `ssh` apparaît aussi dans la feuille EVE | Types réellement observés ; l’essai A4 SSH de la dernière activité n’est pas documenté |
| Journal exploité | `/var/log/suricata/eve.json` sur l’hôte | Fichier présent et objets JSON lus par jq ; réception centralisée non vérifiée |
| Règles ajoutées | Quatre signatures rev 1 dans `/etc/suricata/rules/ais-it8.rules` | Configuration acceptée : 4 chargées, 0 échouées/ignorées, code 0 |
| Mode | IDS réseau, observation et alertes | Aucun blocage établi ; filtrage Docker/8080 non traité selon le bilan antérieur |

Le dépôt de règles est figé par la référence
`23bfba7e688fdf5fadd8e378f070dae843e14263`. Les quatre règles sont :

| SID | Condition principale | Capacité démontrée |
| --- | --- | --- |
| 50500003 | `%2e%2e` dans URI brute, sans distinction de casse | Déclenchement sur requête du serveur temporaire/18080 |
| 50500004 | `..%2f` dans URI brute, sans distinction de casse | Même périmètre de test |
| 50500006 | `%252e%252e` dans URI brute, sans distinction de casse | Même périmètre de test |
| 50100004 | Ouverture de balise script dans URI normalisée | Même périmètre de test ; aucune XSS exécutée |

Ces motifs génériques ne prouvent pas une vulnérabilité de File Browser.
Leur détection sur **8080** n’a pas été testée par ces marqueurs ; ne pas
transférer les résultats de 18080 au service principal.

## 2. Deux exemples effectivement observés

### Activité normale autour de File Browser

Le navigateur charge GET `/` puis JavaScript, CSS, polices et images autour
de **10:58:52 +02:00** sur 8080. Les événements HTTP donnent méthode, URI,
statut 200, user-agent, adresses/ports et interface. La boucle curl produit
ensuite cinq accès de 10:59:51 à 10:59:55, tous HTTP 200 ; les bilans affichés
montrent `alerted:false`. Cela établit les activités visibles, pas l’intention
ni l’identité métier de l’émetteur.

![Accès successifs observés dans EVE](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2011-00-05.png)

**Lecture :** plusieurs transactions sur 8080 peuvent produire des objets
`http` et `fileinfo` distincts ; compter les lignes EVE ne revient pas à
compter les gestes humains ni même uniquement les requêtes.

### Alerte pédagogique

Le **7 octobre à 10:30:38.887961 +02:00**, la requête GET
`/ids-test?probe=%2e%2e` vers `192.168.122.229:18080` déclenche **SID 50500003**.
L’événement brut exporté conserve `event_type:alert`, `in_iface:virbr0`,
le `flow_id` **183670500373292**, les adresses/ports, la signature et le bloc
HTTP. Le serveur retourne 404 ; le champ d’alerte affiche `action:allowed`.

![Objet EVE exporté pour la signature 50500003](../../assets/img/securisation-avancee-infrastructures/it-7/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-07%2010-55-20.png)

**Conclusion :** détection du motif réussie sur un serveur temporaire isolé ;
aucune exploitation, lecture de fichier sensible ou action bloquée démontrée.
Les quatre signatures ont déclenché, avec captures dans la feuille des règles.

## 3. Répondre aux six questions

### 1 — Quels événements sont utiles pour surveiller File Browser ?

- Les alertes reliées au trafic réel de 8080, avec règle, heure, source/destination et contexte HTTP : elles doivent être qualifiées.
- Les événements HTTP sur endpoints sensibles, codes 401/403, erreurs et séries inhabituelles ; rapprocher les requêtes d’un même flux et intervalle.
- Les bilans de flux : nouvelles sources, volumes inhabituels, services/ports et destinations sortantes inattendues.
- Les événements DNS/TLS sortants pour repérer des destinations à examiner, sans considérer une destination nouvelle comme malveillante par nature.
- Les événements SSH pour le suivi des connexions administratives, en complément des journaux serveur.

Les logs applicatifs File Browser et système restent nécessaires pour identité,
authentification, droits et opérations sur documents ; le réseau seul n’est
pas une preuve complète de ces actions. POST `/api/renew` avec 401 a été
observé, mais sa cause n’est pas établie. POST `/api/login` avec 200 ne suffit
pas à identifier l’utilisateur et ses droits.

### 2 — Quels événements peuvent produire beaucoup d’informations ?

Le chargement d’une seule page génère ressources statiques, polices, images,
objets HTTP et parfois `fileinfo`. Requêtes DNS de connectivité, échanges
périodiques et bilans de flux peuvent également se répéter. Ils deviennent
bruyants dans une lecture non filtrée, mais restent utiles à une investigation.
**Aucun volume quotidien ni taux de faux positifs n’est mesuré ici** : on
observe la multiplicité des lignes, sans chiffrer une charge non mesurée.

### 3 — Quelles activités importantes ne sont pas détectées actuellement ?

Les quatre règles ne possèdent pas de détection dédiée aux accès répétés,
séries de refus applicatifs, balayage de ports, exfiltration/volumes inhabituels
ou destinations suspectes. Les cinq GET ont été observés sans alerte dans les
bilans affichés. L’identité métier, les droits et le sens d’un téléchargement
ne peuvent pas être déterminés simplement par leur présence sur le réseau.

Les actions dans du trafic chiffré, le loopback et les échanges internes
hors point de capture ne sont pas couverts par ces signatures HTTP visibles.
Cela décrit les limites du jeu de règles et du capteur, sans affirmer qu’une
attaque a été essayée ou qu’aucun autre événement pourrait jamais apparaître.

### 4 — Quelles règles supplémentaires seraient utiles ?

| Piste pour J8 | Besoin et conditions de validation |
| --- | --- |
| Fréquence d’accès à 8080 | Définir seuil/fenêtre et regroupement par source ; comparer usages normaux, navigateur et outil automatisé |
| Répétition de refus sur endpoints sensibles | Qualifier 401/403 et rôle de /api/login, /api/renew ; tester les limites du suivi des réponses. Corrélation applicative souvent nécessaire |
| Accès à ressources sensibles ou sondes applicables | Sélectionner des signatures compatibles avec les versions et le protocole réellement utilisés, sans associer toute CVE à un constat |
| Connexions administratives inhabituelles | Définir sources/heures autorisées et utiliser aussi les journaux SSH ; le contenu des sessions reste chiffré |
| Sorties inhabituelles | Établir destinations et volumes usuels puis tester une détection adaptée ; un flux DNS/TLS seul ne révèle pas automatiquement une exfiltration |

Ce sont des **pistes**, pas de nouvelles règles installées ni des SID inventés.
Certaines exigent une corrélation dans la supervision ou les logs applicatifs,
plutôt qu’une signature réseau isolée. Lire, tester et justifier chaque règle
avant ajout, conformément à la méthode de l’exercice précédent.

### 5 — Comment réduire le bruit sans perdre les événements importants ?

Commencer par des **vues de lecture** ciblées (VM, port, intervalle, type)
en conservant les objets sources. Regrouper les lignes par activité/flux,
distinguer ressources statiques et endpoints métier, puis mesurer les fréquences.
Une vue centrée sur 8080 doit garder une vue complémentaire des sorties et de
l’administration pour ne pas masquer un changement de trajet.

En J8, envisager ensuite seuils, filtres ou suppressions ciblées par SID et
périmètre, uniquement après tests normaux et tests de détection. Ne pas
supprimer globalement 401, DNS ou toutes les alertes d’une source. Conserver
journal des décisions, sauvegarde, retour arrière et contrôle de non-régression.
Réduire réellement la journalisation peut faire perdre une preuve : documenter
ce compromis et la rétention avant décision, sans promettre zéro perte.

### 6 — Une partie du trafic échappe-t-elle au point d’observation ?

Le trafic local à la VM (`lo`), les échanges internes entre processus ou
conteneurs de son réseau Docker et les trajets passant par un autre réseau
ne traversent pas nécessairement `virbr0`. Les échanges entre invités dépendent
également du chemin de commutation et de la configuration de capture ; leur
visibilité n’a pas été testée. Une autre interface VM pourrait contourner ce point.

Le HTTPS/SSH qui traverse `virbr0` peut être visible en tant que paquets et
métadonnées, tandis que son contenu applicatif reste chiffré : ce n’est pas
la même limite qu’un trafic totalement absent. Les DNS réseau et TLS sortants
observés prouvent certains trajets, pas tous les flux. Mode NAT/routé et
association libvirt restent à confirmer ; ne pas affirmer une couverture complète.

## 4. Limites et priorités pour la prochaine journée

| Priorité | Travail à prévoir | Preuve attendue |
| --- | --- | --- |
| Vérifier la couverture | Associer interfaces VM/bridge, examiner mode réseau et trajets utiles ; compléter l’activité SSH | Relevés et captures ciblées, écarts de visibilité explicités |
| Établir une référence normale | Compter requêtes/objets par type et service sur une période définie | Mesures contextualisées, pas seulement captures isolées |
| Régler les signatures | Tester nouvelles conditions pertinentes et faux positifs ; garder les versions/SID et résultats | Configuration acceptée, essais positifs/négatifs, preuves EVE |
| Réduire le bruit | Commencer par vues/agrégations ; tester chaque suppression proposée | Comparaison avant/après et absence de perte sur les scénarios retenus |
| Préparer la centralisation | Définir collecte, droits, horodatage, rétention et preuve de réception | À établir ultérieurement ; aucune ingestion Wazuh acquise |

Le filtrage Docker/8080 demeure un risque distinct et non corrigé par l’IDS.
L’arrêt du serveur temporaire/18080 reste à confirmer. La ressource supposée
absente a retourné **200**, pas 404 : conserver ce résultat réel ; le 401
sur `/api/renew` ne doit pas être transformé en échec de mot de passe.

## 📦 Bilan conservé

Le dispositif observe déjà plusieurs types d’activité réseau de la VM et
quatre signatures génériques déclenchent sur le serveur temporaire. Des
accès HTTP à File Browser sont également visibles sans alerte affichée dans
les événements sélectionnés. La détection reste limitée à ces règles, au
trafic visible et au contenu décodable. **Aucune configuration définitive
n’est adoptée ; réglage et centralisation sont les prochaines étapes.**

- [Point d’observation](identifier-point-observation.md)
- [Événements produits](comprendre-evenements-produits.md)
- [Règles et export EVE](installer-tester-regles-suricata.md)
- [Activités contrôlées sur File Browser](observer-activite-file-browser.md)
- [Retour à l’itération 8](index.md)
- [Retour au module](../README.md)
