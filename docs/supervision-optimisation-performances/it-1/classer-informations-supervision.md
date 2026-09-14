# Classer les informations de supervision selon leur utilisation

## Objectif

Distinguer les informations qui permettent d'observer un état, de mesurer une performance et de rechercher la cause d'un problème, puis définir un socle minimal de collecte pour les serveurs Linux et Windows.

## Travail demandé

Vous disposez de plusieurs sources d'information :

- métriques système ;
- état des services ;
- disponibilité réseau ;
- journaux système ;
- journaux applicatifs.

Classez-les selon leur utilisation. À partir du tableau, définissez les informations minimales que vous souhaiteriez obtenir automatiquement pour un serveur Linux et un serveur Windows.

## Trois usages complémentaires

- **Observer l'état** : savoir si un élément fonctionne et connaître sa situation actuelle.
- **Mesurer une performance** : quantifier une utilisation, un débit ou un délai et suivre son évolution.
- **Rechercher une cause** : croiser les observations pour expliquer un dysfonctionnement.

Une même information peut servir à plusieurs usages. Une métrique élevée signale une situation à examiner ; elle ne prouve pas, à elle seule, la cause du problème.

## Tableau complété — proposition de classement

| Information | Observer l'état | Mesurer une performance | Rechercher une cause |
| --- | --- | --- | --- |
| CPU | Oui : niveau d'utilisation actuel. | Oui : utilisation dans le temps et durée des pics de charge. | En complément : rapprocher une charge élevée des processus actifs et des événements. |
| RAM | Oui : mémoire disponible et utilisée. | Oui : évolution de la consommation et activité de swap ou de pagination. | En complément : rechercher une pression mémoire et les processus concernés. |
| Stockage | Oui : espace libre et état des volumes. | Oui : débit, latence des entrées/sorties et évolution de l'occupation. | En complément : distinguer manque d'espace, lenteurs et erreurs à l'aide des journaux. |
| Disponibilité | Oui : réponse ou absence de réponse au contrôle effectué. | Selon le contrôle : temps de réponse, pertes réseau et taux de disponibilité sur une période. | En complément : situer le début d'une interruption et comparer les contrôles réseau et applicatifs. |
| État d'un service | Oui : actif, arrêté ou en échec. | Pas seul : l'état actif/arrêté ne mesure ni débit ni temps de réponse. | En complément : repérer un arrêt ou un redémarrage, puis consulter les journaux. |
| Journal système | En complément : événements de démarrage, d'arrêt ou d'erreur ; à recouper avec l'état actuel. | Selon le contenu : calculer des fréquences d'événements ou exploiter des durées enregistrées. | Oui : rechercher les erreurs système, les échecs de services et leur chronologie. |
| Journal applicatif | En complément : activité et erreurs de l'application ; à recouper avec un test fonctionnel. | Selon le contenu : temps de traitement, volume de requêtes et taux d'erreur calculés. | Oui : rechercher les messages d'erreur et le contexte des opérations en échec. |

!!! note "Interpréter les données"
    Un service actif peut mal répondre, et une machine qui répond au ping peut héberger une application indisponible. De même, l'absence d'erreurs dans les journaux ne garantit pas un fonctionnement normal : la collecte peut être interrompue ou les événements utiles ne pas être journalisés.

## Réutilisation — informations minimales à obtenir automatiquement

Dans le laboratoire sur laptop géré avec **virt-manager**, ce socle concerne la **VM Debian** et la **VM Windows Server**. Il décrit la collecte souhaitée ; sa mise en place et son fonctionnement restent à vérifier. Le choix d'une éventuelle VM dédiée à la supervision reste ouvert.

| Besoin minimal | Serveur Linux — Debian | Serveur Windows Server |
| --- | --- | --- |
| Identifier la source et la fraîcheur | Nom de la machine, horodatage de la dernière mesure et état de la collecte. | Nom de la machine, horodatage de la dernière mesure et état de la collecte. |
| Vérifier la disponibilité | Résultat et heure du dernier contrôle réseau, complétés par un test du service attendu. | Résultat et heure du dernier contrôle réseau, complétés par un test du service attendu. |
| Suivre le CPU | Pourcentage d'utilisation et évolution dans le temps. | Pourcentage d'utilisation et évolution dans le temps. |
| Suivre la mémoire | Mémoire disponible, utilisation et activité du swap. | Mémoire disponible, utilisation et activité de pagination. |
| Suivre le stockage | Espace libre en volume et en pourcentage par système de fichiers, inodes libres et latence des entrées/sorties. | Espace libre en volume et en pourcentage par volume, et latence des entrées/sorties. |
| Contrôler les services essentiels | État des services retenus dans l'inventaire et résultat d'un contrôle de leur fonctionnement. | État des services retenus dans l'inventaire et résultat d'un contrôle de leur fonctionnement. |
| Retrouver les événements système | Événements du journal système : erreurs, arrêts, démarrages et échecs des services surveillés. | Événements du journal Système de l'Observateur d'événements : erreurs, arrêts, démarrages et échecs des services surveillés. |
| Retrouver les événements applicatifs | Journaux des applications effectivement installées, notamment erreurs et opérations en échec. | Journal Application et journaux propres aux applications effectivement installées, notamment erreurs et opérations en échec. |

Pour les journaux, conserver au minimum **la date et l'heure, la machine, le service ou l'application, le niveau de gravité lorsqu'il existe et le message**. Des horloges synchronisées facilitent la comparaison des événements entre les deux serveurs.

Les noms exacts des services et des applications seront complétés après inventaire. L'historique des métriques doit permettre de comparer la situation actuelle à celle qui précédait l'incident.

### Première vue d'exploitation attendue

Pour chaque serveur, afficher en priorité la disponibilité, la fraîcheur des données, les ressources sous pression, les services en échec et les erreurs récentes. Prévoir un accès aux courbes et aux journaux pour approfondir le diagnostic.

Le laptop hébergeant les deux VM, ses ressources devront également être prises en compte lors d'un diagnostic : un manque de mémoire ou une saturation du stockage de l'hôte peut affecter plusieurs invités simultanément.

## À consigner dans le dossier de déploiement

- Le classement retenu et les raisons des choix.
- La liste réelle des services et applications à surveiller sur chaque VM.
- Pour chaque information : la source, la fréquence configurée et la durée de conservation retenue.
- Une vérification datée de la remontée des données et les éventuelles limites de collecte.

Cette feuille définit les besoins. Les résultats et captures seront ajoutés après les vérifications réelles, sans présenter une collecte prévue comme déjà opérationnelle.

[Retour au sommaire de l'itération](index.md)
