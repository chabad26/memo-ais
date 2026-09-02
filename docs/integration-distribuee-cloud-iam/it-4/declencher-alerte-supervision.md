# Déclencher une alerte de supervision

!!! info "Fiche d'exploitation"
    Cette feuille décrit la mise en place d'un dashboard et d'une alerte
    proactive. Comme les VM d'exercice OVHcloud et Infomaniak ont été détruites
    après validation, cette procédure est à rejouer lors d'un prochain
    déploiement. Ne pas présenter ces étapes comme exécutées tant qu'une
    nouvelle VM active n'existe pas.

## Objectif

Détecter un problème avant qu'un utilisateur ne s'en plaigne.

Une supervision utile ne se limite pas à regarder un tableau de bord quand un
incident est déjà visible. Elle doit mesurer les ressources, déclencher une
alerte sur dépassement de seuil et vérifier que la notification arrive
réellement.

## Ce que tu vas faire, et pourquoi

| Action | Pourquoi |
| --- | --- |
| Créer un dashboard CPU et réseau. | Visualiser l'état de base des instances. |
| Définir une alerte de seuil. | Détecter une surcharge avant plainte utilisateur. |
| Provoquer volontairement une charge CPU. | Prouver que l'alerte fonctionne vraiment. |
| Vérifier la notification. | Valider la chaîne complète : mesure, seuil, déclenchement, réception. |
| Ajouter une alerte de coût. | Relier exploitation technique et réflexe FinOps. |

## Pré-requis

| Élément | Attendu |
| --- | --- |
| Instance active | Une VM OVHcloud ou Infomaniak disponible pour le test. |
| Accès SSH | Connexion administrateur fonctionnelle. |
| Supervision | Dashboard fournisseur, métriques OpenStack ou outil Prometheus/Grafana disponible. |
| Notification | Adresse mail, webhook ou canal de test configuré. |
| Limite FinOps | Seuil de coût ou de consommation défini avant le test. |

!!! warning "État actuel"
    Aucune VM du module n'est actuellement active. La preuve finale attendue
    pour cette fiche ne peut donc pas être produite maintenant. Les commandes
    ci-dessous sont à conserver pour le prochain déploiement temporaire.

## Étape 1 - Créer le dashboard

Dans la console du fournisseur ou l'outil de supervision retenu, créer une vue
avec au minimum :

| Panneau | Métrique | Intérêt |
| --- | --- | --- |
| CPU | utilisation moyenne ou maximale | Détecter une surcharge de calcul. |
| Réseau entrant | octets ou paquets reçus | Repérer trafic inhabituel ou pic de charge. |
| Réseau sortant | octets ou paquets envoyés | Repérer transfert anormal ou effet d'une attaque. |
| Disque | lecture, écriture ou espace utilisé | Détecter saturation ou activité excessive. |
| État instance | active, arrêtée, supprimée | Vérifier que la ressource surveillée existe encore. |

Pour OVHcloud, la documentation Public Cloud indique que les métriques peuvent
inclure CPU, mémoire, stockage, réseau et latence, et qu'elles peuvent servir à
des dashboards, seuils et alertes.

Pour Infomaniak, le socle OpenStack expose des métriques et services de
facturation/suivi via Ceilometer, Gnocchi et CloudKitty. Les alarmes sont
portées par Aodh lorsque le service est disponible dans le projet.

### Diagnostic réel Infomaniak

Le `02/09/2026`, le catalogue OpenStack du projet Infomaniak expose bien les
services suivants :

| Service | Type | Rôle |
| --- | --- | --- |
| `gnocchi` | `metric` | stockage et consultation de métriques |
| `ceilometer` | `metering` | collecte ou comptage d'usage |
| `aodh` | `alarming` | alarmes OpenStack |
| `cloudkitty` | `rating` | consommation et valorisation FinOps |

Le diagnostic montre aussi deux limites :

| Commande | Résultat | Interprétation |
| --- | --- | --- |
| `openstack endpoint list` | erreur `403 Forbidden` | le compte projet n'a pas le droit de lister tous les endpoints Keystone |
| `openstack metric resource list` | sous-commande inconnue | le client Gnocchi n'est pas installé ou pas chargé dans le CLI |

Ce n'est donc pas Horizon qui "cache" forcément un menu évident. Les services
existent côté catalogue, mais leur exploitation demande les bons clients CLI et
les droits disponibles dans le projet.

Après installation du client Gnocchi, `openstack metric resource list`
fonctionne. La sortie liste les ressources suivies par la plateforme :
`instance`, `instance_disk`, `instance_network_interface`, `public_ip` et
`swift_account`.

Pour lire cette table :

| Colonne | Lecture |
| --- | --- |
| `type` | nature de la ressource mesurée |
| `original_resource_id` | identifiant de la ressource côté OpenStack |
| `started_at` | début de suivi de la ressource |
| `ended_at` | fin de suivi ; `None` signifie que la ressource est encore active ou encore vue par Gnocchi |

Cette sortie devient une preuve utile : elle montre que la métrique cloud
native est accessible en CLI, même si aucun dashboard Horizon dédié n'est
visible.

Une seconde validation confirme que les métriques détaillées sont listables :

| Commande | Résultat constaté | Lecture |
| --- | --- | --- |
| `openstack metric list` | métriques `cpu`, `memory`, `memory.usage`, `network.incoming.bytes`, `network.outgoing.bytes`, `disk.device.*` | Gnocchi expose bien les métriques de base des instances. |
| `cloudkitty module list` | modules `hashmap` et `noop` actifs, `pyscripts` inactif | Le service de rating/FinOps répond. |
| `openstack alarm list` | aucune ligne retournée | Aucune alerte Aodh n'est encore configurée dans le projet. |

Point important : la métrique `cpu` est exposée en `ns` et non directement en
pourcentage. Pour une alerte pédagogique `CPU > 80 %`, il faut soit une
formule/agrégation adaptée côté Aodh ou Gnocchi, soit utiliser une supervision
système temporaire sur la VM pour produire une preuve simple pendant le test
`stress-ng`.

Autre piège : la colonne `granularity` indique la période d'agrégation. Une
granularité `300.0` correspond à un point toutes les 5 minutes. Si la commande
`openstack metric measures show ID_METRIQUE_CPU` est relancée plusieurs fois
dans la même fenêtre de 5 minutes, la sortie peut sembler identique. Ce n'est
pas forcément un échec du test : il faut attendre le point suivant ou comparer
deux points horodatés.

Exemple de lecture :

| Timestamp | Granularité | Valeur CPU |
| --- | ---: | ---: |
| `15:50` | `300.0` | `96990000000.0 ns` |
| `15:55` | `300.0` | `105620000000.0 ns` |

La différence existe, mais elle se lit entre deux points de 5 minutes :

```text
105620000000 - 96990000000 = 8630000000 ns
```

Pour une preuve plus lisible pendant l'exercice, conserver en parallèle une
capture `htop` ou `top` sur la VM pendant l'exécution de `stress-ng`.

![Charge CPU stress-ng et métrique Gnocchi](../../assets/img/integration-distribuee-cloud-iam/it-4/Capture%20d’écran%20du%202026-09-02%2016-09-00.png)

_La capture montre la VM `dist01b-infomaniak` en cours de test : deux processus
`stress-ng-cpu` consomment environ 100 % CPU chacun dans `top`, tandis que la
commande Gnocchi affiche un nouveau point CPU à `16:00`. La valeur passe de
`105620000000 ns` à `341860000000 ns`, soit une hausse de `236240000000 ns` sur
la fenêtre observée._

## Étape 2 - Créer l'alerte CPU

Créer une règle simple :

| Paramètre | Valeur pédagogique |
| --- | --- |
| Ressource | VM de test |
| Métrique | CPU |
| Seuil | supérieur à 80 % |
| Durée | 5 minutes dans le cours, 2 minutes possibles en lab court |
| Notification | mail ou canal de test |
| Gravité | warning |

Si l'outil ne permet pas une alerte native sur CPU, documenter la limite et
utiliser une alternative : Prometheus + Alertmanager, Grafana alerting ou
alarme OpenStack Aodh.

## Étape 3 - Provoquer volontairement la charge

Installer d'abord l'outil de stress sur la VM :

```bash
sudo apt update
sudo apt install -y stress-ng
```

Lancer ensuite une charge CPU contrôlée :

```bash
stress-ng --cpu 2 --timeout 300s --metrics-brief
```

Pour un test plus court en formation :

```bash
stress-ng --cpu 2 --timeout 120s --metrics-brief
```

Pendant le test, garder le dashboard ouvert et vérifier que la courbe CPU
monte. Attendre ensuite le déclenchement de l'alerte.

!!! danger "Charge volontaire"
    Ne jamais lancer ce test sur une machine de production sans accord. La
    charge CPU est volontaire et peut dégrader un service réel.

## Étape 4 - Vérifier la notification

Conserver les preuves suivantes :

| Preuve | Contenu attendu |
| --- | --- |
| Dashboard avant test | CPU normal, instance identifiée. |
| Dashboard pendant test | CPU au-dessus du seuil. |
| Configuration d'alerte | Métrique, seuil, durée, canal de notification. |
| Notification reçue | Mail, webhook ou message de test. |
| Retour à la normale | CPU redescendu après arrêt de `stress-ng`. |

Noter aussi l'heure de début du test, l'heure de déclenchement et le délai de
notification.

## Commandes OpenStack utiles

Lister les instances et vérifier l'identifiant de la VM :

```bash
export OS_CLOUD=PROFIL_OPENSTACK
openstack server list
openstack server show NOM_OU_ID
```

Contrôler les services exposés sans nécessiter le droit administrateur
`identity:list_endpoints` :

```bash
openstack catalog list
openstack catalog list | grep -Ei 'metric|gnocchi|ceilometer|aodh|alarm|cloudkitty|rating'
```

Installer les clients nécessaires si les commandes `metric` ou `alarm` sont
absentes. Sur Ubuntu récent, `pip --user` peut être bloqué par le mécanisme
`externally-managed-environment` : utiliser alors les paquets Debian ou un
environnement virtuel.

Option paquets Debian :

```bash
sudo apt update
sudo apt install -y \
  python3-openstackclient \
  python3-gnocchiclient \
  python3-aodhclient \
  python3-cloudkittyclient
```

Option environnement virtuel local :

```bash
sudo apt install -y python3-venv
cd ~/cloud-iam
python3 -m venv .venv-openstack
source .venv-openstack/bin/activate
python -m pip install -U pip
python -m pip install python-openstackclient gnocchiclient aodhclient python-cloudkittyclient
```

Ouvrir un nouveau terminal ou recharger le `PATH`, puis tester :

```bash
openstack metric resource list
openstack metric list
openstack alarm list
cloudkitty module list
```

Si les clients sont installés mais que les commandes échouent encore, conserver
la sortie comme preuve de limite fournisseur/projet et basculer sur une
supervision système temporaire de la VM pour le test `stress-ng`.

Pour explorer les métriques d'une ressource précise :

```bash
openstack metric resource show ID_RESSOURCE
openstack metric measures show ID_METRIQUE
```

Pour filtrer les métriques utiles au test :

```bash
openstack metric list | grep -E ' cpu |memory.usage|network.incoming.bytes|network.outgoing.bytes'
```

## Pour aller plus loin - alerte de coût

Ajouter une alerte de coût ou de consommation permet de détecter une dérive
avant la facture.

| Contrôle FinOps | Seuil possible | Réaction |
| --- | --- | --- |
| Coût mensuel estimé | supérieur à `20 EUR` sur le lab | Vérifier VM, volumes, IP et snapshots. |
| CPU hours | hausse imprévue | Chercher une instance oubliée. |
| Disk GB-hours | hausse imprévue | Chercher volume détaché ou snapshot ancien. |
| Floating IP | ressource encore présente après clôture | Supprimer si non documentée. |

Sur Infomaniak, CloudKitty sert au suivi de consommation et de facturation du
projet. Si une alerte budget native n'est pas disponible dans l'interface, on
peut conserver un contrôle planifié : interrogation régulière de la
consommation, comparaison avec un seuil, puis notification.

Exemple de logique à documenter :

```text
si consommation_estimee > seuil_budget
alors notifier l'administrateur
et lancer l'audit des ressources résiduelles
```

Le script d'audit FinOps déjà créé peut compléter cette alerte :

```bash
docs/assets/scripts/integration-distribuee-cloud-iam/it-4/audit-ressources-orphelines.sh \
  openstack PROFIL_OPENSTACK
```

## État final attendu

À la fin de cette feuille, quand une VM de test existe :

- un dashboard affiche CPU et réseau ;
- une alerte de seuil est configurée ;
- la charge CPU est provoquée avec `stress-ng` ;
- la notification est reçue et conservée comme preuve ;
- le retour à la normale est vérifié ;
- une piste d'alerte budget ou de suivi de consommation est documentée.

Dans l'état actuel du module :

- la procédure est prête à rejouer ;
- aucune notification réelle n'est inventée ;
- la destruction des VM explique pourquoi le test n'est pas exécutable maintenant.

## Ressources

- [OVHcloud - Understanding metrics in OVHcloud Public Cloud](https://docs.ovhcloud.com/en/guides/public-cloud/cross-functional/metrics-informations)
- [Infomaniak - Billing, Metering and Rating](https://docs.infomaniak.cloud/metering/billing/)
- [Infomaniak - AODH Policies](https://docs.infomaniak.cloud/identity/policies/aodh/)
- [Infomaniak - CloudKitty Policies](https://docs.infomaniak.cloud/identity/policies/cloud-kitty/)
