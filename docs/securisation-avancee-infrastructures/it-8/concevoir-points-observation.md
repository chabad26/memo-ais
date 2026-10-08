# Concevoir les différents points d’observation

**Itération 8 — 8 octobre 2026 — Travail individuel**

## 🎯 Objectif et état du dispositif

Comparer les informations apportées par Suricata sur la machine hôte et par
un agent Wazuh dans l’environnement applicatif de File Browser.
**Suricata est documenté par les captures précédentes ; l’agent dans le
conteneur et la centralisation Wazuh constituent ici une architecture cible,
pas une installation vérifiée.**

## 1. Architecture cible

```text
                         Réseau extérieur
                                |
                    +-----------v-----------+
                    | Machine hôte          |
                    | Suricata sur virbr0   |
                    | eve.json              |
                    +-----------+-----------+
                                | trafic visible de la VM
                    +-----------v-----------+
                    | VM hébergeant Docker  |
                    | 192.168.122.229       |
                    | +-------------------+ |
                    | | File Browser      | |
                    | | Agent Wazuh cible | |
                    | | dans le conteneur | |
                    | +---------+---------+ |
                    +-----------|-----------+
                                | événements de l’agent
                    +-----------v-----------+
                    | VM Wazuh dédiée       |
                    | Ubuntu Server 26.04   |
                    | Docker single-node    |
                    | manager → indexer     |
                    | dashboard             |
                    +-----------------------+
```

Le sujet nomme la VM « Ubuntu 20.04 » : c’est son contexte initial.
La version actuellement utilisée doit être confirmée après les opérations
de migration ; ce schéma ne prouve pas sa version.
La plateforme Wazuh sera hébergée dans une **VM dédiée Ubuntu Server
26.04**, avec les trois composants centraux en conteneurs Docker.
Son adresse et son chemin réseau restent à préciser ; son installation
n’est pas encore vérifiée.
La collecte de `eve.json` depuis l’hôte nécessite une configuration distincte :
le seul agent du conteneur ne lit pas automatiquement ce fichier.

## 2. Ce que chaque point peut observer

| Information / activité | Suricata sur l’hôte, interface virbr0 | Agent dans le conteneur File Browser |
| --- | --- | --- |
| Connexion entrante sur 8080 | IP, ports, protocole, horaires et flux, si les paquets traversent l’interface surveillée | Une trace applicative seulement si File Browser la produit et si elle est collectée |
| HTTP en clair | Méthode, URI, statut et autres champs selon analyse et sorties activées ; motifs des règles | Journaux applicatifs configurés, éventuellement utilisateur et action si ces champs sont journalisés |
| HTTPS | Métadonnées du flux et certaines informations TLS ; contenu applicatif masqué sans déchiffrement | Journaux de l’application après traitement du trafic, si accessibles ; pas le contenu complet des requêtes par défaut |
| Requête DNS de la VM | Nom demandé et réponse si DNS non chiffré visible et journalisation active | Journaux du résolveur ou de l’application s’ils existent et sont lisibles ; aucune collecte DNS automatique supposée |
| Ajout, modification ou suppression de fichier | Éventuelle requête réseau associée ; ne prouve pas l’état final du fichier | Événement d’intégrité si le chemin est surveillé, accessible et le mécanisme de suivi adapté |
| Identité et résultat d’authentification | Un code 401 ou 200 ne suffit pas à identifier le compte ou expliquer le résultat | Informations des journaux applicatifs si File Browser les fournit ; l’agent ne les invente pas |
| Processus et composants installés | Ne déduit pas l’inventaire complet à partir du trafic | Inventaire selon modules, droits et compatibilité ; limité à ce qui est visible dans le conteneur |
| Arrêt ou recréation du conteneur | Silence réseau éventuel, insuffisant pour conclure | L’agent peut disparaître avec le conteneur ; événements Docker à collecter depuis la VM/runtime pour connaître la cause |

L’agent peut collecter des journaux et un inventaire selon ses modules,
comme décrit dans la [documentation de l’agent Wazuh](https://documentation.wazuh.com/current/getting-started/components/wazuh-agent.html).
Il faut vérifier les droits et la portée réelle de chaque module dans le
conteneur ; un agent présent ne garantit pas toutes ces observations.

## 3. Réseau et système : des informations complémentaires

Les paquets, leur ordre, les caractéristiques protocolaires et les tentatives
qui n’atteignent pas l’application sont accessibles au capteur réseau **s’ils
passent par son interface**. Dans les deux sources envisagées, l’agent
applicatif ne possède pas automatiquement ces données. Elles ne sont pas
exclusives à Suricata : une capture réseau ou des journaux réseau adaptés
peuvent également les fournir.

L’état effectif d’un fichier, son empreinte, ses droits et les événements
internes de l’application nécessitent une visibilité système ou applicative.
Le suivi d’intégrité doit préciser les chemins, la fréquence ou le mode de
surveillance : voir le [fonctionnement du FIM Wazuh](https://documentation.wazuh.com/current/user-manual/capabilities/file-integrity/how-it-works.html).
Ce suivi ne fournit pas automatiquement l’auteur ou la commande responsable
de chaque modification ; une collecte d’audit compatible peut être nécessaire.

## 4. Activités susceptibles de laisser deux traces

| Activité | Trace réseau possible | Trace locale possible | Limite de la corrélation |
| --- | --- | --- | --- |
| Envoi d’un fichier par File Browser | Requête HTTP et flux de données | Journal d’envoi et création/modification du fichier surveillé | Nom, auteur et réussite à confirmer côté application ; HTTPS masque la requête au capteur |
| Tentative d’authentification | Requête et réponse HTTP si en clair | Résultat et compte si journalisés | Un renouvellement 401 ne doit pas être assimilé à un mauvais mot de passe |
| Modification de configuration via une fonction applicative | Requête correspondante si visible | Journal d’action ou événement FIM sur la configuration | Une modification locale peut avoir lieu sans requête réseau |
| Marqueur `%2e%2e` testé sur 8080 | Alerte 1008001 déjà visible dans la capture | Éventuel journal d’accès HTTP | Aucune trace Wazuh fournie ; le marqueur inerte ne prouve pas une exploitation |

Corréler date et heure synchronisées, service, IP/port, méthode et ressource
quand disponibles. L’identifiant `flow_id` de Suricata n’est pas un identifiant
partagé automatiquement avec les journaux File Browser. Le NAT ou un proxy
peut modifier l’adresse vue par l’application ; une corrélation temporelle
seule ne prouve pas que deux événements correspondent.

## 5. Limites des deux emplacements

**Suricata sur virbr0.** Le capteur dépend du trajet réel des paquets,
de la qualité de capture et des sorties activées. Il ne voit pas le loopback
de la VM, les échanges internes au conteneur ni les communications entre
conteneurs restant sur un bridge Docker interne à la VM. Un trafic utilisant
une autre interface peut lui échapper. Le chiffrement limite l’analyse ;
une signature ne prouve ni compromission ni résultat applicatif.

**Agent dans le conteneur.** Sa visibilité dépend des espaces de noms,
des montages, des permissions et de la configuration de collecte. Il ne
surveille pas automatiquement l’ensemble de la VM, ses authentifications SSH,
les autres conteneurs ou les événements du moteur Docker. Les logs écrits
uniquement sur stdout/stderr peuvent nécessiter une collecte depuis le runtime
sur la VM. La [surveillance Docker de Wazuh](https://documentation.wazuh.com/current/user-manual/capabilities/container-security/monitoring-docker.html)
est un dispositif spécifique, distinct de la simple présence d’un agent
applicatif.

Installer et exécuter deux services dans une image applicative demande aussi
une gestion des processus, des ressources et de la persistance. L’identité
et la configuration de l’agent doivent survivre de manière maîtrisée aux
recréations ; les fichiers éphémères peuvent disparaître avant collecte.
Une compromission du conteneur peut altérer ses traces ou son agent.
L’accès privilégié ou au socket Docker n’est pas une condition à ajouter
par défaut pour réaliser ce schéma.

## 6. Préparer la validation de l’architecture

| Point à confirmer | Preuve à conserver |
| --- | --- |
| État de la VM et service ciblé | Version OS, adresse, port publié et conteneur réellement utilisé |
| Sources locales disponibles | Emplacement ou sortie des logs, champs produits et chemins à surveiller |
| Agent opérationnel | Identité enregistrée, connexion au manager et événement de test reçu |
| Suivi de fichier | Modification inerte dans un répertoire de test, événement correspondant et portée observée |
| Double observation | Accès normal horodaté et traces réseau/application corrélées sans secrets |
| Centralisation Suricata | Configuration de collecte sur l’hôte et événement EVE reçu dans Wazuh |
| Continuité après recréation | Identité, configuration et reprise de collecte vérifiées lors d’un test ultérieur maîtrisé |

**À ce stade :** la visibilité Suricata sur 8080 est illustrée ; la collecte
locale, la corrélation et la centralisation Wazuh restent à démontrer.

## 📦 Livrable

Conserver le schéma, les tableaux de comparaison, les limites et les preuves
attendues. Deux points d’observation donnent des perspectives différentes :
le réseau décrit les échanges visibles ; les journaux et le suivi local
peuvent expliquer les actions et leurs effets dans le périmètre accessible.

- [Règles locales et preuves Suricata](rechercher-adapter-regles-detection.md)
- [Point d’observation réseau J7](../it-7/identifier-point-observation.md)
- [Retour à l’itération 8](index.md)
- [Retour au module](../README.md)
