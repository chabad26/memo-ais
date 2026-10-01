# Constituer le dossier de preuves

## Objectif

Relier chaque décision aux observations qui la justifient, depuis l'audit
initial jusqu'à la proposition d'évolution de la PSSI.

**Statut : modèles à compléter.** Les lignes « À renseigner » ne sont ni des
constats réels ni des résultats de tests. L1 à L7 sont des repères internes.

## Classer les éléments

| Statut | Usage |
| --- | --- |
| Préparatoire | Méthode ou configuration prévue, sans exécution attestée |
| À compléter | Travail commencé, mais information ou preuve manquante |
| Prouvé | Résultat observé, avec contexte, date, auteur et preuve consultable |
| Non concluant | Test effectué dont le résultat ne permet pas de trancher |
| Simulé | Scénario pédagogique ; distinguer ensuite son exécution prévue ou prouvée |

Une simulation peut être réellement exécutée et documentée, sans devenir pour
autant un incident réel de l'organisation. Une capture d'écran d'accueil d'un
outil prouve son accessibilité, pas l'efficacité de toute la chaîne.

## Organiser les productions

| Repère | Contenu attendu | Validation recherchée |
| --- | --- | --- |
| L1 | Périmètre et rapports Greenbone, constats qualifiés et priorités initiales | Les décisions sont justifiées par le contexte et les preuves |
| L2 | Audit Lynis, vérifications manuelles et analyse consolidée de la VM | Les constats locaux sont confirmés, nuancés ou laissés à vérifier |
| L3 | Objet d’image identifié, rapport Trivy et vulnérabilités qualifiées | Chaque résultat est relié à un composant réellement détecté et à ses limites |
| L4 | Capture réseau, configuration Suricata, règles et tests | Une règle chargée détecte le trafic prévu, avec un contrôle négatif |
| L5 | Architecture Wazuh, collecte et recherches | Le même événement est suivi de la source au dashboard |
| L6 | Chronologie, qualification, confinement, remédiation et REX | Faits, hypothèses et décisions sont séparés |
| L7 | Référence PSSI, analyse du fragment et texte proposé | Chaque évolution répond à un enseignement et possède un contrôle |

## Registre des constats

| ID | Actif et composant | Source et preuve | Qualification | Exposition / exploitabilité | Impact métier | Priorité motivée | Action / responsable / échéance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| À renseigner | À renseigner | Rapport, test et date | Confirmé, à vérifier, faux positif ou non applicable | À renseigner | À renseigner | À justifier | À renseigner |

Utiliser des identifiants stables, par exemple `C-001`. Un même défaut vu par
plusieurs outils conserve un seul constat avec plusieurs sources. Ajouter
l'avis de sécurité pertinent et les limites de vérification lorsqu'ils existent.

## Journal des changements

| ID changement / constat | État avant | Modification et auteur | Risque / retour arrière | Contrôle après | Résultat observé et preuve | Risque restant |
| --- | --- | --- | --- | --- | --- | --- |
| À renseigner | À renseigner | Date, machine et configuration | À préparer | Technique et fonctionnel | À renseigner | À qualifier |

Le statut « corrigé » nécessite un contrôle. Le statut « risque accepté »
nécessite une décision attribuée, une justification et une date de réexamen.

## Fiche de test de détection

| Champ | Valeur à conserver |
| --- | --- |
| Identifiant du test | Repère unique, sans secret |
| Configuration | Version de l'outil, interface, périmètre et règle/SID/révision |
| Action de test | Machine source, cible, protocole, heure et trafic attendu |
| Contrôle positif | Alerte attendue et résultat effectivement observé |
| Contrôle négatif | Trafic témoin et absence attendue de cette alerte précise |
| Chaîne de collecte | Événement local, agent, événement Wazuh et délai constaté |
| Limites | Capture, chiffrement, perte de paquets ou scénario non couvert |

## Chronologie d'incident

| Heure de l'événement et fuseau | Heure de collecte | Source / preuve | Fait observé | Hypothèse et confiance | Décision / acteur / résultat |
| --- | --- | --- | --- | --- | --- |
| À renseigner | À renseigner | À renseigner | À renseigner | À vérifier | À renseigner |

Conserver les originaux dans un emplacement protégé. Travailler sur des copies
et noter qui a collecté quoi, quand et comment. Une empreinte SHA-256 aide à
contrôler qu'une copie n'a pas changé ; elle ne prouve pas à elle seule l'origine
ni l'exhaustivité du journal.

## Relier le REX à la PSSI

| Constat / incident | Fragment existant et référence | Limite observée | Évolution proposée | Responsable | Contrôle / preuve / fréquence |
| --- | --- | --- | --- | --- | --- |
| À renseigner | Version, page et paragraphe | À démontrer | Proposition, non approuvée | À désigner | À définir |

## Préparer la restitution

Pour chaque pièce, préciser auteur, machine, date, version, contexte et résultat.
Conserver les rapports complets dans le dossier privé ; publier uniquement les
extraits utiles et anonymisés. Les rapports de scan, journaux et captures réseau
peuvent contenir des identifiants ou des secrets : les relire avant diffusion.

Le dossier final doit expliquer ce qui a été corrigé, ce qui reste ouvert, ce
qui a été détecté et ce qui n'a pas pu être démontré. Aucune mesure de délai ou
de disponibilité ne doit être inventée pour remplir un tableau.

[Retour au module](README.md)
