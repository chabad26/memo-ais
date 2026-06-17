# Préparation au challenge final

## Contexte de l'itération

Cette itération sert à préparer l'infrastructure réseau avant le challenge final. Les travaux précédents ont permis de mettre en place :

- une segmentation réseau en VLANs ;
- des ACL et règles de filtrage ;
- pfSense ;
- `nftables` ;
- OpenVPN ;
- Zeek et Wireshark ;
- Fail2ban ;
- des scripts de réaction ;
- une démarche de réponse à incident.

L'objectif n'est plus seulement de faire fonctionner le réseau. Il faut maintenant le considérer comme une cible potentielle.

## Objectifs principaux

À la fin de l'itération, il faut être capable de :

- vérifier le niveau réel de sécurité ;
- identifier les points faibles restants ;
- limiter la surface d'exposition ;
- ralentir la progression d'un attaquant ;
- détecter les comportements suspects ;
- empêcher les déplacements latéraux ;
- conserver des traces exploitables dans les logs ;
- documenter les risques encore présents.

## Infrastructure cible

L'infrastructure attendue avant le challenge final doit contenir :

| Élément | Attendu |
| --- | --- |
| Sites réseau | Deux sites distincts |
| VPN | VPN site-à-site opérationnel |
| VLANs | Administration, Production, Visiteurs optionnel |
| Filtrage | pfSense et/ou `nftables` actifs |
| Journalisation | Logs pfSense, Linux, OpenVPN, Fail2ban exploitables |
| Protection SSH | Fail2ban ou mécanisme équivalent |
| Accès admin | SSH disponible uniquement si nécessaire |
| Services | Services explicitement autorisés uniquement |

## Logique du challenge final

Le challenge simulera deux situations :

- attaque depuis l'extérieur du réseau ;
- attaque depuis l'intérieur après compromission d'une machine.

Les attaquants auront un accès limité au VLAN choisi par le groupe : VLAN Visiteurs ou VLAN Administration.

Il faut donc se demander :

- que voit un attaquant depuis ce VLAN ?
- quels ports restent accessibles ?
- quels services répondent encore ?
- quels flux inter-VLAN sont possibles ?
- les protections bloquent-elles réellement les comportements suspects ?
- les logs permettent-ils de reconstituer ce qui s'est passé ?

## Ateliers

| Atelier | Sujet | Objectif |
| --- | --- | --- |
| Atelier 1 | Préparation défensive et validation de l'infrastructure | Vérifier l'exposition réelle, tester les protections, corriger les faiblesses et documenter les risques restants |

## Ressource

- Kali Linux Tools : <https://www.kali.org/tools/>
