# Liens utiles

Cette page regroupe les ressources utiles croisées dans le mémo AIS, classées par thème. Elle sert de point d'entrée pour réviser, vérifier une commande, approfondir une notion ou faire de la veille.

## Linux et administration système

### Installation, Debian et VirtualBox

| Ressource | Utilité |
| --- | --- |
| [Debian 12 - Guide d'installation officiel](https://www.debian.org/releases/stable/amd64/install.fr.pdf) | Installation propre d'une VM Debian serveur |
| [Debian Handbook](https://www.debian.org/doc/manuals/debian-handbook/) | Référence générale Debian |
| [VirtualBox - documentation officielle](https://www.virtualbox.org/manual/ch01.html) | Création et gestion des machines virtuelles |
| [VirtualBox - réseau virtuel](https://www.virtualbox.org/manual/ch06.html) | NAT, pont, host-only, réseau interne |
| [VirtualBox - téléchargements Linux](https://www.virtualbox.org/wiki/Linux_Downloads) | Installation de VirtualBox sur Ubuntu/Debian |

### Arborescence, comptes et permissions

| Ressource | Utilité |
| --- | --- |
| [FHS 3.0 - Spécification officielle](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html) | Comprendre `/etc`, `/var`, `/home`, `/usr`, `/opt` |
| [LinuxTricks - Arborescence Linux](https://www.linuxtricks.fr/wiki/arborescence-du-systeme-linux) | Vue synthétique de l'arborescence Linux |
| [Debian Handbook - Gestion des utilisateurs](https://www.debian.org/doc/manuals/debian-handbook/users.fr.html) | Utilisateurs, groupes, droits |
| [Debian Wiki - Permissions](https://wiki.debian.org/Permissions) | Permissions Unix classiques |
| [chmod Calculator](https://chmod-calculator.com/) | Vérifier rapidement une notation `chmod` |
| [POSIX ACL HowTo](https://tldp.org/HOWTO/html_single/POSIX-ACL-HOWTO/) | ACL Linux avec `setfacl` et `getfacl` |
| [Linux PAM](https://www.linux-pam.org/Linux-PAM-html/) | Authentification modulaire Linux |

Pages man utiles :

- `man hier`
- `man passwd`
- `man shadow`
- `man group`
- `man chmod`
- `man chown`
- `man umask`
- `man setfacl`
- `man getfacl`
- `man acl`

### Logs, Bash et automatisation

| Ressource | Utilité |
| --- | --- |
| [DigitalOcean - journalctl](https://www.digitalocean.com/community/tutorials/how-to-use-journalctl-to-view-and-manipulate-systemd-logs) | Lire et filtrer les journaux systemd |
| [RFC 5424 - Syslog Protocol](https://datatracker.ietf.org/doc/html/rfc5424) | Comprendre le format syslog |
| [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html) | Bonnes pratiques Bash |
| [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/) | Guide Bash avancé |
| [ShellCheck](https://www.shellcheck.net/) | Vérifier les erreurs classiques dans un script |
| [Explainshell](https://explainshell.com/) | Comprendre une commande shell complexe |
| [Terminus](https://frederic-junier.gitlab.io/parc-nsi/chapitre9/terminus/corrige/terminus.html) | S'entraîner aux bases du terminal |

Pages man utiles :

- `man bash`
- `man find`
- `man awk`
- `man tee`
- `man gzip`
- `man journalctl`
- `man systemd-journald`
- `man screen`

### Services Linux

| Ressource | Utilité |
| --- | --- |
| [NFS - Debian Wiki](https://wiki.debian.org/NFSServerSetup) | Configuration d'un serveur NFS Debian |
| [NFS HowTo - Linux Documentation Project](https://tldp.org/HOWTO/NFS-HOWTO/index.html) | Concepts et configuration NFS |
| [Samba - documentation officielle](https://www.samba.org/samba/docs/) | Documentation Samba / SMB |
| [Samba - Debian Wiki](https://wiki.debian.org/Samba/ServerSimple) | Mise en place simple d'un serveur Samba |

Pages man utiles :

- `man exports`
- `man exportfs`
- `man mount.nfs`
- `man smb.conf`
- `man smbpasswd`
- `man testparm`

## Réseau et administration réseau

### Fondations TCP/IP

| Ressource | Utilité |
| --- | --- |
| [RFC 791 - IPv4](https://tools.ietf.org/html/rfc791) | Fonctionnement IPv4 |
| [RFC 9293 - TCP](https://www.rfc-editor.org/rfc/rfc9293) | Spécification TCP à jour |
| [RFC 768 - UDP](https://tools.ietf.org/html/rfc768) | Spécification UDP |
| [RFC 826 - ARP](https://tools.ietf.org/html/rfc826) | Résolution IP vers MAC |
| [RFC 792 - ICMP](https://tools.ietf.org/html/rfc792) | Messages ICMP et `ping` |
| [RFC 1918 - Adresses privées](https://datatracker.ietf.org/doc/html/rfc1918) | Plages privées IPv4 |
| [RFC 4632 - CIDR](https://tools.ietf.org/html/rfc4632) | Notation CIDR |
| [IANA - ports et services](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml) | Référence des ports TCP/UDP |
| [Cloudflare Learning - réseau](https://www.cloudflare.com/learning/) | Explications accessibles TCP/IP, DNS, routage |
| [Cloudflare - routage IP](https://www.cloudflare.com/en-gb/learning/network-layer/what-is-routing/) | Routes, next-hop, principes de routage |

Pages man utiles :

- `man ip`
- `man ss`
- `man ping`
- `man traceroute`
- `man mtr`
- `man dig`

### Adressage, DHCP, DNS, NAT

| Ressource | Utilité |
| --- | --- |
| [Subnet Calculator](https://www.subnet-calculator.com/) | Vérifier sous-réseaux et masques |
| [RFC 2131 - DHCP](https://datatracker.ietf.org/doc/html/rfc2131) | Fonctionnement DHCP |
| [RFC 2132 - Options DHCP](https://datatracker.ietf.org/doc/html/rfc2132) | Options DHCP |
| [RFC 1034 - DNS concepts](https://datatracker.ietf.org/doc/html/rfc1034) | Concepts DNS |
| [RFC 1035 - DNS implementation](https://datatracker.ietf.org/doc/html/rfc1035) | Implémentation DNS |
| [BIND9 documentation](https://bind9.readthedocs.io/) | Configuration DNS BIND9 |
| [ISC - BIND](https://www.isc.org/bind/) | Projet BIND officiel |
| [RFC 3022 - NAT](https://datatracker.ietf.org/doc/html/rfc3022) | NAT traditionnel |
| [RFC 2993 - NAT implications](https://datatracker.ietf.org/doc/html/rfc2993) | Impacts d'architecture du NAT |
| [Cisco - NAT](https://www.cisco.com/c/en/us/support/docs/ip/network-address-translation-nat/13772-12.html) | Configuration NAT côté Cisco |

### Cisco, GNS3 et simulation

| Ressource | Utilité |
| --- | --- |
| [GNS3 - site officiel](https://www.gns3.com) | Laboratoire réseau virtuel |
| [GNS3 - documentation](https://docs.gns3.com) | Installation et usage |
| [GNS3 - installation Linux](https://docs.gns3.com/docs/getting-started/installation/linux/) | Installer GNS3 sur Linux |
| [GNS3 - premier projet](https://docs.gns3.com/docs/using-gns3/beginners/the-gns3-gui) | Prise en main de l'interface |
| [GNS3 Community](https://community.gns3.com) | Aide et discussions |
| [Cisco - Configuration STP](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst3560/software/release/15-0_1_se/configuration/guide/scg3560/swstp.html) | STP / PVST+ |
| [Cisco - routage inter-VLAN](https://www.cisco.com/en/US/docs/ios-xml/ios/lanswitch/configuration/15-0sy/lsw-conf-rout-vlan.html) | VLAN, trunk, routage inter-VLAN |
| [Cisco - OSPF](https://www.cisco.com/c/en/us/tech/ip/ip-routing/tsd-technology-support-troubleshooting-technotes-list.html) | Ressources OSPF |
| [Cisco - icônes topologie](https://www.cisco.com/c/en/us/about/brand-center/network-topology-icons.html) | Schémas réseau |
| [draw.io](https://app.diagrams.net) | Créer des schémas réseau |

### Capture, diagnostic et automatisation réseau

| Ressource | Utilité |
| --- | --- |
| [Wireshark - site officiel](https://www.wireshark.org) | Capture et analyse réseau |
| [Wireshark - User Guide](https://www.wireshark.org/docs/wsug_html_chunked/) | Guide utilisateur |
| [Wireshark - Display Filter Reference](https://www.wireshark.org/docs/dfref/) | Référence des filtres |
| [Wireshark - Sample Captures](https://wiki.wireshark.org/SampleCaptures) | Captures d'exemple |
| [Wireshark - Display Filters Wiki](https://wiki.wireshark.org/DisplayFilters) | Aide filtres |
| [Netmiko](https://github.com/ktbyers/netmiko) | Automatisation SSH vers équipements réseau |
| [Baturin - iproute2](https://baturin.org/docs/iproute2/) | Référence moderne `iproute2` |
| [Ubuntu Server - network configuration](https://ubuntu.com/server/docs/network-configuration) | Réseau Ubuntu Server |

## Cybersécurité et veille

### Organismes et alertes

| Ressource | Utilité |
| --- | --- |
| [ANSSI - guides et recommandations](https://www.ssi.gouv.fr/guide/) | Guides de sécurité officiels |
| [ANSSI - Guide d'hygiène informatique](https://cyber.gouv.fr/guide/guide-dhygiene-informatique/) | Base des bonnes pratiques |
| [ANSSI - Guide d'hygiène informatique (publication)](https://cyber.gouv.fr/publications/guide-dhygiene-informatique) | Version publication |
| [CERT-FR - alertes](https://www.cert.ssi.gouv.fr/alerte/) | Alertes de sécurité en temps réel |
| [CERT-FR](https://cert.ssi.gouv.fr/) | Bulletins, CTI, vulnérabilités |
| [Cybermalveillance.gouv.fr - collectivités](https://www.cybermalveillance.gouv.fr/tous-nos-contenus/bonnes-pratiques/collectivites) | Bonnes pratiques pour collectivités |
| [ANSSI - cyberattaques et remédiation](https://messervices.cyber.gouv.fr/guides/cyberattaques-et-remediation-les-cles-de-decision) | Piloter la remédiation |
| [ANSSI - sauvegarde](https://cyber.gouv.fr/les-regles-dor-de-la-sauvegarde/) | Règles d'or de la sauvegarde |
| [ANSSI - configuration OpenSSH](https://www.ssi.gouv.fr/guide/recommandations-pour-la-configuration-dun-service-openssh/) | Durcissement SSH |
| [ANSSI - sécurité GNU/Linux](https://www.ssi.gouv.fr/guide/recommandations-de-securite-relatives-a-un-systeme-gnulinux/) | Durcissement Linux |

Veille réseaux sociaux :

- [ANSSI sur X](https://x.com/ANSSI_FR)
- [CERT-FR sur X](https://x.com/CERT_FR)
- [CNIL sur X](https://x.com/CNIL)

### Entraînement

| Ressource | Utilité |
| --- | --- |
| [Root-Me](https://www.root-me.org/) | Challenges cybersécurité |
| [TryHackMe](https://tryhackme.com/) | Labs guidés sécurité |
| [Kali Linux](https://www.kali.org/) | Distribution sécurité / pentest |
| [Kali Tools](https://www.kali.org/tools/) | Référence des outils Kali |

### Pare-feu, VPN, IDS et sécurité réseau

| Ressource | Utilité |
| --- | --- |
| [Cloudflare - Firewall](https://www.cloudflare.com/learning/security/what-is-a-firewall) | Concepts pare-feu |
| [Fortinet - Defense in depth](https://www.fortinet.com/resources/cyberglossary/defense-in-depth) | Défense en profondeur |
| [Fortinet Training Institute](https://www.fortinet.com/training) | Ressources réseau/sécurité |
| [nftables Wiki](https://wiki.nftables.org/) | Pare-feu Linux moderne |
| [pfSense - Firewall Rules](https://docs.netgate.com/pfsense/en/latest/firewall/) | Règles pare-feu pfSense |
| [pfSense - Aliases](https://docs.netgate.com/pfsense/en/latest/firewall/aliases.html) | Objets et alias pfSense |
| [pfSense - Logs](https://docs.netgate.com/pfsense/en/latest/monitoring/logs/) | Lire les logs pfSense |
| [OpenVPN documentation](https://openvpn.net/community-resources/) | Ressources OpenVPN |
| [OpenVPN HOWTO](https://openvpn.net/community-resources/how-to/) | Mise en place OpenVPN |
| [WireGuard](https://www.wireguard.com/) | VPN moderne |
| [IPsec - RFC 4301](https://www.rfc-editor.org/rfc/rfc4301) | Architecture IPsec |
| [Linux Foundation - IP routing](https://wiki.linuxfoundation.org/networking/iproute2) | Routage Linux |
| [Zeek documentation](https://docs.zeek.org/) | Analyse réseau Zeek |
| [Zeek logs](https://docs.zeek.org/en/current/logs/index.html) | Comprendre les logs Zeek |
| [Nmap](https://nmap.org/) | Scan réseau |
| [Nmap Reference Guide](https://nmap.org/book/man.html) | Référence Nmap |
| [Yersinia](https://github.com/tomac/yersinia) | Tests couche 2 en laboratoire |
| [Yersinia sur Kali](https://www.kalilinux.fr/commandes/yersinia-sur-kali-linux/) | Guide d'usage |

### Réponse à incident et cas réels

| Ressource | Utilité |
| --- | --- |
| [CHU de Rouen - point officiel](https://www.chu-rouen.fr/le-point-sur-lattaque-informatique-du-15-novembre-2019/) | Cas d'incident SI |
| [Le Monde - CHU de Rouen](https://www.lemonde.fr/pixels/article/2019/11/18/frappe-par-une-cyberattaque-massive-le-chu-de-rouen-force-de-tourner-sans-ordinateurs_6019650_4408996.html) | Article de contexte |
| [LeMagIT - CHU de Rouen](https://www.lemagit.fr/etude/CHU-de-Rouen-autopsie-dune-cyberattaque) | Analyse de l'incident |
| [L'Usine Digitale - CHU de Rouen](https://www.usine-digitale.fr/article/la-cyberattaque-du-chu-de-rouen-serait-bien-d-origine-criminelle.N908519) | Contexte cyberattaque |
| [CERT-FR - Rançongiciel Clop](https://www.cert.ssi.gouv.fr/uploads/CERTFR-2019-CTI-009.pdf) | Note CTI rançongiciel |
| [CERT-FR - MS17-010](https://www.cert.ssi.gouv.fr/alerte/CERTFR-2017-ALE-010/) | Propagation rançongiciel |
| [CrowdStrike - Channel File 291 RCA](https://www.crowdstrike.com/en-us/blog/channel-file-291-rca-available/) | Cas d'incident logiciel |
| [CrowdStrike - Executive Summary RCA](https://www.crowdstrike.com/wp-content/uploads/2024/08/Executive-Summary_Root-Cause-Analysis_Channel-File-291.pdf) | Résumé technique incident |

### Applications et durcissement applicatif

| Ressource | Utilité |
| --- | --- |
| [Spark Security](https://spark.apache.org/docs/latest/security.html) | Sécuriser Apache Spark |
| [Spark Standalone Mode](https://spark.apache.org/docs/latest/spark-standalone.html) | Mode standalone Spark |
| [Fail2ban Documentation](https://www.fail2ban.org/wiki/) | Protection brute force |

## RGPD et droit du numérique

### Textes et principes

| Ressource | Utilité |
| --- | --- |
| [CNIL - Comprendre le RGPD](https://www.cnil.fr/comprendre-le-rgpd-0) | Point d'entrée RGPD |
| [CNIL - RGPD notions clés](https://www.cnil.fr/rgpd-notions-cles-et-bons-reflexes) | Définitions et réflexes |
| [CNIL - six grands principes](https://www.cnil.fr/protection-des-donnees-les-bons-reflexes) | Principes fondamentaux |
| [CNIL - droits des personnes](https://www.cnil.fr/respecter-les-droits-des-personnes) | Droits RGPD |
| [EUR-Lex - Règlement UE 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj?locale=fr) | Texte officiel RGPD |
| [Dastra - 8 règles d'or RGPD](https://www.dastra.eu/fr/guide/8-regles-dor-de-la-conformite-rgpd/357) | Synthèse pédagogique |

### Acteurs et conformité

| Ressource | Utilité |
| --- | --- |
| [CNIL - missions](https://www.cnil.fr/fr/la-cnil/les-missions-de-la-cnil) | Rôle de la CNIL |
| [CNIL - missions et valeurs](https://www.cnil.fr/fr/nos-missions-et-nos-valeurs) | Présentation CNIL |
| [CNIL - responsable et sous-traitant](https://www.cnil.fr/fr/node/167268) | Identifier son rôle |
| [CNIL - DPO](https://www.cnil.fr/fr/passer-laction/le-delegue-la-protection-des-donnees-dpo) | Délégué à la protection des données |
| [CNIL - définition DPO](https://www.cnil.fr/fr/definition/delegue-la-protection-des-donnees-dpo) | Définition DPO |
| [CEPD - rôle](https://www.edpb.europa.eu/role-edpb_fr) | Comité européen de la protection des données |
| [CJUE - Curia](https://curia.europa.eu/site/jcms/d2_5088/fr/que-fait-la-cjue) | Cour de justice de l'UE |
| [CJUE - Union européenne](https://european-union.europa.eu/institutions-law-budget/institutions-and-bodies/search-all-eu-institutions-and-bodies/court-justice-european-union-cjeu_fr) | Institution CJUE |

### Collectivités, travail et violations

| Ressource | Utilité |
| --- | --- |
| [CNIL - collectivités territoriales](https://www.cnil.fr/collectivites-territoriales) | RGPD en collectivité |
| [CNIL - principes clés collectivités](https://www.cnil.fr/fr/collectivites-territoriales/les-principes-cles-de-la-protection-des-donnees) | Synthèse collectivités |
| [CNIL - conformité collectivités en 4 étapes](https://www.cnil.fr/fr/principes-cles/collectivites-territoriales-comment-assurer-votre-conformite-avec-un-plan-daction-en) | Plan d'action |
| [CNIL - guide collectivités PDF](https://www.cnil.fr/sites/default/files/atoms/files/cnil-guide-collectivite-territoriale.pdf) | Guide PDF |
| [CNIL - travail et données personnelles](https://www.cnil.fr/fr/thematiques/travail-et-donnees-personnelles) | Données au travail |
| [CNIL - thématique travail](https://cnil.fr/fr/thematiques-communes/travail) | Ressources travail |
| [CNIL - droits des personnes au travail](https://www.cnil.fr/fr/les-droits-des-personnes-au-travail) | Droits salariés |
| [CNIL - gestion RH](https://www.cnil.fr/fr/la-gestion-des-ressources-humaines) | Données RH |
| [CNIL - AIPD](https://www.cnil.fr/fr/RGPD-analyse-impact-protection-des-donnees-aipd) | Analyse d'impact |
| [CNIL - définition AIPD](https://www.cnil.fr/fr/definition/analyse-dimpact-aipd) | Définition |
| [CNIL - violations de données](https://www.cnil.fr/fr/cybersecurite/les-violations-de-donnees-personnelles) | Violation de données |
| [CNIL - notifier une violation](https://www.cnil.fr/fr/notifier-une-violation-de-donnees-personnelles) | Notification |
| [CNIL - registre des traitements](https://www.cnil.fr/fr/RGPD-le-registre-des-activites-de-traitement) | Registre RGPD |

## Système d'information, architecture et normes

### Cartographie et architecture SI

| Ressource | Utilité |
| --- | --- |
| [ANSSI - cartographie du SI](https://messervices.cyber.gouv.fr/documents-guides/20181213_anssi_guide_cartographie_v1b.pdf) | Cartographier un système d'information |
| [ANSSI - architectures sensibles](https://messervices.cyber.gouv.fr/documents-guides/anssi-guide-recommandations_architectures_systemes_information_sensibles_ou_diffusion_restreinte-v1.2.pdf) | Architectures sécurisées |
| [Red Hat - middleware](https://www.redhat.com/en/topics/middleware/what-is-middleware) | Comprendre le middleware |
| [Single Point of Failure - Wikipedia](https://en.wikipedia.org/wiki/Single_point_of_failure) | SPOF |
| [Hayk Simonyan - SPOF](https://hayksimonyan.substack.com/p/single-point-of-failure-spof-in-system) | SPOF en conception système |
| [GeeksforGeeks - centralisé/décentralisé/distribué](https://www.geeksforgeeks.org/system-design/comparison-centralized-decentralized-and-distributed-systems/) | Typologies d'architecture |
| [Service-public.fr - mairie](https://www.service-public.fr/particuliers/vosdroits/N19808) | Cas collectivité |

### Normes et réglementation SI

| Ressource | Utilité |
| --- | --- |
| [ANSSI - NIS/NIS2](https://cyber.gouv.fr/reglementation/cybersecurite-systemes-dinformation/directives-nis-nis2-et-dispositif-saiv/) | Réglementation cybersécurité |
| [EUR-Lex - DORA](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32022R2554) | Règlement DORA |
| [ISO/IEC 27001](https://www.iso.org/fr/standard/27001) | SMSI / sécurité de l'information |
| [Cour des comptes - sécurité informatique des établissements de santé](https://www.ccomptes.fr/sites/default/files/2024-12/20250103-S2024-1456-La-securite-informatique-des-etablissements-de-sante.pdf) | Retour institutionnel santé |
| [Étude sécurité SI hospitalier après cloud](https://pubmed.ncbi.nlm.nih.gov/35898480/) | Ressource académique santé/cloud |

## Outils pratiques

| Ressource | Utilité |
| --- | --- |
| [Explainshell](https://explainshell.com/) | Expliquer une commande shell |
| [ShellCheck](https://www.shellcheck.net/) | Vérifier un script Bash |
| [draw.io](https://app.diagrams.net) | Schémas réseau / SI |
| [Subnet Calculator](https://www.subnet-calculator.com/) | Calcul de sous-réseaux |
| [Root-Me](https://www.root-me.org/) | Pratique sécurité |
| [TryHackMe](https://tryhackme.com/) | Labs guidés |

## Ressources internes du mémo

| Ressource | Utilité |
| --- | --- |
| [Glossaire Intro AIS](glossaire/intro-rgpd/intro-ais.md) | Termes de base AIS |
| [Glossaire RGPD](glossaire/intro-rgpd/rgpd.md) | Termes RGPD |
| [Commandes Linux PDF](commandes-linux.md) | PDF Ubuntu CLI + rappels `screen`, `ls -of` |
| [Glossaire Systèmes Linux - itération 4](glossaire/admin-systemes-linux/it-4.md) | NFS, Samba, durcissement |
| [Glossaire Réseaux](glossaire/admin-reseaux/iteration-1.md) | Fondations réseau |
| [Glossaire Réseaux sécurisés](glossaire/admin-reseaux-securisation/it-1.md) | VLANs sécurisés, nftables, filtrage |

