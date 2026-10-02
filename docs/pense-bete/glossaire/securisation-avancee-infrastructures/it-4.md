# Pense-bête — Sécurisation avancée : Suricata en individuel

## Périmètre

Itération 4 de la progression prévisionnelle du module. Cette fiche prépare
les notions et les gestes ; les résultats seront ajoutés après les activités.

## Termes à retenir

| Terme | Définition courte |
| --- | --- |
| IDS | Dispositif qui détecte et signale des événements ; le blocage est une fonction distincte. |
| IPS | Dispositif placé pour intervenir sur le trafic et appliquer des actions de prévention. |
| HOME_NET | Variable Suricata décrivant le réseau protégé. |
| SID / révision | Identifiant d'une signature Suricata et version de cette règle. |
| EVE JSON | Sortie structurée des événements produits par Suricata. |
| Test positif | Trafic choisi pour déclencher la règle attendue. |
| Test négatif | Trafic témoin qui ne doit pas déclencher cette règle précise. |
| Visibilité | Trafic réellement reçu par l'interface de la sonde. |

## Manipulations faites

Aucune manipulation de cette itération n'est encore documentée. La préparation
de la fiche ne constitue pas une preuve d'audit, de déploiement ou de test.

## Gestes et commandes à retenir

- Documenter le chemin du trafic et vérifier la capture avant les règles.
- Vérifier version, interface, réseau protégé et règles chargées.
- Prévoir `suricata -T` avec le fichier de configuration adapté avant application.
- Conserver SID, révision, horodatage et adresses pour chaque test.
- Interpréter les limites liées au TLS, aux flux non visibles et aux pertes de paquets.

## Preuves attendues

Configuration valide, visibilité démontrée et tests positif/négatif documentés.

## Docs associées

- [Feuille de l'itération 4](../../../securisation-avancee-infrastructures/it-4/index.md)
- [Dossier de preuves](../../../securisation-avancee-infrastructures/dossier-preuves.md)
- [Vue d'ensemble du module](../../../securisation-avancee-infrastructures/README.md)

## Préparation des remédiations

La [feuille de préparation](../../../securisation-avancee-infrastructures/it-4/preparer-remediations.md)
reprend les constats du J3, les actions retenues, les validations de sécurité et
de fonctionnement et les retours arrière. Les changements restent à réaliser ;
la connexion File Browser avec les identifiants par défaut est confirmée selon
le test utilisateur.

- [Mettre en œuvre et vérifier les remédiations](../../../securisation-avancee-infrastructures/it-4/mettre-en-oeuvre-verifier-remediations.md) :
  méthode, contrôles, résultats et diagnostic ; les validations restent à réaliser.
