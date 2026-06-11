# Atelier 1 - Introduction du module et architecture securisee

## Objectif de l'atelier

Cet atelier ouvre le module d'administration des reseaux securises. L'objectif est de comprendre le cadre du module, les livrables attendus pour le RNCP et les competences qui seront mobilisees pendant les travaux pratiques : cloisonner un reseau, filtrer les flux, mettre en place un acces VPN, observer les traces d'attaque et documenter les choix de securisation.

Le module reprend l'infrastructure reseau deja construite dans le module precedent, mais avec une logique de durcissement. Il ne suffit plus que les machines communiquent : les communications doivent etre justifiees, limitees, journalisees et testees face a des scenarios d'attaque.

## Environnement disponible

Le groupe dispose d'un environnement de laboratoire permettant de simuler une petite infrastructure d'entreprise :

| Equipement | Role dans le module |
| --- | --- |
| 4 machines Linux | Services, postes clients, tests de filtrage et supervision |
| 1 machine Kali Linux | Poste d'attaque pour les scans, tests offensifs et validation des protections |
| 1 routeur physique | Routage, interconnexion des segments et support de tests reseau |
| 2 VLANs minimum | Segmentation des zones reseau et limitation des flux inter-VLAN |
| pfSense | Pare-feu central, NAT, regles de filtrage, journalisation et VPN |
| nftables | Pare-feu local Linux pour filtrer les flux au niveau des machines |

Cette architecture permet de travailler sur deux niveaux de securite complementaires : le filtrage perimetrique avec pfSense et le filtrage local avec nftables. Si un controle echoue ou si une machine est compromise, une autre couche de protection doit limiter la propagation.

## Principes de securisation

### Defense en profondeur

La defense en profondeur consiste a empiler plusieurs mesures de securite complementaires. Un pare-feu seul ne suffit pas : on ajoute la segmentation reseau, le filtrage local, les droits limites, les journaux, la supervision et les sauvegardes. L'idee est qu'une erreur ou une compromission ne doit pas donner acces a toute l'infrastructure.

Dans le module, ce principe se traduit par :

- des VLANs separes ;
- des regles pfSense restrictives ;
- des regles nftables sur les machines Linux ;
- des acces VPN controles ;
- de la journalisation exploitable ;
- des captures et analyses avec Wireshark et Zeek.

### Segmentation reseau

La segmentation reseau consiste a decouper l'infrastructure en zones distinctes selon les usages, les niveaux de confiance ou la sensibilite des services. Par exemple, un VLAN d'administration ne doit pas etre accessible de la meme maniere qu'un VLAN utilisateur.

La segmentation reduit la surface d'attaque et limite les mouvements lateraux. Un attaquant present dans un VLAN ne doit pas pouvoir atteindre librement les autres zones. Les flux inter-VLAN doivent donc etre explicitement autorises, documentes et testes.

### Moindre privilege

Le moindre privilege impose de donner uniquement les droits et acces necessaires. Applique au reseau, cela signifie qu'une machine, un utilisateur ou un service ne doit acceder qu'aux ports, protocoles et destinations indispensables a son fonctionnement.

Exemple : un poste utilisateur peut avoir besoin d'acceder a un serveur web en HTTPS, mais pas d'ouvrir une session SSH sur tous les serveurs. Les regles de filtrage doivent donc partir d'une logique restrictive : tout refuser par defaut, puis autoriser seulement ce qui est justifie.

### Journalisation

La journalisation permet de conserver des traces des evenements importants : connexions acceptees ou bloquees, tentatives d'acces, erreurs VPN, scans, anomalies de trafic. Sans logs, il devient difficile de comprendre un incident ou de prouver qu'une regle fonctionne.

Les journaux doivent etre utiles et lisibles : il faut journaliser les flux importants, eviter le bruit inutile et savoir retrouver rapidement une information lors d'un diagnostic.

## Outils utilises

| Outil | Utilisation principale |
| --- | --- |
| pfSense | Configurer le pare-feu central, les regles inter-VLAN, le NAT, le VPN et les logs |
| nftables | Filtrer localement les paquets sur les machines Linux |
| OpenVPN | Mettre en place un tunnel chiffre pour un acces distant ou site-a-site |
| Wireshark | Capturer et analyser le trafic reseau paquet par paquet |
| Zeek | Produire des journaux reseau exploitables pour l'analyse de securite |
| Kali Linux | Realiser les tests offensifs : scan, enumeration, tentatives d'exploitation controlees |

Ces outils seront utilises ensemble : Kali genere des actions offensives, Wireshark et Zeek permettent de les observer, pfSense et nftables servent a les bloquer ou les limiter, puis les journaux permettent de documenter ce qui s'est passe.

## Challenge final CFP/CTF

Le module se termine par un challenge de type CFP/CTF. L'objectif est de mobiliser les competences du module dans une situation pratique : proteger une infrastructure, identifier des faiblesses, resister a des attaques, analyser des traces et justifier les choix techniques.

Les competences evaluees porteront notamment sur :

- la mise en place d'une segmentation reseau efficace ;
- la configuration de regles de filtrage restrictives ;
- la verification des flux autorises et bloques ;
- l'utilisation d'un VPN ;
- l'analyse de captures reseau et de journaux ;
- la reaction face a un incident ;
- la qualite de la documentation produite.

## Synthese personnelle

Ce premier atelier pose les bases du module : securiser un reseau ne consiste pas seulement a installer un pare-feu, mais a construire une architecture coherente. Les VLANs servent a separer les zones, pfSense controle les flux entre elles, nftables ajoute une protection locale, OpenVPN securise les acces distants et les outils d'analyse permettent de verifier ce qui circule vraiment.

Les notions importantes a retenir sont la defense en profondeur et la segmentation reseau. La defense en profondeur evite de dependre d'une seule protection. La segmentation reseau limite les consequences d'une compromission en empechant un attaquant de circuler librement dans toute l'infrastructure.

## Ressources

- ANSSI - Guides et recommandations : <https://www.ssi.gouv.fr/guide/>
- Fortinet - Defense in depth : <https://www.fortinet.com/resources/cyberglossary/defense-in-depth>
- nftables Wiki : <https://wiki.nftables.org/>

## Notions acquises

- Defense en profondeur
- Segmentation reseau
- Moindre privilege
- Journalisation
- Role des outils pfSense, nftables, OpenVPN, Wireshark, Zeek et Kali Linux
