# Itération 5 — Bilan du durcissement et préparation du fragment de PSSI

## Objectif

Conclure sur les remédiations réalisées, distinguer les risques corrigés des
risques résiduels, puis transformer les problèmes organisationnels du cas
File Browser en propositions de règles. Préparer les sujets du fragment de
PSSI qui sera élaboré en J6.

**Itération terminée le 5 octobre 2026 selon le retour d’Olivier.** Les
contrôles manuels, Greenbone et Lynis ont été refaits avec des résultats
inchangés par rapport au 2 octobre. Les pièces détaillées J5 restent à joindre.
Les propositions de règles sont préparées ; elles ne constituent pas une
PSSI adoptée ni une validation acquise de C2.

## Parcours réalisé

| Étape | Feuille | Travail et résultat |
| --- | --- | --- |
| 1 | [Vérifier l’état du système après remédiation](verifier-etat-systeme-apres-remediation.md) | Comparaison J3/J4/J5, contrôles pertinents, résultats stables déclarés et limites de preuve ; Trivy non relancé, image déclarée inchangée |
| 2 | [Finaliser le compte-rendu de durcissement et de vérification](finaliser-compte-rendu-durcissement-verification.md) | Traçabilité R01–R09, effet des protections, maintien du fonctionnement, diagnostics, état final et risques résiduels |
| 3 | [Identifier ce que la technique ne règle pas](identifier-ce-que-technique-ne-regle-pas.md) | Responsabilités, maintenance, suivi des alertes, exposition et cycle de vie du service |
| 4 | [Analyser une PSSI existante — Université de Poitiers](analyser-pssi-existante-poitiers.md) | Structure, responsabilités et sept règles référencées ; applicabilité et adaptations au cas File Browser |
| 5 | [Proposer des règles adaptées au cas fil rouge](proposer-regles-adaptees-cas-fil-rouge.md) | Huit propositions P01–P08, avec problème, objectif, destinataire, responsable et contrôle |
| 6 | [Préparer le fragment de PSSI](preparer-fragment-pssi.md) | Regroupement en cinq sujets, ancrage dans les faits du cas et plan de rédaction J6 |

## Bilan technique et limites

Les mesures vérifiées en J4 portent sur la migration, SSH, Docker, auditd,
CUPS, sysctl, les identifiants et la reprise du service. Les contrôles J5
refaits sont déclarés stables ; les nouveaux rapports et sorties ne sont pas
encore annexés. Aucun nouveau problème n’est signalé dans ce retour.

Les alertes non qualifiées, les dix HIGH Trivy de l’export précédent et la
fin de maintenance File Browser restent documentés. Une image inchangée
peut recevoir de nouvelles associations de vulnérabilités si les bases du
scanner évoluent. La stabilité des résultats ne signifie pas l’absence de
risque et les compteurs ne suffisent pas à conclure à une sécurité globale.

## Bilan organisationnel

Le cas montre qu’une correction technique ne désigne pas le mainteneur futur,
ne garantit pas le suivi des alertes et ne décide pas du retrait d’un service.
La préparation du fragment est organisée autour de cinq sujets :

1. Responsabilités de maintenance et transmission.
2. Maintenance et suivi des vulnérabilités.
3. Exposition et accès des partenaires.
4. Contrôles, écarts et exceptions.
5. Cycle de vie, remplacement et retrait.

Chaque sujet est relié à un problème du cas, à des rôles, à des règles
proposées et à des preuves de contrôle. Les responsables nominatifs, délais,
fréquences, moyens et autorités de validation restent à arbitrer.

## Livrables de l’itération

- Compte-rendu de durcissement et de vérification renseigné, avec limites des preuves J5.
- Analyse des problèmes organisationnels et de la PSSI de référence.
- Huit propositions de règles adaptées au service.
- Plan du fragment de PSSI, à développer en J6.

**Suite en J6 :** élaborer une première version du fragment à partir de la
[préparation](preparer-fragment-pssi.md), sans transformer les propositions en
règles déjà approuvées. L’annexion des pièces J5 complète le dossier de preuve
sans nécessiter une nouvelle extension automatique du durcissement.

- [Compte-rendu J4](../it-4/finaliser-compte-rendu-durcissement.md)
- [Rapport d’audit et plan initial J3](../it-3/finaliser-rapport-plan-remediation.md)
- [Retour au module](../README.md)
