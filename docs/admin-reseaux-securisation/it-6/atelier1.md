# Atelier 1 - Préparation défensive et validation de l'infrastructure

## Objectif

Cet atelier a pour objectif de vérifier, renforcer et documenter l'infrastructure réseau avant le challenge final.

Le point de vue adopté est celui d'un attaquant placé dans le VLAN Visiteurs ou dans le VLAN Administration. Le but n'est pas de casser l'infrastructure, mais d'observer ce qui est réellement visible, puis de corriger les expositions inutiles.

## Environnement utilisé

L'atelier réutilise l'infrastructure complète construite pendant les itérations précédentes.

| Élément | Rôle |
| --- | --- |
| Machines Linux | Services, administration, tests |
| Routeur physique | Routage entre réseaux ou sites |
| pfSense | Pare-feu, règles inter-VLAN, logs |
| `nftables` | Filtrage local ou routeur Linux |
| OpenVPN | Tunnel entre sites |
| Fail2ban | Protection SSH ou services exposés |
| Kali Linux | Poste de test depuis le VLAN Visiteurs ou Administration |

La topologie utilisée pour préparer la défense est celle du laboratoire GNS3. pfSense est placé au centre et relie les VLANs internes au réseau OpenVPN.

### Zones réseau de la maquette

| Zone | Équipements visibles sur la maquette | Rôle défensif |
| --- | --- | --- |
| VLAN 10 Administration | `KALI-admin`, `Admin-1`, `Admin-2`, `SWVLAN10` | Zone d'administration, accès SSH et règles strictes |
| VLAN 20 Production | `KALI-PROD`, `KALI-Prod-1`, `prod-1`, `prod-2`, `Hub1`, `SWVLAN20` | Zone sensible à protéger contre les déplacements latéraux |
| VLAN 30 RH | `KALI-RH`, `RH1`, `RH2`, `SWVLAN30` | Zone métier à isoler de Production et Administration |
| Coeur pfSense | `pfSense 2.7.0-1`, interfaces `em1`, `em2`, `em3`, `em0` | Filtrage inter-VLAN, logs, règles d'accès |
| Zone OpenVPN | `R2`, `vpnclient`, `NAT1`, `NAT2` | Accès distant et site-à-site à contrôler |

Interfaces pfSense d'après la capture :

| Interface pfSense | Liaison observée | Zone associée |
| --- | --- | --- |
| `em1` | Vers `SWVLAN10` | VLAN 10 Administration |
| `em2` | Vers `SWVLAN20` | VLAN 20 Production |
| `em3` | Vers `SWVLAN30` | VLAN 30 RH |
| `em0` | Vers `R2` / OpenVPN | Réseau VPN / sortie contrôlée |

VLANs à valider :

| VLAN | Rôle |
| --- | --- |
| VLAN 10 Administration | Accès d'administration contrôlés |
| VLAN 20 Production | Machines ou services sensibles |
| VLAN 30 RH | Machines métier RH à isoler |
| Zone OpenVPN | Accès distant via `R2` et `vpnclient` |

### Machines à retravailler en priorité

| Priorité | Machine | Zone | Travail défensif à faire |
| --- | --- | --- | --- |
| 1 | `pfSense` | Coeur | Revoir les règles par interface, activer les logs utiles, supprimer les règles trop larges |
| 1 | `R2` | OpenVPN | Vérifier OpenVPN, routes, accès SSH, logs et filtrage vers les VLANs |
| 1 | `prod-1` | VLAN 20 | Réduire les services exposés, protéger SSH, vérifier Zeek/Spark si présents |
| 1 | `prod-2` | VLAN 20 | Vérifier ports ouverts, accès SSH, journaux et règles locales |
| 2 | `Admin-1` | VLAN 10 | Vérifier que l'administration ne donne pas un accès trop large aux autres VLANs |
| 2 | `Admin-2` | VLAN 10 | Vérifier SSH, comptes, logs, Fail2ban si actif |
| 2 | `RH1` | VLAN 30 | Vérifier que RH n'est pas joignable depuis Production ou Visiteurs |
| 2 | `RH2` | VLAN 30 | Vérifier ports ouverts et isolation inter-VLAN |
| 3 | `vpnclient` | OpenVPN | Vérifier ce qui est accessible depuis le tunnel |
| 3 | `KALI-admin`, `KALI-PROD`, `KALI-RH` | VLANs de test | Utiliser uniquement comme postes de validation offensive contrôlée |

Les Kali ne sont pas à sécuriser en priorité. Ils servent surtout à tester ce qu'un attaquant pourrait voir depuis chaque zone.

## 1. Reprendre l'architecture réseau

Avant les tests, faire un état des lieux.

À vérifier :

- VLANs existants ;
- adresses IP ;
- passerelles ;
- routes ;
- VPN ;
- règles pfSense ;
- règles `nftables` ;
- accès SSH ;
- services actifs ;
- journaux disponibles.

Commandes utiles sur Linux :

```bash
ip -br addr
ip route
sudo ss -tulnp
systemctl --type=service --state=running
```

Sur pfSense :

- vérifier les interfaces ;
- vérifier les règles par interface ;
- vérifier les logs firewall ;
- vérifier les règles NAT si utilisées.

À documenter :

| Élément | Observation |
| --- | --- |
| VLAN de test utilisé | Visiteurs / Administration |
| Adresse IP de Kali | À compléter |
| Réseaux accessibles | À compléter |
| VPN actif | Oui / Non |
| pfSense actif | Oui / Non |
| Fail2ban actif | Oui / Non |

Tableau d'inventaire à compléter à partir de la maquette :

| Zone | Machine | IP | Services attendus | Services à fermer |
| --- | --- | --- | --- | --- |
| VLAN 10 | `Admin-1` | À compléter | SSH admin | À compléter |
| VLAN 10 | `Admin-2` | À compléter | SSH admin | À compléter |
| VLAN 20 | `prod-1` | À compléter | SSH, service utile | À compléter |
| VLAN 20 | `prod-2` | À compléter | Service utile uniquement | À compléter |
| VLAN 30 | `RH1` | À compléter | Service RH si présent | À compléter |
| VLAN 30 | `RH2` | À compléter | Service RH si présent | À compléter |
| OpenVPN | `R2` | À compléter | OpenVPN, SSH admin limité | À compléter |
| OpenVPN | `vpnclient` | À compléter | Client VPN uniquement | À compléter |

## 2. Identifier les services réellement exposés

Depuis Kali Linux, scanner uniquement les réseaux du laboratoire.

Postes Kali à utiliser selon la zone testée :

| Poste de test | Position | Ce qu'il faut vérifier |
| --- | --- | --- |
| `KALI-admin` | VLAN 10 Administration | Ce qu'un poste admin compromis peut atteindre |
| `KALI-PROD` ou `KALI-Prod-1` | VLAN 20 Production | Déplacements latéraux possibles dans Production |
| `KALI-RH` | VLAN 30 RH | Isolation RH vers Admin/Production |

Scanner une machine :

```bash
nmap 192.168.20.10
```

Scanner un sous-réseau :

```bash
nmap 192.168.10.0/24
nmap 192.168.20.0/24
nmap 192.168.30.0/24
```

Identifier les versions de services :

```bash
nmap -sV 192.168.20.10
```

Tester un port précis :

```bash
nc -zv 192.168.20.10 22
```

À documenter :

| Cible | Ports ouverts | Service détecté | Doit être exposé ? | Action |
| --- | --- | --- | --- | --- |
| `Admin-1` | À compléter | À compléter | Oui / Non | Garder / Restreindre / Fermer |
| `Admin-2` | À compléter | À compléter | Oui / Non | Garder / Restreindre / Fermer |
| `prod-1` | À compléter | À compléter | Oui / Non | Garder / Restreindre / Fermer |
| `prod-2` | À compléter | À compléter | Oui / Non | Garder / Restreindre / Fermer |
| `RH1` | À compléter | À compléter | Oui / Non | Garder / Restreindre / Fermer |
| `RH2` | À compléter | À compléter | Oui / Non | Garder / Restreindre / Fermer |
| `R2` | À compléter | OpenVPN / SSH | Oui / Non | Restreindre |

## 3. Vérifier les flux autorisés

Comparer les résultats des scans avec les règles réellement attendues.

Questions à se poser :

- le VLAN Visiteurs peut-il atteindre le VLAN Production ?
- le VLAN Administration peut-il atteindre trop de machines ?
- SSH est-il ouvert à tout le monde ?
- une interface Web d'administration est-elle visible ?
- un service oublié répond-il encore ?

Exemples de tests :

```bash
ping 192.168.20.10
nc -zv 192.168.20.10 22
curl http://192.168.20.10
```

Tableau de validation :

| Flux testé | Résultat observé | Résultat attendu | Conforme ? |
| --- | --- | --- | --- |
| `KALI-admin` vers `prod-1` SSH | À compléter | Autorisé seulement si administration prévue | Oui / Non |
| `KALI-admin` vers `prod-2` SSH | À compléter | Autorisé seulement si administration prévue | Oui / Non |
| `KALI-PROD` vers `Admin-1` SSH | À compléter | Bloqué | Oui / Non |
| `KALI-PROD` vers `Admin-2` SSH | À compléter | Bloqué | Oui / Non |
| `KALI-RH` vers VLAN 20 | À compléter | Bloqué sauf besoin métier | Oui / Non |
| `KALI-PROD` vers VLAN 30 | À compléter | Bloqué sauf besoin métier | Oui / Non |
| `vpnclient` vers VLAN 10 | À compléter | Limité aux flux nécessaires | Oui / Non |
| `vpnclient` vers VLAN 20 | À compléter | Limité aux flux nécessaires | Oui / Non |

## 4. Tester les protections

### Fail2ban

Vérifier que Fail2ban fonctionne :

```bash
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

Depuis Kali, simuler quelques erreurs SSH contrôlées :

```bash
ssh mauvais_user@192.168.x.x
```

Sur la machine protégée :

```bash
sudo fail2ban-client status sshd
sudo journalctl -u fail2ban --no-pager -n 50
```

À observer :

- IP bannie ;
- nombre d'échecs ;
- durée du ban ;
- logs générés.

### pfSense

Dans les logs firewall, vérifier :

- les paquets bloqués ;
- les paquets autorisés ;
- l'interface concernée ;
- l'adresse source ;
- l'adresse destination ;
- le port destination.

Règles pfSense à retravailler en priorité :

| Interface | Règle à vérifier | Attendu |
| --- | --- | --- |
| VLAN 10 / `em1` | Accès vers Production | Autoriser uniquement les flux d'administration nécessaires |
| VLAN 20 / `em2` | Accès vers Administration | Bloquer par défaut |
| VLAN 30 / `em3` | Accès vers autres VLANs | Bloquer par défaut sauf besoin précis |
| OpenVPN / `em0` | Accès depuis `vpnclient` | Restreindre aux machines utiles |
| Toutes | Règles `any any` | Supprimer ou remplacer par des règles précises |

### nftables

Sur les machines Linux ou routeurs Linux :

```bash
sudo nft list ruleset
```

Vérifier que les règles bloquent réellement les flux non autorisés.

## 5. Observer depuis Kali

Kali permet de vérifier ce qu'un attaquant pourrait voir.

Outils possibles :

| Outil | Usage |
| --- | --- |
| `nmap` | Découverte de ports et services |
| `netcat` | Test rapide de port |
| `tcpdump` | Observation du trafic |
| `hydra` | Test contrôlé de robustesse SSH |
| `nikto` | Test basique d'interface Web |

Exemples :

```bash
tcpdump -i eth0
nikto -h http://192.168.20.10
```

Scénarios à jouer depuis chaque Kali :

| Scénario | Source | Cible | Objectif défensif |
| --- | --- | --- | --- |
| Scan Production | `KALI-PROD` | `192.168.20.0/24` | Voir les services exposés dans le même VLAN |
| Scan inter-VLAN Admin | `KALI-PROD` | VLAN 10 | Vérifier que l'accès à Administration est bloqué |
| Scan inter-VLAN RH | `KALI-PROD` | VLAN 30 | Vérifier que RH est isolé |
| Test SSH admin | `KALI-admin` | `prod-1`, `prod-2`, `R2` | Vérifier les accès réellement nécessaires |
| Test brute force limité | `KALI-admin` ou `KALI-PROD` | Machine avec SSH | Vérifier Fail2ban |
| Test VPN | `vpnclient` | VLANs internes | Vérifier ce que le tunnel permet réellement |

Important : les tests doivent rester limités au lab et ne doivent pas chercher à dégrader volontairement les machines.

## 6. Identifier les faiblesses restantes

Pendant les tests, rechercher :

- règles trop permissives ;
- services inutiles ;
- ports oubliés ;
- interfaces Web accessibles ;
- mots de passe faibles ;
- logs absents ;
- VLANs mal isolés ;
- SSH exposé trop largement ;
- règles anciennes non supprimées.

Tableau de synthèse :

| Faiblesse | Preuve | Risque | Correction |
| --- | --- | --- | --- |
| SSH visible depuis Visiteurs | Scan Nmap | Brute force | Restreindre source + Fail2ban |
| Interface Web accessible | Curl/Nikto | Fuite d'information | Filtrage ou authentification |
| Log absent | Vérification journal | Analyse impossible | Activer journalisation |

## 7. Corriger et vérifier

Pour chaque problème identifié :

1. corriger la règle ou le service ;
2. redémarrer si nécessaire ;
3. refaire le test depuis Kali ;
4. vérifier les logs ;
5. documenter le résultat.

Exemples de corrections :

```bash
sudo systemctl disable --now <service>
sudo ufw deny 4040/tcp
sudo nft list ruleset
sudo fail2ban-client set sshd unbanip <IP>
```

Sur pfSense :

- supprimer les règles inutiles ;
- limiter les sources ;
- ajouter des descriptions aux règles ;
- activer les logs sur les règles importantes.

## 8. Préparer la documentation finale

Le document final doit contenir :

- les services réellement exposés depuis le VLAN Visiteurs ou Administration ;
- les ports ouverts identifiés ;
- les flux autorisés observés ;
- les éléments de sécurité déjà présents ;
- les scénarios testés ;
- les événements détectés ;
- les protections qui ont fonctionné ;
- les protections insuffisantes ;
- les risques encore présents ;
- les corrections réalisées ;
- ce qu'un attaquant pourrait encore tenter.

Modèle de tableau final :

| Élément | Résultat |
| --- | --- |
| VLAN de départ de l'attaquant | Visiteurs / Administration |
| Services visibles | À compléter |
| Ports ouverts | À compléter |
| Protections actives | pfSense, nftables, Fail2ban, VPN, logs |
| Détections observées | À compléter |
| Blocages observés | À compléter |
| Risques restants | À compléter |
| Corrections réalisées | À compléter |

## 9. Checklist avant challenge

Avant le challenge final, vérifier :

- les VLANs sensibles sont isolés ;
- seuls les flux nécessaires sont autorisés ;
- SSH est limité et protégé ;
- Fail2ban est actif ;
- pfSense journalise les flux importants ;
- `nftables` ne contient pas de règle trop large ;
- les interfaces Web sensibles sont fermées ou limitées ;
- le VPN fonctionne ;
- les comptes inutiles sont désactivés ;
- les mots de passe faibles sont changés ;
- les logs sont exploitables ;
- les scans depuis Kali ne révèlent pas de service inattendu.

## Conclusion

Cette itération transforme l'infrastructure en cible d'audit. L'objectif est d'observer ce qui est réellement exposé, de vérifier que les protections réagissent, puis de corriger les écarts avant le challenge final.

Une infrastructure prête n'est pas une infrastructure invisible, mais une infrastructure dont les flux sont justifiés, les services limités, les logs exploitables et les déplacements latéraux ralentis ou bloqués.
