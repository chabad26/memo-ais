# Itération 8 — Vulnérabilités et besoins de détection

| Notion | À retenir |
| --- | --- |
| Présence / exploitabilité | Vérifier fonction, entrée contrôlée, version et options ; association CVE insuffisante |
| Visibilité | Trajet sur virbr0, protocole et chiffrement déterminent ce que l’IDS voit |
| Signal indirect | Un flux inhabituel peut aider sans prouver la CVE exploitée |
| Sources complémentaires | Authentification, auditd, runtime et application pour les actions non lisibles sur le réseau |

- [Des vulnérabilités aux besoins de détection](../../../securisation-avancee-infrastructures/it-8/vulnerabilites-besoins-detection.md)
- [Itération 8](../../../securisation-avancee-infrastructures/it-8/index.md)

- [Rechercher et adapter des règles](../../../securisation-avancee-infrastructures/it-8/rechercher-adapter-regles-detection.md)

## MITRE ATT&CK

Tactique : objectif ; technique : manière d’agir. Partir du comportement,
pas du numéro de CVE. Un marqueur HTTP, un code 401 ou des GET répétés
ne prouvent pas une technique d’attaque ; documenter le contexte manquant.

- [Relier les détections à MITRE ATT&CK](../../../securisation-avancee-infrastructures/it-8/relier-detections-mitre-attack.md)

## Deux points d’observation

Suricata voit les échanges passant sur virbr0 ; l’agent voit les sources
locales accessibles et configurées. Un agent dans le conteneur ne surveille
pas toute la VM. La collecte EVE sur l’hôte doit être configurée séparément.

- [Concevoir les différents points d’observation](../../../securisation-avancee-infrastructures/it-8/concevoir-points-observation.md)

## Wazuh single-node

VM dédiée Ubuntu Server 26.04 ; Docker et Compose dans cette VM.
Trois composants centraux : manager, indexer et dashboard. Utiliser le
dossier single-node officiel, générer les certificats et vérifier les
communications ; des conteneurs Up ou une page de login seuls ne suffisent pas.

- [Installer Wazuh en single-node](../../../securisation-avancee-infrastructures/it-8/installer-wazuh-single-node.md)

## Agent dans File Browser

Examiner la base, les bibliothèques et les droits avant installation.
Tester une image dérivée isolée ; prévoir deux processus et une identité
persistante. Agent actif, collecte et maintien de File Browser sont trois
preuves distinctes. Un échec diagnostiqué est un résultat valable.

- [Étudier l’agent dans File Browser](../../../securisation-avancee-infrastructures/it-8/etudier-agent-wazuh-file-browser.md)
