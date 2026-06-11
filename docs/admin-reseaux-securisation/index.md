# ADMINISTRATION DES RÉSEAUX SÉCURISATION

## Objectif global

Avec ce module sur la sécurisation des infrastructures réseau, vous passez d'administrateur réseau à administrateur réseau sécurisé : VLANs cloisonnés, VPN (Virtual Private Network) chiffrés, pare-feux configurés avec règles ACL (Access Control List), analyse forensique de trafic, réponse aux incidents, automatisation de la sécurité. En sept jours, vous reprenez l'infrastructure réseau bâtie lors du module précédent et vous la durcissez face à des scénarios de menace concrets, jusqu'à un challenge CTF (Capture The Flag) en clôture.

L'objectif n'est pas de faire de vous un analyste SOC (Security Operations Center) ou un expert pentest — c'est que vous maîtrisiez les gestes de sécurisation réseau qui font partie du quotidien de l'administrateur d'infrastructure, et que vous acquériez la posture de réponse aux incidents. Ce module conditionne directement la lecture sécurité que tous les modules suivants vont approfondir (supervision, sécurité avancée, droit du numérique, intelligence artificielle).

Vous apprendrez à :

- Décrire les principes et architectures de sécurisation réseau : défense en profondeur, segmentation, moindre privilège, modèle Zero Trust dans ses grandes lignes.
- Configurer des VLANs sécurisés : isolation effective des flux, ACL inter-VLAN (Virtual Local Area Network), protection contre le VLAN Hopping, segmentation au service du moindre privilège.
- Mettre en œuvre un VPN (IPsec ou OpenVPN) et un pare-feu (pfSense ou équivalent) : tunnels chiffrés site-à-site et nomade, règles ACL restrictives, NAT (Network Address Translation), journalisation systématique.
- Identifier les attaques courantes par analyse de trafic avec Wireshark et Zeek : scans de ports, attaques par déni de service (DoS (Denial of Service)), VLAN Hopping, exfiltration de données — formuler un diagnostic d'incident.
- Répondre à un incident de sécurité réseau selon une méthodologie cadrée (référentiel ISO (International Organization for Standardization) 27035) : isoler la menace, analyser les logs, formuler des mesures correctives, documenter le retour d'expérience.
- Automatiser la sécurité réseau : scripts Bash ou Python pour surveiller des indicateurs (échecs de connexion, scans), bloquer dynamiquement des IP malveillantes, alerter sur des anomalies.
- Documenter une infrastructure réseau sécurisée (architecture, règles, justifications) et participer à un challenge CTF en équipe pour mobiliser l'ensemble des acquis.

## Démarche pédagogique

Le module suit une trajectoire configurer → attaquer → sécuriser : configurer une infrastructure réseau, observer ce qui peut être exploité, mettre en place les contre-mesures. Le module se clôt par un challenge CTF qui mobilise l'ensemble des acquis. La progression suit cinq grandes phases :

- VLANs sécurisés et cloisonnement — principes de cloisonnement, ACL inter-VLAN, protection contre le VLAN Hopping. Reprise de l'infrastructure réseau bâtie au module précédent et premier durcissement. Étude de cas : fuite de données par mauvaise configuration VLAN.
- VPN et pare-feu — configuration VPN IPsec ou OpenVPN entre deux sites. Mise en place d'un pare-feu (pfSense ou équivalent) avec règles ACL restrictives, NAT et journalisation. La complexité de la configuration VPN + pare-feu sur un scénario complet ouvre une opportunité naturelle pour une séquence d'autonomie.
- Analyse forensique avec Wireshark et Zeek — Wireshark approfondi (filtres avancés) puis introduction à Zeek pour l'analyse forensique. Détection de scans de ports, attaques par déni de service, exfiltration. Étude d'une capture réelle de VLAN Hopping. Lecture critique des logs.
- Réponse aux incidents et automatisation — méthodologie ISO 27035 (préparation, identification, confinement, éradication, reprise, leçons). Simulation : un serveur compromis — isolation, analyse des logs, mesures correctives, rapport. Scripts Bash/Python pour automatiser la surveillance (blocage IP après échecs répétés, alerte sur scan de ports). Une seconde opportunité d'autonomie peut porter sur la sécurisation complète de l'infrastructure réseau acquise au module précédent + livrable.
- Challenge CTF et clôture — challenge CTF en équipes : sécuriser une infrastructure réseau, contrer une attaque, configurer un VPN, répondre à un scénario d'incident. Présentation des solutions, débriefing collectif.

## Compétences développées

- Sécuriser un cloisonnement par VLANs : isoler effectivement les flux, configurer un filtrage inter-VLAN par ACL, neutraliser les attaques par VLAN Hopping, justifier la segmentation au regard des données traitées.

- Mettre en place un VPN : configurer un tunnel chiffré IPsec ou OpenVPN entre deux sites ou pour un accès nomade, vérifier la connectivité chiffrée, lire les logs.
- Configurer un pare-feu et ses règles ACL : règles ACL restrictives (logique « tout interdire sauf autorisé »), NAT, journalisation systématique, lecture critique des logs pour détecter des anomalies.
- Détecter une attaque par analyse forensique : utiliser Wireshark et Zeek pour identifier scans de ports, attaques par déni de service, VLAN Hopping, exfiltration — qualifier l'incident et documenter le diagnostic.
- Répondre à un incident de sécurité réseau : méthodologie ISO 27035 : isoler la menace, analyser les logs, formuler 3 mesures correctives, produire un rapport d'incident exploitable par un pair.
- Automatiser la sécurité réseau : scripts Bash ou Python pour surveiller des indicateurs (échecs, scans), bloquer dynamiquement des IP malveillantes, alerter sur des anomalies — documentés et réutilisables.
- Mobiliser ses acquis en mise en situation (CTF) : résoudre un challenge CTF en équipe (sécurisation, riposte, configuration), documenter sa solution et défendre ses choix techniques.
