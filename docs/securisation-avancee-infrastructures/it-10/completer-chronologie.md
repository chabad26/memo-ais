# Compléter la chronologie

**Itération 10 — 12 octobre 2026 — Travail individuel**

## 🎯 Objectif

Reconstruire l’activité observée à partir des différentes sources disponibles.
Reprendre la chronologie de J9, rechercher les événements manquants et
séparer les faits observés de leur interprétation.

**Statut : chronologie J9 reprise et complétée en J10 par les sorties
journald/auditd et quatre captures.** Les événements analysés datent du **9 octobre**, pas du 12.
Aucun nouvel événement ou état de service n’est déduit de cette feuille.

## Résultats J10 — journald et auditd retrouvés

Les lectures effectuées le **12 octobre** portent sur les événements du
**9 octobre**. Les sorties sont en **UTC** ; la chronologie ci-dessous les
convertit en CEST pour comparaison avec J9. Les commandes sont des lectures
historiques, pas de nouvelles activités du scénario.

### Faits ajoutés à la chronologie

| Heure CEST | Source | Fait observé | Interprétation | Confiance |
| --- | --- | --- | --- | --- |
| 13:58:05.891775 | Journald VM | SSH accepte une clé publique pour oliv depuis hôte:40862 ; session ouverte puis déconnexion à .967530, session retirée à 13:58:06.957284 | Session SSH courte effectivement réussie ; ne prouve pas que le script utilise cette session | Élevée pour événements |
| 13:59:59.576382 | Journald sudo, PID 157574 | Invocation du script sans argument, fermeture à .577833 | Essai bref ; code prévoit usage/exit 1, sortie réelle non fournie | Élevée pour commande, moyenne pour résultat |
| 14:00:14.389756–14:01:17.061689 | Journald sudo, PID 157761 ; auditd | Script avec cible 192.168.122.229 puis fermeture du contexte | Premier essai avec cible, déroulement détaillé non établi | Élevée pour commande et heures |
| 14:01:27.787212 | Journald sudo | apt update | Préparation d’environnement documentée | Élevée |
| 14:01:40.285200–14:01:56.312047 | Journald sudo, PID 158889 | apt install nmap, ouverture/fermeture du contexte | Concorde avec dpkg/Wazuh déjà reçus ; pas preuve d’un scan à elle seule | Élevée |
| 14:01:59.367435–14:04:28.275425 | Journald sudo, PID 159232 ; auditd événements 738–741 | Nouvelle invocation du script vers la VM ; session sudo ouverte/fermée | Horaire local plus précis que l’heure de réception Wazuh ; les phases restent non établies par sudo seul | Élevée pour événements |
| 14:06:58.250834–.253069 | Journald PackageKit/systemd et auditd événement 742 | PackageKit daemon quit ; packagekit.service Deactivated successfully ; audit SERVICE_STOP unit=packagekit à .252 UTC | **Service manquant identifié : PackageKit**, pas File Browser ; aucun effet sur File Browser établi | Élevée pour service et concordance |
| Recherche sur 14:33:13–14:36:00 | Auditd VM, ausearch | `<no matches>` après correction du format de date | Aucun événement audit retrouvé sur cette fenêtre ; ne prouve pas l’absence des GET capturés par Suricata | Élevée pour le résultat transmis, limitée au périmètre |

**Corrélation avec Wazuh :** PID sudo **159232**, événements audit
**738–741** et commande permettent de rapprocher les pièces. L’invocation
locale est à **12:01:59.367435 UTC**, reçue dans Wazuh à
**12:01:59.967 UTC** ; la fermeture locale est à **12:04:28.275425 UTC**,
alors que la pièce Wazuh affiche une réception à **12:04:29.817 UTC**.
Les différences correspondent à des étapes de journalisation/réception ;
elles ne démontrent pas un décalage d’horloge ou une anomalie.

L’événement **742** de Wazuh, reçu à 12:06:59.831 UTC avec le service absent
de la projection, correspond à l’événement audit local **unit=packagekit**
à 12:06:58.252 UTC. Cette piste est donc résolue au niveau de l’identité du
service ; pas de lien causal au scénario ou d’arrêt File Browser à inventer.

Le format initial `10/09/2026` a été rejeté avant recherche. La correction
`date +%x` donne **10/09/26** : auditd fournit bien des événements sur la
fenêtre initiale. Le `<no matches>` concerne la seconde fenêtre, celle de
la reproduction. Le rôle des sources reste complémentaire : journald décrit
les commandes, auditd les sessions/services, Suricata les requêtes réseau.

### Captures de réalisation

![Journal système de la VM pour la fenêtre initiale](../../assets/img/securisation-avancee-infrastructures/it-10/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-12%2009-30-49.png)

**09:30:49 :** journal du 9 octobre, commandes sudo et arrêt PackageKit
lisibles. L’empreinte de clé SSH affichée n’est pas nécessaire à l’analyse
et n’est pas recopiée dans les tableaux.

![Auditd : session SSH et débuts des sessions sudo](../../assets/img/securisation-avancee-infrastructures/it-10/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-12%2009-31-12.png)

**09:31:12 :** format 10/09/26 et événements audit locaux, session SSH 11
et contexte sudo session 2. Ils ne doivent pas être confondus.

![Auditd : sessions sudo et services](../../assets/img/securisation-avancee-infrastructures/it-10/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-12%2009-31-20.png)

![Auditd : suite des événements de contexte](../../assets/img/securisation-avancee-infrastructures/it-10/Capture%20d%E2%80%99%C3%A9cran%20du%202026-10-12%2009-31-24.png)

**09:31:20 et 09:31:24 :** séquence des sessions/services conservée.
L’identification finale PackageKit et le résultat `<no matches>` sont
établis par la sortie texte complète fournie, pas par les seules parties
visibles de ces captures.

**Bilan complémentaire :** contexte initial mieux daté et service identifié.
Aucune nouvelle trace des ports fermés de la reproduction n’est fournie ici ;
la recherche des flows Suricata reste la piste adaptée pour ce manque.
Les autres sources décrites comme silencieuses par Olivier ne sont pas
assimilées à des recherches exhaustives sans leurs fichiers/filtres/résultats.

## 1. Reprendre les bonnes fenêtres

Conserver la distinction établie dans
[l’analyse J9](../it-9/incident-premiers-elements.md) :

| Séquence | Période et source | Limite à conserver |
| --- | --- | --- |
| Exécution initiale sur la VM | Invocation Wazuh à 14:01:59 CEST, fin de contexte sudo à 14:04:29 | VM vers sa propre adresse ; routage local `lo` confirmé ultérieurement, hors capteur `virbr0` |
| Navigation Firefox | Dix objets HTTP à 14:06:18–14:06:31, source hôte | Activité distincte ; lien causal au script non établi |
| Reproduction depuis l’hôte | 14:33:13–14:35:38 CEST ; 22 GET et 99 alertes SYN retrouvés | Scénario pédagogique généré par Olivier ; aucune compromission établie |
| Tests de capacité antérieurs | Scans, ports 65001–65003, chemins `/ais-lab-inhabituel-*` | Ne pas les ajouter comme événements de la reproduction ; les scans du script ne visent pas 65001–65003 |

Le début choisi 13:20 en J9 était une borne de recherche, pas le début prouvé
des activités. Pour la reproduction, utiliser **14:33:13 inclus à 14:35:39
exclu CEST** ; côté Wazuh cela correspond à **12:33:13–12:35:39 UTC**, avec
extension justifiée pour la réception si nécessaire.

**Avant recherche :** vérifier les fichiers encore disponibles, leurs dates
et rotations. Ne pas relancer le script pour reconstruire le passé ; une
nouvelle exécution serait une nouvelle reproduction à documenter séparément.

## 2. Chronologie reprise des preuves J9

Heures du **9 octobre 2026, CEST (UTC+02:00)**. La confiance concerne la
proposition indiquée, pas la gravité. Les pièces et captures sont référencées
dans [J9](../it-9/incident-premiers-elements.md).

| Heure | Source | Fait observé | Interprétation | Confiance |
| --- | --- | --- | --- | --- |
| 14:01:59.967 | Wazuh journald/sudo, heure de réception convertie | Invocation `/home/oliv/j9-filebrowser-incident.sh 192.168.122.229` sur la VM | Script dirigé vers la propre adresse VM ; actions détaillées non confirmées par la seule invocation | Élevée pour la commande, limitée pour son résultat |
| 14:04:29.817 | Wazuh auditd | USER_END du contexte sudo PID 159232 | Fin de contexte cohérente avec durée du script ; réussite des phases non démontrée | Élevée pour l’événement, moyenne pour le rapprochement |
| 14:06:18–14:06:31 | Suricata HTTP | Dix requêtes Firefox, login/liste/polices/réglages, HTTP 200, source 192.168.122.1 | Navigation compatible avec usage normal ; distincte du script VM | Élevée pour champs, moyenne pour contexte |
| 14:33:13 | Terminal hôte, sortie du script | Début de reproduction depuis l’hôte, cible 192.168.122.229:8080 | Nouvelle exécution sur trajet observable | Élevée |
| Phase 1, heures détaillées à retrouver | Sortie Nmap | Scan 22,80,443,8000,8080,8443 : 22/8080 ouverts, quatre fermés ; scan 1–1000 : 22 ouvert et 999 fermés | Exploration contrôlée ; inventaire limité aux ports testés | Élevée pour résultats client ; horaires précis manquants |
| 14:33:35.132231–.137781 | Suricata alert | 99 alertes SID 1009001, source hôte vers VM, action allowed | Volume SYN pendant la phase de scan ; pas 99 scans ni preuve d’intention hostile | Élevée pour alertes |
| 14:34:05.148812 et 14:34:10.158378 | Suricata HTTP et sortie curl | Deux GET `/`, HTTP 200 | Accès normaux, cinq secondes d’intervalle | Élevée |
| 14:34:30.167933–14:34:51.227912 | Suricata HTTP et curl | GET `/admin`, `/backup`, `/private`, `/config`, `/config.json`, `/.env`, `/debug`, `/old`, tous 200 | Exploration de huit chemins, environ trois secondes entre accès ; ressource demandée ≠ fichier réel | Élevée pour requêtes |
| 14:35:14.245318–14:35:36.343031 | Suricata HTTP | Douze GET `/admin`, tous 200, intervalles proches de deux secondes | Répétition contrôlée, visible sans alerte HTTP correspondante dans l’extrait | Élevée |
| 14:35:38 | Terminal hôte | Fin affichée du scénario | Fin rapportée ; les 22 GET sont confirmés séparément par EVE | Élevée |
| Recherche après reproduction | Docker et archives Wazuh, capture 14:41:37 | Aucun message Docker pour 14:33:13–14:35:39, code 0 ; aucun objet Docker Wazuh dans la sélection 12:33:13–12:36:00 UTC | Limite de visibilité applicative ; absence de résultat ≠ absence d’activité | Élevée sur la capture et son périmètre |

**Origine de la reproduction :** hôte `192.168.122.1` → VM
`192.168.122.229`. L’ordre des événements concorde avec code et sortie du
script. Docker et Wazuh ne confirment pas les GET de la reproduction dans
les recherches montrées ; leur absence ne contredit pas les faits réseau.

## 3. Événements manquants à rechercher en J10

| Besoin | Recherche prioritaire | Ce qui permettrait de compléter | État avant recherche J10 |
| --- | --- | --- | --- |
| Exploration de ports | Flows Suricata commencés dans la phase 1, ports et réponses ; éventuelle capture TCP conservée | Horaires précis des deux scans, ports distincts et états observables | Résultats client et alertes connus ; détail des flows manquant |
| Connexions vers ports fermés | Flows TCP SYN/RST sur les ports effectivement sondés | Concordance refus Nmap / reset réseau et heure de début | Ne pas utiliser les anciens 65001–65003 hors scénario |
| Accès à File Browser | Objets HTTP et réponses déjà fournis, objet original si disponible | Champs supplémentaires et référence de pièce | Deux GET `/` déjà établis ; inutile de les régénérer |
| Chemins inhabituels / répétition | Objets HTTP originaux et recherche applicative si une source nouvelle existe | Provenance, corps ou contexte applicatif éventuellement conservés | 20 GET hors racine établis, dont 13 `/admin` au total |
| Origine et ordre | Comparaison timestamps, flow.start/end, script et sortie client | Séparation des phases et des flux non liés | Hôte confirmé ; ne pas attribuer tous les événements voisins au script |
| Exécution initiale | Sortie initiale, logs système originaux, éventuelles traces locales | Déroulement effectif de l’essai VM | Non vérifiable au-delà des invocations et du contexte sudo |

## 4. Rechercher les flows sans manquer leur émission tardive

### Sur l’hôte Suricata

Localiser les journaux disponibles :

```bash
sudo ls -lh /var/log/suricata/eve.json*
```

Lire le fichier contenant le **9 octobre**. La commande ci-dessous prend
le fichier courant comme exemple ; si la fenêtre est tournée, adapter
l’entrée. Ne pas conclure à l’absence sur un fichier ne contenant plus J9.

```bash
sudo jq -c '
  select(.event_type == "flow")
  | select(.src_ip == "192.168.122.229" or .dest_ip == "192.168.122.229")
  | select((.flow.start // "") >= "2026-10-09T14:33:13"
       and (.flow.start // "") < "2026-10-09T14:35:39")
  | {timestamp,flow_id,src_ip,src_port,dest_ip,dest_port,
     proto,app_proto,flow,tcp}
' /var/log/suricata/eve.json
```

Les bornes supposent le format CEST observé en J9 ; vérifier le fuseau des
champs avant toute comparaison lexicale. Filtrer sur **flow.start** permet
de retrouver les bilans émis après la fin du script. Conserver `timestamp`
comme heure de publication distincte. Les indicateurs TCP d’un flow sont
agrégés ; ne pas les présenter comme une séquence paquet par paquet.

Rapprocher port, source, heure de début et `flow_id` des alertes. Compter
séparément transactions, ports distincts, flux et alertes. SYN/RST est
compatible avec un refus ; absence de réponse ne prouve pas un port fermé.
Les 99 alertes 1009001 comptent des correspondances de règle, pas les
999 ports fermés retournés par Nmap.

### Wazuh et autres sources

Vérifier la présence d’archives correspondant au 9 octobre dans le manager,
ainsi que les journaux système disponibles sur la VM. La collecte applicative
sans résultat a déjà été examinée en J9 : ne pas répéter la même recherche
sans nouveau fichier, filtre ou raison de couverture.

Rechercher de nouvelles pièces pertinentes dans auditd/journald/dpkg ou
les alertes Wazuh, en distinguant origine système et copie du log Docker.
Une projection `data:null` exige l’objet original/full_log pour expliquer
l’événement ; le nom du décodeur seul ne prouve pas une action détaillée.
Les heures de réception Wazuh sont en UTC dans les preuves reçues.

Si une capture réseau ou sortie du script a été conservée, l’utiliser comme
pièce historique. Un `tcpdump` lancé aujourd’hui ne peut pas récupérer les
paquets passés. Une lecture des droits ou de l’état actuel ne reconstitue pas
automatiquement ceux du 9 octobre.

### Commandes Wazuh — sur la VM Wazuh

Identifier les fichiers encore disponibles, y compris les rotations, dans
le conteneur manager :

```bash
sudo docker exec single-node-wazuh.manager-1 sh -c \
  'find /var/ossec/logs/archives /var/ossec/logs/alerts -type f -name "*.json*" -print'
```

**Toutes les sources de l’agent 001** pendant la reproduction, en UTC,
avec une marge jusqu’à 12:36 pour la réception :

```bash
sudo docker exec single-node-wazuh.manager-1 \
  cat /var/ossec/logs/archives/archives.json | jq -c '
  select(.agent.id == "001")
  | select(.timestamp >= "2026-10-09T12:33:13"
       and .timestamp < "2026-10-09T12:36:00")
  | {timestamp,agent,location,decoder,rule,data,full_log}'
```

Ici le filtre Docker de J9 est retiré : journald, auditd et autres sources
peuvent apparaître. Examiner `full_log` localement avant partage, car il peut
contenir des données internes. Ne pas afficher de secrets dans les pièces
publiées.

**Alertes de l’agent** dans la même fenêtre :

```bash
sudo docker exec single-node-wazuh.manager-1 \
  cat /var/ossec/logs/alerts/alerts.json | jq -c '
  select(.agent.id == "001")
  | select(.timestamp >= "2026-10-09T12:33:13"
       and .timestamp < "2026-10-09T12:36:00")
  | {timestamp,agent,location,decoder,rule,data,full_log}'
```

**Invocation initiale du script**, à distinguer de la reproduction hôte :

```bash
sudo docker exec single-node-wazuh.manager-1 \
  cat /var/ossec/logs/archives/archives.json | jq -c '
  select(.agent.id == "001")
  | select(.timestamp >= "2026-10-09T11:58:00"
       and .timestamp < "2026-10-09T12:07:30")
  | select(.location == "journald" or .location == "/var/log/audit/audit.log"
       or .location == "/var/log/dpkg.log")
  | {timestamp,agent,location,decoder,data,full_log}'
```

Si le fichier courant ne contient plus J9, utiliser le chemin retourné par
l’inventaire. Pour un JSON compressé, remplacer `cat <chemin>` par
`gzip -cd <chemin>` **dans docker exec**, puis garder le même filtre `jq`.
Ne pas déduire une absence passée d’une lecture du seul fichier courant.

### Autres sources — sur la VM File Browser

**Journald de reproduction**, avec bornes UTC explicites :

```bash
sudo journalctl --utc \
  --since '2026-10-09 12:33:13 UTC' --until '2026-10-09 12:36:00 UTC' \
  -o short-iso-precise --no-pager
```

**Contexte initial et service arrêté à 14:06:59 CEST** :

```bash
sudo journalctl --utc \
  --since '2026-10-09 11:58:00 UTC' --until '2026-10-09 12:07:30 UTC' \
  -o short-iso-precise --no-pager
```

Pour une vue ciblée SSH/Docker/agent, ajouter avant les bornes :
`-u ssh.service -u docker.service -u containerd.service -u wazuh-agent.service`.
Si un nom d’unité n’existe pas, conserver la lecture générale ; une sélection
d’unités trop étroite peut manquer le service concerné.

**Auditd original**, les heures étant affichées explicitement en UTC :

```bash
# Générer la date dans le format de la même locale que ausearch.
AUD_DATE=$(env TZ=UTC LC_ALL=C date -d '2026-10-09' '+%x')
printf 'Date audit : %s\n' "$AUD_DATE"
# Invocation initiale / événements de session.
sudo env TZ=UTC LC_ALL=C ausearch --input-logs \
  -ts "$AUD_DATE" 11:58:00 -te "$AUD_DATE" 12:07:30 -i
# Fenêtre de reproduction : ne pas présumer un audit de chaque GET.
sudo env TZ=UTC LC_ALL=C ausearch --input-logs \
  -ts "$AUD_DATE" 12:33:13 -te "$AUD_DATE" 12:36:00 -i
```

Le format dépend de la locale : le premier essai avec `10/09/2026`
a été rejeté par `ausearch` avant toute recherche. Générer la date avec
`date +%x` sous le même `LC_ALL=C` évite de présumer la longueur de
l’année. Cette erreur de syntaxe ne constitue pas un résultat sans événement.
Référence : [manuel du projet Linux Audit](https://github.com/linux-audit/audit-userspace/blob/master/docs/ausearch.8). Si `ausearch` n’est pas disponible,
ne pas installer un outil seulement pour remplir une preuve ; consulter
les objets auditd originaux déjà reçus dans Wazuh et noter la limite.

**Logs Docker** (recherche J9 déjà vide, à refaire uniquement si un nouveau
périmètre ou fichier justifie la lecture) :

```bash
sudo docker logs --timestamps \
  --since '2026-10-09T14:33:13+02:00' \
  --until '2026-10-09T14:35:39+02:00' filebrowser 2>&1
echo "Code Docker : $?"
```

Ces lectures portent sur les événements **conservés**. Aucun journal n’est
réactivé, aucun scénario relancé et aucun service redémarré. Fournir les
extraits utiles avec machine, commande et fenêtre ; indiquer explicitement
fichier absent, journal non conservé ou recherche sans résultat.

## 5. Ajouter les nouvelles lignes sans inventer

Les résultats J10 fournis sont consignés dans le tableau en tête de feuille.
Le tableau suivant reste disponible pour les prochains compléments.

| Heure | Source | Fait observé | Interprétation | Confiance |
| --- | --- | --- | --- | --- |
| | | | | |
| | | | | |
| | | | | |

Pour chaque ajout, conserver dans la pièce associée : commande/filtre,
fichier source, fenêtre/fuseau, objet ou capture, résultat et limite de
recherche. Une recherche vide peut être documentée comme résultat de recherche,
mais n’est pas un événement d’activité à dater comme une requête réseau.

- **Fait observé :** champ réellement lu ou résultat fourni, avec provenance.
- **Interprétation :** signification contextualisée ; ne pas confondre allowed et autorisation métier.
- **Hypothèse :** explication possible encore à vérifier, explicitement nommée.
- **Confiance :** élevée pour un fait référencé cohérent, moyenne/faible si rapprochement partiel, Non vérifiable si pièce indispensable manque.

Si les journaux ont disparu ou ne contiennent pas les événements utiles,
écrire le périmètre consulté et **Non disponible / Non vérifiable**, sans
remplacer la preuve passée par un nouveau test présenté comme ancien.

## 📦 Livrable attendu

Chronologie consolidée et nouvelles lignes justifiées, événements utilisés,
recherches sans résultat, limites de couverture et questions restantes.
La situation reste une analyse pédagogique en cours : ni incident réel ni
absence de conséquence ne sont certifiés par les seuls éléments disponibles.

- [État provisoire conservé pour J10](../it-9/qualifier-situation-preparer-suite.md)
- [Chronologie et pièces J9](../it-9/incident-premiers-elements.md)
- [Retour à l’itération 10](index.md)
- [Retour au module](../README.md)
