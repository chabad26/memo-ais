# 2.1 — Atelier 1 | Découvrir les communications Modbus TCP

**Itération 1 · Journée 2 · 1 h · Travail en autonomie.**

## Objectif et organisation

**Identifier les principales caractéristiques du protocole Modbus TCP et comprendre comment les équipements industriels échangent leurs données.** Travail individuel ou en binôme sur le modèle Python/Modbus fourni en J1.

Le formateur n’est pas présent pendant cette séance : utiliser la documentation et l’entraide du groupe. La matinée est autonome ; l’après-midi prévoit mise en commun, validation de l’environnement et essais avec le formateur.

Cette fiche renseigne l’analyse documentaire. Aucune nouvelle capture réseau, écriture ou validation de jumeau numérique n’est présentée comme exécutée ici.

## 1 — Comprendre le principe de Modbus

Modbus fonctionne par **requêtes et réponses** : un client demande une lecture ou une écriture, le serveur traite l’opération et répond, éventuellement par une exception. Le rôle client/serveur décrit l’échange, pas le niveau d’autorité métier. [Modbus Messaging Implementation Guide V1.0b](https://www.modbus.org/file/secure/messagingimplementationguide.pdf).

### Rôles dans le laboratoire

| Élément | Rôle Modbus / interaction |
| --- | --- |
| `lab.server` et `lab/modbus.py` | Serveur TCP sur **127.0.0.1:15020** par défaut, donnant accès aux variables de `Plant`. |
| `lab.client` | Client de maintenance : lectures et écritures selon la commande utilisée. |
| `lab.dashboard` | Client Modbus pour lire les variables, et serveur HTTP pour le navigateur sur **18080**. |
| Navigateur | Client HTTP de la supervision ; il n’envoie pas directement des requêtes Modbus. |
| Processus thermique et régulation | Fonctions internes au même modèle Python ; pas deux équipements Modbus séparés. |

Le port conventionnel Modbus TCP est **502** ; **15020 est le port choisi par le laboratoire**. Employer ce dernier pour les futures observations du TP. [Guide d’implémentation TCP/IP](https://www.modbus.org/file/secure/messagingimplementationguide.pdf).

### Les quatre catégories de données

| Type | Taille élémentaire | Accès classique | Exemple fourni dans le laboratoire |
| --- | --- | --- | --- |
| **Coils** | 1 bit | Lecture et écriture | Porte virtuelle, défaut capteur injecté. |
| **Discrete Inputs** | 1 bit | Lecture | Commande du compresseur et alarme, également exposées sous forme binaire. |
| **Input Registers** | 16 bits | Lecture | Température, commande du compresseur, alarme et défaut capteur. |
| **Holding Registers** | 16 bits | Lecture et, selon la variable, écriture | Consigne et mode automatique modifiables ; limite conseillée en lecture seule. |

Les catégories et opérations sont définies dans la [spécification applicative V1.1b3, §4.3 et §6](https://www.modbus.org/file/secure/modbusprotocolspecification.pdf). Les exemples et restrictions ci-dessus viennent de `docs/REGISTER_MAP.md` et de `Plant.read()` / `write_register()` / `write_coil()`.

**La table ne suffit pas à déterminer un droit d’écriture réel.** Dans ce serveur, le holding register 1 contient la limite conseillée de 8 °C, mais son écriture est refusée. Inversement, un état lu seul peut évoluer sous l’effet d’un autre paramètre écrit : changer la consigne peut modifier la commande du compresseur.

Les adresses PDU commencent à **0**. Toujours préciser **table + adresse** : holding 0 = consigne, input 0 = température, coil 0 = porte. Un registre ne porte pas intrinsèquement une unité ou un sens physique : la table du laboratoire précise ici les dixièmes de degré, par exemple **40 → 4 °C**.

## 2 — Identifier les codes de fonction

| Code | Nom demandé | Données concernées | Opération | Application dans le laboratoire |
| --- | --- | --- | --- | --- |
| **FC01 / 0x01** | Read Coils | Coils | Lecture | Lire porte et défaut injecté. |
| **FC02 / 0x02** | Read Discrete Inputs | Discrete inputs | Lecture | Lire compresseur et alarme sous forme binaire. |
| **FC03 / 0x03** | Read Holding Registers | Holding registers | Lecture | Lire consigne, limite conseillée et mode automatique. |
| **FC04 / 0x04** | Read Input Registers | Input registers | Lecture | Lire température, compresseur, alarme et défaut. |
| **FC05 / 0x05** | Write Single Coil | Une coil | Écriture | Injecter l’ouverture de porte ou le défaut capteur. |
| **FC06 / 0x06** | Write Single Register | Un holding register | Écriture | Modifier la consigne ou le mode automatique. |

Référence : [spécification applicative V1.1b3, §6.1 à §6.6](https://www.modbus.org/file/secure/modbusprotocolspecification.pdf), confrontée au gestionnaire `handle_pdu()` de `lab/modbus.py`. La liste décrit le sous-ensemble étudié, pas toutes les fonctions Modbus existantes.

### Relier les commandes déjà utilisées aux échanges

| Commande J1 | Opérations visibles dans `lab/client.py` |
| --- | --- |
| `python3 -m lab.client status` | FC03 pour les holding registers, FC04 pour les input registers, puis FC01 pour les coils. FC02 n’est pas utilisé par cette commande. |
| `python3 -m lab.client setpoint 6` | FC06, holding 0, valeur **60**. |
| `python3 -m lab.client door 1` | FC05, coil 0, valeur **0xFF00** pour vrai. |
| `python3 -m lab.client door 0` | FC05, coil 0, valeur **0x0000** pour faux. |
| `python3 -m lab.client sensor-fault 1` | FC05, coil 1, valeur **0xFF00**. |

Ce tableau est un **repérage dans le code**, pas un décodage de trames déjà capturées. La supervision Python lit FC04, FC03 et FC01 ; elle ne réalise pas les écritures du client de maintenance.

## 3 — Rechercher les propriétés de sécurité

### 1. Le Modbus TCP conventionnel chiffre-t-il les communications ?

**Non, il ne fournit pas de chiffrement natif.** Sans protection complémentaire, les requêtes, adresses et valeurs peuvent être lues par un acteur capable d’observer le trafic. Le transport TCP ne chiffre pas à lui seul les données.

### 2. Prévoit-il une authentification des clients ?

**Non, pas d’authentification native du client dans le Modbus TCP conventionnel.** Une adresse IP ou un identifiant d’unité ne constitue pas une preuve cryptographique d’identité. Les éléments de corrélation des échanges ne sont pas des identifiants de connexion utilisateur.

### 3. Peut-il distinguer, avec ce seul protocole, un client autorisé d’un client non autorisé ?

**Pas au titre d’une identité authentifiée fournie par le protocole conventionnel.** Si le client peut joindre le serveur et que celui-ci accepte la fonction, l’adresse et la valeur, une écriture peut être exécutée sans preuve native du mandat du client. Un contrôle externe ou propre au produit peut restreindre l’accès, mais ce n’est pas une garantie de ce seul protocole.

Dans le laboratoire, `handle_pdu()` vérifie fonctions, adresses et valeurs, sans authentifier l’opérateur. Une réponse `write accepted` prouve l’acceptation technique, pas l’autorisation métier. Le binding local limite l’accès réseau par défaut, sans ajouter d’identité Modbus.

### 4. Pourquoi est-ce problématique sur un réseau non maîtrisé ?

Un acteur ayant le chemin réseau pourrait consulter les variables, tenter des écritures acceptées ou perturber le service. Une consigne altérée peut modifier la commande puis l’évolution physique ; les conséquences dépendent du procédé et de ses protections. Dans le modèle, la limite conseillée de 8 °C n’empêche pas l’acceptation d’autres consignes dans la plage implémentée.

La portée de ces réponses concerne **Modbus TCP conventionnel**. Le [Modbus Security Protocol](https://www.modbus.org/file/secure/modbussecurityprotocol.pdf) définit une variante s’appuyant sur TLS et des certificats X.509 pour l’authentification, avec le port **802** ; la [page officielle des spécifications](https://www.modbus.org/modbus-specifications) la distingue du protocole historique. Le laboratoire Python ne l’implémente pas. Les protections réseau seront étudiées pendant les journées suivantes ; aucune n’est déclarée déployée par cette fiche.

## Synthèse pour la mise en commun

> Modbus TCP permet à un client de lire ou d’écrire des variables d’un serveur par codes de fonction. La table, l’adresse et l’encodage doivent être connus pour interpréter la donnée. Le serveur du laboratoire n’accepte pas toutes les écritures sur toutes les variables. Sa version conventionnelle n’authentifie pas les clients et ne chiffre pas leurs échanges : un accès réseau n’équivaut pas à une autorisation métier. La supervision lit, tandis que le client de maintenance peut modifier certains paramètres dont les effets se répercutent sur le procédé simulé.

### Éléments préparés / preuves à compléter

- Quatre catégories de données et six fonctions identifiées : tableaux renseignés.
- Questions de sécurité : réponses documentées et variante TLS distinguée.
- Correspondance commandes / registres / fonctions : repérée dans le code.
- Trames, observations nouvelles et tests de validation J2 : **non réalisés dans cette fiche**.
- Environnement à vérifier avant les futurs essais : version de la copie Python et restauration éventuelle des seuils initiaux ; ne pas confondre FUXA statique et supervision connectée.

## Ressources

Sources officielles consultées le **26 octobre 2026** :

- [Modbus Organization — Specifications](https://www.modbus.org/modbus-specifications).
- [MODBUS Application Protocol Specification V1.1b3](https://www.modbus.org/file/secure/modbusprotocolspecification.pdf).
- [MODBUS Messaging on TCP/IP Implementation Guide V1.0b](https://www.modbus.org/file/secure/messagingimplementationguide.pdf).
- [Modbus Security Protocol](https://www.modbus.org/file/secure/modbussecurityprotocol.pdf).

Références locales : `docs/REGISTER_MAP.md`, `lab/model.py`, `lab/modbus.py`, `lab/client.py` et `lab/dashboard.py` dans le laboratoire fourni.

[Retour à l’itération 1](index.md) · [Préparation du jumeau numérique en J1](preparer-jumeau-numerique.md)
