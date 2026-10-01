# Itération 3 — Analyser l’image du conteneur

## Objectif

Compléter l’audit de la VM par une analyse de l’image File Browser, en
distinguant clairement l’hôte Ubuntu, le conteneur en cours d’exécution, l’image
et les données montées.

**Statut : scan et inventaire Trivy réalisés ; qualification à poursuivre.**
Trivy 0.74.0 est installé sur la machine d’audit. L’image exacte a été
identifiée, exportée puis transférée avec une empreinte SHA-256 identique. Le
scan a réussi et produit un rapport JSON. Trivy a reconnu Alpine 3.13.4 avec
20 paquets système ainsi que 53 composants du binaire Go. L’extraction recense
294 associations composant–vulnérabilité, dont 13 critiques. Cinq résultats ont
été vérifiés : quatre sont non pertinents dans la configuration observée et un
reste à vérifier. Des exports séparés regroupent les résultats `CRITICAL`,
`HIGH` et l’ensemble `HIGH` + `CRITICAL` demandé par la formatrice. La
consolidation finale ajoute un seul constat structurel sur l’image hors support.

## Activités

- [Identifier ce qui manque dans l’audit](identifier-manques-audit.md) : reprendre
  l’audit consolidé du J2, séparer les informations connues des inconnues et
  expliquer pourquoi Greenbone, Lynis et les contrôles manuels ne suffisent pas.
- [Analyser l’image avec Trivy](analyser-image-trivy.md) — **1 h** : installer
  l’outil sur la machine d’audit, scanner l’image exacte, conserver le rapport
  et identifier composants, versions, CVE, sévérités et correctifs indiqués.
- [Analyser et vérifier les résultats Trivy](analyser-verifier-resultats-trivy.md) :
  sélectionner cinq résultats significatifs, vérifier leurs conditions dans le
  code, le binaire et l’exposition réelle, puis statuer sur leur applicabilité.
- [Consolider les trois sources d’audit](consolider-trois-sources-audit.md) :
  intégrer Greenbone, Lynis, Trivy, les contrôles manuels et les références CVE
  dans un tableau unique, sans dupliquer les problèmes.

- [Évaluer les risques et définir les priorités](evaluer-risques-definir-priorites.md) — **1 h 15** :
  justifier les priorités selon le risque pour ce serveur et les limites
  des preuves disponibles.

- [Finaliser le rapport d’audit et le plan de remédiation](finaliser-rapport-plan-remediation.md) — **2 h** :
  produire la synthèse finale, regrouper les actions et préparer leur validation
  à partir du J4.

## Périmètres à ne pas confondre

| Objet | Exemple dans le laboratoire | Question principale |
| --- | --- | --- |
| Hôte | VM Ubuntu 20.04 | Quels paquets, services et paramètres protègent le moteur Docker ? |
| Conteneur | Instance `filebrowser` | Avec quels droits et montages l’application s’exécute-t-elle ? |
| Image | ImageID `sha256:a68f…e1a5` | Quels composants sont intégrés dans les couches de l’image ? |
| Application | File Browser 2.15.0 | Quelles vulnérabilités concernent réellement cette version et sa configuration ? |
| Données | `/srv/filebrowser` monté dans `/srv` | Qui peut lire ou modifier les documents servis ? |

Un résultat obtenu sur un objet ne doit pas être automatiquement attribué aux
autres. Une CVE d’un paquet Ubuntu de l’hôte n’est pas une CVE de l’image, et un
scan sans résultat ne garantit pas l’absence de vulnérabilité.

## Preuves attendues pour l’itération

- objet analysé identifié par ImageID et, si disponible, RepoDigest ;
- version de Trivy et date de sa base ;
- commande exacte, scanners et options utilisés ;
- rapport conservé avec date et empreinte ;
- composants et versions détectés, erreurs et éléments non identifiés ;
- qualification des résultats avec les références des vulnérabilités ;
- distinction entre résultat de l’image, configuration du conteneur et données
  montées.

## État final attendu et preuves L3

Un rapport d’analyse d’image reproductible complète les constats Greenbone et
Lynis. Chaque vulnérabilité retenue est rattachée à un composant réellement
détecté et à une condition d’applicabilité. Les limites du scanner et les
composants non identifiés restent visibles.

- [Pense-bête de l’itération](../../pense-bete/glossaire/securisation-avancee-infrastructures/it-3.md)
- [Étape précédente — Itération 2](../it-2/index.md)
- [Étape suivante — Détection Suricata](../it-4/index.md)
- [Retour au module](../README.md)
