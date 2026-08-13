# Construire un réseau isolé OVH à la main

!!! info "Atelier manuel avant automatisation"
    Cette feuille se fait volontairement **à la main** dans OVHcloud /
    Horizon ou avec la CLI OpenStack. Le but est de comprendre les ressources
    avant de les décrire plus tard avec OpenTofu.

## Objectif

Construire un petit réseau privé isolé avec une VM Ubuntu 24.04 accessible en
SSH, en appliquant le principe de moindre exposition réseau.

À la fin de l'atelier, tu dois pouvoir prouver :

- qu'un réseau privé et un sous-réseau existent ;
- qu'une instance Ubuntu 24.04 est raccordée à ce sous-réseau ;
- que le SSH est autorisé uniquement depuis ton IP publique ;
- que le HTTP est autorisé depuis Internet ;
- que l'adresse IP privée attribuée à la VM est vérifiée depuis la VM ;
- qu'une seconde VM peut communiquer en interne sans passer par l'IP publique.

## Pourquoi le faire à la main

Avant d'automatiser une infrastructure, il faut créer une première fois les
ressources manuellement pour comprendre ce que chaque objet apporte réellement.
C'est le même réflexe qu'en **RES-01a** ou **SYS-01a** : on observe d'abord, on
standardise ensuite.

Ici, le point important n'est pas seulement de démarrer une VM. Il faut
comprendre la chaîne complète :

| Ressource | Rôle |
| --- | --- |
| Réseau privé | Isole les communications internes du prototype. |
| Sous-réseau | Définit le plan d'adressage privé attribué aux VM. |
| Instance | Porte le système Ubuntu 24.04 à administrer. |
| Security group | Filtre les flux entrants autorisés vers les instances. |
| IP publique | Sert uniquement au point d'entrée SSH ou HTTP exposé. |
| IP privée | Sert aux communications internes entre VM. |

## Hypothèses de travail

| Élément | Choix retenu |
| --- | --- |
| Fournisseur | OVHcloud Public Cloud |
| Interface | Horizon ou CLI OpenStack |
| Région | À choisir dans le projet OVHcloud et à noter dans les preuves |
| Réseau privé | `dist01b-lab-net` |
| Sous-réseau | `dist01b-lab-subnet` |
| Plan d'adressage | `10.42.10.0/24` |
| Passerelle | `10.42.10.1` |
| Instance 1 | `dist01b-web-01` |
| Instance 2 optionnelle | `dist01b-web-02` |
| Image | Ubuntu 24.04 LTS |
| Accès admin | SSH par clé uniquement |

!!! warning "Coût et nettoyage"
    Une instance cloud peut générer des coûts tant qu'elle existe. À la fin du
    TP, supprimer les ressources inutiles ou noter explicitement qu'elles
    restent actives pour la suite.

!!! danger "Secrets"
    Ne jamais capturer ni publier de clé privée SSH, mot de passe, token OVH,
    fichier `openrc.sh` complet, application key, application secret ou
    consumer key.

## Référence OVH à vérifier avant de créer les règles

La documentation OVHcloud sur les security groups Horizon précise qu'il faut
créer un security group dédié, éviter de modifier le groupe `default`, puis
ajouter les règles depuis `Manage Rules` / `+ Add Rule`.

La documentation OVHcloud sur les règles réseau avec OpenStack CLI rappelle le
même principe : pour une configuration spécifique, créer un nouveau security
group, puis l'associer au port réseau ou à l'instance.

Sources consultées le 13 août 2026 :

- [OVHcloud - Creating and configuring a security group in Horizon](https://docs.ovhcloud.com/en/guides/public-cloud/compute/setup-security-group/)
- [OVHcloud - Managing firewall rules and port security on networks using OpenStack CLI](https://docs.ovhcloud.com/en/guides/public-cloud/cross-functional/security-group-private-network/)

## Étape 1 - Relever ton IP publique

Depuis ton poste :

```bash
curl -4 ifconfig.me
```

Noter le résultat sous forme CIDR :

```text
MON_IP_PUBLIQUE/32
```

Exemple fictif :

```text
203.0.113.10/32
```

!!! warning "Adresse IP"
    L'adresse ci-dessus est un exemple documentaire. Remplace-la par ton IP
    publique réelle au moment du TP.

Preuve à conserver :

| Preuve | Attendu |
| --- | --- |
| IP source SSH | IP publique masquée partiellement, par exemple `203.0.113.xxx/32`. |

## Étape 2 - Créer le réseau privé

Dans Horizon :

1. ouvrir `Network` ;
2. aller dans `Networks` ;
3. créer un réseau nommé `dist01b-lab-net` ;
4. créer le sous-réseau `dist01b-lab-subnet` ;
5. utiliser le CIDR `10.42.10.0/24` ;
6. garder `10.42.10.1` comme passerelle si l'interface le propose.

Équivalent CLI OpenStack :

```bash
openstack network create dist01b-lab-net

openstack subnet create dist01b-lab-subnet \
  --network dist01b-lab-net \
  --subnet-range 10.42.10.0/24 \
  --gateway 10.42.10.1
```

Vérifier :

```bash
openstack network list
openstack subnet show dist01b-lab-subnet
```

Preuves à conserver :

| Preuve | Commande ou capture |
| --- | --- |
| Réseau créé | `openstack network list` ou capture Horizon. |
| Sous-réseau créé | `openstack subnet show dist01b-lab-subnet`. |
| Plan d'adressage | CIDR `10.42.10.0/24` visible. |

## Étape 3 - Créer un security group minimal

Créer un groupe dédié :

```bash
openstack security group create dist01b-web-sg \
  --description "SSH limite a mon IP et HTTP public pour le prototype DIST01b"
```

Ajouter SSH uniquement depuis ton IP :

```bash
openstack security group rule create dist01b-web-sg \
  --protocol tcp \
  --dst-port 22 \
  --remote-ip MON_IP_PUBLIQUE/32
```

Ajouter HTTP depuis Internet :

```bash
openstack security group rule create dist01b-web-sg \
  --protocol tcp \
  --dst-port 80 \
  --remote-ip 0.0.0.0/0
```

Autoriser ICMP en interne pour le test entre VM :

```bash
openstack security group rule create dist01b-web-sg \
  --protocol icmp \
  --remote-ip 10.42.10.0/24
```

Autoriser SSH interne entre VM uniquement dans le sous-réseau :

```bash
openstack security group rule create dist01b-web-sg \
  --protocol tcp \
  --dst-port 22 \
  --remote-ip 10.42.10.0/24
```

Vérifier les règles :

```bash
openstack security group rule list dist01b-web-sg
```

État attendu :

| Flux | Source | Destination | Décision |
| --- | --- | --- | --- |
| SSH | Ton IP publique `/32` | TCP 22 | Autorisé |
| SSH | Internet entier | TCP 22 | Refusé |
| HTTP | `0.0.0.0/0` | TCP 80 | Autorisé |
| ICMP interne | `10.42.10.0/24` | ICMP | Autorisé |
| SSH interne | `10.42.10.0/24` | TCP 22 | Autorisé |

!!! note "Moindre exposition"
    Le port 22 ne doit jamais être ouvert en `0.0.0.0/0` pour cet atelier.
    L'administration vient de ton IP uniquement. La communication entre VM
    passe par les IP privées.

## Étape 4 - Créer l'instance Ubuntu 24.04

Créer une instance nommée `dist01b-web-01` avec :

- image `Ubuntu 24.04` ou nom équivalent disponible dans la région ;
- un flavor économique adapté au TP ;
- la clé SSH publique du poste d'administration ;
- le réseau `dist01b-lab-net` ;
- le security group `dist01b-web-sg`.

Exemple CLI à adapter selon les noms réels disponibles :

```bash
openstack server create dist01b-web-01 \
  --image "Ubuntu 24.04" \
  --flavor d2-4 \
  --key-name admin-dist01b \
  --network dist01b-lab-net \
  --security-group dist01b-web-sg
```

Vérifier l'état :

```bash
openstack server list
openstack server show dist01b-web-01
```

Preuves à conserver :

| Preuve | Attendu |
| --- | --- |
| Instance active | État `ACTIVE`. |
| Image | Ubuntu 24.04 visible ou documentée. |
| Réseau | Rattachement à `dist01b-lab-net`. |
| Security group | `dist01b-web-sg` associé. |

## Étape 5 - Se connecter en SSH

Repérer l'IP publique de l'instance dans Horizon ou avec :

```bash
openstack server show dist01b-web-01
```

Se connecter :

```bash
ssh ubuntu@IP_PUBLIQUE_INSTANCE
```

Si l'image utilise un autre utilisateur par défaut, tester le nom indiqué par
OVHcloud pour l'image.

Vérifier l'adresse IP attribuée depuis la VM :

```bash
hostname
ip -br addr
ip route
```

Résultat attendu :

```text
dist01b-web-01
ens3             UP             10.42.10.x/24 ...
default via 10.42.10.1 ...
```

Preuves à conserver :

| Preuve | Commande |
| --- | --- |
| Connexion SSH réussie | Capture du prompt sans secret. |
| IP privée attribuée | `ip -br addr`. |
| Route par défaut | `ip route`. |

## Étape 6 - Vérifier l'exposition minimale

Depuis ton poste :

```bash
ssh ubuntu@IP_PUBLIQUE_INSTANCE
curl -I http://IP_PUBLIQUE_INSTANCE
```

Le SSH doit fonctionner depuis ton IP. HTTP peut répondre seulement si un
service web est installé. Si aucun serveur HTTP n'est actif, le filtrage réseau
peut être correct même si `curl` échoue avec une connexion refusée.

Pour tester HTTP rapidement sur la VM :

```bash
sudo apt update
sudo apt install -y nginx
systemctl status nginx --no-pager
```

Puis depuis ton poste :

```bash
curl -I http://IP_PUBLIQUE_INSTANCE
```

Preuves à conserver :

| Test | Résultat attendu |
| --- | --- |
| SSH depuis ton IP | Connexion autorisée. |
| HTTP depuis Internet | Réponse HTTP si Nginx est installé. |
| SSH ouvert à tous | Absence de règle `0.0.0.0/0` sur TCP 22. |

## Pour aller plus loin - Ajouter une seconde instance

Créer une seconde instance dans le même sous-réseau :

```bash
openstack server create dist01b-web-02 \
  --image "Ubuntu 24.04" \
  --flavor d2-4 \
  --key-name admin-dist01b \
  --network dist01b-lab-net \
  --security-group dist01b-web-sg
```

Depuis `dist01b-web-01`, repérer l'IP privée de `dist01b-web-02` :

```bash
openstack server list
```

Puis tester sans utiliser l'IP publique :

```bash
ping -c 4 IP_PRIVEE_WEB_02
ssh ubuntu@IP_PRIVEE_WEB_02
```

Résultat attendu :

| Test | Attendu |
| --- | --- |
| `ping IP_PRIVEE_WEB_02` | Réponse depuis `10.42.10.x`. |
| `ssh ubuntu@IP_PRIVEE_WEB_02` | Connexion interne possible si la clé est autorisée. |
| Chemin réseau | Communication par IP privée, pas par IP publique. |

!!! tip "Lecture sécurité"
    Si deux VM doivent échanger en interne, la règle doit viser le sous-réseau
    privé ou un security group interne. Il ne faut pas ouvrir davantage
    l'administration publique pour compenser un problème de communication
    privée.

## Tableau de validation

| Point de contrôle | Statut | Preuve |
| --- | --- | --- |
| Réseau privé créé | À compléter | Capture Horizon ou `openstack network list`. |
| Sous-réseau `10.42.10.0/24` créé | À compléter | `openstack subnet show dist01b-lab-subnet`. |
| Security group dédié créé | À compléter | `openstack security group list`. |
| SSH limité à ton IP | À compléter | `openstack security group rule list dist01b-web-sg`. |
| HTTP public autorisé | À compléter | Règle TCP 80 depuis `0.0.0.0/0`. |
| Instance Ubuntu 24.04 active | À compléter | `openstack server show dist01b-web-01`. |
| IP privée vérifiée dans la VM | À compléter | `ip -br addr`. |
| Communication interne testée | À compléter | `ping` ou SSH privé vers `dist01b-web-02`. |

## Nettoyage ou conservation

Si le TP s'arrête ici, supprimer les ressources dans l'ordre :

```bash
openstack server delete dist01b-web-02
openstack server delete dist01b-web-01
openstack security group delete dist01b-web-sg
openstack subnet delete dist01b-lab-subnet
openstack network delete dist01b-lab-net
```

Si les ressources sont conservées pour l'automatisation, noter :

- la date ;
- la région ;
- les noms exacts ;
- les IP publiques et privées partiellement masquées ;
- le coût estimé ;
- la raison de conservation.

## Trace de réalisation

À compléter après manipulation :

| Élément | Valeur réelle |
| --- | --- |
| Date du TP | À compléter |
| Région OVHcloud | À compléter |
| IP publique source SSH | À compléter |
| Réseau privé | `dist01b-lab-net` |
| Sous-réseau | `10.42.10.0/24` |
| Instance 1 | `dist01b-web-01` |
| IP privée instance 1 | À compléter |
| IP publique instance 1 | À compléter |
| Instance 2 | `dist01b-web-02` ou non créée |
| IP privée instance 2 | À compléter |
| Écart rencontré | À compléter |
