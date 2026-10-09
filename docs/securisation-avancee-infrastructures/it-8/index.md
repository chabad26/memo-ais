# Itération 8 — Des constats d’audit au réglage de la détection

**8 octobre 2026 — Travail individuel**

Reprendre les constats J1–J3 pour choisir des besoins de détection adaptés
au trafic réellement visible. La détection complète la remédiation ; elle ne
corrige ni les versions, ni les privilèges, ni les règles de pare-feu.

- [Des vulnérabilités aux besoins de détection — 1 h](vulnerabilites-besoins-detection.md)
- [Rechercher et adapter des règles de détection — 1 h 15](rechercher-adapter-regles-detection.md)
- [Relier les détections à MITRE ATT&CK](relier-detections-mitre-attack.md)
- [Concevoir les différents points d’observation](concevoir-points-observation.md)
- [Installer Wazuh en single-node — travail en groupe](installer-wazuh-single-node.md)
- [Peut-on installer un agent Wazuh dans le conteneur File Browser ?](etudier-agent-wazuh-file-browser.md)
- [Pense-bête](../../pense-bete/glossaire/securisation-avancee-infrastructures/it-8.md)
- [Bilan Suricata précédent](../it-7/bilan-dispositif-detection.md)
- [Retour au module](../README.md)

**Statut : analyse documentaire réalisée ; capture de validation de sept
signatures et d’une alerte locale 1008001 sur File Browser:8080 intégrée.
Validation des alertes 1008002 et 1008003 à compléter ; test par marqueur
inerte, sans preuve d’exploitation.**

**Cible Wazuh retenue : VM dédiée Ubuntu Server 26.04**, exécutant la stack
Docker single-node officielle ; adresse observée `192.168.122.37` ; dashboard et indexer green illustrés ; logs File Browser reçus par le manager
via un agent sur la VM, avec décodeur JSON. Alerte spécifique à valider.

**Suite :** [Itération 9 — reprendre le dispositif de détection](../it-9/index.md).
