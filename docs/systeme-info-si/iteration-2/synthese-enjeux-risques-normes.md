# Synthèse : relier enjeux, risques et normes

## Objectif

Construire une vision globale du SI en reliant :

- les enjeux ;
- les risques ;
- les normes ou règlements ;
- des exemples concrets.

L'idée est de vérifier que les travaux précédents restent cohérents entre eux.

## Tableau de synthèse

| Enjeu | Risque associé | Norme concernée (option) | Exemple |
| --- | --- | --- | --- |
| Disponibilité | Panne | ISO 27001 | Indisponibilité du SI CHU |
| Disponibilité | Ransomware sur postes et serveurs | NIS2 / ISO 27001 | Applications métiers indisponibles, retour au papier |
| Sécurité | Fuite de données | RGPD / NIS2 | Dossier patient exposé ou compte compromis |
| Sécurité | Compte administrateur compromis | ISO 27001 / NIS2 | Propagation vers serveurs, sauvegardes ou données |
| Évolutivité | Système incapable de supporter la charge | ISO 27001 | Portail de rendez-vous saturé lors d'un pic de connexions |
| Intégration | Système legacy difficile à connecter | ISO 27001 | Ancien logiciel labo mal relié au DPI |
| Intégration | Middleware ou API indisponible | ISO 27001 / NIS2 | Résultats labo ou imagerie non transmis au DPI |
| Conformité | Non-respect des obligations RGPD | RGPD | Données conservées trop longtemps ou accès non tracés |
| Conformité | Prestataire mal encadré | RGPD / NIS2 / DORA selon contexte | Accès externe trop large ou contrat insuffisant |
| Disponibilité | Sauvegardes non isolées | ISO 27001 / NIS2 | Restauration impossible après chiffrement |
| Sécurité | Phishing via messagerie | ISO 27001 / NIS2 | Vol d'identifiants utilisateur |
| Conformité | Défaut de notification ou de gestion d'incident | RGPD / NIS2 / DORA | Incident non remonté dans les délais attendus |

## À compléter dans mon mémo

| Enjeu | Risque associé | Norme concernée (option) | Exemple |
| --- | --- | --- | --- |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

## Méthode

1. Reprendre les enjeux identifiés : disponibilité, sécurité, évolutivité, intégration, conformité.
2. Associer un ou plusieurs risques à chaque enjeu.
3. Ajouter une norme ou un règlement si un lien existe.
4. Donner un exemple concret.
5. Supprimer les doublons et garder les lignes les plus claires.

## Questions de cohérence

- Est-ce que chaque risque est bien relié à un enjeu ?
- Est-ce que la norme citée est vraiment pertinente ?
- Est-ce que l'exemple est concret ?
- Est-ce qu'on distingue bien la cause, le risque et l'impact ?
- Est-ce que le tableau reste lisible ?

## Résultat attendu

Le résultat attendu est un **tableau de synthèse** clair.

Il doit montrer clairement le lien :

**enjeu → risque → norme éventuelle → exemple concret**

## À retenir

Une vision systémique du SI consiste à relier les notions entre elles.

Un même risque peut toucher plusieurs enjeux :

- un ransomware touche la disponibilité, la sécurité et parfois la conformité ;
- un prestataire mal encadré touche la sécurité, l'intégration et la conformité ;
- une sauvegarde mal protégée touche la disponibilité et la sécurité.
