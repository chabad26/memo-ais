# Cadrer le laboratoire et les responsabilités

## Objectif

Préparer un environnement où le même serveur pourra être audité, corrigé,
surveillé et étudié lors d'un incident pédagogique, avec une continuité des preuves.

**Statut : cadrage défini, premiers contrôles documentés.** Les deux systèmes
sont identifiés. File Browser est accessible depuis l'hôte et Greenbone y est
démarré, avec ses feeds en cours de synchronisation sur la capture fournie.
Les preuves figurent dans la
[fiche de préparation](it-1/preparer-cible-installer-greenbone.md).

## Contexte imposé

En 2021, un service a fait installer File Browser 2.15.0 dans un conteneur sur
un serveur Ubuntu 20.04 pour échanger des documents avec des partenaires.
Le serveur reste exposé sur Internet en 2026, avec un suivi de maintenance et
un partage des responsabilités insuffisamment documentés.

Pour les exercices, utiliser le **système hôte comme machine d'audit** et une
**VM Ubuntu Server 20.04 avec 2 vCPU et 4 Go de RAM comme cible**. La VM doit
être joignable depuis l'hôte. **Ne pas scanner les machines des autres apprenants.**

## Retrouver les responsabilités du cas fil rouge

| Sujet | Question à résoudre | Responsable identifié |
| --- | --- | --- |
| Besoin métier | Quel service utilise encore l'application ? Quel impact si elle s'arrête ? | À compléter |
| Système | Qui maintient l'OS, les comptes, les services et les sauvegardes ? | À compléter |
| Application | Qui maintient le code, les dépendances et les données ? | À compléter |
| Exposition | Qui autorise les flux Internet et les accès d'administration ? | À compléter |
| Changements | Qui valide une interruption, une correction ou un retour arrière ? | À compléter |
| Détection et incident | Qui reçoit, qualifie et escalade les alertes ? | À compléter |
| Fin de vie | Qui décide de maintenir, migrer ou retirer le serveur ? | À compléter |

L'absence de responsable clairement désigné est un constat organisationnel à
consigner. Elle ne prouve pas à elle seule une compromission technique.

## Répartir les rôles techniques

| Système | Fonction | Informations à relever avant installation |
| --- | --- | --- |
| Hôte / machine d'audit | Greenbone, outils d'audit, terminal SSH, navigateur et preuves | OS, Docker/Compose, espace disque, mémoire disponible et adresse de la VM |
| VM cible Ubuntu Server 20.04 | Docker et File Browser 2.15.0 sur le port 8080 | 2 vCPU, 4 Go de RAM, IP, compte d'administration, version Docker et digest de l'image |

Greenbone est installé **sur l'hôte**, pas dans la VM cible. Ses ressources
s'ajoutent aux 2 vCPU et 4 Go réservés à la VM. Le placement de Suricata et
l'hébergement collectif de Wazuh seront précisés lors des activités concernées ;
aucune VM d'audit supplémentaire n'est demandée pour ce premier exercice.

Avec virt-manager, utiliser un réseau virtuel permettant à l'hôte de joindre
la VM. Administrer la cible par SSH ou par sa console et ouvrir les interfaces
web depuis le navigateur de l'hôte.

## Préparer les flux et la visibilité

L'exposition Internet appartient au scénario. Le premier exercice nécessite
seulement l'accès de l'hôte à sa propre VM. Conserver le laboratoire dans le
réseau virtuel prévu, sans publication de File Browser sur Internet.

| Flux prévu | Origine → destination | Contrôle à conserver |
| --- | --- | --- |
| Accès applicatif | Hôte → IP de la VM, TCP 8080 | Page File Browser accessible et contrôle HTTP |
| Audit réseau, activité ultérieure | Greenbone sur l'hôte → sa propre VM | Cible unique, ports, profil et fenêtre d'audit |
| Administration | Hôte → VM par SSH ou console | Accès nominatif et possibilité de reprise par console |
| Observation Suricata | Trafic du serveur → interface de capture | Paquets de test effectivement visibles |
| Collecte Wazuh | Agent sur la machine portant les journaux → plateforme | Agent identifié, événement reçu et horodatage |
| Mise à jour des outils | Machines concernées → dépôts et bases nécessaires | État des mises à jour, date des bases et erreurs éventuelles |

Une sonde dans une autre VM du même réseau virtuel ne reçoit pas nécessairement
le trafic unicast du serveur. Prévoir une capture sur l'hôte observé, un port
miroir ou un point de passage adapté, puis vérifier la visibilité avant les règles.
Documenter aussi les limites de lecture des contenus chiffrés en TLS.

## Conditions avant le premier audit

- [ ] Serveur, application, interfaces et cibles identifiés.
- [ ] Responsables métier, système et applicatif renseignés ou absence consignée.
- [ ] Périmètre, horaires et conditions d'arrêt du scan établis.
- [ ] Sauvegarde ou état de laboratoire récupérable disponible ; procédure de retour identifiée.
- [ ] Accès SSH et console vérifiés avant toute modification du réseau ou des comptes.
- [ ] Horloges synchronisées, fuseau et éventuels décalages relevés.
- [ ] Test fonctionnel de l'application défini et exécuté pour l'état initial.
- [ ] Versions des outils, profils et dates des bases enregistrés.
- [ ] Dossier de preuves protégé, distinct des fichiers publiés dans le mémo.

Un snapshot facilite le retour du laboratoire à un état connu. Il ne remplace
pas une sauvegarde indépendante et ne doit pas écraser les preuves d'un incident
avant leur conservation.

## Organiser le travail collectif Wazuh

| Mission | Personne ou groupe | Preuve de contribution attendue |
| --- | --- | --- |
| Héberger et maintenir la plateforme | À compléter | Configuration et vérification des composants |
| Enrôler les agents et raccorder Suricata | À compléter | Association machine/agent et événement de test |
| Définir les recherches et la qualification | À compléter | Filtres, événements corrélés et interprétation |
| Suivre l'incident | À compléter | Chronologie, décisions et acteurs |
| Restituer et relire | À compléter | Synthèse collective et contributions individuelles |

Chaque apprenant conserve la trace de ses propres actions. Un résultat observé
sur le dashboard partagé doit rester attribué à la bonne machine et au bon groupe.

## État final attendu et preuves

Conserver l'inventaire rempli, les flux autorisés, le test fonctionnel initial,
la répartition des responsabilités et les décisions de préparation. Masquer les
secrets, les données personnelles et les informations internes dans les extraits
destinés au formateur ou au dépôt public.

- [Dossier de preuves](dossier-preuves.md)
- [Préparer la cible et installer Greenbone](it-1/preparer-cible-installer-greenbone.md)
- [Commencer l'audit](it-1/index.md)
- [Retour au module](README.md)
