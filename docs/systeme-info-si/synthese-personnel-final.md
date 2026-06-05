# Mémo personnel final

## Objectif

Cette page sert de synthèse finale du module **Système d'information & architecture SI**.

Elle regroupe :

- ce que j'ai compris ;
- ce qui m'a surpris ;
- ce qui reste flou ;
- ma vision du métier d'AIS face à un SI ;
- ma boîte à outils personnelle pour continuer.

## Synthèse personnelle

Un système d'information n'est pas seulement un ensemble de serveurs, de postes et de logiciels. C'est un système complet qui relie des personnes, des données, des applications, des réseaux, des procédures et des contraintes métier.

Ce que j'ai compris, c'est qu'un SI doit toujours être lu à partir des usages réels. Dans un hôpital, le DPI, les admissions, le laboratoire, l'imagerie, les prescriptions, les sauvegardes et l'annuaire ne sont pas de simples composants techniques : ils soutiennent directement les soins. Une panne ou une attaque peut donc avoir un impact métier immédiat.

Ce qui m'a surpris, c'est la vitesse à laquelle un incident peut devenir global. Un poste utilisateur, un accès VPN ou un compte compromis peut permettre une propagation vers l'Active Directory, les serveurs, les applications et parfois les sauvegardes. Le problème n'est pas seulement l'entrée de l'attaque, mais sa capacité à circuler dans le SI.

Ce qui reste flou pour moi concerne surtout le niveau de détail réel d'une architecture : jusqu'où faut-il descendre dans les flux, les VLAN, les ACL, les dépendances applicatives ou les droits d'accès ? Je comprends le principe, mais il faut encore pratiquer pour savoir doser entre un schéma lisible et une cartographie trop détaillée.

Ma vision du métier d'AIS a évolué : l'AIS n'est pas seulement quelqu'un qui administre des machines. Il doit comprendre les usages, repérer les dépendances, documenter, sécuriser progressivement, expliquer ses choix et préparer la continuité. Il doit aussi savoir dire : "je ne sais pas encore, mais je sais ce qu'il faut vérifier".

## Ce qui est clair

- Le SI regroupe personnes, applications, données, infrastructures et procédures.
- La cartographie sert à comprendre les zones, les flux et les dépendances.
- Les 4 axes utiles sont : réseau, applicatif, données, utilisateurs.
- Un risque doit être relié à un impact concret.
- La sécurité vise à réduire les accès inutiles et à limiter la propagation.
- La disponibilité est aussi importante que la confidentialité dans un contexte hospitalier.

## Ce qui reste à travailler

- Lire une architecture réelle sans se perdre dans les détails.
- Identifier les flux vraiment nécessaires avant de poser des ACL.
- Distinguer rapidement un symptôme d'une cause racine.
- Prioriser les mesures selon le coût, l'urgence et la faisabilité.
- Mieux comprendre les dépendances entre applications, annuaire, bases et sauvegardes.

## Boîte à outils personnelle

| Thème | Notions à garder | Fiche associée |
| --- | --- | --- |
| Vocabulaire d'architecture | SI, flux, API, middleware, AD, IAM, SPOF, dépendance critique | [Vocabulaire SI](../pense-bete/systeme-info/systeme-info-si-vocabulaire.md) |
| 4 axes de décomposition | réseau, applicatif, données, utilisateurs | [Cartographie et architecture](../pense-bete/systeme-info/systeme-info-si-cartographie.md) |
| Typologies SI | centralisée, décentralisée, distribuée, cloud, hybride | [Cartographie et architecture](../pense-bete/systeme-info/systeme-info-si-cartographie.md) |
| Enjeux et risques | disponibilité, sécurité, conformité, RTO, RPO, impact, mitigation | [Risques, incidents et enjeux](../pense-bete/systeme-info/systeme-info-si-risques.md) |
| Normes | RGPD, NIS2, DORA, ISO 27001 | [Risques, incidents et enjeux](../pense-bete/systeme-info/systeme-info-si-risques.md) |
| Cas étudiés | CHU de Rouen, fuite Free, incident CrowdStrike | [Analyse des incidents et mitigation](../systeme-info-si/iteration-4/analyse-incidents-mitigation.md) |
| Sécurité SI | segmentation, VLAN, ACL, firewall, chiffrement, redondance, sauvegardes | [Amélioration architecture CHU Rouen](../systeme-info-si/iteration-4/amelioration-architecture-chu-rouen.md) |
| Diagrammes | légende, hypothèses, lisibilité, direction des flux | [Diagrammes SI](../pense-bete/systeme-info/systeme-info-si-diagrammes.md) |
| Posture professionnelle | vérifier, documenter, expliquer, prioriser, rester réaliste | Cette synthèse |

## Formule à garder

**Un bon AIS ne cherche pas seulement à faire fonctionner le SI : il cherche à comprendre ce qui est critique, ce qui peut casser, comment limiter les dégâts et comment reprendre l'activité.**

## Ressource personnelle

Ce mémo doit rester une ressource vivante. Je pourrai l'enrichir avec :

- de nouveaux exemples d'incidents ;
- des schémas plus propres ;
- des définitions ;
- des commandes utiles ;
- des retours d'expérience de stage ou de projet.
