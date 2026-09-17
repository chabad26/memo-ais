# Plan réservé — Production des injects SUP-01 Autonomie 2

> **Diffusion restreinte : injecteur uniquement.** Ce fichier révèle les scénarios et les données attendues. Il n’est pas publié dans MkDocs et ne doit pas être remis au diagnostiqueur.

> **Décision pédagogique confirmée le 17 septembre 2026 :** le formateur autorise la simulation des incidents. Les métriques, journaux et comportements synthétiques sont donc recevables pour la mise en situation, à condition de les présenter comme simulés dans les traces de préparation et de conserver une relation cohérente entre le signal, la cause attendue et le retour à la normale.

## Objectif

Produire les dix situations du classeur `SUP-01_2_Injects_B.xlsx` sans prétendre qu’un signal existe tant que sa collecte, son alerte, ses journaux et son retour arrière n’ont pas été validés.

La procédure détaillée de déploiement se trouve dans [le runbook pas à pas](deployer-injects-step-by-step.md).

Le lab actuel fournit Prometheus, Grafana, Blackbox Exporter, Alertmanager, Elasticsearch, Logstash, Kibana, un endpoint Debian, un endpoint Windows Server Core, deux sondes HTTP, Filebeat/Winlogbeat et cinq règles d’alerte générales. Il ne fournit pas encore tous les services métier décrits par les injects.

## Matrice de faisabilité

| Nº | Inject | État avec le lab actuel | Mise en œuvre retenue ou adaptation nécessaire | Sources attendues | Limite de sécurité |
| ---: | --- | --- | --- | --- | --- |
| 11 | DNS progressivement indisponible | **Non disponible actuellement** | Déployer un DNS de laboratoire isolé et une sonde DNS Blackbox. Produire une saturation contrôlée ou une dégradation du service de test, sans modifier le DNS utilisé par les VM d’administration. | Résultat de sonde DNS, latence, disponibilité du processus, journaux DNS | Ne jamais remplacer le DNS principal du lab ; conserver un accès IP direct pour le retour arrière |
| 12 | Instabilité réseau | **Partiellement reproductible** | Utiliser une interface ou un chemin de test et `tc netem` pour produire pertes et latence. Adapter le signal initial à la perte/latence mesurée si les compteurs d’erreurs physiques ne progressent pas réellement. | Sonde, latence, pertes, métriques de l’interface, journaux réseau | Ne pas appliquer la perturbation à l’interface SSH d’administration sans console et minuterie de restauration |
| 13 | Pool DHCP épuisé | **Non disponible actuellement** | Créer un réseau virtuel isolé avec un serveur DHCP de test, un petit pool et un ou plusieurs clients jetables. Épuiser uniquement ce pool de laboratoire. | Baux disponibles, échecs DHCP, journaux du serveur et état des clients | Ne pas toucher au DHCP libvirt ou au réseau utilisé par les VM existantes |
| 14 | Certificat proche de l’expiration | **Facile après ajout d’un endpoint HTTPS** | Ajouter un service HTTPS de test avec un certificat court, puis collecter sa date d’expiration avec Blackbox. L’injection consiste à présenter le certificat prévu, pas à modifier un service réel. | `probe_ssl_earliest_cert_expiry`, sonde TLS, détails du certificat, journaux du service | Employer une CA et un nom réservés au lab ; ne jamais remplacer les certificats d’Elasticsearch ou de Logstash |
| 15 | Sauvegarde incomplète | **Non disponible actuellement** | Créer une sauvegarde de données fictives avec un manifeste attendu, un journal et une métrique Textfile Collector. Faire échouer une étape avant finalisation tout en laissant le service témoin disponible. | Statut du job, taille attendue/réelle, âge du dernier succès, journal de sauvegarde | Ne pas utiliser des données réelles et ne jamais supprimer le dernier jeu valide pour provoquer l’incident |
| 16 | Échecs d’authentification | **Journaux disponibles, service métier absent** | Utiliser une application ou un annuaire de test et des comptes fictifs. Produire des échecs contrôlés, puis exposer un compteur à Prometheus et les événements dans Kibana. | Taux d’échecs, ressources normales, journaux d’authentification, disponibilité de la dépendance | Ne pas viser les comptes d’administration et éviter tout verrouillage ou bannissement de l’accès au lab |
| 17 | Latence disque | **Métriques possibles, injection risquée sur le disque système** | Ajouter un disque virtuel de test et exécuter une charge d’E/S bornée sur un fichier jetable. Observer la latence du périphérique et celle d’une application témoin. | Temps d’E/S, latence applicative, CPU/mémoire témoins, journaux du traitement | Ne pas saturer le volume système, Elasticsearch ou les volumes Prometheus ; imposer durée, débit et taille maximum |
| 18 | Redémarrages d’un conteneur | **Service Compose présent, métrique de redémarrage à ajouter** | Déployer un conteneur applicatif jetable avec une erreur contrôlée et une politique de redémarrage. Ajouter cAdvisor ou un exporteur équivalent pour compter les redémarrages. | Compteur de redémarrages, état de l’hôte, disponibilité applicative, logs du conteneur | Ne pas utiliser Prometheus, Elasticsearch, Kibana ou un autre composant de supervision comme conteneur victime |
| 19 | Dépendance indisponible | **Très adapté à un mini-lab conteneurisé** | Déployer une application témoin et un backend séparé. Garder la page principale disponible tout en arrêtant uniquement la dépendance ; journaliser les échecs d’appel. | Sonde principale à 1, métrique/sonde de dépendance à 0, erreurs applicatives, état du backend | Cibler uniquement les deux services de test et préparer une commande de redémarrage du backend |
| 20 | Activité inhabituelle | **Collecte de sécurité disponible, détection à créer** | Générer un faible nombre d’échecs sur un compte ou une application de test, avec un seuil volontairement bas. Construire l’alerte à partir d’une métrique dérivée ou d’un compteur exposé. | Événements système/sécurité, compteur temporel, absence d’impact fonctionnel, cible concernée | Aucun test massif, aucun compte réel et aucune tentative vers une machine extérieure au lab |

## Conclusion de faisabilité

Avec l’autorisation de simuler, les dix injects peuvent être produits dans le lab sans reproduire chaque infrastructure réelle. **Aucun des dix n’est aujourd’hui complet de bout en bout** avec le signal exact du classeur : chaque simulation doit encore fournir sa métrique, son alerte, ses journaux, son déclenchement et son retour nominal. Les scénarios 14, 18 et 19 restent les plus proches d’un incident réel isolé. Les autres peuvent s’appuyer sur le simulateur commun afin d’éviter d’ajouter un vrai DHCP, de perturber le réseau d’administration ou de charger réellement le disque système.

Quand le mécanisme réel ne produit pas le signal annoncé, modifier le libellé de `T1` plutôt que fabriquer une preuve. Exemple : `tc netem` démontre une perte ou une latence réseau ; il ne démontre pas nécessairement une hausse des compteurs d’erreurs physiques de l’interface.

## Ordre de réalisation proposé

1. **Inject 19 — dépendance indisponible** : valide le modèle application, dépendance, sonde et logs.
2. **Inject 18 — redémarrage de conteneur** : ajoute l’observation des conteneurs.
3. **Inject 14 — certificat proche de l’expiration** : ajoute la sonde TLS.
4. **Inject 15 — sauvegarde incomplète** : ajoute métrique métier et journal de job.
5. **Inject 17 — latence disque** : nécessite le disque virtuel dédié.
6. **Inject 11 — DNS** : ajoute serveur et sonde DNS isolés.
7. **Inject 13 — DHCP** : ajoute le réseau virtuel isolé.
8. **Inject 16 — authentification** : ajoute le service d’authentification de test.
9. **Inject 20 — activité inhabituelle** : réutilise l’authentification et la détection temporelle.
10. **Inject 12 — instabilité réseau** : à terminer avec console disponible et restauration automatique.

Cet ordre mutualise les composants : l’application créée pour l’inject 19 peut fournir la dépendance, l’authentification et les journaux des injects 16 et 20.

## Contrat de validation d’un inject

Un inject est déclaré prêt seulement si les huit points suivants ont été testés :

- état nominal mesuré avant l’action ;
- commande d’injection ciblée et reproductible ;
- signal `T1` réellement observable ;
- métrique et sonde exploitables pendant l’incident ;
- événement ou journal utile au diagnostic ;
- règle passant effectivement par `pending`, puis `firing` si cette transition est attendue ;
- retour arrière testé ;
- retour nominal démontré avec notification `resolved` et période de stabilité.

Pour chaque scénario, conserver deux dossiers séparés : un dossier **injecteur** contenant la cause, la commande et le retour arrière, puis un dossier **diagnostiqueur** contenant seulement `T1` et les accès aux outils.

## Suivi de production

| Nº | Composant ajouté | Nom de l’alerte | Nominal validé | Injection validée | Retour arrière validé | Captures | Prêt pour passation |
| ---: | --- | --- | :---: | :---: | :---: | :---: | :---: |
| 11 |  |  | ☐ | ☐ | ☐ | ☐ | ☐ |
| 12 |  |  | ☐ | ☐ | ☐ | ☐ | ☐ |
| 13 |  |  | ☐ | ☐ | ☐ | ☐ | ☐ |
| 14 |  |  | ☐ | ☐ | ☐ | ☐ | ☐ |
| 15 |  |  | ☐ | ☐ | ☐ | ☐ | ☐ |
| 16 |  |  | ☐ | ☐ | ☐ | ☐ | ☐ |
| 17 |  |  | ☐ | ☐ | ☐ | ☐ | ☐ |
| 18 |  |  | ☐ | ☐ | ☐ | ☐ | ☐ |
| 19 |  |  | ☐ | ☐ | ☐ | ☐ | ☐ |
| 20 |  |  | ☐ | ☐ | ☐ | ☐ | ☐ |
